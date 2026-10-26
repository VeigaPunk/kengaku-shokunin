# F40CritC1Count — recount of the C1 calibration denominator (wave 2, falsify)

Seat: critic, round 40 wave 2, item F40CritC1Count. Attack target: the 21 `adv` cells of
`plans/round40_c1_verify.py`, the "before→after" count the round may claim, and the lesson/SCORECARD wording.
Measurement tip: lane clone at `ec1005a2a28bc5cfdde7723374368ed4cc956eed` (`git -C "$S/lane" rev-parse HEAD` →
`ec1005a2a28bc5cfdde7723374368ed4cc956eed`; `--show-toplevel` = `/fast/scratch/hyaku/kengaku-r40/F40CritC1Count/lane`).
Nothing in the lane, the index or jj was written; no tool installed (nothing needed). Scratch
`/fast/scratch/hyaku/kengaku-r40/F40CritC1Count` removed before this report was filed.

Receipts (all under `.ufo/waves/round-40/falsify/F40CritC1Count/`):
`adv-cells.txt` (the 21 cells, class, cited-line presence), `counts.txt` (the three committed counter outputs + my rerun),
`witness-battery-at-tip.txt` (full stdout of the rerun). Commands are printed with each number.

---

## 1. The 21 `adv` cells — independent recount

Method: for each `MUTANTS` tuple read the cited `file:line` in the pinned tool (tools unedited: `plans/anchor_digest_check.py`
`11bb2cad…`, `plans/ledger_tip.py` `853bcb2a…`, `plans/order_check.py` `948d5e1d…`, matching `PINS`), then ask whether that
cited text, read literally, states the rule the `old -> new` replacement breaks. Classes:

- **direct** — the cited text itself states the broken rule; a reader of that sentence calls the mutant a defect.
- **indirect** — the cited text is contract prose, but the broken rule needs a second line (code statement/comment, limit
  note, usage block) or one inference.
- **not-advertised** — the cited text is *satisfied by the mutant* (the reference is the deviating side), or the mutated rule
  is nowhere in it.

