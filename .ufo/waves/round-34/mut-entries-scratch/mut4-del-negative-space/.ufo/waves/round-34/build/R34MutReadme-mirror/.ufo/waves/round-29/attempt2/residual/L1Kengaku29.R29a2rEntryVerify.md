# R29a2 residual — entry-vs-registry verification seat

Seat: `L1Kengaku29.R29a2rEntryVerify` · date 2026-10-25 · lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`

Target as assigned: **`ff476d017107ec5ee3df735a16713c5967592b71`**, entry
`corpus/knowledge/benchmark-task-validity-checklist.md` (113 lines at that commit).
Rows to check: S077, S078, S079, S080, S091 — plus S090, which the entry's frontmatter actually cites.

**HEAD moved under this seat.** At first read `git rev-parse HEAD` = `ff476d0…`; by the end of the pass HEAD =
`5fd54a41c34f1275cf47d50bf1fbecde61c4e6ca`, i.e. four commits later:

```
$ git log --oneline -4
5fd54a4 round-29: land Q19 seat-yield criterion and the round-29 yield ledger
c88310f round-29: delete gate code proven behaviour-neutral by the simplifier
7bc2aaf round-29: label self-report sources, command every count, refresh adopted receipts
4b82ff7 round-29: remove entry widenings, tighten used-by and census gating, widen census row anchor
$ git diff --stat ff476d0 HEAD -- corpus/knowledge/benchmark-task-validity-checklist.md corpus/SOURCES.md
 .../knowledge/benchmark-task-validity-checklist.md | 42 ++++++++++++++++++-------
 1 file changed, 30 insertions(+), 12 deletions(-)
