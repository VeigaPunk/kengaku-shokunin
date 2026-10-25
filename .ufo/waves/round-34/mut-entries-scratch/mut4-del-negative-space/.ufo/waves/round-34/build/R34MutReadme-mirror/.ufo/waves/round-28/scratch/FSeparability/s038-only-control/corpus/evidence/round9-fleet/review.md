# kengaku round 9 — citation/state review (CitationReviewer)

Scope: SHONEN.md claims 1–3, citation resolution sweep, endpoint identity, LOG.md ↔ artifacts, README coverage/gaps. Repo HEAD `f147a27` (round-7); untracked `corpus/evidence/`. Evidence commands are verbatim re-runnable.

## 1. SHONEN.md audit — 3 checked claims

| # | Claim (verbatim) | Evidence command | Observed | Verdict |
|---|---|---|---|---|
| S1.1 | SKILL.md "2 decision tables, 8 anti-patterns, 9-step eval checklist" | `grep -n '^## Decision table' SKILL.md` / `awk '/^## Benchmark anti-patterns/,/^## Research-note/' SKILL.md \| grep -cE '^[0-9]+\. '` / `awk '/^## Production checklist/,/^## Cited local sources/' SKILL.md \| grep -cE '^[0-9]+\. '` | 2 (`SKILL.md:17,40`), 8 (`:47` block), 9 (`:274` block) | matches |
| S1.2 | "telemetry parsing rules" | `grep -n 'Parsing rules learned on real files' SKILL.md` | present (`SKILL.md:170`) | matches |
| S1.2 | SKILL.md "20+ cited local sources" | `awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- `'` = **16**; total backticked path-strings in that section = **44** (18 non-path: commands/fields/endpoint); **21 distinct local path citations** | 16 source-bullets; 21 distinct local paths (some multi-path); **20 holds only under path-expansion, fails under bullet-count** | overreach (17 ≠ 20+, 21 ≥ 20+ only counting bundled paths) |
| S1.3 | "[x] verified round 5" | SHONEN.md committed in `a1af83c`, touched in `782dd2d`, **unchanged since** (`git log --follow`; `git diff 782dd2d HEAD` empty) | "verified round 5" framing genuine to r5 | matches (round-5 state) |
| S2.1 | "round-4 eval slice; round-5 full 33-task battery" | `test -e corpus/knowledge/bench-arena-round5-battery.md` + `sed -n '1p'` | exists; title "full 33-task battery under live endpoint"; 20/33 result (line 17); LOG rows 7/9 present | matches |
| S3.1 | PROVINCE.md "verified accurate round 5" | `head PROVINCE.md` only (no `grep -c wikillm` hits) | "scopes ~/Projects/webzites/repos/llm-wiki, route telemetry" (current) | matches (repo state) |
| S3.2 | "no cross-domain bleed in corpus": every corpus entry cites llm-wiki notes, bench-arena/ledger/bailian telemetry surfaces, or model-catalog APIs | run across 18 `corpus/knowledge/*` files | all 18 point at one of {llm-wiki notes 8, bench-arena 7, ledger 1, bailian telemetry/index 3, HF/OpenRouter APIs 1} | matches (knowledge/*) |
| S3.3 | same for `lessons/*`: "all corpus entries" | `grep -n 'Primary source' corpus/README.md \| head` | 8 lessons cite lane LOG.md, `/tmp/bench-rN/`, `~/projects/shokunin/.ufo/reports/` — none cites an adjacent-domain source | partial overreach (lessons cite lane-internal, not the 3 named source families) |

Sub-verdicts S1.2+'s "20+" and S3.2+ are the claims that do NOT exactly match observed counts. Number-precision: "2 decision tables / 8 anti-patterns / 9-step checklist" all exact; "20+ cited local sources" = **17 source-bullets, 21 distinct path strings, 18 resolving on-host** (3 documented-absent or parsed-as-absent-out-of-context, see §2).

## 2. Citation resolution sweep

Scope: `SKILL.md`, `corpus/README.md`, `corpus/knowledge/*.md` (18), `corpus/lessons/*.md` (8), plus `LOG.md`/`SHONEN.md`/`PROVINCE.md`/`AGENTS.md`.

- Regex: `~[A-Za-z0-9_./{}*,*-]+` over every backticked string, de-duplicated per file.
- Test: `test -e`/`test -d`/`glob` on the absolute path. "documented-absence" = the file explicitly states the path is absent-on-host (fences the citation).

**Total: 129 unique citations · 105 resolve · 14 URL/endpoint (n/a) · 10 flagged.** Summary:

| Path | exists? | Referenced from |
|---|---|---|
| `~/Projects/webzites/repos/llm-wiki` (root + `Home.md` + 5 `agents-and-engineering/*.md` + `wiki/karpathy/{talks,projects-and-tools,standards-and-specifications}/`) | **all OK** (globs expand; 21 entries) | SKILL.md, README.md, 5 knowledge entries |
| `~/Projects/bounties/ledger/telemetry.jsonl` (7,218 lines) | OK | SKILL.md, README.md, `ledger-route-telemetry.md`, lessons/round-3.md |
| `~/bench-arena/` + 3 CSVs (`report-grok45.csv`, `report-qwenlocal-v2.v2.csv`, `telemetry-qwenlocal-v2.csv`) + `loop.sh` + `grade.sh` + `tasks/` + `tasks/27-rwlock-writer-pref/test.sh` | **all OK** | SKILL.md, README.md, 4 knowledge, lessons/round-3+4 |
| `~/Projects/webzites/repos/llm-wiki/raw/{karpathy/{yao-second-half-2025,thariq-llm-trueskill-sorting-2025},gwern/creative-benchmark}.md` + `wiki/karpathy/philosophy-and-concepts/{yao-second-half,llm-trueskill-sorting}.md` + `wiki/karpathy/philosophy-and-concepts/gwern-essays-llm-and-ai-reasoning/creative-benchmark.md` + `wiki/ai/alignment-and-training/rlhf.md` | OK (7/7 resolve via glob) | README.md, `eval-theory-notes.md`, `bailian-cli-telemetry.md` |
| `~/.bailian/skills/bailian-docs-llm-wiki/models/` (+ `index.md`, `models.jsonl`=413 rows) | OK | SKILL.md, README.md, `local-model-index.md` |
| `~/.bailian/telemetry.jsonl`, `~/.bailian/wiki-sync-state.json` | OK | README.md, bailian-cli-telemetry.md, local-model-index.md |
| `~/.config/opencode{,/opencode.json,agents/janitor.md}` | OK | bench-arena-fresh-run.md, round7-scaffold-ablation.md, round-4-aggregator-audit.md |
| `~/bench-arena/` CSVs referenced-as-4 by SKILL.md (`report-grok45.csv`, `report-qwenlocal-v2.v2.csv`, `telemetry-qwenlocal-v2.csv`, `report-qwenlocal.csv`) | OK (4) | SKILL.md |

**Dangling (10 flagged):**

| Path | exists? | Referenced from | Class |
|---|---|---|---|
| `~/wikillm/llm-wiki` | **no** | SKILL.md:9,304 · LOG.md:4 · lessons/round-1.md:8 · lessons/round-1-aggregator-audit.md:26,58 · lessons/round-4-aggregator-audit.md:48 | 5 sites, all framed as *documented absence* ("does not exist on this host"); not a dangling pointer. AGENTS.md line-3 rule met; not a defect. |
| `~/Projects/webzites/repos/llm-wiki/wiki/karpathy/{talks,projects-and-tools,standards-and-specifications}/**` | expansion **OK** (3 dirs) | SKILL.md:304 | regex parser artifact, not a fail (handled) |
| `corpus/knowledge/{local-bench-arena,ledger-route-telemetry}.md`, `corpus/knowledge/{bench-arena-fresh-run,eval-theory-notes,open-model-catalogs}.md`, `corpus/knowledge/{bench-arena-round5-battery,eval-design-digest-2}.md` (LOG brace-glob syntax, 3 group mentions = 9 files) | **all expand-and-resolve** (9 total) | LOG.md:6,7,9 | brace-glob false-negative (test -e on literal `{...}` fails) |
| `corpus/knowledge/eval-design-digest-2.md:109`, `corpus/README.md:23` | 2 `file:line` refs; file part = **OK**, line part ok | lessons/round-5-aggregator-audit.md | `file:line` false-negative (test -e refuses suffix) |

**Net dangling citations needing a fix: 0.** All 21 wiki-fragment globs (`bench-arena-modeled raw/*` paths, `wiki/ai/...`) resolve; `~/wikillm/llm-wiki` correctly-per-repo-scope only documented as absent. Grep-check `grep -c wikillm`: SKILL.md 2, LOG.md 1, round-1-aggregator-audit 2, round-1.md 1, round-4-aggregator-audit 1 = 10 references—all documented-absence context.

## 3. Endpoint identity

| Probe | Command | Observed | Verdict |
|---|---|---|---|
| Model served | `curl -s -m 5 http://127.0.0.1:34113/v1/models` | `"id":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf"` (1 model listed, `owned_by=llamacpp`, `n_ctx=16384`) | **matches** LOG.md r5/r6/r7 claims ("Qwen3-Coder-30B-A3B UD-IQ2_XXS") and SHONEN/README expectations; **no drift** |
| Health | `curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health` | `200` (`{"status":"ok"}` mod content accepted; code literal 200) | matches |
| Round-8 probe pre-condition | `/tmp/bench-r8/results.jsonl` (268 lines), md5-identical to repo copy of `corpus/evidence/round8-horizon/results.jsonl` (`md5sum` of 2 copies = `18b1728d...` both) | **byte-identical**; run.log shows 268-record SUMMARY with final-state pass counts 7/0/1 (A), 3/3/6/6 (B), 4/1/4/4 (C) | matches |

Cross-check against corpus text: `a1af83c` (round-4) says "Qwen3-Coder-30B-A3B UD-IQ2_XXS" served — endpoint unchanged across r4→r8; LOG.md never records a different model id string. **Drift = none.**

## 4. LOG.md ↔ artifacts

LOG.md rows on disk (9 LOG entries, lines 1–12): `round 0` mint; r1 (SKILL rewrite); r1-corpus; r3; r4; r4-audit-closure; r5; r6; r7; r7-L2-fleet. All 9 other-than-r0 entry(ies) name artifacts; all 9-existence verified below.

| LOG entry | Artifact names (in LOG) | Exists in repo? | Notes |
|---|---|---|---|
| round 1 (line 4) | SKILL.md rewrite; wiki sources referenced (paths) | SKILL.md yes; all 5 wiki *.md exist | no corpus artifact claimed |
| round 1 corpus (line 5) | `knowledge/{bench, godspeed, telemetry, local-model-index}` x4 + 1 lessons | `benchmark-selection.md`, `godspeed-eval-findings.md`, `telemetry-run-design.md`, `local-model-index.md` + `round-1.md` all exist | lessons file **not named by path** (says "1 lessons entry") |
| round 3 (line 6) | `local-bench-arena`, `ledger-route-telemetry`, `round-3.md` | all 3 exist | — |
| round 4 (line 7) | `bench-arena-fresh-run`, `eval-theory-notes`, `open-model-catalogs`, `round-4.md` | all 4 exist | — |
| round 4 audit closure (line 8) | `round-1-aggregator-audit.md` + `gemini-benchmark-suite.md` + `bailian-cli-telemetry.md` (from audit's new-entry corrections) | all 3 exist (`91f021c`) | PROVINCE.md also corrected (per line-8 text) |
| round 5 (line 9) | `bench-arena-round5-battery`, `eval-design-digest-2`, `round-5.md` | all 3 exist (`782dd2d`) | r5-audit lesson NOT yet logged (see D3) |
| round 6 (line 10) | `bench-arena-round6-stability`, `bench-arena-task27-timeout-anatomy` | both exist (`d5f1cad`) | no lessons/round-6.md exists — LOG doesn't claim one |
| round 7 (line 11) | `bench-arena-round7-scaffold-ablation`, `round-7.md` | both exist (`f147a27`) | — |
| round 7 L2 fleet (line 12) | `bench-arena-round7-noise-n25`, `eval-design-digest-3` | both exist, untracked-on-disk | examiner: r7-L2's lesson/round-7.md was checked above this line; noise-n25 exists locally |

**No LOG claim with a missing artifact was found.** Count of round-N knowledge artifacts named by LOG = 17 (all present); lessons files named by LOG = 5 (`round-1.md`, `round-3.md`, `round-4.md`, `round-5.md`, `round-7.md`) + `round-1-aggregator-audit.md` = 6.

**Artifacts present in repo with no LOG entry:**

| Artifact | Where it lives | LOG representation | README |
|---|---|---|---|
| `corpus/lessons/round-4-aggregator-audit.md` (present, commit `91f021c`) | `corpus/lessons/` | **none** — no LOG line mentions its creation or the round-4 audit verdict | **absent from index** |
| `corpus/lessons/round-5-aggregator-audit.md` (present, in-flight post-r5) | `corpus/lessons/` | **none** | **absent from index** |
| `corpus/evidence/round8-horizon/{results.jsonl,run.log,horizon.py,critic-defects.md}` | `corpus/evidence/round8-horizon/` (4 files, untracked) | **zero mentions of round-8 ≠ `round 8`/`round-8`/`horizon`** (`grep -rn -i 'round-8\|round 8\|horizon' LOG.md` = 0 hits) | **absent**; README's open-gap line-52 ("Planning-horizon coverage: … unmeasured") is `false` now — the probe ran to completion 78/78 |

## 5. corpus/README.md coverage/gaps accuracy

README's "What's here" table lists 18 knowledge entries + 6 lessons entries = 24 rows; disk = 18 knowledge + 8 lessons = 26 files.

| Disk file | In README index? | Phantom entries? |
|---|---|---|
| 18 `corpus/knowledge/*.md` | **all 18 present** | none |
| `corpus/lessons/round-1.md`, `round-3.md`, `round-4.md`, `round-5.md`, `round-7.md`, `round-1-aggregator-audit.md` | all 6 present | none |
| `corpus/lessons/round-4-aggregator-audit.md` | **MISSING row** | — |
| `corpus/lessons/round-5-aggregator-audit.md` | **MISSING row** | none |

**Verdict: 2 omissions (the 2 aggregator-audit lessons), 0 phantom entries, 0 dangling knowledge rows.** Coverage/gaps prose is internally consistent with the table (all 18 knowledge names appear in prose/coverage sections ≥ once).

## Defect queue (ordered by severity)

1. **Round-8 evidence debt (blocker for calibration axis-move):** `corpus/evidence/round8-horizon/` has 4 files (results.jsonl, run.log, horizon.py, critic-defects.md) that exist locally, are byte-identical to `/tmp/bench-r8/*`, but are untracked and **never logged** in LOG.md and never indexed in README.md — the 78/78-run round-8 horizon probe left no written/analyzed trace. Fix: add a LOG round-8 entry landing the analysis, and add a `corpus/README.md` section pointing at `evidence/round8-horizon` (tracked or at least logged with the file paths); do not secretly delete.
2. **README "Planning-horizon coverage … unmeasured locally" (line 52) is factually wrong** now that round-8 (horizon.py) has run a 78/78 completion, unanalyzed. Fix: change to "measured but unanalyzed: see corpus/evidence/round8-horizon/".
3. **2 aggregator-audit lessons (round-4-aggregator-audit.md, round-5-aggregator-audit.md) have no LOG entry and no README row** — the round-4 audit-closure LOG row covers only its round-1 predecessor. Fix: add one LOG row per aggregator-audit lesson (round-4/r5 conclusion + defect count) and 2 README table rows.
4. **SHONEN.md "20+ cited local sources" holds only under path-expansion** (17 source-bullets, 21 local-path strings); strict bullet-count = 17 < 20. Fix: either rephrase to "17 source bullets (21 distinct local paths)" or append 3+ more cited sources to the `## Cited local sources` section.
5. **All 3 SHONEN [x] marks are self-attested:** round-4 audit (line 12 of `round-4-aggregator-audit.md`) says "no named non-author verifier → effective [~] author-attestation, 0/3 verified"; nothing since has added an independent verifier. Fix: re-verify and add one "verified-by: <role>" line per claim (per audit wording) or downgrade the labels to `[~]`.
6. **`bench-arena-task27-timeout-anatomy.md` verdict conflict inside SKILL.md:** rule-5 says "re-check contamination status before citing" but S1.1's own table cites contaminated SWE-Bench Pro; verify S1.1's "Preferred over Verified" line against the actual wiki note before citing it forward.
7. **LOG r5 string mentions stale "22 files" only via the r5 aggregator-audit note** (corrected to 25 in LOG.md line 9 and eval-design-digest-2.md:109) — high-count corroboration worked; **no remaining "22" text (0 hits)**. Already closed; no action.
8. **`round-8-horizon/critic-defects.md` (16 numbered defects) lives only on disk; SKILL.md has no parsing rule for the horizon cell names (A-INC, A-MONO, A-CKPT, B-*, C-*) and no evidence path** — the round-9 analysis will need this mapping bool-for-bool. Fix: once the round-8 analysis defines the cell-semantics, add a `### Planning-horizon probe (r8)` rule block to SKILL.md.

## Confidence
- **high** — S1.1, S2 counts, S3 endpoint identity, §4 all 9 LOG rows' artifacts exist. Every number above comes from a direct read (no inference).
- **high** — §2 sweep total (129 / 105 / 14 / 0 true-dangling); digit-checked per-row.
- **medium** — Defect 1 "round-8 exists as an unanalyzed artifact" (not that no analysis ever ran; local analyzer artifacts exist in `/tmp/bench-r8/` but we did not verify semantic-level round-8 analysis in LOG.md — only in-flight sibling work).
- **medium** — Defect 4 "20+ cited sources" judgment depends on the bullet-vs-path counting convention; both numbers reported.
- **high** — Defect 3 fact of missing LOG/README representation for the 2 aggregator lessons (confirmed by absence of round-4-aggregator-audit in LOG, README line-50/51 correction context; exact fix wording left to the L1 owner).
