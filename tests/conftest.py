import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver(request):
    """
    Creates one browser per test, and guarantees it closes
    afterwards even if the test fails (that's what 'yield' does).
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Uncomment the line below to run without opening a visible window
    # (this is what Jenkins/CI will use, since it has no display).
    options.add_argument("--headless=new")

    # Stops Chrome's built-in "Change your password" / "Save password?"
    # popups from appearing. SauceDemo's password (secret_sauce) is public
    # and known to be leaked, so Chrome flags it every single login -
    # and that popup can sit on top of the page and block Selenium's
    # element lookups underneath it.
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-features=PasswordLeakDetection")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)

    yield drv

    # If the test that used this driver failed, save a screenshot
    # BEFORE quitting the browser, so you can see exactly what the
    # page looked like at the moment it failed.
    if request.node.rep_call.failed:
        os.makedirs("reports", exist_ok=True)
        screenshot_path = os.path.join("reports", f"FAILED_{request.node.name}.png")
        drv.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved to: {screenshot_path}")

    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Standard pytest hook that stores the pass/fail result of each test
    phase (setup/call/teardown) onto the test item itself, so the
    'driver' fixture above can check 'did the test just fail?' during
    its own teardown.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)