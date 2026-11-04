source: S241 (corpus/SOURCES.md) — Terminal-Bench 2.0 nginx-request-logging grader, tests/test_outputs.py at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py — anchor: tests/test_outputs.py lines 11-178 (eight legs in file order), instruction.md lines 1-20 — sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0
verified-at: 2026-11-03 (live re-fetch at the pin: HTTP 200, 5947 bytes, sha256 045cc716…4acda0 = corpus/evidence/round52/graders/SHA256SUMS:111, cmp byte-identical to the committed capture; instruction.md 1882 bytes at the same pin)
recheck: pinned at 2fd12b88aafdd04a52c298e3940bcb189f9766d6 (an immutable commit): `python3 plans/round69_c1_nginx_probe.py --lane . --work <scratch> --receipt <path>` must reproduce the five frozen vectors PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP; `sha256sum corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py` must print 045cc716…4acda0; `--check-receipt` reports the two leg-coverage defects (the honest MISS of record).

# TB2 `nginx-request-logging` — the grader replayed offline, and the legs the frozen table could not price (R69-C1, MISS)

The grader (`nginx-request-logging/tests/test_outputs.py` at pin `2fd12b88`; S241; sha256
`045cc716…4acda0`) runs eight legs in file order: `which nginx` (:13), a GET to
`http://localhost:8080` expecting 200 (:17-31), the exact index body `Welcome to the benchmark
webserver` (:39), the exact custom-404 body `Page not found - Please check your URL` (:52),
`nginx -t` (:59), the two config files read from disk — `listen 8080` + `root /var/www/html` in
`/etc/nginx/conf.d/benchmark-site.conf` (:67-104), then `log_format`, the four `$`-fields and
`limit_req_zone.*?rate=10r/s` in `/etc/nginx/nginx.conf` (:106-121) — the access log file's
existence (:123-142) and its line format (:144-178). The instruction at the same pin states the
same bodies, the rate-limit zone location and the log path (`instruction.md:6-11`).

The offline replay is `plans/round69_c1_nginx_probe.py`: five frozen cases stage a lane-built
HTTP server on 127.0.0.1:8080, lane-written config bytes at `/etc/nginx/`, a lane-written
`/etc/hosts` (`localhost` does not resolve in the sandbox without it), an optional `nginx` shim
on PATH and an optional access log the server writes. All five cases matched their frozen
vectors (K1 `PPPPPPPP`, K2 `PPFPPPPP`, K3 `PPPPPPFF`, K4 `PPPPPFPP`, K5 `FPPPFPPP`), 40/40
legs, `mismatches=0`; but `LEG-COVERAGE legs=8 seen_p=8 seen_f=6`, so the round's frozen
predicate — every leg observed `P` once and `F` once — **fails**: two legs have no red witness
in the table. R69-C1 is an honest MISS; the SKILL class row stays `executed 2 of 8` with the
replay named.

What the replay teaches, independent of the verdict:

- **Legs 2–4 are HTTP-observable and do not need nginx.** K5 (no `nginx` binary anywhere)
  passes legs 2–4: any process answering 200 on loopback:8080 passes the service legs, and the
  bodies are compared exactly, so only the body bytes are priced.
- **Legs 5–6 read files, not nginx.** The shim answers `nginx -t` with exit 0 regardless of the
  config, so a syntactically broken `nginx.conf` still greens leg 5; leg 6 is pure text presence
  in two files.
- **Leg 8's regexes are whole-content, not per-line.** The timestamp pattern needs
  `[+-]ZZZZ`, the method is any of GET/POST/PUT/DELETE/HEAD anywhere in the file, the status is
  any ` NNN ` anywhere, and the user-agent pattern anchors at the file's end — one stale line
  written by an earlier request satisfies all four even when the unique `/test-<epoch>` path
  was never logged (the `unique_path in log_content` test only chooses a file when several
  exist, and the list has one).
- **The two unpriced legs need two case fields for round 70:** a service-down case (leg 2 red;
  `run_case` currently aborts at the server READY-wait, so a `server: False` field plus a
  tolerated 4 s retry loop is needed) and a wrong-404-body case (leg 4 red; the `notfound`
  field already exists and no case mutates it).
- **`case_sha256` is not a staged-state identity.** It digests the whole case tree, which
  includes the server-written access log, so two batteries of the same table produce different
  digests for the log-bearing cases (run 1 vs run 2: K1/K2/K4/K5 differ, K3 matches).

A re-check of this entry's own claims: every line number above was re-read from the committed
capture at `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`, whose
sha256 is on `SHA256SUMS:111`; the live re-fetch at the pin returned the same 5947 bytes.
