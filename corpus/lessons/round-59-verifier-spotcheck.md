# kengaku round 59 — non-author verifier spot-check (closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Round: kengaku lane-round 59, hyaku run 14. Lane base `e0cfa97ae8cae38dbd888963611ce9f2d9e3a3e8`,
head `bc9cd0737444a2925965a138c71112fb193c3328` (branch tip, pushed). Report:
`.ufo/reports/round-59/kengaku.md` (fleet repo, committed by the lane identity at `6772ec89`).
Dispatch digest: `2026-11-01T20:30:56-08:00 launch kengaku round=59 base=e0cfa97ae8ca (zcode
run14)`; `2026-11-02T00:47:03-08:00 complete kengaku round=59 head=bc9cd0737444 pushed=True`
(both lines verified present in `.ufo/watchdog.log`).

Method: the host note says the lane's frozen instruments run in WSL Ubuntu-24.04; no
CLOSURE-PREP artifact exists in the workspace, and WSL Ubuntu-24.04 IS available on this host
(python 3.12.3, bwrap 0.9.0, git 2.56.0, OpenSSL 3.0.13 — byte-for-byte the lane's declared
counter environment). The judge therefore RE-DERIVED on judge-owned clean clones at five
revisions (`tip`=bc9cd073, `e0cfa97ae`, `5420eac92`, `002cde8eb`, `e0512854a` under
`$HOME/kengaku-r59-judge/` in WSL, cloned from the lane repo read-only) and evidence-verified
committed receipts against those re-runs. Everything below is labeled re-derived (judge run) or
evidence-verified (committed bytes read). No lane repo was mutated; no sibling gate was executed
inside the lane's own tree — every re-run happened in the judge's own clones.

## 1. Step-1 conformance — PASS

