# L0FilingScout — report-only L0 questions that never reached the queue

Read-only mistake-mining; axes = filing completeness + queue provenance. Root `/home/vgpnk/Projects/shokunin`.
Population: 21 kengaku report files (16 fleet `.ufo/reports/round-*/kengaku*.md`, lane-local
`.ufo/reports/round-17`, `.ufo/rounds/round-19..22`; no round-23 report). Only the fleet round-24
report carries `## L0 questions`; no lane-local file does.
## Commands and counts
```
$ grep -Hn '^## L0 questions' <21 files>     -> .ufo/reports/round-24/kengaku.md:219 (only)
$ grep -ciE '\bL0\b' <each file> | nonzero   -> round-24/kengaku.md L0=1 (only)
$ grep -cE '^kengaku \|' .ufo/l0-questions.md -> 2 (lines 7, 35)
$ grep -c 'round-24' .ufo/l0-questions.md     -> 0
$ grep -cE '^- kengaku \| round-24 \|' reports/round-24/kengaku.md -> 3
```
Census (python re over `.ufo/reports/round-*/*.md`): 12 files with an L0 section, 28 questions,
28 bullet-prefixed, 0/28 filed by 60-char key. Queue: 66 unbulleted lane lines, 0 bulleted.
## Findings
- **F1 OBSERVED — 3 report-only L0s, 0 filed.** `.ufo/reports/round-24/kengaku.md:219-227`:
  `:221` Coverage cap (does a §Historical surface still count as "declared-but-unresolvable" for the
  coverage rubric cap?); `:224` Novelty r21 (convert verdict-only rounds retroactively, and by whom?);
  `:226` C2 admission (is a score-held closeout/state-accuracy claim an axis-move or bookkeeping?).
  Each 60-char key after `round-24 |` is absent from the queue (`in_queue=False` x3); `git log -S`
  for `Coverage cap`, `Novelty r21`, `C2 admission` -> 0,0,0 commits.
- **F2 OBSERVED — both queue kengaku lines are non-report origin.** Line 7 was added by operator
  commit `46e9ec3` (2026-09-28, also files kumitate r10/r11); the round-10 report only "refers" a
  fleet gate standard. Line 35 was batch-added by `f2df270` (2026-10-15, `ci`/Devin, 11 lanes at
  once), and its text occurs nowhere else (`grep -rln` -> only the queue); the round-13 report has
  no L0 section (next move is novelty work). Neither line is re-derivable from a report section.
- **F3 OBSERVED — systemic bullet-prefix drop.** Report sections emit `- <lane> | round-N | ...`;
  the queue has 0 bulleted and 66 unbulleted lane lines, and 0/28 report questions match. [INFERENCE]
  The append path matches `^lane | round-N |` and never strips `- `; kengaku's 3/3 loss is mechanical.
- **F4 OBSERVED — absence is not a race.** Report committed `dec4b51` 2026-10-19 19:39; queue last
  touched `52b3863` 2026-10-20 18:34 by another lane; nothing was added and later removed.
- **F5 impact.** These three questions gate round-25's C1 coverage verdict and C2 admission. Any
  verdict presuming a ruling is unsupported; the honest state is INDETERMINATE-dependent, not PASS.
## Remaining unknowns
- Whether an out-of-band channel (operator session, hyaku) received the three questions: no on-disk
  evidence; the queue is the only registered channel.
- Whether pre-r24 kengaku reports carried L0 sections later overwritten: no blob search beyond the
  three `-S` probes [scope limit].
## Installs
None; no network, no model requests, no writes outside this file.
VERDICT: 3/3 kengaku report L0s never reached the queue (round-24:221,224,226; absent by key and git
history); the queue's 2 kengaku lines are operator/batch-authored, not report-derived; systemic cause
is a bullet-prefix parse mismatch affecting 28/28 report L0s [INFERENCE].
