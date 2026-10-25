writer: KengakuR29-2.FReviewDeterminism-2

# FReviewDeterminism — determinism and portability of `plans/config_projection.py`

Target under attack: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py`
(548 lines, lane master 56fd949a6478342531e61f4feecb4a685d831640, coordinator seat KengakuR29-2).
Attack area assigned: dict ordering, `sort_keys`, locale independence, Python version assumptions
(`ast.unparse` output inside the contract check), behaviour when run from another cwd.

I DID read the production source for this item (allowed by the contract for this review slot).

Everything below was produced by running the instrument read-only and by running my own scripts on
copies under `/tmp`. The lane tree was not modified: `git status --porcelain` in
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` after all probes shows only untracked wave files
(`.ufo/waves/round-29/falsify*`, `.ufo/waves/round-29/scratch/`, `corpus/lessons/round-29.md`);
no tracked file is modified and no `git add/commit/checkout/stash/reset/branch/worktree` was run.
My scratch dir: `.ufo/waves/round-29/scratch/falsify/FReviewDeterminism/upstream_sim.py`.

---

## 1. Attack summary

Seven axes, each probed with a concrete command:

| # | Axis | Probe | Result |
|---|------|-------|--------|
| A1 | byte-level determinism of `--json` | 2 runs + hash seeds | no defect |
| A2 | Python version | 3.8.20, 3.9.25, 3.10.22, 3.11.17, 3.12.15, 3.13.16, 3.14.8, 3.15.0 | **defect D1/D2** |
| A3 | `ast.unparse` contract strings | direct unparse dump on 3.10–3.14 | no defect |
| A4 | locale / encoding | 6 locale+UTF-8 flag combos | no defect (one latent, D4) |
| A5 | hash seed / TZ / warnings | `PYTHONHASHSEED` 0/1/12345/random, `TZ=Asia/Tokyo`, `PYTHONWARNINGS=error` | no defect |
| A6 | cwd independence | cwd = `/`, `/tmp`, `$HOME`, `plans/`, `corpus/`, symlinked entry | no defect |
| A7 | interpreter flags | `python3 -O`, `python3 -OO` | **defect D2/D3** |

---

## 2. Observed facts — axes with no defect found