The advertised surface is what the counter names as the contract (`plans/round40_c1_verify.py:12-13`: "each tool's own
docstring, which is the contract the lane cites for it (`SKILL.md` gate/probe registry rows, `corpus/QUALITY.md` Q27/Q30)").

| id | cited (as frozen) | surface | class | the rule vs the mutated byte |
|---|---|---|---|---|
| A01 | `anchor:88-89` | docstring | direct | "exactly 64 lowercase hex digits" vs `HEX64` widened to `A-F` |
| A02 | `anchor:84-85` | docstring | direct | "8-63 lowercase hex digits" vs floor 8→1 |
| A03 | `anchor:84-85` | docstring | direct | same sentence, ceiling 63→64 |
| A06 | `anchor:31` | docstring | direct | the census regex `^ {0,3}` is quoted verbatim; `{0,3}`→`{0,4}` |
| A08 | `anchor:81` | docstring | direct | "always a defect, whatever its value" vs the branch disabled |
| A09 | `anchor:34-35` | docstring | direct | "does not have 11 cells is a `row-malformed` defect" vs `!=`→`<` |
| A15 | `anchor:55` | docstring | not-advertised | "matched **exactly**" is true of the mutant; ambiguity ("bind nothing") is only the code comment `:336` |
| A17 | `anchor:74` | docstring | direct | "`--evidence-ref index` reads the index blobs" vs `ref == "index"`→`"head"` |
| A21 | `anchor:44-46` | docstring | not-advertised | both views accepted holds for every uppercase-free manifest; `.lower()` (`:250`) is not named, and `:117-119` argues *against* case-insensitive comparison |
| A22 | `anchor:44-46` | docstring | direct | the manifest-entry view the sentence names is deleted (`if False: pass`) |
| A27 | `anchor:96-98` | docstring | direct | "is `capture-unanchored`" vs `defects.append`→bare expression (silent) |
| L01 | `ledger:23-25` | docstring | direct | "`2` usage/clone/setup refusal" vs `refuse()` `SystemExit(2)`→`(1)` |
| L05 | `ledger:20-21` | docstring | direct | "every open row whose check passes" vs `agree = ok` |
| L06 | `ledger:23-24` | docstring | not-advertised | "`0` no mismatch" is what the mutant prints on an empty ledger; the reference's `rows and` (`:250`) is the deviation (see CX1) |
| L11 | `ledger:58` | docstring | direct | "must not exist" vs the existence refusal disabled |
| L14 | `ledger:228` | code comment | indirect | the comment states it, but it is a trailing comment on the `except Exception`; the registry row `SKILL.md:581` ("`0` every closed ledger row's check passes") is the advertisement, one inference away |
| L15 | `ledger:20-21` + `:220` | docstring + code | indirect | "every closed row whose check fails" needs :220 (unknown check → `ok=False`) to reach the mutant |
| L21 | `ledger:44-45` | docstring | direct | "REFUSE stale pin ref … (exit 2)" vs the refusal disabled |
| O04 | `order:15-16` | docstring | not-advertised | the quoted FAIL clause keys on the *detail* alone; `gate: P10 ok receipt unreadable` is therefore not a hit by the sentence, yet the fixture demands a hit (comment `:56-59` states ok⇒ran; the conjunct is code `:107`; see CX2) |
| O12 | `order:37` | docstring | indirect | "it reads every blob" only implies non-blobs are skipped; the skip is code `:126` |
| O14 | `order:26-27` | docstring | indirect | "unparseable round number" + the Usage name shape imply the exact name; the anchoring is code `:51` (`SKILL.md:590` states it directly) |

Cited-line presence: 21/21 phrases are present at the cited range (`adv-cells.txt`; `python3 -` over the clone). One
citation nit: A06's cell cites `:31` while "…agree on what a row is" wraps onto `:32` — the mutated regex is on `:31`, so the
mutation is still advertised at the cited line. Surfaces: 20 cells' first cite is docstring prose; L14's only cite is a code
comment; L15's cell adds code line `:220`.

**Recount: direct 13 · indirect 4 · not-advertised 4 (total 21).** This reproduces wave-1 `R40CritClaims` §1 exactly
(`.ufo/waves/round-40/build/R40CritClaims.md:51`), and I could not move any cell with local evidence.

Definition sensitivity, stated because the frozen artifact cannot settle it (`MUTANTS` has no directness field):
L14 is the only cell that changes bucket under a literal reading — its cited text *literally* condemns the mutant, so
"direct on the cited text" gives **14/3/4**; it is "indirect" only because the surface is a code comment. Either way the
**advertised** set is 17 (13 direct + 3 advertised-indirect + L14-as-comment via `SKILL.md:581`), and 4 cells (A15, A21, L06,
O04) are documented nowhere in the tool's contract prose. A "consequence" reading of A21 would add one to the advertised set
(18); the cited sentence does not licence uppercase manifest entries, so I keep it not-advertised.

## 2. Before → after: the count the report may claim

Measured strings (`counts.txt`):

```
# claims/control-c1-nothing.txt (freeze bbb1095)     # integrate/measure-final.txt (landing ec17216)
BATTERY fixtures=0  wrong=0 tampered=0 sidechannel=0  BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=0  survived=21                MUTANTS total=21 killed=21 survived=0
PREDICATE C1 fail   exit=1                            PREDICATE C1 pass   exit=0
```

The before is vacuous **by construction**, not by observation: the kill rule requires a fixture whose `tool` equals the
mutant's tool (`plans/round40_c1_verify.py:26`, implemented at `:492` `by_tool = {tool: [fx for fx in fixtures if
fx["tool"] == tool] …}`), so `fixtures=0` entails `killed=0` for any tool. It is a non-vacuity
control, and the claims label it "Before (do-nothing control)" (`plans/round-40-claims.md:53`).

The demonstration state at the freeze is the committed witness battery, which the freeze commit itself contains
(`git log --oneline -1 -- .ufo/waves/round-40/claims/witness-run.txt` → `bbb1095`; `git ls-tree -r --name-only HEAD --
.ufo/waves/round-40/claims/witness` lists `w_anchor.py`, `w_ledger.py`, `w_order.py`). Reproduced at the assigned tip inside
the mandated sandbox:

```
$ bwrap --dev-bind / / --ro-bind ~/.local/bin ~/.local/bin --tmpfs /run/user/1000 --proc /proc \
    --unshare-pid --die-with-parent python3 plans/round40_c1_verify.py --lane . \
    --battery-dir .ufo/waves/round-40/claims/witness --work /fast/scratch/.../r/w1     # cwd = clone @ ec1005a2
