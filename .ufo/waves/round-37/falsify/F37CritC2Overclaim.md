# F37CritC2Overclaim — overclaims in `corpus/knowledge/tb2-git-webserver-grader.md`

Seat: critic (leaf), round 37 wave 2. Target: the C2 entry as landed at tip `357deceb`. Method: every
sentence checked against the frozen receipt, the six captures (`corpus/evidence/round37/tb2-git-webserver/`),
the frozen case table, the probe source at its frozen digest, the wave-1 reports and the corpus files the
entry cites. Two frozen cases were re-run in my own clone at the tip through the probe's own machinery
(`diag-cases.txt`, `diag-verify-stderr.txt`). No lane file was edited; scratch
`/fast/scratch/hyaku/kengaku-r37/F37CritC2Overclaim` removed after the receipts were copied here.

Axes attacked: **calibration** (a label or mechanism stronger than its case), **provenance** (a sentence
claiming less or other than what the round's own evidence shows), **coverage** (a claim whose support is
outside the frozen instrument). Geometry, digest and quote integrity were checked first and held.

## What held (bounds the findings)

- **Located quotes: 32/32 exact.** `python3` rows parse of the entry's `## Located quotes` table against
  the captures: `located-quote rows checked: 32 / byte-exact at cited line, 3-25 words: 32 / problems: []`
  (`quotes-check.txt`). No quote, line number or word-count defect.
- Line refs verified with `grep -n ""` on the captures: `task.toml:22` verifier timeout, `:25` agent
  timeout, `:29` image, `:34` internet; `test.sh:14-25` uvx→pytest→reward; `verify.sh:48-49` (run, status
  unread), `:57/:59/:60/:62/:63/:66/:68/:71/:75/:76/:77/:88`; `test_outputs.py:9-13`; `instruction.md:1-10`.
- Receipt arithmetic and provenance: `cases=22 observed_pass=9 observed_fail=13 mismatches=0` is the
  receipt's last line; the dry table prints `cases=22 predicted_pass=9 predicted_fail=13`; probe sha256
  `63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf`; capture digests equal `SHA256SUMS`
  (`sha256sum corpus/evidence/round37/tb2-git-webserver/*`).
- Cross-entry anchors: S114 body line 39 and meta (`created_at 2026-07-14T06:32:15Z`, `state open`) hold;
  S100 is the same repository at `2fd12b88` (`corpus/SOURCES.md:113`); "89 tasks carry `tests/test.sh`"
  holds via `corpus/knowledge/benchmark-verifier-execution-model.md:93`; the round-31 quote is at
  `benchmark-verifier-execution-model.md:104`.
- My two re-runs agree with the receipt: `static-file-no-git` → `VERDICT pass`; `token-in-body` →
  `VERDICT pass` with stdout `'Content: TEST PASSED'` then
  `'❌ TEST FAILED: Content does not match expected output'` (`diag-cases.txt`).

## Findings

### F1 (high) — the requirement map calls `instruction.md:9` `enforced` while a line-9-violating state passes

Quote (entry:107): `| instruction.md:9 | enforced | capitalised, leading-space |`. The entry's own rule
(entry:98-99): "`enforced` means a probe case that violates the requirement is observed `fail`".

Counterexample: `token-in-body` serves the body `TEST PASSED` — a user running the instruction's `curl`
would not see `hello world` — and the receipt records `observed=pass`; I re-ran it in my own sandbox:
`VERDICT pass`, stdout `'Content: TEST PASSED'` … `'❌ TEST FAILED: Content does not match expected output'`
(`diag-cases.txt`). A state that violates line 9 is observed pass, so by the map's own definition line 9 is
`partly`, not `enforced`. This is internal: the entry's headline 2 says the same body passes.

Axis: calibration — and the frozen counter cannot catch it: `plans/round37_c2_verify.py` v7 only checks
"`enforced` and 'fail' not in verdicts" over the cited cases, and `capitalised` is a failing case, so V7
stays green (`sed -n '/def v7/,/^def /p'`).

Smallest safe correction: label `instruction.md:9` `partly`, cite `token-in-body`/`wget-token-in-body`
alongside the strict-comparison cases, and reword entry:122 from "Strictly enforced by the shell string
comparison" to "exact for the body it compares; the verdict is a stdout substring, so a non-`hello world`
body passes".

### F2 (high) — "the port half is enforced" contradicts the entry's own case-independence caveat

