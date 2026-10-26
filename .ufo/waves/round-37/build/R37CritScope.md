# R37CritScope — C2 scope, axis and wording (round 37, wave 1, 2026-10-26)

Seat: `R37CritScope` (critic, leaf). Lane `kengaku-shokunin` at `a3163e6` (frozen baseline `3ea9a1d9`
is an ancestor; wave-1 battery commit `a3163e6` landed while this seat read). C2's entry exists only
as the draft `build/R37PkgDraft/entry.md` (236 lines); `test -e corpus/knowledge/tb2-git-webserver-grader.md`
→ no, `grep -c '^ *| *S111 *|' corpus/SOURCES.md` → 0. Reports only: no lane file edited, no counter
run for scoring, no commit, no clone, no scratch dir created
(`/fast/scratch/hyaku/kengaku-r37/R37CritScope` absent — every read was path-scoped, no git index
touch). Drafts read: `build/R37PkgDraft/entry.md`, `build/R37SkillDraft/SKILL-r37-draft.md`,
`build/R37DockerOracle.md`, `build/R37IndepVerdicts.md`, `plans/round-37-claims.md`,
`corpus/knowledge/tb2-{protein-assembly,regex-log}-grader.md`, `corpus/README.md`, `PROVINCE.md`,
`SCORECARD.md`, `scripts/hyaku/lane-addendum.md` §9, the captures and the receipt.

**Answer in one line:** the *frozen* C2 — a bubblewrap-sandboxed execution of the captured grader over
22 synthetic states — is **inside** the lane's province and can carry `coverage` only as
`coverage/surfaces` (one §Frontier sub-bullet narrowed, index parity) plus **one new edge class in
the lane's executed sample** (a live-service state, not a new verdict channel), with
`coverage/constructs` unchanged; the draft entry's "a grader class the lane has not read before", its
pass-count sentence, its "decoration" verdict and its "container that lacks them" environment
sentence overclaim, and one wave-1 artifact (`R37DockerOracle`, a real-image oracle/reward run)
**crosses** the round-35/36 admission and must stay out of the entry. 13 drop-in fixes follow; the
frozen predicate is untouched.

---

## 1. Axis: is a third TB2 grader new surface (coverage) or the same instrument on new inputs (quality)?

### 1.1 The rule being applied

`lane-addendum.md` §9 is the binding clause (`scripts/hyaku/lane-addendum.md:317-321`):

> "Name the axis by the surface the round changes, not by the number it produces (kaidoku r29).
> Re-scoring a rule the lane already holds on new inputs … is quality work, never coverage or depth.
> A coverage claim names the surface it moves (frontier → core, a new tool, operation or edge class)
> and the command that would show it unmoved."

So three tests, in order: (a) is the change a surface the clause lists (not a number)? (b) is it a
re-scoring of a held rule on new inputs? (c) does the claim name that surface and a command that
would show it unmoved?

### 1.2 What the lane already held before this round

| Held | Where | What it means for C2's class claim |
|---|---|---|
| WebArena scorer predicates over page/URL/HTML state, read statically | `corpus/knowledge/webarena-task-spec-audit.md:6` ("inventory a scorer's predicates"); `:41` (page-content evaluator table); `:125` (AST-derived scorer-contract locations); `:2` "not live benchmark execution" | a **service/state** grader was already *read* in round 28; only *execution* is new |
| SWE-bench Pro V2's log-scan grader over its PASSED set; Harbor's `Verifier.verify` | `corpus/knowledge/benchmark-verifier-execution-model.md:104-112` ("The *passed* side is not a test-runner verdict but a log scan"; round 31 executed the parser and "minted twenty `PASSED` records", reward `PASSED`) | a **verdict from stdout text** was already *executed* in round 31; only the live-service state is new |
| TB2 `protein-assembly` function executed offline (S105–S107) | `corpus/knowledge/tb2-protein-assembly-grader.md:1-40` | the instrument shape (capture pin → frozen case table → requirement map) is round 35's |
| TB2 `regex-log` function executed offline (S108–S110) | `corpus/knowledge/tb2-regex-log-grader.md:1-35`; README:259 "A second instance of the round-35 ground … not breadth" | a third task is an instance increment, not benchmark coverage |

