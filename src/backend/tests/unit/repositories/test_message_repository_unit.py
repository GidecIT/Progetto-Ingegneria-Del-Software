from __future__ import annotations
from unittest.mock import Mock

import pytest

from participium.models.message import Message


class TestMessageRepositoryWriteAndQuery:
    def test_add(self, message_repository, mock_session):
        mock_message = Mock(spec=Message)
        result = message_repository.add(mock_message)
        assert result == mock_message
        mock_session.add.assert_called_once_with(mock_message)

    def test_list_for_report(self, message_repository, mock_session):
        mock_scalars = Mock()
        mock_scalars.unique.return_value = []  
        mock_session.scalars.return_value = []
        
        result = message_repository.list_for_report(report_id=100)
        assert result == []
        mock_session.scalars.assert_called_once()