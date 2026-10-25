# R30Considerthese — proposal 1 of `considerthese/2026-10-24.md`, grounded and drafted as Q20

Role: leaf scout (kengaku round 30, hyaku run 6). Question asked: which single still-unimplemented
proposal in `considerthese/2026-10-24.md` can be grounded in the lane's own bytes this round, and
what QUALITY.md criterion would encode it. **Findings and one draft criterion block — nothing
landed, no production file touched.** Scratch lives in `/tmp/r30-considerthese/`.

Measured at lane HEAD `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db` (`round-29 verifier spot-check
(integrator, hyaku): non-author admit/reject`), working tree carrying round-30's uncommitted wave
files. Frozen claims read first: `plans/round-30-claims.md`.

## 1. Verdict — proposal 1 (gates on every push) is unimplemented, and it is the only one of the
three that is a mechanism rather than a corpus delta

`considerthese/2026-10-24.md:19-26` asks for "one Actions workflow that runs `python3 grader.py`,
the `--selftest` suites and the latest census on every push to `master`, uploads stdout as an
artifact, and pins the runner image", motivated by the claim that "The tree has zero files under
`.github/`" and that receipts are "author-observed, never non-author closure (`LOG.md` ~L372)".

Both premises hold, byte for byte, today:

| Command | Output | Exit |
|---|---|---|
| `ls -la .github` | `ls: cannot access '.github': No such file or directory` | 2 |
| `git log --all --oneline -- .github` | *(empty — no branch ever carried the path)* | 0 |
| `git ls-files '.github'` | *(empty)* | 0 |
| `grep -rn 'GitHub Actions\|\.github/workflows' --include='*.md' --include='*.py' --include='*.sh' .` | only prose hits in `corpus/evidence/`, `corpus/knowledge/eval-design-digest-2.md:103`, `SKILL.md:38-39`, `LOG.md:546`, plus the proposal itself at `considerthese/2026-10-24.md:21` — no workflow file, no runner script | 0 |
| `ls -1 *.sh Makefile; find . -maxdepth 2 -name 'run_*' -o -name '*gates*'` | *(no aggregate gate runner exists)* | 0 |

Proposals 2 (per-entry `as_of`/`source_status`/`revalidate_by` front-matter) and 3 (30–40 frozen
demand-side questions) both require a corpus payload that this round's claim slots are already
committed to (`contamination-transparency-card.md`, `round30_defects.py`, `sources_adopt.py`
selftest — `plans/round-30-claims.md` C1/C2/C3). Proposal 1 needs no corpus payload: its whole
input set is already committed and every component already runs offline in ≤2 s. It is therefore
the groundable one, and it grounds *as a criterion* in the Q19 precedent (Q19 landed as a QUALITY
row and only later acquired `.ufo/waves/yield.tsv`).

## 2. The lane's own wording, quoted from the bytes it sits in

`LOG.md:370-372`, read verbatim (lines 370-372 are one bullet):

> - `python3 plans/state_check.py --summary` v3 on frozen `f11bffbf` reports278 assertions,5 mismatches;
>   repaired tree reports278 assertions,0 mismatches,5 superseded,3 offline-unverifiable. P2's full
>   keyed assertion projection is unchanged; paired S048-source addition leaves P3b records unchanged.
> - Two-direction separability is UNCHANGED (C1 FAMILY/TOTAL records and C2 summary/exit);
>   `grader.py` retains733 checks,0 mismatches; Q13 selftest is green and r25 admission red reproduces.
>   Prospective scratch-commit Q13 passes with three returned qualifying readers before actual admission;
>   actual-commit measurement follows. Receipts are author-observed, never non-author closure.

