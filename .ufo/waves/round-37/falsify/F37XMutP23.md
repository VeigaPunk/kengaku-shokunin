# F37XMutP23 — extra P2/P3 mutants against `plans/battery37/p23.py` (round-37 wave 2, falsify)

Target: `plans/battery37/p23.py` (sha256 `518340e4d6403b39…`) and the P2/P3 branch of the unedited gate
`plans/pkg_gate.py` at the integration tip `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`
(gate sha256 `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` = the frozen digest,
`frozen=True` in the receipt). Lane files were never written; everything ran on
`/fast/scratch/hyaku/kengaku-r37/F37XMutP23/fx/lane` (clean clone of the tip, `git status --porcelain`
empty, `rev-parse HEAD` = `357deceb…`).

## Method

Harness `.ufo/waves/round-37/falsify/F37XMutP23/harness.py` imports the frozen counter as a module and uses
its machinery unchanged (`load_r36`, `Ctx`, `r36_fixtures`, `battery37_fixtures`, `CLAUSE_LINE`,
`GATE_SHA256`, `sha256`); `probe.py` does the same plus loads `plans/pkg_gate.py` for the gate's own parser.
It builds the full battery **once**, then runs one sweep (8 threads over fixtures, so no two gate runs share
a directory) for the reference, the seven frozen P2/P3 mutants (harness anchor), the four new mutants and
seven supplementary probes: 19 sweeps × 64 fixtures.

```
$ python3 .ufo/waves/round-37/falsify/F37XMutP23/harness.py "$S/fx/lane" "$S/work"
BATTERY fixtures=64 p23=6
BATTERY_CHECK wrong=0
NEWMUT M02 P2 killed by=p23-p2-receipt-deleted,p910-receipt-deleted -- receipt unreadable
NEWMUT M06 P3 killed by=p23-p3-seven-texts -- fewer distinct quotes than min_quotes
NEWMUT M07 P3 killed by=p23-p3-seven-locations -- fewer distinct located lines than min_distinct_locations
NEWMUT M08 P3 killed by=p23-p3-two-word-quote -- a quote outside the word range
NEWMUT X1 P3 killed by=p23-p3-seven-texts -- min_quotes lowered by one (off-by-one threshold)
NEWMUT X2 P3 SURVIVED (0 of 64 fixtures differ) -- min_distinct_locations '>=' -> '>'
NEWMUT X3 P3 killed by=p23-p3-two-word-quote -- word-range check applied to the first row only
NEWMUT X4 P3 killed by=r36-P3 -- bad-rows count off-by-one ('any bad row' -> 'more than one bad row')
NEWMUTANTS total=4 killed=3 survived=1
```
(full receipt: `falsify/F37XMutP23/receipts/harness-final.txt`; `BATTERY_CHECK wrong=0` means the reference
still matches all 64 declarations, so the battery itself is green while these mutants are measured.)
Two independent runs that rebuilt every fixture from scratch produced byte-identical `NEWMUT M02…M08/X1…X3`
lines (`diff` → `IDENTICAL`), so the attributions below are not sweep-order artifacts.

## The four new, non-frozen mutants (same clause, `old -> new` each occurring **once**)

| id | clause | `old` | `new` | result | killing fixture |
|---|---|---|---|---|---|
| X1 | P3 | `len(texts) >= rules["min_quotes"]` | `len(texts) >= rules["min_quotes"] - 1` | **killed** | `p23-p3-seven-texts` (only) |
| X2 | P3 | `len(locs) >= rules["min_distinct_locations"]` | `len(locs) > rules["min_distinct_locations"]` | **survived** 0/64 | — (live limit, see below) |
| X3 | P3 | `short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]` | `short = [q.text[:30] for q in p.quotes[:1] if not lo <= q.words <= hi]` | **killed** | `p23-p3-two-word-quote` (only) |
| X4 | P3 | `if p.bad_rows:` | `if len(p.bad_rows) > 1:` | **killed** | `r36-P3` (only) |

Each `old` was checked with `gate_src.count(old) == 1` before the mutant file was written; each mutant file
compiled (`py_compile`) and no sweep verifies or repairs the lane.

Reading of the three kills:

- **X1** dies only on `p23-p3-seven-texts`, whose P3 note the reference prints as
  `rows=8 distinct_quotes=7 distinct_lines=8 out_of_word_range=0` — i.e. exactly at `min_quotes - 1`. So the
  battery pins the *downward* off-by-one but the equality point (8) is not presented anywhere: the genuine
  table is 22 (`rows=22 distinct_quotes=22 distinct_lines=22`, receipt `P23_DECLARATION_TABLE`).
