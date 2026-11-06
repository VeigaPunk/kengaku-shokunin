# MutC1 — mutation test of the R98-C1 counter (round 98)

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` · seat `MutC1` · 2026-11-06
Measured `T 8e37fc65d5649bb37166fdd6b1657445a8cb55b9` · `BASE 49a1c4f1` · freeze `F e1a3afd9`
Frozen counter under test: `plans/round98_c1_replay.py` sha256 `e361383249d9bdf5c9fffb83c6df5dbd286007c951a70e68dd3e21201b4f2b2a` (the
frozen-instruments value). No lane file was edited; every write is under
`.ufo/waves/round-98/w1/MutC1/` or the private scratch.

## Method

* One `git clone --shared` checkout of the lane detached at `T` under
  `/fast/scratch/hyaku/kengaku-r98/MutC1/clone`; one fixture clone per mutant, each
  exactly **one** edit (or the labelled pair) committed on top of `T`. Input mutants are
  read by the counter through `git show <rev>:<path>`; counter-code mutants are executed
  from the fixture working tree checked out at the mutant commit (a checker cannot be
  invoked from a blob it is itself reading).
* Detector: the frozen counter itself, unmodified, run from each fixture's lane root:
  `python3 plans/round98_c1_replay.py --lane . --rev <mutant commit> --work <w> --grader-venv G`.
  Every run re-executes the full 12-case probe through `L6` (~4–5 min/run), so the matrix
  is behavioural, not static.
* Grader venv `G`: `uv venv -p 3.13` → CPython 3.13.16, `pytest==8.4.1`, `chess==1.11.2`
  (uv channel; no pacman transaction — host-wide pause respected).
* 29 counter runs: pristine baseline, 27 mutant probes (20 single input mutants, 1
  receipt-field probe, 4 counter-code probes, 2 coordinated-stamp doubles) and one
  restored run at `T`.
* Baseline (pristine `T`): `LEGS L1=pass … L10=pass`, TARGET byte-identical to the frozen
  target string, `PREDICATE R98-C1 pass`, rc 0. Wall 14m15s (run while 24 fixture clones
  were being built); the mutant matrix ran 6-way, 40 min wall.

## Kill matrix

`killed` = `PREDICATE R98-C1 fail` (rc 1); `SURVIVED` = predicate still `pass` (rc 0).

| # | mutant | target / edit | failing legs | predicate | verdict |
|---|---|---|---|---|---|
| 1 | `r1_lanetip_nonancestor` | receipt `LANE_TIP` → a real non-ancestor commit (parent `BASE`, made with `commit-tree`) | **L3** | fail | killed |
| 2 | `r2_detail_digest` | receipt `DETAIL C04 … sha=5d12…6d` → `…6e` | **L6** | fail | killed |
| 3 | `r3_case_observed_flip` | receipt `CASE C08 observed=F,F,F,P,0` → `P,P,P,P,1` | **L5, L6** | fail | killed |
| 4 | `r4_case_dropped` | receipt `CASE C12` line removed | **L5, L6** | fail | killed |
| 5 | `r6_subject_sha` | receipt `SUBJECT_SHA` → 64 zeros | **L2** | fail | killed |
| 6 | `r7_tool_sha` | receipt `TOOL_SHA` → 64 zeros | **L6, L9** | fail | killed |
| 7 | `r8_host_bash` | receipt `HOST_BASH` → `… (mutant)` | **L9** | fail | killed |
| 8 | `r10_receipt_absent` | receipt file deleted | **L1, L2, L3, L5, L6, L9** | fail | killed |
| 9 | `t1_predicted_flip` | table C07 `predicted=P,P,P,P,1` → `F,F,F,P,0` | **L4, L5, L6, L9** | fail | killed |
| 10 | `t2_app_swap` | table C06 `app=extra-line` → `drop-last` (same predicted vector) | **L4, L6, L9** | fail | killed |
| 11 | `t4_case_reorder` | table C01/C02 blocks swapped | **L4, L6, L9** | fail | killed |
| 12 | `t5_table_whitespace` | table `"member": "regex-chess"` → `"member":  "…"` (JSON-identical) | **L4, L6, L9** | fail | killed |
| 13 | `g1_extra_executed_member` | ledger `bn-fit-modify` `unexecuted` → `executed` | **L7** | fail | killed |
| 14 | `g2_removed_executed_member` | ledger `regex-log` `executed` → `unexecuted` | **L7** | fail | killed |
| 15 | `g3_legacy_receipt` | ledger `regex-chess.receipt` → another path | **L7** | fail | killed |
| 16 | `g4_classes` | ledger `regex-chess.classes` → `[file-artifact]` | **L7** | fail | killed |
| 17 | `s1_bad_anchor_row` | SOURCES row `S334` appended after BASE, anchor `sha256 1111…` unresolvable | **L10** | fail | killed |
| 18 | `s2_valid_anchor_row` | SOURCES `S334` appended naming a committed capture with its true digest | — | pass | **SURVIVED (control)** |
| 19 | `p1_probe_comment` | probe docstring word changed (behaviour identical) | **L6, L8, L9** | fail | killed |
| 20 | `c1_capture_byte` | capture `instruction.md` one byte changed | — (probe setup pin check refuses) | could-not-evaluate | **refused (rc 2)** |
| 21 | `r11_receipt_mismatches_field` | receipt `mismatches 0` → `mismatches 7` | — | pass | **SURVIVED** |
| 22 | `k1_l10_ignore_flagged` | counter `l10 = bool(added) and not flagged` → `bool(added)` | — | pass | **SURVIVED** |
| 23 | `k2_l7_superset` | counter `rev_set == base_set \| {MEMBER}` → `(base_set \| {MEMBER}) <= rev_set` | — | pass | **SURVIVED** |
| 24 | `d1_k1_s1` | pair: `k1` + `s1` | — | pass | **SURVIVED (pair)** |
| 25 | `d2_k2_g1` | pair: `k2` + `g1` | — | pass | **SURVIVED (pair)** |
| 26 | `d3_t5_table_stamp_coordinated` | pair: `t5` + receipt `CASE_TABLE_SHA` updated to the mutated table's sha | **L4** | fail | killed |
| 27 | `d4_p1_probe_stamp_coordinated` | pair: `p1` + receipt `TOOL_SHA` updated to the mutated probe's sha | **L8** | fail | killed |
| — | `baseline` / `restored` | pristine `T` | — | pass | pass |

Full output per run: `MutC1/out/<name>.out` + `.rc`; defect lines: `MutC1/defects.txt`;
machine-readable matrix: `MutC1/matrix.json`; hashes: `MutC1/hashes.md`.

## Which leg is load-bearing

* **L1** receipt presence — `r10` only.
* **L2** capture pins + receipt subject/test.sh/solve — `r6` only. Capture-byte tampering
  never reaches a leg: the probe's own pin check aborts the rerun and the counter returns
  `could-not-evaluate` before printing `LEGS` (`c1`).
* **L3** `LANE_TIP` ancestry — `r1` only. `LANE_TIP` is not a rerun stamp, so L3 is the
  sole guard.
* **L4** frozen case-table sha — never the sole killer among single mutants: every table
  edit also trips **L9** (receipt `CASE_TABLE_SHA` vs measured table) and **L6** (rerun
  stamp). `d3` (table whitespace + receipt stamp coordinated to the forged table) is
  killed by **L4 alone** — L4 is the only leg that still knows the frozen value.
* **L5** receipt vector equality — `r3`, `r4`, `t1`. It compares verdict vectors, not case
  identity or order: `t2` (app swap, same predicted vector) and `t4` (reorder) pass L5 and
  are caught by L4/L6.
* **L6** rerun reproduction — `r2` alone (DETAIL digest only), plus `r3`, `r4`, `r7`,
  `p1`, `t1`, `t2`, `t4`. It is the only leg that binds the `DETAIL` block.
* **L7** ledger — `g1` (extra executed member), `g2` (removed executed member), `g3`
  (legacy receipt field), `g4` (classes). Set equality is load-bearing: `g1` leaves two
  members in `set_added` and fails; the round-97 superset hole is closed in the frozen
  counter (but see survivor S-A).
* **L8** frozen probe sha — never the sole killer among single mutants: a probe edit also
  trips **L9** and **L6**. `d4` (probe comment + receipt `TOOL_SHA` coordinated) is killed
  by **L8 alone**.
* **L9** receipt stamps — `r8` (`HOST_BASH`) alone, plus `r7`, `t*`, `p1`.
* **L10** new SOURCES rows — `s1` alone; `s2` (valid anchor) passes, so L10 is not "any
  new row fails".

The tasking's premise that counter edits move L8/L4 does not hold for edits to
`plans/round98_c1_replay.py`: **no leg hashes the counter** (`grep -n 'frozen.get'` →
only `TABLE` at L4 and `TOOL` at L8; the counter never reads its own row in the
frozen-instruments table). Case-table edits move L4 (and L6/L9 via the receipt stamp);
probe edits move L8 (and L6/L9).

## Survivors with reproducers

### S-A. The counter's own bytes are unbound (informational; process-enforced, not a claim defect)

`k1` (L10 ignores `flagged`) and `k2` (L7 set equality weakened to superset) each pass on
pristine inputs, and the pairs `d1` (`k1` + bad SOURCES row) and `d2` (`k2` + extra
executed member) also pass. `d1` even prints the honest `new_rows_flagged=1` and `d2`
prints `executed_rows=43` in `TARGET`, while `defects=0` and the predicate says `pass`:
the legs are the only guards, and the counter cannot guard itself.

Reproducer (`d1`; ~5 min, needs the grader venv `G`; the scratch fixtures are deleted, so
rebuild from the lane):

```sh
F=/fast/scratch/hyaku/kengaku-r98/MutC1/f; mkdir -p "$(dirname "$F")"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$F"
git -C "$F" checkout -q --detach 8e37fc65d5649bb37166fdd6b1657445a8cb55b9
sed -i 's/l10 = bool(added) and not flagged/l10 = bool(added)/' "$F/plans/round98_c1_replay.py"
printf '\n| S334 | mutant row with an unresolvable anchor | own-work | A | mutant scope | sha256 %s | mutant | queued | 2026-11-06 | 90d | — |\n' \
  "$(printf '1%.0s' $(seq 64))" >> "$F/corpus/SOURCES.md"
