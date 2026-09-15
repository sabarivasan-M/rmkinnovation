import { Route, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import TransactionDetail from "./pages/TransactionDetail";
import Quantum from "./pages/Quantum";
import Blockchain from "./pages/Blockchain";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/transactions" element={<Transactions />} />
        <Route path="/transactions/:transactionId" element={<TransactionDetail />} />
        <Route path="/quantum" element={<Quantum />} />
        <Route path="/blockchain" element={<Blockchain />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
