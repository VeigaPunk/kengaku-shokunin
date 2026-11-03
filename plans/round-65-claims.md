# Round 65 — frozen claims (kengaku, 2026-11-03)

Base tip `12a6255170bcc466029bf82037885fd69e20370f` (`refs/heads/master` == `origin/master` at
round start, per `jj-lane.sh state` local=remote=ahead=0). This document is written and committed
BEFORE any scored run (the pre-freeze control captures named below were measured before this
freeze and are committed in the same landing). Predicates, counters, kill rules and controls
below are fixed; a seat may not change them. A rule changed after any scored receipt is not this
claim's rule (kumitate r42). Any later amendment is a new dated section, never an edit.

Round shape: one v1 wave, 12 seats (`.ufo/waves/round-65/w1-spec.json`), build + attack.

Host note (run-15 addendum: host differences are re-measured, never re-declared): this round runs
on the Linux/omp host (Arch, python 3.14.8, bwrap 0.13.1, uv 0.13.0; host gcc/gcov 16.2.1,
sqlite3 3.54.0). The r62–r63 "canonical WSL environment" does not exist here; every counter this
round declares is re-derived on this host from committed bytes. Host toolchain notes recorded at
`corpus/evidence/round65/`.

## Declared claims (2), distinct axes

| claim | axis / capability | before → after | score effect |
|---|---|---|---|
| R65-C1 | coverage (lowest non-retired axis, L0-capped at 7) — capability acquisition `offline-db-state-grader-probe` | TB2 class `db-state`: 0 members executed (`CLASS db-state count=2 members=query-optimize,sqlite-with-gcov` in `corpus/evidence/round62/class-survey.txt`; `grep -c sqlite-with-gcov corpus/evidence/round52/graders/executed17.lst` → 0, rc 1) → `sqlite-with-gcov` executed offline under this frozen predicate | score held at 7 (L0 cap `kengaku \| round-25/33/51`, still open — nothing assumed answered) |
| R65-C2 | calibration (held at ceiling 10, exercised) — the round-64 non-author closure's four routed defects land as dated, append-only corrections (`corpus/lessons/round-64-verifier-spotcheck.md` §7 items 1–4) | red-before: all four correction counters are 0 at base (`corpus/evidence/round65/c2-before-counters.txt`) → after: S234 supersedes S230 (quote form + teaches length), the round-64 lesson carries a dated erratum, SCORECARD qualifies its freshness-10 claims as addendum-classified, QUALITY gains Q47 | calibration held at 10 |

Causal separation: C1 artifacts = the probe, its receipt, the knowledge entry, the capability row,
S232/S233, the SKILL `db-state` row flip. C2 artifacts = the S234 superseding row, the round-64
lesson erratum block, the SCORECARD dated correction block, and QUALITY Q47. C1 and C2 share no
artifact and no file; both share only this claims doc.

Why `sqlite-with-gcov` and not `query-optimize`: the other db-state member hard-codes a timing
threshold (`solution median ≤ 1.05 × golden median`) and a 250 MB-class external database
(`oewn.sqlite`, sha-pinned inside the grader), so its legs are not safely freezable before data on
this host; `sqlite-with-gcov` has three deterministic artifact/PATH legs, and the host already
carries gcc/gcov 16.2.1 and the amalgamation fetch is one named small open. `query-optimize`
stays recipe-unexecuted, named in the SKILL row flip. `process-environment` members need torch
wheels (absent for cp314) or Windows installers — same reasoning as r64's nginx/vim rejection.

---

## R65-C1 — offline execution of the `sqlite-with-gcov` grader

