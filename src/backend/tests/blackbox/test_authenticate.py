from __future__ import annotations
  
import pytest
  
from participium.services.auth_service import AuthService
from participium.models.user import User
from participium.core.exceptions import AuthenticationError

@pytest.fixture
def auth_service() -> AuthService:
    return AuthService()

@pytest.mark.skip(reason="Disabled")
@pytest.mark.parametrize(
    "identifier,password,expected_exception",
    [
        ("mario_r", "pass123", None),  # AU01: user exists, active, email verified
        ("mario.r@polito.it", "pass123", None),  # AU02
        ("mario_r", "wrong", AuthenticationError),  # AU03
        ("mario.r@polito.it", "wrong", AuthenticationError),  # AU04
        ("unknown_user", "pass123", AuthenticationError),  # AU05
        ("unknown@mail.it", "pass123", AuthenticationError),  # AU06

        # Boundary cases per "identifier"
        (None, "pass123", AuthenticationError),  # AUB01
        ("", "pass123", AuthenticationError),  # AUB02
        (" ", "pass123", AuthenticationError),  # AUB03

        # Boundary cases per "password"
        ("mario_r", None, AuthenticationError),  # AUB04
        ("mario.r@polito.it", None, AuthenticationError),  # AUB05 
        ("mario_r", "", AuthenticationError),  # AUB06
        ("mario_r", " ", AuthenticationError),  # AUB07

        # Boundary cases per User.is_active e User.is_email_verified
        ("mario_rossi", "pass123", AuthenticationError),  # AUB08 (is_active == False)
        ("mario_rossi@polito.it", "pass123", AuthenticationError),  # AUB09 (is_email_verified == False)
    ],
)
def test_authenticate(auth_service, identifier, password, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            auth_service.authenticate(identifier, password)
    else:
        result = auth_service.authenticate(identifier, password)
        assert isinstance(result, User)