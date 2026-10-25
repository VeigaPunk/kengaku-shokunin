# R30 review — `plans/round30_defects.py`: tautology and failure capability

seat: R30RevCounter (reviewer, leaf) · round: kengaku 30 (hyaku run 6) · date: 2026-10-25
scope: claim C2 (D1-D5 closure) — the checker's predicates only. No lane byte edited by me.

**Pinned revision reviewed and tested: `19ce5332c571903be8e6e3dc679563241c745a4483465abaefb133fd969d982b`**
(220 lines). Everything below is measured on those bytes unless a block is labelled otherwise.

## 0. Provenance, and why the pin matters

The file changed three times while I reviewed it — four revisions observed; it is untracked
(`?? plans/round30_defects.py`), so no commit pins any revision.

| revision | sha256 | lines | note |
|---|---|---|---|
| A | `9a7040648efa097eed27f1ca049a2b8eb68c5a53e588406b4c9bb06bec8f6429` | 167 | first read (D1 greened on `entries=0`+`exit=1` substring) |
| B | `a708abac5134d63db390865b3ba475ab9761fd575796f4859aee34ff63413ad0` | 194 | D1 line-exact, D2 count, D5 note length |
| C | `e565468da8e6d258f254263d4927ce7ea06dc7dd482a1b9f6eb7f221424f9380` | 216 | D1/D4 judged at HEAD; **D2 unsatisfiable (see §4)** |
| **D (pinned)** | **`19ce5332c571903be8e6e3dc679563241c745a4483465abaefb133fd969d982b`** | 220 | D2 scope-on-raw + line-unit count + `hits?` |

`main()` prints no revision stamp, so a `defects=0` line cannot say which of these four revisions, nor
which `HEAD`, produced it — while this very file changed under a reviewer inside ten minutes.

**S1 (report §3) is the fix: print the checker hash and `git rev-parse HEAD` with the tally.**

Live lane verdict at 04:37 with the pinned revision (read-only, `--lane .`):

```
DEFECT D1 receipt-at-cited-path: receipt exists only in the worktree: corpus/evidence/round29-attempt2/control-nothing.txt is not committed at HEAD
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
DEFECT D4 uncommitted-wave-evidence: HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md omits the addendum ('### D. Addendum'); the wave evidence is not landed
ok D5 s091-usedby-asymmetry: repaired
defects=2
```

D1 and D4 are correctly red on the lane's unfinished state (the receipt is untracked; the addendum is
modified in the worktree but not landed at HEAD). Those two are the lane's remaining work, not
checker defects.

## 1. Per-check red condition and gaming verdict

"Red iff" is read off the pinned source at the cited lines. Every claim marked ✔ is a run whose
output is pasted; claims marked *(read)* are source reading only.

### D1 — receipt at the cited path (`check_d1`, :73-89)
Red iff: no worktree file at `corpus/evidence/round29-attempt2/control-nothing.txt`; or `HEAD:<path>`
unreadable (`head_blob` returns `None`); or the committed blob does not carry
`QUOTED_LINE` (the seven-field control line) as a **whole line**; or does not carry `WAVE_LINE` (the
eight-field wave variant) as a whole line; or carries neither `exit=1` nor `exit code of that run: 1`.

Gaming verdict: **partly gameable — the passing specification is the checker's own two constants, so a
transcript can be hand-typed.** A forged receipt that also contradicts itself passes ✔:

```
  forged receipt, self-contradicting pass line, no run re-derived: GREEN
```

(forged bytes: `# hand-typed, never produced by a run` + `QUOTED_LINE` + `WAVE_LINE` + `exit=1` + a
*passing* line `entries=3 … census=ok` + `exit=0`). Real hardening over revision A, which a two-line
file passed and which greened on an uncommitted `??` receipt — both verified on `9a70406`:

```
  fabricated 2-line receipt, no git repo, no report file: GREEN
  bytes: 'entries=0\nexit=1\n'
```

and over B, where `QUOTED_LINE` as a substring (not a line) sufficed.

