# SiblingOverlap — kengaku round 63 w1 (connector seat)

Full deliverable: `.ufo/waves/round-63/w1/connector/overlap.md`
Measurement receipts: `.ufo/waves/round-63/w1/connector/evidence/`

**Verdict: no sibling lane owns (a) offline replay of TB2 graders, (b) a localhost
PEP 503 index replay, (c) a grader-class census, or (d) a grader-class decision
table. No overlap-owned hit; no routing line owed.**

Scan: `grep -rilE 'pypi-server|vectorops|PEP 503|pep-0503|grader-class|class-survey|bwrap|offline replay'`
over each sibling lane's `corpus/ SKILL.md PROVINCE.md plans/` (kengaku excluded),
plus `.ufo/reports/round-6[0-2]/`.
Counts: 79 sibling files / 188 lines; 4 report files / 11 lines.
Term split: `bwrap` 149, `offline replay` 14, claim-specific terms **0**.

Closest siblings, all adjacent only:
- `kama`/`kagi` — `127.0.0.1:8080` is their llama.cpp/Jitsi **model endpoint**
  (`kama-shokunin/corpus/knowledge/consumer-registry.md:90`), not a PEP 503 index.
- `kumitate` — Terminal-Bench named only as a cited benchmark
  (`corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83`); no grader execution.
- `kotoba` — sibling-overlap census is a **lane-scope** census, not a grader-class census
  (`corpus/knowledge/sibling-overlap-census-round74.md:62,93`).
- `revenger`/`tabi` — loopback `http.server` fixtures, plain static serving, no `/simple/` layout.

Read-only note for the L1 (claims untouched): `127.0.0.1:8080` is **not** free
during this wave — the peer seat `PypiProbeBuild` ran a correct `vectorops-0.1.0`
index on it repeatedly (pids 2648510 / 2689887 / 82641 / 110000; `ss -ltnp`).
The draft probe refuses (`SETUP port-8080-occupied`, exit 2) rather than grading
through a foreign listener. Measured alternative: with the index server and the
grader inside one `bwrap --unshare-net` namespace, the host cannot reach that
listener, and the frozen vector holds under a host squatter — K1 P / K2 F
(CalledProcessError) / K3 F (AssertionError) / K4 F (CalledProcessError) = P/F/F/F.
Reported only; no claim, predicate or probe was changed.
