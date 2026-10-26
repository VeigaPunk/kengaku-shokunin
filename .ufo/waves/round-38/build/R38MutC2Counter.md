# R38MutC2Counter — mutation test of `plans/round38_c2_verify.py` (C2 counter)

Seat: R38MutC2Counter (leaf, wave 1, 2026-10-26). Target: the frozen C2 counter's checks V1–V7, one mutant at
a time, on a clone holding a passing package. No frozen file was touched; all mutations lived in my scratch
clone and were byte-restored after each run.

## Setup and baseline

Scratch per operator directive: `S=/fast/scratch/hyaku/kengaku-r38/R38MutC2Counter` (NVMe, `TMPDIR=$S`,
deleted at the end); clone `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`,
toplevel verified `= $S/lane`, clone tip `2c5f4e0`.

Package: the R38PkgEntry drafts were present when I started and were used — `entry.md` →
`corpus/knowledge/tb2-build-pmars-grader.md`, `rows.md` S115/S116 appended to `corpus/SOURCES.md` after the
S114 row, `readme.md` index-row inserted after the `tb2-git-webserver-grader.md` index row and coverage bullet
after the third-task bullet. New files staged index-only (`git add -A` inside my clone only; no commit).

Baseline command (run from `$S/lane`, every counter run in this report used the same command with `--work "$S/w"`):

```
python3 plans/round38_c2_verify.py --lane . --work "$S/w"
```

Output (receipt `baseline.txt`): `V1 ok listed=5`, `V2 ok … gate_exit=0` (gate `P1..P10 ok`, `P10 ok
probe_rerun=byte-equal bytes=5537`), `V3 ok rows=2`, `V4 ok cases=22 mismatches_named=0/0`, `V5 ok
probe=frozen dry_byte_equal=True`, `V6 ok census_exit=0`, `V7 ok rows=7 tags=7`, `checks=7 defects=0`,
`PREDICATE C2 pass`, exit 0 — wall time 1.20 s (the counter is cheap: the P10 fresh probe rerun of 22
bubblewrap cases costs ~1 s on this host).

Mid-run L1 committed the C2 package (`dc0cdb5`); `corpus/SOURCES.md` committed bytes are byte-identical to my
assembled copy (`cec138692f48961d` both, `git -C <lane> show dc0cdb5:corpus/SOURCES.md | sha256sum`), while the
committed entry/README are L1-revised (`e22a82f6434d1664` / `e9d96baeebd39a27`, vs draft `af0af3206e648d61` /
`4caaa05b8d1b4cae`). I therefore re-materialized the committed entry+README into the clone, re-baselined green
(`baseline3-committed.txt`, `checks=7 defects=0`, exit 0) and re-ran every entry/receipt mutant against the
committed bytes; the map region is byte-identical between draft and committed entry, and all six re-runs
reproduced the same DEFECT lines (receipts `m01c…`–`m08c…`, `final-green2.txt` green).

## Mutants — 11 applied, 11 killed, 0 survived

Each row: the mutation, the mutated-file sha256 (first 16 hex), the counter's DEFECT output verbatim, verdict,
and the restored hash. Restoration evidence: after every run the file was copied back from a pristine copy and
re-hashed — every `restored-hash` below equals its pristine/package hash.

