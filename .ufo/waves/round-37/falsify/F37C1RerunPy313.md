# F37C1RerunPy313 — C1 re-run under other interpreters and hash seeds

Seat: executor, wave 2 (falsify). Target: item F37C1RerunPy313 — re-run the frozen C1 counter on a clean
clone of `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5` under Python 3.13 and 3.12 with `PYTHONHASHSEED=1`
and `99`; any difference in the `BATTERY`/`MUTANTS` lines is a determinism finding.

Fixture: `S=/fast/scratch/hyaku/kengaku-r37/F37C1RerunPy313`, `export TMPDIR=$S`,
`git clone -q --no-local <lane> "$S/fx/lane"` + `git -C "$S/fx/lane" checkout -q 357deceb…`; verified
`git -C "$S/fx/lane" rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r37/F37C1RerunPy313/fx/lane`,
`HEAD=357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`, `git status --porcelain | wc -l` = `0`. Lane files were
never edited; every counter run happened in the clone; `git status --porcelain` in the clone after the 9
runs is still empty. Receipts copied to `.ufo/waves/round-37/falsify/F37C1RerunPy313/`.

## Axes tested

| # | interpreter | flags / env | wall |
|---|---|---|---|
| 1 | CPython 3.14.8 (`/usr/bin/python3`, the unqualified `python3` of the frozen predicate) | `PYTHONHASHSEED=1` | 68 s |
| 2 | CPython 3.13.16 (uv) | `PYTHONHASHSEED=1` | 68 s |
| 3 | CPython 3.13.16 (uv) | `PYTHONHASHSEED=99` | 68 s |
| 4 | CPython 3.13.16 (uv) | `PYTHONHASHSEED=1`, repeat of #2 | 68 s |
| 5 | CPython 3.13.16 (uv) | `-O` (asserts stripped), seed 1 | 68 s |
| 6 | CPython 3.12.15 (uv) | `PYTHONHASHSEED=1` | 68 s |
| 7 | CPython 3.12.15 (uv) | `PYTHONHASHSEED=99` | 68 s |
| 8 | CPython 3.12.15 (uv) | `LC_ALL=C LANG=C`, seed 99 | 68 s |
| 9 | PyPy 3.11.16 (uv, JIT) | `PYTHONHASHSEED=1` | 135 s |

Commands (cwd `$S/fx/lane`, `TMPDIR=$S`):

```
uv run --no-project -p 3.13 python3 plans/round37_c1_verify.py --lane .
uv run --no-project -p 3.12 python3 plans/round37_c1_verify.py --lane .
uv run --no-project -p pypy@3.11 python3 plans/round37_c1_verify.py --lane .
python3 plans/round37_c1_verify.py --lane .            # 3.14, predicate's own python3
```

Interpreter identity was proven, not assumed — `uv run --no-project -p 3.13 python3 -c 'import sys,platform;print(sys.version.split()[0], sys.executable, platform.python_implementation())'`
→ `3.13.16 /home/vgpnk/.local/share/uv/python/cpython-3.13.16-linux-x86_64-gnu/bin/python3 CPython`;
`-p 3.12` → `3.12.15 …/cpython-3.12.15-linux-x86_64-gnu/bin/python3 CPython`; `-p pypy@3.11` →
`3.11.16 PyPy /home/vgpnk/.local/share/uv/python/pypy-3.11.16-linux-x86_64-gnu/bin/python3`. The counter
spawns the gate with `sys.executable` (`plans/round37_c1_verify.py`, `run_gate`), so each row above ran the
gate and all 55 mutants under that interpreter — not only the counter itself.

Seed propagation was proven too:
`env PYTHONHASHSEED=99 uv run --no-project -p 3.13 python3 -c '…subprocess.run([sys.executable,"-c","…os.environ.get(\"PYTHONHASHSEED\")…"])…'`
→ `parent seed=99 child='99 3.13.16'`, so the seed reached the gate subprocesses rather than dying at the
counter.

## Result — no determinism finding

