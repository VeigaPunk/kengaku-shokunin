# Round 73 — non-author verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_zfl)
lane: kengaku · lane-round: 73 · base d96c3e62fd01771718368688c2685dceeef5b83e → tip f669367c9051a1716a622e756325f4a48c360348
report: /home/vgpnk/Projects/shokunin/.ufo/reports/round-73/kengaku.md (fleet commit 2edc96f4dd75db7fa8288d9ca1c0ac7b18ebd3cc, author kengaku-shokunin)
watchdog digest: `2026-11-03T23:35:56-03:00 launch kengaku round=73 pgid=3549543 driver=hyaku-inline attempt=1` · `2026-11-04T00:05:47-03:00 complete kengaku round=73; hyaku-inline attempt=1` (both lines present at .ufo/watchdog.log:2193,2200)

## 1. Step-1 conformance

| check | command / observation | result |
|---|---|---|
| report authored by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-73/kengaku.md` → `kengaku-shokunin kengaku@shokunin.local 2edc96f4…` | pass |
| cited commits exist + ancestor of lane branch | `git merge-base --is-ancestor <h> master` for d96c3e62, 255c261d, ea41880f, 208ed16a, f669367c — all YES | pass |
| lane pushed, no leftover work | `jj-lane.sh state` → branch=master local=remote=f669367c ahead=0 behind=0 tracked=0 untracked=0; `git status --porcelain` empty | pass |
| remote proof | `git ls-remote origin refs/heads/master` → f669367c9051a1716a622e756325f4a48c360348 | pass |
| SHONEN heading, one line per box | 4 boxes, all `[~]` with resolvable pointers | pass |
| prompt template contract | `.ufo/prompts/kengaku-round-73.md` carries §1 mission/axes, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (path, SHONEN, hash citation), §5 commit/push scope + L0, §6 hyaku addendum | pass |

Not a marker report: named committed work, evidence pointers, measurements, sources, trends, SHONEN.

## 2. Per-claim re-check

Method note: both claims rest on lane-owned gates/selftests (`plans/round52_c2_registry.py`, `plans/round73_c2_registry_audit.py`). Per PROTOCOL §Gate standard (Closure consequence) I verified their **committed evidence** only — self-test tally, frozen-run verdicts, revision measured — and never executed a sibling's gate. Plain byte measurements (grep/wc/git over committed trees) were re-run by me directly.

### R73-C1 / coverage — original NOT ADMITTED (confirmed); axis unchanged

- Reported before: base ADVERTISED110, MISSING5, rc1. Receipt `corpus/evidence/round73/c1-before.txt` (BASE_TIP d96c3e62): ADVERTISED total=110, REGISTERED 105/rows107, MISSING 5, rc1. Match.
- Reported contradiction: frozen predicate `plans_only0` fails on the registered tree. Receipt `a1-red-green.txt` over identical bytes (TREE ea41880f): frozen counter → R73-C1 fail rc1; amended counter → pass rc0. The freeze's predicate is indeed incompatible with MISSING0 — the lane's self-defeat analysis is confirmed by its own frozen receipt.
- Reported after (amended, engineering only): `final-checks.txt` MEASURED_COMMIT 208ed16a1ba28af8ddcac9011af77fcf98a1b063: full mode files134 plans_seen82 plans_only0, ADVERTISED113, REGISTERED113 rows115, MISSING0, rc0; legacy control rc1 (original predicate still fails). Selftest cases4 failures0 rc0. Match.
- My plain re-measurement: `grep -cE '^\| .*round[0-9]' SKILL.md` base 107 → tip 114 (+7 net = +8 added incl. the new audit row, −1 obsolete malformed tensor row removed after replacement — exactly the report's accounting). Registry-row totals (113/115) are the gate's own printed tallies; evidence-verified, not re-executed.
- Score: SCORECARD round-73 row coverage 7→7, held at L0 cap; the round-72 summary block already held coverage 7. No score cell edited outside the appended round-73 section (full `git diff d96c3e62 f669367c -- SCORECARD.md` reviewed: append-only).

### R73-C2 / calibration — original NOT ADMITTED (confirmed); axis unchanged

- Reported before: frozen audit over base total106, MISMATCH2, rc1. Receipt `c2-red-before.txt`: BASE_TREE = git archive of d96c3e62; total106, D2 defects on sources-adopt failure-map and class-survey kind, MISMATCH2, rc1. Match.
- Reported denominator break: C1's row additions move the derived universe 106→114, so the frozen exact-106 predicate cannot be met post-landing; A2's relaxed 114 threshold is not original admission authority. Confirmed as causally inseparable as frozen; the lane declined retroactive re-scoring — the honest call.
- Reported after (amended): `final-checks.txt` at 208ed16a: total114, parsed114 failed0, D1–D4 n=0, MISMATCH0, rc0. Selftest arms4 red3 ok=True; mutants total7 killed7 survived0 null_detected1; CALLER-PRESERVED True in both modes. Frozen-tuple control `c2-control-frozen-tuple.txt`: old round-72 counter accepts the fifth defective row (DEFECTS0 rc0) while the new audit prices it (MISMATCH2 rc1) — the control discriminates. Match.
- Limits the lane itself filed (structural-not-semantic audit; 13/16 adversarial battery accepted; malformed-row skipping) are consistent with the receipts and are marked, not hidden. Score: calibration 10→10 held (round-72 summary block already held 10).

### Re-measured vs evidence-verified

Re-measured by me directly: SOURCES.md row counts (240→241), SKILL.md registry-row count (107→114), census validate, commit ancestry, SCORECARD diff scope, wave file counts, all receipt files' existence and internal tallies. Evidence-verified (lane-owned gates, not executed): every ADVERTISED/REGISTERED/MISMATCH total, both selftest tallies, the mutant run, and the frozen-run verdicts.

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | unchanged | C1 original not admitted; score held 7; registry repairs landed but the claimed widening increment is explicitly disclaimed |
| calibration | unchanged | C2 original not admitted; score held 10; audit exercised with discriminating controls |

No owned axis harmed: `git diff d96c3e62 f669367c -- SCORECARD.md` is a single appended round-73 section; no historical score row touched. No exploratory claim this round, so no `unprovable-but-better` ruling was required.

## 4. Discernment spot-check (LEARNING.md — from outside)

| item | lane decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S249 (Python 3.15.2 ast docs) | **admit**, narrow API scope only | local capture `corpus/evidence/round73/sources/ast-docs.html` + live `https://docs.python.org/3/library/ast.html` (curl: HTTP 200, 362493 bytes) | **agree** | capture sha256 94bead0ac648…a42fe809 matches the SOURCES.md row; `wc -c` 362493 matches; capture line 2680 contains “Parse the source into an AST node.”; live page re-opened HTTP 200 with byte-identical length and the quote present. Tier A for AST construction only is the correct scope. |
| “AST parse proves executable validity” | **reject** | capture lines 2708–2715 + live page | **agree** | the capture's own warning states parsing “doesn’t guarantee that the source code provided is valid Python code that can be executed” and that `ast.parse()` “won’t do any scoping checks”; the reject's flip (controlled execution + exit/output comparison) is the right repair. |
| S249 SOURCES.md row quote | new row, ≤25-word quote | `corpus/SOURCES.md:265` | **agree** | quote cell is 24 words, located, and the row changed no pre-existing status/recheck/used-by cell (`git diff` shows a single added line). |

