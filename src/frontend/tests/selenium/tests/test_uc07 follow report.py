"""UC-07  Follow and unfollow a published report (citizen role)."""
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, get_first_public_report_id


class TestFollowReport:
    """UC-07 – Follow / unfollow a public report."""

    def test_follow_button_visible_for_citizen(self, page: PageHelper):
        """UC-07: The Follow button is visible for an authenticated citizen."""
        report_id = get_first_public_report_id(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")
        page.by_id_visible("follow-button")

    def test_follow_toggles_label(self, page: PageHelper):
        """UC-07: Clicking Follow changes the button label; clicking again reverts it."""
        report_id = get_first_public_report_id(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")

        btn = page.by_id_visible("follow-button")
        initial_label = btn.text.strip()

        btn.click()

        # Wait explicitly for the label to change before asserting
        page.wait.until(
            lambda d: d.find_element("id", "follow-button").text.strip() != initial_label,
            message="Follow button label did not change after first click",
        )
        new_label = page.driver.find_element("id", "follow-button").text.strip()

        page.driver.find_element("id", "follow-button").click()

        # Wait for label to revert
        page.wait.until(
            lambda d: d.find_element("id", "follow-button").text.strip() == initial_label,
            message="Follow button label did not revert after second click",
        )

    def test_follow_button_absent_for_guest(self, page: PageHelper):
        """UC-07: The Follow button is not shown to unauthenticated visitors."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        assert page.absent("follow-button"), (
            "Follow button should not be visible to unauthenticated users"
        )