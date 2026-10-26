# F42MutC2V9 — mutation test of C2 counter V9 (`plans/round42_c2_verify.py`)

Scope: `v9()` and the module-level regexes it reads, at the freeze the wave was cut on. Counter bytes
= clone of `508434ad55c709337065611691c426f05875492d`, `plans/round42_c2_verify.py` sha256
`270097fdf1d25ee86cced105c731eb5eb4cb73baff6cc547710a8cf5961cf2c7`, restored byte-identical after
every mutant (`git -C $S/lane status --porcelain -- plans/round42_c2_verify.py` → clean).
16 single-line mutants over the six axes named in the tasking (CASE_ROW, receipt regex, the
equality, the `source:` exclusion, PROVINCE and README checks).

Probes per mutant (all bwrap-wrapped, envelope below):
1. **filler-control** — `claims/c2_filler_control.py --lane <clone> --work <scratch>`. The control is
   tracked at `508434ad` (`git ls-files --error-unmatch` ok), so it is reproduced in the clone as
   committed; no copy was needed. Pristine baseline: `CONTROL filler V9 DEFECT` (4 bad items),
   `CONTROL content V9 ok case_rows=16/16`, `CONTROL-C2-FILLER red-as-required`, rc=0.
2. **tip-v9** — `v9()` on a detached worktree of the landing `ff14d76d32d662f7b7073a2acb049594cb740d84`
   (`git rev-parse --show-toplevel` verified). Pristine baseline: `TIP-V9 ok=True case_rows=16/16 bad=0`.
   Sanity: `v9` on the clone itself (`508434ad`) is identical (`ok=True case_rows=16/16`) — the docs
   commit changes no V9 input.

Survivors were re-run against **drafted killer mirrors** (one-axis variants of the control's content
mirror), and the draft was executed, not just specified. Campaign run twice; verdict tables
byte-identical (`diff` of run-A vs run-B BASELINE/MUTANT/SUMMARY lines → empty).

## Table (filler/content/tip = v9 says ok on that probe)

| # | mutant | axis (single-line change) | filler | content | tip | verdict | caught-by / killer control (executed) |
|---|--------|---------------------------|--------|---------|-----|---------|--------------------------------------|
| 1 | CR-upper | CASE_ROW id `[a-z0-9-]+`→`[a-zA-Z0-9-]+` | F | T | T | SURVIVED | killer `id-upper` (ids uppercased in receipt+entry): pristine DEFECT → mutant ok |
| 2 | CR-tests-plus | CASE_ROW tests `[PF]{3}`→`[PF]+` | F | T | T | SURVIVED | killer `tests-long` (extra row, 4-letter tests): pristine ok → mutant DEFECT |
| 3 | CR-verdict-error | CASE_ROW verdict `+ "\|error"` | F | T | T | SURVIVED | killer `verdict-error` (extra row, verdict `error`): pristine ok → mutant DEFECT |
| 4 | CR-verdict-pass-only | CASE_ROW verdict →`(pass)` | F | F | F | CAUGHT | content-control + tip-v9 (`case_rows=7/16`) |
| 5 | RX-id-word | receipt id `\S+`→`\w+` | F | F | F | CAUGHT | content-control + tip-v9 (`case_rows=16/1`; ids contain `-`) |
| 6 | RX-case-prefix | receipt literal `^CASE`→`^CASX` | F | F | F | CAUGHT | content-control + tip-v9 (`case_rows=16/0`) |
| 7 | RX-obs-narrow | receipt observed `(pass\|fail)`→`(pass)` | F | F | F | CAUGHT | content-control + tip-v9 (`case_rows=16/7`) |
| 8 | RX-swap | want tuple `(1,3,2)`→`(1,2,3)` | F | F | F | CAUGHT | content-control + tip-v9 (`16/16 equal=False`) |
| 9 | EQ-drop-compare | `elif not want or got != want:`→`elif not want:` | F | T | T | SURVIVED | killer `eq-flip` (one entry verdict flipped): pristine DEFECT → mutant ok |
| 10 | SRC-exclusion-off | `if not l.startswith("source:")`→`if True` | F | T | T | SURVIVED | killer `src-only` (sids only in `source:` lines): pristine DEFECT → mutant ok |
| 11 | PR-name-off | drop `and name in l` conjunct | F | T | T | SURVIVED | killer `province-nameless` (task w/o entry filename): pristine DEFECT → mutant ok |
| 12 | PR-and-to-or | PROVINCE `and`→`or` | F | T | T | SURVIVED | killer `province-nameless`: pristine DEFECT → mutant ok |
| 13 | TASK-swap | `TASK = "circuit-fibsqt"` | F | F | F | CAUGHT | content-control + tip-v9 (PROVINCE + README bad) |
| 14 | TASK-prefix | `TASK = "circuit-fibsqr"` | F | T | T | SURVIVED (equivalent-in-practice) | no honest control kills it — see F6 |
| 15 | RM-task-off | drop `or TASK not in fr.group(1)` | F | T | T | SURVIVED | killer `readme-taskless` (§Frontier w/o task): pristine DEFECT → mutant ok |
| 16 | RM-frontier-case | `^## Frontier`→`^## frontier` | F | F | F | CAUGHT | content-control + tip-v9 |

