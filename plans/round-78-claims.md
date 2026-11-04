# kengaku round 78 — frozen claims (2026-11-04)

L1: `KengakuR78`. Base: the lane tip at round start (`3ae0ab54`, round-77 verifier spot-check).
This file is frozen **before data**: no counter below has been run over the after state when it was
written. Amendments land as new `## Amendment` sections; they may only add defects, never move a
target, a control or a kill rule (R77-A3..A5 discipline).

Two claims, distinct axes, causally separable: C1 is measured over `SKILL.md` + the census receipt +
a new ledger; C2 is measured over `corpus/evidence/round77|78/` receipts. Neither counter reads the
other's artifact.

## R78-C1 — coverage (lowest non-retired axis, L0-capped at 7)

**Claim.** The three grader classes the lane declares *partially executed* — the only classes whose
member maps are still prose — become a machine-checked member ledger: every member of
`network-service` (8), `process-environment` (3) and `db-state` (2) is accounted exactly once, each
`executed` member names a tracked receipt whose own bytes print its passing predicate, each
`unexecuted` member names a typed reason that a frozen detector must find in that task's stored
grader bytes, and the three `SKILL.md` class rows carry `executed k of n` plus the ledger pointer.

**Why the prior state lacked it.** `SKILL.md:78,81,83` state `executed 4 of 8` / `2 of 3` / `1 of 2`
as prose. `grep -c 'grader-selected-members' SKILL.md plans/` → 0 at base. No command can name the
four executed `network-service` members from the table's bytes, and no command can falsify an
`unexecuted` reason: the round-62 census
(`corpus/evidence/round62/class-survey.txt`) publishes `CLASS … count=… members=…` but nothing
counts how many of those members the lane has replayed.

**Frozen predicate (one sentence, same in counter, receipt and report).**
`PREDICATE R78-C1 pass` iff `plans/round78_c1_class_member_ledger.py --lane .` prints
`DEFECTS n=0` over the universe it derives from `SKILL.md`'s partial-execution rows and prints the
target tuple `TARGET classes=3 members=<M> executed=<E> unexecuted=<U> unaccounted=0 unbacked=0`.

**Counter.** `python3 plans/round78_c1_class_member_ledger.py --lane .` — modes `--rev REV`,
`--selftest --work DIR`, `--mutants --work DIR`, `--control-prose --work DIR`, `--receipt PATH`.
Exit `0` pass, `1` fail, `2` setup.

**Universe (derived, not listed).** Classes := rows of `SKILL.md` §Decision table — grader class
whose `executed` cell matches `executed (\d+) of (\d+)`. Members := that class's `members=` list in
the round-62 census receipt. The counter prints `UNIVERSE classes=<n> members=<m>` and refuses if
either is zero.

**Defect classes.** `MEMBER-UNACCOUNTED`, `MEMBER-EXTRA`, `MEMBER-DUPLICATE`, `CLASS-NOT-IN-CENSUS`,
`COUNT-DRIFT`, `CLASS-ROW-UNLINKED`, `RECEIPT-MISSING`, `RECEIPT-UNTRACKED`, `PREDICATE-ABSENT`,
`EXIT-MISSING`, `ROUND-INVALID`, `STATUS-UNKNOWN`, `REASON-UNKNOWN`, `REASON-UNBACKED`,
`COVERAGE-REGRESSION`.

**Before → after.** Before: no ledger file exists → `LEDGER rows=0`, `<m>` `MEMBER-UNACCOUNTED`
defects, rc 1. After: the ledger lands, the three `SKILL.md` rows carry `k of n` + the ledger
pointer, `DEFECTS n=0`, rc 0.

**Control (must lose).** `--control-prose`: build a ledger from the SKILL rows' prose alone — the
`k of n` numbers with fabricated member names, no receipts and no reason detectors — and score the
same target. It cannot reach `unaccounted=0 unbacked=0` because it names no member the census
carries and resolves no receipt; the counter prints `CONTROL … target_reached=False`.

**Kill rules.** A red before-run at the base revision (rc 1 with the named defect classes) and a
green after-run at the landing tip are both required; a ledger row that passes with the detector
removed (mutant matrix) is a killed claim; a `--control-prose` run that reaches the target invalidates
the counter and the claim is withdrawn before data.

**Axis.** coverage — the surface is the 13-member map of the three partially executed grader classes,
not the numbers 4/2/1.

## R78-C2 — calibration (held at ceiling 10, exercised)

**Claim.** Every receipt under `corpus/evidence/round77/` and `corpus/evidence/round78/` that carries
a verdict signature becomes self-locating: it stamps `LANE_TIP` (an ancestor of `master`),
`WORKTREE`, `TOOL` + `TOOL_SHA` recomputable at **its own stamped revision** (or `TOOL-SUPPLIED` +
`WORKTREE dirty` when the tool did not exist there), and `COMMAND`; the round-77 closure's routed
defects D1/D2 (mis-stamped rerun and battery receipts), D3 (the SCORECARD stamp prose), D4 (the
missing at-tip rerun block) and D5 (`WORKTREE clean` printed for an untracked supplied tool) are
closed by re-minted receipts and dated corrections.

**Why the prior state lacked it.** The round-77 closure (`corpus/lessons/round-77-verifier-spotcheck.md`
§6) priced five routing items, two of them HIGH/MEDIUM: `c1-selftest.txt` stamps `LANE_TIP
51ffc14f` with `TOOL_SHA a4777acf…` while the tool at `51ffc14f` hashes `5a507c08…`; the rerun
receipts stamp `9ebb8ed1` whose tree cannot produce their pass; `c1-before.txt` prints `WORKTREE
clean` for a tool it supplied untracked. No committed gate re-derives a receipt's claims at the
receipt's own stamp.

