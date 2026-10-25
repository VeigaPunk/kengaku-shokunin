# F35CritHarm — no-harm audit, kengaku round 35 wave 2 (falsify)

Seat: critic (leaf). Scope: compare SCORECARD axis rows, PROVINCE, SKILL.md,
QUALITY.md, existing knowledge entries and gates at `58a19f37` vs
`dfee6fff631ebc5f623ba4506e5c7992a215401c` (lane tip, master). All runs read-only in the lane;
nothing outside `.ufo/waves/round-35/falsify/` or /tmp was written.

## 0. What landed (range `58a19f37..dfee6ff`, 7 commits)

`5d0c73d` round-34 verifier spot-check lesson; `11d6453` freeze (claims, counters,
probe, ledger, controls); `dfcd294` C2 close D1–D5 (drafts committed, mirror roots
deleted, manifest, corrections, ledger closed); `4fe72a9` C1 admit + PROVINCE
paragraph + hardening; `6ac9611` SCORECARD/LOG; `056e192` census receipts + lesson;
`dfee6ff` wave-1 evidence (32 seat reports, spec, dispatch, results).

Non-`.ufo` delta = **27 files, all additions/edits, zero deletions**
(`git diff --no-renames --name-status 58a19f37 dfee6ff -- ':!.ufo'` → only `M`).
The 109,413 deleted paths are **all** under
`.ufo/waves/round-34/{mut-entries-scratch,build/R34MutRegistry/mirror,build/R34MutRegistry/mut}`
(count `git diff --no-renames --name-status 58a19f37 dfee6ff | awk '$1=="D"' | wc -l` =
109,413; no path outside `.ufo/`). This is exactly the C2-D2 cleanup the LOG claims
("109,413 committed mirror paths … deleted at the tip; history keeps them").

## 1. Gates at tip (all ran read-only, all green)

| Gate | Command | Output | Expected (frozen) |
|---|---|---|---|
| grader | `python3 grader.py` | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS` / exit 0 | pass |
| state_check | `python3 plans/state_check.py --summary` | `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5` / `VERDICT: PASS — all comparable frozen assertions match` / exit 0 | exit 0 |
| round-33 defects | `python3 plans/round33_defects.py --lane .` | `checks=6 defects=0` / exit 0 | `checks=6 defects=0` |
| C1 counter | `python3 plans/round35_c1_verify.py --lane .` | V1–V6 ok; `checks=6 defects=0`; `PREDICATE C1 pass`; exit 0 | `checks=6 defects=0` + pass |
| C2 ledger | `python3 plans/defect_ledger.py --lane .` | `rows=5 closed=5 observed_pass=5 mismatches=0`; `PREDICATE C2 pass`; exit 0 | `rows=5 closed=5 observed_pass=5 mismatches=0` + pass |

No gate script changed in the range (`grader.py`, `plans/state_check.py`,
`plans/round33_defects.py` absent from the diff), so the gates are byte-identical code
running against the new tree.

## 2. Frozen predicates vs implementation (read of shipped counters)

- `plans/round35_c1_verify.py` docstring restates the frozen C1 predicate verbatim.
  V1 pins match the three captures' sha256 (S105 `44a05a24…`, S106 `9ede4664…`,
  S107 `1bb2af1d…` — equal to the SOURCES anchors and the pinned digests); V2 checks
  S105–S107 rows (11 cells, tier A, mined, opened 2026-10-25, source URL = pinned raw
  URL, used-by = entry); V3 requires ≥8 `## Located quotes` rows, each ≤25 words, each
  verbatim on the cited capture line (entry holds 21 quote rows); V4 checks one README
  index row + coverage bullet + committed knowledge files == index rows == 42 (verified
  independently: 42 files / 42 index rows); V5 re-runs the probe fresh and byte-compares
  to the receipt; V6 census exit 0 (both receipts exist: `corpus/evidence/round35/census-{before,after}.txt`, exit=0, 15 W04 each).
