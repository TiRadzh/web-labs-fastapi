from app.main import app

def test_routes():
    assert "/api/v1/tasks" in app.openapi()["paths"]
