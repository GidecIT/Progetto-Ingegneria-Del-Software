import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from participium.models.base import Base
from participium.models.token import EmailVerificationToken
from participium.models.user import User
from participium.models.enums import Role

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

def test_token_persistence_and_user_relationship(db_session):

    user = User(
        username="integration_user",
        first_name="Test",
        last_name="Integration",
        email="integration@test.com",
        password_hash="any_hash",
        role=Role.CITIZEN,
        is_active=True,
        is_email_verified=False,
    )
    db_session.add(user)
    db_session.commit()

    verification_token = EmailVerificationToken(
        user_id=user.id,
        token="unique-integration-token-string-abc",
        expires_at=datetime.utcnow(),
        is_used=False
    )
    db_session.add(verification_token)
    db_session.commit()

    fetched_token = db_session.query(EmailVerificationToken).filter_by(
        token="unique-integration-token-string-abc").first()
    assert fetched_token is not None
    assert fetched_token.user_id == user.id
    assert fetched_token.user.username == "integration_user"

def test_token_unique_constraint(db_session):
    user = User(username="u", first_name="f", last_name="l", email="e@t.com", password_hash="h", role=Role.CITIZEN)
    db_session.add(user)
    db_session.commit()

    t1 = EmailVerificationToken(user_id=user.id, token="duplicate_token", expires_at=datetime.utcnow())
    t2 = EmailVerificationToken(user_id=user.id, token="duplicate_token", expires_at=datetime.utcnow())

    db_session.add(t1)
    db_session.commit()

    db_session.add(t2)
    with pytest.raises(IntegrityError):
        db_session.commit()