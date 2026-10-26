# R37BatP6 — C1 battery module for the frozen P6 mutants (M20–M27)

Seat: executor R37BatP6, kengaku round 37 wave 1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
at tip `44b7298` ("round-37: wave-1 spec and validated dispatch (40 seats, policy v1)"), `plans/pkg_gate.py`
sha256 `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` = the freeze digest (counter's
`GATE … sha256=frozen` line in every receipt below).

## Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP6/battery/p6.py`

- sha256 `b81746fd6342227917a5c4a32a00235babec4860a07fe7811dcd7f171dc55e46`
  (`sha256sum .ufo/waves/round-37/build/R37BatP6/battery/p6.py`)
- stdlib only (`import re`); 8 fixtures, one per frozen mutant M20–M27, fid prefix `p6-`, `defects: ["P6"]`
  on every fixture; each `build(ctx, d)` = `ctx.genuine_package(d)` → one registry edit →
  `ctx.git_add(d)` → `["package", "--root", str(d), "--require-clean-tree"]` (no `--rerun`, so P10 never runs).
- Nothing in `plans/` was touched: the frozen gate, counter, probe, spec and mutant list are byte-identical,
  and the module is a standalone file the L1 can drop into `plans/battery37/`.

### Fixture design (why each row is a single defect, and 11 cells elsewhere)

All eight defects live in the one clause that reads the registry, `c_sources` (printed as `P6`); no other
clause reads `corpus/SOURCES.md` (P1 instruments, P2 receipt, P3/P4 entry quotes, P5 captures, P7 entry
provenance, P8 README+knowledge, P9 tree). Cells are edited **by index** on the one target row
(`_mutate`/`_set_cell`), so the coincidental `2fd12b88…` hash in cells[5] or the upstream name in cells[1] is
never hit by a whole-line substring replace.

| mutant | fixture fid | injected defect | gate note on the unmodified gate |
|---|---|---|---|
| M20 `rows={len(found)}` | `p6-m20-registry-row-duplicated` | one extra byte-identical copy of S105 | `P6 DEFECT rows=3 bad=1 first=S105: rows=2` |
| M21 `cells={len(cells)}` | `p6-m21-row-with-twelve-cells` | S106 gets a 12th trailing cell | `P6 DEFECT rows=3 bad=1 first=S106: cells=12` |
| M22 `url not the pinned raw path` | `p6-m22-url-off-the-pinned-raw-path` | S107's raw URL repointed to `…/regex-log/instruction.md` | `P6 DEFECT rows=3 bad=1 first=S107: url not the pinned raw path` |
| M23 `tier={cells[3]!r}` | `p6-m23-row-tier-b` | S106 tier `A` → `B` | `P6 DEFECT rows=3 bad=1 first=S106: tier='B'` |
| M24 `status={cells[7]!r}` | `p6-m24-row-status-queued` | S105 status `mined` → `queued` | `P6 DEFECT rows=3 bad=1 first=S105: status='queued'` |
| M25 `used-by is not the entry` | `p6-m25-used-by-another-path` | S107 used-by → `corpus/knowledge/tb2-regex-log-grader.md` | `P6 DEFECT rows=3 bad=1 first=S107: used-by is not the entry` |
| M26 `teaches words={n}` | `p6-m26-five-word-teaches-cell` | S105 teaches → `alpha beta gamma delta epsilon` (5 distinct words < `min_teaches_words`=8; the three cells stay pairwise distinct) | `P6 DEFECT rows=3 bad=1 first=S105: teaches words=5` |
| M27 `teaches cells are not pairwise distinct` | `p6-m27-two-identical-teaches-cells` | S107 teaches := S106's teaches (both ≥ 8 words, so only distinctness breaks) | `P6 DEFECT rows=3 bad=1 first=teaches cells are not pairwise distinct` |

`bad=1` and `defects=1` in each line is the gate's own report that exactly one defect was injected — no
second clause fires, so no "unavoidable second clause" note is needed. Full output:
`.ufo/waves/round-37/build/R37BatP6/single-defect.txt` (driver `single-defect.py`).

## Proof run 1 — every FIXTURE `ok`, every mutant `killed`

Command (verbatim; `$S=/fast/scratch/hyaku/kengaku-r37/R37BatP6`, `TMPDIR=$S`):

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round37_c1_verify.py \
  --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP6/battery \
  --only M20,M21,M22,M23,M24,M25,M26,M27 --work "$S"
```

Output in full (exit 0; saved as `.ufo/waves/round-37/build/R37BatP6/dev-run.txt`):

```
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE p6-m20-registry-row-duplicated expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m21-row-with-twelve-cells expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m22-url-off-the-pinned-raw-path expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m23-row-tier-b expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m24-row-status-queued expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m25-used-by-another-path expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m26-five-word-teaches-cell expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m27-two-identical-teaches-cells expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
BATTERY fixtures=22 wrong=0 renamed_disagree=0
MUTANT M20 P6 killed by=p6-m20-registry-row-duplicated -- registry row missing or duplicated
MUTANT M21 P6 killed by=p6-m21-row-with-twelve-cells -- registry row without 11 cells
MUTANT M22 P6 killed by=p6-m22-url-off-the-pinned-raw-path -- row url not the pinned raw path
MUTANT M23 P6 killed by=p6-m23-row-tier-b -- row tier wrong
MUTANT M24 P6 killed by=p6-m24-row-status-queued -- row status wrong
MUTANT M25 P6 killed by=p6-m25-used-by-another-path -- row used-by is not the entry
MUTANT M26 P6 killed by=p6-m26-five-word-teaches-cell -- teaches cell under min_teaches_words
MUTANT M27 P6 killed by=p6-m27-two-identical-teaches-cells -- teaches cells not pairwise distinct
MUTANTS total=8 killed=8 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`renamed_disagree=0` covers all 22 fixtures (the 14 frozen round-36 ones and my 8), so no fixture is
recognisable by its directory name; `null_detected=0` covers the two-copy null gate over all 22.

