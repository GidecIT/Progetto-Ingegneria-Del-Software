"""UC-04  Browse reports on map"""
from selenium.webdriver.common.by import By

from conftest import PageHelper, wait_for_report_rows


class TestBrowseReportsOnMap:
    """UC-04 – Visitor browses published reports on the public map."""

    def test_map_card_rendered_on_home_page(self, page: PageHelper):
        """UC-04: The public map card is visible on the home page without login."""
        page.go("/")
        assert page.by_id_visible("public-map-card").is_displayed()
        assert page.by_id("public-map-title").is_displayed()

    def test_map_panel_element_present(self, page: PageHelper):
        """UC-04: The Leaflet map container element is present inside the map card."""
        page.go("/")
        map_card = page.by_id("public-map-card")
        map_el = map_card.find_element(By.ID, "public-map")
        assert map_el.is_displayed(), "Map panel element should be visible"

    def test_report_markers_appear_after_data_loads(self, page: PageHelper):
        """UC-04: After the API response, report markers with prefixed IDs
        appear on the map for each published report."""
        page.go("/")
        wait_for_report_rows(page)
        # Each report marker has id="public-report-row-{id}-map-marker"
        markers = page.driver.find_elements(
            By.XPATH, "//*[contains(@id,'-map-marker')]"
        )
        assert len(markers) > 0, (
            "Expected at least one map marker after report data loads"
        )

    def test_map_accessible_without_authentication(self, page: PageHelper):
        """UC-04: The map is part of the public portal and does not require login."""
        page.go("/")
        assert page.absent("login-page"), "Map page should not redirect to login"
        assert page.by_id("public-map-card").is_displayed()