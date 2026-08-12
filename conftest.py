import pytest


DEFAULT_UI_TIMEOUT = 30000


@pytest.fixture(scope="session")
def browser(playwright, pytestconfig):
    headless = not pytestconfig.getoption("--headed")
    slow_mo = pytestconfig.getoption("--slowmo") or 0
    browser = playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    context.tracing.stop(path="reports/trace.zip")
    context.close()


@pytest.fixture(scope="function")
def page(context, request):
    page = context.new_page()
    yield page
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        page.screenshot(path=f"reports/{request.node.name}.png")
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
