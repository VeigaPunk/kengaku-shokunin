# R50C1SimplBudget — simplifier attack on the R50-C1 instrument's size

**Seat:** R50C1SimplBudget (simplifier) · **Serves:** R50-C1 (novelty) · **Judged on:** novelty
**Item:** list every leg, literal and helper the predicate does not need; propose the smallest counter that keeps
the same falsifiable predicate; name what would be lost. No edits to the lane.

---

## Axes

| axis | what it is | direction |
|---|---|---|
| **A1 predicate surface** | the six printed lines of `plans/round-50-claims.md` §C1 and exit 0/1/2 | **immutable** (frozen) |
| **A2 size** | lines / bytes of `plans/round50_c1_verify.py` | ↓ |
| **A3 falsifiability** | can the predicate still reach `fail` for every frozen kill condition | ↑ (never ↓) |
| **A4 receipt fidelity** | every failure/report line byte-identical to the frozen counter | **immutable** |
| **A5 cost** | wall time of a scored run | ↓ |

Keep a move that improves A2/A5 or A3 and harms neither A1 nor A4. A move that shrinks code by weakening A3 or
breaking A4 is rejected even if it is smaller.

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
```

`git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD` → **yes** (lane tip when checked:
`5c56819f7964f4af19c960de08a49cd8f95781ce`; re-checked after the wave advanced, freeze is still an ancestor of
`c3372a9`). All measurement is on a `git clone --shared` of the lane at the freeze commit; the live checkout was
never written to — the only git commands I ran in the lane were `rev-parse`, `status --porcelain` and
`merge-base --is-ancestor`. Instrument digests at the measured revision match the claims file:
`plans/round50_c1_verify.py` `f9b9873e…bd76`, `plans/fixture_fence.py` `05d5fe03…ad5e`,
`plans/honest50/population.txt` `b5197f94…ae69`.

## Commands run (exact)

```
git -C <lane> merge-base --is-ancestor 3b02d573… HEAD
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane && git -C $S/lane checkout 3b02d573…
python3 plans/round50_c1_verify.py --lane . --skip-mutants --work "$S/w1"          # 7 s
python3 plans/round50_c1_verify.py --lane . --work "$S/w2"                          # 8 s
python3 "$S/min_counter.py" --lane . --allow-dirty --work "$S/wc"                   # candidate, both modes
for c in admit_all refuse_all keyed_names; do
  python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants --work "$S/wc" --fence plans/controls50/$c.py
  python3 "$S/min_counter.py"        --lane . --allow-dirty --skip-mutants --work "$S/wc" --fence plans/controls50/$c.py
