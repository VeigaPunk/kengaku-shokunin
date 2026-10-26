source: S111 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py — the one test function, lines 1–13, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S112 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/verify.sh — the helper shell script the test calls, lines 1–92, same commit, accessed 2026-10-26
source: S113 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/instruction.md — the request, lines 1–10, same commit, accessed 2026-10-26
source: S114 — https://github.com/harbor-framework/terminal-bench-2-1/issues/133 — prior report on the TB2.1 version of this task's verifier, issue body line 39, opened 2026-07-14, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — re-fetch the three pinned URLs, run `sha256sum -c corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`, and re-run `plans/git_webserver_probe.py --lane .`; any digest or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `configure-git-webserver`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `configure-git-webserver` task's whole score in this capture is one pytest
function, `test_hello_html_exists`, which shells out to `bash /tests/verify.sh` and asserts that the
script's **stdout contains the substring `TEST PASSED`**. `tests/test.sh` maps the pytest exit status
to a binary reward. The state the verdict is computed from is, as this capture shows it, two HTTP responses from a
service on `:8080`; the git server the instruction asks for is touched only by a helper step whose
exit status no line of the helper reads. Two mechanisms do the real deciding: a shell string comparison of the fetched body after
command substitution, and a Python substring search over everything the helper printed, including an
echo of that body.

Offline execution of the captured grader inside a bubblewrap sandbox over 22 frozen cases
(`plans/git_webserver_probe.py`; receipt `corpus/evidence/round37/git-webserver-probe.txt`) reproduced
every prediction written from the static reading before the first run:

`cases=22 observed_pass=9 observed_fail=13 mismatches=0`

Five of the nine passing cases are states in which no assertion in the capture observes the stated
request: a static file served with no repository, hook or push passes on both tool branches
(`static-file-no-git`, `wget-static-file`); a body whose only content is the token `TEST PASSED`
passes while the helper prints `TEST FAILED` (`token-in-body`, `wget-token-in-body`); and a verdict
assembled from two requests passes although the first response's body is never compared
(`status-then-content-split`). One more passes because the request path is never varied
(`catch-all-200`), one because `curl` runs without a timeout (`slow-server-3s`), and two are
exact-content controls (`exact-no-newline`, `trailing-newlines`).

This entry extends `knowledge/benchmark-verifier-execution-model.md` (where a TB2 verifier runs; S100
is the same repository at the same commit), `knowledge/benchmark-grader-semantics.md` (one Toolathlon
grader read) and `knowledge/tb2-regex-log-grader.md` (round 36's TB2 task read the same way), and
records one new edge class in the lane's **executed** grader sample: the graded state is two HTTP
responses from a service the probe starts, read by a captured helper the grader runs end-to-end. It
is not a new verdict channel and not a new reading: round 28 read WebArena's
`StringEvaluator`/`URL`/`HTML` predicates over page state statically
(`knowledge/webarena-task-spec-audit.md:6,41`), and round 31 executed SWE-bench Pro V2's log-scan
path ("The *passed* side is not a test-runner verdict but a log scan",
`knowledge/benchmark-verifier-execution-model.md:104-112`). What is new in execution is the object —
a live-service state — not the substring. The instrument is the same frozen probe shape as rounds
35–36, so the class difference is a property of this capture's evidence and not a construct claim (no
prior-art novelty claim is made this round). It **narrows**, for this one task only, the
`corpus/README.md` §Frontier clause that left "the other TB2 tasks" open; the clause stays open for
the remaining TB2 task graders (89 tasks carry `tests/test.sh` at `2fd12b88`; 3 are now read).

## Source labels

