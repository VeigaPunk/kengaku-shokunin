# F42RevQuality — review of QUALITY.md Q33 and Q34 (kengaku round 42, wave 2 FALSIFY)

Scope: the two criteria appended this round to `corpus/QUALITY.md` (Q33 at `:692-715`, Q34 at `:717-822`), landed
byte-identical to the wave-1 draft (`build/R42QualityDraft.md` §1/§2; both blocks verified byte-equal by extraction
and substring compare). Attacked on three axes: **checkable** (can the Check lines run as written?), **evidence**
(do the citations resolve to real, matching artefacts?), **failable** (do the seat scripts fail on a mutated copy?).
Working tree: clone of the lane at `508434ad` (docs tip when this wave was cut) in my scratch, plus a second clone at
the current tip `3e8a2e5`; every run inside the Q32 envelope (§5). All git calls read-only `-C` my scratch clones;
no lane file touched.

## 1. Findings by severity

### D1 — HIGH, both criteria: the executable checks point at tools that were never landed in any commit
Q33 check (a) says `python3 plans/carried_direction_diff.py --lane .` "to land as `plans/carried_direction_diff.py`
for this line to run as written"; Q34's Check says `python3 plans/sources_appendonly.py --lane .` and "must land as
`plans/sources_appendonly.py`". Neither file exists at the docs tip `508434ad`, at the current tip `3e8a2e5`, or in
any commit: `git log --oneline --all -- plans/sources_appendonly.py plans/carried_direction_diff.py` → empty;
`ls-tree 508434ad -- plans/` has no match; `python3 plans/sources_appendonly.py --lane .` on the pinned clone →
`No such file or directory`. Wave-1 integration note 2 gave the L1 an either/or — land the tools byte-identically,
**or** edit the criteria to say "draft tool at build/R42QualityDraft/"; the landed text is byte-identical to the
draft (neither leg done), so both criteria's only executable legs are dead as written. Aggravating: even the
fallback paths do not resolve at the pinned commit — `.ufo/waves/round-42/build/R42QualityDraft/` is tracked only
from `445e81f` (wave-1 reports), one commit **after** the docs tip the criteria landed in; at `508434ad` the clone's
`build/` contains only `swarm-registry.json`.

### D2 — HIGH, both criteria: the Check command lines do not match the tools' CLIs
Both draft tools take the lane **positionally** (`LANE = sys.argv[1]` in `carried_vs_rederived.py:5`;
`sys.argv[1] if len(sys.argv) > 1 else "."` in `sources_appendonly.py:14`). The Check lines write `--lane .`.
Demonstrated on the pinned clone: `python3 carried_vs_rederived.py --lane .` →
`FileNotFoundError: [Errno 2] No such file or directory: '--lane/.ufo/waves/round-40/falsify/F40XMutAnchor.md'`;
`python3 sources_appendonly.py --lane .` → `SETUP git log failed: fatal: cannot change to '--lane'` (exit 2). So even
a byte-identical landing at `plans/` (D1's fix) would leave both Checks failing as written. Q34's *measured*
sentences use the positional form (`python3 …/sources_appendonly.py <lane>`) — only the Check sentence is wrong.

### D3 — MEDIUM, Q33: the red half's cited `PREDICATE C1 fail` line is not reachable under the check's own instruction
Check (b) says "run it in **development mode** with the witness fixtures" and cites `PREDICATE C1 fail` (`:37`) and
`exit=1` (`:38`) from `claims/control-c1-direction-mislabel.txt`. But development mode (`--battery-dir` or `--only`
set; counter `plans/round42_c1_verify.py:525` `dev = a.battery_dir is not None or a.only is not None`) prints
`PREDICATE C1 n/a (non-default battery or mutant subset)` (`:657`). My faithful re-run with the witness-run.txt-
recorded command (`--battery-dir .ufo/waves/round-42/claims/witness`, XO5/XO6 patched back to `rc-silence`) printed
exactly `MUTANTS total=14 killed=12 survived=2`, `MUTANTS-BY-TOOL anchor=9/9 order=3/5`, XO5/XO6
`rc-silence SURVIVED exhibits=0>1,rc-mirror`, exit 1 — but `PREDICATE C1 n/a`. The receipt's own line set
(`BATTERY fixtures=14` **and** `PREDICATE C1 fail`) is unreachable on the landed lane: default battery (no flag)
gives `fixtures=29` + judged predicate — my re-run printed `BATTERY fixtures=29`, `MUTANTS total=14 killed=12
survived=2`, `order=3/5`, `PREDICATE C1 fail`, exit 1; witness dev mode gives `fixtures=14` + `n/a`. The receipt's
pair came from the L1's pre-landing measurement copy (its envelope line records `cwd=/fast/scratch/hyaku/kengaku-r42/L1/m/dir`,
where `plans/battery42` still held the 14 witness fixtures). Substance fully reproduces; the instruction line and the
cited output set do not match each other.

