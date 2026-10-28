# R51 · RevSeparability — causal separability of C1 and C2 (scratch experiment)

Seat: `RevSeparability` (reviewer), kengaku round 51, hyaku run 11, 2026-10-28.
Lane read-only throughout; every mutation below happened inside
`/fast/scratch/hyaku/kengaku-r51/RevSeparability` (removed before yield, see §8).
Claims read first: `plans/round-51-claims.md` (in full), then both frozen counters
(`plans/round51_surfaces.py`, `plans/round51_routing.py`), the manifest
(`plans/round51-surfaces.json`), the ledger and both before receipts.

## 1. Axes named

- **freshness (8 → 9)** — the axis R51-C1 moves: every surface `PROVINCE.md` declares is
  machine-checked at the tip (`plans/round51_surfaces.py`, predicate `R51-C1`).
- **adjacency (8 → 9)** — the axis R51-C2 moves: every routed finding names its owner lane
  and its disposition (`plans/round51_routing.py`, predicate `R51-C2`).
- **separability** — the property this seat tests: C1 and C2 are independent claims, so each
  must pass its own counter with only its own work landed and must leave the other counter
  red. Coupling between them is a defect *of the claims*, not of a seat.

## 2. Method

Base: stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c`. The lane tip
`4090c3d` differs from it only by `.ufo/waves/round-51/{build_spec,w1-spec,w1-dispatch}.json`
(`git diff --stat e07f131 4090c3d` → those three files, 1743 insertions, no production file),
so the clones were reset to the freeze commit with `git checkout -B master e07f131…`.

Two clones, `git clone --shared` from the lane, each pinned to the freeze, laid out to
reproduce the real lane topology (`lane.parent` = fleet root, holding a copy of
`/home/vgpnk/Projects/shokunin/shokunin.conf`):

```sh
cd /fast/scratch/hyaku/kengaku-r51/RevSeparability
export TMPDIR=$PWD
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin laneA
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin laneB
mkdir -p fleet && mv laneA laneB fleet/ && cp /home/vgpnk/Projects/shokunin/shokunin.conf fleet/
for D in fleet/laneA fleet/laneB; do
  git -C "$D" rev-parse --show-toplevel          # == $PWD/fleet/$D, asserted before every write
  git -C "$D" checkout -B master e07f131cf7037e58a21db6e1f3986cf401ad257c
done
```

Clone **A** — only C1's repairs (append-only PROVINCE corrections + manifest states):

```sh
git -C fleet/laneA diff --stat e07f131 90fd925
#  PROVINCE.md                 | 10 +++++-----
#  plans/round51-surfaces.json |  8 ++++----
#  2 files changed, 9 insertions(+), 9 deletions(-)
```

The five PROVINCE edits are dated `ABSENT 2026-10-28` markers appended to the four rows
SF01/SF02/SF03 (which asserted their target resolves) and SF04 (which carried no ISO date),
plus a dated `**170 rows at 2026-10-28**` correction on the SF14 Core row; the manifest
records `prose: absent` for SF01–SF03 and `count_claim: 170`. No row deleted, no file
rewritten, `corpus/SOURCES.md` untouched. Commit `90fd925d49a0d91001c46a00927a6d3eeac559e3`.

Clone **B** — only C2's ledger attribution:

```sh
git -C fleet/laneB diff --stat e07f131 131c9ec
#  corpus/routed-findings.jsonl | 142 +++++++++++++++++++++----------------------
#  1 file changed, 71 insertions(+), 71 deletions(-)
```

Every one of the 71 rows keeps `id/class/source/opened_round/status/close/blocker/note`
verbatim and gains `owner`, `disposition`, and (for `routed`) `next`; 70 of 71 `check`
strings were rewritten to resolve lane paths explicitly (`"$LANE/…"`, `git -C "$LANE"`,
`--lane "$LANE"`) because the counter runs every check with `cwd=<scratch>` — the frozen
ledger's checks are cwd-relative and all fail there (61/61 non-empty checks exit non-zero in
a scratch cwd; measured). Resulting distribution: `fixed-verified 40`, `accepted-risk 27`,
`refused-out-of-scope 2`, `fixed-historical 1`, `routed 1`; owners `kengaku 68`,
`unowned:integrator 3`; rows still 71. Commit `131c9ec27d49503a31dd69f6f534874e68ecf5b6`.
This attribution is a **separability vehicle, not a proposed landing**: the ownership calls
are the C2 seats' and the L1's to make (see §6.3 for what it demonstrates about the counter).

## 3. The four results

### 3.1 Clone A (C1 only) — C1 passes

```sh
cd fleet/laneA && python3 plans/round51_surfaces.py --lane .
```
```
REV 90fd925d49a0d91001c46a00927a6d3eeac559e3
MANIFEST plans/round51-surfaces.json entries=19 sections=2
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

