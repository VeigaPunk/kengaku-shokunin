# F37ReopenRows — wave-2 falsify: live re-open of rows S111–S113 (kengaku round 37, 2026-10-26)

Seat: reviewer (leaf). Target: the three registry rows S111–S113 in `corpus/SOURCES.md` (lines 126–128), their anchors vs `corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`, their located quotes, tier/kind/scope, `teaches` grounding, and the lesson `corpus/lessons/round-37.md` `## Gate` rows (lines 22–24).

Method: fetched the three pinned raw URLs live today at commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` into scratch `/fast/scratch/hyaku/kengaku-r37/F37ReopenRows/fetch` (curl, output sizes 547/2681/451 bytes), compared `sha256sum` of the fetches against (a) each row's anchor digest and (b) the frozen `SHA256SUMS`, re-checked the lane captures with `sha256sum -c`, verified every stated quote line with `sed -n`, and checked substring-ness and word counts programmatically. Receipts: `.ufo/waves/round-37/falsify/F37ReopenRows/receipts/` (three fetched files + `transcript.txt` with every command and output below). Scratch removed at end.

## 1. Digests: live fetch vs row anchors vs SHA256SUMS — 3/3 match

| File | Row anchor (SOURCES.md) | SHA256SUMS (frozen) | Live fetch 2026-10-26 | Match |
|---|---|---|---|---|
| `tests/test_outputs.py` (S111, :126) | `526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37` | same | `526aee3d…46b37` | ✓ |
| `tests/verify.sh` (S112, :127) | `1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05` | same | `1dc44c92…3d05` | ✓ |
| `instruction.md` (S113, :128) | `62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97` | same | `62151b73…1d97` | ✓ |

Commands: `sha256sum test_outputs.py verify.sh instruction.md` over the live fetches (receipts §1); `sha256sum -c SHA256SUMS` in `corpus/evidence/round37/tb2-git-webserver/` → all six files `OK` (receipts §2). No drift; the pins hold at the tip's freeze.

## 2. Located quotes verbatim at stated lines — 3/3 pass

- **S111** anchor: `tests/test_outputs.py:9-13, :13 "assert "TEST PASSED" in result.stdout" (5 words)`. `sed -n '13p'` → `    assert "TEST PASSED" in result.stdout, "Did not pass test"`. Quote is an exact substring of line 13; stated range 9–13 is the whole file's one test function (file is exactly 13 lines, `wc -l`). Words: 5, matches the stated count, ≤25. ✓
- **S112** anchor: `tests/verify.sh:49, :57-63, :62 "echo "Content: $CONTENT"" (3 words)`. `sed -n '62p'` → `        echo "Content: $CONTENT"` — exact substring; `sed -n '49p'` → `./git_test.exp` and `sed -n '57,63p'` show the status/body/echo block, both locations exist (file is 91 lines). Words: 3, matches, ≤25. ✓
- **S113** anchor: `instruction.md:1-10, :9 "then I see the output "hello world"." (7 words)`. `sed -n '9p'` → `then I see the output "hello world".` — the quote is the full line, verbatim; range 1–10 is the whole file (10 lines). Words: 7, matches, ≤25. ✓

Programmatic check (python3 substring + word count over the fetched files): `S111: line13 substring=True words=5`, `S112: line62 substring=True words=3`, `S113: line9 substring=True words=7` (receipts §4).

## 3. tier / kind / scope — sensible, 3/3

- **S111**: kind `code`, tier A, scope "the executed scoring predicate … a stdout substring over a helper shell script … for the code's own behaviour". Correct: it is the pytest file the harness runs; the scope stays inside what the file does (one test, substring over stdout) and does not claim task validity. ✓
- **S112**: kind `code`, tier A, scope "the shell script the grader's single assertion reads … which steps it runs, which statuses it ignores, and how status and body are obtained — for the script's own behaviour". Correct and appropriately bounded to the script's behaviour. ✓
- **S113**: kind `docs`, tier A, scope "the request this one task states to the agent … as the maintainer's own specification the grader is mapped against". Correct: an instruction file, read as the task's own spec. ✓

All three: `status=mined`, `opened=2026-10-26`, `recheck=180d`, `used-by=corpus/knowledge/tb2-git-webserver-grader.md` (file exists; its source lines 1–3 name the same three URLs, lines 1–13 / 1–92 / 1–10 — the 92-line claim for verify.sh is off by one: `wc -l` gives 91 lines, a trailing-newline count difference in the doc's prose, not in any row cell; noted as an observation, not a row defect).

## 4. `teaches` grounded — 3/3

- **S111** teaches: "the task score is one pytest function asserting the substring TEST PASSED anywhere in a helper script's stdout, not the helper's exit status nor the served artefact's provenance". Grounded: lines 9–13 are the file's only test; line 11 `subprocess.run(["bash", "/tests/verify.sh"], capture_output=True, text=True)` never reads `returncode`; line 13 is a substring `in result.stdout`; nothing inspects the served artefact's provenance. ✓
- **S112** teaches: "the helper ignores the git step's exit status, fetches status and body in two separate requests, and echoes the body into the stdout the assertion reads". Grounded: line 1 `#!/bin/bash` with no `set -e`; line 49 `./git_test.exp` is followed by no `$?` check; line 57 fetches status (`-o /dev/null -w "%{http_code}"`) and line 60 fetches the body (`CONTENT=$(curl -s …)`) — two separate requests; line 62 echoes the body into stdout. ✓
- **S113** teaches: "a git server plus a push landing on a webserver on port 8080 served back as the exact text hello world; the git half is unobserved by the grader". Grounded: lines 1–6 are the git half, 7–9 the webserver/port-8080/output half (sed 1–10 in receipts §3); "the git half is unobserved by the grader" is the cross-row consequence of S111/S112's behaviour (no assertion reads clone/commit/push state), consistent with the knowledge doc's requirement map (`instruction.md:1-6` → unenforced). ✓

