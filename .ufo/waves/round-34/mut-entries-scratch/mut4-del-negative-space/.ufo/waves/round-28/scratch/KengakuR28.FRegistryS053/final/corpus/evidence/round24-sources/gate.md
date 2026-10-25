# Round 24 — SOURCES gate receipts (kengaku)

Contract: SOURCES-CONTRACT-v1 rule 1 requires each row's URL, access date, and a ≤25-word location-grounded quote.
Access date: 2026-10-19.
Method: reopened all web URLs with read; streamed curl responses to sha256sum and counted bytes with wc -c; quoted own-work anchor lines via sed -n and hashed the cited files.

| id | URL or path | accessed | quote (≤25 words, verbatim) | location | sha256 |
|---|---|---|---|---|---|
| S001 | https://aclanthology.org/2026.gem-main.50/ | 2026-10-19 | “a comparative analysis of five detection families (string-matching, likelihood-based, membership inference, LLM-prompted detection, and benchmark auditing), including access assumptions and failure modes” | Abstract | f4b3eb7ffbf5354091117eaaad35ac528f5b7571f904fd9fec7f5f45697e2221 (47,522 bytes) |
| S002 | https://arxiv.org/html/2510.02386v1 | 2026-10-19 | “Yet, even a brief Group Relative Policy Optimization (GRPO) training can markedly conceal contamination signals that most detection methods rely on.” | Abstract | 3eef8073f4abf573ff15acbdb32a5fa062484345cdbc07084e395825430d3e27 (548,019 bytes) |
| S003 | https://arxiv.org/html/2507.11405 | 2026-10-19 | “Additionally, the current DCR framework is not yet adaptable to generative tasks such as machine translation and summarization.” | Limitations | 04ea3e11fba8a2d40f9243ed1349023af13cf929ed9e57f63d138549f14252b1 (359,691 bytes) |
| S004 | https://arxiv.org/abs/2605.19999 | 2026-10-19 | “we argue that benchmark datasets should be contamination-resistant, i.e., unlearnable, but support inference.” | Abstract | 21d842dbd317820bdf614e9da7a7d312d78f807d5caf2dd2d53d54059d516e5a (42,283 bytes) |
| S005 | https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ | 2026-10-19 | “We found that 59.4% of the 138 problems contained material issues in test design and/or problem description” | ## Too narrow and too wide tests | 8bd40cbc1e2caefe5c616012e52c182d59b1b9fde47f31f028966a2a11c7c1bb (9,843 bytes) |
| S006 | https://openai.com/index/separating-signal-from-noise-coding-evaluations/ | 2026-10-19 | “we estimate that ~30% of SWE-bench Pro tasks are broken”; “we retract our earlier recommendation to adopt SWE-Bench Pro” | Opening summary; Discussion | fba4c0054cf5b60a1e4190477df6eb62b4da27ed792827ab6eeac867acb0f454 (9,852 bytes) |
| S007 | https://arxiv.org/html/2602.16763 | 2026-10-19 | “We define benchmark saturation as the loss of reliable discriminative power among top-performing models under comparison.” | §2.1 Definition and Scope | ae41d64703217a0015b9ec75eb76961e1444180c6c5ed49e0364724ac789d609 (450,852 bytes) |
| S008 | https://arxiv.org/abs/2511.04703 | 2026-10-19 | “we provide eight key recommendations and detailed actionable guidance to researchers and practitioners in developing LLM benchmarks.” | Abstract | e407cba7b76a090da01247eff9c1477e582f4a9b95d17e0cbeab5f957f0dbbbb (47,021 bytes) |
| S009 | https://arxiv.org/html/2506.22316 | 2026-10-19 | “three novel, previously unstudied types: rubric order bias, score ID bias, and reference answer score bias.” | Abstract | 3aa84ebbae3bdc81714e8c4976d0bb5e20c6a0affa85be2e31310c3477ab55f3 (243,278 bytes) |
| S010 | https://arxiv.org/html/2602.02219 | 2026-10-19 | “the top-1 candidate flips on 15% to 41% of prompts.” | §5.6 Downstream Rank Reversal | a89e2256f106c2a2daa72711175b6355951636a2f76e9db2e117dcc02aa49678 (281,257 bytes) |
| S011 | https://proceedings.mlr.press/v306/lee26bl.html | 2026-10-19 | “Our framework constructs confidence intervals that account for uncertainty from both the test dataset and a human-labeled calibration dataset.” | Abstract | 33a1bcaada76e3af6c2812fb288ef831a798bb62c02c34ff7fa96adb417797ad (15,551 bytes) |
| S012 | https://arxiv.org/html/2306.05685v4 | 2026-10-19 | “Our results reveal that strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement” | Abstract | a1768d348815995e70fe3c49c1164e220a74fbd2c35211cffea1861b6ed4e30f (248,401 bytes) |
| S013 | https://arxiv.org/html/2503.14499 | 2026-10-19 | “we propose a new metric: 50%-task-completion time horizon, the time humans typically take to complete tasks that AI models can complete with 50% success rate.” | Abstract | b57bb898e37b1c954e6313e83ccac57224bb03365f41060176fa0c8f5af7ba99 (446,560 bytes) |
| S014 | https://metr.org/time-horizons/ | 2026-10-19 | “The task-completion time horizon is the task duration (measured by human expert completion time)” | Time Horizon 1.1 (Current) | c5135c54ec56954655010d57fe17ad3b121c8b289c013821fa15be30228627ba (682,272 bytes) |
| S015 | https://arxiv.org/html/2411.00640 | 2026-10-19 | “we therefore recommend using the paired version of the standard error estimate wherever practicable.” | §4.2 Paired analysis | a621e31708bc1acc5be9d683c8a6a88e11a1d78a43ef124efdf755be99cfd71e (230,425 bytes) |
| S016 | https://arxiv.org/html/2410.03492 | 2026-10-19 | “setting temperature to 0.0 with a fixed seed appears to reduce answer variability for many models” | §6 Conclusions | 1f9131c89f20cb9ed6e7a7d851c63dd4e1f092727a91c3705ba42ce7c5662189 (111,055 bytes) |
| S017 | https://aclanthology.org/2025.ijcnlp-long.125/ | 2026-10-19 | “accounting for both of them is necessary to avoid substantially underestimating the overall variability over hypothetical replications.” | Abstract | f025410d543454f08c187e973a60bf21607af3dbbf5134897af6a4f220024196 (44,758 bytes) |
| S018 | https://arxiv.org/html/2605.30315 | 2026-10-19 | “report a per-pair resolution ratio q=N/N⋆ as the primary diagnostic.” | Abstract | abc005960183d7239bce259347bfe1c6ce21d3e3c0efc76ae8a9484b211fa07a (599,163 bytes) |
| S019 | https://arxiv.org/html/2601.20251 | 2026-10-19 | “under a fixed query budget, seek tight confidence intervals (CIs) for model accuracy with valid frequentist coverage.” | Abstract | 6185caf63aaef1d3abda79a9d591bbbab03281a28e6f1be7b42f3c1f9f970cba (589,568 bytes) |
| S020 | https://arxiv.org/abs/2601.11868 | 2026-10-19 | “we present Terminal-Bench 2.0: a carefully curated hard benchmark composed of 89 tasks in computer terminal environments” | Abstract | 48056dd2c223c4510d39bd6d06fd8079f7c8e7575276c30430e0186483623d36 (53,747 bytes) |
| S021 | https://arxiv.org/abs/2510.25726v2 | 2026-10-19 | “Toolathlon spans 32 software applications and 604 tools.” | Abstract | e8b0b348a7590dda0e4a83675b87f9e80f1fb924634aee899eb36973b1de0d07 (47,041 bytes) |
| S022 | https://arxiv.org/abs/2406.19314 | 2026-10-19 | “contains frequently-updated questions from recent information sources” | Abstract | 89e8779cdc51e654d867d403eb39bb154fb04fb1e794d07c7b1ab518dceda456 (45,596 bytes) |
| S023 | https://scale.com/blog/swe-bench-pro | 2026-10-19 | “We use code that models haven't been trained on.” | A Benchmark to Meet Today’s Coding Needs → Data Contamination, The Solution | ee510e84ea4f2afea0d6ac38517ba9b184181d490f4560a5522d6d41292f756b (128,773 bytes) |
| S024 | grader.py | 2026-10-19 | `"""kengaku hermetic evidence-replay grader — the operability gate (round 10;` / `def main(argv=None):` | grader.py:2; grader.py:5664 | 90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f |
| S025 | corpus/evidence/attrib-r23-stream.log | 2026-10-19 | “STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL” | corpus/evidence/attrib-r23-stream.log:239 | afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131 |
| S026 | https://scale.com/blog/swe-bench-pro | 2026-10-19 | “We use code that models haven't been trained on. This is sourced from public codebases governed by strong copyleft licenses (e.g., GPL)” | Data Contamination → The Solution | 171087c52dae062de9bca611a5b1e73bde45348a24ed9dd813db9a0ccf86783b (128,773 bytes) |

