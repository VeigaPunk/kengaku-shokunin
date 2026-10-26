# F38IndepProbe — independent re-execution of the `build-pmars` grader probe (round 38, wave 2)

Seat: critic, leaf. Scope: C2 coverage arm only — the executed probe receipt
`corpus/evidence/round38/build-pmars-probe.txt` and the knowledge entry it backs
(`corpus/knowledge/tb2-build-pmars-grader.md`, S115/S116). Everything below is a fresh instrument;
`plans/build_pmars_probe.py` was **not imported** (its source was read, and it was also *run* once as a
separate cross-check, see §6).

## 1. Axes attacked

| Axis | Attack |
|---|---|
| A1 instrument | different sandbox (real `chroot` in a root mount namespace) and different entry point (real `pytest 8.4.1` on CPython 3.13, the versions `test.sh` pins) than the frozen probe (bwrap + host CPython 3.14 + hand-rolled function calls) |
| A2 receipt | every one of the 22 frozen cases re-staged with **my own** C program, script and constants, per-test letters compared to the receipt |
| A3 mechanisms | each causal claim re-proved directly: `DT_NEEDED` vs `dlopen`, exit status, `PATH` order, existence-only shapes, `ldd` failure mode, file mode |
| A4 map | the seven `Requirement map` labels re-derived from the receipt's own `violates=`/`observed=` columns, independently of `V7` |
| A5 anchoring | the C2 predicate re-run in a clean clone at the **stated** landing tip `8c7422d` (the L1 receipt's own `TIP` line is `d93b7d68`) |

## 2. Instrument (differences that matter)

| | frozen probe | this probe |
|---|---|---|
| sandbox | `bwrap --unshare-net --unshare-pid --unshare-ipc --ro-bind /usr …` | `sudo unshare -m --propagation private` + `chroot`; `/usr`,`/etc`,`/dev` bind-mounted rw; no net/pid/ipc namespace |
| shell of grading | host `/bin/sh` | host `/bin/sh` inside chroot (`/bin → usr/bin`) |
| grader runner | module imported, four functions called | `python -m pytest -rA --tb=no -q -p no:cacheprovider /tests/test_outputs.py` |
| python / pytest | 3.14.8, no pytest | 3.13.16 + pytest 8.4.1 (`tests/test.sh` pins `uvx -p 3.13`, `pytest==8.4.1`) |
| privileges | unprivileged user | root inside the namespace |
| artefact texts | `Results: 12 34 78`, exit 3 | `Results: 21 43 99`, exit 7 (deliberately different constants) |
| cwd | `/app` | `/app` |

Tooling: no host install. Existing `uv 0.13.0` was used to build a pytest venv **in scratch** from the local
cache (`uv venv` + `uv pip install --offline pytest==8.4.1`); `pytest 8.4.1` / `Python 3.13.16` confirmed by
`./pytestenv/bin/python -m pytest --version`. No pacman call.

## 3. Result — the 8 assigned cases

```
$ python3 indep_probe.py --capture <lane>/corpus/evidence/round38/tb2-build-pmars \
    --env ./pytestenv --receipt <lane>/corpus/evidence/round38/build-pmars-probe.txt
# capture test_outputs.py sha256=d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85 receipt_pin=<same> pin_match=True
CASE canned-shape observed=pass tests=PPPP pytest_rc=0 assigned receipt_tests=PPPP agree=yes
CASE canned-x11-linked observed=fail tests=PFPP pytest_rc=1 assigned receipt_tests=PFPP agree=yes
CASE canned-x11-dlopen observed=pass tests=PPPP pytest_rc=0 assigned receipt_tests=PPPP agree=yes
CASE results-trailing-text observed=pass tests=PPPP pytest_rc=0 assigned receipt_tests=PPPP agree=yes
CASE canned-exit-nonzero observed=pass tests=PPPP pytest_rc=0 assigned receipt_tests=PPPP agree=yes
CASE path-split observed=pass tests=PPPP pytest_rc=0 assigned receipt_tests=PPPP agree=yes
CASE debian-is-file observed=pass tests=PPPP pytest_rc=0 assigned receipt_tests=PPPP agree=yes
CASE c-is-dir observed=pass tests=PPPP pytest_rc=0 assigned receipt_tests=PPPP agree=yes
assigned_agree=8/8 capture_sha256=d9d2796d…
```

**8/8 agreed, letter for letter**, on a different interpreter, a different sandbox mechanism, root instead
of user, and different canned constants.

## 4. Result — the whole receipt (supplementary)

The remaining 14 cases were re-staged too, so the receipt is checked as a whole, not only where the assignment
looked:

```
CASE empty-tree observed=fail tests=FFFF pytest_rc=1 receipt_tests=FFFF agree=yes
CASE canned-script observed=fail tests=PFPP pytest_rc=1 receipt_tests=PFPP agree=yes
CASE canned-static observed=fail tests=PFPP pytest_rc=1 receipt_tests=PFPP agree=yes
CASE results-two-ints observed=fail tests=FPPP pytest_rc=1 receipt_tests=FPPP agree=yes
CASE results-not-last observed=fail tests=FPPP pytest_rc=1 receipt_tests=FPPP agree=yes
CASE results-negative observed=fail tests=FPPP pytest_rc=1 receipt_tests=FPPP agree=yes
CASE one-address observed=fail tests=FPPP pytest_rc=1 receipt_tests=FPPP agree=yes
CASE four-digit-address observed=fail tests=FPPP pytest_rc=1 receipt_tests=FPPP agree=yes
CASE nonexec-binary observed=fail tests=FPPP pytest_rc=1 receipt_tests=FPPP agree=yes
CASE silent-binary observed=fail tests=FPPP pytest_rc=1 receipt_tests=FPPP agree=yes
CASE no-debian-dir observed=fail tests=PPFP pytest_rc=1 receipt_tests=PPFP agree=yes
CASE src-no-c observed=fail tests=PPPF pytest_rc=1 receipt_tests=PPPF agree=yes
CASE no-src-dir observed=fail tests=PPPF pytest_rc=1 receipt_tests=PPPF agree=yes
CASE pmars-dir-elsewhere observed=fail tests=PPFF pytest_rc=1 receipt_tests=PPFF agree=yes
```

22/22 `agree=yes`; the derived counts `observed_pass=7 observed_fail=15` hold in my run as well (7 `pass`
lines above + §3). `pytest_rc` is `0` exactly on the seven `pass` cases and `1` on the fifteen `fail` cases,
consistent with the read-only `test.sh:25-29` reward mapping (still **not executed** — `uvx`/`/logs` are out of
scope). Two consecutive runs were byte-identical (`diff run1.txt run2.txt` → no output), matching the entry's
"second run's receipt was byte-equal" statement.

Control: `empty-tree` is `FFFF`, so the instrument is not uniformly green.

## 5. Mechanism probes (each claim, proved directly)

| Claim in the entry | Command (inside the case chroot) | Output |
|---|---|---|
| `canned-x11-linked` is caught because `ldd` lists `libX11` | `readelf -d …/pmars \| grep NEEDED; ldd …` | `[libX11.so.6]`, `libX11.so.6 => /usr/lib/libX11.so.6` |
| `canned-x11-dlopen` hides the library from `ldd` but really loads it | `readelf -d`, `ldd`, `strace -f -e trace=openat` | NEEDED shows only `libc.so.6`; `ldd` shows no X11 line; `openat(… "/usr/lib/libX11.so.6", O_RDONLY\|O_CLOEXEC) = 3` |
| exit status is ignored when output is non-empty | `/usr/local/bin/pmars -b >/dev/null; echo rc=$?` | `rc=7` — and the case is still `PPPP` |
| `ldd` fails closed on non-ELF artefacts | `ldd …; echo rc=$?` for `canned-static`, `canned-script` | `not a dynamic executable` / `rc=1` on **stderr** both times (stdout empty → `CalledProcessError` re-raised) |
| two objects graded under one name | `command -v pmars; head -1 /usr/local/sbin/pmars; head -c4 /usr/local/bin/pmars; pmars -e x; ldd /usr/local/bin/pmars` | `/usr/local/sbin/pmars`, `#!/bin/sh`, `\177 E L F`, canned debugger text, `ldd` reads the ELF |
| `debian` may be a regular file | `ls -l /app/pmars-0.9.4/debian; test -f …` | `-rw-r--r-- … 0` and `regular-file`, `not-a-dir` |
| `src/sim.c` may be a directory | `ls -ld …; glob("*.c")` | `drwxr-xr-x … src/sim.c`, glob → `['sim.c']` |
| a non-executable binary fails on behaviour, not presence | `ls -l; /usr/local/bin/pmars -b; echo rc=$?` | `-rw-r--r--` … `-rw-r--r--`, `Permission denied`, `rc=126` |

Receipts: `mechanism-x11.txt`, `mechanism-artefacts.txt`.

## 6. Cross-check of the receipt with its own instrument

```
$ python3 <lane>/plans/build_pmars_probe.py --lane <lane> --work <scratch>
…
cases=22 observed_pass=7 observed_fail=15 mismatches=0
$ diff <(grep '^CASE\|^cases=' frozen_run.txt) <(grep '^CASE\|^cases=' receipt)   # empty
```

The frozen instrument reproduces its receipt byte-for-byte (`frozen-instrument-run.txt`). So the receipt is
not stale relative to its own script.

## 7. Map labels, derived independently of `V7`

Rule: `enforced` iff every case whose `violates=` carries the tag is observed `fail`, `unenforced` iff every
one is `pass`, `partly` otherwise (`label-derivation.txt`):

```
from-source      line=1 stated=partly derived=partly violating=22 cited_ok=True OK
no-x11           line=3 stated=partly derived=partly violating= 3 cited_ok=True OK
debian-source    line=3 stated=partly derived=partly violating=22 cited_ok=True OK
extract-to-app   line=3 stated=partly derived=partly violating=22 cited_ok=True OK
install-path     line=3 stated=partly derived=partly violating= 4 cited_ok=True OK
results-format   line=7 stated=partly derived=partly violating= 5 cited_ok=True OK
debugger-works   line=9 stated=partly derived=partly violating=22 cited_ok=True OK
label_mismatches = 0
```

The contestability the entry itself discloses is real and load-bearing: drop the `no-x11` tag from
`canned-x11-dlopen` and `no-x11`'s violating set becomes `['empty-tree','canned-x11-linked']` (both `fail`),
i.e. the label would derive `enforced`, not `partly`. The entry states exactly this and freezes the tag; no
label is changed by my probe.

## 8. C2 at the stated tip (not the L1's measured tip)

`measure-final.txt:1` records `TIP d93b7d68…`, while the round-38 attack tip is `8c7422d…`
(`git merge-base --is-ancestor 8c7422d HEAD` → true; `git log` → HEAD `1fa7af4`). I therefore re-ran the
frozen C2 predicate in a clean clone **at `8c7422d`**:

```
$ git clone -q --no-local <lane> "$S/lane" && git checkout -q 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
$ python3 plans/round38_c2_verify.py --lane . --work <scratch>
V1 ok … gate: P10 ok probe_rerun=byte-equal bytes=5537 … V4 ok cases=22 … V7 ok rows=7 tags=7 bad=0
checks=7 defects=0
PREDICATE C2 pass
exit=0
```

The frozen predicate passes at the commit the round claims, not only at the L1's `d93b7d68`
(`c2-counter-at-8c7422d.txt`).

## 9. What I could not break, and what remains uncovered

No counterexample found. The strongest attacks available to me — different runner semantics
(`pytest` collection/exit status), different interpreter (3.13 vs 3.14), root vs user, chroot vs bwrap, and
different canned constants (`21 43 99`, exit `7`) — all reproduce the receipt letter for letter, including the
15 negative cases, so the receipt is not an artefact of its instrument.

Still not probed by me (and not claimed by the entry): the oracle `solve.sh` (read, never run), `tests/test.sh`
itself, the task image/Dockerfile toolchain (my shell is the host's, not Debian's `dash`), any warrior file
existing in `/app`, and the accept side with a *real* pMARS build. My sandbox still stages `/app` and no
warriors, i.e. it shares the entry's "fabricated artefact" design; it cannot speak to how the grader treats a
genuine build.

## 10. Verdict and recommendation

- Counterexample: **none**. Every assigned case and every supplementary case matches its receipt letter.
- Impacted axes: A1–A5 all confirm the frozen C2 claim; nothing moves a label, a digest or a count.
- Smallest safe correction: **none required**. If a hardening move were wanted, the only cheap one is
  bookkeeping, not evidence: state in the C2 receipt that the predicate was re-measured at the round's stated
  tip `8c7422d` (the file's own `TIP` line names `d93b7d68`), so the anchor is not misread as pre-landing.

Artifacts in this directory: `indep_probe.py`, `inspect.sh`, `indep-probe-run1.txt`, `indep-probe-run2.txt`,
`frozen-instrument-run.txt`, `mechanism-x11.txt`, `mechanism-artefacts.txt`, `label-derivation.txt`,
`c2-counter-at-8c7422d.txt`, `capture-digests.txt`, `SHA256SUMS`. Scratch
`/fast/scratch/hyaku/kengaku-r38/F38IndepProbe` (clone at `8c7422d`, chroot rootfs, pytest venv) removed after
the receipts above were copied; no lane file, index or jj state touched.

VERDICT: indep-probe-agree-8/8
