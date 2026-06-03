from __future__ import annotations
import pytest

from participium.models.category import Category
from participium.models.user import User
from participium.models.enums import Role


class TestAdminControllerCategoryIntegration:
    def test_list_categories_integration(self, admin_controller, test_category, db_session):
        inactive_cat = Category(name="Disattivata", is_active=False)
        db_session.add(inactive_cat)
        db_session.commit()

        all_cats = admin_controller.list_categories(active_only=False)
        names_all = [c.name for c in all_cats]
        assert test_category.name in names_all
        assert "Disattivata" in names_all

        active_cats = admin_controller.list_categories(active_only=True)
        names_active = [c.name for c in active_cats]
        assert test_category.name in names_active
        assert "Disattivata" not in names_active

    def test_create_category_integration(self, admin_controller, db_session):
        category = admin_controller.create_category("Strade e Marciapiedi")
        
        persisted = db_session.query(Category).get(category.id)
        assert persisted is not None
        assert persisted.name == "Strade e Marciapiedi"
        assert persisted.is_active is True

    def test_update_category_integration(self, admin_controller, test_category, db_session):
        payload = {"name": "Illuminazione Nuova", "is_active": False}
        
        updated = admin_controller.update_category(test_category.id, payload)
        
        db_session.refresh(test_category)
        assert updated.name == "Illuminazione Nuova"
        assert updated.is_active is False


class TestAdminControllerUserIntegration:
    def test_list_users_integration(self, admin_controller, test_user):
        users = admin_controller.list_users()
        user_ids = [u.id for u in users]
        assert test_user.id in user_ids

    def test_create_user_integration(self, admin_controller, db_session):
        payload = {
            "username": "admin_created_user",
            "email": "admin_created@example.com",
            "first_name": "Luigi",
            "last_name": "Bianchi",
            "role": Role.CITIZEN,
            "password": "password_sicura_123"
        }

        created_user = admin_controller.create_user(payload)

        persisted = db_session.query(User).get(created_user.id)
        assert persisted is not None
        assert persisted.username == "admin_created_user"

    def test_update_user_to_operator_with_category_integration(self, admin_controller, test_user, test_category, db_session):
        payload = {
            "is_active": False, 
            "role": Role.OPERATOR, 
            "category_id": test_category.id
        }

        updated_user = admin_controller.update_user(test_user.id, payload)

        db_session.refresh(test_user)
        assert updated_user.is_active is False
        assert updated_user.role == Role.OPERATOR
        assert updated_user.category_id == test_category.id


class TestAdminControllerStatisticsIntegration:
    def test_admin_statistics_integration(self, admin_controller, populated_db):
        stats = admin_controller.admin_statistics()
        
        assert isinstance(stats, dict)
        assert "global" in stats or any(isinstance(v, dict) for v in stats.values())