# r10 review — citation resolution (ReviewerCites)

Repo: /home/vgpnk/projects/shokunin/kengaku-shokunin, HEAD `1bd17ec` (`git rev-parse HEAD` → `1bd17eca24f6a4f93913b69720730f334bbb0365`); `git status --porcelain -- SKILL.md SCORECARD.md corpus/knowledge/` → clean. Read-only; scripts in /tmp/kengaku-r10/ (`resolve.py`, `cited-section.txt`, `tokens-raw.txt`, `urls.txt`, `url-status.txt`).

## Headline counts

```
awk '/^## Cited local sources/,0' SKILL.md | grep -cE '^- '            → 20
awk '/^## Cited local sources/,0' SKILL.md | grep -oE '~/[A-Za-z0-9_./{}*,+-]+' | sort -u | wc -l → 14
awk '/^## Cited local sources/,0' SKILL.md | grep -oE '`[^`]+`' | tr -d '`' | grep -E '[/.]' | sort -u → 80 path-ish tokens
```
80 tokens − 14 bare arXiv IDs − 5 bare-host URLs − 2 https URLs − 1 endpoint (`127.0.0.1:34113`) = **58 distinct local path citations**; 57 resolve on host, 1 documented-absent → **98.3% strict / 100% under repo convention**.

## Table 1 — SKILL.md cited local sources (20 bullets → 58 distinct paths)

Cmd A = `python3 /tmp/kengaku-r10/resolve.py` (os.path.isfile/isdir ≡ `test -e`/`-d`, ~ expanded, brace lists expanded). Cmd B = literal `test -e <path>`.

| # | path | cmd | result | verdict |
|---|---|---|---|---|
| 1 | `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` | A | YES | resolves |
| 2 | `…/godspeed-umwelt-iteration-2.md` | A | YES | resolves |
| 3 | `…/godspeed-umwelt-iteration-3-alpha-shittycodex.md` | A | YES | resolves |
| 4 | `…/gemini-3.1-pro-godspeed-benchmarks.md` | A | YES | resolves |
| 5 | `…/gemini-3.1-pro-godspeed-test-battery.md` | A | YES | resolves |
| 6 | `~/Projects/webzites/repos/llm-wiki/Home.md` | A | YES | resolves |
| 7 | `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md` | A | YES | resolves |
| 7 | `…/models/models.jsonl` (sibling, `+ models.jsonl`) | B | Y | resolves |
| 8 | `~/wikillm/llm-wiki` | B | ABSENT | **documented-absence** — bullet asserts it is absent; absence verified → correctly fenced (review.md §2 convention) |
| 8 | `~/Projects/webzites/repos/llm-wiki` (dir) | B | EXISTS | resolves |
| 9 | `~/Projects/bounties/ledger/telemetry.jsonl` | A | YES | resolves |
| 10 | `~/bench-arena/` | A | YES (dir) | resolves |
| 10 | `~/bench-arena/tasks/` | A | YES | resolves |
| 10 | `~/bench-arena/report-grok45.csv` | A | YES | resolves |
| 10 | `~/bench-arena/report-qwenlocal-v2.v2.csv` | A | YES | resolves |
| 10 | `~/bench-arena/telemetry-qwenlocal-v2.csv` | A | YES | resolves |
| 11 | `~/Projects/webzites/repos/llm-wiki/wiki/karpathy/**` → base `wiki/karpathy/` | A | YES | resolves (5 subdirs confirmed by `ls`) |
| 11 | `wiki/ai/foundations/bitter-lesson.md` (brace-exp of `wiki/ai/{foundations/bitter-lesson,alignment-and-training/rlhf}.md`) | B | EXISTS | resolves — base is the **llm-wiki repo root**, not `wiki/` (verified: `ls …/llm-wiki/wiki/` → ai, anthropology, biology, design, indexes, karpathy, linguistics, psychology; files exist at repo-root `wiki/ai/…`) |
| 11 | `wiki/ai/alignment-and-training/rlhf.md` | B | EXISTS | resolves |
| 12 | `https://huggingface.co/api/models` | curl -w %{http_code} | 200 | live (→ Table 3 note) |
| 12 | `https://openrouter.ai/api/v1/models` | curl -w %{http_code} | 200 | live |
| 13 | `127.0.0.1:34113` | `curl /health`; `/v1/models` | 200; `…Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf` | endpoint resolves, model identity matches SKILL.md/SCORECARD |
| 13 | `~/bench-arena/grade.sh` | A | YES | resolves |
| 14 | `/tmp/bench-r7/` | B | EXISTS (2026-09-28) | resolves today; ephemeral by design, debt-labelled in bullet (no penalty; risk if host cleans /tmp) |
| 15 | `~/bench-arena/` (round-5 battery, dup of #10) | A | YES | resolves |
| 16 | `wiki/karpathy/talks/` `{talks,projects-and-tools,standards-and-specifications}/**` | B | Y | resolves |
| 16 | `wiki/karpathy/projects-and-tools/` | B | Y | resolves |
| 16 | `wiki/karpathy/standards-and-specifications/` | B | Y | resolves |
| 16 | `philosophy-and-concepts/` → `wiki/karpathy/philosophy-and-concepts` | B | EXISTS | resolves — bare names are karpathy-children (the `wiki/philosophy-and-concepts` reading is ABSENT; karpathy-sibling reading confirmed by `ls wiki/karpathy/`) |
| 16 | `gwern-essays/` → `wiki/karpathy/gwern-essays-llm-and-ai-reasoning/` | B | EXISTS | resolves as prefix-shorthand [INFERENCE on intent; a literal `wiki/karpathy/gwern-essays` is ABSENT — only dir with this prefix] |
| 16 | `ai/foundations/complexity.md` | A | YES | resolves |
| 16 | `ai/books/` | B | EXISTS (`how-we-became-posthuman.md`, `thousand-brains.md`) | resolves |
| 17 | `corpus/evidence/round8-horizon/` | A | YES | resolves |
| 18 | `corpus/evidence/round9-replication/` | A | YES | resolves |
| 19 | `corpus/evidence/round9-fleet/` | A | YES | resolves |
| 20 | `corpus/knowledge/eval-prior-art-calibration.md` | A | YES | resolves; its 23 URLs → Table 3, all 200 |

Sub-file tokens inside bullets 17–19 (29-path batch, all `test -e` → Y): `../PROTOCOL.md`, `horizon.py`, `results.jsonl`, `run.log`, `critic-defects.md`, `predictions-r9.md`, `ordering.log`, `run_r9.py`, `results-r9.jsonl`, `replication.md`, `probeA/B/C.md`, `critic.md`, `harness-mutation.md`, `test_harness.py`, `prior-art.md`, `sibling-overlap.md`, `review.md`, plus 12 `corpus/knowledge/*.md` targets named across bullets 7–20 — **29/29 exist**.

**Rule on SCORECARD's claim:** the round-9 post-move depth row (SCORECARD.md:59) claims "cited-source bullets 16 → **20**" — **20 HOLDS exactly at HEAD** (`grep -cE '^- '` → 20; SKILL.md 414 lines, unchanged since commit 2575be6 "round-9"). The "14 distinct `~/…` paths" figure (SCORECARD.md:46 pre-move row and :117 appendix) **reproduces under its own command** (`… grep -oE '~/…' | sort -u | wc -l` → 14, re-run at HEAD, and `git show f147a27:SKILL.md` gives the same 312/16/14 as the pre-move row states) but is a counting-convention artifact: the `~/`-anchored regex (a) drops non-tilde tokens (repo-relative, wiki-relative, sibling, /tmp), (b) counts each `{a,b}` brace list as one token. True distinct local-path count = **58**. So: 20/20 bullets holds; 14 is reproducible-but-convention-bound, not wrong as written.

## Table 2 — corpus/knowledge/*.md source lines (21 files)

Cmd: `python3` first-non-heading-line scan (strict) + first-paragraph scan (lenient), pattern `https?://|~/|/home/|/tmp/|corpus/|../|127.0.0.1|*.md|*.jsonl|…`.

| file | strict (first line) | lenient (first ¶ names a path) | verdict |
|---|---|---|---|
| bailian-cli-telemetry.md | ok `Source: ~/.bailian/telemetry.jsonl` | ok | pass (path exists, B) |
| bench-arena-fresh-run.md | VIOL | ok `~/bench-arena/` | pass lenient |
| bench-arena-round5-battery.md | VIOL | ok (`bench-arena-fresh-run.md`, `127.0.0.1:34113`) | pass lenient |
| bench-arena-round6-stability.md | VIOL | ok | pass lenient |
| bench-arena-round7-noise-n25.md | VIOL | ok `/tmp/bench-r7-l2-executor/` | pass lenient |
| bench-arena-round7-scaffold-ablation.md | **VIOL** | **VIOL** — first path at :10 (`~/.config/opencode/opencode.json`), :13 `/tmp/bench-r7/capture/001-*-req.json` (exists, B); no `Source:` label | **defect** (source named only inside method prose) |
| bench-arena-round8-horizon.md | ok `**Source basis:** corpus/evidence/round8-horizon/{…}` | ok | pass |
| bench-arena-round9-replication.md | ok `**Source basis:** …` | ok | pass |
| bench-arena-task27-timeout-anatomy.md | VIOL | ok (`test.sh` context) | pass lenient |
| benchmark-selection.md | ok `Source: ~/Projects/…` | ok | pass |
| eval-design-digest-2.md | ok (sources in ¶: `karpathy/talks/` etc.) | ok | pass |
| eval-design-digest-3.md | **VIOL** | **VIOL** — ¶ names only directory `wiki/ai/`; labeled block `Sources read in full 2026-09-28:` at :6 with file bullets :8+ (`wiki/ai/scaling-and-forecasting/scaling-hypothesis-revisited.md`, `wiki/ai/agents-and-engineering/papers/react-reasoning-acting.md` — both exist, B) | **defect** (mitigated: source block 5 lines down) |
| eval-prior-art-calibration.md | ok `**Source basis:** corpus/evidence/round9-fleet/prior-art.md` | ok | pass |
| eval-theory-notes.md | VIOL | ok (`yao-second-half.md`, `rlhf.md`, `bitter-lesson.md` under `~/…/llm-wiki/wiki/`) | pass lenient |
| gemini-benchmark-suite.md | ok `Source: llm-wiki/wiki/ai/…/gemini-3.1-pro-godspeed-benchmarks.md + …test-battery.md` | ok | pass (both exist, B) |
| godspeed-eval-findings.md | ok `Source: ~/Projects/…` | ok | pass |
| ledger-route-telemetry.md | ok `Source: ~/Projects/bounties/ledger/…` | ok | pass (exists, B) |
| local-bench-arena.md | ok `Source: ~/bench-arena/` | ok | pass (exists, B) |
| local-model-index.md | ok `Source: ~/.bailian/skills/…` | ok | pass (exists, A) |
| open-model-catalogs.md | ok (names `local-model-index.md` in ¶) | ok | pass |
| telemetry-run-design.md | ok `Source: ~/Projects/…` | ok | pass |

**Counts:** strict first-line = 13/21 pass (61.9%); lenient first-paragraph = **19/21 (90.5%)**; 2 genuine defects (`bench-arena-round7-scaffold-ablation.md`, `eval-design-digest-3.md`). Pre-move claim "18 entries, each opening with a source line" (SCORECARD.md:46) was already loose under strict reading — `git show f147a27:corpus/knowledge/bench-arena-round7-scaffold-ablation.md` shows the same path-less opening at f147a27 (digest-3 also present pre-move).

## Table 3 — URLs in corpus/knowledge/eval-prior-art-calibration.md (23 distinct)

Cmd: `curl -s -o /dev/null -w '%{http_code}' -m 15 -L <url>` (GET only), parallel ×6, 2026-09-28.

| URL | result | verdict |
|---|---|---|
| https://arxiv.org/abs/2205.10625 | 200 | live |
| https://arxiv.org/abs/2209.11895 | 200 | live |
| https://arxiv.org/abs/2210.01296 | 200 | live |
| https://arxiv.org/abs/2305.18654 | 200 | live |
| https://arxiv.org/abs/2307.13702 | 200 | live |
| https://arxiv.org/abs/2309.06275 | 200 | live |
| https://arxiv.org/abs/2310.01798 | 200 | live |
| https://arxiv.org/abs/2310.20410 | 200 | live |
| https://arxiv.org/abs/2406.10149 | 200 | live |
| https://arxiv.org/abs/2406.12045 | 200 | live |
| https://arxiv.org/abs/2409.11055 | 200 | live |
| https://arxiv.org/abs/2410.15553 | 200 | live |
| https://arxiv.org/abs/2501.17399 | 200 | live |
| https://arxiv.org/abs/2504.04823 | 200 | live |
| https://arxiv.org/abs/2505.06120 | 200 | live |
| https://arxiv.org/abs/2507.05257 | 200 | live |
| https://arxiv.org/abs/2607.25987 | 200 | live |
| https://arxiv.org/abs/2609.04061 | 200 | live |
| https://aclanthology.org/2024.findings-acl.818/ | 200 | live |
| https://aclanthology.org/2025.emnlp-main.479/ | 200 | live |
| https://docs.vllm.ai/en/latest/features/batch_invariance/ | 200 | live |
| https://github.com/ggml-org/llama.cpp/issues/7052 | 200 | live |
| https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ | 200 | live |

**23/23 = 100%.** Novelty-pricing citations all live; no dead link weakens the prior-art verdicts. Every bare-host token in SKILL.md bullet 20 (`arxiv.org/abs/2505.06120`, 14 bare IDs, `aclanthology.org/2025.emnlp-main.479`, llama.cpp #7052, vllm, thinkingmachines) cross-resolves to a row above.

# State
- obs: eval-design-digest-3.md opens with no resolvable source path (directory-level `wiki/ai/` only; sources listed at :6–10) — corpus/knowledge/eval-design-digest-3.md:1-10 — medium [certain]
- obs: bench-arena-round7-scaffold-ablation.md has no Source: line; first path at :10, sources only inside method prose — corpus/knowledge/bench-arena-round7-scaffold-ablation.md:1-13 — medium [certain]
- obs: SCORECARD's "14 distinct `~/…` paths" undercounts 4× (58 actual) because its regex anchors at `~/` and collapses brace lists — SCORECARD.md:46,117 — low (convention-bound, command as written reproduces) [certain]
- risk: `/tmp/bench-r7/` and `/tmp/bench-r7/capture/` cited by SKILL.md and knowledge entries exist today but are ephemeral; a /tmp clean makes them dangling-by-drift (already debt-labelled) [moderate]
- risk: `gwern-essays/` resolves only as a prefix-shorthand of `gwern-essays-llm-and-ai-reasoning/` — a literal reading fails [low]

# Artifact: review
scope: SKILL.md §Cited local sources (20 bullets/58 paths), 21 knowledge-file source lines, 23 prior-art URLs; SCORECARD round-9 depth-row claim
verdict: **pass** — 20-bullets claim holds at HEAD; resolution ≥90% on every reading

**Overall citation resolution: 98.0% under the repo's own conventions (58/58 local incl. documented-absence, 19/21 source lines lenient, 23/23 URLs) and 91.2% under the strictest reading (57/58 + 13/21 + 23/23 = 93/102) — ≥90% HOLDS on all readings.**
