# F41RevQuality — review of QUALITY Q31 and Q32 (kengaku round 41, wave 2 falsify)

Date: 2026-10-26. Seat: F41RevQuality (reviewer, leaf). Target: `corpus/QUALITY.md:573-624` (Q31) and
`:626-675` (Q32) at the lane tip.

Scope note: the lane advanced one commit past the tip named in the dispatch — HEAD is `d7c7789`
(round-41 wave-2 dispatch), parent `3d0058f` (the stated tip). `git diff --stat 3d0058f HEAD --
corpus/QUALITY.md` is empty, so every citation below was checked at `d7c7789` and reads identically at
`3d0058f`. All commands ran in the shared clone `/fast/scratch/hyaku/kengaku-r41/F41RevQuality/lane`
(`git rev-parse --show-toplevel` asserted); counter runs used the mandated envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000
--proc /proc --unshare-pid --die-with-parent` with `TMPDIR` pointed at the seat scratch. Receipts:
`.ufo/waves/round-41/falsify/F41RevQuality/{green-run.txt,vacuous-run.txt,q32-checks.txt}`.

## What holds (every claim re-verified at the tip)

Citations, all exact:

- Counter digest: `sha256sum plans/round41_c1_verify.py` →
  `8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8` = `frozen-digests.txt:2`. The frozen
  counter is byte-identical at the tip.
- Q31 counter cites: `:123-124` `TOTAL = 23` / `FLOORS = {"receipts": 13, "sources": 10}`;
  `:640-641` `TOTAL >= 1 and all(FLOORS.get(t, 0) >= 1 …) and sum(FLOORS.values()) == TOTAL` plus the
  per-tool `[counted, killed] == [floor, floor]` leg; `:642` `good = (… and len(MUTANTS) == TOTAL and
  floors_ok and …)`; `:631` the `MUTANTS-BY-TOOL …` print; `:589` `src.count(old) != 1`;
  `:547` `SETUP duplicate fixture id`; `:13-17` the Non-vacuity paragraph (grep -n pinned each).
- Patch: `claims/control-c1-no-mutants.patch` is exactly hunk `233a234` + one line `MUTANTS = []  #
  CONTROL: …`; the list literal closes at line 233 (`]`, grep-pinned), so the hunk number is exact.
- Control receipts at cited lines: `control-c1-no-mutants.txt:24,25,26,29,30` (`BATTERY fixtures=22 …`,
  `MUTANTS total=0 …`, `MUTANTS-BY-TOOL receipts=0/0 sources=0/0`, `PREDICATE C1 fail`, `exit=1`);
  `control-c1-nothing.txt` (`BATTERY fixtures=0`, `MUTANTS total=23 killed=0 survived=23`,
  `PREDICATE C1 fail`, `exit=1`); `control-c1-tool-edited.txt:1` (`PINS total=2 mismatched=1
  first=plans/tip_receipts.py`), 13 receipts mutants `invalid` (`:24-36`), `PREDICATE C1 fail` (`:52`);
  `control-c1-hostile.txt:32` `PREDICATE C1 n/a (non-default battery or mutant subset)`.
- Freeze ordering: `git show --stat 8ef8b4fc` lists all four cited control receipts + patch +
  `h_host_writes.py`; `git ls-tree 8ef8b4fc -- plans/battery41` is empty (battery absent at the freeze);
  `8ef8b4fc` is an ancestor of HEAD.
- Round-40 falsifier cites: `F40CritPlanNext.md:30-33` (`MUTANTS total=0 …` → `PREDICATE C1 pass`,
  `exit=0`), `:105-115` (D1, `<n>` unbound), `runA-vacuous.txt:24,26`; `plans/round-41-claims.md:50`
  carries the quoted sentence verbatim.
- Q32 counter cites: `:56-70` (isolation docstring: child builds in `bwrap --ro-bind / /` with the lane
  hidden `--tmpfs <lane>`, `--unshare-pid --unshare-net`, `HOME=/nonexistent`, fixed system PATH),
  `:116` (`PATH = "/usr/local/sbin:…"`), `:318-325` (`ro_sandbox` argv). `claims/hostile/h_host_writes.py:1-2`
  quote verbatim; `control-c1-hostile.txt:2,3,27,34` exact.
- `corpus/lessons/round-40-verifier-spotcheck.md:95-96` = the R2 host-safety row.
- `build/R40CritC1Counter/crit_git_shim.py:10-12` (import-time `SystemExit`), `:18`
  (`SHIM_DIR = pathlib.Path("/nonexistent/neutralized-shim-dir")`); `crit_ledger_selfread.py:9-11`
  (`SystemExit`). Re-import of both modules from the committed build dir exits 1 with the NEUTRALIZED
  message (`q32-checks.txt`).
- Cross-refs: Q27's fourth limit is "a kill records a result difference, not a reason"
  (`corpus/QUALITY.md:439-441`), which Q31's tool-cell limit extends; Q24's ordering leg ("before the
  round's first data receipt is committed") exists at `:308-311`.

Executable checks, both run as written:

- Q31 green half: `python3 plans/round41_c1_verify.py --lane .` (no `--work`, TMPDIR at scratch, inside
  the envelope) printed `PINS total=2 mismatched=0`, `BATTERY fixtures=48 wrong=0 tampered=0
  sidechannel=0`, `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`,
  `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`,
  exit 0 — in 5.4 s, matching `integrate/measure-final.txt` line for line (`green-run.txt`). The named
  lines appear in the claimed order; FIXTURE/MUTANT detail lines interleave between them, which the
  Check's "then" wording tolerates.
- Q31 red half: the frozen counter copied with the committed patch's one line inserted after line 233
  printed `MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0`,
  `MUTANTS-BY-TOOL receipts=0/0 sources=0/0`, `PREDICATE C1 fail`, exit 1, with `TOTAL`/`FLOORS`
  untouched — the red is the binding, not a second edit (`vacuous-run.txt`).
- Q32 red halves: `grep -n 'markers after the run' .ufo/waves/round-41/claims/control-c1-hostile.txt`
  → line 34 with `No such file or directory`; `ls -l /home/vgpnk/.local/bin/git` → `No such file or
  directory`, exit 2 (`q32-checks.txt`).

## Defects

### D1 (Q31, major — stale lesson pointer): the round has now written the lesson, and the pointer never moved

`corpus/lessons/round-41.md` exists at the tip (committed in `0d57419`, "round-41: lesson, SCORECARD
round-41 section and Planned (round 42), LOG entry …"). Q31's Lesson line still reads: "`corpus/lessons/
round-41.md` does not exist at this draft (2026-10-26: `ls corpus/lessons/round-41.md` → `No such file
or directory`), so the lesson pointer moves there when the round writes it." Both halves of that sentence
are now false at the tip: the file exists, and the promised move did not happen — the lesson carries the
matching row (line 15, "Frozen predicate satisfiable with zero round-41 work", citing
`plans/round41_c1_verify.py:123-124` and `floors_ok` at `:640`), which is exactly where a reader sent by
Q31 should land. Smallest correction: replace the non-existence sentence with the pointer, e.g.
"`corpus/lessons/round-41.md` mistakes-table row 'Frozen predicate satisfiable with zero round-41 work'."

### D2 (Q32, minor — line drift): "bought nothing" sits on line 74, not 73

Q32 cites the ambient-write quote to `corpus/lessons/round-40.md:73`. `grep -n -F 'bought nothing'`
pins it at line 74 (line 73 ends "…so the ambient form"; line 74 opens "bought nothing. Fix applied:
…"). Smallest correction: `:73` → `:74`. I re-pinned every other quote in that paragraph with
`grep -n -F` and they are exact: the SHIM_DIR quote starts on line 67 (`:67` correct — the sentence runs
67→68), "the seat's receipts do not timestamp the writes" is on 69 (`:69` correct, same line carries
`~14:05`), `~14:07` on 70 with the absence check on 71 (`:69-71` correct).

### D3 (Q32, major — the Check's forward leg is red on the round's own cited receipts, and the round does not name that result)

The Check says the forward leg is "a per-receipt sweep — every report a round's claim cites as having run
a counter, battery or fixture build contains its `bwrap … --ro-bind` line and a timestamp line for each
host write it made, and the round names the sweep's result in its report." Executed at the tip:

- 7/7 receipts the round cites carry zero `bwrap` lines and zero timestamp lines
  (`q32-checks.txt`): `claims/witness-run.txt` (cited `plans/round-41-claims.md:43`),
  `claims/control-c1-nothing.txt` (`:57`), `claims/control-c1-no-mutants.txt` (`:60`),
  `claims/control-c1-tool-edited.txt` (`:64`), `claims/control-c1-hostile.txt` (`:65`),
  `integrate/measure-final.txt` and `integrate/measure-baseline.txt` (cited by the LOG round-41 entry:
  "every no-harm instrument at the landing tip as at the baseline (`integrate/measure-final.txt`)").
  `measure-final.txt` even records the counter invocation itself without a wrapper
  (`$ python3 plans/round41_c1_verify.py --lane . --work …`).
- The round names no per-receipt sweep result. The closest text is the lesson's R2 row
  (`corpus/lessons/round-41.md:64-65`): "Every wave-1 item carries the `bwrap --dev-bind / / --ro-bind
  /home/vgpnk/.local/bin …` envelope; wave-1 reports declare no PATH or `$HOME` write" — a
  declaration-based spot-check of three named reports (`R41BatRcvCtl.md`, `R41BatSrcExit.md`,
  `R41BatRcvRun.md`), which is a different and weaker claim than the sweep Q32 specifies, and it does
  not disclose that the claim-cited receipts carry no envelope.

So Q32's own executable Check cannot complete green at the tip by its own text. Fairness nuance for the
L1: the control receipts were committed at the freeze (`8ef8b4fc`), one commit before the criterion
landed (`74513c0`), so the receipts predate the rule they are now measured against; the criterion's
normative sentence and forward leg nonetheless bind "a round's claim cites", which covers them. The
underlying protection is real — the counter sandboxes its children (verified by reading `:56-70`,
`:318-325` and by my green run executing under the mandated envelope), and the round-40 modules stay
neutralized. Smallest correction (L1's choice): either name the sweep's actual result where the round
reports (e.g. in the lesson R2 row or Q32's Check: "receipts committed at the freeze predate the
envelope rule and carry no bwrap/timestamp lines; the sweep binds reports from the rule's landing
forward"), or re-issue future claim-cited run receipts with envelope + timestamp headers.

## Notes (checked, not defects)

- Q32's "Measured absence at the criterion's creation" greps (`→ 0`) are time-anchored and correct as
  history; at the tip both return nonzero purely from Q32's own landed text — `host-safety` hits at
  `QUALITY.md:629,648` (grep -c → 2), `bwrap` at `:640,648,649,655` (grep -c → 3). A tip re-run needs
  the creation-time qualifier the sentence already carries.
- Q31's "`ls plans/battery41` → `No such file or directory`" is anchored to the freeze ("committed with
  the freeze (8ef8b4fc), before plans/battery41 existed") and is correct in that context; the directory
  exists at the tip.
- Q31's limit "a development run cannot be filed as either" is confirmed by `control-c1-hostile.txt:32`
  (`PREDICATE C1 n/a (non-default battery or mutant subset)`, `exit=1`).

## Residual risk and verification gaps

- I took the round-40 falsifier's committed receipt (`runA-vacuous.txt`) at its cited lines rather than
  re-deriving that round's full run A.
- The D3 sweep covered the seven receipts the round-41 claim and LOG entry name; a run report cited
  elsewhere (e.g. the registry addendum) was not swept.
- C2 (V1-V8, probe, prose surfaces) and the battery modules' internals are out of my scope — other seats.

## Receipts

- `.ufo/waves/round-41/falsify/F41RevQuality/green-run.txt` — frozen counter at tip, envelope, exit 0.
- `.ufo/waves/round-41/falsify/F41RevQuality/vacuous-run.txt` — emptied-list copy, exit 1.
- `.ufo/waves/round-41/falsify/F41RevQuality/q32-checks.txt` — Q32 red halves, per-receipt sweep,
  neutralized-module re-imports.

Scratch `/fast/scratch/hyaku/kengaku-r41/F41RevQuality` deleted after receipts were copied out. No
writes outside this report dir and the scratch dir; no lane file edited.

VERDICT: quality-defects-3
