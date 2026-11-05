# S278 gate note (ScribeR89, round 89 wave 1)

Source row: `corpus/SOURCES.md` line 294, S278 (`grep -n 'S278' corpus/SOURCES.md` 2026-11-05). Tier A, scope "member replay only".

Quote (5 whitespace-split words, from line 19 of the pinned file): `assert polyglot_files == ["main.rs"], (`

Access date: 2026-11-05.

Re-verification, one fetch, as specified:

```
$ curl -sS -m 30 -o /dev/null -w '%{http_code} %{size_download}\n' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-rust-c/tests/test_outputs.py
200 1638
curl exit 0
```

Result: HTTP 200, 1638 bytes, matching the S278 row (`live HTTP 200, 1638 B`) and the captured copy (`wc -c` 1638 2026-11-05).

Byte check on the captured copy (`sha256sum corpus/evidence/round52/graders/polyglot-rust-c/tests/test_outputs.py` 2026-11-05): `baed5e4d0cc0e5809ff41a7df1815d18c65c708a3a3f264428e1cda11ce692f9`, equal to the S278 row and the frozen subject SHA. The live body itself was not hashed, because the single fetch used `-o /dev/null` as specified; the status and size are the only live evidence.

Notes for the L1 (frozen text, reported not repaired):

- The assignment's grader line references ":27-44 and :30-44" do not match the file. Measured (`grep -n` 2026-11-05): size list at :27; loop `for n, expected` at :29; `subprocess.run` at :30 and :37; `check=True` at :34 and :41; `rust_out == expected and cpp_out == expected` assert at :44; file ends at :46. The draft uses these numbers.
- The prediction note in `plans/round89-cases.json` says the grader is at "lines 14-46"; the function `def test_fibonacci_polyglot` begins at :10 (`grep -n 'def test_'` 2026-11-05). The 14-46 span covers the body after the docstring, so it is a loose reference, not an error in the vectors.
