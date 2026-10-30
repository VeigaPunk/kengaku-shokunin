# R55-W1 M1RegistryMutants — seat report (mutation probe of `plans/round52_c2_registry.py`)

Role: UFO-FSD mutation tester, kengaku round 55 wave 1 (v2), scratch-only probe. Production
bytes were never edited in place; every run was against scratch copies under
`/fast/scratch/hyaku/kengaku-r55/M1RegistryMutants/` (deleted after receipts were copied out).

## What was frozen and pinned before mutating

- Claims read first: `plans/round-55-claims.md` (freeze commit `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`).
- Lane HEAD at probe time: `git -C kengaku-shokunin rev-parse HEAD` →
  `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` — exactly the frozen base tip.
- `git -C kengaku-shokunin status --porcelain -- plans/round52_c2_registry.py` → empty
  (worktree clean); file last touched by `434382945c28…` ("round-52: wave-2 evidence…").
- `git clone --shared` of the lane into scratch; `sha256sum` of worktree vs clone copy:
  both `9e6f41a457ec2d847f81d513d30545d982e0a118b4cfa8452af34e1d1a509e6b`.

## Method

Fixture lane builder (SKILL.md registry table + SCORECARD advertisement + `corpus/knowledge/depth.md`
advertisement + `plans/tool_a.py` et al.) produced seven fixtures: one focused fixture per
counter leg plus a combined fixture where every leg fires at once. The detector is the same
bounded behavioral run on pristine, mutated, and restored bytes:
`python3 <counter-copy> --lane <fixture>` → the five defect counts + detail lines + exit code.

Baseline expectations were frozen before any mutation (all matched — baseline conclusive,
so no verdict is inconclusive):

| fixture | pristine exit/MISSING/INCOMPLETE/ENTRY-MISSING/UNBACKED/DUPLICATE |
|---|---|
| f1_missing | 1/1/0/0/0/0 |
| f2_incomplete | 1/0/1/0/0/0 |
| f3_entry_missing | 1/0/0/1/0/0 |
| f4_unbacked | 1/0/0/0/1/0 |
| f5_duplicate | 1/0/0/0/0/1 |
| f6_knowledge | 1/1/0/0/0/0 |
| combined | 1/2/1/1/1/1 |

Kill rule: focused fixture flips exit 1→0 with its family →0 (no other family present), AND
the combined fixture loses exactly that family while every other family keeps the pristine
count (orthogonality).

## Mutants — 6/6 killed

