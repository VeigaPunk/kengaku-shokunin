# Round 60 verifier spotcheck — kengaku (hyaku run 14)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Closed 2026-11-02 against lane tip `e33ab0bdfcf6eb16a0d24aa8651ef7f200f04e9e` (branch
`master`, pushed), base `9482c8408f62`. Host note honored: the lane's frozen instruments run
in WSL Ubuntu-24.04; CLOSURE-PREP was present in the round report, so BOTH claims were
**re-derived by execution** in WSL Ubuntu-24.04 (python 3.12.3, bwrap 0.9.0, git 2.56.0,
OpenSSL 3.0.13 — the canonical counter environment, host-verified) on fresh clean clones of
the lane repo (`~/kengaku-r60-closure-freeze` @ `9e37311f`, `~/kengaku-r60-closure-head` @
`e33ab0bd`), receipts kept outside the measured clones. The pushed-head receipt's remaining
legs (registry/landcheck/entry-truth/state_check/anchor/round46-c2/r51/r50/r35) were
**evidence-verified from committed receipts**, not re-executed. Which is which is stated per
leg below.

## 1. Step-1 conformance

| check | command | observed | verdict |
|---|---|---|---|
| report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-60/kengaku.md` | `kengaku-shokunin <kengaku@shokunin.local> e67cb358267aa3d7e60c13644686b275d7057a7e` | pass |
| `SHONEN` heading in committed report bytes | `git show e67cb358:.ufo/reports/round-60/kengaku.md \| grep -n '^## SHONEN'` | line 168 | pass |
| cited lane commits exist + are ancestors of master | `rev-parse --verify` + `merge-base --is-ancestor` for 9e37311f, e26b330e, 07178837, e1a022b7, 2684d8d, e33ab0bd | all six `EXISTS ancestor-OK` | pass |
| lane tip pushed | `rev-parse refs/heads/master` vs `ls-remote origin refs/heads/master` | both `e33ab0bdfcf6eb16a0d24aa8651ef7f200f04e9e` | pass |
| cited work reachable in round range | `git log --format='%h %an %s' 9482c8408f62..e33ab0bdfcf6` | exactly the six lane commits, all kengaku-shokunin, subjects match the report's landed-changes list | pass |
| dispatch/complete digest | contract-provided watchdog digest | `2026-11-02T01:52:32-08:00 launch kengaku round=60 base=9482c8408f62` / `05:27:34-08:00 complete kengaku round=60 head=e33ab0bdfcf6 pushed=True` | pass |
| SHONEN.md untouched | `git diff 9482c8408f62 2684d8d -- SHONEN.md` | empty (0 lines); all four boxes `[~]` at head | pass |

Conformance defects: none that bar admission. Two status-neutral precision defects are
recorded in §6 (mirror byte-fidelity; report mistake-row undercount).

## 2. R60-C1 re-check (coverage, held 7 at its L0 cap) — RE-MEASURED in WSL

Mechanism (read from committed bytes at `e33ab0bd:plans/round59_c1_openssl_probe.py`):
`CASES` carry `(name, defect class, cfg)` only — no stored prediction vectors anywhere in
the file (lines 165–219); `predict_legs()` (lines 222–256) derives all six legs at run time
from the declared builder properties, each predicate grounded in the capture's cited anchor
ranges (test_outputs.py :8-12/:22/:31/:47-80/:84-102/:105-136/:139-158); `run_battery`
calls `predict_legs(cfg)` per case (line 349). **The derive-at-runtime mechanism is real;
the probe no longer stores predictions.**

Commands run (clean clone at freeze tip `9e37311f`, receipts outside the measured clone,
exit captured inside the runner):

```
python3 plans/round59_c1_openssl_probe.py --lane . --work <tmp> --receipt /tmp/…
→ PROBE-EXIT=0
  cases=12 legs=72 mismatches=0 setup=0 predicted_u=0
  PREDICATE R59-C1 pass
python3 plans/round59_c1_openssl_probe.py --lane . --check-frozen-table
→ FROZEN-EXIT=0; DIFF perm-loose legs=[0,1] frozen=F/P/P/P/P/P derived=P/F/P/P/P/P
  DIFF key-1024 legs=[0,1] frozen=F/P/P/P/P/P derived=P/F/P/P/P/P
  FROZEN-TABLE rows=12 differing=2 missing=0 ok