## 5. Lesson `## Gate` quotes (round-37.md:22–24) — 3/3 pass

- **S111 Gate** (:22): quote, line 13: `assert "TEST PASSED" in result.stdout, "Did not pass test"` — the full line 13 verbatim (9 words, ≤25); sha256 `526aee3d…46b37` matches the live digest. The row's "re-opened live by `R37ReopenPins` (`IDENTICAL`, `sha256sum -c` OK)" is a wave-1 seat's historical claim I cannot re-run, but my independent re-open reproduces its result (identical digests, `sha256sum -c` OK). ✓
- **S112 Gate** (:23): quote, line 62: `echo "Content: $CONTENT"` — verbatim (3 words); sha256 `1dc44c92…3d05` matches; the gloss "it echoes the served body into that stdout" is grounded in line 62. ✓
- **S113 Gate** (:24): quote, line 9: `then I see the output "hello world".` — verbatim (7 words); sha256 `62151b73…1d97` matches; "Lines 1–6 ask for the git half, 7–9 for the served output" matches the sed 1–10 output. ✓

## Findings

No defect found against the landing in this seat's scope. Three rows, three digests, three quotes, three Gate quotes — all verified against a fresh live fetch at the pinned commit. One non-row observation: `corpus/knowledge/tb2-git-webserver-grader.md:2` says "lines 1–92" for `verify.sh`; the file has 91 lines (`wc -l`). The row cells and the gate-checked quotes are unaffected; the doc's own located-quote table (which the C2 gate checks) is out of my scope and was not audited line-by-line here.

Residual risk: the fetch is over HTTPS to the pinned raw URL; a compromised CDN view cannot be ruled out from this seat, but the lane captures (`sha256sum -c` OK) and the live fetch agree byte-for-byte, which is the check the recheck clause asks for.

Receipts: `.ufo/waves/round-37/falsify/F37ReopenRows/receipts/` (`test_outputs.py`, `verify.sh`, `instruction.md` — live fetches, digests as in §1 — and `transcript.txt` with all commands and outputs). Scratch `/fast/scratch/hyaku/kengaku-r37/F37ReopenRows` deleted after copying.

VERDICT: rows-3/3-quotes-3/3
