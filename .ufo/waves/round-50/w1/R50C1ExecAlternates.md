# R50C1ExecAlternates — alternates leg, case table against the candidate fence

Seat: `R50C1ExecAlternates` (executor, leaf) · serves **R50-C1** (novelty) · wave `round-50/w1`
Claims read in full first: `plans/round-50-claims.md` (frozen predicate, controls, kill rule, open window).

## Axes named

- **A1 honest-geometry completeness of the alternates rule** — does the candidate admit every git-written
  alternates state whose stores are inside `d` (relative, absolute, `..`-normalised, multi-line, chained)?
- **A2 boundary soundness of the alternates rule** — does the candidate still refuse every alternates state
  that lets a git child read an object store outside `d`?
- **A3 shape exactness** — does the rule accept only byte shapes git itself writes/reads (CR, NUL, comment,
  whitespace, symlink/hardlink, empty, no-final-newline)?
- Axes intentionally untouched: config/refs/FETCH_HEAD/gitfile legs (other seats), the mutant battery, the
  population pin.

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
```

- Lane tip at measurement: `5c56819f7964f4af19c960de08a49cd8f95781ce`.
- Ancestry asserted before any measurement:
  `git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD` → `ANCESTOR_OK freeze`;
  `git merge-base --is-ancestor 71f5f5f77591d8c3d19297ee9785436da45209e4 HEAD` → `ANCESTOR_OK base`.
- All fence measurements ran on `git clone --shared <lane> lane` checked out at `3b02d57`, `TREE dirty=0`.
- git 2.56.0.

### Candidate fence under test (moving target, digests recorded)

The wave names the candidate the repair seat publishes at
`.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py`. It changed seven times during this seat; every
revision was snapshotted and the **alternates function itself was byte-identical across all of them**
(`sed -n '/^def _alternates/,/^def _objects/p' | sha256sum` = `56c6df57c3846e4eb652adedffd26a4a919b7235664363239766b34da597d07c`).
The table below is measured against the last stable revision:

| role | file | sha256 |
|---|---|---|
| base fence (freeze) | `plans/fixture_fence.py` @ 3b02d57 | `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` |
| **candidate fence** | `C1ExecRepair/fence_candidate.py` (== my snapshot `fence_snap5.py`) | `6df6a2a331a66195cfeb963b457372596cd55ac1199d7d97027323a533a76ec2` |
| candidate + this seat's alternates-only patch | scratch `fence_altfix5.py` | `cbadb0f06c23d3d88c94476687bb49fa8b18d98612bc8a8a6a25b57327680d2e` |

## Commands run (verbatim)

```bash
# control: base fence on the frozen population (fast legs)
cd /fast/scratch/hyaku/kengaku-r50/R50C1ExecAlternates/lane
python3 plans/round50_c1_verify.py --lane . --skip-mutants --work "$S/work-base"
#   → HONEST fixtures=126 admitted=113 refused=13 error=0 ; REFUSALS 20/20 ; SEALED 12/12 ; PREDICATE R50-C1 fail

# candidate fence, same legs
python3 plans/round50_c1_verify.py --lane . --skip-mutants --fence "$S/cand/fence_snap5.py" --work "$S/work-snap5"
#   → HONEST fixtures=126 admitted=117 refused=9 error=0 ; REFUSALS total=20 clean=20 leaked=0 ; SEALED total=12 clean=12 leaked=0

# alternates case tables (git truth + base + candidate per case)
python3 case_table.py  --work "$S/cases"  --base "$S/lane/plans/fixture_fence.py" --cand "$S/cand/fence_snap5.py"
python3 case_table2.py --work "$S/cases2" --base "$S/lane/plans/fixture_fence.py" --cand "$S/cand/fence_snap5.py"
python3 witness_escape.py --work "$S/witness" --base "$S/lane/plans/fixture_fence.py" --cand "$S/cand/fence_snap5.py"

