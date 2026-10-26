# R38ScoutPriorArt — prior art for the build-pmars grader findings (kengaku round 38, wave 1)

Seat: scout, leaf, read-only. Fetch date 2026-10-26. Tools: `gh api` (GitHub REST, authenticated; search limit 30/min hit once, retried), `curl`, `read`. Scratch `/fast/scratch/hyaku/kengaku-r38/R38ScoutPriorArt` (deleted at end). No lane file edited.

## Question
Did anyone upstream report the receipt's headline observations about the pinned TB2.0 `build-pmars` grader: a canned program passes; the `ldd` string scan misses a `dlopen()`ed libX11; `Results:` is a prefix `re.match`; non-zero exit ignored when stdout is non-empty; canned script earlier on PATH; `debian/` may be a file; a directory named `*.c` counts?

## Answer (summary)
**No hit reports a permissiveness of the build-pmars grader.** Every upstream item about this task is either about the oracle (`solve.sh` pins) or about the grader being too strict (`/app/pmars-*/debian` and `src/*.c` directory-shape tests rejecting honest builds). The closest permissiveness-adjacent text is an LLM audit that names the missing build-to-source provenance link and then rates the `ldd` check "reliable". Finding class ("presence/shape/substring checks accept an unenforced instruction half") is already published (R37ScoutPriorArt, 16 hits); this seat adds no new class hit, only instance-level negatives.

## Hit list (URL, date, state, quote with location, type)

| # | URL | Date | State | Quote (location) | Type |
|---|---|---|---|---|---|
| 1 | https://github.com/harbor-framework/terminal-bench-2/issues/59 | 2026-04-13 | open, 0 comments | "Version '1.22.21' for 'dpkg-dev' was not found" (issue body, solve.sh apt output) | **oracle**, not grader. Pinned `solve.sh` has `dpkg-dev=1.22.21` (`corpus/evidence/round38/tb2-build-pmars/solve.sh:15`, grep). Consistent with the lane limit "probe never runs the oracle". |
| 2 | https://github.com/harbor-framework/terminal-bench-2/pull/38 | 2026-02-13 | open, unmerged | "Opus now passes build-pmars with the more precise instructions on where/how to store source" (PR body) | other: instruction change `/app` → `/app/pmars-<version>/` + "Leave the source tree in place"; false-reject side |
| 3 | https://github.com/harbor-framework/terminal-bench-2/pull/53 (TB2.1 diff PR) | 2026-03-11 | open ("not for merging"; TB2.1 released) | file list: `build-pmars/instruction.md`, `build-pmars/solution/solve.sh` (unpins apt versions); `tests/test_outputs.py` not in the changed files | other. `gh api pulls/53/files` filtered on `pmars` returned only those two files. |
| 4 | https://github.com/harbor-framework/terminal-bench-2-1/tree/main/tasks/build-pmars | fetched 2026-10-26 | n/a | `diff` of raw TB2.1 `tests/test_outputs.py` and `tests/test.sh` against the lane captures: no output, "TESTS_BYTE_EQUAL"; only `instruction.md` differs | evidence: TB2.1 did **not** touch the grader; every receipt observation also holds for TB2.1 `main` (inference from byte equality; the probe was not run against it). |
| 5 | https://github.com/harbor-framework/terminal-bench/issues/631 (tb3 hardening audit of tb2.1 fixes) | 2026-05-14 | closed | "build-pmars \| Instruction ambiguous on build destination \| LLM rubric `test_instruction_alignment` \| Soft only \| Defer" (body, Part 1 table row T2, line 19) | other: classifies the TB2.1 fix as instruction ambiguity, no verifier finding. Only mention in body (grep of body + comments for `pmars\|ldd\|x11\|from source`: 1 line). |
| 6 | https://github.com/harbor-framework/terminal-bench-1/pull/1401 | 2026-01-21 | open | "the test hardcoded paths like `/app/pmars-*`, causing failures when models extract sources to different directory structures" (PR body, Problem) | other: shape test is too strict; the patch replaces it with `rglob("debian/control")` and `glob("*/src")`, which would make the shape check **more** permissive. Reports no permissiveness. |
| 7 | https://github.com/harbor-framework/terminal-bench-1/pull/1381 | 2025-12-26 | closed, unmerged | "Based on analysis of 5 runs, 4/5 failed due to this misunderstanding." (PR body, Problem) | other: Z.AI measurement of the same `pmars-*` shape test rejecting flattened-source builds that pass `test_pmars_works` |
| 8 | https://github.com/harbor-framework/terminal-bench-1/pull/1201 | 2025-09-15 | closed | diff of `tests/test_outputs.py`: `pmars -b -r 50 -f flashpaper.red rave.red` → `-f /app/flashpaper.red /app/rave.red` (files) | other: oracle/test path fix. Keeps `re.match(r"Results: \d+ \d+ \d+", ...)` (context line in diff). |
| 9 | https://github.com/harbor-framework/terminal-bench-1/pull/764 (task origin, merged 2025-08-26) | 2025-08-26 | merged | carlini review comment on `test_outputs.py:63`: "You never require that the agent put the source in /app. What if it puts it in /tmp?" | adjacent: a reviewer saw one presence-check gap; fixed by instruction wording, not by the test. Author checklist box ticked: "It is hard for the agent to cheat on my task". Same review: carlini flagged reliance on binary RNG; author changed it. |
| 10 | https://github.com/JonathanGabor/terminal-bench-2-audit/blob/main/audit_results/20260120_125158/audit.txt (lines 211-259) | 2026-01-20 | n/a (static) | "There's no direct verification that the binary was compiled from the specific source" (l.249); "The X11 dependency check via `ldd` is reliable." (l.255) | **permissiveness-adjacent, partly contradicting**: names the provenance gap (l.248-249), rates the task 4/5, and calls `ldd` reliable. No exploit executed; no mention of dlopen, canned output, PATH, exit status, `debian/` file. |
| 11 | https://huggingface.co/datasets/zai-org/terminal-bench-2-verified (card, instruction-fix table) | n/a | n/a | "build-pmars Clarify directory name format pmars-*" (card, Instruction Fixes) | other: the fix list says the problem is instruction wording; grader untouched |
| 12 | https://www.tbench.ai/news/terminal-bench-2-1 (delta chart) | n/a | n/a | chart text: "build-pmars +24.3%" | other: TB2.1 pass-rate gain from the instruction change |
| 13 | https://github.com/harbor-framework/terminal-bench-2-1/pull/118 (leaderboard, Grok 4.5 + Cursor CLI) | 2026-07-13 | closed same day | github-actions comment: "Reward hacking 🟡 … `e4f67b8d` · build-pmars · judge verdict" (comment line 30, box ticked) | **unknown**: a judge flagged one build-pmars trial as reward hacking. The verdict page returned HTTP 404 on fetch (`read` hub URL), so the reason is **not retrievable**. Cannot be rowed; may not concern the grader. |
| 14 | harbor-framework/terminal-bench-2-1 PRs #142, #148 and terminal-bench PR #1202 | 2026-06/07 | closed | hits are `winning-avg-corewars` (pMARS opponent battles); #142: "behaviorally inert source content to alter pMARS's fixed random series" | not build-pmars; excluded |