| check | command | result |
|---|---|---|
| report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-59/kengaku.md` | `kengaku-shokunin <kengaku@shokunin.local> 6772ec891b01968b005cce0208ec45130b9c142` — PASS |
| SHONEN heading | `git show HEAD:.ufo/reports/round-59/kengaku.md \| grep -n '^## SHONEN'` | line 179, one `[~]` line per box — PASS |
| cited lane commits exist + ancestor | `rev-parse` + `merge-base --is-ancestor <h> refs/heads/master` for 5420eac9, 002cde8e, e0512854, 85ef87e5, 22ffccc7, fea67b2c, 12a76950, bc9cd073 | all 8 resolve, all YES; all inside e0cfa97a..bc9cd073 — PASS |
| branch tip pushed | `ls-remote origin refs/heads/master` vs local `rev-parse refs/heads/master` | both `bc9cd0737444a2925965a138c71112fb193c3328` — PASS |
| report content = committed bytes | sha256 of disk file vs `git show HEAD:<path>` | both `3685d9e7091caf2d731c8ac59db2b107b53dbad1e5c7090c2d266d78920c9c9e` — PASS |
| lane identity on round commits | `git log --format='%an <%ae>' e0cfa97a..bc9cd073` | all 8 commits `kengaku-shokunin <kengaku@shokunin.local>` — PASS |
| watchdog digest | `grep 'kengaku round=59' .ufo/watchdog.log` | lines 319/346 match the contract's digest verbatim — PASS |
| SHONEN.md untouched | `git diff --stat e0cfa97a..bc9cd073 -- SHONEN.md` | empty — PASS |
| L0 side channel | `.ufo/l0-questions.md` | no new kengaku round-59 lines; carried opens round-25/33/51/56 all present (lines 72/73/163/194/250/251); file committed — PASS |

## 2. Claim re-checks

### R59-C2 (operability) — VERIFIED, admitted. Re-derived end-to-end by the judge.

Instrument sha pins (re-derived, `git show <rev>:plans/receipt_consistency_check.py | sha256sum`):

- freeze `002cde8e`: `efd50ef6811b44935d9a456f4acbc0a4786b13168e671e5277b7efed66c44b77` = the
  freeze's pinned digest.
- amendment tip `e0512854` and round tip `bc9cd073`:
  `3767a4476c26c0c53b80fcb2978be1716d64d97bbca619b82ea1c69884848faa` = the amendment's named
  digest. Both instruments absent at base `e0cfa97a` (`cat-file -e` fails) — do-nothing control
  holds.

Selftest (re-derived, judge clone at tip): `python3 plans/receipt_consistency_check.py
--selftest` → 8 `SELFTEST ok …` lines, `SELFTEST cases=8 failures=0`, exit 0. The 8/8 tally is
reproduced, not just read.

Red-before (re-derived, judge clone at `e0512854`): `python3
plans/receipt_consistency_check.py --lane .` →
`FILE .ufo/waves/round-58/recon/esc-falsifier-fixed-checker.txt defects=2 errata=0 :: line 9:
exit=0 after ANCHORLINE live=1 (exit map wants 1) :: line 13: …`, `files=6854
anchored-exit-pairs=13 selftest-lines=1 defects=2 errata=0`, `PREDICATE R59-C2 fail`, exit 1.
Byte-identical in predicate fields to the committed receipt
`.ufo/waves/round-59/recon/c2-red-before.txt`. The erratum is absent at this revision (errata=0)
— the before-state is genuine.

Green-after (re-derived, judge clone at tip `bc9cd073`): `defects=0 errata=3` (`errata=2` on the
fixed-checker receipt + `errata=1` on the Q20 roster receipt's vacuous pass),
`PREDICATE R59-C2 pass`, exit 0. Matches the committed `final-tip-receipts.txt` section
(`files=6857 anchored-exit-pairs=13 defects=0 errata=3` measured at `12a76950`; the judge's
6858/14 at `bc9cd073` differs by exactly the wave-W3 receipt file itself, +1 file +1 anchored
pair — verdict unchanged).

Q25 amendment window (evidence-verified by commit order): the amended gate (3767a447…) lands at
`e0512854`; the first C2 receipt of record (`c2-red-before.txt`) lands at `85ef87e5`; the green
receipt lands at `22ffccc7`. Amendment BEFORE any C2 receipt of record — holds. Over-count
reproduced (re-derived): the FROZEN gate bytes (efd50ef6…) run over the `e0512854` tree print
`defects=15 errata=0` — the 2 real contradictions + 13 unanchored arbitrary-command labels —
matching the committed over-count receipt (same defects=15 at the freeze tip). The amendment
removed exactly the unanchored tooth; the claims doc diff freeze→tip is 41 insertions, 0
deletions (append-only; the freeze text never rewritten).

Registration: SKILL.md registry row `receipt-consistency-check` (gate; verdict map 0/1/2;
selftest spelling; both self-pins; named limits; write scope `reads the lane read-only … writes
nothing`; owner kengaku) + ledger row, same close commit as the SCORECARD counting command —
PASS per the r58 lesson-3 rule.

### R59-C1 (coverage) — predicate FAIL re-derived by the judge; NOT admitted, honestly carried.

Freeze-before-data (structural, evidence-verified): probe + freeze + captures + S218–S221 at
`002cde8e`; the receipt first lands at `e0512854`; probe sha256 `a7c9b231e4cef27e…b6a18cd`
identical at freeze and tip (`git show <rev>:plans/round59_c1_openssl_probe.py | sha256sum` at
both) — the probe was NOT re-frozen. Claims doc append-only freeze→tip (41 insertions, 0
deletions). Probe `--selftest` re-derived: toy-ok + toy-perm + `SELFTEST pass`, exit 0.

The judge's own re-run of the scored form (judge clone at tip; same bytes as the freeze):

```
$ python3 plans/round59_c1_openssl_probe.py --lane .
MISMATCH perm-loose test_directory_structure:predicted-F-observed-P; test_key_file:predicted-P-observed-F
CASE perm-loose predicted=F/P/P/P/P/P observed=P/F/P/P/P/P FAIL
MISMATCH key-1024 test_directory_structure:predicted-F-observed-P; test_key_file:predicted-P-observed-F
CASE key-1024 predicted=F/P/P/P/P/P observed=P/F/P/P/P/P FAIL
cases=12 legs=72 mismatches=2 setup=0 predicted_u=0
PREDICATE R59-C1 fail        C1-PROBE-EXIT=1
```

Payload byte-identical to the committed receipt `corpus/evidence/round59/openssl-probe.txt`
(diff of CASE/MISMATCH/summary lines: empty; the receipt names `REV 002cde8e…` — it was measured
at the freeze tip, the revision it grades). The frozen predicate (mismatches=0) is falsified:
70/72 confirmed, exactly 2 misses. **The fail stands; the claim is NOT admitted.**

Transcription-miss claim re-derived from committed bytes (as the closure contract asks):

- The freeze at `002cde8e` lines 84–85 read `perm-loose | key mode 0644 (the permission-bits
  leg) | F | P | P | P | P | P` and `key-1024 | 1024-bit key (the openssl rsa size leg) | F | P |
  P | P | P | P` — while the freeze's OWN defect-class annotations name the KEY leg as the
  failing one in both rows (dir should be P, key should be F). The F/P entries contradict the
  freeze's own annotations: author-transcription confirmed from the freeze alone.
- The observed vectors (P/F on both rows, from the receipt my re-run reproduces) are exactly the
  corrected predictions the annotations imply, and no other case deviates. The 2 misses are the
  4 cells (2 rows × legs dir/key) the lane names.
- Not re-frozen: the frozen table at `002cde8e` still reads F/P (checked at the freeze commit;
  the correction is a dated appended section, Q25's letter honored).

Honest-red registration: SKILL registry row `round59-c1-openssl-probe` declares verdict 1
"measured this round as **PREDICATE R59-C1 fail, exit 1: mismatches=2** … the row is declared
RED until a corrected zero-U re-freeze"; ledger row in the same close commit; the entryargv
TIPSTATE at the tip reads `entry_declared_green=59 entry_declared_red=30 observed_green=59
observed_red=30` (judge re-run, exit 0) — declared==observed holds mechanically at the tip, so
the red is registered and observed, not laundered.

Before→after anchors (re-derived): `git show 5420eac9:PROVINCE.md | grep -c sixteenth` → 0 (rc
1); tip → 2. SOURCES rows 210 → 215. `corpus/evidence/round59/` absent at base, present at tip
(4 capture files + 2 receipts; no `.key/.pem/.crt/.p12` anywhere — the r52 GH013 lesson held).
Score held 7 by the standing L0 cap (`kengaku | round-25/33/51` verified still open in
`.ufo/l0-questions.md`; nothing assumed answered).

### Carry-ins

- **Five orphaned round-58 receipts (wave R):** all five exist at `5420eac9` at exactly the
  r58-closure-cited paths (`.ufo/waves/round-58/wavep/r50-after.txt`, `fix/r46c2-after.txt`,
  `wavec/kl-sha-kill.txt`, `wavec-tip/entryargv-full.txt`, `waveR/final-tip-receipts.txt`), each
  opening with a dated re-landing header naming the clean clone at `e0cfa97a`, each carrying the
  green fields the report cites (`PREDICATE R50-C1 pass`; `PREDICATE C2 pass` with `PINS
  total=3 mismatched=0, anchorline live=0`; `KILL-EXIT=1`; `executed=87 … laundered=0` +
  `PREDICATE R55-C2 pass`; `PREDICATE R52-C2 pass` + `LANDCHECK PASS n=4`). All five still
  present at the round tip. Finding (a) DISCHARGED — verified.
- **Finding (b) correction:** closed as R59-C2's erratum (red→green above) — verified.
- **Cosmetic carry-in:** round-58 lesson mistakes-table rows matching
  `^\| (freeze|landing|fixture authoring) ` → 4 (re-derived; the correction's claim is true).
  BUT the second printed re-derive command does not reproduce: `grep -c 'broke four tip
  counters' LOG.md` → **0** on committed bytes (the phrase is line-wrapped at LOG.md:1961–1962:
  "The repair cascade broke\nfour tip counters before closure"); `grep -c 'four tip counters'
  LOG.md` → 1. Substance true, counting command as printed wrong — cosmetic defect below.
