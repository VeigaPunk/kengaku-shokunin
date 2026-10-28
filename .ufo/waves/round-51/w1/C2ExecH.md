# C2ExecH — round 51 executor: attribution of `corpus/routed-findings.jsonl` rows 64–71

Seat: `C2ExecH` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Round 51 / hyaku run 11, one v2 build-and-attack wave.

**Axes named.** Judged axis: **adjacency** (R51-C2, 8→9). **Freshness** (R51-C1) is untouched by this
seat: no `PROVINCE.md`, no `plans/round51_surfaces.py`, no `plans/round51-surfaces.json` read or written.
One axis moved, no axis harmed.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7 (lane tip measured; stage-1 freeze
`e07f131cf7037e58a21db6e1f3986cf401ad257c` verified as an ancestor:
`git merge-base --is-ancestor e07f131… HEAD` → exit 0)

## Deliverable

`.ufo/waves/round-51/w1/C2ExecH.jsonl` — 8 complete row objects, one per line, emitted in the counter's
`FIELDS` order (`id, class, source, opened_round, status, owner, disposition, close, blocker, check, note`).
**Every original field value is preserved** (asserted in the builder: `close unchanged for all: True`);
the only field values I set are `owner`, `disposition`, and `check` (four empty checks authored, four
pre-existing checks re-rooted — see the cwd finding below).

Rows 1–63 of the ledger are owned by sibling fragments `C2ExecA…C2ExecG.jsonl` (9 rows each, disjoint;
verified: no id overlap with this seat).

## What the eight rows are

Rows 64–71 (0-based 63..70) are the sub-items of §5 of
`corpus/lessons/round-45-verifier-spotcheck.md` — the round-45 non-author closure's routed defects.
Source-line audit (the round-50 §6 **D5** class this round answers): each pointer's line carries the
item it names.

| row | source | text at that pointer (verbatim excerpt) |
|---|---|---|
| R45-S5-4 | `round-45-verifier-spotcheck.md:150` | `4. Lesson Gate: record the ≤25-word quote + location per new row (D2).` |
| R45-S5-5 | `:151` | `5. Receipts name the revision measured inside the receipt bytes (D3); run the frozen counters at the tip that ships the report.` |
| R45-S5-6 | `:152` | `6. Name every post-freeze claims-file edit (\`52d7486\`) in the amendment paragraph (D4).` |
| R45-S5-7a | `:153` | `7. Carried, lane-owned: re-freeze the C1 counter under Q39 with the held-out modules as frozen refusals;` |
| R45-S5-7b | `:154` | `` `R45CritV11Bypass` lookup predictors; `` |
| R45-S5-7c | `:154` | `` `R45SentC2Grader` F1 (P10 unpinned `uv` fetch) and F2/F3 (P9); `` |
| R45-S5-7d | `:155` | `` `R45CritIntent` / brace-prefix bypass; `` |
| R45-S5-7e | `:155` | `re-attack the two unattacked mutation items (D5).` |

**Owner evidence, one rule for all eight** (not invented per row): the source sentence itself says
**"Carried, lane-owned"**, and the lane's `SKILL.md:3` sibling arbitration assigns `kotoba` prompt/skill
craft, `kumitate` OMP route resolution, `kama` endpoint health, `chousa` research method, `tameshi`
verification-**fixture** craft — none of which covers kengaku's own lesson gate, receipts, claims file,
C1 counter, V11 predictor, `pkg_gate.py` or mutation seats. `kengaku` is declared in
`/home/vgpnk/Projects/shokunin/shokunin.conf` (`kengaku|kengaku-shokunin|novelty + calibration`).
No row here is cross-lane evidence, so **none is `routed`/`referral`** and no `next` field is emitted.

## Summary table

