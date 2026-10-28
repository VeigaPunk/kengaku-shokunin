# R50C2CritNonVacuity — C2 (calibration) non-vacuity attack

REV: freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` (verified ancestor of the lane tip at measurement:
`git merge-base --is-ancestor 3b02d57… HEAD` → 0, branch tip `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1`, reported by
the audit itself as `TIP c3372a9b…`). `plans/round50_c2_audit.py` sha256
`b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef` (identical at the freeze and at the tip);
`plans/fixture_fence.py` at the freeze `05d5fe03…` (untouched by this seat).

Axes named: **calibration** (C2's own axis; the attack is on whether `unresolved=0` is evidence of
"every row's pointer re-runs"). Novelty/C1 is out of scope here: nothing below touches `plans/fixture_fence.py`,
`plans/honest50/`, `plans/mutants50/`, `plans/sealed50/` or `plans/round50_c1_verify.py`.

Outcome in one line: **the audit can be made green, exit 0, with all 12 unresolved pointers untouched — by
appending 12 correction rows whose targets are unrelated existing files or directories. It also goes green while
the SCORECARD carries a `never-landed` row for a path that IS in history, if a second row for the same pointer
follows it.** Both are *false cleans*, i.e. exactly the repair class the claim's open window authorises
("a leg that cannot run, a false clean, an unreproducible fixture").

## Environment (host rules honoured)

- Scratch: `/fast/scratch/hyaku/kengaku-r50/R50C2CritNonVacuity`, `TMPDIR` exported there, removed before yield
  (`VERDICT` line records it). One `git clone --shared` of the lane at the freeze; all variant trees are
  `cp -a --reflink=auto` copies of that clone; every fixture write asserted
  `git rev-parse --show-toplevel` == the fixture dir first.
- No `GIT_CONFIG_GLOBAL` / `GIT_*_AUTHOR` exports; no pacman; no tool installed; no writes outside this report
  and my scratch; no commit/push/checkout/reset in the lane (fixture commits only, inside scratch copies).
- Read-only against the lane: the lane working tree was dirty from sibling seats (`M plans/fixture_fence.py`,
  `M plans/round50_c1_verify.py`, …), so every measurement was taken on my clone at the freeze commit, never on
  the live checkout.

## Commands run (exact, each against my clone unless stated)

Fast leg / control (tree = freeze, refs = `master`):

```
$ S=/fast/scratch/hyaku/kengaku-r50/R50C2CritNonVacuity
$ git clone --shared --no-hardlinks -q /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane50"
$ cd "$S/lane50" && git checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252
$ python3 plans/round50_c2_audit.py --lane .
TIP c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 branch=master
POINTERS total=275 paths=216 hashes=59 resolved=263 exists=204 superseded=0 never-landed=0 unresolved=12
UNRESOLVED corpus/defects.json
UNRESOLVED corpus/evidence/analyze.py
UNRESOLVED corpus/evidence/round9-replication/predictions-r9.sh
UNRESOLVED corpus/knowledge/repo-git-state.md
UNRESOLVED corpus/routed-findings.json
UNRESOLVED plans/round34_c1_verify.py
UNRESOLVED plans/round34_defects.py
UNRESOLVED plans/round34_mutate.py
UNRESOLVED plans/round48_c1_verify.py
UNRESOLVED plans/round48_c2_verify.py
UNRESOLVED plans/round49_c1_verify.py
UNRESOLVED plans/round49_c2_verify.py
RC=1
```

Each variant below is a `cp -a --reflink=auto lane50 vX` copy, then the named append, then the same command.
The `TIP` line is identical in every run (`c3372a9b…`); only the counts move.

### Variant B — point each of the 12 rows at an unrelated existing file or directory

```
$ cd "$S/vB" && cat >> SCORECARD.md <<'EOF'

## Round 50 — C2 corrections

