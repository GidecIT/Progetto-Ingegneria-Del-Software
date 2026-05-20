from __future__ import annotations
import pytest
from datetime import datetime, timedelta

from sqlalchemy import update

from participium.models.enums import ReportStatus, Role
from participium.models.report import Report, ReportFollower, ReportPhoto, ReportStatusHistory
from participium.models.user import User
from participium.repositories.report_repository import ReportRepository

pytestmark = pytest.mark.integration



# Helpers


def _make_report(user_id: int, category_id: int, **kwargs) -> Report:
    defaults = dict(
        title="Buca",
        description="Buca profonda",
        latitude=45.0,
        longitude=7.0,
        status=ReportStatus.PENDING_APPROVAL,
    )
    defaults.update(kwargs)
    return Report(reporter_id=user_id, category_id=category_id, **defaults)


def _make_user(username: str, email: str) -> User:
    return User(
        username=username, 
        email=email,
        first_name="Nome", 
        last_name="Cognome", 
        password_hash="hash"
    )


def _backdate(session, report: Report, seconds: int = 10) -> None:
    session.execute(
        update(Report)
        .where(Report.id == report.id)
        .values(created_at=datetime.utcnow() - timedelta(seconds=seconds))
    )
    session.commit()


@pytest.fixture
def report_repository(db_session):
    return ReportRepository(db_session)


@pytest.fixture
def other_user(db_session):
    user = _make_user("other", "other@ex.com")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def other_category(db_session):
    from participium.models.category import Category
    cat = Category(name="Viabilità", is_active=True)
    db_session.add(cat)
    db_session.commit()
    return cat



# Test add()

def test_add_report(db_session, report_repository, test_user, test_category):
    added = report_repository.add(_make_report(test_user.id, test_category.id, title="Buca"))
    db_session.commit()

    assert added.id is not None
    assert added.title == "Buca"
    assert added.status == ReportStatus.PENDING_APPROVAL

# Test get_by_id():
# - trovato
# - non trovato

def test_get_by_id_found(db_session, report_repository, test_user, test_category):
    report = _make_report(test_user.id, test_category.id, title="Palo caduto")
    db_session.add(report)
    db_session.commit()

    result = report_repository.get_by_id(report.id)

    assert result is not None
    assert result.id == report.id
    assert result.title == "Palo caduto"
    assert result.category is not None
    assert result.reporter is not None


def test_get_by_id_not_found(report_repository):
    assert report_repository.get_by_id(999) is None


# Test add_photo()

def test_add_photo(db_session, report_repository, test_user, test_category):
    report = _make_report(test_user.id, test_category.id)
    db_session.add(report)
    db_session.commit()

    photo = ReportPhoto(
        report_id=report.id,
        file_path="/uploads/foto.jpg",
        original_filename="foto.jpg",
        content_type="image/jpeg",
    )
    added = report_repository.add_photo(photo)
    db_session.commit()

    assert added.id is not None
    assert added.report_id == report.id
    assert added.file_path == "/uploads/foto.jpg"



# Test add_status_entry()


def test_add_status_entry(db_session, report_repository, test_user, test_category):
    report = _make_report(test_user.id, test_category.id)
    db_session.add(report)
    db_session.commit()

    entry = ReportStatusHistory(
        report_id=report.id,
        previous_status=None,
        new_status=ReportStatus.PENDING_APPROVAL,
        note="Segnalazione inviata.",
        changed_by_id=test_user.id,
    )
    added = report_repository.add_status_entry(entry)
    db_session.commit()

    assert added.id is not None
    assert added.report_id == report.id
    assert added.new_status == ReportStatus.PENDING_APPROVAL



# Test add_follower() 

def test_add_and_get_follower(db_session, report_repository, test_user, test_category):
    report = _make_report(test_user.id, test_category.id)
    db_session.add(report)
    db_session.commit()

    follower = ReportFollower(report_id=report.id, user_id=test_user.id)
    report_repository.add_follower(follower)
    db_session.commit()

    result = report_repository.get_follower(report.id, test_user.id)

    assert result is not None
    assert result.report_id == report.id
    assert result.user_id == test_user.id

