ATTACKS: D18 — kengaku SKILL.md frontmatter YAML-parse, PROTOCOL.md:429 elements, sibling-boundary cross-check
SEAT: KengakuR25.RevFrontmatter · tip 8ea41f9ed · worktree==tip (`git show 8ea41f9ed:SKILL.md | diff - SKILL.md` → empty)

## Findings

F1 [PASS — parses] `python3` + PyYAML 6.0.3 `yaml.safe_load` on the `---` block → keys `['name','description']`, description type str, len 875, `name: kengaku-shokunin` == repo dir. No anchors/aliases/merge keys.
F2 [PASS — quoted triggers] SKILL.md:3: description is a double-quoted YAML scalar; all six triggers single-quoted verbatim (`'model evaluation'`…`'novelty pricing'`); round-trip via parser returns all six as plain strs. Quoting is load-bearing: mutation (strip outer double quotes in /tmp/k25w2-RevFrontmatter copy) → `yaml.scanner.ScannerError: mapping values are not allowed here` (the `Triggers: ` colon). Satisfies PROTOCOL.md:429 "quoted trigger strings".
F3 [PASS — anti-trigger] SKILL.md:3 `Anti-trigger: not serving-flag changes, endpoint remediation or model-serving config` — present per PROTOCOL.md:429.
F4 [PASS — sibling arbitration] SKILL.md:3 `Sibling arbitration: kotoba…; kumitate…; kama…; chousa…; tameshi…` — present per PROTOCOL.md:429.
F5 [PASS — trigger collisions] `grep -rn "<six triggers>" */SKILL.md | grep -v kengaku` → 0 hits across all sibling repos; no misroute vector.
F6 [PASS — kotoba] Claim "kotoba owns prompt and skill craft": kotoba-shokunin/SKILL.md:4-6 "Prompt & skill craft — audits, writes, and rewrites SKILL.md / AGENTS.md / dispatch prompts…" ✓; kotoba PROVINCE.md:29 routes "kengaku — LLM/model evaluation and route telemetry" ✓ reciprocal.
F7 [PASS — kama] Claim "kama owns local endpoint health and identity": kama-shokunin/SKILL.md:3 "local model serving & endpoint health … model-id reconciliation"; kama PROVINCE.md owns-row "served-model-id reconciliation", Refuses "model quality/eval (kengaku)" ✓ reciprocal; kengaku's anti-trigger (F3) mirrors it.
F8 [PASS — chousa] Claim "chousa owns research method": chousa PROVINCE.md:3-9 Owns "question framing; source hierarchy; citation chaining; claim-vs-source verification"; Refuses "model-quality or evaluation claims (→ kengaku)" ✓ reciprocal.
F9 [PASS — tameshi] Claim "tameshi owns verification-fixture craft": tameshi-shokunin/SKILL.md:3 verbatim "verification-fixture craft"; PROVINCE.md:14-18 reusable craft, refuses endpoint health → kama ✓.
F10 [LOW — kumitate asymmetric] Claim "kumitate owns OMP route resolution and fallback policy": kumitate PROVINCE.md (28 lines) has ZERO hits for route/fallback/kengaku; SKILL.md:3 domain line says "OMP task/hub dispatch, ufo-fsd scripts, crates/ufo-core-runtime" — neither phrase appears as an owned boundary; its Adjacent band routes kama/kotoba/chousa but omits kengaku (no "model eval → kengaku" refusal). Not contradicted — route resolution/fallbackChains are core kumitate subject matter (kumitate SKILL.md:204-206 "global OMP config is the SOLE routing authority", :292-293 `retry.fallbackChains`; S5 routing registry) — but kengaku asserts a boundary kumitate's own docs never state. Only sibling of the five without a reciprocal kengaku clause.
F11 [corroboration] SKILL.md:3 `Rank: shonen` == MANIFEST.json roster kengaku rank "shonen".

## Residual risk / gaps
- Single YAML parser (PyYAML 6.0.3); a second parser (js-yaml) not run — npx install skipped, low value: scalar is plain double-quoted, no parser-specific constructs.
- `tameshi-shokukin/` (empty, no SKILL.md) exists fleet-side; kengaku's "tameshi" unambiguously resolves to tameshi-shokukin's roster sibling tameshi-shokunin — no kengaku-side defect.
- F10 is an under-specification on kumitate's side; kengaku cannot fix a sibling's PROVINCE (lane write scope), so no lane action implied.

VERDICT: SURVIVES — frontmatter parses, carries quoted triggers + anti-trigger + sibling arbitration per PROTOCOL.md:429; 5/5 boundaries non-contradicted, 4/5 explicitly reciprocated (kumitate soft gap, F10).
INSTALLS: none (PyYAML 6.0.3 already present; no tools installed).
