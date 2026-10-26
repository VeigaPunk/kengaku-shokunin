# R40CritClaims — attack on `plans/round-40-claims.md` (frozen `8b9ed6e8…`, commit `bbb1095`)

Scope: the frozen claims' framing only. Nothing frozen was edited; no lane file, no lane index. Scratch
`/fast/scratch/hyaku/kengaku-r40/R40CritClaims` (clone of the lane HEAD `3077adb`, `git -C … rev-parse --show-toplevel`
= `/fast/scratch/hyaku/kengaku-r40/R40CritClaims/lane`), deleted at the end. Receipt of the one run I made:
`.ufo/waves/round-40/build/R40CritClaims/receipt-witness-battery.txt`.

Verdict targets: C1 as a calibration move, the meaning of its do-nothing control, the 21 `adv` cells, C2's class
novelty, separability, universal clauses, and every number that is supposed to reproduce from a committed control.

**Claim digest check.** `sha256sum plans/round-40-claims.md` → `8b9ed6e8…d1cf`, equal to the
`frozen-digests.txt` row, and the three tool digests equal `11bb2cad…`, `853bcb2a…`, `948d5e1d…` as the claims
state. Order (`git log --oneline`): `bbb1095` (freeze) → `055748f` (first probe run) → `3077adb` (wave-1 spec). The
order-of-operations sentence reproduces.

---

## 1. The 21 `adv` cells — quote exists? advertises the mutated byte?

Method: quote text read at the cited file:line (all three frozen tools), then the mutant's `old -> new` read against
what that sentence commits the tool to. `direct` = module-docstring sentence whose literal content is broken by the
mutation; `indirect` = quote present but the mutated byte is one inference or one code line away (limit paragraph,
code comment, code statement); `not-advertised` = quote present but true of the mutant as well (the mutation is
outside what the sentence commits), or the docstring licenses the mutant. **All 21 quotes exist at the cited
lines (0 phantom quotes); 19 quote module-docstring prose, 2 quote code (L14, L15).**

| id | cited | quote in source | class | why (the mutated byte vs the sentence) |
|---|---|---|---|---|
| A01 | `anchor_digest_check.py:88-89` | docstring | **direct** | "exactly 64 lowercase hex digits (… `digest-uppercase` otherwise)" names `HEX64`; `[0-9a-f]`→`[0-9a-fA-F]` |
| A02 | `:84-85` | docstring | **direct** | "its hex is 8-63 lowercase hex digits" is the bound; floor 8→1 |
| A03 | `:84-85` | docstring | **direct** | same sentence, ceiling 63→64 |
| A06 | `:31` | docstring | **direct** | quote carries the census regex `^ {0,3}` and "agree on what a row is"; `{0,3}`→`{0,4}` |
| A08 | `:81` | docstring | **direct** | "a token outside the anchor cell … always a defect, whatever its value"; rule deleted |
| A09 | `:34-35` | docstring | **direct** | "does not have 11 cells is a `row-malformed` defect"; `!=`→`<` accepts 12+ |
| A15 | `:55` | docstring | **not-advertised** | quote commits *exact* slug matching, which the mutant keeps; the mutated rule (ambiguous slug binds nothing) is only the code comment `:336`; the adv cell's gloss "(an ambiguous slug binds nothing)" is not tool prose |
| A17 | `:74` | docstring | **direct** | "`--evidence-ref index` reads the index blobs"; mutant sends index to `HEAD:` |
| A21 | `:44-46` | docstring | **not-advertised** | quote commits both capture views being accepted; the mutant removes the manifest entry's case-fold (`:250`), which the quote does not mention and `:117-119` ("a case-insensitive comparison would hide a manifest written in another case") argues against |
| A22 | `:44-46` | docstring | **direct** | mutant deletes the manifest-entry view the sentence names as accepted |
| A27 | `:96-98` | docstring | **direct** | "A capture none of the row's anchor tokens resolves is `capture-unanchored`"; `defects.append(…)`→bare `(…)` (valid statement, silent, not a syntax break) |
| L01 | `ledger_tip.py:23-25` | docstring | **direct** | "`2` usage/clone/setup refusal"; `refuse()` `SystemExit(2)`→`(1)`, and its own docstring `:92` says "exit 2, never 1" |
| L05 | `:20-21` | docstring | **direct** | "every open row whose check passes (stale self-assessment)"; `agree = (is_closed and ok) or …`→`agree = ok` |
| L06 | `:23-24` | docstring | **not-advertised** | "`0` no mismatch · `1` a ledger row genuinely disagrees" *licenses* rc 0 on an empty ledger; the reference's `rows and` guard (`:250`) is code-only, so the reference, not the mutant, is the unadvertised side |
| L11 | `:58` | docstring | **direct** | "<work>/lane (must not exist)"; the existence refusal is removed |
| L14 | `:228` | **code comment** | indirect | "a crash is an observed failure, never a pass" is a trailing comment; the module docstring `:51-54` only covers `CalledProcessError`, so the surface the claims name (docstring) does not carry it |
| L15 | `:20-21` + `:220` | docstring + **code** | indirect | the unknown-check-is-a-failure rule is the code line `:220`; the docstring forces it only by inference ("a check fails") |
| L21 | `:44-45` | docstring | **direct** | "REFUSE stale pin ref … (exit 2) the ref exists but resolves to a commit other than the one under audit" |
| O04 | `order_check.py:15-16` | docstring | **not-advertised** | the quoted rule keys on the *detail* alone ("anything other than `receipt unreadable`"), so an `ok` line carrying that exact detail is not a hit; the `DEFECT` requirement lives only in the comment `:56-59`, which the docstring contradicts. The docstring licenses the mutant |
| O12 | `:37` | docstring (limit note) | indirect | "it reads every blob under claims/" only implies non-blobs are skipped; the skip is code `:126` |
| O14 | `:26-27` | docstring | indirect | the exit-2 list names "unparseable round number"; the claims-name shape is the Usage block plus the code regex `:51` |