Census: `scripts/sources-census.sh validate --root … kengaku` → rc=0, 25 W04 across-scope duplicate-URL warnings, `ok` verdict — identical count to both committed receipts (census-before.txt / census-after.txt). Spot-check axis grades: admit agree, reject agree.

## 5. Trend verdicts

- **expansion: unchanged.** One A-tier row 240→241 (re-counted by me), a held (not admitted) knowledge candidate, no frontier-to-core movement, no capability row. The lane's own `unchanged` stands.
- **quality: improved.** Dead/missing/underdeclared registry declarations corrected (r69 receipt path, usage exits, write scopes, sources-adopt invocation), the malformed tensor row replaced before removal, and a real data-loss defect — selftest/mutants deleting the caller's entire `--work` tree — fixed to an owned-child scheme with red-before (sentinel receipt) and after-repair `CALLER-PRESERVED True` canaries in `cleanup-after.txt`/`final-checks.txt`. Structural weaknesses are marked in the held entry and lesson, not passed off. Bounded engineering improvement, no admitted entry fails re-check.
- **discernment: improved.** The lane provisionally filed `unchanged` only because “no outside non-author agree/disagree on this round yet” — this closure is that outside check, and it agrees with the gate on both the admit and the reject (§4), which is LEARNING.md's criterion for `improved`. Q54 was added this round from the lane's own adversarial findings.

## 6. Defects and routed items

- None blocking; no routed defects to the lane this round. The round's known-limitation list (structural-not-semantic audit, 13/16 attack battery accepted, malformed-row skipping, pad-able A1) is honestly filed in SCORECARD, lesson, and report.
- Superseded pointer: `corpus/lessons/round-73.md` §Outside spot-check says “Pending non-author closure” — this file is that closure; the lane should cite it in its next round's lesson (routine continuation, not a defect).
- For the operator (promotion-owned, never closure): all four SHONEN boxes remain `[~]` lane-asserted. Boxes 2 and 4 look fully checkable by a non-author reviewer now (measured end-to-end registry/audit workflow logged at LOG.md round 73; PROVINCE unchanged, sibling findings reported not absorbed per SiblingConnectorR73). Box 1's best evidence is the *held* knowledge candidate; box 3 carries the lane-named finding-id gap. Promotion review is operator-owned.
- Prior-round errata filed in the report (R72-V1 corrected hash 08df910ab461620741d433def3df38a8406efe9f verified present, 40 chars; R72-V2/V3, R71-R2) are consistent with the committed round-72 spot-check and receipts; filed reports correctly left byte-unchanged.
