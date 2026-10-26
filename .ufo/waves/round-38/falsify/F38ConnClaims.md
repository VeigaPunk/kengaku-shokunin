# F38ConnClaims — cross-claim consistency attack (kengaku r38 wave 2, 2026-10-26)

Seat: connector (leaf). Attacked tip: `8c7422d7a646515d80af44844e8ecc8a1fc1d30a` (falsify-dispatch target,
commit `4d00e6d`). Method: independent re-measure of both counters + direction check on a clean `--no-local`
clone of the attacked tip (scratch `/fast/scratch/hyaku/kengaku-r38/F38ConnClaims`, removed), plus
digest/count/quote verification of every frozen number across claims, SCORECARD, LOG, lesson, entry, README,
SOURCES, controls and receipts.

## Axes

Calibration only: do the same numbers (22 mutants, 22 cases, 7/15, S115/S116, hashes) say the same thing in
every document, and do independent commands reproduce them at the attacked tip?

## Evidence — every number, its documents, and the command that checked it

### C1 numbers (22 mutants, 21/1, fixtures 64→86, PINS 14)

| number | documents | independent check |
|---|---|---|
| `MUTANTS total=22 killed=0 survived=22` before | claims; `claims/control-c1-nothing.txt`; SCORECARD C1 row | receipt read: `killed=0 survived=22`, `BATTERY fixtures=64` |
| `MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0`, `PREDICATE C1 fail` after | claims (as honest stop); `integrate/measure-final.txt` (TIP d93b7d68); `integrate/measure-tip2.txt` (TIP 10d2e97); LOG r38; SCORECARD r38; lesson title/header | re-ran at attacked tip: `python3 plans/round38_c1_verify.py --lane . --work $S/work` → identical lines (`falsify/F38ConnClaims/c1-rerun.txt`); per-mutant kill lines diff byte-equal to `measure-final.txt` (`PERMUTANT-MATCH`) |
| `BATTERY fixtures=86` (64+22) | measure receipts; LOG; SCORECARD | re-run prints `fixtures=86`; `comm -23` of fixture names 86 vs 64 → exactly 22 new, all `b1run/d4m/d5m/mainx/p10a/p10b/p3m/p4a/p4b/p5m/p6m/p7m-` prefixed |
| 12 battery modules | claims ("12 modules"); LOG ("twelve wave-1 executor seats"); commit `dc0cdb54` | `ls plans/battery38/*.py \| wc -l` → 12; `git show --stat dc0cdb54 -- plans/battery38` → 12 files |
| `PINS total=14 mismatched=0` | claims frozen predicate; measure receipts; SCORECARD | re-run prints `PINS total=14 mismatched=0` |
| N21 survivor; frozen `silence` but `observed=mirror`, `DIRECTIONS total=22 mislabelled=1` | claims kill rule; lesson Mistakes row 1; LOG; SCORECARD capability row; `integrate/direction-check.txt`; `integrate/n21-mirror-diagnostic.txt` | re-ran `plans/mutant_direction_check.py` at tip → `DIR N21 D5 declared=silence observed=mirror MISLABELLED`, body diff byte-equal to `direction-check.txt` (`DIR-BODY-MATCH`); relabelled-scratch diagnostic shows 22/22, disclosed as post-hoc |
| `invalid=22` (gate-edited control) | lesson controls list; `claims/control-c1-gate-edited.txt` | receipt read: `PINS ... mismatched=1 first=plans/pkg_gate.py`, `invalid=22` |
| no-harm r37 C1 `killed=55/55` | claims kill rule; measure receipts; SCORECARD no-harm line | `measure-final.txt` and `measure-tip2.txt` both show `MUTANTS total=55 killed=55 ... PREDICATE C1 pass` |

### C2 numbers (22 cases, 7/15, checks 7, defects 4→0, 5537 bytes)

