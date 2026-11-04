# ClaimFalsify70 — round 70 w1 falsification of R70-C1 and R70-C2

Seat: critic (leaf; no subagents, no ask, no mutations). Lane tip at first read: `384e9c76`; during the
review master advanced to `0ef40526` (A2) and the worktree gained A3/A4 (section below).
Claims doc read in full at `plans/round-70-claims.md` (worktree copy; A1 at first read, A2–A4 arrived
during the review — section below).
Scratch: `/fast/scratch/hyaku/kengaku-r70/ClaimFalsify70` (`S`). Two read-only clones: `S/base` at
`502893ad`, `S/r69` at `4038bb11`. No tool installs (curl/python3/git only). Writes: this file and its
evidence dir only; `S` was removed after copying.

## Axes

- A1 C1 predicate strength / do-nothing reachability
- A2 C1 class-row rule (`executed 3 of 8`)
- A3 C1 counting command and whether any instrument guards it
- A4 C1 table / digests / selftest (positive control)
- A5 C2 E-check satisfiability by prose alone
- A6 C2 E1 arithmetic and the frozen-vs-amended instrument
- A7 C2 E6 receipt provenance re-derivability
- A8 C2 E7 reject reality
- A9 C2 E3/E4 clause liveness and the S243 quote anchor

## Verdicts (per claim)

**R70-C1 — reachable.** The frozen predicate is true on the receipt of record — v2 under A2
(PROBE `9c9effeb…`), with v1 (`9aef6d33…`) preserved and also passing — and I reproduced every
sub-clause independently (table, seven staged digests, leg coverage, selftest arms). **Strongest
surviving objection:** the predicate is a *receipt* predicate, not an observation predicate. A receipt
never produced by a run — with self-contradictory live-witness fields — passes `--check-receipt` with
rc 0. The do-nothing control only discriminates the base tree (no receipt) from a tree with a receipt;
it does not discriminate a replay from a transcription. Separately, the class-row target
(`executed 3 of 8`) is not derivable from the row's stated derivation rule and is guarded by no
instrument.

**R70-C2 — reachable on the real lane, not reachable as worded.** The repaired gate prints
`DEFECTS n=0` / `PREDICATE R70-C2 pass` on the real lane, and the red-before reproduces `n=8` at
`502893ad`. But the claim's warrant — "each defect is closed by a dated correction that the gate
re-derives as E1–E8" — fails: six of eight checks are token-presence over prose, and E1/E2 re-derive
only from files the writer supplies. A wholly fabricated lane (synthetic E1 pair, 3-line entry,
fabricated registry rows, 4-line E6 receipt, one-line lesson, `printf 0` rc) prints `DEFECTS n=0` with
rc 0. Two concrete defects were live at measurement: E3/E4's `used-by` clauses were dead code, and
S243 quoted `test_outputs.py:59` while the quoted statement is at `:61`. Both were edited in the
worktree at 21:54–21:55 (gate hash `367ce58e`, S243 `:61`) and are dated in Amendment A4, credited to
this seat; the fabricated-lane counterexample still passes on the edited gate (below).

## What I ran (command, rc)