### D4 — MEDIUM, Q34: the pipe-in-cell sentence is false as written, and its evidence is an invalid inference
The criterion claims a row carrying a literal `|` "would parse as an arity mismatch and is reported (`arity=<n>`,
exit 1) rather than silently misread — `arity=0` over 117 rows × 36 commits says no such row exists today".
Demonstrated false in the case that matters:
- **New row born with a pipe is fully silent.** Fixture `fx-pipe3` (base row S001; commit 2 adds S002 with source
  cell `src-b|x`; commit 3 edits S002's true `teaches` in place): `SOURCES-COMMITS scanned=3 rows_at_tip=2`,
  `SOURCES-APPENDONLY violations=0 arity=0`, **exit 0**. The shifted cells make the teaches edit land on the mutable
  `status` name — the exact silent misread the sentence denies. A first-appearance row never enters the
  length comparison (`rid not in prev → continue`), so no ARITY line is possible for it.
- **Pipe added to an existing row fires ARITY once, then goes blind.** Fixture `fx-pipe2`: `ARITY bacfbe9b S001
  cells 11->12`, exit 1 — but from that commit on the row is never cell-compared again, and my subsequent true-
  `teaches` edit on the piped row produced `violations=0` (misattributed to mutable `status`).
- **The inference is invalid even where the conclusion holds.** `arity=0` cannot establish "no such row exists
  today" — a row born with a pipe never produces an arity line. The conclusion is true: my independent scan
  `awk -F'|' '/^\| S[0-9]+/ && NF!=13'` over the tip registry → `count=0`. But the cited evidence does not support it;
  the honest support is the awk scan, which the criterion does not mention.

### D5 — LOW, Q34: wrong line pin for `registry_check.py`
The criterion cites `plans/registry_check.py` "(`parse_registry(text, …)`, `:20`)". Line 20 is
`def safe_path(value):`; `def parse_registry(text, source_ids):` is at `:25`, and the working-tree-only call is at
`:55` (`parse_registry((root / "corpus/SOURCES.md").read_text(), …)`). Substance verified (parses the working tree,
no git); the pin is wrong.

### D6 — LOW, Q34: "No lane tool reads it from committed history" is self-undermining as landed
The sentence is true at the tip (verified: no `plans/*.py` naming `corpus/SOURCES.md` calls
`rev-list`/`git.show`/`git log` — my crossed grep returns nothing) — but only because D1 left the instrument
unlanded. Had the L1 landed `sources_appendonly.py` as the criterion's own text promises, the sentence would be
falsified by the criterion's own instrument. It needs the same "at this criterion's creation" scoping the
neighbouring measured sentences carry.

## 2. What reproduced (calibration inventory — the criteria are honest everywhere else)

- **Q33 (a)** on the pinned clone with the draft tool (positional): 14 `CARRIED …` lines, `CARRIED-DIRECTIONS
  total=14 differ=2 ids=XO5,XO6`, exit 0 — matches the criterion's claimed output exactly.
- **Q33 (b) red half**, reproduced twice by my own patched-counter runs (witness dev mode and default battery):
  XO5/XO6 `rc-silence SURVIVED exhibits=0>1,rc-mirror`, `killed=12 survived=2`, `order=3/5`, exit 1. The patch
  applies cleanly (4 lines, XO5/XO6 only).
- **Q33 (c)** quotes and pins all exact: `witness-run.txt:29-30` (XO5/XO6 `rc-mirror killed … attributed=L117/L53`),
  `:33` (`killed=14 … unattributed=0`), `:34` (`anchor=9/9 order=5/5`); mislabel receipt `:29/:30/:33/:34/:37/:38`.
- **Q33's declared blind spot is real and honestly disclosed**: flipping the witness receipt's declared cells to the
  round-40 labels → `differ=0 ids=-`, exit 0 — exactly the "copied freeze looks clean" limit the criterion states.
- **Q33's other pins verified**: counter `:38-45` (docstring + four-name vocabulary), `:156/:161/:181` (X6/X7/X14
  class cells), `:201/:206` (XO5/XO6 `rc-mirror` rows), `F40XMutLedgerOrder.md:70-71` (`rc-silence` rows), `:122-124`
  and `:127-128` (witness prose), `F40XMutAnchor.md:71-72,79` (carried classes), `corpus/QUALITY.md:516-517`
  (Q29's UNWITNESSED sentence, wrapped across the two lines), `plans/round-42-claims.md:105-109` (mined mistake),
  `plans/mutant_direction_check.py:92` (`--counter plans/round38_c1_verify.py` default).
- **Q34 Check substance** on the pinned clone (draft tool, positional): `scanned=37 rows_at_tip=121` (creation-time
  numbers 36/117 were pinned to `fda71ae`, consistent), **15 CELL lines matching the criterion's red list
  cell-for-cell** (same ids/cells/commit sha8s: S081 scope, S082 anchor, S086 tier+scope, S092/S100/S100, S103/S104
  source+teaches, S105/S107, S046/S052, S124 anchor; all `repair_row=none`), `violations=15 arity=0`, exit 1; same at
  the current tip `3e8a2e5`. `supersede_later.py`: 15 × `supersede_same_or_later=NO`, exit 0.
- **Q34 failability beyond the wave-1 receipts** (my fixtures, all in scratch): green (supersede row added) →
  `violations=0`, exit 0; red (in-place anchor edit) → `CELL … S001 anchor repair_row=none`, `violations=1`, exit 1;
  **mutable-cell exemption** (status-only edit → no violation, exit 0) — not covered by the original receipts, now
  verified; **act-level same-commit repair** → `CELL … repair_row=same-commit`, `violations=1`, exit 1, exactly as the
  criterion's limit sentence says; **live-registry catch** — in-place edit of S125 on a mutated lane copy →
  `CELL a4ba8c90 S125 source repair_row=none`, `violations=16`, exit 1.
- **Landing is append-only**: S125-S128 added 4 rows (117→121), no new violations at `508434ad` or `3e8a2e5`
  (still 15); `grep -c 'supersedes S0[0-9][0-9]'` → 17 at `508434ad`, matching the criterion's pinned count.
- **Rule-text pins exact**: `SOURCES-CONTRACT-v1.md:49-51` and `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`
  (identical append-only text); `corpus/lessons/round-41-verifier-spotcheck.md` D2 at `:30-36`, R4 at `:116`.
- **Lesson promise fulfilled**: `corpus/lessons/round-42.md` §Mistakes carries the Q33 class ("A declared direction
  copied from a table instead of re-derived from the run") and records R4 as a wave rule with nothing edited in
  place this round.
- **Check (b)'s inputs exist in a clone**: `claims/control-c1-direction-mislabel.patch/.txt`, `claims/witness-run.txt`,
  `claims/witness/w_anchor.py`/`w_order.py` are tracked at `508434ad`.
- **Draft artefact hashes**: all six files in `build/R42QualityDraft/` match §7 of `R42QualityDraft.md`
  (`sources_appendonly.py` `f1b84d8a…`, `carried_vs_rederived.py` `47151f23…`, `supersede_later.py` `dbd20c1d…`,
  `receipt-lane.txt` `4db25114…`, `receipt-green.txt` `b5b48961…`, `receipt-red.txt` `0c82c5de…`).

## 3. Residual risk and verification gaps

- I ran no C2-side work (Q33/Q34 do not reach C2). The 15 historical SOURCES cells are named, not adjudicated —
  by the criterion's own design; I verified the tool's list equals the text's list, not the history behind each cell.
- My pipe fixtures use synthetic 11-cell rows; the defects in D4 are latent (the live registry has 0 pipe rows at
  the tip), but the criterion's sentence would mislead the next person who writes one.
- The counter's inner sandboxes ran nested inside my envelope without error; I did not audit the counter's own
  sandbox flags (that is `R42SentinelCounter`'s lane). In passing: `witness-run.txt:2` records the L1's witness run
  from cwd = the source lane itself, not scratch — Q32's forward leg on L1 receipts is another seat's scope.
- D3's pre-landing receipt combination (`fixtures=14` + `PREDICATE C1 fail`) I could not re-reach on the landed lane
  by any flag combination I tried; my explanation (the L1's `m/dir` copy predated the 29-fixture battery) is
  [INFERENCE] from the receipt's envelope line, not a re-run of that configuration.

## 4. Q32 receipt (host-safety)

Envelope for every counter/fixture/tool run below (bwrap binary `/usr/bin/bwrap`):
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- <command>`

| run | start | end | `ls -A ~/.local/bin \| sha256sum` before → after |
|---|---|---|---|
| draft tools on pinned clone (carried / appendonly / supersede) | 18:10:17 | 18:10:17 | `8cf5b1516051e191…d86d52` → same |
| patched counter, witness dev mode (`--battery-dir …/claims/witness`) | 18:13:17 | 18:13:20 | `8cf5b1516051e191…d86d52` → same |
| patched counter, default battery (no flag) | 18:17:42 | 18:17:46 | `8cf5b1516051e191…d86d52` → same |
| fixture sweep (green/red/mutable/samecommit/pipe3) + tip run | 18:19:20 | 18:19:20 | `8cf5b1516051e191…d86d52` → same |

Full hash (captured after all runs): `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`; the table
shows its 16-char prefix, identical before and after every run. Fixture repos and lane copies (`lane-mut`,
`lane-mut2`, `lane-tip`) live only under `S=/fast/scratch/hyaku/kengaku-r42/F42RevQuality` (round-root sentinel
present); fixture commits used a fixed `fixture` identity; the patched counter ran from a `cp -a` copy so the pinned
clone stayed pristine (no `git checkout`/`reset` needed on it). No host write outside this report, my report subdir
and `$S`; no pacman, no tool installed, no network fetch, no lane git/jj mutation. Scratch deleted after this report.

## 5. Summary

Q33 and Q34 are honest criteria with real, correctly-pinned evidence — every measured number I re-derived matched,
both red halves fail on cue, and the disclosed limits hold. But as landed **neither criterion's executable check can
run**: the tools they name were never committed (D1) and the command lines contradict the tools' own CLIs (D2);
Q33's red half cites a predicate line its prescribed mode cannot print (D3); Q34's pipe sentence is false in the
silent case and its arity inference is invalid (D4); two lower-grade pin/staleness defects (D5, D6).

VERDICT: quality-q33-q34-defects-6
