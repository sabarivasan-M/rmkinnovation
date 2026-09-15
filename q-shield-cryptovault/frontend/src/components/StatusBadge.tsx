interface Props {
  value: string;
  kind?: "risk" | "decision" | "generic";
}

const RISK_COLORS: Record<string, string> = {
  LOW: "bg-emerald-100 text-emerald-800 border-emerald-300",
  MODERATE: "bg-amber-100 text-amber-800 border-amber-300",
  HIGH: "bg-orange-100 text-orange-800 border-orange-300",
  CRITICAL: "bg-red-100 text-red-700 border-red-300",
};

const DECISION_COLORS: Record<string, string> = {
  APPROVE: "bg-emerald-100 text-emerald-800 border-emerald-300",
  FLAG: "bg-amber-100 text-amber-800 border-amber-300",
  REJECT: "bg-red-100 text-red-700 border-red-300",
};

export default function StatusBadge({ value, kind = "generic" }: Props) {
  const palette = kind === "risk" ? RISK_COLORS : kind === "decision" ? DECISION_COLORS : {};
  const classes = palette[value] ?? "bg-slate-100 text-slate-700 border-slate-300";
  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold border ${classes}`}>
      {value}
    </span>
  );
}
