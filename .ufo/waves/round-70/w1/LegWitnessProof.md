# LegWitnessProof — R70-C1 witness authenticity: are K6 and K7 the grader's own verdicts?

Seat: `LegWitnessProof`, round 70, wave w1 (v1, 14 seats). Lane `master` at
`384e9c76415e78093623b3eaff262423a89dbc3e` (freeze commit; `hyaku/jj-lane.sh state` →
`branch=master local=384e9c76… remote=384e9c76… ahead=0 behind=0`). Claims read in full from
`plans/round-70-claims.md` before any command. No file under `plans/`, `corpus/` or any
predicate was edited by this seat; this seat only read the lane and wrote its own evidence
under `.ufo/waves/round-70/w1/LegWitnessProof/`.

**Item attacked.** R70-C1's two new red witnesses (K6 "no HTTP service on 8080",
K7 "custom-404 body differs by one character") could be **staging artifacts** — outcomes
manufactured by the probe's harness rather than produced by the grader's own test functions.
This report establishes, from the battery's own sandbox captures plus an independent host-side
import of the same grader bytes, that every K6/K7 red is a failure raised inside the grader's
own functions, and names the one place where the receipt's `F` label is a normalization
rather than an `AssertionError`.

---

## 1. What I ran

| # | command (cwd = lane root unless noted) | rc | result |
|---|---|---|---|
| 1 | `git -C kengaku-shokunin rev-parse master` / `scripts/hyaku/jj-lane.sh state kengaku-shokunin` | 0 | tip `384e9c76`, ahead=0 behind=0 |
| 2 | `sha256sum corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py` | 0 | `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` (= frozen value = `SHA256SUMS:111`) |
| 3 | `git -C kengaku-shokunin cat-file -e 502893ad:corpus/evidence/round70/nginx/receipt.txt` | 128 | absent at base, as the C1 control states |
| 4 | `mkdir -p $S/witness-work` | 0 | (first battery attempt without it returned rc=2 `SETUP work-dir-required`; the work dir must pre-exist — recorded, not a defect) |
| 5 | `TMPDIR=$S python3 plans/round70_c1_nginx_probe.py --lane . --work $S/witness-work --receipt $S/witness-receipt.txt --evidence-dir $S/witness-sandbox` | 0 | 27.04 s, `PREDICATE R70-C1 pass`, 56/56 legs observed, 7/7 vectors agree |
| 6 | `flock -x /home/vgpnk/.local/share/kengaku-r70/port-8080.lock -c 'python3 $S/repro.py'` | 0 | independent grader import, 9 calls, results in §4(d) |
| 7 | `diff -r -x server.json -x '*.log' K1 K6` and `… K1 K7` (in `$S/witness-work`) | 1 (differences found — expected) | exactly the staged deltas in §4(c) |

`$S` = `/fast/scratch/hyaku/kengaku-r70/LegWitnessProof` (removed after the evidence below was
copied into this directory). No tools were installed or upgraded for this seat.

Battery receipt head and tail (`witness-receipt.txt`, sha256 `8e9a0e54…`):

```
PROBE plans/round70_c1_nginx_probe.py sha256 9aef6d33abc965f52a965b2f9197b78d257dc76003ddc124ca0e692a4fdbbe90
PROBE_BLOB plans/round70_c1_nginx_probe.py sha256 9aef6d33abc965f52a965b2f9197b78d257dc76003ddc124ca0e692a4fdbbe90
PROBE_VERSION 1
GRADER corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0 pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
PORT 8080 free-at-start=True lock=/home/vgpnk/.local/share/kengaku-r70/port-8080.lock
…
LEG-COVERAGE legs=8 seen_p=8 seen_f=8
SUMMARY cases=7 legs=56 mismatches=0 setup=0
PREDICATE R70-C1 pass
```

The working-tree probe sha equals its committed blob sha (`9aef6d33…`), i.e. the battery ran
the frozen instrument. All seven `case_sha256` values in my receipt equal the frozen `CASE_SHA`
table (`K1 0cf77ab8…`, `K2 c072ee5f…`, `K3 286db51e…`, `K4 22ee1ff8…`, `K5 5690e1e1…`,
`K6 d4035f6f…`, `K7 07eb2fd3…`), so K6/K7 ran the frozen staged inputs, not some drifted copy.

---

## 2. K6 — every TEST line, quoted

`witness-sandbox/K6-sandbox.txt` (sha256 `2feb9a52…`), header and body verbatim, stderr empty:

```
rc=0 server_pid=None
--- stdout
TEST test_nginx_installed P 1ms
TEST test_nginx_running F 4002ms Nginx is not running on port 8080
TEST test_index_page_content E:ConnectionError 0ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: / (Caused by NewConnectionError("HTTPCon
TEST test_custom_404_page E:ConnectionError 0ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: /nonexistent-page (Caused by NewConnecti
TEST test_nginx_config_syntax P 1ms
TEST test_nginx_config_settings P 0ms
TEST test_log_file_creation E:ConnectionError 0ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: / (Caused by NewConnectionError("HTTPCon
TEST test_log_file_format E:ConnectionError 1ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: /test-1793753241 (Caused by NewConnectio

--- stderr
```

`E:` messages are truncated by the runner to 120 characters
(`plans/round70_c1_nginx_probe.py:281-284`). The truncation is display-only; a 3-line direct
request run under the same port lock (no service staged, port otherwise idle) returned the
untruncated text:

```
ConnectionError
HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: / (Caused by NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused"))
```

i.e. loopback `[Errno 111] Connection refused`, not DNS failure, not a sandbox fault.

### Which legs fail, and why each is forced by the staged state

| leg | grader source | outcome | forced by |
|---|---|---|---|
| 1 `test_nginx_installed` | `test_outputs.py:13-14` `which nginx` | **P** | shim staged on PATH; the shim exists precisely so this leg is green |
| 2 `test_nginx_running` | `:19-30` retry loop, `assert False, "Nginx is not running on port 8080"` at `:29` | **F** | no listener on 8080. `:22` raises `requests.ConnectionError` on each of 3 attempts; only at `i == max_retries - 1` does `:29` fire. The **4002 ms** runtime is the fingerprint of 3 refused connects + 2 × `time.sleep(2)` (`:30`); the message is the literal string at `:29` |
| 3 `test_index_page_content` | `:35` `requests.get("http://localhost:8080")` is the first statement | **F** (E:ConnectionError) | the connection is refused *before* any assertion; the exception's URL is `/`, exactly `:35`'s URL |
| 4 `test_custom_404_page` | `:48` `requests.get("http://localhost:8080/nonexistent-page")` is the first statement | **F** (E:ConnectionError) | refused before the status/body assertions at `:49`,`:53`; the exception's URL is `/nonexistent-page`, exactly `:48`'s URL |
| 5 `test_nginx_config_syntax` | `:61-62` `nginx -t` | **P** | the shim answers `-t` with rc 0; untouched by the missing service |
| 6 `test_nginx_config_settings` | `:67-120` file-content checks | **P** | the staged config carries `listen 8080`, `root /var/www/html`, `log_format` + all four fields and `limit_req_zone … rate=10r/s` |
| 7 `test_log_file_creation` | `:126` `requests.get("http://localhost:8080")` is the first statement | **F** (E:ConnectionError) | refused at `:126`, before the `Path(...).exists()` check at `:137`; the staged (empty) access log would have made `:141` **pass** — so this red witnesses the connection path, not the log-existence check (K3 is the log witness) |
| 8 `test_log_file_format` | `:148` `requests.get(f"http://localhost:8080{unique_path}")` is the first statement | **F** (E:ConnectionError) | refused at `:148`; the URL `/test-1793753241` is generated by the grader at `:147` (`unique_path = f"/test-{int(time.time())}"`), so the failing call is provably the grader's own |

`server_pid=None` in the sandbox header and in the receipt line
`CASE K6 case_sha256=d4035f6f… server_pid=None sandbox_rc=0` record that the probe started no
service for K6; `PORT 8080 free-at-start=True` records the port was unbound before the battery.
Nothing else could have been listening at the moment legs 3/4/7/8 ran (their connects were
refused in 0–1 ms — a refusal, not a 2 s timeout, and not a foreign server).

---

## 3. K7 — leg 4's body assertion, seven legs green

`witness-sandbox/K7-sandbox.txt` (sha256 `f75dd5b4…`), header and body verbatim, stderr empty:

```
rc=0 server_pid=2874639
--- stdout
TEST test_nginx_installed P 1ms
TEST test_nginx_running P 2ms
TEST test_index_page_content P 1ms
TEST test_custom_404_page F 1ms Expected 'Page not found - Please check your URL',         but got 'Page not found - Please check your URL!'
TEST test_nginx_config_syntax P 1ms
TEST test_nginx_config_settings P 0ms
TEST test_log_file_creation P 1001ms
TEST test_log_file_format P 1001ms

--- stderr
```

