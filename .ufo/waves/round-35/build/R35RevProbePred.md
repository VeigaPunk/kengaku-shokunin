# R35RevProbePred — review of `plans/tb2_grader_probe.py` (18 frozen cases) vs pinned grader + instruction

Scope: (a) label faithfulness vs `corpus/evidence/round35/tb2-eval/instruction.md`, (b) mutant isolation via the
receipt's `assertion=` column, (c) pass-cases that may be instruction violations the grader accepts,
(d) recompute `max_passing_nt=2766`, (e) instruction bullets with no case. Leaf seat; no writes outside
`.ufo/waves/round-35/build/` and `/tmp/k35rev-*`.

## Method (commands → outputs)

1. Receipt reproduction: `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` → exit=0; `diff` vs `corpus/evidence/round35/tb2-grader-probe.txt` → `RECEIPT-BYTE-IDENTICAL` (`cases=18 observed_pass=5 observed_fail=13 mismatches=0`).
2. Arithmetic: imported `plans/tb2_grader_probe.py` (stdlib-only at module level) and re-derived `components()` from the pinned grader bytes → `component_aa_lengths {'flag': 8, 'donor': 259, 'dhfr': 158, 'acceptor': 235, 'snap': 182} sum 842`; `max_passing_nt recomputed = 2766` = 3×(842+4×20) = 3×922. All 18 case nt lengths recomputed match the receipt (2583–3378, all %3==0).
3. Runtime falsifiers (script in `/tmp/k35rev-*/falsify.py`, grader loaded from the pinned capture, same `run_grader` path as the probe):
   - `repeat-flag-under-cap` (extra 8-aa flag, 2625 nt ≤ 3000): **fail**, assertion `'Linker must only contain G and S amino acids.'`
   - `linker-s-only` (all junctions `SSSSS`): **pass**
   - `missing-linker-0aa` (empty flag→donor junction): fail, assertion `'Linker must only contain G and S amino acids.'`
   - `dhfr-one-substitution`, `acceptor-one-substitution`: fail, assertion `'Fusion protein must be in the order flag - donor - dhfr - acceptor - snap'` (same message as `donor-one-substitution` and `donor-acceptor-swapped`)
   - `valid-max-linkers-20aa` (all-G 20-aa junctions, 2766 nt): fail on GC (first violating window at 860, gc=36) — but a GS-mixed (`GGGGS`×4) encoding of the same 2766-nt construct **passes** (`windows_ok True`, grader `pass`), so 2766 is achievable.

## Findings

### F1 (HIGH) — `donor-repeated` is confounded: it fails on the length cap, and the grader has no repeat rule at all
- Receipt line: `case=donor-repeated ... nt=3378 ... assertion='gBlock must be at most 3000 nucleotides.' requirement='do not repeat a protein'` — the observed assertion belongs to the cap bullet, not to any repeat rule. The grader (`corpus/evidence/round35/tb2-eval/test_outputs.py`) contains no repeat/occurrence check; it uses `find()` (first occurrence) plus junction/terminus structure.
- Triple unfaithfulness of the label: (i) no repeat rule exists in the grader; (ii) the instruction bullet it cites — "Only encode the most common variant of that protein sequence, don't repeat the protein multiple times even if it increases binding affinity" (`instruction.md`, antibody-binder bullet) — is scoped to the **antibody binder**, while the mutant repeats **donor**; (iii) the failure is an artifact of check order (cap is asserted before structure).
- Runtime proof that repeats are rejected by structure, not by a repeat rule: a whole-protein repeat that fits under the cap (`repeat-flag-under-cap`, 2625 nt) fails on the **GS-junction** assertion, because any whole-protein copy must sit in a junction region and junctions must be `[GS]+`. So "don't repeat" is enforced only incidentally (junction purity + fixed termini + first-occurrence order), and the probe case's observed failure is purely the cap.
- Corollary: the cap bullet has no clean witness. Structure pins any grader-valid construct to 842 aa + ≤4×20 junction aa = 922 aa = 2766 nt < 3000, so "at most 3000 nt" can never be the sole violated requirement of a structure-valid construct; the only cap-reaching case in the probe is the structurally invalid `donor-repeated`.

### F2 (MEDIUM) — identity mutants are single-delta but share one assertion voice; message-level isolation is impossible
`donor-one-substitution`, `dhfr-one-substitution`, `acceptor-one-substitution`, `donor-acceptor-swapped`, and any missing protein all surface the same assertion `'Fusion protein must be in the order flag - donor - dhfr - acceptor - snap'` (verified at runtime for dhfr/acceptor; receipt shows it for donor/swap). Cause: `find()` returns −1 for any unmatched protein, and the order assertion is the grader's only voice for identity, presence, and order. The probe's labels are faithful to the instruction bullets and the receipt's `assertion=` column discloses this honestly, so these are not counted as confounded — but the receipt cannot distinguish identity from order from presence by message alone; only the case deltas can.

