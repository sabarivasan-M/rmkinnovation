from pydantic import BaseModel


class BehaviourOut(BaseModel):
    behaviour_score: float
    triggers: list[str]


class AnomalyOut(BaseModel):
    anomaly_score: float
    is_anomalous: bool
    triggers: list[str]


class CryptoOut(BaseModel):
    algorithm: str
    key_type: str
    signature_type: str
    security_category: str
    quantum_exposure: str
    migration_status: str
    crypto_score: float


class QuantumOut(BaseModel):
    simulation_status: str
    qubit_count: int
    circuit_depth: int
    simulation_result: dict
    security_interpretation: str
    quantum_score: float
    migration_priority: str


class RiskOut(BaseModel):
    cyber_score: float
    behaviour_score: float
    anomaly_score: float
    crypto_score: float
    quantum_score: float
    unified_score: float
    risk_level: str
    primary_contributors: list[str]


class DecisionOut(BaseModel):
    decision: str
    risk_level: str
    score: float
    reason: str
    policy_trigger: str
    confidence: float


class BlockchainAuditOut(BaseModel):
    status: str
    tx_hash: str
    block_number: int
    network: str


class TransactionAnalysisOut(BaseModel):
    transaction_id: str
    behaviour: BehaviourOut
    anomaly: AnomalyOut
    crypto: CryptoOut
    quantum: QuantumOut
    risk: RiskOut
    decision: DecisionOut
    blockchain: BlockchainAuditOut
