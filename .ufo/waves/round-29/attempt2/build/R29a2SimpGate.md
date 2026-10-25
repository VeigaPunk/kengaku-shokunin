# R29a2SimpGate — YAGNI pass on `plans/sources_adopt.py`

Seat: simplifier. Findings only — no production edits, no integration, no round judgement.
Every claim below is backed by a command + exit code, or by `coverage` measuring the two
mandated scenarios. Nothing here is "looks dead".

## 0. Revisions pinned (read this first)

The working tree changed **while this audit was running**, so line numbers are given against
both revisions:

| tag | what | sha256 | lines |
|---|---|---|---|
| **HEAD** | `git show 8c14a5d:plans/sources_adopt.py` — the committed C2 artifact | `88535ca2bd039fe36a169fbbac3d396eba0285df7d57cbb3a34b6242823e124b` | 367 |
| **WT** | working tree, mtime `2026-10-25 03:44:59 -0300`, stable for the rest of the run | `505478fd0b09c68b0112c7334328a9d07060a4783784dc417093749a56bdffc0f` | 401 |

`git status --porcelain` → ` M plans/sources_adopt.py`. This modification is **not mine**; I
wrote nothing inside the lane except this report (see §9). WT is HEAD + 47/−13 and changes three
things that matter here: `check()` becomes *scoped* to `want_ids`, `print_report` gains `prose=`,
and selftest case 9 is rewritten. Where a verdict differs between the two, the table says so.

## 1. Scenario (b) was reconstructed, and is byte-identical to the receipt

The prior receipt records only output, not the invocation. The invocation that reproduces it
exactly is:

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
git show 8c14a5d:corpus/SOURCES.md > /tmp/.../registry-8c14a5d.md      # 76 rows
python3 plans/sources_adopt.py \
  --registry /tmp/.../registry-8c14a5d.md \
  --package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
