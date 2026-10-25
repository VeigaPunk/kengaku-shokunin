# R35MutLedgerRobust — mutation test of `plans/defect_ledger.py` robustness

Seat: R35MutLedgerRobust (mutation-tester, leaf). Date: 2026-10-25, kengaku round 35 wave 1.
No tools installed; stock `python3` (Python 3.14) only.

## Fixture and provenance

- Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; freeze commit `11d64530179b78e33ba6074fc77d63d36ee7ac31` (clone HEAD; `git rev-parse --show-toplevel` verified equal to the clone root before any write).
- Checker under test: `plans/defect_ledger.py`, sha256 `4e386677b48fd66e1a19a7459ab5e5359139e282e0968afa2cfd2395768d763d` — identical in lane working tree and fixture (`git ls-tree HEAD` blob `28ec7d249855b8ecd1ea5d1e984694738d512f7f`; lane `git status --porcelain` for the file: empty). The lane's `corpus/defects.jsonl` has an unrelated uncommitted `recurrence_of` string edit by another seat; I did not use the moving working tree — all mutations ran against committed bytes in a disposable clone.
- Every `git` call named `-C "$D/lane"`; no commit/add/stash/checkout/reset in the lane; the lane's index was never touched. Fixture disposed: `rm -rf /tmp/k35-HLMd`.

## Baselines (why two)

- **S0 — freeze bytes.** Committed ledger (all 5 rows `open`) at the freeze tip. Run `python3 plans/defect_ledger.py --lane .`:
  ```
  R34-D1 status=open observed=pass agree=NO untracked=0
  R34-D2 status=open observed=fail agree=yes committed_mirror_paths=109413
  R34-D3 status=open observed=fail agree=yes listed=4 evaluator_listed=False bad=0
  R34-D4 status=open observed=fail agree=yes correction_lines=0
  R34-D5 status=open observed=fail agree=yes erratum_lines=0 r35_mistake_row=False
  rows=5 closed=0 observed_pass=1 mismatches=1
  PREDICATE C2 fail
  ```
  exit=1, no crash. A red baseline makes "failed closed" verdicts near-vacuous (a checker that always exits 1 also scores 7/7), so I built a discriminating substrate.
- **S1 — GREEN-4 (canonical substrate for the matrix).** Working-tree-only repairs in the disposable fixture (no commits): D3 manifest gained the two evaluator digest lines; D4 correction line appended to `SCORECARD.md`; D5 erratum appended to `corpus/lessons/round-34.md` + `corpus/lessons/round-35.md` `## Mistakes` S091 row; ledger rows D1/D3/D4/D5 flipped `closed`. D2 stays truthfully `open`: its check reads committed mirror paths at `refs/heads/master` (109413 committed at freeze) and is unfixable without a commit, which the fixture rule forbids. Pristine S1 run:
  ```
  R34-D1 status=closed observed=pass agree=yes untracked=0
  R34-D2 status=open observed=fail agree=yes committed_mirror_paths=109413
  R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
  R34-D4 status=closed observed=pass agree=yes correction_lines=1
  R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
  rows=5 closed=4 observed_pass=4 mismatches=0
  PREDICATE C2 fail
  ```
  exit=1. Every row agrees; the only red is D2's committed-tree truth. A mutant reaching `PREDICATE C2 pass` / exit 0 here is a real pass-finding.

S1 pristine hash manifest (sha256): `corpus/defects.jsonl` `fd35554fd2ed79f8dc7feb16eba2504a358a4698566b308a4b3d71f4d18cf4cb`, `corpus/lessons/round-34.md` `1de74181…`, `corpus/lessons/round-35.md` `797c68a9…`, `SCORECARD.md` `019debcb…`, `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS` `fb46c813…`.

## Mutation matrix (canonical, on S1; each mutant: run → restore → sha256 verify)

| # | Mutant (all are `corpus/defects.jsonl` edits) | Result (verbatim tail) | EXIT | Verdict |
|---|---|---|---|---|
| M1 | unknown check name (`R34-D3` check → `r34_d9`) | `R34-D3 status=closed observed=fail agree=NO unknown check 'r34_d9'` … `rows=5 closed=4 observed_pass=3 mismatches=1` `PREDICATE C2 fail` | 1 | **fail closed** |
| M2 | malformed JSON line (`{not-json` prepended) | `json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)`; traceback at `defect_ledger.py:119` in `main` | 1 | **fail closed** (unhandled crash, nonzero exit) |
| M3 | `corpus/defects.jsonl` missing | `FileNotFoundError: [Errno 2] No such file or directory: '…/corpus/defects.jsonl'`; traceback at `defect_ledger.py:119` | 1 | **fail closed** (unhandled crash, nonzero exit) |
| M4 | duplicate row id (exact copy of `R34-D1` line appended) | duplicate row printed twice, `rows=6 closed=5 observed_pass=5 mismatches=0` `PREDICATE C2 fail` | 1 | **fail closed** — but no id-uniqueness check; rejection is pure count arithmetic (`closed=5 < rows=6`), zero mismatches raised |
| M5 | status typo (`R34-D3` status → `Closed`) | `R34-D3 status=Closed observed=pass agree=NO …` `rows=5 closed=3 observed_pass=4 mismatches=1` `PREDICATE C2 fail` | 1 | **fail closed** |
| M6 | plausible sixth row added (`R35-D6`, closed, check `r34_d1`) | sixth row `agree=yes`, `rows=6 closed=5 observed_pass=5 mismatches=0` `PREDICATE C2 fail` | 1 | **fail closed** on S1 — but only via D2's red (closed=5<6); the script itself has no row-count pin (see F1) |
| M7 | empty file (0 bytes) | `rows=0 closed=0 observed_pass=0 mismatches=0` `PREDICATE C2 fail`, no crash | 1 | **fail closed** (`good = bool(rows) and …` guard, `defect_ledger.py:138`) |

