# R33FHuggingFace — HF raw response, record count, and schema delta

**Seat:** `KengakuR33.R33FHuggingFace` (leaf; no subagent dispatch, no tools installed)
**Date:** 2026-10-25 · **Target:** frozen claim C3 (`plans/round-33-claims.md` §C3), HF half —
committed `corpus/evidence/round33/catalogs/hf.raw.json`, `SHA256SUMS`, `after.txt`, and the
`hf_models` / `hf_schema_delta` derivation in `plans/catalog_probe.py`.
**Verdict:** **caught (derivation semantics), artifact itself uncaught.** The committed HF bytes,
count, digest and the four-field delta are all correct and the capture is corroborated as a
*genuine, distinct, same-day live fetch*. The **derivation** is not response-level: the delta is
computed from record #1 only, the count is a page length with no witness of pagination, and the
HF digest binding is bypassable by omitting its line from `SHA256SUMS`.

All mutations confined to `/tmp/r33fhf-harness/`; the lane was read-only throughout
(`git status --porcelain corpus/evidence/round33/catalogs/ plans/catalog_probe.py` → empty).

---

## 1. Independent parse of committed `hf.raw.json` (not using probe functions)

```
$ python3 /tmp/r33fhf-harness/run.py        # section A
== A. independent derivation from committed bytes ==
hf.raw.json bytes : 27698
sha256 recomputed : 96aba4d1d53c9cc8b06a2238c0a7eb224709ae66417b6a602ca6a34416323121
SHA256SUMS line   : 96aba4d1d53c9cc8b06a2238c0a7eb224709ae66417b6a602ca6a34416323121  hf.raw.json
after.txt sha line: raw_sha256 hf=96aba4d1d53c9cc8b06a2238c0a7eb224709ae66417b6a602ca6a34416323121 or=9755544573fb4fa343afb216f9133371b0b226e94e87dd97d8696a3b68fc6bc5 cap=65536
records           : 50 | unique ids: 50
first-object miss : ['author', 'sha', 'lastModified', 'gated']
union miss        : ['author', 'sha', 'lastModified', 'gated']
any-record miss   : ['author', 'sha', 'lastModified', 'pipeline_tag', 'library_name', 'gated']
presence /50      : {'id': 50, 'author': 0, 'sha': 0, 'lastModified': 0, 'downloads': 50, 'likes': 50, 'trendingScore': 50, 'pipeline_tag': 45, 'library_name': 44, 'tags': 50, 'gated': 0}
after.txt tokens  : {'hf_models=50': True, 'hf_schema_delta=4': True, 'hf=ok': True}
after.txt HF line : HF missing fields: author, sha, lastModified, gated
```

| check | observed | verdict |
|---|---|---|
| size | 27,698 B ≤ 65,536 cap | pass |
| sha256 (recomputed) | `96aba4d1…3121` | matches `SHA256SUMS` **and** `after.txt`'s `raw_sha256 hf=` line **and** the entry block's stated digest |
| shape | top-level JSON **array**, 50 objects, minified, no trailing newline, no header/URL/ETag material inside | as expected for the body only |
| count | 50 records, 50 **unique** `id`s | equals `hf_models=50` |
| first object keys (API order) | `_id, id, likes, trendingScore, private, downloads, tags, pipeline_tag, library_name, createdAt, modelId` | identical to the live endpoint's key order (§4) |
| delta, first-object reading | `author, sha, lastModified, gated` → **4** | equals `hf_schema_delta=4` |
| delta, union reading (absent from *every* record) | same four → **4** | equals receipt |
| delta, any-record reading (absent from *at least one*) | same four **+ `pipeline_tag` (5/50 absent) + `library_name` (6/50 absent)** → **6** | **≠ receipt** — see §3 |

`sha256sum -c` on the committed tree:

```
$ cd corpus/evidence/round33/catalogs && sha256sum -c SHA256SUMS
hf.raw.json: OK
or.raw.json: OK
rc=0
$ python3 plans/catalog_probe.py --verify --lane .
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated
rc=0
```

## 2. Receipt ↔ bytes comparison (`after.txt`, 324 B, 3 lines)

Every HF number in `after.txt` re-derives from the committed bytes: `hf_models=50` (= `len(list)`),
`hf_schema_delta=4` (= `len([f for f in HF_FIELDS if f not in data[0]])`), and the
`HF missing fields:` list is exactly the first object's missing set in `HF_FIELDS` order.

