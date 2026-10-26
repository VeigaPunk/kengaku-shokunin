# R38LessonDraft — round-38 lesson drafted from committed artefacts (scribe, wave 1)

Seat `R38LessonDraft`, kengaku round 38 wave 1 (hyaku run 8). Lane read in place, read-only; nothing in
`kengaku-shokunin` outside `.ufo/waves/round-38/build/R38LessonDraft/` and this report was written. No clone was
made, so no scratch directory existed to remove (`/fast/scratch/hyaku/kengaku-r38/` untouched). No tool installed
or upgraded; no network fetch beyond two GitHub issue reads through the already-configured `gh`.

## Deliverable

`.ufo/waves/round-38/build/R38LessonDraft/round-38.md` — 17,721 bytes, sections `## Gate`, `## Mistakes`,
`## Census`, `## Spot-check`, `## Close`, shaped on `corpus/lessons/round-37.md`. Every landing-only number is the
literal token `<L1 fills>` (11 occurrences): the C1 predicate block, the C2 landing block, the census after-state,
the prior-art disposition and the wave-2 relabelled-map control.

## Axes (godspeed)

- **calibration** — the seat the lesson moves: it turns this round's freeze into two mined mistake rows with one
  mechanically red check each, instead of prose.
- **depth / operability** — no new instrument, no new file outside the report dir; every claim names a command.
- **no-harm** — zero edits to `corpus/`, `plans/`, `SCORECARD.md`, `README.md`, `PROVINCE.md`, the lane's index or
  jj state; `plans/` is entered only by read commands.

## Facts established at drafting (command → output)

1. **Ancestry.** `git merge-base --is-ancestor fc1174f5 e0a37853` → rc 0; `… e0a37853 e95cf550` → rc 0.
2. **Freeze integrity.** `git show e0a37853:<path> | sha256sum` against the eight lines of
   `.ufo/waves/round-38/claims/frozen-digests.txt` → 8/8 `MATCH` (gate `ea638822…`, both counters, probe,
   `pkg-spec-r38.json`, dry table, round-37 counters).
3. **Controls are red.** `control-c1-nothing.txt`: `PINS total=14 mismatched=0`, `BATTERY fixtures=64 wrong=0
   renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0`,
   `PREDICATE C1 fail`, exit 1. `control-c1-gate-edited.txt`: `mismatched=1 first=plans/pkg_gate.py`, `invalid=22`.
   `control-c2-nothing.txt`: `checks=7 defects=4` (V2/V3/V4/V7). `control-c2-skip.txt`: `checks=7 defects=2`
   (V2 on `P10 DEFECT fresh probe output is not byte-equal to the receipt`, V6), `V7 ok rows=7 tags=7`.
   `census-before.txt`: 15 W04, `kengaku ok`, exit 0. No `plans/battery38` exists in the lane
   (`ls plans/ | grep -c battery38` → 0).
