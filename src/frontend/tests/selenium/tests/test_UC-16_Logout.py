"""UC-16  Logout"""
from conftest import (
    CITIZEN_EMAIL, 
    CITIZEN_PASSWORD, 
    PageHelper,
)


class TestLogout:
    """UC-16 – Registered citizen logs out."""

    def test_successful_logout(self, page: PageHelper):
        """UC-16: Activating the logout action terminates the session and
        redirects the user to a non-restricted area, showing the login nav link."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")

        page.click("logout-button")

        assert page.by_id_visible("nav-login").is_displayed(), (
            "Login link should be visible after logout"
        )

        assert page.absent("logout-button"), (
            "Logout button should not be visible after logout"
        )

    def test_restricted_functions_inaccessible_after_logout(self, page: PageHelper):
        """UC-16: After logout, attempting to access restricted pages
        (like /reports/new or /dashboard) redirects to /login."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)

        page.logout()

        page.go("/reports/new")
        page.wait_for_url("/login")
        assert "/login" in page.driver.current_url, (
            "User should be redirected to login when accessing a restricted area after logout"
        )

    def test_expired_session_redirects_to_login(self, page: PageHelper):
        """UC-16 ext 2a: If the session is already expired (simulated by clearing local data),
        the system redirects the user to a non-restricted area."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")

        page.driver.delete_all_cookies()
        page.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")

        page.driver.refresh()
        page.wait_for_url("/login")

        assert "/login" in page.driver.current_url, (
            "User with an expired/cleared session should be redirected away from restricted pages"
        )
        assert page.absent("logout-button")