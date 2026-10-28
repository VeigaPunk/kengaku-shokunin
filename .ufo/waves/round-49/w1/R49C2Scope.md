# R49C2Scope — entry + PROVINCE boundary check against sibling ownership (R49-C2, coverage)

seat: `R49C2Scope` (scout, leaf member, read-only on lane)
round: kengaku 49 (hyaku run 10, attempt 1, wave 1)
date: 2026-10-28
item: check `corpus/knowledge/tb2-polyglot-c-py-grader.md` (the C2 "entry") and the PROVINCE boundary
against sibling ownership; distinguish grader interpretation from benchmark/runtime/model performance.
axes exercised: coverage (entry ground), discernment (boundary split).
REV measured: `9d2900af41e4d1fc6022eff99010436fde6dbd93` (stage-1 freeze; clone-only, no scored counter/probe run — no `MUTANTS`-floored C1 counter and no `--stage-check`-passing C2 probe exists at this tree, so no scored run was made and none was needed for this item).

## Sources opened (URL / access date / located quote ≤25 words)

No external URL was fetched. Opened local lane sources, all at the frozen commit `9d2900a` (byte-identical to
working tree; verified by `git hash-object` vs `git rev-parse 9d2900a:<path>` → EQUAL for every file below):

| file | located quote (≤25 words) | file:line |
|---|---|---|
| `plans/round-49-claims.md` | "the counter's `V7` reports them as a defect" — actually: "Any frozen tag without a committed violating case → C2 not admitted (V7, positively enforced)" | `plans/round-49-claims.md:140` |
| `corpus/lessons/round-48-verifier-spotcheck.md` | "`both-print` and `toolchain` have **NONE** — the V7 defect class is real and unrepaired" | `:40` |
| `corpus/lessons/round-48.md` | "A frozen requirement-tag set with no violating case makes a counter leg unsatisfiable" | `:11` |
| `PROVINCE.md` | "Polyglot construction as a technique, and how an agent should build the file, stay the task's and the authors' business — not this lane's" | `:648` |
| `corpus/knowledge/tb2-polyglot-c-py-grader.md` | "no image run, no agent, no trajectory" | `:191` |
| `plans/polyglot_c_py_probe.py` | "host gcc and host python3 stand in for the image's gcc 13.2.0 / python 3.12.3" | `:49` |
| `plans/pkg-spec-r46.json` | `"entry": "corpus/knowledge/tb2-polyglot-c-py-grader.md"` | `pkg-spec-r46.json` rows field |
| `kasegi-shokunin/PROVINCE.md` | "kengaku — LLM evaluation and benchmarks" | `kasegi PROVINCE.md:50` |
| `tameshi-shokunin/PROVINCE.md` | "Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)" | `tameshi PROVINCE.md:14-17` |

## Commands run (all read-only or in `/fast/scratch/hyaku/kengaku-r49/R49C2Scope`)

- `git clone --shared --no-checkout …/kengaku-shokunin clone && git checkout 9d2900a…` — clone at frozen base;
  `git rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r49/R49C2Scope/clone`.
- `git cat-file -t 9d2900a…` → `commit`; `git show -s` → `2026-10-28 09:14:40 -0300 round-49: stage-1 freeze …`.
  **Stage-1 freeze exists, predates every measurement here.**
- `git hash-object <wt-file>` vs `git rev-parse 9d2900a:<file>` for `plans/round-49-claims.md`, `PROVINCE.md`,
  the entry, `round-48-verifier-spotcheck.md`, `round-48.md` → all **EQUAL** (claims text IS the frozen text).
- `git ls-tree -r HEAD --name-only | grep -E 'polyglot|pkg-spec|order_check|round46_c3_verify|mutants49|round49'`
  → package + instruments present (below); `plans/round49_c2_verify.py`, `plans/pkg-spec-r49.json`,
  `plans/mutants49/plan.json` correctly **absent** at stage-1 (they are stage-2 fills).
- Fleet-wide ownership sweeps from `/home/vgpnk/Projects/shokunin`:
  `grep -rilE 'terminal-bench|polyglot-c-py|tb2' --include='PROVINCE.md' .` → only `kengaku-shokunin/PROVINCE.md`;
  `grep -rinE 'polyglot|fibonacci|C language|compiler|gcc|python semantics' --include='PROVINCE.md' */PROVINCE.md`
  → only kengaku plus `kaidoku` PROVINCE (binary-toolchain context, not C-source semantics);
  `grep -rinE 'model performance|benchmark performance|agent performance|runtime task' --include='PROVINCE.md'`
  → no sibling claims that ground.
