def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["service"] == "q-shield-backend"


def test_system_status(client):
    response = client.get("/api/v1/health/system")
    assert response.status_code == 200
    body = response.json()
    assert body["api"] == "ONLINE"
    assert body["database"] == "ONLINE"
