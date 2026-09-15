from pydantic import BaseModel


class SystemStatusOut(BaseModel):
    api: str
    database: str
    risk_engine: str
    quantum_simulator: str
    blockchain: str


class DashboardSummaryOut(BaseModel):
    transactions_analysed: int
    high_risk_count: int
    critical_count: int
    quantum_exposed_count: int
    system_status: SystemStatusOut
