writer: KengakuR29-2.FRevEnvConfig-2

# FRevEnvConfig: env_config derivation and README export shape (round 29 falsify)

**Target.** How `browser_env/env_config.py` at upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b` derives its env-derived values, and whether that shape matches the README exports. Also attacked: the lane statements that depend on it (prereg six-token framing, S070/S072 anchors, candidate draft L22 and numeric lines).

**Boundaries.** Static reading only. Upstream text was read from the live raw URL (`read`, text) and fetched with curl and the codeload archive of the same commit; all hashes agree. Nothing upstream was imported, executed, or installed. Python snippets used fictitious `KENGAKU_R29_NOSUCH_*` names and `.invalid` hosts. I did NOT read `plans/config_projection.py` (production) or any oracle source. No credential, env value, or private URL is recorded: ACCOUNTS values, the literal non-placeholder host at `parallel_run.sh:11`, and a literal IP in a printed note at `minimal_example.py:46` are withheld.

## Headline findings

1. **Seven, not six.** `env_config.py` L4-L10 derive REDDIT, SHOPPING, SHOPPING_ADMIN, GITLAB, WIKIPEDIA, MAP, HOMEPAGE. The generator substitutes six (`generate_test_data.py` L11-L16). HOMEPAGE is the unsubstituted seventh.
2. **HOMEPAGE gates the generator.** `generate_test_data.py` L5 is `from browser_env.env_config import *`, which runs the module-level assert (`env_config.py` L12-L29) requiring HOMEPAGE to be non-empty. No HOMEPAGE token exists in the input. S070's anchors (main 8-23, replacements 11-16, parse 20, enumerate 21-23) omit L5.
3. **WIKIPEDIA is inert on the frozen input.** Generator L15 substitutes `__WIKIPEDIA__`, which occurs 0 times in the 812-task raw file (raw text and decoded strings). The 23 tasks with "wikipedia" in `sites` start at `__MAP__` (17) or `__GITLAB__` (6).
4. **Scheme-shape conflict.** README L86-L92 exports are scheme-less `<host>:<port>`. The other conventions (setup_env.sh, parallel_run.sh, minimal_example.py hints, environment_docker/README.md) use `http://` for every URL-valued name. The raw input carries no scheme anywhere, so the export's shape flows verbatim into navigation targets.
5. **`/admin` collision.** README L87 puts `/admin` inside SHOPPING_ADMIN. Raw task_id 374 and 375 have `eval.reference_url` beginning `__SHOPPING_ADMIN__/admin/`. Under the README/setup convention these become `/admin/admin/`, which the matcher's substring test (`evaluators.py` L223) cannot satisfy from a single-admin page path.
6. **HOMEPAGE sentinel.** README L92 documents `<your_homepage_domain>:4399` with the comment "this is a placeholder". `setup_env.sh` L34 sets `"PASS"` and `minimal_example.py` L41 prints `'PASS'`. env_config checks truthiness only, so `PASS` passes and becomes a URL_MAPPINGS key, which the prompt rewriter applies as a substring replacement.

## 1. Pinned artifacts (observed)

| artifact @dce04686 | bytes | sha256 | check |
|---|---|---|---|
| browser_env/env_config.py | 1417 (51 lines) | fcec91a2dafd5db16bb390ac5a6fd930ef59c6ef54445b85f7625d8f9404abd7 | live-URL read (text); curl copy and codeload archive identical |
| README.md | 9717 | 081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287 | equals S072 hash |
| scripts/generate_test_data.py | 838 | 45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd | equals manifest pin |
| config_files/test.raw.json | 880776 | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 | equals manifest pin; 812 top-level items |
| docs.python.org reference/expressions.html (label Python 3.15.1) | 273904 | bcefd36ab8f6ca1c691d8c5c3fc1faf33d4adad5ac620b7f4b19fce78a03efa6 | accessed 2026-10-21 |
| docs.python.org reference/simple_stmts.html | 127774 | c0dde64b2eed1992587e81d44ce8c31d8cae84186fe070b070aeef2a27f25627 | accessed 2026-10-21 |

