"""Security Decision Engine (Section 22-23 / Phase 11).

Deterministic policy mapping from risk_level to APPROVE / FLAG / REJECT.
Authentication failure is a fail-safe override that takes precedence over
the normal risk-based policy (Section 22, Section 53 fail-safe policy).
"""
from dataclasses import dataclass

_POLICY = {
    "LOW": "APPROVE",
    "MODERATE": "FLAG",
    "HIGH": "FLAG",
    "CRITICAL": "REJECT",
}

_REASONS = {
    "APPROVE": "No significant risk indicators detected across cyber, behavioural, anomaly, cryptographic, or quantum dimensions.",
    "FLAG": "One or more risk indicators require analyst review before this transaction proceeds.",
    "REJECT": "Multiple high-risk indicators detected. Transaction blocked under Q-Shield fail-safe policy.",
}


@dataclass
class DecisionResult:
    decision: str
    risk_level: str
    score: float
    reason: str
    policy_trigger: str
    confidence: float


def decide(
    *,
    unified_score: float,
    risk_level: str,
    authentication_status: str,
) -> DecisionResult:
    if authentication_status.upper() == "FAILED":
        return DecisionResult(
            decision="REJECT",
            risk_level=risk_level,
            score=unified_score,
            reason="Authentication failed. Transaction rejected under fail-safe authentication policy, "
            "independent of the computed risk score.",
            policy_trigger="AUTHENTICATION_FAILURE_OVERRIDE",
            confidence=1.0,
        )

    decision = _POLICY.get(risk_level, "FLAG")
    reason = _REASONS[decision]

    band_edges = {"LOW": (0, 24), "MODERATE": (25, 49), "HIGH": (50, 74), "CRITICAL": (75, 100)}
    lo, hi = band_edges.get(risk_level, (0, 100))
    span = max(hi - lo, 1)
    distance_from_edge = min(unified_score - lo, hi - unified_score)
    confidence = round(0.6 + 0.4 * min(distance_from_edge / (span / 2), 1.0), 2)

    return DecisionResult(
        decision=decision,
        risk_level=risk_level,
        score=unified_score,
        reason=reason,
        policy_trigger=f"RISK_LEVEL_{risk_level}",
        confidence=confidence,
    )
