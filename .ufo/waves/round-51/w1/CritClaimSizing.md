# CritClaimSizing — adversarial claim sizing for R51-C1 and R51-C2

Seat: `CritClaimSizing` (critic, leaf). Round 51, hyaku run 11. Lane `kengaku-shokunin`.
Assignment: for each claim, build the **cheapest control that skips the claimed work** and score it
with the frozen counter; report whether either reaches `PREDICATE pass`, and if one does, say which
of target/counter is wrong and why.

## Axes I named

| # | Axis | What it tests |
|---|---|---|
| A1 | **pass ⇒ surface truth** | Does `PREDICATE R51-C1 pass` require the declared surface document to have been repaired, or only that the manifest agree with itself? |
| A2 | **kill-rule enforceability** | Can the claim's own kill rule (row-count floor) fire, or is it unmeasured? |
| A3 | **probe ↔ row binding** | Is an entry's probe spec bound to the surface its row declares, or is `STALE 0` vacuous once the probe target is chosen freely? |
| A4 | **attribution vs schema completeness** | Does C2's predicate require a real owner/disposition decision, or only that two constant strings exist? |
| A5 | **disposition branch selection** | Can the ledger author choose the disposition that requires the least evidence and thereby bypass `--run-checks`? |
| A6 | **check non-vacuity** | Is a no-op command (`true`) distinguishable from a real check? |

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```
Clean clone of the lane in my scratch (`git clone --shared`). `git rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r51/CritClaimSizing/lane`.

Instrument inputs at that tip are identical to the stage-1 freeze `e07f131` — the only files that
differ are wave-spec files:

```
$ git -C lane diff --name-only e07f131cf7037e58a21db6e1f3986cf401ad257c..HEAD
.ufo/waves/round-51/build_spec.py
.ufo/waves/round-51/w1-dispatch.json
.ufo/waves/round-51/w1-spec.json
```

Frozen digests of the two documents the counters read (base state, before any of my edits):

```
5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298  PROVINCE.md
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  corpus/routed-findings.jsonl
```

## Baselines reproduce the before receipts exactly

```
$ python3 plans/round51_surfaces.py --lane .
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
STALE 0
UNVERDICTED 1
NUMBER-DRIFT 1
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
exit=1
```

```
$ python3 plans/round51_routing.py --lane . --run-checks
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
PREDICATE R51-C2 fail
exit=1
```
All numbers above are the receipt's, verbatim; `DETAIL` lines elided.

## C1 — controls scored

Fixtures are manifest/province variants passed through the counter's own `--manifest` / `--province`
overrides, so the clone's frozen files were never modified. All fixtures are reproducible from the
recipes given here.

### C1-A — the named control: PROVINCE text only, no probes

Edit: append `**ABSENT 2026-10-28**` to the Route-telemetry row (SF04), and correct the
Public-literature-registry row's `25 rows` → `170 rows` (SF14). Manifest untouched.

```
$ python3 plans/round51_surfaces.py --lane . --province ../c1/A_PROVINCE.md
ANCHORS total=19 dup=0 missing=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
STALE 0
UNVERDICTED 0
NUMBER-DRIFT 1
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
exit=1
```

**Fails, as the claim requires.** Text edits clear `UNVERDICTED` (the counter reads the row for the
date) and clear nothing else: `DRIFT` and `NUMBER-DRIFT` are computed from manifest fields only
(`e["prose"] != e["state"]`, `e["count_claim"]`), so a corrected document cannot move them.

*Incidental, but it bites the landing:* SF04's anchor is the literal
`` `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT** ``. Dating that marker in place
destroys the anchor — measured: `ANCHORS total=19 dup=0 missing=1`. The date must be appended
elsewhere in the row **and** the anchor kept intact, or the manifest anchor must change with it.

### C1-B — manifest metadata only: rewrite the reading, do not repair the row

