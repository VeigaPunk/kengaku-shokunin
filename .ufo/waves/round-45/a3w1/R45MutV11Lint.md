# R45MutV11Lint — V11 source-lint mutation probe

**Measured tip:** `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C /fast/scratch/hyaku/kengaku-r45/R45MutV11Lint/lane rev-parse HEAD`). Clone root was verified as `/fast/scratch/hyaku/kengaku-r45/R45MutV11Lint/lane`. All predictor mutations were to the cloned entry and were restored byte-exactly; no lane file was edited. Predictor entry pristine SHA-256 before and after each completed run: `1385a811cbc126c5c6c035549fa2c9546db841907ff2fcbc8fca94a456a665f2`.

## Detector and measured states

Detector: frozen `round45_c2_verify.py` V11, via `v11()`; its acceptance output is `ok` with 48 states, zero disagreements, and >=8 pass and fail grader states. Every measurement below ran inside `claims/envelope.sh "$S/env" ...`; all completed envelopes reported unchanged local-bin content digest `ff187bb5c98aa6b5` before/after.

Pristine admitted reader command:

```
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 "$S/run_v11.py" "$S/exact_reader.py"
```

Output:

```
ENVELOPE start 00:34:46 cwd=/home/vgpnk/Projects/shokunin
candidate: exact_reader.py bytes: 127
lint_hits: [] | minus: -
entry sha256 orig: 1385a811cbc126c5c6c035549fa2c9546db841907ff2fcbc8fca94a456a665f2 mutated: 0b1aabf10c628d808426cdaac6943a8631e049c671ce676992655e142a4e0e92
V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
restored sha256: 1385a811cbc126c5c6c035549fa2c9546db841907ff2fcbc8fca94a456a665f2 MATCH
ENVELOPE end 00:34:48 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

The generator's output was separately collected by the bounded envelope command `.../envelope.sh "$S/env" /usr/bin/python3 "$S/dump_states.py"`: `nstates=48`, `npass=18`, `nfail=30`; per-kind pass counts were exact 3/3, with-decoys 3/3, crlf-file 3/3, no-newline 3/3, leading-blank 3/3, duplicated 3/3; all other ten kinds 0/3. There were 12 unique passing texts and 19 unique failing non-None texts. Output ended `ENVELOPE end 00:34:11 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.

## Current-lint table evasions

Both candidates have no `PRED_LINT_TOKENS` hits and remain below 4000 bytes. Each uses only exact-input membership of the 12 measured passing strings; neither reads files nor executes grader code. The second builds a mapping with `dict(zip(...))`, no brace literal. Commands and actual outputs:

```
.../envelope.sh "$S/env" /usr/bin/python3 "$S/run_v11.py" "$S/tuple_table.py"
candidate: tuple_table.py bytes: 879
lint_hits: [] | minus: -
V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
restored sha256: 1385a811cbc126c5c6c035549fa2c9546db841907ff2fcbc8fca94a456a665f2 MATCH
ENVELOPE end 00:34:58 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

```
.../envelope.sh "$S/env" /usr/bin/python3 "$S/run_v11.py" "$S/dict_zip_table.py"
candidate: dict_zip_table.py bytes: 913
lint_hits: [] | minus: -
V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
restored sha256: 1385a811cbc126c5c6c035549fa2c9546db841907ff2fcbc8fca94a456a665f2 MATCH
ENVELOPE end 00:35:04 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Thus **2 distinct table encodings tested, both pass lint and the complete V11 behavior detector**. This is a realized memorized-answer table, not only a syntactic/static-lint finding. It is consistent with the explicit counter-header limitation that a small open-coded truth table may fit, but falsifies any stronger interpretation that V11's current lint excludes verdict tables. `dict(zip(...))` does not need parentheses beyond ordinary call parentheses; it avoids braces and passes unchanged lint.

A lint-clean but incorrect substring predictor was a useful detector control: command `.../envelope.sh "$S/env" /usr/bin/python3 "$S/run_v11.py" "$S/bad_table.py"` output `lint_hits: []`, then `V11 DEFECT states=48 grader_pass=18 grader_fail=30 disagree=12`, restored entry hash matched, and envelope ended `exit=0 ... unchanged`. The behavioral detector therefore kills a bad implementation, not the correct memorized table.

## One-token-at-a-time removal matrix

I removed each of the 22 token strings singly from an in-memory copy of the frozen tuple, then tested a minimal source probe containing that token; output came from `.../envelope.sh "$S/env" /usr/bin/python3 "$S/token_matrix.py"`, ending `exit=0 ... unchanged`. 20 removals individually admitted their corresponding minimal probe: `import`, `open`, `os.`, `sys.`, `subprocess`, `socket`, `pathlib`, `hash`, `sha256`, `md5`, `eval(`, `exec(`, `compile(`, `states`, `.json`, `__`, `getattr`, `globals`, `locals`, `print(`. The returned `newly_admitted` was true for each. The `{` and `}` probes were `{1: 2}`; removing either one alone did **not** admit it, since the other delimiter remained prohibited. (A complete removal of both would admit that literal.) This matrix establishes exact-token coverage but does not claim that each admitted minimal expression alone is a working predictor; the demonstrated complete predictor-class escape is the table encoding above.

Other records: an initial invocation with a nonexistent candidate exited 1 before modifying anything; initial parallel candidate trials collided on the shared clone and failed with `FileExistsError`, so those outputs are discarded. The subsequent isolated serial runs above are the evidence. A mistyped envelope path invocation exited 127 before running any detector; not evidence.

## Restoration and verdict

Restoration was recorded after each completed candidate: `restored sha256 ... MATCH`. Final clone entry hash is `1385a811cbc126c5c6c035549fa2c9546db841907ff2fcbc8fca94a456a665f2`; candidate SHA-256s: tuple table `a32c17e2967d4ddd678cf95b944ffb8393d8407699ef363ffacaea75e72cf1f5`, dict/zip table `79add744497709b9f2c6488e4498ab42557475c3ca42fa92402802d9252accd6`. Scratch was removed with `plans/scratch_guard.py safe-rm` after writing this report.

VERDICT: v11-lint-evasions-2-passing-2
