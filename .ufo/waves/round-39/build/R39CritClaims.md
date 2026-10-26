# R39CritClaims — attack on the round-39 claims' framing

Seat: critic, round-39 wave 1. Targets read in full: `plans/round-39-claims.md` (freeze `088f7c3`, first run
`6a1eb5e`); `plans/round39_c1_verify.py` (7 `adv` cells); `plans/round39_c2_verify.py` (V1–V7); the frozen
controls under `.ufo/waves/round-39/claims/`; the frozen dry table and receipt; `plans/pkg_gate.py` at
`ea638822…dd41`; `corpus/QUALITY.md` Q1/Q21/Q24/Q27/Q29; `SCORECARD.md:564`; `corpus/README.md`'s coverage
map; the round-38 wave-2 falsify reports the C1 list is built from. Nothing frozen was edited. All runs used one
`git clone -q --shared` of lane tip `7504738` in `/fast/scratch/hyaku/kengaku-r39/R39CritClaims` (verified
`rev-parse --show-toplevel` = that path), receipts copied to `build/R39CritClaims/`, scratch deleted.

**Answer in one line.** The C1 *axis* survives (it is calibration by Q27's own definition) but its *count* does
not: 3 of the 7 `adv` cells cite no sentence that reaches their behaviour (M01, M04, M07 — independently
corroborated by R39AdvErrata) and 5 of 7 are not direct, not the 3 the claims mark; C1 is round-38's unadmitted C1 finished, with a delta of four fixtures whose
shapes round 38 had already specified; C2's class is new to the coverage map but not a new finding; and the
separability paragraph is false in both directions (demonstrated below), while Q29's named executable cannot load
the round-39 counter at all.

---

## 1. Is C1 a calibration move? Per-mutant advertising audit (M01–M07)

Axis test first, because it is the question the seat exists to answer. AXES.md:15 defines calibration as
"Self-assessment quality: gaps named honestly, confidence graded, overreach caught", and Q27 makes exactly this
claim ("a gate's advertised defect class counts as held only when a single-defect fixture kills that class's
silence mutant; a class whose mutant no fixture kills is advertised debt", `corpus/QUALITY.md:409-411`). Rounds 37
and 38 filed the same instrument on the same axis. **Verdict: the axis label is correct.**

The method is the one R38CritClaims §1 used, so the two rounds are comparable. Tiers: **C** = an advertising
sentence states the property; **K** = only a component noun or a general class sentence covers it; **N** = no
sentence on the declared surface covers it, or the cited bytes do not reach it. Declared surface = gate docstring,
Q24/Q27, SCORECARD capability row `package-gate` (`plans/round-39-claims.md:21-23`).

| M | behaviour silenced by the mutant | advertising sentence (located) | tier | cell |
|---|---|---|---|---|
| M01 D5 mirror | a D5 capture pinned on a non-first manifest row is accepted | cell cites `QUALITY.md:300` "the genuine package must be accepted" — unreachable: the genuine `quarantine-SHA256SUMS` has two rows and row 1 *is* the capture digest (`b60af775…`), so `[:1]` is a no-op on the accepted state. A covering class sentence does exist at `SCORECARD.md:564` ("the labelled D4/D5 correction lines against a spec of pinned digests") but the cell does not name it | **N** (as cited) | marked indirect ✓ but citation unreachable ✗ |
| M02 P1 silence | every pinned instrument is checked, not only the first | `SCORECARD.md:564` "(entry, capture manifest, SOURCES rows, receipt, frozen instruments, clean tree)" — plural noun; the sentence actually quoted, "a stub probe dies on its digest pin", is singular | K | **unmarked** ✗ |
| M03 P3 silence | a quote one word above the spec's upper word bound is a DEFECT | `plans/pkg_gate.py:9-10` "Every clause is spec-driven: paths, digests, … quote bounds … come from --spec" — a provenance sentence; the docstring's defect enumeration (`:12-13`) omits word bounds, and Q24's one-word example (`QUALITY.md:305`) is the *lower* bound | K | **unmarked** ✗ |
| M04 P7 silence | the entry carries exactly one `source:` line per row | none. `SCORECARD.md:564` "SOURCES rows" names the registry that P6 reads (`pkg_gate.py:184-209`); the mutation is in `c_provenance` (`pkg_gate.py:211-232`), which reads the entry's `source:` lines. Q1 (`QUALITY.md:15-18`) describes the entry's opening triad and allows "row id(s)", not one line per row | **N** | marked indirect, but the artefact is misnamed ("a registry row carries exactly one source line") ✗ |
| M05 RUN rc-silence | a package with a DEFECT clause exits 1 | `plans/pkg_gate.py:7` "exit 0 = accept, 1 = reject, 2 = usage/setup"; `SCORECARD.md:564` "Exit 0 accept / 1 reject / 2 setup" | C | unmarked ✓ |
| M06 MAIN rc-mirror | the genuine package exits 0 | `plans/pkg_gate.py:7`; `QUALITY.md:300` "the genuine package must be accepted" | C | unmarked ✓ |
| M07 D5 mirror | a D5 quote is found where its span carries markup | none. `QUALITY.md:300` does not reach it: the genuine D5 capture's quote is contiguous in the **raw** bytes — measured, see §6 — so the strip is never exercised by the accepted state. General D4/D5-accept clause (`SCORECARD.md:564`) covers acceptance of a labelled line, not tag tolerance | **N** | marked indirect, citation unsupported (the round-38 D2 pattern) ✗ |

**Measured: C 2, K 2, N 3** — against the claims' "Three of the seven `adv` cells cover their behaviour only
indirectly (marked in the cell)" (`plans/round-39-claims.md:62`). Five are not direct: the three marked cells
(M01, M04, M07) are *uncitable as cited*, and two genuinely indirect cells (M02, M03) carry no marker. The
marker therefore names the wrong tier and is missing where it belongs. The two direct cells are exactly the two
the freeze's new exit-code legs retro-fit.

One point in the claims' favour, checked because round 38 lost it: none of the seven collides with Q27's
"stay unclaimed" list (`QUALITY.md:436-440`: the empty `frozen_instruments` branch of P1, the setup paths, P10's
OSError arm, `run_checks`' crash handler, `main`'s crash handler, the option gating). M02 mutates the
*multi-instrument* lookup, M05 the defect count, M06 the accept branch — none is a listed exclusion.

## 2. Is 3-of-7-already-killed a soft target?

Reproduced, not inferred: on a clean clone the control state is `MUTANTS total=7 killed=3 survived=4 invalid=0
null_detected=0` (`build/R39CritClaims/receipt-c1-full.txt`), matching `claims/control-c1-nothing.txt` line for
line (M01 by `d5m-n21-manifest-row-2`, M05 by `p23-p2-receipt-deleted`, M06 by `r36-P0`).

Yes, in three specific senses — all of them disclosed, none of them false:

1. **43% of the list is already held.** Round 37's freeze read `killed=5/55`, round 38's `killed=0/22`; this one
   reads `killed=3/7`. The before-state is the strongest of the three.
2. **Two of the three pre-kills are rule credits, not fixture credits.** M05 and M06 die only because the freeze
   added the two exit-code legs (`rc-silence`, `rc-mirror`); no new fixture was written for them. The fixture work
   is exactly the four survivors the claims name.
3. **The four remaining shapes were specified last round.** `F38XMutP.md:96-107` ends each survivor with a
   "Round-39 candidate" line (corrupt a non-first pinned instrument; a quote above the upper word bound; a
   duplicated `source:` line) and `F38XMutRerunMain.md` finding 4 gives the fourth (a capture with markup inside
   the quote span). C1 therefore *executes* round-38's discovery; it does not discover.

The predicate itself is not soft: `killed=7/7` with `wrong=0`, `invalid=0`, `null_detected=0` is full-strength,
and the honest stop from round 38 was the right precedent. The framing that overreaches is the title sentence
"the gate behaviours still undemonstrated after round 38": the seven are the union of three prior survivor lists,
not an enumeration of advertised behaviours, so the calibration count is `4 at freeze` for *these* seven, not a
census. Smallest correction: "the survivors of round-38's two extra-mutant sweeps and its one mislabelled mutant
(an unknown lower bound on the gate's advertised-but-undemonstrated behaviours)".

## 3. Is C2's class new against the coverage map?

Yes for the mechanism, no for the finding class — and the claims say the second part themselves.

- The coverage map (`corpus/README.md:260-263`) carries four TB2 bullets: protein-assembly (one task),
  regex-log (second, pattern-valued), git-webserver (third, "one new executed edge class"), build-pmars (fourth,
  "build-provenance class"). None of the four grades git history: `knowledge/tb2-git-webserver-grader.md:149`
  records that "the graded state need not come from a repository, a hook or a push", and no knowledge entry
  mentions `reflog`, `fsck` or a dangling object as a graded surface (`grep -rn "reflog\|fsck\|dangling"
  corpus/knowledge/*.md` → no hit on a graded-state claim). "Repository-history state" is therefore a new
  mechanism on the map.
- The *finding* is not new: round 38's build-pmars entry already established "a canned C program with an empty
  `debian/` directory and a zero-byte `src/dummy.c` passes all four" (`corpus/README.md:263`). C2's headline
  ("the untouched initial repo fails only the flag test; `echo-only` passes 5/5") is a second instance of
  do-nothing-passes, which `plans/round-39-claims.md:86-88` concedes ("published TB validation practice … the
  entry claims a probed instance only").
- Scale is honest: 5 of 89 tasks, "not breadth", stated in the bullet C2 will write.

No defect here. The one wording risk: "a fifth grader class" in the C2 heading versus the map's convention of
counting tasks and calling the mechanism a class — the two prior rounds used the same word for the same thing, so
this is consistent, not an overclaim.

## 4. Separability — the sentence is false as written (demonstrated both ways)

Claim: "C1 reads only the gate, the round-35 spec, the round-36/37 counters, batteries 37/38 and
`plans/battery39`; C2 reads only its captures, spec, probe, receipt, entry, SOURCES and README. Neither counter
reads the other's work product: C1 can pass with C2 absent and vice versa" (`plans/round-39-claims.md:92-94`).

Mechanism, from frozen code: every C1 fixture package is a **mirror of the live lane corpus**.
`plans/round36_c1_verify.py:55-68` (`copy_package`, called by `Ctx.genuine_package`) copies the spec's entry,
receipt, `corpus/SOURCES.md`, `corpus/README.md`, then every `corpus/knowledge/*.md` and `corpus/lessons/*.md`.
The gate's P8 then requires the copied knowledge files to equal the copied README's index rows
(`plans/pkg_gate.py:233-252`). C2's work product is precisely a new knowledge file plus its index row, bullet,
SOURCES rows and README/PROVINCE edits. Conversely C2's V2 runs the gate with `--require-clean-tree` against the
**lane root** (`plans/round39_c2_verify.py:116-127`), so any untracked file anywhere in the lane — including
C1's `plans/battery39/*.py` while a wave-1 executor is still building — is P9's input.

Counterexample 1 (C2 file reds C1): clone + `corpus/knowledge/zz-coupling-probe.md` (one file, no index row) →
`python3 plans/round39_c1_verify.py --lane . --only M01` prints `BATTERY fixtures=86 wrong=51
renamed_disagree=0 sidechannel=0`, with `FIXTURE r36-P0 expect=accept declared=- observed_rc=1
observed_defects=P8 WRONG` at the head of 51 `WRONG` lines
(`build/R39CritClaims/receipt-c1-knowledge-coupling.txt`).

Counterexample 2 (C1 file reds C2): clone + `plans/battery39/zz-probe.py` (untracked) →
`python3 plans/round39_c2_verify.py --lane .` prints `gate: P9 DEFECT untracked=1
first=plans/battery39/zz-probe.py`, `V2 DEFECT` (`build/R39CritClaims/receipt-c2-untracked-coupling.txt`).

Impacted axis: calibration (a separability claim that does not hold is the "overreach caught" the axis names) and
operability (the landing order). This does **not** break either predicate: both are measured on a clean clone of
the landing tip, where C2's entry, index row and bullet land together and every battery39 module is committed.
The consequence the integrator must hold: **C2's corpus edits and C1's battery39 modules must land in the same
commit (or C2's README index row must precede/never trail its knowledge file), or C1's `wrong=0` leg reds at any
intermediate tip.**

A third direction of the same class, outside the C1↔C2 pair: C2's V6 runs a script **outside the lane and outside
any clone** — `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` (`plans/round39_c2_verify.py:65`)
against `<lane>/corpus/SOURCES.md`. So "measured on a clean clone of the landing tip" silently also requires the
fleet-root tree on the host; the predicate cannot be reproduced from the lane bytes alone. (R39AdvErrata item 10
reaches the same node from the coverage side; `-rwxr-xr-x … 35466` at that path, so it resolves here.)

A fourth direction, which can move C1's own predicate: `c_rerun` falls back to `uv run --no-project --with
biopython==1.85` (`plans/pkg_gate.py:276`), and battery38's two `--rerun` fixtures (`plans/battery38/p10a.py:51`,
`p10b.py:47`) therefore need a warm `uv` cache or network. Measured in round 38 by the sentinel seat, not by me and
not by R39AdvErrata: `.ufo/waves/round-38/falsify/F38SentinelBattery/c1-offline.out` reads `BATTERY fixtures=86
wrong=1 renamed_disagree=0 sidechannel=0` and `MUTANTS total=22 killed=18 survived=4 invalid=0 null_detected=0`,
`c2-offline.out` reads `checks=7 defects=1`. That receipt is on the round-38 counter (22 mutants); the round-39
counter loads the same pinned `p10a`/`p10b` modules (`PINS`, `round39_c1_verify.py:90-91`), so its `wrong` leg
carries the same dependency, while the byte-level half (the two fixtures passing `--rerun`, the `uv` fallback) is
code-verified only.

Smallest safe correction (text only; both counters are frozen/pinned): replace the sentence with
"On a clean clone of the landing tip C1 and C2 pass independently; inside a shared worktree they are coupled —
C1's fixtures mirror the lane's live `SOURCES.md`/`README.md`/`knowledge/`/`lessons/` bytes
(`round36_c1_verify.py:55-68`), and C2's V2 reads the whole tree through P9 — so C2's entry and its README index
row must land in one commit".

## 5. Universal clauses are demonstrated at index 1 only

M02 and M04 are universal over small collections: `frozen_instruments` has three entries in spec order
(`plans/tb2_grader_probe.py`, `plans/round35_c1_verify.py`, `plans/defect_ledger.py`) and `rows` has S105–S107.
The witness for M02 corrupts the **second** instrument (`F38XMutP.md:100-103`, W-X01) and the witness for M04
appends a duplicate `source:` for **S106** (`:105-107`). A single fixture at index 1 leaves a
first-two-only mutant (`pins.items()[:2]`, `prov` compared for the first two rows) alive on this spec. One
fixture at the **last** index kills every prefix mutant at once and costs the same.

Bound, not a defect — Q27's own limit says "demonstration is observational … never that the check is the right
check". Smallest correction: wave-1 executors target the last pinned instrument / the last spec row (S107) in the
M02 and M04 fixtures; nothing frozen changes.

## 6. Numbers: what reproduces, what does not

Everything I re-ran reproduced. Commands and outputs:

| claim | command | observed |
|---|---|---|
| `PINS total=26 mismatched=0` | `python3 plans/round39_c1_verify.py --lane . --work $TMPDIR/w` (clean clone) | identical; 26 keys counted in `PINS` (`round39_c1_verify.py:71-98`: 1 gate + 2 counters + spec + audit + 9 battery37 + 12 battery38) |
| `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0` | same | identical |
| `MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0` | same | identical (`receipt-c1-full.txt`) |
| `control-c1-gate-edited`: one appended gate line → `mismatched=1`, `invalid=7` | read `claims/control-c1-gate-edited.txt` | `PINS mismatched=1` … `MUTANTS total=7 killed=0 survived=0 invalid=7` |
| `control-c1-hostile-inproc`: `killed=3 survived=4` unchanged | read `claims/control-c1-hostile-inproc.txt` | identical |
| round-38 no-harm `killed=21 survived=1` | `python3 plans/round38_c1_verify.py --lane .` | `MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0` |
| round-37 no-harm `PREDICATE C1 pass` | `python3 plans/round37_c1_verify.py --lane .` | `MUTANTS total=55 killed=55 survived=0`, `PREDICATE C1 pass` |
| C2 control `checks=7 defects=4` (V2,V3,V4,V7) | `python3 plans/round39_c2_verify.py --lane .` | identical |
| dry table 25/13/12; receipt 25/13/12/mismatches=0 | read both files | identical |
| gate / probe / dry-table digests | `sha256sum plans/pkg_gate.py plans/git_leak_probe.py corpus/evidence/round39/git-leak-dry-cases-freeze.txt` | `ea638822…`, `4961a50f…`, `e92a5d6d…` |
| "eight predictions copy the round-38 pilot" | `grep -o "pilot [A-H]" corpus/evidence/round39/git-leak-dry-cases-freeze.txt \| sort \| uniq -c` | 8, letters A–H once each |
| "no check added or relaxed" (C2 = round-38's V1–V7) | `difflib` hunk enumeration of the two counters | 11 changed hunks, all docstring / digest / filename / temp-prefix literals; `def v1…v7` bodies byte-identical |
| M07 has no advertised reach | `python3 -c` over the genuine D5 capture: quote ∪ raw vs ∪ tag-stripped | `quote contiguous in raw: True`; `after tag strip: True` — the strip never changes the accepted state |
| freeze → first-run order | `git cat-file -t 088f7c3 / 6a1eb5e`; `rev-parse 088f7c3^` | both `commit`; `088f7c3^ = ef2fba0`, parent of `6a1eb5e` |

Two tokens do **not** reproduce, because no bytes support them:

- `stagecheck cases=25 failed=0` (`plans/round-39-claims.md:10`) — the number is the whole order-of-operations
  evidence, and there is no receipt for it anywhere in `claims/` (the only other in-tree copy is a wave-1 seat's
  draft prose, `build/R39PkgProse/province-round39.md:37`). The *ordering* it defends is independently verifiable
  by ancestry (row above); the number is not.
- "S117 … S118 …, opened 2026-10-26 03:27 -03 by the L1" (`plans/round-39-claims.md:68-70`) — `corpus/SOURCES.md`
  stops at S116 (`:129-131`), so the rows are future work (consistent with P6 reading `S117: rows=0` in the
  control), and the fetch timestamp has no witness.

Minor: "Baseline lane tip `b2bdd42`" — `b2bdd42` is the round-38 spot-check commit and the *grandparent* of the
freeze (`088f7c3^ = ef2fba0`, the round-38 wave-2 commit). Accurate as "where the round started", imprecise as
"tip".

## 7. Q29's named instrument cannot load this list

Q29 (`corpus/QUALITY.md:501-517`) makes one check load-bearing: "`python3 plans/mutant_direction_check.py --lane
.` prints one `DIR …` line per frozen mutant … Rule: a round that freezes a mutant list states, per mutant,
whether the replacement makes its clause laxer or stricter, and runs the check at its first battery integration".
Round-39 closure item R2 repeats it: "state each direction laxer/stricter at freeze (Q29)"
(`corpus/lessons/round-38-verifier-spotcheck.md:157-161`).

Measured: `python3 plans/mutant_direction_check.py --lane . --counter plans/round39_c1_verify.py` →
`AttributeError: module 'kengaku_counter' has no attribute 'battery38_fixtures'` (line 52), exit 1
(`build/R39CritClaims/receipt-direction-check-r39.txt`). Two independent breaks: the round-39 counter renamed
that function to `module_fixtures` (`round39_c1_verify.py:186`), and the checker unpacks 6-tuples
(`mutant_direction_check.py:66`) while round-39's `MUTANTS` are 7-tuples (the `witness` cell was inserted). With
no `--counter`, the checker still certifies the round-38 list only.

The redundancy Q29 wants is present, in a different place: the counter's own survivor line prints the directions a
fixture actually exhibits. Demonstrated in scratch by flipping M01's cell to `silence` in a **copy** of the counter
(frozen file untouched): `MUTANT M01 D5 silence SURVIVED exhibits=mirror,rc-mirror`
(`build/R39CritClaims/receipt-exhibits-leg.txt`). So the obligation is satisfiable — but not by the executable Q29
names, which is what a wave-2 seat will reach for.

Smallest safe correction: either state in §C1 that the Q29 check for this list *is* the counter's
`exhibits=` line (already asserted at `plans/round39_c1_verify.py:32-34` but never tied to Q29's Check), or teach
`plans/mutant_direction_check.py` the 7-tuple and the `module_fixtures` name — that file is not frozen and not in
C1's `PINS`.

A routed fix exists and I checked it rather than taking it on report: `R39DirCheckLeg`'s copy
(`.ufo/waves/round-39/build/R39DirCheckLeg/mutant_direction_check.py`, sha256 `e471630a…`) fails closed —
`--counter plans/round39_c1_verify.py` prints one `SETUP counter … missing=battery38_fixtures,attributed
non_6_tuple_rows=7` line and exits 2, rc measured directly (`rc=2`, no traceback). It does not read the round-39
list, and that seat's reason holds on my evidence: the counter's `exhibits=` leg is the redundancy Q29 wants. So
D4's correction is "adopt the fail-closed copy, or land the adapter", and the L1 no longer has to derive it.

---

## 8. Defects

**D1 — the indirect-cell count and the marker are both wrong (3 claimed; 5 not direct, of which 3 uncitable).**
Counterexample: the three cells marked `indirect` (M01, M04, M07) are exactly the three whose citation cannot
reach the behaviour, while the two genuinely indirect cells (M02's plural component noun "frozen instruments",
M03's provenance clause "quote bounds … come from --spec" — the same `K` tier R38CritClaims assigned to those
phrases) are unmarked.
Evidence: §1 table; `plans/round-39-claims.md:62`; `SCORECARD.md:564`; `pkg_gate.py:9-13`.
Impacted axis: calibration — a count defect inside a calibration claim, the class rounds 37 and 38 were each
faulted for.
Smallest correction: "Two of the seven `adv` cells are direct (M05, M06); two more are indirect and unmarked
(M02, M03, component-noun or provenance citations); three cite no sentence that reaches the behaviour (M01, M04,
M07)".

**D2 — three cells cite no sentence that reaches their behaviour, and one names the wrong artefact.** M01 cites
`QUALITY.md:300`; the genuine manifest's row 1 is the capture digest, so the accepted state exercises the
non-first-row lookup never. M04's mutated half ("exactly one `source:` line") appears in no advertising sentence,
and the cell's "a registry row carries exactly one source line" points at P6's SOURCES registry, not P7's entry
lines — a wave-1 executor could build a duplicated SOURCES row, burn a module, and still see M04 survive. M07's
citation of `QUALITY.md:300` is unreachable: the genuine D5 capture's quote is contiguous raw, so acceptance of
the genuine state says nothing about tag stripping.
Evidence: `pkg_gate.py:211-232` vs `:184-209`; the measured D5 test in §6; `QUALITY.md:15-18` (Q1) allows
"row id(s)".
Impacted axis: calibration (count), operability (a fixture built to the cell's wording misses the mutant).
Smallest correction: M01's cell → "a D5 capture pinned on a non-first manifest row is accepted [`SCORECARD.md:564`
'the labelled D4/D5 correction lines against a spec of pinned digests'; Q24 unreachable, the genuine manifest's
row 1 is the capture"; M04's cell → "the entry carries exactly one `source:` line per row [no advertising
sentence; `SOURCES rows` at `SCORECARD.md:564` names the registry P6 reads]"; M07's cell → "no advertising
sentence; the genuine capture's quote is contiguous raw, so Q24's acceptance does not reach the strip". Then the
calibration count is 4 at freeze (of 7), and §C1 says so instead of "each one advertised behaviour".

**D3 — separability is false as written.** Both directions demonstrated (§4), plus a third node outside the pair
(V6's fleet-root census path, `round39_c2_verify.py:65`). Evidence: `round36_c1_verify.py:55-68`;
`round39_c2_verify.py:65,116-127`; `pkg_gate.py:276`; the two coupling receipts; F38SentinelBattery's round-38
offline receipts. Impacted axis: calibration (overreach) and operability (landing order). Smallest correction: the replacement sentence in §4, plus a note for
the integrator that C2's entry + index row + bullet must land in one commit.

**D4 — Q29's executable cannot load the round-39 list** (§7). Impacted axis: calibration (an instrument that
cannot certify the list it is named for; R2's Q29 clause is unimplemented). Smallest correction: the adapter above,
or name the counter's `exhibits=` leg as the Q29 check for round 39.

**D5 — two provenance tokens have no witness** (`stagecheck cases=25 failed=0`; "S117/S118 opened 2026-10-26
03:27 -03"), and the baseline tip is the freeze's grandparent. Impacted axis: calibration (a claim about bytes
without committed bytes is Q22's subject). Smallest correction: commit the stage-check output beside the controls
(`plans/git_leak_probe.py --stage-check > .ufo/waves/round-39/claims/stagecheck.txt`) or drop the number, and say
"baseline tip `b2bdd42`; freeze parent `ef2fba0`".

No defect found in: the 7-mutant arithmetic (1 + 3 + 3 = 7 reproduces from the three named sources); the
direction witnesses (all five citation targets exist and carry the quoted W-/A-/B- ids); the exclusion of
`F38XMutRerunMain` X04 and the withdrawal of `F38XMutP` X06 (both reports say so); the gate/probe/table digests;
the C1 controls; the C2 controls; the C2 counter's "no check added or relaxed".

Bounds named, not defects: C1 executes round-38's discovery with a four-fixture delta (§2); the universal
clauses are demonstrated at the first non-zero index only (§5); a post-freeze corpus edit that leaves the lane
internally inconsistent reds C1 for a reason outside the gate (§4).

Local hygiene: no tools installed or upgraded (none needed); pacman untouched; no lane file, fleet-root file or
git index written; the lane was never mutated (all work in the `--shared` clone, deleted); clone gate sha256
`ea638822…` before and after.

## 9. Post-report corroboration (R39AdvErrata) — M01 moved from K to N

After this report was first written, seat `R39AdvErrata` independently audited the same seven cells
(`build/R39AdvErrata.md` §3, receipt `build/R39AdvErrata/verify.txt`) and measured what §1 had only inferred:
`quarantine-SHA256SUMS` has two rows and row 1 **is** the capture digest (`b60af775…`), so M01's `[:1]` mutant is
a no-op on the accepted state and its Q24 citation cannot reach the behaviour. I re-confirmed that row order from
the spec's own paths (`pkg-spec-r35.json` `d5_capture_dir` + `d5.manifest_name`), so M01 is tier **N as cited**,
not K: a covering class sentence exists at `SCORECARD.md:564`, but the cell does not name it, and the task's
question is what the cell maps to. Counts are now C 2, K 2, N 3 — the peer's split (2 direct, 2 indirect
unmarked, 3 uncitable) and mine agree cell for cell.

One qualified disagreement, accepted: the peer does not count Q1 (`QUALITY.md:15-19`) against M04, because Q1
constrains what a `source:` line carries, not how many lines a row id gets. §1's Q1 citation is therefore
demoted to supporting context; M04's verdict rests on the wrong-artefact point (`pkg_gate.py:211-232` vs
`:184-209`) and on no sentence anywhere requiring one `source:` line per row, which is what the tier needs.

Nothing frozen was edited in either seat's work; this section is the only change to this report after its first
submission.

VERDICT: claims-attack-5-defects-unadvertised-3
