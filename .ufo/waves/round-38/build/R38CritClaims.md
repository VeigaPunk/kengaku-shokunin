# R38CritClaims — attack on the round-38 claims' framing (C1 calibration count, C2 class, separability, controls)

Seat: critic, round-38 wave 1. Targets: `plans/round-38-claims.md` (freeze commit `e0a37853`, first probe run
`e95cf550`), read in full; `plans/round38_c1_verify.py` (the 22 `adv` cells and the kill rule);
`plans/round38_c2_verify.py` (V1–V7); the frozen controls under `.ufo/waves/round-38/claims/`; the frozen dry
table and receipt; `plans/pkg_gate.py` at its frozen digest
`ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`; `corpus/README.md`'s coverage map;
`corpus/QUALITY.md` Q24/Q27; `SCORECARD.md:564,566`. Nothing frozen was edited; the lane was only read (I did not
even need a clone for the claims audit — the two counter runs below used a `--shared` clone in
`/fast/scratch/hyaku/kengaku-r38/R38CritClaims`, removed).

**Answer in one line.** The *axis* of C1 is calibration and survives a second audit; the *count* does not: 3 of the
22 frozen mutants (5 if Q27's Limits govern) have no advertising sentence, 2 adv cells carry a false Q24 citation,
and the source arithmetic in the same section (`13 + 1 + 6`) does not reach 22. C2's edge class is real but narrower
than claimed (one new component, not a new class); its V7 label rule is a constant on the frozen table; and C1's
"adversarial battery" guard does not survive a battery of two junk fixtures that build nothing.

---

## 1. Is C1 a calibration move? Per-mutant advertising audit (N01–N22)

Method (the round-37 `F37CritC1Axis` method, reused so the two rounds are comparable): every `adv` cell is checked
against the claim's *own* declared surface — "the gate docstring, `corpus/QUALITY.md` Q24/Q27, the SCORECARD
capability rows `package-gate` and `gate-mutation-harness`" (`plans/round-38-claims.md`, §C1 bullet 1).
Tier **C** = an advertising sentence names the property; **K** = only a SCORECARD component noun covers it (the
generous reading round 37 used); **N** = no advertising sentence exists, or the only cited text disclaims it.

| Mutant | Adv cell's own citation | Advertising sentence (≤25 words, located) | Tier |
|---|---|---|---|
| N01 P1 | "capability row: 'against a spec of pinned digests'; R37PlanNext B1" | **none** — `QUALITY.md:433-434` lists "the empty `frozen_instruments` branch of P1" among branches that "stay unclaimed" | **N** |
| N02 P3 | "Q24 'the genuine package must be accepted'" | `QUALITY.md:300-301` "the genuine package must be accepted" — but the genuine package has 22 distinct lines, not 8 (§2 D2) | K |
| N03 P4 | docstring "a quote not verbatim on its cited line" | `pkg_gate.py:12-13` "a quote not verbatim on its cited line" | C |
| N04 P4 | capability row "verbatim on its cited capture line" | `SCORECARD.md:564` "verbatim on its cited capture line" | C |
| N05 P4 | docstring "a quote not verbatim" | `SCORECARD.md:564` same phrase; "verbatim" entails case-exactness | C (weak) |
| N06 P4 | *mutant id only* (`F37XMutP4 X6`) | `SCORECARD.md:564` "on its cited capture line" (a range past the capture is not on it) | K |
| N07 P5 | *mutant id only* | `SCORECARD.md:564` "against a spec of pinned digests" + component "capture manifest" | K |
| N08 P5 | "Q24 genuine accepted; R37PlanNext B2" | **none** — the genuine `SHA256SUMS` has 0 blank lines (§2 D2), so Q24 says nothing about blank-line tolerance | **N** |
| N09 P6 | capability row "teaches cells carry >=8 distinct words" | `SCORECARD.md:564` "teaches cells carry >=8 distinct words" | C |
| N10 P6 | *mutant id only* | component "SOURCES rows" (`SCORECARD.md:564`) | K |
| N11 P7 | *mutant id only* | component "entry" only; `recheck` appears in no advertising text | K |
| N12 P7 | *mutant id only* | component "entry" only | K |
| N13 P10 | docstring "a receipt a fresh run does not reproduce" | `pkg_gate.py:13` same | C |
| N14 P10 | capability row "--rerun byte-compares the receipt" | `SCORECARD.md:564` "`--rerun` byte-compares the receipt" | C |
| N15 P10 | "Q24 genuine accepted; F37XMutP910 L2; B5" | `SCORECARD.md:564` "byte-compares" entails byte-equal ⇒ pass | C |
| N16 RUN | "**gate run_checks comment**; R37PlanNext B6" | **none** — `pkg_gate.py:298` is a code comment, not the docstring; `QUALITY.md:435` lists "`run_checks`' clause-crash handler" as unclaimed | **N** |
| N17 MAIN | docstring "exit ... 2 = usage/setup" | `pkg_gate.py:7` "2 = usage/setup"; **contradicted** by `QUALITY.md:433-434` "every … `root not a directory` setup path … stay unclaimed" | C / contested |
| N18 MAIN | docstring | `pkg_gate.py:7` "an unexpected crash never maps onto 0 or 1"; **contradicted** by `QUALITY.md:435-436` "`main`'s crash→exit-2 handler" unclaimed | C / contested |
| N19 D4 | *mutant id only* | `pkg_gate.py:9` "directional tokens … come from --spec"; `SCORECARD.md:564` "the labelled D4/D5 correction lines" | K |
| N20 D4 | *mutant id only* | same | K |
| N21 D5 | *mutant id only* | `SCORECARD.md:564` "pinned digests" | K |
| N22 D5 | *mutant id only* | `SCORECARD.md:564` "verbatim on its cited capture line" | C (weak) |

Totals: **C 9, K 10, N 3** (9 + 10 + 3 = 22). Under the stricter reading in which Q27's Limits govern N17/N18 as well,
**N = 5** and the calibration-eligible set is 17.

### D1 — the headline count is not reproducible from the declared surface (unadvertised = 3, or 5)

- **Counterexample.** `plans/round-38-claims.md` §C1 asserts "the number of frozen mutants N01–N22 (**each one
  advertised behaviour**, sentence named in its `adv` cell) that no battery fixture kills". Three cells name no
  sentence (N01, N08, N16), and for four of them the surface text the claim itself lists says the opposite:
  `corpus/QUALITY.md:433-435` "… stay unclaimed (the empty `frozen_instruments` branch of P1, every `spec not
  found` / `root not a directory` setup path, … `run_checks`' clause-crash handler, `main`'s crash→exit-2 handler
  …)". N01, N16, N17, N18 are exactly four of those six branches.
- **Impacted axis:** calibration. This is the same count defect round 37 was faulted for (6 of 55), one round later,
  in the sentence that defines the metric. The landed number (`killed=22`) is unaffected; the *claim's* number is.
- **Smallest safe correction (text only, nothing frozen):** §C1 bullet 1 → "the number of frozen mutants N01–N22
  that no battery fixture kills ATTRIBUTABLY, **17 of which** silence a behaviour the declared surface advertises
  (N01, N08, N16 silence branches Q27's Limits calls unclaimed; under Q27's reading N17 and N18 join them)";
  and the same one-sentence disclosure in the counter docstring's "Self-assessment under test" paragraph.

### D2 — two adv cells carry false provenance (both of the *mirror* mutants that need an accept-side fixture)

- N02's cell cites Q24's genuine-acceptance sentence for "exactly min_distinct_locations quote lines". Measured: the
  genuine package prints `P3 ok rows=22 distinct_quotes=22 distinct_lines=22` at `min_distinct_locations 8`
  (`measurements.txt`). The genuine package is at 22, so Q24's sentence does not cover the threshold boundary.
- N08's cell cites the same sentence for "a blank manifest line is tolerated". Measured: the genuine
  `corpus/evidence/round35/tb2-eval/SHA256SUMS` has **0** blank lines (`grep -c "^$"` → `0`). The genuine package
  never exercises the tolerance, so its acceptance says nothing about it.
- **Impacted axis:** calibration (and provenance of the claim's own citations). Two of the three mirrors — the
  part of the list the claim says "tests the false-red direction the round-37 list lacked" — rest on a citation the
  cited bytes do not support.
- **Smallest correction:** N02's cell → "the threshold is inclusive, not exclusive [`pkg_gate.py:9` 'quote bounds …
  come from --spec'; no advertising sentence names the boundary]"; N08's cell → "no advertising sentence; the
  genuine manifest has no blank line, so Q24's acceptance does not reach it".

### D3 — 9 of 22 cells cite no sentence at all

N06, N07, N10, N11, N12, N19, N20, N21, N22 cite a round-37 mutant id (`F37XMutP4 X6`, …) where the claim says a
"sentence named in its `adv` cell" will be. The seam round-37 left open (`F37CritC1Axis` §5.3: "not one row carries
a file:line") is therefore unchanged; the round-38 table adds `file:line` for 13 rows only.
**Smallest correction:** add the citation column of §1 above; rows without one are labelled "component noun only",
which is what they are.

### D4 — the source arithmetic does not reach 22

- Claim: "13 non-equivalent survivors of round-37 wave 2 …, one wave-2 diagnostic survivor …, and the shapes the
  round-37 freeze excluded or never executed (… B1, B2, B5, B6, B7, B8)". 13 + 1 + 6 = **20**.
- Measured from the frozen `MUTANTS` table: **17** distinct `F37XMut*` citations (16 extra mutants + the
  `F37XMutP7 D1` diagnostic) and 6 distinct `B` shapes, with `F37XMutP910 L2` = `B5` counted twice in N15's cell
  → 17 + 6 − 1 = **22**. The "13" should be 16 (per-seat survivor sums from the frozen wave-2 reports:
  P23 1, P4 4, P5 1, P6 2, P7 1, P910 3, D4 2, D5 2).
- **Impacted axis:** calibration — a count defect inside a calibration claim, the exact class round 37's lesson
  named. Same sentence in `plans/round38_c1_verify.py` docstring ("the 13 non-equivalent survivors").
- **Smallest correction:** "16 non-equivalent survivors of round-37 wave 2 … plus the six freeze-excluded shapes
  (B5 = `F37XMutP910 L2`, counted once)".

---

## 2. Can a do-nothing or a junk control reach C1? Do-nothing no; junk **yes** (demonstrated)

**Do-nothing:** as recorded, `killed=0 survived=22` (`claims/control-c1-nothing.txt:89`), `PREDICATE C1 fail`.
Fine.

**Junk: the guard the claim names does not cover the channel the counter opens.** `plans/round38_c1_verify.py:162-173`
imports every `plans/battery38/*.py` and `exec_module`s it **in the counter's own process**; `:240` then calls the
module's `build` there. `run_gate`, `MUTANTS` and the mutant gate files are all reachable from that module as
`sys.modules["__main__"]` globals. The token scan (`/proc`, `ppid`, `cmdline`, `psutil`, `environ`) bans none of it.

Demonstrated in a scratch clone, with a module whose entire content is two fixtures that build **no package** (an
empty directory, and a `--spec` pointing at `{}`) plus a wrapper that calls the real `run_gate` for `ref.py`/`null.py`
and drops/inserts the mutant's own clause for every `N*.py`:

```
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=20 survived=2 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

(`R38CritClaims/junk-battery-reaches-attribution.txt`; `wrong=0` and `sidechannel=0`, i.e. the predicate's two
integrity legs, are both reached.) The two survivors (N15, N16) are fixtures my two-junk set did not supply a
reference for, not a structural limit — N15 needs a reference run that prints `P10 ok`, which any `--rerun` fixture
supplies.

**D8.** The claim's limit sentence reads "the side-channel scan is a token heuristic (`/proc`, `ppid`, …), so
battery38 code review by a non-author seat remains part of admission" — as if the risk were a fixture *detecting
which gate copy runs*. The actual channel is that a fixture **is** code in the counter's process and can replace the
attribution function outright. The named mechanism is the weaker one, so the mitigation ("review") is right for the
wrong reason and can be satisfied by a scan for those five tokens.
**Smallest correction:** replace that sentence with: "battery38 modules are imported and executed inside the
counter (`round38_c1_verify.py:162-173`, `:240`); a module can rebind the counter's own helpers, so the token scan
does not constrain the strongest channel — admission requires a non-author seat to read every module for
`sys.modules` / `run_gate` / `getattr` rebinding, not only for the five tokens."

**Universal clause, minor:** the frozen predicate prints `BATTERY fixtures=<n>` with `<n>` unconstrained, so the
claim fixes the mutant denominator (22) but not the fixture denominator. Not a defect by itself; worth a sentence,
since the round-36 criterion (Q24) is the one that counts fixtures.

---

## 3. C2: is "build provenance" a new class? No — it is a fourth instance with one new executed edge

The coverage map's own headings number **task instances**, not classes: `corpus/README.md:260` "Terminal-Bench 2.0
task grader (one task)", `:261` "(second task)", `:262` "(third task, **one new executed edge class**)". The frozen
claims say "a fourth grader **class** (build provenance)" — a category slide the map's convention rejects.

Component-by-component against what the map already covers:

| C2 class component | Already covered |
|---|---|
| "the graded state is a built artefact" | `README.md:257` "deterministic state comparison — `record.csv` vs `expected_ratio.csv`" (r33); `README.md:260` gblock content (r35) |
| "a regex over program output" | `README.md:261` "exact equality of `re.findall(pattern, log_text, re.MULTILINE)`" (r36) |
| "checked by presence … directory shape" | `README.md:262` "one pytest function asserting that a helper script's stdout contains `TEST PASSED`" (r37) |
| "an `ldd` string scan" | **new** — `ldd` appears nowhere in the coverage map |

**D5.** So C2 is a fourth instance with one new executed edge (`ldd`'s `DT_NEEDED` text read), which is exactly how
round 37 described its own step. The build seat's own README bullet already says so ("A fourth instance of the same
ground", `corpus/README.md:263`), so claim and work product disagree in the direction of the claim being stronger.
**Smallest correction:** §C2 bullet 1 → "a fourth TB2 task instance with one new executed edge class (the `ldd`
`DT_NEEDED` string scan); presence, directory shape and the output regex repeat rounds 33/35/36/37". This costs
nothing on coverage and protects novelty from the same over-claim round 37 was faulted for.

---

## 4. C2's V7 rule is a constant on the frozen table — and the fix for D2 is a co-occurrence heuristic

**D6.** `plans/round38_c2_verify.py:239` builds `violating` from whole-case observed verdicts only (`obs`), and
`:242` derives the label from `set(violating.values())`. The frozen table makes that degenerate:

```
from-source      carriers=22 failing=15 passing= 7 -> V7 label=partly
no-x11           carriers= 3 failing= 2 passing= 1 -> V7 label=partly
debian-source    carriers=22 failing=15 passing= 7 -> V7 label=partly
extract-to-app   carriers=22 failing=15 passing= 7 -> V7 label=partly
install-path     carriers= 4 failing= 3 passing= 1 -> V7 label=partly
results-format   carriers= 5 failing= 4 passing= 1 -> V7 label=partly
debugger-works   carriers=22 failing=15 passing= 7 -> V7 label=partly
```

Three consequences: (i) every row must be `partly`, so V7 can only fail on a mislabelled map, never on the grader;
(ii) four tags share the identical carrier set (all 22 cases), so V7 is forced to give them *identical* labels no
matter what the grader does — it cannot separate "Debian source" from "built from source", the two things
`test_outputs.py:60-85` tests in separate functions; (iii) the receipt already carries a finer signal, the per-test
bits (`tests=PFPP`), which V7 discards.
This matters because §Frontier presents V7 as the fix for round-37 closure D2 ("a requirement-map label chosen from
one witness"). It is not that fix; it is a weaker floor that happens to be honest here. The build seat's entry
concedes it ("All seven labels are `partly`").
**Smallest correction:** §C2 counter bullet (V7) → "V7 checks that the map is the *derivation* of the receipt, not
that the grader enforces anything: on the frozen table all seven tags derive `partly`, and four tags share their
carrier set, so the map's value is its case citations, not its labels."

**D7 — the skip control does not isolate the mechanism it is cited for.** The claims say "V2's P10 fresh-run byte
compare is what makes such a receipt red". In `claims/control-c2-skip.txt` the gate block shows `P3 DEFECT`,
`P4 DEFECT`, `P6 DEFECT`, `P8 DEFECT` **and** `P10 DEFECT` — five defects, so `gate_exit=1` without P10. The same
co-occurrence class round 37's `F37CritC1Axis` §5.1 flagged. Correction: say the skip control is red at V2 with P10
one of five firing clauses, and that isolating P10 needs a package that is valid except for the receipt.

---

## 5. Separability, and one place it is not what the claims say

Read `PINS` (14 entries: gate, r36/r37 counters, r35 spec, r37 attribution audit, nine `battery37` modules) and
C2's constants (5 captures, r38 spec, gate, probe, dry table). **C1 does not read C2's work product and C2 does not
read `plans/battery38`** — the separability sentence holds at file level, and the shared gate digest is disclosed.
Two leaks that are not:

**D9.** `plans/round38_c2_verify.py:63` `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` — an
absolute fleet-root path. The frozen predicate says "measured on a clean clone of the landing tip"; V6 reads bytes
that are not in the clone and are pinned by nothing. That is round-37 closure D4's class ("`ledger-tip` red in
detached clones") reintroduced in the new counter. Correction: read the census relative to the lane, or pin its
digest in the claim's Limits and say the predicate depends on fleet-root state.

**D10.** Both predicates need an unpinned external: the gate's P10 shells out to `uv run --with biopython==1.85`
when `import Bio` fails (`plans/pkg_gate.py:262-266`), and `Bio` is not installed on this host (`ModuleNotFoundError`);
C1's P10 mutants and C2's V2 both depend on that. It worked here (the control receipts show P10 running), but no
claim sentence names the dependency or the cache state it rests on.

---

## 6. What I am not claiming

- The C1 axis is calibration and it survives: 19 of 22 mutants map to an advertising sentence under the generous
  component reading, the do-nothing control is red, and the landed `killed=22` would close 19 genuine mismatches
  (17 under the Q27 reading) plus 3–5 branch-coverage items.
- I did not run the frozen C1/C2 predicates on the landing tip, did not open the wave-2 mutation seats' work, and
  did not re-measure the 22 probe cases beyond reading the frozen receipt; the grader observations in the receipt
  are not re-verified by this seat.
- Q27's supersession of Q24 is unchanged by anything above; the defect is in the *count*, not the criterion.

## Evidence (commands this seat ran)

- `python3` over the frozen dry table (script in `R38CritClaims/measurements.txt`) → per-tag carriers/failing/passing
  and `-> V7 label=partly` for all 7 tags.
- `python3 lane/plans/pkg_gate.py package --root <genuine r35 pkg> --spec lane/plans/pkg-spec-r35.json` →
  `P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0`; `P5 ok manifest_entries=6 bad=0`.
- `grep -c "^$" corpus/evidence/round35/tb2-eval/SHA256SUMS` → `0`; `min_quotes 8 min_distinct_locations 8
  min_teaches_words 8` from `plans/pkg-spec-r35.json`.
- `python3 lane/plans/round38_c1_verify.py --lane <clone> --battery-dir <junk> --work <scratch>` → `BATTERY
  fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=20 survived=2` (receipt:
  `R38CritClaims/junk-battery-reaches-attribution.txt`).
- `grep -n` on `plans/round38_c1_verify.py` → `load` at :155, `battery38_fixtures` at :162, exec at :172, `build`
  call at :240; `MUTANTS` block → 17 distinct `F37XMut*` citations, 6 `B` shapes.
- `grep -c`/`sha256sum` → `PINS` 14 entries; `plans/pkg_gate.py` =
  `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`.
- Lane read at `fc1174f5` + wave-1 working tree; scratch clone `/fast/scratch/hyaku/kengaku-r38/R38CritClaims`
  created with `git clone -q --shared`, verified with `git -C … rev-parse --show-toplevel`, removed at exit
  (`SCRATCH_REMOVED`). No tool installed, no lane file, index or jj state touched.

VERDICT: claims-attack-10-defects-unadvertised-3
