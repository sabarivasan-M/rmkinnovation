"""Q-Shield core pipeline (Section 4 / Phases 4-11):

CAPTURE -> AUTHENTICATE -> BEHAVIOUR -> ANOMALY -> CRYPTO -> QUANTUM
        -> RISK QUANTIFICATION -> DECISION -> BLOCKCHAIN LOG

This is the single place that wires the independent engines together. No
engine talks to another engine directly - this module is the only caller of
all of them, so the pipeline stays inspectable and each engine stays unit
testable in isolation.
"""
import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.blockchain.service import record_security_decision
from app.core.config import get_settings
from app.engines.anomaly.engine import detect_anomaly
from app.engines.behaviour.engine import analyse_behaviour
from app.engines.crypto.engine import assess_crypto_profile
from app.engines.decision.engine import decide
from app.engines.quantum.engine import assess_quantum_exposure
from app.engines.risk.cyber import compute_cyber_score
from app.engines.risk.engine import calculate_unified_risk
from app.models.anomaly_result import AnomalyResult
from app.models.audit_log import AuditLog
from app.models.behaviour_profile import BehaviourProfile
from app.models.crypto_assessment import CryptoAssessment
from app.models.quantum_assessment import QuantumAssessment
from app.models.risk_assessment import RiskAssessment
from app.models.security_decision import SecurityDecision
from app.models.transaction import Transaction
from app.schemas.analysis import (
    AnomalyOut,
    BehaviourOut,
    BlockchainAuditOut,
    CryptoOut,
    DecisionOut,
    QuantumOut,
    RiskOut,
    TransactionAnalysisOut,
)
from app.schemas.transaction import TransactionCreate
from app.services.id_generator import generate_transaction_id
from app.services.wallet_service import count_transactions_today, get_or_create_wallet, has_transacted_before

logger = logging.getLogger("qshield.pipeline")


