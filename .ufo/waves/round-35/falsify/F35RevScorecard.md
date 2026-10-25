# F35RevScorecard — calibration review of the landed round-35 self-assessment (wave 2, falsify)

Lane tip `dfee6fff631ebc5f623ba4506e5c7992a215401c` (master). Scope: every round-35 statement in
`SCORECARD.md` (round-35 section :1178–1200, capability rows :562–563, D4 correction :1176) and
`SHONEN.md`, each checked against observed state by re-running the counter/command it cites.

Method: live-lane read-only counter runs (no lane writes, no git state mutations) plus one
throwaway fixture per the fixture rule — `D=$(mktemp -d /tmp/k35f-XXXX)`;
`git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"`;
`git -C "$D/lane" sparse-checkout set --no-cone plans/ corpus/ SCORECARD.md SHONEN.md LOG.md
PROVINCE.md .ufo/waves/round-34/ .ufo/waves/round-35/`; `checkout -q dfee6ff…`;
`git -C "$D/lane" rev-parse --show-toplevel` == `$D/lane` verified before any run; fixture removed
(`rm -rf` exact `$D` only). No tools installed (uv + `biopython==1.85` already cached — the grader's
own pinned dependency; nothing new to record).

## Findings

### F1 — MODERATE: C2's green predicate is misattributed to `dfcd294c`; the ledger is red at that commit

`SCORECARD.md:1188` (C2 row) states: "→ after `rows=5 closed=5 observed_pass=5 mismatches=0`,
`PREDICATE C2 pass`, exit 0 **at `dfcd294c`**".

Observed at `dfcd294c` (fixture clone, `HEAD=dfcd294c60a00215c55bc4ce0b620440cd5e402f`):

```
$ python3 $D/lane/plans/defect_ledger.py --lane $D/lane
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=fail agree=NO erratum_lines=1 r35_mistake_row=False
rows=5 closed=5 observed_pass=4 mismatches=1
PREDICATE C2 fail
LEDGER-EXIT=1
```

Root cause: D5's check (`plans/defect_ledger.py` `r34_d5`) requires an S091 row in
`corpus/lessons/round-35.md` §Mistakes **and** the round-34 erratum; `corpus/lessons/round-35.md`
does not exist at `dfcd294c` — `git log --follow -- corpus/lessons/round-35.md` names `4fe72a9` as
its first commit. The green state is first observed at `4fe72a9a` (fixture:
`rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`) and at the tip (live and
fixture, same line, exit 0). The frozen prereg itself lists "a round-35 lesson Mistakes row" among
C2's surfaces (`plans/round-35-claims.md` §Separability), so C2's landing was split across
`dfcd294c` (ledger rows, erratum, D4 correction) and `4fe72a9a` (round-35 lesson); the SCORECARD
attributes the whole green state to the earlier commit alone.

Asymmetry that isolates the defect: the C1 row's parallel claim "exit 0 at `4fe72a9a`"
(`SCORECARD.md:1187`) **is** commit-true (fixture-verified at `4fe72a9a`: `checks=6 defects=0`,
`PREDICATE C1 pass`). Only the C2 attribution is wrong. This is the same defect class
(scorecard-misattribution) as routed defect R34-D4 the round was closing.

Nuance recorded honestly: whether the live working tree held `round-35.md` untracked at
`dfcd294c`-time is unrecorded (untracked state leaves no history); either way the predicate is not
a property of the cited commit — a re-run at that commit exits 1. The same misattribution is
propagated to `LOG.md:1013-1014` ("C2 landed at `dfcd294c`: … `PREDICATE C2 pass`") — outside this
seat's file scope, noted for the integrator. C2's admission itself is unaffected: the frozen
predicate is met at the landing tip. Fix is a one-commit-id correction or a rewording ("green from
`4fe72a9a`").

### Caveats (verified true of the landed tree; not counted as mismatches)

- **Hardening H6 is working-tree-sensitive.** `SCORECARD.md:1193-1194`: hardening "passes on the
  landed lane" — TRUE on a clean checkout of the tip (fixture: `H6 ok untracked_anywhere=0`,
  `hardening run=6 failed=0`, exit 0; also at `4fe72a9a`). But in the live lane today the same
  command exits 1: `H6 FAIL untracked_anywhere=55` — all 55 are wave-2 falsify scratch under
  `.ufo/waves/` (`git status --porcelain` → 5 collapsed `??` dirs, all `.ufo/waves`), i.e. current
  wave state, not landed round-35 content. Also: the committed receipt
  `corpus/evidence/round35/hardening-counterexamples.txt` block 1 shows `H6 skipped` (`run=5
  failed=0`) because the generator `.ufo/waves/round-35/claims/hardening-counterexamples.sh`
  hard-codes `--skip H6`; the SCORECARD sentence omits that skip (harmless — H6 passes on the
  clean landed tree — but a reader diffing receipt vs bare re-run should know why they differ).