# Test get_follower():
def test_get_follower_not_found(db_session, report_repository, test_user, test_category):
    report = _make_report(test_user.id, test_category.id)
    db_session.add(report)
    db_session.commit()

    assert report_repository.get_follower(report.id, test_user.id) is None

# Test remove_follower():
def test_remove_follower(db_session, report_repository, test_user, test_category):
    report = _make_report(test_user.id, test_category.id)
    db_session.add(report)
    db_session.flush() 

    follower = ReportFollower(report_id=report.id, user_id=test_user.id)
    db_session.add(follower)
    db_session.commit()

    report_repository.remove_follower(follower)
    db_session.commit()

    assert report_repository.get_follower(report.id, test_user.id) is None



# Test list_reports() / list_all()
# - lista vuota
# - lista solo public
# - filtro categoria
# - filtro status
# - filtro date_from
# - filtro date_to
# - ordinamento asc
# - ordinamento desc
# - tutti i report

def test_list_reports_empty(report_repository):
    assert report_repository.list_reports() == []


def test_list_reports_public_only_excludes_non_public(db_session, report_repository, test_user, test_category):
    from participium.config.constants import PUBLIC_VISIBLE_STATUSES
    public_status = next(iter(PUBLIC_VISIBLE_STATUSES))

    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Pubblico", status=public_status),
        _make_report(test_user.id, test_category.id, title="In attesa", status=ReportStatus.PENDING_APPROVAL),
    ])
    db_session.commit()

    results = report_repository.list_reports(public_only=True)

    assert len(results) == 1
    assert results[0].title == "Pubblico"


def test_list_reports_filter_by_category(db_session, report_repository, test_user, test_category, other_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Cat A"),
        _make_report(test_user.id, other_category.id, title="Cat B"),
    ])
    db_session.commit()

    results = report_repository.list_reports(category_id=test_category.id)

    assert len(results) == 1
    assert results[0].title == "Cat A"


def test_list_reports_filter_by_status(db_session, report_repository, test_user, test_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="In attesa", status=ReportStatus.PENDING_APPROVAL),
        _make_report(test_user.id, test_category.id, title="Assegnato", status=ReportStatus.ASSIGNED),
    ])
    db_session.commit()

    results = report_repository.list_reports(status=ReportStatus.ASSIGNED)

    assert len(results) == 1
    assert results[0].title == "Assegnato"


def test_list_reports_filter_by_date_from(db_session, report_repository, test_user, test_category):
    old = _make_report(test_user.id, test_category.id, title="Vecchio")
    db_session.add(old)
    db_session.commit()
    _backdate(db_session, old, seconds=10 * 86400)

    recent = _make_report(test_user.id, test_category.id, title="Recente")
    db_session.add(recent)
    db_session.commit()

    cutoff = datetime.now() - timedelta(days=5)
    results = report_repository.list_reports(date_from=cutoff)

    titles = [r.title for r in results]
    assert "Recente" in titles
    assert "Vecchio" not in titles


def test_list_reports_filter_by_date_to(db_session, report_repository, test_user, test_category):
    old = _make_report(test_user.id, test_category.id, title="Vecchio")
    db_session.add(old)
    db_session.commit()
    _backdate(db_session, old, seconds=10 * 86400)

    recent = _make_report(test_user.id, test_category.id, title="Recente")
    db_session.add(recent)
    db_session.commit()

    cutoff = datetime.now() - timedelta(days=5)
    results = report_repository.list_reports(date_to=cutoff)

    titles = [r.title for r in results]
    assert "Vecchio" in titles
    assert "Recente" not in titles


def test_list_reports_sort_asc(db_session, report_repository, test_user, test_category):
    first = _make_report(test_user.id, test_category.id, title="Primo")
    db_session.add(first)
    db_session.commit()
    _backdate(db_session, first)

    second = _make_report(test_user.id, test_category.id, title="Secondo")
    db_session.add(second)
    db_session.commit()

    results = report_repository.list_reports(sort="asc")

    assert results[0].title == "Primo"
    assert results[-1].title == "Secondo"


