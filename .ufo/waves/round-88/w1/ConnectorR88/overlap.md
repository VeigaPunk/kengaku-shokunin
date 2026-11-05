# ConnectorR88 — sibling-overlap scan (round 88, w1)

Seat: `ConnectorR88` (connector, leaf). Read-only across sibling lanes; nothing was
written outside this directory. Scan date 2026-11-05. Sibling repos read from
`/home/vgpnk/Projects/shokunin/*-shokunin` worktrees (grep/git show only).

Scope: the three R88 mechanisms —
(a) located offline replay of the captured `fix-git` grader (R88-C1),
(b) a receipt that pins a LANE_TIP ancestor and re-runs its probe (R88-C1 L3/L6),
(c) a counter that re-derives frozen claim figures by re-running historical
    counters at their own BASE revisions (R88-C2, the Q66 executable half).

## 1. Evidence per mechanism

### (a) `fix-git` grader replay — no sibling hit

- `grep -rn 'fix-git\|fix_git\|fixgit' /home/vgpnk/Projects/shokunin/*-shokunin`
  excluding `.git`/`.jj`: every match is inside `kengaku-shokunin` itself or is an
  unrelated `evidence-prefix-git.txt` path in kotodama reports. No sibling lane
  carries the `fix-git` grader, a Terminal-Bench 2.0 capture, or a
  `harbor-framework/terminal-bench` source row (`grep -rln
  'terminal-bench\|harbor-framework' */corpus` → kengaku only).
- `kagi-shokunin/corpus/lessons/round-14.md:149` mentions "kengaku `grader.py`
  (replays hard-coded report tables)" — that is an *old* kengaku instrument
  described by a sibling connector, not a sibling mechanism, and it replays
  report tables, not a TB2 grader.
- Classification: **no mechanism exists anywhere else; R88-C1 (a) is
  fleet-first by default.**

### (b) LANE_TIP-ancestor receipt + probe re-run — closest relatives, none identical

The R88-C1 receipt contract is: a committed receipt carries a `LANE_TIP` stamp,
the counter requires it to be an ancestor of the measured revision (L3), and
re-runs the probe from the measured tree to reproduce the receipt's observation
block (L6). Sibling mechanisms found:

- **kama** — `tools/round72-receipt-tip-binding.py` (registered;
  `corpus/knowledge/receipt-tip-binding.md`): every receipt path cited by a
  round's self-record must exist at the tip, carry a `# tip=<40-hex>` or
  `# rev=<40-hex>` header, name a revision that is an **ancestor** of the tip
  (`git merge-base --is-ancestor`, lines ~62, ~424, knowledge entry lines 15,
  28), and every commit in `<rev>..<tip>` must touch only declared record
  paths. Its own knowledge file states the honest limit verbatim: "the header
  is self-declared text … A fabricated header naming a real, ancestor commit
  with a record-only delta binds" and "Not the receipt's content … Not that the
  command ran." **It never re-runs the probe** — it binds revision ancestry and
  path-delta only. Classification: **DUPLICATE of the L3 ancestor leg in
  spirit** (same `merge-base --is-ancestor` primitive, same self-declared-header
  honesty limit), **NEW-MECHANISM relative to L6** — no probe re-run exists
  there. The L6 leg (reproduce the observation block from the measured tree) is
  the part no sibling has.
- **tameshi** — `tools/receipt-revision-gate.py` (`\brev=` extraction,
  `merge-base --is-ancestor` at lines 72–73, role taxonomy
  positive/verdict/control at lines 16–22): a receipt's `rev=` must equal the
  certified revision or be an ancestor (control role). Again: binds the named
  revision, **does not re-run any probe**, and has no `LANE_TIP` stamp concept.
  Classification: **DUPLICATE of the ancestor leg only.**
- **kake** — `scripts/instrument_receipts.py` +
  `corpus/knowledge/instrument-receipts.json`: binds live gate-registry
  instruments to a committed receipt whose sha256/bytes/`--selftest`
  registration re-derive from the committed blob at the receipt's revision;
  the declared revision must be a 40-hex commit id and may be an ancestor of
  the measuring revision (docstring lines 63–69). This is a *content-digest*
  binder, not an observation-block reproducer. Classification: **adjacent,
  not a duplicate** — different claim (instrument bytes vs probe observation).
