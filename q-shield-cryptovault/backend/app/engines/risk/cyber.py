"""Cyber Risk dimension: authentication & wallet-security posture.

Distinct from behaviour (transaction pattern) and anomaly (ML outlier
detection) - this dimension scores the identity/authentication trust of the
transaction itself.
"""


def _clip(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def compute_cyber_score(*, authentication_status: str, wallet_age_days: int, wallet_failed_auth_count: int) -> float:
    score = 0.0
    if authentication_status.upper() == "FAILED":
        score += 40.0

    if wallet_age_days < 3:
        score += 30.0
    elif wallet_age_days < 14:
        score += 15.0

    score += min(wallet_failed_auth_count * 20.0, 60.0)

    return round(_clip(score), 2)
