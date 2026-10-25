# E0–E8 extraction cost / safety findings

Scope: read-only sentinel measurement against the round-27 C1 semantics (`plans/round-27-claims.md:33-48`). No lane source was edited; scratch implementations and runners live only in `/tmp/sentregex-r27/`.

## Evidence

- Reference behavior: `grader.py:121-134` uses the fenced regex, then `BARE_RE` at line 128, and catches `Exception` around JSON loads. The BARE_RE bytes match `plans/grader_perturb.py:36`.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/sentregex-r27/bench_pop.py` → exit 0; `population n=1964 max_len=361 sum_len=159734`; loader reported zero errors and verified the four pins. E0 extraction matched `grader.extract_json_block` on **1964/1964**.
- Population extraction total (best of 3 timed passes; slowest individual record in ms):

  | Policy | Total s | Max record ms |
  |---|---:|---:|
  | E0 | 0.0028 | 0.0044 |
  | E1 | 0.0027 | 0.1242 |
  | E2 | 0.0027 | 0.0033 |
  | E3 | 0.0025 | 0.0038 |
  | E4 | 0.0022 | 0.0032 |
  | E5 | 0.0025 | 0.0044 |
  | E6 | 0.0027 | 0.0040 |
  | E7 | 0.0013 | 0.0036 |
  | E8 | 0.0016 | 0.0045 |

- `PYTHONDONTWRITEBYTECODE=1 timeout 3300 python3 /tmp/sentregex-r27/orchestrate.py /tmp/sentregex-r27/results.jsonl 8` → exit 0, `jobs=357`, `done`; JSONL has 357 rows, zero timeout-kills.
- 200 KB worst observed per policy across the adversarial matrix (seconds; input noted):

  | Policy | Worst s | Input |
  |---|---:|---|
  | E0 | 0.0698 | BARE_RE interleaved-brace chain |
  | E1 | 0.0703 | BARE_RE interleaved-brace chain |
  | E2 | 0.0702 | BARE_RE interleaved-brace chain |
  | E3 | 0.0714 | BARE_RE interleaved-brace chain |
  | E4 | 0.0033 | deeply nested-object text |
  | E5 | 0.0003 | 200 KB fence/whitespace nonmatch |
  | E6 | 0.0717 | BARE_RE interleaved-brace chain |
  | E7 | 284.2526 | `[` × 200,000 |
  | E8 | 285.0320 | `[` × 200,000 |

- Regex-focused probes (`re.finditer`, 200 KB): BARE_RE on `"{" + "{b}c"*49999 + "x"` (199,998 chars; 49,999 matches) took 0.0087 s; on unmatched `"{a"*100000 + "x"` took 0.0039 s. E6 fence regex took 0.0007 s on an unclosed 200 KB labeled fence and 0.0010 s on 200 KB spaces after backticks. No catastrophic regex backtracking observed in these targeted shapes.
- Raw-decode brace scan: E7/E8 on `{` × 200,000 took 3.0517 / 3.0496 s. On nested open arrays, E7/E8 took 8.4373 / 8.5082 s at 25K, 38.7212 / 38.8658 s at 50K, and 284.2526 / 285.0320 s at 200K. Thus **50K and 200K array inputs exceeded 10 s**. `[` × 4,096 took 0.1852 / 0.1837 s; `[` × 1,024 took 0.0124 / 0.0120 s. Python 3.14.8, recursion limit 1000; raw `raw_decode` on a 100K opener run raised `RecursionError: Stack overflow (used 8144 kB)`. E7/E8 implementations catch that exception and continue, repeating the deep parse at each opener.
- A scratch depth-32 pre-scan prototype matched E7/E8 extraction values on all 1964 population records and reduced the 200K array case to 0.7868 / 0.7756 s. This is only exploratory evidence: a depth cap changes policy behavior for valid JSON deeper than 32 and is not a semantics-preserving general fix.

## Finding

**Severity: High (CPU resource exhaustion in an untrusted-input run).** Exploit path: supply a long raw answer consisting of unmatched nested open brackets to E7/E8; each start position invokes `raw_decode` on almost the full remaining suffix and recurses until failure. One 200 KB answer consumes about 4m45s of wall time (CPU-bound); growth is superlinear. This is a local evaluation/instrument availability risk, not a finding against the frozen 1964 responses (max 361 chars; all population passes were milliseconds total).

**Smallest remediation:** when E7/E8 process untrusted or non-frozen records, enforce an explicit raw-response size / aggregate decode-work budget before scanning, and report budget exhaustion as a distinct bounded extraction failure. A 4 KiB input cap is consistent with the measured 0.19 s worst probe and is well above the frozen population maximum, but it intentionally changes behavior for longer responses; keep uncapped semantics only where the input is trusted and already bounded. Ensure `RecursionError` is caught (a `ValueError`-only handler leaked it in the scratch defect probe).

VERDICT: E0–E6 showed no >10 s behavior in the tested 200 KB regex/policy probes; E7/E8 have a confirmed quadratic/deep-recursion CPU blow-up above 10 s on 50K+ unmatched nested arrays. Recommend an explicit bound only for untrusted/large inputs. Installs: none.
