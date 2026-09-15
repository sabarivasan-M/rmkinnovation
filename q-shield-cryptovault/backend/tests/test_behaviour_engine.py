from app.engines.behaviour.engine import analyse_behaviour


def test_normal_transaction_scores_low():
    result = analyse_behaviour(
        amount=0.85,
        hour_of_day=14,
        is_new_recipient=False,
        wallet_avg_amount=0.8,
        wallet_usual_tx_per_day=3.0,
        recent_tx_count_today=1,
        wallet_failed_auth_count=0,
    )
    assert result.behaviour_score < 25
    assert result.triggers == []


def test_new_recipient_unusual_amount_and_odd_hour_scores_high():
    result = analyse_behaviour(
        amount=6.5,
        hour_of_day=3,
        is_new_recipient=True,
        wallet_avg_amount=0.5,
        wallet_usual_tx_per_day=1.0,
        recent_tx_count_today=4,
        wallet_failed_auth_count=2,
    )
    assert result.behaviour_score > 50
    assert "New destination wallet detected" in result.triggers
    assert "Transaction at unusual hour" in result.triggers
