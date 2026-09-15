from app.engines.anomaly.engine import detect_anomaly


def test_typical_transaction_not_anomalous():
    result = detect_anomaly(
        amount=1.0, hour_of_day=14, is_new_recipient=False, velocity_ratio=1.0, failed_auth_count=0
    )
    assert result.anomaly_score < 60


def test_extreme_outlier_flagged_anomalous():
    result = detect_anomaly(
        amount=50.0, hour_of_day=3, is_new_recipient=True, velocity_ratio=6.0, failed_auth_count=3
    )
    assert result.is_anomalous is True
    assert result.anomaly_score > 50
    assert "New destination wallet detected" in result.triggers


def test_explanation_only_lists_features_that_actually_triggered():
    result = detect_anomaly(
        amount=1.0, hour_of_day=14, is_new_recipient=False, velocity_ratio=1.0, failed_auth_count=0
    )
    assert result.triggers == []
