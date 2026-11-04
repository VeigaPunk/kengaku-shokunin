# LegPricing — Kengaku R69 w1 seat report (attack seat: R69-C1 case design)

Seat: LegPricing · 2026-11-03 · leaf, no subagents. Frozen inputs read in full before any command:
`plans/round-69-claims.md`, `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`
(sha256 `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` — matches the frozen pin and
`SHA256SUMS:111`), `plans/round69_c1_nginx_probe.py` (686 ln, read in full).
Lane tip observed `b288e8e0` (round moved past base `a518980e`); the three frozen files above are clean at
the tip (absent from `git status --porcelain`, which shows only sibling C2 target files: `SKILL.md`,
`corpus/QUALITY.md`, `corpus/knowledge/tb2-network-service-offline-grader.md`, `corpus/lessons/round-68.md`
+ untracked evidence/wave dirs). No lane file touched by this seat.

## Verdict up front

**R69-C1 as frozen cannot print `PREDICATE R69-C1 pass` — two independent structural blockers, both proven
from the instrument's own bytes without running the battery.**

- **F-A (case design / leg coverage).** Legs 2 `test_nginx_running` and 4 `test_custom_404_page` have **no
  red witness in the frozen case table** (P in all five cases). The probe's own gate
  `ok = (mismatches == 0 and setup == 0 and full_p == len(LEGS) and full_f == len(LEGS))`
  (plans/round69_c1_nginx_probe.py:465) requires `full_f == 8`; the frozen table yields `full_f=6`.
  With observed == frozen, `ok=False`; any observed deviation is itself a `mismatches` kill. So the frozen
  predicate ("every one of the eight grader legs is observed P in at least one case and F in at least one
  case") is **unsatisfiable in all worlds**. The claims doc's own sentence "Each of the eight legs has one
  red witness and four green witnesses by construction" is arithmetically false for its own table: the five
  vectors contain exactly 6 red cells (K2:1, K3:2, K4:1, K5:2) for 8 legs — and the doc's very next
  sentence, "a leg the table leaves un-red is a leg the replay does not price", names precisely legs 2 and 4.
- **F-B (receipt re-derivation gate).** The battery writes VECTOR lines with 6 whitespace tokens
  (L460-461: `VECTOR <id> <vector> expected <expected> agree=<bool>`), while `check_receipt` demands
  exactly 5 (L513 `if len(parts) != 5: defect("vector-line", ln)`). Every genuine battery receipt is
  therefore refused with `DEFECT vector-line` ×5 → `vectors` empty → `DEFECT case-set` + all 40 TEST lines
  uncounted (`leg-coverage … p=0 f=0` ×8) → rc 1, **regardless of how the run went**. The
  `--check-receipt` green path is unreachable for any receipt the battery can produce. Demonstrated on a
  byte-format-faithful ideal receipt (below). The `--selftest` cannot expose F-B: its forged fixtures are
  built with the same 6-token writer format (L602) and the tally counts refusal by any defect
  (`red_refused=5/5`), so the checker's semantic path is never exercised green; `--green-receipt` would
  fail against any producible receipt.

Fix direction (for the round to decide; this seat edits nothing, per lane bounds): add two cases — one that
turns leg 2 red (requires a CASES field to skip `start_server` and leave 8080 unbound; today a dead server
aborts the case at the READY-wait instead of yielding leg F) and one that turns leg 4 red (a wrong
`notfound` body, mirroring K2's index mutation) — bringing red cells to 8; and reconcile the VECTOR token
count between writer (L460-461) and parser (L513). Both are frozen-predicate amendments under the claims'
own dated-amendment clause, before any after-receipt is scored.

## What I ran (exact argv)

1. `mkdir -p /fast/scratch/hyaku/kengaku-r69/LegPricing`
2. `wc -l <grader> <probe>`; `sha256sum <grader> <probe>` → grader `045cc716…` (== frozen pin); probe `66b5128dffbb1637b710f9a5d6fb8cacbe7639d89218dfa4b5010539070100ea`
3. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse --short HEAD` → `b288e8e0`
4. `git -C … status --porcelain | wc -l` → `8`; `git -C … diff --stat a518980e -- <claims> <probe> <grader>` → the two plans files are pure insertions (added after the base, clean at tip); grader untouched
5. `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c1_nginx_probe.py --render-table` → byte-matches the frozen claims table (K1–K5 notes+vectors, `FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP`, `LEGS 8`)
6. `python3 /fast/scratch/hyaku/kengaku-r69/LegPricing/pricing_driver.py <scratch>` — pure-function: imports the probe module, tallies P/F witnesses from the frozen CASES, then runs `check_receipt` on an ideal receipt in the battery's exact 6-token VECTOR format
7. `python3 /fast/scratch/hyaku/kengaku-r69/LegPricing/semantic_driver.py <scratch>` — same receipt in the checker's own 5-token VECTOR format, isolating the semantic layer

**Commands NOT run (state per seat spec):** the battery itself (`--lane … --work … --receipt … --evidence-dir …`) — no port-8080 bind, no flock, no bwrap, no live K1–K5 execution; `--check-receipt` on any real receipt (none exists: `corpus/evidence/round69/` holds only `c2-receipts/` and `gates/`); `--selftest` and `--green-receipt`; any lane write; any git/jj write command; any tool install (none needed; pacman guard respected). The vectors below are my **static leg-by-leg derivation from the grader source**, which agrees with all five frozen vectors; the defects found are independent of sandbox behavior.

## Raw output lines that carry a verdict

From (6), witness counts implied by the frozen table:

```
LEG test_nginx_running                 P=5 F=0
LEG test_custom_404_page               P=5 F=0
full_p=8 full_f=6 (run_battery ok requires both == 8)
battery ok-condition satisfiable with observed==frozen: False
```

From (6), `check_receipt` on an **ideal** receipt whose vectors EQUAL the frozen table, written in the battery's exact 6-token format:

```
check_receipt(ideal) rc = 1
DEFECT vector-line VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True     (×5, one per case)
DEFECT case-set got=[] want=['K1', 'K2', 'K3', 'K4', 'K5']
DEFECT leg-coverage test_nginx_installed p=0 f=0                       (×8, all legs)
CHECK stored-predicate=pass derived=fail
PREDICATE R69-C1 fail
```

From (7), the same semantically perfect receipt in the checker's own 5-token format — the format bug disappears and **only** the two un-red legs remain:

```
check_receipt(five-token-format, vectors==frozen) rc = 1
CHECK ok cases=5 legs=8 seen_p=8 seen_f=6
DEFECT leg-coverage test_nginx_running p=5 f=0
DEFECT leg-coverage test_custom_404_page p=5 f=0
CHECK stored-predicate=pass derived=fail
PREDICATE R69-C1 fail
```

## Per-leg pricing (item 2) and the demanded lines

Runner fairness (item 3) first, since every leg depends on it: **PASS** — `RUNNER` (probe L~218-235) loads the sha-pinned grader from `/tests/test_outputs.py` (ro-bound), iterates all eight legs in grader file order via `getattr`, and per leg does `try: fn()` → `P`, `except AssertionError` → `F`, `except BaseException` → `E:<name>` (mapped to F by `run_case`). It contains no mock/patch/skip/monkeypatch/env-override, no reordering, no early exit; the probe never evaluates a leg's condition itself. Two harness-side pre-emptions to disclose, neither of which pre-empts an assertion: (i) `start_server` aborts the whole case (RuntimeError at the READY-wait) if the staged server fails to bind — a dead service can never be graded F on any leg, it kills the battery; (ii) the shim/hosts/config/log files are staged inputs the grader consumes — its own asserts still decide every outcome.

```
LEG 1 test_nginx_installed          priced_by=K5 attributes=PASS
LEG 2 test_nginx_running            priced_by=NONE attributes=FINDING no red witness in the frozen table (P in 5/5); F-side unpriceable in this harness — the HTTP service is probe-started before bwrap, CASES has no service-down field, and a dead server aborts run_case at the READY-wait instead of yielding leg F; the leg-coverage kill rule therefore fires by construction
LEG 3 test_index_page_content       priced_by=K2 attributes=PASS
LEG 4 test_custom_404_page          priced_by=NONE attributes=FINDING no red witness in the frozen table (P in 5/5); CASES exposes no field that can mutate the 404 status/body (K2 mutates index only), so the F side is unpriceable by construction — same leg-coverage kill as leg 2
LEG 5 test_nginx_config_syntax      priced_by=K5 attributes=FINDING red witness is K5's shim absence — the same staged defect that reds leg 1 — so the syntax axis itself is never exercised: SHIM exits 0 unconditionally without reading any config, so a syntactically broken staged nginx.conf would still green this leg, and no case field can stage one
LEG 6 test_nginx_config_settings    priced_by=K4 attributes=PASS
LEG 7 test_log_file_creation        priced_by=K3 attributes=PASS
LEG 8 test_log_file_format          priced_by=K3 attributes=PASS
```

Per-leg detail — exact assertion → deciding staged artifact → red case → false-green window / docstring weakness:

- **LEG 1** — asserts `which nginx` rc==0 inside bwrap (PATH=`/shim:/usr/bin:/bin`). Decided by staged `shim/nginx` presence (+x), K5 red via absent shim → `AssertionError`. *Weaker than docstring "Nginx is installed": presence-only; the binary is never executed (`nginx -v` never asked); any +x file named `nginx` greens it.* No frozen case stages a garbage binary, so no vector is wrong; K5 prices the PATH axis correctly.
- **LEG 2** — 3 retries of `requests.get("http://localhost:8080", timeout=2)`, assert status 200. Decided by the probe-started host-side Python server (shared loopback; no `--unshare-net`). *Weaker than docstring "running and listening on port 8080": greens any HTTP-200 talker on loopback — K5's own frozen vector `FPPPFPPP` shows leg 2 P with zero nginx in the sandbox.* Plus FINDING: no red witness, and none expressible (see runner note (i)).
- **LEG 3** — assert status 200 AND `response.text.strip() == "Welcome to the benchmark webserver"` (exact). Decided by the server `--index` payload; K2's one-character diff reds it. Strongest leg; matches docstring. (Note: `requests.get` without timeout — a hung server would hit the bwrap `timeout=300` and crash the case, not yield F; unreachable with the fixed SERVER.)
- **LEG 4** — assert status 404 AND body `== "Page not found - Please check your URL"` (exact). Decided by the server `--notfound` payload; identical in all five cases → always P. Assertion itself matches docstring; the pricing is the defect (no red witness).
- **LEG 5** — asserts `nginx -t` rc==0. Decided by the staged SHIM (`if [ "$1" = "-t" ]; then exit 0 fi; exit 0` — config-ignoring). K5 red via `FileNotFoundError` → `E:` → F. *Weaker than docstring "configuration is syntactically correct": the syntax axis is never exercised; a garbage nginx.conf greens the leg.* Claims limitation (ii) discloses the shim stand-in but the leg-coverage arithmetic still requires this leg's F, which exists only as the binary-absence side effect shared with leg 1.
- **LEG 6** — on `conf.d/benchmark-site.conf`: regex `listen\s+8080`, `root\s+/var/www/html`; on `nginx.conf`: substring `log_format`, the four field substrings, and regex `limit_req_zone.*?rate=10r/s`. Decided by staged config bytes; K4 (`rate_limit: False` → `{rate}` slot empty) reds the rate regex → `AssertionError`. *Weaker than docstring semantics: pure text presence — commented-out directives would green it; `.*?` without DOTALL false-reds a wrapped directive (staged conf is single-line, so the frozen vector is correct).*
- **LEG 7** — GET `/`, sleep 1s, assert `/var/log/nginx/benchmark-access.log` exists. Decided by staging: `stage_case` pre-creates the empty file iff `log=True`; K3 stages no file AND silences the server writer (`--log ""` → `log_line` no-op) → exists() False → F. *Weaker than docstring "are created": existence-only; in every green case the green is set by the pre-staged empty file, not by the service writing. Within this harness the window is unreachable (the fixed SERVER writes on every request when log=True), and leg 8 backstops an empty file.*
- **LEG 8** — GET `/test-<epoch>`, sleep 1s, read log, four whole-content regexes: timestamp `\d{2}/\w{3}/\d{4}:…\s[+-]\d{4}`, method `(GET|POST|…)`, status `\s(\d{3})\s`, UA `"[^"]*"$`. K3 reds it (file absent → `log_content=""` → timestamp assert F). *Weaker than docstring "correct format with all required fields": searches are whole-content, not per-line — one stale line (e.g. leg 7's `GET /` line) satisfies all four even if the unique request was never logged; the `unique_path in log_content` break only selects content when multiple files exist (list has one); UA regex anchors at content END so only the last line's tail is priced; method/status regexes match anywhere. With the fixed SERVER these never produce a wrong frozen vector.*

## For the claim's attacker (condensed)

Run the measuring command exactly as frozen and the battery prints `LEG-COVERAGE legs=8 seen_p=8 seen_f=6` + `PREDICATE R69-C1 fail` with all five `VECTOR … agree=True` — C1 dies by construction, not by sandbox accident. Even a hypothetical all-agree receipt is refused by `--check-receipt` (F-B), so no producible artifact can satisfy the frozen predicate or the `--check-receipt` leg of the kill rule. The C1 selftest's `red_refused=5/5` cannot distinguish refusal-by-format from refusal-by-semantics, and its fixtures reuse the buggy writer format (L602), so the checker's green path is untested and unreachable. My static derivation confirms all five frozen vectors are otherwise correctly derived from the grader source (K2/K3/K4/K5 reds land exactly where the claims say), and the round's disclosed K1 smoke run (`PPPPPPPPP`—i.e. `PPPPPPPP`) is consistent with it.

Residual risk: no live battery run by this seat (port/bwrap untouched), so sandbox-level surprises (DNS/%z/timing) are unexercised here; nothing above depends on them. Scratch receipts copied inline above; scratch dir deleted before yield. No tools installed.
