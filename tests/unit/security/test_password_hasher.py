from app.infrastructure.security.password_hasher import PasswordHasher

def test_password_hash_and_verify():
    hasher = PasswordHasher()
    password = "super-secret"

    hashed = hasher.hash(password)

    assert hashed != password
    assert hasher.verify(password, hashed)
    assert not hasher.verify("wrong", hashed)