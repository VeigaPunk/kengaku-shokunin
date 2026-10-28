# R50C2ExecAudit — per-pointer adjudication of the 12 unresolved C2 pointers

Seat: `R50C2ExecAudit` (executor), serving **R50-C2 (calibration)**. Lane: `kengaku-shokunin`, round 50, hyaku run 11, w1.
Scope: the one named item only — run `plans/round50_c2_audit.py` at the stage-1 freeze, and adjudicate each of the 12
unresolved pointers (citation site, intended artifact, history proof, proposed resolution). **No lane edits, no commits,
no production-file writes.** The only file this seat wrote in the lane is this report.

REV 3b02d573d58cc6d2e0d27ef92ac0815354912252 (stage-1 freeze; measured revision for every number below unless stated)
LANE_TIP_AT_MEASURE c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 (recorded; only used for the read-only tip cross-check in §2b and §7)

## Axes named

1. **calibration** (served) — does every pointer the self-assessment files carry resolve, and is each correction row the
   *honest* resolution rather than a merely audit-legal one?
2. **evidence integrity** — every resolution in the table is backed by a re-runnable command, not by inference.
3. **instrument correctness** — whether the 12 "unresolved" are 12 real pointer defects or a tokenizer surface defect.

## 1. Freeze gate (run before any measurement)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD && echo "ANCESTOR=yes"
ANCESTOR=yes
$ git log --oneline -1 3b02d57
3b02d57 round-50: C1 four-control receipts and C2 before/selftest receipts (pre-data)
$ sha256sum plans/round50_c2_audit.py
b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef  plans/round50_c2_audit.py
```

The audit digest is byte-identical at the freeze and at the tip
(`git show 3b02d57:plans/round50_c2_audit.py | sha256sum` and `git show c3372a9:…` both →
`b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef`), so the freeze measurement is the same instrument
the tip runs.

Measurement was read-only against a shared clone, never the live checkout:

```
$ export TMPDIR=/fast/scratch/hyaku/kengaku-r50/R50C2ExecAudit
$ cd $TMPDIR && git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane50
$ cd lane50 && git checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252
$ git rev-parse HEAD
3b02d573d58cc6d2e0d27ef92ac0815354912252
$ git rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r50/R50C2ExecAudit/lane50
$ git status --porcelain        # empty
```

## 2. The measurement

### 2a. At the freeze (this seat's revision)

```
$ python3 plans/round50_c2_audit.py --lane .
TIP c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 branch=master
POINTERS total=275 paths=216 hashes=59 resolved=263 exists=204 superseded=0 never-landed=0 unresolved=12
UNRESOLVED corpus/defects.json
UNRESOLVED corpus/evidence/analyze.py
UNRESOLVED corpus/evidence/round9-replication/predictions-r9.sh
UNRESOLVED corpus/knowledge/repo-git-state.md
UNRESOLVED corpus/routed-findings.json
UNRESOLVED plans/round34_c1_verify.py
UNRESOLVED plans/round34_defects.py
UNRESOLVED plans/round34_mutate.py
UNRESOLVED plans/round48_c1_verify.py
UNRESOLVED plans/round48_c2_verify.py
UNRESOLVED plans/round49_c1_verify.py
UNRESOLVED plans/round49_c2_verify.py
EXIT=1
```

Caveat (observed, not inferred): the audit resolves `branch` from `origin/HEAD` → `master` and prints `TIP c3372a9…`
even though the worktree is at the freeze. So in this run the **pointer leg** measured freeze content while the **hash
leg** checked ancestry against the lane tip. No `UNRESOLVED-HASH` line appeared, so the mismatch changed no verdict here;
it is recorded because a hash added later could be judged "ancestor" by a tip measured as if it were the freeze tree.

### 2b. Cross-checks

Recorded "before" receipt, same 12, committed at the freeze
(`.ufo/waves/round-50/claims/c2-before.txt`, sha256 `8412593db1c983ceca04305b343dbeef21cd4e4d87d112e246c867665fd5ee03`):

```
# R50-C2 before (S1 tree f7281bc)
POINTERS total=275 paths=216 hashes=59 resolved=263 exists=204 superseded=0 never-landed=0 unresolved=12
```

Identical numbers and identical 12-pointer set as §2a. The receipt measures S1 tree `f7281bc`, an ancestor of the freeze
(`git merge-base --is-ancestor f7281bc 3b02d57` → yes); the freeze adds only the four control receipts, so the pointer
surface did not move between S1 and the stage-1 freeze.

Read-only tip cross-check (§7): at `c3372a9`, `POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206
superseded=3 never-landed=9 unresolved=0`, exit 0 — the landed correction block works; the table below is about whether
it is the *right* resolution for each pointer, not whether it turns the audit green.

## 3. Per-pointer table (all 12)

`git log --all --oneline -- <pointer>` was run for every pointer in the shared clone (which carries the lane's full
history through `c3372a9`); **every one returned no output** (`# rows=0`), i.e. each of the 12 exact paths never
existed in this lane's history. Citing line numbers are the freeze revision's; the tip's appended correction block
starts at `SCORECARD.md:2145`, so every cited row keeps its number at the tip (verified: `:1168`, `:1169`, `:2104`,
`:2105`, `:2119`, `:2120` unchanged).

