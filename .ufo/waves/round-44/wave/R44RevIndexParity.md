# R44RevIndexParity — corpus/README.md ↔ disk index parity audit (round 44, 2026-10-26)

Independent, read-only audit of `corpus/README.md` against disk, both directions, for
`knowledge/`, `lessons/`, `evidence/`; plus a re-run of the `PROVINCE.md` surface checks.
Reviewer seat R44RevIndexParity; lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`;
no subagents, no lane writes (report + subdir only), no envelope needed for the parity scan
itself (pure reads); the four executed PROVINCE instruments ran under the round-44 envelope (§5).

## 1. Pin

- Final audit run: lane HEAD `02287eeddd912268655aba4014b1e277ab434e1e` ("round-44: closure R1/R2 … README index parity (62/62 lessons) …"),
  `corpus/README.md` sha256 `a592333334454473466b5056879acd9dcb2d9f8de4a81d9ff9862d4ed4dedf9a`, 20:52 local.
  Command: `git rev-parse HEAD; sha256sum corpus/README.md; sh .ufo/waves/round-44/wave/R44RevIndexParity/routed-check.sh` → `dangling=0 missing=0`, exit 0.
- Lane moved during the audit (disclosed, not my writes): `5e3d3aa0` (audit start, ~20:33) → `2a263e5a` (~20:43, feal-linear package + README rows) → `256cc66a` (~20:45) → `02287ee` (~20:46–48, the parity batch). The audit therefore reports three pinned snapshots (§3).

## 2. Method and conventions

- Both directions over `corpus/knowledge/`, `corpus/lessons/`, `corpus/evidence/` (690 files at final pin: 51 + 63 + 576; `find corpus/knowledge corpus/lessons corpus/evidence -type f | wc -l`).
- An index token is a backticked README span that targets one of the three trees (after stripping `corpus/` or `../`, a trailing `/`, and a `:N`/`:N-M` line suffix). `*` globs and `{a,b}` braces expand; a pattern resolves when ≥1 path matches.
- Direction A (rows resolve): every such token must exist on disk. Reported for table first-cell rows only (the lane's round-13 census convention) and for all tokens.
- Direction B (files have rows): a file is covered when its own corpus-relative path is a token (exact or glob match) or — `evidence/` only — an ancestor `evidence/` directory is a token (README indexes evidence by directory rows/bullets).
- Tool: `.ufo/waves/round-44/wave/R44RevIndexParity/index_parity_check.py` (read-only, exit 0 iff clean). Cross-check: the lane's own `python3 evidence/round13-coverage/coverage_census.py` run from `corpus/` (WORKTREE snapshot).
- No dangling was found at any snapshot; every number below was produced by the named command, outputs staged in the report subdir.

## 3. Results — three pinned snapshots

| Snapshot (command) | Files | dangling (any token) | files without a row | Note |
|---|---|---|---|---|
| Run 1, ~20:33, HEAD `5e3d3aa0` (`python3 index_parity_check.py <lane>`) | 688 | 0 raw; 9 pattern tokens, all resolve on expansion (19+4+3+2 probe/attrib log globs; brace pairs round9/11/12) | **127** (lessons 29, evidence 98 — of which 28 root-log files covered only by glob tokens) | pre-batch debt |
| Runs 2–3, 20:44–45, HEAD `2a263e5a`→`256cc66a` | 689 | 0 | **86** (lessons 29, evidence 57; round44 down to 1 pending file) | still pre-batch |
| Runs 4–6 (three identical runs, 20:48–20:52), HEAD `02287ee` | 690 | 0 | **0** | parity batch landed mid-audit |

Direction A never fired: `dangling_table_rows=[]` and `dangling_any_token=[]` at every snapshot; no duplicate first-cell rows.

The 86-file pre-batch inventory (receipt `missing-run2.txt` in this subdir):
- **29 lessons with no README row**: `round-29-verifier-spotcheck.md` plus rounds 30–43 both files (`round-N.md`, `round-N-verifier-spotcheck.md`). knowledge/ was clean throughout (50/50, then 51/51).
- **evidence/**: `round30/` (10 files), `round31/` (11), `round32/` (4, incl. `catalogs/`), `round33/` (3) — no README section at all; `round35/` 3 receipts (`census-before.txt`, `census-after.txt`, `hardening-counterexamples.txt`); `round41/` 14 (`constraints-dry-cases-freeze.txt`, `pr245-body.md`, the `tb2-constraints-scheduling/` captures, a `.pyc`); `round42/` 11 (`fibsqrt-dry-cases-freeze.txt` + `tb2-circuit-fibsqrt/` captures); `round44/` 14 before `2a263e5a`, 1 after (`feal-linear-dry-cases-freeze.txt`, closed by the batch).
- The 28 r19–r23 receipt logs live at `corpus/evidence/` (`probe-r19-*` 19, `attrib-r2*` 9) and were covered only by glob tokens inside lessons rows.

**Closure:** lane commit `02287ee` (subject: "… README index parity (62/62 lessons) …") landed while the audit ran. Corroboration at that HEAD, `python3 evidence/round13-coverage/coverage_census.py` from `corpus/`: `knowledge indexed 51/51 dangling []`, `lessons indexed 63/63 dangling []`. Spot checks: rows now exist for `lessons/round-33.md`, `lessons/round-44.md`, `evidence/round41/tb2-constraints-scheduling/`, `evidence/round30/`, `evidence/round44/feal-linear-dry-cases-freeze.txt`.

## 4. Findings (open items, severity-ordered)

1. **MINOR (hygiene) — 10 committed `.pyc` files under evidence captures.** `find corpus -name '*.pyc'` → `evidence/round35/tb2-eval/__pycache__/` (3: cpython-314, -313, -313-pytest-8.4.1), `evidence/round36/tb2-regex-log/__pycache__/` (6: 311–314 + two `.opt-1`), `evidence/round41/tb2-constraints-scheduling/__pycache__/` (1: cpython-314). These are import byproducts of the probes byte-compiling the captured `test_outputs.py` in place — not durable run bytes, not pinned in any `SHA256SUMS`, and undisclosed by their rows ("the ten pinned `constraints-scheduling` files … with `SHA256SUMS`", README:599 — the directory holds 11 files + this 12th). Suggest the L1 `git rm` the three `__pycache__/` dirs at the next corpus touch (not done by this seat).
2. **MINOR (label drift) — "Root-level receipt logs".** The README table (README.md ~:96) lists the 28 r19–r23 logs as bare filenames and calls them root-level, and PROVINCE.md's round-24 Core row repeats "plus 28 root receipt logs indexed in `corpus/README.md`" — but the bytes live at `corpus/evidence/`, and `corpus/<name>` does not exist. The rows resolve only via the glob mentions in lessons rows (`evidence/probe-r19-*.log`, `evidence/attrib-r2*-*.log`, …). Suggest an append-only relabel ("`evidence/` receipt logs") when the table is next touched.
3. **MINOR (convention drift) — the standing census can no longer see evidence indexing.** At HEAD `02287ee`, `coverage_census.py` reports `evidence dirs indexed 23/38` with 15 dirs "unindexed": `round29-attempt2`, `round30`–`round33`, `round35`–`round44` — all of which are indexed as bullet/heading tokens, a form its `parse_index` (table first-cells only, `coverage_census.py:133-154`) ignores. Its knowledge/lessons verdicts are clean (51/51, 63/63). If bullets are the accepted indexing form for post-34 evidence, a one-line note in that tool's docstring (L1's call) would stop the census from reporting debt that is not there — and keep it loud about real table-row regressions.
4. **INFO — SOURCES row-count pins are population-scoped.** `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 139 today. The 25/37/42-row statements in PROVINCE.md are frozen-population counts with explicit supersession chains (R26-E3: "count `SOURCES.md` ids ≤42, not future additions") — no violation; recorded so a future census does not misread them as current-state claims.
5. **INFO — mid-audit churn.** Three HEADs and an uncommitted README edit landed during the audit window; the final pin (§1) re-measured parity on the then-current bytes (`a5923333…`): 0/0, exit 0. If the round-close batch touches README again, re-run §6's check.

