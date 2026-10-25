# R29 contract recon — `browser_env.env_config` wildcard dependency is inert; AST anchors vs hand-read

**Seat / actual writer:** `KengakuR28.R29ContractInertImports-2` (same). Read-only leaf; no subagents, no production edits, no commits, no network.
**Scope:** one slice of C1 source-contract reconnaissance — the pinned generator's sole upstream dependency (`from browser_env.env_config import *`), its static binding semantics, exact AST line/column anchors versus hand-read claims, and hand-expected counterexamples to wrong interpretations. Not a round admission, not a capability row, not an oracle comparison.
**Prereg:** `plans/round-29-claims.md` (repo `31934e5660f1814326c6472eefdfa0c41e642a2f`), manifest `plans/fixtures/r29/manifest.json` sha256 `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`.
**Tool installs:** none (stdlib `python3`, `sha256sum`, `wc`, `find`, `grep` only).
**Semantic-tool note:** this seat has no `lsp` device in its tool inventory, so no language-server answer was available; `ast.parse` of the retained bytes is the semantic evidence here, and literal `grep` was used only for a file-presence scan (never presented as semantic proof).

## Godspeed axes

| Axis | Question for this slice |
|---|---|
| Novelty | Does the wildcard dependency change what the artifact can claim, beyond “six replacements”? |
| Fidelity | Are line/column anchors and binding semantics exact, not hand-approximated? |
| Safety | Is the route to values structurally excluded (no import, no host env, no auth files)? |
| Bounded surface | Is the remaining unknown named instead of filled with plausible defaults? |

## Pinned open (no fetch performed)

The manifest records source URL `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py` and access date `2026-10-21`. This seat made **no** endpoint/site request (contract forbids it); the URL is transcribed from the pin, and the local bytes are the evidence.

| Artifact | Absolute path | Bytes | sha256 (computed) | Pin match |
|---|---|---:|---|---|
| generator | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | manifest ✓ |
| manifest | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json` | — | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | plan ✓ |
| raw specs | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json` | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | manifest ✓ |
| profiles | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json` | — | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | manifest ✓ |
| sibling pin (below) | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` | 7565 | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | r28 manifest ✓ |

Remote-vs-local byte identity is **not** independently verified in this seat (no fetch); the hash chain above is the whole basis. That stays an unknown.

## Exact located quotes (word count = `len(quote.split())`, verified as in-line substring)

| Line | Quote | Words |
|---:|---|---:|
| 1 | `Replace the website placeholders with website domains from env_config` | 9 |
| 3 | `import json` | 2 |
| 5 | `from browser_env.env_config import *` | 4 |
| 9 | `with open("config_files/test.raw.json", "r") as f:` | 5 |
| 10 | `raw = f.read()` | 3 |
| 11 | `raw = raw.replace("__GITLAB__", GITLAB)` | 4 |
| 13 | `raw = raw.replace("__SHOPPING__", SHOPPING)` | 4 |
| 14 | `raw = raw.replace("__SHOPPING_ADMIN__", SHOPPING_ADMIN)` | 4 |
| 16 | `raw = raw.replace("__MAP__", MAP)` | 4 |
| 17 | `with open("config_files/test.json", "w") as f:` | 5 |
| 18 | `f.write(raw)` | 1 |
| 20 | `data = json.loads(raw)` | 3 |
| 21 | `for idx, item in enumerate(data):` | 5 |
| 23 | `json.dump(item, f, indent=2)` | 3 |
| 26 | `if __name__ == "__main__":` | 4 |
| hf 9 | `from browser_env.env_config import (` | 5 |
| hf 10 | `ACCOUNTS,` | 1 |

(`hf` = sibling `evaluation_harness/helper_functions.py`, same pinned revision.) Line-1 quote is the first physical line of the single docstring `Constant` that AST reports spanning lines 1–2; the substring check is against physical line 1.

## AST anchors (executed on retained bytes; `ast.parse` only, no import/exec)

| Anchor | AST observation |
|---|---|
| star import | `ImportFrom(module='browser_env.env_config', names=[alias(name='*', asname=None)])`, line 5, cols 0–36 (whole line) |
| module-level bindings | exactly `json` (line 3), `*` (line 5), `main` (line 8); no other assignment at module scope |
| six token names | `Name` nodes in `Load` context only, lines 11–16, cols 36, 36, 38, 44, 39, 33 (no `Attribute`, no `Store`) |
| six replace calls | `Call.func=Attribute(value=Name('raw'), attr='replace')`, cols 10→43, 10→43, 10→47, 10→59, 10→49, 10→37 |
| read / parse / enumerate | `f.read()` line 10 col 14; `json.loads` line 20 col 11; `enumerate` line 21 col 21 |
| per-task emit | `open(f"config_files/{idx}.json", "w")` line 22; `json.dump(item, f, indent=2)` line 23 col 12 |
| string constants | 15 total; dunder literals are `__main__` plus exactly the six tokens; no other `__…__` literal anywhere |
| absent constructs | no `__all__`, no `os.`/`environ`, no `urllib`/`urlparse`, no exception handling, no encoding argument on any `open` |

