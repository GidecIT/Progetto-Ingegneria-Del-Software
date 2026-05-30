from __future__ import annotations

import pytest
from participium.core.exceptions import (
    DomainError, ValidationError, AuthenticationError, 
    AuthorizationError, NotFoundError
)

pytestmark = pytest.mark.unit

def test_exception_status_codes():
    assert DomainError().status_code == 400
    assert ValidationError().status_code == 400
    assert AuthenticationError().status_code == 401
    assert AuthorizationError().status_code == 403
    assert NotFoundError().status_code == 404

def test_exception_custom_message():
    exc = ValidationError("Invalid input")
    assert str(exc) == "Invalid input"

def test_exception_custom_status_code():
    exc = DomainError("Err", status_code=418)
    assert exc.status_code == 418
