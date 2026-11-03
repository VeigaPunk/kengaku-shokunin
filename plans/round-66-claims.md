# Round 66 — declared claims (frozen before the wave)

Lane: kengaku (novelty + calibration; LLM and model research and evaluation, run 15 hyaku).
Base: master tip recorded in the freeze landing's commit message and in the round-66 report (`git rev-parse master` at freeze).
Frozen artifacts: this file; `plans/round66_c1_tensor_probe.py` (its sha256 is the `PROBE` line of the control receipt and of the receipt of record); the five cases under `corpus/evidence/round66/tensor/cases/`; the pre-freeze control receipt `corpus/evidence/round66/tensor/prefreeze-run2.txt` (with its junit directory `corpus/evidence/round66/tensor/junit/`); the census start `corpus/evidence/round66/census-start.txt`; the source captures under `corpus/evidence/round66/sources/`; the red-before fixture `corpus/evidence/round66/red/fabricated-r65.txt` and its recorded checker output `corpus/evidence/round66/red/red-before-r65-checker.txt`; the wave spec and dispatch under `.ufo/waves/round-66/`.

Lane-root base for every path in this file and in the round report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

Lowest owned axis: **coverage 7** (L0-capped: `kengaku | round-25/33/51` still open; nothing assumed answered). It is worked by R66-C1. No stagnation waiver is invoked.

Claim count: 2 (distinct axes: coverage, operability). Each is causally separable: C1 is verifiable from its own receipt and the grader bytes; C2 is verifiable from its own fixtures and the committed R65 receipt, without C1 landing.

Frontier step (inside the 1–3 claim cap, not a claim): sources F1–F3 below, one sourced claim (C1 rests on S183, opened live this round), mistake mining, one `considerthese/` item if one qualifies, assimilation none.

---

## R66-C1 — coverage (L0-capped at 7); capability acquisition `offline-torch-tensor-parallel-grader-probe`

Predicate (one sentence, identical in the counter code, the receipt label and this text): the receipt at `corpus/evidence/round66/tensor/receipt.txt` carries five `VECTOR` lines whose outcome vectors equal the frozen table in `plans/round66_c1_tensor_probe.py` (K1 all 13 P; K2 `exists` F and all 12 layer tests F; K3 `exists` P and all 12 layer tests F; K4 `exists` P, column ws1 P, column ws2/ws4 F, row all P; K5 `exists` P, column all P, row ws1 P, row ws2/ws4 F), every `case_sha` and `junit_sha` equals the committed bytes, the grader line names sha `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`, and the receipt ends `PREDICATE R66-C1 pass`.

Counting command (after): `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt; echo $?` → `CHECK ok cases=5`, `PREDICATE R66-C1 pass`, exit 0. The receipt of record is produced by the post-freeze run `python3 plans/round66_c1_tensor_probe.py --run --work <scratch> --receipt corpus/evidence/round66/tensor/receipt.txt`.

