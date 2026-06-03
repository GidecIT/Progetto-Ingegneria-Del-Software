from __future__ import annotations

from unittest.mock import Mock
import pytest

from participium.models.notification import Notification
from participium.services.notification_service import NotificationService

pytestmark = pytest.mark.whitebox


def _notification(*, notification_id: int, user_id: int, report_id: int, is_read: bool = False) -> Notification:
    return Notification(
        id=notification_id,
        user_id=user_id,
        report_id=report_id,
        is_read=is_read,
    )


@pytest.fixture
def notification_service_bundle() -> dict[str, object]:
    session = Mock()
    notification_repository = Mock()
    email_gateway = Mock()
    service = NotificationService(
        session=session,
        notification_repository=notification_repository,
        email_gateway=email_gateway,
    )
    return {
        "service": service,
        "notification_repository": notification_repository,
    }


@pytest.mark.parametrize(
    "msg_report_ids, expected_output",
    [
        ([], {}),
        ([None], {}),
        ([10], {10: 1}),
        ([10, None, 10, 11], {10: 2, 11: 1}),
    ],
)
def test_count_unread_message_notifications_by_report(
        notification_service_bundle,
        msg_report_ids,
        expected_output
):
    service = notification_service_bundle["service"]
    repo = notification_service_bundle["notification_repository"]
    user_id = 10

    notifications = [
        _notification(notification_id=i, user_id=user_id, report_id=rid)
        for i, rid in enumerate(msg_report_ids)
    ]

    repo.list_unread_message_notifications.return_value = notifications

    result = service.count_unread_message_notifications_by_report(user_id=user_id)

    assert result == expected_output
    repo.list_unread_message_notifications.assert_called_once_with(user_id=user_id)