SUPERSEDED plans/round48_c1_verify.py -> plans/round45_c1_verify.py
SUPERSEDED plans/round48_c2_verify.py -> plans/round46_c1_verify.py
SUPERSEDED plans/round49_c1_verify.py -> plans/round46_c1_verify.py
SUPERSEDED plans/round49_c2_verify.py -> SCORECARD.md
SUPERSEDED plans/round34_c1_verify.py -> .
SUPERSEDED plans/round34_defects.py -> plans
SUPERSEDED plans/round34_mutate.py -> corpus/QUALITY.md
SUPERSEDED corpus/defects.json -> corpus/defects.jsonl
SUPERSEDED corpus/routed-findings.json -> corpus/routed-findings.jsonl
SUPERSEDED corpus/evidence/analyze.py -> .ufo
SUPERSEDED corpus/evidence/round9-replication/predictions-r9.sh -> corpus/SOURCES.md
SUPERSEDED corpus/knowledge/repo-git-state.md -> corpus/knowledge
EOF
$ python3 plans/round50_c2_audit.py --lane .
POINTERS total=275 paths=216 hashes=59 resolved=275 exists=204 superseded=12 never-landed=0 unresolved=0
RC=0
```

**ACCEPTED — green, exit 0, with zero real fixes.** Every target was verified to exist and none of them is the
promised counter: `plans/round45_c1_verify.py` is *round 45's* counter, `plans/round46_c1_verify.py` is round
46's, `SCORECARD.md`, `.`, `plans`, `.ufo`, `corpus/knowledge` are not artifacts at all (two are directories).
This is a **defect (D1)**: `audit()`'s only target test is `(lane / target).exists()`, so "resolves" degenerates
to "some path exists". The claim's predicate is the calibration rubric's condition (c) — *"this file exists and
every row's pointer re-runs"* — and the pointer demonstrably does not re-run.

### Variant A — `SUPERSEDED <pointer> -> never-landed` for a pointer that IS in history

Fixture (scratch copy `vA`, toplevel asserted == `$PWD`; two fixture commits — the only commits I made anywhere):

```
$ git add plans/round48_c1_verify.py && git -c user.name=crit -c user.email=crit@local commit -qm "fixture: land round48 c1 verify (stub)"
$ git rm -q plans/round48_c1_verify.py && git -c user.name=crit -c user.email=crit@local commit -qm "fixture: remove round48 c1 verify"
$ git log --all --oneline -- plans/round48_c1_verify.py
629473c fixture: remove round48 c1 verify
d81e28a fixture: land round48 c1 verify (stub)
```

then all 12 pointers appended as `-> never-landed`:

```
### VARIANT A: never-landed for a pointer that IS in history (all 12 marked never-landed)
POINTERS total=275 paths=216 hashes=59 resolved=274 exists=204 superseded=0 never-landed=11 unresolved=1
UNRESOLVED plans/round48_c1_verify.py
RC=1
```

**REFUSED (correctly), and the refusal is surgical**: exactly the one in-history pointer stays unresolved while
the eleven genuinely-never-landed rows are accepted. On a *complete* clone the frozen history guard works.

### Variant A+C — the same lie hidden behind a duplicate row

```
SUPERSEDED plans/round48_c1_verify.py -> never-landed
SUPERSEDED plans/round48_c1_verify.py -> plans/round45_c1_verify.py
```

```
### VARIANT C on the in-history pointer: false never-landed row first, real target second
POINTERS total=275 paths=216 hashes=59 resolved=275 exists=204 superseded=1 never-landed=11 unresolved=0
RC=0
```

**ACCEPTED — green, exit 0, with a `never-landed` row for a path that is in history** (`d81e28a`, `629473c`).
`superseded_map()` is a dict comprehension in file order, so the last row for a pointer silently wins
and no duplicate/conflict is reported. This violates the claim's frozen kill rule ("a `never-landed` row for a
path that is in history") while the audit exits 0. **Defect (D2).**

### Variant C — duplicate corrections, contradictory values

```
SUPERSEDED plans/round48_c1_verify.py -> plans/round_does_not_exist_xyz.py
SUPERSEDED plans/round48_c1_verify.py -> plans/round50_c2_audit.py
SUPERSEDED plans/round49_c1_verify.py -> plans/round50_c2_audit.py
SUPERSEDED plans/round49_c1_verify.py -> plans/round50_c2_audit.py
SUPERSEDED plans/round49_c2_verify.py -> never-landed
SUPERSEDED plans/round49_c2_verify.py -> plans/round46_c1_verify.py
SUPERSEDED plans/round48_c2_verify.py -> plans/round46_c1_verify.py
SUPERSEDED plans/round48_c2_verify.py -> plans/round_does_not_exist_xyz.py
```

```
POINTERS total=276 paths=217 hashes=59 resolved=266 exists=204 superseded=3 never-landed=0 unresolved=10
UNRESOLVED … plans/round48_c2_verify.py
UNRESOLVED plans/round_does_not_exist_xyz.py
RC=1
```

Partly refused, partly accepted: (a) duplicate *identical* rows are silently idempotent (`round49_c1`),
(b) `never-landed` followed by an existing target is accepted with the contradiction unreported (`round49_c2`),
(c) a nonexistent target is caught twice — the pointer stays unresolved *and* the target string itself becomes a
scanned pointer (`total` 275→276, `plans/round_does_not_exist_xyz.py` listed) — which is a genuinely good
self-limiting property, and (d) order matters: a good row followed by a bad one **fails** while a bad row followed
by a good one **passes**. So D2 is not a green-by-itself, it is a masking primitive: it converts any frozen
kill-rule violation into an invisible one, and combined with D1 it turns red into green.

### Variant A′ — `never-landed` rows for pointers that exist at the tip (invisible rows)

```
SUPERSEDED plans/round50_c2_audit.py -> never-landed
SUPERSEDED plans/round45_c1_verify.py -> never-landed
```
(`plans/round50_c2_audit.py history_commits=1 exists_at_tip=yes`; `plans/round45_c1_verify.py history_commits=1 exists_at_tip=yes`)

```
POINTERS total=275 paths=216 hashes=59 resolved=266 exists=206 superseded=1 never-landed=0 unresolved=9
RC=1
```

**ACCEPTED in the only sense that matters**: `never-landed=0` — the two false rows are neither flagged nor even
counted, because the `exists` branch never consults the map. The audit's summary cannot reveal that they exist.
**Defect (D2′)** — the frozen kill rule forbids these rows, and no leg sees them.

### Variant D — the pointer satisfied by a DIRECTORY and by a 0-byte file

```
$ mkdir -p plans/round48_c1_verify.py && : > plans/round49_c1_verify.py
drwxr-xr-x 2 vgpnk vgpnk 6 Oct 28 14:39 plans/round48_c1_verify.py
-rw-r--r-- 1 vgpnk vgpnk 0 Oct 28 14:39 plans/round49_c1_verify.py
POINTERS total=275 paths=216 hashes=59 resolved=265 exists=206 superseded=0 never-landed=0 unresolved=10
RC=1
```

**ACCEPTED**: `exists` 204→206, both pointers leave the `UNRESOLVED` list. A directory named
`plans/round48_c1_verify.py` and an empty file count as "the counter landed". This is the exact failure C2 exists
to catch — r49's row admits "no counter at landing". **Defect (D3)**: resolution is `Path.exists()`, with no
regular-file, non-empty, or re-runnability test.

**Full green from D3+D1**: 2 stubs + 10 unrelated targets ⇒ `unresolved=0`, exit 0, with `round48_c1_verify.py`
being a directory. (Composition of the two accepted variants; not separately re-run.)

### Variant E — corrections outside the `## Round 50 — C2 corrections` block

