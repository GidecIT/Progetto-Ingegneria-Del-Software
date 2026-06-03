from __future__ import annotations

import pytest
from participium.core.security import generate_token, hash_password, verify_password

pytestmark = pytest.mark.unit


def test_password_hash_and_verify():
    password = "SecretPass2026!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_generate_token_produces_unique_values():
    t1, t2 = generate_token(), generate_token()

    assert t1 != t2
    assert len(t1) > 20