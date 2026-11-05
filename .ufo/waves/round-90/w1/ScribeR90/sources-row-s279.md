# S279 row draft (ScribeR90) — for `corpus/SOURCES.md`, appended after S278 (line 294)

Draft only. The L1 integrates. Named placeholders (angle brackets) are filled from ScoutS279's
`.ufo/waves/round-90/w1/ScoutS279/gate-note.md`, never invented here:

- `<LINE>`, `<QUOTE>`, `<WORDS>`: the scout's located quote (≤ 25 whitespace-split words), its file line and its word count.
- `<FETCH-HTTP>`, `<FETCH-BYTES>`, `<FETCH-SHA256>`: the scout's single curl (HTTP code, byte count, sha256).

Fixed facts already checked by the scribe in this round (read-only):
- Round-52 capture `corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py` sha256 = `2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149` (matches the frozen subject SHA in `plans/round-90-claims.md`).
- The capture defines five test functions: `test_git_repo_init` :10, `test_both_bundles_fetched` :16, `test_algo_py_exists` :34, `test_algo_py_has_map_function` :40, `test_algo_map_function_with_test_input` :52.
- The same capture directory holds `tests/test.sh` (the scout's reject-candidate second row).

Cell style: copied from the S278 row (11 cells, `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`, one line, no literal or escaped pipe in any cell).

```
| S279 | Terminal-Bench 2.0 merge-diff-arc-agi-task pinned grader — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py | code | A | member replay only | test_outputs.py:<LINE> quote `<QUOTE>` (<WORDS> whitespace-split words); opened 2026-11-05; live HTTP <FETCH-HTTP>, <FETCH-BYTES> B, sha256 <FETCH-SHA256>, byte-identical to the round-52 capture (sha256 2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149) | five test functions over one graded state (git repo, algo.py, /tests/test.json): test_git_repo_init :10, test_both_bundles_fetched :16, test_algo_py_exists :34, test_algo_py_has_map_function :40, test_algo_map_function_with_test_input :52; acceptance semantics of this pinned grader only, not a solved-task, git-semantics or Terminal-Bench harness claim | mined | 2026-11-05 | 180d | corpus/lessons/round-90.md, corpus/evidence/round90/ |
```

Checks for the L1 before admission (scribe-side, not executed here):
- `awk -F'|' 'NR==N {print NF}'` on the appended line must print 13 (11 cells plus the two outer empty fields), as for S278 (`sed -n 294p corpus/SOURCES.md | awk -F'|' '{print NF}'` = 13 at round 90 base).
- `grep -c '^| S279 '` = 1 after the append; census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` exits 0 with 271 rows (270 measured before the round).

Gate status: the row is admitted only if the scout's fetched bytes are identical to the capture (`cmp` exit 0) and `<QUOTE>` is found at `<LINE>` of the fetched file. If either fails, the row is a rejection with the scout's reason, not an admission.
