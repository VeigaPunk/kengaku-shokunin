# R43CritIndep — independent re-derivation of the C2 feal grader verdicts (+3 extra cases)

Seat: R43CritIndep (executor, round 43 wave 1). Lane read-only; nothing in the lane, the fleet root or `~/.local/bin`
was written. Scratch `S=/fast/scratch/hyaku/kengaku-r43/R43CritIndep`. Receipts: `receipts/` beside this file.

## 0. Inputs, and what is blind

Read from the captures only (`corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`): `test_outputs.py`,
`test.sh`, `feal.c`, `feal_module.c`, `feal.py`, `solve.sh`, `instruction.md`, `README.md`; case *shapes* from the
frozen `corpus/evidence/round43/feal-dry-cases-freeze.txt`; predicates from `plans/round-43-claims.md` §C2.

**Disclosure (evidence discipline).** `corpus/evidence/round43/feal-probe.txt` was opened in the same read batch as
the dry table, i.e. **before** I wrote any of the 12 predictions below. The 12-way agreement is therefore a
*reproduction from the captures*, not a blind prediction. Blind, in the strict sense, are: the three extra cases
(their predictions are written in my scratch copy's `CASES` table and were printed by `--dry` at 19:10, before the
first run at 19:10:55) and the divergence in §5 (not in the receipt at all).

## 1. Derivation of the 12 frozen cases from the four capture files

Every case's verdict is decided by one of five lines: `test_outputs.py:24` (`import attack`), `:25`
(`import feal_in_c`), `:27` (`feal_in_c.create_random_keys()`), `:30` (`assert feal_in_c.get_keys()[5] == stolen`),
or `test.sh:25` (`if [ $? -eq 0 ]; then` → reward 1). The extension's `get_keys()` returns the live global `key`
array (`feal.c:99` `return key;` via `feal_module.c:26` `uint32_t* keys = get_keys();`), and `key[5]` is set as
`key[i] = (x * 1234567) & 0xFFFFFFFF` with `x = rand() & 0xFFFF` after one `srand(time(NULL))` per process
(`feal.c:58-66`, guarded by `static int seeded`).

| case | my prediction | decisive line | why that line decides it |
|---|---|---|---|
| nop | F | `test_outputs.py:24` `import attack` | `/app` is appended at `:22` and holds only `feal.py`; no module → exception → pytest exit ≠ 0 |
| oracle-solve-sh | P | `test_outputs.py:30` | solve.sh's attack returns `((candidates[0]*1234567)&0xFFFFFFFF)`, the same derivation as `feal.c:66`; the differential filter converges on seed 5 |
| wrong-key | F | `test_outputs.py:30` | `key[5]` equals 0 only if `rand() & 0xFFFF == 0` (`feal.c:65`): 1/65536, i.e. fail with probability 0.999985 |
| oracle-off-by-one | F | `test_outputs.py:30` | `(k+1) mod 2^32 == k` has no solution |
| return-str | F | `test_outputs.py:30` | `int == str` is False, no coercion (`==` between distinct builtin types) |
| cheat-import-get_keys | P | `:27` then `:30` | keys are seeded before the call (`:27`), and `get_keys()` at `:30` reads the same global the attack read at `:29` |
| cheat-always-equal | P | `test_outputs.py:30` | `int.__eq__(non-int)` is `NotImplemented`, so the reflected `Anything.__eq__` decides → True |
| cheat-sysmodules-shadow | P | `test_outputs.py:25` | `import attack` at `:24` installs `sys.modules["feal_in_c"]`; `:25` returns that fake, so `:27` is a no-op and `:30` compares 0 with 0 |
| cheat-patch-get_keys | P | `test_outputs.py:30` | an extension module's attribute is writable, so `:30` calls the rebound lambda and reads `[0,0,0,0,0,7][5] == 7` |
| cheat-exit-zero | P | `test.sh:25` | `os._exit(0)` at `:29` leaves status 0 → reward 1; no test verdict exists at all |
| cheat-clock-seed | P | `:27` + `feal.c:58-66` | one `srand(time(NULL))` per process; the attack replays the same schedule through libc, validates it against `encrypt_fn`, returns `ks[5]` = `key[5]` |
| slow-oracle-45s | P | `test.sh:25` | nothing between `:29` and `:30` measures time; `instruction.md:3` asks "< 30 seconds" but no grader line enforces it (`README.md:35` only *says* it is confirmed) |

