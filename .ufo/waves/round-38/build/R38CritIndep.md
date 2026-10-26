# R38CritIndep — independent recompute of the tb2 `build-pmars` probe

Seat: critic (R38CritIndep), kengaku round 38 wave 1, 2026-10-26.
Freeze commit `e0a378539a45cc9388c66cfba22f44275131de23`; first recorded probe run `e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b`.
Work tree: `git clone --shared` of the lane at `/fast/scratch/hyaku/kengaku-r38/R38CritIndep/lane`
(`rev-parse --show-toplevel` = that path), removed after the receipts were copied here.
No lane file was written; every artefact below lives in this report dir or was deleted with the scratch tree.

## 0. Axes

| axis | question this seat moves | result |
|---|---|---|
| calibration | do the 22 frozen predictions follow from `test_outputs.py` alone, and does the receipt reproduce? | **22/22 agree**, replay byte-identical to the receipt |
| coverage | is the capture the pinned upstream bytes, and does the grader see a genuine build as passing? | **5/5 captures equal upstream**; oracle shape = PPPP |
| depth | are the extra tolerances in the grader's mechanism, not in the model? | 3/3 extras predicted then observed, each mechanism checked directly |
| operability | can the wave-2 scribe fill the V7 requirement map without guessing? | all 7 labels derived and tabulated (§6.3) |

## 1. Method, and the independence disclosure (read this first)

