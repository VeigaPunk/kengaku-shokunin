# F42RevLesson — review of `corpus/lessons/round-42.md` (kengaku round 42, wave 2 falsify)

Seat: reviewer (leaf). Lane `kengaku-shokunin`; docs tip reviewed = `508434ad55c709337065611691c426f05875492d`.
Scratch `/fast/scratch/hyaku/kengaku-r42/F42RevLesson` (removed at exit). Nothing in the lane written; receipts under
`receipts/` in this dir. Tooling: installed nothing.

## Method

- Lesson identity: `git -C $S/lane diff 508434a..445e81f -- corpus/lessons/round-42.md` → empty, so the working-copy
  lesson (151 lines) is byte-identical to the docs tip; the commit stat's "150 +" is the no-trailing-newline artifact.
- Every evidence pointer resolved against a no-local clone at `508434a` (`$S/lane`); wave-1 build reports (landed at
  `445e81f`, after the docs tip) read at the working lane. No language server answers `.md` receipt review — all checks
  are text/receipt resolution.
- One re-run: `plans/scratch_guard.py --selftest` under the Q32 envelope
  (`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
  --unshare-pid --die-with-parent`), `date +%T` 18:13:24/18:13:24, `ls -A ~/.local/bin | sha256sum` `8cf5b1516051e191`
  before and after, unchanged — receipt `receipts/scratch-guard-selftest.txt`.

## What resolves (verified, not defects)

**Mistakes row 1 (direction copied from a table).** Class present. Evidence resolves exactly: `xmut_driver.py:113`
`("XO5", "order", "-", "rc-silence",` and `:121` (XO6); witness prose `:116-117`/`:125-126` "reference ORDER ok rc=0,
mutant ORDER HIT rc=1" (8 words); summary table `F40XMutLedgerOrder.md:70-71` carries `rc-silence … SURVIVED` for XO5/XO6
while §2 `:120-125` measures "the reference scans `commits=1` and PASSes; the mutant … FAIL rc=1"; the round-41 scout
re-print is at `R41PlanNext/near40_survivors_only.txt:40-41` (XO5/XO6 `rc-silence SURVIVED`) with the id list at
`R41PlanNext.md:59`. Captured-by present (`plans/round-42-claims.md:105-109` §Frontier: "Captured-by: Q29"). Fix shown
able to fail: `claims/control-c1-direction-mislabel.txt:29-30` (`MUTANT XO5 order rc-silence SURVIVED
exhibits=0>1,rc-mirror`, XO6 same), `:33` `MUTANTS total=14 killed=12 survived=2`, `:37` `PREDICATE C1 fail`, `exit=1`;
counter declares `rc-mirror` at `round42_c1_verify.py:201,206`, definition `:44`; witness `witness-run.txt:29-30`
(`XO5 … attributed=L117`, `XO6 … attributed=L53`).

**Mistakes row 2 (kill credited to a fixture).** Class present. Evidence resolves: `plans/battery40/a_bind.py` (lines
83–105) `build_a17` does `lane = ctx.clone(d / "lane")`; `R42CritEquiv/probe_a17.txt` reproduces the quoted numbers
exactly (`REF rc=0 defects=0`; `X2 rc=1 defects=3 [('S036',…),('S114',…),('S124',…)]`; `X4/X5` one `S110` each; `X11` two
lane rows) and `probe_none.txt` shows all four killable from nothing. Captured-by present (round-41 closure R1;
`R42CritEquiv` §4). Fix shown able to fail: leg f docstring `round42_c1_verify.py:19-30`;
`claims/control-c1-attribution.txt` → `MUTANTS total=14 killed=0 … unattributed=14`, `PREDICATE C1 fail`.

**Named limits (3).** `probe_lbl.txt` matches the quoted class sets verbatim; XO6 `indirect` (`order_check.py:52-53`,
`pkg_gate.py:301` prints only `ok`/`DEFECT`; `R42CritEquiv` §2.3 and §3 row k); witness-as-battery
(`claims/control-c1-witness-as-battery.txt:33,37` → `killed=14`, `PREDICATE C1 pass`). The `--work` note resolves:
`control-c2-nothing.txt` prints `gate: P10 DEFECT receipt unreadable` and `V9 DEFECT receipt, entry, … absent` instead of
crashing.