No mutant produced exit 0 or a crash-with-exit-0 on the canonical substrate. **7/7 fail closed.**

Restoration evidence: after every mutant, `corpus/defects.jsonl` was rewritten from backup and hashed — all seven printed `[restore Mx] sha256=fd35554f… match=True`; post-matrix pristine re-run reproduced the S1 output above with `EXIT=1`, final file hash `fd35554f…` (equal to pristine).

## Supplemental probes (labeled; not part of the 7)

- **P1 — unknown check on an OPEN row (S0 ledger bytes, S1-repaired tree).** `R34-D1` check → `r34_d9`, status stays `open`:
  ```
  R34-D1 status=open observed=fail agree=yes unknown check 'r34_d9'
  …
  rows=5 closed=0 observed_pass=3 mismatches=3
  PREDICATE C2 fail   EXIT=1
  ```
  Row-level miscalibration: for an open row, an unknown check counts as **agreement** (`agree = … or (st == "open" and not ok)`, `defect_ledger.py:132`; `fn is None → ok=False`, `:122-124`) — the broken ledger reference is masked as an agreeing observation. Predicate still fails closed (exit 1). Side observation: the 3 mismatches are the S1 repairs against S0's `open` rows — the checker correctly flags stale self-assessment in the open-row direction too.
- **P1b — the rows=5 pin is textual, not coded (citation, no run).** The frozen C2 predicate sentence requires the literal output `rows=5 closed=5 observed_pass=5 mismatches=0` + `PREDICATE C2 pass` (`plans/round-35-claims.md`, C2 section), and the checker's own docstring states the code's predicate is ledger-generic with the count pinned externally (`defect_ledger.py:13`: "…round 35 additionally requires the row count to read 5."). Neither string is enforced anywhere in `main()` (grep for `json.loads(l)|fn = CHECKS.get|unknown check|is_closed = |agree = |good = bool|PREDICATE C2` hits only lines 119/122/124/131/132/138/139 — no row-count literal).

- **P2 — drifted ledger passes the script (compound probe: all 5 rows retargeted to check `r34_d1` and flipped `closed`, sixth row added).** Run via subprocess on the S1 fixture, ledger restored immediately after:
  ```
  R34-D1 status=closed observed=pass agree=yes untracked=0
  R34-D2 status=closed observed=pass agree=yes untracked=0
  R34-D3 status=closed observed=pass agree=yes untracked=0
  R34-D4 status=closed observed=pass agree=yes untracked=0
  R34-D5 status=closed observed=pass agree=yes untracked=0
  R35-D6 status=closed observed=pass agree=yes untracked=0
  rows=6 closed=6 observed_pass=6 mismatches=0
  PREDICATE C2 pass
  EXIT=0
  ```
  (All six rows printed `agree=yes`; R35-D6 is the added row.) Restoration: `restored: fd35554fd2ed79f8dc7feb16eba2504a358a4698566b308a4b3d71f4d18cf4cb` (= pristine).

## Findings for the L1

- **F1 (pass-finding at script level — the one real coverage gap).** The script's predicate (`defect_ledger.py:138`) is content-blind to *which* check each row names and to the row count: a drifted ledger (all rows retargeted to a passing check + one added row) yields `rows=6 closed=6 observed_pass=6 mismatches=0`, `PREDICATE C2 pass`, **exit 0** (demonstrated in the fixture with a synthetic 6×`r34_d1` ledger; fully restored after). An isolated sixth row fails closed only while any real row is red; on a fully green landed ledger (D2 repaired at a future tip), a sixth plausible closed+passing row — or any check-name drift — would pass the script. The `rows=5` pin and the D1–D5↔check binding live only in the frozen claims sentence (`plans/round-35-claims.md` C2 predicate) and the docstring (`defect_ledger.py:8-10`), not in code. The frozen predicate's literal output match (`rows=5 …`) does catch this at claim level, so C2's admission path is safe; the residual risk is any future consumer running the script without the claims sentence.
- **F2 (nuance, no false pass).** Unknown check names never crash and never pass; on a `closed` row they mismatch (M1), on an `open` row they agree (P1). A stricter checker would treat `fn is None` as a ledger-integrity defect in both directions.
- **F3 (nuance).** M2/M3 are unhandled tracebacks (crash, exit 1). Robust posture (fail closed), though a clean `ledger unreadable` diagnostic would improve operability; M7 is handled cleanly by the `bool(rows)` guard.
- **F4 (nuance).** Duplicate ids are silently accepted (M4): rejection is incidental count arithmetic; ids are never compared.

## Verdict accounting

Total mutants 7 (M1–M7, the tasking list). Fail closed: M1, M2, M3, M4, M5, M6, M7 — all exit 1, no false `PREDICATE C2 pass`, no crash exiting 0. Pass-findings among the 7: none. The F1 drift pass is a supplemental compound probe, reported separately above.

VERDICT: ledger-robust-7/7