```

So every finding below is stated twice where the two states differ: **[ff476d0]** = the assigned landing commit,
**[HEAD 5fd54a4]** = the live repaired state (`git diff ff476d0 HEAD -- corpus/SOURCES.md` is empty: the registry
rows did not change; only the entry did).

## Implementation receipts (exact commands, exact results)

All fetches went to `/tmp/r29a2r-entryverify/`; nothing was written outside that directory and this report.

```
$ curl -sS -m 60 -o s077.md …/harbor-framework/terminal-bench/e67a2cb7…/docs/TASK_REVIEW_AUTOMATION.md   → 200 41842
$ curl -sS -m 60 -o s078.md …/scaleapi/SWE-bench_Pro-os/66f92766…/v2/README.md                          → 200 6858
$ curl -sS -m 60 -o s078gate.md …/scaleapi/SWE-bench_Pro-os/66f92766…/v2/GATE.md                        → 200 1659
$ curl -sS -m 60 -o s079.toml …/laude-institute/terminal-bench-2/2fd12b88…/protein-assembly/task.toml   → 200 973
$ curl -sS -m 60 -o s080.md …/hkust-nlp/Toolathlon/9be8d8fe…/README.md                                  → 200 16883
$ curl -sS -m 60 -o s080cfg.json …/hkust-nlp/Toolathlon/9be8d8fe…/tasks/finalpool/ab-testing/task_config.json → 200 227
$ curl -sS -m 60 -o s090.html https://www.tbench.ai/news/announcement-2-0                               → 200 53390
$ curl -sS -m 60 -o s091.html https://arxiv.org/abs/2507.02825                                          → 200 45559
$ curl -sS -m 40 -o s078sums  …/66f92766…/v2/SHA256SUMS   → 200 1176416 (6436 lines)
$ curl -sS -m 60 -o abc.html  https://arxiv.org/html/2507.02825  → 200 570890
$ curl -sS -m 60 -o tbpaper.html https://arxiv.org/html/2601.11868v1 → 200 1088268
$ curl -sS https://api.github.com/repos/…/git/trees/2fd12b8… → 403 {"message":"API rate limit exceeded …"}
```

Digests (`sha256sum … | cut -c1-16`) reproduce the lesson's pinned capture exactly, so no source drifted:

```
b0a7cb1495a08a44 s077.md      dde4168fed17ca1e s078.md    7c30b8d6aef5ea74 s078gate.md
d714960681ec921a s079.toml    d06165b5ad28ff6f s080.md    0aa31c181ad711e8 s080cfg.json
cbc50108ca8199f2 s090.html
```

Independent cross-check of those bytes against the publisher's own manifest — `v2/SHA256SUMS` at the pin contains
`dde4168fed17ca1ea00b26a93aca78dad43c7b3f981b93a2872428259428231f  README.md` and
`7c30b8d6aef5ea7413831ac5618220f8c01ff15439bc6732a25ceaeb2c401e71  GATE.md`, i.e. the files I tested are the
published files, not a mirror.

GitHub API was rate-limited, so the two count claims were re-derived from real tree objects instead of HTTP JSON:

```
$ git init -q tb2 && git remote add origin https://github.com/laude-institute/terminal-bench-2
$ git fetch -q --depth 1 origin 2fd12b88aafdd04a52c298e3940bcb189f9766d6      → FETCH_OK
$ git ls-tree 2fd12b8 | wc -l                        → 92      (89 040000 + 3 100644)
$ git ls-tree -r --name-only 2fd12b8 | grep -c 'task\.toml$' → 89
$ git init -q tool && git fetch -q --depth 1 origin 9be8d8f…                  → FETCH_OK
$ git ls-tree 9be8d8f tasks/finalpool/ | wc -l       → 109     (108 040000 + task_conflict.json)
```

## 1. Per-quote table

`bytesub` = the span, exactly as the entry prints it between quotation marks, occurs as a byte substring of the
fetched bytes (raw text for markdown/TOML/JSON, raw HTML for pages). Word counts use whitespace splitting.

| # | entry line [ff476d0] | quoted span (truncated) | cited source | bytesub | words | location |
|---|---|---|---|---|---|---|
| Q1 | 11–12 | "the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately" | README §Frontier | **YES** | 15 | `corpus/README.md` L270 |
| Q2 | 12–13 | "turned into a per-benchmark task-validity checklist" | README §Frontier | **YES** | 6 | `corpus/README.md` L270 |
| Q3 | 31 (axis D) | "in download-youtube YouTube's constantly changing anti-bot protections meant that a solution that worked one day might not work the next." | S090 | **NO** (raw HTML) | 20 | rendered-text only; unprefixed 18-word form is byte-verbatim at **offset 48597** |
| Q4 | 32 (axis E) | "The verifier never runs in the agent's sandbox." | S078 | **YES** | 8 | `v2/README.md` L75 |
| Q5 | 32 (axis E) | "hidden-test paths are restored or removed before the test patch is applied" | S078 | **YES** | 12 | `v2/README.md` L103 |
| Q6 | 30 (axis C) | "Doing nothing fails tests" | S077 | **YES** | 4 | L29 (`Nop Validation` row) |
| Q7 | 33 (axis F) | "Adversarial reward-hack detection" | S077 | **YES** | 3 | L31 (`Cheat Trials` row; `/cheat` on the same line) |
| Q8 | 34 (axis G) | "Prevents training data contamination by ensuring a unique canary string is present in task files." | S077 | **YES** | 15 | L95 (`#### check-canary`) |
| Q9 | 47 (adjudication) | "The LLM-based analysis determines whether actual hacking occurred." | S077 | **YES** | 8 | L301 |
| Q10 | 42 (gate oracle) | "**642 / 642** tasks resolved" | S078 GATE | **YES** | 5 | `v2/GATE.md` L7 (= `v2/README.md` L92) |
| Q11 | 42–43 (gate nop) | "**642 / 642** tasks unresolved (0 spurious passes)" | S078 GATE | **YES** | 8 | `v2/GATE.md` L8 (= `v2/README.md` L93) |
| Q12 | 90–91 (§Prior art) | "we introduce the Agentic Benchmark Checklist (ABC), a set of guidelines that we synthesized from our benchmark-building experience" | S091 | **YES** | 18 | arXiv abs raw HTML **offset 3179** (v5 abstract) |
| Q13 | 73–74 (§Counts) | "92 top-level task directories" / "109 task directories" | staged package | **YES** / **YES** | 4 / 3 | `corpus/evidence/round29-attempt2/adopted-block.md` L3, L4 |

Inline code spans (identifiers, not quotations) were checked the same way and are byte-exact:
`schema_version = "1.1"` (S079 L1), `difficulty = "hard"` (L15), `expert_time_estimate_min = 60.0` (L18),
`junior_time_estimate_min = 300.0` (L19), `timeout_sec = 1800.0` (L22); `needed_mcp_servers` (task_config L2) and
`needed_local_tools` (L6). The entry's "lines 2-12" range and README "line 27" are exact
(`This release marks the verified final version of Toolathlon` at L27). The scare quotes at L15–16
("what a validity question is", "the artefact that answers it…") and at L63 ("verifier isolated") attribute nothing
and were not tested.

