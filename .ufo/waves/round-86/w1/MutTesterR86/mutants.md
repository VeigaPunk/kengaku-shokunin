# MutTesterR86 — my own mutation battery on both round-86 counters

Seat: `MutTesterR86` (leaf, one v1 wave, no subagent dispatch). Written 2026-11-05.
Measured lane revision for every run below: `master = a571044c1ea7c243791330607c5b90b6afce9a15`.
All production files read-only; every mutant and fixture lived under
`/fast/scratch/hyaku/kengaku-r86/MutTesterR86/` and has been deleted (receipts copied here first).

Nothing in this battery edits the committed counters: each mutant is a **copy** with one
behavior-bearing source edit (`diffs/`), and each fixture is a copy of the measured tree with one
class of defect planted. The question asked of every pair is the honest one:

> (a) does the **unmutated** counter reject that fixture and name the leg, and
> (b) does the **mutant** accept it?

14 runs total: **4 necessary** (the removed guard is load-bearing), **7 redundant** (another leg
catches the same fixture; catcher named), **2 no-check** (no guard exists to disable), plus 1
inverse ("falsely-red") run that shows the derivation mutant cannot launder a clean tree.

## 0. Frozen-contract check (instrument byte audit)

`git diff --stat 316811fa604eeef1d157bdbf62b5595891dc015a..a571044c -- plans/round86_c1_replay.py
plans/round86_c2_repin.py plans/round86_raman_probe.py plans/round86-cases.json
corpus/evidence/round86/ SHONEN.md PROVINCE.md plans/state_check.py` → one file: `PROVINCE.md`
(1 insertion, 1 deletion). Nothing else. Concretely:

