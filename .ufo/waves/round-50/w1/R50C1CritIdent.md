# R50C1CritIdent — identity-pin attack on the R50-C1 honest population

**Seat** R50C1CritIdent (critic, attack role) · **lane** `kengaku-shokunin` · **claim attacked** R50-C1 (novelty),
the `POPULATION` leg only · **report written by** the seat; no production file, no commit, no lane write.

## Revision measured

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD
$ echo $?            -> 0            (freeze IS an ancestor at the time of measurement)
$ git -C .../kengaku-shokunin rev-parse HEAD    -> 822f3b748306ec6918a415bc713f9688a3de20e7   (at measurement start)
                                                  c3372a9b24d3a200946a6b37dc0a31ed5c982cc1   (lane advanced during the run)
REV_MEASURED 3b02d573d58cc6d2e0d27ef92ac0815354912252   (git clone --shared of the lane, checkout of the S1 freeze)
```

Instrument digests in the clone at S1 (`sha256sum` in the clone):

```
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py          (base fence, as frozen)
f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  plans/round50_c1_verify.py      (S1 counter)
b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  plans/honest50/population.txt   (126 rows)
```

At the lane tip `c3372a9` the counter is the open-window repair `d8787b34…`; its `POPULATION` leg is unchanged
for this attack — `git show HEAD:plans/round50_c1_verify.py | sed -n '196,200p'` still reads

```python
        mismatched = [r["fid"] for r in rows
                      if r["fid"] not in by_fid or hb.tree_identity(by_fid[r["fid"]]["dir"])[0] != r["tree"]]
```

i.e. **digest only, no count, no masked set, no structural audit**. Every finding below therefore holds for the
current instrument, not just for the S1 copy I measured.

## Control (the state I attacked)

```
$ python3 plans/round50_c1_verify.py --lane . --skip-mutants --work <scratch>/work-base   (in the S1 clone)
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE .../plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0   (13 HONEST-REFUSED lines follow)
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

Matches the measured state in the assignment exactly (113/13, 20/20, 12/12). Wall 9.4 s.

## What `tree_sha256` is

`plans/honest50/build_honest_population.py::tree_identity` emits, sorted and sha256'd:

* one line per **directory** `D <relpath> <mode>` — no content, no link target;
* one line per **file** `F <relpath> <mode> <symlink:target | sha256:content | special:st_mode>`;
* **excluded from the walk**: every directory named `__pycache__` (dropped from `dirs` before the loop);
* **skipped entirely** (the `skipped`/`masked` list, *not* hashed): `rel == ".git/index"`, any `rel` ending in
  `/.git/index`, `.git/worktrees/*/index`, and the index of any store named by a `.git` gitfile
  (`gitfile_index_paths`).

No mtime, no inode, no `st_nlink`, no uid/gid, no xattr, no directory link target. Frozen population coverage:
**125 of 126 rows carry ≥1 masked path (128 masked paths total)**; the only zero-mask row is `n10-empty-repo`
(`plans/honest50/identity.jsonl`).

## Probe matrix (measured, not derived)

Method: build each fixture with the lane's own builder (`build_once`), `shutil.copytree(..., symlinks=True)` a
fresh copy per probe, apply one mutation, then compare `hb.tree_identity(...)` and `fence.breach(...)`.
`--lane` tokens in `argv` were rewritten from the pool path to the copy path, and an **unmutated copy control**
was run first (`tree_equal=True`, verdict identical to base) so a verdict difference can only come from the
mutation. Six `battery42/a_class.py` fixtures (base `ADMIT`), identical results on all six — one table:

| probe (item) | `tree_sha256` changes? | fence verdict | counter `mismatched` |
|---|---|---|---|
| a1 extra empty dir `zz_extra_empty` | **yes** (new `D … 0755` line) | ADMIT (same) | >0 → **caught** |
| a2 extra empty dir `__pycache__` | **no** | ADMIT | 0 → **silent** |
| a3 `__pycache__/payload.bin` (5 KB payload) | **no** | ADMIT | 0 → **silent** |
| b1 `chmod 0700 .git/objects` | **yes** (`D … 0700`) | ADMIT | caught |
| b2 `chmod +x` a tracked file | **yes** | ADMIT | caught |
| b3 `chmod 0600 .git/index` | **no** (masked) | ADMIT | silent |
| c1 mtime of a file → (1,1) | **no** | ADMIT | silent (benign) |
| c2 mtime of `.git/index` → (1,1) | **no** | ADMIT | silent (benign) |
| c3 mtime of every file → (2,2) | **no** | ADMIT | silent (benign) |
| d1 `.git/index` ← 25 bytes of garbage | **no** | **ADMIT** | **silent + admitted** |
| d2 `.git/index` → symlink to a file outside `d` | **no** | **BREACH** (`repo/.git/index is a symlink`) | silent pin, fence closes |
| d3 `.git/index` grown to 16 MiB + 1 | **no** | **BREACH** (`index exceeds 16777216 bytes`) | silent pin, fence closes |
| d4 `.git/index` → directory | **yes** (`F`→`D` + `index/inner` hashed) | BREACH | caught |
| d5 `.git/index` deleted | **no** | **ADMIT** | **silent + admitted** (`masked` 1→0, not compared) |
| e1 same content, **new inode** (rewrite via `os.replace`) | **no** | ADMIT | silent (benign) |
| e2 same content, **hardlink** to a file outside `d` (nlink=2) | **no** | **BREACH** (`has more than one hard link`) | silent pin, fence closes |
| f1 empty store dir → symlink to outside dir | **yes** (mode 0755→0777) | BREACH | caught |
| g1 `setxattr user.k50` on `.git/HEAD` | **no** | **ADMIT** | **silent + admitted** |
| g2 symlink **under `__pycache__`** → outside dir | **no** | **BREACH** (`__pycache__/escape is a symlink`) | silent pin, fence closes |