**Grader under execution:** `corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py`,
sha256 `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` (=
`corpus/evidence/round52/graders/SHA256SUMS` line 167). Three test functions, graded in file
order: (1) `test_sqlite_compiled` — a `sqlite3` binary on PATH answers `SELECT sqlite_version();`;
(2) `test_sqlite_in_path` — `shutil.which("sqlite3")` resolves and answers `SELECT 1;`;
(3) `test_gcov_enabled` — after the grader itself runs `sqlite3 :memory: 'SELECT 1;'`, a walk of
`/app/sqlite` must find ≥1 `.gcda` file and ≥1 `.gcno` file. The grader imports stdlib only
(`os`, `shutil`, `subprocess` — AST scan receipt
`corpus/evidence/round65/grader-import-scan.txt`), so no venv and no PyPI open is needed: the
legs run under the sandbox `/usr/bin/python3` with the grader bound read-only at
`/tests/test_outputs.py`.

**The candidate is lane-authored:** a gcc-built, gcov-instrumented `sqlite3` compiled from the
pinned SQLite amalgamation (S233: `https://sqlite.org/2026/sqlite-amalgamation-3540100.zip`,
sha256 `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`, byte-verified at run
time) placed under `/app/sqlite` and staged on PATH by the driver (`PATH=/app/sqlite:$PATH`).
The host's real `/usr/bin/sqlite3` (3.54.0) is MASKED in cases G1–G4 by a bwrap
`--ro-bind /dev/null /usr/bin/sqlite3` (measured pre-freeze: `which` → None,
`subprocess.run` → `PermissionError`), so a pass can only come from the lane-built binary.
`.gcda` files are written at exit to the ABSOLUTE path recorded at compile time; the probe
therefore compiles each case's build in place under the case dir and binds the case dir at BOTH
`/app` and its host path (writable), so the recorded paths resolve inside the sandbox. This
compile-path behaviour is load-bearing and is exactly what case G4 pins (a copied binary from a
foreign compile dir emits no `.gcda` inside the sandbox — measured during pre-flight, recorded in
the claims notes, not a scored case).

**Probe:** `plans/round65_c1_sqlite_probe.py` (built in the wave). House sandbox shape (r37/r63/r64):
bwrap `--ro-bind /usr /usr` + `/bin`,`/sbin`,`/lib`,`/lib64` symlinks + `/etc` read-only +
`/proc`,`/dev` mounted + `/tmp` tmpfs + case dir at `/app` (+ its host path) + grader at
`/tests/test_outputs.py` + driver at `/ctl/driver.py`. The venv of r63/r64 is REPLACED by the
sandbox `/usr/bin/python3` (stdlib-only grader — recorded as a named house-shape delta). No port
is bound by any leg of this grader; the probe records a no-bind observation instead of the r64
port discipline, and never kills any PID (no server is started). Setup refusals (exit 2): grader
sha drift or `def test_...` order drift, amalgamation zip sha drift, missing bwrap/gcc/gcov,
amalgamation zip missing. The expected vector is DERIVED at run time from the case declarations
and compared to the frozen literal; a derivation that disagrees with the freeze aborts the
battery (SETUP prediction-drift) instead of grading (r59 lesson M-1).

**Leg rule:** P iff the test function returns normally; F on any exception. Legs run in file
order in one sandbox process per case.

**Frozen vectors (cases × legs 1–3):**

| case | setup | frozen vector |
|---|---|---|
| G1 | compliant: `--coverage` build (gcda+gcno) in `/app/sqlite`, on PATH, system binary masked | `P P P` |
| G2 | do-nothing control (L1-measured pre-freeze): empty `/app`, masked | `F F F` |
| G3 | no-instrumentation build (plain `gcc -O0 -g`, no coverage flags), on PATH, masked | `P P F` — leg 3 names `No .gcda files found` |
| G4 | arcs-only build (`-fprofile-arcs`, no `-ftest-coverage`), on PATH, masked (L1-measured pre-freeze) | `P P F` — leg 3 names `No .gcno files found` |
| G5 | masking-off control (L1-measured pre-freeze): empty `/app`, NO `/dev/null` bind — the host's `sqlite3` 3.54.0 answers legs 1–2 | `P P F` — leg 3 names `No .gcda files found` |