1. I read the frozen grader `corpus/evidence/round38/tb2-build-pmars/test_outputs.py` in full and, from it alone,
   wrote the derivation table in `R38CritIndep/predictions.md` (file written **02:46**, before
   `plans/build_pmars_probe.py` was opened; the probe's `CASES` table and its `predicted=` fields were read afterwards).
2. **Caveat, stated plainly:** the 22 case descriptions I was told to predict from
   (`corpus/evidence/round38/build-pmars-dry-cases-freeze.txt`) carry the author's own `predicted=`/`tests=`
   columns in the same line. Those columns were therefore visible while I derived. My check is independent of the
   probe's `CASES` code and of the receipt's `observed=` column; it is **not** independent of the author's
   prediction text. The comparison below is against `observed=`, the thing the receipt claims to have run.
3. Then I re-ran the frozen probe twice in the clone and compared bytes with the frozen receipt.
4. Then I built three extra cases of my own (predictions written before the run), plus one non-assigned
   oracle-shape cross-check, in a copy of the probe in the clone.

Derivation rules taken from `test_outputs.py` (line numbers of the frozen capture):

- T1 `test_pmars_works` (`:19`): `assert binary.exists()` at `/usr/local/bin/pmars` (`:24`); two debugger runs must
  each yield `>= 2` matches of `r"\b(\d{5})\s+\w+\.\w+"` (`:31-38`); the battle command's `tail -n 1` must satisfy
  `re.match(r"Results: \d+ \d+ \d+", …)` (`:46`). `run_shell_command` (`:9-17`) `.strip()`s stdout and, on
  `CalledProcessError`, returns `e.output` **iff non-empty** (`:13-14`), else raises.
- T2 `test_headless_no_x11` (`:51`): `ldd /usr/local/bin/pmars` stdout must contain none of
  `libX11/libXt/libXext/libXaw` (`:54-57`). An `ldd` failure with empty stdout raises.
- T3 `test_debian_source_used` (`:60`): `Path("/app").glob("pmars-*")` non-empty (`:62`), first hit's
  `debian` `.exists()` (`:70`).
- T4 `test_built_from_source` (`:73`): same glob (`:75`), `src` exists, `list(src.glob("*.c"))` non-empty (`:84`).
- Order is file order T1,T2,T3,T4; `test.sh:25-29` maps pytest exit 0 → reward 1, else 0, so any non-`PPPP`
  letter string is a task failure.

## 2. Blind derivation, 22/22

`tests` = letters in T1..T4 order. `observed` is the frozen receipt line
(`corpus/evidence/round38/build-pmars-probe.txt`).

| case | my prediction | observed | agree | the one mechanism that decides it |
|---|---|---|---|---|
| empty-tree | FFFF | FFFF | ✓ | no binary (`:24`), `ldd` empty-stdout error, empty `/app` |
| canned-shape | PPPP | PPPP | ✓ | canned stdout + dynamic link + `debian/` + `dummy.c` |
| canned-script | PFPP | PFPP | ✓ | `ldd` prints "not a dynamic executable" on stderr, stdout empty → raise |
| canned-static | PFPP | PFPP | ✓ | static: `ldd` exits 1, stdout empty → raise |
| canned-x11-linked | PFPP | PFPP | ✓ | `libX11` in `ldd` stdout (`:57`) |
| canned-x11-dlopen | PPPP | PPPP | ✓ | no `DT_NEEDED` for `ldd` to list |
| results-two-ints | FPPP | FPPP | ✓ | two ints < three (`:46`) |
| results-trailing-text | PPPP | PPPP | ✓ | `re.match` anchors the start only |
| results-not-last | FPPP | FPPP | ✓ | `tail -n 1` sees the extra line |
| results-negative | FPPP | FPPP | ✓ | `\d+` cannot match `-1` after `Results: ` |
| one-address | FPPP | FPPP | ✓ | needs `>= 2` (`:35`) |
| four-digit-address | FPPP | FPPP | ✓ | `\d{5}` unsatisfied |
| canned-exit-nonzero | PPPP | PPPP | ✓ | `e.output` non-empty returned (`:14`) |
| nonexec-binary | FPPP | FPPP | ✓ | `exists()` true, shell 126 with empty stdout → raise |
| silent-binary | FPPP | FPPP | ✓ | no addresses |
| path-split | PPPP | PPPP | ✓ | `/usr/local/sbin` precedes `/usr/local/bin`; `ldd` reads the silent one |
| no-debian-dir | PPFP | PPFP | ✓ | T3 only |
| debian-is-file | PPPP | PPPP | ✓ | `Path.exists()` on a regular file |
| src-no-c | PPPF | PPPF | ✓ | `glob("*.c")` empty |
| c-is-dir | PPPP | PPPP | ✓ | `glob` matches directories |
| no-src-dir | PPPF | PPPF | ✓ | `src` missing |
| pmars-dir-elsewhere | PPFF | PPFF | ✓ | `/app/pmars-*` glob is one level deep |

Aggregate derived independently: pass 7 (canned-shape, x11-dlopen, trailing-text, exit-nonzero, path-split,
debian-is-file, c-is-dir), fail 15 — the receipt's `observed_pass=7 observed_fail=15`. **Agreement 22/22.**

## 3. Replay of the frozen probe (independent clone, independent host run)

```
$ cd "$S/lane" && python3 plans/build_pmars_probe.py --lane . --work "$S/w"   # (byte copy: xp_base.py)
$ cmp replay1.txt "$S/lane/xreceipt_frozen.txt"   → REPLAY==FROZEN-RECEIPT
$ cmp replay1.txt replay2.txt                      → REPLAY1==REPLAY2
$ python3 xp_base.py --lane . --dry | cmp - corpus/evidence/round38/build-pmars-dry-cases-freeze.txt → DRY==FROZEN
```

`plans/build_pmars_probe.py` = `32f0771c…24a`, dry table = `93b4b60c…df0` (both equal the C2 counter's pins),
`SHA256SUMS` in the capture verifies (`sha256sum -c` → 5 × OK). Receipt copied here as
`R38CritIndep/probe-replay.txt`. So P10's "fresh probe output is byte-equal to the receipt" is reproducible
outside the author's tree.

## 4. Three extra cases (predicted in `predictions.md` before the run)

Run: `python3 xcases_r38.py . "$S/w"` (driver in the clone; imports the byte-copied probe module unmodified,
extends only the staging: symlink and a real ELF under `/app`; grader capture untouched). Receipt:
`R38CritIndep/extras.txt`.

| cid | staged state | predicted | observed | mechanism |
|---|---|---|---|---|
| `x-results-leading-space` | battle output `   Results: 12 34 78` | PPPP | **PPPP** ✓ | `run_shell_command` `.strip()`s the pipeline output before `re.match` |
| `x-debian-broken-symlink` | `/app/pmars-0.9.4/debian` → `missing-target`, `src/dummy.c` present | PPFP | **PPFP** ✓ | `Path.exists()` follows the link → `False` |
| `x-app-pmars-binary` | `/app/pmars` is a working canned ELF; no `/app/pmars-*` | PPFF | **PPFF** ✓ | the glob is the prefix `pmars-*`, so a file named `pmars` is invisible to T3/T4 |

Mechanism checks run directly (not through the sandbox), verbatim output:

```
strip-out='Results: 12 34 78' match=True        # after .strip() the leading spaces are gone
raw-out='   Results: 12 34 78\n' match=False    # without .strip() the regex would reject it
dangling exists()=False is_symlink=True
glob(pmars-*)=[] glob(pmars*)=['pmars']
```

**3/3 predicted correctly.** What the three add to the frozen 22 (instance-level, none contradicts the receipt):

1. leading whitespace on the results line is free — the `.strip()` in `run_shell_command` (`:10`) is a second
   anchor tolerance beside `re.match`; a `Results:` line indented by any amount still passes;
2. the `debian/` check is existence-only *through* symlinks: a dangling `debian` fails, but `debian` → any
   existing directory (e.g. `/usr/share`) passes; the frozen `debian-is-file` case shows only the regular-file case;
3. the built binary may sit at `/app/pmars` and still satisfy nothing — T3/T4 are prefix-glob and directory-shape
   only, so "build output present" is never checked.

## 5. Oracle-shape cross-check (bonus, not one of the assigned three)

The probe's stated limit is that it never runs the oracle. I closed the cheap half of it: fetched
`pmars_0.9.4.orig.tar.xz` + `pmars_0.9.4-1.debian.tar.xz` from `deb.debian.org` (the source `apt-get source pmars`
unpacks, directory `pmars-0.9.4`), applied the oracle's two `sed` edits from `solution/solve.sh`, built, and ran the
grader in the probe's sandbox with the genuine binary in `/usr/local/bin` and the genuine tree + `debian/` +
`rave.red`/`flashpaper.red` under `/app`. Receipt: `R38CritIndep/oracle-shape.txt`.

```
rc=0
TEST test_pmars_works P
TEST test_headless_no_x11 P
TEST test_debian_source_used P
TEST test_built_from_source P        → PPPP
```

Real outputs against the grader's patterns:

- cdb step lines: `00001   CMP.I  $   125, $   113` then `(cdb) 00003   DJN.F  $    -3, <  -308` — the `(cdb) `
  prompt prefixes later lines, `findall` still matches (`\b` before the 5-digit address); `>= 2` holds.
- battle: `Results: 12 32 6` from `-r 50` (integers differ from the canned `12 34 78`; only the shape is graded).
- `ldd`: `libncursesw.so.6`, `libc.so.6`, `linux-vdso`, `ld-linux` — no X11 name.

So the grader is not false-red on a genuine build shape: the "canned passes" findings are about **unenforced
requirements**, not about a grader that rejects real solutions. Build note: this host's gcc defaults to
`-std=gnu23`, where the source's K&R `sort_by_score()` prototype is a hard error
(`global.h:428: error: conflicting types for 'sort_by_score'; have 'void(void)'`), so the oracle-shape run used
`-std=gnu89`. Re-running the same tree with the oracle's own two `sed` edits and **`-std=gnu17`** (Debian 13's
gcc-14 default, i.e. what `solve.sh`'s plain `make` gets) compiles with **0 errors** and produces the binary —
so the oracle's build path is not contradicted, and the probe's "compiled on the host" limit is the only
compiler caveat.

## 6. Findings, each with the smallest safe correction

### 6.1 No counterexample to the receipt
All 22 letters reproduce, byte-identically, from the frozen probe on a clean clone; the receipt's
`cases=22 observed_pass=7 observed_fail=15 mismatches=0` is honest as a record of what that probe prints.
Nothing frozen needs to change; the kill rule ("prediction mismatches are reported, never edited out") is not
triggered. **Correction: none.**

### 6.2 Capture provenance is real, and the oracle has a different path
`terminal-bench-2` @ `2fd12b88`, `build-pmars/`, raw fetches: `tests/test_outputs.py`
`d9d2796d…e85`, `instruction.md` `1606850…b82`, `tests/test.sh` `4770437e…334`, `task.toml` `7ee2eac2…9cd`,
`solution/solve.sh` `105292ca…543` — all five equal the local captures (`R38CritIndep/provenance.txt`).
The oracle is at **`build-pmars/solution/solve.sh`**, not `build-pmars/solve.sh`.
Upstream `environment/Dockerfile` is `FROM debian:13.0-slim`, `WORKDIR /app`, and
`COPY warriors/flashpaper.red warriors/rave.red /app/`.
**Correction:** S115/S116 and the entry must cite `solution/solve.sh` if they cite the oracle at all; and this
Dockerfile is the citation for two things the probe currently only assumes — the verifier's cwd `/app` (T1's
relative `rave.red`) and the root PATH `/usr/local/sbin` before `/usr/local/bin` that makes `path-split` pass.
Cheap, high-value: add that one line to the entry's limits/observations, since `path-split` is a headline item.

### 6.3 V7's derivation, computed — every label will be `partly`
From the frozen dry table's `violates=` sets and the receipt's `observed=`, V7's rule yields exactly:

| tag | frozen line | V7 label | violating cases | pass/fail |
|---|---|---|---|---|
| `from-source` | `instruction.md:1` | partly | 22 (all) | 7 P / 15 F |
| `no-x11` | `instruction.md:3` | partly | 3 (empty-tree, x11-linked, x11-dlopen) | 1 / 2 |
| `debian-source` | `instruction.md:3` | partly | 22 (all) | 7 / 15 |
| `extract-to-app` | `instruction.md:3` | partly | 22 (all) | 7 / 15 |
| `install-path` | `instruction.md:3` | partly | 4 (empty-tree, nonexec, silent, path-split) | 1 / 3 |
| `results-format` | `instruction.md:7` | partly | 5 (empty-tree + the four `results-*`) | 1 / 4 |
| `debugger-works` | `instruction.md:9` | partly | 22 (all) | 7 / 15 |

**Correction / handoff:** any `enforced` or `unenforced` label in the entry's requirement map fails V7. And a
limit worth naming in the entry: the four `FAKE` tags sit on all 22 cases by construction, so their label is
`partly` for the trivial reason that *some* case passes — the label is structural, not a measurement of that
requirement. That is the frozen rule working as written; it should not be presented as if the map graded each
requirement separately.

### 6.4 Probe-model gaps (not receipt errors, worth one line each)
- **No case stages `rave.red`/`flashpaper.red`.** T1 runs `pmars -e rave.red` with cwd `/app`; every canned
  artefact ignores argv, so no case can tell "the binary opened the warrior" from "the binary printed canned
  text". The image supplies the two warriors, so the real task is not at risk — but the probe cannot see the
  `debugger-works` / `results-format` requirements' input side at all. A future case would need a binary that
  only prints when its named input exists.
- **`overall()` collapses pytest ERROR into FAIL.** For the letters and for `test.sh`'s reward the difference is
  nil (any non-zero pytest exit → reward 0), but the receipt's `test_headless_no_x11:error=CalledProcessError`
  is a pytest *error*, and an entry quoting "tests failed" for those cases should say "errored".

### 6.5 Three new tolerances
Section 4 items 1–3. None contradicts a frozen case; if the entry's headline list claims the unenforced set is
enumerated by the 22 cases, these three falsify that claim and should be either cited as wave-1 extras with the
same provenance (this report, `extras.txt`) or excluded by wording.

## 7. Limits of this check

- Letters only: the harness calls the four test functions directly; pytest's error/fail distinction is not
  reproduced (irrelevant to the verdict and to reward).
- Host stand-in throughout: host bash/glibc/gcc, `ldd`, `bwrap`, not the task image. The oracle check built
  pMARS from the Debian orig tarball on this host, not in `alexgshaw/build-pmars:20251031`.
- `-r 50` battle integers vary by seed; only the format was compared.
- I did not read `plans/round38_c1_verify.py`'s mutants, did not judge C1, and did not edit, integrate or ship
  anything. No lane file, index or jj state was touched.

## 8. Tools installed
None. `bwrap`, `gcc`, `ldd`, `python3` were already present; nothing was installed or upgraded.

## 9. Receipts in this directory
`predictions.md` (written 02:46, pre-run), `probe-replay.txt` (frozen probe replay, byte-equal to the receipt),
`extras.txt` (3 extra cases), `oracle-shape.txt` (genuine-build cross-check), `provenance.txt` (upstream digests).

VERDICT: indep-agree-22/22-extra-3/3
