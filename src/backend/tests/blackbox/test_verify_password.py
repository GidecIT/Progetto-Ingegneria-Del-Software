from __future__ import annotations

import pytest

"""
Per questa test suite assumo l'esistenza di una funzione hash(), 
visto che deve ritornare una stringa non posso usare quella di
Python base. Dato che non è presente nel source, assumo che sia
presente un'implementazione in core.security.
"""
from participium.core.security import verify_password, hash

def test_vp01_success() -> None:
    assert verify_password("pass123", hash("pass123")) is True

def test_vp02_wrong_hash() -> None:
    assert verify_password("pass123", hash("xxx")) is False

def test_vp03_empty_string() -> None:
    assert verify_password("", hash("")) is True
# Boundary Tests
def test_vp01_exact_boundary() -> None:
    assert verify_password("pass123", hash("pass123")) is True

def test_vpb02_immediately_above_case() -> None:
    assert verify_password("pass123", hash("Pass123")) is False

def test_vpb03_immediately_below_length() -> None:
    assert verify_password("pass123", hash("pass12")) is False

def test_vpb04_immediately_above_length() -> None:
    assert verify_password("pass123", hash("pass1234")) is False
