# ProbeReview — surgical correctness review of the frozen R67-C1 probe

Seat: ProbeReview (kengaku r67 w1, round-67). Read-only review; no edits; no grader run; no installs.
Frozen artifacts reviewed at HEAD `dcc39ea3` (`git -C kengaku-shokunin rev-parse --short=8 HEAD` → `dcc39ea3`; `git log --oneline -1 -- plans/round-67-claims.md` → `dcc39ea3 round-67: freeze ...`).

- Probe: `plans/round67_c1_pipeline_probe.py` (357 lines, sha256 `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836` — equals the receipt's `PROBE` line).
- Grader: `corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py` sha `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f` — equals `GRADER_SHA256` (:63) and the receipt's `GRADER` line.
- Receipt of record: `corpus/evidence/round67/pipe/receipt.txt` (six VECTOR lines, all `frozen=match`, vectors PPPP/FFFF/PPFF/PFPP/PPPF/PPFF ≡ FROZEN_TABLE :71-78 ≡ claims table).
- Copies preserved in this seat dir: `receipt.observed.txt`, `receipt.junit/`, `mutants/*.receipt.txt`.

## Required runs (item 5)

| Command | cwd | Result |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile plans/round67_c1_pipeline_probe.py` | lane | **Deviation, see P1.** Run on a byte-identical scratch copy (sha256 equal, observed) → rc 0, silent. Committed bytes also compile via `py_compile.compile(<lane path>, cfile=<scratch>/committed.pyc, doraise=True)` → "committed-bytes compile ok". |
| `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt; echo rc=$?` | lane | `CHECK ok cases=6` / `PREDICATE R67-C1 pass` / **rc=0**. Reads committed bytes only; no listener (check_receipt touches no bwrap/pytest/socket), so no flock wrap needed. |

**The R67-C1 predicate passes on the committed bytes.**

## Findings

### Must-fix (routed to lane; frozen file — report only, not edited)

- **M1 — `check_receipt` accepts a receipt that is missing a VECTOR line.** The claims sentence (:23) requires "six `VECTOR` lines whose outcome vectors equal the frozen table"; the code validates only the VECTOR lines that are present (:276-305) and the missing-check (:306-308) tests `seen`, which is populated by CASE lines only. Evidence: mutant `v1_missing_vector` (drop `VECTOR q6-unscaled-loss`) → rc=0, `CHECK ok cases=6`, `PREDICATE R67-C1 pass`. A tamperer can delete the FFFF control's vector and still get a pass. Fix: track VECTOR presence per case in a second set and defect when any case in `CASES` lacks exactly one CASE and one VECTOR line.
- **M2 — junit/case_sha binding is order-sensitive and silently skipped.** The junit-sha, junit-derived-vector and case_sha checks live inside `if case in seen:` (:287) during a single pass; a VECTOR line placed before its CASE line silently skips all binding checks (no else-defect). Evidence: mutant `v2_vector_before_case` (`VECTOR q1-ref` moved before `CASE q1-ref`) → rc=0, pass, no binding performed. The predicate clause "every `CASE` `junit_sha256` equals the bytes of `receipt.junit/<case>.xml`" is unenforced for that line. Fix: two-pass parse (collect CASE lines first) or emit `defect: VECTOR before CASE for {case}`.

M1+M2 do not affect the record receipt (it passes both the real run and v0); they weaken the counter against a tampered receipt — the same class of defect C2 fixes for R65.

### Should-fix

- **S1 — duplicate CASE line silently overwritten.** `seen[case] = ...` (:275); last occurrence wins, first ignored, no defect. Evidence: `v3_duplicate_case_at_end` (second `CASE q1-ref` with a different `case_sha256`) → rc=0 pass. Fix: `if case in seen: findings.append(f"defect: duplicate CASE line for {case}")`.
- **S2 — extra/unknown CASE line accepted.** The unknown-case defect lives only in the VECTOR branch (:283-284); a stray `CASE q7-fake ...` line is recorded in `seen` and reported as `CHECK ok cases=7` with rc=0 (mutant `v4_extra_unknown_case`). Fix: require the CASE-line set to equal `CASES` exactly.
- **S3 — unguarded `junit_outcomes` in `run_case` can exit 1 by traceback.** :190 calls it outside any try; `key_of` raises ValueError on an unexpected testcase name (:98-105) and `ET.parse` raises ParseError — contradicting the docstring's own rule "Setup failures (… missing junit, timeout) are SETUP, exit 2 … never a verdict" (:33-34). `check_receipt` guards the identical call (:295-298) — asymmetric. Today the grader is sha-pinned so names are fixed, but the failure mode is a traceback, not exit 2. Fix: wrap in try/except → `{"case": case, "error": f"junit unreadable: {e}"}`.
- **S4 — the receipt of record and its junit dir are untracked in git.** `git status --porcelain -- plans/ corpus/evidence/round67/` at HEAD `dcc39ea3` → only `?? corpus/evidence/round67/pipe/receipt.junit/` and `?? corpus/evidence/round67/pipe/receipt.txt`. The claims call these "committed"; on any fresh checkout the frozen predicate command fails on a missing receipt (kill-rule-b shape). Lane action: track both paths. (No git mutation performed by this seat.)

### Nits

- **N1** — GRADER line checked by substring `in`, not fullmatch (:263): `v6_grader_extra_field` (extra trailing field) → rc=0. Fix: fullmatch like the PROBE line (:254).
- **N2** — `fcntl.flock` (:206) is blocking with no timeout; a stuck holder hangs the probe indefinitely without reaching could-not-evaluate. (Contract makes holders short-lived; low risk.)
- **N3** — `run()` evaluates all six cases before inspecting errors (:209 vs :210-211); an early timeout still burns up to 6×900 s while holding the port lock. Fix: short-circuit on first error.
- **N4** — a VECTOR line with `frozen=mismatch` whose vec equals the frozen table passes (:277 captures the label; only :285-286 compares vec) — contradictory label accepted. `run()` cannot emit it today; a tamper could.
- **N5** — `probe_sha()` (:258) anchors to the executing file's bytes; identical to the committed probe only when run per the predicate command (verified equal here). Self-referential by design; acceptable while the lane command pins the path.
- **N6** — `--run --receipt <record path>` would rmtree/rewrite the committed `receipt.junit/` and receipt (:213-215, :236). A refuse-if-`receipt == RECORD_RECEIPT` guard would be cheap; frozen usage unaffected.

## Verified clean (positive results, with lines)

1. **Predicate/label/code agreement (item 2).** FROZEN_TABLE :71-78 ≡ claims table ≡ receipt VECTOR lines (order `exists/no_hooks/ws1/ws2` per KEYS :70). Command, exit codes (0 pass :314 / 1 fail :314 / 2 could-not-evaluate :135) and the printed labels `PREDICATE R67-C1 pass|fail` (:313) / `PREDICATE R67-C1 could-not-evaluate` (:134) match the claims sentence and kill rules. Remaining mismatches are exactly M1 and M2 (listed above); no others found.
2. **bwrap argv (item 3).** :152-177 has `--die-with-parent --unshare-net --unshare-pid`; ro-binds `/usr` (:154), `/etc` (:160), venv at its identical path (:164), case→`/app` (:165), grader→`/tests/test_outputs.py` (:166); `--proc /proc` :161, `--dev /dev` :162, `--tmpfs /tmp` :163; `--clearenv` :169 + PATH/HOME=/tmp/PYTHONDONTWRITEBYTECODE/PYTHONNOUSERSITE/HF_HUB_OFFLINE/TRANSFORMERS_OFFLINE (:170-175). Nothing writes under host /tmp: sandbox /tmp is a private tmpfs (HOME=/tmp lands there and dies with the namespace); the only writable host path is `/ctl` → `work/ctl/<case>` under `--work` scratch; `-p no:cacheprovider` prevents `.pytest_cache` writes into the ro-bound /app and /tests.
3. **flock / port-busy ordering (item 3).** Lock opened :205, `flock LOCK_EX` :206, `port_busy()` :207 **inside** the lock, and all six `run_case` calls :209 inside it — two probes serialize and the second sees a free port. The probe self-locks `~/.local/share/kengaku-r67/port-12355.lock`, the same path the contract has seats wrap for their own grader runs; consistent.
4. **Timeout handling (item 3).** `timeout=900` :180 → `except TimeoutExpired` → `{"error": "timeout"}` :181-182 → `setup_error` :210-211 → prints `SETUP …` + `PREDICATE R67-C1 could-not-evaluate`, returns 2, and returns **before** the receipt/junit-dir mutation (:213-215) — never a verdict, kill rule (c) honored.
5. **check_receipt re-derivation (item 4).** Re-parses `receipt.junit/<case>.xml` (`jdir` :249 = `<receipt-stem>.junit`), re-derives per-leg P/F (:295-303) and compares with the VECTOR line; re-hashes the junit (:293-294) and the committed case file or `none` (:304-305); re-checks PROBE sha/version (:250-261) and committed grader bytes (:265-266) — all from committed bytes, matching the predicate clauses.
6. **Named findings, never a traceback (item 4).** Malformed CASE/VECTOR lines → `CHECK defect: malformed …` (:272-273, :278-279); missing CASE+VECTOR → `defect: missing CASE/VECTOR …` (:306-308). Observed: `v5_missing_case_and_vector` rc=1 fail; `v7_malformed_case` rc=1 with `CHECK defect: malformed CASE line: CASE q1-ref case_sha256=not-a-sha junit_sha256=zz rc=x`. (The traceback risk is S3, in `run_case` only.)

## Process notes

- **P1 — seat-spec step 5 as written would write into the frozen lane.** `python3 -m py_compile <file>` writes `__pycache__/<file>.pyc` next to the source **regardless of `PYTHONDONTWRITEBYTECODE=1`** (observed: pyc appeared beside the scratch copy with the env var set). Run literally in the lane it would create `plans/__pycache__/`. I compiled the byte-identical scratch copy (sha256 equal, observed) and the true lane bytes via `py_compile.compile(..., cfile=<scratch>)`; zero writes in L. Route this step through a scratch `cfile` in future seat specs.
- Tooling: nothing installed (tooling-only rule; nothing named by this item).
- Mutant evidence receipts preserved at `mutants/<name>.receipt.txt` in this seat dir; scratch `/fast/scratch/hyaku/kengaku-r67/ProbeReview` removed before yield.
