# Anatomy of the refused r52 E3 patch

Seat: RV3R52PatchAnatomy (round 55, wave 1). Read-only analysis; no lane file touched.
Lane base: `798f5e9e`. Frozen claims: `plans/round-55-claims.md` (commit `80afa613`).

## 0. Sources read and a naming correction

- The brief's `.ufo/waves/round-52/w2/*R4*/` does not exist (`ls -d` → no match). The patch review is at
  `.ufo/waves/round-54/w1/R4R52Fix/review.md` (verdict **DO-NOT-INTEGRATE**), with `independent-delta.diff`
  and `evidence.json` alongside.
- The patch itself: `.ufo/waves/round-54/w1/E3R52RegistryFix.md`, `E3R52RegistryFix/delta.diff`,
  `E3R52RegistryFix/round52_c2_registry.py`, receipts `old-*.txt` / `patched-*.txt`, `fixture-k5.md`, `fixture-k7.md`, `controls.json`.
- `E8NoharmR53C2.md` exists. It is **not** a no-harm check of the R52 counter: it runs
  `plans/round53_c2_tipstate.py` at `62e9bba5` (ROWS / ARGV / RUN / TIPSTATE lines) and compares it with R53 receipts.
  It never executes `plans/round52_c2_registry.py`, so it provides no no-harm evidence for E3.
- Name collision: `grader.py:1430` `check_r11_ordering` is the R11 preregistration check (bundle sha256 + hash-before-first-request
  over `ordering.log` / `results-r11.jsonl`). `grep -c order_check grader.py` = 0. It is **not** the `order-check` registry
  row. The "order check" that regressed is the registry row `order-check` at `SKILL.md:590`, whose entry is `plans/order_check.py`
  (the Q30 gate). The mechanism below lives entirely in the R52 counter, not in grader.py.

## 1. The patch's claimed fix

`delta.diff` (two hunks, verified by the review's difflib run and by me):

- `selftest_unbacked` (patched lines 68–84): drops the cell-wide early return
  `if re.search(r"\bno\b.{0,24}--[a-z][a-z0-9-]*", cell): return False` (old line 74) and instead computes
  `negated = set(re.findall(r"\bno\b.{0,24}?(--[a-z][a-z0-9-]*)", cell, re.IGNORECASE))` (patched line 75) and
  `flags = sorted(set(FLAG.findall(cell)) - negated)` (line 76). Stated intent: a negation about one flag must not
  disable checking of other flags in the same cell (`E3R52RegistryFix.md` "Bug and repair").
- Selftest: 3 → 6 cases. Adds `span-scoped-negation-fixture` (patched lines ~185–189), `K5-decoy-table`, `K7-entry-missing`
  (lines ~191–211).

Claimed effect: on the current lane the old counter misses `order-check`, the new one catches it. The E3 receipt itself
shows the patched lane run exits 1 with `SELFTEST-UNBACKED 1 \`order-check\`` (`patched-lane.txt`), which the E3 author
recorded as a "red live-lane result to resolve separately".

## 2. The order-check regression mechanism

Row `order-check` (SKILL.md:590). The self-test cell (column 5) is:

> `no \`--selftest\` in the script; falsifiers are external — \`plans/round40_c1_verify.py\` mutants … and the measured controls \`--receipt corpus/evidence/round39/git-leak-probe.txt\` → … ; \`--claims plans/round-99-claims.md\` → …`

Measured with the counter's own regexes (read-only, `PYTHONDONTWRITEBYTECODE`/`dont_write_bytecode`):

| quantity | value |
|---|---|
| scripts found (`plans|corpus|grader …\.py`) | `['plans/round40_c1_verify.py']` (one) |
| flags found (`FLAG`) | `['--claims', '--receipt', '--selftest']` |
| negated flags (patched regex) | `['--selftest']` |
| old blanket negation (old line 74) | **True** |

Mechanism, step by step:

1. **Old code masked the whole cell.** Line 74 of the current counter matches `no \`--selftest\`` (the backtick is
   within the 24-char window). `selftest_unbacked` returns `False` for the cell before any attribution. The row is green
   for the wrong reason: nothing in the cell is checked.
2. **The patch removed the mask but not the attribution.** Patched line 76 subtracts only `--selftest`. The remaining
   `--receipt` and `--claims` are then attributed by line 76's rule (cell-wide: the only script mentioned is
   `plans/round40_c1_verify.py`) to round40. `round40_c1_verify.py` declares only `--lane/--battery-dir/--only/--work/--jobs`
   (`plans/round40_c1_verify.py:443-450`; `grep` finds no `--receipt`/`--claims`). Hence `path.read_text()` lacks both flags →
   `all(f not in body …)` → `True` (patched line 83) → `SELFTEST-UNBACKED \`order-check\``.
