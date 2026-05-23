import pytest

from participium.core.exceptions import NotFoundError, ValidationError
from participium.models.category import Category


class TestListCategories:
    
    def test_list_categories(self, category_service, test_category, db_session):
        """Verifica la lista delle categorie, testando anche il filtro active_only."""
        # Creiamo una categoria inattiva a mano per testare il filtro
        inactive_cat = Category(name="Chiusa", is_active=False)
        db_session.add(inactive_cat)
        db_session.commit()

        all_cats = category_service.list_categories(active_only=False)
        names_all = [c.name for c in all_cats]
        assert test_category.name in names_all
        assert "Chiusa" in names_all

        active_cats = category_service.list_categories(active_only=True)
        names_active = [c.name for c in active_cats]
        assert test_category.name in names_active
        assert "Chiusa" not in names_active


class TestGetCategory:

    def test_get_category_success(self, category_service, test_category):
        category = category_service.get_category(test_category.id)
        assert category.id == test_category.id
        assert category.name == test_category.name

    def test_get_category_not_found(self, category_service):
        with pytest.raises(NotFoundError, match="Category not found."):
            category_service.get_category(99999)


class TestCreateCategory:

    def test_create_category_success(self, category_service):
        category = category_service.create_category("  Nuova Categoria  ")
        assert category.id is not None
        assert category.name == "Nuova Categoria"
        assert category.is_active is True

    def test_create_category_empty_name(self, category_service):
        with pytest.raises(ValidationError, match="Category name is required."):
            category_service.create_category("   ")

    def test_create_category_duplicate_name(self, category_service, test_category):
        """Verifica che un nome già esistente blocchi la creazione."""
        with pytest.raises(ValidationError, match="Category name already exists."):
            category_service.create_category(f"  {test_category.name}  ")


class TestUpdateCategory:

    def test_update_category_success(self, category_service, test_category):
        updated = category_service.update_category(
            test_category.id, 
            name="  Nome Aggiornato  ", 
            is_active=False
        )
        assert updated.name == "Nome Aggiornato"
        assert updated.is_active is False

    def test_update_category_partial(self, category_service, test_category):
        original_name = test_category.name
        updated = category_service.update_category(test_category.id, is_active=False)
        assert updated.name == original_name
        assert updated.is_active is False

    def test_update_category_same_name(self, category_service, test_category):
        updated = category_service.update_category(test_category.id, name=test_category.name)
        assert updated.name == test_category.name

    def test_update_category_duplicate_name(self, category_service, test_category, other_category):
        with pytest.raises(ValidationError, match="Category name already exists."):
            category_service.update_category(test_category.id, name=other_category.name)

    def test_update_category_not_found(self, category_service):
        with pytest.raises(NotFoundError, match="Category not found."):
            category_service.update_category(99999, name="Test")