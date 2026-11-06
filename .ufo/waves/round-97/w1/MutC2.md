# MutC2 — R97-C2 gate-kind census under mutation (round 97)

Scope: R97-C2 counter only — `plans/round97_gate_selftest_census.py` at T, its frozen predicate,
its `--selftest`, and forged commits in private fixture repos. No production edits; the lane was
read-only; scratch `/fast/scratch/hyaku/kengaku-r97/MutC2` removed after receipts were copied.
Base `4992cd0e`, freeze F `8d9d2713`, measured T `f1083da6`. Instrument at T:
`a255e83009bc137c40ba42b02c5c4d000dc6656343417d5e4319bd3395460b7f` (matches the freeze table).
Python 3.14.8, git 2.56.0; no tools installed or upgraded.

## Verdict

- **R97-C2 claim at T: MET.** The frozen predicate reproduces byte-exactly at T, and an independent
  re-derivation from the real bytes confirms the claim's semantics: exactly 44 kind cells change,
  all `gate`→`probe`, the demoted set is *exactly* the 44 names in `.ufo/waves/round-97/L1/c2-base.txt`,
  zero other registry cells change, zero registry scripts change, three rows added, none removed.
- **The counter's detection power: FALSIFIED.** Nine forged commits print the byte-identical frozen
  block (`ROWS base=168 rev=171 …`, `GATES total=84 with_selftest=84 …`, `MISMATCH_TOTAL n=0`,
  `PREDICATE R97-C2 pass`, rc 0) while violating the claim's semantics. One genuine self-test is
  rejected. The gate's own `--selftest` survives 16 of 18 detector/test mutants, including one that
  flips the measured predicate from pass to fail. The counter measures spelling plus aggregate
  counts, not capability or cell identity.

These are coverage findings. Nothing here repairs the frozen instrument; the affected claim is
reported not-met in its *detection* sense and routed to round 98.

## Evidence (all under `.ufo/waves/round-97/w1/MutC2/`)

- `baseline-census.txt` — `python3 plans/round97_gate_selftest_census.py --lane . --rev T` from the
  clone root: the five expected lines, rc 0.
- `baseline-selftest.txt` — `--selftest --work DIR`: `SELFTEST cases=8 failed=0`, rc 0.
- `base-self.txt` — `--rev BASE --base BASE`: `GATES total=127 with_selftest=83 without=44`,
  `MISMATCH_TOTAL n=44`, `PREDICATE R97-C2 fail`, rc 1 — identical to `c2-base.txt`.
- `mutants.json`, `out/*.txt`, `delta/*.diff` — 17 forged-commit mutants: full stdout and the
  minimal T→mutant SKILL.md delta for each.
- `selftest_mutants.json` — 18 mutants of the frozen script run through its own `--selftest`.
- `pattern_probe.json` — each of the six `SPELLING` regexes deleted in turn, with both the
  `--selftest` result and the T-census result.
- `extras.json`, `newrow_and_base.json`, `reversed_live.json` — added/hidden/renamed rows, the
  `--base` override, and the functional reversed-dispatch proof.
- `driver.py`, `selftest_driver.py`, `pattern_probe.py`, `extra_probe.py` — the drivers, so every
  number is re-runnable.

## Method

Isolated `git clone --shared --no-checkout` of the lane, detached at T, under
`/fast/scratch/hyaku/kengaku-r97/MutC2/clone` (toplevel asserted before every fixture git write;
`TMPDIR` explicit). Fixture repos are private: `git init` in a fresh directory, commit 1 = the BASE
tree (`SKILL.md`, `plans/`, `grader.py`, `corpus/evidence/round13-coverage/`), commit 2 = the T tree
plus one mutation. The **unmutated** frozen census is run through its public CLI
(`python3 plans/round97_gate_selftest_census.py --lane FIXTURE --rev REV --base BASE`); every input
is read by the census with `git show REV:<path>`, so the forged commits are the only thing under
test. A mutant is a *survivor* when the printed block equals the frozen predicate's expected block
and rc is 0.

## Baseline (positive control)

At T the frozen predicate reproduces exactly:

```
REV f1083da60e7ff6b88f7420aae7424f7762d14700 BASE 4992cd0e32b8db23ca20310deb7de12d485f8bcc
ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0
GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0
MISMATCH_TOTAL n=0
PREDICATE R97-C2 pass
```

`--selftest` is green on all 8 cases. BASE self-census is red with exactly the 44 documented
mismatches. This is the baseline every mutant below is compared against.

## Independent re-derivation of the claim at T

