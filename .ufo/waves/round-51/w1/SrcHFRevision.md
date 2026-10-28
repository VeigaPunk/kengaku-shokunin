# Round 51 · SrcHFRevision — Hugging Face model-revision pin page: absent, row proposed as rejected

Seat: `SrcHFRevision` (scribe). Axes named: **adjacency** (assigned — one source row with a named
owner and a disposition); **freshness** observed (opened/recheck fields carry today's date and a
cadence) but not claimed. Lane `kengaku-shokunin`, read-only. Scope: open the primary documentation
for pinning a model revision on Hugging Face, capture an anchor plus a ≤25-word located quote that
grounds *"a model identity pin must name a revision, not a tag"*, and propose one `docs` row — or,
if the page cannot be fetched, record the failure and propose the row as a **rejection** with its
flip condition. No quote was invented.

## 0. Binding inputs read before any fetch

| path | what was read |
|---|---|
| `plans/round-51-claims.md` | full file — C1 freshness 8→9 (surface truth), C2 adjacency 8→9 (owner + disposition per routed finding), predicates, controls, kill rules, limits |
| `plans/round51_surfaces.json` | entry list read for the model-related surfaces (`SF03` served model `:34113`, `SF14` registry `count_claim`), so the row's scope does not restate a surface |
| `corpus/SOURCES.md` | contract-v1 header (tiers A/B/C, kinds, 11 columns, statuses `queued\|mined\|rejected`) and the full registry |
| `corpus/QUALITY.md` | admission bar Q1–Q7 (Q3 the ≤25-word located quote; Q5 label a source for what it is) |
| `corpus/lessons/round-50-verifier-spotcheck.md` §6 | the routed defects this round answers — D5 (source locations) is the class this seat sits in |
| `.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md`, `SrcLlamaServer.md`, `SrcCensus.md` | sibling evidence on the *same* pin subject and on id allocation (`S178–S251` unallocated) |

Lane revision at read time (read-only `git rev-parse`): `4090c3db79d11279ab5e5121ba25e74aa316e6e7`
(`round-51: v2 wave spec (64 seats) + validated dispatch payload`); the tracked tree was clean
(`git status --porcelain` showed only untracked `.ufo/waves/**` artifacts), so the bytes read equal
that commit. Stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c` is an ancestor
(`git merge-base --is-ancestor … HEAD` → exit 0).

## 1. Commands run (verbatim; `<S>` = `/fast/scratch/hyaku/kengaku-r51/SrcHFRevision`)

```sh
export TMPDIR=/fast/scratch/hyaku/kengaku-r51/SrcHFRevision; cd "$TMPDIR"
date -u +"UTC %Y-%m-%dT%H:%M:%SZ"
curl -sS -o canonical-404.html -D canonical-headers.txt -w "code=%{http_code} url=%{url_effective} bytes=%{size_download}\n" \
  https://huggingface.co/docs/hub/model-revisions
head -5 canonical-headers.txt
grep -o "<title>[^<]*</title>" canonical-404.html
sha256sum canonical-404.html
for u in https://huggingface.co/docs/hub/model-revisions.md \
         https://huggingface.co/docs/hub/en/model-revisions \
         https://huggingface.co/docs/huggingface_hub/guides/model_revisions \
         https://huggingface.co/docs/huggingface_hub/en/guides/model_revisions \
         https://huggingface.co/docs/huggingface_hub/main/en/guides/model_revisions \
         https://huggingface.co/docs/huggingface_hub/v2.3.0/en/guides/model_revisions \
         https://huggingface.co/docs/hub/local-cache \
         https://huggingface.co/docs/hub/local-cache.md \
         https://huggingface.co/docs/hub/transformers.md \
         https://huggingface.co/docs/huggingface_hub/guides/download.md \
         https://huggingface.co/docs/hub/llms.txt ; do
  curl -sS -o /dev/null -w "%{http_code} %{size_download} <- $u\n" -L "$u"; done
