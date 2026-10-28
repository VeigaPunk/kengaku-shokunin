# CritAdmission — kill-rule audit, round 51 (R51-C1 freshness, R51-C2 adjacency)

Seat: `CritAdmission` (critic, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Assignment: read the frozen kill rules in `plans/round-51-claims.md` and decide, **before any
landing**, whether each claim can reach its declared after-target without weakening a predicate
leg; name every leg the planned repair cannot satisfy on this host.

**Axes named.** C1's axis is **freshness** (8 → 9, "every surface `PROVINCE.md` declares is
machine-checked"); C2's axis is **adjacency** (8 → 9, "every routed finding names its owner and
its disposition"). I attacked neither axis directly: my sub-axes are (a) *predicate-leg
reachability on this host*, (b) *before/after comparability of the instrument* (does the after
measurement use the same bytes as the before receipt?), (c) *kill-rule firing power* (does a
vacuous landing trip any kill rule?), (d) *round-50 routed-defect coverage* (D1/D3/D5/D7). No other
axis is claimed or touched.

**Revision measured.** `REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (lane `master`, one commit
after the stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c`; the only diff is three wave
spec files). Every measurement below ran in a `git clone --shared` snapshot of that revision whose
`git rev-parse --show-toplevel` printed the clone dir before any write:

```
clone instrument blobs (frozen bytes, committed):
  plans/round51_routing.py    043533d1a9599b8a9efda155812899d382384fbf
  plans/round51_surfaces.py   6107c605925310ed64433b1f27d3459e8836ed43
  plans/round51-surfaces.json 154ba1cfa0871e7b8c26fbe5118e87565a7bf7f6
lane working-tree instrument at wave time (UNCOMMITTED):
  plans/round51_routing.py    8ea57a501b03968378d93784a32668c52ac59627
```

Scratch: `/fast/scratch/hyaku/kengaku-r51/CritAdmission` (one shared clone; `TMPDIR` exported
there; `df -h /fast` → `804G 256G 548G 32% /fast`; `scripts/hyaku/disk-guard.sh status` → no ENOSPC).
No tool was installed or upgraded for this seat (python3/git/curl/ss only).

---

## A. R51-C1 — leg-by-leg reachability

Frozen command reproduced at the measured revision, exit 1, byte-equal in substance to
`claims/c1-before.txt`:

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3 ... STALE 0
UNVERDICTED 1 ... NUMBER-DRIFT 1
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

| leg | frozen implementation (`plans/round51_surfaces.py`) | reachable on this host? | evidence |
|---|---|---|---|
| `ANCHOR-DUP 0` / `ANCHOR-MISSING 0` | anchor substring searched inside the entry's own section table | yes | base run: `total=19 dup=0 missing=0` |
| `UNCOVERED 0` | every row of `## Surfaces` / `### Core` maps to one entry | yes | base: `rows=9 entries=9 uncovered=0`, `rows=10 entries=10 uncovered=0` |
| `STALE 0` | probe result vs manifest `state` | yes at this tip, **fragile** | 13 present probes include a digest that "floats" (`SF12`), a shim digest (`SF15`), a LISTEN port (`SF16` :8791) and a growing count (`SF14`). At 19/19 `present=13 = floor 13`: one flapping present surface makes `RESOLVE violated` and fails the claim. The after-target's `+1` surface is the only slack. |
| `DRIFT 0` | `e["prose"] != e["state"]` — **manifest-internal**, never reads the row | yes, **vacuously** | measured below: a manifest-only edit prints `pass` while `PROVINCE.md:12/13/14` still assert the three surfaces resolve |
| `UNVERDICTED 0` | `ABSENT\s+\d{4}-\d{2}-\d{2}` searched anywhere in the anchored **line** | yes, but not bound to the probed target | `PROVINCE.md:12,13,14` already carry `ABSENT 2026-10-20`; `:13`'s marker dates the pre-relocation `~/bench-arena/`, not the probed `~/archive/bench-arena/` |
| `NUMBER-DRIFT 0` | `count_claim` vs the probe detail — **manifest-internal** | yes, **vacuously** | a manifest-only `count_claim: 170` prints `NUMBER-DRIFT 0` while `PROVINCE.md:112` still says "25 rows" (measured) |
| `RESOLVE present >= 13` | counts **observed** present probes | yes | base 13; with the `+1` surface 14 |
| `+1 new declared surface` (after-target element, not a predicate leg) | — | yes, mechanically | `:34113` absent (`curl` rc=7); live served endpoints measured: `127.0.0.1:1234` → `{"id":"LFM3-1.7B",...,"owned_by":"llamacpp"}`; `:8793` glm-5.3-flash, `:8795` claude-opus-5-5, `:8796` gemini-3.8-flash shims. A `## Surfaces` row + entry for `:1234` prints the pass below. |

