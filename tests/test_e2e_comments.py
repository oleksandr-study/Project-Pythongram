import pytest
from unittest.mock import MagicMock, patch
from httpx import AsyncClient
from main import app
from src.services.auth import auth_service
from src.models.models import User as Test_user


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: Test_user = session.query(Test_user).filter(Test_user.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"email": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_comment(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "api/images/1/comments",
            json={"comment": "test_tag"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["comment"] == "test_tag"
        assert "id" in data

    # with patch.object(auth_service, 'r') as redis_mock:
    #     redis_mock.get.return_value = None
    #     token = get_token
    #     headers = {"Authorization": f"Bearer {token}"}
    #     response = client.post("api/images/1/comments", headers=headers, json={
    #         "title": "test",
    #         "description": "test",
    #     })
    #     assert response.status_code == 201, response.text
    #     data = response.json()
    #     assert "id" in data
    #     assert data["title"] == "test"
    #     assert data["description"] == "test"


# @pytest.mark.anyio
# async def test_get_comments():
#     async with AsyncClient(app=app, base_url='http://test') as ac:
#         response = await ac.get('/images/1/comments/')
#     assert response.status_code == 200


# @pytest.mark.anyio
# async def test_create_comment():
#     async with AsyncClient(app=app, base_url='http://test') as ac:
#         response = await ac.post('/images/1/comments/', json={'text': 'Comment'})
#     assert response.status_code == 200
# @pytest.mark.anyio
# async def test_update_comm():
#     async with AsyncClient(app=app, base_url='http://test') as ac:
#         response = await ac.patch('/images/comments/1/', json={'text': 'Updated comment'})
#     assert response.status_code == 200
# @pytest.mark.anyio
# async def test_delete_comment():
#     async with AsyncClient(app=app, base_url='http://test') as ac:
#         response = await ac.delete('/images/comments/1/')
#     assert response.status_code == 200