curl -sSL "https://api.github.com/repos/huggingface/hub-docs/contents/docs/hub?ref=main" -o hubdocs-list.json
curl -sSL "https://codeload.github.com/huggingface/hub-docs/tar.gz/refs/heads/main" -o hub-docs.tgz
tar xzf hub-docs.tgz -C hubdocs --strip-components=1
grep -rl "model-revisions" hubdocs ; echo "matches_exit=$?"
grep -rn -i "revision" hubdocs/docs/hub/_toctree.yml
curl -sSL "https://huggingface.co/docs/hub/llms.txt" -o llms.txt
grep -ci revis llms.txt ; grep -c "^- \[" llms.txt
curl -sSL "https://api.github.com/repos/huggingface/huggingface_hub/contents/docs/source/en/guides?ref=main" -o guides.json
curl -sSL "https://api.github.com/repos/huggingface/hub-docs/commits?path=docs/hub/model-revisions.md&per_page=5" -o hist.json
curl -sS "https://web.archive.org/cdx/search/cdx?url=huggingface.co/docs/hub/index&output=json&limit=-2&fl=timestamp,statuscode"
curl -sS "https://web.archive.org/cdx/search/cdx?url=huggingface.co/docs/hub/model-revisions&matchType=prefix&output=json&limit=-3&fl=timestamp,original"
curl -sSL "https://huggingface.co/docs/hub/local-cache.md" -o local-cache.md && sha256sum local-cache.md
curl -sSL "https://huggingface.co/docs/hub/transformers.md" -o transformers.md
curl -sSL "https://huggingface.co/docs/huggingface_hub/guides/download.md" -o download.md
python3 -c '<str.split() word counts over the three candidate quotes>'
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD; echo $?
sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
grep -c "huggingface.co\|hf.co" /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
grep -n "EXIT_MALFORMED\|EXIT_COLLISION" /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py
```

## 2. Observed outputs (verbatim where they are evidence)

### 2.1 The named page does not resolve

```
UTC 2026-10-28T18:29:49Z
code=404 url=https://huggingface.co/docs/hub/model-revisions bytes=52007
HTTP/2 404
content-type: text/html; charset=utf-8
content-length: 52007
date: Wed, 28 Oct 2026 18:29:49 GMT
etag: W/"cb27-kxyDUHDZ85YiA5BBqFNlr+VPrU8"
<title>404 – Hugging Face</title>
10000fede5f5952993db38e83d0c4b71af517a12b0f5f216f9cc1006064dba0b  canonical-404.html
```

URL matrix, same sitting:

```
404 52384 <- https://huggingface.co/docs/hub/model-revisions.md
404 52390 <- https://huggingface.co/docs/hub/en/model-revisions
200 234   <- https://huggingface.co/docs/huggingface_hub/guides/model_revisions
200 234   <- https://huggingface.co/docs/huggingface_hub/en/guides/model_revisions
404 52061 <- https://huggingface.co/docs/huggingface_hub/main/en/guides/model_revisions
200 234   <- https://huggingface.co/docs/huggingface_hub/v2.3.0/en/guides/model_revisions
200 247366 <- https://huggingface.co/docs/hub/local-cache
200 14896  <- https://huggingface.co/docs/hub/local-cache.md
200 7176   <- https://huggingface.co/docs/hub/transformers.md
200 15252  <- https://huggingface.co/docs/huggingface_hub/guides/download.md
200 22494  <- https://huggingface.co/docs/hub/llms.txt
```

The 234-byte responses are not the page — they are the version-switcher stub (verbatim, `v0.30.0`
copy; every tested version returned the same shape and the "main" URL it points at 404s):

```
The documentation page GUIDES/MODEL_REVISIONS doesn't exist in v0.30.0, but exists on the main version. Click <a href="/docs/huggingface_hub/main/en/guides/model_revisions">here</a> to redirect to the main version of the documentation.
```

### 2.2 The page is absent from the documentation sources, not merely unrendered

```
$ python3 - <<'PY'   # over hubdocs-list.json (GitHub contents API, docs/hub @ main)
entries 274
matches for revis/commit/tag: []
$ grep -rl "model-revisions" hubdocs ; echo "matches_exit=$?"
matches_exit=1
$ grep -rn -i "revision" hubdocs/docs/hub/_toctree.yml     # no output
$ grep -ci revis llms.txt ; grep -c "^- \[" llms.txt
0
277
$ python3 - <<'PY'   # huggingface/huggingface_hub docs/source/en/guides @ main
['buckets.md','cli-extensions.md','cli.md','collections.md','community.md','download.md',
 'hf_file_system.md','inference.md','inference_endpoints.md','integrations.md','jobs.md',
 'manage-cache.md','manage-spaces.md','model-cards.md','overview.md','repository.md',
 'sandbox.md','search.md','upload.md','webhooks.md']
