#!/usr/bin/env python3
"""Correction-command reproduction gate (round 60, C2).

The routed class (round-59 non-author closure, routed defect 3): a dated
correction's own counting command does not reproduce -- the r59 claims doc's
cosmetic-correction section prints `grep -c 'broke four tip counters' LOG.md` -> 1
while the committed bytes give 0 (the phrase is line-wrapped at LOG.md:1961-1962).
A dated correction asserts current truth (QUALITY R12: a stale assertion is closed
by an appended correction that itself re-derives); its counting command is a
falsifiable assertion that must KEEP re-deriving at the tip, not only on the day
it was written.

Frozen population: every `plans/round-<N>-claims.md` (glob `plans/round-*-claims.md`,
sorted). Within a file, only the body of a section whose heading matches
`^#{2,3} .*dated correction` (case-insensitive) is scanned -- corrections assert
current truth; freeze-time before-anchor commands elsewhere in a claims doc are
historical statements about the freeze revision and are OUT of scope by design.

Frozen command class: a backticked `` `grep -c<flags> 'PATTERN' PATH` `` on one line,
followed on the same line by the Unicode-arrow expectation `→ <digits>`. The gate
re-runs the command with cwd=lane (shlex-split argv, no shell) and prices the
claimed count: stdout digits must equal the claimed integer.

  CMDPOP files=<f> sections=<s> commands=<n> ok=<k> out_of_scope=<o> defects=<d> errata=<e>
  OK <file>:<line> got=<n> want=<n>
  SKIP <file>:<line> <reason>
  CMD-DEFECT <file>:<line> got=<n> want=<n>   (or reason=exec-error rc=<rc>)
  PREDICATE R60-C2 pass|fail

Erratum discipline (the R1 house form, mirroring plans/receipt_consistency_check.py):
a `===`-delimited block in the SAME file containing both the string `ERRATUM (round`
and the token `correction_command_check` converts that file's defects to `errata=<n>`
-- declared, dated, still printed. A foreign === block without the token converts
nothing (selftest case). Exit 0 iff undeclared defects == 0; 1 on any undeclared
defect; 2 on setup (empty population -- never a vacuous pass).

Named limits (frozen): only grep -c-family commands with an explicit -> expectation
are re-run (python3/probe re-derive commands are out of scope); commands naming
paths outside the lane (absolute paths, `..`, `<fleet>`-style placeholders) are
skipped as out_of_scope, not defects -- the gate reads the lane read-only; only
same-line command+expectation pairs are priced (a command whose expectation lives
on another line is invisible here); the gate re-runs the command as written, so a
pattern that matches only at its authoring revision and by luck still matches at
the tip passes -- the gate prices the claimed count, not the sentence's meaning.

Run as:
  python3 plans/correction_command_check.py --lane .          # verdict
  python3 plans/correction_command_check.py --selftest         # fixture battery
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shlex
import subprocess
import sys
import tempfile

POPULATION_GLOB = "plans/round-*-claims.md"
SECTION_HEADING_RE = re.compile(r"(?im)^#{2,3} .*dated correction.*$")
ANY_HEADING_RE = re.compile(r"(?m)^#{2,3} ")
CMD_RE = re.compile(
    r"`(grep -c[A-Za-z]* '(?:[^']*)' [^`\n]+?)`[^\n]*?→\s*(\d+)")
SEGMENT_RE = re.compile(r"^===.*$", re.M)
GATE_TOKEN = "correction_command_check"

LINE_RE = re.compile(r"(?m)^")


def has_erratum_marker(text: str) -> bool:
    """True when some ===-delimited block names both an ERRATUM (round N) and this gate."""
    matches = list(SEGMENT_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        seg = text[m.start():end]
        if "ERRATUM (round" in seg and GATE_TOKEN in seg:
            return True
    return False


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def iter_sections(text: str):
    """Yield (start_offset, end_offset, heading) for each dated-correction section."""
    matches = list(SECTION_HEADING_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        nxt = ANY_HEADING_RE.search(text, start)
        end = nxt.start() if nxt else len(text)
        yield m.start(), end, m.group(0).strip()


def run_command(cmd: str, lane: pathlib.Path):
    """Execute the frozen command class with cwd=lane. Returns (status, got, detail)
    where status is one of ok / defect / exec-error / out-of-scope."""
    try:
        argv = shlex.split(cmd)
    except ValueError as exc:
        return "out-of-scope", None, f"unparsable ({exc})"
    if not argv or argv[0] != "grep":
        return "out-of-scope", None, "not-a-grep-command"
    path = argv[-1]
    if (path.startswith("/") or path.startswith("\\") or ".." in path
            or "<" in path or ">" in path or ":" in path):
        return "out-of-scope", None, f"path-outside-lane ({path})"
    target = (lane / path)
    try:
        target.resolve().relative_to(lane.resolve())
    except ValueError:
        return "out-of-scope", None, f"path-outside-lane ({path})"
    try:
        proc = subprocess.run(argv, cwd=str(lane), capture_output=True, text=True,
                              timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "exec-error", None, str(exc)[:120]
    out = proc.stdout.strip()
    if proc.returncode not in (0, 1):
        return "exec-error", None, f"rc={proc.returncode} {proc.stderr.strip()[:120]}"
    if not out.isdigit():
        return "exec-error", None, f"non-numeric stdout {out!r}"
    return "ok", int(out), ""


def scan(lane: pathlib.Path, lines: list[str]):
    docs = sorted(lane.glob(POPULATION_GLOB))
    tot_ok = tot_skip = tot_d = tot_e = n_secs = n_cmds = 0
    for doc in docs:
        try:
            text = doc.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            text = doc.read_bytes().decode("utf-8", errors="replace")
        rel = doc.relative_to(lane).as_posix()
        file_cmds = list(CMD_RE.finditer(text))
        if not file_cmds:
            continue
        erratum = has_erratum_marker(text)
        file_d = file_e = 0
        for start, end, heading in iter_sections(text):
            section = text[start:end]
            heading_line = line_of(text, start)
            found = list(CMD_RE.finditer(section))
            if not found:
                continue
            n_secs += 1
            lines.append(f"SECTION {rel}:{heading_line} {heading[:70]}")
            for m in found:
                n_cmds += 1
                cmd, want = m.group(1), int(m.group(2))
                at = line_of(section, m.start()) + heading_line - 1
                status, got, detail = run_command(cmd, lane)
                if status == "out-of-scope":
                    tot_skip += 1
                    lines.append(f"SKIP {rel}:{at} {detail}")
                    continue
                if status == "exec-error":
                    file_d += 1
                    lines.append(f"CMD-DEFECT {rel}:{at} reason=exec-error "
                                 f"detail={detail} want={want}")
                    continue
                if got == want:
                    tot_ok += 1
                    lines.append(f"OK {rel}:{at} got={got} want={want}")
                else:
                    file_d += 1
                    lines.append(f"CMD-DEFECT {rel}:{at} got={got} want={want}")
        if erratum and file_d:
            file_e = file_d
            file_d = 0
            lines.append(f"ERRATUM {rel} converts={file_e}")
        tot_d += file_d
        tot_e += file_e
    lines.append(f"CMDPOP files={len(docs)} sections={n_secs} commands={n_cmds} "
                 f"ok={tot_ok} out_of_scope={tot_skip} defects={tot_d} errata={tot_e}")
    if not docs:
        lines.append("SETUP empty population -- never a vacuous pass")
        lines.append("PREDICATE R60-C2 n/a (setup)")
        return 2, len(docs)
    ok = tot_d == 0
    lines.append(f"PREDICATE R60-C2 {'pass' if ok else 'fail'}")
    return (0 if ok else 1), len(docs)


def selftest() -> int:
    """Fixture battery: both directions of the verdict, the erratum conversion,
    the foreign-block refusal, and the scope fences."""
    with tempfile.TemporaryDirectory(prefix="k60-c2-") as td:
        lane = pathlib.Path(td)
        (lane / "plans").mkdir()
        good = (
            "# claims\n\n"
            "## Dated corrections\n\n"
            "The count is reproducible: `grep -c 'NEEDLE_A' data.txt` → 2.\n"
        )
        bad = (
            "# claims\n\n"
            "## Dated correction: stale\n\n"
            "This one drifted: `grep -c 'NEEDLE_B' data.txt` → 5.\n"
        )
        erratum = bad + (
            "=== ERRATUM (round 60, 2026-11-02) — the command above counts matching "
            "LINES and the claimed phrase spans a wrapped line; the reproducing "
            "command is `grep -c 'NEEDLE_B' data.txt` → 1, per "
            "plans/correction_command_check.py ===\n"
        )
        foreign = bad + (
            "=== ERRATUM (round 60, 2026-11-02) — a correction block that names some "
            "other gate and not this one converts nothing ===\n"
        )
        fenced = (
            "# claims\n\n"
            "## Dated correction: fences\n\n"
            "No expectation: `grep -c 'NEEDLE_C' data.txt`.\n"
            "Not grep: `python3 plans/some_probe.py --lane .` → 3.\n"
            "Outside lane: `grep -c 'NEEDLE_D' <fleet>/reports/x.md` → 1.\n"
            "Escape attempt: `grep -c 'NEEDLE_E' ../outside.txt` → 1.\n"
            "Match on a NON-correction heading (out of population):\n\n"
            "## Before-anchors\n\n"
            "`grep -c 'NEEDLE_F' data.txt` → 999.\n"
        )
        (lane / "plans" / "round-60-claims.md").write_text(good, encoding="utf-8")
        (lane / "data.txt").write_text("NEEDLE_A x\nNEEDLE_A y\nNEEDLE_B z\n", encoding="utf-8")

        cases = []

        def run_case(name, doc_text, want_summary):
            f = lane / "plans" / "round-60-claims.md"
            f.write_text(doc_text, encoding="utf-8")
            lines = []
            rc, files = scan(lane, lines)
            summary = lines[-2]
            ok = (rc == want_summary[0]) and (want_summary[1] in summary)
            cases.append((name, ok, rc, summary))

        run_case("1-ok-reproduces", good, (0, "ok=1"))
        run_case("2-defect-drifted", bad, (1, "defects=1 errata=0"))
        run_case("3-erratum-converts", erratum, (0, "defects=0 errata=1"))
        run_case("4-foreign-block-refused", foreign, (1, "defects=1 errata=0"))
        run_case("5-fences", fenced, (0, "out_of_scope=2"))
        for name, ok, rc, summary in cases:
            print(f"SELFTEST {name} rc={rc} :: {summary} :: "
                  f"{'ok' if ok else 'FAIL'}")
        # empty population: setup, never a vacuous pass
        for p in (lane / "plans").glob("*.md"):
            p.unlink()
        lines = []
        rc, files = scan(lane, lines)
        empty_ok = rc == 2
        print(f"SELFTEST 6-empty-population rc={rc} files={files} :: "
              f"{'ok' if empty_ok else 'FAIL'}")
        cases.append(("6-empty-population", empty_ok, rc, ""))
        failed = sum(1 for c in cases if not c[1])
        print(f"SELFTEST cases={len(cases)} failed={failed}")
        return 0 if failed == 0 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    lane = pathlib.Path(a.lane)
    lines = []
    rc, _files = scan(lane, lines)
    text = "\n".join(lines) + "\n"
    print(text, end="")
    return rc


if __name__ == "__main__":
    sys.exit(main())
