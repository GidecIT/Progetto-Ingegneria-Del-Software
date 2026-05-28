import pytest
from conftest import PageHelper, unique_suffix


class TestRegistration:
    def test_uc03_register_page_renders(self, page: PageHelper):
        page.go("/register")
        page.by_id_visible("register-page")
        page.by_id("register-form")

    def test_uc03_successful_registration(self, page: PageHelper):
        """UC-03: Filling the registration form with unique data shows a success
        message and a verification link."""
        sfx = unique_suffix()
        page.go("/register")
        page.fill("register-username", f"user_{sfx}")
        page.fill("register-first-name", "Test")
        page.fill("register-last-name", "Citizen")
        page.fill("register-email", f"user_{sfx}@test.local")
        page.fill("register-password", "TestPass123!")
        page.click("register-submit")

        success = page.by_id_visible("register-success")
        assert success.text, "Expected a non-empty success message"

    def test_uc03_verification_link_exposed(self, page: PageHelper):
        """UC-03: After successful registration the verification link box appears
        so the demo user can verify the account in local environment."""
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
        assert href and "verify" in href.lower(), "Verification link does not look valid"

    def test_uc03_duplicate_email_shows_error(self, page: PageHelper):
        """UC-03: Attempting to register with an already-taken email shows an error."""
        page.go("/register")
        page.fill("register-username", f"dup_{unique_suffix()}")
        page.fill("register-first-name", "Dup")
        page.fill("register-last-name", "User")
        page.fill("register-email", "citizen@example.com")  # already seeded
        page.fill("register-password", "TestPass123!")
        page.click("register-submit")

        error_box = page.by_id_visible("register-error")      
        error_text = error_box.text.lower()
        assert "email" in error_text, f"Expected an email error, but got: '{error_box.text}'"
