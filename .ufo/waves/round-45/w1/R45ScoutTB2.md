# R45ScoutTB2 — TB2 frontier reconnaissance for round 46 (read-only scout)

Pin: terminal-bench-2 @ 2fd12b88aafdd04a52c298e3940bcb189f9766d6. Raw base
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/…`.
No lane file edited; fetched files lived only in `/fast/scratch/hyaku/kengaku-r45/R45ScoutTB2` (deleted at end). Nothing run, only read.

## 1. Denominator and executed sample (observed)

- Tree at pin via `GET api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…?recursive=1`: `truncated=False`, 1446 entries; **89 top-level task dirs, every one with `tests/test_outputs.py`** (python count printed `89 89`). The "89" in the README Frontier is correct at the pin.
- Executed/admitted in `corpus/knowledge/tb2-*-grader.md` (`ls` = 10 files) and README §Frontier sub-bullets (README.md:295-304, "N of the 89"), in order:
  1 protein-assembly (r35) · 2 regex-log (r36) · 3 configure-git-webserver (r37) · 4 build-pmars (r38) · 5 git-leak-recovery (r39) · 6 db-wal-recovery (r40) · 7 constraints-scheduling (r41) · 8 circuit-fibsqrt (r42) · 9 feal-differential-cryptanalysis (r43) · 10 feal-linear-cryptanalysis (r44).
  Cross-check: SOURCES.md task names with TB2 rows (grep) = exactly those ten, no other.
- **password-recovery is task #11 — confirmed.** It is not among the 10 above, no SOURCES row names it before S149, the capture dir `corpus/evidence/round45/tb2-password-recovery/` is new this round, and the frozen claims file (`plans/round-45-claims.md:71-72`) already words "11 of 89". README §Frontier line should read "11 of 89 read", remaining = **78 of 89 unread**.
- Class bookkeeping (README coverage bullets, :295-304): tasks 1-10 + 11 are F1-like/other exemplars as follows — #10 feal-linear = 100 constants as substrings of one file (`tests/test_outputs.py:120-122`); #11 password-recovery = one constant as exact line in a guess list (`test_outputs.py:14,18` per claims).

## 2. Remaining task graders by shape (78 unread; fetched and read the 14 smallest/most telling)

### 2a. F1-like constant graders (agent writes a small text file; grader compares to a literal)
Sizes from tree (`test_outputs.py` bytes). All quotes ≤25 words, from pinned raw files fetched 2026-10-26 ~23:25 -03.

| task | bytes | comparison | evidence |
|---|---|---|---|
| crack-7z-hash | 789 | strip, exact equality to one 9-char word; no format/count | `crack-7z-hash/tests/test_outputs.py:23,25` `content = f.read().strip()` / `assert content == "honeybear"`; instruction.md:1 |
| count-dataset-tokens | 467 | **substring** of 5-digit constant in file (`"79586" in text`) — "12 345 79586 9" passes | `count-dataset-tokens/tests/test_outputs.py:8-11`; instruction.md:4 says write integer without spaces/commas, grader doesn't check that |
| mteb-leaderboard | 537 | exactly one line, strip-equal to `GritLM/GritLM-7B` (a dated live-leaderboard fact: "as of August 2025") | `mteb-leaderboard/tests/test_outputs.py:11,14-15` |
| mteb-retrieve | 559 | exactly one line == `MTEB: Massive Text Embedding Benchmark` | `mteb-retrieve/tests/test_outputs.py:11,14-15`; oracle `solution/solve.sh:10-14` asserts unique similarities |
| code-from-image | 935 | strip, startswith `bee26a` (hint given in instruction.md:3) AND exact 64-hex equality | `code-from-image/tests/test_outputs.py:25,28-31` — the `startswith` assert is subsumed by the equality |
| gcode-to-text | 644 | strip equality to flag string | `gcode-to-text/tests/test_outputs.py:17` `== "flag{gc0d3_iz_ch4LLenGiNg}"` |
| vulnerable-secret | 1346 | strip equality to `FLAG{…}`; later format test (startswith/endswith/len>10) is dead-subsumed by equality | `vulnerable-secret/tests/test_outputs.py:21-22,33-39` |
| chess-best-move | 971 | set-equality: `sorted(move)==sorted(["g2g4","e2e4"])` over whitespace-split tokens (order/count-fixed pair) | `chess-best-move/tests/test_outputs.py:23,25` |

Near-identical to password-recovery's class (one constant, exact membership/equality) — adding more of these narrows the denominator but adds no new class; at most one more (the substring variant, count-dataset-tokens, or a dated-fact one, mteb-leaderboard) is worth a pass as a class-variant row. Note count-dataset-tokens :8-11 is the same substring family as #10 (feal-linear :121-122), at n=1 constant; mteb-leaderboard/mteb-retrieve share the exact one-line shape (`readlines()` count == 1), a distinct tell from password-recovery's line-membership.

### 2b. Genuinely different shapes (grader executes, compiles or re-derives, not a constant read)
| task | bytes | shape | evidence |
|---|---|---|---|
| polyglot-c-py | 1564 | grader **runs the agent's file twice** (python3 + gcc) on 3 fixed inputs; `os.listdir("/app/polyglot") == ["main.py.c"]` checked BEFORE the gcc build leaves `cmain` | `polyglot-c-py/tests/test_outputs.py:17-19,23-25,27,44-46` |
| prove-plus-comm | 1147 | compiler-as-oracle + text assertions: `coqc plus_comm.v` rc==0, plus substring checks `"Proof."`, `"Qed."`, and `"admit" not in content` (lower-case only) | `prove-plus-comm/tests/test_outputs.py:20-25,30-35` — **[INFERENCE, not run]** capital-A `Admitted.` does not contain lowercase `admit`; whether coqc exits 0 on it is a runnable question |
| fix-ocaml-gc | 809 | grader **rebuilds the whole repo itself** and overwrites the log; the only assert is `"40 tests passed" in tests.txt` | `fix-ocaml-gc/tests/test_outputs.py:13-19`; `tests/test.sh:20-21` re-clones `sadiqj/ocaml` and replaces `testsuite`, `:27-28` `rm tests.txt` then `tee tests.txt`; network at grading time (:4-8, :20) |
| sqlite-db-truncate | 1097 | thresholded set intersection: `len(soln ∩ data) > 6` of 8 expected `(word,value)` tuples (a sibling of #6 db-wal-recovery, thresholded rather than pinned cells) | `sqlite-db-truncate/tests/test_outputs.py:24-31` |
| fix-git | 1194 | md5 of `.strip()`ped file bytes vs reference patch files (both in /app) — repository **end-state hash**, no git inspection of history | `fix-git/tests/test_outputs.py:8,19,30,39` |

Other large/odd shapes seen in the tree listing (sizes only, not read): `schemelike-metacircular-eval` (139 files incl. `tests/shadow_test/*.scm`, `tests/interp.py`), `financial-document-processor` (26 files), `install-windows-3.11` (`tests/qemu-control.sh`), `sam-cell-seg` / `video-processing` / `make-doom-for-mips` (binary reference assets: png/mp4/jpg), `pytorch-model-recovery` (`tests/weights_gtruth.pt`), `train-fasttext` (`tests/private_test.tar.gz`), `filter-js-from-html`/`break-filter-js-from-html` (18746 / 3270 B + `tests/filter.py`), `dna-assembly` (14105 B), `llm-inference-batching-scheduler` (cost model in tests). These are the likely "different shapes" for later rounds but need a read before any claim.

## 3. Round-46 candidates (ranked)

1. **polyglot-c-py** — new class ("grader executes an agent-authored program in two interpreters with a directory-listing precondition"); small (46 lines), no network, no reference assets; lines `:17-19`, `:23-25`, `:27`, `:44-46`; fully runnable offline with python3+gcc in the lane's sandbox style (cases: C-only, Python-only, extra file, `Admitted`-style evasions N/A; fib(42) arithmetic). Distinct from feal-differential (#9) which imports a module in-process.
2. **prove-plus-comm** — new class ("compiler verdict AND blacklist/whitelist substrings over the proof text", `:20-25,:30-35`); 1147 B; probe needs `coqc` (not checked installed — unknown; `pacman` is paused host-wide, so use `uv`/an official binary or run the textual legs only and say so). Closest to a "compiler judges, text lint also judges" shape, contrasting #8's grader-built simulator.
3. **fix-ocaml-gc** *or* **sqlite-db-truncate** — pick by what the lane can run offline: fix-ocaml-gc is the strongest "grader recomputes the evidence itself" class (`test.sh:20-28`) but needs network + a full OCaml build at grading, so only read + a log-marker probe is feasible (`"40 tests passed"` substring, `test_outputs.py:19`); sqlite-db-truncate (`:24-31`, threshold >6 of 8) is cheap and runnable but sits next to #6.
   Fallback for an F1-variant if round 46 wants a low-cost coverage step: **count-dataset-tokens** (substring, `:8-11`) — contrasts #11's whole-line membership with #10's substring family.

## 4. Mined-mistake rows noticed on this walk (for the Frontier step, routing only)
- README-side: the line "task #11 / 11 of 89" must be written once; round-44 README bullets order r44 (tenth) BEFORE r43 (ninth) in the coverage-map list (README.md:303-304) — a presentational ordering slip, not content.
- instruction.md ↔ grader drift: count-dataset-tokens states "without spaces or commas" (`instruction.md:4`) while the grader is a substring check (`test_outputs.py:11`); code-from-image's `startswith` assert (`:25`) is dead given equality (`:28-31`); vulnerable-secret's format assert (`:33-39`) is dead given equality (`:21-22`) — same dead-assert family as password-recovery's `len(guesses) > 0`.

## 5. Limits
Read only; nothing executed (no graders run). The shape sort covers 14 of 78 unread tasks by reading; the rest (64) classified by size/asset listing only and are unread. Sizes come from the git tree API (blob `size`).

VERDICT: frontier-11-of-89-candidates-3
