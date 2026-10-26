# R41CritClaims — attack on `plans/round-41-claims.md` (frozen `3b239b50…`, commit `8ef8b4f`)

Scope: the frozen claims' framing only — whether a do-nothing or junk artefact reaches C1/C2, what
`control-c1-no-mutants` discriminates, whether C2's before-state is honest, separability, the lowest-axis choice
and the novelty sentence. Nothing frozen was edited; no lane file, index, jj state or `~/.local/bin` was touched.
My scratch was `/fast/scratch/hyaku/kengaku-r41/R41CritClaims`; seat `R41CritIndep` deleted the whole round root at
15:42:24 while I was working (orchestrator IRC), so I recreated `$S` and re-ran every step whose receipt I quote.
The scratch was deleted again at the end (`CLEANED=yes`). Every run used the mandated envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
--unshare-pid --die-with-parent` with `HOME`, `TMPDIR`, `UV_CACHE_DIR`, `XDG_CACHE_HOME` inside `$S`; no shared PATH
directory was written and no git shim was planted.

**Claim integrity and order.** `sha256sum plans/round-41-claims.md` → `3b239b5059deda27f874c4b38ea25666ef0d09db57d540fcffaa5de65c85ccfd`,
equal to `claims/frozen-digests.txt`; `plans/round41_c1_verify.py` → `8835a94b…`, `plans/round41_c2_verify.py` →
`cf1632b5…`, also equal. History: `8ef8b4f` freeze → `f774a87` first probe run → `fc79f2a` wave-1 spec. The order
sentence in the claims reproduces.

---

## 1. A content-free C2 filler reaches `PREDICATE C2 pass` 8/8

**Method.** Clone of lane HEAD `fc79f2a` (the real receipt is already committed at `f774a87`; entry, rows and README
row absent). I wrote a 43-line entry whose summary says *"this file exists only to satisfy the machine gate. It states
no finding and teaches nothing."*, appended S122/S123 registry rows and one README index row + one coverage bullet,
`git add` (index only), and ran
`/usr/bin/python3 <clone>/plans/round41_c2_verify.py --lane <clone> --work $S/w` in the envelope above.
Staged diff: 3 files, +49 lines (`junk-package-evidence.txt`).

**Result** (`c2-junk-filler.txt`): every gate clause `P1…P10 ok`; `V1…V8 ok`; `checks=8 defects=0`;
`PREDICATE C2 pass`; `RC=0`. V2's P10 reran the pinned probe from the clone and got `probe_rerun=byte-equal
bytes=5775`; V4 passed because the requirement-map rows cite the two `match=NO` ids; V7 passed because I derived the
11 labels mechanically from `violates=` and the observed verdicts in the receipt; V8 passed because the receipt is
committed after the freeze.

**What the filler omitted — and the counter never read.** The claims' C2 *Surface* names a PROVINCE paragraph, one
§Frontier sub-bullet narrowed to 7 of 89, and S124. In the same junk tree: `grep -c S124 corpus/SOURCES.md` → `0`;
`grep -c constraints-scheduling PROVINCE.md` → `0`; `corpus/README.md` §Frontier still says the clause "stays open
for the remaining TB2 task graders (6 of 89 read)" with no constraints-scheduling bullet (diff has only the two
Coverage-map additions). All three omissions still gave 8/8.

**Classification.** The claims name an "informed-filler limit of V1–V7" carried from rounds 37–40. This confirms the
limit is total — a filler that says it teaches nothing passes — and adds one undisclosed part: none of the three
named surface deliverables (PROVINCE, §Frontier, S124) is read by any check. The smallest safe correction is not a
frozen edit: make the L1's admission review (or a wave-2 non-frozen rider) check those three deliverables and the
entry's headline cases, and say so in the C2 admission paragraph; the frozen predicate stays as it is.

## 2. C1: do-nothing fails; the only junk path is the disclosed copy; `control-c1-no-mutants` is vacuity-only

- **Do-nothing** (`c1-do-nothing.txt`, freeze clone, no `plans/battery41`): `BATTERY fixtures=0`, `MUTANTS total=23
  killed=0 survived=23`, `PREDICATE C1 fail`, `RC=1`. Reproduces the claims' before state.
- **Junk copy** (`c1-witness-as-battery.txt`): copying `claims/witness/w_receipts.py` and `w_sources.py` into
  `plans/battery41` gives `fixtures=22`, `killed=23 survived=0`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`,
  `PREDICATE C1 pass`, `RC=0`. Both witness modules are in the freeze commit
  (`git ls-tree -r --name-only 8ef8b4f -- .ufo/waves/round-41/claims/witness`). So a renamed copy reaches C1; the
  claims forbid it and delegate detection to reviewers ("the battery may not import, copy or read the witness
  modules; reviewers check that"). That is a named limit, not a new defect — but it is the answer to "can junk reach
  C1": yes, by copy.
- **`control-c1-no-mutants`** (`c1-no-mutants-repro.txt`): my copy of the counter with `MUTANTS = []` inserted after
  the frozen list (same 81-byte patch position, line 233) over the 22-fixture battery prints `MUTANTS total=0 …
  PREDICATE C1 fail`, `RC=1`. It discriminates the round-40 D1 vacuity (empty list + battery present) and nothing
  more: it cannot distinguish a witness copy from independent work, and the guard is count-based (I verified the
  frozen list has 23 unique ids; there is no duplicate-id check, but `frozen-digests.txt` pins the counter bytes).
- **C1 wording defect (D1).** The C1 title and self-assessment say these mutants are ones "no committed fixture
  demonstrates" / "no committed fixture kills ATTRIBUTABLY in its declared direction" (`plans/round-41-claims.md:27,34-35`),
  yet the freeze commit contains the two witness fixtures and the claims' own control says they kill 23/23 (line 63:
  "the predicate is reachable, by witnessed work"). This is round-40 `D1` recurring; the count is honest only under
  the narrower "committed `plans/battery41` fixture". Smallest correction: insert `battery41` in the title and the
  self-assessment (or define "battery fixture" there), leaving the 23 as the battery-to-write count.
