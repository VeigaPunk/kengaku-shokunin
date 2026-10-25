# R29a2 prior art — is the per-task validity checklist already published?

Seat: `L1Kengaku29.R29a2PriorArt` (leaf, advice only). Date: 2026-10-25. Repo read at lane tip
`1f3b0f1ec41ec297130e8944ff97968d32324632` (frozen baseline; no production edits made).

Question answered, and nothing else: **is C1's entry instrument already published under another
name, or is it a local synthesis of primary maintainer documents?**

The instrument under test is the 10-axis table (A–J) in
`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-task-validity-checklist.md`
(73 lines, read in full): instruction–grader traceability, solvability, non-triviality,
environment stability, grader integrity, non-cheatability, contamination control, declared task
fields, declared tool surface / state-based evaluation, reproducible release.

**No global absence claim is made anywhere below.** Every statement is scoped to the 8 queries and
23 HTTP requests logged here, run 2026-10-25 between 06:42 and 07:05 UTC.

---

## 1. Method

Angles chosen to span the *naming* space rather than one phrase, because the question is "published
under another name":

1. checklist family — `Agentic Benchmark Checklist`, `BetterBench`, `BenchmarkCards`;
2. audit-protocol family — `Auto Benchmark Audit`, `protocol validity`, construct-validity audits;
3. standards family — UK AISI Autonomous Systems Evaluation Standard;
4. maintainer-protocol family — Terminal-Bench task review, SWE-bench Verified annotation;
5. primary re-open — Harbor `TASK_REVIEW_AUTOMATION.md` at `main` (the entry's own S077), to check
   that the entry's maintainer-protocol half is reproduced rather than invented.

All fetches used `curl -sSL -A "Mozilla/5.0"` and recorded `%{http_code}` plus byte size. A 200 with
a browser-verification page (OpenReview) is logged as *fetched but no content*, not as evidence.

Scratch: `/tmp/r29a2-priorart/` (`pages/` holds the fetched bytes; `searchlog.txt` holds the start
timestamp). Nothing is cited from scratch; quotes below are inline.

## 2. Search log (2026-10-25, all UTC)

| # | query | engine | outcome used |
|---|---|---|---|
| Q1 | `BenchmarkCards framework depicting benchmarks checklist questions` | web_search | found BenchmarkCards (NeurIPS 2025 D&B) + Evaluation Cards/EvalCards family |
| Q2 | `benchmark task validity checklist maintainers audit own tasks protocol` | web_search | found ABC, ABA, "Scorecard of AI Benchmark Quality", HackDetect |
| Q3 | `BetterBench assessing AI benchmarks criteria reviewers checklist` | web_search | found BetterBench 46-criteria reviewer protocol |
| Q4 | `construct validity LLM benchmarks audit checklist Bean et al 2025` | web_search | found Bean et al. 8-recommendation construct-validity checklist (NeurIPS D&B 2025) |
| Q5 | `"eval validity" checklist UK AISI Inspect benchmark task review` | web_search | found UK AISI AS Evaluation Standard + Inspect review workflow |
| Q6 | `Terminal-Bench SWE-bench task validity audit checklist maintainers published protocol` | web_search | found TB ICLR 2026 §2.3 verification criteria + TB 2.1 repair note |
| Q7 | `"Agentic Benchmark Checklist" Zhu arxiv "Establishing Best Practices" rigorous agentic benchmarks` | web_search | confirmed ABC = arXiv:2507.02825, NeurIPS 2025 |
| Q8 | `benchmark maintainers self-audit task quality checklist open-source eval repository CI checks canary oracle nop` | web_search | showed Harbor pipeline described by third parties as a self-audit template; TB authoring-manual mirror |

## 3. HTTP status log (2026-10-25)

| URL | status | bytes | what it yielded |
|---|---|---|---|
| https://uiuc-kang-lab.github.io/agentic-benchmarks/ | 200 | 22,122 | ABC taxonomy, 10-benchmark assessment table |
| https://uiuc-kang-lab.github.io/agentic-benchmarks/checklist/ | 200 | 16,932 | ABC item list, 3 sections, ~40 items |
| https://uiuc-kang-lab.github.io/agentic-benchmarks/checklist.html | **404** | 11,957 | wrong path; logged, superseded by `/checklist/` |
| https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/ABC.md | 200 | 3,833 | canonical ABC item text (diverges from site; see §6) |
| https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/README.md | 200 | 5,285 | ABC scope statement; repo layout |
| https://api.github.com/repos/uiuc-kang-lab/agentic-benchmarks/contents/assessments | 200 | 9,383 | the 10 assessed benchmarks (incl. `swe-bench.yaml`) |
| https://arxiv.org/abs/2507.02825 | 200 | 45,559 | ABC abstract and venue |
| https://arxiv.org/pdf/2411.12990 | 200 | 805,390 | BetterBench: 46 criteria, developer checklist |
| https://betterbench.stanford.edu/checklist.html | 200 | 5,455 | BetterBench checklist landing page (criteria in linked Overleaf/GDoc template) |
| https://aclanthology.org/2026.evaleval-1.25.pdf | 200 | 234,661 | third-party scorecard cites ABC as "evaluation development checklist" |
| https://ukgovernmentbeis.github.io/as-evaluation-standard/ | 200 | 17,191 | AISI per-submission required/recommended standards |
| https://inspect.aisi.org.uk/review.html | 200 | 74,401 | Inspect review workflow (observed, not quoted) |
| https://oxrml.com/research/measuring-what-matters/checklist/ | 200 | 13,654 | Bean et al. 8-section construct-validity checklist |
| https://oxrml.com/measuring-what-matters/checklist.html | 200 | 572 | redirect stub only (canonical path above) |
| https://proceedings.iclr.cc/paper_files/paper/2026/file/444a3737adaee10d86ad2ef5f74468e6-Paper-Conference.pdf | 200 | 2,514,769 | Terminal-Bench §2.3 verification criteria; Appendix C.5; Table 3 |
| https://arxiv.org/html/2601.11868v1 | 200 | 1,088,268 | Terminal-Bench paper HTML (cross-check of §2.3) |
| https://www.tbench.ai/news/terminal-bench-2-1 | 200 | 148,013 | TB 2.1 repair announcement |
| https://arxiv.org/html/2607.22368v1 | 200 | 460,076 | "Protocol Validity" definition |
| https://arxiv.org/html/2605.26079v1 | 200 | 693,504 | Auto Benchmark Audit per-task auditing |
| https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/docs/TASK_REVIEW_AUTOMATION.md | 200 | 41,842 | the entry's own S077 primary, re-opened |
| https://openreview.net/pdf?id=AhXMZPnOPS | **403** | 12,692 | "Benchmarks as Software: Continuous Validation and a Patch for Terminal-Bench 2.0" — **not obtained** |
| https://openreview.net/forum?id=AhXMZPnOPS | 200 | 4,787 | browser-verification wall; **no paper content** |
| https://github.com/SokolAnn/BenchmarkCards | 200 | 341,278 | BenchmarkCards template/collection repo |
| https://arxiv.org/pdf/2410.12974.pdf | 200 | 304,883 | BenchmarkCards primary PDF: "an intuitive and validated documentation framework" |
| https://neurips.cc/media/neurips-2025/Slides/121769.pdf | 200 | 942,326 | ABC slides (cross-check of three-part framing) |

23 requests: 20 usable content, 1 404, 1 403, 1 verification wall. Seven distinct instruments were
located; six were read at item level (BenchmarkCards at framework level).

## 4. Findings — the published instruments, named

### 4.1 Agentic Benchmark Checklist (ABC) — strongest prior

- Site: `https://uiuc-kang-lab.github.io/agentic-benchmarks/` §Taxonomy (200): "Task Validity: a
  task should be solvable if and only if the agent possesses the target capability."
- Canonical items: `ABC.md` at `main` (200). Three sections — Outcome Validity (I.*), Challenge
  Validity (II.*), Benchmark Reporting (III.*).
- Paper: arXiv:2507.02825, "Establishing Best Practices for Building Rigorous Agentic
  Benchmarks", NeurIPS 2025 (Q7 + abs page 200). Abstract (200): "we introduce the Agentic
  Benchmark Checklist (ABC), a set of guidelines".
- Applied to ten benchmarks, including `swe-bench.yaml` (SWE-Bench Verified: Task Validity 100,
  Outcome Validity 50, Reporting 30.8, Overall 60.3) — site table, read directly.
- Item-level text that matches the entry's axes verbatim in substance:
  - "Each task is verified to be solvable." (site II.8) — entry axis B.
  - "Setup does not change over time (e.g., no live website)." (site II.6) — entry axis D.
  - "Reports results of trivial agents (e.g., one that does nothing)." (`ABC.md` III.13) — entry
    axis C, the NOP check, stated as a checklist item.
  - "Agent is completely isolated from any ground truth information." (`ABC.md` II.5) — entry axis E.
  - "Implementation is free of vulnerabilities that could be exploited to pass evaluations without
    completing tasks" (`ABC.md` II.9) — entry axis F.
  - "Includes measures to prevent data contamination, such as a private, held-out test set, or a
    lively updated dataset." (`ABC.md` III.3) — entry axis G.
  - "Versions of all tools (e.g., Python) are clearly specified." / "All required API tools are
    consistently accessible to agents during evaluation." (`ABC.md` II.1–II.2) — entry axis I.

### 4.2 Terminal-Bench §2.3 "Verification" — the closest *maintainer-run, per-task* protocol

Path: ICLR 2026 proceedings PDF (200), §2.3. Named criteria applied task by task by "experienced
task reviewers": Specificity, Solvability, Integrity.

- "We consider a task to be verified if experienced task reviewers determine that a task meets our
  standards in the following criteria" (§2.3) — 23 words.
- Specificity: "A terminal bench task is considered well-specified if the unit tests will pass if
  and only if the container ends in an acceptable state." (§2.3) — 24 words. This is entry axis A
  in one sentence.
- Solvability (§2.3, oracle script causes all tests to pass) — entry axis B.
- Integrity: agents must not "cheat on a task by taking a shortcut that would not exist in a
  real-world deployment" (§2.3) — entry axis F.

**The decisive observation:** the Terminal-Bench paper does not merely publish criteria, it
*applies ABC to Terminal-Bench itself* — Appendix C.5: "We applied the Agentic Benchmark Checklist
(ABC) (Zhu et al., 2025) to further troubleshoot and demonstrate the evaluation rigor." (20 words),
with Table 3 scoring every ABC item (I.a.1 … III.13). So the benchmark whose artefacts the entry
mines has already published its own ABC assessment. Any entry that presents the checklist as newly
assembled from those artefacts must at minimum disclose this.

The maintainer also publishes a *post-release* defect taxonomy. `https://www.tbench.ai/news/terminal-bench-2-1`
(200): "The task issues in Terminal-Bench 2.0 fall into three categories" — External dependencies
("nine tasks where external dependencies changed after the benchmark was built"), Resource
mismatches ("Eight tasks had insufficient resource budgets"), and Misspecification ("instructions
that were not aligned to their tests"). 28 of 89 tasks were repaired and "no task is unsolved in
Terminal-Bench 2.1". These three categories are entry axes D, and partly A/B, already named and
counted by the maintainer — the entry's axis-D evidence is a maintainer-published category, not a
lane discovery.

### 4.3 BetterBench — the published benchmark-developer checklist

- arXiv:2411.12990 (200), abstract: "we provide a checklist for minimum quality assurance based on
  our assessment" (12 words); contribution bullet: "Creates a checklist for minimum quality
  assurance to support benchmark developers in aligning with best practices" (16 words).
- 46 criteria across design / implementation / documentation / maintenance, 0-5-10-15 scoring with
  independent-reviewer consensus, and a separate `checklist.html` (200) telling developers to
  self-justify each criterion with page numbers — i.e. a maintainer-facing self-audit instrument.
- Scope difference from the entry: BetterBench is per-*benchmark*, the entry is per-*task*. Axis J
  ("reproducible release") is entirely covered by BetterBench implementation criteria.

### 4.4 UK AISI Autonomous Systems Evaluation Standard — per-submission, executable gate

`https://ukgovernmentbeis.github.io/as-evaluation-standard/` (200), Required Standards:
"You must provide evidence that you have performed quality assurance (QA) checks on your
evaluation." (17 words). Also requires a canary string, fully automated scoring, unit tests for
custom tools/scorers, pinned dependencies, `METADATA.json`, and passing `poe check`. This is the
closest published analogue to a *maintainer-run acceptance gate* for agentic eval tasks, and it is
enforced by CI rather than prose.

### 4.5 Bean et al. construct-validity checklist (NeurIPS 2025 D&B)

`https://oxrml.com/research/measuring-what-matters/checklist/` (200): eight sections, tick-box
items, e.g. "Verify the quality and relevance of all task items especially for large or
automatically generated datasets" (17 words) — the item-quality half of entry axis A. Recommended
as pass/partial/fail with evidence links.

### 4.6 BenchmarkCards — documentation checklist, not a per-task audit

arXiv:2410.12974 (PDF, 200) line 34: "introduce BenchmarkCards, an intuitive and validated
documentation framework"; repo `github.com/SokolAnn/BenchmarkCards` (200) ships the template and a
card collection. Scope difference: a card documents a benchmark's purpose/data/metrics/risks, so it
does not audit individual tasks and supplies no scores. It is prior art for *reporting* rigour
(entry axes H and J), not for task validity, and should not be counted as an instrument equivalent.

### 4.7 Auto Benchmark Audit (ABA) and "Protocol Validity" — audit counterparts

- ABA (arXiv:2605.26079, HTML 200): "systematically audits individual benchmark tasks, uncovering
  issues such as hidden environment dependencies, specification gaps, and brittle grading logic"
  (19 words). Automated, not a maintainer checklist, but it operationalizes axes A, D, E at task
  granularity.
- Protocol Validity (arXiv:2607.22368, HTML 200): "a benchmark score supports a capability claim
  only when the evaluation protocol keeps that capability necessary for success" (20 words) — the
  theoretical statement of entry axes B/F, and it names the same TB/SWE-bench Pro failure cases the
  entry uses (Appendix C.3 "Harness loophole (Terminal-Bench, CoreWars)").

### 4.8 Negative result inside the searched space

No page in the 20 usable fetches presents *this exact 10-axis table* under a single name for
Terminal-Bench 2.0, Toolathlon and SWE-bench Pro V2 jointly. ABC's ten assessed benchmarks include
SWE-Bench Verified (not Pro), and no Toolathlon row appeared. That is the entry's only unoccupied
ground, and it is an application gap, not an instrument gap.

## 5. Axis-by-axis mapping (entry → published counterpart)

| Entry axis | Published counterpart (observed) |
|---|---|
| A instruction–grader traceability | TB §2.3 Specificity (24-word definition above); ABC I.d.1; Bean "validate automated output parsing" |
| B solvability | TB §2.3 Solvability; ABC site II.8 "Each task is verified to be solvable" / II.9 oracle solver; AISI QA-evidence requirement |
| C non-triviality | ABC III.13 "Reports results of trivial agents"; Harbor S077 "Nop Validation confirms doing nothing fails tests (task is non-trivial)" |
| D environment stability | ABC site II.6 "Setup does not change over time (e.g., no live website)"; AISI pinned versions; Protocol Validity |
| E grader integrity | ABC II.5 isolation, II.9 vulnerability-free; AISI automated scoring; TB Integrity |
| F non-cheatability | TB §2.3 Integrity; ABC II.9; ABC I.c.2 reward hacking; ABA |
| G contamination control | ABC III.3; Harbor `check-canary` "Prevents training data contamination by ensuring a unique canary string is present in task files"; AISI canary; Bean "Prepare for contamination" |
| H declared task fields | ABC II.1 tool versions; AISI `METADATA.json`; TB `task.toml` (entry's own S079) |
| I declared tool surface / state eval | ABC II.1–II.2, I.g state matching; AISI custom-tool tests |
| J reproducible release | BetterBench implementation criteria (public code, reproduction script, build status); ABC III.1–III.2 |

Ten of ten axes have a published counterpart in the fetched set. No axis is unique to the entry.

## 6. Operability observations (things that would bite an implementer)

1. **ABC has two divergent published revisions.** `ABC.md` (II.6 = "Annotated ground truth is
   verified for correctness", 9 items in section II) versus the website checklist (II.6 = "Setup
   does not change over time (e.g., no live website)", 10 items; subsequent items renumbered
   II.7–II.10). Item numbers are therefore not a stable citation key; cite item *text* plus page.
2. **BetterBench's 46 criteria are not on the checklist HTML page** (5,455 bytes, no criteria
   markup); they live in the paper and in linked Overleaf/Google Doc templates. A citable checklist
   needs the PDF, not the landing page.
3. **Two of the strongest prior pages are unquotable by simple fetch**: OpenReview `pdf` returns
   403 and `forum` returns a browser-verification wall. Do not cite the "Continuous Validation and a
   Patch for Terminal-Bench 2.0" paper from a fetch that only returns those two responses.
4. **Terminal-Bench's paper is itself revised evidence about TB2.0 validity** (Appendix C.5 and
   Table 3 score TB against ABC; §2.3 states the maintainer criteria). It is a better anchor for
   axes A/B/F than the CI document the entry currently cites for them.
5. **TB2.0 is not the current revision.** The 2.1 announcement (200) reports 28 of 89 tasks repaired,
   including misspecification and external-dependency cases, and states "no task is unsolved in
   Terminal-Bench 2.1". Any claim about TB2.0 axes A/D must name the revision and date it; a
   claim that TB2.0 still carries the axis-D defect is a claim about a superseded release unless
   the pinned commit is stated.

## 7. Verdict

**INCREMENTAL — the entry's instrument is already published under another name: the Agentic
Benchmark Checklist (ABC) (Zhu et al., NeurIPS 2025, arXiv:2507.02825; checklist page
`https://uiuc-kang-lab.github.io/agentic-benchmarks/checklist/`, HTTP 200 on 2026-10-25), with
Terminal-Bench's own §2.3 Specificity/Solvability/Integrity criteria as the closest published
maintainer-run per-task protocol and BetterBench's 46-criterion developer checklist as the closest
per-benchmark review instrument.** The maintainers also publish the post-release defect taxonomy
(external dependencies / resource mismatches / misspecification) that the entry re-derives as axes
A and D.

What the entry legitimately adds, scoped to the searched space: a per-benchmark *observability*
table for Terminal-Bench 2.0, Toolathlon-Verified and SWE-bench Pro V2 — three benchmarks ABC's ten
do not score — plus the honest marking of which axes each maintainer leaves unobservable. That is
incremental application work over a published instrument, not a new instrument.

## 8. Consequences for C1 (advice to L1; not a judgement or an integration)

Admission is not my call. If the entry is admitted as drafted, three statements are load-bearing and
currently unsupported by the evidence I collected:

1. "The lane's frontier names the **missing** instrument" (entry, opening sentence) is true only
   *in-lane*. In the literature the instrument is published as ABC. Recommend rewording to
   "unheld in-lane; published elsewhere as ABC".
2. Axes A, B, F are restatements of Terminal-Bench's published Specificity/Solvability/Integrity.
   Presenting them as derived from artefacts without attributing that criteria set is a
   provenance defect, not a coverage gain.
3. The entry claims TB2.0's axis-D defect was "reported by the maintainer itself". TB's paper also
   publishes an ABC self-assessment (Table 3). The entry should say which of the two it is relying
   on, and should not assert axis-D invalidity while the same paper's Table 3 scores I.f.* items 1.

Minimum rows that would make the entry's prior-art block honest: ABC (arXiv:2507.02825 + checklist
page), TB ICLR 2026 §2.3 / Appendix C.5, BetterBench (arXiv:2411.12990), UK AISI AS Evaluation
Standard, Bean et al. construct-validity checklist. Rows are for the L1 and the gate scribes to
place; I appended nothing to `corpus/SOURCES.md`.

