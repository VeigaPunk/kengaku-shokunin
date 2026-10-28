# C1RevClaimsFreeze — round 52 claims freeze review

## Verdicts

- **R52-C1: unsound as a claim of independently verified, source-authentic novelty.** The current A2 counter fixes the unsatisfiable capture count and broken prior-read extraction found in the earlier counter, but the predicate still accepts a fully fabricated evidence set (demonstrated below). It checks self-authored checksums, not that captures equal the pinned upstream bytes; the confirmation and prior-art receipts also lack independent-authorship/fetch checks. The cited “independent second reader” and “fetched public primaries” are therefore not established by the frozen predicate.
- **R52-C2: unsound as the stated claim that every advertised instrument has a truthful registry row.** The predicate accepts filler rows without validating their verdict map, pinned values, scope, or self-test behavior; it also omits four existing advertised evidence scripts because its path regex excludes hyphenated directory names, although the frozen universe definition does not.

The two claims are **not strictly causally independent**: C2 scans `corpus/knowledge/*.md` for advertised commands, while C1's required sourced-claim deliverable may write a knowledge entry/round record containing a C1 command. That can add an advertised path C2 must register. The stated predicate separation (C1 does not read SKILL.md's registry; C2 does not read grader captures) is true, but it is insufficient to establish independence of the final-tree predicates.

## Findings by severity

### High — C1 can pass on fabricated captures and receipts

**Evidence.** The current counter reads capture paths from `capture_population` and compares each captured file's digest to `corpus/evidence/round52/graders/SHA256SUMS` (`plans/round52_c1_grader_audit.py`, `collect`). The frozen population JSON contains paths and counts but no expected per-file digest (`plans/round52-tasks.json`; keys observed: `pin`, `repo`, `task_count`, `grader_files`, `tasks`, `capture_population`, `capture_file_count`). Thus the checksum file is self-authored alongside the captures and is not an upstream authenticity anchor.

I built a scratch-only tree containing **184 synthetic capture files** with synthetic `test_outputs.py` content, generated matching SHA256SUMS, and hand-wrote two confirmation rows for candidate tasks `adaptive-rejection-sampler` and `bn-fit-modify` (quote copied from the synthetic bytes, reader set to `independent-second-reader`, confirmed=true). I then hand-wrote `prior-art.md` containing three `example.org` URLs and ran the current counter against that fixture. It printed `CAPTURES expected=184 present=184 mismatched=0`, `CONFIRMED new=2`, `PRIOR-ART ok=True urls=3`, and **`PREDICATE R52-C1 pass`**. The synthetic tasks are not in the corrected 12-task read set. No upstream grader bytes, independent second reader, or fetched public source were used. The predicate did not catch the attack.

The A1 quote check only requires a truthy string to occur as a substring of the captured bytes; `reader` and `confirmed` are merely truthy fields. `prior_art()` only counts three distinct URL strings. It does not verify fetch receipts, public-primary status, per-finding pricing, or phenomenon-known/new labels. The frozen score rule's novelty promotion is thus not mechanically supported by the prior-art predicate.

**Smallest amendments:** pin each expected digest (or upstream blob identity plus verified content digest) in the frozen population before collection and compare every capture to that independent pin; require confirmation receipts to resolve to an independently authored reader artifact/identity and a substantive located quote; require prior-art rows to cite verifiable fetched-primary receipts and explicitly price each confirmed finding. Do not treat a checksum file written with the captures as source authenticity.

### High — C2 passes with non-truthful registry rows

**Evidence.** In a scratch copy, I added 28 rows for the frozen `MISSING 28` paths. Each had the exact `python3 plans/<path>.py` entry but filler values (`unverified` in the descriptive cells and `none declared` for self-test). I changed the pre-existing `order-check` self-test cell to `none declared` to clear its separately counted base defect. The current C2 counter returned:

```
ADVERTISED total=72
REGISTERED total=72 rows=74
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
PREDICATE R52-C2 pass
```

So the predicate catches blank cells, missing entry files, and one narrow textual self-test case; it does **not** check whether a verdict map, pinned-values cell, write-scope claim, or self-test assertion is true. `INCOMPLETE` is only `not all(cells)`, and “none declared” bypasses self-test checking by design. The frozen after-counts therefore do not prove the promised “truthful row” or that a stranger can tell how to exercise the instrument.

