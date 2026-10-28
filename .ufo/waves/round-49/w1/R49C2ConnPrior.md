# R49C2ConnPrior — connector (R49-C2, coverage): sibling-lane ownership of task-grader analysis/execution

seat: R49C2ConnPrior (connector, C2 coverage)
date: 2026-10-28
axes named: coverage (worked, R49-C2). No axis harmed: read-only artifact survey; no scored counter/probe run.
lane tip observed: `af88aab193e6034cb9b386472064e3c18fa90128`; stage-1 freeze `9d2900af41e4d1fc6022eff99010436fde6dbd93` verified present, committer date `2026-10-28 09:14:40 -0300`, subject `round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`. This item is ownership analysis only — the freeze check was precautionary; no scored run was made or needed.

## Item

Check whether any sibling lane owns task-grader analysis/execution; cite sibling PROVINCE paths; return a scoped ownership finding.

## Binding context read first

- `plans/round-49-claims.md` @ `9d2900af…` (read in full): R49-C2 claims admission of the round-46 TB2 `polyglot-c-py` package — `corpus/knowledge/tb2-polyglot-c-py-grader.md`, captures `corpus/evidence/round46/tb2-polyglot-c-py/`, receipts `polyglot-c-py-probe.txt` + `polyglot-c-py-dry-cases-freeze.txt`, `plans/polyglot_c_py_probe.py`, counter `plans/round49_c2_verify.py` (written w1, pinned stage 2).
- `corpus/lessons/round-48-verifier-spotcheck.md`: routed defects 1–4 (receipt path per seat, no role→alias map, V7 unsatisfiable-tag precondition, C1 mutant floor with committed receipts).
- `corpus/lessons/round-48.md`: C2 failure classes restated — r48 tip had no committed stage-2 counter; `both-print`/`toolchain` had zero violating cases; `22b7779e` probe failed 18/18 stage-checks under `RLIMIT_NPROC=48`.

## Method (exact commands run)

All reads; nothing written outside this report and `/fast/scratch/hyaku/kengaku-r49/R49C2ConnPrior` (TMPDIR; removed at yield).

1. `ls /home/vgpnk/Projects/shokunin/*/PROVINCE.md` → 21 lane files (incl. kengaku). NOTE: `glob`/`grep` tools silently skipped them — PROVINCE.md is gitignored; all greps below ran with `gitignore: false`.
2. `git -C …/kengaku-shokunin cat-file -t 9d2900af…` → `commit`; `git log -1 --format='%H %ci %s' 9d2900af…` → line quoted above.
3. `git -C …/kengaku-shokunin show 9d2900af…:PROVINCE.md | sha256sum` → `5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298` — **byte-identical to the working-tree file** (same sha256), so every PROVINCE citation below is valid at the frozen base.
4. `grep -iE 'task.?grader|grader|terminal.?bench|tb2|polyglot|grading|grade path|task.?execution'` over all `*/PROVINCE.md` → non-trivial hits only in **kengaku**, **lore** (`in-world source reliability grading` — fiction metadata), **mori** (`lane silence grading` — health taxonomy). Neither lore nor mori sense touches a benchmark task grader.
5. `grep -iE 'benchmark|scoring|judge|admission counter|task.?spec|evaluat'` over all `*/PROVINCE.md` → every eval-adjacent sibling clause is a *refusal deferring to kengaku* (cited below), not a claim.
6. `grep -rl 'terminal-bench\|terminal_bench'` over every sibling lane tree (20 lane dirs + `ok/` `research/` `scripts/` `templates/`, kengaku excluded) → re-verified the r37 sweep on 2026-10-28; results itemized below.
7. `git -C …/kengaku-shokunin ls-tree -r 9d2900af… --name-only | grep -Ei 'tb2|polyglot|regex_log|grader|test_outputs'` → all committed TB2 grader artifacts present at the freeze (12 `corpus/knowledge/tb2-*-grader.md` entries, `corpus/evidence/round35–46/tb2-*` capture trees, `plans/tb2_grader_probe.py`, `plans/regex_log_probe.py`, `plans/polyglot_c_py_probe.py`, `grader.py`, `plans/grader_perturb.py`, `corpus/knowledge/benchmark-grader-semantics.md`, `grader-perturbation-audit.md`).

## Scoped ownership finding

**No sibling lane owns — or claims — task-grader analysis or execution. It is kengaku's own ground, twice over: by domain assignment and by an admitted, re-verified prior-art inventory.**

### (a) Deed: kengaku's PROVINCE owns the surface