**Tally: direct 13 · indirect 4 · not-advertised 4.**

The claims disclose none of this. Round 39 did: `plans/round-39-claims.md:62` — "Three of the seven `adv` cells cover
their behaviour only indirectly (marked in the cell)." The frozen counter's `MUTANTS` tuple is
`(id, tool, class, direction, adv, witness, old, new)` — there is no directness field, so the receipt
(`MUTANTS … SURVIVED exhibits=none -- <adv>`) cannot show the distinction either, and the counter docstring's
"its `adv` cell quotes the advertising sentence with file:line" is false for L14/L15 (code, not an advertising
sentence) and misleading for the four `not-advertised` cells.

**Consequence for the calibration count.** Four of the 21 behaviours are not advertised at all (the mutants test
undocumented code), so a kill of A15/L06/O04/A21 demonstrates nothing about the docstring contract the claims name as
the surface. The count that is actually about advertised behaviour is 17 (13 direct + 4 indirect), and only 13 are
directly advertised.

---

## 2. Is C1 a calibration move? The before-state and the do-nothing control

The claims' definition (`plans/round-40-claims.md:30-32`): "the number of frozen mutants … that no committed fixture
kills ATTRIBUTABLY in its declared direction", with the C1 title (`:23`) "…and no committed fixture demonstrates".

**Counterexample, reproduced.** The freeze's own committed witness modules are fixtures, and they kill 7 of the 21:

```
$ python3 plans/round40_c1_verify.py --lane "$S/lane" \
    --battery-dir .ufo/waves/round-40/claims/witness --work "$S/w2"
BATTERY fixtures=9 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=7 survived=14 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```
(receipt `.ufo/waves/round-40/build/R40CritClaims/receipt-witness-battery.txt`; the committed
`claims/witness-run.txt` shows the same 7 and lists the 14 survivors).

So the before-state at freeze is **`killed=7 survived=14`**, not `killed=0 survived=21`. The committed
`claims/control-c1-nothing.txt` (`BATTERY fixtures=0`, `killed=0 survived=21`) measures an *empty battery*: under the
counter's own kill rule (fixture `tool` must equal the mutant's tool) zero fixtures entail zero kills. It shows the
predicate is non-vacuous and nothing about the tools. The claims' `:53` sentence ("the same command with no
`plans/battery40`: … `killed=0 survived=21`") is true as printed and is being used as the wrong "before".

**Framing.** Every one of the 21 was observed killable *before* the freeze, with the fixtures recorded:

- 16 by the round-39 `R5`-draft harness runs the claims cite — `out_anchor_r5.txt:41-64` kills the 10 anchor
  mutants we kept (A01, A02, A03, A06, A08, A09, A15, A17, A21, A22), `out_ledger_r5.txt:15-29` kills the 6 ledger
  mutants we kept (L01, L05, L06, L11, L14, L15);
- 5 first witnessed by the freeze's witness modules (A27, L21, O04, O12, O14) — `claims/witness-run.txt`.

