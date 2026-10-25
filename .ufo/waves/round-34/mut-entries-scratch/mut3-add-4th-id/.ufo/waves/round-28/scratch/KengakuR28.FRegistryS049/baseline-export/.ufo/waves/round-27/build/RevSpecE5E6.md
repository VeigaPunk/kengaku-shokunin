# RevSpecE5E6 — round 27 review

Scope: frozen E5/E6 extraction semantics, CommonMark edge strings, and the pinned-response behavior. Read the preregistration first. No LSP device is mounted (`read xd://lsp` returned “No such tool”), so references/definition/diagnostics queries were unavailable.

## Findings

1. **LOW — E6 “any-label-fence” overstates the frozen regex; keep the regex authoritative.** `plans/round-27-claims.md:43` defines E6 as ` ```[A-Za-z0-9_+-]*[ \t]*\r?\n(.*?)``` ` plus E0 fallback. It recognizes an empty or single ASCII-token info label, not every CommonMark info string. CommonMark §4.5 says the opener may contain optional text, “this is trimmed of leading and trailing spaces or tabs” (URL: https://spec.commonmark.org/0.31.2/#fenced-code-blocks; accessed 2026-10-21; lines 2734–2737); its first word is “typically used to specify the language” (same URL/date, §4.5 lines 3192–3195). The spec also admits tilde fences (§4.5 lines 2729–2733).
   - ` ```python\n{"a":2}\n``` `: CommonMark info=`python`; E6 matches the fence; E0 misses that label but its bare fallback still finds the JSON; E5 returns None.
   - ` ``` json\n{"a":1}\n``` `: CommonMark trims info to `json`; E0 and E6 regexes both miss it (E6 cannot skip the `json` after its whitespace), but their bare fallback finds the body; E5 returns None.
   - ` ```json {"a":1}\n``` `: CommonMark info=`json {"a":1}`, body empty; E6 misses the fence, then its bare fallback can parse JSON from the info string. By contrast `~~~json\n{"a":1}\n~~~` is a CommonMark fence but is invisible to all three backtick regexes; E0/E6 may still recover the body via bare fallback, while E5 returns None.
   - CommonMark.js 0.31.2 confirmed these info/content results on the concrete cases. Best-supported reading: E6 is “E0 with a permitted one-token label class,” not a CommonMark-any-info-string parser. Preserve the frozen semantics; if the name remains, document its narrower scope. A matching value from E0/E6 fallback is not proof its fence regex recognized the fence.

2. **INFORMATIONAL — E5 is strictly last-matched-fence-or-None; it never retries an earlier parseable fence.** The table says “last fenced block (E0's regex) if it parses, else None (no bare fallback)” (`plans/round-27-claims.md:42`); the independent writer oracle implements this branch at `plans/fixtures/r27/policy_oracle.py:55–63,102–105`. Concrete case: ` ```json\n{"a":1}\n```\n```json\n{"a":1,}\n``` ` — the first fenced JSON parses, the last does not; E0's bare-last fallback recovers `{"a":1}`, while E5 returns None. This is the strongest reading of “last fence fails but an earlier one parses.”
   - Frozen population probe: `POP n=1964 candidates=1964 excluded=0 errors=0`; E0 reproduced all stored verdicts. `LASTFAIL records=0 with_earlier_parse=0`: the above distinction is not exercised by this population. E5 had `flip_pf=26 flip_fp=0 none=145`; all 26 flips were no-regex-fence stored PASSes (9 BARE, 17 DANGLE), not last-fence-parse failures. Therefore Q8's observation is evidence of bare-fallback reliance on no-match responses, not evidence about earlier-fence recovery.

## Residual risk and verification gaps

- E6 agreed with E0 on all 1964 records (`fence_lists_differ=0`, `verdict_differs_from_E0=0`), but no tested records exercise its distinguishing label grammar, spaces-before-label, tilde fences, or extended info strings. Zero disagreements is not a CommonMark-conformance test.
- Both regexes are extraction patterns, not CommonMark fence parsers: CommonMark requires a same-character closing fence at least as long as its opener (§4.5 lines 2741–2744, 2819–2820, 2857); these regexes only pair triple backticks. This is a scope limitation, not a reason to alter the frozen policies here.
- LSP checks unavailable (device not mounted). The integrated comparison instrument was not present in the lane snapshot during this scoped policy review; the frozen policy text and writer-oracle copy were reviewed.

## Verification and installs

- `PYTHONDONTWRITEBYTECODE=1 /tmp/r27-revE5E6/venv/bin/python /tmp/r27-revE5E6/probe.py` — exit 0; E0 sanity 0 mismatches; E5/E6 counts above.
- `PYTHONDONTWRITEBYTECODE=1 /tmp/r27-revE5E6/venv/bin/python /tmp/r27-revE5E6/probe2.py` — exit 0; last-fence failure and strata counts above.
- `node /tmp/r27-revE5E6/cm_ref.js` — exit 0; 21 constructed cases parsed with CommonMark.js.
- Installs: `markdown-it-py 4.2.0` via `uv pip`/PyPI into `/tmp/r27-revE5E6/venv` for a CommonMark cross-check; `commonmark 0.31.2` via npm into `/tmp/r27-revE5E6/cmjs` as the CommonMark reference parser. Scratch only; no host or lane packages changed.

VERDICT: E5’s strict last-match/no-fallback reading is explicit and correct for the frozen table; E6’s exact one-token regex is likewise frozen, but “any-label” must not be read as covering CommonMark info strings or tilde fences. The pinned population exercises neither edge distinction.