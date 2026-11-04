# C2ReplayR77 — independent freeze replay

Axes: coverage; calibration. Scope: frozen tree only, not the moving landing worktree.

## Revision and method

`git log -1 --format=%H -- plans/round-77-claims.md` (lane cwd), rc 0:
`9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`.

Created an isolated bare clone (rc 0), materialized that exact tree with `git archive | tar -x` (rc 0), and linked its `.git` to the isolated object database. No checkout/reset/commit, production edit, counter import, install, build, lint, formatter, battery run, or child dispatch occurred. Independent Python used subprocess git reads, JSON parsing, section-local regex, ISO-date parsing, line membership counts and hashlib; it did not import either round-77 counter. Git-show rc 128 means missing path, not an empty successful read. Markdown evidence was stripped of fences and HTML comments before leg comparisons.

The clone's branch tip is not used as the measured revision: every independent file read explicitly names the freeze hash. An initial attempt to run the counter directly against the bare clone returned rc 2 (`SETUP corpus/lessons/round-76-verifier-spotcheck.md missing`); the materialized fixture resolves that setup prerequisite.

## Section 6 universe and ledger

Parsed only section `## 6. Routed defects and operator note` of `corpus/lessons/round-76-verifier-spotcheck.md`, stopping at the next level-two heading. Unique ids, in order: **R76-V1, R76-V2, R76-V3, R76-V4, R76-V5, R76-V6, R76-V7**. Count **7**. Parsed every JSON ledger row; matching rows **0** (not seven closed rows).

| Id | Status | close_commit ancestry | verified_at ISO parse | Evidence at close tree |
|---|---|---|---|---|
| R76-V1 | MISSING | not run: no close_commit | not run: no verified_at | not run: no evidence fields |
| R76-V2 | MISSING | not run: no close_commit | not run: no verified_at | not run: no evidence fields |
| R76-V3 | MISSING | not run: no close_commit | not run: no verified_at | not run: no evidence fields |
| R76-V4 | MISSING | not run: no close_commit | not run: no verified_at | not run: no evidence fields |
| R76-V5 | MISSING | not run: no close_commit | not run: no verified_at | not run: no evidence fields |
| R76-V6 | MISSING | not run: no close_commit | not run: no verified_at | not run: no evidence fields |
| R76-V7 | MISSING | not run: no close_commit | not run: no verified_at | not run: no evidence fields |

There is no close_commit, verified_at, evidence_path or evidence_literal for these missing rows. Consequently no per-row ancestry/evidence command can truthfully be run; inventing arguments would not test ledger data. For present rows the independent loop executes `git merge-base --is-ancestor <close_commit> <freeze>` and counts literal-containing lines in `git show <close_commit>:<evidence_path>` output (fixed-string grep-count equivalent), then parses `datetime.date.fromisoformat(verified_at)`.

## Independently re-derived legs

| Leg | Freeze finding | Retained file evidence |
|---|---|---|
| V1 | FAIL: both TOOL_SHA fields absent | Both receipts stamp `c8c116b48fdc1334baf73174ca4f95c86b082590`, ancestor rc 0 each. Tool sha at stamp `37525bcc5105c7f63e4698e52ecad543d5be3706333bbe15d7431273822b3485`; at freeze `552cc63bc8cbc9de13dc1a0284a619d5757d4f8083c26c10e1f5ccaa6e331c9a` (different). Receipt summaries: `SELFTEST cases=12 red=11 failures=0 ok=True`; `MUTANTS total=9 killed=9 expected_matched=9 wrong_id=0 survived=0`. |
| V2 | FAIL: registry rows retain old tallies | C1 `cases=7 red=6`; C2 `cases=10 red=9`, `--mutants 8/8`; not final C1 `cases=12 red=11`/`9/9`, C2 `cases=14 red=13`/`12/12`. Registry rows lack the nine named classes listed below. |
| V3 | FAIL: dated old/new correction line count 0 in all three files | LOG and lesson require `agree=9 disagree=2` plus `agree=8 disagree=3`; SCORECARD requires `wrong=12` plus `wrong=13`. Independent same-line/date intersection counts: LOG 0, lesson 0, SCORECARD 0. Existing unrelated addenda are not these corrections. |
| V4 | FAIL | Visible `Second-reviewer classes` count in LOG = 0. A similarly named lesson block does not repair the LOG pointer. |
| V5 | Semantically OPEN; frozen line-oriented implementation would FAIL | Lesson77 lines 31–32 state proposal 2 (`tb2_grader_admit`, one standing parametrised TB2 / admission counter with a committed filler control) is **open**. Name and status are split across lines. The counter's name-containing line has neither open/unimplemented nor an implementing artifact, so it misses this paragraph. This is not a request to alter the frozen predicate. |
| V6 | FAIL | PROVINCE counts: canonical name 0, `declared-surface-resolver` 1; SCORECARD canonical name 1, old name 0. |
| V7 | PENDING: all three rerun paths absent | `git show <freeze>:corpus/evidence/round77/rerun-{routed-open,r51-c1,r75-c1}.txt` each rc 128. No stamps, tool sha or passing predicates can be derived from missing receipts. |