def analyse_transaction(db: Session, payload: TransactionCreate) -> TransactionAnalysisOut:
    settings = get_settings()

    # ---- CAPTURE ----
    sender = get_or_create_wallet(db, payload.sender_address)
    get_or_create_wallet(db, payload.receiver_address)
    is_new_recipient = not has_transacted_before(db, payload.sender_address, payload.receiver_address)

    transaction_id = generate_transaction_id(db)
    transaction = Transaction(
        transaction_id=transaction_id,
        sender_address=payload.sender_address,
        receiver_address=payload.receiver_address,
        amount=payload.amount,
        currency=payload.currency,
        transaction_type=payload.transaction_type,
        authentication_status=payload.authentication_status,
        status="ANALYSING",
        is_new_recipient=is_new_recipient,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    logger.info("Transaction received: %s", transaction_id)

    hour_of_day = (
        payload.simulated_hour_of_day
        if payload.simulated_hour_of_day is not None
        else datetime.now(timezone.utc).hour
    )
    tx_count_today = count_transactions_today(db, payload.sender_address)

    # ---- BEHAVIOUR ANALYSIS ----
    behaviour = analyse_behaviour(
        amount=payload.amount,
        hour_of_day=hour_of_day,
        is_new_recipient=is_new_recipient,
        wallet_avg_amount=sender.avg_transaction_amount,
        wallet_usual_tx_per_day=sender.usual_transactions_per_day,
        recent_tx_count_today=tx_count_today,
        wallet_failed_auth_count=sender.failed_auth_count,
    )
    db.add(
        BehaviourProfile(
            transaction_id=transaction_id,
            behaviour_score=behaviour.behaviour_score,
            amount_deviation=behaviour.amount_deviation,
            velocity_score=behaviour.velocity_score,
            new_recipient_penalty=behaviour.new_recipient_penalty,
            time_of_day_penalty=behaviour.time_of_day_penalty,
            auth_failure_penalty=behaviour.auth_failure_penalty,
            triggers=behaviour.triggers,
        )
    )
    logger.info("Behaviour analysis completed: %s -> %.2f", transaction_id, behaviour.behaviour_score)

    # ---- ANOMALY DETECTION ----
    velocity_ratio = tx_count_today / max(sender.usual_transactions_per_day, 1.0)
    anomaly = detect_anomaly(
        amount=payload.amount,
        hour_of_day=hour_of_day,
        is_new_recipient=is_new_recipient,
        velocity_ratio=velocity_ratio,
        failed_auth_count=sender.failed_auth_count,
    )
    db.add(
        AnomalyResult(
            transaction_id=transaction_id,
            anomaly_score=anomaly.anomaly_score,
            is_anomalous=anomaly.is_anomalous,
            triggers=anomaly.triggers,
        )
    )
    logger.info("Anomaly detection completed: %s -> %.2f", transaction_id, anomaly.anomaly_score)

    # ---- CRYPTOGRAPHIC ASSESSMENT ----
    crypto = assess_crypto_profile(sender.crypto_algorithm)
    db.add(
        CryptoAssessment(
            transaction_id=transaction_id,
            algorithm=crypto.algorithm,
            key_type=crypto.key_type,
            signature_type=crypto.signature_type,
            security_category=crypto.security_category,
            quantum_exposure=crypto.quantum_exposure,
            migration_status=crypto.migration_status,
            crypto_score=crypto.crypto_score,
        )
    )
    logger.info("Crypto assessment completed: %s -> %s", transaction_id, crypto.algorithm)

    # ---- QUANTUM ASSESSMENT ----
    quantum = assess_quantum_exposure(crypto.quantum_exposure)
    db.add(
        QuantumAssessment(
            transaction_id=transaction_id,
            simulation_status=quantum.simulation_status,
            qubit_count=quantum.qubit_count,
            circuit_depth=quantum.circuit_depth,
            simulation_result=quantum.simulation_result,
            security_interpretation=quantum.security_interpretation,
            quantum_score=quantum.quantum_score,
            migration_priority=quantum.migration_priority,
        )
    )
    logger.info("Quantum simulation completed: %s -> %s", transaction_id, quantum.simulation_status)

    # ---- CYBER RISK ----
    cyber_score = compute_cyber_score(
        authentication_status=payload.authentication_status,
        wallet_age_days=sender.wallet_age_days,
        wallet_failed_auth_count=sender.failed_auth_count,
    )

    # ---- UNIFIED RISK QUANTIFICATION ----
    all_triggers = behaviour.triggers + anomaly.triggers
    risk = calculate_unified_risk(
        cyber_score=cyber_score,
        behaviour_score=behaviour.behaviour_score,
        anomaly_score=anomaly.anomaly_score,
        crypto_score=crypto.crypto_score,
        quantum_score=quantum.quantum_score,
        contributor_triggers=all_triggers,
        settings=settings,
    )
    db.add(
        RiskAssessment(
            transaction_id=transaction_id,
            cyber_score=risk.cyber_score,
            behaviour_score=risk.behaviour_score,
            anomaly_score=risk.anomaly_score,
            crypto_score=risk.crypto_score,
            quantum_score=risk.quantum_score,
            unified_score=risk.unified_score,
            risk_level=risk.risk_level,
            primary_contributors=risk.primary_contributors,
        )
    )
    logger.info("Risk score calculated: %s -> %.2f (%s)", transaction_id, risk.unified_score, risk.risk_level)

    # ---- SECURITY DECISION ----
    decision = decide(
        unified_score=risk.unified_score,
        risk_level=risk.risk_level,
        authentication_status=payload.authentication_status,
    )
    db.add(
        SecurityDecision(
            transaction_id=transaction_id,
            decision=decision.decision,
            risk_level=decision.risk_level,
            score=decision.score,
            reason=decision.reason,
            policy_trigger=decision.policy_trigger,
            confidence=decision.confidence,
        )
    )
    transaction.status = decision.decision
    logger.info("Decision generated: %s -> %s", transaction_id, decision.decision)

    # ---- BLOCKCHAIN AUDIT LOG ----
    blockchain_result = record_security_decision(transaction_id, risk.unified_score, decision.decision)
    db.add(
        AuditLog(
            event="SECURITY_DECISION",
            transaction_id=transaction_id,
            risk_score=risk.unified_score,
            decision=decision.decision,
            blockchain_reference=blockchain_result.tx_hash,
            blockchain_status=blockchain_result.status,
            block_number=blockchain_result.block_number,
        )
    )
    if blockchain_result.status == "CONFIRMED":
        logger.info("Blockchain audit submitted: %s -> block #%d", transaction_id, blockchain_result.block_number)
    else:
        logger.warning("Blockchain audit unavailable for %s - decision remains recorded in database", transaction_id)

    db.commit()

    return TransactionAnalysisOut(
        transaction_id=transaction_id,
        behaviour=BehaviourOut(behaviour_score=behaviour.behaviour_score, triggers=behaviour.triggers),
        anomaly=AnomalyOut(
            anomaly_score=anomaly.anomaly_score, is_anomalous=anomaly.is_anomalous, triggers=anomaly.triggers
        ),
        crypto=CryptoOut(
            algorithm=crypto.algorithm,
            key_type=crypto.key_type,
            signature_type=crypto.signature_type,
            security_category=crypto.security_category,
            quantum_exposure=crypto.quantum_exposure,
            migration_status=crypto.migration_status,
            crypto_score=crypto.crypto_score,
        ),
        quantum=QuantumOut(
            simulation_status=quantum.simulation_status,
            qubit_count=quantum.qubit_count,
            circuit_depth=quantum.circuit_depth,
            simulation_result=quantum.simulation_result,
            security_interpretation=quantum.security_interpretation,
            quantum_score=quantum.quantum_score,
            migration_priority=quantum.migration_priority,
        ),
        risk=RiskOut(
            cyber_score=risk.cyber_score,
            behaviour_score=risk.behaviour_score,
            anomaly_score=risk.anomaly_score,
            crypto_score=risk.crypto_score,
            quantum_score=risk.quantum_score,
            unified_score=risk.unified_score,
            risk_level=risk.risk_level,
            primary_contributors=risk.primary_contributors,
        ),
        decision=DecisionOut(
            decision=decision.decision,
            risk_level=decision.risk_level,
            score=decision.score,
            reason=decision.reason,
            policy_trigger=decision.policy_trigger,
            confidence=decision.confidence,
        ),
        blockchain=BlockchainAuditOut(
            status=blockchain_result.status,
            tx_hash=blockchain_result.tx_hash,
            block_number=blockchain_result.block_number,
            network=blockchain_result.network,
        ),
    )