`files_equal`/`dirs_equal` from the same run: a1 changes `dirs` only; **a2, a3, g2 change neither** (the excluded
subtree is not even counted); d4 changes `files` only. So a counts-based check would not have caught a2/a3/g2.

The two `novel` fixtures in the sample (`n20-linked-worktree`, `n21-separate-gitdir`) are **already refused by the
base fence** (`wt/.git is a file (gitdir redirect), not a directory`), so they carry no discriminating power for
this attack; their probes reproduce the same identity blindness (`ident_same=True` for a2/a3/b3/c*/d1/d2/d3/d5/e1/e2/g1/g2)
but no verdict flip. That is a limit of the sample, not evidence against the finding.

## The five named questions, answered

* **(a) extra empty directory — NOT invisible in general.** A new directory changes the digest through its `D`
  line. **Exception: any directory named `__pycache__`, at any depth, and its entire subtree** are dropped before
  the walk: a2/a3 were digest-identical (`files_equal=True dirs_equal=True`) and the fence **admits** them.
* **(b) mode bit — visible for every unmasked path** (`S_IMODE` is in both line kinds), invisible only on a
  **masked** path (b3).
* **(c) file mtime — fully invisible** (not an input anywhere). Benign for admission: the fence reads no mtime and
  starts no git child.
* **(d) masked `.git/index` — invisible in every dimension**: bytes (d1), size (d3), mode (b3), **presence/absence**
  (d5), and **type, file → symlink** (d2). The mask test runs *before* `os.lstat`, so a symlinked index is excluded
  from the digest, from `n_files`, and from `skipped`'s mode information alike.
* **(e) identical content, different inode — invisible**, and so is `st_nlink`: the digest is content-addressed
  (e1 clean, e2 hardlink clean). The fence's `_linked()` refuses nlink>1 today, so e2 fails closed.

## Strongest counterexample from the frozen data (two real `git` writers, no hand-forging)

1. **Index format change on a pinned fixture.** In a copy of `battery42/a_class-x6-sibling-digest` (toplevel
   asserted equal to the fixture repo before the write):
   `git -C <repo> update-index --index-version 4`, rc 0. Index `ba5a19f1dda4345fc0bf0dff3da8ffbfffd447ae95dedbc06ad318f8065747a9`
   (555 B) → `656332703e4fe3fc71881b7a6f69849458f92cb0d0a67e5d304fd44032d648c5` (510 B), magic `4449524300000004`.
   `tree_identity` **identical** (`765a2dab78cee70d133089837ad2e36d097a00c62c176ffba4465f08e5e44446`), fence **ADMIT**.
   A host git that writes index v4 instead of v2 reproduces `POPULATION … mismatched=0` while the byte population
   differs — exactly the host sensitivity the claim's named limit says the identity pins make "visible rather than
   silent".
2. **An index appearing where the pin recorded none.** `n10-empty-repo` is the one pinned row with `masked=[]`
   (tree `18993be152d5b138480617c35d06006f1e0d9e54f40d6f1cd9410fa0692ac57f`). `git -C <repo> read-tree --empty`,
   rc 0, creates a 65-byte `DIRC` v2 index. After: tree `18993be1…` **unchanged**, `files/dirs 18/10` **unchanged**,
   `masked [] → ['repo/.git/index']`, fence **ADMIT**. The counter would print `mismatched=0`. Presence of git's
   largest stat file is unpinned.

## Does that matter for an admission decision?

Three separate questions, answered on evidence:

1. **Can a hostile fixture be swapped in through the counter's interface?** **No.** `build_all` builds every module
   into `work/honest/…` and `verdicts` consumes only those dirs (`plans/round50_c1_verify.py:107-140,196-199` at
   tip). There is no `--fixture`/`--fixture-dir` input; the counter cannot be pointed at a tree it did not build.
   The identity comparison is a **rebuild-reproducibility** statement, never a provenance statement about an
   externally supplied tree. The attack surface is therefore only "can the rebuild differ in a way the pin misses"
   — which is exactly what the matrix measures.
2. **Does a blind mutation flip an admission decision?** Every blind shape that is an **indirection** — d2 (index →
   symlink), e2 (hardlink out), g2 (symlink under `__pycache__`), d3 (16 MiB index) — is **refused by the fence**,
   so `HONEST admitted < 126` and the predicate **fails closed**. No blind mutation I could build moves a verdict
   from BREACH to ADMIT.
3. **Can a blind mutation be both admitted and non-honest?** Yes: d1 (garbage index), d5 (index deleted), g1
   (xattr), a3 (`__pycache__/payload.bin`), plus mtime/inode churn — all **ADMIT** with `tree_sha256` unchanged.
   None of them is an indirection, and this fence starts **no git child** (its own docstring: "No git child is ever
   started"), so none can make a read leave `d`. They corrupt the *denominator's meaning*, not a verdict.

**Conclusion for admission:** the identity blindness does not admit a hostile fixture and does not turn a false
pass into a true one **today**. It does make two things weaker than the claim states: (i) the sentence "identity
pins make [host sensitivity] visible rather than silent" is false for the masked index (125/126 fixtures, 128
paths) and for `__pycache__` subtrees; (ii) `POPULATION … mismatched=0` is a statement about everything **except**
git's stat cache, so a host git that changes index format — or a future build that stops writing an index — is
reported as a clean match. **Forward risk:** if the S2 repair touches index handling in `_store` (today: size cap
only, no type/mode check), the population pin cannot evidence it — d2/d3 are invisible to identity and change the
fence verdict. The mutant leg would still catch a *fence* change, but not a *denominator* change.

**Fixable defect, not a tradeoff to accept:** the repair is three cheap comparisons using data already frozen at
S1, with zero predicate change.

## Smallest safe correction

`plans/honest50/identity.jsonl` (already committed at S1, one row per fid) carries `files`, `dirs`, `masked`,
`audit.hardlinks|specials|symlinks`, `audit.gitdir_inside`. The counter reads none of them. Repair:

1. `plans/round50_c1_verify.py`, `POPULATION` leg — compare the **tuple**, not `[0]`:

   ```python
   tid, nf, nd, msk = hb.tree_identity(dir)
   bad = (tid != row["tree_sha256"] or nf != row["files"] or nd != row["dirs"]
          or sorted(msk) != sorted(row["masked"])
          or any(row["audit"][k] for k in ("hardlinks", "specials", "symlinks"))
          or not all(row["audit"]["gitdir_inside"]))
   ```

   with the rows loaded from `plans/honest50/identity.jsonl` and that file's sha256 pinned as a counter literal.
   This closes **a2/a3/g2** (audit), **d2** (audit symlinks + masked entry must still exist as a regular file),
   **d5** (`masked` set differs), **d4** (counts), and **e2** (audit hardlinks) — all currently silent.
2. `plans/honest50/build_honest_population.py::tree_identity` — stop dropping `__pycache__` silently: keep it out
   of the walked content but append it to `skipped` as `excluded:<rel>` (and/or drop the exclusion entirely: no
   honest fixture contains one, so the exclusion protects nothing and only creates a blind subtree).
   `skipped` is **not** hashed, so no pinned `tree_sha256` moves and `population.txt` needs no re-freeze.
3. Optional, only if index *type* must be pinned: record masked entries as `(rel, kind, mode)` in the returned
   `skipped` list. Bytes stay exempt (they are the volatile part); presence, type and mode become visible. This
   requires updating `identity.jsonl` values (a receipt re-freeze, not a population re-freeze) — noted so the
   choice is explicit, not silent.

Residual, deliberately left open: d1 (index bytes), c* (mtimes), e1 (inode), g1 (xattrs) stay unseen. Pinning them
would pin a volatile stat cache — the reason the mask exists — and none of them can move a verdict under a fence
that starts no git child.

Admissibility note for the L1: this is a repair of a leg that reports a **false clean** (an enumerated open-window
reason), not a change to the predicate sentence, the four leg names, the literals `126`/`20`/`12`/`SEALED50_MIN`,
or the population pin. It owes the claims file an old→new digest row for both files and a re-run of the four
controls on the S2 tree (the do-nothing control must still print `HONEST fixtures=126 admitted=113 refused=13`
and `PREDICATE R50-C1 fail`).

## Axes

* **novelty (C1)** — impacted: the population pin's evidentiary sentence. Claim survives *as measured*; its
  reproducibility wording overclaims for 125/126 fixtures.