## Census

### Rows
Command: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`

```text
25
```

### Malformed rows
Command: `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md`

```text
0
```

### Tier histogram
Command: `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md`

```text
A=24 C=1 
```

### Status histogram
Command: `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md`

```text
mined=18 queued=5 rejected=2 
```

### Duplicate IDs
Command: `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d`

```text
```

### Enum violations and tier inflation
Command: `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md`

```text
```

### Mined rows with missing used-by paths (final re-run at 2026-10-19T19:07:28-03:00)
Command: `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done`

```text
missing: corpus/knowledge/agent-time-horizon-and-task-validity.md
missing: corpus/knowledge/agent-time-horizon-and-task-validity.md
missing: corpus/knowledge/agent-time-horizon-and-task-validity.md
missing: corpus/knowledge/agent-time-horizon-and-task-validity.md
missing: corpus/knowledge/paired-eval-uncertainty-reporting.md
missing: corpus/knowledge/paired-eval-uncertainty-reporting.md
missing: corpus/knowledge/paired-eval-uncertainty-reporting.md
missing: corpus/knowledge/paired-eval-uncertainty-reporting.md
missing: corpus/knowledge/paired-eval-uncertainty-reporting.md
```

### Final census re-run at round-24 close (2026-10-19T19:22:20-03:00) — supersedes the block above

The block above ran while two peer entries were still being written; this re-run on the final tree is the receipt of record. Commands: the six contract census commands above, verbatim.

```
rows: 25
malformed: 0
tiers: A=24 C=1 
statuses: mined=18 queued=5 rejected=2 
duplicate ids (must be empty): []
enum/tier-inflation (must be empty): []
mined used-by missing (must be empty): []
```

## Access-time capture caveat (appended round 25, 2026-10-20)

The sha256 values above are captures of the bytes fetched at access time. For S005, S006, S023 and S026 the
pages are dynamic or challenge-served: same-day re-fetches return the same byte count but a different hash
(round-25 reviewer RevF10 re-fetched S005 twice 2 s apart: `e6f58c18…` then `1da6fa12…`; S006 `faec654e…`;
scale.com `c7e50638…`). Re-verification of these rows is by quote and location; a hash mismatch alone is not a
finding. (Closes kaika W3 F10.)
- (appended round 25 falsify, CorrF10) The caveat above is not limited to the four named rows: on 2026-10-20 ten of
  24 web rows re-hashed differently — also S004, S008, S020, S021, S022 (arXiv abstract pages grew 586–588 bytes, a
  site template change) and S014 (metr.org). S005/S006 hashes are of a Cloudflare challenge page, not article text.
  Every sha256 in this file is an access-time capture; re-verification is by quote and location for all rows.