## Proof run 2 — every fixture is load-bearing

Method: a wrapper module per run re-exports the shipped `FIXTURES` minus exactly one fid
(`.ufo/waves/round-37/build/R37BatP6/load-bearing.py`, output `load-bearing.txt`), then the counter runs with
`--only <matching mutant>`. Dropping one fixture must flip exactly that mutant to SURVIVED.

| dropped fixture | `--only` | BATTERY | MUTANT | exit |
|---|---|---|---|---|
| `p6-m20-registry-row-duplicated` | M20 | `fixtures=21 wrong=0 renamed_disagree=0` | `M20 P6 SURVIVED` | 1 |
| `p6-m21-row-with-twelve-cells` | M21 | `fixtures=21 wrong=0 renamed_disagree=0` | `M21 P6 SURVIVED` | 1 |
| `p6-m22-url-off-the-pinned-raw-path` | M22 | `fixtures=21 wrong=0 renamed_disagree=0` | `M22 P6 SURVIVED` | 1 |
| `p6-m23-row-tier-b` | M23 | `fixtures=21 wrong=0 renamed_disagree=0` | `M23 P6 SURVIVED` | 1 |
| `p6-m24-row-status-queued` | M24 | `fixtures=21 wrong=0 renamed_disagree=0` | `M24 P6 SURVIVED` | 1 |
| `p6-m25-used-by-another-path` | M25 | `fixtures=21 wrong=0 renamed_disagree=0` | `M25 P6 SURVIVED` | 1 |
| `p6-m26-five-word-teaches-cell` | M26 | `fixtures=21 wrong=0 renamed_disagree=0` | `M26 P6 SURVIVED` | 1 |
| `p6-m27-two-identical-teaches-cells` | M27 | `fixtures=21 wrong=0 renamed_disagree=0` | `M27 P6 SURVIVED` | 1 |
| *(control: none dropped)* | M20…M27 | `fixtures=22 wrong=0 renamed_disagree=0` | `killed=8 survived=0` | 0 |

The control row (last) is the shipped module in the same wrapper; the eight rows above it each lose exactly
their own kill. The 14 frozen round-36 fixtures alone kill none of M20–M27 — that is the round-36 5/55
baseline reproduced for this clause (P6 was advertised by M20–M27 and demonstrated by none of them).

## Limits and risks

1. **Freeze-state dependency (real).** The declarations are the exact defect set on the lane as measured
   today: `corpus/knowledge/` holds 42 files, none of them C2's `tb2-git-webserver-grader.md`, so P8 is green
   on the genuine package (`r36-P0 … ok`). If C2's entry lands in `corpus/knowledge/` without its README
   index row (or the reverse), P8 turns DEFECT on **every** package fixture, including mine, and my
   `defects: ["P6"]` would then be a wrong declaration. The claims plan names this exact hazard
   ("C1 must be measured on a tree where C2's entry and index row are both present or both absent");
   integrating seats should land both in the same tip, or re-run the counter after both land.
2. **Registry-row coupling.** The builders key on row ids `S105`/`S106`/`S107` and require exactly one row
   each (`RuntimeError` otherwise, which would surface as a counter setup failure rather than a silent pass).
   A renumbering of those three rows (the round-36 routed S110-digest mistake class) would need the ids
   updated here; the frozen spec pins those ids, so within this freeze there is nothing to update.
3. **M22 uses a real-looking off-path URL** (`…/regex-log/instruction.md`) rather than a malformed one: the
   defect shown is "not the pinned raw path", i.e. the gate compares against the spec pin, not URL syntax.
4. Not measured (explicitly out of scope): whether each check is the *right* check — demonstration here is
   observational (branch reached, result visible), as the claims plan's C1 limit states.
5. This seat did not run the full 55-mutant predicate (the L1 owns post-integration gate execution); the
   8 assigned mutants were proven in the development mode the ticket specifies
   (`--only` + `--battery-dir`, which prints `PREDICATE C1 n/a` by design).

## Housekeeping

- Nothing written outside `.ufo/waves/round-37/build/R37BatP6/` (+ `R37BatP6.md`) and the scratch dir
  `/fast/scratch/hyaku/kengaku-r37/R37BatP6` (removed after the receipts were copied). No write to the lane's
  `corpus/`, `plans/`, git index or jj state; no commit; no pacman/uv/npx install (nothing new was needed).
- Receipts kept: `dev-run.txt`, `load-bearing.txt`, `single-defect.txt`, plus the two drivers
  `load-bearing.py` and `single-defect.py` (rerun as `python3 <driver> /fast/scratch/hyaku/kengaku-r37/<seat>`).
- Stray `__pycache__` created by the counter's module loader inside `battery/` was removed; the counter only
  globs `*.py`.

VERDICT: battery-p6-killed-8/8-wrong-0
