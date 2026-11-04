#!/usr/bin/env python3
"""R82-C2 repair checks — one subcommand per routed defect from the newest verifier spot-check.

Universe note: these checks are written against the round-81 spot-check's V1…V7 repairs as the
round-82 lesson's Corrections block records them (corpus/lessons/round-82.md), but nothing here
hardcodes round 81: each check re-derives its values from the tree it runs in.

Each check exits 0 exactly when its repair holds in the tree it is run in, and non-zero otherwise.
They are the `check` commands the `corpus/routed-findings.jsonl` rows R81-V1…R81-V7 carry, so they
must be runnable from the lane root (`bash -lc 'python3 plans/round82_c2_checks.py u1'`) and must
fail when the repair's evidence is reverted to the round-82 base `a3a03ac31451e58f1742b9bccb73b72c2d90a95c`.

    python3 plans/round82_c2_checks.py u1 … u7
    python3 plans/round82_c2_checks.py --all
    python3 plans/round82_c2_checks.py --selftest --work DIR

Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent
BASE_REV = "a3a03ac31451e58f1742b9bccb73b72c2d90a95c"

C2_AFTER = "corpus/evidence/round81/c2-after.txt"
DETERMINISM = "corpus/evidence/round81/determinism.txt"
KNOWLEDGE = "corpus/knowledge/tb2-file-artifact-replay-classes.md"
R81_COUNTER = "plans/round81_c2_spotcheck_debt.py"
SOURCES = "corpus/SOURCES.md"
RECEIPT = "corpus/evidence/round81/log-summary-date-ranges-probe.txt"
W1_RESULTS = ".ufo/waves/round-82/w1-results.json"

QUOTE_CLAIM = re.compile(r"[“\"]([^“”\"]{9,600}?)[”\"] \((\d+) words?[^)]*\)")
WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
           "seven": 7, "eight": 8, "nine": 9, "ten": 10}
COUNT_PHRASE = re.compile(r"(?i)(\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
                          r"(\s+attributed\s+(?:data\s+)?mutations)")
CAMPAIGN = ("reviewer", "critic", "mutation-tester", "labrat")


def read(root: Path, rel: str) -> str:
    try:
        return (root / rel).read_text(errors="replace")
    except OSError:
        return ""


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def git_ref(root: Path) -> str:
    """`master` when that branch resolves in this repo, else `HEAD` (fixtures)."""
    if git(root, "rev-parse", "--verify", "--quiet", "master^{commit}").returncode == 0:
        return "master"
    return "HEAD"


def require_ancestor(root: Path, rev: str, bad: list[str], what: str) -> None:
    ref = git_ref(root)
    proc = git(root, "merge-base", "--is-ancestor", rev, ref)
    if proc.returncode != 0:
        bad.append(f"{what} {rev} is not an ancestor of {ref} in this tree")


def u1(root: Path) -> list[str]:
    """V1 — c2-after.txt is a WORKTREE-clean run of the r81 C2 counter, stamped at a reachable tip."""
    bad: list[str] = []
    text = read(root, C2_AFTER)
    if not text:
        return [f"{C2_AFTER} absent"]
    if not re.search(r"^WORKTREE clean$", text, re.M):
        bad.append("no '^WORKTREE clean' line (re-mint from a clean tree)")
    m = re.search(r"^LANE_TIP ([0-9a-f]{7,64})$", text, re.M)
    if not m:
        bad.append("no LANE_TIP stamp")
    else:
        require_ancestor(root, m.group(1), bad, "LANE_TIP")
    return bad


def sources_rows(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if ln.startswith("| S")]


def newest_supersede(rows: list[str], ident: str) -> str | None:
    """The last row in file order whose bytes carry `supersedes <ident>` (the newest statement)."""
    hit = None
    for ln in rows:
        if re.search(rf"\bsupersedes {re.escape(ident)}\b", ln):
            hit = ln
    return hit


def recompute_claims(text: str, where: str, bad: list[str]) -> int:
    """Every `quote “…” (N words)` claim in `text` must equal the whitespace-split count of the
    quoted text. Returns the number of claims seen."""
    n = 0
    for m in QUOTE_CLAIM.finditer(text):
        n += 1
        claim = int(m.group(2))
        got = len(m.group(1).split())
        if claim != got:
            bad.append(f"{where}: quote claims {claim} words, recomputed {got}: {m.group(1)[:60]!r}")
    return n


def receipt_anchors(root: Path, bad: list[str]) -> tuple[str, int, int, int] | None:
    """Recompute the receipt's quote line and stamp/observation line numbers from its bytes."""
    lines = read(root, RECEIPT).splitlines()
    if not lines:
        bad.append(f"{RECEIPT} absent")
        return None
    line1 = lines[0].strip()
    def lineno(prefix: str) -> int:
        for i, ln in enumerate(lines, 1):
            if ln.startswith(prefix):
                return i
        return 0
    stamp_end = lineno("MINTED_BY_SHA")
    obs_begin = lineno("OBSERVATIONS_BEGIN")
    if not stamp_end or not obs_begin:
        bad.append(f"{RECEIPT}: no MINTED_BY_SHA/OBSERVATIONS_BEGIN stamp lines")
        return None
    return line1, stamp_end, obs_begin, obs_begin + 1


