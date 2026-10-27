## Gate

Opened or captured this round. Access date 2026-10-26 for every row; times are -03. The L1 fetched all eleven
files of the task directory at 20:10:09 -03 (`corpus/evidence/round44/tb2-feal-linear-cryptanalysis/` +
`SHA256SUMS`); seat `R44PkgRows` re-fetched all eleven at 20:33:51–20:34:08 under the round-44 envelope, eleven
`http=200`, eleven `cmp=identical` (`.ufo/waves/round-44/wave/R44PkgRows/refetch.txt`); seat `R44ScoutRefetch`
re-fetched the same eleven independently at 20:33:08–20:33:10 (`ok=11`, upstream drift 0 after the pin).
Quotes are ≤25 words and located at the cited line of the capture. Ranges are `:1-<last physical line>`, so
`README.md:1-32` and `decrypt.c:1-142` count the last line of two files that carry no final newline — the
round-43 closure R2 defect was this off-by-one on `README.md`. Base URL
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/`.

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| S138 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/test_outputs.py`, opened 20:10:09, re-fetched 20:33:51. Quote, `test_outputs.py:122`: "assert c in data" (4 words); sha256 `f59ebc72…106ed9f9`. The whole score: 100 decimals inside one string (`:4-103`), the file read whole at `:120`, and one membership assert per constant at `:121-122`. Flip: digest leaves the pin. |
| S139 `instruction.md` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>instruction.md`, opened 20:10:09, re-fetched 20:33:51. Quote, `instruction.md:7`: "Implement a known-plaintext attack that recovers the key of the cipher." (11 words); sha256 `a2f1669d…b6f71b03`. Asks for an attack and an output file and no numeric format; the receipt's `hex-output` case fails a format the instruction never states. Flip: digest leaves the pin. |
| S140 `environment/task-deps/gen.py` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>environment/task-deps/gen.py`, opened 20:10:09, re-fetched 20:33:51. Quote, `gen.py:12`: “keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]” (6 words); sha256 `3a71f0b5…7c452c63`. The four round keys sit in the clear and `:23-28`/`:57-62` derive every plaintext from the public hash chain; receipt cases `decrypt-public-keys` and `replay-public-gen` pass with no attack. Curly delimiters because the line itself carries straight quotes (precedent S121/S123). Flip: digest leaves the pin. |
| S141 `environment/Dockerfile` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>environment/Dockerfile`, opened 20:10:09, re-fetched 20:33:51. Quote, `Dockerfile:14`: "RUN rm gen.py" (3 words); sha256 `ef521cde…28bfff1d`. Builds `feal` and `decrypt`, runs the generator, then deletes `orig_plaintexts.txt` and `gen.py` (`:13-14`): the keys are absent from the image and public in the repo. Flip: digest leaves the pin. |
| S142 `tests/test.sh` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/test.sh`, opened 20:10:09, re-fetched 20:33:51. Quote, `test.sh:26`: "echo 1 > /logs/verifier/reward.txt" (4 words); sha256 `9431cbc2…d2e7c9e1`. Reward is pytest's exit status alone (`:25-28`), after uvx runs pytest 8.4.1 over `/tests/test_outputs.py` (`:18-22`). Flip: digest leaves the pin. |
| S143 `README.md` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>README.md`, opened 20:10:09, re-fetched 20:33:51. Quote, `README.md:32`: "verifies that all 100 expected plaintext values appear in" (9 words); sha256 `a038645f…f6d3dc33`. Its verification claim is exactly the substring behaviour receipt cases `oracle-concatenated`, `oracle-reversed`, `oracle-zero-padded` and `oracle-plus-decoys` exploit. Flip: digest leaves the pin. |
| S144 `solution/solve.sh` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>solution/solve.sh`, opened 20:10:09, re-fetched 20:33:51. Quote, `solve.sh:304`: "./attack > /app/plaintexts.txt" (3 words); sha256 `be50ae01…da29cb77`. The provided oracle; it is not graded (test.sh runs only `/tests/test_outputs.py`) and the probe runs it as a recipe. Flip: an entry sentence implies `solve.sh` participates in grading. |
| S145 `environment/task-deps/decrypt.c` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>environment/task-deps/decrypt.c`, opened 20:10:09, re-fetched 20:33:52. Quote, `decrypt.c:136`: “printf("%lu\n", plaintext);” (2 words); sha256 `4c6864e0…0a94ebd2`. The decimal print is the medium the substring test accepts; `:114-117` refuses a key above `0xFFFFF`. Curly delimiters as on S140. Flip: an entry sentence claims a non-decimal rendering passes (receipt `hex-output` = fail) or that `decrypt.c` is graded. |
| S146 `task.toml` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>task.toml`, opened 20:10:09, re-fetched 20:33:52. Quote, `task.toml:34`: "allow_internet = true" (3 words); sha256 `a39ec2c4…0e7c9fc4`. `timeout_sec = 1800.0` at `:22` (verifier) and `:25` (agent), resources at `:30-32`; `allow_internet` is what keeps the published `gen.py` fetchable although the image deletes it. Flip: an entry sentence asserts grader-side timeout enforcement or calls `:22` the only time bound (the round-43 finding-11 error). |
| `feal.c` @ `2fd12b88` (captured, not a row) | **REJECT — captured, not a row** | `environment/task-deps/feal.c`, re-fetched 20:33:52 (`200`, 3472 B, `cmp` identical, sha256 `bbd38d19…2dea08da`). Implementation of the pair-generator executable: the graded artefact is `/app/plaintexts.txt`, so `feal.c` carries no graded predicate. Flip, decided by the command below: an entry sentence outside `## Located quotes` cites `feal.c:<line>` with no S138–S146 co-citation; if it fires, either re-source the sentence or take the tier-B mechanism path (S135–S137 precedent). |
| `gitignore` @ `2fd12b88` (captured as `gitignore`, upstream `.gitignore`) | **REJECT — captured, not a row** | Upstream path is `.gitignore` (`.gitignore` → `200`, 177 B; every `gitignore` spelling → `404`), re-fetched 20:34:08, `cmp` identical, sha256 `9a8dd8d9…07c25953`; the capture keeps the dotless name. Repo hygiene only: ignores `.git/`, `__pycache__/`, `dist.tar.gz` (`:2`, `:8`, `:23`). Flip: an entry sentence outside `## Located quotes` cites `gitignore:<line>` or `.gitignore:<line>` with no S138–S146 co-citation; no tier-B path exists for it — re-source or delete the sentence. |
| `SHA256SUMS` | **REJECT — inventory, not content** | Manifest of the eleven captures; contentless as evidence. Flip: an entry sentence cites it. |

