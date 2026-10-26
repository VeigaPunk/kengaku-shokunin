# F38C1RerunPy313 — C1 counter under a different Python (round 38, wave 2 FALSIFY)

**Tip attacked:** `8c7422d7a646515d80af44844e8ecc8a1fc1d30a` (clean clone, `git rev-parse --show-toplevel` = the scratch
clone; `git status --porcelain --untracked-files=all` = 0 both before and after every run).
**Scratch:** `/fast/scratch/hyaku/kengaku-r38/F38C1RerunPy313/` (removed at exit).
**Receipts:** `.ufo/waves/round-38/falsify/F38C1RerunPy313/receipts/`.
**Digests at the attacked tip:** `plans/round38_c1_verify.py` = `8069739990c7d3a87f34f4398ea5dc78821193d9fa55499e11e28c84e79c0a4f`,
`plans/pkg_gate.py` = `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`;
`sha256sum -c .ufo/waves/round-38/claims/frozen-digests.txt` → 8/8 `OK`, rc=0.

## 1. What was attacked

* Claims `plans/round-38-claims.md` §C1 brittle line: C1 "measured on a clean clone of the landing tip", predicate
  `MUTANTS total=22 killed=22 survived=0` / `PREDICATE C1 pass`.
* Landing receipt `.ufo/waves/round-38/integrate/measure-final.txt` (`MUTANTS total=22 killed=21 survived=1`,
  `PREDICATE C1 fail`) — reproduced **line by line** on a different interpreter.
* Counter docstring claim that it is interpreter-agnostic by construction: `run_gate` spawns the gate as
  `sys.executable` (`plans/round38_c1_verify.py:179`), and the gate spawns its probe as `sys.executable`
  (`plans/pkg_gate.py:274`). A "same" verdict is worthless if the copies are re-executed under a fixed interpreter,
  so non-vacuity was measured with `strace -f -e trace=execve`, not inferred.

## 2. Method

```
S=/fast/scratch/hyaku/kengaku-r38/F38C1RerunPy313
git clone -q --no-local <lane> "$S/lane" && git -C "$S/lane" checkout -q 8c7422d7a6...
export TMPDIR="$S"; mkdir -p "$S/work-<variant>"
<interpreter> plans/round38_c1_verify.py --lane . --work "$S/work-<variant>"
```

| variant | interpreter | command |
|---|---|---|
| py313 | CPython 3.13.16 (uv-managed) | `uv run --no-project -p 3.13 python plans/round38_c1_verify.py --lane . --work …` |
| py312 | CPython 3.12.15 (uv-managed) | `uv run --no-project -p 3.12 python …` |
| py314 | CPython 3.14.8 (`/usr/bin/python3`, the host interpreter the receipt used) | `python3 plans/…` |
| pypy311 | PyPy 8.0.0 / Python 3.11.16 | `…/pypy3.11 plans/…` |
| hs0 / lc / iso / abs / uvpy312 / strace | 3.13.16 variants | `PYTHONHASHSEED=0`; `PYTHONHASHSEED=987654321 LC_ALL=C LANG=C TZ=UTC`; `-I -B`; `cd / && <abs path> --lane <abs>`; `UV_PYTHON=3.12`; under `strace -f` |
| ascii | 3.13.16 | `PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=C LANG=C` |
| nouv | 3.13.16 | `PATH=/usr/bin:/bin` (no `uv`) |
| at-d93 | 3.13.16 | run at the receipt's own `TIP d93b7d6` |

## 3. Result — identical, not merely equivalent

Eleven runs at `8c7422d` (py313, py312, py314, pypy311, hs0, lc, iso, abs, uvpy312, strace, and the traced pypy run)
produce **the same 112 lines**:

```
$ sha256sum c1-py313.txt c1-py312.txt c1-py314.txt c1-pypy311.txt c1-py313-hs0.txt c1-py313-lc.txt \
            c1-py313-iso.txt c1-py313-abspath.txt c1-py313-uvpy312.txt c1-py313-strace.txt c1-pypy311-strace.txt
5ec311a0842bfa31644ee1c51d8b65e5183bbaa5a0511f1751afbe366e796469  (×11)
exit=1   PINS total=14 mismatched=0
         BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
         MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
         PREDICATE C1 fail
```

Line-by-line against the receipt: `measure.sh`'s `r()` wrapper adds the trailing `exit=$?` line, so the receipt C1
block is 113 lines and the counter emits 112. Stripping the wrapper line:

```
$ head -n -1 out/receipt-c1-body.txt > out/receipt-c1-body-noexit.txt
$ sha256sum out/receipt-c1-body-noexit.txt out/c1-py313.txt
5ec311a0842bfa31644ee1c51d8b65e5183bbaa5a0511f1751afbe366e796469  out/receipt-c1-body-noexit.txt
5ec311a0842bfa31644ee1c51d8b65e5183bbaa5a0511f1751afbe366e796469  out/c1-py313.txt
$ diff -u out/receipt-c1-body-noexit.txt out/c1-py313.txt ; echo $?
0
```

