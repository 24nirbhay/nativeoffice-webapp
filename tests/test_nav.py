import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")
    page.get_by_role("button", name="Close navigation").click()
    page.get_by_role("button", name="Workspace appearance").click()
    page.get_by_role("button", name="Soft Warm and calm").click()
    page.get_by_role("button", name="Dark Low light focus").click()
    page.get_by_role("button", name="Compact More on screen").click()
    page.get_by_role("button", name="Use #d8437a").click()
    page.get_by_role("button", name="Use #078b78").click()
    page.get_by_role("button", name="Use #315fe8").click()
    page.get_by_role("button", name="Use #5746f6").click()
    page.get_by_role("button", name="Use #315fe8").click()
    page.get_by_role("button", name="Done").click()
    page.get_by_role("button", name="Create New").click()
    page.get_by_role("button", name="Document A clean writing page").click()
    page.get_by_role("paragraph").filter(has_text=re.compile(r"^$")).click()
    page.locator("#editor").get_by_role("textbox").fill("hello")
    page.get_by_role("button", name="Share").click()
    expect(page.locator("#share-scrim")).to_be_visible()
    expect(page.get_by_role("heading", name="Share this document")).to_be_visible()
    page.get_by_role("button", name="Done").click()
    expect(page.locator("#share-scrim")).not_to_be_visible()
    page.get_by_role("link", name="NativeOffice").click()
#ye bc create new sheet
    page.locator("#hero-create").click()

    modal = page.locator("#modal-shell")

    sheet = modal.locator('[data-create-kind="sheet"]')
    expect(sheet).to_be_visible()
    expect(sheet).to_be_enabled()

    sheet.click()

# Verify spreadsheet opened
    grid = page.locator("#grid")
    expect(grid).to_be_visible(timeout=15000)

# Select a cell
    cell = page.locator(".g-cell").first
    expect(cell).to_be_visible()
    cell.click()

# Enter a value
    page.keyboard.type("hello")
    page.keyboard.press("Enter")
#sheet end

    page.get_by_role("button", name="Share").click()
    expect(page.locator("#share-scrim")).to_be_visible()
    page.get_by_role("button", name="Done").click()
    page.get_by_role("link", name="NativeOffice").click()


    #ppt---------------------------------------
    page.locator("#hero-create").click()

    modal = page.locator("#modal-shell")
    expect(modal).to_be_visible()
    expect(modal).to_be_enabled()

    presentation= modal.locator('[data-create-kind="slides"]')
    presentation.click()

# Verify presentation editor opened
    expect(page.get_by_text("Click to add title")).to_be_visible(timeout=15000)

# Select title and subtitle areas
    page.get_by_text("Click to add title").click()
    page.get_by_text("Click to add subtitle").click()

#ppt end -----------------------------------------

    #design---------------------------------------
    page.get_by_role("button", name="Share").click()
    page.get_by_role("button", name="Done").click()
    page.get_by_role("link", name="NativeOffice").click()

    page.locator("#hero-create").click()

    modal = page.locator("#modal-shell")

    design = modal.locator('[data-create-kind="design"]')
    expect(design).to_be_visible()
    expect(design).to_be_enabled()

    design.click()
    #_----------------------
    
    page.locator(".sl-paint > .sl-bg").click()
    page.locator(".sl-paint > .sl-bg").click()


    #design end---------------------------


    