```
git -C L rev-parse master                                   -> 384e9c76415e78093623b3eaff262423a89dbc3e
git cat-file -e 502893ad:corpus/evidence/round70/nginx/receipt.txt  -> rc 128 (absent)
git -C L show 502893ad:SKILL.md | grep -c 'executed 2 of 8' -> 1
git -C L show 502893ad:SKILL.md | grep -c 'executed 3 of 8' -> 0
git -C L show 502893ad:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S242[[:space:]]*\|' -> 0
python3 plans/round70_c1_nginx_probe.py --check-receipt corpus/evidence/round70/nginx/receipt.txt -> rc 0
python3 plans/round70_c1_nginx_probe.py --check-receipt S/forged-plausible.txt     -> rc 0  PASS
python3 plans/round70_c1_nginx_probe.py --check-receipt S/forged-contradictory.txt -> rc 0  PASS
python3 plans/round70_c1_nginx_probe.py --render-table                     -> matches frozen table
python3 plans/round70_c1_nginx_probe.py --render-table --stage-sha S/stage -> 7/7 CASE-SHA match, distinct
python3 plans/round70_c1_nginx_probe.py --selftest --work S/selftest       -> rc 0 (7/7 red, accept, path, byte)
python3 plans/round63_gate_checks.py depth --skill S/SKILL-pre.md --receipt corpus/evidence/round62/class-survey.txt --root . -> 33/33 rc 0
python3 plans/round63_gate_checks.py depth --skill SKILL.md       --receipt corpus/evidence/round62/class-survey.txt --root . -> 34/34 rc 0
python3 S/gate-frozen.py   --root S/base        -> DEFECTS n=8 / PREDICATE R70-C2 fail / rc 1
python3 plans/round70_c2_routed_defects.py --root .            -> DEFECTS n=0 / PREDICATE R70-C2 pass / rc 0
python3 plans/round70_c2_routed_defects.py --root S/fake-lane  -> DEFECTS n=0 / PREDICATE R70-C2 pass / rc 0
python3 plans/round70_c2_routed_defects.py --root S/fake-lane  (re-run, worktree 367ce58e after the used-by fix) -> n=0 rc 0
python3 S/gate-frozen.py   --root .            -> E1 defect depth-gate-identity problems=['change-wider-than-counts','recorded-pair']
python3 plans/round70_c2_routed_defects.py --selftest --work S/c2st -> SELFTEST defects-in-fake=8 all-fail=True e2-byte-flip-red=True rc 0
python3 plans/round70_c2_routed_defects.py --mutants  --work S/c2mut -> MUTANTS total=8 killed=8 rc 0
git -C S/r69 checkout 4038bb11; python3 plans/round69_c2_routed_defects.py -> rc 0, block identical to E6 receipt
curl https://raw.githubusercontent.com/.../2fd12b88.../nginx-request-logging/instruction.md -> HTTP 200, 1882 B, 24 lines
```

## Live amendments observed after the freeze read (A2–A4)

The lane advanced while this review ran. The facts, re-derived from the repo:

- **A2 (`0ef40526`, committer 2026-11-03 21:52:53; author date is the freeze committer time
  21:45:23, so the committer date is the honest order).** It adds the A1+A2 text to
  `plans/round-70-claims.md` and changes the C1 probe from `9aef6d33…` to `9c9effeb…` (three
  duplicate-line defects: `duplicate-case`, `duplicate-vector`, `duplicate-test`). The v1 receipt
  (`corpus/evidence/round70/nginx/receipt-v1-pre-a2.txt`, PROBE `9aef6d33…`, 21:47:06) is preserved;
  v2 (`receipt.txt`, 21:53:27) differs only in the PROBE/PROBE_BLOB lines and the `server_pid` values
  (`diff -u` of the two is exactly those lines; every CASE sha and every VECTOR is identical).
  `--check-receipt` passes on both (`check-v1.txt`, `check.txt`), and the selftest now also accepts
  the green receipt (`green_ok=1`).
- **The freeze claims blob had no A1 section** (`git show 384e9c76:plans/round-70-claims.md` is 157
  lines; the only "Amendment A1" there is the round-69 reference at line 28). A1's text landed in
  `0ef40526`, after the first C1 receipt; the C2 repair it describes is still **worktree-only**
  (master's C2 gate blob is `acc6a9e9…` = the frozen inverted gate; the repaired file is
  `367ce58e…`, uncommitted at this check).
- **A3** narrows the claims doc's "`--render-table` must byte-equal it" wording, which is right:
  `--render-table` prints the instrument's `note` column, so the rendered block is not byte-equal to
  the claims doc's table (the vector line and case set are equal; I verified those).
