from playwright.sync_api import Page, expect


def test_authenticated_home(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/", wait_until="domcontentloaded")
    expect(page.get_by_role("button", name="Create new", exact=True)).to_be_visible()
