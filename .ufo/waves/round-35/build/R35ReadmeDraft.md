# R35ReadmeDraft — corpus/README.md additions for C1 (draft for L1)

Seat: R35ReadmeDraft (scribe, kengaku round 35 wave 1). Lane: `kengaku-shokunin`. All paths relative
to `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. This is a draft only — no lane file was edited.

## Working state observed

- Lane HEAD = `11d6453` ("round-35: freeze claims, counters, probe, ledger, controls") = the freeze commit
  named in `plans/round-35-claims.md`. `corpus/README.md` at HEAD has **394 lines** and contains **none**
  of the round-35 insertions (verified: `git show HEAD:corpus/README.md`, numbered).
- The working tree currently carries the same 10 inserted lines as uncommitted modifications
  (`git diff -- corpus/README.md`: 10 insertions, 0 deletions). So the target insertions already exist in
  the working tree at lines 68, 257, 282 and 400–404; those are engaged as the canonical draft text below,
  re-anchored against the HEAD file so L1 can apply them to a fresh checkout (or diff against the working
  tree). No claim below goes beyond the probe receipt, the captures, the knowledge entry, and the frozen
  claim.

## Evidence bound to the draft (what each sentence rests on)

- Probe receipt `corpus/evidence/round35/tb2-grader-probe.txt` (21 lines): header line 1 pins
  `grader=corpus/evidence/round35/tb2-eval/test_outputs.py`, sha256 `44a05a24…`, pin `2fd12b88`, Biopython
  `1.85`; line 2 `components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000`; lines 3–20 record each
  case's predicted/observed/match plus first failing assertion; line 21 `cases=18 observed_pass=5
  observed_fail=13 mismatches=0`.
- Captures `corpus/evidence/round35/tb2-eval/` (re-fetched 2026-10-25): 6 pinned `protein-assembly` files —
  `test_outputs.py`, `test.sh`, `instruction.md`, `task.toml`, `antibody.fasta`, `pdb_ids.txt` — with
  `SHA256SUMS` (test_outputs.py `44a05a24…`, test.sh `9ede4664…`, instruction.md `1bb2af1d…`).
  `test_outputs.py` `test_gblock`: single-line file (`:19`), `[atcg]+` (`:22`), ≤3000 nt (`:23`), order
  flag<donor<dhfr<acceptor<snap (`:42-44`), FLAG at 0 (`:46`), `[GS]+` linkers 5–20 (`:54-59`), SNAP ends
  (`:60-62`), GC 15–35 per 50-nt window (`:65-72`). `test.sh`: binary reward 1/0 (`:27`, `:29`),
  biopython==1.85 (`:21`). `instruction.md` bullets: no empty lines (`:11`), linkers 5–20 (`:29`), GC
  30–70% per 50-nt window (`:30`), order antibody binder - donor - dhfr - acceptor - molecule binder
  (`:33`).
- Knowledge entry `corpus/knowledge/tb2-protein-assembly-grader.md`: negative space (`:82-88`), "other 88
  TB2 tasks" (`:86`), probe runs on host Python not task image (`:87-88`), findings (G-only linker passes;
  cap never decides an otherwise-passing gBlock; one-residue error fails with order message) (`:68-78`).
- Frozen claim `plans/round-35-claims.md`: C1 surface (`:13-37`), entry/probe/receipt names (`:23-25`),
  round-33 frontier clause left open for "Terminal-Bench 2.0's" scoring code (`:15-17`), §Frontier step
  (`:67-70`).
- `corpus/defects.jsonl`: five round-34 rows D1–D5, all `"status": "open"` at freeze (ledger re-run at
  every tip per `plans/defect_ledger.py`).

## Draft insertions (anchor = HEAD line in corpus/README.md@11d6453)

### Insertion 1 — knowledge-table index row (after HEAD line 67, the `` `knowledge/benchmark-grader-semantics.md` `` row)

```
| `knowledge/tb2-protein-assembly-grader.md` | One Terminal-Bench 2.0 task grader read and executed: `protein-assembly`'s `test_gblock` scores a binary reward from literal expected subproteins, order, FLAG/SNAP boundaries, `[GS]+` linkers of 5–20 residues and 50-nt GC windows, never reading its reference inputs; an 18-case offline probe maps instruction bullets to the assertion that enforces them (`cases=18 observed_pass=5 observed_fail=13 mismatches=0`) | S105, S106, S107 (terminal-bench-2 @ 2fd12b88) |
```

### Insertion 2 — coverage-map bullet (after HEAD line 255, the `- **Benchmark grader semantics**:` bullet)

```
- **Terminal-Bench 2.0 task grader (one task)**: covered at source-code depth and executed offline (round 35, 2026-10-25) — knowledge/tb2-protein-assembly-grader.md; S105, S106, S107; probe `plans/tb2_grader_probe.py`, receipt `evidence/round35/tb2-grader-probe.txt`. Discharges the round-33 frontier clause "Terminal-Bench 2.0's" scoring code for `protein-assembly` only: what `test_gblock` asserts, how `test.sh` maps it to a binary reward, and which `instruction.md` bullets each assertion enforces (a G-only linker passes; the 3000-nt cap never decides an otherwise-passing gBlock; a one-residue subprotein error fails with the order message). Not the other 88 TB2 tasks, not the correctness of the grader's literals against PDB/FPbase, not runtime execution inside the task image, not runtime task validity (PROVINCE refuses it).
```

### Insertion 3 — §Frontier sub-bullet (after HEAD line 279, the `*Partly discharged round 33 …*` sub-bullet)

```
  - *Partly discharged round 35 (2026-10-25):* `knowledge/tb2-protein-assembly-grader.md` reads and executes one Terminal-Bench 2.0 task's scoring code (`protein-assembly/tests/test_outputs.py` + `tests/test.sh` @ `2fd12b88`) against its `instruction.md`. The "Terminal-Bench 2.0's" clause is discharged **for that one task only**; it stays open for the other TB2 tasks, for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

