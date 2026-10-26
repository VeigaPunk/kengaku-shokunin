# R37CritCases — are the 22 frozen grader cases single-mechanism, correctly labelled, and sufficient?

Seat: critic (leaf). Round 37 wave 1. Lane read-only; nothing frozen edited. Probe imported at its frozen
digest, captures at their pins:

- `sha256sum plans/git_webserver_probe.py` → `63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf`
  (matches the freeze pin `63cb75cf…5eedf`), printed by my runner as `# probe sha256=63cb75cf…`.
- `sha256sum corpus/evidence/round37/tb2-git-webserver/{instruction.md,test_outputs.py,verify.sh}` →
  `62151b73…1d97`, `526aee3d…8b37`, `1dc44c92…3d05`; each probe pin verified `pinned=yes` at run time.

Executed: `run_uncovered.py` → `uncovered_extra matched=4/4`; `run_extras.py` → `extras matched=2/2`.
Logs and scripts: `.ufo/waves/round-37/build/R37CritCases/` (`PREDICTIONS.md` written before the first run,
`PREDICTIONS-extra.md` before the extras). Scratch `/fast/scratch/hyaku/kengaku-r37/R37CritCases` deleted.

## 1. Adjudication of the 22 frozen cases

Rule used for "confounded": the case's observation cannot distinguish the mechanism its `requirement` label
names from an alternative the harness admits (a second variable is inoperative or a second line produces the
same bytes). Line numbers are from `cat -n` of the captured `verify.sh` (91 lines) and `test_outputs.py`
(13 lines).

| case | label names | line that decides the observed bytes | review |
|---|---|---|---|
| no-server | verify.sh:57-59 | :71 (`HTTP 000`) | isolated |
| static-file-no-git | verify.sh:49 (+ instruction.md:1-6) | :49 never executes in this sandbox | **confounded** (§2.1) |
| exact-no-newline | instruction.md:9 | :63 | isolated |
| trailing-newlines | verify.sh:60 | :60 substitution, :64 pass | isolated |
| capitalised | :63 | :63 → :66 | isolated |
| leading-space | :63 | :63 → :66 | isolated |
| trailing-space | :63 | :63 → :66 | isolated |
| crlf | :63 | :63 → :66 | isolated (rendering caveat, §3.4) |
| bom | :63 | :63 → :66 | isolated |
| empty-200 | :63 | :63 → :66 | isolated |
| not-found | :59 | :59 false → :71 (`404`) | isolated |
| http-500-right-body | :59 | :59 false → :71 (`500`) | isolated |
| redirect-301 | :57 (no `-L`) | :57, :59 false → :71 (`301`) | isolated (would pass with `-L`, since `/real.html` is 200) |
| catch-all-200 | :57,60 | :57/:60, :64 | isolated |
| wrong-port-8081 | instruction.md:7 | :57 hard-coded URL → :71 (`000`) | **confounded** (§2.2) |
| token-in-body | test_outputs.py:13 + verify.sh:62 | :62 **and** :68 both echo `$CONTENT` | **confounded** (§2.3) |
| status-then-content-split | :57,60 | pass ⇒ a second request was compared | isolated (a single request would fail) |
| first-request-404 | :57-59 | :59 false → :71 | isolated (complement of the previous row) |
| slow-server-3s | :57,60 ("without a timeout") | :57/:60, :64 | isolated verdict, **overclaim** (§3.3) |
| wget-static-file | :73-81 | :76 true → :80 true → :81 | isolated |
| wget-404 | :75-76 | :76 false → :88 | isolated |
| wget-token-in-body | :79 | :79 **and** :85 both echo `$CONTENT` | **confounded** (§2.3) |

Distinct grader-stdout signatures among the 22: **15** — `python3 -` over `git-webserver-probe.txt` pairing
each `CASE` with its `grader-stdout:` block prints `cases: 22 distinct grader-stdout signatures: 15`.
Identical groups: `no-server, wrong-port-8081`; `not-found, first-request-404`; and the six-file pass group
`static-file-no-git, exact-no-newline, trailing-newlines, catch-all-200, status-then-content-split,
slow-server-3s`. Identical stdout is not by itself a defect: five of those six are distinguished by their
fixture (a no-newline body, a catch-all path, a two-response sequence, a 3 s delay); only
`no-server`/`wrong-port-8081` vary a dimension the grader never observes.

## 2. Confounds, with the counterexample each admits

### 2.1 `static-file-no-git` — "the git step's status is ignored" is not exercised, only asserted

