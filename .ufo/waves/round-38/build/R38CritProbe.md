# R38CritProbe — attack on the frozen `build-pmars` probe (round 38, wave 1)

Target: `plans/build_pmars_probe.py` (sha256 `32f0771c…`), its receipt `corpus/evidence/round38/build-pmars-probe.txt`,
the five captures in `corpus/evidence/round38/tb2-build-pmars/`. Read-only attack; nothing frozen edited.

Receipts: `.ufo/waves/round-38/build/R38CritProbe/{r1.txt,r2.txt,dry.txt,pytest-parity.txt,syscall-ldd.txt}`.
Scratch: `/fast/scratch/hyaku/kengaku-r38/R38CritProbe` (clone at lane tip `2c5f4e0ba8e2`; deleted before yield).

## Bottom line

The probe does what its docstring claims and the harness's direct call is verdict-identical to pytest (22/22),
but **five `violates=` assignments are contestable**, and one of them is load-bearing: `canned-x11-dlopen` is the
only passing case carrying `no-x11`; without it that row would derive `enforced` instead of `partly`.
Both headline mechanisms survive a syscall-level attack. Nothing in this report asks for a frozen-file edit.

## 1. Reproduction (accept)

```
$ python3 plans/build_pmars_probe.py --lane . --work $S/w1 > r1.txt   rc=0, stderr empty
$ python3 plans/build_pmars_probe.py --lane . --work $S/w2 > r2.txt   rc=0, stderr empty
cmp r1.txt r2.txt                                        -> BYTE-EQUAL
cmp r1.txt corpus/evidence/round38/build-pmars-probe.txt -> RECEIPT-EQUAL
$ python3 plans/build_pmars_probe.py --lane . --dry | cmp - .../build-pmars-dry-cases-freeze.txt -> DRY-EQUAL
```
`len(CASES)==22`, summary line `cases=22 observed_pass=7 observed_fail=15 mismatches=0` — matches the receipt.

## 2. Does each case test what its requirement text says?

Every verdict was re-derived independently: the four test functions run under **pytest 8.4.1** (the pin in
captured `test.sh`) inside the probe's own `sandbox_argv()` per case — **22/22 letters identical to `predicted`,
and `rc==0` iff `PPPP`**, i.e. the receipt's verdicts are also the reward verdicts. The mechanisms of the seven
passing cases were then re-derived one by one:

| case | mechanism re-derived | evidence |
|---|---|---|
| `canned-shape` | canned text + empty `debian/` + zero-byte `src/dummy.c` → PPPP | pytest parity, receipt |
| `canned-x11-dlopen` | **dlopen really fires at run time and leaves no `DT_NEEDED`** | `readelf -d` → only `libc.so.6`; `strace -f -e openat` → `openat(..., "/usr/lib/libX11.so.6", ...) = 3` |
| `results-trailing-text` | `re.match(r"Results: \d+ \d+ \d+")` anchors the start only | grader source `test_outputs.py:41`; parity |
| `canned-exit-nonzero` | `check_output` returns `e.output` when non-empty | grader source `run_shell_command`; parity |
| `path-split` | **the behaviour checks execute `/usr/local/sbin/pmars`, `ldd` reads `/usr/local/bin/pmars`** | in-sandbox `command -v pmars` → `/usr/local/sbin/pmars`; `strace execve("/usr/local/sbin/pmars", ["pmars","-b","x"]) = 0`; `ldd /usr/local/bin/pmars` → libc only |
| `debian-is-file` | `Path.exists()` is true for a regular file | parity |
| `c-is-dir` | `Path.glob("*.c")` matches a directory | parity |

So the two cases the assignment singled out are honest: the dlopen call is real (not a static `ldd` trick), and the
split names the right binaries. Two environment assumptions behind them were checked:

- `PATH` = `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` is exactly `debian:13.0-slim`'s default
  (`docker run --rm debian:13.0-slim sh -c 'echo PATH=$PATH'`), and `/usr/local/sbin` exists there; upstream
  `build-pmars/environment/Dockerfile` is `FROM debian:13.0-slim`. Captured `test.sh` prepends `$HOME/.local/bin`
  before that, which keeps `/usr/local/sbin` ahead of `/usr/local/bin` — the split still holds.
- the host-`ldd` substitution is verdict-neutral: Debian 13's `ldd` on the probe's own binaries gives
  `not a dynamic executable` + rc 1 for static and for a script (→ `CalledProcessError` → `F`, as the receipt
  shows), libc-only for the dlopen binary, and `libX11.so.6 => not found` for the x11-linked one (the substring
  check still fails). Same verdicts as the host.

## 3. Contestable `violates=` assignments

1. **`canned-x11-dlopen` (`plans/build_pmars_probe.py:114`) — `no-x11`. LOAD-BEARING.** The call is real, but the
   artefact never invokes an X11 symbol: it demonstrates "a run-time-loaded library is invisible to the `ldd`
   string scan", not "an X11-enabled pMARS passes". A genuine X11 build carries `DT_NEEDED libX11` (proved by the
   `canned-x11-linked` control, `:112`) and *is* caught, so the bypass needs a hand-written `dlopen` rig, which the
   oracle path never produces. Tag is defensible only against `instruction.md:9`'s word "dependencies" in the
   run-time sense. **Label impact:** this is the *only* tag whose derived label moves if the case is dropped —
   `no-x11` has 3 carriers (`empty-tree` fail, `canned-x11-linked` fail, this one pass); without it, `enforced`.
