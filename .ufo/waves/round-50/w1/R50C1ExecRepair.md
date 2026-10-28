# R50C1ExecRepair — R50-C1 five-class fence repair (executor)

**Axes named.** `novelty` (R50-C1) only. This seat applies the five assigned mechanisms to a scratch candidate
of `plans/fixture_fence.py`, witnesses the refusal direction of every path it opens, and measures the candidate
with the frozen counter. It claims no C1/C2 admission, edits no production file, and does not judge the claim.

**REV** `3b02d573d58cc6d2e0d27ef92ac0815354912252` — the stage-1 freeze. Verified ancestor of the lane tip
(`git merge-base --is-ancestor 3b02d57 HEAD` → `ANCESTOR_OK`; lane tip at seat start `5c56819f7964f4…`).
All measurements ran on `git clone --shared` at that commit in scratch, `TREE dirty=0` printed by the counter.

**Digests at the revision measured.** base fence `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`
(matches the frozen pin), counter `f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76` (matches),
population `b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69` (matches, 126 rows).

## Deliverable

`.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py` — full candidate, sha256
`2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc`, byte-copied from the base fence and then
edited in place (minimal diff, no retyping of the unchanged 500 lines). Full unified diff against the frozen
base fence: `C1ExecRepair/fence_candidate.diff` (sha256 `223982d667bf7b084e3f2c37a2bd3ef712e007500407cfaef4778e2b98d5568f`,
+335/−48, 19 hunks).

## The five mechanisms, as implemented

| item | mechanism | code site (candidate) | base behaviour | candidate behaviour |
|---|---|---|---|---|
| 1 | `.git` FILE whose `gitdir:` target resolves **inside `d`** becomes an extra collected store; a `commondir` it names must also resolve inside `d` | `_tree` (queue `gitfiles`), new `_one_line`/`_pointer`/`_dir_ref`/`_file_ref`, new `_gitfile_store`/`_worktrees`/`_worktree`, `breach` gitfile loop, lane set | blanket `return "… is a file (gitdir redirect), not a directory"` | target lstat'ed: must exist, be a dir inside `d`, not a symlink; then classified as a store (n21) or as per-worktree metadata (n20) with `gitdir` (plain path, git's own shape — measured) and `commondir` both resolved inside `d`; common store classified with memoization (`seen`) so `repo/.git ↔ commondir ↔ gitfile` cannot recurse. Pointer text is taken **verbatim after git's exact `gitdir: ` prefix** (one space) — git trims nothing (measured) |
| 2 | `objects/info/alternates` admitted only when **every** line resolves inside `d` — and every hop it names | `_alternates` (recursive, `ALTERNATES_DEPTH = 4`, `seen` visited set), called from `_objects`'s `info` branch | any entry under `objects/info/` refused ("object-store redirect") | `info/` may hold exactly `alternates`; each line is taken **verbatim** (git trims nothing — measured) and must resolve inside `d` (relative entries against the object dir holding the file), exist, be a dir, not be a symlink; the target's own `info/alternates` is then followed, so an in-`d` hop that borrows from outside `d` is refused (without this, a two-hop chain was an admitted read escape); cycles terminate via `seen`, chains deeper than 4 are refused; comment lines and an empty file are refused; any other `info/` entry still refused |
| 3 | `.git/FETCH_HEAD` allowlisted, content never read | `GIT_TOP` | "not a plain-init entry" | admitted by name; regular-file + single-hardlink checks only, no read |
| 4 | `refs/replace/<40hex>` admitted, any other `refs/*` refused | `GIT_REF_NAMESPACES`, `_refs` → `_ref_tree(…, ns)`, `REPLACE_NAME` | `refs/replace is not refs/heads or refs/tags` | `heads`, `tags`, `replace` only; `replace` leaves must be exactly 40 lowercase hex and flat (no subdirs) |
| 5 | every existing refusal path stays closed | unchanged guards + 39-case adversarial harness (below) | — | out-of-`d`/dangling/non-dir gitfile, out-of-`d` `commondir` and worktree `gitdir`, out-of-`d`/dangling/symlink alternates, `[include]`, symlink, hardlink, multiple lines, BOM, and git's own pointer grammar (trailing spaces, missing space, double space) — all still refused; a missing final newline is admitted because git admits it |