4. **Mistake 1 (order-of-operations recurrence) is corroborated, not just quoted.**
   `git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt` → `fatal: path … exists on disk, but
   not in 'e0a37853'`, rc 128; `git log --diff-filter=A --format='%H %cI' -- corpus/evidence/round38/build-pmars-probe.txt`
   → `e95cf550… 2026-10-26T02:38:41-03:00`. `grep -l "fresh probe" .ufo/waves/round-38/claims/*.txt` →
   `control-c2-skip.txt` alone. So the proposed ordering lint ("no committed control may contain `fresh probe`
   unless the receipt exists at that commit") is **RED on the freeze commit** — a fix that can fail, unlike the
   round-37 "re-pin and byte-compare" which this round recurs despite.
5. **Mistake 2 (witness-picked label) is repaired in the frozen counter and shown to bite.** `plans/round38_c2_verify.py:239-243`
   builds `violating` from every case whose `violates=` carries the tag; `:205-210` derives `enforced|unenforced|partly`.
   Derivation over the frozen receipt (`CASE` lines joined to the dry table's `TAG` lines) prints, for all seven
   tags, **`partly`** — `from-source` 7 pass/15 fail, `no-x11` 1/2, `debian-source` 7/15, `extract-to-app` 7/15,
   `install-path` 1/3, `results-format` 1/4, `debugger-works` 7/15. A row labelled `enforced` (the round-37 defect
   at `tb2-git-webserver-grader.md:107`) is red today. Recorded residual: four tags are carried by all 22 cases,
   so their label is the overall split, not a discriminating state.
6. **Prior art re-opened live** (the claims left it to "a wave-1 seat"; no seat had touched it —
   `grep -rn "issue #59" .ufo/waves/round-38/build/` → no hit before this seat). `gh api
   repos/harbor-framework/terminal-bench-2/issues/59` → open, 2026-04-13, sam571128, body line 14
   `E: Version '1.22.21' for 'dpkg-dev' was not found` (oracle pins, not the grader). Bodies saved and digested:
   `tb2-issue-59-body.md` `22936c6e…646e`, `tb2-issue-38-body.md` `27ee1f27…f713`. Issue #38 (open, 2026-02-13)
   is the stronger prior art: it asks for exactly the `/app/pmars-<version>/` wording that `R38ScoutUpstream.md` §2
   measured in the TB2.1 copy of `instruction.md` line 3.
7. **Census at drafting.** `scripts/sources-census.sh validate --root … kengaku` → exit 0, `kengaku ok`, the same
   15 W04, no new one. Counts: rows 107, knowledge files 44, README index rows 44 → landing 109/45/45 `<L1 fills>`.
8. **Merge re-screen receipts** (`build/R38MergeRescreen/`): `c2-ids` = S115/S116, `c2-collisions` = S115/S116,
   `collisions` = 31 registry ids already inside the staged range S077–S251. Recorded as pending with that count.

## Gates

| gate | state |
|---|---|
| C1 predicate `MUTANTS total=22 killed=22` | not run by this seat (L1's integration run); three wave-1 seats report attributed kills for their own subsets (`R38BatP1Run` N01/N16, `R38BatP3` N02, `R38BatMain` N17/N18) |
| C2 predicate `checks=7 defects=0` | not runnable at drafting — entry absent (`ls corpus/knowledge/ \| grep -ci pmars` → 0), so V4/V7 read `receipt or entry absent` |
| draft completeness | Gate rows for the entry, S115, S116, the three captured-not-rowed files, prior art, proposal 2(c) (rejected), merge re-screen (pending); two Mistakes rows with a demonstrated red each; Census; 10-item Spot-check; Close |
| write bounds | `git status --porcelain` in the lane was not run (no mutating git used); writes confined to `build/R38LessonDraft/` |

## Touched surfaces

| path | role |
|---|---|
| `.ufo/waves/round-38/build/R38LessonDraft/round-38.md` | the drafted lesson (deliverable) |
| `.ufo/waves/round-38/build/R38LessonDraft/tb2-issue-59-body.md`, `tb2-issue-59.json` | prior-art capture, live 2026-10-26 |
| `.ufo/waves/round-38/build/R38LessonDraft/tb2-issue-38-body.md`, `tb2-issue-38.json` | second prior-art capture |
| `.ufo/waves/round-38/build/R38LessonDraft.md` | this report |

No lane file, no sibling directory, no fleet-root file, no jj operation, no index entry.

## Out of scope / not done

- The C1 battery modules (`plans/battery38/`), the C2 entry, registry rows S115/S116, README/PROVINCE text, the
  round-37 entry erratum and any QUALITY criterion: L1 integration work, left as named landing obligations.
- No predicate was run here by design; the lesson's "Gate" verdicts that depend on them are `<L1 fills>`.
- The merge re-screen verdict and the wave-2 relabelled-map control are not mine to measure.

## Findings for the L1 (in priority order)

1. Land the **ordering lint** ("`fresh probe` text in a committed control ⇒ receipt exists at that commit") as a
   counter check; it is red at `e0a37853` and green after `e95cf550`. Without it the recurrence has only prose.
2. The entry's requirement map **must read `partly` on all seven rows** for this receipt; V7 will red anything
   else. Consider naming the four all-case tags' weakness in the entry's limits, or the map looks stronger than
   it is.
3. Row prior art: #59 alone does not make the grader case a replication — cite it as oracle-level; #38 (and the
   2.1 line-3 diff) is the load-bearing prior art for the instruction half. Both need a committed capture outside
   `corpus/evidence/round38/tb2-build-pmars/`, because V1 rejects extra files there.
4. The 2.1 divergence means every `instruction.md:<L>` anchor is a **2.0** anchor; state that in the entry so a
   reader does not resolve line 3 against 2.1.
5. Census landing must be one commit (entry + S115 + S116 + README index) to keep the genuine-package fixture's
   `corpus/` copy and the 109/45/45 counts consistent.

VERDICT: lesson-drafted
