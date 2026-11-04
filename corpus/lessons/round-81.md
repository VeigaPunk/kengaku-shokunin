# Round 81 — kengaku (hyaku run 15, attempt 1, 2026-11-04)

Lane `kengaku-shokunin`. Base `4e833e9fee8022d24559535178c6fe32b2cd62f1` (round-80 verifier spot-check);
freeze `4d896e0daf8831ef7a0016bf3c944d11ba465f70`. Two claims, two axes, frozen before data in
`plans/round-81-claims.md`.

## Claims

**R81-C1 — coverage (lowest non-retired axis, held at its L0 cap).** The two population members the
frozen selection rule derives at the base revision (`unattempted`, stdlib-only imports, class set ⊆
{file-artifact, serialization-schema}, maximum captured-grader assert count = 5 among eleven
candidates) are `log-summary-date-ranges` and `vulnerable-secret`. Each now names a tracked receipt
`corpus/evidence/round81/<member>-probe.txt` whose stamp pins the round-52 capture
(`SUBJECT_CAPTURE`/`SUBJECT_SHA`), the instrument (`TOOL`/`TOOL_SHA`), the replay environment
(`HOST_PYTHON` = `Python 3.14.8`, `HOST_OPENSSL` = `OpenSSL 3.6.5 29 Sep 2026`), a reachable
`LANE_TIP`, `WORKTREE clean`, `COMMAND`, `EXIT 0` and the driver hash, and whose observation block
re-runs at the measured tree. The ledger rows are `executed` with `subject=tb2-header`,
`verdict=predicate`, `round=81`; the round-79 population gate now prints `executed=26 unlocated=0`.
Counter: `python3 plans/round81_c1_new_members.py --lane .` → `TARGET members=2 located=2
reproduced=2 ledger_flipped=2 defects=0` (`corpus/evidence/round81/c1-after.txt`).

**R81-C2 — calibration (held at ceiling 10, exercised).** The round-80 spot-check's six routed
defects `U1`…`U6` are `corpus/routed-findings.jsonl` rows `R80-U1`…`R80-U6`, closed against tracked
repair artifacts whose bytes carry the id and whose check commands exit 0 at the tip and fail at
`4e833e9f`. Counter: `python3 plans/round81_c2_spotcheck_debt.py --lane .` →
`TARGET ids=6 closed=6 checks_passed=6 indexed=yes`, `DEFECTS n=0`
(`corpus/evidence/round81/c2-after.txt`).

## Gate

Every row below was opened in this round; the anchors are the located text the row's claim rests on.

