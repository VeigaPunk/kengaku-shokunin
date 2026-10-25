# R31EntryScope — scope and admission-bar fit of the staged `benchmark-verifier-execution-model.md`

Seat: leaf, read-only. Round 31 (hyaku run 6, 2026-10-25). Lane tip at start `0883e72`.
Nothing under the lane repo was created or modified except this file. Scratch: `/tmp/r31-entryscope/` (3 files, 944 KB — `du -sh`; `tasks.json` 956505 B is the 642-entry listing).
Tooling: none installed or upgraded this seat; `pacman` untouched.

**Question assigned:** (a) which PROVINCE surface the entry lands on and whether any sibling lane owns
harness runtime / verifier ground; (b) Q1–Q19 row verdicts with the bar quoted; (c) is the entry's ground
already held by the coverage map; (d) the entry's own overclaims, located by line.

---

## 0. Evidence actually fetched or run

Lane facts (commands run in `/home/vgpnk/Projects/shokunin/kengaku-shokunin`):

| command | result |
|---|---|
| `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` | `88` |
| `grep -nE '^\| *S09[23] *\||^\| *S100 *\|' corpus/SOURCES.md` | no output, **exit 1** — S092, S093, S100 are **absent** from the registry |
| `grep -rn 'partly observable' corpus/` | **0 hits** |
| `grep -inE 'falsif' corpus/knowledge/*.md` | hits incl. `benchmark-task-validity-checklist.md:137` `**Falsifier.**`, `contamination-transparency-card.md:138` `**Falsifier:**` |
| `grep -l '^writer:' corpus/knowledge/*.md` | 5 files (`contamination-transparency-card.md`, `extraction-policy-comparison.md`, `grader-perturbation-audit.md`, `webarena-config-projection.md`, `webarena-task-spec-audit.md`) — the staged entry is **not** among them |
| blank-first-line census over `corpus/knowledge/*.md` | **0** files start with a blank line; the staged entry does (line 1) |
| `test -e .ufo/waves/yield.tsv` | present (Q19's instrument exists) |

Source bytes opened at the pinned commits (network, `/tmp/r31-entryscope/`):

1. `https://raw.githubusercontent.com/laude-institute/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/task.toml`
   — 973 bytes. Line 21-22 `[verifier]` / `timeout_sec = 1800.0`; line 34 `allow_internet = true` under
   `[environment]` (line 27); line 37 `[verifier.env]` present and empty; **no** `environment_mode`, **no**
   `[verifier.environment]`.
2. `https://api.github.com/repos/scaleapi/SWE-bench_Pro-os/contents/v2/tasks?ref=66f92766bba642462d4bbe5479e83f91f9211862`
   — one call, returns a list of **642** task directories.
3. `…/v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/task.toml`
   — 889 bytes. Line 18-21 `[verifier]` / `network_mode = "public"` / `timeout_sec = 3000.0` / `collect = []`;
   line 30 `[environment]` / `network_mode = "public"`; line 26 `[agent] network_mode = "no-network"`; line 23
   `[verifier.env]` empty; no `environment_mode`, no `[verifier.environment]`.

**Consequence:** the entry's two table cells are factually **right** (see §4 item 9). Every defect below is a
*citation, scope, or provenance* defect, not a fabrication. I did not re-verify the tree-wide negative at
entry `:34-35` (89 + 642 files) — that is the second seat's Q10 job, and the entry gives no command for it.

Staged package (read-only): `/home/vgpnk/Projects/shokuknow/merge/kengaku/` — `MERGE-REPORT.md`,
`SOURCES.append.md` (rows 22, 23, 30 = S092, S093, S100), `knowledge/corpus/knowledge/benchmark-verifier-execution-model.md` (87 lines).

---

## 1. (a) PROVINCE surface, and sibling ownership

### Which surface

The entry lands on the **Frontier bullet 1 class, and specifically its round-29 sub-clause** — not on
"runtime task validity".

- `PROVINCE.md` §Frontier: "agentic benchmark task-spec audits (Terminal-Bench 2.0 / Toolathlon /
  SWE-bench Pro primary specs — unopened leads)". The entry reads primary specs and **code** at pinned
  commits. That is this bullet.
