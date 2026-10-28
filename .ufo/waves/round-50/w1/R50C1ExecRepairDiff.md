# R50C1ExecRepairDiff — repair differential: candidate A vs candidate B vs the base fence

Seat: `R50C1ExecRepairDiff` (executor, leaf). Serves **R50-C1** (novelty, 7 → 8). Scope: exactly the assigned
item — a line-level risk table of what each of the two wave-1 repair candidates OPENS and keeps CLOSED, plus
every case where one candidate admits what the other refuses, with a git-doc or fixture reason for which is
correct. Nothing here judges R50-C1 or R50-C2 admission and nothing here edits production.

## Revision measured (REV receipts)

```
lane checkout measured       3b02d573d58cc6d2e0d27ef92ac0815354912252   (stage-1 freeze)
freeze is ancestor of tip    git merge-base --is-ancestor 3b02d573… d52243af…  -> 0 (FREEZE_IS_ANCESTOR)
live lane tip seen            d52243afab26962c4ba2f469bf7917a491ce3870   (measured only for ancestry + sealed50 source)
plans/fixture_fence.py @ freeze  sha256 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  (575 lines)  = base
plans/honest50/population.txt    sha256 b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  (126 rows)
candidate A  C1ExecRepair/fence_candidate.py    sha256 2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc  (862 lines)
candidate B  C1ExecRepairB/fence_candidate_b.py sha256 4e68592ca640a4f384b767db179ad79b8c5e9863086311ac87968810412ef393 (1059 lines)
blind held-out set  plans/sealed50 @ d52243af   20 modules, manifest digest sha256(sorted sha256sum listing) 26dc9f248f73f9f9cc716b81907db78eeba5832282813f9920005c5887c34c6c
```

The live lane's `plans/fixture_fence.py` is `57adce4a…` (the landed S2 repair). It is **not** part of this
comparison and was not evaluated; the base fence here is `05d5fe03…` from the freeze commit, exactly as the
claims file pins it.

## Axes named (Godspeed)

1. **Honest admission** — how many of the 126 pinned honest fixtures the candidate admits (the C1 HONEST leg).
2. **Hostile closure** — leaked modules across the 20 frozen refusals, 12 frozen sealed and 20 blind sealed.
3. **Differential safety** — for every shape A admits and B refuses (and vice versa), does the admitted shape
   still keep every read inside `d`?
4. **Contract fidelity** — does the rule that decides a shape follow *git's writer* ("states git itself writes",
   claims §Named limits) or git's reader's leniency?
5. **Repair surface** — added/removed lines and hunks per candidate (maintenance risk at S2).
6. **Delta efficiency** — honest classes opened per 100 added lines (A ≈ 1.3, B ≈ 2.5 — see §3).

## 1. Method and exact commands

Read-only against a `--shared` clone of the lane at the freeze commit; the two candidates were copied into
scratch (`PYTHONDONTWRITEBYTECODE=1`) so no byte was written into a sibling seat's wave directory. The frozen
counter was driven unchanged through its own `--fence` switch (it records the fence digest in the receipt).

```
S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecRepairDiff
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane && git -C $S/lane checkout -q 3b02d573…
sha256sum $S/lane/plans/fixture_fence.py            # 05d5fe03… (asserted before any measurement)

# leg A/B with the frozen 32 hostile modules
cd $S/lane && env TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work-a --fence $S/cand/fence_a.py --skip-mutants
cd $S/lane && env TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work-b --fence $S/cand/fence_b.py --skip-mutants
cd $S/lane && env TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work $S/work-base --skip-mutants --allow-dirty

# same three, with the 20 blind sealed50 modules copied into the scratch clone (52 hostile modules total)
cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sealed50/*.py $S/lane/plans/sealed50/ && git -C $S/lane status --porcelain   # dirty=1

# 41-case differential probe battery (each case builds one fixture, records what git does with it, then asks base/A/B)
env PROBE_ROOT=$S TMPDIR=$S python3 $S/probe.py > $S/probe-out.txt
```

