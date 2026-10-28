# R49C1ExecFenceB — C1 fence repair, variant B (kind classification)

Seat: executor `R49C1ExecFenceB` (leaf; no dispatch). Round 49 (hyaku run 10), wave 1, one v2 wave.
Item: fence repair variant B — a different mechanism from variant A (store-shape proof extended with ref-kind /
config-key-kind / object-info-kind classification instead of allowlist widening), measured on the three frozen
behavioural legs with per-leg dev-harness receipts on a scratch clone.
Claim served: **R49-C1 (calibration)**. This seat does **not** claim admission for R49-C1 or R49-C2; the L1 is the
single integration owner and the only seat that may land a stage-2 freeze.

Axes named: **calibration** (primary — the fence's honest over-refusal versus hostile containment, measured as a
count of contradicting fixtures); **mutation sensitivity** (the round-48 routed defect 4: a committed mutant
battery with receipts); **evidence hygiene** (routed defect 1: this report file exists at the seat-named path).

Variant A was not read: neither `.ufo/waves/round-48/w1/R48C1ExecFenceA.md` nor any `R49C1ExecFenceA` artifact was
opened by this seat. The fence below was written from the base fence (`plans/fixture_fence.py` @ `3a548330`), the
frozen refusal/sealed populations, and the 16 round-48 novel honest classes.

## 0. Stage-1 freeze verified before any measured run

| check | command | observed |
|---|---|---|
| freeze commit exists | `git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` | `commit` |
| freeze is the declared stage-1 commit | `git log -1 --format='%H %cI %s' 9d2900af…` | `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 … and C2 …` |
| claimed baseline is an ancestor of the freeze | `git merge-base --is-ancestor 3a548330c4899c6c5df34168a44a59f66828ce74 9d2900af…` | exit 0 (`base-ancestor-of-freeze=yes`) |
| measurement tree | `git -C lane rev-parse HEAD` (clone of the lane) | `9d2900af41e4d1fc6022eff99010436fde6dbd93`, `git status --porcelain` empty |
| measurement after the freeze | wall clock | first measured run 2026-10-28T09:20-03:00 (freeze 09:14:40-03:00; lane tip `af88aab` = `2026-10-28T09:18:20-03:00`) |

The clone was checked out at the **frozen base** `9d2900af` (the lane HEAD `af88aab` only adds the w1 spec /
dispatch evidence; no `plans/` byte differs). No production file was written: every candidate and receipt lives in
scratch `/fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceB/` and was copied into
`.ufo/waves/round-49/w1/R49C1ExecFenceB/` (deliverable + receipts) before scratch removal.

Host: `git 2.56.0`, `bubblewrap 0.13.1`, `strace 7.2`, `Python 3.14.8`, `/proc` thread count 189 (the C2
`RLIMIT_NPROC` failure mode does not apply here). No tool installed or upgraded; no pacman transaction attempted.

## 1. Deliverable

`.ufo/waves/round-49/w1/R49C1ExecFenceB/fence_b.py` — sha256
`c89bc524ea5d751fd7ca6f22fe13b732c0231b7b789d43ea5b507e430571f116`, 820 lines, same frozen contract
`breach(d, argv, tool) -> str | None`, no imports outside the standard library, no git child.

Mechanism (variant B), stated as the difference from the base allowlist fence:

1. **argv** — exact tool option shape; every value lexically inside `d`; NUL, newline and `{…}` placeholders
   refused (unchanged in effect, same code shape).
2. **tree** — one lstat walk: no symlink, no special file, no multiply-linked file anywhere; `.git` must be a
   directory (a `.git` file is a gitdir redirect and is refused).
3. **store top level** — each entry is assigned a **kind** (`head`, `sha`, `message`, `config`, `index`, `text`,
   `packed`, and the dir kinds `hooks`/`info`/`logs`/`objects`/`refs`); a name with no kind is refused. Kinds,
   not an entry-name allowlist, drive the validators.
4. **refs by ref kind** — a ref path is admitted iff every component is a valid git refname component and the
   content is 40-hex (object ref) or `ref: <valid refs/…>` (symbolic ref). `refs/heads`, `refs/tags`,
   `refs/remotes`, `refs/notes` and `refs/stash` are one kind (a namespace is not a security boundary; the content
   cannot name a path), and `refs/<name>` files directly under `refs/` are classified like the nested ones. A name
   with `..`, an absolute path, or a `.lock` suffix is not a refname at all.
