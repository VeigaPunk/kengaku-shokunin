# R44Quarantine — hand check of the `kengaku` rows in the ABSENT defect register

Seat: R44Quarantine (executor, leaf). Wave: kengaku round 44 (build + attack, v2).
Read-only throughout: `/home/vgpnk/Projects/shokuknow` (the source repo — another campaign's tree, never
written/fetched-through) and the lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. I wrote only this
report, its subdir (`wave/R44Quarantine/`) and `/fast/scratch/hyaku/kengaku-r44/R44Quarantine/`.
No tool installed, upgraded or removed (`pacman` untouched, nothing needed). No subagent, no background job.
Every fetch and every counter-style probe below ran inside
`kengaku-shokunin/.ufo/waves/round-44/claims/envelope.sh`; both runs end
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`, so both measurements are valid.

Register under test (read, never edited):
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines, 83,621 B, mtime
`2026-10-24 08:37:00 -0300` — the same file round-38/39 rescreens measured (`R38MergeRescreen.md:42`,
`R39MergeRescreen.md:58`).

```
$ sha256sum absent-defect-register.md
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  absent-defect-register.md
$ grep -cE '^\| `[a-z0-9_-]+` \| round[0-9]+ \| S[0-9]{3,} \|' absent-defect-register.md
194
$ grep -E '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' absent-defect-register.md | awk -F'|' '{print $3 $4 $5}'
 round2  S091  `payload-absent`
 round3  S105  `payload-absent`
```

## 1. The slice: 2 data rows (summary row excluded)

- data rows in the register: **194** (`grep -cE` above).
- `kengaku` data rows: **2** — `round2 S091` (register line 101) and `round3 S105` (line 102).
- line 252 `| kengaku | 2 |` is the **by-lane summary row**, not a data row: it has no `round` cell and no
  `S` id, so the derivation regex cannot see it. Excluded, per the assignment; it independently agrees with 2.
- the register's third section (`## Rows whose quotes were NEVER CHECKED`, lines 256–375) names no `kengaku`
  row — `sed -n '256,375p' … | grep -ciE 'kengaku|S091|S105'` → **0**. So the slice is exactly these two rows,
  both in the fabrication-class section, and no `kengaku` row is merely unreachable.

## 2. Verdicts

| row | registered span (abridged) | what the span actually is | cited source, fetched | anchor located? | verdict |
|---|---|---|---|---|---|
| `kengaku` round2 **S091** | `import re,html;s=open('/tmp/keng_s091.html',…);…;pri` | first 120 chars of the lane's **recheck command** (`round2/SOURCES-PROPOSED.md:43`) | NEC 技報 page: HTTP 200, 60,334 B, sha256 `1b35525e…a69ba7` | yes — the 70-char anchor sentence, present verbatim (`raw_line=276`) | **present-with-anchor**; register class wrong |
| `kengaku` round3 **S105** | `指定されたページまたはファイルは存在しません` | quoted span inside the lane's **explanatory note** about the *live* URL (`round3/SOURCES-PROPOSED.md:65`) | archive snapshot: HTTP 200, 13,030 B, sha256 `0c64866b…b34810` | yes — but at a *different* anchor: live URL + bare UA → HTTP 403, 5,045 B, sha256 `201d4364…afe29`, title line carries the span | **present-with-anchor**; register class wrong |

Counts for the acceptance line: rows **2**, present-with-anchor **2**, demonstrably-absent-no-anchor **0**,
unverifiable **0**. Neither row is a fabrication: in both cases the census bound a span out of the lane's own
**gate machinery** and then asked whether the cited source contains it — a question that had to answer ABSENT.

## 3. Row S091 — `payload-absent` is a binding error, the claim holds

The registered span is not a quotation. It is the opening of the one-line recheck command:

