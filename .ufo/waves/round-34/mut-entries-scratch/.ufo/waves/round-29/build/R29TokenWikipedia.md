# R29TokenWikipedia — token-scoped census for `__WIKIPEDIA__` on the pinned raw config

Seat: `KengakuR28.R29TokenWikipedia-2`. Actual writer: same (leaf; no delegation, no subagents).
Scope: round-29 claim C1 observability only, one token's raw/provenance slice. No round admission, no
score/calibration claim, no production edit, no model/runtime claim. Read-only except this unique
report. Date 2026-10-21. Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Headline (observed, not inferred)

`__WIKIPEDIA__` occurs **0 times** in the pinned raw serialized text and **0 times** at decoded-leaf
and decoded-key level. The raw text contains only **five of the six** source-replacement tokens; the
fifth replacement step in `scripts/generate_test_data.py` is therefore a strict text no-op on this
frozen snapshot under all three neutral profiles. The 23 lowercase `wikipedia` strings that do exist
are `sites` metadata values, are never matched by the exact token, and remain unchanged.

## Pins re-verified before analysis (each file read once, bytes retained)

| Input | Bytes | SHA-256 observed | Expected |
|---|---:|---|---|
| `plans/fixtures/r29/manifest.json` | 1,061 | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | same |
| `plans/fixtures/r29/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | same |
| `plans/fixtures/r29/profiles.json` | 1,391 | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | same |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | 880,776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | same |

HEAD is `31934e5660f1814326c6472eefdfa0c41e642a2f` (preregistration landing); `plans/config_projection.py`
does not exist there (`ls` → No such file), so no production instrument output was available to compare.
`git status --porcelain plans/fixtures` printed nothing. Raw file properties: UTF-8, no BOM, pure ASCII
(max codepoint 127), 880,776 bytes = 880,776 Unicode codepoints, 29,604 `\n`, 0 `\r`. Because the file is
ASCII, codepoint offsets coincide numerically with byte offsets here — that is an observed property of
this file, not an assumption about offsets in general.

## Method (independent, stdlib only)

1. Read the pinned raw bytes once; hash; decode UTF-8; never re-read.
2. Count literal occurrences of `__WIKIPEDIA__` in the retained text; probe escape-encoded variants
   (`\u005f`/`\u005F` underscore escapes, case variants, longer `__WIKIPEDIA...` runs).
3. Build a positional JSON scanner over the same retained text that records every string literal's
   raw span, decoded value and JSON path (tuple of keys/indices). Cross-checked against `json.loads`:
   10,869 string leaves, **0** path/value differences; scanner consumed 880,775 of 880,776 codepoints
   (one trailing `\n`, no trailing garbage). Non-string leaves 4,705 (1,657 int, 1,624 bool, 1,424 null).
4. Replay the six manifest-ordered serialized-text replacements on the retained text per profile,
   recording per-step occurrence count, codepoint delta, digest, and text identity; then parse only the
   projected text and diff scalar leaves against the parsed raw document.
5. Differential control: replay with the `__WIKIPEDIA__` step skipped and compare final digests.

No upstream module was imported or executed (`browser_env.env_config` never touched), no environment
value, auth-state, credential store or endpoint was read, no network request was made, nothing was
written but this report (no `config_files/test.json`, no per-task output). No `lsp` device is exposed to
this seat; the only source reference is a 27-line inert data file read directly with `nl -ba`, so no
semantic symbol trace applies here. Two located quotes, each word-counted programmatically with
whitespace `split()` (limit 25, not estimated): generator line 15 verbatim
`raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)` → **4** words; frozen profile purpose verbatim
"controlled synthetic text-substitution profile, not an observed deployment"
(`plans/fixtures/r29/profiles.json`, all three profiles) → **8** words, string present in the pinned
bytes as written.

## Result 1 — token census (units kept separate)

Source: `plans/fixtures/r28/webarena/config_files/test.raw.json` (pinned bytes above); source-side
replacement lines 11–16 of `plans/fixtures/r29/generate_test_data.py`, order GITLAB, REDDIT, SHOPPING,
SHOPPING_ADMIN, WIKIPEDIA, MAP (WIKIPEDIA is the 5th step, line 15).

| Token | raw serialized occurrences | decoded occurrences | decoded leaves | owning tasks |
|---|---:|---:|---:|---:|
| `__GITLAB__` | 385 | 385 | 385 | 204 |
| `__REDDIT__` | 336 | 336 | 323 | 128 |
| `__SHOPPING__` | 281 | 281 | 275 | 192 |
| `__SHOPPING_ADMIN__` | 300 | 300 | 300 | 182 |
| **`__WIKIPEDIA__`** | **0** | **0** | **0** | **0** |
| `__MAP__` | 133 | 133 | 133 | 128 |

Totals: 1,435 raw occurrences across 1,416 distinct leaves (19 leaves carry two occurrences: 13 REDDIT,
6 SHOPPING), spread over all 812 tasks; 812 tasks carry at least one token. Token length is 13
codepoints (13 UTF-8 bytes), `WIKIPEDIA` = 9 letters with two leading and two trailing underscores.

`__WIKIPEDIA__` has **no owning task, no owning string literal, no key, and no JSON path**. Occurrence
lists at raw, decoded-leaf and decoded-key level are all empty: `[]` / 0 / 0. Complete `__...__`
inventory: a strict `__[A-Z][A-Z0-9_]*__` scan yields exactly the five source tokens above and no sixth
environment token; a permissive `__[^_\n]{1,60}__` scan yields six distinct forms — four of those tokens
(that pattern cannot match `__SHOPPING_ADMIN__`, which has an internal underscore), the browser-runtime
marker `__page__` (12 occurrences, explicitly not one of the six environment tokens), and one
CSS-selector fragment carried inside a `program_html` locator string (5 occurrences, no placeholder
inside it).

## Result 2 — raw-serialized versus decoded/escaped occurrences

- Escaped forms of the token's own underscore characters: `\u005f`/`\u005F` count **0**; the token
  cannot be assembled across an escape boundary either.
- Case variants: `__wikipedia__` 0, `__Wikipedia__` 0; uppercase `WIKIPEDIA` 0 anywhere in the file;
  any `_WIKIPEDIA` prefix 0; any `__WIKIPEDIA<suffix>` run 0.
- Decoded level: `json.loads` plus independent positional walk finds 0 leaves and 0 keys containing the
  token. Raw count and decoded count therefore agree at zero for this token.
- Divergence exists elsewhere and was measured, not assumed: 642 of 10,869 string literals have a raw
  body that differs from their decoded value (1,274 `\"`, 49 `\uXXXX` escapes, 1,335 backslashes total;
  e.g. `Quest Lumaflex\u2122 Band` → `Quest Lumaflex™ Band`). So raw-text and decoded-leaf rewriting are
  genuinely different strategies on this input, but for `__WIKIPEDIA__` both strategies are no-ops
  (0 raw, 0 decoded), and no quote/backslash decode-failure hazard is exercised by this token.

