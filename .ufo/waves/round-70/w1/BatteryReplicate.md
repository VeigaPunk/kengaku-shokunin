# BatteryReplicate — R70-C1 independent battery reproduction + D-fix (path independence)

Seat scope: reproduce the R70-C1 seven-case table twice, independently, and test the round-69
D-fix (`case_sha256` is a staged-input digest, path-independent). Nothing else touched.

Lane tip measured: `384e9c76415e78093623b3eaff262423a89dbc3e` ("round-70 freeze: claims,
instruments, wave spec+dispatch, census-before, controls") via `git -C L rev-parse master`.
Working-tree probe sha256 `9aef6d33abc965f52a965b2f9197b78d257dc76003ddc124ca0e692a4fdbbe90`
equals `git cat-file blob master:plans/round70_c1_nginx_probe.py | sha256sum` — PROBE and
PROBE_BLOB agree, so the run binds the committed bytes.

## Commands and rc

All from cwd `L` (`/home/vgpnk/Projects/shokunin/kengaku-shokunin`); scratch
`S=/fast/scratch/hyaku/kengaku-r70/BatteryReplicate`.

| # | command | rc |
|---|---|---|
| 1 | `python3 plans/round70_c1_nginx_probe.py --lane . --work $S/r2 --receipt $S/receipt2.txt --evidence-dir $S/sandbox2` | **0** (52.0 s) |
| 2 | `python3 plans/round70_c1_nginx_probe.py --lane . --work $S/r3 --receipt $S/receipt3.txt --evidence-dir $S/sandbox3` | **0** (35.0 s) |
| 3 | `python3 plans/round70_c1_nginx_probe.py --selftest --work $S/selftest` | **0** |
| 4 | `python3 plans/round70_c1_nginx_probe.py --render-table --stage-sha $S/stagesha` | **0** |
| 5 | `python3 plans/round70_c1_nginx_probe.py --check-receipt <official / receipt2 / receipt3>` | **0 / 0 / 0** |
| 6 | `python3 plans/round70_c1_nginx_probe.py --lane . --work $S/r2 --receipt $S/receipt2.txt` (existing receipt) | **2**, `SETUP receipt-exists …`, receipt sha256 unchanged |

Runs 1 and 2 launched in parallel; the probe's own `flock` on
`~/.local/share/kengaku-r70/port-8080.lock` serialized them (and the official
NginxBatteryR70 run at 21:47). Each receipt is 3611 bytes with `PORT 8080 free-at-start=True`.

## Finding 1 — every case reproduces in both independent runs

Receipt shas differ (server pids differ): official `237d28a1…`, r2 `8a75923e…`, r3 `f105042d…`.
Extracted fields:

| case | sha2==sha3 | vector2==vector3 | vector2 | sha == frozen `CASE_SHA` |
|---|---|---|---|---|
| K1 | True | True | `PPPPPPPP` | True (`0cf77ab8…`) |
| K2 | True | True | `PPFPPPPP` | True (`c072ee5f…`) |
| K3 | True | True | `PPPPPPFF` | True (`286db51e…`) |
| K4 | True | True | `PPPPPFPP` | True (`22ee1ff8…`) |
| K5 | True | True | `FPPPFPPP` | True (`5690e1e1…`) |
| K6 | True | True | `PFFFPPFF` | True (`d4035f6f…`) |
| K7 | True | True | `PPPFPPPP` | True (`07eb2fd3…`) |

Per case, exact lines (r2; r3 byte-identical after `server_pid` normalisation):

```
CASE K6 case_sha256=d4035f6f30bb3f1a63b09ce268e57f7fb3eea788d8b28a4f393717d683452437 server_pid=None sandbox_rc=0
VECTOR K6 PFFFPPFF expected PFFFPPFF agree=True
VECTOR K7 PPPFPPPP expected PPPFPPPP agree=True
LEG-COVERAGE legs=8 seen_p=8 seen_f=8
SUMMARY cases=7 legs=56 mismatches=0 setup=0
PREDICATE R70-C1 pass
```

`--render-table --stage-sha` reproduces the freeze arithmetic exactly and equals the claims
doc: `FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP/PFFFPPFF/PPPFPPPP`,
`LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8`, and the per-leg counts
`installed p=6 f=1`, `running p=6 f=1`, `index p=5 f=2`, `custom_404 p=5 f=2`,
`config_syntax p=6 f=1`, `config_settings p=6 f=1`, `log_creation p=5 f=2`, `log_format p=5 f=2`.

The official receipt (same minute, `corpus/evidence/round70/nginx/receipt.txt`) has the same
normalised `CASE`/`VECTOR` block: `diff` after stripping `server_pid=` prints `IDENTICAL` for
official↔r2, official↔r3 and r2↔r3. The only whole-file r2↔r3 differences are the six non-None
`server_pid` values (12 diff lines; K6 is `None` in both).

Live witness (named limitation i): the three runs are genuinely separate — disjoint pid ranges
official `2831758…2845742`, r3 `2876509…2884535`, r2 `2888533…2914050` — and the post-run
access log in `S/r2/K1/var/log/nginx/benchmark-access.log` is 511 bytes of real request lines,
e.g. `127.0.0.1 - - [03/Nov/2026:21:47:41 -0300] "GET / HTTP/1.1" 200 34 "-" "python-requests/2.…`.

## Finding 2 — selftest tally (verbatim)

```
RED r1-all-p rc=1 refused=True
RED r2-probe-sha rc=1 refused=True
RED r3-leg-vector rc=1 refused=True
RED r4-missing-leg rc=1 refused=True
RED r5-grader-sha rc=1 refused=True
RED r6-case-sha rc=1 refused=True
RED r7-probe-blob rc=1 refused=True
ACCEPT synthetic rc=0 accepted=True
PATH-INDEPENDENT sha_equal=True
STAGED-STATE changes_on_byte=True
SELFTEST red_refused=7/7 green_ok=0 accept_ok=1 ok=True
```

`--check-receipt` accepts all three receipts with
`CHECK ok cases=7 legs=8 seen_p=8 seen_f=8` / `CHECK stored-predicate=pass derived=pass` /
`PREDICATE R70-C1 pass`, rc 0.

## Finding 3 — the round-69 D-fix holds (path independence), pre- and post-run

`case_dir_sha` hashes only `STAGED_INPUTS` + `var/www/html` + `shim`; `run/server.json` and
`var/log/nginx/*` are excluded by design. Verified four ways:

1. **Frozen digest recomputed in a third, differently-named root**: `--render-table --stage-sha
   $S/stagesha` prints all seven `CASE-SHA` values equal to the instrument's `CASE_SHA`
   (e.g. `CASE-SHA K1 0cf77ab849376a311f85b6cf47d1b2fd61fd21e0644720fb02e541e8ed074fb0`).
2. **Different nesting depth**: K1 staged at `S/depth/x/y/z/K1` digests to
   `0cf77ab8…` — equal to frozen.
3. **Post-run digests**: after the battery wrote access logs, `case_dir_sha` of every case dir
   in `S/r2`, `S/r3` and `S/stagesha` is equal within each case and equal to frozen (all 7
   cases: `equal=True frozen=True`). Non-vacuous: K1's `server.json` carries the absolute
   work path `/fast/scratch/hyaku/kengaku-r70/BatteryReplicate/r2/K1/var/log/nginx/benchmark-access.log`
   and the log has 511 bytes, yet the digest is unchanged.
4. **Byte sensitivity**: mutating `notfound` by one character in a fresh root changes the
   digest (`ADV byte-sensitivity: base==frozen: True | mutated changes digest: True`).

So round 69's path-dependent digest (which hashed `run/server.json` and the access log) is
closed in this instrument: same staged state ⇒ same `case_sha256` across root, depth and run.

## Defects

**None.** No non-reproduced vector or digest; no `SETUP` path fired on the two measured runs;
`--check-receipt` reports no defect lines on any of the three receipts; the kill rule
(`PREDICATE R70-C1 pass`, rc 0) is satisfied under my independent replay.

## Observations (not defects; none edits a frozen element)

- **O1 — digest is blind to `run/server.json` (calibration, low severity).** `run/server.json`
  is not in `STAGED_INPUTS` and holds only the (work-dependent) access-log path; `log_enabled`
  lives in the hashed `run/bodies.json`. Demonstrated: redirecting that file to
  `/tmp/elsewhere.log` leaves the K1 digest at `0cf77ab8…` (`BLIND to server.json log path:
  True`). This matches the frozen wording ("excludes the work path and the server-written
  access log") and cannot drift inside the instrument (`stage_case` derives the path from the
  case root), but it means `case_sha256` is not a complete behavioural identity: a staging
  that silently disabled legs 7/8 via that path would not move the digest.
- **O2 — K6 is one state, not five isolated legs (confirms named limitation iii).** Its five
  red legs all fail by `ConnectionError`, e.g.
  `TEST test_index_page_content E:ConnectionError 0ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded`
  (same for `test_custom_404_page`, `test_log_file_creation`, …), while the shim, configs,
  bodies and an empty access log are staged (`K6 bodies: {'index': 'Welcome to the benchmark
  webserver', 'log_enabled': True, 'notfound': 'Page not found - Please check your URL',
  'server_enabled': False}`, `server_pid=None`). K7 is the only single-leg isolator (leg 4 alone).
- **O3 — live-run witness required.** `--check-receipt` re-derives text fields only; my three
  disjoint pid sets and the timestamped access logs above are the live evidence, consistent
  with named limitation i.

## Provenance note (uncommitted lane edits at run time)

`git status` at 21:45 (before my first battery) already showed ` M plans/round-70-claims.md`
and ` M plans/round70_c2_routed_defects.py`. I read both diffs: the claims change is exactly
the appended **Amendment A1** block, and the C2 change is the single documented E1 pair-order
repair (`diff = [(i, y, x) …]` plus its comment). Neither touches a C1 frozen element, and
`plans/round70_c1_nginx_probe.py` was byte-identical to `master:` (sha256 `9aef6d33…`), which
is the file my two runs executed and the blob `PROBE_BLOB` binds. Not my edits; recorded, not
adjudicated.

## Files written / artifacts
- `W/BatteryReplicate.md` (this report).
- `W/BatteryReplicate/receipt2.txt`, `receipt3.txt` (copied before this report), `compare.txt`,
  `selftest.out`, `render-table.out`, `check-official.txt`, `check-receipt2.txt`,
  `check-receipt3.txt`, `receipt-exists.out`, `sandbox2/` (7 files), `sandbox3/` (7 files).
- Scratch `S` only; **no lane implementation file, predicate, case table, vector, digest or
  kill rule was edited**, and no git/jj mutation was run.
- Tooling: none installed or upgraded.

## Risks / blockers

None blocking. Residual risk is the port-8080 shared loopback: correctness depends on the
probe's `flock`; it held here across three concurrent seats (official + r2 + r3, disjoint pids,
every receipt `free-at-start=True`). If a foreign process grabbed 8080 between the lock and
`port_free`, the probe would report `SETUP port-8080-occupied` (rc 2) rather than a bad vector —
it did not fire.

## Verdict

R70-C1 reproduces independently: **7/7 cases, 56/56 legs, 7/7 vectors and 7/7 staged-input
digests identical between my two runs, to the official receipt, and to the frozen table**;
selftest `red_refused=7/7 … ok=True`; and the round-69 D-fix is confirmed — `case_sha256` is
invariant to work root, nesting depth and post-run state, yet moves on a one-byte input change.
No defect found.
