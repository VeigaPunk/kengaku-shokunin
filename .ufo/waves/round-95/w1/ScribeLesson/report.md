# ScribeLesson — seat report (kengaku round 95, wave 1)

Leaf scribe seat. **Drafts only — I did not edit any lane file.** The lane was read-only
throughout: `git rev-parse` / `log` / `show` / `cat-file` / `ls-tree` / `diff` /
`merge-base` / `status`, plus one `git clone --shared` into scratch. No lane commit, no
lane push, no lane index change, no fleet-root file touched.

## What I was asked for, and what I produced

| asked | produced | file |
|---|---|---|
| a QUALITY.md criterion Q77 grounded in this round's mistake M1, shaped like Q75/Q76, with a check shown able to fail | the criterion text, its style check against Q75/Q76, and the check measured red on the bad receipt and green on the good one | `quality-criterion-q77.md` |
| a SKILL.md `## Gate/probe registry` row for `plans/round95_false_gate_census.py` (+ `plans/round95_c2_counter.py`) in the exact column shape of the `freeze-integrity` row | **two** rows (one entry point per row, as the registry does everywhere else), with every cell sourced and measured | `skill-registry-row.md` |
| a decision-table note for the grader class `serialization-schema` naming this member's report-schema edges (C06–C10, C14) | two cell amendments to the `serialization-schema` row at `SKILL.md:84` — the recipe cell (the report schema and its six decisive edges) and the receipt-pointer cell — plus the count verification and the class-cell history | `decision-table-note.md` |
| proof-read of SOURCES rows S303–S309 against CORPUS.md's SOURCES contract | the full column-by-column audit, the census run, and **no contract violation found** | `sources-proofread.md` |

Raw receipts: `receipts/`. Draft check script: `draft-receipt-rev-check.py`.

## The one substantive finding

**FINDING SL-1 — the M1 mistake receipt is detectable by a command nobody ran, and the
lane has no gate that runs it.**

`.ufo/waves/round-95/L1/mistake-M1-c2-tip-wrong-cwd.txt` is the receipt of the failed
R95-C2 census run. Its first line reads:

```
# R95-C2 census at T, cwd /home/vgpnk/Projects/shokunin HEAD 9b93fc8fbbdb53221694f1e24d6c1f6044d37d2c
```

That stamped HEAD is the **fleet root's** HEAD (`git -C /home/vgpnk/Projects/shokunin
rev-parse HEAD` = `9b93fc8f…`), one directory above the lane. It is not an object of
the lane at all:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -e 9b93fc8f…^{commit}
fatal: Not a valid object name 9b93fc8f…^{commit}          rc 128
$ git -C /home/vgpnk/Projects/shokunin cat-file -t 9b93fc8f…
commit                                                   # the fleet root's own HEAD
```

The three good round-95 receipts stamp `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239` —
the lane's measured tip — and that **does** resolve in the lane (rc 0). So a single
`git cat-file -e` separates a receipt of this lane from a receipt of the tree above it.

The round-94 lesson's M4 fix was *"one measurement per command, cwd asserted in the
receipt"*. **Round 95's M1 receipt does assert a cwd and a HEAD** — the assertion was
made and was simply never *checked*. That is the gap Q77 closes: the receipt's stamp is
the one thing a reader can resolve without trusting the receipt's prose, and nothing in
the lane resolves it.

**Effect on a verdict at T: none.** Both claims pass at T on their own instruments
(re-measured below); the M1 receipt is a filed mistake, not a claim input, and the
committed `c2-tip.txt` is the run of record. This is a standing gap in the lane's
receipt discipline, not a defect in either round-95 claim.

Scope note, stated because it matters for any gate the L1 might land: a lane-wide sweep
of every committed receipt under `.ufo/waves/` finds **13** receipts whose stamped
revision does not resolve in this lane, and **12** of them are legitimately not about
this lane — eleven are round-49 receipts of a *fixture* repository
(`/fast/scratch/hyaku/kengaku-r49/…/fixture`), and one is a round-76 receipt whose
`LANE_TIP` is a revision no longer in the lane's history. A gate must therefore be
scoped to the receipts it is offered, not to every file in the tree.

