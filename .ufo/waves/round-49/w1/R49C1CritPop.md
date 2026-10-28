# R49C1CritPop — C1 honest-denominator identity attack

Seat `R49C1CritPop` (critic), kengaku round 49 wave 1, serving **R49-C1** (calibration). Item: test whether the
C1 honest denominator silently excludes any refused class or counts duplicated/overlapping fixtures; item-level
identity evidence. I claim no admission of R49-C1 or R49-C2.

Axis named: **calibration**.

## Freeze gate (checked before anything else)

- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` → `commit`;
  `git log -1 --format=%H%n%ci%n%an%n%s` → `9d2900af… / 2026-10-28 09:14:40 -0300 / kengaku-shokunin /
  round-49: stage-1 freeze of C1 … and C2 … claims`. The stage-1 freeze exists in the committed tree and predates
  this inspection.
- `git merge-base --is-ancestor 3a548330c4899c6c5df34168a44a59f66828ce74 9d2900af…` → `ANCESTOR_OK` (freeze sits on
  the declared base tip). `git merge-base --is-ancestor a543d920… 9d2900af…` → ok (r48 freeze is also an ancestor).
- `git cat-file -e 9d2900af…:plans/round49_c1_verify.py` → absent; `…:plans/honest49` → absent; `git ls-tree HEAD
  plans/ | grep -E 'round49|honest49|mutants49'` → none. Stage 2 does not exist at the freeze or at HEAD
  (`HEAD == 9d2900af…` in my clone). **No scored counter/probe run was made or is possible**; all findings below
  are static/item-level evidence on committed bytes. Inspected revision: `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`.

## Evidence base

The item-level identity evidence is `.ufo/waves/round-48/w1/R48C1ExecHonest/` — **tracked lane bytes at the
freeze** (`git ls-files` → 143 entries), added by r48 closure commit `d4eacdfb…` (2026-10-27T09:20:03-03:00).
`git show 9d2900af…:…/population.txt | sha256sum` → `70804edeaaf7bc297fac33a88867de59a1c1413addae3d02d32f91ea497bc7da`,
byte-equal to `population.sha256`; `identity.jsonl` sha256 `faed86c7036a6e8b0faf535729ad9a28c4ac430f24637c92ced7b9264252cd44`
matches the blob at the freeze. Frozen population inputs are unchanged since they were built:
`git diff --stat a543d920… 9d2900af… -- plans/battery42 plans/battery43 plans/battery44 plans/fixture_fence.py
plans/round46_c1_verify.py plans/refusals46 plans/sealed46 plans/fixtures` → **empty**.

## Findings

### 1. No refused class is silently excluded from the frozen 120 — measured, item-level

All eight classes the base fence measured-refused (r48 run, `REV abb08e2…`) occur **exactly once each** in the
frozen population:

```
$ for f in n03-detached-head n07-reflog-gc n08-tag-detached n12-local-config-user n13-remote-origin \
           n14-stash-entry n15-commit-graph n16-notes-ref; do grep -c " $f " population.txt; done
n03-detached-head 1   n07-reflog-gc 1   n08-tag-detached 1   n12-local-config-user 1
n13-remote-origin 1   n14-stash-entry 1 n15-commit-graph 1   n16-notes-ref 1
```

Every one of the 16 novel modules appears exactly once (`population.txt` rows: `r46novel/n01…n09`, `novel48/n10…n16`,
each `#build` ×1). The 22 battery modules' digests all equal their `plans/round46_c1_verify.py` PINS rows at the
freeze (re-verified locally: `battery pins checked 22 mismatched []`). The base-fence control therefore cannot be
vaccinated by population construction: the classes it refuses are inside `<H>`.

### 2. No duplicated fixtures in the frozen 120 — item-level identity, not just FIDs

From the committed `identity.jsonl` (120 receipts, one per fixture):

- `dup_fids []`; `dup_tree_sha256 []`.
- **Git-level identity** — grouping by `(repo dir, HEAD, refs tuple)` per receipt: `git_id_duplicate_groups 0`.
  No two fixtures share a git object-graph identity, so none is a renamed copy of another at the store level.
- `multi_repo []`; `nondeterministic []`; `audit_bad []` (no symlinks/specials/hardlinks, `gitdir_inside` all
  true); `fsck_nonzero []`; `toplevel_false []` — all 120 pass `fsck --strict` and `rev-parse --show-toplevel`.