### F3 (MEDIUM) — pass-case audit: one candidate grader-accepts-violation, two are clean negative controls
- `uppercase` (pass): not a violation. Instruction is silent on case ("should contain only the sequence of the gBlock and nothing else"); the grader lowercases before every check (`gblock = lines[0].lower()`). Label "(case is not specified)" is honest. Negative control for the line/regex path.
- `no-trailing-newline` (pass): not a violation; `rstrip`+`splitlines` accept a final line without `\n`. Label faithful.
- `linker-20aa` (pass): within the bullet — "should be between 5 and 20 amino acids long" read inclusively, matching the grader's `5 <= len(linker) <= 20`. Boundary coverage, not a violation.
- `linker-g-only` (pass): **the one candidate**. Under a strict composition reading of "GS linker" / "should only contain GS linkers", a poly-G (`GGGGG`) linker arguably violates the instruction; the grader's `re.fullmatch(r"[GS]+", linker)` accepts any G/S mixture. Runtime symmetry proof: an all-S (`SSSSS`) linker set also passes. The probe's label ("a G-only linker is not distinguished") half-discloses this; the knowledge entry should record it as a grader-tolerance divergence (alphabet membership vs composition), not silently.

### F4 (LOW) — `max_passing_nt=2766` recomputed and achievable
3×(8+259+158+235+182+4×20) = 3×922 = 2766 (recomputed from the pinned grader's own literal components — same parse the probe uses). Achievability verified: a GS-mixed 20-aa-junction encoding of the full 2766-nt construct passes the grader. (An all-G 20-aa-junction encoding of the same length fails GC — the bound is per-encoding, but the receipt's number is the correct structural maximum and is reachable.)

### F5 (LOW) — missing-linker edge unprobed, with a misleading grader message
A 0-aa junction (no linker between subproteins) fails with `'Linker must only contain G and S amino acids.'` (empty string fails `[GS]+`), not a length/absence message. The bullet "There should be a GS linker between every subprotein" has no case; the nearest cases (`linker-4aa`) test short, not absent.

## Instruction bullets with NO case (uncovered = 3)

1. **Antibody-binder bullet** ("doesn't need to match the sequence of a protein in /app/pdb_ids.txt … only encode the most common variant … don't repeat the protein multiple times"): no case. Aggravating: the probe's own valid baseline embeds the grader's `flag_aa = "DYKDDDDK"` (8-aa FLAG epitope) as the first subprotein — i.e., every pass case is a construct with **no actual antibody-binder protein**, which the grader accepts and the instruction arguably requires. `donor-repeated` cites this bullet but repeats donor and fails on the cap (F1).
2. **DHFR bullet** ("For DHFR you should just reuse the protein sequence found in plasmid.gb"): no case touches dhfr — no dhfr substitution mutant exists; identity is only pinned by the grader's hard-coded `dhfr_aa`.
3. **fpbase bullet** ("peak emission/excitation of the donor/acceptor match the filter cube exactly based on the data returned by the fpbase API"): no case, and structurally unprobeable offline — the grader hard-codes one donor/acceptor with comments "We have setup the environment so that this donor is the only one that matches the excitation requirement" / "…emission…". The probe's `donor-one-substitution` is the closest proxy, not a test of this bullet.

Partially covered bullets (have a case, but one-sided): pdb-identity for acceptor and molecule binder (only donor probed); "acceptor and donor … only be separated by DHFR and GS linkers" (indirect via order swap only); "only the sequence … No empty lines" (trailing blank probed; leading blank / multi-line / FASTA-header not); "remove the N terminal methionine … of any protein" (only the flag N-term is testable; the grader's own hard-coded donor keeps an internal M at `…FQGHMVSKG…`, so internal-protein Met removal is untestable by construction); cap (no clean case, F1 corollary); GC window (high side only); "GS linker between every subprotein" (0-aa junction unprobed, F5).

## Probe mechanics notes (no defect, recorded for re-pin fragility)

- `run_grader` monkeypatches `mod.Path` to redirect `/app/gblock.txt`; faithful to the current grader (it uses `Path`), but a re-pinned grader that switched to a literal `open("/app/gblock.txt")` would silently read the host path — re-verify on any re-pin.
- `components()` parses literal `*_aa = "…"` lines by prefix; safe under the SHA-256 pin (`44a05a24…`), brittle only across re-pins.
- `windows_ok` is a faithful independent re-statement of the grader's rolling 50-nt rule (initial `gblock[:50]`, then roll); the receipt's `gcwin=` column cross-checks each case.
- No tool installs were needed (uv + cached biopython 1.85 sufficed); nothing written outside the build dir and `/tmp/k35rev-*`.

## Residual risk and verification gaps

- Prediction-before-first-run is asserted in the docstring and the frozen claims, but is not provable from the artifacts alone (predictions are literals in `build_cases`; the receipt matches them now) — trust anchor is the freeze statement, not a byte I can re-derive.
- The grader-vs-instruction divergences (F1, F3 G-only, antibody-binder leniency) are grader-leniency observations; whether the TB2 task environment (pdb_ids.txt, fpbase setup) would have caught them is outside the offline probe's reach and outside this seat's scope.
- I did not re-verify the C1 counter (`round35_c1_verify.py`) or the other seats' surfaces; receipt equality was re-established here (Method 1), which is the probe-side half of V5.

VERDICT: probe-review-18-confounded-1-uncovered-3
