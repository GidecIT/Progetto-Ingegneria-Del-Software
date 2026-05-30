import pytest
from participium.services.storage_service import LocalFileStorageService, StorageService
from werkzeug.datastructures import FileStorage
import io

class TestLocalStorageSave:
    
    def test_save_file_writes_to_disk(self, storage_service, media_root, mock_file):
        content = b"test content"
        file = mock_file(filename="test.png", content=content)
        
        relative_name = storage_service.save(file)
        
        file_path = media_root / relative_name
        
        assert file_path.exists()
        assert file_path.read_bytes() == content

    def test_save_uses_secure_filename_and_uuid(self, storage_service, mock_file):
        file = mock_file(filename="../../etc/passwd!@#.jpg")
        
        relative_name = storage_service.save(file)
        
        assert "etc_passwd.jpg" in relative_name
        assert len(relative_name.split("_")[0]) == 32 

    def test_save_default_filename(self, storage_service):
        file = FileStorage(stream=io.BytesIO(b"data"), filename="")
        
        relative_name = storage_service.save(file)
        
        assert "attachment.bin" in relative_name


class TestLocalStorageInitialization:

    def test_media_root_creation(self, tmp_path):
        new_path = tmp_path / "non_existent_folder"
        assert not new_path.exists()
        
        LocalFileStorageService(media_root=new_path)
        
        assert new_path.exists()
        assert new_path.is_dir()

class TestStorageServiceBase:

    def test_storage_service_simulation(self, capsys):

        storage = StorageService()
        file = FileStorage(stream=io.BytesIO(b"data"), filename="test.jpg")
        
        result = storage.save(file)
        
        assert result == "simulated-file"
        
        captured = capsys.readouterr()
        assert "Simulating file storage operation." in captured.out