# F35RevReadme — corpus/README.md falsification review (round 35, wave 2)

Seat: F35RevReadme (reviewer, leaf). Lane tip reviewed: `dfee6fff631ebc5f623ba4506e5c7992a215401c`.
Scope: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff 58a19f37 dfee6fff631ebc5f623ba4506e5c7992a215401c -- corpus/README.md`
→ `corpus/README.md | 10 ++++++++++ | 1 file changed, 10 insertions(+), 0 deletions(-)`, four hunks:
index row (L68), coverage bullet (L257), frontier sub-bullet (L282), `### Round-35 evidence` section (L400–404). All 10 added lines accounted for.

Axes: (1) path existence, (2) sentence fidelity vs `corpus/knowledge/tb2-protein-assembly-grader.md` + receipt `corpus/evidence/round35/tb2-grader-probe.txt`, (3) scope honesty — nothing claims more than one task, (4) internal consistency (counts, versions, byte-identity).

## Verified agreements (each with command + output)

1. **Every path named in the diff exists.**
   `ls` confirmed: `corpus/knowledge/tb2-protein-assembly-grader.md` (10584 B), `plans/tb2_grader_probe.py` (9573 B), `plans/round35_c1_verify.py`, `corpus/evidence/round35/tb2-grader-probe.txt` (3399 B), `corpus/evidence/round35/tb2-eval/` containing exactly the six pinned files (`antibody.fasta`, `instruction.md`, `pdb_ids.txt`, `task.toml`, `test.sh`, `test_outputs.py`) plus `SHA256SUMS`, `corpus/defects.jsonl`, `plans/defect_ledger.py`, and `PROVINCE.md` at the lane root (22198 B; the README's "`PROVINCE.md` refuses to this lane" reference resolves).
2. **Byte-identity chain holds.** Per-file sha256 of round-34 captures (`.ufo/waves/round-34/assimilation/captures/tb2-eval/`, committed at tip) vs `corpus/evidence/round35/tb2-eval/`: 6× `SAME` (e.g. `test_outputs.py 44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582`). Independent live re-fetch today of the three pinned raw URLs at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` reproduced exactly the `SHA256SUMS` digests (`44a05a24…`, `9ede4664…`, `1bb2af1d…`). So "re-fetched 2026-10-25, byte-identical to the round-34 captures" is corroborated in its checkable content.
3. **Receipt numbers quoted verbatim and correctly.** Receipt last line: `cases=18 observed_pass=5 observed_fail=13 mismatches=0` — the index row quotes it byte-identically; the receipt holds 18 `case=` lines (5 pass: `valid-balanced`, `uppercase`, `no-trailing-newline`, `linker-20aa`, `linker-g-only`). "18 frozen cases" is supported: the probe (with its predictions) was committed in the freeze `11d6453` (`git show --stat 11d6453`: `plans/tb2_grader_probe.py | 168 +++`), the receipt landed later in `4fe72a9`.
4. **The three findings sentences match the receipt.** `case=linker-g-only predicted=pass observed=pass` → "a G-only linker passes"; `components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000` + knowledge finding 2 → "the 3000-nt cap never decides an otherwise-passing gBlock"; `case=donor-one-substitution … assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap'` → "a one-residue subprotein error fails with the order message".
5. **Index/coverage mechanics match the counter.** `plans/round35_c1_verify.py` V4 checks exactly an index row citing S105/S106/S107 + a coverage-map bullet + `knowledge files == index rows == 42`; measured: `knowledge files: 42`, `index rows: 42`, entry path occurs 3× (L68, L257, L282). V5 re-runs `plans/tb2_grader_probe.py --lane .` and defects on `run.stdout != rec.read_text()` — the evidence bullet's "re-run and byte-compared by `plans/round35_c1_verify.py` V5" is accurate to the code.
6. **SOURCES rows exist as cited.** `corpus/SOURCES.md:120-122` hold S105 (`tests/test_outputs.py`), S106 (`tests/test.sh`), S107 (`instruction.md`), all tier A, URL = pinned raw URL at `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.
7. **Frontier clause quote is verbatim.** The round-33 sub-bullet (README:281) contains `(Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one)`; the new sub-bullet sits under the same parent ("Agentic benchmark task-spec audits") in the 29→31→33→35 chain, and its open/clause wording mirrors round-33's.
8. **"the other 88 TB2 tasks" is arithmetically exact.** GitHub tree API at the pin: `truncated: False`, 89 top-level dirs, `protein-assembly` among them → 88 others.
9. **Ledger bullet is true at this tip.** `corpus/defects.jsonl` holds 5 rows `R34-D1…R34-D5`, all `closed_round: 35`; `python3 plans/defect_ledger.py --lane .` printed `rows=5 closed=5 observed_pass=5 mismatches=0` / `PREDICATE C2 pass`, exit=0. "Re-run at every tip" matches the frozen claims doc ("re-runs at every tip").
10. **One-task scope holds everywhere.** Every task-count phrase in the diff scopes to one: "One Terminal-Bench 2.0 task grader" (L68), "(one task)" / "for `protein-assembly` only" / "Not the other 88 TB2 tasks" (L257), "one Terminal-Bench 2.0 task's scoring code" / "for that one task only" / "stays open for the other TB2 tasks" (L282), "the six pinned `protein-assembly` files" (L402). No sentence claims a second task; the five "Not …" negatives in L257 all match the entry's §Negative space.

## Findings

### F1 (LOW) — frontier sub-bullet claims execution of `test.sh`, which was only read
README:282: "`knowledge/tb2-protein-assembly-grader.md` reads and executes one Terminal-Bench 2.0 task's scoring code (`protein-assembly/tests/test_outputs.py` + `tests/test.sh` @ `2fd12b88`) against its `instruction.md`."

The parenthetical puts both files inside the object of "reads and executes", but only `test_gblock` from `test_outputs.py` was ever executed: `plans/tb2_grader_probe.py` `run_grader()` imports the captured module and calls `mod.test_gblock()`; `test.sh` is never invoked (executing it requires pytest inside the task image). The knowledge entry is explicit — "Offline execution of the captured grader *function* … not a run of Terminal-Bench, of the task image" and "not inside the task image" — and its own title compression ("read and executed") is disambiguated by its body, which the README sub-bullet has no room for. Within the README itself the index row (L68, "`test_gblock` scores…") and the coverage bullet (L257, "how `test.sh` maps it to a binary reward" — mapping, not execution) are precise; L282 is the outlier.

Suggested minimal fix: "…reads and executes the captured grader function from `protein-assembly/tests/test_outputs.py`, and reads `tests/test.sh` (@ `2fd12b88`) against its `instruction.md`."

Severity LOW: no task-count, reward, or coverage error — execution-attribution precision only.

## Non-defect observations (nits)

- **N1 — the two SHA256SUMS manifests differ only in line order.** `diff` of `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS` vs `corpus/evidence/round35/tb2-eval/SHA256SUMS` shows the same six digest+name pairs reordered. The README claims byte-identity of the six *files* (true), not of the manifests; noted so a later `cmp` isn't misread as a defect.
- **N2 — the round-34 captures path is unnamed.** The bullet says "byte-identical to the round-34 captures" without saying those captures live at `.ufo/waves/round-34/assimilation/captures/tb2-eval/` (committed at tip). Verifiable, but requires hunting.
- **N3 — "maps instruction bullets to the assertion that enforces them" (L68).** The entry's table covers the bullets the 18 cases exercise and separately lists three unexercised bullets (antibody-binder variant/repeat, DHFR substitution, FPbase spectral). The sentence describes the mapping method, not totality; the caveat lives in the entry the row points to.

## Adjacent, out of scope (for the C1 seats)

`plans/round35_c1_verify.py` docstring says the frozen predicate sentence is "same sentence in plans/round-35-claims.md and in the receipt label" — the receipt (`corpus/evidence/round35/tb2-grader-probe.txt`, 21 lines) contains no predicate sentence/label; the claims doc has it. Docstring wording only; no README impact.

## Residual risk / verification gaps

- I did not run `python3 plans/round35_c1_verify.py --lane .` myself — the C1 falsifier seats own that predicate (it re-runs the probe via uv and the census). My V4/V5 statements come from reading its code, not a run.
- "Re-fetched 2026-10-25": the checkable content (lane bytes == pinned upstream digests == round-34 capture bytes) holds via my live re-fetch; the fetch *event* during the round has no separate receipt (capture mtimes 15:47 vs 16:26 Oct 25 are consistent with it).
- Task count relies on the GitHub tree API at the pin (`truncated: False`).

VERDICT: readme-1-defects
