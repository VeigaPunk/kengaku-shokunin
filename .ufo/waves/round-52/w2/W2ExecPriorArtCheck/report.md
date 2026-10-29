# W2ExecPriorArtCheck — audit of w1 `C1ScoutPriorArt/prior-art.md` (2026-10-28)

**Attack:** re-fetch every URL in the w1 prior-art file; verify HTTP status, quote at the anchor, date; look for primaries it missed.
**Landed?** Fidelity attack FAILED to land (file is accurate). Completeness attack LANDED (four relevant primaries omitted, one of which audits all 89 TB2 tasks).

## Commands
`python3 fetch.py` (requests 2.34.2, UA-header GETs of 20 URLs → raw/), `python3 verify.py` (HTML tag-strip + whitespace/quote normalisation, `pdftotext` for the FSE PDF, substring match), line-number greps on raw HTML/PR API body, arXiv API search (`export.arxiv.org/api/query`, 8 queries), `arxiv.org/abs|html` of 6 candidates, `raw.githubusercontent.com/few-sh/terminal-wrench/main/{README.md,index/tasks.json}`, `python3 plans/round52_c1_grader_audit.py --lane .` (read-only, output kept in scratch only). No installs.

## Audit table
| id | URL | w1 HTTP | now | quote | anchor/date |
|---|---|---|---|---|---|
| S1 | arxiv.org/html/2601.11868 | 200 | 200 (1,088,268 B = claimed) | FOUND (24 w) | line 4504 id S2.SS3.p2.1 ✔; submitted 2026-01-17 |
| S2 | arxiv.org/html/2605.26079v2 | 200 | 200 (694,146 B) | FOUND ×2 | line 320 ✔, 782 ✔ (id at 773); 2026-05-25 |
| S3 | github PR #53 (+API) | 200/200 | 200/200 | FOUND (API body line 8) | PR open, merged=false, created 2026-03-11, upd 2026-05-28; finding lines 39/53/73/96/102/133 all ✔. Body now says "26 tasks" (ABA read 22) — body has been edited since |
| S4 | tbench.ai/news/terminal-bench-2-1 | 200 | 200 (148,013 B) | FOUND ×2 | line 11 ✔; "fixes 28 tasks" is **3 words, file says 5**; no machine date in HTML |
| S5 | HF zai-org/terminal-bench-2-verified | 200 | 200 (147,928 B) | FOUND ×2 | line 142/148 ✔, "2026.08.18 Update" ✔, 4 named tasks ✔ |
| S6 | june.kim/terminal-bench-frame | 200 | 200 (50,673 B) | FOUND | line 14 ✔; 2026-07-09. **Same page: "Findings are scoped to the public tasks of Terminal-Bench 2.1. The full 2.0 delta is in progress."** (omitted by w1) |
| S7 | testsmells.org FSE2020 PDF + catalog | 200 | 200 (562,193 B) | FOUND ×4 | pdftotext substrings ✔ |
| S8 | arxiv.org/html/2503.15223 | 200 | 200 (214,992 B) | FOUND | line 243 ✔; 2025-03-19 |
| S9 | snorkel.ai leaderboard 2-1 | 200 | 200 (479,156 B) | FOUND | line 491/14 ✔ |
| S10 | github tb issue #1387 | 200 / API 403 | 200 (1,165,626 B, +5) / **API now 200** | FOUND ×2 | line 644 ✔; opened Jul 19 2026; page now shows **"Closed as duplicate"** (w1 silent) |
| N1,N2 | openreview | 200 challenge | same challenge page (4,783/4,787 B) | – | claim holds |
| N3 | lacuna.tiptreesystems.com | 200 | 200 | – | not quoted by w1, fine |
| N4 | openai.com …swe-bench-verified | 403 | **now 200** (538,610 B) | – | drift only |

Totals: 20 URLs, 20× HTTP 200 now; 18/18 quote checks found; 0 fabricated quotes; 2 status drifts (403→200), 1 word-count slip, no publication dates in the file (only access date 2026-10-28, correct).

## What w1 missed (fetched 2026-10-28, all HTTP 200)
- **Terminal Wrench** arXiv 2604.17596 (2026-04-19) + github.com/few-sh/terminal-wrench: README row `terminal-bench__2.0 | 89 | 14 | 15.7%`. A dynamic (hacker-agent) audit of **all 89 TB2 tasks**; 14 tasks hackable: adaptive-rejection-sampler, bn-fit-modify (0 hack trajectories recorded), cobol-modernization, configure-git-webserver, custom-memory-heap-crash, git-multibranch, largest-eigenval, multi-source-data-merger, portfolio-optimization, pypi-server, regex-chess, schemelike-metacircular-eval, sqlite-with-gcov, winning-avg-corewars. Tasks pulled 2026-01-01..03-30.
- **Hacker-Fixer** arXiv 2606.08960 (2026-06-08): "We audit 1,968 tasks across five terminal-agent benchmarks and find 323 (16%) hackable by frontier models given only the task description."
- **2610.15924** (2026-10-11): documents a presence-level verifier miss — "the verifier checks file existence and byte equality, missing that no independent copy was made."
- **BenchJack** 2605.12673 (2026-05-12): taxonomy + Terminal-Bench exploit appendix. ABC checklist 2507.02825: 0 Terminal-Bench mentions (weak adjacency).

Overlap with current counter output (`CANDIDATES total=29`, `CONFIRMED new=0`, `PRIOR-ART ok=False`; confirmations.json and prior-art.md not yet in the lane tree): candidates ∩ Terminal-Wrench-14 = {bn-fit-modify (lane already hand-read), multi-source-data-merger (16 hack traj., 7 serious), winning-avg-corewars (20, all serious)}. If L1 confirms either of the latter two, the exploitability is already documented at task level → price phenomenon-known unless the P1 presence-only weakness is shown to differ from the documented exploits (I did not read the trajectories).

## Overall novelty verdict
- w1 file is faithful (fidelity PASS) but incomplete (completeness FAIL); its own verdict "instrument phenomenon-new, every task-finding phenomenon-known" survives, and is *strengthened* on tasks by Terminal Wrench.
- Whole-benchmark grader triage of TB2 is **not** new as a phenomenon/activity (dynamic: Terminal Wrench 14/89; ABA; June Kim 2.1 probe). A **static, per-test presence-only (A1 P1) classifier** over TB2's 89 graders: no fetched primary states it → phenomenon-new for the instrument. The w1 file prices pre-A1 V1/V4, not P1; the final prior-art.md should be re-priced against P1.
- Score-rule consequence: novelty 9 can rest only on a confirmed finding in a task outside the TW-14 / PR #53 / 2.1 / Z.ai lists with a quote verbatim in the capture. At the audited state (0 confirmed, 183/184 captures, PREDICATE R52-C1 fail) the lane has none.

## Files
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ExecPriorArtCheck/prior-art-audit.json
- this report. Scratch (fetch.py, verify.py, raw/, counter.txt) removed after copying.