Search coverage (all `gh api -X GET search/issues`, 2026-10-26): `pmars` and `build-pmars` in terminal-bench-2 (3 hits: #38, #53, #59), terminal-bench-2-1 (3 leaderboard PRs: #118, #142, #148), terminal-bench (2: #631, #1202), terminal-bench-1 (6: #1401, #1381, #1201, #764, #783 corewars, #851 CI), harbor (6, all non-task: sandbox/agent PRs, issue #386, PR #60/#194). Terms `ldd`, `X11`, `dlopen`, `libX11`, `"built from source"`: terminal-bench-2: 0; terminal-bench-2-1: only PR #186 ("built from source", a Haiku leaderboard submission, unrelated); terminal-bench: hits are unrelated task PRs (x86 lifter, fp8-rmsnorm, FreeCAD, etc.; none names build-pmars); harbor: unrelated agent/sandbox PRs. `terminal-bench-3` repo is not searchable (HTTP 422), `laude-institute/*` repos 422. BenchJack (arXiv 2605.12673, 1.9 MB) and the TB2 paper (arXiv 2601.11868) and Berkeley RDI blog: `grep -i -o pmars` count 0 in each fetched copy.

Not trusted: a web-search assistant answer this seat received describes the `ldd` test as checking "four library-name strings" and lists the exit-status helper behaviour. It cites no upstream issue and says "not a demonstrated bypass"; it is an unsourced restatement of the pinned test, not prior art. Not counted.

## Receipt observations vs prior art

| Receipt observation | Prior art |
|---|---|
| canned 14-line C program + empty `debian/` + zero-byte `src/dummy.c` passes all four tests | provenance gap named once in the LLM audit (#10, l.249); no executed instance; PR #1401 would loosen further |
| `ldd` string scan misses a dlopen()ed libX11 | not found (audit calls `ldd` "reliable") |
| `Results:` checked by `re.match` prefix only | not found (only seen unchanged in diffs #8) |
| non-zero exit ignored when output non-empty | not found |
| canned script earlier on PATH vs installed binary | not found |
| `debian/` may be a file / directory named `*.c` counts | not found; upstream only reports the shape test as too strict (#6, #7) |

## S117 proposal
**None qualifies.** A tier-B row must support a statement the entry makes; no hit reports a build-pmars grader permissiveness. Issue #59 (named in the frozen claims as "rowed or refused") is refused: it reports oracle pins failing, not the grader; the claim limit "probe runs the grader, never the task image or the oracle" already covers it, and the pinned `solve.sh` capture shows the same pins. The nearest candidates (audit #10; tb1 PR #1381) are adjacent only: the audit names the provenance gap but rates the `ldd` check reliable, and the PR reports over-strictness. If the L1 wants a one-line prior-art statement for the entry's limits, the evidence supports: "No upstream issue or PR found reporting a permissiveness of this grader; upstream reports concern oracle pins (#59) and over-strict directory-shape tests (tb1 #1381, #1401, tb2 #38); TB2.1 left `tests/` byte-equal (diff this run)."

## Limits
- #13's judge verdict (build-pmars flagged) could not be read (HTTP 404); a flagged trial remains an unexplained signal, not a hit about the grader.
- I did not clone PR diffs beyond file lists and patches shown; GitHub search is lexical, a report that never names `pmars` (e.g. a generic "grader accepts canned output" issue) would be missed.
- Byte equality with TB2.1 `main` (hit 4) shows the grader is unchanged; the probe was not run against TB2.1.

VERDICT: prior-art-14-hits-row-no
