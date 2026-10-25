# R32 quarantine slice — kengaku hand-check (S091, S105)

- Executor: `L1Kengaku32.R32Quarantine` (leaf; no subagent dispatch)
- Date: 2026-10-25
- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` — kengaku rows at lines 101 (S091) and 102 (S105), both class `payload-absent`
- Method per row: (a) read the cited-source cell; (b) fetch the cited document with `curl --max-time 15`; (c) locate the quoted span in the fetched bytes; (d) verdict: adopt (quote located) / refuse (absent); `unreachable-but-not-fabrication` marked explicitly if the fetch fails for network/server reasons.

## S091 (kengaku round2) — VERDICT: REFUSE (absent)

| field | value |
|---|---|
| cited source | `https://jpn.nec.com/techrep/journal/g23/n02/230212.html` |
| quoted span | `import re,html;s=open('/tmp/keng_s091.html',encoding='utf-8',errors='replace').read();s=re.sub(r'(?s)<[^>]+>',' ',s);pri…` |

Fetch evidence:
- Attempt 1 (no User-Agent): HTTP 403, Akamai "Access Denied" body, 418 B.
- Attempt 2 (browser User-Agent): HTTP 200, 60,335 B. Content is the cited NEC Technical Journal page (meta keywords: `NEC,NEC技報,NEC Technical Journal,生成AI,NGS,LLM,大規模言語モデル,cotomi`; title verified). Fetched cleanly.
- Quote location: tokens `keng_s091`, `import re,html`, `re.sub`, `open('/tmp`, `keng_s091.html` occur 0 times. The only `&lt;` occurrences (2 lines) are unrelated LLM prompt-token examples (`&lt;｜im_start｜&gt;`), not the quoted snippet.
- Reason: the quoted span is a collector-local Python one-liner referencing scratch path `/tmp/keng_s091.html` — it is the fetch/processing command, not page content, and cannot appear in the journal page. Hand-check confirms absence. Refuse.

## S105 (kengaku round3) — VERDICT: REFUSE (absent)

| field | value |
|---|---|
| cited source | `http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html` |
| quoted span | `指定されたページまたはファイルは存在しません` |

Fetch evidence:
- Cited snapshot (https form of the cited URL): HTTP 200, 13,033 B. Content is the archived METI GENIAC 「第1期 性能評価結果公開」 page (`<title>GENIAC事業 第1期 性能評価結果公開 （METI/経済産業省）</title>`; body renders the evaluation-results text incl. the W&B hold-out-dataset paragraph). Not an error page.
- Quote location: tokens `指定されたページ` and `存在しません` occur 0 times in the archived page.
- Companion check (live target URL): HTTP 200, 10,768 B, identical GENIAC page; the phrase occurs 0 times.
- Reason: the quoted span is the standard Japanese "page/file does not exist" error message. It records a fetch-time dead-link state (what a collector sees when the target is unavailable), not content of the cited document. At the cited source the quote is absent. Refuse.

## Network-reachability note
Both cited sources were reachable and fetched. S091 required a browser User-Agent to bypass an Akamai 403 access policy; S105 was served by web.archive.org. No row needed the `unreachable-but-not-fabrication` mark.

## Summary

| id | fetch | quote located | verdict |
|---|---|---|---|
| S091 | HTTP 200 (60,335 B) after UA retry | no | refuse (absent; collector-command span) |
| S105 | HTTP 200 (13,033 B) from cited snapshot; live target HTTP 200 (10,768 B) | no | refuse (absent; 404-message span) |

VERDICT: <hand-checked>
