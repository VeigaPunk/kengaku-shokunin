# R37CritScope drop-ins (round 37, C2) — copy-paste text for the L1

Every block below is new text only; nothing here edits a frozen file. Locations name the draft
(`.ufo/waves/round-37/build/R37PkgDraft/entry.md`) or the lane file the L1 will draft into.
Fix numbers match `R37CritScope.md` §3. Do not apply while any frozen byte changes.

---

## F1 — entry :34–40, class claim (replace the whole paragraph)

```markdown
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
```

## F2 — entry :27–32 (replace the "Six of the nine …" passage)

```markdown
Five of the nine passing cases are states in which no assertion in the capture observes the stated
request: a static file served with no repository, hook or push passes on both tool branches
(`static-file-no-git`, `wget-static-file`); a body whose only content is the token `TEST PASSED`
passes while the helper prints `TEST FAILED` (`token-in-body`, `wget-token-in-body`); and a verdict
assembled from two requests passes although the first response's body is never compared
(`status-then-content-split`). One more passes because the request path is never varied
(`catch-all-200`), one because `curl` runs without a timeout (`slow-server-3s`), and two are
exact-content controls (`exact-no-newline`, `trailing-newlines`).
```

## F3 — entry :11–16 (two sentence replacements)

Replace `the task's whole score is one pytest function` with `in this capture the whole score is one
pytest function`; then replace the "graded artefact" sentence with:

```markdown
The state the verdict is computed from is, as this capture shows it, two HTTP responses from a
service on `:8080`; the git server the instruction asks for is touched only by a helper step whose
exit status no line of the helper reads.
```

## F4 — entry :106 and :145 (observation, not judgement)

- :106 `Nothing in the grader observes it.` → `No line of either captured file reads the clone, commit or push status, and no assertion observes any of the three.`
- :145 `The instruction's first six lines are decoration for this grader.` → `No assertion in this capture observes any of the instruction's first six lines.`

## F5 — entry :116–119 (environment of observation)

```markdown
`apt-get` and `expect` are absent in **every** case by construction: `PATH` is `/work/bin` (only the
named tools), `/usr` is read-only, `expect` is bound to `/dev/null` when the host has it, and the
network namespace is private. The install step and the git step therefore fail with `command not
found` before the grader's verdict is computed — and nothing in `verify.sh` reads their status.
This is one reachable environment, not the task image's: `task.toml:34` declares
`allow_internet = true` and `task.toml:29` names the image, and no case here exercises either.
```

## F6 — README §Frontier, new sub-bullet after the round-36 sub-bullet

```markdown
  - *Partly discharged round 37 (2026-10-26):* `knowledge/tb2-git-webserver-grader.md` reads and
    executes a third Terminal-Bench 2.0 task's scoring code (`configure-git-webserver/tests/test_outputs.py`
    + `tests/verify.sh` @ `2fd12b88`) against its `instruction.md`. The "Terminal-Bench 2.0's" clause
    is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (3 of 89
    read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity
    (which `PROVINCE.md` refuses to this lane).
```

## F7 — entry Negative space, appended refusals

```markdown
… nor **gameability or solver strategy**: that a state in these 22 cases passes says nothing about
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
```

## F8 — entry :2 and :46 (provenance scope)

- :2 `lines 1–91` → `lines 1–92` (the capture has 92 lines; `echo "Test completed"` is `verify.sh:92`).
- :46 `read only for the task description and the verifier timeout` → `read only for the task description, the declared timeouts (`:22`, `:25`), the declared image name (`:29`) and the declared internet policy (`:34`)`.

## F9 — README coverage map, new row after the `(second task)` row

```markdown
- **Terminal-Bench 2.0 task grader (third task, one new executed edge class)**: covered at
  source-code depth and executed offline (round 37, 2026-10-26) — knowledge/tb2-git-webserver-grader.md;
  S111, S112, S113; probe `plans/git_webserver_probe.py`, receipt `evidence/round37/git-webserver-probe.txt`.
  A third instance of the same ground (3 of the 89 TB2 task graders; not breadth, and no quality,
  validity, difficulty or gameability verdict), on `configure-git-webserver` only: in this capture its
  whole score is one pytest function asserting that a helper script's stdout contains `TEST PASSED`;
  the helper's clone/commit/push step is run and its status never read; the content check is a shell
  equality after command substitution over a second request; and the body is echoed into the graded
  stdout. One new edge class in the executed sample: the graded state is a live HTTP service.
  Not the remaining 86 TB2 tasks, not task validity, difficulty or quality, not the image or a
  harness run, not contamination, not agent behaviour.
```