The operative sentence is `LOG.md:372`: **"Receipts are author-observed, never non-author
closure."** The lane has already ruled R6 (`corpus/QUALITY.md`, round-closure criteria): a verifier
counts as non-author only when its id is outside the round's dispatch roster, and
`grep -rn '<id>' .ufo/prompts/` returns nothing. A pasted local gate receipt cannot be made
non-author by re-running it; only an out-of-band executor (proposal 1's workflow) can. That is the
gap Q20 must be honest about.

## 3. Gates that run today with one command, no network, on the archived landing tree

Extraction itself is one command and is what makes the run *landing bytes, not working copy*:

```
git archive 363a4eb | tar -x -C /tmp/r30-considerthese/tree     # exit 0
```

Every roster row below was executed **inside that extracted tree**, never in the lane working tree.
Network import audit — `grep -cE "^import (socket|urllib|http)|^from (urllib|http|socket)|requests\." <tool>`:

| File | hits |
|---|---|
| `grader.py`, `plans/{sources_adopt,registry_check,state_check,adoption_check,config_projection,parser_policy_compare,grader_perturb,attrib_calibration,gate_timing_check}.py` | 0 |
| `plans/benchmark_spec_audit.py` | 1 — `import urllib.parse` (`:13`), URL *parsing* only, no opener |

Roster, with the exact count line each tool prints (all exit 0, all offline):

| # | Command (run in the extracted tree) | Verbatim terminal line(s) | Exit | Wall |
|---|---|---|---|---|
| G1 | `python3 grader.py` | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline` | 0 | 0 s |
| G2 | `python3 grader.py --selftest` | `[selftest] ALL PASS` (7 `[selftest] PASS S1…S7` lines above it) | 0 | 2 s |
| G3 | `python3 plans/sources_adopt.py --selftest` | `SELFTEST cases=10 failed=0` | 0 | 0 s |
| G4 | `python3 plans/registry_check.py --selftest` | `SELFTEST clean cases=15 valid_literal_fence,queued_and_missing,…` | 0 | 1 s |
| G5 | `python3 plans/config_projection.py --selftest` | `SELFTEST clean cases=31 six_tokens_and_non_url_field,…` | 0 | 1 s |
| G6 | `python3 plans/benchmark_spec_audit.py --selftest` | `SELFTEST clean cases=67 hand_expected_scorer_contract,…` | 0 | <1 s |
| G7 | `python3 plans/parser_policy_compare.py --selftest` | `SELFTEST total policies=9 cases=59 mutants=10 killed=10 failures=0` | 0 | <1 s |
| G8 | `python3 plans/grader_perturb.py --selftest` | `SELFTEST MUTATION-CATCH PASS caught=12` / `SELFTEST TOTAL families=10 branch_cases=10 failed=0` | 0 | 0 s |
| G9 | `python3 plans/attrib_calibration.py --selftest` | `selftest: 18 checks, 0 failed` | 0 | <1 s |
| G10 | `python3 plans/state_check.py --selftest` | `[selftest] ALL PASS (canonical seed, pointers, out-of-population box, …)` — **no count token** | 0 | 0 s |
| G11 | `python3 plans/gate_timing_check.py --selftest` | `[selftest] ALL PASS (five allowed roles; …)` — **no count token** | 0 | <1 s |
| G12 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` | `selftest ok` (preceded by `killed  E04-rejected-pair-exemption-exit-0`, …) | 0 | 1 s |
| G13 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-25` | 4× `file  W04  S069/S071/S075/S076 duplicate url …` then `file  ok  /tmp/r30-considerthese/tree/corpus/SOURCES.md` | 0 | 1 s |
| G14 | `python3 plans/round28_census.py --revision 363a4eb` | JSON counters (`tier A 76 / B 4 / C 2`, …) | 0 | 1 s |
| G15 | `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json` | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped` — **the pre-landing control for C1, red as designed** | 1 | <1 s |

Two facts fall straight out of the table and matter for the criterion:

- **G12/G13 are not lane bytes.** Both live in the fleet repo
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`:1-16` documents
  `census|validate|overdue|shared|selftest`, "Read-only: … writes only stdout or --out"). A
  lane-internal criterion can invoke them (C1 already does, through `adoption_check.py --census`,
  which shells out to that exact path), but must not pretend they are in-lane.
- **G10/G11 print no count token**, so they cannot be pinned by a count line the way G3–G9 can.
  A criterion that says "the count line must match the roster" silently exempts them.
- **`plans/adoption_check.py` has no `--selftest` at all** (`grep -n add_argument
  plans/adoption_check.py` → `--lane`, `--expect`, `--census`), i.e. the round-29 standing adoption
  gate is itself outside the self-verifying roster. It can only be checked by running it against a
  known-red expect file (G15 is exactly that receipt).

## 4. Draft criterion — Q20, in QUALITY.md's own format

