"""
UC-13  Admin creates a new user account via the admin panel.
UC-14  Admin edits an existing user's role / status.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, PageHelper, unique_suffix


class TestAdminCreateUser:
    """UC-13 – Admin creates a new user."""

    def test_uc13_admin_page_renders(self, page: PageHelper):
        """UC-13: Admin page is accessible and shows the new-user form."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-page")
        page.by_id("admin-new-user-form")

    def test_uc13_create_operator_user(self, page: PageHelper):
        """UC-13: Filling the new-user form with operator role and submitting
        shows a success message and the user appears in the users table."""
        sfx = unique_suffix()
        email = f"op_{sfx}@test.local"

        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")

        page.fill("admin-new-user-username", f"op_{sfx}")
        page.fill("admin-new-user-first-name", "Op")
        page.fill("admin-new-user-last-name", "Test")
        page.fill("admin-new-user-email", email)
        page.fill("admin-new-user-password", "TestPass123!")

        # set role to operator
        page.select_by_value("admin-new-user-role", "operator")

        page.click("admin-new-user-submit")

        success = page.by_id_visible("admin-status-message")
        assert success.text, "Expected a non-empty admin status message"

        # user should appear in the table
        users_table = page.by_id("admin-users-table-body")
        email_inputs = users_table.find_elements(
            By.XPATH, f".//input[@type='email'][@value='{email}']"
        )
        assert email_inputs, f"Created user with email {email} not found in users table"

    def test_uc13_create_citizen_user(self, page: PageHelper):
        """UC-13: Admin can also create a citizen-role account."""
        sfx = unique_suffix()
        email = f"cit_{sfx}@test.local"

        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")

        page.fill("admin-new-user-username", f"cit_{sfx}")
        page.fill("admin-new-user-first-name", "Cit")
        page.fill("admin-new-user-last-name", "Test")
        page.fill("admin-new-user-email", email)
        page.fill("admin-new-user-password", "TestPass123!")
        page.select_by_value("admin-new-user-role", "citizen")
        page.click("admin-new-user-submit")

        page.by_id_visible("admin-status-message")

    def test_uc13_admin_not_accessible_as_citizen(self, page: PageHelper):
        """UC-13: Citizen role cannot access the admin page."""
        from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/admin")
        assert "/admin" not in page.driver.current_url, (
            "Citizen should be redirected away from the admin page"
        )


class TestAdminEditUser:
    """UC-14 – Admin edits an existing user."""

    def _get_first_non_admin_user_id(self, page: PageHelper) -> str:
        """Return the numeric portion of the first user row ID whose role is
        not 'admin', so we don't accidentally demote our own session."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        tbody = page.by_id("admin-users-table-body")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            row_id = row.get_attribute("id")  # admin-user-row-<id>
            numeric_id = row_id.split("-")[-1]
            role_sel_id = f"admin-user-role-{numeric_id}"
            role_inputs = row.find_elements(By.ID, role_sel_id)
            if role_inputs:
                current_role = Select(role_inputs[0]).first_selected_option.get_attribute("value")
                if current_role != "admin":
                    return numeric_id
        pytest.skip("No non-admin user found in the admin users table")

    def test_uc14_user_row_has_save_button(self, page: PageHelper):
        """UC-14: Each user row contains a Save button."""
        uid = self._get_first_non_admin_user_id(page)
        page.by_id(f"admin-user-save-{uid}")

    def test_uc14_change_user_first_name_and_save(self, page: PageHelper):
        """UC-14: Editing a user's first name and clicking Save shows a
        status message without errors."""
        uid = self._get_first_non_admin_user_id(page)

        fn_input = page.by_id(f"admin-user-first-name-{uid}")
        fn_input.clear()
        fn_input.send_keys(f"Edited{unique_suffix()}")

        page.click(f"admin-user-save-{uid}")

        msg = page.by_id_visible("admin-status-message")
        assert msg.text, "Expected a non-empty admin status message after save"

    def test_uc14_toggle_user_active_status(self, page: PageHelper):
        """UC-14: Toggling the Active checkbox and saving updates the flag."""
        uid = self._get_first_non_admin_user_id(page)

        active_checkbox = page.by_id(f"admin-user-status-{uid}")
        was_checked = active_checkbox.is_selected()
        active_checkbox.click()

        page.click(f"admin-user-save-{uid}")
        page.by_id_visible("admin-status-message")

        # Reload to verify persistence
        page.go("/admin")
        active_checkbox_after = page.by_id(f"admin-user-status-{uid}")
        assert active_checkbox_after.is_selected() != was_checked, (
            "Active status should have toggled after save + reload"
        )
