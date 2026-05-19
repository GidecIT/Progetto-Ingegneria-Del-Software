from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from participium.models.user import User
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

class TestListUsers:
    def test_list_users_empty(self, user_service):
        """Verifica che il servizio restituisca una lista vuota se il repository non ha utenti"""
        user_service.user_repository.list_all.return_value = []

        result = user_service.list_users()

        assert result == []
        user_service.user_repository.list_all.assert_called_once()

    def test_list_users_with_elements(self, user_service):
        """Verifica che funzioni tutto correttamente."""
        fake_users = [Mock(id=1, username="user_1"), Mock(id=2, username="user_2")]
        user_service.user_repository.list_all.return_value = fake_users

        result = user_service.list_users()

        assert result == fake_users
        assert len(result) == 2
        user_service.user_repository.list_all.assert_called_once()
        
class TestGetUser:
    def test_get_user_NotFoundError(self, user_service, mock_user):
        """se non viene trovato l'utente: NotFoundError"""
        user_service.user_repository.get_by_id.return_value = None 

        with pytest.raises(NotFoundError) as exc_info:
            user_service.get_user(mock_user.id)
        assert "User not found." in str(exc_info.value)
        user_service.user_repository.get_by_id.assert_called_once_with(mock_user.id)
    
    def test_get_user_correct(self, user_service, mock_user):
        """Restituisce l'utente"""
        user_service.user_repository.get_by_id.return_value = mock_user

        result = user_service.get_user(mock_user.id)
        assert result == mock_user
        user_service.user_repository.get_by_id.assert_called_once_with(mock_user.id)
class TestCreateUser:
    def test_create_user_missing_fields_one_iteration(self, user_service):
        """Caso 1 campo mancante nel ciclo: lancia ValidationError per un solo campo vuoto."""
        payload = {
            "username": "mario_rossi",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email": "", #manca
            "password": "password123",
            "role": "CITIZEN",
        }

        with pytest.raises(ValidationError ) as exc_info:
            user_service.create_user(payload)

        assert "Missing required fields: email" in str(exc_info.value)
        user_service.session.commit.assert_not_called()

    def test_create_user_missing_fields_two_iterations(self, user_service):
        """Caso 2 campi mancanti nel ciclo: lancia ValidationError con elenco dei campi separati d virgola"""
        payload= {
            "username": "",  # manca
            "first_name": "Mario",
            "last_name": "Rossi",
            "email": "",  # Manca
            "password": "password123",
            "role": "CITIZEN",
        }

        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(payload)

        assert "Missing required fields: username, email" in str(exc_info.value)
        user_service.session.commit.assert_not_called()

    def test_create_user_username_already_in_use(self,user_service):
        """Caso 0 campi mancanti nel ciclo. if dell'username = True -> Lancia ValidationError."""
        payload = {
            "username": "mario_rossi",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email": "mario.rossi@example.com",
            "password": "password123",
            "role": "CITIZEN",
        }
        user_service.user_repository.get_by_username.return_value = Mock()

        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(payload)

        assert "Username already in use." in str( exc_info.value)
        user_service.user_repository.get_by_username.assert_called_once_with("mario_rossi")
        user_service.user_repository.get_by_email.assert_not_called()
        user_service.session.commit.assert_not_called()

    def test_create_user_email_already_in_use(self, user_service):
        """Caso 0 campi mancanti. if username = False, if email = True -> Lancia ValidationError."""
        payload = {
            "username": "mario_rossi",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email": "mario.rossi@example.com",
            "password": "password123",
            "role": "CITIZEN",
        }
        user_service.user_repository.get_by_username.return_value = None
        user_service.user_repository.get_by_email.return_value = Mock()

        with pytest.raises(ValidationError)  as exc_info:
            user_service.create_user(payload)

        assert "Email already in use." in str(exc_info.value)
        user_service.user_repository.get_by_username.assert_called_once_with("mario_rossi")
        user_service.user_repository.get_by_email.assert_called_once_with( "mario.rossi@example.com")
        user_service.session.commit.assert_not_called()

    def test_create_user_success_with_category(self, user_service):
        """0 campi mancanti, tutti gli if di controllo a False
        verifica corretto parsing, lo stripping dei testi e l'assegnazione della categoria.
        """
        payload = {
            "username": "  luigi_verdi  ",  #ßtrip
            "first_name": "Luigi",
            "last_name": "Verdi",
            "email": "LUIGI.VERDI@EXAMPLE.COM ",  # strip e minuscolo
            "password": "secret_password",
            "role": "OPERATOR",
            "category_id": 5,
            "is_active": False,
            "email_notifications_enabled": False,
        }

        user_service.user_repository.get_by_username.return_value = None
        user_service.user_repository.get_by_email.return_value = None

        mock_category = Mock(id=5)
        user_service._parse_role = Mock(return_value=Role.OPERATOR)
        user_service._resolve_operator_category = Mock(return_value=mock_category)

        with patch(
            "participium.services.user_service.hash_password"
        ) as mock_hash:
            mock_hash.return_value = "mocked_hash_value"

            result = user_service.create_user(payload)

        assert isinstance(result, User)
        assert result.username == "luigi_verdi"
        assert result.email == "luigi.verdi@example.com"
        assert result.password_hash == "mocked_hash_value"
        assert result.role == Role.OPERATOR
        assert result.category_id == 5
        assert result.is_active is False
        assert result.email_notifications_enabled is False

        user_service._parse_role.assert_called_once_with("OPERATOR")
        user_service._resolve_operator_category.assert_called_once_with(
            Role.OPERATOR, 5
        )
        user_service.user_repository.add.assert_called_once_with(result)
        user_service.session.commit.assert_called_once()

    def test_create_user_success_defaults_no_category(self, user_service):
        """verifica che i parametri opzionali prendano i valori di default
        quando non sono passati nel payload 
        """
        payload = {
            "username": "mario_rossi",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email": "mario.rossi@example.com",
            "password": "password123",
            "role": "CITIZEN",
        }

        user_service.user_repository.get_by_username.return_value = None
        user_service.user_repository.get_by_email.return_value = None

        user_service._parse_role = Mock(return_value=Role.CITIZEN)
        user_service._resolve_operator_category = Mock(return_value=None)

        with patch(
            "participium.services.user_service.hash_password"
        ) as mock_hash:
            mock_hash.return_value = "mocked_hash_value"

            result = user_service.create_user(payload)

        assert result.category_id is None
        assert result.is_active is True
        assert result.email_notifications_enabled is True

        user_service._resolve_operator_category.assert_called_once_with(  Role.CITIZEN, None)
        user_service.user_repository.add.assert_called_once_with(result)
        user_service.session.commit.assert_called_once()

