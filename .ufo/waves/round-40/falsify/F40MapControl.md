# F40MapControl — red-control of the C2 requirement map (V7), round 40 wave 2

Seat: F40MapControl (mutation-tester) · 2026-10-26 · lane tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed` (branch master)
Raw logs: `.ufo/waves/round-40/falsify/F40MapControl/run-logs.md`

## What this attacks

C2's admission rests on V7 ("requirement map", round-37 closure item D2): the entry's `## Requirement map`
table must carry exactly one row per frozen tag, each row's label equal to the label **derived** from every
receipt case whose `violates=` set carries the tag, and every cited case a real violating case
(`plans/round40_c2_verify.py:64-67` docstring; `v7` at `plans/round40_c2_verify.py:216-247`). If V7 can be
satisfied by a hand-edited map, the "labels are derived, not chosen" claim
(`corpus/knowledge/tb2-db-wal-recovery-grader.md:123`) is decorative and the C2 predicate is gameable by
whichever seat writes the entry. This seat flips each of the six map labels, cites a non-violating case,
drops a row, duplicates a tag, and changes a line number — one mutation per verifier run — and asks whether
V7 reds each time.

## Fixture and detector

- Scratch clone: `S=/fast/scratch/hyaku/kengaku-r40/F40MapControl`; `git clone -q --no-local <lane> "$S/lane"`
  then `checkout -q ec1005a2a28b…`; `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`; `TMPDIR=$S`,
  `--work "$S"`; scratch deleted at the end. No lane file outside the clone was touched; no git mutation.
- Detector: `python3 plans/round40_c2_verify.py --lane "$S/lane" --work "$S"` inside the mandated
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000
  --proc /proc --unshare-pid --die-with-parent …` for **every** invocation (baseline, 10 mutants, restored).
- Mutated file: `corpus/knowledge/tb2-db-wal-recovery-grader.md` (the spec's `entry`,
  `plans/pkg-spec-r40.json`). Pristine sha256 `f51dd9e7766de9a96f7efe96582aadc3f39e24e9b2c2a4975b0b35c29649a9ba`;
  restored to that hash after every run (10/10 verified).

## Baseline (pristine) — green

`V7 ok rows=6 tags=6 bad=0`, `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 (2.55 s). Full output in
`run-logs.md`. A baseline failure would have made every mutant inconclusive; it is green, so kills below are
real.

## Mutations and verdicts (10/10 killed)

| # | Mutation (entry `## Requirement map`, lines 133-138) | Mutated sha256 (first 12) | V7 output | Verdict |
|---|---|---|---|---|
| M1 | `fix-wal` label `partly`→`enforced` | `c5fa6f9ad000` | `V7 DEFECT … bad=['fix-wal: labelled enforced, receipt derives partly']` | killed |
| M2 | `extract-all` label `partly`→`unenforced` | `1556d313e69e` | `bad=['extract-all: labelled unenforced, receipt derives partly']` | killed |
| M3 | `json-at-path` label `enforced`→`partly` | `af29d464faca` | `bad=['json-at-path: labelled partly, receipt derives enforced']` | killed |
| M4 | `record-format` label `partly`→`enforced` | `8693bf689c97` | `bad=['record-format: labelled enforced, receipt derives partly']` | killed |
| M5 | `sorted-by-id` label `enforced`→`unenforced` | `b026fe29be0e` | `bad=['sorted-by-id: labelled unenforced, receipt derives enforced']` | killed |
| M6 | `eleven-records` label `enforced`→`partly` | `ce652153582c` | `bad=['eleven-records: labelled partly, receipt derives enforced']` | killed |
| M7 | cite non-violating case: add `oracle-solve-sh` (receipt `violates=` empty) to the `sorted-by-id` row | `23755cee238a` | `bad=['sorted-by-id: cites no case or a case that does not violate it']` | killed |
| M8 | drop the `sorted-by-id` row | `dd2dd578a9a5` | `V7 DEFECT rows=5 … bad=["tags missing=['sorted-by-id'] duplicated=0"]` | killed |
| M9 | duplicate the `sorted-by-id` row (byte-identical second row) | `26a4fea4df3a` | `V7 DEFECT rows=7 … bad=["tags missing=0 duplicated=['sorted-by-id']"]` | killed |
| M10 | `fix-wal` line `instruction.md:7`→`instruction.md:6` | `aebc1e41c73c` | `bad=['fix-wal: line 6 is not the frozen instruction.md:7']` | killed |

Every mutated run: `checks=7 defects=1`, `PREDICATE C2 fail`, exit 1. The six label flips are caught because
V7 recomputes each label from **all** receipt `violates=` sets (`v7` → `derive(set(violating.values()))`),
not from the cited witnesses — the round-37 failure mode (`enforced` beside an observed-pass violating case)
cannot be reintroduced by relabelling.

## Isolation evidence (the red is V7's, nothing else's)

On every mutated run V1-V6 stayed `ok` and the package gate printed `gate: defects=0` (full gate blocks in
`run-logs.md`); the only flipped check is V7. Two structural reasons, both read from source: the gate's
clean-tree check P9 lists only untracked files (`git ls-files --others --exclude-standard`,
`plans/pkg_gate.py:260`), so an edited tracked entry does not trip it; and P10's fresh probe rerun never
reads the entry (probe input is the capture dir, `plans/db_wal_probe.py`). So a map-only forgery is invisible
to everything except V7 — and V7 catches all ten shapes tried here.

## Restoration evidence

After each mutation the pristine bytes were copied back and sha256-verified equal to
`f51dd9e7766de9a96f7efe96582aadc3f39e24e9b2c2a4975b0b35c29649a9ba` (10/10). Final run on restored bytes:
`checks=7 defects=0`, `PREDICATE C2 pass`, exit 0. `git -C "$S/lane" status --porcelain` empty; HEAD still
`ec1005a2a28bc5cfdde7723374368ed4cc956eed`. Scratch `$S` deleted before finishing.

## Scope and limits

- The detector surface exercised is V7's map control only; V1-V6 were observed green throughout and were not
  separately attacked (other seats' assignments).
- The ten mutants are the assigned shapes (six label flips + non-violating citation + dropped row +
  duplicated tag + changed line number); no other V7 bypass (e.g. renaming a tag to a non-frozen one, which
  the `not a frozen tag` branch also catches) was probed.
- All runs executed under the mandated bwrap; no tool was installed (bwrap 0.13.1 and host python3 already
  present); no process left running.

Caught/total: **10/10** — every assigned map forgery is caught by V7 and by nothing else needing to fire.

VERDICT: map-controls-red-10/10
