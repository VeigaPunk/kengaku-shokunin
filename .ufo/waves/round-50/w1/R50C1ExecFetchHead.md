# R50C1ExecFetchHead — the `.git/FETCH_HEAD` leg of R50-C1 (novelty)

REV `5c56819f7964f4af19c960de08a49cd8f95781ce` (lane tip measured; `git merge-base --is-ancestor
3b02d573d58cc6d2e0d27ef92ac0815354912252 5c56819f7964f4af19c960de08a49cd8f95781ce` → exit 0, so the stage-1
freeze is an ancestor). Measurement tree: `git clone --shared` of the lane at that revision, scratch root
`/fast/scratch/hyaku/kengaku-r50/R50C1ExecFetchHead` (`$S` below), never the live checkout.

Fences in play (sha256 measured, `sha256sum`):

| name | path | sha256 |
|---|---|---|
| base | `plans/fixture_fence.py` @ REV | `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` |
| candidate | `.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py` | `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52` |
| candidate+names | scratch `fence_fetch_head_only.py` | `cdb9d00c22b4d8a655cbc6be8dbe3494bf3768ad24bb30cc2880c71fdaf6ac15` |
| candidate+names+remotes | scratch `fence_fetch_head.py` | `80875a1422ff8d6ddf8d0329fb5e7692b9081945e7523653c615c38c2f7856e5` |

## Axes named

R50-C1 works the **novelty** axis. This seat owns one leg of it, and the leg is measured on four sub-axes:

1. **honest admission** — the frozen honest class `n18-shallow-fetch` is admitted (its store is a state git
   itself writes).
2. **indirection refusal** — the same store entry as a symlink (outside or inside `d`), as a directory, as a
   FIFO or as a hard link is refused.
3. **size bound** — a `FETCH_HEAD`/`shallow` above the fence's `TEXT_CAP` (65536) is refused; at the cap it is
   admitted (`>` not `>=`).
4. **read-freedom** — admitting the *name* adds no `open()` of the file, so the admission cannot carry a read,
   and the widened `refs/remotes`/`logs/refs/remotes` namespace this class needs stays closed to the same
   redirect shapes as every other ref namespace.

## Commands run (all from `$S`, Python 3.14.8)

```
git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout -q 5c56819f7964f4af19c960de08a49cd8f95781ce
python3 "$S/cases_fetch_head.py" "$S/lane" "$S/work" <fence.py> [<fence.py> ...]     # 17-case table, 3 fences
python3 "$S/dump_vectors.py" "$S/lane" "$S/vecwork" <candidate> <repaired>           # full verdict vectors
cd "$S/lane" && python3 plans/round50_c1_verify.py --lane . --work "$S/cw" --fence <fence.py> --skip-mutants
diff -u <candidate> <repaired>                                                       # repair payload below
```

Both drivers build fixtures through the frozen `plans/honest50/build_honest_population.py` `build_once` (which
routes every git call through `round44_c1_verify.Ctx.git`, i.e. `git -C <repo> …` after asserting
`rev-parse --show-toplevel` equals the fixture repo), copy the one built fixture per case, mutate only the named
store entry, and call `fence.breach(dir, argv, tool)` exactly as the counter does. `TEXT_CAP` is asserted equal
to the loaded fence module's literal (65536) before any verdict.

Fixture `d` used by every row (`work/build/f000`, `fid=n18-shallow-fetch`, `argv=["--lane","repo"]`,
`tool=anchor`) holds two plain-init stores (`src/`, `repo/`) and, inside `repo/.git`:

```
FETCH_HEAD   68 bytes  da9314e6…dbb1\t\tbranch 'master' of ../src\n
shallow      41 bytes  da9314e6…dbb1\n
refs/remotes/origin/master, logs/refs/remotes/origin/master   (written by `git fetch`)
```

## Result A — the candidate does not admit this class at all

Frozen counter on the candidate (`--skip-mutants`, clean tree):

