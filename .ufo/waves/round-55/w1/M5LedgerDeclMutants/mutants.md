# M5LedgerDeclMutants — ledger-declaration binding mutants (round 55, wave 1)

Seat: `M5LedgerDeclMutants` (mutation-tester) · lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
· frozen base tip: `798f5e9ef30ef39291295565209b65a17343c00e` · scratch: `/fast/scratch/hyaku/kengaku-r55/M5LedgerDeclMutants/`

Question under test (round-55 frozen claim R55-C2 surface, `plans/round-55-claims.md`):
**do the ledger's own declarations bind?** The r54 counter `plans/round54_c2_entrytruth.py` re-executes
every `plans/round54-entrytruth.json` row and compares the declared `entry_state`/`entry_exit`/`evidence`
with the observed exit code. If a ledger declaration can be changed without the counter noticing, the
ledger does not bind and R55-C2's after-predicate (`laundered=0 mismatched=0 evidence_missing=0`,
`TIPSTATE declared == observed`) is vacuous.

## Detector (identical in every arm)

```
python3 plans/round54_c2_entrytruth.py --lane <pristine-clone> --source <arm-clone> --work <scratch>/work/<arm> --jobs 8
```

* instrument sha256 `44c3f412852396451b34fa7d0373b0a5901480189cbf77447b3b050d1cc0da97` (unchanged r54 module, base tip)
* ledger path read by the counter: `<--source>/plans/round54-entrytruth.json` (r54 `static_legs()` reads
  `root = source`), so each mutant is a **copy** of the ledger inside its own clone of the base tip
* `--lane` is always the pristine clean clone (`src-pristine`, rev `798f5e9e…`) so `lane_rev_equal=yes` in every arm
* defaults kept everywhere (`--timeout 900`); the run executes all 78 registry rows hermetically
* every arm's tree differs from pristine in exactly one file (the ledger) except the DC control (see below)

## Kill criterion (fixed before the runs)

The **pristine baseline at the frozen base tip is already RED** (`PREDICATE R54-C2 fail`, exit 1) — see the
baseline block below — so the overall predicate cannot be the oracle (a baseline failure is inconclusive).
The kill signal is therefore **differential and per-row**: a mutant is *killed* iff its arm emits a defect
line that names the mutated row and that line is absent from **both** the pristine baseline arm and the
dirty-tree control arm (DC), which uses a semantically inert ledger edit and therefore differs from the
baseline only in `clean=NO`.

## Ledger bytes (sha256 of `plans/round54-entrytruth.json`)

| arm | ledger sha256 | bytes |
|---|---|---|
| pristine (base tip) | `40a77a3baa10f8d96159b136083cc1de3f86c1b6515f318bb6fd6503216de5f7` | 20524 |
| M1 bad_decl | `0808512dc7ebb6b3a808d45e461ee3e19ddde0a132886d8320ecab02ae4a1af3` | 20525 |
| M2 false-red + bogus evidence | `ab1d7aac554abfec5598a5d8517565404182feeb2719dab46342dff9afc86f29` | 20714 |
| M3 row deleted | `ce25f6d0fb1f6d9a9a92398fdaa0a3e26d876070e25abd8f2defa5d08f548b8b` | 20307 |
| M4 duplicate row name | `a5663f842c03eff7d35cf08d18eaff0ed2f3a1e97458efd388cb70a71fd7d7c7` | 20730 |
| DC control (inert `sec` 0.4→0.41) | `2130702ab268fc19e917b21aecaf71a0db03b9c460b3705131aa65d0e992fa87` | 20526 |
| restored (all arms) | `40a77a3baa10f8d96159b136083cc1de3f86c1b6515f318bb6fd6503216de5f7` | 20524 |

## Pristine baseline (clean clone of the frozen base tip) — exit 1

```
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=798f5e9ef30ef39291295565209b65a17343c00e clean=yes lane_rev_equal=yes
  LAUNDERED defect-ledger declared green, entry exit=1
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round36-c1-battery declared green, entry exit=1
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=78 timeout=0 mismatched=0 evidence_missing=1 laundered=3
TIPSTATE entry_declared_green=62 entry_declared_red=16 observed_green=59 observed_red=19
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
EXIT=1
```

