# R29a2 — Fixture mutations of the adoption gate (C2 selftest falsification)

Seat: `L1Kengaku29.R29a2FixtureMutations` (leaf). Round 29 attempt 2, hyaku run 6, 2026-10-25.
Object under test: `plans/sources_adopt.py` (C2 standing gate). Detector: `python3 <script> --selftest`
(10 cases, self-contained through `tempfile`, reads no repo file, so it is a clean control).
Scratch: `/tmp/r29a2-FixtureMutations/`. No lane file was created, edited or deleted except this report.

## 0. The file is a live target — two revisions were measured

A sibling seat was editing `plans/sources_adopt.py` while this probe ran. Four hashes were observed
inside one seat (`sha256sum plans/sources_adopt.py`, read-only):

| # | sha256[:12] | note |
|---|---|---|
| rev A | `88535ca2bd03` | bytes this seat started on; `check()` refused any defect globally; no `*_total` keys; case 9 = "a clean package passes" |
| — | `8bc431214fdc` | interim (not measured: observed, superseded) |
| — | `d59f43a16b36` | interim (not measured: observed, superseded) |
| rev B | `505478fdb09c` | **landed bytes, authoritative below**; `check()` scopes refusals by `want_ids`, adds `malformed_total` / `collisions_total` / `duplicates_total` / `prose_recheck[_total]`; case 9 = "a targeted append passes even when an unrequested row is malformed" |

Every run below is a per-revision snapshot; the landed snapshot is
`/tmp/r29a2-FixtureMutations/final-505478fd/` and the file still hashed `505478fd…` after all runs
and after the probes (`cycle.json`, `lane now: 505478fd…`). Verdicts are identical on both
revisions; the *meaning* of survivor 2 changes with the landed scoped-mode rewrite (see F2).

## 1. Baseline (both revisions green — so any FAIL is attributable)

```
rev A ($ python3 pristine/sources_adopt.py --selftest)
SELFTEST cases=10 failed=0        exit 0
rev B ($ python3 final-505478fd/sources_adopt.py --selftest)
SELFTEST cases=10 failed=0        exit 0
```

## 2. Result table — rev B `505478fdb09c` (authoritative)

| # | Mutation (single smallest behavior-bearing edit) | Cases killed | Survivor | Exact selftest summary line |
|---|---|---|---|---|
| M1 | drop the escaped-pipe guard — delete `if "\\\|" in stripped: return None, "escaped-pipe"` (`sources_adopt.py:69-70`) | 1 — `escaped-pipe-refused` | **no** (killed) | `SELFTEST cases=10 failed=1` · exit 1 · `failed: escaped-pipe-refused` |
| M2 | accept a 12-cell row — `if len(cells) != COLUMNS:` → `if len(cells) < COLUMNS:` (`:75`), guard at `:69` left intact | 0 | **YES — survives** | `SELFTEST cases=10 failed=0` · exit 0 |
| M3 | treat any nonempty recheck as valid — `row_defects` recheck clause (`:106-108`) → `if not recheck: defects.append("recheck-empty")` | 0 | **YES — survives** | `SELFTEST cases=10 failed=0` · exit 0 |
| M4 | skip used-by projection — delete `cells[10] = used_by` (`:154`) | 1 — `usedby-projected` | **no** (killed) | `SELFTEST cases=10 failed=1` · exit 1 · `failed: usedby-projected` |
| M5 | return `EXIT_OK` when collisions exist — delete the trailing `if clash: return EXIT_COLLISION, report` (`:211-212`) | 3 — `collision-zero-indent`, `collision-one-space`, `collision-three-space` | **no** (killed) | `SELFTEST cases=10 failed=3` · exit 1 · `failed: collision-zero-indent collision-one-space collision-three-space` |

Same five mutations on rev A `88535ca2bd03` (M5 anchored on the pre-rewrite shape
`if bad or dupes or defects or clash: code = EXIT_COLLISION if clash else EXIT_MALFORMED`):
M1 `failed=1` (`escaped-pipe-refused`), M2 `failed=0` **survivor**, M3 `failed=0` **survivor**,
M4 `failed=1` (`usedby-projected`), M5 `failed=3` (the three collision cases). Identical verdicts.

Case matrix, rev B (`·` PASS, `X` FAIL):

| case | M1 | M2 | M3 | M4 | M5 |
|---|---|---|---|---|---|
| collision-zero-indent | · | · | · | · | X |
| collision-one-space | · | · | · | · | X |
| collision-three-space | · | · | · | · | X |
| four-space-not-a-row | · | · | · | · | · |
| escaped-pipe-refused | X | · | · | · | · |
| prose-recheck-normalized | · | · | · | · | · |
| usedby-projected | · | · | · | X | · |
| duplicate-staged-id | · | · | · | · | · |
| clean-package-passes | · | · | · | · | · |
| missing-requested-id | · | · | · | · | · |