- **A4** dates the two defects this seat found (E3/E4 `used-by` dead clause; S243 `:59` → `:61`) and
  credits `ClaimFalsify70`; `corpus/evidence/round70/c2/a4-usedby-arm.txt` shows both clauses now
  fire when the cell is blanked. The repaired C2 gate is still uncommitted at this check, so the
  landing must commit `plans/round70_c2_routed_defects.py` at `367ce58e…` (or the landing gate is not
  the instrument that produced the green run).

### A2 does not close the forged-receipt counterexample

Rebuilt the contradictory receipt with A2's probe sha (no duplicate lines, so none of A2's three new
defects fire): `forged-contradictory-v2.txt` still passes.

```
$ python3 plans/round70_c1_nginx_probe.py --check-receipt .ufo/waves/round-70/w1/ClaimFalsify70/forged-contradictory-v2.txt
CHECK ok cases=7 legs=8 seen_p=8 seen_f=8
CHECK stored-predicate=pass derived=pass
PREDICATE R70-C1 pass        (rc 0)
```

So the duplicate-line strictness (A2) is a real repair of a different forgery class, but the
`server_pid`/`sandbox_rc`/capture gap in Counterexample 1 is untouched.

## C1 — evidence

### Positive re-derivations (the claim is true on the receipt of record and the committed table)

- Receipt: `--check-receipt` prints `CHECK ok cases=7 legs=8 seen_p=8 seen_f=8`,
  `CHECK stored-predicate=pass derived=pass`, `PREDICATE R70-C1 pass`, rc 0 — on v2 and on the
  preserved v1 (`check-v1.txt`); the two receipts differ only in the PROBE/PROBE_BLOB lines and the
  `server_pid` values, so the A2 re-run is honest and the staged digests are stable.
- Per-leg observed counts parsed directly from the receipt's `TEST` lines:
  `installed 6P/1F, running 6P/1F, index 5P/2F, custom_404 5P/2F, config_syntax 6P/1F,
  config_settings 6P/1F, log_creation 5P/2F, log_format 5P/2F` — exactly the claims doc's
  freeze-time arithmetic, and it is *observed* (not the `--render-table` recount).
- `--render-table` prints `FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP/PFFFPPFF/PPPFPPPP`,
  `LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8`; `--stage-sha` reproduces all seven `CASE_SHA`
  values, 7 distinct.
- `--selftest`: `RED r1..r7 refused=True`, `ACCEPT synthetic accepted=True`,
  `PATH-INDEPENDENT sha_equal=True`, `STAGED-STATE changes_on_byte=True`, rc 0.
- Grader sha: `sha256sum corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`
  = `045cc716…acda0` = `corpus/evidence/round52/graders/SHA256SUMS:111`; 5947 bytes.
- The sandbox captures are genuine-looking live witnesses: e.g.
  `corpus/evidence/round70/nginx/sandbox/K6-sandbox.txt` carries raw grader lines with timings
  (`TEST test_nginx_running F 4003ms Nginx is not running on port 8080`) and the four
  `E:ConnectionError` legs. **But `check_receipt` never opens them** (`grep -n evidence_dir` →
  only `run_battery` at `plans/round70_c1_nginx_probe.py:501,530,885,911`). The predicate does not
  require the artifact its own named limitation calls the live witness.

### Counterexample 1 — a fabricated receipt passes the counter

Built `forged-contradictory.txt` (frozen probe `9aef6d33…`) and, after A2, `forged-contradictory-v2.txt`
(probe `9c9effeb…`) from the frozen `CASES`/`CASE_SHA` without running anything, with impossible live
fields: `K1 server_pid=None` (K1 is a server case), `K6 server_pid=777777` (K6 stages no service; the
real receipt has `server_pid=None`), `K2 sandbox_rc=137`. Each version passes on its own probe; the v2
run:

```
$ python3 plans/round70_c1_nginx_probe.py --check-receipt .ufo/waves/round-70/w1/ClaimFalsify70/forged-contradictory-v2.txt
CHECK ok cases=7 legs=8 seen_p=8 seen_f=8
CHECK stored-predicate=pass derived=pass
PREDICATE R70-C1 pass        (rc 0)
```

