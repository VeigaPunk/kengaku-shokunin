# R32 MutCounters — mutation test of the round-32 counters

- Role: UFO-FSD mutation tester (leaf, no subagent dispatch).
- Date: 2026-10-25. Lane: `kengaku-shokunin` (read-only; no files under the lane were created/edited except this report).
- Targets: `plans/round32_defects.py` (C2 counter) and `plans/catalog_probe.py` (C3 counter).
- Detector: `python3 <copy> --selftest` (exit 0 = green/PASS, exit 1 = red/FAIL). Battle copies in `/tmp/r32-R32MutCounters/` (272K total, < 60 MB cap).
- No tools installed/updated this run (nothing needed; `python3` present). No lane bytes touched.

## Baseline (pristine)

Copies byte-identical to the pinned lane sources (hashes equal those of `plans/` at read time):

| file | sha256 |
|---|---|
| round32_defects.py (lane == pristine == restored) | `4edb2796dae68caad52e26ec791dc070c43c90263d2304af8cdbf4f6acf0ecb8` |
| catalog_probe.py (lane == pristine == restored) | `731abfe03bd6a0dd0a1b84cbf7e6536d4272151ef98014a13911779811328dea` |

Pristine runs:

```
$ python3 round32_defects.py --selftest
CASE registry-complete PASS
CASE R1-red-on-empty PASS
CASE R2-red-on-empty PASS
CASE R3-red-on-empty PASS
CASE R4-red-on-empty PASS
CASE R5-red-on-empty PASS
CASE R6-red-on-empty PASS
CASE R7-red-on-empty PASS
SELFTEST checks=7 failed=0
EXIT=0

$ python3 catalog_probe.py --selftest
CASE hf-parses PASS
CASE hf-missing-detected PASS
CASE or-parses PASS
CASE or-missing-detected PASS
CASE entry-missing-red PASS
CASE entry-current-green PASS
SELFTEST checks=6 failed=0
EXIT=0
```

## Mutants — round32_defects.py (C2 counter)

### M1 — delete the frozen R7 check from `CHECKS` (survived)

Mutation: remove `("R7", "round30-peer-review-erratum", check_r7),` from `CHECKS` (the whole frozen-item 7 vanishes from the counter; `FROZEN` is derived from `CHECKS`, so the registry check stays self-consistent). Post-mutation sha256 `f4a8e5f7…`.

```
$ python3 round32_defects_M1.py --selftest
CASE registry-complete PASS
CASE R1-red-on-empty PASS
CASE R2-red-on-empty PASS
CASE R3-red-on-empty PASS
CASE R4-red-on-empty PASS
CASE R5-red-on-empty PASS
CASE R6-red-on-empty PASS
SELFTEST checks=6 failed=0
EXIT=0
```

**Survived.** Selftest cannot tell that a frozen check was dropped: `registry-complete` compares `FROZEN` against a tuple re-derived from the same `CHECKS` (tautology — it can never fail for this mutation class), and no case asserts the count `checks=7`. With this mutant the real counter prints `checks=6 defects=0` and exits 0 on a tree where R7 is still un-repaired → false green against the frozen C2 predicate (which names exactly seven checks).

### M2 — tautologise `near()` to always `True` (survived)

Mutation: `near()` body replaced by `return True` (all co-occurrence checks report "found"; the content-level acceptance tests of R1/R5/R6/R7 become vacuous). Post-mutation sha256 `1e4008cd80…`.

```
$ python3 round32_defects_M2.py --selftest
CASE registry-complete PASS
CASE R1-red-on-empty PASS
CASE R2-red-on-empty PASS
CASE R3-red-on-empty PASS
CASE R4-red-on-empty PASS
CASE R5-red-on-empty PASS
CASE R6-red-on-empty PASS
CASE R7-red-on-empty PASS
SELFTEST checks=7 failed=0
EXIT=0
```

**Survived.** The selftest never exercises `near()`'s semantics: every `*-red-on-empty` case returns red *before* reaching the `near()` call (missing-file guard), so a vacuous `near()` is invisible to the detector. In real use this mutant makes R1/R5/R6/R7 accept repair text that does not actually co-occur.

### M3 — neuter `check_r1`'s missing-file branch to green `return ""` (survived)

Mutation: `if not R31_REPORT.is_file(): return f"...unreadable..."` → `return ""` (the check is a silent no-op whenever the report is absent). Post-mutation sha256 `803724516153…`.

```
$ python3 round32_defects_M3.py --selftest
CASE registry-complete PASS
CASE R1-red-on-empty PASS
CASE R2-red-on-empty PASS
CASE R3-red-on-empty PASS
CASE R4-red-on-empty PASS
CASE R5-red-on-empty PASS
CASE R6-red-on-empty PASS
CASE R7-red-on-empty PASS
SELFTEST checks=7 failed=0
EXIT=0
```