Counting command (before): `grep -c torch-tensor-parallelism corpus/evidence/round52/graders/executed17.lst` → `0`; `grep -n 'CLASS process-environment' corpus/evidence/round62/class-survey.txt` → `CLASS process-environment count=3 members=install-windows-3.11,torch-pipeline-parallelism,torch-tensor-parallelism` with `executed 0` (class census receipt `corpus/evidence/round62/class-survey.txt`; the class's executed count is 0 in `EXECUTED-COVERAGE`).

Before-evidence (pre-freeze, committed): the host measurement — `uv` 0.13.0 at `~/.local/bin/uv`; torch `2.15.0+cpu` installed by `uv pip install --index-url https://download.pytorch.org/whl/cpu torch==2.15.0` into `~/.local/share/kengaku-r66/venv-torch` (channel: official PyTorch CPU index, reason: the process-environment class needs torch and this host had none); `gloo` available (`torch.distributed.is_gloo_available()` → True); transformers 5.22.1 and pytest 9.2.0 from PyPI into the same venv (not used by the frozen grader; transformers is imported only by the pipeline grader, not this one). Tooling authorization: operator 2026-10-19; RULES.md read first; pacman not used.

Do-nothing control: case K2 (`/app` empty) is run by the same probe in `corpus/evidence/round66/tensor/prefreeze-run2.txt` (its `VECTOR k2-none` line shows `exists=F` and all 12 layer tests `F`; its `CASE` rc is 1). The predicate needs K1 13/13 P and K4/K5 to discriminate, so K2 alone cannot meet it; `--check-receipt` on a receipt containing only K2's VECTOR line refuses (every CASE must be present). This is recorded, not assumed.

Case design (why each exists): K1 is a from-scratch reference build by the lane (no grader text copied; the grader's own assertions decide). K3 is the stub negative control (existence passes, behavior fails). K4 removes the column all-gather (fails only at world sizes 2 and 4, so a world-size-blind counter would miss it). K5 removes the row all-reduce (same shape, row side). Each mutant differs from K1 by exactly one method body (verified by a diff in the wave's FreezeReview seat).

Kill rules: (a) any case vector differs from the frozen table → the claim is not admitted; (b) K1 is not 13/13 P → SETUP-level failure of the reference, the claim is not evaluated; (c) grader sha drift, port 12355 busy, missing venv, or missing junit → could-not-evaluate (exit 2), never a verdict; (d) if K2 alone can be made to pass `--check-receipt` → the counter is wrong and is fixed before data (not done: refused by the CHECK shape above); (e) any seat or the L1 edits a frozen case or the frozen table after a scored run → the claim is re-judged on the frozen bytes only.

Pre-freeze honesty: the probe and its frozen table were written before the first run, and the first run's vectors matched the table. Before the freeze two harness fixes were made (the junit directory is receipt-local, so a re-run cannot overwrite committed junit bytes; the selftest copies junit beside its scratch receipt), and the control was re-run. No vector, predicate, kill rule or case file changed. The superseded first-run receipt was removed unscored. The control of record is `prefreeze-run2.txt`; its `PROBE` sha equals the committed probe's sha (`c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3`). The receipt of record for the claim is a post-freeze run.

Score: coverage held at 7 (L0 cap not lifted by a grader execution; the L0 question stays open). The capability `offline-torch-tensor-parallel-grader-probe` enters the capabilities table on C1's pass. Harm check: no owned axis may fall.

Sourced: C1 rests on `corpus/SOURCES.md` S183 (torch-tensor-parallelism grader, tier A, opened live 2026-11-03: sha256 `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`, capture `corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py`).

---

## R66-C2 — operability (held at ceiling 10, exercised): the round-65 receipt gate can refuse a fabricated receipt

Defect: the round-65 sentinel's fabricated receipt (`corpus/evidence/round66/red/fabricated-r65.txt`, file header "FABRICATED RECEPT … contains NO live-run data") is accepted by the round-65 checker (`corpus/evidence/round66/red/red-before-r65-checker.txt`: `CHECK ok cases=5`, `PREDICATE R65-C1 pass`, exit 0). This is `.ufo/waves/round-65/w1/ClaimFalsifier/atk/fabricated.txt` (SecurityScan M-1, must-fix, routed by `corpus/lessons/round-65-verifier-spotcheck.md` §6 item 8).

Before (counting command, base): `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt; echo $?` → `PREDICATE R65-C1 pass`, exit 0 (recorded in `red-before-r65-checker.txt`).

Predicate (one sentence, same text in the counter's code and this receipt label): the round-65 checker, invoked with `--strict`, exits 1 on the fabricated receipt with a named finding, exits 0 on the committed round-65 receipt `corpus/evidence/round65/sqlite-gcov-probe.txt`, and the default (non-strict) invocation over that receipt still prints `PREDICATE R65-C1 pass` (the default predicate is unchanged: a regression pin, not a re-judged claim).

Strict-mode requirements (frozen): every value the receipt names is checked against the bytes it names — `GRADER` sha equals `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` and the committed grader bytes; `AMALG` sha equals `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`; `TOOLCHAIN` values equal the values the receipt itself carries for gcc/gcov/bwrap/python and are well-formed; the receipt's `PROBE` sha equals the committed `plans/round65_c1_sqlite_probe.py` bytes at the strict run's revision; each `VECTOR` line equals the frozen table; each `NOBIND` line is present for G1–G5 with `delta=0`. A receipt missing any of these, or carrying a sha that does not match committed bytes, exits 1 with a finding naming the missing item.

Counting command (after): `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt --strict; echo $?` → exit 1 with a `CHECK defect:` finding; `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt --strict; echo $?` → exit 0; `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt; echo $?` → `PREDICATE R65-C1 pass`, exit 0.

Kill rules: (a) strict accepts the fabricated fixture → the claim is not admitted; (b) strict refuses the committed R65 receipt → the strict predicate is wrong for the receipt that exists; the claim is not admitted and the miss is reported, the predicate is not narrowed after the run; (c) the default invocation's output changes → the claim is not admitted.

Named limitation (stated before the data, not hidden): a receipt that copies every value from the committed bytes still passes strict. The gate refuses value-free and value-mismatched fabrication, not a hand-copied full receipt; the C1 probe's per-case junit binding is the stronger check and is a different gate.

Score: operability held at 10 (exercised). The R65 probe's SKILL/registry rows are not changed by this claim.

Sourced: the defect is a sentinel seat finding from the round-65 wave (`.ufo/waves/round-65/w1/SecurityScan.md`, M-1), and the R65 receipt bytes are committed evidence; no `S###` row is cited by C2.

---

## Frontier step (not a claim)

- **F1 — sources opened this round (live, 2026-11-03).** S183 (torch-tensor-parallelism grader): re-fetched live at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (curl HTTP 200; sha256 `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`; capture `corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py`). S233 (SQLite amalgamation zip): re-fetched live from `https://sqlite.org/2026/sqlite-amalgamation-3540100.zip` (HTTP 200; 2990966 bytes; sha256 `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`; listing capture `corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt`). S234 (kv-store-grpc grader): re-fetched live at the pin (HTTP 200; sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e`; capture `corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py`).
- **Frozen located quotes for this round's gate (each ≤25 words, verbatim, grep -F-able in its capture):**
  - S183, `corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py`: `assert parallel_linear_path.exists(), f"File {parallel_linear_path} does not exist"`
  - S233, `corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt`: `sqlite-amalgamation-3540100/sqlite3.c` (9582521 bytes)
  - S234, `corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py`: `assert result == 0, f"Port {port} is not listening - no real gRPC server is running"`
- **F2 — mistake mining.** Round-65 spot-check rows 3 and 5 (`corpus/lessons/round-65-verifier-spotcheck.md` §4): S234 `teaches` is meta-text ("supersedes S230 — … teaches is one benefit within the word bar"); S233 located quote `"sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h"` is not in the listing. Both are `## Mistakes` rows in `corpus/lessons/round-66.md` with `captured-by: none`. Fix (counter): `plans/round66_registry_check.py` with two checks — `quote` (every `QUOTE` line of a lesson Gate is `grep -F`-able in its named capture) and `meta` (a `teaches` cell containing a frozen meta phrase is refused). Shown able to fail: the current S233 and S234 rows fail their checks (red); the superseding rows S236/S237 pass (green). Fix counts only with that red→green receipt.
- **F3 — routed defects of round 65 (dated corrections, append-only).** Q47 base statement in this round's report; `battery-run.txt` pointer → `corpus/evidence/round65/sqlite-gcov-probe.txt`; `census-before.txt` relabelled by a dated correction with the base count 224 (`git show <base>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`); the round-end census pointer is re-cited to a committed output; the capability row for `offline-db-state-grader-probe` is appended to the SCORECARD capabilities table.
- **Registry changes (frozen).** S236 (supersedes S233 — the located quote is replaced by a verbatim listing line) and S237 (supersedes S234 — the teaches cell states one grounded benefit). S183 status `queued` → `mined` with `used-by` = the new knowledge entry (logged old→new in the lesson). S232's used-by is unchanged. No row is appended that no admitted entry cites (CORPUS rule 4).
- **Assimilation: none.** The merge/kengaku package's id collision is an open L0 question (`kengaku | round-54`: 114 collisions measured; adoption blocked); this round adopts nothing. The `considerthese/` item, if any qualifies, is recorded in the lesson (see the wave's connector seat).
- **Census.** Start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0 (captured in `corpus/evidence/round66/census-start.txt`). End must also be exit 0.
