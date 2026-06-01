"""UC-15  Manage citizen profile"""
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix


class TestManageCitizenProfile:
    """UC-15 – Citizen manages their profile preferences."""

    def test_dashboard_shows_profile_form(self, page: PageHelper):
        """UC-15: The profile form is accessible from the citizen dashboard."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        assert page.by_id("profile-section").is_displayed()
        assert page.by_id("profile-form").is_displayed()

    def test_profile_form_pre_filled_with_current_data(self, page: PageHelper):
        """UC-15: The system displays current profile data — username and
        email are pre-filled so the citizen can review before changing."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")

        username = page.by_id("profile-username").get_attribute("value")
        assert username, "Username field should be pre-filled"

        email = page.by_id("profile-email").get_attribute("value")
        assert email, "Email field should be pre-filled"

    def test_update_first_name_saves_and_confirms(self, page: PageHelper):
        """UC-15: Changing the first name and clicking Save shows a success
        message confirming the profile was updated."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")

        new_name = f"Auto{unique_suffix()}"
        page.fill("profile-first-name", new_name)
        page.click("profile-save")

        success = page.by_id_visible("profile-success")
        assert success.text.strip(), "Success message should not be empty"

    def test_email_notifications_checkbox_present(self, page: PageHelper):
        """UC-15: The email notifications preference checkbox is present and
        the citizen can toggle it."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        cb = page.by_id("profile-email-notifications")
        assert cb.is_displayed(), "Email notifications checkbox should be visible"

    def test_profile_picture_upload_field_present(self, page: PageHelper):
        """UC-15: The profile picture file input is present on the form."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        assert page.by_id("profile-picture").is_displayed()

    def test_my_reports_table_visible_on_dashboard(self, page: PageHelper):
        """UC-15: The citizen's submitted reports are listed on the dashboard
        so they can monitor their own activity."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        assert page.by_id("my-reports-table").is_displayed()

    def test_notifications_card_visible_on_dashboard(self, page: PageHelper):
        """UC-15: The notifications card is visible on the dashboard so the
        citizen can see status updates."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        assert page.by_id("notifications-card").is_displayed()

    def test_dashboard_not_accessible_as_guest(self, page: PageHelper):
        """UC-15: Unauthenticated access to /dashboard redirects to /login."""
        page.go("/dashboard")
        page.wait_for_url("/login")
        assert "/login" in page.driver.current_url