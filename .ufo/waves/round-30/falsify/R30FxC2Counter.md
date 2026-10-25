# R30FxC2Counter — C2's counter attacked after the repairs

Seat: `L1Kengaku30.R30FxC2Counter-3` (leaf, no dispatch). `writer: L1Kengaku30.R30FxC2Counter-3`
(role: critic). Lane: `kengaku-shokunin`, round 30 falsify wave, 2026-10-25.
Target: `plans/round30_defects.py` against `corpus/lessons/round-29-verifier-spotcheck.md` §5 (D1–D5).
Axis: **calibration**. This seat is neither a source re-read nor the complete-set review, so it carries
no `VERDICT:` line and no candidate path.

Substrate: `/tmp/r30fx-c2/base` — a `cp -a` byte copy of the lane (548 MB incl. `.git`), with the
round-30 worktree committed in one commit, **`c4bd7c2`**, so all five repairs are *landed* in the copy.
Lane HEAD was `363a4eb`; the lane worktree is dirty (15 entries) and was never touched: the only lane
write this seat makes is this file. Tooling installed: **none** (no pacman, no `uv`, no binary).
Every run below was executed by me; nothing is accepted from a build report.

---

## 0. Baselines

Landing the wave's own bytes in the copy and running the counter:

```
===== BASELINE: lane worktree committed at c4bd7c2 =====
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

So `defects=0 / exit 0` is reachable and the 5→0 ladder is real. The *live* lane at pick-up:

```
DEFECT D1 receipt-at-cited-path: receipt exists only in the worktree: corpus/evidence/round29-attempt2/control-nothing.txt is not committed at HEAD
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
DEFECT D4 uncommitted-wave-evidence: HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md omits the addendum ('### D. Addendum'); the wave evidence is not landed
ok D5 s091-usedby-asymmetry: repaired
defects=2
EXIT=1
```

which matches sibling `R30FxC2Recheck` (F1) — `defects=2` at HEAD, none of the three "ok" repairs committed.
That is context, not a survivor: the interesting question is what `defects=0` *means*, and that is below.

---

## 1. The five assigned mutants, verbatim output

### (a) a directory planted at the D1 path — defect deliberately not repaired

```
===== A. directory planted at the cited D1 path (defect deliberately NOT repaired) =====
  drwxr-xr-x 2 vgpnk vgpnk 6 Oct 25 04:42 /tmp/r30fx-c2/base/corpus/evidence/round29-attempt2/control-nothing.txt
DEFECT D1 receipt-at-cited-path: receipt absent at the cited path corpus/evidence/round29-attempt2/control-nothing.txt
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=1
EXIT=1
```

Caught (`is_file()` is False). But the *same commit* answers differently in a clone, because the gate
reads the worktree, not the blob:

```
===== A2. same commit c4bd7c2, fresh clone (no planted directory) =====
c4bd7c2
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

One commit, two verdicts. `check_d1`'s own comment says it judges the HEAD blob; its first gate judges the
host's worktree. The message "receipt absent at the cited path" is also false here: the receipt *is*
committed, at that path, with the quoted line.

### (b) committed D1 receipt whose seven-field line is wrong by one token

```
===== B. committed D1 receipt, seven-field line wrong by one token (entries=0 -> entries=1) =====
  line 3 now: entries=1 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped
DEFECT D1 receipt-at-cited-path: the committed receipt does not carry the report's quoted seven-field line verbatim
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=1
EXIT=1
```

Caught.

### (c) the kappa sentence deleted instead of scoped

```
===== C. kappa sentence deleted instead of scoped =====
  deleted 373 bytes
  kappa lines left: 0
ok D1 receipt-at-cited-path: repaired
DEFECT D2 kappa-sweep-scope: no kappa line in the lesson: the sweep the closure narrowed is gone
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=1
EXIT=1
```

Caught (the empty-kappa-line guard fires).

### (d) the D5 note re-keyed

