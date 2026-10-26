# F37MutProbeCases — mutation-testing the git-webserver probe receipt's discriminating power

kengaku round 37, wave 2 (falsify), 2026-10-26. Lane tip `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5` (branch master).
Target: frozen receipt `corpus/evidence/round37/git-webserver-probe.txt` produced by frozen probe
`plans/git_webserver_probe.py` (22 cases). Question: does each case's verdict depend on its distinguishing
server feature, so the receipt changes exactly where the prediction says it should?

## Axes (godspeed)

1. **Coverage** — mutants across all three server modes (`files`, `catchall`, `sequence`), both tools (`curl`, `wget`), both flip directions (pass→fail, fail→pass), plus no-change controls.
2. **Calibration** — every receipt delta must touch exactly the target case line + its grader-stdout line + the summary line, with the flip direction and stdout text the cited grader line predicts; zero cross-contamination.
3. **Restoration** — pristine/mutated/restored receipt legs on identical bytes; lane untouched.

## Method

Scratch only: `S=/fast/scratch/hyaku/kengaku-r37/F37MutProbeCases` (NVMe, `TMPDIR=$S`, deleted at end).
Clone: `git clone -q --no-local <lane> "$S/fx/lane"; git -C "$S/fx/lane" checkout -q 357deceb…` —
`rev-parse --show-toplevel` = `$S/fx/lane`, `rev-parse HEAD` = `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`,
`status --porcelain` = 0 entries. Every probe run used `--lane "$S/fx/lane"` (my clone, never the lane).

Detector = the probe's own receipt, run three ways per mutant:

```
python3 <copy>/git_webserver_probe.py --lane "$S/fx/lane" --work "$S/out/wk<k>"   # TMPDIR=$S
```

- **Pristine leg:** `python3 $S/fx/lane/plans/git_webserver_probe.py --lane $S/fx/lane --work $S/out/wk0` → rc=0, 52.75 s, `cases=22 observed_pass=9 observed_fail=13 mismatches=0`; `diff -u corpus/evidence/round37/git-webserver-probe.txt pristine.txt` → **byte-identical** (`IDENTICAL-TO-FROZEN`). Probe sha256 `63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf`.
- **Mutated leg:** 14 single-point edits, each a fresh copy of the pristine probe with exactly one server-dict token changed in the `CASES` table (captures, `PINS`, harness, `SERVER_PY` untouched — every mutant run still validated the three capture digests, rc=0, no `SETUP` lines). Mutants ran in parallel batches of 4 (bwrap 0.13.1, private netns per case; no host-port coupling).
- **Restored leg:** pristine probe re-run after all mutants (`R1`) → rc=0, `cases=22 observed_pass=9 observed_fail=13 mismatches=0`, `diff pristine.txt R1.txt` empty (**R1-IDENTICAL**).

## Mutants and verdicts

All 14 as predicted. "Δ" = receipt diff vs pristine (archived as `K<k>.diff`); every flipping mutant's Δ is exactly 3 lines (1 CASE line, 1 grader-stdout line, 1 summary line); every control's Δ is empty.

