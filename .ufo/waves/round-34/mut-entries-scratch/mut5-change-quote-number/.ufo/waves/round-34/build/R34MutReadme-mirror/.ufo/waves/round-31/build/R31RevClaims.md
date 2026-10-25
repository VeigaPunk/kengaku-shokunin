author: R31RevClaims (reviewer, leaf; no subagents, no lane edits)
round: kengaku 31 (hyaku run 6, attempt 1)
date: 2026-10-25
scope: sizing + falsifiability review of the frozen claims in `plans/round-31-claims.md` against
`/home/vgpnk/Projects/shokunin/AXES.md` and the fleet claim-sizing rules (`.ufo/prompts/kengaku-round-31.md`
§6 item 9, operator rulings 2026-10-25). Read-only over lane bytes; every control below ran in
`/tmp/r31-claims/`. Nothing under the lane repo was created, edited or deleted except this file.

Baseline measured: lane tip `0883e72ef8474ca42ac1a54eb0273079f1507035` (local = remote, `ahead=0`,
`head=detached`). Counter bytes at review time are **live and untracked**:
`plans/round31_defects.py` sha256 `370913781baf142d7b565afde544728fff46c7c6566673b273b6c4eefb22e950`
(mtime 05:53:39), `plans/sources_adopt.py` sha256 `39ba62b22915bdcf6943dc2a860bd338a77cbd1d9b92064ab75edd54cda9bc71`
(mtime 05:55:10). Both changed after the claims file was written (05:45) — see §Must-change item 3.

# VERDICT lines

VERDICT: C1 — one-command after-state holds, but the frozen counter is content-blind: a 7-line
metadata-only stub with three stub registry rows prints the frozen pass line and exits 0 (reproduced).
The do-nothing control is red (exit 1, reproduced), so the letter of the control rule is met and its
intent is not. Coverage label is defensible (frontier → core on a surface the map names open); the
kill rule's "two of three survive" branch is unreachable by the frozen predicate.

VERDICT: C2 — one-command after-state holds and the before-state is re-derivable from committed bytes
(`defects=10`, exit 1 on `0883e72`, reproduced). Two defects: the prose claims "§5 items 1–8" while no
check covers §5 item 7 (report ordering), and 2 of the 10 counted items are copyedit (quality), not
self-assessment/repo mismatches, so the calibration count is 8, not 10.

VERDICT: C3 — best-sized of the three: target is one printed line + exit 0, the three new cases assert
exit 8 and 9 through the same `quote_check()` the CLI calls (a blanket-refusal cheat is blocked by the
accept case), and the do-nothing control is verified red (`cases=14`; `--url-map` → argparse exit 2).
Gap: the counting command prints totals only, so the three CASE labels must be in the receipt.

Axes distinct: yes (coverage / calibration / operability, one claim each). Lowest non-retired axis
obligation: met by C1 (coverage 7, tied with novelty 7; waiver unavailable, novelty 7 < saturation 8).

# (a) One concrete after-state, re-derivable with one command

| claim | after-state as frozen | re-derivable with one command? | caveat that survives the freeze |
|---|---|---|---|
| C1 | printed `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` **and** exit 0 (`plans/round-31-claims.md:30-36`) | **yes** — `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` | the command reads **worktree** bytes (`lane / rel`, `adoption_check.py:70`), not `git show <commit>:<path>`; "over committed bytes" is true only with a clean tree, so the measured commit must be accompanied by `git status --porcelain` |
| C2 | `defects=0`, exit 0 (`:56-63`) | **yes** — `python3 plans/round31_defects.py --lane .`; prints `checks=10 defects=N` | same worktree read for R1–R8/R10 (`read()` on `lane/path`); only R9 reads `HEAD:` and `git status` |
| C3 | `SELFTEST cases=17 failed=0`, exit 0 (`:84-90`) | **yes** — `python3 plans/sources_adopt.py --selftest`; already prints `cases=17 failed=0` exit 0 in the live tree | the three new cases are named in the predicate but the counter prints only the total; the receipt must paste the three `CASE` lines |

