from datetime import datetime, timezone
from jose import jwt, JWTError
from uuid import UUID

from app.infrastructure.security.jwt_config import JWTConfig


class JWTService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def create_access_token(self, user_id: UUID) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + JWTConfig.ACCESS_TOKEN_EXPIRE,
            "type": "access",
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=JWTConfig.ALGORITHM,
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + JWTConfig.REFRESH_TOKEN_EXPIRE,
            "type": "refresh",
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=JWTConfig.ALGORITHM,
        )

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[JWTConfig.ALGORITHM],
            )
        except JWTError:
            raise ValueError("Invalid token")