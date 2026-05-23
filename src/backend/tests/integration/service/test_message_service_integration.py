from __future__ import annotations

import pytest

from participium.core.exceptions import AuthorizationError, ValidationError
from participium.models.enums import ReportStatus
from participium.models.message import Message
from participium.models.report import ReportStatusHistory
from participium.models.user import User


class TestMessagingService:
    def test_can_access_thread(
        self, messaging_service, test_report, test_user, admin_user, 
        test_operator, other_user, other_category
    ):
        assert messaging_service.can_access_thread(test_report, None) is False
        assert messaging_service.can_access_thread(test_report, admin_user) is True
        assert messaging_service.can_access_thread(test_report, test_user) is True
        assert messaging_service.can_access_thread(test_report, test_operator) is True
        test_report.category_id = other_category.id
        assert messaging_service.can_access_thread(test_report, test_operator) is False
        assert messaging_service.can_access_thread(test_report, other_user) is False

    def test_list_messages_success_and_denied(
        self, messaging_service, test_report, test_user, other_user, db_session
    ):
        msg = Message(
            report_id=test_report.id, 
            sender_id=test_user.id, 
            recipient_id=test_user.id, 
            body="Primo messaggio"
        )
        db_session.add(msg)
        db_session.commit()

        messages = messaging_service.list_messages(test_report, test_user)
        assert len(messages) == 1
        assert messages[0].body == "Primo messaggio"

        with pytest.raises(AuthorizationError, match="do not have access"):
            messaging_service.list_messages(test_report, other_user)

    def test_send_message_validation_empty_body(
        self, messaging_service, test_report, test_user
    ):
        with pytest.raises(ValidationError, match="Message body cannot be empty."):
            messaging_service.send_message(test_report, test_user, "   \n  ")

    def test_send_message_from_admin_to_reporter(
        self, messaging_service, test_report, admin_user, test_user, notification_service
    ):
        msg = messaging_service.send_message(
            report=test_report, 
            sender=admin_user, 
            body="Stiamo verificando"
        )

        assert msg.sender_id == admin_user.id
        assert msg.recipient_id == test_user.id
        assert msg.body == "Stiamo verificando"
        
        notifications = notification_service.list_notifications(test_user.id)
        assert any("Stiamo verificando" in n.body for n in notifications)

    def test_send_message_no_recipient_available(
        self, messaging_service, test_report, test_user
    ):
        with pytest.raises(ValidationError, match="No recipient available"):
            messaging_service.send_message(test_report, test_user, "Aiuto, nessuno risponde")

    def test_send_message_resolve_recipient_via_previous_message(
        self, messaging_service, test_report, test_user, test_operator, db_session
    ):
        messaging_service.send_message(test_report, test_operator, "Richiesta dettagli")

        reply = messaging_service.send_message(test_report, test_user, "Ecco i dettagli richiesti")

        assert reply.sender_id == test_user.id
        assert reply.recipient_id == test_operator.id

    def test_send_message_resolve_recipient_via_status_history(
        self, messaging_service, test_report, test_user, test_operator, db_session
    ):
        history = ReportStatusHistory(
            report_id=test_report.id,
            changed_by_id=test_operator.id,
            previous_status=ReportStatus.PENDING_APPROVAL,
            new_status=ReportStatus.ASSIGNED
        )
        db_session.add(history)
        db_session.commit()
        
        db_session.refresh(test_report)

        reply = messaging_service.send_message(test_report, test_user, "Grazie per la presa in carico")

        assert reply.sender_id == test_user.id
        assert reply.recipient_id == test_operator.id

    def test_resolve_recipient_messages_loop_iterations(
        self, messaging_service, test_report, test_user, test_operator, db_session
    ):
        test_report.status_history = []
        
        assert messaging_service._resolve_recipient(test_report, test_user) is None

        msg1 = Message(
            report_id=test_report.id, sender_id=test_operator.id, 
            recipient_id=test_user.id, body="Messaggio operatore"
        )
        db_session.add(msg1)
        db_session.commit()
        
        assert messaging_service._resolve_recipient(test_report, test_user) == test_operator

        msg2 = Message(
            report_id=test_report.id, sender_id=test_user.id, 
            recipient_id=test_operator.id, body="Risposta utente"
        )
        db_session.add(msg2)
        db_session.commit()
        
        assert messaging_service._resolve_recipient(test_report, test_user) == test_operator


    def test_resolve_recipient_status_history_loop_iterations(
        self, messaging_service, test_report, test_user, admin_user, db_session
    ):
        test_report.status_history = []
        db_session.commit()
        
        assert messaging_service._resolve_recipient(test_report, test_user) is None

        hist1 = ReportStatusHistory(
            report_id=test_report.id, changed_by_id=admin_user.id, 
            previous_status=ReportStatus.PENDING_APPROVAL, new_status=ReportStatus.ASSIGNED
        )
        db_session.add(hist1)
        db_session.commit()
        db_session.refresh(test_report) 
        
        assert messaging_service._resolve_recipient(test_report, test_user) == admin_user

        hist2 = ReportStatusHistory(
            report_id=test_report.id, changed_by_id=test_user.id, 
            previous_status=ReportStatus.ASSIGNED, new_status=ReportStatus.RESOLVED
        )
        db_session.add(hist2)
        db_session.commit()
        db_session.refresh(test_report)
        
        assert messaging_service._resolve_recipient(test_report, test_user) == admin_user

    def test_sender_name_formatting(self, messaging_service, db_session):
        user_full = User(
            username="jdoe", first_name="John", last_name="Doe", 
            email="j@d.com", password_hash="123"
        )
        user_username_only = User(
            username="matrix99", first_name="", last_name="", 
            email="m@m.com", password_hash="123"
        )
        db_session.add_all([user_full, user_username_only])
        db_session.commit()

        assert messaging_service._sender_name(user_full) == "John Doe"
        assert messaging_service._sender_name(user_username_only) == "matrix99"