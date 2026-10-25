writer: KengakuR29-2.FReopenS072-2

# FReopenS072 — re-open source row S072 live and audit every cell

Item scope: re-open row S072 (the WebArena `README.md` at commit `dce04686`) at its recorded URL,
record access date / HTTP status / byte size / sha256, verify scope, anchor line numbers and teaches
against the live bytes, relocate the build seat's ≤25-word quote and count its words
programmatically, and name any cell that is wrong or unsupported.

## What was attacked

1. The row's snapshot hash and byte count, by fetching the pinned commit URL twice.
2. Every anchor line number, by printing the live file with 1-based numbers.
3. Every clause of `teaches`, including its negative clause (no replacement order / token inventory),
   by literal counting over the whole page.
4. The `scope` cell's two negative exclusions (`env_config` values, deployment URLs) by whole-page grep.
5. The `anchor` parenthetical "not a manifest pin", by reading `plans/fixtures/r29/manifest.json`.
6. The `status` / `used-by` cells, by grepping `corpus/knowledge/`, the round-29 draft and the
   calibration receipts for `S072`.
7. The build seat's quote claim (lines, byte size, hash, word count, occurrence count), by
   re-deriving from the live bytes and `cmp` against the retained excerpt file.

I did **not** read `plans/config_projection.py` at all (not needed for this item; no source of the
instrument was consulted).

## Observed facts

### Fetch (read-only, network)

```
$ curl -sS -o README.md -w 'http_status=%{http_code}\nbytes=%{size_download}\n' \
  'https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/README.md'
http_status=200
bytes=9717
sha256=081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287
```

Second fetch at 2026-10-21T16:48:26Z: `status=200 bytes=9717`, same sha256, `cmp` reports the two
fetches identical. File is LF-only (0 CRLF), no BOM, 9717 bytes, 163 split elements ending in a final
newline.

Access date: 2026-10-21 (UTC), matching the row's `opened` cell and its "(2026-10-21 bytes)" note.
The sha256 equals the row's anchor hash exactly; the URL string in the row is character-identical
(105 chars) to the URL in the build seat's metadata JSON.

### Live numbered lines covering every anchor range

```
 79|> To ensure the correct evaluation, please setup your own WebArena websites following step 1 and step 2. ...
 84|2. Configurate the urls for each website.
 85|```bash
 86|export SHOPPING="<your_shopping_site_domain>:7770"
 87|export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"
 88|export REDDIT="<your_reddit_domain>:9999"
 89|export GITLAB="<your_gitlab_domain>:8023"
 90|export MAP="<your_map_domain>:3000"
 91|export WIKIPEDIA="<your_wikipedia_domain>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"
 92|export HOMEPAGE="<your_homepage_domain>:4399" # this is a placeholder
 93|```
 95|> You are encouraged to update the environment variables in [github workflow](.github/workflows/tests.yml#L7) to ensure the correctness of unit tests
 97|3. Generate config file for each test example
 98|```bash
 99|python scripts/generate_test_data.py
100|```
101|You will see `*.json` files generated in [config_files](./config_files) folder. Each file contains the configuration for one test example.
```

### Cell-by-cell audit against live bytes

| cell | row value (abridged) | live check | result |
|---|---|---|---|
| id | `S072` | exactly one `\| S072 \|` row in `corpus/SOURCES.md` | holds |
| source | title + pinned URL | HTTP 200, 9717 bytes, hash identical to anchor | holds |
| kind | `docs` | README prose, not the generator script | holds |
| tier | `A` | `SOURCES.md` legend counts a maintainer statement as A; this row is scoped to what the maintainer README states | holds |
| scope | site-URL exports + separate per-example config step; not `env_config` values, deployment URLs or task validity | steps 2 and 3 are separate headings (l.84, l.97); `env_config` occurs 0 times in the page; the seven values are `<your_..._domain>` placeholders, no deployed site URL; no task-validity statement | holds |
| anchor | `lines79,84–92,95,97–101` + sha256 | every listed line number lands on the stated content (above); line 93 (closing fence) is the only adjacent line not listed; hash and byte size match two independent fetches | holds |
| anchor parenthetical | "snapshot hash, not a manifest pin" | `plans/fixtures/r29/manifest.json` `files` has 3 keys (`generate_test_data.py`, `r28/.../test.raw.json`, `profiles.json`); `README.md` is absent | holds |
| teaches (1) | seven exported variables | page has exactly 7 lines starting `export `, all inside 86–92 (whole-file count = 7) | holds |
| teaches (2) | scheme-less example origin:port form | no `http://`/`https://` in any of the seven values; each is `<...domain>:PORT` | holds |
| teaches (3) | SHOPPING_ADMIN adds `/admin` | l.87 value ends `:7780/admin` | holds |
| teaches (4) | WIKIPEDIA adds a long path | l.91 value ends `/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing` | holds |
| teaches (5) | HOMEPAGE marked placeholder | l.92 trailing comment `# this is a placeholder` | holds |
| teaches (6) | step 3 runs `scripts/generate_test_data.py` | l.99 is `python scripts/generate_test_data.py` | holds |
| teaches (7) | writes one config file per example | l.97 heading "3. Generate config file for each test example" (singular per example) and l.101 "Each file contains the configuration for one test example." | holds (paraphrase, see nuance N2) |
| teaches (8) | README states no replacement order or token inventory | case-insensitive whole-page counts: `order` = 0 lines, `token` = 0 lines; the only `replace*` hit is l.142 in the prompt-template section | holds (see nuance N3) |
| status | `queued` | `corpus/knowledge/` has no file matching `config`; no admitted entry cites S072 | holds |
| opened | `2026-10-21` | reproduced live 2026-10-21; build receipts dated the same day | holds |
| recheck | `on-release` | same value as sibling pinned-source rows S070, S071, S073; no falsifiable content claim | n/a (policy cell) |
| used-by | `—` | only unadmitted draft `.ufo/waves/round-29/drafts/webarena-config-projection.md:27` names S072 | holds |

