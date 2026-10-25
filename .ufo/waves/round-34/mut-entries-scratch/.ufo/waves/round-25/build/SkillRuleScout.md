# SkillRuleScout — R25 SKILL.md rules for pass bars / min-n / power (read-only)

Base read: lane 6180e4f. Lane-local `PROTOCOL.md`/`AXES.md` absent (`find` at lane root empty); the files the pre-registration cites are fleet-root only.

## Measurement rules — SKILL.md:403-466 (numbered 1-13)
- :403-404 header says "all four were violated at least once in r8" — stale: the list holds 13 rules, and rules 2,8,10,11,12,13 cite r9/r11/r12. Fix the count when appending, do not inherit it.
- MR1 :406-408 unit = problem/seed, never request — the governing precedent for P1's identical-block dedup (count once).
- MR2 :409-412 ESS discount; sign test needs **n≥10** unanimous pairs or **n≥17** with one discordance; "Report exact binomial p as an *upper bound*". A min-n/power rule, not a CI rule.
- MR8 :425-428 pre-registered decision rule with three outcomes — blocks / survives / indeterminate — "and report which fired". Structural precedent for INDETERMINATE, but its own bar is a point fraction (INC 4/8 vs ≥5/8, :427).
- MR10 :433-440 paired contrasts; shrink the prior effect size; "size n for it, and let the verdict rule fire".
- MR11 :441-450 ordered test; seeded-MC power; "minimum n for 80% power = 12"; binding risk is anchor validity.
- MR13 :460-466 absorb critic defects pre-hash so the hash covers the corrections.

## Anti-patterns — SKILL.md:60-177 (numbered 1-19)
- AP13 :120-126 do not assume a grader's `ok` is the claim's conjunction; mutation-test graders (50 cases → 1 live defect).
- AP14 :127-133 "A stored SUMMARY no one can re-derive is a claim, not a measurement" — commit bytes + recompute command, "prove it can fail" (:131-133). Strongest existing warrant for C1 re-verdicting stored receipts.
- AP17 :154-160 an asserted power floor is a measurement: compute it with a committed seeded script and cite the number (42 pairs → 0.791 at the filed dz). Directly constrains C1's n=17 ask.
- AP18 :161-168 never pool heterogeneous forecast events into one Brier; report per set/subgroup.

## Production checklist — SKILL.md:558-597 (numbered 1-9)
- item 1 :558-580 report the pre-registered verdict "even when it is *indeterminate*" (:566-568); "file a power analysis fixing n and the MDE, and hash it with the predictions" (:570-573).
- item 5 :586-588 ≥4 tasks per mechanism class; item 7 :591-593 repeat near-boundary tasks (n≥2).

## Does any rule already require an interval lower bound for a PASS? — No.
- `grep -n -iE "interval|lower bound|upper bound|confidence|clopper|wilson|posterior|credible" SKILL.md` → only :297 and :412.
  - :297 "report pass-rate with block-robust intervals, not per-draw Wilson" — a reporting rule in the route-telemetry section for interior-p̂ tasks; it gates no PASS/FAIL verdict.
  - :412 "Report exact binomial p as an *upper bound*" — a type-I bound for the sign test, not a proportion CI.
  - `grep -c -iE "clopper|wilson|confidence interval" SKILL.md` → 1 (the "per-draw Wilson" rejection); zero Clopper mentions.
- `grep -nE "\bbar\b" SKILL.md` → :618 only ("admission bar"): SKILL.md contains no numeric pass bar. The 0.80 bar in C1 is receipt-sourced, matching pre-reg ("the receipt's own stated bar").
- Only lower-bound-like construct: :380-381 TrueSkill `μ−3σ` sort key — a judge-ranking key, not a PASS gate.
- Existing verdict thresholds are all point fractions: ≥5/8 survival (:427, :568); n≥2 repeats (:593).

## Where a new rule slots (numbering)
- Measurement-rule list 1-13 ends at :466 → new rule = **14**, inserted after :466 (before the :468 scope-limit paragraph). MR14 needs its own scope sentence: :403-404 scopes the list to the r8/r9 probe family, while C1's population is the attribution receipts.
- Anti-pattern list 1-19 ends at :177 → new anti-pattern = **20** (e.g. "a point PASS read as an interval PASS"). Precedent: AP17(:154) pairs with MR11(:441) as rule+anti-pattern.
- Production checklist 1-9 ends at :597 → new checklist item = **10**, only if the rule must fire at run-request time; otherwise it duplicates MR14.
- Recommendation: operative verdict text at MR14, AP20 only for the named failure mode; bind the bar to the source document, never to a lane default.

## Risks the rule text must absorb
- MR2's n≥17 (:410) and C1's n=17 power ask are unrelated derivations that coincide numerically. Verified: `python3 -c "0.025**(1/n)"` → n=16 0.794093, n=17 0.804936 (matches pre-reg 0.7940/0.8049). MR2 counts discordant substrate pairs for a sign test; CP's is a zero-error lower bound. Do not cite MR2 as authority for the CP floor.
- MR8 gives three outcomes; C1 adds a fourth (UNTESTED, n=0). Declare it as an extension rather than silently appending to "blocks/survives/indeterminate".
- Novelty-sweep hazard: the pre-reg's before-sweep (`grep -rlE 'Clopper|Wilson|confidence interval' corpus/evidence/attrib-* plans/attrib*`) does not cover SKILL.md. If MR14 lands, `Clopper` enters SKILL.md; record the sweep transcript before the edit or state the sweep's scope, else a widened sweep reads the new rule as pre-existing construct.
- MR1 (:406) already supports the pre-reg's dedup ("one sample, counted once"); cite it in the receipt parser, not as a new rule.

No installs. No network. No writes outside this report.
VERDICT: No SKILL.md rule requires an interval lower bound for PASS — the file has no numeric pass bar, its min-n rules are sign-test/ESS rules (MR2 n≥17), and its only verdict-outcome precedent is MR8's three-outcome point threshold; a Clopper–Pearson lower-bound rule is new and slots as measurement rule 14 (optionally paired with anti-pattern 20), with the bar bound to the source receipt.