**One measured dependency item 1 needed.** `git worktree add --relative-paths` writes
`core.repositoryformatversion = 1` **and** `[extensions] relativeWorktrees = true` (measured verbatim, see
below). The gitfile admission alone therefore reached a pre-existing config refusal
(`core.repositoryformatversion must be 0`) and left n20 refused. The candidate admits exactly that one
extension: `repositoryformatversion ∈ {0,1}`, `[extensions]` may hold only `relativeWorktrees` (boolean), and
`[extensions]` is refused unless `repositoryformatversion = 1`. Every other section/key stays refused
(`[include]`, `[user]`, `[remote]`, `extensions.objectFormat` all witnessed refused).

`n18` needs **four** further admissions that the item does not assign (measured; see residual table). Only
`FETCH_HEAD` was assigned and only `FETCH_HEAD` is implemented.

## Exact commands run (all in `git clone --shared` at 3b02d57, `TMPDIR=/fast/scratch/hyaku/kengaku-r50/R50C1ExecRepair`)

```
git clone --shared --no-checkout <lane> lane && git -C lane switch --detach 3b02d573d58cc6d2e0d27ef92ac0815354912252
python3 plans/round50_c1_verify.py --lane . --work "$S/work-base"  --skip-mutants                          # control
python3 plans/round50_c1_verify.py --lane . --work "$S/work-final" --fence <candidate> --skip-mutants      # scored
python3 plans/round50_c1_verify.py --lane . --work "$S/work-mut2"  --fence <candidate>                     # mutant leg
python3 probe_adv.py  lane <candidate>                                                                    # 39-case witness
diff -u lane/plans/fixture_fence.py <candidate>                                                           # the diff
```

Scratch-only driver `probe_adv.py` is copied into this directory as `receipt-adversarial-harness.py`. Fixture
git env was set per subprocess by the population builder; nothing global was exported.

## Observed output — base fence control (verbatim, `receipt-base-fence-control.txt`)

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE …/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```
(the counter prints 12 of 13 `HONEST-REFUSED` lines; the 13th, `n08-tag-detached`, appears in the candidate
run below). The base refusal set is therefore **13**, not 5: the five classes this item names
(`n17`, `n18`, `n20`, `n21`, `n22`) **plus eight older ones** (`n03`, `n07`, `n08`, `n12`, `n13`, `n14`, `n15`,
`n16`).

## Observed output — candidate, scored legs (verbatim, `receipt-candidate-skip-mutants.txt`)

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE …/C1ExecRepair/fence_candidate.py sha256=2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=117 refused=9 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../../work-final/k50-c1-iq5opdve/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph is not git's alternates file
HONEST-REFUSED n16-notes-ref ../../../../work-final/k50-c1-iq5opdve/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
HONEST-REFUSED n18-shallow-fetch repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
HONEST-REFUSED n08-tag-detached repo/.git/HEAD is not a plain branch HEAD
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```
Exit 1. **All 20 frozen refusal modules and all 12 sealed modules are still refused** — the repair opens no
hostile path the counter can see.

## Observed output — mutant leg on the candidate (verbatim tail, `receipt-candidate-mutants.txt`)

```
MUTANTS total=23 caught=1 broken=15 floor=12 verdict=unmet
PREDICATE R50-C1 fail
```
The carried r49 battery is a **candidate** (claims: "candidate only"), and this is why: 15 of 23 payloads no
longer apply to the base-fence text (`patch-rc=1`), 7 apply and survive, 1 kills. The battery must be
re-derived with witnessed kills against the S2 fence (Q38) — the lane's mutant seat owns that. Recorded here as
a measured datum, not as a defect of this candidate.

**External corroboration of the final digest.** Peer `R50C1ExecMutRebase` authored a 19-row battery on this
candidate's own bytes and re-measured it against the final digest
`2b142a85…` independently: `caught=17 survived=0 not_applicable=2` (the two that no longer apply are anchored in
the rewritten `_objects`/`info` block; every gitfile/commondir/refs/config/argv/cap/hardlink/symlink row still
applies and still kills). So the digest move at the `alternates` fix did not silently disarm the rows that
matter, and the two recursive-alternates rows are carried forward as the S2 pointer for a class the frozen 32
hostile modules cannot see.

## Observed output — adversarial witness of the new surface (48 cases, 0 mismatched)

`receipt-adversarial-48.txt`, harness `receipt-adversarial-harness.py`. Each case copies a measured honest
fixture and changes exactly one thing; honest copies must ADMIT, hostile copies must BREACH.

