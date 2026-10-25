# R35CritControls — C1 cheapest-junk falsifier (round 35, wave 1)

Seat: R35CritControls (critic). Target: C1 coverage counter `plans/round35_c1_verify.py`
(frozen predicate: `checks=6 defects=0` + `PREDICATE C1 pass`, exit 0). Freeze commit
`11d64530179b78e33ba6074fc77d63d36ee7ac31` (lane head; claims `plans/round-35-claims.md`).

## Axes

1. **Passability** — can any package make the frozen counter print `checks=6 defects=0`?
2. **Cheapness** — minimum bytes/edits, and how much of the claimed work (grader execution,
   located-quote verification, meaningful teaching rows) is skipped.
3. **Legitimacy of the leftover** — what part cannot be faked (V1's cryptographic pin) vs what
   is empty form (V3/V5/V2).

## Method (fixture)

Per fixture rule: `D=$(mktemp -d /tmp/k35-XXXX)`; `git clone -q --no-checkout --shared <lane> "$D/lane"`;
`git -C "$D/lane" sparse-checkout set --no-cone corpus plans`; `checkout -q master`; verified
`rev-parse --show-toplevel` == `$D/lane`. Nothing in the live lane was written; no campaign tools
run; no tools installed (no pacman/uv transactions).

Baseline at freeze (measured in the clone): 41 committed `corpus/knowledge/*.md` files, 41 README
index rows, zero S105–S107 rows, no entry, no capture, no receipt. Controls confirm both red
baselines: `control-c1-nothing.txt` (V1 SHA256SUMS absent, V2 S105 present 0 times, V3 entry
absent, V4 index row absent, V5 receipt absent, V6 ok → 5 defects) and `control-c1-skip.txt`
(V1/V2/V3/V5/V6 red → 5 defects).

## The junk package (exact bytes)

Contents (all under `corpus/` / `plans/` of the clone; entry staged with `git add` so
`git ls-files` counts it):

1. **Captures (real, unavoidable)** — `corpus/evidence/round35/tb2-eval/` with the three pinned
   files, byte-identical to the pin (sha256 match): `test_outputs.py` 3847 B
   `44a05a24…096582`, `test.sh` 631 B `9ede4664…c267b5`, `instruction.md` 2655 B
   `1bb2af1d…03f7c5`; manifest `SHA256SUMS` (237 B, `d310e34d…62a2a84`) lists exactly these
   three at the pinned digests. This is the only part V1 lets survive: the digests are
   cryptographic commitments to authentic bytes, so any passing package must carry them.

2. **Probe = stub (the artifact)** — `plans/tb2_grader_probe.py` (385 B,
   sha256 `6f141799…d8fd888`), which never imports, reads or executes the grader:
   ```
   #!/usr/bin/env python3
   """Stub round-35 C1 probe: prints a pre-recorded receipt without reading the pinned grader."""
   import sys
   assert sys.argv[0].endswith("tb2_grader_probe.py")
   print("tb2 protein-assembly grader probe (stub, 18 frozen cases)")
   print("case  1: PASS G-only linker")
   print("case 18: FAIL order message")
   print("cases=18 observed_pass=5 observed_fail=13 mismatches=0")
   ```
   Contrast: the real instrument loads the pinned `test_outputs.py`, refuses unless sha256
   equals the pin, builds synthetic gblocks, runs `test_gblock()` on 18 frozen cases with
   pre-written predictions, and emits the receipt. The stub emits the identical bytes.

3. **Receipt = stub output** — `corpus/evidence/round35/tb2-grader-probe.txt` (169 B,
   sha256 `7f55cb17…e1c266`):
   ```
   tb2 protein-assembly grader probe (stub, 18 frozen cases)
   case  1: PASS G-only linker
   case 18: FAIL order message
   cases=18 observed_pass=5 observed_fail=13 mismatches=0
   ```
   V5 re-runs the (stub) probe fresh and byte-compares — always equal; summary parses green
   (`mismatches=0`, `observed_pass=5 ≥ 1`).

4. **Entry** — `corpus/knowledge/tb2-protein-assembly-grader.md` (1090 B,
   sha256 `357ad9c8…91d4df`). Head = 3 source lines (S105/S106/S107 carrying the pinned raw
   URLs), `verified-at: 2026-10-25`, `recheck: 180d`. `## Negative space` contains
   "falsifiable". `## Located quotes` contains **8 identical one-word quotes, all from line 4
   of `test_outputs.py`** (`import re`), i.e. the "quotes all from one line" pattern:
   ```
   | | “import” | `test_outputs.py:4` |
   | | “import” | `test_outputs.py:4` |
   | | “import” | `test_outputs.py:4` |
   | | “import” | `test_outputs.py:4` |
   | | “import” | `test_outputs.py:4` |
   | | “import” | `test_outputs.py:4` |
   | | “import” | `test_outputs.py:4` |
   | | “import” | `test_outputs.py:4` |
   ```
   Body carries the receipt summary line verbatim.

5. **Rows with junk teaches cell** — three SOURCES rows inserted before `## Paths` (in the
   `## Registry` section), all with teaches cell literally `junk`, anchor `pin 2fd12b88`,
   scope `pinned grader bytes`, URL exactly the pinned raw URL (no `#L…` fragment):
   ```
   | S105 | Terminal-Bench 2.0 protein-assembly grader source — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py | code | A | pinned grader bytes | pin 2fd12b88 | junk | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-protein-assembly-grader.md |
   | S106 | Terminal-Bench 2.0 protein-assembly verifier runner — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test.sh | code | A | pinned grader bytes | pin 2fd12b88 | junk | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-protein-assembly-grader.md |
   | S107 | Terminal-Bench 2.0 protein-assembly task instruction — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/instruction.md | docs | A | pinned grader bytes | pin 2fd12b88 | junk | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-protein-assembly-grader.md |
   ```

6. **README arithmetic** — one additive index row inserted before the existing
   `knowledge/benchmark-grader-semantics.md` row
   (`| `knowledge/tb2-protein-assembly-grader.md` | TB2 protein-assembly grader | S105, S106, S107 |`)
   → 42 index rows; coverage-map bullet `- TB2 grader (junk package): knowledge/tb2-protein-assembly-grader.md`
   added under `## Coverage map`; the entry staged so `git ls-files corpus/knowledge/*.md` = 42.

## Score (frozen counter, run in the clone)

```
V1 ok
V2 ok
V3 ok
V4 ok
V5 ok
V6 ok
checks=6 defects=0
PREDICATE C1 pass
counter_exit=0
```

Direct census: `scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md` → exit 0
(only pre-existing W04 duplicate-URL warnings, unrelated to the package).

## Finding

The frozen C1 counter is completely satisfiable by a ~2 KB junk delta (excluding the mandatory
real pinned bytes) that performs **none** of the claimed substance:

- V5's "executed offline probe" is faked by a stub that never touches the grader — the receipt is
  self-produced, `cases=18 observed_pass=5 observed_fail=13 mismatches=0` is just printed text.
- V3's "≥8 located quotes verified against capture lines" is faked by 8 copies of the one-word
  token `import` from a single line of the capture.
- V2's rows carry a literal `junk` teaches cell; the census accepts it (E/W codes do not look at
  teaches semantics for mined/A rows).
