# Round 45 — a fixture fence landed whose frozen counter a path-keyed control also passes (8 of 10 held-out modules admitted); an eleventh TB2 grader executed (2026-10-26/27, hyaku run 9; title corrected attempt 3)

L1 `KengakuR45` (planner seat; attempt 2 — attempt 1 died on an invalid_prompt policy refusal with no wave,
report or commit, `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1618`, 22:48; discarded drafts at `.ufo/waves/round-45/attempt1-unclaimed/`). Frozen claims `plans/round-45-claims.md` (freeze `b4fcd35` +
pre-data amendments `9271dda4`); baseline lane tip `9d5f971` (the round-44 non-author spot-check). Wave 1
(build/package, 39 seats) + wave 2 (falsify, 39 seats). Written by the L1 at integration from the seat
reports named in each row.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A receipt committed with envelope framing around the instrument's bytes** — the L1's first recorded probe run captured the whole `envelope.sh` transcript into `corpus/evidence/round45/password-recovery-probe.txt`; the gate's `c_rerun` (`P10`) requires `r.stdout == want`, and three `ENVELOPE ` lines make the file fail byte-equality even though every verdict inside is right. | `.ufo/waves/round-45/w1/R45ProbeFirst.md` §5 (5243 B vs the probe's 4659 B); gate output `P10 DEFECT fresh probe output is not byte-equal to the receipt` | none at freeze — the receipt was copied straight from the harness transcript | reframed at `7d062c0`: the receipt is bare probe stdout (`cf74f451`, 4659 B); the wrapper transcript moved to `corpus/evidence/round45/probe-run-envelope.txt` and is committed *after* the receipt (the `order_check.py` `CASE_LINE` pattern makes a pre-receipt transcript proof of a pre-freeze run — verified both directions by `R45ProbeFirst` on throwaway fixtures). Rule: **a receipt file is the instrument's stdout only; envelope framing is separate evidence.** |
| **A spec whose row `capture` fields disagree with its own capture manifest** — `pkg-spec-r45.json` rows named flat basenames (`test_outputs.py`, `setup.sh`, …) while `SHA256SUMS` and the counter's `CAPTURES` dict used the upstream directory layout (`tests/test_outputs.py`, `environment/setup.sh`, …). Five rows were "not pinned in the manifest" and twelve `## Located quotes` rows cited files that did not exist under the named convention. | `R45ProbeFirst.md` §5b/§5c; gate output `P5 DEFECT manifest_entries=9 bad=10`, `P4 checked=19 bad=12` | nothing: the draft froze with the split convention (the probe read nested, the spec rows were flat) | the capture tree was flattened to the r44 convention (all 9 digests unchanged — same bytes, flat names) and the probe's reads re-pointed; the receipt it prints is byte-identical on re-run (`9363e03e` → still `cf74f451`-content). Rule: **one capture convention per freeze, checked by running the gate once before the freeze commit.** |
| **A defect class that survives "the tool returned the right verdict"** — the round-44 fence's four routed defects were all of the form *the fence refuses correctly but opens/blocks on a path outside d while deciding* (commondir, config.worktree include, refuse-to-describe, parent-process include read). A counter that only records admit/refuse reads every one of them as a pass. | `corpus/lessons/round-44.md` (routed `R44SentinelFences` V1–V3, `R44LabratLaneInclude`); `plans/round-45-claims.md` §C1 | `control-c1-fence-r44.txt` — the r44 counter's own fence as the fence → `REFUSALS total=10 clean=3 leaked=3 read=4`, `contradicted=7` | the round-45 counter runs the fence under `strace -f -y` inside bwrap and counts `LEAKED` (admits), `READ` (refuses but opens outside) and `HUNG` separately — the observed fence, not the asserted one. Rule: **a refusal verdict that required an outside read is a defect, and the counter must see the read.** |
| **A quote that is verbatim but below the word floor** — four `## Mechanism` rows quoted single tokens (`read_text().strip().split("\n")`, `recovered_pass_path.exists()`); the counter's `len(q.split()) < 2` rule rejects them even though they are byte-exact on the cited line. The seat's diagnosis reported them as "not on the line" because the token floor and the substring check report together. | counter run `V10 DEFECT … constant-crlf / dir-state / crlf-line / under-varsea quote not on the line`; `R45ProbeFirst` follow-up | the counter run itself (mechanism rows are checked at every counter run) | multi-word verbatim quotes on the same decisive lines (`guesses = Path("…").read_text()`, `assert recovered_pass_path.exists(), "Recovery file not found"`). Rule: **cite the line's decisive clause wide enough to clear the word floor — the decision line, not the minimal token.** |
| **A frozen-file digest list that drifted behind the freeze it pins** — `frozen-digests.txt` listed the pre-amendment probe/spec/counter/SHA256SUMS digests while the tree had already been corrected, and held a duplicated counter line. | `R45ProbeFirst` follow-up (the digest table + the note that V5's self-reference needed a claims-file line); `.ufo/waves/round-45/claims/frozen-digests.txt` diff | the seat's bookkeeping audit | regenerated in one shot after the amendment commit; the claims file now carries a "Freeze amendments" paragraph that names each pre-data correction and the re-pin, so the digest list is a statement of the amended freeze, not a silent rewrite. |
| **A gate hygiene clause that races the measurement it protects** — `P9` (`untracked=`) counts seat artefacts landing mid-run, so a back-to-back counter run can fail on files another seat just wrote. (Attempt 3: the earlier "`untracked=2` then `untracked=14`" sentence had no receipt — `R45RevLesson` finding 2 — and is withdrawn; the measured instance is `P9 DEFECT untracked=30 first=.ufo/waves/round-45/a3w1-dispatch.json` on the live lane at 00:25, `C2 checks=11 defects=1`, against `checks=11 defects=0` on a clean clone of the same commit: `.ufo/waves/round-45/a3w1/R45SentC2Grader/c2-verify.txt:12` vs `c2-verify-clone.txt`.) | `.ufo/waves/round-45/integrate/measure-final.txt` and `integrate/a3-tip-c2.txt` (clean clones: `P9 ok untracked=0`); the live-lane A/B receipts (`corpus/evidence/round45/counter-a-run.txt`, `counter-b-run.txt`, equal on every non-`ENVELOPE` line, not byte-equal — corrected attempt 3 after `R45RevLesson` finding 2) | the counter's own `--require-clean-tree` rerun | run the measured clone: the tip-clone re-measure under the envelope is the conformance evidence; live-lane runs are bookkeeping. A seat that races the counter is *not* a counter defect — the measurement discipline is. |

## Gate

Opened or captured this round. Access date 2026-10-26 for every row; times are -03. The L1 re-fetched all nine
files of the task directory at ~23:05 -03 (`corpus/evidence/round45/tb2-password-recovery/` + `SHA256SUMS`,
`cmp`-identical to the attempt-1 draft). Base URL
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/`.

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `tests/test_outputs.py` (S149) | admit | the executed scoring predicate: exists() + line-membership of one constant; flips to reject if a re-fetch changes its digest |
| `instruction.md` (S150) | admit | the request the map is against; flips on digest change |
| `environment/setup.sh` (S151) | admit | plants the fragments at 1MB/3MB; flips on digest change |
| `environment/Dockerfile` (S152) | admit | installs the forensic toolset, runs the seed; flips on digest change |
| `tests/test.sh` (S153) | admit | reward = pytest exit status; flips on digest change |
| `README.md` (S154) | admit | authors' check description matches the mechanism; flips on digest change |
| `solution/solve.sh` (S155) | admit | the oracle the `oracle-solve-sh` case executes; flips on digest change |
| `task.toml` (S156) | admit | 900 s timeouts, `allow_internet = true`; flips on digest change |
| `gitignore` capture | reject (as row) | the task's dotfile; captured for byte-complete refetch checks, not a row — no claim rests on it. Flip: admit as a row if an entry sentence cites `gitignore` content (a graded path it hides, an artefact it excludes) — attempt 3 added this flip after `R45RevLesson` finding 1 |
| `environment/varsea-…dat` seeds | reject | runtime-generated image bytes; the probe recreates them from `setup.sh`, and `/dev/urandom` differs run to run — a capture would record noise, not a fact. Flip: capture and admit if upstream commits a fixed seed file at the pin, or `setup.sh` stops reading `/dev/urandom` (re-check on any digest change of S151) — flip added attempt 3, `R45RevLesson` finding 1 |

## What was demonstrated (rewritten attempt 3 — the attempt-2 wording overclaimed, `R45CritC1Overclaim` C1-A)

- **Calibration (C1): the frozen predicate passed, and it cannot certify the work.** `plans/fixture_fence.py`
  (wave variant A) prints `PINS total=33 mismatched=0`, `REFUSALS total=10 clean=10`, `HONEST fixtures=104
  admitted=104`, `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass` on clean clones of `8f9a898`
  (`integrate/measure-final.txt`) and of `fbad1c5` (`integrate/a3-tip-c1.txt`). A fence that inspects nothing and
  keys on the counter's fixture path prints the same pass (`claims/control-c1-fence-keyed_name.txt`), so by the
  round contract's control rule the counter does not separate the claimed work from no work. Held-out modules
  written in attempt 3 against the landed fence: of 10 held-out hostile modules, 8 are admitted (includeIf with CR /
  BOM / conditional sections 3/3, `.git/objects` symlinked outside `d`, a NUL argv token the fence raises on, a
  linked-worktree metadata dir, a relative commondir behind a hidden path, a `core.attributesFile` outside `d` that
  git honours) — `a3w1/R45HoIncludeIf.md`, `R45HoSymlinks.md`, `R45HoArgvEnv.md`, `R45HoCommondir2.md`,
  `R45HoConfigKeys.md`, confirmed independently by `R45CritLandedFence.md` and
  `R45CritIntent.md` finding 2. Fence mutation: 7 of 15 single-edit mutants caught (`R45MutLandedFence.md`). What
  does hold: the fence reads no fixture name (`R45CritIntent` rename control A/A2), and the name-blinded counter
  separates it from the keyed control (`claims/dev-blind-c1-landed.txt` pass vs `dev-blind-c1-keyed.txt` fail).
- **Coverage (C2): the frozen predicate passed and the do-nothing control fails it.** TB2 `password-recovery` @
  `2fd12b88` (S149–S156, tier A); probe `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16
  differ=0`; `checks=11 defects=0`, `PREDICATE C2 pass` on a clean clone of `fbad1c5` (`integrate/a3-tip-c2.txt`);
  `claims/control-c2-nothing.txt` `defects=8`. Non-author review found defects the counter does not check: three row
  anchors cite a line that does not carry the quote (S152 `:15`→`:17`, S153 `:28`→`:26`, S154 `:44`→`:31`) plus ten
  smaller cell defects (`R45RevRowCells.md`); the entry's `## Predictor` disagrees with the captured grader on lone-CR
  states (3 of 9, `R45RevEntryQuotes.md`); one Mechanism row names `:16` where `:18` decides (`empty-file`); V11 admits
  four lint-clean lookup predictors (`R45CritV11Bypass.md`), beyond the 48-bit-table limit the freeze named; the gate's
  P10 leg runs `uv run --with biopython==1.85` outside the sandbox when the host lacks `Bio` (`R45SentC2Grader.md` F1).
- The routed round-44 defects V1–V3 + `R44LabratLaneInclude` are refusal classes f7–f10 inside the frozen counter,
  and the r44 fence fails them (`claims/control-c1-fence-r44.txt`, `contradicted=7`) — that part of the routed-defect
  loop is closed; the fence class itself is not (held-out results above).

## Attempt 3 (2026-10-27, L1 `KengakuR45a3`)

Attempt 2's L1 and its 39 wave-2 seats were killed by the orchestrator session exit at 2026-10-26 23:57:36 -03
(`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1629`); the orchestrator salvaged its working tree as `fbad1c5`.

- **Reused after re-verification:** every committed round-45 claim artefact through `a448a47` — both frozen counters
  re-run on a `--no-local` clone of `fbad1c5` under the envelope (`integrate/a3-tip-c1.txt`, `a3-tip-c2.txt`: both
  `PREDICATE pass`, exit 0); `sha256sum -c claims/frozen-digests.txt` 18/18 OK; the no-harm set re-run
  (`integrate/a3-noharm.txt`: r44 C1/C2 pass, anchor `rows=149 tokens=55 defects=0`, `routed_open=24`, round-close 44
  PASS) — the same values `w2/R45ExecNoHarm.md` reported; census exit 0 (as `w2/R45ExecCensusPost.md`).
- **Kept as record, not cited as evidence:** the salvage commit's partial files of killed seats
  (`w2/R45HoCommondir2/h2_gitfile.py`, `w2/R45MutC1Instrument2/receipts/*`) and `w2-results.json` (a dispatch record).
- **Discarded:** the attempt-2 fleet report draft (it said both claims landed with wave 2 unread); this round's report
  is rewritten from the measurements above. The 34 killed wave-2 items were re-dispatched unchanged as wave `a3w1`.
- **a3w1 settlement** (`.ufo/waves/round-45/a3w1-results.json`): 34 settled; 32 report files. Two seats left no report
  and their output was not retained (`note`: "orchestrator kernel restarted mid-wave; seat output was delivered to the
  orchestrator session but not retained"): `R45MutC1Instrument2` (partial files under `a3w1/R45MutC1Instrument2/`,
  unverified, not cited) and `R45MutC2Checks` (nothing on disk). The reportless-seat class (round-43 D3) recurred: 2 in
  w1 (recovered from results) and 2 here (unrecoverable) — the C1 instrument and C2 check mutation items are unattacked.

### Mistakes (attempt 3)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A freeze whose controls never included a procedure that keys on the counter's own names** — every frozen C1 control fence either inspects the fixture or does nothing; none reads `d`'s path, which the counter builds as `fx/<battery-or-refusals45>-<stem>/fNNN`. A one-line keyed fence passes the frozen predicate. | `.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt` (`PREDICATE C1 pass`, exit 0, frozen counter, clone of `fbad1c5`); first found by `w1/R45CriticPredicate.md` B2 | the round contract's control rule ("build the cheapest control that skips the claimed work") — applied with four shapes, not this one; Q31/Q37 do not name it | QUALITY Q39; shown able to fail: the keyed fence passes the frozen counter and fails the name-blinded one (`claims/dev-blind-c1-keyed.txt`, `contradicted=10`, exit 1) while the landed fence passes both (`dev-blind-c1-landed.txt`). |
| **A claim booked as landed while a wave verdict naming it as forgeable was on disk** — `w1/R45CriticPredicate.md` ended `VERDICT: c1-predicate-bypasses-7-verdict-changing-6` before the attempt-2 SCORECARD cell said `improved` and the attempt-2 report draft said "both claims landed". | `w1/R45CriticPredicate.md:165`; SCORECARD round-45 C1 cell at `fbad1c5`; the discarded draft | none — nothing compares seat VERDICT lines with the scorecard verdict | attempt 3 rewrote the verdicts from the wave; check for the next close: `grep -l 'verdict-changing-[1-9]' .ufo/waves/round-N/*/*.md` must be empty or each hit answered in the lesson before a verdict cell says `improved` — on this round it lists `w1/R45CriticPredicate.md`, so the check is red here. |
| **Self-assessment numerals with no receipt** — the round-45 SCORECARD cited the claims file's sha256 as a commit (`cb2fae38`), the A/B receipts as byte-equal, and a lesson row quoted `untracked=2` then `untracked=14` that no file carries. | `git cat-file -t cb2fae38` → `fatal: Not a valid object name`; `cmp corpus/evidence/round45/counter-a-run.txt counter-b-run.txt` → differ, line 1; `R45RevScorecard.md` finding 4, `R45RevLesson.md` finding 2, `R45CriticMistakes.md` row 6 | none at write time; three non-author reviewers in `a3w1` | each corrected in place with an attempt-3 note; each correction's command fails on the old text (shown above). |
| **Row anchors that pass the gate while citing the wrong line** — S152, S153, S154 quote text that exists in the capture but at another line; the gate printed `P6 ok rows=8 bad=0`. | `a3w1/R45RevRowCells.md` defects 1–3; `corpus/evidence/round45/gate-call.txt` | none — the gate does not compare a row's anchor line with the line holding its quote | routed (round 46): supersede S152–S154 as new rows under Q34 and add the anchor-line comparison to the gate with a red fixture; not yet shown able to fail. |

### Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` — round
start (`.ufo/waves/round-45/claims/census-before.txt`): 15 `W04`, `kengaku ok`, exit 0, 141 rows; round end (attempt 3,
00:20 -03): 15 `W04` (the same ids), `kengaku ok`, exit 0, 149 rows (`grep -cE '^ {0,3}\| *S[0-9]{3}' corpus/SOURCES.md`).

### Assimilation and considerthese

Assimilation: none — the claims were frozen before any package row was re-grounded; `w1/R45MergeRescreen.md` (73
collisions, quarantine slice 2 rows) and `w2/R45CritAssimilation.md` (S091 quote absent from the live page → refuse,
adopt nothing). considerthese: `w1/R45Considerthese.md` mined `considerthese/2026-10-26.md` proposal 2 (one standing
grader-admission counter with a committed filler package that must stay red); not landed this round, carried to
round 46 — the C2 findings above are its motivating instance.