- **Tip health (re-derived at `bc9cd073`, all byte-matching `final-tip-receipts.txt`):**
  registry `ADVERTISED total=88`, `DUPLICATE 0`, `PREDICATE R52-C2 pass` exit 0; landcheck
  `LANDCHECK PASS n=4` exit 0; state_check `mismatch=0 superseded=7`, `VERDICT: PASS` exit 0;
  anchor scan `ANCHORLINE rows=215 cited=69 captured=62 live=0` exit 0 (`ROW S221 state=repaired
  by=S222`); round46-c2 `PREDICATE C2 pass` exit 0; r51 `violations=0`, `PREDICATE R51-C2 pass`
  exit 0; r50 `MUTANTS total=15 caught=15`, `PREDICATE R50-C1 pass` exit 0; r35 exit 1 with the
  declared-red fragment (`V4 DEFECT knowledge files=62 index rows=62 (want 42/42)`); full
  entry-truth `ROWS registry=89 ledger=89 missing=0 extra=0 argv_defect=0 …`, `BINDING l1=0 l2=0
  l3=0`, `SOURCE rev=bc9cd073… clean=yes lane_rev_equal=yes`, `RUN executed=89 timeout=0
  mismatched=0 evidence_missing=0 laundered=0`, `TIPSTATE 59g/30r declared==observed`,
  `PREDICATE R55-C2 pass` exit 0. The only reds at the tip are the two honestly-declared ones
  (the C1 probe; the r35 stale-expectation row). The round's advertised surface re-runs green at
  the round head from the judge's own clone.
