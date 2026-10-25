# R29a2SimpGate — YAGNI pass on `plans/sources_adopt.py`

Seat: simplifier. Findings only — no production edits, no integration, no round judgement.
Every claim below is backed by a command + exit code, or by `coverage` measuring the two
mandated scenarios. Nothing here is "looks dead".

## 0. Revisions pinned (read this first)

`plans/sources_adopt.py` changed **three times under me** while this audit ran (R2, R3, R4) — by
other seats, not by me. Every line number below is tagged with the revision it refers to:

| tag | what | sha256 | lines |
|---|---|---|---|
| **R1** | `git show 8c14a5d:plans/sources_adopt.py` — the committed C2 artifact; the receipt's revision | `88535ca2bd039fe36a169fbbac3d396eba0285df7d57cbb3a34b6242823e124b` | 367 |
| **R2** | worktree at 03:44:59 (`check` scoped to `want_ids`; `print_report` gains `prose=`) | `505478fd0b09c68b0112c7334328a9d07060a4783784dc417093749a56bdffc0f` | 401 |
| **R3** | committed at `8cf7b60` | `ab594472b7577a9598cf8da50e1b537d041e42b4233adfe71f9ac39657391c64` | 424 |
| **R4** | worktree when this report was written, **now committed as `4b82ff7`** (== HEAD, worktree clean for this path): `--scope-to-admit` opt-in, `on-commit` cadence, `recheck_default`, `--entries` now required | `73dae3b7f34acfd130fd72dcf6de2373d6a84b03ca7dfae5cdafaf8fefd79269` | 435 |

The main table (§3) carries **R1** and **R2** line numbers, because that is the pair the frozen
claim and the receipt are about. §3b re-states every candidate against **R4**, so the findings
stay actionable on the code that will ship. Several of my findings were fixed by R3/R4 in flight —
§3b marks each as FIXED or LIVE; I am not re-litigating what is already gone.

## 1. Scenario (b) was reconstructed; R4 no longer matches the receipt

The prior receipt records only output, not the invocation or the input hashes. The invocation that
reproduces it exactly **on R1** is:

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
git show 8c14a5d:corpus/SOURCES.md > /tmp/.../registry-8c14a5d.md      # 76 rows
python3 plans/sources_adopt.py \
  --registry /tmp/.../registry-8c14a5d.md \
  --package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
