# R29TokenReddit — `__REDDIT__` token census (round29 C1, scoped)

**Seat / actual writer:** `KengakuR28.R29TokenReddit-2` (leaf; no delegation, no subagents).
**Milestone:** pinned generated-config projection observability.
**Scope:** one token only — literal `__REDDIT__` in the frozen r28 raw serialized JSON — its
occurrence/leaf/task counts, field and JSON-path ownership, raw-vs-decoded provenance,
non-URL-field metadata, and replacement length/codepoint-span implications under the three
frozen synthetic profiles. Read-only: no production edits, no `config_files` output written,
no network, no upstream import/execution, no model/routing changes. This is author-side
evidence, not round closure or admission.

## 1. Pinned inputs (read once; bytes retained; hashes verified before parse)

| Input | Bytes | SHA-256 | Pin |
|---|---|---|---|
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | matches `plans/fixtures/r29/manifest.json` |
| `plans/fixtures/r29/profiles.json` | 1391 | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | matches manifest `files` entry |
| `plans/fixtures/r29/manifest.json` | 1061 | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | read; matches stated pin |
| `plans/fixtures/r29/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | read as inert data only; matches manifest |

Source contract location: `plans/fixtures/r29/generate_test_data.py:12` —
`raw = raw.replace("__REDDIT__", REDDIT)` (4 whitespace-separated tokens, `wc -w`).
Order context from the same file, lines 11–16: GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN,
WIKIPEDIA, MAP. The `browser_env.env_config` import was **never** executed or evaluated.

Raw input properties observed: 880776 bytes = 880776 Unicode codepoints, 0 non-ASCII
codepoints (so byte offsets equal codepoint offsets *for this file only*), UTF-8 strict
decode succeeded, parsed to 812 top-level objects with 812 distinct `task_id` values and
`output_index == task_id` for all 812.

`plans/config_projection.py` was **absent** at census time (2026-10-21T16:07:04Z):
`ls plans/config_projection.py` → `No such file or directory`;
`git cat-file -e ed26bdf5d924755697cd6812129be2fa441c42a3:plans/config_projection.py` →
`fatal: path 'plans/config_projection.py' does not exist in 'ed26bdf5d924755697cd6812129be2fa441c42a3'`.
Therefore the planner's counting command `python3 plans/config_projection.py --summary` was
not executed by this seat; production-tool verification remains L1's.

## 2. Commands and exact outputs

```
$ RAW=plans/fixtures/r28/webarena/config_files/test.raw.json
$ sha256sum plans/fixtures/r29/manifest.json plans/fixtures/r29/generate_test_data.py \
    plans/fixtures/r29/profiles.json "$RAW"
(condensed: four hashes, each matching the pin in §1)

$ grep -o '__REDDIT__' "$RAW" | wc -l
336
$ grep -o '__reddit__' "$RAW" | wc -l
0
$ grep -o 'REDDIT' "$RAW" | wc -l
336
$ grep -c '__REDDIT__' "$RAW"
323
$ for t in GITLAB REDDIT SHOPPING SHOPPING_ADMIN WIKIPEDIA MAP; do grep -o "__${t}__" "$RAW" | wc -l; done
(condensed, per token: 385 336 281 300 0 133; sum 1435)
$ grep -ob '__REDDIT__' "$RAW" | sed -n '1,3p;334,336p'
(condensed, one offset per line: 26080 27014 27938 ... 778690 779184 779761)
$ python3 -B -c "b=open('plans/fixtures/r28/webarena/config_files/test.raw.json','rb').read(); print(len(b), b.count(b'__REDDIT__'))"
880776 336
```

Independent census script (stdlib only, no project imports, reads the pinned bytes once):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29TokenReddit-2/census_reddit.py`
(sha256 `e6b6091476402580f0710e1b799c738603ade8c30fbc1d6760d0afb982754077`). Output JSON:
same scratch dir `reddit-census.json` (sha256 `2cf9d109c1bdd512ad3fe9ca41c52f962b1d21dc90523596a96fffcba1e9e45d`).
Exit 0. Key stdout:

