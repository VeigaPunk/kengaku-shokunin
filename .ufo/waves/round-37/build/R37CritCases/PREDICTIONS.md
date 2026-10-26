# R37CritCases — predictions for 4 uncovered grader cases (written before any run)

Frozen probe: `plans/git_webserver_probe.py` (imported, not edited; `Case`, `files`, `run_case`).
Captures at their pinned digests: instruction.md 62151b73…, test_outputs.py 526aee3d…, verify.sh 1dc44c92…
Static reading used: `cat -n` of the captured verify.sh / test_outputs.py / instruction.md (2026-10-26).

| id | fixture (server, tools) | predicted | mechanism the case should isolate | why uncovered by the 22 |
|---|---|---|---|---|
| `multiline-token` | curl, files: `200`, body `"first line\nTEST PASSED\n"` | **pass** | verify.sh:62 `echo "Content: $CONTENT"` emits a multi-line body as several stdout lines; test_outputs.py:13 is a substring test over all of stdout, so the token on the body's *second* line still passes | every token case in the 22 (token-in-body, wget-token-in-body) puts the token as the entire body — the multi-line echo is never exercised |
| `hello-plus-second-line` | curl, files: `200`, body `"hello world\nsecond line\n"` | **fail** | verify.sh:60 strips only trailing newlines; :63 compares the whole remaining value, so a right first line plus an extra line is a mismatch | no case has a body with more than one non-newline line; trailing-newlines (pass) only shows stripping, not that surplus lines survive |
| `token-with-404` | curl, files: `404`, body `"TEST PASSED\n"` | **fail** | verify.sh:59 sends a non-200 to :71, so the body is never echoed; the token only works through the 200 branch. Control for token-in-body | token-in-body is `200` only; no case shows the token failing when it cannot be echoed |
| `second-request-500` | curl, sequence: `[[200, "hello world\n"], [500, "hello world\n"]]` | **pass** | verify.sh:60 does not check the second request's status; `curl -s` prints a 500 body, so :63 still matches | status-then-content-split varies the *first* body, first-request-404 varies the *first* status; the second response's status is never non-200 in the 22 |

Ordering note: this file is written before `run_uncovered.py` exists or runs; the run log repeats the four
predictions before any observation, and its output is `run_uncovered.log` in this directory.