### 1.3 The strongest counterexample

> *"C2's 'new grader class' is a recomposition of elements the lane already read: a verdict from a
> subprocess's output text (S093's log-scan grader, round 31) over web state (`StringEvaluator`/`URL`/
> `HTML`, round 28). It is the same instrument on new inputs — quality work."*

This breaks the claims file's sentence, which is the round's own words: "the first service/state
grader the lane reads; rounds 35 and 36 read a data-string grader and an agent-authored regex grader"
(`plans/round-37-claims.md:64-66`). The lane's own entries contradict both halves of it: round 28
read WebArena's state predicates and explicitly did not execute them
(`webarena-task-spec-audit.md:2,6,41`), and round 31 **executed** SWE-bench Pro V2's log-scan path
("The *passed* side is not a test-runner verdict but a log scan") and minted twenty `PASSED` records
(`benchmark-verifier-execution-model.md:104-112`). The draft entry repeats the wider claim:
"adds a grader class the lane has **not read before**" (`entry.md:37`).

The counterexample does **not** break a corrected claim, because the difference that survives is an
**executed object**, not a reading and not a verdict channel: the graded state is two HTTP responses
from a service the probe starts (`verify.sh:57,60`), read by a helper the grader runs end-to-end
(`test_outputs.py:11`) — no executed probe in the lane's sample had a live-service state. The
substring verdict itself is not new: round 31 executed that channel. Under §9 the admissible surface
is therefore "one new edge class in the executed sample: a live-service state", not "a new grader
class" and not "the first service/state grader the lane reads". The entry must say **executed
sample**, name round 28 and round 31 as the held precedents, and say what it does not claim.

### 1.4 Ruling

- **Axis name: coverage is admissible, but only in the two sub-rows.** `coverage/surfaces`: one
  §Frontier sub-bullet narrowed for one task, one coverage-map row, one PROVINCE paragraph, knowledge
  files/index rows 43→44, SOURCES 103→106. `coverage/constructs`: **unchanged**; the class sentence
  is a property of this capture's evidence, not a construct claim (the same demotion round 36's F8
  required for "a new input class"). The surface is one new edge class in the **executed** sample: a
  live-service state, read through a captured helper — not a new verdict channel (round 31 already
  executed the log-scan channel) and not a new reading (round 28 already read state predicates). The command that would show the surface unmoved is the freeze
  control: `python3 plans/round37_c2_verify.py --lane .` → `checks=7 defects=4`, exit 1
  (`.ufo/waves/round-37/claims/control-c2-nothing.txt`), red exactly on the absent entry/rows.
- **Not "quality work on new inputs":** quality-only would be right if the entry claimed nothing about
  the verdict class; it does, and the class difference (helper stdout + live service + two-request
  split) is what the probe was built to show. But it is one instance and one edge class — the entry
  must not read as progress toward 89 TB2 graders, and the README row must say "3 of the 89 … not
  breadth".
- **If the unqualified class sentence lands**, a reader scores novelty/constructs by assertion, a leg
  the frozen counter does not measure. That is the axis defect, and it is fixed by F1/F6/F9/F11.

---

## 2. Scope: does running a sysadmin task's verifier in a sandbox cross PROVINCE?

### 2.1 Boundary test on the frozen probe (the thing C2 actually admits)

