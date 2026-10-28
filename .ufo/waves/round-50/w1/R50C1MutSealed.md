# R50C1MutSealed — sealed-leg mutation probe (R50-C1 novelty)

Seat: `R50C1MutSealed` (mutation-tester), serving **R50-C1** (novelty). Wave `round-50/w1`.
Axes named: **novelty** (C1 instrument's discriminatory power over its own SEALED leg). Coverage is not claimed
here; calibration (C2) is untouched by this seat.

## Revision measured

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
$ git -C …/kengaku-shokunin merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD && echo FREEZE_IS_ANCESTOR=yes
FREEZE_IS_ANCESTOR=yes
```

`REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1` (lane tip: base tip `71f5f5f` → stage-1 freeze `f7281bc` →
freeze receipts `3b02d57` → w1 spec `5c56819` → C2 corrections `822f3b7` → C1 counter repair `c3372a9`).
All measurement was against `git clone --shared` at
`/fast/scratch/hyaku/kengaku-r50/R50C1MutSealed/lane`, `git rev-parse --show-toplevel` = that clone,
`git rev-parse HEAD` = `c3372a9b…`. Fences measured (digests taken in the clone before measuring):

```
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  lane/plans/fixture_fence.py
b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52  lane/.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py
```

The base fence digest equals the frozen `05d5fe03…`, so the lane's later uncommitted rewrite of
`plans/fixture_fence.py` (reported by seat `R50C1ExecRepair` as `57adce4a…`) is **not** in the tree measured here.

## What was done

The 12 modules of `plans/sealed46/` build **15 fixtures**. Each fixture was built with the lane's own harness
(`plans/honest50/build_honest_population.py::build_once` over `plans/round44_c1_verify.py::Ctx`, the same
`Ctx.ENV` with `GIT_CONFIG_GLOBAL=/dev/null` passed per subprocess), then **mutated in the direction of an honest
repository**: the single construct that makes the fixture hostile is removed and nothing else is changed, so the
fixture keeps its shape and the mutated tree can be compared to a from-scratch honest build. Both fences were then
asked `breach(dir, argv, tool)` on the pristine and the mutated tree. Scratch-only probes; no lane file touched.

Commands (all inside `/fast/scratch/hyaku/kengaku-r50/R50C1MutSealed`, `TMPDIR` = that dir):

```
python3 probe_base.py "$PWD/lane" "$PWD/work-base"     # pristine: 15 fixtures × {base, cand}
python3 probe_mut.py  "$PWD/lane" "$PWD/work-mut"      # one honest-direction mutation per fixture
python3 probe_twin.py "$PWD/lane" "$PWD/work-twin" "$PWD/mut.jsonl"   # mutated tree == from-scratch honest twin?
python3 probe_see.py  "$PWD/lane" "$PWD/work-see"      # plain-repack control + carried-mutant matrix
python3 probe_sites.py …                               # one-site knockout sweep (line-exact)
python3 probe_knock.py …                               # union knockouts
```

## 1. Pristine sealed fixtures — both fences refuse all 15

| module | fid | BASE `05d5fe03…` | CAND `b687b1d9…` | first reason, BASE | first reason, CAND |
|---|---|---|---|---|---|
| `a_newline_anchor.py` | `newline-anchor-accept` | BREACH | BREACH | `--lane value carries a newline` | `--lane value carries a newline` |
| `a_newline_anchor.py` | `newline-anchor-reject` | BREACH | BREACH | `--lane value carries a newline` | `--lane value carries a newline` |
| `a_phantom_anchor.py` | `phantom-anchor-accept` | BREACH | BREACH | `--lane 'missing-lane' does not exist inside the fixture` | same |
| `a_phantom_anchor.py` | `phantom-anchor-reject` | BREACH | BREACH | `--lane 'missing-lane' does not exist inside the fixture` | same |
| `a_phantom_order.py` | `phantom-order-accept` | BREACH | BREACH | `--lane 'lane-file' is not a directory` | same |
| `a_phantom_order.py` | `phantom-order-reject` | BREACH | BREACH | `--lane 'lane-file' is not a directory` | same |
| `c_core_attributes_path.py` | `sealed-core-attributes-path` | BREACH | BREACH | `lane/.git/config line b'attributesFile = /fast/scratch/hyaku/ken' is not a plain key=value` | `lane/.git/config key core.attributesfile is not allowlisted` |
| `c_excludes_file.py` | `sealed-core-excludes-file` | BREACH | BREACH | `lane/.git/config line b'excludesFile = /fast/scratch/hyaku/kenga' is not a plain key=value` | `lane/.git/config key core.excludesfile is not allowlisted` |
| `c_url_rewrite.py` | `sealed-url-insteadof-path` | BREACH | BREACH | `lane/.git/config section header b'[url "file:///outside/"]' is not plain` | `lane/.git/config section [url "file:///outside/"] is not allowlisted` |
| `p_info_redirect.py` | `sealed-info-redirect` | BREACH | BREACH | `../../../work-base/p_info_redirect/f000/lane/.git/objects/info is a symlink` | same |
| `p_pack_redirect.py` | `sealed-pack-redirect` | BREACH | BREACH | **`lane/.git/info/refs is not git's exclude file`** | `../../../work-base/p_pack_redirect/f000/lane/.git/objects/pack is a symlink` |
| `p_refs_redirect.py` | `sealed-refs-redirect` | BREACH | BREACH | `lane/.git/refs is a symlink` | same |
| `s_objects_link.py` | `seal-objects-link` | BREACH | BREACH | `lane/.git/objects is a symlink` | same |
| `s_packed_refs.py` | `seal-packed-refs-link` | BREACH | BREACH | `lane/.git/packed-refs is a symlink` | same |
| `s_refs_link.py` | `seal-refs-link` | BREACH | BREACH | `lane/.git/refs is a symlink` | same |

Module count = 12 (the counter's `SEALED46_TOTAL`); fixture count = 15 because the three `a_*` modules hold two
fixtures each. **Note the `p_pack_redirect` row**: the base fence refuses it *before* reaching the symlink, on
`lane/.git/info/refs`. That is not a pointer: it is the honest artefact of the module's own
`git repack -a -d` step (see §4). The base refusal of that module is therefore double-determined.

## 2. Honest-direction mutation — BASE still refuses exactly ONE, CANDIDATE admits 15/15

Each mutation is the removal of the one hostile construct (one byte for the newline anchor, one config line/block
for the config pointers, one directory entry — the symlink — replaced by the real store object it named).

| module | mutation | fid | BASE | CAND | BASE reason after mutation |
|---|---|---|---|---|---|
| `a_newline_anchor.py` | m1: remove the one `0x0a` byte from the `--lane` value | `newline-anchor-accept` | BREACH | BREACH | `--lane 'missinglane' does not exist inside the fixture` |
| `a_newline_anchor.py` | m1 | `newline-anchor-reject` | BREACH | BREACH | `--lane 'anothermissing' does not exist inside the fixture` |
| `a_newline_anchor.py` | m2: m1 + create the named in-`d` repo | `newline-anchor-accept` | **ADMIT** | **ADMIT** | — |
| `a_newline_anchor.py` | m2 | `newline-anchor-reject` | **ADMIT** | **ADMIT** | — |
| `a_phantom_anchor.py` | m1: create the in-`d` repo the `--lane` value names | `phantom-anchor-accept` | **ADMIT** | **ADMIT** | — |
| `a_phantom_anchor.py` | m1 | `phantom-anchor-reject` | **ADMIT** | **ADMIT** | — |
| `a_phantom_order.py` | m1: replace the plain file with a real repo at the same name | `phantom-order-accept` | **ADMIT** | **ADMIT** | — |
| `a_phantom_order.py` | m1 | `phantom-order-reject` | **ADMIT** | **ADMIT** | — |
| `a_phantom_order.py` | m2: m1 + materialise `claims.md`/`receipt.txt` | both | **ADMIT** | **ADMIT** | — |
| `c_core_attributes_path.py` | m1: delete the one `attributesFile = …` line (header stays) | `sealed-core-attributes-path` | **ADMIT** | **ADMIT** | — |
| `c_core_attributes_path.py` | m2: delete the whole appended `[core]` block | same | **ADMIT** | **ADMIT** | — |
| `c_excludes_file.py` | m1: delete the one `excludesFile = …` line | `sealed-core-excludes-file` | **ADMIT** | **ADMIT** | — |
| `c_excludes_file.py` | m2: delete the whole appended `[core]` block | same | **ADMIT** | **ADMIT** | — |
| `c_url_rewrite.py` | m1: delete the `[url "file:///outside/"]`/`insteadOf` block | `sealed-url-insteadof-path` | **ADMIT** | **ADMIT** | — |
| `p_info_redirect.py` | m1: `objects/info` symlink replaced by the store dir itself | `sealed-info-redirect` | **ADMIT** | **ADMIT** | — |
| `p_pack_redirect.py` | m1: `objects/pack` symlink replaced by the pack dir itself | `sealed-pack-redirect` | **BREACH** | **ADMIT** | `lane/.git/info/refs is not git's exclude file` |
| `p_refs_redirect.py` | m1: `refs` symlink replaced by the refs dir itself | `sealed-refs-redirect` | **ADMIT** | **ADMIT** | — |
| `s_objects_link.py` | m1: `.git/objects` symlink replaced by the store dir | `seal-objects-link` | **ADMIT** | **ADMIT** | — |
| `s_packed_refs.py` | m1: `.git/packed-refs` symlink replaced by the file | `seal-packed-refs-link` | **ADMIT** | **ADMIT** | — |
| `s_refs_link.py` | m1: `.git/refs` symlink replaced by the refs dir | `seal-refs-link` | **ADMIT** | **ADMIT** | — |

Counts over the 15 fixtures: **BASE admits 14, still refuses 1; CAND admits 15, refuses 0.**
The one base survivor is `sealed-pack-redirect`, and its refusal reason is not the removed pointer.

## 3. The mutated trees are the honest state, not a look-alike (twin check)

For the 9 single-fixture repository modules a *from-scratch honest twin* was built — the module's own build with
the hostile step never executed — and its `tree_identity` (the population builder's canonical digest) compared to
the mutated tree's:

| module | mutation | mutated tree (16 hex) | honest twin (16 hex) | equal |
|---|---|---|---|---|
| `c_core_attributes_path.py` | m1 drop key only | `94f3ee715cf34222` | `dcd3ef2f45c6fcb9` | no |
| `c_core_attributes_path.py` | m2 drop block | `dcd3ef2f45c6fcb9` | `dcd3ef2f45c6fcb9` | **yes** |
| `c_excludes_file.py` | m1 drop key only | `94f3ee715cf34222` | `dcd3ef2f45c6fcb9` | no |
| `c_excludes_file.py` | m2 drop block | `dcd3ef2f45c6fcb9` | `dcd3ef2f45c6fcb9` | **yes** |
| `c_url_rewrite.py` | m1 drop block | `dcd3ef2f45c6fcb9` | `dcd3ef2f45c6fcb9` | **yes** |
| `p_info_redirect.py` | m1 move back | `dcd3ef2f45c6fcb9` | `dcd3ef2f45c6fcb9` | **yes** |
| `p_pack_redirect.py` | m1 move back | `279c85e1127b38be` | `279c85e1127b38be` | **yes** |
| `p_refs_redirect.py` | m1 move back | `dcd3ef2f45c6fcb9` | `dcd3ef2f45c6fcb9` | **yes** |
| `s_objects_link.py` | m1 move back | `dcd3ef2f45c6fcb9` | `dcd3ef2f45c6fcb9` | **yes** |
| `s_packed_refs.py` | m1 move back | `922899c934727f86` | `922899c934727f86` | **yes** |
| `s_refs_link.py` | m1 move back | `dcd3ef2f45c6fcb9` | `dcd3ef2f45c6fcb9` | **yes** |

Nine of nine pointer-removal mutations land **byte-identical to a fresh honest build** (the repeated
`dcd3ef2f…` is the same two-commit repo shape, which is what several of these modules build). The two `m1`
config variants that only delete the key line keep an empty duplicate `[core]` section and are therefore one
edit short of the twin; both fences admit them anyway. The three `a_*` modules have no store, so no twin exists:
their honest direction is the argv/path shape itself (§2 m1/m2), and `phantom-order` m1 already admits without
the `claims.md`/`receipt.txt` that m2 adds — the fence does not require those paths to exist.

## 4. Control: the base's residual refusal is an over-refusal of a plain repo

A repo built with the same `Ctx` env (`git init -b master`, two commits) and then a default `git repack -a -d`:

```
PLAIN-REPACK {"base": "BREACH", "base_why": "lane/.git/info/refs is not git's exclude file",
 "cand": "ADMIT", "cand_why": "", "git_version": "git version 2.56.0",
 "info_after_repack": ["exclude", "refs"], "info_before_repack": ["exclude"]}
```

Mechanism confirmed independently (per-command env, no global export):

```
BEFORE=exclude
DEFAULT=exclude
refs
NOSERVERINFO=exclude
CFG=unset
```

i.e. `git repack` runs `git update-server-info` by default (`repack.updateServerInfo` unset ⇒ true), writing
`.git/info/refs`; with `-c repack.updateServerInfo=false` it does not. So `.git/info/refs` after a repack is an
**ordinary git state**, and the base fence refuses it while the r49 candidate admits it. Nothing in
`plans/honest50/population.txt` repacks (`grep -c repack plans/honest50/population.txt` → `0`; no repack call in
`plans/battery4[234]` or `plans/honest50/modules`), so the 126-fixture honest leg cannot see this class at all.

The base refuses the same plain repo a **second** time, so this is not one stray rule. Widening its `.git/info`
rule to accept any regular file exposes the next refusal:

```
plain repo, base fence                                 : lane/.git/info/refs is not git's exclude file
+ base `.git/info` rule widened (name != "exclude")     : lane/.git/objects/info/packs present (object-store redirect)
+ that widening and every stat.S_ISLNK condition dead  : lane/.git/objects/info/packs present (object-store redirect)
candidate b687b1d9 on the same tree                      : None (ADMIT)
```

`objects/info/packs` is the file `git repack` writes to describe the packs present (gitrepository-layout(5)); the
base fence classifies it as an object-store redirect. Both of the base's refusals of `sealed-pack-redirect` are
therefore over-refusals of a repacked store, and both fire before the module's symlink is examined
(the `stat.S_ISLNK`-dead run lands on `objects/info/packs`, not on the pointer).

## 5. What the sealed leg can and cannot see (the bound)

### 5.1 Carried r49 mutant battery against the candidate (native target)

All 23 payloads apply cleanly to `b687b1d9…`. Sealed-leg verdict vector (15 fixtures) for each:
**22 of 23 leave it unchanged**; exactly one changes it:

| payload | sealed breach count (ref = 15/15) | fixtures that flip to ADMIT |
|---|---|---|
| `c1-mut-08-config-unknown-key` | 13/15 | `sealed-core-attributes-path`, `sealed-core-excludes-file` |
| all other 22 payloads | 15/15 | none |

(The `BASE` column of the same matrix is **not** used: the payloads are written against the candidate's text, and
`patch` fuzzes them onto the base fence — verified by `diff`, e.g. `c1-mut-03` is applied onto the base as an
*inversion* that adds two lines inside a scope where `st`/`ddev` are not the candidate's variables. Any base-fence
statement below comes from line-exact knockouts, not from those fuzzed applications.)

### 5.2 Single-site knockouts refuse to move the sealed verdict

Line-exact `if False:` knockouts of each symlink refusal site, one site at a time:

```
BASE 05d5fe03 sites 196,211,285,305,334,350,364,390,416,462  → every one: witnesses []
CAND b687b1d9 sites 244,261,391,420,451,467,483,501,537,588,617,638,699 → every one: witnesses []
```

and the union (every `stat.S_ISLNK(...)` condition in the file dead):

```
base-nosymlink-sites 13  admitted []   breach 15/15
cand-nosymlink-sites 15  admitted []   breach 15/15
```

Reason witnessed on the union-knockout variants (same trees, symlink test dead in every site):

```
base p_refs_redirect  -> lane/.git/refs is not a directory
base s_objects_link   -> lane/.git/objects is not a directory
base s_packed_refs    -> lane/.git/packed-refs is not a regular file
cand p_pack_redirect  -> lane/.git/objects/pack is not a directory
cand p_refs_redirect  -> lane/.git/refs is not a directory
cand s_objects_link   -> lane/.git/objects is not a directory
cand s_packed_refs    -> lane/.git/packed-refs is not a regular file
```

A symlink can therefore never be *admitted* by deleting a symlink check: the type discipline refuses the shape
first. The sealed fixtures cannot witness the deletion of any symlink check, singly or jointly, on either fence.

### 5.3 Bound stated as limits of the SEALED leg

1. **Each sealed fixture carries exactly one discriminating construct** (§3: mutated = fresh honest build). Its
   whole detection value is "the fence still sees the pointer". It says nothing about *how* the fence sees it.
2. **Symlink-site deletions are invisible** on both fences (13/13 base sites, 15/15 candidate sites swept; union
   knockouts too). The 6 pointer fixtures cannot witness any symlink-check mutation; only a mutant that drops the
   *type* discipline changes their verdict. Concretely, the carried `c1-mut-02-symlink-dir-dead` is a no-op on all
   15 sealed fixtures — its claimed direction ("nothing downstream re-refuses it") is false for a `.git`-internal
   symlink, whose lstat mode is not a directory, so the `not S_ISDIR` leg refuses it first.
3. **The one visible payload is a config-allowlist deletion** (`c1-mut-08`), and it is visible only through the
   two `[core]` pointer fixtures. The URL-rewrite pointer needs *two* sites dead at once (section allowlist **and**
   the `_sub_name_ok` component shape) — a single knock on either leaves the fixture refused.
4. **A second, unrelated refusal masks the pointer.** `sealed-pack-redirect` keeps `.git/info/refs` from its own
   honest `git repack -a -d` step. Under the base fence that rule fires first, so the base fence's symlink handling
   is *untested by that fixture*, and the fixture's "refused" verdict is not evidence about the pointer at all. On
   the candidate, which admits the honest repacked state, the pointer is the sole and sufficient reason.
5. **Consequence for the mutant floor.** A witnessed-kill battery that targets symlink/boundary *sites* of this
   fence family will read as `broken`/`survived` on the sealed leg no matter how correct the fence is; the sealed
   leg can only witness family-level deletions (allowlist removal, type-discipline removal). The `MUTANTS` leg's
   `caught` count is therefore not a measure of the sealed fixtures' sharpness — it is a measure of how many
   payloads happen to hit a *last* layer of a layered check.
6. **Host sensitivity.** The *first* base refusal (`.git/info/refs`) depends on `repack.updateServerInfo`
   (true by default; git 2.56.0 here, and `-c repack.updateServerInfo=false` removes it — verified). The *second*
   refusal (`objects/info/packs`) does not: that file survives the `updateServerInfo=false` repack
   (`rp/.git/objects/info` = `packs`, `rp/.git/info` = `exclude`), so the base fence refuses every repacked store
   on this host and would on any git that writes the pack list. Twin equality (§3) is stable because `Ctx` pins
   author/committer dates, so trees reproduce across runs on this host.

## Coordination received

Seat `R50C1ExecRepair` reports an uncommitted lane rewrite of `plans/fixture_fence.py` (`57adce4a…`, with a
mount/device-boundary leg, detached-HEAD acceptance, commit-graph/info-refs allowances) written after my clone was
taken. My measurements use the clone's `05d5fe03…`, digest-verified before measuring, and are therefore unaffected;
they say nothing about `57adce4a…`. Their point that the frozen hostile legs miss a `_refs` regression is consistent
with §5.3.2: the sealed fixtures do not exercise per-site `_refs` logic at all, because type discipline refuses
those shapes first.

## Limits of this report

* Verdicts are the fence's `breach()` return only. No leak/strace leg was run (that is
  `plans/round46_c1_verify.py`'s property, out of scope here), and the honest/refusal legs were not re-scored.
* `plans/honest50/population.txt` was not rebuilt; the 126-fixture population is untouched.
* One mutation per fixture (plus the two documented follow-ups for `a_newline_anchor`/`c_*`); not an exhaustive
  edit space.
* The `patch`-fuzzed base-fence mutant matrix was discarded as unusable (see §5.1); line-exact knockouts replace it.
* Scratch tree `/fast/scratch/hyaku/kengaku-r50/R50C1MutSealed` was removed before this report was finalised;
  every number above is transcribed here.

VERDICT: base admits 14/15 mutated sealed fixtures, refuses 1 (`sealed-pack-redirect`, via the honest
`.git/info/refs` rule, not the pointer); r49 candidate admits 15/15. The sealed leg's blind spots: every
single-site symlink-check deletion (13/13 base, 15/15 candidate sites), 22/23 carried payloads, and any check
masked by a second independent refusal — it can only witness family-level deletions of the config allowlist.
