import axios from "axios";
import type {
  AuditLogEntry,
  DashboardSummary,
  RiskActivityPoint,
  ScenarioInfo,
  SecurityAlert,
  TransactionAnalysisOut,
  TransactionSummary,
  Wallet,
} from "../types";

export const api = axios.create({
  baseURL: "/api/v1",
  timeout: 15000,
});

export interface TransactionCreatePayload {
  sender_address: string;
  receiver_address: string;
  amount: number;
  currency: string;
  authentication_status: "SUCCESS" | "FAILED";
  simulated_hour_of_day?: number;
}

export async function fetchHealth() {
  const { data } = await api.get("/health");
  return data as { status: string; service: string; version: string };
}

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const { data } = await api.get("/dashboard/summary");
  return data;
}

export async function fetchRiskActivity(): Promise<RiskActivityPoint[]> {
  const { data } = await api.get("/dashboard/risk-activity");
  return data;
}

export async function fetchRiskDistribution(): Promise<Record<string, number>> {
  const { data } = await api.get("/dashboard/risk-distribution");
  return data;
}

export async function fetchDecisionDistribution(): Promise<Record<string, number>> {
  const { data } = await api.get("/dashboard/decision-distribution");
  return data;
}

export async function fetchAlerts(): Promise<SecurityAlert[]> {
  const { data } = await api.get("/dashboard/alerts");
  return data;
}

export async function fetchTransactions(limit = 50): Promise<TransactionSummary[]> {
  const { data } = await api.get("/transactions", { params: { limit } });
  return data;
}

export async function fetchTransactionDetail(transactionId: string) {
  const { data } = await api.get(`/transactions/${transactionId}`);
  return data;
}

export async function analyseTransaction(payload: TransactionCreatePayload): Promise<TransactionAnalysisOut> {
  const { data } = await api.post("/transactions", payload);
  return data;
}

export async function fetchWallets(): Promise<Wallet[]> {
  const { data } = await api.get("/wallets");
  return data;
}

export async function fetchScenarios(): Promise<ScenarioInfo[]> {
  const { data } = await api.get("/scenarios");
  return data;
}

export async function runScenario(key: string): Promise<TransactionAnalysisOut> {
  const { data } = await api.post(`/scenarios/${key}/run`);
  return data;
}

export async function fetchAuditLogs(limit = 100): Promise<AuditLogEntry[]> {
  const { data } = await api.get("/audit", { params: { limit } });
  return data;
}

export async function fetchQuantumStatus() {
  const { data } = await api.get("/quantum/status");
  return data;
}

export async function fetchQuantumAssessments(limit = 20) {
  const { data } = await api.get("/quantum", { params: { limit } });
  return data as Array<{
    transaction_id: string;
    quantum_score: number;
    migration_priority: string;
    circuit_depth: number;
    qubit_count: number;
  }>;
}

export async function fetchRiskPolicy() {
  const { data } = await api.get("/risk/policy");
  return data;
}

export async function reviewDecision(transactionId: string, action: "APPROVE" | "REJECT" | "KEEP_FLAGGED") {
  const { data } = await api.post(`/decisions/${transactionId}/review`, { action });
  return data;
}
