# F37RevEntryQuotes — entry-quote and claim re-verification, `corpus/knowledge/tb2-git-webserver-grader.md`

Round 37 wave 2 (falsify), 2026-10-26. Target: the wave-1 entry `corpus/knowledge/tb2-git-webserver-grader.md` as landed at tip `357deceb`. Method: every `## Located quotes` row re-checked with `sed -n '<n>p'` against the captures in a clean clone of the tip (`/fast/scratch/hyaku/kengaku-r37/F37RevEntryQuotes/fx/lane`, scratch deleted after); every claim sentence checked against `corpus/evidence/round37/git-webserver-probe.txt`, the capture line numbers, the probe source, and the wave-1 reports the entry cites. Receipt: `.ufo/waves/round-37/falsify/F37RevEntryQuotes/quote-check-receipt.txt`. No lane file was written.

## 1. Quote table: 32 rows, all byte-present; 3 claim cells say more than their quote

Scripted check (parse each row, `sed -n '<n>p'` the cited file, byte-compare): `rows=33 full_line=11 substring_only=21 missing=1` — the one "missing" is the table's header row; all **32 data rows** appear byte-exact inside their cited line (11 as the full line, 21 dropping leading `# `/`"""`/indentation or as an inner fragment). All 32 quotes are 3–25 words (`data_rows=32 outside_3_25=[]`). Capture integrity: `sha256sum -c SHA256SUMS` → 6/6 OK from inside the capture dir; receipt header digests equal SHA256SUMS; the three pinned raw URLs fetched at `2fd12b88` are byte-identical to the captures (digests in the receipt).

**Flags — claim cell says more than the quote (3):**

