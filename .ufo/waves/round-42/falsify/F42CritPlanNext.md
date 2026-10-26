# F42CritPlanNext — round-43 plan-data attack (critic, wave 2 falsify)

Seat: `F42CritPlanNext` (critic, leaf). Target: the round-43 plan data. The file
`.ufo/waves/round-42/build/R42PlanNext.md` **does not exist** (the seat ended without a report; the raw
data directory `.ufo/waves/round-42/build/R42PlanNext/` is present). The plan under attack is therefore the
`### Planned (round 43)` block in `SCORECARD.md:1779-1802` plus the raw data that block cites
(`R42PlanNext/feal/feal_run1.txt`, `res_round_close.json`, `wit_rc.txt`, `prior-art/gh_issue_counts.txt`,
`prior-art/issues_detail.txt`). Lane read-only; no lane file was edited.

## Q32 receipt

Envelope (mandated line): `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>`

This seat executed **no** battery/counter/fixture (read-only critique; the only probes are the source
fetches below). Receipt:
- `BEFORE 18:07:02`; `ls -A /home/vgpnk/.local/bin | sha256sum` → `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`
- `AFTER  18:07:04`; same digest (unchanged).
Scratch: `/fast/scratch/hyaku/kengaku-r42/F42CritPlanNext` (created, empty); no writes outside the report dir.

## What was attacked

For each candidate claim in the round-43 planned block: do-nothing-control reachability, Q31 literal
binding, Q29/Q33 direction witnessing, coverage-class novelty vs the eight admitted TB2 graders, and the
wave-1 remediation carry (R42SentinelCounter V1–V3, R42CritC1Counter V1b), plus the two candidate mutant
lists (round_close survivors; u=18 anchor/order behaviours).

## Verified ground truth

1. **Feal grader mechanism (fetch of the pinned source).** Read the real grader at the pin:
   `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/test_outputs.py`.
   It contains: `sys.path.append("/app")`, `sys.path.append("/tests")`, `import attack`, `import feal_in_c`,
   `feal_in_c.create_random_keys()`, then `stolen = attack.attack(feal_in_c.encrypt)` and
   `assert feal_in_c.get_keys()[5] == stolen`. The in-process class claim is **confirmed by source**: the
   agent's Python module is imported and its function called inside the grader's process, and the reference
   C module `feal_in_c` (built at grade time from `tests/feal_module.c` via `setup.py build_ext --inplace`)
   is importable from the same process. `feal_in_c.get_keys()` exposed means `cheat-import-get_keys`
   (`return feal_in_c.get_keys()[5]`) passes trivially. `cheat-clock-seed` passes 5/5 by reconstructing a
   time-seeded libc `srand/rand` schedule and verifying against `F.encrypt`/`encrypt_fn` (host glibc).

2. **The eight admitted TB2 graders** (`corpus/knowledge/tb2-*-grader.md`, rounds 35–42): protein-assembly,
   regex-log, configure-git-webserver, build-pmars, git-leak-recovery, db-wal-recovery,
   constraints-scheduling, circuit-fibsqrt. Grep of all eight for in-process import/`import attack` terms:
   **zero matches** — none imports an agent-authored Python module. Nearest neighbour: regex-log executes the
   agent's regex *file* in-grader (`re.compile`/`findall`), i.e. agent-authored data executed in-process;
   circuit-fibsqrt executes a grader-owned compiled simulator over the agent's data file. So the class "the
   graded artifact is an agent-authored Python module imported and called in-process, with a reference helper
   module in the same interpreter" is new to the admitted sample — **provided it is worded as module import,
   not as "executes agent code in-process"**.

3. **wave-1 remediation carry (SCORECARD 1783-1788):** V1 "pin `gpg.program`/`log.showSignature`" ✓;
   V2 "hide the builder copy from builds" ✓; V3 "a read-only lane hide" ✓; V1b "refuse a fixture repo whose
   toplevel or `core.worktree` leaves d" ✓. All four are present, each with a stated red hostile control.