- The precise hook is `corpus/README.md:273`: "*Partly discharged round 29 attempt 2 (2026-10-25):* …
  It supersedes the `primary specs` half of the `unopened leads` phrase for those three sources — **their
  scoring code was not read and stays open**; contamination-transparency cards, runtime task validity and
  hosted judges remain open." The entry reads scoring/harness code for two of the three. **That clause** is
  what it discharges.
- It is **not** the "runtime task validity" phrase in the same bullet. `PROVINCE.md`'s round-29 attempt-2
  paragraph already refuses that ground in the lane's own words: "it does not run a benchmark, certify a
  task, or own deployment configuration, **runtime task validity**, hosted judges, contamination measurement
  or any benchmark's web properties." `corpus/README.md:251` carries the same bound ("Not deployment config,
  not runtime task validity, not contamination measurement").
- **Report to Main:** C1's frozen text calls the moved surface "runtime task validity" (claims file, §C1
  "Surface this claim moves"). The entry itself claims only axis E ("grader integrity"), and the lane's
  PROVINCE refuses the runtime-validity label. The C1 surface sentence should name the `README.md:273`
  scoring-code clause; scoring the claim against the "runtime task validity" phrase would be scoring ground
  this lane has already refused.

Landing shape needed (lane convention, one paragraph per partial admission): a **round-31 PROVINCE
paragraph** in the form of the round-29 attempt-2 one — "Core addition: the harness's own verifier execution
model, read from the harness source and two benchmarks' task configs at pinned revisions … it does not run a
benchmark, certify a task, or own deployment configuration, runtime task validity, hosted judges,
contamination measurement or any benchmark's web properties."

### Sibling ownership: **none**

Domain lines read from all 21 `*-shokunin/PROVINCE.md` files; `grep -icE 'benchmark' */PROVINCE.md` returns
only `kasegi:1` and `kengaku:12`.

| lane | its own words | verdict on harness-runtime/verifier ground |
|---|---|---|
| **chousa** | "**Refuses:** … **model-quality or evaluation claims (→ kengaku)**" (`chousa-shokunin/PROVINCE.md:12`) | routes evaluation **to** this lane |
| **kasegi** | "- kengaku — LLM evaluation and benchmarks" (`kasegi-shokunin/PROVINCE.md:49`) | routes benchmarks **to** this lane |
| **tameshi** | "**Domain:** verification-fixture craft … **Refuses:** product domains — every lane's gate remains its own; tameshi owns only the reusable craft" (`tameshi-shokunin/PROVINCE.md:3-16`) | owns *fleet-gate* fixture method; explicitly refuses a benchmark's own gate |
| **kama** | "**Domain:** local model serving & endpoint health" (`:3`) | serving plane; `PROVINCE.md` already routes it there |
| **kumitate** | "**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime" | fleet orchestration, not a third-party harness |
| **kotoba** | "**Domain:** prompt & skill craft" | prompt/skill craft only |
| others (audio, game-dev-2d/3d, kagi, kaidoku, kake, kotodama, lore, mado, mori, revenger, souji, tabi, tsukuroi) | domains read; none names benchmarks or evaluation harnesses | none |

No lane owns Harbor's or SWE-bench Pro's verifier execution model. The entry asserts no fleet runtime fact
(no container on this host, no endpoint), so it does not stray into kama's serving plane, kumitate's
orchestration, or tsukuroi's host operability. **No report-out is owed**; the only boundary worth naming in
the round report is kama (Harbor runs containers, and `PROVINCE.md` routes serving-plane facts to kama) —
recorded as adjacency, not overlap.

---

## 2. (b) Q1–Q19, row by row

Bar text quoted from `corpus/QUALITY.md`. Line pointers are to the **staged entry**
`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-verifier-execution-model.md`
(87 lines; line 1 is empty).