Cause: `check_receipt` parses the `CASE` line only for `case_sha256=`
(`plans/round70_c1_nginx_probe.py:661`: `if len(parts) != 5 or not parts[2].startswith("case_sha256=")`).
`server_pid` appears only where it is written (`:497`, `:535`, `:551`) and in the selftest fixtures
(`:751`, `:803`); it is never read or validated. `sandbox_rc` is likewise unvalidated. The receipt's
`PROBE`/`PROBE_BLOB`/`GRADER` shas are readable from the same committed bytes, so they do not
distinguish a runner from a transcriber.

The claims doc's limitation (i) names "cannot prove a live run", but the *frozen predicate* is exactly
`--check-receipt` rc 0, so the limitation is the predicate. The "Do-nothing control" sentence — "A
round that does nothing cannot reach the target" — is true only for "writes no receipt". A round that
lands no measurement and one file reaches the C1 predicate.

### Counterexample 2 — the class row's rule and its missing guard

Row (SKILL.md:78, as I read it before the 21:48:44 edit): `| network-service | 8 | executed 2 of 8 (...) |`
with the parenthetical "round 69 `nginx-request-logging` replayed offline — five frozen vectors,
40/40 legs, but R69-C1 MISS on its leg-coverage clause, so the member is not counted". The target is
`executed 3 of 8`; the row now reads `executed 3 of 8 (… so the member is counted from round 70 …)`
with the same parenthetical rule.

The row's own stated derivation (SKILL.md:62): "the executed column is derived from
`corpus/evidence/round52/graders/executed17.lst` (a class is `executed` when at least one of its
members is on that list)." Against that rule:

```
$ grep -nE 'nginx-request-logging|kv-store-grpc|pypi-server' corpus/evidence/round52/graders/executed17.lst
(no match, rc 1)
$ grep -n 'CLASS network-service' corpus/evidence/round62/class-survey.txt
11:CLASS network-service count=8 members=filter-js-from-html,git-multibranch,headless-terminal,
   hf-model-inference,install-windows-3.11,kv-store-grpc,nginx-request-logging,pypi-server
21:EXECUTED-COVERAGE ... classes-uncovered=network-service,process-environment,db-state,container-image
```

So under the row's stated rule the class is **not** executed at all; `executed 3 of 8` follows only
from the parenthetical's *unstated* second rule (members replayed offline whose frozen predicate
passed). The count 2 is right under that second rule (round 64 `PREDICATE R64-C1 pass` at
`corpus/evidence/round64/kvstore-probe.txt:66`; round 68 `PREDICATE R68-C1 pass` at
`corpus/evidence/round68/pypi/receipt.txt:12`), and 2+1=3 is right after R70-C1 — but the row carries
two incompatible authorities for one cell and the claim chooses the one that makes 3 follow.

No instrument guards the cell. `round63_gate_checks.py depth` checks the `count` cell, the cell shape
and the pointer cell, never the `executed` cell (`depth_measure`, `plans/round63_gate_checks.py:236-330`); `grep -rln "executed 3 of 8"
--include='*.py' .` returns nothing; the C1 probe never reads SKILL.md
(`grep -n SKILL plans/round70_c1_nginx_probe.py` → no match). Precedent for a gate exists:
`plans/round68_c2_correction_gate.py:160` asserts `"executed 2 of 3" in sec` for its own class row.
During this review the row moved: `grep -c 'executed 3 of 8' SKILL.md` was 0 when I first read the
worktree and 1 after SKILL.md's 21:48:44 edit (the current row carries the new round-70 narrative).
Nothing but the claims doc's manual grep (and, at close, a reader) notices whether a landing skipped
it; no instrument reads the cell.

## C2 — evidence

### The red-before is honest

