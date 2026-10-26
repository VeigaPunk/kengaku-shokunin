# F40XMutLedgerOrder — near-variant mutants of `plans/ledger_tip.py` and `plans/order_check.py` (round 40, wave 2 FALSIFY)

Seat: mutation-tester (leaf). Target: the two non-anchor tripwire tools of the frozen C1 counter, attacked with
**14 near-variant mutants, none in the frozen 21** (`plans/round40_c1_verify.py` `MUTANTS`, ids A01–A27/L01–L21/O04–O14),
run against `plans/battery40` through the counter's own unedited machinery. Lane tip measured:
`ec1005a2a28bc5cfdde7723374368ed4cc956eed` (scratch clone checked out there; `git rev-parse --show-toplevel` = the
scratch clone, verified before any write). Tool pins matched the frozen `PINS` before and after every run
(`853bcb2a…` ledger, `948d5e1d…` order).

## 0. Method and provenance of every number

Scratch (deleted at the end): `S=/fast/scratch/hyaku/kengaku-r40/F40XMutLedgerOrder`. Every counter invocation and
every witness run went through the ruling's exact sandbox:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>
```

The counter ran from a **byte-identical scratch copy** (`cp lane/plans/round40_c1_verify.py $S/counter/`;
`sha256sum` both → `4d47800e3551a0c7a39217987f436ffad9d69663d5f0efc840717edfcbd4642c` for each). A driver
(`$S/counter/xmut_driver.py`, receipt copy in this directory) imports that copy and overrides **only** the module
global `MUTANTS` with the 14 near-variants below — sandbox, `exhibits()` kill rule, battery build, fixture
fingerprinting and survivor bookkeeping are the counter's own code, unedited. Old-string uniqueness (`count==1`,
the counter's `invalid` requirement) was verified for all 12 distinct `old` strings before the run
(`variants/make_variants.py` → `variants-manifest.json` here; all `old_count=1`, all variants compile).

Baseline command (frozen predicate, unmutated tools):

```
$ bwrap … python3 $S/counter/round40_c1_verify.py --lane $S/lane --work $S/run/baseline --jobs 8
PINS total=3 mismatched=0
BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 pass          # exit=0, 61 s wall  → receipts/baseline.txt
```

Campaign command (the 14 near-variants; `--only` ⇒ the counter itself prints `PREDICATE C1 n/a`, the honest label
for a non-frozen mutant subset):

```
$ bwrap … python3 $S/counter/xmut_driver.py --lane $S/lane --work $S/run/campaign --jobs 8 \
        --only XL1,XL2,XL3,XL4,XL5,XL6,XL7,XO1,XO2,XO3,XO4,XO5,XO6,XO7
