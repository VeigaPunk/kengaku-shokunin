# R37RevClaims — review of `plans/round-37-claims.md` (kengaku round 37, wave 1)

Reviewer seat R37RevClaims, 2026-10-26. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Freeze commit `ca790460e9b74d4dc5870c878affd13cc9c4437a`; recorded probe run `5c7b34e9223f460a440596e3a76bdae8bfdd37d8`.

Method: read the frozen claims in full; both counters, `plans/pkg_gate.py`, `plans/git_webserver_probe.py`, `plans/tb2_grader_probe.py` and `plans/round36_c1_verify.py` (helpers) in full; the six controls, `frozen-digests.txt`, `census-before.txt`, `measure-before-committed.txt`; the captures `verify.sh`/`test_outputs.py`/`instruction.md`; `SCORECARD.md:564`, `corpus/QUALITY.md:299-303`, `corpus/lessons/round-36-verifier-spotcheck.md` §5. Mechanically diffed the predicate sentences; measured the P10/uv path and the `__pycache__` trap on scratch fixtures (receipts in `build/R37RevClaims/`). No lane file written; no git mutation in the lane.

## 1. Predicate sentence identity — plan ↔ code ↔ receipt label

- Mechanical normalized-whitespace diff: C1 plan block (`plans/round-37-claims.md:38-41`) == `plans/round37_c1_verify.py:5-10` docstring block → `True`; C2 plan (`plans/round-37-claims.md:85-86`) == `plans/round37_c2_verify.py:5-7` → `True`. Same sentence, verbatim.
- Code is consistent with the printed sentence: C1's accept condition (`round37_c1_verify.py:386-389`) requires `not dev and gate_ok and len(MUTANTS)==TOTAL and wrong==0 and disagree==0 and killed==TOTAL and survived==0 and invalid==0 and null_detected==0`; `total` prints `len(MUTANTS)`, so `killed==TOTAL(55)` ⇔ the printed `killed=55`. C2: `defects==0` ⇔ `checks=7 defects=0` (7 = `len(checks)`, hardcoded list, `round37_c2_verify.py:216-223`).
- Receipt label: both docstrings mandate "same sentence in plans/round-37-claims.md and in the receipt label" (`round37_c1_verify.py:5`, `round37_c2_verify.py:5`); the landing receipt is the L1's to write. Sibling draft receipts already carry the exact strings: `.ufo/waves/round-37/build/R37PkgDraft/c2-final.txt:20` `PREDICATE C2 pass`; `.ufo/waves/round-37/build/R37TipSweep/receipts/summary.tsv:22,25`. No mismatch found.
- Exit-code contract coherent across all three: the counter keeps non-0/1 gate exit codes as results (`round37_c1_verify.py:258-268`, timeout → `"timeout"`), matching the plan's "(exit code, set of clause ids printing `DEFECT`)" (claims:36-37) and the gate's "an unexpected crash never maps onto 0 or 1" (`pkg_gate.py:8`).

## 2. False green — can a check pass on a state that does not deliver the claimed surface?

