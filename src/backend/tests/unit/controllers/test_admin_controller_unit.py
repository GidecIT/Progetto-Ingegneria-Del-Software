from __future__ import annotations
from unittest.mock import Mock
import pytest


class TestAdminCategoryManagement:
    @pytest.mark.parametrize("active_only", [True, False])
    def test_list_categories_delegates_to_service(self, admin_controller, mock_category, active_only):
        mock_categories = [mock_category, mock_category]
        admin_controller.category_service.list_categories.return_value = mock_categories

        result = admin_controller.list_categories(active_only=active_only)

        assert result == mock_categories
        admin_controller.category_service.list_categories.assert_called_once_with(active_only=active_only)

    def test_create_category_delegates_to_service(self, admin_controller, mock_category):
        admin_controller.category_service.create_category.return_value = mock_category

        result = admin_controller.create_category("Strade e Marciapiedi")

        assert result == mock_category
        admin_controller.category_service.create_category.assert_called_once_with("Strade e Marciapiedi")

    def test_update_category_delegates_to_service(self, admin_controller, mock_category):
        admin_controller.category_service.update_category.return_value = mock_category
        payload = {"name": "Nuovo Nome", "is_active": False, "extra_field": "ignored"}

        result = admin_controller.update_category(10, payload)

        assert result == mock_category
        admin_controller.category_service.update_category.assert_called_once_with(
            10, name="Nuovo Nome", is_active=False
        )


class TestAdminUserManagement:
    def test_list_users_delegates_to_service(self, admin_controller, mock_user):
        mock_users = [mock_user, mock_user]
        admin_controller.user_service.list_users.return_value = mock_users

        result = admin_controller.list_users()

        assert result == mock_users
        admin_controller.user_service.list_users.assert_called_once()

    def test_create_user_delegates_to_service(self, admin_controller, mock_user):
        admin_controller.user_service.create_user.return_value = mock_user
        payload = {"username": "admin2", "email": "a2@ex.com", "role": "ADMIN"}

        result = admin_controller.create_user(payload)

        assert result == mock_user
        admin_controller.user_service.create_user.assert_called_once_with(payload)

    def test_update_user_delegates_to_service(self, admin_controller, mock_user):
        admin_controller.user_service.update_user.return_value = mock_user
        payload = {"role": "OPERATOR"}

        result = admin_controller.update_user(5, payload)

        assert result == mock_user
        admin_controller.user_service.update_user.assert_called_once_with(5, payload)


class TestAdminStatistics:
    def test_admin_statistics_delegates_to_service(self, admin_controller):
        mock_stats = {"reports": {"pending": 5, "resolved": 10}}
        admin_controller.statistics_service.admin_statistics.return_value = mock_stats

        result = admin_controller.admin_statistics()

        assert result == mock_stats
        admin_controller.statistics_service.admin_statistics.assert_called_once()