| # | pointer | cited at (freeze numbering) | what it was meant to be (verbatim from the citing line) | history proof | proposed resolution |
|---|---|---|---|---|---|
| 1 | `corpus/defects.json` | `SCORECARD.md:563`, `:1180`, `:1420` | the routed-defect ledger, which every one of these three lines actually writes as `corpus/defects.jsonl` (":563 `run … over \`corpus/defects.jsonl\`; freeze receipt \`rows=5 closed=0 observed_pass=0 mismatches=0\``", ":1180 `Ledger row \`R34-D4\` in \`corpus/defects.jsonl\``", ":1420 `can enter \`corpus/defects.jsonl\` with \`recurrence=2\``") | `git log --all --oneline -- corpus/defects.json` → (no output), rows=0; the real file `corpus/defects.jsonl` exists at the freeze and in history (2 commits: `dfcd294`, `11d6453`) | **-> existing target `corpus/defects.jsonl`** (tokenizer truncation, see §4) |
| 2 | `corpus/evidence/analyze.py` | `SCORECARD.md:113` | the *old, wrong* name for the round-9 analyzer, in a path-drift erratum: "the old §Planned named the grader source as `corpus/evidence/analyze.py` — `test -e` → absent; the analyzer on disk is `corpus/evidence/round9-fleet/analyze.py`" | rows=0 for the exact path; `corpus/evidence/round9-fleet/analyze.py` exists at the freeze and in history (1 commit: `2575be6 round-9`, 11058 B) | **-> existing target `corpus/evidence/round9-fleet/analyze.py`** (the citing line names that path itself) |
| 3 | `corpus/evidence/round9-replication/predictions-r9.sh` | `SCORECARD.md:74`, `:97` | the checksum manifest verified with `sha256sum -c`: both lines write "`sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo`" | rows=0; `…/predictions-r9.sha256.repo` exists at the freeze and in history (1 commit: `2575be6`) | **-> existing target `corpus/evidence/round9-replication/predictions-r9.sha256.repo`** (tokenizer truncation of `.sha…` into `.sh`, see §4) |
| 4 | `corpus/knowledge/repo-git-state.md` | `PROVINCE.md:416` | a **sibling repo's** document: "Kasegi's `corpus/knowledge/repo-git-state.md` is cited as the sibling precedent for git-history-state checks … (`R39ConnSibling.md` §5)" — this lane never carried the file | rows=0; no such path in `git ls-files corpus/` | **-> never-landed** (external sibling artifact; the local record of the citation is `.ufo/waves/round-39/build/R39ConnSibling.md`, which exists at the freeze and names `kasegi-shokunin/corpus/knowledge/repo-git-state.md:1-63` at its line 125). A `-> .ufo/waves/round-39/build/R39ConnSibling.md` row would also pass; `never-landed` is the truthful form for the path itself |
| 5 | `corpus/routed-findings.json` | `SCORECARD.md:1572`, `:1650`, `:1721`, `:1804`, `:1841`, `:1915`, `:2084` | the routed-defect ledger; all seven lines write `corpus/routed-findings.jsonl` (e.g. ":1572 `\`corpus/routed-findings.jsonl\` (10 rows: round-39 and round-40 §5)`") | rows=0; `corpus/routed-findings.jsonl` exists at the freeze and in history (6 commits, latest `85a40be`) | **-> existing target `corpus/routed-findings.jsonl`** (tokenizer truncation, see §4) |
| 6 | `plans/round34_c1_verify.py` | `SCORECARD.md:1168` | the r34 C1 counter for the TB2 `protein-assembly` evaluator coverage row: "counter `plans/round34_c1_verify.py --lane .` … before: entry/counter absent at freeze" — never promoted out of the wave | rows=0; body survives only in wave paths, e.g. `.ufo/waves/round-34/final/round34_c1_verify.py` (exists at the freeze) | **-> never-landed** (the frozen command path; the row itself records the tool as absent) |
| 7 | `plans/round34_defects.py` | `SCORECARD.md:1169` | the r34 C2 counter-hardening candidate: "`plans/round34_defects.py`, `plans/round34_mutate.py` … before: both tools absent" | rows=0; body only at `.ufo/waves/round-34/final/round34_defects.py` (exists) | **-> never-landed** |
| 8 | `plans/round34_mutate.py` | `SCORECARD.md:1169` | the 8-mutant harness of the same row ("the 8-mutant harness did not produce `MUTANTS total=8 detected=8`") | rows=0; body only at `.ufo/waves/round-34/final/round34_mutate.py` (exists) | **-> never-landed** |
| 9 | `plans/round48_c1_verify.py` | `SCORECARD.md:2104` | the frozen r48 C1 command: "Frozen command: `python3 plans/round48_c1_verify.py --lane .`; … No committed stage-2 landing-tip run." | rows=0; the counter body is committed only at `.ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py` (docstring: "Round-48 C1 counter (calibration, v3)") | **-> never-landed** (a target row at the wave path would misstate that the frozen `plans/` command exists) |
| 10 | `plans/round48_c2_verify.py` | `SCORECARD.md:2105` | the frozen r48 C2 command: "Frozen command: `python3 plans/round48_c2_verify.py --lane .`; … No full probe run or committed stage-2 landing-tip run." | rows=0; **no body committed anywhere** (`git ls-files \| grep -E 'R48C2.*\.py\|round48_c2'` → only `R48C2ExecMutBattery/{mutants,mutbattery,run_battery}.py`) | **-> never-landed** |
| 11 | `plans/round49_c1_verify.py` | `SCORECARD.md:2119` | the r49 C1 command, whose row already says "frozen command `python3 plans/round49_c1_verify.py --lane .` is not present at landing" | rows=0; candidate body at `.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py` (exists) | **-> never-landed** |
| 12 | `plans/round49_c2_verify.py` | `SCORECARD.md:2120` | the r49 C2 command, same row wording ("is not present at landing") | rows=0; candidate bodies at `.ufo/waves/round-49/w1/R49C2ExecCounter/candidate.py` and `.ufo/waves/round-49/w1/R49C2ExecControls/receipts/instruments/round49_c2_verify.py` (both exist) | **-> never-landed** |

