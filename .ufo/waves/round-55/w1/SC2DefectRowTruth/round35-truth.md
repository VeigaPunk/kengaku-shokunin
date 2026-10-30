# round35-c1-coverage — independent truth for the ledger row

Seat: `SC2DefectRowTruth` — kengaku round 55, wave 1 (v2, build+attack).
Scope: independent re-measurement of the ledger row `round35-c1-coverage`
(`plans/round54-entrytruth.json`), double-run beside E4.
Axis judged: calibration (feeds R55-C2 ledger-truth correction (a)).

## 1. Environment

| item | value |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/kengaku-shokunin` |
| clone (clean, shared) | `/fast/scratch/hyaku/kengaku-r55/SC2DefectRowTruth/clone` |
| clone HEAD | `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (round-55 freeze commit; base tip `798f5e9e…` is its parent) |
| tree state | `git status --porcelain` empty at HEAD (verified) |
| second clone | `/fast/scratch/hyaku/kengaku-r55/SC2DefectRowTruth/oldclone` @ `6e0a1915` (ledger declaration tip) |
| scratch root | `/fast/scratch/hyaku/kengaku-r55/SC2DefectRowTruth/` |

No mutating git/jj command was run anywhere (`clone`/`checkout` of a *read* revision in a
scratch clone only). No lane file was written except the three named outputs under
`.ufo/waves/round-55/w1/SC2DefectRowTruth*/`. No tool installs were needed.

## 2. Command and full captured output

```
$ cd /fast/scratch/hyaku/kengaku-r55/SC2DefectRowTruth/clone
$ git rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r55/SC2DefectRowTruth/clone
$ python3 plans/round35_c1_verify.py --lane .
```

stdout (verbatim, complete):

```
V1 ok
V2 ok
V3 ok
V4 DEFECT knowledge files=58 index rows=58 (want 42/42)
V5 ok
V6 ok
checks=6 defects=1
PREDICATE C1 fail
```

stderr: *(empty — 0 bytes)*

exit code: **1**

Verdict lines are `V1 ok` … `V6 ok` plus the summary `checks=6 defects=1` and
`PREDICATE C1 fail`. Exactly one leg is red: **V4**.

Byte check of the red line (`cat -A`): `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)$`
— no trailing whitespace, no ANSI, LF-terminated.

### Determinism (4 independent runs)

| run | exit | sha256 of combined stdout+stderr |
|---|---|---|
| run1 | 1 | `69d71d195336bdbed46c4260e71ee46b51f986a7baf392ea60f2c9cb9d8d337d` |
| rep1 | 1 | `69d71d195336bdbed46c4260e71ee46b51f986a7baf392ea60f2c9cb9d8d337d` |
| rep2 | 1 | `69d71d195336bdbed46c4260e71ee46b51f986a7baf392ea60f2c9cb9d8d337d` |
| rep3 | 1 | `69d71d195336bdbed46c4260e71ee46b51f986a7baf392ea60f2c9cb9d8d337d` |

Identical bytes every time; no flakiness, no locale/order dependence.

## 3. The fragment a truthful red declaration must carry NOW

Verbatim, copy-paste ready:

```
V4 DEFECT knowledge files=58 index rows=58 (want 42/42)
```

(As one line; the counter prints exactly this string.)

## 4. Delta vs the ledger's declared fragment

Declared in `plans/round54-entrytruth.json`, row `round35-c1-coverage`:

```json
"entry_exit": 1,
"entry_state": "red",
"evidence": "V4 DEFECT knowledge files=57 index rows=57 (want 42/42)"
```

| | declared | observed NOW | delta |
|---|---|---|---|
| fragment | `V4 DEFECT knowledge files=57 index rows=57 (want 42/42)` | `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)` | **both integers 57 → 58** |
| exit | 1 | 1 | none |
| state | red | red | none |

