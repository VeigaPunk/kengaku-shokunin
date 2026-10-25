# F35ReopenS105 — falsification of S105 (TB2 `protein-assembly` grader) at the round-35 landing tip

Seat: `F35ReopenS105` (scout, leaf — no subagents, no background jobs).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Landing tip audited: `dfee6fff631ebc5f623ba4506e5c7992a215401c` (branch `master`).
Scratch: fixture `/tmp/f35reopen105-*` (removed at the end); scripts under
`.ufo/waves/round-35/falsify/F35ReopenS105/`. No tool installed or upgraded (stock `curl`, `git`, `python3`,
`uv` were already present). Nothing outside `.ufo/waves/round-35/falsify/` and `/tmp` was written; no
lane file was edited by this seat.

---

## Axes

1. **Coverage** — does the S105 row's *content* (scope, anchor, teaches) hold against the bytes it cites?
2. **Freshness** — do the pinned upstream bytes still equal what the lane captured and pinned?

---

## Summary of what I attacked, and the evidence that would have shown disagreement

| # | Attack | Command | Result |
|---|---|---|---|
| 1 | Does upstream `test_outputs.py` @ `2fd12b88` still equal the pinned digest? | `curl` of the pinned raw URL + `sha256sum` | **agree** — `44a05a24…96582` = pinned |
| 2 | Does the capture match the manifest? | `sha256sum -c corpus/evidence/round35/tb2-eval/SHA256SUMS` | **agree** — 6/6 `OK` |
| 3 | Capture bytes == live upstream bytes? | `cmp` of capture vs fresh fetch | **agree** — byte-identical |
| 4 | Is the pin still upstream's branch tip (nothing newer to re-ground against)? | `api.github.com/…/commits/main` | **agree** — `main` HEAD *is* `2fd12b88` (2026-04-30) |
| 5 | Is the S105 row's anchor quote byte-exact on `test_outputs.py:42`? | repro §3 | **agree** — verbatim on line 42 |
| 6 | Is every `test_outputs.py` quote in the entry's `## Located quotes` byte-exact at its cited line? | repro §4 | **agree** — 15/15 |
| 7 | Do the S105 scope/teaches cells say anything the file does not? | repro §5 | **agree** — 8/8 |
| 8 | Is the S105 anchor cell's `(N words)` price the lane's canonical count? | repro §6 vs `sources_adopt.py` / `round30_defects.py` `words()` | **DISAGREE at tip** — row says `(9 words)`, canonical says **11** |
| 9 | Does any instrument catch a wrong S105 anchor cell? | repro §7 (mutation) | **DISAGREE** — 3/3 mutants pass both the frozen counter *and* the canonical anchor gate |

**Verdict of the seat: the row's *content* survives; its *price* does not, and no gate can see it.**

---

## 1. Freshness — the digest chain holds end to end

Upstream re-fetch of the pinned raw URL:

```
$ curl -sS -o up/test_outputs.py \
    https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py
$ sha256sum up/test_outputs.py
44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582  up/test_outputs.py
```

The manifest, the capture and the live fetch all carry the same digest:

```
$ cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS
test_outputs.py: OK
test.sh: OK
instruction.md: OK
task.toml: OK
antibody.fasta: OK
pdb_ids.txt: OK
$ cmp up/test_outputs.py corpus/evidence/round35/tb2-eval/test_outputs.py   # (no output = identical)
```

The pin is not stale: upstream's default branch head **is** the pinned commit, so there is no newer
commit to re-ground against.

```
$ curl -sS "https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/main"
main HEAD sha: 2fd12b88aafdd04a52c298e3940bcb189f9766d6
date: 2026-04-30T05:53:30Z
```

All six pinned files were re-fetched and every digest matched `SHA256SUMS` — so the round-34→35
"byte-identical captures" claim holds for the whole manifest, not just the grader.

## 2. The probe receipt is reproducible, not asserted

Run against the pinned grader in the fixture (`biopython==1.85`, the version `test.sh` pins):

```
$ uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane "$D/lane"
$ cmp probe-fresh.txt corpus/evidence/round35/tb2-grader-probe.txt
   # (no output — byte-identical)
$ tail -1 probe-fresh.txt
cases=18 observed_pass=5 observed_fail=13 mismatches=0
```

The receipt is a re-runnable gate output, not a transcript. It also *executes* the captured
`test_gblock` (the probe loads the file by digest and patches only `Path`, so the graded function
runs unmodified) rather than re-implementing the grader.

