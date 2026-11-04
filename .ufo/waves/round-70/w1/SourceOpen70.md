# SourceOpen70 — live source reopen for R70-C1 / R70-C2

Lane tip at seat time: `384e9c76` (`round-70 freeze: claims, instruments, wave spec+dispatch,
census-before, controls`); frozen base `502893ad` is its parent (`git merge-base --is-ancestor
502893ad master` → ANCESTOR yes). Read-only seat: nothing in L was edited; captures copied to
`.ufo/waves/round-70/w1/SourceOpen70/`. Scratch `S=/fast/scratch/hyaku/kengaku-r70/SourceOpen70`.

## What I ran

| # | command | rc |
|---|---|---|
| 1 | `curl -sS -o instruction.md -w 'HTTP:%{http_code} BYTES:%{size_download}'` on the S242 URL at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` | 0 |
| 2 | `sha256sum instruction.md; wc -l instruction.md` | 0 |
| 3 | `curl -sS -D headers-instruction.txt …` (HEAD-equivalent, headers captured) | 0 |
| 4 | `curl -sS -o test_outputs.py` on the S241/S243 URL at the same pin; `sha256sum`; `wc -l` | 0 |
| 5 | `grep -nE '^\|?[[:space:]]*S24[0-9]' corpus/SOURCES.md` + `awk 'NR==257\|\|NR==258\|\|NR==259' … \| fold -w 200` (unwrapped cells) | 0 |
| 6 | `grep -Ec 'benchmark-error\|sites-enabled\|burst\|10m\|limit_req[^_]' test_outputs.py` (per pattern) | 0 (counts 0) |
| 7 | `grep -n '^def test_' test_outputs.py` | 0 |
| 8 | `python3` byte-compare of grader `expected_content` literals vs instruction `:16`/`:18` after `.strip()` | 0 (True, True) |
| 9 | `sed -n '1,3p' <refused entry>`; `grep -n '^recheck:'`; `grep -o 'S[0-9]\{3\}'` | 0 |
| 10 | `sha256sum corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`; `sed -n '111p' …/SHA256SUMS`; `cmp -s` vs fetched pin | 0 / cmp: BYTE-IDENTICAL |
| 11 | `grep -c 'executed 2 of 8' SKILL.md`; `grep -c 'executed 3 of 8' SKILL.md` | 0 / rc 1 (1 / 0) |

## 1. Fetch at the pin — reproduces exactly

```
HTTP/2 200
etag: "dd01996c7a323342bf97b00edb3a3467abe752f46dd506fe20d0910f4f49aae6"
content-length: 1882
26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99  instruction.md
24 instruction.md
```

Digest `26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99`, 1882 bytes,
24 lines: byte-for-byte the values S242 and R70-C2 E3 record. Grader at the same pin:
`045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0`, 5947 bytes, 178 lines, and
`cmp` says it is **byte-identical** to `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`,
which `SHA256SUMS:111` records as the same digest.

## 2. Exact lines for the three clauses the round depends on

```
9:  - Set up rate limiting to allow only 10 requests per second per IP address with a burst capacity of 10 requests using a 10MB memory zone.
10:  - Add the rate limiting zone definition (`limit_req_zone`) to `/etc/nginx/nginx.conf` and apply the rate limiting (`limit_req`) in the server block.
16:   "Welcome to the benchmark webserver"
18:   "Page not found - Please check your URL"
```

- index body literal — `instruction.md:16`: `"Welcome to the benchmark webserver"` (5 words).
- 404 body literal — `instruction.md:18`: `"Page not found - Please check your URL"`.
- rate-limit clause — `instruction.md:9` (rate/burst/zone sizes) and `:10` (`limit_req_zone` zone
  definition in `nginx.conf` *and* `limit_req` applied in the server block).

**Anchor coverage of `instruction.md:6-11,15-18` — holds.** `15-18` contains :15 (create index.html),
:16 (index body), :17 (create 404.html), :18 (404 body); `6-11` contains :9 and :10. All three
load-bearing clauses fall inside the anchor; nothing in the anchor is outside the task's server-config
and body clauses.

**Byte-equality with what the grader asserts** (grader `:39`, `:52`):
`expected_content = "Welcome to the benchmark webserver"` and
`expected_content = "Page not found - Please check your URL"` — equal to the stripped instruction
lines :16/:18 (`True`, `True`). The literal at `:16` and `:18` is the only occurrence in the file.

## 3. S242 and S243 cells verified against the fetched bytes

| field | S242 (instruction) | S243 (grader leg mapping) |
|---|---|---|
| URL | exact match to the URL I curled | exact match to the URL I curled |
| pin | `2fd12b88` — present in both URLs | `2fd12b88` — present |
| sha256 | `26a7ac98…9edf99` — **re-derived** | `045cc716…4acda0` — **re-derived** |
| quote ≤25 words | `:16 verbatim: "Welcome to the benchmark webserver"` (5 words) | `result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)` (6 words) |
| quote verbatim | yes, `:16` | yes, but at **`:61`**, not the cited `:59` — see F1 |
| used-by exists | `corpus/knowledge/tb2-nginx-request-logging-offline.md` — exists, 5483 B | same path — exists |
| status/ttl/tier | `mined` / `180d` / A | `mined` / `180d` / A |

Registry cardinality: exactly one row each for `S241`, `S242`, `S243`, `S244`
(`grep -cE '^\|[[:space:]]*S24n[[:space:]]*\|'` → 1/1/1/1).

S242's load-bearing claim — *"states four clauses the grader never checks (error-log path,
default-site removal, limit_req application, burst/zone sizes)"* — **verified by absence**:
`grep -Ec` on the grader returns `benchmark-error 0`, `sites-enabled 0`, `burst 0`, `10m 0`,
`limit_req[^_] 0` (the only `limit_req` token is `limit_req_zone` at `:119`). The four clauses do
appear in the instruction at `:8`, `:13`, `:10`, `:9` respectively.

The entry's `source:` line (`corpus/knowledge/tb2-nginx-request-logging-offline.md:1`) names `S242`
and the anchor `instruction.md:6-11,15-18` verbatim (E3's text), though parenthetically: the line
opens `source: S241 (corpus/SOURCES.md) — … — anchor: … , instruction.md:6-11,15-18 (S242) — sha256 …`.
S243's supersedes field opens `supersedes S241 — leg 5 is the nginx -t subprocess, satisfied by a
shim; legs 6-8 read config bytes and a log the server writes, so S241's legs 5-6 file-read summary is
wrong` (E4's text), field 7 of the row.

## 4. The refused package entry (S244) — reject reason holds, on three grounds

`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/grader-fixture-coverage.md`
(2869 B, 39 lines). First three lines, numbered:

```
1  (empty)
2  source: S155 — `lanes/kengaku/round8/toolathlon-grader-fixture-probe2.md` — the probe's result table, its "Not attempted" list and its Counts section — lane own-work artefact, generated 2026-10-24
3  verified-at: 2026-10-24
4  recheck: on-commit — re-run the probe against the pinned commit; …
```

S244's verbatim fragment is `source: S155 — lanes/kengaku/round8/toolathlon-grader-fixture-probe2.md`.

- **The reason's factual core holds.** The transcript exists only at
  `/home/vgpnk/Projects/shokuknow/lanes/kengaku/round8/toolathlon-grader-fixture-probe2.md`
  (113 lines, 7033 B, sha256 `3b9a4902e33f8eafab65cd899a92885d53fe9c41e14061f0c8037c65337642ee`);
  **L has no `lanes/` directory at all** (`ls -d L/lanes` → No such file or directory), and `find`
  over L and the merge package returns no copy. So "bytes are not in this lane" is literal.
- **Q1 fails on the entry's own bytes, independent of the transcript.** `QUALITY.md:15-21` Q1:
  "The first three lines are `source:` …, `verified-at:` … and `recheck:`". The triad is offset by a
  leading blank line, so `recheck:` sits at `:4`, not `:3`.
- **Q2 fails even if the transcript were imported.** Q2 (`QUALITY.md:24-26`) requires tier A/B for the
  claim's scope and says "a tier-C row never stands alone"; S244 registers the entry `own-work | C`.
  Additionally, this lane's `S155` is a *different* source — `S155` at
  `corpus/SOURCES.md:170` is `Terminal-Bench 2.0 password-recovery solution/solve.sh` (code, tier A),
  not the toolathlon transcript, so the cited row id does not resolve to the cited artefact here.

## 5. Cross-checks that make the round's vectors row-ready

- **Frozen leg order equals the grader's definition order**: `test_nginx_installed:11`,
  `test_nginx_running:17`, `test_index_page_content:33`, `test_custom_404_page:46`,
  `test_nginx_config_syntax:59`, `test_nginx_config_settings:67`, `test_log_file_creation:123`,
  `test_log_file_format:144`.
- **Per-leg causal surfaces** (what each frozen vector's `F` prices): leg 1 = `which nginx` (`:13`);
  leg 2 = `requests.get` 8080 with 3 retries (`:19-28`); leg 3 = 200 + index body (`:36-41`);
  leg 4 = `/nonexistent-page` 404 + 404 body (`:48-55`); leg 5 = `nginx -t` subprocess (`:61`);
  leg 6 = config-file reads incl. `re.search(r"limit_req_zone.*?rate=10r/s", …)` (`:119`);
  leg 7 = `requests.get` then `benchmark-access.log` existence (`:127-142`); leg 8 = unique-path
  request then the four log regexes (`:146-178`). K4→leg 6, K7→leg 4, K3→legs 7-8, K5→legs 1+5,
  K6→legs 2,3,4,7,8 are each consistent with those surfaces.
- **K6's five reds and K5's two reds each share one staged cause.** K6 stages "no service", which is
  exactly the input of legs 2,3,4,7,8; K5 stages "no `nginx` on PATH", exactly the input of legs 1 and
  5. Named limitation (iii) records this for K6 only (see F3).
- **C1 before-state is live at the tip**: `grep -c 'executed 2 of 8' SKILL.md` → `1`;
  `grep -c 'executed 3 of 8' SKILL.md` → `0` (rc 1). The after-target is not yet met, as the freeze
  requires.

## 6. Defects found — reported, not edited

- **F1 (calibration, S243 evidence field).** The cell cites `tests/test_outputs.py:59` for
  `result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)`. `:59` is
  `def test_nginx_config_syntax():`; the quoted string is at **`:61`** (`:60` is the docstring). The
  quote itself is verbatim and ≤25 words; only the location is off by two lines. No frozen predicate
  reads S243's line number — E4 reads only "opens `supersedes S241 —`" and "leg 5 is the `nginx -t`
  subprocess" — so this is a row defect, not a predicate risk.
- **F2 (calibration, S244 quote).** S244's "verbatim" drops the backticks around the transcript path;
  the source line reads `` `lanes/kengaku/round8/toolathlon-grader-fixture-probe2.md` ``. Partial quote,
  not verbatim.
- **F3 (calibration, named limitations).** Limitation (iii) says "K6 stages 'no service' as a whole
  candidate state, so its five red legs are not independently isolated". K5 has the same shape: its
  two reds (legs 1 and 5) both trace to the single absent-binary cause. The isolation claim is
  narrower than the table's phrasing implies; the vectors are correct, the limitation list is
  incomplete.
- **F4 (staleness, used-by entry).** `corpus/knowledge/tb2-nginx-request-logging-offline.md:3`
  (`recheck:`) still names `plans/round69_c1_nginx_probe.py` and the **five** frozen vectors. Both
  instruments exist (`round69_c1_nginx_probe.py` 26573 B, `round70_c1_nginx_probe.py` 34657 B), so the
  recheck runs, but it re-derives a table round 70 supersedes. Not in E1–E8; flagged for the lesson.

## Verdict

**Sources reproduce at the pin, and the round's two rows are usable as written.** `instruction.md`
re-derives at HTTP 200 / 1882 B / 24 lines / `26a7ac98…9edf99` and `tests/test_outputs.py` at
5947 B / `045cc716…4acda0` byte-identical to the committed capture and `SHA256SUMS:111`; the anchor
`instruction.md:6-11,15-18` covers the index body (`:16`), the 404 body (`:18`) and the rate-limit
clause (`:9-10`), and both body literals are byte-equal to the grader's `expected_content` strings at
`:39`/`:52`. S242 is clean on every field; **S243 carries one evidence-field location defect (F1:
cites `:59`, string is at `:61`) that no frozen predicate reads**; the S244 reject reason holds, and
two stronger grounds exist inside the entry and this lane's registry (Q1 triad offset by a leading
blank line; `S155` here is the password-recovery row, and a tier-C own-work row cannot stand alone).

## Captures (W/SourceOpen70/)

| file | sha256 |
|---|---|
| `instruction.md` (1882 B) | `26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99` |
| `test_outputs.py` (5947 B) | `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` |
| `headers-instruction.txt` | `e8a7d6e642b81fe54368cfc365a9a6b541e0511aec263613f50e585772c54bc9` |
| `SHA256SUMS-sourceopen70.txt` | `cd4dc979bbb79a85f1dd0219556537f8c0be7745a4c0bb2a336dcf5b69e6cd37` |
| `S155-toolathlon-transcript-copy.md` (7033 B, from shokuknow) | `3b9a4902e33f8eafab65cd899a92885d53fe9c41e14061f0c8037c65337642ee` |

**Tooling:** none installed or upgraded. No subagents dispatched (leaf seat). No git/jj mutation.
