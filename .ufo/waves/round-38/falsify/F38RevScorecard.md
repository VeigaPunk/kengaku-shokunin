# F38RevScorecard — self-report calibration (round 38, falsify wave 2)

Seat: reviewer. Target: `SCORECARD.md` round-38 section (lines 1334–1373), `LOG.md` round-38 section
(lines 1115–1148), `SHONEN.md` — compared against the observed repo at the landing tip
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a`. Method: clean `--no-local` clone in scratch
(`/fast/scratch/hyaku/kengaku-r38/F38RevScorecard/lane`, toplevel verified equal to the clone path,
HEAD = `8c7422d…`), every checkable claim re-run or re-derived there; receipts under
`.ufo/waves/round-38/falsify/F38RevScorecard/`. Scratch removed at end. No lane file, index or jj
state touched; no pacman transaction; no tool installed.

**Result: 41 claim groups checked, 0 mismatches counted.** Every count, hash, verdict and capability
row in the round-38 self-report reproduces at the tip. Two disputes are recorded (not counted) and
three gaps are named at the end.

## 1. Chain, freeze and probe-run facts (SCORECARD header; LOG header; lesson header)

| Claim | Command | Observed |
|---|---|---|
| baseline `fc1174f52b150999bef91f2e81da78732ca0eb9f` = round-37 non-author spot-check | `git log --format='%H %ci %s' -1 fc1174f5` | `2026-10-26 02:25:17 -0300 round-37 verifier spot-check (integrator, hyaku): non-author admit/reject` |
| freeze `e0a378539a45cc9388c66cfba22f44275131de23` is a **child of** `21e6251b` | `git log --format='%H %P' -1 e0a37853` | parent = `21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9` |
| `21e6251b` "landed 3 s earlier" | `git log --format='%ci' -1` on both | `02:38:25` vs `02:38:28` — 3 s |
| first recorded probe run `e95cf550` | `git log -1 e95cf550` | `round-38: first recorded build-pmars probe run on a clean clone of e0a37853 (cases=22 observed_pass=7 observed_fail=15 mismatches=0; second run byte-equal)`; the receipt file is first added in that commit (`git log --diff-filter=A -- corpus/evidence/round38/build-pmars-probe.txt` → `e95cf55`) |
| landing measurement on a clean `--no-local` clone of `d93b7d68`, `untracked_in_clone=0` | `sed -n '1,2p' .ufo/waves/round-38/integrate/measure-final.txt` | `TIP d93b7d68dacfd6a23ec2cf732a4615d6c732c73e` / `untracked_in_clone=0` |
| freeze commit holds claims, both counters, probe, dry table, five captures, red controls | `git ls-tree -r e0a37853 --name-only \| grep -E 'round-38\|round38'` | claims + `round38_c1_verify.py` + `round38_c2_verify.py` + probe + dry table + `tb2-build-pmars/` (5 files + `SHA256SUMS`) + 4 control files + `census-before.txt` + `frozen-digests.txt` |
| lesson header erratum: "neither frozen counter reads anything `21e6251` touched" | `git diff --stat fc1174f5 21e6251 -- plans/ corpus/knowledge corpus/SOURCES.md corpus/README.md \| wc -l` | `0` |
| order-of-operations disclosure: no receipt at freeze | `git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt` | `rc=128` (`exists on disk, but not in 'e0a37853'`) |

## 2. C1 (calibration, honest stop) — SCORECARD C1 row, LOG C1 bullet

Re-run at the tip (`python3 plans/round38_c1_verify.py --lane . --work <scratch>`, receipt
`c1-verify-tip-8c7422d.txt`): `PINS total=14 mismatched=0` / `BATTERY fixtures=86 wrong=0
renamed_disagree=0 sidechannel=0` / `MUTANTS total=22 killed=21 survived=1 invalid=0
null_detected=0` / `PREDICATE C1 fail`, exit 1 — byte-identical values to `measure-final.txt` and to
the SCORECARD "after" cell. "Before" cell matches the committed control verbatim
(`control-c1-nothing.txt`: `BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0`,
`MUTANTS total=22 killed=0 survived=22`, `PREDICATE C1 fail`).

- Gate unedited: `sha256sum plans/pkg_gate.py` → `ea63882240e67e99…` = the claimed `ea638822…`;
  `git log --oneline e0a37853..8c7422d -- plans/pkg_gate.py plans/round37_c1_verify.py
  plans/round37_c2_verify.py plans/battery37 plans/round-38-claims.md plans/round38_c1_verify.py
  plans/round38_c2_verify.py plans/build_pmars_probe.py` → 0 commits (nothing frozen was edited).
- "twelve wave-1 executor seats wrote `plans/battery38/` (22 fixtures, `dc0cdb54`)": `ls
  plans/battery38/ | wc -l` → 12 modules; `git show --stat dc0cdb54 -- plans/battery38` lists exactly
  those 12 files; `build-results.json` has 40 results of which 12 are the `R38Bat*` seats; fixture
  delta 86 − 64 = 22.
- N21 explanation: my re-run prints `MUTANT N21 D5 silence SURVIVED`; `python3
  plans/mutant_direction_check.py --lane . --work <scratch>` → `DIR N21 D5 declared=silence
  observed=mirror MISLABELLED`, `DIRECTIONS total=22 mislabelled=1`, exit 1 (receipt
  `direction-check-tip-8c7422d.txt`) — matches the LOG and the SCORECARD verdict cell, and
  `build/R38BatD5.md` §BLOCKER carries the 8-shape manifest matrix with "No shape has `ref DEFECT`
  with a passing mutant" (8 rows counted).
- SCORECARD verdict-cell disclosures verified against their sources: "3 of 22 `adv` cells name no
  advertising sentence" — N01/N08/N16 cells (`round38_c1_verify.py:94,110,129`) cite a capability-row
  phrase / Q24 / a code comment; `corpus/QUALITY.md:433-437` lists the empty-`frozen_instruments`
  branch, the clause-crash handler and the crash→exit-2 handler as unclaimed; the genuine r35
  `SHA256SUMS` has 0 blank lines (`grep -c '^$'` → 0), so N08's Q24 citation cannot cover it —
  22 − 3 = 19, exactly the lesson's "advertised-class mismatch count is 19→1, not 22→1". "Predicate
  reachable by an in-process monkeypatch" — `R38CritClaims/junk-battery-reaches-attribution.txt`
  shows `BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=20
  survived=2`.

## 3. C2 (coverage, predicate met) — SCORECARD C2 row, LOG C2 bullet

Re-run at the tip (`python3 plans/round38_c2_verify.py --lane . --work <scratch>`, receipt
`c2-verify-tip-8c7422d.txt`): `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0; gate block shows
`P8 ok index_rows=45 knowledge_files=45`, `P10 ok probe_rerun=byte-equal bytes=5537` (the
"second run byte-equal" claim). "Before" cell matches `control-c2-nothing.txt` verbatim
(`checks=7 defects=4`, V2/V3/V4/V7 DEFECT, exit 1).

