# R34 MutC1Counter — mutation test of the C1 counter selftest

Seat: `R34MutC1Counter` (mutation-tester, leaf). Target:
`kengaku-shokunin/.ufo/waves/round-34/build/R34C1CounterDraft/round34_c1_verify.py`
(142 lines; selftest = 1 green fixture + 8 red fixtures V1–V8).
Scratch: `kengaku-shokunin/.ufo/waves/round-34/build/R34MutC1Scratch/`.
No tool installs were needed (python3, stdlib only) — no tooling records.

## 1. Baseline (pristine bytes) — SELFTEST FAILS

Command:
```
cd .../R34MutC1Scratch
python3 orig_round34_c1_verify.py --selftest
```
Output:
```
SELFTEST FAIL: red V5 fixture passed
EXIT=1
```
Baseline copy hash: `f3a90d1331766531c7331bd593fe1d38114252cf2a9107362d7f39daa69e577e`
(identical to the lane draft file, which stayed untouched throughout; re-hashed after all runs).

**Root cause (verified, not inferred):** red fixture idx=4 replaces only the *first* PIN
occurrence in the fixture README (`replace(PIN, "badpin", 1)`), but the fixture README
contains the PIN twice — once in the discharge line, once in the frontier bullet. V5 is:
```
re.search(r"(?is)Benchmark grader semantics.*?Terminal-Bench.*?protein-assembly.*?" + re.escape(PIN), readme)
```
`(?is)` enables DOTALL, so `.*?` after the discharge line's “protein-assembly” spans the
newlines and reaches the frontier bullet's surviving PIN. Standalone replication:
```
python3 -c "..."   # V5_on_tampered_README = True; PIN_occurrences_after_tamper = 1
```
So V5 still passes on the tampered README → the red V5 fixture can never fail → the
selftest aborts at idx=4 on every run.

Per the mutation-tester contract, a failing baseline makes every mutant result
**inconclusive**, and the single-fail abort at red V5 also preempts evaluation of the
later red fixtures (V6–V8) in every run.

## 2. Mutants (5), each = baseline copy + one smallest behavior-bearing change

| # | mutation | diff vs baseline | hash |
|---|----------|------------------|------|
| M1 | delete V1's id-set check (`set(cited_ids) == set(IDS)`) | line 32 shortens to `len(cited_ids) == 3 and len(set(cited_ids)) == 3` | `cdd84c18304757d3de70da06c52c83a60a213aec108c9ef9b2c8d771059de73c` |
| M2 | make V3 accept any status (drop `"status=mined" in lines[0]`) | line 37 | `87c74c1a9e71534d01fd3853ec0d5c80f26797ebfb59362790e389e510576aa9` |
| M3 | replace V5's discharge-sentence regex with substring `Benchmark grader semantics` | line 40 | `976736e939072c68d16a8bad1069b6b370c15d4406d179c52e942ad407d40fbf` |
| M4 | make V7 accept missing control (`(not control_path.is_file()) or (…checks)`) | line 46 | `5c774263efa71b4d6abf36969ffe1a0d5eb4b411889c8b91810d6f4cee6fbe19` |
| M5 | make V8 skip the sha check (`v8 = sums_path.is_file()`) | line 50 | `0fa997aca2090fff9da3b7217642231d06a77b197c57447f25640d2a71e2fe79` |

## 3. Detector runs (`python3 mutant_mX_round34_c1_verify.py --selftest`)

| mutant | observed output | exit | vs baseline |
|--------|-----------------|------|-------------|
| M1 | `SELFTEST FAIL: red V5 fixture passed` | 1 | byte-identical → indistinguishable → survivor |
| M2 | `SELFTEST FAIL: red V3 fixture passed` | 1 | differs (aborts at V3) → the V3 fixture detects the loosened V3 → killed-observable |
| M3 | `SELFTEST FAIL: red V5 fixture passed` | 1 | byte-identical → indistinguishable → survivor |
| M4 | `SELFTEST FAIL: red V5 fixture passed` | 1 | byte-identical → indistinguishable → survivor |
| M5 | `SELFTEST FAIL: red V5 fixture passed` | 1 | byte-identical → indistinguishable → survivor |

Notes:
- M2 is the only mutant whose output differs from baseline: the dedicated red V3 fixture
  correctly flags that V3 passes despite `status=unopened`; the harness aborts there and
  never reaches the broken red V5. This is a genuine kill of the M2 defect (the detector
  catches it; the run still exits 1 only because of the separate baseline defect).
- M1: even with the id-set clause deleted, red V1 would still catch the 2-id fixture via
  `len(cited_ids) == 3`; the mutation removes a clause the fixture does not specifically
  exercise. Indistinguishable as-run.
- M3: any substring surviving in the tampered README ("Benchmark grader semantics",
  "Terminal-Bench", "protein-assembly", or the frontier-line PIN) yields the same V5=True,
  so M3 is robustly indistinguishable from baseline.
- M4: red V7 (97→96, file present) still fails under “accept missing”, so the mutation is
  not exposed by its own fixture; indistinguishable as-run.
- M5: the V8 sha-skip is never reached because the run aborts earlier at red V5;
  indistinguishable as-run.

## 4. Restoration / integrity evidence

- Lane draft file `R34C1CounterDraft/round34_c1_verify.py` hash before and after all runs:
  `f3a90d1331766531c7331bd593fe1d38114252cf2a9107362d7f39daa69e577e` — unchanged.
- All five mutants and the pristine copy remain in scratch (`R34MutC1Scratch/`), hashes in
  §2; scratch is declared disposable by the tasking. No other files were touched; nothing
  was written outside `.ufo/waves/round-34/`.

## 5. Coverage findings (deliverable)

1. **The C1 counter's selftest is itself defective**: the red V5 fixture cannot fail, so
   `--selftest` exits 1 on pristine bytes and never validates V5's discharge-sentence
   requirement. On the real lane tree this means V5 would print green even if the README's
   coverage bullet lost its pin, as long as the frontier bullet carries the pin — the
   claimed “coverage discharge names task and pin” predicate is not actually enforced in
   that case (V6's `PIN in ftext` check is separate and would still catch the missing
   frontier pin, but V5's own sentence is unverified).
2. **Single-fail abort masks later fixtures**: the harness returns on the first red fixture
   that passes, so V6–V8 red fixtures are unreachable whenever an earlier fixture is
   broken; M5's sha-skip (a real detection hole) is invisible to the current run.
3. Per the contract, baseline failure ⇒ all results formally inconclusive; the only
   observable delta is M2 (killed by its own fixture).

VERDICT: mut-c1counter (killed 1/5 [M2], survivors 4/5 [M1, M3, M4, M5] — baseline selftest itself fails at red V5)
