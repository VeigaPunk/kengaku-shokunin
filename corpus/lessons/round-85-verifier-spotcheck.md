author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 85 — verifier spot-check

Reviewed 2026-11-04. Lane before `0de45354d7aff18e4a23a348ec13de3a1f707a44` (BASE), delivered after `c83e39ce9ed57096f35a2d7f462aed435bc8cb34` (AFTER), branch `refs/heads/master`. Fleet report `.ufo/reports/round-85/kengaku.md` is committed as `524448840a73de9e3d260ff1e6476b486e009e6b`. All lane-relative paths below resolve in `kengaku-shokunin/`; `L1/` abbreviates `.ufo/waves/round-85/L1/`.

## Closure

**status=ok; admitted=false; verdict=rejected-honest-stop.** Both full frozen claims are **unprovable**. The narrow member execution and substantive repairs are real; later green executable targets cannot establish the stronger frozen controls, discrimination, unchanged predicates or causal separability. No owned-axis harm is demonstrated. This is a real lane-attributed report, not a completion marker.

No exploratory claim was declared. Neither claim is retrospectively converted to `unprovable-but-better`; no capability, promotion or mint is admitted. The report's honest-stop ruling is upheld. Outside discernment now has an admit/reject sample and is graded improved below; that does not admit either claim.

This review executed plain Git/JSON/text measurements, reopened sources, ran the explicitly required fleet source census, and inspected committed gate evidence. **No lane gate, probe, selftest, mutant battery, grader or sandbox was executed.** Two fresh read-only reviewer seats checked conformance and frozen-claim interpretation; their findings were adjudicated here rather than treated as authority to admit.

## Step-1 conformance

- `git log --format='%an %H' -- .ufo/reports/round-85/kengaku.md` gives `kengaku-shokunin 524448840a73de9e3d260ff1e6476b486e009e6b`. The report author and committer are both `kengaku-shokunin <kengaku@shokunin.local>`. Its author/committer times are `2026-11-04T17:40:49-03:00` / `17:41:21-03:00`, after lane AFTER at `17:40:07-03:00` and before completion.
- The report has one `## SHONEN` heading and four `[~]` lines, one per canonical box. All six required report sections occur in order. Work, LOG/lesson pointers, actual commits and measurable receipts are present: classification **ok**, not failed-marker.
- `git cat-file -t HASH` and `git merge-base --is-ancestor HASH refs/heads/master` succeed for all report-cited lane revisions: `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`, `99a7cb3b0165efe907814947392e6bd98fe45872`, `f88842771a9f0711d3e311550099a68d97e8958b`, `35b1e4e09d7666889e561ede274485aba1e2ad11`, `20eb9ba796324070440c95855e70755f61d059e1`, `1daf0db10bfeb08083629d403539dc59bb248eeb`, `bc9373ba9144eb30f61ee9d2b93eb9aa4e43ae44`, AFTER, BASE, and the receipt's clone revision `dc02d8182890838c4d7609f62aea5d79fbcfc236`. Ancestry was tested against the branch, never a detached HEAD upstream expression.
- `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kengaku-shokunin` before this review's write: `branch=master local=c83e39ce9ed57096f35a2d7f462aed435bc8cb34 remote=c83e39ce9ed57096f35a2d7f462aed435bc8cb34 ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git status --porcelain` is empty. No inherited round work remains uncommitted.
- The dispatched prompt is committed before launch (`04f314bd`); the conformance reviewer compared its rendered prefix against fleet `templates/round-prompt.md`: all 8,304 characters match, followed by `## 6. Campaign addendum`, with no unresolved placeholders. The dispatch-time addendum is present. Mission/axes binding, distinct 1–3 claims, lowest-axis duty, batched L2 floor, commit/push order and scope, L0 channel, report path/filename, commit-before-report, SHONEN, hash citations and lane write scope are embedded. Current later addendum amendments say future launches only; they are not retroactive requirements.
- One 12-seat wave is supported by the committed spec/dispatch, twelve report directories and `L1/settlement.txt`. Role counts are executor 3, scribe 2, reviewer 2, scout/critic/mutation-tester/sentinel/connector 1 each; campaign attack share is 4/12. The result envelope really lacks ids/status/final text. Settlement is evidenced by the retained WAVE-DONE digest, not independently reconstructed model/death counts. Missing metadata stays a disclosed conformance limitation.
- Low/status-neutral defects: four described engineering amendments lack their specific commit-hash binding in the report/LOG; source counts omit their counting command. Change-level logging itself is present through LOG's closing corrections and the referenced lesson; absence of individual hashes does not mean the changes were unlogged. The prompt also retains canonical section-2 large-wave bands alongside the operative run-15 8–16 band; dispatch policy and the addendum explain the 12-seat wave, but the override should explicitly name section 2. See routing below.

