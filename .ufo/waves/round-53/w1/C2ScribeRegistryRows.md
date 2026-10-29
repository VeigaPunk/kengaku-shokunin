# C2ScribeRegistryRows — round 53, wave 1 (scribe)

Seat: `C2ScribeRegistryRows` (leaf member, no subagent dispatch). Judged on operability and calibration. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, frozen claims `plans/round-53-claims.md` (a34838f), wave-1 spec head 1373b6c.

## What was asked and what was produced

1. Two registry rows for `SKILL.md` *Gate/probe registry*: `round53-c1` (counter `plans/round53_c1_triage.py`) and `round53-c2` (counter `plans/round53_c2_tipstate.py`), 8 columns, no raw pipe in any cell.
2. A header-note paragraph for the top of the registry section.
3. A proposed QUALITY criterion Q43 in Q42's shape, with every result sentence marked `[pending]`.

All three are drafts. `SKILL.md`, `corpus/QUALITY.md` and `plans/round53-tipstate.json` were **not** edited in the lane (the ledger is another seat's deliverable; I wrote no ledger in the lane). Verification was done on a scratch clone and a scratch fixture only.

## Blindness

- I did not open any `C1Label*` directory, any label file, or `plans/round53_c1_classify.py`.
- `.ufo/waves/round-53/w1/` was listed (names only, `C1ExecClassifierAlt` among them); none of those entries were opened.
- `git ls-tree -r --name-only HEAD corpus/evidence/round53` shows only `pin-tree-2fd12b88.json` and `tests-index.json`; no `oracle-labels.json` exists at HEAD, so the C1 counter at HEAD could not reach any label.
- No tuning against any seat's output.

## Reading done (complete reads of both counters)

- `plans/round53_c1_triage.py` (578 lines): docstring, pins, legs 1–4, driver, selftest, main. Five booleans feed the predicate: `ok_pins, ok_fz, ok_or, ok_cf, ok_pa`.
- `plans/round53_c2_tipstate.py` (377 lines): docstring, parsing (`registry_block`, `registry_rows`, `row_script`), `static_legs`, `evaluate`, selftest, main.
- Ten-plus existing rows read in full (`hermetic-grader`, `coverage-census`, `interval-reverdict`, `state-assertion-check`, `grader-perturb`, `gate-timing`, `benchmark-spec-audit`, `registry-reference-check`, `config-projection`, `sources-adopt`, `package-gate`, `round36-c1-battery`, `round46-c1`, `round46-c2`, `round46-c3`, `round50-c1`, `round50-c2`, `round51-routing`, `round51-surfaces`, `round52-c1`, `round52-c2`, `routed-findings`, `tb2-grader-probe`). Shape: 8 cells, `·` as separator, measured values in parentheses, no escaped pipes.
- `corpus/QUALITY.md` lines 1133–1148 (Q42 and file tail).

## Commands run (exact)

Scratch: `S=/fast/scratch/hyaku/kengaku-r53/C2ScribeRegistryRows` (TMPDIR and `--work` under it; removed at exit).

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/clone     # HEAD 1373b6c, rev-parse --show-toplevel asserted
cd $S/clone && python3 plans/round53_c1_triage.py --selftest                      # PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S
cd $S/clone && python3 plans/round53_c2_tipstate.py --selftest
cd $S/clone && python3 plans/round53_c2_tipstate.py --lane . --dry                # base: ROWS registry=75
cd $S/clone && python3 plans/round52_c2_registry.py --lane .                      # base: ADVERTISED 74, PREDICATE R52-C2 pass
git clone -q --shared $S/clone $S/fx             # fixture; SKILL.md edited in the fixture only: two rows + header-note inserted after the tb2-grader-probe row / under the heading
cd $S/fx && python3 plans/round52_c2_registry.py --lane .                         # fixture
cd $S/fx && python3 plans/round53_c2_tipstate.py --lane . --dry                   # fixture
cd $S/fx && python3 plans/round53_c1_triage.py --lane .                           # fixture (no classifier/labels at HEAD): observed exit 1
# partial ledger in fixture (plans/round53-tipstate.json, two rows only, argv = --selftest of each counter):
cd $S/clone && python3 plans/round53_c2_tipstate.py --lane $S/fx --source $S/clone --work $S/work-partial --only round53-c1,round53-c2 --jobs 2
```

Plus one stray command I ran and discarded: `python3 plans/round53_c1_triage.py --lane <scratch clone>` with stdout to `/dev/null` (no lane effect; scratch clone only).

## Measured numbers

- `round53-c1 --selftest` (clean clone 1373b6c): `SELFTEST cases=22 failures=0`, exit 0. Saved: `evidence/c1-selftest.out`.
- `round53-c2 --selftest` (clean clone 1373b6c): `SELFTEST cases=12 failures=0`, exit 0. Saved: `evidence/c2-selftest.out`.
- Base tip static legs (`--dry`, clone at 1373b6c): `ROWS registry=75 ledger=0 missing=75 … PREDICATE` absent (`DRY static legs only`), rc 1. Saved: `evidence/clone-base-round53-c2-dry.out`.
- Base `round52-c2`: `ADVERTISED total=74`, `REGISTERED total=74 rows=76`, all five counts 0, `PREDICATE R52-C2 pass`, exit 0.
- `round53-c1` entry at 1373b6c (observed): `PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184`, `FREEZE absent freeze=False classifier=False labels=False`, `ORACLE not evaluable (pins, classifier, freeze or labels absent)`, `CONFIRM new_confirmed=0`, `PRIOR-ART rows=0`, `PREDICATE R53-C1 fail`, exit 1 — matches the cell's `ORACLE not evaluable` and five-leg description.
- Fixture with the two rows (77 registry rows): `round52-c2`: `ADVERTISED total=76`, `REGISTERED total=76 rows=78`, all five counts 0, `PREDICATE R52-C2 pass`, exit 0. Saved: `evidence/fixture-round52-c2.out`.
- Fixture `round53-c2 --dry`: `ROWS registry=77 ledger=0 missing=77`, `help_limit=7.7`, rc 1 (no ledger). Saved: `evidence/fixture-round53-c2-dry.out`.
- Fixture partial-ledger run (only my two rows declared, `--only`): `ROWS registry=77 ledger=2 missing=75 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0`, `SOURCE rev=1373b6ca… clean=yes`, `RUN executed=2 timeout=0 mismatched=0 evidence_missing=0`, `TIPSTATE declared_green=2 declared_red=0 observed_green=2 observed_red=0`, `PREDICATE R53-C2 fail` (the `--only` run never passes, as the code requires). Saved: `evidence/partial-run.out`.
- Cell parse, using the counters' own functions (`registry_rows`, `row_script`) on the fixture: `round53-c1` and `round53-c2` each 8 cells after an unescaped split, no empty cell, script `plans/round53_c1_triage.py` / `plans/round53_c2_tipstate.py`; registry parsed 77 rows, no duplicates.
- Every 40/64-hex digest in `rows.md` appears verbatim in `plans/round53_c1_triage.py` (4 of 4 found). Each row has 9 raw pipes = 8 cells (delimiters only). No `op://`, token-shaped or key-shaped strings in any drafted file.

## Files produced (absolute)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ScribeRegistryRows/rows.md` — the two rows.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ScribeRegistryRows/header-note.md` — the one-paragraph section header note.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ScribeRegistryRows/q43.md` — proposed Q43 (`[pending]` on every result sentence).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ScribeRegistryRows/evidence/` — `c1-selftest.out`, `c2-selftest.out`, `partial-run.out`, `fixture-round52-c2.out`, `fixture-round53-c2-dry.out`, `clone-base-round53-c2-dry.out`, `fixture-skill-diff-stat.txt`.
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ScribeRegistryRows.md`.

## Decisions in the drafted cells (why they are the way they are)

- **No pipes at all in any cell** (not even escaped). `round52_c2_registry.py` splits each registry line on every pipe and keeps only 8-cell lines, so an escaped-pipe row is silently dropped from its check (its own docstring says so). Avoiding pipes keeps the row visible to both round-52 and round-53 parsers.
- **`registry=77` in the `round53-c2` entry/verdict cells** describes the landing tree (75 existing + these two). That number is forward-looking; it is true only after integration. The fixture confirms the parse count (77), not a ledger.
- **Self-test cells name exactly one script.** `round52_c2` marks a self-test cell unbacked when it names a `--flag` a script lacks; both `--selftest` flags exist in their scripts.
- **The `round53-c1` pinned cell names the classifier `plans/round53_c1_classify.py` without a `python3` prefix**, so the round-52 scanner does not advertise it as a second entry; the entry cell names only the counter.
- **Ledger note for the ledger author (not in the row):** a `round53-c2` ledger entry must not use the counting command itself. Inside a worker clone it would re-run the whole counter nested. `--selftest` (as used in my partial test) is the non-recursive choice.
- **Exit 2 is stated in the `round53-c1` verdict cell:** the docstring documents it, the code never returns it, and the cell says so instead of claiming it.

## Findings (for the L1; none fixed — both counters are frozen)

1. `plans/round53_c1_triage.py`: the docstring's `Exit: 0 predicate holds · 1 predicate fails · 2 setup` is not implemented. A grep for `return 2`/`sys.exit(2)` finds none in this file; `round53_c2_tipstate.py` has two (lines 165, 197). Missing-input faults are reported on a leg line or raise a traceback; both exit 1. (`tool: round53_c1_triage.py docstring says exit 2 for setup, but no code path returns 2`.)
2. `plans/round53_c2_tipstate.py` `evaluate`: `clean` is `None` when `--source` has no `.git`, and the predicate accepts `clean in (True, None)`. A non-git source therefore passes the clean leg silently, although the claim text says `clean=yes` is required. The row cell states this. (Code read; not run against a non-git source.)
3. `plans/round53_c2_tipstate.py`: a `--work` that already contains `w0/src` from an interrupted run aborts with an uncaught `subprocess.CalledProcessError` (`git clone … already exists and is not an empty directory`), exit 1, instead of a `SETUP` line with exit 2. Observed at scratch during this seat's partial-ledger run after a killed run. (`tool: round53_c2_tipstate.py --work with a leftover worker directory raises CalledProcessError and exits 1, not the setup exit 2`.)
4. `plans/round53_c1_triage.py --candidates` (code read, not run): it returns 0 only when pins, classifier, labels and authors are present; otherwise it falls through to the `PREDICATE R53-C1 fail` line. The row cell says "when the oracle inputs are present" for that reason.
5. `round52_c2_registry.py` and the `--dry` ROWS line both confirm the row-existence parse is unchanged by adding two rows (`ADVERTISED 74 → 76`, `REGISTERED 74 → 76`), so the round-52 existence leg is not regressed by this draft.
6. Q43 (`q43.md`) lists the limits in the same paragraph as the criterion; this is a requirement, and whether round 53 meets Q42 (a)–(c) is `[pending]`.

## Out of scope / not done

- The 75-row tip-state ledger `plans/round53-tipstate.json` (a separate deliverable) was not written. My fixture ledger had two rows only and is not part of any lane output.
- No real-tree controls (`c2-control-*`) were produced; those belong to the ledger/control seats.
- The lesson file `corpus/lessons/round-53.md` was not written (Q43 references it as pending).

## Tools

No tools were installed or upgraded by this seat. `~/.omp/agent/RULES.md` was not needed because no install was done; no pacman transaction was attempted.

## Cleanup

The scratch directory `/fast/scratch/hyaku/kengaku-r53/C2ScribeRegistryRows` (clone, fixture, workers) is removed before yield; the evidence copies are kept in the seat directory. Lane state: this seat wrote only inside its own seat directory; it ran no git mutation in the lane and changed no tracked lane file. The partial-ledger run in `evidence/partial-run.out` was repeated on the final row text (the entry argv is unchanged by that edit).