The label's mechanism is `verify.sh:49` (`./git_test.exp`, whose status nothing reads). In the probe's
sandbox that line cannot run: `/work/bin` holds only `bash sleep chmod mkdir cat` plus `curl`/`wget`, so
`git` is absent, and the heredoc's shebang is `/usr/bin/expect` (verify.sh:17), absent on this host
(`ls /usr/bin/expect` → `No such file or directory`) and masked to `/dev/null` by `sandbox_argv` on a host
that has it (`if os.path.exists("/usr/bin/expect"): … "--ro-bind", "/dev/null", "/usr/bin/expect"`).

My instrumented run (`run_uncovered.py` DIAG, probe harness, same fixture) prints, inside the sandbox:

```
DIAG stderr_lines=['/tests/verify.sh: line 5: apt-get: command not found', '/tests/verify.sh: line 6: apt-get: command not found', '/tests/verify.sh: ./git_test.exp: /usr/bin/expect: bad interpreter: No such file or directory']
DIAG cwd_files=['git_test.exp']
DIAG expect_path=''
DIAG git_path=''
VERDICT pass
```

So the pass is observed in a regime where the git step **cannot execute**. The alternative explanation the
case cannot exclude is "the step never ran", so the receipt's headline — "a file served on :8080 with no git
repository, hook or push passes (verify.sh never reads the expect step's status)" — is a static reading of
:49 with an observation attached, not a demonstration of :49. The frozen claims name the positive limit
("never runs the oracle … does not show that the intended path passes"); the negative direction — an executed
and *failed* clone/push is tolerated — is unnamed and is exactly what the entry headline needs. It is also
unreachable in this harness by construction, not by choice.

What the case *does* show, and all it shows: a tree with a static file and no repository passes, because the
grader reads nothing from the filesystem outside /work/cwd and makes two HTTP requests. Keep that sentence;
drop the parenthetical mechanism claim or move it to the named limits.

### 2.2 `wrong-port-8081` — indistinguishable from `no-server`

Receipt, both cases: `'❌ TEST FAILED: Web server returned HTTP 000'`. The grader never contacts :8081, so the
fixture's content (correct `hello world`) and its liveness are invisible; the case is `no-server` with an
extra process. The label points at `instruction.md:7` (a requirement), not at a verify.sh line; the decisive
lines are :57 (hard-coded `http://localhost:8080/hello.html`) and :71.

That the :8081 server really was serving was checked separately (probe harness, custom script): inside the
same run that the grader scored `HTTP 000`, `DIAG port8081_body_status='hello world\n|200'`.

Counterexample this admits: "the agent served the right bytes on 8081 and nothing on 8080" is scored
identically to "the agent served nothing", so the case cannot support the claim that the port is a
*requirement* rather than an incidental string. Executed replacement (predicted first, matched): one server
on :8080 answering `200 "not hello\n"`, one on :8081 answering `200 "hello world\n"` →
`'Web server test successful (HTTP 200)' | 'Content: not hello' | '❌ TEST FAILED: Content does not match
expected output'`, verdict `fail`. That fails at :63 on a live :8080 and is distinguishable from 000 and 404.

### 2.3 `token-in-body` and `wget-token-in-body` — the named echo site is not the only one

Labels name :62 (`echo "Content: $CONTENT"`) and :79. But :68 (`echo "Got: '$CONTENT'"`) and :85 echo the
same value unconditionally in the same branch, so no body token can distinguish them. The receipt shows both
files: `token-in-body` stdout contains `'Content: TEST PASSED'` **and** `"Got: 'TEST PASSED'"`. My
`multiline-token` run shows the same structure for a two-line body:
`'Content: first line' | 'TEST PASSED' | … | "Got: 'first line" | "TEST PASSED'"`.

Consequence: the pass is correctly attributed to `test_outputs.py:13` over *some* echo, and not to :62 or :79
specifically. This is not fatal for the entry (the mechanism "the verdict is a substring of stdout, and the
body reaches stdout" survives), but the case cannot be cited as evidence about :62, and a future edit that
removed :62 while keeping :68 would not be caught by it. The label is the defect; the observation is sound.

## 3. Label defects that are not full confounds

1. **Wrong actor for the deciding line**: `wrong-port-8081` cites `instruction.md:7`; the grader's decision
   is made by the literal URL at :57. (Covered in §2.2.)
2. **`no-server`, `not-found`, `http-500-right-body`, `first-request-404`** cite the `if` predicate (:57-59)
   while the bytes come from the `else` echo at :71. Uniform shorthand across the set; acceptable, but a
   reader checking "which line printed TEST FAILED" will land on :71, not the cited line.
3. **`slow-server-3s` overclaims**: "curl is run without a timeout". Three seconds cannot distinguish "no
   timeout" from "any timeout > 3 s", and verify.sh:53 adds `sleep 2` before the requests. The static fact is
   true (no `--max-time` on :57/:60); the case's power is "tolerates ≥ 3 s". A 3 s probe would also pass a
   future `--max-time 5`. Safe relabel: "a 3 s response still counts".
4. **Rendering caveat for `crlf`**: the probe captures with `subprocess.run(..., text=True)`, whose universal
   newlines rewrite `\r` in the *recorded* stdout; the receipt's `Got: 'hello world` / `'` split is an
   artefact of that translation, not of verify.sh. The verdict (fail at :63) is unaffected; the receipt is not
   a byte record for CR bodies.

## 4. Coverage: what has no case

### 4.1 instruction.md lines (10 lines, `cat -n`)

| line | text (≤ 25 words) | case |
|---|---|---|
| 1-6 | "git clone user@server:/git/server … git push origin master" | **none that executes** — the expect step is inert (§2.1); only asserted via a static reading |
| 7 | "a webserver running on port 8080" | only `wrong-port-8081`, confounded; isolated for the first time by my `port-8080-junk-8081-correct` |
| 8 | "curl http://server:8080/hello.html" | negatively by `catch-all-200` (path not enforced); the URL is hard-coded at :57 |
| 9 | "then I see the output \"hello world\"" | yes — 8 cases over :60/:63 |
| 10 | "I'll setup login with the server to work" | **none** — verify.sh:9-13 writes `~/.ssh/config`; nothing checks it, and no case varies it |

### 4.2 verify.sh branches (91 lines)

| branch | case |
|---|---|
| :5-6 `apt-get` failures ignored | none (apt-get absent in every probe run; `prepare()` offers no way to inject a fake) |
| :9-13 `~/.ssh/config` | none |
| :16-46 heredoc/`chmod`/`:49` run | none that executes (§2.1) |
| :52-53 `echo`/`sleep 2` | unconditional; never varied |
| :55 `command -v curl` both arms | yes (`curl` cases; `wget` cases) |
| :57 status request (no `-L`, no timeout) | yes (5 cases) |
| :59 `= "200"` gate | yes |
| :60 **second response's status ignored** | **none** → `second-request-500` (executed, §5) |
| :62 echo, single-line body | yes |
| :62 echo, **multi-line body** | **none** → `multiline-token` (executed) |
| :63 compare, single-line | 7 cases |
| :63 compare, **body with a second line** | **none** → `hello-plus-second-line` (executed) |
| :64 pass echo | yes |
| :66-68 fail echo incl. **:68 co-echo** | no case *isolates* :68; it cannot be isolated (§2.3) |
| :71 non-200 echo | yes |
| :73-81 wget pass path | yes |
| :76 nonzero → :88 | yes for an empty-body 404; a 404 *with* a body is unexercised (minor) |
| :80 compare, false path → :83/:85 | **none** → `wget-wrong-content` (executed) |

**HEAD/GET split**: not a verify.sh branch at all. verify.sh issues two GETs (:57 with `-o /dev/null`, :60)
and nothing uses `-I`; `test_outputs.py:11` only runs `bash /tests/verify.sh`. The probe's `SERVER_PY` sets
`do_HEAD = answer`, so a HEAD/GET divergence is not expressible in the frozen machinery. The split that
exists is the two-**GET** split and it is covered by `status-then-content-split` and `first-request-404`
(which together do attribute: a single request would give fail in the first and pass in the second).

Saturation reading: 7 of 22 cases spend their power on byte-class variants of one clause (:60/:63 exact
compare: capitalised, leading-space, trailing-space, crlf, bom, empty-200, trailing-newlines), while :49's
execution, :60's second status, :62's multi-line echo and :80's false path had no case. The case table reads
as 22 mechanisms; the grader-visible states are 15 signatures.

## 5. Four uncovered cases: prediction first, then run (4/4), plus two extras (2/2)

Predictions were written to `PREDICTIONS.md` before `run_uncovered.py` existed; the log repeats them before
any observation.

| id | fixture | predicted | observed | matched |
|---|---|---|---|---|
| `multiline-token` | curl, `200`, body `"first line\nTEST PASSED\n"` | pass | pass | yes |
| `hello-plus-second-line` | curl, `200`, body `"hello world\nsecond line\n"` | fail | fail | yes |
| `token-with-404` | curl, `404`, body `"TEST PASSED\n"` | fail | fail | yes |
| `second-request-500` | curl, sequence `[[200,"hello world\n"],[500,"hello world\n"]]` | pass | pass | yes |

Observed stdout (from `run_uncovered.log`):

- `multiline-token`: `'Content: first line' | 'TEST PASSED' | '❌ TEST FAILED…' | "Got: 'first line" | "TEST PASSED'"` — the token on the *second* body line still passes, and it is echoed twice (§2.3).
- `hello-plus-second-line`: `'Content: hello world' | 'second line' | '❌ TEST FAILED…'` — a right first line plus a surplus line is a mismatch; trailing-newline stripping does not rescue it.
- `token-with-404`: `'❌ TEST FAILED: Web server returned HTTP 404'` only — the body is never echoed; this is the control `token-in-body` lacked.
- `second-request-500`: `'Content: hello world' | '✅ TEST PASSED…'` — the content request's 500 status is ignored (`curl -s` prints the 500 body).

Extras (`PREDICTIONS-extra.md` first, `run_extras.log`): `wget-wrong-content` (wget, `"Hello World\n"`) →
fail, `'Content: Hello World' | '❌ TEST FAILED…'`, closing :80/:83; `port-8080-junk-8081-correct` → fail,
`'Content: not hello'`, closing the port confound (§2.2). Both predictions matched.

## 6. Impacted axes and the smallest safe correction

- **Coverage**: three instruction.md lines (:1-6, :10, and :7 pre-correction) and five verify.sh mechanisms
  (:49 execution, :60 second status, :62 multi-line, :63 surplus line, :80 false) had no discriminating case.
  The four executed cases close the latter three plus :60; `wget-wrong-content` closes :80. :1-6/:10/:49 stay
  unreachable (expect and git are absent by construction) and should be named, not papered over.
- **Calibration**: the receipt presents mechanism claims stronger than the runs support for 4 of 22 cases;
  the entry's requirement map should inherit the corrected labels, not the receipt wording.
- **Operability**: the probe is not importable as a library on this host's Python 3.14 — `exec_module` of a
  spec whose module is not in `sys.modules` fails at `dataclasses._is_type`
  (`AttributeError: 'NoneType' object has no attribute '__dict__'`). The shim
  `sys.modules["cgw_probe"] = P` before `exec_module` fixes it (used in both my scripts). The frozen counter
  runs the probe as a script, so C2's predicate is unaffected; any seat told to "import run_case/Case" hits
  the traceback first, as this seat did.

Smallest safe correction (probe, receipt and case table are frozen — text and follow-up only):
1. In the receipt/entry, relabel `static-file-no-git` to "a static file with no repository, hook or push
   passes; the expect step does not execute in this sandbox", and move ":49 ignores the status" to the named
   limits.
2. Relabel `wrong-port-8081` to "verify.sh:57 hard-codes :8080; anything off :8080 scores HTTP 000" and mark
   the port requirement as isolated only by the §2.2 replacement fixture (round-38 batch, not this freeze).
3. Relabel `token-in-body` / `wget-token-in-body` to "test_outputs.py:13 over the 200-branch echo (:62 and
   :68 / :79 and :85 both echo `$CONTENT`)".
4. Relabel `slow-server-3s` to "tolerates a ≥ 3 s response".
5. Fold the six executed fixtures of §5 into the round-38 case table (the frozen probe cannot gain cases
   without changing its digest and the receipt) and add requirement-map rows for :10 and the :60 second-status
   clause.

## 7. Limits of this review

- Observational, like the probe: the sandbox has no git and no expect, so no case can speak to the oracle path
  or to a failed push; every claim above is about what the grader scores with those absent.
- My six runs are not the frozen receipt and are not appended to it; they are evidence for the corrections
  above, recorded under `.ufo/waves/round-37/build/R37CritCases/`.
- No mutant analysis: this seat did not vary verify.sh itself (frozen, and C1's mutant list is about
  `pkg_gate.py`). Conclusions about a line are static-plus-observed, not mutant-confirmed.

## Evidence appendix (commands)

```
cat -n corpus/evidence/round37/tb2-git-webserver/verify.sh                    # 91 lines, :57/:59/:60/:62/:63/:68/:71/:75/:76/:79/:80/:85
cat -n corpus/evidence/round37/tb2-git-webserver/test_outputs.py              # 13 lines; :13 substring assert
cat -n corpus/evidence/round37/tb2-git-webserver/instruction.md               # 10 lines; :7 port, :9 output, :10 login
sha256sum corpus/evidence/round37/tb2-git-webserver/{instruction.md,test_outputs.py,verify.sh}
ls /usr/bin/expect                                                            # No such file or directory
python3 .ufo/waves/round-37/build/R37CritCases/run_uncovered.py               # uncovered_extra matched=4/4
python3 .ufo/waves/round-37/build/R37CritCases/run_extras.py                  # extras matched=2/2
python3 - (pair CASE/grader-stdout over git-webserver-probe.txt)              # cases: 22 distinct grader-stdout signatures: 15
```

VERDICT: cases-22-confounded-4-uncovered-extra-4/4