`python3 S/gate-frozen.py --root S/base` (base clone at `502893ad`) prints E1–E8 defect and
`DEFECTS n=8` / `PREDICATE R70-C2 fail`, rc 1 — byte-for-byte the same class of output as
`.ufo/waves/round-70/c2-red-before.txt`, including the same per-check detail strings. The do-nothing
control for C2 holds.

### Counterexample — a fabricated lane passes all eight checks

I built `S/fake-lane` with no real correction of any kind:

- E1: two synthetic one-line captures differing only in `total=33/34` and `resolved=33/34`, plus a
  provenance whose `SHA` lines I computed from those fabricated files and a `LINE-DIFF` naming them.
- E2: a three-line entry (`source: S242 fabricated instruction.md:6-11,15-18`,
  `verified-at:`, `recheck:`) and the real `plans/round63_gate_checks.py`; the receipt is the fresh
  `TRIO pass …` line (64 bytes).
- E3: a fabricated S242 row containing the hard-coded `26a7ac98…9edf99`; its `used-by` cell (index 10)
  is the entry path.
- E4: a fabricated S243 row containing `supersedes S241 —`, `leg 5`, `nginx -t`; `used-by` the entry
  path. (In the first run, against the A1-repaired snapshot `011b5d13`, both rows had `used-by` `—`
  and the gate still passed — the dead-clause finding below. The rebuilt rows satisfy the 21:55:06
  check and the gate still prints `DEFECTS n=0`.)
- E5: a minimal five-line README with the two needles.
- E6: a four-line file `REV 4038bb11 / DEFECTS n=0 / PREDICATE R69-C2 pass / RC 0` — no clone, no run.
- E7: a one-line `## Gate` with "rejected: reason …" and a fabricated S244 row with `| rejected |`
  and `merge/kengaku`.
- E8: `printf '0\n' > w1-validate.rc`, `echo 'this is not a validator log' > w1-validate.out`, empty
  stderr.

```
$ python3 plans/round70_c2_routed_defects.py --root S/fake-lane
E1 ok depth-gate-identity line-changes=1 problems=[]
E2 ok trio-receipt trio bytes=64
E3 ok instruction-row problems=[]
E4 ok s241-correction problems=[]
E5 ok corpus-index problems=[]
E6 ok r69-landing-receipt problems=[]
E7 ok gate-reject problems=[]
E8 ok wave-validation problems=[]
DEFECTS n=0
PREDICATE R70-C2 pass        (rc 0)
```

This is not an artifact of Amendment A1 or of the 21:55:06 used-by fix: the freeze-commit gate fails
only E1 on this same lane (its inverted tuple, below) and passes E2–E8, and the current worktree gate
(`sha256 367ce58e…`) prints the same `n=0` once the fabricated rows cite the entry in `used-by`. So six
checks are pure token presence
(`plans/round70_c2_routed_defects.py:187-222` E3, `:224-245` E4, `:247-260` E5, `:262-276` E6,
`:278-306` E7, `:308-323` E8); E1 (`:122-171`) re-derives sha256 only of the files it is handed, and
E2 (`:173-185`) compares bytes to a fresh run of a three-key format gate.

The `--selftest` / `--mutants` tallies reproduce (`defects-in-fake=8`, `e2-byte-flip-red=True`,
`MUTANTS total=8 killed=8`), but both operate on a fake built by *stripping tokens* and by *deleting
whole checks*; neither tests a forged-but-present correction. The kill rule's "a correction that
exists only as prose with no re-deriving check is not a closed defect" is therefore not enforced for
D3–D8.

### E1 arithmetic and the frozen instrument (A6)

The arithmetic is honest and independently re-derivable:

```
$ git show 4038bb11^:SKILL.md > S/SKILL-pre.md
$ python3 plans/round63_gate_checks.py depth --skill S/SKILL-pre.md --receipt corpus/evidence/round62/class-survey.txt --root .
ROWS n=16 class_match=True count_mismatch=0 paths total=33 resolved=33 share=1.00
$ python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .
ROWS n=16 class_match=True count_mismatch=0 paths total=34 resolved=34 share=1.00
```