5. **HEAD by kind** — symbolic (`ref: refs/…`) or detached (one 40-hex id); anything else refused. The base fence
   required the symbolic form and therefore over-refused detached HEAD.
6. **config by section/key kind** — redirect sections (`include`, `includeIf`, `url`) are refused as a kind;
   `[extensions]` is pinned to `objectFormat=sha1`, `refStorage=files`, `worktreeConfig`/`preciousObjects` false;
   `core` shape keys are pinned (`repositoryFormatVersion=0`, `bare=false`); every PATH-kind key (the explicit
   `core.*` path keys plus any key ending `file|path|dir|directory|location`) must name a relative path that stays
   inside `d` and is not a symlink; every COMMAND-kind key (exec-valued names, `!`-valued values) is refused; every
   other key is an **inert scalar admitted by shape** — printable ASCII, no backslash escape, no control byte, no
   non-ASCII, no NUL/CR — never by a per-key allowlist. This is why `[user]` and `[remote "origin"]` are admitted
   while `[url …]`/`include*` and `core.attributesFile`/`core.excludesFile`/`core.worktree` are not.
7. **objects/info by kind** — `alternates` refused (object-store redirect); `commit-graph`, `commit-graphs/` and
   the `packs` list admitted as opaque store data; any other name refused. Loose objects, `objects/pack` files
   (plus `multi-pack-index`) and `packed-refs` are validated by name/shape at their own kind.
