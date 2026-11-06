author: kengaku (L1 KengakuR95, hyaku run 15 attempt 1)

# Kengaku round 95 — lesson

Lane `kengaku-shokunin`, branch `master`. Base `4524072d` (round 94 closed, lane tip at round
start); P0 mechanism predictions, capture, C2 false-gate population and BEFORE receipts `2457f025`;
instruments P1 `16dcfed7`; pre-freeze controls P2 `7783e9cb`; frozen claims F `d9cd18a7`
(`plans/round-95-claims.md`, 11-row `frozen-instruments` table); official receipt, ledger flip,
SKILL class cells and SOURCES C `afe9c229` = measured tip T; L1 receipts at T and wave spec
`ea19299d`. Wave evidence: `.ufo/waves/round-95/w1/`.

## Round-94 spot-check routed defects — disposition

| # | routed defect (round-94 spot-check §6) | round-95 disposition |
|---|---|---|
| 1 | M1/Q76: run `plans/anchor_line_check.py` before any commit carrying SOURCES rows | done: run on the working tree before C (`ANCHORLINE rows=301 … live=0 cells=0`), re-run at T (`.ufo/waves/round-95/L1/lane-gates-end.txt`); every anchor word count computed (`len(quote.split())`) by the script that wrote the rows |
| 2 | W-2/W-3/M2: the ≥9 wave-built false gates as controls under a new frozen predicate; W3 must not trust a printed SELFTEST line | **claimed (R95-C2)**: 14 false gates in `plans/round95-false-gates.tsv`; W3 now drives the battery red with three probe mutations of the gate's shared functions |
| 3 | W-4: replace refs and non-three-backtick fences | not claimed; carried to round 96 (gate v2 unchanged this round) |
| 4 | W-5/W-6: surviving gate mutants and C1 counter mutants; receipt-side positive controls not based on P1 | gate survivors M01, M02, M07, M15, M19, M20 are census rows (M04, M10, M18 excluded with reasons, tsv header); C1: receipt-side positive control on a P1 clone with a draft table (`controls/c1-pos.txt`, rc 0) and forgeries D4 (m11), D5 (m10), D6 (m03+m04), D7, D8 (`controls/README.md`) |
| 5 | legacy `plans/round79_c1_population_ledger.py` receipt-key mismatch | done (conformance): ledger rows of rounds 92–95 carry `receipt`/`subject`/`verdict`, `mteb-retrieve` subject corrected, SKILL decision-table cells set to the ledger; `DEFECTS n=14` at BASE → `n=0`, `PREDICATE R79-C1 pass` at T (`.ufo/waves/round-95/L1/legacy-r79-gate.txt`) |
| 6 | W-8 uncommitted dry-run bytes; W-10 `--work` inside the lane; SP-2 LANG | W-8: round-94 dry-run-1 is no longer cited; this round's dry run is committed with the P1 bytes it ran. W-10: the round-95 probe, C1 counter, C2 counter and census refuse a `--work` inside the lane (gate v2 itself unchanged; carried). SP-2: the round-95 probe sets `LANG=C.UTF-8` in the sandbox |
| 7 | carried round-92 items | not claimed; still open, same pointers |

The round-94 spot-check §4 recorded no disagreement (5/5 agree), so no discernment criterion is
owed from it.

## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened
here). Every fetch HTTP 200 on 2026-11-05 (19:43 -03, `.ufo/waves/round-95/L1/capture-fetch.txt`) from
raw.githubusercontent.com at terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6` and bottlepy/bottle
`0207a34f0c5716cd292dd4480253ad35d3da49f3`. Quotes and word counts were taken by the script that wrote the rows
(`len(quote.split())` over the captured line), never typed (Q76).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S303 `fix-code-vulnerability/tests/test_outputs.py` (member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200, 4010 B, sha256 `c006a5de…7f26`, byte-identical to the lane's round-52 capture | line 45: `cwe_ids = [str(cwe_id).lower() for cwe_id in cwe_ids]` (7 words) | the six functions the thirteenth replay grades: report tests key on `file_path` and lowercase each `cwe_id` (bare string iterated by character, C08; blank line breaks `json.loads`, C10); the `_hkey` tests import `bottle` after inserting `/tests/bottle` (:58–59), so a package `/app/bottle/` shadows `/app/bottle.py` (C15); no function calls `_hval` (C11) | a claim about the TB2 reward needs the original-repo suite staged (S308) |
| S304 `solution/solve.sh` | **admit** (tier A) | 2026-11-05, HTTP 200, 913 B, sha256 `7a0131b3…e03` | line 20: `{"file_path": "/app/bottle.py", "cwe_id": ["cwe-93"]}` (4 words) | the positive control, run unmodified (host bash + GNU sed): all six functions pass (C01) | a claim about another sed than GNU sed 4.9 needs its own run |
| S305 `environment/Dockerfile` (oracle-removal lines only) | **admit** (tier A) | 2026-11-05, HTTP 200, 814 B, sha256 `09174709…b3ab` | line 22: `RUN sed -i -e '1562,1563d' bottle.py` (6 words) | the two sequential deletions remove `_hkey`'s and `_hval`'s raising checks; the probe applies them offline (`VULNERABLE_BOTTLE_SHA 761756ce…2bba`; the wave's critic pulled the image and found `/app/bottle.py` byte-identical) | — |
| S306 bottlepy `bottle.py` @ `0207a34f` | **admit** (tier A) | 2026-11-05, HTTP 200, 175847 B, sha256 `abf64368…d802` | line 1562: `if '\n' in key or '\r' in key or '\0' in key:` (12 words) | the oracle the image deletes; restoring it passes all six functions (C05); normalisation is untouched by the deletion, so the do-nothing vector still passes the basic and real-world tests (C02) | — |
| S307 `instruction.md` | **admit** (tier A, agent-facing contract) | 2026-11-05, HTTP 200, 3873 B, sha256 `89b1abdf…641a` | line 18: `- The exact files and that exact CWE-ids must appear in the /app/report.jsonl file.` (14 words) | the stated contract is stricter than the graded one: `CWE-93` passes (C06), a split report passes (C09) | — |
| S308 `tests/test.sh` | **reject** | 2026-11-05, HTTP 200, 653 B, sha256 `f1611da6…b17f` | line 9: `pip install pytest==8.4.1 pytest-json-ctrf==0.3.5` (4 words) | REJECTED as a replay input: network pip install, and its first pytest run (line 12) is the cloned repository's own suite, which the replay does not stage. Wave evidence (ExecC1Rerun, CriticClaims): that suite's `test_prevent_control_characters_in_headers` fails the C11 half fix and C15 crashes its collection, so the reward is 0 in both — the rejection is right for inputs and wrong as a coverage statement | an offline copy of bottle's test tree at `0207a34f` and pinned pytest wheels |
| S309 `task.toml` | **reject** | 2026-11-05, HTTP 200, 967 B, sha256 `9aa2bd14…e1dc` | line 29: `docker_image = "alexgshaw/fix-code-vulnerability:20251031"` (3 words) | REJECTED as an input: the harness runs a prebuilt image the replay never pulls. The flip was exercised by the non-author critic (image digest `sha256:cac32525…c5c0`): `/app/bottle.py` = `VULNERABLE_BOTTLE_SHA`; the image also keeps the oracle in site-packages and in `/app/.git`, so the row stays rejected as an input and its finding moves to knowledge | — (flip met; reason now: the image holds two oracle copies the replay must model before it can be an input) |

Round-start census: exit 0, `kengaku ok`, 294 rows (`.ufo/waves/round-95/L1/census-start.txt`). Round-end census:
exit 0, `kengaku ok`, 301 rows (`.ufo/waves/round-95/L1/census-end.txt`). Anchor gate (Q76) on the tree that added
the rows, before the commit: `ANCHORLINE rows=301 cited=111 captured=98 uncaptured=13 defective=10 repaired=10 live=0 cells=0`
(re-run at T in `.ufo/waves/round-95/L1/lane-gates-end.txt`). Rows touched old → new: none (no earlier row's status,
recheck or used-by changed). Assimilation: none (`merge/kengaku/` held by L0 `kengaku | round-54`). considerthese:
none taken (latest file 2026-11-05; its residual, a root of trust outside the lane's commits, is still not implemented).

## Mistakes

Class · evidence pointer · captured-by · fix.

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | **measurement launched from the wrong cwd, again** (round-94 M4 recurring) | the first R95-C2 census and legacy-gate runs at T were `( … ) &` groups chained after `cd $S/t &&`; the `cd` bound to the first group only, so two groups ran from the fleet root: `python3: can't open file '/home/vgpnk/Projects/shokunin/plans/round95_false_gate_census.py'`, rc 2; the receipt's own header stamps `cwd /home/vgpnk/Projects/shokunin HEAD 9b93fc8f…` (`.ufo/waves/round-95/L1/mistake-M1-c2-tip-wrong-cwd.txt`) | the counter's rc 2 (could-not-evaluate is never a pass) and round-94 M4's "cwd asserted in the receipt" — asserted, but nothing checked it (ScribeLesson SL-1) | re-run with a `cd` inside every group and every script by absolute path (`c2-tip.txt`, rc 0); the seat contexts carry the absolute-path rule; **Q77** makes the stamped revision a commit of the lane, a check shown able to fail: the M1 receipt's HEAD `9b93fc8f…` does not resolve in the lane, the good receipt's `afe9c229…` does (`.ufo/waves/round-95/w1/ScribeLesson/draft-receipt-rev-check.py`) |
| M2 | **a conformance repair of a ledger row broke a standing counter that pins that row** | C `afe9c229` changed `mteb-retrieve` `subject` `tb2-result-file` → `tb2-header` (the only shape the round-79 gate accepts); `plans/round87_c1_replay.py --rev` went PASS at BASE → FAIL at T (`DEFECT L7-ledger row … "subject": "tb2-header"`; ExecLegacyHarm H1, `.ufo/waves/round-95/w1/ExecLegacyHarm/report.md`) | none in the lane; non-author wave only | reverted after T (the `subject` is back to `tb2-result-file`; `plans/round87_c1_replay.py` green again, round-79 gate `DEFECTS n=1` SUBJECT-MISMATCH — two lane gates disagree about one cell, routed to round 96 for one counter re-pin); **Q78**: before editing an existing ledger row, `git grep` the old value in `plans/*.py` and run every counter that pins it at BASE and at the edited tree. Shown able to fail: the round-87 counter's BASE/T receipts |
| M3 | **in-sample fixture fitting presented as calibration** (round-94 M2, one level up again) | R95-C2 14 → 0 reproduces, but non-author seats built new false gates that pass the round-95 counter 5/5: CriticClaims HO-A (commented table row) and HO-B (paths-mode history skipped), ExecC2Rerun g1/g2/g4/g5 (chmod-only, `.`-prefixed, gitlink, non-ASCII rows), ReviewerC2 H1/H2/H4 (hollowed battery cases; a forged counter printing the designated RED lines); and a behaviour-preserving rename turns the counter red (CriticClaims HE2, ReviewerC2 H7) | the claims file's declared in-sample scope (frozen at F) — the reading was bounded before data, the discrimination was not | routed to round 96 under a new frozen predicate; Q75's scope sentence holds (every wave-built false gate becomes a next-round control) |

