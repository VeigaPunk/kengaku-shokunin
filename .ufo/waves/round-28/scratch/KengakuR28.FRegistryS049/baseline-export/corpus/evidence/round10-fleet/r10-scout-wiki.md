# r10 scout — digest queue × llm-wiki surface (ScoutWiki)

Scope: SCORECARD.md/LOG.md digest-queue extraction → llm-wiki existence check → freshness inventory.
Repo read-only: /home/vgpnk/projects/shokunin/kengaku-shokunin @ 1bd17ec. Wiki: ~/Projects/webzites/repos/llm-wiki.

## 0. Headline

- The "3-source digest queue" is **external URLs, not llm-wiki paths**: Laban/ICLR 2026 (arXiv `2505.06120`), Lanham 2023 (arXiv `2307.13702`), llama.cpp #7052. Verified: **0 traces of any of the three anywhere in llm-wiki** (all file types, all dirs, `.git` excluded).
- The assignment's freshness command returns **EMPTY**: 0 wiki/*.md newer than `LOG.md`; widened to whole repo, any file type → still **0**. Reason: llm-wiki is frozen — last commit `e66e614` (2026-08-08), working tree clean, 0 commits since 2026-09-01; all 171 wiki md share one mtime (2026-09-20 22:50, wholesale touch) so **mtime is not an edit signal for this repo — git is**.
- Consequence for the L1 axis-moves: the depth ceiling ("named-but-unread digest queue") is **external fetch+digest work** (no repo-side file can close it); the coverage ceiling ("non-karpathy wiki/ai beyond eval scope") is a **standing scope gap** — 23-file `wiki/ai` surface, zero in-round additions.
- Two precision flags for the integrator: (a) corpus says #7052 was "reopened 2026-05-21"; today's fetch shows issue **state=closed** with a 2026-05-21 comment saying "reopening". (b) README:84 "none read yet" coexists with fetch-based quotes in prior-art.md (SNOWBALL +15–20%, App. G +1%) that are **not** in the arXiv abstract — the queue item is *fetched, not digested*.

## 1. Queue extraction (exact sources)

Commands:
```
grep -n -i 'queue|digest' SCORECARD.md LOG.md PROVINCE.md SKILL.md corpus/README.md
awk 'NR==59' SCORECARD.md | cut -c650-2000
awk 'NR==84' corpus/README.md
```
Outputs (terse):
- `SCORECARD.md:59` (depth ceiling, tail): `**Ceiling:** the 3-source digest queue (Laban ICLR 2026, Lanham 2023, llama.cpp #7052) is named but unread.`
- `SCORECARD.md:73` (rubric cap): "…a named-but-unread digest queue; scope explicitly declared unmapped".
- `corpus/README.md:84` verbatim: `- **Prior-art digest queue** (new, round 9): Laban et al. ICLR 2026 (\`arxiv.org/abs/2505.06120\`), Lanham et al. (\`2307.13702\`), llama.cpp #7052 — named in \`knowledge/eval-prior-art-calibration.md\`, none read yet; they supply the RECAP/SNOWBALL controls and the serving flags (\`-np 1\`, fixed \`-b\`/\`-ub\`) this lane's ESS argument needs.`
- `LOG.md`: **no queue enumeration** — only generic "digest" prose (r4/r5/r7 entries); `grep -n -i 'queue' LOG.md` → 0 hits.
- `SKILL.md`: `grep -n -i queue` → 0 hits. `PROVINCE.md`: no queue string (only "digest into `corpus/knowledge/eval-*`" as the digest route, `PROVINCE.md:12`).
- Queue detail block also present at `corpus/knowledge/eval-prior-art-calibration.md:56-68` (numbered 1–3 with per-source rationale).

## 2. Queued sources → llm-wiki status