Quote (entry:116-117): "The port half is enforced — a server on 8081 only makes the first request return
`000` (`wrong-port-8081`, observed fail)." The receipt prints the same line for both cases:
`❌ TEST FAILED: Web server returned HTTP 000` under `no-server` and under `wrong-port-8081`. The entry's
own bullet (entry:208-210) says the case "shows that an empty `:8080` fails, not that a correct body
elsewhere is rejected *as such*"; `R37CritCases` §2.2 reached the same conclusion and isolated the port
clause only with a post-hoc fixture.

Axis: calibration. V7 passes this row too (`partly` + one fail, one pass cited), so the label lands.

Smallest safe correction: state the mechanism, not the verdict: "the URL at `verify.sh:57` is hard-coded to
`:8080`, so a service only on another port is invisible (same stdout as `no-server`); the port clause is
isolated only by the post-hoc extra case, not by the frozen 22".

### F3 (medium) — `slow-server-3s` still carries the causal label wave 1 told the entry to drop

Quote (entry:33): "one because `curl` runs without a timeout (`slow-server-3s`)"; same mechanism in the
group table (entry:154). Wave-1 `R37CritCases` §3.3: "Three seconds cannot distinguish 'no timeout' from
'any timeout > 3 s'" and "Safe relabel: 'a 3 s response still counts'". The static fact (no `--max-time` at
`verify.sh:57/:60`) is real; the case does not demonstrate it.

Axis: calibration — the entry cites the correction but kept the label in the summary.

Smallest safe correction: "one because a ≥3 s answer still counts (`slow-server-3s`); `verify.sh` passes no
`--max-time` (static)". Same wording in the timing row.

### F4 (medium) — the git step does not fail with `command not found`

Quote (entry:133-134): "The install step and the git step therefore fail with `command not found` before
the grader's verdict is computed".

Counterexample (my run, clone at `357deceb`, probe digest verified):
`harness_rc= 0`, `RC 0`, stderr `'/tests/verify.sh: line 5: apt-get: command not found\n/tests/verify.sh:
line 6: apt-get: command not found\n/tests/verify.sh: ./git_test.exp: /usr/bin/expect: bad interpreter: No
such file or directory\n'` (`diag-verify-stderr.txt`). The install step fails `command not found`; the git
step fails at the interpreter (`:49` runs `./git_test.exp`, whose shebang is `/usr/bin/expect`).

Axis: calibration (mechanism description; the conclusion — both statuses unread — is unaffected).

Smallest safe correction: "the install step fails `command not found` and the git step fails on the absent
`expect` interpreter (`bad interpreter`), both before the verdict is computed; nothing in `verify.sh` reads
either status".

### F5 (medium) — "the grader reads nothing from the filesystem"

Quote (entry:167-168): "the grader reads nothing from the filesystem and makes two HTTP requests, so the
only things that can fail it are the HTTP status of the first request and the body of the second."

Counterexample from the capture: `test_outputs.py:11` runs `/tests/verify.sh`; `verify.sh` writes
`~/.ssh/config` (:9-13), writes and then executes `git_test.exp` (:16, :49), and in the wget branch reads
`test_output.html` (:75-77). What is true is that it inspects no repository or solution file. The second
clause is also too strong: a body that is not `hello world` passes (F1), so the failing input is the token
in stdout, not "the body of the second" as such.

Axis: calibration.

Smallest safe correction: "inspects no repository or solution file — only its own scratch files — and
reaches the service over HTTP; it fails a state only when the first request is non-200 or the helper's
stdout lacks the token".

### F6 (medium) — "two HTTP responses" is curl-only

Quote (entry:15-16): "two HTTP responses from a service on `:8080`"; repeated as "the graded state is two
HTTP responses" (entry:42-43).

Counterexample: the wget branch issues one request — `wget -q -O test_output.html
http://localhost:8080/hello.html` (`verify.sh:75`) then `cat test_output.html` (:77); the receipt's three
wget cases print no status request.

Axis: coverage/calibration.

Smallest safe correction: "one or two HTTP requests per case (curl: a status request then a body request;
wget: one, then a local file)".

### F7 (medium) — "whole surface" vs the four post-hoc states the same entry reports

Quotes (entry:196-199): "The 22 cases are the claim's whole surface … are not covered and are not
claimed." vs (entry:204-205): "The critic predicted and ran four cases outside the frozen 22 … a token on
the second line of a multi-line body passes". The second sentence is exactly the "body with an embedded
newline" state the first says is not claimed; `R37CritCases` §5 records that pass (`multiline-token`).

Axis: coverage/provenance — the four extras live only in `.ufo/waves/round-37/build/R37CritCases/` and the
frozen counter cannot reproduce them.