Same-sentence / same-condition / same-label (kumitate r42) is only partly satisfied for C1. The
predicate names four conditions the printed seven fields do not label:
`verified-at: 2026-10-25`, "exactly the three ids" (set equality), "three distinct", "one index row"
(uniqueness + non-empty cells). All four are implemented as exit-code gates
(`adoption_check.py:121-152`: `verified_at_ok`, `ids_ok`, `duplicates_ok`, `opened_ok`,
`index_shape_ok`) and none is printed. A closure reading the receipt line cannot see them; it must
trust exit 0. That is a label gap, not a predicate error — and it is not fixable inside the freeze
(the printed-field set is part of the frozen predicate, unchanged from rounds 29–30).

# (b) Universal clauses that need enumeration

1. **C1 kill rule vs predicate — a contradiction.** `plans/round-31-claims.md:40-42`: "if fewer than
   two of the three survive, the entry is not admitted" — i.e. two of three is admissible. The frozen
   predicate requires `cited_rows=3` (`required = sum(len(entry["sources"]))` = 3, exit 0 only when
   `len(cited) == required`). An entry citing two sources prints `cited_rows=2` and exits 1. So the
   kill rule's admissible branch **cannot verify**: any refused row is an honest stop, not a 2/3
   admit. The report must say so; the branch is dead as written.
