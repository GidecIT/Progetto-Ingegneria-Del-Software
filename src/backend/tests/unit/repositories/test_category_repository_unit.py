from __future__ import annotations
from unittest.mock import Mock

import pytest

from participium.models.category import Category


class TestCategoryRepositoryWriteAndGet:
    def test_add(self, category_repository, mock_session, mock_category):
        result = category_repository.add(mock_category)
        assert result == mock_category
        mock_session.add.assert_called_once_with(mock_category)

    def test_get_by_id_found(self, category_repository, mock_session, mock_category):
        mock_session.get.return_value = mock_category
        result = category_repository.get_by_id(1)
        assert result == mock_category
        mock_session.get.assert_called_once_with(Category, 1)

    def test_get_by_id_not_found(self, category_repository, mock_session):
        mock_session.get.return_value = None
        result = category_repository.get_by_id(999)
        assert result is None
        mock_session.get.assert_called_once_with(Category, 999)

    def test_get_by_name_found(self, category_repository, mock_session, mock_category):
        mock_session.scalar.return_value = mock_category
        result = category_repository.get_by_name("Water")
        assert result == mock_category
        mock_session.scalar.assert_called_once()

    def test_get_by_name_not_found(self, category_repository, mock_session):
        mock_session.scalar.return_value = None
        result = category_repository.get_by_name("Unknown")
        assert result is None
        mock_session.scalar.assert_called_once()


class TestCategoryRepositoryListBranches:
    def test_list_all_branch_active_only_false(self, category_repository, mock_session):
        mock_session.scalars.return_value = []
        result = category_repository.list_all(active_only=False)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_all_branch_active_only_true(self, category_repository, mock_session):
        mock_session.scalars.return_value = []
        result = category_repository.list_all(active_only=True)
        assert result == []
        mock_session.scalars.assert_called_once()