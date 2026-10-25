# Kotoba overlap scan — round 26

Axes: novelty (owned; mapped to coverage/constructs); calibration (no change claimed).

## Evidence
- `plans/round-26-claims.md:37-44,54-73`: C1 measures stored-response verdict invariance/sensitivity under raw-response transformations; it does not perturb prompts. Its target is `extract_json_block` plus the response graders.
- `grader.py:121-134`: extraction prefers the last matching fenced block, then the last parseable brace/bracket candidate. This is grader behavior, regardless of which convention the model was asked to follow.
- `corpus/evidence/round12-ladder/probe_r12.py:31-37`: the probe system prompt says, “Reply with exactly one fenced ```json code block and no other text — unless the user asks you to reply 'ok'.” The particular response-format convention is therefore visible in a model-output prompt, but is outside C1’s transformed variable (`raw`).
- Kengaku `SKILL.md:3`: “kotoba owns prompt and skill craft (kengaku keeps only measured capability effects)”; Kengaku’s `SKILL.md` remains owned by Kengaku.
- Kotoba `PROVINCE.md:3-6,27-30`: owns “prompt & skill craft” over SKILL.md/AGENTS.md quality and dispatch-prompt craft; refuses other domains and lists “kengaku — LLM/model evaluation and route telemetry” as sibling-owned.
- Kotoba `SKILL.md:4-12`: covers dispatch/system prompts “for trigger fidelity and decision density,” but explicitly anti-triggers “general prompt engineering for model outputs (not skill files)”; it says the five domain skills, including kengaku, own their SKILL.md and fixes route to the owning lane.

## Boundary and one bounded move
The C1 family outcomes themselves (including fence stripping/relabeling, prose, and competing fenced blocks) stay Kengaku findings: they measure parser/grader dependence, not prompt quality. Route to Kotoba only a separately evidenced defect in a named prompt/skill-craft surface—e.g. an authored SKILL.md/AGENTS.md/dispatch prompt whose format instruction is unclear or contradictory—for craft audit/reporting. Do not route generic output-format tuning in the probe system prompt to Kotoba under its explicit anti-trigger; do not transfer ownership of Kengaku’s own SKILL.md. This keeps the novelty construct clean and leaves calibration unscored.

Explicit scope tension: Kotoba’s capability clause includes “system prompts” (SKILL.md:4-5), while its anti-trigger excludes general model-output prompt engineering (SKILL.md:8-9). The probe’s fenced-JSON instruction is the latter, not a skill/dispatch-craft finding absent further evidence.

Risk: tightening the output prompt to force fences could conceal a brittle extractor rather than repair or measure it; changing prompt and parser together would confound the registered C1 construct. No C1 family result is asserted by this connector report.

Verification: when C1 results exist, verify each reported failure against its transformed `raw` and `grader.py:121-134`; route only a separately cited instruction-surface defect, not a parser result. No tests/builds run; no installs.

VERDICT: Keep response-format dependence of the grader in Kengaku; send only a proven prompt/skill-craft defect on a named instruction surface to Kotoba, subject to its model-output anti-trigger.