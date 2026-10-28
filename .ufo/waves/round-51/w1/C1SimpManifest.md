# C1SimpManifest — can `plans/round51-surfaces.json` lose fields without losing a predicate leg?

Seat: `C1SimpManifest` (simplifier), kengaku round 51, hyaku run 11.
Item: for each field in `{section, state, prose, probe, why, count_claim, resolve_floor, note}`, remove it in
scratch and show either (a) a selftest case or the real run now fails, or (b) nothing fails and the field is
dead weight. Keep/remove table with evidence; propose the minimal schema. Committed manifest not edited.

Axes I named before measuring:

- **A1 predicate-leg preservation** — does removing the field destroy or silently vacate a leg of the frozen
  C1 predicate (`plans/round-51-claims.md` §C1)?
- **A2 schema surface** — how many fields must a future round maintain to keep the same predicate?
- **A3 evidence fidelity** — does the counter still print the per-row justification a reader needs to act on a
  failure (the round's own `prose` audit contract)?
- **A4 measurement determinism** — does the field removal change what the counter reads, or only how it reports?

## Revision measured

```
REV e07f131cf7037e58a21db6e1f3986cf401ad257c   (HEAD of my scratch clone = stage-1 freeze commit)
```

The instrument's own `REV` line printed `4090c3db79d11279ab5e5121ba25e74aa316e6e7` in every run below, because
`tip_rev()` reads `git rev-parse master`, not the checked-out tree. See Finding F1.

Frozen artifacts under test (sha256, at e07f131):

```
60d05a0a3f5b099061a902fac7612cd178c8dda01680ac04b84611a77fcf2dd8  plans/round51-surfaces.json
edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e  plans/round51_surfaces.py
```

## Method

Two independent directions, both cheap, both run in one batch per field:

- **Direction R (real run).** Strip the field from a scratch copy of the manifest and hand that copy to the
  frozen counter through its own declared override: `--manifest`. Every other input (lane, PROVINCE.md,
  probes, floor) is the frozen one, so any difference in the printed legs is attributable to the field.
- **Direction S (selftest).** Keep the manifest intact, neutralise *one field consumer* in a scratch copy of
  the counter, and run that copy's `--selftest`. A case flipping to FAILED proves the leg is pinned by a
  selftest case; `ALL PASS` proves it is not.

Direction R alone is not discriminating on exit code: the base tip already fails (`exit 1`) for reasons
unrelated to the field, so I compare the **printed leg counters**, which is what the predicate reads.

Commands (all inside `/fast/scratch/hyaku/kengaku-r51/C1SimpManifest`, `TMPDIR` exported there):

```sh
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane rev-parse --show-toplevel          # -> /fast/scratch/hyaku/kengaku-r51/C1SimpManifest/lane
git -C lane checkout --detach e07f131cf7037e58a21db6e1f3986cf401ad257c
cd lane && python3 plans/round51_surfaces.py --lane .            # frozen command, baseline
cd lane && python3 plans/round51_surfaces.py --selftest
python3 mutate.py        # per case: python3 plans/round51_surfaces.py --lane . --manifest <mutant>.json
python3 neutralise.py    # per variant: python3 surfaces-<field>.py --selftest
python3 nosection.py     # candidate counter that ignores per-entry `section`
```

The frozen command was used unmodified for the baseline; `--manifest` is an override the instrument itself
documents ("Honours `--lane`/`--manifest`/`--province` overrides"), so no frozen input was altered.

## Baseline (frozen command, freeze commit)

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

This reproduces the frozen before-receipt (`.ufo/waves/round-51/claims/c1-before.txt`) line for line, so the
removal experiments below are measured against the same tree the claim was frozen on.

Selftest baseline: `[selftest] cases=9 failures=0` / `[selftest] ALL PASS`, exit 0.

Field inventory (measured, not assumed): 7 top-level keys
(`anchor_file, note, resolve_floor, round, sections, surfaces, version`); 8 entry keys, of which 7 are on all 19
entries (`anchor, id, probe, prose, section, state, why`) and `count_claim` is on exactly one (`SF14`). All five
probe kinds are exercised: `paths` ×13, `sha256` ×3, `http` ×1, `port` ×1, `count` ×1 — the probe sub-schema
cannot shrink without deleting a kind some row uses.

## Keep / remove table

| field | level | removal effect, measured (Direction R) | selftest pin (Direction S) | leg? | verdict |
|---|---|---|---|---|---|
| `section` | entry | `ANCHOR-MISSING 19`, `UNCOVERED 19`, `UNVERDICTED 1→6` (absent rows lose their row, so their marker check reads the empty string) | `no_section` → `FAIL case 1 expected pass, got exit 1` | yes — scoped anchor resolution | **KEEP** |
| `state` | entry | `Traceback … KeyError: 'state'` after `PROBES`; no predicate line at all | crash (no case runs) | yes | **KEEP** |
| `prose` | entry | `Traceback … KeyError: 'prose'` | `no_prose` → `FAIL case 2 expected fail, got pass` | yes — the DRIFT leg has no other input | **KEEP** |
| `probe` | entry | `Traceback … KeyError: 'probe'` | crash | yes — STALE/RESOLVE/NUMBER-DRIFT all read it | **KEEP** |
| `why` | entry | **counters byte-identical to baseline**; only the parenthetical in `DETAIL DRIFT …` empties: `(the row's first path cell …)` → `()` | `no_why` → `cases=9 failures=0 / ALL PASS` | no — evidence text only | **KEEP** (evidence leg, not a predicate leg) |
| `count_claim` | entry, 1 row | `NUMBER-DRIFT 1→0`, and the `DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170` line vanishes **while the row still claims 25 and the probe still counts 170** — the leg becomes vacuously satisfiable | `no_count_claim` → `FAIL case 5 expected fail, got pass` | yes — conditional leg, and the only guard on the one numeric row | **KEEP** |
| `resolve_floor` | top | all leg counters print, then `Traceback … KeyError: 'resolve_floor'`: no `RESOLVE` line, no `PREDICATE` line | `no_resolve_floor` → `FAIL case 8 expected fail, got pass` | yes — the do-nothing defence | **KEEP** |
| `note` | top | **counters byte-identical to baseline**, exit 1 both ways | nothing to neutralise — no consumer exists | no | **REMOVE** |
| `version` | top | counters byte-identical | none | no | **REMOVE** |
| `round` | top | counters byte-identical | none | no | **REMOVE** |
| `anchor_file` | top | counters byte-identical — **and setting it to `NOPE-DOES-NOT-EXIST.md` also leaves every counter identical**: the counter never reads it, the province path comes from `--province` or the hardcoded `lane/PROVINCE.md` default | none | no | **REMOVE** (and it is misleading: it declares a binding the instrument does not honour) |
| `id` | entry (not in item list; control) | `Traceback … KeyError: 'id'` | crash | yes | **KEEP** |
| `anchor` | entry (control) | `Traceback … KeyError: 'anchor'` | crash | yes | **KEEP** |
| `sections` | top (control) | `Traceback … KeyError: 'sections'` | crash | yes | **KEEP** |
| `surfaces` | top (control) | `Traceback … KeyError: 'surfaces'` | crash | yes | **KEEP** |

Two-field interaction check: `state` and `prose` are *not* redundant even though a passing row has
`prose == state == observed`. They encode different facts — what the row says today vs what is true today — and
the DRIFT leg exists precisely because they disagree on SF01/SF02/SF03 at this tip. Collapsing them would make
the three DRIFTs disappear without the rows being corrected.

Extra-field tolerance (measured): adding an unknown top-level key and an unknown entry key leaves every counter
identical — the counter validates no field set at all. That is why "nothing fails" is the *only* signal a dead
field gives; there is no schema check to catch it.

## Evidence, verbatim

### Direction R — discriminating cases

`drop-section` (mutant = same manifest, `section` removed from all 19 entries):

```
CASE drop-section exit=1
  ANCHORS total=19 dup=0 missing=19
  UNVERDICTED 6
  ANCHOR-MISSING 19
  UNCOVERED 19
  PREDICATE R51-C1 fail
```

`drop-state` / `drop-prose` / `drop-probe` / `drop-resolve_floor`:

```
CASE drop-state exit=1        Traceback (most recent call last): … KeyError: 'state'
CASE drop-prose exit=1        Traceback (most recent call last): … KeyError: 'prose'
CASE drop-probe exit=1        Traceback (most recent call last): … KeyError: 'probe'
CASE drop-resolve_floor exit=1  … RESOLVE/SECTION-MISSING printed, then Traceback … KeyError: 'resolve_floor'
```

`drop-why` (compare to baseline: every leg counter equal, one evidence field lost):

```
CASE drop-why exit=1
  DRIFT 3
    DETAIL DRIFT SF01 prose=present state=absent ()
    DETAIL DRIFT SF02 prose=present state=absent ()
    DETAIL DRIFT SF03 prose=present state=absent ()
  STALE 0
  UNVERDICTED 1
  NUMBER-DRIFT 1
    DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
  ANCHOR-DUP 0  ANCHOR-MISSING 0  UNCOVERED 0  SECTION-MISSING 0
  RESOLVE observed_present=13 floor=13 verdict=met
  PREDICATE R51-C1 fail
```

`drop-count_claim` (the leg is gone, the disagreement is not):

```
CASE drop-count_claim exit=1
  DRIFT 3
  STALE 0
  UNVERDICTED 1
  NUMBER-DRIFT 0          <- was 1; DETAIL NUMBER-DRIFT line absent
  ANCHOR-DUP 0  ANCHOR-MISSING 0  UNCOVERED 0  SECTION-MISSING 0
  RESOLVE observed_present=13 floor=13 verdict=met
  PREDICATE R51-C1 fail
```

`drop-note`, `drop-version`, `drop-round`, `drop-anchor_file`, `anchor_file=NOPE-DOES-NOT-EXIST.md`,
`extra-field`: all printed the baseline block above, leg for leg, with no added `DETAIL` line. Representative
tail of each:

```
CASE drop-note exit=1        DRIFT 3 / STALE 0 / UNVERDICTED 1 / NUMBER-DRIFT 1 / …0 / RESOLVE …met / fail
CASE drop-version exit=1     (identical)
CASE drop-round exit=1       (identical)
CASE drop-anchor_file exit=1 (identical)
CASE anchor_file-bogus exit=1 (identical — the declared anchor file is not read)
CASE extra-field exit=1      (identical — unknown keys are ignored, not rejected)
```

### Direction S — selftest pins

```
VARIANT no_count_claim exit=1
  [selftest] cases=9 failures=1
  [selftest] FAIL case 5 expected fail, got pass
  [selftest] FAILED
VARIANT no_why exit=0
  [selftest] cases=9 failures=0
  [selftest] ALL PASS
VARIANT no_prose exit=1
  [selftest] FAIL case 2 expected fail, got pass
VARIANT no_resolve_floor exit=1
  [selftest] FAIL case 8 expected fail, got pass
VARIANT no_section exit=1
  [selftest] FAIL case 1 expected pass, got exit 1
```

Case numbering is the counter's own (`S0`…`S8`, incremented in `run()`): case 1 = S0 consistent pass,
case 2 = S1 drift, case 5 = S4 number drift, case 8 = S7 floor violated. So `count_claim`, `prose`,
`resolve_floor` and `section` each have a named selftest case that dies when the field's consumer is
neutralised; `why` has none, which is the selftest-side confirmation of the Direction-R result.

### `section`: removable only at a measured cost

A candidate counter that searches every declared section for each anchor and derives the entry's section from
where the anchor was found (`surfaces-nosection.py`, scratch only) is behaviour-identical on the real manifest:

```
### B: nosection counter, full manifest
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3 / STALE 0 / UNVERDICTED 1 / NUMBER-DRIFT 1 / …0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail          (= baseline, leg for leg)

### C: nosection counter, manifest with `section` stripped
(same block, identical counters, exit=1)
### D: nosection counter --selftest -> exit=0
```

So `section` *is* deletable given that counter change — but the change costs a behaviour the frozen instrument
has today: scoped anchors let two sections legitimately contain the same first cell. Fixture (two sections,
same `| Surface A |` row in each, both probes present, floor 2):

```
### frozen exit=0
  ANCHORS total=2 dup=0 missing=0
  ANCHOR-DUP 0 / UNCOVERED 0
  PREDICATE R51-C1 pass
### nosection exit=1
  ANCHORS total=2 dup=2 missing=0
    DETAIL ANCHOR-DUP SF01 anchor appears 2 times
    DETAIL ANCHOR-DUP SF02 anchor appears 2 times
  UNCOVERED 2
  PREDICATE R51-C1 fail
```

That is a real tightening, not a free deletion: it would force global anchor uniqueness on future rows. The
frozen instrument is frozen for this round, so `section` stays. Recorded as the one *candidate* deletion for a
future round, with its price.

## Minimal schema

Minimal schema that preserves every predicate leg of the frozen counter, with no instrument change:

```json
{
  "sections": ["## Surfaces", "### Core"],
  "resolve_floor": 13,
  "surfaces": [
    {
      "id": "SF01",
      "section": "## Surfaces",
      "anchor": "| Research notes (SSOT for eval craft) |",
      "state": "absent",
      "prose": "present",
      "probe": {"kind": "paths", "targets": ["~/Projects/webzites/repos/llm-wiki"]},
      "count_claim": 25,
      "why": "the row's first path cell asserts the wiki tree resolves"
    }
  ]
}
```

- `count_claim` — **optional**, present only on rows that state a number (1 of 19 today). Its absence is a
  leg-free row; its presence is the only thing that arms NUMBER-DRIFT for that row.
- `why` — **optional** and predicate-inert. Keep it in practice: it is the only per-row justification the
  counter prints on DRIFT, and the claim's own limits section makes `prose` a *recorded reading* that wave
  seats audit row by row. Removing it costs nothing measurable and costs the reader the reason.
- Deleted: `version`, `round`, `anchor_file`, `note` — four of the seven top-level keys, zero predicate legs.
  `anchor_file` is worse than dead: it claims a binding (`PROVINCE.md`) the counter ignores.
- `note` duplicates the predicate in prose inside the manifest while `plans/round-51-claims.md` §C1 is the
  frozen authority. Two copies of one rule drift; the manifest copy has no check. [INFERENCE] this is the
  duplicate-authority class the round-50 closure routes, not a measurement.

Net: 4 top-level fields removable today (7 → 3), 0 entry fields removable without an instrument change
(8 → 8, with `count_claim`/`why` already optional by construction). One further entry field (`section`) is
removable only with the global-anchor-uniqueness tightening measured above.

## Findings (outside the item, recorded because they are measured)

- **F1 — the `REV` line names the wrong revision when HEAD ≠ master.** `tip_rev()` runs
  `git rev-parse master`; my scratch clone had HEAD at `e07f131` (the freeze commit) and master at `4090c3d`,
  and every run printed `REV 4090c3d…`. A receipt measured at a detached checkout therefore cites a tree it did
  not read. The landing measurement is at the landing tip on `master`, so it is not affected *if* the L1 measures
  on master; a detached or re-tagged measurement would be. Evidence: the baseline block above (HEAD `e07f131`,
  printed `REV 4090c3d…`).
- **F2 — `paths` probes are HOME-dependent, so the counter is not environment-independent.** Running the same
  frozen command with `HOME` pointed at scratch flipped one surface to absent: `PROBES present=13 absent=6
  STALE 0` → `PROBES present=12 absent=7 STALE 1`, `RESOLVE … verdict=violated`. All 13 `paths` entries use `~/`.
  The after-measurement must be run with the same HOME the `state` values were recorded under.
- **F3 — the manifest is unvalidated.** Unknown keys are ignored, and no check requires a field to be non-empty
  (`why: ""` on all 19 entries leaves every counter identical). A field can rot silently; only a human diff
  notices. The `count_claim` leg is the exception only because it is conditionally armed.

## Limits

- One lane, one manifest (19 entries), one instrument. Results are about this schema, not about manifests in
  general.
- Direction R compares printed leg counters, not exit codes, because the base tip already fails; the comparison
  is exact (same manifest, same PROVINCE.md, same probes, same floor, one field removed).
- `--manifest` is an override of the frozen command; it changes which manifest is read and nothing else. The
  frozen command itself was run unmodified for the baseline.
- Crashing removals (`state`, `prose`, `probe`, `id`, `anchor`, `sections`, `surfaces`, `resolve_floor`) prove
  the field is load-bearing but do not prove the *leg* is well-implemented — that is `C1RevPredicate`'s item,
  not mine.
- The `section` deletion is a scratch prototype, not a proposal to edit the frozen instrument this round.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C1SimpManifest` was removed before this seat yielded; no scratch
  tree is left on disk and no citable evidence lives in it. Free space observed: `/fast` 540G available (33%
  used).
- No tool was installed or upgraded for this seat.

REV e07f131cf7037e58a21db6e1f3986cf401ad257c

VERDICT: The manifest cannot lose a predicate leg by deleting a *field*: 4 of 7 top-level keys (`version`, `round`, `anchor_file`, `note`) are dead weight and removable with byte-identical counters; all 8 entry fields and `resolve_floor`/`sections`/`surfaces` are load-bearing (7 crash the counter, `section` collapses three legs, `count_claim` silently vacates NUMBER-DRIFT while the SF14 disagreement persists, `why` is predicate-inert but is the only printed justification). Minimal schema: `sections` + `resolve_floor` + `surfaces[{id, section, anchor, state, prose, probe, count_claim?, why?}]`. Two measured defects for the L1: the counter's `REV` line reads `master` not HEAD (F1), and `paths` probes depend on ambient `HOME` (F2).