```
round2/SOURCES-PROPOSED.md:40  ### Gate S091 — NEC技報 Vol.75 No.2
:41  - URL: https://jpn.nec.com/techrep/journal/g23/n02/230212.html
:42  - Pinned revision: NEC技報 Vol.75 No.2（2024年3月）; opened 2026-10-23
:43  - Command: `curl -fsSL '…/230212.html' -o /tmp/keng_s091.html && python3 -c "import re,html;s=open(…)…"`
```

The census agrees about where it bound: its finding for this row carries
`"line": "- Command: \`curl -fsSL 'https://jpn.nec.com/…' -o /tmp/keng_s091.html && python3 -c \"import re,html;…`
(`quote-lint-full-v5.json`, findings, `lane=kengaku round=round2 id=S091`, `"binding": "id"`, `"sweep": false`).
So the span's only possible home is the lane's own file — where it is present:

```
$ grep -cF "import re,html;s=open('/tmp/keng_s091.html',encoding='utf-8',errors='replace').read();s=re.sub(r'(?s)<[^>]+>',' ',s);pri" \
    /home/vgpnk/Projects/shokuknow/lanes/kengaku/round2/SOURCES-PROPOSED.md
1
```

The anchor the row actually rests on — the phrase inside that command — is in the cited page today:

```
$ curl -sS -L --max-time 45 -A "$UA" -H 'Accept: text/html,application/xhtml+xml' -H 'Accept-Language: ja,en;q=0.9' \
    https://jpn.nec.com/techrep/journal/g23/n02/230212.html -o r/s091.html -w 'http=%{http_code} bytes=%{size_download}\n'
http=200 bytes=60334
$ sha256sum r/s091.html
1b35525e2e697d66012eb4b6a8e7706ea430d6fdf762cef4f358e24218a69ba7  r/s091.html
# tag-stripped + html.unescape, then substring:
anchor_present= True | anchor_in_raw= True
full_sentence_present= True len= 70
```

Anchor location: raw HTML line **276** of the fetched bytes, inside the figure-4 discussion —
“図4 にRAKUDAベンチマークにおける評価結果を示します… **ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていない**ことには注意が必要となります。”
(I quote the fragment, 33 Japanese characters of a 70-character sentence; the lane's ≤25-word rule for CJK is
unresolved — round-29 flagged it, `R29a2QuarS091.md:135`, and I do not decide it here.)

Cross-checks, stated honestly: the lane's committed capture of the same page
(`.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html`, 60,335 B, sha256 `b60af775…a262b1`) also
carries the sentence (`grep -cF` → 1), but its bytes are **not** mine: `cmp -l` reports **39,973** differing
byte positions. The NEC page is live and its bytes are header/dynamic-content dependent; the anchor sentence is
stable in both fetches. The old 418-byte `Access Denied` capture next to it (`nec-s091.html`, sha256 `967e4c24…`)
is the artifact round-29 already showed was not evidence of absence.

## 4. Row S105 — the span is real METI text, anchored at the *live* URL, not at the cited snapshot

Four separate questions, four answers:

1. **Is the span in the cited archive snapshot?** No. `grep -c -F` over the 200/13,030 B snapshot: hits **0** for
   `指定されたページまたはファイルは存在しません`.
2. **Is the cited snapshot the page the row is about?** Yes, and it is the real page (title
   `GENIAC事業 第1期 性能評価結果公開 （METI/経済産業省）`), carrying the row's own gate anchor and all four
   phrases the entry claims: `ホールド・アウトデータ` 1, `Weights and Biases` 1, `Jaster-GENIAC-v0.1` 2,
   `JMT-Bench-GENIAC-v0.1` 1. The hold-out paragraph sits at snapshot raw line 112:
   “Weights and Biases社と協業し、**ホールド・アウトデータ**(最終的な性能評価を行うための非公開のデータセット)を生成・評価を行いました。”
