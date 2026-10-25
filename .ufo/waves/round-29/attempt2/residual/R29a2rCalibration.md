# R29 attempt-2 residual — calibration: self-assessment vs committed bytes

Seat `L1Kengaku29.R29a2rCalibration` (leaf). Target: round 29 attempt 2, landing commit
`ff476d0` (`ff476d017107ec5ee3df735a16713c5967592b71`), lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
No production edits; the only lane write is this report. Scratch: `/tmp/r29a2r-calibration/`
(two source tarballs, one `git archive` extraction, mutant copies). No tool installed, no pacman.

**Method.** Every verdict below is an executed command whose output is quoted. The landing state was
measured from an extracted tree (`git archive ff476d0 | tar -x -C /tmp/r29a2r-calibration/tree`) so the
numbers do not move under the audit; the live lane was measured separately because the counter's
`--census` mode depends on the lane directory name (see F6).

**HEAD moved during the audit.** At start HEAD was `ff476d0`; by close it was `30ee3b5` —
`4b82ff7`, `7bc2aaf`, `c88310f` (all 2026-10-25) and `30ee3b5` landed while this seat ran. Table rows
name the commit they were measured at. `ff476d0` is the ticket's landing commit and the primary
reference; the drift section (F7) states what changed after it.

No `lsp` device exists in this subagent's toolset, so no caller/definition claim below rests on
text search: every code-level statement is execution-backed (`--selftest`, mutated copies, real runs).

---

## 1. Claim-by-claim re-derivation

Abbreviations: `PKG=/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`,
`REG76` = `git show 1f3b0f1:corpus/SOURCES.md` (baseline registry, 76 rows).

