from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.domain.uow.unit_of_work import UnitOfWork


class AuthenticateUserUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self.uow = uow
        self.users = user_repo
        self.password_hasher = password_hasher

    async def execute(self, email: str, password: str):
        async with self.uow:
            user = await self.users.get_by_email(email)

            if not user:
                raise ValueError("Invalid credentials")

            if not user.is_active:
                raise ValueError("User is inactive")

            if not self.password_hasher.verify(password, user.hashed_password):
                raise ValueError("Invalid credentials")

            return user
