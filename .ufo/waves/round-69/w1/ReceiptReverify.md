# ReceiptReverify — R69-C1 independent replay, determinism and checker cross-check

Seat: executor, wave kengaku-r69-w1 (leaf; no spawn used, no labrat needed).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` @ `b288e8e0` (freeze commit; tree clean except
the wave's own untracked `.ufo/waves/round-69/w1*` paths).
Scratch: `/fast/scratch/hyaku/kengaku-r69/ReceiptReverify` (deleted before yield; receipts copied to
`.ufo/waves/round-69/w1/ReceiptReverify/`).
I edited nothing: not the instrument, not either receipt, not the claims doc, no tracked file.

## Verdict in one line

The frozen R69-C1 predicate **cannot pass**: two of its eight legs have no red witness in the frozen
case table (`test_nginx_running`, `test_custom_404_page`), and independently `--check-receipt`'s
VECTOR parser disagrees with the receipt writer's own format, so every genuine receipt is refused.
Two independent live runs agree on all 40 observations and both print `PREDICATE R69-C1 fail`, rc 1.

## Inputs read in full before any command

- `plans/round-69-claims.md` (sha256 `0088cfb0034897ccf3e57e4dd86a532d5ca0882249d40bc033a1fe7786a53a41`,
  matches the freeze control's declared hash).
- `plans/round69_c1_nginx_probe.py` (686 lines; sha256
  `66b5128dffbb1637b710f9a5d6fb8cacbe7639d89218dfa4b5010539070100ea`, identical at freeze commit
  `b288e8e0` — `git show b288e8e0:plans/round69_c1_nginx_probe.py | sha256sum` printed the same).
  Read `check_receipt`, `run_selftest`, `run_battery`, `stage_case`, `case_dir_sha`, `port_free`,
  `acquire_port_lock`, `render_table` line by line.
- Grader `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py` in full
  (sha256 `045cc716…4acda0`, equals `corpus/evidence/round52/graders/SHA256SUMS:111`).

## What I ran (exact argv, lane cwd)

1. `python3 plans/round69_c1_nginx_probe.py --render-table`
2. `python3 plans/round69_c1_nginx_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r69/ReceiptReverify/work --receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-69/w1/ReceiptReverify/receipt2.txt`
   — attempts 1 and 2; attempt 3 (same argv) produced the receipt.
3. `python3 plans/round69_c1_nginx_probe.py --check-receipt <my receipt2.txt>` → `check.txt`
4. `python3 plans/round69_c1_nginx_probe.py --check-receipt .ufo/waves/round-69/w1/nginx/receipt.txt`
   → `check-nginxbattery.txt`
5. `python3 plans/round69_c1_nginx_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r69/ReceiptReverify/st --green-receipt <my receipt2.txt>` → `selftest.txt`
6. `python3 plans/round69_c1_nginx_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r69/ReceiptReverify/st2 --green-receipt .ufo/waves/round-69/w1/nginx/receipt.txt`
   → `SETUP work-dir-required (not a directory)`, rc 2 (the work dir must pre-exist; `st` did).
7. Staged-digest recomputation and path-dependence probe by importing the probe
   (`stage_case` + `case_dir_sha` into `S/dep-a`, `S/dep-b`, `S/stage`; no port, no writes outside S).
8. Synthetic parser isolation: rewrote the VECTOR lines of a *copy* of my receipt in scratch into the
   5-field form the checker parses, then injected F witnesses for legs 2/4 consistently in TEST lines
   and stored vector → `parser-probe.txt`. These are **synthetic scratch fixtures, not receipts**.
9. Environment/diagnostic: `ss -ltnp '( sport = :8080 )'`, `ss -tanp '( sport = :8080 )'`,
   `fuser -n tcp 8080`, a direct `bind()` probe with/without `SO_REUSEADDR`, `ps` for probe processes,
   `sha256sum` of grader/claims/probe, `git cat-file -e a518980e:corpus/evidence/round69/nginx/receipt.txt`,
   `grep -c 'executed 2 of 8' SKILL.md`, `grep -c 'executed 3 of 8' SKILL.md`,
   `grep -cE '^\|[[:space:]]*S241[[:space:]]*\|' corpus/SOURCES.md`, `grep -n '^def test_' <grader>`,
   `git show b288e8e0:.ufo/waves/round-69/nginx-control.txt | sha256sum`,
   `grep -rn 'FROZEN-SHA' .`, `diff` of the verdict lines of the two receipts.

## Result 1 — my live battery (independent of NginxBattery)

Receipt: `.ufo/waves/round-69/w1/ReceiptReverify/receipt2.txt`
sha256 `5b329bfaec1e77ceed4574ab1ac47c35dd6e0f71f9e67e2469867632cab1ee64`.

```
PROBE plans/round69_c1_nginx_probe.py sha256 66b5128dffbb1637b710f9a5d6fb8cacbe7639d89218dfa4b5010539070100ea
GRADER corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0 pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
PORT 8080 free-at-start=True lock=/home/vgpnk/.local/share/kengaku-r69/port-8080.lock
CASE K1 case_sha256=37d4d496… server_pid=1732482 sandbox_rc=0
CASE K2 case_sha256=b2f64b2b… server_pid=1737243 sandbox_rc=0
CASE K3 case_sha256=ab907d25… server_pid=1745467 sandbox_rc=0
CASE K4 case_sha256=fb60bb14… server_pid=1752841 sandbox_rc=0
CASE K5 case_sha256=55a9810c… server_pid=1762153 sandbox_rc=0
VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True
VECTOR K2 PPFPPPPP expected PPFPPPPP agree=True
VECTOR K3 PPPPPPFF expected PPPPPPFF agree=True
VECTOR K4 PPPPPFPP expected PPPPPFPP agree=True
VECTOR K5 FPPPFPPP expected FPPPFPPP agree=True
LEG-COVERAGE legs=8 seen_p=8 seen_f=6
SUMMARY cases=5 legs=40 mismatches=0 setup=0
PREDICATE R69-C1 fail
rc=1
```

Five distinct `server_pid`s, all `sandbox_rc=0`: the live witness is present and per-case.

## Result 2 — determinism: my run vs NginxBattery vs frozen table

`diff` of `^(CASE|TEST|VECTOR|LEG-COVERAGE|SUMMARY|PREDICATE)` lines, with `case_sha256=` and
`server_pid=` stripped, between my `receipt2.txt` and `.ufo/waves/round-69/w1/nginx/receipt.txt`
(sha256 `44dd4eb185872e8acee13b48d80fc5e2fa476f91dccb38e9d8321eac749a2263`): **empty** (`DIFF_EMPTY=yes`).

Per-case vectors (mine / NginxBattery / frozen):

| case | mine | nginx | frozen | verdict |
|---|---|---|---|---|
| K1 | PPPPPPPP | PPPPPPPP | PPPPPPPP | AGREE |
| K2 | PPFPPPPP | PPFPPPPP | PPFPPPPP | AGREE |
| K3 | PPPPPPFF | PPPPPPFF | PPPPPPFF | AGREE |
| K4 | PPPPPFPP | PPPPPFPP | PPPPPFPP | AGREE |
| K5 | FPPPFPPP | FPPPFPPP | FPPPFPPP | AGREE |

So the 40 observations are deterministic across two seats, and the observed vectors equal the frozen
table. `mismatches=0 setup=0` in both receipts. `--render-table`'s five vectors also equal the claims
doc's five rows (the row *notes* differ: claims `all-green: …` vs render `all-green end state: …`,
and claims carry markdown backticks around `limit_req_zone`/`nginx`; the vector column is byte-equal).

## Result 3 — the predicate is unsatisfiable on the frozen table (the headline)

`run_battery` computes `ok = (mismatches == 0 and setup == 0 and full_p == 8 and full_f == 8)`, i.e.
it requires every leg to be `F` in at least one case. Witness counts derived from the frozen
`CASES` table (computed by importing the probe):

```
leg1 test_nginx_installed         P=4 F=1
leg2 test_nginx_running           P=5 F=0   <-- no red witness
leg3 test_index_page_content      P=4 F=1
leg4 test_custom_404_page         P=5 F=0   <-- no red witness
leg5 test_nginx_config_syntax     P=4 F=1
leg6 test_nginx_config_settings   P=4 F=1
leg7 test_log_file_creation       P=4 F=1
leg8 test_log_file_format         P=4 F=1
full_f with observed==expected: 6
```

Proof: for `ok` to be true, `mismatches == 0` forces every observed vector to equal its frozen
vector; with observed == frozen the number of legs with an `F` witness is 6, not 8, so `ok` is false.
If any vector differs from the frozen vector, `mismatches > 0` and `ok` is false too. Hence
`PREDICATE R69-C1 pass` is **unreachable for every possible run of the frozen instrument on the frozen
table**, not merely unlucky. The claims doc's statement "Each of the eight legs has one red witness and
four green witnesses by construction" is false for legs 2 and 4 (5 green, 0 red).

This is not an artifact of staging: leg 2 (`test_nginx_running`) only needs HTTP 200 on
`localhost:8080`, and leg 4 (`test_custom_404_page`) only needs the 404 body, which all five cases
stage identically (`notfound` is the same string in K1–K5, and no case suppresses the server). Both are
green in all five cases by construction of `CASES` and `stage_case`.

Empirically confirmed by both seats: `LEG-COVERAGE legs=8 seen_p=8 seen_f=6` + `PREDICATE R69-C1 fail`
in mine and in NginxBattery's receipt.

## Result 4 — `--check-receipt` refuses every genuine receipt (independent second defect)

`--check-receipt` on my genuine receipt (`check.txt`, rc 1) and on NginxBattery's
(`check-nginxbattery.txt`, rc 1) produce the identical 15-defect list:

```
CHECK ok cases=5 legs=8 seen_p=0 seen_f=0
DEFECT vector-line VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True
… (same for K2–K5)
DEFECT case-set got=[] want=['K1', 'K2', 'K3', 'K4', 'K5']
DEFECT leg-coverage test_nginx_installed p=0 f=0
… (all eight legs p=0 f=0)
DEFECT stored-predicate PREDICATE R69-C1 fail
CHECK stored-predicate=fail derived=fail
PREDICATE R69-C1 fail
```

Cause, from the source: the writer emits
`VECTOR <case> <vec> expected <vec> agree=<bool>` — six whitespace fields — while `check_receipt`
does `parts = ln.split(); if len(parts) != 5: defect("vector-line", ln); continue`. Every VECTOR
line is therefore discarded, `vectors` stays empty, which cascades into `case-set` and eight
`leg-coverage` defects. No receipt the writer can produce can satisfy the parser.

Synthetic isolation (`parser-probe.txt`; scratch copies, **not** receipts, not scored):

- **B** — same bytes with VECTOR lines rewritten to the 5-field form the parser expects:
  `CHECK ok cases=5 legs=8 seen_p=8 seen_f=6` and only
  `DEFECT leg-coverage test_nginx_running p=5 f=0`, `DEFECT leg-coverage test_custom_404_page p=5 f=0`
  (+ the stored predicate, still `fail`). This proves the parser bug is separate from the table gap.
- **C** — B plus a forged `PREDICATE R69-C1 pass` line: still refused on the two coverage defects
  (`CHECK stored-predicate=pass derived=fail`). A correct run cannot pass the checker even with the
  stored verdict forged.
- **D** — B plus consistent F witnesses injected for K1 legs 2 and 4 (`PFPFPPPP` in both TEST lines
  and stored vector): coverage becomes `seen_f=8`, and the checker then fails on
  `DEFECT vector-mismatch K1 PFPFPPPP != PPPPPPPP`. Satisfying coverage requires contradicting the
  frozen table; satisfying the frozen table fails coverage. Mutually exclusive — same conclusion as
  the proof in Result 3, reached from the checker side.

The `--selftest` green arm shows the same thing on real bytes (`selftest.txt`):

```
RED r1-all-p rc=1 refused=True
RED r2-probe-sha rc=1 refused=True
RED r3-leg-vector rc=1 refused=True
RED r4-missing-leg rc=1 refused=True
RED r5-grader-sha rc=1 refused=True
GREEN receipt rc=1 accepted=False
SELFTEST red_refused=5/5 green_ok=0 ok=False
rc=1
```

`red_refused=5/5` is vacuous: all five forged fixtures are refused by the VECTOR-parser bug, not by
their intended defect (fixture `r1-all-p`, an all-P vector set, would be refused for
`vector-mismatch` only after the parser is fixed — demonstrated by B/C above). The green arm fails on
a genuine receipt, so the selftest's own contract (`ok`) cannot be met. Note `run_selftest`'s
`dup_leg` parameter is never used by any of the five fixtures — dead code; duplicate-leg collision is
unpriced.

## Result 5 — `case_sha256` is path-dependent, not a content digest

Two `stage_case` calls of the same case into different work roots give different digests:

```
dep-a K1 6fd1df4637828cbe431f76c9ec1324d8415f337412da4bdc2a6c1e6089980df1
dep-b K1 6c4c60e79e2ab74d51dfc6b00e3efba8f6e87b29b2182e9dcf6a692179403fc2
dep-a restage K1 6fd1df4637828cbe431f76c9ec1324d8415f337412da4bdc2a6c1e6089980df1
dep-a K3 ab907d25ffb0cb5b7392f8e11b8765cf193b34866cfd030379c7d62e3657445c
dep-b K3 ab907d25ffb0cb5b7392f8e11b8765cf193b34866cfd030379c7d62e3657445c
```

Cause: `run/server.json` embeds the absolute access-log path
(`"log": "<root>/var/log/nginx/benchmark-access.log"`), and `case_dir_sha` hashes it. K3 has
`log=False` → `"log": ""` → stable. Consequently the receipt's `case_sha256` for K1/K2/K4/K5 cannot be
reproduced or compared across work roots: mine are `37d4d496…`, `b2f64b2b…`, `fb60bb14…`, `55a9810c…`
vs NginxBattery's `ed1cec21…`, `149d9bb2…`, `68de9599…`, `0460d9d2…`; K3 matches
(`ab907d25…`) in both. `check_receipt` never reads `CASE` lines at all, so the field is unverified
either way. Claims-doc limitation (iii) says the checker "records it but cannot re-stage"; in fact it
neither records nor re-derives it, and the value is not a digest of the case.

## Result 6 — the port gate refuses spuriously (blocks other seats)

Attempts 1 and 2 both printed `SETUP port-8080-occupied`, rc 2, while nothing was listening:

```
$ ss -ltnp '( sport = :8080 )'
State Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
$ ss -tanp '( sport = :8080 )'
TIME-WAIT 0 0 127.0.0.1:8080 127.0.0.1:56548
… (5 TIME-WAIT entries)
$ python3 - <<'PY'  # direct bind probe
bind reuse=False ERR 98 EADDRINUSE
bind reuse=True OK
PY
```

`port_free()` does `s.bind(("127.0.0.1", port))` with no `SO_REUSEADDR`, so TIME-WAIT sockets left by
the *previous* battery's accepted connections make it report "occupied" for ~60 s after any run —
while the probe's own server uses `allow_reuse_address=True`. The flock is the real serializer; the
`port_free` gate is not, and it will fire for every seat that replays the battery inside the TIME-WAIT
window. Attempt 3, run at `2026-11-03T21:08:50-03:00` after `ss -H -tan '( sport = :8080 )'` showed 0
sockets, ran the battery and produced the receipt. `battery.txt` records the three attempts.

This is the only reason I did not use NginxBattery's receipt as a substitute: my own run succeeded, so
the cross-check is two independent live runs rather than one run read twice. NginxBattery's receipt
was still checked independently (`check-nginxbattery.txt`).

## Result 7 — the committed do-nothing control is not reproducible from committed bytes

`.ufo/waves/round-69/nginx-control.txt` (tracked at `b288e8e0`, sha256
`eabd527e9a15f65d41549be54024f7d9c9d1c230b3d1d81fd518917af7d0d950`) shows a
`--render-table` transcript containing three `FROZEN-SHA` lines. Neither the freeze-commit probe nor
the working probe contains the string `FROZEN-SHA` (`grep -n 'FROZEN-SHA'` → rc 1 in both; repo-wide
the only occurrences are those three lines in the control file itself), and `render_table()` prints
only the case rows, `FROZEN-VECTOR` and `LEGS`. Running the command today prints exactly those nine
lines and no `FROZEN-SHA`. The three hashes themselves are correct values of the three files
(`66b5128d…`, `ea28b006…`, `0088cfb0…` — verified with `sha256sum`), but no committed command emits
them. So the control's third block is a transcript the instrument cannot produce; the control's other
three blocks do reproduce (`git cat-file` rc 128, `grep -c 'executed 3 of 8'` → 0,
`--check-receipt` → `SETUP receipt-missing` rc 2).

Base-state facts re-derived: `git cat-file -e a518980e:corpus/evidence/round69/nginx/receipt.txt` →
`fatal: path … does not exist`, rc 128; `grep -c 'executed 2 of 8' SKILL.md` → 1;
`grep -c 'executed 3 of 8' SKILL.md` → 0;
`grep -cE '^\|[[:space:]]*S241[[:space:]]*\|' corpus/SOURCES.md` → 0.

## Result 8 — the claim's measuring command has no producer for its receipt path

The frozen measuring command names `--receipt corpus/evidence/round69/nginx/receipt.txt
--evidence-dir corpus/evidence/round69/nginx/sandbox`. That path does not exist and no wave item writes
it: `corpus/evidence/round69/` contains only `c2-receipts/` and `gates/`; the only spec occurrence of
`corpus/evidence/round69/nginx` is in `ClaimFalsify`'s base-absence check; `NginxBattery` was
instructed to write `.ufo/waves/round-69/w1/nginx/receipt.txt`. As written, the claim's own
`--check-receipt` command reports `SETUP receipt-missing` even after the battery has run.

## Findings a claim's attacker should use (ranked)

1. **Unsatisfiable predicate (claim-level, decisive).** Legs 2 and 4 have no `F` witness in the frozen
   table; `ok` requires `full_f == 8`. `PREDICATE R69-C1 pass` is unreachable for *any* run, and the
   frozen after-target ("receipt present with `PREDICATE R69-C1 pass`") cannot be met. Fixing this
   needs a dated amendment before any after-receipt is scored (claims doc allows exactly that), e.g. a
   sixth case that reds leg 2 and/or leg 4 (server down; wrong 404 body) — **not** an edit to the
   table by a seat.
2. **Writer/checker format mismatch (instrument-level, decisive).** `check_receipt` expects 5 VECTOR
   fields, `run_battery` writes 6; every genuine receipt yields 15 defects, so the frozen
   `--check-receipt` conjunct ("defect list nonempty" kill rule) fires on truth.
3. **Vacuous selftest red arm.** All five forged fixtures are refused by defect 2, not by their
   intended defect; `green_ok=0` on a genuine receipt; `dup_leg` unused.
4. **Spurious `SETUP port-8080-occupied`.** `port_free()` without `SO_REUSEADDR` refuses for the
   TIME-WAIT window after any battery; will block later seats replaying C1.
5. **`case_sha256` path-dependent** (embeds the work-root path in `run/server.json`); not comparable
   across seats, and `check_receipt` ignores `CASE` lines entirely.
6. **`check_receipt` cannot verify the GRADER bytes.** It compares the receipt's declared grader sha to
   the frozen constant `GRADER_SHA256` and never reads `GRADER_REL` from disk; only `run_battery` does.
   The predicate's "the receipt's … GRADER sha256 equal the committed bytes" is therefore not
   re-derivable by the checker (it held in both runs: on-disk sha `045cc716…`).
7. **Committed control transcript contains output the instrument cannot emit** (`FROZEN-SHA` lines);
   the control's render-table block is not reproducible from committed bytes.
8. **No producer for the claim's receipt path** `corpus/evidence/round69/nginx/receipt.txt`.

## What did pass (stated exactly)

- Five frozen cases → five frozen eight-leg vectors, deterministic across two independent live runs
  (my receipt and NginxBattery's), `mismatches=0 setup=0`.
- `PROBE` sha256 in both receipts equals the committed probe (`66b5128d…`); `GRADER` sha256 equals the
  committed grader (`045cc716…`) and `SHA256SUMS:111`; `run_battery` verified the on-disk grader
  before running.
- Grader leg order equals the file order of the eight `def test_*` functions
  (`installed, running, index, 404, syntax, settings, log_creation, log_format`) — the `LEGS` tuple and
  the `RUNNER` invocation order agree with the grader source.
- K5's leg 5 is `E:FileNotFoundError` in the raw sandbox capture
  (`TEST test_nginx_config_syntax E:FileNotFoundError 1ms [Errno 2] No such file or directory: 'nginx'`)
  and `run_case` maps any non-`P`/non-`F` outcome to `F`, so `E→F` is real, not assumed.

## Commands I did NOT run

- `plans/round69_c2_routed_defects.py` (C2 gate, its `--selftest`, and `c2-red-before.txt` replay) —
  out of seat scope.
- `plans/round63_gate_checks.py depth|trio` (E7 receipts), the census, and any `pytest` invocation on
  the grader outside the probe's bwrap runner.
- No git/jj write command of any kind (no commit/stage/stash/checkout/switch); only
  `git log/show/cat-file/status/ls-files`-class reads.
- No `pacman`/`uv`/`npx` install or upgrade; no tool changes were needed, so none were recorded.
- No message to `agent://all`, no spawn, no background service.
- No edit to the instrument, the claims doc, either receipt, or any tracked lane file.

## Artifacts

`.ufo/waves/round-69/w1/ReceiptReverify/` — `battery.txt` (three attempts + rc),
`receipt2.txt` (my live receipt), `check.txt`, `selftest.txt`, `check-nginxbattery.txt`,
`selftest-nginxbattery.txt`, `parser-probe.txt` (synthetic isolation A–D + unsatisfiability counts).
Scratch `/fast/scratch/hyaku/kengaku-r69/ReceiptReverify` removed after copying.
