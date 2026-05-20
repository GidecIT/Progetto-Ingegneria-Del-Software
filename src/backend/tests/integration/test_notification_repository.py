import pytest
from participium.models.notification import Notification
from participium.models.enums import NotificationType
from participium.models.user import User
from datetime import datetime, timedelta

pytestmark = pytest.mark.integration

def _make_notification(user_id: int, **kwargs) -> Notification:
    defaults = dict(
        type=NotificationType.SYSTEM,
        title="Titolo",
        body="Body",
        is_read=False
    )
    defaults.update(kwargs)
    return Notification(user_id=user_id, **defaults)


# Test add()

def test_add_notification_persists_successfully(db_session, notification_repository, test_user):
    notification = _make_notification(user_id=test_user.id)

    added = notification_repository.add(notification)
    db_session.commit()

    assert added.id is not None


def test_add_notification_sets_correct_fields(db_session, notification_repository, test_user):
    notification = _make_notification(
        user_id=test_user.id,
        type=NotificationType.MESSAGE,
        title="Nuovo",
        body="Body1",
        is_read=True
    )

    added = notification_repository.add(notification)
    db_session.commit()

    assert added.user_id == test_user.id
    assert added.type == NotificationType.MESSAGE
    assert added.title == "Nuovo"
    assert added.body == "Body1"
    assert added.is_read is True


# Test get_by_id():
# - trovata
# - non trovata

def test_get_by_id_returns_correct_notification(db_session, notification_repository, test_user):
    notification = _make_notification(user_id=test_user.id, title="Notifica")
    db_session.add(notification)
    db_session.commit()
    
    result = notification_repository.get_by_id(notification.id)

    assert result is not None
    assert result.id == notification.id
    assert result.title == "Notifica"


def test_get_by_id_returns_none_if_not_found(notification_repository):
    result = notification_repository.get_by_id(1000) 
    
    assert result is None


# Test list_for_user():
# - lista corretta
# - lista in oridne di creazione desc
# - lista vuota

def test_list_for_user_returns_only_target_user_notifications(db_session, notification_repository, test_user):
    user_b = User(
        username="user_b", first_name="Mario", last_name="Reale",
        email="mr@example.com", password_hash="hash"
    )
    db_session.add(user_b)
    db_session.commit()

    notification_target = _make_notification(user_id=test_user.id, title="a")
    notification_other = _make_notification(user_id=user_b.id, title="b")
    
    db_session.add_all([notification_target, notification_other])
    db_session.commit()

    results = notification_repository.list_for_user(test_user.id)

    assert len(results) == 1
    assert results[0].user_id == test_user.id
    assert results[0].title == "a"


def test_list_for_user_orders_descending_by_creation(db_session, notification_repository, test_user):
    now = datetime.now()
    notification_old = _make_notification(
        user_id=test_user.id, 
        title="Vecchia", 
        created_at=now - timedelta(days=1)
    )
    
    notification_new = _make_notification(
        user_id=test_user.id, 
        title="Nuova", 
        created_at=now
    )
    
    db_session.add_all([notification_old, notification_new])
    db_session.commit()

    results = notification_repository.list_for_user(test_user.id)

    assert len(results) == 2
    assert results[0].title == "Nuova"
    assert results[1].title == "Vecchia"


def test_list_for_user_returns_empty_list_if_none(notification_repository):
    results = notification_repository.list_for_user(99999) 
    assert results == []


# Test list_unread_message_notifications()

def test_list_unread_message_notifications_filters_type_and_read_status(db_session, notification_repository, test_user):
    notification_read = _make_notification(user_id=test_user.id, type=NotificationType.MESSAGE, is_read=True)
    notification_sys = _make_notification(user_id=test_user.id, type=NotificationType.SYSTEM, is_read=False)
    notification_valid = _make_notification(user_id=test_user.id, type=NotificationType.MESSAGE, is_read=False, title="Notifica valida")
    
    db_session.add_all([notification_read, notification_sys, notification_valid])
    db_session.commit()

    results = notification_repository.list_unread_message_notifications(test_user.id)

    assert len(results) == 1
    assert results[0].title == "Notifica valida"


def test_list_unread_message_notifications_filters_by_report_id(db_session, notification_repository, test_user, test_report):
    notification_target = _make_notification(
        user_id=test_user.id, type=NotificationType.MESSAGE, is_read=False, report_id=test_report.id
    )
    notification_other_report = _make_notification(
        user_id=test_user.id, type=NotificationType.MESSAGE, is_read=False, report_id=1000
    )
    
    db_session.add_all([notification_target, notification_other_report])
    db_session.commit()

    results = notification_repository.list_unread_message_notifications(test_user.id, report_id=test_report.id)

    assert len(results) == 1
    assert results[0].report_id == test_report.id



# delete_for_user()


def test_delete_for_user_removes_all_target_user_notifications(db_session, notification_repository, test_user):
    n1 = _make_notification(user_id=test_user.id)
    n2 = _make_notification(user_id=test_user.id)

    db_session.add_all([n1, n2])
    db_session.commit()

    notification_repository.delete_for_user(test_user.id)
    db_session.commit()

    assert len(notification_repository.list_for_user(test_user.id)) == 0


def test_delete_for_user_does_not_affect_other_users(db_session, notification_repository, test_user):
    user_b = User(
        username="luig", first_name="Luigi", last_name="Falsone",
        email="lf@example.com", password_hash="hash"
    )
    db_session.add(user_b)
    db_session.commit()

    notification_target = _make_notification(user_id=test_user.id)
    notification_keep = _make_notification(user_id=user_b.id)

    db_session.add_all([notification_target, notification_keep])
    db_session.commit()

    notification_repository.delete_for_user(test_user.id)
    db_session.commit()

    assert len(notification_repository.list_for_user(test_user.id)) == 0
    assert len(notification_repository.list_for_user(user_b.id)) == 1