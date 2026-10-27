# R44CritIndep — derived predictions from captures alone (written BEFORE reading the receipt)

Source: corpus/evidence/round44/tb2-feal-linear-cryptanalysis/ captures:
- test_outputs.py:4-103 soln = 100 decimal constants; :120 `data = open("/app/plaintexts.txt").read()`;
  :121-122 `for c in soln.split(): assert c in data` -> single test, all-or-nothing, substring membership,
  no count/order/format/exactness check.
- test.sh:18-22 runs pytest via uvx; :25-29 `if [ $? -eq 0 ]; then echo 1 > /logs/verifier/reward.txt; else echo 0 ...`
  -> PASS iff pytest exit 0 (every assert holds); any missing-file error or failed assert -> FAIL.
- gen.py:12 keys = 0x68e63,0x62571,0x1f61c,0xb74a5; :19-28 plaintext = int(sha256(sha256(keys).digest() +
  pack(">Q", i))[:8]) -> public keys + public hash chain fully determine the 100 plaintexts.
- Dockerfile:13 `rm orig_plaintexts.txt`, :14 `rm gen.py` -> only ciphertexts.txt, pairs.txt, feal, decrypt remain.
- decrypt.c main: reads ciphertext lines, printf("%lu\n", plaintext) -> decimal, newline-separated.
- instruction.md:8-10: decrypt all ciphertexts in /app/ciphertexts.txt, save to /app/plaintexts.txt (no format spec).

## Model (predictor)
Verdict = PASS iff /app/plaintexts.txt exists AND every one of the 100 soln constants occurs as a substring of its
decoded text; else FAIL (missing file -> pytest error -> exit!=0 -> reward 0; any missing constant -> assert fail).

## Per-behavior predictions
| behavior | predicted verdict | reason (from captures) |
|---|---|---|
| no file | FAIL | open() FileNotFoundError -> pytest error -> nonzero -> reward 0 |
| one constant missing | FAIL | that `assert c in data` fails |
| hex content | FAIL | hex digit strings are not substrings of the decimal constants |
| wrong key decrypt | FAIL | yields different numbers (with overwhelming probability, none equal the constants) |
| pairs plaintexts (32 pairs lines) | FAIL | pair-file numbers != the 100 constants |
| ciphertexts copied | FAIL | ciphertext values != plaintext constants |
| decrypt with public gen.py keys | PASS | correct keys -> correct plaintexts == constants in decimal |
| replay public gen.py hash chain | PASS | same bytes as constants |
| copy constants from test_outputs.py | PASS | every constant present verbatim |
| concatenated constants | PASS | each constant occurs as substring of the concatenation |
| reversed order (lines reversed) | PASS | order ignored by membership test |
| zero-padded constants | PASS | e.g. "0105..." still contains "105..." as substring |
| 100 wrong-key decoys appended | PASS | real constants still present; extra lines ignored |
| (14th case unknown pre-receipt) | evaluate per model | — |