Raw stdout: `final-505478fd/runs/M{1..5}.out` (rev B), `runs/M{1..5}.out` (rev A).
Mutant sources: `final-505478fd/runs/M{1..5}.py`, `runs/M{1..5}.py`.

## 3. SURVIVOR 1 (M2) — the column-count clause has no test; a 12-cell row is accepted and lands in the registry

The only 12-cell row any fixture produces is the escaped pipe, and that is refused one clause
earlier at `:69`. Nothing feeds `split_cells` a 12-cell row from any other route, so weakening
`!=` to `<` at `:75` is invisible to all ten cases.

Probe, fixture = `GOOD_ROW` with one whole extra cell appended before the closing pipe
(12 cells, **no** backslash-pipe) — `probes-final.json` key `A:*`:

```
pristine : code 4  staged 0  malformed ['S900:columns=12']  malformed_total 1
M2       : code 0  staged 1  malformed []                   malformed_total 0      <-- accepted
M2 build_block -> 12 columns emitted:
  | S900 | fixture source — … | docs | A | fixture scope | anchor text | fixture teaches | mined |
    2026-10-23 | 180d | corpus/knowledge/new.md | extra-cell |
M2 on the escaped-pipe row : code 4  malformed ['S900:escaped-pipe']   (guard still holds)
```

Not merely a missed refusal: `check()` false-greens and `build_block` then writes a 12-column row
into `corpus/SOURCES.md` against `COLUMNS = 11` and C2 clause 2 ("exactly 11 columns"). Real
trigger: any unescaped `|` typed inside a cell (a `a|b` alternation, a pipe inside a title, a URL
fragment). `prose_recheck_total` (`:183`) also calls `row_defects` on a 12-cell row, so the
defect-indexing shifts silently.
Kill: one case staging a 12-cell row with no `\|` and expecting `EXIT_MALFORMED` with
`malformed == ["S900:columns=12"]`.

## 4. SURVIVOR 2 (M3) — the recheck schema check has no case, and on the landed bytes the prose counter is its only observable

No fixture reaches `check()` with an invalid nonempty recheck: every staged row in cases 1-5, 8-10
uses `180d`, and the prose row is handed straight to `build_block` in cases 6-7, never through
`check()`. The recheck clause at `:106-108` is therefore untested in both revisions.

Probe with `recheck = banana` (nonempty, garbage) — `probes-final.json` key `B:*`:

```
rev B pristine, unscoped          : code 4  defects {'S900': ['recheck-prose']}  prose_total 1
rev B pristine, scoped want=[S900]: code 0  defects {}   prose_total 1  prose_scoped 1
rev B M3,       unscoped          : code 0  defects {}   prose_total 0                 <-- refusal gone
rev B M3,       scoped            : code 0  defects {}   prose_total 0  prose_scoped 0  <-- counter gone
same shape for the prose row ('2026-10-23 — re-verify at next release')
```

Why this matters on the landed bytes: the sibling rewrite made scoped mode *deliberately* stop
refusing `recheck-prose` (`:193-201`) on the grounds that `build_block` normalizes it. That leaves
`prose_recheck_total` / `prose_recheck` (`:183`, `:200-201`) as the **only** signal an operator
gets, and it fires for any non-ISO, non-cadence, non-symbolic value — garbage included. M3 zeroes
that counter: a row with `recheck = banana` then passes with no flag, and `build_block` silently
stamps `2026-10-25` into `recheck`. So the mutant is not cosmetic — it deletes the sole
observability of a normalization that the landed design chose to allow.
On rev A the same mutant removed a refusal that was then load-bearing (unscoped prose → exit 4
became exit 0) and additionally exposed that the rev A prose-normalization branch (`build_block`)
was unreachable from `main()`, since `check()` refused prose before `build_block` ran. The landed
rewrite fixes that reachability for scoped mode.

Kill: one case calling `check()` on a package whose requested row has `recheck = banana` and
asserting either the custom-mode refusal or `prose_recheck == 1` — the landed semantics want the
latter (the counter, not an exit code).

## 5. Secondary observation (M1 is killed on the message only)

```
pristine : code 4  malformed ['S900:escaped-pipe']
M1       : code 4  malformed ['S900:columns=12']
```

`escaped-pipe-refused` (`:306`) asserts the diagnostic string, so M1 dies on that string while the
escaped-pipe row is still refused by the column clause. The guard is defense-in-depth, not the
load-bearing refusal — worth knowing, because it is exactly what leaves SURVIVOR 1 uncovered: the
two clauses jointly cover only the `\|` variant of the 12-cell failure.