- **S259 (own-work, supersedes S258)** — `corpus/evidence/round80/<member>-probe.txt` (six) +
  `plans/round80_c1_located_replay.py`. Access 2026-11-04; anchor lines 2-12 of each receipt. Quote
  (`protein-assembly-probe.txt:2`): `MEMBER protein-assembly`. Six sha256s at this round's tip:
  `11a53bf3…`, `1a3d4e1b…`, `afef9380…`, `f60bc00b…`, `b7e66f4c…`, `778565cd…` (full digests in the
  row's anchor). The S258 anchor's six prefixes `7923b6dc…, b32f4b37…, fd337d12…, 9179d62d…,
  08c10b0d…, 82b910af…` and its `lines 1-10` are the superseded text.
- **S260 (own-work, tier A)** — the round-81 located-replay instrument set:
  `plans/round81_log_summary_probe.py`, `plans/round81_vulnerable_secret_probe.py`,
  `plans/round81_probes.json`, `plans/round81_c1_new_members.py` and the two receipts. Access
  2026-11-04; anchor `corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15`. Quote
  (`:1`): `# tb2 log-summary-date-ranges grader probe (round 81)`.
- **S261 (docs, tier A)** — the pinned Terminal-Bench 2.0 task documents at
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/`
  (`log-summary-date-ranges/instruction.md`, `log-summary-date-ranges/task.toml`,
  `vulnerable-secret/instruction.md`, `vulnerable-secret/task.toml`), fetched 2026-11-04T08:26:13Z,
  HTTP 200 each. Quotes: `log-summary-date-ranges/instruction.md:9` — "Write a CSV file /app/summary.csv
  with the following structure (including the header):" (14 words); `vulnerable-secret/instruction.md:1`
  — "The goal is to extract this secret key and save it to `/app/results.txt`." (17 words);
  `log-summary-date-ranges/task.toml:6` — "Evaluates the ability to analyze date-stamped log files,
  calculate counts across multiple date ranges, and generate structured CSV output." (19 words).
  The premise of each replay is what these documents ask the agent to produce; the replay stages it.

Rejected this round (kept as a verdict, not a row): the `tasks/<member>/task.yaml` spine was fetched
and returned 404 at the pinned tree (0 of 1446 entries are `task.yaml`; the metadata is `task.toml`
and the members are top-level directories) — it is a wrong-locator class, not a source.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M81-1 | A gate landed without a registry row, so `SKILL.md`'s registry did not describe the repo's own instruments | R80-U5 (`corpus/lessons/round-80-verifier-spotcheck.md:187`): `plans/round80_c1_located_replay.py` and `plans/round80_c2_spotcheck_debt.py` were absent from the registry until this round | `none` — no criterion required a registry row at landing; Q54 covers a frozen registry predicate, not a new gate's own row | registry rows for the two round-80 gates and the three round-81 instruments now sit in `SKILL.md`, and `python3 plans/round81_c2_checks.py u5` fails when a named gate has no row (red at `4e833e9f`, green at the tip) |
| M81-2 | A receipt was minted from a moving worktree and cited as the measurement of a revision | R80-U2 (`corpus/lessons/round-80-verifier-spotcheck.md:167`): `corpus/evidence/round80/c1-after.txt` prints `WORKTREE dirty` and its `LANE_TIP` is a `HEAD` assertion, not a tree | `none` — the round-80 mint driver checked cleanliness once before writing and the gate had no cleanliness leg in `--rev` mode | the round-81 driver runs every probe first and re-checks `git status --porcelain` before writing a receipt, and the gate rejects `WORKTREE dirty` / a `WORKTREE` stamp that is not `clean`; the dirty round-80 receipt stays as the historical record, with the errata row naming the clean block |

Sweep that found no third mistake (`grep -c` over this round's own evidence): every claim-bearing
receipt in `corpus/evidence/round81/` is named in this lesson or the round report, and every new
instrument has a registry row; the class remaining is the one this round repaired.

## Corrections

- **R80-U1 — S258's anchor pinned the pre-amendment receipt bytes.** S258's row names six sha256
  prefixes `7923b6dc…, b32f4b37…, fd337d12…, 9179d62d…, 08c10b0d…, 82b910af…` and a
  `lines 1-10 (subject at line 1, stamp at 3-10)` anchor; those are the `bb3d6555` blobs. The
  committed receipts hash `11a53bf3…, 1a3d4e1b…, afef9380…, f60bc00b…, b7e66f4c…, 778565cd…` and
  their stamp block runs to line 12 (protein-assembly's `HISTORICAL-DIVERGENCE` note occupies line
  13). S259 supersedes S258 with the measured values; S258's bytes are untouched.
- **R80-U6 — `REMINT minted=6 failed=0` was quoted driver stdout with no committed receipt.** It is
  not a receipt: the six durable artifacts are `corpus/evidence/round80/cancel-async-tasks-probe.txt`,
  `chess-best-move-probe.txt`, `distribution-search-probe.txt`, `largest-eigenval-probe.txt`,
  `openssl-selfsigned-cert-probe.txt` and `protein-assembly-probe.txt`, each carrying its own stamp and
  observation block. The round-80 lesson row in `corpus/README.md` now names both `M80-1` and `M80-2`
  (it named only `M80-1`).

## Limits

- The two replays stage lane-authored end states; they record how the captured graders answer
  constructed files and say nothing about any agent, model or submission. The task images are never
  pulled and no network is used inside the sandbox.
- The `HOST_PYTHON`/`HOST_OPENSSL` pin is a capture-time fact: a later replay on a different
  interpreter is a different measurement and the gate says so rather than silently comparing.
- `considerthese/2026-10-26.md` proposal 3 (batch sweep + class histogram) is mined as QUALITY Q59:
  the sweep is a freshness instrument with a mandatory flake-rate rider, never a coverage claim; the
  sweep itself is round-82 work.
- The gate proves the receipt's block is what the *named* instrument prints at the tree; it cannot
  prove the instrument computed rather than printed. That gap is closed by reading the 120-line
  instruments (they import the capture from `/cap/test_outputs.py` and call its test functions) and
  by the `TOOL_SHA` pin, not by the counter — named here so no later reader mistakes the counter for
  a proof of execution.
- One scratch clone under `/fast/scratch/hyaku/kengaku-r81/ctl` was committed with a throwaway
  identity to freeze the control state before measuring it; the commit never left the scratch tree
  and touched neither the lane nor the fleet. Named because the round's own rules forbid throwaway
  identities outside fixture repos.
- Wave findings that stay open, each with its disposition in
  `corpus/evidence/round81/w1-findings.txt`: the `COMMAND` stamp is substring-validated (F2), the
  universe reads captures from the checked tree rather than `BASE_REV` (F3), the stdlib-import test
  is vacuously true for a zero-import capture (F4), the mint driver's post-probe guard is an OR and
  its writes are not all-or-nothing (S1/S2). None of them changes this round's data; all are
  round-82 work. The critic adds four more of the same class (tool provenance binds to the measured
  tree, the environment pin is a version string, the C2 close resolver's commit branch checks
  ancestry only, and the sensitivity leg reverts one file rather than a base checkout) — recorded in
  the same file.
- `container-image` stays at `executed 0 of 0` (no member exists in the census) and 62 members stay
  `unexecuted`; the population gate's `covered=15` of 16 classes is the honest state.
