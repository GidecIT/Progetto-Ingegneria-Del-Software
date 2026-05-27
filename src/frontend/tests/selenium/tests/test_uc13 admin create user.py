"""UC-13  Admin creates a new user account via the admin panel."""
from selenium.webdriver.common.by import By

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix


class TestAdminCreateUser:
    """UC-13 – Admin creates a new user."""

    def test_admin_page_renders(self, page: PageHelper):
        """UC-13: Admin page is accessible and shows the create-user form."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-page")
        page.by_id("admin-user-form")

    def test_create_operator_user(self, page: PageHelper):
        """UC-13: Submitting the create-user form with operator role shows a
        success message and the user appears in the users table."""
        sfx = unique_suffix()
        email = f"op_{sfx}@test.local"
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.fill("admin-new-user-username", f"op_{sfx}")
        page.fill("admin-new-user-first-name", "Op")
        page.fill("admin-new-user-last-name", "Test")
        page.fill("admin-new-user-email", email)
        page.fill("admin-new-user-password", "TestPass123!")
        page.select_by_value("admin-new-user-role", "operator")
        page.click("admin-new-user-submit")
        msg = page.by_id_visible("admin-success")
        assert msg.text, "Expected a non-empty success message"
        tbody = page.by_id("admin-users-table-body")
        matches = tbody.find_elements(
            By.XPATH, f".//input[@type='email'][@value='{email}']"
        )
        assert matches, f"Created user {email} not found in users table"

    def test_create_citizen_user(self, page: PageHelper):
        """UC-13: Admin can create a citizen-role account."""
        sfx = unique_suffix()
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.fill("admin-new-user-username", f"cit_{sfx}")
        page.fill("admin-new-user-first-name", "Cit")
        page.fill("admin-new-user-last-name", "Test")
        page.fill("admin-new-user-email", f"cit_{sfx}@test.local")
        page.fill("admin-new-user-password", "TestPass123!")
        page.select_by_value("admin-new-user-role", "citizen")
        page.click("admin-new-user-submit")
        page.by_id_visible("admin-success")

    def test_admin_not_accessible_as_citizen(self, page: PageHelper):
        """UC-13: Citizens are redirected away from /admin."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/admin")
        # ProtectedRoute redirects asynchronously after session check
        page.wait_redirect_away_from("/admin")