## Result 3 — the 23 lowercase `wikipedia` values (metadata, not the token)

All 23 occurrences are complete string values equal to `wikipedia`, each at in-value offset 0, each
inside a `sites` array of one task (`sites` is a JSON list of lowercase site names:
`gitlab, map, reddit, shopping, shopping_admin, wikipedia`). Raw body equals decoded value for all 23
(no escapes). No URL-valued key contains the substring: across 2,469 leaves under `start_url`, `url`,
`reference_url`, `url_note`, zero contain `wikipedia`; zero leaves inside any `eval` subtree contain it.
These 23 are the only case-insensitive matches of `wikipedia` in the file.

| task_id (= ordinal) | path | raw codepoint offset | line | value |
|---|---:|---:|---:|---|
| 97 | `$[97].sites[1]` | 89451 | 3103 | `wikipedia` |
| 265 | `$[265].sites[0]` | 239579 | 8334 | `wikipedia` |
| 266 | `$[266].sites[0]` | 240426 | 8367 | `wikipedia` |
| 267 | `$[267].sites[0]` | 241202 | 8397 | `wikipedia` |
| 268 | `$[268].sites[0]` | 242142 | 8432 | `wikipedia` |
| 424 | `$[424].sites[0]` | 387872 | 13314 | `wikipedia` |
| 425 | `$[425].sites[0]` | 388782 | 13350 | `wikipedia` |
| 426 | `$[426].sites[0]` | 389711 | 13386 | `wikipedia` |
| 427 | `$[427].sites[0]` | 390714 | 13422 | `wikipedia` |
| 428 | `$[428].sites[0]` | 391677 | 13458 | `wikipedia` |
| 429 | `$[429].sites[0]` | 392669 | 13494 | `wikipedia` |
| 430 | `$[430].sites[0]` | 393619 | 13530 | `wikipedia` |
| 556 | `$[556].sites[1]` | 527890 | 18039 | `wikipedia` |
| 557 | `$[557].sites[1]` | 529217 | 18087 | `wikipedia` |
| 558 | `$[558].sites[1]` | 530386 | 18129 | `wikipedia` |
| 559 | `$[559].sites[1]` | 531560 | 18171 | `wikipedia` |
| 560 | `$[560].sites[1]` | 532752 | 18211 | `wikipedia` |
| 561 | `$[561].sites[1]` | 533911 | 18252 | `wikipedia` |
| 737 | `$[737].sites[0]` | 781528 | 26229 | `wikipedia` |
| 738 | `$[738].sites[0]` | 783099 | 26285 | `wikipedia` |
| 739 | `$[739].sites[0]` | 784682 | 26341 | `wikipedia` |
| 740 | `$[740].sites[0]` | 786233 | 26397 | `wikipedia` |
| 741 | `$[741].sites[0]` | 787833 | 26455 | `wikipedia` |

