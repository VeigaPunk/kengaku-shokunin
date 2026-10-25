# R29a2CritClaimC2 — critic, claim C2 (adoption gate capability + selftest)

## Revision banner — the object changed while under review

At lane HEAD `8c14a5d` the tool was 367 lines. Mid-review it was edited twice by other seats (367 →
401 → 424 lines), and `corpus/SOURCES.md` gained 6 lines. Those edits are not mine; I wrote only this
report. Every finding below is **re-measured against the newest snapshot**, pinned as:

```
plans/sources_adopt.py  sha256 ab594472b7577a9598cf8da50e1b537d041e42b4233adfe71f9ac39657391c64  424 lines
```

All line numbers below refer to that snapshot. The tree is still moving, so each citation also names the
anchor text (function name, case label, or code line content) so it can be re-located if numbering shifts.
Each finding is tagged with where it applies:

- findings marked **[HEAD & WT]** hold on both revisions;
- **[WT only]** are introduced by the uncommitted edits.

Baseline for every before-measurement is `1f3b0f1ec41ec297130e8944ff97968d32324632`.
All scratch in `/tmp/r29a2-c2crit/` (commands and outputs inlined below, so no citation depends on a
scratch path surviving). No production file was created, edited or deleted by this seat. No tool was
installed or upgraded; no PACMAN transaction was attempted.

Current measured state of the frozen target:

```
$ python3 plans/sources_adopt.py --selftest
CASE ... PASS  (x10)   SELFTEST cases=10 failed=0   rc=0
```

The target string is met on the current bytes. What it certifies is narrower than the claim states.

---

## Q1 — Would the selftest still pass if the tool did nothing useful?

**No at suite level — 7 of 10 cases fail against a constant-returning `check()`. Yes for 3 cases
individually.** [HEAD & WT]

Method: replace the body of `check()` with the most favourable constant — `EXIT_OK` plus
`{"staged": 1, "malformed_total": 1, ...all empty...}` (scratch `y_noop.py`):

```
$ python3 y_noop.py --selftest
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE clean-package-passes PASS
SELFTEST cases=10 failed=7
noop rc= 1
```

Seven cases die, so "does nothing" cannot reach the frozen target. The three survivors split by cause:

- **cases 6 and 7** (`prose-recheck-normalized` :328, `usedby-projected` :340) never call `check()`;
  they call `build_block()` directly. They are block-builder controls only.
- **case 9** (`clean-package-passes` :362) is satisfied by a stub that fabricates its report counters.

Per-case kill sweep on the **current** bytes (`killrule.py` against the pinned snapshot copy `base3.py`, one targeted mutant per
case): 9 of 10 cases are killed by their own mutant —

```
case1 killed=True  case2 killed=True  case3 killed=True  case4 killed=True
case5 killed=True  case6 killed=False case7 killed=True  case8 killed=True
case9 killed=True  case10 killed=True
```

`case6 killed=False` is not a kill-rule formality: it is the tautology in Q2. Case 6 is still killable by
an *unrelated* mutant (break `prose`, `len(block)`, or the token entirely), so the claim's literal kill rule
("each case can be made to fail") still holds — but case 6 is no longer a control for the property the
claim assigns it.

## Q2 — Is any case a tautology (asserts what the fixture already encodes)?

**Yes — case 6, `prose-recheck-normalized`, became self-satisfying with the uncommitted edit.** [WT only]

The case asserts `"| 2026-10-25 |" in block[0]` (`:331`). `build_block` now writes the access date into
**two** columns: `recheck` on the prose branch (`:152`) and `opened` **unconditionally** (`:153`,
`cells[8] = access_date`). At HEAD that line was guarded —
`cells[8] = access_date if not ISO_DATE_RE.match(cells[8]) else cells[8]` (`HEAD:153`) — so the token could
only come from the recheck column.

Mutant N3 — delete `cells[9] = access_date` at `:152` (normalization disabled):

```
$ python3 x_n3.py --selftest     # pinned-snapshot copy, `cells[9] = access_date` deleted
CASE prose-recheck-normalized PASS
SELFTEST cases=10 failed=0      rc=0
```

What N3 actually emits for the case-6 fixture:

```
block:        | S900 | ... | mined | 2026-10-25 | 2026-10-23 — re-verify at next release | corpus/knowledge/new.md |
col 8 opened: 2026-10-25
col 9 recheck: 2026-10-23 — re-verify at next release
prose reported: [('S900', '2026-10-23 — re-verify at next release')]
case-6 assertion '| 2026-10-25 |' in block[0] -> True
```

The recheck cell still holds prose; the case passes anyway because the assertion matches the `opened`
column. The same mutant on the HEAD bytes was **killed** (earlier sweep: `case6 ... killed=True`), which
localises the regression to the uncommitted `:153` edit.