Not checked at all: the report. D1 never opens `.ufo/reports/round-29/kengaku.md`, yet the routed
defect is *that report* citing a path that did not exist. If the lane had instead edited the report to
cite the wave path (the closure's other branch), D1 would stay red: only one of the two repairs is
reachable.

**Tighten:** (i) require `WAVE_LINE.replace("verified_at=0 ", "") == QUOTED_LINE` in-check and require
the receipt's `WAVE_LINE` to equal line 3 of the committed
`.ufo/waves/round-29/attempt2/control.nothing.txt` — an artifact the lane did not author this round;
(ii) forbid any *other* `entries=`/`exit=` line in the receipt, so a contradicting pass line cannot
co-exist; (iii) read the report and require the path it cites to equal `D1_PATH`.

### D2 — kappa sweep scope and count (`check_d2`, :92-118)
Red iff: no lesson line contains `kappa`; or some kappa line contains `in the lane` after stripping
`**`/`__`; or some kappa line lacks the literal `corpus/knowledge/*.md` in the **raw** line; or no
`→ <n> hit(s)` appears in the joined kappa lines; or `n` ≠ the number of lines containing `kappa` under
`corpus/knowledge/*.md`.

Gaming verdict: **sound at the level it claims, with two residual holes and one brittleness.**
Verified on the pinned revision (fixture: one knowledge file holding `kappa kappa on one line`, so
grep line count is 1 and occurrence count 2):

```
  lesson '→ 1 hit'  vs grep line count 1 / occurrences 2: GREEN
  lesson '→ 2 hits' vs grep line count 1 / occurrences 2: RED → kappa sentence states 2 hits, corpus/knowledge/*.md holds 1
  lesson '→ 1 hits' vs grep line count 1 / occurrences 2: GREEN
  wrong count '→ 0 hits' against 1 line: RED → kappa sentence states 0 hits, corpus/knowledge/*.md holds 1
```

Residual holes:
- the sentence's *lane-wide* figure is still not re-derived. On revision A the lesson claimed "finds 65
  files" lane-wide while the lane held 66 (`git grep -li kappa` → **65 at `2ff4b6f`**, 66 at `363a4eb`
  and at HEAD). The pinned lesson now states both numbers and names the extra file — fixed by the
  author, not by the checker.
- the count token must be introduced by `→`; an ASCII `-> 1 hits` with the right count is red
  (`kappa lines carry no '<n> hits' count to re-derive`). A reflow that uses `->` fails a true
  sentence.

**Tighten:** accept `→|->`; re-derive the lane-wide figure too when the sentence names one
(`len(git grep -li kappa)`); normalise wrapped lines (`" ".join(lesson.split())`) before the phrase
tests so formatting cannot decide the verdict.

### D3 — S078 line-75 word count (`check_d3`, :121-143)
Red iff: `cell(registry,"S078")` is not exactly 11 cells; or the anchor cell has no
`"QUOTE" (N words)`; or `N != words(QUOTE)`; or the lesson has no `"QUOTE" — N words`; or its `N` is
wrong.

Gaming verdict: **not gameable in its arithmetic; tautological as an oracle; real anchor gap.**
`8` is `len(QUOTE.split())` over a string literal in the checker — the expected value is defined by the
constant, and nothing confirms `QUOTE` is a byte substring of S078 at `66f92766`, nor that it sits at
line 75. Moving the citation while keeping the count is green ✔:

```
  count 8 kept, cited line 75 -> 951 in both files: GREEN
```

The symmetric false red: a correctly-counted 8-token re-read of the same source line is rejected,
because `QUOTE` is frozen in code ✔:

```
  8-token re-quote of the same source line: RED -> S078 anchor cell carries no word count for the line-75 quote
```

**Tighten:** extract the quote and its count from the cell, compute `words()` from the extracted
string, require the `line 75` token, and require the quote to be a byte substring of the S078 payload
(the registry already pins `sha256 dde4168f…8231f`, 6858 bytes — checkable offline once the blob is
cached under `corpus/evidence/`).

### D4 — uncommitted wave evidence (`check_d4`, :148-165)
Red iff: the worktree file is absent; or `HEAD:<path>` unreadable; or the committed blob lacks the
15-byte marker `### D. Addendum`; or `git status --porcelain -- <path>` is non-empty.

Gaming verdict: **gameable — the evidence can be destroyed and the check stays green.** The marker is
the entire content contract (the real addendum is 714 lines / 64224 bytes; the marker sits at line
694) ✔:

```
   real addendum: lines=714 bytes=64224; marker index line=694
   committed blob: bytes=16
  marker-only committed blob (62894 bytes -> 15 bytes), status clean: GREEN
```

(The label's `62894 bytes` is my probe's leftover text; the measured committed blob is 16 bytes.)
Two states the HEAD read correctly closes, both verified:
- untracked + gitignored, `git status --porcelain` silent — GREEN on revision A, now RED ✔:

  ```
  addendum untracked at HEAD and gitignored (status silent): RED -> .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md is not committed at HEAD
  ```
  (`HEAD blob present: False`, `status --porcelain -- path => ''`, so revision A's status-only test
  was blind by construction.)
- committed then cleaned from the worktree — RED ✔
  (`committed addendum deleted from the worktree: RED -> … is absent altogether`), which is
  over-strict: trackedness is the routed question.

**Tighten:** pin content instead of a marker — require the blob's byte count / line count to match the
round-29 measurement, or `sha256(HEAD blob)` equal to the addendum's sha256 recorded in wave evidence;
and replace the worktree precondition with `git cat-file -e HEAD:<path>`.