## Defects

### D1 — mutant-list numerator is unbound: "20 rc-witnessed survivors" vs 11 witnessed / 9 directional
The plan says the calibration mutant list is "the rc-witnessed plans/round_close.py survivors
(R41PlanNext §2.4; 20 survivors of 70 re-measured at round 42)". `R42PlanNext/res_round_close.json`:
`"survived": 20, "killed": 50` of `population 70` (line 5-8). But `wit_rc.txt` (same raw directory) lists
the 20 survivor rows and shows **9 UNWITNESSED**: lines 12, 13, 15, 17, 19, 22, 23, 24, 25 (L121 ×2,
L144 if→False, L148, L177, L199, L200, L209, L291). Only 11 rows carry an attribution cell, and two of
those are message-only rc `2→2` (L164, L181 — not directional). So at most **9** survivors have a declared
rc direction; the plan's "20 rc-witnessed survivors" would freeze 9 mutants with no direction, failing Q29
(direction declared and witnessed) and Q33 (re-derived direction). Two of the 11 attributed are rc-equivalent
and must not enter an rc-direction list (R41PlanNext §2.4 already said exactly this).
**Fix:** freeze only the witnessed directional subset (9) or add witness fixtures for the remaining 9 before
the freeze; name the mutant ids in the plan; keep L164/L181 out of rc directions.

### D2 — Q33 carried-cell red control is not specified for the u=18 branch
The alternative list "u = 18 advertised anchor/order behaviours with no frozen mutant (R42CritEquiv §3)" is a
real gap (verified: R42CritEquiv §3, u=18 = 9 anchor + 9 order). But the plan's red-control list
("no battery43; emptied list; the four hostile modules; span-forced and site-forced attribution copies") has
no **carried-cell restoration control**: Q33 requires a control that restores a carried direction cell and
reddens the predicate. Without it, re-deriving directions for 18 fresh (previously unfrozen) behaviours is
unpriced and the predicate is not shown non-vacuous for that branch.
**Fix:** add per-mutant restore controls (one hostile module that replays the carried cell and must turn the
predicate red) to the freeze control list.

### D3 — the dishonest-green vectors of R42CritC1Counter (XO1/XO3/X13 substitutes; V2b symlink escape) are absent from the round-43 counter plan
The planned re-freeze lists hostile controls for V1/V2/V3/V1b only. R42CritC1Counter demonstrated
`PREDICATE C1 pass` reached with **substitute fixtures**: `b-xo1-receipt-is-directory`, `b-xo3-emptied-directory`,
`b-x13-staged-manifest` (report §1 table) — all admitted by the frozen kill rule — plus `V2b` (a symlinked
row source resolving outside `d` reads the host, path_ok unenforced) and `V5` (token scan evadable, only
module source scanned). None of these three fixable contract checks appears in the plan: (a) symlink escape
refusal, (b) `.git/config` redirect/exec-key refusal, (c) `--claims`/`--receipt` path must be a blob at HEAD
(R42CritC1Counter §4 ranked list). If round-43 re-freezes without them, the same dishonest battery can green
the new counter again.
**Fix:** carry the three post-build contract checks (a)/(b)/(c) as part of the re-freeze, with red hostile
modules for XO1/XO3/X13 shapes and the symlink row source.

