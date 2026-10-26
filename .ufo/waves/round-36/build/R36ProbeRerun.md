# R36ProbeRerun — frozen `regex-log` probe re-run (round 36, wave 1, C2 freshness/operability)

Seat: R36ProbeRerun (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Assignment: re-run the frozen probe twice and `cmp` to the receipt; re-run under `uv run --no-project -p 3.13`,
`-p 3.12`, `-p 3.11` (each with `PYTHONHASHSEED=1` and `99`) and from a different cwd with an absolute `--lane`;
record every byte difference and its cause; run `plans/round36_c2_verify.py --lane .` read-only and paste its output.
No file under `corpus/`, `plans/`, or any other lane file was written; no git/jj mutation was run.
All scratch output: `.ufo/waves/round-36/build/R36ProbeRerun/` (43 stdout captures, 39 stderr captures, 5 counter logs).

## 1. Instruments as found (digests)

```
$ sha256sum plans/regex_log_probe.py corpus/evidence/round36/regex-log-probe.txt plans/round36_c2_verify.py
d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc  plans/regex_log_probe.py
439101fa2eac0e79ebec088ab47d9fc4481df0ec12d0ebc6c3475319d426a2be  corpus/evidence/round36/regex-log-probe.txt
983ed65c885990f6d783abffbe21b70ab5414431b88a3b27d52fdbda65d67120  plans/round36_c2_verify.py
```

- Probe digest equals the Amendment-1 digest (`d58194c8…`) stated in `plans/round-36-claims.md`; the receipt is 5907 bytes / 26 lines.
- Amendment 1 audited against the freeze commit `3241b86c` — exactly two lines changed, as disclosed:

```
$ git diff 3241b86cde0e9a3b9363a0d4c7fff12ec5d5f5e2 -- plans/
 plans/regex_log_probe.py   |  2 +-
 plans/round-36-claims.md   | 18 ++++++++++++++++++
 plans/round36_c2_verify.py |  2 +-

-            first = (str(e).splitlines() or ["AssertionError"])[0]
+            first = (str(e).splitlines() or ["AssertionError"])[0].replace(d, "<tmp>")
-PROBE_SHA256 = "34ab5dfd6d1c3fb972cb698a1d44db07a1670ee206521d7c3177a9e0f729561b"
+PROBE_SHA256 = "d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc"  # Amendment 1 (claims file)
```
- The pre-amendment first run differs from the pinned receipt in exactly the two path-bearing lines (the disclosed cause):

```
$ diff -u corpus/evidence/round36/regex-log-probe-first-run.txt corpus/evidence/round36/regex-log-probe.txt
-case=invalid-regex … assertion='Regex in /tmp/tmp68j2v92s/regex.txt is invalid: missing ), unterminated subpattern at position 0' …
-case=regex-file-absent … assertion='Regex file /tmp/tmp7c39pj0f/absent-regex.txt does not exist' …
+case=invalid-regex … assertion='Regex in <tmp>/regex.txt is invalid: missing ), unterminated subpattern at position 0' …
+case=regex-file-absent … assertion='Regex file <tmp>/absent-regex.txt does not exist' …
```
Everything else in the receipt is unchanged from the first run.

## 2. Run matrix and result

Interpreter resolution was confirmed, not assumed:

```
$ uv run --no-project -p 3.13 python3 -c 'import sys;print(sys.version.split()[0])'   -> 3.13.16 cpython
$ uv run --no-project -p 3.12 python3 -c …                                           -> 3.12.15 cpython
$ uv run --no-project -p 3.11 python3 -c …                                           -> 3.11.17 cpython
system python3 -VV                                                                   -> Python 3.14.8 (main, Oct  2 2026) [GCC 16.2.1]
```

39 saved non-dry runs; 35 byte-identical to the receipt, 4 differ (§3). Grouped:

| group | command (cwd) | n | vs receipt |
|---|---|---|---|
| A baseline, twice | `python3 plans/regex_log_probe.py --lane .` (lane) | 2 | identical |
| A hashseeds | same, `PYTHONHASHSEED=0,1,99,12345` | 4 | identical |
| B 3.13 | `uv run --no-project -p 3.13 python3 plans/regex_log_probe.py --lane .` (lane) | 2 | identical |
| B 3.13 seeds | same, `PYTHONHASHSEED=1`, `99` | 2 | identical |
| C 3.12 | `uv run --no-project -p 3.12 …` | 2 | identical |
| C 3.12 seeds | same, `PYTHONHASHSEED=1`, `99` | 2 | identical |
| D 3.11 | `uv run --no-project -p 3.11 …` | 2 | identical |
| D 3.11 seeds | same, `PYTHONHASHSEED=1`, `99` | 2 | identical |
| E other cwd | `python3 /abs/…/plans/regex_log_probe.py --lane /abs/lane` from `/tmp`, from `/`, and `uv -p 3.13` / `-p 3.11 PYTHONHASHSEED=99` from `/tmp` | 4 | identical |
| F locale/encoding | `LC_ALL=C LANG=C`; `PYTHONUTF8=0 LC_ALL=C` | 2 | identical |
| G -W / -S / -B / -X dev | `-W error`, `-S`, `-B`, `-X dev` | 4 | identical |
| H TMPDIR shape | `TMPDIR=/var/tmp`, `/var/tmp/`, `/tmp/k36-probe-tmpdeep`, 120-char name, name with spaces, relative `TMPDIR=.` (cwd `/tmp/k36-reltmp`) | 6 | identical |
| I randomized seeds (unsaved) | 4 interpreters × 10 runs, random `PYTHONHASHSEED` | 40 | identical |
| J clean clone | sparse `--shared` clone in `mktemp -d`, no pre-existing `__pycache__`, `--lane $D/lane` | 1 | identical |
| K `--dry` case table | 3.14/3.13/3.12/3.11 `--dry` | 4 | identical to `regex-log-dry-cases-freeze.txt` (`97b4569f…`, 25 lines) |

Representative outputs:

```
$ cmp -s corpus/evidence/round36/regex-log-probe.txt <each of 35 captures>   -> all 35 exit 0
randomized batch: runs: 40
  sys314  sha256=439101fa2eac0e79… exit=0 n=10 equal_to_receipt=True
  uv3.11  sha256=439101fa2eac0e79… exit=0 n=10 equal_to_receipt=True
  uv3.12  sha256=439101fa2eac0e79… exit=0 n=10 equal_to_receipt=True
  uv3.13  sha256=439101fa2eac0e79… exit=0 n=10 equal_to_receipt=True
clean clone: toplevel=/tmp/k36-Rmtr/lane expect=/tmp/k36-Rmtr/lane
             exit=0  CLEAN-CLONE-BYTES: identical  439101fa2eac0e79…
```

Every run exits 0 and ends `cases=24 observed_pass=8 observed_fail=16 mismatches=0`; stderr is empty except where noted in §3.
Cross-version `re` portability of the two version-sensitive messages is measured, not assumed: `(` yields
`missing ), unterminated subpattern at position 0` identically on 3.11.17, 3.12.15, 3.13.16 and 3.14.8, and the
missing-file message is `Regex file <tmp>/absent-regex.txt does not exist` on all four. `findall` returns match order
(no set iteration), so no hash-seed sensitivity exists in the output; the 40 randomized-seed runs confirm it.

## 3. Every byte difference found, and its cause

Four of 39 saved runs differ. None is a version, cwd, hashseed, locale, TMPDIR or cache effect.

**(D1) `-O` / `PYTHONOPTIMIZE=1` — CPython strips the grader's `assert` statements.**
```
$ python3 -O plans/regex_log_probe.py --lane .
exit=1  stderr: FileNotFoundError: [Errno 2] No such file or directory: '/tmp/tmpyng1imqi/absent-regex.txt'
stdout: 21 lines (receipt has 26); 14 lines flip to `match=NO … observed=pass`
$ PYTHONOPTIMIZE=1 python3 plans/regex_log_probe.py --lane .        -> same 21 lines, exit 1
$ uv run --no-project -p 3.13 python3 -O plans/regex_log_probe.py --lane .  -> same 21 lines, exit 1
```
Cause: the pinned grader (`corpus/evidence/round36/tb2-regex-log/test_outputs.py`) enforces everything through bare
`assert` statements. Under `-O` they do not run, so `assert matches == expected_dates` never fires: 14 of the 16
`predicted=fail` cases are reported `observed=pass` (a **false green inside the probe**), `invalid-regex` still fails
because that branch is an explicit `raise AssertionError`, and `regex-file-absent` becomes an uncaught
`FileNotFoundError` (the `assert regex_file.exists()` was stripped, so the grader proceeds to `read_text()`), which
aborts the run before the summary line. The traceback prints the raw temp path because it is not an `AssertionError`
and never reaches the `<tmp>` substitution. Fails safe at counter level (§4, W5 red), but the failure mode is a crash,
not a refusal.

**(D2) `-X warn_default_encoding -W error::EncodingWarning` — probe aborts at case 1.**
```
$ python3 -X warn_default_encoding -W error::EncodingWarning plans/regex_log_probe.py --lane .
exit=1  stdout: 1 line (the `grader=…` header only)
stderr: EncodingWarning: 'encoding' argument not specified
        File "plans/regex_log_probe.py", line 120, in run_grader
          p.write_text(regex)
```
Cause: the probe (and the grader's own `read_text()`/`Path.read_text`) pass no explicit `encoding=`; with the
default-encoding warning policy turned on *and* escalated, the first `write_text` raises. Fails safe (no summary).

**(D3) `-X warn_default_encoding` alone — stderr-only difference, stdout byte-identical.**
One `EncodingWarning` per case is printed to stderr (24 lines + traceback-free), stdout still `cmp`-equal to the
receipt. Not a receipt defect; recorded because it is a real difference in process output under a plausible host
policy (`PYTHONWARNDEFAULTENCODING=1`).

**(D4) First-run receipt vs amended receipt — the two `mkdtemp` paths** (§1 diff). Cause: pre-Amendment-1 probe did
not neutralise the temp directory in `str(e)`; fixed at probe line 127. Confirms the amendment's disclosure is
complete for the receipt: no other byte differs.

No other difference was observed: 3.11/3.12/3.13/3.14, `PYTHONHASHSEED` 0/1/99/12345/random, cwd `/`, `/tmp`, lane,
locale `C`/UTF-8-off, `-B`, `-S`, `-W error`, `-X dev`, TMPDIR `/var/tmp`, trailing slash, 120-char, spaces, relative
`.`, and a cache-free clone all produce the receipt byte-for-byte.

## 4. `plans/round36_c2_verify.py --lane .` (read-only, in the lane)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round36_c2_verify.py --lane .   ; echo exit=$?
W1 ok
W2 DEFECT S108 present 0 times
W3 DEFECT entry absent
W4 DEFECT index row absent or missing S108/S109/S110
W5 DEFECT entry absent
W6 ok
checks=6 defects=4
PREDICATE C2 fail
exit=1
```
Same output under `uv run --no-project -p 3.11 python3 …` and from `/tmp` with an absolute `--lane`
(`c2_sys314_lane.txt`, `c2_uv311_lane.txt`, `c2_tmp_abs.txt` in scratch). `corpus/knowledge/tb2-regex-log-grader.md`
does not exist yet and no S108-S110 rows are in `corpus/SOURCES.md`; W1 and W6 hold at this tip, as the claims predict.

**What W5 proves despite reading "entry absent":** `w5()` returns at the *first* failing branch
(`plans/round36_c2_verify.py:173-188`): probe-digest check (l.173), receipt byte-equality (l.175-180), then the 24-case
summary (l.183-185), and only then `entry absent` (l.186-188). Reaching "entry absent" therefore *measures* that the
probe digest equals `PROBE_SHA256`, that a fresh run is byte-equal to the receipt, and that the summary line reads
`cases=24` — the whole probe half of W5 holds; only the entry half is missing. Everything after l.189 (entry carries
the summary verbatim; every `match=NO` name present) is unreachable until the entry lands.

W5 also fails safe under an optimized environment:
```
$ PYTHONOPTIMIZE=1 python3 plans/round36_c2_verify.py --lane .    ->  W5 DEFECT fresh probe output differs from receipt (exit 1)
$ PYTHONHASHSEED=7 python3 plans/round36_c2_verify.py --lane .    ->  identical to the normal run (W5 DEFECT entry absent)
```

## 5. Findings for the L1 (none acted on — no lane file was edited)

- **F1 (limit, fails safe today).** The receipt is reproducible only with `sys.flags.optimize == 0`. Neither the
  probe nor W5 pins that; the protection is incidental (D1's crash suppresses the summary line, so W5's l.183 test
  goes red). A one-line refusal in the probe is *not* available — the probe digest is frozen — so if the L1 wants an
  explicit invariant it belongs in the counter (e.g. a `sys.flags.optimize` guard, or spawning the probe with
  `PYTHONOPTIMIZE` removed from the child env). Recommended wording for the entry/receipt label: "byte-equal under
  CPython 3.11.17/3.12.15/3.13.16/3.14.8 with asserts enabled".
- **F2 (latent oracle widening).** W5's `re.fullmatch(r"cases=(\d+) observed_pass=(\d+) observed_fail=(\d+)
  mismatches=(\d+)")` (l.183) checks **only** `group(1) == 24`; `observed_pass=8 observed_fail=16 mismatches=0` are
  parsed and discarded. Because the receipt is also the oracle, a receipt regenerated in a behaviour-changing
  environment would be self-consistent. Live reachability is blocked twice over: the probe digest is pinned
  (`d58194c8…`), and the unmodified probe crashes under `-O` before printing a summary (D1). Pinning
  `mismatches == 0` and `observed_pass == 8` would close it without touching the frozen battery.
- **F3 (capture dir is writable state).** The probe imports the pinned grader via `SourceFileLoader`, which writes
  bytecode into the capture dir. `corpus/evidence/round36/tb2-regex-log/__pycache__/` now holds
  `test_outputs.cpython-{311,312,313,314}.pyc` plus `…cpython-{313,314}.opt-1.pyc` (the `.opt-1` pair from my `-O`
  runs; the `cpython-314.pyc` at 22:02 predates me). It is ignored by `.gitignore:2 __pycache__/`, so
  `git ls-files --others --exclude-standard` stays empty and C1's `--require-clean-tree` and C2's W1 are unaffected;
  a cache-free sparse clone still reproduces the receipt exactly (matrix row J), so there is no cache dependence. But
  no check sees this directory, and a poisoned `.pyc` would only surface as output ≠ receipt (W5 red) — cheap
  hardening: pass `-B`/`PYTHONDONTWRITEBYTECODE=1` when spawning the probe, and consider it in the round-36 lesson's
  D2 clause.
- **F4 (message text is version-portable).** The two `re`-generated texts the receipt carries are identical on
  3.11-3.14, so C2's W5 byte-equality is not an accident of one interpreter; this is usable evidence for the entry's
  `## Negative space`/limits section.
- **F5 (operability).** 84 probe invocations in this seat (39 saved + 40 randomized + 1 clone + 4 `--dry`), all exit 0
  where expected; wall clock 7 runs, median 0.225 s, max 0.273 s (`[0.233, 0.187, 0.199, 0.225, 0.262, 0.209, 0.273]`).
  The probe needs no network, no container and no model. The only environmental requirements measured are
  asserts-enabled and default-encoding warnings not escalated to errors.

## 6. Evidence index (all under `.ufo/waves/round-36/build/R36ProbeRerun/`)

`3.11_uvrun{1,2,_seed1,_seed99}.stdout`, `3.12_…`, `3.13_…`, `A{1,2}_sys314_lane.stdout`,
`A_sys314_seed{0,1,99,12345}.stdout`, `cwd_{tmp,root}_sys314.stdout`, `cwd_tmp_uv313.stdout`,
`cwd_tmp_uv311_seed99.stdout`, `env_{lc_all_C,utf8_0,w_error,nosite,pythonoptimize}.stdout`,
`flag_{B,O,X_dev,warn_default_enc,Werr_enc}.stdout`, `uv313_O.stdout`,
`tmpdir_{vartmp,trailing_slash,deep,long120,spaces,relative_dot}.stdout`, `dry_{sys314,uv313,uv312,uv311}.stdout`,
`c2_{sys314_lane,uv311_lane,tmp_abs,pythonoptimize1,pythonhashseed_weird}.txt`, with matching `.stderr`.

## 7. Not measured / limits of this seat

- Only CPython 3.11.17/3.12.15/3.13.16/3.14.8. PyPy/GraalPy/free-threaded 3.13 were not installed (would need a
  download) and were not required by the assignment; the pinned TB2 `tests/test.sh` interpreter is 3.13 (`uv run
  --no-project -p 3.13` resolved to 3.13.16 here).
- Windows/macOS path semantics were not exercised; the `<tmp>` substitution is a plain string replace of the actual
  `TemporaryDirectory` path, which is prefix-stable for every Unix TMPDIR shape I tested (including a 120-char path,
  spaces and a relative path).
- I ran no build, lint, test, or gate command beyond the two prescribed instruments; nothing was judged, committed or
  pushed. `/tmp` fixtures were removed (`mktemp -d` clone, `tmpdir` probe dirs); lane status after the seat is
  unchanged apart from the ignored `__pycache__` described in F3 and my own `.ufo/…/build/R36ProbeRerun*` files.

VERDICT: probe-deterministic-yes-py313-same-py312-same-py311-same