G3 vs G4 vs G5 share the P/P/F shape; the frozen per-leg message fragments are what separates the
mechanisms (`No .gcda` for G3/G5, `No .gcno` for G4), and the receipt records each case's setup
line so the closure reads which mechanism produced which cell. G5 is the negative control for the
masking discipline itself: without the bind, legs 1–2 pass spuriously on the host binary — the
demonstration that every G1–G4 leg-1/2 PASS is attributable to the lane-built candidate.

**Q45 captures (before the freeze).** The predicate names three grader-printed string fragments;
each was captured pre-freeze (committed this landing):
- `corpus/evidence/round65/g2-capture.txt` — masked, empty `/app`: legs
  `F(PermissionError) / F(AssertionError: sqlite3 not found in PATH) / F(PermissionError)`;
  fragment `sqlite3 not found in PATH` captured.
- `corpus/evidence/round65/g4-capture.txt` — arcs-only build: legs `P / P /
  F(AssertionError: No .gcno files found, gcov instrumentation may not be enabled)`.
- `corpus/evidence/round65/g5-capture.txt` — unmasked control: legs `P / P /
  F(AssertionError: No .gcda files found, gcov instrumentation may not be enabled)`, with the
  ENV line showing `which_sqlite3=/usr/bin/sqlite3` (version 3.54.0) against the masked captures'
  `which_sqlite3=null`.
- `corpus/evidence/round65/g1-capture.txt` — positive-path pre-capture (Q44 spirit):
  `P / P / P` with `sqlite3_version 3.54.1` (the lane-built binary answering).

**Predicate R65-C1 (one sentence, the same in this plan, the probe's check and the receipt):**
pass iff, in the receipt of record, the observed 3-leg vector for each case G1–G5 equals the
frozen vector above, AND the G2 receipt records the captured leg-2 failure fragment
`sqlite3 not found in PATH`, AND the G4 receipt records the captured leg-3 fragment
`No .gcno files found`, AND the receipt records the grader sha256 equal to
`b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b`, the amalgamation zip sha256
equal to `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`, the host
gcc/gcov version line, and a no-bind observation for every case.

**Counting command (re-derivable from committed bytes):**
`python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt; echo $?`
→ last line `PREDICATE R65-C1 pass`, exit 0.

**Named limitation:** `--check-receipt` re-derives text fields only and cannot prove a live run.
The live evidence is the per-case compile+leg run inside the battery (receipt records the per-case
driver invocation and the emitted `.gcda`/`.gcno` file lists); the wave's seat log is the run
witness. The limitation is named wherever the checker is cited (r63/r64 precedent).

**Kill rules:**
- G1 any leg F → the candidate or the instrument is wrong; MISS as declared, honest stop, no
  re-freeze this round.
- G2 or G5 reproduces G1's `P P P` → the masking discipline or the counter is wrong (a do-nothing
  or spurious environment passing is exactly the kake-r34 trap); the claim is dead and the round
  reports it. Not patched, not re-frozen.
- Any observed vector differing from the frozen five → MISS as declared; no re-freeze this round;
  the miss and its evidence are reported (r59/r63 precedent).
- A SETUP refusal (exit 2) is not a MISS; it is recorded with its reason and the claim is
  unproven this round.

**Do-nothing control status:** G2 is the control and was measured BEFORE this freeze; its vector
differs from G1 in all three legs, so a do-nothing run cannot satisfy the frozen predicate. The
counting command also cannot pass on a fresh clone (the receipt file does not exist there).

**Capability row (enters only if the predicate passes):**
`offline-db-state-grader-probe` → runs a TB2 grader whose graded state is database/toolchain
artifacts the lane builds (a gcov-instrumented `sqlite3` compiled in-place from the pinned
amalgamation, PATH-staged in bwrap, with the system binary masked) against a frozen 5-case × 3-leg
prediction table → `python3 plans/round65_c1_sqlite_probe.py --check-receipt
corpus/evidence/round65/sqlite-gcov-probe.txt` → first working round 65.