- **Hardening counterexamples reproduce.** Re-ran the committed generator: output byte-equal to
  the receipt (`diff` clean, exit 0) — all five seat counterexamples fail exactly as the receipt
  and `SCORECARD.md:1193-1194` claim.
- **SHONEN pointer anchors are section headings.** `SHONEN.md:10` cites
  `corpus/lessons/round-8-aggregator-box3-coldrun.md:48` = the `## Box-3 verdict` heading (the
  supporting `[x]` verdict text is line 49); `SHONEN.md:12` cites `PROVINCE.md:129` = the
  `### Adjacent` heading. Both resolve to sections whose content supports the items — consistent
  with each other, noted for precision only.
- **Disk-full incident (host intel).** A freeze-state fixture attempt (`checkout 11d6453`) tried to
  materialize the 109k-path round-34 mirror tree (present in the tree at freeze, deleted at
  `dfcd294c`) and died on "No space left on device" (/tmp was at 99%, 2.1G free). That run's
  numbers were discarded as contaminated; /tmp back to 98% (2.7G free) after removing my fixture.
  Seats checking out pre-`dfcd294c` commits with broad sparse patterns will hit this.

## Verified agreements (each with the command that would have shown disagreement)

| SCORECARD/SHONEN statement (location) | Command | Observed |
|---|---|---|
| C1 after `checks=6 defects=0`, `PREDICATE C1 pass`, exit 0 at `4fe72a9a` (:1187) | `python3 plans/round35_c1_verify.py --lane .` (live; fixture at tip and at `4fe72a9a`) | `V1..V6 ok` / `checks=6 defects=0` / `PREDICATE C1 pass` / exit 0, all three runs |
| C1 before `checks=6 defects=5` exit 1 (:1187) | `cat .ufo/waves/round-35/claims/control-c1-nothing.txt`; counter re-run at `dfcd294c` (pre-C1) | receipt: `checks=6 defects=5`, `PREDICATE C1 fail`, `exit=1`; fixture at `dfcd294c`: same 5 defects (V1–V5 red, V6 ok) |
| C2 after green at tip (:1188) | `python3 plans/defect_ledger.py --lane .` (live + fixture) | `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`, exit 0 |
| C2 before `rows=5 closed=0 observed_pass=0 mismatches=0` exit 1 (:1188) | `cat .ufo/waves/round-35/claims/control-c2-nothing.txt` | exact match, `PREDICATE C2 fail`, `exit=1` |
| Skip/flip controls cannot reach target (claims file; :1187/:1188 context) | `cat control-c1-skip.txt control-c2-flip.txt` | `checks=6 defects=5` exit=1; `rows=5 closed=5 observed_pass=1 mismatches=4` exit=1 (D1 green-in-clone disclosed) |
| Probe capability row: `cases=18 observed_pass=5 observed_fail=13 mismatches=0`, receipt byte-equal via V5 (:562) | `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` | exit 0; `diff` vs `corpus/evidence/round35/tb2-grader-probe.txt` clean; summary line carried verbatim in the entry (grep count 1) |
| Hardening "passes on the landed lane" (:1193-1194) | fixture at tip and `4fe72a9a`, no flags | `hardening run=6 failed=0`, exit 0 (H6 ok, untracked=0) |
| Hardening "fails on each of five seat counterexamples" (:1193-1194) | `bash .ufo/waves/round-35/claims/hardening-counterexamples.sh` | byte-equal to committed receipt; CE1–CE5 fail as labelled |
| D4 correction: draft selftest green at `R34C2CounterDraft.md:8`; harness red at `R34MutC2Harness.md:12` (cont. :13); row `R34-D4` in ledger (:1176) | `sed -n '8p' …R34C2CounterDraft.md`; `sed -n '12,13p' …R34MutC2Harness.md`; `grep R34-D4 corpus/defects.jsonl` | `SELFTEST cases=10 failed=0` on :8; `…exit 1, green gate fails:` / `SELFTEST green failed (1)…` on :12-13; row present, class `scorecard-misattribution`; both files under `.ufo/waves/round-34/build/` |
| "eight one-word quotes and `junk` teaches cells pass V2/V3, stub passes V5 (`R35CritControls`, `checks=6 defects=0`)" (:1187) | read `.ufo/waves/round-35/build/R35CritControls.md` | junk package → `V1..V6 ok`, `checks=6 defects=0`, `PREDICATE C1 pass`; 8× one-word `import` quotes from one line; teaches cell `junk`; 385 B stub probe |
| "D4/D5 checks accept labelled-but-false lines (`R35CritC2`); D1 is a working-tree check" (:1188) | read `.ufo/waves/round-35/build/R35CritC2.md`; read `plans/defect_ledger.py` | EXP1/EXP2 false lines pass both checks; D1 = `git ls-files --others` over round-34 paths (working tree) |
| Registry 97 → 100 rows, tier A +3 (:1191) | `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]'`; tier-A grep; rows diff | 97→100; tier A 82→85; diff = exactly +S105 +S106 +S107 |
| knowledge files / index rows 41/41 → 42/42 (:1192) | `git ls-tree -r <rev> --name-only \| grep -c '^corpus/knowledge/.*\.md$'`; README `\| \`knowledge/` count | 41→42 files; 41→42 rows |
| census exit 0 before and after (15 W04) (:1192) | `cat corpus/evidence/round35/census-{before,after}.txt`; fresh `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | both receipts 15 W04 + `ok` + `exit=0`; fresh run exit 0, 15 W04 |
| Coverage capped by open L0 question `.ufo/l0-questions.md:163` (:1183) | `grep -n 'kengaku \| round-33' /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` | line 163 = the kengaku round-33 coverage-cap decision packet, still open; fleet-root-relative path is the lane's documented convention (`corpus/QUALITY.md` R15 "Run from the fleet root") |
| Axis selection: coverage 7 tied novelty 7 lowest; no stagnation waiver (:1180-1181) | SCORECARD round-24 basis table + round-34 section; saturation line 8 | consistent; novelty 7 < 8 → nudge inactive |
| Baseline/freeze commits (:1178-1179) | `git log --oneline`; hardening H1 | `58a19f3` and `11d6453` in history; `changed_since_freeze=0` for all three frozen tools |
| S105–S107 "byte-identical to the round-34 captures" (claims file, inherited by :1187) | `sha256sum` both capture trees | all three files identical; digests equal the C1 pins (`44a05a24…`, `9ede4664…`, `1bb2af1d…`) |
| Capabilities entered, first-working round 35 (:1190-1191) | capability table rows | both rows present, `35` in First-working column |
| SHONEN items (:5-12) | `SKILL.md` structure; `sed -n '7p' LOG.md`; lesson/PROVINCE pointers | decision tables :23/:53, anti-patterns :60, checklist :588, cited sources :631; LOG.md:7 = round-4 "executed first authored eval (closes SHONEN 'end-to-end task' checkbox)"; coldrun :48/:49 and PROVINCE :129 as noted above; PROVINCE round-35 paragraph present (:230-239) |
| "round-34 D1–D5 closed" (:1188) | `cat corpus/defects.jsonl` | 5 rows, all `status=closed`, `closed_round=35` |

## Residual risk / verification gaps

- The counters' token-level weaknesses (V2/V3/V5 junk-passability; D4/D5 labelled-but-false lines)
  are real but already disclosed in the SCORECARD itself and priced as "no score raise" — I
  verified the disclosures, did not re-derive them beyond the committed critic reports and one
  receipt re-run.
- Whether the live working tree held `corpus/lessons/round-35.md` untracked at `dfcd294c`-time is
  unrecordable; F1 stands on the commit-level re-run either way.
- Standing axis scores (novelty/depth/operability/freshness/adjacency "held") were checked for
  consistency with their recorded basis, not re-audited from scratch — no round-35 statement
  moves them, and nothing observed contradicts the "held" claims.

**Mismatch count: 1** (F1).

VERDICT: scorecard-mismatches-1
