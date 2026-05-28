"""UC-02  Login.

A registered citizen authenticates with valid credentials and is redirected
to the appropriate area based on their role.
Invalid credentials do not create a session.
"""
from conftest import (
    ADMIN_EMAIL, ADMIN_PASSWORD,
    CITIZEN_EMAIL, CITIZEN_PASSWORD,
    OPERATOR_EMAIL, OPERATOR_PASSWORD,
    PageHelper,
)


class TestLogin:
    """UC-02 – Registered citizen logs in."""

    def test_login_page_renders(self, page: PageHelper):
        """UC-02: The /login route shows the login form and demo-accounts hint."""
        page.go("/login")
        assert page.by_id_visible("login-page").is_displayed()
        assert page.by_id("login-form").is_displayed()
        assert page.by_id("login-demo-accounts").is_displayed()

    def test_citizen_login_redirects_to_dashboard(self, page: PageHelper):
        """UC-02: Valid citizen credentials authenticate and redirect to /dashboard."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        assert page.by_id("dashboard-page").is_displayed()
        assert "/dashboard" in page.driver.current_url

    def test_operator_login_redirects_to_operator_page(self, page: PageHelper):
        """UC-02: Valid operator credentials authenticate and redirect to /operator."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        assert page.by_id("operator-page").is_displayed()
        assert "/operator" in page.driver.current_url

    def test_admin_login_redirects_to_admin_page(self, page: PageHelper):
        """UC-02: Valid admin credentials authenticate and redirect to /admin."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        assert page.by_id("admin-page").is_displayed()
        assert "/admin" in page.driver.current_url

    def test_invalid_credentials_do_not_authenticate(self, page: PageHelper):
        """UC-02 ext 4a: Wrong password shows an error and the user stays on /login."""
        page.go("/login")
        page.fill("login-identifier", CITIZEN_EMAIL)
        page.fill("login-password", "WrongPassword!")
        page.click("login-submit")

        error = page.by_id_visible("login-error")
        assert error.is_displayed(), "Error element should be visible"
        assert error.text.strip(), "Error message should not be empty"
        assert "/login" in page.driver.current_url, (
            "User should remain on /login after a failed attempt"
        )

    def test_already_authenticated_user_skips_login_page(self, page: PageHelper):
        """UC-02: Visiting /login while already authenticated redirects away —
        the system does not show the login form to a user who already has a
        valid session."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.go("/login")

        try:
            page.wait.until(
                lambda d: "/login" not in d.current_url,
                message="Authenticated user should be redirected away from /login",
            )
        except Exception:
            pass

        assert "/login" not in page.driver.current_url, (
            "Authenticated user should be redirected away from /login"
        )
        assert page.absent("login-form"), (
            "Login form should not be visible for an authenticated user"
        )