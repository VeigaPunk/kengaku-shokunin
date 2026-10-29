# C2CritLedgerReach — attack on the frozen R53-C2 counter (wave 1)

Seat: C2CritLedgerReach (critic, leaf). Target: `plans/round53_c2_tipstate.py` (frozen, committed at a34838f;
sha256 `859ec38d3d39d7b33ca91a1a33269606e8c174e4fbaf40eeaa28280f1dfccfc7`, identical in the lane and in my scratch copy).
Counter not edited. No commit, add, push, stash, checkout, reset or pull in the lane or fleet repo.
Blindness: I read no `C1Label*` file and no classifier file. I did not read any other seat's output.

## Verdict

The counter's `PREDICATE R53-C2 pass` is **not** a truth measure. Its registry and ledger are read from `--lane`, the row set
is never pinned to the frozen 75 names, and the argv leg checks only that a script name appears somewhere in argv. Twenty-plus
ledgers that declare no truth at all return `PREDICATE R53-C2 pass` with exit 0. The most serious ones:

- **Zero rows passes.** No registry heading, or a heading with no table, and an empty ledger: `ROWS registry=0 ledger=0` and `pass`.
- **The real 75-row registry passes when every row is declared green via `python3 -c pass <script>`** (J1: `executed=75 mismatched=0`, `pass`).
- **One prose line above the real table zeroes the registry** (K1, real SKILL.md, empty ledger: `registry=0`, `pass`).
- **Renaming the registry heading silently shrinks the registry to 2 rows** (K2: `registry=2`, `pass`).
- **Removing 5 real rows and their ledger entries passes at 70** (K3). Nothing compares the count or names with the frozen 75.

The claim's Kill rule says a pass must mean "every registry row re-executed to its declared exit". The counter enforces that
only for rows it happens to find, and it finds whichever rows the lane's own SKILL.md says exist. C2 as frozen cannot fail a lane
that edits its own registry, and it cannot tell a vacuous gate from a real one (see residuals).

## Commands run (all in scratch; nothing in the lane or fleet repo was mutated)

- `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/C2CritLedgerReach/lane`
  then `git -C <lane> rev-parse --show-toplevel` → `.../C2CritLedgerReach/lane` (asserted). Clone HEAD `1373b6c`.
- `cp` of the lane's `plans/round53_c2_tipstate.py` to `bin/counter.py` (sha256 matches the lane file).
- `python3 bin/counter.py --selftest` with `TMPDIR` in scratch → `SELFTEST cases=12 failures=0`, rc 0 (out/C0-selftest.txt).
- `python3 -B .../attack_c2.py` (driver below, 147 s wall, rc 0) → 36 counter runs over fixtures and real-tree rows, plus the
  `--selftest` and `--dry` runs; full outputs in `out/<label>.txt` (39 files), one-line summary in `out/SUMMARY.txt`.
- One follow-up: `python3 -B bin/counter.py --lane fx/K2-lane --source fx/J1-src --work fx/K2-work --jobs 4` (out/K2-…txt).
- Real-registry measurements via the counter's own functions (`registry_rows`, `registry_block`, `row_script`) on the clone's SKILL.md.

Driver: `.ufo/waves/round-53/w1/C2CritLedgerReach/attack_c2.py` (kept). It needs the scratch clone and counter copy, which I
removed at exit (see "Scratch"); recreate them with the first two commands above before rerunning.

## Measured facts about the real registry (clone HEAD 1373b6c)

- `## Gate/probe registry` occurs **twice**: line 560 (the heading) and line 636 (inside the `round52-c1` table cell, as prose).
  The counter uses `text.find` = the first, so it currently parses the intended block.
- `registry_rows` on the real SKILL.md: **75 rows**, `dups=''`, `row_script` non-None for **75/75** (`script_none=0`).
- `.ufo/waves/round-53/c2-row-names.json` lists **75** names. The counter never reads that file (grep of the frozen counter: no reference).
- Rows as parsed: `routed-findings` … `tb2-grader-probe` after the heading rename (K2 shrink, see below).

## Routes (construction → counter output → leg holds? → smallest fix)

Pass = `PREDICATE R53-C2 pass`, rc 0. "Lands" = the route makes the predicate pass without the declared tip-state being true.