done
diff <(sed -E 's#k50-c1-[a-z0-9_]+#k50-c1-XXXX#g' A.out) <(same on B.out)             # 6 comparisons
python3 - <<‘PY’ … ast.walk …                                                       # dead-name census
PY
```

`--work` must be an **existing** directory: `tempfile.mkdtemp(dir=a.work)` raises `FileNotFoundError` (exit 1,
traceback, not the documented setup exit 2) when it does not. One-line fix, listed as **R1** below.

## 1. Census: every leg, literal and helper

### Legs (5 printed labels, 6 kill conditions)

| leg | printed line | kill condition (claims §C1) | needed? |
|---|---|---|---|
| POPULATION | `POPULATION fixtures=126 pin=… mismatched=0 build_errors=0` | `mismatched > 0` | yes — the frozen denominator |
| HONEST | `HONEST fixtures=126 admitted=126 refused=0 error=0` | `HONEST admitted < 126` | yes |
| REFUSALS | `REFUSALS total=20 clean=20 leaked=0 build_errors=0` | any module not refused | yes |
| SEALED | `SEALED total=<S> clean=<S> leaked=0 build_errors=0` | any module not refused; `<S>` ≥ 18 | yes |
| MUTANTS | `MUTANTS total=<M> caught=<k> broken=0 floor=12 verdict=met` | `<k>` ≥ 12, `<M>` ≥ 12 | yes |
| (receipts) | `REV`, `TREE`, `FENCE` | dirty tree fails | yes — S3 receipt needs `REV` |

**No leg is subsumed by a cheaper check.** Each answers a question the others cannot:

- POPULATION is not implied by HONEST — a fixture that drifted can still be admitted, and the pinned
  `tree_sha256` rows (not the file hash) are what make the fixture the frozen one. `POPULATION_SHA` alone proves
  only that the *list* did not change.
- REFUSALS is not subsumed by SEALED — different frozen populations (20 vs 12+blind), different literals,
  separate printed lines.
- MUTANTS is not subsumed by any static check. The cheap version of it — assert each payload applies
  (`broken=0`) — costs 23 `patch` calls and **would not detect the 8 mutants that currently change nothing**
  (measured below). That is strictly weaker, so it is not a simplification.

Measured cost split, so no cost argument survives for deleting a leg: fast legs **6–7 s**, full run **7–10 s**,
i.e. the whole mutant leg (23 patches + 3 634 `breach()` calls) is **~1–4 s ≈ 15–40 %**; the 126-fixture rebuild
plus identity walk is the other 60–85 %. There is no cost outlier to amputate.

### Literals

| literal | value | read by | verdict |
|---|---|---|---|
| `HONEST_TOTAL` | 126 | `len(rows) != HONEST_TOTAL` | **frozen, keep** |
| `MUTANT_MIN` | 12 | floor in the printed line and in `ok` | **frozen, keep** |
| `REFUSALS_TOTAL` | 20 | post-hoc re-glob only | **frozen, keep** (move the check) |
| `SEALED50_MIN` | 6 | post-hoc re-glob, **guarded by `is_dir()`** | **frozen keep, but currently decorative** (§3.2) |
| `POPULATION_SHA` | `b5197f94…` | `pop_sha != POPULATION_SHA` | **frozen, keep** |
| `SEALED46_TOTAL` | 12 | **nothing** | **dead — delete** (AST-confirmed) |

`12` is a duplicate literal: `MUTANT_MIN` (live) and `SEALED46_TOTAL` (dead). Only the live one is load-bearing.

### Helpers

| helper | lines | read by | verdict |
|---|---|---|---|
| `main()` | 16 head + ~100 | — | necessary |
| `sha256_file` | 6 | 2 call sites | **shrink** (streaming loop over ≤ 40 KB files) |
| `load` | 5 | 4 sites | necessary |
| `module_path` | 3 | 1 site, body is `lane / module` | **delete — zero-value indirection** |
| `parse_population` | 9 | 1 | necessary |
| `build_all` | 12 | 3 | necessary |
| `verdicts` | 10 | 1 (+1 for mutants) | necessary |
| `apply_mutant` | 15 | 1 | **shrink** (staged `.patch` file, double module load) |
| `say()` (nested) | 2 | 17 | **delete** (see R6) |
| `fids_of` (nested) | 3 | 2 | **delete — inline** |
| `leg()` (nested) | 20 | 1 | **delete — fold into the loop** |
| `import os` | 1 | **0 attribute refs** | **delete** |

AST census over the frozen file: `SEALED46_TOTAL` is the only defined-but-never-loaded top-level name; `os` is the
only import with `attr-refs=0`.

## 2. Ranked deletion list (each proven non-semantic)

Candidate: `min_counter.py`, scratch-only, **300 → 235 lines (−65, −21.7 %)**, 14 345 → 10 957 bytes
(−3 388, −23.6 %); code lines only 254 → 215 (−39), docstring 46 → 20 (−26).

| # | deletion | lines | risk | what would be lost |
|---|---|---|---|---|
| **R1** | docstring prose: round-48/49 history, the repeated predicate block, the named-limits paragraph, the inherited-builder paragraph | **−26** | none to the predicate | the in-file limits statement — it is **already a duplicate** of `plans/round-50-claims.md` §C1 *Named limits*; one authority, not two. Do **not** delete the limits from the claims file. |
| **R2** | `hostile` intermediate list + `leg()` closure → one loop over `(REFUSALS_REL, *SEALED_RELS)`; inline `fids_of` | **−9** | none (proven) | the 4-tuple `leg()` return, whose `leaked` term is already redundant in `ok` (a leak always makes `clean < len(files)`) |
| **R3** | `sha256_file` streaming loop → `hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()` | **−5** | none | constant-memory hashing; the helper is only ever called on the fence (22 744 B) and the population file (20 702 B) |
| **R4** | `module_path()` → inline `lane / r["module"]` | **−4** | none | a named place to make the module-path rule discoverable; the docstring comment carries it |
| **R5** | `apply_mutant`: stage payload to `.patch` and `-i` → pipe payload on **stdin**; return the loaded module instead of re-`load`ing it in the mutant loop | **−3** | none (23/23 payloads identical rc+stdout+stderr) | one scratch `.patch` artefact per mutant; 23 duplicate module executions |
| **R6** | `say()` nested wrapper → `print` | **−2** | none | nothing behavioural; +34 bytes at 17 call sites, so this is the weakest item in the list |
| **R7** | `import os` | **−1** | none | nothing |
| **R8** | `SEALED46_TOTAL` dead literal | **−1** | none | the only in-file record that sealed46 is 12 — see §3.3, where the honest move is to **enforce** it instead |

**Not deletable, and why** (each was checked and rejected as a simplification):

- any of the five legs (frozen kill rules; no cheaper subsuming check — §1);
- the frozen literals `126`, `20`, `12`, `SEALED50_MIN`, `POPULATION_SHA` (the claims' open-window rule names them
  immutable: *"the predicate sentence, the four leg names, the literals `126`, `20`, `12`, `SEALED50_MIN` and the
  population pin never change"*);
- `--fence`, `--allow-dirty`, `--skip-mutants`, `--work` (the four committed controls run through `--fence` +
  `--allow-dirty`; `--skip-mutants` is the documented fast leg check; `--work` is the binding scratch rule);
- `REV` / `TREE` / `FENCE` receipts (S3 requires `REV` in the receipt);
- `apply_mutant`'s external `patch` + its `p.stdout[-160:]` reason (a pure-Python applier is not smaller, and the
  reason string is the `broken` receipt);
- the mutant short-circuit (`stop at the first differing fixture`): semantically equivalent, saves at most
  ~0.9 s of a 7–10 s run because `patch`+import, not `breach()`, dominate that leg — **cost move, not a size
  move**, and it would grow the file by ~6 lines. Rejected.

## 3. Falsifiability defects the size attack exposed (no lines added, or fewer)

These matter more than the −65 lines. Each is a place where the predicate is *smaller than it claims*.

### 3.1 `broken` is printed but not checked — measured, live

```
MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet
```

The claims' predicate block demands `broken=0`; the counter computes `ok` from
`caught < MUTANT_MIN or len(mutants) < MUTANT_MIN` only. **12 of 23 carried rows do not apply to the base fence**
(`patch-rc=1 … hunk FAILED`), and `ok` would still be `True` for a battery of 12 broken + 12 caught + 24 rows,
printing `broken=12 … verdict=met … PREDICATE R50-C1 pass`. Fix: `or broken` in that condition — **−0 lines**.
Correction to the carried number for the S2 battery owner: at the freeze tree the r49 battery is
**caught 3 / survived 8 / broken 12** (3+8+12=23), not "4 of 23 change the verdict vector".

### 3.2 `SEALED50_MIN` is decorative when the blind dir is absent — measured

The only guard is `if (lane / "plans/sealed50").is_dir():`. At the freeze tree (no `sealed50`) the counter prints

```
SEALED total=12 clean=12 leaked=0 build_errors=0
```

and runs **no** `SEALED50` total check, while the claims require the SEALED line to carry `<S>` ≥ 18. Observed at
the freeze tree: the frozen counter emitted `SEALED total=12` with no total check in force. On a tree where HONEST
is 126 this reaches `PREDICATE R50-C1 pass` with `<S>` = 12 — [INFERENCE from the code path: nothing else in the
`sealed50` branch can set `ok = False`]. Fix (0 net lines): drop the `is_dir()` skip and let the leg print
`SEALED total=0 … SEALED50-TOTAL 0 expected_min=6`, which fails. Receipt of the tightening:

```
A(frozen):     SEALED total=12 clean=12 leaked=0 build_errors=0
               PREDICATE R50-C1 fail
