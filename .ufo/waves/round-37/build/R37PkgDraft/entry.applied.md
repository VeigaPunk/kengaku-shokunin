source: S111 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py — the one test function, lines 1–13, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S112 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/verify.sh — the helper shell script the test calls, lines 1–91, same commit, accessed 2026-10-26
source: S113 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/instruction.md — the request, lines 1–10, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — re-fetch the three pinned URLs, run `sha256sum -c corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`, and re-run `plans/git_webserver_probe.py --lane .`; any digest or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `configure-git-webserver`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `configure-git-webserver` task's whole score is one pytest
function, `test_hello_html_exists`, which shells out to `bash /tests/verify.sh` and asserts that the
script's **stdout contains the substring `TEST PASSED`**. `tests/test.sh` maps the pytest exit status
to a binary reward. The graded artefact is neither a data string nor an agent-authored file: it is a
**live HTTP service on port 8080** plus a git server that the helper script tries to clone from, commit
to and push to through an `expect` script — while no step in that script reads the git step's exit
status. Two mechanisms do the real deciding: a shell string comparison of the fetched body after
command substitution, and a Python substring search over everything the helper printed, including an
echo of that body.

Offline execution of the captured grader inside a bubblewrap sandbox over 22 frozen cases
(`plans/git_webserver_probe.py`; receipt `corpus/evidence/round37/git-webserver-probe.txt`) reproduced
every prediction written from the static reading before the first run:

`cases=22 observed_pass=9 observed_fail=13 mismatches=0`

Six of the nine passing cases are states in which the stated request (a git server whose push lands on
a web server) was abandoned or never happened: a static file served from a directory with no
repository, no hook and no push passes; a body whose only content is the token `TEST PASSED` passes
while the helper prints `TEST FAILED`; a body whose first request was not the content that passed the
content check passes. A seventh and eighth pass are legitimate controls (an exact body with no trailing
newline, and the `wget` branch taken when `curl` is absent).

