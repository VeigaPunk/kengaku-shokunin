# R29CritCountUnit — adversarial count-unit attack on round-29 C1 preregistration

Seat: R29CritCountUnit (critic, axis novelty). Actual writer: KengakuR28.R29CritCountUnit-2.
Scope: preregistration/contract only (`plans/round-29-claims.md` at landed prereg 31934e5, frozen
fixtures). No production code exists yet in R29ExecCore/R29ExecOracle/R29ExecCases worktrees
(`find worktrees -maxdepth 4 -name 'config_projection*'` returned nothing), so this attacks the
contract and the frozen data's discriminating power, not an implementation. No code changes, no
upstream import/exec, no network, no installs/updates. r28 admission not rechecked.

## Inputs (read-only, bytes read once per script)

- `plans/fixtures/r28/webarena/config_files/test.raw.json`: 880776 bytes, sha256
  7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 (matches manifest pin).
- `plans/fixtures/r29/profiles.json` sha256 90fdc34d…e018, `manifest.json` sha256 f6390b92…7bf87,
  `generate_test_data.py` sha256 45ddba7b…21cd (all match the plan/manifest pins; `sha256sum`).
- Scratch scripts and their full stdout, all under
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29CritCountUnit/`:
  `census.py`→`census.out`, `census2.py`→`census2.out`, `census3.py`→`census3.out`
  (`python3 censusN.py | tee censusN.out`, all exit 0). Stdlib only. The scripts reimplement the
  six-step `str.replace` sequence from the inert source text. They do not import that source.

## Observed counts (unit named on every number)

| Quantity | Unit | Value |
|---|---|---|
| tasks / distinct `task_id` / `index==task_id` | tasks | 812 / 812 / 812 |
| token occurrences in raw text, per token G/R/S/SA/W/M | occurrences | 385/336/281/300/**0**/133 = 1435 |
| token-bearing string leaves, same order | leaves | 385/323/275/300/0/133 = 1416 |
| leaves holding >1 occurrence (all same token) | leaves | 13 (19 extra occurrences) |
| leaves holding 2+ distinct tokens | leaves | 0 |
| tasks with ≥1 token / per-token task sum | tasks | 812 / 834 (G204 R128 S192 SA182 W0 M128) |
| distinct changed-leaf paths | paths | 5 (`/start_url` 812, `/eval/program_html/[]/url` 338, `/eval/reference_url` 205, `…/must_include/[]` 60, `/eval/reference_answer_raw_annotation` 1) |
| tokens inside JSON object keys | occurrences | 0 |
| sequential applied counts vs original-text counts, each profile | occurrences | equal, all 3 profiles |
| remaining six tokens after projection, each profile | occurrences | 0 |
| other markers left in place: `__last_url__` / `__page__` | occurrences | 65 / 12 |
| non-ASCII codepoints in raw; raw codepoints vs bytes | codepoints | 0; 880776 = 880776 |
| `\uXXXX` escapes in raw; token-bearing string literals containing any backslash | escapes; literals | 49; 0 |
| parsed tasks after projection, each profile | tasks | 812 (3 × 812 = 2436 task/profile) |

Units multiply by profile: 4305 occurrence replacements, 4248 changed leaves and 2436 task/profile
projections. The three numbers measure different things. They must never be summed or substituted for one another.

## Strongest actual objection

On the frozen input and frozen profiles, three behaviors the contract highlights cannot be told apart from
simpler wrong implementations. Any frozen-data output row for them would therefore be false provenance unless
it is labeled non-discriminating:

1. **Order/cascade is vacuous on frozen data.** All 720 permutations of the six replacement steps
   give a projection byte-identical to upstream order, under each of the 3 profiles
   (`census2.out`: `differing_from_upstream_order 0` ×3). No token is a substring of another. The
   overlapping-occurrence count equals the non-overlapping count. Every occurrence is preceded by `"` or space
   and followed by `"` or `/`, and no profile value contains a token. So a wrong-order implementation passes every
   frozen 2436-projection comparison. The plan's "exact order and later-token cascade" (5 words,
   line 74) can only be evidenced by hand cases.
2. **The WIKIPEDIA step is a structural zero.** `__WIKIPEDIA__` occurs 0 times. An implementation
   that omits that step entirely is byte-identical on all 3 profiles (`omit_WIKIPEDIA_step_identical True` ×3).
   "Six token replacements" is therefore evidenced on frozen data for only five tokens.
3. **Codepoint versus byte offsets cannot be told apart in raw coordinates.** The raw text is pure ASCII
   (bytes = codepoints = 880776), and no token-bearing literal contains an escape. A byte-offset
   implementation produces identical raw provenance numbers. The plan's "clearly named Unicode-codepoint offsets, NOT
   claimed byte offsets;" (12 words, line 68) is a labeling requirement here. Only the UTF-8 hand case can test it.