2. **`results-negative` (`:122`) — `results-format`.** `instruction.md:7` reads "where X, Y, Z are integers"; `-1`
   is an integer, so the artefact does **not** violate the line — it exposes a grader false-red (`\d+`), and real
   pMARS scores are non-negative anyway. As written, the case measures grader strictness, not a violating state.
   Label impact: none (`results-trailing-text` keeps `partly`).
3. **`silent-binary` (`:132`) — `install-path`.** A silent binary *is* installed at `/usr/local/bin/pmars`; the
   failed lines are `:7`/`:9`, not `:3`'s install path. `install-path` reads as missing/non-executable only.
   Label impact: none (`path-split` keeps `partly`).
4. **`pmars-dir-elsewhere` (`:147`) — `extract-to-app`.** The tree is at `/app/src/pmars-0.9.4`, i.e. *under* `/app`;
   `:3` says "Extract the source to `/app`". The case demonstrates the grader's one-level `glob("pmars-*")`
   (a possible grader false-red on a defensible layout), not a violated requirement. Label impact: none.
5. **`four-digit-address` (`:126`) — `debugger-works`.** `:9` says only "the debugger works properly"; 5-digit
   addresses are a pMARS convention, not an instruction term. The tag survives only through `FAKE` (the artefact is
   canned), not through the case's stated purpose ("grader needs `\d{5}`"), which is again grader strictness.
   Label impact: none.

Not contestable, checked: `empty-tree` (all seven), `canned-script`/`canned-static` (no `no-x11`: correct, they are
not X11), `debian-is-file`, `c-is-dir`, `nonexec-binary`, `results-not-last` (`tail -n 1` really sees the extra
line; the instruction's own command is the one that ends in `tail`).

**Cumulative map effect:** deriving V7's rule over the receipt gives `partly` for all seven tags
(`from-source` 7/22 pass, `debian-source` 7/22, `extract-to-app` 7/22, `debugger-works` 7/22, `no-x11` 1/3,
`install-path` 1/4, `results-format` 1/5). The map is therefore uniform; its information is the per-line prose, not
the labels. Corrections 2–5 leave every label unchanged; correction 1 would flip `no-x11` to `enforced`.

## 4. Harness direct call vs pytest

Same four functions, same order, same sandbox, pytest 8.4.1 from the captured `test.sh` pin: **0/22 verdict
differences, 0 exit-code differences** (receipt `pytest-parity.txt`). Residual (non-verdict) differences:
interpreter 3.14 (probe and my parity run) vs `uvx -p 3.13` in `test.sh`; the `pytest-json-ctrf` plugin is not
exercised (it only writes `/logs/verifier/ctrf.json`, the reward is pytest's exit code). One latent divergence:
`HARNESS_PY` (`:174`) catches `AssertionError`/`Exception`, not `BaseException`, so a `SystemExit` from a test body
would abort the case as `SETUP rc=2` where pytest records a failure — no current case can raise it.

## 5. Nits and stated limits

- **`C_SRC` is 21 content lines (`:151-171`), not 14.** The dispatch headline and the entry draft on disk
  (`R38PkgEntry/entry.md:26,156,213`) say "14-line"; the frozen claims and receipt contain no "14" (`grep` rc=1).
  Told R38PkgProse; it is prose-only.
- `PINS` (`:55`) covers 2 of the 5 captures; `test.sh`, `task.toml`, `solve.sh` are pinned only by C2's V1. Consistent
  with the docstring ("digest checked before any case" applies to the grader), worth one sentence in the entry.
- `/app` is staged **without** `rave.red`/`flashpaper.red`, although upstream `environment/Dockerfile` copies both
  into `/app`. Disclosed in the docstring, but it means a *genuine* pmars could never pass the probe's own sandbox —
  the accept side (7 passes) is fabricated by construction; the receipt must not be read as "the grader accepts a
  real build".
- Capture provenance re-verified end to end: all five `SHA256SUMS` entries reproduce byte-for-byte from
  `harbor-framework/terminal-bench-2` @ `2fd12b88` (the live `laude-institute/terminal-bench-2` redirects there), so
  the receipt's `@ terminal-bench-2 2fd12b88` header is honest.
- Not done by this seat: no run in the task image (`alexgshaw/build-pmars:20251031` not pulled — only its base
  `debian:13.0-slim`), no oracle run, no `ltrace` (strace sufficed).

## 6. Smallest safe corrections

1. `canned-x11-dlopen`: keep case and tag, but the entry's `no-x11` bullet must bound it — "a hand-made `dlopen`
   artefact; a `-lX11` build is caught (`canned-x11-linked`)" — so no reader takes the row as "an X11-enabled pMARS
   passes". If the L1 rejects the tag, `no-x11` derives `enforced` and the map must say so.
2. `results-negative`: drop `results-format` from its tag (keep the case as a documented grader false-red); label
   unchanged.
3. `silent-binary`: drop `install-path`, keep `FAKE`; label unchanged.
4. `pmars-dir-elsewhere`: drop `extract-to-app`, keep `FAKE`; label unchanged (and the prose already calls it a
   glob-depth limit).
5. `four-digit-address`: no tag change; describe it in the entry as a `\d{5}` strictness probe, not a requirement
   violation.
6. Prose: "21-line", not "14-line".

VERDICT: probe-attack-5-contestable