- **Close-tip counter cascade:** S222 present in SOURCES with the corrected 7-word count
  (re-derived below); R26-E11 supersession row in SCORECARD (verified in the diff);
  state_check/anchor green re-runs cover the repaired legs. LOG wave entries for all 8 waves
  present (R/F/M/E2/close/W2/W2b/W3).

### No axis harmed

`git diff --stat e0cfa97a..bc9cd073 -- SCORECARD.md` → 47 insertions, 0 deletions: purely the
dated round-59 section, the capabilities no-row note, the planned note, and the R26-E11
full-value supersession row. No axis score row touched; all seven scores hold (coverage 7 at its
L0 cap; depth 9, adjacency 9, novelty 8, calibration 10, operability 10, freshness 10).

## 3. Per-axis verdicts (judge)

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | R59-C2 admitted and re-derived: the r58 finding-(b) class moved from eye-caught to mechanically-caught (red defects=2 → green defects=0, selftest 8/8, registry row); score held 10 at ceiling |
| coverage | unchanged | R59-C1 predicate NOT met (judge re-derived mismatches=2); score held 7 by the standing L0 cap; the frontier ground moved (16 of 89, SOURCES 210→215, knowledge entry) but the claim's verify condition failed — honestly carried, not harmed |
| depth | unchanged | 9 held; additive knowledge entry (`corpus/knowledge/tb2-openssl-selfsigned-cert-grader.md` with source/verified-at/recheck lines, README index row) |
| freshness | unchanged | 10 held; the two stale-red flips (state-assertion-check, round28-census) verified green with dated reasons (state_check PASS re-run) — repair, not an axis move |
| calibration | unchanged | 10 held — and exercised: the two misses are dated, mined (lesson Mistakes rows), NOT papered over; `admitted_self=false` is the honest-stop machinery working on its own author |
| adjacency | unchanged | 9 held; `considerthese/` diff empty in range; nothing absorbed |
| novelty | unchanged | 8 held; no new phenomenon claim; the class line rides the executed grader's registration |

