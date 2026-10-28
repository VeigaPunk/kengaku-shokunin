# R50C1ExecRefs — R50-C1 ref-namespace leg (executor seat)

    REV       3b02d573d58cc6d2e0d27ef92ac0815354912252   (measured: the stage-1 freeze)
    LANE TIP  5c56819f7964f4af19c960de08a49cd8f95781ce   (freeze is an ancestor: verified below)
    FENCE     plans/fixture_fence.py sha256 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
    CLAIM     R50-C1 (novelty). This seat does NOT admit the claim; it supplies one leg's case table.

All measurement ran against `git clone --shared` of the lane at the freeze commit, in
`/fast/scratch/hyaku/kengaku-r50/R50C1ExecRefs` (scratch, removed before yielding). Nothing in the lane
was written, committed, checked out or mutated; no `pacman`, no global git env vars.

## Axes named (godspeed)

- **A1 honest admission** — a documented `refs/replace/<40hex>` store (loose and packed) is admitted.
- **A2 escape refusal** — `refs/replace/<non-hex>`, `refs/replace/../` (textual and symlink forms), nested
  replace dirs, lock files, non-40-hex content and `logs/refs/replace` are refused, each with a reason naming
  the offending path.
- **A3 representation parity** — the same ref name gets the same verdict whether it is loose or in
  `packed-refs` (the base fence is *not* parity-safe: see F2).
- **A4 non-perturbation** — `refs/notes/*` and `refs/stash` verdicts are identical with and without the
  refs/replace leg (cand-A vs cand-B), and their hostile variants stay refused.
- **A5 containment preserved** — the 20 frozen refusal modules and the 12 sealed modules stay refused with the
  widened ref namespaces (no leak).

## "The candidate" — what was measured, and why this definition

At the freeze commit no repaired fence exists in the lane: `plans/fixture_fence.py` is still the base fence
`05d5fe03…` and `plans/mutants50/c1-mutants.json` only names a *candidate digest*
`b687b1d9…` for a fence that is not in the tree. So "the candidate" here is the scratch ref-namespace repair
derived in this seat, digest `f8b12573d580857541dc17465a27e86792175f933641ef720420522665a956cd`, produced
from the base fence by the five explicit substitutions in §"Candidate". The S2 repair seat must either adopt
this diff or re-derive an equivalent; either way **this 37-case table is the acceptance test for the leg**, and
it is run by `cases.py` against any fence path.

Two candidate steps are measured separately so "unchanged" is a measurement, not a claim:

- **cand-A** = base + the notes/stash repair only (digest `a6b304e748fb359e2a37df6e4bf880f9a2ebf25a434e57d48d2c1827a9ab8e8a`);
  refs/replace still refused.
- **cand-B** = cand-A + the refs/replace leg (digest `f8b12573…`), i.e. the candidate proper.

## Exact commands run

