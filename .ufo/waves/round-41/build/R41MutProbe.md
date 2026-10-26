# R41MutProbe — mutation test of `plans/constraints_probe.py` and its receipt (round 41, wave 1)

2026-10-26. Leaf seat; no subagents. Nothing frozen was touched: every mutation was applied to a copy inside
`/fast/scratch/hyaku/kengaku-r41/R41MutProbe/lane` (shared git clone of the lane at tip `fc79f2a`), run, and
restored byte-exact (§Restoration). All counter/battery/probe runs used the host-safety envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent …`.
Scratch was removed at the end; evidence outputs are preserved under `build/R41MutProbe/runs/`.

Question asked by the tasking: do the counter's checks — **V2 (gate `--rerun`, whose P10 re-runs the probe and
compares stdout byte-equal to the receipt), V4 (receipt internal consistency + carried-mismatch naming), V5
(probe+dry digests and `--dry` byte-equal)** — catch mutants of (a) a case's meeting text or edit, (b) the
harness verdict mapping, (c) the grader capture (copy), and (d) the receipt itself? Plus: does the probe's
`match=` column compare letters exactly?

## 1. Baseline (pristine scratch lane)

- Probe rerun, direct: `python3 plans/constraints_probe.py --lane $S/lane --work $S/w` → rc=0, 25 s, output
  **byte-equal** to `corpus/evidence/round41/constraints-probe.txt` (`diff -q` clean; `base-driver.out`).
- Frozen counter full run: `python3 plans/round41_c2_verify.py --lane $S/lane --work $S/w` →
  `checks=8 defects=3`, `PREDICATE C2 fail`, rc=1 (`base-full.out`). The 3 are **wave-1-pending integration**,
  not lane defects: `V3 DEFECT rows=2 bad=['S122:row', 'S123:row']` and `V7 DEFECT no '## Requirement map'
  section` (SOURCES rows and the knowledge entry are not landed at tip `fc79f2a`), plus V2 only because the gate
  fails on the same absent pieces (gate `P3 DEFECT no '## Located quotes' section`, `P4`, `P6`, `P7`, `P8`).
  The trio I judge is green at baseline:
  - `V5 ok probe=frozen dry_byte_equal=True`
  - `V4 ok cases=25 mismatches_named=2/2 bad=0`
  - `gate: P10 ok probe_rerun=byte-equal bytes=5775`
- Disclosed stand-in: so V4 could exercise its naming rule before the L1 lands the entry, I staged a 3-line
  `corpus/knowledge/tb2-constraints-scheduling-grader.md` **inside the scratch clone only** (content: the two
  carried mismatch ids in backticks; labeled STAND-IN). It exists nowhere else and died with the scratch. All
  mutant verdicts below are deltas against this baseline.
- Host note (provenance): `python3 -c "import Bio"` fails on this host, so gate P10's rerun took its
  `uv run --no-project --with biopython==1.85 python3` branch (`uv` at `~/.local/bin/uv`, ro-bound in the
  envelope). Baseline P10 still reports byte-equal, so the branch is verdict-neutral here.

## 2. Mutants and detection

Protocol per mutant: copy variant over the live file in the scratch clone → record mutated sha256 → run the
counter checks via a driver (`runs/mprobe.py`) that imports the **frozen** counter module and calls `v5`, `v4`,
`v2` in that order (v2 prints the gate's own `P…` lines) → restore pristine bytes → verify sha256. A check line
`DEFECT` = caught. Full outputs: `runs/pm1.out … pm6.out, CM1.out, CM2.out, RM1.out, RM2.out`.

| id | surface | site | mutation (old → new) | mutated sha256 | V2 / gate P10 | V4 | V5 | caught |
|----|---------|------|----------------------|----------------|---------------|----|----|--------|
| PM1 | case meeting text | probe:141 | `later-valid-wed-1105` meeting `…110500Z/…120500Z` → `…110000Z/…120000Z` | `4128904e…` | P10 DEFECT `not byte-equal` | ok | DEFECT (digest) | yes |
| PM2 | case edit | probe:226 | `alice-append` `fh.write("\n")` → `fh.write("")` | `48030be8…` | P10 DEFECT `not byte-equal` | ok | DEFECT (digest) | yes |
| PM3 | verdict mapping | probe:277 | `overall`: `letters == "P" * len(TESTS)` → `letters[0] == "P"` | `fdda3587…` | P10 DEFECT `not byte-equal` | ok | DEFECT (digest) | yes |
| PM4 | harness letters | probe:211 | AssertionError branch prints `F` → `P` | `8991eacc…` | P10 DEFECT `not byte-equal` | ok | DEFECT (digest) | yes |
| PM5 | match= compare | probe:351 | `match = letters == c.predicted` → `letters[0] == c.predicted[0]` | `6cd66a07…` | P10 DEFECT `not byte-equal` | ok | DEFECT (digest) | yes |
| PM6 | probe comment (behavior-preserving) | probe:365 | `if __name__ == "__main__":` → `…:  # mutated` | `21083d82…` | **P10 ok byte-equal** | ok | **DEFECT (digest)** | yes, V5 only |
| CM1 | grader capture copy | test_outputs.py:112 | expected title `"SUMMARY:Team Planning Meeting"` → `"…Meetng"` | `58de70a2…` | P10 DEFECT `fresh probe exit=2 stderr='SETUP capture test_outputs.py missing or not at its pinned digest'`; gate P5 DEFECT (manifest≠bytes); counter **V1 DEFECT** `bad=['test_outputs.py']` | ok | ok | yes |
| CM2 | input calendar copy | alice_calendar.ics:9 | Alice Mon `DTSTART:20240115T100000Z` → `…100500Z` | `08a45331…` | P10 DEFECT `exit=2 stderr='SETUP capture alice_calendar.ics …'`; gate P5 DEFECT | ok | ok | yes |
| RM1 | receipt | receipt:7 | `CASE nop … observed=fail` → `observed=pass` (tests=FFF kept) | `7f17e1c9…` | P10 DEFECT `not byte-equal` | **DEFECT** `summary disagrees with the CASE lines` | ok | yes |
| RM2 | receipt | receipt:10 | `later-valid-wed-1105` `match=NO` → `match=yes` | `24a2ea6e…` | P10 DEFECT `not byte-equal` | **DEFECT** `summary disagrees with the CASE lines` (`mismatches_named=1/1`) | ok | yes |

