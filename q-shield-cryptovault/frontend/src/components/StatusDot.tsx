export default function StatusDot({ status }: { status: string }) {
  const s = status.toUpperCase();
  const isOnline = s.includes("ONLINE");
  const color = isOnline ? "bg-emerald-500" : s.includes("LOCAL") ? "bg-cyan-500" : "bg-red-500";
  return (
    <span className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-600">
      <span className={`status-dot ${color}`} />
      {status}
    </span>
  );
}
