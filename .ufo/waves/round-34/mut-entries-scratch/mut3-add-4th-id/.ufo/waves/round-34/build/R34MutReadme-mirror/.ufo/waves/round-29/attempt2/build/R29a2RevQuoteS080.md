# R29a2RevQuoteS080 — independent re-grounding of S080 (Toolathlon) + task count

Seat: L1Kengaku29.R29a2RevQuoteS080 (reviewer, leaf). Date 2026-10-25.
Scope: (a) the 2026.06.30 Toolathlon-Verified news entry, verbatim, with its line number;
(b) `tasks/finalpool/ab-testing/task_config.json` keys `needed_mcp_servers` / `needed_local_tools`;
(c) my own count of directories under `tasks/finalpool` against the staged claim of 109.
Read-only over the lane; no production edit. Scratch: `/tmp/r29a2-RevQuoteS080/`.

## 0. What I fetched, and by which channel

| artifact | channel | bytes | sha256 |
|---|---|---|---|
| `README.md` @ `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` | `curl -fsSL https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe…/README.md` | 16,883 | `d06165b5ad28ff6f41160d2bb774de1174e583a2efdb3ba523ae1b4c76a5b46a` |
| same file, second channel | `git init` + `git fetch --depth 1 origin 9be8d8fe…` + `git checkout FETCH_HEAD`, then `sha256sum README.md` | 16,883 | `d06165b5…5b46a` (identical) |
| `tasks/finalpool/ab-testing/task_config.json` | `curl -fsSL …/9be8d8fe…/tasks/finalpool/ab-testing/task_config.json` | 227 | `0aa31c181ad711e85d229afc2a19e644525d8c1810cca098b8b85fad31c9a66a` |
| `tasks/finalpool` tree | GitHub tree API (`git/trees/0e6db218…`) **and** `git ls-tree HEAD:tasks/finalpool` | — | two channels agree |

The 16,883-byte figure also confirms the byte claim in `lanes/kengaku/SEARCH-LOG.md:57`
("README 16,883 B read") — PASS.

## 1. The 2026.06.30 entry — PASS (located, verbatim, line 27)

`README.md` has **339 lines** and exactly **one** occurrence of `2026.06.30`
(`grep -c '2026\.06\.30' README.md` → `1`; `grep -n` → `27:`).

Line 27 verbatim (identical from `sed -n '27p' README.md` and `git show HEAD:README.md | sed -n '27p'`;
line sha256 `504bfe369f756788fe2f4331a26455c860516784e165c195a6ccfaf0bb388bf1`):

```
[2026.06.30] 🎉 **Toolathlon-Verified** is released. This release marks the verified final version of Toolathlon, with task prompts, ground truths, and evaluators reviewed and aligned for the final benchmark release. We have also uploaded trajectories for 8 models to the [**Toolathlon-Verified** trajectories](https://huggingface.co/datasets/hkust-nlp/Toolathlon-Verified_Trajectories/tree/main) dataset on Hugging Face.
```

Note the emphasis markers `**…**` around the product name. They are part of the bytes and
matter at §2.

## 2. The staged quote — FAIL on "verbatim" (word count now compliant)

