# ScribeCorrectionsR76 findings

Axes: coverage and calibration. Paths below are lane-root-relative. Production files were read only.

## Behavior and assignment disposition

The initial seven-text drafting request was superseded by KengakuR76's direct instruction: "Q55 (lines ~1264-1270) IS the round-76 D1 criterion — do not draft Q56 or a supersession of it." The requested deliverable became a line-by-line check of integrated discharge legs plus exact D6 ledger text if both receipts existed. Both existed. The scoped handoff is `.ufo/waves/round-76/w1/ScribeCorrectionsR76/corrections.md`.

## Commands and outcomes

All subprocess commands below used cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin` and environment `PYTHONDONTWRITEBYTECODE=1`. The three independent commands ran concurrently. Exit codes are observed subprocess return codes.

```text
python3 -B plans/round75_c1_index_parity.py --lane . --selftest --work /fast/scratch/hyaku/kengaku-r76/ScribeCorrectionsR76/c1
EXIT 0
SELFTEST cases=8 red=7 failures=0 ok=True

python3 -B plans/round75_c2_registry_audit.py --lane . --selftest --work /fast/scratch/hyaku/kengaku-r76/ScribeCorrectionsR76/c2
EXIT 0
SELFTEST ok tally: real=10 expected_matched=10 wrong_id=0
SELFTEST arms=5 failures=0 ok=True

python3 -B /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/ScribeCorrectionsR76/derive-index.py
EXIT 0
UNIVERSE knowledge files=74 indexed=70 missing=4 orphan=0
UNIVERSE lessons files=123 indexed=87 missing=36 orphan=0
UNIVERSE evidence dirs=66 indexed=46 missing=20 orphan=0
FINAL_RULE rev=43255758 total=60 split=4/36/20
```

Both selftests stamped `LANE_TIP 6977019bdf56a88921e14f728167da8f5726c1fc` and `WORKTREE dirty`; these are not clean committed-tree selftest receipts. Full outputs are c1-selftest.txt, c2-selftest.txt and derive-index.txt under the seat directory.

The independent count script performs read-only Git commands `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 43255758:corpus/README.md` and `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only 43255758 corpus`. It strips comments/fences, accepts complete rendered table rows and compares named entries with the committed tree. No index gate helper was imported for this derivation.

### Leg-only replay, not full CLI gate

The CLI's observed hard-coded scratch path violated seat bounds, so it was not run. An Eval Python cell imported the gate with bytecode disabled and executed these exact calls (lane and scratch are pathlib.Path):

```python
reader = module.Reader(lane, 'worktree')
vals = module.derivations(lane, scratch, False)
lines, defects = module.legs(reader, vals, False)
```

Here `module` loaded `plans/round76_c2_defect_discharge.py`; scratch was `/fast/scratch/hyaku/kengaku-r76/ScribeCorrectionsR76`. `derivations` executed the two selftests again as part of the requested leg check, with `--work` beneath that owned tree. This second execution is disclosed rather than counted as independent corroboration. The leg-only outcome `LEG_ONLY_EXIT 0` means an empty returned defect list, not a CLI process exit code.

```text
LEG D1 ok QUALITY criterion cites R75-D1 + lesson
LEG D2 ok SCORECARD line with R75-D2, stamp 9f8f0f218082, 5d9a0ccc
LEG D3 ok SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
LEG D4 ok registry rows carry cases=8 red=7 / arms=5
LEG D5 ok LOG block with R75-D5, cases=8 red=7, stamp 9f8f0f218082
LEG D6 ok r74-c1-tip.txt=pass/ancestor r74-c2-tip.txt=pass/ancestor
LEG D7 ok round-74 lesson appended correction naming R75-D7
LEG_ONLY_EXIT 0
```

## Numbered findings

1. **MEDIUM — CLI ignored seat-owned scratch.** Observed gate `emit()` at plans/round76_c2_defect_discharge.py:360–361 used the exact bytes `work = Path("/fast/scratch/hyaku/kengaku-r76/c2")`, followed by `work.mkdir(parents=True, exist_ok=True)`. Passing `--work /fast/scratch/hyaku/kengaku-r76/ScribeCorrectionsR76` could not redirect emit's writes. Reported to KengakuR76; L1 subsequently stated it was fixed, crediting this seat and C2ReplayR76. That later fix was not rerun or independently verified by this seat.
2. **INFO — all seven current frozen legs passed leg-only replay.** Pointer: seat directory `legs.txt`. D1/D2/D3/D4/D5/D7 integration locations and D6 field values are in `corrections.md`. No full ledger/predicate verdict is inferred.
3. **INFO — integration text and initial draft formatting differ.** QUALITY.md:1265 names R75-D1, with the lesson path at :1268; LOG.md:2855 starts R75-D5, while counts/stamp follow at :2856–2857; SCORECARD.md:3439 exceeds the initial 200-character drafting limit. These pass the actual frozen legs, which use four-/six-line blocks or unrestricted lines. L1 explicitly instructed no further production edits. Do not silently describe these as satisfying the initial same-line/length drafting constraint.
4. **INFO — final-rule before count corroborated independently.** Pointer: `derive-index.py` and `derive-index.txt`; 60 = 4/36/20 at 43255758, not the historical pre-A3 receipt's 59. Both executed selftest counts match the integrated registry literals.
5. **INFO — D6 has observed receipts, not execution by this seat.** `corpus/evidence/round76/r74-c1-tip.txt:1–12` and `r74-c2-tip.txt:1–12` both stamp `6977019bdf56a88921e14f728167da8f5726c1fc`, declare `WORKTREE clean`, and contain their corresponding predicate pass. The leg resolved ancestry; neither underlying round-74 gate was executed here.

## Touched surfaces, limits and artifacts

Only this seat's `.ufo/waves/round-76/w1/ScribeCorrectionsR76/` artifacts and findings report were written. No production edits, git mutations, fleet access, installations, upgrades, runtime dispatch, commits or publication. Owned scratch was removed in Python `finally` blocks after receipts were saved; both cleanup outputs were `SCRATCH_REMOVED True`.

Artifacts: `corrections.md`, `derive-index.py`, `derive-index.txt`, `c1-selftest.txt`, `c2-selftest.txt`, `legs.txt` under the seat directory, plus this report. The derivation script is retained evidence, not a product implementation.

Unverified: full R76-C1/R76-C2 CLI predicates, complete ledger closure/close_commit correctness, clean landing replay, later integrated scratch-path fix, any subsequent file changes. L1 owns the D6 close_commit and final gate run. No broader round conclusion is claimed.

Self-evaluation (1–5): accuracy 4 (leg-only, not clean landing evidence); completeness 4 (L1's narrowed request fulfilled; full CLI intentionally unrun); clarity 4 (method distinction explicit, detailed provenance adds length); actionability 4 (D6 fields supplied, close_commit necessarily integrator-owned); conciseness 4 (exact evidence retained at cost of report length). Overall 4.0. Highest-impact improvement belongs to L1's final clean-tree gate run, not a new seat-side probe. Would the user agree: the report exposes the execution boundary and supplies the requested integration bytes.
