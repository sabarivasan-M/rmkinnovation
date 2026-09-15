import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { CheckCircle2, Circle, Loader2, PlayCircle } from "lucide-react";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import StatusBadge from "../components/StatusBadge";
import { analyseTransaction, fetchScenarios, fetchTransactions, fetchWallets, runScenario } from "../services/api";
import type { ScenarioInfo, TransactionSummary, Wallet } from "../types";

const PIPELINE_STEPS = [
  "CAPTURE",
  "AUTHENTICATION",
  "BEHAVIOUR ANALYSIS",
  "ANOMALY DETECTION",
  "CRYPTO ASSESSMENT",
  "QUANTUM ASSESSMENT",
  "RISK QUANTIFICATION",
  "SECURITY DECISION",
  "BLOCKCHAIN LOG",
];

function PipelineProgress({ activeStep, done }: { activeStep: number; done: boolean }) {
  return (
    <div className="grid grid-cols-3 sm:grid-cols-5 gap-y-3 gap-x-2">
      {PIPELINE_STEPS.map((step, i) => {
        const isComplete = done || i < activeStep;
        const isActive = !done && i === activeStep;
        return (
          <div key={step} className="flex items-center gap-1.5 text-xs">
            {isComplete ? (
              <CheckCircle2 size={15} className="text-emerald-500 shrink-0" />
            ) : isActive ? (
              <Loader2 size={15} className="text-accent shrink-0 animate-spin" />
            ) : (
              <Circle size={15} className="text-slate-300 shrink-0" />
            )}
            <span className={isComplete ? "text-navy font-medium" : isActive ? "text-accent font-medium" : "text-slate-400"}>
              {step}
            </span>
          </div>
        );
      })}
    </div>
  );
}

