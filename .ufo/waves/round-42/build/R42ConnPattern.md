# R42ConnPattern — cross-claim pattern finding (kengaku round 42, wave 1)

Seat: R42ConnPattern (connector, leaf). Date: 2026-10-26. Scope: the lane's own instruments —
`plans/round42_c1_verify.py`, `plans/round42_c2_verify.py`, `plans/fibsqrt_probe.py`, `plans/pkg_gate.py`,
`plans/order_check.py`, `plans/anchor_digest_check.py`, `plans/routed_open.py` — read in full at the lane tip
(`d69452cfa4ea8f95a43caf3727a7c797ba390b6c` state), plus the frozen receipt, dry table, captures and
controls under `corpus/evidence/round42/` and `.ufo/waves/round-42/claims/`. No lane file was written; no
battery/counter/fixture was run (analysis seat). Method note: the three hunted shapes come from the two
frozen claims — the tb2 grader's `/app/gates.txt` (checked) vs cwd-relative `gates.txt` (used),
`gcc -o sim` (built) vs `/app/sim` (run), the fixed 28-value table standing in for general correctness;
and C1's near-variant classes "a route dropped, a scan bound widened, a regex alternation changed".

Host-safety receipt (Q32) for the verification pass that produced the derived numbers below:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /bin/sh -c 'grep … plans/round42_c1_verify.py; grep -n digest-uppercase plans/anchor_digest_check.py'
ENVELOPE start 17:34:29 end 17:34:29 rc=0 local_bin_listing_before=436b361f9d1edc4e after=436b361f9d1edc4e unchanged
```

Derived numbers and their commands:
- Mutant directions, frozen table: `grep -oE "'(silence|rc-silence|rc-mirror|error)'" plans/round42_c1_verify.py | sort | uniq -c` → `5 rc-mirror, 6 rc-silence, 3 silence` (14 total, **0 error**).
- Manifest star form: `find corpus/evidence -name 'SHA256SUMS*' -exec grep -l ' \*' {} +` → no output (no star-form line corpus-wide; the round-42 manifest has 0: `grep -c ' \*' …/SHA256SUMS` → 0).
- Census script locus: `ls scripts/sources-census.sh` in the lane → `NOT IN LANE`; counter calls `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (fleet root); `grep -c sources-census plans/pkg-spec-r42.json` → 0 (unpinned).
- Grader path forms from the captures: `test_outputs.py:9` `gate_path = Path("/app/gates.txt")` vs `sim.c:319` `parse_gates("gates.txt")`; `test_outputs.py:66` `["gcc", "-O3", "/tests/sim.c", "-o", "sim"]` vs `test_outputs.py:119` `["/app/sim", str(n)]`.
- Receipt: `corpus/evidence/round42/fibsqrt-probe.txt` — `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`; case `lookup-28 … tests=PPP` passes while the probe docstring records it prints 0 on 208/20000.

---

## Pattern A — a path checked in one form, used in another (the `/app/gates.txt` vs `gates.txt` shape)

**A1. `plans/fibsqrt_probe.py:239` — `--chdir /app` is the only thing making the grader's two path forms coincide.**
The probe binds the case work dir at `/app` and hard-chdirs there, so `gcc -o sim` (cwd) lands exactly on
`/app/sim` and `parse_gates("gates.txt")` (cwd-relative) lands exactly on `/app/gates.txt`. All 16 frozen
cases share this one cwd; no case varies it, so the checked-form/used-form split in the pinned grader is
never exercised by the probe that measures it.
Fixture (one line): a 17th `Case` whose `sandbox_argv` keeps the `/app` bind but chdirs to `/tmp` —
`test_gates_file_exists` still passes on `/app/gates.txt` while `test_sqrt_fib` fails `error=FileNotFoundError`
(`/app/sim` never built: gcc wrote `/tmp/sim`), a verdict shape no frozen prediction covers.