Edit: `prose := state` for every entry (three values change: SF01/SF02/SF03), delete the
`count_claim` key on SF14, and append the SF04 date from C1-A. **No probe was run by the author; no
row assertion was repaired.**

```
$ python3 plans/round51_surfaces.py --lane . --manifest ../c1/B_manifest.json --province ../c1/B_PROVINCE.md
PROBES run=19 present=13 absent=6 errors=0
DRIFT 0
STALE 0
UNVERDICTED 0
NUMBER-DRIFT 0
ANCHOR-MISSING 0
UNCOVERED 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
exit=0
```

**Passes.** Four JSON value edits plus one appended date reach `PREDICATE R51-C1 pass`.

### C1-D — manifest only, `PROVINCE.md` untouched byte-for-byte

Edit: drop every `count_claim`; for the six absent entries set `state=present`, `prose=present`,
`probe={"kind":"paths","targets":["PROVINCE.md"]}`. **Zero PROVINCE edits.**

```
$ python3 plans/round51_surfaces.py --lane . --manifest ../c1/D_manifest.json --province PROVINCE.md
PROBES run=19 present=19 absent=0 errors=0
DRIFT 0
STALE 0
UNVERDICTED 0
NUMBER-DRIFT 0
ANCHOR-MISSING 0
UNCOVERED 0
RESOLVE observed_present=19 floor=13 verdict=met
PREDICATE R51-C1 pass
exit=0

$ sha256sum PROVINCE.md
5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298  PROVINCE.md
```

**Passes with the declared-surface document byte-identical to the base tip.** The counter's `STALE`
check is only as truthful as the probe target, and the probe target is a manifest field with no
binding to the row: pointing six probes at a file that exists turns six declared-absent surfaces
into six observed-present ones.

### C1-F — the claim's own kill rule, tested

Claim: *"the claim fails if the landing edit deletes a surface row instead of dating it (`ROWS` per
section must not fall below 9 and 10)"*. Fixture: the passing C1-B manifest plus deletion of the
SF01 row **and** its entry.

```
$ python3 plans/round51_surfaces.py --lane . --manifest ../c1/F_manifest.json --province ../c1/F_PROVINCE.md
ROWS section="## Surfaces" rows=8 entries=8 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=18 present=13 absent=5 errors=0
DRIFT 0 / STALE 0 / UNVERDICTED 0 / NUMBER-DRIFT 0 / ANCHOR-MISSING 0 / UNCOVERED 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
exit=0
```

**Passes with a surface row deleted.** The counter prints `ROWS` and never compares it to anything
(`plans/round51_surfaces.py:187-188` is the only site that touches a row count). The kill rule is
unmeasurable, so it cannot fire.

### C1 verdict on the named control

The named control **fails**; the claim is not reachable by text-only edits. But A1/A2/A3 are all
open: `pass` is reachable (C1-B, C1-D) without the row repair the claim calls its work, and the
claim's own kill rule is unmeasured (C1-F). Additionally the after-target's *"+ one new declared
surface"* is unbound — `RESOLVE` is a floor at the before count, so C1-B passes at 19 entries and
13 present with no surface added.

## C2 — controls scored

The `--ledger` override is unusable out of tree: `check()` calls `ledger.relative_to(lane)` at
`plans/round51_routing.py:77` and dies with `ValueError: '../c2/A.jsonl' is not in the subpath of
…` — a traceback, not a verdict. Controls were therefore scored by swapping the variant into
`corpus/routed-findings.jsonl` **inside my scratch clone** and running the frozen command verbatim;
the frozen ledger was restored afterwards (sha256 verified back to `39fdef1e…`).

### C2-A — the named control: `owner: kengaku` + `disposition: accepted-risk`, no checks

```
$ python3 plans/round51_routing.py --lane . --run-checks
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
  DETAIL CHECK R40-R5 has no check command
  … (10 rows)
PREDICATE R51-C2 fail
exit=1
```

