"""
UC-03  Self-registration of a new citizen account.
"""
import pytest
from conftest import PageHelper, unique_suffix


class TestRegistration:
    """UC-03 – Citizen self-registration."""

    def test_uc03_register_page_renders(self, page: PageHelper):
        """UC-03: /register renders the registration form."""
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

        page.by_id_visible("register-error")
