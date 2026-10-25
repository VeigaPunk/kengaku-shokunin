# R27 SrcStructuredOutputs — source for E4 strict-whole rationale

Access date 2026-10-21 for all sources. Read-only seat; this file is the only write. Lane tree, git/jj state, and SOURCES.md untouched.
Axes: (1) verbatim guarantee wording; (2) fit to E4 `json.loads(raw.strip())`; (3) whether the pinned population was produced under the guarantee.

## F1 OpenAI — JSON mode guarantee (primary)
- URL https://developers.openai.com/api/docs/guides/structured-outputs, section "## JSON mode" (#json-mode), reader line 3933. The requested https://platform.openai.com/docs/guides/json-mode resolved to this page.
- Quote, 22 words, line 3933: "the model's output is ensured to be valid JSON, except for in some edge cases that you should detect and handle appropriately."
- Quote, 20 words, line 3940: "JSON mode will not guarantee the output matches any specific schema, only that it is valid and parses without errors."
- Literal "whole": absent (grep over the full reader output). Nearest, line 3941 (22 words): "Your application must detect and handle the edge cases that can result in the model output not being a complete JSON object"
- Scope: line 14 (20 words): "Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied JSON Schema." Table row 328: "Outputs valid JSON" = Yes for both modes.

## F2 OpenAI — documented exits from whole-output JSON (same page; E4 returns None on each)
- Line 3939 (21 words): "the model may generate an unending stream of whitespace and the request may run continually until it reaches the token limit." (no JSON instruction in context; raw.strip() is "")
- Lines 3968–3972 and 4030–4035: status `incomplete`, reason `max_output_tokens`, comment "resulting in incomplete JSON".
- Lines 3983–3986: status `incomplete`, reason `content_filter`: "so the generation of JSON was halted and may be partial" (11 words).
- Line 2804 (14 words): "Since a refusal does not necessarily follow the schema you have supplied in response_format"

## F3 Anthropic — second provider (corroboration)
- URL https://platform.claude.com/docs/en/build-with-claude/structured-outputs (reader .md). Literal "whole": absent (grep).
- Line 58 (9 words): "Structured outputs guarantee schema-compliant responses through constrained decoding:"; line 60: "Always valid: No more JSON.parse() errors"
- Line 76 (14 words): "Claude returns valid JSON that matches your schema in the response's text content block." Scope is the text block, not the whole response.
- Line 2702 (20 words): "While structured outputs guarantee schema compliance in most cases, there are scenarios where the output may not match your schema:"
- Line 2711 (refusal): "The output may not match your schema because the refusal message takes precedence over schema constraints". Line 2720 (max_tokens): "The output may be incomplete and not match your schema".
- Line 2725: "Structured outputs don't guarantee the capitalization of string enum and const values": the guarantee is grammar-level, not semantic.

## F4 RFC 8259 — what E4's strip admits
- URL https://www.rfc-editor.org/rfc/rfc8259, §2, reader lines 214 and 231–237. Quote (14 words): "Insignificant whitespace is allowed before or after any of the six structural characters." Grammar: `ws = *( %x20 / %x09 / %x0A / %x0D )` (comments elided).
- Local check (stdlib json, exercised): `json.loads` rejects "\x0c{...}", "\xa0{...}", "\x0b{...}"; `json.loads(s.strip())` accepts all three. json's own WHITESPACE is `[ \t\n\r]*`. Pre-registered E4 is therefore looser than an RFC 8259 whole-text parse on non-RFC whitespace.
- Population census (structural, raw strings only, no verdicts): 1964 raw+ok records; records where `raw.strip()` differs from `raw.strip(" \t\n\r")`: 0. The looseness is inert on the pinned inputs.

## F5 Population provenance — no constrained decoding requested
- Pins: plans/grader_perturb.py:29–34 (4 JSONL files): 6139 non-empty JSON lines, 1964 raw+ok, 0 unparseable.
- 56 distinct top-level keys. Exact-key counts 0: response_format, json_object, json_schema, output_config, output_format, text_format, response_mime_type, structured, strict, text, format, mode. Substring scan (format, schema, json, structur, response_f, output_c): only models_json (a descriptor line).
- Request bodies: `{"model": "local", "messages": [...], "temperature": TEMP, "max_tokens": MAXTOK}` at corpus/evidence/round8-horizon/horizon.py:22-23, round9-replication/replicate.py:22-23, round11-power/probe_r11.py:31-32, round12-ladder/probe_r12.py:35-36.
- Grep of corpus/evidence/**/*.py|*.md|*.sh (gitignore off; 21 files hit): every hit is max_tokens, temperature, finish_reason, or prose. None is a request-mode parameter.
- Responses are not uniformly whole-output JSON: format_class FJ1/FJM/MULTI/DANGLE/BARE (grader_perturb.py:54–62); corpus/evidence/round9-fleet/probeA.md:124 notes bare JSON without a fence. Local check: a fenced response makes json.loads raise JSONDecodeError.

## Implication for the E4 rationale [INFERENCE]
- Both vendors guarantee whole-output JSON only for requests that enable a constrained mode, and both document exits. The population requested no mode, so vendor guarantees cannot justify treating these 1964 responses as whole JSON.
- E4 is defensible as the consumer contract for constrained outputs: there it matches the documented guarantee except at the listed exits, which E4 maps to None. On prompt-only outputs, E4 measures strictness, not validity.
- Suggested wording for the C1 knowledge entry: "E4 implements the whole-output contract providers document for JSON mode; the frozen population was produced without that mode, so E4 is a policy comparison, not a validity claim about the responses."
- Not established: that any evaluation harness implements E4 (the claims file's "harnesses actually implement" needs its own rows; lm-eval, inspect_ai, and OpenAI simple-evals were not checked here). The local endpoint is covered by no source opened here.

## Rows and tooling
- SOURCES.md: no existing row for OpenAI JSON mode/Structured Outputs, Anthropic structured outputs, or RFC 8259 (grep: only S005/S006 OpenAI eval posts and S023/S026 Scale). Candidate rows for the integrator, not written here: OpenAI (F1–F2), Anthropic (F3), RFC 8259 (F4); next id S049.
- Installs: none. Tools: reader, grep, glob, eval kernel (stdlib json only). No lane writes; no network beyond the public pages above.
- QA: one xd://report_issue note (eval census printed keys out of sorted order; F5 counts re-run and unaffected).

VERDICT: Vendors guarantee whole-output JSON only under constrained request modes with documented exits; the pinned population used no such mode, so E4 needs a consumer-contract rationale, not a validity claim.