* **coverage** — untouched (no claim, operator-capped).
* **calibration (C2)** — untouched; no `SCORECARD.md`/`SHONEN.md`/`PROVINCE.md` pointer involved.

## Limits

* Measured on one host (git 2.56.0), one filesystem (ext4 on NVMe `/fast`), one clone at S1; the lane advanced to
  `c3372a9` mid-run and I verified the tip's `POPULATION` leg text rather than re-running the full tip build.
* Sample = 6 `battery42` fixtures + 2 `novel` fixtures, chosen for base `ADMIT` so a verdict flip is observable;
  the other 118 rows were inspected only through `identity.jsonl` (masked/audit/`deterministic` fields), not
  probed. `harden`/`special`/`error` classes and multi-repo fixtures beyond n20/n21 were not probed.
* Xattr result is the `user.*` namespace on ext4; SELinux/`security.*` labels were not exercised.
* `io_uring` and path observation outside the scratch root are out of scope (unchanged from the claim).
* Branch-protection/`__pycache__` behaviour under a repo whose *tracked* content legitimately includes
  `__pycache__` was not built: no such honest class exists in the population, and the fence would admit it.
* Scratch-only harness (`probe.py`, pool, copies) was under
  `/fast/scratch/hyaku/kengaku-r50/R50C1CritIdent/` and has been **removed** before yield; the outputs cited above
  are reproduced verbatim in this report because scratch paths are not citable evidence. No tool was installed or
  upgraded for this seat. No git/jj mutation was performed anywhere except inside scratch fixtures and my own
  `git clone --shared`; `git rev-parse --show-toplevel` was asserted equal to the fixture repo before every
  fixture write (`update-index`, `read-tree`).

VERDICT: identity pins are **forgeable in five shapes** — masked `.git/index` (bytes/size/mode/presence/type), any
`__pycache__` subtree, hardlink/inode identity, mtime, xattr — and a swap of that kind is invisible to
`POPULATION … mismatched=0`. It **does not corrupt an admission decision** on the base fence: no external fixture
can be injected, every blind indirection is refused by `_tree`/`_store` (fails closed), and every blind state the
fence admits is a non-indirection that cannot widen a read. It **does** falsify the claim's "visible rather than
silent" sentence for git's stat cache and weakens the population pin as a reproducibility statement; smallest safe
correction is the four comparisons against the already-frozen `plans/honest50/identity.jsonl` plus recording
`__pycache__` in `skipped` (no re-freeze, no predicate change), and it must land in S2 under the "false clean"
open-window reason with an old→new digest row.

## Addendum (written after the lane drifted under the measurement)

At 14:31, when the control and probe runs above were made, the lane working tree still held the frozen fence:
`sha256sum plans/fixture_fence.py` → `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`. At 14:4x the
same path reads `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` and `git status --porcelain`
reports ` M plans/fixture_fence.py` **and** ` M plans/round50_c1_verify.py` (counter `850ec790…`, +59/−15).
Per peer `R50C1ExecRepair` the fence change was written by another seat at 14:36 (mount/device-boundary leg,
detached-HEAD acceptance, commit-graph/`info/refs` allowances) and is one of **two non-stackable repairs** — the
other is that seat's scratch candidate `9baedf13…`. I take no position on which lands.

What this does and does not change here:

* **Identity side — unaffected.** No fence repair touches `plans/honest50/build_honest_population.py::tree_identity`
  or the counter's `POPULATION` comparison. The in-flight counter still reads
  `hb.tree_identity(by_fid[r["fid"]]["dir"])[0] != r["tree"]` (`plans/round50_c1_verify.py:242-243` in the working
  tree), so the digest-only finding and the proposed correction apply to it verbatim.
* **Fence-side outcomes — text-inspected, not re-measured.** On `57adce4a` at 14:4x: `.git/index` is still in
  `GIT_TOP` (line 105) with **size-only** handling (`elif name == "index": if size > INDEX_CAP`, lines 824-826 and
  893-895 for the worktree store), `_tree` still refuses symlinks, special files and `nlink>1` (lines 248-281), and
  the store entry loops still refuse symlinks and `_linked` entries. So d2/d3/e2/g2 are expected to stay
  fence-refused and the "fails closed" half of the verdict to survive — **expected, not executed**.
* **The new fence admits `n20`/`n21`** (`worktrees`, `commondir`, `gitdir` added to `GIT_TOP`), i.e. exactly the
  rows whose masked sets are largest (`repo/.git/worktrees/wt/index` plus the gitfile store index). My d-probes on
  those fixtures had no verdict-flip power against the base fence because it refused them outright; under the
  repaired fence they would verdict ADMIT, and the masked-index blindness becomes load-bearing for newly admitted
  rows. Recommendation: land correction §1 before the S2 score, and have the S2 receipt name the fence digest it
  scored.

Everything above this addendum was measured at `3b02d573…` against `05d5fe03…` only.
