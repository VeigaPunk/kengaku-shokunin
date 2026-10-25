# R30FxEvidence — does every pointer the round cites resolve?

Seat: `R30FxEvidence` (scout/evidence, leaf). Target: every repo-relative path, commit hash and
command cited by `corpus/lessons/round-30.md`, `plans/round-30-claims.md` and the 36 build reports
under `.ufo/waves/round-30/build/`. Checks were run, not trusted: `test -e`, `git cat-file -e
<sha>^{commit}`, and the cited commands themselves.

Candidate this round admits and that these pointers are supposed to carry:
`corpus/knowledge/contamination-transparency-card.md`.

No anchored `VERDICT:` line is emitted here on purpose. This seat is neither a source re-read nor
the complete-set review; `plans/gate_timing_check.py` machine-reads `^VERDICT:` across falsify
reports whose registry role is in `{reviewer, scout, critic, sentinel, revenger}` (scout is
allowed), so a verdict line from an evidence seat would be counted as a Q10 second seat that never
re-opened a source. `R30FxQuotes.md` makes the same choice and says so.

## Read-time pins (the lane was being edited while this ran)

| item | value |
|---|---|
| check time | 2026-10-25T07:43Z (UTC) |
| `git rev-parse HEAD` | `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db` (baseline; no round-30 commit exists) |
| working tree | round-30 bytes entirely uncommitted: `M` on 6 tracked files, `??` on `.ufo/waves/round-30/`, `corpus/evidence/round29-attempt2/control-nothing.txt`, `corpus/evidence/round30/`, `corpus/knowledge/contamination-transparency-card.md`, `corpus/lessons/round-30.md`, `plans/round-30-claims.md`, `plans/round30_defects.py` |
| `corpus/lessons/round-30.md` | sha256 `e80258908899e81820751308c0813a1975fa6e528183523570d08d3c353d1943` (pinned copy; it moved `ad5bd018…` → `e63ea920…` → `e8025890…` during this check) |
| `plans/round-30-claims.md` | sha256 `987dd3383687fef2dd6a8f5fa9fa463863d82fd289302712f055d77e1b9279ef` |
| `plans/round30_defects.py` | 222 lines, sha256 `114b2aad561a2a9ec188fe09d8dca6a0597f8fd4a7a0239ab82d383f2997ba53` |

Line numbers below are from the pinned lesson/claims copies. Because sibling seats were repairing
the lesson live, every `absent` row was re-tested against the live tree at the timestamp above; the
"landed since pin" column records files that appeared mid-run.

## A. Lesson + claims path pointers — 61 tokens, 53 resolve, 6 absent, 2 are patterns

Method for every row: `test -e <path>` (from the lane root) on the pinned citation; `test -e` again
live at 07:43Z.

