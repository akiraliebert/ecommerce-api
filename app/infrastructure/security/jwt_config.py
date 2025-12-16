from datetime import timedelta


class JWTConfig:
    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE = timedelta(days=7)