class TestUpdateUser:

    def test_update_user_success(self, user_service, mock_user):
        """Verifica il percorso di successo con l'aggiornamento di più campi."""
        mock_user.first_name = "Old Name"
        mock_user.is_active = True
        user_service.user_repository.get_by_id.return_value = mock_user

        payload = {"first_name": "New Name", "is_active": False}

        updated_user = user_service.update_user(mock_user.id, payload)

        user_service.user_repository.get_by_id.assert_called_once_with(mock_user.id)
        assert updated_user.first_name == "New Name"
        assert updated_user.is_active is False
        user_service.session.commit.assert_called_once()

    def test_update_user_username_conflict(self, user_service, mock_user):
        """Testa il conflitto di username (l'username è già in uso)."""
        mock_user.username = "old_user"
        user_service.user_repository.get_by_id.return_value = mock_user
        user_service.user_repository.get_by_username.return_value = Mock()

        payload = {"username": "new_user"}

        with pytest.raises(ValidationError) as exc_info:
            user_service.update_user(mock_user.id, payload)

        assert "Username already in use." in str(exc_info.value)
        user_service.user_repository.get_by_id.assert_called_once_with(mock_user.id)
        user_service.user_repository.get_by_username.assert_called_once_with("new_user")
        user_service.session.commit.assert_not_called()

    def test_update_user_email_conflict(self, user_service, mock_user):
        """Testa il conflitto di email (l'email è già in uso)."""
        mock_user.email = "old@email.com"
        user_service.user_repository.get_by_id.return_value = mock_user
        user_service.user_repository.get_by_email.return_value = Mock()

        payload = {"email": "new@email.com"}

        with pytest.raises(ValidationError) as exc_info:
            user_service.update_user(mock_user.id, payload)

        assert "Email already in use." in str(exc_info.value)
        user_service.user_repository.get_by_id.assert_called_once_with(mock_user.id)
        user_service.user_repository.get_by_email.assert_called_once_with("new@email.com")
        user_service.session.commit.assert_not_called()

    def test_update_user_role_with_category(self, user_service, mock_user):
        """Verifica aggiornamento ruolo a OPERATOR con category_id valido."""
        mock_user.role = Role.CITIZEN
        mock_user.category_id = None
        user_service.user_repository.get_by_id.return_value = mock_user

        mock_category = Mock(id=5)
        user_service.category_repository.get_by_id.return_value = mock_category

        payload = {"role": Role.OPERATOR, "category_id": 5}

        updated_user = user_service.update_user(mock_user.id, payload)

        assert updated_user.role == Role.OPERATOR
        assert updated_user.category_id == 5
        user_service.session.commit.assert_called_once()

    def test_update_user_empty_payload(self, user_service, mock_user):
        """Payload vuoto: nessuna modifica applicata ma commit eseguito."""
        mock_user.first_name = "Test"
        user_service.user_repository.get_by_id.return_value = mock_user

        payload = {}

        updated_user = user_service.update_user(mock_user.id, payload)

        assert updated_user.first_name == "Test"
        user_service.session.commit.assert_called_once()

    def test_update_user_not_found(self, user_service):
        """Se l'user_id non esiste, lancia NotFoundError."""
        user_service.user_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc_info:
            user_service.update_user(999, {})

        assert "User not found." in str(exc_info.value)
        user_service.user_repository.get_by_id.assert_called_once_with(999)

    def test_update_user_same_username_no_conflict(self, user_service, mock_user):
        """L'invio dello stesso username attuale salta il check di conflitto sul repository."""
        mock_user.username = "same_user"
        user_service.user_repository.get_by_id.return_value = mock_user

        payload = {"username": "same_user"}
        
        user_service.update_user(mock_user.id, payload)

        user_service.user_repository.get_by_username.assert_not_called()
        user_service.session.commit.assert_called_once()

    def test_update_user_role_to_citizen_clears_category(self, user_service, mock_user):
        """Se il ruolo diventa CITIZEN, la category_id viene azzerata automaticamente."""
        mock_user.role = Role.OPERATOR
        mock_user.category_id = 5
        user_service.user_repository.get_by_id.return_value = mock_user

        payload = {"role": Role.CITIZEN}

        updated_user = user_service.update_user(mock_user.id, payload)

        assert updated_user.role == Role.CITIZEN
        assert updated_user.category_id is None
        user_service.session.commit.assert_called_once()

    def test_update_user_email_notifications(self, user_service, mock_user):
        """Verifica l'aggiornamento del flag booleano delle notifiche email."""
        mock_user.email_notifications_enabled = True
        user_service.user_repository.get_by_id.return_value = mock_user

        payload = {"email_notifications_enabled": False}

        updated_user = user_service.update_user(mock_user.id, payload)

        assert updated_user.email_notifications_enabled is False
        user_service.session.commit.assert_called_once()

