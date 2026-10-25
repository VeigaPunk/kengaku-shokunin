# RowGsm8kYaml — round 27 (novelty, extraction-policy source)

Access date 2026-10-21. Fetched with curl over https from
`raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/<rev>/lm_eval/...`. Harness `main` HEAD at fetch:
`d6de81643928d653435c431bae19945d41d32520` (pinned by SrcLmEvalFlexible; the same revision re-fetched here for
`gsm8k.yaml` and `gsm8k-cot-llama.yaml`). Last commit touching `lm_eval/tasks/gsm8k/gsm8k.yaml`:
`b733598568fde3afa0e008892f8e7bb18cd472b6` (2026-01-27T10:29:09Z, GitHub commits API).
Bytes saved under `/tmp/kengaku-r27-RowGsm8kYaml/`:

- `gsm8k.yaml` sha256 `82eb1780b263bc040729032b3e076990c7933f42163c91e359f38820dd1d8833`
- `gsm8k-cot.yaml` sha256 `7c9dd2561fe334a55f62bdc6a876f045e6dc7f53714c7a9db506b89c6de6bc96`
- `gsm8k-cot-llama.yaml` sha256 `c295bc7e942e8f3a51b91d14d5e592d2b037330c831f4ab5b2f8ddca27e031d6` (at d6de8164)
- `lm_eval/filters/extraction.py` sha256 `eb976bb36d5d3e93faafe6d065678e24b4474e78cd4fce1e730e2b8f49b9fda0`

## (1) SOURCES.md draft row (id left as S0xx)

Format discrepancy: the task asked for 13 cells. The SOURCES.md header and every existing row
(S001–S048) have **11** cells (`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`).
Drafted to the existing 11-cell layout; the integrator must confirm which is intended.
`kind` `docs` follows existing usage (no `code` kind exists in the registry).
Scope is narrowed to `gsm8k.yaml` only, because sibling task files use different markers and selectors.

```
| S0xx | lm-evaluation-harness GSM8K task config (gsm8k.yaml) and regex filter selection — https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/gsm8k/gsm8k.yaml | docs | A | the harness's gsm8k.yaml strict-match and flexible-extract filters and the regex filter's match selection; not sibling gsm8k-cot*.yaml files and not answer-grader accuracy | gsm8k.yaml:33-42 + lm_eval/filters/extraction.py:27, :47-49 @ d6de8164 (file last changed b733598) | in gsm8k.yaml, strict-match takes a literal `####` marker at first match (no group_select, default 0); flexible-extract takes the last regex match (group_select -1): one task ships a first-match and a last-match extraction policy | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |
```

## (2) gate.md line (draft, not written to the lane)

`S0xx: https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/lm_eval/tasks/gsm8k/gsm8k.yaml — accessed 2026-10-21 — main d6de8164…, file last changed b733598… — gsm8k.yaml:41-42 (flexible-extract block):`
`"group_select: -1"` / `"regex_pattern: \"(-?[$0-9.,]{2,})|(-?[0-9]+)\""` (verbatim, two adjacent lines).

Supporting verbatim locations (same access date, rev d6de8164):
- `gsm8k.yaml:36` `regex_pattern: "#### (\\-?[0-9\\.\\,]+)"` (strict-match; no `group_select` line, so first match).
- `extraction.py:27` `group_select: int = 0,` (default selects the first match).
- `extraction.py:47-49` `match = self.regex.findall(resp)` / `match = match[self.group_select]`.
- `gsm8k-cot.yaml:49` `regex_pattern: The answer is (\-?[0-9\.\,]+).` (CoT variant: strict marker `The answer is`, not `####`; no group_select).
- `gsm8k-cot-llama.yaml:48-49` `group_select: -1` / `regex_pattern: The final answer is ((-?[$0-9.,]{2,})|(-?[0-9]+))`
  (CoT-llama strict-match is LAST match. Confirmed by re-fetch at d6de8164.)

## Caution: "strict = first" does not generalize

`gsm8k-cot-llama.yaml` strict-match uses `group_select: -1`, so its strict policy is last-match. Only
`gsm8k.yaml` (and, by absence of a selector, `gsm8k-cot.yaml`) has first-match strict. Any claim about
"the harness's strict-match" must name the file. The row above is scoped to `gsm8k.yaml` for this reason.

## (3) Pre-registered policy grounded

**None of E1–E8.** The harness policies are regex filters keyed to a literal marker (`####`, `The answer is`,
or `The final answer is`) plus a number regex, selected by first or last match depending on the file. No E1–E8
policy reads a marker regex; E0–E8 are JSON-block/BARE_RE policies (`plans/round-27-claims.md:37-46`).
The first/last-match *position axis* named at `round-27-claims.md:26-27` is confirmed by this source, but
E2 (bare-last) and E3 (bare-first) are analogues on that axis only, not grounding: their regex is BARE_RE, not
the harness regex. Citing this row for any Ei would overclaim.

## Notes

- `flexible-extract` tuple handling (`extraction.py:51-54`) keeps the first non-empty group of the selected tuple,
  so "last match" means last number-like token anywhere in the response, not last JSON block.
- Nothing was written to the lane tree, its git/jj state, or `corpus/evidence/round27-sources/gate.md`.

## Installs

None. Used the existing `curl`, `sha256sum`, `sed`, `grep`.

## Files written

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/build/RowGsm8kYaml.md` (this report).
- `/tmp/kengaku-r27-RowGsm8kYaml/{gsm8k.yaml,gsm8k-cot.yaml,gsm8k-cot-llama.yaml,extraction.py}` (scratch fetch; hashes above).

VERDICT: S0xx drafted at the 11-cell registry layout (task said 13, flagged), scoped to gsm8k.yaml after confirming the llama strict-match is last-match at d6de8164, and no pre-registered E1–E8 policy is grounded by this source.