Durable dispatch/completion digest copied from the assigned mutable-log evidence:

```text
2026-11-04T16:40:15-03:00 launch kengaku round=85 pgid=2498736 driver=hyaku-inline attempt=1
2026-11-04T17:42:08-03:00 complete kengaku round=85; hyaku-inline attempt=1
```

## Claim rechecks — measurements versus gate-evidence verification

### Independent committed-byte measurements

Commands used `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show REV:PATH`, `cat-file -e REV:PATH`, `ls-tree REV -- PATH`, and plain Python `json`, `re`, `hashlib` parsing; no lane instrument was imported. BASE and AFTER are the full revisions above.

The population measurement was run at both revisions with:

```sh
git show REV:plans/grader-population-ledger.json | jq -c '{members:(.members|length),statuses:(.members|to_entries|group_by(.value.status)|map({status:.[0].value.status,count:length})),serialization:(.members|to_entries|map(select(.value.classes|index("serialization-schema")))|{n:length,k:(map(select(.value.status=="executed"))|length),executed:map(select(.value.status=="executed")|.key)}),member:.members["sqlite-db-truncate"]}'
```

Observed:

| fact | BASE | AFTER |
|---|---|---|
| population | members=88; executed=28; unexecuted=60 | members=88; executed=29; unexecuted=59 |
| serialization-schema | k=1 n=10; executed=`db-wal-recovery` | k=2 n=10; adds `sqlite-db-truncate` |
| sqlite member | unexecuted; reason=unattempted | executed; round=85; receipt=`corpus/evidence/round85/sqlite-db-truncate-probe.txt`; subject=tb2-header; verdict=cases |
| receipt tree entry | absent (`cat-file -e` nonzero) | regular `100644` blob; eight CASE rows; zero predicted/observed-pair mismatches |

A `json.loads(git_show)['members']` row comparison found **only `sqlite-db-truncate` changed**. The report's corrected 28→29 / 60→59 and 1/10→2/10 agree. Its frozen 0/9→1/9 and first-in-class wording do not; the append-only corrections explicitly supersede those errors.

For C2 the plain checks were `cat-file -e` on the four named R84 evidence paths; regex counts of `^- \*\*Q61 ` / `^- \*\*Q62 `; a line-start `writer:` extraction; the dated `R84-V7 (2026-11-04)` correction; literal `add_argument('--FLAG'...)` matching for the four named flags; and the lesson's `## Definition horizon` heading. Observed:

| checkable repair | BASE → AFTER | interpretation |
|---|---|---|
| V1 tracked evidence | 0/4 → 4/4 | real retained round-84 evidence |
| V2 freeze inputs | absent at BASE; all three claims/cases/defects blobs present at `1a45aeb5` and byte-identical to AFTER | freeze-input binding repaired; not proof of the omitted SETUP-fixture leg in C2 v2 |
| V3 instrument | absent at BASE; reproduction code/control evidence present AFTER | behavioral evidence is read separately below; source tokens alone are not proof |
| V5 QUALITY Q61 | 0 rows → 1 | criterion with lesson/considerthese citation and bounded per-entry control; universal standing counter remains unimplemented |
| Q62 | 0 rows → 1 | grounded freeze-input lesson, not a repair of C1 semantic observation |
| V6 writer | `KengakuR84` → `kengaku-L1-round83-admission` | real collision repair; not universal seat-namespace proof |
| V7 dated correction | absent → present | round-84 expansion correction appended, not historical bytes rewritten |
| V8 literal CLI flags | 0/4 → 4/4 | real byte-level repair; not the original frozen gate-verdict check |
| V9 horizon disclosure | absent → present | explicitly prices absence-red versus measured-and-wrong; not an independent behavioral failure demonstration |

