import pytest
from selenium.webdriver.common.by import By
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, create_public_report_as_new_citizen, get_first_public_report_id

class TestUC07FollowReport:

    def test_follow_button_present_on_public_report_for_citizen(self, page: PageHelper):
        report_id = create_public_report_as_new_citizen(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        assert page.by_id_visible('follow-button').is_displayed()

    def test_follow_button_text_is_follow_or_unfollow(self, page: PageHelper):
        report_id = create_public_report_as_new_citizen(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        btn_text = page.by_id_visible('follow-button').text.lower()
        assert 'follow' in btn_text, f"Follow button text should contain 'follow', got: '{btn_text}'"

    @pytest.mark.implementation_bug("The follow button requires a double click to toggle")
    def test_clicking_follow_button_toggles_text(self, page: PageHelper):
        report_id = create_public_report_as_new_citizen(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        follow_btn = page.by_id_visible('follow-button')
        initial_text = follow_btn.text
        follow_btn.click()
        page.wait.until(
            lambda d: d.find_element(By.ID, 'follow-button').text != initial_text,
            message='Follow button text should change after a single click',
        )
        new_text = page.by_id_visible('follow-button').text
        assert new_text != initial_text
        assert 'follow' in new_text.lower()

    def test_follow_button_not_visible_for_anonymous_user(self, page: PageHelper):
        report_id = get_first_public_report_id(page)
        page.go(f'/reports/{report_id}')
        assert page.absent('follow-button'), 'Follow button must not be visible to unauthenticated visitors'

    @pytest.mark.implementation_bug("The follow button requires a double click to register a follow")
    def test_followers_count_updates_after_follow(self, page: PageHelper):
        report_id = create_public_report_as_new_citizen(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        followers_el = page.by_id_visible('report-detail-followers-value')
        initial_count = int(followers_el.text.strip() or '0')
        follow_btn = page.by_id_visible('follow-button')
        if 'unfollow' in follow_btn.text.lower():
            pytest.skip('Report already followed; skipping count-increase test')
        follow_btn.click()
        page.wait.until(
            lambda d: int(d.find_element(By.ID, 'report-detail-followers-value').text.strip() or '0') == initial_count + 1,
            message='Followers count should increase by 1 after a single click',
        )
        new_count = int(page.by_id_visible('report-detail-followers-value').text.strip() or '0')
        assert new_count == initial_count + 1, f'Followers count should increase by 1 after following, got {initial_count} -> {new_count}'