**Gate.** ≥1 admit (S125/S126/S127, each with a flip) and ≥1 reject (README, Dockerfile — each with reason + flip), plus
two "captured, not rows" rows with flips: structure satisfied. All ten capture digests match my own
`sha256sum` of `corpus/evidence/round42/tb2-circuit-fibsqrt/*` and the capture's `SHA256SUMS` (README `201f7c88…4cbd`,
Dockerfile `780c2398…d3d4`, test.sh `4770437e…c334`, task.toml `9f5aa1f7…0972`, SHA256SUMS `36b15d5b…2edf`, solve.sh
`a4ffab41…5d0b`, gates.txt `032786f9…ad29`, test_outputs `6117b8ed…0438`, instruction `a7f50026…b9ea`, sim.c
`700645ac…6173`). Quotes resolve at the cited lines: `test_outputs.py:23` "assert line_count < 32000" (4 words);
`instruction.md:8` "the first 32 lines are defined by the binary representation of stdin" (12 words); `sim.c:335`
"for (int step = 0; step < 32000; step++)" (9 words); `README.md:10` (15 words); `Dockerfile:3` "WORKDIR /app" (2 words).
Secondary lines: test_outputs `:65-67` (gcc) and `:119` (`/app/sim`), sim.c `:319` (`parse_gates("gates.txt")`) and
`:340` (`if (num_signals >= 32)`), skip at `:112-114`, test.sh `:13` (`if [ "$PWD" = "/" ]`) and `:18-22` (uvx),
task.toml `:22`/`:25` (`timeout_sec = 3600.0`). `plans/pkg-spec-r42.json` pins exactly S125/S126/S127 with those digests
and `raw_base` = the `circuit-fibsqrt/` tree at the pin. Gate prose receipts: `R42PkgRows/refetch.txt` = access
17:24:14 -0300, three `GET 200`, three `cmp=IDENTICAL`; `R42PkgRows.md:93-98` three `E11` lines (S125/S126/S127 missing
used-by), `:87` `CENSUS_EXIT=0 … E=0 W=15`, `:113` `rows=120 tokens=27 defects=0`.

**Routed R1.** Leg f + five repairs at `round42_c1_verify.py:19-30`; fixed system PATH pinned at `:108`
(`PATH = "/usr/local/sbin:…"`); red controls `control-c1-attribution.txt` and `control-c1-hostile-escape.txt`
(`SETUP fixture 'h-esc42-relative-escape' of battery42/h_esc42.py breaks the contract`, `exit=2`); `battery42` carries no
`gpg.program`/`log.showSignature` (`grep -rn` → rc=1); `R42SentinelCounter.md:53` "### V1 — HIGH — a fixture's
`.git/config` runs a program inside the order tool's run" with `gpg.program` reached through `log.showSignature`;
`.ufo/waves/round-41/falsify/F41C1Hardened.md` exists.

**Routed R2.** Sentinel `/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL` exists (71 B, mtime Oct 26 16:56);
`build-dispatch.json` `taskCall.context` carries the "Scratch rule" paragraph exactly once (grep -c = 1);
`plans/scratch_guard.py` landed (ff14d76, 622 lines) and my re-run prints `SELFTEST ok=36/36`, rc=0; envelope census over
`.ufo/waves/round-42/claims/*.txt` = exactly 9 of 13 with `ENVELOPE` (the seven C1 controls, `witness-run.txt`,
`control-c2-nothing.txt`) and `control-c2-filler.txt` with none — matches the lesson word for word.

**Routed R3.** V9 is the ninth check (pointer off by one, D5 below); `grep -n 'closed\|merged'
plans/round42_c2_verify.py plans/pkg_gate.py` → no output, rc=1; `claims/control-c2-filler.txt` carries both halves:
`CONTROL filler V9 DEFECT case_rows=0/16 bad=["no '## Case table' section", …]` and `CONTROL content V9 ok
case_rows=16/16 bad=0`, `CONTROL-C2-FILLER red-as-required` — and no envelope/timestamp line.

**Routed R5.** `integrate/r5-round-close-check.txt`: `CHECK run1_rc=0 run2_rc=0`, identical `SELFTEST checks=5 ok=5
failed=0` tails, `CHECK PASS rc=0 twice, identical output, no nested copy`; the patch landed in `ff14d76`
(`plans/round_close.py | 9 +`); no `frozen-digests.txt` pins `round_close.py` (grep → only `fc58bf3f … plans/fibsqrt_probe.py`);
red-before receipts exist in `R42R5Carried` (`red-run.txt`: `CHECK run1_rc=0 run2_rc=1 … RED_RC=1`); verdict name
`r5-round-close-rerun-fixed-draft` matches the report's terminal line.