# candidate + alternates patch (same three drivers, then the counter fast legs)
python3 case_table.py  --work "$S/cases-fix5"  ... --cand "$S/cand/fence_altfix5.py"   # 0 mismatches
python3 case_table2.py --work "$S/cases2-fix5" ... --cand "$S/cand/fence_altfix5.py"   # 0 mismatches
python3 plans/round50_c1_verify.py --lane . --skip-mutants --fence "$S/cand/fence_altfix5.py" --work "$S/work-fix5"
#   → HONEST admitted=117 refused=9 ; REFUSALS 20/20 ; SEALED 12/12 (identical to the unpatched candidate)
```

Each fixture is built under `<work>/<case>/f000` with `d = f000` and any "outside" store at
`<work>/<case>/outside/…` (a sibling of `d`). Every git call uses `env -i … git …` (per-command env: no
`GIT_CONFIG_GLOBAL`/`GIT_AUTHOR_*` exported into a shell).

## Case table — the six named sub-items

`git` column is git's own reading of the same fixture: `fsck --strict` rc, and `cat-file -t <commit that
exists ONLY in the borrowed store>` taken from the fixture's lane (so `commit` = git really resolved the borrow).
`base` = fence at freeze, `cand` = candidate `6df6a2a`.

### (a) relative alternates inside `d` — HONOURED

| case | geometry | git | base | cand |
|---|---|---|---|---|
| `a-rel-inside` | `lane/.git/objects/info/alternates` = `../../../main/.git/objects` (the `n22` shape) | fsck 0, cat-file `commit` | BREACH | **ADMIT** |

### (b) absolute alternates inside `d` — HONOURED

| case | geometry | git | base | cand |
|---|---|---|---|---|
| `b-abs-inside` | same borrow, entry is `<d>/main/.git/objects` absolute | fsck 0, cat-file `commit` | BREACH | **ADMIT** |

`git clone --shared` writes an absolute entry (measured: it wrote `…/d/lane/.git/objects`), so the absolute
shape is git-written and must be admitted.

### (c) one line outside `d` — REFUSED

| case | geometry | git | base | cand |
|---|---|---|---|---|
| `c-mixed-one-outside` | line 1 inside `d`, line 2 `<outside>/store/.git/objects` | fsck 0, cat-file `commit` | BREACH | **BREACH** (`names '…', which resolves outside the fixture`) |
| `c-all-outside` | only line is `<outside>/store/.git/objects` (the `f5` refusal shape) | fsck 0 | BREACH | **BREACH** |

Line order does not matter: the first offending line refuses the fixture.

### (d) chained alternates — DECISION

| case | geometry | git | base | cand | expected |
|---|---|---|---|---|---|
| `d1-chain-inside-abc` | A→B, B→C, all three repos inside `d`; commit exists only in C | fsck 0, cat-file from A = `commit` | BREACH | **ADMIT** | ADMIT |
| `d10-two-hops-both-inside` | A→`pool/objects`→`store/.git/objects`, all inside | fsck 0, cat-file `commit` | BREACH | **ADMIT** | ADMIT |
| `d3b-chain-nonrepo-inside` | A→`pool/objects`→`pool2/objects`→`store/.git/objects`, all inside | fsck 0, cat-file `commit` | BREACH | **ADMIT** | ADMIT |
| `d2-chain-hop-outside` | A→B (inside); **B's own** alternates names a store outside `d` | fsck 0, cat-file `commit` | BREACH | **BREACH** | BREACH |
| `d3d-recursive-escape-in-repo-store` | same, hop store is a repo `.git` | fsck 0, cat-file `commit` | BREACH | **BREACH** | BREACH |
| `d3e-recursive-escape-via-gitfile-store` | hop store is named only by a `.git` file (`n21` shape) | fsck 0, cat-file `commit` | BREACH | **BREACH** | BREACH |
| `d3-chain-through-nonrepo` | A→`d/pool/objects`; that dir's **own** alternates names a store outside `d` | fsck 0, cat-file from A = **`commit`** | BREACH | **ADMIT ← escape** | BREACH |
| `d3c-recursive-escape-relative` | same, outside store named by a relative climb | fsck 0, cat-file **`commit`** | BREACH | **ADMIT ← escape** | BREACH |
| `d7-escape-via-bare-repo` | A→`d/bare.git/objects` (bare repo: the tree walk collects only dirs holding a real `.git` dir) whose alternates climbs out | fsck 0, cat-file **`commit`** | BREACH | **ADMIT ← escape** | BREACH |
| `d8-escape-via-plain-dir` | A→`d/shared/objects` (plain directory) whose alternates climbs out | fsck 0, cat-file **`commit`** | BREACH | **ADMIT ← escape** | BREACH |
| `d9-hop-store-is-http-alternates` | hop dir carries `info/http-alternates` only | fsck 0, cat-file ERR (git does not read it locally) | BREACH | **ADMIT** | BREACH-or-ADMIT (fix: BREACH) |

**Decision on chains:** a chain whose every hop is inside `d` is **honoured** when each hop that is a collected
store is itself classified (repos and gitfile-named stores are; measured `d2`/`d3d`/`d3e`). It is **not honoured**
transitively: a hop directory that is *not* a collected store (plain directory, bare repo, `d/pool/objects`) is
only `lstat`-ed, its own `objects/info/alternates` is never read, and git **does** follow it — four witnessed
escapes above.

**Decision on cycles:** a cycle is **NOT refused**, by the candidate or by the patched candidate. Measured
`git 2.56.0`: A↔B (`d4-cycle-two-repos`, `cat-file` from A = `commit`, `fsck --strict` rc 0), A→B→C→A
(`d6-cycle-three`, `cat-file` = `commit`, fsck 0), self-reference `.` (`d5-self-reference`, `commit`, fsck 0),
duplicate line (`g7`). git neither errors nor hangs, and a cycle is not an out-of-`d` read, so refusing it would
be unnecessary over-refusal. The obligation it creates is termination: any recursive implementation must carry a
visited set (git normalises and dedups the object-dir list).

### (e) `..` climb: inside `d` vs outside `d`

| case | geometry | git | base | cand |
|---|---|---|---|---|
| `e1-climb-inside` | `../../../src/.git/objects` from `lane/.git/objects` = `d/src` | fsck 0, cat-file `commit` | BREACH | **ADMIT** |
| `e3-abs-dotdot-inside` | `<d>/lane/../src/.git/objects` (absolute, normalises inside) | fsck 0, cat-file `commit` | BREACH | **ADMIT** |
| `e9-climb-out-and-back-in` | `../../../../f000/main/.git/objects` — climbs above `d`, re-enters by name; normalised path is inside `d` | fsck 0, cat-file `commit` | BREACH | **ADMIT** |
| `e2-climb-outside` | `../../../../store/.git/objects` — one `..` too many | fsck 0, cat-file ERR (`unable to normalize alternate object path`) | BREACH | **BREACH** (`resolves outside the fixture`) |
| `e4-dangling-inside` | `../../../nowhere/.git/objects` | fsck 0, cat-file ERR | BREACH | **BREACH** (`does not exist`) |
| `e5-target-is-file` | entry names a regular file inside `d` | fsck 0 | BREACH | **BREACH** (`is not a directory`) |
| `h3-target-is-symlink` | entry names a symlink inside `d` pointing at an inside-`d` object dir | fsck 0, cat-file `commit` | BREACH | **BREACH** (`is a symlink`; the tree walk refuses the symlink first) |

The rule is judged on the **normalised** path (`os.path.normpath` then `_inside`), not on the text — which is
what git does (`e9` and `e3` resolve for git, `e2` does not).

### (f) `http-alternates` — STAYS REFUSED

| case | geometry | git | base | cand |
|---|---|---|---|---|
| `f1-http-alternates` | `objects/info/http-alternates` = URL, plus a valid in-`d` `alternates` | fsck 0, cat-file `commit` (from the `alternates` line) | BREACH | **BREACH** (`info/http-alternates is not git's alternates file`) |
| `f2-http-alternates-alone` | only `http-alternates` present | fsck 0 | BREACH | **BREACH** |
| `d9-hop-store-is-http-alternates` | same file on a hop directory | fsck 0 | BREACH | ADMIT (hop dirs unclassified) |

