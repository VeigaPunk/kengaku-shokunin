# MutCrossCounter — cross-counter interference probe (R51)

Seat: `MutCrossCounter`, mutation-tester, leaf (no dispatch). Lane `kengaku-shokunin`,
hyaku run 11, one v2 build-and-attack wave.
Item: does `plans/round51_surfaces.py` read `corpus/routed-findings.jsonl`, or
`plans/round51_routing.py` read `PROVINCE.md` / `plans/round51-surfaces.json`?
Prove by static read plus scratch runs with each input emptied. Report the coupling graph and
any hidden dependency.

**REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7** (measured). The five frozen inputs are
byte-identical at the stage-1 freeze commit and at the measured tip — `git diff --stat
e07f131 4090c3d -- plans/round51_surfaces.py plans/round51_routing.py plans/round51-surfaces.json
corpus/routed-findings.jsonl PROVINCE.md` printed nothing. Digests measured:

```
edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e  plans/round51_surfaces.py
7bf2d00ccf35ce3ca9a62f1f72aaf2bb0ecb7ea7880b093a05bb927cae6e9b03  plans/round51_routing.py
60d05a0a3f5b099061a902fac7612cd178c8dda01680ac04b84611a77fcf2dd8  plans/round51-surfaces.json
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  corpus/routed-findings.jsonl
5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298  PROVINCE.md
```

## Axes named

1. **Cross-counter interference** — does either instrument's verdict depend on the other's
   input file (C1 ← ledger; C2 ← `PROVINCE.md` / manifest)?
2. **Hidden input coupling** — inputs neither instrument declares: process cwd, the lane's
   parent directory, and the arbitrary shell strings C2 executes.

## Answer in one line

**Neither direction is coupled at the measured tip** — byte-identical output under empty-file
substitution and zero syscalls against the other's files. **But C2's isolation is
content-dependent, not structural**: three ledger fields (`check`, `close`, `source`) are
generic path/command vectors that reach C1's inputs, and this round's landing edits exactly
those fields. C1's isolation is structural by kind: its only generic file reader is the
`count` probe, which is lane-anchored and today points at `corpus/SOURCES.md`, not the ledger.

## Commands run (all in `/fast/scratch/hyaku/kengaku-r51/MutCrossCounter`, TMPDIR exported there)

```sh
git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/base
cd $S/base && python3 plans/round51_surfaces.py --lane .                    # baseline C1
cd $S/base && python3 plans/round51_routing.py --lane . --run-checks        # baseline C2
strace -f -e trace=openat -o c1.strace python3 plans/round51_surfaces.py --lane .
strace -f -e trace=openat -o c2.strace python3 plans/round51_routing.py --lane . --run-checks
strace -f -e trace=openat,newfstatat,stat -o c1.stat.strace python3 plans/round51_surfaces.py --lane .
# 10-case empty-file substitution matrix (mv aside, truncate, run, restore, re-hash)
python3 plans/round51_surfaces.py --lane . --manifest $S/probe-manifest.json   # count-probe retarget
cd $S && python3 base/plans/round51_surfaces.py --lane base                    # cwd anchoring
python3 plans/round51_routing.py --lane . --ledger $D/corpus/r51probe-*.jsonl --run-checks
# 61 ledger checks executed exactly as the counter does, in both cwds
```

Scratch fixture guard: `git -C "$D" rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kengaku-r51/MutCrossCounter/base` before every write. No mutating git
command was run anywhere; the lane was never written (the clone is `--shared`, and every
mutation lived in the scratch worktree, restored and re-hashed per case).

## Baselines reproduce the committed before receipts

C1 (clone, `--lane .`): `ANCHORS total=19 dup=0 missing=0`, `ROWS section="## Surfaces"
rows=9 entries=9 uncovered=0`, `ROWS section="### Core" rows=10 entries=10 uncovered=0`,
`PROBES run=19 present=13 absent=6 errors=0`, `DRIFT 3`, `STALE 0`, `UNVERDICTED 1`,
`NUMBER-DRIFT 1`, `RESOLVE observed_present=13 floor=13 verdict=met`,
`PREDICATE R51-C1 fail`, exit 1 — identical to `.ufo/waves/round-51/claims/c1-before.txt`
except that receipt's `REV 297e179…` line.