The source measurement parsed `git show REV:corpus/SOURCES.md` rows matching `^\|\s*S\d{3,}\s*\|`, stripped the eleven cells, and used `Counter(row[3])` / `Counter(row[7])` for tiers/status. It found rows **263→265**, A **233→235**, B **24→24**, C **6→6**; mined **239→241**, rejected **16→16**, queued **8→8**. All 263 pre-existing row strings are unchanged; only S272/S273 were added. `git ls-tree -r --name-only REV corpus/knowledge/ corpus/lessons/` counted knowledge Markdown **77→77**, lessons **142→143**. These measurements agree with the report's final figures, not its preserved intermediate annotations.

### R85-C1 / coverage — full frozen claim unprovable

The narrow target is supported. `L1/round85_c1_replay.py-before-pinned.txt` records, at BASE with instrument `1daf0db10bfeb08083629d403539dc59bb248eeb`:

```text
TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=8
PREDICATE R85-C1 fail
EXIT 1
```

The corresponding after-pinned file measures that same full instrument/tree revision:

```text
TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0
PREDICATE R85-C1 pass
EXIT 0
```

These are **evidence-verified, not rerun here**. The receipt independently contains the eight matching pairs and pins the captured subject, table and probe. Three instrument SHA256 measurements at AFTER match `L1/final-instrument-sha256.json` and the measured revision:

```text
round85_c1_replay.py                 3f4945ba5b7774489f215623644ee28f6ce60ab6aa0bc6e233797db1d5748e2d
round85_c2_debt.py                   7622c250327cc5eaaa4bbbee6fde18034874fb914f5817acb43d5af9dc83ae5d
round85_sqlite_truncate_probe.py     04d5fc1a78e6bab178005c44bd722bcce1bb5d234b8178aad3b7aed9933d3538
```

`git diff --name-only 1daf0db1 AFTER` prints only the four pinned before/after receipts and `w1-registry.json`; instruments, inputs, ledger and substantive repairs are unchanged. Thus the revision-bound target evidence applies to delivered bytes, while retaining its actual measured revision.

The full frozen claim does not verify:

1. The frozen correct-vector forgery obligation is not demonstrated. `plans/round85_c1_replay.py:349-356` changes `six predicted=6/F observed=6/F` to `6/P,6/P`; that is an internally consistent **wrong** frozen vector, not an observationally identical copy with genuine-looking stamps. Its REPRODUCE rejection proves mismatch detection, not origin authentication. `:273-275` discards `fresh_stamp` and compares only blocks; host/revision stamp presence is not bound provenance. This is not an allegation that this round's actual receipt was forged.
2. Final Q20 evidence at `def5d0ea5fbf49389400663d30c5a2c8820e56a5` reports **C1 mutants 4/5 necessary, exit 1**, not the earlier 5/5. The stale `flip_ledger()` fixture writes `verdict=predicate` while the real counter requires `cases`, leaving an unrelated defect after removing the ledger-status check. Earlier green batteries cannot substitute for final-instrument evidence.
3. The frozen claim's semantic-discrimination sentence overstates the experiment. The score leg is explicitly defined in the freeze as a harness recomputation, so recomputing it is **not by itself a predicate violation**. However, CriticR85 F3's committed strict-type subject experiment leaves the complete vector unchanged: six integer pairs produce F under both internal scores 6 and 0, while the separate harness still prints 6. This refutes the stronger discrimination claim, not the genuine grader-verdict replay. Sixteen printed legs are not sixteen independent internal-score observations.

The narrow execution is real, but admitting a narrowed version would improve/rewrite the round rather than close the frozen claim. **Coverage verdict: unprovable; score 7 held.**

### R85-C2 / calibration — full frozen claim unprovable

Pinned committed receipts, instrument/tree `1daf0db1`, record:

```text
BASE: TARGET ids=8 closed=0 checks_passed=0 indexed=no defects=8
      PREDICATE R85-C2 fail; EXIT 1
AFTER: TARGET ids=8 closed=8 checks_passed=8 indexed=yes defects=0
       PREDICATE R85-C2 pass; EXIT 0
```

The final target is mechanically green, but the original frozen check is not what produced it. V8 originally required the plans-registry predicate **and exit 0**; `plans/round85_c2_debt.py:190-207` now succeeds on four literal flag substrings, using the gate result only as detail. `L1/c2-tip.txt` preserves the earlier `BASE-CHECK v8 GREEN` / sensitivity 7/8; the later 8/8 follows replacement of that check. Commits `da463cbdc1ee9c116fe239fb24f41c99fa0807c7` and `def5d0ea5fbf49389400663d30c5a2c8820e56a5` and the lesson's Closing erratum disclose these post-scoring changes.

V3 also gained a receipt-absent code-only success path (`:144-145`), instead of always executing the frozen forged-control obligation. Its actual successful control runner exits 0, not the frozen cell's stated exit 1. V2 checks freeze presence/identity but omits its promised SETUP-fixture invocation. V6 rejects only a particular seat-name spelling family; V7 does not check the promised date/report; V9 checks token presence rather than substance. The actual writer/correction/horizon repairs deserve the bounded credit in the measurement table, not eight independently substantive frozen discharges.

Causal separation is not established: `L1/revert-test.txt` records C1 green with C2 repairs reverted, but C2 **7/8** with C1 receipt/ledger artifacts reverted (`v3` traceback). Its v2/v3 also read C1-created artifacts directly. A later source-only branch does not backdate successful separation. The report and SCORECARD closing corrections disclose the miss. **Calibration verdict: unprovable; score 10 held.**

## Gate evidence and no-harm review

`SKILL.md:748-750` registers the new probe and both gates, with command, verdict map, selftest spelling, pins, scope and owner. Their existence is conformant; complete current green capability is not asserted.

Evidence read, never executed here:

| committed evidence | observed result and revision boundary |
|---|---|
| `L1/q20-clone.txt`, clone `def5d0ea...` | standard grader 733/0; sources selftest 17/0; registry 15 cases clean; projection 31 clean; benchmark audit 67 clean; gate-timing/state selftests rc=0 |
| same Q20 receipt | touched round83 counter selftest 20 cases / 1 failure; new probe 7 cases / 2 failures; C1 selftest 10 cases / 0 failures, mutants 4/5 necessary rc=1; C2 selftest 6/0 and mutants 3/3 rc=0 |
| `L1/c1-battery.txt` / `c1-mutants.txt` | older 5/5 green is historical, superseded for final-instrument judgment by Q20's red 4/5; four controls reject the fixtures they actually construct |
| `L1/round85_c2_debt.py-{before,after}-pinned.txt` | changed-predicate 0/8→8/8, fail/1→pass/0 at the explicit revisions above; not frozen-predicate admission |
| `L1/population-final.txt` | revision `def5d0ea...`; replayed/located=29, unexecuted=59, defects=0, pass, EXIT 0 |
| `L1/index-final.txt` | revision `def5d0ea...`; knowledge 77/77, lessons 143/143, evidence dirs 76/76, pass, EXIT 0; explicitly says WORKTREE dirty |
| `L1/standing-gates.txt` | earlier population-vocabulary red and stale/missing R74 invocation are not final success evidence; carried state summary is red on `P3c.box.4.pointer.1`, despite state selftest green |

`git diff BASE AFTER -- SCORECARD.md` is an EOF append: **56 additions, zero deletions**. Closing corrections supersede the optimistic rows, class arithmetic, bilateral separation and admission assertions. PROVINCE and SHONEN are unchanged. Existing knowledge bytes change only the one writer line; all 77 entries remain, and the Q13-held entry is not re-admitted. `plans/round83_c2_debt.py` changes only dynamically assembled flags to four equivalent literal `add_argument` calls. Its red Q20 clone selftest has no matched before-clone measurement establishing a regression; new probe failures are new-instrument debt, not proof a previous capability was damaged. No observed axis is graded harmed simply because a gate is red.

