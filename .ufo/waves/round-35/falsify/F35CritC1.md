# F35CritC1 — C1 coverage falsification (round 35, wave 2)

Seat: F35CritC1 (critic). Target: C1 as declared — pinned TB2 `protein-assembly` grader admitted
with an executed probe; frozen predicate `python3 plans/round35_c1_verify.py --lane .` →
`checks=6 defects=0` + `PREDICATE C1 pass`, exit 0. Freeze `11d64530`, landing `dfee6fff`.
All runs read-only in the lane or in `/tmp/k35f-*` fixture clones; no lane writes; no installs
(existing `uv` + cached biopython 1.85 used, as in wave-1 reports).

## Evidence executed

| # | Command | Output |
|---|---|---|
| E1 | `python3 plans/round35_c1_verify.py --lane .` (live lane, tip) | `V1 ok … V6 ok / checks=6 defects=0 / PREDICATE C1 pass` exit 0 |
| E2 | fixture clone @ `11d64530`, same counter | `V1 DEFECT SHA256SUMS absent / V2 DEFECT S105 present 0 times / V3 DEFECT entry absent / V4 DEFECT index row absent / V5 DEFECT probe receipt absent / V6 ok / checks=6 defects=5 / PREDICATE C1 fail / exit=1` — byte-matches `claims/control-c1-nothing.txt` |
| E3 | fixture clone @ `dfee6fff`, same counter | `checks=6 defects=0 / PREDICATE C1 pass / exit=0` |
| E4 | `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` | exit 0; `diff` vs committed receipt → `FRESH==RECEIPT byte-identical`; last line `cases=18 observed_pass=5 observed_fail=13 mismatches=0` |
| E5 | `python3 plans/tb2_grader_probe.py --lane .` (host python, no Bio) | `ModuleNotFoundError: No module named 'Bio'` — the probe requires the uv-provided `biopython==1.85` (as the receipt header records); counter V5 falls back to uv, so the predicate still runs |
| E6 | `git show 11d64530:plans/tb2_grader_probe.py \| sha256sum` vs tip | identical `acd7d38d…040d0`; `git show 11d64530:plans/round35_c1_verify.py` vs tip identical `05a6137d…286f7`; receipt **absent at freeze**, first lands in `4fe72a9` |
| E7 | fresh fetch of the three pinned raw URLs | `test_outputs.py` sha256 `44a05a24…096582`, `test.sh` `9ede4664…267b5`, `instruction.md` `1bb2af1d…03f7c5` — all equal the manifest entries |

## Counterexample (strongest): junk package reaches the target

Fixture at tip (`dfee6fff`), only three C1 substance files replaced — the probe, the receipt, and
the entry — everything else (captures, rows, README, census) untouched:

- `plans/tb2_grader_probe.py` → **stub** that never imports the grader, never computes a case; it
  prints a static 21-line text ending `cases=18 observed_pass=5 observed_fail=13 mismatches=0`.
- `corpus/evidence/round35/tb2-grader-probe.txt` → exactly the stub's stdout.
- `corpus/knowledge/tb2-protein-assembly-grader.md` → head `source:` lines (S105–S107) verbatim,
  `verified-at: 2026-10-25`, `recheck: 180d`, a Negative-space section containing “falsified”,
  and a Located-quotes table of **8 identical one-word quotes** (“import” from `test_outputs.py:4`).

Frozen counter output in that fixture:

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

A do-nothing control cannot reach the target (E2 red), but a ~2 KB stub control can. The counter
cannot distinguish the executed instrument from a stub that does none of the claimed reading, case
construction, or grader execution.

## Findings

1. **V5 byte-equality is self-consistency, not evidence of execution.** V5 re-runs whatever sits
   at `plans/tb2_grader_probe.py` and byte-compares to the committed receipt; nothing pins the
   probe's bytes (V1 pins only the three `tb2-eval/` captures; no check hashes the probe). The junk
   package passes V5 with a probe that never touches the grader. The committed receipt *is* genuine
   in the landed artifact (E4/E7; the real probe digest-gates the grader and executes
   `test_gblock()`), but the counter alone does not establish that.
2. **V3's quote floor is form, not content.** “≥8 located quotes verified against capture lines” is
   satisfied by 8 copies of the one-word token `import` from one capture line — the counter never
   requires distinct quotes, distinct lines, or multi-token quotes.
3. **The 18-case table supports “instruction requirement → enforcing assertion” only partially.**
   The instruction has 15 bullets. Cleanly exercised: file-shape/no-empty-lines, GS-linker alphabet,
   no start/stop codons, no N/C-terminal linkers, linker length 5–20, and subprotein order.
   Partial/confounded: donor-PDB identity (fails via the *order* assertion, `find()` → −1), N-term
   Met removal (only the FLAG N-term is testable), “acceptor/donor separated only by DHFR and GS
   linkers” (only via order swap), GC window (high side only), ≤3000 nt (only via the structurally
   invalid repeated-donor case — no clean witness for the cap), “GS linker between every subprotein”
   (no missing-linker case). **Not exercised at all:** the antibody-binder bullet (most-common
   variant, don't repeat), the DHFR-from-`plasmid.gb` bullet, and the FPbase spectral bullet. The
   entry discloses the three uncovered bullets and the confounded rows (its findings 1–3), which is
   honest — but the table header “Instruction requirement → enforcing assertion (executed, 18
   cases)” overstates what 18 cases show, and the counter does not check any of this.
4. **Coverage-axis honesty holds.** The baseline README (`58a19f37`) still carried the open clause
   “the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's …)”; round
   34 captured the bytes but admitted nothing (round-34 C1 not admitted; D3 even found the round-34
   manifest omitted the evaluator files); round 35 discharges the clause for `protein-assembly` only
   and adds a genuinely new instrument (the probe first appears at the freeze). This is a real
   frontier→core move — the new instrument + first admission — not merely quality work over round-34
   captures, though the reading itself leans on round-34 captures whose bytes are identical.
5. **Prediction-before-run is commit-historical, not byte-provable.** The probe with its frozen
   predictions is committed at the freeze; the receipt first lands later (`4fe72a9`). That ordering
   supports the claim but relies on the freeze commit as a trust anchor — no byte inside the receipt
   or counter can prove the predictions were written before the first run.

## Smallest safe corrections

- Pin `plans/tb2_grader_probe.py`'s sha256 in the counter's FILES-like table (as V1 pins the
  captures), so a substituted stub or mutated probe is a defect.
- In V5, recompute `mismatches` against an independent oracle (or at least require the case lines
  to enumerate the frozen case table and pass `observed_pass + observed_fail == cases`).
- In V3, require ≥8 *distinct* quoted strings, each ≥3 whitespace tokens, drawn from ≥3 distinct
  capture lines.
- In the entry, retitle the mapping table to “instruction bullets exercised (12/15), with
  confounded rows marked”, or add the missing cases (missing-linker, acceptor substitution, DHFR
  substitution, antibody-binder repeat-under-cap) so the “enforcing assertion” rows are not
  conflated with the cap/order assertions.

VERDICT: c1-critic-falls-5-findings
