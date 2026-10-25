# R29a2QuarS091 — hand check of quarantine register row `kengaku / round2 / S091`

Seat: `L1Kengaku29.R29a2QuarS091` (leaf, read-only outside this file).
Register under test (read only, not edited):
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:101`

```
| `kengaku` | round2 | S091 | `payload-absent` | https://jpn.nec.com/techrep/journal/g23/n02/230212.html | `import re,html;s=open('/tmp/keng_s091.html',encoding='utf-8',errors='replace').read();s=re.sub(r'(?s)<[^>]+>',' ',s);pri` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
```

## Verdict

**quote-present — the row is mislabelled, not fabricated.** The registered "quote" is not a
quotation at all: it is the first 120 characters of the **recheck command** in the lane's own
gate block. The anchor the row actually rests on is present verbatim in bytes I fetched today.

- Class I assign: **`quote-column misbinding` / extraction artifact** — the census scanner lifted
  the `python3 -c "…"` payload out of the `- Command:` line and treated it as a claimed quotation,
  so the check could only ever return ABSENT.
- Class the register assigned: `payload-absent` — **wrong for this row**. No passage was invented
  and nothing is unreachable; the register's own header says an ABSENT row is "a CANDIDATE, not a
  verdict" and the hand check's expected outcome is "a corrected quote or a refusal"
  (`absent-defect-register.py:4-24`). Corrected quote is available; **no refusal needed**.

## Fetched evidence (2026-10-25)

Fetch (own scratch only, `/tmp/r29a2-s091q/`):

```
$ curl -sS -LR -o page.html -w 'HTTP=%{http_code} URL=%{url_effective} SIZE=%{size_download} CT=%{content_type}\n' \
    --max-time 60 -A 'Mozilla/5.0 (X11; Linux x86_64)' \
    'https://jpn.nec.com/techrep/journal/g23/n02/230212.html'