| row | class | status | owner | disposition | check | exit in scratch cwd |
|---|---|---|---|---|---|---|
| R45-S5-4 | gate-without-row-quotes | closed | kengaku | fixed-verified | `cd "${LANE:?}" && grep -q 'S166' corpus/lessons/round-46.md` | **0** |
| R45-S5-5 | receipt-without-revision | closed | kengaku | fixed-verified | `cd "${LANE:?}" && grep -q 'lane commit' .ufo/waves/round-46/integrate/c2-landing.txt` | **0** |
| R45-S5-6 | claims-edit-unnamed | closed | kengaku | fixed-verified | `cd "${LANE:?}" && grep -q 'cf7de6af' plans/round-46-claims.md` | **0** |
| R45-S5-7a | c1-refreeze-keyed-control | closed | kengaku | fixed-verified | `cd "${LANE:?}" && test -f .ufo/waves/round-46/claims/control-c1-fence-keyed_name.txt` | **0** |
| R45-S5-7b | v11-lookup-predictors | open | kengaku | fixed-verified | authored: `plans/round46_c3_verify.py` `lint_block` on a dict-table predictor | **0** |
| R45-S5-7c | gate-p10-unpinned-uv | open | kengaku | accepted-risk | authored: `grep` the bare-`uv` fetch in `plans/pkg_gate.py` | **0** |
| R45-S5-7d | intent-brace-prefix | open | kengaku | fixed-verified | authored: `_argv` refuses a brace placeholder on `--evidence-ref` | **0** |
| R45-S5-7e | unattacked-mutation-items | open | kengaku | accepted-risk | authored: successor mutation receipts exist | **0** |

Counter run over the spliced ledger: `VERIFIED ran=6 passed=6 failed=0`, `NEXT violations=0`,
`SOURCES resolved=71 missing=0`, and **zero `DETAIL` lines name any of the eight rows**.

## Per-row evidence

### R45-S5-4 — fixed-verified
Fix artifact: `corpus/lessons/round-46.md:23` `## Gate`, table header at `:28`
`| candidate | verdict | reason + flip | URL | accessed | located quote |`, S166 at `:32`
(`` `:27 "test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]"` ``). The lesson's rule line
(`round-46.md:13`) states exactly the requirement the round-45 gate lacked:
`Each admit row carries \`<file>:<N> "<quote>" (<K> words)\``.