## 4. Discernment spot-check (non-author)

The lesson's `## Gate` records four admits (S218–S221), no rejections, and names two
reject-equivalent decisions sampled for this closure (the Q25 refusal to re-force the C1 table;
the amendment-window timing). Sampled and re-opened:

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S220 (maintainer oracle, solve.sh) | admit tier A | live `raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/openssl-selfsigned-cert/solution/solve.sh` (curl 200) | **agree** | live sha256 `58cf3c844e907745cd81fb4bd75efb3d080e2f0e82b589c56c954ae6e1756510` = row = committed capture; line 14 quote exact, 13 words ≤25; lines 8/11 (`genrsa 2048`, `chmod 600`) as described; the probe's `sol` case passing all six legs (judge re-run) mechanically confirms the oracle's construction |
| S219 (the executed grader, test_outputs.py) | admit tier A | live fetch at the same pin | **agree** | live sha256 `90970bb3c372e8e7fb6bb9ac5f649ba73eb38e1a5ea2e922a9057a72b6b4192d` = row = round-59 capture = round-52 population capture (three-way byte-identity — "two independent fetches" verified); lines 22/79 match the row's located quotes (9 and 5 words) |
| R59-C1 kept FAIL, table NOT re-frozen (Q25) | reject-equivalent (refuse to re-score) | the committed receipt + freeze + judge re-run | **agree** | the 2 misses are real transcription defects re-derived by the judge from the freeze's own contradictory annotations; re-freezing to the observation would launder the freeze discipline; the corrected re-freeze is r60's planned first work |
| Q25 amendment window spent before any C2 receipt of record | reject-equivalent (instrument change discipline) | frozen-gate over-count re-run vs amended-gate re-run | **agree** | the frozen bytes demonstrably over-count (defects=15 vs the amended gate's defects=2 on the same tree; the 13 extra are arbitrary-command labels with no contradiction — judge confirmed); no receipt of record existed at amendment time (commit order verified) |

New-row quote check (≤25 words, all re-counted from the live bytes): S218 line 6 = 21 words,
S220 line 14 = 13, S221/S222 line 5 = **7** (S222's corrected count; S221's 6 was the mined
miscount), line 7 = 8, S219 lines 22/79 = 9/5. All ≤25 and located. Flip check: S222 correctly
supersedes S221; no other flips. Census: `sources-census.sh validate … kengaku` exit 0, verdict
ok, 21 W04 warnings = the 20 pre-existing + S222's supersession duplicate, exactly as the report
states. Mistake mining: `## Mistakes` five rows (3 + 2 appended) + the cascade appendix, each
with class/evidence/captured-by/fix — present.

## 5. Trend verdicts (judge)

- **expansion: improved** — verified: the knowledge entry is admitted on ground the coverage map
  did not hold, citing mined rows S218–S221 (byte-true, re-opened); frontier 15 → 16 of 89
  (PROVINCE re-derived 0→2 `sixteenth` anchors, "16 of 89" present); SOURCES 210→215; the new
  grader is a class the corpus lacked (only openssl-CLI grader in the 184-capture population;
  no executed grader touches st_mode — the class negatives ride the committed claims doc).
- **quality: improved** — verified: the tip's whole advertised surface re-runs green from the
  judge's own clone (registry 88/88, landcheck n=4, entry-truth 89/89 executed laundered=0,
  state_check PASS); the C2 gate admitted red→green with receipts; the close-tip cascade was
  caught by the designed counters and repaired before the round's receipts landed; the r58
  closure's four routed items are discharged with receipts.
