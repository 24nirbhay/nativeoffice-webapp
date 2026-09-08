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
    expect(cell_a3).to_be_visible()
    cell_a3.dblclick()
    page.keyboard.insert_text("=2+2")
    page.keyboard.press("Enter")
    expect(cell_a3).to_have_text("4")


    longahhstring = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem."

    cell_a4 = page.locator('#grid .g-cell[data-r="12"][data-c="9"]')
    expect(cell_a4).to_be_visible()

    cell_a4.dblclick()
    page.keyboard.insert_text(longahhstring)
    page.keyboard.press("Enter")

    expect(cell_a4).to_have_text(longahhstring)



    page.locator('a.brand[href="/"]').click()
    expect(page).to_have_url(
        "https://tools.nativeoffice.online/"
    )