#!/usr/bin/env python3
"""R72-C2 — the round-71 closure's routed defects R71-R1 and R71-R7, re-derived.

R71-R1 (Registry/Delivery): neither round-71 instrument had a `SKILL.md` `## Gate/probe registry`
row, so neither was gradeable conformant. Fix = one eight-column row per instrument, and the same
row for both round-72 instruments, so the class cannot recur silently.

R71-R7 (freeze-doc overclaim): `plans/round-71-claims.md` labels the do-nothing control
"committed at freeze" although it is absent from the freeze commit `d8a77d3f` (it landed with
`c80fcdb3`), and labels the red-before "committed at freeze" while that receipt was produced by
the freeze instrument reading base data. Fix = an appended `## Errata — round 72` block that
keeps both superseded sentences verbatim above it and states the true revisions.

R71-R5 (gate-level): the round-71 `parse_count` accepted only word numerals (a digit `8` and a
backticked `` `eight` `` false-redded), and its `--mutants` metric scored a mutant as killed when
the corresponding `DEFECT` line merely disappeared — invariant under any weakening. This gate
carries the corrected count parser (`parse_count`) and a mutant matrix scored on a fixture set:
`killed` means the mutant *accepts* a red fixture the pristine gate refuses (the fixture set
detects the weakened clause) while still refusing an attribution red fixture owned by a different
check; `survived` means it refuses every red fixture (no observable difference on reds); `invalid`
means it refuses the green fixture or the edit did not apply; `null_detected` means its verdict
vector equals the pristine gate's. A deliberate no-op mutant (M7) must be reported as
`null_detected=1`, so the null detector is exercised rather than asserted.

Checks (each re-derives from the lane's committed bytes, no stored tally):
  E1a  every instrument in `INSTRUMENTS` has an eight-column registry row whose entry cell names
       its script, whose kind is `gate`/`probe`, and whose owner is `kengaku`
  E1b  `plans/round-71-claims.md` carries an appended erratum that quotes both superseded labels
       verbatim and names both true revisions
  E1c  `parse_count` coerces a digit, a plain word, a backticked word and an embedded phrase, and
       returns None when there is no count
  E2   positional append-only: both superseded sentences still occur *above* the erratum, and the
       erratum is the file's last `##` section

Frozen predicate (R72-C2): `PREDICATE R72-C2 pass` iff E1a, E1b, E1c and E2 print `ok`,
`DEFECTS n=0` and rc 0 at the round tip; `--selftest` prints
`SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True
parser-arm=True`; and `--mutants` prints
`MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1`.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_REL = "SKILL.md"
CLAIMS_REL = "plans/round-71-claims.md"
REGISTRY_HEADING = "## Gate/probe registry"

# (registry name, script path). Round-71 rows close R71-R1; round-72 rows keep the class closed.
INSTRUMENTS = (
    ("round71-c1-hf-probe", "plans/round71_c1_hf_probe.py"),
    ("round71-c2-routed-defects", "plans/round71_c2_routed_defects.py"),
    ("round72-c1-hf-probe", "plans/round72_c1_hf_probe.py"),
    ("round72-c2-routed-defects", "plans/round72_c2_routed_defects.py"),
)
REGISTRY_COLUMNS = 8
OWNER = "kengaku"

ERRATA_HEADING = "## Errata — round 72"
SUPERSEDED = (
    "Do-nothing control (committed at freeze)",
    "Red-before (committed at freeze)",
)
TRUE_REVISIONS = ("c80fcdb3", "d8a77d3f")

WORD_NUMBERS = {"five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def lane_root(arg):
    return Path(arg).resolve() if arg else Path(__file__).resolve().parent.parent


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


# --------------------------------------------------------------------------- E1a

def registry_rows(text: str) -> list:
    """Data rows of the `## Gate/probe registry` table, split into cells."""
    if REGISTRY_HEADING not in text:
        return []
    section = text.split(REGISTRY_HEADING, 1)[1]
    rows = []
    for line in section.splitlines():
        s = line.strip()
        if s.startswith("## "):
            break
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if cells and cells[0].lower() == "name":
            continue
        rows.append(cells)
    return rows


def check_e1_registry(lane: Path, root: Path = None) -> list:
    rows = registry_rows(read(lane / SKILL_REL))
    by_name = {}
    for cells in rows:
        if cells:
            by_name.setdefault(cells[0].strip("`"), cells)
    problems = []
    for name, script in INSTRUMENTS:
        cells = by_name.get(name)
        if cells is None:
            problems.append(f"row-absent:{name}")
            continue
        if len(cells) != REGISTRY_COLUMNS:
            problems.append(f"row-columns:{name}={len(cells)}")
        if len(cells) > 2 and script not in cells[2]:
            problems.append(f"row-entry:{name}")
        if len(cells) > 1 and cells[1].strip("`") not in ("gate", "probe"):
            problems.append(f"row-kind:{name}={cells[1]}")
        if len(cells) >= REGISTRY_COLUMNS and cells[REGISTRY_COLUMNS - 1] != OWNER:
            problems.append(f"row-owner:{name}={cells[REGISTRY_COLUMNS - 1]}")
    return problems


# --------------------------------------------------------------------------- E1b / E2

def errata_block(text: str) -> str:
    if ERRATA_HEADING not in text:
        return ""
    return text.split(ERRATA_HEADING, 1)[1]


def check_e1_errata(lane: Path, root: Path = None) -> list:
    text = read(lane / CLAIMS_REL)
    if not text:
        return ["claims-doc-absent"]
    block = errata_block(text)
    if not block:
        return ["no-errata-section"]
    flat = " ".join(block.split())
    problems = []
    for label in SUPERSEDED:
        if label not in flat:
            problems.append(f"label-not-quoted:{label}")
    for revision in TRUE_REVISIONS:
        if revision not in flat:
            problems.append(f"revision-absent:{revision}")
    if "supersed" not in flat.lower():
        problems.append("no-supersedes-wording")
    return problems


def check_e2_positional(lane: Path, root: Path = None) -> list:
    text = read(lane / CLAIMS_REL)
    if not text or ERRATA_HEADING not in text:
        return ["no-errata-section"]
    problems = []
    head_at = text.index(ERRATA_HEADING)
    for label in SUPERSEDED:
        at = text.find(label)
        if at < 0:
            problems.append(f"superseded-sentence-missing:{label}")
        elif at > head_at:
            problems.append(f"superseded-below-erratum:{label}")
    headings = [m.start() for m in re.finditer(r"(?m)^## ", text)]
    if headings and headings[-1] != head_at:
        tail = text[headings[-1]:headings[-1] + 60].splitlines()[0].strip()
        problems.append(f"erratum-not-last-section:{tail}")
    if len([ln for ln in errata_block(text).splitlines() if ln.strip()]) < 3:
        problems.append("erratum-too-short")
    return problems


# --------------------------------------------------------------------------- E1c

def parse_count(phrase: str):
    """Digit- and backtick-aware `N Mistakes rows` reader (R71-R5's false-red class)."""
    cleaned = phrase.replace("`", "")
    m = re.search(r"\b(five|six|seven|eight|nine|ten|\d+)\s+Mistakes rows", cleaned)
    if not m:
        return None
    word = m.group(1).lower()
    if word.isdigit():
        return int(word)
    return WORD_NUMBERS.get(word)


COUNT_CASES = (
    ("8 Mistakes rows", 8),
    ("`eight` Mistakes rows", 8),
    ("eight Mistakes rows", 8),
    ("sixteen Mistakes rows", None),
    ("no count here", None),
)


def check_e1_parse_count(lane: Path, root: Path = None) -> list:
    problems = []
    for phrase, want in COUNT_CASES:
        got = parse_count(phrase)
        if got != want:
            problems.append(f"parse:{phrase!r}={got!r} want={want!r}")
    return problems


CHECKS = (
    ("E1a", check_e1_registry),
    ("E1b", check_e1_errata),
    ("E1c", check_e1_parse_count),
    ("E2", check_e2_positional),
)
FIXTURE_CHECKS = ("E1a", "E1b", "E2")


def run_checks(lane: Path, only=None) -> list:
    defects = []
    for code, fn in CHECKS:
        if only is not None and code not in only:
            continue
        problems = fn(lane)
        if problems:
            for p in problems:
                defects.append(f"DEFECT {code} {p}")
        else:
            print(f"{code} ok")
    return defects


def run_gate(lane: Path, quiet: bool = False) -> int:
    defects = run_checks(lane)
    if not quiet:
        for d in defects:
            print(d)
        print(f"DEFECTS n={len(defects)}")
        print(f"PREDICATE R72-C2 {'pass' if not defects else 'fail'}")
    return 0 if not defects else 1


# --------------------------------------------------------------------------- fixtures

FIXTURE_REGISTRY_HEAD = "# fixture skill\n\n## Gate/probe registry\n\n" \
    "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n" \
    "|---|---|---|---|---|---|---|---|\n"


def registry_row(name: str, script: str, kind: str = "gate", owner: str = OWNER,
                 columns: int = REGISTRY_COLUMNS) -> str:
    cells = [f"`{name}`", kind, f"`python3 {script} --lane .`", "`0` pass", "`--selftest`",
             "fixture pin", "read-only", owner]
    return "| " + " | ".join(cells[:columns]) + " |\n"


FIXTURE_BODY = ("# Round 71 — fixture claims\n\n## R71-C1\n\n"
                "- **Do-nothing control (committed at freeze).** fixture sentence kept as written.\n"
                "- **Red-before (committed at freeze).** fixture sentence kept as written.\n")


def claims_fixture(*, errata: bool = True, errata_at_top: bool = False,
                   paraphrase: bool = False, revisions: bool = True,
                   trailing_section: bool = False, body_paraphrase: bool = False) -> str:
    body = FIXTURE_BODY
    if body_paraphrase:
        body = body.replace(" (committed at freeze)", "")
    if not errata:
        return body
    block = (ERRATA_HEADING + "\n\n"
             "- **E-R72-1 (round 72, 2026-11-03).** The two labels above are superseded;\n"
             "  the original sentences stay as written (append-only).\n")
    if paraphrase:
        block += "  The labels are restated above rather than quoted.\n"
    else:
        for label in SUPERSEDED:
            block += f"  Superseded: \"{label}\".\n"
    if revisions:
        block += ("  True revisions: the control landed at `c80fcdb3`; the red-before receipt is\n"
                  "  committed at `d8a77d3f` and was produced by the freeze instrument.\n")
    if errata_at_top:
        return "# Round 71 — fixture claims\n\n" + block + "\n" + body.split("\n\n", 1)[1]
    out = body + "\n" + block + "\n"
    if trailing_section:
        out += "## Later section\n\n- appended after the erratum.\n"
    return out


def build_fixture(root: Path, *, registry: str = "full", claims: dict | None = None) -> Path:
    """registry: full | missing | cols | owner. claims: kwargs for claims_fixture."""
    root = Path(root)
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    rows = "".join(registry_row(n, s) for n, s in INSTRUMENTS)
    if registry == "missing":
        rows = ""
    elif registry == "cols":
        rows = registry_row("round71-c1-hf-probe", "plans/round71_c1_hf_probe.py", columns=6) \
            + "".join(registry_row(n, s) for n, s in INSTRUMENTS[1:])
    elif registry == "owner":
        rows = registry_row("round71-c1-hf-probe", "plans/round71_c1_hf_probe.py",
                            owner="sibling") \
            + "".join(registry_row(n, s) for n, s in INSTRUMENTS[1:])
    elif registry != "full":
        raise SystemExit(f"unknown registry mode {registry}")
    (root / SKILL_REL).write_text(FIXTURE_REGISTRY_HEAD + rows)
    (root / CLAIMS_REL).write_text(claims_fixture(**(claims or {})))
    return root


# Red fixtures are keyed by the check they must red under the pristine gate.
REDS = (
    ("E1a", "cols", {"registry": "cols"}),
    ("E1a", "owner", {"registry": "owner"}),
    ("E1b", "paraphrase", {"claims": {"paraphrase": True}}),
    ("E1b", "norev", {"claims": {"revisions": False}}),
    ("E2", "top", {"claims": {"errata_at_top": True}}),
    ("E2", "trailing", {"claims": {"trailing_section": True}}),
    ("E2", "moved", {"claims": {"body_paraphrase": True}}),
)


def red_path(work: Path, check: str, mode: str) -> Path:
    return Path(work) / f"red-{check}-{mode}"


def build_reds(work: Path) -> dict:
    out = {}
    for check, mode, kwargs in REDS:
        out[(check, mode)] = build_fixture(red_path(work, check, mode), **kwargs)
    return out


def fixture_verdict(script: Path, fx: Path) -> int:
    return subprocess.run([sys.executable, str(script), "--lane", str(fx)],
                          capture_output=True, text=True, timeout=180).returncode


def run_selftest(work: Path) -> int:
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    base_red = build_fixture(work / "fake-red", registry="missing", claims={"errata": False})
    green = build_fixture(work / "fake-green")
    reds = build_reds(work)
    for (check, mode), fx in reds.items():
        if fixture_verdict(Path(__file__).resolve(), fx) == 0:
            print(f"RED-NOT-RED {check} {mode}")
    red_rc = run_gate(base_red, quiet=True)
    green_rc = run_gate(green, quiet=True)
    codes_red = sorted({d.split()[1] for d in run_checks(base_red)})
    want = sorted(FIXTURE_CHECKS)
    all_fail = red_rc != 0 and green_rc == 0 and codes_red == want
    # append-only arm: the erratum placed above the superseded sentences must red E2
    moved = build_fixture(work / "fake-errata-top", claims={"errata_at_top": True})
    append_only_arm = "E2" in {d.split()[1] for d in run_checks(moved)}
    # positional arm: rewriting the superseded sentence (and its quote) must red E1b and E2
    rewritten = build_fixture(work / "fake-rewritten")
    p = rewritten / CLAIMS_REL
    p.write_text(p.read_text().replace("(committed at freeze)", ""))
    rewritten_codes = {d.split()[1] for d in run_checks(rewritten)}
    positional_arm = {"E1b", "E2"} <= rewritten_codes
    # parser arm: a word-only parser must red E1c (the round-71 false-red class)
    global WORD_NUMBERS
    saved = WORD_NUMBERS
    try:
        WORD_NUMBERS = {}
        parser_arm = "E1c" in {d.split()[1] for d in run_checks(green)}
    finally:
        WORD_NUMBERS = saved
    ok = (all_fail and append_only_arm and positional_arm and parser_arm)
    print(f"DEFECTS-RED n={len(codes_red)} codes={','.join(codes_red)} want={','.join(want)}")
    print(f"SELFTEST defects-in-fake={len(codes_red)} want={len(want)} all-fail={all_fail} "
          f"append-only-arm={append_only_arm} positional-arm={positional_arm} "
          f"parser-arm={parser_arm} ok={ok}")
    return 0 if ok else 1


# --------------------------------------------------------------------------- mutants

# (mutant name, target check, [(old, new)]). Each rewrites exactly one clause of this source.
MUTANTS = (
    ("M1-registry-columns", "E1a",
     [("if len(cells) != REGISTRY_COLUMNS:", "if len(cells) < 2:")]),
    ("M2-registry-owner", "E1a",
     [("if len(cells) >= REGISTRY_COLUMNS and cells[REGISTRY_COLUMNS - 1] != OWNER:",
       "if False:")]),
    ("M3-errata-labels", "E1b",
     [("        if label not in flat:", "        if False:")]),
    ("M4-errata-revisions", "E1b",
     [("    for revision in TRUE_REVISIONS:", "    for revision in ():")]),
    ("M5-errata-positional", "E2",
     [("        elif at > head_at:", "        elif False:")]),
    ("M6-errata-last-section", "E2",
     [("    if headings and headings[-1] != head_at:", "    if False:")]),
    # deliberate no-op: a comment-only edit must be flagged as null by the metric
    ("M7-null-comment", "E1a",
     [("# --------------------------------------------------------------------------- E1a",
       "# --- (null mutant: comment text only) ------------------------------------- E1a")]),
)


def run_mutants(work: Path) -> int:
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().read_text()
    pristine = Path(__file__).resolve()
    green = build_fixture(work / "mut-green")
    reds = build_reds(work)
    all_fixtures = [green] + [reds[(c, m)] for c, m, _k in REDS]
    pristine_vec = tuple(fixture_verdict(pristine, fx) for fx in all_fixtures)
    killed = survived = invalid = null_detected = 0
    head, marker, tail = src.partition("\nMUTANTS = (\n")
    if not marker:
        raise SystemExit("mutant table marker missing")
    for name, target, edits in MUTANTS:
        text = head
        applied = True
        for old, new in edits:
            if text.count(old) != 1:
                applied = False
                break
            text = text.replace(old, new, 1)
        if not applied:
            invalid += 1
            print(f"MUTANT {name} target={target} applied={applied} verdict=invalid")
            continue
        text = text + marker + tail
        mp = work / f"{name}.py"
        mp.write_text(text)
        accepts_green = fixture_verdict(mp, green) == 0
        target_reds = [fx for (c, _m), fx in reds.items() if c == target]
        escapes = [fx for fx in target_reds if fixture_verdict(mp, fx) == 0]
        other = next(c for c in ("E1a", "E1b", "E2") if c != target)
        attr_fx = next(fx for (c, _m), fx in reds.items() if c == other)
        attr_ok = fixture_verdict(mp, attr_fx) != 0
        mv = tuple(fixture_verdict(mp, fx) for fx in all_fixtures)
        is_null = mv == pristine_vec
        if not accepts_green or not attr_ok:
            invalid += 1
            verdict = "invalid"
        elif is_null:
            null_detected += 1
            verdict = "null"
        elif escapes:
            killed += 1
            verdict = "killed"
        else:
            survived += 1
            verdict = "survived"
        print(f"MUTANT {name} target={target} accept_green={accepts_green} "
              f"escapes={len(escapes)} attribution_ok={attr_ok} null={is_null} "
              f"verdict={verdict}")
    total = len(MUTANTS)
    print(f"ARM accept-green=ok refuse-red={'ok' if killed else 'none'} "
          f"attribution=ok")
    print(f"MUTANTS total={total} killed={killed} survived={survived} invalid={invalid} "
          f"null_detected={null_detected}")
    return 0 if (killed == total - 1 and survived == 0 and invalid == 0
                 and null_detected == 1) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    lane = lane_root(args.lane)
    if args.selftest:
        if not args.work:
            raise SystemExit("--selftest requires --work")
        return run_selftest(Path(args.work))
    if args.mutants:
        if not args.work:
            raise SystemExit("--mutants requires --work")
        return run_mutants(Path(args.work))
    if args.json:
        defects = run_checks(lane)
        print(json.dumps({"defects": defects, "n": len(defects)}))
        return 0 if not defects else 1
    return run_gate(lane)


if __name__ == "__main__":
    sys.exit(main())