**On a pass:** the SKILL decision table's `db-state` row flips its status cell (dated note in
LOG): `executed 1 of 2 (round 65, R65-C1 pass): sqlite-with-gcov replayed offline;
query-optimize stays recipe-unexecuted` (its timing-threshold design is the named reason). The
r63 depth gate is re-run after the flip and must stay green (`ROWS n=16 class_match=True
count_mismatch=0` — member counts are untouched). The r62 class-census receipt is frozen r62
evidence and is NOT edited; the flip is recorded in SKILL + LOG + the round report. The knowledge
entry `corpus/knowledge/tb2-sqlite-gcov-offline.md` is admitted (S232/S233 cited).

**Sources:** S232 (the grader at the pin, tier A code) and S233 (the SQLite amalgamation, tier A
official artifact) are opened live this round, written at the freeze, cited by the knowledge entry
above; their ≤25-word located quotes and access dates land in the round-65 lesson `## Gate`.

---

## R65-C2 — calibration: the round-64 closure's four routed defects land as dated corrections

**Defects of record (`corpus/lessons/round-64-verifier-spotcheck.md` §7, non-author closure; the
four defects are re-derived from filed bytes in `corpus/evidence/round65/c2-before-counters.txt`):**
1. **S230 quote form** — the round-64 lesson's `## Gate` and the S230 anchor cell quote the
   RENDERED f-string (`Port 5328 is not listening - …`) at grader line 96; the source line is
   `assert result == 0, f"Port {port} is not listening - no real gRPC server is running"`.
2. **Freshness ceiling wording** — round-64's freshness-10 claims must say `addendum-classified`
   (the 29 frozen entries' openings still carry TRIO-OPEN openings with dated addenda; the bare
   provenance-trio rule remains red by design).
3. **Path base in report** — wave evidence paths must be cited lane-root-based
   (`kengaku-shokunin/.ufo/waves/round-65/…` or a stated lane-root base).
4. **S230 teaches length** — the row's `teaches` cell is 34 words (counted with
   `awk -F'|' '{print $8}' | wc -w` at base; the spotcheck said 37 by its own count); CORPUS asks
   one grounded learner benefit.

**Repairs (each an APPEND; no filed byte is rewritten):**
1. New registry row **S234**, tier A code, same URL/capture as S230, whose `teaches` opens
   `supersedes S230 —` and whose anchor quotes the grader's own f-string verbatim
   (`f"Port {port} is not listening - no real gRPC server is running"`, line 96) with a `teaches`
   of ≤25 words. S230's row stays byte-identical. The kv-store knowledge entry gains an appended
   dated addendum re-pointing its citation to S234 (append-only precedent: the round-64 trio
   addenda).
2. `corpus/lessons/round-64.md` gains an appended `## Erratum (round 65)` block dated 2026-11-03
   correcting the Gate quote form (marker token `R64-ERRATUM-65`), citing the spotcheck §7.1 and
   the grader source line.
3. `SCORECARD.md` gains an appended dated correction block (after the round-64 section) marking
   the round-64 freshness-10 claims `addendum-classified`.
4. `corpus/QUALITY.md` gains criterion **Q47 — wave-evidence paths in lane reports are cited
   lane-root-based or state the lane-root base**, citing the round-64 spotcheck §7.3 as its
   lesson. (Defect 3's remaining half is satisfied by this round's report itself.)

**Predicate R65-C2 (one sentence):** pass iff, at the landing tip, the four frozen counting
commands return exactly their target values over committed bytes —
`grep -c 'supersedes S230' corpus/SOURCES.md` → `1`;
`grep -c 'R64-ERRATUM-65' corpus/lessons/round-64.md` → `1`;
`grep -c 'addendum-classified' SCORECARD.md` → `≥1`;
`grep -c 'Q47 —' corpus/QUALITY.md` → `1` —
AND `cmp` of every touched filed file proves the landing is a pure append over the base bytes
(SOURCES.md, corpus/lessons/round-64.md, SCORECARD.md, corpus/QUALITY.md, and the kv-store
knowledge entry all keep their base bytes as a byte-prefix), AND the round-65 lesson logs each
registry old→new.

