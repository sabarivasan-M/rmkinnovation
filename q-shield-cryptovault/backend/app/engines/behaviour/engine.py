"""Wallet behaviour analysis (Section 14 / Phase 5).

Compares an incoming transaction against the sender wallet's seeded behavioural
baseline and produces a deterministic behaviour_score (0-100) with an explicit
list of triggered features.
"""
from dataclasses import dataclass, field


@dataclass
class BehaviourResult:
    behaviour_score: float
    amount_deviation: float
    velocity_score: float
    new_recipient_penalty: float
    time_of_day_penalty: float
    auth_failure_penalty: float
    triggers: list[str] = field(default_factory=list)


def _clip(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def analyse_behaviour(
    *,
    amount: float,
    hour_of_day: int,
    is_new_recipient: bool,
    wallet_avg_amount: float,
    wallet_usual_tx_per_day: float,
    recent_tx_count_today: int,
    wallet_failed_auth_count: int,
) -> BehaviourResult:
    triggers: list[str] = []

    baseline_amount = max(wallet_avg_amount, 0.01)
    deviation_ratio = abs(amount - baseline_amount) / baseline_amount
    amount_deviation = _clip(deviation_ratio * 35.0)
    if deviation_ratio > 1.5:
        triggers.append("Unusual transaction amount")

    baseline_velocity = max(wallet_usual_tx_per_day, 1.0)
    velocity_ratio = recent_tx_count_today / baseline_velocity
    velocity_score = _clip((velocity_ratio - 1.0) * 60.0) if velocity_ratio > 1.0 else 0.0
    if velocity_ratio > 2.0:
        triggers.append("Abnormal transaction velocity")

    new_recipient_penalty = 55.0 if is_new_recipient else 0.0
    if is_new_recipient:
        triggers.append("New destination wallet detected")

    is_odd_hour = hour_of_day < 5 or hour_of_day >= 23
    time_of_day_penalty = 40.0 if is_odd_hour else 0.0
    if is_odd_hour:
        triggers.append("Transaction at unusual hour")

    auth_failure_penalty = _clip(wallet_failed_auth_count * 25.0)
    if wallet_failed_auth_count > 0:
        triggers.append("Repeated authentication failure history")

    behaviour_score = _clip(
        0.35 * amount_deviation
        + 0.25 * velocity_score
        + 0.20 * new_recipient_penalty
        + 0.10 * time_of_day_penalty
        + 0.10 * auth_failure_penalty
    )

    return BehaviourResult(
        behaviour_score=round(behaviour_score, 2),
        amount_deviation=round(amount_deviation, 2),
        velocity_score=round(velocity_score, 2),
        new_recipient_penalty=round(new_recipient_penalty, 2),
        time_of_day_penalty=round(time_of_day_penalty, 2),
        auth_failure_penalty=round(auth_failure_penalty, 2),
        triggers=triggers,
    )