- **C1: no false green found.** All 55 mutants are pure relaxations (`return True` / `pass` / dropped conjunct — `round37_c1_verify.py:53-123`), so a kill requires the silenced branch's verdict to have been load-bearing on some fixture — exactly the claimed demonstration. A battery37 fixture cannot escape the declaration requirement: `battery37_fixtures` overwrites `r36` to `False` (`:266`), and a battery37 fixture with `defects: None` is counted wrong (`:325-328`). The gate digest is enforced in the accept condition (`gate_ok`), and mutants go invalid when the gate is not at the freeze digest.
- **C2: the receipt's authenticity rests solely on V2's P10 byte-equality — the chain is closed.** V4 alone accepts a hand-typed receipt (demonstrated: `control-c2-skip.txt` passes V4 and V7 on a hand-typed receipt; only V2 reds). The counter docstring states this ("authenticity rests on P10", `round37_c2_verify.py:11-13`). Verified closed: the fresh probe reads the same captures V1 pins; the probe output is deterministic (receipt's second run byte-equal; `P10 ok probe_rerun=byte-equal bytes=8443` in `measure-before-committed.txt` and `R37PkgDraft/c2-final.txt`).
- **FG-1 (residual, counted):** the entry's prose outside the requirement map and the quote rows is unchecked — V1–V7 can all pass while prose claims are false. The gate disclaims it ("Not a truth check on prose that parses", `SCORECARD.md:564`) and the claims cite that row as the advertised surface, but the claims' own C2 limit (claims:96-97) names only the probe's limits (no oracle, no real push), not the prose limit. Bounded by V7 (map labels tied to executed verdicts), V4 (mismatch cases named) and P4 (quotes verbatim).
- Wording notes (not counted): (a) the goal says "SINGLE-DEFECT fixtures" but neither the claims nor the counter enforces single-defect — the counter enforces the exact declared set (`:325-328`), so a multi-defect fixture would pass; the frozen predicate, not the goal phrasing, is the contract. (b) "Neither counter reads the other's work product" (claims:106) is imprecise — C1's genuine fixture copies `corpus/knowledge/*.md` (C2's entry when landed) via `copy_package` (`round36_c1_verify.py:55-70`); the same paragraph (claims:103-105) discloses exactly this coupling, so the framing self-corrects.

## 3. False red — can a truthful landing fail?