**Survived — and reveals a non-hermetic selftest.** `R31_REPORT`/`R32_REPORT` are *absolute fleet paths* (`FLEET / ".ufo/reports/round-31/kengaku.md"`), so the "red-on-empty" cases for R1/R2 do not test an isolated empty tree; they read the live fleet reports. Probe: on an empty temp dir, both pristine and M3 `check_r1` return the same real-bytes verdict `'no appended erratum supersedes the a44b5a8 citation'` (the round-31 report currently fails R1's content check, keeping the case red for the wrong reason). The mutated branch is therefore never exercised while the real report exists. This also implies the R1/R2 red-on-empty cases **flip to red (selftest FAILs) once the C2 repairs actually land** — when the round-31 report carries the superseding erratum + `ae95fe0` and the round-32 report exists citing the tip, pristine `check_r1`/`check_r2` return `""` ⇒ `red=False` ⇒ `R1-red-on-empty`/`R2-red-on-empty` fail. The selftest is state-coupled to the very defects it guards and is expected to report red on the completed claim.

### M4 — delete `check_r6`'s missing-file guard (crash-path) (survived)

Mutation: remove `if not lesson31.is_file(): return "..."`, so on an empty tree `read()` raises `FileNotFoundError`. Post-mutation sha256 `150ddb61d771…`.

```
$ python3 round32_defects_M4.py --selftest
CASE registry-complete PASS
CASE R1-red-on-empty PASS
CASE R2-red-on-empty PASS
CASE R3-red-on-empty PASS
CASE R4-red-on-empty PASS
CASE R5-red-on-empty PASS
CASE R6-red-on-empty PASS
CASE R7-red-on-empty PASS
SELFTEST checks=7 failed=0
EXIT=0
```

**Survived.** `except Exception: red = True` means a check that crashes (e.g. a NameError regression, or this guard removal) is indistinguishable from a check that legitimately reports red. A regression turning a check into a crash passes the selftest.

## Mutants — catalog_probe.py (C3 counter)

### M1 — delete the `entry-missing-red` selftest case (survived)

Mutation: remove `cases.append(("entry-missing-red", entry_ok(lane) != "ok"))`. Post-mutation sha256 `835e7b2a58ba…`.

```
$ python3 catalog_probe_M1.py --selftest
CASE hf-parses PASS
CASE hf-missing-detected PASS
CASE or-parses PASS
CASE or-missing-detected PASS
CASE entry-current-green PASS
SELFTEST checks=5 failed=0
EXIT=0
```

**Survived.** No case-count assertion: dropping a guard case (here the "missing entry is red" invariant) goes unnoticed.

### M2 — tautologise `parse_hf`'s missing-field filter (killed)

Mutation: `[field for field in HF_FIELDS if field not in first]` → `[field for field in HF_FIELDS if False]` (missing-field detection disabled — the counter would print `hf_schema_delta=0` even for a schema-shifted HF response). Post-mutation sha256 `075a953919ba…`.

```
$ python3 catalog_probe_M2.py --selftest
CASE hf-parses PASS
CASE hf-missing-detected FAIL
CASE or-parses PASS
CASE or-missing-detected PASS
CASE entry-missing-red PASS
CASE entry-current-green PASS
SELFTEST checks=6 failed=1
EXIT=1
```

**Killed.** `hf-missing-detected` catches the loss of schema-delta detection.

### M3 — delete the empty-OpenRouter-list guard (survived)

Mutation: remove `if not models: raise ValueError("OpenRouter model list is empty")` (an empty `data` list now proceeds to `models[0]` → `IndexError` in real probe runs instead of a clean failure; in main mode the exception is swallowed into `status=fail:` regardless, so the counter's exit behavior is unchanged either way). Post-mutation sha256 `65f1e8511dcb…`.

```
$ python3 catalog_probe_M3.py --selftest
CASE hf-parses PASS
CASE hf-missing-detected PASS
CASE or-parses PASS
CASE or-missing-detected PASS
CASE entry-missing-red PASS
CASE entry-current-green PASS
SELFTEST checks=6 failed=0
EXIT=0
```

**Survived.** No selftest case feeds an empty OpenRouter model list; the empty-list guard is untested.

### M4 — neuter `entry_ok` to always `"stale"` (killed)

Mutation: `return "ok" if ok else "stale"` → `return "stale"` (entry never accepted). Post-mutation sha256 `15ccaed69275…`.

```
$ python3 catalog_probe_M4.py --selftest
CASE hf-parses PASS
CASE hf-missing-detected PASS
CASE or-parses PASS
CASE or-missing-detected PASS
CASE entry-missing-red PASS
CASE entry-current-green FAIL
SELFTEST checks=6 failed=1
EXIT=1
```

**Killed.** `entry-current-green` catches the neutered entry acceptance.

## Summary

| script | mutant | type | selftest exit | verdict |
|---|---|---|---|---|
| round32_defects.py | M1 delete R7 from CHECKS | delete check | 0 | survived |
| round32_defects.py | M2 `near()` → True | tautologise | 0 | survived |
| round32_defects.py | M3 check_r1 branch → `""` | neuter branch | 0 | survived |
| round32_defects.py | M4 check_r6 guard removed | neuter branch | 0 | survived |
| catalog_probe.py | M1 drop entry-missing-red case | delete case | 0 | survived |
| catalog_probe.py | M2 parse_hf filter → False | tautologise | 1 | killed |
| catalog_probe.py | M3 drop empty-list guard | neuter branch | 0 | survived |
| catalog_probe.py | M4 entry_ok → "stale" | neuter branch | 1 | killed |

Killed 2/8. Survivors: 6/8.

## Selftest defects surfaced (coverage findings)

1. **`round32_defects.py` selftest kills 0/4.** It tests only (a) a tautological registry self-equality (`FROZEN` derived from `CHECKS`) and (b) "each check is red on an empty tree". It cannot detect: a dropped frozen check, a vacuous `near()`, a neutered branch (when masked by real bytes), or a check that crashed instead of reporting red. All four planted defects would produce false-green `defects=0` exits on unrepaired trees.
2. **Non-hermetic red-on-empty cases (R1/R2).** They read absolute fleet report paths, not the empty temp lane. Currently they pass only because the real round-31/round-32 reports are still in a defect state; once the C2 repairs land, pristine `--selftest` will flip red (`R1-red-on-empty`/`R2-red-on-empty` will fail). The selftest is state-coupled to the claim's own repair progress.
3. **Crash == red.** `except Exception: red = True` conflates a check that raises with a check that legitimately reports red; a regression that makes a check crash passes.
4. **`catalog_probe.py` selftest is asymmetric:** schema-delta detection (M2) and entry acceptance (M4) are guarded, but case deletion is undetected (M1) and the empty-OpenRouter guard is untested (M3). Main-mode exit logic (`probe()`/`fetch()`/the final `status == "ok"` conjunction) is not exercised by the selftest at all.

## Restoration evidence

After each mutant run the working copies were restored from `pristine_*` and re-run:

```
$ sha256sum round32_defects.py catalog_probe.py
4edb2796dae68caad52e26ec791dc070c43c90263d2304af8cdbf4f6acf0ecb8  round32_defects.py
731abfe03bd6a0dd0a1b84cbf7e6536d4272151ef98014a13911779811328dea  catalog_probe.py
$ python3 round32_defects.py --selftest; echo EXIT=$?
CASE registry-complete PASS
CASE R1-red-on-empty PASS
CASE R2-red-on-empty PASS
CASE R3-red-on-empty PASS
CASE R4-red-on-empty PASS
CASE R5-red-on-empty PASS
CASE R6-red-on-empty PASS
CASE R7-red-on-empty PASS
SELFTEST checks=7 failed=0
EXIT=0
$ python3 catalog_probe.py --selftest; echo EXIT=$?
CASE hf-parses PASS
CASE hf-missing-detected PASS
CASE or-parses PASS
CASE or-missing-detected PASS
CASE entry-missing-red PASS
CASE entry-current-green PASS
SELFTEST checks=6 failed=0
EXIT=0
```

Restored hashes equal the baseline and the (unchanged, read-only) lane sources; `plans/round32_defects.py` / `plans/catalog_probe.py` on disk still hash to `4edb2796…` / `731abfe0…`. Nothing outside `/tmp/r32-R32MutCounters/` and this report was written.

VERDICT: survivor

## Postscript (2026-10-25, after peer coordination with R32CritC2)

The lane `plans/round32_defects.py` moved after this report's snapshot
(`4edb2796…`/248 lines → `5c22ebef…`/267 → `06428915…`/269 lines, verified read-only).
At 269 lines the owner has CLOSED the R1/R2 state-coupling finding (M3): the generic
loop now `continue`s on R1/R2 (`if item_id in ("R1","R2"): continue`, live :229-230) and
three synthetic fixture cases (`R1-red-without-erratum`, `R1-green-with-erratum`,
`R2-red-missing-report`) replace the absolute-fleet-path red-on-empty cases. The registry
tautology finding (M1) remains OPEN at 269: `FROZEN` is still derived from `CHECKS`
(:204) and main's guard (:251) still compares two tuples rebuilt from the same list, so a
renamed/deleted R7 row passes `registry-complete` and prints no `DEFECT registry:` line
(checks=6 defects=0 on a repaired tree). Fix shape agreed with the critic: literal frozen
tuple plus `len(CHECKS)==7`. My M2 (`near()`→True) remains a survivor in the fixed shape —
token-proximity predicates need non-empty violating fixtures in the selftest to catch that
class (R5/R6/R7 still have zero non-empty coverage at 269).