```
raw sha 7b50386f... bytes 880776 codepoints 880776 non_ascii 0
tasks 812 distinct 812 index==task_id True
counts {'GITLAB': 385, 'REDDIT': 336, 'SHOPPING': 281, 'SHOPPING_ADMIN': 300, 'WIKIPEDIA': 0, 'MAP': 133}
REDDIT raw count 336 decoded 336 keys 0 leaves 323 tasks 128
literal pairing all equal True literals 29009
escapes {'backslash_u_escapes_total': 49, ... 'backslash_slash_escapes': 0,
         'escapes_decoding_to_token_chars': {"'_'":0,"'R'":0,"'E'":0,"'D'":0,"'I'":0,"'T'":0}}
skew nonzero occurrences 0 max skew 0
```

Second, separate code path (independent recursive walk, no shared functions with the script):

```
$ python3 -B -c "<recursive walk with path[1] as task index>"
occ 336 distinct_tasks 128 distinct_leaves 323
```

Independent field-class predicate (leaf key in `{url,start_url,reference_url}` or suffix `_url`):

```
url_typed 282 non_url_typed 54 total 336
```

Units used below: **occurrence** (non-overlapping literal hit in the serialized text),
**decoded occurrence** (hit in a decoded string leaf), **leaf** (distinct JSON string leaf),
**task** (top-level object by `output_index`), **codepoint offset** (Unicode codepoints in the
serialized text, never claimed as bytes in general). Units are not pooled.

## 3. Raw serialized vs decoded/escaped occurrence census

- Raw serialized literal occurrences of `__REDDIT__`: **336**. All 336 lie inside JSON string
  literals; raw whole-file count equals occurrences found inside scanned literals (336), so
  no occurrence exists in structural JSON positions.
- Decoded occurrences in string values: **336**; in string **keys**: **0**. So the raw literal
  count and the decoded count coincide: each serialized hit maps to exactly one decoded hit.
- Escape analysis: the raw file contains **49** `\uXXXX` escapes, decoding only to
  `é`×6, `î`×8, `ó`×2, `ý`×6, `–`×4, `’`×19, `™`×4. **Zero** escapes decode to any character
  of `__REDDIT__` (`_ R E D I T` all 0), and there are **0** `\/` escapes. Therefore there is
  **no escape-split/synthesized decoded occurrence** for this token; decoded hits are exactly
  the literal hits and vice versa.
- Literal-span pairing: all **29009** JSON string literals were scanned, decoded, and paired
  positionally with the decoded-document walk; **0** mismatches. Per-occurrence
  `decoded_leaf_offset → raw_offset` mapping was computed from each literal's escape-aware
  index map; the decoded-to-raw skew is **0 for all 336 occurrences** (all token-bearing
  literals are ASCII-clean before the token), and every computed raw span was re-checked
  against the retained text (`text[raw_off:raw_off+10] == "__REDDIT__"`, 336/336).
- Lowercase variant `__reddit__`: **0**. Bare `REDDIT` without underscores: 336 (i.e. no other
  spelling). No REDDIT span overlaps any other five-token occurrence (0 overlaps).
- Raw codepoint offsets: first `26080`, last `779761`; byte offsets equal these because the
  file is pure ASCII. `grep -ob` independently returns the same boundary offsets
  (26080, 27014, 27938, …, 778690, 779184, 779761).

## 4. Owning tasks, fields, and JSON paths

336 occurrences / 323 leaves / 128 tasks. Distribution by owning leaf key:

| Leaf key | Occurrences | Distinct leaves | Distinct tasks | Field class |
|---|---|---|---|---|
| `start_url` | 114 | 114 | 114 | URL-valued (A) |
| `eval.program_html.[n].url` (`url` key) | 85 | 85 | 42 | URL-valued (A) |
| `eval.reference_url` | 83 | 71 | 71 | URL-valued (A) |
| `eval.program_html.[0].required_contents.must_include.[k]` | 52 | 52 | 9 | non-URL-typed eval metadata (B) |
| `eval.reference_answer_raw_annotation` | 2 | 1 | 1 | non-URL-typed eval metadata (B) |

Class totals: **A (URL-typed field) 282** occurrences (83.93%); **B (non-URL-typed field, but
token used as a URL-shaped string) 54** (16.07%); **C (plain prose metadata) 0**. Field names
observed for B are exactly `required_contents.must_include` (tasks 552–555, 562–566; indices
`[0]`–`[9]`) and `reference_answer_raw_annotation` (task 66). No occurrence lies in `intent`,
`intent_template`, `eval.reference_answers.*`, `sites`, `storage_state`, or `geolocation`.

