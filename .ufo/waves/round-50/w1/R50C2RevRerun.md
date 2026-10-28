# R50C2RevRerun — independent rerun of the C2 counting command (R50-C2, calibration)

Seat: `R50C2RevRerun` (reviewer, leaf). Assignment: rerun `plans/round50_c2_audit.py` and its `--selftest` on a
clean clone at the freeze commit, then on a scratch copy with the corrections block appended to `SCORECARD.md`;
report `POINTERS … unresolved=` before and after, exit codes, and whether the selftest still proves the check can
fail.

## Axes named

- **Primary (the one I judge): calibration** — does every artifact pointer the three self-assessment files carry
  resolve, and does the counting command that says so measure what it claims?
- **Instrument soundness of that same axis** — false-clean and false-unresolved shapes in the pointer leg.
- **Not in scope / not touched:** novelty (C1), the fence, the population, mutants, sealed modules. No production
  file was edited. No commit, push, stash, checkout of the live lane, no sibling repo, no fleet-root tracked file.

## Revisions measured (REV)

```
REV lane           = /home/vgpnk/Projects/shokunin/kengaku-shokunin  HEAD=c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
REV freeze         = 3b02d573d58cc6d2e0d27ef92ac0815354912252  (merge-base --is-ancestor 3b02d57 HEAD -> yes, rc=0)
REV base lane tip  = 71f5f5f77591d8c3d19297ee9785436da45209e4
REV measure clone  = git clone --shared of the lane, checkout 3b02d573d58cc6d2e0d27ef92ac0815354912252, dirty=0
REV instrument     = plans/round50_c2_audit.py sha256 b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef
                     (identical at 3b02d57 and c3372a9b: `git show <rev>:plans/round50_c2_audit.py | sha256sum`)
REV SCORECARD      = f7c3d46840091660c43187d378070760e9e9ba807d3dd08779433200cbe8b67d at 3b02d57
```

Scratch: `/fast/scratch/hyaku/kengaku-r50/R50C2RevRerun` (TMPDIR exported there; all clones under it; removed
before yield — see Limits).

## Before / after, verbatim

### B1 — before, on a clean clone at the freeze (HEAD = 3b02d57, clean tree)

Command (cwd = the clone): `TMPDIR=$S python3 plans/round50_c2_audit.py --lane .`

```
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
EXIT=1
```

The `TIP` line prints `c3372a9b` while HEAD is `3b02d57` because the audit derives the tip from `origin/HEAD`
(`plans/round50_c2_audit.py:75`) — see F5.

### B2 — before, the claim's own `71f5f5f` figure (reproduced)

The counter does not exist at `71f5f5f` (`git cat-file -e 71f5f5f:plans/round50_c2_audit.py` fails), so I ran the
freeze's copy against a separate clone checked out at `71f5f5f`:

`python3 plans/round50_c2_audit.py --lane <clone-at-71f5f5f>`

```
TIP 71f5f5f77591d8c3d19297ee9785436da45209e4 branch=HEAD
POINTERS total=271 paths=213 hashes=58 resolved=259 exists=201 superseded=0 never-landed=0 unresolved=12
EXIT=1
```

This matches `plans/round-50-claims.md` §C2 Before (`total=271 paths=213 hashes=58 resolved=259 … unresolved=12`)
and the do-nothing non-reachability line (`unresolved=12`, exit 1) exactly. Same 12 unresolved names as B1.

### A1 — after, freeze tree + corrections block appended (scratch copy, `SCORECARD.md` modified only)

Block extracted verbatim as `git show c3372a9b:SCORECARD.md | sed -n '/^## Round 50 — C2 corrections/,$p'`
(33 lines) and appended to the freeze copy's `SCORECARD.md`; `git status --porcelain` → ` M SCORECARD.md`.

`python3 plans/round50_c2_audit.py --lane .`

```
TIP 3b02d573d58cc6d2e0d27ef92ac0815354912252 branch=HEAD
POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0
EXIT=0
```

### A2 — after, at the landing tip (clone checked out at `c3372a9b`)

`python3 plans/round50_c2_audit.py --lane .`

```
TIP c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 branch=master
POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0
EXIT=0
```

