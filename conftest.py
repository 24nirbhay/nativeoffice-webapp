import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from importlib import import_module
from html import escape

import pytest
from qa.test_cases import CASES, get_case


pytest_html = import_module("pytest_html")
metadata_key = import_module("pytest_metadata.plugin").metadata_key
_ACTIVE_REPORT_DIR = None
_RUNTIME_RESULTS = {}


def _case_for_item(item):
    marker = item.get_closest_marker("test_case")
    if not marker or not marker.args:
        return None

    return get_case(str(marker.args[0]))


def _case_id_for_item(item):
    case = _case_for_item(item)
    return case.id if case else "UNLINKED"


def _report_dir() -> Path:
    """
    Directory supplied by CI for the current test module.
    Falls back to a timestamped local artifacts directory.
    """
    global _ACTIVE_REPORT_DIR

    if _ACTIVE_REPORT_DIR is not None:
        return _ACTIVE_REPORT_DIR

    path = os.getenv(
        "REPORT_DIR",
        f"artifacts/{datetime.now().strftime('%Y%m%d-%H%M%S')}",
    )

    directory = Path(path).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    _ACTIVE_REPORT_DIR = directory

    return directory


def _evidence_paths(report_dir):
    test_results_dir = report_dir / "test-results"
    if not test_results_dir.exists():
        return []

    evidence = []
    for path in sorted(test_results_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".png", ".zip", ".webm", ".txt"}:
            evidence.append(path.relative_to(report_dir).as_posix())

    return evidence


def _runtime_result(item, report):
    if report.passed:
        status = "PASS"
        actual_result = "Execution passed; pytest assertions completed."
    elif report.skipped:
        status = "SKIPPED"
        actual_result = f"NOT EXECUTED: {report.longreprtext or 'Test was skipped.'}"
    else:
        status = "FAIL" if report.when == "call" else "ERROR"
        detail = report.longreprtext.strip().splitlines()[-1] if report.longreprtext else "Pytest reported an execution failure."
        actual_result = f"{status}: {detail}"

    case = _case_for_item(item)
    return {
        "id": case.id if case else "UNLINKED",
        "status": status,
        "actual_result": actual_result,
        "phase": report.when,
        "automated_test_reference": case.automated_test_reference if case else item.nodeid,
        "evidence": _evidence_paths(_report_dir()),
    }


def _case_record(case, runtime):
    if runtime is None:
        status = (
            case.coverage_status
            if case.coverage_status != "Automated"
            else "NOT TESTED"
        )
        actual_result = (
            case.coverage_status
            if case.coverage_status != "Automated"
            else "NOT TESTED: This catalog case was not included in this pytest invocation."
        )
    else:
        status = runtime["status"]
        actual_result = runtime["actual_result"]

    record = {
        "id": case.id,
        "title": case.title,
        "module": case.module,
        "test_type": case.test_type,
        "objective": case.objective,
        "preconditions": list(case.preconditions),
        "steps": list(case.steps),
        "expected_result": case.expected_result,
        "actual_result": actual_result,
        "status": status,
        "severity": case.severity,
        "priority": case.priority,
        "automation_status": case.automation_status,
        "automated_test_reference": case.automated_test_reference,
        "supporting_evidence": case.supporting_evidence,
        "evidence": [],
    }

    if runtime:
        record["evidence"] = _evidence_paths(_report_dir())

    return record


def _classification(item):
    """
    Classification controlled by pytest markers.

    @pytest.mark.ui
    @pytest.mark.visual
    @pytest.mark.functional
    @pytest.mark.logic
    """

    if item.get_closest_marker("ui") or item.get_closest_marker("visual"):
        return "UI / Visual"

    if item.get_closest_marker("functional") or item.get_closest_marker("logic"):
        return "Functional / Logic"

    return "Functional / Logic"


def _impact(item):
    """
    Impact controlled by pytest markers.

    @pytest.mark.p1
    @pytest.mark.p3
    """

    if item.get_closest_marker("p1"):
        return "Critical / P1"

    return "Medium / P3"