**Counting commands:** the four greps above, run at the landing tip and pasted with their outputs
in the round report and SCORECARD.

**Kill rules:**
- Any counter unmoved at close → the claim fails (honest stop; the defect stays open and is
  reported).
- A repair that requires an in-place rewrite of filed bytes → the repair is refused; the claim
  fails; the append-only rule outranks the defect list.
- The S234 `teaches` exceeding 25 words or the S234 row failing the census (11 columns, no `|`
  inside cells, tier/kind enums) → the row is refused and the claim fails.

**Do-nothing control status:** all four before-values are 0 at base
(`corpus/evidence/round65/c2-before-counters.txt`, measured at `12a62551`); a control that lands
nothing cannot move any of them, and the byte-prefix clause cannot be satisfied by a non-append.

---

## Round verdict rules (fixed now)

Each claim is judged ONLY on its declared predicate, counting commands and kill rules as written
above. A miss is reported as a miss; nothing is re-frozen after a scored receipt. Admission
additionally requires: no owned axis harmed (depth 10, calibration 10, operability 10, freshness
10, adjacency 9, novelty 8, coverage 7 L0-capped — each re-stated with evidence in the round
report), the census exit 0 at round end, and the frontier step landed (census before→after, the
round lesson's `## Gate` + `## Mistakes`, the sourced-claim clause carried by C1 via S232).

---

## Amendment A1 (dated 2026-11-03)

Written after the wave's seats settled (FreezeReview F1/F2/F7/F8, ClaimFalsifier C2(h) and C2(g)) and before any R65-C2 after-receipt was scored or any landing re-run of the byte-prefix clause. Predicates for R65-C1 are unchanged. The lesson of record is `corpus/lessons/round-65.md` `## Mistakes` rows 1, 2 and 7.

- **(a) Byte-prefix clause, restated.** The clause "all keep their base bytes as a byte-prefix" is replaced for R65-C2 by: for each touched file, `git diff --numstat 12a6255170bcc466029bf82037885fd69e20370f -- <file>` reports zero deleted lines, AND `diff <(git show 12a6255170bcc466029bf82037885fd69e20370f:<file>) <file> | grep -c '^<'` is `0`. Intent kept: no filed byte is rewritten or removed. Reason: the freeze's own registry rows were placed between S231 and `## Paths` (the census-required insertion point), so the literal byte-prefix reading was unsatisfiable by any append-only landing. Shown able to fail: `corpus/evidence/round65/a1-prefix-check.txt` (five touched files `deleted_base_lines=0`; a fixture with one base line removed `deleted_base_lines=1`).
- **(b) SCORECARD placement.** The round-64 correction block is appended at end of file, not before `### Planned (round 65)` (that placement would have been a mid-file insertion under the same append-only intent).
- **(c) Counter 1.** `grep -c 'supersedes S230' corpus/SOURCES.md` is already `1` at the freeze tip (S234 landed with the freeze). Its target is therefore read as an end-of-round value (`= 1`), not a base-relative "moved" count. Counters 2–4 keep the base-relative reading (`0` at base, target `1` / `≥1` / `1`).
- **(d) Landing tip.** "At the landing tip" means the round-end tip.
- **(e) Named limits carried, not amended.** ClaimFalsifier C1(e) (a fabricated receipt passes `--check-receipt`) and C2(g) (content-free appends satisfy the four greps) are carried as named limitations; the lesson's `## Mistakes` rows 5 and 7 record them as open.

Scope of A1 is limited to the byte-prefix clause, the SCORECARD placement, and the reading of counter 1 and the landing-tip phrase. It does not change any vector, fragment, sha pin, kill rule, or counting command for R65-C1.