```sh
# 1. ancestry + lane state (read-only; live checkout, no write)
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
git rev-parse HEAD                                     # 5c56819f7964f4af19c960de08a49cd8f95781ce
git merge-base --is-ancestor 3b02d573d5… 5c56819f79…   # rc 0  => FREEZE_IS_ANCESTOR
git diff --stat 3b02d573d5… 5c56819f79… -- plans/fixture_fence.py plans/honest50 \
    plans/round50_c1_verify.py plans/mutants50 plans/sealed50    # empty: no instrument change after freeze

# 2. clean clone at the freeze commit
S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecRefs
git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout --quiet 3b02d573d58cc6d2e0d27ef92ac0815354912252
git -C "$S/lane" rev-parse HEAD          # 3b02d573d58cc6d2e0d27ef92ac0815354912252
git -C "$S/lane" rev-parse --show-toplevel   # /fast/scratch/.../lane
sha256sum "$S/lane"/plans/{fixture_fence.py,round50_c1_verify.py}   # 05d5fe03… / f9b9873e…
sha256sum "$S/lane"/plans/honest50/population.txt                   # b5197f94…

# 3. base fence on the frozen 126-fixture population
cd "$S/lane" && TMPDIR="$S" python3 plans/round50_c1_verify.py --lane . --skip-mutants --work "$S/c1work"

# 4. full refused list (same legs, no [:12] truncation)
cd "$S/lane" && TMPDIR="$S" python3 - <<'PY'
import importlib.util, pathlib, tempfile
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m
lane = pathlib.Path('.').resolve()
c   = load(lane/'plans/round50_c1_verify.py', 'c')
hb  = load(lane/'plans/honest50/build_honest_population.py', 'hb'); hb.ALLOW_NO_REPO = True
k44 = load(lane/'plans/round44_c1_verify.py', 'k44')
rows = c.parse_population(lane/'plans/honest50/population.txt')
mods, seen = [], set()
for r in rows:
    if r['module'] in seen: continue
    seen.add(r['module']); mods.append((lane/r['module'], r['module'].replace('/','-')[:-3]))
work = pathlib.Path(tempfile.mkdtemp(prefix='allref-', dir='/fast/scratch/hyaku/kengaku-r50/R50C1ExecRefs'))
honest, fail = c.build_all(hb, k44, mods, work/'h')
fence = load(lane/'plans/fixture_fence.py', 'f')
v = c.verdicts(fence, honest)
ref = [x for x in v if x['v'] != 'ADMIT']
print(f"total={len(v)} admitted={len(v)-len(ref)} refused={len(ref)}")
for x in ref: print(f"{x['fid']}\t{x['v']}\t{x['why']}")
PY

# 5. candidate generation + case table
cd "$S" && python3 make_candidate.py lane/plans/fixture_fence.py "$S/candidate_fence.py"
cd "$S" && python3 make_cand_a.py  candidate_fence.py candA_fence.py
cd "$S" && S="$S" TMPDIR="$S" python3 cases.py

# 6. the frozen counter against the candidate, both legs present
cd "$S/lane" && TMPDIR="$S" python3 plans/round50_c1_verify.py --lane . \
    --fence "$S/candidate_fence.py" --skip-mutants --work "$S/c1work"
```

The mutant leg is omitted (`--skip-mutants`) exactly as the seat item directs: it scores the *fence under test*
against the carried r49 battery whose kill directions are not yet witnessed (Q38), and it is a property of the
S2 battery, not of this leg. Tools installed: **none** (nothing was needed; no pacman transaction attempted).

## Base fence on the frozen population (verbatim, `base-leg.txt`)

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1ExecRefs/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../../c1work/k50-c1-369hv_oc/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph present (object-store redirect)
HONEST-REFUSED n16-notes-ref ../../../../c1work/k50-c1-369hv_oc/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
HONEST-REFUSED n17-replace-ref repo/.git/refs/replace is not refs/heads or refs/tags
HONEST-REFUSED n18-shallow-fetch repo/.git/FETCH_HEAD is not a plain-init entry
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d lane/.git/objects/info/alternates present (object-store redirect)
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

The counter prints only `refused[:12]`; the untruncated run (`all-refused`) prints the 13th row:

```
n08-tag-detached	BREACH	repo/.git/HEAD is not a plain branch HEAD
```

**Measured refused classes (13 fixtures, 13 classes):** `n03-detached-head`, `n07-reflog-gc`,
`n08-tag-detached`, `n12-local-config-user`, `n13-remote-origin`, `n14-stash-entry`, `n15-commit-graph`,
`n16-notes-ref`, `n17-replace-ref`, `n18-shallow-fetch`, `n20-linked-worktree`, `n21-separate-gitdir`,
`n22-alternates-in-d`.

## Candidate (cand-B) — exact diff against the frozen base fence

Resulting fence sha256 `f8b12573d580857541dc17465a27e86792175f933641ef720420522665a956cd`.
Apply with `patch -p1` after renaming the target, or transcribe; the five substitutions are exactly these.

**Self-check (run after this report was written):** the diff block below was extracted from this file, applied
with `patch --batch -p0` to `plans/fixture_fence.py` @ `05d5fe03…`, and produced
`f8b12573d580857541dc17465a27e86792175f933641ef720420522665a956cd` (patch rc 0) — the block is
transcription-exact, not a paraphrase.

