"""Failure injection tests (Section 52): malformed input must fail safely
with clear validation errors, never a silent approval."""


def test_missing_sender_rejected(client):
    response = client.post(
        "/api/v1/transactions",
        json={"receiver_address": "WALLET-BETA", "amount": 1.0, "currency": "ETH"},
    )
    assert response.status_code == 422


def test_negative_amount_rejected(client):
    response = client.post(
        "/api/v1/transactions",
        json={
            "sender_address": "WALLET-ALPHA",
            "receiver_address": "WALLET-BETA",
            "amount": -5,
            "currency": "ETH",
        },
    )
    assert response.status_code == 422


def test_zero_amount_rejected(client):
    response = client.post(
        "/api/v1/transactions",
        json={
            "sender_address": "WALLET-ALPHA",
            "receiver_address": "WALLET-BETA",
            "amount": 0,
            "currency": "ETH",
        },
    )
    assert response.status_code == 422


def test_invalid_authentication_status_rejected(client):
    response = client.post(
        "/api/v1/transactions",
        json={
            "sender_address": "WALLET-ALPHA",
            "receiver_address": "WALLET-BETA",
            "amount": 1.0,
            "currency": "ETH",
            "authentication_status": "MAYBE",
        },
    )
    assert response.status_code == 422


def test_unknown_transaction_lookup_returns_404(client):
    response = client.get("/api/v1/transactions/TX-QS-DOES-NOT-EXIST")
    assert response.status_code == 404


def test_unknown_scenario_returns_404(client):
    response = client.post("/api/v1/scenarios/not-a-real-scenario/run")
    assert response.status_code == 404
