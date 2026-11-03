# Mutation battery — TB2 `pypi-server` grader (kengaku r63 w1, seat PypiMutate)

- Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, base tip `c78749a5565dfd186f10a1d8ac98e19dac2429666`
- Seat dir: `.ufo/waves/round-63/w1/attack/PypiMutate/` · scratch (removed before yield): `/fast/scratch/hyaku/kengaku-r63/PypiMutate`
- Frozen rules read first: `plans/round-63-claims.md`. **No prediction was altered**; M3/M4 are the seat's own
  pre-declarations, X1/X2/M3B/M0R below are extras this seat pre-declared before running them.
- Instrument: `harness.py` (own code, sha256 `c69b50eaf0a6b51752ffc6be54408e540717aff6380fb1e1c7e3c15c60899163`).
  **The probe's code (`plans/round63_c1_pypi_probe.py`) was not read for building this harness and is not used.**

## 1. Instrument

| step | command / shape |
|---|---|
| venv | `/usr/bin/python3 -m venv $S/venv` → Python 3.14.8, pip 26.2.1 |
| grader copy | `cp corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py $S/tests/` → sha256 `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` (asserted in code) |
| wheels | hand-built with `zipfile`: `vectorops/__init__.py`, `vectorops-<v>.dist-info/{METADATA,WHEEL,RECORD}`, deterministic timestamps, RECORD = `sha256=<urlsafe-b64>` per file |
| index | `$S/idx/<leg>/simple/vectorops/index.html` with `<a href="../../packages/<wheel>#sha256=<hex>">`; wheel at `$S/idx/<leg>/packages/<wheel>` |
| server | `/usr/bin/python3 -m http.server <port> --bind 127.0.0.1 --directory $S/idx/<leg>` via `Popen`; PID recorded; `ss -ltnp` checked that this PID is the holder; killed by that PID after the leg |
| grader leg | `/usr/bin/env -i PATH=$S/venv/bin:/usr/bin:/bin HOME=$S/home PIP_CONFIG_FILE=/dev/null python -c "import sys; sys.path.insert(0,'$S/tests'); import test_outputs as t; t.test_api()"` |
| between legs | `$S/venv/bin/python -m pip uninstall -y vectorops`; residue check `python -c "import vectorops"` must fail; `$HOME/.cache/pip` cleared (fresh fetch every leg, proven by each server log) |
| gate | before every leg `ss -ltnp \| grep ':8080 '` must be empty (item rule); `port_after_stop = null` recorded after each leg |

Preflight (before any server): the M0 wheel installed offline with `pip install --no-index --find-links <packages> vectorops==0.1.0`
(rc 0) and `dotproduct([1,2],[3,4]) == 11`, so a later failure cannot be blamed on a malformed wheel.

## 2. Candidates

| leg | candidate | port | wheel file (sha256) | pre-declared |
|---|---|---|---|---|
| M0 | correct, `sum(a*b)` | 8080 | `vectorops-0.1.0-0-py3-none-any.whl` (`7cc41c59…`) | **P** (= K1) |
| M1 | wrong math `sum(a*b)+1` | 8080 | `vectorops-0.1.0-1-…whl` (`d109526a…`) | **F** (= K3) |
| M2 | correct code, index holds only 0.2.0 | 8080 | `vectorops-0.2.0-0-…whl` (`ecf03bf4…`) | **F** (= K4) |
| M3 | correct code, METADATA `Name: vectorop` | 8080 | `vectorops-0.1.0-3-…whl` (`743a41eb…`) | **F** (seat) |
| M4 | correct code, index on 127.0.0.1:8081 | 8081 | `vectorops-0.1.0-4-…whl` (`7cc41c59…`) | **F** (seat) |
| K2 | do-nothing control, no server | — | — | **F** |
| M0R | stability control: M0 repeated after all mutants | 8080 | same bytes as M0 (`7cc41c59…`) | P (seat) |
| X1 | correct wheel, anchor `#sha256=` replaced by 64 zeros | 8080 | `vectorops-0.1.0-5-…whl` (`7cc41c59…`) | F (seat) |
| X2 | lookup-table "cheat": exact answers for the 4 asserted vectors, `-999` otherwise | 8080 | `vectorops-0.1.0-6-…whl` (`e431713b…`) | P (seat, designed survivor) |
| M3B | name typo in METADATA **and** dist-info dir (`vectorop-0.1.0.dist-info`) | 8080 | `vectorops-0.1.0-7-…whl` (`3310ed89…`) | F (seat) |

