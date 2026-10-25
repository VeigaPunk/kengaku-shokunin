# R30RevDefects — D1/D2/D3/D5 repairs vs the routed wording

role: reviewer (calibration), round 30, leaf seat
lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin
sources of the routed wording: `corpus/lessons/round-29-verifier-spotcheck.md` §5 (read in full);
`plans/round-30-claims.md` §C2 (frozen predicate + kill rule)
wrote: this file only. scratch: `/tmp/r30-R30RevDefects/pre` (pre-append `git archive` tree).
production bytes: none touched.

## 0. The repairs file named in the ticket does not exist

`/tmp/r30-DefectFix/repairs.md` is **absent** (`read` → "Path not found"; `ls /tmp/r30-DefectFix/` →
"No such file or directory"). Verdicts below are therefore derived from the lane's working-tree
repair bytes, hashed and timestamped, not from a seat-authored repair note.

Reviewed revision (the tree is in flight — the D2/D3 owner rewrote the lesson twice while this seat
was reading it: 04:22:13 (`d3b58d9d…07c4`) then `3a0ab556…ee1d4`; verdicts below are on the latest,
and I re-ran every check against it):

| file | mtime | sha256 |
|---|---|---|
| `corpus/lessons/round-29.md` (D2, D3) | 2026-10-25 04:2x | `3a0ab556612f868fbcf57c8b9e4212b9cfa3d7966d1b7a9599ec8351778ee1d4` |
| `.ufo/waves/round-29/attempt2/adoption-expect.json` (D5) | 2026-10-25 04:21:49 | `619feca30b7845de743fc144fb613e2c79f688cca032903b137c2d6addae06b5` |
| `corpus/evidence/round29-attempt2/control-nothing.txt` (D1) | 2026-10-25 04:21:33 | `4b478db43d6f69d7447298db7103e37bb1a8b8109c5efff426d9a943dc18e4bd` |

`git status --porcelain` at review: ` M .ufo/waves/round-29/attempt2/adoption-expect.json`,
` M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md`, ` M corpus/lessons/round-29.md`,
`?? .ufo/waves/round-30/`, `?? corpus/evidence/round29-attempt2/control-nothing.txt`.
`python3 plans/round30_defects.py --lane .` → `ok D1 … ok D2 … ok D3 … DEFECT D4
uncommitted-wave-evidence: .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md is uncommitted …`,
`defects=1`, exit 1. (D4 is outside this seat's four items; recorded as the tree state the counter
reports.)

## 1. Per-item verdicts

### D1 — receipt-at-cited-path: **ADJACENT** (pointer half answered, quoted-bytes half recorded instead of repaired)

Routed wording it had to meet (spotcheck §5, verbatim):

