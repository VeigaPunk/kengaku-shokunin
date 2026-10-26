# F37CritC2Map — semantic attack on the `## Requirement map` (C2 entry)

Seat: critic, round 37 wave 2. Target: `corpus/knowledge/tb2-git-webserver-grader.md:95-125` (the
`## Requirement map`, the section V7 machine-checks). I did not judge, edit or integrate anything; no
lane file was written.

## Method and ground truth

Every claim below is anchored on the frozen receipt plus one re-execution of the frozen instrument on a
scratch clone of the integration tip (`/fast/scratch/hyaku/kengaku-r37/F37CritC2Map`, removed).

- `git -C "$D/lane" rev-parse HEAD` → `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`; toplevel verified equal to the scratch clone.
- `python3 plans/git_webserver_probe.py --lane . --work "$S/work"` → `cases=22 observed_pass=9 observed_fail=13 mismatches=0`
  (receipt: `falsify/F37CritC2Map/probe-run.txt`, sha256 `83550712…29f8`).
- `python3 plans/round37_c2_verify.py --lane . --work "$S/work"` → `V7 ok rows=4 bad=0`, `checks=7 defects=0`, `PREDICATE C2 pass`
  (receipt: `falsify/F37CritC2Map/c2-verify-run.txt`, sha256 `d0a608ca…c934`).

So the predicate is green **and the map is still semantically wrong in two rows**. V7 only asks whether
an `enforced` row cites some case observed `fail`, an `unenforced` row some `pass`, a `partly` row one
of each — a label is never tested against *the cases that violate its line but are cited elsewhere* or
against *whether the cited case violates the line at all*. That is the hole this seat attacks.

Ground truth for the cited cases (server state from `plans/git_webserver_probe.py:69-118`, byte-equal
to the frozen dry table `corpus/evidence/round37/git-webserver-dry-cases-freeze.txt:15-22`; stdout from
my run):

| Case | State | Observed | Decisive stdout line (my run) |
|---|---|---|---|
| `static-file-no-git` | 8080 serves `hello world\n`, no repo/hook/push | pass | `✅ TEST PASSED: Content matches expected output` |
| `catch-all-200` | 8080 answers **every** path `200 hello world\n` | pass | `Content: hello world` … `✅ TEST PASSED` |
| `status-then-content-split` | 8080 answers request 1 `200 not the content\n`, request 2 `200 hello world\n` | pass | `Content: hello world` (`curl -o /dev/null` discarded the first body at `verify.sh:57`) |
| `wrong-port-8081` | 8081 serves `hello world\n`, **nothing on 8080** | fail | `❌ TEST FAILED: Web server returned HTTP 000` — byte-identical to `no-server` |
| `not-found` | 8080 answers `/hello.html` `404` | fail | `❌ TEST FAILED: Web server returned HTTP 404` |
| `capitalised` / `leading-space` | 8080 serves `Hello World\n` / `" hello world\n"` | fail | `Got: 'Hello World'` / `Got: ' hello world'` |
| `token-in-body` | 8080 serves exactly `TEST PASSED\n` at `/hello.html` | **pass** | `Content: TEST PASSED` … `❌ TEST FAILED: Content does not match expected output` … `Got: 'TEST PASSED'` |
| `wget-token-in-body` | same body, `curl` off `PATH` | **pass** | `❌ TEST FAILED: Content does not match expected output` … `Got: 'TEST PASSED'` |

## Per-row verdict

Rows: 4. Agree: 2 (`1-6`, `7`). Disagree: 2 (`8`, `9`).

### `instruction.md:1-6` | `unenforced` | `static-file-no-git` — AGREE

Lines 1–6 narrate a clone, `echo`, `add`, `commit`, `push`. `static-file-no-git` is a state in which
none of that happened (no repository exists) and is observed pass, so it is a valid violating-pass
witness: "a file served with no repository, hook or push" (`probe-run.txt`, case line). No change
required. Two notes, neither a defect: the case cannot separate "the helper ignores the git step's
status" from "the step never ran" — the entry already says so in headline finding 1 and in
§"What the probe does not show"; and `catch-all-200`, `token-in-body`, `status-then-content-split`
corroborate the same label if a second witness is ever wanted.

