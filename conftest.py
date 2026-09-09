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
                :root {
                    --qa-ink: #172033;
                    --qa-muted: #687386;
                    --qa-line: #dfe5ee;
                    --qa-surface: #ffffff;
                    --qa-canvas: #f3f6fa;
                    --qa-accent: #e85d3f;
                    --qa-shadow: 0 12px 30px rgba(23, 32, 51, 0.07);
                }

                body {
                    min-width: 0 !important;
                    margin: 0 auto !important;
                    padding: 28px clamp(14px, 3vw, 42px) 48px !important;
                    max-width: 1480px;
                    font-family: "Avenir Next", "Segoe UI", sans-serif !important;
                    background: var(--qa-canvas) !important;
                    color: var(--qa-ink) !important;
                    line-height: 1.45;
                }

                h1 {
                    font-size: clamp(24px, 3vw, 34px) !important;
                    font-weight: 800 !important;
                    letter-spacing: -0.8px;
                }

                .qa-header,
                .qa-overview {
                    margin: 18px 0 22px;
                    padding: clamp(18px, 3vw, 28px);
                    border: 1px solid var(--qa-line);
                    border-radius: 18px;
                    background: var(--qa-surface);
                    box-shadow: var(--qa-shadow);
                }

                .qa-header {
                    position: relative;
                    overflow: hidden;
                    border-top: 4px solid var(--qa-accent);
                }

                .qa-title {
                    margin: 0 0 6px;
                    color: var(--qa-ink);
                    font-size: 22px;
                    font-weight: 800;
                    letter-spacing: -0.4px;
                }

                .qa-subtitle,
                .qa-overview p,
                .qa-coverage-table small {
                    color: var(--qa-muted);
                    font-size: 13px;
                }

                .qa-subtitle { margin: 0; }

                .qa-status {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    margin-top: 16px;
                    padding: 7px 11px;
                    border: 1px solid #cce9db;
                    border-radius: 999px;
                    background: #effaf4;
                    color: #18734a;
                    font-size: 12px;
                    font-weight: 750;
                }

                .qa-overview h2 {
                    margin: 0 0 5px;
                    font-size: 20px;
                    letter-spacing: -0.3px;
                }

                .qa-overview p { margin: 0 0 17px; }

                .qa-counts {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 9px;
                    margin-bottom: 20px;
                }

                .qa-count,
                .qa-badge {
                    display: inline-flex;
                    align-items: center;
                    width: fit-content;
                    padding: 6px 10px;
                    border-radius: 999px;
                    font-size: 11px;
                    font-weight: 750;
                    white-space: nowrap;
                }

                .qa-count strong { margin-left: 5px; }
                .qa-pass, .qa-functional { background: #e9f8ef; color: #18734a; }
                .qa-fail, .qa-error, .qa-critical { background: #ffebe8; color: #b33a2c; }
                .qa-gap, .qa-medium { background: #fff3dc; color: #9a5b08; }
                .qa-ui { background: #eeeafd; color: #5b45a8; }

                .qa-table-wrap { overflow-x: auto; }

                .qa-coverage-table {
                    width: 100%;
                    min-width: 980px;
                    border-collapse: separate;
                    border-spacing: 0;
                    box-shadow: none;
                }

                .qa-coverage-table th,
                .qa-coverage-table td {
                    padding: 12px 11px;
                    border-bottom: 1px solid #edf0f4;
                    text-align: left;
                    vertical-align: top;
                }

                .qa-dot {
                    width: 7px;
                    height: 7px;
                    border-radius: 50%;
                    background: #2fb673;
                    box-shadow: 0 0 0 4px #dff5e8;
                }

                table {
                    border: 1px solid var(--qa-line) !important;
                    border-radius: 14px !important;
                    overflow: hidden;
                    box-shadow: 0 8px 22px rgba(23, 32, 51, 0.04);
                }

                th {
                    background: #f7f9fc !important;
                    color: var(--qa-muted) !important;
                    font-size: 11px !important;
                    font-weight: 800 !important;
                    letter-spacing: 0.04em;
                    text-transform: uppercase;
                }

                td { font-size: 13px !important; }
                tr:hover td { background: #fbfcfe !important; }

                .qa-evidence { margin: 8px 0; }

                .qa-button {
                    display: inline-block;
                    padding: 8px 12px;
                    border: 1px solid #27334a;
                    border-radius: 9px;
                    background: #27334a;
                    color: #ffffff !important;
                    text-decoration: none !important;
                    font-size: 12px;
                    font-weight: 700;
                }

                .qa-button:hover { background: var(--qa-accent); border-color: var(--qa-accent); }

                code {
                    border: 1px solid var(--qa-line);
                    border-radius: 5px;
                    padding: 2px 5px;
                    background: #f7f9fc;
                    color: #b33a2c;
                }

                @media (max-width: 640px) {
                    body { padding: 16px 10px 30px !important; }
                    .qa-header, .qa-overview { border-radius: 14px; padding: 16px; }
                    .qa-title { font-size: 19px; }
                    .qa-count { flex: 1 1 calc(50% - 9px); justify-content: space-between; }
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