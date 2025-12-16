from app.application.dto.user_dto import CreateUserDTO, UserDTO
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.domain.uow.unit_of_work import UnitOfWork


class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        uow: UnitOfWork,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.uow = uow

    async def execute(self, data: CreateUserDTO) -> UserDTO:
        async with self.uow:
            existing_user = await self.user_repository.get_by_email(data.email)
            if existing_user:
                raise ValueError("User with this email already exists")

            hashed_password = self.password_hasher.hash(data.password)

            user = User.create(
                email=data.email,
                hashed_password=hashed_password,
            )

            await self.user_repository.create(user)

            return UserDTO(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            )