| # | bar (quoted, abridged with …) | verdict | located reason |
|---|---|---|---|
| **Q1** | "**the triad opens the entry.** The first three lines are `source:` (the `S###` row id(s), the URL, and the exact anchor), `verified-at:` … and `recheck:` (ISO date or cadence **and** the re-check action)." | **FAIL** | `:1` is an **empty line** — the first line is not `source:` (0 of 40 landed `corpus/knowledge/*.md` do this — `ls *.md | wc -l` → 40, blank-first-line census → 0). Anchors are not exact: `:3` `# v2/tasks/…/tests/test.sh` (elided) and `:4` `# task tree at 2fd12b8` (a tree, not an anchor) — and neither names `task.toml`, the file the entry's table actually reads. `:5 verified-at: 2026-10-23` ≠ this round's access date 2026-10-25 (C1 requires 2026-10-25); `:6` recheck says "ran 2026-10-23". Multi-source heads are precedent (`contamination-transparency-card.md:1-8`), so the fix is deleting the blank line, not restructuring. |
| **Q2** | "Each load-bearing claim rests on ≥1 `SOURCES.md` row of tier A or B ***for that claim's scope***; a tier-C row never stands alone…" | **FAIL** | Three scope misses: (i) `:31` TB2.0 task.toml cell rests on **S100**, whose registry `scope` is "which repository holds which Terminal-Bench release, how many task directories each release carries, and whether a release tag identifies a dataset version" — task.toml contents are outside it; (ii) `:32` SWE-bench Pro task.toml cell rests on **S093**, whose `scope` is "the executed grading code for one SWE-bench Pro V2 task … what is restored before grading and how the reward is computed" (row lists test.sh, parser.py, config.json — not task.toml); (iii) `:16` "the harness both Terminal-Bench 2.0 and SWE-bench Pro V2 run on" rests on **S092**, whose scope is "the harness's own behaviour", not which benchmarks use it — while in-lane rows that do carry it (S078 `v2/GATE.md` line 3 "Harbor 0.22 on Modal", quoted at `checklist:43`; S090 title "Terminal-Bench 2.0 and Harbor") are **uncited**. `:71-74` (Toolathlon) has **no cited row at all**. `:56` (README quote) has **no cited row** — it is already registered at S078. |
| **Q3** | "Each load-bearing sentence maps to an anchored quote (**≤25 words**, with location …); a paraphrase may narrow the quote, never widen it." | **FAIL** | The block quote `:19-21` is **28 words** (`sed -n '19,21p' <entry> | sed 's/^> //' | tr '\n' ' ' | wc -w` → `28`) — over the limit. (An earlier run of the same pipeline with `tr -d '\n'` printed 26; that figure was an artefact of my own command joining words across line breaks and is withdrawn.) Table cells `:31-32` carry **no quote and no location**. `:34-35` is a negative over 89 + 642 files with no command and no receipt. `:49-52` **widens** S092: only `env_paths.tests_dir` is re-uploaded, yet the entry concludes "the source tree, the fixtures, the data — are *not* overwritten" — and S093's own `teaches` cell contradicts it ("the environment is reset to base state first — but the fixture-restore step iterates tracked modifications only, so an agent-added untracked file under a fixture directory survives into grading"). `:68-70` "depends on the agent adapter used, not on the task" is an unsourced inference. |
| **Q4** | "The entry states what its sources do **not** establish **and the observation that would falsify the claim**." | **FAIL** (half) | Negative space is present (`:59-61` scoping of the README claim; `:71-74` "was not audited this round"). **No falsifier.** Both comparable admitted entries carry one (`benchmark-task-validity-checklist.md:137` `**Falsifier.**`, `contamination-transparency-card.md:138` `**Falsifier:**`). The observation is one line away from the entry's own negative: a task in either tree that sets `environment_mode = "separate"` or a `[verifier.environment]` section. |
| **Q5** | "A lab's disclosure about its own benchmark or model is labelled a self-report, not an independent replication…" | **FAIL** | No label paragraph anywhere. Precedent: `checklist:25-29` "**Source labels (Q5).** S077, S078 … are each a maintainer's **self-report about its own benchmark or its own tooling**"; `contamination-transparency-card.md:150-155`. `:56` is precisely a maintainer's self-report about its own benchmark, used as a contrast, and is not labelled. |
| **Q6** | "The entry **names the existing entry or coverage row it extends**; a weaker entry is superseded by a new entry that names it, and numbers are corrected by appended errata, never in-place edits." | **FAIL** | It names "the round-1 checklist" (`:10`, `:78`, `:85`) with **no repo path**. No file in `corpus/knowledge/` is called round-1; the landed entry is `corpus/knowledge/benchmark-task-validity-checklist.md` (index row `corpus/README.md:64`), admitted round 29 attempt 2. "Round 1" is the **merge package's** label (`MERGE-REPORT.md`: `benchmark-task-validity-checklist.md \| new-file \| round1`). The correction obligation is also unstated: the entry corrects `checklist:36` (axis E cell) and `checklist:96` ("S078 covers A, B, C, E…"), which per Q6/R1 require appended errata naming this entry. |
| **Q7** | "Entry file, its `corpus/README.md` index row and its coverage-map row land together; **no support rests on `/tmp`, `local://` or an unlanded working copy**." | **FAIL** | Two reasons. (i) Mechanical: the file is outside the lane (package path), with no index row and no coverage-map row — satisfiable at landing. (ii) Substantive and **not** satisfiable by the landing alone: the entry's correction target is text that exists **only in the unlanded package copy** — `merge/kengaku/knowledge/corpus/knowledge/benchmark-task-validity-checklist.md:49` "partly observable (the Harbor harness separates the verifier from the agent)". The landed checklist contains **no** "partly observable" (`grep -rn` over `corpus/` → 0 hits) and its TB2.0 line `:94-95` lists "A, B, C, D, F, G" with E simply absent. So `:11`/`:78`/`:85` quote an unlanded working copy. |
| **Q8** | "Every candidate screened and not admitted is recorded with reason and flip condition — as a `rejected` `SOURCES.md` row or a `Rejected:` line in the round `## Gate`." | N/A (round-level) | The entry admits/rejects no source. The round obligation stands: the package stages 65 entries and the lane admits one, so the round `## Gate` should say what happens to the other 64 (out of scope is a reason only if written). |
| **Q9** | "The source cited against a rejected claim must address the same property the claim asserts…" | N/A | No rejection inside the entry. |
| **Q10** | "Before admission, **a seat other than the entry's writer** re-opens each cited source and confirms every quote location and every number against it (exact cells or a stated range…)." | **PENDING — and currently unmeetable for two cells** | `:32` elides the task slug (`instance_internetarchive__openlibrary-…` matches **642** directories at that commit), so there is no single task to re-open; `:34-35` gives no command for the tree-wide negative. Five literal values need a located re-read and none is located by line: `timeout_sec = 1800.0`, `allow_internet = true`, `network_mode = "public"`, `timeout_sec = 3000.0`, `collect = []`. |
| **Q11** | "A knowledge entry or verdict that calls a binary rate a PASS against a bar must show the exact two-sided 95% Clopper–Pearson lower bound…" | N/A | No rate, no PASS/FAIL verdict, no bar. No CP95 obligation arises. |
| **Q12** | "A point fraction with errors can also FAIL …; INDETERMINATE applies only when the interval straddles the bar…" | N/A | Same reason as Q11. |
| **Q13** | "The commit that admits an entry must already contain, in its own tree, every second-seat (Q10) re-read report its `## Gate` row cites; the Gate cell names each such report by repo-relative path…" | **PENDING** | Mechanically checkable after landing: `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-31.md --commit <admitting commit>`. |
| **Q14** | "Qualifying re-read roles are exactly `reviewer`, `scout`, `critic`, `sentinel`, `revenger`… Reject explicit report writer/author … declarations that equal the candidate writer. **Without report-author metadata, identity means the registered seat**…" | **PENDING** | The entry carries **no `writer:` line** (5 landed entries do, e.g. `contamination-transparency-card.md:9 writer: KengakuR30`), so the writer-vs-reviewer comparison must rest on the registered seat. |
| **Q15** | "Q13/Q14 checks must read the requested commit for both cited report support **and total report inventory**." | **PENDING** | Same command family; `--selftest` fixture carries the two-commit control. |
| **Q16** | "Q15's one-report example is strengthened to **two separately cited reports** … All Git writes in that selftest use a temporary repository and an isolated environment…" | **PENDING** | Same. |
| **Q17** | "**literal reference coverage is not source endorsement.** A calibration claim about source-use consistency names its frozen source/path population…" | N/A | The entry makes no source-use-consistency calibration claim over a frozen population. |
| **Q18** | "**a forecast freezes its resolution criterion.** Before seeing output, name the measured unit, population and category rule…" | N/A | No forecast is filed. |
| **Q19** | "Every round appends one row per dispatched seat to `.ufo/waves/yield.tsv` … and reports yield per role family." | N/A at entry level (round obligation; instrument present) | `test -e .ufo/waves/yield.tsv` → present. |

