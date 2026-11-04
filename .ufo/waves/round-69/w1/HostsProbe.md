# HostsProbe — R69-C1 staging hypothesis (K1), round 69 w1

Seat: `HostsProbe` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (L).
Scratch: `/fast/scratch/hyaku/kengaku-r69/HostsProbe` (S), deleted at close.
Observed 2026-11-03 21:06–21:12 -03. No tracked lane file written; no git/jj write command run.

**Hypothesis under test.** The grader's HTTP legs resolve `localhost` only because the sandbox
binds a lane-written `/etc/hosts`; without it `requests` raises `NameResolutionError` and
legs 2–4,7 are scored `F`.

**Verdict: holds in mechanism, imprecise in count.** With the bind removed, **five** of the
eight legs go red — 2, 3, 4, 7, **and 8** — vector `PFFFPPFF`. Leg 2 fails as a plain
`AssertionError` (the grader's own `except (requests.ConnectionError, requests.Timeout)` retry
loop swallows the resolution error); legs 3, 4, 7, 8 fail as `E:ConnectionError` whose message
carries `NameResolutionError`. Direct observation inside the sandbox shows the causal chain:
`/etc/hosts` is the only name source (`/etc/resolv.conf` and `/etc/nsswitch.conf` are absent in
both arms), `localhost` resolves via it and fails with `gaierror -3` without it, while
`nonexistent.invalid` fails in both arms (control).

## Instrument provenance (patched copies are diagnostics, not receipt-grade)

- Lane probe `plans/round69_c1_nginx_probe.py` sha256
  `66b5128dffbb1637b710f9a5d6fb8cacbe7639d89218dfa4b5010539070100ea` (read-only; equals the
  `PROBE … sha256` line of the wave receipt).
- Copies used: `S/probe.py` sha256 `56614ddce467650ac8b67a0171d9c014517910fe1f96284f4ee5e55ef5865b91`
  (arm A), `S/probeB.py` sha256 `fac381b5b414c18dbf83c4cc1ed4fd66320905ae390677d197d5514793f59919`
  (arm B). Both differ from the lane file, so neither could satisfy `--check-receipt`'s
  `own_sha256()` binding; no receipt was produced.
- Patches, exact (`diff -u` against the lane file):
  1. both copies — staging lane made explicit, because `stage_case()` derives the grader path
     from the script's own location and a copy in S would otherwise read a non-existent
     `S/../corpus/...`:
     ```
     -    grader = (lane_root() / GRADER_REL).read_bytes()
     +    grader = pathlib.Path(os.environ["LANE69"]).joinpath(GRADER_REL).read_bytes()
     ```
  2. both copies — one case only (seat bound):
     ```
     -        results = [run_case(work, case) for case in CASES]
     +        results = [run_case(work, case) for case in CASES if case["id"] == "K1"]
     ```
  3. arm B only — the tested removal:
     ```
     -        "--ro-bind", str(root / "etc/hosts"), "/etc/hosts",
     ```
  Nothing else changed: `CASES`, `LEGS`, `NGINX_CONF`, `SITE_CONF`, `SHIM`, `SERVER`, `RUNNER`,
  `stage_case` content and the checker are byte-identical to the lane file.
- Environment: bubblewrap 0.13.1 (`/usr/bin/bwrap`), `/usr/bin/python3` 3.14.8,
  requests 2.34.2 / urllib3 2.8.0. Grader sha256
  `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` = `SHA256SUMS:111`
  (verified). No tool installed or upgraded.

## Arm A — hosts bound (exact argv)

```
LANE69=$L timeout 180 python3 $S/probe.py --lane $L --work $S/workA --evidence-dir $S/evA
```

Verdict lines (battery):

```
PROBE plans/round69_c1_nginx_probe.py sha256 56614ddce467650ac8b67a0171d9c014517910fe1f96284f4ee5e55ef5865b91
GRADER corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0 pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
PORT 8080 free-at-start=True lock=/home/vgpnk/.local/share/kengaku-r69/port-8080.lock
CASE K1 case_sha256=f1e9b6e8085aec69f0b5be14b1f9d9d0c3695c5e7be45ea277ec0cd9fb5bae0e server_pid=1538369 sandbox_rc=0
VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True
LEG-COVERAGE legs=8 seen_p=8 seen_f=0
SUMMARY cases=1 legs=8 mismatches=0 setup=0
PREDICATE R69-C1 fail
rcA=1
```