What does **not** re-derive, and is therefore not evidence of freshness from the artifact alone:
`probed=2026-10-25` (`ACCESS_DATE` constant, `catalog_probe.py:28`), `hf=ok` (set only inside a
successful `capture()`), `cap=65536` (constant `:53`), `entry=pending` (hard-coded string that
survives the landed entry, which now says `entry` is complete — a stale literal, not a freshness
signal). `after.txt` also carries no HF byte count; only the entry block carries `27,698 B`.

## 3. Do the four missing fields derive from the first model object? **Yes — exclusively.**

```python
# plans/catalog_probe.py:63-70
def parse_hf(text: str) -> tuple[int, list[str]]:
    data = json.loads(text)
    ...
    first = data[0]
    ...
    return len(data), [field for field in HF_FIELDS if field not in first]
```

`data[0]` is the only object consulted; records 2…50 are never inspected. On the **committed**
bytes this happens to be harmless: all four gap fields are absent from all 50 records, so
first-object = union = 4. It is not harmless as a rule, and it is not harmless for the fields
that *do* vary (`pipeline_tag` present in 45/50, `library_name` in 44/50).

Proof that the delta is first-object-controlled (sandbox, digests/receipt/entry all recomputed so
the only variable is record #1):

```
--- b2 record #1 gains `gated` (49/50 still lack it) -> delta 3 accepted
    exit=0
    raw=ok hf_models=50 or_models=467 hf_schema_delta=3 or_schema_delta=0 verify=ok
    HF missing fields: author, sha, lastModified
--- b3 same bytes, receipt keeps delta 4
    exit=1
    raw=ok receipt-mismatch missing:hf_schema_delta=3
```

So a real HF page in which 49 of 50 records omit `gated` is reported as `hf_schema_delta=3` if
the first record happens to carry it, and `--verify` exits 0. The counter cross-checks the receipt
against the *same* first-object computation (b3 is red only because it disagrees with itself), so
the cross-check cannot detect the aggregation error.

## 4. Freshness — the committed HF bytes are a genuine, distinct, same-day capture

Refetch of the same URL today (read-only), compared record-for-record:

```
$ python3 /tmp/r33fhf-harness/live.py
committed bytes 27698 sha256 96aba4d1d53c9cc8b06a2238c0a7eb224709ae66417b6a602ca6a34416323121
live      bytes 27698 sha256 9d4d9e6f402cc8e40ee8d8e90191ad015f66a8cbebe3b2731326211b0612d4ae
live response Date header: Sun, 25 Oct 2026 17:53:27 GMT
live Link header (cursor present): True
committed records 50 live records 50
id sets equal: True
records identical ignoring likes/trendingScore/downloads: True
committed presence/50: {'id': 50, 'author': 0, 'sha': 0, 'lastModified': 0, 'downloads': 50, 'likes': 50, 'trendingScore': 50, 'pipeline_tag': 45, 'library_name': 44, 'tags': 50, 'gated': 0}
live      presence/50: {'id': 50, 'author': 0, 'sha': 0, 'lastModified': 0, 'downloads': 50, 'likes': 50, 'trendingScore': 50, 'pipeline_tag': 45, 'library_name': 44, 'tags': 50, 'gated': 0}
committed first-object miss: ['author', 'sha', 'lastModified', 'gated']
live      first-object miss: ['author', 'sha', 'lastModified', 'gated']
```

- **Byte length identical (27,698), sha different** — exactly the signature of the same page
  captured minutes earlier with mutating counters. The full record multiset ignoring
  `likes/trendingScore/downloads` is **identical** (same `_id`s, `id`s, `tags`, `createdAt`,
  `pipeline_tag`, `library_name`, `modelId`), and the only positional differences are swaps of
  neighbours with equal `trendingScore` (indices 28↔29 at 167/167, 31↔32 at 144/144, 45/46) —
  i.e. tie-order flips, not content changes. Field-presence profiles match exactly (0/0/0/0 for the
  four; 45/44 for `pipeline_tag`/`library_name`).
- **Not a re-commit of round 32's capture.** `.ufo/waves/round-32/build/R32CatProbe.md` records
  the round-32 HF capture as `7e05ad8f…` / **27,771 B**; the round-33 bytes are `96aba4d1…` /
  **27,698 B**. Different digest and different length → the round-33 file is a new fetch, not the
  previous round's bytes re-staged.
- **The entry's `?full=true` claim is true today.** `GET /api/models?limit=1&full=true` → 4,415 B,
  keys include `author, sha, lastModified, gated` (plus `siblings`), 0 missing of the 11 expected.
- Two live fetches 35 s apart (17:52:52 and 17:53:27 GMT) returned **different** shas
  (`6f5471…` then `9d4d9e…`) with the same length — confirming the endpoint is counter-mutable, so
  *no* byte-identity check is possible for HF (unlike the OpenRouter artifact) and multiset
  equality is the correct freshness test.

**Conclusion: freshness holds for the HF artifact.** Fabrication is excluded not by the counter
(§5) but by this independent live refetch.

## 5. Count semantics — `hf_models=50` is a page length, and the bytes cannot show it

```
$ curl -sSI -A kengaku-catalog-probe/1.0 "https://huggingface.co/api/models?limit=50"
HTTP/2 200
content-type: application/json; charset=utf-8
content-length: 27698
date: Sun, 25 Oct 2026 17:54:13 GMT
etag: W/"6c32-h7pjyBYnFzieNqOilcmwU6Ww3ik"
…
$ curl -sSI -A kengaku-catalog-probe/1.0 "https://huggingface.co/api/models?limit=50" | grep -i '^link:'
link: <https://huggingface.co/api/models?limit=50&cursor=eyIkb3IiOlt7InRyZW5kaW5nU2NvcmUiOjExMSwiX2lkIjp7IiRndCI6IjZhZDNkYzM2NWM0YmYzN2VlZTFjZGQwZCJ9fSx7InRyZW5kaW5nU2NvcmUiOnsiJGx0IjoxMTF9fSx7InRyZW5…

$ curl -sS -A kengaku-catalog-probe/1.0 -o /tmp/r33fhf-harness/hf.limit100.json \
    -D /tmp/r33fhf-harness/hf.limit100.hdr "https://huggingface.co/api/models?limit=100"
56487 /tmp/r33fhf-harness/hf.limit100.json
records 100
1                                   # rel="next" present in the limit=100 response headers
$ curl -sS -A kengaku-catalog-probe/1.0 -o /tmp/r33fhf-harness/hf.limit1.json \
    "https://huggingface.co/api/models?limit=1"
472 /tmp/r33fhf-harness/hf.limit1.json
records 1
```

The `content-length: 27698` on the `?limit=50` HEAD is the same length as the committed body —
a third independent confirmation that the committed file is that endpoint's body, and that the
headers (which carry `link: … rel="next"`) were discarded at capture time.

- HF's `api/models` is **cursor-paginated** and returns a **bare array with no total count**
  (there is no `total_count` analogue to OpenRouter's 467). `hf_models=50` therefore means
  "50 records in the requested page", and is **indistinguishable from a catalog of exactly 50**
  from the committed bytes, because the only witness of pagination (`Link: … rel="next"`) is a
  **response header that is not committed**. The committed body is the response *body* only.
- No record-level validation backs the number: `parse_hf` checks only that the payload is a
  non-empty list whose **first** element is a dict.

```
--- b4 records 2..50 are non-model junk dicts
    exit=0   raw=ok hf_models=50 … hf_schema_delta=4 … verify=ok
--- b5 50 copies of one record
    exit=0   raw=ok hf_models=50 … hf_schema_delta=4 … verify=ok
```

`hf_models=50` and `hf_schema_delta=4` are both reproducible from a payload that is not a catalog
page at all.

## 6. HF digest binding is optional, not structural

`_load_raw` (`catalog_probe.py:123-144`) iterates the **lines of `SHA256SUMS`** and hashes whatever
each line names. A line that does not exist simply means the file is never hashed:

```
--- b6 fabricated bytes + SHA256SUMS without an hf.raw.json line
    exit=0
    raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
    HF missing fields: author, sha, lastModified, gated
```

Case b6 replaces `hf.raw.json` with 50 synthetic objects (`{"id": "fake/N"}`, first one padded to
exactly the four-field gap) and drops the HF line from the digest manifest; `--verify` exits 0.
The frozen predicate's "digests verifying against the committed `SHA256SUMS`" and the kill rule's
"no fabricated bytes may ever satisfy `--verify`" are therefore both **false as mechanisms** — the
committed `SHA256SUMS` *does* name `hf.raw.json`, so the landed tree is bound, but nothing in the
counter requires that line to exist. This overlaps the build report's rows f/f2
(`.ufo/waves/round-33/build/R33C3Design.md` §1); b6 is the HF-specific instance and adds the
point that the fabricated bytes can carry the exact live delta.

## 7. Mutation matrix (all cases: digests, receipt and entry recomputed; lane untouched)

| case | mutation in `/tmp/r33fhf-harness/sandbox/<case>` | exit | printed |
|---|---|---|---|
| b1 | byte-exact copy of the committed capture | 0 | `hf_models=50 … hf_schema_delta=4 … verify=ok` |
| b2 | record #1 gains `gated`; 49/50 still lack it | **0** | `hf_schema_delta=3` |
| b3 | same bytes, receipt keeps `hf_schema_delta=4` | 1 | `receipt-mismatch missing:hf_schema_delta=3` |
| b4 | records 2…50 are `{"junk": i}` | **0** | `hf_models=50 … hf_schema_delta=4 … verify=ok` |
| b5 | 50 copies of record #1 | **0** | `hf_models=50 … hf_schema_delta=4 … verify=ok` |
| b6 | fabricated 50-record array, HF line removed from `SHA256SUMS` | **0** | `hf_models=50 … hf_schema_delta=4 … verify=ok` |

## 8. Verdict per named sub-item

| sub-item | verdict | basis |
|---|---|---|
| committed HF raw response is genuine + fresh | **uncaught** | live refetch: identical record multiset modulo mutable counters, identical presence profile; distinct from round-32's digest/size |
| SHA256 recomputation | **uncaught** | `96aba4d1…` matches manifest, receipt line and entry line |
| record count | **caught (semantics)** / artifact correct | 50 unique records, but the number is the `?limit=50` page length; `rel="next"` proves the catalog is larger and the header is not committed |
| four missing fields derive from the first model object | **caught** | `parse_hf` uses `data[0]` only; b2 shows a 49/50-absent field reported as present-by-projection; per-record reading of the committed bytes gives 6, not 4 |
| digest binding of the HF bytes | **caught (mechanism)** | b6: omit the HF line from `SHA256SUMS` and fabricated bytes verify green |
| receipt date / `hf=ok` | **limitation** | constants, not observed values; only the live refetch corroborates the date |

## 9. Retained evidence

- `/tmp/r33fhf-harness/run.py` — offline harness, sections A+B (transcript: `/tmp/r33fhf-harness/transcript.txt`).
- `/tmp/r33fhf-harness/live.py` — live refetch comparison (transcript: `/tmp/r33fhf-harness/live.txt`).
- Sandboxes: `/tmp/r33fhf-harness/sandbox/{b1-baseline,b2-gated-first,b3-gated-first-receipt4,b4-junk,b5-dups,b6-unlisted-digest}`.
- Lane reads only: `corpus/evidence/round33/catalogs/{hf.raw.json,SHA256SUMS,after.txt}`,
  `corpus/knowledge/open-model-catalogs.md:66-79`, `plans/catalog_probe.py:28,53,63-70,123-144,147-203`,
  `.ufo/waves/round-32/build/R32CatProbe.md:11-21`, `.ufo/waves/round-33/build/R33C3Design.md:13-23`.

## 10. Risks / blockers / tooling

- None blocking; network reachable (read-only GETs to `huggingface.co`), so freshness could be
  tested directly instead of inferred.
- No tools installed or upgraded (none needed; stdlib `urllib`/`hashlib` sufficed).
- No lane, fleet, git or sibling-repo mutation; no `git` command was run inside `/tmp` sandboxes
  (none was needed) and no lane path was written except this report.
- Residual risk: if the operator's grading expects `hf_schema_delta` to be a **response-level**
  statistic, the landed `4` is wrong (a per-record reading gives 6). The receipt and entry do not
  state which aggregation is used, so the number is only defensible under the first-object/union
  reading that `parse_hf` implements.

Report: .ufo/waves/round-33/falsify/R33FHuggingFace.md
