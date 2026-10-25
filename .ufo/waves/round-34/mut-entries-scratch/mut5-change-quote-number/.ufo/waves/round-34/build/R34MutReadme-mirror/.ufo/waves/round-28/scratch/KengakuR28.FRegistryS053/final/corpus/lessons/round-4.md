# Lessons — round 4

Citations: LOG.md round-4 entry; run artifacts `/tmp/bench-r4/` (ephemeral);
permanent record in `corpus/knowledge/bench-arena-fresh-run.md`.

1. **Endpoint drift is a silent-kill class.** `qwen-local` provider config
   pointed at `localhost:8080` after the server moved to `34113`; `8080`
   was still listening (Jitsi), so failure surfaced only as a 404 on
   `/v1/models` — and prior runs had already degraded to `journal`-source
   telemetry without anyone noticing. Rule: probe `/v1/models` and
   `/health` on the configured port *before* trusting any provider entry;
   a listening-but-wrong service is worse than a closed port.
2. **n=1 per task flips on sampling.** Task `03-extract-isodatetimes`
   passed on the Aug-29 opencode pipeline and failed on the Sep-28
   direct-API pipeline (temp 0.2, no system prompt, fresh generation —
   sol_sha differs). Lesson: status claims on a task need repeat counts
   or a pinned seed; treat any single-run flip near the boundary as
   noise until replicated.
3. **FAIL-latency is a population statistic, not a per-task law.** Round
   3 reported FAIL median < PASS median on 33 rows. This slice inverted
   it locally: fastest task was a PASS (1.2 s), slowest a FAIL
   (14.7 s, driven by a 2,151-token generation). Read the signature at
   aggregate level only.
4. **Grader transport-agnosticism enables surgical reruns.**
   `grade.sh` consumes `out/<label>/*.txt` regardless of producer —
   the model interface can be swapped (direct API vs opencode) without
   touching task/test assets. Keep runner and grader separate.
5. **Ex-ante prediction caught a real miss.** Recorded 2/4 aggregate
   before the run; observed 1/4. The per-task predictions were 3/4 right
   but the aggregate was wrong — aggregate and per-task calibration are
   separate quantities; record both.