| number | documents | independent check |
|---|---|---|
| `cases=22 observed_pass=7 observed_fail=15 mismatches=0` | task; claims; receipt `corpus/evidence/round38/build-pmars-probe.txt`; README:71,451; entry Summary; LOG; SCORECARD; SKILL.md capability row | receipt: 22 `CASE` lines, 7 `observed=pass`, 15 `observed=fail`, 22 `match=yes`, 0 `match=no`, footer `cases=22 observed_pass=7 observed_fail=15 mismatches=0` |
| before `checks=7 defects=4` (V2,V3,V4,V7) | claims; SCORECARD C2 row; `claims/control-c2-nothing.txt` | receipt read: V2/V3/V4/V7 DEFECT |
| skip control `checks=7 defects=2`, V2+V6 red, V7 green | claims disclosure; lesson row 2 + controls list; `claims/control-c2-skip.txt` | receipt read: `V2 DEFECT`, `V6 DEFECT census_exit=1`, `V7 ok` |
| after `checks=7 defects=0`, `PREDICATE C2 pass` | claims; measure receipts; LOG; SCORECARD; lesson | re-ran `plans/round38_c2_verify.py` at attacked tip → `checks=7 defects=0`, V1–V7 all ok (`c2-rerun.txt`) |
| receipt 5537 bytes, byte-equal re-run | `measure-final.txt` gate P10 `bytes=5537`; `tip_receipts.py` output `equal bytes=5537` | `wc -c corpus/evidence/round38/build-pmars-probe.txt` → 5537 |
| dry table 22 cases, 7 predicted pass / 15 fail | claims (`93b4b60c…`); V5 `dry_byte_equal=True` | `grep -c '^CASE'` → 22; `predicted=pass` 7 / `predicted=fail` 15 |
| V7 map 7 rows / 7 tags derived from all violating cases | claims (D2 fix); entry map; QUALITY Q28 | counter `V7 ok rows=7 tags=7`; entry map rows 143–149 = 7 rows, 7 distinct tags |

### Hashes and tips