`kengaku-shokunin/PROVINCE.md` (frozen text, sha256 above):

- `:3` — `**Domain:** LLM/model research & evaluation` with `**Refuses:**` only cross-domain work.
- `:232–240` (r29 attempt-2 core admission) — offline synthetic-fixture execution of a pinned TB2 grader (`protein-assembly … test_gblock`, `plans/tb2_grader_probe.py`); `:244–255` (r36) adds `regex-log` execution (`plans/regex_log_probe.py`, receipt `corpus/evidence/round36/regex-log-probe.txt`); `corpus/knowledge/tb2-polyglot-c-py-grader.md` extends the series.
- `:351–356` — verbatim: `kengaku keeps: which TB2 grader is captured, how it is called offline, what its verdict answers, and the C1/C2 counters over plans/pkg_gate.py. Verified that no sibling reads, scores or claims TB2 grader execution…` (r37 `R37ConnSibling`).

### (b) Sibling PROVINCE citations — every one defers, none claims

| sibling PROVINCE path | line | clause (verbatim) |
|---|---|---|
| `chousa-shokunin/PROVINCE.md` | :10-11 | `Refuses: … model-quality or evaluation claims (→ kengaku)` |
| `kama-shokunin/PROVINCE.md` | :42 | `Refuses: model quality/eval (kengaku), …` |
| `kasegi-shokunin/PROVINCE.md` | :50 | `- kengaku — LLM evaluation and benchmarks` (adjacency list; kasegi keeps documentation corpus only) |
| `mado-shokunin/PROVINCE.md` | :14-15 | `Refuses: … model quality (→ kengaku).` |
| `game-dev-3d-shokunin/PROVINCE.md` | :77 | `LLM/model research and evaluation belong to kengaku-shokunin` |
| `tameshi-shokunin/PROVINCE.md` | :3-17 | owns the **method** (`verification-fixture craft … mutation testing … verdict-line discipline`); `Refuses: product domains — every lane's gate remains its own; … Never edits a sibling's gate code` |
| `kumitate-shokunin/PROVINCE.md` | :24 | owns coordinator-topology **decisions**, `not agent evaluation … kengaku evaluates agents` |
| `kaidoku-shokunin/PROVINCE.md` | (per kengaku PROVINCE :347-350) | owns ELF linkage ground; TB2 `ldd`-string claims route *out* to kaidoku, never grader execution |
| `kotoba-shokunin/PROVINCE.md` | :66 | adjacency row: `kengaku owns measured capability effects … (kengaku SKILL.md:3, PROVINCE.md:30-32,138)` |

Remaining PROVINCE files (`audio, game-dev-2d, kagi, kake, kotodama, lore, mori, revenger, souji, tabi, tsukuroi, kumitate` rest) contain zero grader/benchmark-execution claims — `lore`'s `reliability grading` and `mori`'s `silence grading` are unrelated homonyms.

### (c) Re-verification of the r37 cross-lane sweep (run today, gitignore off)

`terminal-bench|terminal_bench` outside `kengaku-shokunin/` resolves to **citations of kengaku artifacts only**, no ownership:

- `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md` + `corpus/lessons/round-63.md` — the two data citations the r37 sweep already ruled as such (kengaku PROVINCE :353-356). No drift.
- `kaidoku-shokunin/.ufo/waves/round-41/w2/artifacts/R41W2Reservation/tx-scan.json:19601-19604` — a captured dispatch transcript quoting a **kengaku** seat's TB2 task text.
- `kotoba-shokunin/.ufo/waves/round-71/receipts/census-after.txt:28` and `mado-shokunin/.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt:32` — census W04 warnings *about kengaku's SOURCES row S100*.
- `tabi-shokunin/.ufo/waves/round-35/w1/CritC1Counter/bg-blindspots-full.json` — quotes kengaku corpus lines for a blindspot scan.
- `tsukuroi-shokunin/.ufo/waves/round-43/w2/AdjFinal/sibling-skillmd-pin-lines.txt:93` — quotes kengaku's own `R37ConnSibling` output: `kengaku uniquely holds TB2 grader ground … zero sibling surface matches`.
- `kumitate-shokunin/.ufo/waves/round-63/…/build-dispatch.json` — forged/borrowed fixture embedding kengaku r35 dispatch text (attack material, not a claim).
- `MANIFEST.json` — `terminal-bench|task.?grader` hits (lines 25579, 26082) are kengaku recheck strings inside kengaku round records.

## Connector move (one bounded proposal)