PINS total=3 mismatched=0
BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=3 survived=11 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)   # exit=1 (11 survivors) → receipts/campaign.txt
```

`wrong=0` and `mismatched=0` in the campaign confirm the reference phase stayed pristine: the 11 survivors below
are battery40 coverage gaps, not harness noise.

## 1. The 14 near-variants

| id | tool | axis | mutation (one `old→new`, unique) | dir | verdict |
|----|------|------|----------------------------------|-----|---------|
| XL1 | ledger | summary counters | total line `closed={closed} observed_pass={passed}` → swapped | rc-silence | **SURVIVED** |
| XL2 | ledger | summary counters | per-ledger line `observed_pass={lpassed} mismatches={lmism}` → swapped | rc-silence | **SURVIVED** |
| XL3 | ledger | kind labels | `KIND["r34_d2"]: "pin"` → `"live"` | rc-silence | **SURVIVED** |
| XL4 | ledger | kind labels | unknown-check fallback `"unknown"` → `"live"` (`:233`) | rc-silence | **SURVIVED** |
| XL5 | ledger | REF AUDIT line | `print(f"REF AUDIT …state=match")` → `pass` (`:166`) | rc-silence | **SURVIVED** |
| XL6 | ledger | REF BIND line | `why=clone-lacks-ref` → `why=bound-anyway` (`:175`) | rc-silence | **SURVIVED** |
| XL7 | ledger | (contrast probe) | flush loop `for line in statements:` → `[:0]` (`:247`) | silence | killed by=`l_rows-open-row` |
| XO1 | order | freeze-contains-receipt | clause 1 `if git.rc(…) == 0:` → `if False and …` (`:183`) | rc-silence | **SURVIVED** |
| XO2 | order | freeze-contains-receipt | same clause, `== 0` → `!= 0` (inverted) | rc-mirror | killed by=`o_gate-claims-gitlink` |
| XO3 | order | receipt-before-claims | clause 2 `if freeze != receipt_commit and … == 0:` → `if False and …` (`:188`) | rc-silence | **SURVIVED** |
| XO4 | order | receipt-before-claims | same clause, `== 0` → `!= 0` (inverted) | rc-mirror | killed by=`o_gate-claims-gitlink` |
| XO5 | order | scan bounds | `rev-list … upto …` → `rev-list … "HEAD" …` (`:117`) | rc-silence | **SURVIVED** |
| XO6 | order | verdict labels | `GATE_P10` verdict set `(DEFECT|ok)` → `(DEFECT|ok|PASS)` (`:53`) | rc-silence | **SURVIVED** |
| XO7 | order | case-line labels | `CASE_LINE` `observed=[^\s]*` → `observed=(?:pass|fail)` (`:55`) | rc-silence | **SURVIVED** |

All 11 survivor lines print `exhibits=none` — no battery40 fixture exhibits *any* declared direction against them.

## 2. Survivors, each with a witness that the mutant really changes behaviour

The counter only parses ledger **row lines** (`^(\S+) status=… agree=NO`) and order **`ORDER HIT`/`ORDER FAIL`**
lines plus exit codes; everything else a tool prints is invisible to it. Each witness below is a reference-vs-mutant
stdout diff on an input battery40 does not contain (receipts in this directory).

**Summary counters (XL1, XL2).** The docstring advertises "and then the summary line
`rows=<n> closed=<n> observed_pass=<n> mismatches=<n>`" (`plans/ledger_tip.py:18,249`). XL1 on an all-agree clone is
byte-identical (`closed=9 = observed_pass=9`, `wit-xl1.diff`), so the witness uses the `l_rows-open-row` shape:

```
$ diff ref vs XL1 on an open-row-flipped clone          → wit-xl1-openrow.diff
-reference: rows=9 closed=8 observed_pass=9 mismatches=1
+mutant   : rows=9 closed=9 observed_pass=8 mismatches=1   (rc 1 in both)
```

XL2 corrupts every per-ledger line on the plain clone: `LEDGER corpus/defects.jsonl rows=5 closed=5
observed_pass=5 mismatches=0` → `observed_pass=0 mismatches=5` (`wit-xl2.diff`), rc unchanged.

**Kind labels (XL3, XL4).** "kind=pin the check only pins closure bytes" (`plans/ledger_tip.py:15`): XL3 prints
`R34-D2 … kind=live` for a pin row (`wit-xl3.diff`); XL4 prints `kind=live` for an unknown check
(`R34-D5 … agree=NO unknown check 'r34_d6' … kind=live`, `wit-xl4.diff`, on the `l_rows-unknown-check` shape) — an
unknown check masquerades as a behaviour check. The counter's `classes()` never reads `kind=`.

**REF AUDIT / REF BIND lines (XL5, XL6).** "`REF AUDIT ref=<ref> rev=<sha> tip=<sha> state=match`"
(`plans/ledger_tip.py:37`). Every battery40 ledger fixture clone is detached (no local branch — the counter's
`ctx.clone` of a detached clone), so the tool takes the REF BIND path and XL5 is byte-identical there
(`wit-xl5.diff` — the branch is unreached). On a clone with a local master at the tip the reference prints the REF
AUDIT line and the mutant does not (`wit-xl5-master.diff`, `ref_has_REF_AUDIT=true`). XL6 falsifies the reached
line's label: `why=clone-lacks-ref` → `why=bound-anyway` (`wit-xl6.diff`).

**Freeze-contains-receipt (XO1).** "FAIL when the freeze commit (the first commit adding <claims>) already contains
<receipt>" (`plans/order_check.py:17`). On the battery shape (claims commit, then receipt commit) XO1 is
byte-identical (`wit-xo1-basic.diff`). On a repo whose single freeze commit already carries the receipt, the
reference prints `ORDER FAIL freeze-contains-receipt … / ORDER RESULT FAIL` (rc=1) and the mutant prints
`ORDER RESULT PASS` (rc=0) — `wit-xo1-xo1.diff`.

**Receipt-before-claims (XO3).** "FAIL when <receipt> was committed before <claims>"
(`plans/order_check.py:18`). Byte-identical on the battery shape (`wit-xo3-basic.diff`). In the plain
receipt-first repo the mutant still rejects, but via clause 1 with a different label (`wit-xo3-xo3.diff`) — the
receipt file persists in the freeze tree. The sharp shape (receipt added → deleted at the freeze → re-added, so
clause 2 fires alone): reference `ORDER FAIL receipt-before-claims … rc=1`, mutant `ORDER RESULT PASS rc=0`
(`wit-xo3-xo3b.diff`). Pre-registration inversion passes unlabelled.

**Scan bounds (XO5).** "Every blob ever committed under claims_dir up to and including `upto`"
(`plans/order_check.py:116`). Byte-identical on the battery shape (`wit-xo5-basic.diff`) because no fixture commits
claims after the receipt. With a post-receipt claims blob (`gate: P10 ok receipt unreadable`), the reference scans
`commits=1` and PASSes; the mutant scans `commits=2` and prints
`ORDER HIT …post-receipt-p10.txt@…:1 kind=gate-p10` → FAIL rc=1 (`wit-xo5-xo5.diff`) — the mutant is *stricter* and
the battery cannot tell either direction.

**Verdict/case-line labels (XO6, XO7).** XO6: a claims blob `P10 PASS receipt unreadable` is invisible to the
reference and a HIT to the mutant (`wit-xo6-xo6.diff`) — the verdict alternation is untested. XO7: a claims blob
`CASE c1 observed=timeout` is a `hit:case-observed` FAIL (rc=1) for the reference and a PASS (rc=0) for the mutant
(`wit-xo7-xo7.diff`) — narrowing `observed=` to `pass|fail` loses non-pass/fail verdicts undetected.

## 3. The three kills, and what they calibrate

- **XL7** (flush loop emptied) — `killed by=l_rows-open-row`, direction `silence`, class `NO:R34-D2`: the row
  statements are the *only* ledger output the counter parses, so dropping them is caught.
- **XO2 / XO4** (clause comparisons inverted) — both `killed by=o_gate-claims-gitlink`, direction `rc-mirror`: on
  the battery's only accept fixture the inverted gate spuriously FAILs (rc 0→1), which the fixture's `expect=accept`
  catches (`wit-xo2-basic.diff`, `wit-xo4-basic.diff`).

So the harness reports kills exactly when the mutated bytes feed a parsed line or an exit code; every survivor sits
in unparsed output or an uncovered clause.

## 4. Reading for C1 admission

The frozen counter names this limit itself: "text-only mutants (summary-line counts, labels) are not in the list
because no direction here reads them" (`plans/round40_c1_verify.py:61-63`), and the claims freeze withdrew L08 for
the same reason: "minus `L08` (a summary-count-only kill; no direction here reads summary text)"
(`plans/round-40-claims.md:32-33`). This campaign quantifies that limit at the landing tip: **11 of 14 near-variants
survive, all with `exhibits=none`**, covering every axis the tasking named — summary counters (XL1, XL2), kind
labels (XL3, XL4), REF AUDIT/BIND lines (XL5, XL6), freeze-contains-receipt (XO1), receipt-before-claims (XO3),
scan bounds (XO5) — plus two order regex label classes (XO6, XO7). `killed=21` therefore measures the frozen list,
not the advertised surface; the ledger/order third of "every advertised behaviour is demonstrated" holds only for
the 21 frozen behaviours. None of the 14 is equivalent: each survivor has a non-identical witness on some input,
and none duplicates a frozen `old→new` pair. A repair would need battery40 fixtures (and counter `classes()`
extensions) that read summary/kind/REF text and o_gate fixtures for the three uncovered clauses — counter and
battery changes, out of scope for a falsify seat; nothing in the lane was edited.

## 5. Receipts (this directory), hygiene, tooling

`baseline.txt`, `campaign.txt`, `variants-manifest.json`, `wit-xl1.diff`, `wit-xl1-openrow.diff`, `wit-xl2.diff`,
`wit-xl3.diff`, `wit-xl4.diff`, `wit-xl5.diff`, `wit-xl5-master.diff`, `wit-xl6.diff`, `wit-xl7.diff`,
`wit-xo1-basic.diff`, `wit-xo1-xo1.diff`, `wit-xo2-basic.diff`, `wit-xo3-basic.diff`, `wit-xo3-xo3.diff`,
`wit-xo3-xo3b.diff`, `wit-xo4-basic.diff`, `wit-xo5-basic.diff`, `wit-xo5-xo5.diff`, `wit-xo6-basic.diff`,
`wit-xo6-xo6.diff`, `wit-xo7-basic.diff`, `wit-xo7-xo7.diff`. Witness repos and clones lived only under `$S` and
were deleted with it (`rm -rf -- /fast/scratch/hyaku/kengaku-r40/F40XMutLedgerOrder`). No writes outside this
report directory and `$S`; no lane file, lane git state or sibling touched; no pacman/install (none needed —
bwrap/git/python3 already present); no process left running; the neutralized wave-1 evidence scripts were never
executed.

VERDICT: ledger-order-xmut-killed-3/14
