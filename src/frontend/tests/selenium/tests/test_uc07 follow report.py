"""UC-07  Follow and unfollow a published report (citizen role)."""
import pytest
from selenium.webdriver.common.by import By

from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, wait_for_report_rows


def _get_followable_report_id(page: PageHelper) -> int:
    """Return the ID of a public report that the citizen seed account did NOT
    create (to avoid the backend restriction on following your own report).
    Skips if no suitable report is found."""
    page.go("/")
    wait_for_report_rows(page)
    tbody = page.by_id("public-report-table-body")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        links = row.find_elements(By.TAG_NAME, "a")
        if not links:
            continue
        href = links[0].get_attribute("href")
        rid = int(href.rstrip("/").split("/")[-1])
        # Open the detail page and check the reporter
        page.go(f"/reports/{rid}")
        page.by_id("report-detail-page")
        reporter_el = page.by_id("report-detail-reporter-value")
        reporter = reporter_el.text.strip().lower()
        # Skip reports created by the citizen seed account
        if "citizen" not in reporter:
            return rid
    pytest.skip(
        "No followable public report found: all visible reports were created "
        "by the citizen seed account, which cannot follow its own reports."
    )


class TestFollowReport:
    """UC-07 – Follow / unfollow a public report."""

    def test_follow_button_visible_for_citizen(self, page: PageHelper):
        """UC-07: The Follow button is visible for an authenticated citizen
        on a report they did not create."""
        report_id = _get_followable_report_id(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")
        page.by_id_visible("follow-button")

    def test_follow_toggles_label(self, page: PageHelper):
        """UC-07: Clicking Follow/Unfollow changes the button label.
        Uses a report not created by the citizen to avoid backend restrictions."""
        report_id = _get_followable_report_id(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")

        btn = page.by_id_visible("follow-button")
        current_label = btn.text.strip()

        # Normalise to 'not following' state first
        if "Unfollow" in current_label:
            btn.click()
            page.wait.until(
                lambda d: "Follow report" == d.find_element("id", "follow-button").text.strip(),
                message="Could not reset to 'Follow report' state",
            )

        # Now click Follow and verify the label changes
        page.driver.find_element("id", "follow-button").click()
        page.wait.until(
            lambda d: "Unfollow" in d.find_element("id", "follow-button").text.strip(),
            message="Button did not change to 'Unfollow report' after clicking Follow",
        )

    def test_follow_button_absent_for_guest(self, page: PageHelper):
        """UC-07: The Follow button is not shown to unauthenticated visitors."""
        page.go("/")
        wait_for_report_rows(page)
        tbody = page.by_id("public-report-table-body")
        first_row = tbody.find_elements(By.TAG_NAME, "tr")[0]
        href = first_row.find_element(By.TAG_NAME, "a").get_attribute("href")
        rid = int(href.rstrip("/").split("/")[-1])
        page.go(f"/reports/{rid}")
        assert page.absent("follow-button"), (
            "Follow button should not be visible to unauthenticated users"
        )