- **tabi** — `scripts/check-adjacency.mjs:216` (`LANE_TIP_FALLBACKS`) and
  `check-user-round-contract.mjs:159–204` (`LANE_TIPS` map): resolve a lane tip
  for contract checks; no receipt-stamp + ancestor + probe-rerun chain.
  Classification: **not a duplicate.**
- **kama receipt `tip=` emission** — ~20 `tools/roundNN-*.py` print
  `tip=<rev>` as receipt line 1 (e.g. `round43-registry-audit.py:48`,
  `round72-receipt-tip-binding.py` consumes the same header family). This is
  the *producer* side of the same stamp convention R88-C1's `LANE_TIP` field
  belongs to. Classification: **shared convention, not the mechanism** — kama
  stamps receipts and grades their ancestry; it does not replay a captured
  grader's observation block.
- **kaidoku** — `plans/round-78-claims.md:53-55` requires a receipt's `rev` to
  be an ancestor of the measured rev inside its gate-receipt schema check.
  Same ancestor-only shape. Classification: **DUPLICATE of the L3 leg only.**

Net for (b): the *stamp + ancestor* half exists in kama (strongest, with a
committed knowledge entry and selftest), tameshi, kaidoku and kake (digest
variant). The *probe re-run reproducing the observation block* half (L6) has
**no sibling counterpart** — every sibling mechanism stops at "the named
revision is inside the tip's history and record-only bytes moved after it."
R88-C1's L6 is the fleet-first element of (b).

### (c) before-figure re-derivation by re-running historical counters at BASE — closest relative is this lane's own Q66

- **kengaku (this lane)** — `plans/round88_claim_figures.py`: extracts every
  before-figure record from the eight frozen claims files (rounds 80–87),
  re-runs each claim's own counter at that claim's own BASE (modes `rev` /
  `tree` / `prose`), compares, and pins a frozen KNOWN-mismatch set
  (`R87-C1 kv:defects claimed==7 measured 3`). This *is* the R88-C2 mechanism;
  cited here only as the reference point.
- **chousa** — `tools/claims-audit.py` / `claims-audit-v2.py`: a rule-file TSV
  names an anchor in a frozen claims file plus a check class
  (`json-count`, `section-contains-at` which reads `git show <rev>:<path>`,
  `git-first-commit`, etc.); the checker "re-derives the fact from the
  committed bytes and flags the row when the statement is false" (docstring
  lines 9/22). This is the **nearest structural relative**: it audits frozen
  claims files against committed bytes at pinned revisions. **But it never
  re-runs a historical counter** — its `section-contains-at` class reads file
  blobs at a rev, not counter stdout; there is no "run counter X at its BASE"
  leg. Classification: **NEW-MECHANISM for the counter-rerun core**;
  DUPLICATE only of the "audit a frozen claims file" envelope.
- **kagi** — `corpus/QUALITY.md` QM34: "a plan's declared BASE values are
  executed, not estimated, before the plan freezes: every counting command in
  the plan's controls file runs against a `git archive` extraction of the
  named BASE revision." This is a *prospective* rule for the plan's own
  declared values, not a retrospective sweep over historical claims files.
  Classification: **NEW-MECHANISM** (same spirit — measure, don't estimate —
  different population and direction).
- **kaidoku** — many `tools/round-NN/c*-counter.py` take `--rev`/`--base` and
  `tools/round-44/c2-counter.py:222` "re-runs every check at BASE"; but each
  counter re-runs *itself* at its own round's BASE for its own claim — none
  extracts figures from *other rounds'* frozen claims files and re-derives
  them. `tools/round-30/axis-fit-gate.py`, `freeze-integrity.py` etc. are
  per-round instruments. Classification: **NEW-MECHANISM** — the
  cross-round, extract-from-claims-then-rerun-own-counter-at-own-BASE loop is
  unique to R88-C2.