### Build-seat quote: relocation and programmatic word count

Quote claimed at `R29SourceWorkflow.md` "Located quote": README lines 86–92, contiguous, 418 bytes,
sha256 `c4de5223...`, 19 words, one occurrence.

Re-derived from the live page:

- Lines 86–92 joined by LF, **with** the trailing newline: 418 bytes, sha256
  `c4de52237d3ae0b7eff85be10eab91890a633bd7c1cf8d5b11a423136720b697`.
- Same span **without** the trailing newline: 417 bytes, sha256 `2e4934fe...`.
- Word counts on the exact retained bytes: Python `str.split()` = 19; GNU `wc -w` = 19 (both on the
  7-line span and on the no-trailing-newline copy); `tr -s '[:space:]' '\n' | grep -c .` = 19.
- Occurrence count of the full 418-byte string in the 9717-byte page = 1.
- `sed -n '86,92p'` of the live page `cmp`-identical to the retained
  `.ufo/waves/round-29/scratch/KengakuR28.R29SourceWorkflow-2/excerpt-lines86-92.txt` (418 bytes,
  same sha256).
- Quote is 19 ≤ 25 words, so it satisfies the ≤25-word rule; it contains only placeholder
  `<your_..._domain>` values, no credential or real host.

No mismatch: the 418-byte figure includes the trailing newline, which is exactly what the retained
file holds.

## Mismatches found

**None.** No cell is wrong; no clause of `scope`, `anchor` or `teaches` is contradicted by the live
bytes. Line numbers 79, 84–92, 95 and 97–101 all land on the stated content, and the snapshot hash
reproduces byte-for-byte on two fetches.

## Nuances (checked, not mismatches)

- **N1 — 417 vs 418 bytes.** The build report's 418 bytes is correct only including the trailing
  newline; the bare 7-line text is 417 bytes. The retained excerpt file is 418 bytes and hashes to
  `c4de5223...`, so the report is consistent with its own artifact. Anyone re-deriving without the
  newline will get a different hash.
- **N2 — "writes one config file per example".** The README does not use that exact phrase; support
  is l.97 ("Generate config file for each test example", singular) plus l.101 ("Each file contains the
  configuration for one test example."). [INFERENCE] The row's "one ... per example" reads the 1:1
  mapping from those two sentences; it is a faithful paraphrase, not a literal quotation.
- **N3 — "no replacement order or token inventory".** True for the config-generation step, but l.142
  does mention prompt-template `keywords` being enumerated to check they were replaced. That sentence
  is about prompt templates, not the config generator's placeholders, so the negative clause is not
  contradicted; it is only true with the row's config-step scope in force.
- **N4 — "seven exported variables" read globally.** The page documents an eighth exported variable in
  prose at l.108 (`OPENAI_API_KEY`). The row's own qualifier "in scheme-less example origin:port form"
  and the anchor (84–92, excluding 108) keep the count correct; a global reading of "seven exported
  variables" would be incomplete.
- **N5 — anchor superset.** Lines 79 and 95 are in the anchor but are not drawn on by `teaches`; the
  anchor is broader than the taught claims. Not a contradiction.
- **N6 — closing fence.** Line 93 (```` ``` ````) is the only adjacent line not in `84–92`; the block is
  still unambiguously identified.

## Unresolved gaps

- GitHub raw at a commit hash is treated as immutable; the two-identical-fetch result is the only
  evidence of content stability available here (no independent mirror checked).
- The build report's side remark that `.github/workflows/tests.yml#L7` holds env vars was not opened;
  the row does not claim that workflow's contents, so it is outside this audit.
- No access to the build seat's process beyond its landed artifacts; the `opened` date is corroborated
  by live reproduction today, not by an independent timestamp.

VERDICT: PASS