# exit=4
```

`diff <(sed -n 1,173p run.out) <(sed -n 1,173p .ufo/waves/round-29/attempt2/package-gate.txt)`
→ no output (my command echoed `IDENTICAL_HEAD`). So the receipt **is** R1's bytes on the frozen
registry, with `--admit-ids` absent — i.e. it is a **check-only refusal receipt**, which is why it
never touches `build_block` (see §4, the main operability finding).

Registry drift to note (not a defect, an observation): the live registry is now 81 rows, because
C1's five rows (S077 S078 S079 S080 S090) landed after the receipt. Re-running the same command
against the live registry now prints
`registry=81 staged=173 collisions=5 … collisions: S077 S078 S079 S080 S090`, **exit=3** — the
gate's first *real* non-empty collision set, and correct: the package rows are now already adopted.
The receipt is a frozen-moment artifact and must not be re-run against the live tree.

**The shipped gate no longer produces the receipt's output.** R4 adds `on-commit` to
`SYMBOLIC_CADENCE` (R4:36), which four package rows use (S132 S133 S134 S143, `recheck = on-commit`),
so the same command on R4 prints `… defects=167 prose=167` against the receipt's `defects=171`, and
four `defect S…: recheck-prose` lines disappear. That widening is *correct* — those four rows would
otherwise be refused — but it means **`package-gate.txt` no longer describes the gate that would
ship, and no receipt was regenerated after R3/R4.** The receipt also never records `--package` /
`--registry` paths or their hashes, so it cannot be re-derived without guessing (I had to search the
sibling tree for the 173-row package). Two cheap fixes for the L1: put the invocation + input shas in
the receipt header, and re-record it after the tool stops moving.

Package sha256 `a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b`
(181 lines, 173 anchor rows + 2 malformed), mtime `2026-10-24 23:33:20` — unchanged throughout this
audit, so the drift above is entirely the tool's, not the input's.

## 2. Coverage, measured (not asserted)

`coverage.py` (`--branch`), scenario (a) `--selftest` and scenario (b) above, combined:

| revision | stmts | miss | branch | partial | cover | missing |
|---|---|---|---|---|---|---|
| R1 | 221 | 25 | 62 | 13 | 84% | `73, 76, 105, 110, 142, 150->153, 189->192, 212->215, 216, 323-324, 341, 347-363, 366->exit` |
| R2 | 236 | 25 | 68 | 12 | 85% | `73, 76, 105, 110, 142, 150->153, 239->242, 243, 357-358, 375, 381-397, 400->exit` |
| R4 | 248 | 26 | 70 | 10 | 86% | `73, 105, 110, 143, 245->248, 249, 391-392, 419, 425-443, 446->exit` |

R4 closed two gaps in flight: `columns=12` (R1:76) is now exercised by selftest case 5
(R4:312-320), and the *scoped* `check` path is exercised directly (R4:326, 371) — though `main`'s
own tail still is not. Still open at R4: `not-a-table-row` (73), status (105), `source-empty` (110),
the `missing:` printer (249), the duplicate-missing return (143), and every `main` path after
`print_report` (425-443).

Per-function, which scenario reaches what:

- `split_cells`, `parse_rows`, `row_defects`, `ids`, `collisions`, `duplicate_ids`, `collect`,
  `check` — reached by **both**.
- `build_block` — reached **only** by (a) (selftest calls it directly). (b) never gets past
  `check`'s refusal at R1 `184-186`.
- `print_report` — reached **only** by (b). (a) never calls it (`check` is called directly).
- `selftest` — (a) only, trivially. `main` — both, but (a) only ever executes `--selftest` arm
  (R1 `338-339` / R2 `372-373` / R4 `416-417`).

No function is unexercised by *both* scenarios. The dead weight is at branch/field level, below.

## 3. Table — candidates, unreachability, verdict

`(a)` = selftest, `(b)` = the real package run. "—" = not reached by that scenario.
In the two line columns below, **`HEAD` = R1** and **`WT` = R2** (§0).

| # | item | HEAD line | WT line | (a) | (b) | why unreachable / dead | verdict | proof |
|---|---|---|---|---|---|---|---|---|
| T1 | `Row.line_no` (slot + assignment) | 47, 50 | 47, 50 | — | — | written only; no reader anywhere (`grep '\.line_no'` → only `self.line_no =`) | **DELETE** | — |
| T2 | `Row.indent` + `ROW_RE` capture group 1 that only feeds it | 33, 47, 51, 97 | same | — | — | written only; `match.group(1)` is read at 97 solely to pass to `indent` | **DELETE** | mutant M2 (below) |
| T3 | `Row.raw` | 47, 54 | same | — | — | written only | **DELETE** | mutant M2 |
| T4 | `cells[8] = access_date if not ISO_DATE_RE.match(cells[8]) else cells[8]` | 153 | 153 (already `= access_date`) | else-arm only | — | the normalise arm never runs in (a) or (b); the else-arm *retains* a non-frozen `opened`, which CORPUS rule 1 forbids | **DELETE arm** (WT already did) | §5-C |
| T5 | `parse_rows(*, anchor=True)` switch + its docstring justification | 80, 83-84, 86 | same | — | — | **no caller anywhere in the repo passes it**; the ternary's right operand never evaluates; the docstring's claim "the selftest can prove the narrow anchor is load-bearing" is false — case 4 proves it through `check()` with the default | **DELETE** (param, ternary, docstring lines 83-84) | mutant M1 + `grep -rn "import sources_adopt\|sources_adopt\." --include=*.py .` → no hits, exit 1 |
| T6 | `build_block` missing machinery: `missing` list, `if missing: return [], [], missing`, third tuple element; and `main`'s `if missing: print; return EXIT_REQUEST` | 140-142, 157; main 351-354 | 140-142; main 385-388 | case 6/7 **unpack** the third element and assert it is empty (`not missing`) — the value is always `[]` there | — | `check()` has already validated the same `want` set against the same bytes; on a miss it returns `EXIT_REQUEST` (HEAD 191 / WT 217) and `main` returns at HEAD 345-346 / WT 379-380 **before** `build_block`. Reachable only if the package is rewritten between `collect`'s read and `main`'s re-read (TOCTOU) — and it duplicates `print_report`'s `missing:` line (HEAD 216 / WT 243), which is the authority that actually fires | **DELETE** (with T6's main block **and** the selftest unpacks at R1:285/295, R2:312/322, R4:327/333; case 6's `not missing and` becomes redundant); keeps a single `missing` authority | mutant M3 |
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
| T22 | `build_block` prose block (`prose` list, `if not (valid recheck)`, `prose.append`, `cells[9] = …`) | 144, 150-152, 157 | same | direct call only | — | **R1: unreachable from `main`** — `check()` refuses `recheck-prose` at 184-186 before `build_block` runs, so capability 3 can never execute through the CLI; **R2 fixed it** by scoping `check` to `want_ids`; **R4** kept the fix but behind `--scope-to-admit` | **KEEP the capability, fix the caller** (done in R2, gated in R4) | R1: prose row + `--admit-ids` → exit 4, no block. R2: exit 0 + `normalized recheck`. R4 with `--scope-to-admit`: exit 0; without: exit 4 |
| T23 | `collect`: `registry_rows, _ = parse_rows(registry_text)` discarding registry malformed rows | 163 | same | — | — | **not dead**, but an unreported swallow: a mangled registry row is invisible, so a staged collision with its id false-greens capability 1 | **KEEP + surface the count** (do not delete) | receipt's `malformed=` only ever counts staged rows; `registry=76` cannot be cross-checked |
| T24 | recheck-validity predicate duplicated verbatim at `row_defects` and `build_block` | 107 & 150 | same | both | 107 only | not dead — two authorities for one rule (exactly the seam that let "refuse prose" and "normalise prose" coexist) | **no deletion**; fold into one `recheck_ok(value)` helper | reading |

Flags, same question: `--registry`/`--package` are the only flags (b) uses; `--selftest` is the
only flag (a) uses. **`--admit-ids`, `--entries`, `--access-date`, `--out` were exercised by
neither** — all four are reachable and were demonstrated by out-of-band runs (§5-B). At R1/R2,
`--entries` had an unguarded degenerate value: `--admit-ids` without `--entries` emitted an
**empty** `used-by` cell and exited 0 (§5-B). **R4 fixed that** by making `--entries` a hard
requirement (R4:427-428) — which in turn makes `used_by = … or "\u2014"` (R4:146) unreachable from
`main` (T25). R4 also adds two flags neither scenario uses: `--recheck` (404-408) and
`--scope-to-admit` (410-414) — reachable, unexercised by argv (the selftest reaches `scope=True`
through `check()` directly, never through the parser).

## 3b. Status at R4 (the revision that will ship)

Every §3 candidate re-checked against R4 (`73dae3b7…`, 435 lines). Line numbers are R4's.

| # | R4 line | status | note |
|---|---|---|---|
| T1/T2/T3 `Row.line_no`/`indent`/`raw` | 47, 49-54, 97 (+`ROW_RE` 33) | **LIVE** | identical dead fields; re-proved on R4 (`r4-m2`: selftest + real byte-identical, adoption identical) |
| T4 `opened` conditional | 156 | **FIXED** | now `cells[8] = access_date`, unconditional |
| T5 `anchor` switch | 80, 83-84, 86 | **LIVE** | still no caller; re-proved on R4 (`r4-m1`) |
| T6 `build_block` missing machinery | 141-143, 160; `main` 431-434; unpacks 327/333/349 | **LIVE** | `check` still refuses first (R4:221-223); re-proved on R4 (`r4-m3`: selftest, real, adoption and `missing`-id paths all byte-identical). The deletion touches **three** unpack sites at R4, not two — `oc_block, oc_prose, _` at 333 is a third |
| T7 redundant `if bad and …` | 211-213 | **LIVE** | now `if bad and not (want_ids and scope)`; still subsumed by 214-216 — R4 12-case A/B, 0 diffs (§5-G) |
| T8 `collisions_total`/`duplicates_total` | 186-187 | **LIVE** | still write-only |
| T9 `prose_recheck_total` recomputation + nested `get` | 189, 237 | **LIVE** | still two numbers under one field name |
| T10 `from __future__ import annotations` | 25 | **LIVE** | still redundant on ≥3.10 |
| T11 `not-a-table-row` | 72-73 | **LIVE** (gap) | still no fixture; reachable |
| T12 `columns=` | 75-76 | **FIXED (coverage)** | selftest case 5 now asserts `columns=12` (R4:312-320) |
| T13 invalid status | 104-105 | **LIVE** (gap) | unexercised at R4 too (`105` still in the miss list) |
| T14 `recheck-empty` | 108 | **LIVE** (gap) | — |
| T15 `source-empty` | 109-110 | **LIVE** | still outside the frozen schema list and unfixtured |
| T16 `EXIT_OK`-with-`want_ids` | 219-224 | **LIVE** | reachable; `--scope-to-admit` runs demonstrated it (exit 0) |
| T17 `print_report` printers | 240-249 | **PARTIAL FIX** | collisions/duplicates/no-defect arcs now reached via cases; `missing:` printer (249) still unexercised |
| T18 selftest failure path | 390-392 | **LIVE** | fires (M4 on R2 exit 1); same construct at R4 |
| T19 usage guards | 419, 425-426, 427-428 | **LIVE** | `--entries` guard added; all reachable (exit 2) |
| T20 adoption tail | 429-443 | **LIVE** | unexercised by (a)/(b) at R4 too — `425-443` still in R4's miss list |
| T22 prose normalisation | 152-155 | **FIXED** | reachable via `--scope-to-admit`; case 6 asserts it (R4:326,345) |
| T23 registry swallow | 167 | **LIVE** | still `registry_rows, _ =` |
| T24 duplicated predicate | 107 & 151 | **LIVE** | — |

New at R4, same question:

| # | R4 line | item | (a) | (b) | verdict |
|---|---|---|---|---|---|
| T25 | 146 | `used_by = ", ".join(admitted_entries) or "\u2014"` — the `or` arm is now unreachable from `main` (`--entries` required, 427-428) and from the selftest (always passes an entry) | — | — | **DELETE the fallback** (a used-by of `—` is not an admission record); or keep only if `build_block` is meant as a library API, which nothing calls (§: no importer) |
| T26 | 198-199 | comment says prose normalises "to the frozen access date"; the code writes `recheck_default` (`180d`) | — | — | **FIX the comment** — it now contradicts 155 and the design note at 153-154 |
| T27 | 404-408, 410-414 | `--recheck`, `--scope-to-admit` argv paths | — | — | **KEEP** (needed) — but record that no receipt exercises either |
| T28 | 175 & 195 | parameter `scope: bool` is rebound to a `set` inside the same function | — | — | **rename local** (e.g. `scope_ids`) — a bool that becomes a set is a trap for the next editor; no behaviour change |

## 4. The operability finding behind all of this

`package-gate.txt` is a **refusal receipt**: the gate was only ever run in check-only mode, so
(a)+(b) together still leave `main`'s adoption tail at 0% — no recorded evidence that the gate can
*accept* a block. At **R1** the contradiction was worse: 171 of 173 staged rows carry prose
`recheck`, which `check()` treated as fatal, so `build_block`'s normalisation was unreachable
through the CLI and the gate refused every row that capability 3 promises to normalise. R2 removed
the contradiction for every requested row; **R4** made it opt-in (`--scope-to-admit`) and left the
default strict, which is a defensible call — but it also means the default invocation still refuses
all 171 prose rows, and no receipt shows either mode accepting a block. §5-B demonstrates both.

Also worth the L1's attention: T6's deletion removes the only *second* place that reports `missing`,
and `print_report` (R1 216 / R2 243 / R4 249) already reports it — so deleting T6 loses no
observable behaviour (M3 proof).

## 5. Proof log

**A. T7 — 15-scenario A/B, original vs 205-207 deleted → 0 diffs**

```
SAME clean/no-want, clean/want, clean/want+entries, dup/no-want, dup/want,
     escaped/no-want, escaped-unrequested, 12cells/no-want, prose/want,
     prose/no-want, status-wip/want, empty-src/no-want, missing-id,
     real-package/no-want, scoped-clash
