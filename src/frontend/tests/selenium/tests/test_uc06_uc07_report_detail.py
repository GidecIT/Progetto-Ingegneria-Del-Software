"""
UC-06  View the detail page for a published report.
UC-07  Follow and unfollow a published report (citizen role).
"""
import pytest
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper


def _get_first_public_report_id(page: PageHelper) -> int:
    """Return the numeric ID of the first report shown on the home page."""
    page.go("/")
    tbody = page.by_id("public-report-table-body")
    rows = tbody.find_elements("tag name", "tr")
    assert rows, "No public reports in seed data"
    open_link = rows[0].find_element("tag name", "a")
    href = open_link.get_attribute("href")
    return int(href.rstrip("/").split("/")[-1])


class TestReportDetail:
    """UC-06 – View report detail page."""

    def test_uc06_report_detail_accessible_as_guest(self, page: PageHelper):
        """UC-06: Public report detail page is accessible without login."""
        report_id = _get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("report-detail-page")
        page.by_id("report-detail-title")

    def test_uc06_status_history_shown(self, page: PageHelper):
        """UC-06: Status history list is rendered on the detail page."""
        report_id = _get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("status-history-card")
        page.by_id("status-history-list")

    def test_uc06_map_and_photos_sections_present(self, page: PageHelper):
        """UC-06: Map and photo sections are included in the detail layout."""
        report_id = _get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("report-detail-map-card")
        page.by_id("report-detail-photos-card")

    def test_uc06_metadata_fields_displayed(self, page: PageHelper):
        """UC-06: Category, reporter, followers count and timestamps are shown."""
        report_id = _get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("report-detail-category")
        page.by_id("report-detail-reporter")
        page.by_id("report-detail-followers")
        page.by_id("report-detail-created")

    def test_uc06_invalid_report_id_shows_error(self, page: PageHelper):
        """UC-06: Navigating to a non-existent report shows an error message."""
        page.go("/reports/999999")
        page.by_id("report-detail-page")
        page.by_id_visible("report-detail-error")


class TestFollowUnfollow:
    """UC-07 – Follow and unfollow a public report."""

    def test_uc07_follow_button_visible_for_citizen(self, page: PageHelper):
        """UC-07: The Follow/Unfollow button is visible for an authenticated citizen
        on a public report."""
        report_id = _get_first_public_report_id(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")
        page.by_id_visible("follow-button")

    def test_uc07_follow_toggles_label(self, page: PageHelper):
        """UC-07: Clicking Follow changes the button label to 'Unfollow report',
        and clicking again returns it to 'Follow report'."""
        report_id = _get_first_public_report_id(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f"/reports/{report_id}")

        btn = page.by_id_visible("follow-button")
        initial_label = btn.text.strip()

        btn.click()

        btn_after = page.by_id_visible("follow-button")
        after_label = btn_after.text.strip()
        assert initial_label != after_label, (
            "Follow button label should change after click"
        )

        # toggle back
        btn_after.click()
        btn_final = page.by_id_visible("follow-button")
        assert btn_final.text.strip() == initial_label, (
            "Follow button label should revert after second click"
        )

    def test_uc07_follow_button_absent_for_guest(self, page: PageHelper):
        """UC-07: The Follow button is not shown to unauthenticated visitors."""
        report_id = _get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        assert page.absent("follow-button"), (
            "Follow button should not be visible to unauthenticated users"
        )