0 of 112 lines differ, including every `FIXTURE … ok`, every `MUTANT … killed by=…` attribution string and the
`MUTANTS total=22 killed=21 survived=1` line. `N21 D5 silence SURVIVED` is the single survivor under all four
interpreters — the honest stop is interpreter-stable.

## 4. Non-vacuity — the copies really ran under each interpreter

```
$ strace -f -qq -e trace=execve -o execve-py313.txt <cpython-3.13.16> plans/round38_c1_verify.py --lane . --work …
$ grep -o 'execve("[^"]*"' execve-py313.txt | grep -E 'pypy|python' | sort | uniq -c | sort -rn | head -2
   1372 execve("/home/vgpnk/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13"
      1 execve("…/uv-cache/builds-v0/.tmpXXXX/bin/python3"          (P10 probe children, one per fixture)
$ grep -c 'execve("/usr/bin/python3"' execve-py313.txt
0
$ grep 'python3.13"' execve-py313.txt | sed -n '2p' | cut -c1-160
59825 execve("…/cpython-3.13…/bin/python3.13", ["…", "package", "--root", "…", "--require-clean-tree", "--spec", …
```

```
$ strace -f -qq -e trace=execve -o execve-pypy.txt <pypy3.11> plans/round38_c1_verify.py --lane . --work …
   1372 execve("/home/vgpnk/.local/share/uv/python/pypy-3.11.16-linux-x86_64-gnu/bin/pypy3.11"
$ grep 'pypy3.11"' execve-pypy.txt | sed -n '2p' | cut -c1-200
1431713 execve("…/pypy3.11", ["…", "package", "--root", "…", "--require-clean-tree", "--spec", …
```

The 1372 spawns per run are the gate copies (86 fixtures × reference + 22 mutants ≈ the observed count), each with
the gate's `package`/`d4-line`/`d5-line` argv, and each under the parent interpreter. The identity in §3 is
therefore a measurement, not a tautology.

## 5. Findings that landed

### F1 — the landing receipt is one commit behind the tip it is cited for (bookkeeping; numbers survive)

`measure-final.txt:1` says `TIP d93b7d68dacfd6a23ec2cf732a4615d6c732c73e`; the tip under attack is `8c7422d7…`,
whose parent is `d93b7d6` (`git log --oneline -3` in the clone: `8c7422d`, `a022ae6`, `d93b7d6`; commit `a022ae6`'s
subject reads "landing measurement on a clean clone of d93b7d68"). The claims' predicate says the count is
"measured on a clean clone of the landing tip". It was measured on the tip's parent.

```
$ git diff --stat d93b7d6 8c7422d -- plans corpus
 corpus/lessons/round-38.md | 77 ++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 77 insertions(+)
```

Nothing in the C1 read set changed (no pinned file, no battery, no knowledge file, no README row), and I closed the
gap by measurement rather than argument: the counter at `d93b7d6` and at `8c7422d` is byte-identical
(`diff -u c1-py313.txt c1-py313-at-d93b7d6.txt` → rc 0), and the `d93b7d6` run is byte-identical to the receipt body
(§3). **Attack landed on the receipt's provenance line, not on its numbers.** The next landing should re-run
`measure.sh` after the final commit or label the receipt with the tip it actually measured.

### F2 — three of the 22 mutants never test the counter's interpreter (scope limit of this result)

`import Bio` fails in every interpreter on this host (3.14, 3.13, PyPy: `ModuleNotFoundError: No module named 'Bio'`),
so `c_rerun` always takes the fallback `["uv","run","--no-project","--with","biopython==1.85","python3"] + probe`
(`plans/pkg_gate.py:276`). The traces show the probe child as
`execve("…/uv-cache/builds-v0/.tmpXXXX/bin/python3", ["python3","plans/tb2_grader_probe.py","--lane","."])` — a
uv-built interpreter, never the counter's. So N13/N14/N15 (P10) exercise a fixed host interpreter in every run; their
constancy is expected, not evidence. The other 19 mutants do run under the parent interpreter (§4).

Cross-check that this does not hide a version-sensitive P10: forcing the probe child to 3.12 (`UV_PYTHON=3.12`) still
yields the identical 112 lines (`c1-py313-uvpy312.txt`, same sha), so the probe output is version-blind as well.

### F3 — both artifacts silently assume a UTF-8 default encoding; the failure is closed, not open

```
$ PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=C LANG=C cpython-3.13.16 plans/round38_c1_verify.py --lane . --work …
PINS total=14 mismatched=0
Traceback … File "plans/round38_c1_verify.py", line 220, in main
    gate_src = (lane / r37.GATE_REL).read_text() if (lane / r37.GATE_REL).is_file() else ""
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 in position 1105: ordinal not in range(128)
exit=1
```

Byte 1105 of `plans/pkg_gate.py` is `e2 80 9c` (a `U+201C` in the docstring; `dd if=plans/pkg_gate.py bs=1 skip=1095
count=30 | od -An -tx1c`). The pinned gate is fragile the same way:

```
$ LC_ALL=C PYTHONUTF8=0 cpython-3.13.16 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r35.json
setup: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe3 in position 2164: ordinal not in range(128)
rc=2
```

