# R42CritPytest — real-runner parity for C2 (kengaku round 42, wave 1)

Seat: `R42CritPytest` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, clone tip
`fda71ae`. Scratch `S=/fast/scratch/hyaku/kengaku-r42/R42CritPytest` (removed on exit; `TMPDIR=$S`). No lane file was
written: `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `PROVINCE.md` are untouched, and no git/jj
mutation was attempted anywhere.

**Headline: 16/16 frozen end states and 48/48 test-node verdicts match the receipt `tests=` letters — under two
different real-pytest invocations, twice each. Zero differences, zero warnings.**

## Why this check exists (the gap it closes)

`corpus/evidence/round42/fibsqrt-probe.txt` was not produced by pytest. The frozen probe
(`plans/fibsqrt_probe.py`, `run_case` → `HARNESS_PY`) imports `tests/test_outputs.py` with
`importlib.util.spec_from_file_location` and calls the three test functions **directly**, mapping `AssertionError`
and any other exception to `F`. The task's `test.sh` instead runs `uvx -p 3.13 -w pytest==8.4.1 -w
pytest-json-ctrf==0.3.5 pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA` and derives `reward 1`
from pytest's exit status. So the receipt's authority for C2 (V9 compares the entry's `## Case table` against it)
rested on a re-implementation of the grader, not on the grader's runner. This seat replaced the runner and kept
everything else frozen.

## Method (frozen probe reused, only the runner swapped)

1. `git clone -q --shared <lane> $S/lane`; `git -C $S/lane rev-parse --show-toplevel` → `$S/lane`; tip `fda71ae`.
2. `pydriver.py` imports **the clone's copy** of `plans/fibsqrt_probe.py` (`importlib`, registered in `sys.modules`
   before `exec_module` — CPython 3.14 needs that for the frozen `@dataclass(frozen=True)`; 3.13 does not) and
   reuses its `Case` table/`CASES`, `PINS`, `GRADED`, `lookup()` content and its staging code verbatim: `/app` gets
   `sim.c` + the captured `gates.txt`, then the case's `gates` (replace / remove / `<dir>` / `<empty>`), its `sim`
   executable, and its `recipe.sh`. Probe digest at the clone
   `fc58bf3f1780aaefee9df1e635b01765d3fb5d9224f1958494df4e1b8ed061b3` = the frozen record
   `.ufo/waves/round-42/claims/frozen-digests.txt:4`. The probe was read only; its harness is not used for grading.
3. Interpreter/wheels obtained **outside** every sandbox (network): `uv venv -p 3.13 venv` → CPython 3.13.16;
   `uv pip install pytest==8.4.1` and `pytest-json-ctrf==0.3.5`. Inside-sandbox banner (from
   `pytest-out/lookup-28.run1.out`): `platform linux -- Python 3.13.16, pytest-8.4.1, pluggy-1.7.0 --
   $S/venv/bin/python`, `rootdir: /tests`, `collected 3 items`. Nothing was installed into any PATH directory.
4. Case sandbox per case = the probe's sandbox shape (`--unshare-net/pid/ipc`, `/usr` and `/etc` read-only, private
   `/tmp`, `/app` bound from the staged dir, `/tests` = `test_outputs.py` + `sim.c`, `/cap/solve.sh`, cwd `/app`),
   plus read-only binds so CPython 3.13 runs inside:
   `--ro-bind $S/venv $S/venv --ro-bind /home/vgpnk/.local/share/uv /home/vgpnk/.local/share/uv`.
5. The case recipe (`bash -euo pipefail /recipe.sh`, cwd `/app`; only `oracle-solve-sh` has one) runs **before**
   grading in the same sandbox, as in the probe. A non-zero recipe is a setup error, never a verdict.
6. Grading, two forms × two runs per end state, same env (`PATH` fixed, `HOME=/tmp`, `LANG=LC_ALL=C.UTF-8`,
   `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`):
   - **verbatim `test.sh` argv**: `-rA --ctrf /tmp/ctrf.json /tests/test_outputs.py` (only the ctrf path moved —
     there is no `/logs` in the sandbox; the plugin writes a report only). `plugins: json-ctrf-0.3.5` appears in
     32/32 logs of that form, so the shipped argv really ran.
   - **verbose node list**: `-v -p no:cacheprovider /tests/test_outputs.py`.
   A case verdict is `pass` iff all three nodes are `PASSED` (pytest exit 0 = `reward 1`).

## Parity table (verbose form; `receipt` = `tests=` of `corpus/evidence/round42/fibsqrt-probe.txt`)