```
===== D. D5 note re-keyed: usedby_notes.S091 -> usedby_notes.S091-asymmetry =====
  keys: ['S091-asymmetry']
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
DEFECT D5 s091-usedby-asymmetry: adoption-expect.json records no S091 used-by asymmetry note and the entry cites no S091
defects=1
EXIT=1
```

Caught (dict membership on the exact key).

### (e) a D4 blob committed without the addendum

```
===== E1. D4 addendum section (marker + body) deleted and committed =====
  marker at line 694 of 714; deleting through EOF
  marker occurrences: 0
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
DEFECT D4 uncommitted-wave-evidence: HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md omits the addendum ('### D. Addendum'); the wave evidence is not landed
ok D5 s091-usedby-asymmetry: repaired
defects=1
EXIT=1
```

Caught in this form. The same repair, committed so that the heading survives, is not caught — §2.

**Score on the five literal mutants: 5/5 caught.** The counter's literal predicates work. The
counterexample is that each one is a string proxy or a host-state test, so five neighbours of the same
defects pass with `defects=0`. Scratch: `/tmp/r30fx-c2/battery.sh`, full log `/tmp/r30fx-c2/log.txt`.

---

## 2. Seven further mutants: what still passes with the defect unrepaired

### B2 — D1: a falsified control line committed *beside* the quoted one → PASS

```
===== B2. the falsified line kept AND the quoted line restored beside it =====
  3:entries=1 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped
  4:entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped
  10:entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 verified_at=0 census=skipped
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

The receipt now records the same run as both 0 and 1 entry, and the counter reads `QUOTED_LINE in lines`
— an existence test, not a uniqueness test. A reader re-deriving from that receipt gets two answers.

### C2 — D2: the falsified claim kept, one word swapped → PASS

```
===== C2. falsified claim kept, scope word swapped: 'in the lane' -> 'lane-wide' =====
  planted: kappa and a test–retest ceiling — `grep -rn kappa corpus/knowledge/*.md` → 0 hits lane-wide.
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

Ground truth measured by me, read-only, in the lane: `git grep -li kappa` → **66** at HEAD `363a4eb`,
**67** in the live worktree (the dirty `LOG.md` is the extra), `corpus/knowledge/*.md` → **0**. So the
sentence's claim is false by 66 files and the counter certifies it. This is sibling
`R30FxC2Recheck`'s M1 survivor ("across the whole lane") reproduced independently with a different
synonym: the D2 test is a literal `"in the lane"` filter, and any re-wording evades it.
(My baseline's `git grep` reports 82 only because `c4bd7c2` commits the round-30 wave directory, which
the lane has untracked; 66/67 is the lane figure.)

### D2' — D5: note re-keyed away **and** a non-frontmatter `source: S091` line planted → PASS

```
===== D2. note re-keyed AND a non-frontmatter 'source: S091' line planted in a code fence =====
  frontmatter source lines: ['S077', 'S078', 'S079', 'S080', 'S090']
  110:source: S091
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

The asymmetry record is deleted and the entry's real `source:` block still carries five rows, but
`re.search(r"^source:[ \t]*S091\b", entry, re.MULTILINE)` matches a line inside a fenced block. The
"cite it as a source" branch of D5 is a text pattern anywhere in the file, not a frontmatter row — and
the entry's source block is a bare `source:` list, so nothing else distinguishes frontmatter from prose.

### E2 — D4: the addendum body dropped, the heading kept → PASS

```
===== E2. addendum body dropped, heading kept: a D4 blob without the addendum =====
  drops 1286 bytes of body, keeps the heading
  blob bytes: baseline 64749 vs mutant 63468
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

The heading line (75 characters) and 1286 characters of body — the `275/4/279` identity verification, the
per-file prefix loop, the "Audit state at close" paragraph, i.e. the whole reason the wave evidence
existed — are replaced by an 86-character stub; the blob goes 64749 → 63468 bytes. `D4_MARKER in text` is
satisfied by the heading prefix alone, so "the wave evidence is landed" is certified by a 24-character
substring.

### F — D2/D3/D5 do not bind to landed bytes → PASS with the defect at HEAD