**Census.** `claims/census-before.txt` and `integrate/census-final.txt`: exit 0 (`census_rc=0`), 15 `W04` lines each.
Registry 117 → 121 measured with `grep -cE` at `bc856d8`/`508434a` (see D6 for the command as printed).

**Falsifiers paragraph.** All eight named controls verified at the quoted key lines (`control-c1-nothing.txt:19,23`
killed=0/survived=14/C1 fail; `control-c1-no-mutants.txt:19` total=0; `control-c1-tool-edited.txt:3` PINS mismatched=1;
`control-c2-nothing.txt` checks=9 defects=6/C2 fail; filler as above). `R42CritEquiv.md`: §1 e=0, §2 i=0 + three limits,
§3 u=18 (9 anchor + 9 order, narrowest 11), §4 the four provenance corrections, probes present;
`R42CritPytest.md` exists; `integrate/measure-final.txt` exists (committed at `508434a`).

**L1-added row 1 (envelope).** `measure-baseline-v1.txt:40,151,230,377,513` `gate: P10 DEFECT fresh probe exit=2
stderr='error: Could not acquire lock…'`; `integrate/envelope.sh` v2 does `--bind "$SCR/home-cache"
/home/vgpnk/.cache`; fix shown able to fail by the v1 receipt itself.

**L1-added row 2 (attack-surface sentence).** `round42_c1_verify.py:30` is exactly "Both tools execute no fixture code
(git plumbing only, hooks and fsmonitor disabled), so repairs a-c close"; falsified by `R42SentinelCounter` V1 (above).

## Defects

**D1 (moderate) — R4's measured claim is false at the docs tip.** Lesson R4: "`git diff bc856d8..HEAD -- corpus/SOURCES.md`
→ empty (measured)". Measured at `508434a`: the diff is four added lines (`+| S125 …` through `+| S128 …`), receipt
`receipts/r4-sources-diff.txt` (sha256 `fe444b8b97a73f30c7d6192d2f678bfe1d50730b4eca51603a14d8d04f99c793`, 7666 B);
`git show --stat ff14d76` shows `corpus/SOURCES.md | 4 +`; and the lesson's own Census section records "registry
117 → 121". The substance ("nothing edited in place") survives — all four hunks are pure additions — but the stated
measurement is false as written; the honest phrasing is "the diff shows only additions, no in-place edits".

**D2 (moderate) — R5's "named carried again in the freeze (§Limits)" is not true for the F39 trio.** `plans/round-42-claims.md`
has no `§Limits` section at all (headers at `:1,23,65,96,102` only: C1, C2, Separability, Frontier step); its
"Limits named now" bullet (`:59-63`) names XL1–XL6, `state_check.py`/`round_close.py` survivors and the 34 unpriced rows
of `tip_receipts.py`/`sources_adopt.py` — and nothing else. `grep -nE
'LedgerTip|MutDirection|OrderGateMut|fail-open|s_usage' plans/round-42-claims.md` → no output (rc=1): the freeze never
names `F39LedgerTip` D1, `F39MutDirection`, `F39OrderGateMut` fail-open, nor `s_usage-03`, nor the tip_receipts residual
mutants. The lesson asserts these are "named carried again in the freeze … with no owner"; only the round_close
survivors are (loosely) covered by "`round_close.py` survivors".

**D3 (moderate) — L1 row 4's decisive number is unpersisted, and its role list doesn't match wave 2.** The quoted
generator output "33 {'executor': 5, 'reviewer': 10, 'critic': 9, …} attack=22/33 flash=14/33": the role mix matches
`falsify-spec.json` exactly (executor 5, reviewer 10, critic 9, mutation-tester 3, connector 3, scout 3 = 33;
`falsify-dispatch.json` `counts` = `{spawn: 33, resume: 0, total: 33}`), but `flash=14/33` and `attack=22/33` are
recorded nowhere under `.ufo/waves/round-42/` (`grep -rn 'flash=14/33'` and `'attack=22/33'` → nothing; neither
`falsify-spec.json` nor `falsify-dispatch.json` has any model/flash field), so the pointer "make_falsify_spec.py output"
cites unpersisted stdout — the mistake's basis and the fix's "shown able to fail by this spec: 28 < 33" rest on a number
no stored receipt carries. Also the row's role list "(executor/scribe/critic/sentinel)" names scribe, a role wave 2 does
not have (spec roles above).