**Precise delta:** exactly two integer tokens change — the knowledge-file count
(`57`→`58`) and the README index-row count (`57`→`58`). The literal tokens `V4 DEFECT`,
`knowledge files=`, `index rows=`, `(want 42/42)` and the red exit/state are unchanged.
Nothing else in the entry's output changed: V1, V2, V3, V5, V6 all still print `ok`, and the
summary lines `checks=6 defects=1` / `PREDICATE C1 fail` are unchanged.

## 5. Root cause (why the declared fragment went stale)

`v4()` in `plans/round35_c1_verify.py` computes
`len(git ls-files corpus/knowledge/*.md)` and `count of README lines starting with "| \`knowledge/"`
and compares both against the frozen constant **42**. The corpus has legitimately grown past
that constant, so the row is permanently red — that part is honest.

The *ledger* was however not re-derived when the counts moved. History of the two counters:

| revision | knowledge files | README index rows |
|---|---|---|
| `6e0a1915` (ledger `round54-entrytruth.json` created — declaration tip) | 57 | 57 |
| `62e9bba5` | 57 | 57 |
| `9a0746be` ("round-54: retain settled wave findings …") | **58** | **58** |
| `16ef40fd` | 58 | 58 |
| `798f5e9e` (round-54 base tip) | 58 | 58 |
| `80afa613` (round-55 freeze, current tip) | 58 | 58 |

`9a0746be` added `corpus/knowledge/external-anchor-freeze.md` plus its one README index row
(`git diff --name-status 9a0746be^ 9a0746be -- corpus/knowledge corpus/README.md` → `A
corpus/knowledge/external-anchor-freeze.md`, `M corpus/README.md`). That commit *did* re-derive
three other ledger rows' evidence (`plans/round54-entrytruth.json` hunks at lines 401, 832,
908) but **not** `round35-c1-coverage` — whose own counter output changed in the same commit.

Confirmed by re-running the entry at the declaration tip `6e0a1915` (clean clone, same
command):

```
V1 ok
V2 ok
V3 ok
V4 DEFECT knowledge files=57 index rows=57 (want 42/42)
V5 ok
V6 ok
checks=6 defects=1
PREDICATE C1 fail
exit 1
```

i.e. the declared fragment was verbatim-correct **at** `6e0a1915` and became stale at
`9a0746be`. The row was never re-measured afterwards.

## 6. Why this breaks the round-55 ledger (calibration consequence)

The entry-truth counters match a red row's declared fragment as a **substring of the entry's
stdout** — `plans/round54_c2_entrytruth.py:338`:

```python
if rc != 0 and sp["entry_state"] == "red" and sp.get("evidence") not in r["out"]:
    evmiss += 1
    lines.append(f"  EVIDENCE-MISSING {r['name']} fragment not in output")
```

The declared string `…files=57 index rows=57…` is **not** a substring of the current output
(`…files=58 index rows=58…`), so as the ledger stands today this row yields
`EVIDENCE-MISSING round35-c1-coverage`. R55-C2's frozen after-predicate requires
`evidence_missing=0`, so the row **must** be corrected (data) before the after-run — that is
exactly the correction R55-C2 clause (a) ("`round35-c1-coverage`'s declared evidence fragment
is re-derived from the entry's actual output at the landing revision and corrected with the
observed output committed").

### Observed corroboration (unchanged r54 counter at the current tip)

`python3 plans/round54_c2_entrytruth.py --lane . --source . --work <scratch> --jobs 6`
on the tip clone — full output (exit 1):

```
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb clean=yes lane_rev_equal=yes
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=78 timeout=0 mismatched=0 evidence_missing=1 laundered=1
TIPSTATE entry_declared_green=62 entry_declared_red=16 observed_green=61 observed_red=17
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
```

`round35-c1-coverage` is the **only** row in the 78-row ledger with `evidence_missing=1` —
the stale fragment is a single-row defect, not a class-wide one. The other two findings in that
output belong to other rounds and are *not* mine: `LAUNDERED round52-c2` (declared green but
the entry exits 1 at this tip — the R55-C1 registry-regression surface) and the
`entry_declared_red=16 / observed_red=17` skew, which is the same `round52-c2` row.
`laundered=1` is the known r54 soundness gap that R55-C2's new binding legs close.

Note the r54 counter's own static legs are clean at this tip (`argv_defect=0`,
`bad_decl=0`, `missing=0`, `extra=0`): the defect is purely the stale *evidence* datum, not a
declaration-shape problem — so the fix is a one-line data correction.