A correction block inserted at **line 1162**, i.e. inside `## Round 34 — coverage attempt …` (the R50 heading
follows at 2124 in the same file), all twelve targets = `plans/round50_c2_audit.py` (the audit pointing at itself):

```
inserted at line 1162
### VARIANT E: correction block inserted inside the historical Round-34 section (round 1162), 40+ rounds before the R50 block
POINTERS total=275 paths=216 hashes=59 resolved=275 exists=204 superseded=12 never-landed=0 unresolved=0
RC=0
grep -n "C2 corrections" SCORECARD.md → 1164:## Round 50 — C2 corrections
```

**ACCEPTED.** `superseded_map()` regexes the whole file, so (a) a correction need not be in the round-50 block or
appended at all — the claim's "append-only … in the `## Round 50 — C2 corrections` block" is not measured — and
(b) a row may target the audit itself. **Defect (D4).**

### Variant F — the history guard is clone-relative (verdict flip on identical text)

Fixture `vF`: `refs/heads/side` lands `plans/round48_c1_verify.py` (plumbing only: `hash-object` →
temp-index `read-tree`/`update-index` → `write-tree` → `commit-tree` → `update-ref`); master never has it.

```
$ git -C vF log --all --oneline -- plans/round48_c1_verify.py
013f5de fixture: side-branch lands round48 c1 verify
$ git -C vF log --oneline master -- plans/round48_c1_verify.py | wc -l   → 0
$ git clone --shared -q vF vF_full      # branches: master, remotes/origin/side
$ git clone --shared --single-branch -q vF vF_single   # branches: master only
$ git -C vF_single log --all --oneline -- plans/round48_c1_verify.py   → (empty)
```

