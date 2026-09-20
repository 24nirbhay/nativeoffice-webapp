from playwright.sync_api import Playwright, Page, sync_playwright, expect
from qa.test_cases import test_case as link_test_case



@link_test_case("TC-NAV-001")
def test_nav(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")

    # ---------------- NAVIGATION ----------------

    page.get_by_role("button", name="Home", exact=True).click()
    page.get_by_role("button", name="Recent", exact=True).click()
    page.get_by_role("button", name="Create new", exact=True).click()
    page.get_by_role("button", name="Templates", exact=True).click()
    page.get_by_role("button", name="Pinned", exact=True).click()
    page.get_by_role("button", name="Help", exact=True).click()
    page.get_by_role("button", name="Switch to dark theme", exact=True).click()

    # ---------------- DOCUMENT ----------------

    page.get_by_role("button", name="Create new", exact=True).click()
    document = page.get_by_role("button", name="Document Write & collaborate", exact=True)

    expect(document).to_be_visible()
    expect(document).to_be_enabled()
    document.click()

    page.goto("https://tools.nativeoffice.online/")
    expect(page).to_have_url("https://tools.nativeoffice.online/")
    expect(page.get_by_role("button", name="Create new", exact=True)).to_be_visible()

    # ---------------- SPREADSHEET ----------------

    page.get_by_role("button", name="Create new", exact=True).click()
    spreadsheet = page.get_by_role("button", name="Spreadsheet Data & formulas", exact=True)

    expect(spreadsheet).to_be_visible()
    expect(spreadsheet).to_be_enabled()
    spreadsheet.click()

    page.goto("https://tools.nativeoffice.online/")
    expect(page).to_have_url("https://tools.nativeoffice.online/")
    expect(page.get_by_role("button", name="Create new", exact=True)).to_be_visible()

    # ---------------- PRESENTATION ----------------

    page.get_by_role("button", name="Create new", exact=True).click()
    presentation = page.get_by_role("button", name="Presentation Slides that land", exact=True)

    expect(presentation).to_be_visible()
    expect(presentation).to_be_enabled()
    presentation.click()

    page.goto("https://tools.nativeoffice.online/")
    expect(page).to_have_url("https://tools.nativeoffice.online/")
    expect(page.get_by_role("button", name="Create new", exact=True)).to_be_visible()

    # ---------------- DESIGN ----------------

    page.get_by_role("button", name="Create new", exact=True).click()
    design = page.get_by_role("button", name="Design Posters & posts", exact=True)

    expect(design).to_be_visible()
    expect(design).to_be_enabled()
    design.click()

    page.goto("https://tools.nativeoffice.online/")
    expect(page).to_have_url("https://tools.nativeoffice.online/")
    expect(page.get_by_role("button", name="Create new", exact=True)).to_be_visible()


