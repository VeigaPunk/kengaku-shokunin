# CriticR83 — C2 calibration attack

Axes: calibration (record truth and evidence binding); coverage (C1/C2 causal separation, no extra coverage credit). Scores and admission remain the canonical judge's responsibility. This review changes no production bytes.

Frozen contract read in full: `plans/round-83-claims.md`, freeze `6f076679931367d540c3897a4eafa0eca752e1d4`; BASE `614f00559c75155ec100e945b3e8257b14fb7496`. Findings below concern checker SHA256 `1c2b9bf2e7abf5de9cfab85677813b750e3e8401763c6a2f5c1c18e191df0da4`, retained as `CriticR83/reviewed-round83_c2_checks.py`, not future revisions.

## Demonstrated counterexamples

### C83-CRIT-V6-UNBOUND-GATE — unrelated URL/quote passes

Counterexample: preserve original SOURCES rows, add correctly shaped rejected S270, and replace the Gate with one paragraph:

`S265 S266 https://example.invalid/unrelated 2026-11-04 :1 “unrelated invented quote”`

A correction paragraph `R82-V6 S265 and S266 omission corrected.` suffices. Actual S265/S266 locations and source quotes are absent. Executing candidate `v6` with the lane as read-only origin returned **exit 0, `CHECK v6 ok`**. Evidence: `CriticR83/forged-v6.json` (full fixture lesson, instrument hash, exit/stdout).

Cause: lines 123–128 select blank-line blocks, not individual Gate rows. Both ids, any URL, any short quote and any line locator may be unrelated. A whole Markdown table is one block, so S267's URL can license S265's missing locator.

Smallest safe correction: parse each id's actual Gate row independently; bind its location to the corresponding SOURCES source, access date and a quote at the retained capture's specified line. S265 is own-work: require its receipt path, not an unrelated external URL. For S266 bind the actual instruction URL(s) and retained instruction quote(s). Add this exact mutation to the battery. Impact: calibration evidence binding; fixable implementation defect, not a permissible tradeoff or a new predicate.

### C83-CRIT-V2-SYNTHETIC-CENSUS — warning ids masquerade as a full capture

Counterexample: create 27 lines with the correct W04 ids, but every warning body is `fabricated warning`; stamp `COMMAND bash sources-census invented`, the correct historical REV, `EXIT 0`, and `kengaku ok fabricated summary`. Candidate `v2` returned **exit 0, `CHECK v2 ok`**. Evidence: `CriticR83/forged-v2.json` contains the entire forged receipt and output.

Cause: lines 69–76 count known ids and accept broad command/summary regexes. They do not establish the required full historical validator output. Correct ids and a REV token do not prove provenance.

Smallest safe correction: reconstruct the documented historical command against exact `a44b2f083ee8b4115aea64598646f4bd9e3c1470` bytes, compare the full output including warning payloads and final summary modulo explicitly normalized scratch path, and bind command/exit. A separately pinned complete historical capture is also usable if validated against that run. Add fake-command and altered-warning-payload mutations. Impact: calibration/false provenance; fixable implementation defect.

## Eight base mismatches and executable repair requirements

Frozen source line map, derived from BASE: V1=161, V2=168, V3=173, V4=178, V5=182, V6=187, V7=192, V8=195. These actual lines—not section 5 or newest-file selection—must bind the routed rows.

| Id | Substantive BASE mismatch proved | Executable repair predicate / review result |
|---|---|---|
| V1 | Original S262 says 6 for `echo 1 > /logs/verifier/reward.txt` (4 whitespace tokens); S263 says 1 for `-w requests==2.32.4` (2). Original rows retained in base evidence. | Parse S268/S269 anchor quote/count pairs, recompute lengths, match actual retained source quotes, require supersede teachings and unchanged original rows, plus dated Gate/report correction. Candidate implements these, not bare corrected-number presence. |
| V2 | Historical report line 151 says after=26 and BASE has no after capture. Independent historical validator probe returned exit 0, **27 W04**, 28 stdout lines, using SOURCES plus all 83 needed historical paths at the exact revision. | Require full retained historical run, correct REV/COMMAND/EXIT, 27 real warnings and explicit supersession of 26. Candidate does not bind full output: demonstrated false green above. |
| V3 | LOG/SCORECARD say five while the historical affected list has six: SweepGateR82, SweepHarvestR82, ReviewerR82, CriticR82, MutationR82, RegistryCounterR82. Parsing BASE results independently gives 12 seats: **10 JSON-object outputs, 1 empty, 1 unstructured**. | Require affected=6, unrecovered=2, recovered=4, exact six identities, and receipt with source digest plus independently recomputed output categories. Do not label two outputs empty or infer provider events from absent final status fields. Candidate reads `r82-seat-counts.json`; current lesson names `r82-seat-census.json`: unify the actual installed receipt path and paragraph. |
| V4 | Per-file `git log BASE --diff-filter=A --format=%H` gives `82fe89d5dd29fa4c1bb8d85399d9e43442d1b862` for both tools, not c804dd41. | Candidate pinned addition-membership check plus correction naming both files is substantive. Historical membership already holds at BASE; the missing correction is the repair. Correction-only v4 passing is therefore expected, not a false green. |
| V5 | BASE README has no round82 lesson or round82 outside-review rows; round81 outside-review row has two cells. | Parse exact path rows, require exactly one three-nonempty-cell row each, not substring presence elsewhere. Candidate implements table cell counts; ensure rendered table membership, not an arbitrary standalone pipe line. |
| V6 | Historical round82 Gate omits S265/S266, and S264 teaches lacks required REJECTED/flip shape. | Preserve old rows, append rejected S270 with exact supersede teaching, and individually bind S265/S266 Gate locations/quotes/dates. Candidate false green demonstrated above. |
| V7 | Historical fleet report SHONEN box 1 says all ten have selftests. Reparsed ten exact BASE SKILL rows: seven declare, three `none declared`: round37-c1-attribution, round80-c1-remint, round82-c2-checks. | Recompute the ten selftest cells and require explicit seven-of-ten correction plus all exceptions. Do not count `--selftest` elsewhere in row text. Candidate reads cell 5 and names exceptions; no promotion to SHONEN `[x]` follows. |
| V8 | Fleet report says `~07:24Z`, before its own 09:26:48Z launch. The time meant local -03:00, hence ~10:24Z. | Require explicit local/Z correction, UTC round83 convention, and unchanged fleet report against fleet commit c839b658. Independent digest comparison succeeds; see authority receipt below. Do not require the report to exist in the lane repo. |