```diff
--- plans/fixture_fence.py@base
+++ candidate_fence.py
@@ -275,6 +275,32 @@
     return None
 
 
+REF_NAMESPACES = ("heads", "tags", "notes", "replace")   # ref namespaces git writes inside the store
+HEX40_NAME = re.compile(r"\A[0-9a-f]{40}\Z", re.ASCII)
+
+
+def _ref_ns_ok(ns, name):
+    """A ref name inside one admitted namespace. `replace` is one flat level of 40-hex object ids."""
+    if not _ref_name_ok(name):
+        return False
+    if ns == "replace":
+        return HEX40_NAME.match(name) is not None
+    return True
+
+
+def _packed_name_ok(name):
+    """A packed ref name, namespace-checked like its loose twin (`refs/stash` is one file ref)."""
+    if name == "refs/stash":
+        return True
+    m = re.fullmatch(r"refs/replace/([0-9a-f]{40})", name, re.ASCII)
+    if m:
+        return True
+    m = re.fullmatch(r"refs/(?:heads|tags|notes)/(.+)", name, re.ASCII)
+    if not m:
+        return False
+    return _ref_name_ok(m.group(1))
+
+
 def _refs(p, label):
     ents = _entries(p)
     if ents is None:
@@ -285,17 +311,24 @@
             return f"{_rel(q, label)} is a symlink"
         if _linked(mode, _n):
             return f"{_rel(q, label)} has more than one hard link"
-        if name not in ("heads", "tags"):
-            return f"{label}/{name} is not refs/heads or refs/tags"
+        if name == "stash":
+            if not stat.S_ISREG(mode):
+                return f"{label}/stash is not a regular file"
+            body = _read(q, 200)
+            if body is None or HEX40.match(body) is None:
+                return f"{label}/stash is not a 40-hex ref"
+            continue
+        if name not in REF_NAMESPACES:
+            return f"{label}/{name} is not a ref namespace git writes"
         if not stat.S_ISDIR(mode):
             return f"{label}/{name} is not a directory"
-        why = _ref_tree(q, label)
+        why = _ref_tree(q, label, name)
         if why:
             return why
     return None
 
 
-def _ref_tree(p, label):
+def _ref_tree(p, label, ns=None):
     ents = _entries(p)
     if ents is None:
         return f"{_rel(p, label)} unreadable"
@@ -306,15 +339,17 @@
         if _linked(mode, _n):
             return f"{_rel(q, label)} has more than one hard link"
         if stat.S_ISDIR(mode):
-            if not _ref_name_ok(name):
+            if ns == "replace":
+                return f"{_rel(q, label)} is nested below refs/replace (replace refs are flat)"
+            if not _ref_ns_ok(ns, name):
                 return f"{_rel(q, label)} has a name git does not write"
-            why = _ref_tree(q, label)
+            why = _ref_tree(q, label, ns)
             if why:
                 return why
             continue
         if not stat.S_ISREG(mode):
             return f"{_rel(q, label)} is a special file"
-        if not _ref_name_ok(name):
+        if not _ref_ns_ok(ns, name):
             return f"{_rel(q, label)} has a name git does not write"
         body = _read(q, 200)
         if body is None:
@@ -370,10 +405,14 @@
 
 
 def _log_name_ok(rel):
-    """A reflog lives at `HEAD` or under `refs/heads|refs/tags` with git's own name shape."""
-    if rel == "HEAD":
+    """A reflog lives at `HEAD`, `refs/stash`, or under `refs/heads|tags|notes` with git's name shape.
+
+    `refs/replace` is deliberately absent: measured on git 2.56.0, `git replace <obj> <repl>` writes
+    `refs/replace/<40hex>` and no `logs/refs/replace/*`, so a replace reflog is not a state git writes.
+    """
+    if rel in ("HEAD", "refs/stash"):
         return True
-    m = re.fullmatch(r"refs/(?:heads|tags)/(.+)", rel, re.ASCII)
+    m = re.fullmatch(r"refs/(?:heads|tags|notes)/(.+)", rel, re.ASCII)
     if not m:
         return False
     return all(SAFE_NAME.match(part) for part in m.group(1).split("/"))
@@ -391,7 +430,7 @@
         if _linked(mode, n):
             return f"{_rel(q, label)} has more than one hard link"
         if stat.S_ISDIR(mode):
-            if not (rel in ("refs", "refs/heads", "refs/tags") or _log_name_ok(rel)):
+            if not (rel in ("refs", "refs/heads", "refs/tags", "refs/notes") or _log_name_ok(rel)):
                 return f"{_rel(q, label)} has a name git does not write"
             why = _logs(q, label, rel + "/")
             if why:
@@ -445,7 +484,7 @@
             name = ref.decode("ascii")
         except UnicodeDecodeError:
             return f"{label} carries a non-ASCII ref name"
-        if not _ref_name_ok(name):
+        if not _packed_name_ok(name):
             return f"{label} carries a ref name git does not write"
     return None
```

**cand-A** is cand-B minus the replace leg: `REF_NAMESPACES = ("heads","tags","notes")`,
`_ref_ns_ok` reduces to `return _ref_name_ok(name)`, and the `refs/replace/([0-9a-f]{40})` branch is removed
from `_packed_name_ok`. Digest `a6b304e7…`. It exists only to measure A4.

Design note on the two shapes the item names: **`refs/replace` as a DIRECTORY** is walked as a flat namespace
(each child must be exactly 40 lowercase hex, value 40-hex); **`refs/replace` as a FILE** is refused with the
distinct reason `is not a directory`, has no crash path, and is never reinterpreted as a stored ref —
`git replace` writes `refs/replace/<40hex>`, never `refs/replace` itself (measured).

## Case table (37 cases; every fixture built by the frozen population builder, one mutation each)

`cases.py` builds the authentic fixtures with `plans/honest50/build_honest_population.py` (`build_once`) and
mutates a *copy* with the builder's own `Ctx` (fixed dates, `HOME=/nonexistent`, `GIT_CONFIG_NOSYSTEM=1`, no
global config), so no host config can leak into a fixture. Host reflog/rerere state was caught this way: a
`git stash` run under the host's global config created `.git/rr-cache` (a state the base fence refuses), which
the ctx-driven build does not. Every git call asserted `rev-parse --show-toplevel` == the fixture dir.

| # | case | expect | base | cand-A (notes/stash) | cand-B (all) | cand-B reason |
|---|---|---|---|---|---|---|
| 0 | R1 replace/<40hex> loose (git replace) | ADMIT | REFUSE | REFUSE | ADMIT | `-` |
| 1 | R2 replace/<40hex> packed (pack-refs) | ADMIT | REFUSE | REFUSE | ADMIT | `-` |
| 2 | R3 replace/<non-hex> loose name | REFUSE | REFUSE | REFUSE | REFUSE | `02/repo/.git/refs/replace/not-a-40-hex-name has a name git does not write` |
| 3 | R4 replace/<short-hex> loose name | REFUSE | REFUSE | REFUSE | REFUSE | `03/repo/.git/refs/replace/abc123 has a name git does not write` |
| 4 | R5 replace/..x loose name | REFUSE | REFUSE | REFUSE | REFUSE | `04/repo/.git/refs/replace/..x has a name git does not write` |
| 5 | R6 replace/<40hex>.lock present | REFUSE | REFUSE | REFUSE | REFUSE | `05/repo/.git/refs/replace/4d88795d2b61cd3050f970240b8628e8b6313c90.lock has a name git does not write` |
| 6 | R7 replace/<40hex> non-hex content | REFUSE | REFUSE | REFUSE | REFUSE | `06/repo/.git/refs/replace/4d88795d2b61cd3050f970240b8628e8b6313c90 is not a 40-hex ref` |
| 7 | R8 replace nested dir under replace/ | REFUSE | REFUSE | REFUSE | REFUSE | `07/repo/.git/refs/replace/sub is nested below refs/replace (replace refs are flat)` |
| 8 | R9 packed refs/replace/../../../escape | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git carries a ref name git does not write` |
| 9 | R10 packed refs/replace/../heads/master | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git carries a ref name git does not write` |
| 10 | R11 refs/replace as SYMLINK to outside | REFUSE | REFUSE | REFUSE | REFUSE | `10/repo/.git/refs/replace is a symlink` |
| 11 | R12 refs/replace/<40hex> as SYMLINK | REFUSE | REFUSE | REFUSE | REFUSE | `11/repo/.git/refs/replace/4d88795d2b61cd3050f970240b8628e8b6313c90 is a symlink` |
| 12 | R13 refs/replace as FILE (40-hex) | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git/refs/replace is not a directory` |
| 13 | R14 refs/replace as FILE (garbage) | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git/refs/replace is not a directory` |
| 14 | R15 refs/replace empty DIRECTORY | ADMIT | REFUSE | REFUSE | ADMIT | `-` |
| 15 | R16 packed refs/replace/<40hex> only | ADMIT | REFUSE | REFUSE | ADMIT | `-` |
| 16 | R17 logs/refs/replace/<40hex> reflog | REFUSE | REFUSE | REFUSE | REFUSE | `16/repo/.git/logs/refs/replace has a name git does not write` |
| 17 | N1 refs/notes/commits loose (git notes) | ADMIT | REFUSE | ADMIT | ADMIT | `-` |
| 18 | N2 refs/notes/deep/name nested | ADMIT | REFUSE | ADMIT | ADMIT | `-` |
| 19 | N3 refs/notes/commits packed | ADMIT | REFUSE | ADMIT | ADMIT | `-` |
| 20 | N4 refs/notes/commits non-hex content | REFUSE | REFUSE | REFUSE | REFUSE | `20/repo/.git/refs/notes/commits is not a 40-hex ref` |
| 21 | N5 refs/notes/commits as SYMLINK | REFUSE | REFUSE | REFUSE | REFUSE | `21/repo/.git/refs/notes/commits is a symlink` |
| 22 | S1 refs/stash loose (git stash) | ADMIT | REFUSE | ADMIT | ADMIT | `-` |
| 23 | S2 refs/stash packed | ADMIT | REFUSE | ADMIT | ADMIT | `-` |
| 24 | S3 refs/stash non-hex content | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git/refs/stash is not a 40-hex ref` |
| 25 | S4 refs/stash as DIRECTORY | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git/refs/stash is not a regular file` |
| 26 | C1 plain repo control (n19) | ADMIT | ADMIT | ADMIT | ADMIT | `-` |
| 27 | C2 notes + replace in one repo | ADMIT | REFUSE | REFUSE | ADMIT | `-` |
| 28 | C3 stash + replace in one repo | ADMIT | REFUSE | REFUSE | ADMIT | `-` |
| 29 | P1 packed refs/replace/abc123 (n19) | REFUSE | **ADMIT** | REFUSE | REFUSE | `repo/.git carries a ref name git does not write` |
| 30 | P2 packed refs/replace/<40hex> (n19) | ADMIT | ADMIT | REFUSE | ADMIT | `-` |
| 31 | P3 packed refs/stash (n19) | ADMIT | ADMIT | ADMIT | ADMIT | `-` |
| 32 | P4 packed refs/notes/commits (n19) | ADMIT | ADMIT | ADMIT | ADMIT | `-` |
| 33 | P5 packed refs/notes/../heads/master | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git carries a ref name git does not write` |
| 34 | P6 packed refs/stashx (n19) | REFUSE | **ADMIT** | REFUSE | REFUSE | `repo/.git carries a ref name git does not write` |
| 35 | W1 refs/bisect/bad (namespace git hides) | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git/refs/bisect is not a ref namespace git writes` |
| 36 | W2 refs/worktree/x (namespace git hides) | REFUSE | REFUSE | REFUSE | REFUSE | `repo/.git/refs/worktree is not a ref namespace git writes` |

```
CASES total=37 candidate_matches_expect=37 mismatched=0
```

**A4 is measured, not argued:** `N1 N2 N3 S1 S2 P3 P4` are `ADMIT` in cand-A and **identical** in cand-B; the
only cells that move from cand-A to cand-B are the replace cases (`R1 R2 R15 R16 C2 C3 P2`), each `REFUSE →
ADMIT`. Every `REFUSE` cell for notes/stash content variants (`N4 N5 S3 S4 P5`) stays `REFUSE` in all three
fences. So adding the refs/replace leg changes nothing about `refs/notes/*` or `refs/stash` — and "unchanged"
cannot mean "still refused", because `n14`/`n16` are population rows and `HONEST admitted=126` requires them
admitted (measured below: they are two of the base's 13 refusals).

## The frozen counter against the candidate (both non-mutant legs)

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1ExecRefs/candidate_fence.py sha256=f8b12573d580857541dc17465a27e86792175f933641ef720420522665a956cd
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=116 refused=10 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph present (object-store redirect)
HONEST-REFUSED n18-shallow-fetch repo/.git/FETCH_HEAD is not a plain-init entry
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d lane/.git/objects/info/alternates present (object-store redirect)
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
HONEST-REFUSED n08-tag-detached repo/.git/HEAD is not a plain branch HEAD
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

`PREDICATE fail` is expected and correct: this is one leg, not the claim. What matters for A5 is
`REFUSALS 20/20 leaked=0` and `SEALED 12/12 leaked=0` — widening the ref namespaces leaks no hostile module.

## Findings

**F1 (routing defect the L1 must reconcile). The seat spec's refusal census is wrong.** The spec says the base
fence refuses "the five honest classes" `n17, n18, n20, n21, n22`. Measured at the freeze on the frozen
population: **13 fixtures in 13 classes** are refused — `n03`, `n07`, `n08`, `n12`, `n13`, `n14`, `n15`,
`n16`, `n17`, `n18`, `n20`, `n21`, `n22`. The claims file's own `Before` line (`refused=13`) is right; only the
class list in the dispatch item is wrong. Consequence for S2: the ref leg alone moves
`admitted 113 → 116`; ten refusals remain in other legs (config allowlist `n12/n13`, `objects/info`
`n15`, `FETCH_HEAD` `n18`, gitfile stores `n20/n21`, alternates `n22`, detached/tag `n03/n08`,
`info/refs` `n07`). Those are other seats' legs; this seat did not touch them.

**F2. The base fence's ref policy is representation-dependent (a genuine instrument gap).** `_packed()` validates
packed ref names with `_ref_name_ok` only, which accepts *any* well-formed ref path. Measured on a log-free
control (n19), the base fence **admits** `packed-refs` lines `refs/replace/abc123` (P1) and `refs/stashx` (P6),
and admits packed `refs/replace/<40hex>`, `refs/stash`, `refs/notes/commits` (P2/P3/P4) — while refusing the
same names when loose. A fence whose verdict depends on loose-vs-packed storage cannot claim "admit only the
shape git writes". cand-B makes the two representations agree; this is the strongest novelty datum of the leg.

**F3. The notes/stash repair must include the reflog leg, or it silently does nothing.** The base fence refuses
`n14`/`n16` at `_logs` first (`logs/refs/stash`, `logs/refs/notes has a name git does not write`), before
`_refs` is ever reached. A repair that widens `refs/` only still refuses both fixtures. cand-A/cand-B widen
`_log_name_ok` and the `_logs` directory allowlist in the same substitution.

**F4. `refs/replace` has no reflog — measured, so it stays refused.** `git replace <obj> <repl>` on git 2.56.0
writes `refs/replace/<40hex>` and no `logs/refs/replace/*` (n17's built tree, and the isolated probe). Case R17
therefore refuses `logs/refs/replace/<40hex>`; it is a decided exclusion, not an unknown.

**F5. `git replace -d` leaves an empty `.git/refs/replace` directory**, so an empty `refs/replace` dir is a
git-written state. R15 admits it, consistent with the base fence's treatment of an empty `refs/heads`.

**F6. `refs/replace` as a FILE cannot occur in a git-written store**, and the candidate refuses it with a
distinct reason (`is not a directory`) for both 40-hex (R13) and garbage (R14) contents — no crash, no silent
admission, no reinterpretation as a stored ref. This is the "DIRECTORY vs FILE both handled" requirement,
answered as *directory = flat 40-hex namespace walk, file = refused by shape*.

**F7. `refs/replace/../` exists only in textual form.** On POSIX no directory entry can be named `..`, so the
traversal vectors are (a) `packed-refs` ref names (R9 `refs/replace/../../../escape`, R10
`refs/replace/../heads/master`, P5 `refs/notes/../heads/master`) — all refused by the name-shape check, and
(b) symlinks at or below `refs/replace` (R11, R12) — refused by the tree walk. A loose ref name can also start
with a dot (`..x`, R5) and is refused. The candidate's replace namespace additionally forbids nesting (R8),
so `<40hex>` can only ever be one path component: a name that resolves to an object id, never a path.

**F8. Widening refs leaks nothing.** `REFUSALS 20/20`, `SEALED 12/12` on cand-B. The hidden namespaces
(`refs/bisect`, `refs/worktree`) stay refused (W1, W2): the widening is an enumeration, not a blanket
"any refs/ child".

## Named limits

- Measured at the freeze commit. The lane tip (`5c56819`) contains only the wave spec and untracked evidence
  dirs after the freeze: `git diff --stat 3b02d57..5c56819 -- plans/fixture_fence.py plans/honest50
  plans/round50_c1_verify.py plans/mutants50 plans/sealed50` is empty, so the measured instrument is the tip's
  instrument.
- No candidate fence is committed, so "the candidate" is the scratch artifact above (digest `f8b12573…`);
  the mutant leg was not scored (Q38 witness requirement belongs to S2's battery).
- Object *existence* is not checked (the fence starts no git child by design): `refs/replace/<40hex>` names an
  object id and the fence proves only that it is one flat 40-hex component, never that the object exists.
- Host-dependent: git 2.56.0. The replace/dangling semantics and `pack-refs` behaviour are version-sensitive.
- Not measured here: outside-`d` reads (round-46 counter's property, unchanged), io_uring, host paths outside
  the scratch root, `commondir` (decided exclusion, r50 claims), cross-device hard links.
- Case fixtures are git-built states from the frozen builder; hand-written `packed-refs` lines are used only
  where a git command cannot express the hostile state (P1/P5/P6/R9/R10), and each is labelled as such by the
  case name.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1ExecRefs` (clone, candidates, case harness, receipts) is removed before
yielding; every citable number/artifact is inline above, so nothing depends on scratch or `/tmp` paths.
Process-only digests at measurement time (not citable without the code, which is inline): `candidate_fence.py
f8b12573…`, `candA_fence.py a6b304e7…`, `cases.py 8d2436c0…`, `case-table.json 5a02c66d…`.

## VERDICT

**Leg complete, not an admission.** The ref-namespace leg is proven at the freeze revision with 37/37 cases
matching their declared expectations: `refs/replace/<40hex>` admitted loose *and* packed, `refs/replace`
non-hex / short-hex / `../`-textual / symlink / nested / lock / non-hex-content / reflog all refused with
path-naming reasons, `refs/replace` as a directory walked as a flat 40-hex namespace while a `refs/replace`
file is refused by shape, and `refs/notes/*` + `refs/stash` verdicts bit-identical with and without the
replace leg (cand-A vs cand-B) while both remain admitted because the frozen population requires it. The
candidate is containment-neutral (`REFUSALS 20/20`, `SEALED 12/12`) and lifts `HONEST 113 → 116`; the remaining
10 refusals are other legs (F1). R50-C1 itself is **not** admitted by this report — the predicate needs
`HONEST admitted=126`, the sealed50 floor and a witnessed mutant battery, none of which this seat owns.
