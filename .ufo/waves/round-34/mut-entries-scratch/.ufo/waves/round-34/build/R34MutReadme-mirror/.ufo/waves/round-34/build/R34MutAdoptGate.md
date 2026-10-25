# R34MutAdoptGate — mutation test of the source-adoption gate against the drafted TB2 rows

**Seat:** mutation-tester. **Axis:** build + attack. **Lane:** kengaku-shokunin, round 34 (hyaku run 7, 2026-10-25). Freeze: `plans/round-34-claims.md` @ `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`.

**Object under test:** `plans/sources_adopt.py` (the adoption gate; exit map: 0 ok, 2 unreadable/arg, 3 collision, 4 malformed, 5 request/missing, 6 overlong quote, 7 absent quote, 8 url-mismatch, 9 unmapped).

**Fixture basis:** the *drafted append-rows*. `build/R34RowsTB2/append-rows.md` exists (S105/S106/S107). `build/R34RowsQuarantine/append-rows.md` does **not** exist — the R34RowsQuarantine seat explicitly declined to draft it (`build/R34RowsQuarantine.md:12`: S108's quote not locatable in capture; verdict `rows-quarantine-not-drafted`). No quarantine draft was copied; no substitution was fabricated. Mutants were applied to the TB2 draft (the only drafted append-rows), in its gate-consumable table form (11 cells, matching `corpus/SOURCES.md` and the selftest `GOOD_ROW` shape) with the landed quotes from `build/R34RowsTB2/quotes.json` placed in the anchor cell (col 5). Artifact = captured pinned bytes (`assimilation/captures/tb2-eval/`, mirrored read-only to scratch); url-map = the drafted `build/R34RowsTB2/url-map.json` (or a wrong-document variant for M3).

**Scratch:** `/tmp/r34-mutadoptgate/` (outside the lane; lane files untouched — no lane byte was modified, so nothing required restoring). All command outputs below are captured verbatim.

## 1. Baseline (pristine gate)

Command:
```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py --selftest
```
Output tail: `SELFTEST cases=17 failed=0`; `EXIT=0`.

## 2. Pristine runs on the drafted rows (no mutation)

**Registry mode, unscoped** — command:
```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py \
  --registry /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md \
  --package /tmp/r34-mutadoptgate/rows/rows-base.md \
  --admit-ids S105,S106,S107 --entries corpus/knowledge/terminal-bench-task-grader.md \
  --access-date 2026-10-25
```
Output: `registry=97 staged=3 collisions=0 malformed=0 duplicates=0 defects=3 prose=3` + `defect S105/S106/S107: recheck-prose`; `EXIT=4`.

**Registry mode, scoped (the admission branch)** — same + `--scope-to-admit`: prints `normalized recheck S105/S106/S107: annual`, emits the append block with recheck rewritten to `180d`; `EXIT=0`.

**Quote mode, artifact = lane-root mirror, drafted map** — `EXIT=0`, `located=3 found=3 mismatch=0 unmapped=0`, all three rows bound (`S105->…test_outputs.py`, `S106->…test.sh`, `S107->…antibody.fasta`).

**Quote mode, artifact = the capture directory itself, same drafted map** — `EXIT=9`, `unmapped=3` (all three REFUSED). This is a genuine integration hazard: `build/R34RowsTB2/url-map.json` keys are lane-root-relative (`assimilation/captures/tb2-eval/<file>`), but `load_artifact` names a directory artifact's files by basename (`sources_adopt.py:323`); an `--artifact` pointing at the capture dir makes every row read unmapped (exit 9) — the C1 kill rule would then refuse all three cited rows.

**Bare draft as copied (`pkg/bare-draft.md` = verbatim `build/R34RowsTB2/append-rows.md`)** — rows lack the leading/trailing `|`; `ROW_RE` (`sources_adopt.py:43`) never matches them: `registry=97 staged=0 ( missing: S105 S106 S107`; `EXIT=5`. The drafted append-block is not gate-consumable in its as-copied form.

## 3. Mutants — expected vs actual

Fixture hashes (sha256): rows-base = m3-wrongmap = `a8c61abcc04fa6af754c7da215f3301258f0d8d6695aa1c58246ac0d32a57802`; m1-overlong `0c45c5670fa44cc9df6aa644d34da87895d6c4df4fbc65224ddd045294db0a03`; m2-absent `6903d1d9b27b9261e0fbb615e31e9fbec07dc29c2b293edda70d4072e3411582`; m4-escaped-pipe `e1cfc003a3c89901afbc669a15b4f19f4ca6c12b59619c2cc43911256753ce8e`; m5-fourspace-indent `274a9f704409a6e9a36b0c19bc1e3cc4e6dfa6e982d8248cf27973c08ad12ef8`; map drafted `da9702f9d5a8b7e02423fe1bceba50a3c55192250d466fd141e5f19a2b9cc9c9`; map wrong `b44a53396aa7309e31c2d8ae4098c00d3da35746a6305ab8f67e4f517563f5b3`.

| # | Mutant (applied to one row; others pristine) | Expected exit | Actual exit | Gate verdict |
|---|---|---|---|---|
| M1 | Overlong quote: S105 anchor quote = 26 words (`python3 -c` verified `OVERLONG_WORDS=26`) | 6 | 6 | **Killed** — `REFUSED S105 overlong words=26 cap=25 at nowhere`; refused by length even though absent (selftest case 11 pins this precedence) |
| M2 | Absent-from-artifact quote: S105 anchor = `"the verifier shares the agent's container unless a task opts out"`; `grep -rl` across all captures → `ABSENT_PHRASE_NOT_IN_CAPTURES` | 7 | 7 | **Killed** — `REFUSED S105 absent words=11` |
| M3 | Quote bound to wrong document: located in `test_outputs.py` but `url-map-wrong.json` maps that artifact to `test.sh`'s URL | 8 | 8 | **Killed** — `REFUSED S105 url-mismatch words=10 at …test_outputs.py`; `found=3` proves the bytes were located, refusal is the citation |
| M4 | Escaped `\|` inside a cell (S106 teaches cell). `split_cells` returns `None,"escaped-pipe"` (`sources_adopt.py:84-85`) | rejection (4) | 4 | **Killed** — `malformed=1`, `malformed: S106:escaped-pipe` in registry scoped mode too; quote mode `rows=2` (row excluded) |
| M5 | Stray leading-space indentation (>3 spaces): S105 line prefixed with 4 spaces (`ROW_RE` anchor is 0–3 spaces, `sources_adopt.py:43`) | none specified (probe) | 0 | **SLIP** — quote mode `rows=2`, S105 absent from the report, exit 0 green; sole-row variant: quote mode `rows=0 located=0` exit 0 green |

Registry-mode cross-check for M1/M2/M3 (scoped): exit 0 — the registry check does not inspect quotes (expected; the quote surface is the `--quote-file/--artifact/--url-map` mode). M4 scoped registry: exit 4. M5 scoped registry: exit 5 (`missing: S105`) — caught *indirectly* as a missing requested id only when `--admit-ids` names it; with no admit-ids (or sole-row) it is a silent green.

## 4. Verdict

Killed 4/5. **Gap:** a row with >3 leading spaces is outside the gate's row anchor and is silently dropped — never refused — in quote mode (exit 0, `rows` fewer than the file's rows); in registry mode it surfaces only as a "missing" requested id when the caller explicitly lists it. The selftest *pins* this as intended behavior (case 4 `four-space-not-a-row`, `sources_adopt.py:658-665`), so this is a coverage finding, not a gate permission change: the L1 should either (a) have the append step refuse any staged row that fails `ROW_RE` (make >3-space or unpipeable lines a malformed row), or (b) rely on the post-append C1 counter (V3 row presence) to catch the dropped row — currently the round-34 C1 counter's V3 check (`checks=8`) is the only downstream net.

Secondary findings for the L1 (not mutants, but gate-integration gaps surfaced by the same runs):
1. Drafted url-map keys mismatch `load_artifact` naming if `--artifact` is the capture dir → all rows unmapped (exit 9). Use lane-root-relative artifact paths (as mirrored) or basename keys.
2. Drafted rows carry `annual` recheck → unscoped registry gate refuses (exit 4, `recheck-prose`); the admission must be run with `--scope-to-admit` (which normalizes `annual`→`180d`).
3. `build/R34RowsTB2/append-rows.md` as copied is not parseable by the gate (staged=0, exit 5 missing ids); the integration must feed table-form rows.

No tool installed or updated (none needed). No lane file was modified or restored (scratch only). Baseline receipt: `SELFTEST cases=17 failed=0`, exit 0.

VERDICT: mut-adoptgate (killed 4/5; gap list: M5 >3-space indent row invisible/silent-green in quote mode; drafted url-map key naming; `annual` recheck prose refusal unscoped; bare draft unparsable)