Tally: **7 FAIL** (Q1, Q2, Q3, Q4, Q5, Q6, Q7) · **5 PENDING** (Q10, Q13, Q14, Q15, Q16) · **7 N/A or
round-level** (Q8, Q9, Q11, Q12, Q17, Q18, Q19).

Boundary note on the round-30 criterion (**Q20**, outside the assigned Q1–Q19): the entry's own landing
touches `corpus/SOURCES.md` by **append** (schema unchanged), `corpus/README.md` and `corpus/knowledge/`.
Q20's gate roster therefore binds C3's commit (`plans/sources_adopt.py`), not this one — but if the round
lands C1 and C3 in one commit, Q20's out-of-band run covers both.

---

## 3. (c) Is the ground already held by the coverage map?

**Partly — and the held part is the part the entry claims to close.** Three distinct states:

### Held already (do not re-claim as new)

1. **The axis definition and the S078 quote.** `corpus/knowledge/benchmark-task-validity-checklist.md:36`:
   "| E | Grader isolation | the verifier does not run inside the agent's sandbox, and hidden-test paths are
   restored or removed before the test patch applies | S078 "The verifier never runs in the agent's sandbox."
   (line 75) and "hidden-test paths are restored or removed before the test patch is applied" (line 103) |".
   The entry's `:56` re-quotes the same 8 words, cited to no row.
