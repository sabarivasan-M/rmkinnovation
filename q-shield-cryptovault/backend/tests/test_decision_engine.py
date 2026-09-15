from app.engines.decision.engine import decide


def test_low_risk_approves():
    result = decide(unified_score=10, risk_level="LOW", authentication_status="SUCCESS")
    assert result.decision == "APPROVE"


def test_moderate_risk_flags():
    result = decide(unified_score=35, risk_level="MODERATE", authentication_status="SUCCESS")
    assert result.decision == "FLAG"


def test_high_risk_flags():
    result = decide(unified_score=60, risk_level="HIGH", authentication_status="SUCCESS")
    assert result.decision == "FLAG"


def test_critical_risk_rejects():
    result = decide(unified_score=90, risk_level="CRITICAL", authentication_status="SUCCESS")
    assert result.decision == "REJECT"


def test_authentication_failure_overrides_low_risk_score():
    result = decide(unified_score=5, risk_level="LOW", authentication_status="FAILED")
    assert result.decision == "REJECT"
    assert result.policy_trigger == "AUTHENTICATION_FAILURE_OVERRIDE"