Consequence for the frozen claim: target item **(d) "a prose-`recheck` row that must normalize to
`2026-10-25`"** is not verified by the current selftest. That is the round's re-grounding surface
(CORPUS.md rule 1: entry and Gate block must carry this round's access date), so the unverified case is
the one that matters most.

Two lesser observations [HEAD & WT]:

- **Case 4** (`four-space-not-a-row` :295) asserts `staged == 0 and collisions == []`. `collisions` is
  computed from the staged rows, so the second clause is implied by the first and can never fail
  independently. Redundant clause, not a tautological case — the case is still killed by `{0,3}`→`{0,4}`.
- **Case 9 was rewritten** by the same edit from "a clean package passes" to "a targeted append passes even
  when an unrequested row is malformed", asserting `report["malformed_total"] == 1` alongside `EXIT_OK`
  (`:362-365`). It now asserts the weakened contract described under Q3 rather than a clean-package
  baseline.

## Q3 — Is the capability distinct from `scripts/sources-census.sh`, or does it duplicate it?

**Requirement 1 is genuinely distinct. Requirements 2–4 largely restate census checks, and the
uncommitted edit narrows requirement 4 below the frozen text.** [distinctness: HEAD & WT; scoping: WT only]

Distinct, proved — cross-file staged-vs-registry collision:

```
$ scripts/sources-census.sh validate --today 2026-10-25 .../distinct/lane-shokunin
lane-shokunin  E11  S001 missing used-by corpus/x.md          # no E03: E03 is intra-file only
census rc=1
$ scripts/sources-census.sh validate --today 2026-10-25 .../twice-shokunin   # same two rows, one file
twice-shokunin  E03  S001 duplicate id
$ python3 plans/sources_adopt.py --registry .../lane-shokunin/corpus/SOURCES.md --package .../staged.md
registry=1 staged=1 collisions=1 malformed=0 duplicates=0 defects=0
  collisions: S001
gate rc=3
```

Duplicated, proved — escaped pipe is already a census finding, so the docstring's "silently produces 12
cells upstream" (`:22-25`) is not true in the fleet:

```
$ scripts/sources-census.sh validate --today 2026-10-25 .../escpipe-shokunin
escpipe-shokunin  E01  S900 fields=12
census rc=1
```

The same holds for 11-cell shape (E01), `status` enum (E07), `recheck` grammar (E09) and used-by path
(E11). The gate's real contribution on those is *timing* — refusing before the append instead of after —
and rewriting `used-by` rather than reporting it.

Requirement 4 is now contradicted by the shipped path [WT only]. `check()` scopes the refusal sets to
`--admit-ids` (`:185-215`, `scope = set(want_ids)` at `:189`), filtering `clash`, `dupes` and `malformed`.
Frozen requirement 4 says "refusal with a non-zero exit for a missing requested id, an escaped pipe, a
duplicate staged id, or a nonempty collision set" — no scoping. Measured:

```
A. unscoped, package has escaped-pipe row S901
   registry=0 staged=1 collisions=0 malformed=1 duplicates=0 defects=0 prose=0
     malformed: S901:escaped-pipe                                              rc=4   (refused)

B. scoped --admit-ids S900, escape is on unrequested S901
   registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
   wrote out.md rows=1                                                         rc=0   (ACCEPTED)
   emitted: | S900 | ok | docs | B | s | a | teaches one | mined | 2026-10-25 | 180d |  |

C. scoped --admit-ids S900, unrequested S001 collides with the live registry
   registry=1 staged=2 collisions=0 ...                                        rc=0   (ACCEPTED)

D. scoped --admit-ids S900, unrequested S902 duplicated in the package
   registry=0 staged=3 duplicates=0 ...                                        rc=0   (ACCEPTED)
```

So all three refusal reasons in requirement 4 evaporate on the CLI path, and the block is still written.
This is the only finding in this review that is not a wording nit: `--admit-ids` is the path every
adoption round uses, and on it the gate refuses nothing except a missing id.

Provenance nuance on requirement 1 [HEAD & WT]: the claim says the gate uses "the census parser's own ...
anchor". It copies it — `sources_adopt.py:33` and `adoption_check.py:33` are byte-identical literals, and
the census is gawk (`sources-census.sh:573`, clause comment `:40`). Three authorities for one clause; see
impacted axes.

## Q4 — Is the before-state really absent at `1f3b0f1ec41ec297130e8944ff97968d32324632`?

**Yes, for the file and for the capability.** [HEAD & WT]

```
$ git cat-file -e 1f3b0f1...:plans/sources_adopt.py
fatal: path 'plans/sources_adopt.py' exists on disk, but not in '1f3b0f1...'   exit=128
$ git cat-file -e 1f3b0f1...:plans/adoption_check.py                            exit=128
```

No baseline script carries the logic: `git show 1f3b0f1...:plans/round28_census.py | grep -ni
"collision|staged|adopt|used-by"` prints nothing (its header reads "Read-only round28 counters"). Combined
with the Q3 measurement that the fleet census has no cross-file collision check, the absence is of a
capability, not merely of a filename. This part of the claim is sound.

## The one uncatched mutation

**N3 — `build_block`, `sources_adopt.py:152`: delete `cells[9] = access_date` (prose-`recheck`
normalization).**

Survives **all ten** cases: `collision-zero-indent`, `collision-one-space`, `collision-three-space`,
`four-space-not-a-row`, `escaped-pipe-refused`, `prose-recheck-normalized`, `usedby-projected`,
`duplicate-staged-id`, `clean-package-passes`, `missing-requested-id` — `SELFTEST cases=10 failed=0`, rc=0.

Harm: the gate then writes a registry row whose `recheck` column holds free prose
(`2026-10-23 — re-verify at next release`), which is exactly the defect capability 3 exists to prevent, and
the round's frozen case (d) waves it through. Census E09 would catch it only after the append, i.e. after
the row is committed.

Root cause, one line (the same gap produces two further surviving one-token mutants — `cells[7]` `"mined"`
→ `"queued"` and deletion of the `status not in STATUSES` branch — which I do not claim separately):
`build_block`'s output is asserted by column *content* only for `used-by`; every other column is asserted
by a bare substring, and now two columns carry the same token.

## Separate defect found while testing (not a mutation)

**The zero-entry path emits a row that the gate and the fleet census both accept, bypassing the `—`
sentinel.** [HEAD & WT]

`build_block` sets `used_by = ", ".join(admitted_entries)` with no fallback (`:145`) and `main()` requires
`--access-date` but never `--entries` when `--admit-ids` is given:

```
$ python3 plans/sources_adopt.py --registry reg.md --package pkg.md \
      --admit-ids S900 --access-date 2026-10-25 --out block.md
registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0
wrote block.md rows=1                                                   rc=0
$ cat block.md
| S900 | fixture source | docs | A | fixture scope | anchor text | fixture teaches | mined | 2026-10-23 | 180d |  |
$ python3 plans/sources_adopt.py --registry reg.md --package block.md   # re-accepts its own output
registry=0 staged=1 ...                                                 rc=0
$ scripts/sources-census.sh validate --today 2026-10-25 .../emptyused-shokunin   # mined + EMPTY used-by
emptyused-shokunin  ok .../corpus/SOURCES.md                            rc=0
$ scripts/sources-census.sh validate --today 2026-10-25 .../dashused-shokunin    # mined + '—'
dashused-shokunin  W03  S900 mined but unused
```

W03 keys on the `—` literal, so an empty cell is invisible. This is the only path I found where the gate
writes a row whose defect nothing in the fleet detects.

## Impacted axes

- **operability (primary):** requirement 4 does not hold on the `--admit-ids` path (B/C/D), and the gate
  can write a census-clean but semantically empty row. A standing gate that accepts an escaped pipe on the
  path every round uses is not yet a gate.
- **coverage (causal to C1):** frozen case (d) no longer tests normalization (N3), so the re-grounding duty
  is unverified at exactly the point C1 depends on; and `build_block` is the only writer of the
  `status`/`used-by` cells that C1's `rows_mined=5` reads.
- **identity / claim fidelity:** the frozen claim's requirement 4 and its case (d) both describe behavior
  the working tree does not have. Either the code or the claim text must move; as it stands a reader
  verifying C2 against its own text gets a false green.
- **maintainability:** the 0–3-space anchor lives in three places (`sources_adopt.py:33`,
  `adoption_check.py:33`, gawk `sources-census.sh:573`); `adoption_check.py` has no selftest, so its copy
  is unguarded.
- **Not harmed, measured:** no-op tool cannot pass (7/10 fail); per-case kill sweep 9/10 killed; baseline
  absence real (128/128); cross-file collision genuinely distinct.

## Smallest safe correction

1. **Case 6, assert by column, not by substring** (`:328-333`): read the recheck cell positionally —
   `block[0].split("|")[10].strip() == "2026-10-25"` and `2026-10-23` absent from that cell. Two lines;
   kills N3; leaves the unconditional `opened` rewrite (`:153`) free to serve the re-grounding duty.
2. **Do not scope corruption by `--admit-ids`** (`:185-215`): keep `defects`/`prose` scoped (age-related,
   legitimate) but leave `clash`, `dupes` and `malformed` unscoped. Restores frozen requirement 4; a
   collision or escape in the package means the package is corrupt regardless of which row is requested.
3. **Sentinel fallback** (`:145`): `used_by = ", ".join(admitted_entries) or "—"`, and `parser.error` when
   `--admit-ids` is non-empty and `--entries` is empty. Closes the census-blind zero-entry path.
4. Optional: one assertion on the emitted `status` cell
   (`block[0].split("|")[8].strip() == "mined"`) kills the two disclosed same-root mutants.

## Verdict on C2

Requirement 1 (cross-file collision) is a real, baseline-absent capability and the one thing the census
cannot do. The frozen target string and the case-level kill rule both pass on measured bytes. But
requirement 4 does not hold on the CLI path, frozen case (d) no longer tests normalization, and the
gate can emit a row that escapes every downstream check. Those are two assertion fixes and one filter
change — not a rejection of the capability, but C2 should not be read as "ten independent controls"
until case 6 is asserted by column.