2. **The scoping rule, in almost the entry's own words.** `checklist:71-74`: "Axis E is scoped to the harness
   that publishes the claim. S078 states isolation for its locked release protocol; a harness that runs the
   verifier in a **shared environment by default** does not inherit that property, so "verifier isolated"
   must be read per benchmark, never as a general fact about benchmark releases." The *rule* is landed; the
   entry supplies the *value*.
3. **SWE-bench Pro V2's axis E is already recorded as covered.** `checklist:96`: "**SWE-bench Pro V2** —
   S078 covers A, B, C, **E**, F (partly), J". The entry's claim that it "discharges the axis-E sub-question
   for both benchmarks" (`:85`) therefore **narrows an existing coverage** for SWE-bench Pro V2 rather than
   opening one. That narrowing is real and worth having (S078's E is the locked protocol only, not the
   Harbor default) — but it is a **correction**, and corrections are appended errata (Q6/R1).

### Not held (genuinely new)

- Harbor's actual default value, read from harness code (S092) — the checklist states only a conditional.
- Terminal-Bench 2.0's axis E: `checklist:94-95` lists "A, B, C, D, F, G" for TB2.0 — **E is absent**, so E
  is open for TB2.0 on the evidence opened there.
- The two unconditional guarantees (stale-reward deletion, tests-dir re-upload) and the README-vs-default
  split.

### Which map row / frontier bullet it enters

1. **Frontier bullet 1, new sub-bullet under `corpus/README.md:273`**, in the shape of the round-30
   sub-bullet at `:275` — discharging the "their scoring code was not read and stays open" clause for
   TB2.0 and SWE-bench Pro V2 only, and leaving "contamination-transparency cards, runtime task validity and
   hosted judges" open **byte-identically** (the `:273` line is left as written, as `:275`'s round-30
   precedent does).
