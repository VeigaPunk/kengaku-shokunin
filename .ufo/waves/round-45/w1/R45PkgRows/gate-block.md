## Gate

Opened this round. Access date **2026-10-26** for every candidate; times are -03. Every quote below is taken
from the committed capture under `corpus/evidence/round45/tb2-password-recovery/` (frozen at `b4fcd35`), at the
cited physical line, and is ≤25 words (range 3–25 per `plans/pkg-spec-r45.json` `entry_rules.quote_words`).
The capture bytes were re-verified at 23:32:00 -03 by the entry's own recheck command, `(cd
corpus/evidence/round45/tb2-password-recovery && sha256sum -c SHA256SUMS)`: nine `OK`, exit 0
(`controls.txt` §Capture manifest). Base URL
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/`.
Ranges are `:1-<last physical line>`; `setup.sh` (43 lines) and `README.md` (33 lines) carry no final newline,
so their stated ranges are the last physical line, not last newline (round-43 closure R2 off-by-one).

Nine files were captured; **eight are rows**. The ninth, `gitignore`, is rejected below. `plans/pkg-spec-r45.json`
`rows` contains exactly S149–S156, so no registry id is minted for `gitignore` and the registry grows 141 → 149.

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| S149 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/test_outputs.py`, opened 2026-10-26 (capture). Quote, `test_outputs.py:18`: "assert \"8XDP5Q2RT9ZK7VB3BV4WW54\" in guesses, \"Password not found\"" (7 words); sha256 `2dc14fc1…ed3bfc9e`. Whole score: `:9-10` existence, `:14` read+`.strip().split("\n")`, `:16` dead non-empty assert, `:18` membership — no format, case, order, count or uniqueness rule. Flip: the capture digest leaves the pin, or a probe case shows a decoy-bearing file failing. |
| S150 `instruction.md` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>instruction.md`, opened 2026-10-26. Quote, `instruction.md:9`: "You are allowed to make multiple guesses. Write each matching password you find, one per line, to the file: /app/recovered_passwords.txt" (20 words); sha256 `bc4f5011…20b7810a5`. Names the artefact and the three constant constraints (`:4-7`) and permits many guesses; states no order, count or uniqueness. Flip: a capture revision adds a stated output format. |
| S151 `environment/setup.sh` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>environment/setup.sh`, opened 2026-10-26. Quote, `setup.sh:25`: "echo \"PASSWORD=8XDP5Q2RT9ZK7VB3BV4WW54\" > /app/launchcode.txt" (4 words); sha256 `9fdde5d9…5a6f2af8`. The graded constant is a literal of the build recipe (`:25`), fragmented at `:26-37` into a 4 MB image; a reader of the repo holds the answer. Flip: the constant stops appearing in the recipe or the image digest changes the placement offsets. |
| S152 `environment/Dockerfile` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>environment/Dockerfile`, opened 2026-10-26. Quote, `Dockerfile:17`: "RUN bash /app/setup.sh" (3 words); sha256 `6fabcb9e…4b6c9fe0`. Ubuntu 24.04 plus the forensic toolset (`:3-14`), seeding at build time then `rm /app/setup.sh` (`:17-18`), `WORKDIR /app` (`:20`) — which the harness's `/` guard and the oracle's relative output both need. Flip: the seeder is no longer run at build time. |
| S153 `tests/test.sh` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/test.sh`, opened 2026-10-26. Quote, `test.sh:26`: "echo 1 > /logs/verifier/reward.txt" (4 words); sha256 `4770437e…716e6c334`. Reward is pytest's exit status alone (`:25-29`) from one uvx pytest 8.4.1 run over `/tests/test_outputs.py` (`:18-22`); the ctrf json is written and never read. Flip: an entry sentence claims partial credit or a second scored artefact. |
| S154 `README.md` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>README.md`, opened 2026-10-26. Quote, `README.md:31`: "3. That the correct password \`8XDP5Q2RT9ZK7VB3BV4WW54\` is among the recovered passwords" (11 words); sha256 `122bf15e…ac6a13add`. The README prints the graded constant and its three checks (`:29-31`) and its 900 s/15 min figure (`:17`) matches `task.toml:22,25`. Flip: an entry sentence treats `:17` as a bound the verifier enforces. |
| S155 `solution/solve.sh` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>solution/solve.sh`, opened 2026-10-26. Quote, `solve.sh:63`: "echo \"$combined\" >> \"$OUTPUT_FILE\"" (4 words); sha256 `c5f9fc70…7b8d804f`. The oracle: byte-offset search (`:11-16`, `:30-33`), longest A-Z0-9 window (`:22-26`, `:41-47`), trim-pair enumeration at length 23 (`:55-66`); the constant never appears in it, and `:51` writes relatively, reaching `/app` only through `WORKDIR`. Flip: an entry sentence claims the oracle verifies the constant. |
| S156 `task.toml` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>task.toml`, opened 2026-10-26. Quote, `task.toml:22`: "timeout_sec = 900.0" (3 words); sha256 `cfd0362d…cfd091b24b`. `:5`/`:29` pin the task and image, `:22`/`:25` both clocks at 900 s, `:30-34` 1 CPU / 2048 MB / 10240 MB / internet true, `:15`/`:18-19` difficulty hard with 100/300-minute human estimates above the clock. Flip: an entry sentence asserts the human estimates bound the agent. |
| `gitignore` @ `2fd12b88` (captured as `gitignore`, upstream `.gitignore`) | **REJECT — captured, not a row** | Present in the capture set at 23:32 (`sha256sum -c` OK), sha256 `9a8dd8d9…07c25953`, 177 B, 23 lines; content is repo hygiene only — `.git/` (`:2`), `__pycache__/` (`:8`), `dist.tar.gz` (`:23`). It carries nothing about what is graded: it is mentioned zero times in `tests/test_outputs.py`, `tests/test.sh` and `environment/setup.sh` (`controls.txt` §gitignore), and `plans/pkg-spec-r45.json` `rows` admits only S149–S156. Flip condition: an entry sentence outside `## Located quotes` cites `gitignore:<line>` or `.gitignore:<line>` without an S149–S156 co-citation; then re-source or delete the sentence — no tier-B mechanism path exists for it. |
| `SHA256SUMS` (capture-directory manifest) | **REJECT — inventory, not content** | Nine digest lines in upstream-relative names (`environment/setup.sh`, `tests/test_outputs.py`, …), green at 23:32 (`sha256sum -c`, exit 0). It is the recheck instrument, not a graded or explanatory artefact. Flip condition: an entry sentence cites `SHA256SUMS:<line>` as evidence for a claim about the grader. |

