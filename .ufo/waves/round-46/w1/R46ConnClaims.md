# R46ConnClaims — Cross-Claim Map, Code Path Independence, and Separability Analysis

- **Seat:** `R46ConnClaims` (UFO-FSD connector, leaf member)
- **Round:** kengaku round 46 (hyaku run 9, 2026-10-27), wave 1 (build / pre-data attacks)
- **Lane repo:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
- **Base commit:** `64ba8385ea10af1b78d367dcb242b92d97062af7`
- **Freeze commit:** `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f`
- **Target document:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-46-claims.md`
- **Declared axes:** calibration (C1), depth (C2), coverage (C3)
- **Receipts directory:** `.ufo/waves/round-46/w1/R46ConnClaims/`

---

## 1. Cross-Claim File Map

The round attacks three distinct surfaces across three declared axes. The table below maps every file and directory touched, modified, created, or executed by each claim's work, counters, gate tools, and receipts:

| Claim | Declared Axis | Work Files (Modified or Created) | Counters & Gate Tools | Evidence & Captures | Receipt Surfaces |
|---|---|---|---|---|---|
| **C1** | **Calibration** | `plans/fixture_fence.py`<br>`plans/refusals46/` (f1–f10 + held-out conversions)<br>`plans/sealed46/` (critic hostile modules) | `plans/round46_c1_verify.py`<br>(imports `plans/round44_c1_verify.py` @ `6cf05323`) | `plans/battery42/`<br>`plans/battery43/`<br>`plans/battery44/` (104 honest fixtures) | `.ufo/waves/round-46/claims/control-c1-*.txt`<br>`.ufo/waves/round-46/claims/c1-measure-*.txt` |
| **C2** | **Depth** | `corpus/SOURCES.md` (rows S157–S165)<br>`corpus/knowledge/tb2-password-recovery-grader.md` (predictor fix, source ranges, `## Errata (round 46)`) | `plans/round46_c2_verify.py` (frozen @ `2042d873`)<br>`plans/anchor_line_check.py` (gate @ `35d02dc5`)<br>(imports `plans/round45_c2_verify.py` @ `ab6825e3`) | `corpus/evidence/round45/tb2-password-recovery/` (captures @ `2dc14fc1`, etc.) | `.ufo/waves/round-46/claims/control-c2-*.txt`<br>`.ufo/waves/round-46/claims/c2-measure-*.txt` |
| **C3** | **Coverage** | `corpus/SOURCES.md` (rows S166–S172)<br>`corpus/knowledge/tb2-polyglot-c-py-grader.md`<br>`corpus/README.md` (index row, coverage bullet, §Frontier narrowing)<br>`PROVINCE.md` (polyglot-c-py paragraph)<br>`plans/polyglot_c_py_probe.py`<br>`plans/pkg-spec-r46.json` | `plans/round46_c3_verify.py`<br>`plans/pkg_gate.py` (frozen @ `ea638822`)<br>`plans/order_check.py`<br>`scripts/sources-census.sh` | `corpus/evidence/round46/tb2-polyglot-c-py/` (8 captures + SHA256SUMS)<br>`corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`<br>`corpus/evidence/round46/polyglot-c-py-probe.txt` | `.ufo/waves/round-46/claims/control-c3-*.txt`<br>`.ufo/waves/round-46/claims/c3-measure-*.txt` |

### Shared Round-Level Governance Files (Not Claim-Owned)
- `plans/round-46-claims.md`: Frozen whole for C2 at `fd4129eb`; stage-2 freeze amendment modifies pins and before-control receipts for C1 (`<P>`, `<R>`, `<S>`) and C3 (`<V>`) prior to scoring claimed work.
- `plans/scratch_guard.py` & `.ufo/waves/round-46/claims/envelope.sh`: Host safety runtime sandbox and scratch hygiene tools executed uniformly by all counter and probe runners.
- `SCORECARD.md` & `LOG.md`: Round-level closure documents updated exclusively by the L1 integrator (including routed defect D1 append-only correction).

---

## 2. Code-Path Independence: C1 Counter vs C2/C3 Tools

**Question:** *Does C1's new counter share code paths with C2 or C3 tools?*
**Finding:** **No shared code paths exist between C1's new counter and any C2 or C3 tool.**

### Detailed Analysis
1. **Module Imports in `plans/round46_c1_verify.py`:**
   Inspection of `plans/round46_c1_verify.py` (lines 100–125) reveals imports restricted to Python standard library modules (`argparse`, `concurrent.futures`, `hashlib`, `json`, `os`, `pathlib`, `random`, `re`, `secrets`, `shutil`, `signal`, `subprocess`, `sys`, `tempfile`).
   The only repo module loaded via `importlib.util.spec_from_file_location` is `plans/round44_c1_verify.py` (`K44_REL = "plans/round44_c1_verify.py"`, digest-pinned to `6cf05323...`) to reuse the round-44 `Ctx` class and sandbox fixture builder.
