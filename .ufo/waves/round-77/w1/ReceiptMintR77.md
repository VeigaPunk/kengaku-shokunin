# ReceiptMintR77 — frozen rerun proposals

Axes: coverage and calibration. Outcome: three honest proposals minted; one command exits 0, two exit 1. Neither printed predicate passes. No production changes, commits, pushes, tool installs, or subagents.

## Revision and execution evidence

`git log -1 --format=%H -- plans/round-77-claims.md` (rc 0) printed `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`; both counter histories and lane HEAD printed the same revision. Read the frozen claims in full and C2's V7 implementation before reruns.

`git clone --revision=9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb -- /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r77/ReceiptMintR77/clone` exited 0. No checkout command was used. In that clone, `git rev-parse HEAD` exited 0 with the full freeze hash above; `git rev-parse --show-toplevel` exited 0 with the clone directory. `git status --porcelain` exited 0 with empty stdout before and after the three reruns.

Each tool's `python3 <tool> --help` exited 0 before execution and advertised `--lane`. R75 also advertised `--rev REV` (default `master`); used `--rev HEAD` to name the detached clone's measured revision, avoiding the absent master ref in a revision-only clone. Each TOOL_SHA is SHA-256 of bytes returned by `git cat-file blob <freeze>:<tool>` (rc 0); those bytes equaled the clean clone's tool file bytes. All three reruns had empty stderr.

## Retained receipts and exact outcomes

Paths below are relative to the lane. Each file contains the requested stamp order, actual command, complete captured stdout, and lowercase `exit <n>` footer.

| Proposal | Command (clone cwd) | Exit | Printed result |
|---|---|---:|---|
| `.ufo/waves/round-77/w1/receipts/rerun-routed-open.txt` | `python3 plans/routed_open.py --lane .` | 0 | `ROWS total=86 open=31 blocked=1 closed=52 refused=2`; `routed_open=32 oldest_round=39` |
| `.ufo/waves/round-77/w1/receipts/rerun-r51-c1.txt` | `python3 plans/round51_surfaces.py --lane .` | 1 | `NUMBER-DRIFT 1`; `DETAIL NUMBER-DRIFT SF14 row claims 244, probe says SOURCES rows=245`; `PREDICATE R51-C1 fail` |
| `.ufo/waves/round-77/w1/receipts/rerun-r75-c1.txt` | `python3 plans/round75_c1_index_parity.py --lane . --rev HEAD` | 1 | `MISSING lessons/round-76-verifier-spotcheck.md`; `MISSING lessons/round-77.md`; `MISSING-EVIDENCE round77`; `PREDICATE R75-C1 fail` |

The routed-open command prints no `PREDICATE` line; rc 0 means valid ledger input, not zero routed findings. R51 also prints `REV unknown` because its revision display resolves master in this detached revision-only clone; the enclosing receipt's verified full LANE_TIP identifies the actual clean bytes. No fabricated predicate or revised stdout was added.

TOOL_SHA values:

- routed-open: `3ce44d941b14a28c88f8f87dec22c390f8a2eedf19cd0e219494b2cd3b82418b`
- r51-c1: `edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e`
- r75-c1: `f69ab60b8dd06fc6076d2731b40ee0f4ec52e81602823b3b8fddc3c8fe88f81f`

Tool grep over all three retained files located the stamps, exits, summary and predicate lines above. Grep of `plans/round77_c2_defect_discharge.py` located RERUNS at lines 68–70 and the case-sensitive `if "EXIT 0" not in text` requirement at lines 294–295.

## Findings and integration risks

1. These frozen receipts cannot establish the stated green V7 target: R51 and R75 genuinely exit 1 with the failing predicates above. Do not relabel either receipt as passing.
2. The assignment requires lowercase `exit <n>` but frozen V7 requires uppercase `EXIT 0`. Proposals preserve the exact requested lowercase footer. Consequently even the routed-open proposal does not satisfy that literal check. This incompatibility was sent to Main; no frozen rule or counter was altered.
3. V7's implementation checks TOOL_SHA only if present and rejects failing predicate lines without requiring a predicate line to exist (lines 287–299). These receipts do carry actual TOOL_SHA stamps, but routed-open has no predicate line. This is an apparatus observation, not a counter change or an executed V7 result.
4. No R77-C2 gate run, selftest, mutant, build, lint, formatter, or broader verification was performed. Parent owns integrated checks; the assigned three reruns are the only verdict measurements here.

Scratch cleanup: `rm -rf -- /fast/scratch/hyaku/kengaku-r77/ReceiptMintR77 && test ! -e /fast/scratch/hyaku/kengaku-r77/ReceiptMintR77` exited 0. The assigned scratch tree is absent.

## Delivery self-evaluation

Accuracy 4/5: captured bytes/exits are retained; no integrated V7 execution claimed. Completeness 5/5: all three requested proposals and this report supplied, scratch removed. Clarity 4/5: R51's inner REV unknown and lowercase/uppercase mismatch require explicit interpretation above. Actionability 4/5: red frozen predicates block green V7, and repairing production is outside this seat. Conciseness 4/5: provenance detail retained because the deliverable is a receipt audit. Overall 4.2/5. Improvements, in impact order: parent must account for the two red predicates and footer contract conflict before claiming V7; preserve receipts as historical red evidence. Would the user agree: the report exposes rather than conceals every observed blocker.
