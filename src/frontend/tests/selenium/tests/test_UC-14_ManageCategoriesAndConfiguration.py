"""UC-14  Manage categories and configuration.

An administrator creates, edits, and toggles the active state of
report categories. Invalid configuration changes are not applied.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix


def _wait_for_category_rows(page: PageHelper) -> None:
    """Wait until at least one admin-category-row-* is present in the DOM."""
    page.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[starts-with(@id,'admin-category-row-')]")
        ),
        message="No admin-category-row-* found; categories may not have loaded",
    )


def _get_first_non_admin_user_id(page: PageHelper) -> str:
    """Return the numeric ID of the first non-admin user in the admin table."""
    page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url("/admin")
    # Wait for the users table to be populated from the API before iterating,
    # otherwise the rows may not be present yet and the lookup wrongly concludes
    # there is no non-admin user.
    page.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[starts-with(@id,'admin-user-row-')]")
        ),
        message="No admin-user-row-* found; admin users may not have loaded",
    )
    tbody = page.by_id("admin-users-table-body")
    for row in tbody.find_elements(By.TAG_NAME, "tr"):
        row_id = row.get_attribute("id")
        uid = row_id.split("-")[-1]
        role_els = row.find_elements(By.ID, f"admin-user-role-{uid}")
        if role_els:
            role = Select(role_els[0]).first_selected_option.get_attribute("value")
            if role != "admin":
                return uid
    pytest.skip("No non-admin user found in the admin users table")


class TestManageCategoriesAndConfiguration:
    """UC-14 – Administrator manages categories and user configuration."""

    def test_categories_table_rendered(self, page: PageHelper):
        """UC-14: The admin page shows the categories table."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        assert page.by_id("admin-categories-section").is_displayed()
        assert page.by_id("admin-categories-table").is_displayed()

    def test_create_category_form_present(self, page: PageHelper):
        """UC-14: The create-category form is visible on the admin page."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        assert page.by_id("admin-category-form").is_displayed()
        assert page.by_id("admin-new-category-name").is_displayed()
        assert page.by_id("admin-new-category-submit").is_displayed()

    def test_create_new_category_shows_success_and_appears_in_table(self, page: PageHelper):
        """UC-14: Creating a new category shows a success message and the
        category appears in the categories table."""
        cat_name = f"Cat{unique_suffix()}"
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.fill("admin-new-category-name", cat_name)
        page.click("admin-new-category-submit")

        msg = page.by_id_visible("admin-success")
        assert msg.text.strip(), "Expected a non-empty success message"

        tbody = page.by_id("admin-categories-table-body")
        name_inputs = tbody.find_elements(By.XPATH, f".//input[@value='{cat_name}']")
        assert name_inputs, f"Newly created category '{cat_name}' not found in table"

    def test_edit_category_name_saves_successfully(self, page: PageHelper):
        """UC-14: Editing a category name and saving shows a success message."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        _wait_for_category_rows(page)
        tbody = page.by_id("admin-categories-table-body")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        assert rows, "Expected at least one category row"
        cat_id = rows[0].get_attribute("id").split("-")[-1]
        name_input = page.by_id(f"admin-category-name-{cat_id}")
        name_input.clear()
        name_input.send_keys(f"Edited{unique_suffix()}")
        page.click(f"admin-category-save-{cat_id}")
        msg = page.by_id_visible("admin-success")
        assert msg.text.strip(), "Expected a non-empty success message after edit"

    def test_toggle_category_active_flag_saves(self, page: PageHelper):
        """UC-14: Toggling the Active flag on a category and saving shows
        a success message."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        _wait_for_category_rows(page)
        tbody = page.by_id("admin-categories-table-body")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        assert rows, "Expected at least one category row"
        cat_id = rows[0].get_attribute("id").split("-")[-1]
        page.by_id(f"admin-category-active-{cat_id}").click()
        page.click(f"admin-category-save-{cat_id}")
        msg = page.by_id_visible("admin-success")
        assert msg.text.strip()

    def test_admin_creates_operator_user(self, page: PageHelper):
        """UC-14: Admin creates a new operator account via the user form."""
        sfx = unique_suffix()
        email = f"operator_{sfx}@test.local"
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.fill("admin-new-user-username", f"operator_{sfx}")
        page.fill("admin-new-user-first-name", "Op")
        page.fill("admin-new-user-last-name", "Test")
        page.fill("admin-new-user-email", email)
        page.fill("admin-new-user-password", "TestPass123!")
        page.select_by_value("admin-new-user-role", "operator")
        page.click("admin-new-user-submit")
        msg = page.by_id_visible("admin-success")
        assert msg.text.strip()
        tbody = page.by_id("admin-users-table-body")
        page.wait.until(
            lambda d: any(
                el.get_property("value") == email
                for el in tbody.find_elements(By.XPATH, ".//input[@type='email']")
            ),
            message=f"Created user {email} not found in users table",
        )

    def test_admin_edits_user_first_name(self, page: PageHelper):
        """UC-14: Admin edits an existing user's first name and saves."""
        uid = _get_first_non_admin_user_id(page)
        fn = page.by_id(f"admin-user-first-name-{uid}")
        fn.clear()
        fn.send_keys(f"Edited{unique_suffix()}")
        page.click(f"admin-user-save-{uid}")
        msg = page.by_id_visible("admin-success")
        assert msg.text.strip(), "Expected a non-empty success message after edit"

    def test_configuration_not_accessible_as_citizen(self, page: PageHelper):
        """UC-14: Citizens are redirected away from /admin (role-based access)."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/admin")
        page.wait_redirect_away_from("/admin")