writer: KengakuR29-2.FRerunCounts-2

# FRerunCounts — re-run of the three prereg counting receipts

## Attack

Target: the counting commands declared at `plans/round-29-claims.md:20-21`, against lane master
`56fd949a6478342531e61f4feecb4a685d831640` (verified `git rev-parse HEAD`; worktree clean for the
instrument path). Attack surface: is the counting evidence byte-reproducible, and does any value
drift between the build receipts and a fresh run?

Independence: I did **not** read, cat, or import `plans/config_projection.py`. I only `sha256sum`'d
it and executed it read-only. I read the prereg text, the receipt files, pinned input bytes (hashed
only), and git objects. No tool installs or upgrades were needed or performed; no writes outside
`.ufo/waves/round-29/scratch/falsify/FRerunCounts-2/` and this report.

## Result at a glance

| receipt | literal comparison | outcome |
|---|---|---|
| `build-json-sha256.txt` | exact | `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` |
| `build-summary.txt` | body exact, one extra trailing line | 6,914 B stdout vs 6,921 B receipt; delta is `exit=0` |
| `instrument-before.txt` | wording differs, exit matches | `exit=128`; git message branch depends on worktree presence |

No count value drifts. Two literal receipt mismatches, both fully explained below.

## Observed facts

### 1. `--json` determinism

```
$ python3 plans/config_projection.py --json > json1.txt   # exit 0
$ python3 plans/config_projection.py --json > json2.txt   # exit 0
c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630  json1.txt
c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630  json2.txt
```

3,881,050 bytes each; pipe (`| wc -c`) and file redirect agree at 3,881,050. The sha equals
`build-json-sha256.txt` exactly (that file is 68 bytes: 64 hex, two spaces, `-`, newline).

The same sha `c8da0c5a…` was returned by every variant tested:

- two sequential runs (above), plus eight concurrent processes
  (`for i in $(seq 1 8); … & wait` → `uniq -c` showed `8 c8da0c5a…`; total stderr 0 bytes; scratch
  subdir held 16 files after the run: 8 `.out` + 8 `.err`, i.e. no side files);
- `PYTHONHASHSEED` in {0, 1, 12345, random};
- `LC_ALL=C`, `LC_ALL=C.UTF-8`, `LANG=de_DE.UTF-8`, `PYTHONUTF8=1`,
  `PYTHONIOENCODING=latin-1`, `TZ=Asia/Tokyo`;
- stdin `/dev/null`; cwd = scratch dir; explicit `--root <lane>`.

Document validity: `json.loads` succeeds; top-level dict keys are `findings`, `index_mapping`,
`inputs`, `limitations`, `manifest_sha256`, `occurrence_provenance`, `population`, `profiles`,
`raw_text_sha256`, `source_contract`, `upstream_revision`; `findings` length 0; `limitations`
length 7; `occurrence_provenance` length 1,435. No `/home/` or `/tmp/` substring occurs anywhere
in the 3,881,050 bytes (count 0), so the payload is location-independent; 147 escaped `\u`
sequences are present and sha-stable.

### 2. `--summary` determinism

Two runs: `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`, 6,914 bytes,
exit 0, 47 lines, last line `TOTAL findings=0 exit=0`. Identical sha under the same seed/locale/TZ
matrix, under `COLUMNS=20`, under `--root <lane>`, and through a PTY
(`script -q -c … /dev/null | tr -d '\r'`).

### 3. Receipt comparison — `build-summary.txt`

`diff -u` yields exactly one hunk: receipt line 48 `exit=0` has no stdout counterpart.

```
$ head -n 47 corpus/evidence/round29-calibration/build-summary.txt | sha256sum
5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f  -
$ stat -c '%s' …build-summary.txt …sum1.txt
6921 / 6914
$ printf 'exit=0\n' | wc -c
7
```

So lines 1–47 are byte-identical to fresh stdout; the 7-byte delta is exactly the appended shell
status line. The same convention appears in `build-selftest.txt`: a fresh `--selftest` run differs
only by receipt line 2 `exit=0`, body otherwise identical.

### 4. Receipt comparison — `instrument-before.txt`

Receipt (198 bytes): `$ git cat-file -e ed26bdf…:plans/config_projection.py`, then
`fatal: path 'plans/config_projection.py' does not exist in 'ed26bdf…'`, blank line, `exit=128`.

Fresh re-run at lane root: exit 128, but the message reads `… exists on disk, but not in …`.
Mechanism verified in a throwaway repo under `/tmp/gitmsgtest` (git 2.56.0):