- V4 passes via index arithmetic (one additive row + one staged knowledge file), no content.
- The only unfakeable part is V1: the three pinned files must be the authentic bytes (cryptographic
  hash pin). So a passing package necessarily contains the real grader source — but that is the
  admission surface, not the claim's substance; the claim's *reading and executing* is fully
  skippable.

This is the "receipt produced by a modified probe" + "quotes all from one line" +
"teaches cell is junk" package the task asked to test, and it scores 0 defects. The cheapest-junk
package is therefore **0 defects** (the counter's own bar), i.e. the counter cannot distinguish
junk from the real build at its V-checks.

## Smallest safe corrections (suggested to L1)

1. **V5: pin the instrument.** Add the frozen sha256 of `plans/tb2_grader_probe.py` to the
   counter's FILES-like table; any other bytes → defect. A stub cannot then masquerade, and the
   receipt is meaningful only if it comes from the pinned instrument.
2. **V3: quote quality.** Require ≥8 *distinct* quoted strings, each ≥3 whitespace tokens, drawn
   from ≥3 distinct capture lines (monotone line numbers). This blocks the all-from-one-line
   repeat pattern.
3. **V2/V6: teaches semantics.** Gate the teaches cell (e.g. reject generic tokens like `junk`/
   `teaches`, require it to mention the graded predicate) or delegate to a QUALITY Q-criterion
   check; the census alone does not police it.
4. **V5 summary cross-check:** require `observed_pass + observed_fail == cases` and that the case
   lines enumerate the frozen case table — cosmetic until the instrument is pinned, but cheap.

## Evidence & provenance

- Commands producing every number are in this report; run outputs captured verbatim.
- Fixture: `/tmp/k35-ydi9/lane` (clone of freeze `11d6453`); package archive (exact bytes) copied
  to `.ufo/waves/round-35/build/R35CritControls/package/` (SHA256SUMS, test_outputs.py, test.sh,
  instruction.md, tb2-grader-probe.txt, tb2_grader_probe.py, tb2-protein-assembly-grader.md,
  SOURCES.md, README.md).
- Live lane untouched: no writes outside `.ufo/waves/round-35/build/` and `/tmp`; no git
  add/commit on the live lane; no campaign tools; no installs.

VERDICT: cheapest-junk-0-defects