| id | single defect (one per leg, exact byte replacement, occurrences matched = 1) | focused | focused exit | combined family | verdict |
|---|---|---|---|---|---|
| M1-missing-always-empty | `missing = sorted(set(adv) - set(reg))` → `missing = []` | f1_missing | 1→0 | missing 2→0, others unchanged | **killed** |
| M2-incomplete-ignores-blanks | `… if not all(r)]` → `… if not any(r)]` (separator guard already drops fully-empty rows ⇒ blank cells ignored) | f2_incomplete | 1→0 | incomplete 1→0 | **killed** |
| M3-entry-missing-skipped | `entry_missing = sorted(s for s in reg if …)` → `entry_missing = []` | f3_entry_missing | 1→0 | entry_missing 1→0 | **killed** |
| M4-selftest-unbacked-false | `return all(f not in body for f in flags)` → `return False` | f4_unbacked | 1→0 | unbacked 1→0 | **killed** |
| M5-duplicate-check-removed | `duplicate = sorted({n … count(n) > 1})` → `duplicate = []` | f5_duplicate | 1→0 | duplicate 1→0 | **killed** |
| M6-universe-drops-knowledge | `files += sorted(kdir.glob("*.md"))` → `pass` (knowledge/*.md no longer in the advertised universe) | f6_knowledge | 1→0 | missing 2→1 (`plans/kb_tool.py` line vanishes, orphan still caught) | **killed** |

Full per-mutant stdout detail and mutant sha256s: `mutants.md` (same directory) and
`receipts.json`. Example kill evidence, M1 on combined: pristine detail
`[MISSING kb_tool, MISSING orphan, INCOMPLETE-ROW blank, ENTRY-MISSING ghost_tool,
SELFTEST-UNBACKED unbacked, DUPLICATE-ROW dup]` → mutant detail
`[INCOMPLETE-ROW blank, ENTRY-MISSING ghost_tool, SELFTEST-UNBACKED unbacked, DUPLICATE-ROW dup]`.

## Restoration evidence

- Production `plans/round52_c2_registry.py` sha256 after the probe:
  `9e6f41a457ec2d847f81d513d30545d982e0a118b4cfa8452af34e1d1a509e6b` — identical to before;
  the file was never written.
- Re-copied "restored" scratch bytes: same sha256; the detector on restored bytes reproduced
  the pristine combined fingerprint exactly (exit 1, `PREDICATE R52-C2 fail`).

## Coverage finding (no contract change implied)

The counter's shipped `--selftest` battery (3 fixtures: clean / MISSING / INCOMPLETE) catches
mutants M1 and M2 (battery exit 1) but is blind to M3, M4, M5, M6 (battery exit 0). The
ENTRY-MISSING, SELFTEST-UNBACKED, DUPLICATE and knowledge-file legs therefore have no
self-test fixture inside the tool itself; they were demonstrated here only by external
fixtures. Recorded as a finding, not fixed (seats never edit sibling files, and the production
counter is frozen).

## Commands and exit codes

- `mkdir -p <scratch> <outputs>` — ok.
- Read-only git: `rev-parse HEAD`, `log -1 -- <file>`, `status --porcelain -- <file>` — ok.
- `git clone --shared -q <lane> <scratch>/lane` — ok (the contract-sanctioned live clone).
- `python3 harness.py` — first run exit 1 (harness bug: KeyError `comb_delta`; fixed in the
  harness only), second run exit 1 (harness bug: over-strict orthogonality assertion demanded
  combined MISSING stay 2 under M1 — re-labeled M1 "survived" though its exit had flipped;
  assertion corrected, see dead ends), final run exit 0. All six mutants were killed on the
  final run; the two intermediate failures were harness-code defects, never production code,
  and never produced a wrong verdict in a receipt that was kept (receipts overwritten each run).
- Detector subprocesses: ~60 runs of `python3 <counter> --lane <fixture>`, all rc 0/1 as
  fingerprinted above; `--selftest` runs: pristine 0, M1 1, M2 1, M3–M6 0.
- Cleanup: scratch dir deleted after receipts copied (final step of this seat).

## Files written

- `.ufo/waves/round-55/w1/M1RegistryMutants/mutants.md` (per-mutant kill evidence)
- `.ufo/waves/round-55/w1/M1RegistryMutants/receipts.json` (machine receipts: all runs, fingerprints, hashes)
- `.ufo/waves/round-55/w1/M1RegistryMutants/harness.py` (probe driver, receipt copy)
- `.ufo/waves/round-55/w1/M1RegistryMutants/report.md` (this file)
- `.ufo/waves/round-55/w1/M1RegistryMutants.md` (scoped findings summary)

## Defects found

- None in the production counter: no mutant survived; all six advertised legs are
  demonstrated, each flips the observable result on a fixture that exercises it.
- Tool-internal coverage gap (above): `--selftest` battery exercises 2 of 6 legs.

## Dead ends

- First harness draft keyed M1's combined expectation as `comb_missing` instead of
  `comb_delta` (KeyError); fixed.
- Second draft's orthogonality assertion included a redundant `expected_comb_missing` check
  that mislabeled M1 as "survived"; removed — M1's own delta (missing 2→0) plus
  others-unchanged is the correct assertion; verified from receipts that all four other
  families stayed at pristine counts under M1.

## Bounds

No mutating git/jj command anywhere (only `clone --shared` into my scratch; read-only `git -C`
against the lane). No file outside my seat spec + scratch was touched. No tool installs (none
needed). No subagents. Scratch deleted; production bytes hash-verified unchanged.
