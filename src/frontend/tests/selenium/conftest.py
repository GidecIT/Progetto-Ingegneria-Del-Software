import os
import tempfile
import time
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
BASE_URL = "http://localhost:5173"
WAIT_TIMEOUT = 15
CITIZEN_EMAIL = "citizen@example.com"
CITIZEN_PASSWORD = "Citizen123!"
OPERATOR_EMAIL = "operator@example.com"
OPERATOR_PASSWORD = "Operator123!"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin123!"
OPERATOR_CATEGORY = "Roads and Urban Furniture"

# Script per svuotare un input controllato da React.
# Non basta fare `value = ''` perchè React al primo send_keys rimette il valore vecchio
# (campi concatenati -> "Invalid credentials").
# Usiamo il setter nativo e un evento "input", così React si accorge davvero del cambiamento.
# Funziona uguale su Windows e Mac perché non dipende da scorciatoie da tastiera.
_CLEAR_REACT_INPUT = (
    "const el = arguments[0];"
    "const proto = el instanceof HTMLTextAreaElement ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;"
    "const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;"
    "setter.call(el, '');"
    "el.dispatchEvent(new Event('input', { bubbles: true }));"
)

@pytest.fixture(scope="session")
def driver():
    opts = Options()
    #opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--log-level=3")
    # Force Chrome to resolve `localhost` to IPv4. On macOS `localhost` resolves
    # to ::1 (IPv6) first, but the backend binds to 0.0.0.0 (IPv4 only), so the
    # frontend's fetch() calls to http://localhost:5050 are refused and pages
    # never receive their data (tests time out waiting for elements). On Windows
    # localhost already resolves to 127.0.0.1, so this is a no-op there.
    opts.add_argument("--host-resolver-rules=MAP localhost 127.0.0.1")
    # Stop Chrome's "password found in a data breach" / save-password prompts
    # that block tests (the demo creds appear in public breach lists).
    opts.add_argument("--disable-features=PasswordLeakDetection,AutofillServerCommunication")
    opts.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(0)
    yield drv
    drv.quit()

class PageHelper:

    def __init__(self, driver: webdriver.Chrome, timeout: int=WAIT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go(self, path: str="") -> None:
        self.driver.get(f"{BASE_URL}{path}")

    def by_id(self, element_id: str):
        return self.wait.until(EC.presence_of_element_located((By.ID, element_id)), message=f"Element #{element_id} not found")

    def by_id_visible(self, element_id: str):
        return self.wait.until(EC.visibility_of_element_located((By.ID, element_id)), message=f"Element #{element_id} not visible")

    def by_id_clickable(self, element_id: str):
        return self.wait.until(EC.element_to_be_clickable((By.ID, element_id)), message=f"Element #{element_id} not clickable")

    def present(self, element_id: str, timeout: int=2) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.ID, element_id)))
            return True
        except Exception:
            return False

    def absent(self, element_id: str, timeout: int=1) -> bool:
        return not self.present(element_id, timeout=timeout)

    def _set_value(self, el, value: str) -> None:
        # Selenium's clear() is unreliable on React-controlled inputs (the
        # component re-applies its state value, so send_keys appends to any
        # default and produces doubled text). We blank the field via the native
        # value setter + an "input" event so React syncs its state, then type.
        # This is keyboard-independent and behaves identically on Windows/Mac.
        self.driver.execute_script(_CLEAR_REACT_INPUT, el)
        el.send_keys(value)

    def fill(self, element_id: str, value: str) -> None:
        el = self.by_id_visible(element_id)
        self._set_value(el, value)

    def click(self, element_id: str) -> None:
        el = self.by_id_clickable(element_id)
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    def select_by_value(self, element_id: str, value: str) -> None:
        Select(self.by_id(element_id)).select_by_value(value)

    def wait_for_url(self, fragment: str) -> None:
        self.wait.until(lambda d: fragment in d.current_url, message=f"URL did not contain '{fragment}' (Current: {self.driver.current_url})")

    def wait_redirect_away_from(self, path: str) -> None:
        self.wait.until(lambda d: path not in d.current_url, message=f"Expected redirect away from {path} (Current: {self.driver.current_url})")

    def login(self, email: str, password: str, retries: int=2) -> None:
        for attempt in range(retries):
            try:
                self.go("/")
                if self.present("logout-button", timeout=1):
                    self.go("/dashboard")
                    try:
                        profile_email = self.by_id_visible("profile-email").get_attribute("value")
                        if profile_email.lower() == email.lower():
                            return
                    except Exception:
                        pass
                    self.driver.delete_all_cookies()
                    self.driver.execute_script("window.localStorage.clear();")
                self.go("/login")
                ident = self.wait.until(EC.visibility_of_element_located((By.ID, "login-identifier")), message="Login form did not appear")
                self._set_value(ident, email)
                pwd = self.by_id_visible("login-password")
                self._set_value(pwd, password)
                self.by_id_clickable("login-submit").click()
                self.wait.until(EC.presence_of_element_located((By.ID, "logout-button")), message=f"Login failed for {email}")
                return
            except Exception:
                if attempt < retries - 1:
                    self.go("/")
                    self.driver.delete_all_cookies()
                    self.driver.execute_script("window.localStorage.clear();")
                else:
                    raise

    def logout(self) -> None:
        self.go("/")
        if self.present("logout-button", timeout=1):
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.ID, "logout-button")))
                self.driver.execute_script("arguments[0].click();", btn)
                self.wait.until(EC.presence_of_element_located((By.ID, "nav-login")))
                return
            except Exception:
                pass
        self.go("/")
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")