class TestParseRole:
    def test_parse_ValidationError(self, user_service):
        ruolo_non_valido = "non valido"
        with pytest.raises(ValidationError) as exc_info:
          user_service._parse_role(ruolo_non_valido)

        assert "Invalid user role." in str(exc_info.value)

    def test_parse_valid(self, user_service):
        ruolo_valido = "citizen"
        result = user_service._parse_role(ruolo_valido)
        assert isinstance(result, Role)
        assert result == Role.CITIZEN

class TestResolveOperatorCategory:
    def test_resolve_operator_category_role_not_valid(self, user_service, mock_user):
        categoria_vuota = None

        
        result = user_service._resolve_operator_category(mock_user.role, categoria_vuota)
        assert result == None
    
    def test_resolve_operator_category_id_None(self, user_service, mock_operator):

        categoria_vuota = None

        with pytest.raises(ValidationError) as exc_info:
          user_service._resolve_operator_category(mock_operator.role, categoria_vuota)
        assert "Operator category is required." in str(exc_info.value)
    
    def test_resolve_operator_category_id_empty(self, user_service, mock_operator):

        categoria_vuota = ""

        with pytest.raises(ValidationError) as exc_info:
          user_service._resolve_operator_category(mock_operator.role, categoria_vuota)
        assert "Operator category is required." in str(exc_info.value)

    def test_resolve_operator_category_id_ValidationError(self, user_service, mock_operator):

        categoria_non_valida= "uno"

        with pytest.raises(ValidationError) as exc_info:
          user_service._resolve_operator_category(mock_operator.role, categoria_non_valida)
        assert "A valid active category is required for operators." in str(exc_info.value)

    def test_resolve_operator_category_id_ValidationError_not_in_repo(self, user_service, mock_operator):

        categoria_valida= "3"
        user_service.category_repository.get_by_id.return_value = None

        with pytest.raises(ValidationError) as exc_info:
          user_service._resolve_operator_category(mock_operator.role, categoria_valida)
        assert "A valid active category is required for operators." in str(exc_info.value)

    def test_resolve_operator_category_id_ValidationError_category_inactive(self, user_service, mock_operator):
        mock_inactive_category = Mock()
        mock_inactive_category.is_active = False
        
        user_service.category_repository.get_by_id.return_value = mock_inactive_category
        categoria_valida= "3"

        with pytest.raises(ValidationError) as exc_info:
          user_service._resolve_operator_category(mock_operator.role, categoria_valida)
        assert "A valid active category is required for operators." in str(exc_info.value)

    def test_resolve_operator_category(self, user_service, mock_operator):
        categoria_valida = "3"
        
        mock_category = Mock()
        mock_category.id = 3
        mock_category.is_active = True
        
        user_service.category_repository.get_by_id.return_value = mock_category
        result = user_service._resolve_operator_category(mock_operator.role, categoria_valida)
        
        user_service.category_repository.get_by_id.assert_called_once_with(int(categoria_valida))
        
        assert result == mock_category
        assert result.is_active is True