**Do not spend a C2 leg re-arbitrating grader ownership — it is frozen prior art. Instead, spend the attribution the province already mandates: land the stage-2 `round49_c2_verify.py`/probe with the two sibling citations PROVINCE :337-343 names, and use kumitate's `cap-run.mjs` form to close the sandbox limit R40 flagged.** Concretely: (1) cite `kumitate-shokunin` `cap-run.mjs --ro-bind / /` as the runner precedent rather than re-specifying caps — the r40 counter's writable-host-fs limit (`R40SentinelCounter` F1/F2, kengaku PROVINCE :464-466) is the same defect class the `22b7779e` revision hit under `RLIMIT_NPROC=48`; (2) keep the V14 mutation leg under tameshi's rule — mutants apply to **copies** of package bytes (`plans/mutants49/plan.json` semantics already frozen that way), never the gate in place. This improves coverage (the counter's sandbox and mutation legs stand on owned, cited ground) and harms no axis: tameshi's method and kumitate's runner stay theirs, cited not absorbed.

## Contradictions stated, not smoothed

- `plans/round-49-claims.md:3` records baseline lane tip `3a548330…` while the seat assignment names `9d2900af…` as the freeze/base. Observed: `9d2900af` exists, is the round-49 stage-1 commit, and `af88aab1` is current HEAD. Logged for L1 resolution; does not affect this ownership item.
- PROVINCE :351-356 is an r37 self-verification. This report re-ran the sweep today with the same zero-ownership result, but a PROVINCE file is a lane's own claim — a *negative* finding rests on sibling text as read, not on sibling assent in this round.
- `execution` boundary: kengaku owns offline/synthetic-fixture grader execution only. Running the real TB2 task image is recorded routed-not-absorbed (kengaku PROVINCE :285, r37 `R37DockerOracle`) — *no lane owns it*; C2 must not let probe scope creep into real-image execution.

## Limits

- PROVINCE.md files are gitignored (tool `glob`/`grep` skip them by default); sweeps above ran `gitignore: false` over `*/PROVINCE.md` and the named directories — fleet-root dotdirs (`.ufo`, `.jj`, `.scratch`, `.tower`) were not swept; they are process/state dirs, not lane provinces.
- Sibling `.ufo/` wave artifacts were classified as citations by reading each hit's context; I did not exhaustively re-derive each sibling's full wave history.
- No network source opened; no URL fetched this session. Located quotes above are verbatim from local files.

## Source log (path · accessed · ≤25-word located quote)

- `kengaku-shokunin/PROVINCE.md` @ `9d2900af…` (= worktree, sha256 `5e00336f…`) · 2026-10-28 · `:351 "kengaku keeps: which TB2 grader is captured, how it is called offline, what its verdict answers"` (14 words).
- `chousa-shokunin/PROVINCE.md` · 2026-10-28 · `:10-11 "Refuses: … model-quality or evaluation claims (→ kengaku)"` (8 words).
- `tameshi-shokunin/PROVINCE.md` · 2026-10-28 · `:14-17 "every lane's gate remains its own … Never edits a sibling's gate code"` (14 words).
- `kengaku-shokunin/plans/round-49-claims.md` · 2026-10-28 · `:108 "Counter python3 plans/round49_c2_verify.py --lane . (written in wave 1, pinned at stage 2)"` (12 words).

## Tooling

None installed or upgraded; no pacman transaction (host-wide pause honoured). `~/.omp/agent/RULES.md` read.

## Scratch

`/fast/scratch/hyaku/kengaku-r49/R49C2ConnPrior` — created, `TMPDIR` exported, removed before yield. No clone needed (all evidence via `git show`/`ls-tree`, read-only). Receipts cited from this report only; no scratch-resident evidence remains.

## VERDICT

`OWNERSHIP-FINDING: TB2 task-grader analysis/execution is owned by kengaku-shokunin itself (PROVINCE.md :3, :232-255, :351-356 @ freeze 9d2900af, sha256 5e00336f); zero sibling lanes own or claim it (21 PROVINCE files swept; all eval clauses defer to kengaku); r37 no-sibling-ownership verification re-run 2026-10-28 with same result (only data citations of kengaku artifacts). Scoped: offline/captured-grader analysis+execution only — real TB2 image execution remains unowned/routed. Proposed move: skip ownership arbitration; attribute runner (kumitate cap-run.mjs) and method (tameshi) per PROVINCE :337-343 and close the R40 F1/F2 sandbox limit in the stage-2 probe.`
