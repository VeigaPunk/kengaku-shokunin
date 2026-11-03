# GateRedRun — R68-C2 red re-pin (round 68, wave 1)

Seat: GateRedRun (leaf; no dispatch, no background jobs, no installs). Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`; every run below was made with cwd = lane root.
Host Python: `python3 -V` → `Python 3.14.8`.

Tree at pin (`2026-11-03T20:04:59-03:00`):

- HEAD `d5b3c3090dd418bf00a9411a4bee2c593d9ed4ac`.
- `git status --porcelain -- plans SKILL.md corpus/evidence/round67 corpus/evidence/round68` → only
  `?? corpus/evidence/round68/` (the L1's untracked battery bytes **plus one concurrently written
  correction artifact**, see F-1). The instrument and the other C2 inputs are clean vs HEAD.
- Instrument `plans/round68_c2_correction_gate.py` sha256
  `acda6c8a1ee3e6a29a01dbf5fa9576f076808e5cd0339a161eb35e22337ef7f9`, equal to
  `git show HEAD:plans/round68_c2_correction_gate.py | sha256sum` — the frozen instrument bytes.
- Probe bound by E3: `plans/round67_c1_pipeline_probe.py` sha256
  `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e` = the frozen
  `R67_PROBE_SHA` (re-hashed at run time by E3 and again here).
- `plans/round-67-claims.md` sha256
  `1dacb910d7b5c2ca28b874728eb18c24c94d48a54d3c6900856210fb3f4cc76c`;
  `grep -c '^## Erratum (round 68)' plans/round-67-claims.md` → `0` at run time.

No port-8080 access; no installs; no git/jj mutation (read-only `git status/rev-parse/log/show/diff`,
`sha256sum`, `stat`, `diff` only).

---

## 1. Red run (default mode), exit captured in-runner

Command (cwd = lane root):

```sh
{ python3 plans/round68_c2_correction_gate.py; echo "rc=$?"; } \
  > .ufo/waves/round-68/w1/gate/red-before-recheck.txt 2>&1
```

Output — `.ufo/waves/round-68/w1/gate/red-before-recheck.txt`
(mtime `20:00:45.357 -03`, sha256 `d9251370fd80fdba980c430e5b41d36348438319289a84c86328754914f1dd02`):

```text
E1 defect ## Erratum (round 68) section absent in plans/round-67-claims.md
E2 defect no erratum section
E3 defect corpus/evidence/round68/r67-probe-selftest.txt missing (probe re-hash ok)
E4 defect pipeline-row=False, sqlite-row-strict=False
E5 defect no erratum section
DEFECTS n=5
PREDICATE R68-C2 fail
rc=1
```

Matches the required red pin: `DEFECTS n=5`, `PREDICATE R68-C2 fail`, **rc 1**.

## 2. Comparison with the freeze-time receipt

`diff -u .ufo/waves/round-68/w1/gate/red-before.txt .ufo/waves/round-68/w1/gate/red-before-recheck.txt`
→ exactly one hunk, the added in-runner capture line:

```diff
@@ -5,3 +5,4 @@
 E5 defect no erratum section
 DEFECTS n=5
 PREDICATE R68-C2 fail
+rc=1
```

The five defect lines, `DEFECTS n=5` and `PREDICATE R68-C2 fail` are byte-identical to the
freeze-time receipts (`red-before.txt` sha256 `ce593b0f4b7e352e8e96fa3f5b9ad64892a1a9cf588ebf9e910aca47baabb1d1`).
**No difference in the defect list.** The freeze receipt carried no rc capture; the claims' stated
"exit 1" is now evidenced by `rc=1` in the recheck file.

## 3. Selftest, exit captured in-runner

`--work` must be an existing directory (`main()` prints `SETUP work-dir-required` and returns 2
otherwise); `S/gate` was created with `mkdir -p` first.

Command:

```sh
{ python3 plans/round68_c2_correction_gate.py --selftest \
    --work /fast/scratch/hyaku/kengaku-r68/GateRedRun/gate; echo "rc=$?"; } \
  > .ufo/waves/round-68/w1/gate/selftest-recheck.txt 2>&1
