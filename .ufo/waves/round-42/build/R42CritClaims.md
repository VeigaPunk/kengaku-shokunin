# R42CritClaims — attack on the frozen round-42 claims and controls

Seat: `R42CritClaims` (critic, leaf). Round 42 wave 1, 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
at `fda71ae` (freeze `bc856d8`, receipt `523b278`). Nothing frozen was edited; no lane file was written, staged or committed.
All work happened in `--shared` clones at `S=/fast/scratch/hyaku/kengaku-r42/R42CritClaims` (`lane-a`, `lane-b`, `lane-c`),
each verified `git rev-parse --show-toplevel` = its own directory. Artifacts: this directory (`SHA256SUMS.txt` lists them).

## 0. Envelope journal (Q32)

Every counter / gate / fixture build ran under:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent <command>
```

`ls -A /home/vgpnk/.local/bin | sha256sum` = `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18`
before and after **every** run (C1 copy run 17:36:49, C2 counter runs 17:31:23→17:36:32, gate 17:36:48; unchanged each
time; also unchanged at 17:37:09 after the default C1 predicate run). No writes outside `$S`. No install, no pacman.

| receipt | command (cwd = clone) | start → end | exit |
|---|---|---|---|
| `lane-a-c2.txt` | `python3 plans/round42_c2_verify.py --lane . --work $S/w-lane-a3` | 17:35:20 → 17:36:32 | 1 |
| `lane-b-c2.txt` | same, `--work $S/w-lane-b` | 17:31:23 → 17:32:24 | 0 |
| `lane-c-c2.txt` | same, `--work $S/w-lane-c` | 17:32:24 → 17:33:25 | 0 |
| `coupling-p9.txt` | `python3 plans/pkg_gate.py package --root . --spec <effective>` | 17:36:47 → 17:36:48 | 1 |
| `c1-copy-default.txt` | `python3 plans/round42_c1_verify.py --lane .` with copied witness modules in `plans/battery42` | 17:37:04 → 17:37:09 | 0 |
| `c1-copied-witness.txt` | `python3 plans/round42_c1_verify.py --lane . --battery-dir $S/bat-copy --only X1,XO1` (+ token run) | 17:36:47 → 17:36:49 | 0 / 1 |

Frozen-digest check in a clean clone at `fda71ae`: all 12 files in `.ufo/waves/round-42/claims/frozen-digests.txt` match
(`sha256sum` loop, 12/12 OK), including `plans/round-42-claims.md` `2c4a5e04…`. Claims and receipt commits are ordered
`bc856d8` (freeze) → `523b278` (receipt); `bc856d8`'s parent is `d69452c` (the stated baseline). Claims facts about the
captures were re-read from the captures: test 2 `line_count < 32000` (`test_outputs.py:23`), test 3 `["gcc","-O3","/tests/sim.c","-o","sim"]`
(`test_outputs.py:66`), the 28 values (`:73-102`, max 48401), `sim.c` reads `parse_gates("gates.txt")` (`sim.c:319`),
`argv[1]` (`sim.c:323-324`), and prints `values[num_signals - 32 + i]` (highest indices, `sim.c:340-347`). The claims'
grader facts are faithful.

## 1. C2 — the informed filler (headline)

I built the filler the assignment names, from nothing but the shipped receipt, dry table and captures, with a script
(`mkfiller.py`, copied here): source lines, `verified-at`, `recheck`, a `## Case table` copied row-for-row from the
receipt, SOURCES rows S125–S127 carrying the real pinned digests, one README index row, one coverage bullet, one
README §Frontier bullet, one PROVINCE line. No grader was read; no finding is stated.

* **Filler A** (`lane-a`) = exactly that. Entry line 11 reads `Registry rows S125 S126 S127 (mechanical filler; no
  finding is claimed).` Case-table Note column = `x`.