## 2. How env_config derives its values (static, line-cited)

- L4-L10: seven module names, each `NAME = os.environ.get("NAME", "")`. Pure pass-through with empty-string default: no strip, parse, scheme handling, or validation.
- L12-L29: module-level `assert` over the conjunction of all seven names (L13-L19). The message (L21-L28) interpolates all seven values and is evaluated only on failure.
- L32-L41: `ACCOUNTS` literal with five keys (reddit, gitlab, shopping, shopping_admin, shopping_site_admin), each holding username/password literals. Not env-derived. Values withheld.
- L43-L51: `URL_MAPPINGS` keyed by the seven env VALUES (L44-L50), mapped to hard-coded canonical literals. Keys are values, not names.
- Derived set {REDDIT, SHOPPING, SHOPPING_ADMIN, GITLAB, WIKIPEDIA, MAP, HOMEPAGE} has size 7. README exports (L86-L92) have the same 7 names (set-equal). Order differs; env_config has no order dependence.

## 3. Attack log

| # | attack | result |
|---|---|---|
| A1 | count env-derived values | FAILED premise: 7 (env_config L4-L10) |
| A2 | README names vs env_config names | HOLDS: set-equal, 7 = 7 |
| A3 | generator tokens and order vs prereg | HOLDS: L11-L16 = GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP |
| A4 | is HOMEPAGE required at import | YES: env_config L19; generator L5; auto_login.py L12; prompt_constructor.py L7 |
| A5 | is HOMEPAGE substituted anywhere | NO: no generator line; 0 occurrences in raw text or decoded strings |
| A6 | does WIKIPEDIA change generated configs | NO: 0 `__WIKIPEDIA__` in raw text or decoded strings |
| A7 | unreplaced env tokens in raw | NO. Only `__last_url__` (65) and `__page__` (12) remain; evaluators substitute them at runtime (evaluators.py L265, L298) |
| A8 | scheme shape, README vs repo | MISMATCH (M4) |
| A9 | scheme inside raw input | NONE: 0 `http://__`, 0 `https://__`; 812/812 start_url begin with a bare token |
| A10 | README suffix vs raw suffix | MISMATCH for SHOPPING_ADMIN `/admin` (M7); none for the other six |
| A11 | does CI import env_config | REFUTED by static import graph (M11) |
| A12 | README CI pointer | MISMATCH (M11) |
| A13 | does env_config validate shape | NO: truthiness only (M10) |
| A14 | duplicate values and `-O` | semantics confirmed by witness; run-level consequence INFERENCE (M9) |
| A15 | HOMEPAGE placeholder semantics | MISMATCH (M6) |
| A16 | host handling for scheme-less references in URL matcher | parse CONFIRMED; consequence INFERENCE (M8) |
| A17 | candidate draft claims | L22 contradicted (M1); numeric lines verified (section 8) |

## 4. Mismatches (exact location and value)

**M1 Count.** `env_config.py` L4-L10 derive seven values. Draft `drafts/webarena-config-projection.md` L22 says the import "supplies the six values". The six are the generator's replacement subset (`generate_test_data.py` L11-L16), not everything env_config derives.

**M2 Import gate omitted by the lane.** `generate_test_data.py` L5 executes env_config at import. The assert at env_config L12-L29 raises AssertionError if HOMEPAGE, or any of the six, is empty, before `main()` (L8) runs. Source-level, not executed here [INFERENCE from Python import and assert semantics]. Also gated: `auto_login.py` L12-L18 and `prompt_constructor.py` L7. The prereg's "never imports upstream code, including browser_env.env_config" is a design choice, but it leaves this precondition unmodeled.

