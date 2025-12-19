from datetime import datetime, timezone
from jose import jwt, JWTError
from uuid import UUID

from app.infrastructure.security.jwt_config import JWTConfig


class JWTService:
    def __init__(self, secret_access: str, secret_refresh: str):
        self.secret_access = secret_access
        self.secret_refresh = secret_refresh

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
            self.secret_access,
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
            self.secret_refresh,
            algorithm=JWTConfig.ALGORITHM,
        )

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.secret_access,
                algorithms=[JWTConfig.ALGORITHM],
            )
        except JWTError:
            raise ValueError("Invalid token")

    def decode_refresh_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.secret_refresh,
                algorithms=[JWTConfig.ALGORITHM],
            )
        except JWTError:
            raise ValueError("Invalid token")