* **Filler B** (`lane-b`) = A plus two *mechanical* sections: `## Located quotes` = the first 8 capture lines whose
  stripped word count is 3–25 (copied by line number, claim column says `mechanical qN`), and `## Requirement map` =
  7 rows whose label is computed by the counter's own rule (`derive()` over the receipt's `violates=` sets) and whose
  citation is the first violating case.
* **Filler C** (`lane-c`) = B plus deliberately **false** content: Summary says the simulator "reads its input from
  stdin and prints the last 32 lines of gates.txt; a nine-line file passes every test", and every case row's Note
  column says `verified correct by inspection`.

Results (full receipts in this directory):

| check | A | B | C |
|---|---|---|---|
| V1 captures | ok | ok | ok |
| V2 gate (`--rerun --require-clean-tree`) | **DEFECT** (P3, P4) | ok | ok |
| V3 registry rows | ok | ok | ok |
| V4 receipt/entry shape | ok | ok | ok |
| V5 probe dry table | ok | ok | ok |
| V6 census | ok | ok | ok |
| V7 requirement map | **DEFECT** (absent) | ok | ok |
| V8 order | ok | ok | ok |
| V9 case table / mentions | ok | ok | ok |
| **checks / predicate** | **7/9, fail** | **9/9, `PREDICATE C2 pass`, exit 0** | **9/9, `PREDICATE C2 pass`, exit 0** |

B's and C's full output is byte-identical except paths; both print `gate: defects=0`, `gate: P10 ok probe_rerun=byte-equal
bytes=4212`, `checks=9 defects=0`, `PREDICATE C2 pass`, `EXIT 0` (`lane-b-c2.txt`, `lane-c-c2.txt`).

So: the assigned filler already passes **7 of 9** checks; two mechanical additions (8 capture lines, one derived table)
take it to **9/9**. Nothing in the package understands the grader, states a finding, or could be called the "eighth
grader class" the C2 claim is about. The entry even carries the false provenance line "read and executed" in its H1 and,
in C, false statements contradicted by the very captures the gate verified.

The round's own cited proposal warned about exactly this: `considerthese/2026-10-26.md:44-49` proposes "a committed
filler package that must stay red" and says "A counter that admits filler should not appear in a verdict cell as the
admission basis." The frozen C2 predicate admits an informed filler, and the round's `control-c2-filler.txt` only shows
the *round-41* shape (no case table at all) staying red.

