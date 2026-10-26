# R38R37Integrate — round-37 wave-2 integration ledger (kengaku round 38, wave 1, routed D1)

Seat: `R38R37Integrate` (scribe, leaf). Date: 2026-10-26. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(read-only; no lane file, index or jj state touched). Fleet root: `/home/vgpnk/Projects/shokunin`.

Assignment: routed D1 — `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` §5
item 1: "*`.ufo/waves/round-37/falsify/` (19 reports at closure, seats still live) is untracked. Commit it under the
round-38 entry and integrate its findings*". Produce one row per report (seat, VERDICT, strongest finding with
`file:line`, disposition) and draft the LOG and lesson text summarising wave 2.

Axes (godspeed): **calibration** (every cited line opened here, not copied from the report), **quality** (one row per
seat, dispositions that a later round can act on). No axis move is claimed for a line I did not open.

## 1. Coverage, inputs, method

| check | command | observed |
|---|---|---|
| seat count vs dispatch | `python3 -c` over `.ufo/waves/round-37/falsify-spec.json` items vs `os.listdir('falsify')` | `spec items 37`; `missing reports: []`; `reports without spec item: []` |
| report count | `ls .ufo/waves/round-37/falsify/*.md \| wc -l` | `37` |
| every report ends on its verdict | for each `*.md`: last non-blank line starts `VERDICT:` | `nonconforming=0 of 37` |
| last write by any seat | `ls -lt --time-style=full-iso .ufo/waves/round-37/falsify/*.md \| head -1` | `F37MutAttribution.md` `2026-10-26 02:37:19.256770772 -0300` |
| inventory taken | `date -u` at read time | `2026-10-26T05:46:23Z` (= 02:46 −03) — i.e. no seat was writing for ~9 min before the inventory |
| committed at the tip | `git log -1 --format='%H %cI %s' -- .ufo/waves/round-37/falsify/` | `21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9 2026-10-26T02:38:25-03:00 round-37: wave-2 reports and results (37/37), outcome…` |
| files tracked there | `git ls-files .ufo/waves/round-37/falsify/ \| wc -l` | `380` (reports + receipts + result dirs) |
| lane tip at read time | `git log -1 --format='%H %cI %s'` | `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e 2026-10-26T02:42:21-03:00 round-38: wave-1 build spec and validated dispatch…` |

Consequences for the assignment's own framing, stated because they change what D1 still owes:

- **D1's commit half was already done** by `21e6251` (37/37 reports, 380 files, 2026-10-26T02:38:25-03:00) — 66 s
  after the last report was written. D1 was filed at closure when 19 reports existed; the wave finished.
- **No seat is still writing.** All 37 reports predate the commit by seconds and the inventory by ~9 min.
- What remains of D1 is exactly this report: the integration half. The wave's authoring table
  (`inventory.tsv`) and the drafts (`log-draft.md`, `lesson-draft.md`) sit beside this file.

Method: every report was opened; header + VERDICT + every findings / mutants / survivors / isolation region was
read; 12 reports were read end-to-end (`F37MutAnchorTool`, `F37MutProbeCases`, `F37ReopenRows`, `F37RevBatteryCode`,
`F37ScoutMisroot`, `F37CritC2Map` §75-181, `F37NoHarmSweep` §1-3, `F37CritRenamed` §1-2/§7, `F37XMutD4`, `F37XMutD5`,
`F37XMutP910`, `F37CritOverfit`). **Every target line cited in the table below was opened in the lane by this seat**
(20 checks, transcript: `R38R37Integrate/verification-transcript.txt`); no cited number is transcribed from a report
without that check or is labelled `[REPORT]`. No counter was re-run by this seat.

## 2. One row per report (37/37)

`report:line` = the finding statement inside the wave-2 report; `→ target` = the lane line the finding is about,
opened here. Disposition vocabulary is the assignment's four states; "no defect" collapses to *refused with reason:
nothing to route* and "closure consumed it" to *already-closed by round-37 closure*.