git only uses `http-alternates` for dumb-HTTP fetch; local reads ignore it (measured: `cat-file` ERR on the
hop-only case), so refusing it costs no honesty and the hop-level gap is not an escape.

### Shape exactness (git-write/no-write shapes)

| case | geometry | git behaviour (measured) | base | cand |
|---|---|---|---|---|
| `g1-crlf` | entry terminated `\r\n` | **fails** (`object directory …?` + fatal) | BREACH | **BREACH** (bare CR) |
| `g2-nul` | entry carries `\x00` | resolves anyway | BREACH | **BREACH** (NUL byte) |
| `g3-trailing-space` | entry has two trailing spaces | **fails** (`unable to normalize alternate object path`) | BREACH | **ADMIT** (candidate strips `" \t"` — divergence) |
| `g4-comment-line` | `# a comment` then a valid absolute entry | **succeeds** (git skips the comment) | BREACH | **BREACH** (comment line git does not write) |
| `g5-empty-file` | empty `alternates` file | succeeds, no borrow | BREACH | **BREACH** (`names no object directory`) |
| `g6-blank-lines-around` | blank lines around the valid entry | succeeds | BREACH | **ADMIT** |
| `g8-no-final-newline` | one entry, no trailing `\n` | succeeds | BREACH | **ADMIT** |
| `h1-alternates-is-symlink` | the alternates file is a symlink | succeeds (git follows) | BREACH | **BREACH** (`is a symlink`) |
| `h2-alternates-hardlink` | alternates file has a second hard link inside `d` | succeeds | BREACH | **BREACH** |
| `e6-target-not-objectdir`, `e7-target-is-d-itself`, `e8-target-repo-gitdir-not-objects` | target is an inside-`d` directory that is not an object store | `e8` fails, `e6`/`e7` succeed silently | BREACH | ADMIT / ADMIT / ADMIT (inside `d`: no outside read) |