3. **The flags belong to a different script.** `--receipt`/`--claims` are the flags of `plans/order_check.py`
   (argparse required args, `plans/order_check.py:143-145`; `grep` finds both, no `--selftest`). The cell names round40 only
   as the source of mutants and then documents *order_check's* controls in prose. The counter has no notion of which
   script a flag belongs to beyond "the one script in the cell". Row prose is not a claim that round40 accepts those flags.
4. The **entry column** (column 3) of the same row names `plans/order_check.py` with those flags; the counter never uses
   column 3 for self-test attribution.

So the regression is an attribution error that the old blanket return happened to hide. Removing the hide exposed it.
The review's independent run (old `SELFTEST-UNBACKED 0`, `PREDICATE pass`; patched `1`, `fail`) reproduces this and
isolates the single changed row (`review.md` P1; `evidence.json` `row-differences`). My own parse over all 79 rows
(`parse_rows`, same regexes) gives the same single difference:
`SELFTEST-UNBACKED` old-vs-patched: `[('\`order-check\`', False, True)]`.

Negative control: the patched negation regex *does* isolate `--selftest` locally (`no --selftest; python3 plans/tool_a.py --check`
→ unbacked True when `tool_a.py` lacks `--check`). The local-negation idea is correct; the defect is only the
cell-level attribution it sits on.

## 3. The K7 masking mechanism

The K7 control is meant to make `ENTRY-MISSING` a load-bearing leg of the verdict. Mechanics:

- Verdict: `ok = not (missing or incomplete or entry_missing or unbacked or duplicate)` (line 133, unchanged by E3).
- The patched K7 case (patched ~lines 199–207) rewrites `SKILL.md` to contain **only** the ghost row
  `plans/ghost_tool.py`, while the fixture tree still contains the advertised `plans/tool_a.py` and `grader.py`.
  Those two advertised scripts have no registry row, so `MISSING` = 2 (`patched-selftest.txt`: `MISSING 2`,
  `MISSING grader.py`, `MISSING plans/tool_a.py`).
- The test asserts `"plans/ghost_tool.py" in entry_missing and verdict(t) == 1` (patched line 206). With `MISSING` = 2 the
  verdict is 1 regardless of `entry_missing`. The assertion checks the leg list, not that the verdict depends on the leg.
- Confirmed by mutation (my scratch run, `ok` without `entry_missing`, patched module): full K7 fixture (advertised scripts
  registered, only ghost absent) → `ENTRY-MISSING 1`, `MISSING 0`, verdict 1 (correct); the mutant returns **rc=0**, so an
  isolated K7 fixture would kill the mutant. The in-tree K7 fixture (ghost-only + advertised scripts) does not kill it:
  the review's run gave `SELFTEST cases=6 failures=0` for the mutant (`review.md` P2; `evidence.json` `K7-verdict-mutant`).
- `controls.json` and `fixture-k7.md` both describe the correct design (ghost inserted into a complete table; mutation
  "ok expression drops entry_missing" → expected `ENTRY-MISSING 1`, exit 1). The implemented selftest code does not follow
  its own control description.
- Also: the patched docstring still says "three fixtures" (minor).