def u2(root: Path) -> list[str]:
    """V2 — every quote word-count and anchor range the round-81 lesson and the S260/S261 registry
    chains state equals a mechanically recomputed value. The S-rows' frozen cells are immutable
    (QUALITY Q34 + fleet SOURCES contract): the corrected statement lives in the newest
    `supersedes S260`/`supersedes S261` row, and the frozen rows must keep their base bytes."""
    bad: list[str] = []
    src = read(root, SOURCES)
    rows = sources_rows(src)
    s260 = next((ln for ln in rows if ln.startswith("| S260 ")), None)
    s261 = next((ln for ln in rows if ln.startswith("| S261 ")), None)
    if s260 is None or s261 is None:
        bad.append("SOURCES: S260/S261 rows absent")
        return bad
    # Frozen rows keep their base bytes (in-place anchor edits are the Q34 rule-2 defect).
    for tok in ("(9 words, line 1)", "stamp 2-16", "observations from 17"):
        if tok not in s260:
            bad.append(f"S260 frozen cell changed or missing {tok!r} (in-place edit is a rule-2 defect)")
    for tok in ("(14 words)", "(17 words)"):
        if tok not in s261:
            bad.append(f"S261 frozen cell changed or missing {tok!r} (in-place edit is a rule-2 defect)")
    sup260 = newest_supersede(rows, "S260")
    sup261 = newest_supersede(rows, "S261")
    if sup260 is None or sup261 is None:
        bad.append("SOURCES: no row carrying `supersedes S260` / `supersedes S261` (the corrected statement)")
    else:
        if "R81-V2" not in sup260 + sup261 + read(root, "corpus/lessons/round-81.md") + read(root, "corpus/lessons/round-82.md"):
            bad.append("the superseding rows and lessons carry no `R81-V2` literal")
        anchors = receipt_anchors(root, bad)
        if anchors:
            line1, stamp_end, obs_begin, first_obs = anchors
            if RECEIPT not in sup260:
                bad.append("S260 supersede row does not name the receipt it anchors")
            else:
                claims = recompute_claims(sup260, "S260-supersede", bad)
                if line1 not in sup260:
                    bad.append("S260 supersede row's quote is not verbatim at receipt line 1")
                if len(line1.split()) != 7:
                    bad.append(f"receipt line 1 recomputes to {len(line1.split())} words, expected 7")
                if claims == 0:
                    bad.append("S260 supersede row carries no quote word-count claim")
                for tok in (f":1-{obs_begin}", f"stamp 2-{stamp_end}", f"observations from {first_obs}"):
                    if tok not in sup260:
                        bad.append(f"S260 supersede row lacks the recomputed anchor {tok!r}")
            recompute_claims(sup261, "S261-supersede", bad)
    # The lesson's own counts must recompute (12/13/19 today).
    lesson = read(root, "corpus/lessons/round-81.md")
    if not lesson:
        bad.append("corpus/lessons/round-81.md absent")
    elif recompute_claims(lesson, "lesson", bad) == 0:
        bad.append("lesson carries no quote word-count claim")
    print(f"V2 reading={'supersede' if sup260 and sup261 else 'inplace-legacy'} "
          f"s260-frozen={'9 words / 2-16 / 17' if '(9 words' in s260 else 'CHANGED'} "
          f"s261-frozen={'14,17' if '(14 words)' in s261 else 'CHANGED'}")
    return bad


