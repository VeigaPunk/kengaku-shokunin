source: S245 (corpus/SOURCES.md) — Terminal-Bench 2.0 task `hf-model-inference`, instruction at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/instruction.md — anchor: `instruction.md:3` — sha256 `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1`; S246 (the grader) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/tests/test_outputs.py — anchor: `tests/test_outputs.py:103-107` — sha256 `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`; S247 (the sandbox manual) — https://man.archlinux.org/man/bwrap.1.en — anchor: the `--clearenv` entry — sha256 `708f56eed930f9a0b524fd79b8d9db92c4c35eb246646c4b0fab0812d7e68de7`; S248 (the checkpoint the task names) — https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english/raw/main/README.md — anchor: `README.md:145` — sha256 `75f17282923fea5b541df92640e2d8646c4ff5e8e3e16ed0a7e4e50ee7588851`
verified-at: 2026-11-03 (S247 and S248 fetched live this round: HTTP 200, 27981 and 10512 bytes, sha256 as above, captures at `corpus/evidence/round72/sources/`; S245/S246 re-derived from the committed captures `corpus/evidence/round71/hf/instruction.md` and `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`)
recheck: `python3 plans/round72_c1_hf_probe.py --lane . --work <scratch> --port-lock <port-5000.lock> --receipt <path> --evidence-dir <path>` must reproduce the nine frozen vectors of `plans/round-72-claims.md`; `python3 plans/round72_c1_hf_probe.py --lane . --check-receipt <path> --work <scratch>/check` prints `DEFECTS n=0` / `PREDICATE R72-C1 pass`; `python3 plans/round72_c2_routed_defects.py --lane .` prints `E1a ok … E2 ok`, `DEFECTS n=0` / `PREDICATE R72-C2 pass`.

writer: KengakuR72 (with the round-72 wave's reviews)
admission: hold — the QUALITY Q13/Q14 second-seat re-read is not yet on record from a `w2`/`falsify` registry; see `corpus/lessons/round-72.md` `## Gate` (Admission status).

# Making a grader replay's model-load witness a *provenance* check, not an outcome check (R72-C1)

Round 71 replayed the Terminal-Bench 2.0 `hf-model-inference` grader offline and admitted its
eight-case table at **leg** granularity. Its critic found the replay's weakest joint: the
bubblewrap sandbox inherited the caller's environment, so a `transformers` stub on `PYTHONPATH`
was imported in place of the real library and reproduced the whole table — the `LIBRARIES` line
was measured on the host, never inside the sandbox. A check that a stubbed library passes is an
*outcome* check: it says the harness produced the right pytest verdicts, not that the right
library was loaded.

This entry records the round-72 repair, because the pattern generalises to every
`network-service` replay in this lane that needs a real library inside a sandbox.

## The mechanism: `--clearenv` plus an explicit allowlist

`bwrap(1)` states, at the `--clearenv` entry (S247):

> Unset all environment variables, except for PWD and any that are subsequently set by --setenv

So what the caller exports cannot reach an import: the probe's `--setenv` list is nine variables —
`PATH`, `HOME`, `LANG`, `PYTHONPATH=/venv/lib/python3.13/site-packages`, `PYTHONNOUSERSITE`,
`PYTHONWARNINGS`, `TMPDIR`, `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE` — and the observed environment
is those nine **plus** two born inside: `PWD` (bwrap's own exception) and `TORCHINDUCTOR_CACHE_DIR`,
which torch creates on the first `from_pretrained`. Eleven keys, not nine: `allowlist_seen=9/9` is a
superset test, and the inheritance witness is `canary_seen=0`, not the count.

**Two witnesses, both on the receipt.** A provenance clause that can be satisfied by a claim is
worthlessness; the receipt carries evidence computed inside the sandbox:

| line | clause | what backs it |
|---|---|---|
| `PROVENANCE … env_cleared=True` | the probe's own assertion — the emitter prints the literal, and `--check-receipt` only matches it | a declaration a reader checks against `bwrap_argv` (`--clearenv` present, nine `--setenv`); it is not evidence on its own |
| `PROVENANCE … canary_seen=0` | `R72_CANARY` is exported for every case and the harness records whether it sees it | a single leaked case turns the count above 0 |
| `PROVENANCE … distinct=1 transformers_file=/venv/…` | the harness's own `transformers.__file__` | one path, and it must lie under the read-only venv bind — a stub on any writable path cannot satisfy it |
| `PROVENANCE … allowlist_seen=9/9` | every declared variable was actually present | catches a silently dropped `--setenv` |

## The negative control that makes it a check

`--stub-control` writes a `transformers` package whose `__init__` raises, puts it on the *parent*
`PYTHONPATH`, and runs the same nine cases. Expected: `STUB-CONTROL exposed=False
vectors_unchanged=True`. The same injection against the round-71 probe changes the table, which is
what makes the pair a before → after rather than a claim. Rule for a successor probe: **a sandbox
witness must ship the injection that used to defeat it, and that injection must fail.**

## The ninth case, and what one assert site is worth

`test_api_error_handling` has two asserts: status 400 (`tests/test_outputs.py:103`) and
`assert "error" in error_data` (`:107`). Round 71's `no-400` case redded at `:103`, so `:107` was
unreachable and eight cases could not distinguish a 400-with-`error` from a 400-without one. K9
`400-no-error-field` answers 400 with `{"detail": …}` and derives `PPPF` — the first negative
witness for `:107`.

The general rule: **when a leg has two asserts in series, one failing case per assert, or the
second assert is decoration.** A leg-level coverage count (`seen_p=4 seen_f=4`) does not detect
this; the assert-site count does. Round 71 named 6 of 19 assert sites priced; K9 makes it 7.

## Why the staged model is still a fixture

The task names `distilbert-base-uncased-finetuned-sst-2-english` and the card (S248) loads it with
`DistilBertForSequenceClassification.from_pretrained(...)` — so the leg's condition is *class +
files*, not weights. The probe stages a five-file 13,944-byte fixture that the same class loads. The
replay therefore prices the grader's logic and the sandbox's provenance; it says nothing about
distilbert's accuracy. Recording that boundary is what keeps the class-row move honest.

## Reuse checklist for the next `network-service` replay

1. `--clearenv` on, allowlist explicit, `PYTHONPATH` pointing at the read-only bind.
2. A plantable canary exported by the caller; `canary_seen=0` must be on the receipt.
3. The library's `__file__` recorded inside the sandbox; assert a single path under the bind.
4. The stub-injection control that used to defeat the probe, run and required to fail.
5. One case per assert site, not one per leg; count assert sites as well as legs.
6. A do-nothing control (no model, no service) that must derive all-`F`.
