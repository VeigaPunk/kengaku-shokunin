# F39ConnClaims — cross-document drift (round 39, wave 2, falsify)

Seat: F39ConnClaims (connector). Scope: the same fact as stated in
`plans/round-39-claims.md` (freeze `088f7c36`), `corpus/lessons/round-39.md`,
SCORECARD round-39 section, LOG round-39 entry, `corpus/knowledge/tb2-git-leak-recovery-grader.md`,
`corpus/README.md` / PROVINCE round-39 text, and `.ufo/waves/round-39/integrate/measure-final.txt` —
counts, hashes, verdicts, case names. All lane reads were read-only; no lane file edited; no scratch
clone needed (all facts verified from the committed tree and its git history).

## Method

Every numeric/hash claim was cross-checked against the committed bytes and the measurement file:

- `git rev-parse` of `088f7c3`, `6a1eb5e`, `34158b0`, `a6832f5`, `acf4375` → 40-hex values.
- `git log --format='%H %P' -n 1 088f7c3` → freeze parent = `ef2fba062069…`.
- `sha256sum` of `plans/git_leak_probe.py`, `plans/pkg_gate.py`,
  `corpus/evidence/round39/git-leak-dry-cases-freeze.txt`,
  `corpus/evidence/round39/tb2-git-leak-recovery/{test_outputs.py,instruction.md}`.
- `(cd corpus/evidence/round39/tb2-git-leak-recovery && sha256sum -c SHA256SUMS)` → 7/7 OK.
- `wc -c corpus/evidence/round39/git-leak-probe.txt` → 5867.
- Dry-table parse (25 cases; `violates=` tag counts; empty-`violates=` set).
- `cat` of all files under `.ufo/waves/round-39/claims/` (controls, census-before, frozen-digests).
- Counts: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 111;
  `ls corpus/knowledge | wc -l` → 46; `grep -c '^| `knowledge/' corpus/README.md` → 46.

## Agreement matrix (all interlock)