### `instruction.md:7` | `partly` | `wrong-port-8081`, `static-file-no-git` — AGREE (label and cases), mandatory wording fix

Does `wrong-port-8081` test line 7's port requirement or only "nothing on :8080"? **Only the latter,
strictly.** The state does violate line 7 (the web server is on 8081, not 8080) and is observed fail, so
the label survives the map's own definition. But the case carries no information the `no-server` case
does not: both print the identical line `❌ TEST FAILED: Web server returned HTTP 000`, because the
helper never contacts `:8081` (`verify.sh:57,60` hardcode `localhost:8080`). The map's prose
nevertheless reads "The port half is enforced", while the same entry's §Case independence (later in the
file) says the case "shows that an empty `:8080` fails, not that a correct body elsewhere is rejected
*as such*". The map is the section a reader — and V7 — treats as canonical, so the weaker claim must
live there. Push half free via `static-file-no-git`: correct.

Exact replacement for `corpus/knowledge/tb2-git-webserver-grader.md:116-118`:

```markdown
- **7 (that data is pushed to a web server on port 8080).** The port half holds by construction, not by
  comparison: `verify.sh:57,60` request `localhost:8080` literally, so a state serving the right body on
  8081 and nothing on 8080 fails (`wrong-port-8081`) — with the same `Web server returned HTTP 000` line
  `no-server` prints, so the case shows that `:8080` must answer, not that a port is checked (see
  §Case independence). The push half is not enforced: the passing case above serves data on 8080 that no
  clone, commit or push produced (`static-file-no-git`).
```

### `instruction.md:8` | `partly` | `not-found`, `catch-all-200` — **DISAGREE (cited case)**

