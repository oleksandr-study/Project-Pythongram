from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.routes.transform_image_routes import router as cl_image_router

app = FastAPI()
app.include_router(cl_image_router, prefix="/images", tags=["images"])
client = TestClient(app)

def test_transform_image_url():
    response = client.get("/images/transform-image/?public_id=test_image&width=300&height=200&crop=fill")
    assert response.status_code == 200
    assert "url" in response.json()
    assert "w_300" in response.json()["url"]
    assert "h_200" in response.json()["url"]
    assert "c_fill" in response.json()["url"]

def test_transform_image_error_handling():
    response = client.get("/images/transform-image/")
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "public_id" in response.json()["detail"]
