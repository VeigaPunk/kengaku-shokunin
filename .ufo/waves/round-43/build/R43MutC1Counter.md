# R43MutC1Counter — mutation test of the round-43 C1 counter (`plans/round43_c1_verify.py`)

Seat: R43MutC1Counter (leaf, no subagents). Round 43 wave 1, 2026-10-26.
Target: single-line mutants of the C1 counter's guards, run against the committed controls
(`.ufo/waves/round-43/claims/c1_controls.sh` + `control-c1-*.txt` + `hostile/*.py`), reproduced on my clone.
The frozen lane file was never modified: every mutant is a scratch copy
(`/fast/scratch/hyaku/kengaku-r43/R43MutC1Counter/mut/<id>.py`, generator `gen_mutants.py`, sha256 recorded per run).

## Method

- Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane`;
  `git -C $S/lane rev-parse --show-toplevel` = `$S/lane`; clone HEAD `d33350fdb01ce27cbff47b04642fd2c1471e5c26`.
  Counter digest in the clone `1a1cd1f886fd4581170f83dc4a5293276fd9b981f9a6f1235d121b0cc97d6cca` =
  `claims/frozen-digests.txt` line for `plans/round43_c1_verify.py`; both tools match their PINS
  (`11bb2cad…`, `948d5e1d…`). So the clone's counter is byte-identical to the frozen one.
- Detector = the committed controls, re-run by `driver.sh` (a faithful re-spelling of `c1_controls.sh`):
  witness run, do-nothing, witness-as-battery, no-mutants, span={1} (leg f), SITE_EQUAL→True (leg g),
  tool-edited, relative-`../` argv escape, NA7 direction mislabel, and hostile h1–h6 (round-43 halves;
  the round-42 "vector open" halves are not re-run per mutant — they do not run the counter under test;
  the frozen `control-c1-hostile-*.txt` receipts carry them, and my baseline reproduces their round-43 halves).
  Every control invocation runs inside `claims/envelope.sh` (pasted per result below); outputs land in
  `$S/out-<mutant>/<control>.txt`, and `compare.sh` diffs each against the pristine baseline with the
  `ENVELOPE` timestamp lines stripped.
- Caught = at least one control's observable output changes against the pristine baseline (a should-fail
  control flipping to pass, a refusal line appearing/disappearing, or a count/label line changing).
  Survived = no control's output changes → coverage finding, drafted control below. Inconclusive = the
  control's own patch anchor no longer matches the mutated counter (patch assert fails).
- Baseline (pristine counter, my reproduction) matches every frozen receipt I compared:
  `witness` rc=0 (`killed=9 … value=differs` ×9), `nothing` rc=1 (`survived=9`), `wab` rc=0 (`PREDICATE C1
  pass`), `nomut` rc=1, `span` rc=1 (`unattributed=9`, `last=span-not-run`), `value` rc=1 (`unattributed=9`,
  `last=site-record-equal`), `edited` rc=1, `escape` rc=2, `mislabel` rc=1, `h1` rc=1 (fixture `ok`,
  `sidechannel=1`), `h2` rc=1 (`CLEAN-3908b`), `h3` rc=1 (`ERR30`), `h4` rc=2 (`escapes its directory:
  lane/rev-parse --show-toplevel=…`), `h5` rc=2 (`symlink repo/corpus/SOURCES.md -> …`), `h6` rc=2
  (`--receipt … is a tree at HEAD, not a blob`).

## Mutants (single line each; `old` → `new` on the counter copy)

| id | guard (counter line) | mutant |
|---|---|---|
| M01 | L137 `SITE_EQUAL` | `return tuple(mut_sites) == tuple(ref_sites)` → `return True` |
| M02 | L815 reference trace 1 | the traced reference run → `r_sites = 0, frozenset(), frozenset(), ()` (run dropped) |
| M03 | L816 reference trace 2 | `r_sites2 = runner.run(...)` → `r_sites2 = r_sites` (stability check self-comparison) |
| M04 | L787 newline-count validity | `or old.count("\n") != new.count("\n") \` → `or False \` |
| M05 | L500 `symlink_breach` | `if p.is_symlink() and not p.resolve().is_relative_to(d):` → `if False:` |
| M06 | L525 `order_argv_breach` | `if r.returncode == 0 and r.stdout.strip() != "blob":` → `if False:` |
| M07 | L483 `repo_breach` toplevel branch | `if pathlib.Path(seen).resolve() != repo:` → `if False:` |
| M08 | L488 `repo_breach` worktree branch | `if val:` → `if False:` |
| M09 | L627 `exhibits` silence conjunct | drop `cls in set(fx["defects"])` |
| M10 | L860 floors | `sum(FLOORS.values()) == TOTAL` → `True` |
| M11 | L835 unattributed accounting | `unattributed += 1` → `survived += 1` |
| M12 | L387 fingerprint content term | `content = file_sha256(p)` → `content = ""` |
| M13 | L652 sidechannel scan | `if hits:` → `if False:` |
| M14 | L854 PINS-AFTER | `after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]` → `after = []` |
| M15 | L770 null run | `if res != ref[fx["fid"]]:` → `if False:` |

## Results

Detector = the 15 reproduced controls; every control file carries its own ENVELOPE lines (examples pasted
below; full files copied into `build/R43MutC1Counter/receipts/`). "caught" = ≥1 control's output changes
vs the pristine baseline (random `k43-c1-*` scratch names normalised).

| id | guard | verdict | caught by (observed change) |
|---|---|---|---|
| M01 | SITE_EQUAL (L137) | **caught** | `witness`/`wab`/`edited`: all kills → `UNATTRIBUTED … last=site-record-equal`, `killed=9→0`; `value` control inconclusive (its patch anchor IS this line) |
| M02 | reference trace 1 (L815) | **caught** | `witness`/`wab`/`edited`: kills → `UNATTRIBUTED … last=site-record-unstable` (empty first record vs real second record trips the stability check); `value`: `last=site-record-equal` → `site-record-unstable` |
| M03 | reference trace 2 (L816) | **survived** | no control changes (records stable; see draft d03) |
| M04 | newline-count validity (L787) | **survived** | no control changes (no table row has unequal newline counts; see draft d04) |
| M05 | `symlink_breach` (L500) | **caught** | `h5`: refusal gone — `FIXTURE h5-row-source-outside … ok` (the outside row source is read) |
| M06 | `order_argv_breach` (L525) | **caught** | `h6`: refusal gone — `FIXTURE h6-receipt-is-directory … ok` (the directory substitute is admitted) |
| M07 | `repo_breach` toplevel branch (L483) | **caught (message-level)** | `h4`: refusal line changes `rev-parse --show-toplevel=…` → `core.worktree=…` — the fixture is still refused via the worktree branch; no committed control exercises the toplevel branch alone |
| M08 | `repo_breach` worktree branch (L488) | **survived** | no control changes — `h4` still refused via the toplevel branch (see draft d08) |
| M09 | `exhibits` defects conjunct (L627) | **survived** | no control changes (see draft d09) |
| M10 | floors `sum(FLOORS)==TOTAL` (L860) | **survived (equivalent-in-context)** | no control changes — `wab` still `PREDICATE C1 pass`: within `good`, `sum(FLOORS)==TOTAL` is implied by `per_tool==[FLOORS,FLOORS]` (table counts match FLOORS) together with `len(MUTANTS)==TOTAL`; no control can isolate the term (see draft d10) |
| M11 | `unattributed += 1` (L835) | **caught** | `span`/`value`: `unattributed=9` → `survived=9 unattributed=0` |
| M12 | fingerprint content term (L387) | **survived** | no control changes — no run can tamper a fixture (dirs are read-bound during every tool run); see draft d12 |
| M13 | sidechannel scan (L652) | **caught** | `h1` + `h4`: the `SIDECHANNEL … tokens=…` line and the `sidechannel=1` count disappear (h1's module mentions `ppid,chmod`, h4's mentions `core.`); dedicated draft d13 shows it on a comment-only token |
| M14 | PINS-AFTER (L854) | **caught** | `edited`: the tool is edited before the run and stays edited — `PINS-AFTER mismatched=1` → `mismatched=0`; draft d14 exercises the mid-run case directly |
| M15 | null run (L770) | **survived** | no committed control produces a null (see draft d15) |

Tally: **caught 8 / survived 7** (survivors: M03 M04 M08 M09 M10 M12 M15). No mutant produced a false
pass of a should-fail control other than through the recorded lines; no control regressed to accepting an
escape vector except M05/M06 (the guards those controls exist for).

## Draft controls for the surviving guards (this seat's report dir only; not frozen)

All demonstrated on the seat clone (receipts in `build/R43MutC1Counter/receipts/`):

- **d04 — newline-count validity** (`receipts/d04-*.txt`): a mirror whose `MUTANTS` table gains row `XNL1`
  (one-line `old`, two-line `new`). Pristine counter: `MUTANT XNL1 … invalid`, `invalid=1`. M04 counter:
  `MUTANT XNL1 … killed by=wit-long-row attributed=L477 value=differs`, `killed=10`. The check is
  demonstrably load-bearing (without it a span/reference mismatch silently changes attribution semantics).
- **d08 — `repo_breach` worktree branch** (`receipts/d08-*.txt`): hostile fixture `h8-bare-worktree` —
  `.git/config` carries `core.bare=true` + `core.worktree=<outside host>`; measured:
  `git rev-parse --show-toplevel` fails rc=128 ("this operation must be run in a work tree") while
  `git config --get core.worktree` returns the outside path — the ONLY reachable worktree-branch-only
  state. Pristine counter: `SETUP … escapes its directory: repo/core.worktree=…` (exit 2). M08 counter:
  `FIXTURE h8-bare-worktree … ok` (accepted).
- **d09 — `exhibits` defects conjunct** (`receipts/d09-*.txt`): anchor fixture `wd-underdeclared` (a
  12-cell row; fixture declares `defects: []`, so the counter marks it WRONG). Pristine `--only NA1`:
  `MUTANT NA1 … SURVIVED exhibits=1>0,rc-silence`. M09 counter: `MUTANT NA1 … killed by=wd-underdeclared`
  — a kill on a class the fixture never declared.
- **d12 — fingerprint content term** (`receipts/d12-*.txt`): counter patched so a content-only rewrite
  (same-length byte reversal of the fixture's `corpus/SOURCES.md`) happens between the two fingerprints.
  Pristine: `TAMPERED wit-long-row fixture tree changed during the run`, `tampered=1`. M12 counter:
  `tampered=0`. (Incidental in both runs: the tampered row source flips one fixture to `wrong=1` — the
  asserted lines are the TAMPERED line and the tampered count.)
- **d10 — floors sum term (redundancy demo, M10 equivalent-in-context)** (`receipts/drafts/d10-*.txt`):
  `FLOORS` patched to `{"anchor": 6, "order": 4}` (sum 10 ≠ TOTAL 9). Pristine AND M10 counters both print
  `PREDICATE C1 fail` — the `per_tool==[FLOORS,FLOORS]` term fails whenever the sum term would, so no
  control can isolate `sum(FLOORS.values()) == TOTAL`; within `good` it is implied by
  `per_tool==[FLOORS,FLOORS]` ∧ `len(MUTANTS)==TOTAL`. The term is redundant defense; its mutant is
  equivalent-in-context, reported as a limit, not a defect.
- **d13 — sidechannel token scan (dedicated draft; M13 already caught by h1/h4)** (`receipts/drafts/d13-*.txt`):
  battery module `sctoken.py` mentions `psutil` in a docstring only. Pristine:
  `SIDECHANNEL hb-sc/sctoken.py tokens=psutil`, `sidechannel=1`. M13 counter: no SIDECHANNEL line,
  `sidechannel=0`.
- **d14 — PINS-AFTER mid-run edit (targeted draft; M14 already caught by `edited`)** (`receipts/drafts/d14-*.txt`):
  the mirror's `anchor_digest_check.py` is appended to mid-run (between the two pin hashes; `sleep 2` into
  a ~3 s witness run — racy, one clean attempt measured). Pristine: `PINS-AFTER mismatched=1`, exit 1.
  M14 counter: `PINS-AFTER mismatched=0`, exit 0.
- **d15 — null run** (`receipts/d15-*.txt`): counter patched so the second "unmodified" copy is actually
  NA1-shaped (`!= NCELLS` → `< NCELLS`). Pristine: `NULL wit-long-row differs on a second unmodified run`,
  `null_detected=1`, exit 1. M15 counter: no NULL line, `null_detected=0`, exit 0.
- **M03 (reference-trace stability) — drafted, not constructible**: the stability check needs a reference
  whose traced site record differs between two runs. Attempted vector: `PYTHONHASHSEED` randomized
  (`"0"` → `""`) so set-repr order varies — measured NEGATIVE: pristine+random-seed and M03+random-seed
  both print `killed=9` (`receipts/d03-*.txt`): no traced span line of either pinned tool holds a
  hash-order-sensitive local (the tracer sorts dict items; no multi-element set locals). The pinned tools
  are deterministic (no clock/rand; per-run scratch names normalised by the tracer's RUN regex), so with
  these two tools the double trace is always stable and the guard is defense-in-depth. A future control
  would need a third tool (or a tracer-visible nondeterminism) — named as a limit, not a defect.

## Adjacent finding (beyond the mutant table): `repo_breach` misses the gitfile escape

`drafts/h7gitfile.py` + `receipts/h7-pristine.txt`: a fixture repo whose `.git` is a GITFILE
(`gitdir: <sibling repo>/.git`, crafted by the same module) is ACCEPTED by the pristine counter with
`wrong=0`: `FIXTURE h7-gitfile-outside … observed_rc=0 … ok`. Measured git semantics (seat clone,
`gitlab/` experiments): a gitfile marks the worktree, so `git rev-parse --show-toplevel` prints the
FIXTURE dir (inside d) and `core.worktree` is unset — both `repo_breach` branches stay silent — while
every `git -C <repo> cat-file` the tools run resolves against the OUTSIDE gitdir. In the probe the
fixture's own history never committed the capture (unpromoted), yet the row's anchor verifies against the
capture blob served by the outside history — the state `--evidence-ref head` exists to prevent
(`anchor_digest_check.py:73-74`). Natural refusal leg: `git -C <repo> rev-parse --git-dir` prints the
resolved ABSOLUTE outside path for a gitfile vs `.git` for a normal repo (measured) — refuse when it does
not resolve to `<repo>/.git`. (Relative `core.worktree` was checked and is NOT a gap: git resolves it
against the gitdir, so an unresolvable value fails identically in `repo_breach`'s check and in the tool's
run — measured, `gitlab/repo3`, `gitlab/repo4`.)

## Envelope lines (QUALITY Q32)

Every control invocation ran inside `claims/envelope.sh`; every measured run below shows
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` — no `INVALID` measurement,
no re-run needed. Full `ENVELOPE <argv>` lines are in each receipt file; decisive runs (paths abbreviated,
`<COUNTER>` = the counter copy under test, `<LANE>`/`<BATTERY>` = the clone lane / battery dir):

