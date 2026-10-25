# Round-1 aggregator corpus audit — kengaku

Auditor: aggregator L1 (m_qwen) + one independent L2 `reviewer` lane
(m_composer), 2026-09-28. Method: re-executed cited greps/counts against
`/home/vgpnk/Projects/webzites/repos/llm-wiki` and
`/home/vgpnk/.bailian/skills/bailian-docs-llm-wiki/models/`. Scope: `corpus/`
only; lane-owned `SKILL.md`/`LOG.md`/`PROVINCE.md` were not edited — defects are
filed here.

Round evidence: `LOG.md` round-1 entry; commits `90a5ce8` (skill) and `24ff62e`
(corpus); lane report
`~/projects/shokunin/.ufo/reports/round-1/kengaku-shokunin.md`.

## Verdict: NOT conformant — structure sound, two citation defects

Layout, index, coverage map and known-gaps sections all satisfy `CORPUS.md`;
every knowledge entry carries `Source:`; `lessons/round-1.md` cites round,
commit, LOG and report; `godspeed-eval-findings.md` correctly marks its
`## Opinion` block. The failures are citation-level, which `CORPUS.md` treats as
hard ("`knowledge/` entries cite a source"; "no unverifiable claims").

## Independently re-verified

| Claim | Command | Observed |
|---|---|---|
| `~/wikillm/llm-wiki` absent | `test -e /home/vgpnk/wikillm/llm-wiki` | missing ✓ (path correction in SKILL.md is real) |
| 5 cited wiki pages exist | `test -e` each under `wiki/ai/agents-and-engineering/` | all present ✓ |
| 125 agents / 21 experiments | `grep '~125 agents' godspeed-umwelt-iteration-2.md` | line 21 ✓ |
| RMSE 135,367 → 117,791 (~13%) | `grep -E '135,367\|117,791\|13%'` same file | table lines 39–40; "approximately 13%" line 35 ✓ |
| K2 clean split 0/3 vs 3/3 | `grep '0/3'` same file | line 135 ✓ |
| T2 review gradient 7→9→13→17→19 | `grep '7 → 9 → 13 → 17 → 19'` | line 125 ✓ |
| MCP-Atlas 36 servers / 220 tools / 1,000 tasks | `grep 'MCP-Atlas' benchmark-shortlist-…md` | line 54 ✓ |
| SWE-Bench Verified retired 2026-02-23 | `grep '2026-02-23'` shortlist | lines 8, 39 ✓ |
| 180 families / 413 models / generated 2026-09-11 | `wc -l families.jsonl models.jsonl` + `index.md` header | 180 / 413 / 2026-09-11 ✓ |
| model row specs (e.g. kimi-k2-thinking ctx 262144, out 16384) | JSON parse `models.jsonl` | matches ✓ |
| wiki size 402 files / 342 markdown | `find … -type f \| wc -l`; `find … -name '*.md' \| wc -l` | 402 / 342 ✓ |
| 36–40 run floor | `grep '36 to 40 runs'` alpha note | line 272 ✓ |
| 10 telemetry fields | alpha note Phase 0 list | 1–10, matches `telemetry-run-design.md` ✓ |
| tool-call delta ~1.5× | iteration-2 effect-size table | ~1.5× (line 139) and +50% (line 129) — consistent ✓ |

## Defects filed

1. **Mis-attributed source (hard failure).**
   `knowledge/telemetry-run-design.md` lines 20–21 credit the per-run artifact
   triple `response.md` + `telemetry.json` + `judge.json` to
   `godspeed-umwelt-iteration-3-alpha-shittycodex.md`;
   `grep -n 'response.md' <that file>` → **0 hits**. The filenames live in
   `wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3.md:156`. Fix:
   re-point the `Source:` line, or drop the filenames from an alpha-only
   citation.
2. **Dangling example paths in the index.** `corpus/README.md` "Known gaps"
   cites `wiki/karpathy/creative-benchmark` and `wiki/ai/books/
   are-we-smart-enough`; neither exists. Actual:
   `wiki/karpathy/gwern-essays-llm-and-ai-reasoning/creative-benchmark.md` and
   `wiki/biology/books/are-we-smart-enough.md`. Illustrative paths are still
   claims — `CORPUS.md` gives index rows no exemption.
3. **`PROVINCE.md` still names a path that does not exist** (lane-owned, filed
   here for the lane): "scopes `~/wikillm/llm-wiki`" while `SKILL.md`
   frontmatter was corrected to `~/Projects/webzites/repos/llm-wiki`.
   `PROTOCOL.md` promotion gate requires "`PROVINCE.md` still matches reality";
   this blocks a shonen→shokunin review until fixed.

## Gaps for the next round

- Digest `gemini-3.1-pro-godspeed-benchmarks.md` and
  `gemini-3.1-pro-godspeed-test-battery.md` into `knowledge/` — the lane report
  says both were read, but no corpus entry carries them.
- One **executed** evaluation (or a link to run artifacts). The README already
  files this; without it `SHONEN.md` box 2 (end-to-end domain task) stays open.
- A route/provider telemetry entry grounded in real harness artifacts (e.g.
  `~/.bailian/telemetry.jsonl`) rather than wiki prose.