diffs: 0
```
(`scoped-clash` ⇒ exit 3 establishes R2:211-212 is **live**, so it must stay.)

**A2. T7 at R4 — 12-case A/B, `if bad and not (want_ids and scope)` removed → 0 diffs**

```
SAME selftest, real (frozen registry, exit 4), real+scope (exit 0), dup/unscoped (4),
     dup/want (4), escaped/unscoped (4), escaped/scoped-unrequested (0), prose/scoped (0),
     prose/unscoped (4), clean (0), missing (5), scoped-clash (3)
diffs: 0
```
So T7 is still dead weight at R4, and `scoped-clash` ⇒ exit 3 again shows R4:217-218 is live.


**B. Adoption mode is reachable and correct (R2, then R4)**

```
R2: $ python3 work-0345.py --registry registry-8c14a5d.md --package pkg.md \
      --admit-ids S900 --entries corpus/knowledge/new.md --access-date 2026-10-25
    registry=76 staged=1 … defects=0 prose=1
      normalized recheck S900: 2026-10-23 — re-verify at next release
    | S900 | … | mined | 2026-10-25 | 2026-10-25 | corpus/knowledge/new.md |        exit=0
    $ … --out block2.md  →  wrote …/block2.md rows=1                                 exit=0
    $ … --entries omitted →  | … | mined | 2026-10-23 | 180d |  |                    exit=0  ← unguarded (fixed at R4)