**Result: 13 of 14 quoted spans are byte-verbatim and ≤25 words.** The single failure is Q3, and it fails only
because the entry moved the task slug inside the quotation marks: at the pinned bytes the sentence reads
`For example, in <code>download-youtube</code> YouTube&#x27;s constantly changing …`, so the entry's 20-word form
exists in no byte string (it is correct in rendered text). The row's own 18-word anchor is byte-verbatim.

## 2. Structural checks

| check | verdict | evidence |
|---|---|---|
| every `source:` id has a registry row | **PASS** (5/5) | frontmatter ids S077,S078,S079,S080,S090 → `corpus/SOURCES.md` L100, L101, L102, L103, L104 |
| each row's `used-by` names this entry | **PASS for S077–S080, S090; FAIL for S091** | rows L100–L104: `used-by=corpus/knowledge/benchmark-task-validity-checklist.md`. S091 (L106): `used-by=corpus/lessons/round-29.md` — the entry's §Prior art L95 calls S091 "the pricing row" and quotes it at L90–91, so the reverse index misses its only citing entry |
| each row's `recheck` is a cadence or future date, not the access date | **PASS** (6/6) | S077–S080, S090, S091 all `recheck=180d` with `opened=2026-10-25`; `date -d '2026-10-25 +180 days'` → `2027-04-23`, matching the entry's `next due 2027-04-23` (L7) |
| §Prior art correctly attributes S091 | **PARTIAL** | see §3 |

Also verified, because the entry asserts them: `recheck` cadence and the due date agree; S090 is cited as
"page as served 2026-10-25" and its digest still matches that capture; all five frontmatter rows are tier A
(`tier=A`), consistent with Q2.

## 3. §Prior art (entry L88–96) — element by element

