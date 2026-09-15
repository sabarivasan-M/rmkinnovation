"""End-to-end pipeline test (Section 51): one transaction id must remain
consistent from submission through every downstream engine, decision, and
audit record."""


def test_normal_scenario_end_to_end():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/transactions",
            json={
                "sender_address": "WALLET-ALPHA",
                "receiver_address": "WALLET-BETA",
                "amount": 0.85,
                "currency": "ETH",
                "authentication_status": "SUCCESS",
                "simulated_hour_of_day": 14,
            },
        )
        assert response.status_code == 200
        body = response.json()
        transaction_id = body["transaction_id"]
        assert transaction_id.startswith("TX-QS-")

        assert body["risk"]["risk_level"] == "LOW"
        assert body["decision"]["decision"] == "APPROVE"

        detail = client.get(f"/api/v1/transactions/{transaction_id}").json()
        assert detail["transaction"]["transaction_id"] == transaction_id
        assert detail["risk"]["transaction_id"] == transaction_id
        assert detail["decision"]["transaction_id"] == transaction_id

        audit = client.get("/api/v1/audit").json()
        matching = [a for a in audit if a["transaction_id"] == transaction_id]
        assert len(matching) == 1
        assert matching[0]["decision"] == "APPROVE"
        # Blockchain disabled in tests -> must not falsely claim confirmation (Section 53).
        assert matching[0]["blockchain_status"] == "UNAVAILABLE"


def test_suspicious_scenario_flags_or_rejects():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.post("/api/v1/scenarios/suspicious/run")
        assert response.status_code == 200
        body = response.json()
        assert body["risk"]["risk_level"] in ("HIGH", "CRITICAL")
        assert body["decision"]["decision"] in ("FLAG", "REJECT")
        assert len(body["risk"]["primary_contributors"]) > 0


def test_authentication_failure_scenario_always_rejects():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.post("/api/v1/scenarios/authentication_failure/run")
        assert response.status_code == 200
        body = response.json()
        assert body["decision"]["decision"] == "REJECT"
        assert body["decision"]["policy_trigger"] == "AUTHENTICATION_FAILURE_OVERRIDE"


def test_quantum_exposed_scenario_surfaces_crypto_risk():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        response = client.post("/api/v1/scenarios/quantum_exposed/run")
        assert response.status_code == 200
        body = response.json()
        assert body["crypto"]["algorithm"] == "RSA-2048"
        assert body["crypto"]["quantum_exposure"] == "CRITICAL"
