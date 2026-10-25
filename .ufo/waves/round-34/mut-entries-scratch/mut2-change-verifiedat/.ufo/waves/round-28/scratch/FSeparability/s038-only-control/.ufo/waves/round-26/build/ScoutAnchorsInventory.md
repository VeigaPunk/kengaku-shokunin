# Round 26 — SHONEN and axis-anchor inventory

Base: `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d` (`git rev-parse HEAD`). `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, and the lesson are clean at HEAD. The working-tree `PROVINCE.md` diff is append-only after line 171, so its line 129 content is unchanged at base. This is a literal Markdown/path audit; no `lsp` device was mounted, so no semantic-server results are claimed.

## SHONEN.md pointers

- `SHONEN.md:5-6` → `SKILL.md`. **[Observed]** Line 5 asks for decision tables, error patterns, checklists, and cited sources; line 6 is a whole-file pointer. Targets include `SKILL.md:23` “## Decision table — benchmark selection”, `:60` “## Benchmark anti-patterns”, `:568` “## Production checklist — running an eval”, and `:611` “## Cited local sources”. **[Inference]** Broad pointer matches the stated content; no exact line anchor to drift.
- `SHONEN.md:7-8` → `LOG.md:7`. **[Observed]** `LOG.md:7`: “round 4: executed first authored eval (closes SHONEN ‘end-to-end task’ checkbox)” and describes a 4-task slice graded with repo `grade.sh`. **[Inference]** Directly supports the checklist sentence; aligned.
- `SHONEN.md:9-10` → `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`. **[Observed]** Target line 48 is only “## Box-3 verdict”; line 49 begins “**[x]** — decided by steps 17-18” and says the gates “ran cold from the SKILL.md text alone”. **[Inference]** Correct section, but the line anchor lands on its heading, one line before the supporting verdict. Weak/imprecise, not a broken path; `:49` is the direct evidence line.
- `SHONEN.md:11-12` → `PROVINCE.md:129`. **[Observed]** Target line 129 is only “### Adjacent”. Nearby lines 134-137 list routed owners; e.g. line 137 says research method “stays chousa’s” and “this lane holds neither method nor duplicates it.” **[Inference]** The section is relevant to cross-domain boundaries, but `:129` itself does not establish “No cross-domain bleed” or that the whole Province is still accurate. Weak heading-only pointer; unresolved as direct evidence.

## SCORECARD.md line anchors

- `SCORECARD.md:612` (round-24 re-derived table) contains backticked `:162` → same-file `SCORECARD.md:162`. Target: “| **novelty** *(owned)* | 6 → **7** | The written +1 rule’s three legs fire.” **[Inference]** Correctly lands on the round-14 numeric novelty basis.
- Round-25 mapping paragraph `SCORECARD.md:662` contains backticked `:244` (adjacent to, not inside, the axis table) → same-file `SCORECARD.md:244`. Target rubric row: “a probe measures a construct the lane could not previously observe, the instrument is inspectable in-repo, **and** the claim carries a prior-art verdict with a fetched URL”; it excludes “a phenomenon already published (keep as replication, not contribution)”. **[Inference]** Supports the cited novelty rubric.
- The round-25 re-derived axis table (`SCORECARD.md:677-685`) has no backticked `:NNN` line anchor. Its nearby C2 row uses plain `AXES.md:15`, not a backticked anchor.
- Falsify-wave C1 table cell `SCORECARD.md:703` contains backticked `:244` → `SCORECARD.md:244`, the same rubric row quoted above. **[Inference]** Correctly supports the “already published” cap cited in that cell. The falsify C2 row’s `PROTOCOL.md:432` is plain text, not a backticked anchor; revised axis-state lines 721-722 contain none.

## Drift / limits

- `SCORECARD.md:618` still says “no integrator arbitration”; R25-E2 at `SCORECARD.md:647` explicitly supersedes that round-24 basis, noting the orchestrator adjudicated the round and adjacency stayed unchanged. Historical text remains, but the correction is explicit.
- The pre-revision round-25 table is superseded, not current: `SCORECARD.md:679` says novelty “8 claimed” and `:668` gives 11 mismatches; the falsify revision at `:721` records novelty 7 held and `:704` gives base mismatches 10. `:699` explicitly says the revision supersedes the earlier axis table and C1/C2 rows.
- LSP unavailability limits this to literal pointer/target checks. Whether the entire current Province remains accurate or the lane has no cross-domain bleed is not established by the heading pointer alone.

Installs: none.
VERDICT: Four SHONEN pointers found; two align directly, two land on relevant headings rather than supporting text. The round-24 `:162` and round-25/falsify `:244` anchors resolve to the intended rubric/basis; round-24 arbitration and pre-revision round-25 values are explicitly superseded.