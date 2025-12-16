from uuid import uuid4

from app.infrastructure.security.jwt_service import JWTService


def test_create_and_decode_access_token():
    service = JWTService("secret")
    user_id = uuid4()

    token = service.create_access_token(user_id)
    payload = service.decode_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"