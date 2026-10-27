# R46W2Conn — Cross-Claim Pattern Finder (Connector, Round 46 Wave 2)

- **Seat:** `R46W2Conn` (UFO-FSD connector, leaf member)
- **Role:** Cross-claim pattern finder over the landed round 46 at TIP `42d5043afac952fcb43bf4798757785dd258cf85`.
- **Target:** Wave-2 findings across claims C1 (calibration), C2 (depth), and C3 (coverage).
- **Report path:** `.ufo/waves/round-46/w2/R46W2Conn.md`
- **Receipts directory:** `.ufo/waves/round-46/w2/R46W2Conn/`

---

## 1. Provenance & Measured Revision (Closure D3)

Clone verification in scratch container (`/fast/scratch/hyaku/kengaku-r46/R46W2Conn/lane`):
```text
REV 42d5043afac952fcb43bf4798757785dd258cf85
TOP /fast/scratch/hyaku/kengaku-r46/R46W2Conn/lane
```
All commands, inspections, and counter-checks were executed against this clean checkout of landed tip `42d5043afac952fcb43bf4798757785dd258cf85`.

---

## 2. Evidence: Cross-Claim Wave-2 Findings & Shared Root Cause

Review of the available wave-2 reports on disk revealed several critical findings that cut across the three landed claims:
- **C1 reports reviewed:** `R46W2C1HoArgv`, `R46W2C1HoStore`, `R46W2C1HoConfig`, `R46W2C1HoPaths`, `R46W2C1Intent`, `R46W2C1Forge`, `R46W2C1Rerun`, `R46W2C1MutFence`, `R46W2C1HoHonest`.
- **C2 reports reviewed:** `R46W2C2Entry`, `R46W2C2Bypass`, `R46W2C2Rerun`.
- **C3 reports reviewed:** `R46W2C3Rerun`, `R46W2C3Mut`, `R46W2C3Rows`, `R46W2C3Cases`, `R46W2C3Filler`, `R46W2C3Entry`, `R46W2C3Oracle`.
- **Round-level reviews:** `R46W2NoHarm`, `R46W2Census`.

### 2.1 The Shared Root Cause: Nominal Representation without Decoupled Negative Controls (The "Token-Presence Proxy Fallacy")

Across all three claims, the verifier, fence, or grader substituted **nominal presence** (the occurrence of a string literal, token, tag, or static allowlist name) for an **operational or structural invariant**, because no negative control was frozen to prove that the nominal representation could not pass without the substantive property:

1. **In C2 (`R46W2C2Bypass`):**
   `plans/round46_c2_verify.py` Leg C checks `## Errata (round 46)` by string presence: `marks = sum(1 for t in ERRATA_MARKS if er and t in er.group(1))`. A hollow section containing solely the five bare tokens (`lone-CR S152 S153 S154 empty-file`) with zero explanatory text, line references, or evidence passes Leg C (`errata_marks=5/5 ok`). The verifier checked token presence, not substantive correction.
2. **In C1 (`R46W2C1HoPaths`, `R46W2C1Intent`, `R46W2C1HoHonest`, `R46W2C1MutFence`):**
   - `plans/fixture_fence.py` filtered `\n` in the `--lane` CLI argument string, using argument hygiene as a nominal proxy for tree hygiene, but admitted repository files with embedded newlines (`links_special_names.py`, confirmed in `c1-newline-and-allowlist-receipt.txt`).
   - `_tree` inspected entries with `lstat` for `S_ISLNK`, using symlink absence as a proxy for store containment, failing across filesystem mount boundaries (`st_dev`).
   - The fence allowlist (`GIT_TOP`) was fitted against the 104 legacy honest fixtures, causing it to over-refuse 9/9 novel benign honest repositories (`R46W2C1HoHonest` rejected packed refs, tags, reflog, merge commits).
   - 11 of 13 single-edit fence mutants survived (`R46W2C1MutFence`) because the refusal set tests known nominal attack shapes rather than exercising the fence's individual defense clauses.
3. **In C3 (`R46W2C3Cases`, `R46W2C3Rerun` / V7):**
   - `plans/round46_c3_verify.py` V7 extracted requirement tags (`both-print`, `toolchain`) from `instruction.md` lines without requiring an executable violating test case. The dry table treated the textual presence of a tag as a requirement, leaving V7 permanently red on the pristine tree and leaving dual-runtime comparison unisolated.
   - The probe tested only the grader's 3 fixed points {42, 10, 0}, leaving $N=1$ untested while claiming general Fibonacci coverage.
   - `wrong-value` builds `/app/polyglot/cmain`, so its re-grade fails on directory listing pollution rather than isolating the calculation mechanism.

---

## 3. Cross-Claim Pattern Taxonomy (3 Patterns)

The wave-2 findings synthesize into **3 recurring cross-claim patterns**:

### Pattern 1: Nominal Token Presence Substituted for Semantic / Structural Invariants (The "Unsubstantiated Token Bypass" Pattern)
- **Sites:**
  - C2: `R46W2C2Bypass` (5 bare errata tokens pass Leg C without corrections).
  - C1: `R46W2C1HoPaths` (argv newline check substituted for repository tree entry filename validation).
  - C3: `R46W2C3Rerun` / `round46_c3_verify.py` V7 (`MAP_ROW` extracts tags from text lines without requiring an executable violating case).
- **Mechanism:** The verifier matches text tokens via regex/substring rather than verifying structural schema (old value, new value, citation) or behavioral execution.