### R45-S5-5 — fixed-verified
`sed -n '1p' .ufo/waves/round-46/integrate/c2-landing.txt`:
`# C2 frozen counter at lane commit e9d201455c3774921aa5dfc287f07b4b9f113e76 (clean --no-local clone), L1 KengakuR46`.
The row's `close` is left **verbatim** (`round-46 integrate receipts open with the measured lane
commit (.ufo/waves/round-46/integrate/*.txt)`). Note for the L1: that `close`'s first token `round-46` is
not a resolvable path, so the row could never be `fixed-historical` under the frozen predicate without a
pointer repair; as `fixed-verified` it is not checked and the pointer stays untouched.

### R45-S5-6 — fixed-verified
`plans/round-46-claims.md:131`: `**Stage 2 (declared at stage 1; instruments commit
\`cf7de6af112e5d491ebd47318682b05fe864c125\`, 2026-10-27, before any`.

### R45-S5-7a — fixed-verified
`plans/round46_c1_verify.py` exists; the cited control receipt
`.ufo/waves/round-46/claims/control-c1-fence-keyed_name.txt` exists; the cited commit resolves:
`git cat-file -e 7768716c^{commit}` → exit 0 → `7768716 round-46: C1 stage-2 control receipts (21 controls,
all PREDICATE C1 fail; base fence contradicted=22/32) — before the repaired fence is scored`.

### R45-S5-7b — fixed-verified (authored check)
Finding: the round-45 V11 predictor block was bypassable by a lookup table. The live instrument refuses
that shape — `plans/round46_c3_verify.py:64-72` refuses `{`/`}` ("a verdict table needs a dict/set
literal") plus the round-45 token set; `:785-787` turns a lint hit into a refusal.

```
python3 -c 'import importlib.util,sys;from pathlib import Path;p=Path(sys.argv[1]);s=importlib.util.spec_from_file_location("c3",p/"plans/round46_c3_verify.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);b="def predict(text):\n    table = {\"x\": True}\n    return table.get(text, False)\n";l=m.lint_block(b);print("lint=",l);sys.exit(0 if "{" in l else 1)' "$LANE"
```
Observed `lint= ['{', '}']`, **exit 0**. Control: the benign predictor `return text.strip() == "abc"`
lints `[]` (the check is able to fail).

### R45-S5-7c — accepted-risk (authored check)
Live and unfixed: `plans/pkg_gate.py:276` is
`cmd = ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"] + probe` — the package is
pinned, the **`uv` toolchain is not** (`grep -n 'uv.*version\|UV_\|shutil.which' plans/pkg_gate.py` → no
match), and `git log --oneline -4 -- plans/pkg_gate.py` shows one commit, `805fe79 round-36: …`, so no
gate revision has landed since the finding. The lane carries the risk knowingly (the row's own note:
"fix needs a new gate revision"); `status` stays `open`.

```
grep -q '"uv", "run", "--no-project", "--with", "biopython==1.85"' "$LANE/plans/pkg_gate.py" && echo unpinned-uv-fetch-present
```
Observed `unpinned-uv-fetch-present`, **exit 0**.

### R45-S5-7d — fixed-verified (authored check)
Round-45 defect (`.ufo/waves/round-45/a3w1/R45CritIntent.md` finding 1): a leading `{` skipped path
validation, so `--claims {T}/../../etc` returned `ADMIT` while `--claims ../../etc` returned `BREACH`.
The landed fence **refuses** the placeholder instead of skipping validation —
`plans/fixture_fence.py:219-221`: `if val.startswith("{"):` → `return None, f"{opt} value {val!r} is a
placeholder the fence cannot resolve"`; the accepted option set no longer contains `--claims`/`--receipt`
(`ANCHOR_OPTS: ['--evidence-ref', '--lane', '--verbose']`).

```
python3 -c 'import importlib.util,sys;from pathlib import Path;p=Path(sys.argv[1]);s=importlib.util.spec_from_file_location("ff",p/"plans/fixture_fence.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);v,e=m._argv(Path("."),"anchor",["--evidence-ref","{T}/../../etc"]);print("err=",e);sys.exit(0 if v is None and "placeholder" in (e or "") else 1)' "$LANE"
```
Observed `err= --evidence-ref value '{T}/../../etc' is a placeholder the fence cannot resolve`, **exit 0**.

### R45-S5-7e — accepted-risk (authored check)
The two round-45 mutation items (`R45MutC1Instrument2`, `R45MutC2Checks`) were never re-attacked:
`grep -rn 'R45MutC1Instrument2\|R45MutC2Checks' corpus/lessons/round-4[6-9]*.md corpus/lessons/round-50*.md`
returns only the round-46 defect record (`corpus/lessons/round-46.md:16`), and no wave in rounds 47–50
mutates `plans/round45_c1_verify.py` / `plans/round45_c2_verify.py`. What landed instead is mutation
attack on the **successor** instruments — round-46 wave 2 `R46W2C1MutCounter` (`:57`
`VERDICT: c1-counter-mutants-killed-1/6`) and round-46 wave 1 `R46MutC2Gate`. The lane accepts the risk:
the round-45 instruments are frozen and superseded (live C1 counter is `plans/round50_c1_verify.py`), so
re-attacking them measures nothing that ships. `status` stays `open`.

```
test -f "$LANE/.ufo/waves/round-46/w2/R46W2C1MutCounter.md" && test -f "$LANE/.ufo/waves/round-46/w1/R46MutC2Gate.md" && echo successor-mutant-receipts-present
```
Observed `successor-mutant-receipts-present`, **exit 0**.

## Measurements (verbatim)

Scratch clone (one shared clone, toplevel asserted before any write):
`git clone --shared …/kengaku-shokunin /fast/scratch/hyaku/kengaku-r51/C2ExecH/lane`;
`git -C "$D" rev-parse --show-toplevel` → the clone dir; `git rev-parse HEAD` →
`4090c3db79d11279ab5e5121ba25e74aa316e6e7`.

Before (unmodified ledger), `python3 plans/round51_routing.py --lane . --run-checks --scratch <s>/cw0`, exit 1:

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
```
Reproduces the frozen before receipt `claims/c2-before.txt` (rows=71, attributed=0, checks absent=10, exit 1).

After splicing my eight rows (rows 64–71 replaced), same command, exit 1 — the 63 remaining DETAIL lines
are the other seats' rows:

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=8 incomplete=63
OWNERS attributed=8 unattributed=63
DISPOSITIONS set=8 bad=63
SOURCES resolved=71 missing=0
CHECKS present=65 absent=6
VERIFIED ran=6 passed=6 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
```
`grep -c 'DETAIL.*R45-S5-[4-7]'` → **0**.

## Finding routed to the L1 (affects every C2 seat)

`plans/round51_routing.py` runs each `fixed-verified` check as
`subprocess.run(["bash","-lc",cmd], cwd=tmp, env={… "LANE": lane})` — **from a scratch cwd**, with the
lane reachable only as `$LANE`. Every pre-existing check in the ledger is lane-relative, so all 61 of them
fail from that cwd. Measured (scratch cwd → lane root):

```
grep -q 'S166' corpus/lessons/round-46.md                          -> exit 2 (No such file or directory)  | 0
grep -q 'lane commit' .ufo/waves/round-46/integrate/c2-landing.txt -> exit 2                              | 0
grep -q 'cf7de6af' plans/round-46-claims.md                        -> exit 2                              | 0
test -f .ufo/waves/round-46/claims/control-c1-fence-keyed_name.txt -> exit 1                              | 0
```
Consequence: **no row can be `fixed-verified` with an unrooted check** — the counter would print
`CHECK_FAILED` and the predicate would fail. I therefore re-rooted my four pre-existing checks as
`cd "${LANE:?}" && <original command>` (the same form sibling `C2ExecG` used for `R45-S5-1..3`) and
measured all four at **exit 0** from a scratch cwd. Any sibling seat that marks an unrooted check
`fixed-verified` breaks the landing predicate; the L1 must re-root or downgrade those rows.

## Robustness under the repaired counter (working tree, not mine)

`git status --porcelain` shows ` M plans/round51_routing.py` in the lane working tree — not my edit (I
wrote no production file). That uncommitted revision runs checks with `cwd=str(lane)` and a 90 s timeout,
and reads owners from the `LANE|repo|axes` rows of `shokunin.conf`. I measured my eight rows under **both**
counter revisions (committed `cwd=tmp`, and the working-tree `cwd=lane`), each on a fresh spliced clone:

```
committed   : VERIFIED ran=6 passed=6 failed=0 | DETAIL for R45-S5-4..7e = 0
working tree: VERIFIED ran=6 passed=6 failed=0 | DETAIL for R45-S5-4..7e = 0
```
The fragment is therefore cwd-agnostic by construction: the four re-rooted checks begin
`cd "${LANE:?}" && …`, and the four authored checks address the lane as `"$LANE/…"`. Flag for the L1: the
frozen C2 counter currently differs from the commit in the working tree, which is a freeze-integrity
decision only the integrator can make.

## Integration note

`C2ExecLedgerMerge.jsonl` (written 15:33) captured an earlier, more conservative version of this fragment
(4 `fixed-historical` + 2 `fixed-verified` + 2 `accepted-risk`, unrooted checks). The current fragment is
the authoritative one for rows 64–71 and must be re-merged: 6 `fixed-verified` (checks proven to exit 0 in
the counter's own run), 2 `accepted-risk`, `close`/`note`/`status` untouched.

## Limits

- Read-only against the lane: I wrote only `.ufo/waves/round-51/w1/C2ExecH.jsonl` and this report. No
  production file, no commit, no mutating git command; the only git writes were inside the scratch clone.
- `accepted-risk` is a judgement about a live unfixed defect (`7c`) and a superseded instrument pair
  (`7e`); their checks re-derive the risk, they do not close it.
- `fixed-verified` for `7b`/`7d` re-derives the *refusal behaviour of the live instrument*; it does not
  re-run the round-45 wave.
- Row `status` values are preserved verbatim, so `7b`…`7e` still read `open` although `7b`/`7d` carry a
  now-passing check. Reconciling `status` at landing is the L1's call.
- No C1 surface was probed; freshness is untouched by this seat.

## Scratch

`/fast/scratch/hyaku/kengaku-r51/C2ExecH` was created for this seat (`TMPDIR` exported there), held the
single shared clone and the counter runs, and was **removed before yield**. `df -h /fast` reported `548G`
available at the end. No citable evidence lives under `/tmp`.

VERDICT: rows-64-71-attributed (8/8 owner=kengaku; 6 fixed-verified with checks exiting 0 inside the counter run, 2 accepted-risk; 0 DETAIL lines for these rows in the spliced-ledger run; fragment re-merged over the stale C2ExecLedgerMerge capture)