### A1. Counterexample that the kill rule does not fire on: manifest-only C1 pass

Mutation: three `prose` values `present→absent` (SF01/SF02/SF03) and `count_claim 25→170` (SF14)
in a **copy of the manifest**, plus one `ABSENT 2026-10-28` marker appended to the SF04 row
(`PROVINCE.md:15`). The rows that lie (12, 13, 14) and the SF14 cell (112) are **byte-identical**
to the lane; `diff` of the copy against the lane is only lines 15 and 158.

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST .../c1/m.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 0
STALE 0
UNVERDICTED 0
NUMBER-DRIFT 0
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 pass
exit=0
```

`ROWS` stays 9/10, so the kill rule's row-count floor does **not** fire; the claim's declared
surface (`PROVINCE.md`) is never touched. This is the exact premature-saturation path the L1 must
not take. (Corroborates `C1RevPredicate` F1–F3, `C1RevProbes` F2, `C1MutManifest` F1,
`CritProseRead`; my measurement is the full `pass`, not just one zeroed counter.)

### A2. Honest C1 variant (rows corrected) — also passes

Same manifest, plus dated markers and corrected assertions on lines 12/13/14 and the `:112` cell
changed to "170 rows at 2026-10-28 (25 was the round-24 snapshot)":

```
ROWS section="## Surfaces" rows=10 entries=10 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=20 present=14 absent=6 errors=0
DRIFT 0 / STALE 0 / UNVERDICTED 0 / NUMBER-DRIFT 0
RESOLVE observed_present=14 floor=13 verdict=met
PREDICATE R51-C1 pass
exit=0
```

So C1 has **no unreachable leg**: both the vacuous and the honest landings pass. The predicate
cannot distinguish them; only the row diff can.

### A3. C1 kill-rule defects (stated, not new)

1. **Control 1's stated mechanism is wrong.** The claims file says `declare-all-absent` violates
   the resolve floor. The frozen counter counts *observed* present probes, so the receipt
   `claims/control-c1-declare-all-absent.txt` prints `RESOLVE observed_present=13 floor=13
   verdict=met`; the control fails only via `STALE 13`. The manifest docstring repeats the same
   false rationale. (Same finding as `C1CritDeclareAllAbsent`; corroborated, not claimed as new.)
2. **Control 4 must target SF04 after dating.** `SF01/SF02/SF03` already carry an ISO `ABSENT`
   marker, so stripping a date from one of *those* rows cannot produce `UNVERDICTED 1` without also
   removing the 2026-10-20 marker. Only SF04's line 15 lacks a date today.
3. **The kill rule is manual.** `ROWS per section must not fall below 9 and 10` is not a
   predicate leg (the counter has no minimum). A row moved out of a declared section (not deleted)
   keeps `UNCOVERED 0` and shrinks `ROWS` silently; the after receipt must show the `ROWS` lines
   and a `PROVINCE.md` diff, or the floor is unverified.

---

## B. R51-C2 — leg-by-leg reachability

Frozen command reproduced at the measured revision, exit 1, matching `claims/c2-before.txt`
(`rows=71`, `attributed=0`, `CHECKS absent=10`).

| leg | frozen implementation (`plans/round51_routing.py`) | reachable on this host? | evidence |
|---|---|---|---|
| `FIELDS complete=71` | the 11 keys present | yes | all 71 rows already carry the 9 non-new keys; only `owner`,`disposition` are missing |
| `OWNERS attributed=71` | `owner in load_owners(lane.parent)` | yes **only for the 17 hardcoded names** | measured: `load_owners` returns exactly `FALLBACK_OWNERS` (17); the conf regex matches **0** lines; 7 real fleet lanes are rejected; in a clean clone `../shokunin.conf` does not exist at all |
| `DISPOSITIONS bad=0` | value in the 6-name set + `status` in 4-name set | yes | statuses today: closed 41, open 27, refused 2, blocked 1 |
| `SOURCES missing=0` | `(lane / source.split(":")[0]).exists()` — **line number discarded** | yes, but **cannot catch D5** | a row citing `file:999` passes; the round-50 D5 defect class (wrong locations) is invisible to this leg |
| `CHECKS absent=0` | non-empty `check` string | yes | 10 rows need a check authored |
| `CHECK_FAILED 0` | `bash -lc cmd` with `cwd=mkdtemp()`, `LANE` env, 60 s | yes, **only after rewriting 41 checks** | as written: 55/71 fail; with `cd "$LANE" && ` prefix: 18/71 fail and **all 18 are open/blocked** (41 closed rows pass); honest candidate: 41 fixed-verified, 41 passed, 0 failed |
| `CLOSE_REF missing=0` | only `fixed-historical`; first token must be a commit (`git cat-file -e`) or an existing path | yes if used, but not with the recorded prose | 13 rows' first token `77ea425a` resolves (`cat-file` commit-ok); `round-43 …`, `round-46 …`, `measured …`, `F1-F4 …`, `children …` first tokens do **not** resolve — those rows cannot be `fixed-historical` without prepending a real ref |
| `NEXT violations=0` | `routed`/`referral`: owner ≠ kengaku and `next` non-empty | yes | reachable; `unowned:integrator` is accepted as a non-kengaku owner |

### B1. Check-leg measurements (the decisive reachability number)

Three candidate ledgers, each 71 rows, same frozen instrument bytes (`043533d`):

```
A. every row owner=kengaku, disposition=fixed-verified, checks unchanged (empty→`true`)
   VERIFIED ran=71 passed=16 failed=55      PREDICATE R51-C2 fail
   → of the 16 passes, 10 are the `true` placeholders and 6 are real commands;
     I re-ran those 6 in a scratch cwd: R39-R2 rc=0, R42-R3-03 rc=0, R42-R3-07 rc=0,
     R42-R3-08 rc=0, R42-R3-26 rc=0, R39-R5 rc=0.
     R39-R2 and R42-R3-26 accept exit 2, and `python3 plans/…` exits 2 on a missing file;
     R42-R3-03/-07/-08 are negative greps that go green because the file is absent.
     Only R39-R5 (absolute path) is a genuine pass. The frozen cwd makes these checks vacuous.

