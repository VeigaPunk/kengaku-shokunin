#!/usr/bin/env python3
"""Build the Q1/Q21 mutant fixtures from the BASE entry bytes.

Input:  entry-base.md   (git show 4087b2f8:corpus/knowledge/tb2-code-from-image-offline.md,
                         sha256 fc42c76cb5a05c131a5fec4d2aa3e441d9627841d130a54d1b616f2042675271)
Output: fixtures/<id>.md and fixtures/fixtures.json

Every fixture is BASE with a scripted edit to the three header lines only; the
body is byte-identical.  The repaired fixture is the green baseline: BASE's
recheck line gains an ISO date and the commit pin, keeping the command it
already had.  Each mutant removes exactly one property of the repaired fixture
or replaces the recheck value with the battery's specified text.

m8 is not produced here: it is an instrument mutant (rules_m8_always_true.py),
not an entry mutant.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE / "entry-base.md"
FIXTURES = HERE / "fixtures"

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
OTHER_PIN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
SHA64 = "b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a"
COMMAND = "python3 plans/round83_c1_replay.py --lane . --work DIR"
REPAIRED = f"recheck: 2027-05-01 — {COMMAND}; pin {PIN}"

# id -> (recheck line, extra header edit, expected failing rules, purpose)
SPEC: dict[str, tuple[str, dict[int, str], list[str], str]] = {
    "repaired": (
        REPAIRED,
        {},
        [],
        "green baseline: ISO date + command + the commit pin named",
    ),
    "m1": (
        f"recheck: {COMMAND}; pin {PIN}",
        {},
        ["q1"],
        "date removed from recheck (pin and command kept)",
    ),
    "m2": (
        f"recheck: 2027-05-01 — {COMMAND}",
        {},
        ["q21"],
        "pin removed from recheck (date and command kept)",
    ),
    "m3": (
        "recheck: monthly re-verify",
        {},
        ["q1", "q21"],
        "recheck replaced by `monthly re-verify`: cadence, no object, no pin",
    ),
    "m4": (
        REPAIRED,
        {2: "\0BLANK"},
        ["q1"],
        "recheck moved to line 4 (blank line inserted at line 3)",
    ),
    "m5": (
        f"recheck: 2027-05-01 — {COMMAND}; pin {PIN[:-1]}7",
        {},
        ["q21"],
        "recheck pin differs from the source pin by one hex digit",
    ),
    "m6": (
        "recheck: 2027-05-01",
        {},
        ["q1", "q21"],
        "date with no action and no pin",
    ),
    "m7": (
        f"recheck: 2027-05-01 — {COMMAND}; pin {PIN[:7]}",
        {},
        ["q21"],
        "recheck names only the 7-char pin prefix",
    ),
    "P1": (
        f"recheck: quarterly — {COMMAND}; re-pin to the then-current upstream commit",
        {},
        [],
        "Q21 re-pin-cadence branch, no pin named: must pass",
    ),
    "N1": (
        f"recheck: 2027-05-01 — re-pin when needed; {COMMAND}",
        {},
        ["q21"],
        "`re-pin when needed`: re-pin token, no cadence term (date and command kept)",
    ),
    "N2": (
        REPAIRED,
        {0: f"source: S267 — corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py; sha256 {SHA64}"},
        ["q21"],
        "source carries a 64-hex sha256 and no 40-hex commit pin",
    ),
    "N3": (
        REPAIRED,
        {0: f"source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}0/code-from-image/tests/test_outputs.py :10-31"},
        ["q21"],
        "source pin embedded in a 41-hex run (no standalone 40-hex)",
    ),
    "N4": (
        f"recheck: 2027-02-31 — {COMMAND}; pin {PIN}",
        {},
        ["q1"],
        "calendar-invalid ISO shape (Feb 31) with command and pin",
    ),
    "N5": (
        f"recheck: 2027-05-01 — {COMMAND}; pin {OTHER_PIN}",
        {0: f"source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/code-from-image/tests/test_outputs.py :10-31; superseded pin {OTHER_PIN}"},
        ["q21"],
        "source carries two 40-hex pins; recheck names the second",
    ),
}


def build(base_lines: list[str], recheck: str, header_edits: dict[int, str]) -> str:
    if len(base_lines) < 4:
        raise SystemExit("entry-base.md is too short to hold three header lines")
    lines = list(base_lines)
    for index, text in header_edits.items():
        lines[index] = "" if text == "\0BLANK" else text
    # The inserted blank for m4 goes in at index 2, pushing recheck to line 4.
    if header_edits.get(2) == "\0BLANK":
        lines = lines[:2] + ["", recheck] + lines[3:]
    else:
        lines[2] = recheck
    text = "\n".join(lines)
    if not text.endswith("\n"):
        text += "\n"
    return text


def main() -> int:
    raw = BASE.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != "fc42c76cb5a05c131a5fec4d2aa3e441d9627841d130a54d1b616f2042675271":
        print(f"mkfixtures: entry-base.md is not the BASE bytes ({digest})", file=sys.stderr)
        return 2
    base_lines = raw.decode("utf-8").splitlines()

    FIXTURES.mkdir(exist_ok=True)
    manifest = {
        "source_entry": "entry-base.md",
        "source_entry_sha256": digest,
        "source_revision": "4087b2f8369fb0c317a8460725a607681ff2fd7f",
        "fixtures": {},
    }
    for fixture_id, (recheck, edits, expected, purpose) in SPEC.items():
        text = build(base_lines, recheck, edits)
        path = FIXTURES / f"{fixture_id}.md"
        path.write_text(text, encoding="utf-8")
        fixture_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        manifest["fixtures"][fixture_id] = {
            "path": f"fixtures/{fixture_id}.md",
            "sha256": fixture_sha,
            "bytes": len(text.encode("utf-8")),
            "expected_failing_rules": expected,
            "purpose": purpose,
            "header": text.splitlines()[:4],
        }
        print(f"{fixture_id:9s} {fixture_sha}  expect={expected or ['none']}")
    (FIXTURES / "fixtures.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"FIXTURES={len(SPEC)} manifest=fixtures/fixtures.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
