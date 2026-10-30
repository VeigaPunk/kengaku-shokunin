# C1PriceScoutA — R53-C1 prior-art pricing, wave 3 (seat report)

Seat: `C1PriceScoutA`, kengaku round 53, wave 3, lane `kengaku-shokunin`.
Scope (from the seat item): prior-art pricing for R53-C1's PRIOR-ART leg for four CONFIRMED
never-read presence-only tasks — `cobol-modernization` (`test_required_files_exist`,
`test_data_files_exist`), `log-summary-date-ranges` (`test_summary_file_exists`),
`path-tracing-reverse` (`test_image_c_exists`), `sparql-university` (`test_sparql_file_exists`).

Deliverable: `.ufo/waves/round-53/w3/C1PriceScoutA/prior-art-part.json` (4 rows) +
`.ufo/waves/round-53/w3/C1PriceScoutA/fetched/` (24 archives) + `fetched/SHA256SUMS` +
`COPY-MAP.txt`. Nothing outside this seat directory was written in the lane; no
`corpus/evidence/round53/` file was created by this seat (the L1 integrates — see COPY-MAP.txt).

## Verdict summary

| task | verdict | archive used | quote (words) | sweep fetches |
|---|---|---|---|---|
| `cobol-modernization` | **phenomenon-known** | terminal-wrench hack summary (names the task id) | 8 | — (not required for known) |
| `log-summary-date-ranges` | **phenomenon-new** | arXiv 2507.02825v5 abstract (ABC checklist) | 13 | 3 |
| `path-tracing-reverse` | **phenomenon-new** | arXiv 2605.12673v1 abstract (BenchJack / Agent-Eval) | 19 | 4 |
| `sparql-university` | **phenomenon-new** | arXiv 2609.26826v1 abstract (TB task-hardness audit) | 20 | 4 |

Distinct row URLs: 4 (≥ 3 required by leg 4). New rows: 3 (≥ 1 required).

### Why `cobol-modernization` is known and the other three are new

* **`cobol-modernization` — known.** `few-sh/terminal-wrench` publishes a per-task
  "Verifier Inspection" file for this task. Its first line names the task id
  (`` ## `cobol-modernization` — Verifier Inspection ``) and its body states the weakness:
  "**Verifier Only Checks.** The verifier only checks the side effects (the generated .DAT
  files), so this shortcut succeeded." That is a third-party, task-specific public report that
  the grader of *this* task accepted an artefact-only submission — exactly the phenomenon.
  The row's quote is the 8-word window that names the task id (the mechanical requirement);
  the weakness sentence sits further down the same archived file.
* **The other three — new.** No tracker item, issue body, PR body, dataset card or blog post
  found in this sweep names any of these three tasks *and* an existence-only / let-anything-pass
  weakness for it. Every task-specific public artefact located for them describes something
  else (a cross-device rename bug, a timeout bug, a reference-solution-mining incident, task
  provenance). Each therefore carries a general primary on the phenomenon plus a sweep of
  archived GitHub search-API fetches whose bodies (not counting the `SOURCE-URL:` header line,
  per amendment A2) do not name the task or any of its test names — i.e. a documented negative
  search over the three relevant trackers.

## Measured numbers

* Tasks priced: 4. Rows emitted: 4. Rejected rows: 0.
* Archives kept: 24 (4 row archives + 20 sweep fetches), each with a `SOURCE-URL:` first line,
  each ≤ 45.6 KiB (limit 1 MiB). `fetched/SHA256SUMS` lists all 24 digests.
* Quote lengths: 8 / 13 / 19 / 20 words (window 8–25). All four quotes verified
  whitespace-normalised-verbatim inside their archive (`norm(quote) in norm(archive)`).
* Sweep fetches: 3–4 per new row, all with distinct sha256 (the counter rejects duplicates
  within a row), all with a `SOURCE-URL:` header, all zero-hit (`"total_count":0`).
* Tracker sweep coverage per task: `harbor-framework/terminal-bench-2`,
  `harbor-framework/terminal-bench-2-1`, `harbor-framework/terminal-bench` (the 1.0 lineage),
  each in `in:title` and `in:body` scope → 6 candidate queries per task; non-zero hits were
  discarded as unusable (their bodies name the task) and replaced by the remaining zero-hit
  queries, giving 3–4 usable sweeps per task.
* GitHub code search for the four test names: `test_image_c_exists` → 1366 hits, all
  result-logs/other-project copies; `test_sparql_file_exists` → 353 hits, same; none is a
  weakness report for these TB2 tasks.
* GitHub issue search for the four test names: `test_image_c_exists` → 0 hits,
  `test_sparql_file_exists` → 0 hits; `test_required_files_exist` → 31 hits and
  `test_summary_file_exists` → 3 hits, all unrelated third-party projects.