2. **Subject Execution:**
   The counter executes `plans/fixture_fence.py` inside an isolated `bwrap` container under an external `strace -f -y` process. The fence is invoked through an out-of-process harness (`ctl/harness.py`), never imported directly into the counter's own interpreter.
3. **Absence of C2/C3 Code Paths:**
   - C1 does not import or execute `plans/round46_c2_verify.py`, `plans/anchor_line_check.py`, `plans/round45_c2_verify.py`, `plans/anchor_digest_check.py`, `plans/round46_c3_verify.py`, `plans/pkg_gate.py`, `plans/order_check.py`, or `plans/polyglot_c_py_probe.py`.
   - Neither C2 nor C3 counters/tools import or execute C1's counter, `plans/round44_c1_verify.py`, or `plans/fixture_fence.py`.
4. **Deliberate Decoupling in C3:**
   In `plans/round46_c3_verify.py` (drafted by `R46ExecC3Counter`), lines 138–139 explicitly document:
   > `V12's own anchor-line rule (re-implemented from the semantics of plans/anchor_line_check.py; that module is not imported, so a change to it cannot change what this counter certifies)`
   C3 deliberately re-implements the anchor-line check inline to prevent code-level coupling to C2's gate tool.
5. **Substrate-Level Only:**
   The only commonality between C1 and C2/C3 is host-level system tooling: the Linux kernel, Python 3.12/3.13 runtimes, bubblewrap (`bwrap`), git, and the wrapper script `.ufo/waves/round-46/claims/envelope.sh`.

---

## 3. Interaction Between C2 Leg A and C3 Rows

**Question:** *Where do C2 leg A and C3's rows interact?*
**Finding:** **C2 leg A executes a global, whole-registry anchor line check over `corpus/SOURCES.md`. When C3's new rows S166–S172 are landed with their captures, any line, range, or word-count defect in C3's rows directly fails C2 leg A.**

### Mechanism
In `plans/round46_c2_verify.py`:
```python
def leg_a(lane, alc):
    lines = []
    rc, res = alc.check(lane, out=lines.append)
    live = len(res["live"])
    ok = live == 0 and not missing and not changed
    return ok, f"live={live} repaired={rep} base_rows={len(base)} base_missing={len(missing)} base_changed={len(changed)}"
```
`plans/anchor_line_check.py` (`alc.check`) reads `lane / "corpus" / "SOURCES.md"`, parses *every* row in the registry table via `parse_rows()`, and indexes all captures across `corpus/evidence` via `git ls-files`.
- For every row where an anchor quote is cited and the capture exists, `row_defects()` verifies:
  1. The quote sits exactly on the cited line number (`:N`).
  2. The line range (`:a-b`) encompasses `N` and does not exceed file length.
  3. The token count (`(K words)`) matches `len(quote.split())`.
- If defects exist and no superseding row repairs them, the row ID enters `res["live"]`.
- `round46_c2_verify.py` leg A demands `live == 0`.

### Empirical Verification on Scratch Clone
We executed live tests on a `--shared` scratch clone of the lane at `fd4129eb`:

1. **Clean Base (`receipt-c2-base-fail.txt`):**
   - Command: `python3 plans/round46_c2_verify.py --lane .`
   - Output: `A anchorline live=8 repaired=0 base_rows=149 base_missing=0 base_changed=0 DEFECT`
   - Outcome: 8 round-45 live defective rows (S108, S149–S155), fails as expected.
2. **C2 Repaired Rows S157–S165 Only (`receipt-c2-repaired-pass-live0.txt`):**
   - Command: `python3 plans/anchor_line_check.py --lane .`
   - Output: `ANCHORLINE rows=158 cited=48 captured=44 uncaptured=4 defective=8 repaired=8 live=0 cells=0`
   - Outcome: All 8 defective rows repaired by S157–S164 (`repaired=8 live=0`), passes.
3. **C2 Rows S157–S165 + C3 Rows S166–S172 + Captures:**
   - Command: `python3 plans/anchor_line_check.py --lane .`
   - Output: `ANCHORLINE rows=165 cited=55 captured=51 uncaptured=4 defective=8 repaired=8 live=0 cells=0`
   - Outcome: C3's seven rows S166–S172 are captured and defect-free (`live=0`).
