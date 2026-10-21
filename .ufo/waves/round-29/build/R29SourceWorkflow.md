# R29SourceWorkflow — S072 README generated-config workflow / env-variable constraints

seat: KengakuR28.R29SourceWorkflow-2
writer: KengakuR28.R29SourceWorkflow-2 (leaf; no delegation, no production edit)
date: 2026-10-21
scope: one pinned README opened this round; a proposed S072 row and its bounded evidence. This is not a
round admission, not a knowledge-entry admission, and not a runtime/deployment observation.

## Source opened

- URL: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/README.md
- Access date: 2026-10-21. Fetch: `curl -sS --max-time 60` returned
  `http_code=200 size_download=9717 content_type=text/plain; charset=utf-8`.
- Bytes as fetched: 9717 bytes, SHA256 `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287`;
  162 newline characters (`wc -l -w -c`: `162 1023 9717`); 1023 whitespace-separated tokens for the
  whole file.
- The URL is commit-pinned, but this SHA256 is this seat's snapshot hash only. The r29 manifest pins the
  generator, raw task file and profiles; it does not pin README, so this hash cannot be used as a
  manifest-level rebinding guard.
- Retention: the full page was written to scratch, hashed and measured, then deleted. Retained only a
  7-line excerpt (418 bytes, SHA256
  `c4de52237d3ae0b7eff85be10eab91890a633bd7c1cf8d5b11a423136720b697`) and a small metadata JSON under
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29SourceWorkflow-2/`.
  The page contains no credential values; nothing from auth flows, cookie stores or browser profiles was
  read or retained.

## Located quote

Lines 86–92, contiguous (no elision, no folded excerpt). Word count measured two ways on the exact
retained excerpt bytes: Python `str.split()` = 19, GNU `wc -w` = 19. Unicode codepoints = 418; the
excerpt is ASCII, so bytes equal codepoints here. The excerpt occurs exactly once in the 9717-byte page.

```
export SHOPPING="<your_shopping_site_domain>:7770"
export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"
export REDDIT="<your_reddit_domain>:9999"
export GITLAB="<your_gitlab_domain>:8023"
export MAP="<your_map_domain>:3000"
export WIKIPEDIA="<your_wikipedia_domain>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"
export HOMEPAGE="<your_homepage_domain>:4399" # this is a placeholder
```

The values are user-supplied placeholders in the source; none is a real domain, host or credential.

## Proposed S072 row (PROPOSAL ONLY — SOURCES.md was not edited)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S072 | WebArena generated-config workflow and environment-variable constraints — https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/README.md | docs | A | what this README documents about the site-URL exports and the separate per-example config-generation step; not env_config values, deployment URLs or task validity | dce04686, README.md lines79,84–92,95,97–101; sha256 081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287 (2026-10-21 bytes; snapshot hash, not a manifest pin) | seven exported variables in scheme-less example origin:port form (SHOPPING_ADMIN adds /admin, WIKIPEDIA adds a long path, HOMEPAGE is marked placeholder), then step 3 runs scripts/generate_test_data.py and writes one config file per example; the README states no replacement order or token inventory | queued | 2026-10-21 | on-release | — |

Rationale for cells: kind `docs` (README prose, not the generator `code`); tier `A` only for what this
README states about its own workflow; `queued` because the row is opened but no admitted entry cites it
yet; `used-by` left as `—` until a round-29 knowledge entry is actually admitted.

## Located README statements (observed, not extended)

- Lines 84–92: step 2, "Configurate the urls for each website." The fenced block exports exactly seven
  names in this order: SHOPPING, SHOPPING_ADMIN, REDDIT, GITLAB, MAP, WIKIPEDIA, HOMEPAGE. No value has a
  URL scheme. SHOPPING_ADMIN's example carries an `/admin` path; WIKIPEDIA's carries a long path ending
  `Landing`; HOMEPAGE's line carries the literal comment "this is a placeholder".
- Line 95: points readers to `.github/workflows/tests.yml#L7` for environment variables used by unit
  tests. That workflow file was not opened in this seat.
- Lines 97–101: step 3, "Generate config file for each test example", runs
  `python scripts/generate_test_data.py`, and states that generated `*.json` files appear in
  `config_files`, each holding the configuration for one test example.
- Line 79: names 812 examples and says the demo sites are browsing-only, with the reader's own sites
  required for correct evaluation. This is a README statement, not a measured population in this seat.