B. same ledger, each check prefixed `cd "$LANE" && ` (assertion body unchanged)
   VERIFIED ran=71 passed=53 failed=18
   failures by status: {'open','blocked'} — closed rows failing: [] (41/41 closed pass)

C. honest attribution: closed→fixed-verified (prefixed), open/blocked→accepted-risk,
   refused→refused-out-of-scope, empty checks given a source-existence check
   VERIFIED ran=41 passed=41 failed=0
   FIELDS 71/71, OWNERS 71/71, DISPOSITIONS 71/71, SOURCES 71/71, CHECKS 71/71,
   CLOSE_REFS resolved=0 missing=0, NEXT violations=0
   PREDICATE R51-C2 pass      exit=0
```

**Conclusion:** C2 is reachable under the **frozen bytes** with no instrument change, at the cost
of rewriting the 41 closed rows' `check` fields by a `cd "$LANE" && ` prefix (the ledger *is* the
claimed surface, so this is in scope). Candidate C is a reachability proof, not an endorsement of
its dispositions; per-row honesty remains the wave's job.

### B2. The owner leg as declared is not implemented (leg not satisfiable as written)

```
owners_count 17
owners ['aggregator','chousa','kagi','kaidoku','kake','kama','kasegi','kengaku','kotoba',
        'kotodama','kumitate','mori','protocol','souji','tabi','tameshi','unowned:integrator']
