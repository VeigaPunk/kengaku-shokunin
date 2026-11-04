# DefectGateReverify — R70-C2 hand re-derivation (wave w1, round 70)

Reviewer seat. Re-derived all eight checks from bytes by hand; the gate was run only as
corroboration, never as source of truth. Lane tip `384e9c76` (freeze commit); `git status`
dirty: `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/tb2-nginx-request-logging-offline.md`,
`plans/round-70-claims.md`, `plans/round70_c2_routed_defects.py` (the A1 amendment pair), plus
untracked `.ufo/waves/round-70/w1*` and `corpus/evidence/round70/` — the corrections are
working-tree bytes awaiting the L1 close commit, as designed (red-before at the freeze tip is the
committed control `.ufo/waves/round-70/c2-red-before.txt`, verbatim `DEFECTS n=8` / `PREDICATE
R70-C2 fail`).

## Per-check facts and verdicts

**E1 depth-gate-identity (D1) — AGREE, ok.**
- fact: `sha256sum` by hand: wave copy `.ufo/waves/round-69/w1/gates/depth-gate.txt` =
  `f683297c35998f66187475daf2f68333f62294fab9356d436cba459c02efc9d9`; corpus copy
  `corpus/evidence/round69/gates/depth-gate.txt` =
  `d65bbbdad6bf722961e27d8800a4ea92a75e5fafd06113a96781ca2d84a96e22`. Both equal the `SHA` records in
  `corpus/evidence/round70/c2/depth-gate-provenance.txt` (lines 3–4).
- fact: provenance line 1 `TREE-CAPTURE .ufo/waves/round-69/w1/gates/depth-gate.txt PRE-CLASS-ROW`;
  line 2 `LANDING-COPY corpus/evidence/round69/gates/depth-gate.txt`. Both labels the gate requires.
- fact: my own line diff of the two files = exactly 1 line:
  `-ROWS n=16 class_match=True count_mismatch=0 paths total=33 resolved=33 share=1.00`
  `+ROWS n=16 class_match=True count_mismatch=0 paths total=34 resolved=34 share=1.00`; replacing
  `total=34→33, resolved=34→33` in the corpus line reproduces the wave line byte-for-byte
  (`norm_y_equals_x True`, python check). The changed-line delta is count-only (33→34), consistent
  with the frozen "paths total 33 → 34"; the 34th path's identity is recorded in the provenance
  `ADDED-TOKEN corpus/knowledge/tb2-nginx-request-logging-offline.md` line.
- fact: provenance carries exactly one `LINE-DIFF` line and its value equals
  `<wave line> -> <corpus line>` exactly (`recorded==want(wave->corpus) True`) — wave→corpus order,
  matching the A1-repaired gate.
- A1 audit: working-tree diff of `plans/round70_c2_routed_defects.py` vs the freeze commit is exactly
  the swap `diff = [(i, y, x) …]` + a comment; with the frozen order the check would emit
  `change-wider-than-counts` (norm normalizes the already-33 wave line, ≠ corpus line) and
  `recorded-pair` (corpus→wave ≠ recorded wave→corpus) — precisely the tokens A1 records. Predicate,
  recorded pair and frozen sentence unchanged. Legitimate mechanical repair, applied pre-dispatch
  (`.ufo/waves/round-70/w1.ready.dispatched` present).

**E2 trio-receipt (D2) — AGREE, ok.**
- fact: fresh `python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-nginx-request-logging-offline.md`
  from the lane root → rc 0; `cmp` fresh vs `corpus/evidence/round70/gates/trio-nginx.txt`: byte
  identical, 64 = 64 bytes. Receipt content: `TRIO pass corpus/knowledge/tb2-nginx-request-logging-offline.md`.

**E3 instruction-row (D3) — AGREE, ok.**
- fact: entry `corpus/knowledge/tb2-nginx-request-logging-offline.md` line 1 starts `source:` and
  contains `instruction.md:6-11,15-18 (S242)` (anchor and cite present in the same line).
