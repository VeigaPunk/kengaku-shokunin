# F41RevLesson — review of `corpus/lessons/round-41.md` (kengaku round 41, wave 2, 2026-10-26)

Seat: reviewer (leaf). Target: `corpus/lessons/round-41.md` at tip `3d0058f` — every `## Mistakes` row
(class, evidence pointer, captured-by honesty, fix falsifiability), every `## Gate` verdict (S124 and the
refused PR test file re-opened live), the `## Routed` dispositions against the tip, the census numbers.
No lane file was written except this report; scratch `/fast/scratch/hyaku/kengaku-r41/F41RevLesson`
(deleted at exit). No tool installed. External surfaces re-opened read-only (api.github.com,
raw.githubusercontent.com); no mutation anywhere.

## 1. What holds (every check that reproduced)

**Header numbers.** All reproduced from `.ufo/waves/round-41/integrate/measure-final.txt`: C1
`BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=23 survived=0
invalid=0 null_detected=0`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`,
`ADVERTISED direct=21 indirect=2 none=0` (21+2+0=23 ✓), `PREDICATE C1 pass exit=0`; C2 `checks=8
defects=0`, `PREDICATE C2 pass exit=0`. Receipt `corpus/evidence/round41/constraints-probe.txt`
(`grep -E 'cases=25|regrade'`): `regrade cases=25 differ=0`, `cases=25 observed_pass=6
observed_fail=19 mismatches=2`, the two `match=NO` rows being the carried pilot slips
(`later-valid-wed-1105`, `seconds-30`) exactly as the header says.

**Commit chain.** `git merge-base --is-ancestor` against tip `3d0058f`: baseline `e50c1345` ✓, freeze
`8ef8b4fc` (15:30:52 -03) ✓, first probe run `f774a87a` (15:31:31) ✓, wave-1 spec `fc79f2a4`
(15:35:44) ✓, landing `74513c06` (15:54:45) ✓ — order matches the header. `sha256sum -c
.ufo/waves/round-41/claims/frozen-digests.txt` at tip → 11/11 OK: nothing frozen moved.

**Mistakes row 1 (vacuous predicate).** Pointers exact: `.ufo/waves/round-40/falsify/F40CritPlanNext.md:30-33`
(run A `MUTANTS total=0 … PREDICATE C1 pass`, `exit=0`) and `:36` (`counter-vacuous.patch` = `MUTANTS = []`,
`TOTAL = 0`); `plans/round-41-claims.md:118-121` carries the mined text, `:120` the captured-by quote.
Fix verified in the frozen counter: `TOTAL = 23` / `FLOORS = {"receipts": 13, "sources": 10}` at
`plans/round41_c1_verify.py:123-124`, `floors_ok` at `:640-641`, pass clause `:642-643`. The fix is
stronger than its control: because `floors_ok` needs `TOTAL >= 1`, `sum(FLOORS.values()) == TOTAL` and
per-tool floor pairs, the round-40 two-line attack (`MUTANTS=[]` **and** `TOTAL=0`) cannot pass the
frozen counter — `control-c1-no-mutants.txt` (`BATTERY fixtures=22`, `MUTANTS total=0`,
`PREDICATE C1 fail`, `exit=1`) shows the weaker one-edit case red. Shown able to fail ✓.

**Mistakes row 2 (S10 rc-equivalence).** `claims/s10_equivalence.txt`: `S10 requested-id-absent
ref_rc=5 mut_rc=5 EQUIVALENT-BY-RC` verbatim; the driver `claims/s10_equivalence.py` really derives the
label from the two exit codes (`'EQUIVALENT-BY-RC' if rc['ref'] == rc['mut'] else 'DIFFERS'`) — decisive,
not asserted. Counter docstring records S10 NOT frozen (`plans/round41_c1_verify.py:75-77`).
`control-c1-nothing.txt` ends `survived=23` ✓. One pointer is wrong — see defect 5.

**Mistakes row 3 (S124 "published").** `plans/round-41-claims.md:21-22` ("is published as TB2.1 PR #245
(`R40PlanNext.md` §3.2)") and `:105` verbatim; capture `R41PkgRows/pr245-body.md:3` (header
`state=closed merged=false … closed_at=2026-10-08T19:02:36Z`) and `:7` ("local draft only; do not submit
without owner authorization") verbatim; the Gate quote sits at `pr245-body.md:11` (14 words ✓).

**Mistakes row 4 (witness-as-battery loophole).** `claims/control-c1-witness-as-battery.txt`: `MUTANTS
total=23 killed=23 … PREDICATE C1 pass exit=0` verbatim. Docstring limit phrase verbatim at
`plans/round41_c1_verify.py:73-74`. Battery modules declare the rule: `R41BatRcvCtl.md` "No witness
module is read, imported or copied" (verbatim) and pins its module sha; `R41BatSrcExit.md` axes item 2
"no witness import". Captured-by "Nobody — disclosed at the freeze" is honest (the claims name the limit
and control at freeze).

**Mistakes row 6 ("no committed fixture" wording).** `plans/round-41-claims.md:27` (C1 title "…and no
committed fixture demonstrates") and `:34-35` (self-assessment) vs `control-c1-witness-as-battery.txt`
kill-23/23 — the overreach is real and correctly charged to round-40's M1 class (SCORECARD round-40
wave-2 correction names it). Erratum landed: SCORECARD `## Round 41` "Erratum to the frozen claims text
(not a predicate change; `R41CritClaims` D1/D3)" ✓.

