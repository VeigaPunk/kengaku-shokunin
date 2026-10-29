# W2RevReportDraft — round 52 wave 2 (falsify), reviewer seat

Role: reviewer (read-only pre-review of the round report contract). Lane: kengaku. Basis tip: master `87301bacca90c03fa915716fbe6d7023762c5ab3` (`jj-lane.sh state` → local=remote=87301bac, ahead=0 behind=0, untracked=16).

## 1. What was attacked
- The round-52 report does NOT exist yet: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/kengaku.md` → absent (the directory holds only round-51 and earlier reports). Per the item, the requirements were reviewed instead.
- Requirement sources: `.ufo/prompts/kengaku-round-52.md` §2, §2b, §4, §5, §6, §10; `plans/round-52-claims.md` (frozen at 1315234, Amendments A1–A5); `PROTOCOL.md` §Gate standard, §File contract, §Promotion gates; `LEARNING.md` trend table; `SHONEN.md`.
- Incidental attack on the landed R52-C1 instrument, because the claims must be measured against it: `plans/round52_c1_grader_audit.py` (candidate and confirmation logic) vs Amendment A1.
- Full checklist: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevReportDraft/report-requirements.md` (copy of the scratch checklist).

## 2. Commands run (all read-only against the lane; the counters ran on a `git archive` copy of master in scratch)
```
sed -n / read on .ufo/prompts/kengaku-round-52.md (1–689), plans/round-52-claims.md (1–311), PROTOCOL.md, LEARNING.md
ls .ufo/reports/round-52/                                  → directory has no kengaku.md
jj-lane.sh state …/kengaku-shokunin                        → branch=master local=remote=87301bac ahead=0 behind=0 untracked=16
git rev-parse master                                        → 87301bacca90c03fa915716fbe6d7023762c5ab3
git log --oneline -8 master                                 → 87301ba … 1315234 (freeze), 30801b4 (base)
git archive master | tar -x -C /fast/scratch/hyaku/kengaku-r52/w2-W2RevReportDraft/tree
python3 plans/round52_c1_grader_audit.py --lane .          (in archive copy, TMPDIR=scratch) → exit 1
python3 plans/round52_c2_registry.py --lane .              (in archive copy, TMPDIR=scratch) → exit 0
sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku → exit 0 (warnings W04 only)
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md → 171 (master) ; same on 30801b4 → 171
awk over SKILL.md '## Gate/probe registry' → 76 table lines (74 data rows + header/separator)
sed -n 127,131p PROVINCE.md | cat -A                        → line 129 is empty
ls .ufo/waves/round-52/claims | grep -ci control            → 0
python3 json probes of w1-results.json, w2-dispatch.json, w2-spec.json (seat counts, agent roles)
```

## 3. Measured numbers
R52-C1 counter at master 87301ba (literal):
```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
CANDIDATES total=29
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
LABELS agree=0 of 0
PREDICATE R52-C1 fail        (exit 1)
A5 EXCLUDED listed=1 digest_pinned=1 tasks=['sanitize-git-repo']
A5 CAPTURES present+pinned_excluded=184 of 184
A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 fail
```
R52-C2 counter at master 87301ba:
```
ADVERTISED total=72
REGISTERED total=72 rows=74
MISSING 0 / INCOMPLETE 0 / ENTRY-MISSING 0 / SELFTEST-UNBACKED 0
PREDICATE R52-C2 pass        (exit 0)
```
Census at master: exit 0; SOURCES registry rows 171 (base 30801b4: 171; unchanged).
Wave shape: wave 1 = 35 seats (w1-results.json; roles executor 10, scribe 7, scout 5, reviewer 5, critic 3, connector 2, revenger 2, mutation 1; no labrat). Wave 2 = 33 seats (w2-dispatch.json counts.total 33; reviewer 7, critic 3, mutation-tester 2, executor 10, scribe 4, scout 3, connector 2, revenger 1, sentinel 1). Attack share: wave 1 9/35 = 25.7%; wave 2 12/33 = 36.4%.
Control receipts: 0 of 8 present under .ufo/waves/round-52/claims/.
Stale receipts present: claims/c1-after.txt (CAPTURES present=89, TASKS classified=89, pre-A2/A5); claims/c2-after.txt (SELFTEST-UNBACKED 1, PREDICATE fail, pre-A3).