| # | Mutation (file, edit) | mut-hash | DEFECT line(s) observed | Verdict | restored |
|---|---|---|---|---|---|
| M1 | entry map row `results-format` label `partly`→`enforced` | `5bb0b7eec924a169` (committed bytes `c9894515f1906954`) | `V7 DEFECT rows=7 tags=7 bad=['results-format: labelled enforced, receipt derives partly']` | killed | `af0af3206e648d61` / `e22a82f6434d1664` ✓ |
| M2 | entry map row `no-x11` cites `results-not-last` (does not violate the tag) instead of `canned-x11-linked` | `e1a11c6c28dbdd72` (`fcc744d497e5ec2a`) | `V7 DEFECT … bad=['no-x11: cites no case or a case that does not violate it']` | killed | ✓ |
| M3 | entry map: `no-x11` row duplicated verbatim | `c3f5b33dd9d9c912` (`1d04c787f10eb0e9`) | `V7 DEFECT rows=8 tags=7 bad=["tags missing=0 duplicated=['no-x11']"]` | killed | ✓ |
| M4 | entry map: `debugger-works` row deleted | `4b3d9ebb543921c7` (`0f09c21210463f62`) | `V7 DEFECT rows=6 tags=7 bad=["tags missing=['debugger-works'] duplicated=0"]` | killed | ✓ |
| M5 | entry map row `results-format` line `instruction.md:7`→`:6` | `2f79c4c6b0822f2f` (`f20abdd571dd4cc8`) | `V7 DEFECT … bad=['results-format: line 6 is not the frozen instruction.md:7']` | killed | ✓ |
| M6 | SOURCES.md S115 anchor token `sha256 d9d2796d…` → S116's digest `16068505…` | `2befb09dcb92024b` | `V3 DEFECT rows=2 bad=['S115:anchor_digest']` | killed | ✓ (see harness fault below) |
| M7 | receipt: one CASE line deleted (`canned-static`) | `617a0375886ddcea` | `V4 DEFECT cases=21 … bad=['case ids differ from the frozen table', 'summary disagrees with the CASE lines']`; `V2 DEFECT … gate_exit=1` (gate: `P10 DEFECT fresh probe output is not byte-equal to the receipt`) | killed | `2408b477b0299e13` ✓ |
| M8 | `match=NO` case not named: receipt `canned-static` `observed=fail`→`pass` + `match=yes`→`match=NO`, and both backticked `canned-static` mentions removed from the entry (lines 160, 201; `grep -c` = 0 after) | entry `8fee617b1293a00e`, receipt `3837251746da16af` | `V4 DEFECT cases=22 mismatches_named=0/1 bad=['summary disagrees with the CASE lines', "mismatch cases not named in the entry: ['canned-static']"]`; `V2 DEFECT` (gate P10 byte-compare) | killed | entry `e22a82f6434d1664` ✓, receipt `2408b477b0299e13` ✓ |
| M9 | spec one byte: `"min_quotes": 8`→`9` | `d4016acfffd5c485` | `V2/V3/V4/V7 DEFECT error ValueError: spec template not at its freeze digest` (4 checks) | killed | `bd9bfe71c1c9cb02` ✓ (frozen digest) |
| M10 | dry table one byte: description byte `stdout`→`stdouT` (parsed TAG/CASE fields untouched) | `33cfac350c1c4970` | `V4 DEFECT error ValueError: dry table not at its freeze digest`; `V5 DEFECT probe or dry table not at freeze digest`; `V7 DEFECT error ValueError: …` | killed | `93b4b60cfe132ffe` ✓ (frozen digest) |
| M11 | probe one byte: docstring `offline.`→`offlinE.` | `200e5fec77fb7165` | `V5 DEFECT probe or dry table not at freeze digest`; `V2 DEFECT … gate_exit=1` (gate: `P1 DEFECT pinned=2 mismatched=['plans/build_pmars_probe.py']`) | killed | `32f0771cd5c4129a` ✓ (frozen digest) |

Composition note on M8: at freeze the receipt has `mismatches=0` and every CASE line is `match=yes`, so a bare
"unnamed match=NO" state cannot exist without first creating a mismatch; the mutant is the minimal pair (one
receipt line flipped to `match=NO` + the entry de-named) so that V4's naming clause, not just the summary
clause, is the thing under test. Both clauses fired.

## Harness fault disclosed (one invalid run, discarded and re-run)