**M3 WIKIPEDIA inert on the population.** `generate_test_data.py` L15 `raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)` replaces nothing: raw has 0 `__WIKIPEDIA__` (text and decoded). README L91's export therefore affects no generated config. The 23 tasks with "wikipedia" in `sites` start at `__MAP__` (17) or `__GITLAB__` (6). WIKIPEDIA's remaining roles are the env_config L17 gate, the L48 URL_MAPPINGS key, and `evaluation_harness/helper_functions.py` L16, which imports it with no other occurrence in that file.

**M4 Scheme-shape conflict.**
- README L86-L92: `export NAME="<your_..._domain>:port[/path]"`. No scheme.
- `setup_env.sh` L28-L33: `export NAME="http://${SERVER_HOST}:port..."`. L34 is `export HOMEPAGE="PASS"`.
- `parallel_run.sh` L11: all seven names exported as `http://${SERVER}:...`.
- `minimal_example.py` L33-L39: hints `http://YOUR_WEBARENA_SERVER:...`.
- `environment_docker/README.md` L205 and L227: `http://<your-server-hostname>:...`.
- Consumers: generator L11-L16 is a verbatim `str.replace`. All 812 `start_url` values begin with a bare token, so each carries the env value's shape. `envs.py` L151 splits `start_url` on the multi-URL separator and L160 calls `page.goto(url)` with no scheme added. `auto_login.py` L26-L28 concatenates `{GITLAB}/-/profile`, `{SHOPPING}/wishlist/`, `{SHOPPING_ADMIN}/dashboard`; L87 is `page.goto(f"{SHOPPING_ADMIN}")`.
- WHATWG parse (node v24.21.0, W6): scheme-less `k.invalid:7770/wishlist/` gives protocol `k.invalid:` and empty host. Scheme-included gives host `k.invalid:7770`.
- NOT VERIFIED: whether Playwright/Chromium navigates a scheme-less `goto` target. No browser run; no upstream execution.

