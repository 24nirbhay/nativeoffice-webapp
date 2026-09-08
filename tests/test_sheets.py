from playwright.sync_api import Page, expect


def test_sheets(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")

    # Create spreadsheet
    page.locator("#hero-create").click()

    modal = page.locator("#modal-shell")
    expect(modal).to_be_visible()

    spreadsheet = modal.locator('[data-create-kind="sheet"]')
    expect(spreadsheet).to_be_visible()
    expect(spreadsheet).to_be_enabled()
    spreadsheet.click()

    # A1
    cell_a1 = page.locator('#grid .g-cell[data-r="0"][data-c="0"]')
    expect(cell_a1).to_be_visible()
    cell_a1.dblclick()
    page.keyboard.insert_text("helllooooo")
    page.keyboard.press("Enter")

    # A2
    cell_a2 = page.locator('#grid .g-cell[data-r="1"][data-c="0"]')
    expect(cell_a2).to_be_visible()
    cell_a2.dblclick()
    page.keyboard.insert_text("hiiiii")
    page.keyboard.press("Enter")

    # Verify values
    expect(cell_a1).to_have_text("helllooooo")
    expect(cell_a2).to_have_text("hiiiii")

    cell_a3 = page.locator('#grid .g-cell[data-r="1"][data-c="1"]')
    cell_a3.dblclick()
    
    page.locator('a.brand[href="/"]').click()
    expect(page).to_have_url(
        "https://tools.nativeoffice.online/"
    )