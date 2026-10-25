# R31 / C2 — routed defects R4 and R5: duplicated sentence and duplicated clause

Seat: `L1Kengaku31.R31DefR4R5` (leaf, read-only on the lane).
Target: `corpus/knowledge/contamination-transparency-card.md`.
Claim under review: C2 R4 ("entry duplicated 'reconciled truth' sentence removed") and R5
("entry falsifier duplicated clause removed"), `plans/round-31-claims.md`.

## 0. Drift notice — the file was repaired while this review ran

I read the entry at its committed state and captured the defect bytes; by my second read the
worktree had changed underneath me:

| state | bytes | md5 | R4 copies | R5 clause copies |
|---|---|---|---|---|
| `HEAD` (pre-repair) | 19586 | `22664dc7132b1632fec94212b0028241` | 2 | 2 |
| worktree, snapshot 1 | 19685 | `49d16e895939c65285ae1e1f9d636dc2` | 1 | 1 |
| worktree, snapshot 2 (2026-10-25T08:57:18Z) | 19753 | `fde78c3c6cd958e00f0f1b8d9c127f9d` | 1 | 1 |

`git status --porcelain` on the file: ` M`; `git diff --stat HEAD` at snapshot 1 = `12 insertions(+),
10 deletions(-)`. The worktree hunks also carry the R6/R7/R8 repairs from another seat, and R5's
repair shares a hunk with R8's (`@@ -135,8 +137,8 @@`), so the R5 fix is **not** isolable by hunk
alone — I reviewed it at line level (below).

The worktree was **still moving** while I wrote this report (two distinct post-repair snapshots, 68
bytes apart, both with the R4 and R5 repairs intact). Every worktree line/byte offset below is
labelled with the snapshot it belongs to; the `HEAD`-relative offsets are the stable evidence,
because `HEAD` cannot drift. Worktree offsets will shift again as the repair seat finishes.

Consequence for reproduction: **pre-repair byte ranges are `HEAD`-relative** and must be read
through `git show HEAD:<path>`. Current ranges are given separately. Both are quoted below with
the command that produces them.

## 1. R4 — duplicated sentence "…not a reconciled truth."

### Exact byte ranges (pre-repair, `HEAD`)

```
$ git show HEAD:corpus/knowledge/contamination-transparency-card.md | grep -b -o 'Two coders filling this card need not agree'
14162:Two coders filling this card need not agree
14268:Two coders filling this card need not agree
```

| | bytes (0-based, inclusive) | line |
|---|---|---|
| occurrence 1 | `14162-14266` | 124 |
| occurrence 2 (**residue**) | `14268-14372` | 125 |

```
$ git show HEAD:corpus/knowledge/contamination-transparency-card.md | sed -n '124,126p'
  than better agreement" (arXiv abs page, abstract). Two coders filling this card need not agree; the
  card records what each stated, not a reconciled truth. Two coders filling this card need not agree; the card records
  what each stated, not a reconciled truth.
```

Byte-boundary proof (the deletion must take the separating space, not the newline):

```
$ git show HEAD:<path> | dd bs=1 skip=14260 count=16 2>/dev/null | cat -A
 truth. Two code
$ git show HEAD:<path> | dd bs=1 skip=14368 count=11 2>/dev/null | cat -A
ruth.$
- **S
```

So byte 14266 = `.`, 14267 = the single space, 14268-14372 = the duplicate sentence, 14373 = `\n`.

**Proposed repair (as applied): delete bytes `14267-14372` inclusive** — the space plus the second
copy — leaving `…not a reconciled truth.\n`. Equivalent line edit: collapse `HEAD:125-126` to the
single line `  card records what each stated, not a reconciled truth.`

### Intended single sentence

> Two coders filling this card need not agree; the card records what each stated, not a reconciled truth.

Exactly one occurrence, as it stood at `623c1fc:116-117`:

```
$ git show 623c1fc:corpus/knowledge/contamination-transparency-card.md | grep -n -A1 'reconciled'
116-  rather than better agreement). Two coders filling this card need not agree; the card records
117:  what each stated, not a reconciled truth.
```

### Which copy is residue of an earlier fix

`706ed3f` ("round-30 repairs after the falsify wave: … clause fixes"). Its diff against `623c1fc`
removed the two old quote lines and added three new ones, the last of which re-emits the sentence
**and** its own opening:

```
$ git diff 623c1fc 706ed3f -- <path> | grep -E '^[-+].*(coders|reconciled)'
-  rather than better agreement). Two coders filling this card need not agree; the card records
+  than better agreement" (arXiv abs page, abstract). Two coders filling this card need not agree; the
+  card records what each stated, not a reconciled truth. Two coders filling this card need not agree; the card records
```

The rewrite re-flowed the paragraph, wrote the sentence in full, then began it again while the
original tail survived. `git blame` confirms the seam: lines 124-125 are `706ed3f`, line 126 is
still `623c1fc` — i.e. the residue's tail is the *pre-fix* line the fix failed to delete. The
residue is therefore **occurrence 2** (`14268-14372`), not occurrence 1.

### Does removing it change a claim?

No. The two copies are token-identical (18 tokens); they differ only in where the line wraps
(occ. 1 breaks after `the`, occ. 2 breaks after `records`). Deleting either removes no assertion,
no hedge and no qualifier; the bullet still states exactly one thing about coder agreement.

## 2. R5 — duplicated clause `populated (not "unknown")`

### Exact byte ranges (pre-repair, `HEAD`)

The two copies are **not byte-identical**: line 137 emphasises the word, line 138 does not. That is
why a verbatim `grep` finds the clause only once and the defect needs an emphasis-insensitive pass.

```
$ git show HEAD:<path> | grep -b -o 'populated\* (not "unknown")'
15403:populated* (not "unknown")
$ git show HEAD:<path> | grep -b -o 'populated (not "unknown")'
15436:populated (not "unknown")
```

| | bytes (0-based, inclusive) | line |
|---|---|---|
| occurrence 1 (kept) | `15402-15428` (`*populated* (not "unknown")`) | 137 |
| occurrence 2 (**residue**) | `15432-15461` (`and populated (not "unknown") `) | 138 |

```
$ git show HEAD:<path> | sed -n '137,138p'
  its own contamination audit shows the strata and acquired fields are *populated* (not "unknown")
  and populated (not "unknown") would show that the fields this entry's sources measured as rare
```

```
$ git show HEAD:<path> | dd bs=1 skip=15426 count=40 2>/dev/null | cat -A
n")$
  and populated (not "unknown") woul
```

So 15428 = `)`, 15429 = `\n`, 15430-15431 = the two-space indent, 15432-15461 = the 30-byte residue
(`and populated (not "unknown") ` including its trailing space), 15462 = `w` of `would`.

**Proposed repair (as applied): delete bytes `15432-15461` inclusive**, leaving line 138 as
`  would show that the fields this entry's sources measured as rare`.

### Intended single sentence

One bullet, one antecedent predicate:

> **Falsifier:** a benchmark release that publishes a card answering all eight CG questions while its
> own contamination audit shows the strata and acquired fields are \*populated\* (not "unknown") would
> show that the fields this entry's sources measured as rare (R1 strata, S1's acquired type) are
> common — a decision rule the card design cannot supply on its own, which is why this bullet names
> the unit (one benchmark release), the population (its published card) and the observation (both
> fields populated and non-trivial) rather than a trend bullet above.

### Which copy is residue of an earlier fix

`9af639c` ("S086 is not peer-reviewed …; falsifier decision rule"). Before it, `a6a9b57:135-136` read:

```
135-  its own contamination audit shows the strata and acquired fields are *populated* (not "unknown")
136-  and non-trivial would show that the fields this entry's sources measured as rare (R1 strata, S1's
```