**D4 (minor) — `fibsqrt-probe.txt:6` cited twice for content that lives at `:23-24`.** The Gate prose and the
falsified-sentences paragraph cite "(receipt `fibsqrt-probe.txt:6`; `cases=16 observed_pass=7 observed_fail=9
mismatches=0`, `regrade cases=16 differ=0`)". Line 6 of the receipt is `# capture test_outputs.py sha256=…`; the summary
lines are `:23` (`regrade cases=16 differ=0`) and `:24` (`cases=16 observed_pass=7 observed_fail=9 mismatches=0`). Content
verified present; the pointer is wrong (if `:6` was meant to anchor the lookup-28 case, that is `:11`).

**D5 (minor) — `round42_c2_verify.py:327` off by one.** R3 cites ":327" for "V9 is the ninth check"; the checks-list
entry `("V9", lambda: v9(lane))]` is line `:326`; `:327` is `defects = 0`.

**D6 (minor) — the census command as printed does not produce the quoted numbers.** The lesson cites
`grep -c '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 117/121. Run as printed (BRE, no `-E`),
`\|` is alternation and the `^ {0,3}` branch matches every line, so it yields 171/175 — exactly `wc -l` at `bc856d8`/`508434a`.
With `-E` it yields 117/121. The numbers are right; the command as cited is not what produces them.

**D7 (minor) — `Dockerfile:9-10` is one line off.** The README-reject row says "`Dockerfile:9-10` copies only
`tests/sim.c` and `gates.txt`"; the two COPY lines are `:10` (`COPY tests/sim.c /app`) and `:11` (`COPY gates.txt /app`);
`:9` is the comment "# Copying tests/sim.c is allowed for the agent to check its work".

**D8 (low) — L1 row 3's fix has no failure receipt.** Every other Mistakes row names a persisted receipt that shows its
fix failing; row 3's only failure record is "the edit tool's syntax warning" — ephemeral, not stored. `frozen-digests.txt`
`fc58bf3f…` (verified: `sha256sum plans/fibsqrt_probe.py` = `fc58bf3f1780aaefee9df1e635b01765d3fb5d9224f1958494df4e1b8ed061b3`)
proves the frozen probe is the corrected file, but it is not a demonstration that "re-read before every anchored edit"
can fail.

## Observations (not counted as defects)

- "(v2: all green as at round 41)" is loose: `measure-baseline.txt` contains 12 `DEFECT` strings (gate P3/P4/P6/P7/P8,
  V2/V3/V4/V7/V9) — the baseline's absence reds, the same state as round 41. What v2 restores is the envelope-sensitive
  P10/uv leg (no `P10 DEFECT` line anywhere in v2). Defensible in context, falsifiable if read literally.
- L1 rows 1/2/4 have `captured-by` cells reading "none — …" (a capture-gap explanation rather than a captor); consistent
  with main row 1's "None at the time: …" convention, so not counted.
- sim.c ":113-115" — the skip is the `sscanf(...) != 2` → `continue` at `:112-114`; close enough to resolve.
- The Gate cites `refetch.txt` for both re-fetch times (17:20:09 and 17:24:14); `refetch.txt` carries the 17:24:14 fetch;
  the earlier fetch is quoted inside `R42PkgRows.md` itself.

## Residual risk / verification gaps

- The m_flash count (14) cannot be confirmed or refuted from the repo — no persisted routing data exists for wave 2
  (see D3); I did not re-run the generator (it writes spec files).
- I did not re-run the C1 counter/battery, the C2 counter, or the fibsqrt probe (landing measurement is the L1's; the
  lesson itself scopes those to wave 1 receipts and the landing run). My one re-run is the scratch_guard selftest.
- Conditional flip statements in the Gate ("digest leaves the pin") are unexercised by design.
- `R41PlanNext.md` and `near40_survivors_only.txt` verified only at the cited lines (`:59`, `:40-41`).

## Summary

The lesson's two Mistakes rows and three named limits are fully evidenced and every fix but one names a persisted
failing receipt; the Gate has the required admits/rejects with reasons and flips, and all ten capture digests, five
quotes and the spec pin verify byte-exactly. The defects are concentrated in the Routed section's two overstated
dispositions (R4's "empty" diff, R5's freeze-naming claim) and in citation hygiene (one unpersisted number, three
off-by-one/wrong-line pointers, one mis-cited command, one fix without a failure receipt).

VERDICT: lesson-defects-8