Raw sandbox stdout (`$S/evA/K1-sandbox.txt`), no exception anywhere:

```
TEST test_nginx_installed P 1ms
TEST test_nginx_running P 2ms
TEST test_index_page_content P 2ms
TEST test_custom_404_page P 1ms
TEST test_nginx_config_syntax P 1ms
TEST test_nginx_config_settings P 0ms
TEST test_log_file_creation P 1001ms
TEST test_log_file_format P 1002ms
```

The battery's final `PREDICATE R69-C1 fail` is the K1-only artifact of the seat bound
(`seen_f=0`: a one-case run cannot give every leg an F witness), not an observation about K1.
Leg 2 is `P`, as the hypothesis requires, and no `NameResolutionError` occurs.

## Arm B — `/etc/hosts` bind removed (exact argv)

```
LANE69=$L timeout 180 python3 $S/probeB.py --lane $L --work $S/workB --evidence-dir $S/evB
```

Verdict lines (battery):

```
PROBE plans/round69_c1_nginx_probe.py sha256 fac381b5b414c18dbf83c4cc1ed4fd66320905ae390677d197d5514793f59919
GRADER corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0 pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
PORT 8080 free-at-start=True lock=/home/vgpnk/.local/share/kengaku-r69/port-8080.lock
CASE K1 case_sha256=866e9fddb100fc3164c6ca19cbf03345021ff7d6d48698699cc1dce7b21b802e server_pid=2030982 sandbox_rc=0
TEST K1 test_nginx_installed P
TEST K1 test_nginx_running F
TEST K1 test_index_page_content F
TEST K1 test_custom_404_page F
TEST K1 test_nginx_config_syntax P
TEST K1 test_nginx_config_settings P
TEST K1 test_log_file_creation F
TEST K1 test_log_file_format F
VECTOR K1 PFFFPPFF expected PPPPPPPP agree=False
LEG-COVERAGE legs=8 seen_p=3 seen_f=5
SUMMARY cases=1 legs=8 mismatches=1 setup=0
PREDICATE R69-C1 fail
rcB=1
```