### Pattern 2: Fixed Regression Baselines Substituted for General Decision Boundaries (The "Over-Fitted / Unexercised Boundary" Pattern)
- **Sites:**
  - C1: `R46W2C1HoHonest` (allowlist over-fits 104 legacy fixtures, refusing 9/9 novel benign honest repos).
  - C1: `R46W2C1MutFence` (11 of 13 single-edit fence mutants survive because refusal battery lacks tests for individual fence guards).
  - C3: `R46W2C3Cases` (defect 1: grader's 3 fixed points leave boundary point $N=1$ unexercised).
- **Mechanism:** Positive controls check only a historical regression set; no negative boundary controls exist to prove that individual clauses are necessary or that the decision boundary generalizes.

### Pattern 3: Execution Artifact Collision and Conflated Side-Effect Attribution (The "Conflated Mechanism / Pollution Collision" Pattern)
- **Sites:**
  - C3: `R46W2C3Cases` (defect 3: `wrong-value` compiles `cmain` in run 1; re-grade fails on directory listing pollution rather than calculation error).
  - C1: `R46W2C1HoArgv` (counter marks custom modules `LEAKED` on admission even when `touches=0`).
  - C2: `R46W2C2Entry` (verifying line/word anchor syntax conflated with semantic truth of `teaches` clause).
- **Mechanism:** A macro status (exit code, directory listing failure, admission rollup) is treated as evidence for a specific fine-grained mechanism.

---

## 4. Affected Axes

- **Calibration (C1):** Severely undermined when a decision procedure's advertised boundary contradicts its demonstrated behavior: the fence over-refuses 9/9 novel benign git repositories while 11/13 defense mutants survive without detection.
- **Depth (C2):** Compromised when line-level detail is audited by token presence rather than substantive correctness, allowing evidence-free dummy errata to satisfy the counter.
- **Coverage (C3):** Weakened when requirement tags are declared from prose without isolating test cases, and test artifact side-effects mask whether claimed mechanisms actually fire.

---

## 5. Proposed Move: Prevention Rule for Next Round

To prevent this entire class of nominal proxying across C1, C2, and C3 in future rounds, the lane should adopt one binding rule:

### 5.1 Proposed QUALITY.md Rule (Q41)

Append to `corpus/QUALITY.md`:

```markdown
- **Q41 — a counter, gate or decision procedure that checks a structured section, requirement tag or containment property never validates nominal token or substring presence alone; each verified property must bind to an explicit structural assertion (a non-empty correction with evidence, an isolating violating case, or an invariant checked across all tree entries) and be proved before freeze by a negative control that supplies the nominal tokens without the substantive assertion and fails.**
  Round 46's C2 counter verified `## Errata (round 46)` by string presence of five tokens (`round46_c2_verify.py:183`), allowing an empty dummy list of tokens to pass (`.ufo/waves/round-46/w2/R46W2C2Bypass.md`). The same round's C3 counter declared requirement tags in the dry table without isolating violating cases, failing V7 on the pristine tree; and C1 filtered newlines in `--lane` argv while admitting filenames with embedded newlines in the tree (`R46W2C1HoPaths.md`).
  Check (executable): `python3 plans/token_bypass_check.py --lane .` runs negative controls supplying token-only dummy inputs to each counter leg and asserts that all exit nonzero.
  Shown able to fail: on round-46 C2 Leg C, a dummy errata section passes (`errata_marks=5/5`); with structured item enforcement, it exits 1 (`errata_items_missing=5`).
  Limits: checks structural schema and negative control rejection; does not judge semantic truth of historical prose.
  Lesson: `corpus/lessons/round-46.md` §Mistakes. Supersedes: none; extends Q24 (junk battery), Q27 (mutant kill) and Q36 (backed citation) to structured sections and nominal tags.
```

### 5.2 Complementary SKILL.md Anti-Pattern Line

Append to `SKILL.md` under `## Benchmark anti-patterns`:

```markdown
20. **Token-presence proxying / unverified nominal representation.** Checking that a requirement, defect or constraint is met by asserting that its nominal token or substring appears in the text (e.g. `token in text`, an argv string filter, or a tag without an isolating case). A nominal check passes a hollow shell. Every nominal requirement must bind to an operational or semantic invariant and be proved by a negative control that supplies the token without the substance.
```

---

## 6. Risks & Second-Order Effects

- **Runtime:** Adding negative controls (e.g. testing that a dummy token-only errata section fails) adds <0.5s of execution time per verification run.
- **Contract:** Enforcing structured errata schemas requires entries to use standardized Markdown item formats (`- Erratum (<round>): <mark> — <defective> -> <corrected> (evidence: <path>)`), preventing unparseable prose.
- **Substrate:** Path hygiene checks must traverse repository entries explicitly (`stat` and filename encoding), ensuring that containment holds across the entire filesystem subtree, not just in argv arguments.
- **Verification:** Completely eliminates false-positive passes where hollow shells satisfy the counter.

---

## 7. Verification of Receipts

Empirical receipts gathered during this seat's run and retained in `.ufo/waves/round-46/w2/R46W2Conn/`:
1. `c2-bypass-receipt.txt`: Confirms `dummy_marks: 5/5` and `dummy_bypasses: True` on `round46_c2_verify.py` Leg C logic.
2. `c3-tags-receipt.txt`: Confirms that `both-print` and `toolchain` are unexercised tags lacking violating cases in `polyglot-c-py-dry-cases-freeze.txt`.
3. `c1-newline-and-allowlist-receipt.txt`: Confirms `plans/fixture_fence.py` admits filenames with embedded newlines (`newline_file_final_res: None`) while over-refusing ordinary git operations (`.git/MERGE_RR`, `.git/rr-cache`, `[user]`).

No lane files were modified. No tools were installed. Scratch cleanup was performed via `scratch_guard.py safe-rm`.

---

VERDICT: cross-claim-patterns-3
