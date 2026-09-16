from fastapi.testclient import TestClient
from backend.main import app
def test_health():
    with TestClient(app) as c:assert c.get("/health").status_code==200
def test_gateways():
    with TestClient(app) as c:assert len(c.get("/api/gateways").json())>=1
def test_unknown():
    with TestClient(app) as c:assert c.get("/api/gateways/UNKNOWN").status_code==404
def test_e2e():
    with TestClient(app) as c:
        r=c.post("/api/recommendations/run");assert r.status_code==200
        assert r.json()["generated_count"]>=1
def test_analytics():
    with TestClient(app) as c:assert c.get("/api/analytics/summary").status_code==200
def test_config():
    with TestClient(app) as c:assert c.get("/api/admin/config").json()["visit_cost_eur"]==380
