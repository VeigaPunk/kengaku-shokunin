# R33FDefectSelftest — selftest strength for N2/N5/N6 present-but-wrong files

Seat: `KengakuR33.R33FDefectSelftest` (leaf; no subagents, single labrat). Date:
2026-10-25. Assignment: *"Selftest strength for N2/N5/N6 present-but-wrong files —
read selftest fixtures in `plans/round33_defects.py` and independently test whether
each red case uses a missing file rather than present incorrect content; report which
mutants can survive the selftest."*

Target: `plans/round33_defects.py` at lane HEAD `77ac8c1` (HEAD drifted during the
wave; script bytes `sha256` `6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6`
— identical to the freeze-tip bytes `7895588` recorded by R33ExecVerifySelf).
Read-only against the lane: `git status --porcelain -- plans/round33_defects.py`
empty before/after; lane sha256 unchanged. All sandbox/mutation work in
`/tmp/r33-R33FDefectSelftest/` (harnesses `harness.py`, `harness2.py`,
`harness3.py`, fixtures, mutants).
Tools: python3 3.14.8, git, coreutils. No installs.

## 1. The selftest's red-case census (direct probe)

Run: `python3 plans/round33_defects.py --selftest` → baseline green:
`SELFTEST checks=14 failed=0`, exit 0. The 14 cases are: registry-complete;
N3-red-unsuperseded; N3-green-superseded; N4-red-missing-tip; N4-green-tip-named;
N1-red-on-empty; N2-red-on-empty; N5-red-on-empty; N6-red-on-empty;
N1-green-tracked; N2-green-section; N5-green-corrected; N6-green-corrected;
N1-red-untracked.

Direct probe of each frozen check on an empty tempdir (what the red cases actually
exercise):

```
N1: RED :: .ufo/waves/round-32 is not readable on disk: find: ... No such file or directory
N2: RED :: SCORECARD.md is unreadable
N3: GREEN :: (no reason)      # check_n3 defaults to absolute fleet path, which is repaired
N4: GREEN :: (no reason)      # check_n4 defaults to absolute fleet path, which is repaired
N5: RED :: corpus/lessons/round-31.md is unreadable
N6: RED :: corpus/lessons/round-30.md is unreadable
```

**Finding A.** For N1/N2/N5/N6 the red cases are *absence-only*: the empty-dir fixture
exercises nothing but the fail-closed `is_file()`/`find` branches
(`"… is unreadable"` / `"is not readable on disk"`). **No present-but-wrong red case
exists for N2, N5, or N6** — a file on disk with wrong content is never presented to
these checks inside the selftest. (N1 has one present-but-wrong red case,
`N1-red-untracked`, and N3/N4's red cases are present-but-wrong **synthetic** fixtures,
`r31.md`/`r32.md` — so N3/N4 are the only checks whose red cases exercise wrong
*content*.)

## 2. Mutation testing (full-file mutants: one check replaced, bytes otherwise identical)

Method: each mutant is a full /tmp copy of `round33_defects.py` whose only diff is one
check function (verified with `difflib`; function-precise splice); the mutant's own
`--selftest` runs as `python3 <mutant> --selftest`, and the mutant's live check then
runs against a /tmp lane holding a present-but-wrong file, where the **original** check
reddens:

| red-fixture | original check on present-but-wrong file |
|---|---|
| N2 | `SCORECARD.md` present, no `## Round 32` heading → RED `"carries no '## Round 32' section"` |
| N5 | lesson-31 present with stale `:35-38`, no `:39-40` correction → RED `"no appended correction updates … :39-40"` |
| N6 | lesson-30 present with stale `:78-81` + `peer-reviewed`, no `:72`/`82-83` → RED `"no appended correction updates … :72 / :82-83"` |

Mutant results (exact runs, all 14 selftest cases counted):