### D5 — S091 used-by asymmetry (`check_d5`, :167-200)
Red iff: `adoption-expect.json` absent; and the entry carries no `^source: S091` line; or
`usedby_notes` has no `S091`; or the note is not a `str` of ≥10 words naming the entry; or the S091 row
is not 11 cells; or its used-by cell does not name the entry. (The `source: S091` branch returns
`""` immediately — no registry, no URL, no locator check.)

Gaming verdict: **partly gameable — the alternative branch is a bare token, and the note is prose
about a relation nothing verifies.**

```
  bare 'source: S091' line, no URL/locator (siblings all carry one): GREEN
   note words=13, names entry=True
  vacuous note naming the entry, asserting no relation: GREEN
```

The entry's other five source lines each carry `— https://… — locator — commit`; a bare
`source: S091` satisfies D5 while the entry still does not rest on S091. The note branch is a
word-count-and-substring test on free prose (the 5-word, 10-word-short case is red ✔:
`the S091 note is empty, too short to be a record, or does not name the entry`).

**Tighten:** on the source branch require the sibling shape (`^source: S091\b.*https?://` plus a
locator) and keep the registry used-by check; on the note branch, make the predicate the *fact* — the
registry's S091 anchor quote must appear byte-for-byte in the entry's prior-art section (it does today:
`corpus/knowledge/benchmark-task-validity-checklist.md:105`), not the prose that says so.

## 2. The two mandated junk edits

Copy: `/tmp/r30-R30RevCounter/lane3` — the pinned checker plus the six files the five checks read
(`corpus/lessons/round-29.md`, `corpus/SOURCES.md`,
`corpus/knowledge/benchmark-task-validity-checklist.md`,
`corpus/evidence/round29-attempt2/control-nothing.txt`,
`.ufo/waves/round-29/attempt2/adoption-expect.json`,
`.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md`), `git init` + one commit. The lane was never
written to. Baseline before any edit:

```
== BASELINE (rev 19ce533) ==
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
exit=0
```

A green baseline is what makes the two probes interpretable: each red below is attributable.

### 2.1 Junk edit (a) — delete the kappa sentence instead of scoping it

The sweep sentence in the `judge-calibration-thresholds.md` bullet is removed, leaving "kappa and a
test–retest ceiling. Routed defect D2," (`1 insertion, 4 deletions`).

```
== JUNK EDIT (a) on rev 19ce533: kappa sentence DELETED, not scoped ==
1	4	corpus/lessons/round-29.md
ok D1 receipt-at-cited-path: repaired
DEFECT D2 kappa-sweep-scope: kappa line names no measured scope (corpus/knowledge/*.md)
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=1
exit=1
```

Verdict: **red for the right reason, and only D2 moves.** `kappa` survives in "per-variable kappa" on
the same line, which now carries no measured scope, so the branch fires. A deletion that removed every
kappa line would hit the explicit `no kappa line in the lesson` return instead — also red *(read)*.
There is no way to green D2 by deleting the claim.

### 2.2 Junk edit (b) — S078 count rewritten to a wrong-but-equal number (8 → 9, both files)

```
== JUNK EDIT (b) on rev 19ce533: S078 line-75 count 8 -> 9 in BOTH registry and lesson (wrong but equal) ==
1	1	corpus/SOURCES.md
1	1	corpus/lessons/round-29.md
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
DEFECT D3 s078-line75-word-count: registry S078 prices the line-75 quote at 9 words, actual 8
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=1
exit=1
```

Verdict: **red for the right reason.** Agreement between the two files does not launder a wrong number,
because each is compared to the computed count rather than to the other. (The lesson-only branch,
`lesson prices the line-75 quote at N words …`, is a separate return — read, not run; the registry
branch short-circuits first, which is why this run names the registry.) The residual weakness stays
§1 D3: the "computed count" is a constant, so what is pinned is arithmetic, not the citation.

## 3. Structural findings (pinned revision)

- **S1 — no revision stamp.** (See §0.) Add `HEAD` sha and the checker's own hash to the output.
- **S2 — crash instead of a verdict on malformed input.** `check_d2`/`check_d3`/`check_d5` read files
  unguarded; a lane missing the lesson exits with a traceback and **no** `defects=` line:
  `exit: 1 | stdout: DEFECT D1 … receipt absent at the cited path …` then
  `stderr: FileNotFoundError: … '/tmp/…/crash/corpus/lessons/round-29.md'`. Fail-closed but
  unparseable, and the four remaining checks never report. Guard each check and return a reason.
- **S3 — `cell()` splits on a bare `|` and demands exactly 11 cells**, with a misleading message. All
  82 rows are 11 cells today (`rows: 82 not-11-cells: []`), but one literal pipe inside a quote turns
  D3/D5 red naming the wrong cause ✔:
  `one literal pipe in the S078 anchor cell: RED -> S078 row missing or not 11 cells`.
  Split on an unescaped pipe (`re.split(r"(?<!\\)\|", …)`) and name the real reason.
