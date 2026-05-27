from __future__ import annotations
from unittest.mock import Mock
from werkzeug.datastructures import FileStorage
import pytest
from participium.core.exceptions import ValidationError
from participium.models.user import User
from participium.services.user_service import UserService

@pytest.fixture
def user_service_bundle():
    session = Mock()
    user_repository = Mock()
    storage_service = Mock()
    service = UserService(
        session=session,
        user_repository=user_repository,
        storage_service=storage_service,
    )
    return {
        "service": service,
        "session": session,
        "user_repository": user_repository,
        "storage_service": storage_service,
    }


@pytest.fixture
def valid_pic():
    fake_file = Mock(spec=FileStorage)
    fake_file.filename = "pic.jpg"
    fake_file.content_type = "image/jpeg"
    return fake_file


def test_up01_update_profile_success(user_service_bundle, valid_pic):
    svc = user_service_bundle["service"]
    repo = user_service_bundle["user_repository"]
    storage = user_service_bundle["storage_service"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.username = "user1"
    user.first_name = "Old"
    user.last_name = "Name"
    user.email_notifications_enabled = False

    repo.get_by_username.return_value = None
    storage.save.return_value = "profiles/1.jpg"

    updated = svc.update_profile(
        user,
        username="nuovo",
        first_name="Mario",
        last_name="Rossi",
        email_notifications_enabled=True,
        profile_picture=valid_pic,
    )

    assert isinstance(updated, User)
    assert updated.username == "nuovo"
    assert updated.first_name == "Mario"
    assert updated.last_name == "Rossi"
    assert updated.email_notifications_enabled is True
    storage.save.assert_called_once_with(valid_pic)
    session.commit.assert_called_once()


def test_up02_update_profile_username_already_used(user_service_bundle, valid_pic):
    svc = user_service_bundle["service"]
    repo = user_service_bundle["user_repository"]

    user = User()
    user.id = 2
    user.username = "user2"

    another_user = User()
    another_user.id = 99
    another_user.username = "nuovo"
    repo.get_by_username.return_value = another_user

    with pytest.raises(ValidationError):
        svc.update_profile(
            user,
            username="nuovo",
            first_name="Mario",
            last_name="Rossi",
            email_notifications_enabled=True,
            profile_picture=valid_pic,
        )


def test_up03_update_profile_none_username_and_notifications(user_service_bundle, valid_pic):
    svc = user_service_bundle["service"]
    repo = user_service_bundle["user_repository"]
    storage = user_service_bundle["storage_service"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.username = "user1"
    user.first_name = "Old"
    user.last_name = "Old"
    user.email_notifications_enabled = True

    repo.get_by_username.return_value = None
    storage.save.return_value = "profiles/1.jpg"

    updated = svc.update_profile(
        user,
        username=None,
        first_name="Mario",
        last_name="Rossi",
        email_notifications_enabled=None,
        profile_picture=valid_pic,
    )

    assert isinstance(updated, User)
    assert updated.username == "user1"
    assert updated.first_name == "Mario"
    assert updated.last_name == "Rossi"
    assert updated.email_notifications_enabled is True
    storage.save.assert_called_once_with(valid_pic)
    session.commit.assert_called_once()


def test_up04_update_profile_optional_none_fields(user_service_bundle):
    svc = user_service_bundle["service"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.username = "user1"
    user.first_name = "Jane"
    user.last_name = "Doe"
    user.email_notifications_enabled = True

    updated = svc.update_profile(
        user,
        username=None,
        first_name=None,
        last_name=None,
        email_notifications_enabled=False,
        profile_picture=None,
    )

    assert isinstance(updated, User)
    assert updated.username == "user1"
    assert updated.first_name == "Jane"
    assert updated.last_name == "Doe"
    assert updated.email_notifications_enabled is False
    session.commit.assert_called_once()


def test_upb01_boundary_username_exact(user_service_bundle):
    svc = user_service_bundle["service"]
    repo = user_service_bundle["user_repository"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.username = "user1"

    repo.get_by_username.return_value = None

    updated = svc.update_profile(user, username="a")

    assert isinstance(updated, User)
    assert updated.username == "a"
    session.commit.assert_called_once()


def test_upb02_boundary_username_empty(user_service_bundle):
    svc = user_service_bundle["service"]
    repo = user_service_bundle["user_repository"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.username = "user1"

    repo.get_by_username.return_value = None

    updated = svc.update_profile(user, username="")

    assert isinstance(updated, User)
    assert updated.username == "user1"
    session.commit.assert_called_once()


def test_upb03_boundary_first_name_exact(user_service_bundle):
    svc = user_service_bundle["service"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.first_name = "Old"

    updated = svc.update_profile(user, first_name="a")

    assert isinstance(updated, User)
    assert updated.first_name == "a"
    session.commit.assert_called_once()


def test_upb04_boundary_first_name_empty(user_service_bundle):
    svc = user_service_bundle["service"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.first_name = "Old"

    updated = svc.update_profile(user, first_name="")

    assert isinstance(updated, User)
    assert updated.first_name == "Old"
    session.commit.assert_called_once()


def test_upb05_boundary_last_name_exact(user_service_bundle):
    svc = user_service_bundle["service"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.last_name = "Old"

    updated = svc.update_profile(user, last_name="a")

    assert isinstance(updated, User)
    assert updated.last_name == "a"
    session.commit.assert_called_once()


def test_upb06_boundary_last_name_empty(user_service_bundle):
    svc = user_service_bundle["service"]
    session = user_service_bundle["session"]

    user = User()
    user.id = 1
    user.last_name = "Old"

    updated = svc.update_profile(user, last_name="")

    assert isinstance(updated, User)
    assert updated.last_name == "Old"
    session.commit.assert_called_once()