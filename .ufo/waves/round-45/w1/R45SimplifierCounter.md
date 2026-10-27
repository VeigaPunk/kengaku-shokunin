# R45SimplifierCounter — `plans/round45_c1_verify.py` (kengaku r45, wave 1)

Seat: simplifier. Axes named: **operability** (primary — the wave-2 seats run this instrument by hand),
**calibration** (the frozen predicate must be provably untouched), **depth** (one authority per rule instead
of two copies that can drift).

Lane untouched: every run used `$S/lane` (a `--shared` clone, toplevel verified) and a patched copy in
`$S/patched`; the lane file still hashes `7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d`
at mtime `2026-10-26_23:00:38`. No lane/corpus/plans file was written; no git/jj mutation anywhere.

## Method

1. AST pass for unused imports / dead locals / self-referential dead stores, over the frozen file (331 lines).
2. Built a patched copy in scratch (`gen.py`, 11 asserted single-occurrence rewrites), `py_compile`-clean,
   `git apply --check` on the clone → rc 0.
3. Expression-level equivalence: `equiv.py` compares every rewritten expression against the original
   formulation on generated inputs (729 path triples; 477 return-code tokens in `DONE_RE`'s language; 1885
   row multisets covering all four verdicts × three open counts and 0–3 rows) → `FAILURES: [] total 0`.
4. End-to-end: four counter runs under `claims/envelope.sh` on the clone (117 fence runs each) in two
   conditions — fence absent (the frozen `control-c1-nothing` state) and a synthetic fence that opens a
   directory under the build scratch but outside `d` (the `READ`/`LEAKED`/`opens=` path the deleted code
   touched). `orig` vs `patched` output slices are **byte-identical** in both conditions.
   Receipts: `R45SimplifierCounter/receipts.md`.

## Answer to the brief, item by item

| asked | finding |
|---|---|
| unused imports | **None.** AST: `UNUSED IMPORTS: [('annotations', 46)]` is `from __future__ import annotations`, not an import. 12 real imports, all used. |
| unused variables | Two. (a) `first` (lines 197/214/221): stored at three sites, loaded only inside its own assignment RHS (`first = first or str(p)`), and absent from all three `return` statements (189, 229, 230) — a pure dead store chain whose `str(p)` also has no effect. (b) `fxs` at line 289: unused loop variable (shadowed by the comprehension at line 281 for the same name). |
| duplicated verdict logic | The per-row tallies are written twice, seven comprehension passes over the same rows: lines 291–293 (refusal: `ADMIT+ERROR`, `HUNG`, `opens`) and 311–314 (honest: `ADMIT and o==0`, `BREACH+ERROR`, `o>0`, `HUNG`). The asymmetry that must survive — an `ERROR` fixture is a **leak** in a refusal module but a **refusal** for an honest fixture — is expressed twice, once per site, with nothing naming it. Replaced by one `count()` pass per pool. |
| keep-log env hook documented? | **No.** The docstring documents `--work` and `--jobs` only; `--help` exposes no flag. It is however *load-bearing* for a scheduled wave-2 seat (`make_wave2_spec.py` → `R45LabratReadProof`: "set K45_KEEP_STRACE to keep logs, cite the log lines"), and it is fatal when `DIR` does not exist: `FileNotFoundError` inside the thread pool → 39-line traceback, no `PINS`/`PREDICATE` line, rc 1 (receipts §4). Documented + `mkdir(parents=True, exist_ok=True)`, not deleted. |

Also removed: the redundant `p == s or` / `p == d or` in the two outside-open predicates (`is_relative_to`
is reflexive), and the dead `mism and` conjunct.

## Patch-ready list (S1–S8) — no edits made to the lane

