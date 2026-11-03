# Round 63 — FreezeReview (attack on the frozen claims doc)

Seat: FreezeReview (reviewer). Target: `plans/round-63-claims.md` (committed in `9ebde3a7`), read only.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. No lane file edited. Doc not edited.
Git used: read-only only (`cat-file -t`, `rev-parse`, `log`, `ls-files`). No mutating command.
Tools installed: none. Scratch `/fast/scratch/hyaku/kengaku-r63/FreezeReview/` removed on exit.

## Verdict

**freeze-needs-amendment.** Two blockers: the C2 pass criterion is stated three different ways, and the C1
coverage counter is a literal that is written whether or not the probe passes. Both must be amended (as a new
dated section, per the doc's own rule at line 6) before any scored receipt is read as a result.

## Counts by severity

| severity | count | ids |
|---|---|---|
| blocker | 2 | FR-01, FR-02 |
| major | 14 | FR-03 … FR-15, FR-24 |
| minor | 8 | FR-16 … FR-23 |
| total | 24 | |

Doc amendment needed before data: all blockers and majors except FR-09 (fix is in the wave spec, not the doc).

## Checks that passed (evidence, so the gaps are not read as blanket failure)

- Control receipt hash: `sha256sum corpus/evidence/round63/control-k2.txt` → `73f1fa330f02eecc9825e5538cb63c6d9fb76a404cb8a33ee067f408259100c9`, equal to the doc (line 75). Content line 5 is `CONTROL-LEG test_api F CalledProcessError …`, equal to doc line 74; line 6 `rc=0`.
- Grader pin: `sha256sum corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` → `82c6351722…be4c`; doc line 31; `SHA256SUMS` line 134 (`sed -n '130,137p'`) → same hash.
- test.sh pin: `sha256sum …/pypi-server/tests/test.sh` → `d2b1220e…e7784e` = `SHA256SUMS` line 135 (see FR-18 for the doc omission).
- S228 recon copy `.ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py` → `82c6351722…be4c` (matches the pin).
- Grader code (`cat -n …/test_outputs.py`): `install()` uses `check=True` (lines 52, 57–62), so K4 → `CalledProcessError` and `test_api` asserts four values (lines 85–88), so K3 → `AssertionError`. The leg rule (line 54) and K3/K4 expectations (lines 51–52) match the code.
- Census: `grep -cE '^CLASS [^ ]+ count=[0-9]+' corpus/evidence/round62/class-survey.txt` → 16; `network-service count=8` (line 11) with the eight members in the doc's order; `container-image count=0`. C2 row count (16) and count cells are consistent with the receipt.
- `executed17.lst` contains no network-service member, so network-service is unexecuted at base (matches line 14).
- pip trust policy, observed: with a live loopback index started and killed by its own PID (`python3 -m http.server 8081 --bind 127.0.0.1`, `pip install --index-url http://localhost:8081/simple vectorops==0.1.0`, stderr captured), pip printed no "not a trusted or secure host" warning. So an `http://localhost` index is not blocked by pip's policy; K1 is not structurally infeasible for that reason (a K1 F would come from the probe, not pip trust).
- Base tip: `git rev-parse c78749a5` → `c78749a565dfd186f10a1d8ac98e19dac2429666` (the commit exists); the doc's short form `c78749a5` (lines 3, 109) resolves; see FR-09 for the 41-character string in the wave spec.

## Findings

### FR-01 — blocker — C2 pass criterion stated three ways (not one sentence)

- Doc line 101–103: `(b) every count cell equals the receipt's count …; (c) every backticked repo-relative path in the section resolves (test -e from the lane root); and (d) the resolution share is ≥ 90 %.`
- Doc line 111–112 kill rule: `Resolution <90 % → miss.`
- Wave spec, item GateBuild, bullet `depth` d: `pass requires share >= 0.90 and total > 0. Each row's receipt-pointer cell must contain at least one such token, and it must resolve.`
- Consequence: a section with one unresolved path in twenty passes the counter (share 0.95) and fails doc (c) ("every … resolves"). A row whose pointer resolves only for a different path also differs across the three texts. The doc's "every" is a universal clause that the counter does not enumerate (attack (a)).
- Commands: `grep -n 'every backticked' plans/round-63-claims.md` → `102:`; `grep -n '≥ 90' plans/round-63-claims.md` → `103:`; the GateBuild text via `python3 -c` over `.ufo/waves/round-63/w1-spec.json` (item GateBuild).
- Amend before data: **yes** (Amendment A1 §5 below).

### FR-02 — blocker — C1 coverage counter is a literal, independent of the probe outcome

- Doc line 63: `Coverage counter: grep -c 'CLASS network-service executed=1' corpus/evidence/round63/pypi-probe.txt → 1.`
- Wave spec, item PypiProbeBuild, Change, receipt bullet: `… CLASS network-service executed=1; PREDICATE R63-C1 pass|fail; …` The `executed=1` value is written as a fixed string. Only the PREDICATE token is a pass|fail placeholder. The `--check-receipt` item only requires "the CLASS line present".
- Consequence: any receipt the probe writes — including one where K1 = F, or a do-nothing K2 run — satisfies the counter `grep -c … → 1`. This is the attack (b) case: the coverage counter is satisfied by the writer, not the claim. The coverage score is the claim's stated axis effect (line 14).
- Commands: `grep -n 'coverage counter' plans/round-63-claims.md` → `63:`; `python3 -c` over w1-spec.json, item PypiProbeBuild, receipt bullet.
- Amend before data: **yes** — `executed=1` only iff K1 observed = P (A1 §1(iv)).

### FR-03 — major — C1 predicate is not the same sentence in doc, probe check and wave

- Doc line 56–59 (one sentence): `pass iff the observed leg vector over K1–K4 equals the frozen vector P/F/F/F, AND K2's captured pip stderr names localhost:8080, AND K1's receipt records the index server's own PID and the served wheel's sha256.` The doc says this sentence is "the same in the plan, the probe's `check` and the receipt" (line 56).
- Wave spec, item PypiProbeBuild, `--check-receipt` bullet: `requires observed == expected == P/F/F/F, K2 stderr_mentions_8080=True, K1 index_pid and wheel_sha256 non-empty, the CLASS line present, and the GRADER sha line equal to the frozen sha.`
- Differences: (i) the probe also requires `expected` equality (not in doc); (ii) the probe requires the CLASS line and the GRADER sha line (not in the doc sentence); (iii) doc says "the served wheel's sha256" (a value equal to the served wheel), the probe says "non-empty" (any text); (iv) the doc does not state the `expected` vector source.
- Commands: `sed -n '56,59p' plans/round-63-claims.md`; `python3 -c` over w1-spec.json, item PypiProbeBuild.
- Amend before data: **yes** (A1 §1 gives the single sentence).

### FR-04 — major — K1 receipt check is self-attesting; "re-derivable" claim does not hold

- Doc line 58–59: `K1's receipt records the index server's own PID and the served wheel's sha256`. Doc line 62: `(re-derivable from committed bytes)`.
- Wave spec `--check-receipt`: `K1 index_pid and wheel_sha256 non-empty` — a receipt that only contains those fields with any text passes; the check does not recompute the wheel sha from the frozen literal sources, and does not verify the pid belongs to a process the probe started.
- Consequence: a hand-written receipt satisfies the C1 predicate. The "re-derivable" wording in doc line 62 overstates what the counter does (it re-reads receipt lines; it does not re-derive).
- Not-run: the probe is not built at this freeze review; this is read from the spec text. Recorded as a spec-level finding.
- Commands: `sed -n '58,62p' plans/round-63-claims.md`; `python3 -c` over w1-spec.json, item PypiProbeBuild, `--check-receipt` bullet.
- Amend before data: **yes** (A1 §1(iii): recompute the wheel sha; `owned=True` for the pid).

### FR-05 — major — K2 stderr clause is not discriminating (satisfiable by a do-nothing run)

- Doc line 57: `K2's captured pip stderr names localhost:8080`.
- Control receipt `corpus/evidence/round63/control-k2.txt` line 5 contains `localhost:8080` only inside the `CalledProcessError` repr (the echoed argv `'http://localhost:8080/simple'`), not in pip's own stderr.
- My pip run with NO listener on 8081 (`pip install --index-url http://localhost:8081/simple vectorops==0.1.0`, stderr captured): line 1 of output was `Looking in indexes: http://localhost:8081/simple`, followed by five `Connection refused` retry warnings and `ERROR: No matching distribution`. pip names the index URL in stderr whether or not anything listens.
- Consequence: `stderr names localhost:8080` is true for a do-nothing K2 and for any index the probe points pip at. The clause adds no discrimination. The discriminating fact is the refused connection, which the clause does not require.
- Commands: `cat -n corpus/evidence/round63/control-k2.txt` (line 5); pip trial in scratch, output `Looking in indexes: http://localhost:8081/simple` (own server pid was started and killed).
- Amend before data: **yes** (A1 §1(ii): require `Connection refused` / `NewConnectionError` in the separate K2 pip stderr file, and `localhost:8080`).

### FR-06 — major — "no network beyond loopback" contradicted by the sandbox design

- Doc line 42–43: `The sandbox's python is a probe-owned venv; no host pip config, no host credentials, no network beyond loopback.`
- Wave spec, item PypiProbeBuild, Sandbox bullet: `Network stays shared so 127.0.0.1:8080 is reachable.` The bwrap argv has no `--unshare-net`. A shared network namespace is not "loopback only". The universal "no network beyond loopback" is not enumerated by anything and is false under the stated design (attack (a)).
- Commands: `sed -n '42,43p' plans/round-63-claims.md`; `python3 -c` over w1-spec.json, item PypiProbeBuild, Sandbox bullet.
- Amend before data: **yes** (A1 §3).

### FR-07 — major — foreign-listener universal clause not enumerated; port-occupied outcome undefined

- Doc line 70: `Any seat finds the probe reaching a foreign service on 8080 → predicate fails.` The predicate sentence (lines 56–59) has no foreign-listener clause and the check cannot observe one (see FR-04).
- Wave spec: a port-occupied pre-bind exits 2 with `SETUP port-8080-occupied` and writes no receipt. The doc does not say whether a no-receipt run is a miss, nor whether a re-run after the listener exits is allowed. A re-run after an unexplained listener clears is an unrecorded retry.
- Commands: `grep -n 'Any seat finds' plans/round-63-claims.md` → `70:`; spec text (PypiProbeBuild, Sandbox/Cases bullets).
- Amend before data: **yes** (A1 §4).

### FR-08 — major — receipt paths disagree between the doc and the wave

- Doc: C1 receipt `corpus/evidence/round63/pypi-probe.txt` (lines 62, 63, 81); depth-before `corpus/evidence/round63/depth-before.txt` (line 109); trio-red `trio-red.txt` (line 148, no directory).
- Wave spec: C1 receipt `.ufo/waves/round-63/w1/build/pypi-probe.txt` (PypiProbeBuild, Acceptance 2); depth-before `.ufo/waves/round-63/w1/gate/depth-before.txt` (GateBuild, Acceptance 3); trio-red `.ufo/waves/round-63/w1/gate/trio-red.txt` (GateBuild, Acceptance 2). DepthTableDraft also reads `.ufo/waves/round-63/w1/build/pypi-probe.txt`.
- Consequence: the doc's counting commands read paths the wave never writes, so a literal run of the doc command fails for a reason unrelated to the claim. Nothing in the doc says the L1 copies the wave file into `corpus/evidence/round63/`.
- Commands: `grep -n 'corpus/evidence/round63' plans/round-63-claims.md`; `grep -n 'w1/build\|w1/gate' .ufo/waves/round-63/w1-spec.json` (run as `python3 -c`, since the spec is JSON).
- Amend before data: **yes** (A1 §7: the wave file is copied to the corpus path; the doc's counting commands are binding).

### FR-09 — major — 41-character base hash in the wave spec does not resolve (doc is correct)

- `grep -c '565dfd' plans/round-63-claims.md` → 0. `grep -c '565dfd' .ufo/waves/round-63/w1-spec.json` → 3 (context "base tip c78749a5565dfd…", GateBuild `git show c78749a5565dfd…:SKILL.md`, and the dispatch file).
- `git cat-file -t c78749a5565dfd186f10a1d8ac98e19dac2429666` → "Not a valid object name" (41 characters). `git rev-parse c78749a5` → `c78749a565dfd186f10a1d8ac98e19dac2429666` (40 characters).
- The GateBuild before-state command and the ClaimFalsifier command use the invalid form, so the base SKILL.md cannot be extracted as written.
- Doc needs no amendment (it uses `c78749a5`). Wave spec must be corrected: use `c78749a5` or the 40-character hash. Not a doc amendment, because the doc's predicate is unchanged.
- Commands: `printf '%s' c78749a5565dfd186f10a1d8ac98e19dac2429666 | wc -c` → 41; `git -C <lane> cat-file -t <41-char>` → fatal; `git -C <lane> rev-parse c78749a5`.

### FR-10 — major — C2 causal separation is false

- Doc line 17–19: `C2 artifacts = the SKILL.md section and the depth checker. They share no artifact except the census receipt, which C2 reads and C1 does not write.`
- Doc line 92–93: executed-status "plus `pypi-server` if C1 passes"; line 96: recipes cite `plans/round63_c1_pypi_probe.py`; wave spec DepthTableDraft: the network-service cell reads `.ufo/waves/round-63/w1/build/pypi-probe.txt`.
- The C2 table depends on the C1 receipt for one cell, and cites the C1 probe for a recipe. The "share no artifact" sentence is false.
- Commands: `sed -n '17,19p;92,96p' plans/round-63-claims.md`.
- Amend before data: **yes** (A1 §6).

### FR-11 — major — executed-status column has no rule and no check

- Doc line 91–92: `executed-status (from executed17.lst, plus pypi-server if C1 passes)`. The rule (class-level? member-level?) is not stated. Predicate (a)–(d) (lines 100–103) does not check this column.
- Wave spec DepthTableDraft: class is `executed` if at least one member appears in executed17.lst; network-service is `executed` only if K1 = P in the receipt. The doc does not carry this rule.
- Consequence: an arbitrary executed column passes the C2 counter.
- Commands: `sed -n '91,92p' plans/round-63-claims.md`; `python3 -c` over w1-spec.json, item DepthTableDraft.
- Amend before data: **yes** (A1 §6).

### FR-12 — major — trio gate checks key presence only; the CORPUS rule requires more

- Doc line 122–124: the gate passes iff the three keys appear in order within 12 lines before the first `## `.
- Fleet `CORPUS.md` (`/home/vgpnk/Projects/shokunin/CORPUS.md`, lines 163–170): `source:`, `verified-at:` and `recheck:` come first; "when the source is external, `source:` cites its `S###` row in `corpus/SOURCES.md` alongside the URL and anchor."
- Consequence: a file with three empty keys (`source:`, `verified-at:`, `recheck:`) passes the gate. Nothing checks values, the S### row, or a date format. The gate passes a trio in name only (attack (b)).
- Not-run: the gate is not built at this review; read from the frozen rule text and the spec's trio bullet.
- Commands: `sed -n '122,124p' plans/round-63-claims.md`; `sed -n '163,170p' /home/vgpnk/Projects/shokunin/CORPUS.md` (read-only); `grep -rlE '^verified-at:' corpus/knowledge | wc -l` → 36 (lane-wide, context only).
- Amend before data: **yes** (A1 §8).

### FR-13 — major — control receipt has no producing command

- `corpus/evidence/round63/control-k2.txt` (6 lines) states the leg result but not the command, environment, venv path, or stderr capture. Doc lines 72–76 describe it in prose ("the grader's test_api run with the venv on PATH") with no command.
- Only one file exists in `corpus/evidence/round63/` (`ls -la`), and no committed script produces it (`git log --oneline -- corpus/evidence/round63/control-k2.txt` → only `9ebde3a7`).
- The brief requires "every observed value carries the command that produced it". The control's line 5 is produced by a harness that is not committed.
- Commands: `ls -la corpus/evidence/round63/`; `git -C <lane> log --oneline -- corpus/evidence/round63/control-k2.txt`; `cat -n corpus/evidence/round63/control-k2.txt`.
- Amend before data: **yes** (A1 §9: the K2 leg of the probe battery is the control of record for C1; the producer of control-k2.txt is recorded as unknown).

### FR-14 — major — ss -ltnp before-state receipt is absent

- Doc line 35–36: `The host has no listener on 8080 at round start (ss -ltnp → none)`. Doc line 148: `C1 host state (ss -ltnp shows no 8080 listener, recorded in .ufo/waves/round-63/w1/recon/)`.
- `ls .ufo/waves/round-63/w1/recon/` → only `S228-pypi-test_outputs.py` and `S229-pep-0503.html`. No ss output is recorded.
- The current host (not round start) shows no 8080 or 8081 listener: `ss -ltn | grep -E ':8080 |:8081 '` → none. That does not substitute for a round-start receipt.
- Amend before data: **yes** (A1 §10: record the receipt before the battery, or withdraw the citation).

### FR-15 — major — a K1 server left running makes K2 return P, which fires the kill rule spuriously

- Doc line 66–67: `K2 returns P … → the claim is dead and the round reports it.`
- Wave spec: `Between cases: … stop the server by PID` — no check that 8080 is free before K2 starts. If the K1 server survives, K2 is served by the K1 index (which serves the correct wheel) and returns P. The kill rule then fires for a harness fault.
- Amend before data: **yes** (A1 §4: bind-test 8080 before each case; a listener the probe did not start is a SETUP stop, not a leg).

### FR-16 — minor — "committed receipt" overstates the state at freeze

- Doc line 126: `Red-before (committed receipt): trio … → exit 1`. No `trio-red.txt` exists at freeze; the directory listing shows only `control-k2.txt`. The receipt is a future output, not committed.
- Amend before data: **yes** (wording only; A1 §8 handles the receipt location).

### FR-17 — minor — CORPUS.md citations do not resolve from the lane

- Doc line 21: `Frontier step (CORPUS.md rule 1 / §2b)`; line 124 quotes the rule. No `CORPUS.md` in the lane (`find <lane> -name CORPUS.md` → none). It lives at `/home/vgpnk/Projects/shokunin/CORPUS.md`. `grep -n '2b\|§2' /home/vgpnk/Projects/shokunin/CORPUS.md` → no hits: `§2b` is not a section of that file.
- Amend before data: **yes**, wording only (A1 §11).

### FR-18 — minor — test.sh pin absent from the doc

- Doc names only `test_outputs.py` (lines 30–32). `SHA256SUMS` line 135 pins `./pypi-server/tests/test.sh` at `d2b1220e…e7784e`; the file on disk matches. The probe runs `test_outputs.py` only, so the omission has no effect on the predicate.
- Amend before data: no predicate change; record the pin for completeness (A1 §12).

### FR-19 — minor — control and doc share one commit

- `git log --oneline -- corpus/evidence/round63/control-k2.txt` and the doc both → `9ebde3a7`. The doc says the control was "run before this freeze" (line 72). Git cannot show the ordering inside one commit.
- Amend: record the control's run time in A1 §9 or accept as unverifiable.

### FR-20 — minor — S229 not pinned

- Doc line 142–143 gives no hash for S229. `sha256sum .ufo/waves/round-63/w1/recon/S229-pep-0503.html` → `5b97cb7e14fc1a384bdfaac70195763e0b3bfca5a4c5f70142c6e37d2c453c4f`. Title in the file: `PEP 503 – Simple Repository API`.
- Amend: record the pin (A1 §13).

### FR-21 — minor — placement wording differs from the wave

- Doc line 88–89: "placed after the existing benchmark-selection tables". Wave context: "after the '## Decision table — minimal stack when time is tight' section". In the base SKILL.md (`grep -n '^## ' SKILL.md`) the benchmark-selection heading is line 23, minimal-stack line 53, next heading line 60. Placement is not in the predicate.
- Amend: align the wording (A1 §14).

### FR-22 — minor — pip cache isolation across cases is not frozen

- Wave spec sets `HOME=<work>/home` for every case; K1 and K2 share it. The doc does not freeze per-case cache isolation. pip's HTTP cache from K1 could, in principle, be consulted in K2. Not run at this review (the probe is not built).
- Amend: freeze a per-case `HOME`/`XDG_CACHE_HOME` (A1 §4).

### FR-23 — minor — degenerate receipt pointers pass C2

- Doc line 15: "each citing a resolvable receipt path"; line 93: "a repo path that resolves". The counter (GateBuild) requires one resolving token per row, not a pointer that names the class. The same pointer on all sixteen rows passes.
- Amend (optional): the pointer must cite the row's CLASS line or a member's receipt (A1 §5 optional clause).

### FR-24 — major — the counter's path set is narrower than the doc's "every backticked repo-relative path"

- Wave spec GateBuild `depth` d: a token counts only if it contains `/` AND ends in `.py .md .json .txt .sh .lst .yml`, or ends in `/`. A backticked path ending `.html`, `.tsv`, `.csv`, `.toml`, `.tar.gz` (or with no `/`) is outside the denominator, so an unresolved one is not counted (attack (a): the universal "every" is enumerated by an extension whitelist the doc does not state).
- Doc line 102: `(c) every backticked repo-relative path in the section resolves`.
- Amend before data: **yes** (A1 §5: any backticked token containing `/` is a path; the denominator is all such tokens).

## Amendment draft (proposed; new dated section; append to the doc, do not edit the frozen text)

```
## Amendment A1 — 2026-11-03, pre-data (FreezeReview)

Scope: appended section. No scored receipt exists yet; the only file in corpus/evidence/round63/ is
control-k2.txt (a control). This section supersedes the lines it names. The frozen text above it stands
otherwise, and every rule below is fixed before any scored run.

1. R63-C1 predicate (supersedes lines 56–59 and the wording at 62–63). One sentence, the same in the plan,
   in --check-receipt, and in the receipt:
   "PREDICATE R63-C1 pass iff the receipt shows (i) CASE K1..K4 observed legs equal P/F/F/F and each
   observed equals expected; (ii) the separate K2 pip stderr file contains both `Connection refused`
   (or `NewConnectionError`) and `localhost:8080`; (iii) K1 index_pid names a process the probe started with
   Popen (owned=True), and wheel_sha256 equals the sha256 of the vectorops-0.1.0 wheel the probe rebuilds from
   the frozen literal sources (--check-receipt rebuilds it and compares); (iv) the line
   `CLASS network-service executed=N` has N=1 iff K1 observed=P and N=0 otherwise; (v) the GRADER line
   sha256 equals 82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c."
   Coverage counter (line 63): `grep -c 'CLASS network-service executed=1' <receipt>` → 1 counts only when
   PREDICATE R63-C1 pass.

2. Kill rules at 66–70 stand. The K2-returns-P rule applies only with K1's server stopped and 8080 bind-tested
   free (see 4).

3. Sandbox (supersedes line 42–43). The bwrap sandbox shares the host network namespace (no --unshare-net),
   because the grader's fixed URL must reach the probe-owned index on 127.0.0.1:8080. The claim makes no
   isolation statement; the guarantee is (1)(iii): the listener reached is the probe's own process.

4. Port and cases (supersedes line 70). Before each case, bind-test 127.0.0.1:8080. A listener the probe did not
   start ends the run with SETUP port-8080-occupied (exit 2, no receipt), counted as a miss for that run; a
   re-run requires the cause recorded in the wave. Each case gets its own HOME and XDG_CACHE_HOME under its work
   directory. The K1 server is stopped by its own PID and the port is bind-tested free before K2 starts.

5. R63-C2 predicate (supersedes lines 100–103). PREDICATE R63-C2 pass iff, in the new SKILL.md section,
   (a) exactly 16 class rows whose names equal the CLASS names in the receipt; (b) every row's count cell equals
   that CLASS line's count; (c) every backticked token containing `/` is a repo-relative path, the share of those
   that resolve from the lane root is ≥ 0.90, and the total is > 0; (d) every row's receipt-pointer cell contains at
   least one resolving path. Optional tightening: the pointer cell names the row's CLASS line or a member's receipt.
   Kill rule (111–112): a count mismatch, a share < 0.90, or a row without a resolving pointer is a miss.
   The universal "every" in (b)/(d) is enumerated by this list; no clause is left to the counter's discretion.

6. C2 executed column and causal separation (supersedes lines 17–19 and 91–93). executed = `executed` iff any
   member of the CLASS line appears in corpus/evidence/round52/graders/executed17.lst; otherwise
   `recipe-unexecuted`. The network-service row is `executed` iff A1 (1)(iv) N=1, else `recipe-unexecuted`.
   The depth counter checks this column against this rule. C2 reads the C1 receipt for that one cell; that is the
   only shared artifact, and the causal-separation sentence is amended to say so.

7. Receipt locations (supersedes lines 62–63, 72, 81, 109, 148). The wave writes receipts under
   .ufo/waves/round-63/w1/ (build/pypi-probe.txt, gate/depth-before.txt, gate/trio-red.txt). The L1 copies each to
   corpus/evidence/round63/ (pypi-probe.txt, depth-before.txt, trio-red.txt) before the counting commands run. The
   counting commands in this doc are binding; the corpus paths are the ones they read.

8. Trio gate (supersedes lines 122–124). PREDICATE trio pass iff the three keys `source:`, `verified-at:`,
   `recheck:` appear in that order within the first 12 lines and before the first `## ` heading, AND each has a
   non-empty value: `verified-at:` and `recheck:` are ISO dates (YYYY-MM-DD) or, for recheck, a cadence word;
   `source:` cites an S### row present in corpus/SOURCES.md when the source is external (fleet CORPUS.md lines
   163–170). Red-before is the receipt corpus/evidence/round63/trio-red.txt, to be produced; it is not committed
   at freeze (line 126 wording withdrawn).

9. Control receipt (supersedes lines 72–76). corpus/evidence/round63/control-k2.txt is recorded as a control with
   no recorded producing command; its command and run time are not recoverable from git (same commit 9ebde3a7).
   The K2 leg of the probe battery is the control of record for C1.

10. Host state (supersedes line 35–36, 148). The ss -ltnp receipt is written to
    .ufo/waves/round-63/w1/recon/ss-8080.txt before the battery, with the command `ss -ltnp`. Until it exists, the
    before-state claim is not recorded.

11. Citations (supersedes lines 21 and 124). The provenance-trio rule is in the fleet CORPUS.md at
    /home/vgpnk/Projects/shokunin/CORPUS.md lines 163–170. The cited "§2b" is not a section of that file and is
    withdrawn.

12. Pin record. corpus/evidence/round52/graders/pypi-server/tests/test.sh, sha256
    d2b1220e42bcfdcce87907ac5bbd69ac210a3c94926545ca2439636786e7784e (SHA256SUMS line 135). Not executed by this
    round's probe.

13. S229 pin. .ufo/waves/round-63/w1/recon/S229-pep-0503.html, sha256
    5b97cb7e14fc1a384bdfaac70195763e0b3bfca5a4c5f70142c6e37d2c453c4f, opened 2026-11-03.

14. Placement (supersedes lines 88–89). The section goes after "## Decision table — minimal stack when time is
    tight" (SKILL.md line 53) and before "## Benchmark anti-patterns" (line 60). Placement is not in the predicate.

Wave-spec corrections (not doc amendments): the base hash in w1-spec.json (context, GateBuild, dispatch) is
`c78749a5` or `c78749a565dfd186f10a1d8ac98e19dac2429666`. The 41-character string does not resolve.
```

## Residual risk and verification gaps

- The probe, gate checker and trio gate are not built at this review. FR-02, FR-04, FR-05, FR-12, FR-15, FR-22 are
  spec-level findings; they are not run against code. Run `--check-receipt` against a fabricated receipt and the
  trio gate against a three-empty-keys file once they exist.
- The pip trust test used an empty index (no packages). It shows pip does not refuse `http://localhost`; it does not
  show that K1 installs vectorops.
- I did not run the grader, the bwrap sandbox, or any K-case; the leg-rule reading is from `cat -n` of the grader.
- Port 8080 was not touched. My loopback test used 8081 and the server was killed by its own PID; 8081 was free after the kill.