```
# baseline witness (pristine counter, clone lane, witness battery)
ENVELOPE start 19:13:34 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 19:13:38 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
# baseline h4 / h5 / h6 (pristine counter): exit=2 each, same digest pair, unchanged
# M01/M02 decisive (witness): exit=1 … unchanged        # M05 decisive (h5): exit=1 … unchanged
# M06 decisive (h6): exit=1 … unchanged                 # M07 decisive (h4): exit=2 … unchanged
# M11 decisive (span): exit=1 … unchanged               # M13 decisive (h1): exit=1 … unchanged
# M14 decisive (edited): exit=1 … unchanged
# d04 pristine exit=1 / mutant exit=0 … unchanged       # d08 pristine exit=2 / mutant exit=1 … unchanged
# d09 pristine exit=1 / mutant exit=1 … unchanged       # d12 pristine exit=1 / mutant exit=1 … unchanged
# d14 pristine exit=1 / mutant exit=0 … unchanged       # d15 pristine exit=1 / mutant exit=0 … unchanged
# d10 pristine exit=1 / mutant exit=1 … unchanged       # h7 pristine exit=1 … unchanged
```

Sample full lines (baseline witness run):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind <SCR> <SCR> --bind <SCR>/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 <COUNTER> --lane <LANE> --battery-dir <BATTERY> --work <SCR>/w1
ENVELOPE start 19:13:34 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 19:13:38 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

