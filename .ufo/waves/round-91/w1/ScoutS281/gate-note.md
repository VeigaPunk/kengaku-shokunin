# ScoutS281 — gate note: S281 / S282 registry quotes (read-only)

Seat: ScoutS281 (scout, leaf). Lane tip read: `git -C <lane> rev-parse master` = `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0` (= TIP C `a8de3e69`).
Scratch: `S=/fast/scratch/hyaku/kengaku-r91/ScoutS281` (created `mkdir -p`, removed on exit). No lane mutation; no installs.
`U=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/modernize-scientific-stack/tests`, `L=/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## 1. Live fetch (once each)

```
curl -sS -o "$S/test_outputs.py" -w '... http=%{http_code} bytes=%{size_download}\n' "$U/test_outputs.py"   # exit 0
curl -sS -o "$S/test.sh"         -w '... http=%{http_code} bytes=%{size_download}\n' "$U/test.sh"           # exit 0
sha256sum "$S/test_outputs.py" "$S/test.sh"
```
Output:
```
test_outputs.py http=200 bytes=2330
test.sh http=200 bytes=721
0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977  test_outputs.py
e868c85466ebf4815e2e4efbd252bf50ad979bceb14325a9377b1bbf852f0281  test.sh
```
Verdict: PASS — HTTP 200 / 2330 B / `0c24195f…02a977` and HTTP 200 / 721 B / `e868c854…f0281` match the claims file (lines 57, 136) and both SOURCES rows.

## 2. Byte compare with the round-52 capture

```
cmp "$S/test_outputs.py" "$L/corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py"   # exit 0, no output
git -C "$L" cat-file -p a8de3e69:corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py | cmp - "$S/test_outputs.py"   # exit 0
```
Verdict: PASS — identical in the worktree and at TIP C.

By-catch (test.sh):
```
cmp "$S/test.sh" "$L/corpus/evidence/round52/graders/modernize-scientific-stack/tests/test.sh"   # exit 0
git hash-object "$S/test.sh"   # 896bbdbb8b8488c1c2557135636b6430154c5f1e
git -C "$L" ls-tree -r a8de3e69 | grep 896bbdbb   # 100644 blob 896bbdbb… corpus/evidence/round52/graders/modernize-scientific-stack/tests/test.sh
git -C "$L" log --diff-filter=A --format='%h %ad %s' --date=short -- corpus/evidence/round52/.../tests/test.sh
#   19bc16c4 2026-10-28 round-52: correct capture census and hand-read set in C1; land pinned TB2 captures
```
The lane has held these exact test.sh bytes since round 52 (`19bc16c4`). The round lesson's `## Gate` S282 row (`corpus/lessons/round-91.md:14` at C) says "byte-identical to nothing held before (first capture)". **The bytes contradict that statement.** The SOURCES S282 row does not repeat it, so the row is unaffected.

## 3. S281 located quote and function lines

```
sed -n '27p' "$S/test_outputs.py" | cat -A
#       assert "Station 101" in output, "Must output Station 101 results"$
sed -n '27p' "$S/test_outputs.py" | awk '{print "words="NF}'
# words=10
grep -n '^def ' "$S/test_outputs.py"
# 11:def test_modernized_code_runs():
# 46:def test_dependency_file_exists():
```
Verdict: PASS — line 27 text matches exactly (4-space indent; no trailing whitespace); 10 words; `def`s at 11 and 46.

**Discrepancy (frozen text, not repairable):** `plans/round-91-claims.md:35` cites `test_modernized_code_runs` as "lines 16–42" and `:38` cites `test_dependency_file_exists` as "lines 45–48". The bytes have function 1 at **11–43** (def 11; last assert 43) and function 2 at **46–50** (def 46; `any()` assert 49–50). Both frozen ranges are wrong. 16–42 drops the script-exists assert (15) and the Station 102 tolerance assert (43). 45–48 starts on a blank line and drops the assert. The claims file is unchanged A→C (`git diff --quiet cd0c116e a8de3e69 -- plans/round-91-claims.md` exit 0), so the error is frozen. Lesson M2 already discloses it. A similar nit sits in the frozen case table: `plans/round91-cases.json` `prediction_note` says it read "test_outputs.py lines 1-48". The file has 53 newline-terminated lines plus an unterminated line 54 (`wc -l` = 53), so that range also stops before the `any()` assert.

## 4. S282 located quote

```
sed -n '5p' "$S/test.sh" | cat -A      # apt-get install -y curl$
sed -n '5p' "$S/test.sh" | awk '{print "words="NF}'   # words=4
```
Verdict: PASS.

## 5. SOURCES rows at TIP C

```
git -C "$L" show a8de3e69:corpus/SOURCES.md | grep -E '^\| S28[12] '   # exit 0, 2 rows
```