- fact: `corpus/SOURCES.md` line 257 row S242 — cell 3 = instruction URL at pin `2fd12b88`;
  cell 7 carries full `sha256 26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99` with
  `instruction.md:6-11,15-18 fetched 2026-11-03 HTTP 200, 24 lines, 1882 bytes`; cell 12 (used-by) =
  `corpus/knowledge/tb2-nginx-request-logging-offline.md`. All four gate arms satisfied on the real
  12-cell row.

**E4 s241-correction (D4) — AGREE, ok.**
- fact: `corpus/SOURCES.md` line 258 row S243 — cell 8 verbatim:
  `supersedes S241 — leg 5 is the nginx -t subprocess, satisfied by a shim; legs 6-8 read config bytes
  and a log the server writes, so S241's legs 5-6 file-read summary is wrong`; cell 7 verbatim:
  `result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)`; cell 12 (used-by) = the
  entry path. All `supersedes S241` / `leg 5` / `nginx -t` / used-by arms satisfied.

**E5 corpus-index (D5) — AGREE, ok.**
- fact: `corpus/README.md` line 564 = the `lessons/round-69.md` table row; line 786 =
  `## Round-69 supporting artifacts (2026-11-03)` block (lines 788–793 list knowledge, lesson,
  registry, evidence, counters, wave). Both gate needles present on real rows/block.

**E6 r69-landing-receipt (D6) — AGREE, ok, and independently strengthened.**
- fact: `corpus/evidence/round70/gates/r69-c2-landing.txt` records `REV 4038bb11`,
  `FULL 4038bb1150345e11f4c52c8a39ca16cecb9e975a` (= `git rev-parse 4038bb11`, measured),
  `DEFECTS n=0`, `PREDICATE R69-C2 pass`, `RC 0`.
- fact (beyond the gate): I cloned the lane into scratch
  (`git clone --shared L $S/r69clone; git -C $S/r69clone checkout --detach 4038bb11`; toplevel assert
  ok; HEAD = `4038bb1150345e11f4c52c8a39ca16cecb9e975a`) and re-ran
  `python3 plans/round69_c2_routed_defects.py`: rc 0, output
  `E1 ok rows=4/4 … E7 ok problems=[] / DEFECTS n=0 / PREDICATE R69-C2 pass` — byte-identical to the
  receipt's OUTPUT block. The receipt is a true record, not prose.

**E7 gate-reject (D7) — DISAGREE WITH GREEN: check correctly RED right now.**
- fact: `corpus/lessons/round-70.md` does not exist (glob of `corpus/lessons/`: no round-70 file).
  Gate live run: `E7 defect gate-reject problems=['corpus/lessons/round-70.md:missing']` →
  `DEFECTS n=1`, `PREDICATE R70-C2 fail`, rc 1.
- fact: the registry half IS closed — `corpus/SOURCES.md` line 259 row S244 has cell 9 `rejected`
  (so the row contains `| rejected |`), `merge/kengaku` twice in cell 3, and a stated reason in
  cell 8: `REJECTED: its tier-A own-work claim rests on a probe transcript whose bytes are not in
  this lane, so Q1/Q2 cannot be satisfied; flip: the probe artefact lands in this lane and re-runs`.
- Verdict: honest mid-wave state. E7 closes only when the lesson (Lesson70Draft → L1) lands with a
  `## Gate` line containing both "reject" and "reason". Until then the predicate is correctly red;
  the gate refuses to pass on the row alone — which is the right behavior, and itself proves the
  failure mode is reachable.

**E8 wave-validation (D8) — AGREE, ok.**
- fact: `.ufo/waves/round-70/w1-validate.rc` = `0\n` (2 bytes, `od` verified); `w1-validate.out` =
  35,426 bytes (the v1 dispatch JSON, nonempty); `w1-validate.stderr` exists, 0 bytes. The spotcheck
  D8 text itself grounds "validated cleanly (rc 0)" on the empty stderr.

