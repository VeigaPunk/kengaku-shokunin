# NginxBattery — R69-C1 battery receipt of record (round 69, wave w1)

**Verdict: R69-C1 fails as frozen — rc=1, `PREDICATE R69-C1 fail`.** All five frozen cases do
yield their frozen eight-leg vectors, and both bound sha256 values equal the committed bytes;
the predicate is nevertheless unreachable for two independent, pre-data reasons:

1. **Instrument defect (decisive):** `--check-receipt` cannot parse the receipt its own writer
   produces. The writer emits a 6-token `VECTOR` line, the parser requires exactly 5 tokens, so
   every vector line is rejected, `case-set got=[]`, and all eight legs are counted at 0/0.
   No run of the frozen instrument can print `PREDICATE R69-C1 pass`.
2. **Frozen-table defect (decisive):** the five frozen cases red only six of the eight legs.
   `test_nginx_running` and `test_custom_404_page` have no red witness anywhere in the table
   (`F=0` for both, `P=5` each), so `seen_f=6 < 8` and the kill rule's "any leg with no `P` or no
   `F` witness" fires by construction.

Per the kill rule, this is reported, not re-scored. I did not edit the receipt, the instrument,
the case table, or any predicate.

Seat: `NginxBattery`, leaf. One labrat was **not** spawned (no falsifiable hypothesis needed one).

## 1. Exact argv run

| # | argv (cwd = `/home/vgpnk/Projects/shokunin/kengaku-shokunin`) | rc |
|---|---|---|
| 0 | `mkdir -p /fast/scratch/hyaku/kengaku-r69/NginxBattery/{tmp,work}` | 0 |
| 0 | `ss -ltnp '( sport = :8080 )'` | 0 |
| 1 | `python3 plans/round69_c1_nginx_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r69/NginxBattery/work --receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-69/w1/nginx/receipt.txt --evidence-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-69/w1/nginx/sandbox` | **1** |
| 2 | `python3 plans/round69_c1_nginx_probe.py --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-69/w1/nginx/receipt.txt` | **1** |
| 3 | `python3 plans/round69_c1_nginx_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r69/NginxBattery/selftest` | 0 |
| 4 | `python3 plans/round69_c1_nginx_probe.py --selftest --work .../selftest --green-receipt .../w1/nginx/receipt.txt` | **1** |
| 5 | `python3 plans/round69_c1_nginx_probe.py --render-table` | 0 |
| 6 | `sed -E 's/^(VECTOR [A-Z0-9]+ [PF]{8}) expected /\1 /' <receipt> > $S/receipt-5token.txt` then `--check-receipt $S/receipt-5token.txt` (scratch diagnostic, not the receipt) | **1** |

`TMPDIR=/fast/scratch/hyaku/kengaku-r69/NginxBattery/tmp` was exported explicitly for run 1;
`--work` names the scratch dir explicitly. Nothing under `/tmp` was used.

Runs 3–6 are additional read-only diagnostics (selftest fixtures, table render, and one scratch
reformat) beyond the two commands the seat item names; they write only under `S/`.

## 2. Port 8080 and lock

Before the battery:

```
State Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
```

(header only — **no listener**; port free.) After the battery, the identical header-only output:
no leaked listener. Receipt line:

```
PORT 8080 free-at-start=True lock=/home/vgpnk/.local/share/kengaku-r69/port-8080.lock
```

No `SETUP port-8080-occupied`, no lock timeout, no retry loop.

## 3. Receipt of record — bounds

Written to `.ufo/waves/round-69/w1/nginx/receipt.txt` (2647 bytes), evidence at
`.ufo/waves/round-69/w1/nginx/sandbox/K{1..5}-sandbox.txt`. Committed-byte check:

```
$ git show HEAD:plans/round69_c1_nginx_probe.py | sha256sum
66b5128dffbb1637b710f9a5d6fb8cacbe7639d89218dfa4b5010539070100ea  -
$ git show HEAD:corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py | sha256sum
045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0  -
$ sed -n '111p' corpus/evidence/round52/graders/SHA256SUMS
045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0  ./nginx-request-logging/tests/test_outputs.py
```

Receipt header equals both committed hashes; the grader hash equals `SHA256SUMS:111`. Instrument
pre-check: `sha256sum plans/round69_c1_nginx_probe.py` = `66b5128d…100ea`; the file was added whole
at the freeze commit `b288e8e0` (HEAD), 686 lines, and is unmodified since.