Sweep for further mistakes: `grep -n "RED\|rc=2\|UNEXPECTED" .ufo/waves/round-95/L1/*.txt .ufo/waves/round-95/L1/controls/*.txt` — every hit is a designed control (README rows) or M1's receipt.

## Honest limits of this round's evidence

- R95-C1 replays the six functions of `tests/test_outputs.py` on the rebuilt `/app`, not the TB2 reward. The reward also
  needs the cloned repository's own suite (`tests/test.sh:12`), which is not staged: there C11 (half fix) and C15 (package
  shadow) score 0, so they are findings about `test_outputs.py`'s coverage, not about the reward (CriticClaims,
  ExecC1Rerun). In the real image two reward-1 states need no fix at all — delete `/app/bottle.py` (the oracle sits in
  site-packages, installed before the sed step) or `git checkout -- bottle.py` (`.git` keeps it) — and the replay's
  sandbox cannot model either (ReviewerC1 F1, CriticClaims C1-REWARD-DELETE / -GIT).
- Host Python 3.14.8 vs the image's 3.11: ExecC1Rerun re-ran all 15 cases under 3.11.17, identical vectors.
- R95-C2's 14 → 0 is the frozen in-sample measure; held-out false gates pass the counter (M3), the census credits any red
  at the designated leg (ConnectorOverlap R95-O5, ReviewerC2 C2-F1), and the M10 exclusion "no observable" is false on a
  damaged object store (ReviewerC2 C2-F3).
- The probe's sandbox inherits the invoking environment (no `--clearenv`; SentinelProbe SP1): no observed vector depends
  on it, but captured third-party code can read it.
- Standing counters pinned to an absolute executed count (`round94_c1_replay.py` L7, 38) go red when any member is
  added (ExecLegacyHarm H2; rounds 90–93 already red at BASE the same way) — disclosed, not caused by a defect here.

## Wave w1 findings (non-author seats; routed to round 96, never repaired in round)

12 seats dispatched (`.ufo/waves/round-95/w1-results.json`), **12 reported, 0 dead**. No tabled file changed after F
(ReviewerC1: 11/11 rows equal at F and T, `git log --full-history F..T -- <paths>` empty; honest W4 `(11, 11, 0)`).
Both predicates reproduced by non-author seats (ExecC1Rerun, ReviewerC1, CriticClaims: C1 rc 0; ExecC2Rerun, CriticClaims,
ScribeLesson: census rc 0). L1 handling: SentinelProbe's `receipts/outside-env-values.txt` held the host's full environment
with live credential values; the L1 replaced every value with its length before the wave commit (names kept), so no
credential material lands in the lane.

