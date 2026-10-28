# C2ExecA — attribute routed-findings ledger rows 1–9 (0-based 0..8)

Seat: C2ExecA (executor), kengaku round 51, hyaku run 11, 2026-10-28.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Fragment delivered: `.ufo/waves/round-51/w1/C2ExecA.jsonl` (9 rows, one complete object per line).
Binding doc read first: `plans/round-51-claims.md` (§C2 predicate, dispositions, kill rule, limits), then the
frozen instrument `plans/round51_routing.py` in full.

REV e07f131cf7037e58a21db6e1f3986cf401ad257c

## Axes named

1. **adjacency 8 → 9** (the claimed axis; my rows are the C2 counter's input): every row names its owner lane
   and a disposition from the frozen set, every `source` resolves, every `check` is a runnable command, and every
   `fixed-verified` check exits 0 in a counter-equivalent harness.
2. **check truthfulness** (sub-axis of adjacency, held separate because it is falsifiable on its own): a `check`
   that cannot run from the counter's cwd is not a check — measured, not assumed, on all 9 rows.
3. **not-absorbed** (the axis's own signal): the owner is the lane that owns the *fix surface*, not the lane that
   filed the row; where a sibling owns the rule but not the surface, the sibling is named in the evidence and the
   row stays with the surface owner.

## Method

- Read the 9 rows from the lane ledger and each `source` pointer; verified the cited line carries the claim
  (`corpus/lessons/round-39-verifier-spotcheck.md:132,134,135,136,140`;
  `corpus/lessons/round-40-verifier-spotcheck.md:92,95,97,99`).
- Measured in a **clean clone at the stage-1 freeze commit** (`git clone --shared … ; git checkout e07f131`),
  because the live lane tree was dirty and being rewritten while the wave ran (see Limits).
- Ran every check twice: (A) as written in the ledger, in the counter's own harness (`bash -lc <check>`,
  `cwd=<scratch work>`, `LANE=<lane>`, `TMPDIR=<scratch work>`, 60 s), and (B) lane-anchored (`$LANE/...`),
  same harness. Then substituted the 9 attributed rows into a scratch copy of the ledger (71 rows) and ran the
  frozen counter `python3 plans/round51_routing.py --lane . --run-checks`.

## Summary table (rows 0..8 = ledger lines 1..9)

| # | id | owner | disposition | check rc (clean clone @ e07f131) | owner evidence |
|---|----|-------|-------------|----------------------------------|----------------|
| 0 | R39-R1 | kengaku | fixed-verified | 0 | `SKILL.md:590` `order-check`, `SKILL.md:591` `round39-c1-audit`; close commit `ec17216` resolves (`git log -1` → "round-40: battery40 … SKILL section + registry rows") |
| 1 | R39-R2 | kengaku | accepted-risk | 1 (residual persists) | `SKILL.md:664`: "`plans/git_leak_probe.py` does not create `--work` (an absent dir is a `FileNotFoundError` traceback, exit 1 …) … the probe is pinned by `plans/round39_c2_verify.py` `PROBE_SHA256` and `plans/pkg-spec-r39.json` `frozen_instruments`, so it is not edited — create `--work` first" |
| 2 | R39-R3 | kengaku | accepted-risk | 1 (order class absent) | own defect ledger + own pins: blocker names `plans/ledger_tip.py:6-7,72-73` and `plans/round40_c1_verify.py:98` |
| 3 | R39-R4 | kengaku | accepted-risk | 2 (SETUP, as the note records) | bundle of this lane's own instruments (`plans/order_check.py`, `plans/tip_receipts.py`, `plans/mutant_direction_check.py`); `PROVINCE.md:262`: "`plans/pkg_gate.py` stays this lane's own gate (tameshi owns the reusable fixture/mutation method and never edits a sibling's gate)" |
| 4 | R39-R5 | kengaku | fixed-verified | 0 | residue was kengaku's own seat dirs `/fast/scratch/hyaku/kengaku-r39*`; souji's declared hygiene surfaces are "the fleet root repo's … stray checkpoint/scratch files" and per-lane "`.scratch/`" (`souji-shokunin/PROVINCE.md:8,10-11`) — neither covers the wave scratch root |
| 5 | R40-R1 | kengaku | fixed-verified | 0 | `PROVINCE.md:462`: "(`plans/round40_c1_verify.py`, `plans/battery40/`) is kengaku's instrument for its own self-assessment" |
| 6 | R40-R2 | kengaku | fixed-verified | 0 | remedy lives in this lane's `.ufo/waves/round-41/build-spec.json:5` + its own crit modules; the fleet-wide seat-containment *rule* is kumitate's (`kumitate-shokunin/PROVINCE.md:22` "seat-containment rules") and is named as adjacent, not absorbed |
| 7 | R40-R3 | kengaku | fixed-verified | 0 | `SKILL.md:598` `round-close-check`, `SKILL.md:670` "Round-41 registry addendum" |
| 8 | R40-R4 | kengaku | fixed-verified | 0 | `.ufo/waves/round-41/claims/control-c1-nothing.txt:28` + `plans/round41_c1_verify.py:586,590` |

Totals: 9/9 attributed, 9/9 dispositioned, 6 fixed-verified (6/6 checks exit 0 in the run), 3 accepted-risk,
0 routed/referral (see "Why no row is routed" below), 0 rows deleted, 0 rows added, 0 `next` violations.

## Exact commands run (all from `/fast/scratch/hyaku/kengaku-r51/C2ExecA`, `TMPDIR` set there)

```sh
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane checkout -q e07f131cf7037e58a21db6e1f3986cf401ad257c   # rev-parse --show-toplevel == scratch/lane
# (A) original checks in the counter harness: cwd=<scratch>/work, LANE=<lane>, TMPDIR=<scratch>/work
python3 runchecks.py
# (B) lane-anchored checks, same harness
grep -q '^| `order-check`' "$LANE/SKILL.md" && grep -q '^| `round39-c1-audit`' "$LANE/SKILL.md"
d=$(mktemp -d -p "${TMPDIR:-/tmp}"); python3 "$LANE/plans/git_leak_probe.py" --lane "$LANE" --work "$d/absent" >/dev/null 2>&1; rc=$?; rm -rf -- "$d"; [ "$rc" -eq 2 ] || [ "$rc" -eq 0 ]
grep -q '"order' "$LANE/corpus/defects.jsonl"
python3 "$LANE/plans/mutant_direction_check.py" --lane "$LANE" --counter "$LANE/plans/round39_c1_verify.py"
test -z "$(ls -d /fast/scratch/hyaku/kengaku-r39* 2>/dev/null)"
grep -q 'unshare-ipc' "$LANE/plans/round42_c1_verify.py" && grep -q 'unattributed' "$LANE/plans/round42_c1_verify.py" && grep -qs 'R42-R1' "$LANE/corpus/routed-findings.jsonl"
grep -q 'ro-bind /home/vgpnk/.local/bin' "$LANE/.ufo/waves/round-41/build-spec.json" && grep -q 'NEUTRALIZED' "$LANE/.ufo/waves/round-40/build/R40CritC1Counter/crit_git_shim.py" && grep -q 'NEUTRALIZED' "$LANE/.ufo/waves/round-40/build/R40CritC1Counter/crit_ledger_selfread.py"
grep -q '^| `round-close-check`' "$LANE/SKILL.md" && grep -q '^Round-41 registry addendum' "$LANE/SKILL.md"
grep -q 'ADVERTISED direct=21 indirect=2 none=0' "$LANE/.ufo/waves/round-41/claims/control-c1-nothing.txt"
# (C) frozen counter over a 71-row scratch ledger = my 9 rows + original rows 9..70, in a copy of the clean clone
python3 plans/round51_routing.py --lane . --run-checks
```

## Evidence (verbatim)

### 1. The checks as shipped cannot run from the counter's cwd — 7 of 9 red, 1 false green

Counter harness (`cwd=<scratch work>`, `LANE=<lane>`), original check strings:

```
ROW 0 R39-R1 rc=2 :: grep: SKILL.md: No such file or directory
ROW 1 R39-R2 rc=0 ::
ROW 2 R39-R3 rc=2 :: grep: corpus/defects.jsonl: No such file or directory
ROW 3 R39-R4 rc=2 :: python3: can't open file '/fast/scratch/hyaku/kengaku-r51/C2ExecA/work/plans/mutant_direction_check.py': [Errno 2] No such file or directory
ROW 4 R39-R5 rc=0 ::
ROW 5 R40-R1 rc=2 :: grep: plans/round42_c1_verify.py: No such file or directory
ROW 6 R40-R2 rc=2 :: grep: .ufo/waves/round-41/build-spec.json: No such file or directory
ROW 7 R40-R3 rc=2 :: grep: SKILL.md: No such file or directory
ROW 8 R40-R4 rc=2 :: grep: .ufo/waves/round-41/claims/control-c1-nothing.txt: No such file or directory
```

ROW 1's `rc=0` is a **false pass**: `python3 plans/git_leak_probe.py` cannot be opened from the scratch cwd and
python exits **2** for a missing script, which the check's `[ "$rc" -eq 2 ]` accepts. Every `fixed-verified` row
would have been scored against a check that never touched the lane. This is why all 9 `check` fields are
lane-anchored to `$LANE` in the fragment; every other field is byte-preserved (verified by re-parsing: the only
differing key on all 9 rows is `check`).

### 2. R39-R2 — residual re-measured, still unfixed (accepted-risk)

```
$ python3 "$L/plans/git_leak_probe.py" --lane "$L" --work "$d/absent"
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/git_leak_probe.py", line 301, in <module>
    sys.exit(main())
  File "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/git_leak_probe.py", line 258, in main
    root = pathlib.Path(tempfile.mkdtemp(prefix="k39-glr-", dir=a.work))
  ...
FileNotFoundError: [Errno 2] No such file or directory: '.../work/tmp.ONGKSMVvJ1/absent/k39-glr-mc4oq4_3'
rc=1
```

Control with an existing `--work` dir: `rc=0`. The lane's decision is recorded in `SKILL.md:664` (quote in the
table): the probe is digest-pinned by two instruments, so it is not edited and the precondition is declared
instead. Owner kengaku (it is this lane's probe, `PROVINCE.md:375`), disposition **accepted-risk** — the residual
is knowingly retained, not routed out; `next` names the unfreeze condition.

### 3. R39-R3 — order class still absent (accepted-risk, blocked)

```
$ wc -l corpus/defects.jsonl
5 corpus/defects.jsonl
$ grep -c '"order' corpus/defects.jsonl
0        (exit 1)
```

The ledger is still the 5 R34 rows; the blocker named in the row (`plans/ledger_tip.py:6-7,72-73`,
`plans/round40_c1_verify.py:98`) is unchanged at e07f131. accepted-risk, `next` names the unfreeze condition.

### 4. R39-R4 — bundle still partly open, check refuses by design

```
$ python3 plans/mutant_direction_check.py --lane "$L" --counter "$L/plans/round39_c1_verify.py"
SETUP counter .../plans/round39_c1_verify.py is not a round-38-list counter: missing=battery38_fixtures,attributed non_6_tuple_rows=7; this check reads the round-38 MUTANTS rows (id, clause, dir, adv, old, new) and its battery38 loader only
rc=2
```

Item (a) is also still open: `git log -1 --format='%h' -- plans/order_check.py` → `34158b0` (the same commit the
note names). Legs (b) and (c) closed as the note records. accepted-risk; `next` asks the L1 to split (a) and (e)
into their own rows.

### 5. Frozen counter over the 71-row scratch ledger (clean clone @ e07f131)

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=9 incomplete=62
OWNERS attributed=9 unattributed=62
DISPOSITIONS set=9 bad=62
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=6 passed=6 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail          (196 DETAIL lines, all on rows 9..70 — other seats' scope)
```

No `DETAIL` line names R39-R1..R39-R5 or R40-R1..R40-R4 (`grep -E 'DETAIL .*(R39-R[1-5]|R40-R[1-4]) '` → empty):
the 9 rows are predicate-clean, including under `--run-checks` (6 ran, 6 passed, 0 failed).

### 6. Same 9 checks against the live lane (`LANE=/home/vgpnk/…/kengaku-shokunin`, cwd=counter scratch)

```
R39-R1  rc=0     R39-R5  rc=0     R40-R1  rc=0     R40-R2  rc=0     R40-R3  rc=0     R40-R4  rc=0
R39-R2  rc=1     R39-R3  rc=1     R39-R4  rc=2
```

## Why no row is routed (and why 9/9 are kengaku-owned)

Rows 1–9 are the residuals the round-39 and round-40 verifier spot-checks filed **against this lane's own
instruments** (`plans/*`, `SKILL.md`, `corpus/defects.jsonl`, `.ufo/waves/round-4*/`). The owner is the lane that
owns the fix surface, so all nine are `kengaku`. The two plausible cross-lane claims were checked and rejected on
sibling-declared scope, not on convenience:

- **R39-R5 → souji?** No. `souji-shokunin/PROVINCE.md:8,10-11` scopes souji to "the fleet root repo's hygiene
  surfaces: stray checkpoint/scratch files …" and per-lane "`.scratch/`, dead worktree metadata". The wave scratch
  root `/fast/scratch/hyaku/` is neither, and the residue was kengaku's own seat dirs.
- **R40-R2 → kumitate?** No, for the *remedy*. `kumitate-shokunin/PROVINCE.md:22` owns "seat-containment rules"
  (the rule), while the closed remedy for this finding is this lane's `.ufo/waves/round-41/build-spec.json:5` and
  this lane's crit modules. Named as adjacent evidence in the row, not absorbed: if the *rule* regresses, that
  row belongs to kumitate and would be `routed` with a `next`.

`routed`/`referral` are predicate-legal only with a non-`kengaku` owner plus `next`; inventing a sibling owner
for an in-lane surface would be exactly the misattribution the axis measures. Rows 10+ (R40-R5, R42-R*) are where
cross-lane owners first appear; they are outside my item.

## Limits and observations for the L1

- **Measured at the frozen commit, not the live tree.** The live lane was dirty and actively rewritten during the
  wave: `git status --porcelain` at 15:22 showed `M plans/round42_c1_verify.py`, `M plans/routed_open.py`,
  `M plans/scratch_guard.py`, and `plans/round42_c1_verify.py` was transiently **0 bytes** at 15:20 (a truncate-
  then-write window). One live-tree run of R40-R1 therefore returned rc=1; re-measured at e07f131 and in the live
  tree afterwards → rc=0. This is the round-50 D1 class recurring *inside* the wave; not my file, not my edit.
- **`--ledger` outside the lane crashes the counter.** `python3 plans/round51_routing.py --lane <lane> --ledger
  <path outside lane> --run-checks` raises `ValueError` in `ledger.relative_to(lane)` (`plans/round51_routing.py:77`)
  with a traceback instead of a usage message. Harmless for the frozen command, worth a line in the instrument's
  limits if the L1 touches it. Reported, not edited.
- **Check-quality caveat I did not fix**: the R39-R1/R40-R3/R40-R4 checks are greps for registry rows and receipt
  text — they re-derive that the declared artifact exists, not that the gate behaves. That is the frozen check
  text's claim, and I preserved its semantics rather than widening the claim.
- Dispositions are proposals with evidence; the L1 owns the ledger write and may downgrade any `fixed-verified`
  whose grep it judges too shallow (R39-R1, R40-R3, R40-R4 are the candidates).
- No tool was installed or upgraded for this seat (nothing was needed): no `pacman`, no `uv`, no binary drop.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C2ExecA` (clone + work dir + trial copy + `shokunin.conf` copy) was
  removed before yield; free space seen on `/fast` at start: `804G` total, `555G` avail (31% used).
- Evidence that must outlive the scratch is inlined above; no cited path is under `/tmp` or under scratch.

## Files written

- `.ufo/waves/round-51/w1/C2ExecA.jsonl` — 9 attributed rows (originals + `owner`, `disposition`, `next` on the
  three accepted-risk rows, `w1_check_note` recording each check rewrite).
- `.ufo/waves/round-51/w1/C2ExecA.md` — this report.

No production file, no commit, no git mutation anywhere; every git call in scratch used `git -C <scratch path>`
after `rev-parse --show-toplevel` printed that dir.

VERDICT: PASS — 9/9 rows attributed (`owner`, `disposition`), 9/9 checks lane-anchored and executed, 6/6
`fixed-verified` checks exit 0 under `--run-checks` in a clean clone at e07f131, 3 accepted-risk rows carry the
measured residual and an unfreeze `next`, no `DETAIL` line names my rows, no row deleted or added.
REV e07f131cf7037e58a21db6e1f3986cf401ad257c