Plain `LC_ALL=C` alone does **not** trigger it (`sys.flags.utf8_mode 1`, PEP 540). Both paths fail closed: the counter
dies before printing `PREDICATE`, and the gate exits 2 so every fixture observes a non-expected rc (`wrong>0`). No
false pass exists here; the counter is simply not locale-independent in its file reads (`read_text()` with no
`encoding=`).

### F4 — the received `killed=21` is conditioned on `uv` being on `PATH` (fails closed; the count moves to 18)

`uv` resolves to `/home/vgpnk/.local/bin/uv` (0.13.0) but is absent from `/usr/bin:/bin`. With `PATH=/usr/bin:/bin`:

```
$ PATH=/usr/bin:/bin cpython-3.13.16 plans/round38_c1_verify.py --lane . --work …
BATTERY fixtures=86 wrong=1 renamed_disagree=0 sidechannel=0
FIXTURE p10b-rerun-byte-equal-accept expect=accept declared=- observed_rc=1 observed_defects=P10 WRONG
MUTANT N13 P10 silence SURVIVED …
MUTANT N14 P10 silence SURVIVED …
MUTANT N15 P10 mirror SURVIVED …
MUTANTS total=22 killed=18 survived=4 invalid=0 null_detected=0
PREDICATE C1 fail
exit=1
```

So the calibration number is environment-conditioned: 21 kills with `uv`, 18 without, always `PREDICATE C1 fail`. The
direction of the claim under attack (C1 is an honest stop) is stable; the number in the receipt is not portable to a
host without `uv` and network/cache for `biopython==1.85`. My runs used a cold `UV_CACHE_DIR` inside scratch (270
`uv` execs, biopython 1.85 fetched into it) and still reproduced the receipt byte for byte.

### F5 — hygiene holds (checked, not assumed)

`plans/battery38/__pycache__` is ignored (`.gitignore:2:__pycache__/`), so the counter's own module imports cannot
redden P9; the clone stayed at `0` in `git status --porcelain --untracked-files=all` after every run, and the frozen
digest check is 8/8 `OK` at `8c7422d`.

## 6. Limits

* CPython 3.8–3.11 and 3.15 were not exercised (3.15/3.10 are uv "download available"; I did not install or download
  interpreters — no host mutation, nothing filed to pacman). PyPy 3.11 stands in for the 3.11 line. A static scan for
  3.11+/3.12+ constructs in the counter, gate and `battery38/*.py` found none (`from __future__ import annotations`
  present; `str | None` in annotations only), so older CPythons are plausible but unmeasured.
* Identity is at the printed lines. The counter prints no interpreter identity, so §3 equally shows the output leaks
  no version; it does not show that unprinted internal branches (e.g. `re` or `pathlib` edge behaviour) are identical.
* I did not re-litigate the 21 attributions (sibling seats own that); I only confirm they reproduce verbatim under
  four interpreters and that N21 stays the sole survivor.
* `uv`, `git`, host bash and host glibc are assumed; the P10 arm additionally assumes network or a warm cache.

## 7. Environment / tools

Read `/home/vgpnk/.omp/agent/RULES.md` before running. **No installs and no upgrades were performed**: uv 0.13.0 and
the already-present uv-managed CPython 3.12.15 / 3.13.16 / PyPy 3.11.16 (/usr/bin/python3 3.14.8) sufficed, so nothing
was filed to pacman (transactions paused) and no service was touched. `strace` 6.x used read-only.

## 8. Retained evidence

`.ufo/waves/round-38/falsify/F38C1RerunPy313/receipts/` (484 KB):

```
5ec311a0842bfa31644ee1c51d8b65e5183bbaa5a0511f1751afbe366e796469  c1-py313.txt, c1-py312.txt, c1-py314.txt,
    c1-pypy311.txt, c1-py313-hs0.txt, c1-py313-lc.txt, c1-py313-iso.txt, c1-py313-abspath.txt,
    c1-py313-uvpy312.txt, c1-py313-strace.txt, c1-pypy311-strace.txt, c1-py313-at-d93b7d6.txt,
    receipt-c1-body-noexit.txt
aad46f7822fa9565cfac6bd68af3620f301f58338b0ba8818e9428b4eb7f9e84  c1-py313-ascii.txt
6cd5a7caffaac57df59213753d590cd2f11eba7151e16b4f62c93d8286a73588  c1-py313-nouv.txt
e6276feddc0a5b36ea1d2009d965337ecd3008df7b7cd2ccc4f470d29f4c4597  receipt-c1-body.txt (113 lines, with wrapper exit=)
4d4ef7e517fbe3870296e9c831d2f9200432e27ae1c7b21107ae23d9d25cd736  execve-py313.txt.gz
8cef9030ee808e279f12c90fc0d608c1cee6ef9b038e13df8f1e9055042735d2  execve-pypy.txt.gz
e7f3fc7b06749e57f3e067eeba1c42b52ba781747841f4dceae7fe076f7d878e  py313-version.txt
```

Scratch `/fast/scratch/hyaku/kengaku-r38/F38C1RerunPy313` was removed before this report was written.

VERDICT: c1-interpreters-same
