# R46CritC1Freeze — stage-1 C1 freeze attack

Scope: frozen C1 text in `plans/round-46-claims.md` at `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f`; read the frozen text first and compared the claim with round-45 closure §2/§5, Q39, the frozen fence and counter, and the named held-out reports. No counter, fixture, or probe was run. Axis: **calibration**.

## Findings

### 1. Held-out evidence is miscounted and changes the advertised baseline

Frozen claims `plans/round-46-claims.md:29-31` says “9 of 14” held-out hostile modules, adding the VERDICT numerators/denominators as if all units were modules. Those reports do not use a consistent denominator: e.g. `R45HoSymlinks.md:20` says `modules=1 fixtures=5 admitted=2`; `R45HoIncludeIf.md:37` reports four modules including h4 controls, while its `:41` says three hostile modules; `R45HoCommondir2.md:143-145` says four modules, two admitted; ArgvEnv and ConfigKeys each report one module. The closure correctly normalizes hostile modules in `round-45-verifier-spotcheck.md:65`: 8 of 10 (3 IncludeIf + 2 Commondir2 + 1 Symlinks + 1 ArgvEnv + 1 ConfigKeys). This is not just a typo: C1's expected baseline and any `<R>` derivation need a canonical unit and inclusion rule. The round-45 C1 source itself counts a module as contradicted if any fixture admits/reads (`round45_c1_verify.py:289-305`), not by adding fixture-level verdict numerators.

**Smallest correction:** replace the claims sentence with: “The closure counted 8 of 10 held-out hostile modules admitted (IncludeIf 3, Commondir2 2, Symlinks 1, ArgvEnv 1, ConfigKeys 1; closure §2); module verdict is one per hostile module, admitted/read if any fixture admits/reads.” Then require converted modules to use that same aggregation.

### 2. Two-stage freeze does not freeze the entire stage-1 contract

`round-46-claims.md:17-22` calls the predicate, counter contract, controls and kill rule frozen, but stage 2 only says it may not change “a predicate line, a control, or a kill rule.” The detailed counter contract at `:32-45` is not explicitly protected by that prohibition. An L1 could amend (f) to count only selected scratch subtrees, narrow (g)/(h), drop modules from (c)/(d), or weaken log/verdict handling while technically leaving the named predicate, control list and kill rule untouched. Those changes alter what the predicate means, despite the stated freeze.

**Smallest correction:** add after the stage-2 permission sentence: “Stage 2 may change only the literal values and input-pin entries named above; every other stage-1 C1/C3 contract sentence, including counter legs, membership/retention rules, and measurement semantics, is immutable; any necessary change requires an explicitly named pre-data freeze amendment and renewed controls before scoring.”

### 3. `contradicted` is the right unit only if membership is fixed; current count is under-specified

The round-45 precedent defines the count per hostile module and marks it contradicted if any fixture is admitted/read/hung or build fails: `round45_c1_verify.py:289-318` (note its actual expression double-counts build errors, although the all-zero predicate conjuncts separately prevent a false pass). For round 46, `CALIBRATION advertised=<R+S> contradicted=0` is sensible as the count of advertised hostile modules that contradict the fence, **provided R and S enumerate all eligible modules and use that per-module aggregation**. But `R`/`S` are stage-2 literals derived from a filtered set: (c)/(d) retain a module only if the base fence is “LEAKED or READ”; no minimum, complete source inventory, or disposition for build errors/invalid conversions is frozen. A dropped/unbuildable module silently reduces `advertised`, while the base fence's known miss can also be missed by the old counter's limited definition of READ (round-45 critic B3/B5/B6; the stage-1 wording does not require a whole-host measurement). Separately, the predicate exposes no calibration term for honest fixtures; it does require the HONEST leg exactly, so this is not a pass loophole, but `advertised` should be described as hostile-module coverage, not the whole SCORECARD advertisement.

**Smallest correction:** define `contradicted` as `count(hostile modules with ≥1 admitted, read, hung, or unbuilt/invalid fixture)`; require every candidate hostile module to be retained or listed with a specific, evidence-backed exclusion, with zero build/conversion errors; pin the expected module inventory and require `advertised=R+S` to equal that inventory. State explicitly: “This is a sampled calibration count, not a claim that the frozen corpus exhausts the SCORECARD capability.”

