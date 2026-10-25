# P2a — `## Capabilities` rows (3) re-run at base `6180e4f`

Read-only. Sandbox `/tmp/k25-cap` = `git -C <lane> archive 6180e4f | tar -x -C /tmp/k25-cap` (base hash observed `6180e4fb92e90c0b172e9788e2c765d097f2e142`, extract exit 0); all runs `cwd=/tmp/k25-cap`. Population `SCORECARD.md:555-557` (`rows_in_section=3`); lane tree unchanged (`git diff --stat 6180e4f` over SCORECARD.md/SOURCES.md/gate.md → empty).

## Row 1 — `offline-replay-gate` (`:555`)
`python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1` MATCH (identical at `PYTHONHASHSEED=1,99`); `VERDICT: PASS` MATCH (observed `VERDICT: PASS — stored evidence fully re-derives offline`); exit 0 MATCH. **3/3 MATCH.**

## Row 2 — `frozen-table-pin-check` (`:556`)
`python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` → `FREEZE-CHECK: reads=1 block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK`, exit 0. Tokens `block_sha=1b2d6a01bfa431ec` MATCH, `pinned=1b2d6a01bfa431ec` MATCH, `stable=True -> OK` MATCH, exit 0 MATCH. **4/4 MATCH** (extra unclaimed token `reads=1`).

## Row 3 — `sources-registry` (`:557`)
Cell names no single command: `corpus/SOURCES.md` + "the SOURCES contract v1 census"; commands verbatim from `CORPUS.md:130-148`, plus `scripts/sources-census.sh validate /tmp/k25-cap`.

| expected token | observed | verdict |
|---|---|---|
| `rows 25` | `26` | **MISMATCH** |
| `malformed 0` | `0` | MATCH |
| `A=24` | `A=24` | MATCH |
| `C=1` | `C=2` | **MISMATCH** |
| `mined=18` | `mined=18` | MATCH |
| `queued=5` | `queued=5` | MATCH |
| `rejected=2` | `rejected=3` | **MISMATCH** |
| dup-id check prints nothing | empty | MATCH |
| enum/tier-inflation prints nothing | empty | MATCH |
| mined used-by missing prints nothing | empty | MATCH |
| `sources-census.sh validate` clean | `k25-cap<TAB>ok<TAB>/tmp/k25-cap/.../SOURCES.md`, exit 0 | MATCH |

**8/11 MATCH, 3 MISMATCH.** Receipt `corpus/evidence/round24-sources/gate.md` exists but is self-inconsistent: 26 evidence rows (`:34` = S026) vs census block `:98-101` (`rows: 25`, `tiers: A=24 C=1`, `statuses: mined=18 queued=5 rejected=2`).

## Findings
1. Root cause: `e21f9ea` ("round-24: post-review fixes", 19:39:16) appended S026 (tier C, rejected, `supersedes S023`) to `corpus/SOURCES.md:48` and `gate.md:34` after `94da19e` (19:22:56) landed the row on the 19:22:20 census. Per-commit census: `94da19e` = 25 / `A=24 C=1` / `mined=18 queued=5 rejected=2`; `e21f9ea` and `6180e4f` = 26 / `A=24 C=2` / `mined=18 queued=5 rejected=3`.
2. The registry follows the contract (SOURCES-CONTRACT-v1 rule 2: a correction is a new append-only `supersedes` row; the frozen census counts every `| S###` row), so 26 is rules-consistent; the SCORECARD cell and its receipts are stale.
3. Stale values also sit in `corpus/evidence/round24-census/after.txt:17,29,31,32`. Base `sha256(corpus/SOURCES.md)` = `fb57569835c4f1c6a55decbf4a36b5f6dac8f6c3d3b2a961d3dfba4f48cf5cc5`.
4. For `plans/state_check.py`: rows 1-2 carry one backticked command, row 3 does not, so the checker needs an explicit row→(commands, label→token) table. Compare per command, never substring-scrape a receipt — `gate.md`'s stale block would wrongly PASS all three.
5. Commands are cwd-bound: `plans/attrib-r23-frozen.md` resolves against cwd (`FileNotFoundError`, exit 1, from `/tmp`), so `state_check.py` must chdir to `--root` before each row.
6. P2a contributes 3 base mismatches (one row), not 0; closure needs an appended correction (SCORECARD errata + fresh census receipt), never a rewrite of `gate.md`/`after.txt`; `malformed 0`, `A=24`, `mined=18`, `queued=5` stand as-is.

Counts: 18 expected tokens → 15 MATCH / 3 MISMATCH. No installs, no network, no writes outside this report; scratch and stdout captures under `/tmp`.

VERDICT: rows 1-2 reproduce exactly (7/7 tokens); row 3 fails 3/11 at base — `rows 25` (26), `C=1` (C=2), `rejected=2` (3) — because S026 landed after the capability row and its receipts.
