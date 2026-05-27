"""UC-15  Admin manages report categories (create, edit, deactivate)."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, PageHelper, unique_suffix


def _wait_for_category_rows(page: PageHelper):
    """Wait until at least one admin-category-row-* element is in the DOM."""
    page.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[starts-with(@id,'admin-category-row-')]")
        ),
        message="No admin-category-row-* found; categories may not have loaded",
    )


class TestAdminCategories:
    """UC-15 – Admin category management."""

    def test_categories_table_rendered(self, page: PageHelper):
        """UC-15: Admin page shows the categories table."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-categories-section")
        page.by_id("admin-categories-table")

    def test_new_category_form_present(self, page: PageHelper):
        """UC-15: The create-category form is present on the admin page."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-category-form")
        page.by_id("admin-new-category-name")
        page.by_id("admin-new-category-submit")

    def test_create_new_category(self, page: PageHelper):
        """UC-15: Submitting the create-category form shows a success message
        and the category appears in the table."""
        cat_name = f"Cat{unique_suffix()}"
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.fill("admin-new-category-name", cat_name)
        page.click("admin-new-category-submit")
        msg = page.by_id_visible("admin-success")
        assert msg.text, "Expected a non-empty success message"
        tbody = page.by_id("admin-categories-table-body")
        name_inputs = tbody.find_elements(By.XPATH, f".//input[@value='{cat_name}']")
        assert name_inputs, f"Newly created category '{cat_name}' not found in table"

    def test_edit_category_name(self, page: PageHelper):
        """UC-15: Editing a category name and saving shows a success message."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        # Wait for categories to load asynchronously
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
        assert msg.text

    def test_toggle_category_active(self, page: PageHelper):
        """UC-15: Toggling the Active flag on a category and saving updates it."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        _wait_for_category_rows(page)
        tbody = page.by_id("admin-categories-table-body")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        assert rows, "Expected at least one category row"
        cat_id = rows[0].get_attribute("id").split("-")[-1]
        page.by_id(f"admin-category-active-{cat_id}").click()
        page.click(f"admin-category-save-{cat_id}")
        page.by_id_visible("admin-success")