from __future__ import annotations

import pytest

from participium.core.security import verify_password

def hash_mock(password: str) -> str:
    """Mock hash function for testing purposes."""
    return f"hash_{password}"

def test_vp01_success() -> None:
    """VP01: Password e hash corretti -> True"""
    assert verify_password("pass123", hash_mock("pass123")) is True

def test_vp02_wrong_hash() -> None:
    """VP02: Hash errato -> False"""
    assert verify_password("pass123", hash_mock("xxx")) is False

def test_vp03_empty_string() -> None:
    """VP03: Stringa vuota -> True"""
    assert verify_password("", hash_mock("")) is True

# Boundary Tests
def test_vp01_exact_boundary() -> None:
    """VP01: Exact Boundary -> True"""
    assert verify_password("pass123", hash_mock("pass123")) is True

def test_vpb02_immediately_above_case() -> None:
    """VPB02: Immediately above (case difference) -> False"""
    assert verify_password("pass123", hash_mock("Pass123")) is False

def test_vpb03_immediately_below_length() -> None:
    """VPB03: Immediately below (one less char) -> False"""
    assert verify_password("pass123", hash_mock("pass12")) is False

def test_vpb04_immediately_above_length() -> None:
    """VPB04: Immediately above (one more char) -> False"""
    assert verify_password("pass123", hash_mock("pass1234")) is False
