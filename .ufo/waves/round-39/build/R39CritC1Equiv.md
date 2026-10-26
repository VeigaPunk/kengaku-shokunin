# R39CritC1Equiv — Q29 direction check on the seven frozen C1 mutants (before battery39 lands)

Seat: critic, round 39 wave 1. Scope: the seven frozen mutants of `plans/round39_c1_verify.py` only.
Nothing frozen was edited; every mutation was applied to a **copy** of `plans/pkg_gate.py` inside
`/fast/scratch/hyaku/kengaku-r39/R39CritC1Equiv/lane` (a `git clone --shared` of the lane, HEAD
`750473847af9c7a461487ba3a589b5519fac5ed8`, `git rev-parse --show-toplevel` = the clone). Scratch deleted
at the end of the seat; every script and log quoted below is copied under
`.ufo/waves/round-39/build/R39CritC1Equiv/receipts/`.

Short answer: **all seven declared directions are reachable, and I could not make any of the seven
observationally equivalent — each has a constructive witness, and each mutation is provably monotone in
its own predicate, so no contrary direction exists either.** Control kills for M01/M05/M06 are honest
exhibits of their declared direction. I found no defect requiring a change to any frozen file; the items
in §6 are notes for the L1, not edits.

## 1. Environment and control reproduction

    $ python3 - <<EOF   # load round39_c1_verify.py, compare PINS
    PINS total=26 mismatched=0
    M01 D5 mirror count(old)=1 new_count=0      (same for M02..M07: every `old` occurs exactly once)
    TOTAL 7 mutants 7

    $ cd lane && python3 plans/round39_c1_verify.py --lane . --work $S/w39e     # default = do-nothing control
    PINS total=26 mismatched=0
    BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
    MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0
    PREDICATE C1 fail                                           rc=1

Byte-for-byte the state recorded in `claims/control-c1-nothing.txt`, with the same kill attribution
(M01 `d5m-n21-manifest-row-2`, M05 `p23-p2-receipt-deleted`, M06 `r36-P0`). Receipt: `receipts/control.log`.

## 2. Reachability: the seven declared directions, rebuilt from inputs I constructed

Method: `ctx = r37.Ctx(lane, r36)` (round-37 counter), `ctx.genuine_package(d)` + `ctx.git_add(d)` for a
clean-tree genuine package; each mutant written as `gate_src.replace(old, new, 1)`; every run through the
counter's own `run_gate` (so the frozen r35 spec is appended — **no fixture-supplied `--spec` anywhere**).
`receipts/witness_ladder.py`, output `receipts/ladder.json`:

| mutant | declared | my witness input | reference | mutant | direction seen |
|---|---|---|---|---|---|
| M02 | P1 / silence | off-pin byte appended to the **second** frozen instrument (`plans/round35_c1_verify.py`), index staged | rc=1, `{P1}` | rc=0, `{}` | **silence** |
| M03 | P3 / silence | first located-quote row rewritten to **26** words (`quote_words=[3,25]`) | rc=1, `{P3,P4}` | rc=1, `{P4}` | **silence** (P3) |
| M04 | P7 / silence | one **stale duplicate** `source: S106 …` line appended to the entry | rc=1, `{P7}` | rc=0, `{}` | **silence** |
| M07 | D5 / mirror | tag `<b></b>` injected **inside** the D5 quote span of a copied capture, manifest re-pinned | rc=0, D5 ok | rc=1, `{D5}` | **mirror** |
| M01 | D5 / mirror | capture digest moved to **manifest row 2** (one decoy row first), capture untouched | rc=0, D5 ok | rc=1, `{D5}` | **mirror** |
| M05 | RUN / rc-silence | empty (rejecting) package with one DEFECT clause | rc=1, `{P1..P9}`, declared non-empty | rc=0, same set | **rc-silence** |
| M06 | MAIN / rc-mirror | genuine round-35 package, clean tree | rc=0, all ok | rc=1, all ok | **rc-mirror** |