All nine runs printed byte-identical stdout: `sha256sum` of every capture = `651bcf5455a7586fce3548ba3d298cee6a9da69a2a19fb5f1fd3403b93ee500d`,
123 lines, and `diff rpypy_seed1.txt r313_seed1.txt` → rc 0, 0 lines.

```
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

exit 0 in all nine (`exits.txt`, `exits2.txt`). The *kill attribution* is also invariant, not just the
tally: `diff <(grep -o 'killed by=[^ ]*' 3.13) <(grep -o 'killed by=[^ ]*' pypy)` → identical, 55 lines, so
the same fixture kills the same mutant under every interpreter (e.g. `M01 … killed by=r36-P5`,
`M10 … killed by=p4-capture-unreadable`, `M55 … killed by=d5-m55-quote-absent`).

Tip transfer: the integration receipt `.ufo/waves/round-37/integrate/measure-final.txt` is headed
`TIP 5c7d5d75…`; its C1 body (lines between the `$ python3 plans/round37_c1_verify.py --lane .` line and
`exit=0`) is byte-identical to my fresh 3.14/3.13/3.12/PyPy body —
`diff <(tail -n +2 receipt_c1 | head -n -1) r313_seed1.txt` → `RECEIPT-BODY-IDENTICAL`. So the C1 measurement
does transfer from `5c7d5d75` to the assigned tip `357deceb`, and the gate is at its freeze digest in both
(`sha256sum plans/pkg_gate.py` → `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`, matching
`GATE_SHA256` in the counter and the claim's freeze digest; `plans/round37_c1_verify.py` itself →
`dbc9f7199381f5bbd708458bedc45cd199cee38a6440a2968a886229173413cc`).

## Why "same" is the right reading, and what it does not prove

The instrument is order-insensitive *by construction*, which is exactly why these axes cannot move it:
defect sets are compared as `frozenset(...)` and printed through `','.join(sorted(...))`
(`plans/round37_c1_verify.py`, `run_gate` / `main`), mutant kill attribution is `differs()`'s first
differing fixture over `built`, and `built` follows list order plus `sorted(bdir.glob("*.py"))` in
`battery37_fixtures`. No battery37 module reaches for `random`, `datetime`, `os.environ`, `locale`, `hash()`
or an unsorted set — `grep -nE "datetime|random|uuid|locale|hash\(|set\(|sorted\(|os\.environ|tempfile" plans/battery37/*.py`
returns only `p5.py:48 names = set()`, `p5.py:75 sorted(ctx.spec["rows"])[0]`, `p6.py:100` (a `set` equality
test), `p8.py:66 sorted(...)[-1]` — all order-stable. The seed/interpreter axes therefore test *behavioural*
portability (does the gate reach the same verdict under another runtime), which they do; they cannot, on
their own, expose a latent order dependence that the printing path has already normalised away. This is a
limit of what a rerun can falsify here, not a defect found.

`-O` and `LC_ALL=C` were run as extra falsifiers of the same kind (assert stripping, locale-dependent
`re`/`str` behaviour): byte-identical, so neither the counter nor the gate hides its verdict behind an
`assert` or the ambient locale.

## Risks / notes

- `uv` (0.13.0) resolved existing interpreters; I additionally installed `pypy-3.11.16` via
  `uv python install pypy@3.11` (channel: official python-build-standalone, into
  `~/.local/share/uv/python`; reason: third runtime for the interpreter axis). No pacman transaction, no
  host service touched.
- Timing: the CPython runs take ~68 s and PyPy ~135 s per full sweep (~3.8 k gate subprocesses), so the
  counter's 900 s gate timeout and the probe's 600 s limit are not near enough to make a slow interpreter
  masquerade as a result. PyPy's 2× wall clock is JIT startup per subprocess, not a behavioural difference.
- Nothing in the lane, its index or its jj state was written; the falsify tree holds only this report and
  the nine stdout captures plus `MATRIX.txt`, `pypy.diff`, `receipt_c1.txt`, `exits*.txt` under
  `.ufo/waves/round-37/falsify/F37C1RerunPy313/`.

VERDICT: c1-rerun-interpreters-same
