# Integrator notes — round 9 (L1 annotations on the L2 fleet artifacts)

The files in this directory are L2 artifacts, committed **verbatim** as
evidence. Where an artifact's claim was superseded or corrected during round-9
integration, the correction is recorded here rather than edited into the
artifact (round-9 closeout requirement from
`corpus/lessons/round-6-aggregator-audit.md` defect 12: "the round-9 closeout
must reconcile (appended note or re-run) or the first committed copy of this
material will carry a self-falsified claim").

## 1. The round-8 `results.jsonl` "two different executions" reading is falsified

Three artifacts record that the repo copy of
`corpus/evidence/round8-horizon/results.jsonl` differed from the run artifact
and infer different things from it:

| Artifact | Claim as written | Status |
|---|---|---|
| `probeB.md:7` and `:130` | "not byte-identical … it is a *different execution* of the same probe"; confidence **high** | **Falsified** |
| `probeA.md:11-12` | "repo copy is raw-stripped … integrity blocker" | Correct |
| `probeC.md:29` | "the repo copy equals the /tmp copy with the `raw` key stripped from all 268 records (verified pairwise, 0 mismatches; graded fields identical)" | Correct — and it is the measurement that settles the question |

Reconciled fact (measured three ways: L1 field-level diff, `probeC.md`,
`harness-mutation.md`): the two files held the **same 268 records in the same
order** with identical `cell`/`pid`/`rep`/`turn` sequences; the key-set delta
was exactly `{raw}` (present on 258 non-meta records in the run artifact,
absent in the repo copy); **0** semantic differences. md5 run `df154cb5…`
(125,577 B) vs repo `01547cfa…` (97,023 B). An md5 mismatch alone does not
license "different execution" — the tie-break is the finer measurement.

Round-9 action: the run artifact was re-landed byte-identical into
`corpus/evidence/round8-horizon/results.jsonl` (md5 `df154cb5…`, `raw` on
258/258 non-meta records) together with `run.log` (md5 `fc3b232f…`), so every
raw-text audit in these artifacts (ack compliance, B-arm byte identity, C
benign failure modes) is reproducible from the repo. The stripped copy was
working-tree-only and was never committed
(`git ls-tree -r f147a27 --name-only | grep -c evidence` → **0**), so no
committed byte-image of it exists; its md5 is recorded in `LOG.md`'s round-8
entry.

## 2. `probeB.md` §5 vs `critic.md` §1 agree; the counts to cite

Both independently reconstructed the corruption generator: 4/8 corruptions
structurally inert (pids 3,6,7,8), 2/8 fabricated `true_mid+5` (pids 1,2),
pid 1's key untouched by ops 8–10 (critic defect #6 **not landed**,
`horizon.py:187` fallback). Well-formed in **2/8** pids (4,5). Cite
`../knowledge/bench-arena-round8-horizon.md` §B for the reconciled numbers.

## 3. C-benign "1/4" is 0/4 under the intended rule

`probeC.md` (strict re-grading) and `harness-mutation.md` (defect D1, `FIX-O`
flips exactly 1 record) converge: `grade_c` computes `over_repair` and omits it
from `ok` (`horizon.py:288`), and derives `preserved` from the model's
self-declared violations (`:277-279`). The shipped SUMMARY's `C-benign: 1/4`
therefore contains one over-repair "pass"; the strict count is **0/4**. Both
the `run.log` SUMMARY and the shipped flags are left unmodified — the
correction lives in `../knowledge/bench-arena-round8-horizon.md` §C.

## 4. `/tmp` pointers inside these artifacts

Several artifacts cite `/tmp/bench-r8/*`, `/tmp/kengaku-r9/*`,
`/tmp/bench-r5/predictions.md`, `/tmp/bench-r6/predictions.md`. Those are
**labelled historical/absence evidence**, not the durable pointers for round-9
claims: the decisive bytes are committed under
`corpus/evidence/round8-horizon/`, `corpus/evidence/round9-replication/` and
this directory, and every headline number is pasted into the corresponding
`corpus/knowledge/` entry. Two `/tmp` claims are legitimately ephemeral because
they assert *absence* or a past state: `test -e /tmp/bench-r8/predictions.md` →
MISSING (round 8 filed no predictions) and the r5/r6 prediction-file line
counts (25 / 17) that make the r8 omission a regression rather than a first.

## 5. Reviewer defect triage (`review.md` §Defect queue)

| # | Defect | Round-9 disposition |
|---|---|---|
| 1 | round-8 evidence debt (untracked, unlogged, unindexed) | **Closed** — committed, `LOG.md` round-8 entry, README `evidence/` section |
| 2 | README "planning-horizon … unmeasured locally" false | **Closed** — gap line replaced with measured state + remaining limits |
| 3 | 2 aggregator-audit lessons with no README row / LOG representation | **Closed** — 2 README rows added; noted in `LOG.md` round-9 correction entry |
| 4 | SHONEN "20+ cited local sources" overreach | **Closed** — `SHONEN.md` regenerated from the canonical seed; the count now lives in the evidence line as 2 decision tables / 13 anti-patterns / 9 checklist steps / 20 source bullets, each with its counting command |
| 5 | all SHONEN `[x]` self-attested | **Closed** — marks are `[~] [~] [ ] [~]`; zero `[x]` (a dispatched subagent is still the lane, so no box can be promoted this round) |
| 6 | SWE-Bench Pro vs the contamination anti-pattern | **Rejected** — `SKILL.md:24` prefers Pro *because* Verified is contaminated, matching `benchmark-shortlist-for-godspeed-research.md:37-38` ("SWE-Bench Pro (Public)" + the OpenAI retirement link) and anti-pattern 1. No conflict exists |
| 7 | "22 files" stale count | Already closed round 7 (0 hits) |
| 8 | no SKILL rule block for the horizon cell names | **Closed** — `SKILL.md` §"Planning-horizon & transcript-shape probes" (cell semantics table + 9 measurement rules) |
