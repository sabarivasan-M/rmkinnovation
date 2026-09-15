import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Blocks, Layers } from "lucide-react";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import StatusBadge from "../components/StatusBadge";
import { fetchAuditLogs, fetchDashboardSummary } from "../services/api";
import type { AuditLogEntry } from "../types";

export default function Blockchain() {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [blockchainStatus, setBlockchainStatus] = useState<string>("UNAVAILABLE");

  useEffect(() => {
    fetchAuditLogs(100).then(setLogs).catch(() => {});
    fetchDashboardSummary()
      .then((s) => setBlockchainStatus(s.system_status.blockchain))
      .catch(() => {});
  }, []);

  const confirmed = logs.filter((l) => l.blockchain_status === "CONFIRMED");
  const latestBlock = confirmed.reduce((max, l) => Math.max(max, l.block_number), 0);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-navy">Blockchain Security Log</h1>
        <p className="text-sm text-slate-500 mt-0.5">
          Tamper-resistant audit trail of every security decision, written to a LOCAL Hardhat Ethereum-compatible
          network.
        </p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <div className="text-xs text-slate-400 uppercase">Network</div>
          <div className="font-bold text-navy mt-1">LOCAL HARDHAT</div>
        </Card>
        <Card>
          <div className="text-xs text-slate-400 uppercase">Contract</div>
          <div className="font-bold text-navy mt-1 text-sm">QShieldSecurityLog</div>
        </Card>
        <Card>
          <div className="text-xs text-slate-400 uppercase">Latest Block</div>
          <div className="font-bold text-navy mt-1">#{latestBlock}</div>
        </Card>
        <Card>
          <div className="text-xs text-slate-400 uppercase">Blockchain Status</div>
          <div className="mt-1">
            <StatusBadge value={blockchainStatus} />
          </div>
        </Card>
      </div>

      <Card title="Audit Records">
        {logs.length === 0 ? (
          <EmptyState
            title="No audit records yet."
            hint="Analyse a transaction to write its security decision to the blockchain audit log."
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase text-slate-400 border-b border-slate-100">
                  <th className="pb-2 font-medium">TX ID</th>
                  <th className="pb-2 font-medium">Decision</th>
                  <th className="pb-2 font-medium">Risk Score</th>
                  <th className="pb-2 font-medium">Block</th>
                  <th className="pb-2 font-medium">Hash</th>
                  <th className="pb-2 font-medium">Status</th>
                  <th className="pb-2 font-medium">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.transaction_id} className="border-b border-slate-50 last:border-0 hover:bg-slate-50">
                    <td className="py-2.5">
                      <Link to={`/transactions/${log.transaction_id}`} className="text-accent font-medium hover:underline">
                        {log.transaction_id}
                      </Link>
                    </td>
                    <td className="py-2.5">
                      <StatusBadge value={log.decision} kind="decision" />
                    </td>
                    <td className="py-2.5 text-slate-600">{log.risk_score.toFixed(1)}</td>
                    <td className="py-2.5 text-slate-500">
                      {log.blockchain_status === "CONFIRMED" ? (
                        <span className="flex items-center gap-1">
                          <Layers size={13} /> #{log.block_number}
                        </span>
                      ) : (
                        "-"
                      )}
                    </td>
                    <td className="py-2.5 text-slate-400 text-xs font-mono">
                      {log.blockchain_reference ? `${log.blockchain_reference.slice(0, 10)}...` : "-"}
                    </td>
                    <td className="py-2.5">
                      <StatusBadge value={log.blockchain_status} />
                    </td>
                    <td className="py-2.5 text-slate-400 text-xs">{new Date(log.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <div className="flex items-start gap-2 text-xs text-slate-400 bg-slate-50 border border-slate-200 rounded-md p-3">
        <Blocks size={14} className="shrink-0 mt-0.5" />
        <span>
          This is a LOCAL blockchain demonstration environment (Hardhat), not Ethereum mainnet. If the blockchain is
          unavailable, security decisions remain fully recorded in the database - the system never fabricates a
          confirmation.
        </span>
      </div>
    </div>
  );
}