**M5 URL_MAPPINGS keyed by value; substring rewrite.** env_config L44-L50 keys are env values. `prompt_constructor.py` L122-L127 loops `for i, j in URL_MAPPINGS.items()`, applies `if i in url:` then `url = url.replace(i, j)`, and is called on `page.url` (L177-L178, used at L184). With a scheme-less key and a loaded page URL (which carries `http://`), the result is `http://http://...` (W4a). Scheme-included keys (the repo's setup scripts) give the intended URL (W4b). Conditional on page.url carrying the scheme, which holds for a loaded http page.

**M6 HOMEPAGE: README vs repo.** README L92 `export HOMEPAGE="<your_homepage_domain>:4399" # this is a placeholder` (documented as a placeholder with port 4399). `setup_env.sh` L34 `export HOMEPAGE="PASS"`. `minimal_example.py` L41 `print("export HOMEPAGE='PASS'")` while L20 lists HOMEPAGE as required. env_config L19 accepts "PASS" because the gate is truthiness. The key `PASS` enters URL_MAPPINGS (L50), so any observed URL containing uppercase `PASS` is rewritten by M5's loop (W5 alters `PASSWORD` in a path). `parallel_run.sh` L11 uses `http://${SERVER}:4399`, agreeing with README's port, not with `setup_env.sh`.

**M7 `/admin` collision in two raw tasks.**
- README L87: `export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"` (suffix inside the value).
- Raw task_id 374 and 375: `eval.reference_url` = `__SHOPPING_ADMIN__/admin/system_design_theme/edit/id/...`. `eval_types` ['url_match'], `url_note` 'GOLD in PRED', `sites` ['shopping_admin'].
- Under the README/setup convention these expand to `...:7780/admin/admin/system_design_theme/edit/id/...`.
- Matcher: `evaluators.py` L212 `pred = clean_url(page.url)`, L213 splits the reference, L192-L197 `parse_url` returns `netloc + path` as a string, L223 `ref_base_path in pred_base_paths` is a substring test.
- So a single-admin page path does not contain the doubled segment, and url_match cannot return 1 for these two tasks under this convention [INFERENCE: static; admin route not observed]. The other 298 SHOPPING_ADMIN occurrences do not collide.
- The conflict is in the raw data. auto_login's `{SHOPPING_ADMIN}/dashboard` presupposes `/admin` inside the value, and tasks 374/375 presuppose it is absent [INFERENCE from URL structure].

**M8 Scheme-less references lose their host in matching (silent).** `evaluators.py` L195 `base_path = parsed_url.netloc + parsed_url.path`. For a letter-leading host with no scheme, `urlparse` puts the host into the scheme and leaves netloc empty (W7). The reference base reduces to `port/path`. L223 is a substring test, so that reference matches any page whose base contains `port/path`. The host is not compared. Not a crash. [Parse verified; consequence INFERENCE.]

**M9 Value-keyed URL_MAPPINGS; `-O` removes the gate.** Duplicate env values collapse silently (no uniqueness check). Python 3.15.1 docs: "the final dictionary’s value for a given key will be the last one given" (W3). Under `python -O` the assert at env_config L12-L29 is compiled out. Python docs: "The current code generator emits no code for an assert statement when optimization is requested at compile time." Unset values then all key to `""` (W1), and generator L11-L16 substitutes empty strings with no error. [INFERENCE for the run-level outcome; semantics verified on a fictitious replica.]

**M10 No shape validation; failure message echoes values.** The gate checks truthiness only (L13-L19). `os.environ.get` values are not stripped (L4-L10), so whitespace-only passes. The failure message (L21-L28) prints all seven configured values (not recorded here). Low severity.

**M11 Stale README CI pointer; CI import hypothesis refuted.** README L95 says to update env "in github workflow (.github/workflows/tests.yml#L7)". `tests.yml` is 32 lines, has no `env:` block, names none of the seven variables, and line 7 is `strategy:`. The hypothesis that CI imports env_config and fails at collection is REFUTED: the static import graph over 44 `.py` files finds that six test-like files (`tests/conftest.py`, `tests/test_browser_env/{test_action_functionalities,test_actions,test_auth_cookie,test_playwright_actions,test_script_browser_env}.py`) do not reach `browser_env/env_config.py`. Direct importers are `prompt_constructor.py`, `auto_login.py`, `helper_functions.py`, `scripts/collect_obs.py`, `scripts/generate_test_data.py`.

**M12 Credential-shaped literal data in the module.** env_config L32-L41 `ACCOUNTS`: five keys with username/password literal pairs, consumed by `auto_login.py` L13 and `helper_functions.py` L10. Not env-derived. Values withheld. The prereg already flags this.

**M13 Literal non-placeholder host in upstream scripts (hygiene).** `parallel_run.sh` L11 MAP entry is a literal hostname rather than `${SERVER}`; value withheld. `minimal_example.py` L46 prints a literal IP address (withheld). Not env_config.

**Checked, not a mismatch.** The README port numbers agree with `setup_env.sh`, `minimal_example.py` hints, and `parallel_run.sh` for all six non-HOMEPAGE names, and for HOMEPAGE's port in `parallel_run.sh`. `__last_url__` and `__page__` are runtime placeholders, not env residue.

## 5. Name x shape matrix

`<H>` is a README `<your_..._domain>` placeholder. Line numbers are in the named file.

| name | README line and value shape | env_config def / assert / URL_MAPPINGS key | generator line (raw occurrences) | setup_env.sh line, scheme | minimal_example required / hint line | parallel_run.sh L11 scheme |
|---|---|---|---|---|---|---|
| SHOPPING | 86, `<H>:7770` | 5 / 14 / 45 | 13 (281) | 28, http | 14 / 33 | http |
| SHOPPING_ADMIN | 87, `<H>:7780/admin` | 6 / 15 / 46 | 14 (300) | 29, http | 15 / 34 | http |
| REDDIT | 88, `<H>:9999` | 4 / 13 / 44 | 12 (336) | 30, http | 16 / 35 | http |
| GITLAB | 89, `<H>:8023` | 7 / 16 / 47 | 11 (385) | 31, http | 17 / 36 | http |
| MAP | 90, `<H>:3000` | 9 / 18 / 49 | 16 (133) | 32, http | 18 / 37 | http, literal host (withheld) |
| WIKIPEDIA | 91, `<H>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing` | 8 / 17 / 48 | 15 (0) | 33, http | 19 / 39 | http |
| HOMEPAGE | 92, `<H>:4399` ("placeholder") | 10 / 19 / 50 | none (0) | 34, `PASS` | 20 / 41 (`PASS`) | http |

## 6. Witnesses (run with python3 3.14.8 / node v24.21.0; no upstream code)

- W1 replica of the env_config dict pattern under `-O`, fictitious names: `-O | assert skipped | dict len: 1 | keys: ["''"] | value for key: 'http://other.invalid'`
- W1b same without `-O`: `default | AssertionError raised before dict built`
- W3 duplicate display keys: `dup keys -> {'k.invalid:7770': 'last'}`
- W4a `"http://k.invalid:7770/wishlist/".replace("k.invalid:7770", "http://target.invalid")` gives `'http://http://target.invalid/wishlist/'`
- W4b `.replace("http://k.invalid:7770", "http://target.invalid")` gives `'http://target.invalid/wishlist/'`
- W5 `"http://site.invalid/PASSWORD-reset".replace("PASS", "http://target.invalid")` gives `'http://site.invalid/http://target.invalidWORD-reset'`
- W6 node WHATWG: `new URL("k.invalid:7770/wishlist/")` gives protocol `k.invalid:`, host `""`. `new URL("http://k.invalid:7770/wishlist/")` gives protocol `http:`, host `k.invalid:7770`.
- W7 `urllib.parse.urlparse("example.invalid:9999/f/books")` gives scheme `example.invalid`, netloc `""`, path `9999/f/books`. `urlparse("http://example.invalid:9999/f/books")` gives netloc `example.invalid:9999`, path `/f/books`.
- W8 static import graph (`ast.parse` only): 44 `.py` files; test-like files reaching env_config: none; direct importers: 5 (listed in M11).
- W9 raw counts (python json, pinned bytes): occurrences GITLAB 385, REDDIT 336, SHOPPING_ADMIN 300, SHOPPING 281, MAP 133, WIKIPEDIA 0, HOMEPAGE 0, `__last_url__` 65, `__page__` 12. `__SHOPPING_ADMIN__/admin` 2 (task_id 374, 375). `http://__` 0, `https://__` 0. start_url leading token: SHOPPING_ADMIN 182, MAP 128, SHOPPING 192, REDDIT 114, GITLAB 196 (sum 812). start_url containing ` |AND| `: 5. `url_note` for url_match tasks: 'GOLD in PRED' 196, absent 9 (default applies).

## 7. Located quotes (counted with `len(s.split())`; limit 25)

| words | location | quote |
|---|---|---|
| 4 | env_config.py L4 | `REDDIT = os.environ.get("REDDIT", "")` |
| 4 | env_config.py L10 | `HOMEPAGE = os.environ.get("HOMEPAGE", "")` |
| 2 | env_config.py L19 | `and HOMEPAGE` |
| 4 | generate_test_data.py L5 | `from browser_env.env_config import *` |
| 4 | generate_test_data.py L15 | `raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)` |
| 2 | README.md L86 | `export SHOPPING="<your_shopping_site_domain>:7770"` |
| 7 | README.md L92 | `export HOMEPAGE="<your_homepage_domain>:4399" # this is a placeholder` |
| 11 | README.md L95 (part) | You are encouraged to update the environment variables in github workflow |
| 9 | README.md L101 (part) | Each file contains the configuration for one test example. |
| 2 | setup_env.sh L34 | `export HOMEPAGE="PASS"` |
| 2 | minimal_example.py L41 | `print("export HOMEPAGE='PASS'")` |
| 4 | prompt_constructor.py L126 | `url = url.replace(i, j)` |
| 1 | envs.py L160 | `page.goto(url)` |
| 1 | auto_login.py L87 | `page.goto(f"{SHOPPING_ADMIN}")` |
| 7 | environment_docker/README.md L227 | The homepage will be available at `http://<your-server-hostname>:4399`. |
| 18 | Python docs, simple_stmts (Python 3.15.1) | The current code generator emits no code for an assert statement when optimization is requested at compile time. |
| 14 | Python docs, expressions (Python 3.15.1) | the final dictionary’s value for a given key will be the last one given |
| 9 | draft L22 (part) | supplies the six values; the import never runs here |

## 8. Lane-claim checks

- **S070** (`corpus/SOURCES.md` L92): main 8-23 OK; replacements 11-16 OK, order matches prereg; `json.loads` 20 OK; enumerate 21-23 OK; bytes and sha OK. The import at L5 is not cited (M2).
- **S072** (L94): README lines 79, 84-92, 95, 97-101 OK; sha OK; "scheme-less example origin:port" OK. Consequences not stated (M4, M7).
- **Prereg** (`plans/round-29-claims.md`): six replacements in order OK. Import gate not modeled (M2).
- **Draft** `drafts/webarena-config-projection.md`: L22 contradicted (M1, M2). L41 OK: 385, 336, 281, 300, 0, 133 sum 1435. L42 OK: tasks carrying each token 204, 128, 192, 182, 0, 128 sum 834; all 812 tasks carry at least one env token. L43 OK: 1416 changed value leaves of 10869; 13 with more than one occurrence. L44 partly OK: start_url 812 and reference_url 205 recomputed; program_html 338 not recomputed here. L45 not checked here. L46 consistent (no env residue; 65 and 12 other markers). L59 OK: WIKIPEDIA 0; 5 of 6 tokens exercised.

## 9. Verdict

**VERDICT: PARTIAL**, scoped to this item.

- Holds: the generator's six-token set and order, the README-to-env_config name set (7 = 7), and the draft's L59 WIKIPEDIA claim (0 occurrences; 5 of 6 tokens exercised).
- Fails: the "six values" premise for env_config (7 derived; HOMEPAGE import-gated and absent from S070's anchors, M1-M2); the README value shape against the repo's own conventions, runtime consumers, and the raw input (M4-M6); the `/admin` collision in tasks 374 and 375 (M7).
- Not a round admission. No measurement, method, deployment, or task-validity claim is made.

## 10. Tooling and record

- Installs or upgrades: none. Existing tools used: curl 8.23.0, node v24.21.0, python3 3.14.8, system sha256sum, wc, tar.
- Network: raw.githubusercontent.com (live URLs), codeload.github.com (archive of commit dce04686), docs.python.org. No pacman, no service restarts, no REA devices.
- Writes: this report; scratch under `.ufo/waves/round-29/scratch/falsify/FRevEnvConfig/` (README.pinned.md, generate_test_data.pinned.py, shape_matrix.json, quote_counts_final.json, quote_word_counts.json, candidate_token_counts_check.json). The env_config scratch copy was deleted because it contains credential-shaped literals; its sha256 is in section 1. The /tmp extraction was removed after the run.
- Production source: `plans/config_projection.py` NOT read. Oracle source: not read. Lane artifacts read only: `plans/round-29-claims.md`, `plans/fixtures/r29/manifest.json`, `corpus/SOURCES.md` L92-L94, the draft (grep and L22/L41-L59 values).

VERDICT: PARTIAL