### 2.1 Byte-level determinism (A1)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ python3 plans/config_projection.py --json | sha256sum
c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630  -
$ cat corpus/evidence/round29-calibration/build-json-sha256.txt
c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630  -
```

My independent rerun reproduces the recorded build receipt **byte for byte** (3,881,049 bytes of
stdout, sha256 as above). `PYTHONHASHSEED=0|1|12345|random` (random twice) all yield the same
sha256 `c8da0c5a…434630`. Reason (code-level): every set that reaches output is either `len()`
only (`set(map(json.dumps, ids))`, `{r["task_index"] …}`) or explicitly `sorted()`
(lines 103, 120, 137, 274, 283, 324, 325); `by_task` (line 309) is a `defaultdict` keyed by integer in
document order. `json.dumps(..., sort_keys=True)` at line 541 sorts every key recursively, so the
`--json` document is fully key-sorted.

### 2.2 Python version matrix (A2) — the *output* is version-stable, the *failure mode* is not

Full `--json` sha256 (same 3,881,049-byte payload) for every interpreter tried:

```
python3.9   3.9.25   c8da0c5a2d3110ef…  rc=0
python3.10  3.10.22  c8da0c5a2d3110ef…  rc=0
python3.11  3.11.17  c8da0c5a2d3110ef…  rc=0
python3.12  3.12.15  c8da0c5a2d3110ef…  rc=0
python3.13  3.13.16  c8da0c5a2d3110ef…  rc=0
python3.14  3.14.8   c8da0c5a2d3110ef…  rc=0
python3.15  3.15.0   c8da0c5a2d3110ef…  rc=0
python3.8   3.8.20   <empty stdout>    rc=1  (traceback; see D2)
```

Seven consecutive CPython releases (3.9 → 3.15) produce byte-identical output, including the
`--selftest` line and exit code. So the *projection* is version-stable; the defects below are in
the failure paths only.

### 2.3 `ast.unparse` contract-check strings (A3)

The contract check compares `ast.unparse()` output against hardcoded spellings at lines 80, 82, 86.
Direct dumps of the pinned generator's AST on 3.10.22 / 3.11.17 / 3.12.15 / 3.14.8 (identical):

```
('assign', 'data = json.loads(raw)')
('for.target', '(idx, item)')
('for.iter', 'enumerate(data)')
('fstring', ["f'config_files/{idx}.json'"])
```

3.9.25 and 3.15.0 pass the same check (their `--json` sha equals the matrix value above).
**No mismatch observed on any interpreter available on this host.** The literal comparisons at
lines 80/82/86 therefore do not misfire today.

### 2.4 Locale independence (A4)

Identical `--json` sha256 `c8da0c5a…434630` under: default (`LANG=en_US.UTF-8`), `LC_ALL=C`,
`LC_ALL=C PYTHONCOERCECLOCALE=0 PYTHONUTF8=0` (true ASCII locale, no coercion), `LC_ALL=C.utf8`,
`LC_ALL=en_US.utf8`, `TZ=Asia/Tokyo`, `PYTHONWARNINGS=error`, `python3 -O`.

Supporting measurements on the pinned bytes: raw fixture 880,776 bytes, **0 bytes > 127**,
**0 CR**, no BOM, ends with LF; manifest, profiles.json and all four hand fixtures are 0 non-ASCII
bytes. The instrument's own LIMIT line about the ASCII/locale difference is therefore factually
true, and `json.dumps` defaults (`ensure_ascii=True`) keep stdout pure ASCII in both modes.

### 2.5 cwd independence (A6)

Identical `--json` sha256 from cwd `/`, `/tmp`, `/home/vgpnk`, `…/kengaku-shokunin/plans`,
`…/kengaku-shokunin/corpus`, and via a symlinked entry point (`/tmp/cp_link.py` → the script).
Default `--root` is `Path(__file__).resolve().parents[1]` (line 526), i.e. absolute and
symlink-resolved; all pinned paths are joined to it. Neither output mode leaks an absolute path:
`grep -c "/home/vgpnk"` on `--json` and on `--summary` both return **0**.

### 2.6 Digest faithfulness of the two recorded digests (cross-check)

I re-implemented the pinned generator's write path verbatim (same six ordered `str.replace` calls,
same `json.dump(item, f, indent=2)`, same text-mode `open`) in
`.ufo/waves/round-29/scratch/falsify/FReviewDeterminism/upstream_sim.py`, writing only into
`/tmp/r29det/up*`:

```
TESTJSON_SHA 2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4   (upstream-written test.json)
TOOL projected_text_sha256 2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4
TASK_SHA {"0": 9533088e31…, "1": 56613039d9…, "2": 534679e10c…, "405": d5b7b5e8ab…, "811": 18523f7571…}
TOOL would_be_file_sha256 {"0": 9533088e31…, "1": 56613039d9…, "2": 534679e10c…, "405": d5b7b5e8ab…, "811": 18523f7571…}
```

Both recorded digests equal the digests of the bytes the upstream script actually writes, and the
upstream bytes are identical under an ASCII locale and a UTF-8 locale (`diff -r` of the two
simulated trees: no differences).

---

## 3. Defects

### D1 — `python3 -O` silently voids every self-check; the selftest still reports "clean" (severity: medium)

**Location:** all 20 selftest assertions — lines 396, 397, 398, 403, 404, 410, 411, 416, 417, 422,
424, 431, 438, 442, 448, 449, 450, 451, 456, 457, 461, 466, 470, 483, 515 — plus the production
assertions at lines 177, 186, 192, 196.

`assert` statements are removed by `-O`/`-OO`. The selftest appends to `cases` *outside* the
asserts, so the report line and the exit code are produced by a run in which **no assertion was
evaluated**. Demonstration on a copy under `/tmp` (`/tmp/r29det/cp_sabotage.py`, one line inserted
after `cases = []`):

```
$ python3  /tmp/r29det/cp_sabotage.py --root <lane> --selftest
AssertionError: SABOTAGE: verification disabled
rc=1

