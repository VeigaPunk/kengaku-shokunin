# R49C1ConnOverlap — connector scan: sibling lanes × fixture-fencing / calibration ownership (serving R49-C1)

Seat: R49C1ConnOverlap (connector, leaf; no subagents). Lane: read-only at frozen stage-1 base
`9d2900af41e4d1fc6022eff99010436fde6dbd93`. Work clone:
`git clone --shared` → `/fast/scratch/hyaku/kengaku-r49/R49C1ConnOverlap/lane`,
`git rev-parse --show-toplevel` verified = that path; `git rev-parse HEAD` = `9d2900af41…`.
Scratch `TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1ConnOverlap`, removed before yield.

## Axes named

Lane-carried axes (claims freeze, `plans/round-49-claims.md:12-17`): calibration 8, coverage 7,
novelty 7, depth 9, operability 8, freshness 8, adjacency 8. This seat is judged on **calibration**;
the item is a boundary/ownership scan, so the touched axes are **adjacency** (lane-owned ground vs
sibling ground) and **calibration** (the C1 counter's frozen legs must not collide with a sibling's
owned claim). One bounded proposal below improves adjacency and calibration without harming either —
and without touching C2's disjoint surface (separability, `:146-153`).

## Stage-1 freeze verification (precondition for scored work)

- `git merge-base --is-ancestor 9d2900af41… af88aab1…` → true (freeze is an ancestor of lane tip
  `af88aab193e6034cb9b386472064e3c18fa90128`); freeze committer-date `2026-10-28 09:14:40 -0300`,
  this scan measured `2026-10-28T12:24:06Z` → freeze predates measurement.
- `git rev-parse 9d2900af:plans/fixture_fence.py` = `af88aab1:plans/fixture_fence.py` =
  `a2b128ae007bf47d3aefdeda6321ae118c7e5958` — the measured fence is the frozen before-value.
- `git diff --stat 9d2900af… af88aab1… -- plans/` → empty: nothing under `plans/` moved since freeze.
- `plans/honest49`, `plans/sealed49`, `plans/mutants49`, `plans/round49_c1_verify.py` → absent at
  stage-1 (correct: wave-1 seats author them; stage-2 pins them). `plans/refusals46/` = 20 modules,
  `plans/sealed46/` = 12 modules, `plans/battery42|43|44` = 5+7+8=20 fixture modules — frozen
  populations present at base.
- **No scored counter/probe run was made by this seat** (item is a scan, not a measurement); the
  precondition above is nonetheless verified and satisfied.

## Commands run (evidence commands; all read-only)

1. `git clone --shared …/kengaku-shokunin lane && git checkout 9d2900af…` (+rev-parse checks) — above.
2. `find /home/vgpnk/Projects/shokunin/*-shokunin -maxdepth 3 -iname '*province*'` → every lane
   carries `PROVINCE.md`; reads below.