| artefact | changed since instrument freeze `316811fa`? |
|---|---|
| `plans/round86_c1_replay.py` | no |
| `plans/round86_c2_repin.py` | no |
| `plans/round86_raman_probe.py` | no |
| `plans/round86-cases.json` | no |
| `corpus/evidence/round86/raman-fitting-probe.txt` | no |
| `SHONEN.md`, `plans/state_check.py` | no |
| `plans/grader-population-ledger.json` | **yes** — only the `raman-fitting` row, red→`status=executed/round=86/receipt/subject/verdict` (that is the claim's own artefact, not an instrument) |
| `PROVINCE.md` | **yes**, at `a571044c`: the public-literature registry cell at line ~1041 (`rows=253` → `rows=266`). Line 1041 is far below `### Adjacent`, and `### Adjacent` is still line 151 — verified by re-deriving from bytes. |

**No instrument byte changed after the tip run; nothing voids either claim.** Note also that the
post-tip `PROVINCE.md` edit is precisely the drift class C2's `P1` is built for: the token line was
re-measured from the new bytes (`151`), not restored from a constant, and the C2 baseline re-run at
`a571044c` still prints `derived_line=151 … defects=0`.

Counter bytes at battery start and end (worktree, sha256): `round86_c1_replay.py`
`04f6ec2ae8d2e4e51a5937c3e4c0a71c8db5ec4640c65c3498cdd659f95940cf`, `round86_c2_repin.py`
`a3fbf5064c1c84707dac711550df29087c3be8cefa3e4c44c0d53aa3566bd036`, probe
`09731b3ebcf4448546184b39d21d9a28016693af935a20f7efddec5cff209cde` (= the receipt's `TOOL_SHA` and
the counter's `TRUSTED_TOOL_SHA`), case table
`f8aa21f3b3f6ccf9616f9d54e9b6aa2c8482de1f32fadbb33166713c6b2210a4` (= `CASE_TABLE_SHA` in the receipt
and `FROZEN_TABLE_SHA` in the probe), receipt
`192932b28a24efda94744f2ceb0d62accd268f7e6842f230a3e66e4c8d773411`, ledger
`b2e87381b2f3d8c3303389b89233aa627b73db68e273d19f333d7ab79aa76ff4`. All six identical before and
after the battery.

## 1. Baselines before any mutant (a baseline failure would be inconclusive)

```
$ python3 plans/round86_c1_replay.py --lane . --work …/base-c1 --rev a571044c…   → rc=0
  TARGET members=1 cases=8 legs=24 mismatches=0 located=1 executed=1 defects=0
  PREDICATE R86-C1 pass
$ python3 plans/round86_c2_repin.py --lane <clean reflink copy of master>          → rc=0
  TARGET derived_line=151 shonen_pointer=PROVINCE.md:151 pin_line=151 state_mismatches=0 selftest=pass defects=0
  PREDICATE R86-C2 pass
$ python3 plans/round86_c2_repin.py --lane . --rev a571044c…                       → rc=0, same TARGET
```

So every rejection reported below is caused by the planted fixture, not by the tree.

## 2. The battery (14 runs)

Fixtures are built from `a571044c` bytes. `--repo .` keeps the freeze anchor and the tip-ancestry
check on the real lane; the fixture only supplies the measured tree.

| # | mutant (edit) | fixture it should let through | unmutated: rejects? (defect lines) | mutant: accepts? | verdict |
|---|---|---|---|---|---|
| 1 | `exit-nonzero-accepted`: `EXIT != "0"` → `EXIT not in ("0","1")` | receipt `EXIT 0` → `EXIT 1`, tree/ledger otherwise intact | rc=1 — `DEFECT L2-stamp exit=1` | **yes**, rc=0 `PREDICATE R86-C1 pass` | **necessary** |
| 2 | `table-member-accepted`: drop the frozen-table identity guard (`doc.member/subject_sha` @ `FREEZE_REV`) | measured `round86-cases.json` `member: raman-fitting` → `other-member` (receipt digest left as committed) | rc=1 — `L4-table drift 3975605f… != f8aa21f3…`; `L6-reproduce rc=2 no observation block` | **no** — same two legs still fire (L2 `table_sha` also fires when the digest is not re-minted) | **redundant**, catcher `L4-table` (+`L6-reproduce`) |
| 3 | `table-member-accepted-deep`: also drop the L4 byte comparison **and** the L2 `CASE_TABLE_SHA` comparison | same half-vector table, receipt `CASE_TABLE_SHA` re-minted to the drifted bytes | rc=1 — `L2-stamp table_sha=3975605f…`; `L4-table drift …`; `L6-reproduce rc=2` | **no** — only `L6-reproduce rc=2 no observation block` remains | **redundant**, catcher `L6-reproduce` (the probe's own `FROZEN_TABLE_SHA`/member refusal) |
| 4 | `freeze-anchor-nonfatal`: the `except SetupDefect` handler no longer fails closed (prints the target instead of `DEFECT SETUP`, rc 2) | intact tree, `--freeze 88651a72…` (BASE carries no `plans/round86-cases.json`) | rc=**2** — `DEFECT SETUP frozen-input-missing plans/round86-cases.json@88651a72ef11`, `PREDICATE R86-C1 fail` | **yes**, rc=0 `PREDICATE R86-C1 pass` for a freeze revision that carries no table | **necessary** |
| 5 | `executed-always-1`: `stats["executed"] = 1` moves out of the `status == "executed"` branch | ledger row `status: executed` → `unexecuted` (all other fields correct) | rc=1 — `DEFECT L7-ledger status=unexecuted` | **no** — `L7-ledger status=unexecuted` still fires; the mutant only makes the `TARGET` line print `executed=1` | **redundant**, catcher `L7-ledger` |
| 6 | `predicate-absent-accepted`: `if predicate != "pass":` → `if False:` | receipt observation block loses its `PREDICATE R86-PROBE pass` line | rc=1 — `L5-vectors predicate=absent`; `L6-reproduce rc=0 block differs` | **no** — `L6-reproduce rc=0 block differs` still fires | **redundant**, catcher `L6-reproduce` |
| 7 | `missing-stamp-field-accepted`: `missing = [...]` → `missing = []` | receipt loses its `WORKTREE dirty` stamp line | rc=1 — `DEFECT L2-stamp missing=WORKTREE` | **yes**, rc=0 | **necessary** |
| 8 | (no edit; the candidate is "accept a receipt whose WORKTREE says dirty") | the **committed** receipt as delivered (`WORKTREE dirty`, sha256 `192932b2…`) | **accepts**: rc=0 `PREDICATE R86-C1 pass` | n/a — there is no guard to disable | **no-check** |
| 9 | (no edit; same candidate, maximal form) | receipt `WORKTREE` → `exploded // n/a` | **accepts**: rc=0 `PREDICATE R86-C1 pass` | n/a | **no-check** |
| 10 | `skip-p5-selftest`: `if selftest:` → `if False:` | fixture whose `plans/state_check.py --selftest` returns 1 while `--summary` is green (`if args.selftest: return run_selftest()` → `return 1`) | rc=1 — `DEFECT P5-selftest exit!=0` (P1–P4 green) | **yes**, rc=0 `PREDICATE R86-C2 pass` | **necessary** |
| 11 | `derive-returns-stale-line`: `return hits[0]` → `return STALE_LINE` (129) | stale-pin fixture: `SHONEN.md` pointer and `state_check.py` box-4 pin both back at `PROVINCE.md:129`, bytes still have `### Adjacent` at 151 | rc=1 — `P2-shonen`, `P3-pin`, `P4-state mismatches=1` | **no** — `P4-state mismatches=1` still fires (`state_check --summary` re-derives the line itself) | **redundant**, catcher `P4-state` |
| 12 | `pin-line-lax`: `if not pin_ok or line != derived:` → `if not pin_ok:` | pin line 129, `SHONEN` pointer 151, bytes 151 | rc=1 — `P3-pin line=129 derived=151`; `P4-state` | **no** — `P4-state` still fires | **redundant**, catcher `P4-state` |
| 13 | `shonen-compares-to-stale`: P2 compares the pointer to `STALE_LINE` instead of the derived line | `SHONEN` pointer 129, pin 151, bytes 151 | rc=1 — `P2-shonen pointer=PROVINCE.md:129 derived=PROVINCE.md:151`; `P4-state` | **no** — `P4-state` still fires | **redundant**, catcher `P4-state` |
| 14 | `derive-returns-stale-line` (same mutant as #11), **inverse** fixture: the delivered clean tree | none — this is the target tree itself | rc=0 `PREDICATE R86-C2 pass` | **no**, rc=1 — `P2-shonen pointer=PROVINCE.md:151 derived=PROVINCE.md:129`; `P3-pin line=151 derived=129` | **falsely-red** — the mutant cannot launder a clean tree, and `P2`/`P3` name the drift |

Raw lines for all 14 runs: `runs.txt` (human) and `runs.json` (machine, incl. every edit's
needle/replacement and both stdout extracts).

## 3. Necessary (4) — each removed guard decides its own fixture

* **`EXIT` (#1).** A receipt claiming `EXIT 1` passes every other leg (the stamp fields still agree
  with the measured bytes; the observation block is byte-identical to a fresh probe run) and reaches
  the target once the `EXIT == "0"` comparison is relaxed to "0 or 1". The exit-code binding on the
  receipt is load-bearing and not shadowed anywhere else.
* **Freeze anchor fail-closed (#4).** With `--freeze` naming a resolvable revision that carries no
  case table, the pristine counter is right to refuse to grade (rc 2, `DEFECT SETUP`, `PREDICATE
  R86-C1 fail`). Making that `SetupDefect` non-fatal is the difference between "cannot evaluate" and
  "target reached" for a measuring setup that is simply absent — the single most dangerous mutation
  to this claim's shape, because a counter that grades a missing freeze anchor can print
  `defects=0` from nothing.
* **Stamp completeness (#7).** A receipt that is missing a required stamp field is refused only by
  the `missing=…` leg; nothing else compares stamp presence.
* **`P5-selftest` (#10).** A tree whose `state_check.py` still summarises green but no longer
  selftests clean is invisible to `P1`–`P4` and is refused only by `P5`. The round's own edit
  touches the pin *inside that instrument*, so this leg is the one that says the edit did not break
  the instrument holding it.

## 4. Redundant (7) — defence in depth, catcher named

* **#2/#3 — "a table whose `member` differs from the frozen one" is caught three times over.**
  Removing the frozen-table identity guard is inert because the measured table is compared to the
  *frozen bytes* read at `FREEZE_REV`: `L4-table` fires on the half-vector drift. Remove `L4` and
  the receipt digest as well (#3) and the `L2-stamp table_sha` leg had already been removed, so the
  fixture is still refused by `L6-reproduce rc=2 no observation block` — the probe's own
  `FROZEN_TABLE_SHA` / `wrong-table member` refusal. Net: L2 digest → L4 bytes → L6 probe pin, three
  independent gates; the frozen-identity guard is a fourth, and its necessity is *unobservable*
  without also breaking L4 and L6, i.e. it guards a compromise that no fixture from this repo's
  history can otherwise construct.
* **#5 — `executed == 1` cannot fail alone.** `stats["executed"]` is assigned only inside the
  `status == "executed"` branch of L7, so `executed == 0` always comes with the L7 `status=…`
  problem. The `executed == 1` conjunct in `result_code` is therefore entailed by L7 and never the
  sole failing condition. (The mutant inflates the `TARGET` line's `executed=1` and still fails.)
* **#6 — a missing `PREDICATE R86-PROBE` line is caught by `L6-reproduce`, not (only) by L5.** Any
  block-level drift is caught by L6's exact block equality; L5's `predicate != "pass"` check is the
  leg that survives when L6 is disabled — which is exactly why the shipped `no-vectors-no-reproduce`
  mutant removes both.
* **#11–#13 — the P2/P3 pins are all shadowed by `P4-state`.** `state_check.py --summary` re-derives
  the box-4 pointer from `PROVINCE.md` bytes itself, so a stale pointer/pin is red in P4 even when
  P2 or P3 has been relaxed. #11 additionally shows the *derivation* mutant is safe: with
  `derive()` returning `STALE_LINE` the stale-pin fixture still fails on P4, and on the clean tree
  (#14) the mutant turns the target tree red on P2/P3.

`--selftest` cross-check (`selftest-crosscheck.txt`): the counters' own batteries kill three of
these mutants independently — `freeze-anchor-nonfatal` → `SELFTEST freeze-anchor-fails-closed FAIL`
(rc 1), `table-member-accepted-deep` → `SELFTEST table-drift-red FAIL`, and
`derive-returns-stale-line` → `SELFTEST derive-is-not-the-stale-line FAIL`. The other mutants
(`exit`, `missing-field`, `predicate-absent`, `executed-always-1`, `pin-line-lax`,
`shonen-compares-to-stale`, `skip-p5-selftest`) pass `--selftest` with rc 0, so `--selftest` is not
a substitute for the mutants — it is a second net that happens to catch two of them.

## 5. The `WORKTREE` candidate: no check exists (no-check, not a claim defect)

The item's menu included "accept a receipt whose `WORKTREE` says dirty". It cannot be turned into a
mutant pair, and here is the measurement rather than the argument:

```
[worktree:delivered-receipt-dirty] WORKTREE=dirty (committed bytes) rc=0 PREDICATE R86-C1 pass
[worktree:worktree-junk] WORKTREE=exploded // n/a rc=0 PREDICATE R86-C1 pass
# (the first is the receipt exactly as committed, sha256 192932b2…; the second rewrites its value)
```

`WORKTREE` is in `REQUIRED`, so its **presence** is checked (#7 proves that), but its **value** is
never compared — the counter's L2 agrees only `MEMBER/SUBJECT_CAPTURE/SUBJECT_SHA/CASE_TABLE_SHA/
TOOL/TOOL_SHA/EXIT` with the measured bytes, exactly as the frozen claim words it. Two
consequences, stated so neither is overclaimed:

1. **Not a claim defect.** The frozen C1 text lists the fields whose agreement L2 must establish and
   `WORKTREE` is not among them; the committed receipt records `dirty` (sha256 `192932b2…`, minted
   at `bfda0472`), and the lane worktree does carry untracked sibling wave files today. Neither
   target output nor kill rule depends on the field.
2. **A departure worth knowing.** Rounds 80 and 81 did compare the value:
   `plans/round80_c1_located_replay.py:277-278` adds a `WORKTREE-DIRTY` defect when
   `stamp.get("WORKTREE") != "clean"`, and `plans/round81_c1_new_members.py:344-347` does the same.
   Round 86 records the field and does not gate on it. The exposure is limited because the bytes that
   matter are pinned independently — `TOOL_SHA` == `TRUSTED_TOOL_SHA` and the tree's tool digest,
   `L4` on the table bytes, and `L6` re-running the probe under `-I` in a bubblewrap namespace that
   mounts only the staged capture and the case directory (the lane is never mounted) — so a dirty
   mint can only mean *unmeasured extra files elsewhere in the lane*, not different
   tool/table/subject bytes.

## 6. Honest limits of this battery

* Fixtures are constructed by the seat, so a mutant is only exercised on the defect class I could
  build. #2/#3's conclusion ("the frozen-identity guard's necessity is unobservable") is a statement
  about constructible fixtures, not a proof that the guard is dead code.
* The mutants are text replacements on copies; none of them is a shipped `MUTANTS` tuple (the
  shipped C1 tuples: `no-vectors-no-reproduce`, `no-ledger`, `no-tool-sha`, `no-tip-binding`,
  `no-table-binding`, `no-exit`; C2: `no-state`, `no-shonen`, `no-pin`). `exit-nonzero-accepted`
  deliberately relaxes rather than deletes the EXIT comparison, and `pin-line-lax` /
  `shonen-compares-to-stale` are laxer comparisons, not the shipped removals.
* `freeze-anchor-nonfatal` replaces the `SetupDefect` handler with a stub that prints the target; it
  therefore also fabricates the `TARGET` counts. That is why I report its `--selftest` kill
  separately — the mutant is not a realistic implementation, only the minimal way to make the anchor
  non-fatal.
* C1's L6 re-runs the probe under `bubblewrap` on every run; the whole battery is 14 runs in ~70–80 s,
  so no fixture is a timing artefact. Nothing here runs Terminal-Bench, a task image or a harness,
  and no claim is made about model or agent behaviour.
* No instrument, ledger, receipt, case table, `SHONEN.md`, `PROVINCE.md` or `state_check.py` byte was
  written by this seat: the sha256 of all six measured artefacts is identical before and after the
  battery (`runs.json` → `instrument_hashes_before` / `_after`), and the mutated copies are copies.
  Over the battery window `git status --porcelain --untracked-files=no` held exactly one line,
  ` M .ufo/waves/round-86/w1/ExecCensusR86/census.txt` (a sibling seat's tracked file), before *and*
  after. A second tracked modification, ` M corpus/lessons/round-86.md`, appeared after my battery
  finished; it is not this seat's write (this seat wrote only the six files in this directory and its
  own scratch, now deleted).

## 7. Findings against the two claims

**0 defects.** Both counters reject every defect fixture in the battery and reach their target only
when the corresponding guard is removed or relaxed; the necessary set is non-empty on both axes
(C1: 3, C2: 1), the redundant set names its catcher in every case, and the one candidate on the
item's menu without a guard (`WORKTREE`) is reported above with the evidence why it is a no-check
rather than a hole in the claim.

Notes for the L1 (not claim defects): (i) `WORKTREE` is presence-only and drops the rounds-80/81
`WORKTREE clean` gate; (ii) `executed == 1` in `result_code` is entailed by L7 and cannot fail alone;
(iii) L5's vector/predicate legs are subsumed by L6's block equality except when L6 itself is
disabled — the same relationship the shipped `DECLARED_REDUNDANT` already declares.

## 8. Evidence in this directory

| file | what |
|---|---|
| `mutants.md` | this report |
| `runs.txt` / `runs.json` | the 14 runs: fixture, edits, rc, defect lines, `TARGET`, predicate; plus instrument hashes before/after and the tracked-status before/after |
| `battery.py` | the driver that built fixtures, applied edits and ran both copies (`python3 battery.py` from scratch; ~70–80 s) |
| `diffs/*.diff` | `diff -u` of each of the 11 mutated copies against the committed counter |
| `mutant-hashes.txt` | sha256 of each mutated copy |
| `selftest-crosscheck.txt` | each mutated copy run under the counter's own `--selftest` (second detector) |

Scratch (`/fast/scratch/hyaku/kengaku-r86/MutTesterR86`, ≈11 GB / 9.2 GB apparent of reflinked
fixture trees, run work dirs and the mutated copies) deleted after these receipts were copied here.
