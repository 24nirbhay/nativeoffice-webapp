from dataclasses import dataclass
from typing import Callable, Dict, Tuple, TypeVar

import pytest


__test__ = False
F = TypeVar("F", bound=Callable)


@dataclass(frozen=True)
class TestCase:
    id: str
    title: str
    module: str
    test_type: str
    objective: str
    preconditions: Tuple[str, ...]
    steps: Tuple[str, ...]
    expected_result: str
    severity: str
    priority: str
    automation_status: str
    automated_test_reference: str = ""
    supporting_evidence: str = "Failure screenshot and Playwright trace when execution fails."
    coverage_status: str = "Automated"


def test_case(case_id: str) -> Callable[[F], F]:
    """Link a pytest function to one stable catalog ID."""

    return pytest.mark.test_case(case_id)


CASES: Dict[str, TestCase] = {
    "TC-NAV-001": TestCase(
        id="TC-NAV-001",
        title="Navigate workspace and create supported file types",
        module="Navigation",
        test_type="Functional",
        objective="Verify primary workspace navigation and entry points for documents, spreadsheets, presentations, and designs.",
        preconditions=("NativeOffice is available.", "User is on the home workspace."),
        steps=(
            "Open workspace navigation views and utility controls.",
            "Open the create dialog for each supported file type.",
            "Return home and close the create dialog.",
        ),
        expected_result="Each navigation view and create option is available, opens successfully, and returns to the home workspace.",
        severity="Medium",
        priority="P2",
        automation_status="Automated",
        automated_test_reference="tests/test_nav.py::test_nav",
    ),
    "TC-DOC-001": TestCase(
        id="TC-DOC-001",
        title="Edit and format document content",
        module="Documents",
        test_type="Functional",
        objective="Verify common document editing, formatting, sharing, and menu workflows.",
        preconditions=("NativeOffice is available.", "A new document can be opened."),
        steps=(
            "Open a document and enter text.",
            "Apply text formatting, alignment, spacing, lists, indentation, styles, font, and font size.",
            "Open and close document sharing.",
            "Open the primary document menus.",
        ),
        expected_result="Document content accepts the editing actions, formatting controls respond, sharing opens and closes, and menus are available.",
        severity="High",
        priority="P1",
        automation_status="Automated",
        automated_test_reference="tests/test_doc.py::test_doc",
    ),
    "TC-SHEET-001": TestCase(
        id="TC-SHEET-001",
        title="Enter spreadsheet values and calculate a formula",
        module="Spreadsheets",
        test_type="Functional",
        objective="Verify spreadsheet creation, cell editing, formula evaluation, long text entry, and return navigation.",
        preconditions=("NativeOffice is available.", "A spreadsheet can be created from the home workspace."),
        steps=(
            "Create a spreadsheet.",
            "Enter values in multiple cells and verify them.",
            "Enter a formula and verify the calculated value.",
            "Enter a long value and return to the home workspace.",
        ),
        expected_result="Cell values persist after entry, the formula evaluates to 4, long text is accepted, and navigation returns home.",
        severity="High",
        priority="P1",
        automation_status="Automated",
        automated_test_reference="tests/test_sheets.py::test_sheets",
    ),
    "TC-PPT-001": TestCase(
        id="TC-PPT-001",
        title="Create and edit a presentation with image insertion",
        module="Presentations",
        test_type="Functional / UI",
        objective="Verify presentation creation, slide editing, slide deletion, and image insertion dialog behavior.",
        preconditions=("NativeOffice is available.", "A presentation can be created."),
        steps=(
            "Create a widescreen presentation.",
            "Enter title and subtitle content.",
            "Add slides and delete one slide from its context menu.",
            "Open image insertion and submit an image address.",
        ),
        expected_result="Presentation content can be edited, slides can be added and deleted, and the image insertion workflow accepts the address.",
        severity="Medium",
        priority="P2",
        automation_status="Automated",
        automated_test_reference="tests/test_ppt.py::test_ppt",
    ),
    "TC-DESIGN-001": TestCase(
        id="TC-DESIGN-001",
        title="Use design themes, pages, elements, and text tools",
        module="Design",
        test_type="UI / Visual",
        objective="Verify design canvas themes, backgrounds, pages, asset tabs, shapes, and text controls are usable.",
        preconditions=("NativeOffice is available.", "A design canvas can be created."),
        steps=(
            "Create a square design canvas.",
            "Change themes and background colors.",
            "Add pages and browse design, photo, element, and text controls.",
            "Add shapes and text tools, then return home.",
        ),
        expected_result="Design controls open and apply selections, pages can be added, and the user can return to the home workspace.",
        severity="Medium",
        priority="P3",
        automation_status="Automated",
        automated_test_reference="tests/test_design.py::test_design",
    ),
    "TC-DOC-NEG-001": TestCase(
        id="TC-DOC-NEG-001",
        title="Reject invalid or empty document input",
        module="Documents",
        test_type="Negative / Error handling",
        objective="Verify empty submissions and invalid formatting input produce a clear, recoverable response.",
        preconditions=("A document editor is open.",),
        steps=("Submit empty content.", "Enter invalid formatting input.", "Observe validation and recovery behavior."),
        expected_result="Invalid input is rejected or safely handled without data loss, with an understandable user response.",
        severity="Medium",
        priority="P2",
        automation_status="Not automated",
        coverage_status="NOT TESTED / COVERAGE GAP",
    ),
    "TC-SHEET-EDGE-001": TestCase(
        id="TC-SHEET-EDGE-001",
        title="Handle spreadsheet boundaries and invalid formulas",
        module="Spreadsheets",
        test_type="Boundary / Negative",
        objective="Verify empty cells, invalid formulas, boundary coordinates, duplicate edits, and rapid interaction.",
        preconditions=("A spreadsheet is open.",),
        steps=("Use empty and boundary cells.", "Submit invalid and duplicate formulas.", "Repeat edits rapidly."),
        expected_result="The spreadsheet remains responsive and reports invalid operations without corrupting valid data.",
        severity="High",
        priority="P1",
        automation_status="Not automated",
        coverage_status="NOT TESTED / COVERAGE GAP",
    ),
    "TC-SHEET-PERSIST-001": TestCase(
        id="TC-SHEET-PERSIST-001",
        title="Preserve spreadsheet data after refresh",
        module="Spreadsheets",
        test_type="Persistence / Recovery",
        objective="Verify saved spreadsheet values and formulas remain available after refresh or a repeated open workflow.",
        preconditions=("A spreadsheet contains saved values.",),
        steps=("Refresh the page.", "Reopen the spreadsheet.", "Compare values and formulas with the saved state."),
        expected_result="Previously saved content is restored accurately after refresh and reopen.",
        severity="High",
        priority="P1",
        automation_status="Not automated",
        coverage_status="NOT TESTED / COVERAGE GAP",
    ),
    "TC-UI-RESP-001": TestCase(
        id="TC-UI-RESP-001",
        title="Use NativeOffice on a mobile viewport",
        module="Responsive UI",
        test_type="Responsive / UI",
        objective="Verify key navigation and creation workflows remain usable on a narrow mobile viewport.",
        preconditions=("NativeOffice is available.", "A mobile viewport is configured."),
        steps=("Open the home workspace on mobile.", "Navigate and open the create workflow.", "Check controls, dialogs, and scrolling."),
        expected_result="Primary controls remain visible, usable, and free of blocking overlap on mobile.",
        severity="Medium",
        priority="P2",
        automation_status="Not automated",
        coverage_status="NOT TESTED / COVERAGE GAP",
    ),
}


def get_case(case_id: str) -> TestCase:
    return CASES[case_id]