# W2ScribeSourcesRows — kengaku round 52, wave 2 (falsify), scribe seat

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, base tip `30801b479e3418c11089b8586178b6960216f364`, measured 2026-10-28.
Leaf seat, no subagent dispatch, no lane-tree / git / jj mutation. Scratch dir was used under
`/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeSourcesRows/` and removed before yield; receipts kept in `receipts/` beside this file.

## 1. Result in one paragraph

Drafted **15 SOURCES rows, S179–S193**: 12 `mined` rows (the pinned-tree population, the TB2.0 README at the pin,
the three named graders, and the prior-art primaries the scout fetched that I re-opened) and 3 `rejected` rows (kept as taste evidence).
Every row was re-opened by this seat on 2026-10-28, every quote was checked as a verbatim substring of the fetched bytes, and every
`mined` row names exactly `corpus/knowledge/tb2-grader-vacuity-triage.md` in `used-by`. The draft inserts cleanly into a scratch copy of the
registry: `validate` exits 0 with no E-codes. Red controls behave as the census should. One caveat: the knowledge entry does not exist yet, so
E11 fires on the 12 `mined` rows until the L1 writes it. Separately, I attacked the frozen per-test classifier (C1 / Amendment A1) while
checking my hand reads, and two of its defects land (section 5). I did **not** attack R52-C2 (the 28 gate rows); that is outside this item.

## 2. Deliverables (absolute paths)

- Draft rows (registry-table form, Gate block, refusals, fetch receipts):
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeSourcesRows/sources-rows.md`
  (the scratch original was `/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeSourcesRows/sources-rows.md`; it was removed with the scratch dir after the copy)
- Receipts: `…/w2/W2ScribeSourcesRows/receipts/` — `sources-rows.md`, `extract_verify.py` + `verify-receipt.txt` (quote check),
  `classifier-receipt.txt` (frozen classifier on the three graders), `receipt-A-validate.txt`, `receipt-A-census.txt`
  (positive census on the scratch registry with the rows inserted), `receipt-R1-e11.txt`, `receipt-R2-e12.txt` (red controls).
- This report also copied to `…/w2/W2ScribeSourcesRows.md`.

## 3. Proposed ids

| id | source | kind | tier | status | used-by |
|---|---|---|---|---|---|
| S179 | TB2.0 pinned tree, grader-file population (git trees API) | dataset | A | mined | knowledge entry |
| S180 | TB2.0 root README at pin `2fd12b88…` | docs | A | mined | knowledge entry |
| S181 | bn-fit-modify grader | code | A | mined | knowledge entry |
| S182 | pytorch-model-recovery grader | code | A | mined | knowledge entry |
| S183 | torch-tensor-parallelism grader | code | A | mined | knowledge entry |
| S184 | TB2 pull #53 "Terminal-Bench 2.1" (open, "not for merging"), PR body | docs | A | mined | knowledge entry |
| S185 | tbench.ai Terminal-Bench 2.1 announcement | docs | A | mined | knowledge entry |
| S186 | zai-org terminal-bench-2-verified dataset card (2026.08.18 update) | dataset | B | mined | knowledge entry |
| S187 | ABA auditor paper, arXiv:2605.26079v2 (PR #53 comparison) | paper | A | mined | knowledge entry |
| S188 | SWE-bench "Solved Issues" weak-oracle study, arXiv:2503.15223 | paper | A | mined | knowledge entry |
| S189 | tsDetect test-smell catalogue, FSE 2020 PDF, Table 1 | paper | A | mined | knowledge entry |
| S190 | TB2 paper arXiv:2601.11868 §2.3 "Specificity" (HTML anchor) | paper | A | mined | knowledge entry |
| S191 | June Kim blog, TB2.1 probe figure | community | C | rejected | — |
| S192 | harbor-framework/terminal-bench issue #1387 (legacy repo) | community | C | rejected | — |
| S193 | Snorkel AI TB2.1 leaderboard page | docs | C | rejected | — |

Registry state measured before insert: 171 rows, last id S178, next unused S179. Insert point: after the S178 row, inside `## Registry`.

## 4. Commands run and measured numbers

Registry baseline (lane tree, read-only):
```
./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku   -> rc 0, 15 W04, 0 E
./scripts/sources-census.sh census   --root /home/vgpnk/Projects/shokunin kengaku   -> rows 171, tier A147 B22 C2, mined 155 queued 8 rejected 8
```

