from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock

import pytest


class TestStorageService:
    def test_save_returns_simulated_string(self, storage_service, mock_file):
        
        result = storage_service.save(mock_file)
        assert result == "simulated-file"

class TestLocalFileStorageService:
    def test_save_success(self, local_file_storage_service, mock_file):
        result = local_file_storage_service.save(mock_file)
    
        assert isinstance(result, str)
        assert result.endswith("test.png")
        
        mock_file.save.assert_called_once()

        saved_path = mock_file.save.call_args[0][0]
        assert saved_path.parent == local_file_storage_service.media_root
        assert saved_path.name == result

    def test_save_with_none_filename(self, local_file_storage_service):
        mock_file = Mock(filename=None)
        
        result = local_file_storage_service.save(mock_file)
        
        assert "attachment.bin" in result
        mock_file.save.assert_called_once()

    def test_save_sanitizes_filename(self, local_file_storage_service):
        mock_file = Mock(filename="../../../etc/passwd.txt")
        
        result = local_file_storage_service.save(mock_file)
    
        assert "passwd.txt" in result
        assert ".." not in result