`$S/pytest-out/*.run1.out` + `$S/pytest-parity.json`, printed by `parity_compare.py` (pasted verbatim):

```
case                         receipt  pytest  same  rc1 rc2 regrade  failing-node error classes
nop                          PPF      PPF     yes   1   1   PPF      -
oracle-solve-sh              PPP      PPP     yes   0   0   PPP      -
no-gates-file                FFF      FFF     yes   1   1   FFF      AssertionError
empty-gates-file             PPF      PPF     yes   1   1   PPF      -
lookup-28                    PPP      PPP     yes   0   0   PPP      -
lookup-27-drop-48401         PPF      PPF     yes   1   1   PPF      -
lookup-28-plus-examples      PPP      PPP     yes   0   0   PPP      -
lookup-28-bitflip-41         PPF      PPF     yes   1   1   PPF      -
lookup-28-padded-31999       PPP      PPP     yes   0   0   PPP      -
lookup-28-padded-32000       PFP      PFP     yes   1   1   PFP      AssertionError
lookup-28-comment-lines      PPP      PPP     yes   0   0   PPP      -
lookup-28-reversed-lines     PPP      PPP     yes   0   0   PPP      -
lookup-28-crlf               PPP      PPP     yes   0   0   PPP      -
lookup-28-trailing-space     PPF      PPF     yes   1   1   PPF      -
fake-sim-script              PPF      PPF     yes   1   1   PPF      -
gates-is-directory           PFF      PFF     yes   1   1   PFF      IsADirectoryError
parity cases=16 same=16 differ=0
receipt regrade column: ['same']
in-sandbox banner: python=3.13.16 pytest=8.4.1,
warning lines=0
```

Verbatim-`test.sh` form (`--ctrf`, `-rA`; `parity-testsh.txt`) prints the same 16 rows and
`parity cases=16 same=16 differ=0`; node-level detail strings are identical between the two forms for 16/16 cases.
`regrade=PPP|PPF|PFP|PFF` is the second grading of the same end state: identical in all 16, matching the receipt's
`regrade=same` column.

## Differences: none, and the shape of the agreement proves the mapping

- 48/48 node verdicts equal. The letters are positional over `test_gates_file_exists, test_gates_file_size,
  test_sqrt_fib`, and two rows carry a non-terminal `F` (`PFP` for `lookup-28-padded-32000`, `PFF` for
  `gates-is-directory`), so the agreement is not "everything matches the majority letter".
- Exception **classes** agree, not just failure letters: `gates-is-directory` → `E IsADirectoryError: [Errno 21] Is a
  directory: '/app/gates.txt'` at `/tests/test_outputs.py:20` (receipt: `test_gates_file_size:error=IsADirectoryError`);
  `no-gates-file` → `AssertionError: File /app/gates.txt does not exist`; `lookup-28-padded-32000` →
  `AssertionError: gates.txt has 32000 lines, but must have fewer than 32,000 lines` with `assert 32000 < 32000`.
- The probe's Y/N shaping is confirmed by the runner: `empty-gates-file` and `nop` fail only `test_sqrt_fib`,
  `lookup-28-trailing-space` fails it (copy lines stop scanning), `fake-sim-script` fails it although an executable
  `/app/sim` is present — the grader's `gcc -O3 /tests/sim.c -o sim` overwrote it.
- No pytest warnings were emitted in any of the 32 logs (`warning lines=0`), so assertion rewriting and the
  `subprocess` calls introduced no warning-level noise.

## Controls (the comparison is able to fail)

1. **Doctored receipt** — receipt copy with `lookup-28` `tests=PPP` → `tests=PPF`:
   `lookup-28 PPF PPP NO` and `parity cases=16 same=15 differ=1` (`parity-control.txt`).
2. **Missing receipt row** — receipt with the `nop` CASE line deleted: exit 2,
   `SETUP receipt parsed 15 cases, driver ran 16; cid sets differ: ['nop'] / []`. (The first draft of
   `parity_compare.py` had a greedy `.*tests=` regex that silently bound `predicted_tests=`; the doctored-receipt
   control is what exposed it, the regex is now anchored and the cid-set guard added.)
3. **Recipe matters** — `PYDRIVER_SKIPRECIPE=1`, case `oracle-solve-sh`: `pytest=PPF` (mismatch against the receipt's
   `PPP`), i.e. the same end state as `nop`; the receipt's oracle row is real only because `bash /cap/solve.sh` ran
   (`control-no-recipe.txt`). This is also the defect my first full pass had (it staged but did not execute the
   recipe): that pass printed `oracle-solve-sh PPF` while the receipt says `PPP`, and its scratch files were
   overwritten by the corrected run — the reasoning is reproducible with control 3.