$ curl -sSL "https://api.github.com/repos/huggingface/hub-docs/commits?path=docs/hub/model-revisions.md&per_page=5"
entries 0
```

Read together: no `model-revisions` page exists in the Hub docs tree (274 entries), no guide of that
name exists in the `huggingface_hub` docs tree, the docs index `llms.txt` lists 277 pages and none
mentions "revis", and the Hub docs repository has no commit for that path. The page is not a
transient 500 or a version-skew artifact; it is not published.

### 2.3 Archive check (weak, recorded as a limit)

```
control  https://web.archive.org/cdx/search/cdx?url=huggingface.co/docs/hub/index&output=json
[["timestamp","statuscode"],["20261020152231","200"],["20261025121848","200"]]

target   https://web.archive.org/cdx/search/cdx?url=huggingface.co/docs/hub/model-revisions&matchType=prefix&output=json
[]

target   https://web.archive.org/cdx/search/cdx?url=huggingface.co/docs/huggingface_hub/guides/model_revisions&matchType=prefix&output=json
<p>Internet Archive services are temporarily offline.</p>   (HTTP 503)
```

The control proves the CDX endpoint answered; the empty result for the target is suggestive but an
empty CDX result is **not** proof of absence, and one prefix query returned 503. Treated as
corroboration only.

## 3. Findings

1. **The named page cannot be fetched, so no anchor and no quote were captured — and none were
   invented.** The canonical URL, its `.md` twin, the `/en/` variant, and every `huggingface_hub`
   guide version return 404 or the version stub; the docs sources carry no such page. This is the
   item's declared failure branch, taken verbatim.
2. **The prescription is not vendor text.** The live Hub docs state the *opposite permission* — a
   tag, a branch and a commit hash are all valid as a `revision`. Quoting either page as support for
   *"must name a revision, not a tag"* would misattribute a lane prescription to the vendor
   (QUALITY Q5/Q3: claim stays inside its quote). Verbatim, `hub/transformers.md:89` (20 words):

   > You can also load a model from a specific version (based on commit hash, tag name, or branch) as follows:

   and `huggingface_hub` `guides/download.md:39-42`:

   > By default, the latest version from the `main` branch is downloaded. However, in some cases you want to download a file at a particular version (e.g. from a specific branch, a PR, a tag or a commit hash).

3. **What *is* groundable is the mechanism, and it lives on a different page.** `hub/local-cache.md`
   (fetched 2026-10-28, 14896 bytes, sha256 `2f13a05e732b28ed1116ea6f634681a811a6a497ba3733bd57784160b82f3d2e`)
   states the ref→commit relation the lane prescription rests on. Two located quotes, word counts by
   `str.split()`:

   - `local-cache.md:132` (14 words):

     > The `refs/` directory maps human-readable references (branch names, tags, PR numbers) to commit hashes.

   - `local-cache.md:145` (24 words):

     > When a file is downloaded using a branch or tag name, the corresponding ref file is created or updated with the latest commit hash.

   - `local-cache.md:149` (context only, not proposed as a quote): `snapshots/` holds one subdirectory per cached revision (commit hash).

   Together these ground *"a tag is a mutable name that resolves to a commit; the pinned identity is
   the commit hash"*. They do **not** state *"a pin must name a revision, not a tag"* — that sentence
   is the lane's own inference over the mechanism and must be written as lane policy, not as a quote.
   This is offered to the L1 as a **candidate for a new row**, not as this row's quote.
4. **Id collision — do not use `S178`.** `S178` is claimed by the llama.cpp server-docs row
   (`.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md` line 1 derives it;
   `SrcLlamaServer.md` §4 leaves the id as `S0??`), and the integration owner has since staged that
   row in the working tree (see §8). The committed registry at `4090c3d` holds 170 rows, highest
   `S177`, gaps `S087–S089, S095, S096, S098, S099`. This seat therefore leaves `S0??` and states the
   derivation: next free after the llama.cpp row, i.e. `S179` if the L1 assigns sequentially.
5. **No existing Hugging Face row to supersede.** `grep -c "huggingface.co\|hf.co" corpus/SOURCES.md`
   → `0`. The registry has never cited HF; nothing here is an in-place correction (QUALITY §Round42:
   corrections are appended rows).
6. **Adoption mechanics for a rejection row (read from the gate, not run).**
   `plans/sources_adopt.py:52` `EXIT_MALFORMED = 4`; `:289-303` `quoted_spans()` returns
   `no-quote` for an anchor cell with no `"…"` span, and `quote_check` records
   `REFUSED <id> no-quote`. So a rejection row carrying no quote must be adopted **without**
   `--quote-file`/`--artifact`; supplying them would refuse it by design. An id collision exits `3`
   (`EXIT_COLLISION`, `:51-53`, `:231-234`) — the reason finding 4 matters.

## 4. Proposed SOURCES row (one row, contract-v1 shape, 11 columns)

Placeholder id `S0??` (see finding 4). No `|` and no `"` inside cells, so the gate's parser and
quote mode see a well-formed row with no quote span.