## 3. The S105 anchor quote is byte-exact on line 42

`corpus/SOURCES.md` S105 anchor cell (as landed at tip `dfee6fff`):

```
commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test_outputs.py:42
"assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (" (9 words);
sha256 44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582
```

Line 42 of the upstream file is:

```
    assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (
```

The quoted span is a byte substring of that line (`exact=True`), the pinned digest is right, and the
cited line number is right. **The quote and its location survive; only the parenthetical price does
not.**

## 4. Every `test_outputs.py` quote in the entry is byte-exact — 15/15

The entry's `## Located quotes` table has **22** rows; **15** cite `test_outputs.py`. Each was
checked to be a byte-exact substring of the cited capture line (and ≤25 words):

```
OK  test_outputs.py:13  words= 3 | grader reads one fixed path
OK  test_outputs.py:16  words= 7 | trailing whitespace is stripped per line
OK  test_outputs.py:19  words=10 | exactly one line
OK  test_outputs.py:21  words= 3 | case-insensitive
OK  test_outputs.py:23  words=11 | length cap
OK  test_outputs.py:25  words=14 | literals replace lookups (authors' rationale)
OK  test_outputs.py:27  words= 3 | whole-gBlock translation
OK  test_outputs.py:28  words= 3 | antibody binder literal is the FLAG tag
OK  test_outputs.py:38  words= 3 | first-occurrence search
OK  test_outputs.py:42  words=11 | order assertion
OK  test_outputs.py:46  words=11 | FLAG starts the protein
OK  test_outputs.py:54  words= 4 | linker alphabet
OK  test_outputs.py:57  words= 7 | linker length
OK  test_outputs.py:60  words= 7 | SNAP ends the protein
OK  test_outputs.py:71  words= 7 | GC window bound
```

