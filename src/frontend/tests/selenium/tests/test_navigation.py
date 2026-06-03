import pytest
from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, CITIZEN_EMAIL, CITIZEN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper

class TestNavigation:

    def test_brand_link_goes_to_home(self, page: PageHelper):
        page.go('/login')
        page.click('brand-link')
        page.by_id('home-page')

    def test_not_found_page_shown_for_unknown_route(self, page: PageHelper):
        page.go('/this-route-does-not-exist')
        page.by_id('not-found-page')

    def test_guest_sees_login_and_register_nav(self, page: PageHelper):
        page.go('/')
        page.by_id('nav-login')
        page.by_id('nav-register')

    def test_citizen_nav_links(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.by_id('nav-new-report')
        page.by_id('nav-dashboard')
        assert page.absent('nav-operator'), 'Citizen should not see Operator nav'
        assert page.absent('nav-admin'), 'Citizen should not see Admin nav'

    def test_operator_nav_links(self, page: PageHelper):
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.by_id('nav-operator')
        page.by_id('nav-dashboard')
        assert page.absent('nav-new-report'), 'Operator should not see New Report nav'
        assert page.absent('nav-admin'), 'Operator should not see Admin nav'

    def test_admin_nav_links(self, page: PageHelper):
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.by_id('nav-operator')
        page.by_id('nav-admin')

    def test_logout_button_visible_when_logged_in(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.by_id('logout-button')

    def test_swagger_link_always_present(self, page: PageHelper):
        page.go('/')
        link = page.by_id('nav-swagger')
        assert link.get_attribute('href'), 'Swagger nav link has no href'