## 4. Findings (ranked; each a checklist item in report-requirements.md §G)
1. **R52-C1 has not landed.** `corpus/evidence/round52/confirmations.json`, `prior-art.md` and `labels.json` are absent at master. Legs 3 (CONFIRMED new ≥2) and 4 (PRIOR-ART ok, urls ≥3) fail; the literal predicate is `fail`, exit 1. The A5 line does not change this verdict (it still prints `R52-C1-A5 fail`). Landing attack: a report that says "pass" or cites the A5 line as the verdict is wrong. **This attack LANDS against any pass claim; it does not land against the instrument's own arithmetic.**
2. **Control receipts absent.** None of c1-control-nothing / -name-only / -blind-class / -drop-capture, nor c2-control-nothing / -empty-cells / -drop-row / -false-selftest, exist under `.ufo/waves/round-52/claims/`. The frozen claims require each to fail its predicate with a receipt.
3. **Stale after-receipts.** `claims/c1-after.txt` and `claims/c2-after.txt` predate A2/A3/A5; the report must cite the final landing-commit run.
4. **A1 implementation gap (landed counter).** `plans/round52_c1_grader_audit.py:193` sets `candidate = bool(p1) or cls in ("V1","V4")`. The CONFIRMED gate at `:308` (`if not rec.get("candidate")`) uses that flag. Amendment A1 defines a vacuity candidate as "≥1 of its tests is P1". The file-level OR admits tasks with zero P1 tests; `pytorch-model-recovery` and `torch-tensor-parallelism` (which the A1 text itself says are misclassified at file level) are in the CANDIDATES list (`CANDIDATE … class=V1 presence_only=-`). The per-test P1 totals (`p1_tests`, `p1_tasks`, computed at `:324–325`) are never printed, so the A4 figure (P1=33 across 27 tasks) cannot be re-derived from the counter output. Either fix the candidate rule to A1 (and disclose it as an implementation amendment, not a threshold change) or disclose the OR as a known gap. Not a predicate change either way.
5. **Wave shape deviates from the frozen claim.** Claims freeze "two v1 waves, total 64 (32 + 32)". Actual 35 + 33 = 68. Inside the run-11 64–128 band; the deviation still needs naming in the report.
6. **SHONEN box 4 pointer does not resolve.** `SHONEN.md` cites `PROVINCE.md:129`; line 129 is blank. The other three pointers resolve (LOG.md:7 = "round 4" line; corpus/lessons/round-8-aggregator-box3-coldrun.md:48 = `## Box-3 verdict`; SKILL.md exists).
7. **Missing round-52 artefacts at master:** LOG.md round-52 entry, `corpus/lessons/round-52.md` (Mistakes + Gate), SCORECARD round-52 rows, any new SOURCES.md row (171 unchanged, so the §2b sourced-claim leg is unmet unless rows land), round-start census receipt (exit 0 expected; SOURCES.md exists).
8. **Discernment verdict.** Wave-2 seats are lane seats (PROTOCOL: a subagent the lane dispatched is still the lane). `improved` needs an outside spot-check; without a named non-author reviewer the verdict is `unchanged` (or `unprovable-but-better` with a named non-author).
9. **C2 `rows=74` vs `total=72`.** The 2-row gap is not explained anywhere I could find; the report should say what the two extra rows are.
10. **Pre-report gate.** `git ls-remote origin refs/heads/master` must print the final lane hash before the report is written; `untracked=16` must be resolved and named.

What did NOT land (negative results): no finding that R52-C2's frozen predicate is wrong (the counter passes its frozen rules on the archive copy); no evidence the census gate fails (exit 0, 171 rows). I did not verify the W2 attack seats' outputs (not my item).

## 5. Verification gaps
- Did not read the full SKILL.md registry rows or the 28 new rows (not in my item); C2 numbers are the counter's, not a row-by-row audit.
- Did not verify SCORECARD round-52 rows exist beyond the grep (none found for "round 52").
- Did not verify the considerthese proposal choice or the assimilation block (absent).
- Did not verify the 12 hand-read tb2 knowledge entries.

## 6. Tool installs
None.

## 7. Files produced
- /fast/scratch/hyaku/kengaku-r52/w2-W2RevReportDraft/report-requirements.md (checklist; copied to the report dir below before the scratch dir was removed)
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevReportDraft/report-requirements.md (kept copy)
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevReportDraft/report.md (this file)
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevReportDraft.md (findings copy at the path the item names)
- Scratch archive of master (`/fast/scratch/hyaku/kengaku-r52/w2-W2RevReportDraft/tree`) removed before yield.

## 8. Verdict on the attack
Pre-review of the report contract: **landed** for the checklist (every required section, SHONEN, census, pre-report gate, and the C1/C2 measured-vs-claimed gaps are named with paths and numbers). The incidental attack on the C1 instrument: **landed** on the A1 candidate rule (finding 4). The attack against C2 counter arithmetic: **failed to land** (C2 passes on its frozen rules at master).
