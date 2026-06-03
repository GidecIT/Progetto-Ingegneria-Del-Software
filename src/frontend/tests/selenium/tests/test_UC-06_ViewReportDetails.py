from conftest import PageHelper, get_first_public_report_id

class TestViewReportDetails:

    def test_detail_page_accessible_without_login(self, page: PageHelper):
        report_id = get_first_public_report_id(page)
        page.go(f'/reports/{report_id}')
        assert page.by_id('report-detail-page').is_displayed()
        assert page.by_id('report-detail-title').is_displayed()

    def test_detail_page_shows_required_metadata(self, page: PageHelper):
        report_id = get_first_public_report_id(page)
        page.go(f'/reports/{report_id}')
        assert page.by_id('report-detail-category').is_displayed()
        assert page.by_id('report-detail-reporter').is_displayed()
        assert page.by_id('report-detail-followers').is_displayed()
        assert page.by_id('report-detail-created').is_displayed()

    def test_status_history_section_rendered(self, page: PageHelper):
        report_id = get_first_public_report_id(page)
        page.go(f'/reports/{report_id}')
        assert page.by_id('status-history-card').is_displayed()
        assert page.by_id('status-history-list').is_displayed()

    def test_map_and_photos_sections_present(self, page: PageHelper):
        report_id = get_first_public_report_id(page)
        page.go(f'/reports/{report_id}')
        assert page.by_id('report-detail-map-card').is_displayed()
        assert page.by_id('report-detail-photos-card').is_displayed()

    def test_unavailable_report_shows_error(self, page: PageHelper):
        page.go('/reports/999999')
        assert page.by_id('report-detail-page').is_displayed()
        error = page.by_id_visible('report-detail-error')
        assert error.text.strip(), 'Error message should not be empty'