So the "self-assessment" (these advertised behaviours are undemonstrated) is an *observation inherited from previous
measurements*, and the observed state already contains a kill for all 21. What the round actually changes is that the
demonstrating fixtures move from scratch harnesses into a committed battery. Under SCORECARD's calibration proxy
(`SCORECARD.md:245`) — "(a) predictions filed before the first request for every probe, (b) predictions scored
against observed at close" — C1's prediction ("each of the 21 will be killed in its declared direction by a fixture
of the same tool") is already scored at freeze for 7 of 21, and for the other 14 the capability was already
demonstrated by an uncommitted harness. A calibration reading survives only if the claims say so: the open prediction
is 14, and the axis move is *fixture commitment / operability* (a witness → battery promotion), with a calibration
rider. As written, "21 of 21 advertised behaviours are undemonstrated" is a selection statement, not a prediction that
could come out false — the list was built from the survivors §2.7 already measured.

**Smallest safe correction.** In C1's *Before* bullet, replace `BATTERY fixtures=0 … killed=0 survived=21` as the
"before" with the reproduced `killed=7 survived=14` (witness battery) and keep the empty-battery run labelled
"non-vacuity control"; in the *Self-assessment vs observed state* bullet, change "no committed fixture kills" to "no
committed **battery** fixture (`plans/battery40`) kills", state the count as 14 open / 21 frozen, and name the 16
harness kills as the prior observation that makes the list a selection. No tool, counter or fixture change.

---

## 3. C2's class against `corpus/README.md`'s coverage map

New? **Yes.** `grep -rn -i "sqlite\|database\|binary file" corpus/README.md` returns nothing; the map's TB2 bullets
name no database, binary-pair or export-of-a-database class (`corpus/README.md:261-265`). The nearest neighbours are
the round-38 "build-provenance class" (`:264`, an installed binary's stdout) and the round-39 "repository-history
class" (`:265`, a git object store), both distinguishable: db-wal's graded artefact is a JSON export whose source of
truth is a SQLite `main.db` + XOR-encrypted WAL pair, and that pair is never re-derivable from the export.

Ordinal? **Not reproducible.** The claims say (`:69`) "a sixth grader class (binary database file pair)". The map
counts *tasks*: `:265` — "A fifth instance of the same ground (5 of the 89 TB2 task graders…)", and it labels only
three classes at all (`:263` "one new executed edge class", `:264` "build-provenance class", `:265`
"repository-history class"). Six tasks, at most four named classes: "sixth … class" conflates the task ordinal with a
class ordinal, and the source the claims cite for the pilot (§5 draft of `R39PlanNext.md`) says "a sixth
Terminal-Bench 2.0 grader", not a sixth class.

**Smallest safe correction.** "the sixth TB2 task grader; a graded-state class the coverage map does not yet name
(binary database file pair + JSON export)".

---

## 4. Separability

The clause (`:99`): "Each claim's counter passes with the other's work product wholly absent."

- C2 without C1: true, and mechanically so — `plans/pkg-spec-r40.json` pins only `plans/db_wal_probe.py` and
  `plans/pkg_gate.py`; V1–V7 read the captures, spec, gate, probe, dry table, receipt, entry, SOURCES rows and
  README index. `plans/battery40`, `plans/round40_c1_verify.py` are unread.
- C1 without C2: **not stated correctly.** C2's work product is partly *inside the frozen tree C1 clones*: the
  captures, spec, probe and dry table are in commit `bbb1095`; `git show HEAD:corpus/SOURCES.md | grep -c S119` → `0`
  while the working tree has the rows (`grep -c S119 corpus/SOURCES.md` → 1; `git status --porcelain` →
  ` M corpus/SOURCES.md`). So C2's rows are uncommitted working-tree bytes at freeze and will be committed at landing,
  which is exactly the change the next sentence (`:97-99`) says an anchor fixture sees.
- The saving mechanism is real but unstated: the counter compares only exit code + the declared defect-class set,
  never the anchor summary line (`rows=`/`tokens=`), so added clean rows do not move a fixture result. The claims
  instead assert both "C2 landing changes what an anchor tip fixture sees" and "each counter passes with the other's
  work product wholly absent" — two sentences that cannot both be true as written.

**Smallest safe correction.** Replace the absolute with the mechanism: "C1 compares exit code and defect-class sets
only, never summary counts, so the S119/S120 rows do not move a fixture result; C2's gate reads only its own package.
The one coupling is that C1's anchor clone sees whatever SOURCES rows are committed at the landing tip."

---

## 5. Universal clauses

| clause | holds? | evidence |
|---|---|---|
| `:23`/`:32` "no committed fixture demonstrates/kills any of them" | **no** | the 7 witness kills above; needs "battery fixture" |
| `:99` "each claim's counter passes with the other's work product wholly absent" | **no as written** | see §4 |
| `:27` "No round has frozen a mutant list for these tools" | yes | round-39 froze `M01–M07` for `plans/pkg_gate.py` (`round-39-claims.md:25,27`), not these three |
| `:62` "The three tools are not edited this round" | yes | last commit touching any is `34158b0` (round 39) |
| `:38` witnesses "committed before freeze" | yes | `git show --stat bbb1095` lists `claims/witness/*.py`, `witness-run.txt` |
| `:38` "the R5 drafts it ran are byte-identical to the landed tools" | yes | `sha256sum R39AnchorUnion/anchor_digest_check.py plans/anchor_digest_check.py` both `11bb2cad…`; ledger both `853bcb2a…` |
| C2 `:76` counter is "V1–V7 re-pointed … no check added or relaxed" | yes | `diff round39_c2_verify.py round40_c2_verify.py` touches only docstring paths, `CAP`, `CAPTURES` digests, `SPEC_REL/SHA`, `PROBE_REL/SHA`, `DRY_REL/SHA`, tempdir prefix |

---

## 6. Numbers and provenance that do not reproduce

1. **`:38` "14 by `R39PlanNext`'s harness runs … 7 by this freeze's witness run".** The `MUTANTS` witness cells name
   `out_anchor_r5.txt`/`out_ledger_r5.txt` for **16** mutants (10 anchor + 6 ledger); L01 and L11 appear in *both*
   buckets (L01's cell cites only the harness; L11 cites both). The true first-witness split is **16 harness / 5
   here** (A27, L21, O04, O12, O14); 14+7 = 21 only because the two double-witnessed mutants are dropped from the
   first bucket. Fix: "16 witnessed by the round-39 harness (two re-witnessed here), 5 first witnessed here".
2. **`:34` "one mutant per round-39 R5 clause".** Round-39 §5's routed item **R5 is "Seat scratch hygiene: the two
   leftover seat dirs"** (`corpus/lessons/round-39-verifier-spotcheck.md` §5); the tripwire-mutation work is routed
   item **R4** ("the tripwire mutation tests — this C1"), and the claims' own Frontier step says "R5 (seat scratch
   hygiene)". `R39PlanNext.md` §2.7's "the R5 clauses" means the round-39 *R5-draft tools* (`R39AnchorUnion`,
   `R39LedgerProvenance`). As written the sentence assigns A27/L21 to a routed item about scratch directories.
   Fix: name the drafts, not the routed item.
