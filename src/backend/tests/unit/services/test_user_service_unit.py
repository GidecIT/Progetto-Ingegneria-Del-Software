from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from participium.core.exceptions import AuthorizationError, NotFoundError, ValidationError
from participium.models.enums import Role, ReportStatus


class TestUpdateProfile:
    def test_update_profile_ValidationError(self,user_service, mock_user):
        """Username presente, diverso da quello di user ed esiste già in repository"""
        nuovo_username = "luigi_verdi"

        user_service.user_repository.get_by_username.return_value = Mock()

        with pytest.raises(ValidationError) as exc_info:
            user_service.update_profile(mock_user, nuovo_username)
        assert "Username already in use." in str(exc_info.value)
    
    def test_update_profile_not_username1(self,user_service, mock_user):
        """Username non presente, e per SC qualsisi cosa per gli altri casi del IF"""

        user_service.user_repository.get_by_username.return_value = Mock()
        result = user_service.update_profile(mock_user)
        assert result == mock_user
        user_service.session.commit.assert_called_once()

    def test_update_profile_not_username2(self,user_service, mock_user):
        """Username presente, uguale a quello di user e per l'ultima condizione qualsisi cosa
        Inoltre tutti gli altri campi presenti ma senza file name"""
        mock_user.username = "luigi_verdi"
        mock_file = Mock() #True
        mock_file.filename = None #False

        user_service.user_repository.get_by_username.return_value = Mock()
        result = user_service.update_profile(user=mock_user, username=mock_user.username,first_name=mock_user.first_name,last_name=mock_user.last_name,email_notifications_enabled=mock_user.email_notifications_enabled, profile_picture=mock_file)
        assert result == mock_user
        user_service.session.commit.assert_called_once()

    def test_update_profile_not_username3(self,user_service, mock_user):
        """Username presente, diverso da a quello di user e non presente in repository
        Inoltre tutti gli altri campi presenti"""
        nuovo_username = "luigi_verdi"
        mock_file = Mock() #True
        mock_file.filename = "avatar.png" #True

        user_service.user_repository.get_by_username.return_value = None
        result = user_service.update_profile(user=mock_user, username=nuovo_username,first_name=mock_user.first_name,last_name=mock_user.last_name,email_notifications_enabled=mock_user.email_notifications_enabled, profile_picture=mock_file)
        assert result == mock_user
        user_service.session.commit.assert_called_once()
        user_service.storage_service.save.assert_called_once_with(mock_file)

class TestDeleteAccount:

    def test_delete_account_zero_iterations(self, user_service, mock_user):
        user_service.session.scalars.side_effect = [[], [], [], []]
        user_service.notification_repository.list_for_user.return_value = []
        user_service.token_repository.list_for_user.return_value = []

        user_service.delete_account(mock_user)

        user_service.session.delete.assert_not_called()
        user_service.user_repository.delete.assert_called_once_with(mock_user)
        user_service.session.commit.assert_called_once()

    def test_delete_account_one_iteration(self, user_service, mock_user):
        mock_report = Mock(reporter_id=1, is_anonymous=False)
        mock_follower = Mock(user_id=1)
        mock_message = Mock(sender_id=1, recipient_id=99)
        mock_history = Mock(changed_by_id=1)
        mock_notification = Mock()
        mock_token = Mock()

        user_service.session.scalars.side_effect = [
            [mock_report],
            [mock_follower],
            [mock_message],
            [mock_history],
        ]
        user_service.notification_repository.list_for_user.return_value = [
            mock_notification
        ]
        user_service.token_repository.list_for_user.return_value = [mock_token]

        user_service.delete_account(mock_user)

        assert mock_report.reporter_id is None
        assert mock_report.is_anonymous is True
        assert mock_message.sender_id is None
        assert mock_history.changed_by_id is None

        assert user_service.session.delete.call_count == 3
        user_service.session.delete.assert_any_call(mock_follower)
        user_service.session.delete.assert_any_call(mock_notification)
        user_service.session.delete.assert_any_call(mock_token)

        user_service.user_repository.delete.assert_called_once_with(mock_user)
        user_service.session.commit.assert_called_once()

    def test_delete_account_two_iterations(self, user_service, mock_user):
        mock_reports = [Mock(reporter_id=1, is_anonymous=False) for _ in range(2)]
        mock_followers = [Mock(user_id=1) for _ in range(2)]
        mock_messages = [Mock(sender_id=1, recipient_id=10) for _ in range(2)]
        mock_histories = [Mock(changed_by_id=1) for _ in range(2)]
        mock_notifications = [Mock(), Mock()]
        mock_tokens = [Mock(), Mock()]

        user_service.session.scalars.side_effect = [
            mock_reports,
            mock_followers,
            mock_messages,
            mock_histories,
        ]
        user_service.notification_repository.list_for_user.return_value = (
            mock_notifications
        )
        user_service.token_repository.list_for_user.return_value = mock_tokens

        user_service.delete_account(mock_user)

        for report in mock_reports:
            assert report.reporter_id is None
            assert report.is_anonymous is True

        for message in mock_messages:
            assert message.sender_id is None

        for history in mock_histories:
            assert history.changed_by_id is None

        assert user_service.session.delete.call_count == 6
        user_service.session.delete.assert_any_call(mock_followers[0])
        user_service.session.delete.assert_any_call(mock_followers[1])
        user_service.session.delete.assert_any_call(mock_notifications[0])
        user_service.session.delete.assert_any_call(mock_notifications[1])
        user_service.session.delete.assert_any_call(mock_tokens[0])
        user_service.session.delete.assert_any_call(mock_tokens[1])

        user_service.user_repository.delete.assert_called_once_with(mock_user)
        user_service.session.commit.assert_called_once()

    def test_delete_account_messages_branching(self, user_service, mock_user):
        msg_as_sender = Mock(sender_id=1, recipient_id=99)
        msg_as_recipient = Mock(sender_id=11, recipient_id=1)
        msg_as_both = Mock(sender_id=1, recipient_id=1)

        user_service.session.scalars.side_effect = [
            [],
            [],
            [msg_as_sender, msg_as_recipient, msg_as_both],
            [],
        ]
        user_service.notification_repository.list_for_user.return_value = []
        user_service.token_repository.list_for_user.return_value = []

        user_service.delete_account(mock_user)

        assert msg_as_sender.sender_id is None
        assert msg_as_sender.recipient_id == 99

        assert msg_as_recipient.sender_id == 11
        assert msg_as_recipient.recipient_id is None

        assert msg_as_both.sender_id is None
        assert msg_as_both.recipient_id is None

        user_service.session.commit.assert_called_once()
        