3. **Is the span in the live original?** Yes — under exactly the request shape the row's note names, and only
   under it:

   | request shape | HTTP | bytes | span hits | `ホールド・アウトデータ` |
   |---|---|---|---|---|
   | bare UA `kengaku-lane/3.0` | **403** | 5,045 | **2** | 0 |
   | curl default UA | **403** | 5,045 | **2** | 0 |
   | browser-like: UA + `Accept` + `Accept-Language: ja` + `Referer: https://www.meti.go.jp/` | **200** | 10,768 | 0 | **1** |

   The 403 body's line 12 is `<title>指定されたページまたはファイルは存在しません （METI/経済産業省）</title>` —
   METI's own shell, not invented text. Its sha256 `201d4364a8fcd39b8f36f0cce7715401602c8b568f47aad4dd7bbf2fd7bafe29`
   matches the prefix round-29 recorded (`R29a2QuarS105.md`, `201d4364…`), i.e. the error shell is byte-stable
   across rounds, and the bare-UA/default-UA bodies are identical.
4. **Where did the census bind it?** To the row's own prose, `round3/SOURCES-PROPOSED.md:65`, a continuation
   line of the note at :63–68 that says “the original METI URL is **not withdrawn**” and describes this very
   403 shell. Census finding: `"line": "200) and serves METI's own \"指定されたページまたはファイルは存在しません\" shell with HTTP"`.
   The span is present in its bound anchor (`grep -cF` on `round3/SOURCES-PROPOSED.md` → 1).

So the registered citation (the archive snapshot) does not contain the registered span, but the span is
**genuine payload** at a nameable anchor (URL + request shape + status + digest), which is the definition of
present-with-anchor, not fabrication. Correct quote available; no row refusal needed on evidence grounds.

## 5. Mechanism — why the census produced ABSENT, and how far it generalises

Both spans are spans of the lane's *gate block*, which the census binds as if it were a quotation: S091's came
out of a `- Command:` payload (a quoted URL inside the command made it parse as a quoted span), S105's out of a
double-quoted phrase in a `- Note:` sentence. Neither is claimed source text, so the match could only fail.
A sibling shows the same extractor behaving benignly for the same reason: `round2 S092`'s span is its `grep`
pattern, and it passed only because that pattern happens to occur in the GitHub file (`sweep-found`, `exact`).

How far it generalises — measured over all 194 data rows (heuristic, reported as such):

```
rows whose quote cell is a program payload (python -c / starts with "import "): 1   [kengaku round2 S091]
rows whose cited source cell is a lanes/… artefact path:                     8
rows whose span names a lane file or an internal S-id:                       2   [kake S206, tameshi S141]
```

So this is **not** a corpus-wide class: S091 is the register's only embedded-program span. The honest scope is
narrower and sharper: **within the `kengaku` slice, 2 of 2 rows are binding errors, not content errors** — one
of the rare program-payload shape, one of a note-prose shape that these heuristics do not catch. Any fix belongs
in the census's quote extractor (skip `- Command:` / `- Note:` continuation lines, or bind a row's span only
from a `Quote:`/「」 field), not in the two corpus rows.

## 6. Id collision — the register's ids no longer resolve to these documents in the lane corpus

Same string, different document:

| id | register row (round cell preserved) | current lane corpus (`corpus/SOURCES.md`) |
|---|---|---|
| `S091` | `round2` → NEC 技報 Vol.75 No.2, `round2/SOURCES-PROPOSED.md:41` | `:104` → “Agentic Benchmark Checklist (ABC) — https://arxiv.org/abs/2507.02825” |
| `S105` | `round3` → METI GENIAC 第1期 性能評価結果公開, `round3/SOURCES-PROPOSED.md:60` | `:120` → Terminal-Bench 2.0 protein-assembly `tests/test_outputs.py` |

