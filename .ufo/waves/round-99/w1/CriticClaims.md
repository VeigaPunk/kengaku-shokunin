# CriticClaims — round 99, R99-C1 / R99-C2 falsification

Seat: CriticClaims (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, round 99.
Measured tip T = `f72a8bc710b12473b5c768004e2581f980d924f4`; BASE `2233a661`; F `24a5a555`.
Method: isolated `git clone --shared` at T under `/fast/scratch/hyaku/kengaku-r99/CriticClaims/`,
grader venv `G` (python 3.13.16, pandas 2.3.2, scipy 1.16.1, pytest 8.4.1, numpy 2.5.4). Both
counters were run at T and both pass as frozen (`c1-at-T.txt`, `c2-at-T.txt`). No production edit,
no commit, no task call. Receipts in `.ufo/waves/round-99/w1/CriticClaims/`.

**Bottom line.** Both frozen predicates pass at T and neither kill rule triggers. But each claim
sentence is broader than its predicate in one load-bearing place: C1's "receipt written by the
official run at F" is only an ancestry check (F1), and C2's "symmetric census / no SOURCES row
changes" is finding-level only, not row-level (F6). Both are fixable defects, not tradeoffs; both
are routed to round 100.

## Verdicts

| id | verdict | one line | evidence |
|---|---|---|---|
| F1 | **falsified clause** (C1) | receipt `LANE_TIP` rewritten to BASE still passes all 11 legs: "written by the official run at F" is not measured | `c1-lanetip-rewritten-to-BASE.txt` |
| F2 | **field is tautological** (C1) | `located=1` is `cap is not None`; the P1 do-nothing control prints `located=1` with no receipt | `c1-at-T.txt`; lane `controls/c1-do-nothing-run1.txt` |
| F3 | **unmeasured by design** (C1) | SKILL `file-artifact` cell 33→34 of 76 and the four `round99-*` rows: "no counter reads SKILL.md" | `byte-tables-at-T.txt`; lane `SKILL.md:74,710-713` |
| F4 | **minor gap** (C1) | capture dir has 9 files; `SHA256SUMS` (a157b6c0…) is unpinned though the gate reads it as a digest source | `byte-tables-at-T.txt`; lane `corpus/evidence/round99/tb2-bn-fit-modify/SHA256SUMS` |
| F5 | **kill rule unmeasured** (C1) | no leg checks the F..C file set; I verified 12 files = 11 candidate + receipt | `byte-tables-at-T.txt` |
| F6 | **falsified clause** (C2) | remove/rewrite an anchor-less outside row, or add a defective row: C2 still passes | `c2-fx-rm.txt`, `c2-fx-edit.txt`, `c2-fx-add.txt`, `c2-fx-note.txt` |
| F7 | **count exact, census incomplete** (C2) | `outside_rows=313` = 325−12 exactly, but 105 of the 313 have no gate note/defect | `c2-census-denominator.txt` |
| F8 | **approximated clause** (C2) | 4th column with a scheme-less URL passes: "three-column / no URL" is checked as "no `://`" | `c2-fx-url.txt` |
| F9 | **unmeasured clause** (C2) | builder is frozen but no leg checks it; it does reproduce the 8 files byte-for-byte | `builder-repro.txt` |
| F10 | **axis name** (C2) | "freshness" (AXES.md = drift detection against live surfaces) is not what a binding claim does | `c2-at-T.txt`; fleet `AXES.md:14` |
| F11 | **disclosure honest, class unfixed** (P2) | partial-run defect is disclosed and the fixed control fails; runners still `set -u` only | `p2-partial-disclosure.txt` |

## F1 — C1: `LANE_TIP` is ancestry-checked, not bound to F

**Counterexample.** In a fixture at T, rewrite the receipt's `LANE_TIP` from F
(`24a5a555…`) to BASE (`2233a661…`), commit, run the C1 counter. All 11 legs pass and the predicate
prints `pass` (`c1-lanetip-rewritten-to-BASE.txt`).

**Why.** `l3 = merge-base --is-ancestor tip rev`; BASE is an ancestor of T. `LANE_TIP` is not in
`RERUN_STAMPS` (`TOOL_SHA`, `CASE_TABLE_SHA`, `GRADER_SIDE`, `BUILDER_SIDE`), and the L6 rerun's
`LANE_TIP` is `absent` (the rerun is a `git archive`, not a repo), so neither leg can catch the edit.
The counter's own docstring is honest ("L3 the receipt's LANE_TIP is an ancestor"); the claim
sentence is stronger ("the probe receipt … written by the official run at F").

**Impacted axes.** coverage (the receipt's provenance); measurement integrity.

**Smallest safe correction.** Require `tip == F`, where F is already available as the single commit
that added `plans/round-99-claims.md` (`frozen_table` computes it). One-line change:
`l3 = bool(tip) and tip == freeze_commit`. The observations themselves are still verified at T by
L6, so this closes the provenance clause without weakening the replay.

## F2 — C1: `located` and `executed` are self-referential

**Counterexample.** The P1 do-nothing control (`controls/c1-do-nothing-run1.txt`) prints
`located=1` with no receipt and no replay. `located` is `1 if cap is not None` (the capture file
exists); `executed` is `1 if ok else 0` (the predicate itself). Neither field carries the claim's
"located" content (the four grading gaps).

**Impacted axes.** coverage (the headline adjective of the claim).

**Smallest safe correction.** Define `located` from the observation block (e.g., C03, C07, C11, C13
observed `P` with their mechanism) or drop the field. Keep `executed` only if it is renamed
`predicate`.

## F3 — C1: the SKILL cell and registry rows are declared unmeasured

The claim says C1 owns "the SKILL `file-artifact` cell (33 → 34 of 76)" and "the four registry rows
`round99-*` (all four ride in the SKILL candidate; no counter reads SKILL.md)". The parenthetical is
accurate: no leg reads SKILL.md. I verified the cell is correct — BASE `SKILL.md:74` says
"executed 33 of 76", T says "executed 34 of 76", and the ledger's file-artifact executed count is
33→34 (`byte-tables-at-T.txt`) — but a stale or wrong cell would not fail any leg.

**Impacted axes.** coverage (the reported number).

**Smallest safe correction.** Add a leg that parses the SKILL `file-artifact` cell and compares it
to the ledger's executed count (and the four registry rows to the four instrument paths).

## F4 — C1: the capture directory is not fully pinned

`corpus/evidence/round99/tb2-bn-fit-modify/` holds 9 files: the 8 pinned captures plus
`SHA256SUMS` (sha256 `a157b6c0ce52fdc0bcdf18aa8c4a55a4e3e86b65f45314e55cf75779b66fd677`). L2 pins
the 8; the manifest is unpinned. The gate reads `SHA256SUMS` as an alternate digest source
(`dir_entries` in `anchor_digest_check.py`), so a tampered manifest could change a binding without
any leg noticing. The manifest currently verifies clean against the 8 files.

**Impacted axes.** coverage / measurement integrity.

**Smallest safe correction.** Add `SHA256SUMS` to `PINS` (and the claim's "eight flat captures"
becomes "eight captures plus their manifest"), or exclude the manifest from the gate's digest source.

## F5 — C1: the kill rule's "C lands exactly" is not measured

The kill rule says "if C lands bytes other than the candidate-bytes table and the receipt". No leg
diffs F..C. I verified manually: `git diff --name-status F T` is exactly 12 files — the 11
candidate-bytes paths plus `corpus/evidence/round99/bnfit-probe.txt` (`byte-tables-at-T.txt`). The
predicate would pass if C landed an extra file.

**Impacted axes.** coverage (the kill rule).

**Smallest safe correction.** Add a leg: `git diff --name-only F rev` equals the candidate-bytes
paths plus the receipt path.

## F6 — C2: K7 is finding-level, not row-level

**Counterexamples** (all fixtures at T, all committed, all run from the fixture root):

1. Delete S001, a BASE row with no gate note and no defect → `PREDICATE R99-C2 pass`,
   `outside_removed=0` (`c2-fx-rm.txt`).
2. Rewrite S001's URL (`aclanthology.org/2026.gem-main.50/` → `example.invalid/…`) → `pass`,
   `rows_changed=0` (`c2-fx-edit.txt`).
3. Append a new SOURCES row S999 with a bogus 64-hex anchor → `pass`, `outside_added=0`,
   `GATE defects base=45 rev=34` (`c2-fx-add.txt`).
4. Boundary: delete S025, a row with a `BIND` note → `K7=fail`, `outside_rebound=1`
   (`c2-fx-note.txt`).

**Why.** `outside = [s for s in base_rows if s not in POP]`; `removed/added` count DEFECT-line
differences and `rebound` counts note differences, per row id present at BASE. A row that disappears
without changing its findings, or a row that appears with a new finding, is invisible. The counter's
docstring is precise ("its DEFECT lines and its verbose notes … are EQUAL"), so the counter is
internally consistent; the claim sentence and the field names are not: "K7 is symmetric (removals
and re-bindings outside the population count, not only additions)" and "no gate byte, SOURCES row,
capture or existing provenance file changes" read at row level.

**Impacted axes.** freshness (the binding's census).

**Smallest safe correction.** Add row presence to K7:
`removed_rows = set(base_rows) - set(rev_rows)` and `added_rows = set(rev_rows) - set(base_rows) - C1_declared`,
require both empty; or rename the fields to `outside_defect_removed` / `outside_defect_added` and
state the finding-level scope in the claim. The removal half is unambiguous and one line.

## F7 — C2: `outside_rows=313` is exact, but 105 of the 313 are unobservable

BASE SOURCES has 325 distinct `ROWID`-matching ids, no duplicates; 325 − 12 POP = 313. The count is
exact. But 105 of the 313 rows have neither a gate note nor a defect at BASE
(`c2-census-denominator.txt` lists them: S001–S024, S026–S035, S037–S046, …). K7 cannot see any
change to those 105 rows (F6), so the census denominator overstates the observable population.

**Impacted axes.** freshness.

**Smallest safe correction.** Report `outside_rows=313 outside_observable=208`, or add the
row-presence leg from F6 (which makes all 313 observable).

## F8 — C2: "three-column / no URL" is checked as "no `://`"

**Counterexample.** Append a 4th column to the S173 line:
`| S173 | \`gitrepository-layout.adoc\` | \`39ce8d…\` | see www.example.com/mirror/gitrepository-layout.adoc |`.
C2 passes, `url_channel_files=0` (`c2-fx-url.txt`). The gate's `prov_url` channel needs a
`URL_RAW`/`URL_BLOB` match (`://`), so a scheme-less URL is inert for the gate; the substantive
"no URL channel" is closed. But the claim's "three-column … no URL" is broader than the check.

**Impacted axes.** freshness (the anti-forgery clause).

**Smallest safe correction.** Require exactly 3 cells per table line (split on `|`), or change the
claim to "no `://`".

## F9 — C2: the builder is frozen but unchecked

`plans/round99_provenance_build.py` is in the frozen-instruments table, but neither counter
references it (`grep` → NOT REFERENCED). I ran it at F (`--lane` = F fixture, `--out` = scratch) and
it reproduces all eight committed `PROVENANCE.md` files byte-for-byte (`builder-repro.txt`). The
claim's "built by `plans/round99_provenance_build.py`" is true but not measured.

**Impacted axes.** freshness.

**Smallest safe correction.** Add the builder's sha to K1 (a third frozen pin), or run the builder
in the counter's work tree and compare its output to the committed files.

## F10 — C2: "freshness" is not the right name for a binding claim

`AXES.md:14` defines freshness as "Drift detection — skill claims re-verified against live surfaces;
stale items flagged or fixed". C2 re-verifies nothing against a live surface (the run is offline) and
the 12 rows are not stale (their sha256 already equals committed bytes). The move is a gate
blind-spot repair: 12 rows the gate could not bind are now bound, and gate findings fall 45→33.

**Steelman.** The bindings make future drift in those 12 captures detectable, so this is a
drift-detection *capability* improvement. But the claim's own text says "row-scoped provenance
bindings", not "re-verification". Round 98 used the same label for the same kind of move
(`round98_c2_nested_bind.py`), so the mislabel is inherited, not new.

**Impacted axes.** freshness (the axis label — the round is judged on coverage and freshness).

**Smallest safe correction.** Rename to "provenance binding (gate blind-spot repair)", or add the
sentence "the gate can now detect drift in 12 previously unmonitored captures".

## F11 — P2 `partial-run*` disclosure: honest about the instance, not the class

The README row is honest: `partial (partial-run*, HARNESS DEFECT) | fail | pass / pass | invalid
control: git rm of an untracked copy failed, fixture equalled positive (lesson M2)`. The receipts
confirm pass/pass with the positive's `GATE rev=33`; the fixed control (`partial-fixed`) fails twice
with `still=1` S306 (`p2-partial-disclosure.txt`). The run1=run2 claim holds: I md5'd the
`LEGS`/`TARGET`/`PREDICATE`/`rc`/`GATE` lines of all 21 controls × 2 runs, 0 mismatches.

Two caveats:

1. Both runners use `set -u` only (no `set -e`/`pipefail`). The partial defect was a silent `git rm`
   failure; the same class of silent mutation failure is still undetectable in any other control.
2. The committed `run_controls.sh` now uses `rm -f` for the `partial` label, so the committed
   `c2-partial-run*.txt` (pass/pass) are not reproducible by the committed runner (it would produce
   the fixed fail/fail). The script comment discloses this; the README does not say the runner was
   edited after the receipts.

**Impacted axes.** freshness (control integrity).

**Smallest safe correction.** `set -euo pipefail` plus a post-mutation assertion
(`git diff --quiet && { echo "no-op mutation"; exit 3; }`), and label the two `c2-partial-run*.txt`
receipts "pre-fix runner" in the README.

## Separability — holds as frozen

- C1 without C2: `c1-positive` passes C1 (`controls/c1-positive-run{1,2}.txt`); `c2-c1only` fails C2
  with `GATE base=45 rev=45` (`c2-c1only-run1.txt`).
- C2 without C1: `c2-positive` passes C2 (`c2-positive-run1.txt`); `c1-c2only` fails C1
  (`c1-c2only-run1.txt`).
- No shared quantity: C1's L10 is `rev_ids − base_ids`; C2's `outside` is `base_rows − POP`. C1's
  eight new rows cannot enter `outside` (BASE-only), and C2 adds no SOURCES rows. The only coupling
  is the gate run on the rev tree, and `c2-c1only` shows C1 adds no finding.

## Could a do-nothing or cheaper control reach either target?

- **C1 do-nothing:** fails 8 legs (`L1 L2 L3 L5 L6 L7 L9 L10`), `PREDICATE fail`, rc 1. It does
  reach `located=1` (F2), but not the predicate.
- **C1 cheaper forgery:** F1 (rewrite `LANE_TIP`) reaches the target. The P2 controls cover the
  intended forgeries (extra member, forged receipt, counter edit) but not header-field edits.
- **C2 do-nothing:** fails K4/K5, `still=12`, rc 1.
- **C2 cheaper forgery:** F6 (remove/rewrite an anchor-less outside row, or add a defective row)
  reaches the target. The P2 controls cover the intended forgeries (URL channel, duplicate line, sha
  column, outside rebind, row edit, gate/capture/counter edit) but not row removal/addition of
  anchor-less rows.

## C1 surface — new member, same method

The surface is the TB2 task `bn-fit-modify` @ `2fd12b88`: the task-tree grader
`tests/test_outputs.py` (nine test functions) and `test.sh`'s reward. It is a new *member* of the
`file-artifact` class — BASE has it `unexecuted`/`unattempted`, and `crack-7z-hash` is the only
extra-member forgery that fails L7 — so this is a genuine coverage move (+1 member, 33→34 of 76,
42→43 of 88), not a re-scoring. It is the 17th instance of the same replay method; the located gaps
(C03 marginal-only, C13 quantile grid, C11/C12 KS band, C07 duplicate edges) are task-specific
grader defects, not a new defect class. The "seventeenth" ordinal is consistent with the
round-86–98 lineage (5th–16th) but is not measured by any leg.

## Unenumerated clauses the counters do not check

| claim | clause | checked by |
|---|---|---|
| C1 | "seventeenth" ordinal | nothing |
| C1 | "@ `2fd12b88`" (capture = upstream commit) | only SOURCES URLs S334–S341; the gate binds the sha, not the URL content; capture dir has no commit stamp |
| C1 | "one offline run at P0, fit equal to the grader's constants" | fixture bytes pinned + C01 passes; the R run and the coefficients are not reproduced |
| C1 | "predicted at P0 … 13/13 held in dry runs 2–3" | L5 checks the scored run only; dry runs are not in evidence |
| C1 | "Sources: S334–S339 admitted (tier A), S340 rejected (A), S341 rejected (B); opened 2026-11-06 10:28 -03" | no leg checks tier, rejected status, or timestamp |
| C1 | "the SKILL `file-artifact` cell (33 → 34 of 76)" and the four `round99-*` rows | no leg reads SKILL.md (declared) |
| C1 | "the receipt … written by the official run at F" | L3 ancestry only (F1) |
| C1 | "C lands exactly these files … plus the receipt" | no leg diffs F..C (F5) |
| C1 | "no file in the frozen-instruments table changes after F" | L2/L4/L8/L11/K1 cover 17 of 18 rows; the builder is unchecked (F9) |
| C1 | receipt fields `MEMBER`, `GRADER_UNPINNED`, `HOST_USERNS`, `SANDBOX`, `LEG_ORDER`, `mismatches` | not in `RERUN_STAMPS` and not separately checked |
| C1 | `SHA256SUMS` in the capture dir | not pinned (F4) |
| C2 | "three-column" | K4 checks one path + one sha, not the cell count (F8) |
| C2 | "no URL" | K3 checks `://` only (F8) |
| C2 | "built by `plans/round99_provenance_build.py`" | no leg (F9) |
| C2 | "no … SOURCES row … changes" | K6 checks POP rows only; 105 anchor-less outside rows are invisible (F6) |
| C2 | "K7 is symmetric (removals …)" | finding-level only; row removals/additions invisible (F6) |
| C2 | "list `.ufo/waves/round-99/L1/c2-pop.txt`" | list's `REV` is P0 (`f9d29eb3`), not BASE; K2 re-derives at BASE and matches, so the label is stale |
| C2 | "C2 is verifiable without C1" / "C1 is verifiable without C2" | control receipts only, not a leg |

## What I could not falsify

- Both predicates pass at T (`c1-at-T.txt`, `c2-at-T.txt`); no frozen file was touched F..T; C's
  parent is F; the F..C diff is exactly the candidate table plus the receipt.
- All 18 frozen-instruments rows and all 11 candidate-bytes rows hash to their table values at T
  (`byte-tables-at-T.txt`).
- The C1 mechanism gaps are correct against the grader's code: C03 passes because only column D is
  read; C13 passes because the KS test is applied to a deterministic quantile grid; C11 (+0.045 sd)
  passes and C12 (+0.050 sd) fails at p ≥ 0.001; C07 passes because the DAG comparison is a set and
  the column check is `all(col in …)`.
- The C2 population is exactly the 12 claimed rows; the builder reproduces the eight files; the
  provenance files are three-column tables with no `://`; K3/K4/K5/K6/K7 fail on the P2 forgeries
  as declared.
- Separability holds in both directions.
- The P2 partial-run disclosure is honest about the instance and the run1=run2 claim holds.