**Baseline finding (reported to L1):** at the frozen base tip the r54 ledger already carries **four false
declarations**, measured by the frozen r54 counter itself on a clean clone:
`defect-ledger` (declared green/0, observed exit 1), `round36-c1-battery` (declared green/0, observed exit 1),
`round52-c2` (declared green/0, observed exit 1 — the known r52 registry regression that R55-C1 repairs), and
`round35-c1-coverage` (declared red/1, declared evidence fragment absent from the output).
R55-C2's frozen after-predicate demands `laundered=0`, `evidence_missing=0` and `TIPSTATE declared == observed`,
so every one of these four rows must be re-declared from measured behaviour (or the repair must make them
green) **before** the after-run. The claim's correction list names only `round35-c1-coverage` (evidence
re-derivation) and `round52-c2` (kept green, restored by R55-C1's repair); **`defect-ledger` and
`round36-c1-battery` are not named there and are currently mis-declared at the base tip** — the L1 must
re-measure them at the landing revision and correct them, or the after-predicate fails.

## M1 — flip one green row's `entry_exit` 0→1, state kept `green`

Mutation: row `config-projection` (`entry_argv` = `python3 plans/config_projection.py --summary`, declared
green/exit 0) gets `"entry_exit": 1`; `entry_state` stays `"green"`. Static leg must see `green != exit0`.

```
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=1 duplicate_names=0 bad_table_lines=0 headings=1
  BAD-DECL config-projection
SOURCE rev=798f5e9ef30ef39291295565209b65a17343c00e clean=NO lane_rev_equal=yes
  LAUNDERED defect-ledger declared green, entry exit=1
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round36-c1-battery declared green, entry exit=1
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=77 timeout=0 mismatched=0 evidence_missing=1 laundered=3
TIPSTATE entry_declared_green=61 entry_declared_red=16 observed_green=58 observed_red=19
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
EXIT=1
```

**Verdict: KILLED** — new line `BAD-DECL config-projection` (`bad_decl=1`, absent from baseline and DC).
Secondary observation: the malformed row is **excluded from execution** (`executed=77`, `observed_green`
59→58), i.e. a broken declaration makes the row *unmeasured* rather than *measured-and-wrong*; the
`executed == n_reg` conjunct is what catches the exclusion, so nothing is laundered — but the row's true
state is never established.

## M2 — flip one green row to `red` with a bogus evidence fragment

Mutation: row `grader-perturb` (declared green/exit 0) → `entry_state: "red"`, `entry_exit: 1`,
`evidence: "ZZBOGUS mutant-two fabricated fragment never printed"`, plus a ≥10-word `reason`
(so the declaration is *well formed* and passes the static `bad_decl` leg).

```
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=798f5e9ef30ef39291295565209b65a17343c00e clean=NO lane_rev_equal=yes
  LAUNDERED defect-ledger declared green, entry exit=1
  MISMATCH grader-perturb declared exit=1 observed exit=0 sec=0.8
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round36-c1-battery declared green, entry exit=1
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=78 timeout=0 mismatched=1 evidence_missing=1 laundered=3
TIPSTATE entry_declared_green=61 entry_declared_red=17 observed_green=59 observed_red=19
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
EXIT=1
```

**Verdict: KILLED** — new line `MISMATCH grader-perturb declared exit=1 observed exit=0` (`mismatched=1`).
Direction observed: the false **red** declaration fires **MISMATCH**, never `LAUNDERED` (the r54 code labels
`LAUNDERED` only for *declared green* rows whose observed exit is nonzero; a declared-red row whose entry
truly exits 0 lands in the `mism` branch). Second observation: the bogus **evidence fragment is never
tested** — the exit mismatch short-circuits (`continue`) before the evidence leg, so `evidence_missing`
stays 0 for that row; the evidence string is only exercised when the declared exit matches. The TIPSTATE
line shows the declaration shift (declared green 62→61, declared red 16→17) against unchanged observed
counts (59/19), i.e. the declared/observed disagreement is visible there too.

## M3 — delete one ledger row (which direction fires?)

Mutation: row `catalog-probe` removed from the ledger copy (77 rows left; the SKILL.md registry still has 78 rows).

```
ROWS registry=78 ledger=77 missing=1 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
  MISSING catalog-probe
SOURCE rev=798f5e9ef30ef39291295565209b65a17343c00e clean=NO lane_rev_equal=yes
  LAUNDERED defect-ledger declared green, entry exit=1
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round36-c1-battery declared green, entry exit=1
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=77 timeout=0 mismatched=0 evidence_missing=1 laundered=3
TIPSTATE entry_declared_green=61 entry_declared_red=16 observed_green=58 observed_red=19
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
EXIT=1
```

**Verdict: KILLED** — new line `MISSING catalog-probe`.
**Direction observed: `MISSING` fires, `EXTRA` does not** (`missing=1 extra=0`). The counter's direction is
*registry → ledger*: `missing = set(registry rows) − set(ledger rows)`, `extra = set(ledger rows) − set(registry rows)`.
Deleting a ledger row is therefore reported as a **MISSING** (registry row with no ledger entry); `EXTRA`
can only fire for a ledger row that has no registry row (the opposite mistake). The deleted row is also
skipped in execution (`executed=77`, `observed_green` 59→58).

## M4 — duplicate a row name in the ledger JSON (`object_pairs_hook` `no_dup`)

Mutation: the `config-projection` row block is text-duplicated so the JSON object carries the key twice
(the file stays parseable by a naive `json.loads`, which silently keeps the last occurrence).

```
ROWS registry=78 ledger=0 missing=78 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
  LEDGER ledger unreadable: duplicate JSON key
PREDICATE R54-C2 fail
MISSING_COUNT=78
RUN_LINE_PRESENT=0
EXIT=1
```

**Verdict: KILLED** — `LEDGER ledger unreadable: duplicate JSON key`, exit 1.
Observations: (a) the `no_dup` hook makes the **whole ledger unreadable** (fail-closed), so the counter
reports `ledger=0` and then lists **all 78** registry rows as `MISSING` — the duplicate key does not merely
disturb one row, it destroys the ledger; (b) because the ledger is `None`, the run leg is skipped entirely:
there is **no `SOURCE`, no `RUN`, no `TIPSTATE`, no `MIGRATION` line at all** (nothing is executed);
(c) the counter's own `duplicate_names=N` field counts duplicate **SKILL.md registry** rows, not duplicate
JSON keys — the JSON duplicate is visible only as the `LEDGER …unreadable` line, so a reader scanning the
`duplicate_names=0` field alone would miss it.

## DC — dirty-tree control (semantically inert ledger edit)

Control arm: the ledger copy differs from pristine only in the unused `sec` field of `config-projection`
(`0.4` → `0.41`; the r54 counter never reads `sec`). The tree is dirty exactly like the mutant arms.

```
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=798f5e9ef30ef39291295565209b65a17343c00e clean=NO lane_rev_equal=yes
  LAUNDERED defect-ledger declared green, entry exit=1
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round36-c1-battery declared green, entry exit=1
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=78 timeout=0 mismatched=0 evidence_missing=1 laundered=3
TIPSTATE entry_declared_green=62 entry_declared_red=16 observed_green=59 observed_red=19
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
EXIT=1
```

The control's defect-line set is **identical to the pristine baseline**; the only difference is
`clean=NO` instead of `clean=yes` (the mutated ledger cannot be committed — seats run no mutating git
command — so the source tree is dirty and the `clean` conjunct of the predicate is false in every mutant
arm). The dirty-tree confound therefore contributes **only** the `SOURCE` line's `clean` flag and the
already-red predicate, and no defect line — the per-row differential used as the kill signal is clean.

## Restoration evidence

All five clone trees were restored byte-for-byte from the pristine ledger after the mutant runs:

```
PRISTINE .../wt/plans/round54-entrytruth.json sha256=40a77a3baa10f8d96159b136083cc1de3f86c1b6515f318bb6fd6503216de5f7
src-m1-baddecl:            before=0808512d… after=40a77a3b… restored=True git_status=''
src-m2-red-bogus-evidence: before=ab1d7aac… after=40a77a3b… restored=True git_status=''
src-m3-row-deleted:        before=ce25f6d0… after=40a77a3b… restored=True git_status=''
src-m4-duplicate-name:     before=a5663f84… after=40a77a3b… restored=True git_status=''
src-dc-inert-sec:          before=2130702a… after=40a77a3b… restored=True git_status=''
```

The pristine lane worktree was never written: its ledger sha256 is `40a77a3b…` before and after all runs
and `git status --porcelain` in that worktree is empty.

## Restored-bytes detector arms (same detector, restored trees)

Each restored tree was re-run with the identical detector command. **All four restored arms print the
byte-identical block below** (the restored trees are byte-identical to the pristine ledger, sha256
`40a77a3b…`, `dirty=0`), i.e. every mutant's signal vanishes when the bytes are restored:

```
ARM=R-{M1,M2,M3,M4}-restored  ledger_sha=40a77a3baa10f8d96159b136083cc1de3f86c1b6515f318bb6fd6503216de5f7 dirty=0
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=798f5e9ef30ef39291295565209b65a17343c00e clean=yes lane_rev_equal=yes
  LAUNDERED defect-ledger declared green, entry exit=1
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round36-c1-battery declared green, entry exit=1
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=78 timeout=0 mismatched=0 evidence_missing=1 laundered=3
TIPSTATE entry_declared_green=62 entry_declared_red=16 observed_green=59 observed_red=19
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
EXIT=1
```

Wall-clock per full arm: ~218–240 s (78 rows, `--jobs 8`). The `clean=yes` here (vs `clean=NO` in the
mutant arms) is the visible proof that the restore returned the tree to its pristine, committed state.

## Summary table

| mutant | mutation | expected detector | observed | verdict |
|---|---|---|---|---|
| M1 | green row `entry_exit` 0→1 | `bad_decl` | `BAD-DECL config-projection`, `bad_decl=1`, row dropped from execution (`executed=77`) | KILLED |
| M2 | green row → red, bogus evidence | `MISMATCH`/`LAUNDERED` | `MISMATCH grader-perturb declared exit=1 observed exit=0` (LAUNDERED does **not** fire; evidence leg never reached) | KILLED |
| M3 | ledger row deleted | `missing=N` and/or `EXTRA` | `MISSING catalog-probe`, `missing=1 extra=0` → **MISSING** direction only | KILLED |
| M4 | duplicate JSON key | ledger unreadable | `LEDGER ledger unreadable: duplicate JSON key`, `ledger=0`, 78×`MISSING`, no execution | KILLED |

All four mutants are killed by the frozen r54 counter, but by *different* legs than the seat brief assumed:
`LAUNDERED` never fires for a false-red declaration (it is `MISMATCH`), `EXTRA` never fires for a deleted
ledger row (it is `MISSING`), and the JSON duplicate surfaces as `ledger unreadable` rather than through the
`duplicate_names` field.