- **S4 — docstring claim is false.** "none reads an artifact round 30 creates, so C2 stays separable
  from C1". D1 judges a receipt round 30 created (`git log -- corpus/evidence/round29-attempt2/
  control-nothing.txt` is empty) and D5 judges `usedby_notes`, added to `adoption-expect.json` this
  round. Separability from the C1 card holds — no check reads the contamination-transparency entry —
  but the sentence as written does not.
- **S5 — first-offending-line reporting in D2.** The loop returns on the first bad kappa line, so a
  multi-line defect costs one fix cycle per line.

None of these is load-bearing for a *false green* except S3 (wrong diagnostic) and S1 (unanchored
receipt); S2 is a robustness cost.

## 4. Build history: a fatal revision the gate itself could not report

Revision C was **unsatisfiable**: `plain = re.sub(r"[*_`]", "", raw)` stripped the `*` out of the glob
and then tested for the glob in the stripped text, so D2 could never be green and `defects=0` was
unreachable. Measured on C:

```
emphasis-strip result: '  grep -rn kappa corpus/knowledge/.md → 0 hits at the scope'
glob literal after strip: False
A minimal, no emphasis at all: RED -> kappa line names no measured scope (corpus/knowledge/*.md)
```

Consequence: on C, junk edit (a) and the correct repair produced the identical verdict — the check had
become a constant, and the lane's own gate could not distinguish a deletion from a scoped sentence.
Revision D changed exactly those three things — the scope test moved to `raw`, the count moved to
`grep` line units, and `hits?` — which is what I had reported to the seat (`L1Kengaku30`) at the time;
whether that message or an independent pass produced it, §2.1/§1 D2 are the verification of the bytes:
green on the correct lesson, red on the deletion, red on a wrong count, green on the true `1 hit`.
**This is exactly what S1 exists to prevent**: nothing in the output of revision C said which revision
was speaking.

## 5. Residual risk and verification gaps

- The pinned revision is **untracked and still moving**. Any property above can change with no commit;
  a `defects=0` receipt from any revision cannot be tied to the bytes that produced it.
- D1's receipt and D5's note are artifacts the lane authors about itself. No check here can prove a
  counter run happened; at best it can tie the transcript to an artifact the lane did not write this
  round (the committed wave control file). I did **not** run `plans/adoption_check.py` against a
  `git archive` of `1f3b0f1`; the receipt's provenance sentence ("both forms were reproduced … from a
  scratch `git archive`") is unverified by me.
- I did not fetch S078 this round: `8 words` is checked against the lesson, the registry and
  `len(QUOTE.split())`, not against the source. That the quote sits at `v2/README.md` line 75 is the
  round-29 spot-check's live fetch, not mine.
- The lane-wide kappa figures I *did* measure: `git grep -li kappa` → 65 at `2ff4b6f`, 66 at `363a4eb`
  and at HEAD; `grep -rn kappa corpus/knowledge/*.md` → 0 lines. Committing this checker (it mentions
  `kappa` in its own docstring) and round-30 wave files will move the lane-wide number again — which is
  why the lesson should not carry a bare count and the checker should derive it.
- Out of this seat's target: `plans/sources_adopt.py` quote validation (C3) and the C1 amendment.

## 6. What I ran; hygiene

- Ran: the pinned checker on the live lane (read-only) and on `/tmp` slices; the two mandated edits;
  predicate-level probes on synthetic roots under `/tmp/r30-R30RevCounter/pin/` (each a copy of the
  slice, never the lane); `git grep`/`grep` counts for every kappa figure; a registry cell-count survey
  over all 82 rows.
- Read, not run: the round-29 spot-check §5 defect wording, the D1-D5 closure text, the receipt and
  `adoption-expect.json` contents, and the branches explicitly labelled *(read)*.
- Hygiene disclosure: my first inspection imported the checker in-process (04:24), which wrote
  `plans/__pycache__/round30_defects.cpython-314.pyc` inside the lane (embedded source size 6513, i.e.
  the then-current revision). I deleted it; when I checked the tree again at the end a file with the
  same preserved mtime was present (it may have been restored by another seat's `cp -a`, or my first
  removal did not persist), so I removed it a second time and verified `plans/__pycache__/` holds only
  the pre-existing `adoption_check`/`sources_adopt` pycs. `__pycache__/` is gitignored either way.
  Every measurement after 04:24 used `python3 <path>` as a subprocess or `sys.dont_write_bytecode`.
  No other lane byte was created, edited or deleted; my only lane write is this report.
- Tools installed or upgraded: none (no pacman transaction; PACMAN PAUSED respected).
