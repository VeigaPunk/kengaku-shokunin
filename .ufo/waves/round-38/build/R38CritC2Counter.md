# R38CritC2Counter — attack report: `plans/round38_c2_verify.py` (C2, round 38 wave 1)

Target: `plans/round38_c2_verify.py` + `plans/pkg_gate.py` at lane tip `2c5f4e0` (frozen at `e0a3785`, first receipt run
`e95cf55`). Nothing frozen was edited. All work happened in a scratch clone
`/fast/scratch/hyaku/kengaku-r38/R38CritC2Counter/base` (`git rev-parse --show-toplevel` = that path); the lane tree was
never written (its plan/corpus digests are unchanged; the counter's own `PINS`/V1/V5 report `mismatched=0`).

Reproduce: `python3 attack.py` in the scratch dir; transcript and the filler entry are in
`.ufo/waves/round-38/build/R38CritC2Counter/` (`attack-transcript.txt`, `filler-entry.md`).

## 1. Headline counterexample — the cheapest package reaches `checks=7 defects=0`

The package below was generated **without reading one line of the grader's semantics**. It contains, in the entry
itself, a statement that contradicts the receipt's own summary line, eleven verbatim quotes each attached to a false
claim, two registry `teaches` cells that assert the opposite of the capture, and a `## Negative space` section that
says it offers no falsifier:

```
$ python3 plans/round38_c2_verify.py --lane . --work $S/w
V1 ok listed=5 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=11 distinct_quotes=11 distinct_lines=11 out_of_word_range=0
    gate: P4 ok checked=11 bad=0 first=0
    gate: P5 ok manifest_entries=5 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=45 knowledge_files=45 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5537
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=22 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=7 tags=7 bad=0
checks=7 defects=0
PREDICATE C2 pass
exit 0
```

The entry it accepts states, in `## Summary`:

> "The 22-case probe found no passing case at all: 0 pass, 22 fail, so the grader enforces every requirement the
> instruction states and no unenforced half exists."

The receipt one directory away says `cases=22 observed_pass=7 observed_fail=15 mismatches=0`
(`corpus/evidence/round38/build-pmars-probe.txt:26`). This is not an unverifiable prose judgement: the receipt
summary is a single frozen line the counter already parses in V4, and nothing compares the entry to it.

False claims that survive P4 (quotes verbatim, claims unchecked — `plans/pkg_gate.py:148` only tests
`q.text not in ...`), e.g. `filler-entry.md` row 1: claim *"the grader rebuilds pMARS from Debian source and compares
the binary with the oracle build"* on quote *"Build pMARS (http://www.koth.org/pmars/) from source with no X server."*
(`instruction.md:1`). The capture has ten assertions and no `make`/`dpkg`/`gcc` line at all
(`grep -n "make\|dpkg\|gcc" corpus/evidence/round38/tb2-build-pmars/test_outputs.py` → no match).

The `## Negative space` requirement is satisfied by its own negation — `plans/pkg_gate.py:229` only searches for
`falsifi(?:er|ed|es|ability)`, so this text passes:

> "Falsifier: no falsifier is offered for the summary above; … nothing here is stated in a form a counter could
> contradict."

Registry `teaches` cells (P6 only counts words ≥ 8 and distinctness) also lie: S115 *"the grader rebuilds pMARS with
make and diffs the built binary …"*, S116 *"the instruction requires a running X server for the debugger …"* — the
instruction's first line is *"Build pMARS … with no X server."* (`instruction.md:1`).

**Cost of the attack:** one `grep -n` over two captures for 11 lines, the 4-line label printer in §4, two registry rows,
two README lines. The whole build is 110 lines of Python (`attack.py`, `awk '/^# -+ build filler package/,/^say\(""\)/' | wc -l`
→ 110; 254 lines total), most of it the 11 quote rows; the lines were picked by grep and the claim cells were written
without reference to the grader's behaviour — the falsehoods §1 documents are what the entry *claims*, not a reading.

## 2. V3 (`anchor digests`) — the token is bound to the digest, not to the row's provenance

`plans/round38_c2_verify.py:145` `toks = re.findall(r"sha256\s+([0-9a-fA-F]+)", found[0][5])`; the clause requires
only `toks == [row["sha256"]]` plus eleven cells.

| probe | result |
|---|---|
| C1 bare anchor cell, `sha256 <digest>` and nothing else (the package as built) | `V3 (True, 'rows=2 bad=0')` |
| C2 junk around it, `no commit, no line, no quote — irrelevant filler — sha256 <digest>` | `V3 (True, 'rows=2 bad=0')` |
| C3 digest twice (negative control) | `V3 (False, "…['S115:anchor_digest']")` |
| C4 the other row's digest (negative control) | `V3 (False, "…['S115:anchor_digest']")` |
| C5 row **title** says `chart-generation` / `regex-log` instead of `build-pmars` | `V3 (True …)`, `P6 ok rows=2 bad=0`, `census_exit = 0` |
| C6 `opened` changed to `1999-01-01` | `V3 (True …)`, `gate defects=1` (only P2, the counter-filled digest), `census_exit 0` |

So every other registry row's anchor convention — commit pin, line range, quoted sentence
(`corpus/SOURCES.md:125` S110: `commit 2fd12b88…, instruction.md:1-19, :3 "…"`) — is optional for the rows the
admission rests on, and the row can name a different task while V3, P6 and the census are green. The spec's
`row_opened: "2026-10-26"` is read by neither `pkg_gate.py` nor the counter (`grep` over both files), so the frozen
opened date is unenforced.

## 3. V4 (`match=NO` naming) — presence-only, and vacuous on the landed receipt

`plans/round38_c2_verify.py:184` `unnamed = [c for c in no if f"`{c}`" not in entry]`. With a receipt variant whose
`canned-shape` observed verdict is flipped to `fail`/`match=NO` (mismatches=1):

| probe | result |
|---|---|
| D1 not named anywhere (negative control) | `(False, 'cases=22 mismatches_named=0/1 …')` |
| D2 blanket list of all 22 ids in backticks | `(True, '… mismatches_named=1/1 bad=0')` |
| D3 the id inside a fenced block | `(True, '… 1/1 bad=0')` |
| D4 a sentence that *denies* covering it: "The summary above says nothing about `canned-shape` …" | `(True, '… 1/1 bad=0')` |

And on the receipt that can actually land, the clause has no subject: `mismatches=0`, so `V4 ok …
mismatches_named=0/0`, and V2's P10 byte-compares the receipt to a fresh probe run, so no author can introduce a
`match=NO` line. The clause is unfalsifiable by construction on this package, not merely weak.

## 4. V7 (`requirement map`) — duplicate authority, invisible rows, and a printer for labels

`plans/round38_c2_verify.py:222` `sec = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", entry, re.S | re.M)` reads
the **first** heading anywhere in the entry, including inside a code fence; rows that fail `MAP_ROW` are only reported
when `l.startswith("|")`, so an indented row is invisible.

| probe | result |
|---|---|
| E0 base | `(True, 'rows=7 tags=7 bad=0')` |
| E1 one label changed in the parsed section (negative control) | `(False, "… 'from-source: labelled enforced, receipt derives partly'")` |
| E2 a **second** `## Requirement map` section, every label `enforced` | `(True, 'rows=7 tags=7 bad=0')` |
| E3 indented rows, every label `enforced`, inside the parsed section | `(True, 'rows=7 tags=7 bad=0')` |
| E4 prose in the parsed section: "Every tag above is fully enforced …" | `(True, 'rows=7 tags=7 bad=0')` |
| E5 a **fenced decoy** map first (correct labels), visible map all `enforced` | `(True, 'rows=7 tags=7 bad=0')` |
| E6 a tag dropped (negative control) | `(False, '… tags missing=[…]')` |
| E7 a tag duplicated in the same section (negative control) | `(False, '… duplicated=[…]')` |
| E8 a non-violating case cited (negative control) | `(False, "… 'no-x11: cites no case or a case that does not violate it'")` |

E2/E3/E5 are the D2 fix being routed around: the table a reader sees can say `enforced` for every tag while the parsed
copy says `partly`. E5 shows the parse target is positional, not structural: a map shown inside a fenced block is
authoritative if it comes first.

E9 — the label column is a pure function of the frozen receipt and the frozen dry table. The 4-line printer in
`attack.py` produced `['partly', 'partly', 'partly', 'partly', 'partly', 'partly', 'partly']`, identical to the
entry's column; `derive()` reads only `observed` and `violates=`. So V7 cannot tell an author's reading from a
regenerated table — it is a checksum of the receipt, and it forces every tag to one label (all seven here). The
counter's own docstring says the label must "equal the label DERIVED from every receipt case"; that is now the only
permitted value, so the round-37 defect (a map misstating enforcement) is made **unrepresentable**, not detected.

The one free cell — the `cases` column — is satisfied by the alphabetically first violator: the generated package cites
`c-is-dir` (observed `pass`) as the sole witness for `from-source`, `debian-source`, `extract-to-app` and
`debugger-works`, and `empty-tree` (the do-nothing control) for the rest. Transcript §B: distinct case ids cited in the
entry = `['c-is-dir', 'canned-x11-dlopen', 'empty-tree']`. That is the same shape round-37 closure D2 called a defect
("a label chosen from one convenient witness"), now legal in the cases column.

## 5. Surface named by the frozen claims but read by nothing

The claims' C2 surface lists "README index + coverage bullet, PROVINCE paragraph". `PROVINCE.md` is read by neither
`pkg_gate.py` nor `round38_c2_verify.py` (grep: no match), and the accepted package leaves `PROVINCE.md` untouched
(`F. PROVINCE.md mentions build-pmars: False`). The README index row and bullet are shape-checked only (P8: one row
citing S115/S116, one `- ` bullet naming entry + receipt path), so their text is free.

## 6. What the counter does have teeth on (do not "fix" these)

- V2's P10 genuinely re-runs the frozen probe and byte-compares (`P10 ok probe_rerun=byte-equal bytes=5537`; a fresh
  standalone run takes 0.97 s, byte-equal to the receipt). The hand-typed receipt of the skip control cannot land.
- V1/V5's capture, probe and dry-table digests are tight; `PINS`/`P5` reported `mismatched=0`, `bad=0`.
- V6's census run is real: `census_exit=0` with the W04 lines it emits.
- Negative controls E1/E6/E7/E8, C3/C4, D1 fail as they should; the clauses are not vacuous, they are shape-limited.

Fragility worth naming (not a hole): `c_rerun` needs `bwrap`+`gcc`+the host shell, and on this host `Bio` is absent so
it goes through `uv run --no-project --with biopython==1.85` (cached here: 0.016 s). On a cold host with no network that
path fails P10 for a reason that has nothing to do with the package — a false-red inside the frozen counter.

## 7. Impacted axes

- **coverage (8th):** unchanged at 7; C2's counter certifies form, not the admission. `checks=7` can be printed by a
  package whose entry contradicts the receipt it cites.
- **calibration:** the frozen predicate (`claims` §C2) presents `checks=7 defects=0` as the admission. A green counter
  here is evidence about eleven substrings and eight word-counts, so the predicate currently overstates what it measures
  — the same class as round-37's "label from one witness", one level up.
- **depth / novelty / operability:** untouched; the probe and P10 keep their value.

## 8. Smallest safe correction (all local, all receipt-checkable)

1. **Bind the entry to the receipt's own summary line.** One clause: the entry must contain a line
   `receipt: cases=<n> observed_pass=<p> observed_fail=<f>` equal to the receipt's `SUMMARY` line, and must contain no
   other `observed_pass=<…>` statement. Kills the §1 counterexample with ~6 lines of code.
2. **Make the quote claim testable.** Extend `QUOTE_ROW` to a fourth cell carrying a case id (`` `case-id` ``) and
   require ≥4 distinct ids, at least two of them observed `pass`; the claim cell must contain a polarity token
   (`passes`/`fails`/`not checked`) that agrees with that case's observed verdict. Forces the entry's prose to face the
   22 rows instead of 8 word-counts.
3. **`## Negative space`:** require `falsifier: <case-id>` and check the id exists in the receipt; reject the section
   when the sentence containing `falsifi*` also contains `no ` / `none` / `not offered` (P7's own failure mode).
4. **V3:** require the anchor cell to carry `raw_base+upstream`'s basename **and** the commit `2fd12b88` **and** the
   digest, and reject a row whose title/scope names a task other than the spec's `name`-bearing capture; use
   `row_opened` or delete it from the spec.
5. **V7:** require exactly one `^## Requirement map` heading in the entry (count, fence-aware), reject indented
   `instruction.md:` rows instead of skipping them, and require each row's `cases` cell to cite at least one
   observed-`pass` violator where one exists and one observed-`fail` violator where one exists — the discriminating
   pair, so `empty-tree`/`c-is-dir` alone cannot stand in for the reading.
6. **Read `PROVINCE.md`:** require the entry's id in the TB2 frontier paragraph the claims name, or drop that clause
   from the frozen surface.

Items 1–3 are worth ~25 lines and close the false-admission class the task asked about. Items 4–6 close false
provenance. None requires a judgement call the counter cannot make.

## 9. Answers to the three assignments

- **Cheapest package reaching `checks=7 defects=0` without being a real admission:** built and pasted (§1);
  110-line generator, receipt reused unmodified (P10 forces that), 11 verbatim quotes with false claims, a Summary that
  contradicts the receipt, and a mechanically printed map.
- **V3's binding:** bound to the row's digest only (§2, C1/C2 green, C3/C4 red); provenance cells (commit, lines,
  quote) and the row's own title are free text (C5/C6).
- **V4's `match=NO` naming via backticks:** presence-only — blanket list, fence, or a sentence denying coverage all pass
  (D2–D4); the clause is vacuous on the landed receipt (D5, `0/0`).
- **V7 row parsing:** duplicate section, indented rows, prose labels, and a fenced decoy are all invisible to it
  (E2/E3/E4/E5); labels are a printer of the receipt (E9) and the citations can be the do-nothing cases.

VERDICT: c2-counter-holes-8
