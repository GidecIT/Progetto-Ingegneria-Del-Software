import pytest
from participium.core.security import hash_password, verify_password, generate_token

pytestmark = pytest.mark.unit

def test_password_hashing_and_verification():

    password = "SecretCitizen2026!"
    h = hash_password(password)

    assert h != password
    assert verify_password(password, h) is True
    assert verify_password("wrong_password", h) is False


def test_generate_token_behavior():

    t1 = generate_token()
    t2 = generate_token()
    assert t1 != t2
    assert len(t1) > 10

    t_short = generate_token(length=16)
    assert len(t_short) < len(t1)