```

Output — `.ufo/waves/round-68/w1/gate/selftest-recheck.txt`
(mtime `20:00:49.519 -03`, sha256 `ca3df6389bc8ab8f2006160d8a9ba47a416b57cb05380576b411d8c22e0e8680`):

```text
E1 defect ## Erratum (round 68) section absent in plans/round-67-claims.md
E2 defect no erratum section
E3 defect corpus/evidence/round68/r67-probe-selftest.txt missing (probe re-hash ok)
E4 defect pipeline-row=False, sqlite-row-strict=False
E5 defect no erratum section
DEFECTS n=5
PREDICATE R68-C2 fail
SELFTEST defects-in-fake=5 want=5 all-fail=True
rc=0
```

Required line present verbatim: `SELFTEST defects-in-fake=5 want=5 all-fail=True`; **rc 0**.

---

## 4. Finding F-1 (material): a C2 correction artifact landed mid-wave, 6 s after the pin

The wave premise "the corrections are NOT landed yet" no longer held from `20:00:51 -03`:

| fact | value |
|---|---|
| red pin completed | `2026-11-03 20:00:45.357 -03` |
| tally generator header date | `2026-11-03T23:00:47Z` = `20:00:47 -03` |
| `corpus/evidence/round68/r67-probe-selftest.txt` mtime | `2026-11-03 20:00:51.301 -03` |
| tally sha256 / size | `5a15dfd2ec8f2f114d49e344330c5b6ea06115ca95842e200c4e27c0387e7467` / 663 B |
| tally header provenance | names scratch dir `/fast/scratch/hyaku/kengaku-r68/SelftestTally/tally` (a sibling wave seat; not this seat) |

Tally bytes (verbatim):

```text
# R67 probe --selftest tally (round 68: routed defect 3, committed evidence)
# date: 2026-11-03T23:00:47Z
PROBE sha256=03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e
python3 plans/round67_c1_pipeline_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r68/SelftestTally/tally
CHECK ok cases=6
PREDICATE R67-C1 pass
CHECK defect: q1-ref vector FPPP != frozen PPPP
CHECK defect: q1-ref frozen label match contradicts vector FPPP
CHECK defect: q1-ref rc=0 is not the pytest status for vector FPPP (want 1)
CHECK defect: VECTOR q1-ref FPPP disagrees with its junit PPPP
CHECK findings=4
PREDICATE R67-C1 fail
SELFTEST green_rc=0 red_rc=1 ok
rc=0
```

Re-run of the gate after the tally appeared (`red-after-concurrent-tally.txt`, mtime
`20:02:13.227 -03`, sha256 `197757ef25c9b47dcf86f85637584113bc5ee01a3c6984ff3f6b317179ecdfa6`):

```text
E1 defect ## Erratum (round 68) section absent in plans/round-67-claims.md
E2 defect no erratum section
E3 ok probe-line=True, selftest-line=True, rc-capture=True, probe-rehash=ok
E4 defect pipeline-row=False, sqlite-row-strict=False
E5 defect no erratum section
DEFECTS n=4
PREDICATE R68-C2 fail
rc=1
```

Consequences, stated exactly:

- The **pinned** red state (`n=5`, `fail`, `rc=1`) is real and matches the freeze receipt, but it is
  valid only for the `20:00:45` snapshot. A re-run from `20:00:51` onward prints `DEFECTS n=4`
  (E3 turns green) and still exits `1`, i.e. the gate remains red but the "must print n=5" clause is
  no longer reproducible on the live tree.
- This seat did not create or modify that tally. It is untracked (`corpus/evidence/round68/` is
  untracked as a whole) and belongs to the L1's integration.
- The wave spec's premise and the sibling seat's mid-wave write contradict each other; reconciling
  them is the L1's call. If the tally is to count as a correction landing, then correction 3 is
  already present pre-integration and the red-before evidence must be dated accordingly.

---

## 5. Clause-by-clause: does each check implement its frozen sentence?

Frozen source: `plans/round-68-claims.md`, R68-C2 check list. Code source:
`plans/round68_c2_correction_gate.py` (line numbers from the frozen bytes above).

| check | frozen clause | code | verdict |
|---|---|---|---|
| E1 erratum-sha | "contains **exactly one** `## Erratum (round 68)` heading, and the section names both 0379… and 32ba…" | `erratum_section()` `:49-63` returns the **first** section; E1 `:96-104` checks both shas in it, never counts headings | **PARTIAL — uniqueness clause not implemented** (demonstrated) |
| E2 mutant-count | "the same erratum states `7 refused` and `1 accepted by design` (each substring present at least once in the section)" | `:107-113`: `in sec` for both | **MATCH** (the frozen sentence itself specifies substrings) |
| E3 selftest-tally | "exists, contains a `PROBE sha256=03793f4f…` **line**, contains a `SELFTEST` **line** and an `rc=` capture, and the gate's own re-hash of `plans/round67_c1_pipeline_probe.py` equals 0379…" | `:115-129`: `is_file()` ✓; `sha256_file(probe) == R67_PROBE_SHA` ✓; the three content checks are **unanchored substring tests** (`:124-126`) | **PARTIAL — no line anchoring** (demonstrated); current tally is well-formed so E3 passes for the right reasons today |
| E4 registry-rows | "`SKILL.md` contains at least one `round67_c1_pipeline_probe` registry row, and the `round65-c1-sqlite-probe` row line contains `--strict`" | `:70-81` + `:131-147`: confined to the `## Gate/probe registry (PROTOCOL §Gate standard)` section; heading absent ⇒ defect. `registry_section()` docstring says "else the whole text" (`:71`) but the code returns `None` (`:78-79`). Only the **first** line containing `round65-c1-sqlite-probe` is tested (`:142-145`) | **STRICTER than the literal sentence + docstring/code inconsistency**; red on the current tree is nonetheless correct (see below) |
| E5 before-value | "the erratum names the true delta — both `recipe-unexecuted` and `executed 2 of 3` present in the section" | `:149-156`: `in sec` for both | **MATCH** |
| `--selftest` | "build red fixtures under the scratch root and prove every check can fail"; kill rule (c) a check that cannot fail ⇒ vacuous | `:165-209`: lane-shaped fake with the erratum stripped, the pipeline row dropped, `--strict` removed from the sqlite line, and no tally; requires `defects == 5 and rc == 1` | **MATCH**; observed `defects-in-fake=5 want=5 all-fail=True`, rc 0 |