Fetches (`curl -sS -L`, all HTTP 200): pinned tree API (372898 B), README (4574 B), the three graders (5892 / 5591 / 7171 B),
PR #53 API (28522 B), tbench.ai (148013 B), HF card (147928 B), arXiv 2605.26079v2 HTML (694146 B), arXiv 2503.15223 abs (45536 B),
arXiv 2601.11868 HTML (1088268 B), tsDetect PDF (562193 B), june.kim (50673 B), GitHub issue #1387 (1165626 B), snorkel (479156 B).
Per-file sha256 values are in the draft's "Fetch receipts" table (full 64-hex).

Quote and anchor verification: `python3 extract_verify.py` → 15/15 quotes found in the fetched bytes, `ALL-FOUND`
(receipt `receipts/verify-receipt.txt`). Line numbers are of a deterministic renderer in that script (HTML tags stripped, blank lines
dropped); for the three graders and README they are the raw file lines.

Git blob check: `sha1("blob <bytes>\0" + content)` for README and the three graders equals the tree's blob shas
(`a46b155b…`, `978406ce…`, `2dc618ea…`, `6ac3c4b1…`). Captured-grader cross-check: the three grader fetches are byte-identical to the
`corpus/evidence/round52/graders/SHA256SUMS` lines (364069f8…, 5d4d57c4…, 4ae4285e…).

Population composition, counted from the pinned tree: 1446 entries, 1038 blobs, 89 top-level task dirs;
`tests/test_outputs.py` = 94 (5 of them under `environment/tests/`), `tests/test.sh` = 89, `tests/verify.sh` = 1; total 184.

Census on a scratch copy (`receipts/`):
```
scripts/sources-census.sh validate --root <scratch> <scratch>/kengaku-shokunin   -> rc 0; E-codes 0; W04 still 15
census: rows 186 (+15), tier A 158, B 23, C 5, mined 167, queued 8, rejected 11
```
Each new row has NF=13 (11 logical cells).
Red controls: (R1) knowledge entry removed → `E11` for S179–S190, rc 1 (12 findings); (R2) a row copied after `## Paths` → `E12 S199 row outside Registry section`, rc 1.

Attack on the frozen classifier: `classify_tests` (plans/round52_c1_grader_audit.py, copied to scratch, not run against the lane)
on the three graders → see section 5.

## 5. Findings (scoped; the L1 decides)

**F1 — presence-only tests in two of the three named graders are misclassified by the frozen per-test rule (A1). The attack lands.**
Output of `classify_tests` on the captured bytes (receipt `classifier-receipt.txt`):

| grader | test | hand read | frozen per-test class | cause |
|---|---|---|---|---|
| bn-fit-modify | test_bn_sample_exists, test_learned_dag_structure_exists, test_intervened_dag_structure_exists | presence-only (lines 13-17, 20-24, 58-62) | P1 ×3 | — agrees |
| pytorch-model-recovery | test_model_file_exists (103-108) | presence-only | **P3** | `VALUE` contains `\bin\b`, which matches the English word "in" in the comment "operated in (the WORKDIR …)" inside the block; comments are not stripped |
| torch-tensor-parallelism | test_parallel_linear_exists (18-25) | presence-only | **P2** | the block runs from line 18 to line 186: `split_tests` ends a block only at the next `test_` def, so the helper defs `_setup_process_group` / `_cleanup_process_group` (`dist.`) are absorbed and `BEHAV_T` matches `dist.` |

Consequence: under the frozen rule only bn-fit-modify has P1 tests among the three hand-read graders; the other two presence-only tests
are not vacuity candidates. The amendment's own claim ("mechanical split of the frozen vocabulary") does not hold on these two files. Scope
of the check: three files, not the population. Also checked, agreeing with the hand read: `test_weights_file_unchanged` (pytorch) is P3 (its
`torch.allclose` is a real value check), and both `test_column_/row_parallel_linear` are P0 (behaviour through `mp.spawn` with no value
marker in the block).
Impact on the rows: S182 and S183 say what the test asserts (hand read, correct); their teaches do **not** claim the counter flags them. The
knowledge entry must not cite the counter for those two presence tests.

