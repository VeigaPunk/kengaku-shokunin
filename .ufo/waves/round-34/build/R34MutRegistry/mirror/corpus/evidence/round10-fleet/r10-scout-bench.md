# r10 scout — bench-arena surface vs corpus claims (freshness re-verification)

Agent: ScoutBench · 2026-09-28 · read-only against `~/bench-arena` and the kengaku repo.
Scripts: `/tmp/kengaku-r10/{fn.sh,driver.sh,snap-jvb.txt,snap-llama.txt}`.

## 1. Surface inventory

```
$ ls ~/bench-arena/
generate_new_domains.py  grade.sh  graded/  loop.sh  out/  report-grok45.csv
report-qwenlocal-v2.v2.csv  report-qwenlocal.csv  staging/  tasks/  telemetry-qwenlocal-v2.csv

$ ls ~/bench-arena/tasks | wc -l
33

$ md5sum ~/bench-arena/grade.sh ~/bench-arena/loop.sh
a15b02f52d4459d0d198bf70b333d357  /home/vgpnk/bench-arena/grade.sh
44427e241574ba23a712faae661484f3  /home/vgpnk/bench-arena/loop.sh

$ md5sum report-qwenlocal.csv report-grok45.csv report-qwenlocal-v2.v2.csv telemetry-qwenlocal-v2.csv
57aab8982dcfc18c9d4b29b61acc380e  report-qwenlocal.csv
e0a42a2f1ab649f4430ebc5b2e380959  report-grok45.csv
c3bd7efe22630dcc6c47e8fa26f66235  report-qwenlocal-v2.v2.csv
dac11874502f7f3f05fb725035294d4e  telemetry-qwenlocal-v2.csv
```

- Report CSVs present: 3 (`report-qwenlocal.csv` v1, `report-grok45.csv`, `report-qwenlocal-v2.v2.csv`) + 1 telemetry CSV.
- `graded/` and `out/` each hold 3 labels (`grok45`, `qwenlocal`, `qwenlocal-v2`); `staging/` = 90 entries.
- `~/bench-arena` is **not** a git repo (`git status` → "not a git repository"); no VCS pinning available.
- All 33 task dirs `01-reverse-words` … `33-metaclass-shadowing`.

## 2. Claim re-derivations

### Claim A — fresh-run doc: "4/33 tasks" slice, v2 column, r4 observed column, aggregate
Source: `corpus/knowledge/bench-arena-fresh-run.md` §Run record.

```
$ awk -F, 'NR>1{print $2}' ~/bench-arena/report-qwenlocal-v2.v2.csv | sort | uniq -c
     12 FAIL
     21 PASS            # 21+12 = 33 rows  -> "4/33 tasks" CONFIRMED

$ grep -E '^(01-reverse-words|02-parse-log-line|03-extract-isodatetimes|05-semver-regex)' \
      ~/bench-arena/report-qwenlocal-v2.v2.csv
01-reverse-words,PASS,0,96052752,1,5e07646e...
02-parse-log-line,FAIL,1,24363497,1,b290f2d0...
03-extract-isodatetimes,PASS,0,135787572,1,d54bfc23...
05-semver-regex,FAIL,1,83101464,1,ddfc61d6...     # doc's "v2 (Aug 29)" column: PASS/FAIL/PASS/FAIL  -> exact

$ cat /tmp/bench-r4/report-kq-r4.v2.csv
01-reverse-words,PASS,0,163961848,1,21ccd534...
02-parse-log-line,FAIL,1,17771079,1,f9332e6e...
03-extract-isodatetimes,FAIL,1,27554895,1,c3843520...
05-semver-regex,FAIL,1,76634865,1,006cc505...     # doc's round-4 column: PASS/FAIL/FAIL/FAIL -> exact

$ cat /tmp/bench-r4/predictions.md
... 01=PASS 02=FAIL 03=PASS 05=FAIL ... Predicted aggregate: 2/4 PASS
# observed aggregate 1/4 -> doc's "Aggregate 1/4 vs predicted 2/4" -> exact
```
**Verdict: REPRODUCES.** Task count 33, the v2 verdict column, the round-4 verdict column, the 1/4-vs-2/4 aggregate, and the `/tmp/bench-r4` artifact set (still on disk, 16:00–16:01) all match verbatim. The 4 task symlinks under `/tmp/bench-r4/tasks/` still point into `~/bench-arena/tasks/`.

### Claim B — round7 errata: "`0/12` → `0/17` PASSes", discordance 0/25
Source: `corpus/knowledge/bench-arena-round7-noise-n25.md` errata block; provenance cited as `/tmp/bench-r7-l2-executor/` ("ephemeral").