Computed directly from `git show` blobs, not through the census:

| property | observed | claim |
|---|---|---|
| kind changes, BASE→T | 44, all `gate`→`probe` | 44 |
| demoted set vs `c2-base.txt` | set-equal (44/44) | exactly those 44 |
| registry rows with a non-kind cell change | 0 | no other cell |
| registry scripts changed BASE→T | 0 | no script |
| new rows | 3 (`round97-sparql-probe` probe, `round97-c1-replay` probe, `round97-gate-selftest-census` gate) | 3 |
| removed rows | 0 | 0 |

So the candidate bytes are truthful. The findings below are about the counter, not about T.

## Forged-commit matrix

Seven controls reproduce the documented legs (all red, as the claim's P2 controls say). Ten further
mutants probe the legs' boundaries; nine print the frozen block verbatim.

| mutant | mutation | rc | frozen block | finding |
|---|---|---|---|---|
| `ctl-row-removed` | delete `` `round37-c2` `` | 1 | no | `ROW-REMOVED` |
| `ctl-blanket` | every gate → probe | 1 | no | 83 × `DEMOTED` |
| `ctl-duplicate` | duplicate `` `round37-c2` `` | 1 | no | `ROW-DUPLICATE` |
| `ctl-script-changed` | append `if "--selftest" in sys.argv` to closed `plans/round37_c2_verify.py` | 1 | no | `SCRIPT-CHANGED` + `DEMOTED` |
| `ctl-cell-changed` | rewrite the self-test cell | 1 | no | `CELL-CHANGED` |
| `ctl-prose-only` | new gate row, script with no spelling | 1 | no | `MISMATCH` |
| `mut-heading-dup` | duplicate the registry heading | 2 | no | could-not-evaluate (fail-closed) |
| **`mut-45th-kind`** | `` `grader-perturb` `` probe→gate, `` `round97-gate-selftest-census` `` gate→probe | **0** | **yes** | **survivor** |
| **`mut-gate-to-Gate`** | `` `gate-timing` `` gate→`Gate`, `` `grader-perturb` `` probe→gate | **0** | **yes** | **survivor** |
| **`mut-strip-selftest`** | `` `gate-timing` `` → probe **and** strip its self-test, promote a probe | **0** | **yes** | **survivor** |
| **`mut-launder-comment`** | promote a no-self-test probe; append `# if "--selftest" in sys.argv: pass` | **0** | **yes** | **survivor** |
| **`mut-dead-def`** | promote a probe; append never-called `def run_selftest(): pass` | **0** | **yes** | **survivor** |
| **`mut-add-arg-no-handler`** | promote a probe; append an unread `add_argument("--selftest")` | **0** | **yes** | **survivor** |
| **`mut-dead-compare`** | promote a probe; append `_UNUSED = "--selftest" in "never"` | **0** | **yes** | **survivor** |
| **`mut-hidden-row`** | add `\| hidden-gate \| gate \| …` (no backticked name) | **0** | **yes** | **survivor** |
| **`mut-decoy-entry`** | gate row whose entry cell names the census script | **0** | **yes** | **survivor** |
| `mut-reversed-dispatch` | real dispatch `sys.argv[1:2] == ["--selftest"]` | 1 | no | **false positive** |
| `mut-delete-new-row` | delete `` `round97-gate-selftest-census` `` | 0 | no (`rev=170`, `total=83`) | new rows unpinned |
| `mut-rename-new-row` | rename the same row | 0 | no (`rev=171`, `total=84`) | new rows unpinned |

The nine exact-block survivors are the finding. Each is a forged commit in a private fixture; the
public CLI prints the frozen predicate verbatim and exits 0.

## Self-test mutants

18 mutants of the frozen script, run through its own `--selftest`:

| mutant | result |
|---|---|
| delete the `duplicate` case | `cases=7 failed=0` — **survivor** |
| delete the `script-forged` case | `cases=7 failed=0` — **survivor** |
| delete `add_argument` regex | `cases=8 failed=6` — killed |
| delete `add_parser` regex | `cases=8 failed=0` — **survivor** (and flips T, below) |
| delete quoted `--selftest` + `in/==` regex | `cases=8 failed=1` — killed |
| delete `in/==` + quoted `--selftest` regex | `cases=8 failed=0` — **survivor** |
| delete `def run_selftest` regex | `cases=8 failed=0` — **survivor** |
| delete `in/==` + quoted `selftest` regex | `cases=8 failed=0` — **survivor** |
| add a bare `"--selftest"` regex | `cases=8 failed=0` — **survivor** |
| zero the `ROWS` count line | `cases=8 failed=0` — **survivor** |
| zero the `GATES` count line | `cases=8 failed=0` — **survivor** |
| print `PREDICATE R97-C2 pass` unconditionally | `cases=8 failed=0` — **survivor** |
| `ids == want_ids` → `want_ids <= ids` | `cases=8 failed=0` — **survivor** |
| assert rc only (drop ids) | `cases=8 failed=0` — **survivor** |
| `DEMOTED` only when the script is unchanged | `cases=8 failed=0` — **survivor** |
| `SCRIPT-CHANGED` only while the row stays gate | `cases=8 failed=0` — **survivor** |
| parse every `\|` line, not only `\| \`` | `cases=8 failed=0` — **survivor** |
| `SCRIPT.search` → last match | `cases=8 failed=0` — **survivor** |

The decisive one is `add_parser`. Deleting that single regex leaves the self-test green
(`SELFTEST cases=8 failed=0`, rc 0) while the T census flips to
`GATES total=84 with_selftest=83 without=1` / `MISMATCH round54-c1 plans/round54_c1_anchor.py` /
`PREDICATE R97-C2 fail`. The gate cannot detect a regression that breaks the predicate it is
frozen to measure. Of the six regexes, three are load-bearing at T (`add_argument` 63 gates,
`add_parser` 1 gate, quoted `--selftest` + `in/==` 4 gates) and three are not; the self-test
exercises only two of the three load-bearing ones.

## Findings

**1. HIGH — the frozen predicate does not pin the set of changed kind cells.**
`mut-45th-kind` changes two kind cells (promote `` `grader-perturb` `` probe→gate, demote
`` `round97-gate-selftest-census` `` gate→probe) and the census prints the byte-identical frozen
block. The claim says "re-types exactly those 44 rows … changing no other cell"; 45 kind cells
changed and the round-97 gate row is mistyped `probe`, yet `cells_changed=0` (kind is excluded from
`CELL-CHANGED` by design) and the aggregate `total=84 with_selftest=84` is preserved by the
compensating promotion. Minimal reproduction: two kind cells, no script, no new row.

**2. HIGH — `DEMOTED` recognises only the literal `probe`.**
`mut-gate-to-Gate` retypes `` `gate-timing` `` — a BASE gate *with* a self-test — to `Gate`, and
promotes a probe to keep `total=84`. `DEMOTED` requires `rrow[1] == "probe"`, so the over-correction
the leg exists to catch is evaded by any other non-gate spelling (`Gate`, `gateway`, `—`). The
census reports `demoted_with_selftest=0` and passes.

**3. HIGH — `SCRIPT-CHANGED` and `DEMOTED` cancel each other.**
`mut-strip-selftest` demotes `` `gate-timing` `` to `probe` **and** removes every self-test spelling
from `plans/gate_timing_check.py` (verified: the mutated script matches zero of the six regexes),
then promotes a probe to keep `total=84`. `SCRIPT-CHANGED` requires `not has_selftest(bbody)` — the
base script *had* a spelling, so it is silent. `DEMOTED` requires `has_selftest(rbody)` — the rev
script no longer has one, so it is silent. Result: `scripts_changed=0`, `demoted_with_selftest=0`,
pass. A closed-round instrument is rewritten (Q79 harm) and a legitimate gate is neutered, and the
counter reports nothing.

**4. HIGH — the detector measures spelling, not capability.**
Four exact-block survivors back a `gate` row with something that cannot act as a self-test:
a trailing comment `# if "--selftest" in sys.argv: pass` (regex 3), a never-called
`def run_selftest(): pass` (regex 5), an unread `add_argument("--selftest")` (regex 1), and a dead
constant `_UNUSED = "--selftest" in "never"` (regex 3). The module docstring's claim — "a
self-invocation entry point in the script's code, not a mention in prose" — is false of the
implementation: `has_selftest` is a raw regex over the whole file, comments and strings included.

**5. HIGH — the detector also rejects a real self-test (false positive).**
A genuinely working dispatch `if sys.argv[1:2] == ["--selftest"]: raise SystemExit(0)` (proven:
the mutated probe exits 0 on `--selftest`) matches none of the six regexes and is reported
`MISMATCH`. The reversed comparison `"--selftest" == arg` also matches none: regex 3's trailing
`\b` cannot match after `==`, and regex 4 requires `in`/`==` *before* the quote. The counter is
therefore wrong in both directions — it launders a fake and rejects a real one.

**6. MEDIUM — row parsing and row identity are format-dependent.**
Rows are collected only when the line starts with `` | ` ``. `mut-hidden-row` adds
`| hidden-gate | gate | … |` and the census prints `ROWS base=168 rev=171` and the exact block —
the gate row is invisible. Symmetrically, rows added at REV are never checked: deleting or renaming
`` `round97-gate-selftest-census` `` still returns `PREDICATE R97-C2 pass` (only the claim's literal
`rev=171` / `total=84` catches it). `script_of` also trusts the *first* `.py` token in the entry
cell: `mut-decoy-entry` points a gate row's entry at the census script while the row is the sparql
probe, and the census accepts the decoy's self-test.

**7. MEDIUM — the gate's self-test does not assert the predicate it is frozen under.**
The self-test checks only `rc` and the set of finding ids. Zeroing the `ROWS` line, zeroing the
`GATES` line, or printing `PREDICATE R97-C2 pass` unconditionally all leave
`SELFTEST cases=8 failed=0`. The frozen predicate is a text block; a regression in that text is
invisible to the gate's own self-test (the claim's literal comparison is the only backstop).
Related: the case count is unpinned (deleting a case yields `cases=7 failed=0` while the registry
row still advertises "8 fixture repos"), and the finding-id assertion is not load-bearing
(`ids == want_ids` → `want_ids <= ids`, or rc-only, both pass all 8 cases because no case produces
an extra finding).

## Minimal reproductions

All in private fixture repos; the census is the frozen T script, unmodified.

1. **45th kind cell** — in `SKILL.md`, change `` | `grader-perturb` | probe | `` to `gate` and
   `` | `round97-gate-selftest-census` | gate | `` to `probe`. Commit; run
   `python3 plans/round97_gate_selftest_census.py --lane FIXTURE --rev REV --base BASE`.
   Output: the frozen block, rc 0.
2. **Over-correction evasion** — change `` | `gate-timing` | gate | `` to `Gate` and
   `` | `grader-perturb` | probe | `` to `gate`. Same output.
3. **Script rewrite** — change `` | `gate-timing` | gate | `` to `probe`, promote a probe, and
   replace every `--selftest` / `run_selftest` occurrence in `plans/gate_timing_check.py`. Same
   output, `scripts_changed=0`.
4. **Prose laundering** — promote a probe to `gate` and append
   `# if "--selftest" in sys.argv: pass` to its script. Same output.
5. **False positive** — promote a probe to `gate` and insert
   `if sys.argv[1:2] == ["--selftest"]: raise SystemExit(0)` before `if __name__ == "__main__":`.
   The script exits 0 on `--selftest`; the census prints `MISMATCH` and rc 1.
6. **Self-test blind spot** — delete the line
   `r"add_parser\(\s*[\"']self-?test[\"']",` from `SPELLING`. `--selftest` prints
   `SELFTEST cases=8 failed=0`, rc 0; the T census prints `MISMATCH round54-c1` and
   `PREDICATE R97-C2 fail`, rc 1.

## Verification gaps

- I did not run the C1 replay (`plans/round97_c1_replay.py`); that is the C1 seat's instrument and
  my item is the census. The census's own `--base` default is the only C1 coupling I touched.
- I did not test a `git`-level attack (replace-refs, grafts, `core.fsmonitor`); the fixture repos
  are ordinary. The census's `git show REV:<path>` is the only read path.
- The `--base` override is caller-controlled: `--rev T --base T` prints
  `ROWS base=171 rev=171 … PREDICATE R97-C2 pass` (`extras.json`). The claim's command omits
  `--base`, so this is a hardening note, not a claim defect.
- I did not exercise the `--selftest` fixture cleanup on a read-only `--work` (the `finally` rmtree
  path); out of scope.

## Non-mutation / restoration evidence

- Lane HEAD before and after: `f1083da60e7ff6b88f7420aae7424f7762d14700`; the frozen census is
  still `a255e830…`, the replay `f736b04b…`, `SKILL.md` `739fb58b…`. The lane working-tree
  modifications visible at the end (`LOG.md`, `corpus/QUALITY.md`, `corpus/README.md`, untracked
  `.ufo/waves/round-97/*`) are other seats' writes; this seat wrote only
  `.ufo/waves/round-97/w1/MutC2.md` and `.ufo/waves/round-97/w1/MutC2/`.
- The fixture root was asserted with `rev-parse --show-toplevel` at creation, and every fixture
  git call used `git -C <fixture>`. No lane, fleet or sibling repository was mutated. Scratch removed after the
  receipts above were copied.

Trailer: `.ufo/waves/round-97/w1/MutC2.md`