**Frozen predicate.** `PREDICATE R78-C2 pass` iff `plans/round78_c2_stamp_location.py --lane .`
prints `DEFECTS n=0` and `TARGET receipts=<R> located=<R> unlocated=0`.

**Counter.** `python3 plans/round78_c2_stamp_location.py --lane .` — modes `--rev REV`,
`--selftest --work DIR`, `--mutants --work DIR`, `--control-stamp-only --work DIR`, `--receipt PATH`.
Exit `0` pass, `1` fail, `2` setup.

**Universe (derived, not listed).** Regular files under `corpus/evidence/round77/` and
`corpus/evidence/round78/` (excluding `sources/`) whose first 40 lines match a verdict signature
(`LANE_TIP`, `PREDICATE`, `SELFTEST`, `MUTANTS`, `CONTROL`, `VERDICT:`, `exit `). The counter prints
`UNIVERSE dirs=2 receipts=<n>`.

**Legs.** `TIP-ABSENT`, `TIP-UNRESOLVED`, `TIP-NOT-ANCESTOR`, `WORKTREE-ABSENT`,
`TOOL-UNNAMED` (a `TOOL_SHA` with no `TOOL`), `TOOL-DRIFT` (recomputed digest at the stamped tip
differs), `TOOL-ABSENT-AT-TIP` (tool not in that tree and no `TOOL-SUPPLIED` line),
`SUPPLIED-BUT-CLEAN` (`WORKTREE clean` on a receipt whose tool is absent at its tip — D5),
`COMMAND-ABSENT` (verdict line without a `COMMAND`), `PASS-UNLOCATED` (`PREDICATE … pass` with
neither tool pair nor supplied marker), `STAMP-CONFLICT` (two `LANE_TIP` values in one receipt).

**Before → after.** Before: the round-77 receipts as committed → the two HIGH/MEDIUM classes above
fire; after: every round-77 receipt re-minted at a tip that carries the tool it names (or marked
`TOOL-SUPPLIED` + `WORKTREE dirty` for a before receipt), the round-78 receipts minted located from
the start, `DEFECTS n=0`, rc 0.

**Control (must lose).** `--control-stamp-only`: accept any receipt that carries a `LANE_TIP` line
and skip the digest/command/supplied legs. It reaches `located=R` but cannot reach
`TOOL-DRIFT 0 SUPPLIED-BUT-CLEAN 0`, so `target_reached=False` is printed on a fixture where the
skipped legs fire.

**Kill rules.** A receipt whose `TOOL_SHA` matches by coincidence of a truncated pin is refused (full
digest comparison); a red before-run and a green after-run are both required; a mutant that removes
the digest leg and still passes is a killed claim.

**Axis.** calibration — the surface is the lane's evidence self-description (a receipt that cannot be
located at its own stamp over-claims what the lane can prove about itself).

## Out of scope (declared, not claimed)

- Simulating the 6 unexecuted members: this claim accounts for them with detector-backed reasons; it
  does not replay them (a replay is the next coverage move, one member per round as in rounds 63–72).
- Re-minting receipts outside `round77`/`round78`: older receipts predate the stamping discipline and
  are recorded as stated limits, not repaired here.
- Assimilation: `merge/kengaku` stays unadopted (L0 `kengaku | round-54`).

## Amendment A1 (round 78, 2026-11-04, from the wave's critic/reviewer/sentinel) — only adds defects

Both frozen predicates, both targets, both controls and both kill rules are unchanged; each leg
below can only add a defect to a receipt or a ledger row that the frozen form let through.

**R78-C1.** (a) `SKILL.md` fenced blocks are skipped when the class table is parsed — a fenced
shadow table can no longer replace the real one (`...` rows inside ```). (b) A row whose `k == n`
is `CLASS-NOT-PARTIAL`. (c) The ledger is decoded with a duplicate-key hook, so a repeated member
key is `MEMBER-DUPLICATE` instead of being silently collapsed by `json.loads`. (d) An `executed`
receipt must name its task (`TASK-UNDER-TEST <member>` or the member string) — `TASK-MISMATCH`
otherwise, which is what stops a same-class receipt swap and a foreign-round census pass.
(e) A `vectors` verdict needs at least two `VECTOR … frozen=match` lines and no mismatch; one
arbitrary line is no longer a table. (f) A receipt path that is absolute, contains `..`, or is a
symlink is `RECEIPT-ESCAPE` / `RECEIPT-SYMLINK`; a census member name outside `[A-Za-z0-9._-]+` is
`MEMBER-NAME-ESCAPE` and its grader bytes are not read.

**R78-C2.** (a) Tool bytes are resolved **at each receipt's own stamped revision** (the frozen
sentence; the first form read them from the audit tip). (b) `TOOL_SHA` must be a full 64-hex
digest — a shorter pin is `TOOL-PIN-SHORT`, so the truncated-pin bypass is closed. (c) A
`TOOL-SUPPLIED` block with no digest requires the named path to exist in the audit tree, else
`SUPPLIED-UNRECOVERABLE`. (d) Two different `LANE_TIP` values with no `RE-STAMPED`/`CORRECTION`
marker in the last block are `STAMP-CONFLICT` again; a labelled re-stamp still supersedes.
