# R44PytestParity — real-pytest parity for the C2 receipt (kengaku round 44, hyaku run 9)

Seat: executor, leaf. Scope: rebuild the 14 `feal-linear-cryptanalysis` case end states exactly as
`plans/feal_linear_probe.py` does, grade each with **real pytest under test.sh's harness** (`uvx -p 3.13 -w
pytest==8.4.1 pytest`, no network) instead of importing `test_attack`, and compare pytest's exit status with the
receipt's verdicts. **Refines the C2 "pytest is not run" limit named in `plans/round-44-claims.md` §C2 Limits.**

Axes named before work (godspeed): (a) verdict parity per case (14 rows, the acceptance axis); (b) end-state
identity — proof that pytest graded the same `/app` the probe staged; (c) harness fidelity — how far the offline
pytest invocation departs from `tests/test.sh`; (d) repeatability (two grade runs per case, three whole-sweep runs).

Nothing frozen was edited. No lane file was written (report + own subdir only). No tool installed: the scratch uv
cache was populated with the already-installed `uv 0.13.0`; pacman untouched.

## Method

Build half = the frozen probe's own code path, not a re-implementation: `parity.py` imports a **byte-identical**
copy of the probe and calls `pr.harness(cap, work, "recipe")`, which runs `SEED` (Dockerfile:6-11 replay) then the
case recipe under `bash -euo pipefail` in `/app`, inside the probe's bwrap sandbox with the same `/app` (rw),
`/tests` (ro), `/pub` (ro: `gen.py`, `test_outputs.py`, `solve.sh`) binds.

- `sha256sum plans/feal_linear_probe.py` = `0e7a59dab76266a167d9c3f51dd01817f7cec2f62896689bc488947dce545297` =
  `sha256sum $S/probe_ref.py` (identical; the copy is imported, never edited).
- Graded with the probe's sandbox **plus** `--ro-bind /home/vgpnk /home/vgpnk` (uv binary + uv-managed python) and
  `--bind $S $S` (uv cache/tool dir), cwd `/app` (`--chdir /app`, test.sh's `WORKDIR`), command:
  `/home/vgpnk/.local/bin/uvx -p 3.13 -w pytest==8.4.1 pytest /tests/test_outputs.py -v -rA`, env
  `UV_CACHE_DIR=$S/uvcache UV_TOOL_DIR=$S/uvtools UV_TOOL_BIN_DIR=$S/uvbin UV_OFFLINE=1` (run 3 drops
  `UV_OFFLINE`), `--unshare-net` on every run. Network is absent, so pytest 8.4.1 (+5 packages: pluggy 1.7.0,
  iniconfig, packaging, pygments) resolves cache-only from a scratch cache populated once
  (`uvx -p 3.13 -w pytest==8.4.1 pytest --version` → `pytest 8.4.1`).
- Verdict rule = test.sh's: pytest exit status → reward (`tests/test.sh:25-27` `if [ $? -eq 0 ]; then echo 1 ...`).
  `rc==0` → pass, anything else → fail.

## Commands and envelope lines

All three sweep runs and the state check ran under `claims/envelope.sh "$S/env" ...`; `~/.local/bin` content digest
`328be01808ba022f` unchanged before/after in every run (no exit 4, no INVALID).

```
ENVELOPE start 20:34:06 ... end 20:34:07 exit=1  unchanged      # run0 aborted: sys.modules not seeded for dataclasses
ENVELOPE start 20:34:15 cwd=/fast/scratch/hyaku/kengaku-r44/R44PytestParity
ENVELOPE end   20:34:24 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged   # run1
ENVELOPE start 20:34:44 ... end 20:34:52 exit=0 ... unchanged   # run2 (identical rows, diff empty)
ENVELOPE start 20:34:33 ... end 20:34:35 exit=0 ... unchanged   # detail: full pytest output, 2 cases
ENVELOPE start 20:35:10 ... end 20:35:14 exit=0 ... unchanged   # state-parity vs c2-stage-check.txt
ENVELOPE start 20:35:51 ... end 20:35:59 exit=0 ... unchanged   # run3, UV_OFFLINE unset (cache-only control)
```

- `python3 $S/parity.py $S/w` → `pytest-parity rows=14 matched=14 mismatched=0` (exit 0), three times
  (`parity-run1.txt`, `parity-run2.txt`, `parity-run3-nooffline.txt`; `diff` of the 14 `PYTESTCASE` lines between
  run1 and each other run is empty).
- `python3 $S/states.py` → `state-parity cases=14 mismatched=0`.
- `python3 $S/detail.py` → `parity-detail.txt` (full pytest session for `oracle-solve-sh` and `hex-output`).

## 14 rows (receipt ↔ pytest)

`receipt` = `corpus/evidence/round44/feal-linear-probe.txt` `observed`/`tests` columns (`:9-22`); `rc1/rc2` = two
independent pytest runs on the same end state; `collected` from pytest's own line.

| case | receipt | pytest rc1 | rc2 | collected | parity | pytest's own mechanism |
|---|---|---|---|---|---|---|
| `nop` | fail (F) | 1 | 1 | 1 | yes | `FileNotFoundError` on `/app/plaintexts.txt` (`test_outputs.py:120`) |
| `oracle-solve-sh` | pass (P) | 0 | 0 | 1 | yes | 1 passed |
| `decrypt-public-keys` | pass (P) | 0 | 0 | 1 | yes | 1 passed |
| `replay-public-gen` | pass (P) | 0 | 0 | 1 | yes | 1 passed |
| `copy-public-constants` | pass (P) | 0 | 0 | 1 | yes | 1 passed |
| `oracle-concatenated` | pass (P) | 0 | 0 | 1 | yes | 1 passed |
| `oracle-plus-decoys` | pass (P) | 0 | 0 | 1 | yes | 1 passed |
| `oracle-reversed` | pass (P) | 0 | 0 | 1 | yes | 1 passed |
| `oracle-zero-padded` | pass (P) | 0 | 0 | 1 | yes | 1 passed |
| `one-missing` | fail (F) | 1 | 1 | 1 | yes | `AssertionError` at `test_outputs.py:122` |
| `hex-output` | fail (F) | 1 | 1 | 1 | yes | `AssertionError` at `test_outputs.py:122` |
| `wrong-key-decrypt` | fail (F) | 1 | 1 | 1 | yes | `AssertionError` at `test_outputs.py:122` |
| `pairs-plaintexts` | fail (F) | 1 | 1 | 1 | yes | `AssertionError` at `test_outputs.py:122` |
| `ciphertexts-copied` | fail (F) | 1 | 1 | 1 | yes | `AssertionError` at `test_outputs.py:122` |

**Mismatches: 0 of 14.** pytest's exit status → reward would be `1` for the 8 receipt-pass cases and `0` for the 6
receipt-fail cases, matching `feal-linear-probe.txt:24` `observed_pass=8 observed_fail=6`. The probe's direct-import
harness and the real pytest harness are verdict-identical on all 14 end states, and identical on the failure
mechanism too: `nop` is the only case that fails by missing file (probe's note `error=FileNotFoundError`, same here),
the other five fail on `assert c in data`. pytest collected exactly one test in every case, so no collection-order or
parametrisation effect exists.

## End-state identity (what pytest graded = what the probe staged)

`states.py` builds each case with the same code path and records `/app/plaintexts.txt`; all 14 sizes equal
`claims/c2-stage-check.txt` (`state-parity cases=14 mismatched=0`), e.g. `nop absent`, `oracle-solve-sh bytes=6654`,
`oracle-concatenated bytes=5726`, `oracle-plus-decoys bytes=8689`, `one-missing bytes=2026`, `hex-output bytes=1895`,
`pairs-plaintexts bytes=649`, `ciphertexts-copied bytes=2045`, `oracle-zero-padded bytes=2100`.

Measured side finding (supports the F1 constant-compare class, no new claim): the three attack-less pass cases
`decrypt-public-keys`, `replay-public-gen` and `copy-public-constants` produce **byte-identical**
`/app/plaintexts.txt` (`sha256=849f9e33e7848d138d8af9880653b6f582c469f992a3ae77625786abc59068e7`, 2047 bytes). The
graded artefact is the same file whichever non-attack route is taken, so the grader cannot separate them at all —
stronger than "passes without an attack".

## Harness fidelity: deviations from `tests/test.sh`

Named, each measured or provably rc-neutral:

1. **No `--ctrf /logs/verifier/ctrf.json`, no `-w pytest-json-ctrf==0.3.5`** (my task's stated harness). The plugin
   only serialises results; it cannot change pytest's exit status, and `/logs/verifier/` does not exist offline.
2. **`/tests` is read-only in the probe's sandbox**, so pytest's cacheprovider emits `PytestCacheWarning: could not
   create cache path /tests/.pytest_cache/...` (1 warning on pass, 2 on fail). Recorded in every receipt row and in
   `parity-detail.txt`; warnings do **not** affect rc (all 8 passes are `rc=0` with the warning present). In the image
   `/tests` is writable, so this deviation only removes cache files.
3. **Network is absent** (`--unshare-net`), so `UV_OFFLINE=1` is set in runs 1–2. Run 3 unset it and every row is
   identical, i.e. resolution was already cache-only (`simple-v26`/`wheels-v7`); the flag does not alter which
   packages pytest loads. Platform line from the captured session: `Python 3.13.16, pytest-8.4.1, pluggy-1.7.0`.
4. **Host interpreter is the uv-managed CPython 3.13.16** (`~/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu`),
   not the image's `python:3.13-slim-bookworm`; **host gcc** stands in for Debian gcc; the image is never pulled.
   Same standing limit the claims already name for the probe.
5. `rootdir` resolves to `/tests` (the test file lives there, cwd `/app`), which is what test.sh's absolute target
   also yields; `cachedir: .pytest_cache` likewise.

## Risks / limits of this measurement

- Parity is established for **these 14 constructed end states**, not for arbitrary agent outputs; it cannot show
  that every possible `/app/plaintexts.txt` grades the same way under both harnesses. The mechanism is shared though:
  both harnesses execute the same `test_attack` body (`test_outputs.py:120-122`), and the only harness-side predicate
  is pytest's rc.
- pytest's rc collapses *why* a test failed; only `-rA`'s summary was used to name the mechanism. rc 1 cannot be
  distinguished from an internal error by rc alone — the detail receipts show the actual `FileNotFoundError` /
  `AssertionError` for one case each.
- The uv cache is scratch-local evidence, not a pinned input: a fresh host without that cache would need network for
  `pytest==8.4.1`. The receipt names the exact population command so it is reproducible.
- Process note: one cosmetic edit to a scratch-only harness script (adding the cache-only control branch) was applied
  with an inline python string replacement rather than the edit tool; scratch was re-read afterwards and the final
  copies in this subdir are the ones that produced the reported runs (`parity.py` was re-run after the header fix).

## Reproduce

```
S=/fast/scratch/hyaku/kengaku-r44/R44PytestParity; mkdir -p "$S"; export TMPDIR="$S"
cp kengaku-shokunin/plans/feal_linear_probe.py "$S/probe_ref.py"        # sha256 0e7a59da…
uvx -p 3.13 -w pytest==8.4.1 pytest --version                           # once, with network: populates the cache
UV_CACHE_DIR="$S/uvcache" /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/envelope.sh \
  "$S/env" /usr/bin/python3 "$S/parity.py" "$S/w"                        # → pytest-parity rows=14 matched=14
```

Harness sources copied here: `parity.py` (`85d3ffa9…`), `states.py` (`96c29703…`), `detail.py` (`44e4c14b…`).
Receipts: `parity-run1.txt` (`c8eb8a58…`), `parity-run2.txt` (`2cc4f1f7…`), `parity-run3-nooffline.txt`
(`c37f42b0…`), `state-parity.txt` (`f16a7305…`), `parity-detail.txt` (`9e635aa0…`). All under 7 KiB.

For the L1 to integrate (not done by me): the C2 Limits paragraph can replace "pytest is not run" with "pytest 8.4.1
under test.sh's harness was run offline on all 14 end states and agreed 14/14 with the receipt (`regrade` likewise
0 differ); `--ctrf`/plugin, the writable `/tests` cache dir and the image's own python/gcc remain unexercised".

VERDICT: pytest-parity-14/14
