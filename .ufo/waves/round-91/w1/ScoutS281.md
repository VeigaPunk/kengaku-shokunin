# ScoutS281 — findings (R91, w1)

Full evidence: `.ufo/waves/round-91/w1/ScoutS281/gate-note.md`. Tip read: master = `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0`.

| check | command | exit | verdict |
|---|---|---|---|
| fetch test_outputs.py | `curl -sS -o $S/test_outputs.py -w '%{http_code} %{size_download}' $U/test_outputs.py` | 0 | PASS: 200, 2330 B, sha256 0c24195f…02a977 |
| fetch test.sh | `curl -sS -o $S/test.sh -w … $U/test.sh` | 0 | PASS: 200, 721 B, sha256 e868c854…f0281 |
| cmp vs round-52 capture | `cmp $S/test_outputs.py $L/corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py` | 0 | PASS: identical |
| S281 quote | `sed -n 27p` / `awk '{print NF}'` | 0 | PASS: exact text, 10 words |
| defs | `grep -n '^def ' $S/test_outputs.py` | 0 | PASS: 11, 46. Frozen claims cite 16–42 and 45–48; actual spans are 11–43 and 46–50, so **both frozen ranges are wrong** (disclosed as lesson M2) |
| S282 quote | `sed -n 5p $S/test.sh` | 0 | PASS: `apt-get install -y curl`, 4 words |
| SOURCES rows | `git -C $L show a8de3e69:corpus/SOURCES.md \| grep -E '^\| S28[12] '` | 0 | S281: all facts MATCH. S282: identity facts MATCH; the reason clause "adds no grader semantics beyond S281" is NOT SUPPORTED |

Proposed narrowing (S282, keep `rejected`): `test.sh:18–25` uvx `-p 3.13` plus pinned numpy/pandas/scipy/matplotlib become the grader's `sys.executable` at `test_outputs.py:21`. That interpreter decides the `returncode == 0` assert at :23, so it is grader semantics. The offline probe uses host python 3.14.8 (`round91_modernize_probe.py:109`). Disclose this as a C1 limit in a supersede row. S281: no rejection.

By-catch:
1. Lesson `## Gate` S282 says "first capture". In fact the lane has held byte-identical test.sh since round 52: `cmp` exit 0; blob 896bbdbb, added in 19bc16c4.
2. Claims :58 says the cases hold 3 distinct vectors. The frozen case table has 4: EP/FP/PF/PP.
3. The Station 102 regex (:40) has no `-?`, so a printed `-30.30` passes. No case covers it.
4. `prediction_note` "lines 1-48" stops before the any() assert (49–50).

Installs: none. Scratch `/fast/scratch/hyaku/kengaku-r91/ScoutS281` removed on exit.