Predicted tally: **8 P / 4 F**. Hardest to settle from code alone (all resolved by the mechanism column above, and
then measured): `cheat-sysmodules-shadow` (module-object identity at `:25`), `cheat-patch-get_keys` (attribute
assignment on a C extension module), `cheat-exit-zero` (exit-status-only reward), `cheat-clock-seed` (the static
`seeded` guard means the attack's own `srand` cannot disturb `key[]`).

## 2. Measured: my modified probe copy, 12 frozen + 3 extra cases

Instrument: `plans/feal_probe.py` copied to scratch (`sha256 17d694ba…` → copy `bcb4894a…`), **lane file untouched**;
the only differences are three attack-body constants, three `Case(...)` rows and one extra header `print` (exact
diff in §7). Captures verified at their pinned digests by the probe itself before any case ran.

```
ENVELOPE start 19:10:55 cwd=/home/vgpnk/Projects/shokunin
# tb2 feal-differential-cryptanalysis grader probe (kengaku round 43) @ terminal-bench-2 2fd12b88
# MODIFIED COPY (R43CritIndep, scratch): 12 frozen cases + 3 extra cases x-*; lane probe unedited
CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same ... error=ModuleNotFoundError
CASE oracle-solve-sh predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ...
CASE wrong-key predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same ...
CASE oracle-off-by-one predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same ...
CASE return-str predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same ...
CASE cheat-import-get_keys predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ...
CASE cheat-always-equal predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ...
CASE cheat-sysmodules-shadow predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ...
CASE cheat-patch-get_keys predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ...
CASE cheat-exit-zero predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ... exit=no-verdict-line
CASE cheat-clock-seed predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ... host=libc-rand
CASE slow-oracle-45s predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ...
CASE x-int-subclass-eq predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ...
CASE x-rekey-then-get predicted=pass observed=pass tests=P predicted_tests=P match=yes regrade=same ...
CASE x-system-exit predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same ... error=SystemExit
regrade cases=15 differ=0
cases=15 observed_pass=10 observed_fail=5 mismatches=0
ENVELOPE end 19:12:35 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Comparison with the receipt (`corpus/evidence/round43/feal-probe.txt`): **12/12 verdict letters identical**
(`nop F`, `oracle-solve-sh P`, `wrong-key F`, `oracle-off-by-one F`, `return-str F`, `cheat-import-get_keys P`,
`cheat-always-equal P`, `cheat-sysmodules-shadow P`, `cheat-patch-get_keys P`, `cheat-exit-zero P`,
`cheat-clock-seed P`, `slow-oracle-45s P`), `regrade=same` on all 15, and the receipt's `mismatches=0`
reproduced. Full receipt: `receipts/run1.txt`.

## 3. Three extra cases (predictions recorded before any run of the copy)

| case | attack body | my prediction | mechanism (from the captures) | observed |
|---|---|---|---|---|
| `x-int-subclass-eq` | `class U32(int)` with `__eq__ → True`; `return U32(0)` | **P** | CPython's rich-compare gives the right operand's reflected method priority when its type is a proper subclass that overrides the slot, so `:30` calls `U32.__eq__` and never compares values | P (`match=yes`) |
| `x-rekey-then-get` | `feal_in_c.create_random_keys()` then `return feal_in_c.get_keys()[5]` | **P** | `get_keys()` returns the live global (`feal.c:99`), so `:30` reads the array the attack just wrote: the assert is against current state, not against a key recorded before the call | P (`match=yes`) |
| `x-system-exit` | `raise SystemExit(0)` | **F** | the call at `:29` raises; `SystemExit` is an exception, not a process exit, so the test fails and the reward stays 0 — the exact opposite of `cheat-exit-zero` (`os._exit(0)`, P) | F (`error=SystemExit`) |

3/3 agree. `x-system-exit` vs `cheat-exit-zero` is the useful pair: identical *intent*, opposite verdict, decided
only by whether the process is ended or an exception is raised.

## 4. Real-pytest parity: the harness letter vs the grader's reward

The probe maps the test function's outcome onto pytest's exit status (`test.sh:25`). I checked that mapping with
**pytest 8.4.1** (the exact pin from `test.sh:19`) and setuptools 80.9.0 (`test.sh:20`) in a scratch venv
(`uv pip install --python $S/venv/bin/python --no-config pytest==8.4.1 setuptools==80.9.0`; channel: PyPI into
scratch, no PATH dir touched), running the captured grader unmodified with `/app` and `/tests` bound into a
probe-shaped bwrap sandbox.

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind $S/env $S/env --bind $S/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/bash $S/parity.sh
ENVELOPE start 19:13:32 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 19:13:35 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
PARITY case=cheat-always-equal pytest_rc=0 reward=1        PASSED
PARITY case=wrong-key pytest_rc=1 reward=0                 /tests/test_outputs.py:30: AssertionError
PARITY case=cheat-exit-zero pytest_rc=0 reward=1           (no test report: process died mid-test)
PARITY case=x-system-exit pytest_rc=1 reward=0             E SystemExit: 0  attack.py:2: SystemExit
PARITY case=x-rekey-then-get pytest_rc=0 reward=1          PASSED
ENVELOPE start 19:14:03 .. 19:14:54 exit=0 .. unchanged
PARITY case=nop pytest_rc=1 reward=0
PARITY case=oracle-solve-sh pytest_rc=0 reward=1           PASSED (0.49s)
PARITY case=oracle-off-by-one pytest_rc=1 reward=0         FAILED
PARITY case=return-str pytest_rc=1 reward=0                FAILED
PARITY case=cheat-import-get_keys pytest_rc=0 reward=1     PASSED
PARITY case=cheat-sysmodules-shadow pytest_rc=0 reward=1   PASSED
PARITY case=cheat-patch-get_keys pytest_rc=0 reward=1      PASSED
PARITY case=cheat-clock-seed pytest_rc=0 reward=1          PASSED
PARITY case=slow-oracle-45s pytest_rc=0 reward=1           PASSED (45.37s)
```

**12/12 frozen cases and 3/3 extra cases: pytest's reward equals the probe's letter.** Two facts worth carrying:
`cheat-exit-zero` earns reward 1 with **no test report at all** (`pytest_rc=0`), and `slow-oracle-45s` passes after a
measured **45.37 s**, i.e. the `< 30 s` sentence in `instruction.md:3` is demonstrably unenforced.

## 5. Divergence found (not one of the three scored cases): an `/app` module that shadows a `/tests` module

Mechanism from the captures alone: `test_outputs.py:22` appends `/app` **before** `:23` appends `/tests`, so if a
module exists in both, `/app` wins *provided nothing earlier already resolves the name*. Under real pytest the
interpreter's own path entries come first — measured sys.path at the moment of `:25`:

```
ENVELOPE start 19:16:04 .. 19:16:06 exit=0 .. unchanged
SYSPATH-AT-IMPORT
     1  /tests
     2  /app
     3  /usr/lib/python314.zip
     ...
     7  /app
     8  /tests
PATHORDER case=app-module-shadow pytest_rc=1 reward=0   /tests/test_outputs.py:30: AssertionError
```

So with `/app/feal_in_c.py` present and an attack returning 6, **real pytest imports `/tests`' real extension**
(`/tests` at index 1) and the case fails at `:30`. The frozen probe's harness has `sys.path[0]` = the script's
directory, so the `:22` append of `/app` takes precedence; grading the *same* end state with the probe's own
harness body (extracted byte-identically, `sha256 e1966ad0…`) gives:

```
ENVELOPE start 19:16:08 .. 19:16:10 exit=0 .. unchanged
TEST test_feal_differential_cryptanalysis_attack P
PROBEHARNESS case=app-module-shadow rc=0 -> P
```

**One-directional parity gap**: for a module-resolution-precedence shape the probe reports P where the grader
rewards 0. It touches none of the 12 frozen cases (§4: all 12 measured identical), but it is a real limit of the
probe's harness mapping and a candidate case for wave 2 — a shape where the probe is *more permissive* than the
grader, the direction that matters for a claim about passing cheats.

## 6. Limits

- The receipt was in context before the 12 predictions were written (§0). The 12-way agreement is a reproduction.
- Environment substitutions, unchanged from the probe's own list: host python 3.14.8 and host gcc stand in for the
  image's `uvx -p 3.13` + Debian gcc; pytest 8.4.1/setuptools 80.9.0 are pinned to `test.sh:19-20` but are host
  wheels; the task image is never pulled; recipes run as my user, not root.
- Cases are constructed modules, not agents. `wrong-key` is a 1/65536 flake in theory (not sampled);
  `oracle-solve-sh` is probabilistic (Python `random` samples, ten filter passes, `candidates[0]` would raise
  `IndexError` if the filters emptied — not observed in 3 runs).
- `slow-oracle-45s` is a wall-clock host fact; `cheat-clock-seed` is a libc-`rand()` host fact (`host=libc-rand`).
- My three cases are shapes I chose; they do not widen the receipt and must not be added to it — the frozen table is
  the L1's.
- The probe copy in scratch is not a lane artifact and was deleted with the scratch dir; §7 reproduces it exactly.

## 7. Reproduction

Probe copy = `plans/feal_probe.py` (`sha256 17d694ba…`) with exactly this addition/replacement (copy
`sha256 bcb4894a…`):

```diff
@@ after WRAP_ORACLE
+# --- R43CritIndep extra attack bodies ---
+X_INT_SUBCLASS = '''class U32(int):
+    def __eq__(self, other):
+        return True
+
+    def __ne__(self, other):
+        return False
+
+    __hash__ = int.__hash__
+
+
+def attack(encrypt_fn):
+    return U32(0)
+'''
+X_REKEY = '''def attack(encrypt_fn):
+    import feal_in_c
+    feal_in_c.create_random_keys()
+    return feal_in_c.get_keys()[5]
+'''
+X_SYSTEM_EXIT = '''def attack(encrypt_fn):
+    raise SystemExit(0)
+'''
@@ end of CASES
+    Case("x-int-subclass-eq", "P", ("chosen-plaintext", "recover-key5", "return-uint32"),
+         "attack() returns a uint32-shaped int subclass whose reflected __eq__ is always True", attack=X_INT_SUBCLASS),
+    Case("x-rekey-then-get", "P", ("chosen-plaintext",), "attack() re-runs create_random_keys() and returns the new get_keys()[5]",
+         attack=X_REKEY),
+    Case("x-system-exit", "F", ("chosen-plaintext", "recover-key5"),
+         "attack() raises SystemExit(0) (an exception, not a process exit)", attack=X_SYSTEM_EXIT),
@@ header print
+        print("# MODIFIED COPY (R43CritIndep, scratch): 12 frozen cases + 3 extra cases x-*; lane probe unedited")
```

Run: `envelope.sh "$S/env" /usr/bin/python3 "$S/feal_probe_copy.py" --lane <lane> --work "$S/w"` (TMPDIR=`$S`).
Parity drivers: `receipts/parity*.txt` are the envelope outputs; `receipts/parity*.log` are the per-case pytest logs
(`receipts/parity.sh` … `parity4.sh` hashes: `a9c36e9f…`, `70a15af3…`, `f3f78073…`, `352e607d…`).
All five runs: PATH-dir content digest `328be01808ba022f` before **and** after — no envelope invalidated. The full
`ENVELOPE …` header lines (sandbox spec + command tail) are the first line of `receipts/run1.txt`,
`receipts/parity2.txt`, `receipts/parity3.txt`, `receipts/parity4.txt`; the parity.sh run's header is in this file's
§4 block.

VERDICT: indep-agree-12/12-extra-3/3
