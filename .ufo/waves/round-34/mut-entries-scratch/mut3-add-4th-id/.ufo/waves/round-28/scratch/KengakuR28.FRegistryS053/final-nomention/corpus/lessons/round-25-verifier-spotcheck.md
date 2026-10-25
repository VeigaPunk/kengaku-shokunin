# round-25 — non-author verification and spot-check (kengaku, hyaku)

author: hyaku closure (non-author integrator, @m_opus)

Written by the integrator of record, not the lane. Lane round 25 was closed against lane tip
`9d8a00d2a69b83a1e83eb41e1d2ee840910949e4` (base `6180e4fb92e90c0b172e9788e2c765d097f2e142`) and fleet report
`.ufo/reports/round-25/kengaku.md` at `c163a044`. I did not author this round and did not improve it: every
number below is one I re-ran over committed bytes, or a committed receipt I verified; the lane's instruments
were not executed (Gate standard: the integrator verifies a gate's committed evidence, never runs a sibling gate).

Driver digest copied from `.ufo/watchdog.log` (mutable, so recorded here):
`2026-10-20T21:05:24-03:00 launch kengaku round=25 pgid=2568413 driver=hyaku-inline attempt=1`;
`2026-10-21T00:34:26-03:00 complete kengaku round=25; hyaku-inline attempt=1`.

## Conformance (step 1)

- Report `c163a04` is committed in the fleet repo by `kengaku-shokunin <kengaku@shokunin.local>`
  (`git log --format='%an %H' -- .ufo/reports/round-25/kengaku.md`).
- Every cited lane commit exists and is an ancestor of `refs/heads/master`:
  `3f371d2` pre-registration, `710409f` Amendment 1, `8ea41f9` integration, `8239a56` falsify-wave revision,
  `9d8a00d` close — five of five `merge-base --is-ancestor` checks pass against the branch ref (HEAD is detached).
- Lane state: `jj-lane.sh state` → `branch=master local=9d8a00d2 remote=9d8a00d2 ahead=0 behind=0 head=detached
  tracked=0 untracked=0`; `git -C kengaku-shokunin status --porcelain` prints nothing.
- The committed report carries the `## SHONEN` heading with one line per box (four `[~]` lines, four pointers).
  SHONEN.md itself: 4 boxes, exactly one evidence line each (`shonen_evidence_lines_per_box=1,1,1,1` in the
  committed census receipt); pointers `SKILL.md`, `LOG.md:7`,
  `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`, `PROVINCE.md:129` all resolve.
- Dispatched prompt `.ufo/prompts/kengaku-round-25.md` is the shipped `templates/round-prompt.md` rendering plus the
  hyaku §6 addendum (diff is substitutions only). It carries the round-level items (mission/axes binding, 1–3
  falsifiable claims with the lowest-axis rule, ≥8 L2 in one batched call, commit-then-push ordering, push scope,
  L0 side channel) and the five child-lane items (report path/filename, commit-before-report ordering, SHONEN
  heading requirement, commit-hash citation rule, write scope). No L2 route map is quoted — §3 binds the host
  route table and forbids hard-coded aliases — so there is no route map to contradict `MISSION.md` §L2.
- L0 side channel: the two questions in the report's `## L0 questions` are filed at `.ufo/l0-questions.md:72-73`
  (`grep -n "kengaku | round-25" .ufo/l0-questions.md` → two rows).
- Report defect (status-neutral): the Gate table **as landed** at `8ea41f9` (commit time 21:44:48 -03) already
  claims the entry's Q10 numbers were re-derived "by wave-2 seats"; the falsify wave began after that commit
  (first wave-2 report mtime 21:49:53 -03). Evidence cited before it existed is a §Evidence-standard defect at
  the landing commit. The tip text is true — the wave-2 seats did run — but the landing claim was not.
- Fleet repo: report commit is contained in `origin/master`; the only unrelated porcelain entries are the
  driver's mutable `.ufo/watchdog.log` and operator-side `.ufo/state/*.report-baseline` files (not lane debt).

## Claims — re-check

### C1 — novelty (→ coverage/constructs), capability `interval-reverdict`

Commands re-run over committed bytes, observed output:

- `git cat-file -e 6180e4f:plans/attrib_calibration.py` → `fatal: … not in '6180e4f'` (exit 128): the instrument is
  absent at base, as the before-state says.
- `git grep -nE 'Clopper|Wilson|confidence interval' 6180e4f -- corpus/knowledge` → 6 hits, all in
  `attrib-r21.md`, all descriptive Wilson text (no exact, per-leg or verdict-carrying interval).
- P1 pin: the nine `attrib-r2[123]-*.log` receipts against `P1_SHA256` in `plans/attrib_calibration.py` →
  **9/9 MATCH**; `git diff 6180e4f 9d8a00d -- corpus/evidence/attrib-r2*.log` is empty (no receipt was edited).
  The population glob `corpus/evidence/attrib-r[0-9]*.log` returns exactly those nine files.
- `grep -c '^corpus/evidence'` / `grep -oE 'interval=(PASS|INDETERMINATE|UNTESTED|-)'` over
  `corpus/evidence/round25-calibration/attrib-calibration-summary-v2.txt` → 53 evidence lines; `interval=PASS 7`,
  `interval=INDETERMINATE 11`, `interval=UNTESTED 12`, `interval=- 23`; stored verdict lines **7**;
  `transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4`; TOTAL
  `estimates=35 PASS=7 FAIL=0 INDETERMINATE=11 UNTESTED=12 shares=12 n_ge_17=12 stored_verdicts=7 stored_checks=119
  mismatches=0 unique_samples=4 scored_trials=92 correct=92`. Report's "35 estimates, PASS 7 / INDETERMINATE 11 /
  UNTESTED 12 / 5 non-firing" is consistent (7+11+12+5 = 35).
- CP anchors over `plans/fixtures/r25/cp_reference.tsv`: 16/16 lower `0.794093`, 17/17 `0.804936`, 20/20
  `0.831567`, 22/22 `0.845627`, 30/30 `0.884297` — matches the entry's table and the pre-registration's n=17 ask.
- Independent oracle receipt `attrib-oracle-intervals.txt`: `cp_selfcheck=ok max_abs_err=3.1e-16`,
  `VERDICTS(dedup) recall: PASS=2 FAIL=0 INDETERMINATE=5 UNTESTED=5`, exit 0 — matches the entry's per-leg count.
- Selftest evidence (verified, not executed): `attrib-calibration-selftest-v2.txt` ends
  `selftest: 18 checks, 0 failed`, exit 0, with red runs R1–R6 printed; SKILL.md's registry row also says 18 checks.

Reported 7 → 7 (held) is accurate: the observable moved (0 interval-carrying verdicts → 30 verdict-bearing
estimates of 35; stored verdicts re-verdicted 0/7 → 7/7), and the +1 is capped by `SCORECARD.md:244`
("a phenomenon already published — keep as replication, not contribution"), with cigate 0.2.0 as S041.
**Axis verdict: `improved` (observable), score held 7** — admissible under the round-24 ruling that a held
score stands when the declared observable moved; the +1 itself is *not* credited.

### C2 — calibration, capability `state-assertion-check`

- Base census, run by me over `git show 6180e4f:corpus/SOURCES.md`: rows **26**, tiers `A=24 C=2`,
  status `mined=18 queued=5 rejected=3`. Base capability cell `SCORECARD.md:557` claims `rows 25 … A=24 C=1 …
  rejected=2` — the mismatch R25-E1 corrects, reproduced independently.
- Tip census over `corpus/SOURCES.md`: rows **42**, tiers `A=38 B=2 C=2`, status `mined=30 queued=9 rejected=3`,
  malformed rows 0 (42 rows × 11 fields). Report's 26 → 42 with +14 A / +2 B is exact.
- SHONEN canonical form: 4 boxes, one evidence line each; the protocol seed's box texts match modulo `<name>`.
- Committed receipts: `state-check-before-6180e4f-v2.txt` →
  `assertions=241 match=228 mismatch=10 superseded=0 offline_unverifiable=3`, `VERDICT: FAIL`, exit 1;
  `state-check-after-v2.txt` → `assertions=235 match=231 mismatch=0 superseded=1 offline_unverifiable=3`,
  `VERDICT: PASS`, exit 0, with `SUPERSEDED … correction_exact: true, correction_line: 646` for
  `P2a.capability.sources-registry`. `state-check-selftest-v2.txt` → `[selftest] ALL PASS`, exit 0.
- D17/D18: SKILL frontmatter parses as YAML (PyYAML: keys `description,name`; description contains quoted
  `Triggers:`, `Anti-trigger:` and `Sibling arbitration:`); the round census receipt says
  `skill_frontmatter_yaml=valid`.

**Axis verdict: `improved` (observable), score held 8** — base 10 → tip 0 on the frozen P2 population, one exact
supersession, instrument + selftest. The r24 ruling applies again.

- Defects found in the round's own *new* text (out of the frozen P2 population; the receipt marks both new
  capability rows `OUT_OF_POPULATION`, so state_check did not cover them):
  1. `SCORECARD.md:559` (`state-assertion-check`) still prints base `mismatch=11`; the corrected v2 receipt and
     the same file's revision line 719 say **10**. The correction exists only in the revision prose, not as an
     `R25-E*` row against the capabilities table.
  2. `SCORECARD.md:558` (`interval-reverdict`) says `--selftest 14 checks`; the v2 receipt and the SKILL registry
     say **18**.
  3. `PROVINCE.md:119` says the registry "holds 37 after round 25"; the tip registry holds **42** (the line was
     written before S038–S042 landed and has no correction).
  These are the exact class C2 exists to catch; they are routed below, not score-changing.

