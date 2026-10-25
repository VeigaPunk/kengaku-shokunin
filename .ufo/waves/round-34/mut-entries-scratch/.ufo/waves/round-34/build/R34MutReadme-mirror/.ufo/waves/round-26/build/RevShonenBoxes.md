# RevShonenBoxes — read-only review

Scope: SHONEN pointers at the frozen P3 base `f11bffbf` (also checked the pre-registration commit `e0037a8`); content, not line-range validity. Axes: calibration; this is a content-pin review, not a score change.

## Findings
- **MEDIUM — box 4 is not wholly accurate at base** (`SHONEN.md:11-12`). Its target `PROVINCE.md:129` is `### Adjacent`; lines 131+ route adjacent ownership, but do not substantiate the broad “PROVINCE.md still accurate” clause. More importantly, `PROVINCE.md:112` says 25 registry rows and `:119` says 37 after round 25, while frozen `corpus/SOURCES.md:23-64` contains S001–S042 (42 rows). Keep this box partial until the count assertion and supporting pointer are refreshed; this is a stale-content finding, not evidence of cross-domain bleed itself.

## Pointer audit and P3c content-token proposal
- `SHONEN.md:5-6` → `SKILL.md`: **accurate**. Base content includes `## Decision table — benchmark selection` (`SKILL.md:23`), `## Benchmark anti-patterns` (`:60`), `## Production checklist — running an eval` (`:568`), and `## Cited local sources` (`:611`). Pin these four tokens so each part of the checklist claim is guarded.
- `SHONEN.md:7-8` → `LOG.md:7`: **accurate**. Tokens: `ran 4-task slice (01,02,03,05)`, `repo grade.sh`, and `1/4 PASS vs ex-ante predicted 2/4`. This records an executed and graded domain task.
- `SHONEN.md:9-10` → `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`: **accurate as a pointer**. Exact target token: `## Box-3 verdict`. Also pin the next line’s `**[x]**` outcome (`:49`): it reports the cold execution and supports completion, whereas the heading alone is only an identity token.
- `SHONEN.md:11-12` → `PROVINCE.md:129`: literal target token is `### Adjacent`, but that token is **not sufficient evidence for box 4**. Pin it for target identity only; additionally pin `:112`’s `25 rows`, `:119`’s `holds 37 after round 25`, and the frozen SOURCES IDs S001–S042 as a consistency check. Do not freeze 37 as a correct expected count.

The first three pointers still land on relevant content at both reviewed bases. Their current `[~]` markers appear conservative: if `[~]` means partial, consider refreshing boxes 1–3 to `[x]`; the cited content supports them. Box 4 should remain partial pending correction.

## Residual risk and verification gaps
- P3c token matches can detect content drift, but cannot alone establish that a claim is true; box 4 needs the cross-file count consistency check above.
- `lsp` status/references/definition/diagnostics were unavailable: `read xd://lsp` returned “No such tool.” Used literal search only for SKILL headings and the registry census, then checked the cited text with `read`; no semantic proof is attributed to grep.
- No tests/builds run (read-only assignment). Installs: none.

VERDICT: First three pointers are content-accurate; box 4’s PROVINCE accuracy claim is stale at base and needs corrected evidence before completion.