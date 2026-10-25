source: S105 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/tasks/protein-assembly/tests/test_outputs.py#L10-L73
source: S106 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/tasks/protein-assembly/tests/test.sh#L18-L30
source: S107 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/tasks/protein-assembly/environment/antibody.fasta
verified-at: 2026-10-26
recheck: 180d — re-run the Gate commands for S105–S107 against the pinned revision

# Terminal-Bench task grader: protein-assembly

At pinned revision `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, the `protein-assembly` output test grades one `/app/gblock.txt` against literal encoded-protein sequences and sequence-structure constraints; its shell runner writes a binary reward from pytest success.

## Scope and evidence

This is a static reading of `tests/test_outputs.py` and `tests/test.sh` for one task only, grounded against the task environment inputs `environment/antibody.fasta` and `environment/pdb_ids.txt`. Source rows S105–S107 identify those pinned bytes and their located anchors. Harbor context is bounded by S092 (verifier-mode selection, stale reward handling, and test restoration) and S100 (pinned Terminal-Bench tree/task-script context); neither turns this task-level reading into evidence of a particular run. The environment files are reference inputs; the output test embeds the expected protein amino-acid sequences as literals rather than opening either environment file during `test_gblock`.

## Load-bearing grader logic

| Predicate / mechanism | What the captured code does | Boundary |
|---|---|---|
| Output file | Requires `/app/gblock.txt` to exist; strips trailing whitespace per read line, then requires exactly one line. Lowercases that line, requires a full match of `[atcg]+`, and caps length at 3000 nucleotides. | The source checks this file representation and alphabet/length; it does not establish biological correctness generally. |
| Translation and fusion order | Translates the lowercase DNA using Biopython `Seq.translate()`. Searches for literal `flag_aa`, `donor_aa`, `dhfr_aa`, `acceptor_aa`, and `snap_aa`; requires their first found indices strictly ordered flag → donor → dhfr → acceptor → snap. | The specific expected sequences are literals in `test_outputs.py`; index ordering alone is supplemented by the boundary and linker checks below. |
| Fusion boundaries | Requires flag at amino-acid index 0 and snap's end to equal translated sequence length. Between each adjacent literal protein, each intervening segment must fully match `[GS]+` and have length 5–20 amino acids. | This makes the intervening segments GS-only and nonempty; it excludes terminal linkers by the endpoint checks. |
| GC windows | Counts `g`/`c` in the first 50 nucleotides, then slides one base at a time across the sequence; each complete 50-nt window must have 15–35 GC bases inclusive (30–70%). | The checks apply to every full 50-base window; there is no separate partial-window rule. |
| Reward production | `test.sh` runs pytest against `/tests/test_outputs.py`; on pytest exit 0 it writes `1` to `/logs/verifier/reward.txt`, otherwise writes `0`. | This is the runner's pass/fail mapping, not a richer score. |
| Harbor reward context | Harbor source context is cited via S092 and S100: S092 documents harness verifier-mode/restoration behavior and S100 pins the benchmark tree context. | This task excerpt alone does not demonstrate Harbor's behavior in a live task run; the reward-file consumer/aggregation stage is outside these two captured task files. |

## Expected-artifact grounding

`environment/antibody.fasta` contains two FASTA records labelled heavy chain and light chain (captured lines 1–4); `environment/pdb_ids.txt` is a list of PDB identifiers (captured lines 1–20). They are the task's reference inputs, also named by `instruction.md` as antibody sequence and PDB API-selection inputs. The test's implementation does not parse or open these environment files: `test_outputs.py` embeds literal expected amino-acid strings for its five fusion components and checks their translated presence/order. Its comment at lines 25–26 claims that only one PDB-listed protein matches the requirements for each subprotein; its lines 29–35 describe the donor and acceptor setup. Consequently, artifact grounding here establishes their role as task reference inputs and the evaluator's embedded-sequence approach, not a demonstrated runtime lookup or a sequence-by-sequence derivation from those files.

## Negative space

This entry does **not** establish task validity; actual runtime execution or hosted-judge behavior; any contamination measurement; any model performance; or a claim about the other 88 tasks. It does not establish successful biological binding, API availability, or that the embedded sequences faithfully follow every task instruction. It describes the static predicates present in one pinned grader and its runner only.

## Appendix — located quotes from captured bytes

Quotes below are from this round's captured source bytes, not staged package text; each is at most 25 words. Line references name the capture paths.

| Claim supported | Exact quote | Captured location |
|---|---|---|
| File existence | “assert gblock_path.exists(), f"File {gblock_path} does not exist."” | `assimilation/captures/tb2-eval/test_outputs.py:14` |
| Single line | “assert len(lines) == 1, "Invalid number of lines in gblock.txt."” | `assimilation/captures/tb2-eval/test_outputs.py:19` |
| Alphabet and length | “assert re.fullmatch(r"[atcg]+", gblock)” / “assert len(gblock) <= 3000” | `assimilation/captures/tb2-eval/test_outputs.py:22-23` |
| Translation and expected component literals | “gblock_aa = str(Seq(gblock).translate())” | `assimilation/captures/tb2-eval/test_outputs.py:27` |
| Ordered fusion | “assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx” | `assimilation/captures/tb2-eval/test_outputs.py:42` |
| Terminal boundaries | “assert flag_idx == 0” / “assert snap_idx + len(snap_aa) == len(gblock_aa)” | `assimilation/captures/tb2-eval/test_outputs.py:46,60` |
| GS-only linkers | “assert re.fullmatch(r"[GS]+", linker)” | `assimilation/captures/tb2-eval/test_outputs.py:54` |
| Linker length | “assert 5 <= len(linker) <= 20” | `assimilation/captures/tb2-eval/test_outputs.py:57` |
| Sliding GC rule | “assert 15 <= gc <= 35” | `assimilation/captures/tb2-eval/test_outputs.py:71` |
| Reward runner invocation | “pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA” | `assimilation/captures/tb2-eval/test.sh:23` |
| Reward success mapping | “echo 1 > /logs/verifier/reward.txt” | `assimilation/captures/tb2-eval/test.sh:27` |
| Reward failure mapping | “echo 0 > /logs/verifier/reward.txt” | `assimilation/captures/tb2-eval/test.sh:29` |
| FASTA records | “>heavy chain” / “>light chain” | `assimilation/captures/tb2-eval/antibody.fasta:1,3` |
| PDB identifiers | “2IB5” / “4KGE” | `assimilation/captures/tb2-eval/pdb_ids.txt:1-2` |
| Task calls antibody file an input | “whose heavy and light chain sequences are in the antibody.fasta file.” | `assimilation/captures/tb2-eval/instruction.md:6` |
| Task calls PDB list a reference | “found in /app/pdb_ids.txt.” | `assimilation/captures/tb2-eval/instruction.md:14` |
| Embedded protein expectation rationale | “We can directly check that the gBlock contains specific sequences” | `assimilation/captures/tb2-eval/test_outputs.py:25` |

VERDICT: entry-tb2-drafted