All 23 tasks are ordinary tasks whose `start_url` is a tokenized URL (`__MAP__`, `__GITLAB__`,
`__SHOPPING_ADMIN__`, …); their `sites` metadata merely lists `wikipedia` among touched sites. These
values are metadata, are not URL values, and are never candidate matches for the exact token.

## Result 4 — ordered replacement under the three neutral profiles (no-op proof)

Per-occurrence length arithmetic for this token, from the frozen profile bytes (all values synthetic
`*.invalid`, no endpoint contact): token 13 codepoints; `distinct_origins` value 30 codepoints
(`http://wikipedia.invalid:10105`, delta **+17**); `path_prefix` 37 (`…:10205/prefix`, delta **+24**);
`trailing_slash_sensitivity` 31 (`…:10305/`, delta **+18**). No profile value contains any of the six
tokens, so a WIKIPEDIA substitution could not create later-token matches.

Replay on retained text, per profile (occurrence count at that step, codepoint delta, digest after step,
`changed` = text differs from before the step):

`distinct_origins` — GITLAB 385 / +6545 / `355c7f50f797725f…`; REDDIT 336 / +5712 / `a3b9fc88e478087a…`;
SHOPPING 281 / +4777 / `9ca61c454fae6cd0…`; SHOPPING_ADMIN 300 / +5100 / `584c2a4a23891f9e…`;
**WIKIPEDIA 0 / +0 / `584c2a4a23891f9e…` / changed=False**; MAP 133 / +2261 / `2aec098e5705c98c…`.
Final length 905,171, delta +24,395.

`path_prefix` — 385 / +9240; 336 / +8064; 281 / +6744; 300 / +7200; **WIKIPEDIA 0 / +0 /
`3b175917d754cdfc…` / changed=False**; MAP 133 / +3192. Final 915,216, delta +34,440.

`trailing_slash_sensitivity` — 385 / +6930; 336 / +6048; 281 / +5058; 300 / +5400; **WIKIPEDIA 0 / +0 /
`ffb64e7c5dc9aaf7…` / changed=False**; MAP 133 / +2394. Final 906,606, delta +25,830.

At every profile the text and digest immediately before and immediately after step 5 are identical, and
the step-5 digest equals the step-4 (SHOPPING_ADMIN) digest. Differential control: replay with step 5
omitted produces a byte-identical final text and the same final digest at all three profiles
(`2aec098e5705c98c…`, `54cf98337dc6751d…`, `49bbee2e827791b7…`). Because the MAP step runs after
WIKIPEDIA and still sees 133 occurrences at its own step, the zero here also removes any WIKIPEDIA→MAP
cascade question on this input.

Codepoint-span implication, stated exactly: for an occurrence at codepoint offset `o` in a profile with
delta `d`, every codepoint offset `> o + 13` in the post-replacement text shifts by `+d`, leaf-internal
offsets after the match shift by `+d`, and the leaf's decoded length grows by `d`. Observed occurrence
count is 0 for every `o` under all three profiles, so the total shift attributable to this token is
**0 codepoints** (`k·d = 0`), and leaf values and JSON paths are unchanged by it. The document-level
deltas +24,395 / +34,440 / +25,830 are produced entirely by the other five tokens and are not
attributable to `__WIKIPEDIA__`. All projected texts remain pure ASCII, so codepoint and byte lengths
coincide there too.

## Result 5 — post-projection structure (unit separation preserved)

Parsed from the projected text only, per profile: 812 tasks, 812 distinct `task_id`, all integer,
`index == task_id` for all 812 (no mismatches), no null ids. Remaining known-token counts after
projection: all six 0 (WIKIPEDIA trivially 0 before and after). Changed string leaves versus the raw
document: 1,416 per profile, which reconciles with 1,435 occurrences minus 19 second-occurrences;
**0** changed leaves originate from a `__WIKIPEDIA__` match; the 23 `sites`-equal-`wikipedia` leaves are
still present and unchanged in all three projections. No per-task output files were written; these are
in-memory projections of retained bytes.

## Result 6 — discriminating power of this token (boundary probes, independent and labelled)

- Exact-token discipline: a wrong global lowercase substitution `replace("wikipedia", value)` would hit
  23 occurrences and corrupt 23 `sites` metadata leaves (all changes confined to `$[i].sites[j]`), with
  document deltas +483 / +644 / +506 codepoints. This is a probe I ran on retained bytes, not a
  production-tool result; it shows WIKIPEDIA is a useful *negative* control for case/exactness.