- **FR-1 (concrete, measured, counted — headline): a `--rerun` battery fixture is poisoned by `__pycache__` unless it stages a `.gitignore`.** The r35 probe imports the captured grader from the fixture tree (`tb2_grader_probe.py:121` `spec.loader.exec_module(mod)`; no `dont_write_bytecode`/`PYTHONDONTWRITEBYTECODE` anywhere in the probe), which writes `corpus/evidence/round35/tb2-eval/__pycache__/` into the fixture dir during P10 — after P9 has already run in that gate invocation (`pkg_gate.py:305-308`, P9 before P10). Measured on a scratch fixture (genuine r35 package, `--require-clean-tree --rerun`; receipts in `build/R37RevClaims/`):
  - run 1 (reference): `P9 ok untracked=0` … `P10 ok probe_rerun=byte-equal bytes=3399`, `defects=0` (`rerun-pycache-run1.txt`).
  - run 2 on the SAME dir — exactly what the counter's null pass (`:355`) and every mutant pass re-run: `P9 DEFECT untracked=1 first=corpus/evidence/round35/tb2-eval/__pycache__/test_outputs.cpython-313.pyc`, `defects=1` (`rerun-pycache-run2.txt`).
  - the renamed pass copies the polluted dir (`shutil.copytree(d, nd, symlinks=True)`, `:340`) → `renamed_disagree ≥ 1` as well.
  - Consequence: any `--rerun` fixture whose declared set lacks P9 makes C1 unreachable (`null_detected`/`renamed_disagree ≥ 1`) — and a `--rerun` fixture is REQUIRED to kill M41–M43 (P10 only runs with `--rerun`). Neither the claims' excluded-branch list (claims:53-58) nor the goal's fixture API names this.
  - Verified fix, inside the fixture API: stage `.gitignore` containing `__pycache__/` and `git add` it — two consecutive gate runs then both print `P9 ok … P10 ok … defects=0` (`rerun-pycache-mitigated.txt`). (Alternative: declare P9 in the fixture's defect set with a real untracked file present from the start.) The lane already knows the pattern — `copy_package` ignores `__pycache__` when copying captures (`round36_c1_verify.py:62`).
- **FR-2 (counted): the knowledge/README parity coupling is global; Separability discloses only the C2-entry direction.** P8 compares ALL knowledge file names to ALL README index rows (`pkg_gate.py:252-256`, `files != indexed`). So (i) C1's genuine accept fixture reds on ANY seat's half-landed entry — the claims disclose this only for C2's entry (claims:103-106, accurate as far as it goes) — and (ii) C2's own V2 reds on another seat's half-landed entry even though C2's surface is complete: a false red for C2 that Separability does not mention. Landing entry+index row together is the L1's integration control; the claims should state the coupling is global.
- **FR-3 (measured non-issue here, residual): P10's interpreter choice is host-bound.** Host has no Bio (`python3 -c "import Bio"` → ModuleNotFoundError), has uv (`/home/vgpnk/.local/bin/uv`) and bwrap (`/usr/bin/bwrap`); the gate's uv fallback ran the probe successfully — byte-equal at control time (`control-c2-skip.txt` P10 reached the byte-compare), in `measure-before-committed.txt` (`bytes=8443`) and in my runs (`bytes=3399`, r35 receipt). Residual: the uv path needs the `biopython==1.85` wheel cached or network (`pkg_gate.py:276`); and the r35 receipt's first line embeds `biopython=1.85` (`tb2_grader_probe.py:150` prints `Bio.__version__`; receipt line 1 confirms) — a host that later gains a different host-Bio flips the path and breaks byte-equality. Worth one disclosure line.
- **FR-4 (protocol, disclosed by the predicate itself):** V2's P9 runs against `--root str(lane)` (`round37_c2_verify.py:91-93`) — on the WORKING lane this wave's own untracked `build/` files would red P9 (`.gitignore` lists only `.ufo/interactive-sessions/` and `__pycache__/`). The predicate mandates a clean clone, which excludes them by construction. Operational caveat only.
- **FR-5 (disclosed, verified):** half-landed C2 → C1 `wrong=1`. P8's parity logic verified; "a half-landed C2 would show up as a wrong declaration in C1, not as a kill" (claims:105-106) is accurate.
- C1's own lane-side `__pycache__` (importlib load of round36/battery37 modules) is gitignored → no P9 impact on the lane; measured: `measure-before-committed.txt` runs C1 then C2 in one clone and C2's `P9 ok untracked=0`.

## 4. Disclosure of the control-time probe run — adequate

- The disclosure (claims:6-9) verified against code: `c_rerun` captures the fresh output (`capture_output=True`, `pkg_gate.py:278`) and on mismatch returns only the fixed message "fresh probe output is not byte-equal to the receipt" — the output is never printed or written; `control-c2-skip.txt` shows only the clause line. The only mechanical channel from that run to the frozen predictions or the receipt is foreclosed.
- Ordering verified: the dry table (predictions) and the probe are in the freeze commit (`frozen-digests.txt` lists both digests; current files match — `sha256sum` this session); the recorded run `5c7b34e` postdates the freeze (`git log --oneline` order: `44b7298` → `5c7b34e` → `ca79046`); baseline tip `3ea9a1d` is an ancestor of the freeze (`git merge-base --is-ancestor` → yes).
- Smoke-test claim verified in code: `--smoke` runs an inline curl script; the grader HARNESS is unused (`git_webserver_probe.py:283-291`) — "the grader was not imported" holds.
- "No verdict was printed or read": printed — verified in code; read — human assertion, unverifiable, but no artifact carries the fresh output.

## 5. Excluded branches — could the battery reach any?

All five exclusions (claims:53-58) hold under the fixed spec:

1. **P1 empty-`frozen_instruments`:** r35 spec pins 3 instruments, r37 pins 2 — never empty; the counter's `--spec` is fixed (`run_gate` appends it; fixtures may not pass `--spec`, `:317-319`). Unreachable.
2. **`spec not found` / `root not a directory`** (`pkg_gate.py:374-379`): reachable only by a fixture returning a bogus `--root`; the result `(2, ∅)` matches no accept/reject declaration (`wrong=1`) and no mutant touches the early path — cannot kill, harmless.
3. **P10 `OSError`/`SubprocessError`** (`pkg_gate.py:279-280`): needs uv missing (present, measured) or a 600 s probe — the r35 probe is 18 in-memory cases (seconds; byte-equal re-runs measured), the r37 probe is 22 bwrap cases (~1–2 min; `P10 ok bytes=8443`). Unreachable.
4. **`run_checks` clause-crash handler** (`pkg_gate.py:297-300`): I attempted to reach it — missing capture dir, unreadable files, odd encodings all land in `read()`'s OSError guard or early returns before a clause can raise; `Package.load` crashes land in main's exit-2 handler, which no mutant touches. The claims' "no clause crash is known to be reachable with the fixed spec" held under these attempts.
5. **`--require-clean-tree`/`--rerun` gating** (`pkg_gate.py:305-308`): plumbing; the battery reaches P9/P10 THROUGH the flags (that is how M40 and M41–M43 get killed) — the exclusion covers only the conditional-inclusion logic. Correctly framed.

## 6. Numbers cross-check (claims vs controls and captures)

| claims sentence | command/source | observed |
|---|---|---|
| Before: `fixtures=14 wrong=0 renamed_disagree=0`, `killed=5 survived=50`, fail, exit 1 (claims:42-45) | `control-c1-nothing.txt` | identical; killed = M01 M05 M40 M47 M54 (matches claims:46-48) |
| example control kills M08 only (claims:49-51) | `control-c1-example.txt:26,74` | `M08 P3 killed by=ex-p3-two-word-quote`; `killed=6` |
| gate-edited → `invalid=55` (claims:50-51) | `control-c1-gate-edited.txt` | `invalid=55` |
| mislabel → `wrong=1` (claims:51-52) | `control-c1-mislabel.txt` | `wrong=1`, killed=5 |
| C2 before `defects=4` (V2,V3,V4,V7) (claims:88-89) | `control-c2-nothing.txt` | identical, exit 1 |
| skip-control → V2 red only (claims:90-94) | `control-c2-skip.txt` | `defects=1`; gate `P3 … out_of_word_range=8`, `P6 … teaches words=1`, `P10 … not byte-equal`; V3/V4/V7 ok |
| census before: exit 0, 15 W04 (claims:110) | `census-before.txt` | identical |
| receipt `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | `git-webserver-probe.txt` tail vs `git-webserver-dry-cases-freeze.txt` tail | `predicted_pass=9 predicted_fail=13`; 22 CASE ids in the same order |
| headline observations (goal/claims) | captured bytes | `verify.sh:49` `./git_test.exp` with no status read; `:57` `curl -s -o /dev/null -w "%{http_code}"` (no `-L`, no `--max-time`), `:60` second `curl -s`; `:62` `echo "Content: $CONTENT"`; `test_outputs.py:13` `assert "TEST PASSED" in result.stdout`; `:60` substitution strips trailing newlines, `:63` exact compare — capitalised/leading-space/trailing-space/crlf/bom all `observed=fail` |
| V7 coverage 1-9 complete | `wc -l instruction.md` → 10 (9 content lines + trailing blank) | complete |
| frozen digests unchanged | `sha256sum` + `git diff ca79046 HEAD --stat` over the frozen files | all equal `frozen-digests.txt`; diff empty; claims file last touched at `ca79046` |
| L0 cap, planned row, routed items, assimilation candidate | `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:163`; `SCORECARD.md` `### Planned (round 37)`; spotcheck §5 items 1-3; `considerthese/2026-10-25.md:43` | all present and matching the claims' citations |

Advertisement caveat: P7's provenance fields and P8's index checks are advertised only generically ("entry", "SOURCES rows" in `SCORECARD.md:564`; the gate docstring (`pkg_gate.py:10-13`) names four example defects). The operative count is branch-level — the 55 frozen mutants — which is what the counter measures; the "advertised" framing is motivational, not the unit of count.

## Residual risk and verification gaps

- I did not run either counter end-to-end in full mode (a full C1 run with `--rerun` fixtures re-runs the probe inside every surviving-mutant loop; the measured gate runs above cover the mechanisms). The L1's landing measurement is the canonical run.
- Operability: with k `--rerun` fixtures, each surviving mutant's `differs` loop costs up to k probe runs — bounded but noticeable; the `.gitignore` mitigation does not remove the per-invocation probe cost.
- The counter's `--work` does not constrain the probe's scratch inside V2/P10 (the gate subprocess inherits the ambient TMPDIR; the probe cleans up after itself) — hygiene nit.
- V7 accepts any `instruction.md:<n>[-<m>]` range without checking it against the actual instruction length — moot here (9 content lines, 1-9 required), but an overlong row would silently extend "coverage".

Report receipts: `build/R37RevClaims/rerun-pycache-run1.txt`, `rerun-pycache-run2.txt`, `rerun-pycache-mitigated.txt` (scratch `/fast/scratch/hyaku/kengaku-r37/R37RevClaims` removed).

VERDICT: claims-review-1-false-green-2-false-red