```
honest-n17/n20/n21/n22                        ADMIT
gitfile-out-rel / -abs                        BREACH  names '…', which resolves outside the fixture
gitfile-missing                               BREACH  names '../nope', which does not exist
gitfile-file-target                           BREACH  names '../afile', which is not a directory
gitfile-symlink                               BREACH  linkstore is a symlink
gitfile-hardlink                              BREACH  wt/.git has more than one hard link
gitfile-two-lines / gitfile-bom               BREACH  is not a single line / carries a non-ASCII byte
gitfile-target-trailing-spaces                BREACH  names '../store   ', which does not exist
gitfile-prefix-without-space                  BREACH  is not a `gitdir: ` redirect
gitfile-prefix-double-space                   BREACH  names ' ../store', which does not exist
HONEST-gitfile-no-trailing-newline             ADMIT  (git accepts it: measured)
commondir-out / -trailing-spaces              BREACH  names '…', which resolves outside the fixture / does not exist
wt-gitdir-out / -abs / -trailing-spaces       BREACH  names '…', which resolves outside the fixture / does not exist
wt-unknown-entry                              BREACH  …/locked is not worktree metadata git writes
alt-rel-out / alt-abs-out / two-lines-one-out BREACH  names '…', which resolves outside the fixture
alt-dangling / alt-empty / alt-comment        BREACH  does not exist / names no object directory / comment line
alt-symlink / alt-hardlink                    BREACH  is a symlink / has more than one hard link
alt-chain-repo / -bare / -plain               BREACH  … -> '…' names '…', which resolves outside the fixture
alt-trailing-space                            BREACH  names '…/objects   ', which does not exist
HONEST-alt-cycle / -2hop / -4hop-at-cap     ADMIT  (all hops inside d; cycle terminates via `seen`; 4 hops = the cap admits)
alt-chain-cap5 (5 in-d hops)                  BREACH  … -> '../../../h1/objects' -> … -> '../../h4/objects' chains deeper than 4 object stores
alt-chain-cap-escape (4 in-d then outside)    BREACH  … -> '../../h4/objects' names '…/store/.git/objects', which resolves outside the fixture
ref-replace-nonhex / -nested / -badbody       BREACH  not a 40-hex replace ref / subdirectory / not a 40-hex ref
ref-notes                                     BREACH  is not refs/heads, refs/tags or refs/replace
cfg-include / cfg-user / cfg-ext-objectformat BREACH  section/key not allowlisted
cfg-ext-v0 / cfg-v2                           BREACH  needs repositoryformatversion = 1 / must be 0 or 1
SUMMARY cases=48 mismatched=0
```

The three `alt-chain-*` rows are the shape peer `R50C1ExecAlternates` measured as an escape at digest
`9baedf13` (an entry inside `d` whose own `alternates` borrow from outside `d`): a one-level checker admits it,
the recursive one refuses it on the hop. The repo-hop row copies a complete plain-init store into `a/.git` first,
so its refusal cannot come from a missing store entry — the reason names the hop.

