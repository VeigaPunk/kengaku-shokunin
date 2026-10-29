# W2ScoutPriorArtFresh — scoped findings (round 52 wave 2, prior-art pricing)

Seat: W2ScoutPriorArtFresh (scout, leaf). Read-only. Full detail:
`.ufo/waves/round-52/w2/W2ScoutPriorArtFresh/report.md` and
`.ufo/waves/round-52/w2/W2ScoutPriorArtFresh/prior-art.md` (receipts alongside).

**14 public primaries fetched, all HTTP 200 (2026-10-28).** Key ones: TB2 paper
(arXiv:2601.11868, §B.4 adversarial exploit agent, §B.5 ABC self-assessment), Auto Benchmark Audit
(arXiv:2605.26079v1 — automated static+trajectory audit of the same 89-task TB2 population, strict
recall 14/21 vs maintainer PR #53, +9.6% leaderboard lift when flagged tasks are dropped), ABC
checklist (arXiv:2507.02825), BenchGuard (arXiv:2604.24955v2), maintainer PR #53 (base sha = the
lane's pin `2fd12b88`; "Tests were updated when they over-specified or let any solution pass";
26 tasks), TB 2.1 release note (28 tasks), tb issues #67/#1387/#2086, CONTRIBUTING.md,
june.kim frame-blindness probe (40/83 on 2.1).

## Per-finding verdicts (confirmed findings priced at weakness level)

- FINDING bn-fit-modify verdict=phenomenon-new because no fetched primary names this task (0 hits in ABA per-task tables; absent from PR #53's 57 files and the 2.1 note's 28 tasks); only the weakness class is published (TB2 §B.4 existence-only checks; PR #53 "let any solution pass").
- FINDING build-cython-ext verdict=phenomenon-new because no fetched primary names this task (0 ABA hits; absent from PR #53 files and the 2.1 note); class-level documentation only.
- FINDING caffe-cifar-10 verdict=unclear because this task's grader is publicly reviewed twice (ABA: two over-strict Evaluation issues; PR #53 rewrites tests/test_outputs.py) yet the presence-only `test_prototxt_files_exist` survives both unflagged — weakness-level new, task-level known. Weakest of the five.
- FINDING cancel-async-tasks verdict=phenomenon-new because no fetched primary names this task (0 ABA hits; absent from PR #53 files and the 2.1 note); class-level documentation only.
- FINDING code-from-image verdict=phenomenon-new because no fetched primary names this task (0 ABA hits; absent from PR #53 files and the 2.1 note); class-level documentation only.

## Overall instrument-level novelty verdict

Category **phenomenon-known**: whole-benchmark grader triage and published audits of TB2 graders
exist in at least four fetched forms (TB2's own benchmark-wide exploit agent + ABC self-assessment;
ABA's automated audit of the same population; issue #2086's all-tasks verification-audit proposal;
the maintainers' own 26/28-task public revisions). The lane's **specific variant** — static,
per-test-function, marker-vocabulary presence-only classification of grader bytes — is not
documented in any fetched primary, and TB2 §B.5 itself concedes "Test case quality is not assessed
via objective, automated metrics". The score rule's phenomenon-new leg survives only under
instance/weakness-level pricing (4 new, 1 unclear); under class-level pricing it fails. The lane's
prior-art file must cite TB2 §B.4/§B.5, ABA, PR #53 and the 2.1 note at class level and disclose
the dual reading, or the PRIOR-ART leg overstates novelty and is falsifiable by the ABA paper
alone. Cross-check vs wave 1 (C1ScoutPriorArt): same structural verdict, reached independently,
with 4 sources wave 1 lacked and with the five confirmed ids wave 1 could not price.
