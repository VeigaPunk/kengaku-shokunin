#!/usr/bin/env python3
"""Require every conditional refusal in a lesson's Gate section to be resolved.

A Gate row that refuses a candidate and states a flip condition — "Flip: ...",
"... flips when ...", "if ... admit ..." — is an obligation on a later round,
because the condition can fire at landing. Round 42 is the measured instance:
its `Dockerfile` reject says "if the entry keeps the `WORKDIR /app` sentence
..., admit `Dockerfile` as a tier-B mechanism row", the landed entry kept the
sentence and made it load-bearing, no `S###` row was ever opened, and nobody
recorded that the flip had fired (`.ufo/waves/round-42/falsify/` D3; the
round's own Gate prose at `corpus/lessons/round-42.md:44`).

The checker reads one lesson file (one `--lesson` argument), takes the `## Gate`
section, keeps the refusals that carry a flip condition, and requires each to
be resolved by a LATER line of the same lesson:

    Flip check (round N): <item> — fired|not fired — <evidence>

Rules, in the order they are applied:

1. Section. `## Gate` is matched as a level-2 heading and ends at the next
   level-1 or level-2 heading (or EOF). No such section is a setup error.
2. Refusals. A table row (a `|`-delimited line in the section, header and
   `---` separator skipped) is a refusal when its verdict cell — the second
   cell — matches REJECT, REJECTED, REFUSE or REFUSED case-insensitively.
   A bullet (`- ...` / `* ...`) is a refusal when it carries the same words.
   A row whose verdict says "Admitted" is not a refusal and is not counted
   even though admitted rows usually carry a flip sentence too; a row that is
   only "Captured, not a row" is not an explicit REJECT and is likewise not
   counted. That exclusion is deliberate and is visible in `refused_rows=`.
3. Flips. A refusal carries its flip in its own text (`flip:`, `flips when`,
   `if ... admit` — the three shapes the lessons use) or in a companion line of
   the same section that names the refused candidate: the round-30 shape, where
   the table's rejects are followed by a bullet list "Flip conditions (one per
   rejected candidate)". A companion line that names no refused candidate is
   not attached, and a refusal with no flip at all is not an obligation.
4. Resolution. A line matching `Flip check (round N): <item> — <state> —
   <evidence>` resolves a row when (a) it sits after the row's flip statement,
   (b) `<item>` equals the row's item or is that item plus a qualifier
   (`Dockerfile @ 2fd12b88`), (c) `<state>` is `fired` or `not fired`,
   (d) `<evidence>` has at least two words and is not a placeholder
   (`none`, `n/a`, `todo`, `tbd`, `-`, ...), and (e) N is not smaller than the
   round in the lesson's file name. `--` is accepted as a separator when the
   em dash is not used. A line that starts `Flip check (round` but breaks the
   shape is reported as malformed and resolves nothing. When several lines
   name the same item, the last one decides: an appended correction
   supersedes the line it corrects, and a later malformed or thin-evidence
   line leaves the obligation unresolved.

5. Citation leg (round 44). A `not fired` resolution that names a file is
   checked against the entry the lesson's Gate concerns: the `.md` files the
   Gate section names resolve under the lesson repo's `corpus/knowledge/`
   (plus any `--entry` path), and when one of them carries a
   `<file>:<line>` citation of a file the `not fired` line names, the line is
   red (`FLIP-CITE ... verdict=RED`). Round 43 is the measured instance: its
   `task.toml` reject is recorded `not fired` while the landed entry cites
   `task.toml:22` twice as the only ceiling on the graded call
   (`corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md:122`,
   `:300`; disagreement `corpus/lessons/round-43-verifier-spotcheck.md:129-141`).
   The leg only reads a `not fired` line that the checker accepts as the
   resolution; a `fired` line is never tested, and a Gate whose entries are
   absent leaves the leg inactive (`FLIP-CITE entries=-`).

Exit: 0 every conditional refusal is resolved and no `not fired` resolution
names a file an entry cites; 1 either defect is present (the `FLIPS` and
`FLIP-CITE` lines carry the counts); 2 setup/usage (unreadable lesson, no
`## Gate` section, argparse).

`--selftest` builds fixtures in a temporary directory and runs this script on
them as a subprocess, so both the parser and the CLI are exercised: each case
is expected red (exit 1) or green (exit 0) and the run prints one line per
case plus `SELFTEST ok=<k>/<n>`.

Limits, named: the section split is heading-based, so a lesson that puts its
Gate table under `### Gate` is a setup error rather than a guess; a cell
containing a literal `|` is read as extra cells (the verdict is still cell 2,
the rest only widen the scanned text); a companion flip line attaches to
every refused candidate it names (a bullet naming two ids obliges both) and
its item is the bullet's first code span, so a bullet whose candidate is
described only in prose attaches only when the prose matches the cell
verbatim after markdown stripping; the tool checks that a flip was
*recorded*, never that the recorded consequence was the right one, so a
`fired` line whose evidence contradicts its own landing passes; it reads the
working tree only and has no opinion about history, so a resolution line that
was committed and later deleted is invisible; one obligation per row is
assumed, so a row carrying two independent flip conditions is resolved by one
line naming it; and the citation leg is a name match, not a reading: it sees
`<file>:<line>` where the file name and the line stand together, so an entry
that names the file in one cell and the line in the next (`| cmd | task.toml |
:22 |`) is not seen, an extension-less name outside its small literal set is
not seen, a `<file>:<range>` inside a longer citation list is seen once for
the whole entry, a cited *directory* is not seen, and an entry it cannot
resolve under `corpus/knowledge/` is reported `missing` rather than judged.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

EMDASH = "\u2014"

GATE_HEADING_RE = re.compile(r"^##\s+Gate\s*$")
SECTION_END_RE = re.compile(r"^#{1,2}\s+\S")
REFUSAL_RE = re.compile(r"(?i)\b(?:reject(?:ed)?|refus(?:e|ed))\b")
ADMIT_RE = re.compile(r"(?i)\b(?:admit(?:ted)?|accepted?)\b")
SEPARATOR_CELL_RE = re.compile(r"^:?-{2,}:?$")

SHAPE_PATTERNS = (
    ("flip:", re.compile(r"(?i)\bflips?\s*:")),
    ("flips-when", re.compile(r"(?i)\bflips?\s+when\b")),
    ("if-admit", re.compile(r"(?i)\bif\b[^|]{0,240}?\badmit(?:ted)?\b")),
)

RES_PREFIX_RE = re.compile(r"(?i)^flip\s+check\s*\(\s*round\s+(\d+)\s*\)\s*:")
ROUND_IN_NAME_RE = re.compile(r"(?i)\bround-(\d+)\b|\br(\d+)\b")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
ID_PREFIX_RE = re.compile(r"^[A-Z]{1,3}\d{2,}\b")

MD_REF_RE = re.compile(r"[A-Za-z0-9._/+-]+\.md\b")
FILE_TOKEN_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.+-]*\.[A-Za-z][A-Za-z0-9]{0,7}\b")
BARE_FILE_RE = re.compile(r"(?i)\b(?:dockerfile|makefile|sha256sums|licen[cs]e|changelog)\b")
KNOWLEDGE_DIR = os.path.join("corpus", "knowledge")

PLACEHOLDERS = frozenset({
    "none", "n/a", "na", "nil", "todo", "tbd", "tba", "?", "-", "ok", "yes", "no", "done",
})


class SetupError(Exception):
    """The lesson cannot be evaluated."""


def normalize(text):
    """Comparison form: no code marks, no emphasis, collapsed spaces, casefold.

    A leading article is dropped so a candidate cell ("remaining 63 staged
    entries") and a companion flip bullet ("the remaining 63 staged entries")
    compare equal.
    """
    out = text.replace("`", "").replace("*", "").replace("_", "")
    out = out.strip().strip("\"'").strip()
    out = " ".join(out.split()).casefold()
    if out.startswith("the "):
        out = out[4:]
    return out


def gate_section(lines):
    """Return (start, end) line indices of the `## Gate` body."""
    start = None
    for i, line in enumerate(lines):
        if GATE_HEADING_RE.match(line.strip()):
            start = i
            break
    if start is None:
        raise SetupError("no '## Gate' section")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if SECTION_END_RE.match(lines[j].strip()):
            end = j
            break
    return start + 1, end


def table_fields(line):
    """Cells of a `| a | b |` line, outer pipes dropped."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.strip() for cell in body.split("|")]


def item_token(candidate_text):
    """Human item name for a Gate row/bullet.

    Order: an id prefix (`S042`, `XO5`), else the first code span, else the
    leading words up to ` @ `, ` (` or a comma. A bullet's bold verdict marker
    (`**Rejected:**`) is dropped first so the item is the candidate, not the
    verdict word.
    """
    text = re.sub(r"^\*\*[^*]+\*\*\s*:?\s*", "", candidate_text.strip()).strip()
    text = text.strip("*_ ")
    ident = ID_PREFIX_RE.match(text)
    if ident:
        return ident.group(0)
    span = CODE_SPAN_RE.search(text)
    if span:
        raw = span.group(1).rstrip(",:;")
    else:
        raw = re.split(r"\s+@\s+|\s+\(|,", text, maxsplit=1)[0]
    return " ".join(raw.strip().strip("*_ ").split())


def flip_shapes(text):
    return [name for name, pattern in SHAPE_PATTERNS if pattern.search(text)]


def collect_obligations(lines, start, end):
    """Refusals in the Gate section, each with its flip condition.

    A refusal carries its flip either in its own text (`Flip:`, `flips when`,
    `if ... admit`) or in a companion line of the same section that names the
    refused candidate — the round-30 shape, where the table's rejects are
    followed by a bullet list "Flip conditions (one per rejected candidate)".
    A companion line that names no refused candidate is not attached, and a
    table row that is not a refusal is never attached even when it carries a
    flip (admitted and merely-captured rows do).
    """
    refusals = []
    companion = []
    for i in range(start, end):
        stripped = lines[i].strip()
        shapes = flip_shapes(stripped)
        if stripped.startswith("|"):
            fields = table_fields(stripped)
            if not fields or all(SEPARATOR_CELL_RE.match(cell) for cell in fields if cell):
                continue
            lowered = [cell.casefold() for cell in fields]
            if "verdict" in lowered and any(cell.startswith("candidate") for cell in lowered):
                continue
            if len(fields) < 2:
                continue
            candidate, verdict = fields[0], fields[1]
            if ADMIT_RE.search(verdict) and not REFUSAL_RE.search(verdict):
                continue
            if not REFUSAL_RE.search(verdict):
                continue
            refusals.append({
                "line": i + 1,
                "item": item_token(candidate),
                "shapes": shapes,
                "flip_line": i + 1 if shapes else None,
            })
            continue
        body = stripped[1:].strip() if stripped[:1] in ("-", "*") else stripped
        if REFUSAL_RE.search(body):
            refusals.append({
                "line": i + 1,
                "item": item_token(body),
                "shapes": shapes,
                "flip_line": i + 1 if shapes else None,
            })
        elif shapes:
            companion.append((i + 1, body))

    for flip_line, text in companion:
        keys = {normalize(item_token(text))}
        keys.update(normalize(span) for span in CODE_SPAN_RE.findall(text))
        keys.discard("")
        for refusal in refusals:
            if refusal["flip_line"] is not None:
                continue
            if normalize(refusal["item"]) in keys:
                refusal["flip_line"] = flip_line
                refusal["shapes"] = flip_shapes(text)
    return [row for row in refusals if row["flip_line"] is not None], len(refusals)


def parse_resolution(line):
    """Parse a `Flip check (round N): ...` line, or None when the prefix is absent."""
    match = RES_PREFIX_RE.match(line.strip())
    if not match:
        return None
    rest = line.strip()[match.end():].strip()
    if EMDASH in rest:
        parts = [part.strip() for part in re.split(r"\s*" + EMDASH + r"\s*", rest)]
    else:
        parts = [part.strip() for part in re.split(r"\s+--\s+", rest)]
    record = {"round": int(match.group(1)), "item": "", "state": "", "evidence": "",
              "malformed": ""}
    if len(parts) < 3:
        record["malformed"] = "expected '<item> " + EMDASH + " fired|not fired " + EMDASH + " <evidence>'"
        return record
    record["item"] = parts[0]
    record["state"] = " ".join(parts[1].split()).casefold()
    record["evidence"] = " ".join(parts[2:]).strip()
    if record["state"] not in ("fired", "not fired"):
        record["malformed"] = "state is neither 'fired' nor 'not fired'"
        return record
    if not record["item"]:
        record["malformed"] = "empty item"
    return record


def evidence_problem(evidence):
    words = [word.strip("`*_.,;:()[]") for word in evidence.split()]
    words = [word for word in words if word]
    if not words:
        return "evidence-missing"
    if len(words) == 1 and words[0].casefold() in PLACEHOLDERS:
        return "evidence-placeholder"
    if len(words) < 2:
        return "evidence-thin"
    return ""


def item_matches(key, resolved_item):
    right = normalize(resolved_item)
    if right == key:
        return True
    if right.startswith(key) and len(right) > len(key) and right[len(key)] in " @(:;,/":
        return True
    return False


def lesson_round(path):
    match = ROUND_IN_NAME_RE.search(os.path.basename(path))
    if not match:
        return None
    return int(match.group(1) or match.group(2))


def resolve(obligation, lines, lesson_rnd):
    """Return (detail, ok, (line, record)) for one obligation.

    The resolution must follow the flip line, and the LAST matching line
    decides: an appended correction (the lane's append-only way of fixing a
    false verdict, `corpus/lessons/round-43-verifier-spotcheck.md` R1) must be
    able to supersede the line it corrects, and a later malformed or
    thin-evidence record leaves the obligation unresolved rather than letting
    an older valid line stand.
    """
    key = normalize(obligation["item"])
    matched_item_after_row = False
    last_reason = "no-line"
    accepted = None
    for j, line in enumerate(lines):
        record = parse_resolution(line)
        if record is None:
            continue
        if j + 1 <= obligation["flip_line"]:
            if item_matches(key, record["item"]):
                last_reason = "before-flip"
            continue
        if not record["item"]:
            continue
        if not item_matches(key, record["item"]):
            continue
        matched_item_after_row = True
        accepted = None
        if record["malformed"]:
            last_reason = "malformed"
            continue
        problem = evidence_problem(record["evidence"])
        if problem:
            last_reason = problem
            continue
        if lesson_rnd is not None and record["round"] < lesson_rnd:
            last_reason = "round-before-lesson"
            continue
        last_reason = "accepted"
        accepted = (j + 1, record)
    if accepted is not None:
        record = accepted[1]
        return ("line:%d:%s:round=%d" % (accepted[0], record["state"], record["round"]),
                True, accepted)
    if not matched_item_after_row and last_reason == "no-line":
        return "unresolved:no-line", False, None
    return "unresolved:" + last_reason, False, None


def lesson_repo_root(lesson_path):
    """Nearest ancestor of the lesson that holds a corpus/knowledge directory."""
    here = os.path.dirname(os.path.abspath(lesson_path))
    while True:
        if os.path.isdir(os.path.join(here, KNOWLEDGE_DIR)):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            return None
        here = parent


def named_files(text):
    """Files a resolution line names, in order, deduplicated case-insensitively."""
    names = []
    seen = set()
    for match in FILE_TOKEN_RE.finditer(text):
        name = match.group(0).rstrip(".")
        key = name.casefold()
        if key and key not in seen:
            seen.add(key)
            names.append(name)
    for match in BARE_FILE_RE.finditer(text):
        name = match.group(0)
        key = name.casefold()
        if key not in seen:
            seen.add(key)
            names.append(name)
    return names


def gate_entries(lines, start, end, lesson_path, extra_paths=()):
    """The entries a lesson's Gate concerns: its named .md files, resolved.

    A `.md` name in the Gate section is looked up as
    `<repo>/corpus/knowledge/<basename>`; `extra_paths` (the `--entry` option)
    adds files, or every `*.md` of a directory. Returns ([(path, lines)],
    [missing name]). A name that resolves nowhere is missing, never judged.
    """
    names = []
    for i in range(start, end):
        for token in MD_REF_RE.findall(lines[i]):
            base = os.path.basename(token)
            if base.casefold() not in {name.casefold() for name in names}:
                names.append(base)
    paths = []
    missing = []
    root = lesson_repo_root(lesson_path)
    for name in names:
        found = None
        if root is not None:
            candidate = os.path.join(root, KNOWLEDGE_DIR, name)
            if os.path.isfile(candidate):
                found = candidate
        if found is None:
            missing.append(name)
        elif os.path.realpath(found) not in paths:
            paths.append(os.path.realpath(found))
    for extra in extra_paths:
        extra = os.path.abspath(extra)
        if os.path.isdir(extra):
            for name in sorted(os.listdir(extra)):
                candidate = os.path.join(extra, name)
                if name.endswith(".md") and os.path.isfile(candidate):
                    real = os.path.realpath(candidate)
                    if real not in paths:
                        paths.append(real)
        elif os.path.isfile(extra):
            real = os.path.realpath(extra)
            if real not in paths:
                paths.append(real)
        else:
            missing.append(os.path.basename(extra) + "(not-a-file)")
    entries = []
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as handle:
                entries.append((path, handle.read().splitlines()))
        except OSError:
            missing.append(os.path.basename(path) + "(unreadable)")
    return entries, missing


def citation_re(name):
    """`<name>:<line>` with backticks or spaces allowed around the colon."""
    return re.compile(r"(?<![A-Za-z0-9_./+-])" + re.escape(name) +
                      r"[`\s]*:[`\s]*\d+(?:\s*[-\u2013]\s*\d+)?")


def citation_defects(record, entries):
    """(files named, [(file, entry path, entry line)]) for a `not fired` record."""
    names = named_files(record["item"] + " " + record["evidence"])
    defects = []
    for name in names:
        base = os.path.basename(name)
        pattern = citation_re(base)
        for path, entry_lines in entries:
            for lineno, line in enumerate(entry_lines, 1):
                if pattern.search(line):
                    defects.append((name, path, lineno, line.strip()))
                    break
    return names, defects


def check(lesson_path, entry_paths=()):
    try:
        with open(lesson_path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        raise SetupError("unreadable lesson: %s" % exc)
    lines = text.splitlines()
    start, end = gate_section(lines)
    obligations, refused_rows = collect_obligations(lines, start, end)
    rnd = lesson_round(lesson_path)
    entries, missing_entries = gate_entries(lines, start, end, lesson_path, entry_paths)

    unresolved = 0
    malformed = sum(1 for line in lines
                    if (parse_resolution(line) or {}).get("malformed"))
    not_fired = 0
    cited = 0
    for obligation in obligations:
        detail, ok, resolution = resolve(obligation, lines, rnd)
        if not ok:
            unresolved += 1
        print("FLIP line=%d flip_line=%d item=%s shapes=%s resolution=%s"
              % (obligation["line"], obligation["flip_line"], obligation["item"],
                 ",".join(obligation["shapes"]), detail))
        if not ok or resolution is None or resolution[1]["state"] != "not fired":
            continue
        not_fired += 1
        names, defects = citation_defects(resolution[1], entries)
        if not defects:
            print("FLIP-CITE line=%d item=%s state=not fired files=%s verdict=clear"
                  % (resolution[0], resolution[1]["item"], ",".join(names) or "-"))
            continue
        cited += 1
        for name, path, lineno, entry_line in defects:
            print("FLIP-CITE line=%d item=%s state=not fired file=%s citation=%s:%d "
                  "quote=\"%s\" verdict=RED"
                  % (resolution[0], resolution[1]["item"], name,
                     os.path.basename(path), lineno, entry_line[:120]))
    print("FLIP-DETAIL lesson=%s lesson_round=%s refused_rows=%d malformed_resolutions=%d"
          % (lesson_path, "-" if rnd is None else rnd, refused_rows, malformed))
    print("FLIPS total=%d unresolved=%d" % (len(obligations), unresolved))
    print("FLIP-CITE entries=%s missing=%s not_fired=%d red=%d"
          % (",".join(os.path.basename(path) for path, _ in entries) or "-",
             ",".join(missing_entries) or "-", not_fired, cited))
    return 0 if unresolved == 0 and cited == 0 else 1


# ---------------------------------------------------------------- selftest

SELFTEST_HEAD = "# Round 42 - fixture\n\n## Gate\n\n"

SELFTEST_TABLE = (
    "| Candidate | Verdict | Reason and flip condition |\n"
    "|---|---|---|\n"
)

SELFTEST_TAIL = "\n## Routed\n\nNothing routed in this fixture.\n"

DOCKER_ROW = (
    "| `Dockerfile` @ `2fd12b88` | **REJECT - captured, not a row** | "
    "The cwd claim rests on `Dockerfile:3`. Flip: if the entry keeps the "
    "`WORKDIR /app` sentence, admit `Dockerfile` as a tier-B mechanism row. |\n"
)

DOCKER_OK = "Flip check (round 43): Dockerfile " + EMDASH + " fired " + EMDASH + \
    "entry :435-438 keeps the WORKDIR sentence (D3)\n"

CITE_ROW = (
    "| `task.toml`, `setup.py` @ `2fd12b88` | **REJECT - captured, not rows** | "
    "read once. Flip: an entry sentence that rests on one of them alone. |\n"
)

CITE_ENTRY_REF = "\nGate prose: the landed entry is `tb2-fixture-grader.md`.\n"

CITE_NOT_FIRED = ("Flip check (round 43): task.toml " + EMDASH + " not fired " + EMDASH +
                  "no entry sentence rests on task.toml alone\n")

CITE_FIRED = ("Flip check (round 43): task.toml " + EMDASH + " fired " + EMDASH +
              "entry :122 cites task.toml:22 as the only ceiling\n")

CITE_ENTRY = "corpus/knowledge/tb2-fixture-grader.md"

ENTRY_CITING = (
    "# fixture entry\n\nsource: S001\n\nThe verifier timeout is `task.toml:22`.\n\n"
    "| `slow-oracle-45s` | `task.toml:22` | \"timeout_sec = 1800.0\" |\n"
)

ENTRY_CLEAR = (
    "# fixture entry\n\nsource: S001\n\nNo metadata is cited here; the capture is `README.md:35`.\n"
)


def selftest_cases():
    """(id, lesson text, expected exit code[, {path: text}[, [argv...]]]); `{case}` is the case dir."""
    table = SELFTEST_HEAD + SELFTEST_TABLE
    flips_when_row = (
        "| S042 `paper` | rejected | not openable this round; flips when an opened copy exists. |\n"
    )
    flips_when_ok = ("Flip check (round 43): S042 " + EMDASH + " not fired " + EMDASH +
                     "publisher still 403 at 2026-10-26\n")
    admit_row = (
        "| S125 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined, tier A)** | "
        "Quote at `:23`. Flip: the capture's digest leaves the pin. |\n"
    )
    captured_row = (
        "| `test.sh`, `task.toml` @ `2fd12b88` | **Captured, not rows** | "
        "author metadata, read only. Flip: a claim that needs a declared timeout. |\n"
    )
    plain_reject_row = (
        "| `notes.md` | **REJECT** | restates the three admitted artefacts; nothing to flip. |\n"
    )
    companion_row = (
        "| `paper.md` | rejected | not openable this round. |\n"
    )
    companion_flip = "\n- `paper.md` " + EMDASH + " flips when an opened copy exists.\n"
    companion_ok = ("Flip check (round 43): paper.md " + EMDASH + " not fired " + EMDASH +
                    "publisher still 403 at 2026-10-26\n")
    bullet_red = (
        "- **Rejected:** S003 (DCR factor as a general accuracy) - "
        "authors scope it as risk-aware; flip: validation on frontier-scale tasks.\n"
    )
    return [
        ("reject-flip-unresolved", table + DOCKER_ROW + SELFTEST_TAIL, 1),
        ("reject-flip-resolved", table + DOCKER_ROW + SELFTEST_TAIL + DOCKER_OK, 0),
        ("reject-flips-when-resolved",
         table + flips_when_row + SELFTEST_TAIL + flips_when_ok, 0),
        ("reject-flips-when-unresolved", table + flips_when_row + SELFTEST_TAIL, 1),
        ("resolution-before-row",
         SELFTEST_HEAD + DOCKER_OK + "\n" + SELFTEST_TABLE + DOCKER_ROW + SELFTEST_TAIL, 1),
        ("resolution-wrong-item", table + DOCKER_ROW + SELFTEST_TAIL +
         "Flip check (round 43): README.md " + EMDASH + " fired " + EMDASH +
         "entry :435 keeps the sentence\n", 1),
        ("resolution-placeholder-evidence", table + DOCKER_ROW + SELFTEST_TAIL +
         "Flip check (round 43): Dockerfile " + EMDASH + " fired " + EMDASH + "none\n", 1),
        ("resolution-thin-evidence", table + DOCKER_ROW + SELFTEST_TAIL +
         "Flip check (round 43): Dockerfile " + EMDASH + " fired " + EMDASH + "done\n", 1),
        ("resolution-round-before-lesson", table + DOCKER_ROW + SELFTEST_TAIL +
         "Flip check (round 4): Dockerfile " + EMDASH + " fired " + EMDASH +
         "entry :435 keeps the sentence\n", 1),
        ("resolution-ascii-separator", table + DOCKER_ROW + SELFTEST_TAIL +
         "Flip check (round 43): Dockerfile -- not fired -- entry :41 dropped the sentence\n", 0),
        ("resolution-malformed-shape", table + DOCKER_ROW + SELFTEST_TAIL +
         "Flip check (round 43): Dockerfile " + EMDASH + " probably " + EMDASH +
         "entry :435 keeps the sentence\n", 1),
        ("admitted-row-with-flip-not-counted",
         table + admit_row + captured_row + SELFTEST_TAIL, 0),
        ("plain-reject-without-flip",
         table + plain_reject_row + DOCKER_ROW + SELFTEST_TAIL + DOCKER_OK, 0),
        ("bullet-reject-flip-unresolved", SELFTEST_HEAD + bullet_red + SELFTEST_TAIL, 1),
        ("bullet-reject-flip-resolved", SELFTEST_HEAD + bullet_red + SELFTEST_TAIL +
         "Flip check (round 43): S003 " + EMDASH + " not fired " + EMDASH +
         "no frontier-scale validation run\n", 0),
        ("companion-flip-unresolved",
         table + companion_row + companion_flip + SELFTEST_TAIL, 1),
        ("companion-flip-resolved",
         table + companion_row + companion_flip + SELFTEST_TAIL + companion_ok, 0),
        ("companion-flip-unmatched-candidate",
         table + companion_row + "\n- `ghost.md` " + EMDASH +
         " flips when an opened copy exists.\n" + SELFTEST_TAIL, 0),
        ("no-gate-section", "# Round 42 - fixture\n\n## Admitted\n\nNothing.\n", 2),
        # citation leg (round 44): a `not fired` line naming a file the entry cites
        ("cite-not-fired-red",
         table + CITE_ROW + CITE_ENTRY_REF + SELFTEST_TAIL + CITE_NOT_FIRED, 1,
         {CITE_ENTRY: ENTRY_CITING}),
        ("cite-not-fired-clear",
         table + CITE_ROW + CITE_ENTRY_REF + SELFTEST_TAIL + CITE_NOT_FIRED, 0,
         {CITE_ENTRY: ENTRY_CLEAR}),
        ("cite-fired-not-tested",
         table + CITE_ROW + CITE_ENTRY_REF + SELFTEST_TAIL + CITE_FIRED, 0,
         {CITE_ENTRY: ENTRY_CITING}),
        ("cite-entry-missing",
         table + CITE_ROW + CITE_ENTRY_REF + SELFTEST_TAIL + CITE_NOT_FIRED, 0, {}),
        ("cite-not-fired-names-no-file",
         table + flips_when_row + "\nGate prose: `tb2-fixture-grader.md` is the entry.\n" +
         SELFTEST_TAIL + flips_when_ok, 0, {CITE_ENTRY: ENTRY_CITING}),
        ("cite-later-fired-supersedes",
         table + CITE_ROW + CITE_ENTRY_REF + SELFTEST_TAIL + CITE_NOT_FIRED + CITE_FIRED, 0,
         {CITE_ENTRY: ENTRY_CITING}),
        ("cite-later-not-fired-reopens",
         table + CITE_ROW + CITE_ENTRY_REF + SELFTEST_TAIL + CITE_FIRED + CITE_NOT_FIRED, 1,
         {CITE_ENTRY: ENTRY_CITING}),
        ("cite-entry-flag",
         table + CITE_ROW + SELFTEST_TAIL + CITE_NOT_FIRED, 1,
         {CITE_ENTRY: ENTRY_CITING},
         ["--entry", "{case}/" + CITE_ENTRY]),
    ]


def parse_flips(stdout):
    total = unresolved = None
    for line in stdout.splitlines():
        if line.startswith("FLIPS "):
            fields = dict(part.split("=", 1) for part in line.split()[1:] if "=" in part)
            total = int(fields.get("total", "-1"))
            unresolved = int(fields.get("unresolved", "-1"))
    return total, unresolved


def parse_cite(stdout):
    for line in stdout.splitlines():
        if line.startswith("FLIP-CITE entries="):
            fields = dict(part.split("=", 1) for part in line.split()[1:] if "=" in part)
            return int(fields.get("not_fired", "-1")), int(fields.get("red", "-1"))
    return -1, -1


def run_selftest():
    here = os.path.abspath(sys.argv[0])
    work = tempfile.mkdtemp(prefix="flip-selftest-")
    failures = 0
    cases = selftest_cases()
    try:
        for case in cases:
            name, text, expect_rc = case[0], case[1], case[2]
            extras = case[3] if len(case) > 3 else {}
            case_dir = os.path.join(work, name)
            lessons = os.path.join(case_dir, "corpus", "lessons")
            os.makedirs(lessons)
            for rel, body in extras.items():
                path = os.path.join(case_dir, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(body)
            lesson = os.path.join(lessons, "round-42.md")
            with open(lesson, "w", encoding="utf-8") as handle:
                handle.write(text)
            extra_args = [arg.replace("{case}", case_dir)
                          for arg in (case[4] if len(case) > 4 else [])]
            proc = subprocess.run([sys.executable, here, "--lesson", lesson] + extra_args,
                                  capture_output=True, text=True)
            total, unresolved = parse_flips(proc.stdout)
            not_fired, cite_red = parse_cite(proc.stdout)
            got = "green" if proc.returncode == 0 else ("red" if proc.returncode == 1 else "setup")
            want = "green" if expect_rc == 0 else ("red" if expect_rc == 1 else "setup")
            ok = proc.returncode == expect_rc
            if not ok:
                failures += 1
            print("SELFTEST case=%s expect=%s got=%s total=%s unresolved=%s "
                  "not_fired=%s cite_red=%s rc=%d %s"
                  % (name, want, got, total, unresolved, not_fired, cite_red,
                     proc.returncode, "ok" if ok else "FAIL"))
            if not ok:
                for line in (proc.stdout + proc.stderr).splitlines():
                    print("SELFTEST   | " + line)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("SELFTEST ok=%d/%d" % (len(cases) - failures, len(cases)))
    return 0 if failures == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Require every conditional Gate refusal to be resolved by a recorded flip check.")
    parser.add_argument("--lesson", help="lesson markdown file whose `## Gate` section is checked")
    parser.add_argument("--entry", action="append", default=[],
                        help="entry markdown file (or a directory of them) the Gate concerns; "
                             "repeatable; defaults to the `.md` names of the Gate section resolved "
                             "under the lesson repo's corpus/knowledge/")
    parser.add_argument("--selftest", action="store_true",
                        help="run the built fixtures and show the checker red and green")
    args = parser.parse_args(argv)
    if args.selftest:
        return run_selftest()
    if not args.lesson:
        parser.error("--lesson is required unless --selftest is given")
    try:
        return check(args.lesson, args.entry)
    except SetupError as exc:
        print("SETUP %s" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