conf_lanes 23 ['aggregator','audio','chousa','game-dev-2d','game-dev-3d','kagi','kaidoku','kake',
               'kama','kasegi','kengaku','kotoba','kotodama','kumitate','lore','mado','mori',
               'protocol','revenger','souji','tabi','tameshi','tsukuroi']
conf_lanes_rejected ['audio','game-dev-2d','game-dev-3d','lore','mado','revenger','tsukuroi']
owners_not_in_conf ['unowned:integrator']
clean-clone parent conf_exists False → owners_count 17
```

The claims' leg is "every `owner` names a fleet lane from `../shokunin.conf` (or
`unowned:integrator`)". The frozen `load_owners` parses `name: {` lines; this host's conf lists
lanes as `id|repo|axes` inside `LANES="…"` → 0 matches → the accepted universe is a hardcoded
17-name list. Consequences the L1 must respect:

- No current row *requires* a rejected lane (grep of the 71 rows for `tsukuroi|lore|mado|revenger|audio|game-dev` → 0 hits), so the leg is reachable for this ledger.
- If any row's honest owner is one of the 7 (`tsukuroi` is the plausible one for the
  `plans/pkg_gate.py` rows `R42-R3-08`/`R45-S5-7c`), the claim is **unreachable as frozen**: the
  counter rejects the honest name, and passing would require false provenance. That case must be
  escalated, never narrowed.
- In a clean clone the conf is absent, so the after measurement cannot verify the declared leg at
  all; the after receipt must not claim it did. (Same finding as `C2ConnProtocol:155`,
  `C2ConnTooling:120`; my numbers above are an independent measurement.)

### B3. The check leg is satisfiable by a tautology

The counter's own selftest blesses `check: "true"` as `VERIFIED ran=1 passed=1`
(`--selftest` case 1, measured `cases=11 failures=0`), and control 2 (`fake-fix`) only exercises
`false`. So `CHECK_FAILED 0` is not evidence of verification unless the check text is audited.
The honest path exists (candidate C), so the L1 must keep each assertion body byte-identical and
publish the prefix-only diff. (Same as `CritClaimSizing` A6, `C2CritDisposition`; corroborated.)

### B4. The SOURCE leg cannot answer round-50 D5

`source.split(":")[0]` discards the line number and tests file existence only. Round-50 D5 is a
*wrong-location* defect (S175/S177 quotes at the wrong `:lines`); C2's predicate passes on it.
The after-target's `SOURCE missing=0` must not be reported as D5 closure.

---

## C. The decisive landing hazard: the frozen C2 instrument changed mid-wave

At wave time the lane working tree carries an **uncommitted** edit to the frozen instrument:

```
$ git status --porcelain | grep -v '^?? '
 M plans/round51_routing.py
$ git diff --stat plans/round51_routing.py
 plans/round51_routing.py | 18 +++++++++++++-----
 1 file changed, 13 insertions(+), 5 deletions(-)
$ ls -l --time-style=full-iso plans/round51_routing.py
 -rwxr-xr-x 1 vgpnk vgpnk 10562 2026-10-28 15:33:21.513675706 -0300
   (freeze commit e07f131 at 15:09:28; wave dispatch 15:17:41; this edit at 15:33)
$ git hash-object plans/round51_routing.py  -> 8ea57a501b03968378d93784a32668c52ac59627
$ git rev-parse HEAD:plans/round51_routing.py -> 043533d1a9599b8a9efda155812899d382384fbf
```

The diff changes exactly the two legs this audit found weak: `load_owners` now parses `id|` rows
and globs `*-shokunin` dirs (repairs the owner leg), and checks run `cwd=str(lane)` with a 90 s
timeout (repairs the 55 check failures), plus `--ledger` resolution. The modified file's own
selftest passes (`cases=11 failures=0`) and the base ledger still prints `PREDICATE R51-C2 fail`,
so the edit is not a cheat — but it is a **post-freeze predicate change**:

- The before receipt (`c2-before.txt`) and all five controls were measured with the frozen bytes;
  an after receipt measured with `8ea57a5` is **not comparable** to them, and the controls do not
  bind the landed predicate.
- No receipt names either counter's digest, so a reader cannot tell which predicate printed a
  `pass`.
- The frozen bytes already reach `pass` (candidate C), so the edit is **not needed for
  reachability**. Reverting it costs 41 mechanical check prefixes; landing it requires the
  round-50 precedent: commit the repaired counter, append the deviation + new digest to
  `plans/round-51-claims.md` (append-only, before the after measurement), re-run the before receipt
  and every control with the new bytes, and name the digest in the after receipt.
- `plans/round51_surfaces.py` and the manifest are **clean** (`mtime 15:03:32`, blobs as frozen),
  so C1's instrument identity is not in question.

This is also the round-50 **D1** defect class recurring (uncommitted round work in the tree). A
clean clone of the tip measures the committed bytes, so an L1 that forgets to commit gets the
*frozen* predicate in the after receipt — which fails if any row is `fixed-verified` with an
unrooted check.

---

## D. Round-50 routed defects this round answers

| defect | answered by the frozen instruments? | consequence for the landing |
|---|---|---|
| **D1** wave outputs uncommitted | no (no counter reads git state) | the tree already carries `M plans/round51_routing.py`; the L1 must commit or revert it and commit the wave outputs before the after measurement, or D1 recurs verbatim |
| **D3** no `WAVE-DONE` | no | the wave must land `WAVE-DONE` + `w1-results.json`; a settled seat without a report is a routed defect class |
| **D5** wrong source locations | **no** — `source.split(":")[0]` drops the line | a second check (line-number verification) is required; `SOURCE missing=0` must not be cited as D5 closure |
| **D7** lesson spot-check row | no | the L1 must append the spot-check line to the round-51 lesson and cite the closure file |

---

## E. Decision and smallest safe corrections

**Reachability (asked before landing):** neither claim has a leg that is unreachable on this host.
C1's predicate passes at 19/19 (`present=13`, zero slack) and at 20/20 with the `+1` live surface
(`present=14`); C2's predicate passes with the frozen bytes at 41 fixed-verified / 28 accepted-risk
/ 2 refused-out-of-scope. **Do not narrow either after-target.** The danger is the opposite:
both predicates are satisfiable without the claimed work, and no kill rule fires.

Smallest safe corrections, in landing order:

1. **C1 — land the row corrections, not just the manifest.** Edit `PROVINCE.md:12,13,14` (dated
   `ABSENT 2026-10-28` + corrected assertion) and `:112` (`25 → 170`), then update `prose` /
   `count_claim` in the same commit, and put the `PROVINCE.md` diff in the after receipt. A
   manifest-only pass must be rejected at landing. Keep `ROWS` at 10/10 by adding the `+1` row
   (measured live: `:1234` LFM3-1.7B) rather than by deleting anything; word it as reachability
   only — the serving plane stays unowned (§Refusals) and must not be used for prompts.
2. **C1 — receipt must show the slack.** `RESOLVE observed_present=14 floor=13` (or state
   explicitly that it is 13 = floor and name the four flapping probes). A single `pass` at
   `present=13` is one host restart away from failing.
3. **C2 — do not measure the after with `8ea57a5`.** Either revert the working-tree edit and use
   the frozen bytes with a prefix-only rewrite of the 41 closed checks (measured pass), or commit
   the repaired counter and append the deviation + digest to the claims before re-running the
   before receipt and all controls. Never cite `c2-before.txt` (frozen bytes) next to a `pass`
   printed by different bytes.
4. **C2 — keep check assertions byte-identical.** Prefix only (`cd "$LANE" && `), publish the diff,
   and reject any `fixed-verified` row whose check is `true`/`false`-shaped or whose green depends
   on a missing file. The 6 as-written "passes" above are exactly that failure mode.
5. **C2 — owner values stay inside the 17-name fallback set** unless the counter is repaired and
   re-frozen; if an honest owner is `tsukuroi|lore|mado|revenger|audio|game-dev-*`, escalate
   instead of misattributing.
6. **D5/D7 are not covered by either counter**; land them as their own append-only items and do not
   claim them through `SOURCE missing=0`.

## F. Landing observed after my measurement (not verified by me)

After the measurements above, the L1 began landing in the lane working tree. Read-only `git diff`
at 15:38 shows the honest path being taken: `PROVINCE.md:12,13,14` dated `ABSENT 2026-10-28` with
corrected text, `:112` corrected to 171 rows, a new `## Surfaces` row for the live LFM3 pair
(`:45669` direct, `:1234` router) with its manifest entry (20 entries), `prose` `present→absent`
for SF01–SF03, `count_claim 25→171`, and two append-only amendments in `plans/round-51-claims.md`
written before the scored run — **A1** (instrument: check cwd, timeout, owner universe, `--ledger`
resolve) and **A2** (ledger rows 71 → 75 with four new owned rows). Both amendments are the right
instrument for a post-freeze change; A2's row count is consistent with the after-target's
parenthetical ("no row added without an owner") and does not trip the kill rule ("drops below 71").

Three corrections the after receipt must still absorb:

1. **Stale `why`.** `plans/round51-surfaces.json` SF14 now reads `count_claim: 171` but its `why`
   still says "Core row states the registry holds **25** rows". The `why` is the entry's recorded
   justification; leaving it at 25 is false provenance for a 171 claim. Change it in the same
   commit as the count.
2. **Table shape.** `PROVINCE.md:12,13,14` now carry **4 cells in a 3-column table** (5 pipes vs the
   header's 4); the appended 4th cell holds the correction while the third cell still asserts
   "all resolve at the archive path" / "declares a live served endpoint". The counter passes either
   way, but the row now asserts and denies in one line and the table's column count changed
   silently. Prefer the house style the round-25 correction used (a paragraph after the table) or
   amend the assertion in place, so the table stays 3-column and the row has one reading.
3. **Digest + controls.** A1 says the predicate legs are unchanged and discloses the `VERIFIED
   ran=0` consequence, but the C2 controls were printed by the frozen bytes and no C2 control
   receipt exists yet in `.ufo/waves/round-51/claims/`. Either re-run all five C2 controls under the
   committed A1 bytes, or record that controls 1/3/4/5 are byte-invariant and control 2
   (`check: false`) still exits nonzero under `cwd=lane`. The after receipt must name
   `plans/round51_routing.py`'s digest and print `LEDGER rows=75` with 75 attributed.

## Limits

- Endpoint probes are point-in-time (`:1234`, `:8791`, the shim digests, the SOURCES count); my
  `present=14` measurement is true of the capture minute, not of the landing minute.
- My C2 candidate C is a *mechanical* reachability proof; its per-row dispositions are placeholders
  for the wave's attribution and are not proposed as the landing ledger.
- I did not re-run the C1 controls (other seats own them) and did not audit the `prose` readings
  row by row (that is the wave's row audit); I used the manifest's recorded readings as given.
- I read no sibling repository; the fleet `shokunin.conf` was read only to count lanes.
- Scratch `/fast/scratch/hyaku/kengaku-r51/CritAdmission` was removed before yield; no production
  file was written by this seat (only this report), no commit or mutating git command was run
  anywhere, and every fixture write was inside the scratch clone after asserting
  `git rev-parse --show-toplevel` equal to it.

`REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7`

**VERDICT:** Both claims are **reachable** at their frozen predicates — C1 measured `pass` at
19/19 (`present=13=floor`) and at 20/20 with the live `+1` surface (`present=14`); C2 measured
`pass` with the **frozen bytes** at `VERIFIED ran=41 passed=41 failed=0`, 71/71 owners,
dispositions, sources and checks — so **no after-target may be narrowed**. But four predicate legs
are satisfiable vacuously (`DRIFT`, `NUMBER-DRIFT` are manifest-internal; `UNVERDICTED`'s marker is
not target-bound; `CHECK_FAILED 0` accepts tautologies), one leg is not implemented as declared
(`owner from ../shokunin.conf`; 7 real lanes rejected, clean clone has no conf), and the frozen C2
instrument was edited uncommitted in the working tree mid-wave (`043533d → 8ea57a5`, 15:33), so an
after receipt printed by those bytes is not comparable to the before receipt or the controls.
Land the row corrections with a `PROVINCE.md` diff; for C2 either rewrite the 41 closed checks by
prefix only under the frozen bytes, or land amendment A1 with a named instrument digest and re-run
the C2 controls; and escalate rather than misattribute any owner outside the 17-name set.
