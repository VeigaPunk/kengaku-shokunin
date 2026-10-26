# R43PkgEntry — C2 knowledge-entry draft: TB2 `feal-differential-cryptanalysis` grader

Round 43 (hyaku run 9), wave 1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, cloned at
`d33350fdb01ce27cbff47b04642fd2c1471e5c26`. Claim C2 as frozen in `plans/round-43-claims.md`
(freeze commit `02753f260805e2e45b05af22145da00f91671364`, first probe run `6b49694d2ff533135fc238a8400f3e0dc1c82026`).
This seat drafted the entry and the four-file integration, and validated both inside a clone. It did not write the
lane, commit, or touch any frozen instrument.

## Behavior — what was produced

1. **Entry draft** — `.ufo/waves/round-43/build/R43PkgEntry/tb2-feal-differential-cryptanalysis-grader.md`
   (396 lines, 36 242 bytes, sha256 `7646f60604b287fbddbad74dc5281a81f51338800a42b22b619869d16f855ae9`). Sections, in
   order: six `source:` lines (S129 plan → S134), `verified-at: 2026-10-26`, `recheck: 180d`, Summary, Source
   labels, What is graded, Located quotes, Requirement map (+ Contestable tags), Case table, Mechanism, Findings
   (12, one per receipt case), Regrade, What the probe does not show, Prior art (an explicit SLOT for
   `R43ScoutPriorArt`), Negative space with a six-clause falsifier.
2. **Integration patch** — `.ufo/waves/round-43/build/R43PkgEntry/integration.patch` (62 726 bytes):
   `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` (new), `corpus/SOURCES.md` (+6 rows
   S129–S134, 11 cells each), `corpus/README.md` (+index row citing S129–S134, +coverage bullet, +one
   `## Frontier` discharge sub-bullet), `PROVINCE.md` (+one round-43 paragraph whose first line names both
   `feal-differential-cryptanalysis` and the entry file name). 421 insertions, 0 deletions.
3. **Receipts** — `gate-receipt.txt` (green), `gate-receipt-red-p6.txt` (first run, red on P6),
   `c2-functions-receipt.txt`, `c2-counter-receipt.txt`.

## Gates run (exact command, envelope, output)

All runs used the round-43 envelope, as the host-safety rule requires. Scratch `S=/fast/scratch/hyaku/kengaku-r43/R43PkgEntry`,
`TMPDIR=$S`. Steps before the runs: `git clone -q --shared <lane> "$S/lane"`; `git -C "$S/lane" rev-parse
--show-toplevel` → `/fast/scratch/hyaku/kengaku-r43/R43PkgEntry/lane`; draft copied to
`$S/lane/corpus/knowledge/`; the four integration files edited; `git -C "$S/lane" add -A <the four paths>` (staging
only — no commit; this is how `P9 clean tree` sees the files as tracked rather than untracked). Effective spec
`$S/effective-spec.json` = the frozen `plans/pkg-spec-r43.json` with `receipt_sha256` filled from the receipt
(`8c987463d6c9b4dd7c7478beedbefef20e6a7996ec59d1620167d66ae4e637b4`).

**Gate, first run (red, before the S134 tier fix).** Command:

```
envelope.sh "$S/env" /usr/bin/python3 plans/pkg_gate.py package --root "$S/lane" \
  --spec "$S/effective-spec.json" --rerun --require-clean-tree
```

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43PkgEntry/env /fast/scratch/hyaku/kengaku-r43/R43PkgEntry/env --bind /fast/scratch/hyaku/kengaku-r43/R43PkgEntry/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg_gate.py package --root /fast/scratch/hyaku/kengaku-r43/R43PkgEntry/lane --spec /fast/scratch/hyaku/kengaku-r43/R43PkgEntry/effective-spec.json --rerun --require-clean-tree
ENVELOPE start 19:11:01 cwd=/home/vgpnk/Projects/shokunin
P1 ok pinned=2 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=18 distinct_quotes=18 distinct_lines=16 out_of_word_range=0
P4 ok checked=18 bad=0 first=0
P5 ok manifest_entries=12 bad=0 first=0
P6 DEFECT rows=6 bad=1 first=S134: tier='B'
P7 ok source_lines=6 bad=0 first=0
P8 ok index_rows=50 knowledge_files=50 bad=0 first=0
P9 ok untracked=0 first=0
P10 ok probe_rerun=byte-equal bytes=3292
defects=1
ENVELOPE end 19:12:40 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

