import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Atom, Cpu, ShieldCheck } from "lucide-react";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import StatusBadge from "../components/StatusBadge";
import { fetchQuantumAssessments, fetchQuantumStatus } from "../services/api";

export default function Quantum() {
  const [status, setStatus] = useState<any>(null);
  const [assessments, setAssessments] = useState<any[]>([]);

  useEffect(() => {
    fetchQuantumStatus().then(setStatus).catch(() => {});
    fetchQuantumAssessments(20).then(setAssessments).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-navy">Quantum Security Center</h1>
        <p className="text-sm text-slate-500 mt-0.5">
          Local Qiskit simulation demonstrating quantum-computing concepts relevant to cryptographic threat
          assessment - SIMULATED, not a real quantum attack.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Quantum Simulation Engine">
          {status ? (
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm font-medium text-navy">
                <Cpu size={16} className="text-cyan" /> {status.engine}
              </div>
              <div className="flex items-center gap-2">
                <StatusBadge value={status.mode} />
                <StatusBadge value={status.status} />
              </div>
              <div className="grid grid-cols-2 gap-3 pt-2 text-sm">
                <div>
                  <div className="text-xs text-slate-400">Qubits</div>
                  <div className="font-semibold text-navy">{status.qubits}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400">Circuit Depth</div>
                  <div className="font-semibold text-navy">{status.circuit_depth}</div>
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed pt-2 border-t border-slate-100 mt-2">
                {status.interpretation}
              </p>
            </div>
          ) : (
            <EmptyState title="Quantum simulator status unavailable." />
          )}
        </Card>

        <Card title="Post-Quantum Readiness Roadmap">
          <div className="flex flex-col gap-3 text-sm">
            {[
              { label: "CURRENT", detail: "Classical Public-Key Cryptography (ECDSA / RSA)" },
              { label: "ASSESS", detail: "Quantum Exposure evaluated per wallet profile" },
              { label: "PRIORITISE", detail: "Migration Priority: LOW / MEDIUM / HIGH / CRITICAL" },
              { label: "PREPARE", detail: "PQC Candidates: ML-KEM · ML-DSA · SLH-DSA" },
            ].map((step, i, arr) => (
              <div key={step.label} className="flex items-start gap-3">
                <div className="flex flex-col items-center">
                  <div className="w-7 h-7 rounded-full bg-navy text-white flex items-center justify-center text-xs font-bold">
                    {i + 1}
                  </div>
                  {i < arr.length - 1 && <div className="w-px h-8 bg-slate-200" />}
                </div>
                <div>
                  <div className="font-semibold text-navy text-xs tracking-wide">{step.label}</div>
                  <div className="text-slate-500 text-xs">{step.detail}</div>
                </div>
              </div>
            ))}
          </div>
          <p className="text-xs text-slate-400 mt-4 pt-3 border-t border-slate-100">
            This is an ASSESSMENT and migration-readiness demonstration - not a claim that any blockchain network
            has been automatically migrated to post-quantum cryptography.
          </p>
        </Card>
      </div>

      <Card title="Quantum Exposure by Analysed Transaction">
        {assessments.length === 0 ? (
          <EmptyState title="No quantum assessments yet." hint="Analyse a transaction to see its quantum exposure profile here." />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase text-slate-400 border-b border-slate-100">
                  <th className="pb-2 font-medium">TX ID</th>
                  <th className="pb-2 font-medium">Quantum Score</th>
                  <th className="pb-2 font-medium">Migration Priority</th>
                  <th className="pb-2 font-medium">Qubits</th>
                  <th className="pb-2 font-medium">Circuit Depth</th>
                </tr>
              </thead>
              <tbody>
                {assessments.map((a) => (
                  <tr key={a.transaction_id} className="border-b border-slate-50 last:border-0 hover:bg-slate-50">
                    <td className="py-2.5">
                      <Link to={`/transactions/${a.transaction_id}`} className="text-accent font-medium hover:underline">
                        {a.transaction_id}
                      </Link>
                    </td>
                    <td className="py-2.5">{a.quantum_score}</td>
                    <td className="py-2.5">
                      <StatusBadge value={a.migration_priority} kind="risk" />
                    </td>
                    <td className="py-2.5 text-slate-500">{a.qubit_count}</td>
                    <td className="py-2.5 text-slate-500">{a.circuit_depth}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <div className="flex items-start gap-2 text-xs text-slate-400 bg-slate-50 border border-slate-200 rounded-md p-3">
        <ShieldCheck size={14} className="shrink-0 mt-0.5" />
        <span>
          <Atom size={11} className="inline mb-0.5" /> This quantum module runs a LOCAL simulation only. It does not
          use real quantum hardware and does not represent a real-world attack against Bitcoin, Ethereum, or any
          live cryptographic system.
        </span>
      </div>
    </div>
  );
}