2. **C1 "every one of those three cited rows … status=mined, opened=2026-10-25, used-by naming the
   entry"** — a universal over 3, and it *is* enumerated: `rows_present=3`, `rows_mined=3`,
   `usedby_ok=1` (all-of over the expect file's three ids, `adoption_check.py:96-107`). Allowed.
3. **C1 "the three ids adopted this round"** — the set is not in the predicate text; it lives in
   `.ufo/waves/round-31/adoption-expect.json` (`S092`, `S093`, `S100`). Enumerated, but only via the
   expect file, which is untracked.
4. **C1's admitted entry carries its own universal negative** — the staged entry states "No task in
   either repository sets `environment_mode` or a `[verifier.environment]` section — verified by
   grepping every `*.toml` in both trees" (staged file, §The finding). The claim's counter never sees
   it, and the kill rule only locates quotes. If this sentence is admitted into core, the round must
   receipt the grep with per-tree file counts and the zero-hit output, or narrow the sentence. A
   universal negative over "every `*.toml` in both trees" is exactly the clause class item 9 forbids
   unless the counting command enumerates the full set.
5. **C2 "§5 items 1–8" — the enumeration is short by one.** §5 of
   `corpus/lessons/round-30-verifier-spotcheck.md` has 8 items. The ten checks map to items
   1,2,3,4,5 (twice: R7 + R8),6,8 = **seven** items, plus the two residues R5/R6 that §5 does not
   list. §5 **item 7 (report ordering: round-30's report commit precedes its last three lane commits;
   erratum 3 cites a three-commits-stale tip)** has **no check at all** and is not named as open.
   `R1..R10` is a closed enumeration (`FROZEN` tuple, asserted by `--selftest`), but the prose clause
   "§5 items 1–8" is a claim over eight items the counter does not enumerate. Must be restated as
   "seven of the eight §5 items plus two residues; item 7 reported open or closed by an appended
   `LOG.md` correction".
6. **C3 "three new failure-capable cases"** — enumerated by content in the predicate, printed only as
   `cases=17 failed=0`. The three labels are `quote-url-bound-accepted`,
   `quote-url-mismatch-refused`, `quote-url-unmapped-refused`; they must appear in the receipt.
7. **C3 control's "argparse exit 2"** — `EXIT_QUOTE_UNREADABLE = 2` (`sources_adopt.py:49`) is the
   same numeric code the tool itself returns for caller/env faults, so "exit 2" alone does not prove
   argparse. The committed `gate-before.txt` does carry the argparse stderr line, which disambiguates
   it; a receipt that pasted only the code would not.

# (c) Targets a do-nothing control cannot reach — and the cheaper control that does

| claim | do-nothing control | reproduced? | cheapest skip-the-work control | result |
|---|---|---|---|---|
| C1 | pre-append tree | **yes** — `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok`, exit 1, byte-identical to `.ufo/waves/round-31/claims/control-nothing.txt` (the receipt omits the exit code; I re-derived `exit=1`) | **metadata-only stub**: 7-line entry (3 `source:` lines + `verified-at: 2026-10-25` + 3 lines of prose "stub body, no reading of any harness rule"), one index row with non-empty cells, three registry rows placed inside `## Registry` with `status=mined opened=2026-10-25 used-by=<entry>`, anchors reading "stub anchor" | **prints the frozen line and exits 0**: `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` / `exit=0`. The target is reachable without reading one byte of the harness. This is the kake-r34 "junk-row commit met both counters" class |
| C2 | pre-repair tree | **yes** — `checks=10 defects=10`, exit 1 against `0883e72` (archive export; R9 red there for the missing `.git`, and separately the committed `R30DraftGate.md` blob is 199 lines with **zero** `Pass 9` occurrences, so a git worktree of the baseline also yields R9 red) | append-the-expected-string | **not separable from the repair**: R1/R2/R3/R10 *are* appended errata that must quote the superseded wording (R1 requires ≥2 occurrences plus a "correction" label plus the admitted wording). Substance is re-derived independently for R3 (registry tier `S086`), R6 (staged-file URLs vs registry), R9 (committed blob ≥100 lines + pass-9) and R10 (falsify registry member count). Control adequate |
| C3 | baseline tool | **yes** — baseline blob selftest `SELFTEST cases=14 failed=0` exit 0; `--url-map /tmp/x` → `error: unrecognized arguments: --url-map /tmp/x`, `exit=2` | add three cases that print `cases=17` without binding | **blocked**: the three cases assert `EXIT_URL_MISMATCH`/`EXIT_URL_UNMAPPED` (8/9) *and* an accept case, all through `quote_check(..., url_map=...)` — the same function the CLI dispatches to. A blanket-refusal stub fails the accept case; an ignored `--url-map` fails both refusals. Control adequate |

**C1's committed hardening precedent is misattributed and does not close the gap.**
`corpus/evidence/round30/counter-hardening-control.txt` records "the same stub now census=fail /
exit=1". Reproduced: a stub with **blank** index cells prints the pass line with `census=ok` and
`exit=1` (the `index_shape_ok` gate), and `census=fail` appears only when the census root lacks
`shokunin.conf` — which is what a `/tmp` copy without the conf produces (I reproduced that exact
`census=fail` shape before adding the conf). With a valid census root and non-blank cells the stub
passes. So round 30's "hardening" is an index-cell gate mislabelled as a census gate, and the
junk-row path is open in round 31.

# (d) Axis distinctness and the lowest-axis obligation

- C1 coverage, C2 calibration, C3 operability — three distinct axes, one claim each; no two claims
  on one axis. Pass.
- Lowest non-retired axis is **coverage 7**, tied with **novelty 7** (`SCORECARD.md:1013-1017`;
  round-30 rows: calibration 8, operability 8, depth 9, freshness 8, adjacency 8). C1 works coverage
  and carries the obligation. The tie-break ("most falsifiable with the sources an on-host tool can
  open") is a recorded lane rule (`SCORECARD.md:9-10` for round 13, restated at `:1013-1017`). Pass.
- Waiver correctly unavailable: saturation line 8 (`SCORECARD.md:569`, ratified at `:651`), novelty 7
  below it, and capability rows entered at rounds 29 and 30, so window N=4 is not exhausted. Pass.
- C1's own axis-verdict shape is honest about the cap (`:43-45`): the score stays 7 while the
  round-25 L0 cap is open and the row records a ledger delta, matching the round-24 precedent
  `7 (held by cap; counts moved)`. Pass.

# (e) Quality work mislabelled

1. **C2 carries two copyedit items inside a calibration claim.** Item 9: "A calibration claim must
   count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state."
   R4 ("the card records what each stated, not a reconciled truth" appears twice) and R5 ("populated
   (not \"unknown\")" appears twice) are prose duplication inside one entry: neither is a
   self-assessment/repo mismatch, and the claim's own prose calls them "the two copyedit residues"
   (`:51-52`). The other eight do qualify: R1 (LOG statement vs entry), R2/R3 (lesson cells vs
   registry/entry), R6 (entry's stated count vs the count re-derived from the staged file and the
   registry), R7/R8 (entry claim vs its own source rows), R9 (report claim vs tree state), R10
   (lesson seat count vs falsify registry). Honest count: **8 calibration mismatches + 2 copyedit**,
   not "mismatch count 10 → 0". The SCORECARD row must state the split; the frozen counter cannot.
2. **C1's coverage credit is real but its counter is not the evidence for it.** The surface is named
   open and the citation resolves (see below), and the entry is new ground: the staged entry closes
   axis E of `knowledge/benchmark-task-validity-checklist.md` with a per-task resolution table. So
   the *label* is defensible. But `entries=1 indexed=1 …` is index-parity bookkeeping — the same line
   a sourceless stub prints — so the row must not present the counter as proof the surface moved; the
   movement rests on the kill rule's located quotes at the three pinned commits. The entry's content
   type is source-digest (a depth signal); the coverage credit comes from the new ground, not from the
   digest.
3. **C3 creates a new calibration mismatch it does not plan to fix.** `SCORECARD.md:1024` still
   states the gate "does not bind the artifact to the cited URL", and the capability row
   (`SCORECARD.md:1035`) describes a gate without capture-to-citation binding. After C3 both are
   false statements about observed repo state. The round must update the capability row and the scope
   sentence in the same commit, or C3 lands a fresh self-assessment/repo mismatch.

# What must change BEFORE data (still possible — no predicate rewrite)

1. **Commit the freeze.** `plans/round-31-claims.md` and `.ufo/waves/round-31/` (all four control
   receipts) are **untracked** (`git status --porcelain`: `?? plans/round-31-claims.md`,
   `?? .ufo/waves/round-31/`). The freeze is asserted in prose but not dated by committed bytes, and
   wave seats have already run (`build-spec.json` 05:47, counters edited 05:53/05:55), so "frozen
   before any seat scored" is now supported only by mtime. Commit the claims and receipts unchanged —
   this changes no predicate.
2. **Build and commit the C1 skip-the-work control** with its honest result (`exit=0` on a stub). The
   rule requires the cheapest control that skips the claimed work, scored with the frozen counter,
   committed before data. It is missing from `.ufo/waves/round-31/claims/`; round 30's substitute is
   misattributed (see (c)).
3. **Regenerate the before receipts against the final counter bytes.** The committed
   `defects-before.txt` was produced by an earlier counter: on the same baseline tree the current
   `round31_defects.py` reports R6 as "the entry states no staged-source count; the re-derived count is
   2" where the receipt says "the entry still says three staged source rows are unregistered". Count
   and exit match (10 / 1); the messages do not. A receipt that no longer re-derives from the shipped
   counter is not evidence for it.
4. **Fix C1's citation pointer.** `plans/round-31-claims.md:23` cites `corpus/README.md:250` for the
   round-29 bound "Not deployment config, not runtime task validity, not contamination measurement".
   Line 250 is blank; the bound is verbatim at **`corpus/README.md:251`**. The §Frontier bullet-1
   quote at `:20-21` does resolve verbatim at `corpus/README.md:273`.
5. **Restate C2's §5 clause** as seven of eight items plus two residues, and either append the item-7
   correction (a named `LOG.md` correction naming round-30 erratum 3's stale tip `caf1e2b4` and the
   true tip `2dcf06c5`) or report item 7 as an open defect. No counter clause covers it either way.
6. **C1 report wording**: record that the kill rule's 2/3 branch is unreachable by the predicate, and
   that the counter verifies admission only. Put the three located quotes (S092/S093/S100 at the
   pinned commits, with access date 2026-10-25) in the receipt so the surface movement has evidence
   the counter cannot supply.
7. **C3 receipt**: paste the three `CASE` lines beside `SELFTEST cases=17 failed=0`, and note that
   `exit=2` for the baseline is argparse's (`gate-before.txt` carries the stderr that proves it).

# Impossible without violating the freeze — say so, do not repair

The claims file is frozen and seats have scored against it, so these cannot be changed as predicates:

- **C1's content-blindness.** Making the counter read the entry's substance (e.g. requiring the three
  quoted spans to be located in the fetched bytes) would change the counter and the label set. Not
  available. The honest handling is disclosure plus the kill-rule receipt (item 6 above).
- **C1's kill rule.** Widening "fewer than two" to "any refusal is a stop" is a kill-rule change. Not
  available; the report must state that the written 2/3 branch never verifies.
- **C2's calibration composition.** Moving R4/R5 out of the count changes the frozen ten. Not
  available; disclose the 8+2 split.
- **The printed seven-field set** (no `verified_at`/`opened`/`index-shape` labels) is frozen by
  inheritance from rounds 29–30. Not available.

# Evidence appendix (commands I ran; outputs quoted, not paraphrased)

```
# C1 do-nothing control, on an archive export of 0883e72 with a valid census root
$ python3 plans/adoption_check.py --lane . --expect adoption-expect.json --census
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
exit=1

# C1 skip-the-work control: 7-line metadata-only stub + 3 stub registry rows inside ## Registry
$ python3 plans/adoption_check.py --lane . --expect adoption-expect.json --census
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=0

# same stub, blank README index cells (round-30 "hardening" shape)
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=1
# same stub, no index row
entries=1 indexed=0 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=1
# rows appended outside ## Registry (census guard works)
kengaku	E12	S092 row outside Registry section      # exit 1
# stub root without shokunin.conf (the shape round 30's receipt records)
ERROR: config not found: /tmp/.../shokunin.conf ; census=fail ; exit=1

# C2 before-state on 0883e72 with the current counter
$ python3 plans/round31_defects.py --lane .
DEFECT R1 ... R10 (ten lines) ; checks=10 defects=10 ; exit=1
# live lane at review time (mid-round repair)
$ python3 plans/round31_defects.py --lane .
DEFECT R9 round30-seat-reports-committed: ... still differs from HEAD: M .ufo/waves/round-30/build/R30DraftGate.md
checks=10 defects=1

# baseline seat-report blobs at 0883e72
.ufo/waves/round-30/build/R30DraftGate.md lines=199 pass9=0   (worktree: 243 lines, pass9=1)

# C3 baseline control
$ python3 /tmp/r31-claims/gate/baseline.py --selftest
SELFTEST cases=14 failed=0 ; exit=0
$ python3 /tmp/r31-claims/gate/baseline.py --url-map /tmp/x --selftest
baseline.py: error: unrecognized arguments: --url-map /tmp/x ; exit=2
# C3 current bytes
$ python3 plans/sources_adopt.py --selftest
CASE quote-url-bound-accepted PASS
CASE quote-url-mismatch-refused PASS
CASE quote-url-unmapped-refused PASS
SELFTEST cases=17 failed=0 ; exit=0

# freeze status
$ git status --porcelain
 M .ufo/waves/round-30/build/R30DraftGate.md  (x2 build, x3 falsify — the five R9 files)
 M plans/sources_adopt.py
?? .ufo/waves/round-31/
?? plans/round-31-claims.md
?? plans/round31_defects.py
```

# Residual risk and verification gaps

- The three counters were **live** during this review (both .py files changed at 05:53 and 05:55).
  My C2/C3 runs are against those bytes; the C1 runs against `adoption_check.py` as committed at
  `0883e72`. A closure must re-run all three against the landed commit with a clean tree.
- `adoption_check.py` and `round31_defects.py` (R1–R8, R10) read the worktree, so a green run on a
  dirty tree proves nothing about the commit. No counter I reviewed prints a tree-clean assertion.
- C1's surface-movement evidence (three located quotes at the pinned revisions) is prose-gated by the
  kill rule; I did not fetch the three sources myself — that is C1's re-grounding duty, and its
  absence or presence is what separates an admitted entry from a stub.
- C2's R9 is red on any later rewrite of one of the five round-30 seat reports by an active seat; no
  guard pins them after the repair commit.
- C1's census leg is whole-registry, not entry-scoped: it exits 0 with 14 `W04` warnings today and
  would not notice a stub's own rows.

Tool installs: none. No package manager ran; no tool version changed.