The label is right; the passing case cited for it does not test this line. `catch-all-200` answers
`/hello.html` on `:8080` with `200 hello world` — that is line 8 satisfied exactly as written ("if I run
curl http://server:8080/hello.html then I see the output hello world", `instruction.md:8-9`). Its stdout
is `Content: hello world` … `✅ TEST PASSED`. A catch-all server violates nothing in line 8; it violates
only an inferred *routing-specificity* requirement the instruction never states. So the row's "shown
free for another [clause]" half rests on a clause that does not exist, and the prose sentence "the
request is never varied: a server answering **every** path with `hello world` also passes" argues against
a requirement the line does not carry.

A genuine violating-pass for line 8 is already in the receipt: `status-then-content-split`. The first
response to the exact request the line names is `not the content` (discarded at `verify.sh:57` with
`-o /dev/null`); only the *second* fetch at `:60` returns `hello world`. A user running the line's
command once sees `not the content`, so the line is violated and the case is observed pass. That is what
`partly` should be standing on.

Exact replacement for `:106` and `:119-121`:

```markdown
| `instruction.md:8` | partly | `not-found`, `status-then-content-split` |
```

```markdown
- **8 (`curl http://server:8080/hello.html`).** One path on `localhost` is requested and a 404 there
  fails (`not-found`), but the body that request returns is never the body compared: `verify.sh:57`
  discards it and `:60` fetches again, so a server answering `not the content` first and `hello world`
  second passes (`status-then-content-split`). The hostname `server` is never used (`localhost` is
  hardcoded at `:57,60`). A server answering every path passes (`catch-all-200`) and that satisfies the
  line as written; it is **not** this row's evidence — routing beyond `/hello.html` is not a clause of
  the line.
```

(V7 stays green either way: `not-found` fails, `status-then-content-split` passes → `partly` satisfied.)

### `instruction.md:9` | `enforced` | `capitalised`, `leading-space` — **DISAGREE (label)**

This is the landing defect. Line 9 says "then I see the output `hello world`". `token-in-body` serves
exactly `TEST PASSED` and is observed **pass**: my run's stdout is `Content: TEST PASSED` … `❌ TEST
FAILED: Content does not match expected output` … `Got: 'TEST PASSED'`. The body the line requires is
absent, the comparison explicitly rejected it, and the verdict was `pass` because `test_outputs.py:13`
searches stdout for the token the body itself supplied (`verify.sh:62` echo). Under the map's own
definition of `enforced` ("a probe case that violates the requirement is observed `fail`") the row is
false: a violating state is observed pass, and it is in the same receipt the row claims to read labels
off. `wget-token-in-body` shows the same on the other branch. The entry's headline finding 2 states the
probe result correctly; the map contradicts it five paragraphs later. `partly` is the strongest label
the receipt supports.

Exact replacement for `:107` and `:122-124`:

```markdown
| `instruction.md:9` | partly | `capitalised`, `leading-space`, `token-in-body` |
```

```markdown
- **9 (the output is `hello world`).** Confirmed for every body that does not carry the verdict token:
  `capitalised`, `leading-space`, `trailing-space`, `crlf`, `bom` and `empty-200` fail (`verify.sh:63`),
  and `trailing-newlines` passes because command substitution strips newlines. Free once the body
  contains `TEST PASSED`: `token-in-body` serves exactly that string, the helper prints
  `❌ TEST FAILED: Content does not match expected output` with `Got: 'TEST PASSED'`, and the case is
  observed **pass** — the same on the wget branch (`wget-token-in-body`).
```

(V7 stays green: `capitalised` fails, `token-in-body` passes → `partly` satisfied.) Secondary fix in
the same row: the current prose names `trailing-space`, `crlf`, `bom`, `empty-200` and
`trailing-newlines` but the Receipt-cases column omits them, so none of those claims is machine-checked;
listing them keeps the row auditable.

## Why these matter beyond the prose

- The map is the entry's contract with V7 and with a reader who will not re-run the probe. Today it says
  line 9 is `enforced` while the entry's own headline finding says a body that is not `hello world`
  passes — a downstream citation of either sentence contradicts the other.
- Row 8's `catch-all-200` citation is the one place the map attributes free-ness to a requirement the
  instruction does not make, which is exactly the over-read a later round would copy.
- Row 7's "port half is enforced" is true only in the degenerate sense; without the qualification it
  invites the reading that the grader compares ports, which §Case independence retracts.

## Axes

- **Coverage** — 4/4 rows still cover `instruction.md:1-9` after the edits; ranges unchanged
  (`instruction.md:10` is the instruction's own "you don't have to worry about that", correctly unmapped
  and outside V7's `range(1,10)`).
- **Machine-greenness** — both edited rows remain V7-satisfiable from the frozen receipt
  (`not-found`/`status-then-content-split` = fail/pass; `capitalised`/`token-in-body` = fail/pass); no
  probe rerun, no new case, no receipt change is needed for either fix.
- **Honesty / no-harm** — no label gets stronger; one prose sentence that contradicts a later section is
  qualified; one citation is replaced with a case that actually tests the line. No verdict, digest,
  receipt or other section is touched.

## Evidence index

| Number | Command | Output |
|---|---|---|
| tip under test | `git -C "$D/lane" rev-parse HEAD` | `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5` |
| probe reproduced | `python3 plans/git_webserver_probe.py --lane . --work "$S/work"` | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` |
| predicate green | `python3 plans/round37_c2_verify.py --lane . --work "$S/work"` | `V7 ok rows=4 bad=0` / `checks=7 defects=0` / `PREDICATE C2 pass` |
| token body | `probe-run.txt`, case `token-in-body` | `grader-stdout: … 'Content: TEST PASSED' \| '❌ TEST FAILED: Content does not match expected output' … observed=pass` |
| wrong-port identity | `probe-run.txt`, cases `no-server`, `wrong-port-8081` | both `❌ TEST FAILED: Web server returned HTTP 000` |
| catch-all satisfies the line | `probe-run.txt`, case `catch-all-200` | `'Content: hello world' \| '✅ TEST PASSED: Content matches expected output'` |
| split body | `plans/git_webserver_probe.py:104-107` + `probe-run.txt` | request 1 `not the content\n`, request 2 `hello world\n`, observed=pass |
| instruction line numbering | `nl -ba corpus/evidence/round37/tb2-git-webserver/instruction.md` | line 7 `…webserver running on port 8080…`, line 8 `curl http://server:8080/hello.html`, line 9 `then I see the output "hello world".` |

Quotes above are from the receipts in `falsify/F37CritC2Map/` and from
`corpus/knowledge/tb2-git-webserver-grader.md:97-124`, each under 25 words.

VERDICT: req-map-2/4