| Mutant | Single-point mutation (CASES table only) | Predicted receipt delta | Actual | Verdict |
|---|---|---|---|---|
| K1 | `token-in-body` body `TEST PASSED\n` → `TEST PASSE\n` | pass→fail; `Content: TEST PASSE`; `Got: 'TEST PASSE'` | exactly that, Δ=6 lines | as predicted |
| K2 | `status-then-content-split` responses swapped → `[[200, HW], [200, "not the content\n"]]` | pass→fail; `Content: not the content` | exactly that, Δ=6 | as predicted |
| K3 | `slow-server-3s` `delay: 3` → `0` | no change (receipt is timing-free; verdict insensitive to delay) | Δ=0, byte-identical | as predicted |
| K4 | `capitalised` body `Hello World\n` → `hello world\n` | fail→pass; success stdout | exactly that, Δ=6 | as predicted |
| K5 | `http-500-right-body` `status=500` → `200` | fail→pass; success stdout | exactly that, Δ=6 | as predicted |
| K6 | `not-found` `routes: {}` → serves `[200, HW+"\n"]` at `/hello.html` | fail→pass | exactly that, Δ=6 | as predicted |
| K7 | `wrong-port-8081` `port=8081` → `8080` | fail→pass; HTTP 000 → 200 success | exactly that, Δ=6 | as predicted |
| K8 | `wget-token-in-body` body → `TEST PASSE\n` | pass→fail on the wget branch; `Got: 'TEST PASSE'` | exactly that, Δ=6 | as predicted |
| K9 | `wget-404` `routes: {}` → serves `/hello.html` | fail→pass on the wget branch | exactly that, Δ=6 | as predicted |
| K10 | `trailing-newlines` body `HW+"\n\n\n"` → `HW+" \n\n"` (space hidden among newlines) | pass→fail; `Got: 'hello world '` | exactly that, Δ=6 | as predicted |
| K11 | `first-request-404` first response `[404, ""]` → `[200, HW+"\n"]` | fail→pass; success stdout | exactly that, Δ=6 | as predicted |
| K12 | `catch-all-200` `body` → `"not hello\n"` | pass→fail; `Got: 'not hello'` | exactly that, Δ=6 | as predicted |
| K13 | `no-server` `{}` → `files(HW+"\n")` | fail→pass; HTTP 000 → success | exactly that, Δ=6 | as predicted |
| K14 | `exact-no-newline` `files(HW)` → `files(HW+"\n")` | no change (single trailing newline stripped by command substitution) | Δ=0, byte-identical | as predicted |

Example calibration evidence (K1, `K1.diff`, archived): removed line `CASE token-in-body … observed=pass match=yes`, added `CASE token-in-body … observed=fail match=NO`, grader-stdout `Content: TEST PASSE` and `Got: 'TEST PASSE'`, summary `cases=22 observed_pass=8 observed_fail=14 mismatches=1`. All other 21 CASE lines byte-unchanged in every mutant.

## Findings

1. **The receipt discriminates.** 12/12 verdict-flipping mutants flipped exactly at their target case, in the direction and with the exact grader-stdout text the case's cited grader line predicts (e.g. K5's flip confirms "the status must be exactly 200 even when the body is right"; K2's confirms the first request's body is never compared; K8/K9 confirm the wget branch mirrors curl's). No mutant changed any other case line — the 22 cases are behaviorally independent at receipt granularity.
2. **Two cases are receipt-insensitive to their distinguishing feature — as the claims already disclose.** K3 (delay 3→0) and K14 (exact→trailing newline) leave the receipt byte-identical: the receipt is deliberately timing-free and newline-normalizing, so those two features are only evidenced by the frozen case table in `plans/git_webserver_probe.py` (checked by the C2 verifier's P5 `--dry` byte-compare), not by the receipt line alone. For `slow-server-3s` the pass verdict still carries information the delay-0 run lacks — it rules out a harness timeout at ≥3 s scale (a timeout would change rc and print a `SETUP` line) — but the delay itself is not receipt-detectable. This is a coverage note, not a defect: the requirement strings state the mechanism, and the frozen source carries the configuration.
3. **Mutation surface is clean.** All mutations were confined to the probe's `CASES` table; the pinned captures (`test_outputs.py`, `verify.sh`, `instruction.md`) were re-digest-validated on every mutant run, so no mutant could have "fixed" the grader itself.

## Restoration evidence

- Restored leg: pristine re-run after all 14 mutants → `diff pristine.txt R1.txt` empty; `R1` receipt archived (`restored-rerun-receipt.txt`).
- Lane untouched: `git -C "$S/fx/lane" status --porcelain` → 0 entries; `rev-parse HEAD` = `357deceb…`; lane probe sha256 still `63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf`. No lane file was edited; no git/jj mutating command was run in the lane.
- Mutant file digests and per-mutant diff sizes recorded in `MANIFEST.txt` (same dir).
- Scratch `$S` deleted after archiving receipts.

## Receipts archived (this dir)

`pristine-receipt.txt`, `restored-rerun-receipt.txt`, `K1-receipt.txt`…`K14-receipt.txt`, `K1.diff`…`K14.diff`, `MANIFEST.txt`.

## Tooling

None installed or upgraded (bwrap 0.13.1 and python 3.14.8 preexisting on host; pacman untouched).

VERDICT: probe-case-mutants-14/14