C2 (clone, `--lane . --run-checks`): `LEDGER corpus/routed-findings.jsonl rows=71`,
`FIELDS complete=0 incomplete=71`, `OWNERS attributed=0 unattributed=71`,
`DISPOSITIONS set=0 bad=71`, `SOURCES resolved=71 missing=0`, `CHECKS present=61 absent=10`,
`VERIFIED ran=0 passed=0 failed=0`, `CLOSE_REFS resolved=0 missing=0`, `NEXT violations=0`,
`PREDICATE R51-C2 fail`, exit 1 — same summary lines as `c2-before.txt` (see F9 for the
difference: 223 `DETAIL` lines).

## Static read — complete file-access inventory

| Instrument | Path reached | How | Anchored to |
|---|---|---|---|
| C1 | `plans/round51-surfaces.json` | `json.loads(read_text)` | `--manifest` or `lane/plans/…` |
| C1 | `PROVINCE.md` | `read_text().split("\n")` | `--province` or `lane/PROVINCE.md` |
| C1 | probe `paths` targets | `expand(t).exists()` — **no lane join** | **process cwd** |
| C1 | probe `sha256` target | `expand(target).read_bytes()` — **no lane join** | **process cwd** |
| C1 | probe `count` target | `lane / target` if relative, else absolute | **lane** |
| C1 | probe `port` / `http` | socket / urllib, no file | — |
| C1 | git | `git -C lane rev-parse master` (subprocess) | lane |
| C1 | tempfile | `tempfile.mkdtemp` only under `--selftest` | TMPDIR |
| C2 | `corpus/routed-findings.jsonl` | `read_text().split("\n")` + `json.loads` per line | `--ledger` or `lane/corpus/…` |
| C2 | `<lane>/../shokunin.conf` | `read_text` + `re.match(r"\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{")` | **lane parent** |
| C2 | every row's `source` | `(lane / src.split(":")[0]).exists()` | lane |
| C2 | every `fixed-historical` `close` | hex → `git -C lane cat-file -e <tok>^{commit}`; else `(lane/tok).exists()` | lane |
| C2 | every `fixed-verified` `check` | `bash -lc <cmd>` with `cwd=scratch`, `LANE=<lane>`, 60 s | **arbitrary** |
| C2 | tempfile | `mkdtemp(prefix="r51route-")` or `--scratch` | TMPDIR |

Neither instrument contains a literal reference to the other's files. `grep` over both sources
for `routed-findings`, `PROVINCE`, `round51_routing`, `round51_surfaces`, `shokunin.conf`
returns only each file's own path.

## Syscall evidence (observed, not inferred)

```
C1 opens (openat):  …/plans/round51-surfaces.json  …/PROVINCE.md  (plus probe targets: SOURCES.md ×2)
C1 stat+open hits:  routed-findings 0 | shokunin.conf 0 | round51_routing 0 | SOURCES 2
C2 opens (openat):  …/corpus/routed-findings.jsonl
C2 hits:            PROVINCE 0 | round51-surfaces 0 | round51_surfaces 0 | shokunin.conf 0 | SOURCES 0
```

`shokunin.conf 0` in C2 is not a mis-trace: `load_owners` only reaches the file when the lane
has a parent — in this clean clone it does not (see F5).

## Empty-file substitution matrix

Each case: `sha256` before → move the file aside → `: > file` → run the *other* instrument →
restore → `sha256` after. All ten restores verified byte-exact (`sha_before == sha_after`),
worktree clean afterwards (`git status --porcelain` empty).

