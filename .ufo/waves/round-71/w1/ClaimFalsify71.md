# ClaimFalsify71 — falsification of R71-C1 and R71-C2

Seat: critic, round 71 wave w1. Lane tip at review start: `d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0`
(`git -C L rev-parse master`). No predicate, case table, vector, digest, kill rule, target or
instrument was edited. All mutations were on scratch copies under
`S=/fast/scratch/hyaku/kengaku-r71/ClaimFalsify71`; the forged/stub receipts are copied beside
this report.

## What I ran (command → rc)

| # | command | rc |
|---|---|---|
| 1 | `python3 plans/round71_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round71/hf/receipt.txt --work S/real-check` | **0** — `DEFECTS n=0` / `PREDICATE R71-C1 pass` |
| 2 | `python3 S/forge.py` (builds a receipt through the probe's own `battery_lines`, no case executed) | 0 |
| 3 | `python3 plans/round71_c1_hf_probe.py --lane . --check-receipt S/forged-receipt.txt --work S/checkwork` | **0** — `DEFECTS n=0` / `PREDICATE R71-C1 pass` |
| 4 | `flock /fast/scratch/hyaku/kengaku-r71/port-5000.lock python3 S/c1_stub_attack.py` | 0 (4 sandbox runs; results below) |
| 5 | full 8-case sandbox run with the designed stub, then `diff S/stub-receipt.txt corpus/evidence/round71/hf/receipt.txt` | **0 — empty diff** |
| 6 | 7 self-contradictory receipt mutations through `--check-receipt` | 1 × rc 1, 6 × **rc 0** |
| 7 | `grep` counter demo on `git show d8a77d3:SKILL.md` in scratch | 0 |
| 8 | `python3 plans/round71_c2_routed_defects.py --lane .` | 0 — all four `ok`, `DEFECTS n=0` |
| 9 | `… --selftest --work S/c2-self` | 0 — `defects-in-fake=4 want=4 all-fail=True append-only-arm=True ok=True` |
| 10 | `… --mutants --work S/c2-mut` | 0 — `MUTANTS total=4 killed=4 survived=0` |
| 11 | `python3 S/c2_attacks.py` + follow-ups (10 scratch-lane attacks) | per-attack below |

Hygiene: no git/jj mutation; no tool installs; the only lane-side artifact is
`plans/__pycache__/round71_c1_hf_probe.cpython-314.pyc` (gitignored via `.gitignore:2
__pycache__/`) created when my attack script imported the probe — no tracked file touched.

---

## R71-C1

The predicate as frozen (`plans/round-71-claims.md:43-48`) is **met**: attack 1 above re-derives
`DEFECTS n=0` / `PREDICATE R71-C1 pass` / rc 0 on the committed receipt. I found no kill in the
predicate's own terms. Four attacks land against the claim's *evidence* language.

### C1-a — junk receipt with all `P`s and consistent arithmetic passes

Command: `S/forge.py` stages the eight cases (no subprocess, no model load, no sandbox), builds
`results` with `legs` copied from `VECTORS`, and emits a receipt via the probe's own
`battery_lines`. Then attack 3.

Result: **`DEFECTS n=0` / `PREDICATE R71-C1 pass` / rc 0.** This is not a format exploit: the
receipt is emitted by the probe's own writer (`battery_lines`), and its `CASE` lines are
digit-for-digit identical to the receipt of record; the only difference in those lines is
`server_pid=424242` vs `server_pid=3` (the forged receipt also omits K6's two `EXC` lines and
carries `exc=0`, which the checker accepts because it recomputes `exc_n` from the `EXC` lines
present), and `check_receipt` never validates `server_pid` (it reads only
`case_sha256` and `sandbox_rc`: `plans/round71_c1_hf_probe.py:668-678` and `:706-707`). The `case_sha256`
"staged-input digests" are deterministic over staged bytes (`stage_case` + `tree_digest`,
`plans/round71_c1_hf_probe.py:381-414,266-275`), so they bind bytes, not execution.

Verdict: **lands, and is a declared limitation** (claims `:63-73` (v)). The consequence the
limitation does not name: the predicate is satisfiable with zero execution, so the clause
"every one of its four legs is witnessed both `P` and `F`" is carried only by the per-case
sandbox captures — which no instrument reads. `check_receipt` takes no evidence directory and
`battery_lines` never emits capture hashes (`plans/round71_c1_hf_probe.py:513-555`).

### C1-b — a stub `transformers` on `PYTHONPATH` fakes leg 1, invisibly

`bwrap_argv` has no `--clearenv` (`plans/round71_c1_hf_probe.py:416-441`), so the parent
environment is inherited. I ran the probe's own staging and argv unchanged; the only delta was
`PYTHONPATH=/tests/stub` with the stub placed in the already-bound `/tests` directory. (I ran it
*inside* the probe's sandbox rather than sandbox-free: the sandbox is not the defence, and this
is the real attack surface.)

Stub used (the naive one):

```python
class _Obj: pass
class AutoModelForSequenceClassification:
    @classmethod
    def from_pretrained(cls, path, *a, **k): return _Obj()
class AutoTokenizer:
    @classmethod
    def from_pretrained(cls, path, *a, **k): return _Obj()
```

Results:

```
naive-stub   case=K1 rc=0 derived=PPPP frozen=PPPP agree=True
naive-stub   case=K8 rc=0 derived=PPPP frozen=FPPP agree=False   <- crude stub is caught by K8
designed-stub case=K8 rc=0 derived=FPPP frozen=FPPP agree=True
designed-stub case=K7 rc=0 derived=FPPP frozen=FPPP agree=True
```

A designed stub that adds the same `config.json` readability check the real library performs
(`json.loads` → raise) reproduces **8/8 frozen vectors**:

```
STUB-MATRIX K1 derived=PPPP frozen=PPPP agree=True
… K2 PPFP / K3 PPFP / K4 PPPF / K5 PFPP / K6 PFFF / K7 FPPP / K8 FPPP …
STUB-MATRIX agree=8/8
```

and the receipt that run produces is **byte-identical** to the receipt of record:

```
$ diff S/stub-receipt.txt corpus/evidence/round71/hf/receipt.txt
$ echo $?
0
```

K8 is not a defence: the grader's `from_pretrained` is wrapped in `try/except Exception → assert
False` (`corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py:17-22`), and a
stub can raise on unreadable config exactly as the real library does. The only artifact that
distinguishes a real load from the stub is the *detail* string in the un-checked capture —
`sandbox/K8/manifest.json`: `"It looks like the config file at
'/app/model_cache/sentiment_model/config.json' is not a valid JSON file."` — and `battery_lines`
does not put `detail` in the receipt (the `CASE/LEGS/EXC/VECTOR` writer at `:513-555`), nor does
`check_receipt` read the evidence dir.

The probe's handling of `PYTHONPATH`/import provenance is: **nothing**. The `LIBRARIES` line is
derived by `library_versions()` running `/fast/ComfyUI/.venv/bin/python3` **on the host**
(`plans/round71_c1_hf_probe.py:315-325`), not inside the sandbox, so the checker re-derives the
host venv's versions regardless of what the sandbox imported. This falsifies the mechanism
claims in `:63-65` (ii) ("the receipt records the exact versions and the checker re-derives
them").

Verdict: **lands hard.** The frozen table prices the grader's control flow, but it does not
witness the model-load half it exists to price; the receipt cannot tell a real load from a stub.
The crude stub is caught (K8), the designed stub is not — the defence is an outcome check, not a
provenance check.

### C1-c — the class-row move (`3 of 8` → `4 of 8`) is guarded by no instrument

- The frozen predicate (`plans/round-71-claims.md:43-48`) contains **no** `SKILL.md` clause.
- Neither round-71 instrument reads `SKILL.md`: `grep -c SKILL plans/round71_c1_hf_probe.py
  plans/round71_c2_routed_defects.py` → `0`, `0`.
- The only stated check is the manual pair in `:52-54`: `grep -c 'executed 3 of 8' SKILL.md` → 0
  and `grep -c 'executed 4 of 8' SKILL.md` → 1. On the frozen blob both counters are the
  pre-move values; a bare token edit satisfies them:

```
$ git show d8a77d3:SKILL.md | grep -c 'executed 3 of 8'     -> 1
$ git show d8a77d3:SKILL.md | grep -c 'executed 4 of 8'     -> 0
$ sed 's/executed 3 of 8/executed 4 of 8/' (frozen copy)     -> 0 and 1
```

Nothing requires the row to name `hf-model-inference`, round 71, or the receipt. During this
review the L1 landed the row in the working tree (`SKILL.md:78` now reads `executed 4 of 8 (…;
round 71 \`hf-model-inference\` replayed offline under an eight-case table …)` and its evidence
column cites `corpus/evidence/round71/hf/receipt.txt`) — the landed text is right, but the
instrument that is supposed to force it does not exist.

Verdict: **lands.** The coverage move is an assertion in prose, not a derived count. Also, at
review time `corpus/evidence/round71/hf/receipt.txt`, `check.txt` and `sandbox/` are untracked
(`git ls-files corpus/evidence/round71/` lists only `instruction.md` and the five model files),
so "the receipt of record … committed bytes" is not yet literally true.

### C1-d — `--check-receipt` accepts six kinds of self-contradiction

Each tamper was applied to the passing forged receipt and checked with `--work`.

| tamper | rc | result |
|---|---|---|
| `VECTOR K2 … agree=False` (control) | 1 | **killed** — `DEFECT vector-agree K2` |
| duplicate `LEGS K2` all-`P`, then the correct `PPFP` line | **0** | pass |
| `EXC K1 test_model_downloaded=E` while `LEGS K1` leg 1 is `P`, `SUMMARY … exc=1` | **0** | pass |
| duplicate `CASE K1 case_sha256=deadbeef …`, then the correct digest | **0** | pass |
| a wrong `SUMMARY … mismatches=7 setup=5 exc=99` line before the correct one | **0** | pass |
| a line `PREDICATE R71-C1 fail` before the correct predicate line | **0** | pass |
| duplicate `VECTOR K2 expected=PPPP derived=PPPP agree=True`, then the correct line | **0** | pass |

`parse_receipt` is last-line-wins with no duplicate detection (`plans/round71_c1_hf_probe.py:
600-617`; the dict assignments overwrite). Round 70's checker in the same capability had
`duplicate-vector`, `duplicate-test` and `duplicate-case` defects
(`plans/round70_c1_nginx_probe.py:645,654,665`); round 71 dropped all three — a regression
across instruments. The sixth row is the sharpest: a receipt whose own bytes say the predicate
failed exits 0, because `want_pred in text` only asks whether the passing line is *present*.

Verdict: **lands.** Every self-contradiction except a value flip passes; a nested red line is
silently ignored.

---

## R71-C2

The gate is green on the lane (attack 8, rc 0) and its own arms are real (attacks 9–10). The
attacks below are on scratch copies of the four lane files; none was run against `L`.

### C2-a — `E1a` can be satisfied while the lesson carries a wrong count / fake rows

| attack (scratch lane) | gate | result |
|---|---|---|
| 9th data row **inside** the `## Mistakes` table (control) | rc 1 | **killed** — `DEFECT E1a row-count=9 want=8` |
| prose line "This round records six Mistakes rows" in `## Gate` | **rc 0** | pass |
| the eight row labels replaced with `junk-row-1…8`; the eight keys moved to a prose line | **rc 0** | pass |

`check_e1_lesson` counts rows (`plans/round71_c2_routed_defects.py:93-103`) but matches the keys
against the **whole file**: `if key not in text` (`:100`). So the eight class names need not be
row labels, and a wrong count anywhere outside the table is invisible. The count itself is
guarded.

Verdict: **lands.** `E1a`'s literal sentence ("data-row count is 8 and the eight class keys are
present") is satisfied by eight junk rows plus eight names in prose; the names are not bound to
rows.

### C2-b — `E1b` passes on a line that corrects nothing, and on one that corrects to the wrong number

`check_e1_log` (`:105-122`) looks for `R70-D1` within a ±2/+24-line window and requires, in that
window, `"superseded"`, `"five"`, `re.search(r"\beight\b")` and `"2026-11-03"` (`:115-116`).

| LOG.md body (scratch) | gate |
|---|---|
| `- R70-D1 was routed. The reviewer's note said \`five\`; that note is superseded by eight unrelated cases in round 71 on 2026-11-03. No correction was written.` | **E1b ok**, `DEFECTS n=0`, rc 0 |
| `- **R70-D1 (round 71, 2026-11-03).** The note \`five\` is superseded, but the correct count is seven, not eight.` | **E1b ok**, rc 0 |
| `- R70-D1.` followed by an unrelated neighbouring line carrying `superseded`/`five`/`eight`/date | **E1b ok**, rc 0 |

The second row is the decisive one: the claims sentence (`plans/round-71-claims.md:104-105`) says
`E1b` is "a dated R70-D1 entry that quotes the superseded 'five' and states eight"; the check
accepts an entry that states **seven** because the word `eight` merely appears. The third shows
the window lets unrelated lines supply every token.

Verdict: **lands.** `E1b` does not establish the count it certifies — the check is weaker than
its own frozen sentence.

### C2-c — `E1c`: names-without-count is killed; two natural wrong counts escape

| attack | gate |
|---|---|
| index row and support block list all eight names, no count (control) | rc 1 — **killed**: `DEFECT E1c index-row:count=None` |
| appended `Round-70 lesson carries six Mistakes rows in the supporting block.` | **rc 0** |
| appended `round-70 lesson — Mistakes rows: six, per the first sweep.` | **rc 0** |
| appended second index row `| \`lessons/round-70.md\` | round-70 Mistakes rows: six, … |` | rc 1 — **false red**: `DEFECT E1c line805:count=70` |

The catch-all at `:162` is case-sensitive (`"round-70" in line`), so the sentence-initial
`Round-70` spelling is never scanned. `parse_count` (`:85-91`) requires the number immediately
before `Mistakes rows`, so `Mistakes rows: six` yields `None` and no defect; conversely
`round-70 Mistakes rows` is parsed as **count 70** and refused. The instrument is
under-inclusive on the natural forms and produces a false red on the hyphenated round label.

Verdict: **lands on two forms, killed on the name-only form.** `E1c`'s sentence ("every README
mention … says eight … no unsuperseded wrong count remains") is false of lanes the gate passes.

### C2-d — `E2a` passes on an erratum that denies the correction, and does not pin the range

`check_e2_entry` (`plans/round71_c2_routed_defects.py:172-188`) requires `E-D2`, the literal
`instruction.md:6-11,15-18`, the substring `supersede`, and the quoted sentence `states the same
bodies` **anywhere after the first `## Errata` heading** — and the entry already carries
`## Errata (round 70)` at `:53`, so the slice (`:180`) spans both errata sections and the round-70
addendum. E-D3 (`:55-59`) already carries the literal range; E-D4 (`:60-65`) already carries
`supersedes`. Results on scratch copies:

| entry variant | gate |
|---|---|
| round-71 `## Errata` block deleted entirely (control) | rc 1 — **killed**: `no-E-D2`, `erratum-does-not-quote-superseded-sentence` |
| real block replaced by `## Errata` + `- E-D2.` | rc 1 — **killed**: `erratum-does-not-quote-superseded-sentence` (the only occurrence of the phrase is inside the removed block, `:98`) |
| real block replaced by a **denial** that quotes the sentence and mentions the range: "… is NOT superseded; `instruction.md:6-11,15-18` is mentioned only to show the citation range … No correction made." | **rc 0** — `E2a ok`, `DEFECTS n=0`, `PREDICATE R71-C2 pass` |
| real block replaced by a block that states the **wrong** corrected range ("the corrected range is `instruction.md:99-100`. The bodies are not at 15-18.") | **rc 0** — the required literal is supplied by E-D3 |

The control shows the quote and `E-D2` are genuinely bound to the block. The two passing rows
show the other two clauses are not: a denial satisfies "supersede", and the "corrected range"
literal need not be in the round-71 block at all.

Verdict: **lands on two of four clauses.** `E2a` cannot distinguish an erratum from a denial of
the erratum, and it does not require the corrected range to be stated by the round-71 block.

---

## Calibration — what the gates did kill

- `E1a` row-count drift: 9th row inside the table → `row-count=9 want=8`, rc 1.
- `E1c` names-without-count → `count=None`, rc 1.
- C1 `VECTOR … agree=False` → `DEFECT vector-agree`, rc 1.
- C2's own arms re-derived by me: selftest `defects-in-fake=4 want=4 all-fail=True
  append-only-arm=True ok=True` (rc 0); mutants `4 killed=4 survived=0` (rc 0).
- C1's do-nothing control (`.ufo/waves/round-71/c1-control.txt`) is `FFFF` in all eight cases
  and the counter prints fail — the counter does refuse a do-nothing lane.

So the instruments are not vacuous. The wounds are in the *positive* direction: they pass texts
that do not carry the property they certify.

---

## Verdict

**R71-C1 survives its frozen predicate and is wounded as a witness.** I re-ran
`--check-receipt` on the receipt of record (`DEFECTS n=0`, `PREDICATE R71-C1 pass`, rc 0), and
no clause of the frozen predicate fails. But the predicate is satisfied by a forged receipt with
zero execution (rc 0, digests identical modulo the never-checked `server_pid`), by a small
`transformers` stub whose eight-case receipt is **byte-identical** to the receipt of
record (`diff` rc 0), and six self-contradictory receipts pass — because `parse_receipt` lost
round 70's duplicate-line guards. The class-row move is not instrumented at all. The claim's
"witnessed both `P` and `F`" therefore rests on un-checked sandbox captures, and its
"model-load half is priced" language is falsified at the mechanism level, not just conceded by
limitation (iii).

**R71-C2 is wounded.** The gate prints `E1b ok`/`E1c ok`/`E2a ok` on a lane where the `LOG.md`
entry corrects "five" to **seven**, the README says `Round-70 … six Mistakes rows`, and the
round-71 errata block is a denial that the sentence is superseded (while E-D3 elsewhere supplies
the "corrected range" literal the check asks for). The actual lane corrections are genuine —
I read them at `LOG.md:2650-2656`, `corpus/README.md` (both round-70 mentions),
`corpus/lessons/round-70.md:63-69` and
`corpus/knowledge/tb2-nginx-request-logging-offline.md:90-99` — so the claim's proposition about
the current bytes holds; what does not hold is "a re-deriving gate": three of its four checks
are token-presence, and the fourth (`E1a`) does not bind names to rows. Only the `E1a` row
count is genuinely re-derived.

### Smallest safe corrections (no frozen element changed)

R71-C1:
1. Restore round-70's duplicate guards in `parse_receipt` (`duplicate-vector`, `duplicate-test`,
   `duplicate-case`) and require the `SUMMARY`/`PREDICATE` lines to be unique.
2. Bind the receipt to the live witness: emit `CAPTURE <cid> manifest_sha256=… stdout_sha256=…`
   in `battery_lines` and re-derive those files in `check_receipt` (this puts K8's real
   `not a valid JSON file` detail, and K6's `ConnectionError`, into the checked bytes).
3. Emit an in-sandbox import-provenance line (e.g. `IMPORT transformers=<path> sha256=<…>` from
   the harness) and add `--clearenv` plus an explicit `PYTHONPATH` to `bwrap_argv`; then a stub
   on `PYTHONPATH` is either impossible or visible.
4. Instrument the class row: a `plans/round71_c1_classrow.py` that parses the `network-service`
   row and asserts `executed 4 of 8` + `hf-model-inference` + `round 71` + the receipt path,
   wired into the counting command.

R71-C2:
1. `E1b`: require the corrected count adjacent to a correction verb (`correct(ed) count is eight`
   / `states eight` / `carries eight rows`) and reject a competing stated count in the same
   block; or re-derive eight from the lesson and require the LOG entry to state that number.
2. `E1c`: make the scan case-insensitive; parse `Mistakes rows[:=]? <count>` as well as
   `<count> Mistakes rows`; exclude a number preceded by `round-` (fixes the false `count=70`);
   scan every mention, not only the first index/support site.
3. `E2a`: scope the errata slice to the block that carries `E-D2` (split on the **last**
   `## Errata`, or extract the section containing `E-D2`), require the corrected range inside
   that block, require the erratum to assert the correction (`bodies are at` / `corrected range
   is`), and reject `not superseded` / `no correction` in the block.
4. `E1a`: match the eight keys against each row's first cell (`cells[0]`), not the whole file,
   so names and rows are bound.

Tooling: none installed or upgraded; nothing was run with `pacman`. Scratch under
`S=/fast/scratch/hyaku/kengaku-r71/ClaimFalsify71` was removed after the two receipts and the
stub source were copied beside this report.
