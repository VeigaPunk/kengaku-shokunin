# ControlProbe — R63-C1 K2 stderr clause, settled

Seat: ControlProbe (revenger). Scope: the pypi-server grader's install step and the do-nothing
control K2, to settle the exact stderr clause the frozen R63-C1 predicate reads
("K2's captured pip stderr names localhost:8080"). Read-only on the lane; nothing edited.
Receipts: `.ufo/waves/round-63/w1/control/` (see `revenger-notes.md`, `k2-pip-stderr.txt`).

## Verdict (acceptance)

| item | observed | command |
|---|---|---|
| K2 pip rc | **1** | `env -i PATH=<venv>/bin:/usr/bin:/bin HOME=<home> PIP_DISABLE_PIP_VERSION_CHECK=1 <venv>/bin/python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0` |
| stderr names `localhost:8080` (contiguous literal) | **False** — 0 matches | `grep -c 'localhost:8080' k2-pip-stderr.txt` |
| stderr names localhost **and** port 8080 as one endpoint | **True** — 5 matches | `grep -c "host='localhost', port=8080" k2-pip-stderr.txt` |
| split fields present | 5 × `host='localhost'`, 5 × `port=8080`, 5 × `Errno 111`, 0 × `::1` | `grep -c` each |
| pip error class line | `ERROR: No matching distribution found for vectorops==0.1.0` | last stderr line |
| preceding class line | `ERROR: Could not find a version that satisfies the requirement vectorops==0.1.0 (from versions: none)` | stderr line 6 |
| grader exception | `subprocess.CalledProcessError` | grader `test_api` run, see `k2-grader-exception.txt` |

Captured stderr: 7 lines / 1526 bytes, sha256 `dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d`.
Reproduced byte-identically on a second run. pip 26.2.1, vendored urllib3 2.7.0, CPython 3.14.8,
grader sha256 `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` (matches frozen).

The literal `localhost:8080` exists once in the run — on **stdout**
(`Looking in indexes: http://localhost:8080/simple`), not stderr.

## Evidence chain

1. Grader hash and copy: `sha256sum` of `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py`
   → `82c6351…`; equal to SHA256SUMS line 134 and to the frozen constant.
2. Install step: bare `python` argv at grader lines 23 (uninstall), 25 (install), 58 (show);
   `command -v python` under `env -i PATH=<venv>/bin:…` → `<venv>/bin/python`, under
   `PATH=/usr/bin:/bin` → `/usr/bin/python` (no pip module).
3. K2 run (above), stderr captured to a file, `wc -l`/`wc -c`/`sha256sum` recorded.
4. `grep -c` counts on the captured stderr (table above).
5. Grader's own run of `test_api`: `CalledProcessError`, `.stderr` present and byte-identical to
   the pip stderr (`cmp` clean), `.stdout` = the URL line.
6. strace `-f -e trace=connect`: 6 TCP + 6 UDP connects to 127.0.0.1:8080 and 6 TCP + 6 UDP to
   ::1:8080 per K2 (1 attempt + 5 retries). `getaddrinfo("localhost")` returns ::1 first.

## Divergences found (reported, not edited)

1. **Clause rendering.** The frozen sentence says "names localhost:8080"; with the toolchain the
   probe uses (pip 26.2.1 / urllib3 2.7.0) the endpoint is named as
   `HTTPConnection(host='localhost', port=8080)`, never the contiguous literal. The probe's
   `ENDPOINT_PATTERNS` already accepts both renderings and prints which form matched; a re-check
   that greps the stderr for the contiguous literal will read False on a passing K2.
2. **Toolchain dependence of the clause.** pip 25.3 / urllib3 1.26.20 and pip 23.0.1 /
   urllib3 1.26.14 render the refused connection as an *object repr*
   (`<…HTTPConnection object at 0x…>`) — **neither** localhost nor 8080 nor even "8080" appears
   in stderr (measured). The grader's own `tests/test.sh` pins `-w pip==25.2`, i.e. under the
   grader's declared environment the K2 clause would be unsatisfiable as written. It is satisfied
   only because the probe's venv is built from the host CPython 3.14 (pip 26.2.1).
3. **Retry dependence.** The endpoint appears only in the retry WARNING lines; with
   `PIP_RETRIES=0` stderr is the two ERROR lines and names no endpoint. Probe does not set
   `PIP_RETRIES`.
4. **Port guard is v4-only.** `port_free()`/`port_listening()` use 127.0.0.1 only; a foreign
   `[::1]:8080` listener is invisible to the guard (measured True while `ss` shows the v6 holder).
   On the bare host pip prefers ::1, and a foreign v6 index served K1/K3 legs while the
   probe-owned index served 0 requests (probe index access log empty, foreign log 2 hits).
   Inside the probe's bwrap sandbox this is not reachable via `localhost` — the sandbox binds
   `/etc/hosts` but not `/etc/host.conf`, so `getaddrinfo("localhost")` collapses to 127.0.0.1
   and only 6 v4 connects occur. The probe's pass with a v6-only foreign listener present
   therefore rests on that side effect, not on a check.
5. **K2 confound is real for v4.** With a foreign compliant index on 127.0.0.1:8080 and the K2
   driver starting nothing, the leg is **P** (kill-rule trigger). The probe's `require_port_free`
   plus the `Errno 111 / Connection refused` requirement is what excludes it. A foreign 404
   service also makes the leg F while its stderr *does* contain the URL literal twice (2 matches)
   — so the literal grep alone cannot distinguish "quiet port" from "foreign 404".
6. **Receipt does not bind the stderr bytes.** `--check-receipt` verifies the self-reported
   `K2 stderr_mentions_8080=True` line only; the receipt carries no stderr sha256/path, and a
   copy of the receipt with no stderr file beside it still returns rc=0.
7. **Draft evidence file is truncated.** `.ufo/waves/round-63/w1/draft/corpus/evidence/round63/k2-pip-stderr.txt`
   is a 4-line / 1092-byte prefix (sha256 `505dc930…`) of the 7-line / 1526-byte capture
   (sha256 `dedbc20d…`): it omits `Retry(total=0)` and both ERROR lines, and its `port=8080`
   count is 4, not the 5 the knowledge entry states. The sibling `k2-pip-stderr-repro.txt` is
   the complete 7-line capture and matches this seat's independent reproduction.
8. **The committed do-nothing control does not demonstrate the clause.**
   `corpus/evidence/round63/control-k2.txt` has one `localhost:8080` match, but it is the argv
   echo inside the CalledProcessError message; the file contains no pip stderr at all
   (`port=8080`: 0, `Errno 111`: 0).

## Main-agent checks to run

- `grep -c 'localhost:8080' .ufo/waves/round-63/w1/control/k2-pip-stderr.txt` → 0
- `grep -c "host='localhost', port=8080" .ufo/waves/round-63/w1/control/k2-pip-stderr.txt` → 5
- `sha256sum .ufo/waves/round-63/w1/control/k2-pip-stderr.txt` → `dedbc20d70cc…`
- `grep -c 'port=8080' .ufo/waves/round-63/w1/draft/corpus/evidence/round63/k2-pip-stderr.txt`
  → 4 (truncated) vs `…k2-pip-stderr-repro.txt` → 5 (complete)

Confidence: high for the captures, counts, hashes, rc, error lines and connect traces (all
first-hand, reproduced twice); high for the pip-version rendering difference (three pip lines
measured, urllib3 source inspected); medium for the claim that pip 25.2 specifically behaves like
25.3 (25.2 could not be installed offline — uvx `--offline` has no cached wheel, and no network
open was authorised for this seat).