## 4. Why the no-harm check failed and why it was not caught

- `E3R52RegistryFix.md` did not run `--dry` (not implemented by either counter: argparse exit 2 for both, `evidence.json`
  `old-dry`/`patched-dry`). Those are matching usage errors, not a no-harm pass.
- `E8NoharmR53C2.md` checks a different counter (see §0).
- The only no-harm check that would have caught it is the supported default invocation on the lane, which E3 did run
  (`patched-lane.txt`, exit 1), but E3 reported it as "resolve separately" rather than as a regression of a green row.

## 5. Correct-fix sketch (what must differ)

Requirements a correct fix must meet:

1. **Keep every other row's verdict identical** (no-harm on 79 rows): changing attribution must not flip any currently-green row.
2. **Negation stays flag-local** (the patch's `.{0,24}?` capture + `IGNORECASE`). Keep the span-scoped fixture.
3. **Flags must be attributed to the script that accepts them**, not to whichever script the prose mentions. Two naive rules
   were measured in scratch and rejected:
   - *Entry-script only* (check the cell's flags only against column 3): flips `package-gate` green→red (its cell runs
     `plans/round36_c1_verify.py --lane .`; `plans/pkg_gate.py` lacks `--lane`), so the cell's own script must count.
  - *Command-span only* (flags counted only inside `python3 <script> …` spans): drops claims on 8 rows that name a
    script (e.g. `gate-timing` loses `--commit/--lesson`, `db-wal-probe` loses `--dry/--stage-check`,
    `order-check` loses `--receipt/--claims`), so it weakens the leg.
4. **Candidate that passes these** (measured in scratch, `probe5`): a flag is unbacked only if it is absent from **both**
   the cell's sole script **and** the row's entry script (column 3). Results on the lane's 79 rows: zero differences from the
   old counter; `order-check` → backed; negation fixture → True. Cost: a flag absent from the cell script but present in the
   entry script is no longer reported. That is a weakening; zero current rows are affected, but L1 must decide whether that
   is acceptable under the frozen predicate ("registry rows naming a script+flag the script lacks").
5. **K7 must be isolated.** Build the fixture so the advertised scripts are registered (or absent from the advertised set),
   so `ENTRY-MISSING` is the only failing leg. Assert the *leg set* (`{ENTRY-MISSING}`) and that the verdict is 1, and
   check that the verdict depends on `entry_missing` by a mutant the selftest itself runs (drop the term → must go red).
6. **Real no-harm evidence for the R52 counter**: run old and new on the lane and on the landed tip; require identical
   `PREDICATE` per row, not just one green lane. Record exit codes. Do not count matching argparse errors.
7. **Governance**: `plans/round-55-claims.md:150-151` says the production r52 counter stays unchanged this round and the
   defect is "reconstructed as evidence (R11/RV3)". Any landed fix is therefore a new counter or a claims amendment decided by L1,
   not a silent edit of `plans/round52_c2_registry.py`.

## 6. Verification of this analysis

Commands run (all read-only with respect to the lane; scratch removed):

- `ls -d .ufo/waves/round-52/w2/*R4*` → no match (dead end; brief's path wrong).
- `grep -n check_r11_ordering grader.py` → line 1430 (R11 check; not the order-check row).
- `cat` / `sed` of E3, E8, R4R52Fix, plans/round52_c2_registry.py, plans/order_check.py, plans/round40_c1_verify.py (exit 0).
- `python3 -B` probes in `/fast/scratch/hyaku/kengaku-r55/RV3R52PatchAnatomy/` (exit 0 for the reported runs; one candidate
  harness failed on a path bug in my own script (exit 1), rewritten; not a lane result).
- The mutant K7 run and the candidate attribution runs above (exit 0).

Confidence: high on the regression mechanism and K7 mask (matches review P1/P2 and reproduced); medium on the candidate fix
(only 79 rows, no frozen-predicate reading by L1). No tools installed; no pacman/uv/npm; no git mutation.