### Separability / no-axis-harm

`SCORECARD.md` diff base→tip rewrites no existing table row (`git diff … -- SCORECARD.md | grep '^-|'` prints
nothing); the diff adds the round-25 section and appended corrections. PROVINCE adds dated `ABSENT` markers to
five surface rows and two surface rows — no surface is removed; SKILL adds rule 14 and two registry rows;
SOURCES is 24 added / 1 changed line (S011 used-by). No owned axis score falls.

## Spot-check (LEARNING.md — at least one admit and one reject)

| item | decision | re-opened source (my fetch, hash) | agree / disagree | reason |
|---|---|---|---|---|
| `knowledge/attribution-interval-calibration.md` | admit, judged at tip with §Corrections | S030/S042 PDF `zero_numerator.pdf` — sha256 `e3150aec…` **MATCH**; quote "we can be 95% confident … three in n (ie, 3/n)" on PDF p.2 = printed p.1744. S027 SciPy page — sha256 `f814ec0f…` **MATCH**; "‘exact’ : Use the Clopper-Pearson exact method [1]." under Parameters→method. S041 PyPI JSON — sha256 `318b81e5…` **MATCH**; version 0.2.0, summary carries the quoted gate sentence. S011 PMLR PDF — sha256 `c1645e31…` **MATCH**; "Substituting estimates q̂1 and q̂0 into (4) gives the bias-corrected estimator" in §4.1, p.4 left column, before eq. (5). S040/S035 arXiv PDF — sha256 `a16bf2c1…` **MATCH**; §4.2.2 "Label shift", p.16, "Central to our analysis will be the confusion matrix", Theorem 3 | **disagree at first landing; agree at tip** | At `8ea41f9` the entry's S030 anchor said p.1 (quote is printed p.1744), S032 said "final sentence" (4th of 5), S011 said §4.2 (§4.1); the gate's Q10 second-seat location re-read had not run. The tip's §Corrections plus superseding rows S039/S040/S042 correct all three, and the tip entry clears Q1–Q12. The *landing decision* admitted an entry that failed its own Q10. |
| "rule of three as the verdict rule" | reject | `plans/fixtures/r25/cp_reference.tsv` and the frozen rule in `plans/round-25-claims.md` | **agree** | One-sided 3/n passes 15/15 and 16/16 at bar 0.80; exact two-sided CP95 lower is `0.781981` (15/15) and `0.794093` (16/16) — INDETERMINATE; 17/17 is `0.804936` PASS. The reject and its flip condition (an operator ruling that one-sided bounds suffice) are sound. |
| "prediction-powered inference (S035) as the share correction" | reject, reason superseded | arXiv 2301.09633 v4 PDF (same fetch as S040) | **disagree with the as-landed reason; agree with the reject** | §4.2.2 "Label shift" does infer class shares through the confusion matrix (Theorem 3), so the landed Q9 reason ("not classifier sensitivity/specificity") was a non-sequitur. S040 supersedes S035, the reject stands, and the entry's §Corrections records it (M33). |
| new row S038 | — | Cambridge PDF URL | **could not re-open** | HTTP 429 from this network (363-byte challenge page; hash not reproduced). `gate.md` already says re-verification of dynamic pages is by quote/location; not counted as verified here. |