## What I measured, and what it showed

| measurement | command | result |
|---|---|---|
| the R95-C2 census at the measured tip T | `python3 plans/round95_false_gate_census.py --lane . --rev afe9c229… --work <scratch>` (from inside a clean clone) | `FALSEGATES total=14 passing=0 designated_red=14 honest=pass` / `PREDICATE R95-C2 pass` / rc 0 — **byte-identical to the committed receipt** `.ufo/waves/round-95/L1/c2-tip.txt` |
| the C1 probe at T | *not re-run by this seat* | the committed receipt `corpus/evidence/round95/vuln-probe.txt` records `mismatches=0 defects=0` over 15 cases and 105 legs; the C1 counter's committed receipt records `LEGS L1=pass … L9=pass`, `TARGET executed_rows=39 … mismatches=0 defects=0`, `PREDICATE R95-C1 pass`, rc 0. **I did not re-run the C1 probe** — each of its 15 cases takes a bwrap sandbox, and this seat's brief was drafting, not re-measuring. |
| the legacy round-79 population-ledger gate | `python3 plans/round79_c1_population_ledger.py --lane .` at F and at T | at F: 14 DEFECTS, `PREDICATE R79-C1 fail`, rc 1. At T: `DEFECTS n=0`, `PREDICATE R79-C1 pass`, rc 0 |
| the SOURCES anchor gate | `python3 plans/anchor_line_check.py --lane .` at F and at T | at F `rows=294 cited=104 … live=0 cells=0` rc 0; at T `rows=301 cited=111 captured=98 … live=0 cells=0` rc 0 — **+7 rows, +7 cited, +7 captured, no new defect** |
| the CORPUS SOURCES census | the contract's own awk commands, plus `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | 301 rows, 0 malformed, `A=271 B=24 C=6`, `mined=266 queued=8 rejected=27`, no duplicate ids, no enum violations, no missing used-by paths; the maintained CLI agrees (`kengaku rows 301 …`) |
| S303–S309 re-verified against the captures | sha256 → tracked capture; cited line → the line holding the quote; declared words → `len(quote.split())` | all seven match on all three counts; every quote is ≤ 25 words (CORPUS rule 1); all seven fetched HTTP 200 on 2026-11-05 per the round's own `capture-fetch.txt` |
| the draft Q77 check, good receipt | `python3 draft-receipt-rev-check.py --lane . --receipt .ufo/waves/round-95/L1/c2-tip.txt` | `verdict=IN-LANE` … `PREDICATE RECEIPT-REV pass`, rc 0 |
| the draft Q77 check, bad receipt | same, on `mistake-M1-c2-tip-wrong-cwd.txt` | `verdict=NOT-IN-LANE` … `PREDICATE RECEIPT-REV fail`, rc 1 |

## The SOURCES proof-read: no violation