| mutant | selftest | present-but-wrong file |
|---|---|---|
| N2 exists-only (`is_file()` body) | **SURVIVES** (14/14) | **GREEN** — even an *empty* `SCORECARD.md` |
| N2 substring-anywhere (`"Round 32" in text`, no heading anchor) | **SURVIVES** (14/14) | red on this fixture (still demands the token) |
| N2 CONTROL-strictened (heading + disposition token) | KILLED — `N2-green-section` FAIL | — |
| N2 CONTROL-always-red | KILLED — `N2-green-section` FAIL | — |
| N5 stale-only (`:35-38` present, no existence guard, no correction binding) | **SURVIVES** (14/14) | **GREEN** — even a fenced `:35-38` with *no correction at all* |
| N5 no-append-guard (drops stale-token requirement, keeps correction+label) | **SURVIVES** (14/14) | red on this fixture (still requires `:39-40`) |
| N5 no-label (drops labelled-correction requirement) | **SURVIVES** (14/14) | red on this fixture |
| N5 CONTROL-always-green | KILLED — `N5-red-on-empty` FAIL | — |
| N6 stale-only (`:78-81`/`78–81` present, no S086/line-ref checks) | **SURVIVES** (14/14) | **GREEN** |
| N6 no-S086 (drops both S086 peer-review requirements) | **SURVIVES** (14/14) | red on this fixture |
| N6 no-line-refs (drops `:72`/`82-83` entirely) | **SURVIVES** (14/14) | red on this fixture |
| N6 no-label (drops both label requirements) | **SURVIVES** (14/14) | red on this fixture |

(First harness round silently substituted module globals; rebuilt as true source
mutation in `harness2.py`/`harness3.py` — N6 mutants initially failed to import via the
first splice because module-level `CHECKS`/`FROZEN` sit between `check_n6` and
`selftest`; rerun with a line-precise splice. All numbers above are from the corrected
runs.)

## 3. Which mutants can survive the selftest — verdict

The selftest kills only: constant-red, constant-green, and *strengthening* mutants
(every kill above is one of those three). **Every pure-weakening mutant of
N2/N5/N6 survives all 14 cases**, because the red cases never present a file with wrong
content and the green fixtures are the minimal correct repair, which a weakening check
trivially accepts:

- `N2` — surviving: **exists-only** (accepts an *empty* `SCORECARD.md`; silent green on
  present-but-wrong), **substring-anywhere** (accepts `Round 32` in prose or inside a
  code fence).
- `N5` — surviving: **stale-only** (accepts a fenced `:35-38` with no correction at
  all; silent green), **no-append-guard**, **no-label**.
- `N6` — surviving: **stale-only** (silent green on present-but-wrong), **no-S086**,
  **no-line-refs**, **no-label**.

So for N2/N5/N6 the selftest's discriminating power is exactly "file absent vs file
present-and-shaped-like-the-fixture"; the checks' real predicates (heading anchor,
append-only stale-token guards, co-located correction bindings, labels, S086 erratum)
are **never put under tension** by any selftest case. This is the same hole R33CounterAttack
surfaced for live `--lane` runs (E2/E5/E6), and it is structural here: the selftest
inherits the counter's token-presence predicates, and its red cases don't even test
those predicates' negative space. The C2 kill rule ("a partial receipt or a selftest is
not closure") is corroborated: a green selftest certifies nothing about a repair that is
present but wrong.

## 4. Evidence index

- `/tmp/r33-R33FDefectSelftest/orig.py` — byte copy of `plans/round33_defects.py`
  (`sha256` `6ef17abc…`).
- `/tmp/r33-R33FDefectSelftest/harness.py`, `harness2.py`, `harness3.py` — harnesses;
  `harness2.out`, `harness3.out` full transcripts.
- `/tmp/r33-R33FDefectSelftest/mutants/` (N2/N5 files) and `mutants3/` (N6 files) —
  12 mutant full-file copies; each verified diff scope.
- `/tmp/r33-R33FDefectSelftest/lanes{2,3,4}/` — present-but-wrong + empty-file fixtures.

Lane bounds respected: no lane file written except this report; no commit/stage/index
mutation; no subagents; no installs.