```
FENCE …/fence_a.py sha256=b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=121 refused=5 error=0
HONEST-REFUSED n17-replace-ref repo/.git/refs/replace is not a ref namespace git writes
HONEST-REFUSED n18-shallow-fetch repo/.git/FETCH_HEAD is not a plain-init entry
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d …/lane/.git/objects/info/alternates is not a plain-object-info entry (object-store redirect)
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

So `FETCH_HEAD` (and `shallow`) are simply not in the candidate's `GIT_TOP` allowlist
(`GIT_TOP = {HEAD, ORIG_HEAD, COMMIT_EDITMSG, config, description, hooks, index, info, logs, objects, refs,
packed-refs}`): the r49 candidate never closed this leg. The base fence's number is the frozen control and
reproduces exactly: `HONEST fixtures=126 admitted=113 refused=13`.

A **second** measured over-refusal sits behind the first: once `FETCH_HEAD`/`shallow` are named, the same
honest fixture is still refused because `git fetch` also writes the remote-tracking ref and its reflog
(`repo/.git/logs/refs/remotes has a name git does not write` — `+names` column below). The candidate's
`REF_NAMESPACES`/`_log_name_ok` admit only `heads|tags|notes`, and its docstring states `refs/remotes` is
refused on purpose ("a clone is not a plain-init state") — but `git fetch` from a sibling-relative remote inside
`d` writes exactly that, so the stated theory is too narrow for the class it must admit. Admitting `n18` needs
both shapes; FETCH_HEAD alone is not sufficient (measured, column 5).

## Result B — the repair payload (candidate → repaired)

Applied to a scratch copy of the candidate; this is the whole deliverable, no other line changes:

```diff
--- a/plans/fixture_fence.py
+++ b/plans/fixture_fence.py
@@ -101,9 +101,10 @@
 REF_PATH = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._/-]*\Z", re.ASCII)
 
 GIT_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index", "info",
-           "logs", "objects", "refs", "packed-refs"}
+           "logs", "objects", "refs", "packed-refs",
+           "FETCH_HEAD", "shallow"}     # round-50: `git fetch` writes both; names only, never opened
 GIT_DIRS = {"hooks", "info", "logs", "objects", "refs"}