| axis | verdict | evidence |
|---|---|---|
| coverage | unprovable | narrow 28→29 located/executed move is real; full frozen controls/discrimination unsupported; score 7 held |
| calibration | unprovable | post-scoring predicate changes, incomplete check obligations and failed separation; score 10 held |
| novelty | unchanged | no new construct, prior-art claim or score increase; score 8 held |
| depth | unchanged | added method/correction detail, no separately verified depth claim; score 10 held |
| operability | unchanged | runnable instruments retained with explicit red batteries; no previous runnable behavior shown harmed and no new capability admitted; score 10 held |
| freshness | unchanged | pinned source reopened, no new live serving-endpoint verification or unmarked freshness loss; score 10 held |
| adjacency | unchanged | committed ConnectorR85 report distinguishes related registry/DB work from member replay; nothing absorbed and PROVINCE unchanged; score 9 held |

## Outside discernment spot-check

Access date 2026-11-04. The upstream URL below was reopened with the static reader, not inferred from a seat's report. The reject's captured source and the actual runtime-lookup command were reopened separately.

| item | Gate decision | reopened source | agree/disagree | reason |
|---|---|---|---|---|
| S273, Gate addendum | admit superseding annotation, tier A code, member replay only | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-db-truncate/tests/test_outputs.py ; local captured source lines 8-31 | agree | The source loads `/app/recover.json`, forms sets and asserts an intersection above six. Exact quote `assert score > 6, "Did not load data correctly"` is on captured-source line 31 and has **9 whitespace-split words**, within 25. Scope excludes solved-task/model/image claims. |
| `adaptive-rejection-sampler` | reject as this host's member-replay candidate | `corpus/evidence/round52/graders/adaptive-rejection-sampler/tests/test_outputs.py:10,73-79,130-136`; `command -v Rscript R` | agree | numpy is imported and Rscript is invoked at lines 74 and 132. Runtime lookup prints no path, exit 1. Refusing this host replay is grounded. The ledger's `no-blocker` label is a bounded detector result, not evidence all runtime dependencies exist; no interpreter was installed or grader executed by this review. |
| S272 historical quote annotation | admit source semantics, later annotation superseded by S273 | same live URL; `corpus/SOURCES.md` S272/S273; lesson Closing erratum/Gate addendum | agree with corrected disposition; disagree with preserved original annotation | Line 30 is blank and the quote has nine words, not six. The error was explicitly corrected before filing by a new immutable superseding row, not left as an unmarked current claim. |

Independently measured capture: **1,097 bytes**, SHA256 `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`; line-31 text equals the reopened source quote and `len(quote.split())=9`. This is a captured-blob digest measurement plus a live semantic/quote re-open, not a newly claimed raw live-byte hash comparison.