git -C "$F" -c user.name=m -c user.email=m@example.invalid commit -qam mutant
cd "$F" && python3 plans/round98_c1_replay.py --lane . --rev HEAD --work /tmp/w-mut --grader-venv "$G"
# → LEGS … L10=pass ; TARGET … new_rows=9 new_rows_flagged=1 defects=0
# → PREDICATE R98-C1 pass
```

Interpretation: the frozen-instruments table lists `plans/round98_c1_replay.py`
`e3613832…`, but no leg reads that row. This is inherent to a self-checking predicate and
the round's freeze rule ("a frozen file changes after F" → claim not met) is enforced by
the round process (Q79/Q80), not by the counter. Recorded as an observation for round 99;
no repair attempted.

### S-B. Receipt informational fields are unread (low severity)

`r11` changes the receipt's `mismatches 0` to `mismatches 7`; all ten legs pass and the
TARGET line is byte-identical to the baseline (`mismatches=0` is recomputed from the CASE
lines). Static confirmation: `GRADER_UNPINNED`, `HOST_USERNS`, `SANDBOX`, `LEG_ORDER`
occur 0 times in the counter, and `MEMBER` / `mismatches` are never read via
`fields.get`. The predicate-bearing receipt parts (`SUBJECT_SHA`, `SOLVE_SHA`,
`TEST_SH_SHA`, `LANE_TIP`, `TOOL_SHA`, `CASE_TABLE_SHA`, `GRADER_SIDE`, `HOST_BASH`, and
the whole observation block) are bound. Severity low: the fields are informational and the
counter's printed `mismatches` is its own recomputation, so the TARGET line stays honest
even when the receipt field disagrees.

Reproducer (`r11`; same rebuild pattern):

```sh
F=/fast/scratch/hyaku/kengaku-r98/MutC1/f2; mkdir -p "$(dirname "$F")"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$F"
git -C "$F" checkout -q --detach 8e37fc65d5649bb37166fdd6b1657445a8cb55b9
sed -i 's/^mismatches 0$/mismatches 7/' "$F/corpus/evidence/round98/regexchess-probe.txt"
git -C "$F" -c user.name=m -c user.email=m@example.invalid commit -qam mutant
cd "$F" && python3 plans/round98_c1_replay.py --lane . --rev HEAD --work /tmp/w-mut2 --grader-venv "$G"
# → PREDICATE R98-C1 pass, TARGET identical to baseline (mismatches=0 recomputed)
```

## Control that must not be killed

`s2_valid_anchor_row` appends an `S334` row that names a committed capture and carries its
true digest: `L10=pass`, `TARGET … new_rows=9 new_rows_flagged=0`, rc 0. L10 is therefore
specific to *bad* new anchors, not to novelty.

## Restoration evidence

* Every fixture was reset to `T` after its run: `git status --porcelain` empty and the
  mutated file's sha256 back to its pre-mutation value (`MutC1/hashes.md`, 31 file rows;
  all `restored clean = True`). `r10` restores the deleted receipt to
  `575e5298…4092`.
* Counter-code fixtures (`k1`, `k2`, `d1`, `d2`) were executed from the mutant commit by
  design and then reset: `plans/round98_c1_replay.py` sha256 back to
  `e361383249d9bdf5c9fffb83c6df5dbd286007c951a70e68dd3e21201b4f2b2a`, working tree clean.
* Restored run at `T` in fixture `r1_lanetip_nonancestor` after its mutant run:
  `LEGS` and `TARGET` byte-identical to the pristine baseline, `PREDICATE R98-C1 pass`,
  rc 0 (`MutC1/out/restored.out`, diff against `MutC1/baseline.out` empty).
* The pristine clone was never mutated; all fixture commits are local to the scratch and
  are deleted with it.

## Verdict

**No input mutant survived.** All 18 single mutants of the counter's inputs that should be
rejected were killed by the leg the claim names (plus the redundant stamps), the capture
mutant was refused (`could-not-evaluate`, rc 2), and the one new-SOURCES-row control with
a valid anchor passed. The predicate is behaviourally sensitive across receipt fields,
case table (including a JSON-semantics-preserving byte change), ledger membership in both
directions, SOURCES anchors, probe bytes and capture bytes.

Two survivor classes, both outside the predicate's stated scope:

1. **Counter self-integrity** — no leg binds `plans/round98_c1_replay.py`; a weakened
   counter plus the input it should reject prints `pass` (`d1`, `d2`). Process-enforced by
   the freeze rule, not by the predicate. Informational, routed to round 99.
2. **Receipt informational fields** — `mismatches`, `MEMBER`, `GRADER_UNPINNED`,
   `HOST_USERNS`, `SANDBOX`, `LEG_ORDER` are unread (`r11`). Low severity; predicate-bearing
   fields are bound.

Redundancy noted, not a gap: L4 and L8 are never sole killers among single mutants because
the receipt's `CASE_TABLE_SHA` / `TOOL_SHA` stamps duplicate their bindings; the
coordinated doubles `d3`/`d4` show each is the only remaining guard once the receipt stamp
is updated with the forged bytes.

## Tooling record

| tool | version | channel | reason |
|---|---|---|---|
| CPython (grader venv) | 3.13.16 | `uv venv -p 3.13` | test.sh's `-p 3.13` pin |
| pytest | 8.4.1 | `uv pip install` | test.sh's `-w pytest==8.4.1` pin |
| chess | 1.11.2 | `uv pip install` | test.sh's `-w chess==1.11.2` pin |

No pacman transaction was run (host-wide pause). No tool outside the grader pins was
installed.

## Evidence index (`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-98/w1/MutC1/`)

| file | content |
|---|---|
| `baseline.out` | pristine `T` run (LEGS/TARGET/PREDICATE, rc 0) |
| `out/<name>.out`, `out/<name>.rc` | one run per mutant + `restored` |
| `defects.txt` | every `DEFECT` line emitted, grouped by run |
| `matrix.md`, `matrix.json` | kill matrix (table / machine-readable) |
| `hashes.md` | per-mutant before / after / restored sha256, fixture commit, clean flag |
| `manifest.json` | mutant definitions, fixture paths, commits, edits |
| `mk_mutants.py`, `run_mutants.py`, `summarise.py` | fixture builder, runner, summariser |