- `git show HEAD:.ufo/waves/round-46/w1/R46ScribeC3Entry/tb2-polyglot-c-py-grader.md | sha256sum` →
  `76318ca…` vs committed entry `4c05769…` — scribe draft was amended before landing (expected).

## Findings

### 1. The entry is inside kengaku's own ground — PROVINCE-admitted, not open frontier

`PROVINCE.md:648` (Round-46 paragraph, verbatim at `9d2900a`) names
`knowledge/tb2-polyglot-c-py-grader.md` as the **twelfth** TB2 scoring-code read, and the entry sits in
`corpus/knowledge/` beside exactly 11 other `tb2-*-grader.md` files (count verified). This is the progressive
Core narrowing declared in the round-35→46 paragraphs: each admission names its task and narrows only the
"remaining TB2 tasks" clause. The Frontier item it serves — "agentic benchmark task-spec audits"
(`corpus/README.md:329`) — is the lane's declared frontier ground, and `kasegi PROVINCE.md:50` independently
routes "LLM evaluation and benchmarks" to kengaku. **No sibling claims this ground**: the fleet-wide sweep for
`terminal-bench|polyglot-c-py|tb2` over `PROVINCE.md` returns only kengaku (and two kengaku scratch copies),
and the prior `grep -rl 'terminal-bench\|terminal_bench' */` verification recorded at `PROVINCE.md:353-356`
matched only non-owning kumitate coordinator-topology citations. The class claim ("dual-runtime execution,
agent-authored source file executed by two toolchains") is a lane-internal taxonomy, not an ownership assertion.

### 2. The entry respects the sibling-owned borders the lane pattern fixes

Every sibling owner the round-37/38/39/40 routing paragraphs name is honoured:

| sibling | owns | entry's stance |
|---|---|---|
| `kumitate` | the bounded runner (`cap-run.mjs`, systemd-run+bwrap) | probe *consumes* bwrap; caps/bind policy not re-specified |
| `tameshi` | verifier-fixture/mutation *method* (`mutate-and-run.sh`; read-only probes, never edits a sibling's gate) | V14 mutation battery uses the method; no `tameshi` bytes touched; `plans/pkg_gate.py` stays kengaku's own |
| `chousa` | source-hierarchy/citation method | entry uses their method; no method asserted here |
| `kotoba` | prompt/skill craft | `instruction.md` is read as a requirement source, not a craft rule |
| `kama` | serving plane / endpoint identity | untouched |
| `kake` | web properties | raw.githubusercontent capture only; no web property claim |
| `kaidoku` | ELF/binary linkage (`DT_NEEDED`, dlopen) | untouched — `main.py.c` is source, not a binary; `ldd` absent |
| unowned/integrator | flag-change authority, runtime task validity, deployment config | **refused** by the established paragraph pattern, repeated below |

Round-43 precedent fixes the one new boundary this task raises: **C-and-Python language semantics beyond the
single verdict they decide are unowned** — the r43 grep returned 0 sibling PROVINCEs for `sys.modules|import
system|python semantics`, and this round's sweep returns 0 for `polyglot|fibonacci|C language`. The r46
paragraph already disclaims it: "Polyglot construction as a technique … stay the task's and the authors'
business."

### 3. The interpretation / performance split the entry makes — verified, and it is the correct one

**Grader interpretation (owned):**
- three-move mechanism: `os.listdir` exact-equality on `["main.py.c"]` before the build (`test_outputs.py:17-18`),
  `gcc … -o cmain` into that same directory (`:24`), three fixed stdout comparisons under `check=True` (`:27,31-46`);
- requirement-map labels (`enforced/partly/unenforced`) derived *from the receipt*, not asserted;
- case-table verdicts `observed_pass=7 observed_fail=11`, `regrade=DIFF:F` non-idempotence;
- `Predictor` block — admitted `V11` contract, sourced to `R46ExecC3Counter` (an instrument, not a model claim).

**Benchmark/runtime performance (correctly excluded — the boundary is honest):**
- `tests/test.sh` uv/pytest bootstrap and `/logs/verifier/reward.txt` are **read, not run**
  (`probe:27` "pytest is not invoked; tests/test.sh only wraps pytest"); `test.sh:22-29` quoted but never executed;
- the task image is never pulled (`probe:51`), `Dockerfile`'s `apt install gcc` is not replayed;
- host `gcc`/`python3` stand in for the image's `gcc 13.2.0`/`python 3.12.3` — a **named divergence**
  (`probe:49-50`), so `instruction.md:9` toolchain claims are deliberately unexercised (see §4);
- `task.toml` metadata (900 s timeout, `allow_internet`, image tag) is cited as text, never measured;
- Harbor execution, retry, `/app` restore are explicitly disclaimed (`entry:196`).

**Model/agent performance (correctly excluded):**
- `entry:191` — "no image run, no agent, no trajectory";
- `leftover-cmain` is a constructed end state, not an agent-behaviour claim (`:192`);
- `lookup-table` passing is recorded as *grader mechanics* (three fixed points are public literals), never priced
  as agent exploitability — consistent with the unowned "difficulty/gameability" exclusion in every sibling paragraph;
- `Predictor` predicts the held-out *generator's* shapes, not a model's.

### 4. Boundary hazard the wave's case-author seats must respect (the actionable split)

V7 (`round-49-claims.md:110-116`) requires a violating case for **all 7** tags before scoring. The two
unexercised tags sit exactly on this boundary, and their reachable forms differ:

- **`both-print`** (`instruction.md:7`) — reachable purely by grader interpretation: a case whose end state makes
  the two-runtime output comparison fail is a `both-print` violation (`python-only`, `c-only` already produce
  that end state; a re-tagging of an existing `violates=` token or a one-runtime-silent variant is in-lane).
  **In province.**
- **`toolchain`** (`instruction.md:9`) — the instruction declares *versions* (`python3 3.12.3 and gcc 13.2.0`),
  and the host deliberately stands in for them. A `violates=toolchain` case observable by the grader requires
  either (a) a source that parses under the substituted host toolchain and fails under the declared one — an
  in-lane construct but one that leans on language-semantics facts that are unowned, or (b) a substituted
  PATH/toolchain inside bwrap that makes a "different toolchain" end state — a *runtime* state, still inside the
  case's own sandbox but asserting what the probe itself names a divergence. The probe may NOT pin the image's
  real toolchain (image never pulled, L0 boundary). The C2 case-author seat should satisfy `toolchain` with an
  **interpretation-shaped** case (a source whose leg behaviour flips on a toolchain feature the instruction's
  versions pin), recorded as an end-state violation, never as a claim about the image's installed versions —
  the latter would be benchmark-runtime performance, out of province.

### 5. Write-scope boundary inside wave 1 (sibling seat ownership)

C2 file surface (frozen, `round-49-claims.md:149-153`): `plans/polyglot_c_py_probe.py` (amended),
`plans/round49_c2_verify.py`, `plans/pkg-spec-r49.json`, `plans/mutants49/plan.json`, the round-46 package paths
(new dry table + receipt under `corpus/evidence/round49/`), `plans/order_check.py` **read-only**.
C1's disjoint surface: `plans/fixture_fence.py`, `plans/round49_c1_verify.py`, `plans/honest49|sealed49`,
`plans/mutants49/c1-mutants.json`. **`plans/mutants49/` is the only shared directory** — split by filename
(`plan.json` C2 vs `c1-mutants.json` C1); seats must not touch each other's file. This seat wrote only this
report and its scratch clone.

## Limits

No scored counter or probe run was made (none exists at stage-1 for C2; the `22b7779e` candidate fails
`--stage-check` on this host per `w1/R48C2ExecProbe.md`, and the amended probe is not yet written). Ownership
conclusions rest on fleet PROVINCE.md/SKILL.md sweeps — text-level claims of ownership, not a behavioural audit.
The `toolchain`-tag reachability analysis in §4 is advisory scoping, not a case design.

## Cleanup

`/fast/scratch/hyaku/kengaku-r49/R49C2Scope` held one `clone/` (shared clone of `9d2900a`); all citations above
are lane paths in the wave dir or lane tree. Scratch removed before yield (verified).

## VERDICT

The entry `corpus/knowledge/tb2-polyglot-c-py-grader.md` is inside kengaku's PROVINCE Core (round-46 paragraph,
twelfth of a declared class), no sibling lane claims TB2/polyglot/grader ground, and its interpretation /
runtime / model-performance split is correctly drawn and honoured — the only boundary to police this round is
the `toolchain` tag, which must be violated as a grader-interpretation end state, never as a benchmark-runtime
claim. VERDICT: in-province, boundary holds, one advisory constraint for C2 case authors.
