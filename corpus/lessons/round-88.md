# Kengaku round 88 — a sixth executed Terminal-Bench 2.0 member, and the Q66 counter-side check made executable

Round 88 (hyaku run 15, attempt 1), 2026-11-05. L1 `KengakuR88`. Lane `kengaku-shokunin`, branch `master`.
Frozen claims: commit `0220c2f9f356bf032bd58b4ed39e32f6e26fa440` (`plans/round-88-claims.md`,
`plans/round88-cases.json`), frozen before any instrument existed. Base `801b903af6412cb424209a60b3a52e56c3532866`.
Instruments: `1f267d4b6f60f1137ebf8b905d318bd2d9894e99`.

Two claims on two distinct surfaces:

- `R88-C1` coverage: one more located offline replay, `fix-git`, by `plans/round88_c1_replay.py`,
  the first `crypto-credential`-class member executed since round 41/80.
- `R88-C2` capability acquisition (no axis-score move, round-82-C3 framing): `plans/round88_claim_figures.py`,
  the executable half of QUALITY.md Q66 routed to this round by the round-87 verifier spot-check
  (`corpus/lessons/round-87-verifier-spotcheck.md`, dated pointer appended below per its routed defect V3).

## Gate

The L1 opened the source below on 2026-11-05 (`curl`, HTTP 200, 1194 bytes) and byte-compared it with the
round-52 capture (`cmp` silent, sha256 `a8a6f51eb0d7c4ebdf0813c8f0b645edf29c995f1f9faf2aca3886a6713043f3`
equal). One new row was appended to `corpus/SOURCES.md`; no existing row's status, recheck or used-by cell
changed. Dated pointer per round-87 spot-check routed defect V3: the non-author spot-check of this lane's
round-87 work is `corpus/lessons/round-87-verifier-spotcheck.md` (committed 801b903a, 2026-11-05); this
round's lesson Gate carries the pointer its V3 defect asked for.

| id and decision | URL | access date | located quote (5 words, ≤25) | reason / flip |
|---|---|---|---|---|
| S277 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/fix-git/tests/test_outputs.py | 2026-11-05 | `assert hash_file(path_a) == hash_file(path_b), (` at line 19 | the grader's md5-pair predicates over `/app` file pairs are the replay's acceptance surface; `hash_file` strips bytes before hashing at :6-9, which the trailing-whitespace case exercises; scope is member replay only |

Census, `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`: exit 0 before
(268 rows) and after (269 rows); rows added by tier: A 1 (S277 admitted). Status: mined 243 → 244,
rejected 17, queued 8 unchanged.

Considerthese: no unimplemented proposal is mined this round. The latest `considerthese/2026-10-26.md`
proposal 2 is Q61's per-entry form, already implemented in round 86; nothing new was taken.

Assimilation: none. `merge/kengaku/` remains blocked by L0 `kengaku | round-54`.

## Claims and their measurements

- **R88-C1 (coverage).** Before (BASE `801b903a`): `TARGET executed_rows=31 member=fix-git located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3`, `PREDICATE R88-C1 fail`, exit 1. Three defects: `L4-table` (table absent at base), `L1-receipt` (receipt absent), `L7-ledger` (row unexecuted). After (measured tip): `TARGET executed_rows=32 member=fix-git located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0`, `PREDICATE R88-C1 pass`, exit 0. Ledger: executed 31 → 32; `crypto-credential` 2 of 12 → 3 of 12; `file-artifact` 23 of 76 → 24 of 76.
- **R88-C2 (capability acquisition).** Before (BASE): the instrument does not exist — `git cat-file -e 801b903a:plans/round88_claim_figures.py` fails. After (measured tip): `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, one `MISMATCH KNOWN R87-C1 kv:defects claimed==7 measured 3`, `DEFECTS n=0`, `PREDICATE R88-C2 pass`, exit 0; `--selftest` prints four `SELFTEST … pass` lines, `PREDICATE R88-C2-SELFTEST pass`, exit 0.

## Controls and battery

Committed before the measured tip is scored (see `.ufo/waves/round-88/L1/`):

- do-nothing controls at BASE (the blocks above);
- the ledger-only and forged-receipt controls against the measured tip (fixtures in scratch clones, transcripts in `.ufo/waves/round-88/L1/controls.txt`);
- the Q66 able-to-fail battery: `--selftest` T1 feeds a doctored claims copy (`defects=7`→`defects=9`) through the same extract+check pipeline and must observe `verdict=mismatch`; T2–T4 pin marker negatives, backward `at BASE` direction and dedupe.

## Mistakes

1. **Class `figure-not-measured`** (routed defects R87-V2/V4, QUALITY.md Q66). Evidence: `plans/round-87-claims.md` asserts R87-C1's BASE figure as `defects=7`; the counter's own BASE output measures `defects=3` (three defects: table, receipt, ledger — the `7` was carried over from the round-86 shape and never measured for this member). Captured-by: none until this round — no criterion re-derived a frozen before-figure from its counter. Fix: `plans/round88_claim_figures.py` extracts every before-figure record from the eight frozen claims files (rounds 80–87), re-runs each claim's counter at its own BASE, and requires the mismatch set to equal the frozen KNOWN set exactly; the mispredict is reported `MISMATCH KNOWN`, not silently passed. Red-before is the round-87 spot-check V2 finding; green-after is `PREDICATE R88-C2 pass` with the `MISMATCH KNOWN` line and a passing `--selftest`.

## Frontier

One source opened and admitted this round (S277, above). The `fix-git` candidate queued in round 87's
lesson ("the next candidate, not admitted") is now executed; no further candidate was opened.

## Wave

<!-- wave results appended after WAVE-DONE -->
