# R40BatAnchorRow — battery40 anchor row-shape fixtures (kengaku r40, wave 1)

Scope: one C1 battery40 module that kills frozen mutants **A06, A08, A09** of
`plans/round40_c1_verify.py` ATTRIBUTABLY in their declared directions. Nothing frozen was edited, no lane file
was written: the only landing artefact is `plans/battery40/a_row.py` for the L1 to copy in.

## Deliverable

| item | value |
|---|---|
| module (draft) | `.ufo/waves/round-40/build/R40BatAnchorRow/battery/a_row.py` |
| intended landing path | `plans/battery40/a_row.py` |
| sha256 | `7b0b6e9cc48ff65fa9bb3ad37f8536b9bad3feed70e2fe32a3f280a1e6be13bc` (2678 bytes) |
| fids | `a_row-indent4-wrong`, `a_row-token-in-teaches`, `a_row-12-cells` |
| mutant targets | A06, A08, A09 (anchor tool, exit-code directions) |

```
$ sha256sum .ufo/waves/round-40/build/R40BatAnchorRow/battery/a_row.py
7b0b6e9cc48ff65fa9bb3ad37f8536b9bad3feed70e2fe32a3f280a1e6be13bc  .../battery/a_row.py
$ python3 - <<'PY'   # SIDECHANNEL scan over the module source (counter token list, lowercased)
... print("sidechannel hits:", [x for x in S if x in t])
sidechannel hits: []
```
(receipt: `R40BatAnchorRow/sidechannel-scan.txt`)

## Fixtures: one row-shape behaviour each

Each `build(ctx, d)` does `ctx.clone(d / "lane")`, rewrites only the S111 row of
`corpus/SOURCES.md` **in that clone's working tree**, and returns `["--lane", "<d>/lane"]`. No commit is needed:
`parse_rows` reads `lane / "corpus/SOURCES.md"` from the working tree, while `evidence_index` reads
`git ls-tree HEAD`, and no fixture touches `corpus/evidence/`. A missing S111 or S108 row raises
`ValueError` → counter `SETUP`, never a silent wrong fixture.

| fid | one-line behaviour (builder docstring) | expect | declared `defects` | ref rc / classes | mutant | mut rc / classes | direction |
|---|---|---|---|---|---|---|---|
| `a_row-indent4-wrong` | 4-space-indented copy of S111 carrying another row's real digest: not a row | accept | `-` | 0 / `-` | A06 | 1 / `digest-wrong-capture` | rc-mirror ✓ |
| `a_row-token-in-teaches` | S111's digest claim moved into the teaches cell: present, but outside the anchor cell | reject | `token-outside-anchor` | 1 / `token-outside-anchor` | A08 | 0 / `-` | rc-silence ✓ |
| `a_row-12-cells` | S111 with a twelfth cell appended: still census-shaped, no longer an 11-cell row | reject | `row-malformed` | 1 / `row-malformed` | A09 | 0 / `-` | rc-silence ✓ |

Mutant branches exercised (frozen cells, `plans/round40_c1_verify.py`):

* A06 `ROW = … "^ {0,3}\|…"` → `"^ {0,4}\|…"` (:31 adv: "so this check and the census agree on what a row is").
  Reference does not parse the indented line as a row at all (round-39 witness `X09-indent4-wrong`:
  `rows=108` vs `109` at the tip, `rc=0`), so its wrong digest is invisible; the mutant parses it and flags
  `digest-wrong-capture`. "Wrong digest" = the **S108 row's committed
  digest**, a real capture of another row (not synthetic hex), i.e. the substitution shape the tool advertises
  against.
