"""Anomaly detection (Section 15 / Phase 6).

Uses a scikit-learn IsolationForest trained once, deterministically, on a
seeded synthetic baseline of "normal" wallet behaviour. The same trained
model + same input always yields the same output (fixed random_state and
fixed training data), satisfying the determinism requirement.
"""
from dataclasses import dataclass, field

import numpy as np
from sklearn.ensemble import IsolationForest

_RANDOM_STATE = 42
_FEATURE_NAMES = ["amount", "hour_of_day", "is_new_recipient", "velocity_ratio", "failed_auth_count"]


def _build_baseline() -> np.ndarray:
    rng = np.random.RandomState(_RANDOM_STATE)
    n = 300
    amount = rng.normal(loc=1.0, scale=0.4, size=n).clip(0.01, None)
    hour = rng.randint(7, 22, size=n)
    new_recipient = rng.binomial(1, 0.12, size=n)
    velocity_ratio = rng.normal(loc=1.0, scale=0.5, size=n).clip(0.05, None)
    failed_auth = rng.binomial(1, 0.03, size=n)
    return np.column_stack([amount, hour, new_recipient, velocity_ratio, failed_auth])


_BASELINE_DATA = _build_baseline()
_MODEL = IsolationForest(n_estimators=150, random_state=_RANDOM_STATE, contamination=0.1)
_MODEL.fit(_BASELINE_DATA)

# Calibrate the raw decision_function output against the training distribution itself,
# so a typical baseline transaction maps to a low score and only genuine outliers map high.
_BASELINE_SCORES = _MODEL.decision_function(_BASELINE_DATA)
_SCORE_HIGH = float(np.percentile(_BASELINE_SCORES, 95))  # typical inlier -> maps near 0
_SCORE_LOW = float(np.percentile(_BASELINE_SCORES, 1))  # extreme outlier -> maps near 100


@dataclass
class AnomalyResult:
    anomaly_score: float
    is_anomalous: bool
    triggers: list[str] = field(default_factory=list)


def detect_anomaly(
    *,
    amount: float,
    hour_of_day: int,
    is_new_recipient: bool,
    velocity_ratio: float,
    failed_auth_count: int,
) -> AnomalyResult:
    features = np.array([[amount, hour_of_day, int(is_new_recipient), velocity_ratio, failed_auth_count]])

    raw_score = _MODEL.decision_function(features)[0]
    is_outlier = _MODEL.predict(features)[0] == -1

    score_range = max(_SCORE_HIGH - _SCORE_LOW, 1e-6)
    anomaly_score = float(np.clip((_SCORE_HIGH - raw_score) / score_range * 100.0, 0, 100))

    triggers: list[str] = []
    if amount > 2.5:
        triggers.append("Unusual transaction amount")
    if is_new_recipient:
        triggers.append("New destination wallet detected")
    if velocity_ratio > 2.0:
        triggers.append("Abnormal transaction velocity")
    if failed_auth_count > 0:
        triggers.append("Repeated authentication failure history")
    if hour_of_day < 5 or hour_of_day >= 23:
        triggers.append("Transaction at unusual hour")

    return AnomalyResult(
        anomaly_score=round(anomaly_score, 2),
        is_anomalous=bool(is_outlier),
        triggers=triggers,
    )
