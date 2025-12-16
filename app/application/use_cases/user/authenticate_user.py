from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.domain.uow.unit_of_work import UnitOfWork


class AuthenticateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        uow: UnitOfWork,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.uow = uow

    async def execute(self, email: str, password: str):
        async with self.uow:
            user = await self.user_repository.get_by_email(email)

            if not user:
                raise ValueError("Invalid credentials")

            if not user.is_active:
                raise ValueError("User is inactive")

            if not self.password_hasher.verify(password, user.hashed_password):
                raise ValueError("Invalid credentials")

            return user