The register is internally consistent because it keeps the `round` cell; a consumer that resolves the bare id
against `corpus/SOURCES.md` lands on an unrelated held row. Round 38/39 already noted this (`R38MergeRescreen.md:49`);
I confirm it against today's files rather than copying the claim. Consequence for integration: the NEC row has
**no row in the curated corpus to correct** — `grep -rln '230212.html' corpus/` hits only
`corpus/lessons/round-34-verifier-spotcheck.md` and `…round-35…`, so “correct the quote” has no corpus target;
the METI row survives only inside the downstream entry that cites `S105`.

## 7. Prior art — where I agree, and one assertion my measurement contradicts

- `R29a2QuarS091.md` (round 29): same class (“quote-column misbinding / extraction artifact”), same anchor,
  quote-present. **Agree**; re-measured independently today (my own fetch, my own digests).
- `R29a2QuarS105.md` (round 29): same split (snapshot carries the hold-out paragraph; the shell is the live
  URL's 403 body). **Agree**, including the byte-stable 5,045 B shell.
- `R39MergeRescreen.md:58-68`: slice = 2 rows, summary-row and NEVER-CHECKED derivations match mine. **Agree.**
- `R38MergeRescreen.md:49`: “S105's ‘quote’ is an error page for a withdrawn METI page.” **Disagree on
  *withdrawn*.** The live GENIAC index is up: browser-like → HTTP 200/10,768 B carrying the hold-out paragraph;
  the row's own note says “the original METI URL is **not withdrawn**” (`round3/SOURCES-PROPOSED.md:63`). The
  *withdrawn* document is the programme PDF `geniac_kentjokyo.pdf` (round-4 row S112), a different URL. The
  rescreen's summary conflates the two; flagging for the L1, no edit made.

## 8. Integration recommendation (for the L1 — I edit nothing)

1. Do **not** adopt either registered span as a quote; both are lane machinery.
2. If an entry needs S091: the corrected span is the NEC sentence (70 chars) at `raw_line=276`, pinned by
   sha256 `1b35525e…`; resolve the CJK word-count rule first (round-29 flagged it, still open).
3. If an entry needs S105: use the snapshot's hold-out paragraph. The error shell is defensible only with
   URL + request shape + status + digest, which the lane's row schema does not carry — recommend against
   quoting it at all; it evidences CHANNELS, not the row's content.
4. Downstream, round-38 named the citing entries `cjk-eval-journal-access.md` (S091) and
   `cjk-benchmark-governance-2026-10-23.md` (S105). I did not re-adjudicate those entries (out of scope); the
   corrected spans above are what an admit would need.
5. File the census defect with the extractor owner: rows whose bound line starts with `- Command:` or lies in a
   `- Note:` continuation should not yield spans.

## 9. Limits and risks

- Live-web measurement: the NEC page is dynamic (39,973 byte positions differ from the round-34 capture, same
  anchor sentence), so my digest pins *my* bytes, not the page forever. The archive snapshot is immutable in
  principle; its digest is given.
- Request-shape dependence is invisible to every whitespace/tag fold the census applies; no single fetch can
  settle S105's shell phrase. I report both shapes rather than choosing one.
- The 194-row generalisation in §5 is a pattern count over quote cells, not a hand check of 194 rows; I claim
  only what the count shows.
- All fetches were content reads of public pages; nothing was written to the source repo or the lane.

## 10. Receipts

- `wave/R44Quarantine/envelope-fetch.txt` — first envelope run (both sources + the bare-UA live probe).
- `wave/R44Quarantine/envelope-fetch2.txt` — second envelope run (browser-like live probe, default-UA probe,
  anchor contexts).
- `wave/R44Quarantine/evidence.txt` — digests, sizes, hit counts, anchor lines, register derivation.

Envelope lines, verbatim:

```
ENVELOPE start 20:36:07 cwd=/fast/scratch/hyaku/kengaku-r44/R44Quarantine
ENVELOPE end 20:36:14 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 20:36:34 cwd=/fast/scratch/hyaku/kengaku-r44/R44Quarantine
ENVELOPE end 20:36:36 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

VERDICT: quarantine-rows-2-present-2-absent-0