### 3.2 Clone A (C1 only) — C2 still fails, at exactly the before numbers

```sh
cd fleet/laneA && python3 plans/round51_routing.py --lane . --run-checks
```
```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
exit=1
```

`diff` of this output against the frozen `.ufo/waves/round-51/claims/c2-before.txt` is empty
except the trailing `exit=1` line I append to every receipt: C1's landing perturbs no C2
counter at all.

### 3.3 Clone B (C2 only) — C2 passes

```sh
cd fleet/laneB && python3 plans/round51_routing.py --lane . --run-checks
```
```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=40 passed=40 failed=0
CLOSE_REFS resolved=1 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
exit=0
```

### 3.4 Clone B (C2 only) — C1 still fails, byte-identical to the before receipt

```sh
cd fleet/laneB && python3 plans/round51_surfaces.py --lane .
```
```
REV 131c9ec27d49503a31dd69f6f534874e68ecf5b6
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
exit=1
```

`diff` against `.ufo/waves/round-51/claims/c1-before.txt`, after removing the `REV` line from
both, is **empty except my appended `exit=1`**: same DRIFT/UNVERDICTED/NUMBER-DRIFT counts,
same three DETAIL lines, same probe census. C2's landing perturbs no C1 counter.

### 3.5 Extra: both landed together (no negative interaction)

Branch `combined` on clone A = `90fd925` + B's ledger → `2fb5e3a641def6dbdc6415cefe22b97a18141400`.
Both counters pass (`PREDICATE R51-C1 pass`, exit 0; `PREDICATE R51-C2 pass`, exit 0,
`VERIFIED ran=40 passed=40 failed=0`). This is not one of the four required cells; it rules
out the possibility that the two landings are individually fine but jointly red.

## 4. Read-set measurement (why separability holds, not just that it did)

`strace -f -e trace=openat,newfstatat,access` over each counter, lane paths extracted and
normalised:

- **C1 lane read-set (7 entries):** `PROVINCE.md`, `corpus/SOURCES.md`,
  `plans/round51-surfaces.json`, `plans/round51_surfaces.py`, `plans/`, `.git` — and **not**
  `corpus/routed-findings.jsonl`.
- **C2 lane read-set (635 entries):** does **not** contain `PROVINCE.md`,
  `plans/round51-surfaces.json` or `plans/round51_surfaces.py`; it does contain
  `corpus/SOURCES.md` (via the check of row `R42-R4`).
- Intersection excluding `.git` and directory stats: **`corpus/SOURCES.md`** — one shared
  input, discussed in §6.2.

Static corroboration: no ledger `check` string names `PROVINCE.md`,
`plans/round51-surfaces.json` or `plans/round51_surfaces.py` (`grep -c` → 0 for each; the two
rows whose *notes* mention PROVINCE name it as prose, not as a check target).

## 5. Findings

### 5.1 MEDIUM — the C2 owner oracle is a hardcoded 17-name list, not `../shokunin.conf`
*(measured against the frozen counter at `e07f131`; **answered** at the lane tip by the L1's
uncommitted instrument amendment A1 item 3 — see §10, where the amended counter is re-measured
and accepts `tsukuroi` with a 24-name universe. Kept here as the independent reproduction.)*