4. **Runner identity** — `collected 3 items` in 32/32 verbose logs and 32/32 ctrf logs; `rootdir: /tests`; banner as
   above; `plugins: json-ctrf-0.3.5` in the ctrf form.

## Host guard / Q32 envelope

Every driver invocation, including the control, ran under

    bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
          --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 $S/pydriver.py …

| run | `date +%T` start → end | `ls -A /home/vgpnk/.local/bin \| sha256sum` before → after |
|---|---|---|
| full, verbose (evidence) | 17:23:44 → 17:24:52 | `436b361f…3c18` → `436b361f…3c18` |
| full, verbatim `test.sh` | 17:26:14 → 17:27:29 | `436b361f…3c18` → `436b361f…3c18` |
| control (no recipe) | 17:28:27 → 17:28:28 | `436b361f…3c18` → `436b361f…3c18` |

(The superseded 17:21:52 → 17:22:00 pass had the same before/after digest; baseline `436b361f…3c18` was also read at
17:20:58 before any run.) The case sandbox binds `/usr`, `/etc`, the venv and the uv CPython tree read-only and
mounts `/tmp` private; nothing was written outside `$S` and
`.ufo/waves/round-42/build/R42CritPytest/`. No host tool was installed into a PATH directory; the only installs were
into `$S/venv` (`pytest 8.4.1`, `pytest-json-ctrf 0.3.5`, CPython 3.13.16 via `uv 0.13.0`, channel `uv`).

## Artifacts (`.ufo/waves/round-42/build/R42CritPytest/`, 532K total, no file > 1 MiB)

| file | sha256 |
|---|---|
| `run-full.txt` (verbose, 16 CASE lines) | `df7ad0ed…eafb87` |
| `run-testsh.txt` (ctrf form) | `df7ad0ed…eafb87` (byte-identical: the driver prints the same derived columns) |
| `pytest-parity.json` / `pytest-parity-testsh.json` | `af3faf82…be635d` both |
| `parity.txt` / `parity-testsh.txt` | `37c0279e…d46bd30` both |
| `parity-control.txt` (doctored receipt) | `68916f37…099f8d2` |
| `control-no-recipe.txt` (control 3, with envelope lines) | `d30fa477…a5235` |
| `pytest-parity-only.json` (control-3 run, JSON form) | `703b1156…deed96c` |
| `pydriver.py` — the driver that produced the full-run evidence | `856fdfe9…df5c848` |
| `pydriver-with-controls.py` — same file plus the `-only` naming suffix and `PYDRIVER_SKIPRECIPE` switch | `d964e15f…e704ebf` |
| `parity_compare.py` | `c2c991e8…10cc3a39` |
| `pytest-out/` (32 raw verbose logs) | dir digest `52720f45…6540b48` |
| `pytest-out-testsh/` (32 raw ctrf logs) | dir digest `23534b80…44e363e` |
| `lookup-28.run1.out`, `gates-is-directory.run1.out` | `f4bd4165…7544e60`, `2ed52d54…ce2ed8e` |

Captures re-hashed before use, all equal to `PINS`: `test_outputs.py 6117b8ed…`, `sim.c 700645ac…`,
`gates.txt 032786f9…`, `solve.sh a4ffab41…`, `instruction.md a7f50026…`.

## Limits (stated, not claimed away)

- The task image `alexgshaw/circuit-fibsqrt:20251031` is never pulled; host **gcc 16.2.1** stands in for the image's
  Debian bookworm gcc, and the run is as the probing user, not root. The interpreter and pytest are the pinned
  versions the image's `test.sh` installs (3.13.16, 8.4.1), but they come from `uv`, not from the image layer.
- The ctrf report path is `/tmp/ctrf.json`, not `/logs/verifier/ctrf.json`; the plugin only writes a report, so
  verdicts are unaffected, and `reward.txt` is not written (pytest's exit code is recorded instead).
- Parity says the probe's direct-call verdicts equal real pytest's on these 16 end states. It does not say the probe
  would equal pytest on an end state where collection or fixture machinery matters (e.g. an import error in
  `test_outputs.py`, which the probe's `exec_module` would raise before any test and pytest would report as a
  collection `ERROR`); no such case is in the frozen set, and none was added — the case table is frozen.
- Integration hint for the L1 (no lane edit made): this is evidence the entry may cite beside the receipt — the
  `## Case table` rows are the same verdicts real pytest produces, in both shipped invocation forms.

VERDICT: pytest-parity-16/16