V2 classes checked against the two registry rows: `NONLOCAL-ANCHOR`, `ESCAPE-ANCHOR`, `OVERFLOW-ANCHOR`, `MALFORMED-DATE`, `DUPLICATE-SURFACE`, `MANIFEST-DRIFT`, `EMPTY-SCOPE`, `LEG-PENDING`, `NEGATED-DISCHARGE`. No passing landing verdict is claimed.

### Exact matching freeze lines

#### SKILL.md

```text
| `round76-c1-surface-resolver` | gate | `python3 plans/round76_c1_surface_resolver.py --lane .` (flags implemented: `--lane --rev --receipt --selftest --mutants --control-declared --work`) | `0` pass (`PREDICATE R76-C1 pass`, `AGREE disagree=0`) · `1` fail (`UNDECLARED-ABSENT`, `STALE-ABSENT`, `STALE-TEXT`, `NOANCHOR`, `MALFORMED`, `TALLY-MISMATCH`) · `2` setup | `python3 plans/round76_c1_surface_resolver.py --selftest --work DIR` (cases=7 red=6) | pinned: every `## Surfaces` row resolved live by its first backticked `~/…` path or localhost endpoint, brace alternatives expanded, `ABSENT YYYY-MM-DD` agreement both directions, 3 s probe timeout | read-only in lane; `--receipt`/`--work` writes | kengaku |
| `round76-c2-defect-discharge` | gate | `python3 plans/round76_c2_defect_discharge.py --lane .` (flags implemented: `--lane --rev --probe --receipt --selftest --selftest-git --mutants --control-status --work`) | `0` pass (`PREDICATE R76-C2 pass`, `discharged=ids`) · `1` fail (`MISSING-ROW`, `OPEN`, `NO-CLOSE-COMMIT`, `CLOSE-NOT-ANCESTOR`, `CLOSE-UNRESOLVED`, `CHECK-TRIVIAL`, `LEG-FAIL`) · `2` setup | `python3 plans/round76_c2_defect_discharge.py --selftest --work DIR` (cases=10 red=9; `--selftest-git` 3/3; `--mutants` 8/8) | pinned: universe = ids in the newest `round-*-verifier-spotcheck.md`; legs D1–D7 re-derive the round-75 stamp, the final-rule 60 = 4/36/20 at `43255758`, the two printed selftests, the two round-74 receipts; S252 three `merge-base --is-ancestor` states; `close_commit` must be an ancestor | read-only in lane; `--receipt`/`--work` writes | kengaku |
```

#### LOG.md

```text
2858:   `LANE_TIP`): c1 before rc 1 (`agree=9 disagree=2`, `STALE-TEXT` row 2, `UNDECLARED-ABSENT` row 4) and
```

#### corpus/lessons/round-76.md

```text
58: - R76-C1 before `SURFACES total=11 present=4 absent=7 prose=0`, `AGREE agree=9 disagree=2`,
```

#### SCORECARD.md

```text
3455: | **R76-C2 / calibration** (held at ceiling 10, exercised) — the newest closure's routed ids must be ledger rows; every close names a `close_commit` that passes S252's three-state ancestry test; legs D1–D7 re-derive their values (round-75 stamp, final-rule `60 = 4/36/20` at `43255758`, both round-75 selftest counts, both round-74 tip receipts) | before (`c2-before.txt`, `--rev fda63968`): `SCOPE ids=7 registered=0 closed=0 open=7 discharged=0 legs_passed=0 legs_pending=2 wrong=12`, seven `LEDGER … MISSING-ROW`, `PREDICATE R76-C2 fail`, rc 1 → after (`c2-after.txt`, stamped `d76db01c`): `SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0`, `PREDICATE R76-C2 pass`, rc 0; the two round-74 gates are green at `6977019b` with committed receipts (`r74-c1-tip.txt`, `r74-c2-tip.txt`) | `python3 plans/round76_c2_defect_discharge.py --lane .` | **admitted on its frozen predicate**; calibration held at **10**, exercised |
3466: `legs_pending=2 wrong=12` (D4/D5 are PENDING at a revision where their inputs do not exist); predicate,
3509: | `province-surface-resolver-table-anchored` | Resolve every declared `PROVINCE.md` `## Surfaces` row live from the table's own bytes (first backticked path or loopback endpoint, brace alternatives expanded), refuse present-tense prose on an absent row, confine probes to loopback and refuse `..`/unbounded braces, and pin the identity manifest so a deleted row is visible — an **increment of round 51's manifest-based resolver** (`plans/round51_surfaces.py`), not a first acquisition | `python3 plans/round76_c1_surface_resolver.py --lane .` → `SURFACES total=11 present=4 absent=7 prose=0`, `AGREE agree=11 disagree=0`, `IDENTITIES n=11 unique=11 sha256=7f41f588…`, exit 0 (`corpus/evidence/round76/c1-after.txt`) | 76 |
3549: `d31feec9`. The C2 before receipt now reads `wrong=13` (7 `MISSING-ROW`, 5 `LEG-FAIL`, 1
```

#### PROVINCE.md

```text
996: capability `declared-surface-resolver`) parses every row, resolves the row's first declared `~/…`
```

#### corpus/lessons/round-77.md

```text
31:   landed as the round-62 class census. Proposal 2 (`tb2_grader_admit`, one standing parametrised TB2
32:   admission counter with a committed filler control) is **open**: `grep -rn 'tb2_grader_admit' plans
```

