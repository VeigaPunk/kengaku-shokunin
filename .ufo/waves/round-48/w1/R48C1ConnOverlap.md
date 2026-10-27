# R48C1ConnOverlap — C1 fixture-fence/calibration ownership overlap

## Axes
Calibration (C1); coverage (C2 is distinct and not evaluated here). This bounded connector scan makes no axis score or admission claim.

## Evidence and commands
Access date: 2026-10-27. Local source URLs are file paths in the current host checkout; no external web sources opened. No scored execution was run. Freeze requirement blocks scored work until stage 2 is committed; the claims file at stage 1 explicitly says stage 2 pins the frozen population/literals and must precede claimed-work scoring.

Commands run (cwd fleet root):
- `cat /home/vgpnk/.omp/agent/RULES.md`
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --short`
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD`
- `find /home/vgpnk/Projects/shokunin -maxdepth 3 -type d -name '*kengaku*'`
- Read required files in full: `plans/round-48-claims.md`; `corpus/lessons/round-46-verifier-spotcheck.md` (tool output truncates long lines; cited material below is visible).
- Read `kengaku-shokunin/PROVINCE.md`, `tameshi-shokunin/PROVINCE.md`, `kama-shokunin/PROVINCE.md`; fleet directory listing and `.ufo/waves/round-48/w1.ready`.
- Attempted broad `glob` at fleet root: timed out (incomplete; not treated as evidence of absence). `grep` query returned large fleet-wide results; no scored/probe commands.

Observed outputs:
- `git rev-parse HEAD` → `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`; this is not the user-specified base `a543d92083557dd9b33ee674e9b99b03411f80af`.
- `git status --short` showed pre-existing untracked `.ufo/waves/round-48/claims/`, `w1.ready.partial`, and `w1/`; left untouched.
- `.ufo/waves/round-48/w1.ready` says `{"lane":"kengaku","round":48,"wave":"w1","dispatch":"/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1-dispatch.json","l1":"KengakuR48"}`.

## PROVINCE overlap findings; disposition
1. **Tameshi — report out, do not absorb.** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md:3-17,44-47` owns reusable verification-fixture craft (hermetic suites, mutation testing, fail-closed controls, verdict discipline); explicitly refuses sibling gate code and says recommendations travel in reports. C1's frozen counter and mutation battery are Kengaku's own gate; reusable methodological observations (e.g. separating benign admission from traced leak and control ordering) may be routed to Tameshi, but no Kengaku fence/counter ownership transfers. Located quote (15 words): “Never edits a sibling's gate code (read-only probes; recommendations travel in round reports).”
2. **Kama — no substantive ownership overlap; report out only if serving endpoint appears.** `/home/vgpnk/Projects/shokunin/kama-shokunin/PROVINCE.md:3-16,42-55` owns local model serving/endpoint-health and consumer registries, not filesystem fixture admission. Its generic verification instruments do not establish fixture-fence ownership. C1 uses local Git fixtures and traced filesystem access; no service or endpoint is needed or sampled. Located quote (13 words): “kama answers *\"is the thing at this baseURL the model this config believes it is, right now\"*”.
3. **Kengaku — retain gate and decision.** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md:3-6,19` says Kengaku owns LLM evaluation domain knowledge and reports outside-domain evidence rather than absorbing it. Round-48 claims define C1 as repair/rejudgment of `plans/fixture_fence.py` and its counter. No sibling claim on the product-specific fence was found in the bounded direct Province scan.

Relevant defect evidence: `corpus/lessons/round-46-verifier-spotcheck.md:19,45-47` records C1's prior kill-rule fire, 9/9 novel honest refusals and weak mutation result; routed defect says repair over-refusal and broaden positive controls under a newly frozen counter. The round-48 claims say kill rule now keys on traced outside access and freeze stage 2 must precede claimed scoring. This connector did not score or probe.

## Proposed bounded move
**Compatible synthesis:** keep all C1 implementation, frozen counter, classification and admission authority in Kengaku; report reusable control/mutation-method observations to Tameshi as methodological input only. Do not absorb Tameshi's general method or kama's endpoint-health surface. This preserves the distinction between an admission event and observed hostile access without altering the frozen predicate or kill rule.

## Risks / contradictions
- Current checked-out HEAD differs from requested stage-1 base, and the required stage-2 freeze is not established by the sources read. Therefore this report is not evidence from a verified clone at the requested revision. No scored run was made.
- Potential apparent overlap: both Kengaku and Tameshi use gates/mutation tests, but Province boundaries separate product-specific gates (Kengaku) from reusable verification craft (Tameshi); do not collapse them.
- The blanket request to scan sibling lanes is bounded here to directly relevant Province declarations (Tameshi, kama) plus Kengaku's own Province; the broad fleet glob timed out, so absence of other overlaps is not claimed.

## Verification / limits
No build, tests, scored counter, probe, clone, or fixture Git mutation executed. No tools installed/updated. No revision was measured by a receipt; `REV` is therefore not applicable. No scratch tree was created, so cleanup is not applicable. Evidence is limited to the current filesystem checkout and the listed Province/claim/lesson files; no sibling-lane history or unlisted Province was exhaustively searched.

VERDICT: **report out to Tameshi as method-only; retain C1 gate in Kengaku; no kama overlap identified. Scored work blocked pending verified base and committed stage-2 freeze.**