Checks run (from `~/Projects/webzites/repos/llm-wiki`):
```
grep -rni --exclude-dir=.git -e '2505\.06120' -e '2307\.13702' -e '\b7052\b' -e 'laban' -e 'lanham' .      # → 0 hits (all types)
grep -rli --exclude-dir=.git 'recap' wiki raw outputs state                                                   # → 0 hits
find . \( -iname '*laban*' -o -iname '*lanham*' -o -iname '*2505.06120*' -o -iname '*2307.13702*' \) -not -path './.git/*'   # → 0 hits
ls raw/papers/   # slug convention 10-<doi>.md; only 10-48550-arxiv-1706-03762.md is an arXiv paper
```
Corpus-side citation census (from repo root):
```
for id in '2505.06120' '2307.13702' '7052'; do grep -rn "$id" --include='*.md' corpus | awk -F: '{print $1}' | sort | uniq -c; done
```

| # | Source (queue name) | Exists under llm-wiki? | Lines (local) | Already digested? | URL resolves today | Verdict |
|---|---|---|---|---|---|---|
| 1 | **Laban et al., LLMs Get Lost In Multi-Turn Conversation**, ICLR 2026 — arXiv `2505.06120` | **NO** — 0 hits for ID/author across all file types; no filename match | n/a (no local file; `raw/papers/` holds no 2505* slug) | **NO — cited-only queue.** Corpus hits: `README.md:84`, `eval-prior-art-calibration.md` ×2 (:20, :57-61), `prior-art.md` ×2 (:18, :27) | **YES** (fetched 2026-09-28 via arXiv API: authors Laban/Hayashi/Zhou/Neville, 2025-05-09; abstract confirms 39% avg multi-turn drop, 200k sims, assumption+over-reliance) | Actionable **external** digest: supplies RECAP/SNOWBALL arms + aptitude/unreliability decomposition. Note: SNOWBALL +15–20% / App. G +1% quotes are not in the abstract re-fetched here — they rest on r9's full-text fetch claim (`prior-art.md:5-7`) [observed-claim, not re-verified by me] |
| 2 | **Lanham et al., Measuring Faithfulness in CoT** — arXiv `2307.13702` | **NO** — same 0-hit grep | n/a | **NO — cited-only.** Hits: `README.md:84`, `eval-prior-art-calibration.md` ×2 (:21, :62-64), `prior-art.md` ×2 (:25, :36 section) | **YES** (fetched: 30 authors, 2023-07-17; abstract confirms CoT-intervention method, task-variation in conditioning) | Actionable external digest: template upgrading probe B; nothing repo-side can close it |
| 3 | **llama.cpp issue #7052** — `github.com/ggml-org/llama.cpp/issues/7052` | **NO** — `\b7052\b` 0 hits | n/a | **NO — cited-only.** Hits: `README.md:84`, `eval-prior-art-calibration.md` ×2 (:23, :65), `prior-art.md` ×4 (:34, :69, :84, :109), `lessons/round-9.md:37` | **YES, state flag:** header **closed**; opened 2024-05-03 by @reuank; updated 2026-05-21 (@MannyKayy "reopening"; labels `bug-unconfirmed, stale`). Corpus says "reopened 2026-05-21" (`prior-art.md:34`) — commenter intent ≠ GitHub state | Re-verify state before citing "reopened"; body itself (8 slots, temp 0, seed 1234 → 5–8 unique completions; single slot deterministic) matches the corpus quote |

Trace-file line counts (for reference): `wc -l` → `eval-prior-art-calibration.md` 68, `prior-art.md` 115, `lessons/round-9.md` 61.

## 3. Freshness inventory

Exact command (as specified):
```
find ~/Projects/webzites/repos/llm-wiki/wiki -name '*.md' -newer /home/vgpnk/projects/shokunin/kengaku-shokunin/LOG.md | head -40
```
Output: **empty** (0 lines).
Widened:
```
find . -name '*.md' -not -path './.git/*' -newer .../LOG.md | wc -l            → 0
find . -not -path './.git/*' -type f -newer .../LOG.md | wc -l                 → 0
find wiki -name '*.md' -printf '%TY-%Tm-%Td %TH:%TM\n' | sort | uniq -c        → 171 files, all "2026-09-20 22:50"
stat -c '%y' .../LOG.md                                                        → 2026-09-28 18:53:43 -0300
cd llm-wiki && git log -1 --format='%h %ad %s'                                 → e66e614 2026-08-08 "Add product ship evidence for the static site pipeline."
git status --porcelain | wc -l                                                 → 0
git log --since=2026-09-01 --oneline | wc -l                                   → 0
```