Evidence: `CriticR83/base-evidence.json`, `historical-census.txt`, `historical-report-preservation.json`. The census receipt uses validator `--file` and therefore labels its rows `file`; it is independent corroboration, **not** a proposed replacement for the canonical `kengaku`-labelled committed receipt.

## Required controls and sensitivity

Created two isolated BASE-byte fixtures, without cloning or git mutations:

1. Presence-only: eight closed rows with source bindings and canonical check commands, no substantive repair bytes. All v1…v8 return 1.
2. Correction-paragraph-only: same rows, entire current lesson including Gate/corrections, outside-review index marker, but original SOURCES/README lesson index and absent census/seat receipts remain. Results with proper read-only origin: v1/2/3/5/6/7/8 return 1; v4 returns 0 for the legitimate attribution correction. Thus this fixture cannot satisfy all eight checks. `CriticR83/controls-with-origin.json` retains each exit/stdout/stderr.

Initial attempts without origin produced unavailable-git reds for several checks; these are retained separately in `attack-attempts.json` and are **not** counted as substantive control evidence. Counter draft was absent at the control capture, so no end-to-end TARGET verdict or counter selftest is claimed. The exact two false greens above are check-level defects, not claims of full-target attainment. No general tests/build/lint were run.

Literal integration hazard: current checker requires exact strings such as `S262=4 S263=2`, `seven of ten new registry rows declare selftests`, and `07:24-03:00=10:24Z`, while the current lesson expresses several facts differently. Bind structured, id-scoped semantic correction content or coordinate exact evidence literals; do not weaken substantive checks to make prose green. Its paragraph splitter also combines adjacent list items into a single block: require each Vn's own bullet/section, so unrelated corrections cannot authorize a repair.

## Append-only, authority and separability

- Candidate immutability currently covers selected original source rows only (S262/S263 and S264/S265/S266). Frozen contract says **no old immutable SOURCES cell modified**. Compare all BASE source ids' immutable cells, not only five ids. This is a concrete enforcement gap from the reviewed code; no all-eight green mutation was claimed.
- Original historical report authority is **fleet repo** `/home/vgpnk/Projects/shokunin`, commit `c839b658102dbcc401c78bbb7ea3bb47f11a333d`, path `.ufo/reports/round-82/kengaku.md`. Current and committed SHA256 both `5a83443dc6544a76633ee42b90394cb1028a1abab18ee69ff54a4857758b0480`; byte-identical. Initial lane-only absence was resolved, not left as a blocker.
- Reviewed C2 checks import no C1 artifacts. Shared lesson contains C1 prose, but C2 must select only its named correction/Gate records. The frozen C1 predicate excludes C2 SOURCES/README/record changes; a full two-direction executable revert proof was unavailable because the counter draft was absent. Do not claim empirical separability from code inspection alone.
- Classification is calibration record-debt repair, not newly discovered model capability, novel method, or permission to increase coverage beyond cap 7. Seven-of-ten selftest correction and retained final output categories prevent premature saturation and false operability credit. Canonical judge alone decides claim admissibility; these findings are implementation repairs, not an alternate admission rule.

## Handoff

No production edits, no installs, no pacman, no delegation, no commits/index mutations, no fleet/domain writes. Scratch removed after preserving receipts. L1 should repair both demonstrated binding defects, resolve literal/path mismatches, then exercise the canonical after/base/sensitivity/selftest/mutant/control suite once against integrated tracked bytes.

Self-evaluation: accuracy 4 (observed outputs and pinned hashes; no end-to-end counter result); completeness 4 (all eight mismatches and two required controls covered; full counter unavailable); clarity 4 (finding-specific receipts and matrix, necessarily detailed); actionability 4 (minimal binding corrections and exact counterexamples; L1 owns implementation); conciseness 4 (machine receipts avoid embedding repeated payloads). Overall 4.0. Highest-impact improvement is the canonical integrated counter run after L1 applies the named fixes; no unsupported green is asserted.