`vectorops-0.1.0-{0,4,5}` wheels are byte-identical (`7cc41c59…`); only the filename differs, so X1 isolates the
anchor hash and M4 isolates the port.

## 3. Results (observed)

| leg | grader rc | exception (grader) | leg | server PID | holder = PID | port free after | match |
|---|---|---|---|---|---|---|---|
| M0 | 0 | — | **P** | 2837149 | yes | yes | ✔ |
| M1 | 1 | `AssertionError` (test_outputs.py:85, `dotproduct([1,1],[0,1]) == 1`) | **F** | 2840217 | yes | yes | ✔ |
| M2 | 1 | `subprocess.CalledProcessError` (install) | **F** | 2843097 | yes | yes | ✔ |
| M3 | 1 | `subprocess.CalledProcessError` (install) | **F** | 2846807 | yes | yes | ✔ |
| M4 | 1 | `subprocess.CalledProcessError` (install) | **F** | 3295105 | yes | yes | ✔ |
| K2 | 1 | `subprocess.CalledProcessError` (install) | **F** | — | — | n/a | ✔ |
| M0R | 0 | — | **P** | 3323596 | yes | yes | ✔ |
| X1 | 1 | `subprocess.CalledProcessError` (install) | **F** | 3326465 | yes | yes | ✔ |
| X2 | 0 | — | **P** | 3328963 | yes | yes | ✔ |
| M3B | 1 | `subprocess.CalledProcessError` (install) | **F** | 3331887 | yes | yes | ✔ |

M0's grader stdout: `Successfully installed vectorops-0.1.0`, `pip show` → `Name: vectorops / Version: 0.1.0`,
all four asserts pass, rc 0. M1's traceback names line 85 — the first assert — with `sum+1` making it 2.

## 4. Tally

- **Frozen-vector echo (independent): P / F / F / F** over (correct · wrong math · wrong version · empty 8080).
  Identical to the frozen K1–K4 vector. M4 adds port specificity: a correct index on 8081 does **not** satisfy the grader.
- **Escape** (correct candidate that fails): **0 / 2** (M0 P, M0R P).
- **Survivor** (mutant that passes): **0 / 6** mutants designed to fail (M1, M2, M3, M4, X1, M3B).
- **Designed survivor: 1 / 1** — X2 (lookup-table cheat) passes `test_api` (rc 0) and is wrong off-test.
  This is a **coverage finding about the grader**, not a licence to change the frozen contract.
- **Mismatches with frozen or pre-declared predictions: none (10/10 legs matched).**
- One diagnostic attempt (MP-EMPTY, not a scored leg) was **confounded** by a foreign index on 8080 and excluded;
  it was then re-run **cleanly on 8080** (`MP-EMPTY-CLEAN`: 5 × `Connection refused`, 7.70 s, `ss` empty before and
  after) and a substitute witness on an uncontended port is also recorded in §5.

## 5. Mechanisms (pip stderr, captured by direct re-runs of the grader's install command)

The grader captures pip's output and re-raises `CalledProcessError` with only the command, so the *class* alone
cannot separate K2 from K4 (both `CalledProcessError`). Direct re-runs of the same pip command supply the text:

