import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, Blocks, Brain, Cpu, Lock, ShieldQuestion } from "lucide-react";
import Card from "../components/Card";
import StatusBadge from "../components/StatusBadge";
import { fetchTransactionDetail, reviewDecision } from "../services/api";

const RISK_LEVEL_BG: Record<string, string> = {
  LOW: "from-emerald-500 to-emerald-600",
  MODERATE: "from-amber-500 to-amber-600",
  HIGH: "from-orange-500 to-orange-600",
  CRITICAL: "from-red-600 to-red-700",
};

const DECISION_ICON_BG: Record<string, string> = {
  APPROVE: "bg-emerald-600",
  FLAG: "bg-amber-600",
  REJECT: "bg-red-600",
};

function DimensionBar({ label, score }: { label: string; score: number }) {
  const color = score >= 70 ? "bg-red-500" : score >= 40 ? "bg-amber-500" : "bg-emerald-500";
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-500 font-medium">{label}</span>
        <span className="text-navy font-semibold">{score.toFixed(0)}</span>
      </div>
      <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
        <div className={`h-full ${color} transition-all`} style={{ width: `${Math.min(score, 100)}%` }} />
      </div>
    </div>
  );
}

export default function TransactionDetail() {
  const { transactionId } = useParams();
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [reviewing, setReviewing] = useState(false);

  const load = () => {
    if (!transactionId) return;
    fetchTransactionDetail(transactionId)
      .then(setData)
      .catch(() => setError("Transaction not found or backend unavailable."));
  };

  useEffect(load, [transactionId]);

  async function handleReview(action: "APPROVE" | "REJECT" | "KEEP_FLAGGED") {
    if (!transactionId) return;
    setReviewing(true);
    try {
      await reviewDecision(transactionId, action);
      load();
    } finally {
      setReviewing(false);
    }
  }

  if (error) {
    return (
      <div className="space-y-4">
        <Link to="/transactions" className="text-sm text-accent flex items-center gap-1">
          <ArrowLeft size={14} /> Back to Transactions
        </Link>
        <Card>
          <p className="text-sm text-critical">{error}</p>
        </Card>
      </div>
    );
  }

  if (!data) return <p className="text-sm text-slate-400">Loading transaction analysis...</p>;

  const { transaction, behaviour, anomaly, crypto, quantum, risk, decision, blockchain } = data;

  return (
    <div className="space-y-6">
      <Link to="/transactions" className="text-sm text-accent flex items-center gap-1 w-fit">
        <ArrowLeft size={14} /> Back to Transactions
      </Link>

      <Card title="Transaction Details">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <div className="text-xs text-slate-400">Transaction ID</div>
            <div className="font-semibold text-navy">{transaction.transaction_id}</div>
          </div>
          <div>
            <div className="text-xs text-slate-400">Sender</div>
            <div className="font-medium">{transaction.sender_address}</div>
          </div>
          <div>
            <div className="text-xs text-slate-400">Receiver</div>
            <div className="font-medium">{transaction.receiver_address}</div>
          </div>
          <div>
            <div className="text-xs text-slate-400">Amount</div>
            <div className="font-medium">
              {transaction.amount} {transaction.currency}
            </div>
          </div>
          <div>
            <div className="text-xs text-slate-400">Timestamp</div>
            <div className="font-medium">{new Date(transaction.timestamp).toLocaleString()}</div>
          </div>
          <div>
            <div className="text-xs text-slate-400">Authentication</div>
            <StatusBadge value={transaction.authentication_status} />
          </div>
          <div>
            <div className="text-xs text-slate-400">New Recipient</div>
            <div className="font-medium">{transaction.is_new_recipient ? "Yes" : "No"}</div>
          </div>
          <div>
            <div className="text-xs text-slate-400">Status</div>
            <StatusBadge value={transaction.status} kind="decision" />
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
        <Card title="Cyber Risk">
          <DimensionBar label="Score" score={risk.cyber_score} />
        </Card>
        <Card title="Behaviour Risk">
          <DimensionBar label="Score" score={risk.behaviour_score} />
          {behaviour?.triggers?.length > 0 && (
            <ul className="mt-2 text-xs text-slate-500 list-disc list-inside space-y-0.5">
              {behaviour.triggers.map((t: string) => (
                <li key={t}>{t}</li>
              ))}
            </ul>
          )}
        </Card>
        <Card title="Anomaly Risk">
          <DimensionBar label="Score" score={risk.anomaly_score} />
          <p className="text-xs text-slate-400 mt-2">{anomaly?.is_anomalous ? "Flagged as anomalous" : "Within normal range"}</p>
        </Card>
        <Card title="Crypto Risk">
          <DimensionBar label="Score" score={risk.crypto_score} />
          <p className="text-xs text-slate-400 mt-2">{crypto?.algorithm}</p>
        </Card>
        <Card title="Quantum Risk">
          <DimensionBar label="Score" score={risk.quantum_score} />
          <p className="text-xs text-slate-400 mt-2">Exposure: {crypto?.quantum_exposure}</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <div className={`rounded-lg bg-gradient-to-br ${RISK_LEVEL_BG[risk.risk_level]} text-white p-6`}>
            <p className="text-xs font-semibold uppercase tracking-wide opacity-80">Unified Quantum-Cyber Risk Score</p>
            <div className="text-5xl font-extrabold mt-2">{risk.unified_score.toFixed(1)}</div>
            <p className="text-sm opacity-90">/ 100</p>
            <div className="mt-3">
              <span className="inline-block bg-white/20 rounded-md px-3 py-1 text-sm font-bold">{risk.risk_level}</span>
            </div>
          </div>
          {risk.primary_contributors?.length > 0 && (
            <div className="mt-4">
              <p className="text-xs font-semibold text-slate-500 uppercase mb-2">Primary Contributors</p>
              <ul className="space-y-1">
                {risk.primary_contributors.map((c: string) => (
                  <li key={c} className="text-sm text-navy flex items-start gap-1.5">
                    <span className="text-critical font-bold">+</span> {c}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </Card>

        <Card title="Security Decision">
          <div className="flex items-center gap-4">
            <div className={`w-14 h-14 rounded-full flex items-center justify-center text-white ${DECISION_ICON_BG[decision.decision]}`}>
              <ShieldQuestion size={26} />
            </div>
            <div>
              <div className="text-2xl font-extrabold text-navy">{decision.decision}</div>
              <div className="text-xs text-slate-400">Confidence: {(decision.confidence * 100).toFixed(0)}%</div>
            </div>
          </div>
          <p className="text-sm text-slate-600 mt-4">{decision.reason}</p>
          <p className="text-xs text-slate-400 mt-2">Policy trigger: {decision.policy_trigger}</p>

          {decision.decision === "FLAG" && (
            <div className="mt-4 pt-4 border-t border-slate-100">
              <p className="text-xs font-semibold text-slate-500 uppercase mb-2">Analyst Review</p>
              {decision.analyst_override ? (
                <StatusBadge value={`Analyst: ${decision.analyst_override}`} />
              ) : (
                <div className="flex gap-2">
                  <button
                    disabled={reviewing}
                    onClick={() => handleReview("APPROVE")}
                    className="flex-1 text-xs font-semibold bg-emerald-600 text-white rounded-md py-2 hover:bg-emerald-700 disabled:opacity-50"
                  >
                    Approve
                  </button>
                  <button
                    disabled={reviewing}
                    onClick={() => handleReview("REJECT")}
                    className="flex-1 text-xs font-semibold bg-red-600 text-white rounded-md py-2 hover:bg-red-700 disabled:opacity-50"
                  >
                    Reject
                  </button>
                  <button
                    disabled={reviewing}
                    onClick={() => handleReview("KEEP_FLAGGED")}
                    className="flex-1 text-xs font-semibold bg-slate-200 text-navy rounded-md py-2 hover:bg-slate-300 disabled:opacity-50"
                  >
                    Keep Flagged
                  </button>
                </div>
              )}
            </div>
          )}
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Cryptographic Security Assessment">
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2 text-navy font-medium">
              <Lock size={15} className="text-accent" /> {crypto.algorithm}
            </div>
            <p className="text-slate-500 text-xs">Key Type: {crypto.key_type}</p>
            <p className="text-slate-500 text-xs">Signature: {crypto.signature_type}</p>
            <p className="text-slate-500 text-xs">Security Category: {crypto.security_category}</p>
            <div className="flex items-center gap-2 pt-1">
              <span className="text-xs text-slate-400">Quantum Exposure:</span>
              <StatusBadge value={crypto.quantum_exposure} />
            </div>
            <p className="text-xs text-slate-400">Migration Status: {crypto.migration_status}</p>
          </div>
        </Card>

        <Card title="Quantum Assessment">
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2 text-navy font-medium">
              <Cpu size={15} className="text-cyan" /> Local Qiskit Simulation - {quantum.simulation_status}
            </div>
            <p className="text-slate-500 text-xs">
              Qubits: {quantum.qubit_count} · Circuit Depth: {quantum.circuit_depth}
            </p>
            <p className="text-slate-500 text-xs">Migration Priority: {quantum.migration_priority}</p>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">{quantum.security_interpretation}</p>
          </div>
        </Card>
      </div>

      <Card title="Blockchain Audit Log">
        <div className="flex items-center gap-3">
          <Blocks size={18} className={blockchain?.status === "CONFIRMED" ? "text-emerald-600" : "text-slate-400"} />
          <div className="text-sm space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Status:</span>
              <StatusBadge value={blockchain?.status ?? "UNAVAILABLE"} />
              <span className="text-xs text-slate-400 ml-2">{blockchain?.network}</span>
            </div>
            {blockchain?.status === "CONFIRMED" ? (
              <>
                <p className="text-xs text-slate-500">Block #{blockchain.block_number}</p>
                <p className="text-xs text-slate-400 font-mono break-all">{blockchain.tx_hash}</p>
              </>
            ) : (
              <p className="text-xs text-slate-400">
                Blockchain confirmation unavailable. The security decision above remains fully recorded in the
                database - this system never fabricates a blockchain confirmation.
              </p>
            )}
          </div>
        </div>
      </Card>
    </div>
  );
}
