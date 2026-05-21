from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock

import pytest

from participium.core.exceptions import NotFoundError, ValidationError


class TestListCategories:
    def test_list_categories_active_only(self, category_service, mock_category):
        category_service.category_repository.list_all = Mock(return_value= [mock_category] )
        result = category_service.list_categories(True)
        assert result == [mock_category]
        category_service.category_repository.list_all.assert_called_once_with(active_only=True)
    
    def test_list_categories_not_active_only(self, category_service, mock_category):
        mock_category.category.is_active = False
        category_service.category_repository.list_all = Mock(return_value= [mock_category] )
        result = category_service.list_categories(False)
        assert result == [mock_category]
        category_service.category_repository.list_all.assert_called_once_with(active_only=False)

class TestGetCategory:
    def test_get_category_NotFoundError(self, category_service):
        category_service.category_repository.get_by_id.return_value = None
        with pytest.raises(NotFoundError) as exc_info:
            category_service.get_category(1)
        assert "Category not found." in str(exc_info.value)
    
    def test_get_category_success(self, category_service, mock_category):
        category_service.category_repository.get_by_id.return_value = mock_category
        risultati = category_service.get_category(1)
        assert risultati == mock_category

class TestCreateCategory:
    def test_create_category_not_cleaned_name(self, category_service):
        with pytest.raises(ValidationError) as exc_info:
            category_service.create_category("     ")
        assert "Category name is required." in str(exc_info.value)

    def test_create_category_already_exist(self, category_service, mock_category):
        category_service.category_repository.get_by_name.return_value = mock_category
        with pytest.raises(ValidationError) as exc_info:
            category_service.create_category(mock_category.name)
        assert "Category name already exists." in str(exc_info.value)
    
    def test_create_category_success(self, category_service, mock_category):
        new_cat_name = "cat1"
        category_service.category_repository.get_by_name.return_value = False
        category_service.category_repository.add.return_value = mock_category
        
        result = category_service.create_category(new_cat_name)
        
        category_service.category_repository.add.assert_called_once()
        category_service.session.commit.assert_called_once()
        assert result == mock_category

class TestUpdateCategory:
    class TestUpdateCategory:
        def test_update_category_name_already_exists(self, category_service, mock_category):
            category_service.category_repository.get_by_id.return_value = mock_category
            duplicate_category = Mock(id=2) #altra categoria con stesso nome
            category_service.category_repository.get_by_name.return_value = duplicate_category
            
            with pytest.raises(ValidationError) as exc_info:
                category_service.update_category(mock_category.id, name="Duplicate Name")
            assert "Category name already exists." in str(exc_info.value)

    def test_update_category_success(self, category_service, mock_category):
        category_service.category_repository.get_by_id.return_value = mock_category
        category_service.category_repository.get_by_name.return_value = None 
        new_name = "New Water Name"

        result = category_service.update_category(mock_category.id, name=new_name, is_active=False)
        
        assert result.name == new_name
        assert result.is_active is False
        category_service.session.commit.assert_called_once()

    def test_update_category_only_name(self, category_service, mock_category):
        category_service.category_repository.get_by_id.return_value = mock_category
        category_service.category_repository.get_by_name.return_value = None
        
        original_active_status = mock_category.is_active
        new_name = "Only name"
        
        result = category_service.update_category(mock_category.id, name=new_name)
        
        assert result.name == new_name
        assert result.is_active == original_active_status
        category_service.session.commit.assert_called_once()

    def test_update_category_only_state(self, category_service, mock_category):
        category_service.category_repository.get_by_id.return_value = mock_category
        
        original_name = mock_category.name
        
        result = category_service.update_category(mock_category.id, is_active=False)
        
        assert result.name == original_name
        assert result.is_active is False
        category_service.session.commit.assert_called_once()
        category_service.category_repository.get_by_name.assert_not_called()

        

 


             