python3 plans/round59_c1_openssl_probe.py --lane . --check-receipt corpus/evidence/round59/openssl-probe.txt
→ OBSCHECK-EXIT=0; OBSERVED-CHECK cases=12 agree=12
python3 plans/round59_c1_openssl_probe.py --selftest --work <tmp>   (at head)
→ PROBE-SELFTEST-EXIT=0; SELFTEST pass (toy-ok, toy-perm)
```

My scored-run receipt is **byte-identical** to the committed receipt of record:
`sha256(closure-freeze-receipt2.txt) == sha256(git cat-file blob e26b330e:corpus/evidence/round60/openssl-probe-refreeze.txt) == 0829cfac26a58f5ac09a874cf6002272bc1c7f639a1960e7dcca8082caf864d2`
(REV `9e37311f76f7495a3ed6d7e68982d77a39005d38`), and the committed blob is unchanged at
`e33ab0bd`. The claims doc's embedded table is **byte-identical to a fresh `--render-table`**
(15/15 lines, `cmp` clean). Head-tip battery re-run: same verdict, exit 0.

Untouched receipts and pins:

- r59 receipt of record: `git rev-parse 9482c8408f62:corpus/evidence/round59/openssl-probe.txt` == `git rev-parse e33ab0bd:…` == `41b28d6f02dc24fab030bdbce2632ba6f2e03623` — **byte-identical base↔head; not re-scored.** Its MISMATCH lines name exactly perm-loose/key-1024 at dir/key (the declared RED before-state), `mismatches=2`, `PREDICATE R59-C1 fail`.
- Instrument amendment: probe sha256 at base `a7c9b231e4cef27e…b6a18cd` → at freeze `6faf217c723efaf8…2465d4646` (unchanged freeze→head) — matches the SKILL registry row's named pins and the Q25 two-digest rule.
- Registry/ledger green flips (committed evidence, `e26b330e`): SKILL `round59-c1-openssl-probe` row amended + "**the row is GREEN as of the round-60 corrections landing** (dated flip; the r59 fail of record above stands as history and the r59 receipt is untouched)"; `plans/round54-entrytruth.json` probe row `entry_exit 1→0`, `red→green`, dated `ROUND-60 FLIP` reason naming both digests, the receipt, and the untouched r59 receipt. Same commit carries the SCORECARD counting command.
- Do-nothing controls: `git cat-file -e 9482c8408f62:corpus/evidence/round60` → exit 128 (absent at base); `plans/correction_command_check.py` absent at base; the before-state re-derives from the committed r59 receipt exactly as the row declares.

**Verdict: predicate met — the r59 completion is admitted; coverage unchanged (held 7, L0 cap `kengaku | round-25/33/51` still open; 16 of 89 unchanged; no new ground claimed).**

## 3. R60-C2 re-check (operability, held at ceiling 10) — RE-MEASURED in WSL

Gate `plans/correction_command_check.py` frozen at `9e37311f`, self-pin sha256
`b8ad6bd65dac8d6172baa3def9852bf7c214e1408b8512a82448bfdca9b0c690` at freeze == at head
(matches the SKILL row and the claims freeze). Population `plans/round-*-claims.md`
dated-correction sections only; command class backticked `grep -c` + same-line `→ <n>`;
erratum conversion requires both `ERRATUM (round` and the gate token in one `===` block;
exit 0 iff undeclared defects = 0; 2 = empty population.

```
python3 plans/correction_command_check.py --selftest            (at head)
→ SELFTEST-EXIT=0; cases=6 failed=0 (1-ok, 2-defect, 3-erratum-converts,
  4-foreign-block-refused, 5-fences, 6-empty-population)
python3 plans/correction_command_check.py --lane .              (at freeze 9e37311f)
→ RED-EXIT=1; CMDPOP files=37 sections=1 commands=3 ok=1 out_of_scope=1 defects=1 errata=0
  PREDICATE R60-C2 fail     — byte-identical to committed .ufo/waves/round-60/recon/c2-red-before.txt @ e26b330e
python3 plans/correction_command_check.py --lane .              (at head e33ab0bd)
→ GREEN-EXIT=0; CMDPOP files=37 sections=2 commands=9 ok=3 out_of_scope=1 defects=0 errata=5
  PREDICATE R60-C2 pass     — byte-identical to committed .ufo/waves/round-60/recon/c2-green-after.txt @ 2684d8d
```

The head-state pricing re-derives the erratum ladder exactly: the 5 errata are the
wrapped-phrase defect at :195 plus the four superseded priced lines (original block →1/→2
and continuation-1 →2/→3, all stale vs current truth got=3/got=4), while continuation-2's
lines price OK (got=3 want=3; got=4 want=4). THE HARD STOP is present in ERRATUM
CONTINUATION 2 (no lane prose quotes these fragments again; later text names the class).

S223 grounding: row complete in `corpus/SOURCES.md` (tier A docs, opened 2026-11-02,
quote "instead print a count of matching lines for each input file." = 11 words at capture
:379, status mined, used-by named). Capture sha256 re-computed =
`517177d02c39c446470c898273036a7616f705e4cbdcb6486b76a25700675f37` (matches row and
report); line 379 of the committed capture carries the quote. Live re-open (see §5) agrees.
SOURCES census command `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
→ 216 at head, 215 at base (the single appended row landed at the freeze commit, +2/−0
lines, append-only). Registration same-commit (`e26b330e` touches SKILL.md + entrytruth +
SCORECARD.md together). Amendment 1 in `plans/round-60-claims.md` records the wave-F
doubling drift and the same-line pairing limit without touching the frozen gate bytes.

**Verdict: red→green admitted; operability unchanged (held at ceiling 10).**

## 4. Carry-in routed defects (r59 closure's four) — discharge check

- **(a) fleet-root r58-report erratum append** — the append is still uncommitted in the
  fleet working tree (committed 201 lines at `a286489a`/current HEAD vs 227 working-tree;
  working tree == committed + the 26-line append, byte-verified). The lane correctly did NOT
  mutate the fleet root; the mirror landed at `e26b330e` and the landing is routed to the
  orchestrator. Routing decision: correct. **Byte-fidelity defect found (see §6, D1).**
- **(b) two `path@hash` citations missing landing commits** — discharged: the SKILL
  `receipt-consistency-check` row and the PROVINCE round-59 paragraph now name measured-at
  AND landed-at for both receipts ("measured at `e0512854`, first landed at `85ef87e5`";
  "measured at `85ef87e5`, first landed at `22ffccc7`"), dated round-60 precision fix;
  entrytruth reason carries the same note.
- **(c) non-reproducing counting command** — closed BY R60-C2: the R1-form dated erratum on
  `plans/round-59-claims.md` carries the reproducing commands, one per line, priced at
  current truth (verified live by the gate runs above).
- **(d) SCORECARD r59 cell stale "210→214"** — discharged: appended "Round-59 verifier-routed
  precision corrections" block (cells stay as written) with the dated touch-up 210→215 at
  the r59 tip (S222 landed later at `fea67b2c`), 215→216 this round; counting command
  re-derived by me (215 at base, 216 at head).

## 5. Discernment spot-check (outside view)

Census: `bash <fleet>/scripts/sources-census.sh validate --root <fleet> kengaku` → exit 0,
verdict `ok`, 21×W04 (20 pre-existing + S222's supersession duplicate — matches the report;
CENSUS-END-EXIT=0).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S223 GNU Grep manual admit (tier A, narrow scope) | admit | live https://www.gnu.org/software/grep/manual/grep.html + committed capture :379 | **agree** | the quoted sentence appears verbatim in the live manual §2.1.3 General Output Control under `-c`/`--count` ("Suppress normal output; instead print a count of matching lines for each input file."); quote byte-locates in the committed capture; 11-word count correct; sha256 matches |
| refusal to revert this round's own wave-F LOG entry to keep "→ 1" true | reject-equivalent (price at current count 2, keep the append) | LOG wave-F entry + Amendment 1 + the gate's live pricing (got=2 want=2 ok) | **agree** | reverting an appended LOG entry would violate the append-only rule and launder the drift; pricing at current truth is exactly what the gate exists to force |
| fleet-root erratum handled as mirror + route, not committed by the lane | reject-equivalent (do not commit; mirror + route) | fleet working tree vs committed bytes; round contract | **agree** | the lane may not mutate the fleet root; the orchestrator lands the authoritative bytes (verified == committed + append). Agree with the decision — but the mirror itself carries defect D1 below |

## 6. Defects and routed items (all status-neutral; none bars admission)

- **D1 — mirror byte-fidelity (routed to the lane for next round).** The claim "mirrored
  byte-for-byte" (report, PROVINCE, SCORECARD, LOG, lesson) is false at the byte level:
  the mirror's 26 lines are content-complete and ASCII-identical, but its 9 non-ASCII
  characters (em-dashes `—`, arrows `→`) are cp1252-double-encoded (e.g. `E2 80 94` →
  `C3 A2 E2 82 AC E2 80 9D`), and the mirror block carries one extra trailing blank line
  (27 vs 26). Verified in WSL by byte compare of `git show e26b330e:.ufo/waves/round-60/r58-report-corrections-mirror.md`
  (marker-stripped) against `git -C <fleet> diff HEAD -- .ufo/reports/round-58/kengaku.md`
  `+`-lines. The authoritative append bytes are intact in the fleet working tree (verified),
  so the orchestrator's landing is unaffected; the lane should re-mirror byte-true (or append
  a dated erratum downgrading the claim to content-mirror) and sweep every mention.
