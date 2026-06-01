from __future__ import annotations
from participium.models.user import User
from participium.models.report import Report
from participium.models.notification import Notification
from participium.models.enums import NotificationType
from participium.services.notification_service import NotificationService

from unittest.mock import Mock

import pytest


pytestmark = pytest.mark.blackbox


@pytest.fixture
def notification_service_bundle():
    session = Mock()
    repo = Mock()
    email = Mock()
    service = NotificationService(session=session, notification_repository=repo, email_gateway=email)
    return {"service": service, "session": session, "repo": repo, "email": email}


def test_cn01_create_with_user_and_report(notification_service_bundle):
    """TC-ID: CN01 - Utente esiste, Segnalazione presente"""
    svc = notification_service_bundle["service"]
    repo = notification_service_bundle["repo"]
    email_gw = notification_service_bundle["email"]

    user = User(id=1, email="user1@example.com", email_notifications_enabled=True)
    report = Report(id=101)

    result = svc.create_notification(user, NotificationType.MESSAGE, "Aggiornamento", "Messaggio", report=report)

    assert isinstance(result, Notification)
    assert result.user_id == 1
    assert result.report_id == 101
    assert result.title == "Aggiornamento"
    assert result.body == "Messaggio"
    assert result.type == NotificationType.MESSAGE
    repo.add.assert_called_once_with(result)
    email_gw.send.assert_called_once_with("user1@example.com", "Aggiornamento", "Messaggio")


def test_cn02_create_with_user_no_report(notification_service_bundle):
    """TC-ID: CN02 - utente esiste (senza report)"""
    svc = notification_service_bundle["service"]
    repo = notification_service_bundle["repo"]
    email_gw = notification_service_bundle["email"]

    user = User(id=1, email="user1@example.com", email_notifications_enabled=False)

    result = svc.create_notification(user, NotificationType.MESSAGE, "Aggiornamento", "Messaggio", report=None)

    assert isinstance(result, Notification)
    assert result.user_id == 1
    assert result.report_id is None
    email_gw.send.assert_not_called()
    repo.add.assert_called_once()


def test_cn03_create_no_user_with_report(notification_service_bundle):
    """TC-ID: CN03 - Segnalazione presente (senza utente)"""
    svc = notification_service_bundle["service"]
    repo = notification_service_bundle["repo"]

    report = Report(id=101)

    result = svc.create_notification(None, NotificationType.MESSAGE, "Aggiornamento", "Messaggio", report=report)

    assert result is None
    repo.add.assert_not_called()


def test_cn04_create_no_user_no_report(notification_service_bundle):
    """TC-ID: CN04 - Nessun utente, nessun report"""
    svc = notification_service_bundle["service"]
    repo = notification_service_bundle["repo"]

    result = svc.create_notification(None, NotificationType.MESSAGE, "Aggiornamento", "Messaggio", report=None)

    assert result is None
    repo.add.assert_not_called()

def test_cn05_email_failure_is_swallowed(notification_service_bundle):
    """TC-ID: CN05 - Il gateway email fallisce (Exception), ma l'errore viene gestito internamente senza bloccare il sistema"""
    svc = notification_service_bundle["service"]
    repo = notification_service_bundle["repo"]
    email_gw = notification_service_bundle["email"]

    email_gw.send.side_effect = Exception("SMTP Gateway Error")

    user = User(id=1, email="user1@example.com", email_notifications_enabled=True)

    result = svc.create_notification(user, NotificationType.MESSAGE, "Aggiornamento", "Messaggio")

    assert isinstance(result, Notification)
    repo.add.assert_called_once_with(result)
    email_gw.send.assert_called_once()


def test_cnb01_boundary_title_body_min_length(notification_service_bundle):
    """TC-ID: CNB01 - Boundary around title and body (1 char)"""
    svc = notification_service_bundle["service"]
    user = User(id=1, email="u@e.com", email_notifications_enabled=False)

    result = svc.create_notification(user, NotificationType.MESSAGE, "a", "b")

    assert isinstance(result, Notification)
    assert result.title == "a"
    assert result.body == "b"


def test_cnb02_boundary_empty_title(notification_service_bundle):
    """TC-ID: CNB02 - Boundary around title and body (empty title)"""
    svc = notification_service_bundle["service"]
    user = User(id=1, email="u@e.com", email_notifications_enabled=False)

    result = svc.create_notification(user, NotificationType.MESSAGE, "", "b")

    assert isinstance(result, Notification)
    assert result.title == ""


def test_cnb03_boundary_empty_body(notification_service_bundle):
    """TC-ID: CNB03 - Boundary around title and body (empty body)"""
    svc = notification_service_bundle["service"]
    user = User(id=1, email="u@e.com", email_notifications_enabled=False)

    result = svc.create_notification(user, NotificationType.MESSAGE, "a", "")

    assert isinstance(result, Notification)
    assert result.body == ""