## Receipts (copied into `build/R43MutC1Counter/`)

- `receipts/base/` — the pristine baseline, all 15 controls (each with its ENVELOPE lines).
- `receipts/<mutant>-<control>.txt` — the decisive control output per caught mutant (M01 M02 witness; M05 h5; M06 h6; M07 h4; M11 span; M13 h1; M14 edited).
- `receipts/drafts/` — every draft run (d02 d03 d04 d08 d09 d10 d12 d13 d14 d15 h7).
- `receipts/modules/` — the draft fixture modules (`h7gitfile.py`, `h8bare-wt.py`, `sctoken.py`, `wrongdecl.py`).
- `receipts/rig/` — `gen_mutants.py`, `driver.sh`, `compare.sh`, `drafts.sh` (the whole rig; rerunnable).
- Mutant counter copies and per-mutant full control sets stay in scratch (`$S/mut/`, `$S/out-*`) and are
  deleted with the scratch at cleanup; the rig regenerates them.

## Limits

- "Caught" is output-level: a control whose text changes counts, even when the security property survives
  via a redundant branch (M07). The property-level reading is stated per row.
- M10 is equivalent-in-context (proved above), not merely uncovered — reported as a limit per the round's
  own equivalence rule.
- M03's stability check has no constructible trigger with the two pinned tools (measured negative with
  randomized hashing); the draft is a spec plus the negative measurement.
- The hostile controls' round-42 "vector open" halves were not re-run per mutant (they never execute the
  counter under test); the frozen `control-c1-hostile-*.txt` receipts carry them, and my baseline
  reproduces every round-43 half.
- The d14 control is racy by construction (mid-run edit timed into a ~3 s run); one clean attempt is
  recorded, and M14 is independently caught by the committed `edited` control.

VERDICT: c1-counter-mutants-caught-8/15


