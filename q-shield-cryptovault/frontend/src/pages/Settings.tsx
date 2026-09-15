import { useEffect, useState } from "react";
import Card from "../components/Card";
import { fetchRiskPolicy } from "../services/api";

export default function Settings() {
  const [policy, setPolicy] = useState<any>(null);

  useEffect(() => {
    fetchRiskPolicy().then(setPolicy).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-navy">Settings</h1>
        <p className="text-sm text-slate-500 mt-0.5">Q-Shield prototype risk policy configuration (read-only).</p>
      </div>

      <Card title="Unified Risk Score Weights">
        {policy ? (
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
            {Object.entries(policy.weights).map(([dim, weight]: [string, any]) => (
              <div key={dim} className="text-center border border-slate-100 rounded-md py-3">
                <div className="text-xl font-bold text-navy">{(weight * 100).toFixed(0)}%</div>
                <div className="text-xs text-slate-400 capitalize mt-1">{dim}</div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-400">Loading policy...</p>
        )}
      </Card>

      <Card title="Risk Level Thresholds">
        {policy && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {Object.entries(policy.thresholds).map(([level, range]: [string, any]) => (
              <div key={level} className="text-center border border-slate-100 rounded-md py-3">
                <div className="text-sm font-bold text-navy">{level}</div>
                <div className="text-xs text-slate-400 mt-1">
                  {range[0]} - {range[1]}
                </div>
              </div>
            ))}
          </div>
        )}
        {policy && <p className="text-xs text-slate-400 mt-4 pt-3 border-t border-slate-100">{policy.disclaimer}</p>}
      </Card>

      <Card title="About This Prototype">
        <ul className="text-sm text-slate-600 space-y-2 list-disc list-inside">
          <li>Quantum component uses a local Qiskit simulation - not real quantum hardware.</li>
          <li>PQC layer evaluates cryptographic migration readiness, not automatic migration.</li>
          <li>Blockchain audit logging runs on a local Hardhat Ethereum-compatible network.</li>
          <li>Demo wallets and scenarios use seeded demonstration data.</li>
          <li>Risk thresholds above are Q-Shield prototype policy, not an industry standard.</li>
        </ul>
      </Card>
    </div>
  );
}
