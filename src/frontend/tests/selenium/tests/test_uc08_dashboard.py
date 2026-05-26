"""
UC-08  Citizen dashboard – view reports, notifications, edit profile.
"""
import pytest
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix


class TestDashboard:
    """UC-08 – Citizen dashboard."""

    def test_uc08_dashboard_renders(self, page: PageHelper):
        """UC-08: The dashboard page is accessible after citizen login."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.by_id("dashboard-page")
        page.by_id("profile-section")

    def test_uc08_profile_form_pre_filled(self, page: PageHelper):
        """UC-08: The profile form is pre-filled with the current user's data."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        username_el = page.by_id("profile-username")
        assert username_el.get_attribute("value"), "Profile username should be pre-filled"
        email_el = page.by_id("profile-email")
        assert "citizen" in email_el.get_attribute("value").lower(), (
            "Profile email should contain the citizen address"
        )

    def test_uc08_update_profile_first_name(self, page: PageHelper):
        """UC-08: Changing the first name and saving shows a success message."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")

        new_name = f"Auto{unique_suffix()}"
        page.fill("profile-first-name", new_name)
        page.click("profile-save")

        success = page.by_id_visible("profile-success")
        assert success.text, "Expected a non-empty profile success message"

    def test_uc08_my_reports_table_present(self, page: PageHelper):
        """UC-08: The 'My reports' table is shown in the dashboard."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.by_id("my-reports-table")

    def test_uc08_notifications_card_present(self, page: PageHelper):
        """UC-08: The notifications card is rendered in the dashboard."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.by_id("notifications-card")

    def test_uc08_dashboard_not_accessible_as_guest(self, page: PageHelper):
        """UC-08: Accessing /dashboard without login redirects to /login."""
        page.go("/dashboard")
        page.wait_for_url("/login")