| # | lines (frozen file) | change | why |
|---|---|---|---|
| S1 | 197, 214, 221 | delete `first = ""` and both `first = first or str(p)` | dead store chain; never returned, never printed |
| S2 | 212, 219 | one `outside(p, scratch, d)` helper replaces two copies of `any(p == s or p.is_relative_to(s) …) and not (p == d or p.is_relative_to(d))` | two authorities for one rule; the `==` legs are implied by `is_relative_to` |
| S3 | 209 | `done.group(1).startswith("E") or …startswith("-")` → `not done.group(1).isdigit()` | `DONE_RE` only admits `-?\d+` or `E[A-Z]+`; the class test is the whole condition |
| S4 | 289, 291–293, 310–314 | `count(rows)` does one pass returning `(verdict counts, opens, fixtures-with-open, admitted-clean)`; honest pool derived from `built["honest"]` instead of scanning `per.items()`; `fxs` → `_fxs` | seven passes → two; the `ERROR`-is-failure asymmetry now lives in two named additions (`c["ADMIT"] + c["ERROR"]`, `c["BREACH"] + c["ERROR"]`) next to each other |
| S5 | after 43 (docstring) | document `K45_KEEP_STRACE=DIR`, the `DIR/f<NNNNN>.txt` naming and that logs are otherwise deleted | the hook the wave-2 prompt instructs seats to use was invisible from the tool |
| S6 | 223–225 | `pathlib.Path(keep).mkdir(parents=True, exist_ok=True)` before the copy | a missing `DIR` currently destroys a whole 117-fence measurement with a traceback |
| S7 | 246 | `if mism and K44_REL in mism:` → `if K44_REL in mism:` | membership on an empty list is already false |
| S8 | 283 | `ex.map(lambda t: run_fence(…, t[1][2], t[0]), enumerate(jobs))` → named `one(item)` unpacking `n, (_g, _f, fx)` | `t[1][2]` silently breaks if the `jobs` tuple shape changes |

Cost: 7 hunks, +37/−19 lines (5 added lines are blank separators), 331 → 349 lines. S8 is cosmetic — drop that
hunk if the L1 prefers the minimum diff; S1–S7 are the substantive items.

Apply from the lane root: `git apply .ufo/waves/round-45/w1/R45SimplifierCounter/round45_c1_verify.simplify.patch`
(sha256 `3396cbbae824b911cde1700d635e947e65dc5f81520512f476f629e0059a9324`; `git apply --check` passes on the
freeze clone).

## Evidence that behaviour is unchanged

| check | result |
|---|---|
| fence absent, original vs frozen control | `297748129f21cf07…` = `297748129f21cf07…` → **PATCHED == FROZEN CONTROL `control-c1-nothing.txt`, byte-identical** (133-line slice, exit 1) |
| synthetic outside-open fence, original vs patched | `4503c32c84bd761a…` both → **byte-identical**; the run shows `REFUSAL f1_gitfile.py READ … opens=1`, `REFUSAL f7_commondir.py LEAKED fixtures=3 admitted=3 … opens=3`, `HONEST fixtures=104 admitted=104 … read=0` |
| expression equivalence | 729 path triples, 477 rc tokens, 1885 row multisets, honest-pool derivation, pin-guard truthiness → `FAILURES: [] total 0` |
| keep hook | original + missing `DIR` → traceback, no verdict line; patched → 117 logs kept, run completes |
| envelope | every run: `local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged` |

## Refused simplifications (deliberately not in the patch)

- **The two `--work` checks (249–258).** The first runs *before* `mkdtemp`; deleting it as "duplicate" would
  create a scratch dir inside the lane before failing — a lane write, which the round's rules forbid.
- **The before/after `PINS` scans (240, 319).** Different assertions: precondition vs no-drift-during-run.
- **Hoisting `mods.mkdir(exist_ok=True)` / `empty.mkdir(exist_ok=True)`** out of `build_module` (32 × 2
  idempotent mkdirs): churn with no measurable gain.
- **Deleting the keep hook.** Load-bearing for a scheduled wave-2 seat; documented and hardened instead.
- **Rewriting the strace parsing (`DONE_RE`/`UNFINISHED_RE`/`RESUMED_RE`) into one parser.** That grammar is
  the instrument's whole judgement; a rewrite would trade a proven parser for an unproven one.
- **`REFUSAL_TOTAL`/`HONEST_TOTAL` vs the discovered counts.** Intentional: advertised constant vs measured
  value, and the predicate fails when they diverge (`rtotal == REFUSAL_TOTAL`).

## Flags for the L1 (frozen behaviour or out of scope — not patched)