def pytest_configure(config):
    config._qa_results = {}
    _report_dir()

    if hasattr(config, "stash"):
        config.stash[metadata_key]["Tester"] = "Peru"
        config.stash[metadata_key]["Application"] = "NativeOffice"
        config.stash[metadata_key]["Environment"] = "CI"
        config.stash[metadata_key]["Report Generated"] = (
            datetime.now(timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        )


def pytest_html_report_title(report):
    report.title = "NativeOffice QA Test Report"


def pytest_html_results_table_header(cells):
    cells.insert(
        2,
        '<th class="qa-case-header">Test Case</th>',
    )

    cells.insert(
        3,
        '<th class="qa-area-header">Area</th>',
    )

    cells.insert(
        4,
        '<th class="qa-impact-header">Impact</th>',
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    report.area = _classification(item)
    report.impact = _impact(item)
    case = _case_for_item(item)
    report.case_id = case.id if case else "UNLINKED"
    report.case_title = case.title if case else "No catalog link"
    report.priority = case.priority if case else "Unassigned"
    report.severity = case.severity if case else "Unassigned"
    report.test_type = case.test_type if case else "Unclassified"

    extras = getattr(report, "extras", [])

    if case and report.when == "call":
        runtime = _runtime_result(item, report)
        item.config._qa_results[case.id] = runtime
        _RUNTIME_RESULTS[case.id] = runtime
        extras.append(
            pytest_html.extras.text(
                f"{case.id} | {case.title} | {case.test_type}",
                name="Test Case",
            )
        )
        extras.append(
            pytest_html.extras.text(
                f"{case.priority} | {case.severity}",
                name="Priority / Severity",
            )
        )

    if report.when == "call" and report.failed:

        report_dir = _report_dir()

        screenshot_dir = report_dir / "screenshots"
        screenshot_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        safe_name = (
            item.nodeid
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            .replace("[", "_")
            .replace("]", "_")
        )

        screenshot_path = screenshot_dir / f"{safe_name}.png"

        page = item.funcargs.get("page")

        # --------------------------------------------------
        # FAILURE SCREENSHOT
        # --------------------------------------------------

        if page:
            try:
                screenshot_bytes = page.screenshot(
                    full_page=True
                )

                screenshot_path.write_bytes(
                    screenshot_bytes
                )

                encoded = base64.b64encode(
                    screenshot_bytes
                ).decode("utf-8")

                extras.append(
                    pytest_html.extras.image(
                        encoded,
                        mime_type="image/png",
                        extension="png",
                        name="Failure Screenshot",
                    )
                )

            except Exception as exc:
                extras.append(
                    pytest_html.extras.text(
                        f"Screenshot capture failed: {exc}",
                        name="Screenshot Error",
                    )
                )

        # --------------------------------------------------
        # PLAYWRIGHT FAILURE EVIDENCE
        # --------------------------------------------------

        test_results_dir = report_dir / "test-results"

        if test_results_dir.exists():

            # Failure screenshots generated by Playwright
            screenshots = list(
                test_results_dir.rglob("test-failed-*.png")
            )

            for screenshot in screenshots:

                relative_path = screenshot.relative_to(
                    report_dir
                ).as_posix()

                extras.append(
                    pytest_html.extras.html(
                        f"""
                        <div class="qa-evidence">
                            <a
                                href="{relative_path}"
                                target="_blank"
                                class="qa-button"
                            >
                                {escape(report.case_id)}: View Playwright Screenshot
                            </a>
                        </div>
                        """
                    )
                )

            # Playwright traces
            traces = list(
                test_results_dir.rglob("trace.zip")
            )

            for trace in traces:

                relative_path = trace.relative_to(
                    report_dir
                ).as_posix()

                extras.append(
                    pytest_html.extras.html(
                        f"""
                        <div class="qa-evidence">
                            <a
                                href="{relative_path}"
                                target="_blank"
                                class="qa-button"
                            >
                                {escape(report.case_id)}: Open Playwright Trace
                            </a>
                        </div>
                        """
                    )
                )

        # Evidence path
        if screenshot_path.exists():
            extras.append(
                pytest_html.extras.text(
                    screenshot_path.relative_to(
                        report_dir
                    ).as_posix(),
                    name="Evidence Path",
                )
            )

    report.extras = extras


def pytest_sessionfinish(session, exitstatus):
    report_dir = _report_dir()
    runtime_results = getattr(session.config, "_qa_results", {})
    records = [
        _case_record(case, runtime_results.get(case.id))
        for case in CASES.values()
    ]

    manifest = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "exit_status": exitstatus,
        "cases": records,
    }
    (report_dir / "qa-test-case-results.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def pytest_html_results_table_row(report, cells):

    area_class = (
        "qa-ui"
        if report.area == "UI / Visual"
        else "qa-functional"
    )

    impact_class = (
        "qa-critical"
        if report.impact == "Critical / P1"
        else "qa-medium"
    )

    evidence_links = ""
    if report.failed:
        evidence_links = "<br>".join(
            f'<a href="{escape(path)}" target="_blank">{escape(path)}</a>'
            for path in _evidence_paths(_report_dir())
        )

    cells.insert(
        2,
        f"""
        <td>
            <strong>{escape(report.case_id)}</strong><br>
            <small>{escape(report.case_title)}</small><br>
            <small>{escape(report.test_type)}</small>
            {f'<br><small>{evidence_links}</small>' if evidence_links else ''}
        </td>
        """,
    )

    cells.insert(
        3,
        f"""
        <td>
            <span class="qa-badge {area_class}">
                {report.area}
            </span>
        </td>
        """,
    )

    cells.insert(
        4,
        f"""
        <td>
            <span class="qa-badge {impact_class}">
                {report.impact}
            </span>
        </td>
        """,
    )


def pytest_html_results_summary(prefix, summary, postfix):
    counts = {
        "PASS": 0,
        "FAIL": 0,
        "ERROR": 0,
        "SKIPPED": 0,
        "NOT TESTED / COVERAGE GAP": 0,
    }
    rows = []

    for case in CASES.values():
        runtime = _RUNTIME_RESULTS.get(case.id)
        status = runtime["status"] if runtime else "NOT TESTED"
        actual_result = runtime["actual_result"] if runtime else "NOT TESTED"
        counts[status] = counts.get(status, 0) + 1
        evidence = ""
        if runtime:
            runtime["evidence"] = _evidence_paths(_report_dir())
        if runtime and runtime["evidence"]:
            evidence = "<br>".join(
                f'<a href="{escape(path)}" target="_blank">{escape(path)}</a>'
                for path in runtime["evidence"]
            )
        rows.append(
            f"""
            <tr>
                <td><strong>{escape(case.id)}</strong></td>
                <td>{escape(case.title)}<br><small>{escape(case.objective)}</small></td>
                <td>{escape(case.test_type)}</td>
                <td>{escape(case.severity)}</td>
                <td>{escape(case.priority)}</td>
                <td><strong>{escape(status)}</strong><br><small>{escape(actual_result)}</small></td>
                <td>{escape(case.automated_test_reference) or "Not automated"}</td>
                <td>{evidence or "None"}</td>
            </tr>
            """
        )

    overview = f"""
    <section class="qa-overview">
        <h2>QA Overview</h2>
        <p>Human test-case design linked to the automated pytest execution.</p>
        <div class="qa-counts">
            <span class="qa-count qa-pass">PASS <strong>{counts["PASS"]}</strong></span>
            <span class="qa-count qa-fail">FAIL <strong>{counts["FAIL"]}</strong></span>
            <span class="qa-count qa-error">ERROR <strong>{counts["ERROR"]}</strong></span>
            <span class="qa-count qa-gap">NOT TESTED <strong>{counts.get("NOT TESTED", 0) + counts["NOT TESTED / COVERAGE GAP"]}</strong></span>
        </div>
        <div class="qa-table-wrap">
            <table class="qa-coverage-table">
                <thead>
                    <tr>
                        <th>Test Case</th>
                        <th>Scenario</th>
                        <th>Type</th>
                        <th>Severity</th>
                        <th>Priority</th>
                        <th>Status / Actual Result</th>
                        <th>Automated Test Reference</th>
                        <th>Evidence</th>
                    </tr>
                </thead>
                <tbody>{"".join(rows)}</tbody>
            </table>
        </div>
    </section>
    """

    prefix.extend(
        [
            overview,
            """
            <style>

                /* -----------------------------------------
                   NativeOffice QA report
                ----------------------------------------- */

                body {
                    font-family:
                        Inter,
                        -apple-system,
                        BlinkMacSystemFont,
                        "Segoe UI",
                        Arial,
                        sans-serif !important;

                    background: #f6f7fb !important;
                    color: #111827 !important;
                }

                h1 {
                    font-weight: 750 !important;
                    letter-spacing: -0.5px;
                }

                /* Metadata / summary area */

                .qa-header {
                    margin: 20px 0 24px;
                    padding: 22px 24px;
                    border: 1px solid #e5e7eb;
                    border-radius: 16px;
                    background: #ffffff;
                    box-shadow:
                        0 4px 18px rgba(15, 23, 42, 0.05);
                }

                .qa-title {
                    margin: 0 0 6px;
                    font-size: 20px;
                    font-weight: 750;
                    color: #111827;
                }

                .qa-subtitle {
                    margin: 0;
                    color: #6b7280;
                    font-size: 13px;
                }

                .qa-status {
                    display: inline-flex;
                    align-items: center;
                    gap: 7px;
                    margin-top: 14px;
                    padding: 7px 11px;
                    border-radius: 999px;
                    background: #f3f4f6;
                    color: #374151;
                    font-size: 12px;
                    font-weight: 700;
                }

                .qa-overview {
                    margin: 20px 0 24px;
                    padding: 22px 24px;
                    border: 1px solid #e5e7eb;
                    border-radius: 16px;
                    background: #ffffff;
                    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.05);
                }

                .qa-overview h2 {
                    margin: 0 0 5px;
                    font-size: 18px;
                }

                .qa-overview p {
                    margin: 0 0 15px;
                    color: #6b7280;
                    font-size: 13px;
                }

                .qa-counts {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-bottom: 16px;
                }

                .qa-count {
                    padding: 6px 10px;
                    border-radius: 999px;
                    font-size: 11px;
                    font-weight: 700;
                }

                .qa-count strong {
                    margin-left: 4px;
                }

                .qa-pass { background: #ecfdf5; color: #047857; }
                .qa-fail, .qa-error { background: #fef2f2; color: #b91c1c; }
                .qa-gap { background: #fff7ed; color: #c2410c; }

                .qa-table-wrap {
                    overflow-x: auto;
                }

                .qa-coverage-table {
                    width: 100%;
                    min-width: 980px;
                    border-collapse: collapse;
                    box-shadow: none;
                }

                .qa-coverage-table th,
                .qa-coverage-table td {
                    padding: 9px;
                    border-bottom: 1px solid #eef0f4;
                    text-align: left;
                    vertical-align: top;
                }

                .qa-coverage-table small {
                    color: #6b7280;
                }

                .qa-dot {
                    width: 7px;
                    height: 7px;
                    border-radius: 50%;
                    background: #22c55e;
                }

                /* Table */

                table {
                    border-radius: 14px !important;
                    overflow: hidden;
                    border: 1px solid #e5e7eb !important;
                    box-shadow:
                        0 4px 18px rgba(15, 23, 42, 0.04);
                }

                th {
                    background: #f9fafb !important;
                    font-size: 12px !important;
                    font-weight: 700 !important;
                    color: #6b7280 !important;
                }

                td {
                    font-size: 13px !important;
                }

                tr:hover td {
                    background: #fafafa !important;
                }

                /* QA badges */

                .qa-badge {
                    display: inline-block;
                    padding: 5px 9px;
                    border-radius: 999px;
                    font-size: 11px;
                    font-weight: 700;
                    white-space: nowrap;
                }

                .qa-ui {
                    background: #eef2ff;
                    color: #4338ca;
                }

                .qa-functional {
                    background: #ecfdf5;
                    color: #047857;
                }

                .qa-critical {
                    background: #fef2f2;
                    color: #b91c1c;
                }

                .qa-medium {
                    background: #fff7ed;
                    color: #c2410c;
                }

                /* Failure evidence */

                .qa-evidence {
                    margin: 8px 0;
                }

                .qa-button {
                    display: inline-block;
                    padding: 8px 12px;
                    border-radius: 9px;
                    background: #111827;
                    color: #ffffff !important;
                    text-decoration: none !important;
                    font-size: 12px;
                    font-weight: 650;
                    transition: opacity 0.15s ease;
                }

                .qa-button:hover {
                    opacity: 0.8;
                }

                code {
                    border-radius: 5px;
                    padding: 2px 5px;
                    background: #f3f4f6;
                }

            </style>

            <div class="qa-header">

                <div class="qa-title">
                    NativeOffice QA
                </div>

                <p class="qa-subtitle">
                    Automated Playwright / Pytest test execution
                </p>

                <div class="qa-status">
                    <span class="qa-dot"></span>
                    Failure evidence enabled
                </div>

            </div>
            """
        ]
    )