- **discernment: improved** — verified: the round carries `admitted_self=false` on a failed
  predicate rather than re-freezing to the observation; the spot-check (this file §4) agrees
  with all four sampled gate decisions; five mined mistakes carry concrete fixes; correction
  rows are dated full-value forms (S222, R26-E11, errata).

## 6. Routed defects (status-neutral; the lane must fix next round)

1. **Fleet-repo round-58 report erratum uncommitted.** The round-59 report states the cosmetic
   corrections were "mirrored into … the round-58 report's `## Corrections (round 59)` section
   appended to `.ufo/reports/round-58/kengaku.md` (fleet root)". That append (26 lines,
   `## Corrections (round 59, 2026-11-02 …)`) exists ONLY in the fleet repo's working tree —
   `git diff HEAD -- .ufo/reports/round-58/kengaku.md` shows it uncommitted; the committed tree
   has no such section. The pointer does not resolve at closure. Fix: commit the working-tree
   append (it is already written) or re-land it; until then the erratum is not durable evidence.
2. **Two `path@hash` citations miss the landing commit** (the receipt-pointer class the lane has
   itself mined twice): the report and the SKILL registry row cite
   `.ufo/waves/round-59/recon/c2-red-before.txt at e0512854` — the file first lands at
   `85ef87e5` (at `e0512854` the recon dir holds only the over-count receipt; judge verified via
   `ls-tree` + `git log --reverse -- <path>`); and the report cites
   `corpus/evidence/round59/receipt-consistency.txt at 85ef87e` — it first lands at `22ffccc7`
   (`85ef87e5` is the measurement revision, not the landing commit). The claims doc's "the
   red-before receipt is committed BEFORE the erratum lands" is likewise imprecise: both land in
   `85ef87e5`. Substance intact — the before-state is independently on record (the judge
   re-derived defects=2/errata=0 at `e0512854`, where the erratum is absent). Fix: cite landing
   commits for `path@hash` pointers, or say "measured at".
3. **A dated correction's own counting command does not reproduce.** The cosmetic-correction
   section (claims doc §Dated corrections and the report) prints `grep -c 'broke four tip
   counters' LOG.md` → 1; on the committed bytes it prints **0** (the phrase is line-wrapped at
   LOG.md:1961–1962). `grep -c 'four tip counters' LOG.md` → 1. Fix: quote the wrapped phrase or
   use the unwrapped token string.
4. **SCORECARD round-59 section staleness (cosmetic):** it says SOURCES "210→214" (written at
   the close commit `22ffccc7`); S222 landed later at `fea67b2c`, tip count 215 (the report
   itself says 210→215 correctly). Fix: one dated touch-up line next round, or leave as a dated
   measurement — named so the drift is on record.

## 7. SHONEN note for the operator

All four boxes are `[~]` (asserted-by-author) with resolvable pointers; `SHONEN.md` itself
untouched in range. This non-author reviewer notes the boxes look fully checkable by a
non-author promotion review: box 1's registry re-derives via `R52-C2 pass` (judge re-run);
box 2's end-to-end task is logged with receipts (probe receipt re-run byte-identical); box 3's
canonical cold-run form is cited; box 4's `state_check` → `VERDICT: PASS` re-derived at the tip.
No `[x]` written anywhere by this closure.

## 8. Admission ruling

Per AXES.md ("a round is admitted only if every claim verifies and no axis harmed") and the
closure contract: R59-C2 verifies (re-derived admitted); R59-C1's frozen verify condition
(mismatches=0) is falsified on the round's only capture run and stands FAIL (judge re-derived;
not re-frozen; honestly carried; score held 7). Every-claim-verifies is therefore NOT met —
**the round is NOT admitted: verdict `rejected-honest-stop`, `admitted=false`**, with no axis
harmed and the durable defect-fix (C2) verified — the honest-stop machinery working as designed,
matching the lane's own `admitted_self=false`. Conformance defects above are status-neutral and
routed; they do not bar or cause this outcome.
