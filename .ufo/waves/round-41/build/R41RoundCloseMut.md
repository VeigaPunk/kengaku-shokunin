# R41RoundCloseMut — pricing round-40 closure R3's residuals (round 41, wave 1)

Seat: mutation-tester (leaf). Target: the residuals round-40 closure R3 left open —
`plans/round_close.py`'s 8 surviving mutants (`.ufo/waves/round-40/falsify/F40RoundClose.md`: 6/14
caught) and `plans/tip_receipts.py`'s 6 `F40TipReceipts` defects — re-measured at the wave-1 tip,
each priced with the smallest fixture or fix, drafted here (nothing landed, no lane file written).

Every run below executed inside
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`
with `TMPDIR=$S`. Scratch `S=/fast/scratch/hyaku/kengaku-r41/R41RoundCloseMut` (NVMe); clone
`$S/lane` via `git clone -q --shared`, `git -C $S/lane rev-parse --show-toplevel` → `$S/lane`,
`git -C $S/lane status --porcelain --untracked-files=all | wc -l` → `0` after every mutant restore.
No commit, no jj command, no lane write, no tool installed (pacman paused; nothing needed).

## 0. State at measurement

| item | value | command |
|---|---|---|
| lane tip | `fc79f2a49be0221e138b3885fa0d83bc43b31a42` (wave-1 spec and dispatch; 3 commits after freeze `8ef8b4f`) | `git rev-parse HEAD` |
| `plans/round_close.py` | `112b52f0051357491b1654932948989d57b923c22bea817c15b710e5f9785c3b` — byte-identical to what F40RoundClose measured | `sha256sum plans/round_close.py` |
| `plans/tip_receipts.py` | `e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3` (frozen) | `sha256sum plans/tip_receipts.py` |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, sha256 `3fb72615…4a64e30`, passed as `--census` (a `/fast/scratch` clone cannot discover it) | printed in every `ROUND-CLOSE census tool=` line |
| pin blast radius | `grep -c round_close` over `plans/round41_c1_verify.py`, `round41_c2_verify.py`, `pkg-spec-r41.json`, `pkg_gate.py` → `0 0 0 0`; `corpus/SOURCES.md` → 0 rows | the R3 registry rows are not landed at this tip |

Incident, disclosed: the scratch tree was wiped once mid-wave (only my two driver scripts
survived; a sibling seat's cleanup is the likely cause). No lane or sibling file was touched; the
drivers rebuild their clone and were re-run; all recorded numbers come from post-incident runs.

## 1. round_close.py re-measured — rounds 38/40/41 + `--selftest`

Baseline on shipped bytes (`python3 $S/lane/plans/round_close.py --lane $S/lane --round N --census <fleet>/scripts/sources-census.sh`; receipts `receipts/baseline-round{38,40,41}.txt`):

```
BASE selftest_exit=0 last=SELFTEST checks=5 ok=5 failed=0
BASE rounds={38: 1, 40: 0, 41: 0}   round99_exit=2 (ERROR no claims file: plans/round-99-claims.md)
round 41: ROUND-CLOSE receipts=1 · ORDER RESULT PASS (freeze=8ef8b4f, receipt_commit=f774a87)
          · census exit=0 warnings=15 verdict=PASS · ROUND-CLOSE RESULT PASS exit=0