| hash | where cited | check |
|---|---|---|
| freeze `e0a378539a45cc9388c66cfba22f44275131de23` | claims header; task; LOG; SCORECARD; lesson | `git merge-base --is-ancestor` vs attacked tip → ancestor; `git diff e0a37853 8c7422d7 -- <6 frozen files>` → empty; receipt at freeze absent: `git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt` → rc 128 (lesson row 2 verified) |
| landed/measured tip `d93b7d68dacfd6a23ec2cf732a4615d6c732c73e` | measure-final header; SCORECARD; LOG; lesson | `git diff d93b7d68 8c7422d7 -- plans corpus` → only `corpus/lessons/round-38.md` +77 (no counter/probe/corpus input changes), so the measurement transfers to the attacked tip; `measure-tip2.txt` at HEAD `10d2e97` re-confirms identical numbers |
| first recorded probe run `e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b` | claims; task; LOG; SCORECARD; lesson; SKILL.md | commit exists; message: "first recorded build-pmars probe run on a clean clone of e0a37853 (cases=22 observed_pass=7 observed_fail=15 mismatches=0; second run byte-equal)"; `--stat` adds only the receipt |
| baseline `fc1174f52b150999bef91f2e81da78732ca0eb9f`; r37 L1 `21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9`; battery commit `dc0cdb54` | claims; lesson header; LOG | all resolve as commits; `dc0cdb54` message matches LOG citation |
| frozen digests: gate `ea638822…`, r38 c1 `8069739990…`, r38 c2 `d906d55f…`, probe `32f0771c…`, spec `bd9bfe71…`, dry table `93b4b60c…`, r37 c1 `dbc9f719…`, r37 c2 `b8cba11a…` | claims body (abbrev.); `claims/frozen-digests.txt` (full); SCORECARD | `sha256sum` of all 8 files at attacked tip = `frozen-digests.txt` byte-identical (`digests-at-tip.txt`) |
| TB2 pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` | claims; SOURCES S115/S116; entry; receipt header; README | present verbatim in all five |
| S115 sha256 `d9d2796d…f4e85`, S116 sha256 `1606850…3b82` | SOURCES rows 130–131; lesson rows | `sha256sum` of captures matches; `sha256sum -c SHA256SUMS` 5/5 OK; quoted lines exact: `test_outputs.py:46` and `instruction.md:9`; quote word counts 7/17 correct |

### Corpus counts

| count | documents | check |
|---|---|---|
| SOURCES 107→109, knowledge 44→45, README index 44→45 | SCORECARD C2 row; lesson Census; measure-final tail (`registry_rows=109 knowledge_files=45 index_rows=45`) | at attacked tip: `grep -c '^| S' corpus/SOURCES.md` → 109; `ls corpus/knowledge/*.md \| wc -l` → 45; README index grep → 45; at freeze via `git show e0a37853:...` → 107/44/44 |
| census exit 0, 15 W04 before and after | lesson; controls | `grep -c W04 claims/census-before.txt` → 15; `integrate/census-after.txt` → 15, both `kengaku ok` exit 0 |
| tip_receipts `receipts=24 byte_equal=4 differ=0 skipped=20` | LOG; SCORECARD capability row; lesson assimilation row; measure receipts | identical line in `measure-final.txt` and `measure-tip2.txt`; tamper control `differ` present |
| anchor check `rows=109 tokens=17 defects=0`; ledger `rows=9 closed=9 observed_pass=9 mismatches=0` | SCORECARD no-harm; LOG; lesson D3/D4 rows | identical lines in both measure receipts; R38AnchorBind/R38LedgerTip reports agree (`digest-wrong-capture`, before/after exit-2) |
| wave-1 build "40 seats, 40 reports, 0 dead"; battery "22 fixtures, dc0cdb54"; sibling report-out 16 surfaces; upstream 5/5 byte-equal; pytest 8.4.1 agrees 22/22; indep re-derivation 22/22 + 3/3 | commit `8c7422d7` message; LOG; SCORECARD; lesson | `ls .ufo/waves/round-38/build/*.md \| wc -l` → 40; R38SiblingCite table → 16 rows; R38ScoutUpstream verdict "5/5 byte-equal"; R38CritPytest "pytest-agree 22/22"; R38CritIndep "22/22 agree" |
| r37 falsify closure `git ls-files .ufo/waves/round-37/falsify \| wc -l` → 380 | lesson D1 row | command output 380 |
| "21-line" canned program everywhere (the "14-line" correction) | entry (3×), README:71 (2×), LOG; lesson/integration note | `grep -R '14-line'` → no hits; "21-line" in all citing docs |

## Findings

1. **No undisclosed cross-document drift.** Every attacked number (22 mutants N01–N22, 21/1 with N21 the
   survivor, 22 cases 7/15/0, checks 7 defects 4→0, fixtures 64→86, PINS 14, S115/S116 pins and quotes,
   receipt 5537 bytes, 107→109/44→45/44→45, tip_receipts 24/4/0/20, all nine commit ids, all 8 frozen
   digests) says the same thing in claims, SCORECARD, LOG, lesson, entry, README, SOURCES, SKILL.md, the
   controls and the measure receipts — and each reproduces under my own commands at the attacked tip.
2. **One disclosed in-round discrepancy (not hidden drift):** the frozen claims' §C1 prose "13 non-equivalent
   survivors … one diagnostic … B1, B2, B5, B6, B7, B8" sums to 20 ≠ 22. It is mined as lesson Mistakes row 4
   with corrected arithmetic 16+1+6−1=22; verified: R38CritClaims per-clause counts sum to 16
   (1+4+1+2+1+3+2+2), the counter's MUTANTS rows carry 17 distinct `F37XMut*` citations + 6 shapes, and the
   frozen list (what the counter scores) is unchanged. SCORECARD/LOG do not repeat the bad arithmetic.
3. **Tip-sequence note (not drift):** docs consistently cite `d93b7d68` for measure-final while this wave was
   dispatched against `8c7422d7`; `git diff d93b7d68 8c7422d7 -- plans corpus` touches only
   `corpus/lessons/round-38.md` (+77), and `measure-tip2.txt` at HEAD `10d2e97` re-confirms every number, so
   the measurement stands at the attacked tip.

## Receipts

`falsify/F38ConnClaims/`: `c1-rerun.txt`, `c2-rerun.txt`, `dir-rerun.txt` (independent re-runs at the
attacked tip), `digests-at-tip.txt` (tip sha256 set, byte-identical to `claims/frozen-digests.txt`).
Scratch clone `/fast/scratch/hyaku/kengaku-r38/F38ConnClaims` removed. No lane files edited; no installs.

VERDICT: cross-doc-drift-0 undisclosed (one disclosed in-round: claims §C1 source arithmetic 13+1+6=20≠22, mined lesson Mistakes row 4, corrected 16+1+6−1=22 verified against R38CritClaims and the counter)
