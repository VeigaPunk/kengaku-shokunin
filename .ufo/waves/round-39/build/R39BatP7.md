# R39BatP7 — battery39 module `p7m39`: attributably kills frozen mutant M04 (P7, silence)

Seat: executor, round 39 wave 1. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (untouched outside my report dir).
Scratch `S=/fast/scratch/hyaku/kengaku-r39/R39BatP7` (NVMe, `TMPDIR=$S`), removed at the end of this seat.

## 1. Deliverable

| item | value |
|---|---|
| module | `.ufo/waves/round-39/build/R39BatP7/battery/p7m39.py` (the file the L1 copies to `plans/battery39/`) |
| sha256 | `2c228ba8d4ceeb6f5311be5e8b7df98971e3ac287003b6520aa3e486c0558d2e` |
| stdlib only | yes (`pathlib`-free too — uses only builtins and `ctx`/`ctx.spec`) |
| fids | `p7m39-s105-two-source-lines` (all fids start `p7m39-`) |
| fixtures | 1 (`expect=reject`, `defects=["P7"]`) |
| side-channel tokens | none — `grep -nE '/proc|ppid|cmdline|psutil|environ' p7m39.py` → `sidechannel-tokens: none` (counter agrees: `sidechannel=0`) |
| instruments installed | none (nothing needed; no pacman/`uv tool`/`npx` call made) |

## 2. The mutant and the fixture

M04 (`plans/round39_c1_verify.py` MUTANTS row 4: clause `P7`, direction `silence`, witness
`.ufo/waves/round-38/falsify/F38XMutP/witness-run.txt` W-X15 = `ref_defects=P7,P9 mut_defects=P9`) rewrites the
per-row provenance test at `plans/pkg_gate.py:220`

```python
if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:
```

into a first-element-only test

```python
if (prov.get(sid) or [""])[0] != p.spec["raw_base"] + row["upstream"]:
```

`c_provenance` (`plans/pkg_gate.py:211-234`) builds `prov` by appending **one** URL per `^source: S### ...`
line of the entry, so the unmodified gate rejects a row that carries two `source:` lines while M04 — which reads
only element 0 — accepts it when the pinned URL comes first.

Fixture `p7m39-s105-two-source-lines`: on the genuine round-35 package (`ctx.genuine_package`) it inserts a second
`source: S105 — <raw_base + rows["S107"].upstream> — …` line directly after the single genuine
`source: S105 — <pinned url> — …` line of `corpus/knowledge/tb2-protein-assembly-grader.md` (line 1 of that file),
then stages everything (`ctx.git_add`). Observed: reference `observed_rc=1 observed_defects=P7`; M04 gives `P7 ok`
and rc 0. That is `direction=silence` exactly (`clause in ref[1]`, `clause in declared`, `clause not in mut[1]`).

Deviations from W-X15 worth recording: the witness needed `P9` red in both legs to show the flip. This fixture
stages the tree, so P9 is green and the flip is `{P7}` → `{}` alone — the declared defect set is the exact set the
unmodified gate prints, no incidental second clause.

Why one fixture and not two: any fixture that kills M04 must be a two-`source:`-line row with the pinned URL first
(the other ordering, pinned-after-other, makes the reference and the mutant both print `P7 DEFECT`, so it cannot
kill [INFERENCE: read off the two predicates, not run]). Two killing fixtures would make the load-bearing table
vacuous — deleting one would still leave the other killing — so the module carries exactly the one load-bearing
fixture.

## 3. Evidence — attributed kill (paste of `dev-m04.txt`, the command in the assignment verbatim)