| # | Instrument | Emptied file | Exit | Output vs baseline | Reading |
|---|---|---|---|---|---|
| 1 | C1 | `corpus/routed-findings.jsonl` | 1 | **IDENTICAL** | C1 does not read the ledger |
| 2 | C1 | `plans/round51_routing.py` | 1 | **IDENTICAL** | C1 does not read the C2 counter |
| 3 | C1 | `plans/round51-surfaces.json` (own) | 1 | traceback `JSONDecodeError` | own input, load-bearing |
| 4 | C1 | `PROVINCE.md` (own) | 1 | `ANCHORS … missing=19`, `UNVERDICTED 6` | own input, load-bearing |
| 5 | C1 | `corpus/SOURCES.md` | 1 | `probe says SOURCES rows=0` | count-probe target, load-bearing |
| 6 | C2 | `PROVINCE.md` | 1 | **IDENTICAL** | C2 does not read PROVINCE.md |
| 7 | C2 | `plans/round51-surfaces.json` | 1 | **IDENTICAL** | C2 does not read the manifest |
| 8 | C2 | `plans/round51_surfaces.py` | 1 | **IDENTICAL** | C2 does not read the C1 counter |
| 9 | C2 | `corpus/SOURCES.md` | 1 | **IDENTICAL** | no incidental corpus coupling |
| 10 | C2 | `corpus/routed-findings.jsonl` (own) | **0** | `rows=0 … PREDICATE R51-C2 pass` | own input — and see F6 |

Cases 3–5 and 10 are positive controls: the substitution method demonstrably *can* move each
instrument, so cases 1, 2, 6, 7, 8, 9 are real nulls, not a dead probe.

Case 10 verbatim:

```
LEDGER corpus/routed-findings.jsonl rows=0
FIELDS complete=0 incomplete=0
OWNERS attributed=0 unattributed=0
DISPOSITIONS set=0 bad=0
SOURCES resolved=0 missing=0
CHECKS present=0 absent=0
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
```

## Coupling graph (measured at 4090c3d)

```
                 ┌──────────────────────────────┐
   process cwd ──┤ C1 round51_surfaces.py       │
                 │  paths/sha256 probes (cwd)   │
   TMPDIR ───────┤  count probe → lane-joined   │──► corpus/SOURCES.md   (only count probe)
                 │  port/http → host sockets    │
                 └───────────┬──────────────────┘
                             │ reads: manifest + PROVINCE.md (+ git rev-parse master)
                             ▼
        plans/round51-surfaces.json ── PROVINCE.md ── git(master)
                             ╎
                    NO EDGE (0 syscalls, byte-identical output)
                             ╎
        corpus/routed-findings.jsonl ◄── reads ──┐
                                                 │
   lane parent ──────────────────────────────────┤ C2 round51_routing.py
   (../shokunin.conf — regex never matches)      │  source/close → (lane/p).exists()   ← latent edge to any path
   TMPDIR ───────────────────────────────────────┤  check → bash -lc, cwd=scratch, LANE ← latent edge to any path
                                                 └──► git cat-file (fixed-historical)
```

Solid edges are exercised at the tip; the two latent edges from `source`/`close`/`check` are
inert only because no ledger row currently names a C1 input — `sources named by the 71 rows:
15 distinct files, none is PROVINCE.md or plans/round51*`; `checks mentioning PROVINCE/round51/
surfaces.json: NONE`.

## Hidden dependencies found

**F1 — `count` probe is a generic lane-relative file reader (the vector the item names).**
Live but unused: the only `count` entry is SF14 → `corpus/SOURCES.md` (claim 25, probe 170).
Retargeting it at the ledger proves the edge is one manifest edit away — a scratch manifest
with `{"kind":"count","target":"corpus/routed-findings.jsonl","pattern":"\"id\"","label":"ledger rows"}`
and `count_claim: 70` printed:

```
  DETAIL NUMBER-DRIFT SF14 row claims 70, probe says ledger rows=71
```

**F2 — C2's `check` field is arbitrary code with `LANE` in its environment.** A synthetic row
`{"disposition":"fixed-verified","check":"grep -q '## Surfaces' \"$LANE/PROVINCE.md\""}` made
the counter open C1's input:

```
LEDGER corpus/r51probe-check.jsonl rows=1
VERIFIED ran=1 passed=1 failed=0
PREDICATE R51-C2 pass
PROVINCE.md opens during H1: 1
  808843 openat(AT_FDCWD, "…/base/PROVINCE.md", O_RDONLY|O_NOCTTY) = 3
```

**F3 — `close`/`source` are existence probes against arbitrary lane paths.** A row with
`"disposition":"fixed-historical","close":"PROVINCE.md"` yields `CLOSE_REFS resolved=1
missing=0`, `PREDICATE R51-C2 pass`. So C2 can be *made* to stat any C1 input without editing
the counter — the separator between the two claims is a property of today's ledger rows, not
of the instruments.

**F4 — `--lane` does not anchor `paths`/`sha256` probes; `count` is anchored.** Run from the
scratch parent with `--lane base`: `PROBES run=19 present=3 absent=16 errors=0`, `STALE 10`
(SF07, SF08, SF09, SF10, SF11, SF12, SF13, SF17, SF18, SF19), `RESOLVE observed_present=3
floor=13 verdict=violated`, while `NUMBER-DRIFT` still reports `rows=170` because that probe
joins the lane. The C1 predicate therefore depends on the caller's cwd, and the claims' after
measurement ("in a clean clone") silently assumes `cd` into the clone. Fixing this is an
instrument change and is out of scope for this seat; the wave must at least never run C1 from
anywhere but the lane root.

**F5 — the owner set never comes from `../shokunin.conf`.** `load_owners`' regex
`\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{` matches **0** lines of the real fleet conf, whose lanes
are pipe-delimited inside `LANES="…"` (`protocol|.|…`, `aggregator|.|…`). Effective owner set =
the hardcoded `FALLBACK_OWNERS` (19 names). Two consequences for the C2 predicate ("every
`owner` names a fleet lane from `../shokunin.conf`"):
- the conf clause is inert at the tip;
- a *correct* parser would be worse — the conf's `LANES` block lists only `protocol` and
  `aggregator`, so `kengaku`, `kama`, `kagi`, … (15 of the fallback names) would all be
  rejected as "not a fleet lane".
The set is also location-dependent: with a YAML-ish conf in the lane parent, a row owned by
`zeta` gives `OWNERS attributed=1`; the same row in the clean clone gives
`OWNERS attributed=0`, `DETAIL OWNER H5 owner 'zeta' not a fleet lane`. After-target numbers
are therefore reproducible only for the clean-clone case, and the fallback list is the actual
contract the seats must write against.

**F6 — C2 has no row floor: an empty ledger passes.** C1 has `resolve_floor` to defeat
do-nothing; C2's equivalent ("rows must not fall below 71") exists only in the claims doc.
Measured: empty ledger → `rows=0`, `PREDICATE R51-C2 pass`, exit 0. The kill rule is not
implemented by the instrument, so the after receipt's `rows=71` is the only guard — a seat that
deletes rows instead of attributing them scores `pass`.

**F7 — `--ledger` is unusable with a relative path.** `print("LEDGER %s" % ledger.relative_to(lane))`
raises when `ledger` is relative (and when it is absolute but outside the lane):

```
ValueError: 'corpus/r51probe-check.jsonl' is not in the subpath of '…/base'
```

The override only works with an absolute path inside the lane — every synthetic-ledger probe in
this report used that form.

**F8 — checks run in a scratch cwd, not in the lane; 55 of 61 cannot pass there.** Executing
all 61 non-empty `check` strings exactly as the counter does (`cwd=<scratch>`, `LANE=<lane>`):

```
PASS 6   FAIL 55
passes in counter cwd (scratch)      : 6
fails in scratch, passes in lane cwd : 41  -> pure cwd-coupling defect, fixable with $LANE/ prefix
fails in BOTH cwds                   : 14  -> check itself stale/false
```

The 14 unsatisfiable-as-written checks: R39-R3, R39-R4, R42-R1, R42-R3, R42-R5, R42-R6,
R42-R3-02, R42-R3-05, R42-R3-06, R42-R3-18, R42-R3-19, R42-R3-27, R42-R3-32, R42-R3-36
(verified by hand: `plans/carried_direction_diff.py` and `plans/sources_appendonly.py` are
ABSENT; `SKILL.md:238` no longer holds the grepped text; `corpus/evidence/round43/` contains no
`prior-art` entry). Direct impact on C2's after target `CHECK_FAILED 0`: no row among those 55
may be dispositioned `fixed-verified` unless its check is rewritten with `$LANE/` (41 rows) or
replaced outright (14 rows). The six that pass today are R39-R2, R39-R5, R42-R3-03,
R42-R3-07, R42-R3-08, R42-R3-26.

**F9 — the committed `c2-before.txt` is a filtered view, not verbatim output.** The frozen
instrument prints 223 `DETAIL` lines for the before state (71 FIELDS + 71 OWNER + 71
DISPOSITION + 10 CHECK); `wc -l` on the receipt is 10 and `grep -c DETAIL` is 0, yet its line
10 is `PREDICATE R51-C2 fail`, which the instrument emits *after* the details. The receipt was
therefore passed through a `DETAIL` filter (exit 1 captured separately). Counts are not
falsified, but the receipt cannot be regenerated byte-for-byte by the frozen command — a
provenance defect for C2's before state. `c1-before.txt` (21 lines, 5 DETAIL lines —
identical to the clone run) is verbatim.