- Probe re-run at the tip (`python3 plans/build_pmars_probe.py --lane . --work <scratch>`, receipt
  `build-pmars-probe-tip-8c7422d.txt`): `cases=22 observed_pass=7 observed_fail=15 mismatches=0`,
  22 `CASE` lines, exit 0 — equals the committed receipt `corpus/evidence/round38/build-pmars-probe.txt`
  and the frozen dry table's `cases=22 predicted_pass=7 predicted_fail=15`.
- All six LOG "observations on the pinned capture" map 1:1 onto committed CASE lines: `canned-shape`
  (canned C program, empty `debian/`, zero-byte `src/dummy.c`) `observed=pass tests=PPPP`;
  `canned-x11-dlopen` pass vs `canned-x11-linked` fail (`ldd` lists libX11); `results-trailing-text`
  pass (`re.match anchors the start only`); `canned-exit-nonzero` pass (`run_shell_command returns
  e.output when it is non-empty`); `path-split` pass (script earlier on `PATH`, `ldd` reads
  `/usr/local/bin/pmars`); `debian-is-file` and `c-is-dir` both pass. The "21-line C program" is the
  probe's `C_SRC` (`plans/build_pmars_probe.py:151-171` = 21 content lines; `R38CritProbe` §5 records
  the 14→21 correction, and the entry says `21-line` ×3, `14-line` ×0).
- Independent agreement: `R38CritPytest.md` §3 "Result — 22/22, three channels" (pytest 8.4.1, venv
  `uv venv -p 3.13`); `R38CritIndep.md` "22/22 agree" + "3/3 extras predicted then observed".