- **S10.** `s10_equivalence.txt` is rc-only (`ref_rc=5 mut_rc=5`), and the counter's `classes()` returns an empty set
  for `sources`, so rc-equivalence is the counter's own notion. The label "rc-equivalent" is honest.

## 3. C2 before-state is honest; the committed control is not a clean-clone control

Clean clone at `8ef8b4f` (`c2-freeze-before.txt`): `V2, V3, V4, V7, V8 DEFECT`; gate `P10 DEFECT receipt
unreadable`; `V8 DEFECT order_exit=2 result=not-PASS`; `checks=8 defects=5`; `PREDICATE C2 fail`; `RC=1`. This
matches the claims exactly: V8 is red because the receipt is not in `HEAD` at freeze (a setup error, not an order
violation), and P10 never executes the probe. Honest.

Note: `control-c2-nothing.txt` was taken in the lane and shows `P9 DEFECT untracked=30` from the freeze-day build
artefacts; my clean clone shows `P9 ok untracked=0` with the same `defects=5`. The verdict is robust, but the
committed control is not measured under the claims' own "clean clone" condition.

## 4. Separability holds both ways

- C2 8/8 in a clone with no `plans/battery41` at all (C1's work absent).
- C1 23/23 in a freeze clone with no C2 entry, receipt, S122/S123 rows or README row (C2's work absent).

One integration coupling, not a work-product dependency: C2's V2 P9 checks the whole tree's untracked files, so C2
cannot be measured green while C1's battery files are present but untracked. At landing everything is committed.

## 5. Lowest-axis choice and novelty sentence

The axis state matches SCORECARD round 40 (`calibration 8, coverage 7, novelty 7, depth 9, operability 8,
freshness 8, adjacency 8`); the L0 cap `kengaku | round-33` is real (`corpus/lessons/round-38-verifier-spotcheck.md:87`,
and the round-40 report repeats it). Coverage-as-lowest-tied is honest.

**Novelty wording defect (D3).** The claims say "Novelty 7 has no candidate this round" because the sharpest finding
is published as TB2.1 PR #245. Live check: PR #245 is **closed**, `merged=false`, closed `2026-10-08T19:02:36Z`, title
"Bind constraints-scheduling checks to the requested event"; its body does publish the first-`DTSTART` event-binding
defect ("the constraint and earliest-slot tests parse the first DTSTART", 11 words). But the round's own receipt
carries `CASE input-crlf-rewrite … violates=inputs-readonly` (line 31): rewriting all three inputs with CRLF passes
3/3 although `instruction.md:17-18` says any modification fails, because the integrity check compares
`read_text()` (universal newlines). PR #245's body discusses the *output parser* accepting CRLF ("It accepts CRLF,
folded lines, case-insensitive property names", 9 words), not the input-integrity `read_text()` hole. So an
unpublished novelty candidate exists; the next clause ("prices any unpublished case as a rider") concedes it. Smallest
correction: say "no novelty is claimed; the sharpest candidate is published; `input-crlf-rewrite` and the RFC-form
cases are riders", and (for the S124 row) record the PR as closed/unmerged.

## 6. Defect table

| # | defect | smallest safe correction |
|---|---|---|
| D1 | C1 title/self-assessment say "no committed fixture" kills the 23, but the freeze commit's own witness fixtures kill 23/23 (reproduced); round-40 D1 recurred | narrow to "no committed `plans/battery41` fixture"; keep 23 as the battery-to-write count |
| D2 | C2's frozen predicate passes a 43-line filler that says it teaches nothing (8/8), and never reads three named surface deliverables — PROVINCE paragraph, §Frontier 7-of-89 narrowing, S124 row | leave the frozen predicate; require those three in the L1 admission review (or a wave-2 non-frozen rider) |
| D3 | "Novelty 7 has no candidate this round" is contradicted by the receipt's `input-crlf-rewrite`; PR #245 is a closed draft about event binding, not the input-integrity hole | rephrase to "no novelty claimed; sharpest candidate published; other cases are riders"; record S124 as closed/unmerged |
| D4 | `corpus/lessons/round-41.md` is cited as the mined-mistake location but is absent at `HEAD` (`ls` error) | create it in wave 1 or cite the existing `F40CritPlanNext` D1 evidence |

D1/D3/D4 are frozen-text errata (nothing frozen may change this round; they belong in the L1's integration note or
the lesson). D2 is live admission work, not a frozen edit.

**What holds / what I did not attack.** The freeze digests and order reproduce; the do-nothing and tool-edited
controls behave as reported; `control-c1-no-mutants` fires; the freeze list has 23 unique ids; the C1 pins and the
C2 spec/gate/probe/capture pins match `frozen-digests.txt`; C2's V8 before-state is a setup-error red for the stated
reason; separability holds; the C1 copy loophole, the sidechannel token heuristic and the read-only host limit are
named by the claims. I did not run the hostile module, the C1 tool-edited control, or a fresh C2 probe outside V2's
P10; I did not test the relative-`..` argv escape or the count-based guard's duplicate-id blind spot, both of which
need a re-frozen counter and are limits, not this round's claims.

**Receipts** in `.ufo/waves/round-41/build/R41CritClaims/`: `c2-junk-filler.txt` (8/8), `c2-freeze-before.txt`
(defects=5), `c1-do-nothing.txt`, `c1-witness-as-battery.txt`, `c1-no-mutants-repro.txt`, `junk-entry.md`,
`junk-package-evidence.txt`.

VERDICT: claims-attack-defects-4-junk-c2-8/8