HTTP=200 URL=https://jpn.nec.com/techrep/journal/g23/n02/230212.html SIZE=60335 CT=text/html
exit=0
```

Second, header-only fetch (proves a live 200 today, and dates the bytes):

```
HTTP/2 200
last-modified: Thu, 19 Mar 2026 09:48:51 GMT
etag: "db0f-64d5d79cc66c0"
cache-control: no-store
date: Sun, 25 Oct 2026 06:42:16 GMT        <- the access date of this check
content-type: text/html
```

`sha256(page.html) = 0b661f1c7ce49b82ff071d6e52de7c142325845df43ac89118a370adb6146dc6`
(60,335 bytes, UTF-8, `<title>日本語性能に優れたNECの大規模言語モデル（LLM）: Vol.75 No.2 …`).
Body text after tag-strip: 13,403 chars — the **full article**, §6.2 through §7 むすび, so no PDF
fetch is needed for this anchor. Page identity as printed on the page:
`Vol.75 No.2 2024年3月` (matches the lane's registry row "NEC技報 Vol.75 No.2（2024年3月）").
The bytes' `last-modified` (2026-03-19) precedes the lane's 2026-10-23 open and today's open, so
the same text was served on both dates.

### The anchor I located

The lane's real anchor is the `anchor` cell of the registry row
(`lanes/kengaku/round2/SOURCES-PROPOSED.md:23`):

> 「ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていないことには注意が必要となります。」

Located in today's fetched bytes:

```
SENT present: True | byte offset 43351 | raw line 276 col 447
PROBE present: True
gate predicate printed value would be: True
```

Raw context at that offset (unambiguous — it is body prose, not a nav label or snippet):

```
…と比較すると大きく勝率で上回っています。ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていないことには注意が必要となります。</p> <!--/.str-inner --> …
```

It sits in §6.2 対話モデルとしての評価, immediately before the 図4 caption
("図4 RAKUDAベンチマークにおいて他モデルに対するNECの開発したLLMの勝率"). `RAKUDA` occurs 6×
in the article; the 「ただし…注意が必要となります。」 sentence is unique (1×).

I also ran the gate's own predicate string, which the registered one-liner tests for:

```
PROBE = 'RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため'
PROBE present: True        # i.e. the Gate S091 command, re-run today, prints True
```

## What the registered quote actually is — provenance, traced

1. `lanes/kengaku/round2/SOURCES-PROPOSED.md:43` (§ "Gate S091") is a recheck command, not a quote:
   `- Command: `curl -fsSL '…/230212.html' -o /tmp/keng_s091.html && python3 -c "import re,html;…print('RAKUDAベンチマークは…のため' in html.unescape(s))"``
2. `quote-lint-full-v5.json` (and `-v4.json`) carry the finding
   `{lane:kengaku, round:round2, id:S091, verdict:ABSENT, quote:"import re,html;s=open('/tmp/keng_s091.html'…", line:"- Command: `curl -fsSL '…", binding:"id"}`
   — the `line` field is byte-identical (to 200 chars) to `SOURCES-PROPOSED.md:43`, and the `quote`
   is the **double-quoted span inside that command**. The span scanner
   (`quote-lint.py:72-75`, `QUOTE_SPAN_RE`, second alternative `"…"`) matches any `"…"` of length
   4–600 on a line it considers quote-bearing, and a `- Command:` line is not excluded the way
   `META_LINE_RE` (`quote-lint.py:91-94`) excludes locator/metadata lines. A Python program is
   therefore checked for literal presence in an HTML article: it can never match.
3. `absent-defect-register.py:142` renders each census quote as `` `{q[:120]}` `` — hence the
   truncated, 120-char one-liner in the register cell. Verified: the registered string is exactly
   chars 107–226 of the `SOURCES-PROPOSED.md:43` command (`REG_Q in CMD == True`, next chars after
   the cut are `nt('RAKUDAベン`), i.e. a mechanical slice, not a paraphrase.
4. Direct presence tests: the registered string as a literal is in **neither** the raw bytes nor the
   stripped text (`import re,html;s=open('/tmp/keng_s091.html'… ) in raw: False`) — trivially, as it
   is source code. So the register's note "the quote is in none of them" is **true but vacuous**.

## Scope of the extraction defect (so the L1 does not over- or under-read it)

Across all 1,841 absent findings in `quote-lint-full-v5.json`, exactly **2** rest on a
`- Command:` line — both in this lane: `kengaku round2 S091` (verdict `ABSENT`) and
`kengaku round2 S092` (verdict `sweep-found`, i.e. it escaped because `SWEEP_HINT`,
`quote-lint.py:84-86`, fires on the `grep` in its command). This is a **narrow, singular**
scanning defect, not a systemic class: a register-wide reclassification is **not** warranted.

## Operability notes for the L1 (no action taken here)

1. **Correct quote for the row** (if anyone fixes the register): the `anchor` cell of
   `SOURCES-PROPOSED.md:23`, not the `- Command:` payload. The census should read the table
   `anchor` cell — which is where the lane put the quotation — and treat `- Command:` lines like
   `META_LINE_RE` lines. Two rows in the whole corpus are affected.
2. **The register's "local artifacts … were all checked" clause is unfalsifiable for this row.**
   `/tmp/keng_s091.html` does not exist (`ls: cannot access … No such file or directory`) and
   `lanes/kengaku/round2/` holds no archived page (`find … -name '*.html' -o -name '*.pdf'` → empty).
   There was no surviving artifact to check; the local-artifact clause could not have fired.
3. **File mtime is not access evidence.** The page I saved today carries
   `mtime=2026-03-19 06:48:51 -0300`, which is the server's `last-modified`
   (`Thu, 19 Mar 2026 09:48:51 GMT`) inherited into the local file — not the fetch time. Any future
   "opened on <date>" proof for a saved page must cite the HTTP `date` header / `etag`, never the
   file timestamp. This matters directly for C1's re-open duty: a 2026-10-25 fetch leaves a file
   dated 2026-03-19 on disk.
4. **This source is safe for C1's re-grounding.** It returns 200 today, content is unchanged since
   2026-03-19 (`etag: "db0f-64d5d79cc66c0"`, `cache-control: no-store`), the anchor is body prose
   in the HTML (no PDF dependency), and the ≤25-word located quote is
   「ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていないことには注意が必要となります。」 (44 Japanese characters; count words by the lane's rule before pasting — the sentence is a single clause, so if the ≤25-word rule is counted as whitespace tokens it is 1, and if counted per morpheme it exceeds 25). **Flag, not a verdict:** whoever drafts C1's S091 quote must check which counting rule the round applies; I did not decide it.
   Note the merged entry `merge/kengaku/knowledge/corpus/knowledge/cjk-eval-journal-access.md:2`
   carries `# 本文` as its source marker (a lane section convention, used alongside `# Abstract`
   and `# 摘要`) and the actual quote at :84 — the marker is not a page literal (`"本文"` occurs
   0× in the page text), so it must not be mistaken for a located quote.

## Residual unknowns

- The exact producer of `quote-lint-full-v*.json` is not in
  `.ufo/waves/corpus-expansion-1/` (`quote-lint.py` there emits `fold`/`quote`/`url`/`line` but no
  `binding` key; `absent-defect-register.py` defaults to a non-existent
  `quote-lint-full-v3.json`). I could not read the scanner that added `"binding": "id"`. Does not
  change the verdict: the `line` field is byte-identical to `SOURCES-PROPOSED.md:43` and the
  `quote` is that line's double-quoted span.
- Whether the register is meant to quote the table `anchor` cell at all is a campaign-format
  question I did not settle; I report only that the cell, not the command, is the locatable quote.

## Tool installs / updates

None. Used only preinstalled `curl`, `python3`, coreutils. No `pacman` transaction attempted
(host-wide pause respected).

Scratch: `/tmp/r29a2-s091q/page.html` (60,335 B, sha256 `0b661f1c7ce49b82ff071d6e52de7c142325845df43ac89118a370adb6146dc6`).

**Scratch-retention independence.** This report cites **no** `.ufo/waves/round-35/scratch/` path
(`grep -c round-35` over this file = 0). That tree is not in this lane at all — it belongs to
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/` — and it is unstable, so no claim
about its state is load-bearing here. What I verified on 2026-10-25 in that repo: `scratch/` was
absent at check time (re-created and erased again during the round, per `L1Mado35.RevEntryR15`); a
checkpoint copy is tracked at `scratch-evidence/` — 59 seat dirs, `git ls-files … | wc -l` = **261**,
commit `4efaf63` ("checkpoint the 235 seat evidence files …"). Note the three file counts in
circulation (235 in the commit subject, 240 from one peer, 261 measured) do not agree; none is mine
to reconcile. Nothing above needs any scratch file, or the network to be re-read: the verdict rests
on text inlined here — the anchor sentence verbatim, its byte/line/column offsets, the HTTP status
and headers, the local sha256, and the gate predicate's printed value. If the `/tmp` copy is also
swept, reproduce with:

```
curl -sS -LR -o /tmp/r29a2-s091q/page.html -w 'HTTP=%{http_code} SIZE=%{size_download}\n' \
  -A 'Mozilla/5.0 (X11; Linux x86_64)' 'https://jpn.nec.com/techrep/journal/g23/n02/230212.html'
sha256sum /tmp/r29a2-s091q/page.html   # 0b661f1c…46dc6 as of 2026-10-25; etag "db0f-64d5d79cc66c0"
```

No file outside this report was created or modified; the register and every campaign file are
untouched.
