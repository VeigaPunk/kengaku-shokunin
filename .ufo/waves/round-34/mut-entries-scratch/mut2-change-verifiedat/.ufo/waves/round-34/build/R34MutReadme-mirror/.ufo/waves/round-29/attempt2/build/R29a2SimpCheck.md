# R29a2SimpCheck — YAGNI pass on `plans/adoption_check.py`

Seat: `L1Kengaku29.R29a2SimpCheck` (leaf, no dispatch). Adversarial simplifier, advice only.
Audited revision: **HEAD `8c14a5d`** (`git show HEAD:plans/adoption_check.py`), baseline tip
`1f3b0f1` per `plans/round-29-attempt2-claims.md:8`. Scratch: `/tmp/r29a2-SimpCheck/`.
Production edits by me: **none** (only this report). Tool installs/updates: **none**.

## Axes named

- **Coverage** — does each printed counter measure something the claim actually froze
  (`plans/round-29-attempt2-claims.md:23-26`), or does it measure a self-declared proxy?
- **Operability** — can the counter run, fail for the right reason, and be pointed at a fixture at
  all?

Both axes move in the same direction here: three counters are measuring themselves, one is
outside the frozen line, one is satisfied by doing nothing.

## Live drift during this pass (read before citing line numbers)

Sibling seats edited the tree while I measured. `git status --porcelain` now shows
`M corpus/README.md, M corpus/SOURCES.md, M plans/adoption_check.py, M plans/sources_adopt.py`
(not mine). The one change to the audited file is a real bug fix that invalidates one of my
findings against the working tree only:

```
@@ -92,8 +92,9 @@
     if args.census:
+        lane_name = lane.name[: -len("-shokunin")] if lane.name.endswith("-shokunin") else lane.name
         proc = subprocess.run(
-            [str(CENSUS), "validate", "--root", str(lane.parent), lane.name],
+            [str(CENSUS), "validate", "--root", str(lane.parent), lane_name],
```

I say so explicitly so the L1 does not re-fix an already-fixed defect; the finding below is
recorded against HEAD, where I observed the failure.

`plans/round-29-attempt2-claims.md` also gained a 12-line C2 scope clarification **appended after
line 90** (`git diff --stat` = `1 file changed, 12 insertions(+)`). C1's frozen target
(`claims:23-26`) and its used-by wording (`claims:31-33`) are byte-unchanged, so every line
citation in this report still resolves; the insertion only invalidates citations *below* line 90.

## A. Counters: dead, mode-vacuous, redundant, or out-of-contract

