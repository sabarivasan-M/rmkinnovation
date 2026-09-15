import { NavLink, Outlet } from "react-router-dom";
import { Activity, Atom, Blocks, LayoutDashboard, Settings as SettingsIcon, Shield, ArrowLeftRight } from "lucide-react";
import { useEffect, useState } from "react";
import { fetchHealth } from "../services/api";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/transactions", label: "Transactions", icon: ArrowLeftRight, end: false },
  { to: "/quantum", label: "Quantum Security", icon: Atom, end: false },
  { to: "/blockchain", label: "Blockchain Audit", icon: Blocks, end: false },
  { to: "/settings", label: "Settings", icon: SettingsIcon, end: false },
];

export default function AppLayout() {
  const [backendUp, setBackendUp] = useState<boolean | null>(null);

  useEffect(() => {
    let mounted = true;
    const check = () => {
      fetchHealth()
        .then(() => mounted && setBackendUp(true))
        .catch(() => mounted && setBackendUp(false));
    };
    check();
    const id = setInterval(check, 15000);
    return () => {
      mounted = false;
      clearInterval(id);
    };
  }, []);

  return (
    <div className="min-h-screen flex bg-offwhite text-navy">
      <aside className="w-60 shrink-0 bg-navy text-white flex flex-col">
        <div className="flex items-center gap-2 px-5 py-5 border-b border-white/10">
          <Shield size={22} className="text-accent" />
          <div>
            <div className="font-bold tracking-wide leading-none">Q-SHIELD</div>
            <div className="text-[10px] text-white/50 leading-none mt-1">CRYPTOVAULT</div>
          </div>
        </div>
        <nav className="flex-1 py-4 px-2 space-y-1">
          {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                  isActive ? "bg-accent text-white" : "text-white/70 hover:bg-white/10 hover:text-white"
                }`
              }
            >
              <Icon size={17} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="px-4 py-4 border-t border-white/10 text-[11px] text-white/40">
          Post-Quantum Security Infrastructure
          <br />
          DEMO ENVIRONMENT
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-14 shrink-0 bg-white border-b border-slate-200 flex items-center justify-between px-6">
          <div className="text-sm font-semibold text-navy">Security Control Center</div>
          <div className="flex items-center gap-2 text-xs font-medium">
            <span
              className={`status-dot ${
                backendUp === null ? "bg-slate-300" : backendUp ? "bg-emerald-500" : "bg-red-500"
              }`}
            />
            <span className="text-slate-600">
              {backendUp === null ? "Checking system status..." : backendUp ? "System Operational" : "Backend Unreachable"}
            </span>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