Shapes (all 336):
- Position in leaf: leaf start 323, immediately after a space 13. Following character: `/`
  232, end-of-string 104. Whole-leaf value exactly `__REDDIT__`: 104 (all `start_url`).
- `start_url`: 104 bare token, 10 token + `/f/...` path (e.g. `[409].start_url`,
  `[615]–[619].start_url`, `[650]–[652].start_url`).
- `eval.reference_url`: values are token + `/f/...` alternatives joined by ` |OR| `; 19
  occurrences sit in 7 leaves with 2–4 alternatives each (64 single-occurrence leaves,
  3×2, 3×3, 1×4).
- `eval.program_html.[n].url`: 85 leaves in 42 tasks, each token + `/r|/f|/user/...` path.
- `must_include`: each value is token + `/f/...` (scheme-less URL path in a non-URL field).
- `eval.reference_answer_raw_annotation` (task 66): prose containing two token-led URL paths
  separated by `, `.

Leaves by occurrence count: 315×1, 4×2, 3×3, 1×4 (max 4). Multi-occurrence leaves:
`[66].eval.reference_answer_raw_annotation` (2), `[604]/[609]/[681].eval.reference_url` (3),
`[682].eval.reference_url` (4), `[608]/[625]/[683].eval.reference_url` (2).
No leaf contains `__REDDIT__` together with any other of the six frozen token literals, so
there is no intra-leaf cross-token ordering interaction for this token; the only interaction
is the global GITLAB-before-REDDIT offset shift (§5).

Task ownership: 128 tasks, ranges
`27–31, 66–69, 399–410, 552–555, 562–566, 580–584, 595–652, 671–675, 681–688, 714–735`.
Per-task occurrence counts: `{1:15, 2:77, 3:17, 4:5, 5:7, 6:2, 8:1, 9:1, 10:1, 11:2}`
(max 11 in tasks 724 and 730; 10 in task 565; 9 in 721; 8 in 566). Because
`output_index == task_id` for all 812 inputs, each affected task's upstream output ordinal
equals its `task_id` (e.g. task 27 → `config_files/27.json`); this is a property of this
frozen input, not a general identity.

## 5. Replacement length and codepoint-span implications (3 synthetic profiles)

`__REDDIT__` is 10 codepoints. Profiles are controlled synthetic `*.invalid` fixtures, not
observed deployment values.

| Profile | REDDIT value | len | Δ per occurrence | REDDIT total Δ | Final text (cp = bytes) |
|---|---|---|---|---|---|
| `distinct_origins` | `http://reddit.invalid:10102` | 27 | +17 | +5712 | 905171 |
| `path_prefix` | `http://reddit.invalid:10202/prefix` | 34 | +24 | +8064 | 915216 |
| `trailing_slash_sensitivity` | `http://reddit.invalid:10302/` | 28 | +18 | +6048 | 906606 |

Length arithmetic verified exactly per profile:
`880776 + Σ_tokens(count × Δ_token) = observed final length`
(24395 / 34440 / 25830 total codepoints added; all six token Δ values are uniform within a
profile: 17 / 24 / 18, so REDDIT's Δ equals the other tokens' Δ in the same profile).