| probe | port | pip rc | pip stderr (decisive lines) |
|---|---|---|---|
| MP-M2 | 8080 | 1 | `Could not find a version that satisfies the requirement vectorops==0.1.0 (from versions: 0.2.0)` |
| MP-M3 | 8080 | 1 | `Could not find a version that satisfies the requirement vectorops==0.1.0 (from versions: 0.1.0)` — the only candidate is *listed and rejected*; the wheel was fetched (`GET …whl` 200) before rejection → pip's metadata-name consistency check |
| MP-X1 | 8080 | 1 | `THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE … Expected sha256 000…0 Got 7cc41c59…` |
| MP-X2 | 8080 | 0 | (none) — then `dotproduct` on-test `[1,2,1,0]`, off-test `dotproduct([2,3],[4,5]) = -999` (expected 23) |
| MP-REFUSED | 18080, nothing listening | 1 | 5 × `NewConnectionError(… [Errno 111] Connection refused)`, 7.68 s, then `Could not find a version … (from versions: none)` |
| MP-EMPTY-CLEAN | **8080**, `ss` empty before/after | 1 | 5 × `NewConnectionError("HTTPConnection(host='localhost', port=8080) … [Errno 111] Connection refused")`, 7.70 s, then `(from versions: none)` — same shape as K2 (7.88 s) |
| MP-EMPTY | 8080 | 1 | **confounded** (first attempt): a foreign index answered `GET /simple/vectorops/` 200 listing `vectorops-0.1.0-py3-none-any.whl` (no build tag — no wheel of this seat) whose href 404'd in 0.17 s. Excluded; replaced by MP-EMPTY-CLEAN above. |

K2 (empty 8080, same command) took **7.88 s** with the five-retry signature; a foreign answering index takes
~0.17 s. K2's mechanism is therefore connection-refused, confirmed on the real port by MP-EMPTY-CLEAN. pip 26.2.1
renders the endpoint as `host='localhost', port=8080`, not as a URL — the form a K2 stderr match must accept.
Every served leg's access log shows only this seat's requests plus pip's own `GET /simple/pip/` version self-check
(404, ignored).

## 6. Findings for the wave (scoped, no contract change)

1. **K2 vs K4 are indistinguishable by exception class.** The probe's predicate already requires K2's captured pip
   stderr to name `localhost:8080`; this battery shows *why* that is necessary: the grader eats pip's text, so
   without it a foreign 404 index and an absent index both give `CalledProcessError`.
2. **`test_api` has no off-test input** (X2 survives). Four fixed vectors are the whole contract; a lookup table
   that returns `-999` everywhere else is graded correct. Recorded as a coverage limit of the grader, not patched.
3. **pip self-check traffic:** every install first asks the index for `/simple/pip/` (`PIP_DISABLE_PIP_VERSION_CHECK`
   is absent from the frozen env). A 404 is fine; the probe's index must not serve a real pip distribution there.
4. **Port specificity is real:** correct bytes on 8081 give F (M4), and a refused 8080 costs ~8 s of retries (K2).
   Together with the ~0.2 s foreign-index signature, a probe can prove its own server by PID + access log.
5. **Hash fragments are enforced** (X1): if the probe's index carries `#sha256=`, a K1 pass also proves the served
   bytes match the advertised digest.
6. `pip show vectorops` is a second gate after install; the name-typo mutants die earlier, inside `pip install`.

## 7. Evidence

`evidence/results.json` (all legs + mechanism probes), `evidence/run/<leg>/{grader.stdout,grader.stderr,server.log}`,
`evidence/idx/<leg>/{simple/…,packages/…}` (index pages and wheels as served), `evidence/run/MP-REFUSED/`,
`evidence/run/MP-EMPTY-CLEAN/` (clean empty-8080 stderr), `evidence/tests/test_outputs.py` (sha asserted above),
`evidence/env.txt`, `evidence/contention-log.txt`, `evidence/MANIFEST.sha256` (all of the above).

Reproduction: rebuild the scratch layout (venv, grader copy, `harness.py --preflight`), then `harness.py <LEG>`
per leg and `harness.py --mp` for the mechanism probes. Every seed is literal in `harness.py`.