2. **A new coverage-map row**, in the shape of `corpus/README.md:242` (the card's row, which lands as an
   amendment and states its own bound): e.g. "**Benchmark verifier execution model**: covered at
   source-code-read depth (round 31, 2026-10-25) — knowledge/benchmark-verifier-execution-model.md;
   S092, S093, S100 (+S078). … Not a run of either benchmark, not runtime task validity, not deployment
   config, not a contamination measurement."
3. **Two appended errata, not in-place edits** (`checklist:36` axis E cell; `checklist:96` SWE-bench Pro V2
   covered set), each naming this entry and carrying its recompute locator. Without them the lane holds two
   contradictory statements about the same axis — the failure Q6/R1 exist to prevent.

The round-29 coverage row's own bound (`corpus/README.md:251`, "Not deployment config, not runtime task
validity, not contamination measurement") **stays true** and needs no edit — which is why the entry must not
be described as moving "runtime task validity".

---

## 4. (d) The entry's own overclaims, by line

Fabrication is not the problem — I fetched both task files and both table cells are correct. The overclaims
are claims whose *support is wider than the entry's citations*, plus one quote of a document the lane has
not landed.

1. **`:16`** "Harbor, the harness both Terminal-Bench 2.0 and SWE-bench Pro V2 run on" — S092's scope is the
   harness's behaviour, not its adopters. The fact is carried in-lane by S078 (`v2/GATE.md` line 3, "Harbor
   0.22 on Modal") and S090 (title "Terminal-Bench 2.0 and Harbor"); neither is cited. *[The fact is true;
   the citation is the defect.]*
2. **`:34-35`** "No task in either repository sets `environment_mode` or a `[verifier.environment]` section —
   verified by grepping every `*.toml` in both trees." A negative over **89 + 642** task directories (89 per
   `checklist:78-79` "**89 task directories and 89 `task.toml` files**"; 642 confirmed by my `v2/tasks`
   listing) with **no command, no count, no receipt**. As
   written it cannot be falsified by a reader, which is the state Q4's falsifier requirement exists to
   prevent.
3. **`:49-52`** "The agent's edits to the **environment under test** — the source tree, the fixtures, the data
   — are *not* overwritten; they persist into the grading phase." **Widened** beyond S092 (only
   `env_paths.tests_dir` is re-uploaded) and **contradicted by S093's own registered `teaches` cell**: "the
   environment is reset to base state first — but the fixture-restore step iterates tracked modifications
   only, so an agent-added untracked file under a fixture directory survives into grading." For SWE-bench Pro
   V2 the fixtures are **partly restored**; the precise claim is S093's, and the entry drops it.
4. **`:56`** "SWE-bench Pro V2's own README states "The verifier never runs in the agent's sandbox."" — an
   8-word quote already registered at **S078** ("§The locked protocol line 75: … (8 words)") and already
   landed at **checklist:36**, cited here to no row and not labelled a self-report (Q5).
5. **`:57-59`** "the replay path that captures `model.patch` and re-applies it to a pristine image before
   running the unchanged verifier there" — the mechanism belongs to `v2/tooling/patch_replay.py`, which the
   package registers as **S101** (package round-3 entry `:2`). No row cited in this entry carries it; S093 is
   `tests/test.sh`.
6. **`:68-70`** "which one produced a given score depends on the agent adapter used, not on the task" —
   inference, no row, and the two-armed reading is not established by anything cited. The fetched
   SWE-bench Pro task.toml shows the agent arm is `network_mode = "no-network"` (line 26) against a
   `"public"` verifier and environment — evidence the split is *declared per task*, which is the opposite of
   "not on the task".
7. **`:71-74`** Toolathlon: four concrete assertions (`evaluation/` directory, `EVAL_SERVICE_README.md`,
   `eval_server.py`, `eval_client.py`) with **no source line** — the entry cites S092/S093/S100, none of them
   Toolathlon. Rows exist (in-lane S080; package S102/S107), none cited.