- **X3** dies only on `p23-p3-two-word-quote`: cutting the 7th data row to two words (`out_of_word_range=1`,
  `P4 ok checked=22`) is invisible to a word-range check that looks at `p.quotes[:1]`. This is the sharpest
  isolation evidence in the module — one fixture, one mutant, no second fixture reacts.
- **X4** dies only on `r36-P3` (`P3 DEFECT unparsed_rows=1 first='| a claim | "straight quotes row" | …'`).
  `p23.py` carries no unparsed-row fixture, so this branch is demonstrated by the round-36 fixture alone
  (M05 likewise: `M05 … killed by=r36-P3`). That dependency is undocumented in the p23 docstring, which
  enumerates six fixtures and never says the seventh P3 branch lives in the round-36 battery.

## X2 is a live battery limit, not an inert mutant

`probe.py` builds one fixture no frozen battery fixture supplies — the genuine table cut to its first eight
data rows (`8 texts, 8 distinct (capture, line) locations, all in range`):

```
PROBE eight ref=rc0 defects=-
    ref P3 ok rows=8 distinct_quotes=8 distinct_lines=8 out_of_word_range=0
PROBE eight X2=rc1 defects=P3 -> LIVE
    X2 P3 DEFECT rows=8 distinct_quotes=8 distinct_lines=8 out_of_word_range=0
```
The reference **accepts** a package that sits exactly on both floors; X2 rejects it. So X2 is distinguishable
by a correct battery and survives the actual 64-fixture battery. The same probe kills the supplementary
`Y3` (`min_quotes` `>=`→`>`): `PROBE eight Y3=rc1 defects=P3 -> LIVE`. The battery's location counts are 22
(genuine, and every p23 fixture except the two 8-row ones), 8-with-7-texts (`p23-p3-seven-texts`), 7
(`p23-p3-seven-locations`) — never exactly 8 with 8 texts. **Counterexample: a gate whose location floor is
9 (`>`), or whose quote floor is 9, passes all 55 frozen mutants and the whole 64-fixture battery.**

## Supplementary probes (reported, not part of the four)

| id | clause | probe | outcome |
|---|---|---|---|
| Y1 | P3 | `for line in rows[1:]:` → `rows[1:2]:` (only the first quote row parses) | killed by 38 fixtures — coarse, no boundary value |
| Y2 | P3 | `not lo <= q.words <= hi` → `not lo <= q.words <= hi + 1` | **survived, and unreachable**: genuine `words_max=19`, `test_outputs.py` `max_words_per_line=16 at line 43`, spec `quote_words=[3,25]` — a 26-word verbatim span cannot exist in this capture, so no fixture could carry it |
| Y3 | P3 | `len(texts) >= rules["min_quotes"]` → `>` | **survived**, and LIVE (`probe eight` above) → the `min_quotes` equality boundary is unpinned too |
| Y4 | P3 | `“(.+?)”` → `“(.*?)”` (empty quote text parses) | survived; **inert**: `PROBE empty-quote ref=rc1 defects=P3 … unparsed_rows=1` vs `Y4=rc1 defects=P3 … out_of_word_range=1` — same rc, same clause id, only the note differs |
| Y5 | P3 | no-section branch reordered behind the bad-rows branch (unreachable) | survived; **inert by construction**: `PROBE heading-renamed ref=rc1 defects=P3,P4` vs `Y5=rc1 defects=P3,P4 … rows=0 distinct_quotes=0 distinct_lines=0` — P3 sub-branches share one clause id, so branch identity is not observable |
| Y6 | P3 | `if p.bad_rows:` → `if len(p.bad_rows) > 2:` | killed by `r36-P3` (fall-through flips the package to accept) |
| Z1 | P2 | `return got == want,` → `return got[:8] == want[:8],` | survived; **inert**: my own design error, disproved by probe — receipt edits at offset 8 and at the last byte (3398 of 3399) both leave `Z1=rc1 defects=P2`, because SHA-256 avalanche changes the leading hex digits on any single-byte edit |

The `Z1` result is the useful negative: P2 has exactly two observable behaviours (unreadable — M02;
any digest difference — M03), every non-inverted weakening of the digest comparison is equivalent to
always-true, and the inverted comparison is killed by any accept fixture. **P2 is saturated by M02+M03; a
fifth P2 mutant cannot add calibration.** That is why all four required mutants sit on P3.

## Does each `p23.py` fixture isolate one defect, as its docstring says?

Yes for all six, with two coverage caveats.

Declared vs observed sets (reference over the built fixtures, `BATTERY_CHECK wrong=0`):