**Caught 7/16.** 8 survivors killed by their drafted controls; 1 equivalent-in-practice.

## Findings

- **F1 (headline) — V9's core equality is never negatively exercised by the frozen control.**
  Mutant 9 deletes `got != want` outright and survives filler-control, content-control and the
  landed tip: the filler arm defects on "no '## Case table' section" (it has no table at all), while
  the content arm and the tip are row-equal. A regression that silently disables the comparison
  passes `control-c2-filler.txt` and the landing measurement. Executed control: `eq-flip` mirror
  (content mirror, one entry verdict `fail`→`pass`, receipt unchanged) → pristine
  `KILLER eq-flip ok=False ... equal=False`, mutant `ok=True`. Recommend the L1 add an eq-flip arm
  to `claims/c2_filler_control.py`.
- **F2 — pristine V9 silently ignores non-conforming rows inside `## Case table`.** Killer
  baselines on pristine bytes: `KILLER tests-long ok=True`, `KILLER verdict-error ok=True` — an
  entry may carry an extra row with a 4-letter tests cell or a verdict `error` and V9 passes, because
  non-matching lines are skipped rather than flagged. Mutants 2/3 survive for the same reason
  (relaxation only makes ignored rows visible). Same drafted controls kill them.
- **F3 — the `source:` exclusion is only positively exercised.** Both honest mirrors and the landed
  entry name S125–S127 outside `source:` lines, so disabling the exclusion survives (mutant 10).
  `src-only` control (sids only in `source:` lines, table present) kills it.
- **F4 — PROVINCE conjunction untested.** Both relaxations (mutants 11, 12) survive; one
  `province-nameless` control kills both.
- **F5 — README §Frontier task check untested.** Mutant 15 survives; `readme-taskless` control kills it.
- **F6 — equivalent-in-practice mutant.** `TASK in l` is substring containment, so any truncation
  keeping a prefix of `circuit-fibsqrt` matches every honest line (mutant 14 survives; no honest
  mirror kills it). A non-prefix typo (mutant 13) is caught. Property of substring checks, not a
  control gap.
- **F7 (harness hazard for future counter attacks) — stale `__pycache__`.** Importing the counter
  from a writable path validates pyc by (mtime-second, size): same-length edits in the same second
  served the *previous* mutant's bytecode (first run: RX-case-prefix reported `receipt cases=1` —
  RX-id-word's result; a rerun baseline inherited RM-frontier-case's behavior). Fix applied and
  verified: purge `plans/__pycache__` before every import + `PYTHONDONTWRITEBYTECODE=1`; runs A/B
  then identical. The landed measurement is unaffected (the lane counter is read-only at HEAD);
  this bites anyone who edits a counter in place and imports it.
- **F8 — no-harm.** Every control/tip/killer run inside the mandated envelope; `~/.local/bin`
  listing sha unchanged across my campaign bracket.

## Receipt

- Envelope for every run: `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>`
- `date +%T` / `ls -A /home/vgpnk/.local/bin | sha256sum`: 18:04:33 `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`; campaign bracket 18:21:28→18:21:31 `77408cab9a10361a9f6025bab21f5f07933d94ce46e6a10b9117805d58811c11` before == after; 18:21:48 `8cf5b151…` again. The listing changed between snapshots — concurrent host activity by other seats, outside my sandbox (my runs had that path read-only).
- Per-run timestamps, rc, outputs, mutant-by-mutant results: `.ufo/waves/round-42/falsify/F42MutC2V9/receipt-mutc2v9.json` (full JSON, < 1 MiB).
- Counter restoration: final sha256 `270097fdf1d25ee8…` == pristine; `git status --porcelain -- plans/round42_c2_verify.py` → clean.
- Determinism: run A vs run B verdict tables identical (diff empty).
- Scratch: `/fast/scratch/hyaku/kengaku-r42/F42MutC2V9` (clone at `508434ad`, detached worktree at `ff14d76d`), removed after this report.

VERDICT: v9-mutants-caught-7/16