| # | Route | Construction | Counter output (key lines) | Lands? | Smallest fix |
|---|---|---|---|---|---|
| A1 | Zero rows, no heading | SKILL.md with no `## Gate/probe registry`; ledger `{}` | `ROWS registry=0 ledger=0 … executed=0`, `PREDICATE pass` | **yes** | Assert `n_reg == 75` and `sha256("\n".join(sorted(names)))` equals a digest constant in the counter. |
| A2 | Heading, zero rows | heading + header row only; ledger `{}` | same, `registry=0` | **yes** | same |
| A3 | Heading in prose before the table | "The table `## Gate/probe registry` below…", then `## Overview`, then the real table with a defective row `a` | `registry=0`, `pass`; row `a` (exits 1) never run | **yes** | Line-anchored heading only (`(?m)^## Gate/probe registry`), and fail if it occurs ≠ 1 times. |
| K1 | Real SKILL.md, one prose line above the table | prepend "Note: see `## Gate/probe registry`…" to the real file; ledger `{}` | `registry=0 ledger=0`, `pass` (real tree) | **yes** | same as A3 |
| K2 | Real SKILL.md, heading renamed | rename the line-560 heading to `## Registry`; the first occurrence becomes the line-636 cell text; block = rest of file | `ROWS registry=2 ledger=2`, `PREDICATE pass` | **yes** | same as A3; the count pin also catches it |
| K3 | Real rows deleted | delete the last 5 table rows of the real SKILL.md; ledger = 70 forged-green | `ROWS registry=70 ledger=70`, `pass` | **yes** | count pin against the frozen 75 (A1 fix) |
| J1 | Real 75-row registry, forged green | real SKILL.md; each row argv `python3 -c pass <its script>`, exit 0 green | `ROWS registry=75 ledger=75`, `ARGV entry=75`, `executed=75 mismatched=0`, `pass` | **yes** | argv shape check (A5/A7 fix) |
| A4 | Heading appears twice | block 1 = row `a`; `## Notes`; block 2 = row `b` (exits 1, real defect) | `registry=1`, `pass`; `b` never counted | **yes** | Reject duplicate heading occurrences (A3 fix). |
| D1 | Name cell without backticks | row `| b | gate | python3 plans/b.py |…` (no backticks); `b` exits 1 | `registry=1`, `pass` | **yes** | Fail on any table line in the block whose first cell is not a backticked name (`BAD-NAME`). |
| D2 | Row named `__dups__` | row `__dups__` (exits 1) | `registry=1`, `pass`: `rows["__dups__"] = ",".join(dup)` overwrites the row line | **yes** | Keep the duplicate list in a separate variable, not in the row dict. |
| D3 | Row outside the block | row `b` (exits 1) placed after `## Retired` | `registry=1`, `pass` | **yes** | Same as A3: the block must cover every table in the registry section; fail on a second table with `|`-rows after a heading. |
| D4 | Duplicate JSON key in ledger | `"a"` written twice (red with evidence, then green); `a.py` exits 1 | `ledger=1`, `MISMATCH a declared exit=0 observed exit=1`, `fail` | integrity only, not a pass | `json.loads(object_pairs_hook=…)` that rejects duplicate keys. |
| A5 | Script as dead argument | ledger argv `["python3","-c","pass","plans/a.py"]`, green; `a.py` exits 1 | `pass` (`executed=1`, `mismatched=0`) | **yes** | Require `argv[0]=="python3"` and `argv[1]==script`. Current code checks `script in argv` only. |
| A6 | `--help` relabelled `entry` | argv `["python3","plans/a.py","--help"]`, `kind":"entry"`; the script exits 1 without `--help` | `pass`, `ARGV entry=1 selftest=0 help=0` | **yes** | Kind must match argv: `help` ⇔ `--help` in argv; `selftest` ⇔ `--selftest`; `entry` ⇔ neither. `kind` is never checked against argv. |
| A7 | `cat` as the gate | argv `["cat","plans/a.py"]`, green; `a.py` exits 1 | `pass` (script never executed) | **yes** | argv[0] check (A5 fix). |
| A8 | Wrapper swallows the exit | argv `["sh","-c","python3 plans/a.py; exit 0","plans/a.py"]`; `a.py` exits 1 | `pass` | **yes** | No shell wrappers: argv[0] must be `python3`; reject `sh`/`bash`/`-c`. |
| A9 | Non-git `--source` | plain directory copy containing an untracked helper; `a.py` passes only because of it | `pass`, **no `SOURCE` line**; `clean=None` accepted by `clean in (True, None)` | **yes** | Require `(source/.git).exists()` and `clean is True`; the frozen text says `clean=yes`. |
| A9b | Same helper, git source | control | `clean=no`, `MISMATCH`, `fail` | caught (control) | — |
| H1 | Source is an older commit | `--source` = clone checked out at the commit before the defect (a.py green); tip has a.py red | `SOURCE rev=1c0e617… clean=yes`, `pass`; the ledger's `base` field is never read | **yes** | Pass only if source `HEAD` equals an expected landing rev (a required argument or a digest constant), and use `ledger["base"]`. |
| H1c | Control: real tip source | same ledger | `MISMATCH`, `fail` | caught (control) | — |
| I1 | Lane registry, not the tip's | tip SKILL.md has rows `a` and `b` (`b` exits 1); the lane's SKILL.md has only `a` | `registry=1`, `pass`; the counter reads SKILL.md and ledger from `--lane`, never from the clean `--source` | **yes** | Read SKILL.md and the ledger from `--source` (the clean tree), not from `--lane`. |
| B1 | Cross-row state through `.git/config` (clone) | row `a` runs `git config c2.flag 1`; row `b` exits 0 only if the flag is set; `b` is declared green | `--jobs 1`: `executed=2 mismatched=0`, `pass`. **Fresh clone, row `b` alone: exit 1.** | **yes** (at jobs=1) | Fresh `git clone --shared` per row, or `reset --hard <pinned rev>` plus `clean -ffdx` and a clean `.git/config`. |
| B2 | Same ledger at `--jobs 4` (default in the frozen command) | 5 runs | **5/5 `MISMATCH b declared exit=0 observed exit=1`, `fail`** | caught here; the outcome depends on the `--jobs` value | Run once per job-count and require equal verdicts, or use the fresh-clone fix. |
| B3 | Non-git source, no reset | plain dir; `a` writes `plans/flag.txt`; `b` requires it; jobs=1 | `pass`; fresh copy, `b` alone: exit 1 | **yes** | Fresh copy per row (same as B1 fix). `reset` is git-only. |
| E1 | Generic evidence | `a` crashes (`raise RuntimeError`); evidence `"Traceback (most recent call last)"` | `pass` (`evidence_missing=0`) | **yes** | Evidence is presence-only, so this is a weak leg. Fix: evidence must be a full output line of at least 12 chars and must not be a generic traceback header; or record the observed output digest. Not fully closable (see residuals). |
| E2 | Padded reason, short evidence | reason = 10 filler words; evidence `"DEFECT"` (6 chars) | `pass`, `bad_reason=0` | **yes** | Count words is not a reason; minimum evidence length 12 and reason must mention the evidence text. |
| E3 | Gate that kills itself | `a` prints `FAULT injected` then `SIGKILL`; declared red `exit=-9` | `pass`, `declared_red=1 observed_red=1` | **yes** | Reject negative exit codes (signal kills are not a red verdict): require `0 ≤ exit ≤ 255`. |
| F1 | `timeout_s` as a string | `"timeout_s": "2.5"` | rc 1, Python traceback from `int()` in `run_row` (`evaluate` line 223); no `PREDICATE` line | no (fails, but noisily) | Validate types in `static_legs` and print `BAD-DECL`. |
| G1 | `--dry` exit code | valid static legs, `--dry` | rc **0**, `DRY static legs only: no predicate` | exit-code route only | `--dry` should exit 2 or print `PREDICATE SKIPPED`, so `$?` alone cannot be read as a pass. |