- **F1 `test_outputs.py:4`** — claim cell "the captured file is a harness template with one test". The quote ("by the test harness to evaluate the final state of the terminal") supports neither "template" (line 3's word) nor "one test" (a file property absent from the quote and the cited line). Quote verifies; label overreaches.
- **F2 `verify.sh:34`** — claim cell "the commit the helper attempts". The quoted fragment `cd server-test && echo 'hello world' > hello.html && git add hello.html` stops before the commit; `git commit -m 'Add hello.html'` sits in the same line but outside the quote. The cited *line* supports the claim; the quoted *bytes* do not.
- **F3 `verify.sh:48`** — claim cell "the git step is run without its status read". The quote is the comment `Run the expect script` (minus `# `); the status-ignored fact lives at `verify.sh:49` (`./git_test.exp`, no capture), which the static-reading table cites correctly. The quote row cites the comment line for a claim the next line carries.

Not flagged (checked, supported by quote + cited line + immediate file context): `test_outputs.py:10` (their own statement of intent; the actual assertion is the next row), `verify.sh:53` ("stands in for a readiness check" — no readiness check exists anywhere in `verify.sh`), `verify.sh:60` ("second" — ordering from :57/:60), `verify.sh:62`/`:66` ("graded stdout"/"same stdout" — cross-file context from `test_outputs.py:13`), `verify.sh:76` (`$?` attributed to wget by :75), `test.sh:18` (uvx wrapper is lines 14–17 of the same command block), `test.sh:22`/`:24` (branches of the `$?` test at :21), `task.toml:6`, `solve.sh:33`/`:37` (WEBROOT=`/var/www/html` at :36), `instruction.md:1,6,7,9,10`.

## 2. Claim sentences: 4 unsupported/defective

- **F4 (case-independence paragraph) — the critic's four post-hoc cases are misattributed.** The entry lists four items as "four cases … (4/4 matched)": token on a second line; `hello world` plus a second line; content request answered `500` with the right body; and "a wrong body on `:8080` with the right body on `:8081` fails at the content comparison". Per `R37CritCases.md` §5, the four executed cases are `multiline-token`, `hello-plus-second-line`, `token-with-404`, `second-request-500` (4/4); the :8080/:8081 item is one of the two **extras** (`port-8080-junk-8081-correct`, extras 2/2), and `token-with-404` — the control `token-in-body` lacked — is omitted from the entry entirely. Counts (4/4, extras 2/2) are right; the composition is wrong.
- **F5 (negative space) — internal contradiction on embedded newlines.** The bullet "The 22 cases are the claim's whole surface" lists "a body with an embedded newline that command substitution keeps" among states "not covered and are not claimed"; the entry's own case-independence paragraph (and `R37CritCases.md` §5 `multiline-token`, §6 ":62 multi-line" closed) reports exactly that state run and matched post-hoc. One of the two passages is wrong as written.
- **F6 (recheck clause + falsifier (a)) — the `sha256sum -c` invocation fails as written.** The clause says to run `sha256sum -c corpus/evidence/round37/tb2-git-webserver/SHA256SUMS` alongside `plans/git_webserver_probe.py --lane .`, i.e. from the lane root. `SHA256SUMS` lists bare filenames, so `-c` resolves them against CWD: from the lane root the command prints 6× `FAILED open or read` (verified); from inside the capture dir it prints 6× OK (verified). A literal recheck would spuriously fire falsifier (a) on a healthy capture. The clause needs `sha256sum -c` run from the capture dir (or `--directory`-style paths in the sums file).
- **F7 (probe description) — "PATH holding only the tools the case names" / "`PATH` is `/work/bin` (only the named tools)".** `/work/bin` also holds the five `BASE_TOOLS` (`bash`, `sleep`, `chmod`, `mkdir`, cat — probe lines 48, 222), which no case names. Literally inaccurate; the load-bearing absence claims (no `apt-get`, no `expect`, no `git`) still hold.

## 3. Verified true (evidence in the receipt)

- **Receipt fidelity**: totals line verbatim (`cases=22 observed_pass=9 observed_fail=13 mismatches=0`); all 22 `CASE` lines match the entry's group table, requirement-map labels and case ids; the freeze file `git-webserver-dry-cases-freeze.txt` carries the same 22 predictions (`predicted_pass=9 predicted_fail=13`), 1:1 with the receipt's `match=yes`.
- **Static-reading table**: every line citation checks (`test_outputs.py:11,13`; `test.sh:14-25`; `verify.sh:4-13,16-49,49,57-59,60-63,62,73-90`); `result.returncode` is never read; `./git_test.exp` at :49 has no status read anywhere downstream.
- **Structural consequences**: no `-L`/`--max-time` (lines 57, 60); `task.toml:22` `timeout_sec = 900.0`; two separate requests; trailing-newline-only normalisation — each backed by the named receipt cases (`redirect-301`, `slow-server-3s`, `status-then-content-split`, `trailing-newlines`/`trailing-space`/`crlf`/`bom`).
- **Probe mechanics**: digest `63cb75cf…5eedf` == `frozen-digests.txt:3`; bwrap `--unshare-net`, `/usr` ro, `/tests` ro-bind, `expect`→`/dev/null`, `HOME=/work/home`, direct import+call, `AssertionError`→fail / return→pass — all as stated (probe lines 204-215, 235, 172-181).
- **Headline findings**: both bounded exactly as the receipt shows, including the honest "static reading, not an observation" caveat citing `R37CritCases` §2.1 (which exists and says precisely that), and the `:62`/`:68` double-echo attribution (line 68 is `echo "Got: '$CONTENT'"`).
- **Cross-references**: `benchmark-verifier-execution-model.md:104` carries the quoted sentence (cited :104-112); `webarena-task-spec-audit.md:6,41`; `benchmark-grader-semantics.md` is the Toolathlon entry; SOURCES rows S100/S111–S114 match the entry's source block; README index row (:70), coverage bullet (:261) and frontier partial (:288, "3 of 89 read") all present.
- **"89 tasks carry `tests/test.sh` at `2fd12b88`"**: independently confirmed via the GitHub tree API — `truncated: False`, 89 top-level dirs, `tasks_with_tests_test_sh: 89`, none missing. (The wave-1 scout had counted task dirs only; the entry's stronger phrasing is nonetheless correct.)
- **Prior art**: `tb21-issue-133-body.md:39` is exactly the quoted sentence; `R37ScoutUpstream.md` §3 confirms the TB2.1 `verify.sh` DIFFERS (SSH-key auth, `git@`→`user@`, expect/wget removed); `R37ScoutPriorArt.md` confirms class published (6 hits) / instance not found ("Hits that name the O1 instance: 0") — the entry's "replication, not a discovery" and "no novelty claim" both follow.
- **Byte-equal second run**: `R37ProbeRerun.md:108` `gate: P10 ok probe_rerun=byte-equal bytes=8443`; the rerun seat's R1 caveat (text-mode compare, 8443 chars vs 8529 bytes) does not weaken the entry's claim — decoded equality of two UTF-8 renderings implies byte equality.

## 4. Minor notes (not counted)

- "The install step and the git step therefore fail with `command not found`" — exact for `apt-get` (off PATH); the git step's failure mode is an exec failure of the expect shebang (`/dev/null`), not literally "command not found". Direction (both fail, status unread) holds.
- Disclosure compression: "discarded its output unread" vs `round-37-claims.md:6-9` "the gate compared its output with the hand-typed receipt and discarded it … no verdict was printed or read" — the gate byte-compared the output (comparison failed); no seat read a verdict. Substance preserved.
- "nothing below rests on it" (solve.sh, tier C) — two quote-table rows below cite solve.sh; they are orientation quotes about the oracle itself, consistent with "read only for orientation".

## 5. Residual risk / gaps

- The entry's disclosure that predictions were "written … before the first run" rests on the freeze file and the claims file's freeze statement; I did not re-derive the freeze ordering beyond those artifacts.
- `R37ScoutUpstream.md`'s other upstream numbers (TB2.1 91 task entries unreconciled, SpecPi rates) are the scout's own reads, not re-verified here — out of this seat's scope.

## 6. Verdict basis

Quotes: 32 rows checked, 29 fully OK (quote byte-present **and** claim cell supported by quote + cited line), 3 flagged (F1–F3). Claims: 4 unsupported/defective prose sentences (F4–F7). No quote is fabricated or mislocated; no receipt number disagrees with the entry; the defects are label overreach, one misattributed case list, one internal contradiction, one broken recheck command, and one wording inaccuracy.

VERDICT: entry-quotes-29/32-claims-4-unsupported
