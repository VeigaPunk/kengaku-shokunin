author: hyaku closure (non-author integrator, @m_opus)

# Round 38 — non-author closure spot-check (kengaku, 2026-10-26)

Measured against lane tip `1fa7af4528a5a5fe4e15a630caf33bacee7a05b9` (before: `fc1174f52b150999bef91f2e81da78732ca0eb9f`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-26T02:26:17-03:00 launch kengaku round=38 pgid=1126675 driver=hyaku-inline attempt=1` ·
`2026-10-26T03:15:53-03:00 complete kengaku round=38; hyaku-inline attempt=1`.
Wave-2 (falsify) reports read at closure: 14 files under `.ufo/waves/round-38/falsify/*.md` (untracked; 34 seats
dispatched, the rest still writing at 2026-10-26T06:21Z): F38AnchorFix, F38C1Rerun, F38C1RerunPy313, F38C2Rerun,
F38CritBatD, F38CritBatE, F38CritNoHarmDiff, F38LedgerTip, F38MapV7Control, F38MutDirection, F38ReopenRows,
F38RevLesson, F38ScoutMisroot, F38XMutP. Cited below by seat name.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-38/kengaku.md` | `kengaku-shokunin 121208e56ddc12db61880c02417b4eaeffd7142c 2026-10-26 03:15:19 -0300`; after the lane tip commit (`1fa7af45`, 03:15:02), before the 03:15:53 complete line; on `origin/main` and `origin/master` — ok |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` on the report; `grep -cE '^\s*- \[[ x~]\]' SHONEN.md` | 1 heading; 4 report lines for 4 `SHONEN.md` boxes, all `[~]` with pointers — ok |
| cited lane commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `fc1174f5 21e6251b e0a37853 e95cf550 2c5f4e0b dc0cdb54 d93b7d68 a022ae60 8c7422d7 4d00e6d8 10d2e977 1fa7af45` | 12/12 resolve, 12/12 ancestors; all 11 round commits authored `kengaku-shokunin` |
| pushed | `scripts/hyaku/jj-lane.sh state …`; `git ls-remote origin refs/heads/master` | `local=remote=1fa7af45… ahead=0 behind=0 head=detached tracked=0 untracked=2`; remote `1fa7af45…` |
| uncommitted round work | `git -C lane status --porcelain` | `?? .ufo/waves/round-38/falsify.ready.dispatched`, `?? .ufo/waves/round-38/falsify/` — wave-2 seat outputs, seats still live; not L1 edits, but uncommitted round evidence (R1 below) |
| prompt carries the template contract | `diff templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/kengaku-round-38.md)` (prompt committed `794e9566`) | 10 hunks; every removed template line carries a placeholder (`grep -vc '{{'` over them → 0: `{{FLEET_ROOT}}` 8, `{{LANE}}` 5, `{{ROUND}}` 4, `{{AXES}}` 1); `grep -c '{{'` on the prompt → 0; §6 hyaku addendum and §7 scratch discipline follow — ok |
| minimum report content | read report | work + evidence pointers, landed-changes table tied to `LOG.md`, before→after per claim with counting commands, Sources & frontier, trend verdicts, stale-lane line, tool-install line, round shape (wave 1: 40 seats, 40 reports — `build-results.json` 40 seats 0 dead, 40 `build/*.md`) — ok |

Conformance defects (status-neutral):
- **Report filed before WAVE-DONE falsify** (disclosed, `kengaku.md:72`); wave-2 outputs are untracked in the lane and
  unintegrated — the same shape as round-37 D1 (R1).
- **Measured revision.** `integrate/measure-final.txt` is measured at `d93b7d68`, `integrate/measure-tip2.txt` at
  `10d2e977`. `git diff --stat d93b7d68 1fa7af45 -- . ':!.ufo/waves'` → only `LOG.md`, `SCORECARD.md`,
  `corpus/lessons/round-38.md`; `git diff --stat 10d2e977 1fa7af45 -- . ':!.ufo/waves'` → empty. The measurement
  transfers to the cited tip; I also re-ran the probe at `1fa7af45` (§2).
- **Baseline drift (disclosed).** The freeze `e0a37853` is a child of the round-37 L1's late `21e6251b`, not of
  `fc1174f5`; `git diff --stat fc1174f5 21e6251b -- plans/ corpus/knowledge corpus/SOURCES.md corpus/README.md` → empty,
  so no frozen input moved.
- **Prompt attribution.** The dispatched prompt `.ufo/prompts/kengaku-round-38.md` was committed under the
  `kengaku-shokunin` identity (`794e9566`, 02:26:15, before the launch line); orchestrator-generated prompts are
  integrator-committable — attribution noted, no effect.

Status: `ok`.

## 2. Claims — re-measured vs evidence-verified

Plain measurements over committed bytes (`git show <rev>:…`, `git ls-tree`), my own `git clone --shared` at `1fa7af45`
under `/fast/scratch/hyaku/kengaku-r38-closure/probe` (`status --porcelain --untracked-files=all | wc -l` → 0), and live
re-opens.

| quantity | command | before (`fc1174f5`) | after (`1fa7af45`) | reported |
|---|---|---|---|---|
| SOURCES registry rows | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 107 | 109 | 107→109 ✓ |
| tier / status histogram; malformed; duplicate ids | CORPUS census awk | A=91 B=14 C=2; mined=91 queued=8 rejected=8; 0; none | A=93 B=14 C=2; mined=93 queued=8 rejected=8; 0; none | tier A +2, both `mined` ✓ |
| knowledge files / README index rows | `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'`; `git show <rev>:corpus/README.md \| grep -cE '^\| \`knowledge/[^\`]+\` \|'` | 44 / 44 | 45 / 45 | 44→45 ✓ |
| removed lines in lane-authored docs | `git diff --numstat fc1174f5 1fa7af45 -- SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md corpus/{SOURCES,README,QUALITY}.md corpus/knowledge corpus/lessons` | — | `+35/0 +82/0 +61/0 +56/0 +67/0 +23/0 +2/0 +342/0 +155/0 +20/0 +77/0`; `SHONEN.md` absent (unchanged) | append-only ✓ (`F38CritNoHarmDiff` per-commit: 0 removed) |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | exit 0, 15 W04 (`claims/census-before.txt`) | exit 0, 15 W04, `kengaku ok`; `diff` of the W04 id sets → identical | ✓ |

- **C1 (calibration) — evidence-verified, not executed; frozen predicate NOT met.** `plans/round38_c1_verify.py`
  (`round38-c1-mutants`, `SKILL.md:583`) and `plans/pkg_gate.py` are registered gates, so I did not run them. Committed
  evidence: `integrate/measure-final.txt` (clean clone of `d93b7d68`, `untracked_in_clone=0`): `PINS total=14
  mismatched=0`, `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=21 survived=1
  invalid=0 null_detected=0`, `MUTANT N21 D5 silence SURVIVED`, `PREDICATE C1 fail`, `exit=1`; same at `10d2e977`
  (`measure-tip2.txt`). Before: `claims/control-c1-nothing.txt` `killed=0 survived=22`; `control-c1-gate-edited.txt`
  `invalid=22`. Plain cross-checks I ran: `sha256sum -c .ufo/waves/round-38/claims/frozen-digests.txt` in my clone →
  8/8 OK (gate, both round-38 counters, probe, spec, dry table, both round-37 counters); `git diff --stat e0a37853
  1fa7af45 --` those eight paths, `plans/round-38-claims.md` and `claims/` → empty; `git cat-file -e
  e0a37853:plans/battery38` fails (battery written after the freeze). Static read of the N21 site
  (`plans/pkg_gate.py:347-349`, `pinned = any(… for parts in (row.split() for row in sums.splitlines()))`) against the
  kill rule (`round38_c1_verify.py:202-204`): restricting `any` to `splitlines()[:1]` can only turn `pinned` from True
  to False, so the mutant's D5 DEFECT set always contains the reference's and the `silence` leg (reference DEFECT,
  mutant not) is unreachable — the lane's explanation is correct and the honest stop is the right frozen outcome. Wave
  2 independently: `F38C1Rerun` re-run byte-identical to the receipt (`c1-rerun-fail-killed-21/22`),
  `F38C1RerunPy313` interpreters agree, `F38MutDirection` confirms N21 is witnessed only as `mirror`
  (`integrate/n21-mirror-diagnostic.txt` 22/22 is post-hoc, not the frozen rule). **Not verified (honest stop);
  score 8 → 8 held; no relabel after scoring.** Limits on the 21 kills: `R38CritClaims` §2 in-process monkeypatch
  reaches `killed=20` (counter alone gameable); `F38CritBatE` D1/D2 — N11's and N09's `adv` sentences overstate what
  the frozen gate enforces; `F38XMutP` 20 non-frozen P1–P8 mutants, 17 killed / 3 survived.
- **C2 (coverage) — re-measured (probe) + evidence-verified (counter).** In my clone at `1fa7af45`: `python3
  plans/build_pmars_probe.py --lane . --work <scratch>` (registered **probe**, `SKILL.md:582`) exit 0, `cmp` with
  `corpus/evidence/round38/build-pmars-probe.txt` → identical, last line `cases=22 observed_pass=7 observed_fail=15
  mismatches=0`; `--dry` byte-identical to `build-pmars-dry-cases-freeze.txt`; `(cd corpus/evidence/round38/tb2-build-pmars
  && sha256sum -c SHA256SUMS)` 5/5 OK. Counter `round38_c2_verify.py` is a registered gate (`SKILL.md:584`) —
  evidence-verified: `measure-final.txt` `V1 ok … V7 ok rows=7 tags=7 bad=0`, `checks=7 defects=0`, `PREDICATE C2 pass`,
  `exit=0` (same at `10d2e977`); before `control-c2-nothing.txt` `checks=7 defects=4` (V2, V3, V4, V7), skip-control
  `defects=2`. Wave 2: `F38C2Rerun` predicate reproduces, three probe re-runs byte-equal (one under `env -i`), no-op and
  fail-injected graders flip 15/18 verdicts (verdicts are caused by the grader), before-control reproduces;
  `F38MapV7Control` five map mutants 5/5 turn V7 red; `F38ReopenRows` S115/S116 2/2 rows, 2/2 quotes. Entry provenance
  trio first (`source:` S115, S116, `verified-at: 2026-10-26`, `recheck: 180d …`), README index row `corpus/README.md:71`,
  coverage bullet `:263`. **Verified.** Score 7 → 7 held (L0 cap `kengaku | round-33`).
- **Frontier/routed fixes (not claims).** D2: Q28 + `## Errata (round 38)` on `tb2-git-webserver-grader.md`, V7 shown red
  (`F38MapV7Control`). D3: `anchor_digest_check.py` catches cross-row substitution the round-37 tool missed
  (`F38AnchorFix` `anchor-cross-row-caught`), residual F1 below. D4: `ledger_tip.py` detached clone ok
  (`F38LedgerTip`), residual F1 below. Capabilities: `build-provenance-grader-probe` (re-run by me, byte-equal),
  `mutant-direction-check` (committed receipt `integrate/direction-check.txt` exit 1 on N21; `F38C1Rerun`
  `rerun-direction-check.txt`), `tip-receipt-validator` (`measure-tip2.txt` `receipts=24 byte_equal=4 differ=0
  skipped=20`; tamper control `build/R38TipReceipts/tip-receipts-tamper-control.txt` → `differ`).

### No-harm audit

`git diff fc1174f5 1fa7af45 -- SCORECARD.md`: +61/−0 — round-37 wave-2 outcome (appended by the round-37 L1 in
`21e6251b`), the round-38 section stating C1 honest stop (calibration held 8) and C2 pass (coverage held 7), three
capability rows (first-working round 38), `### Planned (round 39)`; every other axis stated held (novelty 7, depth 9,
operability 8, freshness 8, adjacency 8). No removed line in any lane-authored doc (table above). No-harm receipts at the
tip (`measure-tip2.txt`): round-37 C1 `killed=55/55` pass, round-37 C2 pass, round-36 C2 pass, anchor `rows=109
tokens=17 defects=0`, ledger-tip `mismatches=0`, census exit 0; `integrate/r37-attribution-at-tip.txt` `ATTRIBUTED 55/55`.

### Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| calibration (C1) | **unchanged** | frozen predicate not met (`killed=21 survived=1`, `PREDICATE C1 fail`, committed and re-run by wave 2); honest stop, N21 named and not relabelled, Q29 check shown red; score held 8; not harmed — nothing frozen edited, no score moved |
| coverage (C2) | **improved** | probe re-run byte-equal at the tip, dry table byte-equal, captures 5/5, S115/S116 re-opened live (§3), knowledge/index 44→45, registry 107→109; fourth TB2 task moved frontier→core; score 7→7 held by the L0 cap |
| novelty | unchanged | no claim |
| depth | unchanged | SKILL §Build-provenance decision table added, not claimed |
| operability | unchanged | three capability rows entered with demonstrations; not claimed |
| freshness | unchanged | not claimed; the entry's recheck command reds as written (`F38ReopenRows` F38R-2, R4) |
| adjacency | unchanged | PROVINCE sibling report-out (D6), not claimed |

No axis harmed. C2 verifies; C1 does not (honest stop). Neither claim is exploratory. Round **not admitted**.

## 3. Discernment spot-check (`round-38.md` `## Gate`)

| item · decision | re-opened source | agree/disagree | reason |
|---|---|---|---|
| `knowledge/tb2-build-pmars-grader.md` · **Admitted** | the entry at `1fa7af45`; probe re-run (byte-equal); live `environment/Dockerfile:9` at `2fd12b88` | **agree** | sources, captures and the 22-case receipt reproduce; map rows all `partly`, each derived over every tagged case (V7 green, 5/5 mutants red); live Dockerfile `:9` reads `COPY warriors/flashpaper.red warriors/rave.red /app/`, as the entry's "fabricated by construction" limit cites; contestable `no-x11` tag on `canned-x11-dlopen` disclosed, not hidden |
| S115 `tests/test_outputs.py` · **Admitted (mined)** | `curl` of the pinned raw URL at `2fd12b88`, `sha256sum`, `sed -n 46p` | **agree** | live = row = capture = manifest `d9d2796d…f4e85`, 85 lines; `:46` `assert re.match(r"Results: \d+ \d+ \d+", battle_result), (` verbatim minus indent (7 words) |
| S116 `instruction.md` · **Admitted (mined)** | `curl` of the pinned raw URL, `sed -n 9p` | **agree** | live = row = capture = manifest `16068505…3b82`, 9 lines; `:9` "We'll verify the binary has no X11 dependencies, uses Debian sources, and that the debugger works properly." exact (17 words) |
| TB2 issue #59 · **Refused as a row** | `gh api repos/harbor-framework/terminal-bench-2/issues/59` | **agree** | title "`build-pmars` failing with oracle solution", open, 2026-04-13; body is the oracle `solve.sh` apt pin failing (`E: Version '1.22.21' for 'dpkg-dev' was not found`), nothing about `test_outputs.py`; no entry statement rests on it |
| `JonathanGabor/terminal-bench-2-audit` `audit_results/20260120_125158/audit.txt` · **Refused as a row** | GitHub contents API → raw `main` (blob `d94c8e66`), `sed -n 247,258p` | **agree** | `:249` "There's no direct verification that the binary was compiled from the specific source in `/app`"; `:255` "The X11 dependency check via `ldd` is reliable." — a static LLM rating with no executed case, partly contradicted by `canned-x11-dlopen` (`observed=pass`, receipt `:9`); right to cite as prior statement and not to row it (also unpinned: `main`) |

New SOURCES rows re-opened: S115, S116 (both). Both URLs resolve, digests match live and capture, quotes verbatim at their
stated lines and ≤25 words. Census exit 0, `kengaku ok`, the same 15 W04 as before.

**Discernment conclusion:** 3/3 sampled admits and 2/2 sampled refusals agree. Last round's outside disagreement (D2,
witness-picked map label) became `QUALITY.md` Q28, citing `round-37-verifier-spotcheck.md` §5 and shown red; this
round's freeze defect became Q29, citing `round-38.md` §Mistakes and shown red. Caveat: the order-of-operations mistake
recurred although `round-37.md:42` carried a rule forward, and the lesson misstates that prior fix (`F38RevLesson`
Defect 1) — routed (R3).

## 4. Trend verdicts

- **expansion — improved.** One admitted entry on ground the coverage map held as Frontier (fourth TB2 grader, first whose
  graded state is a built artefact plus a source tree), S115/S116 `mined` and re-opened live, three capability rows
  entered with demonstrations (one re-run by me).
- **quality — improved.** The weaker round-37 entry is corrected by an appended erratum backed by a forward rule (Q28/V7,
  shown red 5/5); cross-row anchor substitution and detached-clone ledger red are fixed with red-before evidence; the new
  entry re-verifies (probe byte-equal, captures equal live). Residuals that keep "Closed" overstated: D3 accepts either
  digest on a multi-locator row (`F38AnchorFix` F1), D4 control mode still reads an unbound `master` silently
  (`F38LedgerTip` F1), and the entry's recheck command reds as written (`F38ReopenRows` F38R-2). None is an admitted
  entry found false; all routed.
- **discernment — improved.** Spot-check agrees on admits and rejects; both outside/own disagreements became grounded
  criteria (Q28, Q29). The recurrence of a mined mistake is the counterweight (R3).

## 5. Routed defects (lane fixes next round; status-neutral)

1. **R1 — wave-2 outputs uncommitted and unintegrated** (recurrence of round-37 D1). Commit
   `.ufo/waves/round-38/falsify/` and `falsify.ready.dispatched` under the round-39 entry and integrate the findings
   below; the remaining ~20 seats' reports were not available to this closure.
2. **R2 — C1 re-freeze.** Carry N21 as `mirror`; add the `F38XMutP` survivors (X01 P1, X05 P3, X15 P7) and the
   round-37/38 extra survivors; run battery modules out of process (`R38CritClaims` §2); reword N11/N09 `adv` cells to
   what the gate enforces (`F38CritBatE` D1/D2); fix the 3 `adv` cells with no advertising sentence; state each direction
   laxer/stricter at freeze (Q29). `F38MutDirection`: the direction check's mislabel signal has one path (m1, m2
   survive) — add a redundant leg before it is load-bearing.
3. **R3 — order-of-operations recurrence.** `round-37.md:42`'s rule forward ("a control that executes a frozen instrument
   keeps the run as a receipt") was not followed; the round-38 lesson row 2 misstates the prior fix (`F38RevLesson`
   Defect 1) and lists `census-before.txt` among "all red" controls (Defect 2). Append a correction and turn the lint into
   a gate with a red-before state.
4. **R4 — recheck command reds as written.** `sha256sum -c corpus/evidence/round38/tb2-build-pmars/SHA256SUMS` from the lane
   root fails (bare basenames); the same wording sits in the round-35/36/37 TB2 entries (`F38ReopenRows` F38R-2). Append
   corrected recheck lines; TB2.1 comparison unpinned (F38R-3).
5. **R5 — D3/D4 residuals.** `anchor_digest_check.py` unions digests over every locator a row names (`F38AnchorFix` F1);
   `ledger_tip.py --lane` reads an existing but stale `refs/heads/master` with no provenance line (`F38LedgerTip` F1, F2).
   Qualify "Closed" in an appended note and fix.
6. **R6 — carried.** C2 counter admits an informed filler package (`R38CritC2Counter` §1); `R36CritScope` F3–F5 wording
   still open; wave-2 scratch under `/fast/scratch/hyaku/kengaku-r38` (22 GB at 06:20Z, live seats) must be gone at advance.
7. **SHONEN (for the operator).** All four boxes remain `[~]`. The end-to-end-task box now has non-author-checkable,
   byte-equal probe re-runs in three consecutive rounds (36 regex-log, 37 git-webserver, 38 build-pmars — the last re-run
   by this closure). I did not tick it; promotion is operator-owned.
