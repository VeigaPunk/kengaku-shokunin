# E5ChessProbe — round 55 wave 1 seat report

## Assignment
NEW instrument `plans/round55_c3_chess_probe.py` (R55-C3, frozen contract in
`plans/round-55-claims.md` §R55-C3): bubblewrap-sandboxed offline execution of the captured
TB2 `chess-best-move` grader against 12 frozen synthetic `move.txt` cases with pre-written
predictions.

## What was built
`plans/round55_c3_chess_probe.py` (only file written in the lane). Design:
- Frozen 12-case table (name | move.txt bytes | prediction) embedded as a literal, written
  before any run, matching the seat spec exactly (incl. `g\uFF12` fullwidth digit, CRLF,
  empty file, decoy/duplicate tokens).
- Per case: materializes `<work>/cases/<name>/move.txt`; materializes the captured grader as
  a byte-copy at `<work>/tests/test_outputs.py` (bytes read from
  `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py`, no network);
  refuses SETUP (exit 2) unless the capture's sha256 equals the frozen pin
  `a540714e…30cb8f286` (TB2 pin `2fd12b88…`).
- Sandbox per frozen spec: `bwrap --unshare-all --die-with-parent --ro-bind /usr /usr`
  (+ root symlink recreation for /bin /sbin /lib /lib64, ro /etc, --proc, --dev, tmpfs /tmp
  and /home), `/tests` bound read-only, case dir bound writable at /app, then
  `python3 -c "import sys; sys.path.insert(0,'/tests'); import test_outputs as t;
  t.test_move_correct()"`.
- Verdicts: rc 0 → P; nonzero with `AssertionError` in output → F; anything else (bwrap
  error, OSError, timeout, other exception) → per-case SETUP, printed, overall exit 2.
- Output: one `CASE <name> predicted=<P|F> observed=<P|F> rc=<n>` line per case, then
  `cases=12 observed_pass=P observed_fail=F mismatches=M`, then
  `PREDICATE R55-C3 pass|fail`; exit 0 iff M==0, 1 iff M>0, 2 on any setup error.
- CLI: `--lane` (default `.`), `--work` (scratch; defaults to a fresh dir under TMPDIR;
  always `shutil.rmtree`'d on exit — no /tmp hardcode), `--receipt <path>` (tee full output,
  parent dirs created), `--selftest` (toy grader + toy artefacts only, never touches the TB2
  capture; prints `SELFTEST cases=2 failures=N`; 0/1/2 = plumbing ok / plumbing mismatch /
  setup error).

## Commands run (all from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`)
| Command | Exit | Result |
|---|---|---|
| `command -v bwrap; bwrap --version; sha256sum <capture>` | 0 | bwrap 0.13.1 at /usr/bin/bwrap; capture sha256 matches frozen pin exactly |
| `python3 plans/round55_c3_chess_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r55/E5ChessProbe/selftest-work` | **0** | `SELFTEST cases=2 failures=0` (toy-pass observed=P rc=0, toy-fail observed=F rc=1) — the acceptance check |
| `python3 plans/round55_c3_chess_probe.py --lane . --work …/w1 --receipt .ufo/waves/round-55/w1/E5ChessProbe/battery-verify.txt` | **0** | full 12-case battery (one permitted verification run, see below): all 12 observed == predicted; `cases=12 observed_pass=5 observed_fail=7 mismatches=0`; `PREDICATE R55-C3 pass` |
| same command re-run to a second work dir, `diff` against receipt | 0 | stdout and receipt byte-identical (deterministic) |
| battery with `--lane` pointing at an empty dir | 2 | `SETUP captured grader missing: …`, exit 2 |
| battery against a tampered capture (sha mismatch) | 2 | `SETUP grader sha256 … != frozen pin …`, exit 2 |
| `rm -rf /fast/scratch/hyaku/kengaku-r55/E5ChessProbe` | 0 | seat scratch removed (verified gone); instrument also self-cleans every `--work` dir it creates |

## Disclosure: the real 12-case battery was run once
The seat spec says a sibling runs the official battery and I should not — but permits one
verification run if disclosed. I ran it once (command above) to verify the battery path
(byte-copy materialization, per-case verdict classification, summary/predicate lines,
receipt tee) because `--selftest` alone does not exercise grader materialization. Output kept
at `.ufo/waves/round-55/w1/E5ChessProbe/battery-verify.txt`. **I did not write the frozen
receipt path `corpus/evidence/round55/chess-best-move-probe.txt`** — that belongs to the
sibling's official run. Predictions were embedded in the file before this (and any) run;
the observed battery result (mismatches=0) matches the frozen table.

## Verification status
- `python3 plans/round55_c3_chess_probe.py --selftest` exits 0 — PASS (acceptance).
- No tool installs/upgrades this seat (nothing recorded).

## Defects found
None in the frozen claims or the captured grader. Two spec-ambiguity notes, resolved as
documented in the module docstring (both within "adapt bind targets to your layout"):
- The frozen bwrap sketch `--ro-bind /tests <t>` has bwrap's SRC/DEST order inverted for the
  stated goal; I bind `<work>/tests /tests` (SRC DEST) which is the only reading that puts
  the byte-copy at /tests read-only.
- The frozen sketch binds no interpreter tree; python3 cannot exec without it, so /usr is
  bound read-only with root symlinks recreated — the same pattern used by existing
  `plans/password_recovery_probe.py`.

## Dead ends
None. No subagents spawned, no git mutations, no files outside the seat's scope touched
(lane file + `.ufo/waves/round-55/w1/E5ChessProbe/` outputs + seat scratch, now deleted).
