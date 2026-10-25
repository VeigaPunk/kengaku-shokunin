# Quarantine slice — independent reconstruction

Command: `awk -F'|' -v l='kengaku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`

Observed output (2 lines):
```
 S091  `payload-absent` 
 S105  `payload-absent` 
```

Full verbatim register rows (file `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, lines 101–102):

| `kengaku` | round2 | S091 | `payload-absent` | https://jpn.nec.com/techrep/journal/g23/n02/230212.html | `import re,html;s=open('/tmp/keng_s091.html',encoding='utf-8',errors='replace').read();s=re.sub(r'(?s)<[^>]+>',' ',s);pri` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
| `kengaku` | round3 | S105 | `payload-absent` | http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html | `指定されたページまたはファイルは存在しません` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |

These are the entire qualifying slice: the awk command yields exactly two rows, matching the two `kengaku` register rows at lines 101–102. Summary staleness: none observed. Header says corpus-expansion rounds 1–10 (line 1); the by-lane summary says `kengaku | 2` (line 252), consistent with the reconstructed two rows.

VERDICT: recon-quarantine (2 rows)