`g5` and `g4` are decided refusals (git reads those shapes but never writes them); `g3` is a genuine divergence —
git cannot resolve a whitespace-padded entry while the candidate strips it and admits.

## The defect: transitive alternates through an unclassified hop (witnessed)

`witness_escape.py` builds each shape, asserts the borrowed object file exists **only outside `d`**, asks git
from the fixture's lane, then asks the fence. Verbatim rows (one per shape, object sha trimmed to shape):

```json
{"kind": "plain-dir-hop",            "object_file_exists_outside": true, "copies_inside_d": [],
 "git_cat_file_type": "commit", "git_cat_file_rc": 0, "cand_verdict": "ADMIT", "cand_why": "", "base_verdict": "BREACH"}
{"kind": "plain-dir-hop-relative",   "object_file_exists_outside": true, "copies_inside_d": [],
 "git_cat_file_type": "commit", "git_cat_file_rc": 0, "cand_verdict": "ADMIT", "cand_why": "", "base_verdict": "BREACH"}
{"kind": "bare-repo-hop",            "object_file_exists_outside": true, "copies_inside_d": [],
 "git_cat_file_type": "commit", "git_cat_file_rc": 0, "cand_verdict": "ADMIT", "cand_why": "", "base_verdict": "BREACH"}
{"kind": "non-repo-dir-hop",         "object_file_exists_outside": true, "copies_inside_d": [],
 "git_cat_file_type": "commit", "git_cat_file_rc": 0, "cand_verdict": "ADMIT", "cand_why": "", "base_verdict": "BREACH"}
```

