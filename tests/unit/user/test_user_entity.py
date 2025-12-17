from uuid import UUID

from app.domain.entities.user import User


def test_create_user_success():
    user = User.create(email="test@gmail.com", hashed_password='dsf3kjfwijwofjs21')
    assert isinstance(user.id, UUID)
    assert user.email == 'test@gmail.com'
    assert user.hashed_password == 'dsf3kjfwijwofjs21'
    assert user.is_active is True
    assert user.created_at.tzinfo is not None
