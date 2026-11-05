# ReviewerR88a — correctness attack on the R88-C1 counter and probe (read-only)

Item: review `plans/round88_c1_replay.py` (280 ln) and `plans/round88_fixgit_probe.py` (282 ln)
against claims section R88-C1 (`plans/round-88-claims.md`), frozen at `0220c2f9`.

**Grounding.** Instrument bytes verified unchanged between the instrument freeze
`1f267d4b` and measured tip `7fcc680` (`git diff --stat 1f267d4b..7fcc680 -- plans/round88_c1_replay.py
plans/round88_fixgit_probe.py plans/round88-cases.json` → empty). Case table unchanged
`0220c2f9..7fcc680` → empty. Ledger blob at `7fcc680`: fix-git row
`{"status":"executed","round":88,"receipt":"corpus/evidence/round88/fix-git-probe.txt","subject":"tb2-header","verdict":"cases"}`,
`executed_rows=32`; receipt `LANE_TIP da16ec39` verified ancestor of `7fcc680`
(`merge-base --is-ancestor` exit 0). No LSP server is mounted in this session, so caller/definition
checks are by full-file read plus execution experiments (grep as literal fallback only). No tools
installed (operator tooling authorization unused); no network fetches made (all inputs local).

**Experiment harness.** `git clone --no-hardlinks` of the lane into seat scratch; toplevel asserted
equal to the clone dir; counter bytes extracted from the measured tree itself
(`git show 7fcc680:plans/round88_c1_replay.py`). Forged revisions built with plumbing only
(`read-tree` under a private `GIT_INDEX_FILE`, `hash-object -w --stdin`, `update-index --cacheinfo`,
`write-tree`, `commit-tree -p 7fcc680`) — never checkout/stage of the clone worktree, never any
write to the lane. All commands and outputs: `receipts/01-base.out.txt` … `08-forge-dup.out.txt`,
driver `receipts/forge.py`, forged SHAs `receipts/forged-shas.txt`.

## Target 1 — per-leg DEFECT path and forge-satisfiability

Counter file = `plans/round88_c1_replay.py` (`C:`), probe = `plans/round88_fixgit_probe.py` (`P:`).

| Leg | DEFECT emission (path:line, quote) | Satisfiable by a receipt the probe did not produce at the measured tree? |
|---|---|---|
| L1-receipt | C:166 `defect("L1-receipt", f"{RECEIPT} absent at {rev_sha[:12]}")` guarded by C:165 `if receipt_raw is None:` | **Yes.** Existence-only; any blob at the path satisfies. |
| L2-stamp | C:186 `defect("L2-stamp", f"missing {','.join(missing)}")`; C:199 `defect("L2-stamp", f"{key}={stamp.get(key)!r} != measured {value!r}")` over `expect` C:187-197 | **Yes.** Every checked field is a public function of measured tree bytes (`sha256` of capture/table/tool blobs) or literals (`WORKTREE clean`, `EXIT 0`). `HOST_PYTHON/HOST_OPENSSL/COMMAND` are presence-only (C:54-55, never in `expect`). |
| L3-tip | C:206 `defect("L3-tip", f"LANE_TIP {tip!r} does not resolve to a commit")`; C:207-208 `elif not lane.is_ancestor(resolved, rev_sha): defect("L3-tip", ...)` | **Yes.** Any resolvable ancestor commit works; nothing binds the stamp to the true mint point. |
| L4-table | C:160 `defect("L4-table", f"{TABLE} absent at ...")`; C:162 `elif table != frozen_table: defect("L4-table", f"table sha=... != frozen ...")` | Not a receipt property — tree bytes only (full byte equality vs `FREEZE_REV` blob). |
| L5-vectors | C:213 block-absent; C:215-216 `if tuple((c, p) for c, p, _ in observed_cases) != FROZEN:`; C:217-219 per-case `observed != predicted`; C:220-223 summary/predicate; C:224-225 EXIT | **Yes.** The frozen vector is public — the case table itself prints `predicted`, and L5 requires `observed == predicted`, so a hand-written receipt can state it with zero executions. |
| L6-reproduce | C:240-243 `rerun = observation_block(proc.stdout) ... if rerun is None: defect("L6-reproduce", f"probe re-run rc={proc.returncode} ...")` / `elif rerun != observed_block: defect("L6-reproduce", "re-run observation block differs from the receipt")`; C:245 tool-absent | **Content-binding only.** The receipt need not be probe-*produced*; it must equal the probe's deterministic output — which is publicly predictable from the table's predicted vector. So yes, in effect. |
| L7-ledger | C:250 `defect("L7-ledger", f"{LEDGER} has no {MEMBER} row ...")`; C:251-253 tuple mismatch `("executed", 88, RECEIPT, "tb2-header", "cases")` | **Yes.** Editable JSON; no execution check (verified live row matches the tuple exactly). |
| L8-subject | C:154 capture-absent; C:156 `elif sha256(capture) != SUBJECT_SHA: defect("L8-subject", f"sha={sha256(capture)[:16]} != frozen")` | Not a receipt property — tree bytes only (verified: capture at tip hashes to the frozen `a8a6f51e…`). |