### 4. Measurement boundary and unresolved B7 weaken the calibration meaning

The fence docstring says the process tree must never open outside `d` (`plans/fixture_fence.py:8-9`); the claims identify the broader SCORECARD/docstring promise as deciding without reading outside `d` (`round-46-claims.md:26-28`). Yet counter contract (f) only counts opens under “the whole scratch root” (`:41-42`), leaving host paths outside scratch (e.g. `/etc`, `/proc`) outside its measurement. The named round-45 B3 example already demonstrated host-read as a bypass (`R45CriticPredicate.md:50-60`). The contract's exception for harness/fence copy is not scoped to paths or access type, and (g)'s “stat-family” does not enumerate metadata/content-returning calls such as `getxattr` (round-45 B5 explicitly names it, `R45CriticPredicate.md:70-77`). Finally B7 is left as a limit “unless blocked cheaply” (`round-46-claims.md:44-45`), granting stage 2 discretion over whether to close a demonstrated invisible read channel.

**Smallest correction:** either narrow the self-assessment explicitly to the measured scratch threat model, or say “any fence access outside `d` that can return path, metadata, or file content is a contradiction, including host paths; the log is out-of-band and tamper-evident; count/deny `io_uring` (or list it as a fixed, explicitly unverified limit that bars an unqualified pass).” Enumerate syscall classes rather than relying on “stat-family.”

### 5. The wave-2 kill rule is binding in outcome but not in coverage or threshold

The rule at `round-46-claims.md:58-60` is outcome-binding (“C1 not admitted”) and has provenance in closure §5, item 7, but it has no minimum number of wave-2 modules, no per-module test protocol/measurement semantics, and no fallback if none are authored or reported. Two-or-more threshold also tolerates one admitted/read module, unlike the frozen wave-1 predicate's zero tolerance. A wave-2 suite with zero or one module therefore leaves the rule practically vacuous/too weak; counts of HUNG/build-error modules are also not addressed by “admitted or read.”

**Smallest correction:** “Wave 2 must report at least N independently authored, successfully built hostile modules, each evaluated against the landed fence with the frozen counter semantics; any module admitted, read, hung, or not successfully tested makes C1 not admitted.” If retaining the `>=2` threshold, explain why one contradiction is accepted and identify that as a deliberately weaker post-freeze kill criterion; do not present it as equivalent to the zero-defect frozen predicate.

## Judgment

**Predicate reachable without the work?** The stage-1 text materially improves the Q39/Q31/Q37 design: random names and shuffled jobs, a required keyed control against remaining exposed names/structure, and an explicit stop if a control passes directly address the round-45 name-keyed bypass. However, I cannot say reachability is ruled out by this freeze: the counter is not yet pinned, contract amendments are not fully forbidden, the module inventory can shrink, and the measurement semantics retain an explicit B7 discretion plus incomplete path/call coverage. The safest classification is **fixable freeze defects**, not proof that a future counter must fail.

**Verdict-changing gaps:** (1) count/denominator mismatch in the frozen historical premise; (2) stage-2 may alter counter semantics outside the named freeze protections; (3) eligibility/inventory can shrink `R+S`, making calibration vacuous on omitted or unbuildable adversaries; (4) a wave-2 run with too few modules or one admitted/read can still satisfy the kill rule. Measurement-boundary omissions additionally make the advertised “without reading outside d” claim broader than the defined counter.

## Evidence locations

- Frozen claims: `plans/round-46-claims.md:15-60` (freeze scope; C1 advertisement, contract, predicate, controls, kill rule).
- Closure normalization: `corpus/lessons/round-45-verifier-spotcheck.md:63-71,153-155`.
- Per-module semantics: `plans/round45_c1_verify.py:289-323`.
- Fence promise: `plans/fixture_fence.py:1-17`.
- Q39 / known limits: `corpus/QUALITY.md:1059-1087`.
- Host-read / metadata / pending-open evidence: `.ufo/waves/round-45/w1/R45CriticPredicate.md:50-60,70-89,91-95`.
- Held-out unit examples: `.ufo/waves/round-45/a3w1/R45HoSymlinks.md:20`, `R45HoIncludeIf.md:33-42`, `R45HoCommondir2.md:143-147`.

VERDICT: c1-freeze-gaps-5-verdict-changing-4