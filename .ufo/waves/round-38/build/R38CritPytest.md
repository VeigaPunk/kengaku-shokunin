# R38CritPytest — is the frozen build-pmars receipt faithful to real pytest?

Seat: `R38CritPytest` (critic). Wave 1, round 38 (hyaku run 8), 2026-10-26.
Mode: fidelity attack on a frozen artifact. **No lane file was written, staged, or committed.** All work
in `/fast/scratch/hyaku/kengaku-r38/R38CritPytest` (clone + venv), deleted at the end; evidence copied here.

## 0. Question asked

The C2 receipt `corpus/evidence/round38/build-pmars-probe.txt` states per-case letters (`tests=`) that were
produced NOT by pytest but by the frozen probe's own harness: import `/tests/test_outputs.py`, call the four
`test_*` functions in file order, `AssertionError`→F, any other exception→F, return→P
(`plans/build_pmars_probe.py:264-274`). The verifier the entry describes runs **pytest 8.4.1** and maps its
**exit code** to reward (`test.sh:18-29`). So the receipt's letters are only as good as that substitution.

Attack: run the same 22 frozen cases, in the same bwrap layout, under real pytest 8.4.1 (same argv shape as
`test.sh`), and compare (a) per-test outcomes and (b) pytest's exit code against the receipt's letters.

## 1. Inputs, pinned