Smallest safe correction: "not covered by the frozen receipt and not claimed as receipt results; four
post-hoc states are recorded in the independence note below, outside the receipt".

### F8 (high) — "was not executed" for the oracle is contradicted inside `corpus/`

Quote (entry:58): "was not executed, and nothing below rests on it" (of `solution/solve.sh`).
`corpus/lessons/round-37.md:27` records: "Real-image run of the task (`build/R37DockerOracle.md`: oracle
path, static-file and token-body states, `reward.txt = 1` through `test.sh`) | **Refused for the corpus;
routed**". `R37DockerOracle` §A ran `bash /tests/solve.sh` (exit 0, 18.08 s) and the oracle path reached
`reward.txt = 1`; the entry's own negative space then says "(no run of the image …)" (entry:222).

Axis: provenance/identity. The entry is right that it *uses* no real-image observation (entry:240), but
"was not executed" is false of the round, and a corpus reader can hold the entry and the lessons row at
once.

Smallest safe correction: scope the sentence to the instrument — "not executed by the probe, and this entry
uses no execution of it (this round's one image run is routed, `lessons/round-37.md:27`)". That keeps
F13's routing rule: the build artifact is not cited.

### F9 (medium) — the WebArena cross-reference cites a heading

Quote (entry:42): "round 28 read WebArena's `StringEvaluator`/`URL`/`HTML` predicates over page state
statically (`knowledge/webarena-task-spec-audit.md:6,41`)".

Counterexample: `sed -n '1,12p;39,43p'` of that file — line 6 is the H1 title ("# WebArena task-spec audit
— inventory a scorer's predicates without certifying task validity"); the `URL` row is `:40`, the
page-content/HTML row `:41`, and `StringEvaluator` appears at `:1` (source line). `:6` locates no predicate.

Axis: provenance.

Smallest safe correction: cite `:1,40-41`.

### F10 (low) — "the failure message itself carries the token"

Quote (entry:171). The failure message is `echo "❌ TEST FAILED: Content does not match expected output"`
(`verify.sh:66`) and contains no token; the token reaches stdout at `:62` (`Content: $CONTENT`) and `:68`
(`Got: '$CONTENT'`). The entry's next clause already attributes it to "an echo".

Axis: calibration.

Smallest safe correction: "the helper's failing output carries the token, via `:62` and `:68`; the failure
message at `:66` does not".

### F11 (low) — "`HOME` and `/tmp` inside scratch"

Quote (entry:130). The probe binds the scratch work dir at `/work` and sets `HOME=/work/home`
(`plans/git_webserver_probe.py:235`), but `/tmp` is a fresh tmpfs (`--tmpfs /tmp`, `:209`), not the scratch
directory. The frozen claim has the same wording (`plans/round-37-claims.md:77`), so this is inherited;
the entry is what the corpus admits.

Axis: operability (residue accounting), calibration.

Smallest safe correction: "`HOME` in the scratch work dir and a private `/tmp` tmpfs".

### F12 (low) — "discarded its output unread"

Quote (entry:66-67). `plans/round-37-claims.md:7-9`: "the gate compared its output with the hand-typed
receipt and discarded it … no verdict was printed or read" — a comparison reads the output. The stronger
and supported claim is the one about the verdict.

Axis: provenance.

Smallest safe correction: "discarded without a verdict being printed or read".

### F13 (low) — the prediction disclosure narrows the pre-run reading

Quote (entry:62-63): "a static reading of `verify.sh`, `test_outputs.py` and `instruction.md`".
`plans/round-37-claims.md:74-75` records the same sentence with "(the reading included the captured
oracle)". The entry's disclosure as written claims a narrower pre-run input than the frozen claim.

Axis: provenance/calibration.

Smallest safe correction: add "and the captured oracle" to the disclosure sentence.

## What I checked and did not find

- No located-quote, digest, line-number or word-count defect (32/32).
- No defect in the receipt's counts, the dry table's predictions, the probe digest, or the falsifier's
  four conditions as written; my two re-runs agree with the receipt.
- The case-independence bullet, the headline-1 caveat, the prior-art paragraph, the S114 quote and line,
  the README frontier narrowing, the "89/3" count and the S100 identity are supported as written.
- I did not re-run all 22 cases (two only) and did not run the task image; the real-image material here is
  read from `R37DockerOracle.md` and the routed row in `corpus/lessons/round-37.md:27`. I make no statement
  about the image run's repeatability or about task validity.

VERDICT: overclaims-13
