# FGateQ15 — Q15 tree-inventory selftest review

Identity: `KengakuR27.FGateQ15`, **not** candidate writer `KengakuR27`. Axes: novelty → canonical coverage/constructs (no score judgment); calibration/Q15 authority and detector coverage (no score adjustment).
Entry reread: whole `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`; proposed canonical path `corpus/knowledge/extraction-policy-comparison.md`. It remains a draft; this is not an admission verdict.
Observed base: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`. Clone command `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FGateQ15 && git -C /tmp/kengaku-r27-FGateQ15 switch -c r27-FGateQ15 b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FGateQ15 rev-parse HEAD` → exit 0; observed HEAD matches the pinned base.

## Findings (severity order)

### MEDIUM — selftest passes when commit-tree parsing stops after one entry

`parse_tree` is intended to consume every `ls-tree` line (`plans/gate_timing_check.py:420-435`); `main` uses that map for both admission evidence and total report count (`:768-810`). The fixture creates only a registry and one cited report under the wave tree (`:497-498`), and asserts only inventory 0 then 1 (`:572-579`). It therefore does not establish traversal completeness.

Exact mutant: in the private clone only, inserted `break` immediately after `files[path] = TreeFile(...)` at `plans/gate_timing_check.py:434`. `cd /tmp/kengaku-r27-FGateQ15 && PYTHONDONTWRITEBYTECODE=1 python3 plans/gate_timing_check.py --selftest` → **exit 0**; early commit remained `exit=1`, `second-seat-reports=0`; late commit remained `exit=0`, `second-seat-reports=1`; selftest printed `ALL PASS`. This is a false-green for the traversal regression.

Impact demonstrated against the real round-26 tree: the same mutant run with `--lesson corpus/lessons/round-26.md --commit b5f62e5e637b34a1549e3475fc58b4227ed87e5a --repo /tmp/kengaku-r27-FGateQ15` → exit 1 and `second-seat-reports=0`; the three cited reports were all incorrectly reported absent. Restored source on the same tree → exit 0, three cited reports found, `second-seat-reports=53`. This is fail-closed for admission, but silently green selftest does not protect Q15's total-inventory/diagnostic contract and the regression can false-reject a real admission.

### MEDIUM — caller `GIT_INDEX_FILE` escapes the temporary-repository write boundary

Normal Git write calls are directed to the `TemporaryDirectory` repo (`plans/gate_timing_check.py:481-489,491-546`), but `run_git` does not pass a sanitized `env` (`:409-417`) and `check()` copies all caller environment variables (`:527-541`). In a scratch probe, copied the pristine checker to `/tmp/gtc-probe/gtc.py`, then ran `GIT_INDEX_FILE=/tmp/gtc-probe/esc-index PYTHONDONTWRITEBYTECODE=1 python3 /tmp/gtc-probe/gtc.py --selftest` → **exit 0**; `stat -c 'size=%s mode=%a path=%n' /tmp/gtc-probe/esc-index` reported `size=710 mode=644`. Thus Git wrote an index outside the selftest's temporary repository while the selftest passed. A caller that points `GIT_INDEX_FILE` at an existing index risks modifying it [INFERENCE]. A clean `env -i` run also passed (exit 0); the confinement is environment-dependent, not unconditional.

## Q15 checks and bounded verification

- Q15's explicit worktree-inventory mutant is covered by the retained fixture: `plans/fixtures/r27/gate-timing-worktree-mutant.txt:1-22` records mutant selftest exit 1 because early inventory becomes 1; `...worktree-restored.txt:1-21` records restored exit 0 with early 0/later 1. This satisfies that specific Q15 mutation criterion; it does not catch the truncated traversal above. Rubric: `corpus/QUALITY.md:123-130`.
- Pristine and restored `--selftest` each exited 0. The fixture output was early `exit=1`/inventory 0, later `exit=0`/inventory 1. It checks `early_lesson == late_lesson == lesson_text` (`plans/gate_timing_check.py:555-581`), so the timing pair compares identical lesson content.
- Real report-tree support on restored checker: `--lesson corpus/lessons/round-26.md --commit b5f62e5e637b34a1549e3475fc58b4227ed87e5a --repo /tmp/kengaku-r27-FGateQ15` → exit 0, `passed=1 failed=0 second-seat-reports=53`.
- One alternate mutant: changed `ls-tree -rl` to `ls-tree -r` at `:768` in the clone. Same `--selftest` → exit 1; late expected exit 0 but got 1, and expected inventory 1 but got 0. Mutant killed. Restored the source; SHA-256 `7c8b498ea501a1d4ec67283d51ac0a0d7d57a293e3180a85218dbd2930f284f1`; restored selftest exit 0.
- LSP status/definition/references/diagnostics unavailable: `read xd://lsp` returned “No such tool” and the mounted-tool list contained no LSP device. `grep -n` was used only for source line anchors, not as semantic proof.

Residual risk: caller-environment testing covered `GIT_INDEX_FILE`, not every Git environment/config/template/hook override. No lane Git/jj/index mutations, builds, lint, formatter, model/endpoint calls, or installs/updates were made; all mutations/probes stayed in `/tmp` and this report is the only lane write.

VERDICT: **RECOMMEND HOLD on treating Q15 as complete without a traversal-completeness check and isolated Git environment.** The specifically required worktree mutant is killed; the observed truncation mutant survives green, and an exported `GIT_INDEX_FILE` redirects selftest writes.

Installs/updates: none.

## Follow-up 2026-10-21 — v2 checker (`be03e881c421af3fd000b61c9ce13c00db8800199171ba8e78f9e92fd23b641c`)