## F10 — PROVINCE, new paragraph after the round-36 paragraph

```markdown
## Round37 partial frontier admission (2026-10-26)

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader —
`configure-git-webserver/tests/test_outputs.py` and its helper `tests/verify.sh` at terminal-bench-2
`2fd12b88` — over 22 frozen synthetic service states, via `corpus/knowledge/tb2-git-webserver-grader.md`
(S111–S113), `plans/git_webserver_probe.py` and receipt `corpus/evidence/round37/git-webserver-probe.txt`
(`cases=22 observed_pass=9 observed_fail=13 mismatches=0`). Each case runs the captured test function and
helper in a per-case bubblewrap sandbox: private network namespace, no root, scratch `HOME` and `/tmp`,
`/tests` read-only, `PATH` scoped to the named tools. The graded state is two HTTP responses from a
service the probe starts. It records how that captured grader answers those synthetic states only: it
does not run Terminal-Bench, the task image or a harness, or a real submission; it does not validate or
certify a task, measure difficulty or gameability, judge the assertion's correctness, measure
contamination, or speak for the remaining 86 TB2 task graders (89 carry `tests/test.sh`; 3 are read).
Any observation from a real-image run is a separate, routed observation and is not part of this
admission. Adjacent: web properties (kake), serving plane (kama), deployment configuration and runtime
task validity (refused). The round35/36 paragraphs above stay as written; this paragraph narrows only
their "other TB2 tasks" clause for this one task.
```

## F11 — SCORECARD, the C2 coverage cell (and optional capability row)

Coverage cell text:

```markdown
coverage (lowest, tied; **7 held** by the L0 cap) — `coverage/surfaces`: one §Frontier sub-bullet
narrowed for one task, one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows
43→44, SOURCES 103→106; `coverage/constructs`: **unchanged** — the executed-sample class sentence is a
property of this capture's evidence, not a construct claim. Command that would show the surface
unmoved: `python3 plans/round37_c2_verify.py --lane .` at freeze prints `checks=7 defects=4` (entry and
rows absent), and the round-28/31 entries already hold the static precedents. No score move claimed.
```

Optional capability row (first working round 37):

```markdown
| service-grader-probe | Execute a captured grader's helper script offline in a per-case unprivileged sandbox and count observed verdicts against a frozen case table; captures and helper bound read-only, `PATH` scoped, no network. Not task certification, not runtime inside the task image, not a reward measurement. | `python3 plans/git_webserver_probe.py --lane .` (summary line, not `$?`); `python3 plans/round37_c2_verify.py --lane .` V1–V7 | 37 |
```

## F12 — SKILL draft Part C (rewrite the recipe framing)

Replace `the helper probes a live service whose state the agent chooses` with `the helper probes a
live service the probe starts; the capture does not show what state the task's run leaves`.

Rename the table column `probe it with` → `what the frozen run tested`, and replace each imperative
cell with a past-tense observation:

| old cell | new cell |
|---|---|
| `serve the verdict token as the response body` | `a body equal to the verdict token was served` |
| `delete the tool a required step needs and see whether the verdict moves` | `a case ran with the required tool absent from PATH` |
| `answer the status request 200 and the content request with the wrong body` | `the status request was answered 200; the content request supplied the body` |
| `a catch-all server answering /hello.html and everything else` | `a server answered every path with the same body` |
| `move the server to :8081 and leave 8080 empty` | `the server listened on :8081 and 8080 was empty` |

Replace `What a green means here: the agent served /hello.html on :8080 with a body equal to hello
world after command substitution, at the moment of two separate requests.` with:

```markdown
What a green means here: in the probe's state, the service answered two requests and the content
body equalled `hello world` after command substitution.
```

Append the bounds line:

```markdown
A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict,
not solver advice, and not a statement about any agent's behaviour.
```

## F13 — no absorption of the real-image run (`R37DockerOracle.md`)

Do not cite `build/R37DockerOracle.md`, its `reward.txt = 1` lines, its B/B2/C/C2 "cheat" runs, or
its `NOT TEST PASSED` observation in the entry, SKILL.md, README or PROVINCE. Keep it in the round
report as a routed observation with its own limits (single observation per scenario, apt-mutated
containers, `/tests` copied rather than harness-bound, `/logs/verifier` created by hand, `--cpus 1`
not enforced, image removed). If the L1 wants any of it inside the lane's admitted scope, it needs
(a) its own PROVINCE paragraph naming a real-image observation as a new surface, (b) a post-hoc
section in the entry labelled outside the frozen 22 cases, and (c) no reward, gameability, oracle-
passes or task-validity claim. Without all three it crosses the round-35/36 admission.