```

Round 41 is green under shipped bytes: its claims name the receipt by rule (b)
(`round-41-claims.md:92`, the only rule-(b) hit) and rule (c) (`plans/constraints_probe.py`);
rule (a) has **zero** hits — the `Receipt (first recorded run, …)` mention wraps across
`round-41-claims.md:91-92`, so word and path never share a line.

Mutant matrix (driver `rc_matrix.py`, receipt `receipts/rc-matrix.txt`; each mutant is the F40
one-line edit, applied to the clone, compiled, run, restored, sha256-verified):

| # | mutant (round_close.py line) | selftest | rounds 38/40/41 | r99 | verdict |
|---|---|---|---|---|---|
| M01 | `:84` rule-(a) regex → `\breceiptzz\b` | 0 | 1/0/0 | 2 | **SURVIVED** |
| M02 | `:87` rule-(b) `-probe\.txt`→`\.txt` | 0 | 1/**1**/**1** | 2 | KILLED (40, 41) |
| M03 | `:126` rule-(c) drops `_`→`-` | 1 | **2**/2/0 | 2 | KILLED (38, 40) |
| M04 | `:126` rule-(c) hardcodes `round40` | 1 | **2**/0/0 | 2 | KILLED (38) |
| M05 | `:202` order map swapped | 1 | 0/1/1 | 2 | KILLED (38, 40, 41) |
| M06 | `:202` unknown rc → `PASS` | 1 | 1/0/0 | 2 | KILLED (selftest) |
| M07 | `:192` zero-receipt guard → `return 0` | 1 | 1/0/0 | 2 | KILLED (selftest) |
| M08 | `:175` no-claims guard → `return 0` | 0 | 1/0/0 | **0** | **SURVIVED** |
| M09 | `:215` census status → `max(status, 0)` | 0 | 1/0/0 | 2 | **SURVIVED** |
| M10 | `:131` readability filter → `if True:` | 0 | 1/0/0 | 2 | **SURVIVED** |
| M11 | `:115` dedup removed | 0 | 1/0/0 | 2 | **SURVIVED** |
| M12 | `:294` selftest exit → `return 0` | 0 | 1/0/0 | 2 | **SURVIVED** |
| M13 | `:141` `find_census` returns non-file | 0 | 1/0/0 | 2 | **SURVIVED** (equiv) |
| M14 | `:179` gate census guard → `if False:` | 0 | 1/0/0 | 2 | **SURVIVED** (equiv) |

`SUMMARY total=14 killed=6 survived=8` — the survivor set is unchanged from round 40 at the new
round set. Two margin shifts are new information:

- **M02's kill set grew**: round 41 joins. Mechanism (`receipts/M02-rule-b-any-txt-round41.txt`):
  the loosened rule (b) also gates `corpus/evidence/round41/constraints-dry-cases-freeze.txt`,
  which the freeze commit `8ef8b4f` itself carries → `ORDER FAIL freeze-contains-receipt
  8ef8b4f… already has …dry-cases-freeze.txt` → exit 1. The dry table committed with the claims
  is a new discriminating witness for rule (b)'s suffix discipline.
- **Rule (c)'s round-kill margin narrowed**: M03 `[38,39,40]`→`[38,40]`, M04 `[38,39]`→`[38]`
  (`receipts/M03…-round41.txt`, `M04…-round41.txt`: round 41 stays `receipts=1 … PASS` because
  rule (b) names the receipt directly). The selftest still kills both (3/5 cases fail), but the
  rounds alone now keep rule-(c) mutants alive on the newest round — rounds that quote their
  evidence path stop calibrating rule (c).

Hermeticity re-measured at the tip (F40 §5.5 recipe: one `mined` row with a dangling used-by
appended to the clone's `corpus/SOURCES.md`, no tool change; restored, sha256-verified):

```
HERM selftest_exit=1 last=SELFTEST checks=5 ok=4 failed=1   (case A-excused-p10 expect=0 got=1)
HERM round41_exit=1 census_line=ROUND-CLOSE census exit=1 warnings=15 verdict=FAIL
```

Attack-G equivalence re-measured at the tip (`receipts/attack-g-equiv.txt`; `--round 41 --census
/nonexistent/census.sh` on shipped, M13, M14 bytes): `EQUIV shipped==M13 byte-identical=True`,
`EQUIV shipped==M14 byte-identical=True` — both rc=2 with the same stderr line. M13/M14 are
equivalent mutants today, exactly as F40 §attack-G concluded.

## 2. Draft: `round_close.py` selftest v2 — verified to kill 5 of the 8 survivors

Draft driver `rc_draft.py`; diff `receipts/round-close-selftest-v2.diff` (5 edits: docstring
paragraph, SELFTEST table 5→10 cases with three new columns `round_no/census/expect_orders`,
three new FIXTURE_CLAIMS constants, `build_fixture` claims/receipt selection, selftest loop).
`gate()` is untouched. Verified on the scratch clone:

```
DRAFT-SELFTEST shipped-bytes exit=0 last=SELFTEST checks=10 ok=10 failed=0   (no false kills)
DRAFT-ROUND41 exit=0 ['ORDER RESULT PASS', 'ROUND-CLOSE RESULT PASS exit=0'] (rounds leg unchanged)
DRAFT-M01-rule-a-dead selftest=1 [case=F-rule-a-only expect=0 got=2] VERDICT=KILLED
DRAFT-M08-no-claims-pass selftest=1 [case=G-no-claims-round99 expect=2 got=0] VERDICT=KILLED
DRAFT-M09-census-ignored selftest=1 [case=H-census-fails expect=1 got=0] VERDICT=KILLED
DRAFT-M10-unreadable-kept selftest=1 [case=I-phantom-receipt expect=0 got=2] VERDICT=KILLED
DRAFT-M11-dedup-off selftest=1 [case=J-dedup-three-rules expect=0 got=0 verdict=FAIL] VERDICT=KILLED
DRAFT-SUMMARY selftest-killed=5 still=M12,M13,M14
```

The five new cases, in the draft's own terms:

- **F-rule-a-only** (kills M01): claims name a receipt only via `Receipt:
  `corpus/evidence/round39/audit-notes.txt`` (no `-probe` suffix, no probe script), committed
  after the claims; expect 0. Under M01: `receipts=0` → 2.
- **G-no-claims-round99** (kills M08): an A-shaped fixture gated at `--round 99`; expect 2.
  Under M08: 0.
- **H-census-fails** (kills M09): A-shaped fixture, census replaced by a stub `#!/bin/sh\nexit 1`;
  expect 1. Under M09 the census verdict is discarded → 0.