```
p23-p2-receipt-deleted  declared=P2     rc=1 observed=P2     P2 DEFECT receipt unreadable: … / P3 ok rows=22 … / P4 ok checked=22
p23-p2-receipt-byte     declared=P2     rc=1 observed=P2     P2 DEFECT receipt_sha256=fd3829017c42… / P3 ok / P4 ok
p23-p3-heading-renamed  declared=P3,P4  rc=1 observed=P3,P4  P3 DEFECT no '## Located quotes' section / P4 DEFECT no parsed quote
p23-p3-seven-texts      declared=P3     rc=1 observed=P3     P3 DEFECT rows=8 distinct_quotes=7 distinct_lines=8 out_of_word_range=0
p23-p3-seven-locations  declared=P3     rc=1 observed=P3     P3 DEFECT rows=8 distinct_quotes=8 distinct_lines=7 out_of_word_range=0
p23-p3-two-word-quote   declared=P3     rc=1 observed=P3     P3 DEFECT rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=1
```

1. **Exactly one clause each** (except the declared `{P3,P4}` pair). The docstring's "unavoidable" claim for
   `p23-p3-heading-renamed` holds: `_parse_quotes` returns before parsing unless `^## Located quotes` matches,
   so a parsed quote without that heading is impossible.
2. **Each fixture reacts to its own mutant and no other P2/P3 mutant** (7×6 matrix, `harness-final.txt`):

```
  mutant  p23-p2-receipt-deleted  p23-p2-receipt-byte  p23-p3-heading-renamed  p23-p3-seven-texts  p23-p3-seven-locations  p23-p3-two-word-quote
  M02      K                       .                    .                       .                   .                       .
  M03      .                       K                    .                       .                   .                       .
  M04      .                       .                    K                       .                   .                       .
  M05      .                       .                    .                       .                   .                       .
  M06      .                       .                    .                       K                   .                       .
  M07      .                       .                    .                       .                   K                       .
  M08      .                       .                    .                       .                   .                       K
```
   Perfect diagonal, empty M05 column (as expected: no p23 fixture presents an unparsed row).
3. **The stated mechanisms are the mechanisms the gate reports.** M06's docstring says "7 distinct texts on
   8 distinct located lines" → gate prints `distinct_quotes=7 distinct_lines=8`; M07 says the reverse →
   `distinct_quotes=8 distinct_lines=7`; M08 says "still verbatim" → `P4 ok checked=22`. M02's docstring says
   the deletion is staged so P9 stays clean → `--require-clean-tree` is in the argv, P9 does not appear in the
   DEFECT set. "P10 is not asked to run" is true by construction (`rerun=False`).
4. **Caveat A (coverage, the X2/Y3 finding).** Both count fixtures sit *one below* the floor (7) and the
   genuine table sits at 22, so neither floor's equality point is ever presented; the module cannot detect a
   gate that raises `min_quotes`/`min_distinct_locations` by one. The module's isolation claim is true, its
   floor *calibration* claim is incomplete.
5. **Caveat B (unreachable branch).** `p23-p3-two-word-quote` exercises only the low word bound; the high
   bound (25) is unreachable for this capture set (max 16 words per `test_outputs.py` line, max genuine quote
   19 words), so no fixture of any battery can demonstrate it. Not a repair target — a limit of the corpus.
6. `p23-p2-receipt-byte` edits `data[0]`. That is harmless (the gate compares full digests and every
   weakening is inert or always-true, see Z1), but the docstring's "one byte differs" is the most
   digest-forgiving byte choice; it carries no demonstrable extra risk.

## Axes, impact, smallest safe correction

Axes: (1) frozen-mutant calibration breadth beyond the 55; (2) per-fixture isolation as documented;
(3) instrument observability (which mutants no battery can ever kill); (4) reproducibility of every number.

Impacted: **C1 calibration coverage only** (the battery, not the gate, not the frozen predicate). The frozen
C1 sentence counts only the 55 frozen mutants, so 3 killed / 1 survived here neither passes nor fails C1; it
bounds what a reader may infer from `PREDICATE C1 pass` — the battery pins each P3 branch *firing*, not each
threshold's exact value. No lane file was edited and none should be for this seat.

Smallest safe correction (wave-3 request, not this seat's edit): add to `plans/battery37/p23.py` one
`expect: accept` fixture holding the genuine table cut to eight rows — bytes already exercised by
`probe.py`'s `eight` fixture (`ref P3 ok rows=8 distinct_quotes=8 distinct_lines=8 out_of_word_range=0`,
`ref=rc0 defects=-`) — declared `"defects": []`. It kills X2 and Y3 and closes both floor boundaries with one
fixture. Optional second: one `expect: reject` fixture at `min_quotes - 1` *texts* with a located-line count
of exactly 8 so the two floors are separated by more than the fresh/22 pair.

Scratch `/fast/scratch/hyaku/kengaku-r37/F37XMutP23` removed after copying receipts; harness and probe are
kept in `falsify/F37XMutP23/`. No tooling was installed or upgraded.

VERDICT: extra-mutants-p23-killed-3/4