Every probe fixture is built with `git -C <dir>` and verifies `git -C <dir> rev-parse --show-toplevel` equals
the fixture dir before any write; the git env (`HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_CONFIG_NOSYSTEM=1`, author/committer dates) is passed **per command**, never exported into the shared shell.

Environment note (not a lane defect, recorded because it corrupts any harness that misses it): this host's
`~/.config/git/config` sets `rerere.enabled=true`, so a fixture built without isolating `XDG_CONFIG_HOME`
gets `.git/rr-cache/` and `.git/MERGE_RR`, which no fence allowlists. My first probe run showed exactly that
(`.git/MERGE_RR is not a plain-init entry`) before isolation. The lane's own population is unaffected: the
pinned identity leg printed `mismatched=0` on all three fences.

## 2. Counter outcomes (verbatim)

Base fence, frozen 32 hostile modules (`--allow-dirty` because the scratch clone carried the blind set):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE …/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry …repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph present (object-store redirect)
HONEST-REFUSED n16-notes-ref …repo/.git/logs/refs/notes has a name git does not write
HONEST-REFUSED n17-replace-ref repo/.git/refs/replace is not refs/heads or refs/tags
HONEST-REFUSED n18-shallow-fetch repo/.git/FETCH_HEAD is not a plain-init entry
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d lane/.git/objects/info/alternates present (object-store redirect)
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=20 clean=20 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

(base's 13th refusal, not printed by the counter's 12-line cap, is `n08-tag-detached`; it appears in candidate
A's receipt below and in `C1ExecRepair/fence_candidate.py`'s own report.)

Candidate A, 32 hostile modules (identical with the 52-module set):