**A2. `plans/round42_c2_verify.py:80` — `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` is host-anchored while the predicate is measured on a clean clone.**
v6 validates the clone's `corpus/SOURCES.md` (lane-relative subject) with a fleet-root tool that is not in
the lane, not in the clone, and not pinned anywhere (`pkg-spec-r42.json` has no `sources-census` token; the
counter's own digest pin list covers spec/gate/probe/dry/captures only). The clone's own
`scripts/sources-census.sh` — even if it existed — is never invoked.
Fixture: drop a doctored `scripts/sources-census.sh` (or a same-named stub) into the measured clone → v6
still passes, because it executed the host copy; the checked tree and the used tool live under different roots.

**A3. `plans/anchor_digest_check.py:377-384` — errata paths are enumerated from HEAD but bytes are read from the working tree; `:398` rows are worktree bytes checked against HEAD evidence.**
`load_errata` lists lesson paths via `tree_paths(lane, LESSONS)` (HEAD commit) then reads `f.read_text()`
from the worktree, silently skipping (`if not f.is_file(): continue`) a deleted worktree file;
`parse_rows` reads `corpus/SOURCES.md` worktree text while every evidence digest comes from HEAD blobs.
Checked-in-one-form (committed), used-in-another (worktree) — the exact shape, inside a tool whose
advertising is about *committed* claims.
Fixture: on a green HEAD, add an uncommitted erratum line citing a row's exact wrong token plus the capture's
true digest → that row is exempted and the tool prints `defects=0` from content HEAD does not contain (mirror:
delete the worktree lessons file → the committed erratum is silently ignored).

**A4. `plans/order_check.py:84-93` — `repo_path` re-roots every CLI path at the git toplevel, not at `--lane`.**
`p = (p if p.is_absolute() else (root / p))` where `root = rev-parse --show-toplevel`; the `--lane` argument
only locates the repo. A caller passing `--lane <repo>/<sub>` naturally reads `--claims <rel>` as relative to
`<sub>`; the tool resolves it against the toplevel. Coincides only because every frozen caller passes
`--lane .` at the toplevel.
Fixture: run `order_check.py --lane <repo>/.ufo --claims plans/round-42-claims.md --receipt corpus/evidence/round42/fibsqrt-probe.txt` — the check proceeds against toplevel-relative paths although every argument names another root.

## Pattern B — a fixed table standing in for a general property (the 28-value `GRADED` shape)

**B1. `plans/fibsqrt_probe.py:86-92` — `GRADED` (28 fixed inputs) is the graded property; `lookup()` builds circuits correct on exactly it.**
This is the tb2 shape carried deliberately inside the measuring instrument: `answer(n)` is general, but only
the 28 table values are graded, and the freeze's own receipt shows the gap — `lookup-28` passes 3/3 printing
0 for the instruction's examples 208 and 20000 (case `lookup-28-plus-examples`, observed `tests=PPP`).
Fixture (one line): `Case("lookup-28-flip-5", "PPP", (), "correct on the 28 graded inputs, wrong on ungraded N=5", gates=text(lookup(GRADED + [5], flip=(5, 0))))` — predicted `PPP`: wrong on a non-tabulated input, fully green.

**B2. `plans/round42_c1_verify.py:145` (`MUTANTS`) with `:113-114` (`TOTAL=14`, `FLOORS`) — the 14-row frozen table is the property "every advertised behaviour is demonstrated".**
The predicate binds literal counts (`killed == TOTAL`, `per_tool == FLOORS`), so the claim certifies the
table, not the tools; the freeze itself carries the acknowledgment (XL1-XL6, the `state_check.py`/
`round_close.py` survivors and 34 unpriced rows are "named as carried" outside it). A near-variant outside
the 14 cannot be killed by any battery42 fixture and the predicate still prints `PREDICATE C1 pass`.
Fixture: a 15th variant of the X6 family aimed at a different anchor line (e.g. the `HEX64`→`HEX64_ANY` swap
re-applied inside the abbreviation check, `anchor_digest_check.py:508-518`) — survives unattributed while
the counter reports 14/14.

**B3. `plans/round42_c2_verify.py:84` — V9's `CASE_ROW` pins `(cid, [PF]{3}, pass|fail)` and leaves the descriptive column `.*` free.**
v9 builds `want` from the receipt's (id, tests, observed) and compares only those three fields; the case
table's text column is unconstrained beyond being non-empty. The fixed 3-tuple stands in for "the entry
describes the receipt"; a false description passes.
Fixture: row `| `nop` | PPF | fail | the size test rejected the shipped example (test 2) |` — letters and
verdict match the receipt exactly; the text is false; V9 reports `case_rows=16/16`.

**B4. `plans/order_check.py:60` — `EXECUTED_EXCUSE` is one fixed sentence (`receipt unreadable`, optional `: path`) standing in for "the gate reports it did not run".**
`blob_hits` treats any `P10 DEFECT` whose detail is not that exact sentence as proof the probe ran; the
gate's no-run vocabulary is frozen to a single phrase. A future/other no-run verdict is scored as execution.
Fixture: a pkg_gate variant whose no-run state prints `P10 DEFECT receipt absent` (no colon path) →
`EXECUTED_EXCUSE` misses, order_check records a `gate-p10` HIT on a claims blob that only quotes a not-run verdict.

**B5. `plans/pkg_gate.py:31` — `MANIFEST_LINE` accepts the coreutils binary-mode star (`\s+\*?(\S+?)\*?$`) but no producer emits it.**
Verified: no `SHA256SUMS*` anywhere under `corpus/evidence/` contains a ` *` line. The star grammar stands in
for "any sha256sum output"; it is dead acceptance today and would silently re-split a filename that itself
begins/ends with a literal `*`.
Fixture: a capture manifest written by `sha256sum -b` (`<digest> *<name>`) → exercises `\*?` in P5/V1; or a
file literally named `*note` in a manifest → its digest line is misparsed rather than rejected.

**B6. `plans/routed_open.py:35-37` — `is_ledger` guards only names starting with `defects`.**
The guard is a fixed prefix table standing in for "the pinned ledgers this file must never read or move"
(the comment names `corpus/defects*.jsonl`). A pinned ledger under any other name is unguarded.
Fixture: `--file corpus/faults.jsonl` shaped as a pinned ledger → the guard does not fire and routed_open
reads/moves a ledger the seat rules treat as pinned.

## Pattern C — an alternation never exercised (the `GATE_P10 (DEFECT|ok|PASS)` shape)

**C1. `plans/order_check.py:53` — `GATE_P10 = (DEFECT|ok)` is exactly coextensive with the gate's verdict vocabulary; the token `PASS` is never produced by any instrument.**
The claims file itself records the shape ("a `P10 PASS` line is not a gate verdict the gate prints"). The
alternation is the whole contract: one never-emitted token is the entire XO6 mutant. This is the same
repair family as the fibsqrt split — a contract written as a two-form grammar whose unchecked form hides
the gap (instruction says stdin/last-32-lines; grader does argv/highest-indexed).
Fixture (frozen): a claims blob `gate: P10 PASS receipt unreadable` committed before the receipt → reference
order_check records no HIT; the XO6-widened alternation records a HIT. (This is exactly the frozen `wit-xo6`.)

**C2. `plans/round42_c1_verify.py:452-453` (`error` branch of `exhibits`) and `:105,446-447` (`PAIR = ^(\d)>(\d)$`) — declared grammar with no frozen input.**
`SIMPLE_DIRECTIONS` advertises `error` and `EXPECT_RC` maps it; the frozen 14 contain zero error-direction
mutants (verified counts above) and no numeric-pair direction, so both branches are unreachable this round.
A kill through them cannot be attributed because no frozen mutant can flow into them.
Fixture: a 15th `error`-direction mutant — e.g. the XO1 `if False` pattern applied to the `CLAIMS_NAME` check
(`order_check.py:80-82`) so a malformed claims name exits 0 instead of 2 — killed by a fixture with
`expect=error` whose argv names `foo.md`; unreachable while `MUTANTS` stays frozen at 14.

**C3. `plans/anchor_digest_check.py:519-526` — the `digest-short|digest-long|digest-uppercase` alternation never executes in any green run.**
At a green tip no defective token exists, so the whole `if not HEX64.fullmatch(tok)` block is dead in lane
runs; and none of the 14 frozen mutants covers it (X6/X7 hit the sibling wrong-capture/unknown alternation at
`:527-537`, X9 hits row-malformed, X14/X15 hit the erratum classes). The strictness the docstring advertises
("an uppercase 64-hex digest is a defect") has no exercised witness.
Fixture: a battery fixture whose row carries its own capture's digest uppercased → reference prints
`class=digest-uppercase` exit 1, declared `defects=["digest-uppercase"]`, killing nothing frozen but proving
the branch.

---

## Synthesis

One shape, three scales. At the grader scale (frozen, can't change) the two-form path split
(`/app/gates.txt` vs cwd `gates.txt`, `./sim` vs `/app/sim`) is latent because the image pins cwd=/app; the
lane's probe faithfully reproduces that coincidence (A1) rather than perturbing it, so the freeze measures
the grader at exactly the one environment where the split is invisible — the probe's 16 cases are a fixed
table (B1) over that single environment. At the counter scale the same shapes reappear in the instruments
themselves: a host-anchored census script judges a clone it doesn't live in (A2), HEAD-listed paths are read
from the worktree (A3), arguments are silently re-rooted (A4), literal-count predicates certify fixed tables
(B2, B3, B4), and alternations carry never-exercised branches/tokens (C1, C2, C3). The C1 near-variant
classes named in the assignment — route dropped (XO1/XO3 `if False`), bound widened (XO5 `upto`→HEAD),
alternation changed (XO6 `|PASS`, XO7 `observed=[^\s]*`→`(?:pass|fail)`) — are precisely the mutation
operators that would expose A3 (dropped `f.is_file()` guard), A4 (widened re-root), B4 (narrowed excuse
bound) and C1-C3 (grammar branches), if a wave-2 seat chose to aim them at the lane's own instruments. None
of the 13 sites requires editing a frozen file; each is listed with a fixture that runs against the
instrument as it stands.

VERDICT: pattern-13-sites
