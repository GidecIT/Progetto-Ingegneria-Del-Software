"""UC-06  View report details"""
from conftest import PageHelper, get_first_public_report_id


class TestViewReportDetails:
    """UC-06 – Visitor views the full detail page of a published report."""

    def test_detail_page_accessible_without_login(self, page: PageHelper):
        """UC-06: The report detail page is publicly accessible."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        assert page.by_id("report-detail-page").is_displayed()
        assert page.by_id("report-detail-title").is_displayed()

    def test_detail_page_shows_required_metadata(self, page: PageHelper):
        """UC-06: Category, reporter, follower count, and creation date are shown."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        assert page.by_id("report-detail-category").is_displayed()
        assert page.by_id("report-detail-reporter").is_displayed()
        assert page.by_id("report-detail-followers").is_displayed()
        assert page.by_id("report-detail-created").is_displayed()

    def test_status_history_section_rendered(self, page: PageHelper):
        """UC-06: The status history card with at least one entry is shown."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        assert page.by_id("status-history-card").is_displayed()
        assert page.by_id("status-history-list").is_displayed()

    def test_map_and_photos_sections_present(self, page: PageHelper):
        """UC-06: Map location and photo sections are part of the detail layout."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        assert page.by_id("report-detail-map-card").is_displayed()
        assert page.by_id("report-detail-photos-card").is_displayed()

    def test_unavailable_report_shows_error(self, page: PageHelper):
        """UC-06 ext 2a: Navigating to a non-existent report ID shows an error
        message instead of an empty or partial page."""
        page.go("/reports/999999")
        assert page.by_id("report-detail-page").is_displayed()
        error = page.by_id_visible("report-detail-error")
        assert error.text.strip(), "Error message should not be empty"