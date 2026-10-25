# FPolicyE2 — independent E2 extraction-value falsification

Seat: `KengakuR27.FPolicyE2`; reviewer, **not candidate writer KengakuR27**.
Axes: novelty (legacy novelty 7 → canonical coverage/constructs) and calibration.

## Scope and frozen sources

- Observed private-clone base: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`. Command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FPolicyE2 && git -C /tmp/kengaku-r27-FPolicyE2 switch -c r27-FPolicyE2 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FPolicyE2 rev-parse HEAD`; output: clone done, switched to `r27-FPolicyE2`, `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`; exit 0.
- Frozen contract: `plans/round-27-claims.md:39,47-48,162-163` — E2 is last parseable non-overlapping `BARE_RE` match from the original raw response, including matches inside fences. Pattern/pins/population loader: `plans/grader_perturb.py:28-36,187-256`.
- Candidate implementation: `plans/parser_policy_compare.py:48-53,75-76` reverses `gp.BARE_RE.findall(raw)`, returning the first candidate `json.loads` accepts; E2 dispatch delegates to it. Candidate entry states the same E2 semantics at `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:36` and disclaims general-parser equivalence at `:44-50,72-73,100-109`.
- Read the whole 110-line draft at `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (including a raw reread of truncated source-metadata line 1). Proposed canonical `corpus/knowledge/extraction-policy-comparison.md` was not found at this base; this report does not imply admission.
- LSP availability: first attempted `read xd://lsp`; tool returned `No such tool: xd://lsp` and no mounted LSP device. No LSP references/definition/diagnostics were available; no grep was used.

## Independent extracted-value comparison

Scratch script `/tmp/kengaku-r27-FPolicyE2/e2_independent.py` transcribes the frozen regex and E2 algorithm directly; its independent path does not use `gp.BARE_RE` or the instrument's extractor. It uses `gp.build_population` solely to load and baseline-validate the frozen input records, then compares each parsed E2 value against `parser_policy_compare.e2_bare_last`, using sorted compact JSON serialization to compare values rather than verdicts.

Exact command: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FPolicyE2/e2_independent.py; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"` (exit 0). Selected stdout lines:

```text
POPULATION count=1964 candidate_count=1964 excluded=0 pins=4/4 loader_errors=0
E2_EXTRACTED_VALUE_COMPARISON compared=1964 mismatches=0 exceptions=0
EDGE_TOTAL cases=4 failures=0
EXIT=0
```

Hand-derived off-population outcomes (the script checked both independent and candidate results): (1) a fence candidate followed by a later raw object yields `{"v":"outside"}` because E2 includes fence contents and selects the last match; (2) after `{"v":1} then {"v":}`, the invalid final regex match is skipped and `{"v":1}` is returned; (3) for `{"outer":{"inner":{"leaf":3}}}`, the bounded pattern finds the parseable middle candidate `{"inner":{"leaf":3}}`, not the outer object; (4) `{"v":1} then 42` yields `{"v":1}` because a top-level scalar is outside the brace/array regex.

## Findings, residual risk, verification gaps

**No actionable E2 defect observed within the frozen definition and 1964 pinned records.** Independently transcribed E2 values matched the candidate for every record (1964/1964); this is a scoped implementation equivalence result, not a verdict-only comparison and not equivalence on arbitrary JSON or inputs. The edge cases also confirm the intentionally bounded regex behavior; they do not establish general parser correctness or safety.

Residual risk: E2's contract is specifically the regex's non-overlapping object/array matches, not fence stripping, whole-response validation, scalar parsing, or an unbounded JSON parser. LSP-based semantic checks were unavailable. P4/Q15 are outside this E2 assignment. No tools installed or updated.

VERDICT: SCOPED E2 VALUE EQUIVALENCE — no surviving E2 defect found in the tested frozen population and four hand-derived off-population cases; advisory only, not an admission.