The failing message is produced by the grader's own f-string at `test_outputs.py:53-55`:
`expected_content` comes from `:52` (`"Page not found - Please check your URL"`), the observed
`content` from the HTTP response body, and the nine-space run after the comma (one space after the comma plus the
f-string's eight-space continuation indent) is the literal `\`-continuation formatting in the
grader's f-string. The `got` string ends in `!` — the one
staged character. The other seven legs pass **with the service up**: leg 2 reaches the same
host:port in `2 ms` and leg 3's `/` returns the exact index body, so the sandbox network and
the service work in this exact run; leg 4 fails on `content == expected_content`, not on
reachability or status code.

---

## 4. Why these are the grader's verdicts, not staging artifacts

**(a) The grader bytes are the pinned bytes in every case.** Staged `tests/test_outputs.py`
sha256 in all seven case roots (`witness-staging-diff.txt`):
`045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` — equal to the committed
file and to `corpus/evidence/round52/graders/SHA256SUMS:111`. The runner imports that file at
`/tests/test_outputs.py` and calls its functions by name; no leg is asserted by the probe
(probe docstring, `plans/round70_c1_nginx_probe.py:16-17`: "an AssertionError is F, any other
exception is E (scored F), a return is P").

**(b) K1 is all-green through the identical sandbox argv.** `bwrap_argv(root)` differs between
cases only by the case-root path strings; the namespace flags are identical for every case
(`--unshare-pid|ipc|uts`, **no** `--unshare-net`). K1 in this same battery observed
`VECTOR K1 PPPPPPPP` — the very legs 2, 3, 4, 7, 8 that are red in K6 are green in K1 through
the same sandbox, so the K6 reds cannot be attributed to bwrap network isolation, read-only
mounts, or a missing Python.

**(c) The staged states differ from K1 exactly as claimed.** `witness-staging-diff.txt`:
K1 vs K6 differs only in `run/bodies.json`'s documentary `"server_enabled": true→false` (the
probe writes that key at `:409` and never reads it; the actual staged condition is
`if case["server"]: server = start_server(root)` at `:471`, which K6 skips) plus the absent
listener. K1 vs K7 differs only in the last byte of `notfound`
(`…your URL"` → `…your URL!"`). Every other staged input — the grader, `tests/runner.py`,
`run/server.py`, both nginx configs, `/etc/hosts`, the shim, and the access log (staged empty
in both; excluded from the diff only because the running servers append to it) — is
byte-identical between K1 and each witness. So the vector delta K1→K6 is caused only by the
missing service and K1→K7 only by the one-byte body edit; nothing else was available to
produce a red.

**(d) Independent reproduction without the probe's runner.** `repro.py` (copied here, sha256
`03bd2a52…`) imports the same grader file with `importlib` on the host, starts its **own**
15-line `http.server` on 127.0.0.1:8080 (not the probe's staged `run/server.py`), and calls
the grader's functions directly. Output (`witness-repro.txt`, sha256 `3fa4e0fa…`):

```
REPRO grader_sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0
REPRO no-service:test_nginx_running ASSERTION 4004ms 'Nginx is not running on port 8080'
REPRO no-service:test_index_page_content EXC:ConnectionError 1ms 'HTTPConnectionPool(host=\'localhost\', port=8080): Max retries exceeded with url: / (Caused by NewConnectionError("HTTPCon'
REPRO no-service:test_custom_404_page EXC:ConnectionError 1ms "HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: /nonexistent-page (Caused by NewConnecti"
REPRO K7-body:test_nginx_running PASS 1ms
REPRO K7-body:test_index_page_content PASS 1ms
REPRO K7-body:test_custom_404_page ASSERTION 1ms "Expected 'Page not found - Please check your URL',         but got 'Page not found - Please check your URL!'"
REPRO K1-body:test_nginx_running PASS 1ms
REPRO K1-body:test_index_page_content PASS 1ms
```

Byte comparisons made programmatically: K6 leg 2's sandbox message equals the grader's literal
`Nginx is not running on port 8080` (and the repro's assertion message); K7 leg 4's sandbox
message is **character-for-character equal** to the repro's assertion message, including the
nine-space gap; the K6 leg-3/leg-4 `E:` payloads equal the repro's exception strings over their
120-character runner prefix. The K1-body control passes the same `test_custom_404_page`, so the
assertion discriminates on the staged byte, not on the harness.

**(e) Run-clock fingerprints.** K6 leg 8's URL carries `/test-1793753241`, which is
`2026-11-04T00:47:21Z` — this run's clock (local `2026-11-03 21:47`). A staged transcript
could not carry the run's own epoch; the grader generated the path at `:147`.

**(f) No harness fault anywhere in the battery.** All seven captures report `rc=0` and empty
stderr (`witness-sandbox/*.txt`); in K6 the same runner executed legs 1, 5, 6 to `P`, which is
only possible if `importlib` loaded the grader, `/shim/nginx` resolved on PATH, and the
subprocess leg ran. A crash of bwrap or the runner would have produced a non-zero rc or stderr,
not per-leg `TEST` lines with the grader's strings.

---

## 5. Legs whose red is an exception, not an assertion — named limitation

No leg's red is caused by a **harness** exception: bwrap and the runner exit clean, and the
assertion legs are intact. But four of K6's five reds are **uncaught exceptions raised inside
the grader's own test functions**, not `AssertionError`s:

- K6 legs 3, 4, 7, 8 are `requests.exceptions.ConnectionError` raised at
  `test_outputs.py:35`, `:48`, `:126`, `:148` (the grader never guards those calls);
- the probe's runner prints them as `E:ConnectionError` (`plans/round70_c1_nginx_probe.py:281-284`)
  and `run_case` maps any outcome that is not `P` to `F` (`:482-485`:
  `legs[parts[1]] = ("P" if outcome == "P" else ("F" if outcome == "F" else "F"))`).

So the receipt's `F` for K6 legs 3/4/7/8 is a **classification of an uncaught exception**, and
the receipt alone cannot distinguish an assertion-red from an exception-red — the `E:` labels
survive only in the sandbox captures (this directory). The verdict direction is unchanged under
the real TB2 path, which runs pytest (`…/nginx-request-logging/tests/test.sh:17-28`, `uvx …
pytest … /tests/test_outputs.py`), where an uncaught exception is also a test failure and
`reward.txt` becomes 0. Two further reading cautions, both consistent with the frozen table:

1. **K6 leg 4 is not the body assertion.** K6 stages the *correct* 404 body; its leg-4 red is
   the refused connection at `:48`. The only witness of `:53`'s body assertion is K7.
2. **K6 legs 7/8 are not the log checks.** The staged access log exists (empty); the reds come
   from `:126`/`:148` refusing before the log assertions. K3 is the log-leg witness.

---

## 6. Verdict

**PASS (witness authenticity).** In the single frozen battery run (`PREDICATE R70-C1 pass`,
rc 0), K6's reds are the grader's own outcomes — one `AssertionError` at
`test_outputs.py:29` after its own three-retry loop, and four `ConnectionError`s raised by the
grader's own unguarded `requests.get` calls at `:35`, `:48`, `:126`, `:148` — and K7's single
red is the grader's own body assertion at `:53-55` while its other seven legs pass with the
service up. The same grader bytes run green in K1 through the same sandbox, staged state
differs from K1 only by the claimed deltas, an independent host-side import reproduces the same
messages byte-for-byte, and all captures are rc=0 with empty stderr. No leg's red is a harness
fault; the one calibration limitation is that K6 legs 3/4/7/8 are exception-reds that the
receipt folds into `F` (pytest-equivalent, but not distinguishable inside the receipt).

Scope note: this report judges **witness authenticity only**. It does not re-score the C1
predicate, the case table, the vectors, the digests or the kill rule; the `--check-receipt`
re-derivation and the landing decision belong to the L1 and the other wave seats.

---

## 7. Retained evidence (this directory)

```
LegWitnessProof.md                     this report
SHA256SUMS                             hashes of the evidence files below
repro.py                               independent grader-import reproduction (sha256 03bd2a52…)
witness-receipt.txt                    battery receipt (sha256 8e9a0e54…): PREDICATE R70-C1 pass
witness-repro.txt                      independent repro output (sha256 3fa4e0fa…)
witness-staging-diff.txt               per-case grader shas + K1/K6 and K1/K7 staged diffs (sha256 c1dee40b…)
witness-untruncated-exc.txt            full [Errno 111] Connection refused text (runner truncates to 120 chars)
witness-sandbox/K1..K7-sandbox.txt     sandbox captures; K6 sha256 2feb9a52…, K7 sha256 f75dd5b4…
```

Scratch `/fast/scratch/hyaku/kengaku-r70/LegWitnessProof` was removed after these copies were
taken; the only other paths touched were the instrument's documented port-lock file
(`/home/vgpnk/.local/share/kengaku-r70/port-8080.lock`, present in the receipt) and its staged
work dirs under that scratch dir. No git/jj mutation, no
commit, no push, no credential read.