- Split: `pop_counts {battery42:29, battery43:42, battery44:33, novel48:7, r46novel:9}` = 120;
  `tool_counts {anchor:85, order:35}`; 41 distinct normalized argv shapes — no two rows share (fid, argv, tree).
- The 16 novel module files hash to their committed `modules.sha256` rows (16/16 `OK`, re-verified at the freeze).

### 3. Semantic overlap that is real but not a duplicate (name it at stage 2)

`n08-tag-detached` is the composite of `n02-annotated-tag` + `n03-detached-head`; `n09-ignored-untracked` is
`n05-gitignore` plus an ignored file. Distinct git states (distinct `tree_sha256`, distinct HEAD/refs), and the
base fence refuses the composites for *different* reasons than the components — they are not double counting.
But `<H>` counts fixtures, not classes: stage 2 should record n08/n09 as composite classes in the manifest so a
later "classes admitted" reading can't claim 120 distinct refusal mechanisms.

### 4. Counterexample: the exclusion/dup channels live in stage-2 mechanics, not the frozen set

The frozen population is clean; the denominator can still be silently wrong at scoring time through these
channels — all verifiable in the stage-2 diff:

- **(a) Empty-output module absorption (carried from r48, still unclosed in the claim text).** In the imported
  contract, `build_module` (round46 counter lines 428–445) requires exactly one `BUILT ` line but accepts
  `BUILT []`: the loop over the decoded list emits zero rows and zero errors. A `def build(ctx, d): return []`
  module disappears from `hrows` with `build_errors=0`. Only an **authored** `<H>` catches it — if `<H>` or the
  wave-1 fold-in count is *derived from produced rows*, the drop is absorbed silently. Claims (a) says the
  wave-1 count is "folded into `<H>` at stage 2": it must be folded from the authored manifest, never re-measured.
- **(b) Non-recursive enumeration.** The contract enumerates `sorted((lane/rel).glob("*.py"))` (line 536) —
  top-level only, no pin-complaint for files outside the glob set. A wave-1 module committed at
  `plans/honest49/sub/x.py`, or left in its wave dir instead of `plans/honest49/`, is silently absent; a module
  present in *both* `plans/honest49/` and another globbed dir is counted twice. Stage-2 check: honest glob set
  = exactly `battery42|43|44` + flat `plans/honest49/*.py`.
- **(c) Wave-dir double count.** The carried 16 exist both at
  `.ufo/waves/round-48/w1/R48C1ExecHonest/modules/{r46novel,novel48}/` (committed, pinned) and, after stage 2, at
  `plans/honest49/`. The counter must enumerate the committed location only; globbing both inflates `<H>` by 16
  with all fixtures duplicated.