BATTERY fixtures=9 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=7 survived=14 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)          exit=1
killed by: A27 w-a27-second-url · L01,L21 w-l21-control-stale-master · L11 w-l11-work-exists ·
           O04 w-o04-p10-ok-excuse · O12 w-o12-gitlink · O14 w-o14-claims-name-suffixed
```
(`witness-battery-at-tip.txt`; 14 `SURVIVED` lines, identical to the committed `claims/witness-run.txt`.)

Class accounting of that 7/14 split (counts from §1): the 7 killed = 4 direct (A27, L01, L11, L21) + 2 indirect (O12, O14) +
1 not-advertised (O04); the 14 survivors = 9 direct + 2 indirect (L14, L15) + 3 not-advertised (A15, A21, L06).

**Numbers the report may claim**

| quantity | freeze `bbb1095` | landing `ec17216`, measured at `ec1005a2` |
|---|---|---|
| default-battery fixtures / killed / survived | 0 / 0 / 21 (non-vacuity control) | 21 / 21 / 0 |
| committed witness battery, killed / survived | 7 / 14 (9 fixtures) | 7 / 14 (reproduced) |
| advertised mutants (of 21) | 17 (13 direct) | 17 (13 direct) |
| advertised demonstrated by any committed fixture | 6 | 17 |
| advertised **open** | **11** | **0** |
| not-advertised mutants (A15, A21, L06, O04) open | 3 | 0 |

So: `killed 0 → 21`, `survived 21 → 0`, promoted mutants **14**, promoted **advertised** behaviours **11**. A sentence of
the form "21 advertised behaviours were undemonstrated before this round" is false twice — 4 of the 21 are not advertised
behaviours, and 7 were already killed by committed fixtures at the freeze. The honest form is: "21 frozen mutants killed by
the default battery (0 → 21); 17 of them advertised behaviours (13 directly), 11 of those advertised behaviours newly
demonstrated; the other 4 test reference behaviour the contract does not state."

Does the witness kill change the before? It does **not** change the printed control (`control-c1-nothing`) — that run has no
fixtures. It **does** change the honest before for demonstration (0 → 7 killed, 17 → 11 advertised open) and it falsifies
every unqualified "no committed fixture demonstrates" sentence, including the counter's own abstract.

## 3. Lesson and SCORECARD wording against the count

- **Lesson (`corpus/lessons/round-40.md:11-14`)** — "the pre-freeze witnesses kill A27, L01, L11, L21, O04, O12, O14 in
  their declared directions; the anchor and ledger tip fixtures kill none of the other 14". Accurate: it names exactly the
  7 my rerun reproduces and 21−7 = 14. The lesson carries **no** advertised count and no directness mix, so it cannot be
  used to recover the 17/13/11 numbers; it is silent, not wrong. Its "every mutant declares one [direction], and every one has
  a pre-freeze witness" is consistent with the `witness` cells and does not claim advertisement.
- **SCORECARD (`SCORECARD.md:1460`)** — "Advertised count (wave-1 `R40CritClaims` §1): 13 direct + 4 indirect = 17
  advertised of 21; 17 → 0 undemonstrated by the standing counter". This is the only landed line that states my count, and it
  is right: 13/4/4, 17 advertised, and "by the standing counter" is the correct scope (at the freeze the default battery had
  zero fixtures). Two wording residues: (a) its before string is the vacuous `fixtures=0` control, with no mention that the
  committed witness battery already killed 7 — the row's "before" therefore reads as an absence of demonstration when it is
  an absence of fixtures; (b) its axis label "advertised-vs-demonstrated mismatch count" over a 21-mutant list invites the
  reading 21; the row's own arithmetic (17) is the one to keep.
- **Frozen, cannot be fixed, must be recorded as limits.** Counter abstract
  (`plans/round40_c1_verify.py:2-3`): "the behaviours … advertise that no committed **fixture** demonstrates" — false: the
  same commit `bbb1095` ships 9 witness fixtures that demonstrate 7. Counter `:15`: "its `adv` cell quotes the advertising
  sentence" — false for L14 (code comment) and for L15 (`:220`). Claims title (`plans/round-40-claims.md:23`) repeats "no
  committed fixture demonstrates", and `:30-31` asserts "each one advertised behaviour … quotes the sentence" for all 21.
- **Landed, not frozen.** `SKILL.md:625-626` (round-40 registry addendum): "21 frozen mutants, each `adv` cell quoting the
  tool's own docstring with file:line" — false for the same two cells. Smallest safe correction: "…quoting the tool's own
  docstring (or, for L14/L15, the code line that states the rule) with file:line".

## 4. Counterexamples with receipts

**CX1 — L06's kill asserts the exit code the contract assigns the other way.** Fixture
`plans/battery40/l_rows.py:53` is `{"fid": "l_rows-empty-ledgers", "tool": "ledger", "expect": "reject"}`; the measurement is
`observed_rc=1` (`integrate/measure-final.txt`). The advertised map is `plans/ledger_tip.py:23-24`: "`0` no mismatch · `1` a
ledger row genuinely disagrees", and `SKILL.md:581`: "`0` every closed ledger row's check passes at the tip and no open row
passes". Empty ledgers have no mismatch and no open row: both advertisements give **0**. The mutant (`return 0 if mism == 0
else 1`) is contract-conformant; the reference's `rows and` guard (`:250`) is the unadvertised behaviour the fixture
enshrines. The counter counts this as a kill of an advertised behaviour; it is a kill of the reference's extra guard.

**CX2 — O04's kill asserts a hit the FAIL clause excludes.** Fixture `plans/battery40/o_gate.py:47-49` commits
`gate: P10 ok receipt unreadable` and expects `hit:gate-p10`; the FAIL clause (`plans/order_check.py:15-16`) is "a gate `P10`
line whose detail is anything other than `receipt unreadable`" — that line's detail *is* the excuse, so by the sentence it is
not a hit. The `DEFECT` conjunct lives only in code (`plans/order_check.py:107`), and the adjacent comment `:56-59` names
"`P10 ok …`" as evidence the probe ran — the tool's two prose surfaces disagree. The battery's own docstring asserts the code's conjunct as the
advertised rule (`plans/battery40/o_gate.py:6-8`: "only a DEFECT line may carry the executed-nothing excuse").

**CX3 — the frozen abstract falsifies itself.** `plans/round40_c1_verify.py:2-3` says no committed fixture demonstrates the
listed behaviours; `claims/witness/` in the same commit contains 9 fixtures that run through the same counter and kill 7
(reproduced above).

**CX4 — A06's cite is one line short.** Cell cites `anchor:31`; the "agree on what a row is" clause is on `:32`. The mutated
regex is on `:31`, so the classification is unaffected; the citation is.

**CX5 — a not-advertised kill can be counted as advertised only through a gloss.** A15's cell appends "(an ambiguous slug
binds nothing)" and A21's "(a manifest entry is read case-folded)"; neither is tool prose at the cited line (A15's rule is
the comment `:336`; A21's is `:250` plus `SIDECHANNEL`-free normalisation). `R40CritClaims` said this; my recount confirms it.

## 5. Impacted axes and the smallest safe corrections

- **calibration (primary)**: the denominator is 17 advertised (13 direct), not 21; the freeze baseline is `killed=7
  survived=14`, not `killed=0`; the new advertised demonstrations are 11. SCORECARD already carries 17/13; add "11 open at
  freeze" and the 4 not-advertised names, and call `control-c1-nothing` a non-vacuity control (one sentence in the wave-2
  outcome block; no number changes).
- **depth**: three landed prose surfaces state something false about the frozen artifact — counter abstract, claims title,
  `SKILL.md:625-626`. The two frozen ones become limits in the lesson/SCORECARD; the SKILL addendum gets the L14/L15 clause.
- **operability**: L06 and O04 fixtures encode reference behaviour the documented contract contradicts. For the frozen
  counter this is a limit ("the kill rule tests the reference, not the advertisement"); the cheapest safe correction is to
  exclude L06 and O04 from the *advertised* denominator (already done by the 17) and to say so beside
  `plans/battery40/l_rows.py` / `o_gate.py` in the next round's battery, not to edit a frozen tool or a frozen counter.
- No tool, counter, fixture or lane file was edited by this seat; nothing was installed; no process left running.

---

VERDICT: c1-count-direct-13-indirect-4-unadvertised-4