3. `find … -iname '*fixture*fence*' -o -iname '*fence*'` → fence-named files in chousa, kotoba,
   tabi, kengaku (only kengaku's is an admission fence; others are markdown-fence fixtures).
4. `grep -rlin --include='*.py' 'def .*(admit|refus|fixture)|strace|symlink.*escape|realpath.*inside|
   os.path.commonpath'` over every sibling lane → candidate instrument list (audio, chousa, kagi,
   kaidoku, kake, kama, kasegi, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji,
   tabi, tameshi, tsukuroi).
5. `grep -rin 'fixture.?fence|breach('` over all sibling lanes → zero non-kengaku hits for a
   `breach(d, argv)` contract; `grep -rin 'fixture.fence'` over every `PROVINCE.md`/`SKILL.md` →
   zero non-kengaku hits. **No sibling cites or claims kengaku's fixture fence.**
6. `grep -n 'fence|fixture_fence' kengaku-shokunin/PROVINCE.md` → **zero hits**; same for
   `SKILL.md`. The lane's own province never names the fence it is about to re-claim on (see P3).
7. Docstring reads: `tameshi-shokunin/tools/mutate-and-run.sh`, `souji-shokunin/tests/fixtures/
   r14-census-boundary.py`, `kasegi-shokunin/corpus/instruments/mirror-containment-check.py`,
   `revenger-shokunin/corpus/self_assessment_check.py`, `tsukuroi-shokunin/tools/
   probe-git-env-leak.py`, `audio-shokunin/corpus/live/r70-scribe/strace_leg.py`,
   `kama-shokunin/.ufo/waves/round-50/w1/out/R0Controls2.md`, `mado-shokunin/tools/mado-verify.sh`,
   `plans/round46_c1_verify.py` (frozen counter parent at base).

## Findings — overlap map (PROVINCE paths cited; disposition per item)

Legend: **contested** = a sibling also claims the ground; **method-overlap** = shared craft,
different owner; **name-collision** = shared word, different thing; **no overlap** = adjacent
substrate only.

| # | Sibling ground (PROVINCE / file citation) | Overlap class | Disposition |
|---|-------------------------------------------|---------------|-------------|
| 1 | `tameshi-shokunin/PROVINCE.md:3-5` — "**Domain:** verification-fixture craft — the reusable method of honest checks: hermetic suites, mutation testing, fail-closed arms …"; `:14-18` — "every lane's gate remains its own; tameshi owns only the reusable craft … Never edits a sibling's gate code" | **method-overlap on the MUTANTS leg.** C1's frozen delta (f) commits `<M>` fence mutants + caught-floor (`plans/round-49-claims.md:65-72`). Tameshi owns the *method* (`tools/mutate-and-run.sh`, 10 measured fleet legs incl. kumitate `gate-mutants.mjs`); kengaku owns the *instance* — `plans/fixture_fence.py` is kengaku's gate. Not contested: tameshi's own refusal clause concedes every gate to its owner. | **Report-out (post-landing).** C1's mutant battery is a *new shape* in tameshi's recorded leg set (a Python containment fence under `strace`, kill = signature-line flip) — the 11th measured-leg candidate, exactly the "evidence in TWO independent lanes" admission bar tameshi sets (`:14-16`). Land first, then report the leg; pre-landing it does not exist. Never absorb tameshi's runner or ledger. |
| 2 | `kengaku-shokunin/PROVINCE.md:282-284` — "mutation testing of a lane's own gate is a fleet-wide pattern, not kengaku ground — tameshi's `tools/mutate-and-run.sh` and kumitate's `gate-mutants.mjs` are the precedents" + `:324` (kumitate `gate-mutants.mjs` — 43-mutant battery, `prlimit`, no bwrap) | **self-cited precedent.** Own province already routes gate-mutation craft out; the C1 mutant battery is the lane's own instance of that fleet pattern. | **Absorb.** Mutation-tester seats author mutants against the landed fence per the fleet pattern; the counter stays lane-owned. Also: `mado-shokunin/PROVINCE.md:28` + `tools/mado-verify.sh:2245` shows the established *consumption* form — read-only pin of `tameshi-shokunin/tools/mutate-and-run.sh` with its revision printed in the receipt. Wave-1 authors MAY cite that runner revision; the battery itself stays in `plans/mutants49/`. |
| 3 | `souji-shokunin/PROVINCE.md:100-103` — "The census must refuse credential-store roots, ancestor roots and known aliases before enumeration; this is a refusal fence, not credential hygiene" + `tests/fixtures/r14-census-boundary.py:1-20` — strace `open/openat/getdents64` access-check + PATH spies + canary-string egress check | **name-collision on "fence"; craft-sibling on enforcement.** Souji's fence refuses enumeration inputs; C1's fence admits git fixtures. Souji's fixture is the fleet's closest precedent for C1's B-envelope (B3/B5 traced-open discipline of `plans/round46_c1_verify.py:46-62`). | **Absorb as craft precedent.** The r14 boundary fixture already proves the host-level `strace`+spy+canary pattern; C1 counter authors can cite it as prior art for the B1/B3/B5 legs. No ownership conflict: souji fences its census, kengaku fences its fixtures. No report needed — souji's own `:102` already labels it a "refusal fence." |
| 4 | `kasegi-shokunin/corpus/instruments/mirror-containment-check.py:18-23` — "a non-GONE class must name an existing path confined to the root that class implies … Fixture names are confined: an absolute name, a `..` segment, or a location whose parent resolves outside the case root is rejected" | **craft-sibling.** A containment-matrix admission gate over a resolver's outputs — the closest *conceptual* sibling to `breach(d, argv)`: expected-class pin + path-confinement assertion + tamper-proof fixture names. | **Absorb.** The "pin a class AND assert its path confines to the case root" pattern is directly reusable for `plans/sealed49/` held-out module design (a hostile module must both be refused AND show zero traced outside access — the counter's `leaked=0 read=0` columns already encode this). No report: kasegi's instrument is scoped to its own resolver matrix. |
| 5 | `tsukuroi-shokunin/tools/probe-git-env-leak.py:7-11` — "A tool that builds a private sandbox repository but passes the caller's environment to git obeys an inherited `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE` and writes wherever they point." | **adjacent substrate.** tsukuroi measures *harness-side* GIT_* steering of git writes; C1's fence admits fixtures only if the *store and argv* stay inside `d` — and the base fence starts no git child at all (`fixture_fence.py` docstring ¶6). GIT_* steering is outside the fixture's attack surface (fixtures can't set the harness env), but a repair that admits linked-worktree fixtures reopens the question of *which* git runs downstream. | **No route.** The frozen counter already runs the fence under `env={"PATH":…,"HOME":"/nonexistent","LANG":"C.UTF-8"}` (`round46_c1_verify.py:372,423`) — the env channel is scrubbed at the counter, so tsukuroi's leak class is unreachable from a fixture. Recorded here so the counter author does not need to rediscover it. |
| 6 | `revenger-shokunin/corpus/self_assessment_check.py:3-6` — "Self-assessment mismatch checker (round-70 C2, calibration). Calibration is the distance between what the lane says about itself and what the repository shows … six named mismatch classes" | **name-collision on "calibration" AND on the claim's own phrasing.** R49-C1's frozen text says "Self-assessment under test" (`round-49-claims.md:43`) — revenger's SM1–SM6 measure prose-vs-repo distance; C1 measures advertised-vs-observed fence behaviour. Same axis word, different object. | **No route.** Both lanes use "calibration" for self-report-vs-measurement; revenger's object is documents, kengaku's is instrument behaviour. If the fleets ever unify the axis, this pair is the precedent for "self-assessment" being *behavioural* as well as *textual* — noting, not routing. |
| 7 | `kagi-shokunin/PROVINCE.md:52` — "`corpus/claim-ledger.sh` — calibration gate"; `:51` — `scope-gate.sh` "ownership partition + shared-directory breadth"; `:49` — POLICY-before-exec refusal of ref-token fixtures | **name-collision on "calibration gate"; craft-sibling on refuse-before-execute.** Kagi calibrates its own claim-ledger revision stamps; the POLICY arm (refuse a hostile *fixture class* before any exec) is the same shape as C1's `breach()` refusal, different domain (credential fixtures). | **No route.** Lane-scoped; kagi's own `:67` routes credential ground *to* kagi, nothing from it. |
| 8 | `mado-shokunin/PROVINCE.md:26` — "symlinks, path traversal and escaping paths refused" | **craft-sibling, weakest form.** Declared-tool input refusal (JSON bundles), not git-store shape. | **No route.** |
| 9 | `kotoba-shokunin/PROVINCE.md:17` — "Sibling arbitration (round 49): … the primary-source finding that **no documented tie-break exists between overlapping descriptions**" + `verifiers/fixtures/checklist/command-fence-filter` + `verifiers/check_infoless_fences.py` | **name-collision on "fence" (kotoba's = markdown code-fences); meta-finding binding on THIS scan.** | **Absorb the arbitration finding.** Kotoba's census proves: when two sibling descriptions overlap, no written precedence resolves it — so any genuinely contested fence ground would have to be settled by explicit report-out, exactly the disposition column above. No "fence" claim collision: kotoba's fences are markdown. |
| 10 | `kama-shokunin/.ufo/waves/round-50/w1/out/R0Controls2.md` — "the frozen counters are defeatable below the ablation floor — demonstrated met=True on a fixture-gated C2 shim … and on a deny-list C1 env patch" | **counter-sensitivity precedent, not ground overlap.** Kama's seat proved J-ablation floors (whole-mechanism removal) do not bound cheaper evasions — the same threat shape C1's `<M>/2` floor carries. | **Absorb as caveat.** C1's floor counts *declared* mutants in `c1-mutants.json`; the R0 finding warns that a caught-floor says nothing about mutants outside the declared set. The claim already caps at `<M>/2` — seats authoring mutants should prefer *cheap* evasions (argv spelling, lexical tricks) over mechanism removal, or the floor certifies little. Worth one line in the mutant authors' context, not a routed item. |
| 11 | `audio-shokunin/PROVINCE.md:41` ("threshold-calibration" fixture battery), `game-dev-2d|3d PROVINCE.md` ("executable headless fixtures"), `mori-shokunin/PROVINCE.md:51` ("Alert-threshold calibration"), `tabi-shokunin/corpus/evidence/w10-aud-b10-work/fence.txt` (loopback fixture server), `chousa-shokunin/corpus/knowledge/fenced-anchor-r23.md` (markdown-fence anchor arm), `kaidoku-shokunin/PROVINCE.md:62` (strace as host fallback reader), `kumitate-shokunin` (fleet orchestration; `corpus/knowledge/agent-isolation-substrates.md` covers *seat* isolation, not fixture gates), `lore/kotodama` (domain gates) | **name-collisions / adjacent substrates only.** "fixture," "fence," and "calibration" are fleet-common words; none of these lanes claims a git-store admission fence or gate-behaviour calibration. | **No route.** Enumerated to bound the scan: the probe word's breadth is exactly why a sibling sweep can't rest on name-match. |

## Proposed move (one, bounded)

**P3 — declare the fence's own ground in kengaku's next PROVINCE append, with the sibling-sweep
line attached.** `kengaku-shokunin/PROVINCE.md` names `grader.py`, `attrib_probe.py`,
`benchmark_spec_audit.py`, probes per TB2 grader — but `plans/fixture_fence.py`, the instrument
three consecutive claims rounds (45, 46, 48, now 49) have built a calibration axis on, is absent
from `## Surfaces`, `## Province map`, and every round append (`grep -n 'fence' PROVINCE.md` → 0
hits; same `SKILL.md`). Meanwhile this scan shows the *only* fleet ground of the same shape —
tameshi's method (`tameshi-shokunin/PROVINCE.md:14-18` "every lane's gate remains its own") —
explicitly defers to the owner lane, and kengaku's own `:282-284` already routes the *method* out.
The declaration exists in practice but not in the province: a sibling-claims collision on
"fixture fence" is undetectable by any later connector reading only PROVINCE files (kotoba's
`:17` finding says a collision would then have no tie-break).

**Disposition:** report-out to **L1 `KengakuR49`** (this lane's own integrator — the only writer
allowed to touch `PROVINCE.md`), not to any sibling. One append-only paragraph, appended at the
round-49 wrap: "`plans/fixture_fence.py` (fixture containment admission gate; blob
`a2b128ae…`) is lane-owned ground of the calibration surface; the reusable fence/mutation method
stays tameshi's (`tameshi-shokunin/PROVINCE.md:3-18`), containment-matrix fixture craft cites
`kasegi-shokunin/corpus/instruments/mirror-containment-check.py:18-23` and `souji-shokunin/
tests/fixtures/r14-census-boundary.py`; report sibling collisions, never absorb."
Two-lane synthesis inside one move: names kengaku's instance AND tameshi's method-boundary in
the same paragraph, so both sides of the ownership line are pinned where the next connector
looks.

**Axis effect:** adjacency ↑ (a lane-claimed instrument finally has a named, checkable home — a
connector's grep finds it; no sibling ground moves). Calibration ↑ (the fence's ownership is
pinned to the same blob the counter scores — an undated drift between "the fence that is ours"
and "the fence under test" becomes a diff, not an interpretation). Harm: none — no sibling text
changes, no claim file edit, no C2 surface touched; the append is one paragraph in the lane's
own append-only section, the established per-round admission form (rounds 28–38 all appended
this way).

## Risks

- Appending mid-round is out of freeze scope — the proposal is for the *wrap-up* append, the
  normal per-round admission paragraph; L1 decides timing. If L1 prefers, it lands verbatim as a
  "Reported out" line instead — same effect, smaller claim.
- "Lane-owned" language could read as scope inflation; mitigated by citing the existing
  `:282-284` fleet-pattern line that already establishes the method/instance split.
- Rows 5, 10 are harness/precondition observations, not defect claims — if the v3 counter's env
  discipline diverges from the frozen parent, row 5's "unreachable" conclusion must be
  re-derived; flagged so no one cites it blindly.

## Verification

- Freeze ancestor + predate + blob equality: shown above (merge-base, rev-parse ×2, diff --stat
  empty, committer-date vs measured time).
- All PROVINCE citations re-grepped for line numbers; each quote ≤25 words, verbatim.
- Contradiction stated, not smoothed: C1's frozen text claims the fence is "the self-assessment
  under test" while the lane's province does not list that instrument — the proposal resolves the
  contradiction by declaration, not by re-scoring.
- No scored counter/probe was run by this seat; no admission of R49-C1 or R49-C2 is claimed;
  nothing in the lane tree was modified (only this report file under `w1/`).

VERDICT: scan complete — no sibling lane claims fixture-fencing ground; tameshi owns the method
(every lane's gate its own), kengaku's fence instance is undeclared in its own PROVINCE; proposed
bounded move = L1 append-only ownership declaration citing both sides of the boundary; report-out
to L1 only, absorb all craft precedents (souji r14 strace fixture, kasegi containment matrix,
mado→tameshi runner-pin form); kama R0 ablation-floor caveat absorbed for mutant authors.
