"""UC-01  Register account"""
from conftest import PageHelper, unique_suffix


class TestRegisterAccount:

    def test_register_page_renders(self, page: PageHelper):
        """UC-01: The /register route renders the registration form."""
        page.go("/register")
        assert page.by_id_visible("register-page").is_displayed()
        assert page.by_id("register-form").is_displayed()

    def test_successful_registration_shows_success_message(self, page: PageHelper):
        """UC-01: Submitting valid unique credentials shows a success message."""
        sfx = unique_suffix()
        page.go("/register")
        page.fill("register-username", f"user_{sfx}")
        page.fill("register-first-name", "Test")
        page.fill("register-last-name", "Citizen")
        page.fill("register-email", f"user_{sfx}@test.local")
        page.fill("register-password", "TestPass123!")
        page.click("register-submit")

        success = page.by_id_visible("register-success")
        assert success.text.strip(), "Success message should not be empty"

    def test_verification_link_exposed_in_local_env(self, page: PageHelper):
        """UC-01: After registration a verification link is shown so the demo
        user can activate the account without a real email service."""
        sfx = unique_suffix()
        page.go("/register")
        page.fill("register-username", f"ver_{sfx}")
        page.fill("register-first-name", "Ver")
        page.fill("register-last-name", "Test")
        page.fill("register-email", f"ver_{sfx}@test.local")
        page.fill("register-password", "TestPass123!")
        page.click("register-submit")

        box = page.by_id_visible("verification-box")
        link = box.find_element("id", "verification-link")
        href = link.get_attribute("href")
        assert href and "verify" in href.lower(), (
            f"Verification link href '{href}' does not look valid"
        )

    def test_duplicate_email_shows_error(self, page: PageHelper):
        """UC-01 ext 4b: Registering with an already-used email shows an error
        and keeps the user on the registration page."""
        page.go("/register")
        page.fill("register-username", f"dup_{unique_suffix()}")
        page.fill("register-first-name", "Dup")
        page.fill("register-last-name", "User")
        page.fill("register-email", "citizen@example.com") 
        page.fill("register-password", "TestPass123!")
        page.click("register-submit")

        error = page.by_id_visible("register-error")
        assert "email" in error.text.lower(), (
            f"Expected an email-related error, got: '{error.text}'"
        )