**F10 — two checks read the ledger itself.** R42-R3-24 and R42-R3-25 grep
`corpus/routed-findings.jsonl` from `cwd=scratch`, so as written they cannot pass (F8) — but if
a seat rewrites them as `$LANE/corpus/routed-findings.jsonl` and marks them `fixed-verified`,
C2 executes a read of its own input inside its own run. Self-referential, not cross-counter, but
it makes the check outcome depend on the very bytes being validated.

## What is *not* coupled (measured)

- C1 never opens or stats `corpus/routed-findings.jsonl`, `plans/round51_routing.py`, or
  `../shokunin.conf` (0 hits in the openat+stat trace; empty-file substitution byte-identical).
- C2 never opens or stats `PROVINCE.md`, `plans/round51-surfaces.json`, or
  `plans/round51_surfaces.py` at the tip (0 hits; three independent empty-file substitutions
  byte-identical).
- No ledger row's `source` names a C1 input (15 distinct sources, none matching
  `PROVINCE`/`round51`), and no `check` string mentions them.
- Both instruments read `git` state of the same lane (`rev-parse master` vs `cat-file -e`) —
  read-only, and only the `fixed-historical` path uses it.

## Limits

- One measurement point (4090c3d) in one clean clone; endpoint probes (SF03 http, SF16 port)
  are point-in-time and were not varied.
- The synthetic rows in F2/F3/F5 are probes of the *counter's* behaviour, not proposals for the
  landing ledger; they were written inside the scratch clone and deleted.
- F8's 55 failures were classified by exit status in two cwds, not by reading each command's
  intent; a few may be failing for environment reasons beyond the two classes named.
- No tool was installed or upgraded (strace already present at `/usr/bin/strace`; `pacman`
  untouched per the host-wide guard). Free space seen: `/fast` 541 G available, scratch peak
  1.2 G.

VERDICT: **no cross-counter interference at the measured tip in either direction** — C1 is
structurally isolated from the ledger, C2 from `PROVINCE.md`/the manifest (byte-identical
outputs under empty-file substitution plus zero syscalls), **but C2's isolation is
content-dependent**: `check`/`close`/`source` are generic path/command vectors that reach C1's
inputs from ledger content alone, and 55 of 61 existing checks cannot pass under the counter's
own execution model (41 cwd-coupled, 14 stale) — so C2's after target `CHECK_FAILED 0` is
reachable only if the landing rewrites those checks or keeps them out of `fixed-verified`.
Secondary defects for the L1: C2 has no row floor (empty ledger passes, F6), `load_owners`
never parses the real `shokunin.conf` (F5), `paths`/`sha256` probes ignore `--lane` and follow
cwd (F4), `--ledger` crashes on a relative path (F7), and `c2-before.txt` is a filtered view
(F9).