- **(d) Rebuild provenance.** `builder-receipt.txt` guard `lane-rev-ok a543d920…` means any stage-2 rebuild runs
  `--no-assert-base` and emits a **new `population.txt` header/digest** (the header pins the builder's lane rev).
  Re-pinning a rebuilt file instead of the committed item set can absorb a silently dropped or re-authored class.
  Pin per-item `(population, module#build, fid, tree_sha256)` against the committed `identity.jsonl` rows — the
  file digest pins the header, not the items.
- **(e) FID-keyed identity would merge items.** Battery convention does not promise global FID uniqueness (r48
  limit 7); the counter keys rows by module file (`per[(g,f)]`), so a same-FID pair across modules would count
  twice while looking like one in `FENCE-RUN`-only evidence, and module rollup prints `f.name` only
  (`battery42/a_row.py` vs `battery43/a_row.py` ambiguous). Manifest key must be `(population, module#build, fid)`;
  give rollup rows fully qualified module paths.

### 5. Looked for exclusions outside the named set — none

`plans/battery37`–`battery41` (39 modules), `plans/refusals45|46`, `plans/sealed46`, `plans/fixtures/r25–r29` and
`plans/filler46` all contain `build()`-shaped or fixture material but are earlier generations or the *hostile*
legs — outside the C1 honest contract by the frozen text, not silently dropped. `plans/honest49/` is correctly
absent at stage 1 (stage 2 lands it). No honest class exists in the tree that the denominator should but doesn't
count.

## Commands run (all read-only except the scratch clone)

- `mkdir -p /fast/scratch/hyaku/kengaku-r49/R49C1CritPop`; `export TMPDIR=…`; `git clone --shared --quiet <lane>
  lane && git checkout -q 9d2900af…` → `rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r49/R49C1CritPop/lane`,
  `rev-parse HEAD` = `9d2900af…` (verified before any use; no writes into the lane).
- `find plans/battery4{2,3,4} -name '*.py' | wc -l` → `22`; `-type l` → `0`; `grep -hoE '"fid": "[^"]+"'` → 104,
  `uniq -d` → `0`; module-file sha256 `uniq -d` → `0`.
- Python over committed `identity.jsonl` → outputs quoted in §2 verbatim.
- `git ls-files .ufo/waves/round-48/w1/R48C1ExecHonest/` → 143 tracked paths; `git show 9d2900af…:…/population.txt
  | sha256sum` → `70804ede…` (matches `population.sha256`).
- `grep -c '^HONEST' population.txt` → `120`; `find receipts -name '*.json' | wc -l` → `120`.
- `sha256sum` of the 16 novel modules vs `modules.sha256` → 16 `OK`, 0 mismatches.

## Sources opened (local lane bytes; access date 2026-10-28)

| source | located quote (≤25 words) |
|---|---|
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` | "honest population frozen at stage 2 = the 104 fixtures of `plans/battery42\|43\|44` + the 16 novel honest classes" |
| `file://…/corpus/lessons/round-48-verifier-spotcheck.md` | "the candidate's ≥12-mutant kill battery was never reported" |
| `file://…/corpus/lessons/round-48.md` | "the candidate counter measured the base fence as `HONEST fixtures=120 admitted=112 refused=8`" |
| `file://…/.ufo/waves/round-48/w1/R48C1ExecHonest/population.txt` @ `9d2900af` | "HONEST <tree_sha256> <population> <module>#<build> <fid> <tool>" (header) |
| `file://…/.ufo/waves/round-48/w1/R48C1ExecHonest/identity.jsonl` @ `9d2900af` | '"deterministic": true, "fsck_rc": 0, "toplevel_ok": true' (per-fixture receipt fields) |
| `file://…/.ufo/waves/round-48/w1/R48C1ExecHonest/builder-receipt.txt` | "COUNTS battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7" |
| `file://…/.ufo/waves/round-48/w1/R48C1ExecCounter.md` | "FENCE-RUN honest honest48/n03_detached_head.py n03-detached-head BREACH clean touches=0" |
| `file://…/.ufo/waves/round-48/w1/R48C1CritPop.md` | "an empty-output module can disappear unless stage 2 independently freezes expected identities" |
| `file://…/plans/round46_c1_verify.py` @ `9d2900af` | "built = [l for l in r.stdout.splitlines() if l.startswith(\"BUILT \")]" |

## Limits

- `identity.jsonl` is committed seat evidence (built at `a543d920`, git 2.56.0, two-sample determinism); I verified
  its input bytes are unchanged at `9d2900af` and re-derived its group statistics — I did **not** re-execute the
  builder (its own limits note host-git sensitivity in digests; `.git/index` is masked by design).
- Wave-1-authored honest classes for r49 do not exist yet: channels (a)–(e) are stage-2 requirements, not measured
  defects of a landed counter. A same-FID or byte-identical wave-1 module cannot be checked until it exists.
- `expect` in battery receipts (`reject`/`accept`/`error`) is the *grader* expectation the fixtures were authored
  for; for the fence every row is an honest store regardless — informational, not a denominator defect.

## Smallest safe correction (for the stage-2 amendment)

Commit an authored manifest — one row per honest item `(population, module#build, fid, tree_sha256, argv-shape)` —
seeded from the committed `identity.jsonl` (120 rows) plus one row per wave-1 class; require: ≥1 fixture per
pinned module, unique manifest keys, unique `tree_sha256`, observed rows == manifest rows (not just count), honest
glob set exactly `battery42|43|44 + plans/honest49/*.py` (flat), and a pinned count for the wave-1 fold-in. Mark
n08/n09 as composite classes in the manifest.

VERDICT: **the committed honest denominator neither excludes a refused class nor duplicates a fixture** — all 8
measured base-refused classes present exactly once, 120/120 distinct by FID, tree digest and git-level identity —
**but the exclusion surface moves to stage 2**: empty-`BUILT` absorption, non-recursive/out-of-root globbing,
wave-dir double counting, and rebuilt-population re-pinning can each silently shrink or inflate `<H>` unless the
amendment pins an authored per-item manifest. Static attack only; no scored run was made (stage-2 files absent
at the freeze).
