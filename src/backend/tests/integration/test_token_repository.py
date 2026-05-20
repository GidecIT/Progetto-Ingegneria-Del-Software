import pytest
from datetime import datetime, timedelta
from participium.models.token import EmailVerificationToken
from participium.repositories.token_repository import TokenRepository
from participium.models.user import User

pytestmark = pytest.mark.integration


# Test add() / get_by_token()
# - aggiunta corretta
# - token trovato tramite stringa
# - token non trovato tramite stringa

def test_add_token(db_session, token_repository, test_user, make_token):
    added = token_repository.add(make_token(test_user.id, token="Nuovo-token"))
    db_session.commit()

    assert added.id is not None
    assert added.token == "Nuovo-token"
    assert added.is_used is False
    assert added.user_id == test_user.id


def test_get_by_token_found(db_session, token_repository, test_user, make_token):
    db_session.add(make_token(test_user.id, token="token2"))
    db_session.commit()

    result = token_repository.get_by_token("token2")

    assert result is not None
    assert result.token == "token2"
    assert result.user_id == test_user.id


def test_get_by_token_not_found(token_repository):
    assert token_repository.get_by_token("inesistente") is None



# Test list_for_user()
# - lista vuota se l'utente non ha token
# - restituisce tutti i token dell'utente
# - token di altri utenti non restituiti


def test_list_for_user_empty(token_repository, test_user, make_token):
    assert token_repository.list_for_user(test_user.id) == []


def test_list_for_user_returns_all_tokens(db_session, token_repository, test_user, make_token):
    db_session.add_all([
        make_token(test_user.id, token="tok-1"),
        make_token(test_user.id, token="tok-2", is_used=True),
    ])
    db_session.commit()

    results = token_repository.list_for_user(test_user.id)

    assert len(results) == 2
    assert all(t.user_id == test_user.id for t in results)


def test_list_for_user_isolation(db_session, token_repository, test_user, other_user, make_token):
    db_session.add_all([
        make_token(test_user.id,  token="token_mio"),
        make_token(other_user.id, token="tokeno_altro"),
    ])
    db_session.commit()

    results = token_repository.list_for_user(test_user.id)

    assert len(results) == 1
    assert results[0].token == "token_mio"