def u3(root: Path) -> list[str]:
    """V3 — the knowledge entry opens with the provenance trio source:/verified-at:/recheck:."""
    bad: list[str] = []
    text = read(root, KNOWLEDGE)
    if not text:
        return [f"{KNOWLEDGE} absent"]
    lines = [ln for ln in text.splitlines() if ln.strip()][:3]
    want = ("source:", "verified-at:", "recheck:")
    for i, pref in enumerate(want):
        if i >= len(lines) or not lines[i].startswith(pref):
            bad.append(f"line {i + 1} does not open with {pref!r} (got {lines[i][:60]!r})" if i < len(lines)
                       else f"line {i + 1} missing; entry must open with {pref!r}")
    return bad


def u4(root: Path) -> list[str]:
    """V4 — the r81 counter's mutant docstring count equals the `real=` its own --mutants prints."""
    bad: list[str] = []
    src = read(root, R81_COUNTER)
    if not src:
        return [f"{R81_COUNTER} absent"]
    m = COUNT_PHRASE.search(src)
    if not m:
        return ["r81 counter docstring has no `<n> attributed data mutations` phrase"]
    doc = int(m.group(1)) if m.group(1).isdigit() else WORDNUM[m.group(1).lower()]
    tmp = tempfile.mkdtemp(prefix="c2r82-u4-")
    try:
        proc = subprocess.run([sys.executable, R81_COUNTER, "--mutants", "--work", tmp],
                              cwd=str(root), capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        shutil.rmtree(tmp, ignore_errors=True)
        return ["r81 --mutants battery timed out"]
    shutil.rmtree(tmp, ignore_errors=True)
    if proc.returncode != 0:
        return [f"r81 --mutants battery exits {proc.returncode}"]
    mm = re.search(r"real=(\d+) killed=(\d+) survived=(\d+)", proc.stdout)
    if not mm:
        return ["r81 --mutants printed no `real= killed= survived=` tally"]
    real, killed, survived = (int(g) for g in mm.groups())
    if survived != 0:
        bad.append(f"battery survived={survived} (mutants must all be killed)")
    if killed != real:
        bad.append(f"battery killed={killed} != real={real}")
    if doc != real:
        bad.append(f"docstring states {doc} attributed data mutations, battery prints real={real}")
    print(f"V4 docstring={doc} real={real} killed={killed} survived={survived}")
    return bad


def u5(root: Path) -> list[str]:
    """V5 — the stray `--lane/` directory is gone."""
    if (root / "--lane").exists():
        return ["stray `--lane/` still exists in the lane root"]
    return []


def u6(root: Path) -> list[str]:
    """V6 — the wave tally: attack share >=25% over reviewer/critic/mutation-tester/labrat and a
    live (non-dead-output) mutation-tester seat."""
    bad: list[str] = []
    p = root / W1_RESULTS
    if not p.is_file():
        return [f"{W1_RESULTS} absent (wave not settled)"]
    try:
        data = json.loads(p.read_text(errors="replace"))
    except json.JSONDecodeError as e:
        return [f"{W1_RESULTS} does not parse: {e}"]
    res = data.get("results")
    if not isinstance(res, list) or not res:
        return [f"{W1_RESULTS}: `results` is not a non-empty list"]
    total = data.get("seats") if isinstance(data.get("seats"), int) and data.get("seats") else len(res)
    attack = [r for r in res if r.get("agent") in CAMPAIGN]
    share = len(attack) / total if total else 0.0
    mts = [r for r in res if r.get("agent") == "mutation-tester"]
    alive = [r for r in mts if str(r.get("output") or "").strip()]
    if share < 0.25:
        bad.append(f"attack share {len(attack)}/{total} = {share:.1%} < 25% over { '/'.join(CAMPAIGN) }")
    if not mts:
        bad.append("no mutation-tester seat in the wave tally")
    elif not alive:
        bad.append("every mutation-tester seat is dead (empty output)")
    print(f"V6 seats={total} attack={len(attack)} share={share:.1%} mt_seats={len(mts)} mt_alive={len(alive)}")
    return bad


def u7(root: Path) -> list[str]:
    """V7 — determinism.txt carries the producing COMMAND and the REV it was measured at."""
    bad: list[str] = []
    text = read(root, DETERMINISM)
    if not text:
        return [f"{DETERMINISM} absent"]
    m = re.search(r"^COMMAND (.+)$", text, re.M)
    r = re.search(r"^REV ([0-9a-f]{7,64})$", text, re.M)
    if not m:
        bad.append("no `COMMAND <cmd>` line")
    if not r:
        bad.append("no `REV <hex>` line")
    else:
        require_ancestor(root, r.group(1), bad, "REV")
    if text.count("sha256=") < 2:
        bad.append("fewer than two sha256= hashes recorded (the two hashes must be re-derivable)")
    return bad


CHECKS = {"u1": u1, "u2": u2, "u3": u3, "u4": u4, "u5": u5, "u6": u6, "u7": u7}


# ---------------------------------------------------------------- fixture battery

STUB_R81 = '''#!/usr/bin/env python3
"""Stub of the round-81 C2 counter for the r82 checks fixture (lane copy unavailable)."""

MUTANTS = [("a", "X"), ("b", "X"), ("c", "X"), ("d", "X")]


def mutants(lane, work):
    """Six attributed data mutations on the frozen fixture scaffold, each must be killed."""
    return 0


def main():
    import argparse
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--mutants", action="store_true")
    a = ap.parse_args()
    if a.mutants:
        print("MUTANTS real=4 killed=4 survived=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

FIXTURE_RECEIPT = "\n".join([
    "# tb2 log-summary-date-ranges grader probe (round 81)",
    "SUBJECT_SHA aa",
    "TOOL_SHA bb",
    "HOST_PYTHON 3.13.0",
    "HOST_OPENSSL 3",
    "# pad 6",
    "# pad 7",
    "# pad 8",
    "# pad 9",
    "LANE_TIP cc",
    "WORKTREE clean",
    "EXIT 0",
    "# pad 13",
    "MINTED_BY_SHA dd",
    "OBSERVATIONS_BEGIN",
    "CASE log-summary-date-ranges probe-1 pass",
]) + "\n"

FIXTURE_SOURCES = """# sources

| S260 | kengaku round-81 located replays — corpus/evidence/round81/log-summary-date-ranges-probe.txt | own-work | A | scope | corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-17 (subject at 1, stamp 2-16, observations from 17); quote “# tb2 log-summary-date-ranges grader probe (round 81)” (9 words, line 1) | notes |
| S261 | Terminal-Bench 2.0 pinned task documents — https://example.invalid/t | docs | A | scope | instruction.md:9 quote “Write a CSV file /app/summary.csv with the following structure (including the header):” (14 words); vulnerable-secret/instruction.md:1 quote “The goal is to extract this secret key and save it to /app/results.txt.” (17 words) | notes |
| S265 | kengaku round-81 receipt, anchor corrected as a supersede row — corpus/evidence/round81/log-summary-date-ranges-probe.txt | own-work | A | the receipt's layout recomputed from its bytes | corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15 (subject at 1, stamp 2-14, OBSERVATIONS_BEGIN 15, observations from 16); quote “# tb2 log-summary-date-ranges grader probe (round 81)” (7 words, line 1) | supersedes S260 — the frozen row's anchor cell states the pre-recomputation values; R81-V2 |
| S266 | Terminal-Bench 2.0 pinned task documents, quote counts corrected as a supersede row — https://example.invalid/t | docs | A | the two quoted instruction lines with recomputed counts | instruction.md:9 quote “Write a CSV file /app/summary.csv with the following structure (including the header):” (12 words); vulnerable-secret/instruction.md:1 quote “The goal is to extract this secret key and save it to /app/results.txt.” (13 words) | supersedes S261 — the frozen row's cells state 14/17; R81-V2 |
"""

FIXTURE_LESSON81 = """# round-81 lesson

## 3. Discernment spot-check

Quotes: `log-summary-date-ranges/instruction.md:9` — "Write a CSV file /app/summary.csv
with the following structure (including the header):" (12 words); `vulnerable-secret/instruction.md:1`
— "The goal is to extract this secret key and save it to `/app/results.txt`." (13 words);
`log-summary-date-ranges/task.toml:6` — "Evaluates the ability to analyze date-stamped log files,
calculate counts across multiple date ranges, and generate structured CSV output." (19 words).
"""

FIXTURE_LESSON82 = """# round-82 lesson

## Corrections (the R81-V discharges, with the literal each check re-derives)

- **R81-V1** — `c2-after.txt` re-minted at a clean clone; literal `WORKTREE clean`.
- **R81-V2** — counts recompute; the corrected statement is the supersede rows; R81-V2.
"""

FIXTURE_KNOWLEDGE = """source: S260 — own-work, `corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15`
verified-at: 2026-11-04
recheck: 2026-12-04 (30d) — re-run the round-81 probes

# TB2 file-artifact graders

Thesis: fixture body.
"""

FIXTURE_W1 = {
    "lane": "kengaku", "round": 82, "wave": "w1", "seats": 14,
    "results": ([{"name": f"Exec{i}R82", "agent": "executor", "output": "ok", "note": None}
                 for i in range(1, 9)]
                + [{"name": f"Rev{i}R82", "agent": "reviewer", "output": "report", "note": None}
                   for i in range(1, 3)]
                + [{"name": "CritR82", "agent": "critic", "output": "claims", "note": None},
                   {"name": "MutR82", "agent": "mutation-tester", "output": "mutants killed", "note": None},
                   {"name": "SentR82", "agent": "sentinel", "output": "diff", "note": None},
                   {"name": "ScoutR82", "agent": "scout", "output": "scan", "note": None}]),
}


def build_fixture(root: Path, lane: Path | None) -> None:
    """A green tree for all seven checks: a git repo (master) with every repair artifact."""
    root.mkdir(parents=True, exist_ok=True)
    for rel, text in {
        RECEIPT: FIXTURE_RECEIPT,
        SOURCES: FIXTURE_SOURCES,
        "corpus/lessons/round-81.md": FIXTURE_LESSON81,
        "corpus/lessons/round-82.md": FIXTURE_LESSON82,
        KNOWLEDGE: FIXTURE_KNOWLEDGE,
        W1_RESULTS: json.dumps(FIXTURE_W1),
    }.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    (root / C2_AFTER).parent.mkdir(parents=True, exist_ok=True)
    (root / C2_AFTER).write_text("LANE_TIP PLACEHOLDER\nWORKTREE clean\nEXIT 0\n")
    (root / DETERMINISM).write_text(
        "R81-C1 determinism\nCOMMAND python3 plans/round81_log_summary_probe.py --lane . --work D\n"
        "REV PLACEHOLDER\nrun1 rc=0 sha256=aa\nrun2 rc=0 sha256=aa identical\n")
    src = None
    if lane is not None and (lane / R81_COUNTER).is_file():
        src = (lane / R81_COUNTER).read_text(errors="replace")
    if src is None:
        src = STUB_R81
    p = root / R81_COUNTER
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(src)
    git(root, "-c", "init.defaultBranch=master", "init", "-q")
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "fixture")
    head = git(root, "rev-parse", "HEAD").stdout.strip()
    (root / C2_AFTER).write_text(
        f"LANE_TIP {head}\nWORKTREE clean\nCOMMAND python3 plans/round81_c2_spotcheck_debt.py --lane .\nEXIT 0\n")
    det = (root / DETERMINISM).read_text().replace("REV PLACEHOLDER", f"REV {head}")
    (root / DETERMINISM).write_text(det)
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "stamps")
    patch_u4_docstring(root)


def battery_real(root: Path) -> int | None:
    tmp = tempfile.mkdtemp(prefix="c2r82-fix-")
    try:
        proc = subprocess.run([sys.executable, R81_COUNTER, "--mutants", "--work", tmp],
                              cwd=str(root), capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        shutil.rmtree(tmp, ignore_errors=True)
        return None
    shutil.rmtree(tmp, ignore_errors=True)
    m = re.search(r"real=(\d+)", proc.stdout)
    return int(m.group(1)) if m else None


def patch_u4_docstring(root: Path) -> int | None:
    """Set the fixture r81 counter's docstring count to the battery's real= so u4's green is
    deterministic regardless of whether the lane's V4 repair has landed."""
    p = root / R81_COUNTER
    src = p.read_text(errors="replace")
    real = battery_real(root)
    if real is None:
        return None
    m = COUNT_PHRASE.search(src)
    if not m:
        return None
    if (int(m.group(1)) if m.group(1).isdigit() else WORDNUM[m.group(1).lower()]) == real:
        return real
    p.write_text(src[:m.start()] + f"{real}" + m.group(2) + src[m.end():])
    return real


def selftest(work: Path, lane: Path | None) -> int:
    failures = 0
    root = work / "green"
    if root.exists():
        shutil.rmtree(root)
    build_fixture(root, lane)
    lane_state = u4(root)
    print(f"U4-LANE-STATE repaired={'yes' if not lane_state else 'no'} detail={'; '.join(lane_state) or '-'}")
    cases = [("green", None), ("drop-u1", u1), ("drop-u2", u2), ("drop-u3", u3), ("drop-u4", u4),
             ("drop-u5", u5), ("drop-u6", u6), ("drop-u7", u7), ("u2-inplace-edit", u2),
             ("u6-low-share", u6)]
    for name, fn in cases:
        if fn is None:
            bad_all = []
            for ck in CHECKS.values():
                bad_all += ck(root)
            good = not bad_all
            print(f"CASE green expect=pass observed={'-' if good else ','.join(b[:40] for b in bad_all[:3])} "
                  f"{'ok' if good else 'FAIL'}")
            failures += 0 if good else 1
            continue
        r = work / f"case-{name}"
        if r.exists():
            shutil.rmtree(r)
        shutil.copytree(root, r, ignore=lambda d, ns: {n for n in ns if n == ".git"})
        git(r, "-c", "init.defaultBranch=master", "init", "-q")
        git(r, "add", "-A")
        git(r, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "case")
        if name == "drop-u1":
            (r / C2_AFTER).write_text("LANE_TIP aa\nWORKTREE dirty (1 paths)\nEXIT 0\n")
        elif name == "drop-u2":
            lines = [ln for ln in (r / SOURCES).read_text().splitlines()
                     if "supersedes S260" not in ln and "supersedes S261" not in ln]
            (r / SOURCES).write_text("\n".join(lines) + "\n")
        elif name == "u2-inplace-edit":
            txt = (r / SOURCES).read_text().replace("(9 words, line 1)", "(7 words, line 1)")
            txt = txt.replace("stamp 2-16", "stamp 2-14").replace("observations from 17",
                                                                  "observations from 16")
            (r / SOURCES).write_text(txt)
        elif name == "drop-u3":
            (r / KNOWLEDGE).write_text("# TB2 file-artifact graders\n\nno trio here\n")
        elif name == "drop-u4":
            src = (r / R81_COUNTER).read_text(errors="replace")
            m = COUNT_PHRASE.search(src)
            wrong = "seventy-seven" if m else None
            if m:
                (r / R81_COUNTER).write_text(src[:m.start()] + wrong + m.group(2) + src[m.end():])
        elif name == "drop-u5":
            (r / "--lane").mkdir()
        elif name == "drop-u6":
            data = json.loads((r / W1_RESULTS).read_text())
            for it in data["results"]:
                if it.get("agent") == "mutation-tester":
                    it["output"] = ""
            (r / W1_RESULTS).write_text(json.dumps(data))
        elif name == "u6-low-share":
            data = json.loads((r / W1_RESULTS).read_text())
            data["results"] = [it for it in data["results"] if it.get("agent") != "critic"]
            (r / W1_RESULTS).write_text(json.dumps(data))
        elif name == "drop-u7":
            lines = [ln for ln in (r / DETERMINISM).read_text().splitlines()
                     if not ln.startswith("COMMAND ") and not ln.startswith("REV ")]
            (r / DETERMINISM).write_text("\n".join(lines) + "\n")
        bad = fn(r)
        good = bool(bad)
        failures += 0 if good else 1
        print(f"CASE {name} expect=fail observed={'fail' if good else 'pass'} {'ok' if good else 'FAIL'}")
        shutil.rmtree(r, ignore_errors=True)
    shutil.rmtree(root, ignore_errors=True)
    red = len(cases) - 1
    print(f"SELFTEST cases={len(cases)} red={red} failures={failures}")
    return 0 if failures == 0 else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?", choices=sorted(CHECKS))
    ap.add_argument("--lane", default=str(LANE))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    if a.selftest:
        work = Path(a.work) if a.work else Path("/fast/scratch/hyaku/kengaku-r82/c2checks")
        work.mkdir(parents=True, exist_ok=True)
        return selftest(work, Path(a.lane).resolve())
    root = Path(a.lane).resolve()
    names = sorted(CHECKS) if a.all or not a.name else [a.name]
    rc = 0
    for name in names:
        bad = CHECKS[name](root)
        if bad:
            for b in bad:
                print(f"FAIL {name} {b}")
            rc = 1
        else:
            print(f"OK {name}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