## Hand-read claims corrected by the anchors

| Plausible hand-read | Anchored observation |
|---|---|
| “six replacements are lines 10–15” | 1-based lines 11–16; line 10 is `f.read()` |
| “test.json is written on line 17” | the `with` is line 17; `f.write(raw)` is line 18 |
| “the star import is five words” | `len(split())` = 4 |
| “replace calls share a column width” | end columns 43/43/47/59/49/37; only the first two coincide |
| “`__SHOPPING__` also matches inside `__SHOPPING_ADMIN__`” | substring containment is false both ways; the 11th character of `__SHOPPING_ADMIN__` is `A`, not `_` |
| “read/parse/write are one visible step” | read line 10, `test.json` write line 18, `json.loads` line 20; the file is written before the JSON is validated |

The last row is only an anchor corroboration inside my slice; output-order ownership stays with its own seat.

## The wildcard dependency: what it does and does not contribute

File-presence census (literal `find`/`glob`, whole lane, git dirs excluded): **no** `browser_env` directory and **no** `env_config*` file exists anywhere under the lane, and no lane production module references `env_config` yet (`plans/config_projection.py` absent; `ls` → no such file). Consequences:

1. The generator cannot be imported in-lane even if someone tried; more importantly, it must not be. `import *` executes `browser_env/env_config.py` module-level code at import time (line 5 is unconditional, outside the `if __name__ == "__main__"` guard at line 26, which protects only `main()`).
2. The pinned bytes define **token spellings, RHS names, order and `str` semantics only**. There is no literal default, no `__all__`, no environment read, no network call. Therefore the substitution value domain is *external to the artifact* and can only be supplied by `profiles.json`.
3. Cross-artifact witness that `env_config` exposes more than six names: the same pinned upstream revision's `helper_functions.py` (r28 fixture) imports `ACCOUNTS` alongside the six names by name (lines 9–17). So a `*` import can bind credential-bearing names into the generator namespace, although the generator uses six. Whether `import *` actually binds `ACCOUNTS` depends on `env_config.__all__`, which is **unopened and unknown** — the point is that the binding set is not derivable from the 838 pinned bytes.
4. Ordering hazard from the anchors: the star import (line 5) executes *after* `import json` (line 3). Any public `json` attribute in `env_config` would rebind the module name for lines 20 and 23, so `json.loads`/`json.dump` would resolve to a foreign object.

Synthetic seat-owned demo (my two-line module, not upstream, scratch `…/.ufo/waves/round-29/scratch/KengakuR28.R29ContractInertImports-2/envcfg_demo.py`, sha256 `f908272f1c98d724d610751dbfcb50f5171bfe3827682e945865eb76bffdd569`) observed: after `from envcfg_demo import *`, the name `json` is the fixture string and `json.loads("[]")` raises `AttributeError: 'str' object has no attribute 'loads'`; a named `from envcfg_demo import MAP` raises `ImportError`; the star form binds no `MAP` silently. That is the shape of the wildcard failure mode, not a claim about upstream.

## Hand-expected counterexamples to wrong interpretations

**A. “The star import equals six named imports, so a tool may resolve the six values from `env_config`.”**
Expected under the language rule: the star form validates nothing (missing `GITLAB` would fail only as a `NameError` at line 11 during `main()`), while named imports fail at import time; and the star form additionally rebinds any public `json`. Hand-expected output of my fixture: `json.loads` → `AttributeError`; `from … import MAP` → `ImportError`. Any audit that reports “values resolved from source” is reporting host/credential state as source metadata — the pinned artifact contains no values.

**B. “URL-only substitution is faithful.”**
Census on the frozen raw text (independent, my own parse): tokens occur in 61 non-URL-heuristic leaves — `eval.program_html[*].required_contents.must_include` 60 leaves (GITLAB 8 + REDDIT 52 occurrences) and `eval.reference_answer_raw_annotation` 1 leaf (REDDIT 2 occurrences). Expected: a field-name URL heuristic leaves 61 leaves and 62 occurrences unsubstituted, diverging from upstream `str.replace` on serialized text. Tokens appear in string values only, never in JSON keys, on this input.

**C. “Rule order does not matter because the tokens are distinct.”**
Expected forward cascade, hand-computed: with GITLAB value `http://gitlab.invalid:10101/__MAP__` and text `A __GITLAB__ B __MAP__`, ordered passes give `A http://gitlab.invalid:10101/http://map.invalid:10106 B http://map.invalid:10106`, while reversing the order leaves `__MAP__` inside the inserted value: `A http://gitlab.invalid:10101/__MAP__ B http://map.invalid:10106`. The adjacent pair is also order-bearing by cascade, not prefix overlap: with SHOPPING value `http://shopping.invalid:10103/__SHOPPING_ADMIN__`, text `__SHOPPING__/x` ordered → `http://shopping.invalid:10103/http://shopping-admin.invalid:10104/x`; swapping only rules 3 and 4 → `http://shopping.invalid:10103/__SHOPPING_ADMIN__/x`.