This red run is kept as the evidence that `P6` can fail on this package: the spec's `entry_rules.row_tier` is `A`
for every row, and my first S134 row said `B` (the authors' README is prose, tier B by my first reading). The
frozen assignment says S129–S134 tier A, so the row was corrected to `A`; no other clause moved.

**Gate, second run (green).**

```
envelope.sh "$S/env2" /usr/bin/python3 plans/pkg_gate.py package --root "$S/lane" \
  --spec "$S/effective-spec.json" --rerun --require-clean-tree
```

```
ENVELOPE start 19:12:31 cwd=/home/vgpnk/Projects/shokunin
P1 ok pinned=2 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=18 distinct_quotes=18 distinct_lines=16 out_of_word_range=0
P4 ok checked=18 bad=0 first=0
P5 ok manifest_entries=12 bad=0 first=0
P6 ok rows=6 bad=0 first=0
P7 ok source_lines=6 bad=0 first=0
P8 ok index_rows=50 knowledge_files=50 bad=0 first=0
P9 ok untracked=0 first=0
P10 ok probe_rerun=byte-equal bytes=3292
defects=0
ENVELOPE end 19:14:10 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

**Counter functions v4/v7/v9/v10** (the C2 counter imported by path, not copied; `$S/run_c2_functions.py`):

```
envelope.sh "$S/env" /usr/bin/python3 "$S/run_c2_functions.py" "$S/lane"
ENVELOPE start 19:12:17 cwd=/home/vgpnk/Projects/shokunin
V4 ok cases=12 mismatches_named=0/0 bad=0
V7 ok rows=5 tags=5 bad=0
V9 ok case_rows=12/12 bad=0
V10 ok mechanism_rows=12/12 bad=0
functions=4 defects=0
ENVELOPE end 19:12:18 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

**Full counter on the clone** (all ten checks, including the V2 gate rerun and the V8 order check):

```
envelope.sh "$S/env3" /usr/bin/python3 plans/round43_c2_verify.py --lane "$S/lane" --work "$S/w"
ENVELOPE start 19:14:14 cwd=/home/vgpnk/Projects/shokunin
V1 ok listed=12 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=18 distinct_quotes=18 distinct_lines=16 out_of_word_range=0
    gate: P4 ok checked=18 bad=0 first=0
    gate: P5 ok manifest_entries=12 bad=0 first=0
    gate: P6 ok rows=6 bad=0 first=0
    gate: P7 ok source_lines=6 bad=0 first=0
    gate: P8 ok index_rows=50 knowledge_files=50 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=3292
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=6 bad=0
V4 ok cases=12 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=5 tags=5 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=12/12 bad=0
V10 ok mechanism_rows=12/12 bad=0
checks=10 defects=0
PREDICATE C2 pass
ENVELOPE end 19:15:54 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Every envelope line reports the same `~/.local/bin` content digest before and after; no measurement was marked
`INVALID`. No tool was installed or upgraded by this seat (nothing needed), so no tooling record is owed.

## Coverage against the gate's rules

| Rule | Where it is satisfied | Measured |
|---|---|---|
| ≥10 located quotes, ≥10 distinct locations, 3–25 words, verbatim on the cited capture line | `## Located quotes`, 18 rows | `P3 rows=18 distinct_quotes=18 distinct_lines=16 out_of_word_range=0`; `P4 checked=18 bad=0` |
| one requirement-map row per frozen TAG, label derived from **all** violating cases, frozen line, ≥1 violating citation | `## Requirement map`, 5 rows over 5 tags | `V7 rows=5 tags=5 bad=0` |
| case table = the receipt's 12 CASE lines in order, letter and verdict equal | `## Case table` | `V9 case_rows=12/12 bad=0` |
| `## Mechanism` = one row per receipt case in order, decisive capture line + ≥2-word verbatim quote | `## Mechanism` | `V10 mechanism_rows=12/12 bad=0` |
| S129–S134 `source:` lines, `verified-at`, `recheck`, `## Negative space` with falsifier | entry header + tail | `P7 source_lines=6 bad=0` |
| every row id in the entry outside its `source:` line | Source labels, Findings, Falsifier | `V9` (`bad=0`) |
| PROVINCE line naming task + entry; README `## Frontier` naming task; README index row citing all six rows; coverage bullet naming entry + receipt | integration patch | `P8 index_rows=50 knowledge_files=50 bad=0`, `V9 bad=0` |
| SOURCES rows: 11 cells, pinned raw URL, tier A, status mined, teaches ≥8 words and pairwise distinct, used-by = entry | 6 new rows | `P6 rows=6 bad=0`, `V3 rows=6 bad=0`, `V6 census_exit=0` |

Distinct locations are 16 rather than 18 because three quote rows cite `instruction.md:3` (attack path, uint32
return, 30 s) — the gate's `min_distinct_locations` is 10, so the margin is 6.

## What the draft argues (one line per finding)

The class is worded as **module import + in-process call**: `test_outputs.py:22-24` appends `/app` then `/tests` and
imports the agent's `attack` and the reference `feal_in_c` into the same interpreter; `:27` seeds six keys in that
process; `:29` calls `attack.attack(feal_in_c.encrypt)`; `:30` is the entire value check — `assert
feal_in_c.get_keys()[5] == stolen`; `test.sh:25` makes pytest's exit status the reward. The entry's 12 findings:

1. `nop` — `import attack` fails, `ModuleNotFoundError`, no `/app/attack.py`.
2. `oracle-solve-sh` — the shipped `solve.sh` filter at `solve.sh:90` yields a value the assert accepts.
3. `wrong-key`, `oracle-off-by-one` — any wrong integer fails the one equality.
4. `return-str` — a correct number as `str` fails; `int == str` does not coerce.
5. `cheat-import-get_keys` — `get_keys` is an exported `METH_NOARGS` function (`feal_module.c:51`), so the answer is
   importable from the graded module.
6. `cheat-always-equal` — `int.__eq__` returns `NotImplemented`, so the right operand's `__eq__` decides.
7. `cheat-sysmodules-shadow` — `import attack` runs before `import feal_in_c`, so a module-level `sys.modules`
   assignment wins.
8. `cheat-patch-get_keys` — `get_keys` is looked up after `attack()` returned, so rebinding it changes both sides.
9. `cheat-exit-zero` — `os._exit(0)` inside `attack()` leaves exit status 0, and `test.sh:25` rewards it.
10. `cheat-clock-seed` — `srand(time(NULL))` once per process plus 16-bit seeds times 1234567 (`feal.c:60-66`)
    makes the schedule replayable; flagged `host=libc-rand`.
11. `slow-oracle-45s` — nothing times `:29`; the only ceiling is `task.toml:22`'s 1800 s.
12. `feal.c:84` — round 3 mixes with `key[round_num + 2]`, which is why index 5, not 0 or 1, is the graded value.

Derived labels: `chosen-plaintext` unenforced (6 passing violators), `recover-key5` partly (3 fail, 4 pass),
`attack-file` enforced (1 failing), `return-uint32` partly (1 fail, 1 pass), `time-30s` unenforced (1 passing).
No novelty is claimed; `knowledge/tb2-regex-log-grader.md` already executes an agent regex in-process, and the
Prior-art section is an explicit SLOT for `R43ScoutPriorArt` because this seat ran no tracker search.

## Touched surfaces (all outside the lane)

- `$S/lane/` (clone): the four integration files, edited and **staged with `git add` only**; no commit, no other git
  mutation, every git call named `-C "$S/lane"`.
- Build dir: the draft, the patch, four receipts.
- Scratch `$S`: removed at the end (see below).

**Lane state: unwritten.** No file under `/home/vgpnk/Projects/shokunin/kengaku-shokunin` outside
`.ufo/waves/round-43/build/` was created or modified; `corpus/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`
and the jj/Git state of the lane are untouched. The L1 applies `integration.patch`, then runs the gate and counter
on the landing tip; the entry path must be `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` and the
six SOURCES rows must keep tier A / status mined / opened 2026-10-26.

## Known limits

- **Validation is on a clone at a later tip than the freeze**, not on the landing tip. The clone's
  `plans/pkg-spec-r43.json`, `pkg_gate.py`, `feal_probe.py` and receipt are at their freeze digests (P1/P2/P5/V2/V5
  agree), so the instrument identity is checked; the tree is not the final landing tree.
- **P9 was satisfied by staging, not committing.** `git add` in the clone makes the new file tracked; nothing was
  committed anywhere. On the landing tip the L1 must have the file committed for the clean-tree clause to hold for
  the same reason.
- **The gate's `P10` re-runs the probe**, which is a real bwrap execution of the captured grader; both green runs
  reported `probe_rerun=byte-equal bytes=3292`. The probe never pulls the task image, never runs real pytest and
  never runs `tests/test.sh` — these are the entry's own named limits, not new ones.
- **The entry's 12 cases are constructed modules, not agents**, and `cheat-clock-seed` is a host fact
  (`host=libc-rand`); the draft says both.
- **`S134` tier was corrected from my first reading (B) to the frozen assignment's A**; the red receipt is kept so
  the correction is auditable. No other row cell changed after the first run.
- **The Prior-art section is a slot**, deliberately unfilled; this seat ran no tracker search and asserts nothing
  about published reports.

## Artifacts

- `.ufo/waves/round-43/build/R43PkgEntry/tb2-feal-differential-cryptanalysis-grader.md` — the entry draft.
- `.ufo/waves/round-43/build/R43PkgEntry/integration.patch` — the four-file integration (entry, SOURCES, README,
  PROVINCE).
- `.ufo/waves/round-43/build/R43PkgEntry/gate-receipt.txt` — green gate run (`defects=0`).
- `.ufo/waves/round-43/build/R43PkgEntry/gate-receipt-red-p6.txt` — first gate run (`P6 DEFECT … S134: tier='B'`).
- `.ufo/waves/round-43/build/R43PkgEntry/c2-functions-receipt.txt` — `V4 V7 V9 V10` (`defects=0`).
- `.ufo/waves/round-43/build/R43PkgEntry/c2-counter-receipt.txt` — full counter (`checks=10 defects=0`,
  `PREDICATE C2 pass`).

Scratch removed with `python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r43 R43PkgEntry
/fast/scratch/hyaku/kengaku-r43/R43PkgEntry` after the receipts were copied out.

VERDICT: entry-drafted-quotes-18-tags-5/5-case-rows-12/12-mechanism-12/12