4. **Induced Defect in C3 Row S166 (`receipt-c2-coupled-c3-defect.txt`):**
   - We modified C3 row S166 in `corpus/SOURCES.md`, changing `:18 ... (5 words)` to `(99 words)`.
   - Command: `python3 plans/anchor_line_check.py --lane .`
   - Output:
     ```
     ROW S166 state=live defects=words:1
     ANCHORLINE rows=165 cited=55 captured=51 uncaptured=4 defective=9 repaired=8 live=1 cells=1
     ```
   - Command: `python3 plans/round46_c2_verify.py --lane .`
   - Output: `A anchorline live=1 repaired=8 base_rows=149 base_missing=0 base_changed=0 DEFECT`
   - Outcome: **C2 fails entirely due to a defect in C3's row S166.**

### Asymmetry of Coupling
- **C2 depends on C3:** C2's leg A evaluates all captured rows in `corpus/SOURCES.md`. A defect in C3's rows turns C2 red.
- **C3 does NOT depend on C2:** In `plans/round46_c3_verify.py`, leg V12 loops exclusively over `pkg.spec["rows"].items()` (the rows specified in `plans/pkg-spec-r46.json`, namely S166–S172). V12 does not inspect S157–S165. C3's leg V6 runs `sources-census.sh`, which validates schema structure and `used-by` paths, but does not check line/range/word defects. C3 passes V12 and V6 even if S108 or S149–S155 remain defective.

---

## 4. Cross-Claim Pattern: Gates That Certified Something False

**Question:** *Are all three claims 'a gate that certified something false' repairs?*
**Finding:** **Yes. All three round-46 claims repair verification gates or package counters that previously certified false, defective, or vacuous artifacts as passing.**

### Detailed Comparison Across All Three Claims

| Claim | What the Prior Gate Certified | Why the Certification Was False | How Round 46 Repairs the Gate |
|---|---|---|---|
| **C1** | Round-45 counter printed `PREDICATE C1 pass` (`REFUSALS 10/10 clean`, `HONEST 104/104`, `contradicted=0`). | The counter leaked module/fixture names in directory paths. A 7-line dummy fence (`fences/keyed_name.py`) checking `"/refusals45-" in str(d)` passed the counter without inspecting fixture internals, while 8 of 10 held-out hostile modules were admitted. | **Q39 Name Hiding & Sandbox Integrity:** Fixture names, parents, and build dirs are randomized tokens (`secrets`); child directory counts are padded with decoys; strace logs are written outside sandbox mounts (B1); stat channels and directory-relative touches outside `d` are blocked and detected (B3, B5, B6). |
| **C2** | Round-45 C2 counter printed `PREDICATE C2 pass` (`checks=11 defects=0`) for the `password-recovery` package. | (1) The entry's `## Predictor` claimed universal-newline handling (`:150, :194`) but only replaced `\r\n` with `\n`, false-negativing 3 classes of lone-CR newlines. (2) Three row anchors cited incorrect lines (S153 cited line 28 `echo 0` instead of line 26 `echo 1`). | **Newline Adversarial Testing & Anchor Gate:** Counter leg B tests 16 frozen newline states against the captured grader; leg C enforces entry errata marks (`lone-CR`, `S152`, `S153`, `S154`, `empty-file`); leg A uses `plans/anchor_line_check.py` to enforce that quotes match exact lines, ranges, and word counts; Q34 superseding rows S157–S165 correct the registry without mutating historical rows. |
| **C3** | Previous package gates (`plans/pkg_gate.py`) certified structural presence of files and syntax. | Prior gates could be passed by: (1) a filler package containing syntactically valid but substantively empty entries/rows, (2) lookup-table predictors memorizing test inputs, or (3) rows citing mislocated quotes. | **Hardened Coverage Verification (V11–V13):** (1) V11 generates randomized state sets per run using `os.urandom` to defeat memorized lookup predictors. (2) V12 validates line, range, and word counts for all package rows. (3) V13 enforces negative control rejection: asserting that a committed filler package (`plans/filler46/`) triggers DEFECT on at least 3 substantive content legs (V3, V4, V7, V9, V10, V12). |

### Proposed SKILL.md Line
> **A gate without negative controls certifies ceremony, not truth:** every verifier must test blinded inputs (Q39), negative controls (admit-all/refuse-all/filler packages), and adversarial or mutated states (lone-CR, hostile modules) before its pass verdict is admitted.

---

## 5. Concrete Separability Break & Cross-Claim Couplings

**Question:** *Flag any separability break with the concrete file.*
**Finding:** **The concrete file breaking separability is `corpus/SOURCES.md`.**

While `plans/round-46-claims.md` §Separability (lines 121–127) asserts that claims are causally separable, physical and verification separability breaks at `corpus/SOURCES.md`.