This is a **repeat of a known class**, not a new discovery: round 41's critic measured the same thing at 8/8
(`.ufo/waves/round-41/build/R41CritClaims.md:114`: "C2's frozen predicate passes a 43-line filler that says it teaches
nothing (8/8)") and recommended "leave the frozen predicate; require those three in the L1 admission review". Round 42's
counter docstring cites that finding as V9's motive (`plans/round42_c2_verify.py:14`) and V9 closes only the *shape*
half; my B is the same class at 9/9.

### 1.1 What V9 actually is (format/consistency, not content)

V9 (`plans/round42_c2_verify.py:282-309`) binds the entry's `## Case table` to the receipt as a **triple**
`(cid, tests letters, observed)`; the Note column is `.*` (`CASE_ROW`, line 84). It then does four substring tests:
row ids anywhere in the entry body outside `source:` lines (line 303-304), the task + file name on one PROVINCE line,
and the task anywhere inside README `## Frontier`. It reads no prose.

What it cannot see, shown by B and C:

1. **The Note column** — `x` (B) and `verified correct by inspection` for a failing `nop` (C) are both accepted.
2. **Row-id placement** — one line `Registry rows S125 S126 S127` satisfies it; no per-row registry citation.
3. **PROVINCE semantics** — my line says the grader is "named … and nowhere else" (`filler-b-entry` clone,
   `PROVINCE.md:536`); it passes, though the claim promises a PROVINCE *paragraph* narrowing the round-35..41 clause.
4. **README Frontier semantics** — B's bullet at `corpus/README.md:371` says `named; see …`; C's coverage bullet says
   `No finding.` Both pass.
5. **All prose truth** — Summary/Findings/Negative space are unread. C's stdin / "last 32 lines" / "nine-line file"
   statements are false (captures: `instruction.md:8-9`, `sim.c:319,323-324,340-347`) and pass.
6. **The captures** — V9 compares the table to the *receipt*, never to the captures, so it cannot tell whether any row's
   description matches what was observed; V7's labels are derived from the receipt's own `violates=` tags, so the map
   mirrors the probe rather than an independent reading.
7. **The analysis that would justify admission** — which instruction line each test enforces, the cwd/`argv[1]`/highest-index
   semantics that make the lookup circuit work, the instruction-vs-grader gaps, limits, prior art: none of it is read.

What V9 *does* bind: the 16 case ids, their test letters and observed verdicts (against the receipt), and the receipt is
bound to a byte-equal probe rerun by the gate's P10 (`4212` bytes). So the numbers are authentic; the meaning is not
checked. The claims file calls this block "**V9 content**" (`plans/round-42-claims.md:79`) — it is a consistency check.

Related gate facts: P6 accepts a `teaches` cell that says "describing nothing that was read from the captured grader"
(it only counts words), P7 accepts the sentence `Falsifiers are not named here; this is a mechanical filler control.`
(it only matches `/falsifi(er|ed|es|ability)/`), and P3 ignores the "Claim supported" column entirely.

## 2. Control discrimination

| control | claimed | observed | discriminating? |
|---|---|---|---|
| C1 `control-c1-nothing.txt` | 0 fixtures, 14 survived, fail | `BATTERY fixtures=0`, `MUTANTS total=14 killed=0 survived=14`, `PREDICATE C1 fail`, exit 1 | yes |
| C1 `control-c1-no-mutants.txt` | `total=0`, fail | `MUTANTS total=0 … killed=0`, `PREDICATE C1 fail` | yes |
| C1 `control-c1-attribution.txt` | forced span → `unattributed=14`, fail | `killed=0 survived=0 … unattributed=14`, `PREDICATE C1 fail` | yes |
| C1 `control-c1-tool-edited.txt` | pin mismatch, 9 invalid, fail | `PINS mismatched=1`, `anchor=0/9`, `invalid=9`, `PINS-AFTER mismatched=1`, fail | yes |
| C1 `control-c1-hostile-escape.txt` | `SETUP … breaks the contract`, exit 2 | exact line, exit 2 | yes |
| C1 `control-c1-direction-mislabel.txt` | round-40 labels fail | `XO5/XO6 SURVIVED exhibits=0>1,rc-mirror`, 12/14, `PREDICATE C1 fail` | yes |
| C1 `control-c1-witness-as-battery.txt` | copies → `PREDICATE C1 pass` | pass, 14/14, sidechannel=0 | **dual role: also the forbidden-copy bypass (§3)** |
| C1 sidechannel leg | (no red control at freeze) | I injected `# socket` into a copied module → `SIDECHANNEL bat-copy/a_copied.py tokens=socket`, `sidechannel=1`, exit 1 (`c1-copied-witness.txt`) | yes, now shown; the freeze had no control for it |
| C2 `control-c2-nothing.txt` | `checks=9 defects=6` | `defects=6` (V2 V3 V4 V7 V8 V9) | yes |
| C2 `control-c2-filler.txt` | filler V9 red; "same mirror with the measured content → V9 ok" | red for the no-table shape only; the green mirror's row text is the literal word `measured` (`c2_filler_control.py:59`) | **not against an informed filler** (§1) |

Both claims' do-nothing controls are honest and red; the gap is on the *junk-but-shaped* side of C2 and the *copied*
side of C1.

## 3. C1 — the forbidden renamed copy reaches the frozen predicate

Claims rule (`plans/round-42-claims.md:55-56`): "The battery may not import, copy or read the freeze modules
(`claims/witness/`); the token scan flags `witness`." The counter has no check that a module is not a copy: it hashes
nothing against the witness files and scans only the `SIDECHANNEL` token list (`round42_c1_verify.py:100-103,478-482`).

Counterexample (default predicate, not development mode): I copied the two frozen witness modules, unchanged, to
`plans/battery42/aa.py` and `bb.py` in my clone and ran the predicate as the claims file specifies:

```
PINS total=2 mismatched=0
BATTERY fixtures=14 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=9/9 order=5/5
PINS-AFTER mismatched=0
PREDICATE C1 pass
EXIT 0
```

(`c1-copy-default.txt`; the copies contain none of the 27 tokens — I checked each — and the injected-token run above
shows the scan is otherwise discriminating.) The claims file already contains this result as a *positive* control
(`control-c1-witness-as-battery.txt`, "reachable by witnessed work") without noting that the artifact it used is exactly
the one the work rule forbids. Consequence for the *claim*, not just hygiene: C1's self-assessment is "the number of
these 14 frozen mutants that **no `plans/battery42` fixture** kills attributably"; with a copied battery that number is
reached with **zero new fixtures**, so the round's calibration move is imported from the freeze's own pre-freeze witness
and the predicate cannot tell the two apart.

Smallest safe correction: in `round42_c1_verify.py`, compare each module's normalized token multiset (or AST dump) against
`claims/witness/*.py` and print `COPY`/fail; failing that, add this to "Limits named now" and make the integrator diff
`plans/battery42` against the witness modules before admission. Do not relabel the positive control as reachability
without the caveat.

## 4. Are the claims causally separable?

* **C1 from C2: yes, structurally.** The counter reads the two tools (`TOOLS`/`PINS`), the battery dir, and hides the
  lane from builds; it never opens the C2 entry, SOURCES, README, PROVINCE or receipt. The freeze's witness-as-battery
  control passed in a mirror with no C2 entry.
* **C2 from C1: only with C1's work product *wholly absent*.** C2's V2 runs the gate with `--require-clean-tree`, whose
  P9 is `git ls-files --others --exclude-standard` over the **whole worktree** (`pkg_gate.py:259-265`). With one
  untracked C1 module present (`plans/battery42/untracked_probe.py`), the otherwise-9/9 clone prints
  `P9 DEFECT untracked=1 first=plans/battery42/untracked_probe.py`, `EXIT 1` (`coupling-p9.txt`). C2's V8 also executes
  the frozen `plans/order_check.py` (the tool C1 pins). The good direction is real too: `lane-b`/`lane-c` carry no
  `plans/battery42` at all and pass V1-V9 (9/9), so C2 does pass with C1's product absent.
* The claims' sentence — "Neither counter reads the other's work product: each passes with the other's work wholly
  absent" (`plans/round-42-claims.md:96-100`) — is literally true and materially misleading: C2 is **not independent of
  a sibling's in-flight files**, only of its absence, and C2 has to be measured after C1's `plans/battery42` is
  staged/committed. Scope correction: add the worktree to C2's read set and state the landing order.

## 5. Is the lowest-axis choice honest?

Yes, and it is disclosed rather than dressed up. `SCORECARD.md:1689-1695` records calibration 8, coverage 7 (capped by
the open L0 question `kengaku | round-33`), novelty 7, and says "A coverage claim is score-dead (+0) under the cap".
The claims file repeats the tie-break and the cap and says "C2 is judged on its counter, not on a score move". The L0
question is present and open (`.ufo/l0-questions.md:163`), so the cap's basis is real, not a stale excuse. The only
concession: because the cap is real, the round has **no** score-moving lowest-axis claim — the claims do not hide this.
(Minor: the corrected plan's C2 do-nothing expectation `checks=8 defects>=4` predates V9; the claims' `checks=9
defects=6` matches the frozen counter.)

## 6. Defects, impacted axes, smallest safe correction

**D1 — C1: the forbidden renamed copy reaches the predicate undetected.** Impact: calibration (the round's new-fixture
count), admission integrity. Evidence: `c1-copy-default.txt`; freeze's own `control-c1-witness-as-battery.txt`; token
scan discriminating (`c1-copied-witness.txt`). Correction: copy/similarity check in the counter, or a named limit + a
mandatory pre-admission diff.

**D2 — C2: "V9 content" is a consistency check; a content-free (and in C, false) entry passes 9/9.** Impact: coverage
(the admission basis), calibration. Evidence: `lane-b-c2.txt`, `lane-c-c2.txt`, `filler-b-entry.md`,
`filler-c-entry.md`; `round42_c2_verify.py:84,282-309`. Correction: rename V9 to what it checks, state in the claims
that the *content* half of admission is not counter-checked, and pin the admission rule to `considerthese/2026-10-26.md`
proposal 2 (a filler that must stay red cannot be a consistency mirror).

**D3 — C2: the filler control's green leg is itself a filler.** Impact: calibration (control evidence). Evidence:
`c2_filler_control.py:59` writes the row text `measured`; the claims call it "the same mirror with the measured content"
(`plans/round-42-claims.md:87`). Correction: reword the claim; add the informed filler (my B) to the freeze controls with
the honest expectation that V9 *passes* it, so no reader takes `CONTROL-C2-FILLER red-as-required` as covering fillers
with a table.

**D4 — C2/Separability: "reads only …" is false for the worktree.** Impact: calibration (separability statement),
operability (landing order). Evidence: `coupling-p9.txt`; `pkg_gate.py:259-265`. Correction: add the whole worktree to
C2's read set and require C1's files staged first, or scope P9 to the package paths.

**D5 — R3 is claimed discharged by V9, but R3 has a second leg and the "standing" filler control is neither
standing nor red against an informed filler.** Impact: calibration (routed-item ledger, Q30-class honesty). Evidence:
`corpus/lessons/round-41-verifier-spotcheck.md:114-115` asks for "a standing filler control that must stay red, and a
check that reads S124-style tier-B PR rows' live state word"; the claims map only "R3 (V9)" (`plans/round-42-claims.md`
§Frontier step), grep finds no S124/tier-B/live-state code in `round42_c2_verify.py`, `pkg_gate.py` or `fibsqrt_probe.py`,
and nothing re-runs `c2_filler_control.py` at the tip. Correction: name R3's tier-B leg as carried (this round's rows
S125–S127 are tier A, so its surface is absent) and stop presenting V9 as R3's discharge; if a standing control is kept,
say plainly that it can only be red for shape — my B passes V9 with no content at all.