**F2 — the pinned-tree document digest is not stable across fetches; blob shas are.** My fetch is 372898 B, sha256 22f26aa9…; the wave-1
scribe's fetch (`C1ScribeSources/report.md`) recorded 453523 B, sha256 b5d86dfe…. Both list 1446 entries. I did not reproduce the wave-1
bytes and do not know the cause. The four blob shas I checked (README, three graders) agree with my tree, so S179 anchors on the pin and the blob
shas, not on the document digest.

**F3 — prior-art quotes from wave 1 re-verify.** All 10 quoted primaries of `C1ScoutPriorArt` (PR #53, tbench.ai, HF card, arXiv 2605.26079,
2503.15223, 2601.11868, tsDetect PDF, june.kim, snorkel, #1387) re-verify as verbatim substrings of my own fresh bytes. Line numbers differ
from the scout's because the renderers differ; the rows state the renderer. The scout's june.kim quote ("On Terminal-Bench 2.1, 40 of 83
gold-passing tasks (48%) certify success after a careless deletion") is a substring of line 9 of the fetched page.

**F4 — the phenomenon-new question, from the rows (reading, not a score).** No fetched primary in these rows names the per-test presence-only
class (P1). The nearest items are: the maintainers' own categories "tests … over-specified or let any solution pass" (S184, PR #53, body
line 8); the official "instructions not aligned to their tests" (S185); the HF card's named false-fail/false-pass tasks (S186); the ABA
auditor's 14-of-21 strict recovery against PR #53 (S187); SWE-bench weak oracles (S188); and tsDetect's Resource Optimism, which is the
opposite flag (S189). So "whole-benchmark grader defect triage" is phenomenon-known at family level (maintainers and reviewers already
name these defects for this pin), and the presence-only per-test class is not named in any row. That is a reading for the critic and
the prior-art seat, not a verdict.

**F5 — PR #53 is an open, unmerged "not for merging" demonstration, not a merged 2.0 fix.** Its body says "THIS PR IS TO DEMONSTRATE THE DIFF
AND COMMUNITY DISCUSSION (not for merging)" (line 2). S184 carries recheck 30d for that reason.

**F6 — S190 is a new row, not an in-place change to S020.** S020 (queued) cites the abs page and the Abstract. S190 cites the HTML URL and
§2.3 "Specificity", a different anchor, so it cannot be an in-place status change. The S190 claim that "a presence-only test passes on container
states outside that bar" is an inference from the paper's if-and-only-if wording, not a quote; the row teaches state it as a consequence.

**F7 — knowledge entry dependency.** Every `mined` row names `corpus/knowledge/tb2-grader-vacuity-triage.md`, which is not on disk yet
(`ls corpus/knowledge | grep tb2-grader` shows only the 12 hand-read entries). E11 fails until the L1 writes it. The entry must carry
`source:`, `verified-at:` and `recheck:` and cite the S-ids it uses.

**F8 — id collision risk.** S179–S193 are proposed from the registry as it stood at 30801b47 (last S178). Another round-52 seat drafting rows
(W2ScribeGateBlock) could claim the same ids. I did not message that seat; the L1 must reconcile ids at insert time (the census catches duplicates
as E03).

**F9 — refused / not rowed.** Refused as rows (kept as `rejected`): June Kim blog (2.1 scope, S191), issue #1387 (legacy repo, S192), snorkel
(duplicates S185, S193). Not rowed: OpenReview "Benchmarks as Software" (challenge pages only, never opened; a row-shaped line for it outside
Registry would fire E12), the Lacuna summary (not quoted by the scout; a summary of the unread paper), the GitHub issue API for #1387 and
openai.com (403; S006 already covers the OpenAI post). S115 already holds the build-pmars grader, byte-identical, so no new row for it.

## 6. Tooling

No tool installed, upgraded or removed. No pacman, no `uv tool install`. Used `curl`, `python3`, `pdftotext`, `jq` and `gawk` as already present.

## 7. Scope honesty

- Attack on C2 (the 28 gate rows) was not part of this item and was not run.
- The per-test classifier attack (F1) is checked on three files only.
- The S-rows are a draft: nothing was copied into the lane tree, `corpus/SOURCES.md` is unchanged, no knowledge entry was written.
- Scratch dir removed after copying the draft and receipts into this report directory.
