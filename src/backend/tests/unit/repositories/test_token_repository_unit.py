from __future__ import annotations
from unittest.mock import Mock

import pytest

from participium.models.token import EmailVerificationToken


class TestTokenRepositoryWriteAndGet:
    def test_add(self, token_repository, mock_session):
        mock_token = Mock(spec=EmailVerificationToken)
        result = token_repository.add(mock_token)
        assert result == mock_token
        mock_session.add.assert_called_once_with(mock_token)

    def test_get_by_token_found(self, token_repository, mock_session):
        mock_token = Mock(spec=EmailVerificationToken)
        mock_session.scalar.return_value = mock_token
        
        result = token_repository.get_by_token("fake-token-abc")
        assert result == mock_token
        mock_session.scalar.assert_called_once()

    def test_get_by_token_not_found(self, token_repository, mock_session):
        mock_session.scalar.return_value = None
        
        result = token_repository.get_by_token("unknown-token")
        assert result is None
        mock_session.scalar.assert_called_once()


class TestTokenRepositoryQueries:
    def test_list_for_user(self, token_repository, mock_session):
        mock_session.scalars.return_value = []

        result = token_repository.list_for_user(user_id=1)
        assert result == []
        mock_session.scalars.assert_called_once()