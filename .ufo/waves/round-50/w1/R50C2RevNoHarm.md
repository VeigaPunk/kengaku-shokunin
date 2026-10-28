# R50C2RevNoHarm — reviewer: are the C2 corrections append-only, and do they re-point rather than rewrite history?

Seat: `R50C2RevNoHarm` (reviewer, leaf). Serving R50-C2 (calibration).
Item: diff the `## Round 50 — C2 corrections` block against `SCORECARD.md`, confirm the cited lines are
untouched, and state whether any correction changes a historical claim instead of re-pointing it.

REV: `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1` (lane tip measured; `git -C <clone> rev-parse HEAD`).
Freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` verified ancestor of the tip before any measurement
(`git merge-base --is-ancestor 3b02d57 HEAD` → exit 0); `71f5f5f` is likewise an ancestor of `3b02d57`.
All work read-only against `git clone --shared` of the lane in scratch; no production file touched.
Instrument under audit unchanged since the freeze: `plans/round50_c2_audit.py` sha256
`b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef` at both `3b02d57` and `HEAD`
(`git diff 3b02d57..HEAD -- plans/round50_c2_audit.py` empty).

Axes named: (1) **append-only integrity** of the correction block; (2) **referential honesty** of each
`SUPERSEDED` row (does the historical text actually carry that pointer; is the target the referent);
(3) **measurement consistency** of the before/after numbers against the frozen claims text.

---

## 1. Append-only integrity — CONFIRMED, byte-for-byte

```
$ git rev-parse HEAD
c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
$ git diff --numstat 3b02d57..HEAD -- SCORECARD.md SHONEN.md PROVINCE.md
34      0       SCORECARD.md
$ git diff --numstat f7281bc..HEAD -- SCORECARD.md SHONEN.md PROVINCE.md
34      0       SCORECARD.md
$ git diff -U0 3b02d57..HEAD -- SCORECARD.md | grep -E '^(@@|\+\+\+|---)'
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -2134,0 +2135,34 @@ while its cap question is open. Full predicates, controls, kill rules, stages an
$ git diff 3b02d57..HEAD --check -- SCORECARD.md ; echo $?
0
```

One hunk, zero deletions, appended after the file's last pre-existing line (`3b02d57:SCORECARD.md` = 2134
content lines; `HEAD` = 2168). No edit is interleaved anywhere in the file.

Byte identity of everything that existed before the block:

```
$ B=$(git show 3b02d57:SCORECARD.md | wc -c)              # 253372
$ git show 3b02d57:SCORECARD.md | sha256sum
f7c3d46840091660c43187d378070760e9e9ba807d3dd08779433200cbe8b67d  -
$ git show HEAD:SCORECARD.md | head -c "$B" | sha256sum
f7c3d46840091660c43187d378070760e9e9ba807d3dd08779433200cbe8b67d  -
$ git diff --quiet 3b02d57..HEAD -- SHONEN.md   → SHONEN identical
$ git diff --quiet 3b02d57..HEAD -- PROVINCE.md → PROVINCE identical (649 lines both sides)
```

Cited lines: the twelve pointer names are carried by **20 distinct pre-existing lines**, not twelve —
`SCORECARD.md` 74, 97, 113, 563, 1168, 1169, 1180, 1420, 1572, 1650, 1721, 1804, 1841, 1915, 2084, 2104,
2105, 2119, 2120 and `PROVINCE.md` 416. Every one is byte-identical at `HEAD` at the same line number
(programmatic line-equality check: `mismatched: []`; `PROVINCE:416 identical: True`). The 34 appended lines
occupy 2135–2168; nothing earlier moved because the append is at EOF.

No rollback, no reflow, no whitespace churn: **the block is append-only and rewrites no earlier SCORECARD text.**

## 2. Referential honesty — 9/12 rows record a real absence; 3/12 supersede pointers the text never carried

Row inventory at `HEAD` (`SUPERSEDED` regex used by the counter): 12 rows, 12 unique pointers,
9 `never-landed`, 3 with an existing target.

`never-landed` rows are honest, measured: `git log --all --oneline -- <pointer>` returns 0 lines for all
twelve, including the nine `never-landed` ones and the three re-pointed ones. Targets exist
(`corpus/defects.jsonl`, `corpus/evidence/round9-replication/predictions-r9.md`, `corpus/routed-findings.jsonl`
all `git cat-file -e HEAD:…` → present).

**Finding H1 (high, calibration).** Three of the twelve rows — `corpus/defects.json`,
`corpus/routed-findings.json`, `corpus/evidence/round9-replication/predictions-r9.sh` — resolve not
historical pointers but **tokens the counter's own regex truncates**. The counter's `TOKEN` alternation lists
`json` before `jsonl`, `sh` is an extension, the match is non-greedy and there is no boundary assertion after
the extension, so:

```
'over `corpus/defects.jsonl`; freeze'                                     -> ['corpus/defects.json']
'`corpus/routed-findings.jsonl` (10 rows'                                 -> ['corpus/routed-findings.json']
'`sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo`**'
                                                                          -> ['corpus/evidence/round9-replication/predictions-r9.sh']