New SOURCES rows checked: S027, S030/S042, S040/S035, S041 (hashes reproduced) and S011 (hash reproduced).
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, exit 0, one
`W04 S040 duplicate url arxiv.org/abs/2301.09633 across scopes` — exactly the warning the report names.

## Trend verdicts

- **expansion: harmed.** The round's net new admitted entry is `knowledge/attribution-interval-calibration.md`.
  At its landing commit `8ea41f9` its cited locations were wrong in three places (Q10) and the round's PPI reject
  reason did not follow from its evidence (Q9). `LEARNING.md`'s expansion row is explicit: harmed when "an admitted
  entry fails the bar it was admitted under"; the kagi r21 closure rule is the same fact pattern — "errata were
  appended by the lane, but the admissions failed their own bar at landing". The in-round §Corrections and
  S039/S040/S042 repair the record but do not convert the landing decision into one that passed. The counter-reading
  (judge the gate at the tip, where the corrections are in) would give `improved`; it is recorded here and not taken.
- **quality: unchanged.** Nothing false or stale is left unmarked in the corpus (the r22 "hyper validated" reading is
  marked by R25-E6 and `attrib-r21.md` §Erratum; the entry's slips are superseded), so not harmed. The new entry
  failed its own re-check at landing, so the `improved` clause's proviso does not hold either.
- **discernment: unchanged.** The outside check agrees with the sampled reject and disagrees with the landing admit;
  that disagreement was already mined as M33/M34 and did not add a QUALITY criterion (Q10 predates the round). The
  round's own Q11/Q12/R11–R15 are grounded in wave-2 lessons, but wave seats are the lane, not the outside check.

## Adjudication

**REJECTED-HONEST-STOP.** Both declared claims verify (C1 `0 → 35` estimates and `0/7 → 7/7` re-verdicts with the
nine receipts pinned; C2 `10 → 0` on the frozen P2 population with the base mismatch independently reproduced);
both capabilities are demonstrated; no axis is harmed. The round is not admitted because its net expansion failed
its own Q9/Q10 at landing, which the campaign's prior ruling treats as an expansion/quality trade — the honest stop
is on the round's admission, not on the work, which stays in the lane. If the operator prefers the tip-corrected
reading, only the `admitted` field changes; the trends stand as measured.

Routed to the lane for round 26 (append-only fixes, never rewrites):

1. `SCORECARD.md:559`: base `mismatch=11` → `10` (v2 receipt); add an `R25-E*` row against the capability cell, not
   only the revision prose.
2. `SCORECARD.md:558`: `--selftest 14 checks` → `18 checks` (v2 receipt; SKILL registry already says 18).
3. `PROVINCE.md:119`: "holds 37 after round 25" → 42 (or a correction naming S038–S042).
4. Landing-time Gate: never cite a seat that has not returned; `8ea41f9`'s Q10 cell named the wave-2 seats before
   the first wave-2 report existed.
5. Keep the out-of-population list complete: the two new capability rows are currently outside state_check's frozen
   population; pin their numbers when the round-26 calibration claim content-pins the remaining anchors.

Routed to the ledger, not rewritten: `MANIFEST.json:2744`'s "hyper COVERED (run-2 10/10 = 1.000)" is an overclaim
under the exact CP95 rule (INDETERMINATE on the registered population; PASS only pooled with run 1). The historical
row is closed history and stays byte-identical; the lane's R25-E6 erratum and the entry §Corrections carry the
corrected reading, and the closure entry records the pointer. The lane's report-out to kumitate is accepted as a
report-out (leg-share bounds are within-P1 shares, never natural fallback rates).

## Verification inventory

- **Re-measured by me (commands above):** C1 base absence and widened sweep; 9/9 receipt sha256 vs the frozen
  manifest; C1 summary counts and transitions; CP anchors; oracle tally; base/tip SOURCES census and tier/status
  histograms; base capability-row mismatch; SHONEN boxes and pointer resolution; SKILL frontmatter YAML; report
  author/commit and cited-commit ancestry; lane state and porcelain; prompt/template fidelity and contract items;
  L0 filing; wave report counts (92 + 87) and registry member counts; misroot sweep (fleet copies absent, lane
  copies present); sources-census validate.
- **Evidence-verified, not executed:** `state_check.py` before/after/selftest receipts, `attrib_calibration.py`
  summary/selftest receipts, round census receipts, wave registries/specs.
- **Not verified:** S038's hash (HTTP 429); the "no dead seats" claim is consistent with 179 committed seat reports
  and two registries but seat liveness is not observable post-hoc; the lane's gate/instrument binaries were not run.
- No tool was installed or updated by this closure; no model parameter was passed; no routing or config changed.