| # | seat | VERDICT (report:line) | strongest finding (report:line → target, verified) | disposition |
|---|---|---|---|---|
| 1 | F37AnchorRerun | `anchor-before-5-after-0-mutants-3/4` (:109) | anchor test is membership in **one global set**, so a row may carry another row's real digest: `allowed = set(files) \| set(manifests)` (:82 → `plans/anchor_digest_check.py:200`) | **closed-by-round-38-item R38AnchorBind** — draft binds each token to the capture its own row names; tip receipt `rows=107 tokens=15 defects=0` / `EXIT=0`. Its F37A-2 (index-mode manifest mint) is **routed-to-round-39** (draft reads index blobs; a staged fabricated `SHA256SUMS` line is not shown refused either way) |
| 2 | F37C1Rerun | `c1-rerun-pass-killed-55/55` (:198) | predicate is safe only because the battery **path** is fixed; an arbitrary hostile battery passes with `ATTRIBUTED 6/55` (:173) | **closed-by-round-38-item C1 counter** (`plans/round38_c1_verify.py`: `PINS total=14`, attributed kill rule, sidechannel scan; claims §C1 Limits name it) |
| 3 | F37C1RerunPy313 | `c1-rerun-interpreters-same` (:105) | no defect: 9 runs byte-identical (`sha256 651bcf54…`); the instrument is order-insensitive **by construction**, so these axes cannot move it (:76) | **already-closed by round-37 closure** (§1: the measurement transfers) — nothing new owed |
| 4 | F37C2Rerun | `c2-rerun-pass-probe-byte-equal-yes` (:162) | V7 cannot see `partly`→`enforced`, because the rule is one-directional (:110 → `plans/round37_c2_verify.py:196-197`, opened) | **closed-by-round-38-item C2 counter** — round-38 V7 derives the label from *all* violating cases (`plans/round38_c2_verify.py:241-247`, opened). N1 (`bytes=` is a character count, `pkg_gate.py:285`, opened) and N3 (`uv`+biopython) → **routed-to-round-39** |
| 5 | F37ConnCrossCheck | `crosscheck-unaddressed-20` (:181) | 20 wave-1 findings with no landed citation; `grep -rln` over SCORECARD/LOG/lesson/SKILL/PROVINCE → no output (:90) | **routed-to-round-39** — the D2/D3/D4 families inside the 20 are closed by `R38MapErratum`/`R38AnchorBind`/`R38LedgerTip`; the V1/V4/V5/V6/V7-internal items (#3-#11 of its list) survive by construction in the round-38 counter |
| 6 | F37ConnSiblingCite | `sibling-cite-3-gaps` (:130) | tameshi bwrap defect-probes and kumitate `cap-run.mjs` uncited in every round-37 surface (:109) | **closed-by-round-38-item R38SiblingCite** (dir exists, empty at 05:46Z → verdict pending) + `R38ConnSibling` |
| 7 | F37CritC1Axis | `c1-axis-calibration-unadvertised-6` (:200) | 6 of 55 mutants (M34–M39) advertise nothing, so the calibration count is 44, not 50 (:9 → `plans/round-37-claims.md:19`, opened: `… no fixture demonstrates, 50 → 0`) | **routed-to-round-39** for the round-37 count; the method (per-item `adv` cell) is **closed-by-round-38-item R38CritClaims** |
| 8 | F37CritC2Map | `req-map-2/4` (:181) | line 9 row says `enforced` while a line-9-violating state passes; line 8 row cites `catch-all-200`, which satisfies the line as written (:110 → `corpus/knowledge/tb2-git-webserver-grader.md:107`, opened) | **closed-by-round-38-item R38MapErratum** (+ `R38MapRetro` drafts both rows; V7 stays green either way per the seat) |
| 9 | F37CritC2Overclaim | `overclaims-13` (:226) | F8: "was not executed" for the oracle is contradicted by `corpus/lessons/round-37.md:27` inside the same corpus (:144) | **routed-to-round-39** (F1/F2 closed by `R38MapErratum`; F3–F13 are entry prose, append-only errata next round) |
| 10 | F37CritCalibStatements | `statements-60-mismatches-3` (:168) | M2: the lesson quotes `defects=3/1 … WRONG` from a receipt that now reads `defects=3/3 … ok` (:134 → `.ufo/waves/round-37/build/R37AnchorSweep/fixture-receipt.txt:26,32`, opened) | **closed-by-round-38-item R38LessonDraft** (M2/M3); M1 (LOG provenance) → **R38ScorecardDraft** |
| 11 | F37CritNoHarmDiff | `no-harm-removed-lines-0` (:171) | landing ships `SKILL.md:608-610` calling a green tool "a red state" at "lane tip `44b7298`", five commits before the tip (:61 → opened) | **closed-by-round-38-item R38PkgProse** (SKILL addendum draft, pending); F2/F3 (missing supersede markers, unrecorded retraction) → **routed-to-round-39** |
| 12 | F37CritOverfit | `overfit-gate-matches-cues-2` (:130) | `BATTERY … wrong=0` carries no class information; a 2-cue lookup reproduces it, declarations are transcribed from the gate (:60) | **routed-to-round-39** (documentary sentence in counter docstring + claims `Battery:` bullet) |
| 13 | F37CritRenamed | `renamed-run-weak-cues-5` (:205) | a gate that recognises the genuine fixture by content prints the full `PREDICATE C1 pass` — the renamed run varies one path component (:47) | **routed-to-round-39** (extend the observable to clause-status lines; the seat's §7 priced it at ~15 lines) |
| 14 | F37MutAnchorTool | `anchor-tool-mutants-1/5` (:43) | the frozen pair is verdict-shaped, not class-shaped: M1 survives while `digest-short detail=63-hex` degrades to `digest-unknown` (:34) | **routed-to-round-39** — `R38AnchorBind` changes the binding rule but adds no class-sensitive assertion; M4's unverifiable-erratum axis is removed by the per-row binding |
| 15 | F37MutAttribution | `attribution-mutants-1/4-residual-1` (:131) | a counter-clean fixture that conditions on the running gate's bytes re-sources three attributions with `ATTRIBUTED 55/55` unchanged (:58) | **closed-by-round-38-item C1 counter** for the `/proc` shape (the frozen sidechannel token scan, claims §C1); a path- or bytes-based oracle without those tokens is **routed-to-round-39** |
| 16 | F37MutC2Counter | `c2-landed-mutants-10/10` (:130) | V4 never cross-checks `match=` against `predicted=`/`observed=` (:119) | **routed-to-round-39** — round-38 V4 still reads `match=NO` text (`plans/round38_c2_verify.py:171`, opened) |
| 17 | F37MutProbeCases | `probe-case-mutants-14/14` (:75) | no defect: 12/12 verdict-flipping mutants flipped exactly at their target case; K3/K14 receipt-insensitive by design (:56) | **refused with reason: no defect — nothing to route** |
| 18 | F37NoHarmSweep | `no-harm-29/30-new-red-1` (:219) | `ledger-tip` red in the mandated clone shape: `rows=9 closed=9 observed_pass=7 mismatches=2`, both from `BRANCH = "refs/heads/master"` (:78 → `plans/defect_ledger.py:29`, `plans/round36_c1_verify.py:38`, both opened) | **closed-by-round-38-item R38LedgerTip** (D4). N2 (`--work` must pre-exist; absence exits 1) → **routed-to-round-39** |
| 19 | F37ProbeOnTip | `probe-on-tip-byte-equal-adversarial-3/3` (:285) | a host without Bio and without network turns P10 into a *rejection* (exit 1) though the docstring reserves 2 for setup (:229) | **routed-to-round-39** (frozen gate); F2 (`bytes=` label) same as #4 N1 |
| 20 | F37ReopenRows | `rows-3/3-quotes-3/3` (:53) | no defect (3 digests, 3 quotes, 3 Gate rows live-fetched); one span note: entry says `lines 1–92`, `verify.sh` has 91 (:45; both sides opened) | **already-closed by round-37 closure** §2 (evidence re-open consumed). The span note → **routed-to-round-39** (append-only errata) |
| 21 | F37RevBatteryCode | `battery-code-0-defects` (:170) | no defects across 6 axes; N2 = P10's host dependency (:152) | **refused with reason: no defect**; N2 duplicates #19 → **routed-to-round-39** |
| 22 | F37RevEntryQuotes | `entry-quotes-29/32-claims-4-unsupported` (:51) | F6: the documented recheck `sha256sum -c …/SHA256SUMS` prints 6× `FAILED open or read` from the lane root (:21) | **routed-to-round-39** (entry prose; append-only) |
| 23 | F37RevLesson | `lesson-5-defects` (:57) | D2: spot-check item 6 ("the S110 63-hex cell must be gone") is unfulfillable under append-only rule 2, and the cell is still 63 hex (:29 → `corpus/lessons/round-37.md:102`, `corpus/SOURCES.md:125`, both opened) | **closed-by-round-38-item R38LessonDraft** (plus errata); D1/D3/D4/D5 same item |
| 24 | F37RevProvinceErrata | `province-errata-1-defects` (:197) | `corpus/knowledge/tb2-regex-log-grader.md:298`: "a superset of the two rows below" has no literal-true reading (:155) | **routed-to-round-39** (append-only erratum) |
| 25 | F37RevQuality | `quality-6-defects` (:170) | Q27 omits the gameability/attribution limit the same round demonstrated (:62); F2 counts "55 fixtures" where the battery has 64 (:93 → `corpus/QUALITY.md:445`, opened) | **routed-to-round-39** for the Q27 text (the derived-label re-run it needs is `R38MapRetro`, in flight) |
| 26 | F37RevScorecardLog | `scorecard-log-2-defects` (:57) | the SCORECARD/LOG round-37 sections cite `build/` receipts that were uncommitted at the reviewed tip (`git ls-tree … \| wc -l` → 0) (:45) | **closed-by-round-38-item R38R37Integrate** (this ledger + `21e6251`); D2 (`grader.py` freshness) → **R38ScorecardDraft** |
| 27 | F37RevSkillReadme | `skill-readme-1-defects` (:138) | the `ledger-tip` row's declared green state is unreachable on a clean clone; both mismatches are ref artifacts (:28) | **closed-by-round-38-item R38LedgerTip** (same defect as #18, independent seat — two seats, one root cause) |
| 28 | F37ScoutMisroot | `misroot-1-scratch-leftovers-22` (:70) | 0 seat-written strays at the fleet root; 22 `/fast/scratch/hyaku/kengaku-r37/` dirs were **live peers**, plus one stray `/tmp/r37close-src.*` (:29) | **refused with reason**: fleet-root and `/tmp` hygiene is operator-owned; the 22 dirs were in-flight seats, not leftovers, and nothing in the lane changes |
| 29 | F37XMutD4 | `extra-mutants-d4-killed-2/4` (:113) | X3 (`patterns[:-1]`: last directional pattern unchecked) and X4 (`re.IGNORECASE`) survive (:39) | **closed-by-round-38-item R38BatD4** (N19, N20; receipt opened: `MUTANTS total=2 killed=2 survived=0`) |
| 30 | F37XMutD5 | `extra-mutants-d5-killed-2/4` (:196) | X3 (manifest pin on the first row only) and X4 (20-char quote prefix) survive; `d5.py` has no accept-side fixture (:121) | **closed-by-round-38-item R38BatD5** (N21, N22; module drafted, no receipt at 05:46Z); the missing accept side → **routed-to-round-39** |
| 31 | F37XMutP23 | `extra-mutants-p23-killed-3/4` (:166) | X2 `>=`→`>` on `min_distinct_locations` survives 0/64 (:43) | **closed-by-round-38-item R38BatP3** (N02, the mirror direction; `counter-n02.txt` present at 05:46Z). Its Y3 (`min_quotes` equality, live) → **routed-to-round-39** |
| 32 | F37XMutP4 | `extra-mutants-p4-killed-1/4` (:172) | X2 (first quote only) and X4 (whole capture, not the cited lines) survive; X3 is equivalent at clause granularity (:49) | **closed-by-round-38-item R38BatP4a** (N03, N04) + **R38BatP4b** (N05, N06) |
| 33 | F37XMutP5 | `extra-mutants-p5-killed-2/4` (:128) | X1 (first registry row only) and X4 (off-pin check shadows unpinned) survive (:34) | **X1 → closed-by-round-38-item R38BatP5** (N07). **X4 is not in N01–N22** and survives the round-38 battery too → **routed-to-round-39** |
| 34 | F37XMutP6 | `extra-mutants-p6-killed-2/4` (:164) | X1 (`min_teaches_words - 1`) and X4 (scheme-blind URL compare) survive; both proven real, not equivalent (:39) | **closed-by-round-38-item R38BatP6** (N09, N10) |
| 35 | F37XMutP7 | `extra-mutants-p7-killed-3/4` (:200) | X4 survives **and the gate itself** accepts an emptied recheck line, because `\s*` at `pkg_gate.py:224` crosses the newline (:121) | **closed-by-round-38-item R38BatP7** for the branch (N11, N12); the gate's `\s*` crossing is a real defect that N11 cannot demonstrate → **routed-to-round-39** |
| 36 | F37XMutP8 | `extra-mutants-p8-killed-4/4` (:156) | 4/4 killed; the mirrored half S1 survives but is documented as *not* a battery hole (:69) | **routed-to-round-39** (the P8 index branch has no N id this round) |
| 37 | F37XMutP910 | `extra-mutants-p910-killed-4/4` (:149) | three P10 weakenings survive; no round-37 fixture ever lets P10 pass (:50) | **closed-by-round-38-item R38BatP10a** (N13, N14) + **R38BatP10b** (N15, the accept-side mirror) |

### Tally (primary disposition)

| disposition | n | seats |
|---|---|---|
| closed-by-round-38-item | 20 | 1, 2, 4, 6, 8, 10, 11, 15, 18, 23, 26, 27, 29, 30, 31, 32, 33, 34, 35, 37 |
| routed-to-round-39 | 12 | 5, 7, 9, 12, 13, 14, 16, 19, 22, 24, 25, 36 |
| refused with reason | 3 | 17, 21, 28 (all "no defect" / out-of-lane) |
| already-closed by round-37 closure | 2 | 3 (§1), 20 (§2) |
| **total** | **37** | |

## 3. Routed items D1–D7 → where each one now stands

| item | what it asked | round-38 item | evidence state at 05:46Z (observed, not asserted) |
|---|---|---|---|
| D1 | commit + integrate wave-2 outputs | `R38R37Integrate` | commit done by `21e6251` (380 files); integration = this file; `inventory.tsv` + drafts written |
| D2 | map overstates enforcement; derivate labels from *all* violating cases | `R38MapErratum`, `R38MapRetro` | V7 derives and requires cited cases to violate (`plans/round38_c2_verify.py:241-247`, opened); drafts `map-corrected.md`, `run-ablation-cited-rule.txt` present |
| D3 | anchor must bind to the capture the row names | `R38AnchorBind` | draft `anchor_digest_check.py` + `receipts/run-tip-new.txt` → `rows=107 tokens=15 defects=0`, `EXIT=0` |
| D4 | `ledger-tip` red in detached-HEAD clones | `R38LedgerTip` | dir created, empty at 05:46Z; `plans/defect_ledger.py:29` still `refs/heads/master` in the lane (frozen until the landing) |
| D5 | add survivors to the frozen mutant list; attribute kills | `R38BatP1Run … R38BatD5` (12 seats, N01–N22) | 7 of 12 have a report; most have receipts; N19/N20 and N17/N18 receipts opened: `killed=2 survived=0` each |
| D6 | cite sibling prior art with file:line | `R38SiblingCite`, `R38ConnSibling` | dir created, empty at 05:46Z |
| D7 | C2 counter must pin its inputs; no informed-filler pass | frozen in `plans/round38_c2_verify.py` | docstring §PINS cites D7/R37CritC2Counter v4; `v5` re-checks probe and dry-table digests (`:191`); `v4` pins case ids against the frozen table (`:174`) |

The 14 N-mutants drawn from these reports (N02–N07, N09–N12, N19–N22) and the 8 that came from elsewhere
(N01, N08, N15 mirrors; N16 RUN; N17/N18 MAIN — `R37PlanNext` shapes B1/B2/B5/B6/B7/B8) match
`plans/round38_c1_verify.py:93-133` exactly; I re-derived the 13 non-frozen survivors + 1 diagnostic survivor
from the reports and got the same 14, with one excluded shape (see §6 I-3).

## 4. Defect families — read these once, not 37 times

| family | seats | root cause | status |
|---|---|---|---|
| **First-item-only / off-by-one in a loop or threshold** (the tournament's dominant class) | `F37XMutP4` X2, `F37XMutP5` X1, `F37XMutP6` X1, `F37XMutP23` X2, `F37XMutD4` X3, `F37XMutD5` X3, `F37XMutP7` X4, `F37XMutP910` L1/L3 | a check applied to one element or a boundary moved by one | 12 of these are now N02–N07, N09–N13, N14, N19–N22; P5 X4 and P8 S1 routed |
| **Loosened comparison** (case, scheme, prefix, whitespace) | `F37XMutP4` X4/X5, `F37XMutP6` X4, `F37XMutD4` X4, `F37XMutD5` X4, `F37XMutP910` L1 | a normalising compare standing in for an exact one | N04/N05/N10/N20/N22 frozen; P10 L1 = N13 |
| **Pass side never exercised (no mirror)** | `F37MutProbeCases` K3/K14, `F37XMutP910` :50, `F37XMutD5` :121, `F37CritRenamed` §2, `F37CritOverfit` §F1 | the battery only ever drives reject | N02/N08/N15 are the round-38 mirrors; D5 still has no accept-side fixture (routed) |
| **Predicate/observable too weak for what it is quoted as** | `F37CritRenamed` :47, `F37CritOverfit` :60, `F37C1Rerun` :173, `F37CritC1Axis` :9, `F37MutAttribution` :58 | `(rc, DEFECT set)` + transcribed declarations | routed (documentary + observable extension) |
| **Green state unreachable / precondition undeclared** | `F37NoHarmSweep` :78, `F37RevSkillReadme` :28 (`ledger-tip`); `F37ProbeOnTip` :229 (`uv`/Bio); `F37NoHarmSweep` :121 (`--work`) | a documented command that cannot be run as written | ledger-tip → `R38LedgerTip`; the other two routed |
| **Lesson / registry prose outruns its evidence** | `F37CritCalibStatements` :134, `F37RevLesson` :29/:33, `F37CritNoHarmDiff` :61, `F37RevQuality` :62, `F37RevEntryQuotes` :21, `F37CritC2Overclaim` :144, `F37RevProvinceErrata` :155 | a pointer or count that no longer reproduces | lessons → `R38LessonDraft`; SKILL → `R38PkgProse`; the rest routed |
| **Tool/environment coupling** | `F37C2Rerun` :110/:127, `F37ProbeOnTip` :229, `F37RevBatteryCode` :152, `F37RevSkillReadme` §1-3 | P10 needs `uv` + warm `biopython==1.85`; text-mode compares; hardcoded refs | `bytes=` label and `uv` dependency routed (gate frozen); refs → `R38LedgerTip` |

## 5. Conflicts and tensions — verbatim, for the canonical judge

No two seats contradict each other on a measured number. Four readings diverge; each is quoted with its
location and left unresolved here.

1. **Whether the receipt's text-mode compare implies byte equality.** `F37C2Rerun.md:110-112`: "a receipt
   rewritten with CRLF line endings would compare equal to the probe's LF output while the files differ
   byte-for-byte". `F37RevEntryQuotes.md:34` (opened): "does not weaken the entry's claim — decoded
   equality of two UTF-8 renderings implies byte equality". These cannot both be right about universal-newline
   translation; the entry's negative space inherits whichever holds.
2. **How much `PREDICATE C1 pass` buys, at the same tip.** `F37C1Rerun.md:173-177`: "The predicate is safe only
   because it fixes the battery path (`plans/battery37`)". `F37CritRenamed.md:47`: "a gate that recognizes the
   genuine fixture passes the frozen predicate". `F37CritOverfit.md:60-61`: "`BATTERY fixtures=64 wrong=0
   renamed_disagree=0` carries no information about the advertised defect classes." Reading: Renamed narrows
   Rerun (a fixed path is not sufficient), Overfit narrows the `wrong=0` half only. The round-38 claims adopt
   the narrowest form (attributed kills); the judge should treat round-37's `killed=55` as demonstrated-branch
   coverage, not calibration.
3. **The count of advertised-but-undemonstrated clauses at freeze.** `plans/round-37-claims.md:19` (opened):
   "advertised package-gate clauses that no fixture demonstrates, 50 → 0". `F37CritC1Axis.md:9` (opened):
   "**Answer: the axis is calibration, over-counted by 6.**" The seat's 44 is derived per mutant; the claim's
   50 is not. `corpus/QUALITY.md:445` compounds it with "55 fixtures" where the battery runs 64.
4. **Severity of `ledger-tip`.** `F37NoHarmSweep.md:78`: "Finding N1 (new red)" — counted as the one red among
   30 comparable entries. `F37RevSkillReadme.md:28`: "D1 (HIGH) — the declared green state is unreachable as
   documented". Same root cause, different objects (a counter-vs-script mismatch vs a row-vs-reality gap);
   the round-37 closure's D4 routes it as a fix, which is the stronger of the two readings.

## 6. Findings of this seat (integration-level; each opened here)

**I-1 (round-38-facing, medium) — the anchor checker's erratum exemption is hardcoded to round 37.**
`plans/anchor_digest_check.py:80` (opened): `ERRATUM = re.compile(r"^ {0,3}Erratum \(round 37\): (S\d{3,}) anchor
sha256\b")`. `F37RevProvinceErrata.md:171` already recorded it as an observation. Round 38 plans two append-only
errata (`R38MapErratum` for the git-webserver entry, whose rows S111–S113 carry anchors). Unless the pattern is
extended in the same landing, a round-38 erratum that corrects an anchor token will be invisible to the exemption
and the row will red — the failure is fail-closed, so it cannot launder, but it can flip a green check at landing.

**I-2 (claims-facing, low) — two round-37 counter limits survive into the round-38 counter unchanged, and the
frozen claims do not name them.** `plans/round38_c2_verify.py:171` still reads the receipt's own `match=NO` text
(`F37MutC2Counter.md:119`, `F37ConnCrossCheck.md` item 4), and `:195` still compares decoded text
(`F37C2Rerun.md:110`). Both are inside V4/V5, both are cheap to state as limits. The claims §C2 Limits list the
probe's limits, not the counter's.

**I-3 (calibration, low) — one non-frozen survivor did not become a round-38 mutant.** `F37XMutP5.md:37` (opened,
X4) moves `pinned.get(name) != row["sha256"]` ahead of `name not in pinned` so the off-pin branch shadows the
unpinned branch; it survives 0/64 and is not in N01–N22. The round-38 battery therefore cannot kill it, and no
frozen limit names it. Either it is a deliberate omission (state it) or a list gap.

**I-4 (inherited gate defect, medium) — `pkg_gate.py:224`'s `\s*` crosses the newline.** `F37XMutP7.md:121-160`
(opened): the unmodified gate accepts `recheck:` followed by nothing, because `^recheck:\s*\S` lets the next
heading's `#` satisfy `\S`. Round 38's N11 freezes this branch but cannot demonstrate the defect (a fixture with an
emptied recheck line prints `ok` on the reference, so it cannot be a `reject` fixture). The defect is real and
carried; the seat's witness (`WITNESS recheck-last-line-empty ref_rc=1 ref_defects=P7`) is the smallest safe fix.

**I-5 (process, low) — D1 is a recurring shape, not an incident.** Round-37's wave-2 directory was committed 66 s
after its last report; round-38's wave-1 directory is untracked at `2c5f4e0` right now (`git status --porcelain`
→ `?? .ufo/waves/round-38/build/`, `?? .ufo/waves/round-38/integrate/`, `?? plans/mutant_direction_check.py`). The
same commit-under-the-next-round-entry rule will be owed again; the lane has no mechanical check for it
(`F37ConnDefects` C4/C6/C9, `F37ConnCrossCheck.md:143-145`).

**I-6 (verified observation, informational) — `F37ReopenRows`'s span note is real and still live.**
`corpus/knowledge/tb2-git-webserver-grader.md:2` says "lines 1–92"; `wc -l corpus/evidence/round37/tb2-git-webserver/verify.sh`
→ `91`. Both opened. It is entry prose, so only an erratum may correct it.

## 7. Drafts for the L1 (paste-ready, not applied)

- `R38R37Integrate/log-draft.md` — LOG.md round-38 integration bullet set (D1 status, what returned, D1–D7
  disposition, carried-open list, the anchor-erratum risk).
- `R38R37Integrate/lesson-draft.md` — 10 `## Mistakes` rows for `corpus/lessons/round-38.md`, each citing the seat
  and line that established it, plus a "what wave 2 changed in the lane's own habits" paragraph.
- `R38R37Integrate/inventory.tsv` — seat / lines / bytes / mtime / `VERDICT` for all 37.
- `R38R37Integrate/verification-transcript.txt` — the 20 lane checks quoted in this report, with their outputs.

Wave 2 of round 37 in one paragraph (for the round-38 LOG, expanded in the drafts): 37 seats returned, 33 of them
with at least one defect, survivor or observation, 3 clean over their whole scope and 1 with no finding; they produced 13 non-frozen gate survivors plus one
diagnostic survivor, which are now the frozen round-38 mutants N02–N07, N09–N12, N19–N22; they confirmed the C1
and C2 predicates reproduce byte-identically across interpreters and under adversarial hosts, while bounding what
those predicates buy (content-recognisable fixtures, transcribed declarations, a one-directional label rule); and
they found the landing's prose defects (a map row stronger than its case, a lesson quoting an overwritten receipt,
a spot-check item that no legitimate fix can satisfy, a registry sentence describing a pre-tip state).

## 8. Limits, provenance, tooling

- **Read, not re-run.** No counter, probe, gate or battery was executed by this seat; every predicate number above
  is quoted from its report and labelled so. The only commands run were `ls`, `wc`, `sed`, `grep`, `git log/status/
  ls-files` (read-only) and one `python3 -c` over two JSON files.
- **Coverage of reading.** All 37 reports: header, VERDICT, findings/mutants/survivors regions. 12 end-to-end. 25
  reports' setup/evidence appendices were not read line by line; nothing in the table depends on them.
- **Verification of cited lines.** 20 target lines opened in the lane (`verification-transcript.txt`); report-internal
  line numbers resolved by `grep -nF` on the exact finding string (37/37 resolved, 5 spot-checked for content).
- **Not verified here.** Whether `R38BatD5`'s N21/N22 fixtures kill (no receipt at 05:46Z); whether `R38LedgerTip`,
  `R38SiblingCite` or `R38PkgProse` will land what their prompts ask (their dirs were empty when read); whether the
  round-38 C1 counter reaches `killed=22` (12 seats in flight).
- **Scratch.** None used: this seat needed no clone (read-only references only), so there is no
  `/fast/scratch/hyaku/kengaku-r38/R38R37Integrate/` to remove. No `TMPDIR` override was needed.
- **Writes.** `.ufo/waves/round-38/build/R38R37Integrate.md` and `R38R37Integrate/` (4 files) only. No lane file,
  index, jj state or fleet-root file touched; no git mutating command.
- **Tooling.** Nothing installed, upgraded or attempted; no pacman transaction (host policy paused), no `uv`/`npx`
  install needed — `python3` 3.14, `git` 2.56 preexisting were sufficient.

VERDICT: r37-falsify-integrated-37-reports
