"""Central configuration. Risk weights and thresholds live here, not scattered in code."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./qshield.db"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Unified Quantum-Cyber Risk Score weights (Section 19). Must sum to 1.0.
    risk_weight_cyber: float = 0.20
    risk_weight_behaviour: float = 0.20
    risk_weight_anomaly: float = 0.20
    risk_weight_crypto: float = 0.20
    risk_weight_quantum: float = 0.20

    # Q-Shield prototype policy thresholds (Section 20) - NOT an industry standard.
    risk_threshold_low: int = 24
    risk_threshold_moderate: int = 49
    risk_threshold_high: int = 74
    # 75-100 = CRITICAL

    blockchain_rpc_url: str = "http://127.0.0.1:8545"
    blockchain_contract_address: str = ""
    blockchain_enabled: bool = True

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