### Concrete Separability Break: `corpus/SOURCES.md`
1. **Physical Edit Conflict (Merge Hazard):**
   - Claim 2 writes rows S157–S165 to `corpus/SOURCES.md`.
   - Claim 3 writes rows S166–S172 to `corpus/SOURCES.md`.
   - Both sets of rows must be inserted at the exact same location in the document: immediately after `| S156 |` (line 171) and immediately before `## Paths` (line 172). Parallel development on independent branches creates an unavoidable git merge conflict in `corpus/SOURCES.md`.
2. **Sequential Row ID Allocation Dependency:**
   - C3 allocates IDs S166–S172 under the assumption that C2's superseding rows occupy S157–S165. If C2's rows were modified, re-ordered, or reduced, C3's IDs in `plans/pkg-spec-r46.json` and its counter would require re-numbering.
3. **Verification Coupling (C2 Leg A):**
   - As proven empirically in §3, `plans/round46_c2_verify.py` Leg A scans the entire `corpus/SOURCES.md` file. C2 cannot pass unless C3's rows in `corpus/SOURCES.md` are also completely free of line, range, and word defects.
4. **Census Schema Coupling (C3 Leg V6):**
   - `plans/round46_c3_verify.py` Leg V6 runs `sources-census.sh validate --file corpus/SOURCES.md`. A malformed row or invalid date/tier cell introduced by C2 fails C3's counter. Furthermore, C3 rows in `corpus/SOURCES.md` cause census exit 1 (`E11 missing used-by`) if landed before `corpus/knowledge/tb2-polyglot-c-py-grader.md` is created.

### Enumeration of Cross-Claim Couplings (`n = 5`)
1. **Coupling 1 — `corpus/SOURCES.md` Physical Merge Collision (C2 ↔ C3):** Concurrent write to the same table insertion point.
2. **Coupling 2 — Registry ID Sequence Dependency (C2 ↔ C3):** C3 row IDs S166–S172 depend on C2 row IDs S157–S165.
3. **Coupling 3 — Whole-Registry Anchorline Validation (C2 ↔ C3):** C2 Leg A scans all of `corpus/SOURCES.md`, making C2 pass/fail dependent on C3 row correctness.
4. **Coupling 4 — Whole-Registry Census Validation (C3 ↔ C2):** C3 Leg V6 runs whole-file census validation, coupling C3 to C2 row formatting.
5. **Coupling 5 — Stage-2 Claims Freeze Amendment (C1 ↔ C3):** Both C1 and C3 modify `plans/round-46-claims.md` at stage 2 to pin counter digests, `<P>`, `<R>`, `<S>`, `<V>`, and before-control receipts.

**Summary Counts:**
- Cross-claim couplings: **5**
- Separability breaks (concrete files): **1** (`corpus/SOURCES.md`)

---

## 6. Connector Proposed Move (FSD Synthesis)

In accordance with UFO-FSD connector discipline, we propose one bounded, non-obvious move that improves round execution without harming any declared axis:

- **Evidence:** Receipt `receipt-c2-coupled-c3-defect.txt` confirms that uncoordinated or defective landing of C3 rows in `corpus/SOURCES.md` breaks C2 leg A (`A anchorline live=1 DEFECT`), while `receipt-sources-census-c2-c3.txt` confirms that landing C3 rows before the knowledge entry breaks census (`E11 missing used-by`).
- **Affected Axes:** Depth (C2) and Coverage (C3).
- **Proposed Move (Staged Staging Protocol for `corpus/SOURCES.md`):**
  The L1 integrator must enforce a two-stage sequential commit protocol for landing wave-2 work into the master branch:
  1. **Commit 1 (C2 Depth Landing):** Land C2 rows S157–S165 into `corpus/SOURCES.md` alongside the `password-recovery` entry fixes. Execute `plans/round46_c2_verify.py` and verify `checks=4 defects=0` and `PREDICATE C2 pass` in isolation.
  2. **Commit 2 (C3 Coverage Landing):** Append C3 rows S166–S172 into `corpus/SOURCES.md`, add `corpus/evidence/round46/tb2-polyglot-c-py/` captures, create `corpus/knowledge/tb2-polyglot-c-py-grader.md`, and land C3 specs/probes/counters. Re-run both `plans/round46_c3_verify.py` and `plans/round46_c2_verify.py`.
- **Risks:** Adds one intermediate commit to the L1 landing sequence. Minimal overhead; prevents tangled rollbacks.
- **Verification:** Verification of Commit 1 proves C2's depth repair stands independently on base, isolating any subsequent C3 regression to Commit 2.

---

VERDICT: cross-claim-couplings-5-separability-breaks-1
