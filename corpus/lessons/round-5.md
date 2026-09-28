# Lessons — round 5

Citations: LOG.md round-5 entry; run artifacts `/tmp/bench-r5/` (ephemeral);
permanent record in `corpus/knowledge/bench-arena-round5-battery.md`;
digest record in `corpus/knowledge/eval-design-digest-2.md`.

1. **Aggregate-correct predictions can hide wrong models.** Predicted 20/33
   and observed 20/33 — a perfect score — while 8/33 tasks flipped status
   and my flip prediction (1) missed by 8×. Calibration at the aggregate
   level was luck; the per-task model (near-identity to v2) was wrong at a
   24% rate. Record *per-task confidence*, not just status predictions, or
   an exact aggregate hit will certify a wrong generative model of the
   system.
2. **Truncation is a distinct failure class from wrongness.** Task 06 hit
   `finish_reason=length` at the 4096-token cap mid-regex-expansion, which
   the grader reports as HARNESS_DEFECT (no closed fence). But the harness
   was fine — the model's generation strategy was unbounded. Reading rule:
   `fence_found=0` + `finish=length` = model limitation; `fence_found=0` +
   `finish=stop` = actual format/harness defect. Check finish_reason before
   filing as harness.
3. **Fail direction inverts per pipeline again — with a new axis.** v2: FAIL
   faster on inference latency. Round-4 slice: FAIL slower on wall. Round-5:
   FAIL slower on *both* wall (1.71 s vs 0.84 s median) and completion
   tokens (260 vs 128). On direct-API, FAILs are expensive because wrong
   solutions are long. The signature is real but pipeline-owned; quote it
   with its pipeline tag.
4. **Byte-identical outputs mark scaffold-insensitive tasks.** Five tasks
   (16, 25, 28, 32, 33) emitted identical sol_sha256 to v2 despite the
   opencode→bare-API pipeline change. All tiny deterministic tasks. If a
   task is sha-stable across pipelines, scaffold comparison claims cannot
   use it — flip-capable tasks (03, 09, 13, 20, 31, 08, 12) are the
   sensitive probe set.
5. **Stable-FAIL is evidence, not noise.** 33-metaclass-shadowing is
   byte-identical FAIL across pipelines — a deterministic wrong answer, i.e.
   a capability gap with zero sampling variance. Distinguish from boundary
   tasks (which flip) before deciding what to re-probe.
6. **Second digest pass closes by grep+sweep discipline.** The "remaining
   karpathy branches" gap covered 25 files (count corrected round 7 — was
   written as 22); scanning all for eval keywords
   then deep-reading ~8 yielded the corpus-usable rules (sampling-proves-
   presence, worst-case reference-class, autonomy slider, planning-not-
   execution bottleneck, spec-ability tiers). Full sequential reading would
   have taken ~3× longer for the same rule yield — the sweep command is
   itself part of the evidence trail per CORPUS.md's negative-claim rule.

## Errata (appended round 9)

- **`:8` "8/33 tasks flipped status" — terminology, not count.** The round-5
  battery entry (`corpus/knowledge/bench-arena-round5-battery.md:17,36`) settles
  on **8 status deltas** because one of the eight (task 06) is
  FAIL→HARNESS_DEFECT via `finish=length`, not a PASS↔FAIL flip. Count 8 stands;
  "flipped" is the superseded word. Swept round 9 in `corpus/README.md:22`,
  `SKILL.md:204,409`; recorded in `LOG.md`'s round-9 correction entry per the
  round-6 aggregator audit (`corpus/lessons/round-6-aggregator-audit.md`
  defect 6).
