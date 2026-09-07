from playwright.sync_api import Playwright, Page, sync_playwright, expect



def test_nav(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")

    # ---------------- NAVIGATION ----------------

    page.get_by_role("button", name="All files", exact=True).click()
    page.get_by_role("button", name="Templates", exact=True).click()
    page.get_by_role("button", name="Pinned", exact=True).click()
    page.get_by_role("button", name="Pinned", exact=True).dblclick()
    page.get_by_role("button", name="Shared", exact=True).click()
    page.get_by_role("button", name="Trash", exact=True).click()
    page.locator('button[data-view="home"]').click()

    page.locator("#notify").click()

    page.locator("#help").click()

    page.locator("#appearance").click()


    # ---------------- DOCUMENT ----------------

    page.get_by_role(
        "button",
        name="Create new",
        exact=True
    ).click()

    modal = page.locator("#modal-shell")
    expect(modal).to_be_visible()

    document = modal.locator(
        '[data-create-kind="doc"]'
    )

    expect(document).to_be_visible()
    expect(document).to_be_enabled()
    document.click()

    page.locator('a.brand[href="/"]').click()
    expect(page).to_have_url(
        "https://tools.nativeoffice.online/"
    )


    # ---------------- SPREADSHEET ----------------

    page.get_by_role(
        "button",
        name="Create new",
        exact=True
    ).click()

    modal = page.locator("#modal-shell")
    expect(modal).to_be_visible()

    spreadsheet = modal.locator(
        '[data-create-kind="sheet"]'
    )

    expect(spreadsheet).to_be_visible()
    expect(spreadsheet).to_be_enabled()
    spreadsheet.click()

    page.locator('a.brand[href="/"]').click()
    expect(page).to_have_url(
        "https://tools.nativeoffice.online/"
    )


    # ---------------- PRESENTATION ----------------

    page.get_by_role(
        "button",
        name="Create new",
        exact=True
    ).click()

    modal = page.locator("#modal-shell")
    expect(modal).to_be_visible()

    presentation = modal.locator(
        '[data-create-kind="slides"]'
    )

    expect(presentation).to_be_visible()
    expect(presentation).to_be_enabled()
    presentation.click()

    page.locator('a.brand[href="/"]').click()
    expect(page).to_have_url(
        "https://tools.nativeoffice.online/"
    )


# ---------------- DESIGN ----------------

    page.locator("#hero-create").click()

    modal = page.locator("#modal-shell")
    expect(modal).to_be_visible()

    design = modal.locator(
        '[data-create-kind="design"]'
    )

    expect(design).to_be_visible()
    expect(design).to_be_enabled()

    design.click()

    page.locator('a.brand[href="/"]').click()
    expect(page).to_have_url(
        "https://tools.nativeoffice.online/"
    )


    # ---------------- CLOSE CREATE WINDOW ----------------

    page.get_by_role(
        "button",
        name="Create new",
        exact=True
    ).click()

    modal = page.locator("#modal-shell")
    expect(modal).to_be_visible()

    page.get_by_role(
        "button",
        name="Close",
        exact=True
    ).click()