**D. “`str.replace` rescans, so six passes reach a fixpoint.”**
Expected: single left-to-right pass, no rescan of inserted text; MAP value `__MAP__` yields `__MAP__` unchanged. Therefore “remaining known placeholders = 0” is an emergent property of the three frozen profiles (none contains a token), not a law of the generator; the summary must report residuals per profile rather than assert zero. On the frozen input `__WIKIPEDIA__` occurs 0 times, so the fifth rule is a **no-op** there — “six replacements executed” must not be read as “six replacements effective.”

**E. “Codepoint offsets can be reported as byte offsets because they coincide here.”**
Observed: the raw file is pure ASCII — 880776 bytes = 880776 codepoints, 0 non-ASCII characters — so the numbers coincide *for this input only*. Hand case: insert one `é` (1 codepoint, 2 UTF-8 bytes) before a token at codepoint offset k; the byte offset becomes k+1. Offsets must stay labelled codepoints (`str` indexing), and they address the pre-projection text; projected text has different lengths, so raw offsets cannot be reused on output.

## Source metadata versus runtime configuration

The docstring's “website domains from env_config” is **source intent**, not an observed deployment: the pinned bytes carry no domain, port, or credential. Raw tasks are templates — `require_login` is true for 812/812 items, and 684 items carry relative auth-state paths `./.auth/{shopping,gitlab,shopping_admin,reddit,gitlab.reddit}_state.json` (187/186/182/111/18; 128 items `null`) — all of which stay unread. `sites` lists such as `["map","wikipedia"]` describe task scope metadata, not verified site state. The wildcard's real upstream values, and therefore the actual substituted hosts of any real run, remain **unknown and unobserved** by this instrument; an offline projection under `*.invalid` fixtures is not runtime configuration and cannot support deployment or model-behavior claims.

## Units kept separate (no pooling)

Observed on the frozen input with my own parse: 812 tasks, 812 distinct `task_id`, 3 profiles → 2436 task/profile projections; `output_index == task_id` for 812/812 (the shuffled witness belongs to selftest). Serialized occurrence counts per token: GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133 (sum 1435). Changed decoded leaves by terminal field: `start_url` 812, `url` 338, `reference_url` 205, `must_include` 60, `reference_answer_raw_annotation` 1 (sum 1416). 1435 ≠ 1416 because multiple serialized hits collapse into one decoded leaf; occurrence, leaf and task counts are distinct units. `__last_url__` (65) and `__page__` (12) are runtime markers, not environment tokens, and must not enter the six-token residuals.

## Preserved unknowns

- Remote URL bytes were never fetched in this seat; source identity rests on the manifest hash chain.
- `env_config` contents, `__all__`, value types and values are unopened: unknown by construction (may include credentials).
- Whether real upstream values would make any profile-like substitution valid — not evaluated; synthetic `*.invalid` fixtures only.
- No implementation of `plans/config_projection.py` exists in the lane at this seat, so no execution, `--summary` count, exit code or oracle agreement is observed here.
- F1–F5 forecasts are not scored; capability row and canonical knowledge stay deferred to L1.

## Commands actually executed

```text
sha256sum plans/fixtures/r29/{generate_test_data.py,manifest.json,profiles.json} \
          plans/fixtures/r28/webarena/config_files/test.raw.json \
          plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py
wc -c plans/fixtures/r29/generate_test_data.py plans/fixtures/r28/webarena/config_files/test.raw.json
find /…/kengaku-shokunin -name 'env_config*' -not -path '*/.git/*'   → no output
python3 (stdlib) ast.parse on the 838 retained bytes → anchors, bindings, constants
python3 (stdlib) json/str census on the raw text → token/field/leaf/index/storage_state counts
python3 (stdlib) hand-case string computations → counterexample expected outputs
python3 (stdlib) synthetic fixture import demo in seat scratch → wildcard shadow/missing-name behavior
grep (tool) for `env_config` under plans/ → prereg text, generator line 5, helper_functions lines 9–17
```

Report: `.ufo/waves/round-29/build/R29ContractInertImports.md`

VERDICT: PASS

Scoped to: read-only reconnaissance of the wildcard `browser_env.env_config` dependency and exact AST anchors in the pinned 838-byte generator, with hand-expected counterexamples and source-vs-runtime boundaries. It does not admit round closure, does not certify `plans/config_projection.py` (absent), and does not claim oracle agreement, deployment configuration, or task validity.
