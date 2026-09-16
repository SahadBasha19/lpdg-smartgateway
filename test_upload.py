from fastapi.testclient import TestClient
from backend.main import app
def test_bad_extension():
    with TestClient(app) as c:assert c.post("/api/admin/upload-csv",files={"file":("x.txt",b"x")}).status_code==400
def test_missing_columns():
    with TestClient(app) as c:
        r=c.post("/api/admin/upload-csv",files={"file":("x.csv",b"gateway_id,name\nGW-X,T\n")})
        assert r.status_code==400
