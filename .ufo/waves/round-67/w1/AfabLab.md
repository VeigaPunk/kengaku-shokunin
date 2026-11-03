# AfabLab — round 67 w1 (labrat seat)

Scope: one bounded empirical probe of the grader's AFAB check at world size 1. No frozen file was
edited, no claim predicate or vector table was changed, no tool was installed, no network was used.
Evidence: `.ufo/waves/round-67/w1/AfabLab/labrat.md` and the receipts beside it.

## What was run

Four ws1-only grader runs, each `flock <port-12355 lock> bwrap …` with the argv copied from
`plans/round67_c1_pipeline_probe.py::run_case` (only the `/app` and `/ctl` binds swapped, `-k
'test_pipeline_parallel and 1'` added, `--junitxml=/ctl/junit.xml`), frozen grader
sha256 `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f`:

| run | rc | junit `test_pipeline_parallel[1]` | where it stopped |
|---|---|---|---|
| 1F1B variant of `q1-ref` (loop order only) | 0 | P | — |
| committed `q1-ref` (reference control) | 0 | P | — |
| detector-positive control (`lm_head` first entered after backward) | 1 | F | `test_outputs.py:156` `AFAB violation: found forward after backward at lm_head.fwd` |
| literal split-decoder construction (partial backward first) | 1 | F | `test_outputs.py:163` `Rank 0 mismatch at model.layers.1.bwd, microbatch 0, max diff=0.0087443` |

Plus a no-process-group mechanism run (`hookorder.py`, rc 0) that re-registers the grader's hook
code verbatim and prints key insertion order, counts and the AFAB predicate applied to that order.

## Findings

- **F1 — H-AFAB confirmed at ws1.** A one-forward-one-backward microbatch loop passes the ws1 leg
  (rc 0, P) with values inside the grader's 1e-5 tolerance, so the `ws1` column of the frozen R67-C1
  table cannot separate 1F1B from AFAB. `ws1 P` means "correct numerics and no late first entry",
  not "the schedule is AFAB". Confirmed for the frozen grader and one model configuration only.
- **F2 — the mechanism is key insertion order, measured.** `hookorder.txt`: the AFAB reference and
  the 1F1B loop produce the *same* 15-key dictionary order and the same per-key counts (all 4), and
  neither triggers the predicate. The dict records when a name is first created; interleaving within
  a rank does not change it while every hooked module is first entered in microbatch 0's forward.
- **F3 — the check is not dead code, but its reach is narrow.** The positive control fires the raise
  at `:156`; it needs a module first entered after a backward, which at ws1 requires substituting a
  forward call (functional head vs module call). The seat item's literal construction (split decoder,
  microbatch 0 backwarded on the first chunk before the last layers run forward) creates the
  fwd-after-bwd key but never reaches the raise: the per-key value comparison at `:163` fails first on
  `model.layers.1.bwd`. A truncated backward therefore cannot be used to falsify the detector from
  outside; any positive control must preserve the reference numerics for every earlier key.
- **F4 — cost.** Each ws1 grader run is ~7.4 s wall under the port lock (suite time), so detector
  controls of this kind are cheap enough to attach to any round that leans on this grader.

## Relation to the round's claims

- R67-C1: named limitation (i) in `plans/round-67-claims.md` said the AFAB check "cannot separate a
  1F1B schedule at world size 1" as a *hypothesis for a labrat seat*. It is now measured on the frozen
  grader (F1/F2). The claim's predicate, counter, kill rules and six-case vector table are untouched
  and nothing here is a miss: the frozen table stays as written.
- R67-C2: not touched; no sqlite probe, receipt or fixture was read for content beyond the claims text,
  and no file under `corpus/evidence/round65/` was modified.

## Risks / blockers (observed, not remediated — parent's call)

- `git -C L status --porcelain -- corpus/evidence/round67` reports
  `?? corpus/evidence/round67/pipe/receipt.txt` and `?? corpus/evidence/round67/pipe/receipt.junit/`
  while the six case files under `corpus/evidence/round67/pipe/cases/` are tracked
  (`git ls-files`). The receipt of record therefore is **not in git** at wave time (mtime
  2026-11-03 18:54:45, before this seat started). If the round report's "committed receipt of record"
  wording is to be literally true, that pair must be added by whoever owns the commit; this seat does
  not run `git add`.
- `plans/` frozen files and `corpus/evidence/round65/**` are clean in `git status` from this seat's
  view (`frozen-path-status.txt`); only the two `round67/pipe` entries above appear.
- ws2 was not run (seat item: do not generalise beyond ws1); the non-last-rank branch of the 1F1B
  file is untested, and `case-ctl`/`case-ctl2` raise `NotImplementedError` at world size >1.

## Files written

- `.ufo/waves/round-67/w1/AfabLab/labrat.md` (commands, exit codes, junit outcomes, verdict)
- `.ufo/waves/round-67/w1/AfabLab/case-1f1b-pipeline_parallel.py` (`573d5cc3…ce1c5`)
- `.ufo/waves/round-67/w1/AfabLab/case-ctl-pipeline_parallel.py` (`4fdfb458…3b4957`)
- `.ufo/waves/round-67/w1/AfabLab/case-ctl2-pipeline_parallel.py` (`4ff7dc2f…40d0bb73`)
- `.ufo/waves/round-67/w1/AfabLab/run_ws1.py` (`3142c2bb…761ec0a`), `hookorder.py` (`d71ccd77…b5ad423`)
- `.ufo/waves/round-67/w1/AfabLab/{1f1b,ref,ctl,ctl2}-junit.xml` and `…-log.txt`,
  `hookorder.txt`, `kfilter-check.txt`, `frozen-path-status.txt`
- scratch `/fast/scratch/hyaku/kengaku-r67/AfabLab` deleted after the copies.
