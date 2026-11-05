author: kengaku (L1 KengakuR93, hyaku run 15 attempt 1)

# Kengaku round 93 — lesson (fresh start)

Lane `kengaku-shokunin`, branch `master`. Base `28e9f8bf`; instruments P1 `17cb9337`; pre-freeze
controls P2 `0e77e98f`; frozen claims F `d8d0a4b8` (`plans/round-93-claims.md`, with the
`frozen-instruments` sha256 table); official receipt, ledger flip and SOURCES rows C `22972a31`
(the measured tip for both counters). L1 receipts: `.ufo/waves/round-93/L1/`; wave evidence:
`.ufo/waves/round-93/w1/`.

## Fresh-start reading (rounds 90–92, all `rejected-honest-stop`)

Read before declaring: MANIFEST indices 1333 (r90), 1342 (r91), 1361 (r92) and the three
verifier spot-checks. The shared root failure: instruments edited after the freeze or after the
first scored run (r92 C2/C3: critic P1, lesson M8; r91 C3: selftest outside the predicate path),
plus a control the host could not reproduce (r92 M13, absolute `/usr/bin/bwrap`). This round's
order (P1 instruments → P2 executed controls → F table → receipt → measurement) and the C2 gate
are the answer to the first; the injectable `--bwrap` in both new counters is the answer to the
second.

## Round-92 spot-check routed defects — disposition

| # | routed defect (round-92 spot-check §6) | round-93 disposition |
|---|---|---|
| 1 | freeze-hash check with a red-before witness (M8) | **claimed (R93-C2)**: `plans/round93_freeze_integrity.py`; red-before = W1 on the real r92 history (broken=3) and battery B02/B03; forgeries caught at P2 |
| 2 | override-branch vacuity in `plans/round92_burndown.py:306-329` | not claimed; still open at `22972a31` (file unchanged since `1df76536`); routed to round 94 |
| 3 | planted-marker battery skip (`:445`, `:558`) | not claimed in that gate; the new gate is built without the channel (battery in-process, no marker, no child) — the old gate's skip stays open, routed |
| 4 | pin the three round-92 counters in `plans/counter-pins-r91.json` | not claimed; superseded in kind for round-93 instruments by the frozen table (the freeze commit is the pin), the round-92 counters stay unpinned, routed |
| 5 | `sandbox-red` control must be injectable (M13) | met by construction: `--bwrap` in `plans/round93_c1_replay.py` and the probe; control `controls/c1-sandbox-red.txt` rc 2 at P1 |
| 6 | unguarded sibling `cost_model_for_tests.py` (ScoutS283 F1) | not claimed; routed |
| 7 | WAVE-DONE addressing after a relaunch | operator-owned (L0 `kengaku | round-92`); this round had one attempt |

No disagreement was recorded in the round-92 spot-check §4 (all four sampled decisions agreed), so
no discernment criterion is owed from it.

## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened
here; every fetch HTTP 200 on 2026-11-05 from raw.githubusercontent.com at `2fd12b88aafdd04a52c298e3940bcb189f9766d6`).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S290 `schemelike-metacircular-eval/tests/test_outputs.py` (member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200, 6823 B, sha256 `fbb84e3c…be7ed`, byte-identical to the lane capture | line 121: `def test_interp():` (2 words) | the single function the replay grades; its 10 s/60 s subprocess timeouts and its trailing-True normalization decide every case vector | a claim about the TB2 harness or a real submission needs its own receipt |
| S291 `tests/interp.py` (member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200, 17578 B, sha256 `efb8b5cd…ea2c1`, identical to `environment/tests/interp.py` | line 381: `env.define("newline", lambda: print())` (3 words) | both comparison sides run it; staged unmodified | an interpreter-version claim would need a new fetch |
| S292 `solution/solve.sh` (member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200, 11910 B, sha256 `e2c5b0ac…10512` | line 4: `cat <<'EOF' > eval.scm` (4 words) | the reference eval.scm: positive control C01 (63/63) and the base of C04/C05/C08 | — |
| S293 the 63 test programs (dataset, member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200 ×63; sorted manifest digest `227d7bd1…be8f` | `tests/test/01-factorial.scm:1`: `;; Test 1: Factorial - Classic recursive function` (8 words) | the population the grader globs; shadow_test/ defeats memorized outputs | — |
| S294 `tests/test.sh` (verifier wrapper) | **reject** | 2026-11-05, HTTP 200, sha256 `4770437e…c334` | line 3: `# Install curl` (3 words) | network installs (apt-get, uv) forbidden by the offline replay; no grader semantics beyond S290 | a verifier-harness claim with the network legs pinned |
| S295 `financial-document-processor/tests/test_outputs.py` (member candidate) | **reject** | 2026-11-05, HTTP 200, 10336 B, sha256 `978f506a…f5a9a` | line 14: `digest = hashlib.file_digest(f, "sha512")` (4 words) | full pass needs the 17 pinned-digest documents (~4.2 MB) and pandas (absent on host) | capture the documents and supply pandas offline |
| S296 `large-scale-text-editing/tests/test_outputs.py` (member candidate) | **reject** | 2026-11-05, HTTP 200, 8935 B, sha256 `f5e69f4f…cd43` | line 170: `cmd = ["vim", "-Nu", "NONE", "-n", "-Es", str(INPUT), "-S", str(APPLY_SCRIPT)]` (10 words) | two of five test functions run vim; vim is absent and pacman is paused | vim through an official channel |

Round-start census: exit 0, `kengaku ok`, 281 registry rows (30 pre-existing W04 duplicate-url warnings) (`.ufo/waves/round-93/L1/census-start.txt`).
Round-end census: see the report.

## Mistakes

Class · evidence pointer · captured-by · fix.

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | **mechanism-derived prediction (wrong twice)** | draft case C05 (`(newline)(display "True")` suffix) was designed to show the one-True strip passing 60 of 63; dry run 1 observed `F,0,63,63,0` (`.ufo/waves/round-93/L1/dryrun-1.txt`). Its successor C08 (bare suffix) was predicted `F,60,3,63,0` from the same stacking hypothesis; dry run 2 observed `F,56,7,63,0` (`dryrun-2.txt`; y_combinator ×2 also fail) | the pre-freeze dry-run rule (a vector enters the frozen table only after a scratch run shows it) | both vectors frozen as observed, with the refuted hypotheses written into the case `why` text and the claims file; mechanism is not frozen, only the vector. Shown able to fail: the 60/3 prediction itself went red in dry run 2 |
| M2 | **post-freeze instrument edits invisible to the lane (round 92, carried)** | round-92 lesson M8; this round's W1 measures it: `INSTRUMENT plans/round92_c2_conformance.py … touched=4 verdict=broken`, `round92_burndown.py … touched=3`, `round91_counter_pin.py … touched=1`, `FREEZE-INTEGRITY instruments=4 intact=1 broken=3` (`controls/c2-real-at-P1.txt`) | none until this round | `plans/round93_freeze_integrity.py` (R93-C2). Shown able to fail: W1 rc 1 on real history, battery B02/B03/B05, and four forgeries red at P2 |
| M3 | **exit-code collision (counter design)** | the first C1 counter draft returned `could-not-evaluate` rc 2 at BASE because the absent probe file made `python3` itself exit 2, the same code the probe uses for a setup defect (scratch run before P1) | the do-nothing control run before P1 | the counter checks the probe exists at the revision before re-running it (absent → L6 fail, rc 1). Fixed before P1, so every committed control ran the fixed bytes; shown able to fail: `controls/c1-base.txt` rc 1 with all nine legs red |

## Honest limits of this round's evidence

- The C1 replay grades lane-staged inputs against the captured grader bytes on this host's
  Python 3.14.8 (the TB2 image uses Python 3.13 under pytest); it says nothing about the harness
  or a real agent submission. The grader is called directly, not through pytest; a returning
  `test_interp()` is counted as `P`, which is what pytest would also report (C07's return value 1
  only raises a pytest warning).
- C06's timing wall depends on host speed: `fib 35` in the interpreted language must not finish
  in 60 s. On this host it does not; a much faster host could flip C06.
- The freeze-integrity gate trusts the lane's git history. A rewritten history (force push)
  defeats it; the remote and the closure's ancestry checks are the outer guard
  (considerthese 2026-11-05 proposal 2, root of trust, is related and not implemented).
- C2's W1 expected values come from the round-92 closure's own re-measurement and were
  re-observed by the gate at P1 before the freeze; they are history, not a prediction.
