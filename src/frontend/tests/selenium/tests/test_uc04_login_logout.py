"""
UC-04  Login and logout flows for all three roles.
"""
import pytest
from conftest import (
    ADMIN_EMAIL, ADMIN_PASSWORD,
    CITIZEN_EMAIL, CITIZEN_PASSWORD,
    OPERATOR_EMAIL, OPERATOR_PASSWORD,
    PageHelper,
)


class TestLogin:
    """UC-04 – Login with valid credentials redirects to the role dashboard."""

    def test_uc04_login_page_renders(self, page: PageHelper):
        """UC-04: The /login route renders the login form and demo-accounts hint."""
        page.go("/login")
        page.by_id_visible("login-page")
        page.by_id("login-form")
        page.by_id("login-demo-accounts")

    def test_uc04_citizen_login_redirects_to_dashboard(self, page: PageHelper):
        """UC-04: Citizen credentials redirect to /dashboard."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.by_id("dashboard-page")

    def test_uc04_operator_login_redirects_to_operator(self, page: PageHelper):
        """UC-04: Operator credentials redirect to /operator."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        page.by_id("operator-page")

    def test_uc04_admin_login_redirects_to_admin(self, page: PageHelper):
        """UC-04: Admin credentials redirect to /admin."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-page")

    def test_uc04_invalid_credentials_show_error(self, page: PageHelper):
        """UC-04: Wrong password shows an error message on the login page."""
        page.go("/login")
        page.fill("login-identifier", CITIZEN_EMAIL)
        page.fill("login-password", "WrongPassword!")
        page.click("login-submit")
        page.by_id_visible("login-error")

    def test_uc04_logout_returns_to_public(self, page: PageHelper):
        """UC-04: Clicking Logout clears the session and shows Login / Register links."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.logout()
        page.by_id("nav-login")
        page.by_id("nav-register")

    def test_uc04_already_logged_in_skips_login_page(self, page: PageHelper):
        """UC-04: Visiting /login while already authenticated redirects away."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.go("/login")
        # Should redirect; the login form should not stay visible
        assert "/login" not in page.driver.current_url, (
            "Authenticated user should be redirected away from /login"
        )
