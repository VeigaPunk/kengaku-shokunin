# F40ConnFrontier — frontier consistency check at ec1005a2a28bc5cfdde7723374368ed4cc956eed

Seat: F40ConnFrontier (connector, leaf). Scope: (1) README §Frontier TB2 clause says "6 of 89";
(2) binary-database-pair class recorded consistently in README coverage map, PROVINCE, SKILL;
(3) SHONEN/SCORECARD self-assessment lines mismatch the repo (count, file:line).

Fixture: clean `--no-local` clone at `ec1005a2a28bc5cfdde7723374368ed4cc956eed` under
`/fast/scratch/hyaku/kengaku-r40/F40ConnFrontier/lane` (`git rev-parse HEAD` → `ec1005a2a28bc5cfdde7723374368ed4cc956eed`), removed after the check. No lane files touched.

Note on "README": the root `README.md` is 14 lines (lane intro only; `grep -i frontier` → 0 hits). The
§Frontier section and the coverage map live in `corpus/README.md` (the lane's corpus README); that is what
the round's routed work ("README index/coverage/frontier/evidence lines") landed in, and what prior rounds
(SC r37–r39 rows) call the §Frontier clause.

## 1. §Frontier TB2 clause = "6 of 89" — YES

- `corpus/README.md:337` (§Frontier round-40 sub-bullet): "it stays open for the remaining TB2 task
  graders (6 of 89 read)".
- `corpus/README.md:267` (coverage-map bullet): "A sixth instance of the same ground (6 of the 89 TB2
  task graders…)".
- Progression is monotonic and stale-free; `grep -rn "of 89"` over README/corpus-README/PROVINCE/SKILL/
  SCORECARD/SHONEN/lesson/knowledge returns only round-correct counts: r36 "one more of the 89"
  (corpus/README.md:263), r37 "3 of 89" (:294), r38 "4 of 89" (:307), r39 "5 of 89" (:322), r40
  "6 of 89" (:337). No 7-of-89, no leftover 5-of-89 in any round-40 context.
- Arithmetic: PROVINCE.md:445 "remaining 83 TB2 task graders (89 carry `tests/test.sh`; 6 are read)"
  → 89−6=83 ✓. Denominator 89 cross-checks with corpus/README.md:262 (r35 bullet) "Not the other 88
  TB2 tasks" → 88+1=89 ✓.
- Knowledge entry agrees: `corpus/knowledge/tb2-db-wal-recovery-grader.md:44` "(6 of 89 read at
  `2fd12b88`)".
- SCORECARD row agrees: `SCORECARD.md:1461` "one §Frontier TB2 sub-bullet narrowed by one task (6 of 89)".

## 2. binary-database-pair class consistent across README coverage map, PROVINCE, SKILL — YES

Six surfaces, one class, no contradiction (quotes ≤ 25 words):
- Coverage-map bullet header `corpus/README.md:267`: "(sixth task, binary database file pair)".
- §Frontier `corpus/README.md:330`: "a JSON export at `/app/recovered.json` whose source of truth is a
  binary database file pair — `main.db` plus an XOR-encrypted `main.db-wal`".
- PROVINCE.md:426: "export at `/app/recovered.json` whose source of truth is a binary database file
  pair — `main.db` plus an XOR-encrypted write-ahead log" (round-40 paragraph at PROVINCE.md:419).
- SKILL.md:971: "truth is a binary database file pair — `main.db` plus an XOR-encrypted `main.db-wal` —
  and the whole score is seven pytest functions over that export".
- SCORECARD.md:1473 capability name `binary-db-grader-probe`: "graded artefact is an export of a binary
  database pair". SCORECARD.md:1461 phrases the same class descriptively ("a SQLite main database plus an
  XOR-encrypted WAL") — same meaning, not a conflicting class label.
- Lesson title `corpus/lessons/round-40.md:1`: "a sixth TB2 grader (binary database pair) executed".
- "New class" claim holds: rounds 35–39 classes are G-block/regex-log/git-webserver/build-provenance/
  repository-history (corpus/README.md:262–266); a JSON export of a binary DB pair is not among them.

## 3. SHONEN/SCORECARD self-assessment vs repo — no mismatch

SHONEN.md (12 lines) anchors, all resolve at the tip:
- box 2 `LOG.md:7` → round-3 end-to-end entry (`sed -n '7p'` = 2026-09-28 round-3 bench-arena +
  telemetry analysis) ✓.
- box 3 `corpus/lessons/round-8-aggregator-box3-coldrun.md:48` → line 48 = "## Box-3 verdict" ✓.
- box 4 `PROVINCE.md:129` → line 129 = "### Adjacent" (the routing section that states no-bleed) ✓.
- box 1 cites SKILL.md without line; SKILL.md (1030 lines) carries decision tables ✓.

SCORECARD round-40 block (SCORECARD.md:1448–1493) counts, all reproduce:
- "knowledge files/index rows 46→47": `ls corpus/knowledge | wc -l` → 47;
  `grep -c '^| \`knowledge/' corpus/README.md` → 47 ✓.
- "SOURCES 111→114": `grep -c '^| S' corpus/SOURCES.md` → 114 ✓. Tier split "tier A +2, tier B +1"
  verified from the rows: SOURCES.md:134 S119 tier A, :135 S120 tier A, :136 S121 tier B ✓.
- C1 "21 frozen mutants (anchor 11, ledger 7, order 3)": `awk '/^MUTANTS = \[/,/^\]/' plans/
  round40_c1_verify.py | grep -oE '"(anchor|ledger|order)"' | sort | uniq -c` → 11 anchor, 7 ledger,
  3 order = 21 ✓. Battery module set in plans/battery40/ = a_tok, a_row, a_bind, a_man, l_rows,
  l_refuse, o_gate (7 modules) ✓.
- Receipt numbers: `sed -n '34,35p' corpus/evidence/round40/db-wal-probe.txt` → "regrade cases=28
  differ=0" / "cases=28 observed_pass=8 observed_fail=20 mismatches=0" — matches SKILL.md:966–967,
  corpus/README.md:267, PROVINCE paragraph, SCORECARD.md:1461 ✓.
- "order_check round 38 exit 1, rounds 39 and 40 exit 0": `.ufo/waves/round-40/integrate/measure-final.txt`
  shows round-40 `ORDER RESULT PASS` (:79), round-39 PASS (:86), round-38 `ORDER RESULT FAIL`/`exit=1`
  (:95–96) ✓.
- "S046/S052 anchor notes": registry rows SOURCES.md:68 (S046) and :74 (S052) both carry
  "rechecked 2026-10-26 on Python 3.15.2 docs (R40SourcesRecheck)" ✓.
- No-harm lines in measure-final.txt: round-40 C1 `MUTANTS total=21 killed=21 … PREDICATE C1 pass`
  (:47–50), C2 `checks=7 defects=0`/`PREDICATE C2 pass` (:71–72) ✓.

## Cross-document drift note (out of scope, recorded)

None found inside this scope. The one historical drift class (wave-context tip hash vs measured tip,
`F39ConnClaims` pattern) does not recur: the SCORECARD round-40 header names landing
`ec17216844585d0fecde9f1d4c4be0b78a3bf76f`, the assignment's measurement tip is
`ec1005a2a28bc5cfdde7723374368ed4cc956eed` — both post-claims commits on master; the frozen claims file
itself pins baseline `d3a6277f…` and the predicates were re-measured on the tip I checked. No count or
file:line mismatch results from it, so it is noted, not counted.

## VERDICT

VERDICT: frontier-consistent-yes-mismatches-0