### D4 — coverage class sentence is asserted from a non-frozen host probe; prior-art hits exist for this exact task
The planned coverage bullet states "a grader that imports agent code in-process, a class the eight admitted
TB2 graders do not cover" on the strength of `feal_run1.txt` alone. The probe's own header says: "Host
python/gcc stand in for the image. Not a frozen probe." It ran host glibc (clock-seed cheat), not
`alexgshaw/feal-differential-cryptanalysis:20251031`; it is not byte-frozen as a probe receipt. Likewise the
prior-art files show live adjacency: `gh_issue_counts.txt` = `terminal-bench-2-1 | feal-differential-cryptanalysis | 1`
and `feal attack | 1`; `issues_detail.txt` lists PR #7 (2026-05-26) "Suppress pytest traceback in task
verifiers to prevent test-source leak" for this task, and third-party repos (`elizaOS/eliza`,
`minghinmatthewlam/openbench`, `gkroiz/agent-interp-envs`) already use `feal_in_c.get_keys()` scoring —
so "unpublished"/novel wording must stay gated on a dated prior-art receipt (the plan does say a seat must
check; the class sentence itself is still written into the plan unqualified).
**Fix:** re-run the controls in the pinned image, freeze dry-table predictions before the first recorded run
(round-35…42 convention), pin the probe + receipt digests, and tie the "new class" sentence to a dated
prior-art receipt; word the class as *Python-module import and in-process call* (regex-log already executes an
agent-authored regex in-process, so "executes agent code in-process" would overclaim).

### D5 — `cheat-clock-seed` is glibc/platform-dependent; the "5/5" is a host result
The clock-seed cheat reconstructs keys from `libc.srand(time())`/`libc.rand()` — a host-specific RNG
sequence. It passed 5/5 on this host; in the task image (different glibc/py3.13) the same cheat may not
reproduce, which would silently change the control battery's pass set.
**Fix:** make the primary cheat independent of the RNG (rely on `get_keys` import only — this is the robust
one), keep clock-seed as a secondary, host-flagged control, and re-derive both before freeze.

## Class-novelty assessment (asked)
Yes — *with the precise wording*: none of the eight admitted TB2 graders imports an agent-authored Python
module into the grader process (source-verified for the captured test_outputs.py of all eight via the
knowledge entries and the feal grader fetch). The claim must be pinned to "module import + in-process call +
reference helper module in the same interpreter" and to `test_outputs.py`'s `import attack` / `attack.attack(...)`
lines; as phrased in the scorecard ("imports agent code in-process") it risks being read as covering regex-log,
which executes agent-authored regex in-process.

## Do-nothing control reachability (asked)
- Calibration: do-nothing = no battery43 → planned red (`killed=0`) ✓; emptied list → red ✓.
- Coverage: do-nothing = nop → observed FAIL (`ModuleNotFoundError: No module named 'attack'`) ✓, so a
  do-nothing cannot reach the pass predicate; the cheats reaching PASS are the intended red controls. No
  vacuity found there.

## Evidence citations (≤25 words each)
- `test_outputs.py` (pin `2fd12b88`): "stolen = attack.attack(feal_in_c.encrypt)" and "assert feal_in_c.get_keys()[5] == stolen".
- `R42PlanNext/res_round_close.json`: `"survived": 20, "killed": 50` (population 70).
- `R42PlanNext/wit_rc.txt:12-25`: nine `UNWITNESSED` rows among the 20 survivors.
- `R42PlanNext/feal/feal_run1.txt`: `CASE nop rep=1 RESULT FAIL … ModuleNotFoundError: No module named 'attack'`; `CASE cheat-import-get_keys rep=1 RESULT PASS`; `CASE cheat-clock-seed rep=5 RESULT PASS`.
- `R42PlanNext/feal/feal_probe.py:4`: "Host python/gcc stand in for the image. Not a frozen probe."
- `R42CritC1Counter.md` §1: three substitute fixtures reach `PREDICATE C1 pass`; §4 fixes (a)/(b)/(c).
- `R42SentinelCounter.md` V1–V3 remediations match the plan's V1/V2/V3 wording.
- `R42PlanNext/prior-art/gh_issue_counts.txt`: `terminal-bench-2-1 | feal-differential-cryptanalysis | 1`.
- `corpus/knowledge/tb2-regex-log-grader.md:11-12`: "it is a regex pattern file … compiles and runs".

VERDICT: plan43-defects-5