def test_list_reports_sort_desc(db_session, report_repository, test_user, test_category):
    first = _make_report(test_user.id, test_category.id, title="Primo")
    db_session.add(first)
    db_session.commit()
    _backdate(db_session, first)

    second = _make_report(test_user.id, test_category.id, title="Secondo")
    db_session.add(second)
    db_session.commit()

    results = report_repository.list_reports(sort="desc")

    assert results[0].title == "Secondo"
    assert results[-1].title == "Primo"

def test_list_all_reports(db_session, report_repository, test_user, test_category):

    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Rep1"),
        _make_report(test_user.id, test_category.id, title="Rep2")
    ])
    db_session.commit()

    results = report_repository.list_all()

    assert len(results) == 2
    titles = [r.title for r in results]
    assert "Rep1" in titles
    assert "Rep2" in titles



# Test list_user_reports():
# - lista vuota
# - lista per utente
# - lista per creazione crescente


def test_list_user_reports_empty(report_repository, test_user):
    assert report_repository.list_user_reports(test_user.id) == []


def test_list_user_reports_isolation(db_session, report_repository, test_user, other_user, test_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Mio"),
        _make_report(other_user.id, test_category.id, title="Altro"),
    ])
    db_session.commit()

    results = report_repository.list_user_reports(test_user.id)

    assert len(results) == 1
    assert results[0].title == "Mio"


def test_list_user_reports_ordering(db_session, report_repository, test_user, test_category):
    first = _make_report(test_user.id, test_category.id, title="Primo")
    db_session.add(first)
    db_session.commit()
    _backdate(db_session, first)

    second = _make_report(test_user.id, test_category.id, title="Secondo")
    db_session.add(second)
    db_session.commit()

    results = report_repository.list_user_reports(test_user.id)

    assert results[0].title == "Secondo"
    assert results[1].title == "Primo"


# Test list_pending()
# - solo report PENDING_APPROVAL
# - filtro category_id
# - filtro date_from
# - filtro date_to
# - ordinamento crescente per created_at

def test_list_pending_returns_only_pending(db_session, report_repository, test_user, test_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="In attesa", status=ReportStatus.PENDING_APPROVAL),
        _make_report(test_user.id, test_category.id, title="Assegnato", status=ReportStatus.ASSIGNED),
    ])
    db_session.commit()

    results = report_repository.list_pending()

    assert len(results) == 1
    assert results[0].title == "In attesa"


def test_list_pending_filter_by_category(db_session, report_repository, test_user, test_category, other_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Cat A", status=ReportStatus.PENDING_APPROVAL),
        _make_report(test_user.id, other_category.id, title="Cat B", status=ReportStatus.PENDING_APPROVAL),
    ])
    db_session.commit()

    results = report_repository.list_pending(category_id=test_category.id)

    assert len(results) == 1
    assert results[0].title == "Cat A"


def test_list_pending_filter_by_date_from(db_session, report_repository, test_user, test_category):
    old = _make_report(test_user.id, test_category.id, title="Vecchio Pending", status=ReportStatus.PENDING_APPROVAL)
    db_session.add(old)
    db_session.commit()
    _backdate(db_session, old, seconds=10 * 86400) # Vecchio di 10 giorni

    recent = _make_report(test_user.id, test_category.id, title="Recente Pending", status=ReportStatus.PENDING_APPROVAL)
    db_session.add(recent)
    db_session.commit()

    cutoff = datetime.now() - timedelta(days=5)
    results = report_repository.list_pending(date_from=cutoff)

    titles = [r.title for r in results]
    assert "Recente Pending" in titles
    assert "Vecchio Pending" not in titles


def test_list_pending_filter_by_date_to(db_session, report_repository, test_user, test_category):
    old = _make_report(test_user.id, test_category.id, title="Vecchio Pending", status=ReportStatus.PENDING_APPROVAL)
    db_session.add(old)
    db_session.commit()
    _backdate(db_session, old, seconds=10 * 86400)

    recent = _make_report(test_user.id, test_category.id, title="Recente Pending", status=ReportStatus.PENDING_APPROVAL)
    db_session.add(recent)
    db_session.commit()

    cutoff = datetime.now() - timedelta(days=5)
    results = report_repository.list_pending(date_to=cutoff)

    titles = [r.title for r in results]
    assert "Vecchio Pending" in titles
    assert "Recente Pending" not in titles