## Exact commands run

```sh
# --- tracker sweeps (GitHub REST via gh), archived verbatim with a SOURCE-URL header
gh api "search/issues?q=repo:harbor-framework/terminal-bench-2+<task>+in:title"
gh api "search/issues?q=repo:harbor-framework/terminal-bench-2+<task>+in:body"
gh api "search/issues?q=repo:harbor-framework/terminal-bench-2-1+<task>+in:title"
gh api "search/issues?q=repo:harbor-framework/terminal-bench-2-1+<task>+in:body"
gh api "search/issues?q=repo:harbor-framework/terminal-bench+<task>+in:title"
gh api "search/issues?q=repo:harbor-framework/terminal-bench+<task>+in:body"

# --- global issue/code search (task ids and test names)
gh api "search/issues?q=<task-id>+in:title,body"
gh api "search/code?q=<task-id>&per_page=30"
gh api "search/code?q=<test-name>&per_page=30"
gh api "search/issues?q=<test-name>&per_page=20"

# --- issue / PR bodies and comment threads opened
gh api repos/harbor-framework/terminal-bench-2/issues/{68,73,89}
gh api repos/harbor-framework/terminal-bench-2/pulls/68
gh api repos/harbor-framework/terminal-bench-2/issues/{64,61,67,68,73,89}/comments
gh api repos/harbor-framework/terminal-bench-2-1/issues/{149}
gh api repos/harbor-framework/terminal-bench-2-1/pulls/53
gh api repos/harbor-framework/terminal-bench-2/issues?state=all\&per_page=100   # 89 items
gh api repos/harbor-framework/terminal-bench-2-1/issues?state=all\&per_page=100 # 247 items
gh api repos/RyanMarten/terminal-bench-3/pulls/{11,18,34,55}

# --- raw sources archived
curl -sSL https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/cobol-modernization/hack_summary.md
curl -sSL https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/cobol-modernization/gemini-3.1-pro/task.json
curl -sSL https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/cobol-modernization/gemini-3.1-pro/original_task/analysis.toml
curl -sSL https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/cobol-modernization/gemini-3.1-pro/hack_trajectories/v5_5/trial/verifier/test-stdout.txt
curl -sSL https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/917/hack_summary.md
curl -sSL https://raw.githubusercontent.com/few-sh/terminal-wrench/main/README.md
curl -sSL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/main/<task>/tests/test_outputs.py        # 4 tasks
curl -sSL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/main/tasks/<task>/tests/test_outputs.py  # 4 tasks
curl -sSL https://raw.githubusercontent.com/theseus-labs-rsi/Env-Rethink/main/hardening/tasks-tb21/<task>/README.md      # 2 tasks
curl -sSL https://raw.githubusercontent.com/minghinmatthewlam/openbench/main/tasks-imported/terminal-bench-2/<task>/PROVENANCE.md
curl -sSL https://arxiv.org/abs/{2507.02825v5,2605.12673v1,2609.26826v1}
curl -sSL https://arxiv.org/html/{2608.22103v1,2601.11868v1,2605.12673v1,2609.26826v1,2607.14004,2610.21088}
curl -sSL https://poolside.ai/blog/through-the-looking-glass
curl -sSL https://autobenchaudit.com/benchmark/tb2
curl -sSL https://rohanverma.net/pages/harness-engineering/research/pi-weaver/tasks/log-summary-date-ranges/
curl -sSL https://www.tbench.ai/benchmarks/terminal-bench-2/<task>            # 4 tasks
curl -sSL https://registry.harborframework.com/tasks/terminal-bench/<task>       # 4 tasks
curl -sSL https://huggingface.co/datasets/zai-org/terminal-bench-2-verified/raw/main/README.md
```

## Every URL opened, and every rejected candidate with its reason

### Kept (archived, in `fetched/`)

| archive | URL | role |
|---|---|---|
| `cpsa-tw-cobol-modernization-hack-summary.md` | `https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/cobol-modernization/hack_summary.md` | row 1 archive (known) |
| `cpsa-arxiv-2507.02825v5-abs.html` | `https://arxiv.org/abs/2507.02825v5` | row 2 general primary (ABC: weak/insufficient test suites, empty-response success) |
| `cpsa-arxiv-2605.12673v1-abs.html` | `https://arxiv.org/abs/2605.12673v1` | row 3 general primary (BenchJack/Agent-Eval: reward hacking = maximising score without performing the task) |
| `cpsa-arxiv-2609.26826v1-abs.html` | `https://arxiv.org/abs/2609.26826v1` | row 4 general primary (verifier bypass as a distinct failure layer from real hardness) |
| 20 × `cpsa-<task>__<tracker>__<scope>.json` | `https://api.github.com/search/issues?q=repo:<tracker>+<task>+<scope>` | negative sweeps (all `total_count:0`) |

