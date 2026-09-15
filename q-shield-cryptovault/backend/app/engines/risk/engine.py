"""Unified Quantum-Cyber Risk Engine (Section 19-21 / Phase 8 core innovation).

Combines five independent risk dimensions into one transparent, deterministic
Unified Quantum-Cyber Risk Score using weights from configuration (not
scattered through code). Risk-level thresholds are Q-Shield prototype policy
thresholds, NOT an industry-standard scoring system (Section 20).
"""
from dataclasses import dataclass, field

from app.core.config import Settings


@dataclass
class RiskBreakdown:
    cyber_score: float
    behaviour_score: float
    anomaly_score: float
    crypto_score: float
    quantum_score: float
    unified_score: float
    risk_level: str
    primary_contributors: list[str] = field(default_factory=list)


def _risk_level(score: float, settings: Settings) -> str:
    if score <= settings.risk_threshold_low:
        return "LOW"
    if score <= settings.risk_threshold_moderate:
        return "MODERATE"
    if score <= settings.risk_threshold_high:
        return "HIGH"
    return "CRITICAL"


def calculate_unified_risk(
    *,
    cyber_score: float,
    behaviour_score: float,
    anomaly_score: float,
    crypto_score: float,
    quantum_score: float,
    contributor_triggers: list[str],
    settings: Settings,
) -> RiskBreakdown:
    unified_score = (
        cyber_score * settings.risk_weight_cyber
        + behaviour_score * settings.risk_weight_behaviour
        + anomaly_score * settings.risk_weight_anomaly
        + crypto_score * settings.risk_weight_crypto
        + quantum_score * settings.risk_weight_quantum
    )
    unified_score = round(unified_score, 2)
    risk_level = _risk_level(unified_score, settings)

    dimension_scores = {
        "Cyber Risk": cyber_score,
        "Behaviour Risk": behaviour_score,
        "Anomaly Risk": anomaly_score,
        "Crypto Risk": crypto_score,
        "Quantum Risk": quantum_score,
    }
    contributors = list(dict.fromkeys(contributor_triggers))
    if crypto_score >= 70:
        contributors.append("Cryptographic profile requires quantum-readiness review")
    high_dimensions = [name for name, val in dimension_scores.items() if val >= 70]
    if high_dimensions and not contributors:
        contributors.append(f"Elevated {high_dimensions[0]}")

    return RiskBreakdown(
        cyber_score=cyber_score,
        behaviour_score=behaviour_score,
        anomaly_score=anomaly_score,
        crypto_score=crypto_score,
        quantum_score=quantum_score,
        unified_score=unified_score,
        risk_level=risk_level,
        primary_contributors=contributors,
    )