**Fails** — on the ten rows whose `check` is `null`, and on nothing else. Both constant fields are
accepted: `kengaku` is in `FALLBACK_OWNERS`, `accepted-risk` is in `DISPOSITIONS`.

### C2-B — the same, plus a non-empty check on those ten rows

Edit: the ten `check: null` rows get `check: "true"`. Nothing else changes.

```
$ python3 plans/round51_routing.py --lane . --run-checks
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
exit=0
```

**Passes.** Two constant fields on 71 rows plus ten copies of the string `true`. `VERIFIED ran=0`:
the frozen command's distinguishing flag `--run-checks` executed **nothing**, because `accepted-risk`
has no branch of its own (`plans/round51_routing.py:42` is the only site naming it) — no check run,
no `close` resolution, no `next` requirement.

### C2-C — the other free branch: everything `fixed-verified`

Edit: `owner=kengaku`, `disposition=fixed-verified`, `check="true"` on all 71 rows.

```
$ python3 plans/round51_routing.py --lane . --run-checks
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=71 passed=71 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
exit=0
```

**Passes**, with all 71 checks executed and all 71 passing — because `true` exits 0. `CHECK_FAILED 0`
is satisfied by a command that can never fail.

### C2 data point that sizes the claim

The ledger's 71 rows carry **no machine-visible cross-domain owner** to attribute: every `source`
resolves inside this lane (counter: `SOURCES resolved=71 missing=0`), 41 of 71 are sourced from
`.ufo/waves/round-42/falsify`, 28 from `corpus/lessons`, and **zero rows name a sibling lane in
`class` or `note`** (`grep`-equivalent over the parsed JSON: 0 matches for
`kama|kagi|kake|kasegi|kumitate|kotoba|kaidoku|souji|tabi|mori|chousa|kotodama|tameshi`).
So for the bulk of the ledger the *truthful* attribution is `kengaku` — the same constant the cheap
control writes. The axis move therefore rests on a minority the counter cannot identify, and the
counter cannot distinguish a diligent `kengaku` attribution from a blanket one.

## Which is wrong — target or counter

