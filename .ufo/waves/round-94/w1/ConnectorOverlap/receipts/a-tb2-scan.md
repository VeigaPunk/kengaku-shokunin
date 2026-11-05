# Receipt (a) — TB2 / write-compressor / TB2-bytes scan, 2026-11-05

Tool: grep (ripgrep-backed), gitignore respected. **Caveat (measured): the glob path form `…/*-shokunin` silently
returns zero results; explicit `;`-joined lane paths were used for every query below.**

Sibling lane HEADs at scan time (git rev-parse --short=12):
audio f9da7ee97e0b, chousa 378fda82dc2c, game-dev-2d 1e033ef053be, game-dev-3d 39ca3973c786, kagi f5977284a8ce,
kaidoku c19d57cd2e65, kake 7838981e4e40, kama 9b4c7af16fdd, kasegi d16d2124fd52, kotoba 372195d32e3f,
kotodama 16c4759241cb, kumitate 1325caf47a25, lore 0f044aa7c7e4, mado 24ba2a9ddac2, mori 5013f0be8ac9,
revenger 9ddd38ac8bae, souji e063a2fcb3f5, tabi 58d84eda992f, tameshi f256302b394a, tsukuroi 64f45b790f2d.
kengaku master d04e6664c4fc (T 90c7677f judged via detached shared clone).

## Query 1 — `(?i)(terminal.?bench|write.?compressor)` over the glob path form
Result: **No matches found** — FALSE NEGATIVE (kengaku plans/round-94-claims.md contains both strings; re-proven by
query 2 scoped to kengaku). Filed to harness issue channel.

## Query 2 — `write-compressor` scoped to kengaku-shokunin/plans (control proving the tool works)
Hits (excerpt):
- plans/round-94-claims.md:39 `write-compressor` @ `2fd12b88` …; :48 `TARGET executed_rows=38 member=write-compressor …`
- plans/round94_c1_replay.py:2,41,56 (CAPDIR/MEMBER)
- plans/round94_compressor_probe.py:2,44,47,48
- plans/round94-cases.json:2 `"member": "write-compressor"`
- plans/grader-population-ledger.json:917 `"write-compressor": {`
- plans/round52-tasks.json:535-539,901-903

## Query 3 — `(?i)(terminal.?bench|write.?compressor)` over 21 sibling lanes + fleet scripts/ (explicit paths)
All sibling hits are wave-history echoes of kengaku bytes (no tracked corpus/grader/capture):
- chousa `.ufo/waves/round-73/w1/R73S03/.ufo__l0-questions.md.txt:206` — kengaku r52 L0 question quoting the TB2
  push-protection incident (`corpus/evidence/round52/graders/sanitize-git-repo/tests/test_outputs.py:12`).
- kagi `.ufo/waves/round-30/w1/ConnOverlap-report.md:64,228`, `round-33/build-results.json:58,73,114-115`,
  `round-37/build/K37ConnFeeds.md:107` — "Terminal-Bench grader surface … kengaku"; "kengaku = Terminal-Bench …
  term overlap only"; classified NO CLAIM / already disambiguated.
- kaidoku `.ufo/waves/round-41/w2/artifacts/R41W2Reservation/tx-scan.json:19601,19614` — embeds KengakuR41 driver text
  (PIN 2fd12b88, constraints-scheduling capture); `round-69/w1/ConnectorCross/sweep/s4-receipt.txt:185-212` — sweep
  quoting kengaku SKILL.md registry rows.
- kake `.ufo/waves/round-71/w1-results.json:64`, `round-71/w1/ConnOverlap.md:29-32` — S129–S132 homonym survey:
  "kengaku = Terminal-Bench"; `round-92/w1/ConnectorScope/receipts/query-422.txt:74`, `query-stale.txt:234`.
- kumitate `.ufo/waves/round-63/build/K63RevengerDispatcher/forgery-borrowed/.ufo/waves/round-35/build-dispatch.json:370-471`
  — kengaku r35 dispatch copied as forgery fixture.
- kasegi `.ufo/waves/round-58/w1/SiblingOverlap.md:271`, `round-60/w1/SiblingOverlap.md:39` — quotes kengaku PROVINCE.md
  benchmark-audit frontier.
- (souji/kotoba/etc. no direct hits beyond the ones above.)

## Query 4 — `harbor-framework|2fd12b88` over 21 sibling lanes + fleet scripts/ (tracked + history)
No sibling-tracked TB2 URL or pin. Sibling hits, all echoes:
- kaidoku tx-scan.json:19601,19614 (as above); kaidoku r69 s4-receipt.txt:196 (quotes kengaku SKILL round52-c1 row with
  population `plans/round52-tasks.json`, pin, 184 captures — kengaku's own capture, quoted); kake r92/r93 receipts
  (query-422.txt:74 — S126 circuit-fibsqrt row; query-stale.txt:234 — S241 nginx-request-logging row; sibling-scan.txt:22
  — feal-linear-cryptanalysis 304 recheck); kumitate forgery-borrowed build-dispatch.json (kengaku r35 URLs);
  tabi `.ufo/waves/round-62/w1/R62Exec1/context-6.stdout:255-980` — transcription of kengaku PROVINCE round history
  (protein-assembly, regex-log, git-webserver, build-pmars, git-leak-recovery, db-wal-recovery, constraints-scheduling,
  circuit-fibsqrt, feal, password-recovery, polyglot-c-py, chess-best-move, largest-eigenval, distribution-search,
  openssl-selfsigned-cert, cancel-async-tasks, kv-store-grpc) — kengaku's own registry text; kengaku r90
  ConnectorOverlap receipts; kaidoku r87 ConnectorR87/links.md:56 (kengaku pin-tree path cited for a "packer" name).
- Tracked sibling mention of the benchmark name: kumitate `corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83`
  (S197 paper capture; "Terminal-Bench (2 tools) …" — benchmark evaluation rows in a paper, zero task bytes).
- souji `census/round-31/waves/w2/SwarmConnector28.md:21` (tracked) — routes kengaku's TB2 git-leak ground to kengaku.

## Query 5 — `(?i)(write.?compressor|data\.comp)` over 21 sibling lanes + fleet scripts/ **tracked only** (`;!**/.ufo/**`)
Only false positives: game-dev-3d `corpus/fixtures/r94vendor/three.core.js:29685,49752` (+ 30 vendored copies under
`reports/round-104/…`) — `data.compareFunction` matching the `data\.comp` prefix. **No sibling tracks write-compressor
bytes or a data.comp artifact.**

## Query 6 — bonus, non-lane fleet dirs (counters, reports, research, st2, wt2, exp-full, history-recheck, tools,
templates, kumitate-shokinin), `(?i)(terminal.?bench|harbor-framework|write.?compressor|counter_not_frozen|frozen.?instrument)`
Result: **No matches found.**

Conclusion (a): no sibling replays TB2 graders (write-compressor or any compression/codec task) and none captures TB2
task bytes; kengaku's ownership is re-affirmed by three prior connector rounds (kagi r30, souji r31, kake r71).