### Insertion 4 — `### Round-35 evidence` subsection (append at EOF, after HEAD line 394, the last `### Round-34 evidence` table row)

```
### Round-35 evidence

- `evidence/round35/tb2-eval/` — the six pinned `protein-assembly` files (re-fetched 2026-10-25, byte-identical to the round-34 captures) with `SHA256SUMS`.
- `evidence/round35/tb2-grader-probe.txt` — receipt of `plans/tb2_grader_probe.py` (18 frozen cases; re-run and byte-compared by `plans/round35_c1_verify.py` V5).
- `defects.jsonl` + `plans/defect_ledger.py` — the persistent routed-defect ledger (round-34 D1–D5), re-run at every tip.
```

## Sentence-to-evidence binding

- "scores a binary reward … never reading its reference inputs" ← `test_outputs.py:10-73,28-41` (literal
  subproteins), `test.sh:26-30` (reward 1/0), entry `:9-14`.
- "18-case offline probe maps instruction bullets to the assertion that enforces them" ← receipt lines
  3–20 (`assertion=`/`requirement=` pairs), summary line 21.
- "a G-only linker passes" ← receipt line 13 (`linker-g-only` predicted=pass observed=pass), entry `:70-71`.
- "the 3000-nt cap never decides an otherwise-passing gBlock" ← receipt line 2 (`max_passing_nt=2766`),
  entry `:72-75`.
- "a one-residue subprotein error fails with the order message" ← receipt line 17 (`donor-one-substitution`,
  assertion='Fusion protein must be in the order …'), entry `:76-78`.
- "Not the other 88 TB2 tasks" ← entry `:86` (89-task set at the pinned commit minus `protein-assembly`).
- "not the correctness of the grader's literals against PDB/FPbase" ← entry `:82-84`.
- "not runtime execution inside the task image" ← entry `:87-88`.
- "not runtime task validity (PROVINCE refuses it)" ← claim `:15-17` frontier wording; mirrors prior round-31/33 bullets.
- Evidence subsection lines ← capture listing + `SHA256SUMS`, receipt line 21, and `corpus/defects.jsonl`
  (rows D1–D5, all open at freeze).
- "byte-identical to the round-34 captures" ← claim `:20` (captures re-fetched 2026-10-25).

## Limits

- The "88" count is carried from the round-31 S100 entry's census (89 `tests/test.sh` files at the pinned
  commit), not from this round's captures; it appears in the draft only inside the entry-grounded negative
  clause.
- No model performance, no trajectory, no Harbor runtime execution, no task validity is claimed anywhere in
  the draft.

VERDICT: readme-draft-4-insertions
