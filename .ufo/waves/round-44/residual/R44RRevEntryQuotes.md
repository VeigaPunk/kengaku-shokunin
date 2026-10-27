# R44RRevEntryQuotes — quote & findings review of `tb2-feal-linear-cryptanalysis-grader.md`

Seat: R44RRevEntryQuotes (reviewer, residual round 44). Date: 2026-10-26.
Reviewed object: `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` at lane commit `2a263e5a56ef6d48d06805e1ccd106de5de9ba66` (landed integration commit), reviewed from a `--shared` clone at `/fast/scratch/hyaku/kengaku-r44/R44RRevEntryQuotes/lane` (`git rev-parse HEAD` = `2a263e5a…`; `rev-parse --show-toplevel` = the clone).

## Method

1. Capture integrity first: `sha256sum -c SHA256SUMS` inside `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/` — all twelve files OK (Dockerfile, README.md, decrypt.c, feal.c, gen.py, gitignore, instruction.md, solve.sh, task.toml, test.sh, test_outputs.py, SHA256SUMS). So quote targets are the frozen bytes.
2. Parsed the entry (432 lines) and extracted every quote and citation:
   - `## Located quotes` table: 22 rows (claim, quote, `capture:line`).
   - `## Mechanism` table: 14 rows (case, decisive `capture:line`, quote).
   - Inline backticked `capture:line` tokens in prose: 98.
   - Prose quoted phrases near citations: 2 (both are table headers, not quotes).
3. For every table quote: byte-substring check of the quote against the cited capture line (1-based; `sed -n 'Np'` semantics), plus word-count check (Located quotes claim 3–25 words; Mechanism quotes ≥2 words).
4. For every inline `capture:line` token: file existence in captures and line-range validity.
5. Findings: each numbered `## Findings` sentence (1–10) and its receipt-cited cases checked against `corpus/evidence/round44/feal-linear-probe.txt`, plus the `## Summary`, `## Requirement map`, `## Regrade` and `## Predictor` quantitative claims (counts, letters, violates-tags, regrade equality, constants==chain identity).

## Quote verification results

| Check | Count | Result |
|---|---|---|
| Located quotes, verbatim substring on cited line | 22 | 22/22 OK |
| Located quotes, word count 3–25 | 22 | min 3, max 14, all OK |
| Mechanism quotes, verbatim substring on cited line | 14 | 14/14 OK |
| Mechanism quotes, ≥2 words | 14 | 14/14 OK |
| Inline `capture:line` tokens, file+line valid | 98 | 96/96 direct capture refs OK; 2 tokens are not capture refs (see Observations) |

All 36 table quotes match the capture bytes exactly. The README.md:32 quote is verbatim as a byte substring of the raw line, including the capture's own markdown backticks (`The test suite (`test_outputs.py`) verifies that all 100 expected plaintext values appear in `/app/plaintexts.txt`…`). No quote mismatch found.

Cited-line evidence (via `sed -n`, capture dir abbreviated `C`):

- `C/instruction.md` 1,4,7,9: `The file /app/feal.c implements a FEAL-like encryption function,` / `(Each of the 4 round keys is derived from a 20 bit seed.` / `Implement a known-plaintext attack that recovers the key of the cipher.` / `the file /app/ciphertexts.txt, and saving your answer in the file`
- `C/test_outputs.py` 4,108,120,121,122: `soln = """1050628112036199672` / `    Test that the linear cryptanalysis attack correctly decrypts all ciphertexts.` / `    data = open("/app/plaintexts.txt").read()` / `    for c in soln.split():` / `        assert c in data`
- `C/test.sh` 22,25,26: `  pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -v -rA` / `if [ $? -eq 0 ]; then` / `  echo 1 > /logs/verifier/reward.txt`
- `C/gen.py` 12,61,62: `    keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]` / `        plaintext_hash = hashlib.sha256(seed_hash + counter_bytes).digest()` / `        plaintext = int.from_bytes(plaintext_hash[:8], "big")`
- `C/Dockerfile` 13,14: `RUN rm orig_plaintexts.txt` / `RUN rm gen.py`
- `C/README.md` 32: `The test suite (`test_outputs.py`) verifies that all 100 expected plaintext values appear in `/app/plaintexts.txt`, confirming successful key recovery and decryption.`
- `C/solve.sh` 289,290,303,304: `  snprintf(cmd, sizeof(cmd), "./decrypt ciphertexts.txt 0x%x 0x%x 0x%x 0x%x", k0, k1, k2, k3);` / `  system(cmd);` / `gcc -o attack attack.c -O3` / `./attack > /app/plaintexts.txt`
- `C/task.toml` 22,34: `timeout_sec = 1800.0` / `allow_internet = true`
- `C/decrypt.c` 136: `            printf("%lu\n", plaintext);`

## Findings vs receipt (`feal-linear-probe.txt`)