| id | seat | severity | finding | effect on a verdict at T |
|---|---|---|---|---|
| W-1 | CriticClaims verdicts | — | R95-C1 **verifies-narrowed** (six functions, byte-identical `/app/bottle.py`, not the reward); R95-C2 **verifies-narrowed** (in-sample regression count, not calibration of unseen gates) | none; both predicates reproduce |
| W-2 | CriticClaims C1-REWARD-DIVERGE; ExecC1Rerun | major (scope) | in the real image and under the repository's own suite C11 (half fix) and C15 (package shadow) score reward 0 (`test_prevent_control_characters_in_headers` fails; 25 collection errors) | none (claim scoped to the six functions) |
| W-3 | CriticClaims C1-REWARD-DELETE/-GIT; ReviewerC1 F1 | major | two reward-1 states need no fix: `rm /app/bottle.py` (site-packages holds the oracle, installed before the sed) and `git checkout -- bottle.py` (`.git` keeps it); the sandbox cannot model either | none (no tabled case) |
| W-4 | ReviewerC1 F2, F3 | minor | `hkey_basic`/`hkey_real` never F in any case (normalisation regression unexercised); replay ≠ reward | none |
| W-5 | ExecC1Rerun | info | three probe runs byte-identical; Python 3.11.17 gives the same 15 vectors | none |
| W-6 | MutTesterC1 | major | 32 counter mutants: m10, m11 newly killed by D5/D4; m01 (member-set check) LOST — this round's swap control also breaks cells; m05 (L4 read at --rev) and m13 (rc 2→1) survive and flip on held-out fixtures; the D6 kill of m03+m04 is a count coincidence | none at T |
| W-7 | ExecC2Rerun g1/g2/g4/g5; CriticClaims HO-A, HO-B; ReviewerC2 H1/H2/H4 | major | held-out false gates pass the round-95 counter 5/5 (chmod-only, `.`-prefixed, gitlink, non-ASCII and commented rows; paths-mode history skipped; hollowed battery cases; a forged counter printing the designated RED lines passes the census) | none at T (in-sample claim) — lesson M3 |
| W-8 | CriticClaims HE2; ReviewerC2 C2-F4 | major | a behaviour-preserving rename of gate v2 turns the counter red (W3/W5 byte anchors) | none at T |
| W-9 | MutTesterC2 MUTC2-1…7 | major | 20 counter mutants: 6 killed, 14 survive (13 byte-identical at T, e.g. W1/W4/W5 gating removed, W3 acceptance relaxed); census `designated_red` forced and honest clause dropped are killed only by P2 receipts | none at T |
| W-10 | ExecC2Rerun N1, N2; ReviewerC2 C2-F3 | major (latent) | gate v2 itself: `git replace` hides an edit (rc 0), a symlink instrument hashes the link text; M10's "no observable" exclusion is false on a damaged object store | none at T (0 replace refs, no symlinks, intact object store) |
| W-11 | ReviewerC2 C2-F5, C2-F6; ConnectorOverlap R95-O5 | minor | the M04 exclusion's "equivalence" is wrong (crash on an absent-at-freeze row, cannot turn a breach into a pass); M18 exclusion justified; census credits any red at the designated leg | none |
| W-12 | ExecLegacyHarm H1, H2 | major / minor | H1 the `mteb-retrieve` subject repair turned `plans/round87_c1_replay.py` PASS → FAIL (lesson M2; reverted after T); H2 `round94_c1_replay.py` pins `executed_rows=38` and goes red with any new member (rounds 90–93 already red at BASE) | none on round-95 claims |
| W-13 | SentinelProbe SP1–SP5 | major / minor | SP1 the sandbox inherits the full environment (no `--clearenv`; fix verified on bwrap 0.13.1); SP2 `/etc` readable; no host writes, zero AF_INET sockets, no lane bind | none (environment enters no observed vector) |
| W-14 | ScoutSources | info | S303–S309 re-opened live: 7/7 HTTP 200, sha256 = row = capture, quote on the cited line, word counts exact; the prebuilt image's anonymous config history carries exactly the two sed lines | none |
| W-15 | ScribeLesson SL-1…SL-5 | major / info | SL-1 the M1 receipt's stamped HEAD resolves in no lane (adopted as Q77); SL-3 claims file: "sha256 equal to the table above" holds for 4 of 7 rows (instruction, test.sh, task.toml are not tabled instruments) | none |
| W-16 | ConnectorOverlap R95-O1…O7 | info | no sibling replays a TB2 grader; kaidoku round 100 independently builds forgery controls (complement); PROVINCE.md holds | adjacency note |
