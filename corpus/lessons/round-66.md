# Round 66 — a tensor-parallel grader replayed offline; the round-65 receipt gate grew a `--strict` mode that refuses a fabricated receipt; and the registry's own shape checks became counters

author: kengaku L1 (round 66, attempt 1), 2026-11-03. Lane-root base for every path below:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Claims (frozen before the wave): `plans/round-66-claims.md`
(R66-C1 coverage, L0-capped at 7, capability `offline-torch-tensor-parallel-grader-probe`; R66-C2 operability,
held at ceiling 10). Wave `.ufo/waves/round-66/w1`: v1, 13 seats. The L1 files this lesson as
`corpus/lessons/round-66.md`.

## Gate

**Candidates considered this round (2026-11-03).** Three registry rows and one row-status change were in
scope: S183 (the TB2 `torch-tensor-parallelism` grader), S236 (superseding S233's anchor form), S237
(superseding S234's `teaches` form), and S183's status/used-by lifecycle for the new knowledge entry.

**Located quotes (≤25 words, verbatim, with their location).** Each line is in the form the round's own
counter reads — `QUOTE S### | <capture path relative to the lane root> | <verbatim>` — and is `grep -F`-able
in the capture it names.

- **S183** — Terminal-Bench 2.0 `torch-tensor-parallelism` grader, `tests/test_outputs.py` at pin
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-tensor-parallelism/tests/test_outputs.py .
  Accessed 2026-11-03 (live re-fetch, HTTP 200; sha256 `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`;
  `cmp`-identical to the committed capture `corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py`;
  211 lines / 7171 bytes; the same sha is `corpus/evidence/round52/graders/SHA256SUMS` line 171). Located
  quote, grader line 25 of the capture:

  QUOTE S183 | corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py | assert parallel_linear_path.exists(), f"File {parallel_linear_path} does not exist"

- **S236** (supersedes S233's anchor form) — SQLite amalgamation 3.54.1,
  https://sqlite.org/2026/sqlite-amalgamation-3540100.zip (download page https://sqlite.org/download.html).
  Accessed 2026-11-03 (live re-fetch, HTTP 200, 2990966 bytes; zip sha256
  `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`; page sha256
  `d0e3fb1a3d9a813560fb525c7124e0088f976a3bd66c330a64963649eb5b2a77`). Located quote, line 5 of the committed
  `unzip -l` listing capture (the same line carries the size 9582521):

  QUOTE S236 | corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt | sqlite-amalgamation-3540100/sqlite3.c

- **S237** (supersedes S234's `teaches` form) — Terminal-Bench 2.0 `kv-store-grpc` grader,
  `tests/test_outputs.py` at the same pin,
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py .
  Accessed 2026-11-03 (live re-fetch, HTTP 200; sha256
  `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e`;
  `cmp`-identical to `corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py`; sha = SHA256SUMS line 80).
  Located quote, grader line 96 of the capture:

  QUOTE S237 | corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py | assert result == 0, f"Port {port} is not listening - no real gRPC server is running"

**Admitted.**

1. **S236** (new row, tier A, code) — supersedes S233's anchor form. The S233 anchor cell quoted the
   composite `"sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h"`, which is **not** a substring of the listing
   capture (`grep -c -F 'sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h'
   corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt` → `0`; the listing is one file per
   row). S236's anchor names the verbatim listing line instead. `teaches` (one grounded learner benefit, 16
   words): *the amalgamation ships sqlite3.c at 9582521 bytes, the compile input a local gcov-instrumented
   sqlite3 build uses* — grounded in listing line 5 (9582521) and in the compile the round-65 probe actually
   performs (`plans/round65_c1_sqlite_probe.py:548`: `-o sqlite3 sqlite3.c shell.c -I.`).
2. **S237** (new row, tier A, code) — supersedes S234's `teaches` form. `teaches` (18 words): *seven legs
   execute in file order; the handshake accepts only grpc.RpcError as proof of a real gRPC server* —
   grounded in the capture itself: seven `test_*` functions at lines 15, 35, 50, 67, 83, 99, 138, and
   `except grpc.RpcError:` at line 128 (the only exception the handshake test treats as proof).
3. **S183 — status/used-by lifecycle for the new knowledge entry** `corpus/knowledge/tb2-torch-tensor-parallel-offline.md`
   (drafted this round by the KnowledgeDraft seat at
   `.ufo/waves/round-66/w1/KnowledgeDraft/tb2-torch-tensor-parallel-offline.md`, whose provenance trio cites
   S183 by id, URL at the pin, anchor `tests/test_outputs.py` lines 18-25 and 43-211, and the grader sha).

**Rejected, with reasons and flip conditions.**

- **S234's `teaches` cell, as written — REJECTED (form).** Reason: meta-text, not a learner benefit — the
  cell reads `supersedes S230 — same source and capture, anchor quotes the grader's own f-string verbatim,
  teaches is one benefit within the word bar`; it describes the row instead of teaching the reader
  (`corpus/lessons/round-65-verifier-spotcheck.md` §4 row 3, which disagreed with the round-65 admission;
  CORPUS.md `teaches` = "one grounded learner benefit"). **Flip:** a grounded benefit within the 25-word bar
  — satisfied by S237 above (18 words, and the text is the grader's own leg order and its
  `grpc.RpcError`-only handshake tolerance).
- **S233's located quote, as written — REJECTED (form).** Reason: the composite is not in the listing
  (`grep -c -F` → `0`, `corpus/lessons/round-65-verifier-spotcheck.md` §4 row 5, which disagreed with the
  round-65 admission; CORPUS.md rule 1 requires a quote grounded in the source). **Flip:** a verbatim listing
  line — satisfied by S236 above (`sqlite-amalgamation-3540100/sqlite3.c`, line 5 of the capture).

**Registry changes logged old→new** (CORPUS.md rule 2: only `status`, `recheck`, `used-by` change in place;
every change is logged here).

| row | field | old → new | observed base |
|---|---|---|---|
| S183 | `status` | `mined` → `mined` (unchanged) | `corpus/SOURCES.md:198` reads `mined`; `git show 12a62551:corpus/SOURCES.md` and every one of the 18 commits in the lane's `corpus/SOURCES.md` history reads `mined` |
| S183 | `used-by` | `corpus/knowledge/tb2-grader-vacuity-triage.md` → `corpus/knowledge/tb2-grader-vacuity-triage.md, corpus/knowledge/tb2-torch-tensor-parallel-offline.md` | the existing citation is real (`corpus/knowledge/tb2-grader-vacuity-triage.md:5` and `:53` cite S183); the new one is the knowledge entry admitted above |
| S183 | `recheck` | `180d` → `180d` (unchanged) | row cell 10 |
| S236 | new row | `mined`, opened 2026-11-03, recheck `180d`, used-by `corpus/lessons/round-66.md` (this lesson) | proposed in `.ufo/waves/round-66/w1/QuoteGateBuild/proposed/rows.md` |
| S237 | new row | `mined`, opened 2026-11-03, recheck `180d`, used-by `corpus/lessons/round-66.md` (this lesson) | as above |
| S233 | `used-by` | `corpus/knowledge/tb2-sqlite-gcov-offline.md` → unchanged; `status` `mined` → unchanged; `recheck` `180d` → unchanged | `corpus/SOURCES.md:249` |
| S234 | `used-by` | `corpus/knowledge/tb2-kv-store-grpc-offline.md` → unchanged; `status` `mined` → unchanged; `recheck` `90d` → unchanged | `corpus/SOURCES.md:250` |
| S232 | `used-by` | `corpus/knowledge/tb2-sqlite-gcov-offline.md` → unchanged | `corpus/SOURCES.md:248` |

**Conflict reported, not edited (the claims doc is frozen).** The frozen claims doc (`plans/round-66-claims.md`,
"Registry changes (frozen)") states "S183 status `queued` → `mined`". The committed row has read `mined` —
never `queued` — since it was opened on 2026-10-28 (`corpus/SOURCES.md:198`; the same cell reads `mined` in
every commit that touched `corpus/SOURCES.md`). This lesson logs the **observed** old value (`mined` →
`mined`) plus the `used-by` append, which is the change the round actually needs; the claims doc's wording is
left untouched and the conflict is reported to the judge.

**Registry-id note (no edit).** S236 and S237 skip S235. In this lane's registry S235 is unused
(`grep -cE '^\|[[:space:]]*S235[[:space:]]*\|' corpus/SOURCES.md` → `0` over all history), so "the next
unused" would be S235 — but S235 is a staged id of the merge/kengaku package
(`.ufo/waves/round-54/assimilation/staged-ids:159`), so the frozen choice avoids that collision. Recorded as an
observation under the open id-drift question `kengaku | round-54`; nothing edited.

**Landing-order constraint (measured, binds this landing).** `scripts/sources-census.sh` E11 requires every
`used-by` path of a `mined` row to exist on disk. Appending S183's new `used-by` before
`corpus/knowledge/tb2-torch-tensor-parallel-offline.md` exists produces
`E11 S183 missing used-by corpus/knowledge/tb2-torch-tensor-parallel-offline.md` (reproduced in a scratch copy;
receipt `.ufo/waves/round-66/w1/LessonDraft/receipts/census-proposed-rows.txt`). The knowledge entry and this
lesson must land with, or before, the registry rows.

**Census shape finding that changes how S236/S237 must be written.** As drafted in
`.ufo/waves/round-66/w1/QuoteGateBuild/proposed/rows.md`, both rows put the supersession marker in the
**source** cell (`(supersedes S233 anchor form)` / `(supersedes S234 teaches form)`) instead of opening the
**teaches** cell with `supersedes S0NN —`, as CORPUS.md rule 2 requires. `scripts/sources-census.sh:646-649`
exempts a within-scope duplicate URL only when the *teaches* cell matches `/supersedes S[0-9]{3}/`; the rows
as drafted therefore fail the census:

```
lanecopy	E04	S236 duplicate url sqlite.org/2026/sqlite-amalgamation-3540100.zip within scope offline instrument builds for db-state graders (R65-C1): the compile-input bytes the probe pins
```

With the `teaches` cells opened `supersedes S233 — …` and `supersedes S234 — …` the same scratch copy is
clean of E04 (only the pre-existing W04 duplicate-URL warnings remain) and the round's own meta counter still
passes (`CHECK meta rows=2 findings=0`, `CHECK ok meta`). The landing must therefore write the two new rows
with the `supersedes S0NN —` opener in `teaches`. Receipt:
`.ufo/waves/round-66/w1/LessonDraft/receipts/census-proposed-rows.txt`.

**The counter was amended mid-wave (state at this seat's write).** The L1's Amendment A1 changed
`plans/round66_c1_tensor_probe.py` in the working tree after the wave's seats had measured it (frozen sha
`c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3` → working-tree sha
`7640a639bbfeeb5276763fe05f63d25e14d2544d5ffc98faa0fabff1e172106e`; `git status --porcelain plans/` →
` M plans/round66_c1_tensor_probe.py`), re-issued the receipt of record (`corpus/evidence/round66/tensor/receipt.txt`
now names the amended probe sha and checks green), and added a per-receipt junit directory
(`corpus/evidence/round66/tensor/receipt.junit/`, `control-a1.junit/`). `plans/round-66-claims.md` carries no
`Amendment A1` text yet (`grep -n 'Amendment A1' plans/round-66-claims.md` → no hits). The amendment closes
three gaps this round's seats measured against the frozen bytes (Mistakes rows 10-12) and adds the round's own
new control receipt `corpus/evidence/round66/tensor/control-a1.txt` (checks green, its `junit_sha` values
equal the bytes in `control-a1.junit/`). Receipt:
`.ufo/waves/round-66/w1/LessonDraft/receipts/04-amendment-a1-state.txt`. This lesson cites the frozen bytes
where the claim is about them and the amended bytes where it is about the fix.

## Mistakes

Class · evidence pointer · captured-by · fix. Classes from the fleet mistake taxonomy (`vacuous`,
`survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`).

1. **S234 `teaches` is meta-text** · `corpus/lessons/round-65-verifier-spotcheck.md` §4 row 3 (the non-author
   closure disagreed with the round-65 admission) · captured-by: none · fix: the `meta` check of
   `plans/round66_registry_check.py` (a `teaches` cell containing a frozen meta phrase is refused), shown
   red→green: `.ufo/waves/round-66/w1/QuoteGateBuild/red/red-output.txt` (exit 1, three findings on S234)
   versus `.ufo/waves/round-66/w1/QuoteGateBuild/green/green-output.txt` (exit 0, findings=0).
2. **S233's located quote is not verbatim** · `corpus/lessons/round-65-verifier-spotcheck.md` §4 row 5 ·
   captured-by: none · fix: the `quote` check of the same counter — every `QUOTE` line of a lesson's `## Gate`
   must be `grep -F`-able in the capture it names, and a capture outside `corpus/evidence/` is refused;
   red→green in `red/red-output.txt` (exit 1, `quote S233 miss`) versus `green/green-output.txt` (exit 0,
   `QUOTE S236 … FOUND`, `QUOTE S237 … FOUND`).
3. **The R65 receipt checker admits a hand-fabricated receipt** · `.ufo/waves/round-65/w1/SecurityScan.md`
   M-1 (must fix) and the round-65 lesson's Mistakes row 5; the red-before is committed at
   `corpus/evidence/round66/red/red-before-r65-checker.txt` (`CHECK ok cases=5` / `PREDICATE R65-C1 pass`) and
   the fixture at `corpus/evidence/round66/red/fabricated-r65.txt` (its own header reads "contains NO
   live-run data") · captured-by: none — the frozen predicate checked field *presence*, never value ·
   fix: R66-C2's `--strict` mode. Measured this round by re-running the proposed gate over the committed
   bytes: strict on the fabricated fixture → exit 1 with named findings (`fabrication-declaration`,
   `toolchain-not-well-formed` ×4, `toolchain-banner-count` ×3, `probe-binding-missing`); strict on the
   committed R65 receipt → exit 0 (`CHECK ok cases=5 strict=yes`); default mode unchanged (exit 0 on both
   fixtures, `default-mode-identical=yes`). Receipt:
   `.ufo/waves/round-66/w1/LessonDraft/receipts/02-c2-strict.txt`.
4. **`battery-run.txt` was named as carrying the per-case BUILD/RUN/FILES lines; it carries CASE and
   PREDICATE lines only** · the pointer is `SKILL.md:686` (the `round65-c1-sqlite-probe` registry row:
   "the live evidence is the per-case BUILD/RUN/FILES lines in
   `corpus/evidence/round65/battery-run.txt`"), `SCORECARD.md:2885` (the round-65 capability row, "live
   witness `corpus/evidence/round65/battery-run.txt`"), `LOG.md:2512`, and
   `.ufo/reports/round-65/kengaku.md:14` and `:78`; `corpus/lessons/round-65-verifier-spotcheck.md` §6 item 5
   names `SKILL.md:83` for this pointer — that line names the **correct** file
   (`corpus/evidence/round65/sqlite-gcov-probe.txt`) and does not carry the string
   (`sed -n '83p' SKILL.md | grep -c 'battery-run'` → `0`, at every revision of `SKILL.md` I checked), and the
   routed item's `corpus/SKILL.md` path does not exist (`ls corpus/SKILL.md` → no such file); the lane's
   `SKILL.md` is at the lane root · captured-by: none · fix: a dated correction naming
   `corpus/evidence/round65/sqlite-gcov-probe.txt`, which is where those lines live
   (`grep -cE '^(BUILD|RUN|FILES|ENV) ' corpus/evidence/round65/battery-run.txt` → `0` versus the same count on
   `sqlite-gcov-probe.txt` → `20`; `battery-run.txt` is 6 lines: 5 `CASE` lines and
   `PREDICATE R65-C1 pass`). Measured: `.ufo/waves/round-66/w1/LessonDraft/receipts/03-counter-gaps.txt`.
5. **`census-before.txt` is mislabelled** (it is headed round-start but shows 227 rows and S234's duplicate-URL
   warning, so it is not a base-state capture) · `corpus/evidence/round65/census-before.txt` (its S234 warning
   is present: `grep -c 'S234' corpus/evidence/round65/census-before.txt` → `1`); the true base count is 224
   (`git show 12a62551:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `224`, and
   the round-65 report states 224→227) · captured-by: none · fix: a dated correction that states the base
   count with the command that measures it.
6. **The round-65 report did not satisfy Q47** (no lane-root base statement) ·
   `corpus/QUALITY.md:1200` (Q47) and the round-65 report — `grep -c -i 'lane-root\|lane root'
   /home/vgpnk/Projects/shokunin/.ufo/reports/round-65/kengaku.md` → `0` · captured-by: none · fix: this
   round's report states the lane-root base once (this lesson states it in its header).
7. **The round-65 report's round-end census pointer named an unreachable scratch path** ·
   `.ufo/reports/round-65/kengaku.md:57` cites `/fast/scratch/hyaku/kengaku-r65/L1/census-after.txt`, a
   directory the same report says was removed (`:106`) · captured-by: none · fix: the census output is
   committed; this round's start capture is committed at `corpus/evidence/round66/census-start.txt` (exit 0,
   24 lines) and the round-end capture lands beside it under `corpus/evidence/round66/`.
8. **The frozen claims doc's registry-change premise for S183 is false against the committed row** — it says
   "S183 status `queued` → `mined`"; the row has read `mined` since it was opened (2026-10-28) in every
   commit of the lane's `corpus/SOURCES.md` history · `plans/round-66-claims.md` ("Registry changes
   (frozen)") against `corpus/SOURCES.md:198` and `git show 12a62551:corpus/SOURCES.md` ·
   captured-by: none — the claims doc is frozen, so a seat reports the conflict instead of editing it ·
   fix: this lesson logs the observed old value (`mined` → `mined`) and the `used-by` append that the round
   actually needs; the conflict is reported to the judge.
9. **The two proposed superseding rows would fail the lane's own census as drafted** — the supersession
   marker sat in the `source` cell instead of opening the `teaches` cell with `supersedes S0NN —`
   (CORPUS.md rule 2), and `scripts/sources-census.sh:646-649` then reports
   `E04 S236 duplicate url … within scope` · `.ufo/waves/round-66/w1/QuoteGateBuild/proposed/rows.md`;
   receipt `.ufo/waves/round-66/w1/LessonDraft/receipts/census-proposed-rows.txt` (E04 present on the rows
   as drafted, absent with the `supersedes S0NN —` opener) · captured-by: none — the quote/meta counter
   cannot see the census's E04 clause, and the census was not run against the proposal before it was handed
   to the L1 · fix: the landing writes S236/S237 with `teaches` opening `supersedes S233 — …` /
   `supersedes S234 — …`; verified green on the meta counter and clean of E04 on the census.
10. **The frozen C1 receipt checker accepts a receipt with no `CASE` lines at all** — the predicate says
    "every `case_sha` and `junit_sha` equals the committed bytes", but the byte-binding clause is only
    applied to `CASE` lines that are present, so a receipt with the five `VECTOR` lines and no `CASE` line
    passes · measured this round against the **frozen** counter (sha `c5ef1b54…`): `grep -v '^CASE '
    corpus/evidence/round66/tensor/receipt.txt` → the checker prints `CHECK ok cases=5` /
    `PREDICATE R66-C1 pass`, exit 0 (receipt
    `.ufo/waves/round-66/w1/LessonDraft/receipts/03-counter-gaps.txt`); also found independently by the
    FreezeReview seat (`.ufo/waves/round-66/w1/FreezeReview/findings.md` F1) ·
    captured-by: none — the `VECTOR` side of the same clause *is* enumerated ("every CASE must be present"),
    so the asymmetry was never checked · fix: **closed in the working tree by the L1's Amendment A1** — the
    amended counter prints `CHECK defect: <case> has no CASE line` for all five cases and exits 1 (receipt
    `.ufo/waves/round-66/w1/LessonDraft/receipts/04-amendment-a1-state.txt`, A1). The claim's predicate
    sentence is not narrowed after the run; the fix makes the code enforce the sentence as written.
11. **The claims doc's pre-freeze honesty sentence about junit bytes is false as executed** — it says "the
    junit directory is receipt-local, so a re-run cannot overwrite committed junit bytes", but the frozen
    probe resolves it as `receipt.parent / "junit"`, so two receipts in one directory share it; the
    post-freeze run overwrote the committed pre-freeze junit bytes, and the frozen control receipt
    `corpus/evidence/round66/tensor/prefreeze-run2.txt` fails its own checker ·
    `plans/round-66-claims.md` line 33 against `plans/round66_c1_tensor_probe.py:221` and the measured
    re-check (5 × `CHECK defect: … junit_sha does not match committed junit bytes`, exit 1; receipt
    `.ufo/waves/round-66/w1/LessonDraft/receipts/01-c1-checks.txt`); independently found by the ProbeMutate
    seat (`.ufo/waves/round-66/w1/ProbeMutate/report.md` F-A), the FreezeReview seat (F5) and the TensorRecon
    seat (`findings.md` Finding 1) · captured-by: none · fix: **closed in the working tree by the L1's
    Amendment A1** — the junit now lives beside the receipt at `<receipt-stem>.junit/`, so a later run cannot
    overwrite another receipt's bytes (receipt `04-amendment-a1-state.txt`, A3), and the round's own new
    control `corpus/evidence/round66/tensor/control-a1.txt` checks green with its own `control-a1.junit/`
    (A5). The **frozen** control remains re-derivable only from the freeze commit's bytes: each file's
    sha256 at `9a07df6a` equals the `junit_sha` its receipt names (k1 `9c02c973…`, k2 `f1f42b55…`,
    k3 `8e5c4d5c…`, k4 `28267e68…`, k5 `8f7fa27b…`), and `prefreeze-run2.txt` is now additionally refused
    for naming the pre-amendment probe sha (A4). The lesson states which bytes each control binds; the round
    report must not repeat the "receipt-local" sentence as fact.
12. **A VECTOR line naming an unknown case crashes the checker with a traceback instead of a named
    finding** · `sed 's/^VECTOR k3-stub /VECTOR bogus /'` over the receipt of record → `KeyError: 'bogus'`
    against the frozen counter (receipt
    `.ufo/waves/round-66/w1/LessonDraft/receipts/03-counter-gaps.txt`; also FreezeReview F7) ·
    captured-by: none · fix: **closed in the working tree by the L1's Amendment A1** — the amended counter
    prints `CHECK defect: unknown case 'bogus' in a VECTOR line` and exits 1 (receipt
    `04-amendment-a1-state.txt`, A2).
13. **The counter was amended mid-wave, after the wave's own seats had measured it** — the L1's Amendment A1
    changed `plans/round66_c1_tensor_probe.py` in the working tree at 18:28 (frozen sha `c5ef1b54…` → working
    tree sha `7640a639…`; `git status --porcelain plans/` → ` M plans/round66_c1_tensor_probe.py`) and
    re-issued the receipt of record (`corpus/evidence/round66/tensor/receipt.txt` now names the amended
    probe sha and checks green, `04-amendment-a1-state.txt` A6) while `plans/round-66-claims.md` still
    carries no `Amendment A1` text (`grep -n 'Amendment A1' plans/round-66-claims.md` → no hits) ·
    captured-by: none — the claims doc is the frozen contract and no seat may edit it, so an amendment to
    the instrument that the contract names cannot be recorded there by the wave ·
    fix: the L1 lands the amendment **with** a dated `Amendment A1` block in `plans/round-66-claims.md`
    (the counter's own docstring already cites one), so the predicate, the counter's bytes and the receipt
    agree in one committed state; until then the wave's receipts 01 and 03 measure the frozen bytes and
    receipt `04-amendment-a1-state.txt` measures the amended ones, and the lesson cites both.

## Carried -> closed / open

Every routed item of the round-65 non-author closure (`corpus/lessons/round-65-verifier-spotcheck.md` §6,
items 1-10). Status is stated against this round's landing; where the closing bytes do not exist at the freeze
tip (`2c1ef88a`) the tip state is named in the evidence column, so a reader can check either.

| # | routed item | status | evidence |
|---|---|---|---|
| 1 | Capability row missing from the SCORECARD capabilities table (`offline-db-state-grader-probe` was prose only) | closed (this landing) | the capability table rows live at `SCORECARD.md:2282` (round 52) and `:2854` (round 64); round 65's section carries the capability as prose at `SCORECARD.md:2885` only, so at the freeze tip the row is still absent; this round's frontier step (claims doc F3) appends the row — its demonstration pointer is `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` and the first-working round is 65 |
| 2 | S234 `teaches` is not a learner benefit | closed | S237 supersedes it with an 18-word grounded benefit (Gate section above); the meta counter refuses the old cell (red, exit 1) and accepts the new rows (green, exit 0) — `.ufo/waves/round-66/w1/QuoteGateBuild/red/red-output.txt`, `green/green-output.txt` |
| 3 | S233's located quote is not verbatim | closed | S236 replaces it with the verbatim listing line; `grep -c -F 'sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h' corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt` → `0` (the old form), while the new needle is present in the same capture (quote check, green, exit 0) |
| 4 | The report did not satisfy Q47 | closed | Q47 (`corpus/QUALITY.md:1200`); the round-65 report has 0 hits for a lane-root base (`grep -c -i 'lane-root\|lane root' /home/vgpnk/Projects/shokunin/.ufo/reports/round-65/kengaku.md` → `0`); this round's report states the base once |
| 5 | The `battery-run.txt` pointer is wrong | closed | dated correction to `corpus/evidence/round65/sqlite-gcov-probe.txt`; the counts that decide it: 0 vs 20 `BUILD/RUN/FILES/ENV` lines (Mistake row 4). The correction must land on the four real pointers — `SKILL.md:686`, `SCORECARD.md:2885`, `LOG.md:2512`, and the round-65 report lines 14 and 78 — not on `SKILL.md:83`, which names the correct file (Mistake row 4) |
| 6 | `census-before.txt` is mislabelled | closed | dated correction stating base count 224 with the command that measures it (Mistake row 5) |
| 7 | The round-end census pointer named an unreachable `/fast` scratch path | closed | the census output is committed under `corpus/evidence/round66/` (`census-start.txt` is committed, 24 lines, exit 0); the round-65 pointer at `.ufo/reports/round-65/kengaku.md:57` is not repeated |
| 8 | Sentinel M-1 (must fix): `--check-receipt` accepts fabricated receipts | closed | R66-C2's `--strict` mode: fabricated → exit 1 with named findings, committed receipt → exit 0, default unchanged (receipt `02-c2-strict.txt`; `.ufo/waves/round-66/w1/ReceiptGateBuild/receipts/01-a…08-h`) |
| 9 | Round-65 lesson Mistakes rows 3, 5, 6, 7 remain the lane's; the first counter amendment should pin the toolchain values and bind the receipt to the probe sha | open (partly closed) | row 5 is closed by the strict mode (toolchain well-formedness + banner agreement; probe binding; `probe-sha 000… != committed f44b7283…`); the r66 C1 instrument was frozen before the wave, so the "instrument authored after the freeze" class does not recur here (`plans/round66_c1_tensor_probe.py` sha `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3` = the receipt's `PROBE` line); rows 3 (registry rows carrying unverified line/size numbers — the new registry counter checks quotes and meta phrases, not line numbers or byte counts) and 7 (a counter already at its target at the freeze tip) remain the lane's |
| 10 | Cosmetic: the round-64 erratum heading and the kv-store citation addendum heading follow a paragraph with no blank line | open | still true at the freeze tip: `corpus/lessons/round-64.md:108` → `:109` (`## Erratum (round 65)` directly after the paragraph) and `corpus/knowledge/tb2-kv-store-grpc-offline.md:229` → `:230` (`## Citation addendum (round 65)`); fix in the next append |

**L0 questions carried, nothing assumed answered:** `kengaku | round-25/33/51` (coverage L0 cap),
`kengaku | round-56`, `kengaku | round-63` (amended K2 detector), `kengaku | round-54` (merge/kengaku id
drift — 114 collisions measured; nothing adopted this round, see Assimilation).

## Discernment spot-check

A sample of this round's gate decisions, for a **non-author** seat to judge. The verdict cells are left
`pending non-author`; this lesson does not attest its own taste. The seat named to verify is
**SourceReview** (its source re-open report for this round is
`.ufo/waves/round-66/w1/SourceReview/findings.md`; as a lane-dispatched seat its report is seat evidence, and
the standing non-author verdict remains the round closure's, per `LEARNING.md`).

| # | item | decision | source to re-open | verdict |
|---|---|---|---|---|
| 1 | S236 (new row, supersedes S233's anchor form) | admit | `corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt` line 5; zip sha256 `0a9c8e34…` | pending non-author |
| 2 | S237 (new row, supersedes S234's `teaches` form) | admit | `corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py` lines 15-138, `except grpc.RpcError:` at :128 | pending non-author |
| 3 | S234's `teaches` cell as written | reject (meta-text) | `corpus/SOURCES.md:250` | pending non-author |
| 4 | S233's located quote as written | reject (not verbatim) | `corpus/SOURCES.md:249`; `grep -c -F 'sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h'` → 0 | pending non-author |
| 5 | S183 status/used-by lifecycle for the new knowledge entry | admit the used-by append; the `queued → mined` step is rejected as a false premise | `corpus/SOURCES.md:198`; `git show 12a62551:corpus/SOURCES.md` | pending non-author |

## Sources census

- Before: 227 registry rows at the round-start tip `f0587e53` (`git show f0587e53:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `227`). Round-start census, command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`: exit 0, committed at `corpus/evidence/round66/census-start.txt` (24 lines; W04 warnings only).
- After: 229 registry rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `229`). The same census command at the landing tip: exit 0, committed at `corpus/evidence/round66/census-end.txt` (W04 warnings only; no E-class findings: `grep -c 'E0\|E1' corpus/evidence/round66/census-end.txt` → `0`).

Rows added: S236 and S237 (2). Rows touched old→new: S183 `used-by` `corpus/knowledge/tb2-grader-vacuity-triage.md` → `corpus/knowledge/tb2-grader-vacuity-triage.md, corpus/knowledge/tb2-torch-tensor-parallel-offline.md`; S183 `status` `mined` → `mined`. No other row changed.

## Assimilation

`Assimilation: none` — the merge/kengaku package's id drift is still open (`kengaku | round-54`: 114
collisions measured, adoption blocked), and its staged ids already include S235
(`.ufo/waves/round-54/assimilation/staged-ids:159`), which is why this round's new rows take S236/S237. This
round adopts nothing from the package and changes no sibling-owned surface.

## Landing verdicts (L1, appended at landing, 2026-11-03)

These entries correct and close the draft above; the draft's body is kept as the wave's record. Where the draft and this section disagree, this section governs.

- **R66-C1 — admitted, on the amended counter.** Predicate met: `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt` → `CHECK ok cases=5`, `PREDICATE R66-C1 pass`, exit 0; control `corpus/evidence/round66/tensor/control-a1.txt` → same, exit 0. Capability `offline-torch-tensor-parallel-grader-probe` enters the SCORECARD capabilities block. Coverage held at 7 (L0 cap `kengaku | round-25/33/51` not lifted by a grader execution). Verdict basis: the amended counter (plans/round-66-claims.md, Amendment A1); the vector table, cases and kill rules are unchanged.
- **R66-C2 — not admitted, kill rule (b).** The frozen strict clause requires the receipt's `PROBE` sha to equal the committed probe bytes, and the committed round-65 receipt has no `PROBE` line (`grep -c '^PROBE' corpus/evidence/round65/sqlite-gcov-probe.txt` → `0`). The proposal's pass on that receipt (`ReceiptGateBuild`) rests on a path-and-version binding that the frozen text does not allow, so its committed-receipt pass is not the claim's evidence. What the proposal does show, and is carried as evidence only: strict refuses the fabricated fixture (exit 1), and the default R65 predicate is unchanged. Operability held at ceiling 10; no score change.
- **Mistake fixes, status at landing.** Row 1 (S234 `teaches` meta-text) and row 2 (S233 quote) — fixed and landed as `plans/round66_registry_check.py` (selftest 13/13; red refused, green accepted); the two rows are superseded by S236/S237. Row 3 (fabricated receipt accepted by the R65 checker) — **open**: the strict proposal is not admitted (R66-C2 kill rule b); carried to the next round as a new claim with its PROBE binding frozen before data. Rows 4–7 (dated pointer and census corrections) — **open**: not landed in this round's commits; routed to the next round with their evidence pointers, not claimed closed. Row 8 (false S183 premise) — reported, not edited (claims doc frozen; Amendment A1.8 records it). Row 9 (E04 duplicate-URL on the drafted rows) — closed: S236/S237 open `teaches` with `supersedes S0NN —`; census exit 0. Rows 10 and 12 (no-CASE receipt accepted; unknown case traceback) — closed by Amendment A1 with red→green evidence (the no-CASE receipt and the unknown-case line are refused by name; selftest). Row 11 (junit receipt-local sentence false) — closed by Amendment A1.4 (per-receipt junit directory); the pre-freeze control's bytes remain at commit `9a07df6a`. Row 13 (counter amended mid-wave without claims-doc text) — closed by Amendment A1 in the claims doc (dated).
- **Mistake mined from the sandbox review (new).** Class `scope`: the probe's bwrap sandbox shared the host network and PID namespaces (SecurityScan M-4, M-5: outbound connect succeeded; host processes were signalable). Captured-by: none. Fix: Amendment A1.3 adds `--unshare-net --unshare-pid`. Shown: the vectors reproduce under the new sandbox (`control-a1.txt` and `receipt.txt`, both `PREDICATE R66-C1 pass`, every `VECTOR` line equal to the frozen table).
- **Mistake mined from the attack seats (new).** Class `survivor` in the counter's own selftest: the round-66 selftest did not exercise the no-CASE or unknown-case paths that FreezeReview F1 and F7 named. Captured-by: none. Fix: the selftest now refuses a no-CASE receipt and a malformed VECTOR token (`SELFTEST` all True).
- **Discernment spot-check (for the round closure).** Sample: admit S236 and S237 (decisions 1-2); reject S234 `teaches` and S233 quote (3-4). The non-author source re-open is `.ufo/waves/round-66/w1/SourceReview.md` (all five checks pass: live bytes equal the captures, the three frozen quotes are grep-F-able with word counts ≤ 25, the S183 row sha equals the capture). Discernment verdict on this round's gate decisions: pending the round's non-author closure; this lesson does not attest it.
- **considerthese (one proposal, selected, not implemented).** `considerthese/2026-10-26.md`, item 2, verbatim: "One standing TB2 admission counter with a built-in filler control." Its implementing check (`grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md`) returns 0 hits; the item stays unimplemented and is recorded as the next frontier candidate (SiblingOverlap seat, `.ufo/waves/round-66/w1/SiblingOverlap.md`).
- **Assimilation: none** (see above).
- **Quality criterion.** Q49 is appended to `corpus/QUALITY.md`, citing this lesson's rows 10 and 12 and the A1 red→green receipts.

## Stale-lane line

Stale-lane: not stale. The round's wave settled 13 of 13 seats within the round; no mission was left open beyond its driver tick.