$ python3 -O /tmp/r29det/cp_sabotage.py --root <lane> --selftest
SELFTEST clean cases=20 six_tokens_and_non_url_field,units_not_pooled,…,cli_manifest_tampered
rc=0
```

The `-O` run prints the *byte-identical* "clean" line as a fully verified run. The production
receipt `corpus/evidence/round29-calibration/build-selftest.txt` contains exactly that string plus
`exit=0` and records no interpreter flags, so **the receipt cannot distinguish "20 checks passed"
from "0 checks executed"**.

Consequence for the prereg requirement (plans/round-29-claims.md, Tool interface section:
test findings and exits checked): the selftest receipt is not self-validating. [INFERENCE] The
build-seat run was most likely a normal `python3` run, because my own normal run reproduces the
receipt byte for byte and the `-O` output is identical — but the receipt text alone cannot prove
it.

Second-order effect of the same flag: the production asserts in `string_spans` (lines 177, 186,
192, 196) are the only structural validation of the JSON text. Under `-O` they disappear, so a
malformed (non-sha-pinned) input would silently yield wrong spans instead of the exit-2
`input_invalid` finding that lines 538–539 currently produce via `AssertionError`.

### D2 — Python < 3.9 crashes with an uncaught `AttributeError`, exit 1 (severity: medium)

**Location:** `plans/config_projection.py:80` — `ast.unparse(statement)`; also lines 82 and 86.
`ast.unparse` was added in CPython 3.9.

```
$ python3.8 plans/config_projection.py --json
  File "plans/config_projection.py", line 80, in source_contract
    elif isinstance(statement, ast.Assign) and ast.unparse(statement) == "data = json.loads(raw)":
AttributeError: module 'ast' has no attribute 'unparse'
rc=1     stdout length = 0 bytes
```

The prereg declares the tool "stdlib" only, with no version floor, and the shebang is
`#!/usr/bin/env python3`, so the interpreter is whatever `python3` resolves to first on `PATH`.
On a host with python3 < 3.9 the instrument does not report "could-not-evaluate"; it aborts with
a traceback and **exit 1**.

### D3 — `python3 -OO` crashes before any work, exit 1 (severity: medium)

**Location:** `plans/config_projection.py:525` — `argparse.ArgumentParser(description=__doc__.splitlines()[0])`.
`-OO` strips docstrings, so `__doc__` is `None`.

```
$ python3 -OO plans/config_projection.py --summary
AttributeError: 'NoneType' object has no attribute 'splitlines'
rc=1
$ python3 -OO plans/config_projection.py --json
AttributeError: 'NoneType' object has no attribute 'splitlines'
rc=1
```

Both output modes fail identically; the parser is built before the `try` block, so the failure
is not caught at all.

### D4 — Unhandled environment errors are reported with exit 1, the code the prereg reserves for "projection/invariant finding" (severity: medium)

**Location:** `plans/config_projection.py:538` — `except (OSError, ValueError, KeyError, TypeError, AssertionError, IndexError) as error:`

`AttributeError` (D2, D3) and `RecursionError`/`MemoryError` are not in that tuple, so an
environment-level failure escapes as an uncaught exception: **stdout is empty (0 bytes)** and the
exit code is 1. The prereg (`plans/round-29-claims.md` lines 53–54) defines exit 1 as
"projection/invariant finding" and exit 2 as "could-not-evaluate including … unrecognized source
contract", with "CLI usage2". A crash that prints nothing on stdout but exits 1 is
indistinguishable, to a machine consumer of `--json`, from "the audit ran and found a finding".
A consumer that parses stdout as JSON sees an empty document rather than a finding object.

### D5 — `--summary` and `--json` order the same dictionaries differently (severity: low)

**Location:** `plans/config_projection.py:368` (`original_occurrences_by_token`, no `sort_keys`),
line 376 (`applied_replacements`, no `sort_keys`), line 380 (explicitly
`sort_keys=key != "changed_leaves_by_token" and key != "changed_tasks_by_token"`), versus line 541
(`json.dumps(result, sort_keys=True, …)`).

Observed for the same profile:

```
--summary: changed_leaves_by_token={"__GITLAB__": 385, "__REDDIT__": 323, "__SHOPPING__": 275, "__SHOPPING_ADMIN__": 300, "__WIKIPEDIA__": 0, "__MAP__": 133}
--json   : ['__GITLAB__', '__MAP__', '__REDDIT__', '__SHOPPING_ADMIN', '__SHOPPING__', '__WIKIPEDIA']
```

Both modes are internally deterministic, and the `--json` document is fully key-sorted; the
divergence is only between modes, so the two outputs cannot be compared key-by-key or diffed
mechanically. The summary deliberately keeps generator `ORDER` for token-keyed maps (line 380) and
loses that order in `--json`.

### D6 — Locale-dependent text decoding inside the selftest path (severity: low, currently inert)

