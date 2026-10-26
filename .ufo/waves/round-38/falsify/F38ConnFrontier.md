# F38ConnFrontier — frontier read (round 38 wave 2 falsify)

Seat: F38ConnFrontier (connector). Target: does `corpus/README.md` §Frontier and the coverage map at
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a` reflect four TB2 grader classes correctly, and which sibling
lanes hold adjacent material the round should cite. Method: read-only; no lane file touched. All paths
below are lane-relative unless absolute.

## Axes

- Coverage correctness: README index + coverage bullets + §Frontier sub-bullets vs the four landed TB2 entries and receipts.
- Adjacency: PROVINCE report-out pointers vs sibling-lane reality; uncited adjacent material sweep.

## Q1 — README reflection of the four TB2 classes: HOLDS

**Entries present in the tip tree** — `git ls-tree --name-only 8c7422d7… corpus/knowledge/ | grep tb2`:

```
corpus/knowledge/tb2-build-pmars-grader.md
corpus/knowledge/tb2-git-webserver-grader.md
corpus/knowledge/tb2-protein-assembly-grader.md
corpus/knowledge/tb2-regex-log-grader.md
```

**Coverage map (What's here table) rows** — `sed -n '68,71p'` of the tip README shows all four rows with
correct source groups: protein-assembly S105–S107 (:68), regex-log S108–S110 (:69),
git-webserver S111–S114 (:70), build-pmars S115–S116 (:71).

**Coverage bullets (:260–263)** — four bullets, arithmetic coherent: r35 "Not the other 88 TB2 tasks",
r36 "one more of the 89 TB2 task graders", r37 "3 of the 89", r38 "4 of the 89".

**§Frontier sub-bullets (:288–303)** — r35 "discharged", r36 "discharged", r37 "**narrowed** … (3 of 89
read)", r38 "**narrowed** … (4 of 89 read)". The "narrowed" verb matches the entries' own language
(`tb2-git-webserver-grader.md` and `tb2-build-pmars-grader.md` both say "It **narrows** the … clause");
not a wording drift.

**Receipt numbers match the bullets and claims** — `tail -1` on each receipt:

```
corpus/evidence/round35/tb2-grader-probe.txt      cases=18 observed_pass=5  observed_fail=13 mismatches=0
corpus/evidence/round36/regex-log-probe.txt       cases=24 observed_pass=8  observed_fail=16 mismatches=0
corpus/evidence/round37/git-webserver-probe.txt   cases=22 observed_pass=9  observed_fail=13 mismatches=0
corpus/evidence/round38/build-pmars-probe.txt     cases=22 observed_pass=7  observed_fail=15 mismatches=0
```

**"89" count is grounded, not asserted** — two independent anchors:
- `.ufo/waves/round-35/build/R35ScoutMergePkg.md:214,230` — live-repo parse at the pinned commit: "89 task
  directories and 89 `task.toml` files"; "92 top-level entries — 89 directories plus .gitignore, LICENSE
  and README.md".
- "89 carry `tests/test.sh`" traces to `corpus/knowledge/benchmark-verifier-execution-model.md:93`
  (round-31 entry), quoted in `.ufo/waves/round-36/build/R36CritScope.md:236` and
  `.ufo/waves/round-37/build/R37CritScope.md:164`.

**PROVINCE r38 arithmetic** — `PROVINCE.md:303`: "remaining 85 TB2 task graders (89 carry `tests/test.sh`;
4 are read)" — 89−4=85. ✓

**S115/S116 digests match the captures** — `sha256sum corpus/evidence/round38/tb2-build-pmars/{test_outputs.py,instruction.md}`:

```
d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85  test_outputs.py
1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82  instruction.md
```

Identical to the `corpus/SOURCES.md:130-131` rows. `sha256sum -c SHA256SUMS` → all five files `OK`.

**SKILL.md registry** — tip `SKILL.md` carries the `build-pmars-probe` row (:582) and the
"## Build-provenance TB2 grader — round 38" section (:813) with a 14-row decision table; the receipt
summary line it quotes (`build-pmars-probe.txt:26`) matches the receipt.

### Minor observations (pre-existing, not round-38 gaps)

- The r35 §Frontier sub-bullet (:288) still reads "reads and executes … `tests/test_outputs.py` +
  `tests/test.sh`"; the standing correction at README :429 notes `test.sh` was read, not run. The r36/r38
  bullets use the careful "read, not run" phrasing. Predates round 38; the dated-sub-bullet convention
  keeps it as round-35 history.
- None of the four TB2 knowledge entries names a sibling lane (`grep -c "kaidoku|tameshi|kumitate"` → 0
  in all four). That is lane convention — adjacency is registered in `PROVINCE.md`, which does carry it.

## Q2 — Sibling adjacent material: cited pointers all real; sweep found nothing required uncited

**PROVINCE report-out table (D6)** lists seven lanes. Existence check on all seven primary pointers:

```
OK tameshi-shokunin/tools/mutate-and-run.sh      OK kake-shokunin/.ufo/waves/round-36/sealed_count_v2.py
OK tameshi-shokunin/tools/env-diff.py            OK mori-shokunin/.ufo/waves/round-31/count-c2-a1.py
OK kumitate-shokunin/scripts/cap-run.mjs         OK kaidoku-shokunin/SKILL.md
OK mado-shokunin/quality/counters/c1-r40-live-v2.py
```

Spot-checked line accuracy: `tameshi …/mutate-and-run.sh:1418,1423,1428` shows the `env -i` isolation
the table claims ("env -i, not bwrap"); `mori …/count-c2-a1.py:75-77` is the cited `bwrap --ro-bind / /`
arm; `kake …/sealed_count_v2.py:158-163` is the bwrap argv. `kaidoku-shokunin/PROVINCE.md:4,48,57`
confirms the native-ELF ground (Ghidria/REA, `nm -D`/N-API taxonomy) the table cites as
"owner of binary-linkage interpretation" — the right owner for the build-pmars `ldd`/`DT_NEEDED` reading.

**Named-adjacent without a table pointer** (PROVINCE r38 paragraph): chousa "capture and citation method"
(`chousa-shokunin/corpus/knowledge/anchor-boundaries-r4.md`, `archived-export-intake.md`) and tameshi
"build and package craft" (its defect-probe/mutation tooling; no dedicated compilation entry exists in
`tameshi-shokunin/corpus/knowledge/`). Acceptable as prose-level adjacency; a future round could pin a
chousa row if the citation-method link is ever load-bearing.

**Sweep for uncited adjacent material** — sibling-wide greps:
- `grep -rli "pmars|build-pmars" */` (excl. kengaku): only `kasegi-shokunin/.ufo/waves/round-34/wave1/CritBoundary.md:206`
  (a ledger-tip line *about kengaku's own* probe run `e95cf55` — kasegi citing kengaku, not adjacent ground)
  and `kotodama-shokunin/…/ReviewReadmeRevCode.md:244` (coincidental `/tmp/tmpmarsp6nu` substring). No
  sibling holds pmars ground.
- `grep -rli "provenance|supply.chain|SBOM|reproducible build" */corpus/`: audio-shokunin hits are
  dubbing provenance (ElevenLabs), not binary build provenance; `tsukuroi-shokunin` AUR risk-plane entries
  are package-source risk — marginal to the Debian-source-provenance class, not required.
- No sibling lane has read a TB2 task grader (`terminal-bench` grep hits are routing/ledger mentions,
  e.g. `kumitate-shokunin` registry rows, `kama-shokunin` wave outputs).

## Proposed move (bounded)

None required for admission. Optional, zero-harm: when a future round next edits the r35 §Frontier
sub-bullet for another reason, align its `tests/test.sh` phrasing with the standing :429 correction
("read, not run") — cosmetic only; the correction note already covers it, so no edit is being claimed
necessary now.

VERDICT: frontier-ok