**New/changed file list (the acceptance ask): EMPTY — no changed wiki files to classify.**
- Why empty, stated precisely: LOG.md (2026-09-28 18:53) post-dates every file in llm-wiki (max mtime 2026-09-20 22:50; last commit 2026-08-08; tree clean). The 2026-09-20 22:50 mtime is a wholesale touch (171/171 identical) — a checkout/rsync artifact, not edits; therefore the mtime channel carries **no** eval-relevance information for llm-wiki and any future round should use `git log`/`git diff`, never `find -newer`, on this repo.
- Eval-relevance flag for the empty list: **n/a (no entries; 0 eval-relevant additions, 0 non-eval additions).**

Standing surface (what the freshness axis cannot see, since nothing changed) — `wiki/ai` = **23 md files** (`find wiki/ai -name '*.md' | wc -l` → 23). Read-in-full per digest entries: 7 (bitter-lesson, complexity, rlhf, books ×2, scaling-hypothesis-revisited, papers/react-reasoning-acting — per `eval-theory-notes.md`/digest-2/digest-3 source lists). Remaining 16 with per-file corpus-filename census (`grep -rl <basename> corpus`):

| wiki/ai file | corpus filename mentions | eval-relevance flag |
|---|---|---|
| agents-and-engineering/benchmark-shortlist-for-godspeed-research.md | 3 (`knowledge/benchmark-selection.md`, README, `round9-fleet/INTEGRATOR-NOTES.md`) | cited → digested elsewhere |
| agents-and-engineering/godspeed-umwelt-iteration-2/-3/-3-alpha.md | 3/3/4 (`knowledge/godspeed-eval-findings.md`, `lessons/round-1-aggregator-audit.md`) | cited → digested elsewhere |
| agents-and-engineering/gemini-3.1-pro-godspeed-*.md | 2/2/0/0/0 (`knowledge/gemini-benchmark-suite.md`) | partly cited; run-1/run-2/veigapunk/physical-results unflagged |
| agents-and-engineering/weng-llm-agents.md (139 L) | 0 | **eval-relevant candidate** — agent-dimension taxonomy (planning/memory/tools) maps to probe design [INFERENCE] |
| agents-and-engineering/building-effective-agents.md (156 L) | 0 | **eval-relevant candidate** — scaffold-pattern taxonomy, adjacent to r7 scaffold-ablation [INFERENCE] |
| agents-and-engineering/anthropic-multi-agent-research.md (148 L) | 0 | **eval-relevant candidate** — multi-agent orchestration eval design [INFERENCE] |
| agents-and-engineering/autoagent.md (246 L) | 0 | candidate — tool-agent scaffold [INFERENCE] |
| agents-and-engineering/tool-ai.md (108 L) | 0 | candidate (concept note) [INFERENCE] |
| adoption-and-diffusion/guo-ai-adoption-coordination.md (108 L) | 0 | NOT eval (adoption economics) — matches the declared "beyond eval scope" ceiling |
Caveat: digest-2 describes a "25 remaining wiki files" sweep; that list is not enumerated in-repo, so the 0-mention rows are *candidates*, not proven-undigested [uncertain].

Side observation: the wiki-side queue mechanism (`state/branch-proposals.md`) is **empty** — "no pending proposals" — so there is no second queue hiding on the wiki side; the only open queue is the repo-side 3-source one.

## 4. Confidence

- Three-source queue identity + repo-side citation census: **high** (commands above, re-runnable).
- Zero traces in llm-wiki (all file types): **high** (single all-file grep; distinctive IDs/authors).
- Freshness = empty: **high** for the commands as run; the "git is the right instrument here" conclusion is **medium** (explained by 171/171 identical mtimes + clean tree at e66e614, but the checkout that stamped 2026-09-20 is inferred).
- Digest-status "none read yet" from README:84: **high as quoted**; the fetched-not-digested nuance: **medium** (`prior-art.md` asserts full-text fetch provenance I did not re-verify; my re-fetch confirms only abstracts).
- #7052 state=closed vs corpus "reopened": **high for the fetched header**, and the corpus correction is open to Main.