Raw sandbox stdout (`$S/evB/K1-sandbox.txt`), verbatim (messages as printed, 160/120-char
truncation is the runner's own):

```
TEST test_nginx_installed P 1ms
TEST test_nginx_running F 4002ms Nginx is not running on port 8080
TEST test_index_page_content E:ConnectionError 0ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPCo
TEST test_custom_404_page E:ConnectionError 0ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: /nonexistent-page (Caused by NameResolut
TEST test_nginx_config_syntax P 1ms
TEST test_nginx_config_settings P 0ms
TEST test_log_file_creation E:ConnectionError 0ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPCo
TEST test_log_file_format E:ConnectionError 1ms HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded with url: /test-1793751016 (Caused by NameResoluti
```

Per-leg exception class, therefore: leg 1 `P`; leg 2 `F` (AssertionError, after the grader's
3 × 2 s retry loop — 4002 ms); leg 3 `E:ConnectionError` (NameResolutionError); leg 4 same;
leg 5 `P`; leg 6 `P`; leg 7 same as 3; leg 8 same as 3. The server did bind and was killed
normally (`sandbox_rc=0`); its access log stayed empty in arm B (0 lines) versus 5 lines in
arm A — no request reached it.

## Mechanism, observed inside each staged sandbox

Same `bwrap_argv()` as the two arms, with only the runner tail replaced
(`argv[:-3] + ["/usr/bin/python3", "-c", CODE]`) so the sandbox itself reports its `/etc` and
`getaddrinfo`:

```
--- arm A rc=0
ETC ['hosts', 'nginx']
FILE /etc/hosts True
FILE /etc/resolv.conf False
FILE /etc/nsswitch.conf False
RESOLVE localhost ('127.0.0.1', 8080)
RESOLVE nonexistent.invalid ERR gaierror -3 [Errno -3] Temporary failure in name resolution
--- arm B rc=0
ETC ['nginx']
FILE /etc/hosts False
FILE /etc/resolv.conf False
FILE /etc/nsswitch.conf False
RESOLVE localhost ERR gaierror -3 [Errno -3] Temporary failure in name resolution
RESOLVE nonexistent.invalid ERR gaierror -3 [Errno -3] Temporary failure in name resolution
```

`gaierror -3` = `EAI_AGAIN`; urllib3 wraps it as `NameResolutionError`, requests re-wraps as
`requests.exceptions.ConnectionError`. Arm A's `localhost` entry comes from the bound file —
the control name fails in both arms, so the difference is not a resolver cache or a numeric
shortcut. No `--unshare-net` is used, so loopback is shared, as the probe documents.

## Findings a claim attacker should use

### H1 — R69-C1's frozen predicate is unsatisfiable by the frozen case table (high confidence)

The wave receipt (`W/nginx/receipt.txt`, sha256
`44dd4eb185872e8acee13b48d80fc5e2fa476f91dccb38e9d8321eac749a2263`, mtime 21:06:24, size
2647) records all five frozen vectors agreeing and still fails:

```
VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True
VECTOR K2 PPFPPPPP expected PPFPPPPP agree=True
VECTOR K3 PPPPPPFF expected PPPPPPFF agree=True
VECTOR K4 PPPPPFPP expected PPPPPFPP agree=True
VECTOR K5 FPPPFPPP expected FPPPFPPP agree=True
LEG-COVERAGE legs=8 seen_p=8 seen_f=6
SUMMARY cases=5 legs=40 mismatches=0 setup=0
PREDICATE R69-C1 fail
```

Per-leg tally parsed from that receipt's 40 `TEST` lines:

```
test_nginx_installed         P=4 F=1
test_nginx_running           P=5 F=0  <-- NO F WITNESS
test_index_page_content      P=4 F=1
test_custom_404_page         P=5 F=0  <-- NO F WITNESS
test_nginx_config_syntax     P=4 F=1
test_nginx_config_settings   P=4 F=1
test_log_file_creation       P=4 F=1
test_log_file_format         P=4 F=1
```

This follows from the frozen table itself: the only red witnesses are K2→leg 3, K3→legs 7,8,
K4→leg 6, K5→legs 1,5. **Legs 2 (`test_nginx_running`) and 4 (`test_custom_404_page`) have no
red case anywhere in K1–K5.** The probe's `ok` requires `full_f == len(LEGS)` (`seen_f=8`), and
the frozen sentence says "each of the eight grader legs is observed … `F` in at least one
case", so no run consistent with the frozen vectors can print `pass`. The claims doc's
"Each of the eight legs has one red witness and four green witnesses by construction" is false
for legs 2 and 4 (and the red/green split is otherwise 1/4, not uniform for legs 7 and 8 only
via K3). The measuring command therefore exits 1 and the kill rule's "any leg with no `P` or no
`F` witness" fires on every honest run. Fixing this needs a case-table or predicate change,
both frozen — a claim defect, not a seat defect. (I did not run `--check-receipt`; this tally is
of the receipt's own `TEST`/`VECTOR` bytes plus the frozen table.)

### H2 — `port_free()` reports TIME_WAIT as "occupied" (high confidence; instrument gauge)

`port_free()` binds `127.0.0.1:8080` with `SO_REUSEADDR` unset, but the probe's own HTTP server
sets `allow_reuse_address=True`. After any prior traffic on 8080, the port is unlistenable to
the gauge for ~60 s while the probe's server could still bind. Observed directly:

```
21:08:17 / 21:08:22 / 21:08:32  SETUP port-8080-occupied   (arm B attempts 1-3)
21:08:42  ss -ltnp '( sport = :8080 )'   -> only the header (no listener)
21:08:42  ss -tan  '( sport = :8080 )'   -> TIME-WAIT 127.0.0.1:8080 -> 127.0.0.1:56528
                                            (five rows: 56528, 56532, 56548, 56560, 56576)
python3 bind probe: SO_REUSEADDR=False -> FAIL 98 Address already in use
                    SO_REUSEADDR=True  -> bind OK
```

The five TIME-WAIT rows are exactly arm A's five HTTP requests (legs 2,3,4,7,8) against
127.0.0.1:8080. Consequence: `SETUP port-8080-occupied` is not evidence of a foreign occupant,
and back-to-back batteries/arms within 60 s cannot start honestly. My first arm-A attempt
(~21:07:3x) also hit `SETUP port-8080-occupied` with no listener visible seconds later; that
one is consistent with residual TIME_WAIT from the wave battery (receipt written 21:06:24) —
[INFERENCE], not directly captured with `ss` at that instant. Arm B was run after a 72 s wait;
I retried three times with 3/5/10 s backoff before the wait, and did not loop further. The
receipt's `PORT 8080 free-at-start=True` line is not re-derived by `--check-receipt`, so this
gauge can neither be audited from the receipt nor distinguish "busy" from "recently used".

### H3 — `case_sha256` binds the absolute work path, so it is not re-derivable (high confidence)

Arms A and B stage semantically identical trees (arm B additionally has no bind, but the staged
`etc/hosts` file is written in both). Their `case_sha256` differ:
`f1e9b6e8…` (workA) vs `866e9fdd…` (workB), and the wave receipt's K1 is `ed1cec21…`.
`diff -r workA/K1 workB/K1` shows why — the only content differences are
`run/server.json`'s `"log": "<absolute work root>/var/log/nginx/benchmark-access.log"` and the
log contents after the run. An independent re-stage in a different scratch root cannot
reproduce the receipt's per-case digest. Claim limitation (iii) says the checker "records it
but cannot re-stage"; the sharper statement is that re-staging elsewhere can never match, so
`case_sha256` is a run-distinguisher, not a case-identity witness.

### H4 — Identical vector symbols, different witnesses (calibration)

Arm B's leg 7 is `F` because `requests.get(...)` raises before the grader ever stats the log,
whereas the frozen K3 leg 7 is `F` because the requests succeed and no log exists. Both print
`F`; only the raw sandbox capture separates them (`E:ConnectionError` vs `AssertionError`). The
receipt's `TEST <case> <leg> F` lines carry no witness class, so a leg's red can be
exception-driven (the leg never priced its property) or assertion-driven. For R69-C1 that is
material: legs 2–4,7,8 are all red in an environment without name resolution, and a replay that
lost `/etc/hosts` would look like a legitimate `F` witness unless the raw capture is read. The
probe's own docstring is correct that "an AssertionError is F, any other exception is E (scored
F)", but the receipt strips the distinction.

### Context observation (not my item)

As of 21:09 the claim's measuring-command path
`corpus/evidence/round69/nginx/receipt.txt` did not exist (`ls` ENOENT); the wave receipt is at
`.ufo/waves/round-69/w1/nginx/receipt.txt`. This may be in-flight seat work; I did not run
`--check-receipt` against either path.

## Commands NOT run (explicit)

- The full five-case battery (seat bound to one K1 case per arm; no `--receipt` produced).
- `--check-receipt` and `--selftest` (the patched copy's sha cannot satisfy the probe-sha
  binding; and the seat's item is the staging hypothesis only).
- The C2 gate and every C2 file; the round's census, depth/trio gates.
- No run of K2–K5 in either arm; no second full repetition of either arm (one clean run each,
  plus three bounded retries that all hit `SETUP port-8080-occupied` before arm B ran).
- No lane file edited; no `git`/`jj` write command; no `pacman`; no installs or upgrades; no
  writes to fleet-root tracked files or PATH directories. Only writes: S/* and this report.

## Confidence

H1 high (receipt bytes + frozen table arithmetic + probe `ok` expression). H2 high (direct
`ss`, bind probe, exact TIME-WAIT count match). H3 high (two observed digests + `diff -r`).
H4 high (raw captures). Hypothesis mechanism: high; the enumeration "legs 2–4,7" is corrected
to "legs 2,3,4,7,8".