## 5. PROVINCE.md surfaces — re-verified 2026-10-26 20:45–20:52

Every §Province-map Core check re-run; **all resolve as documented**:
- `test -e grader.py && sha256sum grader.py` → `90c87c88…e941f` full match (`90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f`).
- `plans/attrib_probe.py` sha256 → `489f938a…16e06b` exact (`489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b`); `attrib-r21/22/23-frozen.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md` present.
- `sha256sum ~/.local/share/ds-flash-shim/shim.py` → `42d86d99…15a386` exact; `ss -ltn 'sport = :8791'` → LISTEN on `127.0.0.1:8791`; `:34113` → no listener (as documented).
- The 18 documented-ABSENT home paths (`llm-wiki`, `~/archive/bench-arena`, `~/bench-arena`, `~/Projects/bounties*`, `the-bounty-hunter`, `~/.bailian` ×3, qwen service/jinja, `/proc/1299/cmdline`) — all still absent; none returned.
- The 12 named evidence dirs (`round8-horizon` … `round18-kimi-routing`) — all present (`test -d` loop, no output).
- Instruments (executed lane code → envelope; all four runs `local_bin_content` unchanged):
  - `python3 plans/state_check.py --summary` → exit 0, `VERDICT: PASS — all comparable frozen assertions match`; `--selftest` → exit 0.
  - `python3 plans/attrib_calibration.py --summary` → exit 0 (`scored_trials=92 correct=92 … stored_checks=119 mismatches=0`); `--selftest` → exit 0 (`18 checks, 0 failed`).
