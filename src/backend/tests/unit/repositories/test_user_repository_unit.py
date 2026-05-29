from __future__ import annotations
from unittest.mock import Mock

import pytest

from participium.models.user import User


class TestUserRepositoryWriteAndGet:
    def test_add(self, user_repository, mock_session, mock_user):
        result = user_repository.add(mock_user)
        assert result == mock_user
        mock_session.add.assert_called_once_with(mock_user)

    def test_get_by_id_found(self, user_repository, mock_session, mock_user):
        mock_session.scalar.return_value = mock_user
        result = user_repository.get_by_id(1)
        assert result == mock_user
        mock_session.scalar.assert_called_once()

    def test_get_by_id_not_found(self, user_repository, mock_session):
        mock_session.scalar.return_value = None
        result = user_repository.get_by_id(999)
        assert result is None
        mock_session.scalar.assert_called_once()

    def test_get_by_email_found(self, user_repository, mock_session, mock_user):
        mock_session.scalar.return_value = mock_user
        result = user_repository.get_by_email("mario.rossi@example.com")
        assert result == mock_user
        mock_session.scalar.assert_called_once()


class TestUserRepositoryQueries:
    def test_get_by_username_found(self, user_repository, mock_session, mock_user):
        mock_session.scalar.return_value = mock_user
        result = user_repository.get_by_username("test_user")
        assert result == mock_user
        mock_session.scalar.assert_called_once()

    def test_get_by_username_or_email_found(self, user_repository, mock_session, mock_user):
        mock_session.scalar.return_value = mock_user
        result = user_repository.get_by_username_or_email("test_user")
        assert result == mock_user
        mock_session.scalar.assert_called_once()

    def test_list_all(self, user_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []
        mock_session.scalars.return_value = mock_scalars

        result = user_repository.list_all()
        assert result == []
        mock_session.scalars.assert_called_once()
        mock_scalars.unique.assert_called_once()

    def test_delete(self, user_repository, mock_session, mock_user):
        user_repository.delete(mock_user)
        mock_session.delete.assert_called_once_with(mock_user)