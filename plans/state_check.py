#!/usr/bin/env python3
"""Re-derive the frozen round-24 current-state assertions offline (round 25, C2).

Population P2 (plans/round-25-claims.md §C2 + Amendment 1) is frozen at base
6180e4f: SCORECARD capabilities (P2a) and round-24 axis table (P2b), SHONEN
canonical form (P2c, seed frozen in plans/fixtures/r25/shonen-seed.txt — PROTOCOL.md:439-448
verbatim, slice sha256 3962e6b8...; whole-file PROTOCOL.md sha256 886e459b... at freeze), PROVINCE ## Surfaces rows (P2d) and
corpus/README index rows both directions (P2e). A stale base assertion closed by
an appended dated correction is reported SUPERSEDED only when the correction's
own tokens re-derive. Exit 0 all comparable assertions match, 1 any mismatch,
2 usage / unreadable input / empty population (never a vacuous PASS).
Precedents cited, not rebuilt: kaidoku .ufo/gates/c1-census-v10.py (exit map,
silent-empty defect H1), souji citation-drift-probe.py (content-checked
anchors), kotoba verify_corpus_integrity.py and kengaku
corpus/evidence/round13-coverage/coverage_census.py (README both directions).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

LANE_NAME = "kengaku-shokunin"

CAPABILITY_IDS = (
    "offline-replay-gate",
    "frozen-table-pin-check",
    "sources-registry",
)
AXIS_IDS = (
    "novelty",
    "calibration",
    "depth",
    "coverage",
    "operability",
    "freshness",
    "adjacency",
)
SURFACE_IDS = (
    "Research notes (SSOT for eval craft)",
    "Local benchmark battery",
    "Served local model",
    "Route telemetry",
    "Client CLI telemetry",
    "Model catalogs",
    "Own probe artifacts",
    "In-repo gate",
    "Public literature",
)

# Frozen from corpus/README.md's fixed index tables at 6180e4f. New entries in
# those tables, or new immediate children under these namespaces, are reported
# as out-of-population and are not silently admitted to P2e.
README_INDEX_PATHS = (
    "knowledge/benchmark-selection.md",
    "knowledge/godspeed-eval-findings.md",
    "knowledge/telemetry-run-design.md",
    "knowledge/local-model-index.md",
    "knowledge/local-bench-arena.md",
    "knowledge/ledger-route-telemetry.md",
    "knowledge/bench-arena-fresh-run.md",
    "knowledge/eval-theory-notes.md",
    "knowledge/gemini-benchmark-suite.md",
    "knowledge/bailian-cli-telemetry.md",
    "knowledge/bench-arena-round5-battery.md",
    "knowledge/open-model-catalogs.md",
    "knowledge/bench-arena-round6-stability.md",
    "knowledge/bench-arena-task27-timeout-anatomy.md",
    "knowledge/bench-arena-round7-scaffold-ablation.md",
    "knowledge/eval-design-digest-3.md",
    "knowledge/bench-arena-round7-noise-n25.md",
    "knowledge/eval-design-digest-2.md",
    "knowledge/bench-arena-round8-horizon.md",
    "knowledge/bench-arena-round9-replication.md",
    "knowledge/eval-prior-art-calibration.md",
    "knowledge/bench-arena-round11-power.md",
    "knowledge/bench-arena-round12-ladder.md",
    "knowledge/kimi-model-routing-round18.md",
    "knowledge/probe-battery-r19.md",
    "knowledge/attrib-prior-art-r21.md",
    "knowledge/attrib-r21.md",
    "knowledge/contamination-detection-and-transparency.md",
    "knowledge/llm-judge-calibration.md",
    "knowledge/benchmark-saturation-and-lifecycle.md",
    "knowledge/agent-time-horizon-and-task-validity.md",
    "knowledge/paired-eval-uncertainty-reporting.md",
    "lessons/round-1.md",
    "lessons/round-3.md",
    "lessons/round-4.md",
    "lessons/round-1-aggregator-audit.md",
    "lessons/round-5.md",
    "lessons/round-7.md",
    "lessons/round-4-aggregator-audit.md",
    "lessons/round-5-aggregator-audit.md",
    "lessons/round-8.md",
    "lessons/round-9.md",
    "lessons/round-11.md",
    "lessons/round-6-aggregator-audit.md",
    "lessons/round-8-aggregator-box3-coldrun.md",
    "lessons/round-12.md",
    "lessons/round-13.md",
    "lessons/round-14.md",
    "lessons/round-9-aggregator-corpus-verdict.md",
    "lessons/round-16-recensus.md",
    "lessons/round-13-coverage.md",
    "lessons/2026-10-16-round19-freeze-chain.md",
    "lessons/2026-10-16-round20-grid-closure.md",
    "lessons/2026-10-16-round21-attribution-freeze-surface.md",
    "lessons/2026-10-16-round22-leg-coverage-forcing.md",
    "lessons/2026-10-16-round23-stream-surface.md",
    "lessons/round-24.md",
    "evidence/round8-horizon/",
    "evidence/round9-replication/",
    "evidence/round9-fleet/",
    "evidence/round10-fleet/",
    "evidence/round11-power/",
    "evidence/round11-fleet/",
    "evidence/round12-ladder/",
    "evidence/round12-fleet/",
    "evidence/round13-ack-state/",
    "evidence/round14-fleet/",
    "evidence/round13-coverage/",
    "evidence/round18-kimi-routing/",
    "evidence/probe-r19-P1-key1-quota.log",
    "evidence/probe-r19-P2-servicetier.log",
    "evidence/probe-r19-P3.log",
    "evidence/probe-r19-P4-devinleg.log",
    "evidence/probe-r19-P4-glm.log",
    "evidence/probe-r19-P5-glm.log",
    "evidence/probe-r19-P6-zai.log",
    "evidence/probe-r19-P8-kimi-code-auth.log",
    "evidence/probe-r19-P9-absent-port.log",
    "evidence/probe-r19-devin-shim-seat.log",
    "evidence/probe-r19-hyper-predictions.log",
    "evidence/probe-r19-hyper.log",
    "evidence/probe-r19-opencode-health.log",
    "evidence/probe-r19-p1-listing-mismatch.log",
    "evidence/probe-r19-quota23.log",
    "evidence/probe-r19-shim-ds-predictions.log",
    "evidence/probe-r19-shim-ds-run.log",
    "evidence/probe-r19-shim-glm-predictions.log",
    "evidence/probe-r19-shim-glm-run.log",
    "evidence/attrib-r21-ds-trials.log",
    "evidence/attrib-r21-glm-trials.log",
    "evidence/attrib-r21-impl-ds-trials.log",
    "evidence/attrib-r21-impl-glm-trials.log",
    "evidence/attrib-r22-legs.log",
    "evidence/attrib-r22-legs-hyper.log",
    "evidence/attrib-r22-opencode-trials.log",
    "evidence/attrib-r23-stream-trials.log",
    "evidence/attrib-r23-stream.log",
    "evidence/round24-sources/",
    "evidence/round24-census/",
)
# The base file population includes this unindexed lesson, so file→row exposes
# its defect without admitting a new README row into the frozen row population.
README_FILE_PATHS = README_INDEX_PATHS + (
    "lessons/round-24-verifier-spotcheck.md",
)

FREEZE_CHECK_COMMAND = (
    "python3",
    "plans/attrib_probe.py",
    "freeze-check",
    "--frozen",
    "plans/attrib-r23-frozen.md",
)
ALLOWED_COMMANDS = {
    ("python3", "grader.py"),
    FREEZE_CHECK_COMMAND,
}

# P2a sources-registry: the evidence cell names no command, so the census is
# hardcoded (never parsed from SCORECARD text) and scoped to the base registry
# population S001..S026 (append-only registry), so later rows cannot move it.
SOURCES_BASE_MAX_ID = 26
SOURCES_EXPECTED_TOKENS = ("rows 25", "malformed 0", "A=24 C=1",
                           "mined=18 queued=5 rejected=2")
# P2b frozen anchor content: the line each backticked SCORECARD anchor must
# still show (content-checked, never a bare in-range test).
AXIS_ANCHOR_CONTENT = {":162": ("**novelty**", "**7**")}
# Appended correction lines: "- **R25-E<n> (date)** supersedes `<assertion-id>` — now `tok` `tok` ..."
SUPERSEDE_RE = re.compile(r"^- \*\*R25-E\d+[^*]*\*\* supersedes `([^`]+)`(.*)$")
POINTER_ONLY_RE = re.compile(r"^[A-Za-z0-9_./-]+(?::\d+(?:-\d+)?)?$")
SEED_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "r25" / "shonen-seed.txt"
SEED_FIXTURE_SHA256 = "3962e6b87c5412623416dfd8d10d3830f9ebc35d5dd093679104b03082cf0927"  # PROTOCOL.md:439-448 verbatim, frozen round 25
# Frozen capability rows that named an offline command at base: losing it is a mismatch.
COMMAND_CAPABILITIES = ("offline-replay-gate", "frozen-table-pin-check")
# Only the declared marker counts (round-25 falsify CritPreregAdherence): **ABSENT** or **ABSENT <date>**.
ABSENT_MARK_RE = re.compile(r"\*\*ABSENT(?: \d{4}-\d{2}-\d{2})?\*\*")

CODE_RE = re.compile(r"`([^`]+)`")
FILE_REF_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"(?:\.\.?/)?(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+"
    r"\.(?:md|py|json|jsonl|log|txt|sh|toml|yaml|yml)"
    r"(?::\d+(?:-\d+)?)?"
    r"(?![A-Za-z0-9_.-])"
)
SECTION_REF_RE = re.compile(
    r"§([A-Za-z][A-Za-z0-9 -]*?)"
    r"(?=[,.;:)\]]|\s+(?:and|or|but|with|from|in|on|at|for|to|the)\b|$)",
    re.IGNORECASE,
)


@dataclass
class Assertion:
    id: str
    source_line: int | None
    check: str
    observed: Any
    verdict: str


def add(
    out: list[Assertion],
    assertion_id: str,
    source_line: int | None,
    check: str,
    observed: Any,
    verdict: str,
) -> None:
    out.append(Assertion(assertion_id, source_line, check, observed, verdict))


def physical_lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def line_text(line: str) -> str:
    return line[:-1] if line.endswith("\n") else line


def content_text(line: str) -> str:
    return line_text(line).rstrip("\r")


def read_repo_text(root: Path, relative: str) -> str | None:
    try:
        return (root / relative).read_bytes().decode("utf-8")
    except (OSError, UnicodeError):
        return None


def table_cells(line: str) -> list[str] | None:
    candidate = line.strip()
    if not candidate.startswith("|") or not candidate.endswith("|"):
        return None
    cells = [cell.strip() for cell in candidate[1:-1].split("|")]
    if cells and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", ""))
                     for cell in cells):
        return None
    return cells


def find_line(lines: list[str], predicate, start: int = 0) -> int | None:
    for index in range(start, len(lines)):
        if predicate(content_text(lines[index])):
            return index
    return None


def next_h2(lines: list[str], start: int) -> int:
    for index in range(start + 1, len(lines)):
        text = content_text(lines[index])
        if text.startswith("## ") and not text.startswith("### "):
            return index
    return len(lines)


def table_rows(lines: list[str], start: int, end: int):
    for index in range(start, end):
        cells = table_cells(content_text(lines[index]))
        if cells is not None:
            yield index + 1, cells


def code_spans(text: str) -> list[str]:
    return [match.group(1).strip() for match in CODE_RE.finditer(text)]


def normalize_command(text: str) -> tuple[str, ...] | None:
    try:
        argv = tuple(shlex.split(text))
    except ValueError:
        return None
    return argv if argv in ALLOWED_COMMANDS else None


class CommandRunner:
    """Run only the two frozen, offline commands named by P2a/P2b."""

    def __init__(self, root: Path):
        self.root = root
        self.cache: dict[tuple[str, ...], dict[str, Any]] = {}

    def run(self, command: tuple[str, ...]) -> dict[str, Any]:
        if command in self.cache:
            return self.cache[command]
        if command not in ALLOWED_COMMANDS:
            result = {
                "returncode": None,
                "stdout": "",
                "stderr": "command is outside the frozen offline allowlist",
                "timed_out": False,
            }
            self.cache[command] = result
            return result
        try:
            proc = subprocess.run(
                command,
                cwd=self.root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                check=False,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            result = {
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "timed_out": False,
            }
        except subprocess.TimeoutExpired as exc:
            result = {
                "returncode": None,
                "stdout": (exc.stdout or b"").decode("utf-8", "replace")
                if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
                "stderr": (exc.stderr or b"").decode("utf-8", "replace")
                if isinstance(exc.stderr, bytes) else (exc.stderr or ""),
                "timed_out": True,
            }
        except OSError as exc:
            result = {
                "returncode": None,
                "stdout": "",
                "stderr": f"{type(exc).__name__}: {exc}",
                "timed_out": False,
            }
        self.cache[command] = result
        return result


DUPLICATE_ROWS: list[tuple[str, int]] = []


def row_map(lines: list[str], start: int, end: int) -> dict[str, tuple[int, list[str]]]:
    rows: dict[str, tuple[int, list[str]]] = {}
    for line_number, cells in table_rows(lines, start, end):
        if not cells or not cells[0] or cells[0].lower() in {
            "capability", "axis", "surface", "entry", "file", "dir"
        }:
            continue
        key = cells[0].strip().strip("`")
        if key in rows:
            # Round-25 falsify (RevengeFirstLocalPath, RevP2Population): a second row with a frozen
            # key must not silently shadow the first; the first stays, the duplicate is a finding.
            DUPLICATE_ROWS.append((key, line_number))
            continue
        rows[key] = (line_number, cells)
    return rows


def sources_base_census(root: Path) -> str | None:
    """Contract-v1 census over registry rows S001..S026 (base population)."""
    text = read_repo_text(root, "corpus/SOURCES.md")
    if text is None:
        return None
    rows = malformed = 0
    tiers: dict[str, int] = {}
    statuses: dict[str, int] = {}
    ids: list[int] = []
    for line in text.splitlines():
        match = re.match(r"^\|\s*S(\d{3,})\s*\|", line)
        if not match or int(match.group(1)) > SOURCES_BASE_MAX_ID:
            continue
        ids.append(int(match.group(1)))
        rows += 1
        fields = line.split("|")
        if len(fields) != 13:
            malformed += 1
            continue
        tier, status = fields[4].strip(), fields[8].strip()
        tiers[tier] = tiers.get(tier, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
    tier_text = " ".join(f"{k}={tiers[k]}" for k in sorted(tiers))
    status_text = " ".join(f"{k}={statuses[k]}" for k in ("mined", "queued", "rejected")
                           if k in statuses)
    # Round-25 falsify (RevSupersede): the base population must be exactly S001..S026 once each.
    idset = "" if sorted(ids) == list(range(1, SOURCES_BASE_MAX_ID + 1)) else "; id-set-defect"
    return f"rows {rows}; malformed {malformed}; {tier_text}; {status_text}{idset}"


def superseding_tokens(root: Path, assertion_id: str) -> tuple[int, list[str]] | None:
    """Latest appended SCORECARD correction naming this assertion, with its tokens."""
    text = read_repo_text(root, "SCORECARD.md")
    if text is None:
        return None
    found = None
    for number, line in enumerate(text.splitlines(), 1):
        match = SUPERSEDE_RE.match(line)
        if match and match.group(1) == assertion_id:
            found = (number, code_spans(match.group(2)))
    return found


def check_sources_registry(root: Path, out: list[Assertion], line_number: int) -> None:
    assertion_id = "P2a.capability.sources-registry"
    observed = sources_base_census(root)
    if observed is None:
        add(out, assertion_id, line_number, "hardcoded contract census on S001..S026",
            "corpus/SOURCES.md missing or unreadable", "MISMATCH")
        return
    missing = [token for token in SOURCES_EXPECTED_TOKENS if token not in observed]
    if "id-set-defect" in observed:
        add(out, assertion_id, line_number, "base registry population is exactly S001..S026",
            {"observed": observed}, "MISMATCH")
        return
    if not missing:
        add(out, assertion_id, line_number, "hardcoded contract census on S001..S026",
            {"observed": observed, "expected": list(SOURCES_EXPECTED_TOKENS)}, "MATCH")
        return
    correction = superseding_tokens(root, assertion_id)
    if correction is not None:
        correction_line, tokens = correction
        # Round-25 falsify (RevSupersede, CritC2Fresh): a correction supersedes only when its
        # tokens restate the whole observed census exactly, never a cherry-picked fragment.
        exact = "; ".join(tokens) == observed
        add(out, assertion_id, line_number,
            "stale row superseded by an appended correction restating the full census",
            {"observed": observed, "stale_tokens": missing, "correction_line": correction_line,
             "correction_tokens": tokens, "correction_exact": exact},
            "SUPERSEDED" if exact else "MISMATCH")
        return
    add(out, assertion_id, line_number, "hardcoded contract census on S001..S026",
        {"observed": observed, "missing_tokens": missing}, "MISMATCH")


def check_capabilities(root: Path, out: list[Assertion], runner: CommandRunner) -> None:
    text = read_repo_text(root, "SCORECARD.md")
    if text is None:
        add(out, "P2a.scorecard", None, "read SCORECARD.md", "missing or unreadable", "MISMATCH")
        return
    lines = physical_lines(text)
    heading = find_line(lines, lambda line: line == "## Capabilities")
    if heading is None:
        add(out, "P2a.capabilities.section", None, "find fixed ## Capabilities section",
            "heading missing", "MISMATCH")
        return
    end = next_h2(lines, heading)
    rows = row_map(lines, heading + 1, end)
    for key, (line_number, cells) in rows.items():
        if key not in CAPABILITY_IDS:
            add(out, f"P2a.out-of-population.{key}", line_number,
                "capability row outside frozen 6180e4f population", key,
                "OUT_OF_POPULATION")
    for capability in CAPABILITY_IDS:
        row = rows.get(capability)
        if row is None:
            add(out, f"P2a.capability.{capability}", heading + 1,
                "run frozen capability row command and compare its evidence tokens",
                "frozen row missing", "MISMATCH")
            continue
        line_number, cells = row
        if capability == "sources-registry":
            check_sources_registry(root, out, line_number)
            continue
        evidence = cells[2] if len(cells) > 2 else ""
        command_text = next((span for span in code_spans(evidence)
                             if span.startswith("python3 ")), None)
        if command_text is None:
            add(out, f"P2a.capability.{capability}", line_number,
                "run frozen capability row command and compare its evidence tokens",
                {"command": None, "reason": "evidence cell names no runnable offline command"},
                "MISMATCH" if capability in COMMAND_CAPABILITIES else "OFFLINE_UNVERIFIABLE")
            continue
        command = normalize_command(command_text)
        if command is None:
            add(out, f"P2a.capability.{capability}", line_number,
                "run frozen capability row command and compare its evidence tokens",
                {"command": command_text, "reason": "not in frozen offline allowlist"},
                "MISMATCH")
            continue
        tail = evidence.split("→", 1)[1] if "→" in evidence else ""
        expected_tokens = code_spans(tail)
        exit_match = re.search(r"\bexit\s+(\d+)\b", tail)
        expected_exit = int(exit_match.group(1)) if exit_match else 0
        result = runner.run(command)
        missing = [token for token in expected_tokens
                   if token not in result["stdout"]]
        ok = (result["returncode"] == expected_exit and not result["timed_out"]
              and not missing)
        add(out, f"P2a.capability.{capability}", line_number,
            "run row command; require recorded exit and every expected output token",
            {
                "command": list(command),
                "expected_exit": expected_exit,
                "expected_tokens": expected_tokens,
                "returncode": result["returncode"],
                "missing_tokens": missing,
                "stdout": result["stdout"].strip(),
                "stderr": result["stderr"].strip(),
                "timed_out": result["timed_out"],
            },
            "MATCH" if ok else "MISMATCH")


def check_axis_table(root: Path, out: list[Assertion], runner: CommandRunner) -> None:
    text = read_repo_text(root, "SCORECARD.md")
    if text is None:
        add(out, "P2b.scorecard", None, "read SCORECARD.md", "missing or unreadable", "MISMATCH")
        return
    lines = physical_lines(text)
    marker = find_line(lines, lambda line: line.startswith("Re-derived axis state, round 24"))
    if marker is None:
        add(out, "P2b.axis-table", None, "find round-24 re-derived axis table",
            "fixed marker missing", "MISMATCH")
        return
    header = find_line(lines, lambda line: line == "| Axis | Round-24 value | Basis |", marker + 1)
    if header is None:
        add(out, "P2b.axis-table", marker + 1, "find fixed axis table header",
            "header missing", "MISMATCH")
        return
    end = header + 2
    while end < len(lines) and table_cells(content_text(lines[end])) is not None:
        end += 1
    rows = row_map(lines, header + 2, end)
    for key, (line_number, cells) in rows.items():
        if key not in AXIS_IDS:
            add(out, f"P2b.out-of-population.{key}", line_number,
                "axis row outside frozen 6180e4f population", key,
                "OUT_OF_POPULATION")
    for axis in AXIS_IDS:
        row = rows.get(axis)
        if row is None:
            add(out, f"P2b.axis.{axis}", header + 1,
                "frozen round-24 axis row exists", "row missing", "MISMATCH")
            continue
        line_number, cells = row
        basis = cells[2] if len(cells) > 2 else ""
        spans = code_spans(basis)
        for span_index, span in enumerate(spans, 1):
            anchor_match = re.fullmatch(r":(\d+)(?:-(\d+))?", span)
            if anchor_match:
                start_line = int(anchor_match.group(1))
                end_line = int(anchor_match.group(2) or start_line)
                in_range = 1 <= start_line <= end_line <= len(lines)
                needles = AXIS_ANCHOR_CONTENT.get(span)
                anchored = (content_text(lines[start_line - 1]) if in_range else "")
                ok = in_range and needles is not None and all(n in anchored for n in needles)
                add(out, f"P2b.axis.{axis}.anchor.{span_index}", line_number,
                    "backticked SCORECARD line anchor shows its frozen content",
                    {"anchor": span, "expected": list(needles or ()),
                     "anchored_line": anchored, "resolved": ok},
                    "MATCH" if ok else "MISMATCH")
                continue
            command = normalize_command(span)
            if span == "freeze-check":
                command = FREEZE_CHECK_COMMAND
            if command is not None:
                for arg in command[1:]:
                    if arg.endswith((".py", ".md", ".sh")):
                        exists = (root / arg).exists()
                        add(out, f"P2b.axis.{axis}.command-path.{span_index}.{arg}",
                            line_number, "command path exists under --root", arg,
                            "MATCH" if exists else "MISMATCH")
                result = runner.run(command)
                expected_words = {
                    ("python3", "grader.py"): ["PASS"],
                    FREEZE_CHECK_COMMAND: ["OK"],
                }[command]
                missing = [word for word in expected_words
                           if word not in result["stdout"]]
                ok = result["returncode"] == 0 and not result["timed_out"] and not missing
                add(out, f"P2b.axis.{axis}.command.{span_index}", line_number,
                    "re-run named offline command and compare stated verdict tokens",
                    {
                        "command": list(command),
                        "returncode": result["returncode"],
                        "expected_tokens": expected_words,
                        "missing_tokens": missing,
                        "stdout": result["stdout"].strip(),
                        "stderr": result["stderr"].strip(),
                        "timed_out": result["timed_out"],
                    },
                    "MATCH" if ok else "MISMATCH")
                continue
            if span in {"test -e", "ss", "sha256sum"}:
                continue
            path_text = span.rstrip("/")
            if re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", path_text):
                exists = (root / path_text).exists()
                add(out, f"P2b.axis.{axis}.path.{span_index}", line_number,
                    "backticked path resolves under --root", span,
                    "MATCH" if exists else "MISMATCH")
        for anchor_index, match in enumerate(SECTION_REF_RE.finditer(basis), 1):
            section = match.group(1).strip()
            if not section:
                continue
            target = "PROVINCE.md" if "province" in basis.lower() else "SCORECARD.md"
            target_text = read_repo_text(root, target)
            target_lines = target_text.splitlines() if target_text is not None else []
            resolved = any(section.casefold() in line.casefold()
                           and line.lstrip().startswith("#") for line in target_lines)
            add(out, f"P2b.axis.{axis}.section.{anchor_index}", line_number,
                "section anchor resolves in cited file", {
                    "file": target, "anchor": section, "resolved": resolved,
                }, "MATCH" if resolved else "MISMATCH")


def find_protocol(root: Path) -> Path | None:
    candidates: list[Path] = [root.parent / "PROTOCOL.md"]
    for start in (Path.cwd(), Path(__file__).resolve().parent):
        candidates.extend(parent / "PROTOCOL.md" for parent in (start, *start.parents))
    seen: set[Path] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return resolved
    return None


def canonical_seed(protocol_text: str) -> tuple[list[str] | None, int | None]:
    lines = physical_lines(protocol_text)
    marker = find_line(lines, lambda line: line.startswith(
        "The canonical `SHONEN.md` seed"))
    if marker is None:
        return None, None
    block: list[str] = []
    started = False
    start_line: int | None = None
    for index, line in enumerate(lines[marker + 1:], marker + 1):
        text = line_text(line)
        blank = text.strip("\r \t") == ""
        if blank:
            if started:
                block.append(line)
            continue
        if not text.startswith("    "):
            break
        if not started:
            start_line = index + 1
        started = True
        block.append(line[4:])
    while block and content_text(block[-1]) == "":
        block.pop()
    return (block if block else None), start_line


def resolve_pointer(root: Path, ref: str) -> tuple[Path, int | None, int | None]:
    cleaned = ref.strip().strip("`'\".,;()[]{}")
    anchor_start = anchor_end = None
    match = re.fullmatch(r"(.+?):(\d+)(?:-(\d+))?", cleaned)
    if match:
        cleaned = match.group(1)
        anchor_start = int(match.group(2))
        anchor_end = int(match.group(3) or match.group(2))
    candidate = Path(cleaned).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate, anchor_start, anchor_end


def pointer_refs(text: str) -> list[str]:
    refs = [match.group(0) for match in FILE_REF_RE.finditer(text)]
    out: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            out.append(ref)
    return out


def shonen_box_line(text: str) -> bool:
    return bool(re.match(r"^\s*- \[[ ~x]\] ", text))


def check_shonen(root: Path, protocol_path: Path, out: list[Assertion]) -> None:
    shonen_text = read_repo_text(root, "SHONEN.md")
    protocol_text = read_repo_text(protocol_path.parent, protocol_path.name)
    if shonen_text is None:
        add(out, "P2c.shonen", None, "read SHONEN.md", "missing or unreadable", "MISMATCH")
        return
    if protocol_text is None:
        add(out, "P2c.protocol", None, "read canonical PROTOCOL.md seed",
            "missing or unreadable", "MISMATCH")
        return
    seed, protocol_start = canonical_seed(protocol_text)
    if seed is None:
        add(out, "P2c.protocol-seed", None, "extract canonical seed block",
            "fixed seed marker or indented block missing", "MISMATCH")
        return
    seed = [line.replace("<name>", LANE_NAME) for line in seed]
    actual = physical_lines(shonen_text)
    canonical_actual: list[str] = []
    evidence: list[tuple[int, str, int]] = []
    seed_ok = True
    cursor = 0
    box_number = 0

    for expected in seed:
        expected_content = content_text(expected)
        if expected_content.startswith("- [ ] "):
            expected_payload = expected_content[len("- [ ] "):]
            if cursor >= len(actual):
                seed_ok = False
                add(out, f"P2c.box.{box_number + 1}.seed", None,
                    "canonical checkbox text and order match seed",
                    "checkbox missing", "MISMATCH")
                continue
            observed_line = actual[cursor]
            observed_content = content_text(observed_line)
            match = re.match(r"^(\s*- \[)( |~|x)(\] .*)$", observed_content)
            if match is None or match.group(3)[2:] != expected_payload:
                if shonen_box_line(observed_content):
                    seed_ok = False
                    add(out, f"P2c.box.{box_number + 1}.seed", cursor + 1,
                        "canonical checkbox text and order match seed",
                        observed_content, "MISMATCH")
                    cursor += 1
                else:
                    seed_ok = False
                    add(out, f"P2c.box.{box_number + 1}.seed", cursor + 1,
                        "canonical checkbox text and order match seed",
                        observed_content, "MISMATCH")
                box_number += 1
                continue
            normalized = match.group(1) + " " + match.group(3)
            normalized_line = normalized + ("\n" if observed_line.endswith("\n") else "")
            canonical_actual.append(normalized_line)
            box_number += 1
            box_line_number = cursor + 1
            cursor += 1
            evidence_lines: list[tuple[str, int]] = []
            while cursor < len(actual):
                evidence_content = content_text(actual[cursor])
                if (evidence_content.startswith(("  ", "\t"))
                        and evidence_content.strip()):
                    evidence_lines.append((actual[cursor], cursor + 1))
                    cursor += 1
                else:
                    break
            if evidence_lines:
                first_line, first_source = evidence_lines[0]
                evidence.append((box_number, first_line, first_source))
                observed = [content_text(line).strip() for line, _ in evidence_lines]
                add(out, f"P2c.box.{box_number}.evidence-line", first_source,
                    "exactly one indented evidence line follows this box",
                    {"count": len(evidence_lines), "lines": observed},
                    "MATCH" if len(evidence_lines) == 1 else "MISMATCH")
                pointer_only = bool(POINTER_ONLY_RE.match(observed[0]))
                add(out, f"P2c.box.{box_number}.pointer-only", first_source,
                    "evidence line is one resolvable pointer and no other prose "
                    "(PROTOCOL.md:432)", observed[0],
                    "MATCH" if pointer_only else "MISMATCH")
            else:
                add(out, f"P2c.box.{box_number}.evidence-line", box_line_number,
                    "exactly one indented evidence line follows this box",
                    "missing; next line is not an indented evidence line", "MISMATCH")
        else:
            if cursor >= len(actual):
                seed_ok = False
                add(out, "P2c.seed-line", None, "canonical seed line matches",
                    "line missing", "MISMATCH")
                continue
            observed_line = actual[cursor]
            canonical_actual.append(observed_line)
            if observed_line != expected:
                seed_ok = False
                add(out, "P2c.seed-line", cursor + 1,
                    "canonical seed line matches byte-for-byte modulo name and box mark",
                    {"expected": line_text(expected), "observed": line_text(observed_line)},
                    "MISMATCH")
            cursor += 1

    add(out, "P2c.seed", 1, "SHONEN seed matches canonical PROTOCOL seed modulo lane name and box mark",
        {
            "canonical_seed_start_line": protocol_start,
            "canonical_seed_lines": len(seed),
            "normalized_match": seed_ok and canonical_actual == seed,
        },
        "MATCH" if seed_ok and canonical_actual == seed else "MISMATCH")

    for box_number, evidence_line, source_line in evidence:
        refs = pointer_refs(content_text(evidence_line))
        if not refs:
            add(out, f"P2c.box.{box_number}.pointer", source_line,
                "evidence line contains at least one resolvable local pointer",
                "no path pointer found", "MISMATCH")
            continue
        for pointer_number, ref in enumerate(refs, 1):
            target, anchor_start, anchor_end = resolve_pointer(root, ref)
            exists = target.exists()
            anchor_ok = True
            target_lines = 0
            if exists and (anchor_start is not None or anchor_end is not None):
                try:
                    target_lines = len(target.read_bytes().splitlines())
                except OSError:
                    anchor_ok = False
                else:
                    anchor_ok = (anchor_start is not None and anchor_end is not None
                                 and 1 <= anchor_start <= anchor_end <= target_lines)
            ok = exists and anchor_ok
            add(out, f"P2c.box.{box_number}.pointer.{pointer_number}", source_line,
                "evidence pointer resolves to a file/directory and any line anchor is in range",
                {
                    "pointer": ref,
                    "resolved_path": str(target),
                    "exists": exists,
                    "anchor": ([anchor_start, anchor_end]
                               if anchor_start is not None else None),
                    "target_lines": target_lines if anchor_start is not None else None,
                    "anchor_resolves": anchor_ok,
                }, "MATCH" if ok else "MISMATCH")
    text = read_repo_text(root, "corpus/README.md") or ""
    for box_number, evidence_line, source_line in evidence:
        for section_index, match in enumerate(
                SECTION_REF_RE.finditer(content_text(evidence_line)), 1):
            section = match.group(1).strip()
            if not section:
                continue
            # In the frozen SHONEN boxes, section labels refer to corpus/README.md.
            target = root / "corpus/README.md"
            resolved = any(section.casefold() in line.casefold()
                           and line.lstrip().startswith("#") for line in text.splitlines())
            add(out, f"P2c.box.{box_number}.section-pointer.{section_index}", source_line,
                "section pointer resolves to a README heading",
                {"file": str(target), "anchor": section, "resolved": resolved},
                "MATCH" if resolved else "MISMATCH")

    while cursor < len(actual):
        observed = content_text(actual[cursor])
        line_number = cursor + 1
        if not observed.strip():
            cursor += 1
            continue
        if shonen_box_line(observed):
            add(out, f"P2c.out-of-population.box.line-{line_number}", line_number,
                "checkbox added after frozen four-box seed; not checked", observed,
                "OUT_OF_POPULATION")
            cursor += 1
            if cursor < len(actual) and content_text(actual[cursor]).startswith(("  ", "\t")):
                cursor += 1
            continue
        add(out, f"P2c.extra-prose.line-{line_number}", line_number,
            "no prose is permitted outside the frozen seed and its evidence lines",
            observed, "MISMATCH")
        cursor += 1


def section_bounds(lines: list[str], start_text: str, end_text: str) -> tuple[int, int] | None:
    start = find_line(lines, lambda line: start_text in line)
    if start is None:
        return None
    end = find_line(lines, lambda line: end_text in line, start + 1)
    return (start, end if end is not None else len(lines))


def first_local_path(cell: str) -> str | None:
    for span in code_spans(cell):
        value = span.strip().strip("`'")
        if ("http://" in cell.lower() or "https://" in cell.lower()) and re.fullmatch(
                r"/(?:v1/[^\s]+|health)", value):
            continue
        if re.match(r"https?://", value, re.IGNORECASE):
            continue
        value = value.split(" — ", 1)[0].strip()
        value = value.split(";", 1)[0].strip()
        path_match = re.match(
            r"^(?:~?/|\.\.?/|(?:corpus|plans|knowledge|lessons|evidence)/)"
            r"[^\s,;|`]+",
            value,
        )
        if path_match is None:
            path_match = re.match(
                r"^[A-Za-z0-9_.-]+\.(?:md|py|json|log|txt|sh)/?$", value)
        if path_match:
            path = path_match.group(0).rstrip(".,)")
            if "{" in path:
                path = path.split("{", 1)[0].rstrip("/")
            if path:
                return path
    return None


def check_surfaces(root: Path, out: list[Assertion]) -> None:
    text = read_repo_text(root, "PROVINCE.md")
    if text is None:
        add(out, "P2d.province", None, "read PROVINCE.md", "missing or unreadable", "MISMATCH")
        return
    lines = physical_lines(text)
    heading = find_line(lines, lambda line: line.startswith("## Surfaces"))
    if heading is None:
        add(out, "P2d.surfaces.section", None, "find fixed ## Surfaces section",
            "heading missing", "MISMATCH")
        return
    end = next_h2(lines, heading)
    rows_by_name = row_map(lines, heading + 1, end)
    for name, (line_number, cells) in rows_by_name.items():
        if name not in SURFACE_IDS:
            add(out, f"P2d.out-of-population.{name}", line_number,
                "surface row outside frozen 6180e4f population", name,
                "OUT_OF_POPULATION")
    for surface in SURFACE_IDS:
        row = rows_by_name.get(surface)
        if row is None:
            add(out, f"P2d.surface.{surface}.row", heading + 1,
                "frozen surface row exists", "row missing", "MISMATCH")
            continue
        line_number, cells = row
        path_cell = cells[1] if len(cells) > 1 else ""
        row_text = " | ".join(cells)
        spans = code_spans(path_cell)
        # Pre-registration P2d: a row whose surface is a URL/endpoint (its first backticked
        # span) is offline-unverifiable; a later /proc pid pin inside it is live process
        # state, not a declared path (round-25 falsify finding, StateSelftestExec).
        endpoint_row = bool(spans) and bool(re.match(r"https?://", spans[0], re.IGNORECASE))
        candidate = None if endpoint_row else first_local_path(path_cell)
        has_url = bool(re.search(
            r"https?://|\b(?:endpoint|port|URLs?)\b", path_cell, re.IGNORECASE))
        if candidate is None:
            add(out, f"P2d.surface.{surface}.availability", line_number,
                "local path tested, or URL/endpoint explicitly offline-unverifiable",
                {"path": None, "url_or_endpoint": has_url, "row": row_text},
                "OFFLINE_UNVERIFIABLE")
            continue
        path = Path(candidate).expanduser()
        if not path.is_absolute():
            path = root / path
        exists = path.exists()
        marked_absent = bool(ABSENT_MARK_RE.search(row_text))
        ok = ((exists and not marked_absent) or (not exists and marked_absent))
        add(out, f"P2d.surface.{surface}.path", line_number,
            "first backticked local path agrees with test -e and ABSENT marker",
            {
                "path": candidate,
                "resolved_path": str(path),
                "exists": exists,
                "ABSENT_marked": marked_absent,
            }, "MATCH" if ok else "MISMATCH")
        if has_url:
            add(out, f"P2d.surface.{surface}.url", line_number,
                "URL/endpoint recorded without contacting it",
                "offline-unverifiable; no request made", "OFFLINE_UNVERIFIABLE")


def readme_index_rows(root: Path) -> tuple[list[tuple[str, int]], dict[str, int]]:
    text = read_repo_text(root, "corpus/README.md")
    if text is None:
        return [], {}
    lines = physical_lines(text)
    rows: list[tuple[str, int]] = []
    anchors: dict[str, int] = {}
    what = section_bounds(lines, "## What's here", "### `lessons/`")
    if what is not None:
        anchors["knowledge/"] = what[0] + 1
        anchors["lessons/"] = what[0] + 1
        for line_number, cells in table_rows(lines, what[0] + 1, what[1]):
            if not cells:
                continue
            spans = code_spans(cells[0])
            if spans and spans[0].startswith(("knowledge/", "lessons/")):
                rows.append((spans[0], line_number))
    lessons = section_bounds(lines, "### `lessons/`", "Supporting corpus files:")
    if lessons is not None:
        anchors["lessons/"] = lessons[0] + 1
        for line_number, cells in table_rows(lines, lessons[0] + 1, lessons[1]):
            if not cells:
                continue
            spans = code_spans(cells[0])
            if spans and spans[0].startswith("lessons/"):
                rows.append((spans[0], line_number))
    evidence = section_bounds(lines, "### `evidence/`", "### `plans/`")
    if evidence is not None:
        anchors["evidence/"] = evidence[0] + 1
        receipt_marker = find_line(
            lines, lambda line: line.startswith("Root-level receipt logs"), evidence[0] + 1)
        round24_marker = find_line(
            lines, lambda line: line.startswith("Round-24 additions:"), evidence[0] + 1)
        for line_number, cells in table_rows(lines, evidence[0] + 1, evidence[1]):
            if not cells:
                continue
            spans = code_spans(cells[0])
            if not spans:
                continue
            first = spans[0]
            if first.startswith("evidence/"):
                rows.append((first, line_number))
            elif (receipt_marker is not None and line_number - 1 > receipt_marker
                  and (round24_marker is None or line_number - 1 < round24_marker)
                  and first.endswith(".log") and "/" not in first):
                rows.append((f"evidence/{first}", line_number))
    return rows, anchors


def actual_index_scope(root: Path) -> list[str]:
    corpus = root / "corpus"
    paths: list[str] = []
    for namespace in ("knowledge", "lessons"):
        directory = corpus / namespace
        if directory.is_dir():
            paths.extend(f"{namespace}/{entry.name}" for entry in directory.iterdir()
                         if entry.is_file())
    evidence = corpus / "evidence"
    if evidence.is_dir():
        paths.extend(f"evidence/{entry.name}{'/' if entry.is_dir() else ''}"
                     for entry in evidence.iterdir()
                     if entry.is_dir() or entry.is_file())
    return sorted(paths)


def path_exists(root: Path, relative: str) -> bool:
    candidate = root / "corpus" / relative
    if relative.endswith("/"):
        return candidate.is_dir()
    return candidate.is_file()


def check_readme_index(root: Path, out: list[Assertion]) -> None:
    text = read_repo_text(root, "corpus/README.md")
    if text is None:
        add(out, "P2e.readme", None, "read corpus/README.md", "missing or unreadable", "MISMATCH")
        return
    rows, anchors = readme_index_rows(root)
    expected = set(README_INDEX_PATHS)
    row_locations: dict[str, list[int]] = {}
    for relative, line_number in rows:
        row_locations.setdefault(relative, []).append(line_number)
        if relative not in expected:
            add(out, f"P2e.out-of-population.row.{relative}@{line_number}", line_number,
                "README index row outside frozen 6180e4f population; not checked",
                relative, "OUT_OF_POPULATION")
    for relative in README_INDEX_PATHS:
        locs = row_locations.get(relative, [])
        source_line = locs[0] if locs else anchors.get(relative.split("/", 1)[0] + "/")
        exists = path_exists(root, relative)
        add(out, f"P2e.row-to-file.{relative}", source_line,
            "frozen README index row resolves to a file or directory",
            {"path": relative, "exists": exists, "row_lines": locs},
            "MATCH" if exists else "MISMATCH")
        if len(locs) > 1:
            add(out, f"P2e.duplicate-row.{relative}", locs[1],
                "frozen path occurs exactly once in the README index", locs,
                "MISMATCH")
    for relative in README_FILE_PATHS:
        locs = row_locations.get(relative, [])
        source_line = locs[0] if locs else anchors.get(relative.split("/", 1)[0] + "/")
        present = path_exists(root, relative)
        add(out, f"P2e.file-to-row.{relative}", source_line,
            "frozen base file/directory still exists and has a README index row",
            {"path": relative, "exists": present, "indexed": bool(locs), "row_lines": locs},
            "MATCH" if (locs and present) else "MISMATCH")
    frozen_files = set(README_FILE_PATHS)
    for relative in actual_index_scope(root):
        if relative not in frozen_files:
            add(out, f"P2e.out-of-population.file.{relative}", None,
                "on-disk index-scope path outside frozen 6180e4f population; not checked",
                relative, "OUT_OF_POPULATION")

def check_all(root: Path, protocol_path: Path) -> list[Assertion]:
    assertions: list[Assertion] = []
    DUPLICATE_ROWS.clear()
    runner = CommandRunner(root)
    check_capabilities(root, assertions, runner)
    check_axis_table(root, assertions, runner)
    check_shonen(root, protocol_path, assertions)
    check_surfaces(root, assertions)
    check_readme_index(root, assertions)
    for key, line_number in DUPLICATE_ROWS:
        add(assertions, f"P2.duplicate-row.{key}@{line_number}", line_number,
            "a frozen table key appears once", key, "MISMATCH")
    return assertions


def counts(assertions: list[Assertion]) -> dict[str, int]:
    verdict_counts = {name: 0 for name in
                      ("MATCH", "MISMATCH", "SUPERSEDED", "OFFLINE_UNVERIFIABLE",
                       "OUT_OF_POPULATION")}
    checked = 0
    for assertion in assertions:
        verdict_counts[assertion.verdict] = verdict_counts.get(assertion.verdict, 0) + 1
        if assertion.verdict != "OUT_OF_POPULATION":
            checked += 1
    return {
        "assertions": checked,
        "match": verdict_counts["MATCH"],
        "mismatch": verdict_counts["MISMATCH"],
        "superseded": verdict_counts["SUPERSEDED"],
        "offline_unverifiable": verdict_counts["OFFLINE_UNVERIFIABLE"],
        "out_of_population": verdict_counts["OUT_OF_POPULATION"],
    }


def print_summary(assertions: list[Assertion]) -> None:
    summary = counts(assertions)
    print("assertions={assertions} match={match} mismatch={mismatch} "
          "superseded={superseded} "
          "offline_unverifiable={offline_unverifiable}".format(**summary))
    for assertion in assertions:
        if assertion.verdict in {"MISMATCH", "SUPERSEDED", "OUT_OF_POPULATION"}:
            prefix = assertion.verdict
            where = f":{assertion.source_line}" if assertion.source_line is not None else ""
            observed = json.dumps(assertion.observed, ensure_ascii=False, sort_keys=True)
            print(f"{prefix}: {assertion.id}{where} — {observed}")
    if summary["mismatch"]:
        print("VERDICT: FAIL — at least one frozen assertion mismatches")
    else:
        print("VERDICT: PASS — all comparable frozen assertions match")


def extract_seed_text_for_selftest() -> str:
    return (
        "The canonical `SHONEN.md` seed (verbatim):\n"
        "\n"
        "    # <name> — Promotion checklist\n"
        "\n"
        "    Promotion to shokunin requires all of:\n"
        "\n"
        "    - [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources\n"
        "    - [ ] At least one end-to-end domain task executed and logged in LOG.md\n"
        "    - [ ] Instructions executable by an agent without oral context\n"
        "    - [ ] No cross-domain bleed (PROVINCE.md still accurate)\n"
        "\n"
        "Marks: described outside the seed.\n"
    )


def run_selftest() -> int:
    seed_text = extract_seed_text_for_selftest()
    seed, _ = canonical_seed(seed_text)
    if seed is None:
        print("selftest: canonical seed extraction failed", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory(prefix="state-check-r25-") as temp:
        root = Path(temp)
        (root / "corpus").mkdir()
        (root / "corpus/README.md").write_text(
            "# Corpus\n\n## Source availability\n", encoding="utf-8")
        (root / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
        body = [line_text(line).replace("<name>", LANE_NAME)
                for line in seed]
        shonen_lines: list[str] = []
        for line in body:
            if line.startswith("- [ ] "):
                shonen_lines.append(line.replace("- [ ]", "- [~]", 1))
                shonen_lines.append("  SKILL.md")
            else:
                shonen_lines.append(line)
        shonen_text = "\n".join(shonen_lines) + "\n"
        (root / "SHONEN.md").write_text(shonen_text, encoding="utf-8")
        protocol = root / "PROTOCOL.md"
        protocol.write_text(seed_text, encoding="utf-8")
        assertions: list[Assertion] = []
        check_shonen(root, protocol, assertions)
        if any(item.verdict == "MISMATCH" for item in assertions):
            print("selftest: canonical SHONEN fixture did not pass", file=sys.stderr)
            return 1
        if sum(item.id.endswith("evidence-line") and item.verdict == "MATCH"
               for item in assertions) != 4:
            print("selftest: evidence-line population was not four", file=sys.stderr)
            return 1

        mutated = shonen_text.replace("  SKILL.md\n", "  missing.md\n", 1)
        (root / "SHONEN.md").write_text(mutated, encoding="utf-8")
        assertions = []
        check_shonen(root, protocol, assertions)
        if not any(item.id.startswith("P2c.box.1.pointer")
                   and item.verdict == "MISMATCH" for item in assertions):
            print("selftest: dangling-pointer mutation survived", file=sys.stderr)
            return 1

        extra = shonen_text + "- [~] extra box\n  missing.md\n"
        (root / "SHONEN.md").write_text(extra, encoding="utf-8")
        assertions = []
        check_shonen(root, protocol, assertions)
        if (not any(item.verdict == "OUT_OF_POPULATION" for item in assertions)
                or any(item.id == "P2c.seed" and item.verdict == "MISMATCH"
                       for item in assertions)):
            print("selftest: later checkbox was not isolated as out-of-population",
                  file=sys.stderr)
            return 1

        # P2c pointer-only (PROTOCOL.md:432): prose after a valid pointer must fail.
        prose = shonen_text.replace("  SKILL.md\n", "  SKILL.md decision tables; not reviewed\n", 1)
        (root / "SHONEN.md").write_text(prose, encoding="utf-8")
        assertions = []
        check_shonen(root, protocol, assertions)
        if not any(item.id == "P2c.box.1.pointer-only" and item.verdict == "MISMATCH"
                   for item in assertions):
            print("selftest: prose-evidence mutation survived pointer-only", file=sys.stderr)
            return 1

        # P2a sources-registry: stale tokens MISMATCH; a correction re-derives -> SUPERSEDED;
        # a correction with a wrong token stays MISMATCH; rows past S026 never move the census.
        head = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |"
        def row(i: int, tier: str, status: str) -> str:
            return f"| S{i:03d} | s | paper | {tier} | x | y | z | {status} | 2026-10-19 | 90d | — |"
        registry = [head] + [row(i, "A", "mined") for i in range(1, 19)] \
            + [row(i, "A", "queued") for i in range(19, 24)] \
            + [row(24, "A", "queued"), row(25, "C", "rejected"), row(26, "C", "rejected"),
               row(27, "A", "mined")]
        (root / "corpus/SOURCES.md").write_text("\n".join(registry) + "\n", encoding="utf-8")
        census = sources_base_census(root)
        if census != "rows 26; malformed 0; A=24 C=2; mined=18 queued=6 rejected=2":
            print(f"selftest: base-population census wrong: {census}", file=sys.stderr)
            return 1
        card = "## Capabilities\n\n| Capability | What | Evidence | Round |\n|---|---|---|---|\n" \
               "| sources-registry | r | rows 25 | 24 |\n"
        for erratum, want in (("", "MISMATCH"),
                              ("- **R25-E1 (t)** supersedes `P2a.capability.sources-registry` — "
                               "now `rows 26` `A=24 C=2`\n", "MISMATCH"),
                              ("- **R25-E1 (t)** supersedes `P2a.capability.sources-registry` — "
                               "now `rows 26` `malformed 0` `A=24 C=2` `mined=18 queued=6 rejected=2`\n",
                               "SUPERSEDED"),
                              ("- **R25-E1 (t)** supersedes `P2a.capability.sources-registry` — "
                               "now `rows 27` `A=24 C=2`\n", "MISMATCH")):
            (root / "SCORECARD.md").write_text(card + "\n" + erratum, encoding="utf-8")
            got = []
            check_sources_registry(root, got, 5)
            if got[-1].verdict != want:
                print(f"selftest: sources-registry expected {want}, got {got[-1].verdict}",
                      file=sys.stderr)
                return 1

        # P2d: a missing first path passes only when its row says ABSENT.
        for marker, want in (("", "MISMATCH"), (" **ABSENT 2026-10-20**", "MATCH"), (" ABSENT", "MISMATCH")):
            (root / "PROVINCE.md").write_text(
                "## Surfaces\n\n| Surface | Path | Use |\n|---|---|---|\n"
                f"| Research notes (SSOT for eval craft) | `~/nonexistent-r25-selftest/x` | r{marker} |\n",
                encoding="utf-8")
            got = []
            check_surfaces(root, got)
            verdict = next(a.verdict for a in got if a.id.endswith("Research notes (SSOT for eval craft).path"))
            if verdict != want:
                print(f"selftest: P2d ABSENT rule expected {want}, got {verdict}", file=sys.stderr)
                return 1
        # Round-25 falsify survivors (MutStateCheck): ABSENT must be a whole word; only an
        # R25-E correction line supersedes; a :line anchor must show its frozen content.
        (root / "PROVINCE.md").write_text(
            "## Surfaces\n\n| Surface | Path | Use |\n|---|---|---|\n"
            "| Research notes (SSOT for eval craft) | `~/nonexistent-r25-selftest/x` | NONABSENTX |\n",
            encoding="utf-8")
        got = []
        check_surfaces(root, got)
        if next(a.verdict for a in got if a.id.endswith(".path")) != "MISMATCH":
            print("selftest: ABSENT matched inside another word", file=sys.stderr)
            return 1
        (root / "SCORECARD.md").write_text(
            card + "\n- note: supersedes `P2a.capability.sources-registry` — now `rows 26` `A=24 C=2`\n",
            encoding="utf-8")
        got = []
        check_sources_registry(root, got, 5)
        if got[-1].verdict != "MISMATCH":
            print("selftest: a non-R25 line superseded a stale row", file=sys.stderr)
            return 1
        filler = ["filler"] * 161
        for line162, want in (("| **novelty** *(owned)* | 6 → **7** |", "MATCH"),
                              ("| **depth** | 8 → **9** |", "MISMATCH")):
            body = filler + [line162, "", "Re-derived axis state, round 24", "",
                             "| Axis | Round-24 value | Basis |", "|---|---|---|",
                             "| novelty | 7 | numeric anchor r14 (`:162`) |"]
            (root / "SCORECARD.md").write_text("\n".join(body) + "\n", encoding="utf-8")
            got = []
            check_axis_table(root, got, CommandRunner(root))
            verdict = next(a.verdict for a in got if a.id == "P2b.axis.novelty.anchor.1")
            if verdict != want:
                print(f"selftest: :162 anchor content expected {want}, got {verdict}", file=sys.stderr)
                return 1
        # duplicate surface row must not shadow the first (round-25 falsify)
        (root / "PROVINCE.md").write_text(
            "## Surfaces\n\n| Surface | Path | Use |\n|---|---|---|\n"
            "| Research notes (SSOT for eval craft) | `~/nonexistent-r25-selftest/x` | r |\n"
            "| Research notes (SSOT for eval craft) | `PROVINCE.md` | r |\n", encoding="utf-8")
        DUPLICATE_ROWS.clear()
        got = []
        check_surfaces(root, got)
        if not DUPLICATE_ROWS or next(a.verdict for a in got if a.id.endswith(".path")) != "MISMATCH":
            print("selftest: a duplicate surface row shadowed the frozen row", file=sys.stderr)
            return 1
    print("[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, "
          "sources supersession, ABSENT rule, ABSENT word boundary, R25-E prefix, anchor content)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parent.parent,
                        help="lane tree to inspect (default: this script's repository)")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--summary", action="store_true", help="print counts and mismatches")
    output.add_argument("--json", action="store_true", help="print every assertion as JSON")
    parser.add_argument("--selftest", action="store_true",
                        help="run local mutation checks without network or repo writes")
    args = parser.parse_args(argv)
    if args.selftest:
        return run_selftest()
    try:
        root = args.root.expanduser().resolve(strict=True)
    except OSError as exc:
        print(f"state_check: INPUT ERROR: --root cannot be resolved: {exc}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"state_check: INPUT ERROR: --root is not a directory: {root}", file=sys.stderr)
        return 2
    protocol = SEED_FIXTURE if SEED_FIXTURE.is_file() else find_protocol(root)
    if protocol == SEED_FIXTURE:
        import hashlib
        digest = hashlib.sha256(SEED_FIXTURE.read_bytes()).hexdigest()
        fleet = find_protocol(root)
        drift = fleet is not None and SEED_FIXTURE.read_text(encoding="utf-8") not in fleet.read_text(encoding="utf-8")
        if digest != SEED_FIXTURE_SHA256 or drift:
            print(f"state_check: SETUP: SHONEN seed fixture pin broken (sha256 {digest[:16]}, "
                  f"fleet PROTOCOL drift={drift})", file=sys.stderr)
            return 2
    if protocol is None:
        print("state_check: INPUT ERROR: canonical PROTOCOL.md was not found; "
              "run from the fleet root or place the lane beside PROTOCOL.md",
              file=sys.stderr)
        return 2
    unreadable = [name for name in ("SCORECARD.md", "SHONEN.md", "PROVINCE.md", "corpus/README.md")
                  if read_repo_text(root, name) is None]
    if unreadable:
        print(f"state_check: SETUP: unreadable lane file(s): {', '.join(unreadable)}", file=sys.stderr)
        return 2
    try:
        assertions = check_all(root, protocol)
    except (OSError, UnicodeError, ValueError, IndexError) as exc:
        print(f"state_check: INPUT ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"summary": counts(assertions),
                          "assertions": [asdict(item) for item in assertions]},
                         ensure_ascii=False, indent=2))
    else:
        print_summary(assertions)
    if counts(assertions)["assertions"] == 0:
        print("state_check: SETUP: empty population — refusing a vacuous PASS", file=sys.stderr)
        return 2
    return 1 if any(item.verdict == "MISMATCH" for item in assertions) else 0


if __name__ == "__main__":
    sys.exit(main())