- **D2 — report mistake-row undercount.** The report says the lesson mines "2 mistakes + 2
  appended rows"; the landed lesson carries 3 initial rows + 2 appended rows (5 total). The
  lesson itself is complete (every row has class · evidence · captured-by · fix). Precision
  nit only.
- **D3 — observed, self-declared, not a defect.** The SKILL `correction-command-check` row
  quotes the landing-time green value (`defects=0 errata=1`) while the receipt it cites
  (landed at `2684d8d`) prices the final tip truth (`errata=5`). Coherent under the ladder
  story and the HARD STOP (the row says "at the round-60 corrections landing"; re-quoting is
  forbidden); recorded here so a future reader does not misread it as drift.
- **Carried environment note (pre-existing, not round-owned):** the Windows worktree cannot
  check out 110 historical wave files (NTFS-uncheckpointable names); all committed bytes were
  measured on complete WSL-native-fs clones. My clones checked out fully in WSL and
  reproduced the receipts byte-identically, so no counter saw the worktree gap.
- **SHONEN for the operator:** all four boxes remain `[~]` (asserted-by-author). Box 2 ("at
  least one end-to-end domain task executed and logged in LOG.md") looks checkable by a
  non-author on the current record (the r59/r60 openssl-grader execution chain is fully
  re-derivable from committed bytes, as this spotcheck demonstrates). This verifier did not
  write any `[x]` (duty: never edit lane-authored files).

## 7. Per-axis verdicts (non-author)

| axis | score (base → head) | verdict | evidence |
|---|---|---|---|
| depth | 9 → 9 | unchanged | additive dated knowledge-entry addendum (pure append, verified); no entry weakened |
| coverage | 7 → 7 | unchanged | C1 predicate met at the L0 cap; 16 of 89 unchanged; PROVINCE completion paragraph opens no new ground |
| operability | 10 → 10 | unchanged (held at ceiling) | C2 gate re-derived red→green byte-identically; registration complete |
| freshness | 10 → 10 | unchanged | LOG re-verification lines for every touched claim; all citations resolve at the tip (registry row / receipt / claims-doc spots re-opened) |
| calibration | 10 → 10 | unchanged — exercised | the counters caught the round's own close-out prose twice and the Q20 clip once; every disposition is a held score; nothing papered over |
| adjacency | 9 → 9 | unchanged | nothing absorbed; the fleet-root erratum mirrored + routed, not absorbed |
| novelty | 8 → 8 | unchanged | no new phenomenon claim; the class line is the r59 registration |

No owned axis harmed. Both declared claims verify. **kengaku round 60: admitted.**

## 8. Trend verdicts (with evidence)

- **expansion: unchanged** — verified: SOURCES 215→216 (one docs row, counted by me at base
  and head); coverage held 7 at its standing L0 cap; 16 of 89 unchanged; no new province
  ground; no new capability row (the round correctly declines one — C1 completes an existing
  registration, C2 is an instrument row).
- **quality: improved** — the sixteenth grader's admission completes under a full-commitment
  72/72 clean run whose predictions can never again be retyped (derive-at-runtime, verified
  structurally and by byte-identical re-run); a new mechanical gate closes a routed-by-eye
  class red→green (re-run both directions, receipts byte-identical); the advertised surface
  re-runs green at the pushed head (final-tip + pushed-head receipts evidence-verified; the
  probe/gate legs re-measured by me).
- **discernment: improved** — the round carried its own failures visibly: the first final-tip
  take discarded uncommitted (dirty tree), the self-quoting ladder caught twice by the
  round's own counters and stopped structurally (HARD STOP), the Q20 receipt clip caught by
  the r59 gate and erratum'd with receipt bytes preserved, and the harness exit-capture class
  mined with runner-captured exits everywhere. All four fires are mined in
  `corpus/lessons/round-60.md` (3+2 rows, each class/evidence/captured-by/fix); my spot-check
  agrees with the sampled admit and both sampled reject-equivalent decisions.

## 9. Pushed-head verification receipt

`.ufo/waves/round-60/pushed-head-verification.txt` (A at `e33ab0bd`, measured at `2684d8d`):
every leg green — registry `ADVERTISED 89 / REGISTERED 89`, `LANDCHECK PASS n=4`, entry-truth
`executed=90 evidence_missing=0 laundered=0`, `TIPSTATE 61g/29r declared==observed`,
state_check PASS, R59-C2 `defects=0 errata=4`, probe `PREDICATE R59-C1 pass` exit 0, gate
`PREDICATE R60-C2 pass` exit 0, anchor `live=0`, round46-c2/r51/r50 pass, r35
red-as-declared exit 1 — with the two known self-inclusion drifts named (+2 receipt-gate
files 6863→6865; +1 anchored pair 14→15; verdicts unchanged). The probe and gate legs of
this receipt I re-measured byte-identically myself; the remaining legs are evidence-verified
from the committed receipt bytes (not re-executed).