Not a source at all: `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` (the frozen dry table) and
`corpus/evidence/round45/password-recovery-probe.txt` (this round's receipt) — lane outputs, never registry rows.

Flip checks are decided by the command below, not by the presence of a flip line. The quote table is excluded;
a body hit is unbacked when its line carries no `S1xx` co-citation:

```
check_flip() { # $1 = file token, $2 = entry path
  body=$(awk '/^## Located quotes/{skip=1;next} /^## /&&skip{skip=0} !skip' "$2")
  if printf '%s\n' "$body" | grep -nE "$1:[0-9]+" | grep -qvE 'S1[0-9]{2}'; then
    echo "Flip check (round 45): $1 — fired"
  else
    echo "Flip check (round 45): $1 — not fired"
  fi
}
check_flip 'gitignore'                 .ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md
check_flip '(\.gitignore|SHA256SUMS)'  .ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md
```

Run 23:32 -03 against the seat draft
`.ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md` (read-only; the landed entry must
reproduce this, or the reject verdicts are re-decided at integration):

Flip check (round 45): gitignore — not fired (the draft never names it)
Flip check (round 45): (.gitignore|SHA256SUMS) — not fired (the draft names `SHA256SUMS` only as the
`sha256sum -c` command, never as `SHA256SUMS:<line>` evidence)

Gate prose: the eight rows are the spec-pinned set (`plans/pkg-spec-r45.json` `rows` = S149–S156) — five `code`
(S149, S151, S152, S153, S155) and three `docs` (S150, S154, S156) — tier A as `entry_rules.row_tier` fixes, status
mined, opened 2026-10-26, recheck 180d, one used-by entry `corpus/knowledge/tb2-password-recovery-grader.md`.
Registry 141 → 149.
