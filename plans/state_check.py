#!/usr/bin/env python3
"""Re-derive frozen P2/P3/P4 current-state assertions offline (rounds 25–27).

Population P2 (plans/round-25-claims.md §C2 + Amendment 1) is frozen at base
6180e4f: SCORECARD capabilities (P2a) and round-24 axis table (P2b), SHONEN
canonical form (P2c, seed frozen in plans/fixtures/r25/shonen-seed.txt — PROTOCOL.md:439-448
verbatim, slice sha256 3962e6b8...; whole-file PROTOCOL.md sha256 886e459b... at freeze), PROVINCE ## Surfaces rows (P2d) and
corpus/README index rows both directions (P2e). A stale base assertion closed by

Population P3 is frozen at f11bffbf by plans/round-26-claims.md §C2: capability
receipt values (P3a), PROVINCE census/instrument rows (P3b), SHONEN pointer
content pins (P3c), round-24/25 axis-table anchors (P3d), and base
out-of-population README rows/files in both directions (P3e).
Population P4 is frozen at b5719440 by plans/round-27-claims.md §C2: SCORECARD
numeric claims and receipts (P4a), round-26 README artifact inventory (P4b),
lesson wave counts against retained wave records and Git trees (P4c), the
grader-audit population and family table against the JSON command and oracle
(P4d), and S043–S048 used-by citations in knowledge/lessons (P4e).
Only an appended R27-E correction with every re-derived token may supersede P4.
An appended dated correction is SUPERSEDED only when its complete tokens re-derive the observed value.
Exit 0 means all comparable frozen assertions match; 1 means any mismatch; 2 means usage,
unreadable input, or empty population (never a vacuous PASS).
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
import shutil
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
# Appended correction lines: "- **R2[5-9]-E<n> (date)** supersedes `<assertion-id>` — now `tok` `tok` ..."
SUPERSEDE_RE = re.compile(r"^- \*\*R2[5-9]-E\d+[^*]*\*\* supersedes `([^`]+)`(.*)$")
POINTER_ONLY_RE = re.compile(r"^[A-Za-z0-9_./-]+(?::\d+(?:-\d+)?)?$")
SEED_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "r25" / "shonen-seed.txt"
SEED_FIXTURE_SHA256 = "3962e6b87c5412623416dfd8d10d3830f9ebc35d5dd093679104b03082cf0927"  # PROTOCOL.md:439-448 verbatim, frozen round 25
# Frozen capability rows that named an offline command at base: losing it is a mismatch.
COMMAND_CAPABILITIES = ("offline-replay-gate", "frozen-table-pin-check")
# Only the declared marker counts (round-25 falsify CritPreregAdherence): **ABSENT** or **ABSENT <date>**.
ABSENT_MARK_RE = re.compile(r"\*\*ABSENT(?: \d{4}-\d{2}-\d{2})?\*\*")

P3A_INTERVAL_SUMMARY = "corpus/evidence/round25-calibration/attrib-calibration-summary-v2.txt"
P3A_INTERVAL_SELFTEST = "corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt"
P3A_STATE_BASE = "corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt"
P3A_STATE_AFTER = "corpus/evidence/round25-calibration/state-check-after-v2.txt"
P3A_STATE_SELFTEST = "corpus/evidence/round25-calibration/state-check-selftest-v2.txt"

# P3b's registry population is frozen before C1 additions: later S043+ rows
# cannot change its census; the retained S001..S042 id set must remain exact.
P3B_SOURCES_MAX_ID = 42

# P3 is frozen at f11bffbf. These are only the round-25 assertions that the
# round-25 v2 population reported OUT_OF_POPULATION or did not content-pin.
P3C_PINS = (
    (1, "SKILL.md", None, "## Decision table — benchmark selection", 1),
    (1, "SKILL.md", None, "## Benchmark anti-patterns", 2),
    (1, "SKILL.md", None, "## Production checklist — running an eval", 3),
    (1, "SKILL.md", None, "## Cited local sources", 4),
    (2, "LOG.md:7", 7, "round 4: executed first authored eval", None),
    (3, "corpus/lessons/round-8-aggregator-box3-coldrun.md:48",
     48, "## Box-3 verdict", None),
    (4, "PROVINCE.md:129", 129, "### Adjacent", None),
)
P3D_TABLES = (
    ("round24", "Re-derived axis state, round 24", "| Axis | Round-24 value | Basis |"),
    ("round25", "Re-derived axis state, round 25:", "| Axis | Round-25 value | Basis |"),
)
P3D_ANCHORS = {
    ("round24", ":162"): ("novelty", ("**novelty**", "**7**")),
}
P3E_ROW_PATHS = (
    "knowledge/attribution-interval-calibration.md",
    "lessons/round-24-verifier-spotcheck.md",
    "lessons/round-25.md",
    "evidence/round25-sources/",
    "evidence/round25-calibration/",
)
P3E_FILE_PATHS = (
    "knowledge/attribution-interval-calibration.md",
    "lessons/round-25-verifier-spotcheck.md",
    "lessons/round-25.md",
    "evidence/round25-sources/",
    "evidence/round25-calibration/",
)

# P3 corrections are append-only below each frozen document boundary. P2 keeps
# its v2 lookup and its independent R2[5-9]-E token convention.
P3_CORRECTION_FLOORS = {
    "SCORECARD.md": 730,
    "PROVINCE.md": 173,
    "corpus/README.md": 257,
}
P3_CORRECTION_DOCS = tuple(P3_CORRECTION_FLOORS)
P3_CORRECTION_ID_RE = re.compile(
    r"^- \*\*(R2[5-9]-E\d+[A-Za-z]?)\b")
P3_CORRECTION_LINE_RE = re.compile(
    r"^- \*\*(R2[5-9]-E\d+[A-Za-z]?) \(\d{4}-\d{2}-\d{2}\)\*\* "
    r"supersedes `([^`]+)` — now (`[^`]+`(?: `[^`]+`)*)\.?$")

P3A_NUMERIC_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])\d+(?![A-Za-z0-9])")
P3A_NUMERIC_FIELD_PATTERNS = (
    r"unique_samples=(\d+)",
    r"scored_trials=(\d+)\s+correct=(\d+)",
    r"transitions=(FAIL>UNTESTED:\d+,PASS>INDETERMINATE:\d+,PASS>PASS:\d+)",
    r"mismatches=(\d+)",
    r"\bmismatch=(\d+)",
    r"\bsuperseded=(\d+)",
    r"exit\s+(\d+)",
    r"--selftest`?\s+(\d+)\s+checks?\s+(\d+)\s+failed",
)

# Independent selftest oracle: changing/removing a registered comparison must
# fail even if the production checker and its output population shrink together.
P3_SELFTEST_ASSERTION_IDS = {
    "P3a": (
        "P3a.capability.interval-reverdict.unique-samples",
        "P3a.capability.interval-reverdict.scored-trials",
        "P3a.capability.interval-reverdict.transitions",
        "P3a.capability.interval-reverdict.mismatches",
        "P3a.capability.interval-reverdict.summary-exit",
        "P3a.capability.interval-reverdict.selftest-checks",
        "P3a.capability.interval-reverdict.selftest-red-runs",
        "P3a.capability.interval-reverdict.numeric-token-audit",
        "P3a.capability.state-assertion-check.base-mismatch",
        "P3a.capability.state-assertion-check.base-exit",
        "P3a.capability.state-assertion-check.landed-mismatch",
        "P3a.capability.state-assertion-check.landed-superseded",
        "P3a.capability.state-assertion-check.landed-exit",
        "P3a.capability.state-assertion-check.numeric-token-audit",
    ),
    "P3b": (
        "P3b.province.public-literature-registry.rows",
        "P3b.province.round25-correction.rows",
        "P3b.province.interval-reverdict.exits",
        "P3b.province.interval-reverdict.unique-samples",
        "P3b.province.interval-reverdict.scored-trials",
        "P3b.province.interval-reverdict.transitions",
        "P3b.province.state-assertion-check.landed-exits",
        "P3b.province.state-assertion-check.base-exit",
        "P3b.province.state-assertion-check.base-mismatch",
    ),
    "P3c": (
        "P3c.box.1.pointer.1.needle.1",
        "P3c.box.1.pointer.1.needle.2",
        "P3c.box.1.pointer.1.needle.3",
        "P3c.box.1.pointer.1.needle.4",
        "P3c.box.2.pointer.1",
        "P3c.box.3.pointer.1",
        "P3c.box.4.pointer.1",
    ),
    "P3d": (
        "P3d.axis-table.round24",
        "P3d.axis-table.round25",
        "P3d.axis.novelty.anchor.1.pin",
    ),
    "P3e": (
        "P3e.row-to-file.knowledge/attribution-interval-calibration.md",
        "P3e.row-to-file.lessons/round-24-verifier-spotcheck.md",
        "P3e.row-to-file.lessons/round-25.md",
        "P3e.row-to-file.evidence/round25-sources/",
        "P3e.row-to-file.evidence/round25-calibration/",
        "P3e.file-to-row.knowledge/attribution-interval-calibration.md",
        "P3e.file-to-row.lessons/round-25-verifier-spotcheck.md",
        "P3e.file-to-row.lessons/round-25.md",
        "P3e.file-to-row.evidence/round25-sources/",
        "P3e.file-to-row.evidence/round25-calibration/",
    ),
}

# P4 is frozen at round-27 base b5719440. These ids are the complete base
# population; additions to the inspected documents do not silently widen it.
P4_BASE_COMMIT = "b5719440e5eee46c1886fddbdf7bdc1624829454"
P4A_ASSERTION_IDS = (
    "P4a.scorecard.claim.c1",
    "P4a.scorecard.claim.c2",
    "P4a.scorecard.capability.grader-perturbation-audit",
    "P4a.scorecard.final.c1",
    "P4a.scorecard.final.c2",
    "P4a.scorecard.revision.c1",
    "P4a.scorecard.revision.c2",
    "P4a.scorecard.revision.q13",
    "P4a.scorecard.revision.sources-index",
)
P4B_ARTIFACT_PATHS = (
    "evidence/round26-sources/",
    "evidence/round26-calibration/",
    "../plans/grader_perturb.py",
    "../plans/gate_timing_check.py",
    "../plans/round26_census.sh",
    "../plans/fixtures/r26/",
)

# Exact base erratum in README.md:283-285 corrects the historical source range.
P4B_SOURCE_CORRECTION_ANCHOR = (
    "Round-26 source-support correction: the supporting-artifact row's initial "
    "S043–S047 range is superseded",
    "by **S043–S048**; S048 corrects S043's quote location before knowledge admission",
    "(`lessons/round-26.md` §Source-location correction before admission).",
)
P4B_SOURCE_ID_SET = tuple(f"S{number:03d}" for number in range(43, 49))
P4B_SOURCE_DERIVED_TOKENS = (
    "sources=S043–S048",
    "source_count=6",
    "source_ids=S043,S044,S045,S046,S047,S048",
)
P4B_ASSERTION_IDS = tuple(
    f"P4b.readme.artifact-row.{path}" for path in P4B_ARTIFACT_PATHS
) + (
    "P4b.readme.artifact-inventory",
    "P4b.readme.covers.round26-sources",
)
P4C_ASSERTION_IDS = (
    "P4c.build.seats",
    "P4c.build.role-mix",
    "P4c.build.reports",
    "P4c.falsify.seats",
    "P4c.falsify.role-mix",
    "P4c.falsify.dead-seats",
    "P4c.falsify.reports",
    "P4c.round.total-136",
    "P4c.round.total-139",
    "P4c.r25.raw-tree-entries",
    "P4c.r25.markdown-reports",
)
P4D_FAMILY_ORDER = ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "D1", "G1", "G2")
P4D_FILE_COUNTS = (
    ("corpus/evidence/round8-horizon/results.jsonl", 188),
    ("corpus/evidence/round9-replication/results-r9.jsonl", 128),
    ("corpus/evidence/round11-power/results-r11.jsonl", 320),
    ("corpus/evidence/round12-ladder/results-r12.jsonl", 1328),
)
P4D_ASSERTION_IDS = (
    "P4d.population.records",
    "P4d.population.files",
    "P4d.population.verdicts",
    "P4d.population.graders",
) + tuple(f"P4d.family.{family}" for family in P4D_FAMILY_ORDER)
P4E_SOURCE_IDS = tuple(f"S{number:03d}" for number in range(43, 49))
P4E_CITATION_FILES = (
    "corpus/knowledge/grader-perturbation-audit.md",
    "corpus/lessons/round-26.md",
)
P4E_ASSERTION_IDS = tuple(f"P4e.sources.{source_id}.used-by"
                          for source_id in P4E_SOURCE_IDS)
P4_ASSERTION_IDS = (
    P4A_ASSERTION_IDS + P4B_ASSERTION_IDS + P4C_ASSERTION_IDS
    + P4D_ASSERTION_IDS + P4E_ASSERTION_IDS
)
P4_ASSERTION_INVENTORY_ID = "P4.population.assertion-inventory"

# Corrections must be appended after each frozen document span and must carry
# every re-derived token for one exact assertion id.
P4_CORRECTION_FLOORS = {
    "SCORECARD.md": 810,
    "corpus/README.md": 285,
    "corpus/lessons/round-26.md": 197,
    "corpus/knowledge/grader-perturbation-audit.md": 128,
    "corpus/SOURCES.md": 70,
}
P4_CORRECTION_DOCS = tuple(P4_CORRECTION_FLOORS)
P4_CORRECTION_ID_RE = re.compile(r"^- \*\*(R27-E\d+)\b")
P4_CORRECTION_LINE_RE = re.compile(
    r"^- \*\*(R27-E\d+) \(\d{4}-\d{2}-\d{2}\)\*\* "
    r"supersedes `([^`]+)` — now (`[^`]+`(?: `[^`]+`)*)\.?$"
)
P4_CITATION_RE = re.compile(r"\bS(\d{3})(?:\s*[-–—]\s*S(\d{3}))?\b")

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


def superseding_tokens(
    root: Path, assertion_id: str, document: str = "SCORECARD.md",
) -> tuple[int, list[str]] | None:
    """Latest appended correction in a source document, with its tokens."""
    text = read_repo_text(root, document)
    if text is None:
        return None
    found = None
    for number, line in enumerate(text.splitlines(), 1):
        match = SUPERSEDE_RE.match(line)
        if match and match.group(1) == assertion_id:
            found = (number, code_spans(match.group(2)))
    return found

def p3_superseding_tokens(
    root: Path, assertion_id: str, document: str,
) -> tuple[int, list[str] | None] | None:
    """Parse only unique, strict, post-freeze P3 corrections; never route around bad primary."""
    primary = "SCORECARD.md" if document == "SHONEN.md" else document
    if primary not in P3_CORRECTION_FLOORS:
        primary = "SCORECARD.md"
    candidates = [primary]
    if primary != "SCORECARD.md":
        candidates.append("SCORECARD.md")

    texts = {name: read_repo_text(root, name) for name in P3_CORRECTION_DOCS}
    id_counts: dict[str, int] = {}
    for text in texts.values():
        for line in (text or "").splitlines():
            match = P3_CORRECTION_ID_RE.match(line)
            if match:
                correction_id = match.group(1)
                id_counts[correction_id] = id_counts.get(correction_id, 0) + 1

    for candidate in candidates:
        text = texts.get(candidate)
        if text is None:
            continue
        matching = []
        for number, line in enumerate(text.splitlines(), 1):
            match = SUPERSEDE_RE.match(line)
            if match and match.group(1) == assertion_id:
                matching.append((number, line))
        if not matching:
            continue
        number, line = matching[-1]
        parsed = P3_CORRECTION_LINE_RE.fullmatch(line)
        if number <= P3_CORRECTION_FLOORS[candidate] or parsed is None:
            return number, None
        correction_id = parsed.group(1)
        if parsed.group(2) != assertion_id or id_counts.get(correction_id) != 1:
            return number, None
        return number, code_spans(parsed.group(3))
    return None


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


def named_table_row(
    lines: list[str], key: str, start: int = 0, end: int | None = None,
) -> tuple[int, list[str]] | None:
    stop = len(lines) if end is None else end
    for line_number, cells in table_rows(lines, start, stop):
        if cells and cells[0].strip().strip("`") == key:
            return line_number, cells
    return None


def p3_record(
    root: Path,
    out: list[Assertion],
    assertion_id: str,
    source_line: int | None,
    check: bool,
    observed: Any,
    derived_tokens: list[str] | None,
    document: str,
) -> None:
    verdict = "MATCH" if check else "MISMATCH"
    correction = None
    if not check and derived_tokens is not None:
        correction = p3_superseding_tokens(root, assertion_id, document)
        if correction is not None and correction[1] == derived_tokens:
            verdict = "SUPERSEDED"
    details = {
        "observed": observed,
        "assertion_document": document,
        "derived_tokens": derived_tokens,
        "correction_line": correction[0] if correction else None,
        "correction_tokens": correction[1] if correction else None,
    }
    add(out, assertion_id, source_line, "frozen P3 assertion and full-value supersession",
        details, verdict)


def regex_groups(text: str | None, pattern: str) -> tuple[str, ...] | None:
    if text is None:
        return None
    match = re.search(pattern, text, re.MULTILINE)
    return tuple(match.groups()) if match else None

def regex_group_matches(
    text: str | None, pattern: str,
) -> list[tuple[str, ...]]:
    if text is None:
        return []
    return [tuple(match.groups()) for match in re.finditer(pattern, text, re.MULTILINE)]


def p3_selftest_red_run_ids(text: str | None) -> tuple[int, ...] | None:
    if text is None:
        return None
    return tuple(sorted({
        int(match.group(1))
        for match in re.finditer(r"(?m)^selftest ok\s+R(\d+)[A-Za-z]*:", text)
    }))


def p3_compare_groups(
    root: Path,
    out: list[Assertion],
    assertion_id: str,
    source_line: int | None,
    claim_text: str,
    claim_pattern: str,
    receipt_text: str | None,
    receipt_pattern: str,
    token_names: tuple[str, ...],
    document: str,
    token_templates: tuple[str, ...] | None = None,
) -> None:
    claim_occurrences = regex_group_matches(claim_text, claim_pattern)
    receipt_occurrences = regex_group_matches(receipt_text, receipt_pattern)
    claim = claim_occurrences[0] if len(claim_occurrences) == 1 else None
    truth = receipt_occurrences[0] if len(receipt_occurrences) == 1 else None
    expected_tokens = (
        [template.format(value=value)
         for template, value in zip(token_templates, truth)]
        if truth is not None and token_templates is not None
        and len(truth) == len(token_templates)
        else ([f"{name}={value}" for name, value in zip(token_names, truth)]
              if truth is not None and len(truth) == len(token_names) else None)
    )
    p3_record(root, out, assertion_id, source_line,
              len(claim_occurrences) == 1 and len(receipt_occurrences) == 1
              and claim == truth,
              {"claim": claim, "receipt": truth,
               "claim_occurrences": claim_occurrences,
               "receipt_occurrences": receipt_occurrences},
              expected_tokens, document)


def capability_evidence_row(
    root: Path, capability: str,
) -> tuple[int, str] | None:
    text = read_repo_text(root, "SCORECARD.md")
    if text is None:
        return None
    lines = physical_lines(text)
    heading = find_line(lines, lambda line: line == "## Capabilities")
    if heading is None:
        return None
    row = named_table_row(lines, capability, heading + 1, next_h2(lines, heading))
    if row is None:
        return None
    line_number, cells = row
    return line_number, cells[2] if len(cells) > 2 else ""

def p3a_unclassified_numeric_tokens(text: str | None) -> list[tuple[str, int]] | None:
    if text is None:
        return None
    claimed_spans: set[tuple[int, int]] = set()
    for pattern in P3A_NUMERIC_FIELD_PATTERNS:
        for match in re.finditer(pattern, text):
            for group_number in range(1, len(match.groups()) + 1):
                start, end = match.span(group_number)
                claimed_spans.update(
                    number.span()
                    for number in P3A_NUMERIC_TOKEN_RE.finditer(text, start, end))
    return [
        (number.group(), number.start())
        for number in P3A_NUMERIC_TOKEN_RE.finditer(text)
        if number.span() not in claimed_spans
    ]


def check_p3a(root: Path, out: list[Assertion]) -> None:
    interval = capability_evidence_row(root, "interval-reverdict")
    state = capability_evidence_row(root, "state-assertion-check")
    summary = read_repo_text(root, P3A_INTERVAL_SUMMARY)
    interval_selftest = read_repo_text(root, P3A_INTERVAL_SELFTEST)
    state_base = read_repo_text(root, P3A_STATE_BASE)
    state_after = read_repo_text(root, P3A_STATE_AFTER)

    for metric, pattern, names in (
        ("unique-samples", r"unique_samples=(\d+)", ("unique_samples",)),
        ("scored-trials", r"scored_trials=(\d+)\s+correct=(\d+)",
         ("scored_trials", "correct")),
        ("transitions",
         r"transitions=(FAIL>UNTESTED:\d+,PASS>INDETERMINATE:\d+,PASS>PASS:\d+)",
         ("transitions",)),
        ("mismatches", r"mismatches=(\d+)", ("mismatches",)),
    ):
        p3_compare_groups(
            root, out, f"P3a.capability.interval-reverdict.{metric}",
            interval[0] if interval else None, interval[1] if interval else "",
            pattern, summary, pattern, names, "SCORECARD.md")
    p3_compare_groups(
        root, out, "P3a.capability.interval-reverdict.summary-exit",
        interval[0] if interval else None, interval[1] if interval else "",
        r"exit\s+(\d+)", summary, r"(?m)^exit=(\d+)",
        ("exit",), "SCORECARD.md")

    p3_compare_groups(
        root, out, "P3a.capability.interval-reverdict.selftest-checks",
        interval[0] if interval else None, interval[1] if interval else "",
        r"--selftest`?\s+(\d+)\s+checks?\s+(\d+)\s+failed",
        interval_selftest, r"selftest:\s*(\d+)\s+checks,\s*(\d+)\s+failed",
        ("checks", "failed"), "SCORECARD.md", ("{value} checks", "{value} failed"))
    run_range_matches = regex_group_matches(
        interval[1] if interval else "",
        r"\bred runs R(\d+)[–-]R(\d+)\s+included\b")
    receipt_red_runs = p3_selftest_red_run_ids(interval_selftest)
    claimed_range = (tuple(int(value) for value in run_range_matches[0])
                     if len(run_range_matches) == 1 else None)
    expected_runs = (tuple(range(claimed_range[0], claimed_range[1] + 1))
                     if claimed_range is not None and claimed_range[0] <= claimed_range[1]
                     else None)
    derived_tokens = (
        [f"receipt_red_runs={','.join(f'R{i}' for i in receipt_red_runs) or 'none'}"]
        if receipt_red_runs is not None else None)
    p3_record(
        root, out, "P3a.capability.interval-reverdict.selftest-red-runs",
        interval[0] if interval else None,
        len(run_range_matches) == 1 and expected_runs is not None
        and expected_runs == receipt_red_runs,
        {"claim_ranges": run_range_matches, "receipt_red_runs": receipt_red_runs},
        derived_tokens, "SCORECARD.md")
    p3_compare_groups(
        root, out, "P3a.capability.state-assertion-check.base-mismatch",
        state[0] if state else None, state[1] if state else "",
        r"base\s+`?6180e4f`?.*?mismatch=(\d+)",
        state_base, r"(?m)^assertions=.*?\bmismatch=(\d+)",
        ("mismatch",), "SCORECARD.md")
    p3_compare_groups(
        root, out, "P3a.capability.state-assertion-check.base-exit",
        state[0] if state else None, state[1] if state else "",
        r"base\s+`?6180e4f`?.*?exit\s+(\d+)",
        state_base, r"(?m)^exit=(\d+)", ("exit",), "SCORECARD.md")
    p3_compare_groups(
        root, out, "P3a.capability.state-assertion-check.landed-mismatch",
        state[0] if state else None, state[1] if state else "",
        r"landed tree\s+`?mismatch=(\d+)",
        state_after, r"(?m)^assertions=.*?\bmismatch=(\d+)",
        ("mismatch",), "SCORECARD.md")
    p3_compare_groups(
        root, out, "P3a.capability.state-assertion-check.landed-superseded",
        state[0] if state else None, state[1] if state else "",
        r"landed tree\s+`?mismatch=\d+\s+superseded=(\d+)",
        state_after, r"(?m)^assertions=.*?\bsuperseded=(\d+)",
        ("superseded",), "SCORECARD.md")
    p3_compare_groups(
        root, out, "P3a.capability.state-assertion-check.landed-exit",
        state[0] if state else None, state[1] if state else "",
        r"landed tree.*?exit\s+(\d+)",
        state_after, r"(?m)^exit=(\d+)", ("exit",), "SCORECARD.md")
    for assertion_id, row in (
        ("P3a.capability.interval-reverdict.numeric-token-audit", interval),
        ("P3a.capability.state-assertion-check.numeric-token-audit", state),
    ):
        evidence = row[1] if row else None
        unclassified = p3a_unclassified_numeric_tokens(evidence)
        add(out, assertion_id, row[0] if row else None,
            "every semantic numeric token in this evidence cell is receipt-backed",
            {"unclassified_numeric_tokens": unclassified},
            "MATCH" if unclassified == [] else "MISMATCH")


def p3_sources_census(root: Path) -> dict[str, Any] | None:
    text = read_repo_text(root, "corpus/SOURCES.md")
    if text is None:
        return None
    ids = []
    for line in text.splitlines():
        match = re.match(r"^\|\s*S(\d{3,})\s*\|", line)
        if match and int(match.group(1)) <= P3B_SOURCES_MAX_ID:
            ids.append(int(match.group(1)))
    expected_ids = set(range(1, P3B_SOURCES_MAX_ID + 1))
    counts: dict[int, int] = {}
    for source_id in ids:
        counts[source_id] = counts.get(source_id, 0) + 1
    missing = sorted(expected_ids - set(ids))
    duplicates = sorted(source_id for source_id, count in counts.items() if count > 1)
    unexpected = sorted(set(ids) - expected_ids)
    return {
        "rows": len(ids),
        "ids": sorted(ids),
        "exact_id_set": sorted(ids) == list(range(1, P3B_SOURCES_MAX_ID + 1)),
        "missing_ids": missing,
        "duplicate_ids": duplicates,
        "unexpected_ids": unexpected,
    }


def p3_sources_tokens(census: dict[str, Any] | None) -> list[str] | None:
    if census is None:
        return None
    if census["exact_id_set"]:
        id_set = "exact"
    else:
        def ids_text(values: list[int]) -> str:
            return ",".join(f"S{source_id:03d}" for source_id in values) or "none"
        id_set = (f"missing:{ids_text(census['missing_ids'])};"
                  f"duplicate:{ids_text(census['duplicate_ids'])};"
                  f"unexpected:{ids_text(census['unexpected_ids'])}")
    return [f"rows={census['rows']}", f"id_set={id_set}"]


def province_row(
    root: Path, key: str,
) -> tuple[int, list[str]] | None:
    text = read_repo_text(root, "PROVINCE.md")
    if text is None:
        return None
    return named_table_row(physical_lines(text), key)


def receipt_exit(text: str | None) -> str | None:
    matches = re.findall(r"(?m)^exit=(\d+)\s*$", text or "")
    return matches[-1] if matches else None


def check_p3b(root: Path, out: list[Assertion]) -> None:
    province_text = read_repo_text(root, "PROVINCE.md")
    province_lines = physical_lines(province_text) if province_text is not None else []
    census = p3_sources_census(root)
    count = census["rows"] if census is not None else None
    exact_id_set = census is not None and census["exact_id_set"]

    registry_row = province_row(root, "Public-literature registry")
    registry_text = " | ".join(registry_row[1]) if registry_row else ""
    registry_count = regex_groups(registry_text, r"\b(\d+)\s+rows?\b")
    derived_tokens = p3_sources_tokens(census)
    p3_record(root, out, "P3b.province.public-literature-registry.rows",
              registry_row[0] if registry_row else None,
              count is not None and exact_id_set
              and registry_count == (str(P3B_SOURCES_MAX_ID),),
              {"claim": registry_count, "SOURCES_frozen_census": census},
              derived_tokens, "PROVINCE.md")

    correction_line = find_line(
        province_lines,
        lambda line: "Round-25 correction" in line and "Public-literature registry" in line)
    correction_text = line_text(province_lines[correction_line]) if correction_line is not None else ""
    correction_count = regex_groups(
        correction_text, r"holds\s+(\d+)\s+after round 25")
    p3_record(root, out, "P3b.province.round25-correction.rows",
              correction_line + 1 if correction_line is not None else None,
              count is not None and exact_id_set
              and correction_count == (str(P3B_SOURCES_MAX_ID),),
              {"claim": correction_count, "SOURCES_frozen_census": census},
              derived_tokens, "PROVINCE.md")

    interval_row = province_row(root, "Interval re-verdict instrument (round 25)")
    interval_text = " | ".join(interval_row[1]) if interval_row else ""
    interval_summary = read_repo_text(root, P3A_INTERVAL_SUMMARY)
    interval_selftest = read_repo_text(root, P3A_INTERVAL_SELFTEST)
    interval_exits = regex_groups(interval_text, r"exit\s+(\d+)\s*/\s*exit\s+(\d+)")
    expected_exits = (receipt_exit(interval_summary), receipt_exit(interval_selftest))
    p3_record(root, out, "P3b.province.interval-reverdict.exits",
              interval_row[0] if interval_row else None,
              interval_exits is not None and interval_exits == expected_exits
              and None not in expected_exits,
              {"claim": interval_exits, "receipts": expected_exits},
              [f"summary_exit={expected_exits[0]}", f"selftest_exit={expected_exits[1]}"]
              if None not in expected_exits else None,
              "PROVINCE.md")
    p3_compare_groups(
        root, out, "P3b.province.interval-reverdict.unique-samples",
        interval_row[0] if interval_row else None, interval_text,
        r"(\d+)\s+unique samples", interval_summary,
        r"unique_samples=(\d+)", ("unique_samples",), "PROVINCE.md")
    p3_compare_groups(
        root, out, "P3b.province.interval-reverdict.scored-trials",
        interval_row[0] if interval_row else None, interval_text,
        r"(\d+)/(\d+)\s+correct", interval_summary,
        r"scored_trials=(\d+)\s+correct=(\d+)",
        ("scored_trials", "correct"), "PROVINCE.md")
    p3_compare_groups(
        root, out, "P3b.province.interval-reverdict.transitions",
        interval_row[0] if interval_row else None, interval_text,
        r"transitions\s+FAIL>UNTESTED\s+(\d+),?\s*PASS>INDETERMINATE\s+(\d+)",
        interval_summary,
        r"transitions=FAIL>UNTESTED:(\d+),PASS>INDETERMINATE:(\d+)",
        ("FAIL>UNTESTED", "PASS>INDETERMINATE"), "PROVINCE.md")

    state_row = province_row(root, "State-assertion check (round 25)")
    state_text = " | ".join(state_row[1]) if state_row else ""
    state_base = read_repo_text(root, P3A_STATE_BASE)
    state_after = read_repo_text(root, P3A_STATE_AFTER)
    state_selftest = read_repo_text(root, P3A_STATE_SELFTEST)
    state_exits = regex_groups(state_text, r"exit\s+(\d+)\s*/\s*exit\s+(\d+)")
    landed_exits = (receipt_exit(state_after), receipt_exit(state_selftest))
    p3_record(root, out, "P3b.province.state-assertion-check.landed-exits",
              state_row[0] if state_row else None,
              state_exits is not None and state_exits == landed_exits
              and None not in landed_exits,
              {"claim": state_exits, "receipts": landed_exits},
              [f"summary_exit={landed_exits[0]}", f"selftest_exit={landed_exits[1]}"]
              if None not in landed_exits else None,
              "PROVINCE.md")
    base_claim = regex_groups(state_text, r"base.*?exit\s+(\d+),\s*(\d+)\s+mismatches")
    base_receipt_exit = receipt_exit(state_base)
    base_receipt_mismatch = regex_groups(state_base, r"(?m)^assertions=.*?\bmismatch=(\d+)")
    p3_record(root, out, "P3b.province.state-assertion-check.base-exit",
              state_row[0] if state_row else None,
              base_claim is not None and base_receipt_exit is not None
              and base_claim[0] == base_receipt_exit,
              {"claim": base_claim[0] if base_claim else None,
               "receipt": base_receipt_exit},
              [f"exit={base_receipt_exit}"] if base_receipt_exit is not None else None,
              "PROVINCE.md")
    p3_record(root, out, "P3b.province.state-assertion-check.base-mismatch",
              state_row[0] if state_row else None,
              base_claim is not None and base_receipt_mismatch is not None
              and base_claim[1] == base_receipt_mismatch[0],
              {"claim": base_claim[1] if base_claim else None,
               "receipt": base_receipt_mismatch[0] if base_receipt_mismatch else None},
              [f"{base_receipt_mismatch[0]} mismatches"]
              if base_receipt_mismatch is not None else None,
              "PROVINCE.md")


def check_p3c(root: Path, out: list[Assertion]) -> None:
    text = read_repo_text(root, "SHONEN.md")
    lines = physical_lines(text) if text is not None else []
    evidence_rows: list[tuple[int, int, list[str]]] = []
    for index, line in enumerate(lines):
        if not shonen_box_line(content_text(line)):
            continue
        cursor = index + 1
        while cursor < len(lines):
            evidence_text = content_text(lines[cursor])
            if not evidence_text.startswith(("  ", "\t")) or not evidence_text.strip():
                break
            refs = [match.group(0) for match in FILE_REF_RE.finditer(evidence_text)]
            evidence_rows.append((len(evidence_rows) + 1, cursor + 1, refs))
            cursor += 1

    for box_number, pointer, target_line, token, needle_number in P3C_PINS:
        evidence = next((row for row in evidence_rows if row[0] == box_number), None)
        source_line = evidence[1] if evidence else None
        refs = evidence[2] if evidence else []
        actual_pointer = refs[0] if refs else None
        pointer_count = sum(
            bool(row[2]) and row[2][0] == pointer for row in evidence_rows)
        target_path = pointer.split(":", 1)[0]
        target_text = read_repo_text(root, target_path)
        target_lines = physical_lines(target_text) if target_text is not None else []
        observed_line = (content_text(target_lines[target_line - 1])
                         if target_line is not None and 1 <= target_line <= len(target_lines)
                         else "")
        token_hits = ((target_text or "").count(token) if target_line is None
                      else observed_line.count(token))
        target_ok = (target_text is not None and token_hits == 1
                     if target_line is None
                     else target_line <= len(target_lines) and token_hits == 1)
        derived_tokens = [
            f"pointer={actual_pointer or '<missing>'}",
            f"pointer_count={pointer_count}",
            f"target={target_path}:{target_line if target_line is not None else 'whole-file'}",
            f"token={token}",
            f"token_hits={token_hits}",
        ]
        if target_line is not None:
            line_text = (observed_line if target_line <= len(target_lines)
                         else "<missing>")
            derived_tokens.append(f"line_text={line_text or '<blank>'}")
        if actual_pointer != pointer:
            derived_tokens = None
        suffix = f".needle.{needle_number}" if needle_number is not None else ""
        assertion_id = f"P3c.box.{box_number}.pointer.1{suffix}"
        ok = actual_pointer == pointer and pointer_count == 1 and target_ok
        p3_record(root, out, assertion_id, source_line, ok,
                  {"pointer": actual_pointer, "pointer_count": pointer_count,
                   "target_line": target_line, "target_text": observed_line,
                   "token": token, "token_hits": token_hits},
                  derived_tokens, "SHONEN.md")
        for extra_pointer in refs[1:]:
            add(out, f"P3c.out-of-population.pointer.{extra_pointer}@{source_line}",
                source_line, "additional SHONEN evidence pointer outside frozen P3",
                extra_pointer, "OUT_OF_POPULATION")
    for box_number, source_line, refs in evidence_rows[4:]:
        for pointer in refs:
            add(out, f"P3c.out-of-population.pointer.{pointer}@{source_line}",
                source_line, "SHONEN evidence pointer outside the frozen f11bffbf population",
                pointer, "OUT_OF_POPULATION")


def axis_anchor_inventory(
    root: Path,
) -> tuple[list[str], dict[tuple[str, str], list[tuple[str, int, int]]]]:
    text = read_repo_text(root, "SCORECARD.md")
    if text is None:
        return [], {}
    lines = physical_lines(text)
    present: list[str] = []
    anchors: dict[tuple[str, str], list[tuple[str, int, int]]] = {}
    for table_id, marker, header_text in P3D_TABLES:
        marker_line = find_line(lines, lambda line: marker in line)
        if marker_line is None:
            continue
        header = find_line(lines, lambda line: line == header_text, marker_line + 1)
        if header is None:
            continue
        present.append(table_id)
        end = header + 2
        while end < len(lines) and table_cells(content_text(lines[end])) is not None:
            end += 1
        axis_indices: dict[str, int] = {}
        for line_number, cells in table_rows(lines, header + 2, end):
            if len(cells) < 3:
                continue
            axis = cells[0].strip().strip("`")
            for span in code_spans(cells[2]):
                if re.fullmatch(r":\d+(?:-\d+)?", span):
                    axis_indices[axis] = axis_indices.get(axis, 0) + 1
                    anchors.setdefault((table_id, span), []).append(
                        (axis, axis_indices[axis], line_number))
    return present, anchors


def check_p3d(root: Path, out: list[Assertion]) -> None:
    text = read_repo_text(root, "SCORECARD.md")
    lines = physical_lines(text) if text is not None else []
    present, anchors = axis_anchor_inventory(root)
    for table_id, _, _ in P3D_TABLES:
        ok = table_id in present
        p3_record(root, out, f"P3d.axis-table.{table_id}", None, ok,
                  {"table": table_id, "present": ok},
                  [f"table={table_id}", f"present={str(ok).lower()}"],
                  "SCORECARD.md")
    for (table_id, anchor), (axis, needles) in P3D_ANCHORS.items():
        hits = anchors.get((table_id, anchor), [])
        source_line = hits[0][2] if hits else None
        match = re.fullmatch(r":(\d+)(?:-(\d+))?", anchor)
        start = int(match.group(1)) if match else 0
        stop = int(match.group(2) or start) if match else 0
        in_range = 1 <= start <= stop <= len(lines)
        anchored = content_text(lines[start - 1]) if in_range else ""
        needle_hits = {needle: anchored.count(needle) for needle in needles}
        ok = (len(hits) == 1 and hits[0][0] == axis and in_range
              and all(count == 1 for count in needle_hits.values()))
        actual_axis = hits[0][0] if hits else "<missing>"
        line_text = (anchored if in_range and anchored else
                     "<blank>" if in_range else "<missing>")
        derived_tokens = [
            f"table={table_id}", f"axis={actual_axis}", f"anchor={anchor}",
            f"reference_count={len(hits)}", f"line={start}",
            f"line_text={line_text}",
            *[f"{needle}={count}" for needle, count in needle_hits.items()],
        ]
        p3_record(root, out, f"P3d.axis.{axis}.anchor.1.pin", source_line, ok,
                  {"table": table_id, "anchor": anchor, "hits": hits,
                   "anchored_line": anchored, "needle_hits": needle_hits},
                  derived_tokens, "SCORECARD.md")
    for key, hits in anchors.items():
        if key in P3D_ANCHORS:
            continue
        for axis, occurrence, source_line in hits:
            add(out, f"P3d.out-of-population.{key[0]}.{axis}.anchor.{occurrence}",
                source_line, "axis-table anchor outside frozen f11bffbf population",
                {"anchor": key[1], "axis": axis}, "OUT_OF_POPULATION")


def check_p3e(root: Path, out: list[Assertion]) -> None:
    rows, anchors = readme_index_rows(root)
    row_locations: dict[str, list[int]] = {}
    for relative, line_number in rows:
        row_locations.setdefault(relative, []).append(line_number)
    for relative in P3E_ROW_PATHS:
        locs = row_locations.get(relative, [])
        exists = path_exists(root, relative)
        source_line = locs[0] if locs else anchors.get(relative.split("/", 1)[0] + "/")
        expected = [f"path={relative}", f"exists={str(exists).lower()}",
                    f"row_count={len(locs)}"]
        observed = {"path": relative, "exists": exists, "row_lines": locs}
        p3_record(root, out, f"P3e.row-to-file.{relative}", source_line,
                  exists and len(locs) == 1, observed, expected, "corpus/README.md")
    for relative in P3E_FILE_PATHS:
        locs = row_locations.get(relative, [])
        exists = path_exists(root, relative)
        source_line = locs[0] if locs else anchors.get(relative.split("/", 1)[0] + "/")
        expected = [f"path={relative}", f"exists={str(exists).lower()}",
                    f"row_count={len(locs)}"]
        observed = {"path": relative, "exists": exists, "row_lines": locs}
        p3_record(root, out, f"P3e.file-to-row.{relative}", source_line,
                  exists and len(locs) == 1, observed, expected, "corpus/README.md")


def check_p3(root: Path, out: list[Assertion]) -> None:
    check_p3a(root, out)
    check_p3b(root, out)
    check_p3c(root, out)
    check_p3d(root, out)
    check_p3e(root, out)

class P4Evidence:
    """Run only the pinned offline commands used by the P4 population."""

    COMMANDS = {
        "grader_summary": ("python3", "plans/grader_perturb.py", "--summary"),
        "grader_json": ("python3", "plans/grader_perturb.py", "--json"),
        "oracle": ("python3", "plans/fixtures/r26/perturb_oracle.py", "--root", "."),
    }

    def __init__(self, root: Path):
        self.root = root
        self.cache: dict[str, dict[str, Any]] = {}

    def command(self, name: str) -> dict[str, Any]:
        if name in self.cache:
            return self.cache[name]
        argv = self.COMMANDS.get(name)
        if argv is None:
            result = {"returncode": None, "stdout": "", "stderr": "unknown P4 command"}
            self.cache[name] = result
            return result
        try:
            proc = subprocess.run(
                argv,
                cwd=self.root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                check=False,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            result = {"returncode": proc.returncode, "stdout": proc.stdout,
                      "stderr": proc.stderr}
        except (OSError, subprocess.TimeoutExpired) as exc:
            result = {"returncode": None, "stdout": "",
                      "stderr": f"{type(exc).__name__}: {exc}"}
        self.cache[name] = result
        return result


P4_CORRECTION_LINE_RE = re.compile(
    r"^- \*\*(R27-E\d+) \(\d{4}-\d{2}-\d{2}\)\*\* "
    r"supersedes `([^`]+)` — now (`[^`]+`(?: `[^`]+`)*)\.?$"
)


def p4_superseding_tokens(
    root: Path, assertion_id: str, document: str,
) -> tuple[int, list[str] | None] | None:
    if document not in P4_CORRECTION_FLOORS:
        return None
    texts = {name: read_repo_text(root, name) for name in P4_CORRECTION_DOCS}
    correction_id_counts: dict[str, int] = {}
    for text in texts.values():
        for line in (text or "").splitlines():
            match = P4_CORRECTION_ID_RE.match(line)
            if match:
                correction_id_counts[match.group(1)] = (
                    correction_id_counts.get(match.group(1), 0) + 1
                )
    lines = (texts[document] or "").splitlines()
    matching = [
        (number, line) for number, line in enumerate(lines, 1)
        if number > P4_CORRECTION_FLOORS[document]
        and (match := P4_CORRECTION_ID_RE.match(line))
        and (parsed := P4_CORRECTION_LINE_RE.fullmatch(line))
        and parsed.group(2) == assertion_id
    ]
    if not matching:
        return None
    number, line = matching[-1]
    parsed = P4_CORRECTION_LINE_RE.fullmatch(line)
    if parsed is None or correction_id_counts.get(parsed.group(1)) != 1:
        return number, None
    return number, code_spans(parsed.group(3))


def p4_record(
    root: Path,
    out: list[Assertion],
    assertion_id: str,
    source_line: int | None,
    check: bool,
    observed: Any,
    derived_tokens: list[str] | None,
    document: str,
) -> None:
    verdict = "MATCH" if check else "MISMATCH"
    correction = None
    if not check and derived_tokens is not None:
        correction = p4_superseding_tokens(root, assertion_id, document)
        if correction is not None and correction[1] == derived_tokens:
            verdict = "SUPERSEDED"
    add(out, assertion_id, source_line, "frozen P4 assertion and full-value supersession",
        {"observed": observed, "assertion_document": document,
         "derived_tokens": derived_tokens,
         "correction_line": correction[0] if correction else None,
         "correction_tokens": correction[1] if correction else None},
        verdict)


def p4_numbered_line(
    lines: list[str], predicate, start: int = 0, end: int | None = None,
) -> tuple[int, str] | None:
    stop = len(lines) if end is None else end
    index = find_line(lines, predicate, start)
    if index is None or index >= stop:
        return None
    return index + 1, content_text(lines[index])


def p4_groups(text: str | None, pattern: str, flags: int = 0) -> tuple[str, ...] | None:
    if text is None:
        return None
    matches = list(re.finditer(pattern, text, flags))
    return tuple(matches[0].groups()) if len(matches) == 1 else None


def p4_receipt_summary(text: str | None) -> dict[str, int] | None:
    groups = p4_groups(
        text,
        r"(?m)^assertions=(\d+)\s+match=(\d+)\s+mismatch=(\d+)\s+"
        r"superseded=(\d+)\s+offline_unverifiable=(\d+)\s*$",
    )
    if groups is None:
        return None
    names = ("assertions", "match", "mismatch", "superseded", "offline_unverifiable")
    return dict(zip(names, (int(value) for value in groups)))


def p4_kv_receipt(text: str | None) -> dict[str, str]:
    return {
        match.group(1): match.group(2)
        for match in re.finditer(r"(?m)^([A-Za-z0-9_]+)=(.*)$", text or "")
    }


def p4_round24_scores(lines: list[str]) -> dict[str, int] | None:
    marker = find_line(lines, lambda line: line.startswith("Re-derived axis state, round 24"))
    if marker is None:
        return None
    header = find_line(lines, lambda line: line == "| Axis | Round-24 value | Basis |",
                       marker + 1)
    if header is None:
        return None
    scores: dict[str, int] = {}
    for _, cells in table_rows(lines, header + 2, next_h2(lines, header)):
        if len(cells) >= 2 and cells[0] in {"novelty", "calibration"}:
            try:
                scores[cells[0]] = int(cells[1])
            except ValueError:
                return None
    return scores if set(scores) == {"novelty", "calibration"} else None


def p4_word_number(value: str | None) -> int | None:
    if value is None:
        return None
    words = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
             "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
             "eleven": 11}
    return int(value) if value.isdecimal() else words.get(value.lower())


def p4a_summary_values(text: str | None) -> dict[str, Any] | None:
    total = p4_groups(
        text,
        r"(?m)^TOTAL population=(\d+) excluded=(\d+) audited_verdicts=(\d+) "
        r"policy_checks=(\d+) families_with_interval_verdict=(\d+)\s*$",
    )
    family = p4_groups(
        text,
        r"(?m)^FAMILY F1\b.*?\bn=(\d+)\s+k=(\d+).*?composite=(\d+)/(\d+)",
    )
    multi = p4_groups(text, r"(?m)^CLASSES F1\b.*?\bMULTI=(\d+)/(\d+)")
    if total is None or family is None or multi is None:
        return None
    values = [int(value) for value in total]
    return {
        "population": values[0],
        "excluded": values[1],
        "audited_verdicts": values[2],
        "policy_checks": values[3],
        "families": values[4],
        "f1_n": int(family[0]),
        "f1_k": int(family[1]),
        "composite_n": int(family[2]),
        "composite_k": int(family[3]),
        "multi_n": int(multi[0]),
        "multi_k": int(multi[1]),
    }


def check_p4a(root: Path, out: list[Assertion], evidence: P4Evidence) -> None:
    scorecard = read_repo_text(root, "SCORECARD.md")
    lines = physical_lines(scorecard) if scorecard is not None else []
    start_receipt = read_repo_text(root, "corpus/evidence/round26-calibration/round-start.txt")
    base_receipt = read_repo_text(
        root, "corpus/evidence/round26-calibration/state-check-base-f11bffbf.txt")
    final_receipt = read_repo_text(root, "corpus/evidence/round26-calibration/state-check-final.txt")
    census_receipt = read_repo_text(
        root, "corpus/evidence/round26-calibration/round26-census-after.txt")
    gate_receipt = read_repo_text(
        root, "corpus/evidence/round26-calibration/gate-timing-actual-commit.txt")
    source_receipt = read_repo_text(
        root, "corpus/evidence/round26-calibration/sources-census-final.txt")
    summary_result = evidence.command("grader_summary")
    summary = p4a_summary_values(summary_result.get("stdout"))
    base_state = p4_receipt_summary(base_receipt)
    final_state = p4_receipt_summary(final_receipt)
    census = p4_kv_receipt(census_receipt)
    axis_scores = p4_round24_scores(lines)
    start_is_absent = bool(
        start_receipt
        and "git cat-file -e f11bffbf:plans/grader_perturb.py" in start_receipt
        and "does not exist in 'f11bffbf'" in start_receipt
        and re.search(r"(?m)^exit=128$", start_receipt)
    )

    c1 = p4_numbered_line(
        lines, lambda line: line.startswith("| C1 finite-corpus response-format audit"))
    c2 = p4_numbered_line(
        lines, lambda line: line.startswith("| C2 content-pinned frozen self-assertions"))
    capability = p4_numbered_line(
        lines, lambda line: line.startswith("| grader-perturbation-audit |"))
    c1_claim = p4_groups(
        c1[1] if c1 else None,
        r"(\d+)\s*→\s*(\d+)\s+audited verdicts across\s*(\d+)\s*MP/MC "
        r"interval-verdict families,\s*plus\s*(\d+)\s*NOT_SCORED policy captures",
    )
    c1_score = p4_groups(c1[1] if c1 else None, r"\|\s*(\d+)\s*→\s*(\d+)\s*held")
    c2_claim = p4_groups(c2[1] if c2 else None, r"reports\s*(\d+)\s+P3 mismatches")
    c2_score = p4_groups(c2[1] if c2 else None, r"\|\s*(\d+)\s*→\s*(\d+)\s*held")
    c1_expected = (
        "0",
        str(summary["audited_verdicts"]) if summary else None,
        str(summary["families"]) if summary else None,
        str(summary["policy_checks"]) if summary else None,
    )
    c1_score_expected = (
        str(axis_scores.get("novelty")) if axis_scores else None,
        str(axis_scores.get("novelty")) if axis_scores else None,
    )
    c1_ok = (
        start_is_absent and summary_result.get("returncode") == 0
        and c1_claim == c1_expected and c1_score == c1_score_expected
    )
    p4_record(
        root, out, P4A_ASSERTION_IDS[0], c1[0] if c1 else None, c1_ok,
        {"claim": c1_claim, "score": c1_score, "receipt_baseline": 0,
         "grader_summary": summary, "command_exit": summary_result.get("returncode")},
        [f"baseline=0", f"audited_verdicts={c1_expected[1]}",
         f"families={c1_expected[2]}", f"policy_checks={c1_expected[3]}",
         f"novelty={c1_score_expected[0]}→{c1_score_expected[1]}"]
        if summary and axis_scores else None,
        "SCORECARD.md",
    )

    base_mismatch = base_state.get("mismatch") if base_state else None
    c2_score_expected = (
        str(axis_scores.get("calibration")) if axis_scores else None,
        str(axis_scores.get("calibration")) if axis_scores else None,
    )
    c2_ok = (
        c2_claim == (str(base_mismatch),) if base_mismatch is not None else False
    ) and c2_score == c2_score_expected
    p4_record(
        root, out, P4A_ASSERTION_IDS[1], c2[0] if c2 else None, c2_ok,
        {"claim_base_mismatch": c2_claim, "receipt_base": base_state,
         "claim_score": c2_score, "axis_scores": axis_scores},
        [f"base_mismatch={base_mismatch}",
         f"calibration={c2_score_expected[0]}→{c2_score_expected[1]}"]
        if base_state and axis_scores else None,
        "SCORECARD.md",
    )

    capability_text = capability[1] if capability else ""
    capability_round = p4_groups(capability_text, r"\|\s*(\d+)\s*\|\s*$")
    capability_ok = (
        summary_result.get("returncode") == 0 and summary is not None
        and capability_round == ("26",)
        and "plans/grader_perturb.py --summary" in capability_text
        and "independent oracle" in capability_text
        and "corpus/evidence/round26-calibration/" in capability_text
    )
    p4_record(
        root, out, P4A_ASSERTION_IDS[2], capability[0] if capability else None,
        capability_ok,
        {"row": capability_text, "grader_summary": summary,
         "command_exit": summary_result.get("returncode")},
        [f"round=26", f"audited_verdicts={summary['audited_verdicts']}",
         f"policy_checks={summary['policy_checks']}",
         f"families={summary['families']}"] if summary else None,
        "SCORECARD.md",
    )

    outcomes_start = find_line(
        lines, lambda line: line.startswith("### Round-26 final measured outcomes"))
    revision_start = find_line(
        lines, lambda line: line.startswith("### Round-26 measured revision"))
    outcomes = (
        "\n".join(content_text(line) for line in lines[outcomes_start:revision_start])
        if outcomes_start is not None and revision_start is not None
        else None
    )
    c1_outcome_line = p4_numbered_line(
        lines, lambda line: "C1 improved observable, score" in line,
        outcomes_start or 0, revision_start)
    c2_outcome_line = p4_numbered_line(
        lines, lambda line: "C2 improved observable, score" in line,
        outcomes_start or 0, revision_start)
    c1_outcome_counts = p4_groups(
        outcomes,
        r"population\s*(\d+),\s*excluded\s*(\d+),\s*audited verdicts\s*(\d+),\s*"
        r"policy checks\s*(\d+),\s*(nine|\d+)\s+MP/MC interval-verdict families",
        re.IGNORECASE,
    )
    c1_outcome_family = p4_groups(
        outcomes,
        r"Pooled F1/F2\s*(\d+)/(\d+).*?MULTI\s*(\d+)/(\d+).*?composite\s*(\d+)/(\d+)",
        re.IGNORECASE | re.DOTALL,
    )
    c1_expected_counts = (
        (summary["population"], summary["excluded"], summary["audited_verdicts"],
         summary["policy_checks"], summary["families"])
        if summary else None
    )
    c1_claim_counts = (
        tuple(int(value) if value.isdecimal() else p4_word_number(value)
              for value in c1_outcome_counts)
        if c1_outcome_counts else None
    )
    c1_expected_family = (
        (summary["f1_k"], summary["f1_n"], summary["multi_k"], summary["multi_n"],
         summary["composite_k"], summary["composite_n"])
        if summary else None
    )
    c1_claim_family = (
        tuple(int(value) for value in c1_outcome_family)
        if c1_outcome_family else None
    )
    c1_outcome_score = p4_groups(
        c1_outcome_line[1] if c1_outcome_line else None, r"score\s*(\d+)\s+held")
    c1_score_value = int(c1_outcome_score[0]) if c1_outcome_score else None
    c1_score_value_expected = axis_scores.get("novelty") if axis_scores else None
    p4_record(
        root, out, P4A_ASSERTION_IDS[3],
        c1_outcome_line[0] if c1_outcome_line else None,
        summary_result.get("returncode") == 0
        and c1_claim_counts == c1_expected_counts
        and c1_claim_family == c1_expected_family
        and c1_score_value == c1_score_value_expected,
        {"claimed_counts": c1_claim_counts, "summary_counts": c1_expected_counts,
         "claimed_family": c1_claim_family, "summary_family": c1_expected_family,
         "claimed_score": c1_score_value, "axis_score": c1_score_value_expected},
        [f"population={summary['population']}", f"excluded={summary['excluded']}",
         f"audited_verdicts={summary['audited_verdicts']}",
         f"policy_checks={summary['policy_checks']}", f"families={summary['families']}",
         f"F1_k/n={summary['f1_k']}/{summary['f1_n']}",
         f"MULTI_k/n={summary['multi_k']}/{summary['multi_n']}",
         f"composite_k/n={summary['composite_k']}/{summary['composite_n']}",
         f"novelty_score={c1_score_value_expected}"]
        if summary and c1_score_value_expected is not None else None,
        "SCORECARD.md",
    )

    c2_outcome = p4_groups(
        outcomes,
        r"base.*?mismatch\s*(\d+).*?repaired tree mismatch\s*(\d+),\s*"
        r"superseded\s*=?\s*(\d+)\s*\((\d+)\s+assertions,\s*(\d+)\s+offline",
        re.IGNORECASE | re.DOTALL,
    )
    c2_expected = (
        (base_state["mismatch"], final_state["mismatch"], final_state["superseded"],
         final_state["assertions"], final_state["offline_unverifiable"])
        if base_state and final_state else None
    )
    c2_claim_values = tuple(int(value) for value in c2_outcome) if c2_outcome else None
    c2_outcome_score = p4_groups(
        c2_outcome_line[1] if c2_outcome_line else None, r"score\s*(\d+)\s+held")
    c2_score_value = int(c2_outcome_score[0]) if c2_outcome_score else None
    c2_score_value_expected = axis_scores.get("calibration") if axis_scores else None
    p4_record(
        root, out, P4A_ASSERTION_IDS[4],
        c2_outcome_line[0] if c2_outcome_line else None,
        c2_claim_values == c2_expected and c2_score_value == c2_score_value_expected,
        {"claimed": c2_claim_values, "base_receipt": base_state,
         "final_receipt": final_state, "claimed_score": c2_score_value,
         "axis_score": c2_score_value_expected},
        [f"base_mismatch={c2_expected[0]}", f"final_mismatch={c2_expected[1]}",
         f"superseded={c2_expected[2]}", f"assertions={c2_expected[3]}",
         f"offline_unverifiable={c2_expected[4]}",
         f"calibration_score={c2_score_value_expected}"]
        if c2_expected and c2_score_value_expected is not None else None,
        "SCORECARD.md",
    )

    revision_text = (
        "\n".join(content_text(line) for line in lines[revision_start:])
        if revision_start is not None else None
    )
    c1_revision_line = p4_numbered_line(
        lines, lambda line: "C1 audited" in line,
        revision_start or 0)
    c2_revision_line = p4_numbered_line(
        lines, lambda line: "C2 assertions" in line,
        revision_start or 0)
    c1_revision = p4_groups(
        revision_text,
        r"C1 audited\s*(\d+)\s*/\s*policy\s*(\d+)\s*/\s*families\s*(\d+)"
        r",?\s*exit\s*(\d+)",
    )
    c1_revision_expected = (
        (summary["audited_verdicts"], summary["policy_checks"], summary["families"],
         summary_result.get("returncode"))
        if summary else None
    )
    p4_record(
        root, out, P4A_ASSERTION_IDS[5],
        c1_revision_line[0] if c1_revision_line else None,
        c1_revision is not None
        and tuple(int(value) for value in c1_revision) == c1_revision_expected,
        {"claimed": c1_revision, "grader_summary": c1_revision_expected},
        [f"audited_verdicts={c1_revision_expected[0]}",
         f"policy_checks={c1_revision_expected[1]}",
         f"families={c1_revision_expected[2]}",
         f"exit={c1_revision_expected[3]}"] if c1_revision_expected else None,
        "SCORECARD.md",
    )

    c2_revision = p4_groups(
        revision_text,
        r"C2 assertions\s*(\d+)\s*/\s*match\s*(\d+)\s*/\s*mismatch\s*(\d+)\s*/\s*"
        r"superseded\s*(\d+)\s*/\s*offline-unverifiable\s*(\d+)\s*,?\s*exit\s*(\d+)",
    )
    final_exit = receipt_exit(final_receipt)
    c2_revision_expected = (
        tuple(final_state[key] for key in
              ("assertions", "match", "mismatch", "superseded", "offline_unverifiable"))
        + (int(final_exit),)
        if final_state and final_exit is not None else None
    )
    revision_scores = p4_groups(revision_text, r"Scores stay\s*(\d+)/(\d+)")
    revision_score_values = (
        tuple(int(value) for value in revision_scores) if revision_scores else None
    )
    revision_score_expected = (
        (axis_scores["novelty"], axis_scores["calibration"])
        if axis_scores else None
    )
    p4_record(
        root, out, P4A_ASSERTION_IDS[6],
        c2_revision_line[0] if c2_revision_line else None,
        c2_revision is not None
        and tuple(int(value) for value in c2_revision) == c2_revision_expected
        and revision_score_values == revision_score_expected,
        {"claimed": c2_revision, "final_receipt": final_state,
         "receipt_exit": final_exit, "score_claim": revision_score_values,
         "axis_scores": revision_score_expected},
        [f"assertions={c2_revision_expected[0]}", f"match={c2_revision_expected[1]}",
         f"mismatch={c2_revision_expected[2]}", f"superseded={c2_revision_expected[3]}",
         f"offline_unverifiable={c2_revision_expected[4]}",
         f"exit={c2_revision_expected[5]}",
         f"scores={revision_score_expected[0]}/{revision_score_expected[1]}"]
        if c2_revision_expected and revision_score_expected else None,
        "SCORECARD.md",
    )

    gate_values = p4_groups(
        gate_receipt,
        r"admissions=(\d+)\s+passed=(\d+)\s+failed=(\d+)\s+second-seat-reports=(\d+)",
    )
    gate_paths = p4_groups(
        gate_receipt, r"(?m)^  existing returned second-seat report\(s\): (.+)$")
    gate_exit = p4_groups(gate_receipt, r"(?m)^exit=(\d+)\s*$")
    gate_report_count = len(gate_paths[0].split(", ")) if gate_paths else None
    q13_claim = bool(
        revision_text
        and re.search(
            r"one admit,\s*three cited qualifying returned reports,\s*zero failed support checks",
            revision_text, re.IGNORECASE,
        )
    )
    gate_expected = ("1", "1", "0", "53")
    p4_record(
        root, out, P4A_ASSERTION_IDS[7],
        revision_start + 1 if revision_start is not None else None,
        gate_values == gate_expected and gate_report_count == 3
        and gate_exit == ("0",) and q13_claim,
        {"claim": q13_claim, "gate": gate_values,
         "returned_report_paths": gate_report_count, "exit": gate_exit},
        ["admissions=1", "passed=1", "cited_reports=3",
         "second_seat_reports=53", "failed=0", "exit=0"]
        if gate_values and gate_report_count is not None else None,
        "SCORECARD.md",
    )

    source_exit_matches = re.findall(r"(?m)^exit=(\d+)\s*$", source_receipt or "")
    source_exit = source_exit_matches[-1] if source_exit_matches else None
    source_revision = p4_groups(
        revision_text,
        r"Knowledge/index parity\s*(\d+)/(\d+).*?SOURCES\s*(\d+),\s*malformed\s*(\d+).*?"
        r"source-validator exit\s*(\d+)",
        re.IGNORECASE | re.DOTALL,
    )
    source_expected = (
        census.get("knowledge_files"), census.get("knowledge_readme_index_rows"),
        census.get("sources_rows"), census.get("sources_malformed"), source_exit,
    )
    source_claim = tuple(
        str(p4_word_number(value)) if not value.isdecimal() else value
        for value in source_revision
    ) if source_revision else None
    p4_record(
        root, out, P4A_ASSERTION_IDS[8],
        revision_start + 1 if revision_start is not None else None,
        source_claim == source_expected and census.get("knowledge_readme_parity") == "match"
        and source_exit == "0" and "kengaku\tok" in (source_receipt or ""),
        {"claim": source_claim, "census": source_expected,
         "parity": census.get("knowledge_readme_parity"), "source_receipt_exit": source_exit},
        [f"knowledge_files={source_expected[0]}", f"index_rows={source_expected[1]}",
         f"sources_rows={source_expected[2]}", f"sources_malformed={source_expected[3]}",
         f"source_validator_exit={source_expected[4]}"]
        if all(value is not None for value in source_expected) else None,
        "SCORECARD.md",
    )


def p4_readme_artifact_rows(root: Path) -> tuple[list[tuple[int, str, str]], int | None]:
    text = read_repo_text(root, "corpus/README.md")
    lines = physical_lines(text) if text is not None else []
    heading = find_line(
        lines, lambda line: line == "## Round-26 supporting artifacts (2026-10-21)")
    if heading is None:
        return [], None
    end = next_h2(lines, heading)
    rows = []
    for line_number, cells in table_rows(lines, heading + 1, end):
        if len(cells) < 2:
            continue
        spans = code_spans(cells[0])
        if len(spans) == 1:
            rows.append((line_number, spans[0], cells[1]))
    return rows, heading + 1


def p4_artifact_target(root: Path, row_path: str) -> Path:
    if row_path.startswith("../"):
        return root / row_path[3:]
    return root / "corpus" / row_path.rstrip("/")


def p4_artifact_files(root: Path) -> set[str]:
    files: set[str] = set()
    for relative in (
        "corpus/evidence/round26-sources",
        "corpus/evidence/round26-calibration",
        "plans/fixtures/r26",
    ):
        path = root / relative
        if path.is_file():
            files.add(path.relative_to(root).as_posix())
        elif path.is_dir():
            files.update(
                child.relative_to(root).as_posix()
                for child in path.rglob("*") if child.is_file()
            )
    for relative in (
        "plans/grader_perturb.py",
        "plans/gate_timing_check.py",
        "plans/round26_census.sh",
    ):
        path = root / relative
        if path.is_file():
            files.add(path.relative_to(root).as_posix())
    return files


def p4_source_ids(root: Path) -> list[int]:
    text = read_repo_text(root, "corpus/SOURCES.md")
    if text is None:
        return []
    ids = []
    for line in physical_lines(text):
        match = re.match(r"^\|\s*S(\d{3,})\s*\|", content_text(line))
        if match and 43 <= int(match.group(1)) <= 48:
            ids.append(int(match.group(1)))
    return ids


def check_p4b(root: Path, out: list[Assertion]) -> None:
    rows, anchor = p4_readme_artifact_rows(root)
    by_path: dict[str, list[tuple[int, str]]] = {}
    for line_number, path, covers in rows:
        by_path.setdefault(path, []).append((line_number, covers))
    for index, row_path in enumerate(P4B_ARTIFACT_PATHS):
        matches = by_path.get(row_path, [])
        line_number = matches[0][0] if matches else anchor
        target = p4_artifact_target(root, row_path)
        exists = target.exists()
        if row_path.endswith("/"):
            exists = target.is_dir()
        ok = len(matches) == 1 and exists
        p4_record(
            root, out, P4B_ASSERTION_IDS[index], line_number, ok,
            {"path": row_path, "row_count": len(matches), "exists": exists},
            [f"path={row_path}", "row_count=1", "exists=true"] if exists else None,
            "corpus/README.md",
        )

    expected_rows = set(P4B_ARTIFACT_PATHS)
    listed_paths = [path for _, path, _ in rows]
    actual_files = p4_artifact_files(root)
    normalized_rows = [
        (row_path[3:] if row_path.startswith("../") else f"corpus/{row_path}").rstrip("/")
        for row_path in listed_paths
    ]
    uncovered = sorted(
        path for path in actual_files
        if not any(path == row or path.startswith(row + "/") for row in normalized_rows)
    )
    extra_rows = sorted(set(listed_paths) - expected_rows)
    missing_rows = sorted(expected_rows - set(listed_paths))
    inventory_ok = (
        set(listed_paths) == expected_rows
        and len(listed_paths) == len(expected_rows)
        and not uncovered
    )
    p4_record(
        root, out, "P4b.readme.artifact-inventory", anchor, inventory_ok,
        {"listed": listed_paths, "missing_rows": missing_rows,
         "extra_rows": extra_rows, "on_disk_files": len(actual_files),
         "uncovered_files": uncovered},
        [f"rows={len(expected_rows)}", f"on_disk_files={len(actual_files)}",
         "uncovered_files=0"] if inventory_ok else None,
        "corpus/README.md",
    )

    source_row = next(
        ((line_number, covers) for line_number, path, covers in rows
         if path == "evidence/round26-sources/"),
        None,
    )
    claimed_range = p4_groups(
        source_row[1] if source_row else None, r"\bS(\d{3})\s*[–-]\s*S(\d{3})\b")
    source_ids = p4_source_ids(root)
    expanded = (
        list(range(int(claimed_range[0]), int(claimed_range[1]) + 1))
        if claimed_range else None
    )
    expected_ids = list(range(43, 49))
    source_range = (
        f"S{min(source_ids):03d}–S{max(source_ids):03d}" if source_ids else None
    )
    source_id_set = ",".join(f"S{source_id:03d}" for source_id in source_ids)
    derived_tokens = (
        [f"sources={source_range}", f"source_count={len(source_ids)}",
         f"source_ids={source_id_set}"]
        if source_range is not None else None
    )
    readme_text = read_repo_text(root, "corpus/README.md")
    readme_lines = physical_lines(readme_text) if readme_text is not None else []
    correction_hits = [
        index for index in range(max(0, len(readme_lines) - 2))
        if tuple(content_text(readme_lines[index + offset]) for offset in range(3))
        == P4B_SOURCE_CORRECTION_ANCHOR
    ]
    correction_line = correction_hits[0] + 1 if len(correction_hits) == 1 else None
    exact_base_correction = (
        len(correction_hits) == 1 and claimed_range == ("043", "047")
        and source_ids == expected_ids and source_range == "S043–S048"
        and derived_tokens == list(P4B_SOURCE_DERIVED_TOKENS)
    )
    source_line = source_row[0] if source_row else anchor
    observed = {
        "claimed_range": claimed_range, "expanded": expanded,
        "SOURCES_ids": source_ids, "derived_range": source_range,
        "derived_tokens": derived_tokens, "base_erratum_line": correction_line,
        "base_erratum_exact": exact_base_correction,
    }
    assertion_id = P4B_ASSERTION_IDS[-1]
    if expanded == source_ids and source_ids == expected_ids:
        add(out, assertion_id, source_line,
            "README Covers range re-derives from the frozen S043-S048 id set",
            observed, "MATCH")
    elif exact_base_correction:
        add(out, assertion_id, source_line,
            "the exact base README source-support correction restates the full six-id range",
            observed, "SUPERSEDED")
    else:
        p4_record(
            root, out, assertion_id, source_line, False, observed,
            derived_tokens, "corpus/README.md",
        )


def p4_json_file(root: Path, relative: str) -> dict[str, Any] | None:
    text = read_repo_text(root, relative)
    if text is None:
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def p4_role_counts(items: Any) -> tuple[dict[str, int], set[str]] | None:
    if not isinstance(items, list):
        return None
    counts_by_role: dict[str, int] = {}
    names: set[str] = set()
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            return None
        role = item.get("role")
        if not isinstance(role, str) or item["name"] in names:
            return None
        names.add(item["name"])
        counts_by_role[role] = counts_by_role.get(role, 0) + 1
    return counts_by_role, names


def p4_assignment_names(value: dict[str, Any] | None) -> set[str] | None:
    if value is None or any(not isinstance(name, str) for name in value):
        return None
    return set(value)


def p4_report_names(root: Path, relative: str) -> set[str]:
    directory = root / relative
    return {
        path.stem for path in directory.glob("*.md") if path.is_file()
    } if directory.is_dir() else set()


def p4_git_repo(root: Path) -> Path | None:
    candidates = [root, *root.parents, Path(__file__).resolve().parents[1],
                  Path.cwd(), *Path.cwd().parents]
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if not (candidate / ".git").exists():
            continue
        try:
            witness = subprocess.run(
                ["git", "cat-file", "-e", f"{P4_BASE_COMMIT}^{{commit}}"],
                cwd=candidate,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if witness.returncode == 0:
            return candidate
    return None


def p4_git_tree_counts(root: Path, revision: str) -> tuple[int, int] | None:
    repo = p4_git_repo(root)
    if repo is None:
        return None
    try:
        proc = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", revision, "--",
             ".ufo/waves/round-25/falsify/"],
            cwd=repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    names = proc.stdout.splitlines()
    return len(names), sum(name.endswith(".md") for name in names)


def p4_lesson_section(root: Path) -> tuple[str | None, list[str]]:
    text = read_repo_text(root, "corpus/lessons/round-26.md")
    lines = physical_lines(text) if text is not None else []
    return text, lines


def check_p4c(root: Path, out: list[Assertion]) -> None:
    lesson, lines = p4_lesson_section(root)
    build_spec = p4_json_file(root, ".ufo/waves/round-26/build-spec.json")
    build_assignments_json = p4_json_file(
        root, ".ufo/waves/round-26/build-assignments.json")
    falsify_spec = p4_json_file(root, ".ufo/waves/round-26/falsify-spec.json")
    falsify_assignments_json = p4_json_file(
        root, ".ufo/waves/round-26/falsify-assignments.json")
    dead_record = p4_json_file(root, ".ufo/waves/round-26/falsify-dead-seats.json")
    build_roles = p4_role_counts(build_spec.get("items") if build_spec else None)
    falsify_roles = p4_role_counts(falsify_spec.get("items") if falsify_spec else None)
    build_assignments = p4_assignment_names(build_assignments_json)
    falsify_assignments = p4_assignment_names(falsify_assignments_json)
    build_report_names = p4_report_names(root, ".ufo/waves/round-26/build")
    falsify_report_names = p4_report_names(root, ".ufo/waves/round-26/falsify")
    build_declared = build_roles[1] if build_roles else set()
    falsify_declared = falsify_roles[1] if falsify_roles else set()

    build_claim = p4_groups(
        lesson,
        r"(?m)^Build:\s*(\d+)\s+distinct seats.*?all\s+(\d+)\s+reports returned",
        re.DOTALL,
    )
    build_count = len(build_assignments) if build_assignments is not None else None
    build_spec_count = len(build_declared) if build_roles else None
    build_ok = (
        build_claim == ("72", "72") and build_count == 72 and build_spec_count == 72
        and build_assignments == build_declared
    )
    p4_record(
        root, out, P4C_ASSERTION_IDS[0],
        p4_numbered_line(lines, lambda line: line.startswith("Build:"))[0]
        if p4_numbered_line(lines, lambda line: line.startswith("Build:")) else None,
        build_ok,
        {"lesson": build_claim, "spec_items": build_spec_count,
         "assignment_names": build_count, "spec_assignment_match":
         build_assignments == build_declared},
        ["build_seats=72", "build_reports=72"] if build_spec_count is not None else None,
        "corpus/lessons/round-26.md",
    )

    expected_build_roles = {
        "scout": 22, "executor": 14, "reviewer": 12, "connector": 6,
        "critic": 6, "scribe": 6, "revenger": 4, "sentinel": 1, "simplifier": 1,
    }
    build_role_claim = p4_groups(
        lesson,
        r"(?m)^Build:.*?;\s*(\d+)\s+scout,\s*(\d+)\s+executor,\s*(\d+)\s+reviewer,\s*"
        r"(\d+)\s+connector,\s*(\d+)\s+critic,\s*(\d+)\s+scribe,\s*(\d+)\s+revenger,\s*"
        r"(\d+)\s+sentinel,\s*(\d+)\s+simplifier",
        re.DOTALL,
    )
    build_claim_roles = (
        dict(zip(("scout", "executor", "reviewer", "connector", "critic", "scribe",
                  "revenger", "sentinel", "simplifier"),
                 (int(value) for value in build_role_claim)))
        if build_role_claim else None
    )
    p4_record(
        root, out, P4C_ASSERTION_IDS[1],
        p4_numbered_line(lines, lambda line: line.startswith("Build:"))[0]
        if p4_numbered_line(lines, lambda line: line.startswith("Build:")) else None,
        build_roles is not None and build_roles[0] == expected_build_roles
        and build_claim_roles == expected_build_roles,
        {"lesson": build_claim_roles,
         "spec": build_roles[0] if build_roles else None,
         "expected": expected_build_roles},
        [f"{role}={count}" for role, count in expected_build_roles.items()],
        "corpus/lessons/round-26.md",
    )
    p4_record(
        root, out, P4C_ASSERTION_IDS[2],
        p4_numbered_line(lines, lambda line: "all " in line and " reports returned" in line)[0]
        if p4_numbered_line(lines, lambda line: "all " in line and
                            " reports returned" in line) else None,
        build_report_names == build_assignments and len(build_report_names) == 72,
        {"report_count": len(build_report_names), "assignment_count": build_count,
         "missing_reports": sorted(build_assignments - build_report_names)
         if build_assignments is not None else None,
         "unexpected_reports": sorted(build_report_names - build_assignments)
         if build_assignments is not None else None},
        ["reports=72", "missing=0", "unexpected=0"],
        "corpus/lessons/round-26.md",
    )

    falsify_claim = p4_groups(
        lesson, r"(?m)^(\d+)\s+distinct seats dispatched in one validated call")
    falsify_count = len(falsify_assignments) if falsify_assignments is not None else None
    falsify_spec_count = len(falsify_declared) if falsify_roles else None
    falsify_ok = (
        falsify_claim == ("64",) and falsify_count == 64 and falsify_spec_count == 64
        and falsify_assignments == falsify_declared
    )
    p4_record(
        root, out, P4C_ASSERTION_IDS[3],
        p4_numbered_line(lines, lambda line: "distinct seats dispatched in one validated call"
                          in line)[0]
        if p4_numbered_line(lines, lambda line: "distinct seats dispatched in one validated call"
                            in line) else None,
        falsify_ok,
        {"lesson": falsify_claim, "spec_items": falsify_spec_count,
         "assignment_names": falsify_count,
         "spec_assignment_match": falsify_assignments == falsify_declared},
        ["falsify_seats=64"] if falsify_spec_count is not None else None,
        "corpus/lessons/round-26.md",
    )

    expected_falsify_roles = {
        "reviewer": 39, "mutation-tester": 10, "scout": 7,
        "critic": 4, "executor": 2, "connector": 2,
    }
    falsify_role_claim = p4_groups(
        lesson,
        r"role mix\s*(\d+)\s+reviewer,\s*(\d+)\s+mutation-tester,\s*(\d+)\s+scout,\s*"
        r"(\d+)\s+critic,\s*(\d+)\s+executor,\s*(\d+)\s+connector",
        re.DOTALL,
    )
    falsify_claim_roles = (
        dict(zip(("reviewer", "mutation-tester", "scout", "critic", "executor", "connector"),
                 (int(value) for value in falsify_role_claim)))
        if falsify_role_claim else None
    )
    p4_record(
        root, out, P4C_ASSERTION_IDS[4],
        p4_numbered_line(lines, lambda line: "role mix" in line and
                         "mutation-tester" in line)[0]
        if p4_numbered_line(lines, lambda line: "role mix" in line and
                            "mutation-tester" in line) else None,
        falsify_roles is not None and falsify_roles[0] == expected_falsify_roles
        and falsify_claim_roles == expected_falsify_roles,
        {"lesson": falsify_claim_roles, "spec": falsify_roles[0] if falsify_roles else None,
         "expected": expected_falsify_roles},
        [f"{role}={count}" for role, count in expected_falsify_roles.items()],
        "corpus/lessons/round-26.md",
    )

    dead = dead_record.get("dead") if dead_record else None
    dead_names = {
        item.get("name") for item in dead
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    } if isinstance(dead, list) else set()
    dead_claim = p4_groups(lesson, r"\b(Eleven|\d+)\s+failed with the recorded")
    dead_claim_count = p4_word_number(dead_claim[0]) if dead_claim else None
    dead_ok = (
        isinstance(dead, list) and dead_claim_count == len(dead) == 11
        and dead_record.get("replaced") is False
        and falsify_assignments is not None and dead_names <= falsify_assignments
    )
    p4_record(
        root, out, P4C_ASSERTION_IDS[5],
        p4_numbered_line(lines, lambda line: "failed with the recorded" in line)[0]
        if p4_numbered_line(lines, lambda line: "failed with the recorded" in line) else None,
        dead_ok,
        {"lesson_dead": dead_claim_count, "dead_file_count": len(dead) if isinstance(dead, list) else None,
         "replaced": dead_record.get("replaced") if dead_record else None,
         "unassigned_dead_names": sorted(dead_names - falsify_assignments)
         if falsify_assignments is not None else None},
        ["dead=11", "replaced=false"] if isinstance(dead, list) else None,
        "corpus/lessons/round-26.md",
    )

    report_units_claim = p4_groups(
        lesson,
        r"(\d+)\s+report-bearing returns plus the failure record account for all\s*(\d+)",
    )
    expected_returned = (
        len(falsify_assignments - dead_names) if falsify_assignments is not None else None
    )
    p4_record(
        root, out, P4C_ASSERTION_IDS[6],
        p4_numbered_line(lines, lambda line: "report-bearing returns plus the failure record"
                          in line)[0]
        if p4_numbered_line(lines, lambda line: "report-bearing returns plus the failure record"
                            in line) else None,
        report_units_claim == (str(expected_returned), "64")
        and falsify_report_names == (falsify_assignments - dead_names),
        {"lesson": report_units_claim, "returned_reports": len(falsify_report_names),
         "assignment_minus_dead": expected_returned,
         "missing_reports": sorted((falsify_assignments - dead_names) - falsify_report_names)
         if falsify_assignments is not None else None},
        [f"reports={expected_returned}", "dead=11", "assignments=64"]
        if expected_returned is not None else None,
        "corpus/lessons/round-26.md",
    )

    totals_claim = p4_groups(
        lesson,
        r"two inherited waves total \*\*(\d+) unique dispatched seats\*\*; "
        r"three\s+recovery\s+reviewers\s+bring\s+the round-wide total to \*\*(\d+)\*\*",
        re.IGNORECASE | re.DOTALL,
    )
    total_136 = (
        len(build_assignments) + len(falsify_assignments)
        if build_assignments is not None and falsify_assignments is not None else None
    )
    total_139 = total_136 + 3 if total_136 is not None else None
    p4_record(
        root, out, P4C_ASSERTION_IDS[7],
        p4_numbered_line(lines, lambda line: "two inherited waves total" in line)[0]
        if p4_numbered_line(lines, lambda line: "two inherited waves total" in line) else None,
        totals_claim is not None and int(totals_claim[0]) == total_136 == 136,
        {"lesson": totals_claim, "build": len(build_assignments)
         if build_assignments is not None else None,
         "falsify": len(falsify_assignments) if falsify_assignments is not None else None,
         "derived_total": total_136},
        [f"unique_dispatched={total_136}"] if total_136 is not None else None,
        "corpus/lessons/round-26.md",
    )
    p4_record(
        root, out, P4C_ASSERTION_IDS[8],
        p4_numbered_line(lines, lambda line: "three recovery reviewers bring the round-wide total"
                          in line)[0]
        if p4_numbered_line(lines, lambda line: "three recovery reviewers bring the round-wide total"
                            in line) else None,
        totals_claim is not None and int(totals_claim[1]) == total_139 == 139,
        {"lesson": totals_claim, "recovery_reviewers": 3, "derived_total": total_139},
        [f"recovery_reviewers=3", f"round_total={total_139}"]
        if total_139 is not None else None,
        "corpus/lessons/round-26.md",
    )

    raw_claim = p4_groups(
        lesson, r"raw tree entries\s+\*\*(\d+)/(\d+)/(\d+)\*\*")
    md_claim = p4_groups(
        lesson, r"Markdown seat reports\s+\*\*(\d+)/(\d+)/(\d+)\*\*")
    tree_counts = [p4_git_tree_counts(root, revision)
                   for revision in ("8ea41f9", "8239a56", "9d8a00d")]
    raw_observed = tuple(value[0] for value in tree_counts) if all(
        value is not None for value in tree_counts) else None
    md_observed = tuple(value[1] for value in tree_counts) if all(
        value is not None for value in tree_counts) else None
    raw_values = tuple(int(value) for value in raw_claim) if raw_claim else None
    md_values = tuple(int(value) for value in md_claim) if md_claim else None
    raw_line = p4_numbered_line(lines, lambda line: "raw tree entries" in line)
    md_line = p4_numbered_line(lines, lambda line: "Markdown seat reports" in line)
    revisions = ["8ea41f9", "8239a56", "9d8a00d"]
    if raw_observed is None:
        add(out, P4C_ASSERTION_IDS[9], raw_line[0] if raw_line else None,
            "read-only Git tree counts at the three cited revisions",
            {"status": "UNVERIFIABLE", "lesson": raw_values, "revisions": revisions},
            "OFFLINE_UNVERIFIABLE")
    else:
        p4_record(
            root, out, P4C_ASSERTION_IDS[9], raw_line[0] if raw_line else None,
            raw_values == raw_observed == (0, 83, 88),
            {"lesson": raw_values, "git_ls_tree": raw_observed, "revisions": revisions},
            [f"raw_entries={','.join(str(value) for value in raw_observed)}"],
            "corpus/lessons/round-26.md",
        )
    if md_observed is None:
        add(out, P4C_ASSERTION_IDS[10], md_line[0] if md_line else None,
            "read-only Git tree Markdown counts at the three cited revisions",
            {"status": "UNVERIFIABLE", "lesson": md_values, "revisions": revisions},
            "OFFLINE_UNVERIFIABLE")
    else:
        p4_record(
            root, out, P4C_ASSERTION_IDS[10], md_line[0] if md_line else None,
            md_values == md_observed == (0, 82, 87),
            {"lesson": md_values, "git_ls_tree_markdown": md_observed,
             "revisions": revisions},
            [f"markdown_reports={','.join(str(value) for value in md_observed)}"],
            "corpus/lessons/round-26.md",
        )


def p4_manifest_rows(root: Path) -> tuple[list[str], list[dict[str, str]]] | None:
    text = read_repo_text(root, "plans/fixtures/r26/perturb_population.tsv")
    if text is None:
        return None
    lines = text.splitlines()
    if not lines:
        return None
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        values = line.split("\t")
        if len(values) != len(header):
            return None
        rows.append(dict(zip(header, values)))
    return header, rows


def p4_population_manifest(
    manifest: tuple[list[str], list[dict[str, str]]] | None,
) -> dict[str, Any] | None:
    if manifest is None:
        return None
    header, rows = manifest
    required = {"file", "cell", "grader", "stored_ok", "baseline_ok", "disposition"}
    if not required <= set(header):
        return None
    file_counts: dict[str, int] = {}
    grader_counts: dict[str, int] = {}
    pass_count = fail_count = c_mono_count = included = excluded = 0
    for row in rows:
        file_name = row["file"]
        file_counts[file_name] = file_counts.get(file_name, 0) + 1
        grader = row["grader"]
        grader_counts[grader] = grader_counts.get(grader, 0) + 1
        if row["disposition"] == "include":
            included += 1
        else:
            excluded += 1
        if row["stored_ok"] == "true":
            pass_count += 1
        elif row["stored_ok"] == "false":
            fail_count += 1
        else:
            return None
        if row["cell"] == "C-MONO":
            c_mono_count += 1
    return {
        "records": len(rows),
        "included": included,
        "excluded": excluded,
        "files": file_counts,
        "graders": grader_counts,
        "pass": pass_count,
        "fail": fail_count,
        "c_mono": c_mono_count,
        "baseline_replays": sum(
            row["baseline_ok"] == row["stored_ok"] for row in rows
        ),
    }


def p4_oracle_values(text: str | None) -> tuple[dict[str, Any] | None, dict[str, dict[str, Any]]]:
    population = p4_groups(
        text, r"(?m)^POPULATION candidates=(\d+) included=(\d+) excluded=(\d+)\s*$")
    pop = (
        {"candidates": int(population[0]), "included": int(population[1]),
         "excluded": int(population[2])}
        if population else None
    )
    families: dict[str, dict[str, Any]] = {}
    for match in re.finditer(
        r"(?m)^(F[1-7]|D1|G1|G2) kind=(MP|MC|PC) n=(\d+) k=(\d+)\s*$",
        text or "",
    ):
        family, kind, n, k = match.groups()
        if family in families:
            return pop, {}
        families[family] = {"kind": kind, "n": int(n), "k": int(k)}
    return pop, families


def p4_audit_family_rows(
    root: Path,
) -> dict[str, tuple[int, list[str]]] | None:
    text = read_repo_text(root, "corpus/knowledge/grader-perturbation-audit.md")
    lines = physical_lines(text) if text is not None else []
    heading = find_line(
        lines, lambda line: line == "## Observed finite-population results")
    if heading is None:
        return None
    table_header = find_line(
        lines, lambda line: line == "| family | kind | k/n | nominal exact CP95 lower | interpretation |",
        heading + 1,
    )
    if table_header is None:
        return None
    result: dict[str, tuple[int, list[str]]] = {}
    for line_number, cells in table_rows(lines, table_header + 1,
                                         next_h2(lines, table_header)):
        if len(cells) >= 3 and cells[0] in P4D_FAMILY_ORDER:
            if cells[0] in result:
                return None
            result[cells[0]] = (line_number, cells)
    return result


def check_p4d(root: Path, out: list[Assertion], evidence: P4Evidence) -> None:
    audit = read_repo_text(root, "corpus/knowledge/grader-perturbation-audit.md")
    manifest = p4_population_manifest(p4_manifest_rows(root))
    json_result = evidence.command("grader_json")
    oracle_result = evidence.command("oracle")
    try:
        grader = json.loads(json_result.get("stdout", ""))
    except (json.JSONDecodeError, TypeError):
        grader = None
    if not isinstance(grader, dict):
        grader = None
    oracle_population, oracle_families = p4_oracle_values(oracle_result.get("stdout"))
    families = grader.get("families") if grader else None
    if not isinstance(families, dict):
        families = {}
    pins = grader.get("pins") if grader else None
    pins = pins if isinstance(pins, dict) else {}
    file_claims: dict[str, int] = {}
    file_claim_lines: list[int] = []
    audit_lines = physical_lines(audit) if audit is not None else []
    audit_text = audit or ""
    for relative, _ in P4D_FILE_COUNTS:
        short = relative.removeprefix("corpus/evidence/")
        matches = list(re.finditer(
            rf"`{re.escape(short)}`\s*\((\d+)(?:\s+graded responses)?\)",
            audit_text,
        ))
        if len(matches) == 1:
            match = matches[0]
            file_claim_lines.append(audit_text[:match.start()].count("\n") + 1)
            file_claims[relative] = int(match.group(1))
    manifest_files = manifest["files"] if manifest else {}
    expected_file_counts = dict(P4D_FILE_COUNTS)
    json_pin_paths = set(pins)
    files_ok = (
        file_claims == expected_file_counts
        and manifest_files == expected_file_counts
        and json_pin_paths == set(expected_file_counts)
        and json_result.get("returncode") == 0
    )
    p4_record(
        root, out, P4D_ASSERTION_IDS[1],
        min(file_claim_lines) if file_claim_lines else None,
        files_ok,
        {"audit": file_claims, "manifest": manifest_files,
         "json_pin_paths": sorted(json_pin_paths), "expected": expected_file_counts,
         "grader_exit": json_result.get("returncode")},
        [f"{Path(path).name}={expected_file_counts[path]}"
         for path, _ in P4D_FILE_COUNTS] if manifest else None,
        "corpus/knowledge/grader-perturbation-audit.md",
    )

    records_claim = p4_groups(
        audit,
        r"All\s+\*\*(\d+)\*\*\s+raw\+ok candidate records replay their stored verdict;\s*"
        r"\*\*(\d+) excluded\*\*,\s*\*\*(\d+) PASS / (\d+) FAIL\*\*",
    )
    json_records = (
        (grader.get("population"), grader.get("population_expected"),
         grader.get("candidate_count"), grader.get("excluded"))
        if grader else None
    )
    record_claim_values = tuple(int(value) for value in records_claim) if records_claim else None
    record_expected = (
        (manifest["records"], manifest["records"], manifest["records"], manifest["excluded"])
        if manifest else None
    )
    records_ok = (
        manifest is not None and grader is not None
        and json_result.get("returncode") == 0 and oracle_result.get("returncode") == 0
        and json_records == (1964, 1964, 1964, 0)
        and oracle_population == {"candidates": 1964, "included": 1964, "excluded": 0}
        and record_claim_values is not None
        and record_claim_values[0] == manifest["records"] == 1964
        and record_claim_values[1] == manifest["excluded"] == 0
        and record_claim_values[2:] == (manifest["pass"], manifest["fail"])
        and manifest["baseline_replays"] == manifest["records"]
        and manifest["included"] == manifest["records"]
    )
    p4_record(
        root, out, P4D_ASSERTION_IDS[0],
        p4_numbered_line(audit_lines, lambda line: line.startswith("All **"))[0]
        if p4_numbered_line(audit_lines, lambda line: line.startswith("All **")) else None,
        records_ok,
        {"audit": record_claim_values, "manifest": record_expected,
         "grader_json": json_records, "oracle": oracle_population},
        [f"population={manifest['records']}", f"excluded={manifest['excluded']}",
         f"PASS={manifest['pass']}", f"FAIL={manifest['fail']}"]
        if manifest else None,
        "corpus/knowledge/grader-perturbation-audit.md",
    )
    pass_claim = (record_claim_values[2], record_claim_values[3]) if record_claim_values else None
    pass_expected = (manifest["pass"], manifest["fail"]) if manifest else None
    p4_record(
        root, out, P4D_ASSERTION_IDS[2],
        p4_numbered_line(audit_lines, lambda line: line.startswith("All **"))[0]
        if p4_numbered_line(audit_lines, lambda line: line.startswith("All **")) else None,
        pass_claim == pass_expected == (1021, 943)
        and manifest is not None and manifest["records"] == 1964,
        {"audit_PASS_FAIL": pass_claim, "manifest_PASS_FAIL": pass_expected},
        [f"PASS={pass_expected[0]}", f"FAIL={pass_expected[1]}"]
        if pass_expected else None,
        "corpus/knowledge/grader-perturbation-audit.md",
    )


    grader_claim = p4_groups(
        audit,
        r"State grading covers\s+(\d+)\s+records,\s*sequence grading\s+(\d+),\s*"
        r"`grade_c`\s+(\d+),\s*and\s*`valid_latin`\s*(\d+)\s+C-MONO records",
    )
    grader_claim_values = tuple(int(value) for value in grader_claim) if grader_claim else None
    grader_counts = manifest["graders"] if manifest else {}
    derived_grader_counts = (
        (grader_counts.get("state"), grader_counts.get("seq"),
         grader_counts.get("c", 0) - manifest["c_mono"], manifest["c_mono"])
        if manifest else None
    )
    p4_record(
        root, out, P4D_ASSERTION_IDS[3],
        p4_numbered_line(audit_lines, lambda line: "State grading covers" in line)[0]
        if p4_numbered_line(audit_lines, lambda line: "State grading covers" in line) else None,
        grader_claim_values == derived_grader_counts
        and derived_grader_counts == (1708, 240, 12, 4)
        and manifest is not None and manifest["records"] == 1964,
        {"audit": grader_claim_values, "manifest_derived": derived_grader_counts,
         "manifest_graders": grader_counts},
        [f"state={derived_grader_counts[0]}", f"seq={derived_grader_counts[1]}",
         f"grade_c={derived_grader_counts[2]}",
         f"valid_latin={derived_grader_counts[3]}"]
        if derived_grader_counts else None,
        "corpus/knowledge/grader-perturbation-audit.md",
    )

    family_rows = p4_audit_family_rows(root) or {}
    for index, family in enumerate(P4D_FAMILY_ORDER, 4):
        row = family_rows.get(family)
        cells = row[1] if row else []
        claim = p4_groups(" | ".join(cells[1:3]), r"^\s*(MP|MC|PC)\s*\|\s*(\d+)/(\d+)\s*$")
        claim_values = (
            {"kind": claim[0], "k": int(claim[1]), "n": int(claim[2])}
            if claim else None
        )
        json_family = families.get(family)
        if not isinstance(json_family, dict):
            json_family = None
        command_values = (
            {"kind": json_family.get("kind"), "n": json_family.get("n"),
             "k": json_family.get("k")}
            if json_family else None
        )
        oracle_values = oracle_families.get(family)
        family_ok = (
            row is not None and claim_values is not None
            and command_values is not None and oracle_values is not None
            and json_result.get("returncode") == 0
            and oracle_result.get("returncode") == 0
            and claim_values["kind"] == command_values["kind"] == oracle_values["kind"]
            and claim_values["n"] == command_values["n"] == oracle_values["n"]
            and claim_values["k"] == command_values["k"] == oracle_values["k"]
        )
        p4_record(
            root, out, P4D_ASSERTION_IDS[index], row[0] if row else None,
            family_ok,
            {"claim": claim_values, "grader_json": command_values,
             "oracle": oracle_values},
            [f"family={family}", f"kind={command_values['kind']}",
             f"k/n={command_values['k']}/{command_values['n']}"]
            if family_ok else None,
            "corpus/knowledge/grader-perturbation-audit.md",
        )


def p4_cited_source_numbers(line: str) -> set[int]:
    numbers: set[int] = set()
    for match in P4_CITATION_RE.finditer(line):
        first = int(match.group(1))
        second = int(match.group(2)) if match.group(2) else None
        if first == 43 and re.search(r"\bsupersedes\s+S043\b", line, re.IGNORECASE):
            continue
        if second is None:
            numbers.add(first)
        else:
            numbers.update(range(min(first, second), max(first, second) + 1))
    return numbers


def p4_citing_files(root: Path, source_number: int) -> list[str] | None:
    # Candidate paths are frozen at b5719440; later lesson/knowledge files are
    # outside P4e even if they mention one of the six source ids.
    hits = []
    for relative in P4E_CITATION_FILES:
        path = root / relative
        if not path.is_file():
            return None
        try:
            text = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeError):
            return None
        if any(source_number in p4_cited_source_numbers(line)
               for line in text.splitlines()):
            hits.append(relative)
    return sorted(hits)


def check_p4e(root: Path, out: list[Assertion]) -> None:
    text = read_repo_text(root, "corpus/SOURCES.md")
    lines = physical_lines(text) if text is not None else []
    source_rows: dict[str, list[tuple[int, list[str]]]] = {}
    for line_number, cells in table_rows(lines, 0, len(lines)):
        match = re.match(r"^S(\d{3})$", cells[0].strip()) if cells else None
        source_id = f"S{match.group(1)}" if match else None
        if source_id in P4E_SOURCE_IDS:
            source_rows.setdefault(source_id, []).append((line_number, cells))
    for index, source_id in enumerate(P4E_SOURCE_IDS):
        matches = source_rows.get(source_id, [])
        row = matches[0] if len(matches) == 1 else None
        used_by = row[1][-1] if row and row[1] else ""
        claimed = [value.strip().strip("`") for value in used_by.split(",")
                   if value.strip() and value.strip() != "—"]
        expected = p4_citing_files(root, int(source_id[1:]))
        p4_record(
            root, out, P4E_ASSERTION_IDS[index], row[0] if row else None,
            row is not None and expected is not None
            and len(claimed) == len(set(claimed)) and set(claimed) == set(expected),
            {"source_id": source_id, "row_count": len(matches), "used_by": claimed,
             "citing_files": expected},
            [f"used-by={source_id}:" + "|".join(expected)]
            if row is not None and expected is not None else None,
            "corpus/SOURCES.md",
        )


def check_p4(root: Path, out: list[Assertion], evidence: P4Evidence) -> None:
    start = len(out)
    check_p4a(root, out, evidence)
    check_p4b(root, out)
    check_p4c(root, out)
    check_p4d(root, out, evidence)
    check_p4e(root, out)
    actual_ids = tuple(item.id for item in out[start:])
    add(
        out, P4_ASSERTION_INVENTORY_ID, None,
        "exact frozen P4a-P4e assertion-id population",
        {"expected": P4_ASSERTION_IDS, "actual": actual_ids},
        "MATCH" if sorted(actual_ids) == sorted(P4_ASSERTION_IDS) else "MISMATCH",
    )

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
    check_p3(root, assertions)
    check_p4(root, assertions, P4Evidence(root))
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



def write_p3_fixture(root: Path) -> None:
    (root / "corpus").mkdir(parents=True, exist_ok=True)
    (root / "corpus/evidence/round25-calibration").mkdir(parents=True, exist_ok=True)
    (root / "corpus/evidence/round25-sources").mkdir(parents=True, exist_ok=True)
    (root / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    (root / "corpus/lessons").mkdir(parents=True, exist_ok=True)

    scorecard_lines = [
        "## Capabilities",
        "",
        "| Capability | What | Evidence | Round |",
        "|---|---|---|---|",
        "| interval-reverdict | r | unique_samples=4; scored_trials=92 correct=92; "
        "transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4; "
        "mismatches=0; exit 0; --selftest 18 checks 0 failed (red runs R1–R6 included) | 25 |",
        "| state-assertion-check | r | base `6180e4f` mismatch=10 exit 1; "
        "landed tree mismatch=0 superseded=1 exit 0; --selftest ALL PASS | 25 |",
        "",
        "Re-derived axis state, round 24",
        "",
        "| Axis | Round-24 value | Basis |",
        "|---|---|---|",
        "| novelty | 7 | numeric anchor r14 (`:162`) |",
    ]
    while len(scorecard_lines) < 161:
        scorecard_lines.append("fixture filler")
    scorecard_lines.append("| **novelty** *(owned)* | 6 → **7** |")
    scorecard_lines.extend([
        "",
        "Re-derived axis state, round 25:",
        "",
        "| Axis | Round-25 value | Basis |",
        "|---|---|---|",
        "| novelty | 7 | C1 above |",
    ])
    while len(scorecard_lines) < P3_CORRECTION_FLOORS["SCORECARD.md"]:
        scorecard_lines.append("fixture filler")
    (root / "SCORECARD.md").write_text("\n".join(scorecard_lines) + "\n", encoding="utf-8")

    source_rows = ["| id | source |", "|---|---|"]
    source_rows.extend(f"| S{i:03d} | source |" for i in range(1, 44))
    (root / "corpus/SOURCES.md").write_text(
        "\n".join(source_rows) + "\n", encoding="utf-8")
    province_lines = [
        "## Province map",
        "",
        "| Surface | Check | Result |",
        "|---|---|---|",
        "| Public-literature registry | `test -e corpus/SOURCES.md` | present; 42 rows |",
        "*Round-25 correction: Public-literature registry held 42 at base and holds 42 after round 25.*",
        "| Interval re-verdict instrument (round 25) | `python3 plans/attrib_calibration.py` | "
        "exit 0 / exit 0; 4 unique samples, 92/92 correct, "
        "transitions FAIL>UNTESTED 2, PASS>INDETERMINATE 1 |",
        "| State-assertion check (round 25) | `python3 plans/state_check.py` | "
        "exit 0 / exit 0 on landed tree (base `6180e4f`: exit 1, 10 mismatches) |",
    ]
    while len(province_lines) < 128:
        province_lines.append("")
    province_lines.append("### Adjacent")
    while len(province_lines) < P3_CORRECTION_FLOORS["PROVINCE.md"]:
        province_lines.append("")
    (root / "PROVINCE.md").write_text("\n".join(province_lines) + "\n", encoding="utf-8")

    (root / "corpus/evidence/round25-calibration/attrib-calibration-summary-v2.txt").write_text(
        "TOTAL unique_samples=4 scored_trials=92 correct=92 "
        "transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 mismatches=0\n"
        "exit=0\n", encoding="utf-8")
    (root / "corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt").write_text(
        "selftest ok R1: fixture\nselftest ok R1b: fixture\n"
        "selftest ok R2: fixture\nselftest ok R3: fixture\n"
        "selftest ok R4: fixture\nselftest ok R5: fixture\n"
        "selftest ok R6: fixture\nselftest: 18 checks, 0 failed\nexit=0\n",
        encoding="utf-8")
    (root / "corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt").write_text(
        "assertions=241 match=228 mismatch=10 superseded=0\nexit=1\n", encoding="utf-8")
    (root / "corpus/evidence/round25-calibration/state-check-after-v2.txt").write_text(
        "assertions=235 match=231 mismatch=0 superseded=1\nexit=0\n", encoding="utf-8")
    (root / "corpus/evidence/round25-calibration/state-check-selftest-v2.txt").write_text(
        "selftest: ALL PASS\nexit=0\n", encoding="utf-8")

    (root / "SKILL.md").write_text(
        "---\nname: kengaku-shokunin\ndescription: test\n---\n\n"
        "# kengaku-shokunin\n## Decision table — benchmark selection\n"
        "## Benchmark anti-patterns\n## Production checklist — running an eval\n"
        "## Cited local sources\n", encoding="utf-8")
    log_lines = ["fixture"] * 6 + ["2026-09-28 — round 4: executed first authored eval"]
    (root / "LOG.md").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    cold_lines = ["fixture"] * 47 + ["## Box-3 verdict"]
    (root / "corpus/lessons/round-8-aggregator-box3-coldrun.md").write_text(
        "\n".join(cold_lines) + "\n", encoding="utf-8")
    shonen_text = (
        "# SHONEN\n"
        "- [~] skill\n  SKILL.md\n"
        "- [~] log\n  LOG.md:7\n"
        "- [~] cold run\n  corpus/lessons/round-8-aggregator-box3-coldrun.md:48\n"
        "- [~] province\n  PROVINCE.md:129\n"
    )
    (root / "SHONEN.md").write_text(shonen_text, encoding="utf-8")

    (root / "corpus/README.md").write_text(
        "# Corpus\n\n## What's here\n\n| Path | Contents |\n|---|---|\n"
        "| `knowledge/attribution-interval-calibration.md` | fixture |\n"
        "### `lessons/`\n\n| Path | Contents |\n|---|---|\n"
        "| `lessons/round-24-verifier-spotcheck.md` | fixture |\n"
        "| `lessons/round-25.md` | fixture |\n"
        "| `lessons/round-25-verifier-spotcheck.md` | fixture |\n"
        "Supporting corpus files:\n\n### `evidence/`\n\n| Path | Contents |\n|---|---|\n"
        "| `evidence/round25-sources/` | fixture |\n"
        "| `evidence/round25-calibration/` | fixture |\n"
        "### `plans/`\n",
        encoding="utf-8")
    for relative in dict.fromkeys((*P3E_ROW_PATHS, *P3E_FILE_PATHS)):
        path = root / "corpus" / relative.rstrip("/")
        if relative.endswith("/"):
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture\n", encoding="utf-8")


def p4_selftest_copy_tree(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for relative in (
        "corpus/knowledge",
        "corpus/lessons",
        "corpus/evidence/round26-calibration",
        "corpus/evidence/round26-sources",
        ".ufo/waves/round-26",
        "plans/fixtures/r26",
    ):
        source_path = source / relative
        destination_path = destination / relative
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    for relative in (
        "SCORECARD.md",
        "SHONEN.md",
        "SKILL.md",
        "LOG.md",
        "PROVINCE.md",
        "corpus/README.md",
        "corpus/SOURCES.md",
        "plans/grader_perturb.py",
        "plans/gate_timing_check.py",
        "plans/round26_census.sh",
    ):
        source_path = source / relative
        destination_path = destination / relative
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)
    for relative in P4_CORRECTION_DOCS:
        path = destination / relative
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines(keepends=True)
            path.write_text(
                "".join(line for line in lines
                        if not P4_CORRECTION_ID_RE.match(content_text(line))),
                encoding="utf-8",
            )


def p4_selftest_evidence() -> Any:
    population_files = dict(P4D_FILE_COUNTS)
    family_values = {
        "F1": ("MP", 1819, 1802), "F2": ("MP", 1819, 1802),
        "F3": ("MP", 1964, 1964), "F4": ("MP", 1720, 1720),
        "F5": ("MP", 1964, 1964), "F6": ("MP", 1964, 1964),
        "F7": ("MP", 1876, 1876), "D1": ("PC", 909, 909),
        "G1": ("MC", 1021, 1021), "G2": ("MC", 1021, 1021),
    }
    families = {
        family: {"kind": kind, "n": n, "k": k,
                 "pid_composite": {"n": 194, "k": 187} if family == "F1" else {},
                 "by_class": {"MULTI": {"n": 31, "k": 14}} if family == "F1" else {}}
        for family, (kind, n, k) in family_values.items()
    }
    pins = {path: "selftest-pin" for path in population_files}
    result = {
        "population": 1964, "population_expected": 1964, "candidate_count": 1964,
        "excluded": 0, "audited_verdicts": 15168, "policy_checks": 909,
        "families_with_interval_verdict": 9, "pins": pins, "families": families,
        "errors": [],
    }
    summary = (
        "FAMILY F1 kind=MP n=1819 k=1802 rate=0.990654 "
        "composite=194/187@0.963918\n"
        "CLASSES F1 FJ1=1296/1296 MULTI=31/14 DANGLE=0/0 BARE=0/0\n"
        "TOTAL population=1964 excluded=0 audited_verdicts=15168 "
        "policy_checks=909 families_with_interval_verdict=9\n"
    )
    oracle = ["POPULATION candidates=1964 included=1964 excluded=0"]
    oracle.extend(
        f"{family} kind={kind} n={n} k={k}"
        for family, (kind, n, k) in family_values.items()
    )
    outputs = {
        "grader_summary": {"returncode": 0, "stdout": summary, "stderr": ""},
        "grader_json": {"returncode": 0, "stdout": json.dumps(result), "stderr": ""},
        "oracle": {"returncode": 0, "stdout": "\n".join(oracle), "stderr": ""},
    }

    class FakeEvidence:
        def command(self, name: str) -> dict[str, Any]:
            return outputs.get(name, {"returncode": None, "stdout": "", "stderr": "unknown"})

    return FakeEvidence()


def p4_selftest_verdict(assertions: list[Assertion], assertion_id: str) -> str | None:
    matches = [item.verdict for item in assertions if item.id == assertion_id]
    return matches[0] if len(matches) == 1 else None


def run_p4_selftest() -> bool:
    source_root = Path(__file__).resolve().parents[1]
    evidence = p4_selftest_evidence()

    with tempfile.TemporaryDirectory(prefix="state-check-p4-") as tempdir:
        def prepare(name: str) -> Path:
            root = Path(tempdir) / name
            p4_selftest_copy_tree(source_root, root)
            return root

        def red_case(label: str, root: Path, assertion_id: str, check, mutate) -> bool:
            clean: list[Assertion] = []
            check(root, clean)
            if p4_selftest_verdict(clean, assertion_id) != "MATCH":
                print(f"selftest FAIL {label}: pristine control did not MATCH ({assertion_id})")
                return False
            mutate()
            changed: list[Assertion] = []
            check(root, changed)
            if p4_selftest_verdict(changed, assertion_id) != "MISMATCH":
                print(f"selftest FAIL {label}: red mutation survived ({assertion_id})")
                return False
            print(f"selftest ok {label}: mutation red ({assertion_id})")
            return True

        all_passed = True

        root = prepare("P4a")
        card = root / "SCORECARD.md"
        original = card.read_text(encoding="utf-8")
        mutated = original.replace(
            "0 → 15168 audited verdicts", "0 → 15167 audited verdicts", 1)
        all_passed &= red_case(
            "P4a", root, P4A_ASSERTION_IDS[0],
            lambda target, records: check_p4a(target, records, evidence),
            lambda: card.write_text(mutated, encoding="utf-8"),
        )

        root = prepare("P4b")
        readme = root / "corpus/README.md"
        readme_text = readme.read_text(encoding="utf-8")
        readme_mutation = "".join(
            line for line in readme_text.splitlines(keepends=True)
            if "`evidence/round26-calibration/`" not in line
        )
        all_passed &= red_case(
            "P4b", root, "P4b.readme.artifact-row.evidence/round26-calibration/",
            lambda target, records: check_p4b(target, records),
            lambda: readme.write_text(readme_mutation, encoding="utf-8"),
        )

        root = prepare("P4c")
        dead_path = root / ".ufo/waves/round-26/falsify-dead-seats.json"
        dead_record = json.loads(dead_path.read_text(encoding="utf-8"))
        dead_record["dead"] = dead_record["dead"][:-1]
        all_passed &= red_case(
            "P4c", root, P4C_ASSERTION_IDS[5],
            lambda target, records: check_p4c(target, records),
            lambda: dead_path.write_text(json.dumps(dead_record, indent=2), encoding="utf-8"),
        )

        root = prepare("P4d")
        audit_path = root / "corpus/knowledge/grader-perturbation-audit.md"
        audit_text = audit_path.read_text(encoding="utf-8")
        audit_mutation = audit_text.replace(
            "| F1 | MP | 1802/1819 |", "| F1 | MP | 1801/1819 |", 1)
        all_passed &= red_case(
            "P4d", root, "P4d.family.F1",
            lambda target, records: check_p4d(target, records, evidence),
            lambda: audit_path.write_text(audit_mutation, encoding="utf-8"),
        )

        root = prepare("P4e")
        sources = root / "corpus/SOURCES.md"
        source_lines = sources.read_text(encoding="utf-8").splitlines(keepends=True)
        source_mutation = "".join(
            line.replace(
                "corpus/lessons/round-26.md, corpus/knowledge/grader-perturbation-audit.md",
                "corpus/lessons/round-26.md",
                1,
            ) if line.startswith("| S044 |") else line
            for line in source_lines
        )
        all_passed &= red_case(
            "P4e", root, "P4e.sources.S044.used-by",
            lambda target, records: check_p4e(target, records),
            lambda: sources.write_text(source_mutation, encoding="utf-8"),
        )
        root = prepare("P4-correction-scope")
        readme_path = root / "corpus/README.md"
        coverage_id = "P4b.readme.covers.round26-sources"
        base_readme = readme_path.read_text(encoding="utf-8")
        anchor_text = "\n".join(P4B_SOURCE_CORRECTION_ANCHOR)
        no_anchor = base_readme.replace(anchor_text, "", 1)
        baseline: list[Assertion] = []
        check_p4b(root, baseline)
        if (no_anchor == base_readme
                or p4_selftest_verdict(baseline, coverage_id) != "SUPERSEDED"):
            print("selftest FAIL P4 supersession: exact base anchor was not superseded")
            all_passed = False
        remove_result: list[Assertion] = []
        readme_path.write_text(no_anchor, encoding="utf-8")
        check_p4b(root, remove_result)
        if p4_selftest_verdict(remove_result, coverage_id) != "MISMATCH":
            print("selftest FAIL P4 supersession: removing base erratum survived")
            all_passed = False
        wrong_range = base_readme.replace(
            P4B_SOURCE_CORRECTION_ANCHOR[1],
            P4B_SOURCE_CORRECTION_ANCHOR[1].replace("S043–S048", "S043–S049"),
            1,
        )
        wrong_result: list[Assertion] = []
        readme_path.write_text(wrong_range, encoding="utf-8")
        check_p4b(root, wrong_result)
        if p4_selftest_verdict(wrong_result, coverage_id) != "MISMATCH":
            print("selftest FAIL P4 supersession: wrong source-range erratum survived")
            all_passed = False
        partial = base_readme.replace(P4B_SOURCE_CORRECTION_ANCHOR[2] + "\n", "", 1)
        partial_result: list[Assertion] = []
        readme_path.write_text(partial, encoding="utf-8")
        check_p4b(root, partial_result)
        if p4_selftest_verdict(partial_result, coverage_id) != "MISMATCH":
            print("selftest FAIL P4 supersession: partial base anchor survived")
            all_passed = False
        r27_tokens = " ".join(f"`{token}`" for token in P4B_SOURCE_DERIVED_TOKENS)
        padding = "\n" * max(
            1, P4_CORRECTION_FLOORS["corpus/README.md"] - len(no_anchor.splitlines()) + 1)
        r27_line = (
            "- **R27-E1 (2026-10-21)** supersedes "
            "`P4b.readme.covers.round26-sources` — now " + r27_tokens + "\n"
        )
        r27_tree = no_anchor + padding + r27_line
        r27_result: list[Assertion] = []
        readme_path.write_text(r27_tree, encoding="utf-8")
        check_p4b(root, r27_result)
        if p4_selftest_verdict(r27_result, coverage_id) != "SUPERSEDED":
            print("selftest FAIL P4 supersession: complete R27-E did not supersede")
            all_passed = False
        else:
            print("selftest ok P4 supersession: exact base anchor and R27-E full tokens")
        r29_result: list[Assertion] = []
        readme_path.write_text(r27_tree.replace("R27-E1", "R29-E1", 1), encoding="utf-8")
        check_p4b(root, r29_result)
        if p4_selftest_verdict(r29_result, coverage_id) != "MISMATCH":
            print("selftest FAIL P4 supersession: out-of-round R29-E closed P4")
            all_passed = False

        root = prepare("out-of-population-preservation")
        new_knowledge = root / "corpus/knowledge/r27-out-of-pop-selftest.md"
        new_knowledge.write_text("fixture\n", encoding="utf-8")
        p2_oop: list[Assertion] = []
        check_readme_index(root, p2_oop)
        p2_oop_id = "P2e.out-of-population.file.knowledge/r27-out-of-pop-selftest.md"
        if p4_selftest_verdict(p2_oop, p2_oop_id) != "OUT_OF_POPULATION":
            print("selftest FAIL OUT_OF_POPULATION: P2e disclosure was removed")
            all_passed = False
        else:
            print("selftest ok OUT_OF_POPULATION: P2e new-file disclosure retained")
        shonen_path = root / "SHONEN.md"
        shonen = shonen_path.read_text(encoding="utf-8")
        shonen_mutation = shonen + "- [~] round27 extra\n  outside-r27.md\n"
        shonen_path.write_text(shonen_mutation, encoding="utf-8")
        p3_oop: list[Assertion] = []
        check_p3c(root, p3_oop)
        if not any(item.id.startswith("P3c.out-of-population.pointer.outside-r27.md@")
                   and item.verdict == "OUT_OF_POPULATION" for item in p3_oop):
            print("selftest FAIL OUT_OF_POPULATION: P3c pointer disclosure was removed")
            all_passed = False
        else:
            print("selftest ok OUT_OF_POPULATION: P3c pointer disclosure retained")
    return all_passed

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
        for erratum, want in (
            ("", "MISMATCH"),
            ("- **R25-E1 (t)** supersedes `P2a.capability.sources-registry` — "
             "now `rows 26` `A=24 C=2`\n", "MISMATCH"),
            ("- **R25-E1 (t)** supersedes `P2a.capability.sources-registry` — "
             "now `rows 26` `malformed 0` `A=24 C=2` `mined=18 queued=6 rejected=2`\n",
             "SUPERSEDED"),
            ("- **R25-E1 (t)** supersedes `P2a.capability.sources-registry` — "
             "now `rows 27` `A=24 C=2`\n", "MISMATCH"),
            ("- **R27-E1 (t)** supersedes `P2a.capability.sources-registry` — "
             "now `rows 26` `malformed 0` `A=24 C=2` `mined=18 queued=6 rejected=2`\n",
             "SUPERSEDED"),
            ("- **R29-E1 (t)** supersedes `P2a.capability.sources-registry` — "
             "now `rows 26` `malformed 0` `A=24 C=2` `mined=18 queued=6 rejected=2`\n",
             "SUPERSEDED"),
        ):
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
        p3root = root / "p3-fixture"
        write_p3_fixture(p3root)
        baseline: list[Assertion] = []
        check_p3(p3root, baseline)
        for class_name, expected_ids in P3_SELFTEST_ASSERTION_IDS.items():
            actual_ids = sorted(
                item.id for item in baseline if item.id.startswith(class_name + "."))
            if actual_ids != sorted(expected_ids):
                missing = sorted(set(expected_ids) - set(actual_ids))
                extra = sorted(set(actual_ids) - set(expected_ids))
                print(f"selftest: frozen {class_name} assertion IDs differ; "
                      f"missing={missing}, extra={extra}", file=sys.stderr)
                return 1
        if any(item.verdict == "MISMATCH" for item in baseline):
            failures = [item.id for item in baseline if item.verdict == "MISMATCH"]
            print(f"selftest: P3 fixture baseline failed: {failures}", file=sys.stderr)
            return 1

        def p3_verdict(items: list[Assertion], assertion_id: str) -> str | None:
            return next((item.verdict for item in items if item.id == assertion_id), None)

        scorecard_path = p3root / "SCORECARD.md"
        scorecard_fixture = scorecard_path.read_text(encoding="utf-8")
        p3a_mutated = scorecard_fixture.replace(
            "--selftest 18 checks 0 failed", "--selftest 14 checks 0 failed", 1)
        if p3a_mutated == scorecard_fixture:
            print("selftest: P3a cell mutation anchor missing", file=sys.stderr)
            return 1
        scorecard_path.write_text(p3a_mutated, encoding="utf-8")
        got = []
        check_p3a(p3root, got)
        p3a_id = "P3a.capability.interval-reverdict.selftest-checks"
        def p3a_verdict_for(text: str, assertion_id: str) -> str | None:
            scorecard_path.write_text(text, encoding="utf-8")
            checks: list[Assertion] = []
            check_p3a(p3root, checks)
            return p3_verdict(checks, assertion_id)
        if p3_verdict(got, p3a_id) != "MISMATCH":
            print("selftest: P3a selftest-count mutation survived", file=sys.stderr)
            return 1
        partial = (p3a_mutated + "\n- **R26-E1 (2026-10-21)** supersedes "
                   f"`{p3a_id}` — now `18 checks`\n")
        scorecard_path.write_text(partial, encoding="utf-8")
        got = []
        check_p3a(p3root, got)
        if p3_verdict(got, p3a_id) != "MISMATCH":
            print("selftest: partial R26-E token set superseded P3a", file=sys.stderr)
            return 1
        full = (p3a_mutated + "\n- **R26-E1 (2026-10-21)** supersedes "
                f"`{p3a_id}` — now `18 checks` `0 failed`\n")
        scorecard_path.write_text(full, encoding="utf-8")
        got = []
        check_p3a(p3root, got)
        if p3_verdict(got, p3a_id) != "SUPERSEDED":
            print("selftest: complete R26-E token set did not supersede P3a", file=sys.stderr)
            return 1
        scorecard_path.write_text(scorecard_fixture, encoding="utf-8")
        p3a_state_mutated = scorecard_fixture.replace(
            "base `6180e4f` mismatch=10",
            "base `6180e4f` mismatch=11", 1)
        if p3a_state_mutated == scorecard_fixture:
            print("selftest: P3a base mismatch mutation anchor missing", file=sys.stderr)
            return 1
        scorecard_path.write_text(p3a_state_mutated, encoding="utf-8")
        got = []
        check_p3a(p3root, got)
        p3a_state_id = "P3a.capability.state-assertion-check.base-mismatch"
        p3a_state_item = next((item for item in got if item.id == p3a_state_id), None)
        if (p3a_state_item is None or p3a_state_item.verdict != "MISMATCH"
                or p3a_state_item.observed.get("observed", {}).get("claim") != ("11",)
                or p3a_state_item.observed.get("observed", {}).get("receipt") != ("10",)):
            print("selftest: P3a base mismatch mutation did not compare 11 against 10",
                  file=sys.stderr)
            return 1
        scorecard_path.write_text(scorecard_fixture, encoding="utf-8")
        p3a_unique_id = "P3a.capability.interval-reverdict.unique-samples"
        duplicate_unique = scorecard_fixture.replace(
            "unique_samples=4", "unique_samples=4 duplicate unique_samples=999", 1)
        if p3a_verdict_for(duplicate_unique, p3a_unique_id) != "MISMATCH":
            print("selftest: contradictory duplicate unique_samples survived", file=sys.stderr)
            return 1
        range_id = "P3a.capability.interval-reverdict.selftest-red-runs"
        short_range = scorecard_fixture.replace(
            "red runs R1–R6 included", "red runs R1–R5 included", 1)
        if p3a_verdict_for(short_range, range_id) != "MISMATCH":
            print("selftest: P3a selftest red-run range mutation survived", file=sys.stderr)
            return 1
        interval_audit_id = "P3a.capability.interval-reverdict.numeric-token-audit"
        unknown_interval_number = scorecard_fixture.replace(
            "mismatches=0; exit 0", "mismatches=0 unregistered_metric=999; exit 0", 1)
        if p3a_verdict_for(unknown_interval_number, interval_audit_id) != "MISMATCH":
            print("selftest: P3a unregistered interval number survived", file=sys.stderr)
            return 1
        state_audit_id = "P3a.capability.state-assertion-check.numeric-token-audit"
        unknown_state_number = scorecard_fixture.replace(
            "landed tree mismatch=0", "landed tree mismatch=0 auxiliary=777", 1)
        if p3a_verdict_for(unknown_state_number, state_audit_id) != "MISMATCH":
            print("selftest: P3a unregistered state number survived", file=sys.stderr)
            return 1

        def correction(correction_id: str, target: str, tokens: str) -> str:
            return (f"- **{correction_id} (2026-10-21)** supersedes "
                    f"`{target}` — now {tokens}")

        full_tokens = "`18 checks` `0 failed`"
        early_lines = p3a_mutated.splitlines()
        early_lines.insert(1, correction("R26-E5", p3a_id, full_tokens))
        if p3a_verdict_for("\n".join(early_lines) + "\n", p3a_id) != "MISMATCH":
            print("selftest: pre-freeze R26-E line superseded P3a", file=sys.stderr)
            return 1
        contradictory = (p3a_mutated + "\n"
                         + correction("R26-E6", p3a_id,
                                      "17 checks; unrelated `18 checks` `0 failed`") + "\n")
        if p3a_verdict_for(contradictory, p3a_id) != "MISMATCH":
            print("selftest: contradictory R26-E prose superseded P3a", file=sys.stderr)
            return 1
        duplicate_id = (p3a_mutated + "\n"
                        + correction("R26-E7", p3a_id, full_tokens) + "\n"
                        + correction("R26-E7", p3a_id, full_tokens) + "\n")
        if p3a_verdict_for(duplicate_id, p3a_id) != "MISMATCH":
            print("selftest: duplicate R26-E ID superseded P3a", file=sys.stderr)
            return 1
        distinct_ids = (p3a_mutated + "\n"
                        + correction("R26-E1", p3a_id, full_tokens) + "\n"
                        + correction("R26-E5", p3a_id, full_tokens) + ".\n")
        if p3a_verdict_for(distinct_ids, p3a_id) != "SUPERSEDED":
            print("selftest: latest distinct full R26-E did not supersede P3a",
                  file=sys.stderr)
            return 1
        for correction_id in ("R27-E8", "R29-E8"):
            future_correction = (
                p3a_mutated + "\n" + correction(correction_id, p3a_id, full_tokens) + "\n")
            if p3a_verdict_for(future_correction, p3a_id) != "SUPERSEDED":
                print(f"selftest: {correction_id} did not supersede P3a", file=sys.stderr)
                return 1
        print("selftest ok   P2/P3 supersession range: R27 and R29 accepted")
        latest_invalid = (p3a_mutated + "\n"
                          + correction("R26-E1", p3a_id, full_tokens) + "\n"
                          + correction("R26-E5", p3a_id,
                                       "`17 checks` `0 failed`") + "\n")
        if p3a_verdict_for(latest_invalid, p3a_id) != "MISMATCH":
            print("selftest: invalid latest R26-E fell back to older correction",
                  file=sys.stderr)
            return 1
        scorecard_path.write_text(scorecard_fixture, encoding="utf-8")
        print("selftest ok   P3a: duplicate metric, R1–R6, base mismatch and correction-parser reds")
        province_path = p3root / "PROVINCE.md"
        province_fixture = province_path.read_text(encoding="utf-8")
        province_path.write_text(
            province_fixture.replace("4 unique samples", "3 unique samples", 1),
            encoding="utf-8")
        got = []
        check_p3b(p3root, got)
        p3b_unique_id = "P3b.province.interval-reverdict.unique-samples"
        p3b_unique_item = next(
            (item for item in got if item.id == p3b_unique_id), None)
        if (p3b_unique_item is None or p3b_unique_item.verdict != "MISMATCH"
                or p3b_unique_item.observed.get("observed", {}).get("claim") != ("3",)
                or p3b_unique_item.observed.get("observed", {}).get("receipt") != ("4",)):
            print("selftest: P3b unique-samples mutation did not compare 3 against 4",
                  file=sys.stderr)
            return 1
        province_path.write_text(province_fixture, encoding="utf-8")
        province_path.write_text(
            province_fixture.replace("92/92 correct", "91/92 correct", 1),
            encoding="utf-8")
        got = []
        check_p3b(p3root, got)
        p3b_id = "P3b.province.interval-reverdict.scored-trials"
        if p3_verdict(got, p3b_id) != "MISMATCH":
            print("selftest: P3b instrument-count mutation survived", file=sys.stderr)
            return 1
        province_path.write_text(province_fixture, encoding="utf-8")
        sources_path = p3root / "corpus/SOURCES.md"
        sources_fixture = sources_path.read_text(encoding="utf-8")
        sources_path.write_text(
            sources_fixture.replace("| S042 | source |", "| S041 | duplicate |", 1),
            encoding="utf-8")
        got = []
        check_p3b(p3root, got)
        census_ids = (
            "P3b.province.public-literature-registry.rows",
            "P3b.province.round25-correction.rows",
        )
        if any(p3_verdict(got, assertion_id) != "MISMATCH"
               for assertion_id in census_ids):
            print("selftest: P3b same-count id-set mutation survived", file=sys.stderr)
            return 1
        sources_path.write_text(sources_fixture, encoding="utf-8")
        print("selftest ok   P3b: unique-samples, scored-trials and frozen-id-set reds")
        p3b_public_id = "P3b.province.public-literature-registry.rows"
        p3b_round25_id = "P3b.province.round25-correction.rows"
        stale_province = province_fixture.replace(
            "present; 42 rows", "present; 25 rows", 1).replace(
                "holds 42 after round 25", "holds 37 after round 25", 1)
        full_province_corrections = (
            stale_province + "\n"
            + correction("R26-E9", p3b_public_id, "`rows=42` `id_set=exact`") + "\n"
            + correction("R26-E10", p3b_round25_id, "`rows=42` `id_set=exact`") + "\n")
        province_path.write_text(full_province_corrections, encoding="utf-8")
        got = []
        check_p3b(p3root, got)
        if (p3_verdict(got, p3b_public_id) != "SUPERSEDED"
                or p3_verdict(got, p3b_round25_id) != "SUPERSEDED"):
            print("selftest: full P3b rows/id-set correction did not supersede both stale claims",
                  file=sys.stderr)
            return 1

        partial_province_corrections = full_province_corrections.replace(
            "`rows=42` `id_set=exact`", "`rows=42`", 1)
        province_path.write_text(partial_province_corrections, encoding="utf-8")
        got = []
        check_p3b(p3root, got)
        if (p3_verdict(got, p3b_public_id) != "MISMATCH"
                or p3_verdict(got, p3b_round25_id) != "SUPERSEDED"):
            print("selftest: partial P3b source correction did not fail independently",
                  file=sys.stderr)
            return 1

        source_id_mutation = sources_fixture.replace(
            "| S042 | source |", "| S041 | duplicate |", 1)
        sources_path.write_text(source_id_mutation, encoding="utf-8")
        province_path.write_text(full_province_corrections, encoding="utf-8")
        got = []
        check_p3b(p3root, got)
        if (p3_verdict(got, p3b_public_id) != "MISMATCH"
                or p3_verdict(got, p3b_round25_id) != "MISMATCH"):
            print("selftest: full old P3b corrections overrode a changed id set",
                  file=sys.stderr)
            return 1
        sources_path.write_text(sources_fixture, encoding="utf-8")

        scorecard_fallback = (
            scorecard_fixture + "\n"
            + correction("R26-E11", p3b_public_id, "`rows=42` `id_set=exact`") + "\n"
            + correction("R26-E12", p3b_round25_id, "`rows=42` `id_set=exact`") + "\n")
        scorecard_path.write_text(scorecard_fallback, encoding="utf-8")
        province_path.write_text(stale_province, encoding="utf-8")
        got = []
        check_p3b(p3root, got)
        if (p3_verdict(got, p3b_public_id) != "SUPERSEDED"
                or p3_verdict(got, p3b_round25_id) != "SUPERSEDED"):
            print("selftest: SCORECARD fallback did not close absent-primary P3b rows",
                  file=sys.stderr)
            return 1

        invalid_primary = (stale_province + "\n"
                           + correction("R26-E13", p3b_public_id, "`rows=42`") + "\n")
        scorecard_with_fallback = (
            scorecard_fixture + "\n"
            + correction("R26-E14", p3b_public_id, "`rows=42` `id_set=exact`") + "\n"
            + correction("R26-E15", p3b_round25_id, "`rows=42` `id_set=exact`") + "\n")
        province_path.write_text(invalid_primary, encoding="utf-8")
        scorecard_path.write_text(scorecard_with_fallback, encoding="utf-8")
        got = []
        check_p3b(p3root, got)
        if (p3_verdict(got, p3b_public_id) != "MISMATCH"
                or p3_verdict(got, p3b_round25_id) != "SUPERSEDED"):
            print("selftest: invalid primary P3b correction routed around via SCORECARD",
                  file=sys.stderr)
            return 1
        province_path.write_text(province_fixture, encoding="utf-8")
        scorecard_path.write_text(scorecard_fixture, encoding="utf-8")
        print("selftest ok   P3b: strict source-first/fallback corrections and exact id set")

        skill_path = p3root / "SKILL.md"
        skill_fixture = skill_path.read_text(encoding="utf-8")
        for _, _, _, token, needle_number in P3C_PINS[:4]:
            pin_id = f"P3c.box.1.pointer.1.needle.{needle_number}"
            mutations = (
                ("missing", skill_fixture.replace(token, "", 1)),
                ("duplicate", skill_fixture.replace(token, token + "\n" + token, 1)),
            )
            for mutation_name, mutated_skill in mutations:
                if mutated_skill == skill_fixture:
                    print(f"selftest: P3c Box-1 {mutation_name} anchor missing: {token}",
                          file=sys.stderr)
                    return 1
                skill_path.write_text(mutated_skill, encoding="utf-8")
                got = []
                check_p3c(p3root, got)
                if p3_verdict(got, pin_id) != "MISMATCH":
                    print(f"selftest: P3c Box-1 {mutation_name} survived ({pin_id})",
                          file=sys.stderr)
                    return 1
            skill_path.write_text(skill_fixture, encoding="utf-8")
        print("selftest ok   P3c: all Box-1 headings red on missing and duplicate")
        cold_path = p3root / "corpus/lessons/round-8-aggregator-box3-coldrun.md"
        cold_fixture = cold_path.read_text(encoding="utf-8")
        cold_path.write_text(cold_fixture.replace(
            "## Box-3 verdict", "## Wrong verdict", 1), encoding="utf-8")
        got = []
        check_p3c(p3root, got)
        p3c_id = "P3c.box.3.pointer.1"
        if p3_verdict(got, p3c_id) != "MISMATCH":
            print("selftest: P3c target-content mutation survived", file=sys.stderr)
            return 1
        cold_path.write_text(cold_fixture, encoding="utf-8")
        print(f"selftest ok   P3c: red mutation ({p3c_id})")

        scorecard_path.write_text(scorecard_fixture.replace(
            "| **novelty** *(owned)* | 6 → **7** |",
            "| **depth** *(owned)* | 6 → **7** |", 1), encoding="utf-8")
        got = []
        check_p3d(p3root, got)
        p3d_id = "P3d.axis.novelty.anchor.1.pin"
        if p3_verdict(got, p3d_id) != "MISMATCH":
            print("selftest: P3d anchor-content mutation survived", file=sys.stderr)
            return 1
        scorecard_path.write_text(scorecard_fixture, encoding="utf-8")
        print(f"selftest ok   P3d: red mutation ({p3d_id})")

        readme_path = p3root / "corpus/README.md"
        readme_fixture = readme_path.read_text(encoding="utf-8")
        spotcheck_row = "| `lessons/round-25-verifier-spotcheck.md` | fixture |\n"
        without_spotcheck = readme_fixture.replace(spotcheck_row, "", 1)
        if without_spotcheck == readme_fixture:
            print("selftest: P3e outside-spotcheck row fixture missing", file=sys.stderr)
            return 1
        readme_path.write_text(without_spotcheck, encoding="utf-8")
        got = []
        check_p3e(p3root, got)
        spotcheck_id = "P3e.file-to-row.lessons/round-25-verifier-spotcheck.md"
        if p3_verdict(got, spotcheck_id) != "MISMATCH":
            print("selftest: P3e missing outside-spotcheck row survived", file=sys.stderr)
            return 1
        readme_path.write_text(readme_fixture, encoding="utf-8")
        readme_path.write_text(readme_fixture.replace(
            "| `lessons/round-25.md` | fixture |\n", "", 1), encoding="utf-8")
        got = []
        check_p3e(p3root, got)
        row_id = "P3e.row-to-file.lessons/round-25.md"
        file_id = "P3e.file-to-row.lessons/round-25.md"
        if p3_verdict(got, row_id) != "MISMATCH" or p3_verdict(got, file_id) != "MISMATCH":
            print("selftest: P3e missing-index-row mutation survived", file=sys.stderr)
            return 1
        readme_path.write_text(readme_fixture, encoding="utf-8")
        (p3root / "corpus/lessons/round-25.md").unlink()
        got = []
        check_p3e(p3root, got)
        if (p3_verdict(got, row_id) != "MISMATCH"
                or p3_verdict(got, file_id) != "MISMATCH"):
            print("selftest: P3e missing-file mutation did not fail both directions",
                  file=sys.stderr)
            return 1
        print(f"selftest ok   P3e: outside-spotcheck row, row/file mutations ({row_id}; {file_id})")
    if not run_p4_selftest():
        return 1
    print("[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, "
          "R25–R29-E exact-token supersession, P2/P3 R27/R29 corrections, "
          "P4 R27-only supersession, P2e/P3c OUT_OF_POPULATION retention, "
          "P3a–P3e and P4a–P4e red mutations)")
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
