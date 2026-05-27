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
        """UC-07: Clicking Follow/Unfollow changes the button label.
        We first ensure the report is in the 'not followed' state so the
        expected transition is always Follow → Unfollow."""
        report_id = get_first_public_report_id(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")

        btn = page.by_id_visible("follow-button")
        current_label = btn.text.strip()

        # If already following, click once to unfollow and reach known state
        if "Unfollow" in current_label:
            btn.click()
            page.wait.until(
                lambda d: "Follow report" == d.find_element("id", "follow-button").text.strip(),
                message="Could not reset to 'Follow report' state",
            )

        # Now we are in 'not following' state — click to follow
        page.driver.find_element("id", "follow-button").click()
        page.wait.until(
            lambda d: "Unfollow" in d.find_element("id", "follow-button").text.strip(),
            message="Button did not change to 'Unfollow report' after clicking Follow",
        )

    def test_follow_button_absent_for_guest(self, page: PageHelper):
        """UC-07: The Follow button is not shown to unauthenticated visitors."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        assert page.absent("follow-button"), (
            "Follow button should not be visible to unauthenticated users"
        )