```
$ S=/fast/scratch/hyaku/kengaku-r39/R39BatP7; export TMPDIR="$S"
$ python3 plans/round39_c1_verify.py --lane "$S/lane" \
    --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-39/build/R39BatP7/battery \
    --only M04 --work "$S/w"
PINS total=26 mismatched=0
… (86 pre-existing fixture lines, all `ok`) …
FIXTURE p7m39-s105-two-source-lines expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M04 P7 silence killed by=p7m39-s105-two-source-lines -- a registry row carries exactly one source line, the pinned URL [package-gate row 'SOURCES rows ... against a spec of pinned digests' (indirect: the row names the source, the gate pins its URL)]
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Exit status 0. Full receipt (all 87 `FIXTURE` lines): `.ufo/waves/round-39/build/R39BatP7/dev-m04.txt`
(`grep -cE '^FIXTURE '` → 87).

Every `FIXTURE` line in the run reads `ok`; `wrong=0`, `renamed_disagree=0` (the fixture's clause result survives the
`x…q` directory rename, so it does not depend on the leaf path name), `sidechannel=0`, `null_detected=0` (the
counter's copy of the unmodified gate reproduces the reference result on this fixture).

## 4. Load-bearing table (`.ufo/waves/round-39/build/R39BatP7/loadbearing.txt`)

| battery state | fixtures | M04 |
|---|---|---|
| `p7m39.py` as delivered | 87 | `killed by=p7m39-s105-two-source-lines` |
| same module with `FIXTURES = []` (fixture deleted) | 86 | `SURVIVED exhibits=none` |
| `p7m39.py` file absent from the battery dir | 86 | `SURVIVED exhibits=none` |

```
== fixture removed (FIXTURES = []) ==
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M04 P7 silence SURVIVED exhibits=none -- a registry row carries exactly one source line, the pinned URL …
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
== module file absent ==
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M04 P7 silence SURVIVED exhibits=none -- a registry row carries exactly one source line, the pinned URL …
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
```

The two removal legs both print `exhibits=none`, i.e. no other fixture in batteries 36/37/38 exhibits `P7` silence
against M04 — the kill is this fixture's alone.

## 5. Full default counter with the module landed in the clone's `plans/battery39/`

```
$ cp .ufo/waves/round-39/build/R39BatP7/battery/p7m39.py "$S/lane/plans/battery39/"
$ cd "$S/lane" && python3 plans/round39_c1_verify.py --lane . --work "$S/w"
PINS total=26 mismatched=0
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M01 D5 mirror killed by=d5m-n21-manifest-row-2 -- …
MUTANT M02 P1 silence SURVIVED exhibits=none -- …
MUTANT M03 P3 silence SURVIVED exhibits=none -- …
MUTANT M04 P7 silence killed by=p7m39-s105-two-source-lines -- …
MUTANT M05 RUN rc-silence killed by=p23-p2-receipt-deleted -- …
MUTANT M06 MAIN rc-mirror killed by=r36-P0 -- …
MUTANT M07 D5 mirror SURVIVED exhibits=none -- …
MUTANTS total=7 killed=4 survived=3 invalid=0 null_detected=0
PREDICATE C1 fail
```

Exit status 1. Receipt: `.ufo/waves/round-39/build/R39BatP7/full-run.txt`. This is the expected intermediate state of
wave 1: the do-nothing control was `killed=3 survived=4`, this module moves the count to `killed=4` and the survivor
list to M02, M03, M07 — no other mutant changed state, `invalid=0`, `null_detected=0`, and `PINS mismatched=0`
(the module adds no pinned byte; `plans/battery39` is not in `PINS`).

## 6. Risks, limits, blockers

- **Scope.** This module closes M04 only. M02 (P1 first-instrument-only), M03 (P3 word bound +1) and M07 (D5 markup
  strip) are still `SURVIVED exhibits=none` in the full run above; they belong to other wave-1 seats. C1's frozen
  predicate needs all seven, so the lane cannot land C1 on this module alone.
- **One fixture.** Deliberate (see §2): a second M04-killing fixture would break the load-bearing test rather than
  add coverage. If a reviewer wants redundancy, the alternative killing form is the same pinned URL twice
  (`prov == [u, u]`), which kills identically by the same predicate [INFERENCE from the source; not run].
- **Two-source-line class only.** The fixture demonstrates the "first element" defect, not the `(prov.get(sid) or
  [""])[0]` absent-case (`sid` missing from `prov` at all): an entry with no `S105` source line yields `prov.get →
  None → [""] → [""][0] != pinned` in the mutant as well, so it defects in both legs and cannot kill [INFERENCE,
  not run]. That is a limit of M04's reachability surface, not of this module.
- **Side-channel scan is a heuristic** (frozen claims, §C1 limits): `sidechannel=0` here is a token scan only; the
  module reads nothing but `ctx`, `ctx.spec` and the copied package tree, and spawns nothing.
- **No blockers.** No mutating git command was run in the lane (fixtures git-init their own scratch repos; the
  clone at `$S/lane` got index-only `git add` through the counter's fixtures and one file copy into
  `plans/battery39/`). No pacman / `uv tool` / `npx` transaction was made.

VERDICT: battery39-p7m39-M04-killed-wrong-0
