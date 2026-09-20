# AI Healing Log

## 2026-09-20

- [tests/test_nav.py](../tests/test_nav.py): `#hero-create` / `#modal-shell` create flow and stale button names → current public home-page create buttons (`Create new` + `Document Write & collaborate`, `Spreadsheet Data & formulas`, `Presentation Slides that land`, `Design Posters & posts`) with accessible-role selectors. Reason: live NativeOffice homepage structure no longer exposes the older workspace-only IDs. Status: AI-HEALED
- [tests/test_doc.py](../tests/test_doc.py): `page.get_by_role("button", name="doc")` → `Create new` → `Document Write & collaborate`, and updated editor target to the current editor. Reason: the old document entry button and editor selector were stale against the live app. Status: AI-HEALED
- [tests/test_design.py](../tests/test_design.py): `.sl-paint` / old design-create entry → `Create new` → `Design Posters & posts` and a neutral canvas click to start editing. Reason: the app’s design flow has changed from the earlier canvas-specific selectors. Status: AI-HEALED
- [tests/test_ppt.py](../tests/test_ppt.py): `Presentation A widescreen` + literal `Click to add title` text → `Presentation Slides that land` + regex fallback for title placeholder text. Reason: current presenter landing flow and placeholder text differ from the old automation. Status: AI-HEALED
- [tests/test_sheets.py](../tests/test_sheets.py): `#hero-create` / `#modal-shell` spreadsheet create flow → `Create new` + `Spreadsheet Data & formulas` role-based selector. Reason: workspace creation flow changed to a public accessible button flow. Status: AI-HEALED