Split of the 12: **3 tokenizer artifacts whose real artifact exists in the same line** (#1, #3, #5), **1 self-documented
path drift whose real target exists** (#2), **1 external sibling path** (#4), **7 never-landed frozen commands** (#6–#12,
each with a surviving wave-dir candidate body except #10).

## 4. Instrument finding: 3 of the 12 are manufactured by the token regex (measured, not inferred)

`plans/round50_c2_audit.py` builds its token regex as
`\.(?:md|py|json|jsonl|txt|patch|whl|sh|json5|tres)` with no trailing boundary. Python alternation is ordered, so:

- `corpus/defects.jsonl` and `corpus/routed-findings.jsonl` tokenize as `…/defects.json` / `…/routed-findings.json`
  (`json` wins over `jsonl`);
- `corpus/evidence/round9-replication/predictions-r9.sha256.repo` tokenizes as `…/predictions-r9.sh` (`sh` matches the
  first two characters of `sha256`).

Probe (scratch-only candidate code, the exact `TOKEN` pattern copied from the frozen audit, run over the three files at
the freeze tree; second pattern orders `jsonl|json5|json|…` and adds `(?![A-Za-z0-9_])` after the extension):

```
OLD paths=216 hashes=59 total=275
NEW paths=215 hashes=59 total=274
ONLY-OLD ['corpus/defects.json', 'corpus/evidence/round9-replication/predictions-r9.sh', 'corpus/routed-findings.json']
ONLY-NEW ['corpus/defects.jsonl', 'corpus/routed-findings.jsonl']
OLD unresolved candidates: 12 (the list in §2a)
NEW unresolved candidates: 9  (analyze.py, repo-git-state.md, 7 × plans/)
```

So a boundary+ordering repair would have made #1 and #5 resolve as the real files and removed #3 entirely (ext `repo`
is not in `EXTS`), leaving 9 genuinely unresolved. **This is a recorded option, not a recommendation to act inside
R50-C2 as frozen:** the audit's token surface is part of the C2 claim's frozen command, and no open-window repair is
listed for `plans/round50_c2_audit.py` in `plans/round-50-claims.md`. If the L1 wants it, the repair must be recorded in
the claims file's repair table (old→new digest) before the scored run, exactly as the C1 counter repair was; the
`SUPERSEDED`-row route the lane already landed needs no instrument change and is the lower-risk path.

## 5. Comparison against the landed correction block (`822f3b7`, at the tip)

Landed rows (`SCORECARD.md:2145-2156`):

```
2145 SUPERSEDED corpus/defects.json -> corpus/defects.jsonl
2146 SUPERSEDED corpus/evidence/analyze.py -> never-landed
2147 SUPERSEDED corpus/evidence/round9-replication/predictions-r9.sh -> corpus/evidence/round9-replication/predictions-r9.md
2148 SUPERSEDED corpus/knowledge/repo-git-state.md -> never-landed
2149 SUPERSEDED corpus/routed-findings.json -> corpus/routed-findings.jsonl
2150-2156 SUPERSEDED plans/round{34,48,49}_*.py -> never-landed
```

Against this table:

- **9 of 12 agree** with §3 as landed (targets exist; every `never-landed` row covers a path with `rows=0` history, so
  none breaks the claim's kill rule "a `never-landed` row for a path that is in history").
- **`:2147` names the wrong artifact.** The audit-legal target `corpus/evidence/round9-replication/predictions-r9.md`
  exists, but the citing lines (`:74`, `:97`) verify `predictions-r9.sha256.repo` with `sha256sum -c`; the predictions
  *document* is a different file. Proposed row: `SUPERSEDED …/predictions-r9.sh -> …/predictions-r9.sha256.repo`.
  Audit effect: none (both exist), so the claim's kill rules are not triggered — this is a correctness/honesty defect in
  the correction, not an audit failure.
- **`:2146` is legal but strictly weaker than available.** `corpus/evidence/round9-fleet/analyze.py` exists and is named
  by the citing line itself; `never-landed` for the truncated name is true but discards the resolvable target. Proposed
  row: `SUPERSEDED corpus/evidence/analyze.py -> corpus/evidence/round9-fleet/analyze.py`.
- **`:2145`, `:2149`** are correct under both readings.
- **`:2148`** is correct: the pointer names a sibling repo's file (`kasegi-shokunin/corpus/knowledge/repo-git-state.md`,
  recorded in the lane at `.ufo/waves/round-39/build/R39ConnSibling.md:125`), never a lane artifact.
- **`:2150-2156`** are correct and match #6–#12, including the note that the wave-dir candidate bodies exist but were
  never the frozen `plans/` commands.

## 6. Secondary findings on the claim text (evidence integrity, for the L1)

1. **"Before" attribution.** `plans/round-50-claims.md` §C2 says Before was "measured at `71f5f5f`, 2026-10-28, receipt
   `.ufo/waves/round-50/claims/c2-before.txt`" with `total=271 paths=213 hashes=58 resolved=259 … unresolved=12`. The
   cited receipt measures **S1 tree `f7281bc`** and prints **275/216/59/263**; `plans/round50_c2_audit.py` does not exist
   at `71f5f5f` (`python3 plans/round50_c2_audit.py --lane .` there → `[Errno 2] No such file or directory`, exit 2), so
   the `71f5f5f` run cannot be re-executed from a plain checkout of that revision. The `271/213/58` triple *is*
   reproducible as a token scan of the three files at `71f5f5f` (probe: `71f5f5f paths=213 hashes=58 total=271`;
   `f7281bc` and `3b02d57` both `216/59/275`), i.e. it is a pre-stage-1 token count, and the resolved/unresolved legs
   were measured with the stage-1 counter on an S1 tree. Proposed correction wording for the claims file: cite
   `f7281bc` for the counter receipt and `71f5f5f` only for the token count.
2. **Arithmetic in the same paragraph.** The C2 Before paragraph says "six pointers name counters … (`plans/round48_c1_verify.py`,
   `plans/round48_c2_verify.py`, `plans/round49_c1_verify.py`, `plans/round49_c2_verify.py`, `plans/round34_c1_verify.py`,
   `plans/round34_defects.py`, `plans/round34_mutate.py`, and four corpus paths)" — seven plans paths plus "four corpus
   paths" is 11, while the measured set is 12: 7 plans + **five** corpus paths (`defects.json`, `analyze.py`,
   `predictions-r9.sh`, `repo-git-state.md`, `routed-findings.json`). The "six" and "four" are both off; the measured
   split in §3 is the authority.