| Boundary | Answer | Evidence (command → output) |
|---|---|---|
| Runs Terminal-Bench or a harness? | No | the probe imports the captured test function and calls it; `test.sh` is read, not executed (`entry.md:157-160`); probe code `plans/git_webserver_probe.py:203-240` |
| Runs the task image? | No | no docker in the probe; the image name is only read from `task.toml:29`; `grep -n 'docker\|subprocess.run' plans/git_webserver_probe.py` shows one local `subprocess.run` of `bwrap` |
| Runtime task validity / certification? | No | 22 synthetic states authored by the lane; no submission, no agent, no harness; entry Negative space refuses validity |
| Deployment configuration (round-29 refusal)? | No | the oracle's nginx/git/ssh config is described, not applied (`entry.md:146-153`); the probe's service is a lane-owned `http.server` (`probe:180-215`) |
| Web properties (**kake**)? | No | the server is on the sandbox's own loopback in a `--unshare-net` namespace (`probe:204`); no site, no property |
| Serving plane / endpoint identity (**kama**)? | No | no model, no shim, no host port; `--unshare-net` severs the namespace |
| Can a sysadmin script mutate the host? | No | `--unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session`, `/usr` and `/tests` read-only, `HOME=/work/home`, `PATH=/work/bin` (`probe:203-240`); independent seat re-ran all 22 and verified the operator's `~/.ssh/config` `mtime`/`sha256` unchanged (`build/R37IndepVerdicts.md`) |

**Ruling: inside.** The sandbox is precisely what keeps a sysadmin verifier inside: no network, no
root, no host `HOME`, `/tests` read-only, `PATH` scoped. This is the round-35 admission ("offline
synthetic-fixture execution of one pinned … grader function", `PROVINCE.md:230-240`) applied to a
helper script instead of a function.

Two wording conditions make that stay true:

1. The entry must not imply it ran the verifier *as the image runs it*. It ran it with no network, no
   root, no `expect`/`git`/`apt-get`, and a scoped `PATH`; `task.toml:34` declares
   `allow_internet = true` and `task.toml:29` names the image. The draft's "fail exactly as they
   would in a container that lacks them" (`entry.md:118`) is a container counterfactual the lane has
   not observed, and the image is not such a container.
2. The oracle description must be labelled as the maintainers' own file, not a deployment recipe
   (F7).

### 2.2 The crossing candidate in this round's wave-1 material

`build/R37DockerOracle.md` did what the frozen claims' limit says the round does not do: it pulled the
pinned image, ran `solution/solve.sh`, ran `verify.sh`, ran `tests/test.sh` through `uvx`, and read
`/logs/verifier/reward.txt = 1` on the oracle path and on two "cheat" states (B/B2/C), plus a new
`NOT TEST PASSED` observation (C2). That is **runtime execution inside the task image** and an
**oracle-passes task-validity instrument** — the exact classes the lane's admissions exclude:

- `PROVINCE.md:236` (round 35): "does not run Terminal-Bench **or the task image**, validate or
  certify the task or any real submission";
- `PROVINCE.md:218-219` (round 29a2): "does not run a benchmark, certify a task, or own deployment
  configuration, runtime task validity, hosted judges, contamination measurement";
- every TB2 coverage bullet says "not runtime execution inside the task image".

It does not hit a kama/kake/kotoba refusal, but it is outside the admitted instrument scope, and
absorbing it would also import a **reward** observation and a **gameability** claim the frozen
counter never checks. It must be **routed, not absorbed** (F13). If the L1 wants any of it, the
minimum is: a new PROVINCE paragraph naming the real-image observation as its own surface, a post-hoc
entry section labelled outside the frozen 22, and no reward/gameability/oracle-passes/task-validity
claim. Without all three, the round crosses.

**Impacted axes:** coverage (the absorbed run would be a different, unmeasured surface), calibration
(reward claim not checked by any frozen predicate), adjacency (task-validity instrument, which the
lane routes out).

**Smallest safe correction:** leave `R37DockerOracle`'s content in the build dir; cite it nowhere in
`corpus/`; record it in the round report as a routed observation with its limits.

---

## 3. Wording fixes (13; full copy-paste text in `R37CritScope/dropins.md`)

Each fix is new text only; none changes a frozen byte (claims, gate, counters, probe, mutants).

**F1 — class claim (entry :34-40; claims :64-66 recorded as an overstatement, never edited).**
Replace "adds a grader class the lane has not read before" with "records one new edge class in the
lane's **executed** grader sample", name the held precedents (round-28 WebArena
`StringEvaluator`/`URL`/`HTML` read statically; round-31 SWE-bench log-scan executed — so the
substring channel is not new, the live-service object is), state "a property of this capture's
evidence, not a construct claim", and change "It discharges" to "It **narrows** … for this one task
only; … stays open for the remaining TB2 task graders (89 carry `tests/test.sh`; 3 are now read)".
Drop-in in `dropins.md` §F1. Because the claims file is frozen, put the correction in the entry and
record the claims sentence in the round report under a dated erratum line — the round-36
stale-digest precedent (append, never rewrite).