| pointer | cited at | check | result |
|---|---|---|---|
| `plans/round-30-claims.md` | lesson:4 | `test -e` | resolved |
| `corpus/knowledge/contamination-transparency-card.md` | lesson:3,8,28 and claims:18,31 | `test -e` | resolved (17 074 B, six `source:` lines, no other S-id in the body) |
| `corpus/lessons/round-29.md` (+ `:180`, `:227`, `:241-243`) | lesson:9 | `test -e`; `sed -n` | resolved — `:180` is the attempt-2 Gate flip row, `:227` "amendment, not a rival", `:241-243` the flip condition |
| `.ufo/waves/round-30/build/R30SrcS081.md` … `R30SrcS086.md` (6) | lesson:17,31 | `test -e` ×6 | all resolved |
| `.ufo/waves/round-30/build/R30DraftGate.md` | lesson:18-20 | `test -e` | resolved |
| `.ufo/waves/round-30/assimilation/{reg-ids,staged-ids,collisions}` (3) | lesson:21 | `test -e` ×3 | resolved (410 B / 875 B / 30 B) |
| `.ufo/waves/round-30/build/R30BuildAppend.md` | lesson:21 | `test -e` | resolved |
| `corpus/SOURCES.md` S091 | lesson:22 | `test -e` + `grep '^\| S091'` | resolved |
| `.ufo/waves/round-30/assimilation/quarantine-slice` | lesson:23 | `test -e` | resolved (52 B) |
| `corpus/QUALITY.md` Q20 | lesson:24 | `grep -n Q20` | resolved (line 198) |
| `.ufo/waves/round-30/build/R30Considerthese.md` | lesson:24 | `test -e` | resolved |
| `LOG.md:372` | lesson:24 | `grep -n` | resolved — exact sentence "Receipts are author-observed, never non-author closure." |
| `.ufo/waves/round-30/build/R30RevCounter.md` | lesson:72 | `test -e` | resolved |
| `plans/round30_defects.py` | lesson:73 | `test -e` | resolved |
| `.ufo/waves/round-30/claims/control-nothing.txt` | lesson:111 | `test -e` | resolved; content `entries=0 … census=ok` / `exit=1` |
| `.ufo/waves/round-30/claims/defects-before.txt` | lesson:113 | `test -e` | resolved; 5 DEFECT lines, `defects=5`, `exit=1` |
| `.ufo/waves/round-30/claims/gate-before.txt` | lesson:117 | `test -e` | resolved; `cases=10`, `quote_mode_exit=2` |
| `.ufo/waves/round-30/assimilation/` | lesson:62 | `test -d` | resolved |
| `corpus/evidence/round30/census-before.txt` (+ `rows-opened.tsv`) | lesson:63,95 | `test -e` | resolved; 14 `W04` lines |
| `.ufo/waves/yield.tsv` | lesson:123 | `test -e` + `grep round-30` | resolved; exactly 36 round-30 rows, all `build/` reports |
| `.ufo/waves/round-30/adoption-expect.json` | claims:32 | `test -e` | resolved |
| `.ufo/waves/round-29/attempt2/adoption-expect.json` | claims:68 | `test -e` | resolved |
| `corpus/evidence/round29-attempt2/`, `.ufo/waves/round-29/attempt2/` | claims:67 | `test -d` | resolved |
| `corpus/lessons/round-29-verifier-spotcheck.md` §5 | claims:50,75 | `test -e` + headings | resolved (§5 "Trend verdicts and routed defects") |
| `corpus/README.md` §Frontier bullet 4 | claims:11 | `awk '/^- \*\*/'` | resolved — bullet 4 is line 281 "Identity-verified endpoint for novelty probes" |
| `corpus/README.md` §Frontier bullet 2 | claims:22 | same | resolved — line 274, contamination bullet |
| `plans/adoption_check.py`, `plans/sources_adopt.py`, `plans/gate_timing_check.py` | claims:32,82; lesson:36 | `test -e` | resolved |
| **`.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md`** | **lesson:17, 31** | `test -e` | **absent** (E2) |
| **`.ufo/waves/round-30/falsify/R30FxRowsCensus.md`** | **lesson:35** | `test -e` | **absent** (E2) |
| `.ufo/waves/round-30/falsify/R30FxSrcS085.md` | lesson:17,33 | `test -e` | absent at 07:43Z, **landed 07:45Z** — window closed by the seat, not by an edit |
| **`.ufo/waves/round-30/falsify/R30FxSrcS08{1,2,3,4,6}.md`** | lesson:17,33 | `test -e` | resolved for 081/082/083/084/086 |
| `.ufo/waves/round-30/falsify/R30FxEntryQ7Q9.md` | lesson:100 | `test -e` | absent at 07:43Z, **landed 07:45Z** |
| **`.ufo/waves/round-30/falsify/swarm-registry.json`** | lesson:36 | `test -e` | resolved (8 896 B) |
| **`ufo-wave-policy.json`** | **claims:13** | `test -e` | **absent at lane root** (E6); resolves at `scripts/hyaku/ufo-wave-policy.json`, `waveMinLanes=32` / `waveMaxLanes=64` |
| `[^`] corpus/knowledge/*.md` (glob), `assimilation/{…}` (brace list) | lesson:70,21 | pattern, not a path | not a pointer (both expand) |

## B. Hashes — 21 commit-shaped citations, all 21 resolve

Method: `git cat-file -e <tok>^{commit}` from the lane (and, for one, the fleet repo).

| hash | cited at | result |
|---|---|---|
| `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db` | lesson:4 | resolved (baseline tip = HEAD) |
| `1f3b0f1ec41ec297130e8944ff97968d32324632` | R30DefectFix.md:54; receipt provenance | resolved (round-29 baseline) |
| `8c14a5d` (`8c14a5dc…`) | R30CritC1.md:157, R30DefectFix.md:55 | resolved (round-29 freeze) |
| `2ff4b6f`, `1f3b0f1`, `8cf7b60`, `f11bffbf`, `6180e4f`, `f09ff1f`, `30ee3b5`, `ff476d0`, `4b82ff7`, `7bc2aaf`, `c88310f`, `363a4eb(f)`, `8a9ad488c492`-family (12 tokens) | R30Census.md, R30ConsidereThese.md:42, R30GateQuote.md, R30SimplGate.md:14, R30Yield.md:72 | resolved |
| `d4090261` (fleet repo) | R30DefectState.md:51 | resolved — `git -C /home/vgpnk/Projects/shokunin cat-file -e d4090261^{commit}` |
| **`e565468`** | **lesson:71 ("counter revision")** | **not a git object** — `git cat-file -t e565468` → `fatal: Not a valid object name` (E4). It is the sha256 prefix in `R30RevCounter.md:18` (`e565468da8e6…9380`, 216 lines). Live counter: 222 lines, sha256 `114b2aad…ba53`. |
| 119 further hex tokens (64-char sha256, md5, ETag, byte sizes `2697379`/`1949572`, mtimes `1792911454`) | lesson:51-56, build reports | not commits by design — digests/identities, correctly cited as `sha256 …` |

Scratch-only commits (`dd83a3d`, `126145a`, `756f499`, `9a70406`, `19ce533`, `8a9ad48`) exist only
in the `/tmp` sandboxes the build seats made; they are labelled as sandbox commits where cited and
are not lane pointers.

## C. Commands the round cites — 13 run, 10 green, 3 non-green

| command | cited at | observed | verdict |
|---|---|---|---|
| `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census` | claims:32, lesson:109 | `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, rc 0 — the exact frozen string | green |
| same on the pre-append tree (C1 control) | claims:35, lesson:111 | baseline clone (`git clone` + `checkout 363a4eb` + only the untracked expect file): `entries=0 … usedby_ok=0 census=fail`, rc 1 | green on substance: six fields and exit 1 reproduce; `census` differs only because the fleet census needs `<root>/shokunin.conf` (see H) |
| `python3 plans/round30_defects.py --lane .` (C2) | claims:54, lesson:112 | `DEFECT D1 receipt-at-cited-path: … not committed at HEAD`; `ok D2`; `ok D3`; `DEFECT D4 uncommitted-wave-evidence: HEAD:…R29a2CritEntry.md omits the addendum`; `ok D5`; **`defects=2`, rc 1** | **red** (E1) |
| same on pre-repair bytes (C2 control) | claims:56, lesson:113 | baseline clone + counter copied in: `DEFECT D1 … DEFECT D2 … DEFECT D3 … DEFECT D4 … DEFECT D5 …`, **`defects=5`, rc 1** — matches `claims/defects-before.txt` line-for-line (D5's message appends "and the entry cites no S091", additive only) | green — the counter is failure-capable, not a no-op |
| `python3 plans/sources_adopt.py --selftest` (C3) | claims:79, lesson:115 | `SELFTEST cases=14 failed=0`, rc 0; includes `quote-overlong-refused`, `quote-absent-refused`, `quote-boundary-25-accepted`, `quote-located-accepted` | green |
| pre-change body, `--quote-file … --artifact …` (C3 control) | claims:82, lesson:117 | `git show 363a4eb:plans/sources_adopt.py` → argparse `unrecognized arguments: --quote-file … --artifact …`, **rc 2**; its selftest `cases=10 failed=0` | green |
| C3's two refusal classes are distinct (my own probe, `/tmp` fixture row from S081) | claims:80 | 26-word quote vs unrelated artifact → **rc 6**; located-but-absent → **rc 7** | green (6 ≠ 7, both non-zero) |
| `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit <admitting sha>` | lesson:36 | no admitting sha exists; with `--commit HEAD`: `INPUT ERROR: cannot read corpus/lessons/round-30.md at HEAD: fatal: path … exists on disk, but not in 'HEAD'`, **rc 2** | **red** (E3) |
| `python3 plans/gate_timing_check.py --selftest` | claims:79 (set of gates) | `[selftest] ALL PASS …`, rc 0 | green — the gate works; the gap is the commit |
| `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census` (C2 kill rule) | claims:60 | `entries=1 … cited_rows=5 … usedby_ok=1 census=ok`, rc 0 — round 29's frozen counter unchanged | green |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (census sentence) | lesson:62 | rc 0, exactly 14 `W04` lines, same 14 as `census-before.txt` | green |
| `git show <baseline>:corpus/SOURCES.md` / `git diff --numstat <baseline> -- corpus/SOURCES.md` | lesson:57-60 | 82 rows at baseline with last ids `S077 S078 S079 S080 S090 S091`; numstat `6 0`; tiers parsed from cells: baseline A 76 / B 4 / C 2 → now A 79 / B 7 / C 2; rows now 88 | green (all four numbers as written) |
| `python3 grader.py` and the five plan selftests Q20 names | QUALITY.md Q20 via lesson:24 | `CHECKS n=733 mismatches=0 errata_pinned=1` + `VERDICT: PASS`; `attrib_calibration` 18/0 (895 ms), `benchmark_spec_audit` 67, `config_projection` 31, `parser_policy_compare` 9 policies/59 cases/10 killed, `grader_perturb` 10/0, `registry_check` 15, `state_check` ALL PASS, `sources_adopt` 14 — all rc 0, ≤ 895 ms each | green |

## D. Build-report sweep (36 reports, 8 032 lines)

Method: every backticked token with a path/extension shape, 2 821 tokens → 181 resolve in-lane,
159 are non-lane (URLs, code, `/tmp` scratch), 41 are lane-shaped and absent. The 41 were triaged
by context, not by guess:

| bucket | count | examples |
|---|---|---|
| asserted as existing and **absent** | 4 tokens / 6 sites | E7, E8 below |
| wrong line number on an existing file | 1 | E9 |
| self-declared absent, proposed, or a required-but-missing artefact | 9 | `.ufo/reports/round-30/` ("does not exist yet", R30RevEntryQ7Q9.md:56), `.ufo/waves/round-30/d5-usedby-note.json` (proposal, R30CritC2.md:208), `corpus/source-fetches.tsv` + `corpus/inrow-pins.tsv` (tested `ABSENT` by the report itself, R30ConnSibling.md:73), `plans/round30_census.sh` / `plans/mkyield.py` (proposed landings), `corpus/evidence/round30-sources/` (required list, R30RevEntryQ7Q9.md:234), `corpus/knowledge/nonexistent-entry.md` (negative fixture) |
| other-root, resolves where stated | 15 | `kengaku-shokunin/PROVINCE.md(:125)` ✓, `kengaku-shokunin/corpus/SOURCES.md` ✓, `/home/vgpnk/Projects/shokuknow/merge/kengaku/…` ✓, `scripts/sources-census.sh` ✓, `.ufo/reports/round-29/kengaku.md` ✓ (fleet root) |
| quoted from another lane, not this lane | 6 | `kagi-shokunin/corpus/{sources-census.sh,rendered-text-v1.py}`, `chousa-shokunin/…`, `tools/research-gate.sh`, `corpus/evidence/round36/c1-count.py` |
| patterns/fragments | 6 | `corpus/evidence/roundNN-sources/gate.md`, `knowledge/[^…`, `plans/sources_adopt.quoted_spans` (attribute) |

## E. Defects — absent or unresolvable pointers, named

**E1 (blocking, calibration).** `corpus/lessons/round-30.md:112-113` records C2 as measured:
"`defects=5` exit 1 at freeze → `defects=0` exit 0 after the commit that lands D1's receipt and D4's
wave evidence." No such commit exists: HEAD is still `363a4eb` and every round-30 byte is untracked.
The reported command now prints **`defects=2`, rc 1**, and the two red items are exactly the two the
sentence says the commit closed (D1: the receipt exists only in the worktree; D4: `HEAD:` blob lacks
`### D. Addendum`). Same gap in `:9-10` ("Both flip loci … are discharged in one commit") and
`:15-16` ("the Q10 second-seat row cites a report path that lands in the same commit").

**E2 (blocking, freshness).** `corpus/lessons/round-30.md:17`, `:31`, `:35` cite falsify reports
that were not on disk at 07:43Z. Re-tested at 07:45:02Z, two are still absent —
**`R30FxEntryCompleteSet.md`** (the Q10 complete-set seat, the one `:17` says carries a `VERDICT
line`) and **`R30FxRowsCensus.md`** — while `R30FxSrcS085.md` and `R30FxEntryQ7Q9.md` landed in the
two-minute window. The sentence around them is past tense ("Second-seat re-reads for this
admission: …", "a `reviewer` seat that did not write the entry re-opened all six sources and
re-derived every number"), so it asserts a complete-set return that does not exist. Five per-source
seats and the registry have landed (S081–S085, S086; each carrying an anchored `VERDICT:` that names
the candidate), so E2 is a timing defect that closes when the complete-set seat lands — but the
lesson bytes must not read as returned until it does, and the `VERDICT line` the Gate row promises
is specifically the missing one.

**E3 (blocking, operability).** `corpus/lessons/round-30.md:36` prescribes
`python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit <admitting sha>`.
There is no admitting sha in the lane, and at `HEAD` the gate exits 2 (`INPUT ERROR … exists on
disk, but not in 'HEAD'`). The gate itself is healthy (`--selftest` ALL PASS), so a reader cannot
execute the round's own Q13 check.

**E4 (calibration).** `corpus/lessons/round-30.md:71-72` calls `e565468` a "counter revision" and
pairs it with `R30RevCounter.md`. `git cat-file -t e565468` → `fatal: Not a valid object name`. It
resolves only as the sha256 prefix of `plans/round30_defects.py` recorded at
`R30RevCounter.md:18` (`e565468da8e6…9380`, 216 lines); the live body is 222 lines with sha256
`114b2aad…`. A reader following the lesson's wording alone cannot resolve it.

**E5 (low).** `corpus/lessons/round-30.md:124` — "dead-seat detail is in the round report".
`.ufo/reports/round-30/` does not exist (`test -e` → absent; `R30RevEntryQ7Q9.md:56` says so too).
Dangling referent: the sentence names no path.

**E6 (low, ambiguity).** `plans/round-30-claims.md:13` cites `ufo-wave-policy.json` bare. Absent at
the lane root; the file the claim's band comes from is
`scripts/hyaku/ufo-wave-policy.json` (`waveMinLanes: 32`, `waveMaxLanes: 64` — band 32–64 confirmed).

**E7 (medium).** `.ufo/waves/round-30/build/R30Q13Check.md:92`, `:138`, `:195` cite
`.ufo/waves/round-30/falsify/FR30ReReadSources.md` as the *returned* Q10 re-read, with a sha256
(`7b72aaaa51bed252…`). The file does not exist and no seat in `.ufo/waves/round-30/falsify-spec.json`
has that name. The same seat is spelled `R30FxEntryCompleteSet` in the spec and
`R30FxEntryCompleteSet.md` in the lesson — three spellings, zero bytes under two of them.

**E8 (medium).** `.ufo/waves/round-30/build/R30RevLesson.md:119-121` cite
`.ufo/waves/round-30/falsify/R30RevEntryQ1Q6.md`, `…/R30RevEntryQ7Q9.md`, `…/R30RevRows.md`. All
three are absent under `falsify/`; the same names exist under `build/`. Mis-pathed pointers to
files that do exist.

**E9 (low).** `.ufo/waves/round-30/build/R30ConnSibling.md:33` cites
`kengaku-shokunin/corpus/README.md:272` for the "Contamination transparency cards" bullet. Line 272
is the *Agentic benchmark task-spec audits* bullet; the cited text is at `:274`. (The lesson's own
"bullet 2" at `:22` and the claims' "bullet 4" at `:11` are both correct.)

## F. Numbers that were wrong and were repaired mid-run (calibration record)

At digest `ad5bd018…` the lesson's Sources table disagreed with the entry and with the quotes
seat's independent measurement; at the pinned digest `e8025890…` it agrees. Not live defects, but
they show the table was re-derived while this seat ran.

| cell | at `ad5bd018` | at `e8025890` | independently measured |
|---|---|---|---|
| S081 third span | 21 words | 18 | 18 (`R30FxQuotes.md:37` `S081.3`) |
| S084 second span | 13 | 7 | 7 whitespace tokens (12 CJK chars) |
| S084 third span | 3 | 1 | 1 |
| S086 caveat | 23 CJK chars, lines 78-81 | 30 CJK chars, lines 80-81 | 30 (`R30FxSrcS086.md` FAIL names the same 23-vs-30 gap against entry line 6) |

Entry-side note for the Q10 seat, not resolved here: `R30FxSrcS086.md` returns `VERDICT: FAIL` on
the entry's own S086 line (23 stated vs 30 measured), and `corpus/SOURCES.md`'s S086 row states 30 —
a C1 kill-rule input (`fewer than four of the six survive`), not a pointer defect.

## G. Split

- **Paths:** 61 cited tokens in the lesson + claims → **53 resolve, 6 absent, 2 patterns** at
  07:43Z; after two seats landed, **55 resolve, 4 absent** (`R30FxEntryCompleteSet.md`,
  `R30FxRowsCensus.md`, and `ufo-wave-policy.json` at the lane root). Build
  reports: 181 in-lane tokens resolve; of 41 absent, **4 are asserted-and-absent** (E7, E8), 1 wrong
  line (E9), 36 correctly self-declared, proposed, other-root or negated.
- **Hashes:** 21/21 commit-shaped citations resolve; 1 digest-style citation (`e565468`) resolves
  only through the build report that recorded it (E4); 119 further hex tokens are digests/ETags/
  sizes, not commit claims.
- **Commands:** 13 run — 10 green, 3 non-green (C2 `defects=2` rc 1; Q13 rc 2; and C2's post-repair
  control of `defects=0` cannot be run at all, which is the same defect as E1).

## H. Limits of this check (stated so the next reader does not inherit a false green)

- The census field of the C1 control could not be reproduced off the fleet root: `sources-census.sh`
  needs `<root>/shokunin.conf`, so a `/tmp` clone prints `census=fail`. Six of seven fields and the
  exit code reproduce exactly, and the live fleet census is rc 0 with the same 14 `W04` lines. The
  control receipt is not contradicted by this; the `census` cell is simply fleet-root-scoped.
- Nothing in the lane was modified; every probe that needed mutated bytes ran on `/tmp` copies
  (`/tmp/r30fx-evidence3/{clone,root,c3}`), and no tool was installed or upgraded.
- The lesson moved three times during this run (`ad5bd018` → `e63ea920` → `e8025890`) because
  sibling seats are repairing it. Any `absent` row above should be re-tested before it is quoted as
  a standing defect; the three that matter (E1, E2, E3) are all gated on the missing commit, which
  no lesson edit can supply.

## Hand-off status (last live check 2026-10-25T07:45:02Z)

| item | state |
|---|---|
| `git rev-parse --short HEAD` | `363a4eb` — unchanged; still no round-30 commit |
| `python3 plans/round30_defects.py --lane .` | `defects=2`, rc 1 (D1 receipt uncommitted, D4 addendum absent from `HEAD:`) |
| `gate_timing_check … --commit HEAD` | rc 2, `INPUT ERROR … not in 'HEAD'` |
| falsify reports landed since the main check | `R30FxSrcS085.md`, `R30FxEntryQ7Q9.md` |
| falsify reports still absent | `R30FxEntryCompleteSet.md` (Q10 complete set), `R30FxRowsCensus.md` |

E1 and E3 cannot be closed by any seat's bytes: they need `git add` + one commit of the round-30
tree. E2 closes when the complete-set seat lands, and only then may the Gate row read as returned.