8. **logs by refname kind** — `HEAD` or any valid `refs/…` reflog path; **info/** admits `exclude` and git's
   `refs` list (validated as `<40-hex>\t<refname>` lines); **hooks/** admits `*.sample` only; hardlinks and
   symlinks refused at every level.
9. **`--lane`** must be one of the collected repositories; no git child is started, so the decision reads only
   inside `d` (measured: `touches=0` on all 136 fixtures in every run below).

Two of the repairs are forced by this host's git (2.56.0), not by the fixture author: `git gc` writes
`.git/info/refs` and `.git/objects/info/packs`, and `git commit-graph write`/`gc` write
`.git/objects/info/commit-graph`. The base fence refuses all three by "info must be empty", which is why honest
class `n07_reflog_gc` is refused twice over.

## 2. Dev harness

`.ufo/waves/round-49/w1/R49C1ExecFenceB/dev_harness.py` imports the round-46 counter unchanged from the frozen
clone (`plans/round46_c1_verify.py`: bwrap sandbox, round-44 builder, strace analyser, verdict table, HARNESS
fd-closing rule, host-side log, exit-status verdict channel) and extends its legs for this round:

- HONEST = the 104 battery fixtures (`plans/battery42|43|44`) **plus** the 16 round-48 novel honest classes
  (`.ufo/waves/round-48/w1/R48C1ExecHonest/modules/{r46novel,novel48}`) = the frozen 120-fixture population;
- REFUSALS = `plans/refusals46/*.py` (20 modules), SEALED = `plans/sealed46/*.py` (12 modules), unchanged;
- a per-leg receipt and a BENIGN-ADMIT line (admissions with `touches=0`, counted separately, never as a leak);
- a MUTANTS leg: each mutant file named in `mutants/index.json` is applied to a copy of the fence, re-measured on
  its named target fixtures, and counted **caught** iff the clean signature changes (a new LEAK/READ/refusal or an
  HONEST refusal);
- `PINS` = digests of the imported counter, the imported builder and the fence under test, recomputed after the
  run.

Exact commands (run from the seat scratch, `TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceB/tmp`):

```
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93
python3 cand/dev_harness.py --lane lane --fence lane/plans/fixture_fence.py --seed before-49c1 \
        --label base-fence-9d2900a --out receipts/before_base_fence.txt
python3 cand/dev_harness.py --lane lane --fence cand/fence_b.py --seed final-49c1-b \
        --label fence-b-final --mutant-index cand/mutants/index.json --mutant-out receipts/mutants.json \
        --out receipts/final_fence_b.txt
python3 cand/dev_harness.py --lane lane --fence cand/fence_b.py --seed repeat-49c1-b \
        --label fence-b-repeat --out receipts/repeat_fence_b.txt
python3 cand/make_mutants.py                     # writes mutants/*.py + mutants/index.json
```

## 3. Observed outputs (verbatim)

### 3.1 Before — base fence (`plans/fixture_fence.py` @ `3a548330`, sha256 `05d5fe03…`), `receipts/before_base_fence.txt`

```
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 benign_admit=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 benign_admit=0 build_errors=0
HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0 modules=38
PINS total=3 mismatched=0
CALIBRATION advertised=32 contradicted=0
PREDICATE R49-C1 fail
```

The 8 honest refusals reproduce the round-48 measurement (`HONEST fixtures=120 admitted=112 refused=8`) and name
the classes, verbatim from the same receipt:

```
BREACH repo/.git/objects/info/commit-graph present (object-store redirect)      # novel48/n15_commit_graph
BREACH repo/.git/HEAD is not a plain branch HEAD                                # r46novel/n03_detached_head
BREACH repo/.git/config section header b'[remote "origin"]' is not plain        # novel48/n13_remote_origin
BREACH refs/notes has a name git does not write                                 # novel48/n16_notes_ref
BREACH repo/.git/info/refs is not git's exclude file                            # r46novel/n07_reflog_gc
BREACH refs/stash has a name git does not write                                 # novel48/n14_stash_entry
BREACH repo/.git/HEAD is not a plain branch HEAD                                # r46novel/n08_tag_detached
BREACH repo/.git/config section [user] is not allowlisted                       # novel48/n12_local_config_user
```

The before value is a **failing** predicate, so the predicate this receipt prints is not vacuous.

### 3.2 After — variant B, `receipts/final_fence_b.txt` (seed `final-49c1-b`, mutants in-line)

```
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 benign_admit=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 benign_admit=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 read=0 hung=0 build_errors=0 modules=38
PINS total=3 mismatched=0
CALIBRATION advertised=32 contradicted=0
MUTANTS total=13 caught=13 floor=6 verdict=met
PREDICATE R49-C1 pass
```

Per-leg receipts with every module row and its `touches=` count: `receipts/leg_refusals.txt` (25 lines),
`receipts/leg_sealed.txt` (17), `receipts/leg_honest.txt` (43), `receipts/leg_summary.txt` (22). Every hostile and
honest fixture line is `touches=0`, e.g.

```
REFUSALS f20_attributes_file.py clean fixtures=1 admitted=0 hung=0 touches=0
SEALED s_packed_refs.py clean fixtures=1 admitted=0 hung=0 touches=0
HONEST n14_stash_entry.py BENIGN-ADMIT fixtures=1 admitted=1 hung=0 touches=0
HONEST n07_reflog_gc.py BENIGN-ADMIT fixtures=1 admitted=1 hung=0 touches=0
```

### 3.3 Repeat — same fence, different per-run token seed (Q39 name hiding), `receipts/repeat_fence_b.txt`

```
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 benign_admit=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 benign_admit=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 read=0 hung=0 build_errors=0 modules=38
PINS total=3 mismatched=0
CALIBRATION advertised=32 contradicted=0
PREDICATE R49-C1 pass
```

### 3.4 MUTANTS — 13 mutants, `receipts/leg_summary.txt` + `receipts/mutant_rows.json`

```
MUTANT m01_objects_redirect_unguarded caught=yes sealed:clean=1/3 leaked=0
MUTANT m02_objects_hardlink_off caught=yes refusals:clean=0/1 leaked=0
MUTANT m03_config_path_kind_off caught=yes refusals:clean=0/2 leaked=0 sealed:clean=0/2 leaked=0
MUTANT m04_store_redirect_unguarded caught=yes sealed:clean=0/4 leaked=0
MUTANT m05_config_path_absolute caught=yes refusals:clean=0/1 leaked=0 sealed:clean=0/2 leaked=0
MUTANT m06_config_url_scalar caught=yes sealed:clean=0/1 leaked=0
MUTANT m07_lane_membership_off caught=yes refusals:clean=0/1 leaked=0
MUTANT m08_refs_namespace_allowlist caught=yes honest:admitted=0/2 refused=2
MUTANT m09_noncore_sections_refused caught=yes honest:admitted=0/2 refused=2
MUTANT m10_detached_head_refused caught=yes honest:admitted=0/2 refused=2
MUTANT m11_objects_info_refused caught=yes honest:admitted=0/2 refused=2
MUTANT m12_info_refs_refused caught=yes honest:admitted=0/1 refused=1
MUTANT m13_argv_shape_off caught=yes refusals:clean=0/1 leaked=0
MUTANTS total=13 caught=13 floor=6 verdict=met
```

Each mutant is one textual weakening at one kind boundary of `fence_b.py` (generator `make_mutants.py`, mutant
sources under `mutants/`, `mutants/index.json` carries per-mutant target fixtures and a one-line note). Both
directions are represented: 7 mutants admit a hostile class or break argv/lane shape, 5 mutants restore an
over-strict rule and refuse an honest class, and one drops the object-info name kind (`m01`).

## 4. Revision measured (REV line)

`REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` — the stage-1 freeze commit, clean clone, `TREE-BYTES` not
applicable (working tree clean after checkout). Every receipt above carries that line; receipts naming scratch
paths are the harness's `TREE <scratch>/lane` line, which is the seat's clone of that revision.

## 5. Limits (named, not hidden)

1. **This is a dev-harness receipt, not the v3 counter's predicate receipt.** `plans/round49_c1_verify.py` does
   not exist at the frozen base (it is wave-1/stage-2 work); its `PINS total=<P>`, `BENIGN total=<B>` and
   `MUTANTS total=<M>` literals are not frozen yet. My harness prints `PINS total=3` (counter + builder + fence
   only) and a self-authored 13-mutant battery with floor 6; the frozen `<M>`≥12 battery is authored by the
   mutation-tester seats and applied by the counter, not by this seat.
2. **Population**: HONEST is the 104 battery + 16 round-48 novel fixtures. The novel honest classes authored by
   wave-1 seats this round (folded into `<H>` at stage 2) are not in this measurement, and my rebuild was not
   diffed against `R48C1ExecHonest/population.txt`'s per-fixture `tree_sha256` list.
3. **Kind-completeness assumption**: config keys are admitted by *kind*, so a key whose name ends in no path-ish
   suffix and whose value is a plain scalar is admitted even if a future git gives it an external-read effect. The
   named kind guards are `include*`/`url`/`extensions`, the `core.*` path and command keys, and the
   `file|path|dir|directory|location` suffix rule. `objects/info` beyond `alternates|commit-graph*|packs` is
   refused by design.
4. **Opaque-by-kind content**: `.git/index`, `COMMIT_EDITMSG`, `description`, `logs/*`, pack files,
   `commit-graph*`, `multi-pack-index`, `info/refs` and `objects/info/packs` are admitted by name + size/shape, not
   content-validated (same class of limit as the base fence).
5. **Inherited counter limits** (unchanged from `plans/round46_c1_verify.py`): io_uring SQE opens emit no traced
   syscall and are not blocked; host paths outside the scratch root (`/etc`, `/proc`, `/sys`) are not counted; a
   directory stat's `st_nlink` channel is nulled by parent padding, not measured.
6. **Mount boundary** (`w2/R46W2C1C1Intent` rule): the fence's path-kind check is lexical plus a symlink lstat, so
   an honest fixture whose store sits on a mount boundary inside `d` is admitted iff the decision reads only
   inside `d`. This seat measured that through the population only; no explicit mount-boundary fixture was built.
7. A store must carry `HEAD`, `config`, `objects` and `refs`; a `.git` skeleton missing any of them is refused
   (not exercised by the frozen population).

## 6. Blockers and risks

- Blockers: none. No scored counter/probe execution was made beyond the dev harness; the freeze precondition was
  verified first, and nothing was measured that the claim does not authorise.
- Risk for stage 2: if the L1 pins a different honest population digest or a mutant battery whose mutants are
  single-guard removals over *redundant* guards, some mutants may stay uncaught while the fence is still sound (as
  my first battery showed: 10/13 when three mutants removed one of two overlapping guards). The frozen-floor rule
  (`caught ≥ M/2`) tolerates that; the counter should record per-mutant output.
- Risk: kind-based relaxations must not be re-frozen after scoring (claim kill rule); if the stage-2 counter
  disagrees with any line above, the claim stops rather than being re-measured.

## 7. Cleanup

Scratch `/fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceB/` (573 MB: shared clone, `tmp/` harness roots, probe
repo) was removed after the deliverable and receipts were copied into
`.ufo/waves/round-49/w1/R49C1ExecFenceB/`. No scratch tree remains; no lane file, no `~/.local/bin` entry, no
fleet-root file was written.

Sources opened: none from the network; no URL, access date or quote to record. The only external inputs read are
the lane's own committed files at `9d2900af` and this round's claims/lesson documents.

VERDICT: R49-C1 fence repair variant B measured **pass** on the three frozen behavioural legs at the stage-1
freeze `9d2900af` (dev harness: REFUSALS 20/20 clean, SEALED 12/12 clean, HONEST 120/120 admitted, `touches=0`
everywhere, PINS mismatched=0, MUTANTS 13/13 caught at floor 6, same result across two token seeds), versus the
base fence's **fail** (`HONEST 112/120`, 8 refusals). No admission claimed; the L1 owns the stage-2 pin and the
landed-tip predicate run.