Same twelve `never-landed` rows appended to both clones:

```
### vF_full:  all 12 marked never-landed (round48_c1 IS in history on refs/heads/side, absent from master)
POINTERS total=277 paths=218 hashes=59 resolved=276 exists=206 superseded=0 never-landed=11 unresolved=1
UNRESOLVED plans/round48_c1_verify.py
RC=1

### vF_single: all 12 marked never-landed (same rows, same TIP)
POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=0 never-landed=12 unresolved=0
RC=0
```

**ACCEPTED on a single-branch clone — green with a false `never-landed` row for a path that IS in history.**
The frozen definition ("only when `git log --all --oneline -- <pointer>` is empty") is clone-relative and the
audit prints no completeness evidence (no `--is-shallow-repository`, no `remote.origin.fetch`), so the S3
receipt cannot be distinguished from a receipt minted on a narrow clone. **Defect (D5).** Note the hash leg does
*not* rescue this: a full-history single-branch clone resolves all 59 hashes and stays green (measured above:
`hashes=59`, `unresolved=0`).

### Documented correction template is not parseable

```
SUPERSEDED plans/round34_c1_verify.py -> plans/round45_c1_verify.py          # target exists at the tip
SUPERSEDED plans/round34_defects.py -> plans/round45_c1_verify.py
```

```
POINTERS total=275 paths=216 hashes=59 resolved=266 exists=206 superseded=1 never-landed=0 unresolved=9
UNRESOLVED … plans/round34_c1_verify.py
RC=1
```

**REFUSED but silently**: the row in the claim's own documented form (with the explanatory `# …` column shown in
`round-50-claims.md`) is dropped by `^\s*SUPERSEDED\s+(\S+)\s+->\s+(\S+)\s*$`; only the bare row registered
(`superseded=1`). An integrator copying the template literally gets a *false red with no diagnostic*. **Defect
(D6)** — the mirror of D1: quiet rejection as well as quiet acceptance.

## Controls are blind to every hole above

```
$ python3 plans/round50_c2_audit.py --lane . --selftest
…
SELFTEST pristine_rc=1 bogus_rc=1 new_unresolved=['plans/round50_selftest_bogus.py'] verdict=ok
RC=0
```

The claim's only self-check appends one bogus *pointer* to a scratch copy and asserts it is the single new
unresolved row. It never exercises `SUPERSEDED` (no row, no duplicate, no target, no placement), so all of
D1–D6 pass the control set untouched. `pristine_rc=1` also confirms the pre-correction state is red only through
the 12 pointers.

## Provenance of the claim's "Before" line (adjacent, non-blocking)

The claim states `POINTERS total=271 …` "measured at `71f5f5f`" with receipt `c2-before.txt`. Measured:

- The tree at `71f5f5f` scanned with the frozen audit reproduces **exactly** `total=271 paths=213 hashes=58 resolved=259 … unresolved=12` — so the numbers are right for that tree.
- But the tool did not exist there: `git log --all --oneline -- plans/round50_c2_audit.py` → one commit,
  `f7281bc` (the S1 freeze); `git ls-tree 71f5f5f plans/round50_c2_audit.py` → empty.
- And the cited receipt is not at 71f5f5f either: `c2-before.txt` prints `TIP f7281bc…` with
  `total=275 paths=216 hashes=59 resolved=263`, which is what I reproduce at the freeze.

So the "Before" sentence is a retro-computation whose receipt shows different numbers. The do-nothing control
(`unresolved=12`, exit 1) is sound; only its label needs to say "tree `71f5f5f` scanned with the `f7281bc` audit"
and quote the S1 receipt's `275`. **D7 (label, not a kill).**

## Smallest safe correction (open-window repair; predicate sentence and literals unchanged)

The claim's open window allows repairs for "a false clean"; D1–D5 are exactly that, so the repair is authorised
before the first scored C2 run. All changes are inside `audit()`/`superseded_map()`; `FILES`, `EXTS`, the
`POINTERS … unresolved=0` predicate and exit 0 are untouched.