```
FENCE …/cand/fence_a.py sha256=2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc
POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
HONEST fixtures=126 admitted=117 refused=9 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry …/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph is not git's alternates file
HONEST-REFUSED n16-notes-ref …/logs/refs/notes has a name git does not write
HONEST-REFUSED n18-shallow-fetch repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
HONEST-REFUSED n08-tag-detached repo/.git/HEAD is not a plain branch HEAD
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=20 clean=20 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

Candidate B, 32 hostile modules (identical with the 52-module set):

```
FENCE …/cand/fence_b.py sha256=4e68592ca640a4f384b767db179ad79b8c5e9863086311ac87968810412ef393
POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=20 clean=20 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```

Delta on the frozen denominator: base refuses 13, **A opens exactly 4** (`n17-replace-ref`, `n20-linked-worktree`,
`n21-separate-gitdir`, `n22-alternates-in-d`) and still refuses the other 9, **B opens all 13**. Neither candidate
leaks a hostile module: 20/20 refusals, 12/12 sealed46 and 20/20 blind sealed50 clean for both.

## 3. Line-level repair surface

```
diff -u base A : 19 hunks, +313 −46   (862 lines vs 575)
diff -u base B : 22 hunks, +512 −65  (1059 lines vs 575)
diff -u A    B : 1090 lines of divergence
```

Neither candidate imports `subprocess` (A:48-51, B:44-47) — both keep the "no git child at all" property, so
every new admission is a decision over bytes already inside `d`.

Decision sites (all line numbers are in the candidate files):

| decision | base | A | B |
|---|---|---|---|
| store top-level allowlist | `GIT_TOP` 64-65 | 74-76 (`+FETCH_HEAD +worktrees`) | 75-76 (`+FETCH_HEAD +shallow +worktrees`) |
| worktree metadata allowlist | — | `WORKTREE_TOP` 77, `WORKTREE_DIRS` 78 | `WT_TOP` 78 |
| ref namespaces | `_refs` 278-296 (`heads/tags` only) | `GIT_REF_NAMESPACES` 79, `_refs` 383, `_ref_tree` 403 | `REFS_DIRS` 79, `REFS_FILES` 80, `_refs` 432, `_ref_tree` 460 |
| config sections | `CFG_SECTIONS={"core"}` 67 | 81 (`+extensions`) | 83-84 (`core/branch/extensions/remote/user` + subsections) |
| config key typing | `CFG_KEYS` 68-76 (literal) | 82-91 (`version`,`bool`,`false`) | 85-96 (`version,bool,false,text,refname,refspec,url`) |
| section/subsection grammar | `SECTION_LINE` 56, `KEY_LINE` 57 | 65, 66 (no subsection) | 60, 61 (quoted subsection; printable values) |
| `objects/info/*` | 327-345 (`info/` empty, else refuse) | 500-553 (only `alternates`) | 545-603 (`OBJ_INFO` 81: alternates/commit-graph/packs) |
| `info/*` | 508-516 (`exclude` only) | 704 (`exclude` only) | `INFO_FILES` 82 + `_info_refs` 700-720 |
| `.git` file | 213 refused outright | `_one_line` 148, `_pointer` 167, `_dir_ref` 193, `_tree` 273-321, `_gitfile_store` 800 | `GITFILE_LINE` 62, `_gitfile_target` 224, `_chain_ok` 167, `_resolve` 187, `_discover` 928 |
| `commondir` / wt `gitdir` | — | `_file_ref` 209, `_worktree` 743-798 (back-pointer only `lstat`ed) | `_wtmeta` 757-823 (back-pointer equality at 809) |
| `alternates` | — | `_alternates` 436-498, `ALTERNATES_DEPTH=4` 58, cap at 492 | `_alternates` 520-543, queue + `seen` (no depth cap) |
| HEAD value | `HEAD_REF` 55, check 474-477 | A:669 (store), A:772 (wtmeta): branch only | B:851-853 (store), B:779-781 (wtmeta): branch **or** 40-hex |
| reflog names | 372-380, 394 | 555-563, 577 (unchanged: `HEAD`, `refs/heads`, `refs/tags`) | 605-654 (`+refs/stash +notes +remotes +replace`, `_log_dir_ok` 618) |
| store classification driver | `_store` 453, `breach` 531 | `_store(…, seen)` 636 (memo), `breach` 813 (gitfiles loop 845) | `_store(kind, wt, queue)` 825, `_discover` 928, `breach` 996 (alternate queue) |

Efficiency: A buys 4 honest classes for 313 added lines; B buys 13 classes (+ the shape classes the probes
exercise) for 512. Both spend most of their delta on the same three mechanisms (pointer resolution, worktree
metadata, alternates closure); B additionally types five config classes and three ref namespaces.

## 4. What each OPENS (newly admitted shape) — risk table

"git-written" = the shape is produced by a git command as measured in this wave; "git-accepted" = hand-forged
but `git rev-parse`/`cat-file` accepts it. Risk is stated against the fence's own advertisement (all reads stay
inside `d`, no git child).

| # | newly admitted shape | base | **A** | **B** | risk of the opening | witness |
|---|---|---|---|---|---|---|
| 1 | `refs/replace/<40hex>` (flat, 40-hex leaf) | refuse 289 | **ADMIT** (79, 403-434) | ADMIT (79, 460-480) | none outside `d`: a replace ref is a local oid→oid rule; both require flat + 40-hex name and 40-hex body | git-written (`git replace A B`) — probe `replace-ref`; fixture `n17-replace-ref` |
| 2 | `.git` file → store dir inside `d` (`--separate-git-dir`) | refuse 213 | **ADMIT** (273-321, 800) | ADMIT (224, 928) | the whole store graph now hangs on a pointer: both resolve it, require a real dir inside `d`, then classify the target store's config/refs/objects incl. its alternates | git-written — probe `separate-gitdir`; escape pair `separate-gitdir-alt-outside` refused by both |
| 3 | `.git` file → `.git/worktrees/<id>` metadata | refuse 213 | **ADMIT** (743-798) | ADMIT (757-823) | same; additionally `commondir` must resolve inside `d` and be classified as a store | git-written — probes `linked-worktree`, `linked-worktree-relative`; `commondir-outside` and `wt-gitdir-outside` refused by both |
| 4 | `.git/worktrees/<id>/` inside a store | refuse 464 | **ADMIT** (724-741) | ADMIT (722-735 + discovery) | each metadata dir is classified; `gitdir` back-pointer must be inside `d` | git-written — same probes |
| 5 | `[extensions] relativeWorktrees = true` with `repositoryformatversion = 1` | refuse (section not allowlisted) | **ADMIT** (81-91, gated `saw_ext and version != "1"`) | ADMIT (83-96, gated `ext and version != "1"`) | inert extension flag; the version gate is the real guard | git-written — `git -c worktree.useRelativePaths=true worktree add` writes exactly `repositoryformatversion = 1` + `[extensions] relativeWorktrees = true` (probe `linked-worktree-relative` config, dumped) |
| 6 | `FETCH_HEAD` | refuse 464 | **ADMIT, content unread** (74) | ADMIT, rows validated (64, 864) | A: any bytes a fixture puts in `FETCH_HEAD` pass; git only *records* fetched refs there, it is not a pointer, so no read escapes — but A's own doctrine ("nothing admitted until every byte classified") is broken by its own allowlist; B validates the row shape | git-written — probe `fetch-head-real` (`<sha>\t\t../src`, B admits); A-only admission of junk measured in `fetch-head-junk` |
| 7 | `objects/info/alternates` inside `d` | refuse 342 | **ADMIT** to depth 4 (436-498) | ADMIT, unbounded + cycle-safe (520-543) | the escape vector this class exists for: a chain that borrows from outside `d`. Both follow the chain and refuse an out-of-`d` hop; A also refuses hop 5+ | git-written (`git clone --reference`) / git-accepted — probes `alternates-in-d`, `alternates-relative-inside`; `alternates-outside`, `alternates-escape-chain` refused by both; `alternates-chain6` refused by A, admitted by B |
| 8 | `.git/shallow` | refuse 464 | **refused** (74 lacks `shallow`) | **ADMIT** with hex rows (75, 860) | none: a list of boundary oids | git-written (`git fetch --depth`, `n18`) — probe `shallow-valid-sha`; `shallow-junk` refused by B |
| 9 | `HEAD` = 40-hex (detached HEAD) | refuse 474-477 | **refused** (A:669, A:772) | **ADMIT** (B:851-853, B:779-781) | none: an oid, no pointer | git-written (`git checkout --detach`, `git worktree add --detach`) — probes `detached-head`, `detached-linked-worktree`; fixtures `n03`, `n08` |
| 10 | `[user] name/email` | refuse (section) | **refused** (81) | **ADMIT** typed `text` ≤512 (85-96) | none: inert strings; B refuses an empty or >512-byte value | git-written (`git config --local user.name`) — probe `config-user`; fixture `n12` |
| 11 | `[remote "<n>"] url/fetch` (+ `[branch "<n>"] remote/merge`) | refuse (section) | **refused** (65, 81) | **ADMIT** with `_config_url` containment (335-350) + refspec/refname validators | the one genuinely dangerous new surface: `remote.<name>.url` is a path git *reads*. B accepts a network URL (inert) or a path that stays inside `d`, and refuses `file://…`, an absolute outside path, and any `..` that leaves `d` | git-written — probes `remote-relative-in-d`, `fetch-head-real`, `clone-local-in-d`; escapes `remote-abs-outside`, `remote-file-url-outside` refused by B |
| 12 | `refs/stash` (+ `logs/refs/stash`) | refuse 289/394 | **refused** (79, 555-563) | **ADMIT** (80, 443, 605-654) | none: a normal 40-hex ref in a top-level file slot | git-written (`git stash`) — probe `stash-ref`; fixture `n14` |
| 13 | `refs/notes/**` | refuse 289 | **refused** (79) | **ADMIT** plain subtree (79, 460-500) | none: 40-hex leaves | git-written (`git notes add`) — probe `notes-ref`; fixture `n16` |
| 14 | `refs/remotes/<n>/**` | refuse 289 | **refused** (79) | **ADMIT** one remote-name level, then plain (79, 470-478) | none for regular 40-hex remote-tracking refs; **residual gap**: the `<n>/HEAD` *symbolic* ref is refused (§7.1) | git-written — probes `remote-relative-in-d` (B stops only at `origin/HEAD`), `refs-remote-symref` |
| 15 | `objects/info/commit-graph`, `objects/info/packs` | refuse 342 | **refused** (522) | **ADMIT** size-capped (81, 567) | none: binary/text data, no path | git-written (`git commit-graph write`, `git update-server-info`) — probes `commit-graph`, `objects-info-packs`; fixture `n15`; `objects-info-unknown` refused by both |
| 16 | `info/refs` | refuse 512 | **refused** (704) | **ADMIT**, rows `sha\tref` validated (82, 700-720) | none: a dumb-transport listing | git-written (`git update-server-info`) — probe `server-info`; fixture `n07` |
| 17 | `worktrees/<id>/refs/{bisect,worktree}` | refuse | **refused** (A:794 reuses `_refs`; namespace gate A:393) | **ADMIT** exactly those two namespaces (B:737-755) | none: per-worktree refs, 40-hex leaves | git-written (`git bisect` inside a linked worktree) — probe `linked-worktree-bisect-ref` (`git rev-parse refs/bisect/bad` rc=0) |
| 18 | `.git` gitfile with **no trailing newline** | refuse | **ADMIT** (`_one_line` 148-165 strips an optional `\n`) | **refused** (`GITFILE_LINE` 62 requires `\n`) | none: target still must be inside `d`; but it is a byte shape git never writes (reader-only leniency) | git-**accepted**, not git-written — probe `gitfile-no-newline` (`git rev-parse HEAD` rc=0 on the stripped file) |
| 19 | alternates chain of 5+ hops inside `d` | refuse | **refused** (58, 492) | **ADMIT** (520-543) | none: every hop is checked; only the hop cap differs | git-written/readable — probe `alternates-chain6` (`git cat-file -t` = `commit` through 6 hops) |

## 5. What both keep CLOSED (measured, not assumed)

Every shape below was built, then offered to base/A/B; all three refused. "leak" would have been an ADMIT.

| kept closed | A site | B site | probe |
|---|---|---|---|
| `.git` file naming a store outside `d` | 193-206 (`_dir_ref` + `_inside`) | 187-211 (`_resolve`/`_chain_ok`) | `gitfile-outside` (git **accepts** the shape — `git -C wt rev-parse HEAD` rc=0, measured; both fences refuse because following it reads outside `d`) |
| `commondir` outside `d` | 786 (`_dir_ref`) | 791 (`_pointer`) + `_inside` 187-211 | `commondir-outside` |
| worktree `gitdir` back-pointer outside `d` | 783 (`_file_ref`) | 801 (`_pointer`) | `wt-gitdir-outside` |
| `alternates` row outside `d` | 479 | 520-543 (`_resolve`) | `alternates-outside` |
| a 2-hop `alternates` chain that borrows outside `d` | 487-497 (recursive, `seen`) | 520-543 (queue) | `alternates-escape-chain` (`git cat-file -t` = `commit`: the escape is live, both refuse) |
| n21 store with out-of-`d` alternates | 636-722 → `_objects` | discovery → `_objects` queue | `separate-gitdir-alt-outside` (git reads outside `d`; both refuse) |
| n20 worktree whose common store borrows outside `d` | same | same | `worktree-store-alt-outside` (same) |
| `[remote] url` = absolute outside path | section refused | `_config_url` 335-350 | `remote-abs-outside` |
| `[remote] url` = `file://…` | section refused | `_config_url` (`"://"` not in the network set) | `remote-file-url-outside` |
| `[include]`, `core.attributesFile` | 323-381 (`CFG_KEYS`) | 352-430 (`CFG_KEYS`) | `config-include`, `config-attributesfile` |
| unknown `objects/info/*` entry | 503-553 | 545-603 | `objects-info-unknown` |
| non-hex `refs/replace` leaf | 426 (`REPLACE_NAME`) | 473 (`SHA_NAME`) | `refs-replace-junk` |
| symlink anywhere in the tree | `_tree` 273-300 | `_tree` 283-310 | `symlink-in-tree` |
| special file / multi-link file anywhere | `_tree` + `_linked` | `_tree` + `_linked` | `hardlink-in-store` |
| junk `shallow` row | (file itself not allowlisted) | `_hex_lines` 505-518 | `shallow-junk` |
| non-record `FETCH_HEAD` row | — (A admits: §4/6) | `FETCH_LINE` 64 | `fetch-head-junk` |
| NUL/CR/non-ASCII in `config`, multi-line pointers, dangling pointer targets | 148-228, 323-381 | 167-238, 352-430 | exercised throughout; all three refuse |

Aggregate hostile evidence: 20/20 `refusals46`, 12/12 `sealed46`, **20/20 blind `sealed50`** for both
candidates — 52 hostile modules, zero leaks, zero build errors.

## 6. Differences where one candidate admits what the other refuses

### 6.1 B admits / A refuses — 9 of the 126 pinned fixtures, all over-refusals

| fixture(s) | A's refusal line | why B is correct (git reason, then fixture reason) |
|---|---|---|
| `n03-detached-head`, `n08-tag-detached` (+ `detached-linked-worktree`) | A:669 / A:772 (`HEAD_REF` only) | gitrepository-layout(5): "HEAD can also record a specific commit directly … Such a state is often called detached HEAD"; `git checkout --detach`/`git checkout <tag>` writes it. Fixture: pinned row in `population.txt` with `tree_sha256`, built by git, `fsck` clean (identity.jsonl) — a state git writes, so the fence must admit it |
| `n12-local-config-user` | A:81 (`CFG_SECTIONS`) | `git config --local user.name/…` writes `[user]`; git-config(1) documents `user.name`/`user.email`, and every `git commit` needs an identity. B types the value instead of refusing the section |
| `n13-remote-origin`, `n18-shallow-fetch` (first refusal hit) | A:65 (`SECTION_LINE` cannot parse `[remote "origin"]`) and A:81 | git-config(1) `remote.<name>.url`, `.fetch`; `branch.<name>.remote/.merge`; `git remote add`/`git clone` write them. The escape they carry is the URL path, which B checks with `_config_url` (inside-`d` path or inert network URL only) — refusing the whole section is over-refusal |
| `n14-stash-entry` | A:79 + A:555-563 (`refs`/`logs` namespaces) | git-stash(1): "The latest stash you created is stored in refs/stash". B allowlists the file (`REFS_FILES`) and its reflog |
| `n16-notes-ref` | A:79 + A:555-563 | git-notes(1): "By default, notes are saved to and read from refs/notes/commits" |
| `n15-commit-graph` | A:522 (`objects/info` holds only `alternates`) | `git commit-graph write` (and `fetch.writeCommitGraph`) writes `objects/info/commit-graph`; it carries no path. B admits it size-capped |
| `n07-reflog-gc` | A:704 (`info/` holds only `exclude`) | gitrepository-layout(5): "info/refs … regenerated by git update-server-info"; B validates the rows |
| `n18` again at the store level (`shallow`), demonstrated separately | A:74 (`GIT_TOP` lacks `shallow`) | gitrepository-layout(5): "shallow … internally used and maintained by shallow clone mechanism"; probe `shallow-valid-sha`: A REFUSE, B ADMIT, `git rev-parse` rc=0 |
| `linked-worktree-bisect-ref` | A:794 (`_refs` on the wt refs) + A:393 | per-worktree refs written by `git bisect` inside a linked worktree; B restricts to `bisect`/`worktree` exactly |

Every one of these is an **over-refusal by A**: the fixture is a pinned honest row, B admits it, and the shape
is produced by a git command. A therefore cannot reach `HONEST admitted=126` at any later stage without opening
these 9 sites; that is the whole of A's 117 vs B's 126.

### 6.2 A admits / B refuses — 2 shapes, both inside `d`, and B is the contract-faithful one

| shape | A | B | which is correct, and why |
|---|---|---|---|
| `.git` gitfile **without a trailing newline** (`probe gitfile-no-newline`) | ADMIT (`_one_line` 148-165 strips an optional `\n`; `_pointer` 167) | REFUSE (`GITFILE_LINE` 62 is anchored `…\n\Z`) | **B.** The frozen semantics are "states git itself writes" (claims §Named limits), and `git init --separate-git-dir` always terminates the `gitdir: <path>` line (measured content `gitdir: …/store\n`). A's rule is faithful to git's *reader* instead — measured: `git -C wt rev-parse HEAD` rc=0 on the stripped file — so A admits a byte shape no git command produces. Neither leaks: A still requires the target to be a real directory inside `d`. Risk if A is chosen: a one-byte authoring difference decides admission, i.e. the fence's contract becomes "bytes git tolerates" instead of "bytes git writes" |
| `FETCH_HEAD` row that is not `sha\t<desc>` (`probe fetch-head-junk`) | ADMIT (74: name-only) | REFUSE (`FETCH_LINE` 64, applied at 864) | **B**, on the claim's own doctrine, though this is *not* a security difference: git-fetch(1) documents FETCH_HEAD as "the names of refs that are fetched, together with the object names they point at"; `git fetch` writes only that row shape (probe `fetch-head-real`: `<sha>\t\t../src`, B admits). A's own docstring admits the gap ("admitted by name, content never read"), and because FETCH_HEAD is a record, not a pointer, the junk row cannot move a read outside `d` — measured: no hostile module in 52 exploits it (A: REFUSALS 20/20, SEALED 32/32 clean) |
| per-worktree `gitdir` back-pointer consistency (no verdict difference on any probe) | ADMIT any existing single-link file inside `d` (`_file_ref` 209) | REFUSE unless the file is a `gitdir:` gitfile pointing back at this metadata dir (809) | **B.** gitrepository-layout(5): `worktrees/<id>/gitdir` is "the absolute path back to the .git file that points to here". git writes a consistent pair; A admits an inconsistent one (still inside `d`, so no escape, but an unclassifiable state) |

### 6.3 A-only leniency that is a *closure* strength difference, not a verdict difference

- **A caps `alternates` at 4 hops** (A:58, 492) where git has no cap (gitrepository-layout(5) — one path per
  line per store; measured 6-hop chain read by `git cat-file`). B follows the queue with a `seen` guard. This
  makes A refuse `alternates-chain6`, which B admits: **B correct**, A's cap is an invented false-refusal bound.
- **A's `_pointer` requires exactly `gitdir: ` (one space)** and A strips an optional trailing newline
  (`_one_line` 148-165, `_pointer` 167-191); B's regex demands the newline and accepts any printable path
  (`GITFILE_LINE` 62). Both refuse the trailing-space and double-space variants git itself rejects (measured in
  A's own report); no differential except the missing-newline case in §6.2.
- **A resolves pointers with `os.path.normpath` only** and lstats the target, while **B lstats every component
  below `d`** (`_chain_ok` 167-186) so the lexical path *is* the real path. Same verdicts on every probe; B is
  strictly stronger (a component symlink would be caught even if a future walk change stopped refusing symlinks).

## 7. Residual defects left by BOTH candidates (outside the frozen denominator — for S2, not this predicate)

Measured, git-written states that both A and B still refuse. None is in the 126, so neither affects the C1
predicate; they are the open frontier the S2 repair should not inherit.

1. **`refs/remotes/<remote>/HEAD` (symbolic ref).** `git fetch <remote>` with the configured refspec wrote
   `refs/remotes/origin/HEAD` = `ref: refs/remotes/origin/main` (probe `remote-relative-in-d`); git-remote(1)
   documents it as the symbolic ref set by clone/`set-head`. A refuses the `refs/remotes` namespace (79); B
   refuses the non-40-hex leaf (500). Probe `refs-remote-symref`: base/A/B all REFUSE, `git rev-parse` rc=0.
2. **`remote.<name>.url = file://<path inside d>`.** `git remote add origin file://…/src` inside `d` (probe
   `file-url-inside-d`); B refuses categorically ("not a plain network URL", 341) even though the target is
   inside `d`, A refuses the section. A `file://` URL that names a path inside `d` is an inside-`d` read and
   should be contained, not refused.
3. **Local `git clone` inside `d`.** git hardlinks the source objects, so the `nlink > 1` rule (`_linked`)
   refuses the clone for base, A and B alike (probe `clone-local-in-d`). This is a pre-existing base rule, not a
   repair regression — but it means "states git writes" and "single-link only" are in tension for local clones.
4. **`#` comment rows in `objects/info/alternates`.** git's reader skips them (measured: `cat-file` reaches the
   object); A refuses explicitly ("carries a comment line git does not write", 473-474), B by resolving the row
   as a path. Both stricter than git's reader, consistent with git's writer (git writes no comments).

## 8. VERDICT

**Candidate B is the correct repair; candidate A is an incomplete repair.**

- On the frozen denominator: base 113/126 → **A 117/126 (still `PREDICATE fail`, 9 honest over-refusals)** →
  **B 126/126 (`PREDICATE pass`)** with REFUSALS 20/20, SEALED 12/12 and blind SEALED 20/20 clean for both.
- Every B-over-A admission is a state git writes (detached `HEAD`, `[user]`, `[remote]`/`[branch]`,
  `refs/stash`, `refs/notes`, `objects/info/commit-graph`, `objects/info/packs`, `info/refs`, `shallow`,
  per-worktree `refs/bisect`, detached linked-worktree `HEAD`) — A's refusals there are pure over-refusal.
- The only A-over-B admissions are two byte shapes git accepts but does not write (`gitfile` without a trailing
  newline, junk `FETCH_HEAD` rows) and one laxity (no `gitdir` back-pointer check). All three stay inside `d`
  and leak nothing (52/52 hostile modules clean for A), but they weaken A's own stated doctrine and make the
  admitted state space "what git tolerates" instead of "what git writes".
- Line budget: A spends 313 added lines across 19 hunks to open 4 classes; B spends 512 across 22 to open 13,
  with typed validators for the one dangerous new surface (`remote.<name>.url`) and a component-wise pointer
  resolver. On the maintenance axis B is not cheaper, but every one of its extra lines buys a measured honest
  class or a measured closure, and none of its openings was exploited by the 52 hostile modules.
- Neither candidate is complete: §7 lists four git-written (or git-tolerated) shapes both still refuse, so the
  S2 repair should carry them as named limits rather than claim a closed allowlist.

## 9. Limits of this measurement, and scratch state

- Measured revision is the stage-1 freeze clone only; the live tip's `plans/fixture_fence.py` (`57adce4a…`,
  S2) was not evaluated and nothing here judges it.
- The blind `sealed50` set was sourced from the live lane at `d52243af` and copied into the scratch clone
  (`TREE dirty=1`, `--allow-dirty`); it is not part of the frozen denominator and its 20/20 result is
  supplementary to `SEALED 12/12`.
- The mutant leg (`--skip-mutants`) was not run for either candidate: the carried r49 battery is a candidate
  against the r49 fence and re-derivation with witnessed kills is a separate seat's item (QUALITY Q38).
- The outside-`d` syscall property (round-46 counter B1-B6) was not re-scored; both candidates start no git
  child (`import` list checked), and the probes above exercise path containment only.
- Three probes initially mis-reported because of my own fixture bugs (host `rerere.enabled=true` via
  `XDG_CONFIG_HOME`; a relative `alternates` row with one `..` too many; a `.git` file naming a worktree
  directory instead of its store, which made git itself return rc 128). All were fixed and the whole 41-case
  battery re-run; the quoted results are from the fixed run (`LEAKS none`). The corrected outside-gitfile
  witness is the honest one: git **accepts** a `.git` file naming a store outside `d` (rc=0), and both fences
  refuse it by containment.
- Scratch: `/fast/scratch/hyaku/kengaku-r50/R50C1ExecRepairDiff/` was created for this seat and is removed
  after this report is written (clone, candidate copies, probe fixtures, diffs). No lane file, no sibling wave
  file and no production file was written; nothing was committed, pushed, stashed or checked out.

VERDICT: **B correct, A incomplete (fails HONEST 126/126 by 9 pinned fixtures); A-only admissions are inside-`d`
and non-leaking but contract-unfaithful; both leave four git-written shapes open (§7).**
