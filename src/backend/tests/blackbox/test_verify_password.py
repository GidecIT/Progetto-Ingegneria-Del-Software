from __future__ import annotations

import pytest

from participium.core.security import verify_password, hash_password

PASSWORD = "pass123"
CORRECT_HASH = hash_password(PASSWORD)
WRONG_HASH = hash_password("xxx")
UPPERCASE_HASH = hash_password("Pass123")
SHORTER_HASH = hash_password("pass12")
LONGER_HASH = hash_password("pass1234")


@pytest.fixture
def seed_verify_password_data() -> None:
    # Non sono presenti dati da persistere in memoria per questi test
    pass


def test_verify_password_success(seed_verify_password_data: None) -> None:
    # VP01, VPB01
    assert verify_password(PASSWORD, CORRECT_HASH) is True


def test_verify_password_wrong_hash(seed_verify_password_data: None) -> None:
    # VP02
    assert verify_password(PASSWORD, WRONG_HASH) is False


def test_verify_password_case_sensitivity(seed_verify_password_data: None) -> None:
    # VPB02
    assert verify_password(PASSWORD, UPPERCASE_HASH) is False


def test_verify_password_shorter_hash(seed_verify_password_data: None) -> None:
    # VPB03
    assert verify_password(PASSWORD, SHORTER_HASH) is False


def test_verify_password_longer_hash(seed_verify_password_data: None) -> None:
    # VPB04
    assert verify_password(PASSWORD, LONGER_HASH) is False