My M6 "restore" copied a pristine `SOURCES.md` snapshot taken **before** the S115/S116 rows were inserted — it
wiped the two registry rows. The first M7 run therefore executed against a broken package and fired V3
spuriously (`bad=['S115:row', 'S116:row']`, receipt `m07-case-deleted.txt`, kept as evidence). That run is
**invalid, not a kill**: a baseline failure is inconclusive. I re-inserted the rows (hash `cec138692f48961d`),
re-baselined green (`baseline2.txt`, `checks=7 defects=0`, exit 0), and re-ran M7 cleanly (`m07b-case-deleted.txt`
above). M1–M5 and M8 ran before the fault and are unaffected; M6's own run was also unaffected (its tree still
had the rows; only its restore was wrong).

## Calibration findings for the L1 (what each kill is made of)

1. **M6: V3 is the sole detector.** With S115's anchor token swapped for S116's digest, the gate (V2) stayed
   green — `c_sources` checks URL/tier/status/used-by/teaches but not the anchor digest — and the census (V6)
   stayed green too. This is routed item D3 doing real work: a round-37-shaped counter without V3 would have
   **survived** this mutant.
2. **M10: V2 is correctly blind to the dry table.** The gate never reads it, so V2 stayed green; the kill is
   carried by V5's digest check plus V4/V7 (both die on the same `ValueError` from `dry()`). The dry pin is
   load-bearing for three checks at once.
3. **M11: two independent detectors, and P10 alone would miss it.** A docstring byte leaves the probe's output
   byte-identical, so gate P10 stayed green; the kill comes from gate P1 (the spec's `frozen_instruments` pin)
   and V5's digest. Digest pins catch what output comparison cannot.
4. **M7/M8: P10 is a second, independent net over the receipt.** Any receipt byte change trips the gate's
   fresh-run byte-compare in addition to V4's structural checks — matching the claims file's note that V2's P10
   is what makes a hand-typed receipt red.
5. **M9: a spec byte kills 4 of 7 checks simultaneously** (V2/V3/V4/V7, same `ValueError`) — redundant, so no
   single-check fragility.
6. **V7's clause coverage:** M1–M5 exercised five distinct V7 failure messages (label≠derived, bad citation,
   duplicate, missing, wrong line); the `label != want` clause is direction-agnostic, so a flip to `unenforced`
   dies by the same clause as M1. `derive()`'s three branches are all reachable at freeze (all 22 cases carry
   four tags; `no-x11`/`install-path`/`results-format` have narrow violating sets), and M8 confirmed a
   verdict-flip on a non-map-cited case leaves V7 correctly green (the flipped case's tags were already `partly`
   via other passing violators, e.g. `canned-shape`).

## Evidence, restoration, and bounds

- Every counter run's full stdout/stderr is preserved: `baseline.txt`, `baseline2.txt`, `m01…m11` (first pass),
  `m01c…m08c`, `baseline3-committed.txt`, `final-green.txt`, `final-green2.txt` — 23 files under
  `.ufo/waves/round-38/build/R38MutC2Counter/`. Final state after all restorations: `final-green2.txt` →
  `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0.
- Restoration: every mutated file re-hashed after restore and matched its pristine/package digest (per-row ✓
  above; full digests in the run receipts). Scratch clone then deleted.
- The lane was never written: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain` shows
  only other seats' `.ufo/waves/round-38/*` artifacts and `corpus/lessons/round-38.md` (7 lines, none mine);
  lane HEAD moved `2c5f4e0`→`d93b7d6` by L1 commits (`dc0cdb5` C2 package), not by me. No git
  add/commit/stash/checkout/reset/push/pull ran in the lane; only index-only `git add` inside my clone.
- Tooling: nothing installed or upgraded (no need — host python3, gcc, bwrap sufficed); no pacman transaction.
- Limits: mutants are one-per-claim as tasked; I did not fuzz beyond the 11 (e.g., no `unenforced`-direction
  flip, no `partly`↔`unenforced` swap — same clause as M1); the counter's `--work` default (`/tmp`) was never
  used (`--work "$S/w"` throughout).

VERDICT: c2-mutants-11/11
