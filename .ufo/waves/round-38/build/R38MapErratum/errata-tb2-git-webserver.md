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