B(candidate):  SEALED total=12 clean=12 leaked=0 build_errors=0
               SEALED total=0 clean=0 leaked=0 build_errors=0
               SEALED50-TOTAL 0 expected_min=6
               PREDICATE R50-C1 fail
```

(On every tree where all three hostile dirs exist the two counters are byte-identical — proven below — including
the wrong-count path, where both print `SEALED50-TOTAL 4 expected_min=6`.)

### 3.3 `sealed46` has no total check at all

Same shape as 3.2 for the 12 frozen modules: `SEALED46_TOTAL` is dead, so if `plans/sealed46` lost 4 modules the
predicate would still print `clean == total` and pass with `<S>` = 14. The honest move is to **use** the literal
(`len(files) != SEALED46_TOTAL` for that dir), not to delete it — i.e. R8 should be reversed into a
one-line enforcement.

### 3.4 A frozen mutant is silently **reversed** and counted as a kill — measured

`patch` detects a payload whose hunks match in reverse and applies the inverse with **exit 0**:

```
c1-mut-03-drop-file-mountbound: default=(0, True) --forward=(1, True)
```

`(rc, "Reversed" in output)` on a fresh copy of the fence: mut-03 is applied **backwards**, counted in `caught`,
and is one of the 3 kills. Q38 requires a *witnessed* kill direction; this one is not witnessed. Fix:
`--forward` — measured to change exactly this one row to `rc=1` and nothing else across all 23 payloads
(**−0 lines**, one flag). q38 note for S2: with `--forward`, the base-fence reading becomes caught 2 / broken 13.

### 3.5 Contract inconsistency: "four legs" vs five printed leg lines

Claims §C1 open-window text freezes *"the four leg names"*; the instrument prints five (`POPULATION`, `HONEST`,
`REFUSALS`, `SEALED`, `MUTANTS`). A repair seat reading "four" literally could delete a line the kill rules need.
No code change; flag for the L1 to pin the count of five.

## 4. The smallest counter — equivalence evidence

`min_counter.py` (235 lines): all of R1–R7 applied, no hardening from §3 folded in (so A1/A4 stay identical).
Six comparisons, `diff` after normalising only the `mkdtemp` suffix:

| tree / fence | frozen | candidate | result |
|---|---|---|---|
| freeze tree, `--skip-mutants` (base fence) | 20 lines, rc 1 | 20 lines, rc 1 | **IDENTICAL** |
| S2-shaped tree (my 6 stub blind modules), fast | 20 lines, rc 1 | 20 lines, rc 1 | **IDENTICAL** |
| S2-shaped tree, **full** (mutant leg) | 42 lines, rc 1 | 42 lines, rc 1 | **IDENTICAL** |
| `--fence plans/controls50/admit_all.py` | 58 lines, rc 1 | 58 lines, rc 1 | **IDENTICAL** |
| `--fence plans/controls50/refuse_all.py` | 21 lines, rc 1 | 21 lines, rc 1 | **IDENTICAL** |
| `--fence plans/controls50/keyed_names.py` | 47 lines, rc 1 | 47 lines, rc 1 | **IDENTICAL** |
| S2-shaped, `sealed50` reduced to 4 modules | `SEALED50-TOTAL 4 expected_min=6` | same | **IDENTICAL** |

Those six runs exercise every reporting path: the 13 `HONEST-REFUSED` lines, `REFUSALS/SEALED clean/leaked`
counts up to 34 leaks, `-MISS` lines, `-BUILD-ERROR`, all 12 `MUTANT broken … .rej` lines, `MUTANT survived`, and
the `MUTANTS` summary. Worst case observed `admit_all`: `HONEST admitted=126 refused=0` with
`REFUSALS leaked=34`, `SEALED leaked=15+9` — the candidate reports it identically.

The one **deliberate** divergence is §3.2 (a tree with no `plans/sealed50`): the candidate fails where the frozen
counter silently skips the leg. The predicate sentence is unchanged; A3 is strictly higher.

Where I stopped: what remains is 215 code lines whose next deletions are obfuscation, not weight —
`parse_population` into a comprehension, `argparse` into `sys.argv`, the predicate format strings into a template.
Each harms A4/receipt readability for ≤ 4 lines. **The next deletion would harm the receipt axis.**

## 5. What would be lost (summary, honest)

1. The in-file **named-limits** paragraph (io_uring, outside-`d` reads, host sensitivity). It survives verbatim in
   `plans/round-50-claims.md` §C1 — deleting the copy removes a *second* authority, not the authority.
2. The round-48/49 **history** that motivates the instrument (`HONEST 120/112/8`, `124 and never scored`).
   That is the report's job, not the counter's.
3. **Constant-memory** hashing in `sha256_file` (irrelevant at 22 KB / 20 KB per call; the helper is not generic).
4. The **`leg()` closure** as a seam where a future leg could be added by writing a function instead of editing a
   loop body. This is the one real maintainability trade: the candidate trades an extension seam for a single
   straight-line loop. I take the trade because the leg set is frozen by the claims.
5. One scratch `.patch` file per mutant, and 23 duplicate module executions (pure waste).
6. Nothing about the falsifiable predicate — except that §3 makes it *stronger* if the L1 chooses to fold those
   four zero-line fixes into the S2 repair.

## 6. Limits

- I did not build, score or repair the fence; `plans/fixture_fence.py` was read-only input at the freeze digest.
- `plans/sealed50` does not exist at the freeze commit: my S2-shaped tree is **6 copies of frozen sealed46
  modules**, used only to give both counters a ≥ 6 blind leg so their output could be compared. It is not a claim
  about blind-module quality, and the 12/8/3 battery census is unaffected by it (mutant rows patch the fence, not
  the blind modules).
- The `caught=3 / survived=8 / broken=12` census is at `3b02d57` against the **base** fence, which is what the
  carried battery was not authored against; it is a statement about the *carried* battery, not about a re-derived
  one.
- §3.1's pass-with-`broken` scenario and §3.2's `pass` with `<S>` = 12 are code-path inferences, labelled; the
  *observed* facts are `broken=12` printed with `ok` not consulting it, and `SEALED total=12` printed with no
  total check in force.
- Equivalence is proven on stdout/stderr/exit-code, not on internal state; the mutant leg's `verdicts` call count
  is unchanged in the candidate (no short-circuit — deliberately, see §2).
- Host git is 2.56.0; fixture identity is host-sensitive where git output is, as the claims already name.

**Tooling:** none installed or upgraded (no package manager transaction attempted; pacman untouched).

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1SimplBudget/` (587 MB: one `--shared` clone, the candidate, receipts) was
removed before yielding — confirmed gone. The candidate `min_counter.py` is transcribed in §2/§4 as an edit list;
it was never placed in the lane. Lane state after my work: ` M corpus/QUALITY.md` (another seat's write, not mine)
and the untracked `.ufo/waves/round-50/w1/` (this report).

## Appendix — exact edits (reproducible against the frozen file `f9b9873e…bd76`)

*Reference block; §7 follows it with the drift re-check against the live revision.*

**R2** replaces `hostile` + `fids_of()` + `leg()` + both post-hoc `is_dir()` blocks with one loop:

```python
        reference = list(honest_v)
        hostile_built = []
        for rel in (REFUSALS_REL, *SEALED_RELS):
            files = sorted((lane / rel).glob("*.py"))
            fixtures, fails = build_all(hb, k44, [(f, f"{rel.split('/')[-1]}-{f.stem}") for f in files],
                                        work / rel.replace("/", "-"))
            v = verdicts(fence, fixtures)
            leaked = sum(1 for x in v if x["v"] == "ADMIT")
            clean = sum(1 for f in files if (ids := {x["fid"] for x in fixtures if x["module"] == f.name})
                        and all(x["v"] == "BREACH" for x in v if x["fid"] in ids))
            label = "REFUSALS" if rel == REFUSALS_REL else "SEALED"
            print(f"{label} total={len(files)} clean={clean} leaked={leaked} build_errors={len(fails)}")
            for e in fails[:8]:
                print(f"{label}-BUILD-ERROR {e}")
            if clean != len(files):
                for f in files:
                    ids = {x["fid"] for x in fixtures if x["module"] == f.name}
                    for x in [x for x in v if x["fid"] in ids and x["v"] != "BREACH"][:2]:
                        print(f"{label}-MISS {f.name} {x['fid']} {x['v']} {x['why']}")
            if rel == REFUSALS_REL and len(files) != REFUSALS_TOTAL:
                print(f"REFUSALS-TOTAL {len(files)} expected={REFUSALS_TOTAL}")
                ok = False
            elif rel.endswith("sealed50") and len(files) < SEALED50_MIN:
                print(f"SEALED50-TOTAL {len(files)} expected_min={SEALED50_MIN}")
                ok = False
            reference += v
            hostile_built.append((rel, files, fixtures, fails))
            if clean != len(files) or fails:
                ok = False
```

**R5** — stdin payload, module returned instead of re-loaded:

```python
def apply_mutant(fence_path, payload, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(fence_path, dest)
    p = subprocess.run(["patch", "--batch", "--silent", "-p1", str(dest)],
                       input=payload if payload.endswith("\n") else payload + "\n",
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None, f"patch-rc={p.returncode} {p.stdout.strip()[-160:]}"
    try:
        return load(dest, f"mutant_{dest.stem}"), None
    except Exception as e:
        return None, f"import: {type(e).__name__}: {e}"
```

and in the mutant loop (`mod, why = apply_mutant(...)`; `if mod is None:`; delete the second `load`):

```python
            seq = honest + [x for _rel, _files, fx, _fails in hostile_built for x in fx]
            ...
                if [(x["fid"], x["v"]) for x in verdicts(mod, seq)] != ref_vec:
```

**§3 fixes, zero net lines** (each changes output only where the current counter is wrong):

```python
            if caught < MUTANT_MIN or len(mutants) < MUTANT_MIN or broken:            # §3.1
            elif rel.endswith("sealed46") and len(files) != SEALED46_TOTAL:           # §3.3 (revives R8's literal)
                print(f"SEALED46-TOTAL {len(files)} expected={SEALED46_TOTAL}"); ok = False
    p = subprocess.run(["patch", "--batch", "--silent", "--forward", "-p1", str(dest)],  # §3.4
```

§3.2 needs no code: it is the deletion of the `if (lane / "plans/sealed50").is_dir():` guard, already inside R2.
The `--forward` measurement was made with the `-i` form; combining it with R5's stdin form is untested here
([INFERENCE] equivalent on POSIX `patch` 2.7.6) — re-run the battery to re-witness the kill directions either way.

**R7/R8** are the single deletions `import os` and `SEALED46_TOTAL = 12` (**R7 is moot at `850ec790`, where `os`
is used by the harness env — §7**); **R1** is the docstring rewrite (keep only:
title, the six predicate lines, the five leg names in one sentence, the `broken` note, usage, exit codes);
**R3/R4/R6** are the one-line swaps named in the table.

## 7. Post-freeze drift — re-checked at close (my own reads, lane tip `d45c5bb`)

The instrument I audited moved after the freeze. Everything above binds to
`plans/round50_c1_verify.py` **`f9b9873e…bd76`**; the live file is now different:

```
git status --porcelain          ->  M plans/round50_c1_verify.py
sha256sum plans/round50_c1_verify.py -> 850ec7906e965834…   344 lines (was 300), +59/−15 vs HEAD
sha256sum plans/fixture_fence.py     -> 57adce4a598e1ca8…   committed, not the frozen 05d5fe03…
```

The live counter replaced in-process `verdicts()` with a **separate-process harness per fixture** (Q39 decoy
padding: `secrets.token_hex` parents + `PAD=8` decoy siblings; `FENCE_TIMEOUT`). Measured cost of that change, same
clone at `3b02d57`, same base fence:

| run | frozen `f9b9873e` (in-process) | live `850ec790` (subprocess) | ratio |
|---|---|---|---|
| `--skip-mutants` | 7 s | **13 s** | 1.9× |
| full (incl. mutant leg) | 8 s | **54 s** | 6.8× |

⇒ ≈ **23.6 ms per harness spawn**; the mutant leg is 41 s of the 54 s.

**Applicability of my ranked list to `850ec790`** (re-checked by AST + grep, not assumed):

- still apply, ≈ **−49 lines**: R1 (−26, docstring is still 46 lines), R2 (−9, `leg`/`fids_of` still present),
  R3 (−5, `sha256_file` still streams), R4 (−4, `module_path` still present), R5 first half (−2, still stages a
  `.patch` and passes `-i`), R6 (−2, `say` still present), R8 (−1);
- **moot**: R7 — `os` is now used (`verdicts` builds the harness env);
- **moot, and now load-bearing in reverse**: R5's second half. `verdicts` takes a *path* and the harness imports the
  fence per fixture, so `apply_mutant`'s in-process `load` must **stay** — it is what classifies a non-importable
  mutant as `broken` instead of letting 158 `ERROR` verdicts manufacture a "catch".

**All four §3 defects are still present at `850ec790`** (verified by my own reads at the tip, not from a peer):

- `SEALED46_TOTAL = 12` (line 66) still never loaded — AST census, zero load refs;
- line 334: `if caught < MUTANT_MIN or len(mutants) < MUTANT_MIN:` — still no `broken` term;
- line 307: `if (lane / "plans/sealed50").is_dir():` — `SEALED50_MIN` still decorative;
- no `--forward`, and the measured caught set is **identical** to the frozen run
  (`{c1-mut-03-drop-file-mountbound, c1-mut-13-entry-cap-shrink, c1-mut-19-lane-membership}`) — the silently
  reversed row is still credited as one of the 3 kills.

**Invariance datapoint:** the subprocess harness reproduces the in-process verdicts exactly on the base fence —
`HONEST fixtures=126 admitted=113 refused=13`, `REFUSALS 20/20`, `SEALED 12/12`,
`MUTANTS total=23 caught=3 broken=12`. So every conclusion in §1 (leg census, no cheaper subsuming check) holds
unchanged at the live revision.

### One item I withdraw — for this design only

§2 rejected the mutant short-circuit because it saved ≤ 0.9 s on an in-process counter. **That rejection does not
carry to `850ec790`.** The vector differs iff one fixture's verdict differs, so stopping at the first difference is
exactly equivalent; at 23.6 ms/spawn each caught mutant currently wastes 158 spawns ≈ **3.7 s**. Measured waste on
the base battery = 3 caught ≈ 11 s (54 s → ~43 s); on a re-derived battery with ≥ 12 caught it is ≥ 44 s of a
scored run, and the floor is 12. It is now the single largest cost item — but it **grows** the file by ~6 lines, so
it is a cost trade, never a size deletion, and must not be reported as one.

**Not on my deletion list, deliberately:** the harness string, `PAD`, `secrets`, `FENCE_TIMEOUT` and the decoy
padding added after the freeze. Their docstrings cite measured attacks (a fence forging the counter's own globals;
a directory-name-keyed fence passing `--skip-mutants`), so those lines buy A3. Deleting them would harm the axis I
am not allowed to harm.

The `--work`-must-exist defect (a non-existent `--work` raises `FileNotFoundError`, exit 1, not the documented
setup exit 2) is **also still present** at line 209.

---

VERDICT: **R50-C1 instrument is ~22 % larger than its predicate needs.** 65 of 300 lines are provably removable
without touching the printed predicate or any failure line (235-line candidate, byte-identical across six runs incl.
the full mutant leg and three committed controls), and 8 more items are non-deletable for stated reasons. The size
attack surfaced four falsifiability defects that cost **0 net lines** to fix — unguarded `broken`, decorative
`SEALED50_MIN`, unenforced `SEALED46_TOTAL`, and a silently reversed mutant credited as a kill — plus two carried
numbers the S2 owner should not trust (`broken=12`, and mut-03's kill direction). No edits made; nothing admitted;
next deletion would harm the receipt axis. **Re-checked at close against the drifted live file `850ec790` (§7):
≈ 49 of those 65 lines are still available there, all four defects survive the drift unchanged, and the one item I
withdrew for that design — the mutant short-circuit, now worth ≥ 44 s of a scored run at ~3.7 s per caught mutant
— is a cost trade of +6 lines, not a deletion.**