- URL-only discipline: 0 occurrences live under `start_url`/`url`/`reference_url`/`url_note`, so on this
  input a wrong "URL-only" implementation is byte-indistinguishable from a faithful whole-text
  implementation for this token. WIKIPEDIA therefore cannot serve as the failing witness for URL-only
  scoping; GITLAB or REDDIT (which also have multi-occurrence leaves) are the discriminating choices.
- Ordering: since the step changes nothing and no later token can be created by it, wrong-order
  implementations are also invisible through this token on this snapshot. It is a null case for the
  order witness, not evidence about ordering.
- Claim-level implication for L1: a faithful instrument must report WIKIPEDIA raw-replacement count 0
  for each profile and must leave the 23 `sites` values untouched; any expectation or assertion of
  nonzero WIKIPEDIA replacements, or any replacement reaching `sites`, is contradicted by these bytes.
  Task/profile totals (812×3 = 2,436) are unaffected: this is a token-count fact, not a task-count fact.

## Source-versus-runtime boundary

Everything above is offline source/data evidence about one pinned snapshot. Nothing here observes or
predicts a running benchmark, an upstream environment launch, scorer/judge behavior, or any consumer of
the `sites` metadata array. Profile values are synthetic `*.invalid` fixtures; no deployment endpoint,
model, routing, credential, cookie or browser profile was read or contacted. No upstream code was
imported or executed; `scripts/generate_test_data.py` was treated strictly as inert data.

## Unknowns (kept open, not resolved by inference)

- U1: Whether upstream `dce04686…`'s `config_files/test.raw.json` genuinely lacks `__WIKIPEDIA__`, or
  whether the lane fixture differs from the manifest's URL. The pin↔bytes match is verified inside the
  lane; the URL identity is asserted by the manifest only and was not fetched (no endpoint requests).
- U2: Whether any other upstream config split (beyond the single pinned raw file) contains the token.
  Only one `config_files/*.json` exists in the fixture tree; no other upstream config was opened.
- U3: Why a retained fifth replacement step is inert on this revision (upstream history/intent) —
  not established, and not inferred from absence.
- U4: Whether an upstream runner consumes the `sites` metadata and how — runtime behavior, out of scope.
- U5: Production instrument agreement for this token: `plans/config_projection.py` is absent at HEAD
  `31934e5`, so there is no tool row to compare; the numbers above are raw-input facts, and tool
  verification is L1's step after all seats return.

## Exact commands and observed output (as run; lane root)

```
$ python3 -c '…hash/count…' plans/fixtures/r28/webarena/config_files/test.raw.json
bytes 880776
sha256 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652
codepoints 880776
ascii True
__WIKIPEDIA__ raw 0

$ python3 -c '…json leaf walk…' plans/fixtures/r28/webarena/config_files/test.raw.json
tasks 812 string_leaves 10869
decoded __WIKIPEDIA__ leaves 0
sites==wikipedia leaves 23
__GITLAB__ raw 385 decoded_leaves 385
__REDDIT__ raw 336 decoded_leaves 336
__SHOPPING__ raw 281 decoded_leaves 281
__SHOPPING_ADMIN__ raw 300 decoded_leaves 300
__WIKIPEDIA__ raw 0 decoded_leaves 0
__MAP__ raw 133 decoded_leaves 133

$ python3 -c '…six ordered replacements per profile…' plans/fixtures/r28/webarena/config_files/test.raw.json plans/fixtures/r29/profiles.json
distinct_origins len 905171 delta 24395
   … SHOPPING_ADMIN 300 5100 584c2a4a23891f9e03840fde64360ed896ac2a2aaedd84485dfc38cdbca79fee False
   WIKIPEDIA 0 0 584c2a4a23891f9e03840fde64360ed896ac2a2aaedd84485dfc38cdbca79fee True
   MAP 133 2261 2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4 False
   skip-step5 identical: True 2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4
path_prefix len 915216 delta 34440
   WIKIPEDIA 0 0 3b175917d754cdfcfcbd32bc61475ee16e56c68a75a21c2b66672347c75194bb True
   skip-step5 identical: True 54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b
trailing_slash_sensitivity len 906606 delta 25830
   WIKIPEDIA 0 0 ffb64e7c5dc9aaf7dfb36f26f324451f96880fde523c425adbc8abe863016a2c True
   skip-step5 identical: True 49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2
```

(Kernel-side scans additionally produced the 23-row offset table, the 10,869-leaf scanner-versus-
`json.loads` equality result, the 642 escaped-literal count, the 1,416 changed-leaf reconciliation and
the three boundary probes; all are reproducible from the retained bytes and the same stdlib logic.)

No installs, upgrades, package transactions or service changes were performed; no tool version changed.

VERDICT: PASS
