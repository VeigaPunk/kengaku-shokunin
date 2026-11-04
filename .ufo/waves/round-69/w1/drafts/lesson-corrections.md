# Draft — two one-line additions for `corpus/lessons/round-68.md`

Target: `corpus/lessons/round-68.md`, appended as a dated section after the `## Mistakes` table. Closes
R69-C2 **E5** and **E6** (`plans/round69_c2_routed_defects.py:236-251`):

- E5: **exactly one** line containing `strict attack share`, `3/12`, and all of `reviewer`, `critic`,
  `mutation-tester`, `labrat` — so a second line carrying the same phrase breaks the check.
- E6: **at least one** line containing `w1-results.json`, `output: ""`, and `per-seat`.

Both additions are single physical lines: the gate counts `text.splitlines()` entries, so a wrapped line
is a miss.

**If a correction section already exists in the lesson, replace its two bullets — do not append a second
copy.** At drafting time the working tree already carried such a section (` M corpus/lessons/round-68.md`);
appending would make `strict-lines=2` and fail E5.

## Paste-ready text

<!-- paste-start -->
## Corrections (round 69, dated; the round-68 text above is not edited)

- **Strict attack share.** The round-68 report's w1 line counted sentinel, revenger and scout as attack seats (6/12 = 50 %); the run-15 definition is the strict set {reviewer, critic, mutation-tester, labrat}, so the strict attack share is 3/12 = 25 % (floor met exactly) — the wider set is named here and is never counted as attack share again.
- **`w1-results.json` record.** That file carries twelve entries with no seat output — the frozen clause words it `output: ""`, the committed bytes say `"output": null` — under the kernel-restart note; the output record is the twelve per-seat reports under `.ufo/waves/round-68/w1/`, and `results.json` must not be read as the seat-output record for any round.
<!-- paste-end -->

## Grounding

| claim | source (re-derived at drafting time) |
|---|---|
| w1 attack line counted 6/12 over `{reviewer, critic, mutation-tester, sentinel, revenger, scout}` | `corpus/lessons/round-68-verifier-spotcheck.md` §5 item 5 |
| strict share is `3/12` | re-derived: `python3 -c` over `.ufo/waves/round-68/w1-results.json` `results[*].agent` → `Counter({'executor': 3, 'scribe': 2, 'scout': 1, 'reviewer': 1, 'critic': 1, 'mutation-tester': 1, 'sentinel': 1, 'revenger': 1, 'connector': 1})`; strict set members = `ReceiptReview`/reviewer, `ClaimFalsify`/critic, `CounterMutate`/mutation-tester → `3 / 12` |
| twelve entries, kernel-restart note | same file: `seats: 12`, `results: 12`, `notes` all `orchestrator kernel restarted mid-wave; …` |
| twelve per-seat reports | `.ufo/waves/round-68/w1/` — 12 seat `.md` files (`PypiReplicate`, `GateRedRun`, `SelftestTally`, `RegistryRows`, `SourcesRows`, `SourceOpen`, `ReceiptReview`, `ClaimFalsify`, `CounterMutate`, `ForgeScan`, `RenderingTrace`, `SiblingOverlap`) |
| `"output": null` (not `""`) | `grep -o '"output": [^,]*' .ufo/waves/round-68/w1-results.json \| sort \| uniq -c` → `12 "output": null`; JSON load → `Counter({'NoneType': 12})` |

## Fact I could not ground as the routed defect states it

Round-68 spot-check §5 item 6 says the file carries `output: ""`. The committed bytes carry
`"output": null` in all twelve entries. E6's frozen literal is `output: ""`, so the correction line has to
quote that clause — the draft therefore quotes it as the frozen wording and states the committed value
(`"output": null`) in the same line, rather than asserting `""` as fact. A reader who greps the JSON for
`output: ""` gets zero hits; a reader who greps for `"output": null` gets twelve. This is a defect in the
routed item's wording (and in the frozen E6 literal), reported, not edited.