Not counted as defects (named limits): (a) V2's P2 is self-pinning — `round42_c2_verify.py:136` writes `receipt_sha256`
from the tree it checks, so `P2 ok receipt_sha256=pinned` cannot fail; the counter's own docstring discloses this
(`:20-22`: "P2 is a presence check and authenticity rests on P10"), so it is a limit, not a hidden hole; (b) attribution proves a
replaced line *executed*, not that it *caused* the difference — the claims' limit sentence covers "not the fixture's
intent" but not this nuance; (c) my filler is not the round-41 filler shape, so `control-c2-filler.txt` is not wrong —
it is scoped too narrowly.

## 7. Reproduce

```
S=/fast/scratch/hyaku/kengaku-r42/R42CritClaims
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane-b
python3 $S/mkfiller.py $S/lane-b B && git -C $S/lane-b add -A
cd $S/lane-b && bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  python3 plans/round42_c2_verify.py --lane . --work $S/w-b      # checks=9 defects=0, PREDICATE C2 pass
# C1 copy: cp claims/witness/w_*.py $S/lane-a/plans/battery42/{aa,bb}.py; run with --lane .
```

Limits of this attack: I did not write a 14-fixture battery myself, so I make no independent statement about the
*difficulty* of C1 beyond the copy path; I did not re-fetch the upstream bytes (the capture-vs-upstream equality is the
L1's recorded fetch, not re-observed here); V2/P10 reran the frozen probe offline (host gcc/python), as the claims say.

VERDICT: claims-attack-defects-5-informed-filler-7/9