(All 22 rows of the table — including the 7 citing `test.sh`/`instruction.md` — also verify; the
counter's V3 regex matches all 22 rows, so none is silently skipped.)

Two structural details also checked and confirmed: the table uses curly quotes U+201C/U+201D
throughout (no straight-quote rows, which is what the counter's regex requires), and the entry's
"static reading" line-range table (`13–21, 22–23, 27, 28–41, 42–44, 46/60, 47–59, 65–73`) places
every mechanism on the line the file actually has it.

## 5. The scope and teaches cells say nothing the file does not

Scope: *"the executed scoring predicate of one Terminal-Bench 2.0 task at a pinned commit … for the
code's own behaviour; the comments' claims about which PDB entries match are the authors' self-report."*
Verified: the file defines exactly one function (`test_gblock`), and its comments at lines 25–26 and
29–34 make exactly the PDB-matching claims the scope cell labels as author self-report.

Teaches: *"the task score is one pytest function over literal expected subproteins, order, FLAG/SNAP
boundaries, 5-20 residue `[GS]+` linkers and 15-35 GC per 50-nt window; reference input files are
never read."* Each clause checks out against the bytes:

| teaches clause | evidence in the file |
|---|---|
| one pytest function | exactly one `def ` in the file (`test_gblock`, line 10) |
| literal expected subproteins | five `*_aa = "…"` literals, lines 28–36 |
| order | `assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx`, line 42 |
| FLAG/SNAP boundaries | `assert flag_idx == 0` (46); `snap_idx + len(snap_aa) == len(gblock_aa)` (60) |
| 5-20 residue `[GS]+` linkers | `re.fullmatch(r"[GS]+", linker)` (54); `5 <= len(linker) <= 20` (57) |
| 15-35 GC per 50-nt window | `gc = sum(c in "gc" for c in gblock[:50])` (65); `assert 15 <= gc <= 35` (66, 71) |
| reference input files never read | the only `open()` is `gblock.txt` (line 15); `pdb_ids.txt` occurs only in a comment (26) |

## 6. DEFECT — the S105 anchor cell's `(9 words)` price is wrong (canonical: 11)

The lane's canonical word counter is unambiguous and stated twice in the code:

- `plans/sources_adopt.py:280-281` — `def words(text): return len(text.split())`, with the comment
  *"a word count printed by this gate cannot disagree with one in a round's defect receipt"*.
- `plans/round30_defects.py:39-40` — the identical `len(text.split())`.

The lane's own anchor gate prices the S105 quote **11**, not 9:

```
$ python3 plans/sources_adopt.py --quote-file rows.txt \
    --artifact corpus/evidence/round35/tb2-eval/test_outputs.py
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=test_outputs.py
  ok S105 words=11 at test_outputs.py quote="assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, ("
```

`len("assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (".split())` = **11**
(`assert`, `flag_idx`, `<`, `donor_idx`, `<`, `dhfr_idx`, `<`, `acceptor_idx`, `<`, `snap_idx,`, `(`).
The row says 9. No counting rule over the quoted string yields 9: the only variant that does
(`assert` and `, (` stripped) is a *different string* than the one the row quotes. The lane's own
precedent counts code tokens the same way this row's own sibling rows do — S093 prices
`success = all_required <= passed_tests` at 5, counting `=` and `<=` as words.

Registry-wide, the parenthesis is only wrong where round 35 introduced it:

```
$ python3 - <<'EOF'   # every "(N words)" annotation in corpus/SOURCES.md vs len(split())
total annotations: 24
mismatches in pre-round-35 rows (S001-S104): 0
mismatches in round-35 rows (S105+): 2
    ('S105', claimed=9, canonical=11)
    ('S107', claimed=16, canonical=15)
```

**Precedent that this class is a defect, not a nit:** the round-31 falsify seat
`.ufo/waves/round-31/falsify/R31FxQuoteS100.md` found the same class on S100 (row priced the span at
8, canonical 6) and the lane **corrected the row** in commit `634ded8`
(`-(8 words)` → `+(6 words)`). `plans/round30_defects.py` check D3 exists solely to keep the S078
anchor's price honest. So "the row's parenthetical disagrees with the canonical counter" is a defect
the lane has already ruled on twice; round 35 reintroduced it in two new rows.

**Severity: cosmetic, not claim-breaking.** The quote text, the cited line, the digest and the URL
are all correct; the miscount is in a parenthetical that no sentence of the row depends on. It also
does not breach the ≤25-word contract rule (11 ≤ 25 either way).

**Status at this seat's write time:** the **committed tip** `dfee6fff` still carries `(9 words)`. The
lane's **working tree** has already been corrected to `(11 words)` for S105 and `(15 words)` for S107,
and `corpus/lessons/round-35.md` (also uncommitted) records the correction under "Falsify-wave
additions" — *"Rows touched old→new (correction to the Census section above): S105 anchor '(9 words)'
→ '(11 words)'; S107 anchor '(16 words)' → '(15 words)'"*. That pending edit is **not mine**: this seat
never wrote to `corpus/SOURCES.md` (its only lane writes are this report and the two scripts beside it;
every mutation ran inside the fixture clone). My re-run against the corrected tree shows
`mismatches: 0`. The finding therefore stands as of the landed tip and is already fixed in the
pending working-tree change.

## 7. DEFECT — no instrument can catch a wrong S105 anchor cell

This is the falsification-relevant part, and it is a *capability* finding rather than a content
finding. Three mutations of the S105 anchor cell, each run against **both** the frozen C1 predicate
and the lane's canonical anchor gate:

| mutant | S105 anchor cell becomes | frozen C1 counter | `sources_adopt.py` gate |
|---|---|---|---|
| baseline | (unchanged) | `checks=6 defects=0 \| PREDICATE C1 pass` | `ok S105 words=11` |
| A | wrong line **and** wrong quote (`test_outputs.py:71 "assert 15 <= gc <= 35, (" (7 words)`) | `checks=6 defects=0 \| PREDICATE C1 pass` | `ok S105 words=7` |
| B | right quote, **wrong line** (`:999`) | `checks=6 defects=0 \| PREDICATE C1 pass` | `ok S105 words=11` |
| C | right quote, right line, **wrong count** (`(99 words)`) | `checks=6 defects=0 \| PREDICATE C1 pass` | `ok S105 words=11` |

**3/3 mutants pass both instruments.** Reproduction (fixture-only; the lane is untouched):

```
$ python3 .ufo/waves/round-35/falsify/F35ReopenS105/mutate_s105_anchor.py \
    --lane "$D/lane" --fleet /home/vgpnk/Projects/shokunin --work "$D/mut"
```

Why, from the code:

- `plans/round35_c1_verify.py` **V2** (`v2()`, lines 82–99) unpacks the 11 cells into
  `_id, source, _kind, tier, _scope, _anchor, _teaches, status, opened, _recheck, used` — the
  variable `_anchor` is **never used**. V2 checks cell count, URL, tier/status/opened and used-by only.
- **V3** (lines 121–133) checks the *entry's* `## Located quotes` table for ≤25 words and byte
  presence on the cited capture line. It never reads the **row** anchor cells in `corpus/SOURCES.md`.
- `scripts/sources-census.sh` has **0** occurrences of `words`; its E-codes cover structure and
  enums (E01–E12), never a quoted span or a price.
- `plans/sources_adopt.py` *does* read the anchor cell and *does* compute the canonical count — but it
  **prints** that count (`ok S105 words=11`) without comparing it to the parenthetical the row
  states, and it locates the quote anywhere in the artifact rather than at the cited line. That is
  why mutant A (quote from the wrong line, different text) and mutant B (quote not on line 999 at
  all) both pass.

The gap is not hypothetical: mutant C is exactly the shape of the defect found in §6, and the lane's
gate prints the true count without ever failing on a disagreement with the row.

**Cheapest fix** (not applied by this seat — it edits a lane file): in `v2()`, compare the row's
parenthetical against `len(quote.split())` for each quoted span in `_anchor`, and in `sources_adopt.py`
compare the printed `words=` against the parenthetical carried in the cell. Either closes the class;
the round-31 S100 fix is the precedent that this row cell is expected to be exact.

---

## What would have shown disagreement, and did not

- A **digest or byte drift** at the pin (upstream moved, capture corrupted) — did not occur; all six
  files re-fetched byte-identically, and the pin is upstream's current branch head.
- A **quote that is not byte-exact** at its cited line (off-by-one line, dropped character, altered
  text) — did not occur; 15/15 `test_outputs.py` quotes and 22/22 table rows are exact.
- A **row cell asserting something the file does not** (scope, anchor, teaches) — did not occur on
  substance; every mechanism claimed maps to a real line of the file.
- A **probe receipt that does not reproduce** — did not occur; the fresh run is byte-identical.
- The **only disagreement found** is the row's stated word price (9 vs the canonical 11), and the
  **only capability gap found** is that no instrument compares a row's price, quote or cited line
  against the source.

## Reproduce

```
# freshness + digest chain
curl -sS -o up.py https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py
sha256sum up.py
(cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS)

# quotes, anchor, canonical word count (read-only, prints every check)
python3 .ufo/waves/round-35/falsify/F35ReopenS105/verify_s105.py --lane . --upstream up.py

# the anchor-cell blind spot (fixture-only; needs a clone, see below)
python3 .ufo/waves/round-35/falsify/F35ReopenS105/mutate_s105_anchor.py \
    --lane "$D/lane" --fleet /home/vgpnk/Projects/shokunin --work "$D/mut"
```

Fixture used (per the round's fixture rule; the live lane was never written to):

```
D=$(mktemp -d /tmp/f35reopen105-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus /plans
git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c
git -C "$D/lane" rev-parse --show-toplevel     # == "$D/lane" (verified before any write)
git -C "$D/lane" config user.name "fixture <fixture@invalid>"
git -C "$D/lane" config user.email "fixture@invalid"
# …mutations and commits happen only inside "$D/lane" …
rm -rf "$D"                                   # removed at the end of the seat
```

## Not established (scope limits)

- Nothing here re-derives the grader's *biological* correctness, or whether the five literals are
  the right PDB/FPbase/antibody answers — the grader's comments are the authors' self-report, and
  the row says so.
- Nothing about Harbor's runtime execution of the verifier, the task image, or any model's
  performance: the probe executes the captured function offline under Biopython 1.85, not the task.
- Nothing about the other 88 TB2 tasks, and nothing about the entry's other two sources
  (S106 `test.sh`, S107 `instruction.md`) — those are the sibling seat `F35ReopenS106S107`'s scope;
  my §6 finding names S107's parenthetical only as the second instance of the same class, from the
  registry-wide sweep, not as an independent re-open of that row.
- The mutation finding shows the instruments are blind; it does not show the *content* of the landed
  anchor cell is wrong beyond the §6 price (the quote, line, digest and URL are correct).

## Cleanup

The fixture `/tmp/f35reopen105-*` was removed. This seat wrote only
`.ufo/waves/round-35/falsify/F35ReopenS105/{verify_s105.py,mutate_s105_anchor.py}` and this report.
A note to siblings: a peer reported that a `/tmp/k35f-*` glob deleted a sibling's fixture. I had
created `/tmp/k35f-upstream-test_outputs.py` (a file sharing that prefix) early on; it was deleted
mid-run by such a glob and I re-fetched into a uniquely-named path. **Use a per-seat tmp prefix and
`rm -rf` only your own exact `$D`.**

VERDICT: s105-defect-quotes-15/15