Shape: `A/.git/objects/info/alternates` = `../../../pool/objects` (inside `d`), and
`d/pool/objects/info/alternates` = `<outside>/c/.git/objects`. The candidate admits `A`; git then resolves a
commit that exists only outside `d` (`copies_inside_d: []`). The repair's own item (5) requires "every existing
refusal path stays closed", and the base fence refuses this fixture, so this is a regression introduced by the
candidate, not an inherited limit. The reason it survives: `_alternates` classifies one level only, and
`_tree` collects only directories holding a real `.git` dir (plus gitfile targets), so a plain `…/objects`,
a bare repo and `d/pool/objects` are never classified. No frozen module covers the shape (`plans/refusals46/`
and `plans/sealed46/` mention alternates only in `f5_alternates.py`, direct out-of-`d`, and
`sealed46/p_info_redirect.py`, a symlinked `objects/info`), so the frozen REFUSALS/SEALED legs stay green while
the escape exists — this shape should be a **blind sealed50 module**.

## Minimal patch (scratch-verified; for the L1 to transcribe)

Applied to the candidate `6df6a2a` in scratch; 40/40 case verdicts match expectation and all four escape shapes close
while all honest chains stay admitted. One change of substance (recurse into every hop's `info/`), one of
exactness (do not strip whitespace).

```diff
--- fence_snap5.py   (candidate 6df6a2a)
+++ fence_altfix5.py  (candidate + alternates patch)
@@ -55,6 +55,7 @@
 CONFIG_CAP = 1 << 20        # a `.git/config` larger than this is refused unread
 INDEX_CAP = 1 << 24         # a `.git/index` larger than this is refused
 TEXT_CAP = 1 << 16          # cap for HEAD / ORIG_HEAD / COMMIT_EDITMSG / logs
+ALT_CAP = 8                 # alternates hops before the chain itself is refused as pathological
 
 ORDER_SHAPE = ("--lane", "--claims", "--receipt")
 ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}
@@ -428,13 +429,18 @@
     return None
 
 
-def _alternates(p, label, base, d):
-    """`objects/info/alternates`: every line must name an object dir inside `d`.
+def _alternates(p, label, base, d, seen=None, depth=0):
+    """`objects/info/alternates`: every line must name an object dir inside `d`, transitively.
 
     A relative entry resolves against the objects dir the file lives in (`base`), which is how git reads it.
-    Comment lines are refused: git writes none. An out-of-`d`, dangling or symlinked target is refused, and so
-    is a file with no entry at all.
+    git follows the alternates of an alternate (measured: a three-hop chain resolves a commit that lives only
+    in the last store), so each target's own `info/` is classified here too: only `alternates` may appear in
+    it, and its entries must resolve inside `d` as well. A target already classified is not re-entered, so a
+    cycle terminates (git tolerates cycles: measured `fsck` rc 0 and `cat-file` rc 0); a chain deeper than
+    `ALT_CAP` hops is refused. Comment lines are refused: git reads them but writes none. An out-of-`d`,
+    dangling or symlinked target is refused, and so is a file with no entry at all.
     """
+    seen = set() if seen is None else seen
     raw = _read(p, TEXT_CAP)
     if raw is None:
         return f"{label} unreadable"
@@ -446,8 +452,7 @@
         return f"{label} carries a bare CR"
     if any(b >= 0x80 for b in raw):
         return f"{label} carries a non-ASCII byte"
-    lines = [line.strip(b" \t") for line in raw.split(b"\n")]
-    lines = [line for line in lines if line]
+    lines = [line for line in raw.split(b"\n") if line]
     if not lines:
         return f"{label} names no object directory"
     for line in lines:
@@ -466,6 +471,32 @@
             return f"{label} names {text!r}, which is a symlink"
         if not stat.S_ISDIR(st.st_mode):
             return f"{label} names {text!r}, which is not a directory"
+        key = _norm(target)
+        if key in seen:
+            continue                                  # cycle: git tolerates it, and it is already classified
+        seen.add(key)
+        if depth + 1 > ALT_CAP:
+            return f"{label} nests alternates deeper than {ALT_CAP} hops"
+        inner = target / "info"
+        try:
+            ist = os.lstat(inner)
+        except OSError:
+            continue                                  # no info/ under the target: nothing further to follow
+        if stat.S_ISLNK(ist.st_mode):
+            return f"{label} target {text!r} has a symlinked info directory"
+        if not stat.S_ISDIR(ist.st_mode):
+            return f"{label} target {text!r} has an info entry that is not a directory"
+        ients = _entries(inner)
+        if ients is None:
+            return f"{label} target {text!r} info unreadable"
+        for iname, imode, _is, _in in ients:
+            if iname != "alternates":
+                return f"{label} target {text!r} carries info/{iname}, which is not git's alternates file"
+            if stat.S_ISLNK(imode) or not stat.S_ISREG(imode):
+                return f"{label} target {text!r} info/{iname} is not a regular file"
+            why = _alternates(inner / iname, f"{label} -> {_rel(target, d)}", target, d, seen, depth + 1)
+            if why:
+                return why
     return None
 
 
```

Effect, measured on the same six legs:

| fence | HONEST | REFUSALS | SEALED | alternates cases matching expectation |
|---|---|---|---|---|
| base `05d5fe03` | 113/126 admitted (13 refused) | 20/20 | 12/12 | 0/16 admit-side, all refusals correct |
| candidate `6df6a2a` | 117/126 admitted (9 refused) | 20/20 | 12/12 | 6 divergences (34/40): escapes `d3`/`d3c`/`d7`/`d8`, hop-http `d9`, whitespace `g3` |
| candidate + patch `cbadb0f0` | 117/126 admitted (9 refused) | 20/20 | 12/12 | **40/40** |

The patch is verdict-neutral on the frozen population and batteries (identical counters), because it only
*adds* refusals for shapes no frozen module builds.

## Observations outside the alternates leg (measured, flagged only)

1. Candidate `6df6a2a` refuses `n08-tag-detached` (`HEAD is not a plain branch HEAD`), which the base fence
   **admits** (base refused list: `n12 n13 n14 n15 n16 n17 n18 n20 n21 n22 n03 n07`). That is a new
   over-refusal on a pinned honest class and a blocker for `HONEST admitted=126` regardless of this leg.
2. Candidate refuses `n15-commit-graph` with `objects/info/commit-graph is not git's alternates file` — the
   `objects/info` branch admits only `alternates`, so `commit-graph` (git-written) stays over-refused.
3. `n18-shallow-fetch` is now refused through `[remote "origin"]` config, not through `FETCH_HEAD`; the
   `FETCH_HEAD` allowance is present in `GIT_TOP` but unreachable until the config leg lands.
4. `C1ExecRepair`'s `_tree` copy at revision `b839244c` appended `.git`-file repos to `repos`; later revisions
   return `(repos, gitfiles, why)` — the file is still moving, so the L1 should re-run this table against the
   digest it actually lands.

## Limits

- The table measures `breach()` admission decisions only. It does not re-run the round-46 strace legs; the
  "git really reads outside `d`" claim is measured by `git cat-file -t` on an object that exists only outside
  `d` (`witness_escape.py` asserts `copies_inside_d: []`), not by syscall tracing.
- Absolute-path cases (`b`, `g3`, `e3`) embed the scratch root in the fixture, so they cannot join the frozen
  population; they are probes, not population rows.
- Case `e6`/`e7`/`e8` (target is a non-object directory inside `d`) are decided admissions with no outside
  read; whether they should be refused is a shape-policy call for the L1, not a boundary property.
- `http-alternates` was tested with a URL only; a path spelled in that file is never read by local git.
- Host: git 2.56.0, one filesystem (`/fast`), no mount-cross or case-insensitive variant tested.
- The candidate is a live file owned by another seat; all digests above are the ones actually measured.

## VERDICT

**Alternates leg proven, with one witnessed defect in the candidate.** (a) relative in-`d` alternates is
honoured, (b) absolute in-`d` alternates is honoured, (c) a single out-of-`d` line (any position) is refused,
(d) chained alternates are honoured hop-by-hop when every hop is a classified store inside `d` and **not**
honoured transitively — a hop that is a plain directory, a bare repo or any directory the tree walk never
classifies lets git read outside `d` while the candidate admits (four witnessed escapes, `git cat-file` resolves
an object that exists only outside `d`); a cycle is **not** refused, matching git 2.56.0 which neither errors nor
hangs on A↔B / A→B→C→A / self-reference, and the recursive fix terminates on a visited set; (e) a `..` climb is
judged on the normalised path — inside `d` admitted (including out-and-back-in), outside `d` refused; (f)
`objects/info/http-alternates` stays refused at the store level. The candidate reaches 34/40 case verdicts; the patch below (one recursive hop block plus `ALT_CAP` and
dropping whitespace-stripping) reaches 40/40 with identical counter legs
(117/20/12). The escape is invisible to the frozen REFUSALS/SEALED legs and should be a blind sealed50 module.

No production file was read for write, no commit/push/stash ran, no sibling scratch was written; scratch
`/fast/scratch/hyaku/kengaku-r50/R50C1ExecAlternates` was removed before this yield.

## Addendum — re-measure after the sibling's final candidate and the in-lane repair (same session)

Trigger: `R50C1ExecRepair` reported its final candidate as `9baedf13…` and that the lane file `plans/fixture_fence.py`
had meanwhile been rewritten (uncommitted, by another seat) to `57adce4a…`. Both digests were re-measured on the
same 14-case compact alternates probe, same clone (`git clone --shared` at `3b02d57`, `TREE dirty=0`), base column =
the frozen fence:

```
9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1  .ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py
57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1  plans/fixture_fence.py   (in lane, uncommitted)
```

| case | expected | git | base `05d5fe03` | candidate `9baedf13` | lane `57adce4a` |
|---|---|---|---|---|---|
| `a-rel-inside` | ADMIT | cat-file commit | BREACH | ADMIT | ADMIT |
| `b-abs-inside` | ADMIT | commit | BREACH | ADMIT | ADMIT |
| `c-mixed-one-outside` | BREACH | commit | BREACH | BREACH | BREACH |
| `d-chain-inside` | ADMIT | commit | BREACH | ADMIT | ADMIT |
| `d4-cycle` | ADMIT/BR each | commit | BREACH | ADMIT | ADMIT |
| `e-climb-inside` | ADMIT | commit | BREACH | ADMIT | ADMIT |
| `e2-climb-outside` | BREACH | commit | BREACH | BREACH | BREACH |
| `d3c` plain-hop escape | BREACH | commit | BREACH | **ADMIT** | **BREACH** |
| `d7` bare-repo escape | BREACH | commit | BREACH | **ADMIT** | **BREACH** |
| `d8` plain-dir escape | BREACH | commit | BREACH | **ADMIT** | **BREACH** |
| `f1-http-alternates` | BREACH | commit | BREACH | BREACH | BREACH |
| `g1-crlf` | BREACH | fails | BREACH | BREACH | BREACH |
| `g3-trailing-space` | BREACH | fails | BREACH | **ADMIT** | **BREACH** |
| `g5-empty-file` | ADMIT/BR each | tolerates | BREACH | BREACH | **ADMIT** |

Measured consequences:

1. **The escape is present in the final candidate `9baedf13`** — all three hop shapes (`d3c`, `d7`, `d8`) are
   admitted while git resolves a commit that exists only outside `d`. Its `_alternates` is textually the
   one-level function measured above; the patch in this report still applies to it unchanged.
2. **The in-lane `57adce4a` already closes all three** — it carries a recursive `_alternates(path, objects,
   depth, seen)` with a visited set and `ALTERNATES_DEPTH = 4`. **Do not stack my patch on it**; a clean cutover
   means taking one repair, not both.
3. Two residual facts about the in-lane `57adce4a`, measured on the same probe:
   - an alternates entry carrying `\x00` **raises `ValueError: lstat: embedded null character in path`** out of
     `breach()` (`except OSError` does not catch it). A raising fence is never an admission (the counter's
     `verdicts()` records `ERROR`), but it breaks the frozen `str | None` contract on hostile input; the
     candidate `9baedf13` refuses it with `carries a NUL byte`.
   - an **empty** alternates file is now admitted (`g5`); git tolerates it and never writes it, so this is a
     shape-policy widening, not an escape.
   - its hop cap is `ALTERNATES_DEPTH = 4` (my patch used `ALT_CAP = 8`); a legitimate 5-hop chain would be
     refused. No frozen honest class has one.

Revision note: the lane file's digest is uncommitted and owned by another seat; the numbers above are the ones
measured at `57adce4a`, not a claim about what S2 will commit.

## Addendum 2 — final state (lane tip `d45c5bb`, landed fence, sibling's fixed candidate)

The lane advanced while this seat was reporting: `6db0279` landed the S3 fence repair, `d6f2fce` froze the
mutant battery and `d45c5bb` carries the scored receipt. Measured final digests:

```
d6f2fce9889f429162c12f851bae41891bedf5cd   scored C1 receipt revision (corpus/evidence/round50/c1-receipt.txt)
57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1   plans/fixture_fence.py at HEAD (= the in-lane file
                                                                  measured in Addendum 1, byte-identical)
2b142a852190f1f30f3c83da7abfcc57f6597eb09194feba8dc2b087bef804fc   C1ExecRepair/fence_candidate.py (their fixed candidate)
```

Scored receipt (verbatim, `corpus/evidence/round50/c1-receipt.txt`):

```
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
```

Eight-case probe, same clone at `3b02d57`, run against the landed fence and the fixed candidate:

| case | expected | git | landed `57adce4a` | candidate `2b142a85` |
|---|---|---|---|---|
| `escape-plain-hop` | BREACH | cat-file commit (object only outside `d`) | **BREACH** (`pool/objects/info/alternates names a store outside the fixture`) | **BREACH** (`… -> '../../../pool/objects' names '../..`) |
| `escape-bare-repo` | BREACH | commit | **BREACH** (`bare.git/objects/info/alternates names a store outside the fixture`) | **BREACH** |
| `escape-plain-dir` | BREACH | commit | **BREACH** (`shared/objects/info/alternates names a store outside the fixture`) | **BREACH** |
| `honest-2hop` | ADMIT | commit | ADMIT | ADMIT |
| `honest-cycle` | ADMIT/BR | commit | ADMIT | ADMIT |
| `edge-trailing-space` | BREACH | git fails | **BREACH** (`store/.git/objects   does not exist`) | **BREACH** |
| `edge-empty-file` | ADMIT/BR | git tolerates | **ADMIT** | **BREACH** (`names no object directory`) |
| `edge-nul` | BREACH/ERROR | commit | **ERROR** — `ValueError: lstat: embedded null character in path` escapes `breach()` | **BREACH** (`carries a NUL byte`) |

Conclusions for the integrator:

1. **The defect this seat reported is closed by the landed fence.** Its own recursive `_alternates` refuses all
   three hop shapes at the hop, with hop-specific reasons; the base fence also refused them, so the landing
   restores the boundary rather than inheriting the candidate's escape. No part of this seat's patch should be
   ported onto `57adce4a` (stacking two recursive walks is not a clean cutover).
2. **Two residuals remain on the landed artifact**, neither covered by the population, the 20 refusals or the 18
   sealed modules — which is why the predicate passes with them present:
   - an alternates entry containing `\x00` **raises `ValueError` out of `breach()`** (`except OSError` does not
     catch it). The counter records `ERROR`, never an admission, so it is not a leak, but it breaks the frozen
     `str | None` contract under hostile input — the one thing worth a follow-up.
   - an **empty** `objects/info/alternates` file is admitted; git tolerates it and never writes it, and it stays
     inside `d`, so it is a shape widening, not a boundary break.
3. The three hop shapes are absent from the scored hostile set (`20 + 18` modules: `f5_alternates.py` is the
   direct out-of-`d` case, `sealed46/p_info_redirect.py` a symlinked `objects/info`). The landing closes the
   category by construction, not by test; a blind two-hop module would make that visible next round.
