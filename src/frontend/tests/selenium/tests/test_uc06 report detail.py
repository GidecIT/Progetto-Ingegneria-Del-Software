"""UC-06  View the detail page of a published report."""
from conftest import PageHelper, get_first_public_report_id


class TestReportDetail:
    """UC-06 – Report detail page."""

    def test_detail_accessible_as_guest(self, page: PageHelper):
        """UC-06: Public report detail is accessible without login."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("report-detail-page")
        page.by_id("report-detail-title")

    def test_status_history_shown(self, page: PageHelper):
        """UC-06: Status history list is rendered on the detail page."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("status-history-card")
        page.by_id("status-history-list")

    def test_map_and_photos_sections_present(self, page: PageHelper):
        """UC-06: Map and photo sections are included in the detail layout."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("report-detail-map-card")
        page.by_id("report-detail-photos-card")

    def test_metadata_fields_displayed(self, page: PageHelper):
        """UC-06: Category, reporter, followers count and timestamps are shown."""
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("report-detail-category")
        page.by_id("report-detail-reporter")
        page.by_id("report-detail-followers")
        page.by_id("report-detail-created")

    def test_invalid_report_id_shows_error(self, page: PageHelper):
        """UC-06: Navigating to a non-existent report shows an error message."""
        page.go("/reports/999999")
        page.by_id("report-detail-page")
        page.by_id_visible("report-detail-error")