| Fact | Stated in | Verified value | Agreement |
|---|---|---|---|
| Freeze hash | claims, lesson, LOG(abbrev), measure-final `order_check` | `088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8` | yes |
| Freeze parent = `ef2fba0` (not `b2bdd425`) | lesson "Baseline drift" | `git log %H %P` shows parent `ef2fba062069…` | yes |
| First recorded probe run | lesson, LOG, measure-final `order_check` | `6a1eb5e1da4a435940b821e28530c31f3411549c` | yes |
| First-run artefact | lesson → `.ufo/waves/round-39/first-run/first-run.txt` | exists; committed in `6a1eb5e` (`git log --follow`); rc1=0 rc2=0 byte-equal; sha256 matches receipt file | yes |
| Probe digest `4961a50f…` | claims | `4961a50f28ae85e8…` | yes |
| Gate digest `ea638822…` | claims, SCORECARD | `ea63882240e67e99…` | yes |
| Dry-table digest `e92a5d6d…` | claims | `e92a5d6d62cb81e3…` | yes |
| S117 digest / quote | lesson gate table | `dc7b01c1b9dbb0c1…`; quote `test_outputs.py:16` matches entry | yes |
| S118 digest / quote | lesson gate table | `54ac693fd26a4c00…`; quote `instruction.md:4` matches entry | yes |
| Probe cases | claims (25; predicted 13/12), lesson/LOG/SCORECARD/PROVINCE/corpus-README (observed 13/12) | dry table + receipt: 25 cases, 13 predicted/observed pass, 12 fail, 0 mismatches | yes |
| Second run byte-equal | lesson, LOG, SCORECARD, PROVINCE, measure-final P10 | `probe_rerun=byte-equal bytes=5867`; receipt = 5867 bytes | yes |
| C1 landing predicate | claims vs measure-final/LOG/SCORECARD | `PINS total=26 mismatched=0`; `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0`; `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`; `PREDICATE C1 pass`; exit 0 | yes |
| C1 do-nothing control | claims, lesson, SCORECARD | `control-c1-nothing.txt`: pins 26/0, `fixtures=86`, `killed=3 survived=4`, fail, exit 1 | yes |
| C1 gate-edited control | claims, lesson | `control-c1-gate-edited.txt`: `mismatched=1`, `invalid=7`, fail | yes |
| C1 hostile-inproc control | claims, lesson | `control-c1-hostile-inproc.txt`: `fixtures=88`, `killed=3 survived=4` unchanged | yes |
| C1 audit | LOG, SCORECARD, lesson spot-check | measure-final `AUDIT C1 clean`, `nondeterministic_kills=0`, `PINS final total=26 mismatched=0` | yes |
| C2 landing predicate | claims vs measure-final/LOG/SCORECARD | `checks=7 defects=0`; `PREDICATE C2 pass`; exit 0; V7 rows=4 tags=4 | yes |
| C2 do-nothing control | claims, lesson, SCORECARD | `control-c2-nothing.txt`: `checks=7 defects=4`, V2/V3/V4/V7 DEFECT, fail, exit 1 | yes |
| Case names (25) | dry table, receipt, entry findings, lesson | identical 25 name set in dry table and receipt; entry/lesson cite only names present | yes |
| Tag weights | entry ("secret-gone 16, recover-secret 5, messages-untouched 3, files-untouched 2"; 22 of 25 tagged; empty = oracle-solve-sh/clean-echo/flag-padded-crlf) | dry-table parse: 16/5/3/2, 22 tagged, empty set exactly those three | yes |
| Census | lesson, SCORECARD, measure-final | registry 109→111 (SOURCES now 111), knowledge 45→46 (46), index 45→46 (46); before/after exit 0, 15 W04 (both census-before.txt and measure-final) | yes |
| Order gate | lesson, SCORECARD, measure-final | round 38: `ORDER HIT …control-c2-skip.txt@e0a378539a45:11`, FAIL, exit 1; round 39: PASS, exit 0 | yes |
| No-harm re-runs | claims, lesson spot-check, SCORECARD | measure-final: round-37 C1 `killed=55` pass; round-38 C1 `killed=21 survived=1` fail; round-38/37/36 C2 pass; anchor `rows=111 tokens=19 defects=0`; ledger-tip `rows=9 … mismatches=0`; frozen digests 9/9 OK | yes |
| Batteries/names | claims vs measure-final | M01←d5m-n21-manifest-row-2, M02←p1m-second-pin-appended-bytes, M03←p3m39-quote-one-word-above-upper-bound, M04←p7m39-s105-two-source-lines, M05←p23-p2-receipt-deleted, M06←r36-P0, M07←d5m39-tagged-quote-span; battery39 modules p1m/p3m39/p7m39/d5m39 | yes |
| Captures | claims ("7 files + SHA256SUMS"), corpus-README | capture dir: 7 files + SHA256SUMS; manifest 7/7 OK | yes |
| Advertised-only recount | LOG, SCORECARD, lesson Mistakes row 4 | all three: 2 → 0; sentences reach M02/M03/M05/M06, not M01/M04/M07 | yes |
| S117/S118 open time | claims, lesson | 2026-10-26 03:27 -03 by L1 | yes |
| Report run/order | claims vs git history | commits: `088f7c3` (freeze) < `6a1eb5e` (first run) < `7504738` (wave-1) < `34158b0` (battery39 + C2 package) | yes |

## Disagreements found

1. **Spec-vs-document landing-tip hash.** The wave-2 dispatch text says the lane is
   "measured at lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (branch master)". Every document
   says the measurement was taken at a clean clone of `34158b0ca0f7b527d60af0e612511f7f27aebcbc`
   (measure-final.txt:1 `TIP 34158b0…`; measure-final `ledger_tip` `REF AUDIT ref=refs/heads/master
   rev=34158b0… state=match`; lesson Mistakes row 5 calls `34158b0` "the landing tip"). `git log`
   confirms `a6832f5` is the *commit that adds* lesson/SCORECARD/LOG + measure-final, i.e. it is a
   descendant of the measured tip, and HEAD is now `acf4375` (wave-2 dispatch). No document claims any
   counter was run at `a6832f53`; the "measured at a6832f53" attribution is therefore inaccurate. Re-running
   the frozen counters at `a6832f53` would reproduce the same numbers (no frozen input moved between the two
   commits), so this is a provenance wording defect, not a predicate failure.

All other checked facts agree across the seven documents; no drift in counts, hashes, verdicts, or case
names was found between them.

VERDICT: cross-doc-drift-1