3. **`:104` "Mined mistake (`corpus/lessons/round-40.md`)".** The path is not in the freeze commit and not in HEAD:
   `git show bbb1095 --name-only | grep -c lessons` → 0; `git cat-file -e HEAD:corpus/lessons/round-40.md` →
   absent; `git log --all -- corpus/lessons/round-40.md` → empty; `git status` → `?? corpus/lessons/round-40.md`.
   The claims cite an uncommitted draft as a frozen source. Fix: "wave-1 draft `corpus/lessons/round-40.md`
   (uncommitted at freeze)" or drop the path.
4. **`:35` "`O13` was withdrawn before freeze: its witness showed it EQUIVALENT".** No committed artefact shows the
   O13 mutant's behaviour: `claims/witness-run.txt` has 9 `FIXTURE` lines and no `MUTANT O13` line (O13 is not in
   `MUTANTS`; the counter docstring records the equivalence as a code-reading argument — "the pattern starts with
   `^` and lines are matched one at a time"). `w-o13-quoted-case` shows only that the *reference* accepts. The
   witness cannot show equivalence without running the mutant. Fix: "`O13` argued equivalent by code reading
   (`^`-anchored, line-at-a-time); its fixture only shows the reference accepts — not measured".
5. **Inherited, not in the frozen file: "the grader pins only 22 of 33 id/name/value cells"** (`R39PlanNext.md`
   §3.2; repeated in this round's dispatch headline). The capture pins **11**: values of ids 1–2 and names of ids
   3–11 (`test_outputs.py:64-80`, one assertion per cell), leaving names 1–2 and values 3–11 unpinned (22 cells). The number and its own
   parenthetical are inverted. This must not reach the entry; the entry's statement is "22 of 33 unpinned / 11
   pinned", and that is what makes `literals-never-open-db` pass 7/7.
6. **Minor, frozen:** the C2 counter's abstract still says "the frozen dry table and the seven captures" while V1
   says "the eight captured" and the claims say "8 files + SHA256SUMS"; `SHA256SUMS` lists 8 files including
   `test.sh`. Doc-only, unfixable in the frozen counter — record as a limit.

**Numbers that do reproduce** (each against its committed artefact): 21 = anchor 11 + ledger 7 + order 3 (`MUTANTS`
table, `TOTAL = 21`); 17 − L08 + 2 + 3 = 21 (`R39PlanNext.md` §2.7 list minus `L08`, plus A27/L21, plus 3 of the 4
order mutants); `cases=28 predicted_pass=8 predicted_fail=20` (dry table, last line); `cases=28 observed_pass=8
observed_fail=20 mismatches=0` and `regrade cases=28 differ=0` (receipt); `stagecheck cases=28 failed=0`
(`c2-stage-check.txt`); `checks=7 defects=4` + `P10 DEFECT receipt unreadable` (`control-c2-nothing.txt`);
`PINS mismatched=1 … invalid=11` (`control-c1-tool-edited.txt`); `tampered=0`, `nothing killed` plus the
`COUNTERFACTUAL … = True` line (`control-c1-hostile-daemon.txt`); "two exit-code directions are new"
(`round39_c1_verify.py:102` has `silence, mirror, rc-silence, rc-mirror`; `round40_c1_verify.py:103` adds
`error, rc-error` — note `mirror` was also *dropped*, unmentioned); seven `(pilot…)` cases in the dry table.

---

## 7. Defects and the smallest safe correction (ranked)

| # | defect | smallest safe correction |
|---|---|---|
| D1 | C1 title/definition universal and before-count false: 7 of 21 are killed by the freeze's own committed witness fixtures; reproduced `killed=7 survived=14` | narrow to "committed battery fixture"; before = `killed=7 survived=14`; open count 14 |
| D2 | The named C1 do-nothing control is vacuous as a before (`fixtures=0` ⇒ `killed=0` by the kill rule) | keep it as a non-vacuity control only; cite `witness-run.txt` as the before |
| D3 | C1 labelled a calibration (self-assessment vs observed) move, but every listed behaviour was observed killable pre-freeze (16 harness, 5 witness) and 7 predictions are already scored at freeze — the move is fixture commitment | label it operability/fixture-commitment with a calibration rider, or file the list before any harness run so the prediction can be false |
| D4 | `adv` cells: 13 direct / 4 indirect (L14, L15, O12, O14) / 4 not-advertised (A15, A21, L06, O04), undisclosed; no directness field in `MUTANTS`; L14/L15 quote code, not docstrings; O04/L06 docstrings license the mutant | add a `direct` field per mutant and a claims limit naming the 8; count the calibration as 17 advertised (13 direct) or 14 open |
| D5 | "a sixth grader class" not reproducible: the map counts 6 tasks and names ≤4 classes; the cited planning report says "sixth … grader" | "sixth TB2 task grader; a graded-state class the map does not name yet" |
| D6 | Separability absolute contradicted by the next sentence and by the frozen tree (C2 captures in `bbb1095`; S119/S120 uncommitted) | state the mechanism (rc + defect-class sets only, never summary counts) |
| D7 | `corpus/lessons/round-40.md` cited as a frozen source but untracked/absent from `bbb1095` and HEAD | mark it a wave-1 draft or drop the path |
| D8 | Witness split "14 + 7" vs the table's cells (16 harness, L01/L11 double-witnessed) | "16 harness (2 re-witnessed here) + 5 here" |
| D9 | "one mutant per round-39 R5 clause" collides with routed item R5 (scratch hygiene); the work is R4, and `R39PlanNext`'s "R5 clauses" are the R5 *drafts* | name `R39AnchorUnion`/`R39LedgerProvenance`, not the routed item |
| D10 | `O13` "its witness showed it EQUIVALENT" — no mutant run committed; the fixture shows only the reference | record one O13 mutant run, or say "argued by code reading, not measured" |

D1/D2/D3 are the same root (the before-state), D4 is the independent calibration-count root, D5–D10 are
provenance/ordinal defects. D1 and D4 change the headline numbers; the rest are wording.

**What I did not attack / what holds.** The kill rule's direction semantics are coherent and the `exhibits=` field
makes a mislabel visible; `A27`'s `defects.append`-drop is a valid expression statement, not a syntax break (so
"silence" is the honest direction); the pins, the pid-namespaced build, `PINS-AFTER`, `tampered`, and the one fixed
variant path are present as claimed; the three tools and both R5 drafts are byte-identical at the claimed digests; the
C2 counter is a faithful re-point (only paths/digests/names change); C2's class is new to the coverage map even
though its ordinal is wrong.

VERDICT: claims-attack-10-defects-adv-direct-13/21