## Reachability / vacuity (assignment step 4)

- **No unreachable check.** My scratch run: `--selftest --work $S/st` → fake lane (corrections
  stripped by construction from real files) `SELFTEST defects-in-fake=8 want=8 all-fail=True`,
  `SELFTEST e2-byte-flip-red=True`, rc 0; `--mutants --work $S/mu` → `MUTANTS total=8 killed=8`
  (each removal leaves exactly 7 defects, rc 0). Every check demonstrably fails when its correction
  is absent; the exception wrapper (crash = defect) bars vacuous crash-passes.
- **Prose-only success (named):** E6's gate arm is string-presence in a receipt the same round wrote
  — self-attestation; only an external re-run (which I did, byte-identical) removes the risk. E8's
  rc file is equally self-attested (a committed `0` cannot be re-derived from bytes; the 35 KB
  stdout capture mitigates). E7's lesson arm is prose by design (taste cannot be re-derived); its
  byte-grounded half is the S244 row.
- **Partial-armor soft spots (all reachable, none fired here):** E3/E4 skip the used-by arm when a
  row has ≤12 cells (`len(c) > 11` guard); E5's "row" arm is any-occurrence substring, not a
  row-shape check (actual state is a true table row, line 564); E1's added-token arm checks the
  token anywhere in the provenance (it lives in the ADDED-TOKEN line, not the changed line — the
  changed line's delta is count-only, as the frozen sentence's "paths total 33 → 34" acknowledges);
  E8 never requires stderr to be empty, only that it exists.

## Verdict

R70-C2 re-derivation: **E1, E2, E3, E4, E5, E6, E8 verified closed by hand — agree with the gate's
`ok` on each; E7 is open (`corpus/lessons/round-70.md` missing, S244 row landed) and the gate's
current `DEFECTS n=1 / fail / rc 1` matches my hand derivation exactly.** No check is unreachable;
no verdict disagreement; the A1 amendment is a predicate-preserving mechanical repair whose claimed
red tokens I reproduced from the code. Landing requires: the round-70 lesson with a Gate reject
line naming a reason, then the L1 commit of the working-tree corrections (the freeze tip itself
still scores n=8 by design, per the committed red-before control).

## Commands run (all rc recorded)

- `git -C L rev-parse master` → `384e9c76…`; `git status --porcelain` (9 entries as listed above).
- `sha256sum` both depth-gate files + provenance + trio + landing receipts (values above).
- `diff -u` wave vs corpus depth-gate → 1 hunk, 1 line, rc 1 (expected).
- `python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-nginx-request-logging-offline.md`
  → rc 0; `cmp` vs receipt → identical.
- `git rev-parse 4038bb11` → `4038bb1150345e11f4c52c8a39ca16cecb9e975a`.
- `git clone --shared L $S/r69clone && git -C $S/r69clone checkout --detach 4038bb11`
  (toplevel assert ok) + `python3 plans/round69_c2_routed_defects.py` → rc 0, byte-identical output.
- `python3 plans/round70_c2_routed_defects.py` (corroboration only) → rc 1, `DEFECTS n=1` (E7).
- `python3 plans/round70_c2_routed_defects.py --selftest --work $S/st` → rc 0;
  `--mutants --work $S/mu` → rc 0, killed=8/8. Scratch
  `/fast/scratch/hyaku/kengaku-r70/DefectGateReverify` (to be trap-cleaned; receipts quoted here).
- `git diff plans/round70_c2_routed_defects.py plans/round-70-claims.md` (A1 audit, quoted above).
- Tooling: none installed — stock `python3`/`git` only; no tool/channel changes to record.
- Bounds: no mutating git/jj outside the scratch fixture (clone+detach checkout inside $S with
  toplevel assert); no edits to any frozen file, MANIFEST, scripts/, templates/, .ufo/state/,
  watchdog.log, or fleet-root tracked files; no subagents (leaf reviewer); no `agent://all`.
