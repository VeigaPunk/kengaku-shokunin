# Lessons — round 7

Source: LOG.md round-7 entry; run artifacts `/tmp/bench-r7/`;
knowledge `bench-arena-round7-scaffold-ablation.md`.

- **"Scaffold-determined" over-claimed at n=3.** Round 6's unanimous-reps
  test classified 5/8 flips as scaffold-determined; component ablation
  showed only **1/5** (13-stack-min) survives as genuinely
  scaffold-caused. Unanimity proves the flip isn't temperature noise —
  it does NOT prove the scaffold caused it; v2's single draw could itself
  have been noise. To attribute, ablate the components (E2/E3/E4 cells),
  don't just re-run the endpoints.
- **Tools-without-system-prompt is a trap condition.** At `tool_choice:
  auto`, removing the system prompt turned 14/15 outputs into
  `finish=tool_calls` with empty or unfenced content — graded
  HARNESS_DEFECT, and temperature-invariant (9/9 at temp 0.2 on labrat
  repro). A "minimal" API probe that forwards `tools` but strips
  `system` measures nothing about the model.
- **Context mass moves strategy; temperature is a *second*, bare-only
  lever.** +4.7K tokens of opencode scaffold (skills/env/powered-by,
  ZERO stack-relevant tokens per grep audit — pure context-mass regime
  shift) reliably switched 13-stack-min to the canonical monotone-stack
  at BOTH temps (10/10 code sols); bare-API needed temp 0.8 to escape
  the sorted-stack attractor (1/3 at 0.8 vs 0/5 byte-identical
  `d268ef61` FAILs at 0.2). Don't claim "decoding irrelevant" until the
  {no-system × high-temp} cell exists — the critic caught exactly that
  missing cell; E5 added it.
- **Draws at temp 0.2 are non-iid on this server** (n=25 probe): lag-1
  autocorr +0.26/+0.32, burst-state coupling (`--cont-batching
  --parallel 2`), unseeded output stream is a coarse structured sequence
  (09 alternated two shas period-2). Same-prompt replays are NOT
  independent samples — separate reps in time or interleave tasks to
  decorrelate; report block-robust intervals.
- **`enable_thinking` was a no-op on this host.** The
  `qwen-coder-godspeed.jinja` template has no think branch; r5/r6 claims
  of "thinking off" described the template, not the flag. Check the
  template before crediting a request parameter.
- **Temporary-provider capture is the cheap way to read agent wire
  format.** Adding a proxy provider to `opencode.json` + one run captured
  the exact request (system text, tools, sampling) in ~6 s; the session
  DB stores messages but not the wire body. Restore config immediately
  after; never leave a re-pointed provider.
- **`tools:{name:false}` in agent config doesn't remove all tools** —
  `janitor_auth` and `skill` still shipped in the request. Verify the
  wire payload, not the config intent.