R4, same prose row + --scope-to-admit → the recheck cell becomes `180d`, `opened` becomes the
access date (R4:155-156); without --scope-to-admit → exit=4, `defect … recheck-prose`;
`--entries` omitted → parser.error, exit=2.
```
R1, same inputs with a prose row: `defect S900: recheck-prose`, **exit=4**, no block.

**C. R1's normalise arm (line 153)** — a row with `opened = "probe date"` is written out as
`2026-10-25` when `build_block` is called directly; no recorded path ever calls it with a
non-ISO `opened`, and the else-arm would have preserved the stale date. R2 dropped the conditional
entirely (T4 FIXED).

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
| M3 `m3-nodupmissing.py` | `build_block` returns 2-tuple (missing machinery removed), `main`'s `if missing` block removed, selftest case 6/7 unpack adjusted | `cases=10 failed=0` | identical (full-output `diff`, not first line) | behaviour-neutral; adoption-mode output and the `missing`-id refusal (exit 5) are byte-identical to base |
| M4 `m4-failingcase.py` | one case's expected constant broken | `cases=10 failed=1`, `failed: duplicate-staged-id`, **exit 1** | — | T18 fires |
| (T7) `mut-noredundant.py` | 205-207 removed | `cases=10 failed=0` | identical | 0/15 diffs |

**All three mutants were re-built against R4 and re-measured** (`r4-m1.py`, `r4-m2.py`, `r4-m3.py`
in the same scratch dir): `--selftest` output byte-identical, real-run output byte-identical
(`diff -q` silent, exit 4), adoption-mode output identical, `missing`-id refusal identical. The R4
build of M3 needed a **third** unpack fix (`oc_block, oc_prose, _` at R4:333) — the deletion's blast
radius grew with the selftest.

M2 needed the group renumbering: `ROW_RE`'s capture group 1 exists **only** to feed the dead
`indent` field, so deleting the field also shifts the id group. That coupling is itself the argument
for deleting it.

**F. An accidental control, and what it proves.** My *first* M3 cut `main`'s unpack to two values
but left `build_block` returning three. That broken deletion **passed both mandated scenarios**
(selftest `cases=10 failed=0`, real run byte-identical, exit 4) and only blew up on an adoption-mode
run: `ValueError: too many values to unpack (expected 2, got 3)`, rc=1. So neither (a) nor (b) can
observe a defect on the `build_block`→`main` seam — corroborating §4 independently of the coverage
numbers. The corrected M3 (both sides changed) is the one measured in §5-E.

## 6. Deletion set, if the L1 wants one patch

Against **R4** (what will ship) — every item here is still LIVE in §3b and proven
behaviour-neutral by the mutant named:

- **T1+T2+T3** — one edit: `Row.__slots__` and `__init__` (R4:47-54), the `Row(...)` construction
  (R4:97), and `ROW_RE`'s dead capture group (R4:33 → `(?: {0,3})`, with `group(2)`→`group(1)` at
  R4:95 and 97). Proof M2.
- **T5** — `anchor` param, ternary, and docstring lines R4:83-84. Proof M1.
- **T6** — `build_block` R4:141-143 + `return …, []` R4:160; `main` R4:432-434; selftest unpacks
  R4:327/333/349 (case 6's `not missing and` at R4:336 goes with it). Proof M3.
- **T7** — R4:211-213. Proof §5-G (0/12).
- **T8** — R4:186-187. Proof: grep, no reader.
- **T9** — the recomputation at R4:189 (derive from the unfiltered `defects` at R4:181 instead) and
  make the printer single-sourced (R4:237).
- **T10** — R4:25.
- **T25** — the `or "\u2014"` fallback at R4:146, which `main` can no longer reach.
- **T26/T28** — comment fix at R4:198-199, local rename for the rebound `scope` (R4:195). Not
  deletions, one-line corrections.

Net ≈ −20 lines at R4. Total deletions already FIXED by R2/R4 and not to be re-done: T4, T12's
coverage gap, T22.

Not recommended for deletion: T11-T15 (reachable refusals), T16-T20, T21, T23, T24, T27.

## 7. What a fixture would need to cover the gaps (advisory, not my call)

Still-uncovered refusals a fixture *can* reach at R4 — one case each: not-a-table-row (T11, R4:73),
invalid status (T13, R4:105), empty recheck (T14, R4:108), source-empty (T15, R4:110). Adoption
mode needs a receipt of its own (T20/T27): today nothing in the round's evidence shows the gate
emitting a block or using `--recheck`/`--scope-to-admit`. That is a coverage defect in *evidence*,
not in code.

## 8. Axis report

- **Weight**: at R4, eight dead items — six edit units — remain live and proven behaviour-neutral
  (T1, T2, T3, T5, T6, T7, T8, T10; M1/M2/M3 and both A/B batteries), plus one duplicate authority
  (T6), one duplicate computation (T9), one unreachable fallback (T25). Two former findings are
  already fixed upstream (T4, T22) and one coverage gap closed (T12).
- **Contract preserved**: all ten selftest cases pass in every mutant; the R1 receipt reproduces
  byte-identically before and after every mutant; R4's own selftest stays 10/10.
- No production file was touched to reach these conclusions.

## 9. Bounds check

- Scratch only: `/tmp/r29a2-simpgate/` (snapshots of R1/R2/R4, mutants, coverage data, fixtures,
  outputs).
- Reads outside the lane: `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` (read
  only; no campaign tool run), `git show` on the lane itself.
- The lane working tree already had ` M plans/sources_adopt.py` and untracked C1 artifacts when I
  started; I neither created nor removed any of them. My only write in the lane is this file.
- **Tooling**: `coverage.py 7.16.2` was already installed (`~/.local/bin/coverage`, uv-tool shim) and
  I ran it for R1/R2. Mid-audit the shim's target disappeared (`~/.local/bin/coverage` → dangling
  symlink into `~/.local/share/uv/tools/coverage/bin/`, `python3 -c "import coverage"` →
  `ModuleNotFoundError`), so I reinstalled it: **`uv tool install coverage --force` → coverage
  7.17.0** (channel: uv tool; reason: restore the measurement tool for R4; no pacman transaction —
  the host-wide pause was respected). Everything else (`uv`, `python3 3.14.8`, `git`) pre-existing.
- No subagents, no background jobs retained, no `ask` calls.