The pre-fix continuation was `and non-trivial`. `9af639c` rewrote that continuation to introduce the
decision rule and replaced `and non-trivial` with `and populated (not "unknown")` — re-emitting the
predicate the line above had just stated instead of advancing it. The residue is **occurrence 2**,
and it is precisely the slot where the earlier wording had a different word.

### Does removing it change a claim?

No — the falsifier keeps both of its conditions:

* `populated (not "unknown")` survives once, line 137 (current 139);
* `non-trivial` survives in the observation clause, `and the observation (both fields populated and
  non-trivial)` (current line 143);
* the decision rule (unit / population / observation) is untouched.

The deletion removes a verbatim repeat of the antecedent predicate and nothing else. One nuance
worth recording rather than hiding: `non-trivial` was *already* only in the observation clause at
`HEAD` (the pre-`9af639c` antecedent had it, the `HEAD` antecedent did not), so the repair does not
move it — it leaves the qualifier exactly where the previous fix had already put it.

## 3. Whole-file sweep — do other repetitions exist?

**Yes, other repeated spans exist; no other duplicated sentence or clause does.** The negative claim
carries the sweep below. It is failure-capable: run against the pre-repair bytes it finds both R4 and
R5, and against the current bytes it finds neither.

### The sweep command

`python3 dup.py <file>` — four passes: **A** whitespace-normalised sentence duplicates (>=5 words);
**B** maximal repeated token spans, verbatim bytes (>=8 tokens); **C** the same after stripping
markdown emphasis markers `* _ \`` (this is the pass that can see R5, whose copies differ by an
asterisk); **D** local duplication, a >=3-token span repeated within 12 tokens of itself (the
copy-paste signature below B's 8-token floor). All offsets are 0-based inclusive **byte** offsets.

```python
import re, sys, collections
s = open(sys.argv[1], 'rb').read().decode()
bp, a = [0]*(len(s)+1), 0
for i, c in enumerate(s): bp[i] = a; a += len(c.encode())
bp[len(s)] = a
L = lambda c: s.count('\n', 0, c) + 1
def tok(x): return [m.group() for m in re.finditer(r'\S+', x)], [m.start() for m in re.finditer(r'\S+', x)], [m.end() for m in re.finditer(r'\S+', x)]
def emit(label, spans, toks, cs, ce, mp):
    print(f'== {label} ==')
    for la, ra, lb, rb in spans:
        print(f'  DUP x2 [{ra-la+1} tok]: {" ".join(toks[la:ra+1])[:120]}')
        for lo, hi in ((la, ra), (lb, rb)):
            o0, o1 = mp(cs[lo]), mp(ce[hi]-1)+1
            print(f'    bytes {bp[o0]}-{bp[o1]-1}  line {L(o0)}')
def maximal(t, n=8):
    ix = collections.defaultdict(list)
    for i in range(len(t)-n+1): ix[tuple(t[i:i+n])].append(i)
    out = []
    for p in ix.values():
        if len(p) < 2: continue
        for x in range(len(p)):
            for y in range(x+1, len(p)):
                la, lb = p[x], p[y]; ra, rb = la+n-1, lb+n-1
                while la and lb-la >= n and t[la-1] == t[lb-1]: la -= 1; lb -= 1
                while ra+1 < len(t) and rb+1 < len(t) and rb-ra >= n and t[ra+1] == t[rb+1]: ra += 1; rb += 1
                out.append((la, ra, lb, rb))
    out = sorted(set(out), key=lambda z: -(z[1]-z[0])); keep = []
    for z in out:
        if not any(k[0] <= z[0] and k[1] >= z[1] and k[2] <= z[2] and k[3] >= z[3] and k[1]-k[0] > z[1]-z[0] for k in keep): keep.append(z)
    return keep
nm, im, pw = [], [], False
for i, c in enumerate(s):
    if c.isspace():
        if not pw: nm.append(' '); im.append(i)
        pw = True
    else: nm.append(c); im.append(i); pw = False
x = ''.join(nm); cuts = [0]+[m.end() for m in re.finditer(r'(?<=[.!?])\s+', x)]+[len(x)]
d = collections.defaultdict(list)
for a0, b0 in zip(cuts, cuts[1:]):
    g = x[a0:b0]; ld = len(g)-len(g.lstrip()); g = g.strip()
    if len(g.split()) >= 5: d[re.sub(r'\s+', ' ', g).lower()].append((a0+ld, a0+ld+len(g), g))
print('== A: duplicated sentences (>=5 words) ==')
nA = 0
for o in d.values():
    if len(o) > 1:
        nA += 1; print(f'  DUP x{len(o)}: {o[0][2][:120]}')
        for ca, cb, _ in o:
            o0, o1 = im[ca], im[cb-1]+1
            print(f'    bytes {bp[o0]}-{bp[o1]-1}  line {L(o0)}')
print(f'  A duplicates: {nA}')
t, cs, ce = tok(s); emit('B: verbatim', maximal(t), t, cs, ce, lambda i: i)
f, fm = [], []
for i, c in enumerate(s):
    if c not in '*_`': f.append(c); fm.append(i)
ft, fcs, fce = tok(''.join(f)); emit('C: emphasis-insensitive', maximal(ft), ft, fcs, fce, lambda i: fm[i])
print('== D: local duplication (3 tok, gap<=12) ==')
h = 0
for i in range(len(ft)-2):
    for j in range(i+3, min(i+13, len(ft)-2)):
        if ft[i:i+3] == ft[j:j+3]:
            h += 1
            o0, o1 = fm[fcs[i]], fm[fce[i+2]-1]+1
            p0, p1 = fm[fcs[j]], fm[fce[j+2]-1]+1
            print(f'  DUP x2 gap {j-i}: {" ".join(ft[i:i+3])}')
            print(f'    bytes {bp[o0]}-{bp[o1]-1}  line {L(o0)}')
            print(f'    bytes {bp[p0]}-{bp[p1]-1}  line {L(p0)}')
print(f'  D hits: {h}')
```

### Output on the pre-repair bytes (`git show HEAD:<path> > head.md`)

```
== A: duplicated sentences (>=5 words) ==
  DUP x2: Two coders filling this card need not agree; the card records what each stated, not a reconciled truth.
    bytes 14162-14266  line 124
    bytes 14268-14372  line 125
  A duplicates: 1
== B: verbatim ==
  DUP x2 [19 tok]: a property of one run, it must be recorded with the reported score rather than with the benchmark release"
    bytes 130-235  line 1
    bytes 4166-4271  line 19
  DUP x2 [18 tok]: "Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type
    bytes 321-456  line 1
    bytes 13307-13444  line 116
  DUP x2 [18 tok]: Two coders filling this card need not agree; the card records what each stated, not a reconciled truth.
    bytes 14162-14266  line 124
    bytes 14268-14372  line 125
  DUP x2 [16 tok]: "transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to l
    bytes 778-905  line 2
    bytes 4569-4696  line 23
  DUP x2 [10 tok]: "Item-level transparency and procedural transparency have opposite effects on benchmark
    bytes 667-753  line 2
    bytes 4467-4553  line 22
  DUP x2 [10 tok]: | **already a column** in two of three | |
    bytes 7716-7757  line 64
    bytes 7844-7885  line 65
== C: emphasis-insensitive ==
  DUP x2 [19 tok]: a property of one run, it must be recorded with the reported score rather than with the benchmark release"
    bytes 130-235  line 1
    bytes 4166-4271  line 19
  DUP x2 [18 tok]: "Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type 
    bytes 321-456  line 1
    bytes 13307-13444  line 116
  DUP x2 [18 tok]: Two coders filling this card need not agree; the card records what each stated, not a reconciled truth.
    bytes 14162-14266  line 124
    bytes 14268-14372  line 125
  DUP x2 [16 tok]: "transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to l
    bytes 778-905  line 2
    bytes 4569-4696  line 23
  DUP x2 [10 tok]: "Item-level transparency and procedural transparency have opposite effects on benchmark
    bytes 667-753  line 2
    bytes 4467-4553  line 22
  DUP x2 [10 tok]: | already a column in two of three | |
    bytes 7716-7757  line 64
    bytes 7844-7885  line 65
  DUP x2 [8 tok]: | already a column in one of three
    bytes 8088-8125  line 66
    bytes 8547-8582  line 69
== D: local duplication (3 tok, gap<=12) ==
  DUP x2 gap 11: not in this
    bytes 5663-5673  line 40
    bytes 5735-5745  line 41
  DUP x2 gap 11: in this lane's
    bytes 5667-5680  line 40
    bytes 5739-5752  line 41
  DUP x2 gap 8: | (absent) |
    bytes 8157-8168  line 67
    bytes 8227-8238  line 67
  DUP x2 gap 9: | (absent) |
    bytes 8368-8379  line 68
    bytes 8427-8438  line 68
  DUP x2 gap 4: | (absent) |
    bytes 8505-8516  line 69
    bytes 8536-8547  line 69
  DUP x2 gap 4: populated (not "unknown")
    bytes 15403-15428  line 137
    bytes 15436-15460  line 138
  DUP x2 gap 5: Contamination transparency card
    bytes 17348-17378  line 162
    bytes 17395-17425  line 163
  DUP x2 gap 5: transparency card format.
    bytes 17362-17387  line 162
    bytes 17409-17434  line 163
  DUP x2 gap 8: | Compare the
    bytes 18075-18087  line 172
    bytes 18115-18127  line 172
  D hits: 9
```

The sweep is failure-capable: pass A and B both isolate R4 at `14162-14266` / `14268-14372`, and
pass D isolates R5 at `15403-15428` / `15436-15460`. Pass A alone would have missed R4's sentence if
it were preceded by a parenthetical — `(abstract). Two` does not satisfy a terminator lookbehind —
which is why B and D exist and why I report the passes separately rather than one aggregate.

### Output on the current worktree bytes (snapshot 2, md5 `fde78c3c…`, 19753 bytes)

```
== A: duplicated sentences (>=5 words) ==
  A duplicates: 0
== B: verbatim ==
  DUP x2 [19 tok]: a property of one run, it must be recorded with the reported score rather than with the benchmark release"
    bytes 130-235  line 1
    bytes 4166-4271  line 19
  DUP x2 [18 tok]: "Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type 
    bytes 321-456  line 1
    bytes 13607-13744  line 120
  DUP x2 [16 tok]: "transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to l
    bytes 778-905  line 2
    bytes 4569-4696  line 23
  DUP x2 [10 tok]: | **already a column** in two of three | |
    bytes 7730-7771  line 65
    bytes 7858-7899  line 66
  DUP x2 [10 tok]: "Item-level transparency and procedural transparency have opposite effects on benchmark
    bytes 667-753  line 2
    bytes 4467-4553  line 22
== C: emphasis-insensitive ==
  DUP x2 [19 tok]: a property of one run, it must be recorded with the reported score rather than with the benchmark release"
    bytes 130-235  line 1
    bytes 4166-4271  line 19
  DUP x2 [18 tok]: "Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type 
    bytes 321-456  line 1
    bytes 13607-13744  line 120
  DUP x2 [16 tok]: "transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to l
    bytes 778-905  line 2
    bytes 4569-4696  line 23
  DUP x2 [10 tok]: | already a column in two of three | |
    bytes 7730-7771  line 65
    bytes 7858-7899  line 66
  DUP x2 [10 tok]: "Item-level transparency and procedural transparency have opposite effects on benchmark
    bytes 667-753  line 2
    bytes 4467-4553  line 22
  DUP x2 [8 tok]: | already a column in one of three
    bytes 8102-8139  line 67
    bytes 8561-8596  line 70
== D: local duplication (3 tok, gap<=12) ==
  DUP x2 gap 8: | (absent) |
    bytes 8171-8182  line 68
    bytes 8241-8252  line 68
  DUP x2 gap 9: | (absent) |
    bytes 8382-8393  line 69
    bytes 8441-8452  line 69
  DUP x2 gap 4: | (absent) |
    bytes 8519-8530  line 70
    bytes 8550-8561  line 70
  DUP x2 gap 5: Contamination transparency card
    bytes 17515-17545  line 165
    bytes 17562-17592  line 166
  DUP x2 gap 5: transparency card format.
    bytes 17529-17554  line 165
    bytes 17576-17601  line 166
  DUP x2 gap 8: | Compare the
    bytes 18242-18254  line 175
    bytes 18282-18294  line 175
  D hits: 6
```

`A duplicates: 0`, and the R5 clause no longer appears in D. Both defects are gone from the
worktree.

### Triage of every remaining repetition (all benign, none claim-bearing duplication)

1. **Front-matter `source:` quotes echoed in the body** — 4 spans: S081's run rule
   (`130-235` ↔ `4166-4271`), S081's abstract sentence (`321-456` ↔ `13607-13744`, line 120),
   S082's item-level claim (`667-753` ↔ `4467-4553`), S082's transparency-should claim (`778-905` ↔
   `4569-4696`). **By design.** QUALITY Q1 requires the first three lines to be `source:` and Q3
   requires each load-bearing sentence to map to an anchored quote (≤25 words); the `source:` line
   carries the located quote and the body quotes it. `corpus/knowledge/contamination-detection-and-transparency.md`
   uses the same shape. Not a defect.
2. **Table verdict cells** — `**already a column** in two of three` (lines 65, 66) and
   `already a column in one of three` (lines 67, 70). These are *cell values on different rows*
   (R2 elicitation budget / R5 instrument currency; R4 regeneration status / R1 strata), not
   duplicated sentences. Legitimate: two different fields can each be present in the same number of
   published designs. The only thing worth an eye is that the two "one of three" verdicts are
   word-identical — but each row's own columns justify it, and neither is in R4/R5's scope.
3. **Three-token structural coincidences** — `| (absent) |` cells, `| Compare the`, and the
   coverage-map row name `Contamination transparency card` echoed by the following `New:` line
   (snapshot 2, lines 165-166). Structural, not duplication.

**Naming hazard, reported so nobody mis-closes:** the entry's mapping table uses **R1–R5 / S1–S2 as
card-field ids** (`R4 regeneration status`, `R5 instrument currency`), which collide with round 31's
defect ids R1–R10. "R4" in the table is a field, not defect R4; likewise "R5".

## 4. Verification of the applied repairs

`sed -n '123,129p' | cat -A` on snapshot 2 ends the agreement bullet at
`  card records what each stated, not a reconciled truth.$` — one copy, no trailing space, no
double space at the join. `sed -n '137,146p'` shows the falsifier reading `…are *populated* (not
"unknown")` / `would show that the fields…` and still naming `and the observation (both fields
populated and non-trivial)`. Snapshot-2 offsets: `Two coders…` at `128:14462` (single),
`populated* (not "unknown")` at `140:15597` (single), `both fields populated and non-trivial` at
`144:15924`; `grep -c 'and populated'` on the file returns no residue.

The lane's own counter agrees on these two items:

```
$ python3 plans/round31_defects.py --lane .
DEFECT R9 round30-seat-reports-committed: .ufo/waves/round-30/build/R30DraftGate.md still differs from HEAD: M .ufo/waves/round-30/build/R30DraftGate.md
checks=10 defects=1
exit=1
```

R4 and R5 no longer fire; **R9 is the only open item** (an uncommitted round-30 seat report —
another seat's surface, outside this ticket).

### The counter's own R4/R5 checks are failure-capable

Proved without mutating the lane: the `HEAD` bytes were copied into a throwaway lane root under
`/tmp/r31-R31DefR4R5/fakelane/`, `plans/round31_defects.py` was imported as a module, and
`check_r4` / `check_r5` were called directly against both roots.

```
R4 pre-repair : FIRES -> the entry carries the 'reconciled truth' sentence 2 times, not exactly once
R4 post-repair: passes
R5 pre-repair : FIRES -> the falsifier bullet repeats 'populated (not "unknown")' 2 times, not exactly once
R5 post-repair: passes
```

Both checks normalise through `plain()` — whitespace-collapsed (`flat`) **and** emphasis-stripped
(`re.sub(r"\*\*|__|\*", "", …)`, whose docstring reads "a duplicated clause hides behind `*` marks").
That is exactly what lets R5's check see the `*populated*` copy. A naive verbatim check would not:
`grep -c 'populated (not'` returns **0** on both the pre-repair and the post-repair tree, because the
retained copy carries an asterisk. Any future R5-style check must be emphasis-insensitive or it
passes vacuously.

## 5. Residual risk and verification gaps

- **Byte ranges are `HEAD`-relative** for the pre-repair state, because the worktree was already
  repaired when I finished. A reader reproducing against the live file will see one copy, not two;
  the `git show HEAD:` form in every command above is deliberate.
- **The worktree moved twice under this review** (19586 → 19685 → 19753 bytes) and may move again.
  Snapshot-2 offsets are pinned to md5 `fde78c3c6cd958e00f0f1b8d9c127f9d`; re-running the sweep after
  any further edit will print different byte offsets for the *benign* spans while `A duplicates: 0`
  and the absence of the R5 clause should hold. The R4/R5 repairs themselves were present and intact
  in both post-repair snapshots.
- **R5's hunk is shared with R8's repair** (`@@ -135,8 +137,8 @@`), so hunk-level review cannot
  separate them; I verified R5 at line level and confirmed the only R5-relevant change on those
  lines is the removal of `and populated (not "unknown") `.
- **Pass D at 3 tokens is a detector, not an oracle** — it produced 9 hits pre-repair and 6 now,
  and I triaged every one. A different entry with denser table markup would produce more benign
  hits; the pass should not be used as an unattended gate.
- **Pass A's sentence splitter is lookbehind-based** and misses a sentence that follows a
  parenthetical (`(abstract). Two …`), which is exactly R4's context. I did not repair the splitter;
  I compensated with passes B and D, and I state the limitation rather than claiming A alone is
  sufficient.
- **Not in scope, not checked:** whether R1–R3, R6–R8 and R10's repairs are correct; whether the
  worktree should be committed; R9's disposition.
- **Tools:** none installed or upgraded. `python3` (stdlib only) and read-only `git` were used.
  Scratch stayed in `/tmp/r31-R31DefR4R5/` (80 KB); nothing outside it was touched. My only write in
  the lane is this report (`?? .ufo/waves/round-31/build/R31DefR4R5.md`); the entry's ` M` is the
  repair seat's edit, not mine.

VERDICT: R4 and R5 are real, exactly where the ticket says (R4: `HEAD` bytes 14162-14266 / 14268-14372, lines 124-125; R5: `HEAD` bytes 15402-15428 / 15432-15461, lines 137-138), both are residue of earlier round-30 fixes (`706ed3f` and `9af639c`), both are already repaired correctly in the worktree with no claim change, and a four-pass whole-file sweep finds no other duplicated sentence or clause — the remaining repetitions are front-matter quote echoes and table cell values, all by design.