Intended placement: a new section after
`## Round29 attempt-2 criterion — wave yield is recorded` (`corpus/QUALITY.md:186-194`), so that
Q19's row stays byte-identical (QUALITY's own rule: "Criteria are superseded by a new row that
names the row it replaces — never edited in place"). **Not written to `corpus/QUALITY.md`.**

```markdown
## Round30 criterion — a gate-touching landing carries an out-of-band gate run

- **Q20 — a landing that touches a gate carries a gate run taken from the landing bytes.** Any commit
  that changes `grader.py`, any `plans/*.py` or `plans/*.sh`, the `corpus/SOURCES.md` registry schema
  the gates parse, or the workflow files under `.github/` once they exist, must be accompanied in the
  same round by a receipt produced from a tree extracted at the landing sha
  (`git archive <sha> | tar -x -C <dir>`, never the author's working copy) that prints, in full, the
  exit code and the count line of every roster gate: `python3 grader.py` →
  `CHECKS n=733 mismatches=0 errata_pinned=1` and `VERDICT: PASS — stored evidence fully re-derives
  offline`, exit 0; `python3 grader.py --selftest` → `[selftest] ALL PASS` with seven
  `[selftest] PASS` lines, exit 0; `python3 plans/sources_adopt.py --selftest` →
  `SELFTEST cases=10 failed=0`; `python3 plans/registry_check.py --selftest` →
  `SELFTEST clean cases=15 …`; `python3 plans/config_projection.py --selftest` →
  `SELFTEST clean cases=31 …`; `python3 plans/benchmark_spec_audit.py --selftest` →
  `SELFTEST clean cases=67 …`; `python3 plans/parser_policy_compare.py --selftest` →
  `SELFTEST total policies=9 cases=59 mutants=10 killed=10 failures=0`;
  `python3 plans/grader_perturb.py --selftest` → `caught=12 families=10 branch_cases=10 failed=0`;
  `python3 plans/attrib_calibration.py --selftest` → `selftest: 18 checks, 0 failed`;
  `python3 plans/state_check.py --selftest` and `python3 plans/gate_timing_check.py --selftest` →
  `[selftest] ALL PASS` (both print no count token, so only their exit code is pinned).
  A count line that differs from this roster is a Q20 failure unless the same commit's diff changes
  that count and the receipt states the old value, the new value and the reason. The receipt is
  still author-observed: Q20 standardizes the run and its reproducibility, it does not make the run
  non-author (R6 stands; only an out-of-band executor does that).
  Check: on the extracted landing tree, exit 0 from
  `python3 grader.py | grep -qx 'CHECKS n=733 mismatches=0 errata_pinned=1'
   && python3 grader.py --selftest | grep -qx '\[selftest\] ALL PASS'
   && python3 plans/sources_adopt.py --selftest | grep -qx 'SELFTEST cases=10 failed=0'
   && python3 plans/registry_check.py --selftest | grep -q '^SELFTEST clean cases=15 '`
  plus the touched tool's own row when the change is not one of those four; and exit 1 on a tree
  where a single executed check has been deleted (recorded probe:
  `.ufo/waves/round-30/build/R30Considerthese.md` §5, copies `copyA`–`copyC`).
  Lesson: `LOG.md:372` ("Receipts are author-observed, never non-author closure");
  `considerthese/2026-10-24.md:19-26` (proposal 1, unimplemented at `363a4eb`: `ls .github` exits 2,
  `git log --all -- .github` is empty); `corpus/lessons/round-29.md` M89, and Q19's precedent that a
  criterion may land ahead of its implementation.
```

The compound check line above is not hypothetical. Run verbatim from a script in the extracted
`363a4eb` tree (plus the fleet census row appended) it prints `Q20 GATE RUN: PASS`, exit 0; run
identically against a tree with one executed check deleted it exits 1 without printing PASS. The
lane-internal subset (the four `grep -qx` components, no fleet path) also exits 0 on `363a4eb`
and 1 on the deleted-check tree — that is the form the criterion should cite while `.github/` does
not exist, because it needs nothing outside the repo.

## 5. What Q20 cannot do — three reproduced probes, not assertions

All three run in `/tmp/r30-considerthese/`, each on a fresh `cp -a` of the `363a4eb` extraction.

**P1 — exit 0 does not detect deleted selftest cases.**
Delete grader's S6 and S7 cases (663 bytes, from `# S6: analytic stats anchors` up to the `finally:`
that removes the temp dir), then run `python3 grader.py --selftest`:

```
[selftest] PASS S5 r11 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r11.summary.A-CKPT4710 (id fired: True)
[selftest] ALL PASS
EXIT=0
PASS_LINES=6
```

Seven cases became six, and the tool still says `ALL PASS` and exits 0. **A criterion written as
"the selftest exits 0" is defeated by deleting the case.** This is why Q20 pins `ALL PASS` **with
seven `PASS` lines** and the numeric tokens on G3–G9 rather than trusting the exit code.

**P2 — the pinned count does detect a deleted check.**
Delete the single executable line `rep.eq("r11.census.requests", (g4710 + g710) + (a4710 + a710) +
fillers + 1, 22 * n + 1)` from the real replay body and run `python3 grader.py`:

```
CHECKS n=732 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
EXIT=0
```

Exit 0, PASS verdict, `n=732`. Only the integer differs. The pinned `n=733` is the detector; the
verdict line is not. The compound run fails (exit 1) on this tree — proved.

**P3 — the pinned count does not detect a *weakened* check, and this is Q20's hard limit.**
Replace the same assertion's right-hand side with a copy of its left-hand side (a tautology), keeping
the `rep.eq(...)` call so the counter is untouched:

```
weakened one assertion to a tautology, call count preserved
CHECKS n=733 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
EXIT=0
=== compound gate on copyC ===
Q20 GATE RUN: PASS
EXIT=0
```

The whole compound check passes green on a gate whose r11 request-count assertion no longer compares
anything. Therefore:

1. **Q20 buys shrinkage detection, not correctness.** It proves a gate still runs, still counts what
   it counted, and still re-derives the stored evidence; it cannot prove an assertion still states
   the right relation. A landing that edits a gate and keeps every counter satisfies Q20, so **the
   gate diff must still be read by a reviewer** — Q20 makes that read cheaper (the counters localize
   the change), it never replaces it.
2. **It does not make the receipt non-author.** Nothing in Q20 changes R6: an author-run local gate
   is still author-observed (`LOG.md:372`). The only mechanism that changes that is proposal 1's
   workflow, which remains unlanded. A round that wants non-author closure still needs a verifier id
   outside the dispatch roster.
3. **It cannot judge a claim**, exactly as the proposal concedes ("It is the cheapest mechanical
   non-author verifier available: it can't judge a claim"). G1 proves stored evidence re-derives; it
   says nothing about whether the stored evidence should have been produced at all.
4. **It cannot cover `plans/adoption_check.py`.** That gate has no `--selftest`; Q20's roster cannot
   self-verify it, and only a red-expect run (G15: `entries=0 …`, exit 1) demonstrates it is
   failure-capable. A future Q20 revision should require `adoption_check.py --selftest`, but that
   tool does not exist today, so Q20 as drafted cannot demand it.
5. **Two roster rows are unpinnable and one is out-of-lane.** G10/G11 print no count token, so their
   coverage is exit-code-only and P1's deletion attack applies to them unmodified; G12/G13 depend on
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside the lane and outside any
   `.github` workflow that would check out only this repo.

## 6. Remaining unknowns (stated, not papered over)

- **Whether anything already pins `n=733` in the lane's gate path outside LOG prose.** `LOG.md:371`
  states "retains733 checks,0 mismatches" as a round-29 receipt, but no checked-in expectation file
  carries the integer; I did not find one in `plans/fixtures/` and did not exhaustively read that
  tree. If a fixture already holds it, Q20's roster is a transcription, not a new pin.
- **Whether `.github/` workflows are admissible under the fleet's lane contract.** `SOURCES`-level
  rules do not govern it, but `/home/vgpnk/Projects/shokunin/shokunin.conf` and the fleet's own
  `.github` conventions were not read here (out of my read scope), so a workflow that "pins the
  runner image" has an unverified upstream standard to conform to.
- **G2's seven-case count is a local measurement** at `363a4eb`; the specific count `7` is quoted
  from the observed `[selftest] PASS S1…S7` lines in this run and would move with any future case.

## 7. Tooling record

No installs, no upgrades, no package-manager transactions. `pacman` transactions are paused
host-wide and nothing needed one; `/usr/bin/time` is absent on this host, so walls were measured
with shell `$SECONDS` instead (noted because the first roster attempt failed on it: `error: command
not found: /usr/bin/time`).
