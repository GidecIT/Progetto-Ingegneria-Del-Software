from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock

import pytest

from participium.models.enums import ReportStatus, Role
from participium.models.report import ReportPhoto, ReportFollower, ReportStatusHistory


class TestReportRepositoryAdders:
    def test_add(self, report_repository, mock_session, mock_report):
        result = report_repository.add(mock_report)
        assert result == mock_report
        mock_session.add.assert_called_once_with(mock_report)

    def test_add_photo(self, report_repository, mock_session):
        photo = Mock(spec=ReportPhoto)
        result = report_repository.add_photo(photo)
        assert result == photo
        mock_session.add.assert_called_once_with(photo)

    def test_add_status_entry(self, report_repository, mock_session):
        entry = Mock(spec=ReportStatusHistory)
        result = report_repository.add_status_entry(entry)
        assert result == entry
        mock_session.add.assert_called_once_with(entry)

    def test_add_follower(self, report_repository, mock_session):
        follower = Mock(spec=ReportFollower)
        result = report_repository.add_follower(follower)
        assert result == follower
        mock_session.add.assert_called_once_with(follower)


class TestReportRepositoryGettersAndRemovers:
    def test_get_follower(self, report_repository, mock_session):
        mock_follower = Mock(spec=ReportFollower)
        mock_session.scalar.return_value = mock_follower

        result = report_repository.get_follower(100, 1)
        assert result == mock_follower
        mock_session.scalar.assert_called_once()

    def test_remove_follower(self, report_repository, mock_session):
        follower = Mock(spec=ReportFollower)
        report_repository.remove_follower(follower)
        mock_session.delete.assert_called_once_with(follower)

    def test_get_by_id(self, report_repository, mock_session, mock_report):
        mock_session.scalar.return_value = mock_report
        result = report_repository.get_by_id(100)
        assert result == mock_report
        mock_session.scalar.assert_called_once()


class TestReportRepositoryListReportsBranches:
    def test_list_reports_all_branches_false(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_reports(
            public_only=False,
            category_id=None,
            status=None,
            date_from=None,
            date_to=None
        )
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_reports_branch_category_id_true(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_reports(category_id=5)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_reports_branch_status_true(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_reports(status=ReportStatus.ASSIGNED)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_reports_branch_date_from_true(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_reports(date_from=datetime(2026, 1, 1))
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_reports_branch_date_to_true(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_reports(date_to=datetime(2026, 1, 10))
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_reports_branch_public_only_true(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_reports(public_only=True, sort="asc")
        assert result == []
        mock_session.scalars.assert_called_once()


class TestReportRepositoryQueriesAndPendingBranches:
    def test_list_user_reports(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_user_reports(user_id=1)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_pending_all_branches_false(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_pending(category_id=None, date_from=None, date_to=None)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_pending_branch_category_id_true(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_pending(category_id=5)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_pending_branch_date_from_true(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_pending(date_from=datetime(2026, 1, 1))
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_pending_branch_date_to_true(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_pending(date_to=datetime(2026, 1, 10))
        assert result == []
        mock_session.scalars.assert_called_once()


class TestReportRepositoryOperatorAndFollowers:
    def test_list_for_category_with_none(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_for_category(category_id=None)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_for_category_with_id(self, report_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = report_repository.list_for_category(category_id=5)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_operator_reports_as_operator(self, report_repository):
        report_repository.list_for_category = Mock(return_value=[])
        result = report_repository.list_operator_reports(role=Role.OPERATOR, category_id=5)
        assert result == []
        report_repository.list_for_category.assert_called_once_with(5)

    def test_list_operator_reports_as_admin(self, report_repository):
        report_repository.list_for_category = Mock(return_value=[])
        result = report_repository.list_operator_reports(role=Role.ADMIN, category_id=5)
        assert result == []
        report_repository.list_for_category.assert_called_once_with(None)

    def test_list_followers(self, report_repository, mock_session):
        mock_session.scalars.return_value = []
        result = report_repository.list_followers(report_id=100)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_all(self, report_repository):
        report_repository.list_reports = Mock(return_value=[])
        result = report_repository.list_all()
        assert result == []
        report_repository.list_reports.assert_called_once_with(public_only=False)