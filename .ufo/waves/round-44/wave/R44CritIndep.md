# Seat R44CritIndep — round-44 wave report (critic: independent re-derivation + own grader cases)

Seat: R44CritIndep (leaf, critic). Date: 2026-10-26. Milestone: kengaku r44 wave (v2, build+attack).
Report subdir: `.ufo/waves/round-44/wave/R44CritIndep/` (transcripts + pre-receipt predictions).

## 0. Method and temporal ordering

The probe (`plans/feal_linear_probe.py`) was never read or run. Re-derivation input = captures only:

- `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/test_outputs.py` (S138),
- `gen.py` (S140), `Dockerfile` (S141), `test.sh` (S142), `solve.sh` (S144), `decrypt.c` (S145),
- `instruction.md` (S139), `task.toml` (S146).

Order: (1) read captures; (2) wrote predictions to scratch
`/fast/scratch/hyaku/kengaku-r44/R44CritIndep/predictions.md` **before** opening the receipt
(sha256 `f89d8c174e15d94ce52f35c5772dbdb61093c09eb2f6d586d39d9705e4f13f42`, copy kept at
`…/wave/R44CritIndep/predictions-before-receipt.md`); (3) read receipt; (4) compared; (5) ran own cases.
The frozen `plans/round-44-claims.md` was read in full after (2) so its disclosed facts could not bias the
predictions.

## 1. Grader model derived from captures

- `test_outputs.py:120` — `data = open("/app/plaintexts.txt").read()`; `:121-122` —
  `for c in soln.split(): assert c in data`. One test, all-or-nothing, **substring membership** of each of the
  100 decimal constants (`:4-103`); no count/order/format/exactness check.
- `test.sh:18-22` — runs `pytest` (uvx, python 3.13, pytest 8.4.1); `:25-28` — reward 1 iff pytest exit code 0,
  else 0.
- `gen.py:12` — `keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]`; `:19-28` and `:57-62` —
  plaintext = `int.from_bytes(hashlib.sha256(seed_hash + struct.pack(">Q", counter)).digest()[:8], "big")`
  for counters 32..131 → the 100 expected plaintexts are fully determined by public material.
- `Dockerfile:13-14` — `RUN rm orig_plaintexts.txt` / `RUN rm gen.py` (image keeps only ciphertexts.txt, pairs.txt,
  feal, decrypt).
- `decrypt.c:132-137` — decrypt prints each plaintext as decimal `printf("%lu\n", plaintext)`, newline-separated.
- `instruction.md:8-10` — "decrypting all the ciphertexts in the file /app/ciphertexts.txt, and saving your answer
  in the file /app/plaintexts.txt" (no output format named).

Model: **PASS iff `/app/plaintexts.txt` exists AND every one of the 100 constants occurs as a substring of its
decoded text; else FAIL** (missing file → `FileNotFoundError` → pytest error → exit≠0 → reward 0; any missing
constant → assert fail).

## 2. Predictions (written before receipt)

13 behaviors enumerated in `predictions-before-receipt.md` with per-case reasoning, all derived from the model:
no file→FAIL, one constant missing→FAIL, hex content→FAIL, wrong-key decrypt→FAIL, pairs plaintexts→FAIL,
ciphertexts copied→FAIL, decrypt with public gen.py keys→PASS, replay public hash chain→PASS, copy constants from
test file→PASS, concatenated constants→PASS, reversed line order→PASS, zero-padded decimals→PASS, +100 wrong-key
decoys→PASS.

## 3. Receipt comparison

Receipt: `corpus/evidence/round44/feal-linear-probe.txt` (`cases=14 observed_pass=8 observed_fail=6 mismatches=0`,
`regrade cases=14 differ=0`).

| receipt CASE | observed | my prediction | match |
|---|---|---|---|
| nop | fail | fail (no file) | yes |
| oracle-solve-sh | pass | pass (model: solve.sh output = true plaintexts ⇒ membership holds) | yes |
| decrypt-public-keys | pass | pass | yes |
| replay-public-gen | pass | pass | yes |
| copy-public-constants | pass | pass | yes |
| oracle-concatenated | pass | pass | yes |
| oracle-plus-decoys | pass | pass | yes |
| oracle-reversed | pass | pass | yes |
| oracle-zero-padded | pass | pass | yes |
| one-missing | fail | fail | yes |
| hex-output | fail | fail | yes |
| wrong-key-decrypt | fail | fail | yes |
| pairs-plaintexts | fail | fail | yes |
| ciphertexts-copied | fail | fail | yes |

13 of 14 cases were enumerated in the pre-receipt prediction file and all 13 match; the 14th
(oracle-solve-sh) was not enumerated (unknown cid before receipt) but its verdict follows from the same model and
matches. **k = 14/14.**

## 4. Own cases the probe lacks (bwrap harness)

Harness: the frozen capture `test_outputs.py` was copied per case; the **only** difference is the data path on line
120 (`"/app/plaintexts.txt"` → scratch fixture path). Verified byte-identical after path normalization (python check:
`identical-after-path-normalization: True` for all three). pytest 8.4.1 on CPython 3.13 via `uvx` (matching
`test.sh`), run inside the round-44 envelope (home read-only; ~/.cache from scratch; `~/.local/bin` content digest
before/after). Reward per `test.sh:25-28` (exit 0 → 1 else 0).

Fixtures (all built from the capture's 100 constants): case1 = `\r\n` separators; case2 = trailing NUL byte after
final newline; case3 = `0xff 0xfe` injected between constant 50 and 51 (invalid UTF-8).

| case | fixture (sha256) | pytest | envelope exit | reward → verdict | predicted |
|---|---|---|---|---|---|
| case1-crlf | 5b664eb1843e5cdc8990e64520bfde63d5ec75ef1b896382f266855a219e91e2 | 1 passed | 0 | 1 → PASS | PASS |
| case2-nul | 3a96463039cb5af9c0bf94b196cb720e1062f74257bdd8f3200d370ce5d45879 | 1 passed | 0 | 1 → PASS | PASS |
| case3-nonutf8 | dfd5c01760ef29dec40901cbfa2cb20c4a929414d3a8f5b543835bd5b458948e | 1 failed (UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 1022) | 1 | 0 → FAIL | FAIL |

All three observed verdicts match the model.

ENVELOPE lines (Q32; full transcripts in `…/wave/R44CritIndep/*.env.txt`):

```
case1: ENVELOPE start 20:34:03 cwd=/home/vgpnk/Projects/shokunin
       ENVELOPE end 20:34:05 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
case2: ENVELOPE start 20:34:07 ... ENVELOPE end 20:34:09 exit=0 ... unchanged
case3: ENVELOPE start 20:34:10 ... ENVELOPE end 20:34:12 exit=1 ... unchanged
```

(The `--ctrf` plugin of test.sh was omitted: it only writes a report file; the reward comes from pytest's exit
code, which is what was measured. `uvx` fetched python 3.13/pytest into scratch via `UV_CACHE_DIR`,
`UV_PYTHON_INSTALL_DIR`, `UV_TOOL_DIR`; `~/.local/bin` untouched — digest unchanged in every run.)

## 5. Tooling installs

None (used existing `/usr/bin/python3` for fixture tooling and existing `~/.local/bin/uvx`, read-only inside the
envelope).

## 6. Cleanup

Scratch `S=/fast/scratch/hyaku/kengaku-r44/R44CritIndep` removed with
`python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44CritIndep "$S"` after this report was
written (predictions and transcript copies kept in the report subdir).

VERDICT: rederived-14/14-own-cases-3.
