export type RiskLevel = "LOW" | "MODERATE" | "HIGH" | "CRITICAL";
export type Decision = "APPROVE" | "FLAG" | "REJECT";

export interface TransactionSummary {
  transaction_id: string;
  sender_address: string;
  receiver_address: string;
  amount: number;
  currency: string;
  status: string;
  timestamp: string;
  unified_score: number | null;
  risk_level: RiskLevel | null;
  decision: Decision | null;
}

export interface BehaviourOut {
  behaviour_score: number;
  triggers: string[];
}

export interface AnomalyOut {
  anomaly_score: number;
  is_anomalous: boolean;
  triggers: string[];
}

export interface CryptoOut {
  algorithm: string;
  key_type: string;
  signature_type: string;
  security_category: string;
  quantum_exposure: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  migration_status: string;
  crypto_score: number;
}

export interface QuantumOut {
  simulation_status: string;
  qubit_count: number;
  circuit_depth: number;
  simulation_result: Record<string, number>;
  security_interpretation: string;
  quantum_score: number;
  migration_priority: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
}

export interface RiskOut {
  cyber_score: number;
  behaviour_score: number;
  anomaly_score: number;
  crypto_score: number;
  quantum_score: number;
  unified_score: number;
  risk_level: RiskLevel;
  primary_contributors: string[];
}

export interface DecisionOut {
  decision: Decision;
  risk_level: RiskLevel;
  score: number;
  reason: string;
  policy_trigger: string;
  confidence: number;
}

export interface BlockchainAuditOut {
  status: "CONFIRMED" | "UNAVAILABLE";
  tx_hash: string;
  block_number: number;
  network: string;
}

export interface TransactionAnalysisOut {
  transaction_id: string;
  behaviour: BehaviourOut;
  anomaly: AnomalyOut;
  crypto: CryptoOut;
  quantum: QuantumOut;
  risk: RiskOut;
  decision: DecisionOut;
  blockchain: BlockchainAuditOut;
}

export interface SystemStatus {
  api: string;
  database: string;
  risk_engine: string;
  quantum_simulator: string;
  blockchain: string;
}

export interface DashboardSummary {
  transactions_analysed: number;
  high_risk_count: number;
  critical_count: number;
  quantum_exposed_count: number;
  system_status: SystemStatus;
}

export interface RiskActivityPoint {
  timestamp: string;
  unified_score: number;
  risk_level: RiskLevel;
}

export interface AuditLogEntry {
  event: string;
  transaction_id: string;
  risk_score: number;
  decision: string;
  blockchain_reference: string;
  blockchain_status: string;
  block_number: number;
  timestamp: string;
}

export interface Wallet {
  address: string;
  label: string;
  crypto_algorithm: string;
}

export interface ScenarioInfo {
  key: string;
  label: string;
  expected: string;
}

export interface SecurityAlert {
  severity: RiskLevel;
  message: string;
  transaction_id: string;
  timestamp: string;
}