**F2 — pass-count arithmetic (entry :27-32).** The draft says "Six of the nine passing cases … A
seventh and eighth pass are legitimate controls (an exact body with no trailing newline, and the
wget branch taken when curl is absent)". Both halves are wrong: the wget examples
(`wget-static-file`, `wget-token-in-body`) are inside the six, so the same cases are counted twice,
and the ninth (`slow-server-3s`) is never classified. Exact breakdown from the receipt:
five no-assertion passes (`static-file-no-git`, `wget-static-file`, `token-in-body`,
`wget-token-in-body`, `status-then-content-split`), one request-not-varied (`catch-all-200`), one
no-timeout (`slow-server-3s`), two exact-content controls (`exact-no-newline`, `trailing-newlines`)
= 9. Drop-in in `dropins.md` §F2.

**F3 — "graded artefact" sentence (entry :11-16).** "it is a **live HTTP service on port 8080** plus
a git server" makes the git server part of the graded artefact; the capture shows the opposite (the
helper's git step is run, its status never read). Also "the task's whole score" must be "in this
capture the whole score". Drop-in in `dropins.md` §F3.

**F4 — observation, not judgement (entry :106 and :145).** "Nothing in the grader observes it" →
"No line of either captured file reads the clone, commit or push status"; "The instruction's first
six lines are decoration for this grader" → "No assertion in this capture observes any of the
instruction's first six lines". "Decoration" is a validity verdict; the observable is the missing
read.

**F5 — environment of observation (entry :116-119).** Replace "fail exactly as they would in a
container that lacks them" with the actual construction (`PATH=/work/bin`, `/usr` read-only, `expect`
bound to `/dev/null`, private netns) and the disclosure that `task.toml:34` declares
`allow_internet = true` and `:29` names the image, neither exercised. This sentence is what keeps the
"sysadmin verifier" inside; as written it makes a container claim.

**F6 — "discharges" in README §Frontier.** Use "Partly discharged round 37 … **narrowed for that one
task only**; it stays open for the remaining TB2 task graders (3 of 89 read) … and for runtime task
validity". Drop-in in `dropins.md` §F6.

**F7 — Negative space additions (entry :177-186).** Add five refusals: gameability/solver strategy;
deployment or web-property guidance (kake; deployment outside); harness/toolchain fidelity
(`test.sh` runs under `uvx -p 3.13`/`pytest==8.4.1`, the probe runs host `bash`/`curl`/`wget`/Python;
`allow_internet = true`); contamination (`test_outputs.py:1-2` canary); and "nothing from a run of
the task image". Drop-in in `dropins.md` §F7.

**F8 — provenance scope (entry :2, :46).** S112's label "lines 1–91" is one short: the capture has
92 lines (`echo "Test completed"` is `verify.sh:92`). The task.toml label says "read only for the
task description and the verifier timeout", but the entry uses the image name (`task.toml:29`); widen
the label to description, declared timeouts (`:22`, `:25`), declared image (`:29`) and declared
internet policy (`:34`).

**F9 — README coverage row.** New third-task row that says "3 of the 89 TB2 task graders; not
breadth, and no quality, validity, difficulty or gameability verdict", one new edge class in the
executed sample (the graded state is a live service), and the explicit not-list. Drop-in in
`dropins.md` §F9.