The claim's after-line (`POINTERS total=… unresolved=0`, exit 0) reproduces on both trees.

### S1 / S2 — `--selftest`

At the freeze (S1):

```
SELFTEST pristine_rc=1 bogus_rc=1 new_unresolved=['plans/round50_selftest_bogus.py'] verdict=ok
EXIT=0
```

At the landing tip (S2):

```
SELFTEST pristine_rc=0 bogus_rc=1 new_unresolved=['plans/round50_selftest_bogus.py'] verdict=ok
EXIT=0
```

**Yes — the selftest still proves the check can fail at the tip**: the bogus pointer is the only new unresolved
row and the dirty copy exits 1. At the freeze the same selftest reported `verdict=ok` with `pristine_rc=1`, i.e.
green selftest on an already-red surface (F4). No temp dir leaked: `ls $TMPDIR | grep -c k50-c2` → `0`.

## Independent verification of the claim's own kill rules (all exercised, not restated)

| check | command shape | observed |
|---|---|---|
| `never-landed` row truthful (9 rows) | `git -C <lane> log --all --oneline -- <pointer> \| wc -l` for each of `corpus/evidence/analyze.py`, `corpus/knowledge/repo-git-state.md`, `plans/round34_{c1_verify,defects,mutate}.py`, `plans/round48_{c1,c2}_verify.py`, `plans/round49_{c1,c2}_verify.py` | `history_rows=0` for all nine, against the **widest** ref set (the lane's `--all`, incl. `refs/jj/keep/*`) |
| `SUPERSEDED` targets exist (3 rows) | `git cat-file -e c3372a9b:<target>` | `corpus/defects.jsonl`, `corpus/evidence/round9-replication/predictions-r9.md`, `corpus/routed-findings.jsonl` → all exist |
| append-only (no rewrite) | `git diff --numstat 71f5f5f 3b02d57 -- SCORECARD.md` / `3b02d57 c3372a9b -- SCORECARD.md` | `12	0` and `34	0` (zero deletions); block at lines 2136–2168 of a 2168-line file = EOF; `grep -c '^SUPERSEDED '` → `12` |
| bad `SUPERSEDED` target must stay unresolved | appended `SUPERSEDED plans/round48_c1_verify.py -> plans/round48_c1_verify_landed.py` on a copy | `unresolved=3` incl. `UNRESOLVED plans/round48_c1_verify.py`, exit 1 — rule holds |
| `never-landed` lie (path IS in history) must stay unresolved | appended `SUPERSEDED corpus/evidence/round45/tb2-password-recovery/environment/setup.sh -> never-landed` (absent at tip, 7 history rows) | `UNRESOLVED corpus/evidence/round45/tb2-password-recovery/environment/setup.sh`, `unresolved=1`, exit 1 — rule holds |
| hash leg can fail | appended a bogus 40-hex | `UNRESOLVED-HASH 0000000000000000000000000000000000000000 missing`, exit 1 |
| 59 hashes resolve and are ancestors of tip (independent of the script) | re-extract `(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])` from the three files at `c3372a9b`, then `git cat-file -e` / `merge-base --is-ancestor` | `hashes 59 · missing 0 · not_ancestor_of_tip 0` |

## Findings by severity

### F1 — MEDIUM (instrument soundness; the leg C2 rests on). The pointer regex truncates `.jsonl` → `.json` and can admit a false clean.

`plans/round50_c2_audit.py:42` lists `json` before `jsonl`, and `TOKEN` (`:43-45`) has a lookbehind but **no
right-hand boundary** after the extension. So every `…jsonl` pointer in the surface is scanned as `…json`.

Measured consequences:

1. **False unresolved (present today, 2 of 12).** At `3b02d57` and `71f5f5f` the three files contain only
   `corpus/defects.jsonl` (3×) and `corpus/routed-findings.jsonl` (7×) — verified with
   `grep -o 'corpus/[a-z-]*\.jsonl\?'` and with `grep -n 'corpus/defects\.json[^l]'` → no match (rc=1). Yet the
   audit prints `UNRESOLVED corpus/defects.json` and `UNRESOLVED corpus/routed-findings.json`. Two of the twelve
   frozen "before" rows and two of the twelve correction rows therefore correct a *scanner artifact*, not a
   dangling pointer; the correction rows point at the very `.jsonl` files the text already names. The real
   dangling set is **10**, not 12.
2. **False clean (latent, demonstrated).** On a copy I appended `plans/round50_falseclean.jsonl` (a pointer with
   no file):

   ```
   POINTERS total=278 paths=219 … unresolved=1
   UNRESOLVED plans/round50_falseclean.json
   EXIT=1
   ```

   then created an empty sibling `plans/round50_falseclean.json` while `plans/round50_falseclean.jsonl` still did
   not exist (`ls` → `No such file or directory`):

   ```
   POINTERS total=278 paths=219 hashes=59 resolved=278 exists=207 superseded=3 never-landed=9 unresolved=0
   EXIT=0
   ```

   A dangling pointer is reported resolved. That is exactly the shape the C2 kill rule ("any unresolved pointer")
   assumes cannot pass. It does not falsify today's green (no such sibling exists at `c3372a9b`), but the counting
   command carries a false-clean path on its only leg.
3. **Latent extension blind spot.** `EXTS` omits `.adoc`, `.yml`, `.html`, `.csv`, `.log`, `.repo`. Broad-regex
   scan of the three files at the freeze: exactly 4 non-`EXTS` matches, all existing —
   `corpus/evidence/attrib-r23-stream.log`, `corpus/evidence/round9-replication/predictions-r9.sha256.repo`
   (plus the two truncated `.jsonl` forms above). So no pointer is currently invisible, but a future dangling
   `.adoc` pointer — including the round's own `corpus/evidence/round50/*.adoc` — would be outside the surface.

Fix (open-window repair, C2's own instrument row): order extensions longest-first and add `(?![\w])`, then
re-measure — the before number moves 12→10 and the two `.json` correction rows become inert but harmless.

### F2 — LOW (documentation). Correction block mis-cites its own before number.

`SCORECARD.md:2139` says "the before measurement (`POINTERS total=275 … unresolved=12`) are frozen in
`plans/round-50-claims.md` §C2". §C2 (and `SCORECARD.md:2134`) record `total=271` at `71f5f5f`. `275` is the
receipt number on tree `f7281bc` (`.ufo/waves/round-50/claims/c2-before.txt`, `TIP f7281bc…`). Both are red with
`unresolved=12`, so the claim is not harmed, but the citation is wrong.

### F3 — LOW (selftest coverage). The hash leg is never exercised for failure.

`plans/round50_c2_audit.py:125,128` both call `audit(…, check_hashes=False)`, so the 59 hash items (21 % of the
277-item surface) are not part of what `--selftest` proves. The leg does fail correctly when exercised (see the
`UNRESOLVED-HASH … missing` probe), so this is coverage, not a broken check.

### F4 — LOW (selftest semantics). A green selftest coexists with a red surface.

`selftest()` compares only the delta `dirty_bad - clean_bad`; `clean_rc` is never asserted. Observed at the
freeze: `pristine_rc=1` (12 unresolved) and `verdict=ok`, exit 0. The claims' requirement ("the bogus pointer is
the only new unresolved row") is satisfied literally; the corollary "a green selftest means the surface is clean"
is false.

### F5 — LOW (reproducibility). Hash ancestry is measured against the branch tip, not the measured revision.

`audit()` takes `tip` from `origin/HEAD` (`:75`) with a `master`/`HEAD` fallback. On a detached checkout of
`3b02d57` in a clone whose `master` is at `c3372a9b`, the audit printed `TIP c3372a9b … branch=master` (B1). All
59 hashes are ancestors of `3b02d57` as well (A1 in the second-level clone, where `TIP 3b02d57 branch=HEAD` —
`resolved=277`), so the result is right here, but a re-run at an older revision silently checks the wrong tip.

### F6 — LOW (correction resolution semantics). Last `SUPERSEDED` row wins, silently.

`superseded_map` (`:65`) is a dict keyed by pointer, so an appended second row overrides the first. Observed in
the bad-target probe: inserting `SUPERSEDED plans/round48_c1_verify.py -> …` dropped `never-landed` from 9 to 8
with no conflict report. Consistent with append-only discipline, but a stray row can disable a correct earlier one
without any signal from the audit.

## Lane worktree state at measurement (read-only note)

`git -C <lane> status --porcelain` at the time of this run listed 5 entries — ` M plans/round50_c1_verify.py`,
`?? corpus/evidence/round50/c1-receipt.txt`, `?? .ufo/waves/round-50/w1/`, `w1.ready`, `w1.ready.partial`. The
live worktree was therefore dirty, so every C2 number above comes from a clean `--shared` clone checked out at
`3b02d57` / `c3372a9b`, never from the lane worktree. `plans/fixture_fence.py` was **not** among the modified
files at that moment (relevant to peer `R50C1ExecRepair`'s C1 note claiming an uncommitted fence rewrite in the
lane; C1 is not my item and I did not measure it).

## Residual risk

- The C2 green is a property of the *pointer surface as the regex sees it*, not of the files' text. F1(b) shows a
  reading where `unresolved=0` while a named artifact does not exist; today's tip does not contain that shape, so
  the measured green is not falsified, only unsupported by a bounded instrument.
- The two artifact correction rows are vacuous rather than dangerous: their `SUPERSEDED` targets keep the raw
  `.jsonl` spelling (`\S+`, `plans/round50_c2_audit.py:46`), so target existence is checked on the real file —
  deleting `corpus/defects.jsonl` or `corpus/routed-findings.jsonl` would turn those rows red. The standing
  false-clean exposure is only F1(b): text naming a `.jsonl` pointer whose `.json` sibling exists. No such shape
  exists at `c3372a9b` (checked: neither `corpus/defects.json` nor `corpus/routed-findings.json` exists).

## Verification gaps (what I did not do)

- I did not run the C1 counter, the fence, the population, mutants or sealed modules (out of scope, other seats).
- I did not measure the `.ufo/waves/...` receipts cited by C2's own text: the audit's frozen surface is
  `plans/`/`corpus/` + 40-hex only, so `c2-before.txt` / `c2-selftest.txt` are outside the predicate. (The C2
  claim's surface sentence says the same; recorded so no reader assumes otherwise.)
- I did not test whether every *resolved* pointer points at the semantically right artifact (F2-style naming);
  only existence/ancestry is mechanically checkable.
- Findings rest on `read`/`bash`/`git`; no `lsp` server was engaged for this item (a Python language server would
  not add semantic evidence about a regex over Markdown — recorded per the reviewer contract).

## Limits

- One live clone was used for measurement plus 4 short-lived `--shared` clones for the copy probes (c2..c6), all
  under `/fast/scratch/hyaku/kengaku-r50/R50C2RevRerun`; nothing under `/tmp`; no fixture git env exported.
- Every git call was `git -C <dir>` with `dir` inside my scratch, or a read-only query (`log --all`, `cat-file`,
  `diff`, `show`, `rev-parse`, `merge-base`) against the live lane. `git status --porcelain` on the live lane was
  not modified by me; my measurement clone ended `0` dirty lines.
- Scratch tree removed before yield: `/fast/scratch/hyaku/kengaku-r50/R50C2RevRerun` (verified absent afterwards).

## VERDICT

R50-C2's after-predicate **reproduces exactly** on a clean clone at the freeze with the corrections block appended
(`unresolved=0`, exit 0) and at the landing tip `c3372a9b` (`unresolved=0`, exit 0); the before is `unresolved=12`,
exit 1 at both `3b02d57` and `71f5f5f`; and `--selftest` **still proves the check can fail** (bogus row is the only
new unresolved; exit 0, `verdict=ok`). All four kill rules I probed fire. **However** the counting command's
pointer regex truncates `.jsonl`→`.json`, which (i) makes 2 of the 12 frozen before-rows and 2 of the 12 correction
rows artifacts and (ii) admits a demonstrated false-clean shape (`F1`); F2–F6 are minor. Recommendation (not an
admission): **C2's predicate holds as measured**, and `F1` should land as an open-window repair to
`plans/round50_c2_audit.py` with the before count re-measured (12→10) before the round is scored, since fixing the
regex moves the instrument's own numbers.