Controls that the counter caught (each is a real failure, so the predicate held where it should):
C2 forged green (`MISMATCH a declared exit=0 observed exit=1`); C3 `--only` (`pass` never; `fail`); C4 tight `timeout_s`
(`TIMEOUT a after 1s`, `fail`); C5 dirty git source (`clean=no`, `fail`); A9b; H1c. Honest red+green ledger (C1) passes, as it should.

## Residuals the counter cannot close (route, but not a counter bug)

- **A gate that cannot fail.** `plans/b.py` = `sys.exit(0)` (C1) is "truthfully green". The counter compares declarations with
  observation, so a vacuous gate is indistinguishable from a real one. The claim's own "truth" leg does not cover this. Fix
  would be a planted-fault leg per row (out of scope for C2).
- **Evidence is presence-only** (E1, E2). Any output containing the fragment satisfies it. Causality needs a planted-fault or
  an output digest, not a substring.
- **Process-group leak on timeout** (not tested): `subprocess.run` kills only the direct child on TIMEOUT. Its descendants
  keep running into the next row's reset. Fix: `start_new_session=True` and kill the group.
- **`HOME` and `~/.cache` are not isolated per row** (not tested): rows that write there leak across runs and across rows.

## Smallest fix bundle (proposal; NOT implemented or run; the counter stays frozen)

The claim cannot be repaired by a patch to the counter without a dated amendment (claims §Amendments). The minimal set that closes
the pass routes above: (1) pin the row count and names as constants (75, digest of sorted names) and fail on any other
count; (2) line-anchored, single-occurrence heading, and every table row in the block must be a backticked name; (3) read
SKILL.md and the ledger from `--source`, not `--lane`; (4) argv must be `[python3, <entry script>, …]`, and `kind` must match
the flags; (5) exit must be 0–255, duplicate JSON keys rejected; (6) source must have `.git` with `clean is True` and an expected
HEAD; (7) fresh clone per row. Each of these was **not run** against my fixtures.

## Other observations

- `script in argv` (membership) is the only argv check; the claim says "names the same script as its row's entry cell".
- `ledger["base"]` is written but never read.
- The counter prints `SOURCE rev=` but never compares it to anything.
- `executed == n_reg` is only as strong as `n_reg`, which is the lane's own table (see A1–K3).
- Counter-line numbers (e.g. the `evaluate` traceback at line 223, `static_legs` at 124–157) are the frozen file's own.
- `tool:` none. No tool was installed or upgraded in this seat.

## Scratch

Fixtures and the clone lived under `/fast/scratch/hyaku/kengaku-r53/C2CritLedgerReach/`; I removed that directory before
yield. The seat's kept files are below. Credential-shaped strings: none written.

## Files (absolute paths)

- Driver: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2CritLedgerReach/attack_c2.py`
- Summary (every run, one line each): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2CritLedgerReach/out/SUMMARY.txt`
- Full per-run output: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2CritLedgerReach/out/<label>.txt`
  (`C0-selftest`, `C1-control-honest` … `K3-real-five-rows-removed`, `G1-dry`, `K2-renamed-heading-shrinks-registry`)
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2CritLedgerReach.md`
