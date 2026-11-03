# PypiMutate — independent mutation battery on the TB2 `pypi-server` grader

Seat: r63 w1 attack · lane base `c78749a5` · full record: `.ufo/waves/round-63/w1/attack/PypiMutate/mutation.md`
+ `attack/PypiMutate/evidence/` (results.json, per-leg grader stdout/stderr and HTTP access logs, index pages,
wheels, MANIFEST.sha256). Harness is this seat's own (`attack/PypiMutate/harness.py`, sha256 `c69b50ea…`);
the probe's code was not used. Plan predictions were not altered.

## Result in one line

Observed leg vector **P / F / F / F** for (correct · wrong math · wrong version · empty 8080), identical to the
frozen K1–K4 vector; **0 escapes** (2/2 correct candidates pass), **0 survivors** among 6 fail-designed mutants,
**1 designed survivor** (lookup-table cheat) as a grader-coverage finding. **0 prediction mismatches (10/10).**

## Table

| leg | candidate | port | wheel sha256 (short) | grader rc | exception | leg | pre-declared | match |
|---|---|---|---|---|---|---|---|---|
| M0 | correct `sum(a*b)` | 8080 | `7cc41c59…` | 0 | — | **P** | P | ✔ |
| M1 | `sum(a*b)+1` | 8080 | `d109526a…` | 1 | `AssertionError` (test_outputs.py:85) | **F** | F | ✔ |
| M2 | index holds only 0.2.0 | 8080 | `ecf03bf4…` | 1 | `CalledProcessError` (install) | **F** | F | ✔ |
| M3 | METADATA `Name: vectorop` | 8080 | `743a41eb…` | 1 | `CalledProcessError` (install) | **F** | F | ✔ |
| M4 | correct code on :8081 | 8081 | `7cc41c59…` | 1 | `CalledProcessError` (install) | **F** | F | ✔ |
| K2 | nothing on 8080 | — | — | 1 | `CalledProcessError` (install) | **F** | F | ✔ |
| M0R | M0 repeated after all mutants | 8080 | `7cc41c59…` | 0 | — | **P** | P | ✔ |
| X1 | correct wheel, anchor `#sha256=0…0` | 8080 | `7cc41c59…` | 1 | `CalledProcessError` | **F** | F | ✔ |
| X2 | lookup-table cheat (`-999` off-test) | 8080 | `e431713b…` | 0 | — | **P** | P | ✔ |
| M3B | typo in METADATA + dist-info dir | 8080 | `3310ed89…` | 1 | `CalledProcessError` | **F** | F | ✔ |

Every leg: `ss -ltnp` showed 8080 free at the gate, the serving PID was verified as the port holder, the access
log names only this seat's requests, and the port was free again after the leg. Between legs: `pip uninstall -y
vectorops`, `import vectorops` fails, pip cache cleared (each pass fetched the wheel over HTTP, per access log).

## Mechanisms (pip stderr the grader swallows)

- M2: `Could not find a version … (from versions: 0.2.0)`.
- M3: `Could not find a version … (from versions: 0.1.0)` — candidate listed then rejected; wheel fetched 200 then
  refused by pip's metadata-name consistency check. Same class for M3B.
- X1: `THESE PACKAGES DO NOT MATCH THE HASHES … Expected sha256 000…0 Got 7cc41c59…` → the anchor digest is enforced.
- Empty target: 5 × `NewConnectionError(… [Errno 111] Connection refused)` then `(from versions: none)` —
  observed on 8080 itself with `ss` empty before and after (7.70 s), and on an uncontended :18080 (7.68 s);
  K2 on 8080 took 7.88 s with the same five-retry shape → K2 is connection-refused, not a foreign index
  (a foreign answering index returns in ~0.17 s; one such confound is logged and excluded).
- pip 26.2.1 renders the endpoint as `HTTPConnection(host='localhost', port=8080)`, not as a URL — the clean
  8080 capture shows exactly that form, matching PypiProbeBuild's K2 stderr correction.

## Findings for the wave

1. Exception class alone cannot separate K2 from K4 (both `CalledProcessError`); the C1 predicate's requirement to
   capture K2's pip stderr is necessary, and the decisive strings are `Connection refused` / `port=8080`.
2. `test_api` checks four fixed vectors only: an implementation correct on those and wrong elsewhere passes
   (X2, off-test `dotproduct([2,3],[4,5]) = -999`). Coverage limit of the grader — reported, not patched.
3. Every install also issues `GET /simple/pip/` (pip's version self-check; 404 tolerated). A probe index should
   leave that 404.
4. Port specificity is real (M4 F on 8081; K2 ~8 s refusal). A probe proves its own index by served PID + access
   log; a foreign service on 8080 answers in ~0.2 s.
5. `pip show vectorops` is a second post-install gate, but name-inconsistent wheels already die inside `pip install`.

## Port-8080 contention (affects no scored leg)

Two harness aborts fired *before any bind* and no leg ran: (a) a bash watch loop that merely mentions the probe
filename, (b) a sibling's `bwrap --unshare-net` pip (private netns, cannot reach host 8080). Detector was narrowed
to `ss` listeners + same-netns python/pip. One diagnostic (MP-EMPTY) was answered by a foreign index and is
excluded; its replacement witness binds nothing. Log: `attack/PypiMutate/evidence/contention-log.txt`.