| # | Counter | file:line (HEAD) | Class | Evidence |
|---|---|---|---|---|
| A1 | `verified_at` (and the `ok` term) | `plans/adoption_check.py:67,78,107,115` | **out-of-contract / must go** | It is the only field the counter prints that the frozen target does not contain. Frozen target (`claims:23-26`): `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`. Actual (`/tmp/r29a2-SimpCheck/v/B_all_good`): `...usedby_ok=1 verified_at=1 census=skipped`. Field lists differ at position 7, so **no run of this script can ever match the frozen acceptance string**. |
| A2 | `census` without `--census` | `:93` (`census_code = 0`), `:116` | **dead in the control invocation** | The frozen control command passes no `--census` (`claims:49`). With the flag absent the counter prints `census=skipped` and the `ok` term is constant-true; it cannot change between a passing and a failing round in that invocation. Receipt `.ufo/waves/round-29/attempt2/control.nothing.txt:4` and fixture `A_do_nothing` both show `census=skipped`. |
| A3 | `census` with `--census` at HEAD | `:96` | **broken at HEAD (fixed in working tree)** | `validate --root <parent> lane.name` passes `kengaku-shokunin`; the census roster keys lanes as `rel%-shokunin` (`scripts/sources-census.sh:482`). Observed: `ERROR: unknown lane (not a dir, not in conf or root): kengaku-shokunin`, census exit 2 → `census=fail`. The same census passes (exit 0) when given the absolute lane dir. Working tree fix verified: `python3 plans/adoption_check.py --expect … --census` → `… census=ok`, exit 0. |
| A4 | `rows_present` | `:81`, ok term `:112` | **redundant — can never be the sole failure** | `rows_mined ≤ rows_present ≤ |cited|` by construction (`:81-82`). So `rows_present < |cited|` ⟹ `rows_mined < |cited|`. Fixtures: `C_status_queued` fails `rows_mined` alone (rows_present=5); `D_rows_absent`, `E_rows_indented_2sp`, `G_extra_citation` fail both. No fixture exists where `rows_present` is the distinguishing term. |
| A5 | `rows_present == len(cited)` and `rows_mined == len(cited)` as `ok` terms | `:112-113` | **satisfied by doing nothing** | The do-nothing run evaluates both as `0 == 0` → **true** (fixture `A_do_nothing`, and the receipt's `cited_rows=0 rows_present=0 rows_mined=0`). Two of the five data counters therefore contribute nothing to rejecting the control; the control's exit 1 comes only from `present`(`:110`), `indexed`(`:111`), `usedby_ok`(`:114`), `verified_at`(`:115`). |
| A6 | `cited_rows` | printed `:106`, never in `ok` | **self-referential / display-only** | The RHS of `:112-113` is the measurement itself, so the entry's own `source:` lines set the bar. Fixture `K_three_of_five` (entry declares **3** of the 5 frozen sources, all 5 registry rows mined and linked): current counter prints `cited_rows=3 rows_present=3 rows_mined=3` and **exits 0**. The expect-declared set (`adoption-expect.json:10`) is never compared to what the entry says. |
| A7 | `usedby_ok` | `:83-90` (`break` at `:90`), ok term `:114` | **under-strict existential** | `break` after the first matching row makes the counter per-entry `any()`, not per-row. Fixture `J_partial_usedby` (1 of 5 rows names the entry, 4 name `corpus/knowledge/other.md`) → `usedby_ok=1`, **exit 0**. C1's "used-by naming the entry" (`claims:31-33`) is not what this measures. |

Non-counter dead weight in the same file:

| # | Item | file:line | Class | Evidence |
|---|---|---|---|---|
| A8 | `--lane` | `:53` | **argument the frozen use never passes** | Only in-repo caller is `claims:23,49`; neither passes it. `grep -rn adoption_check` over the lane returns only the claims file. It has no `help=`, is undocumented in the module docstring, and is unexercised by any committed test. Keep **only** if it becomes the seam of a `--selftest` (it is the sole non-destructive way to run the counter against a fixture — I used it for all 10 fixtures); otherwise delete. |
| A9 | `expect["round"]`, `expect["attempt"]` | `.ufo/waves/round-29/attempt2/adoption-expect.json:2-3` | **unread keys** | `:60-61` read only `access_date` and `entries`. Both keys are decoration; the counter is not round-aware. |
| A10 | `expect["access_date"]` | `:60` | **becomes dead once A1 goes** | It is consumed only by the `verified_at` string test (`:78`). Removing A1 removes the key's last reader. |

## B. Logic duplicated with `plans/sources_adopt.py`

| # | Counter site | Gate site | Divergence observed |
|---|---|---|---|
| B1 | `ROW_RE` literal `:33` | `sources_adopt.py:33` | Byte-identical regex, two copies. |
| B2 | `registry_rows()` cell split `:44-46` (`raw.rstrip()[1:-1].split("|")`, `len(cells) != 11 → continue`) | `sources_adopt.py:38` `COLUMNS=11`, `:60-76` `split_cells`, `:80-99` `parse_rows` | **The parsers disagree on legal rows.** `ROW_RE` admits 0–3 leading spaces, but the slice `[1:-1]` assumes column 0, so a 2-space-indented row yields **12** parts and is silently dropped. Measured: `split_cells('  | S077 | … |')` → 11 cells, reason `''` (gate accepts); counter fixture `E_rows_indented_2sp` → `rows_present=0 rows_mined=0 usedby_ok=0`, output identical to genuinely-absent `D_rows_absent`. Escaped-pipe rows are likewise silently dropped rather than reported (`sources_adopt.py:70-72` returns `escaped-pipe`). |
| B3 | `registry[row_id][7] == "mined"` `:82` | `sources_adopt.py:103` `row.cell(7)` status check; written by `:155` `cells[7] = "mined"` | Two copies of the status index, and the counter re-asserts the literal the gate itself writes — it can only catch a hand edit or a non-gate append. |
| B4 | `rel in cells[10]` `:88` | `sources_adopt.py:154` `cells[10] = used_by` | Same column, two owners; the gate projects `used-by`, the counter tests it with `break` (A7). |
| B5 | registry read `:62` → `registry_rows()` `:38` | `sources_adopt.py:160` `collect()` | `corpus/SOURCES.md` is parsed by two independent parsers in the same round; only one of them is exercised by C2's selftest. |

Cheapest de-duplication: `sys.path.insert(0, str(Path(__file__).resolve().parent))` then
`from sources_adopt import ROW_RE, split_cells`. Two lines delete B1+B2's second parser and make
the counter inherit the gate's indent/escaped-pipe semantics. I ran that exact import in the
minimal counter below; it compiles and behaves as predicted.

## C. Minimal discriminating counter set I would keep

Constraint honoured: the frozen line (`claims:23-26`) is **not** edited; the same seven fields print
in the same order. Do-nothing must still fail; a real adoption must still pass.

| Keep | Role | `ok` term becomes |
|---|---|---|
| `entries` | only term that actually rejects the do-nothing control | `present == len(entries)` |
| `indexed` | independent surface: `corpus/README.md` index row | `indexed == len(entries)` |
| `cited_rows` | live measurement of the entry's own `source:` lines | `cited == required` where `required = {sid for e in entries for sid in e["sources"]}` |
| `rows_present` | **print-only diagnostic** (A4) | — (dropped from `ok`) |
| `rows_mined` | registry work load-bearing, measured over `required` (A6) | `rows_mined == len(required)` |
| `usedby_ok` | cross-link, per-entry **all()** over `required` (A7) | `usedby_ok == len(entries)` |
| `census` | fleet gate still green | `census_code == 0` (only reachable with `--census`) |
| ~~`verified_at`~~ | **deleted** from print and `ok` (A1) | — |

Net: 8 printed / 7 gating → **7 printed / 6 gating**, one diagnostic, zero out-of-contract fields.

The frozen control knob is one line: measure against `adoption-expect.json` instead of against the
entry's own text. That single substitution is what makes `rows_present`/`rows_mined` non-vacuous on
the control (A5) and what makes a 3-of-5 entry fail (A6).

### Measured before/after (identical fixtures, `/tmp/r29a2-SimpCheck/`)

| Fixture | current HEAD | minimal | Note |
|---|---|---|---|
| `A_do_nothing` | exit 1, `…usedby_ok=0 verified_at=0 census=skipped` | exit 1, same minus `verified_at` | control preserved |
| `B_all_good` | exit 0, 8 fields | exit 0, **7 fields = frozen target shape** | pass preserved |
| `C_status_queued` | exit 1 | exit 1 | `rows_mined=0` |
| `D_rows_absent` | exit 1 | exit 1 | `rows_present=0` |
| `E_rows_indented_2sp` | exit 1 | **exit 0** (`rows_present=5`) | parser divergence fixed (B2) |
| `F_wrong_verified_at` | exit 1 | **exit 0** | honest cost of A1 — see tradeoffs |
| `G_extra_citation` | exit 1 | exit 1 | extra citation still refused |
| `H_readme_missing` | exit 1 | exit 1 | `indexed=0` |
| `I_usedby_other_entry` | exit 1 | exit 1 | `usedby_ok=0` |
| `J_partial_usedby` | **exit 0** | **exit 1** (`usedby_ok=0`) | A7 closed |
| `K_three_of_five` | **exit 0** (`cited_rows=3`) | **exit 1** | A6 closed |

End-to-end on the lane after the sibling registry/index edits landed, the minimal counter prints the
frozen target **byte-for-byte** and exits 0:

```
$ python3 /tmp/r29a2-SimpCheck/patched/adoption_check.py \
    --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
exit=0
```

while the production counter on the same tree still prints the extra field:

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok
exit=0
```

## Ranked moves (cheapest first, each exit-status-invariant on A/B except where stated)

1. **Delete `verified_at`** (`:67,78,107,115`) — restores the frozen line; ~6 lines. Invariant on A
   (fail) and B (pass); flips `F` only, stated below.
2. **Reconcile `cited` with `required`** — kills A5/A6; ~2 lines (`required` set + `cited == required`),
   plus `rows_*` loops over `required`.
3. **`break` → `all()`** (`:86-90`) — closes A7; one expression.
4. **Drop `rows_present` from `ok`** (`:112`) — keep the print.
5. **Import the gate's parser** (`from sources_adopt import ROW_RE, split_cells`) — closes B1/B2,
   fixes `E`; 2 lines.
6. **Delete or tests-seat `--lane`** (`:53`) — A8. Either is defensible; deleting is cheaper, keeping
   plus a three-fixture `--selftest` is the more useful (the gate already has that pattern).
7. **`round`/`attempt` keys** — delete from `adoption-expect.json` or stop pretending they are read.

## Tradeoffs (not hidden)

- **Removing `verified_at` gives up the counter's only automated check of the re-grounding date.**
  After that, `C1`'s "entry carries `2026-10-25`" is enforced only by the five
  `R29a2RevQuoteS07*/S090` seats and the Gate-block audit, not by the frozen command. That is the
  correct trade only because the frozen target does not contain the field: a silent extra gate that
  cannot be seen in the acceptance line is worse than a duty that is visibly owned elsewhere.
- **`rows_present` kept as a print-only diagnostic** costs one unverified number on the line, in
  exchange for the frozen output shape. It is the only redundant field I would not delete outright.
- **`K_three_of_five` is a counter hole, not a claim hole** — the entry-drafting duty may already
  forbid citing 3 of 5; the counter as written would not catch it either way.
- **`--lane`**: deleting it removes the only fixture seam; the counter would then have no way to be
  tested without touching the lane. I rank the import-of-gate-parser move (5) above it because (5)
  buys correctness, whereas (6) buys tidiness.

## Checks run (all read-only against the lane; scratch writes only under `/tmp/r29a2-SimpCheck/`)

- `git show HEAD:plans/adoption_check.py` greps — line numbers above.
- `python3 -m py_compile plans/adoption_check.py` → `compile-ok`.
- `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json` (no
  `--census`) → `entries=1 indexed=0 cited_rows=5 rows_present=0 rows_mined=0 usedby_ok=0
  verified_at=1 census=skipped`, exit 1 (mid-run partial state, before siblings landed rows).
- `python3 plans/adoption_check.py … --census` at HEAD → `census=fail` (census exit 2,
  `unknown lane: kengaku-shokunin`); after the sibling `lane_name` fix → `census=ok`, exit 0.
- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  /home/vgpnk/Projects/shokunin/kengaku-shokunin` → 15 `W04 duplicate url` warnings + `ok`, exit 0.
  (`validate` is stdout-only outside `--selftest`; no `--out` was passed, no write occurred.)
- 11 counter fixtures + 1 minimal-counter comparison run: `/tmp/r29a2-SimpCheck/build.py`,
  `/tmp/r29a2-SimpCheck/patched/adoption_check.py`.
- Not run: `plans/sources_adopt.py --selftest` (owned by C2's seats; the file is modified in the
  working tree, so any result I reported would be stale on arrival).

## Scope statement

Findings only. I did not integrate, did not judge the round, and did not edit any production file.
`plans/adoption_check.py`, `plans/sources_adopt.py`, `corpus/README.md` and `corpus/SOURCES.md`
are dirty from sibling seats, not from this one.