## Required base replay

Executed from the materialized scratch freeze tree:

```sh
python3 plans/round77_c2_defect_discharge.py --lane . --rev 07c97fcd
```

Exit **1**. Printed:

```text
LANE_TIP 07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59
REV 07c97fcd
WORKTREE clean
TOOL_SHA 7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c
SCOPE ids=7 registered=0 closed=0 open=0 discharged=0 legs_passed=0 legs_pending=2 wrong=12
DEFECTS n=12
PREDICATE R77-C2 fail
```

Thus the specified base `registered=0`, `wrong=12`, rc 1 reproduces. Seven missing ledger ids plus failed V1/V2/V3/V4/V6 account for 12 defects; V5/V7 are pending at base. The bare metadata fixture's `WORKTREE clean` is a counter output, not a separate clean-worktree certification.

The before receipt path itself does not exist in the freeze tree: `git show <freeze>:corpus/evidence/round77/c2-before.txt` rc 128. I confirm the prescribed printed before values by execution, not by claiming to have read a receipt absent from that tree.

## Exact independent read commands and return codes

All below used `git --git-dir=/fast/scratch/hyaku/kengaku-r77/C2ReplayR77/repo.git`; sha values were computed over stdout bytes using hashlib.sha256 (the sha256sum equivalent), never over decoded/re-encoded text.

```text
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/lessons/round-76-verifier-spotcheck.md
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/routed-findings.jsonl
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:SKILL.md
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:LOG.md
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/lessons/round-76.md
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:SCORECARD.md
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:PROVINCE.md
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/lessons/round-77.md
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:plans/round76_c1_surface_resolver.py
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/evidence/round76/c1-selftest.txt
rc=0 git merge-base --is-ancestor c8c116b48fdc1334baf73174ca4f95c86b082590 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
rc=0 git show c8c116b48fdc1334baf73174ca4f95c86b082590:plans/round76_c1_surface_resolver.py
rc=0 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/evidence/round76/c1-mutants.txt
rc=0 git merge-base --is-ancestor c8c116b48fdc1334baf73174ca4f95c86b082590 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
rc=0 git show c8c116b48fdc1334baf73174ca4f95c86b082590:plans/round76_c1_surface_resolver.py
rc=128 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/evidence/round77/rerun-routed-open.txt
rc=128 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/evidence/round77/rerun-r51-c1.txt
rc=128 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/evidence/round77/rerun-r75-c1.txt
rc=128 git show 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb:corpus/evidence/round77/c2-before.txt
```

Specialized grep also checked the cited files in the materialized freeze tree for the ids, registry rows, correction literals, LOG heading, proposal name, capability names, stamps and battery summaries; its returned matches agree with the git-blob replay. A separate live-worktree grep saw in-flight corrections and reminted receipts. Those moving bytes were intentionally not substituted for freeze bytes or used to assert a landing pass.

## Risks, blockers and handoff

No implementation change is authorized for this seat. The frozen revision has zero registered R76 rows, absent rerun receipts and failed correction/registry/name legs. These are measured entering-state findings, not a claim that integration cannot repair them. V5's split-line mismatch is a concrete risk for the frozen counter. Parent must evaluate the landing tree and commit ancestry after integration; this report does not certify any unseen landing state. LSP definition/reference/refactor support is not exposed in this seat's tool inventory and no symbol edit/refactor was attempted.

Only deliverable changed: `.ufo/waves/round-77/w1/C2ReplayR77.md`. No tools installed. Scratch cleanup result is supplied in the terminal seat result (not assumed here).