Span model (serialized text, codepoints). REDDIT replacement runs **after** GITLAB, so its
true operand is the text already modified by the GITLAB replacement:
- Observed REDDIT spans in the post-GITLAB text were re-located (336 per profile, not
  inferred). Shift of each occurrence = (# GITLAB occurrences strictly before it) ×
  (GITLAB value length − 10); verified match for all 336 × 3 profiles
  (`shift_checks_all_match True`). Example: occurrence 6 (raw offset 60981) → post-GITLAB
  `61083` (distinct, shift +102 = 6×17), `61125` (path_prefix, +144 = 6×24), `61089`
  (trailing, +108 = 6×18). Occurrences 1–5 shift 0.
- Final start offsets inside the REDDIT-replaced text: `s_j = span_j + j × Δ`; each final span
  was verified to contain exactly the profile value (336/336 per profile). Example occurrence
  6 final spans: `[61168,61195)` / `[61245,61279)` / `[61179,61207)`. Last (336th) final start:
  `790505` / `794929` / `791137`.
- The profile value occurs exactly **336** times in the post-REDDIT text — one per replacement,
  no pre-existing occurrence and no duplicate creation.
- Parsed consequence: after the full six-token ordered pipeline, each profile parses to
  **812** tasks with **812** distinct IDs, `index == task_id` for all, and all six remaining
  token counts **0** (including `__REDDIT__`). No profile value contains any token literal, so
  REDDIT's replacement cannot cascade into later-token hits; no value contains `"` or `\`
  (`json.dumps` inner encoding clean), and token hits start at leaf start or after a space and
  are followed only by `/` or end-of-string, so the replacement cannot split a token/identifier
  or alter JSON string structure.
- Trailing-slash profile observation: for the 232 occurrences followed by `/`, literal text
  concatenation yields `http://reddit.invalid:10302//path` (double slash); the 104 whole-leaf
  values become `http://reddit.invalid:10302/`. This is recorded as a serialized-text
  consequence; no URL normalization, escaping repair, or URL-only substitution was applied.
- Per-leaf/per-task impact (identical across profiles in unit counts): 323 changed leaves,
  128 changed tasks, 969 leaf×profile projections, 384 REDDIT-affected task×profile
  projections, 1008 replacement events across 3 profiles.

## 6. Count units for this token (never pooled)

| Unit | Value | Derivation |
|---|---|---|
| raw serialized replacement occurrences | 336 | `str.count` + `grep -o` + literal scan |
| decoded occurrences (values) | 336 | decoded walk; 0 in keys |
| distinct changed leaves | 323 | (task, path) pairs with ≥1 hit |
| distinct changed tasks | 128 | distinct top-level indices/`task_id`s |
| occurrence/leaf/task ratio | 336 / 323 / 128 | three separate units |
| task×profile projections | 2436 expected (812×3); 384 REDDIT-affected | in-memory projection |
| replacement events across profiles | 1008 (336×3) | per-profile counts identical |
| remaining `__REDDIT__` after full pipeline | 0 raw and 0 decoded, all 3 profiles | post-projection scan |

Cross-checks: six-token raw total `385+336+281+300+0+133 = 1435` matches the independently
reported all-token occurrence total for `distinct_origins`; `grep -c` line count 323 is
consistent with 315 single-occurrence leaves + 8 multi-occurrence leaves each on one line
(315+8 = 323). All three counting paths (grep, literal scan, recursive walk) agree on 336;
the recursive walk independently returns 128 tasks / 323 leaves.

## 7. Unknowns and boundaries

- Profiles are own-work synthetic `*.invalid` fixtures; they are sensitivity controls, not
  observed benchmark deployment, endpoints, or model/judge behavior. No endpoint or site was
  contacted; no host env/credential/auth-store value was read.
- The upstream runtime value of `REDDIT` (and the other five variables) is **not observed**:
  `browser_env.env_config` was never imported/executed; the pinned generator is inert data.
  Whether any actual deployment joins origins/paths differently is unknown.
- This census covers `__REDDIT__` only. It is not a six-token resolution claim and not a
  global absence claim; `__WIKIPEDIA__` = 0 is a same-file observation only.
- `plans/config_projection.py` was absent at census time, so the planner's `--summary`/`--json`
  outputs were not observed by this seat; 2436 is spec arithmetic (812×3) independently
  reproduced in memory, not a production-tool reading. Production verification belongs to L1.
- No actual `config_files/test.json` or per-task files were written; projection was in memory
  only (scratch census artifacts are this seat's own scratch).
- Byte offsets equal codepoint offsets only because this frozen file is pure ASCII; the
  provenance units are Unicode codepoints, as required, with byte values noted as equal here.
- Full 336-row occurrence table (raw codepoint offset, raw byte offset, decoded leaf offset,
  literal span, task index, `task_id`, path, leaf key, category, leaf value) is retained in
  `reddit-census.json`; this report shows bounded samples only. No exhaustive mutation
  coverage and no fixture-quality judgment is claimed.

VERDICT: PASS