Flip checks (round 44) are decided by the command below, not by presence of a flip line (`plans/gate_flip_check.py`
tests line existence, which is how round 43 recorded a false `not fired`). Quote table excluded; a hit line is
unbacked when it carries no `S1xx` co-citation:

```
check_flip() { # $1 = file token, $2 = entry path
  body=$(awk '/^## Located quotes/{skip=1;next} /^## /&&skip{skip=0} !skip' "$2")
  if printf '%s\n' "$body" | grep -nE "$1:[0-9]+" | grep -qvE 'S1[0-9]{2}'; then
    echo "Flip check (round 44): $1 — fired"
  else
    echo "Flip check (round 44): $1 — not fired"
  fi
}
check_flip 'feal\.c'    corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
check_flip gitignore    corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
check_flip SHA256SUMS   corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
```

Run 20:39 -03 against the seat draft `.ufo/waves/round-44/wave/R44PkgEntry/tb2-feal-linear-cryptanalysis-grader.md`
(the landed entry must reproduce this, or the verdict below is void — the flip line is re-decided at integration):

Flip check (round 44): feal.c — not fired — the draft names `feal.c` only as a compile target backed by `Dockerfile:9` and inside the `instruction.md:1` quote
Flip check (round 44): gitignore — not fired — the draft never names it
Flip check (round 44): SHA256SUMS — not fired — the draft never names it

Gate prose: all nine rows are the spec-pinned set (`plans/pkg-spec-r44.json` `rows` = S138–S146) — six `code`
(S138, S140, S141, S142, S144, S145), three `docs` (S139, S143, S146) — tier A as `entry_rules.row_tier`
fixes, status mined, opened 2026-10-26, recheck 180d, one used-by entry. Registry 130 → 139. Validated in a
scratch `--shared` clone at `5e3d3aa` with the rows appended uncommitted: `sources-census.sh validate --file
<clone>/corpus/SOURCES.md` exit 0, 15 W04 (all pre-existing), 0 E-codes; `anchor_digest_check.py --lane
<clone>` `rows=139 tokens=45 defects=0`, nine `BIND … by=url-task` and nine `RESOLVED`. Red controls on the same
two legs: removing the used-by file fires E11 on all nine rows (exit 1); flipping S138's last digest nibble
prints `DEFECT S138 … class=digest-unknown` (`defects=1`, exit 1). The census copy carried a labelled
placeholder file at the entry path because the entry is authored by seat `R44PkgEntry` and was not
present when these rows were written; E11 tests existence only, and the placeholder is never a lane file.