- Line 108: documents an API-key environment variable as a user-supplied placeholder. No key value and no
  key-prefix string is reproduced in this report; line 108 is outside the proposed S072 anchor.
- Lines 103–107: instruct obtaining auto-login cookies into `./.auth`. No cookie or auth-state content was
  read, fetched or retained.

## Supplementary cross-check against the frozen inputs (not part of S072's README scope)

Read-only census only; no projection run, no file written to `config_files`, no upstream import.

- `plans/fixtures/r29/generate_test_data.py` SHA256
  `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` matches the manifest. Its six
  `raw.replace` calls are at lines 11–16 in order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA,
  MAP; `json.loads` is line 20; the `enumerate` output loop is lines 21–23.
- `plans/fixtures/r28/webarena/config_files/test.raw.json` SHA256
  `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` matches the manifest.
- Serialized-text occurrence counts in that raw file (occurrences, not tasks, not changed leaves, not
  output files): `__GITLAB__` 385, `__REDDIT__` 336, `__SHOPPING_ADMIN__` 300, `__SHOPPING__` 281,
  `__MAP__` 133, `__WIKIPEDIA__` 0; total six-token occurrences 1435. Runtime markers `__last_url__` 65
  and `__page__` 12 were counted separately and are not environment tokens. `__HOMEPAGE__` occurs 0 times.
- Scheme check: `grep -o -E 'https?://__[A-Z_]+__'` on the raw file returned 0 occurrences, so no six-token
  occurrence is immediately prefixed by an explicit scheme in this frozen text.
- Distinct `"task_id": <int>` keys in the raw file: 812. This is a key-count census, not evidence of task
  validity, and not a re-derivation of the projection.
- README export order and generator replacement order differ: README lists SHOPPING and SHOPPING_ADMIN
  first; the generator replaces GITLAB first. The projection contract should take order from the
  generator, never from README listing order.
- README's SHOPPING_ADMIN example includes `/admin`, while the frozen raw appends `/admin` itself in 2 of
  300 occurrences. Applying that example verbatim would duplicate the segment in those 2 contexts. Since
  `browser_env/env_config.py` was not fetched (assignment prohibition) and `prepare.sh` belongs to another
  seat, which base value this snapshot actually expects remains unresolved.
- `__WIKIPEDIA__` occurring 0 times means the generator's WIKIPEDIA replacement is vacuous on this frozen
  raw. It does not show that the README variable is unused elsewhere; that would require env_config,
  which this seat did not open.

## Source-versus-runtime boundary

Everything above is static source and fixture text. The README describes an intended operator workflow;
it does not establish actual deployment domains, actual config files, live task counts, scorer behavior,
model performance or task validity. The example ports and paths are illustrative placeholders. The three
`*.invalid` profiles are synthetic fixtures and are not deployment evidence. The bounded census says
nothing about which queries or cookies a running WebArena instance would use.

## Unknowns / limits

- `browser_env/env_config.py` contents (value forms, scheme handling, HOMEPAGE use) are unread and were
  not fetched; the README explicitly leaves the wildcard-import target open.
- `prepare.sh` invocation and `.github/workflows/tests.yml#L7` env-var usage were not opened by this seat.
- Whether README's `:7780/admin` example matches the pinned snapshot's intended SHOPPING_ADMIN base is
  unresolved (see the 2-of-300 suffix census).
- The 812 figure is a README statement; the projection's task/profile counts remain to be measured by the
  instrument, not by this report.
- Search log is bounded to the single assigned URL. No additional web search, no endpoint request beyond
  that raw file fetch, no claim of global absence or novelty.

## Artifacts

- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/build/R29SourceWorkflow.md`
- Scratch: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29SourceWorkflow-2/README.meta.json`
  and `excerpt-lines86-92.txt` (the full page was deleted after measurement).
- No SOURCES.md, registry, index, plan, draft, production code or fixture was edited. No commit or push.
  No build, selftest, linter or formatter was run. No package install or update occurred.

VERDICT: PASS
Scope: S072 source seat only — assigned README opened at the pinned commit on 2026-10-21, located 19-word
quote and snapshot hash recorded, proposed row supplied without writing it, fixture cross-checks kept as
separate units, and runtime/deployment claims left unasserted. Not a round or corpus admission.