Lane base check: `git cat-file -e a518980e:corpus/evidence/round69/nginx/receipt.txt` →
`fatal: path ... does not exist in 'a518980e'`, rc=128 (target's "before" still holds).

## 4. Receipt content, verbatim

```
PROBE plans/round69_c1_nginx_probe.py sha256 66b5128dffbb1637b710f9a5d6fb8cacbe7639d89218dfa4b5010539070100ea
PROBE_VERSION 1
GRADER corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0 pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
PORT 8080 free-at-start=True lock=/home/vgpnk/.local/share/kengaku-r69/port-8080.lock
CASE K1 case_sha256=ed1cec21cd2b81e0da7da8d3aee750db1bcd506e375cf75c1fac8c1e444799bf server_pid=1256831 sandbox_rc=0
TEST K1 test_nginx_installed P
TEST K1 test_nginx_running P
TEST K1 test_index_page_content P
TEST K1 test_custom_404_page P
TEST K1 test_nginx_config_syntax P
TEST K1 test_nginx_config_settings P
TEST K1 test_log_file_creation P
TEST K1 test_log_file_format P
VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True
CASE K2 case_sha256=149d9bb23cb62121e70adba6f6f0bcf0dad02c0c884a9e324820c4517f7757ae server_pid=1262306 sandbox_rc=0
TEST K2 test_nginx_installed P
TEST K2 test_nginx_running P
TEST K2 test_index_page_content F
TEST K2 test_custom_404_page P
TEST K2 test_nginx_config_syntax P
TEST K2 test_nginx_config_settings P
TEST K2 test_log_file_creation P
TEST K2 test_log_file_format P
VECTOR K2 PPFPPPPP expected PPFPPPPP agree=True
CASE K3 case_sha256=ab907d25ffb0cb5b7392f8e11b8765cf193b34866cfd030379c7d62e3657445c server_pid=1266496 sandbox_rc=0
TEST K3 test_nginx_installed P
TEST K3 test_nginx_running P
TEST K3 test_index_page_content P
TEST K3 test_custom_404_page P
TEST K3 test_nginx_config_syntax P
TEST K3 test_nginx_config_settings P
TEST K3 test_log_file_creation F
TEST K3 test_log_file_format F
VECTOR K3 PPPPPPFF expected PPPPPPFF agree=True
CASE K4 case_sha256=68de95995d40cae616017018ba48b3c4e0ff7c564fecaf1b958b0fb6dc7eefaa server_pid=1270481 sandbox_rc=0
TEST K4 test_nginx_installed P
TEST K4 test_nginx_running P
TEST K4 test_index_page_content P
TEST K4 test_custom_404_page P
TEST K4 test_nginx_config_syntax P
TEST K4 test_nginx_config_settings F
TEST K4 test_log_file_creation P
TEST K4 test_log_file_format P
VECTOR K4 PPPPPFPP expected PPPPPFPP agree=True
CASE K5 case_sha256=0460d9d2269cb35bd39f55c1b12212b0f0e23600a1353efef9a6f2b2e027171b server_pid=1277524 sandbox_rc=0
TEST K5 test_nginx_installed F
TEST K5 test_nginx_running P
TEST K5 test_index_page_content P
TEST K5 test_custom_404_page P
TEST K5 test_nginx_config_syntax F
TEST K5 test_nginx_config_settings P
TEST K5 test_log_file_creation P
TEST K5 test_log_file_format P
VECTOR K5 FPPPFPPP expected FPPPFPPP agree=True
LEG-COVERAGE legs=8 seen_p=8 seen_f=6
SUMMARY cases=5 legs=40 mismatches=0 setup=0
PREDICATE R69-C1 fail
```

**Five server PIDs:** K1 `1256831`, K2 `1262306`, K3 `1266496`, K4 `1270481`, K5 `1277524`.
All five `sandbox_rc=0`; all five `case_sha256` distinct (each case staged a different tree).

**Cases whose observed vector differs from its frozen vector: none.** All five `agree=True`;
`mismatches=0`, `setup=0`. The failure is coverage + checker, not vector drift.

`stdout.txt` for the battery holds only `rc=1`: with `--receipt` set, `run_battery` writes the
body to the receipt and prints nothing (`sys.stdout.write(body)` is the no-receipt branch), so the
verdict-bearing lines live in the receipt above, not on stdout. That is instrument design, not a
lost capture.

## 5. Defect 1 — `--check-receipt` cannot parse its own writer's output (decisive)

`check.txt` verbatim (`W/NginxBattery/check.txt`):

```
CHECK ok cases=5 legs=8 seen_p=0 seen_f=0
DEFECT vector-line VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True
DEFECT vector-line VECTOR K2 PPFPPPPP expected PPFPPPPP agree=True
DEFECT vector-line VECTOR K3 PPPPPPFF expected PPPPPPFF agree=True
DEFECT vector-line VECTOR K4 PPPPPFPP expected PPPPPFPP agree=True
DEFECT vector-line VECTOR K5 FPPPFPPP expected FPPPFPPP agree=True
DEFECT case-set got=[] want=['K1', 'K2', 'K3', 'K4', 'K5']
DEFECT leg-coverage test_nginx_installed p=0 f=0
DEFECT leg-coverage test_nginx_running p=0 f=0
DEFECT leg-coverage test_index_page_content p=0 f=0
DEFECT leg-coverage test_custom_404_page p=0 f=0
DEFECT leg-coverage test_nginx_config_syntax p=0 f=0
DEFECT leg-coverage test_nginx_config_settings p=0 f=0
DEFECT leg-coverage test_log_file_creation p=0 f=0
DEFECT leg-coverage test_log_file_format p=0 f=0
DEFECT stored-predicate PREDICATE R69-C1 fail
CHECK stored-predicate=fail derived=fail
PREDICATE R69-C1 fail
```

Root cause, from the frozen source:

- writer, `plans/round69_c1_nginx_probe.py:460`:
  `lines.append(f"VECTOR {res['id']} {res['vector']} expected {res['expected']} " … "agree=…")`
  → `VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True` = **6** whitespace tokens.
- parser, `:513`: `if len(parts) != 5: defect("vector-line", ln); continue` → the 6-token line is
  rejected, `vectors` stays empty, and because the per-case loop does `if not got: continue`, every
  leg is counted 0/0 and `case-set got=[]`.
- selftest fixture writer, `:602`, emits the **same** 6-token shape:
  `out.append(f"VECTOR {cid} {vec} expected {case['expected']} agree=True")`.

So every selftest fixture is refused for the parse defect, not for the property it forges:

```
RED r1-all-p rc=1 refused=True
RED r2-probe-sha rc=1 refused=True
RED r3-leg-vector rc=1 refused=True
RED r4-missing-leg rc=1 refused=True
RED r5-grader-sha rc=1 refused=True
SELFTEST red_refused=5/5 green_ok=0 ok=True
rc=0
```

The red arm is vacuous — it cannot discriminate "refuses the forgery" from "refuses everything" —
and the green arm is opt-in (`:627`, only when `--green-receipt` is passed). With the real receipt
as the green arm:

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

The instrument therefore **cannot accept any receipt the frozen writer can emit**. This alone makes
the frozen predicate unreachable: `--check-receipt` can never print `PREDICATE R69-C1 pass`.

`--render-table` (rc=0) reproduces the frozen ids and vectors exactly:

```
case  setup                                                     vector
K1    all-green end state: service, bodies, config, shim, access log PPPPPPPP
K2    index body differs by one character (server otherwise green) PPFPPPPP
K3    service answers but writes no access log                   PPPPPPFF
K4    config lacks the limit_req_zone rate clause                PPPPPFPP
K5    no nginx binary on PATH (shim absent)                      FPPPFPPP
FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP
LEGS 8
```

(Byte-equality with the markdown case table, as the claims sentence demands, is impossible at
format level: the doc row is pipe-framed and K4's note carries backticks around `limit_req_zone`.
Field-wise the ids, notes-modulo-backticks and vectors match. Non-decisive.)

## 6. Defect 2 — the frozen table reds only 6 of 8 legs (decisive)

To separate Defect 2 from Defect 1, I reformatted **only** the `VECTOR` lines in a scratch copy
(`$S/receipt-5token.txt`, dropping the literal `expected` token) and re-ran the checker on it. This
is a diagnostic copy, not the receipt of record, and is not scored:

```
VECTOR K1 PPPPPPPP PPPPPPPP agree=True
VECTOR K2 PPFPPPPP PPFPPPPP agree=True
VECTOR K3 PPPPPPFF PPPPPPFF agree=True
VECTOR K4 PPPPPFPP PPPPPFPP agree=True
VECTOR K5 FPPPFPPP FPPPFPPP agree=True
CHECK ok cases=5 legs=8 seen_p=8 seen_f=6
DEFECT leg-coverage test_nginx_running p=5 f=0
DEFECT leg-coverage test_custom_404_page p=5 f=0
DEFECT stored-predicate PREDICATE R69-C1 fail
CHECK stored-predicate=fail derived=fail
PREDICATE R69-C1 fail
rc=1
```

With the parse defect neutralised, the only new reds are the two legs the table never prices.
Per-leg witness tally computed from the receipt's `TEST` lines (40 observations):

| # | leg | P | F | E |
|---|---|---|---|---|
| 1 | test_nginx_installed | 4 | 1 | 0 |
| 2 | **test_nginx_running** | **5** | **0** | 0 |
| 3 | test_index_page_content | 4 | 1 | 0 |
| 4 | **test_custom_404_page** | **5** | **0** | 0 |
| 5 | test_nginx_config_syntax | 4 | 0 | 1 |
| 6 | test_nginx_config_settings | 4 | 1 | 0 |
| 7 | test_log_file_creation | 4 | 1 | 0 |
| 8 | test_log_file_format | 4 | 1 | 0 |

The claims doc's sentence "Each of the eight legs has one red witness and four green witnesses by
construction" is false for legs 2 and 4: their only witness is green (5/5). Leg 5's single red is
an `E`, not an `F` — sandbox K5 shows `TEST test_nginx_config_syntax E:FileNotFoundError 1ms
[Errno 2] No such file or directory: 'nginx'` — so under a *literal* reading of the kill rule
("observed `F`") only legs 1, 3, 6, 7, 8 are red-witnessed (5/8); under the instrument's own E→F
scoring it is 6/8. Either way the coverage clause `seen_f == 8` cannot be met by these five cases.

Why it is unreachable, not bad luck: the probe always starts its lane server on 8080 and always
stages the 404 body, so `test_nginx_running` reds only on a failed/non-200 `GET /` and
`test_custom_404_page` only on a wrong `/nonexistent-page` body. K1–K5 vary the index body (K2,
reds leg 3 only), the log (K3, reds 7–8), the rate clause (K4, reds 6), and the nginx shim (K5,
reds 1 and 5); no case varies the 404 body or removes the service. Grader source confirms the
mechanics: `test_nginx_running` asserts `status_code == 200` on `http://localhost:8080`
(`test_outputs.py:17-30`), `test_custom_404_page` asserts status 404 **and** the exact body on
`/nonexistent-page` (`:46-56`), while `test_log_file_creation` merely re-requests `/`
(`:123-133`) — so the two un-priced legs are exactly the two the probe never perturbs.

## 7. Consequences for the claim and the landing

- Kill rule, clause 2 ("any leg with no `P` or no `F` witness") fires: legs 2 and 4. Honest miss.
- Kill rule, clause 3 (`--check-receipt` defect list nonempty) fires for instrument-internal
  reasons; the list is nonempty even for a perfect live run.
- The before→after target "receipt present with `PREDICATE R69-C1 pass`" is unreachable with the
  frozen bytes: the writer/checker mismatch is deterministic and the table cannot price two legs.
- The do-nothing control is unaffected: at base the receipt is absent, so `--check-receipt` prints
  `SETUP receipt-missing` and exits 2. That control still discriminates.
- The receipt of record now exists at `.ufo/waves/round-69/w1/nginx/receipt.txt` with
  `PREDICATE R69-C1 fail`. Because `run_case` refuses an existing receipt
  (`SETUP receipt-exists`), a later battery at this path needs the parent to remove or repoint it.
  I did not delete or rewrite it.
- I did not write `corpus/evidence/round69/nginx/receipt.txt` (the claims' measuring path): my seat
  item names only the W path. If the landing is meant to cite the corpus path, that copy is the
  parent's call, and it would carry `fail`.

## 8. Findings a C1 attacker should use

1. **Kill the "every leg is red-witnessed" clause or add a case.** With the frozen table the
   coverage half of the predicate is unsatisfiable. One additional case staging "no service bound
   on 8080" would price both gaps: from the grader source its vector derives to `PFFFPPFF`
   (legs 2/3/4 fail on `ConnectionError`, legs 7/8 see no log; legs 1/5/6 stay green with the shim
   and config present). **Derived by reading the grader; not run.** A narrower extra case —
   wrong `/nonexistent-page` body with everything else green — derives to `PPPFPPPP` and prices
   leg 4 alone. Either needs a dated amendment before any after-receipt is scored, or the clause
   must be restated as "six of eight legs".
2. **The writer/checker token mismatch is the cheaper kill.** Writer `:460` and selftest `:602`
   emit `VECTOR <id> <obs> expected <exp> agree=…`; parser `:513` requires exactly 5 tokens. Any
   receipt produced by this instrument fails the checker. Fix by dropping the literal `expected`
   word in both writers, or by accepting 6 tokens and comparing `parts[2]` against the case's
   `expected`; either changes the instrument, so it must be a dated amendment.
3. **The selftest's red arm is vacuous and its green arm is opt-in.** `SELFTEST red_refused=5/5
   green_ok=0 ok=True` (rc 0) is a false green: all five fixtures are refused by the same parse
   defect, and `ok` ignores the absence of a green witness. Any close that records "the C1 selftest
   tally" from `--selftest` alone records a number that cannot fail. Require `--green-receipt`
   in the selftest's own arm, or make `green_ok=0` force `ok=False`.
4. **The E-vs-F distinction.** Leg 5's red in K5 is an `E:FileNotFoundError`, scored F by the
   probe's own rule. A predicate phrased "observed `F`" is literally satisfied for only five legs;
   phrase it "scored F" if the instrument's E→F mapping is intended.
5. Replay fidelity itself is sound: the lane server answered on 8080, the grader's eight legs ran
   per case with `sandbox_rc=0`, K3's two log legs carried the grader's own messages ("Nginx access
   log file was not created", "Timestamp format missing in logs"), and K5's leg 1 carried "Nginx is
   not installed". The bottleneck is the frozen table and the frozen checker, not the staging.

## 9. Commands NOT run

- No editing of the receipt, the sandbox captures, the instrument, the claims doc, or any case
  table/vector/kill rule/target.
- No re-run of the battery after the first (a second would print `SETUP receipt-exists`).
- No `pacman` transaction of any kind (host-wide pause), no install/upgrade; nothing recorded
  because nothing was installed.
- No `git`/`jj` write command anywhere: no init/commit/add/stage/stash/checkout/switch. Only
  `rev-parse`, `log`, `cat-file`, `show`, `status`, `diff --stat`.
- No write to `corpus/evidence/round69/**`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
  `corpus/knowledge/**`, `corpus/lessons/**`, `.ufo/waves/round-69/nginx-control.txt`, or any
  fleet-repo path (`/home/vgpnk/Projects/shokunin`, its `.ufo/`, `.scratch/`, `MANIFEST.json`).
- No C2 work of any kind: `plans/round69_c2_routed_defects.py` was never executed, no defect was
  examined or corrected, no C2 receipt was read or written.
- No build, lint, test, or formatter run (editing wave in flight; parent owns post-integration
  gates).
- No labrat/spawn, no `agent://all`, no peer messages.
- No `ss` retry loop and no port lock probing beyond the two `ss` snapshots.

## 10. Risks / state left behind

- Lane tracked tree is dirty from **other** seats' in-flight C2 work (`M SKILL.md`,
  `M corpus/QUALITY.md`, `M corpus/knowledge/tb2-network-service-offline-grader.md`,
  `M corpus/lessons/round-68.md`). I touched none of them; my lane writes are untracked:
  `.ufo/waves/round-69/w1/nginx/{receipt.txt,sandbox/K{1..5}-sandbox.txt}` and
  `.ufo/waves/round-69/w1/NginxBattery/{stdout.txt,check.txt}` plus this report.
- Scratch `/fast/scratch/hyaku/kengaku-r69/NginxBattery` is removed before yield; the
  5-token diagnostic receipt lived only there and its output is transcribed in §6.
- C1 cannot reach `pass` at this freeze; any close that records C1 as covered must either amend
  the case table/predicate (dated, before scoring) or record the miss.