**Location:** `Path.read_text()` without an `encoding=` argument at lines 436, 444, 445, 453, 460;
`Path.write_text()` without an `encoding=` argument at line 497; `subprocess.run(…, text=True)`
at line 482 (decodes the child's stdout with the locale encoding, not UTF-8).

These use `locale.getpreferredencoding(False)`, whereas the pinned inputs are decoded explicitly as
UTF-8 (`verified[RAW].decode("utf-8")`, line 352). Measured today: every file read that way is
100 % ASCII (0 non-ASCII bytes in the four hand fixtures, manifest and profiles.json), and the
selftest passes under `LC_ALL=C LANG=C PYTHONCOERCECLOCALE=0 PYTHONUTF8=0` with exit 0 — so the
difference is inert *for the current fixtures*. It is a latent locale coupling in exactly the
place the tool claims locale independence.

---

## 4. Residual risk and verification gaps

- R1 — The contract check couples to CPython's *unparser formatting* rather than to the AST
  (lines 80, 82, 86 compare `ast.unparse()` output against fixed spellings). Measured identical
  on 3.9–3.15 for the pinned generator, but any future CPython formatting change, or a
  re-spelling of the pinned `data = json.loads(raw)` line, would surface as
  `source_contract_unrecognized` → exit 2, i.e. as "could-not-evaluate" rather than as a real
  contract change. [INFERENCE] Low likelihood, low impact.
- R2 — `PYTHONOPTIMIZE`/`-O` is not recorded in any receipt. The receipt
  `build-selftest.txt` cannot prove that assertions ran (D1). The build seat's own environment is
  not observable from the lane tree.
- R3 — The `--root` argument accepts a relative path, which is then resolved against the current
  cwd. Only the default (script-relative, absolute) is cwd-independent; verified in §2.5.
- R4 — Python 3.8 was tested through `uv`-provisioned CPython 3.8.20; no other <3.9 interpreter
  (PyPy 3.8, GraalPy) was available offline for the same probe, and `ast.unparse` is absent in
  both, so the same `AttributeError` path is expected there. [INFERENCE]
- R5 — Not probed (out of my assigned area): runtime behaviour of the produced `config_files/*.json`
  upstream would write, WebArena task validity, and any browser/helper interaction. The instrument
  writes nothing; my upstream simulation writes only under `/tmp`.
- R6 — The three profile orderings, the occurrence provenance and the index/task_id mapping were
  not re-derived here (other falsify items own those); my checks were restricted to
  determinism/portability of the emitted bytes and digests.

---

## 5. Tooling record

| tool | version | channel | reason |
|------|---------|---------|--------|
| `uv python install 3.9 3.8` | CPython 3.9.25, CPython 3.8.20 (python-build-standalone, Astral official uv channel) | uv (no pacman transaction; pacman is PAUSED host-wide and was not used) | probe the `ast.unparse` (3.9+) floor of the contract check |
| uv-managed CPython already present | 3.10.22, 3.11.17, 3.12.15, 3.13.16, 3.15.0 | pre-installed, no change | cross-version determinism matrix |
| system CPython | 3.14.8 | pre-installed, no change | lane interpreter |

No packages were installed via pacman, no host service was restarted, no credential, cookie,
auth-state value or private URL was read or recorded.

---

## 6. Scoped verdict

Determinism of the emitted bytes is **not** refuted: the `--json` document is byte-identical across
CPython 3.9→3.15, all six locale/UTF-8 combinations tested, four `PYTHONHASHSEED` values, two
`TZ` values, five working directories and a symlinked entry point, and it reproduces the recorded
build receipt sha256 `c8da0c5a…434630` exactly. The `ast.unparse` contract strings match on every
interpreter available. The two recorded digests (`projected_text_sha256`,
`would_be_file_sha256`) equal the digests of the bytes the upstream generator actually writes.

Portability is **partly** refuted, with four concrete defects and one latent one:
D1 (`-O` voids all self-checks while still printing "clean", which makes the recorded selftest
receipt non-self-validating), D2 (Python < 3.9 → uncaught `AttributeError`, exit 1),
D3 (`-OO` → uncaught `AttributeError` at line 525, exit 1), D4 (uncaught environment errors
consume the prereg's exit-1 "finding" slot instead of exit-2 "could-not-evaluate", with empty
stdout), D5 (`--summary`/`--json` key-order divergence), D6 (locale-dependent `read_text()`/
`write_text()`/`text=True` in the selftest path).

Scope: this verdict covers this item only (determinism and portability of
`plans/config_projection.py`). It is not a round-29 admission and not an integration decision.

VERDICT: PARTIAL
