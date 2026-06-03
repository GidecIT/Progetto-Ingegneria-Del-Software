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

    def test_clicking_follow_button_toggles_text(self, page: PageHelper):
        report_id = create_public_report_as_new_citizen(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        follow_btn = page.by_id_visible('follow-button')
        initial_text = follow_btn.text
        for _ in range(4):
            btn = page.by_id_visible('follow-button')
            if btn.text != initial_text:
                break
            btn.click()
            try:
                page.wait.until(lambda d: d.find_element(By.ID, 'follow-button').text != initial_text)
                break
            except Exception:
                page.go(f'/reports/{report_id}')
        else:
            raise AssertionError('Follow button text should change after clicking')
        new_text = page.by_id_visible('follow-button').text
        assert new_text != initial_text
        assert 'follow' in new_text.lower()

    def test_follow_button_not_visible_for_anonymous_user(self, page: PageHelper):
        report_id = get_first_public_report_id(page)
        page.go(f'/reports/{report_id}')
        assert page.absent('follow-button'), 'Follow button must not be visible to unauthenticated visitors'

    def test_followers_count_updates_after_follow(self, page: PageHelper):
        report_id = create_public_report_as_new_citizen(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        followers_el = page.by_id_visible('report-detail-followers-value')
        initial_count = int(followers_el.text.strip() or '0')
        follow_btn = page.by_id_visible('follow-button')
        initial_btn_text = follow_btn.text
        if 'unfollow' not in initial_btn_text.lower():
            for _ in range(4):
                btn = page.by_id_visible('follow-button')
                if btn.text != initial_btn_text:
                    break
                btn.click()
                try:
                    page.wait.until(lambda d: d.find_element(By.ID, 'follow-button').text != initial_btn_text)
                    break
                except Exception:
                    page.go(f'/reports/{report_id}')
            else:
                raise AssertionError('Follow button text should change after clicking')
            new_count = int(page.by_id_visible('report-detail-followers-value').text.strip() or '0')
            assert new_count == initial_count + 1, f'Followers count should increase by 1 after following, got {initial_count} -> {new_count}'
        else:
            pytest.skip('Report already followed; skipping count-increase test')