## 9. Limits and unresolved gaps

- **No absence claim.** I did not search: non-English literature, MLCommons/ISO-style standards
  bodies, BIG-bench/HELM task-review docs, vendor-internal checklists, or anything behind a paywall.
  A published 10-axis equivalent could exist outside the 20 pages I read.
- OpenReview paper `AhXMZPnOPS` was not read (403 + verification wall); its title and abstract
  fragment arrived only through a search-result snippet, and is therefore used for orientation, not
  evidence.
- BenchmarkCards was read from its primary PDF (200) and repo (200) only for the framework claim;
  I did not verify its six-section template against the paper's own template listing, so the
  section-level detail from the search summary is deliberately not repeated here.
- I read the entry draft from the campaign merge directory (read-only) and the lane's
  `corpus/README.md`; I did not re-open S077–S080/S090 for quote correctness — that is the scouts'
  and quote reviewers' scope, and any conflict between this report and their located quotes should
  resolve in favour of the re-opened bytes.
- HTTP status records reachability on 2026-10-25 only; they do not establish that a quoted line sits
  at a stable anchor, and ABC's two revisions are a live example of that instability.

## 10. Tooling record

No installs, no upgrades, no package-manager transactions. Tools used: `curl`, `python3`, `pdftotext`
(poppler, pre-existing), `web_search`. PACMAN guard respected (nothing attempted).
