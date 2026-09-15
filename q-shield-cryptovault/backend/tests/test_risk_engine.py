from app.core.config import Settings
from app.engines.risk.engine import calculate_unified_risk


def _settings():
    return Settings(
        risk_weight_cyber=0.20,
        risk_weight_behaviour=0.20,
        risk_weight_anomaly=0.20,
        risk_weight_crypto=0.20,
        risk_weight_quantum=0.20,
        risk_threshold_low=24,
        risk_threshold_moderate=49,
        risk_threshold_high=74,
    )


def test_uniform_low_inputs_produce_low_risk():
    result = calculate_unified_risk(
        cyber_score=20,
        behaviour_score=20,
        anomaly_score=20,
        crypto_score=20,
        quantum_score=20,
        contributor_triggers=[],
        settings=_settings(),
    )
    assert result.unified_score == 20.0
    assert result.risk_level == "LOW"


def test_uniform_high_inputs_produce_critical_risk():
    result = calculate_unified_risk(
        cyber_score=80,
        behaviour_score=80,
        anomaly_score=80,
        crypto_score=80,
        quantum_score=80,
        contributor_triggers=["Unusual transaction amount"],
        settings=_settings(),
    )
    assert result.unified_score == 80.0
    assert result.risk_level == "CRITICAL"


def test_score_is_deterministic_for_same_inputs():
    kwargs = dict(
        cyber_score=45,
        behaviour_score=60,
        anomaly_score=30,
        crypto_score=72,
        quantum_score=78,
        contributor_triggers=["New destination wallet detected"],
        settings=_settings(),
    )
    result_a = calculate_unified_risk(**kwargs)
    result_b = calculate_unified_risk(**kwargs)
    assert result_a.unified_score == result_b.unified_score
    assert result_a.risk_level == result_b.risk_level


def test_boundary_thresholds():
    settings = _settings()
    for score, expected_level in [(24, "LOW"), (25, "MODERATE"), (49, "MODERATE"), (50, "HIGH"), (74, "HIGH"), (75, "CRITICAL")]:
        result = calculate_unified_risk(
            cyber_score=score,
            behaviour_score=score,
            anomaly_score=score,
            crypto_score=score,
            quantum_score=score,
            contributor_triggers=[],
            settings=settings,
        )
        assert result.risk_level == expected_level, f"score={score}"
