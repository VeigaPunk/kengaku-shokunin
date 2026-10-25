# FxQuarantine — cross-check of R32Quarantine verdicts vs absent-defect-register (S091/S105)

Reviewer: `L1Kengaku32.FxQuarantine` (leaf). Date: 2026-10-25.
Target: `.ufo/waves/round-32/build/R32Quarantine.md` vs register
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.

Method per row: read the register row (lines 101/102), re-fetch the cited source
independently, re-locate the quoted span in the fetched bytes, then compare the seat's
verdict reason against the register's class and quote.

## Per-row agreement

### S091 — AGREES
- Register (line 101): lane `kengaku` round2, class `payload-absent`, cited source
  `https://jpn.nec.com/techrep/journal/g23/n02/230212.html`, quote `import re,html;s=open('/tmp/keng_s091.html',encoding='utf-8',errors='replace').read();s=re.sub(r'(?s)<[^>]+>',' ',s);pri…`.
- Seat verdict: REFUSE (absent). Reason: quoted span is a collector-local Python
  one-liner referencing scratch path `/tmp/keng_s091.html` — a fetch/processing command,
  not page content; cannot appear in the journal page.
- Independent re-check (this review): fetched `https://jpn.nec.com/techrep/journal/g23/n02/230212.html`
  with Safari UA + `--http1.1` → HTTP 200, 14,442 B (gzip; decompressed 60,344 B,
  ≈ seat's 60,335 B). Title: `<title>日本語性能に優れたNECの大規模言語モデル（LLM）: Vol.75 No.2: ビジネスの常識を変える生成AI特集 ～社会実装に向けた取り組みと、それを支える生成AI技術～ | NEC</title>` — genuine NEC Technical Journal page. Token counts in decoded bytes:
  `keng_s091` 0, `import re,html` 0, `re.sub` 0, `open('/tmp` 0, `errors='replace'` 0.
  Only `&lt;` occurrences (7) are LLM prompt-token examples
  (`&lt;｜im_start｜&gt;...`, `&lt;プロンプト、正例、負例&gt;`), not the snippet.
- Conclusion: verdict matches register (payload-absent; quote not in cited source) and
  the reason (collector-command span) is correct.

### S105 — AGREES
- Register (line 102): lane `kengaku` round3, class `payload-absent`, cited source
  `http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html`,
  quote `指定されたページまたはファイルは存在しません`.
- Seat verdict: REFUSE (absent). Reason: quoted span is the standard Japanese
  "page/file does not exist" error message — a fetch-time dead-link state, not content of
  the cited document; at the cited source the quote is absent.
- Independent re-check (this review): fetched the cited snapshot → HTTP 200, 13,029 B.
  Title: `<title>GENIAC事業 第1期 性能評価結果公開 （METI/経済産業省）</title>` — genuine
  archived METI page, not an error page. Token counts: `指定されたページ` 0, `存在しません` 0,
  full phrase 0. Body text is the GENIAC evaluation-results page (headline + JS snippet
  present; no 404/NR message).
- Conclusion: verdict matches register (payload-absent; quote not in cited source) and
  the reason (404-message span) is correct.

## Notes
- Seat's fetch evidence reproduced for both rows (NEC page real and on-topic; archived
  METI page real; both quotes absent; `&lt;` contexts are prompt-token examples, per the
  seat).
- No row needed the `unreachable-but-not-fabrication` mark; both sources fetched cleanly
  in this review too.
- First bare-curl attempt at the NEC page hit Akamai 403 "Access Denied" (418 B), same
  as the seat's attempt 1; the seat's Use 2 (browser UA) reproduced with Safari UA +
  `--http1.1` → HTTP 200. Consistent with the seat's network note.

## Verdict per row
| row | register class | seat verdict | seat reason matches register? |
|---|---|---|---|
| S091 | payload-absent | refuse (absent) | yes |
| S105 | payload-absent | refuse (absent) | yes |

VERDICT: verdicts-agree
