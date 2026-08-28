from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")

    # ==================== OPEN PRESENTATION ====================

    page.get_by_role(
        "button",
        name="Presentation Design stunning"
    ).click()

    # ==================== TITLE ====================

    title = page.get_by_text("Click to add title")
    expect(title).to_be_visible()

    title.dblclick()

    editor = page.locator(".sl-editor")
    expect(editor).to_be_visible()
    expect(editor).to_be_editable()

    editor.fill("hello this is a test")
    expect(editor).to_contain_text("hello this is a test")

    # ==================== SUBTITLE ====================

    subtitle = page.get_by_text("Click to add subtitle")
    expect(subtitle).to_be_visible()

    subtitle.dblclick()

    expect(editor).to_be_visible()
    editor.fill("playwright")
    expect(editor).to_contain_text("playwright")

    # ==================== SLIDE CANVAS ====================

    canvas = page.locator(".sl-paint")
    expect(canvas).to_be_visible()