Same identity (`KengakuR27.FGateQ15`, not candidate writer `KengakuR27`); no lane edit — live `plans/gate_timing_check.py` (885 lines, SHA `be03e881…641c`) copied read-only to `/tmp/gtc-probe/gtc_v2.py`; all runs below on that copy. Read v2 in full at the delta (`:409-435` run_git/parse_tree unchanged; `:479-659` rebuilt selftest). L1 receipts present: `plans/fixtures/r27/gate-timing-parse-tree-mutant.txt`, `gate-timing-v2-worktree-mutant.txt`, `gate-timing-v2-worktree-restored.txt` (old one-report receipts preserved).

- Finding 1 (traversal-stop false pass) **CLOSED**. My exact mutant re-applied to the v2 copy (`break` after `files[path] = TreeFile(...)`): mutant SHA `1674da1a877eb89f2e2f69339e8bdd63f726908e839fa3d0fec0fb66dc357da4` — byte-identical to L1's retained receipt. `python3 /tmp/gtc-probe/gtc_v2_mutA.py --selftest` → exit 1: `selftest: later commit expected exit 0, got 1` and `expected second-seat-reports=2, got 1`. The early0/late2 fixture now kills truncation.
- Finding 2 (GIT_INDEX_FILE escape) **CLOSED**. Re-run: `GIT_INDEX_FILE=/tmp/gtc-probe/esc-index2 PYTHONDONTWRITEBYTECODE=1 python3 /tmp/gtc-probe/gtc_v2.py --selftest` → exit 0 and `esc-index2` never created; selftest printed the isolated-environment lines (`caller index untouched; hostile GIT_DIR/WORK_TREE/object/config/template/hooks did not escape`). Extra probe: exported `GIT_DIR` at a fresh bare victim repo → selftest exit 0, victim gained 0 commits, tree listing hash unchanged. Clean `env -i` selftest → exit 0.
- Alternate mutant (`ls-tree -rl` → `-r`) re-run on v2 → exit 1, `expected second-seat-reports=2, got 0` — still killed.
- Pristine v2 selftest (clean env and hostile-env runs) → exit 0 both; `ALL PASS … working-copy inventory, tree truncation, and hostile Git environment controls red`.

Remaining residual (new, scoped): production `run_git` (`:409-417`, unchanged) still inherits the caller environment in non-selftest grading runs; under an exported `GIT_DIR`/`GIT_OBJECT_DIRECTORY`, `git -C <repo> show|ls-tree` could read a different repository than `--repo` names. Read-only operations only (no write escape; index untouched), so it cannot mutate caller Git state, but the graded tree could be silently wrong. Not one of my two assigned findings; left for L1 judgment.

VERDICT: **Both FGateQ15 findings closed by v2 — traversal truncation and the GIT_INDEX_FILE escape are now caught by the permanent selftest, independently re-run on the live bytes; one read-only residual (production-path env inheritance) remains disclosed.**

Installs/updates: none.

## Follow-up 2 2026-10-21 — v3 checker (`51c18a9edfecba9cb6e15449b8063668f41225e98347c6221c6df7c2b0b80a2a`, 940 lines)

Same identity (`KengakuR27.FGateQ15`, not candidate writer `KengakuR27`); no lane edit. Live file copied read-only to `/tmp/gtc-probe/gtc_v3.py` (hash matches). Diff v2→v3 reviewed: new `isolated_git_environment()` (PATH/TMPDIR/TEMP/TMP/LANG/LC_ALL + `PYTHONDONTWRITEBYTECODE` + `GIT_CONFIG_NOSYSTEM=1` + `GIT_CONFIG_GLOBAL=/dev/null`) passed by production `run_git`; selftest adds hostile `GIT_DIR`+`GIT_OBJECT_DIRECTORY` checker runs with fresh-bare-victim and object-sentinel snapshots. v3 receipts present: `plans/fixtures/r27/gate-timing-v3-{repo-env-mutant,traversal-mutant,worktree-mutant,restored}.txt`; v1/v2 receipts preserved.

- Residual (production env inheritance) **CLOSED, actual run**: `GIT_DIR=/tmp/gtc-probe/victim3.git GIT_OBJECT_DIRECTORY=/tmp/gtc-probe/objdir3 python3 /tmp/gtc-probe/gtc_v3.py --lesson corpus/lessons/round-26.md --commit b5f62e5e637b34a1549e3475fc58b4227ed87e5a --repo /tmp/kengaku-r27-FGateQ15` → exit 0, `passed=1 failed=0 second-seat-reports=53`, all three Fx*.md cited reports found from the requested clone; victim repo file-snapshot hash, object-dir listing, and `count-objects -v` all unchanged before/after.
- 2-case timing fixture still green: v3 `--selftest` with the same hostile exports → exit 0, `ALL PASS (… worktree/parser/run_git mutants red; caller index and fresh bare victim unchanged)`, including the new `production run_git ignores caller GIT_DIR/object directory` line.
- Both prior mutants re-run on v3 copies: traversal `break` → exit 1 (now caught in both normal and hostile late checks: `second-seat-reports=2, got 1`); alternate `ls-tree -rl`→`-r` → exit 1 (`got 0`). Scratch copy hash unchanged after runs.

VERDICT: **All three FGateQ15 findings closed on v3 (`51c18a9e…80a2a`) — Q15 tree authority survives truncated traversal, worktree substitution, and inherited Git selectors in both the permanent selftest and an actual round-26 grading run; no remaining FGateQ15 defect.**

Installs/updates: none.
