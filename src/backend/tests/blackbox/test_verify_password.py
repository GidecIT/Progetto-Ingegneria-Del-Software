from __future__ import annotations

import pytest

from participium.core.security import verify_password

# Utilizziamo stringhe costanti per effettuare i test a causa di una mancanza di una funzione che calcola l'hash realmente 
PASSWORD = "pass123"
CORRECT_HASH = "HASH_OF_pass123"
WRONG_HASH = "HASH_OF_xxx"
UPPERCASE_HASH = "HASH_OF_Pass123"
SHORTER_HASH = "HASH_OF_pass12"
LONGER_HASH = "HASH_OF_pass1234"


@pytest.fixture
def seed_verify_password_data() -> None:
    # Non sono presenti dati da persistere in memoria per questi test
    pass


@pytest.mark.skip(reason="Disabled.")
def test_verify_password_success(seed_verify_password_data: None) -> None:
    # VP01, VPB01
    assert verify_password(PASSWORD, CORRECT_HASH) is True


@pytest.mark.skip(reason="Disabled.")
def test_verify_password_wrong_hash(seed_verify_password_data: None) -> None:
    # VP02
    assert verify_password(PASSWORD, WRONG_HASH) is False


@pytest.mark.skip(reason="Disabled.")
def test_verify_password_case_sensitivity(seed_verify_password_data: None) -> None:
    # VPB02
    assert verify_password(PASSWORD, UPPERCASE_HASH) is False


@pytest.mark.skip(reason="Disabled.")
def test_verify_password_shorter_hash(seed_verify_password_data: None) -> None:
    # VPB03
    assert verify_password(PASSWORD, SHORTER_HASH) is False


@pytest.mark.skip(reason="Disabled.")
def test_verify_password_longer_hash(seed_verify_password_data: None) -> None:
    # VPB04
    assert verify_password(PASSWORD, LONGER_HASH) is False
