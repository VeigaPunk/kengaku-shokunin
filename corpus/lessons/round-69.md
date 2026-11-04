# Round 69 — kengaku (hyaku run 15)

Round 69 declared two claims (`plans/round-69-claims.md`, frozen at `b288e8e0`; Amendment A1
dated after the wave): **R69-C1** coverage — replay the `nginx-request-logging` TB2 grader offline
under a frozen five-case table — and **R69-C2** calibration — close the round-68 non-author
closure's seven routed defects with a re-deriving gate. R69-C1 is an **honest MISS** (the frozen
leg-coverage clause cannot be met by the frozen table, and the instrument's checker could not
parse its own receipt); R69-C2 is **admitted on its frozen sentence** (`DEFECTS n=7` → `n=0`,
`PREDICATE R69-C2 pass`, selftest `defects-in-fake=7 want=7 all-fail=True`, gate mutation
`killed=7 survived=0`), with the limitations below named rather than smoothed.

## Gate (SOURCES contract v1)

- **S241** — Terminal-Bench 2.0 `nginx-request-logging`, `tests/test_outputs.py` at pin
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`
  (`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py`),
  opened live 2026-11-03 by `curl` (HTTP 200, 5947 bytes, sha256
  `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` = `SHA256SUMS:111`, `cmp`
  byte-identical to the committed capture). Located quote (≤25 words), line 13:
  `result = subprocess.run(["which", "nginx"], capture_output=True, text=True)`.
  **Admit** (tier A, code): the eight legs in file order, the two exact body literals (`:39`,
  `:52`), the config regexes (`:67-121`) and the log-leg regexes (`:123-178`) are the surfaces the
  replay prices. The row's `used-by` resolves to
  `corpus/knowledge/tb2-nginx-request-logging-offline.md` (this round's new entry; trio gate green).
- **No rejects this round** — no assimilation set was opened (`Assimilation: none`; the round-54
  id-drift L0 question stays open and the round-68 precedent is followed).

## Findings the round landed

- **R69-C1 (MISS).** Five frozen cases, 40/40 legs matched their predicted vectors
  (`mismatches=0`) in three independent runs, but `LEG-COVERAGE legs=8 seen_p=8 seen_f=6`:
  `test_nginx_running` and `test_custom_404_page` have no red witness in the frozen table, so the
  predicate's "every leg P once and F once" clause fires by construction. The SCORECARD records
  the MISS; the class row stays `executed 2 of 8`.
- **What the replay teaches anyway** (landed in `corpus/knowledge/tb2-nginx-request-logging-offline.md`):
  legs 2–4 are HTTP-observable and pass with no nginx present (K5); leg 5 is a shim (`nginx -t`
  exit 0 regardless of config); leg 6 is text presence in two files; leg 8's four regexes search
  the whole log content, not per line, so one stale line satisfies all four; `case_sha256`
  digests the server-written log and is therefore not a staged-state identity.
- **R69-C2 (admitted).** The round-68 closure's seven routed defects closed as E1–E7; the gate's
  pre-correction fixture yields `DEFECTS n=7`, the landing tip `n=0`; single-check deletion kills
  all seven mutants on two independent fixtures (`GateMutate.md`:
  `MUTANTS total=7 killed=7 survived=0`).
- **C2's named limitation (ClaimFalsify, routed to round 70).** E1/E2/E4/E5/E6 verify text facts
  (the correction *is* prose in the lane's own correction-gate pattern), E3's input set is not
  tied to the six paths the round-68 receipt names (a one-input erratum would pass), and E7's
  byte-diff arm was exercised only after the fact. The predicate sentence is met on the committed
  bytes; the successor gate should pin E3's input set and run each E1 entry command.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **asserted-coverage (a frozen table's anti-vacuity claim stated in prose, not computed)** | `plans/round-69-claims.md` R69-C1 says "Each of the eight legs has one red witness and four green witnesses by construction"; the battery's `LEG-COVERAGE legs=8 seen_p=8 seen_f=6` shows legs 2 and 4 have none (`.ufo/waves/round-69/w1/nginx/receipt.txt`; `LegPricing.md` LEG 2/LEG 4) | the probe's own `LEG-COVERAGE` clause at the battery — the first execution of the frozen table (`NginxBattery.md` §Verdict) | the clause stays (a miss is reported, not re-scored). The freeze step now computes a table's per-leg P/F counts from the frozen vectors before freezing; round 70's table carries the two missing cases — a service-down case (needs a `server: False` stage field) and a wrong-404-body case (`notfound` already exists; no case mutates it). QUALITY Q51 records the rule. |
| **self-unreadable receipt (a checker that cannot parse its own writer's output)** | `check_receipt` required exactly 5 whitespace tokens for `VECTOR`; `run_battery` writes 6 (`VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True`) → every genuine receipt was refused (`NginxBattery.md` run 2; `ReceiptReview.md` M-A; `ReceiptReverify.md` §Verdict) | the `NginxBattery` and `ReceiptReverify` seats, on the first two battery receipts | parser repaired (accept the 6-token form, verify the `expected` field equals the observed vector) and a re-run receipt committed (`corpus/evidence/round69/nginx/receipt-v2.txt`); the frozen table, vectors, kill rule and target are untouched and the MISS stands (Amendment A1). |
| **spurious-selftest (five red fixtures refused for the wrong reason, so `red_refused=5/5` proved nothing)** | all five red fixtures were refused through the parser defect; no clause was actually exercised, and no acceptance fixture existed (`ReceiptReview.md` §2; `NginxBattery.md` run 3 prints `red_refused=5/5` while M-A holds) | `ReceiptReverify.md` §Verdict and the L1's re-run after the parser repair | `--selftest` gains an acceptance arm on a synthetic full-coverage table (v2: `red_refused=5/5 ... accept_ok=1 ok=True`, `corpus/evidence/round69/nginx/selftest-v2.txt`); the rule: a selftest that refuses everything is not evidence until it also accepts the shape it is meant to judge. |
| **port-gate false refusal (a free port refused while a TIME_WAIT socket lingers)** | `ReceiptReverify`'s first two battery attempts printed `SETUP port-8080-occupied` while `ss` showed no listener and `fuser` nothing; a direct `bind()` probe reproduces the refusal without `SO_REUSEADDR` (`ReceiptReverify.md` result 6) | the `ReceiptReverify` seat, on the second battery of the same wave | `port_free` sets `SO_REUSEADDR` (v2); the re-run battery succeeds immediately after the previous one — the failing condition. |
| **path-dependent case digest (a staged-state digest that includes server-written bytes)** | `case_sha256` digests the whole case tree, including `var/log/nginx/benchmark-access.log`; two batteries of the identical table give different digests for K1/K2/K4/K5, and the same digest only for K3 (no log) — `ReceiptReverify.md` §Result, run-1 vs run-2 CASE lines | the `ReceiptReverify` seat, comparing its receipt with the battery's | named, not patched: the checker records `case_sha256` but never re-derives it, so no verdict depends on it. Round 70's re-freeze digests only the staged inputs (config bytes, shim, `server.json`). |
| **misattributed dirt (a seat read the L1's in-flight integration as a sibling lane's landing)** | `CorrectionDraft.md` and `CensusAudit.md` both describe `M SKILL.md`, `M corpus/QUALITY.md`, … as "sibling landings"; the four modified files are the L1's own C2 corrections, landed in the working tree while the wave ran (`git diff --stat` → the four C2 targets) | the L1's re-read of its own diff and of the wave reports | the round report names the four files as the L1's integration, and the wave context states the L1 may land corrections mid-wave; no file was misrooted. |

## Round-69 re-derivation commands

- C1: `python3 plans/round69_c1_nginx_probe.py --check-receipt corpus/evidence/round69/nginx/receipt-v2.txt`
  → `CHECK ok cases=5 legs=8 seen_p=8 seen_f=6`, two `DEFECT leg-coverage`, `PREDICATE R69-C1 fail`, rc 1
  (`corpus/evidence/round69/nginx/check-v2.txt`); the v1 receipt's check adds the `probe-sha` defect
  (`corpus/evidence/round69/nginx/check-v1.txt`).
- C2: `python3 plans/round69_c2_routed_defects.py` → `E1..E7 ok`, `DEFECTS n=0`,
  `PREDICATE R69-C2 pass`, rc 0; `--selftest --work <scratch>` → `defects-in-fake=7 want=7
  all-fail=True`; the E7 byte-diff arm at
  `corpus/evidence/round69/c2-receipts/e7-byte-arm.txt` (`differ` → `n=1`, restored → `n=0`).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
  → exit 0 at round start (232 rows) and at close (233 rows, S241; 24 pre-existing W04 warnings).