**10/10 caught.** V2's P10 caught every behavior-bearing mutant (8 of 8 that change rerun stdout or rerun
success); V5's digest pin caught all 6 probe mutants including the behavior-preserving one; V4 caught both
receipt mutants via its summary arithmetic. No survivor, no invalid, no null detection (PM6 is not equivalent —
it changes the frozen instrument's bytes, which V5 pins).

Behavioral confirmation that the probe-source mutants really bite (fresh outputs, not just byte-diffs):

- PM1 (`runs/PM1-direct.out`): `CASE later-valid-wed-1105 … tests=PFF … observed=fail` → `tests=PPP observed=pass`;
  summary `observed_pass=6 observed_fail=19` → `7/18`.
- PM3 (`runs/PM3-direct.out`): every case whose S-test passes flips to `observed=pass` — summary
  `observed_pass=6 observed_fail=19` → `13/12` (13 cases have `tests` starting with `P`).
- CM1/CM2: the probe's own `PINS` digest gate stops the run before any case (stderr quoted in the P10 lines).

## 3. Full-counter demonstration (CM1)

`python3 plans/round41_c2_verify.py --lane $S/lane --work $S/w` with the CM1 capture mutant in place:
`checks=8 defects=4`, `PREDICATE C2 fail`, rc=1 — delta vs baseline `defects=3` is exactly `V1 DEFECT
bad=['test_outputs.py']` plus the flipped gate `P5`/`P10` lines (`runs/CM1-full.out`).

## 4. Does `match=` compare letters exactly?

**Yes — exact, order-fixed, case-sensitive full-string equality.**

- Code: `letters = "".join(got[t][0] for t in TESTS)` (probe:345) vs `match = letters == c.predicted`
  (probe:351); the harness prints exactly one-char tokens `P` / `F` (`HARNESS_PY`, probe:206-213), so
  `got[t][0]` is the whole verdict, and the SETUP guard rejects predictions that are not `{P,F}^3`
  (`set(c.predicted) - {"P","F"}`, `len(c.predicted) != len(TESTS)`, probe:293).
- Receipt cross-check (all 25 CASE lines): `tests==predicted_tests` ⟺ `match=yes` holds with zero
  inconsistencies; tokens are exactly `{yes, NO}`; `match=NO` only on the two carried mismatches
  `later-valid-wed-1105`, `seconds-30`.
- Mutation evidence: PM5 (prefix compare) would flip exactly those two cases — both are `PPF` predicted vs
  `PFF` observed, identical at position 0 — silently zeroing `mismatches` in the rerun; the counter still catches
  it (P10 byte-unequal + V5 digest). RM2 shows the receipt-side twin: a lying `match=` column in the receipt is
  caught by V4's `mismatches`-arithmetic and by P10. One-way-check note: V4's naming rule only demands that
  mismatching cases be named in the entry; a named case that stops mismatching is not itself flagged (RM2 shows
  `mismatches_named=1/1` on the mutated receipt) — the arithmetic is what fires.

## 5. Findings (coverage/calibration, for the integrator)

1. **P10 alone is blind to behavior-preserving probe edits** (PM6: rerun byte-equal). Detection there rests
   entirely on V5's `PROBE_SHA256` pin — correct by design, worth keeping in mind if anyone ever argues the
   rerun subsumes the digest.
2. **V4 and V5 are both blind to capture mutants** (CM1/CM2: `V4 ok`, `V5 ok` — V5's `--dry` path never checks
   captures). Capture integrity is carried by three independent layers: counter V1 (digest table), gate P5
   (manifest vs bytes), and the probe's own `PINS` front door that turns a mutated capture into `P10 DEFECT
   exit=2`. Redundant, but each layer alone would suffice — no gap.
3. **V4's naming check is one-directional** (named-but-no-longer-mismatching is unflagged); the summary
   arithmetic (`mismatches` vs counted `match=NO`) is the actual invariant that caught RM2. Fine as built; do
   not cite "mismatches_named=n/n" alone as proof a receipt's mismatch set is honest.
4. Probe mutants keep V4 green in every case (V4 only reads the committed receipt) — receipt-vs-rerun drift is
   exclusively V2/P10 territory. The trio is non-overlapping and jointly exhaustive over the surfaces probed.

## 6. Restoration evidence

Final sweep over the scratch clone after all runs (`sha256sum` vs frozen digests): probe `8c471fbd…` OK,
receipt `c5aa6742…` OK, test_outputs.py `1422b345…` OK, alice_calendar.ics `5a5d4580…` OK, dry table
`a656ce9b…` OK, counter == lane counter OK, gate `ea638822…` OK, spec `8e96421d…` OK;
`git status --short` empty except the staged STAND-IN entry (`A  corpus/knowledge/…`), which is the disclosed
scratch-only fixture. Per-mutant `RESTORED_OK` lines were asserted after every run (mutated digest ≠ frozen
digest before, = after). The real lane at `/home/vgpnk/Projects/shokunin/kengaku-shokunin` was never written.

Incidental disclosure: one stray `cp … /tmp/x` (a byte copy of a frozen capture) was created and deleted in the
same session; `/tmp` was otherwise never used (operator directive honored everywhere else).

## 7. Limits

- Baseline `defects=3` (V2, V3, V7) reflects wave-1 pieces not yet landed at tip `fc79f2a` (SOURCES rows
  S122/S123, the knowledge entry, README row/bullet); all verdicts are deltas against that disclosed baseline.
- The STAND-IN entry satisfies V4's naming rule only; V7 was left red by design (its requirement map is the
  L1's deliverable, not mine).
- P10's rerun ran under the gate's `uv run --with biopython==1.85` branch (host `import Bio` fails); uv resolved
  from cache inside the envelope. A hermetic host would pin this branch explicitly.

VERDICT: probe-mutants-caught-10/10
