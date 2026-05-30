"""UC-16  Logout.

A Registered Citizen wants to end the current session before leaving the portal
or handing the device to someone else.
The authenticated session is terminated and restricted functions require a new login.
"""
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

        # Perform logout manually via UI click
        page.click("logout-button")

        # Check that user is presented with the login nav option
        assert page.by_id_visible("nav-login").is_displayed(), (
            "Login link should be visible after logout"
        )

        # Check that logout button is gone
        assert page.absent("logout-button"), (
            "Logout button should not be visible after logout"
        )

    def test_restricted_functions_inaccessible_after_logout(self, page: PageHelper):
        """UC-16: After logout, attempting to access restricted pages
        (like /reports/new or /dashboard) redirects to /login."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)

        # Perform logout using the helper method
        page.logout()

        # Attempt to access a restricted creation page
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

        # Simulate expired session by clearing browser cookies and storage
        page.driver.delete_all_cookies()
        page.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")

        # Refresh to trigger authentication check
        page.driver.refresh()
        page.wait_for_url("/login")

        assert "/login" in page.driver.current_url, (
            "User with an expired/cleared session should be redirected away from restricted pages"
        )
        assert page.absent("logout-button")