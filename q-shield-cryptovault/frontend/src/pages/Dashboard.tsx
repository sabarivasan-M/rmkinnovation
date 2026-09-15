import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AlertTriangle, Atom, ShieldAlert, ShieldCheck, TrendingUp } from "lucide-react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import StatusBadge from "../components/StatusBadge";
import StatusDot from "../components/StatusDot";
import {
  fetchAlerts,
  fetchDashboardSummary,
  fetchRiskActivity,
  fetchRiskDistribution,
  fetchTransactions,
} from "../services/api";
import type { DashboardSummary, RiskActivityPoint, SecurityAlert, TransactionSummary } from "../types";

const RISK_PIE_COLORS: Record<string, string> = {
  LOW: "#10b981",
  MODERATE: "#d97706",
  HIGH: "#f97316",
  CRITICAL: "#dc2626",
};

function MetricCard({
  label,
  value,
  icon: Icon,
  tone,
}: {
  label: string;
  value: number;
  icon: typeof ShieldCheck;
  tone: string;
}) {
  return (
    <Card className="flex-1">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-3xl font-extrabold text-navy leading-none">{value}</div>
          <div className="text-xs font-medium text-slate-500 mt-2 uppercase tracking-wide">{label}</div>
        </div>
        <div className={`p-2.5 rounded-lg ${tone}`}>
          <Icon size={20} />
        </div>
      </div>
    </Card>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [activity, setActivity] = useState<RiskActivityPoint[]>([]);
  const [distribution, setDistribution] = useState<Record<string, number>>({});
  const [alerts, setAlerts] = useState<SecurityAlert[]>([]);
  const [transactions, setTransactions] = useState<TransactionSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      try {
        const [s, a, d, al, tx] = await Promise.all([
          fetchDashboardSummary(),
          fetchRiskActivity(),
          fetchRiskDistribution(),
          fetchAlerts(),
          fetchTransactions(8),
        ]);
        if (!mounted) return;
        setSummary(s);
        setActivity(a);
        setDistribution(d);
        setAlerts(al);
        setTransactions(tx);
      } catch {
        // handled by system status indicator in header
      } finally {
        if (mounted) setLoading(false);
      }
    };
    load();
    const id = setInterval(load, 8000);
    return () => {
      mounted = false;
      clearInterval(id);
    };
  }, []);

  const pieData = Object.entries(distribution)
    .filter(([, count]) => count > 0)
    .map(([level, count]) => ({ name: level, value: count }));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-navy">Security Overview</h1>
        <p className="text-sm text-slate-500 mt-0.5">
          Unified Quantum-Cyber Risk monitoring across every analysed transaction.
        </p>
      </div>

      <div className="flex flex-wrap gap-4">
        <MetricCard
          label="Transactions Analysed"
          value={summary?.transactions_analysed ?? 0}
          icon={TrendingUp}
          tone="bg-blue-50 text-accent"
        />
        <MetricCard
          label="High Risk"
          value={summary?.high_risk_count ?? 0}
          icon={ShieldAlert}
          tone="bg-orange-50 text-orange-600"
        />
        <MetricCard
          label="Critical Alerts"
          value={summary?.critical_count ?? 0}
          icon={AlertTriangle}
          tone="bg-red-50 text-critical"
        />
        <MetricCard
          label="Quantum-Exposed Profiles"
          value={summary?.quantum_exposed_count ?? 0}
          icon={Atom}
          tone="bg-cyan-50 text-cyan"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="Risk Activity Over Time" className="lg:col-span-2">
          {activity.length === 0 ? (
            <EmptyState
              title="No security events yet."
              hint="Run a transaction analysis to populate the security dashboard."
            />
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={activity.map((p, i) => ({ ...p, index: i + 1 }))}>
                <defs>
                  <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563EB" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                <XAxis dataKey="index" tick={{ fontSize: 11, fill: "#64748b" }} axisLine={false} tickLine={false} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: "#64748b" }} axisLine={false} tickLine={false} />
                <Tooltip
                  formatter={(value: number, _n, entry) => [`${value}`, `Unified Score (${entry.payload.risk_level})`]}
                  contentStyle={{ fontSize: 12, borderRadius: 8, border: "1px solid #e2e8f0" }}
                />
                <Area type="monotone" dataKey="unified_score" stroke="#2563EB" fill="url(#riskGradient)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </Card>

        <Card title="Risk Distribution">
          {pieData.length === 0 ? (
            <EmptyState title="No data yet." />
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={55} outerRadius={85} paddingAngle={3}>
                  {pieData.map((entry) => (
                    <Cell key={entry.name} fill={RISK_PIE_COLORS[entry.name] ?? "#94a3b8"} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8, border: "1px solid #e2e8f0" }} />
              </PieChart>
            </ResponsiveContainer>
          )}
          <div className="flex flex-wrap gap-3 mt-2 justify-center">
            {Object.entries(distribution).map(([level, count]) => (
              <div key={level} className="flex items-center gap-1.5 text-xs text-slate-600">
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: RISK_PIE_COLORS[level] }} />
                {level}: {count}
              </div>
            ))}
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="Security Alerts" className="lg:col-span-1">
          {alerts.length === 0 ? (
            <EmptyState title="No active alerts." hint="Alerts appear when a transaction is flagged HIGH or CRITICAL." />
          ) : (
            <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
              {alerts.map((alert, i) => (
                <div key={i} className="flex items-start gap-2.5 pb-3 border-b border-slate-100 last:border-0 last:pb-0">
                  <StatusBadge value={alert.severity} kind="risk" />
                  <div className="min-w-0">
                    <p className="text-sm text-navy leading-snug">{alert.message}</p>
                    <Link to={`/transactions/${alert.transaction_id}`} className="text-xs text-accent hover:underline">
                      {alert.transaction_id}
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card title="Recent Transactions" className="lg:col-span-2">
          {transactions.length === 0 ? (
            <EmptyState title="No transactions yet." hint="Create or run a demo transaction to see it here." />
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-xs uppercase text-slate-400 border-b border-slate-100">
                    <th className="pb-2 font-medium">TX ID</th>
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

      {summary && (
        <Card title="System Status">
          <div className="flex flex-wrap gap-x-8 gap-y-2">
            <StatusDot status={`API ${summary.system_status.api}`} />
            <StatusDot status={`DATABASE ${summary.system_status.database}`} />
            <StatusDot status={`RISK ENGINE ${summary.system_status.risk_engine}`} />
            <StatusDot status={`QUANTUM SIMULATOR ${summary.system_status.quantum_simulator}`} />
            <StatusDot status={`BLOCKCHAIN ${summary.system_status.blockchain}`} />
          </div>
        </Card>
      )}
      {loading && !summary && <p className="text-sm text-slate-400">Loading security dashboard...</p>}
    </div>
  );
}