Contract being applied, read from the lane itself:
- `CORPUS.md` §SOURCES.md Rules 1 ("…the URL, the access date, and a ≤25-word quote with its
  location grounding `teaches`", file `/home/vgpnk/Projects/shokunin/CORPUS.md`);
- `corpus/evidence/round24-sources/gate.md:3` — "SOURCES-CONTRACT-v1 rule 1 requires each row's
  URL, access date, and a ≤25-word location-grounded quote", with the column header
  at that file's table spelled `quote (≤25 words, verbatim)`.

Three states of the S080 anchor quote were observed in this session; the tree moved under me
(siblings active — both statements below are timestamped):

**(a) As staged in the campaign package** — `merge/kengaku/SOURCES.append.md:10` and
`lanes/kengaku/SOURCES-PROPOSED.md:30` (read-only, outside the lane):

```
Toolathlon-Verified is released. This release marks the verified final version of Toolathlon, with task prompts, ground truths, and evaluators reviewed and aligned for the final benchmark release.
```

- word count, measured: **27** → exceeds the ≤25-word bound → FAIL;
- `q in readme` → **False**: the bytes are `…**Toolathlon-Verified** is released…`, so the
  quote is **not verbatim** → FAIL;
- location given as "README news entry dated 2026.06.30", no line number.

**(b) As first generated into this round's block** (`adopt-block.md`, mtime 03:44:59) — the same
27-word, emphasis-stripped quote, plus the stale count of §3.

**(c) Current state** (`adopt-block.md`, mtime 03:45:31) — a sibling rewrote it while I worked:

```
Toolathlon-Verified is released. This release marks the verified final version of Toolathlon
```

- word count **12** → within bound → PASS;
- `q in readme` → **False** (the source has `**Toolathlon-Verified** is released.`).
  `'**Toolathlon-Verified** is released. This release marks the verified final version of Toolathlon' in readme`
  → **True**, 12 words. → **still FAIL on verbatim**.

**Verdict §2: FAIL.** A reviewer running the contract's own verbatim check on the row that is
about to be appended gets a miss. The fix is one edit and costs no words: restore the two `**`
pairs in the quote cell. Nothing else in that cell needs to change.

The sibling quotes in the same anchor cell are fine: `needed_mcp_servers` and
`needed_local_tools` occur verbatim in `task_config.json` at lines 2 and 6, and
`108 task directories plus one task_conflict.json file` matches my count in §3.

## 3. Directory count — the staged "109 task dirs" is wrong; 108 is right

Measured three ways, all agreeing:

| method | result |
|---|---|
| `curl https://api.github.com/repos/hkust-nlp/Toolathlon/git/trees/0e6db218…` | 109 entries, `truncated: false`; **108 `tree`**, **1 `blob`** = `task_conflict.json` (`923bedda…`) |
| `git ls-tree -d --name-only HEAD:tasks/finalpool \| wc -l` | **108** |
| `git ls-tree --name-only HEAD:tasks/finalpool \| wc -l` | 109 |
| `find tasks/finalpool -mindepth 1 -maxdepth 1 -type d \| wc -l` | **108** |
| `ls -1 tasks/finalpool \| wc -l` | 109 |
| `grep -v '^040000' <<< "$(git ls-tree HEAD:tasks/finalpool)"` | `100644 blob 923bedda…	task_conflict.json` (the one non-directory) |

- **My count: 108 task directories.** **Delta from the staged 109: −1.**
- The 109 is the *entry* count, and it includes `task_conflict.json`, a run-config blob that is
  not a task. Every task directory does carry a `task_config.json` (checked `ab-testing`);
  `task_conflict.json` is not one.
- `README.md` states no numeric task count (`grep -n '109\|108\|number of tasks'` → no match), so
  the number is not a README claim that could back the staged wording.

**Verdict: the staged claim "109 task directories" FAILS.** Both lane-side artifacts have been
corrected since my first read, and both corrections match my measurement exactly:
- entry `corpus/knowledge/benchmark-task-validity-checklist.md:57-58` — "**109 entries under
  `tasks/finalpool`**, of which **108 are directories**" → PASS;
- `adopt-block.md` S080 anchor, current — "108 task directories plus one task_conflict.json file
  under tasks/finalpool (count re-derived 2026-10-25)" → PASS.

Paired cross-check, same rule, cheap to run and load-bearing in the same entry:
`git/trees/2fd12b88…` for `laude-institute/terminal-bench-2` → **92 root entries, 89 trees, 3
blobs** (`.gitignore`, `LICENSE`, `README.md`) — matches the entry's "92 root entries … leaving
89 task directories". PASS.

## 4. task_config.json keys — PASS, with line numbers

`tasks/finalpool/ab-testing/task_config.json` (227 B) parses; top-level keys are exactly
`needed_mcp_servers`, `needed_local_tools`, `meta`.

| required key | present | line | value |
|---|---|---|---|
| `needed_mcp_servers` | **yes** | 2 | `["google-cloud", "filesystem"]` |
| `needed_local_tools` | **yes** | 6 | `["claim_done", "python_execute", "handle_overlong_tool_outputs", "manage_context", "history"]` |
| `meta` (not required) | yes | 13 | `{}` |

Both required names also appear verbatim in the row's anchor as `"needed_mcp_servers"` /
`"needed_local_tools"`. **PASS.**

## 5. Findings, by severity

**F1 (blocking for C1's re-grounding duty) — the S080 quote is not verbatim.**
`adopt-block.md` S080 anchor cell, current state: `"Toolathlon-Verified is released. This release
marks the verified final version of Toolathlon"`; `in README.md` → `False`. The source bytes carry
`**Toolathlon-Verified**` (README.md line 27). Restoring the emphasis gives a 12-word verbatim
quote that still satisfies the ≤25-word bound — so the defect is pure transcription, and it is
the same emphasis-stripping that came in from the campaign package (§2a).

**F2 (blocking for C1, resolved mid-review — keep it resolved) — the stale count.**
`adopt-block.md` S080 at 03:44:59 carried "109 task directories under tasks/finalpool" while the
entry it is cited by already said 108 directories. `build_block()` cannot reconcile this: it
rewrites only `status`, `recheck`, `used-by` and a non-ISO `opened` (`plans/sources_adopt.py`
`build_block`), never `anchor`. So a corrected count in the entry does not propagate to the
registry row, and the registry is what the census and later rounds read. Current block is now 108
+ `task_conflict.json` — correct, but it was corrected by hand, not by the gate.

**F3 (C2 operability, for the GateAudit seat — cited, not adjudicated here) — the gate cannot see
either defect, and its normalization path is unreachable.**
`plans/sources_adopt.py` contains no quote, word-count or verbatim validation at all
(`grep -n 'quote\|verbatim\|word\|25' plans/sources_adopt.py` → matches only docstring prose and
fixture lines; `row_defects()` checks `status`, `recheck`, `source-empty` only). A 27-word,
emphasis-stripped quote passes the schema check. Separately, `check()` classifies any prose
`recheck` as a defect, so the prose→access-date normalization that C2 requires (duty 3) is
unreachable through the CLI. Observed read-only, this tree:

```
$ python3 plans/sources_adopt.py --registry corpus/SOURCES.md \
    --package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
registry=76 staged=173 collisions=0 malformed=2 duplicates=0 defects=171
  malformed: S093:escaped-pipe S101:escaped-pipe
  defect S077: recheck-prose
  … (169 more, including) defect S080: recheck-prose
EXIT=4
```
The same output is already on disk at `.ufo/waves/round-29/attempt2/package-gate.txt`
(`exit=4`). The round's staged package is therefore refused wholesale while the feature that is
supposed to absorb those cells (`build_block`'s normalization, exercised by selftest case d) sits
downstream of a hard exit. Note the two `escaped-pipe` refusals are correct refusals, not noise.

**F4 (minor, CORPUS.md "a count carries its command") — the entry gives a locator, not a command.**
`benchmark-task-validity-checklist.md:58` cites `contents/tasks/finalpool?ref=9be8d8f` for the
108/109 split. That is a location, not the command that produced the number. The command I used,
which anyone can re-run: `git ls-tree -d --name-only HEAD:tasks/finalpool | wc -l` after
`git fetch --depth 1 origin 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, and
`git ls-tree HEAD:tasks/finalpool | grep -v '^040000'` for the single blob. The entry's
"re-derived 2026-10-25" date is present, so only the command string is missing.

**F5 (minor, location precision) — the row carries no line number.**
CORPUS.md "A quote names its location" and Rules 1 both want a location; this package's own
attempt-1 Gate records quotes as "`…` — line 11, 4 words" (`corpus/lessons/round-29.md:40-46`),
and the entry's `source:` line 4 for S080 does say "`README.md` news line 27". The adopt-block
anchor says only "README news entry dated 2026.06.30". Adding "line 27" makes the row
self-locating, and this file has only one such entry (§1), so there is no ambiguity to resolve.

**F6 (precondition not yet met) — no attempt-2 Gate block exists.**
`corpus/lessons/round-29.md` is unmodified since 2026-10-21 15:16 and contains no "Attempt 2"
section (`grep -n 'Attempt 2'` → no match). C1's duty and CORPUS.md Rule 1 place the URL, access
date and ≤25-word located quote in the round lesson's §Gate. Until that block exists, S080's
re-grounding is recorded only in the row and the entry, not where the contract requires it. The
LessonDraft seat appears to own this; flagged, not actioned.

## 6. Residual risk and verification gaps

- **No LSP device on this seat.** `xd://lsp` → "No such tool"; the mounted tool list has no `lsp`,
  and no `lsp` binary is on PATH. Markdown/JSON byte checks are the right instrument for this
  scope (verbatim containment, key presence, tree counts), but every statement above is
  text/API-level only — there is no semantic-callers dimension for these file types. Recorded as
  unavailable rather than silently substituted.
- **The tree moved during review.** `adopt-block.md` was rewritten at 03:44:59 and again at
  03:45:31; the S080 row differs between the two (§2b vs §2c). F1 is asserted against the
  03:45:31 bytes and should be re-checked against the final commit, since a sibling may fix it.
- **Not verified here:** the S077/S078/S079/S090 quotes (separate seats), `sources_adopt.py
  --selftest` and the 10-case claim, `adoption_check.py` census output, and whether the lane's
  other existing gates still exit 0. My read-only gate run in F3 exercises `check()` only.
- **Not a finding:** the campaign-side files under `shokuknow` still carry the 27-word quote and
  "109 task directories". They are outside my write bound and the lane's entry explicitly
  documents the correction; the binding artifacts are the lane's entry and adopt-block, and both
  now carry 108.
- **Tooling:** nothing installed, nothing upgraded. Scratch is `/tmp/r29a2-RevQuoteS080/`
  (`README.md`, `task_config.json`, `clone/`, `dirs.txt`, `root_tree.json`). **No `.ufo/…/scratch`
  or round-35 path is cited anywhere in this report**, so the round-35 scratch relocation noticed
  by `L1Mado35.RevQuoteS210` (scratch → `scratch-evidence/`) and the checkpoint at `4efaf63`
  reported by `L1Mado35.RevEntryR15` do not touch it. Following the same principle — the report
  body is the durable evidence locus, scratch a convenience copy — every number above (hashes,
  byte counts, line numbers, exit codes, gate output) is inlined in the body, not referenced out.

## 7. One-line verdicts

| item | verdict |
|---|---|
| 2026.06.30 entry located & verbatim | **PASS** — `README.md` line 27 (of 339), sha256 `504bfe36…` |
| staged S080 quote | **FAIL** — not verbatim (`**` stripped); word count now 12, was 27 |
| `needed_mcp_servers` | **PASS** — line 2, `["google-cloud","filesystem"]` |
| `needed_local_tools` | **PASS** — line 6, 5 tools |
| `tasks/finalpool` directories | **108** — delta **−1** from the staged 109; the 109 counts `task_conflict.json` |
