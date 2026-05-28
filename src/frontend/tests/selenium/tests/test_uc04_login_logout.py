import pytest
from conftest import (
    ADMIN_EMAIL, ADMIN_PASSWORD,
    CITIZEN_EMAIL, CITIZEN_PASSWORD,
    OPERATOR_EMAIL, OPERATOR_PASSWORD,
    PageHelper,
)

class TestLogin:
    def test_uc04_login_page_renders(self, page: PageHelper):
        page.go("/login")
        page.by_id_visible("login-page")
        page.by_id("login-form")
        page.by_id("login-demo-accounts")

    def test_uc04_citizen_login_redirects_to_dashboard(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.by_id("dashboard-page")

    def test_uc04_operator_login_redirects_to_operator(self, page: PageHelper):
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        page.by_id("operator-page")

    def test_uc04_admin_login_redirects_to_admin(self, page: PageHelper):
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-page")

    def test_uc04_invalid_c2redentials_show_error(self, page: PageHelper):
        page.go("/login")
        page.fill("login-identifier", CITIZEN_EMAIL)
        page.fill("login-password", "WrongPassword!")
        page.click("login-submit")
        page.by_id_visible("login-error")

    def test_uc04_logout_returns_to_public(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.logout()
        page.by_id("nav-login")
        page.by_id("nav-register")

    def test_uc04_already_logged_in(self, page: PageHelper):
        # skippa login page
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