**Smallest amendment:** either narrow the claim to non-empty inventory rows, or add independently re-derivable checks for the relevant registry facts (at minimum execute the declared self-test and validate its exit/finding; validate the verdict map and pinned-value reference against the instrument's committed behavior). Require concrete, resolvable “no self-test” evidence rather than accepting that phrase as an unchecked escape hatch.

### High — C2's enumerator omits four paths in its frozen advertised universe

The claim defines `corpus/evidence/<dir>/<name>.py` without restricting `<dir>` to alphanumerics/underscores. The counter's `CMD` regex instead requires `[A-Za-z0-9_]+` for that directory, excluding hyphenated directories. I found four existing scripts literally advertised as `python3 <path>` in the named source files, but excluded by that regex:

- `corpus/evidence/round9-fleet/test_harness.py` — `SCORECARD.md:74`
- `corpus/evidence/round11-power/recompute_r11.py` — `corpus/knowledge/bench-arena-round11-power.md:100`
- `corpus/evidence/round12-ladder/recompute_r12.py` — `corpus/knowledge/bench-arena-round12-ladder.md:186` (also repeated at 196, 253–254)
- `corpus/evidence/round13-coverage/coverage_census.py` — `SKILL.md:565`

Using the written scope (existing paths of the stated forms appearing as `python3 <path>` in the named files) yielded **76** paths; the counter reports **72**. Whether or not individual rows happen to exist, the predicate cannot establish the universal “every advertised instrument” claim for these four paths. The attack is not caught.

**Smallest amendment:** broaden the regex to admit the path characters allowed by the frozen universe (including `-`), then freeze or print the enumerated path list and require exact coverage. Alternatively freeze the universe explicitly at the base tip and use that list for both controls and after-run.

### Medium — C1/C2 final-tree coupling and moving C2 denominator

C1's round deliverables include a sourced knowledge entry; C2 scans every `corpus/knowledge/*.md` file plus `LOG.md`, `SCORECARD.md`, and `SKILL.md` for advertised commands. A C1 entry/round record that advertises `python3 plans/round52_c1_grader_audit.py` (or another new script) changes C2's `ADVERTISED` set and requires another row. Thus the exact 28-item base missing set is not the final universe, and C2's final verdict can depend on C1's documentation choices. The current after target `MISSING 0` can accommodate new rows, but the claims' “each verifies without the other having landed” is not guaranteed by the predicates as written.

**Smallest amendment:** freeze the complete base advertised path set in a committed manifest, require all those paths remain represented, and state whether newly advertised round-52 instruments are included in the same C2 target. This makes the cross-claim dependency explicit and measurable.

### Medium — control set did not track A1's revised candidate definition

A1 changes candidates to include tasks with a per-test `P1`, while the frozen blind-class control still says “force every task to `V0`.” The counter's candidate value is now `bool(p1) or cls in (V1,V4)`. If the control only forces the file-level class to V0 while leaving per-test classification intact, P1 candidates remain, and confirmations may still satisfy the threshold; the control is not guaranteed to fail as specified.

**Smallest amendment:** define the blind-class mutation against the post-A1 predicate (force every task's candidate flag false / every per-test class to non-P1), and assert that `CONFIRMED new=0`.

### Freeze/revision note — A1/A2 were appended after wave-1 dispatch

The current worktree has `HEAD=07ea2084053f5112ea797a653e6a3a96e8cf4a64` (A1) and uncommitted changes to `plans/round-52-claims.md` and `plans/round52_c1_grader_audit.py` (A2). A1 changes the classification unit and confirmation predicate after the freeze commit and after wave-1 dispatch; A2 records corrections to the C1 implementation. Both are disclosed and pre-scored, but a wave-1 report based on the original dispatch cannot silently be treated as having reviewed A1/A2. The prior committed counter also had the defects A2 identifies: with 184 files present it reported `present=89`, and its read-task parser returned only `{'0','this'}`. A2 fixes those two counter defects in the current working tree; I do **not** count them as remaining defects in the current A2 implementation. The initial C1 before receipt also predates A1's extra `TESTCLASS` output, so it is not byte-identical to the current command output.

A1/A2 are append-only disclosures, but the reviewer should score against the exact version supplied to the seat and identify any post-dispatch rule change. The current report evaluates the current visible A1/A2 text and counter, with the pre-A2 measurements identified as historical.

## Contract checks

- **Concrete/re-derivable after-state:** C1's numeric predicate and C2's four zero counts are executable values. However, C1's source authenticity, independent reading, and prior-art semantics are not re-derived by its counter; C2's truthfulness is not re-derived by its counter.
- **Do-nothing controls:** the base controls fail (`C2` currently reports `MISSING 28` and `SELFTEST-UNBACKED 1`; the pre-A2 C1 base run reported no captures and no confirmations). But these negatives do not prevent the passing attacks above. C1's earlier `c1-control-drop-capture` expected signature (`present=183 mismatched=1`) did not match the pre-A2 counter (`present` maxed at 89 and deletion did not increment mismatch); A2 corrected the capture enumeration, but controls should be replayed against the amended counter. The A1 blind-class control needs the amendment described above.
- **Universal clauses:** C1's A2 code now enumerates `capture_population` and checks every listed path/digest against SHA256SUMS, but it does not anchor those digests to upstream bytes. C2's universe is explicitly described and scanned, but its regex omits the four paths above.
- **Axis claims:** the two claims target distinct axes (novelty and operability), so the axis targets are distinct. The claims file's base score/lowest-band rationale is not independently re-derived in this review.
- **Protocol reference:** `PROTOCOL.md` has no numbered “§9” heading. I applied its `## Round-robin rounds`, `## Gate standard`, and `## Fleet-2 conventions (adopted)` clauses, including falsifiable before→after measurements and registry evidence.

## Commands and measurements

Commands/actions exercised:

1. Read `plans/round-52-claims.md` in full, then relevant ranges of `plans/round52_c1_grader_audit.py`, `plans/round52_c2_registry.py`, `plans/round52-tasks.json`, `SKILL.md`, `SCORECARD.md`, and PROTOCOL sections above.
2. `git log -3 --format='%H %ci %s'`; `git status --porcelain`; `git diff HEAD -- plans/round-52-claims.md plans/round52_c1_grader_audit.py` — observed A1 at `07ea208`; A2 is a worktree modification at review time.
3. `python3 -c` inspection of `round52-tasks.json`: `capture_file_count=184`, unique `capture_population` paths `=184`, no per-file `sha256` fields.
4. `ls corpus/knowledge/tb2-*-grader.md | wc -l` → **12**.
5. `python3 plans/round52_c2_registry.py --lane .` → `ADVERTISED 72`, `REGISTERED 44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1`.
6. Scratch-only synthetic C1 experiment: materialized a lane copy with `git archive HEAD`, wrote 184 synthetic capture files plus matching SHA256SUMS, wrote two synthetic confirmations and three `example.org` URLs, then ran `python3 plans/round52_c1_grader_audit.py --lane /fast/scratch/hyaku/kengaku-r52/C1RevClaimsFreeze/c1sat` → **`PREDICATE R52-C1 pass`**.
7. Scratch-only C2 experiment: materialized a lane copy with `git archive HEAD`, added 28 nonempty filler rows, changed the existing `order-check` self-test cell to `none declared`, then ran `python3 plans/round52_c2_registry.py --lane /fast/scratch/hyaku/kengaku-r52/C1RevClaimsFreeze/c2filler` → **`PREDICATE R52-C2 pass`** with the counts shown above.
8. `curl -sS -o /dev/null -w '%{http_code}\n' https://api.github.com/repos/harbor-framework/terminal-bench-2` → **403**; I could not independently fetch the pinned upstream tree from this host.

No tools were installed or updated. No lane-tree files were edited by this reviewer. Scratch fixtures were under `/fast/scratch/hyaku/kengaku-r52/C1RevClaimsFreeze/` and removed before yield. No LSP device/server was available in the tool inventory; source review used `read` and executable counter results, not grep as semantic proof.