- Prior art: `R38ScoutPriorArt.md` row 1 = TB2 issue #59 with the `dpkg-dev=1.22.21` apt output (body
  captured at `R38LessonDraft/tb2-issue-59-body.md`); row 10 = the audit naming the provenance gap
  (l.249) and calling `ldd` "reliable" (l.255); row 4 = TB2.1 grader files byte-equal,
  `instruction.md` differs — exactly the LOG's three prior-art sentences.
- Coverage counts: SOURCES rows 107 → 109 (`git show e0a37853:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '`
  → 107; tip → 109; S115/S116 both tier A, status mined); knowledge files 44 → 45 (freeze tree 44,
  tip 45); README index rows 44 → 45; census exit 0 before (`census-before.txt`, 15 W04) and after.
  Frontier sub-bullet narrowed by one task (README round-38 discharge bullet), one coverage-map
  bullet (README:263 "fourth task, build-provenance class"), one PROVINCE paragraph
  (PROVINCE:287-292 "Round38 partial frontier admission").

## 4. Capability rows (SCORECARD "Round-38 capabilities") — each demonstrated at the tip

| Row | My demonstration at `8c7422d` | Matches the row's evidence cell |
|---|---|---|
| `build-provenance-grader-probe` | `python3 plans/build_pmars_probe.py --lane .` → `cases=22 observed_pass=7 observed_fail=15 mismatches=0`, exit 0 | yes; byte-equal re-run confirmed by C2 V2 P10 (`probe_rerun=byte-equal bytes=5537`) |
| `mutant-direction-check` | `python3 plans/mutant_direction_check.py --lane .` → `DIRECTIONS total=22 mislabelled=1`, `N21 … MISLABELLED`, exit 1 | yes (`integrate/direction-check.txt`) |
| `tip-receipt-validator` | `python3 plans/tip_receipts.py --lane .` → `receipts=24 byte_equal=4 differ=0 skipped=20`, control `verdict=differ`, exit 0 | yes, including the tamper control |

First-working round 38 holds for all three: first commits are `e0a3785` (probe), `dc0cdb5`
(mutant_direction_check), `d93b7d6` (tip_receipts) — all round-38 commits.

## 5. No-harm sentence (SCORECARD "Other axes held…") — every instrument re-run at the tip

`round37_c1_verify` → `MUTANTS total=55 killed=55 survived=0`, `PREDICATE C1 pass`, exit 0
(receipt `r37-c1-verify-tip-8c7422d.txt`); `round37_c2_verify` → `checks=7 defects=0`, pass, exit 0
(`r37-c2-verify-tip-8c7422d.txt`); `round36_c2_verify` → `checks=6 defects=0`, pass; `anchor_digest_check`
→ `rows=109 tokens=17 defects=0`; `ledger_tip` → `rows=9 closed=9 observed_pass=9 mismatches=0`;
census → exit 0; `sha256sum -c .ufo/waves/round-38/claims/frozen-digests.txt` → 8/8 `OK`. All seven
match the SCORECARD sentence and `measure-final.txt`.

## 6. Frontier / routed / assimilation / tool-use claims (LOG)

- `## Errata (round 38)` exists on `corpus/knowledge/tb2-git-webserver-grader.md:293`; Q28/Q29 exist
  in `corpus/QUALITY.md:455,501`; the witness-picked round-37 label verified in place
  (`tb2-git-webserver-grader.md:107` = `| instruction.md:9 | enforced | …` beside `CASE token-in-body
  … observed=pass` in the round-37 receipt); V7's derived-label rule shown able to fail
  (`R38MapErratum/controls.txt` Control B → `bad=['results-format: labelled enforced, receipt derives
  partly']`, Control C present).
- D3: `R38AnchorBind.md` adds `digest-wrong-capture` and rebuilds M4b/M5; D4: `R38LedgerTip.md` §4
  "Before / after, same machine, same seconds", exit-2 refusal; D6: PROVINCE "Reported out (round 38)"
  block has exactly 16 sibling-surface rows; D1: `git ls-files .ufo/waves/round-37/falsify | wc -l`
  → 380.