1. **Target identity (D1).** A `SUPERSEDED p -> t` row resolves only if `t` is a regular, non-empty file in the
   same top-level tree as `p` (`plans/*`→`plans/`, `corpus/*`→`corpus/`), `t != p`, `t` is not the audit itself,
   **and the row carries an evidence receipt**: extend the grammar to
   `SUPERSEDED <pointer> -> <target> @ <receipt>` where `<receipt>` is an existing non-empty file whose text
   contains `<pointer>` verbatim. (Cheapest alternative if a grammar change is unwanted: require the target's
   text or name to contain the pointer or the pointer's `round<NN>` token, and print
   `SUPERSEDED-CHECK <pointer> -> <target>` for every row so the judge reads the mapping rather than a count.)
2. **Duplicate/conflict detection (D2, D2′).** Any pointer with more than one `SUPERSEDED` row is
   `UNRESOLVED <p> duplicate-correction` regardless of order; a `never-landed` row whose pointer exists at the
   tip or whose `git log --all` is non-empty is `UNRESOLVED <p> never-landed-but-committed` even when the
   `exists` branch would have short-circuited (parse the map *before* the existence test).
3. **Resolution shape (D3).** Replace `(lane/p).exists()` with
   `p.is_file() and not p.is_symlink() and p.stat().st_size > 0` (and the same for targets).
4. **Row placement and grammar (D4, D6).** Only rows inside the `## Round 50 — C2 corrections` block count;
   every line containing `SUPERSEDED` that the row regex rejects must be printed as `BADROW <line>` and is fatal.
5. **Clone completeness (D5).** Print and require `git rev-parse --is-shallow-repository` = `false` and a
   wildcard `remote.origin.fetch`; otherwise print `CLONE partial=<why>` and exit 2 instead of certifying. Also
   print `rev-list --all --count` in the receipt.
6. Receipt hygiene (D7): print the tree identity being audited (`git rev-parse HEAD` *and* the branch tip) and
   refuse when the three scanned files are dirty, mirroring C1's dirty-tree kill.

Each of 1–5 flips one of my accepted variants red while leaving the honest repair path green (an honest
`never-landed` row for a genuinely absent pointer still passes: measured `never-landed=11` accepted in variant A).
Digest old→new must be recorded in `round-50-claims.md` and the stage-2 commit, per the claim's own rule.

## Limits of this review

- I did not and cannot judge whether the S3 corrections will be honest; I measured only whether the instrument can
  tell honest from dishonest. It cannot, on the five axes above.
- The hash leg (`cat-file -e` + `merge-base --is-ancestor tip`) was not attacked beyond the clone-completeness
  case; a 40-hex token can be satisfied by any ancestor commit, which is the frozen rule, so no defect is claimed.
- All measurements are on copies at the freeze (`3b02d57` tree) or on a clone whose checkout is the tip
  (`c3372a9b`, variants F only, `TIP` line matching the tree there). The live lane working tree is dirty from
  sibling seats and was never measured.
- Fixture commits exist only in my scratch copies (three fixture commits: two in `vA`, one plumbing commit in
  `vF`). The lane was not mutated; `git status` in `lane50` was clean at the freeze.
- `--selftest` output was taken at the freeze; its `TIP 7bca8872…` is the selftest's own scratch commit.

VERDICT: **C2's counter is vacuous on its own predicate as frozen.** Five accepted variants make the audit print
`unresolved=0` and exit 0 (unrelated/directory targets; a false `never-landed` masked by a duplicate row; a
directory or 0-byte file standing in for a counter; a correction block placed in a historical section with the
audit as its own target; a false `never-landed` accepted on a single-branch clone of a repo whose history holds
the path), and two more are silently ignored or silently rejected (a `never-landed` row for an existing pointer;
the claim's own commented row template). Three variants are correctly refused (a `never-landed` row for an
in-history pointer on a complete clone; an unresolvable pointer; a nonexistent target, which also surfaces as its
own unresolved token). **Recommendation to the L1/canonical judge: do not admit C2 on `unresolved=0`/exit 0 as
frozen.** Either repair `plans/round50_c2_audit.py` under the open window (items 1–5 above, with old→new digest
recorded) or weaken the claim text to "every pointer resolves to an existing path" and re-state condition (c) as
unmet. As written, the audit's green is not evidence that "every row's pointer re-runs", so the calibration
8→9 step would rest on a measurement that a dishonest SCORECARD can satisfy without changing a single artifact.

Scratch: `/fast/scratch/hyaku/kengaku-r50/R50C2CritNonVacuity` was removed before yield (this report and its
transcribed receipts are the only artifacts; nothing citable was left in `/tmp`).
