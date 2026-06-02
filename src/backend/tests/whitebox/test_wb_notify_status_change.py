from __future__ import annotations

import pytest

from participium.services.notification_service import NotificationService


pytestmark = pytest.mark.whitebox




from unittest.mock import Mock
from participium.models.enums import NotificationType

def _user(id: int) -> Mock:
    user = Mock()
    user.id = id
    return user


@pytest.fixture
def notification_service() -> NotificationService:
    session = Mock()
    notification_repository = Mock()
    email_gateway = Mock()
    service = NotificationService(
        session=session,
        notification_repository=notification_repository,
        email_gateway=email_gateway,
    )
    service.create_notification = Mock()
    return service


def test_empty_recipients_case(notification_service: NotificationService) -> None:
    notification_service.notify_status_change(recipients=[], report=Mock(id=1), body="Test notifica")
    notification_service.create_notification.assert_not_called()

def test_none_recipient_case(notification_service: NotificationService) -> None:
    notification_service.notify_status_change(recipients=[None], report=Mock(id=2), body="Test notifica")
    notification_service.create_notification.assert_not_called()

def test_single_user_case(notification_service: NotificationService) -> None:
    service = notification_service
    recipient = _user(id=3)
    report = Mock(id=42)
    body = "Test notifica"
    service.notify_status_change([recipient], report, body)
    service.create_notification.assert_called_once_with(
        recipient,
        NotificationType.STATUS_CHANGE,
        f"Report #{report.id} status updated",
        body,
        report=report,
    )

def test_duplicate_users_case(notification_service: NotificationService) -> None:
    service = notification_service
    recipient1 = _user(id=4)
    recipient2 = _user(id=4)
    report = Mock(id=23)
    body = "Test notifica"
    service.notify_status_change([recipient1, recipient2], report, body)

    service.create_notification.assert_called_once_with(
        recipient1,
        NotificationType.STATUS_CHANGE,
        f"Report #{report.id} status updated",
        body,
        report=report,
    )