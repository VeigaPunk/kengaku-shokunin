# R48C2ScribeEntry — r46 C3 entry wording repair after the Q40 review (drafted, not applied)

REV a543d92083557dd9b33ee674e9b99b03411f80af (stage-1 freeze; the entry bytes quoted here are identical at that
commit, at lane tip `bf783c1` and in the worktree — `sha256 4c05769fd8b43905e1b84873fafc53e61c18f1e4cba031392953b564200a6073`).
Seat role: scribe, serving R48-C2 (coverage). Date 2026-10-27. Item: draft precise edits repairing the r46 C3 entry
wording after the Q40 review — the V7/V8 admissions, the unadmitted status and the condition under which it lifts —
preserving negative scope and asserting no pass.

**Axes named:** coverage (the only axis this item can move; the repairs change no count, no capture, no probe).

## Freeze / ordering gate (answered before any measurement)

I ran **no scored counter or probe execution** — neither `plans/round46_c3_verify.py`, nor
`plans/polyglot_c_py_probe.py`, nor any wave-1 candidate counter. That is not merely the seat bound; the round-48 C2
counter does not exist yet, so no scored run of it is possible:

- `git ls-tree -r --name-only a543d920 plans/ | grep -E 'round48|polyglot'` → `plans/polyglot_c_py_probe.py`
  only. There is no `plans/round48_c2_verify.py` in the committed tree.
- `git show a543d920:plans/round-48-claims.md | grep -nE '<V>|<N>|<P>|<H>|<S>|<B>|<M>'` → the frozen predicate still
  carries the stage-2 placeholders (`checks=<V> defects=0`, `<V>`/`<N>` "fixed at stage 2", claims lines 104-110).
- `git log --oneline a543d920..HEAD -- plans/round-48-claims.md` → empty: no stage-2 amendment commit, so the
  claim is still pre-literal, pre-pin, pre-data.

Consequence for this item: **no pass assertion is even representable**. Every drafted sentence below says the
package is withheld and names the lift condition as a condition. Nothing in this report upgrades an unobserved run
into evidence, and nothing here re-freezes, weakens or re-labels any predicate, kill rule or control.

## Evidence base (verbatim, from committed bytes; no external URL opened)

Access date 2026-10-27 for every row below. Lane-local sources carry `path:line` in place of a URL (the lane has no
public remote); each prose quote is a located fragment of ≤25 words, and the long quoted lines are tool output
(counter/control receipts) reproduced verbatim because the line itself is the evidence.

I opened no network source this round. The wording repair is against committed lane bytes and the committed round-46
counter output; the entry's own external citations (S166-S172 at `2fd12b88`) were **not** re-fetched by this seat, and
this report makes no claim about them. All reads below are at `a543d920` (worktree clean, entry digest identical).