Boundary controls in the same run show the flips are exactly at the mutation's boundary, not artefacts:

    PROBE pin-index0            ref=1:P1        mut=1:P1        SAME       (first pin is still checked)
    PROBE pin-index1 / -index2  ref=1:P1        mut=0:-         EXHIBIT
    PROBE pin0-deleted          ref=1:P1        mut=1:P1        SAME
    PROBE words-25              ref=1:P4        mut=1:P4        SAME
    PROBE words-26              ref=1:P3,P4     mut=1:P4        EXHIBIT
    PROBE words-27              ref=1:P3,P4     mut=1:P3,P4     SAME
    PROBE srcline-first-stale   ref=1:P7        mut=1:P7        SAME       (first line is still compared)
    PROBE srcline-1-stale/2-stale ref=1:P7      mut=0:-         EXHIBIT
    PROBE d5row-1of2            ref=0:-        mut=0:-         SAME
    PROBE d5row-2of2            ref=0:-        mut=1:D5        EXHIBIT
    PROBE d5tag-outside         ref=0:-        mut=0:-         SAME       (a tag away from the quote is harmless)
    PROBE d5tag-inside          ref=0:-        mut=1:D5        EXHIBIT
    LADDER probes=23 exhibit=11 same=12 other=0

I also re-ran the committed round-38 harness itself,
`.ufo/waves/round-38/falsify/F38XMutP/witness.py LANE WORK`:

    WITNESS wx01 mutant=X01 ref_rc=1 ref_defects=P1,P9 mut_rc=1 mut_defects=P9 flip=P1->P1-ok ok
    WITNESS wx05 mutant=X05 ref_rc=1 ref_defects=P3,P4,P9 mut_rc=1 mut_defects=P4,P9 flip=P3->P3-ok ok
    WITNESS wx15 mutant=X15 ref_rc=1 ref_defects=P7,P9 mut_rc=1 mut_defects=P9 flip=P7->P7-ok ok
    WITNESSES total=3 ok=3

identical to the committed `witness-run.txt`, and its three `old`/`new` pairs are **byte-equal** to
M02/M03/M04's (checked programmatically: `X01->M02 old_equal=True new_equal=True`, same for X05->M03,
X15->M04). M01's `old`/`new` are byte-equal to round-38 `N21`'s
(`plans/round38_c1_verify.py:140-141`), so the relabel preserves mutant identity. The round-38 `X07`,
`X10`, `X15` texts named in `F38XMutRerunMain.md:53,56,57` are exactly M05/M06/M07's.

Note the round-38 witnesses are *not* clean-tree packages (`P9 DEFECT untracked=…` in every line). My
ladder variants stage the index (`ctx.git_add`) and the target clause is the only defect — a battery39
fixture must do the same.

## 3. Are the three control kills honest exhibits?

Pulled from the full pair matrix (`receipts/matrix.py`, `receipts/matrix.json`):

    M01 d5m-n21-manifest-row-2  expect=accept declared=[]      ref [0,[],[D5]]   mut [1,[D5],[]]   mirror + rc-mirror
    M05 p23-p2-receipt-deleted  expect=reject declared=[P2]    ref [1,[P2],…]    mut [0,[P2],…]    rc-silence
    M06 r36-P0                  expect=accept declared=None    ref [0,[],[P1..P9]] mut [1,[],[P1..P9]] rc-mirror

- **M06 is not an artefact of `r36-P0`'s shape**: `r36-P0` is the round-36 recipe *"genuine round-35
  package"* (`plans/round36_c1_verify.py:130`), and my independently built genuine package flips the same
  way (`PROBE accept-genuine … ref=0:- mut=1:-`). Both are the advertised sentence.
- **M05's fixture** is a real reject whose declaration (`["P2"]`) matches the reference DEFECT set, so
  `rc-silence`'s precondition (`expect=reject` + non-empty `defects`) is met by the fixture, not by a
  fallback. Clause lines are identical on both sides: only the exit code moves.