| # | claim (file:line @ commit) | command | observed | verdict |
|---|---|---|---|---|
| 1 | Registry 82 rows, S001–S080 + S090 + S091, tiers A76/B4/C2 (LOG.md:697 @ff476d0; lessons:205 @30ee3b5) | `grep -cE '^\s*\| *`?S[0-9]{3}' corpus/SOURCES.md` ; `awk -F'|' … $5` tier histogram ; id-set check | `82`; `A 76 / B 4 / C 2`; 82 unique ids, no gap in S001–S080, extras `S090 S091` | **MATCH** |
| 2 | Baseline 76 rows, tiers A70/B4/C2 | `git show 1f3b0f1:corpus/SOURCES.md \| grep -cE …` ; same tier awk | `76`; `A 70 / B 4 / C 2` | **MATCH** |
| 3 | "Registry 76 → 81 rows" (SCORECARD.md:994, LOG.md:641 both still at `30ee3b5`; lessons:205 @`ff476d0`) | as #1 | landed registry is `82`; `8cf7b60` was `81`, `ff476d0` is `82` | **MISMATCH** |
| 4 | "tiers A 70 → 75" (lessons:205 @`ff476d0`) | tier awk at `8cf7b60` and `ff476d0` | `8cf7b60`: A75; `ff476d0`: A76 | **MISMATCH** (@ff476d0 only; corrected at `4b82ff7` to "A 70 → 76", which **MATCHES**) |
| 5 | knowledge files 37 → 38 | `ls corpus/knowledge \| wc -l` at baseline tree and landing tree | `37` → `38` | **MATCH** |
| 6 | knowledge index rows 37 → 38 | `grep -cE '^\| `knowledge/' corpus/README.md` both trees | `37` → `38` | **MATCH** |
| 7 | selftest ten cases, `failed=0`, exit 0 | `python3 plans/sources_adopt.py --selftest` | ten `CASE … PASS` lines, `SELFTEST cases=10 failed=0`, exit `0` | **MATCH** |
| 8 | C1 counter prints exactly `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, exit 0 | `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census` | byte-identical line; 7 fields; exit `0` | **MATCH** |
| 9 | do-nothing control `entries=0 …`, exit 1 | same command, `--lane /tmp/r29a2r-calibration/base` (baseline `corpus/` extracted) | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped`; exit `1` | **MATCH** |
| 10 | unrun census is a failure | same command without `--census` in the live lane | `… usedby_ok=1 census=skipped`; exit `1` | **MATCH** |
| 11 | adopted rows carry `180d`, due 2027-04-23, so `overdue` is clean | `date -d "2026-10-25 +180d"`; `grep -cE '\| 2026-10-25 \| 180d' corpus/SOURCES.md`; `scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin --today 2026-10-25 kengaku` | `2027-04-23`; `6` rows (S077–S080, S090, S091); overdue: cadence lines only, `0` overdue rows, exit `0` | **MATCH** |
| 12 | pre-repair overdue blast radius (correction 1) | `scripts/sources-census.sh overdue --today 2026-10-25 --file <registry @8cf7b60>` | 5 rows `overdue … 0d recheck=2026-10-25 opened=2026-10-25` (S077–S080, S090), exit `1`; the same registry was `81` rows with `recheck == opened == 2026-10-25` | **MATCH** as behaviour |
| 13 | "(round28_census overdue 0 → 1)" (LOG.md correction 1) | `grep -n overdue plans/round28_census.py`; `python3 plans/round28_census.py --revision 6baa3090` | the script has **no** overdue field (only a `corpus/SOURCES.md` read at `:39`); its output contains no `overdue`; exit `0`. The `overdue` mode belongs to `scripts/sources-census.sh` (`:35-36`); pre-repair the count is **5 rows**, the `1` is the exit code | **MISMATCH** (wrong instrument, unit conflation) |
| 14 | strict gate refuses: exit 3, 2 escaped-pipe rows + 6 collisions | `python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package $PKG` (landing tree, output redirected to file) | `registry=82 staged=173 collisions=6 malformed=2 duplicates=0 defects=167 prose=167` / `collisions: S077 S078 S079 S080 S090 S091` / `malformed: S093:escaped-pipe S101:escaped-pipe`; exit `3` | **MATCH** |
| 15 | scoped append passes on the pre-append registry, exit 0 | `… --admit-ids S077,S078,S079,S080,S090 --entries corpus/knowledge/benchmark-task-validity-checklist.md --access-date 2026-10-25 --scope-to-admit --out …` (registry `REG76`) | `registry=76 staged=173 collisions=0 malformed=0 duplicates=0 defects=0 prose=5`; exit `0`; written block columns `opened=2026-10-25`, `recheck=180d` ×5 | **MATCH** |
| 16 | re-append of the five landed ids: `collisions=5`, exit 3 | same with `--scope-to-admit` against the landed registry | `registry=82 … collisions=5` / `collisions: S077 S078 S079 S080 S090`; exit `3` | **MATCH** (scoped). Unscoped the same ids give `collisions=6` (adds S091), exit `3` |
| 17 | "171 prose `recheck` cells" (lessons:181, still at `30ee3b5`) | `parse_rows($PKG)` + `row_defects`, and the strict run's `prose=` counter | `parsed 173 bad 2 prose 167`; strict line `defects=167 prose=167`. At the **freeze** revision the tool printed `defects=171` — 171 was the pre-repair **total defect** count, not prose cells | **MISMATCH** |
| 18 | "168 uncited rows and 64 uncited entries" not appended | `173 − 5`; `python3 -c "len(json.load(open(MERGE-REPORT.json))['entries'])"` | `168`; `65` entries in the package − 1 admitted = `64` | **MATCH** |
| 19 | 92 root entries = 89 task dirs + 3 files (S079 / M94) | `curl -sL codeload…/terminal-bench-2/tar.gz/2fd12b88…` then count first path components and dir/file split | `92` top entries; `dir 89`, `file 3` (`.gitignore`, `LICENSE`, `README.md`) | **MATCH** |
| 20 | 108 task directories plus one `task_conflict.json` (S080 / M94) | same for `hkust-nlp/Toolathlon@9be8d8fe`, path `tasks/finalpool` | `109` entries; `dir 108`, `file 1` = `tasks/finalpool/task_conflict.json` | **MATCH** |
| 21 | pinned bytes/hashes per source row | `curl … \| wc -c`, `sha256sum` on S077/S078/S080/S090 raw URLs | `41842 b0a7cb14`, `6858 dde4168f`, `16883 d06165b5`, `53390 cbc50108` — all as claimed | **MATCH** |
| 22 | every anchor quote is a byte substring and ≤25 words | substring test + whitespace word count on the 7 quoted spans (incl. S091 arXiv abs) | 15, 4, 3, 8, 9, 18, 11 words; all present verbatim | **MATCH** |
| 23 | S090 upgraded from the package's tier B to registry A | `awk -F'\|' '{print $5}'` on `$PKG` vs `corpus/SOURCES.md` for S090 | package `B`, registry `A` | **MATCH** |
| 24 | fleet source census exit 0, 14 cross-scope duplicate-URL warnings retained | `scripts/sources-census.sh validate` (fleet) and `… kengaku` | exit `0`, `0` E-codes; `14` `kengaku W04` lines (fleet-wide `319` — the 14 is the lane's, not the fleet's); `census-after.txt` also ends `kengaku ok` | **MATCH** (wording: the 14 is lane-scoped) |
| 25 | `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1`, PASS, exit 0 | landing tree and live lane | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline`; exit `0` | **MATCH** |
| 26 | `round28_census.py --revision 6baa3090` exit 0 | live lane | exit `0` | **MATCH** |
| 27 | `config_projection.py --summary` → `TOTAL findings=0 exit=0` | live lane | `TOTAL findings=0 exit=0`, exit `0` | **MATCH** |
| 28 | one 36-seat wave, band 32–64, role composition | `.ufo/waves/round-29/attempt2/build-dispatch.json`; `swarm-registry.json` role histogram; `scripts/hyaku/ufo-wave-policy.json` | `counts: spawn 36 resume 0 total 36`; `scout 10, reviewer 10, scribe 3, executor 3, critic 3, connector 2, simplifier 2, mutation-tester 1, revenger 1, sentinel 1` = 36; `waveMinLanes 32, waveMaxLanes 64`; wave id `kengaku-r29a2-build` | **MATCH** |
| 29 | 14 attack seats (39%) | role histogram | `reviewer 10 + critic 3 + mutation-tester 1 = 14` → `38.9 %` | **MATCH** under that role set; `16 (44 %)` if sentinel+revenger are counted as attack |
| 30 | selftest kills the mutants, incl. the two first-pass survivors | frozen revision: 10-case suite; each single-edit mutant copied to `/tmp` and run | freeze revision: M2 (`<` columns) `failed=0 exit 0`, M3 (any nonempty recheck) `failed=0 exit 0` → the two survivors reproduce; landing revision: M2→`escaped-pipe-refused`, M3→`missing-requested-id`, M1/M4/M5 as documented, plus `anchor-column-zero`→2 cases, `no-recheck-normalize`→`prose-recheck-normalized`, `drop-dupe-check`→3 cases — **every** mutant dies, exit 1 | **MATCH** |
| 31 | "five mutants … including the two survivors" (SCORECARD C2) vs "four mutants re-run after the fix" (LOG correction 4) | mutation report `R29a2FixtureMutations.md` + the seven probes above | five mutants ran (M1–M5), two survived, all five die now; the four named in correction 4 also all die | **MATCH** on substance; the 5-vs-4 numbering is an internal count mismatch, not a false claim |
| 32 | `coverage 7 → 7 held`, `operability 8 → 8 held` (+ depth 9, novelty 7, freshness 8, adjacency 8, calibration 8) | — | no command emits an axis number; the prior state *is* recorded (`SCORECARD.md` r28 table: `coverage 7`, `operability 8`, `calibration 8`). Their stated premise does re-derive: `test -e` on three capped surfaces → exit `1`/`1`/`1` (bounties telemetry, llm-wiki, bench-arena all absent) | **NOT DERIVABLE** (judgment); premise **MATCH** |

**Totals:** 32 rows — 26 MATCH, 5 MISMATCH (#3, #4, #13, #17 and, as a count, #31's 5-vs-4),
1 judgment-only (#32).

---

## 2. Claims no command can re-derive

1. **The two score verdicts** — `7 → 7 held` (coverage) and `8 → 8 held` (operability), and the
   "other axes held" list. Axis scores are rubric judgments; nothing in the tree converts a run to a
   number. What *is* checkable is the prior state they claim to hold from (r28 table) and the cap
   premise (F8 below).
2. **"No dead seats."** The dispatch record holds `spawn 36 / resume 0` and the registry holds role,
   axes and milestone per seat — no per-seat completion status. Seat yield is unrecorded in the
   committed round artifacts (the later `5fd54a4` adds a fleet-level `yield.tsv`, outside this lane).
3. **The safety/locality paragraph** — "`shokuknow/` was read only (no campaign tool run, no write,
   no fetch, no push); the fleet root, sibling lanes and `.ufo/state` untouched; the lane's own new
   bytes carry no credentials." Absence of action is not a byte artifact; the corpus half is
   partly checkable (`git grep`-scoped credential scan) and I did not run one.
4. **"No pacman or tool installs."** Process claim with no committed receipt.
5. **"21 files" / "ten-case selftest" style line-location claims** in the sources table ("line 95",
   "line 99", "byte 43351", "line 27"): the quotes re-derive as substrings with the claimed word
   counts, but the line/byte offsets were not independently recomputed here.
6. **Residual, from #13**: the parenthetical "`round28_census` overdue 0 → 1" is re-derivable in no
   reading — the instrument does not exist; only the behaviour (5 rows, exit 1) is.

---

## 3. Findings

**F1 (MAJOR — calibration). `SCORECARD.md:994` still states "Registry 76 → 81 rows" while the landed
registry holds 82.** Measured at the ticket's landing commit and again at `30ee3b5`
(`grep -cE '^\s*\| *`?S[0-9]{3}' corpus/SOURCES.md` → `82`). The same round's own
`LOG.md:697` says "82 rows (S001–S080 + S090 + S091), tiers A 76 / B 4 / C 2" and
`LOG.md:724` item 10 records "Counts corrected in the lesson: registry 76 → 82"; `lessons:205` was
repaired to 82/A76 in `4b82ff7`. The C1 row of the **score-bearing** table is the one surface left
uncorrected, and its "counting command" column cites a counter that never prints a registry row count,
so a reader cannot see the discrepancy from the cell itself.

**F2 (MAJOR — same defect, body text). `LOG.md:641`** ("Registry 76 → 81 rows (5 tier-A additions…)")
contradicts the appended correction 24 lines below it in the same file, and the corrections paragraph
is presented as append-only history, so the body is not marked stale.

**F3 (MEDIUM — count unit). `corpus/lessons/round-29.md:181` "171 prose `recheck` cells" is 167.**
`python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package $PKG` → `… defects=167 prose=167`;
direct `parse_rows` count → `prose 167` (`173` parsed rows, `2` malformed escaped-pipe). The 171 comes
from the pre-repair tool's total-defect line (`defects=171` at `8c14a5d`), i.e. a different quantity
from a superseded revision. This is the same class as M94 (wrong unit) inside the section that
documents M94.

**F4 (MEDIUM — instrument attribution). LOG correction 1 names `round28_census.py` as the overdue
instrument.** `grep -n overdue plans/round28_census.py` → no match; the script reads
`corpus/SOURCES.md` for its own metrics and prints no overdue field. The re-derivable instrument is
`scripts/sources-census.sh overdue …` (header `:35-36`), which at `8cf7b60` reported **5** overdue rows
at `0d` and exit `1`, not "0 → 1". The repair itself is correct and verifiable (`overdue` → 0 rows,
exit 0 at `ff476d0`); only the citation is wrong.

**F5 (LOW — index completeness). `corpus/README.md`'s `evidence/round29-attempt2/` table indexes 5 of
the 10 committed files.** Unindexed: `gate-strict.txt`, `gate-scoped.txt`, `control-nocensus.txt`,
`adopted-block.md`, `round28-census-after.txt` — two of which the LOG correction cites by path as the
round's decisive receipts. The lane's own coverage rubric counts index both directions
(`SCORECARD.md:247`), so this is a live index gap, not cosmetics.

**F6 (LOW — receipt reproducibility). `corpus/evidence/round29-attempt2/adoption-gate-run.txt` records
`registry=81`,** which cannot be regenerated from the landed tree (registry 82); the same refusal is
still re-derivable as `collisions=6` unscoped / `collisions=5` scoped, exit 3. Also,
`adoption_check.py --census` is **path-dependent**: run in an extracted copy of the landing tree it
prints `… census=fail`, exit `1` (lane name derived from the directory name), so the C1 line is only
reproducible in place. Worth labelling in the receipt, since a copied tree silently fails the claimed
line. Same class: the frozen control receipt `.ufo/waves/round-29/attempt2/control.nothing.txt` records
**eight** fields (`… usedby_ok=0 verified_at=0 census=skipped`), so the current seven-field counter
reproduces it only semantically (M99 is the correct account of why the printed set changed; the
receipt was not re-stamped).

**F7 (INFO — drift under audit).** HEAD advanced from `ff476d0` to `30ee3b5` during this seat
(`4b82ff7`, `7bc2aaf`, `c88310f`, `30ee3b5`, all 2026-10-25). At `30ee3b5` the scoped append now
refuses staged rows whose `opened` cell is not the access date unless `--attest-opened` is passed, so
LOG correction 2's "(exit 0 on the pre-append registry)" no longer reproduces without the new flag;
the strict refusal (`exit 3`, 6 collisions, 2 malformed, 167 defects) and the selftest (`10/0`,
exit 0) still reproduce. Anything a reviewer measures against "HEAD" today is not the state the
attempt's table describes.

**F8 (INFO — verdict premises hold).** The `coverage 7` hold rests on three declared-but-unresolvable
surfaces; all three re-verify absent: `test -e ~/Projects/bounties/ledger/telemetry.jsonl` → 1,
`…/webzites/repos/llm-wiki` → 1, `…/bench-arena` → 1. So the *capped* half of the verdict is
evidence-backed even though the number is a judgment.

---

## 4. Residual risk and verification gaps

- **Not re-derived:** line/byte positions of quoted anchors (only substring + word count); S079's
  973-byte `task.toml` digest; the 13-row/35-path registry population; anything about the campaign
  register outside this lane; the absence half of the safety paragraph.
- **Sampling:** 4 of 5 raw-source byte/hash pins were re-fetched (S091 is a rendered page, checked for
  substring only). All matched, so the pin discipline holds as sampled, not as proven for every row.
- **Judgment vs evidence:** the two verdicts cannot be promoted or demoted by any command; this seat
  can only say their premises are sound and their recorded prior state is consistent with r28.
- **Concurrency:** the tree changed four times during the audit. Verdicts marked `ff476d0` are stable;
  the F7 note is a snapshot taken at `30ee3b5` and may already be stale.
- Not an admission: this is a recommendation only.