def test_list_pending_ordering(db_session, report_repository, test_user, test_category):
    first = _make_report(test_user.id, test_category.id, title="Primo", status=ReportStatus.PENDING_APPROVAL)
    db_session.add(first)
    db_session.commit()
    _backdate(db_session, first)

    second = _make_report(test_user.id, test_category.id, title="Secondo", status=ReportStatus.PENDING_APPROVAL)
    db_session.add(second)
    db_session.commit()

    results = report_repository.list_pending()

    assert results[0].title == "Primo"
    assert results[1].title == "Secondo"



# Test list_for_category():

def test_list_for_category_excludes_pending(db_session, report_repository, test_user, test_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="In attesa", status=ReportStatus.PENDING_APPROVAL),
        _make_report(test_user.id, test_category.id, title="Assegnato", status=ReportStatus.ASSIGNED),
    ])
    db_session.commit()

    results = report_repository.list_for_category(test_category.id)

    assert len(results) == 1
    assert results[0].title == "Assegnato"


def test_list_for_category_filters_by_category(db_session, report_repository, test_user, test_category, other_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Cat A", status=ReportStatus.ASSIGNED),
        _make_report(test_user.id, other_category.id, title="Cat B", status=ReportStatus.ASSIGNED),
    ])
    db_session.commit()

    results = report_repository.list_for_category(test_category.id)

    assert len(results) == 1
    assert results[0].title == "Cat A"


def test_list_for_category_none_returns_all_non_pending(db_session, report_repository, test_user, test_category, other_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Cat A", status=ReportStatus.ASSIGNED),
        _make_report(test_user.id, other_category.id, title="Cat B", status=ReportStatus.IN_PROGRESS),
        _make_report(test_user.id, test_category.id, title="Pending", status=ReportStatus.PENDING_APPROVAL),
    ])
    db_session.commit()

    results = report_repository.list_for_category(None)

    titles = [r.title for r in results]
    assert "Cat A" in titles
    assert "Cat B" in titles
    assert "Pending" not in titles



# Test list_operator_reports():
# - solo propria categoria
# - tutti i report assegnati

def test_list_operator_reports_operator_sees_only_own_category(db_session, report_repository, test_user, test_category, other_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Cat A", status=ReportStatus.ASSIGNED),
        _make_report(test_user.id, other_category.id, title="Cat B", status=ReportStatus.ASSIGNED),
    ])
    db_session.commit()

    results = report_repository.list_operator_reports(Role.OPERATOR, test_category.id)

    assert len(results) == 1
    assert results[0].title == "Cat A"


def test_list_operator_reports_admin_sees_all(db_session, report_repository, test_user, test_category, other_category):
    db_session.add_all([
        _make_report(test_user.id, test_category.id, title="Cat A", status=ReportStatus.ASSIGNED),
        _make_report(test_user.id, other_category.id, title="Cat B", status=ReportStatus.IN_PROGRESS),
    ])
    db_session.commit()

    results = report_repository.list_operator_reports(Role.ADMIN)

    titles = [r.title for r in results]
    assert "Cat A" in titles
    assert "Cat B" in titles



# Test list_followers()_
# - lista vuota
# - lista con follower


def test_list_followers_empty(db_session, report_repository, test_user, test_category):
    report = _make_report(test_user.id, test_category.id)
    db_session.add(report)
    db_session.commit()

    assert report_repository.list_followers(report.id) == []


def test_list_followers_returns_followers(db_session, report_repository, test_user, other_user, test_category):
    report = _make_report(test_user.id, test_category.id)
    db_session.add(report)
    db_session.commit()

    db_session.add_all([
        ReportFollower(report_id=report.id, user_id=test_user.id),
        ReportFollower(report_id=report.id, user_id=other_user.id),
    ])
    db_session.commit()

    results = report_repository.list_followers(report.id)

    assert len(results) == 2
    assert all(f.report_id == report.id for f in results)