# F35GOnlyLinker — round-35 wave-2 falsify report (findings 1 & 3)

Seat: `F35GOnlyLinker` (executor, leaf). Target: falsify entry findings 1 (a G-only linker
passes) and 3 (a one-residue subprotein error fails with the order message) by re-running those
cases with fresh content — different codon choices, different substituted positions, substitution
in acceptor/snap instead of donor — through the probe's `run_grader` under
`uv run --no-project --with biopython==1.85`.

## Method

- All runs execute the **pinned grader bytes** `corpus/evidence/round35/tb2-eval/test_outputs.py`
  (SHA-256 `44a05a24…a096582`, matches the probe's pinned digest) through the probe's own
  functions — `components`, `fusion`, `back_translate`, `windows_ok`, `run_grader` — loaded via
  `importlib` from `plans/tb2_grader_probe.py`, so grader path, digest guard and tempfile dance are
  byte-identical to the committed probe.
- **Instrument baseline:** a fresh run of the committed probe reproduces the committed receipt
  byte-for-byte:

  ```
  $ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
  $ uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .
  … (full 21-line output saved at .ufo/waves/round-35/falsify/F35GOnlyLinker/baseline-rerun.txt)
  cases=18 observed_pass=5 observed_fail=13 mismatches=0
  $ cmp corpus/evidence/round35/tb2-grader-probe.txt \
        .ufo/waves/round-35/falsify/F35GOnlyLinker/baseline-rerun.txt && echo BYTE-IDENTICAL
  BYTE-IDENTICAL
  ```

- **Fresh content** (`harness2.py`, run with the same `uv` command; full output in
  `.ufo/waves/round-35/falsify/F35GOnlyLinker/battery2.txt`):
  - *Different codon choices:* every case run twice — `balanced` (probe's deterministic greedy)
    and `variant`, a seeded random tie-break among equal-score codons chosen so the whole construct
    still passes every 50-nt GC window. Variants differ from `balanced` at 271–320 of 862–890
    residues (≈31–36% of codons re-coded); each variant's translate() is asserted equal to the
    intended amino-acid sequence.
  - *Finding 1:* G-only linkers in **all four** gaps, at length 5 (`GGGGG`), length 20 (`G`×20),
    and mixed lengths 5/9/14/20; first-gap 20-mer included as the exact-length analogue of the
    entry's case.
  - *Finding 3:* one-residue substitutions moved to new positions (donor 1/130/258, acceptor
    0/120/234, snap 0/30/181, dhfr 0/90/157) plus the entry's donor 10, and — beyond the asked
    donor/acceptor/snap — the first subprotein (antibody-binder literal `flag_aa`, DYKDDDDK),
    positions 0/4/7.

## Finding 1 — a G-only linker passes: CONFIRMED (with one GC-boundary caveat)

Observed (verbatim from `battery2.txt`):

```
== finding 1: G-only linkers ==
case=f1-all4-gonly5 enc=balanced observed=pass assertion='-' nt=2586 gcwin=ok
  [f1-all4-gonly5 variant seed=1 codon_diff_vs_balanced=286 (286/862 residues differently encoded)]
case=f1-all4-gonly5 enc=variant observed=pass assertion='-' nt=2586 gcwin=ok
case=f1-gonly20-first enc=balanced observed=pass assertion='-' nt=2631 gcwin=ok
  [f1-gonly20-first variant seed=1 codon_diff_vs_balanced=314 (314/877 residues differently encoded)]
case=f1-gonly20-first enc=variant observed=pass assertion='-' nt=2631 gcwin=ok
case=f1-gonly20-all4 enc=balanced observed=fail assertion='GC content must be between 30 and 70% in all 50 nucleotide windows.' nt=2766 gcwin=violated
  [f1-gonly20-all4 variant: NO window-safe seed found in 3000 attempts]
case=f1-gonly-mixed enc=balanced observed=pass assertion='-' nt=2670 gcwin=ok
  [f1-gonly-mixed variant seed=1 codon_diff_vs_balanced=292 (292/890 residues differently encoded)]
case=f1-gonly-mixed enc=variant observed=pass assertion='-' nt=2670 gcwin=ok
```

- G-only linkers pass at every length 5–20, in every gap, and under both codon encodings; the
  linker alphabet/length assertions never fire. The claim's mechanism (`[GS]+` admits `GGGGG`) is
  confirmed.
- **Caveat (boundary, does not refute):** with *all four* linkers at the 20-residue max
  (`f1-gonly20-all4`, 2766 nt) the construct fails the **GC window** assertion — the linker check
  is still never reached. No window-safe re-encoding exists among 3000 deterministic variant seeds,
  so this is a property of the amino-acid sequence (four G-runs), not of the encoding. The entry's
  "a solution with G-only linkers scores 1" therefore holds exactly when the construct also
  satisfies the other bullets (GC included); the strong reading "any G-only-linker construction
  scores 1" is overbroad.

## Finding 3 — a one-residue subprotein error fails with the order message: REFUTED (first subprotein)

Observed (verbatim from `battery2.txt`; all rows `gcwin=ok`):

```
== finding 3: one-residue subprotein errors ==
case=f3-donor-pos10 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-donor-pos10 variant seed=1 codon_diff_vs_balanced=295 (295/862 residues differently encoded)]
case=f3-donor-pos10 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-donor-pos1 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-donor-pos1 variant seed=1 codon_diff_vs_balanced=291 (291/862 residues differently encoded)]
case=f3-donor-pos1 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-donor-pos130 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-donor-pos130 variant seed=1 codon_diff_vs_balanced=312 (312/862 residues differently encoded)]
case=f3-donor-pos130 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-donor-pos258 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-donor-pos258 variant seed=1 codon_diff_vs_balanced=285 (285/862 residues differently encoded)]
case=f3-donor-pos258 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-acceptor-pos0 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-acceptor-pos0 variant seed=1 codon_diff_vs_balanced=320 (320/862 residues differently encoded)]
case=f3-acceptor-pos0 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-acceptor-pos120 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-acceptor-pos120 variant seed=1 codon_diff_vs_balanced=293 (293/862 residues differently encoded)]
case=f3-acceptor-pos120 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-acceptor-pos234 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-acceptor-pos234 variant seed=1 codon_diff_vs_balanced=289 (289/862 residues differently encoded)]
case=f3-acceptor-pos234 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-snap-pos0 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-snap-pos0 variant seed=1 codon_diff_vs_balanced=312 (312/862 residues differently encoded)]
case=f3-snap-pos0 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-snap-pos30 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-snap-pos30 variant seed=1 codon_diff_vs_balanced=302 (302/862 residues differently encoded)]
case=f3-snap-pos30 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-snap-pos181 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-snap-pos181 variant seed=1 codon_diff_vs_balanced=312 (312/862 residues differently encoded)]
case=f3-snap-pos181 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-dhfr-pos0 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-dhfr-pos0 variant seed=1 codon_diff_vs_balanced=287 (287/862 residues differently encoded)]
case=f3-dhfr-pos0 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-dhfr-pos90 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-dhfr-pos90 variant seed=1 codon_diff_vs_balanced=301 (301/862 residues differently encoded)]
case=f3-dhfr-pos90 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-dhfr-pos157 enc=balanced observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
  [f3-dhfr-pos157 variant seed=1 codon_diff_vs_balanced=303 (303/862 residues differently encoded)]
case=f3-dhfr-pos157 enc=variant observed=fail assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' nt=2586 gcwin=ok
case=f3-flag-pos0 enc=balanced observed=fail assertion='Start of gBlock must match flag protein.' nt=2586 gcwin=ok
  [f3-flag-pos0 variant seed=1 codon_diff_vs_balanced=277 (277/862 residues differently encoded)]
case=f3-flag-pos0 enc=variant observed=fail assertion='Start of gBlock must match flag protein.' nt=2586 gcwin=ok
case=f3-flag-pos4 enc=balanced observed=fail assertion='Start of gBlock must match flag protein.' nt=2586 gcwin=ok
  [f3-flag-pos4 variant seed=1 codon_diff_vs_balanced=271 (271/862 residues differently encoded)]
case=f3-flag-pos4 enc=variant observed=fail assertion='Start of gBlock must match flag protein.' nt=2586 gcwin=ok
case=f3-flag-pos7 enc=balanced observed=fail assertion='Start of gBlock must match flag protein.' nt=2586 gcwin=ok
  [f3-flag-pos7 variant seed=1 codon_diff_vs_balanced=284 (284/862 residues differently encoded)]
case=f3-flag-pos7 enc=variant observed=fail assertion='Start of gBlock must match flag protein.' nt=2586 gcwin=ok
SUMMARY f1_total=7 f1_pass=6 f1_fail=1
SUMMARY f3_total=32 f3_order_message=26 f3_flag_message=6 f3_other=0
SUMMARY gcwin_violated=1 (f1-gonly20-all4)
```

- **Confirmed for donor/acceptor/snap/DHFR:** all 26 rows (positions 0/1/10/30/90/120/130/157/
  181/234/258/last, both encodings) fail with the exact order message
  `Fusion protein must be in the order flag - donor - dhfr - acceptor - snap`. Different
  positions, acceptor/snap instead of donor, and different codon choices do not change it.
- **Refuted for the first subprotein:** all 6 rows substituting one residue of the antibody-binder
  literal (`flag_aa = "DYKDDDDK"`, `test_outputs.py:28` — the first subprotein of the required
  order, `instruction.md:33`) fail with **`Start of gBlock must match flag protein.`**, not the
  order message. Mechanism (confirmed by source + index trace, `debug_idx.py` under the same `uv`
  env; grader lines per the entry's own quote table):

  ```
  case=flag-pos4
    indices flag=-1 donor=13 dhfr=277 acceptor=440 snap=680
    order_assertion_passes=True
    next_assertion_flag_idx_eq_0 -> False
    message_if_not = 'Start of gBlock must match flag protein.'
  case=donor-pos130
    indices flag=0 donor=-1 dhfr=277 acceptor=440 snap=680
    order_assertion_passes=False
    message = 'Fusion protein must be in the order flag - donor - dhfr - acceptor - snap'
  ```

  With `flag_idx = -1`, the chained `assert flag_idx < donor_idx < …` (`test_outputs.py:42`)
  evaluates `-1 < donor_idx` true, so the order assertion **passes**; the next assertion
  `assert flag_idx == 0` (`test_outputs.py:46`) then fails with the start message. So the
  finding's generalization "A one-residue error in a subprotein fails with the *order* message,
  because `find` returns −1" is false for the first subprotein — `find` returning −1 only maps to
  the order message when the missing literal is not the first in the chain.

## Files changed (all scratch, inside the allowed falsify dir)

- `.ufo/waves/round-35/falsify/F35GOnlyLinker/harness.py` (first attempt; naive alternate codon
  encodings — skipped due to GC-window confounds, kept as evidence of iteration)
- `.ufo/waves/round-35/falsify/F35GOnlyLinker/harness2.py` (window-safe battery; the evidence
  source)
- `.ufo/waves/round-35/falsify/F35GOnlyLinker/debug_idx.py` (index/mechanism trace)
- `.ufo/waves/round-35/falsify/F35GOnlyLinker/battery.txt`, `battery2.txt`, `baseline-rerun.txt`
  (output captures)

No lane files were modified; no git/jj operations ran; no tools were installed (uv 0.13.0 was
already present at `~/.local/bin/uv`).

## Risks / notes

- The 18-case probe never exercised a *mutation* of the antibody-binder literal (wave-1 review
  `R35RevProbePred` noted only that no *variant or repeat* of it was probed); this falsify run
  adds it and shows that corner breaks the entry's finding-3 wording. The binary reward (fail) is
  unaffected — the entry's central "reward unaffected" claim holds in every row.
- Finding 1's "scores 1" sentence is best read as conditional on the other bullets (GC), which the
  entry itself states ("A solution with G-only linkers scores 1" in the context of the executed
  table). The `f1-gonly20-all4` boundary is reported as a caveat, not a refutation.
- C1/C2 counters were not run; this seat's scope is the two findings.

VERDICT: findings13-refuted