| input | sha256 |
|---|---|
| `plans/build_pmars_probe.py` | `32f0771cd5c4129a9a9795e3016a4f1c2cf660003f09cb4d719731fd5825c24a` |
| `corpus/evidence/round38/build-pmars-probe.txt` | `2408b477b0299e1339064b4b3df968a00174b3a5999016073b5fe4fd8cbb4ef9` |
| `.../tb2-build-pmars/test_outputs.py` | `d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85` (probe PINS) |
| `.../tb2-build-pmars/test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| `.../tb2-build-pmars/instruction.md` | `1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82` (probe PINS) |

Versions used: uv 0.13.0; runner python **3.13.16** (uv-managed CPython, matching `test.sh:18` `-p 3.13`);
**pytest 8.4.1**; **pytest-json-ctrf 0.3.5** (both as pinned in `test.sh`); bubblewrap 0.13.1; gcc 16.2.1;
host python 3.14.8 (probe driver only). No package installed into the host: the venv is a `uv venv -p 3.13`
under scratch, `uv pip install pytest==8.4.1 pytest-json-ctrf==0.3.5`.

## 2. Method

Draft probe `build_pmars_probe_pytest.py` (kept here, **new file**, not a change to the frozen probe) does:

1. `importlib`-loads the **frozen** `plans/build_pmars_probe.py` from my clone, so `CASES`, `Art`,
   `build_art`, `stage_app`, `TESTS`, `PATH`, `HARNESS_PY` are the frozen objects, not retyped copies.
2. Stages each case once, then runs **two** bwrap commands on the *same* read-only staged tree:
   - `direct`: `/usr/bin/python3 /harness.py` — the frozen harness verbatim.
   - `pytest`: `<venv>/bin/pytest -rA --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py`, cwd `/app`,
     env `PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`, i.e. the shape of
     `test.sh:18-24` (`uvx -p 3.13 -w pytest==8.4.1 … pytest --ctrf … /tests/test_outputs.py -rA`).
3. Adds to the frozen `sandbox_argv` three binds: the venv and its uv-managed interpreter at their original
   absolute paths (relocation breaks `pyvenv.cfg` detection), and a writable `/logs` so the ctrf plugin
   writes where `test.sh` tells it to. Everything else (namespaces, `/usr` ro, `/etc` ro, private `/tmp`,
   ro `/app` + `/usr/local/bin` + `/usr/local/sbin`, `/tests` holding only the capture, `--chdir /app`) is
   the frozen layout.
4. Reads three independent outcome channels and requires all of them to agree:
   `direct` harness prints, pytest `-rA` short summary, the ctrf JSON `results.tests[].status`.

Commands (all under `S=/fast/scratch/hyaku/kengaku-r38/R38CritPytest`, `export TMPDIR=$S`):

```
git clone -q --shared <lane> "$S/lane"                       # rev-parse --show-toplevel == "$S/lane"
uv venv -q -p 3.13 "$S/venv"; VIRTUAL_ENV=$S/venv uv pip install -q pytest==8.4.1 pytest-json-ctrf==0.3.5
python3 plans/build_pmars_probe_pytest.py --lane "$S/lane" --work "$S/w3" --venv "$S/venv" --ctrf-out "$S/ctrf"
python3 plans/build_pmars_probe.py        --lane "$S/lane" --work "$S/w2"     # frozen probe, same host
```

## 3. Result — 22/22, three channels

Full output: `pytest-all.txt` (27 KB, all 22 cases with per-test lines, raw `E`/`FAILED`/`PASSED` lines);
`pytest-run2.txt` (second run: `diff` of `^CASE` lines → empty, so the pytest run is deterministic, same as
the receipt's second-run claim); `ctrf/<case>.json` (22 files); `receipt.diff` (0 bytes).

```
CASE empty-tree            receipt=FFFF direct=FFFF pytest=FFFF ctrf=FFFF rc=1 agree=yes
CASE canned-shape          receipt=PPPP direct=PPPP pytest=PPPP ctrf=PPPP rc=0 agree=yes
CASE canned-script         receipt=PFPP direct=PFPP pytest=PFPP ctrf=PFPP rc=1 agree=yes
CASE canned-static         receipt=PFPP direct=PFPP pytest=PFPP ctrf=PFPP rc=1 agree=yes
CASE canned-x11-linked     receipt=PFPP direct=PFPP pytest=PFPP ctrf=PFPP rc=1 agree=yes
CASE canned-x11-dlopen     receipt=PPPP direct=PPPP pytest=PPPP ctrf=PPPP rc=0 agree=yes
CASE results-two-ints      receipt=FPPP direct=FPPP pytest=FPPP ctrf=FPPP rc=1 agree=yes
CASE results-trailing-text receipt=PPPP direct=PPPP pytest=PPPP ctrf=PPPP rc=0 agree=yes
CASE results-not-last      receipt=FPPP direct=FPPP pytest=FPPP ctrf=FPPP rc=1 agree=yes
CASE results-negative      receipt=FPPP direct=FPPP pytest=FPPP ctrf=FPPP rc=1 agree=yes
CASE one-address           receipt=FPPP direct=FPPP pytest=FPPP ctrf=FPPP rc=1 agree=yes
CASE four-digit-address    receipt=FPPP direct=FPPP pytest=FPPP ctrf=FPPP rc=1 agree=yes
CASE canned-exit-nonzero   receipt=PPPP direct=PPPP pytest=PPPP ctrf=PPPP rc=0 agree=yes
CASE nonexec-binary        receipt=FPPP direct=FPPP pytest=FPPP ctrf=FPPP rc=1 agree=yes
CASE silent-binary         receipt=FPPP direct=FPPP pytest=FPPP ctrf=FPPP rc=1 agree=yes
CASE path-split            receipt=PPPP direct=PPPP pytest=PPPP ctrf=PPPP rc=0 agree=yes
CASE no-debian-dir         receipt=PPFP direct=PPFP pytest=PPFP ctrf=PPFP rc=1 agree=yes
CASE debian-is-file        receipt=PPPP direct=PPPP pytest=PPPP ctrf=PPPP rc=0 agree=yes
CASE src-no-c              receipt=PPPF direct=PPPF pytest=PPPF ctrf=PPPF rc=1 agree=yes
CASE c-is-dir              receipt=PPPP direct=PPPP pytest=PPPP ctrf=PPPP rc=0 agree=yes
CASE no-src-dir            receipt=PPPF direct=PPPF pytest=PPPF ctrf=PPPF rc=1 agree=yes
CASE pmars-dir-elsewhere   receipt=PPFF direct=PPFF pytest=PPFF ctrf=PPFF rc=1 agree=yes
pytest-agree 22/22
```

`grep -c 'pytest_rc=0'` = **7**, `grep -c 'pytest_rc=1'` = **15** — the receipt's
`cases=22 observed_pass=7 observed_fail=15` is exactly what the real verifier's exit code gives, and under
`test.sh:25-28` those 7 cases would each write `reward=1`.

Per-test evidence, the six required cases (verbatim from `pytest-all.txt`):

- `empty-tree` FFFF rc=1 — `E AssertionError: pmars not installed at /usr/local/bin/pmars`;
  `E subprocess.CalledProcessError: Command 'ldd /usr/local/bin/pmars' returned non-zero exit status 1.`
- `canned-shape` PPPP **rc=0** — 4× `PASSED ../tests/test_outputs.py::test_*`.
- `canned-x11-dlopen` PPPP **rc=0** — 4× `PASSED` (the dlopen()ed libX11 is invisible to
  `test_outputs.py:56` `for lib in x11_libs:`).
- `canned-exit-nonzero` PPPP **rc=0** — 4× `PASSED`; the `return e.output` at `test_outputs.py:14` eats
  exit status 3.
- `path-split` PPPP **rc=0** — 4× `PASSED`; `ldd` reads `/usr/local/bin/pmars`, the shell resolves
  `pmars` to the sbin script earlier on `PATH`.
- `c-is-dir` PPPP **rc=0** — 4× `PASSED`; `test_outputs.py:84` `c_files = list(src_dir.glob("*.c"))`
  matches a *directory* named `sim.c`.

Cross-channel samples (`ctrf/empty-tree.json`, `ctrf/path-split.json`, `ctrf/canned-shape.json`):
`{"tests":4,"passed":0,"failed":4}` / `{"tests":4,"passed":4,"failed":0}` / idem. No case showed a
`-rA`-vs-ctrf divergence (`NOTE parse-divergence` never printed).

### 3.1 The receipt itself is reproducible on this host

`python3 plans/build_pmars_probe.py --lane "$S/lane" --work "$S/w2"` → `cmp` against the frozen receipt:
**byte-identical**, `sha256 = 2408b477…ef9` on both sides (`frozen-rerun.txt`, 5537 bytes = receipt size).
So the agreement above is not attributable to host drift (gcc 16.2.1, glibc, bash-as-`/bin/sh`).

## 4. Findings (impact on what the C2 entry may say)

**F1 — CONFIRMED, no defect in the receipt's letters.** Real pytest 8.4.1 reproduces every one of the 22
frozen letters and every exit code, so the seven headline observations the entry will carry
(canned-shape, canned-x11-dlopen, results-trailing-text, canned-exit-nonzero, path-split, debian-is-file,
c-is-dir all `PPPP` → `reward=1`) are verifier-true, not harness artefacts. The direct-call harness is a
valid proxy **for this grader**.

**F2 — the receipt's `error=` annotations must not be described as pytest ERRORs.** Two cases carry
`test_headless_no_x11:error=CalledProcessError` (`empty-tree`, `canned-script`) and one carries
`test_pmars_works:error=CalledProcessError` (`nonexec-binary`). Under pytest a raise inside a test body is
`FAILED`, never `ERROR` (ERROR is fixture/collection), and the ctrf plugin records `"status":"failed"`
(`ctrf/empty-tree.json`). The `error=<Class>` text is the *probe harness's* label (`plans/build_pmars_probe.py`
prints `TEST name F error=...`). Impacted: any sentence in the S115/S116 row prose or the entry body that
says a test "errors"; say **"fails"** and, if the class matters, "fails with `CalledProcessError`".

**F3 — the harness substitution has a demonstrated boundary, which the entry must not overstate.** The frozen
harness catches `Exception` only, so a `BaseException` escapes it and kills the harness mid-run; the frozen
probe then aborts the whole receipt (`if rc != 0 or set(got) != set(TESTS) … return 2`). Demonstrated with a
synthetic 4-test file (not the grader): `sem/direct_baseexc.txt` =
`TEST test_a P` then `direct_rc=7` (two verdicts never produced); `sem/pytest_baseexc.txt` =
`1 failed, 2 passed`, `pytest_rc=2`. Impacted: any claim that "the receipt's letters are what pytest says"
in general — true for this grader (no test raises `BaseException`, none skips/xfails), not a general
equivalence. Word it as "for these four tests and these cases", not as a property of the harness.

**F4 — inert differences, no letter impact (checked, not assumed).** My `/tests` is read-only and the env
carries `PYTHONDONTWRITEBYTECODE=1`, so pytest's assertion rewriting and its cache provider are inactive;
rewriting only adds assertion introspection, and collection still succeeded (`collected 4 items`). pytest's
fd capture points fd 0 at `/dev/null`, whereas the frozen harness inherits stdin — harmless here because the
only stdin producers are the grader's own `echo -e … | pmars` pipelines and every frozen artefact ignores
stdin (`C_SRC` in `plans/build_pmars_probe.py:151-172` contains no `read`/`scanf`/`getchar`; the only
`stdin` token in the probe is docstring text at `:34`).

**F5 — shell: the real container is dash, my sandbox and the freeze run are bash; still no letter impact.**
Debian `dash` (extracted from `dash_0.5.12-12_amd64.deb`, deb.debian.org) makes
`echo -e "s\ns\ns\nq"` print an extra literal `-e s` line, where bash does not — the exact hazard the frozen
probe names in its docstring. It cannot move a verdict: the extra line is only ever read by a canned artefact
that reads no stdin. Not tested in-sandbox (no dash in the frozen `/usr` and I did not modify the layout);
stated as an argument, not as a run.

## 5. Smallest safe corrections

1. Entry prose (S115/S116 rows + body): replace any "errors"/"ERROR" wording for the three
   `error=CalledProcessError` cases with "**fails** — pytest reports `FAILED`, ctrf `failed`" (F2). This is
   a wording fix; no receipt, table or counter changes.
2. Where the entry says the receipt's letters are pytest-faithful, scope it: "the four tests in
   `tests/test_outputs.py`, cases …" (F3). Optionally cite this seat's run
   (`pytest-agree 22/22`, 7×rc=0 / 15×rc=1) as the warrant.
3. Nothing to change in `plans/build_pmars_probe.py`, the captures, the dry table, or the receipt: their
   letters are verifier-true (F1). The `error=` field is probe-internal and accurate **as a probe field** —
   leave the frozen bytes alone; constrain only the prose that reads them.
4. If a later round wants the pytest check to be re-runnable from the lane, land
   `build_pmars_probe_pytest.py` as a NEW file (e.g. `plans/build_pmars_probe_pytest.py`) with the
   `--venv` / `--ctrf-out` flags as written; it imports the frozen probe and needs no edits to it.

## 6. What I did not do

- Did not execute the oracle `solve.sh` (needs root/apt/network), did not fetch the Docker image, did not
  run distro `dash` inside the sandbox.
- Did not use the counter (`round38_c2_verify.py`), the gate, the spec, or C1 batteries — out of this seat.
- Did not judge, admit, integrate or ship. The only artifacts I created are under this directory.
- Observation, not a finding: `git status --porcelain` in the lane during my cleanup showed one untracked
  lane file I did not create — `plans/mutant_direction_check.py`, mtime `2026-10-26 02:50:24`, an N21
  direction check. Owner is another seat; the L1 should confirm it is theirs and integrate or delete it.

## 7. Scratch

`/fast/scratch/hyaku/kengaku-r38/R38CritPytest` (clone `lane/`, venv, `w*` work dirs, dash `.deb`) —
removed:

```
trap 'rm -rf -- /fast/scratch/hyaku/kengaku-r38/R38CritPytest' EXIT   # executed
ls /fast/scratch/hyaku/kengaku-r38/R38CritPytest  ->  No such file or directory
```

## 8. Files here

`pytest-all.txt` (22 cases, 3 channels, per-test raw lines) · `pytest-run2.txt` (determinism) ·
`frozen-rerun.txt` (frozen probe rerun; byte-identical to the receipt) · `receipt.diff` (empty) ·
`ctrf/*.json` (22) · `sem/` (BaseException boundary demo: `test_baseexc.py`, `direct.py`,
`direct_baseexc.txt`, `pytest_baseexc.txt`) · `build_pmars_probe_pytest.py` (draft probe).

Impacted axes: C2 fidelity of the receipt's `tests=` letters (confirmed), receipt field semantics
(`error=` vs pytest `FAILED`, wording defect), harness-substitution scope (boundary demonstrated).
C1, the gate, the spec, the dry table, the captures and the counters: untouched.

VERDICT: pytest-agree-22/22