The claim's predicate says "every `owner` names a fleet lane from `../shokunin.conf` (or
`unowned:integrator`)". `load_owners()` parses the conf with
`^\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{`, but `shokunin.conf` declares lanes as
`LANES="lane|repo|axes"` lines. Measured:

```
owners with conf present: 17
owners with conf absent : 17
identical sets: True
```

so the conf leg never contributes a name, in a clean clone *or* in place. The oracle is the
hardcoded `FALLBACK_OWNERS` set, and it disagrees with the conf's 23 declared lanes in one
direction that matters for this axis:

```
conf LANES (23): aggregator audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama kasegi
                 kengaku kotoba kotodama kumitate lore mado mori protocol revenger souji tabi
                 tameshi tsukuroi
conf-only, REJECTED by the counter (7): audio game-dev-2d game-dev-3d lore mado revenger tsukuroi
```

Demonstrated, not inferred — one row (`R40-R2`, the bwrap-envelope finding, whose honest owner
is host operability) set to a real conf lane:

```
OWNERS attributed=70 unattributed=1
  DETAIL OWNER R40-R2 owner 'tsukuroi' not a fleet lane
PREDICATE R51-C2 fail
```

So an attribution that routes to `tsukuroi`/`mado`/`lore`/`revenger`/`audio`/`game-dev-*` —
all lanes the fleet conf declares — **fails the counter**, while `unowned:integrator` (not a
lane) passes. On the adjacency axis this pushes the honest owner of host-envelope and
scratch-root findings into a catch-all token. Fix is in the counter's conf parser (or the
claim text): the predicate must name what it actually measures.

### 5.2 MEDIUM — C1's `REV` line reports `master`, not the measured tree

`tip_rev()` runs `git -C <lane> rev-parse master`. Measured on the combined branch
(HEAD `2fb5e3a`, `master` `90fd925`):

```
REV 90fd925d49a0d91001c46a00927a6d3eeac559e3      <- printed by the counter
HEAD 2fb5e3a641def6dbdc6415cefe22b97a18141400     <- the tree actually measured
```

Any measurement on a branch other than `master`, or on a detached HEAD (the natural way to
measure a clean clone at a freeze SHA), stamps a receipt with a revision that does not contain
the measured bytes. The landing measurement is only safe if it is taken on `master` itself.
Secondary: `plans/round51_routing.py` prints **no** `REV` line at all (`grep -c REV` → 0), so a
C2 receipt cannot identify its revision from its own output — the seat protocol's
"a `REV <hash>` line for any receipt" is unsatisfiable for C2 as the counter stands.

### 5.3 LOW — the frozen `c2-before.txt` is not the frozen command's output

`python3 plans/round51_routing.py --lane . --run-checks` at the base tip prints 10 summary
lines **plus 223 `DETAIL` lines**; `.ufo/waves/round-51/claims/c2-before.txt` holds the 10
summary lines only (`wc -l` → 10). The C1 before receipt (21 lines) is complete and faithful
(diff-verified). So the two "before" receipts were recorded by different procedures; a
verifier cannot compare C2's DETAIL set before/after, and the before/after pairs are not
symmetrical evidence. Neither receipt records its exit code.

### 5.4 LOW — C1's after-target is under-specified by its own predicate

The claims' C1 after-target asks for "coverage 19/19 **plus one new declared surface** (the
live served endpoint found this round)". The predicate never measures a 20th surface: my
clone-A repair added none and printed `PREDICATE R51-C1 pass` with `ROWS 9+10`. The kill rule
("`ROWS` must not fall below 9 and 10") only forbids shrinkage. A landing that silently skips
the new surface still passes — acceptable if intended, but the claim text should not present
it as part of the pass condition.

### 5.5 LOW — every ledger check was cwd-relative and dead under the counter
*(**answered** at the lane tip by amendment A1 item 1, which runs checks with `cwd=<lane>`;
under that amendment the 61 pre-existing checks revive and the `"$LANE"` rewrite is no longer
required — see §10. The `R42-R4` fail-open shape is still worth knowing: with `cwd=<lane>` the
`git diff` leg evaluates, so an in-place `corpus/SOURCES.md` edit now flips it red, as §6.3
measured.)*

