from __future__ import annotations
from unittest.mock import Mock
  
import pytest
  
from participium.services.auth_service import AuthService
from participium.models.user import User
from participium.core.exceptions import AuthenticationError
from participium.core.security import hash_password
  
@pytest.fixture
def auth_service() -> AuthService:
    user_repo = Mock()

    def mock_get_by_identifier(identifier: str):
        if identifier in ("mario_r", "mario.r@polito.it"):
            return User(
                id=1,
                username="mario_r",
                email="mario.r@polito.it",
                password_hash=hash_password("pass123"),
                is_active=True,
                is_email_verified=True,
            )
        if identifier == "mario_rossi":
            return User(
                id=2,
                username="mario_rossi",
                email="mario_rossi@mail.it",
                password_hash=hash_password("pass123"),
                is_active=False,
                is_email_verified=True,
            )
        if identifier == "mario_rossi@polito.it":
            return User(
                id=3,
                username="mario_rossi_2",
                email="mario_rossi@polito.it",
                password_hash=hash_password("pass123"),
                is_active=True,
                is_email_verified=False,
            )
        return None

    user_repo.get_by_username_or_email.side_effect = mock_get_by_identifier
    return AuthService(
        session=Mock(),
        user_repository=user_repo,
        token_repository=Mock(),
        email_gateway=Mock(),
    )
  
##@pytest.mark.skip(reason="Disabled")
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
        (None, "pass123", AttributeError),  # AUB01
        ("", "pass123", AuthenticationError),  # AUB02
        (" ", "pass123", AuthenticationError),  # AUB03

        # Boundary cases per "password"
        ("mario_r", None, AttributeError),  # AUB04
        ("mario.r@polito.it", None, AttributeError),  # AUB05 
        ("mario_r", "", AuthenticationError),  # AUB06
        ("mario_r", " ", AuthenticationError),  # AUB07

        # Boundary cases per User.is_active e User.is_email_verified
        ("mario_rossi", "pass123", AuthenticationError),  # AUB08 (is_active == False)
        ("mario_rossi@polito.it", "pass123", AuthenticationError),  # AUB09 (is_email_verified == False)
    ],
)
def test_authenticate(auth_service, identifier, password, expected_exception):

    #if expected_exception:
    #    print("SONO NELL IF")
    #    with pytest.raises(expected_exception):
    #        auth_service.authenticate(identifier, password)
    #else:
    #    result = auth_service.authenticate(identifier, password)
    #    #stampa result
    #    print("STAMPO : ", result)
    #    assert isinstance(result, User)
    if expected_exception is None:
        result = auth_service.authenticate(identifier, password)
        assert isinstance(result, User)
    else:
        with pytest.raises(expected_exception):
            auth_service.authenticate(identifier, password)