-REF_NAMESPACES = ("heads", "tags", "notes")     # directories under `refs/` git writes
+REF_NAMESPACES = ("heads", "tags", "notes", "remotes")  # directories under `refs/` git writes (`fetch`)
 CFG_SECTIONS = {"core", "user", "init"}
 CFG_SUB_SECTIONS = {"remote", "branch"}         # inert declarations: URLs and refspecs, no reads
 CFG_KEYS = {
@@ -571,7 +572,7 @@
     """A reflog lives at `HEAD`, at `refs/stash`, or under git's ref namespaces with git's own name shape."""
     if rel in ("HEAD", "refs/stash"):
         return True
-    m = re.fullmatch(r"refs/(?:heads|tags|notes)/(.+)", rel, re.ASCII)
+    m = re.fullmatch(r"refs/(?:heads|tags|notes|remotes)/(.+)", rel, re.ASCII)
     if not m:
         return False
     return all(SAFE_NAME.match(part) for part in m.group(1).split("/"))
@@ -591,7 +592,7 @@
         if _linked(mode, n):
             return f"{_rel(q, label)} has more than one hard link"
         if stat.S_ISDIR(mode):
-            if not (rel in ("refs", "refs/heads", "refs/tags", "refs/notes")
+            if not (rel in ("refs", "refs/heads", "refs/tags", "refs/notes", "refs/remotes")
                     or (_log_name_ok(rel) and rel != "refs/stash")):
                 return f"{_rel(q, label)} has a name git does not write"
             why = _logs(q, label, ddev, rel + "/")
@@ -721,6 +722,11 @@
         elif name == "COMMIT_EDITMSG":
             if size > TEXT_CAP:
                 return f"{label}/COMMIT_EDITMSG exceeds {TEXT_CAP} bytes"
+        elif name in ("FETCH_HEAD", "shallow"):
+            # Admitted by name and bounded size only: the fence never opens either file, so their bytes cannot
+            # redirect a read. Indirection is already excluded above (symlink, special file, hard link, device).
+            if size > TEXT_CAP:
+                return f"{label}/{name} exceeds {TEXT_CAP} bytes"
         elif name == "config":
             why = _config(q, label)
             if why:
```

Note the shape of the FETCH_HEAD rule: **name + `lstat` shape + size only**. Every indirection the admission
could hide is already refused for *all* store entries before the name dispatch runs (`stat.S_ISLNK` → symlink,
`dev != ddev` → mount boundary, `not S_ISREG` → special file, `_linked(...)` → >1 hard link), so the only new
decision the repair makes is "this name, under the text cap, is a regular single-link file on `d`'s device".

## Result C — case table (17 cases, three fences, same built bytes)

`python3 "$S/cases_fetch_head.py" "$S/lane" "$S/work" <repaired> <names-only> <candidate>`
Exit 0; the repaired fence matches its expectation on all 17 rows. "candidate" = `fence_a.py`,
"+names" = FETCH_HEAD/shallow only, "+names+remotes" = the repair above.

| # | case | expect | candidate | +names | +names+remotes | reason (repaired fence) |
|---|---|---|---|---|---|---|
| 1 | `honest-as-built` | ADMIT | BREACH | BREACH | **ADMIT** | — |
| 2 | `fetch-head-absent` | ADMIT | BREACH | BREACH | **ADMIT** | — |
| 3 | `fetch-head-small-clean` | ADMIT | BREACH | BREACH | **ADMIT** | — |
| 4 | `fetch-head-at-cap` (65536 B) | ADMIT | BREACH | BREACH | **ADMIT** | — |
| 5 | `fetch-head-oversize` (65537 B) | BREACH | BREACH | BREACH | **BREACH** | `repo/.git/FETCH_HEAD exceeds 65536 bytes` |
| 6 | `fetch-head-symlink-outside` | BREACH | BREACH | BREACH | **BREACH** | `repo/.git/FETCH_HEAD is a symlink` |
| 7 | `fetch-head-symlink-inside` | BREACH | BREACH | BREACH | **BREACH** | `repo/.git/FETCH_HEAD is a symlink` |
| 8 | `fetch-head-directory` | BREACH | BREACH | BREACH | **BREACH** | `repo/.git/FETCH_HEAD is not a regular file` |
| 9 | `fetch-head-fifo` | BREACH | BREACH | BREACH | **BREACH** | `repo/.git/FETCH_HEAD is not a regular file` |
| 10 | `fetch-head-hardlink-outside` | BREACH | BREACH | BREACH | **BREACH** | `repo/.git/FETCH_HEAD has more than one hard link` |
| 11 | `shallow-oversize` | BREACH | BREACH | BREACH | **BREACH** | `repo/.git/shallow exceeds 65536 bytes` |
| 12 | `shallow-symlink-outside` | BREACH | BREACH | BREACH | **BREACH** | `repo/.git/shallow is a symlink` |
| 13 | `remote-ref-symbolic` | BREACH | BREACH | BREACH | **BREACH** | `…/refs/remotes/origin/master is not a 40-hex ref` |
| 14 | `remote-ref-bad-name` | BREACH | BREACH | BREACH | **BREACH** | `…/refs/remotes/origin/-bad has a name git does not write` |
| 15 | `remote-log-symlink-outside` | BREACH | BREACH | BREACH | **BREACH** | `…/logs/refs/remotes/origin/master is a symlink` |
| 16 | `fetch-head-redirect-content` (`gitdir: /etc`) | ADMIT | BREACH | BREACH | **ADMIT** | — |
| 17 | `fetch-head-host-path-column` (`…\t\t/etc/shadow`) | ADMIT | BREACH | BREACH | **ADMIT** | — |

Row-by-row: the three requirements of the item are rows 1 (admitted), 6 (symlink outside `d` refused), 5
(oversize refused); row 4 fixes the boundary (`>` the cap, not `>=`). Rows 7–10 and 11–12 show the refusal is
the *store-entry shape* rule, not a name special-case: a symlink is refused even when it points inside `d`, and a
FIFO, a directory and a hard link all fall to the same generic rules. Rows 13–15 close the widening I had to add
for the class (a symbolic ref inside `refs/remotes`, a component name git does not write, a reflog symlink
pointing outside `d`).

## Result D — "admitting the file does not admit a read", measured

One line: **the fence classifies `FETCH_HEAD` by name, `lstat` shape and size only — it never opens it (there is
no `_read` call on it anywhere in the module), so its bytes cannot name a path, and a path that is never opened
cannot redirect a read.**

Static: the only two occurrences of the name in the repaired module are the `GIT_TOP` member and the size
branch (`grep -n 'FETCH_HEAD\|shallow'` → lines 105 and 725).

Dynamic: the driver installs `sys.addaudithook` and records every `open`/`os.open` event during each `breach()`,
filtering by basename (`FETCH_HEAD`, or `shallow` under a `.git/`). Every FETCH_HEAD/shallow case (1–12, 16, 17)
records **`opened_store_text_entries=[]`**, including the two `ADMIT` rows whose content is deliberately hostile
(`gitdir: /etc`, a 40-hex + `/etc/shadow` column): admitting them adds no open. The complete open list for
`honest-as-built` is the classification set only — the two stores' `HEAD`, `config`, `refs/heads/master`,
`refs/remotes/origin/master` — and never `FETCH_HEAD` or `shallow`:

```
…/cases/honest-as-built/repo/.git/HEAD
…/cases/honest-as-built/repo/.git/config
…/cases/honest-as-built/repo/.git/refs/heads/master
…/cases/honest-as-built/repo/.git/refs/remotes/origin/master
…/cases/honest-as-built/src/.git/HEAD
…/cases/honest-as-built/src/.git/config
…/cases/honest-as-built/src/.git/refs/heads/master
```

## Result E — no regression, measured on identical built bytes

`dump_vectors.py` builds all 44 population modules (126 fixtures, `build_errors=0`), `plans/refusals46` (20
modules / 34 fixtures) and `plans/sealed46` (12 modules / 15 fixtures) **once**, then evaluates both fences on the
same trees. Verdict-vector delta, candidate → repaired:

```
refused_honest: candidate ['n17-replace-ref','n18-shallow-fetch','n20-linked-worktree','n21-separate-gitdir','n22-alternates-in-d']
                repaired  ['n17-replace-ref',              'n20-linked-worktree','n21-separate-gitdir','n22-alternates-in-d']
plans/refusals46  fixtures 34  non-breach 0  (both fences)
plans/sealed46    fixtures 15  non-breach 0  (both fences)
```

Exactly one vector entry changes — `n18-shallow-fetch: BREACH → ADMIT` — and every hostile fixture keeps its
`BREACH`, with identical reasons. Frozen counter on the repaired fence:

```
REV 5c56819f7964f4af19c960de08a49cd8f95781ce
TREE dirty=0
FENCE …/fence_fetch_head.py sha256=80875a1422ff8d6ddf8d0329fb5e7692b9081945e7523653c615c38c2f7856e5
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=122 refused=4 error=0
HONEST-REFUSED n17-replace-ref repo/.git/refs/replace is not a ref namespace git writes
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d …/alternates is not a plain object-info entry (object-store redirect)
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

`PREDICATE … fail` is expected and is **not** this seat's claim: four honest classes (`n17`, `n20`, `n21`,
`n22`) still need their own S2 legs, and `plans/sealed50/` does not exist yet at REV. This seat claims only the
`n18` delta and the unchanged hostile legs — it does not claim R50-C1 admission.

## Result F — integration risk measured (not repaired here)

The carried r49 battery `plans/mutants50/c1-mutants.json` (23 inline diffs, `candidate_fence_sha256=b687b1d9…`)
does not survive a fence carrying this repair unchanged: applying each payload with
`patch --batch --silent -p1` to the repaired fence, **21 apply, 2 fail** — `c1-mut-05-git-top-commondir` (its
`GIT_TOP` hunk context changed) and `c1-mut-21-log-namespace` (its `_log_name_ok`/namespace hunk context
changed). Any S2 fence including this repair must re-derive those two rows (and re-witness every row's kill
direction on the S2 fence per QUALITY Q38) before the mutant leg can pass. Cheapest shape: keep the battery
keyed to the S2 fence digest rather than to the r49 candidate, and author the two rows against the new context.

## Named limits

- The read-freedom measurement is a Python `sys.addaudithook` trace of `open`/`os.open`, not `strace`; it proves
  the decision performs no open of these two names, not that no lower-level syscall mentions the path.
- `FETCH_HEAD`/`shallow` are admitted by name and size only; their **content is not validated**. A fixture whose
  `FETCH_HEAD` holds a host path or a `gitdir:` line is admitted (rows 16–17). That is sound under this fence's
  advertised property (it never opens the file, and the tool behind it never resolves a path from it), and it
  would stop being sound the moment a consumer opened the file to resolve anything from it.
- `TEXT_CAP` is a resource bound, not a shape check: a legitimate `.git/shallow` listing more than ~1600
  boundary commits (65536 bytes / 41 bytes per line) would be over-refused. Not observed in this population.
- The repair widens `refs/remotes` and `logs/refs/remotes` for *every* fixture, not only shallow ones. The
  namespace is closed to the same redirect shapes as `heads|tags|notes` (non-40-hex content, symbolic refs,
  names git does not write, symlinks/hard links/mount boundaries — rows 13–15 plus the unchanged
  `plans/refusals46`/`plans/sealed46` legs). A clone fetched from a **host path** remote would still be refused
  through `.git/config` (`[remote] url` must be a relative, in-`d` value), which is the intended boundary.
- `/tmp` was not used; all builds lived under `$S` on `/fast` and were removed before this report was finalised
  (see bottom). No pacman/uv/npm installs were needed or made; no production file was touched.

## Files

- report: this file (only lane write).
- scratch (candidate code, removed before yield): `cases_fetch_head.py`, `dump_vectors.py`,
  `fence_fetch_head.py`, `fence_fetch_head_only.py`, `repair.diff`, `vs-case receipts`.

## VERDICT

**PASS (scoped).** The `.git/FETCH_HEAD` leg is proven as a recipe, not as a landed state: the r49 candidate
(`b687b1d9…`) does **not** admit `n18-shallow-fetch` (`HONEST … admitted=121 refused=5`, refused at
`repo/.git/FETCH_HEAD is not a plain-init entry`), so this leg of S2 is still open. A five-hunk repair
(`80875a14…`, payload above) closes it: `n18` admitted, symlink-outside/oversize/shape cases refused, no
`open()` of either name, verdict vector delta exactly `{n18}`, `REFUSALS 20/20` and `SEALED 12/12` unchanged,
`HONEST 122/4` with the remaining four refusals belonging to other legs. Blockers for integration: the class
needs the `refs/remotes` namespace in the same commit (names-only patch still refuses it, measured), and 2 of the
23 r49 mutant payloads lose their hunk context against this repair and must be re-derived. Scratch tree removed;
no scratch left on disk.