| S0?? | Hugging Face Hub docs — the model-revisions page named for the model-identity pin claim, canonical https://huggingface.co/docs/hub/model-revisions | docs | B | refused correction record: the named page does not resolve on 2026-10-28 at any tested URL, so no anchored quote exists to admit; not an admitted citation and not support for any claim | no anchor — the page is absent, not unread: HTTP 404 at the canonical URL and at its `.md` twin (body 52007 bytes, sha256 `10000fed…`), 0 of 274 entries in `huggingface/hub-docs` `docs/hub` carry `model-revisions`, and the Hub docs index `llms.txt` (277 pages) has 0 lines matching `revis` | REJECTED: the page cannot be fetched, so nothing grounds the pin sentence; the live Hub docs instead permit a tag as a `revision` (`hub/transformers.md:89`), so the prescription is lane policy over the ref-to-commit mechanism, not vendor text; flip: a page at a resolving canonical URL that states the ref-to-commit distinction must be opened as a NEW row id with its own located quote — candidate `https://huggingface.co/docs/hub/local-cache` section `refs/`, fetched 2026-10-28, sha256 `2f13a05e…` | rejected | 2026-10-28 | 90d | — |

Tier is `B` nominally, following the refusal-record precedent of S094 (`docs`, `B`, status
`rejected`): the row is a refusal record, not a source, so the tier is not load-bearing. `recheck 90d`
is the shortest cadence already in use in the registry (values present: `180d` ×109, `on-release` ×22,
`90d` ×12, plus fixed dates) and matches a page that may be re-published.

## 5. Routed-finding shape (for the L1's ledger, if it opens one)

