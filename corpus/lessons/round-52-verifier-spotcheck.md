author: hyaku closure (non-author integrator, @m_zfl)

# Round 52 — non-author closure spot-check (kengaku)

Closure of lane-round kengaku 52 against lane tip `7a76a4bbfe6cc2a2f8dc9999f671a7645c6f2c2e` (base `30801b479e3418c11089b8586178b6960216f364`), 2026-10-28.
Driver digest (`.ufo/watchdog.log`): launch 16:09:50 attempt 1 → `lane-dead-no-report` 16:31:32; launch 16:31:35 attempt 2 → `lane-dead-no-report` 16:35:23;
launch 16:49:53 attempt 3 → `lane-dead-no-report` 17:25:36; launch 20:40:07 attempt 4 (`hyaku-inline`) → `complete` 21:21:17.

**Verdict: `rejected-honest-stop`, not admitted.** C1 fails its frozen literal predicate (the lane says so itself and does not claim the A5 reading); C2 verifies. Lane status `ok` (a real, committed, honest report).

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed in fleet repo by lane identity | `git log --format='%an %H' -- .ufo/reports/round-52/kengaku.md` | `kengaku-shokunin 024282e18ccfd13aae6d4b685dc32a031d041fe1` |
| SHONEN heading, one line per box | read report | `## SHONEN`, 4 lines, all `[~]` with pointers |
| cited lane commits ancestors of branch | `git merge-base --is-ancestor <h> master` for `1315234 07ea208 19bc16c 28c0018 bfbcb07 4343829 87301bac 43438294 30801b47 7a76a4bb` | all `ok` (branch `master` = `7a76a4b…`) |
| lane pushed | `jj-lane.sh state …` ; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0`; remote `7a76a4bbfe6cc2a2f8dc9999f671a7645c6f2c2e` |
| leftovers | `git status --porcelain` | one untracked file `.ufo/waves/round-52/w2/W2ScoutPriorArtFresh/receipts/fetch/tb2-paper-full.html` (>1 MiB seat fetch; the report discloses it). No tracked round work uncommitted. |
| prompt carries template contract | read `.ufo/prompts/kengaku-round-52.md` | §1–§6 present (claims, frontier step, L2 floor, report contract, commit scope, hyaku addendum) |
| waves | `w1-results.json`, `w2-results.json` | seats 35/35 and 33/33 returned (68 total, above the 64 floor) |

Defects (status-neutral): (a) the untracked >1 MiB receipt remains in the lane worktree (disclosed, not committed; should be deleted or excluded by a committed ignore rule); (b) `corpus/evidence/round52/confirmations.json` `source_file` fields are absolute `/home/vgpnk/...` paths into `.ufo/waves/` (resolve only on this host); (c) the fleet root carries untracked/added `.scratch/` and `lane3/` trees that are not round-52 lane work (reported by the lane, not attributable to it).

## 2. Per-claim re-check

Claim measurement basis: committed bytes at `7a76a4b` (`git archive` into a scratch dir; I did not run the lane's gates — PROTOCOL §Gate standard, Closure consequence — I verified their committed evidence and re-derived the numbers with my own plain measurements).

### R52-C1 — novelty 8→9 (TB2 grader-vacuity triage) — NOT VERIFIED (literal predicate fails)

- Evidence verified: `.ufo/waves/round-52/claims/c1-after.txt` (measured at `434382945c28…`, clean clone): `CAPTURES expected=184 present=183`, `classified=88` of 89, `CONFIRMED new=8`, `PRIOR-ART urls=14`, `PREDICATE R52-C1 fail`; selftest `c1-selftest.txt` `cases=6 failures=0`.
- Re-measured:
  - `git ls-tree -r --name-only 7a76a4b | grep -E '^corpus/evidence/round52/graders' | wc -l` → 185 = 183 captures + `EXCLUDED.md` + `SHA256SUMS`; `SHA256SUMS` has 184 lines; `grep -v sanitize-git-repo SHA256SUMS | sha256sum -c --quiet` → exit 0 (183/183 digests match); the one missing path `sanitize-git-repo/tests/test_outputs.py` carries the digest `57e4904…` in `EXCLUDED.md`. So CAPTURES 183/184 reproduces; the frozen kill rule (all 184) is failed by one operator-excluded file.
  - `plans/round52-tasks.json`: `task_count 89`, `capture_file_count 184`.
  - Independent `ast` pass over the 89 `tests/test_outputs.py` captures (my own classifier: a test function whose every `assert` tests only `exists/is_file/is_dir/isfile/isdir`): 305 test functions, 54 presence-only in 43 tasks — against the counter's 33 in 27 tasks and the lane's own AST figure 47. The three counts disagree, which confirms the lane's own finding that the instrument's per-test split is leaky (a confirmed weakness of the instrument, not hidden).
  - `confirmations.json`: 16 receipts over 8 tasks, every `quote` found verbatim in the committed capture (16/16, `grep`-style `in` test); tasks confirmed = bn-fit-modify, build-cython-ext, caffe-cifar-10, cancel-async-tasks, code-from-image, crack-7z-hash, extract-elf, financial-document-processor. Spot-read `crack-7z-hash`: `test_solution_file` is presence-only beside a real `test_solution_content` — the finding is a presence-only test inside a larger grader, exactly as the knowledge entry states (not a whole-grader vacuity).
- Ruling on the A5 question left to closure ("does a digest-pinned absence count?"): **no for the frozen predicate** — A5 is an additive line after the fact (A5 added after wave-2 showed the instrument misclassifies and is forgeable; `W2CritA1Amendment` found a swap passes it). The literal verdict stands: `fail`. Novelty stays 8 = `unchanged`.
- No exploratory claim.

### R52-C2 — operability 8→9 (gate-registry closure) — VERIFIED

- Evidence verified: `c2-after.txt` (measured at `434382945c28…`): `ADVERTISED 74`, `REGISTERED 74 rows=76`, `MISSING 0 INCOMPLETE 0 ENTRY-MISSING 0 SELFTEST-UNBACKED 0 DUPLICATE 0`, `PREDICATE R52-C2 pass`, exit 0; `c2-selftest.txt` `cases=3 failures=0`; `c2-before.txt` 72/44/28.
- Re-measured at `7a76a4b` with my own regex copy of the counter's `CMD` pattern over `SCORECARD.md SKILL.md LOG.md corpus/README.md corpus/knowledge/*.md`: 78 command-named scripts, of which 4 (`plans/round48_c1_verify.py`, `round48_c2_verify.py`, `round49_c1_verify.py`, `round49_c2_verify.py`) do not exist in the tree (the counter drops absent files) → 74 advertised existing; all 74 appear as an entry command inside the `## Gate/probe registry` block (0 missing); registry rows by name 75 backticked rows, 0 duplicate names. Reproduces 74/74/0.
- Row-truth spot checks (the counter cannot see a false cell; Q42): `routed-findings` row says `ROWS total=75 open=31 blocked=1 closed=41 refused=2` at `1315234` → `git show 1315234:corpus/routed-findings.jsonl | wc -l` = 75 and status counter {closed 41, open 31, refused 2, blocked 1} — **true**. `round51-routing` row says argparse-only exit 2, no setup exit: `plans/round51_routing.py` has `argparse` (line 226) and no `return 2`/`sys.exit(2)` — **consistent**. `gate-flip-check` appears once (stale duplicate removed). These confirm the repairs for those cells; the other repaired cells (`round46-c1`/`c3`, `round35-hardening`) were not re-executed by me (they need the lane's heavy gates) — evidence-verified only.
- Caveat for the verdict: the 8→9 bump rests on a counter that proves row existence/completeness/entry-script presence, not truth. The lane itself says so (Q42). Re-measured legs plus the spot checks above support `improved` (28 previously undiscoverable gates now discoverable; 7 false cells repaired) and no cell I opened was false.

### Axis verdicts

| axis | verdict | basis |
|---|---|---|
| novelty | unchanged (8) | C1 literal predicate fails; the SCORECARD agrees (novelty stays 8) |
| operability | improved (8→9) | C2 re-measured 74/74/0; row-truth spot checks true; counter-limited (Q42) |
| coverage | unchanged (7) | `git diff 30801b4 7a76a4b -- SCORECARD.md` adds only the round-52 section; cap by open L0 questions unchanged |
| calibration | unchanged (9) | the report declares the literal C1 fail and refuses the A5 reading; no score change claimed |
| depth | unchanged (9) | held (anti-double-count) |
| freshness | unchanged (9) | held |
| adjacency | unchanged (9) | held; `lane3/` at the fleet root is not lane work |

No axis harmed (`SCORECARD.md` diff is append-only, one new section; no prior row altered).

## 3. Discernment spot-check (LEARNING.md) — lesson `corpus/lessons/round-52.md` `## Gate`

All sources re-opened 2026-10-28 over HTTP (200), page text stripped of tags, lane quote searched verbatim.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S184 | admit, A | https://github.com/harbor-framework/terminal-bench-2/pull/53 | agree (caveat) | quote "Tests were updated when they over-specified or let any solution pass" found verbatim (11 words); maintainers' own change description of the 2.0→2.1 test edits, which bears directly on the claim. Tier A for an open PR body is generous — the lane flags it mutable. |
| S187 | admit, A | https://arxiv.org/html/2605.26079v2 | agree | "Our trajectory audit independently recovered 14 of these 21 issues under strict matching" found verbatim (13 words, as the lane counts). Independent audit of the same PR #53 fixes. |
| S190 | admit, A | https://arxiv.org/html/2601.11868 | agree | "A terminal bench task is considered well-specified if the unit tests will pass if and only if the container ends in an acceptable state." found verbatim in §2.3 "Specificity" (24 words ≤ 25). Authors' own bar. |
| S186 (new row, tier B) | admit, B | https://huggingface.co/datasets/zai-org/terminal-bench-2-verified | agree | "the test logic itself misjudged valid submissions or let non-compliant outputs through" found verbatim (12 words); correctly tiered B as third-party. Row carries page sha256 and located line. |
| S191 | reject | https://june.kim/terminal-bench-frame | agree | quote found ("On Terminal-Bench 2.1, 40 of 83 gold-passing tasks (48%) certify success after a careless deletion…"): measured on 2.1, not the 2.0 pin, and a different failure mode (destruction blindness); reject with committed flip condition is right. |
| S193 | reject | https://snorkel.ai/leaderboard/terminal-bench-2-1/ | agree | "A revision of Terminal-Bench 2.0 that fixes 28 of 89 tasks and introduces continuous validation for agentic benchmarks." found verbatim (18 words) — it restates the official notice rowed as S185 and adds no task-level grader evidence. |
| S185 (support) | admit, A | https://www.tbench.ai/news/terminal-bench-2-1 | agree | "Some tasks had instructions that were not aligned to their tests." found verbatim. |

New-row quote check: S186, S191, S193 rows read in `corpus/SOURCES.md` — each carries a ≤25-word located quote (12 / 15 / 18 words), fetch date 2026-10-28 and sha256.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → 15 pre-existing `W04` duplicate-url warnings, final line `kengaku ok …/corpus/SOURCES.md`, exit 0 (matches the report).

Disagreements: none on admit/reject direction.

## 4. Trend verdicts

- **expansion: improved.** One new knowledge entry (`corpus/knowledge/tb2-grader-vacuity-triage.md`) on ground the coverage map did not hold, citing mined rows S179–S190 (opened and quote-checked above for the sampled rows); 15 new SOURCES rows (census exit 0); 28 advertised gates now discoverable. Caveat: the entry's own claim is "not admitted" and says so; a capability row correctly did not enter the table.
- **quality: improved.** 7 false registry cells and a stale duplicate repaired; spot-read cells true; counter defects fixed before the scored after-run with dated amendments; Q42 added. Gap is recorded, not hidden: the C1 counter is forgeable and its per-test class leaky (my independent AST count 54 vs counter 33 vs lane AST 47).
- **discernment: improved.** The spot-check agrees with the gate on 3 admits + 1 tier-B admit and 2 rejects; the round reports the literal C1 fail rather than claiming A5; Q42 is grounded in the round lesson's `## Mistakes`.

## 5. Routed defects for the lane (next round)

1. **C1 instrument unsound** (lane already plans it for r53): per-test split disagrees with independent counts (33 / 47 / 54); predicate reachable without reading a grader (five routes, `W2CritC1Reach`); 0/16 mutants killed (`W2MutC1`). Fix under a frozen forged-complete control before any novelty claim; do not re-score A5 without a closure ruling (this closure: literal verdict governs).
2. Commit or delete the untracked `tb2-paper-full.html` (>1 MiB) so the worktree is clean at round close.
3. Replace absolute host paths in `confirmations.json` `source_file` with repo-relative paths.
4. Carried from the lane's own list: C2 `SELFTEST-UNBACKED` span-scoped negation fix; unfrozen controls K5/K7; prior-art pricing for the three unpriced confirmed tasks.

## 6. For the operator

SHONEN boxes 1–4 all `[~]` with pointers; box 1 (decision tables, error patterns, cited sources in `SKILL.md`), box 3 (executable re-run instructions in the knowledge entry) and box 4 (`PROVINCE.md` untouched) look checkable by a non-author from committed bytes; I did not edit `SHONEN.md` (promotion is operator-owned).