```
===== F. the D2 defect committed at HEAD, worktree left repaired ( M corpus/lessons/round-29.md ) =====
  HEAD: 1 occurrence(s) of 'in the lane'
  worktree: 0 occurrence(s)
  status:  M corpus/lessons/round-29.md
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

The original D2 sentence — `grep kappa` → "0 hits in the lane" — is what is *landed*; the worktree merely
holds the repair. `check_d1`/`check_d4` read `HEAD:` blobs; `check_d2`/`check_d3`/`check_d5` read
`lane/<path>`. Sibling F3 recorded the passive form of this (three verdicts rest on uncommitted bytes);
this is the active form: the counter certifies a repair the commit tree does not contain, so a lane can
land the defect and pass by keeping the fix uncommitted. Against §C2's own predicate ("`defects=0` on the
repaired tree") the tree is not what is measured.

### G1 — D3: a second price for the same quote in the same lesson → PASS

```
===== G1. lesson carries 8 words in the table and 9 words for the same quote at EOF =====
194:| S078 | https://raw.githubusercontent.com/scaleapi/SWE-
246:Retained note: the same line-75 quote "The verifier never runs in the agent's sandbox." — 9 words
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

(the two grep lines are shown as the log printed them, truncated by the driver's `cut -c1-60`/`-c1-90`;
line 194's cell is `"731 -> 642 tasks: 89 dropped after review." — 8 words, line 99; "The verifier never
runs in the agent's sandbox." — 8 words, line 75`, line 246 the appended 9-word price for the same quote.)

D3's defect was "prices the line-75 quote at 9 words". The mutant writes "9 words" for that exact quote
into the same file and passes, because `D3_LESSON_RE.search` takes the first match. `.search` is the same
existence-not-uniqueness flaw as B2.

### H — one line added to C1's entry flips C2's verdict → false DEFECT

```
===== H. one kappa sentence added to the C1 entry; the D2 sentence untouched =====
  scoped count now: 1
ok D1 receipt-at-cited-path: repaired
DEFECT D2 kappa-sweep-scope: kappa sentence states 0 hits, corpus/knowledge/*.md holds 1
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=1
EXIT=1
```

The docstring says: "Each check is a command over committed/live lane bytes; none reads an artifact round
30 creates, so C2 stays separable from C1 (QUALITY R13)". D2 re-derives its count over
`corpus/knowledge/*.md` — precisely the directory C1 lands its entry in. If the C1 card had mentioned
kappa (a canary/Greek-letter vocabulary is on-topic for a contamination card), C2 would report a defect
for a D2 repair that is intact. The separability sentence is false in one direction; it should say
"reads no round-30 artifact by name; D2's scoped count is measured over the surface C1 writes".

---

## 3. Per-check verdict

| check | assigned mutant | result | does a neighbour pass unrepaired? | smallest safe correction |
|---|---|---|---|---|
| **D1** receipt-at-cited-path | (a) dir, (b) one-token line | caught | **YES** — B2 (falsified line beside the quoted one); A/A2 (verdict moves with the worktree, not HEAD) | require *exactly one* seven-field and *exactly one* eight-field control line (`lines.count(QUOTED_LINE)==1 and lines.count(WAVE_LINE)==1` and no third `^entries=\d+ .* census=` line); drop the `is_file()` gate to a note, since `head_blob` is the authority it claims to be |
| **D2** kappa-sweep-scope | (c) delete sentence | caught | **YES** — C2 (`lane-wide`), F (defect at HEAD, repair in worktree), H (C1 bytes move the count) | (i) read the lesson from `head_blob` like D1/D4; (ii) replace the `"in the lane"` filter with a re-derived bound: if a kappa line mentions `lane`, every `→ N` on it must equal the lane-wide count (`git grep -li kappa` at HEAD → 66); (iii) recompute the scoped count against the pinned round-29 revision `2ff4b6f`, not the live tree, so C1 cannot move it |
| **D3** s078-line75-word-count | — (not assigned) | — | **YES** — G1 (8 and 9 for one quote in one file) | require *all* prices to agree: `{int(m[1]) for m in D3_LESSON_RE.finditer(lesson)} == {words(QUOTE)}`, and the same for the parenthesised form in the lesson, not only in the registry cell |
| **D4** uncommitted-wave-evidence | (e) blob without addendum | caught (E1) | **YES** — E2 (heading kept, 1286 bytes of body gone) | probe the body, not the heading: require `"275 + 4 = 279"` and `"Audit state at close"` in `HEAD:<path>`, or the addendum byte length (64749) as a floor |
| **D5** s091-usedby-asymmetry | (d) re-keyed note | caught | **YES** — D2' (re-key + fenced `source: S091`) | restrict the source test to the frontmatter block: `front = entry.split("\n\n", 1)[0]` then `re.search(r"^source:[ \t]*S091\b", front, re.MULTILINE)` |

## 4. Does any check still pass without its defect repaired?

**Yes — all five, each through a different door.** `defects=0` / exit 0 does not entail that D1–D5 are
repaired:

- **D1** — commit the falsified `entries=1` line next to the quoted one (B2). The quoted line is present,
  so the receipt is "repaired" while it records two contradictory results for one run.
- **D2** — keep the false claim and write "lane-wide" instead of "in the lane" (C2); or land the original
  defect and keep the repair in the worktree (F). The sentence the round-29 verifier routed ("renders the
  sweep as 0 hits in the lane") survives one word away, and the verdict does not bind to committed bytes.
- **D3** — write a second price of 9 words for the same quote somewhere later in the lesson (G1).
- **D4** — commit the file with `### D. Addendum` and no addendum (E2); the heading and 1286 characters of
  body replaced by an 86-character stub, verdict still "repaired".
- **D5** — delete the asymmetry note and plant `source: S091` in a code fence (D2').

For the canonical judge: the four survivors are **fixable defects** — each is a one-line tightening
(§3), and the 5→0 ladder is verified reachable. The claim that must be **rejected as written** is narrower:
`defects=0` is not evidence that D1–D5 are repaired, and the module's separability sentence from C1 is
false for D2. Until the tightenings land, C2 can be admitted only as "five literal predicates reproduce",
never as "the five repairs re-derive".

## 5. Axis impact

- **calibration — harmed if the survivor set ships.** A check that certifies a gutted addendum (E2), a
  self-contradictory receipt (B2) and a double-priced quote (G1) is a check that has stopped discriminating:
  the exact failure mode this lane's mistake register calls a survivor (M90). The counter's own history
  shows it already killed three such mutants; these four are the same class, one level up.
- **quality — subtle.** Nothing here harms the five repairs themselves (exact per sibling F7 and B/C/D/E1
  above); what is harmed is the assertion that the counter's zero *means* repaired.
- **coverage / depth / novelty / freshness / adjacency — untouched.** No production byte, no registry row,
  no entry is changed by this review.

## 6. Not covered, and honesty limits

- **D3's provenance is circular and was not falsified further**: the counter prices its own hardcoded
  `QUOTE` constant; no byte copy of the SWE-bench Pro `v2/README.md` exists under `corpus/evidence/`, only
  prose in `build/R29a2RevQuoteS078.md` (line 68 shows the raw line, line 72 the substring test). So D3
  can only prove "row, lesson and constant agree", never "the constant is line 75". Out of this item's
  scope; recorded because it is the same false-provenance shape.
- **Overlap with `R30FxC2Recheck`**: their M1 (D2 literal test) and F3 (mixed substrate) are the same
  findings as C2 and F; I reproduced both independently rather than inheriting them, and did not repeat
  their M2/M4/M5/M6.
- **My `/tmp` baseline commits the round-30 wave**, so counts taken there (e.g. lane-wide kappa 82) are
  not lane figures; every lane figure quoted above was measured in the lane, read-only.
- The counter's `git status --porcelain` test in D4 means a dirty worktree can never pass; that is intended
  for D4 and is the one place the layer is stated. No other check states one.