| Source opened (lane path) | Quoted bytes (verbatim) |
|---|---|
| `corpus/knowledge/tb2-polyglot-c-py-grader.md:36-39` | `first recorded after the stage-2` / `freeze `4fdeebaa` (QUALITY Q30)` |
| `corpus/knowledge/tb2-polyglot-c-py-grader.md:75-79` | `no label can be derived for them — they are listed below as `not exercised`, and the counter's `V7` reports` / `them as a defect` |
| `corpus/knowledge/tb2-polyglot-c-py-grader.md:86,89` | `\| instruction.md:7 \| both-print \| not exercised \| no frozen case violates it \|` (and the same shape for `instruction.md:9`) |
| `corpus/knowledge/tb2-polyglot-c-py-grader.md:307-308` | `map's coverage of `instruction.md:7,9` is partial and the counter's `V7` reports it.` |
| `corpus/knowledge/tb2-polyglot-c-py-grader.md:312-321` | `## Errata (round 46, wave 2)` … items 1-2 (class contrast; unexercised `f(1)`) |
| `.ufo/waves/round-46/integrate/c3-landing.txt:21` | `V7 DEFECT rows=5 tags=7 bad=["unparsed row '\| instruction.md:7 \| both-print \| not exercised \| '", "unparsed row '\| instruction.md:9 \| toolchain \| not exercised \| n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]` |
| `.ufo/waves/round-46/integrate/c3-landing.txt:22` | `V8 DEFECT order_exit=1 result=not-PASS` |
| `.ufo/waves/round-46/integrate/c3-landing.txt:35-36` | `checks=13 defects=2` / `PREDICATE C3 fail` |
| `.ufo/waves/round-46/integrate/c3-landing.txt:42-44` | `ORDER HIT .ufo/waves/round-46/claims/control-c3-echo.txt@4fdeebaa546c:15 kind=gate-p10` / `ORDER FAIL probe-executed-before-receipt hits=1` / `ORDER RESULT FAIL` |
| `.ufo/waves/round-46/claims/control-c3-echo.txt:4` | `ENVELOPE start 02:32:09 cwd=/fast/scratch/hyaku/kengaku-r46/L1/s2/control-c3-echo/lane` |
| `.ufo/waves/round-46/claims/control-c3-echo.txt:15` | `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt` |
| `plans/round46_c3_verify.py:135` | `MAP_ROW` row regex: the tag cell must be a backticked lowercase slug and the label cell exactly one of `enforced`, `unenforced`, `partly`; any other `instruction.md:` row is appended to `bad` as `unparsed row` (`:390`) |
| `plans/round46_c3_verify.py:390` | `bad.append(f"unparsed row {line[:50]!r}")` |
| `plans/round46_c3_verify.py:400-401` | `if not violating:` / `bad.append(f"{tag}: no receipt case violates it")` |
| `plans/round46_c3_verify.py:413` | `return not bad, f"rows={sum(seen.values())} tags={len(tags)} bad={bad or 0}"` |
| `SCORECARD.md` §Round 46 wave-2 verdicts | `C3 \| coverage \| **not admitted** (V7, V8)` |
| `LOG.md:1471-1476` | `probe first recorded run after the amendment` … `V7 (two` / `frozen tags no case violates) and V8 (a stage-2 control ran the gate's P10 before the receipt)` |
| `corpus/lessons/round-46-verifier-spotcheck.md:43-45` | `C3:` / `freeze violating receipt cases for every requirement tag, make pre-receipt controls unable to run P10 … Keep the new knowledge unadmitted until the counter passes` |
| `corpus/QUALITY.md:1091-1093` | `Q40 — before a counter that derives requirement labels from a receipt is pinned, every `TAG` its frozen dry table` / `declares is carried by at least one frozen case's `violates=` set; and a control run before the first recorded probe` / `run never executes a leg that re-runs the probe.` |
| `.ufo/waves/round-46/w2/R46W2C3Entry.md` | `The requirement-map treatment of `both-print` and `toolchain` is transparent: it explicitly calls them “not exercised,”` (the wave-2 review treated the rows as honest annotation; it did not test them against `V7`'s row regex) |

Chronology supporting the V8 repair (`git log -1 --format='%h %ci %s'`):

```
4fdeeba 2026-10-27 02:32:46 -0300 round-46: stage-2 freeze amendment (C1 P=65 R=20 S=12, C3 V=13; C2/C3 control receipts, control runner)
8d7f74c 2026-10-27 02:33:05 -0300 round-46: C3 first recorded probe run (polyglot-c-py, 18 cases, mismatches=0) + receipt digest in spec
e9d2014 2026-10-27 02:37:26 -0300 round-46: C3 — polyglot-c-py package (entry, rows S166-S172, README index/coverage/frontier 12 of 89, PROVINCE, round-46 evidence index)
264b775 2026-10-27 03:16:44 -0300 round-46: wave-2 evidence (32 seats, 4 recovered outputs) + verdicts (C1 not admitted by kill rule, C2 predicate met, C3 not admitted), appended corrections, census after
```

`git log -S 'not exercised' --oneline -- corpus/knowledge/tb2-polyglot-c-py-grader.md` → `e9d2014`: the two
annotation rows are the entry's own landing bytes, not a later append. `git -C lane diff e9d2014 264b775 --
corpus/knowledge/tb2-polyglot-c-py-grader.md` → a single hunk that **appends** `## Errata (round 46, wave 2)` items
1-2 and nothing else, so the Summary sentence, the two `not exercised` rows and the "the counter's `V7` reports them
as a defect" prose were all present at the landing commit `e9d2014` and were not touched by wave 2.

## Findings

1. **The Summary's Q30 sentence is false in substance under V8.** `… first recorded after the stage-2 freeze
   `4fdeebaa` (QUALITY Q30)` (entry:38-39) reads as Q30 compliance, but the gate's fresh-probe leg ran at 02:32:09
   (`control-c3-echo.txt:4`) inside control receipt commit `4fdeebaa` (02:32:46), 56 s before the first recorded
   probe receipt commit `8d7f74c` (02:33:05). The order check proves it (`ORDER HIT …@4fdeebaa546c:15 kind=gate-p10`,
   `ORDER FAIL probe-executed-before-receipt hits=1`) and the counter's V8 fails on it. What is true is narrower: the
   receipt is the first *retained* probe output. The entry never mentions V8 at all.
2. **The Requirement map wording understates V7 by three defects to one.** The prose (entry:77-79) says the two tags
   "are listed below as `not exercised`, and the counter's `V7` reports them as a defect". `V7`'s committed line has
   three bad entries: two `unparsed row` (the rows themselves fail `MAP_ROW`, `plans/round46_c3_verify.py:135`) and
   `tags missing=['both-print', 'toolchain']` — `rows=5 tags=7`. Two independent regex failures per row: the tag
   cell is not backticked (`MAP_ROW` requires `` `([a-z0-9-]+)` ``) and `not exercised` is not one of the three
   labels it accepts. So the annotation is honest to a reader and unreadable to the counter; the entry currently
   implies a well-formed row whose only problem is a missing case.
3. **The derivation rule as stated is incomplete.** The entry (entry:75-77) states `enforced` iff every case carrying
   the tag fails — a vacuous reading over zero cases yields `enforced`. `V7` does not do that: it refuses to derive
   for an empty violating set (`:400-401`, `no receipt case violates it`). The wording must say the quantifier is
   guarded, or a reader can legitimately derive `enforced` for `both-print`/`toolchain` from the entry's own rule.
4. **The entry carries no admission status at all.** Under the round-46 verdict it is not admitted (`checks=13
   defects=2`, `PREDICATE C3 fail`; SCORECARD wave-2 `not admitted (V7, V8)`; the spot-check's routed defect says
   "Keep the new knowledge unadmitted until the counter passes"), yet nothing in the entry says so, and the entry is
   indexed in `corpus/README.md:79` and `PROVINCE.md:648` without a withheld marker. A reader who stops at the entry
   has no way to learn it is coverage work rather than an admitted finding.
5. **The `recheck:` line can be mistaken for a status lever.** `recheck: 180d — … then re-run
   `python3 plans/polyglot_c_py_probe.py --lane .`` invites the reading that a passing probe re-run restores the
   entry. It cannot: admission is the frozen counter's verdict (`plans/round-48-claims.md` §C2), not the probe's. The
   status paragraph must say so; I deliberately do **not** reword `recheck:` (it is machine-read by the package gate).
6. **Non-finding, recorded to prevent a wrong repair.** The wave-2 review (`R46W2C3Entry.md`) called the two rows
   "honest negative space". That is half right: they are honest, and they are also unparseable. Repairing the
   *label* alone (writing `enforced`/`partly`) would be a re-label of a predicate and is forbidden; the rows stay as
   committed this round.

## Draft edits (for the L1 to apply; nothing here is applied)

Anchors are line numbers at `a543d920`. All old bytes are quoted verbatim from the committed entry. Insertion of new
text removes no committed byte; the two replaced blocks have their old bytes quoted in the new erratum (lane rule R1,
round-46 lesson mistake 1).

### E1 — new section `## Admission status`, inserted between the title (line 11) and `## Summary` (line 13)

```markdown
## Admission status

**Withheld — no pass asserted.** The round-46 counter `plans/round46_c3_verify.py` failed this package at
`e9d20145`: `V7 DEFECT rows=5 tags=7` and `V8 DEFECT order_exit=1 result=not-PASS`; `checks=13 defects=2`,
`PREDICATE C3 fail` (`.ufo/waves/round-46/integrate/c3-landing.txt:21-22,35-36`). This entry is therefore coverage
work — a twelfth TB2 grader read and executed — not an admitted finding, and the round-46 wave-2 verdict records
the same (`SCORECARD.md`, C3 `not admitted (V7, V8)`). The status lifts only on the round-48 re-frozen counter
named in `plans/round-48-claims.md` §C2 (`plans/round48_c2_verify.py`): a clean clone of the landing tip on which
it prints `checks=<V> defects=0`, then `PREDICATE R48-C2 pass`, exit 0, `<V>` pinned at stage 2. That counter was
neither pinned nor run when this paragraph was written, so nothing here predicts its outcome. Satisfying this
entry's own `recheck:` — a capture re-fetch, a digest re-check, a probe re-run — changes no admission status.
```

Landing note for the L1: keep the literal `<V>` (it mirrors the frozen predicate) or substitute the stage-2 pinned
integer; do not turn the sentence into a measurement claim.

### E2 — Summary, replace lines 36-40

Old (verbatim):

```
changes the graded directory in the middle of its own test. Every measured end state is recorded in the
receipt named by `plans/pkg-spec-r46.json` (`corpus/evidence/round46/polyglot-c-py-probe.txt`: `cases=18
observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7`), first recorded after the stage-2
freeze `4fdeebaa` (QUALITY Q30); the sections below were drafted from the sources before that run and their
verdict cells filled from the receipt.
```

New:

```
changes the graded directory in the middle of its own test. Every measured end state is recorded in the
receipt named by `plans/pkg-spec-r46.json` (`corpus/evidence/round46/polyglot-c-py-probe.txt`: `cases=18
observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7`), committed at `8d7f74c` (02:33:05)
after the stage-2 amendment `4fdeebaa`; the sections below were drafted from the sources before that run and their
verdict cells filled from the receipt. Commit order alone does not satisfy QUALITY Q30: a stage-2 control
executed the gate's fresh-probe leg 56 s before the first recorded probe output was committed —
`.ufo/waves/round-46/claims/control-c3-echo.txt:4` `ENVELOPE start 02:32:09`, `:15 gate: P10 DEFECT fresh probe
output is not byte-equal to the receipt` — and the counter records it as `ORDER HIT
…/control-c3-echo.txt@4fdeebaa546c:15 kind=gate-p10`, `ORDER FAIL probe-executed-before-receipt hits=1`,
`V8 DEFECT`. The receipt is the first *retained* probe output, not the first probe execution.
```

### E3 — Requirement map, replace lines 75-79

Old (verbatim):

```
Labels are **derived** from the receipt by the counter's `V7` rule: `enforced` iff every case whose `violates=` set
carries the tag is observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise. The
probe froze seven tags on five instruction lines; two of them (`both-print`, `toolchain`) are violated by no frozen
case, so no label can be derived for them — they are listed below as `not exercised`, and the counter's `V7` reports
them as a defect (round-46 lesson §Mistakes: the stage-2 pin never checked that every frozen tag has a violating case).
```

New:

```
Labels are **derived** from the receipt by the counter's `V7` rule: `enforced` iff every case whose `violates=` set
carries the tag is observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — but
only over a non-empty violating set. `V7` matches a row only in the form
``| `instruction.md:N` | `tag` | enforced|unenforced|partly | … |`` and refuses to derive a label for a tag whose
violating set is empty (`plans/round46_c3_verify.py:135`, `:400-401`), so the vacuous reading of the quantifier
("every case fails" over no case) is not the label it gives either tag. The probe froze seven tags on five
instruction lines; two of them (`both-print`, `toolchain`) are violated by no frozen case and neither carries a
label: they are listed below as `not exercised`, which is an annotation rather than one of `V7`'s three labels, and
those two rows also leave the tag cell unbackticked. `V7` therefore records three defects on them, not one — two
`unparsed row` entries plus `tags missing=['both-print', 'toolchain']` — and prints `rows=5 tags=7` although seven
rows are present (`.ufo/waves/round-46/integrate/c3-landing.txt:21`; the row strings quoted there are the counter's
own 50-character truncation, `line[:50]`, not empty cells). The row cells stay exactly as committed: no frozen tag
is re-worded and no case is added here. A later amendment derives the two missing labels from an amended case table
(the round-48 C2 claim amends cases, never tags); until then neither tag has a derived label.
```

### E4 — Limits, replace lines 307-308

Old (verbatim):

```
- Two frozen requirement tags (`both-print`, `toolchain`) are exercised by no case (see Requirement map), so the
  map's coverage of `instruction.md:7,9` is partial and the counter's `V7` reports it.
```

New:

```
- Two frozen requirement tags (`both-print`, `toolchain`) are exercised by no case (see Requirement map), so the
  map's coverage of `instruction.md:7,9` is partial — partial in a second sense: `V7` prints `rows=5 tags=7` with
  three defects on those rows (two `unparsed row` against `plans/round46_c3_verify.py:135`, whose label set is
  `enforced|unenforced|partly` and whose tag cell must be backticked, plus
  `tags missing=['both-print', 'toolchain']`). The table is readable to a reader and partly unreadable to the
  counter; neither tag carries a label.
```

### E5 — Errata, append after item 2 (line 321)

```markdown
## Errata (round 48, wave 1)

3. **The Summary's Q30 sentence and the Requirement-map prose understated what the counter reported.**
   Old bytes: “first recorded after the stage-2 freeze `4fdeebaa` (QUALITY Q30)” and “they are listed below as
   `not exercised`, and the counter's `V7` reports them as a defect”. Corrected in place above. The receipt is the
   first *retained* probe output, not the first execution: `control-c3-echo` started at 02:32:09 and executed the
   gate's P10 before the `8d7f74c` receipt commit (02:33:05) → V8. `V7`'s bad list has three entries — two
   unparsed rows plus the two missing tags — at `rows=5 tags=7`. No frozen tag, case or label changed.
4. **The entry now states its admission status.** New text at `## Admission status`; it removes no bytes and
   asserts no pass — the package stays withheld until the round-48 re-frozen counter's frozen predicate prints what
   `plans/round-48-claims.md` §C2 requires. Found and drafted by round-48 seat `R48C2ScribeEntry`
   (`.ufo/waves/round-48/w1/R48C2ScribeEntry.md`).
```

## Negative-scope preservation (what the edits deliberately do not do)

| Not done | Why |
|---|---|
| No tag re-worded, no case added, no label written into the two rows | The claim amends the case table at stage 2, never the tags; assigning a label now would re-label a predicate before data. |
| No assertion that the round-48 counter passes, no literal `<V>` filled | Stage-2 pin absent; no scored run exists. |
| No change to `## Negative space`, `## Predictor`, `## Case table`, `## Mechanism`, `## Findings`, `## Located quotes`, or errata 1-2 | Outside this item; the class claims and their limits stand as committed. |
| No change to `recheck:` | Machine-read; the status paragraph carries the "rechecking does not lift" fact instead. |
| No re-measurement of the probe, captures or digests | No scored execution allowed before the freeze; the entry's receipt bytes are quoted, not re-derived. |
| No claim added about the image toolchain, Harbor behaviour, or task validity | The entry's existing limits (host gcc/python3, no image run) are untouched. |
| No edit to `SCORECARD.md`, `LOG.md`, `README.md`, `PROVINCE.md`, `corpus/QUALITY.md` | Out of the seat's write scope; the L1 integrates. |

## Commands run (exact; all read-only)

```
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2ScribeEntry && cd /fast/scratch/hyaku/kengaku-r48/R48C2ScribeEntry
git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane rev-parse --show-toplevel          → /fast/scratch/hyaku/kengaku-r48/R48C2ScribeEntry/lane
git -C lane log --oneline -3                   → bf783c1 / 453ddfd / a543d92
git -C lane cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af   → commit
git -C lane log -1 --format='%H %ci %s' a543d92083557dd9b33ee674e9b99b03411f80af
                                               → a543d920… 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze …
git -C lane show a543d920:plans/round-48-claims.md | grep -nE '<V>|<N>|<P>|<H>|<S>|<B>|<M>'   → 9 placeholder lines incl. checks=<V>
git -C lane ls-tree -r --name-only a543d920 plans/ | grep -E 'round48|polyglot'              → plans/polyglot_c_py_probe.py
git -C lane log --oneline a543d920..HEAD -- plans/round-48-claims.md                          → (empty)
git -C lane show a543d920:corpus/knowledge/tb2-polyglot-c-py-grader.md | sha256sum             → 4c05769f…
sha256sum corpus/knowledge/tb2-polyglot-c-py-grader.md                                        → 4c05769f…
git -C lane log -1 --format='%h %ci %s' 4fdeebaa 8d7f74ce e9d20145 264b775                    → the four chronology lines above
git -C lane log --oneline -- .ufo/waves/round-46/claims/control-c3-echo.txt                   → 4fdeeba
git -C lane log -S 'not exercised' --oneline -- corpus/knowledge/tb2-polyglot-c-py-grader.md   → e9d2014
git -C lane diff e9d2014 264b775 -- corpus/knowledge/tb2-polyglot-c-py-grader.md              → one appended-errata hunk only
grep -n '^## ' corpus/knowledge/tb2-polyglot-c-py-grader.md
                                               → Summary:13 Located quotes:42 Requirement map:73 Case table:108
                                                 Mechanism:135 Findings:160 Negative space:188 Predictor:215
                                                 Limits:300 Errata (round 46, wave 2):312
sed -n '21p;22p;35p;36p' .ufo/waves/round-46/integrate/c3-landing.txt        → V7/V8/checks/PREDICATE lines quoted above
sed -n '39,44p' .ufo/waves/round-46/integrate/c3-landing.txt                 → ORDER lines quoted above
sed -n '4p;15p' .ufo/waves/round-46/claims/control-c3-echo.txt              → ENVELOPE start 02:32:09 / gate: P10 DEFECT
sed -n '374,420p' plans/round46_c3_verify.py                                 → v7() body; :390, :400-401, :413
grep -n "line\[:50\]\|no receipt case violates it\|if not violating\|rows={sum(seen" plans/round46_c3_verify.py
                                               → 390 / 400 / 401 / 413
```

No `plans/round46_c3_verify.py`, no `plans/polyglot_c_py_probe.py`, no wave-1 candidate was executed. No git/jj
mutation was run anywhere; the only clone is `--shared` inside the seat scratch and its top level was asserted
before any read-write operation (none occurred).

## Touched surfaces

- **Lane:** exactly one path written — `.ufo/waves/round-48/w1/R48C2ScribeEntry.md` (this report). No production file
  was edited: `corpus/knowledge/tb2-polyglot-c-py-grader.md` is unchanged at `sha256 4c05769f…` after this seat, and
  the draft edits above exist only inside this report. No commit, push, jj command, pacman transaction or tool install
  was run, and no sibling repo, `.ufo/state`, `MANIFEST.json` or fleet-root file was touched.
- **Scratch:** `/fast/scratch/hyaku/kengaku-r48/R48C2ScribeEntry` held one `git clone --shared` of the lane (568 MB,
  top level `/fast/scratch/hyaku/kengaku-r48/R48C2ScribeEntry/lane`, asserted with `git rev-parse --show-toplevel`
  before any read-write call — none occurred). Evidence was cited from the lane worktree, not from scratch, so
  nothing needed copying out; the scratch tree was removed before this report was finalised and `ls -d` now prints
  `No such file or directory`. No scratch residue remains.

## Limits

- This report drafts text; it does not apply it. Whether the L1 lands E1-E5, and in what commit, is the L1's
  decision; the round-48 C2 counter is not the instrument this seat may invoke.
- The V8 repair rests on committed bytes (control receipt, receipt commit, order-check output). I did not re-run
  `plans/order_check.py`; its printed result is quoted, and the 56 s gap is derived from the two commit clocks plus
  the control's own `ENVELOPE start 02:32:09` line, not from wall-clock observation by this seat.
- The commits' `%ci` timestamps are author-committer clocks, not proof of execution order by themselves; the
  evidence for the pre-receipt probe execution is the control receipt's own `P10` line plus the committed
  `ORDER HIT`/`ORDER FAIL` verdict, which is what V8 reads.
- The entry's external anchors (S166-S172 at `2fd12b88`) were not re-fetched here, so this report carries no
  access date or located quote for them and makes no claim about their current bytes. The only quotes in this
  report are lane-local, with path and line.
- `not exercised` in the two rows remains unparseable by `V7` by design of this draft; a later stage-2 case-table
  amendment is what makes a derived label possible, and that amendment is not in this seat's scope.
- The status paragraph names `plans/round48_c2_verify.py`; if the L1 lands the counter under another path, the
  paragraph must be adjusted at landing (path only — not the condition).

VERDICT: **draft-only, no pass asserted** — the r46 C3 entry is repaired in wording for both admissions (V7: three
defects, two unparsed rows plus the two missing tags, `rows=5 tags=7`; V8: the gate's P10 executed at 02:32:09, 56 s
before the `8d7f74c` receipt commit) and for its unadmitted status, whose lifting is stated as the round-48 frozen
predicate's outcome and is not claimed. The two frozen tags keep their cells and receive no label; no case, capture,
probe, counter, claim or score was created, re-frozen or re-labelled by this seat.
