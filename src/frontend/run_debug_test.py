import pytest

pytest.main(["-c", "tests/selenium/pytest.ini", "tests/selenium/tests/test_UC-07_FollowReport.py::TestUC07FollowReport::test_follow_button_present_on_public_report_for_citizen"])
