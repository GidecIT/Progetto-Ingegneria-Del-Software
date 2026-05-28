from __future__ import annotations
import io
from datetime import datetime, timedelta
from unittest.mock import Mock
from flask import Flask

import pytest
from werkzeug.datastructures import FileStorage

from participium.controllers.statistics_controller import StatisticsController
from participium.core.security import hash_password
from participium.models.category import Category
from participium.models.notification import Notification
from participium.models.user import User
from participium.controllers.auth_controller import AuthController
from participium.services.auth_service import AuthService
from participium.controllers.admin_controller import AdminController
from participium.controllers.user_controller import UserController
from participium.core.auth import login_required, roles_required
from participium.config.constants import PUBLIC_VISIBLE_STATUSES
from participium.models.enums import NotificationType, ReportStatus
from participium.models.enums import Role
from participium.models.message import Message
from participium.models.report import Report, ReportFollower, ReportStatusHistory
from participium.models.token import EmailVerificationToken
from participium.services.category_service import CategoryService
from participium.services.messaging_service import MessagingService
from participium.services.notification_service import NotificationService
from participium.services.report_service import ReportService
from participium.services.statistics_service import StatisticsService
from participium.services.storage_service import LocalFileStorageService
from participium.controllers.report_controller import ReportController
from participium.services.user_service import UserService

@pytest.fixture
def statistics_controller(statistics_service):
    return StatisticsController(statistics_service=statistics_service)

@pytest.fixture
def user_controller(user_service, notification_service):
    return UserController(user_service=user_service, notification_service=notification_service)

@pytest.fixture
def report_controller(report_service, messaging_service, notification_service):
    return ReportController(
        report_service=report_service,
        messaging_service=messaging_service,
        notification_service=notification_service,
    )

@pytest.fixture
def admin_controller(category_service, user_service, statistics_service):
    return AdminController(
        category_service=category_service,
        user_service=user_service,
        statistics_service=statistics_service,
    )

@pytest.fixture
def auth_controller(auth_service):
    return AuthController(auth_service=auth_service)

@pytest.fixture
def media_root(tmp_path):
    return tmp_path / "media"

@pytest.fixture
def auth_service(db_session, user_repository, token_repository):
    return AuthService(
        session=db_session,
        user_repository=user_repository,
        token_repository=token_repository,
        email_gateway=Mock(),
    )

@pytest.fixture
def storage_service(media_root):
    return LocalFileStorageService(media_root=media_root)


@pytest.fixture
def mock_file():
    def _maker(filename="test.jpg", content=b"fake data"):
        return FileStorage(stream=io.BytesIO(content), filename=filename)
    return _maker

@pytest.fixture
def notification_service(db_session, notification_repository):
    return NotificationService(
        session=db_session,
        notification_repository=notification_repository,
        email_gateway=Mock(),
    )


@pytest.fixture
def report_service(db_session, report_repository, category_repository, notification_service, storage_service):
    return ReportService(
        session=db_session,
        report_repository=report_repository,
        category_repository=category_repository,
        storage_service=storage_service,
        notification_service=notification_service,
    )


@pytest.fixture
def user_service(db_session, user_repository, category_repository, token_repository, notification_repository, storage_service):
    return UserService(
        session=db_session,
        user_repository=user_repository,
        category_repository=category_repository,
        token_repository=token_repository,
        notification_repository=notification_repository,
        storage_service=storage_service,
    )


@pytest.fixture
def messaging_service(db_session, report_repository, message_repository, notification_service):
    return MessagingService(
        session=db_session,
        report_repository=report_repository,
        message_repository=message_repository,
        notification_service=notification_service
    )


@pytest.fixture
def statistics_service(report_repository):
    return StatisticsService(report_repository=report_repository)


@pytest.fixture
def category_service(db_session, category_repository):
    return CategoryService(session=db_session, category_repository=category_repository)


@pytest.fixture
def populated_db(db_session, test_user, test_category, other_category, make_report, backdate):
    public_status = next(iter(PUBLIC_VISIBLE_STATUSES))

    rep_public_cat_a = make_report(
        reporter_id=test_user.id,
        category_id=test_category.id,
        title="Target Cat A",
        description="Descrizione dettagliata della segnalazione A",
        latitude=41.9028,
        longitude=12.4964,
        status=public_status,
        is_anonymous=False
    )

    rep_public_cat_b = make_report(
        reporter_id=test_user.id,
        category_id=other_category.id,
        title="Escluso Cat B",
        description="Descrizione dettagliata della segnalazione B",
        latitude=45.4642,
        longitude=9.1900,
        status=public_status,
        is_anonymous=True
    )

    rep_private = make_report(
        reporter_id=test_user.id,
        category_id=test_category.id,
        title="Privato Approvazione",
        description="Segnalazione non ancora approvata dal moderatore",
        latitude=40.8518,
        longitude=14.2681,
        status=ReportStatus.PENDING_APPROVAL
    )

    db_session.add_all([rep_public_cat_a, rep_public_cat_b, rep_private])
    db_session.commit()

    backdate(db_session, rep_public_cat_b.__class__, rep_public_cat_b.id, days=5)

    return {
        "report_pubblico_a": rep_public_cat_a,
        "report_pubblico_b_vecchio": rep_public_cat_b,
        "report_privato": rep_private,
    }