- `plans/defect_ledger.py` r34_d1–d5 each compare a self-assessment sentence against an
  observation computed from repo bytes: D1 (untracked under round-34 wave + the three
  round-34 plan-tool paths), D2 (zero committed mirror-root paths at branch tip), D3
  (`tb2-eval/SHA256SUMS` lists test_outputs.py/test.sh and digests match bytes), D4
  (reads `R34C2CounterDraft.md:8` = `cases=10 failed=0` and `R34MutC2Harness.md:12`
  = `SELFTEST green failed` — **both files exist at those paths**, verified), D5
  (tag-stripped `nec-s091-reopen.html` contains the staged S091 quote — verified present;
  erratum line in `round-34.md`; `round-35.md` §Mistakes S091 row). Control receipts are
  byte-consistent with the claims: `control-c1-nothing.txt` (`checks=6 defects=5` exit 1),
  `control-c1-skip.txt` (`checks=6 defects=5` exit 1), `control-c2-nothing.txt`
  (`rows=5 closed=0 observed_pass=0 mismatches=0` exit 1), `control-c2-flip.txt`
  (`mismatches=4` exit 1).
- Probe receipt `corpus/evidence/round35/tb2-grader-probe.txt` carries all 18 frozen
  cases; summary `cases=18 observed_pass=5 observed_fail=13 mismatches=0` matches the
  entry's quoted line and the SCORECARD row.

## 3. Prior-claim evidence integrity (the actual no-harm question)

- **No deletions of corpus/plans/docs evidence.** The only deletions are the round-34
  mirror/scratch roots, which are the *defect record* C2 closes, not evidence a positive
  claim cites; history keeps them (LOG states "no rewrite"). No file under `corpus/`,
  `plans/`, `SCORECARD.md`, `PROVINCE.md`, `LOG.md`, `QUALITY.md`, `SKILL.md` was
  removed or had a line replaced.
- **Prior admitted claims' cited paths still resolve.** Round-34 spot-check D1–D5 source
  lines (`corpus/lessons/round-34-verifier-spotcheck.md:75-79`) intact. D4's cited build
  files exist (see §2). `considerthese/2026-10-25.md` §Self-improvement suggestions 2
  exists in-lane and contains the quoted ledger proposal. The `.ufo/l0-questions.md:163`
  anchor cited by claims/SCORECARD resolves to the fleet root
  `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`, line 163 = the round-33 L0
  coverage-cap question — the same notation every round-25–35 doc uses and QUALITY
  R11/R15 explicitly document as fleet-root-resolved; no claim's anchor is removed.
- **Corrections are append-only and label what they replace.** SCORECARD D4 correction
  and the `round-34.md` erratum preserve the earlier sentence and mark it false; the
  round-35 non-append outcome still holds (no admitted entry cites the NEC S091 row —
  the lane's own S091 row is the ABC paper, a different source).
- **Frontier/novelty wording narrowed only as claimed.** `corpus/README.md` §Frontier's
  new round-35 bullet discharges "Terminal-Bench 2.0's" scoring code for `protein-assembly`
  only and explicitly keeps open the other TB2 tasks, other SWE-bench Pro V2 graders,
  and runtime task validity; PROVINCE's round-35 paragraph matches this scope ("narrows
  only the Terminal-Bench 2.0 scoring-code clause for this one task").
- **Axis scores untouched.** SCORECARD round-35 section records held scores (coverage 7
  capped by the L0 question, novelty 7, depth 9, operability 8, freshness 8, calibration
  8, adjacency 8); no prior score row changed.

## 4. Known post-freeze weaknesses — disclosed, not hidden, not falsifying

Wave-1 falsifiers proved the frozen C1 counter passes on a junk package (stub probe,
one-word quotes, junk teaches) and that D4/D5 checks accept labelled-but-false lines;
the frozen predicates were left unchanged, `plans/round35_hardening.py` was added
post-hoc and is shown able to fail on all five counterexamples
(`corpus/evidence/round35/hardening-counterexamples.txt`: H1–H6 rows, `failed=0` on the
landed copy, ≥1 failure per counterexample CE1–CE5). The ledger's `recurrence_of` is
recorded-not-enforced and D1 is round-34-scoped by design — both stated in Q23/claims.
None of this makes a landed claim false, because the claims say exactly what the counters
check (predicate-met verdicts), and the weaknesses are recorded in SCORECARD/lessons.

## 5. What could not run

Network re-fetch of the three pinned URLs was not needed: V1/V2 verify the captures'
digests against the pins and the SOURCES anchors, and the captures exist in-tree. No
campaign tool (sources-census writes/validations outside the lane, etc.) was run; census
V6 and the committed receipts were used instead.

## Verdict

No landed change makes an existing claim false, breaks any gate, or removes evidence a
prior admitted claim cites; the six-axes and novelty surfaces are additive or unchanged,
and the C1/C2 frozen predicates hold at tip with reproducible command+output.

VERDICT: harm-0
