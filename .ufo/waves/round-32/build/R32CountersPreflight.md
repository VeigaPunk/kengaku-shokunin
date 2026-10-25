# R32CountersPreflight — frozen control receipts on the base tree

Agent: `L1Kengaku32.R32CountersPreflight` · 2026-10-25 · lane: `kengaku-shokunin`
Task: re-run the three frozen control receipts (round 32 claims) on the base tree and compare
to the committed control files under `.ufo/waves/round-32/claims/`.

## Lane state at run

- `git rev-parse master` = `6084cd3492c6aef10fd66afc36ffc00e79ace94a` (`round-32: freeze-commit gate receipt (Q20 out-of-band)`).
- Freeze commit `0d32691d` is parent; the only delta is `.ufo/waves/round-32/gate-receipt.txt` (+16 lines).
  Nothing any of the three counters reads. `git diff 0d32691d -- .ufo/waves/round-32/claims/` is empty —
  control files are byte-identical to the freeze commit.
- Working tree: no tracked modifications (only untracked round-32 wave/build artifacts).
- No tools installed/updated this run (system python3 only); no pacman, no channel activity.

## (a) C1 receipt — `plans/adoption_check.py`

Command: `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census` (cwd = lane root)

```
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
exit=1
```

Control `control-nothing.txt` (committed at freeze): same single counter line + `exit=1`; informational header
`expect_sha256=a1a7e8604008532242b9b8e4ef06485b386e24508ac0e29072d95263ca73be9f` — verified
`sha256sum` of on-disk `adoption-expect.json` matches exactly.
Result: **MATCH** (stdout line identical; exit 1 == control).

## (b) C2 receipt — `plans/round32_defects.py`

Command: `python3 plans/round32_defects.py --lane .`

```
DEFECT R1 round31-report-phantom-hash: no appended erratum supersedes the a44b5a8 citation
DEFECT R2 round32-report-order-tip: /home/vgpnk/Projects/shokunin/.ufo/reports/round-32/kengaku.md does not exist yet: the round-32 report must land after the last lane commit
DEFECT R3 round31-cli-receipt-regenerated: the tip receipt still contains 'can't open file' failure lines
DEFECT R4 skill-registry-row: SKILL.md has no sources_adopt.py row
DEFECT R5 round31-dead-seat-recorded: corpus/lessons/round-32.md does not exist yet: the round-32 lesson must record the seat ledger
DEFECT R6 lesson-locators-corrected: no appended correction updates verifier_mode.py's precedence locator to :39-40
DEFECT R7 round30-peer-review-erratum: no appended erratum records S086 as published without peer review
checks=7 defects=7
exit=1
```

Control `defects-before.txt`: byte-identical stdout, `exit=1`.
Result: **MATCH** (exit 1 == control).

## (c) C3 receipt — `plans/catalog_probe.py`

Command: `python3 plans/catalog_probe.py --diff --lane .` (live probes to HF `api/models` and OpenRouter `api/v1/models`)

```
probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale
HF missing fields: author, sha, lastModified, gated
exit=1
```

Control `catalogs-before.txt`: byte-identical stdout, `exit=1`.
Result: **MATCH** (exit 1 == control).

## Comparison and hazards

- All three receipts print exactly the frozen control lines and exit 1, matching the committed
  `*-before.txt` controls (byte-level diff done on stripped stdout; `exit=` trailer verified against each run).
- No hazard: no difference between run output and committed controls for any of the three receipts.
- Observations (not receipt drift): lane tip is `6084cd3`, one commit past the claimed baseline
  `f20a1097`; that commit is the out-of-band Q20 gate-receipt add and does not touch any counter input.
  The C2 R2 check reads `rev-parse master` (now `6084cd3`) and currently fails only because the
  round-32 report does not exist yet — consistent with the pre-repair control.

## VERDICT: controls-match