### Rejected (opened, not used) — with reason

1. `https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/cobol-modernization/gemini-3.1-pro/original_task/analysis.toml`
   — task-flaw note ("the tests only verified that the output files were correct"), but the file
   contains **neither the task id nor any test name** → fails the mechanical naming rule for a
   known row and is not a general primary (it is task-specific) → unusable.
2. `https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/cobol-modernization/gemini-3.1-pro/task.json`
   — names the task id 27×, but the nearest weakness sentence ("the verifier only evaluates the
   final states of the output `.DAT` files and does not check the contents of the Python file")
   is 53 words away → no 8–25-word window can carry both the name and the weakness → rejected
   in favour of the hack_summary archive, whose heading names the task id.
3. `https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/cobol-modernization/gemini-3.1-pro/hack_trajectories/v5_5/trial/verifier/test-stdout.txt`
   — names `test_required_files_exist` / `test_data_files_exist` / `test_program_output`, but it
   is a transcript of the hacked run's own PASS lines; it documents the outcome, not the
   weakness → not a "describes an existence-only verifier" archive.
4. `https://raw.githubusercontent.com/few-sh/terminal-wrench/main/README.md`
   — names `cobol-modernization` only inside a statistics table (baselines/hacks counts); the
   prose about weakness is global (exploit-category table) and far away; the per-task row gives
   no weakness → rejected.
5. `https://raw.githubusercontent.com/few-sh/terminal-wrench/main/tasks/917/hack_summary.md`
   — the closest shape match found anywhere ("The verifier only checked for the existence of the
   summary file … allowing this hollow implementation to achieve a perfect score") but task id
   `917` is an unrelated desktop-entry task, not one of my four → rejected (it would be
   circular to price my tasks with another task's report).
6. `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/main/<task>/tests/test_outputs.py`
   (all four) — the graders themselves. They are the object under audit, not third-party
   documentation of a weakness; citing them as prior art would make every task trivially
   "known" → rejected by construction.
7. `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/main/tasks/<task>/tests/test_outputs.py`
   (all four) — byte-identical to the tb2 graders (`diff -u` empty for all four) → no
   independent primary, and 2.1 did not touch these graders → rejected.
8. `https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/68` and
   `https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/68`
   — names `path-tracing-reverse`, `test_image_compiles`, `test_image_similarity`, but the
   defect is an EXDEV cross-device rename failure (a false-fail robustness bug), not an
   existence-only weakness → rejected as a known row; its body also names the task, so it is
   unusable as a sweep for that task.
9. `https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/89`
   — a false-pass report, but for `filter-js-from-html`, a different task → rejected.
10. `https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/149`
    — names `cobol-modernization`, but the defect is unbounded verifier subprocess timeouts
    (a hang), not an existence-only weakness → rejected.
11. `https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls/53`
    — title "Share judge jobs with the harbor org"; no task names, no weakness → rejected.
12. `https://arxiv.org/html/2608.22103v1` (Hack-Verifiable Terminal Bench)
    — names **all four** of my task ids in its difficulty table → would fail the
    phenomenon-new "does not name the task" test and does not name any of their test names →
    rejected as a row archive. Its one weakness passage about `sparql-university` is about an
    agent reading `admin/tests/test.sh` (a planted-leak artefact of that study), not an
    existence-only grader.
13. `https://arxiv.org/html/2601.11868v1` and the ICLR proceedings PDF
    `https://proceedings.iclr.cc/paper_files/paper/2026/file/444a3737adaee10d86ad2ef5f74468e6-Paper-Conference.pdf`
    — names all four task ids (task tables / figures) and the PDF is 2.5 MB (over the 1 MiB cap)
    → rejected.
14. `https://arxiv.org/html/2610.21088` (Probe-and-Resume) — names all four task ids in its
    per-task verifier-strength table → rejected.
15. `https://arxiv.org/html/2607.14004` — names `path-tracing-reverse` and `sparql-university`
    in an agent-timeout table; no weakness claim → rejected.
16. `https://poolside.ai/blog/through-the-looking-glass` — names `path-tracing-reverse` only to
    report that an agent found the upstream `smallpt` implementation; that is a
    reference-solution-mining incident, not an existence-only grader weakness → rejected.
17. `https://autobenchaudit.com/benchmark/tb2` — a TB2-wide aggregate ("5 carry a major
    finding … typically instruction ambiguity, environment conflicts, or evaluation
    oversights") naming no task → usable only as a general primary; I used the arXiv
    abstracts instead (they state the phenomenon more precisely for a 8–25-word quote) →
    rejected, listed here as the alternate general primary.
18. `https://rohanverma.net/.../pi-weaver/tasks/log-summary-date-ranges/` — names the task but
    is about agent overhead, not the grader → rejected.
19. `https://www.tbench.ai/benchmarks/terminal-bench-2/<task>` and
    `https://registry.harborframework.com/tasks/terminal-bench/<task>` (4 each) — task
    description pages, no verifier-weakness claim → rejected.
20. `https://raw.githubusercontent.com/theseus-labs-rsi/Env-Rethink/main/hardening/tasks-tb21/{cobol-modernization,log-summary-date-ranges}/README.md`
    — descriptive "Verification" lists that do mention "/app/summary.csv exists", but the files
    contain neither the hyphenated task id nor a test name → cannot serve a known row; and they
    are task-specific, so not a general primary → rejected.
21. `https://raw.githubusercontent.com/minghinmatthewlam/openbench/main/tasks-imported/terminal-bench-2/{log-summary-date-ranges,sparql-university}/PROVENANCE.md`
    — conversion/provenance notes; no weakness → rejected.
22. `https://huggingface.co/datasets/zai-org/terminal-bench-2-verified/raw/main/README.md` —
    names neither of my four task ids (only `path-tracing`) and lists grading fixes for other
    tasks → rejected.
23. `https://api.github.com/repos/RyanMarten/terminal-bench-3/pulls/{11,18,34,55}` — one
    "Add <task> task" PR per task; bodies are only "Task imported from terminal-bench-2 for QA
    testing." → no weakness claim → rejected.
24. `https://openreview.net/pdf?id=AhXMZPnOPS` and `https://openreview.net/attachment?id=AhXMZPnOPS&name=pdf`
    — both fetches returned an HTML interstitial (12 692 bytes), not a PDF; the underlying
    "Continuous Validation and a Patch for Terminal-Bench 2.0" audit could not be archived as
    bytes → rejected (and it is a general primary anyway, not task-specific).

## Files produced (absolute paths)

* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutA/prior-art-part.json`
  — 4 rows; keys exactly `task`, `verdict`, `url`, `fetched`, `fetched_sha256`, `quote`, `sweep`
  (`sweep` omitted for the known row, as required).
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutA/fetched/` — 24 archives.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutA/fetched/SHA256SUMS`
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutA/COPY-MAP.txt`
  — maps every seat archive to its integration target `corpus/evidence/round53/fetched/<name>`.
  The `fetched` / `sweep[].file` paths in `prior-art-part.json` already point there, so the L1
  only has to copy the bytes (the counter's `inside()` check requires the archive to live under
  `corpus/evidence/round53/fetched`).

## Counter-leg self-check performed by this seat

Re-implemented the counter's `leg_prior_art` predicates locally over the produced JSON and
archives and asserted, for every row: `url` matches `^https?://[^/\s]+\.[^/\s]+/` and is not
`example.org`; the archive's `SOURCE-URL:` header equals the row `url` under
`url_key()` normalisation; `sha256` of the archive equals `fetched_sha256`; the quote is 8–25
words and appears whitespace-normalised in the archive; for known rows the quote names the task
id or one of its test names; for new rows neither the row archive nor any sweep body names the
task id or any of its test names (header line excluded per A2), and the sweep entries have
pairwise-distinct sha256 and `SOURCE-URL:` headers. All assertions passed.

## Tooling

No tool was installed or upgraded for this seat: `gh` (already present at
`/home/vgpnk/.local/bin/gh`) and `curl` sufficed, and `pdftotext` (poppler, already present)
was used once to read a PDF. No `pacman` transaction was run, per the host-wide pacman pause.

## Notes / caveats for the L1

* The three `phenomenon-new` rows rest on a **negative** argument: no public item naming these
  tasks and an existence-only weakness was found in this sweep. The sweep covers the two
  Terminal-Bench trackers (2.0 and 2.1) and the 1.0-lineage tracker by task id, in both title
  and body scope, plus global issue and code search on the task ids and the four test names.
  A tracker item filed after this sweep, or one outside GitHub, would change the verdict.
* For `cobol-modernization` the known archive is a **dataset write-up**, not an upstream
  tracker item; upstream `harbor-framework/terminal-bench-2` has no issue or PR about this
  task's grader. The weakness it documents (artefact-only acceptance of a hollow submission)
  is the same phenomenon the confirmed presence-only tests encode.
* The upstream graders of all four tasks are byte-identical between `terminal-bench-2` and
  `terminal-bench-2-1` (`diff -u` empty for all four) — the 2.1 release did not repair them.