> **D1** `.ufo/reports/round-29/kengaku.md` cites
> `corpus/evidence/round29-attempt2/control-nothing.txt` twice; no such path is committed. The bytes
> are at `.ufo/waves/round-29/attempt2/control.nothing.txt` (which also carries `verified_at=0`, a
> field the report's quoted line omits). Commit the receipt under the cited name or cite the wave
> path.

The cited report text (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/kengaku.md:122-124`, fleet
repo, read-only):

> `- **Before (control, committed at freeze `8c14a5d`):** `entries=0 indexed=0 cited_rows=0
>   rows_present=0 rows_mined=0 usedby_ok=0 census=skipped` — exit 1
>   (`corpus/evidence/round29-attempt2/control-nothing.txt`, `.ufo/waves/round-29/attempt2/control.nothing.txt`).`

What the repair did: created `corpus/evidence/round29-attempt2/control-nothing.txt` as a 9-line file —
a five-line provenance header plus the **wave receipt's 8-field line** and `exit=1`:

```
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 verified_at=0 census=skipped
```

Byte test against the quoted line (the assignment's bar: *make that path exist with the quoted bytes*):

```
report 7-field line in new file: False
report 7-field line in wave file: False
wave 8-field line in new file: True
```

So the cited path now exists and the counter's weak check passes, but it does **not** carry the
report's quoted bytes. `verified_at=0` is spliced between `usedby_ok=0` and `census=skipped`, so the
report's quoted sequence is not a substring of the receipt — exactly the mismatch D1's parenthetical
named. The repair's own header records that instead of resolving it ("the report quoted this line
without the `verified_at=0` field the wave file carries. Both fields are kept below; the quoted prefix
… is unchanged"), which is the "record that the path/quote was wrong" behaviour the bar excludes.

Two further facts make the chosen branch the wrong one, not a forced one:

1. **The quoted bytes are producible, and the current tool produces exactly them.** The M99 row
   (`corpus/lessons/round-29.md:169`) states the repair: "`adoption_check.py` now prints exactly the
   frozen seven fields and keeps `verified-at` as an unprinted gating condition". Code agrees:
   `plans/adoption_check.py:114-119` prints seven fields; `verified_at_ok` is only a gating variable
   (`:126`). An 8-field line is **not producible by the shipped counter at all** — the receipt planted
   at the cited path is pre-M99 output.
2. **I reproduced the report's quoted line today**, without touching the lane, from a pre-append tree
   extracted to scratch:
   `git archive 1f3b0f1ec41ec297130e8944ff97968d32324632 | tar -x -C /tmp/r30-R30RevDefects/pre`
   then
   `python3 plans/adoption_check.py --lane /tmp/r30-R30RevDefects/pre --expect .ufo/waves/round-29/attempt2/adoption-expect.json`
   → `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped`,
   `exit=1`. That is the report's quoted line, byte for byte, with the citation's own directory holding
   it. The defect's option (a) was satisfiable with the quoted bytes; the repair picked the stale
   capture instead.

3. **The before/after pair is now non-comparable inside one directory.**
   `corpus/evidence/round29-attempt2/adoption-measured.txt` (the report's *after* line) is 7 fields
   (`entries=1 … usedby_ok=1 census=ok`); the new `control-nothing.txt` beside it is 8. M99 asserts the
   counter run and the frozen line are "byte-comparable in
   `corpus/evidence/round29-attempt2/adoption-measured.txt`"; the planted control breaks that pairing.

4. **Not committed.** D1 says "Commit the receipt under the cited name"; the file is `??`
   (untracked) at review. `check_d1` (`plans/round30_defects.py`) tests `path.is_file()`,
   `"entries=0"`, `"exit=1"` — a string proxy that cannot see a missing commit (D4's check is the only
   one that consults `git status`), cannot see the field set, and passes on a receipt whose line
   disagrees with the report it is cited from.

**Verdict: adjacent.** It discharges "no such path is committed" (existence) and keeps the `exit=1`
line; it does not discharge "with the quoted bytes" and it does not commit. A conforming repair is
either (a) the seven-field line above (reproduced at a pinned pre-append rev, provenance header naming
the rev), with the frozen 8-field capture kept as the *wave* artifact it is; or (b) the report's other
allowed route — cite the wave path and drop the quoted 7-field rendering in favour of the captured
8-field one. As shipped, the counter prints `ok D1` while the citation still does not reproduce.

### D2 — kappa-sweep scope: **ANSWERS** (rev drift fixed in flight; one residual imprecision)

Routed wording: "renders the kappa sweep as '0 hits **in the lane**'; the scan's own command is
`corpus/knowledge/*.md`, and a lane-wide grep finds 65 files. Narrow the sentence to the scope the
command measured."

Current bytes (`corpus/lessons/round-29.md:231-236`, hash `3a0ab556…`):

> `point duplicates `knowledge/llm-judge-calibration.md:7-13`. The only new items are per-variable`
> `kappa and a test–retest ceiling — `grep -rn kappa corpus/knowledge/*.md` → 0 hits at the scope`
> `that command measured, while a lane-wide `git grep -li kappa` (corpus/knowledge/*.md included)`
> `finds 65 files at the round-29 tip `2ff4b6f` and 66 at round 30 — the extra file is`
> `corpus/lessons/round-29-verifier-spotcheck.md` itself. Routed defect D2,`
> `` `corpus/lessons/round-29-verifier-spotcheck.md` §5. ``

Checks I ran against these bytes:

| check | result |
|---|---|
| `grep -rn 'kappa' corpus/knowledge/*.md \| wc -l` | `0` — the narrowed scope is stated and holds |
| `git grep -li kappa 2ff4b6f -- . \| wc -l` | `65` — reproduces exactly as the lesson now records it |
| `git grep -li kappa HEAD -- . \| wc -l` | `66` — reproduces |
| set difference of those two lists | **one** added path: `corpus/lessons/round-29-verifier-spotcheck.md` — the lesson's attribution of the 66th file is correct |
| `"in the lane"` on any kappa line | gone; every kappa line names `corpus/knowledge/*.md`, so `check_d2` is satisfied for the right reason, not by phrasing |
| kappa in the inter-rater sense outside scratch (`git grep -E 'kappa[^a-z]*(score\|agreement\|coefficient\|reliab\|inter-rater)'`) | no hits — the finding ("only per-variable kappa and a test–retest ceiling are new") survives the narrowing |

The narrowing is honest, the finding is kept, and the recorded command is runnable and reproduces. Note
the seat repaired my first objection **between my two reads**: the version at `d3b58d9d…` said only
"finds 65 files", which was already 66 at tip; `3a0ab556…` pins both revs and names the added file, and
I verified that attribution. **D2 answers the defect as worded.**

One residual imprecision (advisory, not routed): 54 of the 66 hits are round-28 scratch clones of the
same round-12 evidence — excluding `.ufo/waves/round-28/scratch/`, the population is **12 files at HEAD
(11 at `2ff4b6f`)**: `corpus/evidence/round12-ladder/{probe_plan_r12.md,probe_r12.py,recompute_r12.py,results-r12.jsonl}`,
`corpus/evidence/round12-fleet/{grader_r12_draft.py,recompute_r12_draft.py}`, `grader.py`,
`plans/fixtures/r26/perturb_cases.jsonl`, `.ufo/waves/round-26/build/SrcLetMeSpeakFreely.md`,
`.ufo/waves/round-29/attempt2/build/R29a2RejectScan.md`, plus the two lessons. A reader who takes "65
files" as prevalence is reading ~6× the distinct corpus. Content check stands: those files use `kappa`
as a Greek-letter token — `grader.py:4260` `TOKENS = ["alpha", … "kappa" …]`, `probe_r12.py:316`
`TOKVOCAB = […]`, `results-r12.jsonl` cells with `"kappa"` in `init`/ops, `probe_plan_r12.md:78` quoting
the vocab list — never the agreement statistic. The gloss the seat dropped in the rewrite ("mostly the
round-12 Greek-letter token vocabulary") was true; its absence leaves the inflated number unexplained.

### D3 — S078 line-75 word count: **ANSWERS** (exact, minimal, non-cosmetic)

Routed wording: "§Sources opened this round prices S078's line-75 quote at 9 words; the row and the
registry say 8, and 8 is correct. Correct the table cell."

Diff is one table cell, `9 words` → `8 words`, on the line-75 quote; the quote text, the line-99 quote,
the GATE.md sentence and the sha256/byte cells are untouched (`git diff -U1 -- corpus/lessons/round-29.md`
shows a single-character-class change on that row). Independent re-derivations:

- `len("The verifier never runs in the agent's sandbox.".split())` → 8 (`The, verifier, never, runs, in, the, agent's, sandbox.`).
- `git show HEAD:corpus/SOURCES.md | grep '^| S078'` → anchor cell prices both quotes `(8 words)`;
  registry was already right, so the repair changed only the surface that was wrong — no registry
  rewrite, no quote edit.
- The counter agrees: `ok D3 s078-line75-word-count: repaired`; `check_d3` derives the count with
  `words()` on both the registry and lesson surfaces rather than trusting either cell.

**Verdict: answers.** This is the one routed item where the repair is exactly the defect and nothing
else. Not cosmetic: the pre-repair cell asserted a false count against its own registry row.

### D5 — S091 `used-by` asymmetry: **ANSWERS via the route the defect names** (documentation-only, as permitted)

Routed wording: "S091 is `used-by` the entry in `SOURCES.md`, but the entry's `source:` block does not
cite it, so the frozen counter cannot see the relation the registry asserts. **Either** cite it in the
entry's prior-art section as a source, **or** record the asymmetry in `adoption-expect.json`."

Repair chose the second route: a new `usedby_notes.S091` string key (the only diff hunk, `+4` lines).
Facts the note asserts, each re-derived:

| note's claim | verification |
|---|---|
| "SOURCES.md carries S091 used-by corpus/knowledge/benchmark-task-validity-checklist.md" | `corpus/SOURCES.md:106` cell 11 = `corpus/lessons/round-29.md, corpus/knowledge/benchmark-task-validity-checklist.md` — true |
| "that entry quotes S091 in its Prior art section" | `benchmark-task-validity-checklist.md:103-111`: "The Agentic Benchmark Checklist (ABC, arXiv 2507.02825 …)" with the located quote, "The pricing row is S091 and the located quote, anchor and rejection reasoning live in `corpus/lessons/round-29.md` §Attempt 2"; also `:25` "S091 (ABC) is the one independent third-party instrument here" — true |
| "deliberately does not carry a `source: S091` line" | the entry's five `source:` lines are S077, S078, S079, S080, S090 — true |
| "the counter's seven printed fields are unchanged (cited_rows=5)" | `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json` → `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=skipped`, 7 fields (exit 1 only because `--census` was omitted; the claim's command adds it) — **no widening** |
| "not read by plans/adoption_check.py" | code reading: `main()` reads `expect["access_date"]` and `expect["entries"]` only (`plans/adoption_check.py:64-66`); nothing enumerates expect keys, so an extra top-level key cannot reach any counter — true |

So C2's kill rule ("D5's repair must leave round 29's frozen counter fields unchanged
(`cited_rows=5`)") holds by construction *and* by run. `check_d5` is also coupled to the described
state (it fails if `^source: S091` appears in the entry), so the note cannot silently outlive its
subject.

**Verdict: answers the wording** — the route is explicitly one of the two offered. It is, however, the
one repair that is *cosmetic by construction*: a prose sentence inside a machine expectation file,
invisible to the counter, the census and every selftest, guarding a registry↔entry asymmetry that
nothing enforces. That is allowed here because the routed defect named it; had it been my choice, the
first route (cite S091 as a source line) would have made the relation observable to the counter at
`cited_rows=6` — but that would move a frozen field and is exactly why the defect offered the note.

## 2. Named list — cosmetic or adjacent repairs

| item | class | why |
|---|---|---|
| D1 as shipped (provenance header + wave 8-field line at the cited path) | **adjacent** | answers "no such path is committed" but not the quoted bytes; the mismatch is *recorded in a comment*, which is the behaviour the bar rejects. Also uncommitted, and the planted line is output the shipped counter can no longer emit. |
| D2's added lane-wide clause (final form) | **advisory only** | the narrowing is repaired and both revs are now pinned correctly (65 @`2ff4b6f`, 66 @HEAD, extra file named and verified). Imprecision that remains: 54/66 hits are round-28 scratch clones, so "65 files" reads as prevalence over a 12-file distinct population. |
| D5's `usedby_notes.S091` | **cosmetic by permission** | prose in a machine file, read by no tool; permitted by D5's own wording, correct in every particular, but changes no observable. |
| D3's table cell | **not cosmetic** | single false numeric claim corrected on the surface that was wrong; registry already right, quote untouched. |
| `check_d1` / `check_d2` as detectors | **calibration gap** | string-presence proxies. `check_d1` passes on any file containing `entries=0` and `exit=1` (no field set, no quoted-line match, no commit test); `check_d2` passes on a line that merely mentions `corpus/knowledge/*.md`. `defects=0` is therefore reachable with D1's substance unmet — which is what happened. |

## 3. Residual risk

- **C2 can print `defects=0` on the current tree while D1's citation still does not reproduce the cited
  number line.** If the claim's axis verdict rests on `defects=0`, the calibration evidence is weaker
  than the routed wording requires for D1. Recommended either strengthen `check_d1` (assert the
  seven-field quoted line as a byte substring, and `git cat-file -e` on the path) or record D1 as
  *partially* closed.
- **D2's count still overstates prevalence** (scratch clones). If the number stays, add "54 of them
  round-28 scratch copies of the round-12 evidence" or substitute the 12-file distinct figure.
- **The lesson file was rewritten twice mid-review** (04:05 → 04:22 → `3a0ab556…`), so the D2/D3
  verdicts are pinned to `3a0ab556612f868fbcf57c8b9e4212b9cfa3d7966d1b7a9599ec8351778ee1d4`. If the
  seat edits again, re-run the five D2 commands and the one word-count check against the new hash; the
  substantive conclusions (scope narrowed with 0 hits, cell at 8 words) held across all three versions
  I read, and the seat's own in-flight edit moved the D2 clause from unpinned to rev-pinned.
- **D4 remains open** at review (`defects=1`); out of this seat's item list, noted because it is what
  the counting command prints today.
- **Out of scope, observed once:** `.ufo/waves/round-30/claims/control-nothing.txt` prints
  `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` (`exit=1`) —
  seven fields, `census=ok`, while the round-29 report's frozen text says `census=skipped`. That is C1's
  control, not a D-item; flagged only because it is the one place where the 7-field format the D1
  receipt should have carried is already on disk.

## 4. Verification gaps (honest)

- I did not fetch the S078 source bytes; the word count is arithmetic on the quoted string and the
  cross-surface agreement (lesson cell ↔ registry anchor cell ↔ `words()`), not a re-open of the
  README. The round's access-date obligation is not discharged by this seat.
- I did not run `python3 plans/adoption_check.py … --census` (no `sources-census.sh` invocation), so
  `census=ok` for D5's kill-rule check is asserted only through the 7-field print with
  `census=skipped`; `cited_rows=5` — the field the kill rule names — is measured.
- No LSP server covers this tree (`plans/`, `corpus/` are Python + Markdown with no project config);
  caller checks were done by reading `plans/adoption_check.py` and `plans/round30_defects.py` in full
  and by running the two commands above. No semantic-index claim is made.
- No tool was installed or upgraded for this seat; no pacman transaction was attempted.
