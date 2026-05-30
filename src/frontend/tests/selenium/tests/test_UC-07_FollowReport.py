"""UC-07  Follow report.

An authenticated citizen follows a report submitted by another citizen
in order to receive status update notifications.
"""
import pytest
from selenium.webdriver.common.by import By

from conftest import (
    CITIZEN_EMAIL, 
    CITIZEN_PASSWORD, 
    PageHelper, 
    wait_for_report_rows,
    create_public_report_as_new_citizen
)


class TestFollowReport:
    """UC-07 – Citizen follows and unfollows a report."""

    def test_follow_button_visible_for_authenticated_citizen(self, page: PageHelper):
        """UC-07: The Follow button is visible on a public report detail page
        for an authenticated citizen who did not create the report."""
        report_id = create_public_report_as_new_citizen(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")
        assert page.by_id_visible("follow-button").is_displayed()

    def test_follow_action_changes_button_label(self, page: PageHelper):
        """UC-07: Clicking Follow registers the citizen as follower — the button
        label changes to 'Unfollow report', confirming the system recorded the
        follow action."""
        report_id = create_public_report_as_new_citizen(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")

        btn = page.by_id_visible("follow-button")

        # Normalise to 'not following' state first
        if "Unfollow" in btn.text.strip():
            btn.click()
            page.wait.until(
                lambda d: "Follow report" == d.find_element("id", "follow-button").text.strip(),
                message="Could not reset to 'Follow report' state",
            )

        page.driver.find_element("id", "follow-button").click()
        page.wait.until(
            lambda d: "Unfollow" in d.find_element("id", "follow-button").text.strip(),
            message="Button did not change to 'Unfollow report' after clicking Follow",
        )

    def test_follow_button_absent_for_unauthenticated_visitor(self, page: PageHelper):
        """UC-07 ext 3b: The Follow button is not shown to visitors who are not
        logged in — the system requires authentication before following."""
        page.go("/")
        wait_for_report_rows(page)
        tbody = page.by_id("public-report-table-body")
        first_row = tbody.find_elements(By.TAG_NAME, "tr")[0]
        href = first_row.find_element(By.TAG_NAME, "a").get_attribute("href")
        rid = int(href.rstrip("/").split("/")[-1])
        page.go(f"/reports/{rid}")
        assert page.absent("follow-button"), (
            "Follow button must not be visible to unauthenticated visitors"
        )