Clause evidence for E4's red on the current tree (all re-checked at `20:04:59 -03`):

- `SKILL.md` registry heading at line **587** (count 1).
- `round67_c1_pipeline_probe` occurs exactly once in `SKILL.md`, at line **81** — the
  process-environment class row naming `plans/round67_c1_pipeline_probe.py`, **outside** the
  registry section. E4's section scoping is what stops that mention from producing a false green.
- `round65-c1-sqlite-probe` occurs exactly once, at line **686** (the row inside the registry), and
  that line does **not** contain `--strict` (`grep -c 'round65-c1-sqlite-probe.*--strict'` → 0). So
  one occurrence also means the first-match brittleness is not material today.

### Demonstrations (scratch copies of the lane; lane bytes untouched)

Transcript retained at `.ufo/waves/round-68/w1/gate/clause-fixtures.txt` (sha256
`e8ef9fd378bb369bdc4e81a831ce74d1416098dc60f3666125886c89c546e407`); fixtures were built under
`S/clause-fixtures/` and deleted with the scratch root. Each fixture is a minimal lane-shaped root
run with `--root`.

1. **green** (landed-tree simulation: erratum with both shas / `7 refused` / `1 accepted by
   design` / `recipe-unexecuted` / `executed 2 of 3`, tally copy, pipeline row inserted inside the
   registry heading, `--strict` appended to the sqlite line) → `DEFECTS n=0`,
   `PREDICATE R68-C2 pass`, rc 0. The gate can go green when the corrections are present.
2. **dup-heading** (green + a second empty `## Erratum (round 68)` heading) → `E1 ok`,
   `DEFECTS n=0`, rc 0. **Proof the "exactly one heading" clause is unenforced**: E1 examines the
   first section only, never counts.
3. **no-registry-heading** (green minus the `## Gate/probe registry …` heading, row text still in
   `SKILL.md`) → only `E4 defect registry section absent (## Gate/probe registry (PROTOCOL §Gate
   standard))`, `DEFECTS n=1`, rc 1. Demonstrates the narrowing vs the literal frozen sentence and
   the docstring promise ("else the whole text").
