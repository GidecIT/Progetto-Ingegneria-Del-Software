from __future__ import annotations

from unittest.mock import MagicMock
import pytest

from participium.core.exceptions import ValidationError
from participium.models.enums import Role
from participium.services.user_service import UserService

pytestmark = pytest.mark.whitebox

@pytest.fixture
def user_repository_mock():
    """Fixture for mocking the user repository."""
    return MagicMock()

@pytest.fixture
def category_repository_mock():
    """Fixture for mocking the category repository."""
    return MagicMock()

@pytest.fixture
def db_session_mock():
    """Fixture for mocking the database session."""
    return MagicMock()

@pytest.fixture
def user_service(user_repository_mock, category_repository_mock, db_session_mock):
    """Fixture for the UserService with mocked dependencies."""

    return UserService(
        user_repository=user_repository_mock,
        category_repository=category_repository_mock,
        session=db_session_mock,
        session=db_session_mock,
    )

def test_uu01_update_user_success(user_service, user_repository_mock):
    """UU-01: Verifica il percorso di successo con l'aggiornamento di più campi."""
    user = MagicMock()
    user.id = 1
    user.first_name = "Old Name"
    user.is_active = True
    user_repository_mock.get_by_id.return_value = user

    payload = {"first_name": "New Name", "is_active": False}

    updated_user = user_service.update_user(1, payload)

    user_repository_mock.get_by_id.assert_called_once_with(1)
    assert updated_user.first_name == "New Name"
    assert updated_user.is_active is False
    user_service.session.commit.assert_called_once()


def test_uu02_update_user_username_conflict(user_service, user_repository_mock):
    """UU-02: Testa il conflitto di username."""
    user = MagicMock()
    user.id = 1
    user.username = "old_user"
    user_repository_mock.get_by_id.return_value = user
    user_repository_mock.get_by_username.return_value = MagicMock()

    payload = {"username": "new_user"}

    with pytest.raises(ValidationError, match="Username already in use."):
        user_service.update_user(1, payload)

    user_repository_mock.get_by_id.assert_called_once_with(1)
    user_repository_mock.get_by_username.assert_called_once_with("new_user")
    user_service.session.commit.assert_not_called()

    user_service.session.commit.assert_not_called()

def test_uu03_update_user_email_conflict(user_service, user_repository_mock):
    """UU-03: Testa il conflitto di email."""
    user = MagicMock()
    user.id = 1
    user.email = "old@email.com"
    user_repository_mock.get_by_id.return_value = user
    user_repository_mock.get_by_email.return_value = MagicMock()

    payload = {"email": "new@email.com"}

    with pytest.raises(ValidationError, match="Email already in use."):
        user_service.update_user(1, payload)

    user_repository_mock.get_by_id.assert_called_once_with(1)
    user_repository_mock.get_by_email.assert_called_once_with("new@email.com")
    user_service.session.commit.assert_not_called()

def test_uu04_update_user_role_with_category(user_service, user_repository_mock, category_repository_mock):
    """UU-04: Verifica aggiornamento ruolo a OPERATOR con category_id."""
    user = MagicMock()
    user.id = 1
    user.role = Role.CITIZEN
    user.category_id = None
    user_repository_mock.get_by_id.return_value = user

    category = MagicMock()
    category.id = 5
    category_repository_mock.get_by_id.return_value = category

    payload = {"role": Role.OPERATOR, "category_id": 5}

    updated_user = user_service.update_user(1, payload)

    assert updated_user.role == Role.OPERATOR
    assert updated_user.category_id == 5
    user_service.session.commit.assert_called_once()

def test_uu05_update_user_empty_payload(user_service, user_repository_mock):
    """UU-05: Payload vuoto, nessuna modifica ma commit eseguito."""
    user = MagicMock()
    user.id = 1
    user.first_name = "Test"
    user_repository_mock.get_by_id.return_value = user

    payload = {}

    updated_user = user_service.update_user(1, payload)

    assert updated_user.first_name == "Test"
    user_service.session.commit.assert_called_once()