1. `UNFINISHED_RE` includes `=\s*\?`, i.e. a syscall whose return strace prints as `?` is counted as
   *never returned*. The honest battery's `read=0` therefore also depends on strace never printing `= ?` for
   an open. Predicate semantics are frozen; flagged, not changed.
2. `admitted=` in the per-module line counts `ERROR` rows (the fence-absent control prints
   `f7_commondir.py LEAKED fixtures=3 admitted=3` for a fence that raised). Correct for the verdict, wrong
   as a label; the printed contract is frozen by the control receipts.
3. Wave-2 spec/counter mismatch: `make_wave2_spec.py` gives `R45MutC1Instrument2` the line "the `dev`/
   `--battery-dir` escape hatches (can a dev flag make the predicate print `pass` on a broken lane?)", but
   this counter exposes only `--lane`, `--work`, `--jobs` (round 44 had `--battery-dir`, `--only`,
   `--build-module`, `--dest`). Either the prompt is stale or the hatch was dropped on purpose — decide
   before that seat runs, or it will report "not found".
4. Keep-log index: `f<NNNNN>.txt` is the job index across both groups (117 runs: 13 refusal fixtures first,
   then 104 honest in `built` order). A wave-2 seat must map it back through the `FENCE-RUN` line order; the
   docstring sentence from S5 should say so if that seat is going to quote logs by index.

## Limits

- Two end-to-end conditions, 117 fence runs each, four runs total; the `HUNG` branch (120 s per fixture) was
  not exercised end-to-end — it is covered by the exhaustive `count()` equivalence only, and no patched line
  is unique to it.
- The synthetic fence is a test double: it proves the counter's *reporting* path (opens → `READ`/`LEAKED`),
  not any real fence's behaviour.
- No fence source exists yet (`plans/fixture_fence.py` absent), so this review says nothing about the fence.

Scratch removed after copying receipts: `python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45SimplifierCounter $S`.

## The patch (verbatim, from `round45_c1_verify.simplify.patch`)