- **All 30 sibling-lane pointers resolve at their named bases** (existence-only; nothing opened): tameshi (PROVINCE.md, SKILL.md, `tools/env-diff.py`, `tools/mutate-and-run.sh`, `.ufo/evidence/round-18/defect-probes.py`), kumitate (PROVINCE.md, SKILL.md, `scripts/{cap-run,cap-spawn,bind-oracle}.mjs`, coordinator-topologies + round-63 lessons), mado (SKILL.md, `quality/counters/c1-r40-live-v2.py`, `c1-r41-globals.py`, `.ufo/waves/round-20/isolate.sh`, round-15 lesson), kake (`.ufo/waves/round-36/sealed_count_v2.py`, `round-42/c42_count.py`, `round-57/c57_idresolver_gate.py`), mori (`.ufo/waves/round-31/count-c2-a1.py`), kotodama (SKILL.md, `reports/round-39/calib/isolation-replay-protocol.md`), kaidoku (SKILL.md, PROVINCE.md, `tools/round-31/sqlite_oracle.py`), chousa/kotoba/lore PROVINCE.md, kagi `corpus/knowledge/surface-census.md`, kasegi `corpus/knowledge/repo-git-state.md`. Lane-internal `.ufo/waves/...` pointers (R37/R38/R39/R40–R43 stage-checks and build files) all resolve. `scripts/generate_test_data.py` (WebArena @ dce04686) is a pinned external snapshot, unresolvable on host by design.
- No PROVINCE surface was found that "no longer resolves" beyond the already-documented ABSENT rows.

## 6. Checker for a routed row `check` (tested)

Self-contained, run from the lane root; exit 0 exactly when no in-scope index token dangles and no file is unindexed:

```
sh .ufo/waves/round-44/wave/R44RevIndexParity/routed-check.sh
```

Tested: clean lane → `dangling=0 missing=0`, exit 0 (three runs, HEAD `02287ee`); planted stray `corpus/lessons/zz-stray-unindexed.md` in a throwaway `git clone --shared` scratch clone → `missing=1` naming the file, exit 1. The script's body is the paste-able form if a wave-relative path is unwanted; logic and conventions are documented in its header and in `index_parity_check.py`.

## 7. Receipts (this subdir; all < 1 MiB)

`index_parity_check.py` (auditor), `routed-check.sh` (routed check), `run-final2.txt` (final 0/0 run), `missing-run2.txt` (pre-batch 86-file debt receipt), `parity-summary.json`, `province_check.py` + `province-check.txt` (79 resolved / 18 documented-absent home paths / sibling pointer sweep), `state-check-{summary,selftest}.txt`, `attrib-cal-{summary,selftest}.txt` (envelope receipts). Scratch cleaned with `scratch_guard.py safe-rm` at close.

## 8. Residual risk and verification gaps

- The lane was being edited throughout (four HEADs, plus README bytes changed between my 20:48 and 20:52 pins); the 0/0 verdict is pinned to §1's bytes, and §6 re-checks it in one command.
- Coverage is token-based: a file referenced only inside a table's *second* cell counts as covered if the same path appears as a token anywhere (including prose). This matches how the README actually indexes (dir rows + bullets), and direction-A resolution still applies to every such token; but a row whose *entry cell* was deleted while a prose mention survived would not be flagged as a row loss.
- Sibling-lane pointers were existence-checked only (lane sovereignty; contents unread). PROVINCE line-number anchors (`:N`) inside resolved files were not re-verified line-by-line.
- The lane census's 15-dir "unindexed" residual (finding 3) is a convention question for the L1, not a byte defect; I did not change the census tool or README.

VERDICT: parity-missing-0-dangling-0