**Mistakes row 7 (forgeable frozen counter).** `R41CritC1Counter.md` §2 (A1′ "works", line 37/53), §3
(dead-site T03/T04, line 98), §4 (A2 closed — two legs) all present; `R41SentinelCounter.md` F1 (variant
readable), F2 (AF_UNIX), F3 (SysV IPC), F4 (relative argv) all present with reproduction commands;
`corpus/routed-findings.jsonl` R40-R1 note routes the repairs to a re-frozen round-42 counter ✓.
`sidechannel=0` at landing ✓ (measure-final).

**Gate S122/S123.** Capture digests recomputed: `sha256sum` in
`corpus/evidence/round41/tb2-constraints-scheduling/` → `1422b345…90c5d1` (test_outputs.py), `342def78…37b6`
(instruction.md) — equal to `plans/pkg-spec-r41.json` `rows` (exactly S122+S123, so "the two A-tier rows
are the only two the spec pins" ✓) and to the lesson's abbreviated digests. Quotes verbatim at
`test_outputs.py:143` (11 words) and `instruction.md:18` (8 words); `_EXPECTED_SHA256` at `:27-37`;
integrity `read_text()` at `:88-96` as the S123 falsification mechanism states; first-DTSTART regex at
`:135`. V1/P8 at landing: `listed=10 bad=0`, `index_rows=48 knowledge_files=48` ✓.

**Gate S124 — re-opened live (this seat, 2026-10-26 ~16:2x -03).**
`curl -sS https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls/245` → `"state": "closed"`,
`"merged": false`, `"closed_at": "2026-10-08T19:02:36Z"` — unchanged since wave 1's 15:37 -03 read. Landed
capture digest matches the anchor: `sha256sum corpus/evidence/round41/pr245-body.md` →
`8f3b04c34edeb558d8b1e45ac49462bf28fdaa3392cec03bc6ee54d30253410f`. The SOURCES row keeps "closed
unmerged at access" and "state closed, merged false, closed_at 2026-10-08T19:02:36Z"; the entry says
"closed unmerged" (`corpus/knowledge/tb2-constraints-scheduling-grader.md:337`). Flip condition not
triggered; verdict **stands**.

**Gate refused PR test file — re-opened.** `curl` of
`…/terminal-bench-2/2fd12b88…/constraints-scheduling/tests/test_event_binding_adversarial.py` → **404**
(file exists only on the closed PR; the API `pulls/245/files` lists
`tasks/constraints-scheduling/tests/test_event_binding_adversarial.py` among the PR's 4 files). No capture
of it exists anywhere in the lane (`grep -rl test_event_binding_adversarial corpus/ plans/` → only
`pr245-body.md` and the lesson itself), and no case count was executed. The refusal ("the 55 is the PR
body's claim, not a measurement") **stands**; the flip condition remains unmet.

**Gate assimilation row — recounted at tip.** `git show HEAD:corpus/SOURCES.md` ids (117) ∩
`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` ids (175) → **collide=41**, with S122,
S123, S124 in the intersection — the lesson's "collisions rise to 41 when they land" is now measured
true, not just inferred. Package unchanged: `git -C shokuknow log -1 -- merge/kengaku` → `ba6779f0
2026-10-24 10:50:02 -0300`; 65 knowledge files (`find …/merge/kengaku/knowledge -type f | wc -l`) ✓.

**Gate SOURCES-curation row.** `R41SourcesRecheck.md` §1-§3 matches the lesson exactly: `overdue` → 0
lines, 87 `cadence`, earliest due 2027-01-17; S114 open with body sha equal; S121 still open (the landed
SOURCES row still reads "open … merged false at 2026-10-26 14:04 -03"); S100 301-redirects with `main` =
`2fd12b88`; S105 raw sha equal.

**Routed dispositions against the tip.** R1 "Partly closed" is exactly right — closed halves verified
(`control-c1-hostile.txt` prints the quoted `SIDECHANNEL … tokens=/home/`, `h-host-writes.
build_write=OSError.lane_read=FileNotFoundError`, `BATTERY fixtures=1 … sidechannel=1`, and
`markers after the run: … No such file or directory`; PATH-shim vector closed per `R41CritC1Counter` §4
"two independent legs"), open halves verified (F1-F4 present in the sentinel report). R2: the round-40
modules still open with `NEUTRALIZED` (`grep -l NEUTRALIZED` hits both `crit_git_shim.py` and
`crit_ledger_selfread.py`); build-spec carries the envelope (routed-findings R40-R2 closed with its check).
R3: SKILL.md has `sources-adopt` at `:573` (eight exit codes), the four new rows (`round41-c1-mutants`,
`round41-c2`, `constraints-probe`, `round-close-check`) and the "Round-41 registry addendum" at `:649`;
`R41RoundCloseMut` verdict "residuals-remeasured-14-still-open-14" matches "14 still open"; order gate
green at landing too (`measure-final.txt` `ORDER RESULT PASS exit=0` with `freeze=8ef8b4f…` before
`receipt_commit=f774a87…`). R4: `ADVERTISED direct=21 indirect=2 none=0` in both cited controls ✓.
R5: order-class blocked (routed-findings R39-R3 `status: blocked`, 5 rows in `corpus/defects.jsonl` ✓);
the F39 trio has no wave-1 work item ✓ (R39-R4/R40-R5 open); `--work` fix verified
(`round41_c2_verify.py` creates `--work`, measured by R41RevC2Counter with the round-40 contrast
traceback); W04 instruction discharged — the lesson census prints 15 `W04` and SCORECARD round 41 prints
"census exit 0 (15 `W04`, unchanged)" (SCORECARD:1556).

**Census.** Row counts by the lesson's own command (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`):
baseline `e50c1345` = 114, landing `74513c06` = 117, tip = 117 — "114 → 117" ✓. `grep -c W04`:
census-before.txt = 15, census-after.txt = 15 ✓, both `exit=0`, `kengaku ok`. Live re-run of
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kengaku` at tip → rc=0, `kengaku ok` ✓. S122/S123/S124 rows landed `mined`, tier A/A/B, used-by the entry
(census E11-clean) ✓. PROVINCE has 3 `constraints-scheduling` mentions; README has 4 incl. the §Frontier
"7 of 89 read" narrowing (README:356) ✓.

**Falsifiers section.** Summaries match the cited reports: `R41CritPytest` (real pytest 8.4.1 via
`uvx -p 3.13`, layout `/tests` + `/app` + ctrf; VERDICT "pytest-parity-25/25"); `R41CritIndep`
(`AGREE 25/25 disagree=0` + extras `dtend-tzid-only`, `first-conflicting-decoy`,
`alice-wed-1000-shifted-1100` all agreeing); `R41RegistryRows` (C1 `fixtures=0 … survived=23` fail at
`fc79f2a4`; C2 `defects=4` V2/V3/V4/V7 with V8 ok; tip-receipts `equal bytes=5775`, `receipts=27
byte_equal=7 differ=0`). One omission — defect 8.

## 2. Defects

**D1 (medium) — row 5's transcript citation is unverifiable and self-inconsistent.** Evidence column:
"Seat transcript (`R41CritIndep` session, tool call at 18:42:23Z: `rm -rf -- /fast/scratch/hyaku/kengaku-r41`)".
Greps over `history://R41CritIndep`: pattern `rm -rf -- /fast` → **no match** (the only round-root
reference outside the prompt rules is an `ls /fast/scratch/hyaku/kengaku-r41/`); pattern
`18:4[0-9]:[0-9]{2}|2026-10-26T18` → **no match** — the transcript carries no timestamps at all in the
form the lesson cites. Meanwhile the class column says "at 15:42:24 -03" (= 18:42:24Z), so the lesson
itself gives the same call two timestamps 1 s apart, and siblings spread further (`R41CritClaims.md:6-7`
"at 15:42:24"; `R41RegistryRows.md` §8 "at 15:44 local that directory was emptied";
`R41SentinelCounter.md` §4 "between 15:41 and 15:42"). The incident is real — three sibling reports
independently record it, and `R41RevC2Counter.md:82` records a mid-run "external deletion" race that
DEFECTed cleanly — but the lesson's specific citation (exact command + timestamp from the transcript) is
not verifiable from the transcript as rendered. Cite the corroborating sibling reports instead, or quote
the transcript line that actually exists.

**D2 (medium) — `disk-guard.log` is unresolvable.** Row 5's "(not the reaper)" exclusion says
"`disk-guard.log` has no `kengaku-r41` line". No file named `disk-guard.log` exists at any location I can
reach: `find /fast /home/vgpnk /var/local /srv -maxdepth 4 -name '*disk-guard*'` → only
`/fast/scratch/hyaku-run8/disk-guard.keep` and `disk-guard-dryrun.log` (a different run's tree). Either
name the log's absolute path, or drop the exclusion — as written it cannot be checked. (If the log lived
under the wiped round root, the claim is unfalsifiable for a second reason.)

**D3 (medium) — the baseline first-attempt line does not exist in the cited file.** Row 5: "L1 baseline
`integrate/measure-baseline.txt` first attempt ended with `registry_rows= knowledge_files=0` and was
re-run". `grep -n registry_rows` over that file → exactly one hit, line 725:
`registry_rows=114 knowledge_files=47 index_rows=47` — the successful run. `grep -rn knowledge_files=0
.ufo/waves/round-41/integrate/` → no match. The failed first attempt is recorded nowhere in the lane;
point the evidence at whatever does record it (L1 transcript) or cut the clause.

**D4 (medium) — the round's strongest C2 result is missing from `## Mistakes`.** `R41CritClaims.md` §1/§6
D2 demonstrated that a self-declared content-free 43-line package passes C2 8/8 (`PREDICATE C2 pass`,
probe byte-equal) and that "none of the three named surface deliverables … is read by any check"
(PROVINCE paragraph, §Frontier 7-of-89 narrowing, S124 row). `grep -c 'filler|content-free'` over the
lesson → 0. Row 4 records the exact C1 analogue (copy loophole; "No automated check exists; a limit, not
a repair") but no C2 counterpart exists anywhere in the lesson, and the closing "New for round 42"
paragraph proposes only the S124 state-word schema check. The frozen claims named an "informed-filler
limit of V1–V7"; wave 1 confirmed it total and extended it — the lesson should carry that, symmetric with
row 4.

**D5 (low/medium) — the S10 withdrawal is mis-cited to `claims/witness-run.txt`.** Row 2 fix: "recorded
as a limit in the counter docstring and `claims/witness-run.txt`". `grep -n S10
claims/witness-run.txt` → **no match** (the file is the 22-fixture witness run only). The mis-cite
originates in the counter docstring itself (`plans/round41_c1_verify.py:77` "recorded in
`claims/witness-run.txt`") and the lesson repeats it. The withdrawal IS recorded — docstring :75-77 and
`claims/s10_equivalence.txt` — so the substance holds; the second location is wrong.

**D6 (low) — the round-42 planned heading is corrupted at tip.** SCORECARD line 1575 (raw):
`### Planned (round 42)` data walk (kengaku r41, wave 1, scout)` — a stray backtick plus the R41PlanNext
report title fused into the heading, with the whole scout report pasted beneath it. Both row-5 and row-7
fixes route "to round 42" and their landing spot (the hygiene bullet and counter-repair bullets at
SCORECARD:1643-1652) sits under this malformed heading. L1-fixable; listed because the lesson's routed
fixes point into it.

**D7 (low) — row 3's fix phrase is a splice, not a quote.** The fix cell quotes "closed, unmerged patch
proposal; no upstream issue" attributing it to `R41PkgRows.md` §3 / §5 row S124. Neither says that
verbatim: §3 says "published as an unmerged/closed patch proposal", the §5/landed SOURCES row says
"closed unmerged at access", the entry says "closed unmerged" (`:337`). All three surfaces say the right
thing; the composite quoted phrase matches none of them.

**D8 (low) — the R41CritIndep bullet drops that report's own caveat.** The lesson's Falsifiers section:
"built an independent slots model and reproduced the receipt: `AGREE 25/25 disagree=0`". The report's
§2.1 states, verbatim, "not a blind prediction (receipt read first)" and a "Calibration caveat, stated
plainly". Omitted, the bullet oversells the independence of the 25/25 agreement.

## 3. Residual risk and verification gaps

- The transcript rendering available to me summarizes tool calls; if the harness stores fuller command
  text with envelope timestamps elsewhere, D1's citation may yet exist — I record what the transcript
  exposes, and the 1 s internal conflict stands regardless.
- I did not re-run either counter (L1's measure-final and `R41RegistryRows`'s envelope re-runs cover
  both; the frozen digests still check out at tip), and did not re-grade probe cases beyond the receipt
  read.
- `R41LessonDraft.md` (draft provenance in the header) was not diffed against the integrated lesson; the
  header's claim was taken as recorded, not audited.
- Wave-2 sibling seats (battery reviewers) own the C1 "uses a gameable vector?" question; my scope was
  the lesson's rows, and row 7's framing of that delegation is accurate.

Every checked pointer not listed as a defect resolved exactly, including all seven Mistakes rows' classes,
their captured-by honesty (all "None/Nobody" entries correspond to genuinely absent pre-existing rules),
and both re-opened Gate rows (S124, refused PR test file), which stand unflipped.

VERDICT: lesson-defects-8