**F10 — PROVINCE paragraph.** New "Round37 partial frontier admission" paragraph: sandbox
construction, the graded state (two HTTP responses from a probe-started service), the full not-list
(no harness, image, submission, validity, difficulty/gameability, assertion correctness,
contamination, remaining 86 tasks), "any real-image observation is routed out and not part of this
admission", and the adjacency routing (kake/kama/refusals). Drop-in in `dropins.md` §F10.

**F11 — SCORECARD coverage cell + optional capability row.** Name `coverage/surfaces` vs
`coverage/constructs: unchanged`, give the unmoved-surface command (`checks=7 defects=4` at freeze),
claim no score move; add first-working-round `service-grader-probe` capability if the capability
table is updated this round. Drop-in in `dropins.md` §F11.

**F12 — SKILL draft Part C (the exploit-recipe vector).** The table heading "probe it with" plus
cells like "serve the verdict token as the response body", "delete the tool a required step needs and
see whether the verdict moves", "answer the status request 200 and the content request with the
wrong body" is a **recipe** for constructing passing states, not a record of what the receipt shows.
Also "whose state the agent chooses" presumes solve-time agent control the capture does not
establish, and "What a green means here: the agent served …" is solver framing. Rewrite as past-tense
observations of the frozen run, drop the agent premise, and append the bounds line. Drop-in in
`dropins.md` §F12.

**F13 — no absorption of the real-image run.** Do not cite `R37DockerOracle.md`, its
`reward.txt = 1`, its B/B2/C "cheat" runs or its `NOT TEST PASSED` observation in the entry,
SKILL.md, README or PROVINCE. Keep them in the build dir and the round report as a routed observation
with their limits (one observation per scenario, apt-mutated containers, `/tests` copied not
harness-bound, `/logs/verifier` hand-made, `--cpus 1` not enforced, image removed). If absorbed, the
three conditions in §2.2 apply or the round crosses.

---

## 4. Checked and not defects

- **All 32 located quotes are byte-verbatim on their cited capture lines.** Script:
  parse `| claim | “quote” | \`file:line\` |` from `entry.md`, compare to the capture line →
  `quotes parsed: 32`, `BAD quotes: 0`. The round-36 routed-item-3 failure mode (quote shape) is not
  present at the draft stage; the gate's V2 legs (verbatim, distinct, 3–25 words, ≥8 locations) have
  a clean input.
- **Receipt arithmetic is consistent.** 22 CASE lines; 9 `observed=pass`, 13 `observed=fail`;
  summary `cases=22 observed_pass=9 observed_fail=13 mismatches=0`; parse in §5. Every case the entry
  cites by id is present, with the observed verdict the entry assigns it.
