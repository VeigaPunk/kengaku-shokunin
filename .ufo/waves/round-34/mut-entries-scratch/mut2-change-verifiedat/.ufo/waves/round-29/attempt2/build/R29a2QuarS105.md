# R29a2QuarS105 — hand check of quarantine register row `kengaku / round3 / S105`

Seat: `L1Kengaku29.R29a2QuarS105` (leaf, read-only outside this file). No production edit was
made; the register was read, not touched. Scratch: `/tmp/r29a2-quars105/`.

Register under test (read only, not edited):
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:102`

```
| `kengaku` | round3 | S105 | `payload-absent` | http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html | `指定されたページまたはファイルは存在しません` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
```

## Verdict

**Neither page content nor a scrape artifact: the string is METI's WAF error shell, and the
census bound it from a note that says the opposite.**

Two separate answers, because the question splits:

1. **Is it the cited page's actual content? — No.** The pinned archive snapshot serves the real
   GENIAC page (HTTP 200, title `​GENIAC事業 第1期 性能評価結果公開`), and the string is **ABSENT**
   from those bytes.
2. **Is it a fetch-failure artifact? — Yes, in exactly one sense, and it is reproducible.** The
   string is what METI's live URL returns to a non-browser client: **HTTP 403** with a 5,045-byte
   body whose title is `指定されたページまたはファイルは存在しません`. It is genuine METI
   error-page text, not invented text — so the register's `payload-absent` class (its own
   "fabrication class", `absent-defect-register.py:20-23`) is **wrong for this row**.

- **Class I assign:** `quote-column misbinding — error-shell quote`. The census lifted a quoted
  span out of an *explanatory sentence in the lane's gate note* and treated it as a claimed
  quotation of the row's source, so the check could only ever return ABSENT. Same defect family
  as the sibling `R29a2QuarS091` row ("quote-column misbinding / extraction artifact").
- **No refusal needed.** The row's actual anchor — the ホールド・アウトデータ paragraph — is present
  verbatim in the cited snapshot today, so a corrected quote is available and nothing was
  fabricated (`absent-defect-register.py:4-24`: an ABSENT row is "a CANDIDATE, not a verdict",
  and the hand check ends in "a corrected quote or a refusal").

### HTTP status and what the page now renders

| Target | Request shape | HTTP | Bytes | Rendered content |
|---|---|---|---|---|
| `web.archive.org/web/20251118034714/…/selection_1/result_1/index.html` | `curl -L`, `UA: Mozilla/5.0 (X11; Linux x86_64)` | **200** | 13,027 | Title `​GENIAC事業 第1期 性能評価結果公開 （METI/経済産業省）`; headings `性能評価結果（日本語）(※2024年８月時点)` and `参考）性能評価結果（英語）(※2024年８月時点)`; the hold-out paragraph present at UTF-8 byte offset 7,458 |
| `www.meti.go.jp/…/selection_1/result_1/index.html` (live) | browser-like: UA + `Accept` + `Accept-Language: ja` + `Referer: https://www.meti.go.jp/` | **200** | 10,768 | Same title; `last-modified: Thu, 25 Jun 2026 02:16:07 GMT` — the page is **not** withdrawn |
| same live URL | bare UA `kengaku-lane/3.0` | **403** | 5,045 | Title and body `指定されたページまたはファイルは存在しません` — METI's "not found" shell |
| same live URL | `UA: Mozilla/5.0 (X11; Linux x86_64)` alone (no Accept/Referer) | **403** | 5,045 | Identical body, sha256 `201d4364…` — a UA string alone does not pass the WAF |