| field | value |
|---|---|
| class | `source-row-refused` |
| source | `corpus/SOURCES.md` (proposed row above); evidence this report §2 |
| opened_round | 51 |
| owner | `kengaku` (the sources registry is this lane's; no non-`kengaku` owner applies) |
| disposition | `refused-out-of-scope` — the page does not exist, so the claim is out of the vendor's text; the lane keeps the prescription as policy |
| check | `curl -sS -o /dev/null -w '%{http_code}\n' https://huggingface.co/docs/hub/model-revisions` (404 today; a 200 flips the rejection) |
| close | this report plus the landed row |
| blocker | none |
| note | the mechanism page `hub/local-cache` §`refs/` is the groundable alternative (finding 3); it needs its own row id and its own quote |

This finding is in-lane: it names no second lane and routes nothing out. If the L1 judges otherwise,
the vocabulary that would apply is `refused-out-of-scope` with owner `kengaku`; a `routed` row would
require a non-`kengaku` owner and a `next` field, and no such owner exists for a dead URL.

## 6. Limits

- **No quote exists for the named page**, so the item's primary deliverable is a documented absence,
  not an anchor. The two mechanism quotes in finding 3 belong to a *different* URL and are labelled
  as such; they are not this row's quote.
- **The 404 is point-in-time.** The body digest `10000fed…` and etag `W/"cb27-…"` describe the
  2026-10-28 18:29:49Z response; a re-published page would differ and would flip the rejection.
- **Archive evidence is weak** (§2.3): empty CDX plus one 503 is corroboration, not proof.
- **`hf.co` and the Hub API were not probed for a revision endpoint**; the item named a documentation
  page, and this seat did not widen into the API surface.
- **`plans/sources_adopt.py` was read, not run** — the gate behaviours in finding 6 are code readings
  with line numbers, not observed exits.
- **The prescription sentence has no current citing entry**: no `corpus/knowledge/*`, `SKILL.md` or
  `PROVINCE.md` line states *"a model identity pin must name a revision, not a tag"* today (grep over
  `corpus/knowledge`, `corpus/lessons`, `PROVINCE.md`, `SKILL.md` returned only unrelated `commit
  hash` hits), so `used-by` is `—` and the row cannot be landed as support for an existing entry.
- **Word counts** are `str.split()` counts over the quoted text as fetched, the same counter the
  sibling seats used.
- **Scratch**: `/fast/scratch/hyaku/kengaku-r51/SrcHFRevision` held only fetch bytes
  (`canonical-404.html`, `hub-docs.tgz` 13 MB, `hubdocs/`, the `.md` captures); it was removed
  before this report was finalised, so nothing citable lives there — every quote above is inline,
  with its URL, line number and the digest of the bytes it was read from.

## 7. Files touched / tooling

- Written: `.ufo/waves/round-51/w1/SrcHFRevision.md` (this report) only. No fragment file was named
  by the item, so none was written; no evidence directory was created (the seat's write scope names
  the report path only).
- Not written: any `plans/*`, `corpus/*`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`,
  `MANIFEST.json`, `.ufo/state`, `.scratch/`. No commit, push, or mutating git/jj command (only
  `rev-parse`, `merge-base --is-ancestor`, `status`, `show`). No fixture git repository was created.
- Tooling: no installs, no package manager (pacman untouched per the host guard). `curl`, `tar`,
  `sha256sum`, `grep`, `python3` stdlib only.

## 8. Observed concurrent landing (not mine, recorded for the reader)

Between my last registry read and the final check, the working tree gained the integration owner's
uncommitted round-51 landing — no seat wrote these:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain | grep -v '^?? .ufo/waves/'
 M corpus/SOURCES.md
 M plans/round-51-claims.md
 M plans/round51_routing.py
?? corpus/evidence/round51/
?? corpus/knowledge/served-endpoint-identity-pin.md
$ git diff --stat
 corpus/SOURCES.md        |  1 +
 plans/round-51-claims.md | 27 +++++++++++++++++++++++++++
 plans/round51_routing.py | 18 +++++++++++++-----
 3 files changed, 41 insertions(+), 5 deletions(-)
$ grep -c '^| S[0-9]\+ ' corpus/SOURCES.md   → 171   (tail: S176 S177 S178)
```

The single `SOURCES.md` added line is `| S178 | llama.cpp server API reference …` — the row finding 4
predicted would take `S178`. The `round-51-claims.md` addition is instrument amendment A1 (C2 counter
cwd, timeout, owner universe, `--ledger` path); it does not touch C1 or this row. My own measurements
remain those at `4090c3d` (`corpus/SOURCES.md` sha256 `8a1ba155…` at that commit); the worktree's
`SOURCES.md` now differs by that one landed row, which is why the id is left as `S0??`.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
REV-FREEZE e07f131cf7037e58a21db6e1f3986cf401ad257c

VERDICT: The named Hugging Face model-revisions page cannot be fetched — HTTP 404 at
`https://huggingface.co/docs/hub/model-revisions` (body 52007 bytes, sha256 `10000fed…`, 2026-10-28
18:29:49Z), 404 at its `.md` and `/en/` twins, a 234-byte version stub at every `huggingface_hub`
guide version whose "main" target 404s, zero `model-revisions` entries among 274 `docs/hub` files in
`huggingface/hub-docs` main, and zero "revis" lines in the 277-page docs index — so no anchor and no
quote were captured and none were invented; the live Hub docs in fact permit a tag as a `revision`
(`hub/transformers.md:89`), so the pin sentence is lane policy over the ref→commit mechanism
(`hub/local-cache.md:132`, `:145`) and not vendor text. One `docs`/tier-B row is proposed **as a
rejection** with a precise flip condition and the mechanism page named as its candidate successor;
the id is left `S0??` because `S178` is already claimed by the llama.cpp row. Axes: adjacency
(disposition + owner named), freshness (opened 2026-10-28, recheck 90d). No lane file was edited, no
gate was run as a gate, and the seat scratch tree was removed before yield.
