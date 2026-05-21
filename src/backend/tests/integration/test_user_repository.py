import pytest
from participium.models.user import User
from participium.models.enums import Role
from datetime import datetime, timedelta


pytestmark = pytest.mark.integration



def test_add_and_get_user_methods(db_session, user_repository, test_category):

    new_user = User(
        username="mario_op",
        email="op@example.com",
        first_name="Mario",
        last_name="Spinnato",
        password_hash="hash",
        role=Role.OPERATOR,
        category_id=test_category.id
    )


    user_repository.add(new_user)
    db_session.commit()


    by_id = user_repository.get_by_id(new_user.id)
    assert by_id is not None
    assert by_id.username == "mario_op"
    assert by_id.category is not None
    assert by_id.category.name == test_category.name


    by_email = user_repository.get_by_email("op@example.com")
    assert by_email is not None
    assert by_email.id == new_user.id


    by_username = user_repository.get_by_username("mario_op")
    assert by_username is not None
    assert by_username.id == new_user.id


def test_get_methods_not_found(user_repository):
    assert user_repository.get_by_id(9999) is None
    assert user_repository.get_by_email("emailsbagliata@ex.com") is None
    assert user_repository.get_by_username("ghost") is None



# Test get_by_username_or_email()

def test_get_by_username_or_email_match(db_session, user_repository):
    user = User(username="user1", email="user1@ex.com", first_name="A", last_name="A", password_hash="hash_user1")
    db_session.add(user)
    db_session.commit()

    match_username = user_repository.get_by_username_or_email("user1")
    assert match_username is not None
    assert match_username.id == user.id

    match_email = user_repository.get_by_username_or_email("user1@ex.com")
    assert match_email is not None
    assert match_email.id == user.id

    assert user_repository.get_by_username_or_email("wrong_value") is None

def test_list_all_ordering(db_session, user_repository):

    base_time = datetime.utcnow()
    
    u1 = User(username="user1", email="u1@ex.com", first_name="A", last_name="A", password_hash="h")
    u2 = User(username="user2", email="u2@ex.com", first_name="B", last_name="B", password_hash="h")
    
    db_session.add(u1)
    db_session.commit()
    u1.created_at = base_time - timedelta(days=1)
    
    db_session.add(u2)
    db_session.commit()
    u2.created_at = base_time
    
    db_session.commit()

    users = user_repository.list_all()
    assert len(users) >= 2

    index_u1 = next(i for i, u in enumerate(users) if u.id == u1.id)
    index_u2 = next(i for i, u in enumerate(users) if u.id == u2.id)
    assert index_u2 < index_u1



# Test delete()

def test_delete_user(db_session, user_repository):
    user = User(username="user2", email="user2@ex.com", first_name="user", last_name="2", password_hash="hash_user2")
    db_session.add(user)
    db_session.commit()
    assert user_repository.get_by_id(user.id) is not None

    user_repository.delete(user)
    db_session.commit()

    assert user_repository.get_by_id(user.id) is None