**The depth cap is a refusal, not a decision point** (blind critic `R50C1CritBlind1`'s F5 challenge). Three
fixtures pin it: five in-`d` hops → BREACH whose reason walks the whole chain and ends `chains deeper than 4
object stores`; four in-`d` hops then an outside hop → BREACH by **containment**, reason naming the chain and
the outside path; and an honest four-hop chain **at** the cap → ADMIT, so the cap is not enforced by blanket
refusal and the honest leg does not pay for it. Two design notes the same critic asked for: the visited set is
keyed on `_norm`, which collapses `.`/`..` spellings. That is equivalent to a `realpath` key **only because
`_tree` refuses every symlink anywhere under `d`** — pointer-level `lstat` alone would not be enough, since an
intermediate symlink component leaves the final component a real directory. The blanket symlink rule is
therefore load-bearing for two properties, not one: whoever narrows it (the first honest class that legitimately
carries a symlink) must re-run this leg with a symlinked intermediate component, because no fixture in the
current set observes that axis — `..`-based fixtures cannot, `normpath` collapses them. A dedupe skip is sound
because the first visit processed every hop of that node to completion — any refusal returns immediately, so a
skipped node cannot hide an escape.

**Cross-check.** Peer `R50C1ExecGitfile` ran an independent 14-case gitfile/commondir table and reported
13/14 at the previous digest (`6df6a2a3…`): the one divergence was that my `_pointer` stripped trailing
whitespace from the `gitdir:` line while git keeps it and refuses the fixture. I reproduced git's grammar
myself (per-command env only) before changing anything:

```
base      gitdir: ../store\n       ACCEPT          sp     'gitdir: ../store   \n'  REJECT
nonl      gitdir: ../store         ACCEPT          nospace 'gitdir:../store\n'      REJECT
crlf      gitdir: ../store\r\n     ACCEPT          twospace 'gitdir:  ../store\n'    REJECT
commondir '../..   \n'             REJECT          worktree gitdir '…/wt/.git   \n' REJECT
```

so the candidate now requires git's exact prefix `gitdir: ` and trims nothing. Scored legs are unchanged by
the tightening (`117/9`, `20/20`, `12/12`), which is the point: the honest population writes no such shape.

## Blind hostile modules authored against this candidate (external check)

Two sealed50 modules were written blind against the branches this candidate opens
(`C1CritBlind1/sealed/`: `s50_gitfile_symlink_chain.py` `70705f02…`, `s50_alternates_dotdot_abs.py`
`9fe77895…`). Installed into a scratch clone's `plans/sealed50/` and run through the same counter
(`--allow-dirty --skip-mutants`, candidate as `--fence`), receipt `receipt-blind50-crosscheck.txt`:

```
SEALED total=2 clean=2 leaked=0 build_errors=0
s50_gitfile_symlink_chain.py    s50-gitfile-symlink-chain    BREACH hop2 is a symlink
s50_alternates_dotdot_abs.py    s50-alternates-dotdot-abs    BREACH lane/.git/objects/info/alternates names
  '…/lane/.git/objects/../../../../store/.git/objects', which resolves outside the fixture
```

Both are refused, but **not both by the newly opened branch** (the critic's F1 distinction, which they were right
to press): the gitfile chain dies on the pre-existing symlink `lstat` (`hop2 is a symlink`, a rule the base fence
already had), while the alternates line dies on containment after `..` collapse — i.e. one witness of a kept rule
and one witness of the new one. The claimed discriminator ("unnormalized lexical containment admits both") does
not fire here because `_inside` collapses `..` with `os.path.normpath` **before** the prefix test (not
`PurePath.is_relative_to` on raw text) and every pointer target is `lstat`'ed for symlink-hood.

The critic also named an unbuilt shape — chained alternates through a non-repository object dir inside `d`. That
shape was independently measured as an escape at `9baedf13` (see the `alt-chain-*` rows above); the recursive
`_alternates` now refuses all three hop variants, and the two honest in-`d` chain rows still admit.

## Class-by-class outcome

| class | base | candidate | note |
|---|---|---|---|
| `n17-replace-ref` | refused (`refs/replace`) | **ADMIT** | item 4 |
| `n20-linked-worktree` | refused (`.git` file) | **ADMIT** | item 1 + the one measured extension key |
| `n21-separate-gitdir` | refused (`.git` file) | **ADMIT** | item 1 |
| `n22-alternates-in-d` | refused (`info/alternates`) | **ADMIT** | item 2 |
| `n18-shallow-fetch` | refused (`FETCH_HEAD`) | **still refused** | `FETCH_HEAD` is admitted (item 3 done), but the same fixture carries four shapes outside the item — see below |

### `n18` residual, measured verbatim

```
[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = true\n
[remote "origin"]\n\turl = ../src\n\tfetch = +refs/heads/*:refs/remotes/origin/*\n
```
plus `.git/shallow` = `da9314e69a1a45b05fd69755f0c6aa7442abdbb1`, `refs/remotes/origin/master`,
`logs/refs/remotes/origin/master`. So admitting `n18` honestly needs (a) `SECTION_LINE` to accept the quoted
subsection form `[remote "origin"]`, (b) `KEY_LINE` to accept a refspec value (`+`, `*`, `:` are outside its
value charset), (c) `refs/remotes` in the ref namespaces, (d) `logs/refs/remotes/…` in `_log_name_ok`, and
(e) `.git/shallow`. (a)+(b) is the `n13` site; `(c)`–`(e)` are this class only. None is assigned to this item
and `FETCH_HEAD` allowlisting alone reaches the config site first (deterministic; `config` sorts before
`shallow`). I did not implement them: that would be unassigned admission surface, and `shallow` alone would
have changed no verdict.

## The diff against the base fence

19 hunks; full text in `C1ExecRepair/fence_candidate.diff`.

| hunk | site | change |
|---|---|---|
| 1 | module docstring | structure items 3–7: gitfile admission, `FETCH_HEAD`, `info/alternates`, `refs/replace`, `worktrees/`, the one extension key, the "`.git` file is not a redirect until proved" rule |
| 2 | constants | `REPLACE_NAME`; `GIT_TOP` += `FETCH_HEAD`, `worktrees`; `GIT_DIRS` += `worktrees`; new `WORKTREE_TOP`/`WORKTREE_DIRS`/`GIT_REF_NAMESPACES`; `GITDIR = b"gitdir: "` (git's exact prefix, space included); `CFG_SECTIONS` += `extensions`; `repositoryformatversion` `"0"`→`"version"`; `("extensions","relativeworktrees"): "bool"` |
| 3 | new helpers | `_one_line`, `_pointer`, `_dir_ref`, `_file_ref` (lexical resolution only: no `resolve()`, no follow; pointer text verbatim, nothing trimmed) |
| 4–7 | `_tree` | returns `(repos, gitfiles, reason)`; the blanket `.git`-FILE kill is replaced by parse-and-queue (`gitdir:` resolved inside `d`), placed **after** the existing regular-file and single-hardlink guards so those still refuse first |
| 8 | `_config` | `version`/`saw_ext` tracking; `version` values `{0,1}`; `[extensions]` requires `repositoryformatversion = 1`; dead `need == "0"` branch removed |
| 9–11 | `_refs` / `_ref_tree` | namespace set, `ns` threaded through recursion, `replace` leaves must be flat 40-hex |
| 12 | `_alternates` + `_objects` | recursive validator (`seen` + `ALTERNATES_DEPTH = 4`), verbatim lines, every hop followed; `info/` may hold only `alternates`, every other entry still refused; new `ALTERNATES_DEPTH` constant |
| 13 | `_store` | `(gd, label, d, seen)` + memo + `worktrees` hook + `_objects(…, d)` |
| 14 | `_worktrees`, `_worktree`, `_gitfile_store` | per-worktree metadata allowlist (`HEAD`, `ORIG_HEAD`, `index`, `logs/`, empty-or-plain `refs/`, `gitdir`, `commondir`); `gitdir` is a **plain path** (measured), `commondir` resolved against the metadata dir, common store classified with `seen` |
| 15–18 | `breach` | `repos, gitfiles, why`; stores then gitfile targets; `--lane` may be a gitfile repo (n21 `lane = wt`) |

Four defects were found and fixed during the wave, all by measurement (two by peers' independent tables): a
duplicated `_objects` call; an edit that dropped `_refs(gd / "refs", …)` from `_store`, which made `n17` pass
**by absence of refs classification** rather than by the `replace` allowlist — the 20 frozen refusal modules and
12 sealed modules did **not** catch that drop, only the adversarial harness did (a `refs/notes` name and a
non-hex `refs/replace` leaf were briefly admitted); a `gitdir:` parse that trimmed whitespace git keeps, which
admitted a gitfile git itself rejects; and a **one-level `alternates` check**, which admitted a two-hop chain
whose second hop borrows from outside `d` (a genuine read escape, measured by peer `R50C1ExecAlternates` at
`9baedf13`, and the same shape blind critic `R50C1CritBlind1` had named as unbuilt). The last one is why
`_alternates` is recursive with a visited set and a depth cap. Present in the final file: `_refs` is called from
both
`_store` and `_worktree`.

## Limits and inherited observations

- The pointer grammar is now git's, with two declared divergences, both named by peer `R50C1ExecGitfile`'s
  16-case table: (a) **strict** — a CR (including CRLF) in a `.git`/`commondir`/`gitdir` file is refused, where
  git 2.56.0 accepts a CRLF terminator; no fixture in the frozen population writes one, and a refusal cannot
  admit anything. (b) **safety-neutral** — a `.git` file with no final newline is admitted, which git accepts but
  git itself never writes. Neither changes an admission among the 126.
- `ALTERNATES_DEPTH = 4` bounds an `alternates` chain; a deeper chain is refused. The honest population is depth
  1, and git's own recursion limit is the same order of magnitude, so this is a bound on pathological input
  rather than a rule about states git writes.
- **`mount cross` (item 5) is vacuous at the base.** `grep -n "st_dev\|mount\|statvfs"` on the frozen base fence
  returns nothing: the base has no mount-boundary leg, so there is no existing path to keep closed, and I added
  none (unassigned admission/refusal surface). A mount leg would be a new item.
- **`_rel(q, label)` quirk, inherited unchanged.** In `_logs` the reason argument is a *label* (`repo/.git/logs`),
  not a path, so `os.path.relpath` resolves it against the process cwd and some hostile reasons read as
  `../../../../work-…/repo/.git/logs/refs/stash`. Cosmetic, pre-existing, untouched (it is why the two `n14`/`n16`
  receipt lines carry scratch paths).
- The candidate starts **no child process** (`grep -n "subprocess\|Popen\|os.system\|execv\|fork"` → none), so
  the round-46 outside-`d` read property is untouched by construction; not re-scored here.
- The `[extensions]` admission is a real widening of the config surface. It is bounded to one key and gated on
  `repositoryformatversion = 1`; `extensions.objectFormat`, `extensions.relativeWorktrees` with version 0, and
  version 2 are all witnessed refused. A reviewer should decide whether the S2 fence wants `relativeWorktrees`
  at all (it is what `git worktree add --relative-paths`, i.e. the frozen `n20` fixture, writes).
- Importing the candidate with `importlib` writes a `__pycache__/` next to it; I removed it from the deliverable
  directory, but any further counter run recreates it — keep it out of the S2 commit.
- I did not touch the lane, `plans/*`, `corpus/*`, `.ufo/state`, or any sibling repo; no git/jj mutation outside
  my own scratch clone's detached checkout of the freeze commit.
- **Coexistence note (not my write).** The lane's `plans/fixture_fence.py` was `05d5fe03…` when I started; it
  now reads `57adce4a…` and is **committed** at `6db0279` ("round-50: S3 fence repair … sealed50 hostile set,
  re-derived mutant battery"), worktree clean, an ancestor of the tip I last observed (`d45c5bb2`). At 14:36 I
  observed it as ` M` mid-flight; it has since landed. So the state is one **landed** repair plus my unlanded
  scratch candidate — still "choose one, do not stack them". My numbers were measured against the frozen base
  fence `05d5fe03…` in a clone at `3b02d57`, so they are evidence about the candidate and about the frozen
  control, not a verdict on the landing tip. The lane's mutant battery was also replaced at that commit, so my
  `total=23 caught=1 broken=15` is a datum about the superseded carried battery only.

## Files written

- `.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py` (full candidate)
- `.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.diff`
- `.ufo/waves/round-50/w1/C1ExecRepair/receipt-base-fence-control.txt`
- `.ufo/waves/round-50/w1/C1ExecRepair/receipt-candidate-skip-mutants.txt`
- `.ufo/waves/round-50/w1/C1ExecRepair/receipt-candidate-mutants.txt`
- `.ufo/waves/round-50/w1/C1ExecRepair/receipt-adversarial-48.txt`
- `.ufo/waves/round-50/w1/C1ExecRepair/receipt-adversarial-harness.py`
- `.ufo/waves/round-50/w1/C1ExecRepair/receipt-blind50-crosscheck.txt` (external blind modules)

Tool installs: none (no pacman transaction attempted; nothing needed).

Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1ExecRepair` removed before yield; no scratch tree left on disk.

## VERDICT

`DELIVERED_WITH_RESIDUAL` — all five assigned mechanisms implemented as a scratch candidate and each witnessed
in its refusal direction (48/48 cases, `mismatched=0`), with `REFUSALS 20/20 clean, leaked=0`,
`SEALED 12/12 clean, leaked=0`, and both externally authored blind modules aimed at these branches refused by
the rules under test (2/2, leg-specific reasons), and the two-hop `alternates` chain that a one-level check
admitted is now refused on the hop (3/3 variants) while honest in-`d` chains still admit. HONEST moves
`113 → 117` (four of the five named classes: `n17`, `n20`, `n21`,
`n22`); `n18` remains refused because the item's `FETCH_HEAD` mechanism is necessary but not sufficient, and the
four remaining legs (quoted-section config with a refspec, `refs/remotes`, `logs/refs/remotes`, `shallow`) are
outside this item and `n13`'s site. The peer-verified divergence at the previous digest (trailing whitespace on
a `gitdir:` line: fence looser than git) is closed by matching git's pointer grammar exactly. The candidate is
**not** a landing patch by itself: the predicate still reads `fail` at `admitted=117`, and the eight older
classes plus `n18` remain for other seats/the integrator. No claim is made that R50-C1 is admitted.