`git diff 4038bb11^ 4038bb11 -- SKILL.md` shows the network-service row is the class-table change in
that commit (the other hunk is four gate-registry rows outside the depth section). So one added
pointer produces 33→34, and the provenance shas match the files
(`f683297c…` wave, `d65bbda…` corpus). Two wording imprecisions: the claims doc says "only delta is
the class-row pointer (paths total 33 → 34)" while the capture lines also change `resolved=33 → 34`,
and the pointer itself is not in the capture bytes at all — the depth-gate line is a summary, so the
added token is inferred from the SKILL diff and the provenance's `ADDED-TOKEN` line. E1 only checks
that the nginx path appears *somewhere* in the provenance text
(`plans/round70_c2_routed_defects.py:167`); it never parses `ADDED-TOKEN`.

The freeze-commit instrument is inverted and cannot pass the landing E1:

```
$ python3 S/gate-frozen.py --root .        # git show master:plans/round70_c2_routed_defects.py
E1 defect depth-gate-identity line-changes=1 problems=['change-wider-than-counts','recorded-pair']
```

Cause: `git show master:plans/round70_c2_routed_defects.py | sed -n '152p'` is
`diff = [(i, x, y) for i, (x, y) in enumerate(zip(la, lb)) if x != y]`, i.e. it normalises the
*corpus* line's counts against the *wave* line and then compares to the corpus line; no provenance
ordering can satisfy it for this pair. Amendment A1's one-line swap (`diff = [(i, y, x) …]`) is
necessary, not cosmetic. A1's ordering claim ("before any receipt was scored; the wave had not
dispatched") checks out by mtime: gate repair 21:45:51, `w1.ready.dispatched` 21:46:23, first receipt
21:47:06 (freeze commit 21:45:23). But A1's *text* is also post-freeze: the freeze claims blob is 157
lines and has no A1 section (line 28 only cites round-69's A1 item 3); the A1 and A2 text landed
together in `0ef40526` (committer 21:52:53), after the first C1 receipt. The repair mtime is
pre-dispatch, so A1's clause is true of the repair itself, not of the amendment's publication. At this
check master's C2 gate is still the frozen inverted blob (`acc6a9e9…`); only the worktree has the
repair. The residual issue is provenance of the *green* run: the C2 landing receipt/stdout does not
record the amended gate's blob sha, so a reader re-deriving from the frozen commit gets `E1 defect`,
while the green run came from an uncommitted-at-the-time file.

### E6 — re-derivable (A7)

I re-derived it exactly as the receipt says:

```
$ git clone --shared L S/r69 && git -C S/r69 checkout 4038bb11   # HEAD 4038bb11
$ cd S/r69 && python3 plans/round69_c2_routed_defects.py
E1 ok rows=4/4 missing=[] thin=[]
E2 ok headings=1 q50=True round68-lesson=True spotcheck=True
...
DEFECTS n=0
PREDICATE R69-C2 pass        (rc 0)
```

Identical to `corpus/evidence/round70/gates/r69-c2-landing.txt`, which records the command, the full
rev, the clone provenance, the output block, `RC 0` and the date. A reader can re-derive this one.
The gate's E6 check, however, is four substring needles (`:262-276`) — my four-line fabricated file
passed it. Honest receipt, weak check.

### E7 — the reject is real (A8)

- Candidate: `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/grader-fixture-coverage.md`
  exists (2869 bytes); its first line is
  `source: S155 — \`lanes/kengaku/round8/toolathlon-grader-fixture-probe2.md\` — …`.
- The cited probe transcript is **not in this lane**: `git -C L ls-files | grep -c toolathlon-grader-fixture-probe2`
  → 0; `corpus/knowledge/grader-fixture-coverage.md` does not exist here.
- `corpus/SOURCES.md:259` keeps S244 with `status` = `rejected`, `used-by` = `—`, and the reason
  "its tier-A own-work claim rests on a probe transcript whose bytes are not in this lane, so Q1/Q2
  cannot be satisfied; flip: the probe artefact lands in this lane and re-runs".
- The lesson's `## Gate` states the reject with the same reason and the flip.

Caveat: the reason's clause "cites S155, a campaign staging transcript" is registry-relative; in *this*
lane `S155` is `Terminal-Bench 2.0 password-recovery solution/solve.sh` (`corpus/SOURCES.md:170`).
The decisive clause (probe bytes not in this lane) is verifiable; the S155 phrasing is not. The E7
check (`:278-306`) accepts the tokens `| rejected |` + `merge/kengaku` from my fabricated row, so it
cannot distinguish this real refuse from a manufactured one.

### E3/E4 — dead `used-by` clause (A9)

Found live at 21:51–21:54 in the freeze-commit gate and in the A1-repaired snapshot `011b5d13`:
registry rows have **11** cells (header at `corpus/SOURCES.md:21`; measured
`cells(registry_row(...,'S242')) = 11`, `used-by` at index 10), but both checks used
`if len(c) > 11 and NGINX_ENTRY not in c[11]:` (`plans/round70_c2_routed_defects.py:217` E3,
`:240` E4) — always False. My first fabricated lane put `—` in `used-by` and E3/E4 still passed, so
the claims doc's "the entry in `used-by`" was unenforced. At 21:55:06 the worktree was changed to
`if len(c) != 11 or NGINX_ENTRY not in c[10]:` (worktree hash `367ce58e…`); S242/S243 both carry the
entry at cell 10, so the real lane stays green and the clause is now live. Amendment A4 now dates this
fix (and credits this seat); `corpus/evidence/round70/c2/a4-usedby-arm.txt` shows both clauses fail
when the cell is blanked. The repaired gate (`367ce58e…`) is still uncommitted at this check —
master's C2 blob is `acc6a9e9…`, the frozen inverted gate — so the landing must commit it, or the
landing gate is not the instrument that produced the green run.

### S243 — false quote anchor (A9)

Found live at 21:51–21:54: `corpus/SOURCES.md:258` (S243) said
`tests/test_outputs.py:59 fetched 2026-11-03, sha256 045cc716…; verbatim: result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)`.
The quoted statement is at **line 61** of the pinned file; line 59 is `def test_nginx_config_syntax():`.
`corpus/lessons/round-70.md` repeated "Located quote, line 59". The round-69 routing text got it
right (`corpus/lessons/round-69-verifier-spotcheck.md` D4: "`test_outputs.py:61`"). By 21:55:06 the
SOURCES row read `:61` and the lesson no longer carried `:59`; the defect is closed in the worktree
and dated in Amendment A4, but E4 still checks only `supersedes S241`, `leg 5`, `nginx -t`
(`:224-245`) and cannot catch a false anchor. The durable objection is the check's inability to
validate the quote's location, not the (fixed) digit.

### E8 — satisfies on `printf` (A5)

`check_wave_validation` (`:308-323`) requires `w1-validate.rc` == `"0"`, a non-empty
`w1-validate.out`, and the existence of `w1-validate.stderr`. All three are writable by any seat; my
fake lane's `"this is not a validator log"` passed. In the real lane the files are committed at the
freeze and `w1-validate.out` is byte-identical to `w1-dispatch.json` (`cmp -s` rc 0), with empty
stderr and no recorded command or validator identity. D8's original complaint was that "validated
cleanly (rc 0) is inferred from an empty stderr"; the fix adds an rc and an output but still records
no *what* ran, and the out is the dispatch payload.

## Impacted axes and smallest safe corrections

1. **C1 coverage axis (A1/A4).** Predicate strength, not truth. Smallest correction: in
   `check_receipt` (a) validate each `CASE` line's `server_pid` against the case's `server` flag
   (`None` iff `server: False`, positive int otherwise) and require `sandbox_rc == 0`; (b) require the
   seven `K*-sandbox.txt` captures beside the receipt and re-derive each `TEST` line from the
   capture's `--- stdout` block. This kills the contradictory-receipt counterexample and binds the
   named live witness; it still cannot prove a run, so the claim's limitation (i) remains and should
   bound the predicate's wording ("receipt-and-capture consistent", not "replayed").
2. **C1 class row (A2/A3).** Smallest correction: either state the replay-count rule in the row's
   preamble or drop the `executed` label against `class-survey.txt:21`; and add a gate assertion on
   the cell (round 68's `plans/round68_c2_correction_gate.py:160` is the pattern), or remove the
   bullet from the target. The row moved during this review; no instrument reads it.
3. **C2 calibration axis (A5).** Six checks are presence checks. Smallest corrections that make the
   wording true without changing the frozen predicate: (a) E3 should fetch/receipt the instruction
   bytes and compare the sha to a committed receipt rather than the constant
   (I verified the constant live: HTTP 200, 1882 B, 24 lines, sha
   `26a7ac98…9edf99`, line 16 body and line 18 404 literal as quoted); (b) E6 should execute the
   clone+checkout+run it already documents and compare the block (I did: identical); (c) E8 should
   record the validator command and a sha of its output, or re-run the validator. E4/E7 cannot be
   fully byte-derived (they are judgments), so the claim should say "E1–E2 re-derive; E3–E8 assert a
   dated correction's content", not "the gate re-derives as E1–E8".
4. **E3/E4 dead clause (A9).** The worktree already has the correct form
   (`len(c) != 11 or NGINX_ENTRY not in c[10]`); A4 dates it. Keep it and commit the repaired gate.
   If the landing is meant to be the frozen gate, revert instead.
5. **S243 anchor (A9).** Already `:61` in SOURCES and the lesson no longer says `:59`; keep those, and
   consider making E4 parse the anchor's line number against a committed quote receipt, since even a
   wrong digit passes today.
6. **C2 green-run provenance (A6).** Record the repaired gate's blob sha (`367ce58e…`) in the C2 green
   receipt, as C1 does with `PROBE_BLOB`, and commit that file: master's blob is still the frozen
   inverted gate (`acc6a9e9…`), so `git show master:plans/round70_c2_routed_defects.py` re-derives
   `E1 defect`, not green. Date the A1/A2/A4 texts' order by committer time; the L1's author dates
   are fixed at the freeze time.

## Notes / limits of this review

- I did not run the C1 battery (owned by `NginxBatteryR70` / `BatteryReplicate` / `LegWitnessProof`);
  my C1 positive checks are receipt/table/digest/selftest re-derivations plus the committed captures'
  content. I did not judge, admit, edit or integrate anything; the only lane paths I wrote are this
  report and its evidence copies, and no commit/push/jj mutation was made.
- The review ran against a moving lane: master advanced to `0ef40526` (A2) and the claims doc gained
  A3/A4 while I measured. Every state claim above is timestamped; the last live check was at 21:56,
  when the A2 v2 receipt passed, the repaired C2 gate (uncommitted) passed on the real lane and on
  the fabricated lane, and the frozen C2 gate still failed E1 on the real lane.
- Clones are `--shared` local clones in `S`; no commits were made in them. `S` was removed after the
  evidence copies below were made.
- Evidence copies: `.ufo/waves/round-70/w1/ClaimFalsify70/` — `forged-plausible.txt`,
  `forged-contradictory.txt` (v1, frozen probe), `forged-contradictory-v2.txt` (A2 probe),
  `fake-lane/` (the fabricated lane), `c2-fake-pass.out`, `c2-real-pass.out`,
  `c2-frozen-on-real.out`, `c2-frozen-on-base.out`, `frozen-on-fake.out`, `r69-gate.out`,
  `depth-pre.out`, `depth-current.out`, `gate-worktree-367ce58e.py`,
  `gate-snapshot-011b5d13.py`, `gate-frozen-384e9c76.py`.
