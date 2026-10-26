# F37ConnCrossCheck — cross-artifact cross-check (kengaku round 37, wave 2, falsify)

Seat: F37ConnCrossCheck (connector, leaf). Date: 2026-10-26.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; integration tip `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`
(pushed, branch master). Wave-1 reports read at `.ufo/waves/round-37/build/*.md` (committed `67cbe7a`, a
descendant of the tip; the landing tree at `357deceb` is what was checked for "fixed"). All lane reads were
read-only; counters were NOT re-run (receipts already committed at the tip were used). Scratch clone:
`/fast/scratch/hyaku/kengaku-r37/F37ConnCrossCheck/fx/lane` at `357deceb`, verified
`git rev-parse --show-toplevel` == the clone before any write; deleted at the end. No tools installed
(nothing needed); no pacman; no lane file written.

Axes named (godspeed): **calibration** (every claim's limit and every defect's disposition is traced to a
committed artifact, not asserted), **coverage** (every wave-1 defect-naming report is dispositioned, not
sampled).

Note on the landing tip vs the measurement receipt: `integrate/measure-final.txt` names `TIP 5c7d5d75`;
`357deceb` differs only by the post-hoc attribution-audit commit and the wave specs
(`git log --oneline 5c7d5d75..357deceb`), none of which touches the frozen instruments — the round-37
verifier spot-check (`corpus/lessons/round-37-verifier-spotcheck.md` §1) confirmed the measurement transfers.

---

## Cross-check 1 — lesson Mistakes → QUALITY criteria

Round 37 added exactly two QUALITY criteria (command: `grep -c '^## Round37 criterion' corpus/QUALITY.md`
→ `2`), and both cite lesson rows that exist:

| criterion | cites | lesson row (as ordered in `corpus/lessons/round-37.md` ## Mistakes) | match |
|---|---|---|---|
| Q26 — an anchor digest resolves to committed bytes | "Lesson: `corpus/lessons/round-37.md` §Mistakes (1). Supersedes: none." (`corpus/QUALITY.md:405`) | row 1 — reference-drift / transcription (S110 63-hex + S070/S072/S073/S074) | ✓ |
| Q27 — an advertised defect class is held only when a fixture kills its silence mutant | "Lesson: `corpus/lessons/round-37.md` §Mistakes (2)…" (`corpus/QUALITY.md:447`) | row 2 — vacuous, the frozen round-36 battery demonstrated 5 of 55 advertised gate classes | ✓ |

Forward direction (each criterion has a lesson row): **2/2**.

Reverse direction (each lesson row has a criterion): the round-37 Mistakes table has **7 rows** (read
directly from the table); only rows 1–2 have criteria. Rows 3–7 have none:

| row | class | disposition in lieu of a criterion |
|---|---|---|
| 3 | order-of-operations — the C2 skip-control executed the frozen probe before the first recorded run | a "Rule forward" recorded inside the lesson itself ("a control that executes a frozen instrument keeps the run as a receipt"); the probe's freeze-digest re-pinning is cited (V5, V2 P10) |
| 4 | derived-number — two totals readable for the same mutant id | a rule recorded inside the lesson ("the only admissible C1 number is the frozen predicate line measured on a clean clone") |
| 5 | count — fixture matrix measured expectation in ids, checker answered in lines | fixed inside the instrument (matrix fixed; final receipt §5 eleven falsifier cases `ok`) |
| 6 | vacuous — frozen C2 counter admits an informed filler and reads an unpinned spec | recorded as a limit (SCORECARD "Limits" C2-counter bullet; round-38 plan: "the next counter must pin it") |
| 7 | vacuous — frozen C1 counter counts a kill without attributing it | recorded as a limit (SCORECARD "Limits" C1 bullet) + post-hoc audit landed at the tip (see §3) |

So the strict bidirectional claim ("each criterion has a lesson row **and vice versa**") fails 5/7 in
reverse. This matches the lane's standing convention rather than a round-37 regression: `corpus/QUALITY.md`'s
own contract is one-directional ("Every criterion cites the lesson that produced it"), and prior rounds also
carry many more Mistakes rows than criteria (e.g. round-35's lesson has 6 Mistakes rows for its one
criterion Q23; round-33's has ~15 for Q22). Every row 3–7 is nonetheless dispositioned in a committed
artifact. **No unaddressed item from this cross-check; the vice-versa gap is reported as the finding.**

## Cross-check 2 — the claims' limits → report-facing SCORECARD text

The frozen claims name exactly two limits.

- **C1** (`plans/round-37-claims.md` §C1): "demonstration is observational …, not proof that each check is
  the right check." → **carried** in SCORECARD twice: the `gate-mutation-harness` capability row ends "Not
  proof that any check is the right check." (`SCORECARD.md:566`), and the round-37 Limits bullet restates "a
  kill records a result difference, not a reason." Not dropped.
- **C2** (`plans/round-37-claims.md` §C2): "the probe shows what the grader's verdict depends on with
  `apt-get` and `expect` absent; it never runs the oracle or a real git push, so it does not show that the
  intended path passes." → the mechanism half is **carried** in the SCORECARD round-37 Limits bullet ("the
  probe never runs the oracle, the task image or a real git push; in the sandbox the git step never
  executes, so 'the git step's failure is ignored' is a static reading, not an observation"); the
  consequence clause "does not show that the intended path passes" is **absent from SCORECARD's round-37
  text** but is carried in two other report-facing artifacts: `SKILL.md` §"Service-class TB2 grader — round 37"
  ("the probe shows what the verdict depends on, never that the intended path passes") and the entry
  (`corpus/knowledge/tb2-git-webserver-grader.md:183`). No freeze limit is fully dropped from the
  report-facing set; one clause is compressed out of SCORECARD itself (flagged, not counted).

## Cross-check 3 — wave-1 defect-naming findings → fixed / recorded-as-limit / unaddressed

Ten wave-1 reports carry VERDICT lines naming defects (method: `grep -n 'VERDICT' .ufo/waves/round-37/build/*.md`).
Disposition of each, checked against the tree at `357deceb`:

| report | VERDICT | disposition |
|---|---|---|
| R37CritScope | `scope-inside-13-wording-fixes` (F1–F13) | **FIXED.** Entry carries F1 (`:32-50` "records one new edge class in the lane's **executed** grader sample", "narrows … (89 tasks carry `tests/test.sh`; 3 are now read)"), F2 (exact 9-pass breakdown `:27-35`), F3/F4 (requirement-map prose `:108-121`), F5 (`:133-136` "This is one reachable environment, not the task image's"), F7 (Negative space `:225-240`), F8 (`:2` "lines 1–92"; `:47-48` task.toml timeouts/image/internet-policy). README carries F6 (`:288` "narrowed for that one task only") and F9 (`:261` third-task row, "3 of the 89 … not breadth"). PROVINCE carries F10 (`:264` "Round37 partial frontier admission"). SCORECARD carries F11 (coverage cell names `coverage/surfaces` vs `coverage/constructs: unchanged`). SKILL carries F12 (`:755` — decision table is past-tense observations of the frozen run; "What a green means here" bounds, no recipe). F13 verified: `grep -n 'DockerOracle' SKILL.md corpus/README.md corpus/knowledge/tb2-git-webserver-grader.md` → no hit; only `PROVINCE.md:285` ("routed, not absorbed"). Sub-gap: F1's "record the claims sentence in the round report under a dated erratum line" has no home (the round report is not in the lane; no other artifact carries the claims overstatement) — noted in §4. |
| R37CritCases | `cases-22-confounded-4-uncovered-extra-4/4` | **RECORDED.** Entry §"Case independence" (`:201-203`) names the seat and records the three weaker labels (`static-file-no-git`, `wrong-port-8081`, the `:62`/`:68` and `:79`/`:85` double echoes) plus the four post-hoc cases ("sharpen the map; none changes a frozen verdict"); SCORECARD Limits records the static-reading limit and "four case labels are weaker than they read"; SKILL records the case-independence limits. Sub-gap: the §6 "fold the six fixtures into the round-38 case table" is not in the binding round-38 plan — noted in §4. |
| R37CritC1Battery | `c1-counter-gameable-yes-9-attacks` | **RECORDED + post-hoc mitigation at the tip.** Not repaired inside the frozen counter (kill rule); SCORECARD Limits C1 bullet + lesson Mistakes row 7 record it; `plans/round37_c1_attribution.py` landed at `357deceb` (`ATTRIBUTED 55/55 UNATTRIBUTED=0` `integrate/c1-attribution.txt`; hostile battery `ATTRIBUTED 6/55 UNATTRIBUTED=49` under a frozen `PREDICATE C1 pass`, `integrate/c1-attribution-hostile.txt`); lesson row 7 + SCORECARD `### Planned (round 38)`: round 38's counter must attribute kills. |
| R37CritC2Counter | `cheapest-filler-c2-0-defects` | **RECORDED.** SCORECARD Limits "C2 counter" bullet + lesson Mistakes row 6 record the informed-filler and unpinned-spec limits; spec digest re-checked at the tip (`measure-final.txt`: `pkg-spec-r37.json` = freeze digest `4c61d103…`); round-38 plan: "the next counter must pin it". |
| R37DockerOracle | `real-image-oracle-pass-static-pass-token-pass` | **RECORDED as routed**, with limits: LOG round-37 ("Routed, not absorbed"), SCORECARD Limits C2 bullet, PROVINCE `:285`, entry `:240`, lesson Gate row ("Refused for the corpus; routed"). |
| R37RevClaims | `claims-review-1-false-green-2-false-red` | **FR-1 FIXED** (`plans/battery37/p910.py:36-37` stages the lane's `.gitignore` with `__pycache__/`, docstring `:14-22` explains the P9-poisoning it prevents). **FG-1 and FR-2 UNADDRESSED** (below). |
| R37RevC2Counter | `c2-counter-review-14-false-green-9-false-red-5` | F1, F3 recorded (SCORECARD + lesson row 6); F4/F14 protocol-covered by the predicates' "on a clean clone" sentence; F6 subsumed by the landed lane-wide `plans/anchor_digest_check.py`. Remaining 9 **UNADDRESSED** (below). |
| R37RevProbeCode | `probe-review-2-defects-8-risks` | D1, D2 **UNADDRESSED** (below); the 8 risks noted in §4. |
| R37MutProbeHarness | `probe-harness-mutants-2/6` | 4 undetected mutants **UNADDRESSED** (below). |
| R37ConnDefects | `classes-13-recurring-9-unchecked-3` | The 3 unchecked recurring classes **UNADDRESSED** (below); its proposal-2(b) sketch is recorded as unbuilt (lesson Gate: "2(b) and 2(c) stay unbuilt"). |

Citation sweep confirming the unaddressed set: `grep -rln 'R37RevC2Counter\|R37RevProbeCode\|R37MutProbeHarness\|R37ConnDefects\|R37RevClaims' SCORECARD.md LOG.md corpus/lessons/round-37.md SKILL.md PROVINCE.md corpus/README.md corpus/knowledge/tb2-git-webserver-grader.md .ufo/waves/round-37/integrate/ .ufo/reports/` → **no output** (none of these five reports, nor any paraphrase — checked: `substring test`, `drops stderr`/`discards.*stderr`, `sys.modules`, `newline-normalized`, `duplicate CASE`, `fleet-absolute`, `host-bound` — appears in any landed artifact).

### The unaddressed findings (20)

From **R37RevClaims** (2):
1. **FG-1** — the entry's prose outside the requirement map and quote rows is unchecked; V1–V7 can all pass
   while prose claims are false; the claims' C2 limit names only the probe's limits, not this prose limit.
2. **FR-2** — the knowledge/README parity coupling (gate P8) is global: C2's own V2 reds on *another seat's*
   half-landed entry (a C2 false red), which the claims' Separability paragraph does not state (it discloses
   only the C1 `wrong=1` direction).

From **R37RevC2Counter** (9) — all are round-38-counter inputs per that report's own "highest-value fixes"
list, none recorded in any landed artifact:
3. **F2** — V4's "named in the entry" is a bare substring test; `wget-token-in-body` embeds `token-in-body`,
   so a receipt line for the curl case counts as named when the entry never mentions it.
4. **F5** — V4 never recomputes a line's `match=` from its own `predicted`/`observed`; receipt bookkeeping
   is self-reported (`mismatches=0` is the receipt's claim about itself).
5. **F7** — V1 (and gate P5) silently overwrite duplicate manifest lines; dot-prefixed capture files escape
   both.
6. **F8** — V4 counts every CASE line while V7's `observed[]` is last-wins; a duplicated case id can satisfy
   V4's arithmetic while V7 judges the polarity of whichever line is last.
7. **F9** — V5's `dry_byte_equal=True` is newline-normalized on both sides (`text=True` universal newlines);
   the label overstates byte equality (only the raw-bytes digest pin binds the file).
8. **F10** — V7's citation grammar extracts only all-lowercase-hyphen backtick content; `` `git push` ``
   extracts nothing (false "cites no case") and a bare `` `curl` `` yields an "unknown case" defect.
9. **F11** — V3 requires exactly one sha256 token byte-identical; an honest anchor citing a second digest
   (e.g. an upstream tree digest) reds.
10. **F12** — V6 couples C2 to whole-registry hygiene: any E-finding on any row of the lane's registry fails C2.
11. **F13** — V6 hardcodes the fleet-absolute census script path
    (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`); C2 cannot pass where the script is absent
    and the verdict can change when the unpinned script changes, with zero lane change.

From **R37RevProbeCode** (2) — both are defects in the frozen probe, recorded nowhere but the build report:
12. **D1** — `run_case` captures and drops `r.stderr` (`plans/git_webserver_probe.py:237-239`); the fail-fast
    path prints stdout only, so a sandbox/setup failure's cause is invisible.
13. **D2** — the harness imports the captured grader without `sys.modules` registration (`:172-174`); on
    CPython 3.14 a dataclass-using capture would print `VERDICT fail error=AttributeError` where pytest
    would pass (latent wrong verdict; unreachable at the frozen digests).

From **R37MutProbeHarness** (4) — all four mutants are undetected by the frozen probe, recorded nowhere but
the build report:
14. **M-c** — the probe has no internal detection of a missing `--unshare-net`; on a host serving anything on
    `:8080`, every case's verdict could be silently shaped by that host service (the one finding the seat
    calls "the one real coverage finding").
15. **M-d** — stubbed `apt-get`/`expect` on the case PATH run undetected (confirms the status-unread
    invariant; benign today).
16. **M-e** — the ready-file-before-bind race is masked by `verify.sh`'s `sleep 2`; undetected across 6 clean
    runs (benign today).
17. **M-f** — removing the HOME override is undetected; `verify.sh`'s `~/.ssh/config` write would move to the
    inherited HOME (confirmed sandbox-private; no host leak observed).

From **R37ConnDefects** (3) — recurring defect classes with no mechanical check this round and no landed
record of the gap:
18. **C4** — scratch leaks (uncommitted round work / committed mirrors): 4 rounds of recurrence, no check.
19. **C6** — report-before-commit / stale tip: closed since r33, but nothing prevents recurrence.
20. **C9** — seat-ledger / round-shape / attribution conformance: 5 rounds of recurrence, no check.

## Minor notes (reported, not counted in the 20)

- F1's second half (a dated erratum line recording the claims' "first service/state grader" overstatement)
  has no home: the round report is not in the lane and no other artifact carries it.
- R37CritCases' "fold the six executed fixtures into the round-38 case table" is not in the binding
  `### Planned (round 38)` block (it covers C1 pinning and a fourth grader only).
- R37RevClaims FR-3 (P10 interpreter choice is host-bound; needs the `biopython==1.85` wheel cached or
  network) is a named residual the reviewer graded "measured non-issue here"; R37CritCases' Python-3.14
  import-shim operability note and R37RevProbeCode's risks R1–R8 sit in the same class.
- `corpus/lessons/round-37.md` §Close was written before wave 2 returned; none of the 20 is integrated there.

## Evidence appendix (commands and outputs)

- Clone: `git clone -q --no-local <lane> $D/lane && git -C $D/lane checkout -q 357deceb3b5…` →
  `git rev-parse HEAD` = `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`; toplevel verified == `$D/lane`.
- QUALITY criteria: `grep -c '^## Round37 criterion' corpus/QUALITY.md` → `2`;
  `grep -n 'Lesson: .corpus/lessons/round-37.md' corpus/QUALITY.md` → `:405` (Q26→§Mistakes (1)), `:447` (Q27→§Mistakes (2)).
- Lesson Mistakes rows: 7 (read directly from `corpus/lessons/round-37.md` ## Mistakes).
- C1 limit carried: `grep -nE 'observational|right check' SCORECARD.md` → `SCORECARD.md:566` "Not proof that
  any check is the right check." (gate-mutation-harness row).
- C2 limit: SCORECARD round-37 Limits bullet (mechanism) + `SKILL.md` §Service-class + entry `:183`
  (consequence clause "never that the intended path passes").
- Attribution audit at tip: `tail -3 .ufo/waves/round-37/integrate/c1-attribution.txt` →
  `ATTRIBUTED 55/55 UNATTRIBUTED=0`, `exit=0`; hostile → `ATTRIBUTED 6/55 UNATTRIBUTED=49` under a frozen
  `PREDICATE C1 pass`.
- FR-1 fix: `plans/battery37/p910.py:14-22` (docstring) and `:36-37` (`_ignore_rule` copies the lane's
  `.gitignore`).
- Unaddressed sweep: `grep -rln 'R37RevC2Counter\|R37RevProbeCode\|R37MutProbeHarness\|R37ConnDefects\|R37RevClaims' SCORECARD.md LOG.md corpus/lessons/round-37.md SKILL.md PROVINCE.md corpus/README.md corpus/knowledge/tb2-git-webserver-grader.md .ufo/waves/round-37/integrate/ .ufo/reports/` → no output;
  `grep -rn 'substring test\|drops stderr\|sys.modules\|newline-normalized\|duplicate CASE\|fleet-absolute\|host-bound' SCORECARD.md LOG.md corpus/lessons/round-37.md SKILL.md PROVINCE.md corpus/README.md corpus/knowledge/tb2-git-webserver-grader.md` → no output.
- Predicate receipt: `.ufo/waves/round-37/integrate/measure-final.txt` carries `BATTERY fixtures=64 wrong=0
  renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`,
  `checks=7 defects=0`, `PREDICATE C2 pass`, both `exit=0` (`grep -c 'MUTANT M.. .* killed by='` → `55`).
- No tools installed this seat (none needed); reads and greps only.

VERDICT: crosscheck-unaddressed-20
