# CounterR84 — R84-C1 counter (leaf seat)

Claim R84-C1, base `4087b2f8369fb0c317a8460725a607681ff2fd7f`, freeze
`b12a9d46806cb8d69fe48fac0f4efff0b266e4c2`. The frozen predicate, target, case table,
control set and kill rule were read from `plans/round-84-claims.md` and not edited.

## Deliverable

`.ufo/waves/round-84/w1/CounterR84/round84_c1_replay.py`,
sha256 `ea8cfdda495959b5ceeac52ca2e2a8581562c89c7edacfba9cc9ae0670bb61ee`
(draft; the L1 installs it at `plans/round84_c1_replay.py`).

Structure and verdict grammar copied from `plans/round83_c1_replay.py`: UNIVERSE, RECEIPT,
REPRODUCE, LEDGER, `DEFECT <CODE> <detail>`, `DEFECTS n=`, `TARGET …`, `PREDICATE R84-C1
pass|fail`; exit 0/1/2. Modes: verdict (`--lane DIR [--rev REV] --work DIR`), `--selftest`,
`--mutants`, `--control-do-nothing`, `--control-ledger-only`,
`--control-fabricated-observations`. `--work` defaults to TMPDIR; no hardcoded `/tmp`.
The production path runs the tracked instrument from the measured tree; runner injection
exists only inside fixtures.

## Evidence (scratch $S=/fast/scratch/hyaku/kengaku-r84/CounterR84; lane copy is a shared
`--no-checkout` clone at BASE, toplevel verified)

| mode | exit | transcript |
|---|---|---|
| production BASE, `--rev 4087b2f8…` | 1 | `before-base.txt` |
| selftest | 0 | `selftest.txt` (30 cases, 29 red, 0 failures) |
| mutants | 0 | `mutants.txt` (16 real corruptions, 16 killed) |
| control do-nothing | 0 | `control-do-nothing.txt` (target_reached=False) |
| control ledger-only | 0 | `control-ledger-only.txt` (target_reached=False) |
| control fabricated-observations | 0 | `control-fabricated-observations.txt` (target_reached=False) |
| green fixture lane (worktree) | 0 | `green-fixture-lane.txt` |
| green fixture lane (`--rev`) | 0 | `rev-head-green.txt` |
| trust pin absent | 2 | `setup-missing-tool-draft.txt` |
| reviewed probe, fixed bytes (compat) | 0 | `probe-compat.txt` |
| probe minted body vs counter grammar | 0 | `probe-receipt-grammar.txt` |

BASE verdict (exact frozen before-state shape):
`DEFECTS n=34`, `TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0
defects=34`, `PREDICATE R84-C1 fail`, exit 1.

Green fixture-lane after-state: `REPRODUCE … rc=0 matched=yes`, `located=1`, `executed=1`,
`TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0`,
`PREDICATE R84-C1 pass`, exit 0. The lane is a scratch construction from BASE (real subject
bytes, eight claims vectors, receipt naming the minting tip); it is not production evidence.

## Findings for the L1

1. **Freeze tree lacks `plans/round84-cases.json` and `plans/round84_gcode_probe.py`.**
   `git ls-tree b12a9d46 -- plans/` has neither. The counter therefore freezes the eight
   vectors from the claims (`CLAIMS_CASES`, order and `[PF]/[PF]` re-derived) and
   byte-compares the measured table to the freeze tree only if that tree carries it. To
   make the domain probe's own pin hold, install the table byte-identical to ProbeR84's
   `round84-cases.json` (sha256 `5b86f8d7efc24a529b4c53a23c6a4ccaed51866428535e6f0fcb4dbf13982cb5`,
   which the probe pins as `FROZEN_TABLE_SHA`).
2. **The probe draft had a staging defect and was fixed mid-wave.** At sha `ff2a2a9e…` it
   staged `app/output.txt` while the capture reads `/app/out.txt`; a real replay printed
   `observed=F/F` for all eight cases, `cases=8 mismatches=7`, `PREDICATE R84-PROBE fail`,
   exit 1. ProbeR84 reports the fix; the final bytes (`82f359e6…`, 17205 bytes, verified
   here) print all eight vectors as predicted and exit 0. Its pre-commit receipt body was
   parsed with this counter's own grammar (`probe-receipt-grammar.txt`): 12 stamps in order,
   8 CASE lines, `cases=8 mismatches=0`, `PREDICATE R84-PROBE pass`, 6-token COMMAND,
   TOOL_SHA equal to the draft, block equal to a fresh run — rejected only by `WORKTREE
   dirty` and its pre-integration `LANE_TIP`, which the L1 re-mints after the commit.
   Mint only from the fixed instrument.
3. **Receipt header.** The counter requires line 1 to be exactly
   `# tb2 gcode-to-text grader probe`. The reviewed probe now prints it from `main()`;
   a plain stdout mint satisfies the grammar.
4. **Trust pin is run-time.** `TRUSTED_TOOL_SHA` is read from
   `.ufo/waves/round-84/w1/ProbeR84/round84_gcode_probe.py`; absent → exit 2
   (`DEFECT SETUP trusted tool draft absent: …`), never a fabricated pin. Install
   `plans/round84_gcode_probe.py` byte-identical to the final draft, or the counter emits
   `TOOL-UNTRUSTED`.
5. **Mint on a clean tree, after the integration commit(s).** Probe stamps and the counter
   both reject a dirty tree; the pre-integration lane is dirty (untracked
   `.ufo/waves/round-84/`). `LANE_TIP` must be an ancestor of the measured tip and carry the
   same subject/table/tool bytes.
6. The claims' "table byte-equal at the freeze commit" shape is unavailable because the
   file postdates the freeze commit; the semantic pin is the faithful reading. Reported,
   claim untouched.

No blockers. Tool installs: none.