**C2: the target is wrong, and it is the more serious of the two.**
"Every routed finding names its owner and disposition" is a *schema-completeness* property. It is
satisfied by two constants (C2-B). The axis (`AXES.md`: cross-domain evidence "is named with its
owner and **routed, not absorbed**") is an *attribution-quality* property. `owner: kengaku` +
`disposition: accepted-risk` on every row **is** maximal absorption, and the vocabulary renames it as
a legitimate disposition — a false-provenance rename, not a measurement gap. The claim's own field
rules make self-ownership legal for `accepted-risk` (only `routed`/`referral` must name a
non-`kengaku` owner), so the counter is behaving as written; the writing is the defect.
Secondary: `--run-checks` is opt-out by disposition choice, and a `true` check is indistinguishable
from a real one.

**C1: the target is right; the counter under-measures it.**
The target — every declared surface machine-checked at the tip — is the correct axis statement. The
counter does not reach it: `DRIFT` compares two manifest fields and never reads the row's assertion;
`STALE` is vacuous once the probe target is unbound from the row; `UNVERDICTED` has no converse (a
row carrying a dated `ABSENT` marker may be recorded `present` silently — C1-D does exactly this for
six rows); the kill rule's row floor is printed but not enforced; and the after-target's new surface
is unbound by a floor-only `RESOLVE`.

One further sizing note that lands on the *claim*, not the counter: the before receipt labels
SF01/SF02/SF03 as `DRIFT` with the reading *"the row asserts the target resolves"* — but those three
rows already carry dated `ABSENT` markers from round 25 (`ABSENT 2026-10-20`). Either the readings
are wrong (then C1's claimed work is three JSON strings, i.e. C1-B, and the rows need no repair) or
the readings are right (then the counter still cannot tell a repaired row from a re-read one).
`DRIFT 3 → 0` is not, by itself, evidence that any surface declaration became truer.

## Smallest safe corrections (each verified against the current data)

C1 — three clauses, each one condition:
1. **Bind the probe to the row.** Require at least one probe target's basename (or full path; for
   `http`, the `host:port`; for `port`, `:N`) to appear in the entry's anchored row line.
   *Verified satisfiable today:* 19/19 entries bind (`SF01…SF19` all YES with basename-or-path
   matching; the three that fail a strict full-path test — SF06, SF11, SF17 — pass on basename,
   because their rows use brace/list shorthand). This kills C1-D.
2. **Enforce the kill rule.** Fail when `ROWS` for `## Surfaces` `< 9` or `### Core` `< 10`, taken
   from the claim text. This kills C1-F.
3. **Make the absent case text-bound.** When `state == "absent"` and the row carries
   `ABSENT <ISO date>`, `prose` must be `absent`. This converts the three DRIFT entries from
   author-self-agreement into a statement about the row, and makes C1-B's flip either unnecessary
   (if the row is dated) or wrong (if it is not).

C2 — two clauses:
1. **Forbid self-accepted absorption:** `disposition == "accepted-risk"` with `owner == "kengaku"`
   is a `NEXT` violation, mirroring the existing `routed`/`referral` rule (one line at
   `plans/round51_routing.py:113`). This kills C2-B.
2. **Reject vacuous checks:** a `check` whose stripped value is `true`, `:`, `exit 0`, or that names
   no lane path, is a `CHECK` defect. This kills C2-C's branch.

If only one C2 correction is affordable, (1) is the smallest: it encodes the axis sentence directly
and needs no new field.

## Limits

- My controls edit the counters' **inputs** (manifest, province, ledger) in scratch, never the
  counters. A control that repoints a probe (C1-D) is a lie in the instrument's input data, not a
  counter bug — I report it because the counter's `STALE 0` claims to catch exactly that class of
  lie and cannot, and because the claim's own control #1 (`declare-all-absent`, entries only, rows
  untouched) is in the same "manifest-only" class.
- Endpoint state is point-in-time: `:34113` and `:8791` were absent/present as the receipt says at
  my measurement; a change there would move `STALE`, not any of my findings.
- I did not measure the wave's `prose` readings row by row; I measured that the counter cannot
  falsify a reading. Whether the 19 readings are individually right is the wave's audit, not mine.
- `REV` is the clone tip `4090c3db`; the instrument inputs are byte-identical to freeze `e07f131`
  (diff above). `PROVINCE.md` and `corpus/routed-findings.jsonl` were restored to their frozen
  digests after the C2 swaps.
- Scratch `/fast/scratch/hyaku/kengaku-r51/CritClaimSizing` removed before yield; the fixtures are
  fully specified inline above. No tool was installed.

Both named controls fail (C1-A `PREDICATE R51-C1 fail`; C2-A `PREDICATE R51-C2 fail`), but both
claims are reachable without the claimed work: C1-B/C1-D print `PREDICATE R51-C1 pass` with
`PROVINCE.md` byte-identical to the base tip (`sha256 5e00336f…`), and C2-B prints
`PREDICATE R51-C2 pass` with `VERIFIED ran=0`. C2's **target** is wrong (schema completeness renamed
as adjacency; `kengaku`+`accepted-risk` is the absorption the axis forbids and the counter accepts
it); C1's **counter** under-measures its correct target (`DRIFT`/`NUMBER-DRIFT` never read the row,
`STALE` is unbound to the row, and the kill rule's `ROWS` floor is unenforced — C1-F passes with a
surface row deleted). Neither claim may be scored `pass` as evidence of its axis move until the
corrections above land.

VERDICT: both named controls fail, but both claims are gameable — C1 passes with PROVINCE.md untouched and C2 passes with VERIFIED ran=0; C2's target (schema completeness) is wrong for the adjacency axis and C1's counter does not bind its predicate to the declared rows, so neither claim's `pass` is evidence of its axis move.
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