export default function Transactions() {
  const navigate = useNavigate();
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [scenarios, setScenarios] = useState<ScenarioInfo[]>([]);
  const [transactions, setTransactions] = useState<TransactionSummary[]>([]);

  const [sender, setSender] = useState("WALLET-ALPHA");
  const [receiver, setReceiver] = useState("WALLET-BETA");
  const [amount, setAmount] = useState("0.85");
  const [currency, setCurrency] = useState("ETH");
  const [authStatus, setAuthStatus] = useState<"SUCCESS" | "FAILED">("SUCCESS");

  const [processing, setProcessing] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const reload = () => fetchTransactions(20).then(setTransactions).catch(() => {});

  useEffect(() => {
    fetchWallets().then(setWallets).catch(() => {});
    fetchScenarios().then(setScenarios).catch(() => {});
    reload();
  }, []);

  async function runPipeline(action: () => Promise<{ transaction_id: string }>) {
    setError(null);
    setProcessing(true);
    setActiveStep(0);
    const stepTimer = setInterval(() => {
      setActiveStep((s) => Math.min(s + 1, PIPELINE_STEPS.length - 1));
    }, 160);
    try {
      const result = await action();
      clearInterval(stepTimer);
      setActiveStep(PIPELINE_STEPS.length);
      await reload();
      setTimeout(() => {
        setProcessing(false);
        navigate(`/transactions/${result.transaction_id}`);
      }, 400);
    } catch (err: any) {
      clearInterval(stepTimer);
      setProcessing(false);
      setError(err?.response?.data?.detail ?? "Security analysis unavailable. Backend connection could not be established.");
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const parsedAmount = Number(amount);
    if (!Number.isFinite(parsedAmount) || parsedAmount <= 0) {
      setError("Amount must be greater than 0.");
      return;
    }
    runPipeline(() =>
      analyseTransaction({
        sender_address: sender,
        receiver_address: receiver,
        amount: parsedAmount,
        currency,
        authentication_status: authStatus,
      })
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-navy">Transaction Security Analysis</h1>
        <p className="text-sm text-slate-500 mt-0.5">
          Submit a transaction through the full CAPTURE → ANALYSE → QUANTIFY → DECIDE → LOG pipeline.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="New Transaction" className="lg:col-span-1">
          <form onSubmit={handleSubmit} className="space-y-3.5">
            <div>
              <label className="text-xs font-medium text-slate-500">Sender Wallet</label>
              <select
                value={sender}
                onChange={(e) => setSender(e.target.value)}
                className="mt-1 w-full border border-slate-200 rounded-md px-3 py-2 text-sm"
              >
                {wallets.map((w) => (
                  <option key={w.address} value={w.address}>
                    {w.address} - {w.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs font-medium text-slate-500">Receiver Wallet</label>
              <input
                value={receiver}
                onChange={(e) => setReceiver(e.target.value)}
                className="mt-1 w-full border border-slate-200 rounded-md px-3 py-2 text-sm"
                placeholder="WALLET-BETA or new address"
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-medium text-slate-500">Amount</label>
                <input
                  type="number"
                  step="0.0001"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="mt-1 w-full border border-slate-200 rounded-md px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="text-xs font-medium text-slate-500">Currency</label>
                <select
                  value={currency}
                  onChange={(e) => setCurrency(e.target.value)}
                  className="mt-1 w-full border border-slate-200 rounded-md px-3 py-2 text-sm"
                >
                  <option>ETH</option>
                  <option>BTC</option>
                  <option>USDT</option>
                </select>
              </div>
            </div>
            <div>
              <label className="text-xs font-medium text-slate-500">Authentication</label>
              <select
                value={authStatus}
                onChange={(e) => setAuthStatus(e.target.value as "SUCCESS" | "FAILED")}
                className="mt-1 w-full border border-slate-200 rounded-md px-3 py-2 text-sm"
              >
                <option value="SUCCESS">SUCCESS</option>
                <option value="FAILED">FAILED</option>
              </select>
            </div>
            {error && <p className="text-xs text-critical">{error}</p>}
            <button
              type="submit"
              disabled={processing}
              className="w-full bg-accent text-white text-sm font-semibold py-2.5 rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {processing ? "Analysing..." : "ANALYSE TRANSACTION"}
            </button>
          </form>

          <div className="mt-5 pt-5 border-t border-slate-100">
            <p className="text-xs font-semibold text-slate-500 uppercase mb-2">Demo Scenarios (Seeded Demonstration Data)</p>
            <div className="space-y-2">
              {scenarios.map((s) => (
                <button
                  key={s.key}
                  disabled={processing}
                  onClick={() => runPipeline(() => runScenario(s.key))}
                  className="w-full flex items-center gap-2 text-left text-xs px-3 py-2 rounded-md border border-slate-200 hover:border-accent hover:bg-blue-50 transition-colors disabled:opacity-50"
                >
                  <PlayCircle size={14} className="text-accent shrink-0" />
                  <span>
                    <span className="font-semibold text-navy">{s.label}</span>
                    <br />
                    <span className="text-slate-400">{s.expected}</span>
                  </span>
                </button>
              ))}
            </div>
          </div>
        </Card>

        <div className="lg:col-span-2 space-y-6">
          {processing && (
            <Card title="Security Pipeline">
              <PipelineProgress activeStep={activeStep} done={activeStep >= PIPELINE_STEPS.length} />
            </Card>
          )}

          <Card title="Recent Transactions">
            {transactions.length === 0 ? (
              <EmptyState title="No transactions yet." hint="Submit a transaction or run a demo scenario to get started." />
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-xs uppercase text-slate-400 border-b border-slate-100">
                      <th className="pb-2 font-medium">TX ID</th>
                      <th className="pb-2 font-medium">Sender → Receiver</th>
                      <th className="pb-2 font-medium">Amount</th>
                      <th className="pb-2 font-medium">Risk</th>
                      <th className="pb-2 font-medium">Decision</th>
                      <th className="pb-2 font-medium">Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.map((tx) => (
                      <tr key={tx.transaction_id} className="border-b border-slate-50 last:border-0 hover:bg-slate-50">
                        <td className="py-2.5">
                          <Link to={`/transactions/${tx.transaction_id}`} className="text-accent font-medium hover:underline">
                            {tx.transaction_id}
                          </Link>
                        </td>
                        <td className="py-2.5 text-slate-500 text-xs">
                          {tx.sender_address} → {tx.receiver_address}
                        </td>
                        <td className="py-2.5 text-slate-600">
                          {tx.amount} {tx.currency}
                        </td>
                        <td className="py-2.5">{tx.risk_level && <StatusBadge value={tx.risk_level} kind="risk" />}</td>
                        <td className="py-2.5">{tx.decision && <StatusBadge value={tx.decision} kind="decision" />}</td>
                        <td className="py-2.5 text-slate-400 text-xs">{new Date(tx.timestamp).toLocaleTimeString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
