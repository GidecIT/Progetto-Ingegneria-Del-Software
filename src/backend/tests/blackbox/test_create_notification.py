from __future__ import annotations

from participium.services.notification_service import NotificationService
from __future__ import annotations

from unittest.mock import Mock

import pytest

from participium.models.user import User
from participium.models.report import Report
from participium.models.notification import Notification
from participium.models.enums import NotificationType
from participium.services.notification_service import NotificationService

pytestmark = pytest.mark.blackbox


@pytest.fixture
def notification_service_bundle():
    session = Mock()
    repo = Mock()
    email = Mock()
    service = NotificationService(session=session, notification_repository=repo, email_gateway=email)
    return {"service": service, "session": session, "repo": repo, "email": email}


def test_create_notification_with_report_sets_fields_and_persists(notification_service_bundle):
    svc = notification_service_bundle["service"]
    repo = notification_service_bundle["repo"]
    session = notification_service_bundle["session"]

    # make repo.add simulate DB assigning an id
    def add_side_effect(notification: Notification) -> None:
        notification.id = 555

    repo.add.side_effect = add_side_effect

    user = User(id=10, email="u@example.com", email_notifications_enabled=True)
    report = Report(id=20)

    result = svc.create_notification(user, NotificationType.MESSAGE, "Aggiornamento", "Messaggio", report=report)

    assert isinstance(result, Notification)
    assert result.id == 555
    repo.add.assert_called_once()
    added = repo.add.call_args[0][0]
    assert added.user_id == user.id
    assert added.report_id == report.id
    assert added.title == "Aggiornamento"
    assert added.body == "Messaggio"
    assert added.type == NotificationType.MESSAGE
    session.commit.assert_called_once()


def test_create_notification_without_report_persists_with_none_report_id(notification_service_bundle):
    svc = notification_service_bundle["service"]
    repo = notification_service_bundle["repo"]
    session = notification_service_bundle["session"]

    user = User(id=11, email="u2@example.com", email_notifications_enabled=False)

    result = svc.create_notification(user, NotificationType.MESSAGE, "Titolo", "Body", report=None)

    assert isinstance(result, Notification)
    repo.add.assert_called_once()
    added = repo.add.call_args[0][0]
    assert added.user_id == user.id
    assert added.report_id is None
    session.commit.assert_called_once()


def test_create_notification_with_no_user_returns_none_and_no_persistence(notification_service_bundle):
    svc = notification_service_bundle["service"]
    repo = notification_service_bundle["repo"]
    session = notification_service_bundle["session"]
    email = notification_service_bundle["email"]

    result = svc.create_notification(None, NotificationType.MESSAGE, "Titolo", "Body", report=Report(id=1))

    assert result is None
    repo.add.assert_not_called()
    session.commit.assert_not_called()
    email.send.assert_not_called()