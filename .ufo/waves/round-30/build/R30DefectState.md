# R30 defect state — independent re-derivation of D1–D5

Seat: `L1Kengaku30.R30DefectState` (leaf scout). Scope: re-derive the five routed defects from
`corpus/lessons/round-29-verifier-spotcheck.md` §5 against this lane's own bytes, with my own
commands. **No repair performed; no lane file edited outside this report.**

- Repo measured: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, HEAD `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db`
  (`protocol-shokunin`, "round-29 verifier spot-check (integrator, hyaku)", 2026-10-25 04:05:25 -0300).
- Measurement time: 2026-10-25T04:23:14-03:00.
- Two byte surfaces are separated in every row: **HEAD** (committed bytes, the pre-repair state the
  claim's control is defined on) and **worktree** (live, concurrently dirty: 8 `git status --porcelain`
  entries from other round-30 seats, including four of the five D-targets). A worktree-only change is
  *not* a repair until committed; conversely a HEAD-only measurement does not describe what a peer has
  already staged. Both are reported.

Lane `git status --porcelain` at measurement (context for the worktree column, my own run, 8 lines):

```
 M .ufo/waves/round-29/attempt2/adoption-expect.json
 M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md
 M corpus/lessons/round-29.md
?? .ufo/waves/round-30/
?? corpus/evidence/round29-attempt2/control-nothing.txt
?? corpus/evidence/round30/
?? plans/round-30-claims.md
?? plans/round30_defects.py
```
Four of the eight carry D-repairs in flight (the three `M` lines and the untracked receipt: D1 via the
receipt, D2/D3 via the lesson, D4 via the wave file, D5 via the expect file). HEAD is a clean committed
tree; every worktree delta above is another seat's in-flight work, not mine.

## D1 — cited control receipt path

Commands and output (cwd = lane):

```
$ git cat-file -e HEAD:corpus/evidence/round29-attempt2/control-nothing.txt
fatal: path 'corpus/evidence/round29-attempt2/control-nothing.txt' exists on disk, but not in 'HEAD'
cat-file-exit=128

$ git ls-files --error-unmatch corpus/evidence/round29-attempt2/control-nothing.txt
error: pathspec 'corpus/evidence/round29-attempt2/control-nothing.txt' did not match any file(s) known to git
ls-files-exit=1

$ ls -l corpus/evidence/round29-attempt2/control-nothing.txt .ufo/waves/round-29/attempt2/control.nothing.txt
-rw-r--r-- 1 vgpnk vgpnk 699 Oct 25 04:21 corpus/evidence/round29-attempt2/control-nothing.txt
-rw-r--r-- 1 vgpnk vgpnk 222 Oct 25 03:39 .ufo/waves/round-29/attempt2/control.nothing.txt

$ git cat-file -e HEAD:.ufo/waves/round-29/attempt2/control.nothing.txt   → present (tracked)

$ cd /home/vgpnk/Projects/shokunin && git show d4090261:.ufo/reports/round-29/kengaku.md | grep -c 'corpus/evidence/round29-attempt2/control-nothing.txt'
1
$ git show d4090261:.ufo/reports/round-29/kengaku.md | grep -n 'control-nothing'
124:  (`corpus/evidence/round29-attempt2/control-nothing.txt`, `.ufo/waves/round-29/attempt2/control.nothing.txt`).
$ git status --porcelain -- .ufo/reports/round-29/kengaku.md      → (empty; report committed at d4090261)
```

The cited-path bytes now on disk (worktree, untracked) open with a provenance header and carry the
field the report's quoted line omits:

```
# control: do-nothing round, frozen counter (round 29 attempt 2)
# base 1f3b0f1ec41ec297130e8944ff97968d32324632
# provenance: byte-identical control output first committed at .ufo/waves/round-29/attempt2/control.nothing.txt
# (round 29 attempt 2). Round 30 (2026-10-25) re-commits it at the path the round-29 report cites
# (routed defect D1, corpus/lessons/round-29-verifier-spotcheck.md section 5): the report quoted this
# line without the `verified_at=0` field the wave file carries. Both fields are kept below; the
# quoted prefix `entries=0 indexed=0 cited_rows=0 …` is unchanged.
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 verified_at=0 census=skipped
exit=1
```
(verbatim `cat` of the untracked file, all 9 lines).

**Verdict: DEFECT at HEAD bytes; repair staged, uncommitted.** The report (`d4090261`, the committed
tip of that file) cites `corpus/evidence/round29-attempt2/control-nothing.txt`, and that path is absent
from git (`cat-file` exit 128; `ls-files` exit 1). Re-derivation nuance worth recording: the spotcheck
says "cites … twice", but the committed report name that path **once** — on line 124, in the same
parenthesis that also names the committed wave path `.ufo/waves/round-29/attempt2/control.nothing.txt`.
The defect is real (a cited receipt is not in git); the "twice" count is not reproducible from report
bytes. The remedy's *second* branch ("cite the wave path") is already satisfied on that same line, so
the live remedy is the *first* branch: commit the receipt under the `corpus/evidence/…` name — which is
exactly what the untracked 699-byte file does, and it cannot count until `git add`ed.

## D2 — kappa sweep scope