## 6. Observation on the landed refusal surface vs C2 clause 4 (not judged, reported)

`check()` now scopes every refusal to `want_ids` (`:184-207`), and the landed case 9 encodes that
an unrequested escaped-pipe row must not fail the run:

```
package = good S008 + escaped-pipe S011, registry = header
unscoped          -> exit 4  malformed ['S011:escaped-pipe']  malformed_total 1
scoped want=S008  -> exit 0  malformed []                     malformed_total 1   (case 9 asserts this)
scoped want=S011  -> exit 4  malformed ['S011:escaped-pipe']  malformed_total 1
```

C2 clause 4 as frozen says "refusal with a non-zero exit for a missing requested id, an escaped
pipe, a duplicate staged id, or a nonempty collision set", with no scoping qualifier. The landed
gate refuses an escaped pipe only when the row is requested. That may be the intended reading
("only the rows this round appends are under test", `:185-187`), but the frozen claim text does not
say it, and case 9 now asserts the weaker behavior. Flagging for the L1, not adjudicating.

## 7. Coverage gaps, priority order

1. 12-cell row with no `\|` (kills M2); also an unescaped `|` inside a cell value.
2. `check()` on a requested row with an invalid recheck (`banana`): asserts either refusal or
   `prose_recheck == 1` (kills M3 under landed semantics).
3. A `check()` → `build_block` composition on a non-prose requested row (binds the schema result to
   the emitted block; cases 6-7 bypass `check()` entirely, cases 9-10 never call `build_block`).
4. `row_defects` sub-clauses with no fixtured instance in either revision: `status` outside
   `STATUSES`, empty `recheck`, empty `source` (cell 1).
5. `four-space-not-a-row` asserts `staged == 0` but never asserts the 4-space row is reported
   anywhere, so a silently dropped row and a correctly excluded row are indistinguishable.

## 8. Restoration evidence

Rev B `505478fd…` — mutate → run → restore from the snapshot bytes → re-run (`final-505478fd/cycle.json`):

| mutant | mutant sha256[:12] | restored sha256[:12] | restored == pristine | mutated run | restored run |
|---|---|---|---|---|---|
| M1 | `ad37b36f6554` | `505478fdb09c` | yes | exit 1, `failed=1` | exit 0, `failed=0` |
| M2 | `428337ad7e8e` | `505478fdb09c` | yes | exit 0, `failed=0` | exit 0, `failed=0` |
| M3 | `7047a8b7a3a6` | `505478fdb09c` | yes | exit 0, `failed=0` | exit 0, `failed=0` |
| M4 | `b18063c73258` | `505478fdb09c` | yes | exit 1, `failed=1` | exit 0, `failed=0` |
| M5 | `d91813aaf67e` | `505478fdb09c` | yes | exit 1, `failed=3` | exit 0, `failed=0` |

Rev A `88535ca2…` — same cycle (`cycle.json` at scratch root): M1 `9e41faee2a80`, M2
`a92340437cd0`, M3 `8998c2dbb68e`, M4 `4e33bd6338f4`, M5 `6d932cf81034`; every restore hashed back
to `88535ca2bd03` and re-ran `SELFTEST cases=10 failed=0`.
Lane integrity after the whole seat: `plans/sources_adopt.py` hashed `505478fd…`, i.e. bytes only
moved by siblings, never by this seat.

## 9. Bounds / tooling

- Leaf seat: no subagents, no background jobs, no `ask`, no campaign tool under `shokuknow`.
- No production edits: this report is the only write inside the lane; all scratch is
  `/tmp/r29a2-FixtureMutations/`; files under the lane were only read (and `git status`/`diff`
  inspected read-only).
- No installs or upgrades — Python 3.14.8 was sufficient; `pacman` unused, nothing to record for
  the tooling directive.
- Self-contained evidence: every baseline line, per-mutant summary line, probe output and restore
  hash needed to re-check this report is quoted inline above. The `/tmp/r29a2-FixtureMutations/`
  paths are provenance only — if that scratch directory is relocated or swept (scratch trees under
  `.ufo/waves/*/` moved once during this session), this report still carries its own
  evidence; the mutants are reproducible by applying the one-line edits quoted in the table to
  `plans/sources_adopt.py` at `505478fdb09c…`.
- As the assignment names: not judged here whether C2's "ten PASS" target is met, nor whether the
  landed scoping rewrite is the right reading of clause 4; this seat reports 3 of 5 targeted
  defects killed, 2 survivors (M2 and M3), with the exact case counts and the outputs above.