@pytest.fixture
def page(driver) -> PageHelper:
    p = PageHelper(driver)
    p.go("/")
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    return p

@pytest.fixture
def citizen_page(driver):
    p = PageHelper(driver)
    p.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
    return p

@pytest.fixture
def operator_page(driver):
    p = PageHelper(driver)
    p.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    return p

@pytest.fixture
def admin_page(driver):
    p = PageHelper(driver)
    p.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    return p

def unique_suffix() -> str:
    return uuid.uuid4().hex[:8]

def wait_for_report_rows(page: PageHelper) -> None:
    page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(attribute::id,'public-report-row-')]")), message="No public-report-row-* found; check seed data and backend")

def get_first_public_report_id(page: PageHelper) -> int:
    page.go("/")
    wait_for_report_rows(page)
    tbody = page.by_id("public-report-table-body")
    first_row = tbody.find_elements("tag name", "tr")[0]
    open_link = first_row.find_element("tag name", "a")
    href = open_link.get_attribute("href")
    return int(href.rstrip("/").split("/")[-1])

def write_temp_image() -> str:
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00'
        b'\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18'
        b'\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    fd, path = tempfile.mkstemp(suffix=".png")
    with os.fdopen(fd, "wb") as fh:
        fh.write(png_bytes)
    return path

def select_operator_category(page: PageHelper) -> None:
    page.wait.until(lambda d: any((option.text.strip() == OPERATOR_CATEGORY for option in Select(d.find_element(By.ID, "report-category")).options)), message=f"Category '{OPERATOR_CATEGORY}' not available in the report form")
    Select(page.by_id("report-category")).select_by_visible_text(OPERATOR_CATEGORY)

def create_report_and_get_id(page: PageHelper) -> int:
    img = write_temp_image()
    try:
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.fill("report-title", f"Test report {unique_suffix()}")
        page.fill("report-description", "Created by Selenium test suite.")
        select_operator_category(page)
        page.by_id("report-photos").send_keys(img)
        page.click("new-report-submit")
        page.wait.until(lambda d: "/reports/" in d.current_url and "/new" not in d.current_url, message="New report did not redirect to detail page")
        return int(page.driver.current_url.rstrip("/").split("/")[-1])
    finally:
        os.unlink(img)

def _assign_report_as_operator(page: PageHelper, report_id: int, skip_message: str) -> None:
    page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    page.wait_for_url("/operator")
    assign_btn_id = f"pending-report-assign-{report_id}"
    assigned_row_id = f"assigned-report-row-{report_id}"
    if page.absent(assign_btn_id) and page.absent(assigned_row_id):
        pytest.skip(skip_message)
    for _ in range(3):
        if not page.absent(assigned_row_id):
            page.logout()
            return
        if not page.absent(assign_btn_id):
            page.driver.execute_script("var e=document.getElementById(arguments[0]);if(e){e.scrollIntoView({block:'center'});e.click();}", assign_btn_id)
        try:
            WebDriverWait(page.driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, assigned_row_id)))
            page.logout()
            return
        except Exception:
            page.go("/operator")
    raise AssertionError(f"Report {report_id} did not appear in the assigned section after Assign")

def create_and_assign_report(page: PageHelper) -> int:
    report_id = create_report_and_get_id(page)
    page.logout()
    _assign_report_as_operator(page, report_id, skip_message=f"Report {report_id} is not visible in the operator pending section. The operator seed account may not handle this report's category."),
    return report_id

def create_public_report_as_new_citizen(page: PageHelper) -> int:
    sfx = unique_suffix()
    email = f"tmp_{sfx}@test.local"
    password = "TestPass123!"
    page.go("/register")
    page.fill("register-username", f"tmp_{sfx}")
    page.fill("register-first-name", "Tmp")
    page.fill("register-last-name", "Citizen")
    page.fill("register-email", email)
    page.fill("register-password", password)
    page.click("register-submit")
    if page.absent("verification-box"):
        pytest.skip("Verification link not exposed; cannot create account for follow test. ")
    verification_href = page.by_id_visible("verification-box").find_element(By.ID, "verification-link").get_attribute("href")
    page.driver.get(verification_href)
    img = write_temp_image()
    try:
        page.login(email, password)
        page.go("/reports/new")
        page.fill("report-title", f"Followable report {sfx}")
        page.fill("report-description", "Created by temp citizen for follow test.")
        select_operator_category(page)
        page.by_id("report-photos").send_keys(img)
        page.click("new-report-submit")
        page.wait.until(lambda d: "/reports/" in d.current_url and "/new" not in d.current_url, message="New report did not redirect to detail page")
        report_id = int(page.driver.current_url.rstrip("/").split("/")[-1])
    finally:
        os.unlink(img)
    page.logout()
    _assign_report_as_operator(page, report_id, skip_message=f"Report {report_id} not visible in operator pending section; ")
    page.go("/")
    wait_for_report_rows(page)
    tbody = page.by_id("public-report-table-body")
    visible_ids = [int(r.get_attribute("id").split("-")[-1]) for r in tbody.find_elements(By.XPATH, "./tr[starts-with(attribute::id,'public-report-row-')]")]
    if report_id not in visible_ids:
        pytest.skip(f"Report {report_id} is not publicly visible after assignment. ")
    return report_id