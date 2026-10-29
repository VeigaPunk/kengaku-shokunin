# W2ScoutVerifyQuotes — kengaku round 52, wave 2 (falsify), hyaku run 11

2026-10-28. Read-only seat: verified every quote and anchor the round's new SOURCES rows will
carry for the four sources my item names. **Verdict: attack landed; no defect found.** All four
quotes appear verbatim at their cited lines in the pinned bytes, all four are ≤25 words, and the
three grader fetches are byte-identical to the lane's pinned captures.

## Sources verified (repo `harbor-framework/terminal-bench-2`, pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`)

| # | source | pinned URL | line | verbatim quote | words | sha256 (fetched bytes) | bytes |
|---|---|---|---|---|---|---|---|
| 1 | TB2 README | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md` | 24 | `Terminal-Bench is a popular benchmark for measuring the capabilities of agents and language models to perform valuable work in containerized environments.` | 21 | `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364` | 4574 |
| 2 | bn-fit-modify grader | `…/2fd12b88aafdd04a52c298e3940bcb189f9766d6/bn-fit-modify/tests/test_outputs.py` | 17 | `assert bn_sample_path.exists(), f"File {bn_sample_path} does not exist"` | 7 | `364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b` | 5892 |
| 3 | pytorch-model-recovery grader | `…/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pytorch-model-recovery/tests/test_outputs.py` | 108 | `assert hello_path.exists(), f"File {hello_path} does not exist"` | 7 | `5d4d57c43e6913bf3d0081da764ad36d1b7275e3bb114a05abda529afe563905` | 5591 |
| 4 | torch-tensor-parallelism grader | `…/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-tensor-parallelism/tests/test_outputs.py` | 25 | `assert parallel_linear_path.exists(), f"File {parallel_linear_path} does not exist"` | 7 | `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290` | 7171 |

Line numbers are 1-based on the pinned bytes. Each quote occurs exactly once in its file.
URLs abbreviated with `…` in this table carry the same `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2` prefix; the full URLs are in `quote-check.json`.

## Exact commands run

```sh
S=/fast/scratch/hyaku/kengaku-r52/w2-W2ScoutVerifyQuotes
B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6
curl -fsS "$B/README.md" -o "$S/README.md"
curl -fsS "$B/bn-fit-modify/tests/test_outputs.py"          -o "$S/bn-fit-modify__test_outputs.py"
curl -fsS "$B/pytorch-model-recovery/tests/test_outputs.py" -o "$S/pytorch-model-recovery__test_outputs.py"
curl -fsS "$B/torch-tensor-parallelism/tests/test_outputs.py" -o "$S/torch-tensor-parallelism__test_outputs.py"
sha256sum "$S/README.md" "$S"/*__test_outputs.py
grep -n 'Terminal-Bench is a popular benchmark' "$S/README.md"
grep -n 'bn_sample_path.exists()' "$S/bn-fit-modify__test_outputs.py"
grep -n 'hello_path.exists()' "$S/pytorch-model-recovery__test_outputs.py"
grep -n 'parallel_linear_path.exists()' "$S/torch-tensor-parallelism__test_outputs.py"
```

Plus a Python pass (kernel `eval`) that re-hashed the fetched bytes, re-verified each quote as a
unique substring of its cited line, counted words (whitespace split), and wrote
`quote-check.json`. Cross-checks against the lane tree (grep tool, read-only):
`corpus/evidence/round52/graders/SHA256SUMS` lines 3 / 138 / 171 carry digests
`364069f8…`, `5d4d57c4…`, `4ae4285e…` — each **equals** the fetched file's sha256; and each
quote's exact bytes are present in the lane's own captured file
(`corpus/evidence/round52/graders/<task>/tests/test_outputs.py`).

## Measured findings

- **All 4 quotes verbatim at the cited lines** in the pinned bytes; each unique in its file.
- **All 4 quotes ≤25 words**: README first sentence 21 words; each assert quote 7 words
  (word rule: whitespace split). Note for the scribe: README line 24 as a whole is 34 words —
  the row's quote must be the first sentence only to satisfy the ≤25-word rule.
- **Fetched == captured**: the three grader files' fetched sha256 equal their `SHA256SUMS`
  digests and the sha256 of the lane's captured bytes, so the A1 hardened CONFIRMED leg's
  "quote appears verbatim in the captured grader bytes" requirement is demonstrably satisfiable
  for these three tasks.
- **Anchors agree with Amendment A1's per-test names**: the bn-fit-modify assert at line 17 sits
  in `test_bn_sample_exists` (def line 13); pytorch-model-recovery line 108 sits in
  `test_model_file_exists` (def line 103); torch-tensor-parallelism line 25 sits in
  `test_parallel_linear_exists` (def line 18). Each function's file contains further tests that
  compare content (e.g. `test_sampled_data` at bn-fit-modify:115, `test_state_dicts_match` at
  pytorch-model-recovery:119, `test_column_parallel_linear` at torch-tensor-parallelism:187),
  consistent with A1's statement that the weakness is per test function, not file-level.
- **README has no lane capture** (the 184-capture population is grader files only), so no local
  byte cross-check exists for it; its fetched sha256 is recorded above for the SOURCES row.
- No anomalies found: no quote mismatch, no digest mismatch, no off-by-one line anchor.

## Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScoutVerifyQuotes/report.md` — this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScoutVerifyQuotes.md` — same report at the seat-target path (wave-1 convention).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScoutVerifyQuotes/quote-check.json` — machine-readable receipt (per-source URL, line number, verbatim line, quote, word count, sha256, byte count, lane-capture crosschecks). Original written in scratch, copied here before scratch removal per scratch discipline.

## Scope notes

- Scratch dir `/fast/scratch/hyaku/kengaku-r52/w2-W2ScoutVerifyQuotes/` removed before yield (542 GB free on `/fast` at start; no ENOSPC).
- No tools installed or upgraded (nothing needed beyond `curl`/`sha256sum`/`grep`/`python3`).
- No lane-tree, fleet-repo, sibling, `.ufo/state/`, watchdog, `templates/`, `scripts/`, `MANIFEST.json`, or `~/.local/bin` writes. No git/jj mutations. No peer messages (none authorized).
- The excluded capture (`sanitize-git-repo/tests/test_outputs.py`, A5) was never touched, fetched, or counted — it is not among my four sources.
- Verification method is text/byte-level (curl + sha256 + substring match); LSP is inapplicable to remote pinned bytes. The three graders' fetch-equals-capture equality makes text-level proof byte-exact for those sources.