@pytest.fixture
def user_with_relations(db_session, test_user, test_category, make_report, make_notification):
    report = make_report(reporter_id=test_user.id, category_id=test_category.id)
    db_session.add(report)
    db_session.commit()

    follower = ReportFollower(report_id=report.id, user_id=test_user.id)
    message = Message(
        report_id=report.id,
        sender_id=test_user.id,
        recipient_id=test_user.id,
        body="Questo è un messaggio di test tra utenti dell'integrazione."
    )
    history = ReportStatusHistory(
        report_id=report.id,
        changed_by_id=test_user.id,
        previous_status=ReportStatus.ASSIGNED,
        new_status=ReportStatus.RESOLVED
    )
    notification = make_notification(user_id=test_user.id)
    token = EmailVerificationToken(
        user_id=test_user.id,
        token="token-da-eliminare",
        expires_at=datetime.now() + timedelta(days=1)
    )

    db_session.add_all([follower, message, history, notification, token])
    db_session.commit()

    return {
        "user": test_user,
        "report": report,
        "message": message,
        "history": history,
        "notification": notification,
        "token": token
    }

@pytest.fixture
def make_historical_report(db_session, make_report):
    def _make(user_id, category_id, created_at, is_public=True, status=None):
        if status is None:
            status = next(iter(PUBLIC_VISIBLE_STATUSES)) if is_public else ReportStatus.PENDING_APPROVAL
        report = make_report(reporter_id=user_id, category_id=category_id, status=status)
        report.created_at = created_at
        db_session.add(report)
        db_session.commit()
        return report
    return _make


@pytest.fixture
def store_notification(db_session, make_notification):
    def _store(user_id: int, **kwargs):
        notification = make_notification(user_id=user_id, **kwargs)
        db_session.add(notification)
        db_session.commit()
        return notification
    return _store


@pytest.fixture
def test_app():
    """Configura l'applicazione fittizia Flask per i test d'integrazione dei middleware."""
    app = Flask("test_auth_middleware")
    app.config["SECRET_KEY"] = "secret_key_test"
    app.config["PROPAGATE_EXCEPTIONS"] = True

    @app.route("/login", endpoint="web.login")
    def mock_login():
        return "login_page"

    @app.route("/web/dashboard")
    @login_required
    def web_dashboard():
        return "web_success"

    @app.route("/api/v1/data")
    @login_required
    def api_data():
        return "api_success"

    @app.route("/api/admin")
    @roles_required(Role.ADMIN)
    def admin_route():
        return "admin_success"

    return app

@pytest.fixture
def test_user(db_session):
    user = User(
        username="tester",
        email="test@ex.com",
        first_name="Mario",
        last_name="Rossi",
        password_hash=hash_password("password_di_test"),
        role=Role.CITIZEN,
        is_active=True,
        is_email_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_category(db_session):
    category = Category(name="Verde Pubblico", is_active=True)
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def other_category(db_session):
    category = Category(name="Illuminazione", is_active=True)
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def make_report(db_session):
    from participium.models.report import Report

    def _make(reporter_id, category_id, **kwargs):
        defaults = {
            "title": "Segnalazione di Test",
            "description": "Descrizione di test",
            "latitude": 41.9028,
            "longitude": 12.4964,
            "status": ReportStatus.PENDING_APPROVAL,
            "is_anonymous": False,
        }
        defaults.update(kwargs)
        report = Report(reporter_id=reporter_id, category_id=category_id, **defaults)
        db_session.add(report)
        db_session.flush()
        return report

    return _make


@pytest.fixture
def make_notification(db_session):
    def _make(user_id, **kwargs):
        defaults = {
            "title": "Notifica di Test",
            "body": "Corpo della notifica",
            "type": NotificationType.MESSAGE,
            "is_read": False,
        }
        defaults.update(kwargs)
        notification = Notification(user_id=user_id, **defaults)
        db_session.add(notification)
        db_session.flush()
        return notification

    return _make

@pytest.fixture
def test_operator(db_session, test_category):
    user = User(
        username="operator_test",
        email="operator@ex.com",
        first_name="Franco",
        last_name="Franchi",
        password_hash=hash_password("password_di_test"),
        role=Role.OPERATOR,
        category_id=test_category.id, 
        is_active=True,
        is_email_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def operator_controller(report_service, notification_service):
    from participium.controllers.operator_controller import OperatorController
    return OperatorController(report_service=report_service, notification_service=notification_service)