## 7. Landing-revision re-derivation rule (for the L1)

The fragment is *not* a constant — it is a function of the tree. At the measured-after
revision the L1 must regenerate it, not copy `58`:

```
V4 DEFECT knowledge files=<N> index rows=<N> (want 42/42)
```

where `N = git ls-files 'corpus/knowledge/*.md' | wc -l` at the landing revision, **provided**
the count of README lines matching `^| \`knowledge/` equals `N`; if the two differ, the
counter prints both numbers and the fragment must carry both (e.g. `files=59 index rows=60`).

**Prediction [INFERENCE]** for the round-55 landing revision: R55-C3 admits exactly one new
knowledge entry (`corpus/knowledge/tb2-chess-best-move-grader.md`) with exactly one new
`corpus/README.md` knowledge index row, and the other round-55 landings touch only
`plans/`, `LOG.md`, `SCORECARD.md` and corpus rows — so `N = 59` and the fragment would be

```
V4 DEFECT knowledge files=59 index rows=59 (want 42/42)
```

Unverified: no round-55 corpus entry has landed yet in the tree I measured (the wave is
in flight), so the `59` value is a prediction, not a measurement. The L1 should re-run the
entry at the landing revision and commit the *observed* line, exactly as R55-C2 (a) requires.

### Observed transient shape on the live in-flight lane (read-only snapshot)

Running the same command against the live lane tree while round-55 work is in flight
(`--lane /home/vgpnk/Projects/shokunin/kengaku-shokunin`, exit 1) prints:

```
V1 ok
V2 ok
V3 ok
V4 DEFECT knowledge files=58 index rows=59 (want 42/42)
V5 ok
V6 DEFECT census exit 1
checks=6 defects=2
PREDICATE C1 fail
```

Two things to note for the L1:

1. **The two counters come from different sources.** `v4()` counts knowledge files with
   `git ls-files corpus/knowledge/*.md` (**tracked files only**) but counts index rows by
   reading `corpus/README.md` from the **working tree**. At this instant the round-55 README
   index row for `knowledge/tb2-chess-best-move-grader.md` is already present (59 rows) while
   the entry file itself has not landed (58 tracked files) — hence the asymmetric
   `files=58 index rows=59`. At the landing revision, with both committed, they should agree
   again (`59/59`). **The ledger correction must therefore be made against a clean, committed
   landing revision, never against a dirty in-flight tree** — a mid-flight measurement can
   capture the asymmetric shape and bake it into the ledger.
2. `V6 DEFECT census exit 1` in that snapshot is the **live-lane** branch of `v6()` (it
   validates the live lane's `corpus/SOURCES.md`, which other seats are editing in flight),
   not a defect of the round-35 entry. On a clone lane `v6()` validates the clone's own
   registry (`--file`) and prints `V6 ok`. The L1's after-run must be on a clean clone, where
   `V6 ok` and the fragment is the `N/N` shape.

## 8. What was NOT done

- No lane writes: no tracked file in the lane repo was created, modified or deleted; no
  `git add/commit/push/stash/checkout/reset` anywhere; the only lane-repo writes are the three
  named outputs under `.ufo/waves/round-55/w1/`.
- No change to `plans/round35_c1_verify.py`, to `plans/round54-entrytruth.json`, or to any
  registry/registry-adjacent file — the ledger correction is the L1's data edit, not mine.
- No network calls, no benchmark runs, no subagents dispatched.
