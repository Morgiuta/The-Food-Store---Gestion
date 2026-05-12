import pytest


class TestHealthEndpoint:
    async def test_health_returns_200_with_status_ok(self, client):
        response = await client.get("/api/v1/health")
        assert response.status_code == 200

    async def test_health_response_structure(self, client):
        response = await client.get("/api/v1/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
        assert len(data) == 1
