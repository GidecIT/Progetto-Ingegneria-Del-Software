"""UC-13  Admin creates a new user account via the admin panel."""
from selenium.webdriver.common.by import By

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix


def _create_user_and_verify(page: PageHelper, role: str) -> None:
    """Fill the create-user form, submit, and verify the new user appears
    in the users table. Used by both operator and citizen creation tests."""
    sfx = unique_suffix()
    email = f"{role}_{sfx}@test.local"

    page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url("/admin")
    page.fill("admin-new-user-username", f"{role}_{sfx}")
    page.fill("admin-new-user-first-name", role.capitalize())
    page.fill("admin-new-user-last-name", "Test")
    page.fill("admin-new-user-email", email)
    page.fill("admin-new-user-password", "TestPass123!")
    page.select_by_value("admin-new-user-role", role)
    page.click("admin-new-user-submit")

    msg = page.by_id_visible("admin-success")
    assert msg.text, "Expected a non-empty success message"

    # After creation loadAdminData() reloads the table. Each row has an
    # <input type="email"> whose JS .value property holds the address.
    # React does not update the HTML @value attribute, so we read the
    # property directly with get_property("value").
    tbody = page.by_id("admin-users-table-body")
    page.wait.until(
        lambda d: any(
            el.get_property("value") == email
            for el in tbody.find_elements(By.XPATH, ".//input[@type='email']")
        ),
        message=f"Created {role} user {email} not found in users table after reload",
    )


class TestAdminCreateUser:
    """UC-13 – Admin creates a new user."""

    def test_admin_page_renders(self, page: PageHelper):
        """UC-13: Admin page is accessible and shows the create-user form."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-page")
        page.by_id("admin-user-form")

    def test_create_operator_user(self, page: PageHelper):
        """UC-13: Admin creates an operator account; success message appears
        and the user is present in the users table."""
        _create_user_and_verify(page, "operator")

    def test_create_citizen_user(self, page: PageHelper):
        """UC-13: Admin creates a citizen account; success message appears
        and the user is present in the users table."""
        _create_user_and_verify(page, "citizen")

    def test_admin_not_accessible_as_citizen(self, page: PageHelper):
        """UC-13: Citizens are redirected away from /admin."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/admin")
        page.wait_redirect_away_from("/admin")