Observed page content, quoted (the row's page as the archive serves it today):

> `​GENIAC事業 第1期 性能評価結果公開 （METI/経済産業省）` … `性能評価結果（日本語）(※2024年８月時点)`

## Fetched evidence (2026-10-25)

All fetches in `/tmp/r29a2-quars105/`; every `curl` exited 0.

```
$ curl -sS -L --max-time 90 -A 'Mozilla/5.0 (X11; Linux x86_64)' -o arch.html -w 'code=%{http_code} size=%{size_download}\n' \
    'http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html'
code=200 size=13027          exit=0
```

Response headers of the same snapshot prove the memento and the captured original:

```
HTTP/1.1 200 OK
memento-datetime: Tue, 18 Nov 2025 03:47:14 GMT
x-archive-orig-date: Tue, 18 Nov 2025 03:47:14 GMT
x-archive-orig-last-modified: Wed, 29 Oct 2025 10:51:14 GMT
x-archive-orig-content-length: 10110
link: <https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html>; rel="original"
```

Byte-level probes on `arch.html` (13,027 B, sha256 `4fa9b78749406fcae029f80d244940ca63dbdfc8aa022a1ba9cd586f1071ccd0`):

```
'指定されたページまたはファイルは存在しません' : ABSENT     <- the register's quote
'ホールド・アウトデータ'                      : present ×1
'Jaster-GENIAC-v0.1'                          : present ×2
'JMT-Bench-GENIAC-v0.1'                       : present ×1
title                                          : ​GENIAC事業 第1期 性能評価結果公開 （METI/経済産業省）
```

The lane's own gate predicate, re-run by me on today's bytes
(`lanes/kengaku/round3/SOURCES-PROPOSED.md:62`):

```
$ grep -c 'ホールド・アウトデータ' arch.html
1
```

Live original, both request shapes (same minute, so the difference is the request, not the site):

```
$ curl -sS -I -L -A 'Mozilla/5.0 … Chrome/124.0 Safari/537.36' -H 'Accept: text/html' -H 'Accept-Language: ja' -H 'Referer: https://www.meti.go.jp/' <live URL>
HTTP/2 200 ; content-length: 10768 ; last-modified: Thu, 25 Jun 2026 02:16:07 GMT ; server: AmazonS3

$ curl -sS -I -A 'kengaku-lane/3.0' <live URL>
HTTP/2 403 ; content-length: 5045 ; server: AmazonS3
```

The 403 body is stable across two unrelated UA values — `live.html` (plain `Mozilla/5.0`) and
`live-bareua.html` (`kengaku-lane/3.0`) are the **same 5,045 bytes**,
sha256 `201d4364a8fcd39b8f36f0cce7715401602c8b568f47aad4dd7bbf2fd7bafe29`.

Wayback captures of that URL, from the CDX index (all three are 200, so no snapshot in the
archive is a 404):

```
20241223050854 https://www.meti.go.jp/…/result_1/index.html 200 text/html 5024
20250126083553 … 200 text/html 4714
20251118034714 … 200 text/html 4711
```

### One precision note on the archive bytes

A second fetch of the same snapshot is **not byte-identical**: 13,022 B, sha256 `b91ff47a…`. The
diff is confined to the Wayback instrumentation comment — the banner's server time
(`06:42:57` → `06:48:47 Oct 25, 2026`) and the timing block (`cdx.remote: 6.203` →
`75.112`, etc.). Content probes are identical in both copies (`ホールド・アウトデータ` ×1,
`Jaster-GENIAC-v0.1` ×2, `JMT-Bench-GENIAC-v0.1` ×1, 404 shell absent). So: **payload stable,
container churning** — cite the content predicate, never the archive-file sha.

## Where the register's quote actually came from

The census record itself names the line it bound to
(`.ufo/waves/corpus-expansion-1/quote-lint-full-v5.json`, identical in `-v4` and `quote-lint-full.json`):

```json
{ "lane": "kengaku", "round": "round3", "id": "S105", "verdict": "ABSENT", "fold": null,
  "quote": "指定されたページまたはファイルは存在しません",
  "url": "http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html",
  "line": "200) and serves METI's own \"指定されたページまたはファイルは存在しません\" shell with HTTP",
  "binding": "id" }
```

That `line` is `lanes/kengaku/round3/SOURCES-PROPOSED.md:65`, inside the Gate S105 note:

```
64:  full page to browser-like requests (UA + Accept + Accept-Language + Referer → HTTP
65:  200) and serves METI's own "指定されたページまたはファイルは存在しません" shell with HTTP
66:  403 to anything else.
```

The sentence is the lane documenting the *opposite* of a withdrawal. Quoting it as the row's
evidence inverts its meaning, and because the cited source is the snapshot (which the sentence
contrasts with the live URL), ABSENT was the only possible outcome.

For completeness, the row's real anchor cell (identical in the lane's proposal and the staged
merge row) is the hold-out paragraph:

- `lanes/kengaku/round3/SOURCES-PROPOSED.md:28` and `merge/kengaku/SOURCES.append.md:35`, anchor
  cell `§ 性能評価結果（日本語）(※2024年８月時点): "GENIACでは、公平性担保のため完全に未知なテストデータを用いて…"`;
- located today at UTF-8 byte offset **7,458** of `arch.html`, immediately after
  `<h2>性能評価結果（日本語）(※2024年８月時点)</h2>` and before the 図1/図2 caption paragraph —
  body prose, not navigation.

## Second finding: the row's note is false about local artifacts

The register's note says "cited source, companion URLs **and local artifacts** were all checked;
the quote is in none of them". For this row that is not true of the lane tree: the string is in
**seven** local files, including the gate note the census read.

```
lanes/kengaku/round3/DOMAIN.md:31
lanes/kengaku/round3/CHANNELS.md:56
lanes/kengaku/round3/SOURCES-PROPOSED.md:65
lanes/kengaku/round3/KNOWLEDGE-PROPOSED.md:337
lanes/kengaku/round3/SEARCH-LOG.md:50
lanes/kengaku/round3/SEARCH-LOG.md:78
lanes/kengaku/round3/CANNOT-ANSWER.md:18
```

So the census's "local artifacts" check covers something narrower than the lane's prose — a
scanner-scope gap, not a fabrication. It also means this binding will recur: the same shell string
is quoted in the merge tree at
`merge/kengaku/knowledge/corpus/knowledge/cjk-benchmark-governance-2026-10-23.md:114`,
`merge/kengaku/knowledge/corpus/knowledge/cjk-eval-journal-access.md:105`, and in the withdrawal
note of `merge/kengaku/SOURCES.append.md:42` (`S112`). **Lead, not a verdict:** `S112` (and any
kengaku row whose note mentions the WAF shell) plausibly carries the same misbinding and deserves
its own hand check before anyone treats its ABSENT label as a fabrication.

## What a reader should do with this row

1. **Do not refuse it and do not treat it as fabricated.** No claim in the lane rests on the error
   shell: `lanes/kengaku/round3/KNOWLEDGE-PROPOSED.md:289-296` quotes the hold-out paragraph, and
   the shell appears only in the access-recipe prose (`:335-341`).
2. **Correct the quote binding** to the anchor cell's paragraph (present today at offset 7,458), or
   record the row as `quote-column misbinding` with the error shell named as such.
3. **Keep the archive URL pinned.** The oracle for this row is the snapshot's content predicate
   (`grep -c 'ホールド・アウトデータ'` → 1), because the live URL's status is a function of request
   shape (200 browser-like, 403 otherwise) and therefore unusable as a gate.

## Bounds actually observed

- Register and lane tree read only; nothing written under `shokuknow`, `shokunin`, or any sibling
  lane. No campaign tool (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`,
  `absent-defect-register.py`) was run.
- One file written: this report. Scratch in `/tmp/r29a2-quars105/` only.
- No installs or upgrades were needed; no pacman transaction attempted. Tooling used as found:
  `curl 8.23.0`, `Python 3.14.8`, `grep 0.2.0 (pi-uu-grep)`.
- Unresolved: whether the census intends lane prose to count as a local artifact (its note implies
  it does); and whether the register's `S112` row has the same misbinding. Both are outside this
  row's question and stated as leads above.