| element | verdict | evidence |
|---|---|---|
| quote verbatim, 18 words | **PASS** | Q12; abs HTML offset 3179 |
| "Task Validity criterion is the same construct" | **PASS** | ABC §4.1 "Assessing Task Validity"; §3 defines task validity as "a task should be solvable if and only if the agent possesses the target capability" |
| INCREMENTAL pricing (no novelty credit) | **PASS** | consistent with S091's row `teaches` ("prior art, not a new instrument") and lesson §Attempt 2 "priced the entry **INCREMENTAL**" |
| "ABC's items cover axes B, C, D, E, F, G and I at item level" | **PARTIAL** | item inventory from §4 + Appendix D (T.1–T.10, O.a–O.h, R.1–R.9): B ← T.7/T.8 (ground-truth correctness) + T.9 (oracle solver); D ← T.6 ("environment setup should be fully reproducible and frozen"); E ← T.5 ("fully isolate agents from the ground truth results"); I ← T.1–T.3 (tool/package versions, API availability) + O.g.1–O.g.3 (state matching). **C** has no empty/no-op-submission item (nearest: T.10 pilot outliers, O.b.2/O.b.3 "prevent success by listing all possible answers or guessing"); **F** has no adversarial cheat-trial item (nearest: T.5 isolation, T.3 interrupt detection); **G** is a *benchmark-reporting* item R.3/R.4 ("measures to prevent data contamination", "plans to consistently update tasks"), not a per-task canary |
| "the benchmark this entry's S077 comes from applies ABC to itself" | **FAIL — wrong pointer** | `grep -ic 'ABC' s077.md` → **0** (`Agentic Benchmark Checklist`, `ABC`, `arxiv` all absent); `git grep -l -i 'Agentic Benchmark Checklist' 2fd12b8` → none. The claim is true of a *different* document: the Terminal-Bench paper, arXiv 2601.11868, Appendix B.5 — "We applied the Agentic Benchmark Checklist (ABC) ( Zhu et al., 2025 ) to further troubleshoot and demonstrate the evaluation rigor." That paper is registry row **S020** (`queued`, `used-by —`), cited nowhere in the entry |
| "Zhu et al., NeurIPS 2025" | **UNVERIFIABLE at the anchor** | arXiv abs page for 2507.02825 has an empty `Comments:` field and **zero** occurrences of `NeurIPS` (the only NeurIPS text is the paper's own template appendix "G NeurIPS Paper Checklist"); v5 is dated 07 Aug 2025 |
| "the located quote, anchor and rejection reasoning live in `corpus/lessons/round-29.md` §Attempt 2" | **PASS on location, loose on wording** | lesson L150 "## Attempt 2"; its "Sources opened this round" table row S091 carries the quote, 18 words, "Abstract". But S091's row status is `mined`, and the only rejected thing nearby is the campaign register's `payload-absent` verdict (lesson M96) — "rejection reasoning" invites the misread that S091 was rejected |

## 4. Numbers the entry claims (§Counts, L70–77) — re-derived independently

| claim | verdict | evidence |
|---|---|---|
| 92 root entries, 3 files (.gitignore, LICENSE, README.md), 89 dirs, 89 task.toml | **EXACT** | `git ls-tree 2fd12b8 \| wc -l` = 92; blobs = 3 with exactly those names; `grep -c 'task\.toml$'` = 89 |
| 109 entries under tasks/finalpool, 108 dirs, 1 file (`task_conflict.json`) | **EXACT** | `git ls-tree 9be8d8f tasks/finalpool/ \| wc -l` = 109; blobs = 1 (`tasks/finalpool/task_conflict.json`) |
| 1 of 89 task dirs carries schema_version+difficulty but neither time baseline = `caffe-cifar-10` | **EXACT** | scan of all 89 blobs: `no expert=1 no junior=1 no both=1` → `caffe-cifar-10/task.toml`; `no schema_version=0 no difficulty=0` |
| [ff476d0] "6 lines across 3 tasks write integer literals (`30`)" | **count right, value partly wrong** | 6 lines / 3 tasks ✓ — `count-dataset-tokens` L18–19, `reshard-c4-data` L18–19, `train-fasttext` L18–19; but only 3 of the 6 are `30`, the juniors are `60`, `90`, `120`. **Repaired at HEAD**: that sentence is replaced by a deferral to `R29a2RevQuoteS079.md` F4 with no count claimed |
| "both counts correct the staged package" | **PASS** | both phrases are byte-present in the committed receipt `corpus/evidence/round29-attempt2/adopted-block.md` L3 and L4 |

## Findings by severity

**F1 — MEDIUM — §Prior art attributes the ABC self-application to the wrong document.**
Entry L92: *"the benchmark this entry's S077 comes from applies ABC to itself."* S077 never mentions ABC
(`grep -ic 'ABC' s077.md` → 0) and the pinned TB2 repo never mentions it (`git grep` → none). The sentence is true
only of Terminal-Bench's paper §B.5 (arXiv 2601.11868), which is registry row S020, status `queued`, `used-by —`.
The claim therefore rests on an uncited, unmined row while naming a row that does not contain it (Q2/Q3).
Fix: cite S020 with the B.5 quote (and move the row off `queued`, or accept it as prior-art-only and keep it
unmined), or delete the clause. **Persists at HEAD.**

**F2 — MEDIUM-LOW — axis D quotes a non-byte-verbatim span and gives no location.**
Entry L31 prints *"in download-youtube YouTube's changing …"* inside the quotation marks; the pinned bytes put
`download-youtube` inside a `<code>` element (`… in <code>download-youtube</code> YouTube&#x27;s constantly …`), so
the 20-word form matches rendered text only. S090's own anchor quotes the 18-word form, which *is* byte-verbatim
(offset 48597). Axis D also omits a location while axes E quote with `(line 75)` / `(line 103)` — Q3 wants
"≤25 words, with location". Fix: move `in download-youtube` outside the quotes and add the offset/line.
**Persists at HEAD (L37).**

**F3 — MEDIUM-LOW — S090 is asked to support a claim it does not make.**
Entry L58: *"S090 is the one axis-B/C-passing task that still failed after publication."* S090 says only
*"we weren't satisfied with the level of verification in the original dataset. Our community discovered several
problems with tasks from 1.0."* It never states that `download-youtube` passed oracle/nop validation before
publication, so "axis-B/C-passing" is added by the entry, not narrowed from the quote (Q3). Fix: drop the
"B/C-passing" predicate or cite the document that shows pre-publication validation for that task.
**Persists at HEAD (L66).**

**F4 — MEDIUM-LOW — S091 is body-cited but has no `source:` line, and its `used-by` omits the entry.**
Frontmatter (L1–5) declares five rows; §Prior art (L90–95) names and quotes a sixth, calls it "the pricing row",
and defers its anchor and word count to `corpus/lessons/round-29.md`. Row S091's `used-by` is
`corpus/lessons/round-29.md`, so the registry's reverse index does not lead a reader back to the only entry that
quotes it, and the entry's `recheck:` list (L7) omits S091, so the quote would never be re-fetched. **Persists at
HEAD** (`git diff ff476d0 HEAD -- corpus/SOURCES.md` empty).

**F5 — LOW — "NeurIPS 2025" is unverifiable at S091's anchor.** The abs page has an empty Comments field and no
`NeurIPS` string. The entry inherits the row's phrasing; either verify the venue elsewhere or write
"arXiv 2507.02825 (Zhu et al.)". **Persists at HEAD.**

**F6 — LOW — coverage claim is broader than ABC's items for C, F and G.** "ABC's items cover axes B, C, D, E, F, G
and I at item level" (L92–93) is clean for B (T.7–T.9), D (T.6), E (T.5), I (T.1–T.3, O.g.1–3) but ABC has no
empty-submission item (C), no adversarial cheat-trial item (F), and a benchmark-reporting contamination item
(R.3/R.4) rather than a per-task canary (G). Fix: state the three as "related items exist in weaker form" rather
than "cover". **Persists at HEAD.**

**F7 — LOW — [ff476d0 only] integer-literal count miscites its own value.** "6 lines across 3 tasks write integer
literals (`30`)" is 6/3 exactly, but the six values are 30, 30, 30, 60, 90, 120. Already repaired at HEAD (the
count is now deferred to the reviewer seat's artifact). No action on the surviving text.

**F8 — NIT — "rejection reasoning" for a `mined` row.** S091 is `mined`; the rejected item is the campaign
register's `payload-absent` verdict (lesson M96). Reword as "the register-verdict reversal and pricing reasoning".

**F9 — LOW-MEDIUM — [HEAD 5fd54a4 only] the new canary sentence understates the tree and can be misread.**
HEAD's new bullet says *"Applied to the pinned Terminal-Bench 2.0 tree, Harbor's literal `harbor-canary` string
occurs in 0 of its files"*. True: `git grep -l 'harbor-canary' 2fd12b8 | wc -l` → **0** (of 1038 files). But the
tree is canaried under a different literal: `git grep -l 'terminal-bench-canary' 2fd12b8 | wc -l` → **275 files
across 88 of 89 task dirs** (only `headless-terminal` has none), 278 lines, GUID `26b5c67b-…` present in 279
files. Since S077 L95 shows `check-canary` hunting the *exact* string `harbor-canary GUID 26b5c67b-…`, the honest
and stronger statement is: the published tree carries `terminal-bench-canary GUID …`, so the documented check
literal would not match it, and 1 of 89 task dirs carries no canary at all. As written, a reader can conclude the
tree has no canary. Fix: state both counts and the prefix mismatch, and name `headless-terminal` as the gap
(axis G is exactly the axis this is evidence about).

## Residual risk and verification gaps

- **HEAD drift is the main residual risk.** Findings F1, F2, F3, F4, F5, F6 all survive in the live entry at
  `5fd54a4`; F7 is repaired; F9 is new text. A verdict taken against `ff476d0` alone would miss F9, and a verdict
  taken against HEAD alone would report F7 as live. Both states are recorded above.
- **GitHub API quota** (403, `API rate limit exceeded`) meant the entry's own `curl …/git/trees/…` and
  `curl …/contents/…` commands could not be executed literally. The counts were re-derived from the same commit
  objects via `git fetch --depth 1` + `git ls-tree`, which is equivalent for the unit question but is not a re-run
  of the entry's printed commands. `curl -s https://api.github.com/…` remains unverified as typed (its shape is
  correct; its output is not reproduced here).
- **ABC item text** was read from the arXiv HTML with whitespace collapsed (`/tmp/r29a2r-entryverify/abc.txt`), so
  the item quotes cited under F6 are rendered-text, not byte-verified against `abc.html`.
- The §Prior art quote was checked against the abs page only (the row's anchor). The paper body's own abstract
  repetition was not compared.
- I did not verify the README §Frontier "Partly discharged round 29 attempt 2" annotation beyond the two quoted
  fragments, nor the round-29 lesson's claim set beyond the S091 row it carries.
- Nothing was installed or updated in this seat; no package manager was invoked.