Composite answer: **yes — demonstrated.** A receipt minted only from frozen constants plus
`git show <rev>:<path> | sha256sum` (zero probe executions by the forger), committed on top of the
tip, makes the counter exit 0 (Target 4). The only leg that would reject a *wrong* observation is
L6, and L6 binds content, not execution, because the case table's predicted vector *is* the
deterministic observation. This is exactly the frozen honest limit (claims: "L6 reproduces the
observation; it does not authenticate an author"); the attack confirms the limit is real, not wider
in any way that changes a frozen predicate (but see F1 for the L3 widening).

## Target 2 — L6 whole-block line equality

Comparison: C:242-243 `elif rerun != observed_block:` where C:115-121
`observation_block` returns `lines[begin + 1:end]` — the **entire** marker-delimited line list, so
`!=` is Python list equality: count, order, and content, all enforced. The rerun block comes from
the probe executed on `git archive` of the measured rev (C:228-239, `-I -B`, clean env,
`TMPDIR` inside `--work`).

- **Extra CASE line** → the receipt block has 10 lines vs the rerun's 9 → list inequality → `DEFECT L6-reproduce re-run observation block differs from the receipt`. Empirically: `receipts/06-forge-extra.out.txt` exit 1, also `DEFECT L5-vectors case set/predicted differs: [... 'exact', 'exact']` from the ordered-tuple check C:215-216 (9-tuple ≠ 8-tuple FROZEN). TARGET echoed `cases=9 legs=18`.
- **Reordered CASE lines** → element-wise inequality → same L6 defect; L5's tuple check is order-sensitive and also fires. Empirically: `receipts/07-forge-reorder.out.txt` exit 1, `case set/predicted differs: ['exact', 'layout-content-mismatch', 'about-content-mismatch', ...]`.

## Target 3 — L5 frozen tuple in frozen order

Confirmed: C:215-216 compares the **ordered** tuple of `(case_id, predicted)` pairs against
`FROZEN` (C:50-53), identical to the table's order (`exact, about-content-mismatch,
layout-content-mismatch, both-content-mismatch, about-new-absent,
trailing-whitespace-tolerance, about-new-is-dir, layout-old-is-dir`) and to the probe's
`FROZEN_CASES` (P:46-55). **A duplicate case id cannot pass**: it makes the tuple 9 elements (or
displaces a required pair), failing C:215-216, and independently fails L6's list equality.
Empirically: `receipts/08-forge-dup.out.txt` (id `exact` duplicated, summary kept at `cases=8`)
→ `DEFECT L5-vectors` + `DEFECT L6-reproduce`, exit 1. The probe itself also cannot emit
duplicates: `load_inputs` zips table cases against `FROZEN_CASES` in order (P:139-145) and the
sandbox protocol check pins the test order (P:216-221).

## Target 4 — forging a pass without a real grader execution

**Attempt:** "stamp-faithful forgery" — write the receipt by hand from the frozen constants
(`SUBJECT_SHA`), `git show 7fcc680:<path> | sha256sum` for `CASE_TABLE_SHA`/`TOOL_SHA` (72f8ea0c…,
50ae36d6…, both matching the genuine receipt), any ancestor as `LANE_TIP`, `WORKTREE clean`,
`EXIT 0`, and the observation block copied from the table's predicted vector (`observed ==
predicted` for all eight). Commit it on top of the measured tip with plumbing; run the counter.

**Command (excerpt):** `python3 counter_tip.py --lane <clone> --rev aaa796df11682c71324820aaa2b0df22a35e17c2 --work counter-work`
(driver `receipts/forge.py`; blob builder `receipt()` at forge.py:60-84).

**Output (`receipts/03-forge-faithful.out.txt`):**
```
TARGET executed_rows=32 member=fix-git located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0
PREDICATE R88-C1 pass
[exit 0]
```
A second forgery naming the round BASE `801b903a` as `LANE_TIP` also passes
(`receipts/04-forge-oldtip.out.txt`, rev `635b6ae7f55b…`, exit 0) — see F1.

So the honest answer to "is there a way": **yes, and it is the frozen honest limit made
concrete** — no leg is the "sole reason" a forgery fails, because a forgery that states the
correct deterministic block fails nothing. What the legs *do* deliver (verified, not forged):
- Do-nothing control at BASE reproduces the frozen before-figure exactly: `receipts/01-base.out.txt` → `DEFECT L4-table … absent at measured` + `DEFECT L1-receipt … absent` + `DEFECT L7-ledger row {"status":"unexecuted",...}` → `TARGET executed_rows=31 ... defects=3`, `PREDICATE R88-C1 fail`, exit 1.
- Genuine tip measurement reproduces the frozen after-figure: `receipts/02-tip.out.txt` → `defects=0`, exit 0 (its L6 re-ran the probe from the extracted measured tree — 8 bwrap sandboxes — and matched the receipt block, independently re-demonstrating the E/P and P/E classifications).
- Frozen forged-receipt control semantics hold: a real commit that is **not** an ancestor as `LANE_TIP` → `DEFECT L3-tip 7ca19d539764 is not an ancestor of 7d3fa6ddaea6`, `located=0`, exit 1 (`receipts/05-forge-nonancestor.out.txt`, rev `7d3fa6ddaea6…`).

## Target 5 — probe sandbox and staging

**Writable binds:** the only read-write bind in `sandbox_argv` is the case directory:
P:191 `["--bind", str(case_dir / "app"), "/app", ...]`. `/usr` and `/etc` are `--ro-bind`
(P:186); `/bin`, `/sbin`, `/lib`, `/lib64` are recreated as symlinks to the host targets
(P:187-189, inside the new root); `/proc` and `/dev` are fresh API mounts (P:190);
`--clearenv` (P:194) plus `-I -B` (P:196) strip environment and user-site influence;
`--unshare-all` includes the network namespace → the replay is genuinely offline. **Nothing
writable outside the case directory is bound.** (Read-side note N6: host `/etc` is visible
read-only inside the sandbox; the grader only opens `/app` paths.)

**`stage()` cannot escape `/app`:** path validation runs before staging for every table entry —
P:160-161 `if not isinstance(rel, str) or ".." in rel.split("/") or rel.startswith("/"): raise SetupDefect(f"wrong-table path {case_id}:{rel}")` — so no absolute path and no `..` component reaches
P:172-181 (`target = app / rel; target.parent.mkdir(parents=True, exist_ok=True); ... target.mkdir(...)` / `target.write_bytes(...)`). The destination `case_dir/app` is a fresh empty
`TemporaryDirectory` per case (P:203-205), so no pre-existing symlink can be followed; `stage`
itself never creates symlinks. The frozen table (pinned byte-for-byte by L4) contains no escape
shape. Residual edge F2 below (`rel=""`), unreachable at the frozen table.

**`IsADirectoryError` cases really produce E, not F:** the classification is entirely in the
harness — P:69-74 `except (AssertionError, FileNotFoundError) ... "F"` / `except BaseException
... "E"` — and the grader opens files with `open(file_path, "rb")` (capture `hash_file`,
test_outputs.py:9-12). On Linux, `open()` on a directory raises `IsADirectoryError`, an `OSError`
subclass distinct from `FileNotFoundError`, so it falls to the `BaseException` branch → `E`.
For `layout-old-is-dir` the OLD leg path is the directory and `compare_file_hashes` evaluates
`hash_file(path_a)` (the OLD path) first, so the layout leg is E while about stays P → `P/E`;
symmetrically `about-new-is-dir` → `E/P`. Empirical: genuine receipt lines
`CASE about-new-is-dir predicted=E/P observed=E/P` / `CASE layout-old-is-dir predicted=P/E
observed=P/E`, and the counter's L6 rerun at the tip reproduced the block exactly
(`receipts/02-tip.out.txt`).

## Findings

- **F1 — MINOR — L3 accepts any ancestor, wider than the claims sentence.**
  `plans/round88_c1_replay.py:201-208` (`resolves` + `merge-base --is-ancestor`). The claims'
  honest-limit sentence says "a receipt ... whose stamp **names the measured tip** is not
  distinguishable"; in fact a stamp naming **any** resolvable ancestor (demonstrated: the round
  BASE `801b903a`, forge rev `635b6ae7f55b…`) is equally indistinguishable. The frozen control
  (non-ancestor must fail L3) still holds, and no frozen predicate requires the tip to be the
  measured commit, so this widens no gate — but the honest-limit prose understates the forgery
  surface. Show: `python3 <counter> --lane <clone> --rev 635b6ae7f55b8c6c7ccad76820c4a0fa64fa63d0 --work <w>` → exit 0.
- **F2 — MINOR — `stage()` `rel=""` edge crashes outside the documented exit contract.**
  `plans/round88_fixgit_probe.py:160-161` admits `rel=""` (no `..` component, no leading `/`);
  P:174 `target = app / ""` is the `/app` dir itself and P:181 `write_bytes` then raises an
  uncaught `IsADirectoryError` outside `main`'s `SetupDefect` handling → traceback with an exit
  code that is neither 0/1/2. Unreachable at the frozen table (no empty key; bytes pinned by L4)
  and it fails loudly — it cannot fake a pass. Robustness only. Show: run the probe with a table
  whose `files` maps `""` to a string.

Checked-clean (severity NONE, no defect): stamp `HOST_PYTHON/HOST_OPENSSL/COMMAND` presence-only
by design (C:54-55, C:187-197; docstring: COMMAND never executed from the receipt); TARGET
`cases/legs/mismatches` echo the receipt's own numbers when L5/L6 fail (cosmetic; exit is
defect-driven, seen in 06/08); probe branch-name dependence (`lane_tip` reads literal `master`,
P:144-145 — ops note, lane uses master); L4 is full byte-equality against the `FREEZE_REV` blob
(strongest form); `archive.extractall(filter="data")` needs a modern Python (host 3.14.8 ✓);
malformed-ledger JSON at a rev would crash rather than report (unreachable at measured rev);
duplicate stamp keys are first-wins (C:109-111) so a receipt cannot shadow-check itself.

## Residual risk and verification gaps

- The counter cannot, by construction, distinguish a receipt minted at the measured tree from a
  byte-identical forgery minted anywhere else — declared frozen; demonstrated here end-to-end
  (rev `aaa796df1168…`). Location therefore rests on the committer's honesty plus L2/L4/L8 byte
  pins, not on execution evidence.
- I reviewed only the C1 counter and probe (item scope); R88-C2 instruments untouched.
- Experiments ran inside a scratch clone at the measured tree with counter bytes extracted from
  `7fcc680` itself; the lane repository was never written (clone source read + read-only git
  commands only). Scratch tree deleted after copying all receipts into `receipts/`.
- No LSP device available this session; semantic claims above are grounded in full-file reads,
  the quoted lines, and the executed experiments, not in LSP-backed reference/definition checks.