Impacted axes: novelty (coverage/constructs claim C1). Also provenance honesty and calibration of F2/F4 scoring.

## Decisive bounded counterexamples and smallest safe repairs

- **CE-1 order/omission (from point 1 and 2).** Reverse-order and drop-WIKIPEDIA variants match all 3 frozen
  projection digests. *Repair:* report `order_sensitive_permutations=0/720` and
  `wikipedia_occurrences=0` per profile as explicit non-discriminating facts. The required
  "failing wrong … witness" must come from the hand-case file. The frozen data do supply a real wrong
  witness for the URL-only option (next item), but not for wrong order. The plan's disjunction "a failing wrong
  URL-only or wrong-order witness" (16 words, line 100) can be satisfied by URL-only alone. The wrong-order witness
  still needs its own hand case before "exact order" is claimed.
- **CE-2 URL-only witness has bounded power.** Substituting only leaves whose key name contains
  `url` misses 61 leaves: 60 `must_include` entries and 1 `reference_answer_raw_annotation`. Those leaves sit in 18
  tasks per profile, so this wrong variant is detectable on frozen data. A *value-shape* URL-only rule (a leaf starting with a token)
  misses 0 leaves, because every token-bearing leaf starts with a token. *Repair:* the witness must
  name which URL-only definition it uses. Only the key-name variant counts as a frozen-data failing witness.
- **CE-3 F3 has no pinned resolution criterion.** "F3 global replacement changes at least one
  non-URL-valued field, p=.7;" (10 words, line 106). Judged by key name, it resolves true (61 leaves). Judged by value
  shape, every changed leaf is URL-like, though 13 are multi-URL lists joined by `|AND|` (5), `|OR|` (7) or `,`
  (1). The forecast can be resolved either way after the fact. *Repair:* before scoring, freeze the definition (key-name or value-shape) and
  report both counts. Neither reading creates a task-validity claim.
- **CE-4 site values versus token keys are not the same thing.** The `sites` metadata lists `wikipedia` for 23
  tasks, yet the WIKIPEDIA token is absent (17 of those tasks start at `__MAP__`, 6 at `__GITLAB__`). `reddit` is listed for 129 tasks
  against 128 REDDIT-token tasks, and `shopping_admin` for 184 against 182. In total, 26 tasks have a site set that differs from their token set.
  *Repair:* compute per-token task counts only from token occurrences in the authenticated text. Never
  derive them from `sites`, consistent with "unread metadata remains metadata, not a consumed scorer
  predicate." (9 words, line 46).
- **CE-5 offset frame is unpinned.** Sequential replacement shifts coordinates. Under
  `distinct_origins`, original-raw codepoint offsets differ from the offsets in the text being
  replaced for 1027 of 1050 occurrences of steps 2–6 (REDDIT 331/336, SHOPPING 275/281, SHOPPING_ADMIN 288/300,
  MAP 133/133). Original-raw offsets do not depend on the profile, while intermediate offsets do. *Repair:* name the frame
  explicitly, either `raw_codepoint_offset` (original text) or `step_input_codepoint_offset`. The oracle must
  compare in the same frame.
- **CE-6 unit pooling traps.** 1435 occurrences ≠ 1416 leaves (13 leaves are multi-occurrence),
  and the per-token task sum of 834 ≠ 812 distinct tasks. Requirement: "distinguish replacement occurrence counts,
  changed-leaf counts and task counts; do not pool units." (13 words, line 71). *Repair:* emit per-token
  rows carrying all three units, plus distinct-task totals that are not sums of the per-token rows.
- **CE-7 remaining-placeholder scope.** A case-insensitive `__…__` census would report 77 "remaining"
  markers (65 `__last_url__` plus 12 `__page__`), which are runtime markers, not environment tokens. *Repair:* count remaining placeholders against
  the exact six tokens only, and list the other markers separately. F2 resolves true for these profiles by construction,
  because no profile value contains a token.

## Not objections (checked, no defect)

No token appears in a JSON object key. No token is substring-nested in another (`__SHOPPING__` is not contained in
`__SHOPPING_ADMIN__`). The sequential applied counts equal the original-text counts. Decoded-leaf counts
equal serialized counts, so no token is hidden behind an escape. Every projection parses to 812 tasks. `index==task_id`
holds for 812/812, so F4's shuffled half rests on the hand witness alone, as the plan already states.

## Classification

Every counterexample above is a fixable labeling, frame or definition defect. None is a tradeoff that the
canonical judge must reject. The C1 count `812×3=2436` and the frozen-data token census stand. No task invalidity,
runtime or deployment claim is made. All counts are source/data-side. Runtime behavior is unknown and out of scope.

Quote word counts were produced programmatically by `len(q.split())` in `census3.py`, and each quote was confirmed present
(whitespace-normalized) in the plan, at the lines printed in `census3.out`.

VERDICT: PARTIAL