* A08 `if cell_idx != ANCHOR_CELL:` → `if False:` (:81 adv: "a token outside the anchor cell is
  `token-outside-anchor` — always a defect, whatever its value"). The moved token is S111's **correct** digest,
  so the mutant falls through, resolves it as the anchor and exits 0.
* A09 `if len(r["cells"]) != NCELLS:` → `< NCELLS` (:34-35 adv: "A row that matches the census regex but does
  not have 11 cells is a `row-malformed` defect"). Anchor cell index 5 is unchanged by the appended cell, so
  the mutant sees a valid token and exits 0.

### Cross-fixture isolation (explicit ref/mutant runs, receipt `probe-runs.txt`)

```
a_row-indent4-wrong expect=accept ref_rc=0 ref_classes=-
  A06 mut_rc=1 mut_classes=['digest-wrong-capture']
  A08 mut_rc=0 mut_classes=-
  A09 mut_rc=0 mut_classes=-
a_row-token-in-teaches expect=reject ref_rc=1 ref_classes=['token-outside-anchor']
  A06 mut_rc=1 mut_classes=['token-outside-anchor']
  A08 mut_rc=0 mut_classes=-
  A09 mut_rc=1 mut_classes=['token-outside-anchor']
a_row-12-cells expect=reject ref_rc=1 ref_classes=['row-malformed']
  A06 mut_rc=1 mut_classes=['row-malformed']
  A08 mut_rc=1 mut_classes=['row-malformed']
  A09 mut_rc=0 mut_classes=-
```
Only the diagonal satisfies a declared direction; each off-diagonal cell leaves the other mutant at the
reference exit code, so no kill is borrowed.

## Proof run: `--only A06,A08,A09`

```
$ S=/fast/scratch/hyaku/kengaku-r40/R40BatAnchorRow; export TMPDIR="$S"
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round40_c1_verify.py \
    --lane "$S/lane" \
    --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-40/build/R40BatAnchorRow/battery \
    --only A06,A08,A09 --work "$S/w"
PINS total=3 mismatched=0
FIXTURE a_row-indent4-wrong tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_row-token-in-teaches tool=anchor expect=reject declared=token-outside-anchor observed_rc=1 observed=token-outside-anchor ok
FIXTURE a_row-12-cells tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
MUTANT A06 anchor rc-mirror killed by=a_row-indent4-wrong -- plans/anchor_digest_check.py:31 'Row set — the census shape (... `^ {0,3}\\|\\s*(S\\d{3,})
MUTANT A08 anchor rc-silence killed by=a_row-token-in-teaches -- plans/anchor_digest_check.py:81 'a token outside the anchor cell is `token-outside-anchor`
MUTANT A09 anchor rc-silence killed by=a_row-12-cells -- plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have 
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```
(receipt: `R40BatAnchorRow/dev-only.txt`; exit 0)

## Load-bearing table (remove one fixture, re-run the same three mutants)

Each variant module is the shipped source with exactly one `FIXTURES` entry deleted (scratch only):

| removed fixture | A06 | A08 | A09 | receipt |
|---|---|---|---|---|
| `a_row-indent4-wrong` | **SURVIVED** `exhibits=none` | killed by=`a_row-token-in-teaches` | killed by=`a_row-12-cells` | `drop-indent4.txt` |
| `a_row-token-in-teaches` | killed by=`a_row-indent4-wrong` | **SURVIVED** `exhibits=none` | killed by=`a_row-12-cells` | `drop-token_in_teaches.txt` |
| `a_row-12-cells` | killed by=`a_row-indent4-wrong` | killed by=`a_row-token-in-teaches` | **SURVIVED** `exhibits=none` | `drop-cells12.txt` |

Every row also prints `BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0` /
`MUTANTS total=3 killed=2 survived=1 invalid=0 null_detected=0`. The mapping fixture→mutant is 1:1 and each
fixture is necessary.

## Full default counter in the clone (module copied to `$S/lane/plans/battery40/`)

```
$ cp .ufo/waves/round-40/build/R40BatAnchorRow/battery/a_row.py "$S/lane/plans/battery40/a_row.py"
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round40_c1_verify.py \
    --lane "$S/lane" --work "$S/w2"
PINS total=3 mismatched=0
FIXTURE a_row-indent4-wrong tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_row-token-in-teaches tool=anchor expect=reject declared=token-outside-anchor observed_rc=1 observed=token-outside-anchor ok
FIXTURE a_row-12-cells tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
MUTANT A01 anchor silence SURVIVED exhibits=none
MUTANT A02 anchor rc-silence SURVIVED exhibits=none
MUTANT A03 anchor rc-silence SURVIVED exhibits=none
MUTANT A06 anchor rc-mirror killed by=a_row-indent4-wrong
MUTANT A08 anchor rc-silence killed by=a_row-token-in-teaches
MUTANT A09 anchor rc-silence killed by=a_row-12-cells
MUTANT A15 anchor rc-silence SURVIVED exhibits=none
MUTANT A17 anchor rc-mirror SURVIVED exhibits=none
MUTANT A21 anchor rc-mirror SURVIVED exhibits=none
MUTANT A22 anchor rc-mirror SURVIVED exhibits=none
MUTANT A27 anchor silence SURVIVED exhibits=none
MUTANT L01 ledger error SURVIVED exhibits=none
MUTANT L05 ledger rc-silence SURVIVED exhibits=none
MUTANT L06 ledger rc-silence SURVIVED exhibits=none
MUTANT L11 ledger error SURVIVED exhibits=none
MUTANT L14 ledger rc-silence SURVIVED exhibits=none
MUTANT L15 ledger rc-silence SURVIVED exhibits=none
MUTANT L21 ledger error SURVIVED exhibits=none
MUTANT O04 order rc-silence SURVIVED exhibits=none
MUTANT O12 order rc-error SURVIVED exhibits=none
MUTANT O14 order error SURVIVED exhibits=none
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=3 survived=18 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```
(receipt: `R40BatAnchorRow/full-counter.txt`)

Reading: all three of my mutants are killed in the full default topology too, `wrong=0`, `tampered=0`,
`sidechannel=0`, `invalid=0`, `null_detected=0`, pins stable. The 18 survivors are the other wave-1 seats'
targets — my clone's `plans/battery40/` holds only `a_row.py` — so `PREDICATE C1 fail` here is the
pre-integration state, not a defect of this module.

## Notes, limits, risks

* Determinism: both the reference and the null pass run byte-identical (`null_detected=0`); fixture trees are
  fingerprinted before/after (`tampered=0`), i.e. builds leave no process or file mutation behind.
* The fixtures' only argv is `--lane <inside d>`; the counter's `path_ok` contract check passed for all three.
* The A06 fixture's "wrong digest" is S108's token read at build time from the same `SOURCES.md`, so it tracks
  the corpus: should S108's row move or lose its token, the build fails loudly (`AttributeError`/`ValueError`
  → `SETUP`) rather than declaring a fixture whose reference result silently drifts.
* Limit inherited from the counter, not repaired here: the module cannot prove the fixture's *intent*, only the
  result difference in the declared direction; A06's adhesion to "not a row" is what makes the difference
  attributable (the reference reports 0 defects on that tree).
* Hygiene: all clones, variants and work dirs lived under `/fast/scratch/hyaku/kengaku-r40/R40BatAnchorRow/`
  (removed at the end); receipts were copied into this report dir first. No `git add/commit` ran in the lane; no
  jj command ran anywhere; no pacman transaction was attempted and no tool was installed.
* Scratch receipts in `R40BatAnchorRow/`: `battery/a_row.py` (sha256 above), `dev-only.txt`, `drop-*.txt`,
  `probe-runs.txt`, `full-counter.txt`, `sidechannel-scan.txt`, this report.

VERDICT: battery40-a_row-killed-3/3-wrong-0