4. **loose-tally** (green with the tally replaced by
   `XPROBE sha256=03793f4f… trailing\nNOTSELFTEST blob rc=0\n` — neither a `PROBE` line nor a
   `SELFTEST` line) → `E3 ok probe-line=True, selftest-line=True, rc-capture=True,
   probe-rehash=ok`, `DEFECTS n=0`, rc 0. Demonstrates the missing line anchoring: malformed tally
   bytes are accepted.

No check was found that fails to match its sentence in the direction of being *weaker than the
frozen red state requires* except the two gaps above (E1 uniqueness, E3 line anchoring); E4 is the
opposite direction (stricter than the literal sentence). The instrument is frozen — this seat did
not edit it.

## 6. Provenance notes (observations, not verdicts)

- The freeze receipt `.ufo/waves/round-68/w1/gate/red-before.txt` has mtime
  `19:54:43.128 -03`, ~2 s **before** the frozen instrument's mtime `19:54:45.660 -03`. The
  instrument bytes equal HEAD and my independent run reproduces the receipt's five defect lines
  exactly, so no behavioral discrepancy is observable; the ordering only means the receipt cannot
  *prove* which bytes produced it (same class as R68-C1's named limitation (i)). Recorded for the
  L1 rather than resolved here.
- The gate's default mode reads the working tree, so it sees the untracked tally; after the L1
  commits the tally, E3 remains green without further work.

## 7. Verdict

```text
GATE red-reproduced=True selftest=ok
```

Caveat, exactly: `True` refers to the pinned `20:00:45 -03` snapshot (`DEFECTS n=5`,
`PREDICATE R68-C2 fail`, rc 1, defect list identical to the freeze receipt). From `20:00:51 -03`
(F-1) a re-run prints `DEFECTS n=4` and still exits red (`PREDICATE R68-C2 fail`, rc 1).

## 8. What the L1 must integrate

- Keep `W/gate/red-before-recheck.txt` as the wave's red re-pin (rc 1); it differs from
  `W/gate/red-before.txt` only by the added `rc=1` line. No defect-list difference.
- Keep `W/gate/selftest-recheck.txt` (rc 0, `defects-in-fake=5 want=5 all-fail=True`).
- `W/gate/red-after-concurrent-tally.txt` is the **drift measurement**, not the pin — do not
  present it as red-before evidence.
- Decide how the mid-wave tally (`corpus/evidence/round68/r67-probe-selftest.txt`, untracked,
  sibling-produced) is dated and counted. If it is integrated, correction 3's anchor exists before
  the wave's end; the remaining red anchors are E1/E2/E4/E5.
- If the instrument is integrated as-is, record its three clause gaps as named limitations (do not
  edit the frozen bytes): E1 does not enforce "exactly one" erratum heading; E3 accepts the
  PROBE/SELFTEST tokens without line anchoring; E4's `registry_section()` docstring promises a
  whole-text fallback it does not implement.
- For the landed SKILL.md: put the `round67_c1_pipeline_probe` row **inside** the
  `## Gate/probe registry (PROTOCOL §Gate standard)` section (heading currently line 587), and put
  `--strict` on the line containing `round65-c1-sqlite-probe` (currently the single occurrence,
  line 686) — a separate continuation line would not satisfy E4.

## 9. Evidence files (relative to the lane root)

| path | sha256 | mtime -03 |
|---|---|---|
| `.ufo/waves/round-68/w1/gate/red-before-recheck.txt` | `d9251370fd80fdba980c430e5b41d36348438319289a84c86328754914f1dd02` | 20:00:45.357 |
| `.ufo/waves/round-68/w1/gate/selftest-recheck.txt` | `ca3df6389bc8ab8f2006160d8a9ba47a416b57cb05380576b411d8c22e0e8680` | 20:00:49.519 |
| `.ufo/waves/round-68/w1/gate/red-after-concurrent-tally.txt` | `197757ef25c9b47dcf86f85637584113bc5ee01a3c6984ff3f6b317179ecdfa6` | 20:02:13.227 |
| `.ufo/waves/round-68/w1/gate/clause-fixtures.txt` | `e8ef9fd378bb369bdc4e81a831ce74d1416098dc60f3666125886c89c546e407` | 20:04 |
| `.ufo/waves/round-68/w1/gate/red-before.txt` (freeze reference, read-only) | `ce593b0f4b7e352e8e96fa3f5b9ad64892a1a9cf588ebf9e910aca47baabb1d1` | 19:54:43.128 |