Every clause of the CORPUS contract's Shape and Rules sections holds for S303–S309:
the ids are new and consecutive; each row has a title and a canonical pinned URL; each
`kind` is in the enum; each tier is **A** and justified (a pinned upstream source file at
a fixed commit is A's own definition, and the tier-inflation check prints nothing); each
`scope` names its topic; each `anchor` names a file:line, a located quote and a revision
(a sha256 of a byte-exact capture, *plus* the commit in the source URL); each `teaches`
carries one grounded learner benefit, and the two rejected rows carry the contract's
exact `REJECTED: <reason>; flip: <what would change the verdict>` form; `status`,
`opened` and `recheck` are in their enums; and every `used-by` path exists.

Two **observations**, neither a violation, both for the L1:

1. **`used-by` names a plan file, not a knowledge entry or lesson.** The contract's
   wording is "the knowledge entries or lessons citing the row"; S303–S307 name
   `plans/round95-cases.json`. This is the lane's convention for this benchmark — the
   round-94 rows name `plans/round94-cases.json`, and 38 mined rows across the file
   point at a `plans/` or `corpus/evidence/` path. The file also contains no S-id for
   these rows (it names the *member* and the case ids), so `used-by` here records "the
   case table this row's claim rests on". House convention, not a defect.
2. **The claims file's "sha256 equal to the table above" is loose.** Of the seven rows'
   digests, **four** are in the `frozen-instruments` table (the grader, the solution, the
   Dockerfile, the upstream bottle); the instruction's `89b1abdf…`, the test wrapper's
   `f1611da6…` and the task manifest's `9aa2bd14…` are not, because they are not
   instruments the counters read. The claims file is F-frozen and I do not edit it; the
   rows themselves carry the correct digests. Reported for the L1 to route or not.

## The class-cell history, which a reader will trip over

The `serialization-schema` cell reads `executed 3 of 10` at F and `executed 6 of 10` at T —
a jump of three for a round that admitted **one** member of the class. The cause is
declared work: `plans/round-95-claims.md:114` says the legacy
`plans/round79_c1_population_ledger.py` repair (round-94 routed defect 5) "lands as
conformance with its before/after counts in the report, not as a claim", and the C commit
resynced the whole class table against the ledger — eleven cells moved, not two. The
lane's own receipt `.ufo/waves/round-95/L1/legacy-r79-gate.txt` records 14 DEFECTS at
BASE → 0 at T, which I reproduced. No defect; a reader should know the number moved
because the table drifted, not because the round admitted three members.

## Out of scope for this seat (stated, not done)

- I did **not** re-run the C1 probe (15 bwrap cases). Its committed receipt is the
  evidence; the C1 counter's own receipt is green at T.
- I did **not** edit `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SKILL.md`,
  `plans/round-95-claims.md` or any instrument. Every draft is a text in this wave dir.
- I did **not** re-fetch the seven upstream URLs. The round's own fetch receipt (HTTP
  200 for all seven, with byte counts and digests) is the evidence of opening; rule 1's
  "Non-author verification re-opens a sample" is a separate seat's job this wave.
- I did **not** propose a lane-wide receipt-revision gate. The 13-hit scan shows such a
  gate needs a population scope, and scoping it is the L1's call, not mine.
- I did **not** repair the M1 receipt, the M4 lesson, or the round-94 wave's stale
  `S303` id draft (`.ufo/waves/round-94/w1/ScribeQuality/lesson-gate.md:101` proposed a
  supersede row also numbered S303 — never landed; S299's word count was corrected in
  place instead, which is round-94's business and is recorded in its lesson).

## Scratch discipline

One clone, one scratch root: `/fast/scratch/hyaku/kengaku-r95/ScribeLesson/`. The clone
was `git clone --shared` of the lane and was checked out `--detach` at F and at T for the
read-only comparisons; the census ran from **inside** it with an absolute `--work` under
the same scratch root; every script was run by absolute path. Nothing was written to the
lane, the fleet root, or any sibling lane. The scratch root was removed after the
receipts were copied into this wave dir.

## Honest limits of this seat's evidence

- The census re-measurement took **889 s** on this host (the brief's estimate is ~4 min);
  the census is 15 counters 8-wide and each counter re-runs the 20 W2 fixtures plus the
  10 W5 mutants. The run is slower here than the brief's estimate, and I did not
  investigate why.
- The Q77 check is measured on this host with this lane's git object store. It tests
  whether the receipt's stamp *belongs to the lane*, not whether the receipt's contents
  describe what that stamp points at. That second property is the frozen-instruments
  table's job, and Q77 does not touch it.
- The decision-table note's edge descriptions are read from the **captured grader bytes**
  and the **committed probe receipt**, both frozen at T. I did not re-run the C1 probe to
  re-derive the six vectors.
- The registry rows are drafts of an interface. They assert what each script's argparse,
  exit paths and printed lines do, as measured on this host at T; they do not assert that
  the round's claims are met, which is the claims file's business.