- **I-phantom-receipt** (kills M10): claims name the real receipt (rule c) *and* a phantom
  `Receipt: `corpus/evidence/round39/ghost.txt`` that exists nowhere; expect 0 (phantom dropped).
  Under M10 the phantom is kept → `ORDER ERROR receipt not committed in HEAD` → 2.
- **J-dedup-three-rules** (kills M11): claims reach the same receipt by rules (a)+(b)+(c);
  expect 0 **and exactly one** `ROUND-CLOSE order receipt=` line. Under M11: three lines.

M12 cannot be killed inside the tool (the mutant *is* the exit line); its kill is counter-side —
the hermeticity leg of §1, which the tip re-measure confirms (`selftest_exit=1` from a registry
row alone). A round-42 counter runs `--selftest` twice: clean lane → exit 0 **and** stdout
`failed=0`; registry with one dangling used-by → exit 1 **and** `failed=1`. Under M12 the second
run exits 0 → killed. M13/M14: declare equivalent in the frozen mutants table (the round-41 S10
precedent: `ref_rc=5 mut_rc=5`); do **not** remove either guard — `main`'s guard is the only
thing standing between a bad `--census` and the uncaught-traceback exit-1 shape F40 §5.6 (F7)
already measured for a non-executable census, and neither guard checks executability.

## 3. tip_receipts.py — the six F40TipReceipts defects re-measured on the frozen bytes