# exit=4
```

`diff <(sed -n 1,173p run.out) <(sed -n 1,173p .ufo/waves/round-29/attempt2/package-gate.txt)`
→ no output, **IDENTICAL_HEAD**. Package sha256 `a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b`
(181 lines, 173 anchor rows + 2 malformed). So the receipt **is** HEAD's bytes on the frozen
registry, with `--admit-ids` absent — i.e. it is a **check-only refusal receipt**, which is why it
never touches `build_block` (see §4, the main operability finding).

Registry drift to note (not a defect, an observation): the live registry is now 81 rows, because
C1's five rows (S077 S078 S079 S080 S090) landed after the receipt. Re-running the same command
against the live registry now prints
`registry=81 staged=173 collisions=5 … collisions: S077 S078 S079 S080 S090`, **exit=3** — the
gate's first *real* non-empty collision set, and correct: the package rows are now already adopted.
The receipt is a frozen-moment artifact and must not be re-run against the live tree.

## 2. Coverage, measured (not asserted)

`coverage.py 7.16.2` (already installed at `~/.local/bin/coverage`; I installed/upgraded nothing),
`--branch`, scenario (a) `--selftest` and scenario (b) above, combined:

| revision | stmts | miss | branch | partial | cover | missing |
|---|---|---|---|---|---|---|
| HEAD | 221 | 25 | 62 | 13 | 84% | `73, 76, 105, 110, 142, 150->153, 189->192, 212->215, 216, 323-324, 341, 347-363, 366->exit` |
| WT | 236 | 25 | 68 | 12 | 85% | `73, 76, 105, 110, 142, 150->153, 239->242, 243, 357-358, 375, 381-397, 400->exit` |

Per-function, which scenario reaches what:

- `split_cells`, `parse_rows`, `row_defects`, `ids`, `collisions`, `duplicate_ids`, `collect`,
  `check` — reached by **both**.
- `build_block` — reached **only** by (a) (selftest calls it directly). (b) never gets past
  `check`'s refusal at HEAD `184-186`.
- `print_report` — reached **only** by (b). (a) never calls it (`check` is called directly).
- `selftest` — (a) only, trivially. `main` — both, but (a) only ever executes `--selftest` arm
  (HEAD `338-339` / WT `372-373`).

No function is unexercised by *both* scenarios. The dead weight is at branch/field level, below.

## 3. Table — candidates, unreachability, verdict

`(a)` = selftest, `(b)` = the real package run. "—" = not reached by that scenario.

| # | item | HEAD line | WT line | (a) | (b) | why unreachable / dead | verdict | proof |
|---|---|---|---|---|---|---|---|---|
| T1 | `Row.line_no` (slot + assignment) | 47, 50 | 47, 50 | — | — | written only; no reader anywhere (`grep '\.line_no'` → only `self.line_no =`) | **DELETE** | — |
| T2 | `Row.indent` + `ROW_RE` capture group 1 that only feeds it | 33, 47, 51, 97 | same | — | — | written only; `match.group(1)` is read at 97 solely to pass to `indent` | **DELETE** | mutant M2 (below) |
| T3 | `Row.raw` | 47, 54 | same | — | — | written only | **DELETE** | mutant M2 |
| T4 | `cells[8] = access_date if not ISO_DATE_RE.match(cells[8]) else cells[8]` | 153 | 153 (already `= access_date`) | else-arm only | — | the normalise arm never runs in (a) or (b); the else-arm *retains* a non-frozen `opened`, which CORPUS rule 1 forbids | **DELETE arm** (WT already did) | §5-C |
| T5 | `parse_rows(*, anchor=True)` switch + its docstring justification | 80, 83-84, 86 | same | — | — | **no caller anywhere in the repo passes it**; the ternary's right operand never evaluates; the docstring's claim "the selftest can prove the narrow anchor is load-bearing" is false — case 4 proves it through `check()` with the default | **DELETE** (param, ternary, docstring lines 83-84) | mutant M1 + `grep -rn "import sources_adopt\|sources_adopt\." --include=*.py .` → no hits, exit 1 |
| T6 | `build_block` missing machinery: `missing` list, `if missing: return [], [], missing`, third tuple element; and `main`'s `if missing: print; return EXIT_REQUEST` | 140-142, 157; main 351-354 | 140-142; main 385-388 | — | — | `check()` has already validated the same `want` set against the same bytes; on a miss it returns `EXIT_REQUEST` (HEAD 191 / WT 217) and `main` returns at HEAD 345-346 / WT 379-380 **before** `build_block`. Reachable only if the package is rewritten between `collect`'s read and `main`'s re-read (TOCTOU) — and it duplicates `print_report`'s `missing:` line (HEAD 216 / WT 243), which is the authority that actually fires | **DELETE** (with T6's main block; keeps a single `missing` authority) | mutant M3 |
| T7 | `if bad and not want_ids: …` block | — | 205-207 | — | — | subsumed by 208-210: `bad` ⟹ `malformed` non-empty, and both compute the identical `EXIT_COLLISION if clash else EXIT_MALFORMED` | **DELETE** (4 lines) | 15-scenario A/B, **0 diffs** (§5-A) |
| T8 | `"collisions_total"`, `"duplicates_total"` report keys | — | 180, 181 | — | — | write-only: no reader in the file outside their own definition (`malformed_total` is read by WT case 9 l.347; `prose_recheck_total` by l.231) | **DELETE** | `grep -n "collisions_total\|duplicates_total" work-0345.py` |
| T9 | `prose_recheck_total` recomputing `row_defects` over every staged row + the nested `report.get("prose_recheck", report.get("prose_recheck_total", 0))` | — | 183, 231 | — | — | second computation of a number already derivable from the unfiltered `defects` dict at 175; and the fallback makes `prose=` **change meaning by mode**: same 2-prose-row package prints `prose=2` unscoped, `prose=1` when scoped to one row (§5-D) | **KEEP field, DELETE the recomputation**; make the printed number single-sourced | §5-D |
| T10 | `from __future__ import annotations` | 25 | 25 | — | — | no behaviour on any interpreter ≥ 3.10 (runtime here 3.14.8); every annotation is a PEP 585/604 builtin resolvable at `def` time | **DELETE** (low priority; precondition ≥3.10) | `python3 -V` → 3.14.8 |
| T11 | `split_cells` `return None, "not-a-table-row"` | 72-73 | same | — | — | **not dead** — a row matching the anchor but missing the closing pipe reaches it | **KEEP**; add fixture (no case covers it) | `| S400 | x | … | p.md\n` → `[(3, 'S400', 'not-a-table-row')]` |
| T12 | `split_cells` `return None, f"columns={len(cells)}"` | 75-76 | same | — | — | **not dead** — this *is* capability 2's literal-pipe detector (an unescaped `\|` inside a cell yields 12 cells) | **KEEP**; add fixture | 12-cell row → `[(3, 'S401', 'columns=12')]` |
| T13 | `row_defects` invalid-status defect | 104-105 | same | — | — | **not dead** — a named capability-2 item; a `status=wip` row reaches it | **KEEP**; add fixture | `status=wip` row → `['status=wip']`, CLI exit=4 |
| T14 | `row_defects` `"recheck-empty"` arm of the same conditional | 108 | same | only the prose arm | prose arm only | **not dead** — empty `recheck` reaches it | **KEEP** | empty recheck → `['recheck-empty']` |
| T15 | `row_defects` `source-empty` defect | 109-110 | same | — | — | reachable (empty source cell), but **outside the frozen C2 schema list** (columns / no-pipe / status / recheck) and has no case, so it is an unclaimed extra refusal | **KEEP** (a genuinely unadmittable row) — but either add an 11th case or note it as an unclaimed rule; delete only if strict-contract minimalism is wanted | empty source → `['status=wip','source-empty']`, exit=4 |
| T16 | `check`'s `EXIT_OK`-with-`want_ids` arc | 189->192 | 213-218 | taken only in the `missing` arm (case 10) | — (exits at 186) | **not dead** — this is the gate *accepting* a block | **KEEP** | clean row + `--admit-ids S900` → exit 0 |
| T17 | `print_report`: collisions/duplicates print, the no-defects arc, the `missing:` print | 210, 212->215, 216 | 237, 239->242, 243 | — (never called) | defects arc only | **not dead** — all three reachable | **KEEP** | `missing:` printed on `--admit-ids S999` (exit 5); `collisions: S077 …` printed on the live registry (exit 3); clean run prints no defect lines (exit 0) |
| T18 | selftest failure reporting | 322-324 | 357-358 | — (all pass) | — | reachable only when a case fails — the class the brief says must stay; it is the harness's own refusal | **KEEP** | broken-case mutant M4 → **exit 1**, `SELFTEST cases=10 failed=1`, `failed: duplicate-staged-id` |
| T19 | `main` usage guards (`--registry/--package`, `--access-date`) | 341, 347-348 | 375, 381-382 | — | — | reachable from argv | **KEEP** | no args → exit 2; `--admit-ids` without `--access-date` → exit 2 |
| T20 | `main` adoption tail (`--access-date` read, re-parse, `--entries`, prose print, `--out` / stdout) | 349-363 | 383-397 | — | — | the tool's whole purpose; unreached only because the recorded run is a refusal | **KEEP** | `wrote …/block.md rows=1` (exit 0) and the stdout branch both exercised; block content correct |
| T21 | `if __name__ == "__main__"` →exit arc | 366->exit | 400->exit | — | — | standard entry-point arc; untaken because both runs execute the module as `__main__` | **KEEP** (no action) | coverage artifact only |
| T22 | `build_block` prose block (`prose` list, `if not (valid recheck)`, `prose.append`, `cells[9] = access_date`) | 144, 150-152, 157 | same | direct call only | — | **HEAD: unreachable from `main`** — `check()` refuses `recheck-prose` at 184-186 before `build_block` runs, so capability 3 can never execute through the CLI; **WT fixed this** by scoping `check` to `want_ids` | **KEEP the capability, fix the caller** (WT already does); delete only if the L1 prefers refusal — then claim C2 item 3 must be amended, not quietly dropped | HEAD: prose row + `--admit-ids` → exit 4, no block. WT: exit 0, `normalized recheck S900: …`, block written |
| T23 | `collect`: `registry_rows, _ = parse_rows(registry_text)` discarding registry malformed rows | 163 | same | — | — | **not dead**, but an unreported swallow: a mangled registry row is invisible, so a staged collision with its id false-greens capability 1 | **KEEP + surface the count** (do not delete) | receipt's `malformed=` only ever counts staged rows; `registry=76` cannot be cross-checked |
| T24 | recheck-validity predicate duplicated verbatim at `row_defects` and `build_block` | 107 & 150 | same | both | 107 only | not dead — two authorities for one rule (exactly the seam that let "refuse prose" and "normalise prose" coexist) | **no deletion**; fold into one `recheck_ok(value)` helper | reading |

Flags, same question: `--registry`/`--package` are the only flags (b) uses; `--selftest` is the
only flag (a) uses. **`--admit-ids`, `--entries`, `--access-date`, `--out` were exercised by
neither** — all four are reachable and were demonstrated by out-of-band runs (§5-B). `--entries`
has an unguarded degenerate value: `--admit-ids` without `--entries` emits an **empty** `used-by`
cell and exits 0 (§5-B) — an unguarded output path, not dead code; recommend a refusal.

## 4. The operability finding behind all of this

`package-gate.txt` is a **refusal receipt**: the gate was only ever run in check-only mode, so
(a)+(b) together still leave `main`'s adoption tail at 0% — no recorded evidence that the gate can
*accept* a block. Combined with T22, HEAD's adoption mode could not have accepted the campaign
package either way: 171 of 173 staged rows carry prose `recheck`, which `check()` treats as fatal,
so `build_block`'s normalisation is unreachable through the CLI and the gate refuses every row that
capability 3 promises to normalise. WT removes that contradiction (§5-B demonstrates the fix).

Also worth the L1's attention: T6's deletion removes the only *second* place that reports `missing`,
and `print_report` (HEAD 216 / WT 243) already reports it — so deleting T6 loses no observable
behaviour (M3 proof).

## 5. Proof log

**A. T7 — 15-scenario A/B, original vs 205-207 deleted → 0 diffs**

```
SAME clean/no-want, clean/want, clean/want+entries, dup/no-want, dup/want,
     escaped/no-want, escaped-unrequested, 12cells/no-want, prose/want,
     prose/no-want, status-wip/want, empty-src/no-want, missing-id,
     real-package/no-want, scoped-clash
