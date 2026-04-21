from __future__ import annotations

import pytest

from participium.core.exceptions import ValidationError
from participium.core.security import verify_password

PWD1 = "pass123"
HASH1 = "hash_of_pass123"
HASH2 = "wrong_hash"

@pytest.mark.skip(reason="Disabled.")
def test_vp01_success() -> None:
    """Password e hash corretti"""
    assert verify_password(PWD1, HASH1) is True

@pytest.mark.skip(reason="Disabled.")
def test_vp02_wrong_hash() -> None:
    """Password corretta, hash errato"""
    assert verify_password(PWD1, HASH2) is False

@pytest.mark.skip(reason="Disabled.")
def test_vp03_none_hash() -> None:
    """Password fornita, hash omesso"""
    with pytest.raises(ValidationError):
        verify_password(PWD1, None)  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_vp04_none_password() -> None:
    """Password omessa, hash fornito"""
    with pytest.raises(ValidationError):
        verify_password(None, HASH1)  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_vp05_both_none() -> None:
    """Entrambi i campi omessi"""
    with pytest.raises(ValidationError):
        verify_password(None, None)  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_vpb01_equality() -> None:
    """Uguaglianza"""
    assert verify_password("pass123", "hash_of_pass123") is True

@pytest.mark.skip(reason="Disabled.")
def test_vpb02_case_difference() -> None:
    """Differenza lettera maiuscola"""
    assert verify_password("pass123", "hash_of_Pass123") is False

@pytest.mark.skip(reason="Disabled.")
def test_vpb03_one_less_char() -> None:
    """Un carattere in meno"""
    assert verify_password("pass123", "hash_of_pass12") is False

@pytest.mark.skip(reason="Disabled.")
def test_vpb04_one_more_char() -> None:
    """Un carattere in più"""
    assert verify_password("pass123", "hash_of_pass1234") is False

@pytest.mark.skip(reason="Disabled.")
def test_vpb05_empty_string() -> None:
    """Stringa vuota"""
    assert verify_password("", "hash_of_") is True