```diff
--- a/plans/round45_c1_verify.py
+++ b/plans/round45_c1_verify.py
@@ -41,6 +41,8 @@
   landing tip.
 
 `--work DIR` puts the scratch root under DIR (it must lie outside the lane); `--jobs N` parallel fence runs.
+`K45_KEEP_STRACE=DIR` copies each fixture's strace log to `DIR/f<NNNNN>.txt` (DIR is created if absent; the
+wave-2 strace read proofs use it); unset, the logs are deleted with the scratch root.
 Exit 0 pass, 1 fail, 2 setup error.
 """
 from __future__ import annotations
@@ -171,6 +173,23 @@
     return out
 
 
+def outside(p, scratch, d):
+    """True when strace reports p under the build scratch but outside the fixture dir d."""
+    return any(p.is_relative_to(s) for s in scratch) and not p.is_relative_to(d)
+
+
+def count(rows):
+    """(verdict counts, outside opens, fixtures with an outside open, fixtures admitted with no outside open)."""
+    c = {}
+    opens = read = adm_clean = 0
+    for _fx, v, _w, o in rows:
+        c[v] = c.get(v, 0) + 1
+        opens += o
+        read += o > 0
+        adm_clean += v == "ADMIT" and o == 0
+    return c, opens, read, adm_clean
+
+
 def run_fence(k44, lane, root, fence_copy, fx, n):
     """One fence decision in a read-only sandbox under strace -f -y -> (verdict, reason, outside_opens)."""
     logdir = root / "strace" / f"s{n:05d}"
@@ -194,7 +213,6 @@
     except OSError:
         lines = []
     pending = {}
-    first = ""
     for line in lines:
         pidm = re.match(r"^\s*(\d+)", line)
         pid = pidm.group(1) if pidm else "-"
@@ -206,22 +224,19 @@
             pending[pid] = line
             continue
         done = DONE_RE.search(line)
-        if not done or done.group(1).startswith("E") or done.group(1).startswith("-"):
+        if not done or not done.group(1).isdigit():
             continue
-        p = pathlib.Path(done.group(2) or "")
-        if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
+        if outside(pathlib.Path(done.group(2) or ""), scratch, d):
             opens += 1
-            first = first or str(p)
     for line in pending.values():
         # an open that never returned (blocked on a FIFO, killed mid-syscall) still touched the path
         for m in re.finditer(r'"(/[^"]+)"', line):
-            p = pathlib.Path(m.group(1))
-            if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
+            if outside(pathlib.Path(m.group(1)), scratch, d):
                 opens += 1
-                first = first or str(p)
                 break
     keep = os.environ.get('K45_KEEP_STRACE')
     if keep:
+        pathlib.Path(keep).mkdir(parents=True, exist_ok=True)
         shutil.copy(log, pathlib.Path(keep) / f'f{n:05d}.txt')
     shutil.rmtree(logdir, ignore_errors=True)
     out = r.stdout.strip()
@@ -243,7 +258,7 @@
         if not os.access(exe, os.X_OK):
             print(f"SETUP {exe} is required", file=sys.stderr)
             return 2
-    if mism and K44_REL in mism:
+    if K44_REL in mism:
         print("SETUP the round-44 counter (builder) is not at its pinned digest", file=sys.stderr)
         return 2
     if a.work:
@@ -279,18 +294,22 @@
                     build_errors[g] += 1
                     print(f"BUILD-ERROR {g} {f.parent.name}/{f.name} {str(e)[:120]}")
         jobs = [(g, f, fx) for g in built for f, fxs in built[g] for fx in fxs]
+        def one(item):
+            n, (_g, _f, fx) = item
+            return run_fence(k44, lane, root, fence_copy, fx, n)
+
         with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
-            res = list(ex.map(lambda t: run_fence(k44, lane, root, fence_copy, t[1][2], t[0]), enumerate(jobs)))
+            res = list(ex.map(one, enumerate(jobs)))
         per = {}
         for (g, f, fx), (verdict, why, opens) in zip(jobs, res):
             per.setdefault((g, f), []).append((fx, verdict, why, opens))
             print(f"FENCE-RUN {g} {fx['module']} {fx['fid']} {verdict} opens={opens}" + (f" -- {why}" if why else ""))
         clean = leaked = read = hung = 0
-        for f, fxs in built["refusal"]:
+        for f, _fxs in built["refusal"]:
             rows = per.get(("refusal", f), [])
-            n_admit = sum(v in ("ADMIT", "ERROR") for _fx, v, _w, _o in rows)
-            n_hung = sum(v == "HUNG" for _fx, v, _w, _o in rows)
-            n_open = sum(o for _fx, _v, _w, o in rows)
+            c, n_open, _read, _clean = count(rows)
+            n_admit = c.get("ADMIT", 0) + c.get("ERROR", 0)
+            n_hung = c.get("HUNG", 0)
             if not rows or n_admit:
                 verdict = "LEAKED"
                 leaked += 1
@@ -307,11 +326,10 @@
         rtotal = len(groups["refusal"])
         print(f"REFUSALS total={rtotal} clean={clean} leaked={leaked} read={read} hung={hung}"
               f" build_errors={build_errors['refusal']}")
-        hrows = [row for (g, _f), rows in per.items() if g == "honest" for row in rows]
-        h_adm = sum(v == "ADMIT" and o == 0 for _fx, v, _w, o in hrows)
-        h_ref = sum(v in ("BREACH", "ERROR") for _fx, v, _w, _o in hrows)
-        h_read = sum(o > 0 for _fx, _v, _w, o in hrows)
-        h_hung = sum(v == "HUNG" for _fx, v, _w, _o in hrows)
+        hrows = [row for f, _fxs in built["honest"] for row in per.get(("honest", f), [])]
+        c, _opens, h_read, h_adm = count(hrows)
+        h_ref = c.get("BREACH", 0) + c.get("ERROR", 0)
+        h_hung = c.get("HUNG", 0)
         print(f"HONEST fixtures={len(hrows)} admitted={h_adm} refused={h_ref} read={h_read} hung={h_hung}"
               f" build_errors={build_errors['honest']}")
         contradicted = rtotal - clean + build_errors["refusal"]
```

VERDICT: simplifications-8