The counter runs each `check` with `cwd=<scratch tmp>`. All 61 non-empty frozen checks that
reference lane paths fail there (`grep: SKILL.md: No such file or directory`,
`python3: can't open file '<tmp>/plans/…'`), and one (`R42-R4`) fails *open*: `git diff
d69452cf..HEAD` outside a repository prints to stderr, `grep -c '^-[^-]'` yields `0`, and
`test 0 -eq 0` passes — a vacuous clause that reports `fixed-verified`. Rewriting the 61
checks to `"$LANE/…"` / `git -C "$LANE"` / `--lane "$LANE"` is part of the attribution work,
not cosmetic: without it no row can honestly be `fixed-verified`. (`R42-R4`'s `git` sits inside
`$(…)`, so a naive "prefix a leading `git`" rewrite leaves it dead — the `-C` must be applied
to every git invocation.)

## 6. Residual risk and verification gaps

1. **C2's `fixed-verified` leg is self-attested.** `VERIFIED ran=40 passed=40` means my 40
   checks exit 0 *in this run*; it does not mean the 40 defects are fixed. Several are
   pass-conditions I inherited (e.g. `R42-R3-07`'s `! grep -qF …` passes because the row was
   already corrected) and the counter cannot tell an honest pass from a vacuous one — §5.5
   is the worked example.
2. **`accepted-risk` is an unmeasured bucket.** 27 rows carry it; the counter asks nothing of
   them beyond a non-empty check. A landing could mark all 27 `accepted-risk` and pass. The
   claims should either bound that bucket or require a `blocker`/`note` rationale.
3. **The one shared file is live in one direction.** `corpus/SOURCES.md` is read by both
   counters (C1: SF14 count probe; C2: row `R42-R4`'s `git diff d69452cf..HEAD`). Controlled
   experiment on the combined clone: a committed in-place edit of one SOURCES row turned C2
   red —
   ```
   VERIFIED ran=40 passed=39 failed=1
     DETAIL CHECK_FAILED R42-R4 fixed-verified but check exits nonzero
   PREDICATE R51-C2 fail
   ```
   Neither claim's landing touches SOURCES.md (C1 only *describes* its row count), so this
   does not fire; but if the L1's integration edits SOURCES.md in place, C1 flips
   `NUMBER-DRIFT` **and** C2 flips `CHECK_FAILED`. The claims' sentence "neither counter reads
   the other's files" is true as written and should be read as "no shared *surface*", not
   "no shared input".
4. **Point-in-time probes.** C1's `port`/`http`/`paths` probes and the shim digest are host
   facts; the experiment inherits the claims' declared limit. My run reproduced the recorded
   `present=13 absent=6` census exactly, so nothing moved between the freeze and now.
5. **Not tested here (other seats' scope):** the ten frozen controls (declare-all-absent,
   drop-one-entry, stale-pin, undated-absence, do-nothing; strip-owner, fake-fix,
   absorbed-routed, empty-check, do-nothing), the `prose` readings row by row, and whether the
   71 attributions name the *right* owner. My clone-B ledger is a passing vehicle, not a
   proposal.

## 7. Limits

- One machine, one moment (2026-10-28). Both counters are deterministic over their inputs
  except for the host probes noted above.
- The clones are ephemeral: they were removed before yield, so the three commits
  (`90fd925`, `131c9ec`, `2fb5e3a`) are not fetchable from this report. The C1 patch is 9
  changed lines (recipe in §2, reproducible by hand); the C2 change is a 71-row rewrite
  governed by the rule in §2 and the histogram there.
- `git clone --shared` gives the clones the lane's full object database, so `cat-file`,
  `git diff <old>..HEAD` and `close`-ref resolution behave as in a real clone.
- No pacman transaction was run (host guard); no tool was installed or upgraded — nothing was
  needed (`strace` and `python3` were already present).
- I did not read the wave's other seats' reports and did not edit any production file; the
  only file I wrote in the lane tree is this report.

## 8. Scratch

`/fast/scratch/hyaku/kengaku-r51/RevSeparability` (`TMPDIR` pointed there for every run;
`fleet/laneA`, `fleet/laneB`, `receipts/`, `work/`, `work2/`, the two helper scripts and the
ledger backup) was removed after the measurements above were copied into this report. **No
scratch tree is left on disk.**

## 9. Concurrent lane changes observed during this seat (disclosure)

The lane is live. Between my clones and the end of this seat, three tracked files changed under
me and none of the changes is mine (`git -C <lane> status --porcelain`; mtimes read at 15:38–15:39):

| file | mtime | size of change |
|---|---|---|
| `plans/round51_routing.py` | 15:33 | +18/−5 |
| `corpus/SOURCES.md` | 15:37 | +1 |
| `plans/round-51-claims.md` | 15:38 | +49 |

The counter diff is the L1's **instrument amendment A1** (check `cwd=<lane>` instead of a scratch
tmp; 60 s → 90 s; owner universe = curated set ∪ the `id|` rows of `shokunin.conf` ∪ every
`*-shokunin` directory; `--ledger` resolved); the claims diff is **A1 + ledger amendment A2**
(75 rows at landing). A1 says "The C1 instrument is unchanged", so §5.2 stays open; §5.1 and
§5.5 are exactly A1 items 3 and 1, found here independently against the frozen counter.