All six reproduce at tip `fc79f2a` with tool sha256 `e4f49714…` (`receipts/tr-defects.txt`;
D1/D6 live on the lane clone, D2–D5 on rebuilt fixture repos authored fresh — same shapes as the
round-40 seat's f1–f4, none copied from it):

| defect | re-measure | evidence |
|---|---|---|
| D1 green with no control | `--only regex-log-probe-first-run` → rc=0, `receipts=1 byte_equal=0 skipped=1`, no control line; `--only probe-r19` → 19 skips, rc=0, no control | attacks `tip_receipts.py:29` ("0 … and the control reports `differ`") and `SKILL.md:586` |
| D2 `compared` counts skips | fixture f1: `note compared=2 … no_command=4` while `zeta-probe.txt skip reason=no-committed-re-run-command` is in the same run (`:374` counts mapped byte-kind regardless of skip) | live reachability at tip: `plans/attrib_probe.py`, `plans/catalog_probe.py` → `command_lines=0` |
| D3 first prose line wins | f2: tool picks the `--smoke` line (`:144` first match), genuine receipt (`stdout_matches_receipt=True` for the `--lane` command) → `differ first_diff=byte 8` rc=1; f4 single-space: prose becomes argv → `differ byte 29` rc=1 | false red on a genuine receipt |
| D4 empty receipt never passes | f3: `equal bytes=0` then `control … verdict=unavailable` rc=1 (`:346` treats empty blob as no control) | `differ=0`, exit 1, none of the docstring's exit-1 causes happened |
| D5 provenance reads worktree | f5: committed SKILL.md = 3 lines, `provenance=SKILL.md:3+SKILL.md:5` with `worktree dirty='M SKILL.md'` (`:167` reads `lane/name`) | cites a line that does not exist at HEAD |
| D6 tamper excluded by --only | live: `--only round39 --tamper corpus/evidence/round40/db-wal-probe.txt` → `SETUP: … is not a mapped receipt` rc=2 (`:335` tests the filtered results) | that receipt **is** mapped at the tip |

## 4. Drafts: six fixes, each verified against its own defect demo

Driver `tr_fixes.py`; per-fix diffs `receipts/fix-D*.diff`; post-fix runs `receipts/fix-*.txt`
(in `tr-fixes.txt`). Each patch applied to a fresh copy of the frozen bytes; every fix verified:

| fix | patch (lines) | verified post-fix |
|---|---|---|
| D1 | print a marker when no control ran (2) | `control none no byte-equal mapped receipt to tamper`, rc=0 — the green-no-evidence shape becomes visible |
| D2 | `strict` excludes skipped mapped receipts (2) | f1: `note compared=1` (was 2), rc=0 |
| D3 | `usage_argv` prefers the matching line that already carries `--lane` (9) | f2: `equal bytes=21` rc=0 (was false red); **f4 stays `differ` rc=1** — a single-space line has no clean sibling, so that shape remains a named limit unless the tool tries every candidate (runtime cost, not drafted) |
| D4 | split the control guard: no fresh output → fail; empty blob → `verdict=unavailable-empty-receipt`, not a failure (6) | f3: rc=0 with `control … verdict=unavailable-empty-receipt` |
| D5 | provenance reads committed text (`ls-tree` + `git show`, pathlib-glob semantics) (12) | f5: `provenance=command=SKILL.md:3,receipt=undocumented` — the phantom `:5` hit is gone |
| D6 | test `--tamper` ids against the full `plan`, and say "mapped but excluded by --only" (5) | live: rc=2 with the true sentence |

Lane-neutrality of the whole bundle, measured: all six patches applied together, `--list` on the
clean lane clone → `COMBINED --list lane-identical=True` (byte-identical to the unpatched tool).
On a clean clone every fix is output-neutral; each only changes the defective shape.

## 5. What a round-42 claim can freeze

- **`round_close.py` selftest v2 — freezable now, cheapest.** No r41 counter, spec or gate
  references `round_close.py` (grep count 0 across the four pinned files), and no SOURCES row for
  it exists yet (the R3 rows are still to land), so editing it busts no pin. Claim shape: freeze
  the new bytes (selftest region only; `gate()` untouched — the diff shows it), a mutants table
  of 14 with M01/M08/M09/M10/M11 killed by the shipped selftest, M02–M07 killed by
  selftest+rounds (M02's kill set now includes 41 via the dry table), M12 killed by the counter's
  hermeticity leg, M13/M14 declared equivalent with the byte-identical attack-G receipt →
  **12 of 14 killed, 2 equivalent**, predicate `killed=12 survived=0 equivalent=2`.
- **`tip_receipts.py` defect fixes — freezable only as a bundle with a C1 re-pin.** The tool is
  pinned by r41 C1 (`PINS` content digest `e4f49714…`); any edit flips `PINS mismatched=1` on a
  later clean clone by design, so a round-42 fix means one tool revision + new pins + re-running
  (and possibly re-touching) the 23-fixture battery whose fixtures assert the tool's printed
  shapes. All six fixes are small (2–12 lines), verified, and lane-neutral, so the bundle is
  coherent — but it is a C1-successor claim, not a rider. Cheaper alternative: file the six
  defect fixtures under the routed-findings rider (`considerthese/2026-10-26.md` proposal 1's
  append-only file) as demonstrated-open defects and defer the tool revision to a round that
  re-pins C1 anyway.
- **Not freezable as kills:** M13/M14 (equivalent — declare, with the attack-G receipt); M12
  inside the tool (counter-side only); D3's f4 single-space shape without a try-all-candidates
  rewrite.

## 6. Limits

- One tip (`fc79f2a`), one clone, mutants are F40's 14 single-line edits (not an exhaustive set —
  `norm_repo_path`, the work-tree-top check and argument handling remain unmutated, as F40 §6
  already recorded).
- The selftest-v2 draft and the six fixes are verified on scratch copies only; nothing is landed,
  and the draft's `expect_orders` column extends the selftest contract from exit-only to
  exit+output (one captured-stdout assertion) — that contract change is part of the proposal.
- Fixture probes for D2–D5 are my own minimal scripts; the round-40 seat's fixtures were not
  copied (only their shapes, as its report describes them).
- The scratch tree was wiped once by an external actor mid-wave; drivers self-heal and all
  recorded numbers are post-incident. No lane file, index or jj state was touched at any point.

## Evidence index (`receipts/`, all under this report dir)

`rc-matrix.txt` (14-mutant re-measure) · `rc-draft-matrix.txt` (draft verification) ·
`round-close-selftest-v2.diff` · `attack-g-equiv.txt` · `baseline-round{38,40,41}.txt` ·
`M02/M03/M04/M05/M11…-round41.txt` · `tr-defects.txt` · `tr-fixes.txt` · `fix-D{1,2,3,4,5,6}*.diff`

VERDICT: residuals-remeasured-14-still-open-14