**S281** (code, tier A, `mined`, scope "member replay only"). Each fact against the bytes:
- URL, HTTP 200, 2330 B, sha256 `0c24195f…02a977`, byte-identical to the round-52 capture: MATCH (§1, §2).
- Quote `test_outputs.py:27` …, 10 words: MATCH (§3).
- "two test functions over a staged /app script, CSV and dependency file": MATCH (lines 11/46; paths `/app/analyze_climate_modern.py` :14, `/app/climate_analyzer/sample_data/climate_data.csv` :17, `/app/requirements.txt`/`/app/pyproject.toml` :48).
- "script-run returncode check": MATCH (:23).
- "two station-name asserts with a 0.1 numeric tolerance": MATCH in substance but loosely worded. The station-name asserts (:27, :28) are separate from the two regex-match asserts (:35, :41) and the two `< 0.1` tolerance asserts (:37, :43).
- "a phrase check": MATCH (:29, case-folded via `output.lower()`).
- "one dependency-file any() check": MATCH (:49).
- "30 s subprocess timeout that surfaces uncaught": MATCH (:21–22 `timeout=30`; no try/except anywhere in the module).
Verdict: row facts MATCH the fetched bytes.

**S282** (tool, tier A, `rejected`, scope "harness wrapper only"):
- URL, HTTP 200, 721 B, sha256 `e868c854…f0281`: MATCH (§1).
- Quote `test.sh:5` `apt-get install -y curl`, 4 words: MATCH (§4).
- "installs curl and uv over the network": MATCH (:4–5 apt-get; :8 `curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh`).
- "runs uvx pytest over /tests/test_outputs.py, writing reward.txt": MATCH (:18–26; :29–33 writes 1 on exit 0, otherwise 0).
- Rejection reason "the wrapper adds no grader semantics beyond the test_outputs.py held as S281": **NOT SUPPORTED by the bytes** (see §6). The rest of the reason (offline replay can't run apt/curl/uv over the network) MATCHES.
Verdict: identity facts MATCH. The "no grader semantics" clause overstates.

## 6. Proposed rejection / narrowing

**Narrow S282's rejection reason. Keep the `rejected` status and its flip.** Bytes:
- `test.sh:18–25`: `uvx -p 3.13 -w pytest==8.4.1 -w numpy==2.3.4 -w pandas==2.3.3 -w matplotlib==3.10.7 -w scipy==1.16.3 -w pytest-json-ctrf==0.3.5 pytest …`.
- `test_outputs.py:21`: `subprocess.run([sys.executable, str(script_path)], …)`.

Under the real harness, `sys.executable` is the uvx-provisioned CPython 3.13, which has exactly those numpy/pandas/scipy/matplotlib versions installed. The graded `returncode == 0` assert (:23) for a "modernized scientific stack" script is therefore decided by the interpreter and library set that test.sh pins. The task's dependency file (requirements.txt/pyproject.toml) is only checked for existence and is never installed. That makes it grader semantics beyond S281. Other wrapper semantics:
- `test.sh:13–16` exits 1 without writing reward.txt when `$PWD` is `/`.
- `:29–33` maps the pytest exit code to the reward.

The C1 probe runs the script with the host `sys.executable` (`plans/round91_modernize_probe.py:109`, `sys.executable -I -B …`; host python 3.14.8). The case fixtures are stdlib-`csv` scripts, so I see no effect on the ten frozen vectors [INFERENCE: not re-run]. The general statement is still false to the bytes.

Proposed supersede text (append-only, as a new row; not made by this seat): "REJECTED: network-bound (apt, curl, uv); its environment semantics — python 3.13 plus pinned numpy 2.3.4 / pandas 2.3.3 / scipy 1.16.3 / matplotlib 3.10.7, which become the grader's `sys.executable` at test_outputs.py:21 — are not replayed offline and are disclosed as a C1 limit; flip unchanged."

No rejection proposed for S281.

## By-catch (for routing, not this item's verdict)

1. **Frozen claims vs frozen case table.** `round-91-claims.md:58` honest limit (a) says the ten cases yield "three distinct predicted vectors (`PP`, `FP`, `PF`)". The frozen `plans/round91-cases.json` (unchanged since A) has **four**: `['EP','FP','PF','PP']` (`script-hangs` = `EP`). The claim text undercounts its own E leg (it names the timeout class at :42 but leaves EP out of the count).
2. **Untested grader asymmetry.** The Station 102 regex (`test_outputs.py:40` `r'Station 102.*?(\d+\.\d+)'`) has no `-?`, unlike Station 101's (:34). An output of `Station 102 mean temperature: -30.30` therefore parses as `30.30` and passes :43. None of the ten cases stages a negative Station 102 value. This is not a defect of the claim, but it is the sharpest discriminating case the table does not hold.
3. **Lesson Gate S282 "first capture" is false** (§2): the lane has held identical test.sh bytes since round 52 (`19bc16c4`).