Consequences for this report, measured:

1. **The four cells above are against the frozen instruments** at `e07f131` — what my item names —
   not against the amended working tree.
2. **The matrix survives the amendment.** Re-running both clones with the amended counter copied
   in: C1-only → `FIELDS complete=0 incomplete=71`, `PREDICATE R51-C2 fail`, exit 1; C2-only →
   `OWNERS attributed=71`, `VERIFIED ran=40 passed=40 failed=0`, `PREDICATE R51-C2 pass`, exit 0.
   Separability is not an artefact of the frozen cwd/owner bugs.
3. **The owner fix is confirmed.** Amended universe: 24 names, `tsukuroi` present; the row the
   frozen counter rejected now reads `OWNERS attributed=71 unattributed=0`, `PREDICATE R51-C2 pass`.
4. **A2 is not yet in the tree.** The lane's `corpus/routed-findings.jsonl` is still the frozen
   71-row file (`wc -l` → 71; rows carrying `owner` → 0) at 15:39, so A2's "the landed ledger
   carries 75" describes a pending landing. My C2 cell is measured on the 71-row artifact the
   frozen claims name; four appended, owned rows cannot change the separability argument (C2's
   read-set contains no C1 file), but that 75-row run is unmeasured here.

## 10. Verdict

C1 and C2 are causally separable as claimed: with only C1's repairs landed, C1 prints
`PREDICATE R51-C1 pass` (exit 0) and C2 stays red at exactly its before numbers; with only
C2's attribution landed, C2 prints `PREDICATE R51-C2 pass` (exit 0) and C1 stays red with an
output byte-identical to `c1-before.txt` modulo its `REV` line. The measured read-sets are
disjoint on every claim-owned file. No coupling defect in the claims' separability paragraph.
Two instrument defects surfaced on the way: C2's owner oracle could not name seven real fleet
lanes (§5.1) — answered at the lane tip by amendment A1 item 3 and re-measured here under the
amended counter — and C1's `REV` line stamps `master` rather than the measured tree while C2
stamps nothing (§5.2), which A1 leaves untouched and which the landing measurement must account
for (measure on `master`, or add a REV line to C2).

REV 90fd925d49a0d91001c46a00927a6d3eeac559e3   (C1-only landing; clone A `master`)
REV 131c9ec27d49503a31dd69f6f534874e68ecf5b6   (C2-only landing; clone B `master`)
REV 2fb5e3a641def6dbdc6415cefe22b97a18141400   (combined; clone A branch `combined`, counter printed `REV 90fd925…` — §5.2)
REV e07f131cf7037e58a21db6e1f3986cf401ad257c   (stage-1 freeze both clones started from)

VERDICT: PASS — C1 and C2 are separable (each passes alone, each leaves the other red) against both the frozen and the amended C2 counter; the only instrument defect left open in my scope is C1's `REV` stamp (§5.2).
