# R34MutRegistry — mutation probe: SOURCES census vs the new rows

**Seat:** R34MutRegistry (mutation-tester, leaf — no subagents, no background jobs).
**Target under test:** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (fleet script, used read-only) in `validate --file` / `census` modes, against a scratch registry = lane `corpus/SOURCES.md` + the drafted append rows. No tool installed or updated (none needed). Writes confined to `.ufo/waves/round-34/build/R34MutRegistry/` (this report, `probe.sh`, `out/`, `mirror/`, `mut/`).

## Scratch registry construction

- `mirror/` = byte copy of lane `corpus/` (23M), plus the drafted rows appended **inside** the `## Registry` table, immediately after the `| S104 |` row (the table ends at `corpus/SOURCES.md:119`; appending at EOF would land after `## Search log`/`## Leads` and be E12, so insertion point matters).
- Drafted append-rows that exist: **S105–S107 only** (`.ufo/waves/round-34/build/R34RowsTB2/append-rows.md`, 11 pipe-delimited fields each, rendered as markdown table rows verbatim). **S108/S109 have no drafted append rows**: the quarantine seat refused S108 (NEC quote absent from the 418-byte Access-Denied capture) and wrote no row payload for S109 (`build/R34RowsQuarantine.md`: "No `append-rows.md` … was written"). The scratch registry therefore contains S105–S107; this is stated, not silently narrowed.
- E11 stand-in: the mirror needs `corpus/knowledge/terminal-bench-task-grader.md` to exist (S105–S107 are `mined` with that `used-by`), so the staged draft `build/R34EntryTB2/entry.md` was copied to that path inside the mirror only. The census reads row bytes, not entry contents; entry admission is C1's counter's business, not this probe.
- Pristine mirror `SOURCES.md` sha256 `53b5f9ec6b13032e74b4d36338186b9674f0c76f95accce0709c6a773c896e1d` (110 lines added=3 rows; hash recorded in `out/pristine.sha256`).

## Baseline (pristine mirror) — must be clean or the probe is void

Command: `scripts/sources-census.sh census --file <mirror>/corpus/SOURCES.md` → `file rows 100`, `tier.A 85 / tier.B 13 / tier.C 2`, `status.mined 84 / queued 8 / rejected 8`, `EXIT=0` (`out/baseline.census.txt`). 100 = 97 registered rows + S105/S106/S107.

Command: `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → exactly the 15 `W04` warnings of the freeze receipt's set (S040…S100), then `file ok <mirror path>`, `EXIT=0` (`out/baseline.validate.txt`). New rows contribute no findings; warnings never change exit status. **Baseline clean, probe valid.**

## Five mutants — expected detector, actual output, verdict

Each mutant = fresh real copy of the mirror corpus with one behavior-bearing point mutated in `SOURCES.md`; `validate --file` per mutant. Probe v1 discarded: mutant files at `mut/*.md` made `--file` resolve E11 paths against the wrong parent (E11 flood = instrumentation artifact); v2 places each mutant at `mut/<name>/corpus/SOURCES.md` so path resolution matches the baseline tree and the only possible delta is the mutation. Per-mutant full outputs in `out/mut-*.txt`, findings-only diffs in `out/mut-*.diff.txt`.

| # | Mutant (smallest point) | Expected | Actual finding line | Exit | Verdict | Mutant sha256 |
|---|---|---|---|---|---|---|
| M1 | drop the scope cell of the S106 row (11→10 fields) | E01 | `file E01 S106 fields=10` | 1 | **killed** | `8acc8321…7431b` |
| M2 | markdown-escaped `\|` inserted inside the S105 teaches cell | E01 (contract counts raw pipes: NF=13) | `file E01 S105 fields=12` | 1 | **killed** | `7ad0d218…785ee` |
| M3 | relabel S106 row id → `S105` (duplicate id) | E03 | `file E03 S105 duplicate id` | 1 | **killed** | `69abb3ac…53802` |
| M4 | S107 kind `dataset`→`community`, tier stays A (kind enum still valid) | E10 | `file E10 S107 community-at-A` | 1 | **killed** | `9278cbda…4be7` |
| M5 | S105 used-by → `corpus/knowledge/terminal-bench-task-grader-MISSING.md` | E11 | `file E11 S105 missing used-by corpus/knowledge/terminal-bench-task-grader-MISSING.md` | 1 | **killed** | `a3952812…347c` |

In every mutant run the 15 `W04` lines are byte-identical to baseline (`diff` shows only the single E line replacing `file ok …`/`EXIT=0` with `EXIT=1`) — no cross-effect, single-fault isolation confirmed.

## Restoration evidence

- After all runs, pristine mirror re-validated: output `cmp`-identical to baseline (`PRISTINE-VALIDATE-IDENTICAL=yes`).
- Bytes re-hashed: `53b5f9ec6b13032e74b4d36338186b9674f0c76f95accce0709c6a773c896e1d` before and after (`PRISTINE-BYTES-RESTORED=yes`; `out/pristine.sha256` == `out/pristine.post.sha256`).
- Lane tree untouched outside this probe dir; census script and `corpus/` only ever read.

## Coverage finding

No survivors: 5/5 killed. Observations (not defects): (a) M2 shows the validator counts raw `|` per the SOURCES-CONTRACT-v1 `NF=13` rule — an escaped pipe is rejected as malformed rather than parsed as a literal, which is the contract's stated behavior; any future row text containing a literal pipe must avoid it, the census will not launder it. (b) E11 is bound to `--file`'s parent-of-parent directory resolution — registries probed via `--file` must sit at `<root>/corpus/SOURCES.md` for used-by checks to mean anything; the freeze receipt's lane-root run (`--root … kengaku`) has the same property by construction.

**VERDICT: mut-registry (killed 5/5, no survivors)**