- **M01's fixture** is a genuine capture with the matching digest on row 2 (`D5 ok directional=True
  digest_pinned=True` vs mutant `DEFECT … bad=['capture digest is not the one in the manifest']`). The
  mutation `sums.splitlines()` → `[:1]` feeds one `any(...)` over a shorter list, so the mutant can only
  *add* the pin defect and never remove it — `plans/battery38/d5m.py:21` states the same ("the gate change
  only ever adds the pin defect, so no input can make the reference defect where the mutant passes").
  The original `silence` label was therefore unreachable and `mirror` is the only possible direction; the
  control kill is an honest exhibit, not a relabel artefact.

## 4. Equivalence attack at (exit code, DEFECT set) granularity

Measurement object is the counter's own `run_gate` triple `(rc, DEFECT set, ok set)` — at or finer than
(exit code, DEFECT set).

**(a) Per-mutation monotonicity (the mutation's effect is one-directional by construction).**

| mutant | change | why only one direction is possible |
|---|---|---|
| M02 | `pins.items()` → `list(pins.items())[:1]` | `bad` = comprehension over a shortened list ⇒ `bad_mut ⊆ bad_ref`; `bool(pins)` unchanged. Laxer only ⇒ `mut ok ⇒ ref ok`. |
| M03 | `hi` → `hi + 1` | `short` shrinks ⇒ P3 can only turn ok. Laxer only. |
| M04 | `prov.get(sid) != [u]` → `(prov.get(sid) or [""])[0] != u` | `ref ok` (list == `[u]`) ⇒ first element == `u` ⇒ `mut ok`; the converse fails when the list has >1 entry. Laxer only. |
| M05 | `defects += not ok` → `defects += 0` | only `cmd_*` return value changes; clause prints untouched. rc 1→0 only. |
| M06 | `return 0 if …==0 else 1` → `return 1 if …==0 else 1` | accept branch 0→1; reject branch unchanged (1); setup/exception path 2 untouched. Stricter only. |
| M01 | `any(...)` over all rows → over `[:1]` | `pinned_mut ⇒ pinned_ref`; everything else in D5 unchanged. Stricter only. |
| M07 | tag strip removed from `flat` | `flat_ref` is `flat_mut` with tag spans deleted; the spec's D5 quote contains no `<`, so a contiguous occurrence in `flat_mut` survives deletion ⇒ `mut ok ⇒ ref ok`. Stricter only. |

**(b) Frozen 86-fixture battery, all seven mutants** (`BATTERY fixtures=86`, families 66 package /
8 d4-line / 12 d5-line):

    M01 D5 mirror   fixtures=12 differences=1  directions={mirror:1, rc-mirror:1}   (d5m-n21-manifest-row-2)
    M02 P1 silence  fixtures=66 differences=0
    M03 P3 silence  fixtures=66 differences=0
    M04 P7 silence  fixtures=66 differences=0
    M05 RUN rc-silence fixtures=66 differences=60  directions={rc-silence:53}       (7 unclassified = r36-P1..P7)
    M06 MAIN rc-mirror fixtures=86 differences=4   directions={rc-mirror:4}
    M07 D5 mirror   fixtures=12 differences=0

**No mutant produced a difference outside its declared direction.** The seven "unclassified" M05 rows are
round-36 fixtures that carry `defects=None`, so `exhibits()`'s rc-silence arm (which needs a non-empty
declaration) cannot label them; they are the same 1→0 flip.

**(c) Differential fuzz over the mutant-relevant surface** (60 random package variants built from the
genuine package with 1–2 random edits from {duplicate source line (same/stale URL), off-pin byte, quote-row
rewrite at a random word count, quote-row deletion, untracked file, capture byte, receipt byte}; 30 random
D5 variants from {manifest permutation, stale digest, tag inside/outside the capture}):

    M01 diffs=3  {mirror:3, rc-mirror:3}      M02 diffs=3  {silence:3, rc-silence:2}
    M03 diffs=0                               M04 diffs=18 {silence:18, rc-silence:13}
    M05 diffs=47 {rc-silence:47}              M06 diffs=13 {rc-mirror:13}
    OUT-OF-DIRECTION 0

(M03 drew no word-count that lands exactly on `hi+1`; the ladder's `words-26` covers it.)

**(d) Where each mutant *would* be equivalent — precise, spec/domain-relative.** None of these is reachable
with the frozen r35 spec, which is why every witness above holds:

- M02 is exactly equivalent on any spec with **≤1** entry in `frozen_instruments` (`[:1]` == `items()` then);
  the frozen spec has 3.
- M04 is equivalent whenever every registry row ends up with exactly one `source:` line.
- M01 is equivalent whenever the D5 capture's digest always sits on manifest row 1.
- M07 is equivalent whenever no capture carries markup inside a quote span.
- M05/M06 are *not* domain-limited: they flip on every accept/reject respectively.

So: **equivalent = 0/7**. The equivalence question is closed by witness, not merely unproven.

## 5. Counter-side closure: the four survivors die inside the frozen machinery

I wrote one critic-side module of four fixtures from `Ctx` alone (no `--spec`, no forbidden token:
`sidechannel=0`) and ran the counter with `--battery-dir` (nothing written into the lane):

    $ python3 plans/round39_c1_verify.py --lane . --battery-dir $S/b39 --work $S/w39d
    PINS total=26 mismatched=0
    BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
    MUTANT M01 … killed by=d5m-n21-manifest-row-2
    MUTANT M02 … killed by=reach-pin2
    MUTANT M03 … killed by=reach-words26
    MUTANT M04 … killed by=reach-srcline
    MUTANT M05 … killed by=p23-p2-receipt-deleted
    MUTANT M06 … killed by=r36-P0
    MUTANT M07 … killed by=reach-d5tag
    MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0

(rerun byte-equal, `receipts/full7.log` vs `receipts/full7b.log` → `REPEAT-BYTE-EQUAL`). Fixture
declarations the counter accepts exactly: `reach-pin2 → ["P1"]`, `reach-words26 → ["P3","P4"]`,
`reach-srcline → ["P7"]`, `reach-d5tag → accept/[]`. Renamed-tree check passes for all four, so they are
path-independent. This is a demonstration that C1's claimed work is achievable, **not** a proposal that my
module is what should land (executors own `plans/battery39`; a different module with the same exhibits is
equally valid).

## 6. Findings for the L1 (no frozen file needs a change)

1. **No defect in the seven rows.** Directions are correct, reachable, monotone and attributed; the three
   control kills are honest. Nothing here blocks C1's `killed=7`.
2. **Witness-provenance wrinkle (documentation only).** The label `X15` is reused across round-38 seats:
   `F38XMutP/witness.py`'s `X15` is the P7 provenance-first-item mutant (→ M04), while
   `F38XMutRerunMain.md:57`'s `X15` is the D5 tag-strip mutant (→ M07). M07's witness cell cites
   `survivor-probeB.txt` without an id, so it resolves unambiguously; M02/M03/M04's cells resolve inside
   `F38XMutP/`. Recommend the landing note say "X-ids are per-seat" rather than touch the frozen counter.
3. **M05 is broader than its sentence, and the kill rule is narrower.** `defects += 0` also flattens
   `d4-line`/`d5-line` rejects, but `family_ok("RUN", argv)` admits only `package`, so the mutant's
   behaviour outside `package` is unmeasurable under the frozen rule. No action: the advertised sentence is
   about the package exit code.
4. **M06's rc-mirror is package-only and cannot be killed by an error fixture** (the setup path still
   returns 2). Sound; noted so no one tries.
5. **Review intensity for battery39:** two of the four survivor kills (M03, M04) share the "rewrite/append a
   row" mechanic, and the counter cannot check intent (a named limit in the claims). The four exhibits I
   produced are single-purpose; recommend the non-author module review check that each of the survivors'
   fixtures names the behaviour it is priced at.
6. **Do not land the round-38 witnesses verbatim** if they are copied: their packages are unstaged, so they
   add a `P9 DEFECT` to the declared set (harmless for the kill, but the declaration then reads `P1,P9`
   rather than `P1`). Stage with `ctx.git_add` as in `receipts/reach.py`.

Limits of this check: I measured one host (`git 2.56.0`, Python 3.14), one frozen spec (r35), and the
counter's own runner; "equivalence" is refuted constructively, not exhaustively enumerated over arbitrary
inputs — but each mutation's monotonicity argument in §4(a) is a proof over all inputs, so the search space
that remains is only whether a witness exists, and it does for each.

VERDICT: c1-directions-reachable-7/7-equivalent-0
