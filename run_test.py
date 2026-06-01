import subprocess
import time

def run():
    print("Running a single failing test...")
    start = time.time()
    result = subprocess.run(
        ["pytest", "-c", "tests/selenium/pytest.ini", "tests/selenium/tests/test_UC-07_FollowReport.py::TestUC07FollowReport::test_follow_button_present_on_public_report_for_citizen"],
        capture_output=True,
        text=True
    )
    print(f"Took {time.time() - start:.2f}s")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)

run()
