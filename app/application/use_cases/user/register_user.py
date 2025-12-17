from app.application.dto.user_dto import CreateUserDTO, UserDTO
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.domain.uow.unit_of_work import UnitOfWork


class RegisterUserUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self.uow = uow
        self.users = user_repo
        self.password_hasher = password_hasher

    async def execute(self, data: CreateUserDTO) -> UserDTO:
        async with self.uow:
            existing_user = await self.users.get_by_email(data.email)
            if existing_user:
                raise ValueError("User with this email already exists")

            hashed_password = self.password_hasher.hash(data.password)

            user = User.create(
                email=data.email,
                hashed_password=hashed_password,
            )

            await self.users.create(user)

            return UserDTO(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            )