8. **`:10-12` and `:78`** "Round 1 left axis E … flagged it as *partly observable*" / "The round-1 checklist
   entry recorded axis E for TB2.0 as "partly observable"." — the phrase exists **nowhere in the lane**
   (`grep -rn 'partly observable' corpus/` → 0 hits) and the landed entry's TB2.0 line (`:94-95`) does not
   record E at all. It exists only in the **unlanded package copy**
   (`merge/kengaku/knowledge/corpus/knowledge/benchmark-task-validity-checklist.md:49`). A quotation of a
   document the lane has not admitted, attributed to the one it has.
9. **`:32`** the elided slug `instance_internetarchive__openlibrary-…/task.toml` — not a locator: **642**
   directories match that prefix at the pinned commit. (The cell's values are correct — verified, §0 item 3
   — but they cannot be re-found from the entry.) Same class at `:3` (source anchor `v2/tasks/…/tests/test.sh`).
10. **`:85`** "This entry discharges the axis-E sub-question for **both** benchmarks by reading the harness
    and the task configs" — for SWE-bench Pro V2, E is already recorded covered (`checklist:96`); "discharges"
    overstates a **narrowing**. The same line's "ground: Frontier § "Agentic benchmark task-spec audits""
    names the bullet but not the sub-clause (`README.md:273`) that actually opens.

Not an overclaim (checked and cleared): **`:23-25`** "the verifier runs in the *same container the agent was
working in*" — S092's registered `teaches` cell says "the framework default is that the verifier shares the
agent's container", which supports the narrowing.

---

## 5. Minimum repair set for admission (handoff to the C1 owner)

Nothing here is a design choice; each item is a one-line edit or one appended errata.

1. Delete the blank line 1 so `source:` opens the file; re-ground `verified-at`/`recheck` to **2026-10-25**
   (and the three staged rows' `opened` cell from `2026-10-23` to `2026-10-25`, per C1's frozen predicate).
2. Replace the two elided anchors (`:3`, `:4`) with the exact file+line locators the table reads
   (`v2/tasks/<full slug>/task.toml` — name one slug — and `protein-assembly/task.toml`).
3. Either add **S078** as a fourth source line or delete `:56`/`:57-59` — S078 is the registered row for the
   README quote and the locked-protocol statement. **This collides with C1's frozen "exactly the three ids
   adopted this round (three distinct)"** — the claim text must be amended to allow one already-adopted row,
   or the README/locked-protocol section must be dropped. Report the choice to Main; do not silently widen
   the predicate.
4. Widen S093's registry `scope` (or add a row) to cover `task.toml`, and widen S100's `scope` (or add a row)
   to cover task-config contents — otherwise Q2's "for that claim's scope" fails on two of the three adopted
   rows. Adding rows changes the registry count C1 reports.
5. Narrow `:49-52` to S092's actual guarantee and carry S093's untracked-fixture finding.
6. Add the `**Source labels (Q5).**` paragraph and a `**Falsifier.**` line (Q4/Q5).
7. Name the extended entry by path — `corpus/knowledge/benchmark-task-validity-checklist.md` — and replace
   "round-1"/"partly observable" with the landed text (`:36`, `:94-96`).
8. Land, in the same commit: the entry, the `corpus/README.md` index row (after `:65`), the new coverage-map
   row, the Frontier sub-bullet under `:273`, and the two appended errata at `checklist:36` and `:96`.

---

VERDICT: NOT-ADMISSIBLE-AS-STAGED — 7 of 19 bar rows fail (Q1, Q2, Q3, Q4, Q5, Q6, Q7), 5 are pending on seats not yet run (Q10, Q13–Q16), the ground is only partly new (checklist:36 and :96 already hold axis E and the S078 quote, so the SWE-bench Pro half is a narrowing that needs appended errata), the entry cites a document the lane has not landed (package checklist:49) and two of its three adopted rows have scopes that do not cover the cells they support; no sibling lane owns harness-runtime/verifier ground (chousa routes evaluation to kengaku, kasegi routes benchmarks to kengaku, tameshi owns only fleet-gate fixture craft), and the eight located repairs in §5 plus the three errata in §3 are the whole distance to admission.