## 7. Limits

- Measured surface is exactly what the frozen audit scans: `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, extension list
  `md|py|json|jsonl|txt|patch|whl|sh|json5|tres`, and 40-hex tokens. Pointers in `LOG.md`, `SKILL.md`, `corpus/**/*.md`
  or the wave reports are outside this claim and were not adjudicated (they were read only to establish #2, #4 and the
  wave-dir candidate bodies).
- Hash leg caveat recorded in §2a (TIP printed from `master`, not the checked-out freeze). No hash verdict changed here.
- `never-landed` verdicts are relative to this lane's object database as cloned (full history of `master`, all refs
  reachable via `--all`); a path that only ever existed on an unreferenced/foreign branch would read as `never-landed`.
- The proposed rows in §5 are *proposals*; this seat wrote no lane file and did not apply them.
- No fixture git tree was created or mutated; no `git` state-changing command was run in the lane or the clone (only
  `checkout` inside the seat's own scratch clone to move between the freeze, `71f5f5f` and the tip for read-only runs).

## 8. Risks handed to the integration owner

- `SCORECARD.md:2147`'s target is the wrong artifact and would survive every kill rule the claim defines (`unresolved=0`,
  target exists). Fix it append-only if the block is still amendable in this window; otherwise record it as a known
  lossy correction.
- If a future round adds a hash that is only an ancestor of the tip and the audit is run from a detached freeze
  checkout, the `master`-derived TIP can green-light it (§2a). Not this round's verdict, but it is a live gap in the
  hash leg's meaning.
- The 3 tokenizer-artifact pointers will keep reappearing in every future run of the same frozen surface; each round then
  needs rows for pointers no author wrote (see §4).

## VERDICT

12 unresolved pointers adjudicated at REV `3b02d57` (`unresolved=12`, exit 1, reproduced verbatim in §2a and identical to
the committed S1 receipt at `f7281bc`). Proposed resolutions: **4 → existing target** (`corpus/defects.jsonl`,
`corpus/evidence/round9-fleet/analyze.py`, `corpus/evidence/round9-replication/predictions-r9.sha256.repo`,
`corpus/routed-findings.jsonl`), **8 → never-landed** (`corpus/knowledge/repo-git-state.md` and the seven
`plans/round{34,48,49}_*` tools), each with `git log --all --oneline -- <path>` = 0 rows. The landed block at the tip is
audit-green (`unresolved=0`, exit 0) but resolves `:2147` to the wrong artifact and `:2146` to a weaker target than the
one on disk; two claims-text defects (§6) are recorded. **No lane edits; scratch tree removed before yield.**

## Appendix A — the two probes, verbatim (replayable; each ran with cwd = the shared clone checked out at `3b02d57`)

`tokprobe.py` — §4 (old vs boundary+ordering-fixed token surface, over the freeze tree):

```python
import re, pathlib
EXTS = ("md","py","json","jsonl","txt","patch","whl","sh","json5","tres")
OLD = re.compile(r"(?<![\w/.-])((?:plans|corpus)/[A-Za-z0-9_][A-Za-z0-9_./+-]*?\.(?:" + "|".join(EXTS) + r"))"
                 r"|(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
NEW = re.compile(r"(?<![\w/.-])((?:plans|corpus)/[A-Za-z0-9_][A-Za-z0-9_./+-]*?\.(?:jsonl|json5|json|patch|tres|txt|whl|md|py|sh))(?![A-Za-z0-9_])"
                 r"|(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
lane = pathlib.Path("lane50")
FILES = ("SCORECARD.md","SHONEN.md","PROVINCE.md")
def scan(rx):
    paths, hashes = set(), set()
    for n in FILES:
        for m in rx.finditer((lane/n).read_text()):
            (paths if m.group(1) else hashes).add(m.group(1) or m.group(0))
    return paths, hashes
op, oh = scan(OLD); np_, nh = scan(NEW)
print(f"OLD paths={len(op)} hashes={len(oh)} total={len(op)+len(oh)}")
print(f"NEW paths={len(np_)} hashes={len(nh)} total={len(np_)+len(nh)}")
print("ONLY-OLD", sorted(op - np_))
print("ONLY-NEW", sorted(np_ - op))
bad = sorted(p for p in op if not (lane/p).exists())
print("OLD unresolved candidates:", bad)
badn = sorted(p for p in np_ if not (lane/p).exists())
print("NEW unresolved candidates:", badn)
```

`tok71.py` — §6 (token counts at the three revisions, content-only via `git show`, no checkout):

```python
import re, subprocess
EXTS=("md","py","json","jsonl","txt","patch","whl","sh","json5","tres")
OLD=re.compile(r"(?<![\w/.-])((?:plans|corpus)/[A-Za-z0-9_][A-Za-z0-9_./+-]*?\.(?:"+"|".join(EXTS)+r"))|(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
for rev in ("71f5f5f77591d8c3d19297ee9785436da45209e4","f7281bc90ca953ff3b84413a21023b9793ef2043","3b02d573d58cc6d2e0d27ef92ac0815354912252"):
    paths,hashes=set(),set()
    for n in ("SCORECARD.md","SHONEN.md","PROVINCE.md"):
        t=subprocess.run(["git","show",f"{rev}:{n}"],capture_output=True,text=True).stdout
        for m in OLD.finditer(t):
            (paths if m.group(1) else hashes).add(m.group(1) or m.group(0))
    print(f"{rev[:8]} paths={len(paths)} hashes={len(hashes)} total={len(paths)+len(hashes)}")
```

Outputs are quoted in §4 and §6. Both probes read only; nothing was written inside the clone.
