# R45CritV11Bypass — attack V11 (held-out predictor) in `plans/round45_c2_verify.py`

Scope: write predictors that pass `disagree=0` without performing the line-membership reading; run each
through the FROZEN counter's own `v11()` on scratch mirrors (harness shape from
`.ufo/waves/round-45/claims/c2_predictor_control.py`). Measured on a `--shared` clone of the lane.

## Base measured

- Lane tip measured: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (= `master` per dispatch; clone rule clone
  of `/home/vgpnk/Projects/shokunin/kengaku-shokunin`).
- Counter exercised: `$S/lane/plans/round45_c2_verify.py`, sha256 `ab6825e34596ba71f59a184a59fd4e672fd22dcf4b892c511cae5ead2b104f50`
  (content digest printed by my driver; the frozen COMMIT is `52d7486a8caf930855cd1f748032ac21648303f5` — untouched).
- Command: `envelope.sh "$S/env" python3 "$S/v11_probe.py" "$S/lane" "$S" "$S/rcpt"` (full receipt:
  `.ufo/waves/round-45/a3w1/R45CritV11Bypass/run1.txt`, sha256-comparable, 4457 bytes).
- ENVELOPE (VALID): `ENVELOPE start 00:30:54 …` / `ENVELOPE end 00:30:56 exit=0
  local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.

## Ground truth obtained first

I ran the counter's own `GRADE_PY` inside its own `sandboxed()` bwrap (same argv shape as `v11`) on a
scratch workdir: the 48 seeded states grade to bitstring
`111100000000011011110000000001101111000000000110` (bit k = state k), `grader_pass=18 grader_fail=30`
— non-vacuity (≥8/≥8) holds on the real seed. An independent semantic model of the pinned grader
(`read_text()` universal-newline translation → `.strip().split("\n")` → membership of the
`"([0-9A-Z]{23})"` constant; `test_outputs.py:14-18`) reproduced all 48 verdicts exactly
(`semantic_model_mismatches []`), so `disagree=0` results below are genuine table/heuristic hits, not
a corrupted grader. Note `Path.read_text()`'s universal-newline mode is why `crlf-file` grades PASS
(the `predict` input keeps raw `\r\n`; a model that skips the `\r\n→\n` translation disagrees).

## Verdict-changing bypasses (lint clean → `ok`, `disagree=0`, no membership reading)

Receipts are `.ufo/waves/round-45/a3w1/R45CritV11Bypass/p*.py`; all four printed
`V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0`.

1. `p1-callidx-table` (87 bytes): `def predict(text, n=[-1]): n[0]+=1; return (105619152396303 >> n[0]) & 1 == 1`
   — the argument `text` is never read. A mutable default arg counts calls; `PREDICT_PY` calls
   `ns["predict"](t)` sequentially over `states` in the same order the grader visited them. The R44
   repair removed the `at=` label leak (counter line 561, count-only note) but the **call-ORDER leak
   is structural and remains**: position is the whole key a table needs.
2. `p2-keyed-table` (127 bytes): `(9243193507842 >> ((len(t) + 19*sum(ord(c) for c in t)) % 48)) & 1`.
   No dict/set literal, no file, no `hash(` — an injective-enough affine key over the seeded 48
   (searched `(a,b,M)`, first hit `M=48,a=1,b=19`; labels consistent, `None`→key of `''`). Directly
   falsifies the lint's premise (counter line 415): "a verdict TABLE needs a dict/set literal, a file
   read, or a hash" — a 13-digit int literal + shift + one affine feature suffices.
3. `p3-textidx-table` (1981 bytes): verbatim tuple of all 48 state strings (1908 bytes) +
   `(TABLE >> tuple.index(text))`. Even the *verbatim* table the lint was built to stop fits: `{`/`}`
   are banned but `(` `)` are not, and 4000 bytes covers the states. Order- and feature-free.
4. `p4-boundary-substr` (163 bytes): `'\n'+ANS+'\n' in '\n'+u+'\n'` after `\r\n→\n`. Not a table and
   not line membership (no `.strip().split('\n')`, no whole-line equality) — yet agrees on all 48
   seeded states. V11 verifies sample-equivalence, not the reading; a wrong-but-close semantics is
   indistinguishable on this seed.

## What the hardening actually stops (measured)

- Replay-from-bound-file class: **dead by lint + mount shape.** `p6-read-grader`
  (`open('/run.py').read()`) → `lint=open → DEFECT`; `p7-import-states` (`import json`) → `lint=import
  → DEFECT`. Every file-read route is refused at source level: `open`, `import`, `__` (blocks
  `__class__`/`__subclasses__`/`__builtins__` climbs), `getattr`, `eval(`, `exec(`, `compile(`.
  Independently, `v11`'s predict sandbox ro-binds only `/predictor.py` (extra args at line 553); the
  grader's `test_outputs.py` is never mounted there, and `/states.json` is unreadable without
  `open`/`import`. Replaying the grader's logic *from a bound file* is impossible; re-deriving the
  answer constant likewise (predictor cannot read the capture — the constant must be typed in, which
  is what every admitted predictor legitimately does anyway).
- Structural smuggling: `p11` (two ```python blocks) → `DEFECT … (found 2)`; `p12` (a `## Predictor`
  line inside the block, amputating `PRED_SECTION`) → `blocks_found 0 → DEFECT`. The section/block
  regex pair cannot hide code.
- Timing/purity: **no channel found, statically.** Grade and predict run in separate bwrap sandboxes
  with fresh `--tmpfs /tmp`, no shared writable bind, `stdin=DEVNULL`, predict runs strictly after;
  `bool()` coercion in `PREDICT_PY` kills truthy-object games; `dir()`/`vars()` inside `predict`
  expose only the predictor's own locals (`states` is bound in the `exec` globals, not reachable
  without banned introspection — and the token `states` is linted anyway). The only observable the
  harness leaks is call order — exploited by p1.
- Sample discrimination is real for *near* heuristics: `p9` (`ANS in u`, raw substring) →
  `disagree=12 DEFECT` (joined/password-eq/bom states); `p10` (`ANS in u.split()`) → `disagree=3
  DEFECT` (the three `padded-lines` states). The seeded table does reject close-but-wrong readings.
- `p5-chr-membership` (answer built by `chr()` joins, identical membership semantics) → `ok
  disagree=0`. Counted as a legit pass, NOT a bypass: `chr()` can only obfuscate literals, never a
  banned *call*, and the answer string is not a banned token.

## Axis verdict

`VERDICT: v11-bypasses-4-verdict-changing-4`. Four predictors pass `disagree=0` with zero membership
reading (three truth tables: call-order-indexed, feature-keyed, verbatim-tuple-indexed; one
boundary-substring heuristic). This is the header's own disclosed residual — lines 25-28: "A
memorizer that embeds the grader's OWN observed 48 verdicts as a 48-bit list still fits the lint —
that is the named limit" — so the C2 `checks=11 defects=0` claim stands on the real entry; what is
new is that (a) the lint's stated premise is false on all three legs (no dict/set, file, or hash is
needed), (b) the order leak survives the count-only repair, and (c) even non-table wrong semantics
(p4) passes. Smallest safe corrections for the L1 if V11 must distinguish reader from memorizer:
seed `random.Random` per run from `os.urandom` (kills all three static tables), and/or lint cap on
integer literal width; p4-class heuristics can only be bounded by the sample, not eliminated —
non-author review of the admitted block stays load-bearing either way.

VERDICT: v11-bypasses-4-verdict-changing-4