- Assimilation: `considerthese/2026-10-25.md` proposal 2(c) is verbatim "includes a tip-receipt
  validator (every `corpus/evidence/**` receipt re-run and byte-compared)" and 2(b) is the
  pre-registration block — both as the lesson describes; merge re-screen `R38MergeRescreen.md`:
  "admit 2 (rows 1–2), hold 5 (rows 3–7), refuse 5 (rows 8–12)", package unchanged since `ba6779f0`
  (verified at the read-only source repo: `git -C /home/vgpnk/Projects/shokuknow log -1 -- merge/kengaku`
  → `ba6779f0 2026-10-24`); collisions file 31 ids; quarantine slice 2 rows.
- Tool use: `gcc --version` → 16.2.1; `bwrap --version` → 0.13.1; libX11 present (`ldconfig -p` → 4
  `libX11.so` entries); `plans/pkg_gate.py:276` = `uv run --no-project --with biopython==1.85`;
  `R38CritPytest.md` pins pytest 8.4.1 + pytest-json-ctrf 0.3.5 in a `uv venv -p 3.13`.

## 7. SHONEN.md

All four pointers resolve at the tip: `SKILL.md` present; `LOG.md:7` (round-4 end-to-end eval entry);
`corpus/lessons/round-8-aggregator-box3-coldrun.md:48` = `## Box-3 verdict`; `PROVINCE.md:129` =
`### Adjacent`. The four `[~]` partials are honest judgements, not falsifiable counts. 0 mismatches.

## 8. Disputes recorded, NOT counted as mismatches

1. **C2 "class" framing** (`R38CritClaims` §3 D5 calls "a fourth grader class" a category slide; the
   new executed edge would be the `ldd` scan). My check partially supports the critic — `ldd` has 0
   hits in `corpus/README.md` at the freeze — but the critic's own component table mis-maps
   presence/directory-shape to round 37 (that grader checks a stdout substring, not presence/shape),
   and `R37PlanNext.md:21` itself priced the candidate as "a fourth TB2 grader of the
   **build-provenance** class". SCORECARD, README and PROVINCE are mutually consistent. Unresolved
   in-lane; not a self-report/repo contradiction I can adjudicate against the self-report.
2. **C2 counter V6 reads an absolute fleet-root census path** (`plans/round38_c2_verify.py:63`,
   `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`) while the frozen predicate
   sentence says "measured on a clean clone of the landing tip" — `R38CritClaims` D9. Verified, but
   (a) the sentence lives in the frozen prereg, not in the SCORECARD/LOG round-38 text, and (b) the
   admitted round-37 counter has the identical constant (`round37_c2_verify.py:58`), so it is a
   carried property, not a round-38 over-claim. Flagged for the round-39 lesson, not counted.
3. **Claims-file sentence "V2's P10 fresh-run byte compare is what makes such a receipt red"**
   (`R38CritClaims` D7: the skip control's V2 fires with five gate clauses, and V6 is red too —
   `control-c2-skip.txt` shows `P10 DEFECT` among `P3/P4/P6/P8` and `V6 DEFECT census_exit=1`).
   Prereg imprecision, disclosed control; the LOG's own sentence about it ("the C2 skip-control ran
   the probe through P10 before the first recorded run, disclosed in the claims") is accurate.

## 9. Verification gaps

- Did not re-open S115/S116 live at the pin (needs network; the lesson's own spot-check item 6 is
  marked pending; `R38ScoutUpstream.md` records the 2026-10-26 equality checks I verified as a report).
- Did not re-run the do-nothing controls (their trees lack `battery38`/the entry by construction);
  their quoted numbers were verified verbatim against the committed control files instead.
- Did not re-run the V7 relabel control at the tip myself; verified the committed control output
  (`R38MapErratum/controls.txt` Control B/C red) instead.
- `R38CritClaims` §1's per-cell advertising audit was spot-checked (N01, N08, N16 + the two false Q24
  citations), not re-derived cell by cell for all 22.

## 10. Count

Claim groups checked: 41 (chain/freeze 8, C1 5, C2 7, capabilities 3+first-working, no-harm 7,
frontier/routed 6, assimilation 3, tool use 1, SHONEN 1). **Mismatches counted: 0.** The self-report's
numbers were measured at `d93b7d68` and every one of them still reproduces at the landing tip
`8c7422d`, including all three capability rows demonstrated fresh.

VERDICT: self-report-mismatches-0
