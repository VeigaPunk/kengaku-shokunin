# CaseTableAudit — R70-C1 case-table re-derivation (wave w1, 2026-11-03)

Seat: re-derive the seven frozen vectors leg by leg from the grader source, recheck the
leg-coverage arithmetic by hand, and attack the case notes. Read-only seat: no edits to any
frozen element, no battery run, no scratch or fixture needed (`--render-table` without
`--stage-sha` writes nothing). Tooling: system `python3` and `git` only — nothing installed.

## What I ran

| command (at L) | rc | result |
|---|---|---|
| `git -C L rev-parse master` | 0 | `384e9c76415e78093623b3eaff262423a89dbc3e` (tip audited) |
| `sha256sum corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py` | 0 | `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` — equals claims doc, probe `GRADER_SHA256` (plans/round70_c1_nginx_probe.py:9), and `corpus/evidence/round52/graders/SHA256SUMS:111` |
| `python3 plans/round70_c1_nginx_probe.py --render-table` | 0 | output quoted in full below |
| independent recount (python one-liner over the frozen vector string only, not the probe's counting code) | 0 | per-leg counts below |

`--render-table` verbatim:

```
case  setup                                                     vector
K1    all-green end state: service, bodies, config, shim, access log PPPPPPPP
K2    index body differs by one character (server otherwise green) PPFPPPPP
K3    service answers but writes no access log                   PPPPPPFF
K4    config lacks the limit_req_zone rate clause                PPPPPFPP
K5    no nginx binary on PATH (shim absent)                      FPPPFPPP
K6    no HTTP service on 8080 (legs 2, 3, 4, 7, 8 red)           PFFFPPFF
K7    custom-404 body differs by one character (leg 4 red alone) PPPFPPPP
FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP/PFFFPPFF/PPPFPPPP
LEGS 8
LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8
LEG test_nginx_installed p=6 f=1
LEG test_nginx_running p=6 f=1
LEG test_index_page_content p=5 f=2
LEG test_custom_404_page p=5 f=2
LEG test_nginx_config_syntax p=6 f=1
LEG test_nginx_config_settings p=6 f=1
LEG test_log_file_creation p=5 f=2
LEG test_log_file_format p=5 f=2
```

## Leg order = grader file order

`def test_` lines at grader :11, :17, :33, :46, :59, :67, :123, :144 — exactly the probe's
`LEGS` tuple (plans/round70_c1_nginx_probe.py:60-69) and the claims doc's leg order. All
line refs below are `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`
("G:") or `plans/round70_c1_nginx_probe.py` ("P:").

## Leg-by-leg re-derivation (deciding line per leg)

- **Leg 1 `test_nginx_installed`** — G:13-14 `result = subprocess.run(["which", "nginx"] …)` /
  `assert result.returncode == 0`. K5 stages no shim, so `which` exits 1 → F; K1-K4, K6, K7
  stage the shim on `PATH=/shim:/usr/bin:/bin` (P:437-438, staged chmod 0755 P:403-405) → P.
- **Leg 2 `test_nginx_running`** — G:22-23 GET with `timeout=2` + `assert response.status_code == 200`;
  refusal path G:27-30 `except (requests.ConnectionError, requests.Timeout):` → last retry
  `assert False, "Nginx is not running on port 8080"` (G:28-29), else `time.sleep(2)`. K6
  starts no server (P:471-472 `if case["server"]:`) → all 3 attempts refuse → F; others P.
- **Leg 3 `test_index_page_content`** — G:35-36 GET `/` + status 200; G:38-40 body equality
  after `.strip()` vs `"Welcome to the benchmark webserver"`. Server maps `/` → `INDEX, 200`
  (P:240-241). K2 stages `"…webserver!"` → status passes, G:40 fails → F; K6 ConnectionError
  at G:35 → F; others P.
- **Leg 4 `test_custom_404_page`** — G:48-49 GET `/nonexistent-page` + `assert … == 404`;
  server's else-branch returns `NOTFOUND, 404` (P:242-243), so the status assert passes
  whenever the service is up; G:51-53 body equality vs `"Page not found - Please check your URL"`.
  K7 stages `"…URL!"` → only G:53 fails → F; K6 ConnectionError at G:48 → F; others P.
- **Leg 5 `test_nginx_config_syntax`** — G:61-62 `subprocess.run(["nginx", "-t"])` rc 0. The
  shim exits 0 for any argv (P:203-210). K5: no `nginx` on PATH → exec raises
  FileNotFoundError; the runner prints an `E:…` line (P:277-279) and run_case maps every
  non-P/non-F outcome to F (P:484-485) → F; others P.
- **Leg 6 `test_nginx_config_settings`** — conf.d checks G:86 (`listen\s+8080`) and G:89
  (`root\s+/var/www/html`); after re-reading `/etc/nginx/nginx.conf` (G:93-104) the same
  `config_content` is checked for `log_format` (G:111, G:113), the four fields
  `$time_local $request_method $status $http_user_agent` (G:107-108, G:114) and
  `limit_req_zone.*?rate=10r/s` (G:119-120). K4 renders `NGINX_CONF` with `rate=""`
  (P:391-395; `{rate}` placeholder P:176), removing only the `limit_req_zone` line from
  nginx.conf → only G:120 fails → F alone; others P.
- **Leg 7 `test_log_file_creation`** — G:126 GET `/`, G:129 sleep 1, G:141
  `assert log_found` for `/var/log/nginx/benchmark-access.log` (G:133-140). K3: `log=False`
  → file not staged (P:397-399) and server started with `--log ""` so `log_line` returns
  early (P:227-229) → F. K6: GET at G:126 raises → F. Others: file staged empty and the log
  dir is bind-mounted rw (P:432-434) → P.
- **Leg 8 `test_log_file_format`** — G:146-147 GET `/test-<ts>`, G:151 sleep 1, G:157-163
  read log, then four regexes: timestamp G:165-166, method G:169-170, status G:173-174,
  user-agent G:177-178. The shim's log line (P:230-232)
  `127.0.0.1 - - [%s] "GET %s HTTP/1.1" %d %d "-" "%s"` with `%d/%b/%Y:%H:%M:%S %z` (P:230)
  satisfies all four (e.g. `03/Nov/2026:… +0000`; ` 404 `; trailing quoted UA, `$` matches
  before the final `\n`). K3/K6: no/empty content or the GET raises → F; others P.

**Result: all seven frozen vectors agree with the re-derivation; zero disagreements.**
K6's `PFFFPPFF` is forced: legs 1, 5, 6 (G:13, G:61, G:67-121) never touch the socket, legs
2, 3, 4, 7, 8 (G:22, G:35, G:48, G:126, G:147) each begin with a request to :8080. K7's
`PPPFPPPP` is forced: single-position delta vs K1, red at G:53 only.

## Hand arithmetic vs `--render-table`

Independent recount over the frozen vector string (columns, not the probe's code):
`installed p=6 f=1 (F K5)`, `running p=6 f=1 (F K6)`, `index p=5 f=2 (F K2,K6)`,
`custom_404 p=5 f=2 (F K6,K7)`, `config_syntax p=6 f=1 (F K5)`, `config_settings p=6 f=1
(F K4)`, `log_creation p=5 f=2 (F K3,K6)`, `log_format p=5 f=2 (F K3,K6)` — 56 observations.
Identical to the probe's `LEG` lines and to the claims doc's freeze-time counts;
`LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8`. The counts are computed from `CASES` by
`render_table` (P:844-869) before any data exists, as claimed.

## Case-note attack

1. **K6 "legs 2, 3, 4, 7, 8 red" — exact as a set, and complete.** Those five are exactly
   the socket-first legs (citations above); no sixth leg can redden and none of the five can
   stay green with nothing listening (leg 2 terminates in G:28-29 after 3 tries). The note
   predicts a set, not per-leg isolation; claims limitation (iii) says precisely that
   ("its five red legs are not independently isolated; only K7 isolates one leg (4)").
   No overstatement.
2. **K7 "leg 4 red alone" — exact.** Verified single-position delta (`PPPFPPPP` vs K1) and
   mechanism: G:49 status passes because the server answers 404 (P:243), G:53 fails on the
   trailing `!`. No other leg reads the notfound body (leg 8 greps the log for `/test-<ts>`,
   written regardless of body; leg 3 uses the index body).
3. **Other notes checked:** K2 (leg 3 alone), K4 (leg 6 alone — the rate regex runs against
   nginx.conf content at G:119, which is exactly where the template's `{rate}` sits),
   K3 (legs 7+8, one cause), K5 (legs 1+5, one cause) — all exact; none claims more
   isolation than the vector shows.
4. **Disclosure nit (documentation, not a frozen element):** the claims doc's case-table
   "staged end state" wording differs from the probe `CASES` notes for K1, K6, K7 (claims K1
   "all-green: …" vs P:78 "all-green end state: …"; claims K6 "(shim, config, bodies staged)"
   vs P:126 "(legs 2, 3, 4, 7, 8 red)"; claims K7 without "(leg 4 red alone)", P:148 with it).
   "`--render-table` must byte-equal it" is therefore satisfiable only at vector level — and
   the vectors + FROZEN-VECTOR line do byte-equal. Read the byte-equality clause as
   vector-level; no predicate impact.
5. **Cause-bundling ceiling (depth caveat, not a defect):** F witnesses bundle by cause —
   K5 reddens legs 1+5 jointly (leg 5's only F witness), K6 reddens 2,3,4,7,8 jointly (leg
   2's only F witness), K3 reddens 7+8 jointly. Single-leg F isolation exists only for legs
   3 (K2), 4 (K7), 6 (K4). Consequence: a grader-side behaviour change confined to one
   bundled leg (e.g. leg 5's rc parsing or leg 2's retry semantics) cannot move any frozen
   vector; the table prices leg *outcomes*, not causes. Limitation (iv) points at this
   ("case_sha256 binds staged inputs, not the grader's own behaviour") and (iii) covers
   K6's bundle, but the K5 bundle (legs 1+5) is not spelled out anywhere. The frozen
   predicate ("every leg observed F in ≥1 case") is nonetheless priced by construction.
6. **Instrument mapping worth knowing when reading receipts:** in K6, legs 3/4/7/8 go red as
   uncaught `requests.exceptions.ConnectionError` (runner `E:…` lines, mapped to F at
   P:485) while leg 2 goes red via `assert False` (G:29). Both are pytest failures; the
   frozen vector prices outcomes.

## Verdict

**R70-C1 case table: the frozen table prices all eight legs both ways before data — YES.**
All seven frozen vectors re-derive leg by leg from the grader source plus the staged
environment; the hand recount, `--render-table`, and the claims doc agree byte-for-byte
(`LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8`, 56 observations); K6's five-leg note and
K7's single-leg note are both exact; no note overstates isolation. Findings are two
disclosure nits (item 4 note-text paraphrase, item 5 K5-bundle not spelled out), neither a
frozen-element defect; reported, not edited.

Residual risk: outcome-level pricing cannot detect grader-side changes confined to a single
bundled leg (legs 1/5 via K5, leg 2 via K6, legs 7/8 via K3+K6) — inherent to the design,
covered by limitations (iii)/(iv) once item 5's K5 note is read alongside them. Vectors for
legs 7/8 P additionally assume the lane shim's log format satisfies all four grader regexes
(verified here by inspection, P:230-232 vs G:165-178); a mismatch would surface as an honest
vector-miss under the kill rule, not a silent pass.