Required command actually executed:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
```

Exit **0**; final output `kengaku ok /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`; thirty W04 duplicate-URL/different-scope warnings. This validates the registry's structure, not the frozen claims or source truth. The lane's separate `census-before-replay.txt` is correctly labelled a replay, not a historical capture; its original pre-run is not newly executed here.

## Learning trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | knowledge 77→77; no admitted uncovered-ground entry, capability or frontier move; new source/ledger rows alone do not count |
| quality | unchanged | useful criterion, writer and annotation repairs coexist with unresolved control/check and red-battery debt; no net corpus-quality increase established and no false entry left newly unmarked |
| discernment | improved | this fresh outside sample agrees with a current admit (S273) and the host-grounded reject; S272's old annotation error has a learned, explicit superseding correction. This replaces the report's pre-spotcheck unchanged trend, not either frozen axis verdict |

## Routed defects — next steered round

All are status-neutral conformance/method debt; none permits retuning the frozen round-85 claims or rewriting historical receipts. Owner **kengaku** unless explicitly operator-owned.

- **R85-V1 — C1 final battery and probe fixtures.** Repair `flip_ledger`'s stale verdict vocabulary prospectively and address the new probe's two selftest failures and touched round83 counter's clone failure. Retain the losing receipts and commit revision-bound successor evidence; do not cite historical 5/5 as current. Q20's red results remain the authority for this instrument.
- **R85-V2 — C1 provenance/control sizing.** The promised correct-vector forgery was not tested: `six=6/P` is a changed vector. In a successor freeze, price indistinguishable copies honestly and bind or explicitly bound host/revision stamp assertions. Preserve the genuine replay without calling it authenticated mint provenance or grader-internal-score observation. For internal semantic discrimination, choose prospective observations/cases that can fail that alternative; do not rewrite the frozen case table.
- **R85-V3 — C2 frozen obligations/separation.** Prospectively restore a real gate-verdict requirement for V8, the V2 SETUP fixture, behavioral V3 obligation and honest control-runner exit convention; make V6 seat identities, V7 date/report and V9 disclosure checks substantive. Do not backdate the changed checks' 8/8 or code-only branch as frozen verification. Record the actual shared-artifact dependencies and 7/8 separation loss.
- **R85-V4 — C2 advertised default invocation.** `v1()` passes the default label `worktree` to `git cat-file -e worktree:PATH` (CriticR85 F4); the advertised no-`--rev` command reports real tracked evidence missing. Resolve an actual revision for that leg or prospectively require/document explicit revision. The report does not name this default-mode defect.
- **R85-V5 — registry revision blindness and standing evidence.** The round82 plans-registry gate reads instrument bytes from the working tree even with `--tip`. Keep its base-green failure witness and fix through its owning successor round. Label `standing-gates.txt` as superseded by the revision-bound final population evidence; do not treat its captured `rc=0` wrappers as clean verdicts. Re-pin the carried SHONEN box-4 assertion through the owner; state selftest success is not state-summary success.
- **R85-V6 — scope guards and stamp integrity.** Carry SentinelR85 S1/S2/S4/S6: require a committed regular receipt blob at the measured revision, reject duplicate/unsupported stamp assertions, map timeout to setup/could-not-evaluate, avoid optional Git status locks. S3 trusted-counter identity is a procedural trust-boundary limitation; S5 minimal `/etc`/read-only sandbox root is optional hardening, not demonstrated credential exposure. These findings concern gate acceptance, not a claim this actual regular receipt escaped the repo.
- **R85-V7 — report counting and amendment attribution.** Next report should supply the SOURCES counting command and explicit hash-bound amendment accounting: `217910c513a46b5ff607561136e4beaac056ace0` (V3 exit convention), `da463cbdc1ee9c116fe239fb24f41c99fa0807c7` (V8 byte check), `b1e570972e51525b9a5a28781717883a1aaa043f` (C1 header acceptance), `def5d0ea5fbf49389400663d30c5a2c8820e56a5` (V3 split). The changes are described by LOG/lesson corrections; missing individual hash binding is not missing work. Corrections are appended in the successor record, never edits to this filed report.
- **R85-V8 — wave metadata (orchestrator/operator).** Preserve ids/status/final text and per-seat routing evidence before kernel loss. For this round deaths and answering models remain unrecoverable, not zero. **Operator:** clarify run-15 precedence over canonical section-2 seat bands. The faithful dispatch snapshot is not rewritten.
- **Carried open queue:** R84-V4 Q13 one-wave checker shape (operator/gate owner), coverage cap (`kengaku | round-25/33/51`), mass package-id drift (`kengaku | round-54`), R82-F1 annotation parser blind spot, and the standing TB2 admission counter remain open. V1 tracked evidence, input binding, actual writer, Q61 criterion and dated expansion correction received bounded substantive repairs, but the collective eight-discharge claim remains unverified.

## Promotion and write scope

No promotion/mint, no `[x]`, no edits to lane-authored report, lesson, LOG, SCORECARD, SKILL or PROVINCE. Existing SHONEN boxes do **not** all look fully checkable from the current pointers: the box-4 line pointer is stale and executable-instruction evidence includes red/default-mode failures. Promotion remains operator-owned. Only this non-author spot-check and the prescribed temporary closure JSON/helper-appended MANIFEST entry are written by this closure. No tool was installed or upgraded.