diffs: 0
```
(`scoped-clash` ⇒ exit 3 establishes WT 211-212 is **live**, so it must stay.)

**B. Adoption mode is reachable and correct (WT)**

```
$ python3 work-0345.py --registry registry-8c14a5d.md --package pkg.md \
    --admit-ids S900 --entries corpus/knowledge/new.md --access-date 2026-10-25
registry=76 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=1
  normalized recheck S900: 2026-10-23 — re-verify at next release
| S900 | … | mined | 2026-10-25 | 2026-10-25 | corpus/knowledge/new.md |        exit=0
$ … --out block2.md  →  wrote …/block2.md rows=1                                 exit=0
$ … --entries omitted →  | … | mined | 2026-10-23 | 180d |  |                    exit=0  ← unguarded
```
HEAD, same inputs with a prose row: `defect S900: recheck-prose`, **exit=4**, no block.

**C. HEAD 153's normalise arm** — a row with `opened = "probe date"` is written out as
`2026-10-25` when `build_block` is called directly; no recorded path ever calls it with a
non-ISO `opened`, and the else-arm would have preserved the stale date.

**D. T9 — one field, two numbers**

```
unscoped:                    registry=76 staged=2 … defects=2 prose=2
scoped to S900 (--admit-ids): registry=76 staged=2 … defects=0 prose=1
```

**E. Mutants** (each is a copy in `/tmp/r29a2-simpgate/`, run against both scenarios)

| mutant | change | selftest | (b) output | verdict |
|---|---|---|---|---|
| M1 `m1-noanchor.py` | `anchor` param + ternary + docstring removed; `pattern = ROW_RE` | `cases=10 failed=0` | identical | behaviour-neutral |
| M2 `m2-slimrow.py` | `line_no`/`indent`/`raw` removed, `ROW_RE` group 1 → `(?: {0,3})`, `group(2)`→`group(1)` | `cases=10 failed=0` | identical, and adoption output identical | behaviour-neutral |
| M3 `m3-nodupmissing.py` | `build_block` returns 2-tuple; `main`'s `if missing` block removed | `cases=10 failed=0` | identical | behaviour-neutral |
| M4 `m4-failingcase.py` | one case's expected constant broken | `cases=10 failed=1`, `failed: duplicate-staged-id`, **exit 1** | — | T18 fires |
| (T7) `mut-noredundant.py` | 205-207 removed | `cases=10 failed=0` | identical | 0/15 diffs |

M2 needed the group renumbering: `ROW_RE`'s capture group 1 exists **only** to feed the dead
`indent` field, so deleting the field also shifts the id group. That coupling is itself the argument
for deleting it.

## 6. Deletion set, if the L1 wants one patch

**HEAD**: T1+T2+T3 (one edit: `Row` slots/ctor + `ROW_RE` + 2 `group()` renumbers), T5 (3 lines +
2 docstring lines), T4 (arm), T6 (3 lines in `build_block`, 4 in `main`, third tuple element), T10.
Net ≈ −18 lines, behaviour-neutral (M1/M2/M3 measured); plus T22's caller fix, which *adds*
reachability rather than removing lines.

**WT additionally**: T7 (4 lines, 0/15 diffs), T8 (2 dict entries), T9's recomputation (1 line).

Not recommended for deletion: T11-T15 (reachable refusals), T16-T20 (reachable acceptance/CLI
surface), T18 (harness refusal), T21, T23, T24.

## 7. What a fixture would need to cover the gaps (advisory, not my call)

Uncovered refusals a fixture *can* reach — one case each: not-a-table-row (T11), `columns=12`
(T12), invalid status (T13), empty recheck (T14), source-empty (T15). Adoption mode needs a
receipt of its own (T20/T22): today nothing in the round's evidence shows the gate emitting a
block. That is a coverage defect in *evidence*, not in code.

## 8. Axis report

- **Weight**: 5 behaviour-neutral deletions proven on HEAD (T1-T3, T5, T6, T10) + 2 on WT
  (T7, T8), one duplicate authority removed (T6), one duplicate computation (T9). No axis harmed:
  M1/M2/M3 and the T7 A/B change no exit code and no output byte across both scenarios.
- **Contract preserved**: all ten selftest cases still pass in every mutant; the frozen receipt
  reproduces byte-identically before and after.
- No production file was touched to reach these conclusions.

## 9. Bounds check

- Scratch only: `/tmp/r29a2-simpgate/` (snapshots, mutants, coverage data, fixtures, outputs).
- Reads outside the lane: `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` (read
  only; no campaign tool run), `git show` on the lane itself.
- The lane working tree already had ` M plans/sources_adopt.py` and untracked C1 artifacts when I
  started; I neither created nor removed any of them. My only write in the lane is this file.
- Tooling: **no install or upgrade.** `coverage.py 7.16.2` was already present at
  `~/.local/bin/coverage` (uv-tool shim); `uv` and `python3 3.14.8` pre-existing. Pacman untouched.
- No subagents, no background jobs retained, no `ask` calls.