Receipt facts (from the file itself): 14 `CASE` lines + `cases=14 observed_pass=8 observed_fail=6 mismatches=0` + `regrade cases=14 differ=0`. Every entry case letter and observed verdict equals the receipt line (nop F/fail, oracle-solve-sh P/pass, decrypt-public-keys P/pass, replay-public-gen P/pass, copy-public-constants P/pass, oracle-concatenated P/pass, oracle-plus-decoys P/pass, oracle-reversed P/pass, oracle-zero-padded P/pass, one-missing F/fail, hex-output F/fail, wrong-key-decrypt F/fail, pairs-plaintexts F/fail, ciphertexts-copied F/fail); receipt order = entry order; `match=yes` on all 14; `regrade=same` on all 14.

| Finding | Receipt/static support | Verdict |
|---|---|---|
| 1 nop F; FileNotFoundError; no `exists()`; :120 decides, :122 unreached | receipt nop line contains `FileNotFoundError -- no /app/plaintexts.txt (the image state only)` verbatim; `exists(` absent in test_outputs.py; :120 is bare `open`, :122 inside same function | supported |
| 2 oracle-solve-sh P; solve.sh writes/compiles :303, redirects :304, runs ./decrypt :289 | receipt oracle-solve-sh P/pass; solve.sh 289/303/304 lines verified | supported |
| 3 three public passes; keys gen.py:12; chain :61-62; constants test_outputs.py:4-103; image deletes only gen.py (Dockerfile:14), never ships tests | receipt all three P/pass; lines verified; constants==chain identity checked below | supported |
| 4 shape free: concatenated/reversed/zero-padded/decoys all pass | receipt: four P/pass | supported |
| 5 one-missing F; conjunction only quantity | receipt F/fail | supported |
| 6 hex-output F; instruction.md:9-10 names no format; decimal shape from decrypt.c:136 `printf("%lu\n", plaintext)` via solve.sh:290 `system(cmd)`; zero-padded passes | receipt hex-output F/fail and oracle-zero-padded P/pass; lines verified | supported |
| 7 wrong-key-decrypt F; positive control decrypt-public-keys passes | receipt F/fail and P/pass | supported |
| 8 oracle-plus-decoys P; 200 numbers pass; pairs-plaintexts F (32 true, 68 missing) | receipt P/pass and F/fail | supported |
| 9 pairs-plaintexts F; ciphertexts-copied F | receipt F/fail both | supported |
| 10 test.sh:25-29 reward from exit status; no partial credit | test.sh 25-29 verified (`if [ $? -eq 0 ]; then` / `echo 1 > …reward.txt` / `else` / `echo 0 > …reward.txt`); receipt distinguishes recipes, not rewards | supported |

Requirement-map labels recomputed from the receipt's `violates=` sets: known-plaintext-attack → partly (6 cases, mixed), recover-key → partly (7 cases, mixed), decrypt-all → partly (7 cases, mixed), plaintexts-file → enforced (nop only, fails). Matches the entry's table and prose. Contestable-tags prose verified against the receipt tags (replay-public-gen carries recover-key; decrypt-public-keys carries known-plaintext-attack but not decrypt-all).

Predictor/constants identity: `CONSTANTS` generated from `hashlib.sha256(b"0x68e630x625710x1f61c0xb74a5").digest()` + `struct.pack(">Q", 32+i)`[:8] for i in 0..99 equals the 100 constants parsed from `test_outputs.py:4-103` exactly, in order (100/100). Supports the entry's “verified here … all 100 in order” claim (Findings 3, Predictor comment).

## Defects

None found. Table of checks executed: 22 located quotes, 14 mechanism quotes, 96 inline capture refs, 10 findings, 4 requirement-map labels, constants identity — 0 mismatches, 0 wrong findings.

## Observations (non-defects)

- Entry line 18 cites `` `tests/test_outputs.py:106-122` `` — repository-relative path; the capture stores the bare file `test_outputs.py`. Same file, valid range 106–122 (def at 106, file ends at 122). Not a defect.
- Entry line 334 cites `` `alexgshaw/feal-linear-cryptanalysis:20251031` `` — a Docker image tag (content of task.toml:29), not a capture reference. Correctly quoted; matches task.toml:29.
- All other inline `capture:line` tokens resolve to capture files with in-range lines, including two-line tokens (`:25-29`, `:106-122`, `:303-304`, `:4-103`, `:60-62`, `:19-20`, `:26-28`, `:30-31`, `:61-62`, `:31-32`, `:18-29`, `:25-29`, `:22-25`, `:1-10`, `:1-14`, `:1-29`, `:1-32`, `:1-304`, `:1-141`, `:1-41`, `:1-97`).

## Evidence

- Verification script outputs: `.ufo/waves/round-44/residual/R44RRevEntryQuotes/quote_results.json` (134 checks), `prose_quotes.json`.
- Capture checksums: all `OK` from `sha256sum -c SHA256SUMS`.
- Receipt assertions reproduced in-script from the receipt file.

VERDICT: quotes-36/36-findings-wrong-0
