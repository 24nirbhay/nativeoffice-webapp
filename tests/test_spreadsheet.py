from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")

    # ==================== OPEN SPREADSHEET ====================

    page.get_by_role(
        "button",
        name="Spreadsheet Analyze data and"
    ).click()

    grid = page.locator("#grid")
    expect(grid).to_be_visible()

    # ==================== CELL LOCATORS ====================

    def cell(row: int, col: int):
        return page.locator(
            f'#grid .g-cell[data-r="{row}"][data-c="{col}"]'
        )

    # ==================== CREATE DATA TABLE ====================

    # A1 - Header
    cell(0, 0).click()
    page.keyboard.type("hello")
    page.keyboard.press("Enter")

    # B1 - Header
    cell(0, 1).click()
    page.keyboard.type("amount")
    page.keyboard.press("Enter")

    # B2:B7 - Amount values
    values = ["15", "20", "67", "200", "36", "78"]

    for row, value in enumerate(values, start=1):
        cell(row, 1).click()
        page.keyboard.type(value)
        page.keyboard.press("Enter")

    # ==================== VERIFY DATA ====================

    expect(cell(0, 0)).to_contain_text("hello")
    expect(cell(0, 1)).to_contain_text("amount")

    for row, value in enumerate(values, start=1):
        expect(cell(row, 1)).to_contain_text(value)

    # ==================== BORDERS ====================

    # Apply borders to header cells
    cell(0, 0).click()
    page.get_by_role("button", name="Borders").click()
    page.get_by_role("menuitem", name="All borders").click()

    cell(0, 1).click()
    page.get_by_role("button", name="Borders").click()
    page.get_by_role("menuitem", name="All borders").click()

    # ==================== NUMBER FORMATTING ====================

    # 15 → 15.0
    cell(1, 1).click()
    page.get_by_role("button", name=".0", exact=True).click()

    # 20 → 20.0
    cell(2, 1).click()
    page.get_by_role("button", name=".0", exact=True).click()

    # Remaining values → two decimals
    for row in range(3, 7):
        cell(row, 1).click()
        page.get_by_role("button", name=".00").click()

    # ==================== CELL FILL COLOURS ====================

    # A1
    cell(0, 0).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#ffff00").click()

    # B1
    cell(0, 1).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#4a86e8").click()

    # B2
    cell(1, 1).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#d5a6bd").click()

    # B3
    cell(2, 1).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#a4c2f4").click()

    # B4
    cell(3, 1).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#ff00ff").click()

    # B5
    cell(4, 1).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#ffffff").click()

    # B6
    cell(5, 1).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#ffd966").click()

    # B7
    cell(6, 1).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#ffe599").click()

    # Additional fill-colour test
    cell(3, 1).click()
    page.get_by_role("button", name="Fill colour").click()
    page.get_by_role("button", name="#00ffff").click()

    # ==================== TEXT FORMATTING ====================

    # Bold B6
    cell(5, 1).click()
    page.get_by_role(
        "button",
        name="B",
        description="Bold (Ctrl+B)"
    ).click()

    # Bold B7
    cell(6, 1).click()
    page.get_by_role(
        "button",
        name="B",
        description="Bold (Ctrl+B)"
    ).click()

    # Italic B3
    cell(2, 1).click()
    page.get_by_role(
        "button",
        name="I",
        description="Italic (Ctrl+I)"
    ).click()

    # Strikethrough B2
    cell(1, 1).click()
    page.get_by_role(
        "button",
        name="S",
        description="Strikethrough"
    ).click()

    # ==================== HORIZONTAL ALIGNMENT ====================

    # B2 → Right
    cell(1, 1).click()
    page.get_by_role("button", name="Horizontal align").click()
    page.get_by_role("menuitem", name="Right").click()

    # A1 → Centre
    cell(0, 0).click()
    page.get_by_role("button", name="Horizontal align").click()
    page.get_by_role("menuitem", name="Centre").click()

    # B1 → Left
    cell(0, 1).click()
    page.get_by_role("button", name="Horizontal align").click()
    page.get_by_role("menuitem", name="Left").click()

    # ==================== FUNCTIONS ====================

    # Select cells below the table for function testing.
    # These intentionally test the function toolbar.

    # SUM
    cell(7, 1).click()
    page.get_by_role("button", name="Functions").click()
    page.get_by_role("menuitem", name="SUM").click()

    # AVERAGE
    cell(8, 1).click()
    page.get_by_role("button", name="Functions").click()
    page.get_by_role("menuitem", name="AVERAGE").click()

    # COUNT
    cell(9, 1).click()
    page.get_by_role("button", name="Functions").click()
    page.get_by_role("menuitem", name="COUNT").click()

    # MAX
    cell(10, 1).click()
    page.get_by_role("button", name="Functions").click()
    page.get_by_role("menuitem", name="MAX").click()

    # ==================== INSERT CHART ====================

    page.get_by_role("button", name="Insert chart").click()

    # ==================== APPLICATION MENUS ====================

    page.get_by_role("button", name="Edit").click()
    page.get_by_role("button", name="View").click()

    page.get_by_role(
        "button",
        name="Insert",
        exact=True
    ).click()

    page.get_by_role(
        "button",
        name="Format",
        exact=True
    ).click()

    page.get_by_role("button", name="Data").click()
    page.get_by_role("button", name="Tools").click()
    page.get_by_role("button", name="Extensions").click()
    page.get_by_role("button", name="Help").click()

    # ==================== RETURN HOME ====================

    page.get_by_role(
        "link",
        name="NativeOffice"
    ).click()