The cited directory **still exists** (contra the doc's "ephemeral" parenthetical): `REPORT.md`, `matrix.md`, `summary.json`, `graded/` (125 label dirs), `out/` (125), 128 `.sol` files, mtime max `2026-09-28 17:12`.

```
$ awk '/^## 09-/,/^## 20-/' matrix.md | awk -F'|' '/^\| [0-9]+ /{gsub(/ /,"",$4); print $4}' | sort | uniq -c
      8 FAIL
     17 PASS                                   # doc :15 table "17/25" -> exact

$ window fractions (corrected field indexes) -> A 5/5, B 6/10, C 1/5, D 5/5
$ distinct sol_sha (col 9) -> 13               # doc ":15" 5/5, 6/10, 1/5, 5/5, 13 -> exact

$ for i in $(seq 1 25); do f=graded/n09-rep$i/09-sql-top-n-per-group.sol; \
    grep -qP 'WHERE[^;]*(DENSE_RANK|RANK)\s*\(\s*\)\s*OVER' "$f" && echo MATCH || echo NOMATCH; done | sort | uniq -c
# cross-tab against matrix status:
      8 FAIL MATCH
     17 PASS NOMATCH                           # 8/8 FAILs matched, 0/17 PASSes matched -> discordance 0/25
```
**Verdict: REPRODUCES (0/17 is the correct denominator).** The original `0/12` was internally inconsistent (8 FAIL + 12 PASS = 20 ≠ 25); the n=20 prefix of the same matrix has exactly 12 PASS / 8 FAIL, which explains the stale figure. The n=25 matrix gives 17 PASS / 8 FAIL → `0/17`, discordance 0/25 unchanged — exactly as the errata states.

Adjunct findings (non-load-bearing, but they touch the errata's provenance):
- The errata's own source artifact is still uncorrected: `/tmp/bench-r7-l2-executor/REPORT.md:38` reads `8/8 FAILs and 0/12 PASSes — **discordance 0/25**` while `:24` and `:147` say `17/25`. The errata is right; the source REPORT.md remains internally inconsistent.
- Doc line 8 claims "97 label dirs"; on disk there are **125** label dirs (`ls /tmp/bench-r7-l2-executor/graded | wc -l` = 125, `out` = 125; 50 of them are the `n09-rep1..25`/`n20-rep1..25` headline set). Stale count, minor.
- Task 20 side of the same table also reproduces: `8 PASS / 17 FAIL`, windows `A 4/5, B 1/10, C 3/5, D 0/5`, distinct sol_sha `22` — all exact vs the doc's `:16` row.

### Claim C — fresh-run doc, "Harness facts (verified live)": 8080/34113 drift and the telemetry-NULL origin
Source: `corpus/knowledge/bench-arena-fresh-run.md` §Harness facts.

Port facts — **REPRODUCE**:
```
$ grep -n 'LLAMA_METRICS_URL\|journalctl\|available=n' ~/bench-arena/loop.sh
5:METRICS_URL=${LLAMA_METRICS_URL:-http://127.0.0.1:8080/metrics}
38:  journalctl --user -u qwen-coder.service --since "@$start_s" ... 
61:  sha=$(...); source=metrics; available=n

$ grep -n -A4 '"qwen-local"' ~/.config/opencode/opencode.json
158:        "baseURL": "http://localhost:8080/v1"          # doc's drift claim -> exact

$ curl -s -m3 -o /dev/null -w 'code=%{http_code} bytes=%{size_download} ct=%{content_type}\n' http://127.0.0.1:8080/metrics
code=200 bytes=27461 ct=application/openmetrics-text;charset=utf-8;version=1.0.0
$ curl -s -m3 http://127.0.0.1:8080/metrics | head -2
# TYPE jitsi_jvb_bytes_sent counter
# HELP jitsi_jvb_bytes_sent The total number of bytes sent in RTP packets.
#  + /about/health -> 200 ; jvb/jicofo processes present (s6-supervise jvb, org.jitsi.videobridge.MainKt)
#  => "8080 is occupied by Jitsi" -> CONFIRMED, with the occupant identified as jitsi-videobridge metrics

$ curl -s -m3 http://127.0.0.1:34113/health ; curl -s -m3 http://127.0.0.1:34113/v1/models
{"status":"ok"}
{"models":[{"name":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf" ...
$ tr '\0' ' ' < /proc/1299/cmdline | tr ' ' '\n' | grep -E 'port|metrics|parallel|kv-unified|cont-batching'
--metrics --port 34113 --cont-batching --kv-unified --parallel 2
#  => live server = llama-server pid 1299 on 34113, exactly as claimed (also confirms the r7 --kv-unified/--parallel 2
#     mechanism suspects are still the running config)
```

The stated *causal chain* — "the harness's metrics fallback therefore degrades silently — likely origin of the `telemetry_available=n`/`NULL` rows in v2" — **DRIFTS**:
```
$ grep -n 'int(oka and okb)' ~/bench-arena/loop.sh
32:print(f'{...},{...},{...},{...},{int(oka and okb)}')          # producer: 5 comma fields
$ grep -n 'read -r pt et pms em tps mok' ~/bench-arena/loop.sh
63:  IFS=, read -r pt et pms em tps mok <<< "$m"                 # consumer: 6 variables
64:  if [[ $mok == 1 ]]; then :; else source=journal; ... fi

$ bash -c 'IFS=, read -r pt et pms em tps mok <<< "0,0,0.000,0.000,1"; echo "tps=[$tps] mok=[$mok]"; \
           [[ "$mok" == 1 ]] && echo BRANCH=metrics || echo BRANCH=journal'
tps=[1] mok=[]
BRANCH=journal                                                   # 5 fields into 6 vars -> mok ALWAYS empty
$ control with 6 fields -> BRANCH=metrics

$ bash /tmp/kengaku-r10/driver.sh          # loop.sh's metric_snapshot+metric_delta extracted verbatim, run vs live 8080
metric_delta output (pt,et,pms,em,mok) = 0,0,0.000,0.000,1
=> would record: source=journal available=JOURNAL_PATH tps=1
```
Consequences, all observed:
1. The journal fallback is **unconditional** in the on-disk `loop.sh` — `mok` can never equal `1`, whatever `METRICS_URL` points at. v2's `telemetry_source=journal` for **33/33** rows (`awk -F, 'NR>1{print $11}' telemetry-qwenlocal-v2.csv | sort | uniq -c` → `33 journal`) is explained by this field-count bug, **not** by the 8080/34113 mismatch. The port mismatch is real but not the cause of those rows.
2. The premise "the metrics scrape fails" is false today: `curl -fsS --max-time 2 http://127.0.0.1:8080/metrics` exits **0** (HTTP 200, jvb openmetrics). And `grep -icE 'prompt|eval'` over that body = **0**, so a corrected reader pointed at 8080 would silently log zeros rather than fall back.
3. NULL detail: exactly **1** row carries `telemetry_available=n` (`20-csv-group-sum`, `telemetry_source=journal`, `predicted_tokens=NULL`), with 4 NULL cells (`prompt_tokens,predicted_tokens,inference_latency_ms,tokens_per_sec`); 32/33 rows are `y`. The doc's phrase "rows" (plural) and the attribution to the port drift are both imprecise.

**Verdict: DRIFTED** (port facts reproduce; the causal attribution and the "scrape fails" premise do not).

## 3. Drift since round 9 (mtime > 2026-09-28 18:00)

```
$ find ~/bench-arena /tmp/bench-* -newermt '2026-09-28 18:00' -printf '%TY-%Tm-%Td %TH:%TM %p\n'
(no output)                       # ZERO files
```
- `~/bench-arena` is frozen at **2026-08-29 03:06–03:58** (newest: the directory itself 03:58; CSVs 03:06/03:15/03:30). No modification in 30 days, let alone since round 9.
- `/tmp/bench-r4 … r8`, `/tmp/bench-r7-l2-{executor,labrat,rev,wikisweeper}`: nothing newer than 18:00; newest overall `/tmp/bench-r7-l2-executor/REPORT.md` 17:12. The round-4 and round-7 provenance trees that the corpus cites are **still intact and re-derivable**.
- Corpus repo (context, not owned by this lane): normal round-9/10 authoring after 18:00 — `corpus/evidence/round8-horizon/{results.jsonl,run.log}` 18:08, `round9-fleet/*` 18:19–18:26, `round9-replication/ordering.log` 18:26, `knowledge/bench-arena-round7-noise-n25.md` 18:49 (the errata append). `knowledge/bench-arena-fresh-run.md` untouched since 16:03.
- Runtime drift that matters more than mtimes: port 8080 now answers `/metrics` with HTTP 200 jvb openmetrics (the doc's mechanism assumed a failed scrape). This is invisible to the harness only because of the `mok` bug above.

## Unknowns / gaps
- Whether 8080 served jvb metrics (and thus "succeeded") on 2026-08-29 is unobservable now; the v2 telemetry's `source=journal` is fully explained by the `read` bug either way, so the question does not affect Claim C's verdict.
- `ss -ltnp` cannot show the 8080 owner (foreign user / no root); the Jitsi attribution rests on the metric names (`jitsi_jvb_*`), `/about/health` 200, and live jvb/jicofo processes.
- No VCS in `~/bench-arena` → content-addressing is by md5 only (recorded above); any future mutation will not self-announce.