- **Requirement map labels agree with the receipt** (V7's premise): `1-6` unenforced cites
  `static-file-no-git` (pass); `7` partly cites `wrong-port-8081` (fail) + `static-file-no-git`
  (pass); `8` partly cites `not-found` (fail) + `catch-all-200` (pass); `9` enforced cites
  `capitalised`, `leading-space` (both fail). Ranges cover `instruction.md` lines 1–9 of 10.
- **The sandbox claims in the entry match the probe code**: `--unshare-net/pid/ipc`,
  `--ro-bind /usr`, `/etc`, `/tests`; `--tmpfs /tmp`; `--bind work /work`; `PATH=/work/bin` with
  `BASE_TOOLS = bash, sleep, chmod, mkdir, cat` plus the case's `curl`/`wget`
  (`plans/git_webserver_probe.py:49,203-240`). No `--uid/--gid`, so it runs as the invoking user.
- **`test_outputs.py:13` is the whole verdict** and `verify.sh:62` echoes the body (both quoted).
- **The free-standing facts**: `instruction.md` 10 lines; `task.toml` 41 lines with
  `[verifier] timeout_sec` at :22, `[agent]` at :25, `docker_image` at :29, `allow_internet` at :34;
  `test.sh` 25 lines with `uvx`/`pytest` at :14-18 and the reward writes at :22/:24.

---

## 5. Evidence (every number with the command that produced it)

| Fact | Command | Output |
|---|---|---|
| lane tip | `git -C … rev-parse HEAD` | `a3163e675374551bc911d97040d01caf2377a7d7` |
| locale of the `coverage` label | `grep -n "surface the round changes" scripts/hyaku/lane-addendum.md` | `:317` (clause quoted in §1.1) |
| WebArena state predicates were read, not run | `sed -n '1,12p;41p;125p' corpus/knowledge/webarena-task-spec-audit.md` | title "inventory a scorer's predicates"; `:41` page-content evaluator row; `:125` AST statement locations; "not live benchmark execution" |
| SWE-bench log-scan grader executed in round 31 | `sed -n '104,112p' corpus/knowledge/benchmark-verifier-execution-model.md` | "The *passed* side is not a test-runner verdict but a log scan"; "output minted twenty `PASSED` records and the reward came out `PASSED`, exit 0" |
| TB2 task count | `grep -n "89 \`tests/test.sh\`" corpus/knowledge/benchmark-verifier-execution-model.md` | `:93` "of its 89 `tests/test.sh` files" |
| current index state | `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md`; `ls corpus/knowledge/*.md | wc -l`; `grep -c '^| \`knowledge/' corpus/README.md` | `103`; `43`; `43` |
| S111 absent at draft time | `grep -c '^ *| *S111 *|' corpus/SOURCES.md` | `0` |
| entry absent at draft time | `test -e corpus/knowledge/tb2-git-webserver-grader.md` | `no` |
| quotes verbatim | parse `entry.md` quote table vs captures | `quotes parsed: 32` / `BAD quotes: 0` |
| receipt cases | parse `CASE …` lines of the receipt | `cases 22`; passes = `static-file-no-git, exact-no-newline, trailing-newlines, catch-all-200, token-in-body, status-then-content-split, slow-server-3s, wget-static-file, wget-token-in-body`; `fails 13` |
| receipt summary | `grep '^cases=' receipt` | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` |
| capture lengths | python `splitlines()` over each capture | `verify.sh 92`, `task.toml 41`, `instruction.md 10` |
| sandbox construction | `read plans/git_webserver_probe.py:203-240` | bwrap flags as quoted in §2.1; `BASE_TOOLS` at :49 |
| before control | `cat .ufo/waves/round-37/claims/control-c2-nothing.txt` | `checks=7 defects=4`, `PREDICATE C2 fail`, `exit=1` |
| independent sandbox re-run agrees | `read .ufo/waves/round-37/build/R37IndepVerdicts.md` | `cases=22 agree_receipt=22 disagree_receipt=0`; operator `~/.ssh/config` unchanged |
| real-image run (the crossing candidate) | `read .ufo/waves/round-37/build/R37DockerOracle.md` | image pulled; oracle path `reward.txt = 1`; B/B2 static pass, C token pass, C2 `NOT TEST PASSED` pass; single observation per scenario |

---

## 6. Limits of this review

- I judged the **draft** bytes at `a3163e6`, not the landed entry; the L1 may re-cut every string.
  The drop-ins are text, not patches.
- I did not run either counter for a score, and I make no finding on C2's predicate (C1/C2 scoring is
  the frozen counters' job). The quote check was my own parse, not the gate's V2.
- The claims file is frozen; I did not treat its "first service/state grader the lane reads"
  (`plans/round-37-claims.md:64-66`) as editable. The entry and the round report must carry the
  correction; if the L1 instead lands the claims sentence verbatim, the axis defect stands.
- I did not execute the probe or the image. The real-image report is read as an artifact; its
  observations are not re-derived here, and I make no claim about which of them are repeatable.
- Whether the L1 admits F13's real-image observation is a scope decision I recommend against; the
  conditions under which it would be admissible are stated, not tested.

VERDICT: scope-inside-13-wording-fixes
