"""UC-14  Admin edits an existing user's role and status."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, PageHelper, unique_suffix


def _get_first_non_admin_user_id(page: PageHelper) -> str:
    """Return the numeric ID of the first non-admin user in the admin table."""
    page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url("/admin")
    tbody = page.by_id("admin-users-table-body")
    for row in tbody.find_elements(By.TAG_NAME, "tr"):
        row_id = row.get_attribute("id")   # admin-user-row-<id>
        uid = row_id.split("-")[-1]
        role_els = row.find_elements(By.ID, f"admin-user-role-{uid}")
        if role_els:
            role = Select(role_els[0]).first_selected_option.get_attribute("value")
            if role != "admin":
                return uid
    pytest.skip("No non-admin user found in the admin users table")


class TestAdminEditUser:
    """UC-14 – Admin edits an existing user."""

    def test_user_row_has_save_button(self, page: PageHelper):
        """UC-14: Each user row contains a Save button."""
        uid = _get_first_non_admin_user_id(page)
        page.by_id(f"admin-user-save-{uid}")

    def test_change_first_name_and_save(self, page: PageHelper):
        """UC-14: Editing a user's first name and saving shows a success message."""
        uid = _get_first_non_admin_user_id(page)
        fn = page.by_id(f"admin-user-first-name-{uid}")
        fn.clear()
        fn.send_keys(f"Edited{unique_suffix()}")
        page.click(f"admin-user-save-{uid}")
        # success message ID from AdminPage.tsx is 'admin-success'
        msg = page.by_id_visible("admin-success")
        assert msg.text, "Expected a non-empty success message after save"

    def test_toggle_active_status(self, page: PageHelper):
        """UC-14: Toggling Active and saving persists the change on reload."""
        uid = _get_first_non_admin_user_id(page)
        cb = page.by_id(f"admin-user-status-{uid}")
        was_checked = cb.is_selected()
        cb.click()
        page.click(f"admin-user-save-{uid}")
        page.by_id_visible("admin-success")
        page.go("/admin")
        cb_after = page.by_id(f"admin-user-status-{uid}")
        assert cb_after.is_selected() != was_checked, (
            "Active status should have toggled after save and reload"
        )