```

The pre-existing text contains **zero** genuine occurrences of those three tokens:

```
BASE text occurrences of 'corpus/defects\.json(?!l)': 0
BASE text occurrences of 'corpus/routed-findings\.json(?!l)': 0
BASE text occurrences of 'corpus/evidence/round9-replication/predictions-r9\.sh(?!a)': 0
```

(`SCORECARD.md:563` reads "over `corpus/defects.jsonl`"; `:1572` "`corpus/routed-findings.jsonl` (10 rows…)";
`:97` "`sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo`**" — all three referents
exist at the tip and needed no correction.)

Consequences:
- The frozen before figure `unresolved=12` is **3 false positives**; the honest before count is **9**
  (`plans/round34_c1_verify.py`, `plans/round34_defects.py`, `plans/round34_mutate.py`,
  `plans/round48_c1_verify.py`, `plans/round48_c2_verify.py`, `plans/round49_c1_verify.py`,
  `plans/round49_c2_verify.py`, `corpus/evidence/analyze.py`, `corpus/knowledge/repo-git-state.md`).
- The block's premise "Each row below resolves one pointer that the self-assessment files still carry and
  that does not resolve at the tip" is false for those three rows: the files do not carry them; the counter
  emits them. This is exactly the case for an open-window **counter repair** (boundary after the extension,
  or `jsonl` before `json`, longest-match), not for a SCORECARD correction.
- The block's prose then retro-describes history: "the round-35 ledger landed as `defects.jsonl`" and "the
  `.sh` name never existed" are both true statements, but they are offered as if the earlier text had named
  `.json`/`.sh`. It had not. **These three rows therefore record a claim about what earlier text said rather
  than re-pointing what it said** — the only place in the block where a correction touches a historical
  claim instead of adding an absence record.
- The counter is also self-referential at the tip: the correction rows themselves are scanned as pointers
  (`corpus/evidence/round9-replication/predictions-r9.sh` occurs at `HEAD` only inside the block, line 2147),
  so the after-state is partly satisfied by the text that claims to fix it. `total` therefore grows from
  271 (71f5f5f) → 275 (3b02d57) → 277 (HEAD), and the after number is not directly comparable to the before row.

**Finding M2 (medium, measurement consistency).** The block restates the before measurement as
`POINTERS total=275 …` and attributes it to `plans/round-50-claims.md` §C2, but §C2 freezes
`POINTERS total=271 paths=213 hashes=58 resolved=259 … unresolved=12` at `71f5f5f`, and the SCORECARD row at
line 2134 repeats `total=271`. Measured with the counter's own frozen regex:

```
REV 71f5f5f77591 paths=213 hashes=58 total=271
REV f7281bc        paths=216 hashes=59 total=275
REV 3b02d573d58c   paths=216 hashes=59 total=275
REV HEAD           paths=218 hashes=59 total=277
```

275 is the S1-tree figure (`f7281bc`) and matches receipt `claims/c2-before.txt` (which itself prints
`TIP f7281bc …`), not the frozen 71f5f5f figure. So SCORECARD now carries two different "before" totals for
the same claim (2134: 271; 2139: 275), and the block mis-cites which number §C2 froze. No earlier bytes were
changed, but a reader cannot reproduce 275 at the revision the claim names. (The frozen claims text has the
same defect in reverse: it cites `c2-before.txt` for a 71f5f5f figure the receipt does not contain — outside
my edit surface; recorded, not repaired.)

**Finding L3 (low, evidence-citation accuracy in the appended block).**
- "The four `plans/round34_*` and four `plans/round48_*`/`round49_*` counters": the rows are 3 round-34
  (`c1_verify`, `defects`, `mutate`) + 4 round-48/49 = **7**, not 8. (The frozen claims text has the mirror
  error: "six pointers name counters" over a list of seven, "and four corpus paths" over five.)
- "PROVINCE:415 cites Kasegi's entry of that name": the pointer is on **PROVINCE.md:416**; 415 is the wrapped
  sentence head ending "…never a removal procedure. Kasegi's". Off by one, sentence-boundary only.
- "round 34, 48 and 49 all closed as honest stops": verbatim true for r34 (SCORECARD:1162) and r48
  (SCORECARD:2107); the r49 header (SCORECARD:2113) says "neither admitted", and "honest stop" appears in
  `corpus/lessons/round-49.md` — substantively right, not verbatim.

**Finding I4 (informational).** `plans/round50_c2_audit.py` is listed under "Instrument digests frozen with
this file" but carries no digest there, unlike the C1 counter and the population. It is in fact unchanged
since `3b02d57` (`b911d03a…`), so nothing is broken today; the pin is simply absent from the claims text.

## 3. Answer to the item

- **Append-only:** yes — single `+34/−0` hunk at EOF, prefix sha256 identical, `SHONEN.md`/`PROVINCE.md`
  byte-identical, all 20 pre-existing pointer-carrying lines identical at identical line numbers.
- **Twelve cited lines untouched:** the twelve pointers occupy 20 pre-existing lines (19 SCORECARD, 1
  PROVINCE); all untouched. If the intent was one line per pointer, every pointer group is untouched.
- **Does any correction change a historical claim rather than re-point it?** Nine rows are machine-honest
  absence records (`log --all` empty) that change no claim and offer no target — the cross-lane
  `repo-git-state.md` row resolves to nothing a reader can follow, which is the rule's intended use but worth
  naming as residual risk. The other three rows do **not** re-point a pointer the text carried: they
  supersede tokens manufactured by the counter's extension truncation, and their prose retro-describes the
  earlier rows. Plus M2's 275-vs-271 restatement. No earlier SCORECARD bytes were altered, so the discipline
  held; the *content* of three rows is a counter defect laundered as a documentation defect.

## 4. What the integrator should do (recommendation, not an admission)

1. Repair `plans/round50_c2_audit.py` inside the open window (measured defect: extension truncation and
   missing boundary after the extension; freeze `jsonl` before `json` or require a non-alphanumeric boundary).
   Re-measure before/after with the repaired counter; expect before `unresolved=9` (the three phantom tokens
   gone; the total moves to whatever the corrected token set yields — `.jsonl`/`.sha256.repo` referents enter
   or leave the population), and the three target rows to become unnecessary.
2. Do not delete the three rows silently (that would be a rewrite); either keep them as explicit errata that
   say the pointer was a counter artifact, or land a new append-only note in the block superseding the
   correction itself.
3. Align the 275/271 restatement with the frozen 271 (or state both revisions explicitly).

## 5. Limits and verification gaps

- `c2-before`/`selftest` receipts were read, not re-run; the audit was re-run only at `HEAD` in a clone.
- The 71f5f5f "before" counts were reproduced by emulating the frozen regex over `git show` output (paths and
  hashes counted exactly); I did not populate a 71f5f5f worktree, so I did not reproduce the resolution
  split (resolved/exists/superseded) at that revision.
- Tokenizer behaviour was demonstrated on the three affected literals and enumerated for every `.json*`/`.sh`
  token in the current text; a new pointer with a similar prefix collision could exist elsewhere later.
- Hash ancestry at `HEAD` was exercised by the counter itself (`unresolved=0`, 59 hashes), not re-derived per
  hash.
- No tool installs; no pacman; no model/routing data recorded. Scratch
  `/fast/scratch/hyaku/kengaku-r50/R50C2RevNoHarm` (one `git clone --shared`, no writes elsewhere) removed
  before this report was yielded.

VERDICT: Append-only — **PASS** (byte-for-byte; no earlier SCORECARD text rewritten). Referential honesty —
**3 of 12 corrections (25%) resolve counter tokenizer artifacts, not historical pointers**, and the block
mis-cites the frozen before total (275 vs 271 at `71f5f5f`). C2 as currently staged rests on a counter defect;
recommend the open-window counter repair before any scored C2 run. Not an admission.
