# R36NestedPaths — nested `.ufo/waves/` path census, citation safety, jj deletion semantics

Seat: R36NestedPaths (executor, leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
All commands run from the lane root unless the path is absolute. Tip measured: `f9efce3` (`round-36: wave-1 spec and dispatch (40 seats)`), worktree `master`.

## 1. The 21 committed paths matching `^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-`

Command:

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only master \
  | grep -E '^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-' | cat -n
```

Output: 21 lines (persisted verbatim at `.ufo/waves/round-36/build/R36NestedPaths/nested-21.txt`, `wc -l` = 21):

```
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a3/.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a3/.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a3/.ufo/waves/round-34/claims/control-c1.txt
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a4/.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a4/.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a4/.ufo/waves/round-34/claims/control-c1.txt
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a5/.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a5/.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a5/.ufo/waves/round-34/claims/control-c1.txt
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a6/.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a6/.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a6/.ufo/waves/round-34/claims/control-c1.txt
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a7/.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a7/.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a7/.ufo/waves/round-34/claims/control-c1.txt
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a8/.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a8/.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a8/.ufo/waves/round-34/claims/control-c1.txt
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/base/.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/base/.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh
 .ufo/waves/round-34/build/R34ReviewCounterC1Attacks/base/.ufo/waves/round-34/claims/control-c1.txt
```

Structure: 7 seat dirs (`a3,a4,a5,a6,a7,a8,base`) × 3 files (`assimilation/captures/tb2-eval/{SHA256SUMS,test.sh}`, `claims/control-c1.txt`).

Frozen-set stability (`for r in 11d64530 e7f0decd b662a5d6 master`): counts are `102164, 21, 21, 21`; the 21 at `e7f0decd` are byte-for-byte the same *path list* as at `master` (`diff` of the two filtered listings → empty, `IDENTICAL`). So the C1 row's "21 → 0" target is measured on exactly these 21 paths.

Distinct digests inside the set (all 21 verified against `.ufo/waves/round-36/integrate/nested-paths-removed.sha256`: `ok=21 bad=0`; loop read each line, `git show master:$p | sha256sum` vs the recorded digest):

| file | digests |
|---|---|
| `…/tb2-eval/test.sh` | `e91090b09ca7c508…` ×7 (a *mutated* test.sh; the genuine capture `corpus/evidence/round35/tb2-eval/test.sh` is `9ede46648fc67c9c…`) |
| `…/tb2-eval/SHA256SUMS` | `a01e1093a0b8ba9a…` ×6 (a3,a4,a5,a6,a7,base), `1fac92ffc6211075…` (a8) |
| `…/claims/control-c1.txt` | `e3fe6d236ac4701a…` ×6, `32f1ae09a097521b…` (a7) |

## 2. Citation census — enumerated lane docs

Enumerated set: `LOG.md`, `SCORECARD.md`, `README.md`, `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/lessons/*.md`, `corpus/defects*.jsonl`, `plans/*.py`, `plans/*.md`.
Patterns searched: the 21 path strings, `R34ReviewCounterC1Attacks`, and the affected parent dirs (`…/assimilation/captures/tb2-eval`, `…/claims`, `.ufo/waves/round-34/build`).

```
grep -rIc 'R34ReviewCounterC1Attacks' . --exclude-dir=.git
grep -rIc 'round-34' <enumerated files>
```

| file:line | quoted citation | breaks a tip evidence pointer? |
|---|---|---|
| `corpus/lessons/round-35-verifier-spotcheck.md:88` | "At `e7f0decd` I count 21 committed paths matching `^\.ufo/waves/round-3[0-9]/…` (all under `.ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a3..a6/`; the report cites 28 by a different method)." | **No.** It names rev `e7f0decd` and the regex, not a file:line into the deleted bytes; the sentence is a historical measurement and it *asks* for the deletion ("Extend the D2 check to nested `.ufo/waves/` recursion"). |

Nothing else in the enumerated set names the seat dir or any of the 21 paths. Near-misses that do **not** hit:
`SCORECARD.md:1176` and `LOG.md:978,1007` say `.ufo/waves/round-34/build/` generically (the corrected sources are `R34C2CounterDraft.md`, `R34MutC2Harness.md`, `mut-entries-scratch`, `R34MutRegistry`, none of which is among the 21); `corpus/defects.jsonl:1-5` and `plans/defect_ledger.py:30,50` reference `r34_d2`'s three literal roots, also disjoint.

**Enumerated-scope hits: 1.**

## 3. Citation census — lane evidence files outside that set

```
grep -rIc 'R34ReviewCounterC1Attacks' . --exclude-dir=.git   # per-file counts
```

14 citation lines across 9 files (the 21-line removal manifest excluded):

| file:line | citation | pointer status after deleting the 21 |
|---|---|---|
| `.ufo/waves/round-34/build/R34ReviewCounterC1.md:15` | "Attack trees under `build/R34ReviewCounterC1Attacks/` … digests recomputed: test.sh = e91090b0…, README = d1342e15…" | **Degrades.** `e91090b0` is the digest of the deleted `test.sh` (×7). The table's attack trees can no longer be re-read at the tip; only history (`git show e7f0decd:<path>`) and the removal manifest preserve the digests. `d1342e15` is *not* among the 21 (it is `…/<seat>/corpus/README.md`, which survives). |
| `.ufo/waves/round-34/build/R34ReviewCounterC1.md:70` | `d1342e15…  ../../../../../../corpus/README.md` → `defects=0` with zero evaluator bytes | **No.** Hits a surviving sibling, not the 21. |
| `.ufo/waves/round-35/falsify/F35DanglingRefs.md:109,417,445` | "Under round-34 they sit in `.ufo/waves/round-34/build/R34ReviewCounterC1Attacks/{base,a3..a8}/` (28 paths)" | **No (historical).** Directory-level count at the then-tip; deletion changes present-tense truth from 42→21 under that dir, so the sentence becomes stale but no pointer dangles. |
| `.ufo/waves/round-35/falsify/F35MutLedgerD2.md:53,59,69` | same 28-path class list, "present at parent `11d6453…`" | **No (historical).** Anchored to a rev for the "predates the deletion" claim. |
| `.ufo/waves/round-35/falsify-results.json:52,118` | residual-mirror JSON evidence, counts 28 / 43 | **No (historical).** Anchored to the rev it measured. |
| `.ufo/waves/round-36/build-dispatch.json:518`, `build-spec.json:114`, `make_build_spec.py:114` | this seat's own assignment text | **No.** Dispatch prose. |
| `.ufo/waves/round-36/build/R36RowsDraft/validate/corpus/lessons/round-35-verifier-spotcheck.md:1` | fixture mirror of spot-check:88 | **No.** It is a validation copy, not a lane doc. |

Recommendation for the L1 (integration, not mine to write): commit `nested-paths-removed.sha256` and point `R34ReviewCounterC1.md`'s erratum at it, e.g. an appended line "Erratum (round 36): the attack trees were deleted at the tip; digests are pinned in `.ufo/waves/round-36/integrate/nested-paths-removed.sha256`, bytes remain at `git show e7f0decd:<path>`." Without that, exactly one evidence pointer (R34:15) loses tip-recomputability.

**Verdict input:** deleting the 21 does not break an evidence pointer in the enumerated lane-doc set (1 hit, historical, satisfiable), and all 21 digests are preserved in a verified manifest. Pointer-safe = yes, **conditional on that manifest being committed** (see risk R1).

## 4. Calibration gaps found (for the gate/mutation seats; do not fix silently)

**G1 — "21 → 0" massively understates the surviving class.** The seat dirs hold **42** committed files, not 21:

```
git ls-tree -r --name-only master -- .ufo/waves/round-34/build/R34ReviewCounterC1Attacks | wc -l   # 42
… | grep -vE '^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-'                                     # 21 lines
```

The other 21 are 7 seats × {`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/terminal-bench-task-grader.md`}. They are **mutated** copies, not verbatim ones (`base corpus/SOURCES.md` sha `3de7c15f…` vs lane `33549258…`; `a3 corpus/SOURCES.md` `3162e1f0…`; `corpus/README.md` `d1342e15…` vs lane `edc42e62…`). Consequence: after the 21-path deletion, `plans/round36_c1_verify.py:292-295` (`NESTED_RE`, line 42) prints `committed_nested_wave_paths=0` and R35-D3 closes **while seven forged `corpus/SOURCES.md`, seven forged `corpus/README.md` and seven forged knowledge entries remain committed inside a seat tree**. Round 35's own pre-pass already classified `/corpus/SOURCES.md$` under a seat dir as same-class (`F35DanglingRefs.md:101-110`), so 7 of the 21 survivors are in the class the routed defect names. A wave-2 mutant ("gate says closed, 21 mirrors remain") would be detected by nothing in the frozen predicate. R35-D3's frozen wording claims only the 21 paths, so this is a **limit to disclose**, not a predicate violation — but a `## Gate` row that says "nested wave paths: 21 → 0" without naming the 21 survivors overstates closure.

**G2 — the routed defect's own count is misattributed.** `corpus/lessons/round-35-verifier-spotcheck.md:88` says the 21 are "all under `…R34ReviewCounterC1Attacks/a3..a6/`". Measured at `e7f0decd`: `a3 3, a4 3, a5 3, a6 3, a7 3, a8 3, base 3` — seven seat dirs, `a3..a8` + `base`. Any quote of that line should carry the correction.

**G3 — the manifest does not cover the siblings and is untracked.** `nested-paths-removed.sha256` has 21 lines, `grep -c '/corpus/'` = 0 (no sibling coverage). `git ls-files --error-unmatch` → "did not match any file(s) known to git"; `git status --porcelain -- .ufo/waves/round-36/integrate` → `?? .ufo/waves/round-36/integrate/`. Lane-wide untracked count at measurement time: **907** (`git ls-files --others --exclude-standard | wc -l`), i.e. wave-1 seats are mid-write. See risk R1.

## 5. `jj-lane.sh commit … -- <deleted tracked path>` semantics

Source read (read-only, not executed): `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh`, `cmd_commit` lines 598-730, guards 519-598.

**Does it stage deletions of tracked files? Yes, by design.** In the path loop (`cmd_commit`, the `for p in "$@"` loop):

- `[ -d ]` → directory request;
- `[ -e ] || [ -L ]` → existing file request (large-file cap 10 MiB unless `--allow-large`);
- **`elif git cat-file -e "refs/heads/$branch:$q"` → "Deleted or renamed-away path present in the branch tip: include it so the commit records the deletion."** It appends to `req`/`fs_req` as `root-file:"<path>"`, and the later `jj commit -m … -- root-file:"<path>"` records the removal in `@-` and then advances the bookmark after the guard chain passes.
- else → `warn: skipping missing path`.

**Deletion guard requirements** (a deletion must satisfy all of these or the bookmark does not move):

1. **File must be gone from disk before commit.** `validate_change_scope` (line ~556): `if [ "$status" = D ] && { [ -e "$cpath" ] || [ -L "$cpath" ]; }` → `err "commit would delete $cpath but it exists on disk (nested repo?) — refusing"`, `rc=1`. So `rm` the 21 first; a path named while still present is an `M`, not a `D`, and the deletion is simply not recorded.
2. **Pathspec containment.** Every NUL-delimited `git diff-tree --name-status -r -z --no-renames` entry must match a requested path exactly or as a prefix child: `case $cpath in "$rp"|"$rp"/*) matched=1`. Naming one seat dir (e.g. `…/a3`) admits everything under it; naming the 21 files admits exactly those.
3. **Path allowlist.** `repo_path_allowed`: rejects empty/`..`/absolute escapes, `.git`, `.git/*`, `.jj`, `.jj/*`, and **`.ufo`, `.ufo/state`, `.ufo/state/*`, `.ufo/watchdog.log`**. `.ufo/waves/**` is **allowed** — the 21 are committable and deletable by this helper.
4. **Tree shape only.** Status must be one of `A|M|D|T`; a rename is seen as `D`+`A` (`--no-renames`); a failed `git diff-tree` is an error, never an empty change set; a candidate with zero changed paths is rejected.
5. **Candidate integrity before the bookmark moves.** `candidate_is_child_of` (single parent == current tip), `candidate_is_conflict_free` (empty `conflicts()`), `candidate_has_identity` (`<id>-shokunin` author *and* committer), and the working copy must already sit on the tip (`base != tip` with a non-empty change set → "refusing to sweep or strand work").
6. `jj commit` runs under `--config 'snapshot.auto-track="none()"'`, so no untracked wave-34/36 scratch gets swept in. `jj file track` is only invoked for *existing* named files/dirs, never for the deleted ones.

Practical note for the L1: the deletion commit's diff will also include any other changed path the request covers. A directory request such as `…/R34ReviewCounterC1Attacks` after `rm` of the 21 would also record nothing else today (the 21 surviving corpus mirrors are unchanged bytes), but naming the seven seat dirs explicitly is the tighter pathspec. **Not executed** — this section is a static reading of the helper; no `commit`/`recover` was run, per the seat brief.

## 6. The 912 round-28 nested paths

```
git ls-tree -r --name-only master | grep -E '^\.ufo/waves/round-28/scratch/.*/\.ufo/waves/' | wc -l   # 912
```

- **Two** parent roots, 456 each: `.ufo/waves/round-28/scratch/FSeparability/s038-only-control/` and `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS049/baseline-export/`.
- Inner targets: `round-25` 370, `round-26` 288, `round-27` 254 (sum 912). They are 456-file slices of two full repo mirrors committed under `scratch/`.
- `NESTED_RE` (`round-3[0-9]` on both sides) does **not** match them: the verified freeze statement ("912 … match `/.ufo/waves/` but not the spot-check's `round-3x` pattern") holds.

**Who cites them** (all-file search, `.git`/`.jj` excluded):

| file | lines | what |
|---|---|---|
| `corpus/evidence/round30/quote-mode-six-rows.txt` | 6, 13, 19 | the census artifact lists; **all 912 paths appear verbatim, three times** (extraction: `grep -o '[^,]*\.ufo/waves/round-28/scratch/[^,]*\.ufo/waves/[^,]*' … \| sort -u \| wc -l` = 912) |
| `.ufo/waves/round-36/build/R36RowsDraft/validate/corpus/evidence/round30/quote-mode-six-rows.txt` | 6, 13, 19 | validation fixture mirror of the same file |
| `plans/round-36-claims.md:56-58` | 56-58 | the freeze's own limit clause (pattern-level, no path) |
| `.ufo/waves/round-28/falsify/FSeparability.md:66` | 66 | mentions the *dir* `scratch/FSeparability/s038-only-control`, not a nested `.ufo/waves/` path |
| `.ufo/waves/round-28/large-evidence-paths.json:71,75` | 71, 75 | large files *inside* the mirrors (`…/corpus/evidence/round12-ladder/results-r12.jsonl`), not the 912 |
| `.ufo/waves/round-29/falsify/FPreserveR28.md:153` | 153 | "The baseline-export …" prose, no path |

So they are **not** deletable under the same rule as the 21: a committed corpus receipt (`corpus/evidence/round30/quote-mode-six-rows.txt`) lists every one of the 912 as an existing artifact, and 14 of them are a mirror of round-25/26/27 wave evidence. Freeze says they are not touched; that is the correct call. Minor correction for the freeze's wording: the verbatim citer is a **round-30** evidence receipt, not "round-28 evidence pointers".

## 7. Risks / blockers for the L1

- **R1 (blocking for the frozen predicate).** `--require-clean-tree` requires `git -C ROOT ls-files --others --exclude-standard` to be empty. At measurement the lane had 907 untracked files and `.ufo/waves/round-36/integrate/` (holding the 21-line deletion manifest) is untracked. The manifest must be committed in the same landing as the deletion, otherwise the deletion's own evidence is deleted with the untracked tree — or the gate fails for a reason unrelated to the claim.
- **R2.** R35-D3's check will read `0` while 21 same-class forged corpus mirrors survive under the seat dirs (G1). Disclose as a limit in the round-36 lesson/`## Gate`; do not widen the frozen predicate after scoring.
- **R3.** `corpus/lessons/round-35-verifier-spotcheck.md:88`'s seat range (`a3..a6`) is wrong; if the round-36 lesson quotes it, correct to `a3..a8 + base` (G2).
- **R4.** R34's attack-tree table (`R34ReviewCounterC1.md:15`) loses tip-recomputable digests. One appended erratum line pointing at the committed manifest closes it.

## 8. Commands used (all read-only; no lane writes outside this seat's build dir)

```
git ls-tree -r --name-only master | grep -E '^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-'      # 21
git ls-tree -r --name-only master | grep -E '^\.ufo/waves/round-28/scratch/.*/\.ufo/waves/' | wc -l # 912
git ls-tree -r --name-only master -- .ufo/waves/round-34/build/R34ReviewCounterC1Attacks | wc -l     # 42
for r in 11d64530 e7f0decd b662a5d6 master; do git ls-tree -r --name-only $r | grep -cE '…'; done     # 102164 21 21 21
grep -rIc 'R34ReviewCounterC1Attacks' . --exclude-dir=.git                                          # 9 files
grep -rIc 'round-28/scratch' . --exclude-dir=.git                                                   # 140 files
while read -r h p; do git show master:$p | sha256sum; done < .ufo/waves/round-36/integrate/nested-paths-removed.sha256  # ok=21 bad=0
```

Writes: `.ufo/waves/round-36/build/R36NestedPaths.md` (this report) and `.ufo/waves/round-36/build/R36NestedPaths/nested-21.txt`. No lane index, corpus, plans or jj state touched.

VERDICT: nested-21-pointer-safe-yes-hits-1