- **tameshi** — `tools/selfstate-freshness.py:251,404-410` `extract_token`
  compares a row's figure against document scope and measured stdout; and
  `tools/defect-bind.py` binds a receipt's figure to the receipt. These
  re-derive *current* self-assessment figures against live instrument output,
  not historical claims at their BASEs. Classification: **NEW-MECHANISM**.
- **kumitate** — `corpus/lessons/round-72-verifier-spotcheck.md:90` documents a
  BEFORE-checklist figure drift defect (the same *class* of bug R88-C2's KNOWN
  set records), but it is a lesson, not an instrument. Classification:
  **motivation only, no mechanism.**
- **kengaku `corpus/QUALITY.md:1356-1363`** already carries Q66 with the
  executable-half pointer to `plans/round88_claim_figures.py` — the design is
  this lane's own; no sibling QUALITY.md has a Q66-equivalent row (verified:
  `grep -n 'Q66' */corpus/QUALITY.md` shows unrelated Q66s in kama, kotoba,
  kumitate, souji — different numbering spaces).

Net for (c): **R88-C2 is fleet-first.** The only near-relative is chousa's
`claims-audit` (frozen-claims-file auditing envelope, no counter re-run) and
kagi's QM34 (prospective BASE-value execution, no historical sweep).

## 2. Classification summary

| # | Mechanism | Closest sibling | Class |
|---|---|---|---|
| a | located offline replay of `fix-git` grader | none (kagi r14 lesson cites old kengaku `grader.py`, different target) | NEW-MECHANISM, fleet-first |
| b-L3 | receipt stamp is ancestor of measured rev | kama `round72-receipt-tip-binding.py`; tameshi `receipt-revision-gate.py`; kaidoku r78 gate-receipt rev check; kake `instrument_receipts.py` (digest variant) | DUPLICATE (ancestor leg exists) |
| b-L6 | re-run probe from measured tree, reproduce observation block | none — every sibling stops at ancestry/content-digest | NEW-MECHANISM, fleet-first |
| c | extract before-figures from frozen claims files, re-run each claim's counter at its own BASE, compare to frozen KNOWN set | chousa `claims-audit*.py` (claims-file audit envelope, blob reads not counter reruns); kagi QM34 (prospective); kaidoku per-round `--rev/--base` counters (self-only) | NEW-MECHANISM, fleet-first |

## 3. Fleet-first and shared-standard ownership

- **Fleet-first instruments:** R88-C1's replay counter + probe (a, b-L6) and
  R88-C2's `round88_claim_figures.py` (c) are all fleet-first; no sibling lane
  holds any of the three mechanisms.
- **Shared-standard candidate:** the *receipt-revision binding* convention —
  `tip=`/`rev=` 40-hex header + `merge-base --is-ancestor` + record-only-delta —
  is already a de-facto fleet standard owned by **kama**
  (`tools/round72-receipt-tip-binding.py` +
  `corpus/knowledge/receipt-tip-binding.md`, with the most complete exit map,
  selftest, and an honest-limit write-up). tameshi's
  `receipt-revision-gate.py` and kaidoku's round-78 gate-receipt rev check are
  the same family. If a shared standard is wanted, **kama is the owning lane**;
  R88-C1's L3 leg is a lane-local instance of that convention, not a candidate
  to replace it. The L6 observation-reproduction leg has no standard anywhere
  and would be a kengaku-originated candidate if the fleet ever wants one.

## 4. Contradictions / notes for L1

- None of the frozen elements looked wrong; no predicate, target, case table,
  control set, kill rule, leg list or KNOWN set was touched.
- Honest-limit parity: kama's knowledge entry and R88-C1's claims file both
  state that a self-declared ancestor stamp does not authenticate content —
  the two mechanisms share the same ceiling, stated independently. Not a
  defect; noted so the round report does not overclaim L3 as stronger than it
  is.
- `kengaku` is the only lane whose `corpus/SOURCES.md` carries a
  `terminal-bench`/`harbor-framework` row; sibling scans for (a) are therefore
  exhaustive by construction (no sibling could replay a grader it never
  sourced).