- path absent on disk → `does not exist in`, exit 128;
- path present on disk → `exists on disk, but not in`, exit 128.

Equivalent-state reproduction returns the receipt text exactly:
`git --git-dir=<lane>/.git --work-tree=/tmp/emptywt cat-file -e ed26bdf…:plans/config_projection.py`
→ `fatal: path 'plans/config_projection.py' does not exist in 'ed26bdf…'`, exit 128.

The underlying claim (absent at baseline) is independently confirmed, not merely inferred from the
receipt: `git ls-tree ed26bdf… -- plans/config_projection.py` returns 0 lines; `-- plans/` returns
28 entries; `git merge-base --is-ancestor ed26bdf5d924755697cd6812129be2fa441c42a3 HEAD` exits 0.

### 5. Receipt provenance against the instrument under test

- `sha256sum plans/config_projection.py` = `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`,
  identical to the blob at lane master `56fd949`, and identical to the `control sha256` line in
  `mutation-witness.txt`.
- `git status --porcelain -- plans/config_projection.py` → empty.
- Receipts are tracked in `b98dcf317b6c50179ac5c70b6ba3dacc7e2976fe` (ancestor of `56fd949`);
  `git show b98dcf3:<receipt>` equals the worktree file for all five receipts
  (`build-summary` `fc0fdc8c…`, `build-json-sha256` `3d2dec88…`, `build-selftest` `94289d4e…`,
  `instrument-before` `4a7355d9…`, `mutation-witness` `a9629170…`).
- Pinned input hashes recomputed and equal to the values embedded in `--json`:
  manifest `f6390b92…bf87`, raw `7b50386f…7652`, generator `45ddba7b…21cd`,
  profiles `90fdc34d…e018`.

### 6. Cross-receipt value agreement

58 value-level comparisons between `--summary` fields and the corresponding `--json` fields
(population scalars, per-token occurrence/task maps, other `__…__` markers, index mapping, and for
each of the three profiles: applied replacements, changed-leaf/task counts, category/path-template/
token maps, remaining-token maps, stimulus observations, projected text sha256): 0 mismatches.
Render-shape differences only: summary prints `"violations": 0`, JSON keeps `"violations": []`
(same empty set); summary hoists `applied_replacements`, JSON nests it per step in `steps[]`.
Sum of per-step replacement counts is 1,435, equal to `occurrence_provenance` length and to the sum
of `original_occurrences_by_token`.

Output hygiene: no date-like substring, no `/home/`, no `/tmp/`, no hostname in either mode.

## Every mismatch, with location and value

| # | location | recorded value | reproduced value | delta | reading |
|---|---|---|---|---|---|
| M1 | `build-summary.txt:48` | `exit=0` | absent from `--summary` stdout | +7 bytes (6,921 vs 6,914) | capture-wrapper line, same convention as other receipts; stdout body hash-equal |
| M2 | `instrument-before.txt`, fatal line (line 2) | `does not exist in` | `exists on disk, but not in` | +9 characters | git worktree-presence branch; exit code 128 and baseline-absence semantics both match |

No mismatch in `build-json-sha256.txt`; no numeric mismatch in any receipt; no exit-code mismatch
(`--summary`, `--json`, `--selftest` all 0; baseline probe 128).

## Inference

- [INFERENCE] M1 and M2 are capture-convention artifacts, not altered evidence. The wrapper line is
  present in every command-capture receipt; the summary body hashes equal to fresh stdout; M2's
  wording is exactly what git 2.56.0 emits when the path is absent from the work tree and is
  reproducible today from an empty work tree at exit 128.
- [INFERENCE] Consequently the counting receipts do not overstate the claim: every counted value is
  stable, environment-invariant within the tested set, mutually consistent across `--summary` and
  `--json`, and equal to the prereg's 812 / 3 / 2436 framing.

## Residual unknowns

- Non-C locale invariance is untested in substance: `locale -a` lists 4 locales, only `C` and
  `C.utf8`; `LANG=de_DE.UTF-8` fell back rather than switching. The instrument itself declares
  text-mode locale behavior inert for this ASCII input.
- No receipt records the interpreter or git version, so exact environment replication cannot be
  proven from receipts alone (observed now: Python 3.14.8, git 2.56.0).
- This item tests stability and receipt agreement, not count correctness: I built no independent
  oracle and did not re-derive 812x3 from generator bytes, and — per the independence rule — I did
  not read the instrument source, so how each count is computed remains unattributed here.

VERDICT: PARTIAL
