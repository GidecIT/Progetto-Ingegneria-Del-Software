from __future__ import annotations
from werkzeug.datastructures import FileStorage

from participium.core.exceptions import ValidationError
from participium.models.user import User
from participium.services.user_service import UserService

from unittest.mock import Mock

import pytest


pytestmark = pytest.mark.blackbox


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


def test_update_profile_success_updates_fields_and_saves_picture(user_service_bundle):
    svc = user_service_bundle["service"]
    repo = user_service_bundle["user_repository"]
    storage = user_service_bundle["storage_service"]
    session = user_service_bundle["session"]

    user = User(id=1, username="olduser", first_name="Old", last_name="Name", email_notifications_enabled=False)

    # username not in use
    repo.get_by_username.return_value = None

    # simulate storage saving and returning a path
    storage.save.return_value = "profiles/1.jpg"

    fake_file = Mock(spec=FileStorage)
    fake_file.filename = "pic.jpg"
    fake_file.content_type = "image/jpeg"

    updated = svc.update_profile(
        user,
        username="nuovo",
        first_name="Mario",
        last_name="Rossi",
        email_notifications_enabled=True,
        profile_picture=fake_file,
    )

    assert isinstance(updated, User)
    assert updated.username == "nuovo"
    assert updated.first_name == "Mario"
    assert updated.last_name == "Rossi"
    assert updated.email_notifications_enabled is True
    storage.save.assert_called_once_with(fake_file)
    session.commit.assert_called_once()


def test_update_profile_raises_when_username_already_used(user_service_bundle):
    svc = user_service_bundle["service"]
    repo = user_service_bundle["user_repository"]

    user = User(id=1, username="user1")

    # another user exists with requested username
    repo.get_by_username.return_value = User(id=2, username="nuovo")

    with pytest.raises(ValidationError):
        svc.update_profile(user, username="nuovo")


def test_update_profile_none_username_does_not_change_existing_username(user_service_bundle):
    svc = user_service_bundle["service"]
    repo = user_service_bundle["user_repository"]
    session = user_service_bundle["session"]

    user = User(id=1, username="user1", first_name="Old", last_name="Old")

    # ensure get_by_username not triggered (or returns None)
    repo.get_by_username.return_value = None

    updated = svc.update_profile(user, username=None, first_name="Mario", last_name="Rossi", profile_picture=None)

    assert isinstance(updated, User)
    assert updated.username == "user1"
    assert updated.first_name == "Mario"
    assert updated.last_name == "Rossi"
    session.commit.assert_called_once()


def test_update_profile_optional_none_fields_do_not_change_except_provided_flags(user_service_bundle):
    svc = user_service_bundle["service"]
    session = user_service_bundle["session"]

    user = User(
        id=1,
        username="user1",
        first_name="Jane",
        last_name="Doe",
        email_notifications_enabled=True,
        profile_picture_path=None,
    )

    updated = svc.update_profile(user, username=None, first_name=None, last_name=None, email_notifications_enabled=False, profile_picture=None)

    assert isinstance(updated, User)
    assert updated.username == "user1"
    assert updated.first_name == "Jane"
    assert updated.last_name == "Doe"
    assert updated.email_notifications_enabled is False
    session.commit.assert_called_once()