S111–S113 are the benchmark maintainers' own task files: primary for *what this grader checks* and for
the requirement text it is mapped against, and a self-report for everything else. `task.toml` (captured,
not a registry row) is the authors' own metadata and is read only for the task description, the declared
timeouts (`:22`, `:25`), the declared image name (`:29`) and the declared internet policy (`:34`). The captured `solution/solve.sh` oracle is **own reading, tier C** — it is not a
registry row, was not executed, and nothing below rests on it. The probe receipt is the lane's own
re-runnable gate output (tier A for its own scope: these 22 states against these captures under the
host's Python and `bash`, in a private network namespace).

Disclosure: the probe predictions were written from a static reading of `verify.sh`,
`test_outputs.py` and `instruction.md` **before the first run**, and the frozen case table
(`corpus/evidence/round37/git-webserver-dry-cases-freeze.txt`) carries them; the second run's receipt
was byte-equal to the first. No prediction mismatched, so this entry reports no re-prediction. One earlier execution exists and is
disclosed in `plans/round-37-claims.md:3-10`: the C2 skip-control's gate clause P10 ran the frozen probe once
inside a scratch clone at control time and discarded its output unread; the probe was already at its
frozen digest.

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

- **1–6 (a git server that a clone/commit/push reaches).** No line of either captured file reads the clone, commit or push status, and no assertion
  observes any of the three.
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
tools the case names. `apt-get` and `expect` are absent in **every** case by construction: `PATH` is `/work/bin` (only the
named tools), `/usr` is read-only, `expect` is bound to `/dev/null` when the host has it, and the
network namespace is private. The install step and the git step therefore fail with `command not
found` before the grader's verdict is computed — and nothing in `verify.sh` reads their status.
This is one reachable environment, not the task image's: `task.toml:34` declares
`allow_internet = true` and `task.toml:29` names the image, and no case here exercises either.
The captured test function is imported and called directly; `AssertionError` is `fail`,
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

1. **A file served on :8080 with no git repository, hook or push passes.** What the case shows is
   that a tree with a static file and no repository passes: the grader reads nothing from the
   filesystem and makes two HTTP requests, so the only things that can fail it are the HTTP status of
   the first request and the body of the second. That `verify.sh:49` ignores the status of an expect
   step that *ran and failed* is a static reading here, not an observation: in the sandbox the git
   step cannot execute at all (`apt-get` and `expect` absent, `git` off `PATH`), so the case cannot
   separate "the step's failure is ignored" from "the step never ran" (`R37CritCases` §2.1). No assertion in this capture observes any of the
   instruction's first six lines.
2. **A body that merely contains `TEST PASSED` passes even though the helper prints `TEST FAILED`.**
   `test_outputs.py:13` searches stdout for a substring that `verify.sh:62` echoes from the response
   body, so the failure message itself carries the token (`Content: TEST PASSED` precedes
   `❌ TEST FAILED: Content does not match expected output` in the receipt's stdout line). The verdict
   channel and the diagnostic channel are the same channel. `verify.sh:68` (`Got: '$CONTENT'`) echoes the
   same body in the same branch, so the case attributes the pass to `test_outputs.py:13` over *an* echo of
   the body, not to `:62` specifically.

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
- **Case independence (wave-1 critic `R37CritCases`, `.ufo/waves/round-37/build/R37CritCases.md`).**
  Three labels are weaker than they read: `static-file-no-git` (above); `wrong-port-8081` prints the same
  `HTTP 000` as `no-server`, because the grader never contacts `:8081`, so it shows that an empty `:8080`
  fails, not that a correct body elsewhere is rejected *as such*; the two token cases share the `:62`/`:68`
  (`:79`/`:85`) double echo. The critic predicted and ran four cases outside the frozen 22 through the same
  machinery (4/4 matched, post-hoc, not part of the receipt): a token on the second line of a multi-line
  body passes; `hello world` plus a second line fails; a content request answered `500` with the right body
  passes (only the first request's status is read); and a wrong body on `:8080` with the right body on
  `:8081` fails at the content comparison. These sharpen the map; none changes a frozen verdict.

## Prior art (S114)

The static-file weakness was reported upstream before this round. Terminal-Bench 2.1 issue #133, opened
2026-07-14 and open when accessed on 2026-10-26, says: “But the script has no `set -e` / explicit failure
check on the clone/push.” (`corpus/evidence/round37/prior-art/tb21-issue-133-body.md:39`, body captured with
`SHA256SUMS` beside it). It concerns the TB2.1 version of `verify.sh`, whose auth block differs from the
pinned TB2.0 file (`.ufo/waves/round-37/build/R37ScoutUpstream.md` §3), so `static-file-no-git` is a
replication on the pinned file, not a discovery. The wave-1 prior-art scout
(`.ufo/waves/round-37/build/R37ScoutPriorArt.md`) found the class — a verdict read from output that the
checked artefact can write — reported elsewhere, and no report of the `token-in-body` instance for this task.
No novelty claim is made.

## Negative space

This entry does **not** establish: that the task is valid, well-calibrated or appropriately difficult
(no run of the image, no model, no trajectory — that is PROVINCE's question, not this lane's); that
`TEST PASSED` is the *right* assertion (it is the authors' choice, and its weakness is described, not
judged); anything about how Harbor executes this verifier (`benchmark-verifier-execution-model.md`
covers where it runs and what it restores); that `verify.sh` is the only file the harness runs (the
capture at this commit holds one test function, but a run may add files the capture does not show);
any agent behaviour, pass rate or failure mode; or anything about the other TB2 tasks; nor **gameability or solver strategy**: that a state in these 22 cases passes says nothing about
whether an agent can reach it, would find it, or would be rewarded for it in a run, and this entry
offers no solving advice; nor **deployment or web-property guidance**: the oracle's nginx/git/ssh
configuration is the maintainers' own file summarized for orientation, not a configuration this lane
recommends, and the probe's service is a lane-owned `http.server` on a private loopback (kake owns
web properties; deployment configuration is outside this lane); nor **harness or toolchain
fidelity**: the probe runs host `bash`/`curl`/`wget`/Python, while `test.sh:14-25` runs the file under
`uvx -p 3.13` with `pytest==8.4.1` and `task.toml:34` declares `allow_internet = true` for the image;
nor **contamination**: `test_outputs.py:1-2` carries the canary banner and this capture exists for
digest-pinned re-execution, not as a contamination measurement; nor **anything from a run of the task
image**: no real-image observation is used anywhere in this entry.

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

## Errata (round 38)

Appended 2026-10-26 (round 38, wave 1). This file is append-only: the bytes above stand as filed, and this
section is the correction of record. Base: the file as landed in round 37 (sha256
`6e3f8c77139f64737bc64094f7c91a3e7f7598e1ebdce91cb0fd92eb4854812a`, git blob
`68263f2990e0543f8e2e1814307201a0c66f87f1`, read at lane tip `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`);
nothing above was edited. The corrections are adjudicated from two round-37 wave-2 falsifier seats and the
round-37 non-author closure's routed item D2 (`corpus/lessons/round-37-verifier-spotcheck.md` §5):
`F37CritC2Map` (per-row verdicts) and `F37CritC2Overclaim` (findings F1-F13), whose receipts are filed under
`.ufo/waves/round-37/falsify/F37CritC2Map/` and `…/F37CritC2Overclaim/`. No probe case was re-run for this
section, no case was added and the receipt is unchanged (`cases=22 observed_pass=9 observed_fail=13
mismatches=0`); every corrected row is restated from that one receipt.

**Scope.** Three requirement-map rows are corrected (the `:104-107` table and its `:111-124` prose): row 7
(qualifier only — label and cases stand), row 8 (cited witness replaced; label stands), row 9 (label
`enforced` → `partly`, cases extended). Row `1-6` (`:104`, `:111-115`) stands as filed: the Map seat re-tested
it against `static-file-no-git` and agreed. The thirteen prose overclaims the overclaim seat verified are
folded in §B; §C names what still holds, so this section is not read wider than it is.

### A. Corrected requirement map

Complete restatement; the `:102-107` table is superseded by this one and `enforced`/`unenforced`/`partly` keep
the definition at `:97-100`.

| Instruction line | Label | Receipt cases |
|---|---|---|
| `instruction.md:1-6` | unenforced | `static-file-no-git` |
| `instruction.md:7` | partly | `wrong-port-8081`, `static-file-no-git` |
| `instruction.md:8` | partly | `not-found`, `status-then-content-split` |
| `instruction.md:9` | partly | `capitalised`, `leading-space`, `token-in-body` |

Rows `1-6` and `7` are unchanged; `catch-all-200` is dropped from row 8 and `token-in-body` added to row 9
(§A.2, §A.3). Corroborating witnesses for row `1-6`, if a second is ever wanted: `catch-all-200`,
`token-in-body`, `status-then-content-split` — the Map seat's note on that row, not a defect.

#### A.1 Row 7 — the port half holds by construction (`:116-118` superseded)

The filed sentence (`:116-117`) reads "The port half is enforced — a server on 8081 only makes the first
request return `000`". That invites the reading that the grader compares ports; it does not. `verify.sh:57,60`
name `localhost:8080` literally, so no other port is ever contacted, and `wrong-port-8081` prints the same
line `no-server` prints (`❌ TEST FAILED: Web server returned HTTP 000`) — the case shows that `:8080` must
answer, not that a port is checked (F37CritC2Map row 7; F37CritC2Overclaim F2; the entry's own §Case
independence at `:200-203` already said so). Replacement:

> - **7 (that data is pushed to a web server on port 8080).** The port half holds by construction, not by
>   comparison: `verify.sh:57,60` request `localhost:8080` literally, so a state serving the right body on
>   8081 and nothing on 8080 fails (`wrong-port-8081`) with the same `Web server returned HTTP 000` line
>   `no-server` prints — the case shows that `:8080` must answer, not that a port is checked (see §Case
>   independence). The push half is not enforced: the passing case above serves data on 8080 that no clone,
>   commit or push produced (`static-file-no-git`).

Label `partly` and both cited cases stand. The port clause as such is isolated only by the post-hoc extra case
(a wrong body on `:8080`, the right body on `:8081`, fails at the content comparison), which is outside the
frozen 22.

#### A.2 Row 8 — the witness is `status-then-content-split`, not `catch-all-200` (`:106`, `:119-121` superseded)

`catch-all-200` answers `/hello.html` on `:8080` with `200 hello world` — line 8 satisfied exactly as
written (the instruction asks that the served output be `hello world`, `instruction.md:8-9`). A catch-all
server violates only an inferred routing-specificity requirement the line does not state, so it is not a
violating pass and must not be cited as one (F37CritC2Map row 8). The receipt holds a genuine one:
`status-then-content-split` answers the instruction's own request with `not the content` first and
`hello world` second and is observed pass, because `verify.sh:57` discards the first body (`-o /dev/null`)
and `:60` fetches again. Replacement:

> - **8 (`curl http://server:8080/hello.html`).** One path on `localhost` is requested and a 404 there fails
>   (`not-found`), but the body that request returns is never the body compared: `verify.sh:57` discards it
>   and `:60` fetches again, so a server answering `not the content` first and `hello world` second passes
>   (`status-then-content-split`). The hostname `server` is never used (`localhost` is hardcoded at
>   `:57,60`). A server answering every path passes (`catch-all-200`), which satisfies the line as written;
>   routing beyond `/hello.html` is not a clause of the line and is not this row's evidence.

Label `partly` stands: `not-found` is a violating fail, `status-then-content-split` a violating pass.

#### A.3 Row 9 — `partly`, not `enforced` (`:107`, `:122-124` superseded)

This is the landing defect and the round-37 discernment disagreement (closure §3). Under the map's own
definition at `:97-98`, `enforced` requires that a violating case be observed `fail`; `token-in-body` serves
exactly `TEST PASSED`, is observed **pass**, and sits in the same receipt the rows claim to read labels off
(receipt line 35; `wget-token-in-body` passes the same way). The filed row contradicts the entry's own
headline 2 at `:169-171`. Replacement:

> | `instruction.md:9` | partly | `capitalised`, `leading-space`, `token-in-body` |
>
> - **9 (the output is `hello world`).** Confirmed for every body that does not carry the verdict token:
>   `capitalised`, `leading-space`, `trailing-space`, `crlf`, `bom` and `empty-200` fail (`verify.sh:63`),
>   and `trailing-newlines` passes because command substitution strips newlines. Free once the body carries
>   `TEST PASSED`: `token-in-body` serves exactly that string, the helper prints `❌ TEST FAILED: Content does
>   not match expected output` with `Got: 'TEST PASSED'`, and the case is observed **pass** — the same on the
>   wget branch (`wget-token-in-body`).

Secondary fix in the same row: the `:122-124` prose names `trailing-space`, `crlf`, `bom`, `empty-200` and
`trailing-newlines` while the Receipt-cases cell named only two cases, so none of those claims was
machine-checked (F37CritC2Map, row-9 note). The restatement keeps them in prose and the cell lists only cases
a derived check can use — `trailing-newlines` is an exact-content control and does not violate the line.

#### A.4 Why the frozen round-37 V7 stayed green, and what now reddens on these rows

`plans/round37_c2_verify.py:192-201` reads the verdicts of the cases a row **cites** and asks only for the
cited direction (`enforced` needs one failing cited case; `partly` needs one of each). Rows `:106` and `:107`
each cited cases that satisfy that direction, so V7 printed `V7 ok rows=4 bad=0` and `PREDICATE C2 pass`:
the green predicate and the wrong map coexist (falsifier receipt
`.ufo/waves/round-37/falsify/F37CritC2Map/c2-verify-run.txt`, sha256 `d0a608ca90e1…8032fc934`). Round 38's
counter closes that hole — `plans/round38_c2_verify.py:239-248` derives the label from **every** receipt case
whose `violates=` set carries the tag (`enforced` iff all fail, `unenforced` iff all pass, `partly` otherwise)
and rejects any cited id that is not one of them; the criterion is `corpus/QUALITY.md` Q28. On row 9 the
derivation is `partly` (violating: `capitalised` fail, `token-in-body` pass), so the row fails the label leg
on its own receipt; on row 8 the derivation is also `partly` but `catch-all-200` is not in the violating set,
so the row fails the citation leg.

**Limit on that claim.** The round-37 receipt carries no `violates=` tags
(`grep -c violates= corpus/evidence/round37/git-webserver-probe.txt` → `0`; the dry table → `0`) and its rows
use a three-cell layout the round-38 four-cell parser does not accept, so the derived rule cannot be
*machine*-run on this entry: this section is hand-adjudicated from the two seats' receipts, and rows `1-6`
and `7` are not re-derived by it. Retro-fitting tags to a frozen receipt would be a new claim, not a
correction.

### B. Prose overclaims folded in (F37CritC2Overclaim F1-F13, plus the Map seat's notes)

All thirteen findings the overclaim seat verified are folded; F1 and F2 are the map rows corrected in §A.3 and
§A.1. Anchors are the filed bytes (this section does not edit them; the "correction now of record" column is
the text of record from here on). One anchor is corrected by this seat: F5's sentence is at `:162-163`, not
`:167-168` (that is the case-independence caveat).

| F | Entry anchor | What the filed bytes say | Correction now of record |
|---|---|---|---|
| F1 | `:107`, `:122` | `instruction.md:9 \| enforced`; "Strictly enforced by the shell string comparison" | label `partly` — §A.3; the shell comparison is exact only for the body it compares, while the verdict is a stdout substring, so a non-`hello world` body passes |
| F2 | `:116-117` | "The port half is enforced — a server on 8081 only makes the first request return" | by-construction qualifier — §A.1 |
| F3 | `:33`, `:154` | "one because `curl` runs without a timeout (`slow-server-3s`)" | a ≥3 s answer still counts (`slow-server-3s`); `verify.sh:57,60` pass no `--max-time` (static). Three seconds cannot separate "no timeout" from "any timeout > 3 s" (`.ufo/waves/round-37/build/R37CritCases.md:124`) |
| F4 | `:133-134` | "The install step and the git step therefore fail with `command not found`" | the install step fails `command not found`; the git step fails on the absent `expect` interpreter (`./git_test.exp: /usr/bin/expect: bad interpreter: No such file or directory`) — falsifier receipt `diag-verify-stderr.txt`, sha256 `8e801b0a59a9…be3d2de4`. Conclusion unchanged: neither status is read |
| F5 | `:162-163` | "the grader reads nothing from the filesystem and makes two HTTP requests" | it inspects no repository or solution file — only its own scratch files (`~/.ssh/config` at `verify.sh:9-13`, `git_test.exp` at `:16`, `test_output.html` at `:75-77`) — and reaches the service over HTTP; a state fails when the first request is non-200 or the helper's stdout lacks the token (see F1) |
| F6 | `:15-16`, `:39-40` | "two HTTP responses from a service on `:8080`" | one or two HTTP requests per case: curl issues a status request then a body request (`verify.sh:57,60`), wget issues one and reads a local file (`:75-77`) |
| F7 | `:196` vs `:204-205` | "The 22 cases are the claim's whole surface" beside "The critic predicted and ran four cases outside the frozen 22" | not covered by the frozen receipt and not claimed as receipt results; the four post-hoc states are recorded in the §Case independence bullet (`:204-208`), outside the receipt |
| F8 | `:58`, `:222-224` | "was not executed, and nothing below rests on it" | not executed **by the probe**; this entry uses no execution of it — the round's one image run is routed (`corpus/lessons/round-37.md:27`), and §Negative space's "no run of the image" is scoped the same way |
| F9 | `:41-43` | cites `knowledge/webarena-task-spec-audit.md:6,41` for the predicates | that file's `:6` is its H1; `StringEvaluator` is in the `source:` line `:1`, the `URL` row `:40`, the page-content row `:41` — cite `:1,40-41` |
| F10 | `:171` | "so the failure message itself carries the token" | the helper's **failing output** carries the token, via `verify.sh:62` (`Content: $CONTENT`) and `:68` (`Got: '$CONTENT'`); the failure message at `:66` contains none |
| F11 | `:130` | "`HOME` and `/tmp` inside scratch" | `HOME` in the scratch work dir (`plans/git_webserver_probe.py:235`) and a private `/tmp` tmpfs (`:209`) |
| F12 | `:66-67` | "and discarded its output unread" | discarded without a verdict being printed or read (the gate had compared it) |
| F13 | `:62-63` | "a static reading of `verify.sh`, `test_outputs.py` and `instruction.md`" | the pre-run reading also included the captured oracle (`plans/round-37-claims.md:74-75`) |

Map-seat notes not carried as defects: row `1-6` agreed, and `static-file-no-git` cannot separate "the helper
ignores the git step's status" from "the step never ran" (already stated at `:166-167`); rows 7 and 8 carried
the right labels — only the wording and one witness moved.

### C. What this erratum does not change

The overclaim seat checked the rest of the file and found no defect, so nothing else is corrected here: 32/32
located quotes byte-exact at their cited lines and 3-25 words (`quotes-check.txt`, sha256
`1e9f62011880…ef44251`); the receipt arithmetic, the dry table's predictions, the probe digest
`63cb75cf…5eedf` and the six captures' digests equal to `SHA256SUMS`; the case-independence bullet, headline
1's caveat, the S114 prior-art paragraph and its line-39 quote, the "89 tasks carry `tests/test.sh`" count and
the S100 identity all hold. The receipt, the case table, the digests and the **Falsifier** block at `:242-250`
are untouched: a fresh probe run must still print `cases=22 observed_pass=9 observed_fail=13 mismatches=0`,
and the falsifier's conditions stand as filed. This section moves no verdict and adds no case.

## Errata (round 39)

Appended 2026-10-26 (round 39, wave 1, seat `R39RecheckFix`; round-38 closure R4). Append-only: the bytes above
stand as filed; this section is the correction of record. Measured in a clean clone of the lane at `75047384`
(`git status --porcelain --untracked-files=all | wc -l` → `0`), run from its root.

**Erratum (round 39): the `recheck:` line reds as written.** `corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`
lists bare basenames, so `sha256sum -c` resolves them against the CWD: the `recheck:` command printed
`instruction.md: FAILED open or read` (and the same for `solve.sh`, `task.toml`, `test.sh`, `test_outputs.py`,
`verify.sh`) plus `sha256sum: WARNING: 6 listed file(s) could not be read`, exit 1. Corrected leg:
`(cd corpus/evidence/round37/tb2-git-webserver && sha256sum -c SHA256SUMS)` → 6/6 `OK`, exit 0. The probe leg is
sound as written (`plans/git_webserver_probe.py --lane .`, exit 0).

**Corrected `recheck:` line (replaces `:6`, one line):**

    recheck: 180d — at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`: re-fetch the three pinned URLs, `(cd corpus/evidence/round37/tb2-git-webserver && sha256sum -c SHA256SUMS)`, and re-run `python3 plans/git_webserver_probe.py --lane .`; the full one-liner is under `## Errata (round 39)`; any digest or receipt change supersedes this entry

**Full recheck one-liner (lane root, bash; verified exit 0 on 2026-10-26):**

    T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver && for p in tests/test_outputs.py tests/verify.sh instruction.md; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|verify\.sh|instruction\.md)$' corpus/evidence/round37/tb2-git-webserver/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round37/tb2-git-webserver && sha256sum -c SHA256SUMS) && mkdir -p "$T/w" && python3 plans/git_webserver_probe.py --lane . --work "$T/w" && rm -rf "$T"

Green: 3/3 refetched `OK`, 6/6 capture `OK`, `cases=22 observed_pass=9 observed_fail=13 mismatches=0`, byte-equal
to `corpus/evidence/round37/git-webserver-probe.txt`. `--work` must be an existing directory (a missing one raises
`FileNotFoundError`); omitting `--work` also works.
