import { Inbox } from "lucide-react";

export default function EmptyState({ title, hint }: { title: string; hint?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center text-slate-400">
      <Inbox size={32} className="mb-3 opacity-60" />
      <p className="text-sm font-medium text-slate-500">{title}</p>
      {hint && <p className="text-xs text-slate-400 mt-1 max-w-xs">{hint}</p>}
    </div>
  );
}