```
$ git show HEAD:corpus/lessons/round-29.md | sed -n '231,232p'
  point duplicates `knowledge/llm-judge-calibration.md:7-13`. Only per-variable kappa and a
  test–retest ceiling are new (`grep kappa` → 0 hits in the lane).

$ sed -n '231,235p' corpus/lessons/round-29.md      # worktree, verbatim
  point duplicates `knowledge/llm-judge-calibration.md:7-13`. The only new items are per-variable
  kappa and a test–retest ceiling — `grep -rn kappa corpus/knowledge/*.md` → 0 hits at the scope
  that command measured, while a lane-wide `git grep -ni kappa` over corpus/knowledge/*.md included
  finds 65 files (mostly the round-12 Greek-letter token vocabulary). Routed defect D2,
  `corpus/lessons/round-29-verifier-spotcheck.md` §5.

$ git grep -li kappa HEAD -- 'corpus/knowledge/*.md' | wc -l        → 0        (the scan's own scope)
$ git grep -li kappa HEAD -- . | wc -l                              → 66       (lane-wide, tracked)
$ git grep -li kappa -- . | wc -l                                   → 66       (worktree)
$ git grep -li kappa 2ff4b6f -- . | wc -l                           → 65       (round-29 tip)
$ diff <(git grep -li kappa 2ff4b6f -- . | sed 's/^2ff4b6f://') <(git grep -li kappa HEAD -- . | sed 's/^HEAD://')
62a63
> corpus/lessons/round-29-verifier-spotcheck.md
```

**Verdict: DEFECT at HEAD bytes; worktree repair present, uncommitted, and its count is one behind.**
At HEAD the sentence states `grep kappa` → "0 hits in the lane": the command carries no scope, and the
lane-wide truth is 66 tracked files, so the universal is false. The worktree sentence is correctly
narrowed ("at the scope that command measured") — but it prices the lane-wide sweep at "65 files",
which reproduces only at round-29 tip `2ff4b6f`; at HEAD it is 66, the delta being the spotcheck file
itself (`corpus/lessons/round-29-verifier-spotcheck.md`), which mentions kappa. As written the repaired
sentence is falsifiable by one `git grep` at HEAD. Correct value at HEAD: 66.

## D3 — S078 line-75 quote word count

```
$ printf '%s\n' "The verifier never runs in the agent's sandbox." | wc -w   → 8
$ printf '%s\n' "731 -> 642 tasks: 89 dropped after review." | wc -w       → 8

$ git show HEAD:corpus/lessons/round-29.md | sed -n '194p'
| S078 | …66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md | "731 -> 642 tasks: 89 dropped after review." — 8 words, line 99; "The verifier never runs in the agent's sandbox." — 9 words, line 75; `v2/GATE.md` line 1 … |
   (row elided at the URL prefix and row tail; the two quotes and both word counts are verbatim)

$ git show HEAD:corpus/SOURCES.md | grep -nE '^ {0,3}\|[[:space:]]*S078' | grep -o 'line 75[^;]*'
line 75: "The verifier never runs in the agent's sandbox." (8 words)

$ grep -n 'S078' corpus/lessons/round-29.md      # worktree line 194
… "The verifier never runs in the agent's sandbox." — 8 words, line 75; …
```

Live re-fetch of the pinned artifact (my own bytes, not the lesson's):

```
$ curl -sS 'https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md'
6858 bytes  sha256=dde4168fed17ca1ea00b26a93aca78dad43c7b3f981b93a2872428259428231f
$ sed -n '75p;99p' s078.md
2. **The verifier never runs in the agent's sandbox.** The locked agents capture the agent's `git diff` as
- 731 -> 642 tasks: 89 dropped after review. Same repositories, same base commits.
byte-substring test: both registry quotes → True; words = 8 and 8
```

**Verdict: DEFECT at HEAD bytes; worktree repair present, uncommitted.** `wc -w` on the quoted text is
8; the registry row is right (8); the HEAD lesson cell is wrong (9). The sha256 and byte count I fetched
match the lesson's own receipt (`dde4168f…8231f`, 6858 bytes), so this is a count error only, not a
fabricated quote.

## D4 — uncommitted round-29 wave evidence

```
$ git status --porcelain -- .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md
 M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md

$ git diff --numstat -- .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md
22	0	.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md

$ git cat-file -e HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md   → present (tracked)
$ git check-ignore -v .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md    → exit 1 (not ignored)

$ git diff -- .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md | sed -n '6,12p'
@@ -690,3 +690,25 @@ …
+### D. Addendum — the 275/4/279 identity is exact (verified, not accepted)
…
+… Those are advisory findings for the L1; nothing in this report edits
+the lane, and no claim above rests on an unrun check.
```

**Verdict: DEFECT, open at the committed tip.** The file is tracked and non-ignored, and carries a
22-line-added critic addendum that has never been committed — the same 22/0 the spotcheck reported. No
other round-29 wave path is dirty, so the defect is exactly this one file. Its own text self-labels the
content advisory, which is an argument for recording *why* it stays advisory — but the D4 remedy is a
commit either way, and no commit has happened. Pre-repair state = this status line; the fix is a lane
commit (or a recorded advisory-only rationale), neither of which is in the tree I measured.

## D5 — S091 `used-by` asymmetry vs the frozen counter

```
$ grep -nE '^ {0,3}\|[[:space:]]*S091' corpus/SOURCES.md        # row 106; the last four cells verbatim, leading cells elided
… | mined | 2026-10-25 | 180d | corpus/lessons/round-29.md, corpus/knowledge/benchmark-task-validity-checklist.md |

$ grep -n '^source:' corpus/knowledge/benchmark-task-validity-checklist.md
1:source: S077 — …/terminal-bench/…/TASK_REVIEW_AUTOMATION.md — …
2:source: S078 — …/SWE-bench_Pro-os/…/v2/README.md — …
3:source: S079 — https://github.com/laude-institute/terminal-bench-2 — …
4:source: S080 — …/Toolathlon/…/README.md — …
5:source: S090 — https://www.tbench.ai/news/announcement-2-0 — …
   (five lines; S091 absent. URL paths elided with `…` in this block only; the line count and the five
   ids are verbatim — the command prints exactly 5 lines and no sixth.)

$ git show HEAD:.ufo/waves/round-29/attempt2/adoption-expect.json
{
  "round": 29,
  "attempt": 2,
  "access_date": "2026-10-25",
  "entries": [
    {
      "path": "corpus/knowledge/benchmark-task-validity-checklist.md",
      "sources": ["S077", "S078", "S079", "S080", "S090"]
    }
  ]
}
   → HEAD keys: round, attempt, access_date, entries

$ python3 -c "import json;print(sorted(json.load(open('.ufo/waves/round-29/attempt2/adoption-expect.json')).keys()))"
   → worktree keys: ['access_date', 'attempt', 'entries', 'round', 'usedby_notes']

$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=skipped
exit=1            # exit 1 is the unrun-census branch (--census absent), not a row failure

$ grep -n 'expect\[' plans/adoption_check.py
60:    expect = json.loads(args.expect.read_text(encoding="utf-8"))
61:    access_date = expect["access_date"]
62:    entries = expect["entries"]

$ cat corpus/evidence/round29-attempt2/adoption-measured.txt   # the round-29 frozen receipt (tracked)
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
```

**Verdict: DEFECT at HEAD bytes; documentation repair staged, uncommitted, and correctly inert.** The
registry asserts a relation the entry's `source:` block does not carry: 5 `source:` lines, no S091. The
counter is built so that cannot be seen — `usedby_ok` counts *cited ids* whose `used-by` cell names the
entry (`plans/adoption_check.py:21,90-98`), and an uncited id is not in that set; my run prints
`usedby_ok=1` (1 of 1 entry) with `cited_rows=5` unchanged, so the frozen round-29 fields survive. The
worktree adds a `usedby_notes` key whose text states the asymmetry and asserts the note is not read by
the counter — my read of lines 60–62 confirms the loader touches only `access_date` and `entries`, and
the run above prints identical fields, so the key is inert exactly as claimed. Not yet committed.

## Summary table

| item | check | HEAD bytes | worktree | verdict |
|---|---|---|---|---|
| D1 | cited receipt committed at `corpus/evidence/round29-attempt2/control-nothing.txt` | absent (`cat-file` 128) | present untracked, 699 B, provenance header | **defect** at HEAD; repair uncommitted |
| D2 | kappa sentence scoped to its measured command | "0 hits in the lane"; lane-wide 66 files | narrowed text, but prices sweep at 65 | **defect** at HEAD; repair uncommitted + count stale by 1 at HEAD |
| D3 | S078 line-75 quote priced at `wc -w` | lesson 9, registry 8, `wc -w` 8 | lesson corrected to 8 | **defect** at HEAD; repair uncommitted |
| D4 | round-29 wave evidence committed | ` M` + 22/0 uncommitted, tracked, not ignored | same | **defect**, open |
| D5 | S091 asymmetry visible / recorded | 5 `source:` lines, no S091; expect keys 4 | `usedby_notes` added, counter fields unchanged | **defect** at HEAD; repair uncommitted |

Net: all five reproduce as real defects on committed bytes; four have an in-flight repair visible only
in the worktree, and one of those four (D2) carries a count that no longer reproduces at HEAD (65 vs 66).
Nothing in this report repaired, committed, or reverted anything; the round's C2 control
(`defects=5` pre-repair) is still the correct reading of `363a4eb`.

## Confidence and remaining unknowns

- **Observed**: every path, cell, count, sha256, and command output above, from my own invocations.
- `[INFERENCE]` D1's "twice" is a spotcheck wording slip, not a second citation: one `grep -c` on the
  committed report returns 1 and the whole report file has one `control-nothing` line.
- `[INFERENCE]` D4's defect is confined to one file: `git status --porcelain` shows no other
  `.ufo/waves/round-29/**` entry.
- **Unknown / out of scope**: whether the in-flight repairs finish before the lane commits (concurrent
  seats own them); `plans/round30_defects.py` (untracked) was not read or run — the C2 counter's own
  behaviour is not my question, so I did not treat its presence as evidence for any D verdict.
- Tooling: none installed or upgraded (no need; `git`, `python3`, `curl`, `sha256sum` sufficed). No
  pacman transaction attempted.