This entry extends `knowledge/benchmark-verifier-execution-model.md` (where a TB2 verifier runs; S100
is the same repository at the same commit), `knowledge/benchmark-grader-semantics.md` (one Toolathlon
grader read) and `knowledge/tb2-regex-log-grader.md` (round 36's TB2 task read the same way), and adds
a grader class the lane has not read before: a verdict that is a **stdout substring over a shell
helper probing a live service**, where status, content and body-echo come from separate places. It
discharges, for this one task only, the `corpus/README.md` §Frontier clause that left "the other TB2
tasks" open.

## Source labels

S111–S113 are the benchmark maintainers' own task files: primary for *what this grader checks* and for
the requirement text it is mapped against, and a self-report for everything else. `task.toml` (captured,
not a registry row) is the authors' own metadata and is read only for the task description and the
verifier timeout. The captured `solution/solve.sh` oracle is **own reading, tier C** — it is not a
registry row, was not executed, and nothing below rests on it. The probe receipt is the lane's own
re-runnable gate output (tier A for its own scope: these 22 states against these captures under the
host's Python and `bash`, in a private network namespace).

Disclosure: the probe predictions were written from a static reading of `verify.sh`,
`test_outputs.py` and `instruction.md` **before the first run**, and the frozen case table
(`corpus/evidence/round37/git-webserver-dry-cases-freeze.txt`) carries them; the second run's receipt
was byte-equal to the first. No prediction mismatched, so this entry reports no re-prediction.

## What the grader checks (static reading)

| Step | Mechanism | Lines |
|---|---|---|
| Entry point | `subprocess.run(["bash", "/tests/verify.sh"], capture_output=True, text=True)` — the helper is a black box; only its stdout is read, never its exit status | `test_outputs.py:11` |
| Decision | `assert "TEST PASSED" in result.stdout` — a case-sensitive **substring** of the whole stdout, not a line or a prefix | `test_outputs.py:13` |
| Reward | `test.sh` runs the file under `uvx -p 3.13` with `pytest==8.4.1` and writes `1` iff pytest exits 0, else `0` | `test.sh:14-25` |
| Environment setup | `apt-get update` then `apt-get install -y expect` (the comment above says it installs curl; it does not), plus a `~/.ssh/config` with `StrictHostKeyChecking no` | `verify.sh:4-13` |
| Git step | an `expect` script clones `git@localhost:/git/server`, echoes `hello world` into `hello.html`, commits and pushes; `verify.sh:49` runs it and **ignores its status** | `verify.sh:16-49` |
| Status check | first request: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/hello.html`, compared to the literal `200` | `verify.sh:57-59` |
| Content check | **second** request: `CONTENT=$(curl -s http://localhost:8080/hello.html)`, then `[ "$CONTENT" = "hello world" ]` | `verify.sh:60-63` |
| Echo | the body is printed as `Content: $CONTENT` into the same stdout the assertion reads | `verify.sh:62` |
| wget branch | taken when `curl` is not on `PATH`: `wget -q -O test_output.html …`, `if [ $? -eq 0 ]` gates the same content comparison | `verify.sh:73-90` |

Three structural consequences follow from the reading alone:

- `curl` runs without `-L` and without `--max-time`, so a redirect is a non-200 status and a slow
  server still counts as long as the answer arrives before the harness timeout
  (`task.toml:22` declares `timeout_sec = 900.0` for the verifier).
- Command substitution strips **trailing newlines only**: `hello world\n\n\n` compares equal, while a
  leading space, a trailing space, a `\r` or a BOM do not.
- Status and content are two separate requests to the same path. Nothing compares the first response's
  body, so a server that answers the first request with a different body and the second with
  `hello world` passes (`status-then-content-split`).

## Requirement map

Labels are read off the executed receipt, not from the prose: `enforced` means a probe case that
violates the requirement is observed `fail`; `unenforced` means a state violating it is observed
`pass`; `partly` means the hypothesis direction is confirmed for one clause of the line and shown
free for another. Case ids are the receipt's `CASE` ids.

| Instruction line | Label | Receipt cases |
|---|---|---|
| `instruction.md:1-6` | unenforced | `static-file-no-git` |
| `instruction.md:7` | partly | `wrong-port-8081`, `static-file-no-git` |
| `instruction.md:8` | partly | `not-found`, `catch-all-200` |
| `instruction.md:9` | enforced | `capitalised`, `leading-space` |

Line-by-line reading:

- **1–6 (a git server that a clone/commit/push reaches).** Nothing in the grader observes it.
  `verify.sh` installs `expect` but never checks that the clone, commit or push happened; the graded
  state can be a plain file in a directory with no repository, no hook and no push. Case
  `static-file-no-git` serves such a file and is observed **pass**.
- **7 (that data is pushed to a web server on port 8080).** The port half is enforced — a server on
  8081 only makes the first request return `000` (`wrong-port-8081`, observed fail). The push half is
  not: the same passing case above shows data on 8080 that no push ever produced.
- **8 (`curl http://server:8080/hello.html`).** Only one path on `localhost` is ever requested, and a
  404 there fails (`not-found`). But the request is never varied: a server answering **every** path
  with `hello world` also passes (`catch-all-200`), and the hostname in the instruction is never used.
- **9 (the output is `hello world`).** Strictly enforced by the shell string comparison: capitalised
  and leading-space bodies both fail (`capitalised`, `leading-space`), as do a trailing space, a `\r`,
  a BOM and an empty body.

## The executed probe

Frozen instrument `plans/git_webserver_probe.py` (sha256 `63cb75cf…5eedf`), 22 cases, one bubblewrap
sandbox per case: private network namespace (so `:8080` is the case's own loopback, never the host's),
`HOME` and `/tmp` inside scratch, `/tests` bound read-only to the captures, `PATH` holding only the
tools the case names. `apt-get` and `expect` are absent in **every** case, so the install step and the
git step fail exactly as they would in a container that lacks them — and nothing in `verify.sh` reads
their status. The captured test function is imported and called directly; `AssertionError` is `fail`,
a return is `pass`.

Receipt summary, verbatim:

`cases=22 observed_pass=9 observed_fail=13 mismatches=0`

What each group shows (each line is one receipt case):

| Group | Cases | Observed | What it demonstrates |
|---|---|---|---|
| no service at all | `no-server`, `wrong-port-8081` | fail, fail | the first request's status gates everything; `000` and a server on the wrong port are both non-200 |
| service without any git | `static-file-no-git` | **pass** | the graded state need not come from a repository, a hook or a push |
| any path, same body | `catch-all-200` | **pass** | only `/hello.html` is requested; a server answering every path passes |
| body normalisation | `exact-no-newline`, `trailing-newlines` | pass, pass | command substitution makes trailing newlines irrelevant |
| body strictness | `capitalised`, `leading-space`, `trailing-space`, `crlf`, `bom`, `empty-200` | fail ×6 | case, any leading whitespace, a trailing space, CR, BOM and an empty body are all literal mismatches |
| status handling | `not-found`, `http-500-right-body`, `redirect-301`, `first-request-404` | fail ×4 | the status must be exactly `200`; `curl` has no `-L`; the **first** request decides whether the body is fetched |
| timing | `slow-server-3s` | **pass** | `curl` is invoked without a timeout, so a 3 s answer still counts |
| substring verdict | `token-in-body` | **pass** | `TEST PASSED` in the served body passes while the helper prints `❌ TEST FAILED` |
| two-request split | `status-then-content-split` | **pass** | the first response's body (`not the content`) is never compared; the second supplies `hello world` |
| wget branch | `wget-static-file`, `wget-404`, `wget-token-in-body` | pass, fail, **pass** | with `curl` off `PATH`, `wget`'s exit status gates the same comparison, and the body echo carries the token there too |

The two headline findings, each bounded to this capture:

1. **A file served on :8080 with no git repository, hook or push passes.** `verify.sh` runs the expect
   script and never reads its status; the only things that can fail the grader are the HTTP status of
   the first request and the body of the second. The instruction's first six lines are decoration for
   this grader.
2. **A body that merely contains `TEST PASSED` passes even though the helper prints `TEST FAILED`.**
   `test_outputs.py:13` searches stdout for a substring that `verify.sh:62` echoes from the response
   body, so the failure message itself carries the token (`Content: TEST PASSED` precedes
   `❌ TEST FAILED: Content does not match expected output` in the receipt's stdout line). The verdict
   channel and the diagnostic channel are the same channel.

Both hold on the `wget` branch as well (`wget-token-in-body`), so they are properties of the two-file
grader, not of `curl`.

## What the probe does not show

- **The oracle is never run.** `solution/solve.sh` needs root, `apt`, `nginx` and `sshd`; the probe
  shows what the verdict depends on, never that the intended path passes. Its content is read only for
  orientation: it installs `git nginx openssh-server`, creates a `git` user with password `password`,
  makes a bare repo at `/git/server`, installs a `post-receive` hook that checks out into
  `/var/www/html`, and configures nginx to listen on 8080.
- **No real git push, clone or ssh.** `expect` (and `git`) are absent from every case's `PATH`, so the
  git step always fails; the probe cannot show that a push lands, nor how a push failure interacts
  with the rest of the script beyond "the status is ignored".
- **`test.sh` was not executed.** The reward mapping is read (`test.sh:14-25`), not run: the probe
  calls the test function itself. Network installs (`uv`, `curl`) and `/logs/verifier/` are outside the
  sandbox.
- **No harness, image or model.** Nothing here is a run of Terminal-Bench, of
  `alexgshaw/configure-git-webserver:20251031`, or of any agent; the 900 s verifier timeout is
  declared in `task.toml`, not exercised.
- **The 22 cases are the claim's whole surface.** They were fixed before the first run; states outside
  them (chunked transfer, HTTP/1.1 keep-alive, a body with an embedded newline that command
  substitution keeps, TLS, IPv6 `localhost`, a server that answers the first request 200 and closes)
  are not covered and are not claimed.

## Negative space

This entry does **not** establish: that the task is valid, well-calibrated or appropriately difficult
(no run of the image, no model, no trajectory — that is PROVINCE's question, not this lane's); that
`TEST PASSED` is the *right* assertion (it is the authors' choice, and its weakness is described, not
judged); anything about how Harbor executes this verifier (`benchmark-verifier-execution-model.md`
covers where it runs and what it restores); that `verify.sh` is the only file the harness runs (the
capture at this commit holds one test function, but a run may add files the capture does not show);
any agent behaviour, pass rate or failure mode; or anything about the other TB2 tasks.

**Falsifier:** this entry is falsified if (a) a re-fetch of the three pinned URLs yields bytes whose
SHA-256 differs from `corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`; (b) a fresh run of
`plans/git_webserver_probe.py --lane .` prints anything other than
`cases=22 observed_pass=9 observed_fail=13 mismatches=0` — in particular if `static-file-no-git`,
`token-in-body`, `status-then-content-split` or `catch-all-200` is observed `fail`, or `not-found` or
`capitalised` is observed `pass`; (c) the captured grader applied to a body containing only the text
`TEST PASSED` raises `AssertionError`; or (d) a line of `verify.sh` between 34 and 49 is shown to
consult the git step's exit status, or `test_outputs.py:13` is shown to read something other than
`result.stdout` (for example a line-anchored match or `returncode`).

## Located quotes

Quotes are byte-exact from the round-37 captures (`corpus/evidence/round37/tb2-git-webserver/`,
identical to the pinned raw files at `2fd12b88`), each 3–25 words, verified line by line with
`sed -n '<n>p'`.

| Claim supported | “Quote” | `file:line` |
|---|---|---|
| the captured file is a harness template with one test | “by the test harness to evaluate the final state of the terminal” | `test_outputs.py:4` |
| the graders' own statement of the assertion | “Test that the hello.html file exists and contains the correct content.” | `test_outputs.py:10` |
| the helper is invoked as a subprocess | “result = subprocess.run(["bash", "/tests/verify.sh"], capture_output=True, text=True)” | `test_outputs.py:11` |
| the decision is a stdout substring | “assert "TEST PASSED" in result.stdout, "Did not pass test"” | `test_outputs.py:13` |
| the install comment names curl | “# Install curl for testing” | `verify.sh:4` |
| the install line names expect instead | “DEBIAN_FRONTEND=noninteractive apt-get install -y expect” | `verify.sh:6` |
| the clone the helper attempts | “spawn git clone git@localhost:/git/server server-test” | `verify.sh:21` |
| the commit the helper attempts | “cd server-test && echo 'hello world' > hello.html && git add hello.html” | `verify.sh:34` |
| the git step is run without its status read | “Run the expect script” | `verify.sh:48` |
| the helper announces itself before probing | “echo "Testing web server..."” | `verify.sh:52` |
| a fixed sleep stands in for a readiness check | “sleep 2 # Give some time for nginx to process” | `verify.sh:53` |
| the first request fetches status only | “HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/hello.html)” | `verify.sh:57` |
| the status must be exactly 200 | “if [ "$HTTP_RESPONSE" = "200" ]; then” | `verify.sh:59` |
| the second request fetches the body | “CONTENT=$(curl -s http://localhost:8080/hello.html)” | `verify.sh:60` |
| the body is echoed into the graded stdout | “echo "Content: $CONTENT"” | `verify.sh:62` |
| the content comparison is a shell string equality | “if [ "$CONTENT" = "hello world" ]; then” | `verify.sh:63` |
| the failure message is printed into the same stdout | “echo "❌ TEST FAILED: Content does not match expected output"” | `verify.sh:66` |
| a non-200 status is its own failure message | “echo "❌ TEST FAILED: Web server returned HTTP $HTTP_RESPONSE"” | `verify.sh:71` |
| the wget branch fetches the same path | “wget -q -O test_output.html http://localhost:8080/hello.html” | `verify.sh:75` |
| wget's exit status gates the content branch | “if [ $? -eq 0 ]; then” | `verify.sh:76` |
| the wget branch's failure message | “echo "❌ TEST FAILED: Web server could not be reached"” | `verify.sh:88` |
| the test file is run under uvx pytest | “pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA” | `test.sh:18` |
| the reward is 1 on pytest success | “echo 1 > /logs/verifier/reward.txt” | `test.sh:22` |
| the reward is 0 on pytest failure | “echo 0 > /logs/verifier/reward.txt” | `test.sh:24` |
| the authors' description of the task | “automatic deployment to an nginx web server using post-receive hooks.” | `task.toml:6` |
| the oracle's post-receive hook step | “# Step 6: Create a post-receive hook to deploy code to web server” | `solve.sh:33` |
| the oracle's hook checks out into the web root | “GIT_WORK_TREE=$WEBROOT git checkout -f” | `solve.sh:37` |
| the served output the instruction asks for | “then I see the output "hello world".” | `instruction.md:9` |
| the request's first line | “Configure a git server so that I can run on my computer” | `instruction.md:1` |
| the push the instruction asks for | “git push origin master” | `instruction.md:6` |
| the 8080 requirement | “And have this data then be pushed to a webserver running on port 8080 so if I run” | `instruction.md:7` |
| login is out of scope for the agent | “I'll setup login with the server to work, you don't have to worry about that.” | `instruction.md:10` |
