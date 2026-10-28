# C2MutLedger — mutation probe of the merged C2 candidate ledger

Seat: `C2MutLedger` (mutation-tester), kengaku round 51, hyaku run 11.
Item: mutate the merged candidate ledger in scratch with the seven named defects, run the
frozen C2 counter on each, record which leg fires, report any mutation that passes.

## Axes named

- **adjacency** (primary, R51-C2): does the frozen counter actually force every routed finding to
  name an owner lane and a disposition, or can a row keep the shape and lose the attribution?
- **freshness** (secondary, read-only here): does the counter's own claim — "every `owner` names a
  fleet lane from `../shokunin.conf`" — hold against the file it names?

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

Clone HEAD and lane HEAD both print `4090c3db79d11279ab5e5121ba25e74aa316e6e7`; the counter is
byte-identical in both trees (`sha256 7bf2d00ccf35ce3ca9a62f1f72aaf2bb0ecb7ea7880b093a05bb927cae6e9b03`
for `plans/round51_routing.py`, clone and lane). The stage-1 freeze commit is `e07f131`; the tip
above adds only the wave spec/dispatch.

## Setup

```
mkdir -p /fast/scratch/hyaku/kengaku-r51/C2MutLedger
export TMPDIR=/fast/scratch/hyaku/kengaku-r51/C2MutLedger
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C .../lane rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r51/C2MutLedger/lane
df -h /fast/scratch -> /dev/nvme1n1p2 804G 256G used 548G avail 32%
```

Pristine ledger in the clone: `sha256 39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d`
(71 rows, 64 distinct classes, no `owner`/`disposition` field on any row).

**Candidate provenance.** `w1/C2ExecLedgerMerge.jsonl` was stale for the first half of my seat
(15:22 snapshot, 49743 B, 71 rows, **9 attributed**) while the fragments on disk already covered 62
rows; the merge seat rewrote it at **15:34** with 75 rows, all attributed. I therefore measured
twice: first on a candidate I merged myself from the fragments (below), then on the authoritative
15:34 artifact (`sha256 dfed001963199bdaaf5a59822b5b8b913e119d506691e9e1b30b5e1037dcef6c`, see
"Authoritative candidate").

```
fragments: ['C2ExecA.jsonl', 'C2ExecB.jsonl', 'C2ExecC.jsonl', 'C2ExecD.jsonl', 'C2ExecF.jsonl', 'C2ExecG.jsonl', 'C2ExecH.jsonl']
rows: 71 covered: 62 unattributed: 9
missing ids: ['R42-R3-18','R42-R3-19','R42-R3-20','R42-R3-21','R42-R3-22','R42-R3-23','R42-R3-24','R42-R3-25','R42-R3-26']
```

Candidate: `sha256 48f09fc577085dc8343cebc324713c46f2fb7698e720c5ffb3dae7c20131f550`.
The 9 rows with no fragment (block E) were filled by me — `owner: kengaku`,
`disposition: accepted-risk`, and a lane-anchored `check` where the base `check` was empty — only
so that a *passing* baseline exists; every mutation below is applied to one of the 62 real rows
unless stated. Filled baseline: `sha256 3d5e17fa55bcea6bc45747e6ba671174079c090336aa53a2d0000ab5b6d718c8`.

Dispositions in the candidate: `fixed-verified 32`, `accepted-risk 21`, `fixed-historical 7`,
`refused-out-of-scope 2`, filled 9. Owners: `kengaku 62`, filled 9 — **no row is owned by any lane
other than kengaku**, and 3 rows carry `next` (`R39-R2`, `R39-R3`, `R39-R4`, all `accepted-risk`).

## Baseline (must pass, else a mutant's exit code is not evidence)

```
python3 lane/plans/round51_routing.py --lane lane \
  --ledger $PWD/lane/.mutants/c-baseline.jsonl --run-checks --scratch $PWD/work/verbatim
```
```
LEDGER .mutants/c-baseline.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=32 passed=32 failed=0
CLOSE_REFS resolved=7 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
EXIT=0
```

All seven mutants below are one-field edits of that passing baseline, written as separate files and
passed with `--ledger`, so the pristine bytes were never the detector's input.

## Seven named mutations

| # | mutation (row, field) | exit | leg fired (verbatim detail) | verdict |
|---|---|---|---|---|
| 1 | drop `owner` from `R39-R1` | 1 | `FIELDS R39-R1 missing owner`, `OWNER R39-R1 has no owner` | **killed** |
| 2 | `owner: "nope"` on `R39-R1` | 1 | `OWNER R39-R1 owner 'nope' not a fleet lane` | **killed** |
| 3 | `disposition=fixed-verified`, `check: "false"` on `R39-R1` | 1 | `CHECK_FAILED R39-R1 fixed-verified but check exits nonzero` (`VERIFIED ran=32 passed=31 failed=1`) | **killed** |
| 4 | `check: ""` on `R39-R1` | 1 | `CHECK R39-R1 has no check command` (`CHECKS present=70 absent=1`) | **killed** |
| 5 | `disposition=routed`, `owner=kengaku`, `next` present, on `R39-R2` | 1 | `NEXT R39-R2 is routed but owned by kengaku (absorbed, not routed)` | **killed** |
| 5b | same, `next` omitted | 1 | two `NEXT` details (absorbed **and** missing `next`) | **killed** |
| 6 | `source: "corpus/absent-round51-mutant.md:3"` on `R39-R1` | 1 | `SOURCE R39-R1 source 'corpus/absent-round51-mutant.md:3' does not resolve` | **killed** |
| 7 | `disposition=fixed-historical`, `close: "deadbeef…deadbeef round 52"` on `R39-R1` | 1 | `CLOSE_REF R39-R1 close 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeef round 52' does not resolve` (`CLOSE_REFS resolved=7 missing=1`) | **killed** |

Reproduced twice: once against the 54-attributed intermediate merge and once against the
62-attributed candidate above — same seven legs, same verdicts. Against the raw stale merge artifact
(9 attributed, 62 rows with no fields) the baseline fails on `FIELDS/OWNER/DISPOSITION/CHECK`; there
the per-mutant *delta* is still legible (M1 `incomplete 62→63`, M2 `unattributed 62→63`, M3
`failed 0→1`, M4 `absent 7→8`, M5 `NEXT 0→1`, M6 `missing 0→1`, M7 `CLOSE_REF 0→1`) but I record
those seven as **inconclusive** under the role rule, not as kills.

**Mutations that pass: none of the seven.** All seven named defects are killed.

## Survivors (coverage findings, same detector, same passing baseline)

| probe | change | exit | finding |
|---|---|---|---|
| S1 | duplicate a row verbatim (72 rows, duplicate `id`) | 0 | no `id`-uniqueness check |
| S2 | delete one row (70 rows) | 0 | no row-count floor; the kill rule "rows must not fall below 71" is outside the counter |
| S3 | `disposition=fixed-verified`, `check: "true"` | 0 | **fake fix launders**: any command exiting 0 counts as verification, so `true` (or `false; true`) is accepted |
| S4 | `disposition=fixed-verified` with `status: "open"` | 0 | disposition/status coherence unmeasured |
| S5 | `source: "corpus:1"` (an existing directory) | 0 | `source` is existence-checked, not file-and-line checked |
| S6 | `close: "corpus"` on a `fixed-historical` row | 0 | a bare directory resolves as a close reference |
| S7 | unknown extra field added | 0 | benign: presence-only schema, no closure |
| S8 | `owner: "unowned:integrator"` on a `routed` row | 0 | by design (`NEXT` only rejects `kengaku`), but it means the integrator is a legal sink for a "routed" row |

S3 is the one that matters for the claim: mutation 3 shows `check:"false"` is caught, but the
adjacent defect — a tautological `check` — is not. A `fixed-verified` row with `check:"true"` passes
the predicate that is supposed to prove the fix.

## Truth defects in the counter (measured, not inferred)

1. **`OWNER` is a hardcoded allowlist, not `../shokunin.conf`.** `load_owners` scans for
   `^\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{`; the fleet conf uses `LANES="id|repo|axes"` lines, which
   that regex never matches. Measured against the real fleet root: **17 owners, 0 of them from the
   conf** (`only in fallback: []`, `from conf: 0`). The set is `FALLBACK_OWNERS` verbatim.
2. **Eight real lanes are refused as owners.** `/home/vgpnk/Projects/shokunin/*/` git repos include
   `audio, game-dev-2d, game-dev-3d, lane3, lore, mado, revenger, tsukuroi`; none is in the allowlist.
   Measured on the candidate with `owner` set to each: `tsukuroi`, `revenger`, `mado` all exit 1 with
   `OWNER R39-R1 owner '<lane>' not a fleet lane`. These are exactly the lanes a routed finding would
   name. The claim text ("every `owner` names a fleet lane from `../shokunin.conf`") is not what the
   code does.
3. **`CLOSE_REF` reads only the first whitespace token.** 23 of the 41 non-null `close` values in the
   base ledger start with a prose token that does not resolve (`F1-F4`, `children`, `round-43`,
   `corpus/QUALITY.md:759` …), and 17 of those 23 contain a resolving hash or path later in the
   string. Unlike `source`, `close` is not stripped of a `:line` suffix. A `fixed-historical`
   attribution written in the ledger's own prose style will be marked missing.
4. **Check cwd is the counter's scratch dir, not the lane.** Of the 61 non-empty base checks, **6**
   exit 0 with `cwd=<scratch>` and **43** with `cwd=<lane>` (41 checks flip). The wave's executors
   already rewrote their checks to `cd "$LANE" && …`; without that rewrite the C2 after-target is
   unreachable, and a reviewer who restores the original `check` string will see `CHECK_FAILED`.
5. **Integration hazard (routed to the L1):** `w1/C2ExecLedgerMerge.jsonl` stayed at the 15:22
   snapshot (9 attributed) until 15:34, while A/C/H landed at 15:28–15:29; `C2RevRecount` and
   `C2RevFieldLoss` were tasked to read that file and may have counted the stale candidate. The
   final 15:34 artifact has 75 rows (not the claim's `rows=71`) and fails the frozen predicate on
   2 `SOURCE` + 4 cwd-artifact `CHECK_FAILED` rows — see "Authoritative candidate".

## Restoration evidence

In-place round trip on the clone's ledger (mutate → run → restore → run), proving the detector
input is byte-restored:

```
BEFORE   3d5e17fa55bcea6bc45747e6ba671174079c090336aa53a2d0000ab5b6d718c8
MUTATED  39d7ecb2a981bafff81c7259dddefe5f971626493ca5ee82d96e101d54174db7   (R39-R1 check -> "false")
  exit 1, DETAIL CHECK_FAILED R39-R1 fixed-verified but check exits nonzero
RESTORED 3d5e17fa55bcea6bc45747e6ba671174079c090336aa53a2d0000ab5b6d718c8
  RESTORE EXACT
  exit 0, PREDICATE R51-C2 pass
```

The clone's tracked ledger is back to the pristine base,
`sha256 39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d`, identical to the hash
taken before any probe; `git -C <clone> status --porcelain` shows only `?? .mutants/`. No file in the
lane, no tracked file anywhere, and no git object was modified. Scratch
`/fast/scratch/hyaku/kengaku-r51/C2MutLedger` is removed before this seat yields.

## Re-measurement against the patched counter (the instrument moved under me)

At 15:33 the lane's `plans/round51_routing.py` was modified in place by the integration owner
(`sha256 7bf2d00c… -> 6f084fdfa3caf003c9e8580d96c4eb63e434f90b7cd9c1bdd8ca70619ad472ba`,
uncommitted, `M plans/round51_routing.py`). The patch rewrites `load_owners` (parses the `id|`
LANES form and globs `*-shokunin` lane dirs), runs checks with `cwd=lane` (was `cwd=<scratch>`),
and raises the check timeout to 90 s — i.e. it addresses items 1, 2 and 4 of the truth defects
above. I re-ran the whole matrix on the patched bytes in a fresh `--shared` clone, this time with
**71/71 rows from the real fragments** (block E had landed; no row filled by me), candidate
`sha256 788786bc1d3d7f0137e6ff60202cf9569e5f19f89d70a046e3b14138370af02e`:

```
LEDGER .mutants/p-baseline.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=38 passed=38 failed=0
CLOSE_REFS resolved=7 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
EXIT=0
```

- All seven named mutations: **still killed**, same leg each (`FIELDS+OWNER`, `OWNER`,
  `CHECK_FAILED`, `CHECK`, `NEXT`, `SOURCE`, `CLOSE_REF`), exit 1.
- All five survivors: **still survive** (`p-s1-dup`, `p-s2-del`, `p-s3-true`, `p-s4-open`,
  `p-s5-srcdir` all exit 0). The tautological `check:"true"` fake fix is unchanged by the patch.
- Owner false negative **closed**: with `owner` set to `tsukuroi`, `revenger`, `mado`, the patched
  counter exits 0 (previously 1). `load_owners` on a fleet-shaped parent now returns 20 owners,
  `new: ['mado','revenger','tsukuroi']`.
- Check cwd **closed**: a row carrying the original cwd-relative base `check` string now exits 0
  (`p-cwd-relative-check`), so the executors' `$LANE` rewrites are no longer load-bearing.
- `CLOSE_REF` first-token behaviour is **unchanged** by the patch: prose-style `close` values
  (`F1-F4`, `round-43`, `corpus/QUALITY.md:759`) still resolve to nothing.

Consequence for the claim: the C2 predicate is scored against a *frozen* instrument, and the frozen
bytes changed after the freeze (`7bf2d00c` → `6f084fdf`). The L1 has since recorded this as
**Instrument amendment A1** in `plans/round-51-claims.md` (append-only, predicate legs unchanged),
citing this seat's measurements for the cwd (6/61 vs 43/61), the owner universe (0 conf matches) and
the timeout. One precision note for that record: of the eight real lane directories refused by the
frozen allowlist, the patch's `*-shokunin` glob recovers seven — `lane3` is a real lane repo but is
not named `lane3-shokunin`, so it stays outside the owner universe unless the curated set or the
conf lists it. A4 in the amendment (`--ledger` relative path `ValueError` in `relative_to`) is the
reason every command in this report passes an absolute `--ledger`.

## Authoritative candidate (the 15:34 merged artifact)

`w1/C2ExecLedgerMerge.jsonl`, `sha256 dfed001963199bdaaf5a59822b5b8b913e119d506691e9e1b30b5e1037dcef6c`,
75 rows: the 71 base ids in base order plus 4 new rows `R51-R1..R51-R4`. Dispositions
`fixed-verified 41`, `accepted-risk 28`, `refused-out-of-scope 2`, `routed 4`; owners `kengaku 71`,
`kama 2`, `protocol 1`, `unowned:integrator 1`; **`fixed-historical 0`** — so the `CLOSE_REF` leg
has no real coverage at all, and the four `routed` rows (`R51-R1..R4`) do exercise `NEXT`.

### The artifact does not pass the frozen predicate

```
python3 plans/round51_routing.py --lane <clone> --run-checks        # frozen bytes 7bf2d00c
LEDGER .mutants/final.jsonl rows=75
FIELDS complete=75 incomplete=0
OWNERS attributed=75 unattributed=0
DISPOSITIONS set=75 bad=0
SOURCES resolved=73 missing=2
CHECKS present=75 absent=0
VERIFIED ran=41 passed=37 failed=4
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
  DETAIL SOURCE R51-R2 source 'corpus/lessons/round-51.md' does not resolve
  DETAIL SOURCE R51-R3 source 'corpus/evidence/round51/surfaces/paths.txt' does not resolve
  DETAIL CHECK_FAILED R45-S5-4 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R45-S5-5 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R45-S5-6 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R45-S5-7a fixed-verified but check exits nonzero
PREDICATE R51-C2 fail
```

Two distinct causes, both diagnosed by re-running the same four checks with `cwd=lane`:

```
--- R45-S5-4 fixed-verified | grep -q 'S166' corpus/lessons/round-46.md
   cwd=scratch rc=2  grep: corpus/lessons/round-46.md: No such file or directory
   cwd=lane    rc=0
--- R45-S5-5 fixed-verified | grep -q 'lane commit' .ufo/waves/round-46/integrate/c2-landing.txt
   cwd=scratch rc=2  cwd=lane rc=0
--- R45-S5-6 fixed-verified | grep -q 'cf7de6af' plans/round-46-claims.md
   cwd=scratch rc=2  cwd=lane rc=0
--- R45-S5-7a fixed-verified | test -f .ufo/waves/round-46/claims/control-c1-fence-keyed_name.txt
   cwd=scratch rc=1  cwd=lane rc=0
```

- The four `CHECK_FAILED` rows are **pure cwd artifacts** of the frozen counter: all four pass with
  `cwd=lane`, and all four are unrewritten cwd-relative checks from the base ledger.
- The two `SOURCE` failures are **forward references**: `corpus/lessons/round-51.md` and
  `corpus/evidence/round51/surfaces/paths.txt` do not exist yet. This is a landing-order
  constraint — the lesson and the evidence file must exist in the same commit as (or before) the
  attributed ledger, or the C2 after-measurement cannot print `pass`.
- Under the patched counter (`6f084fdf`, `cwd=lane`) the same artifact fails on **`SOURCE` only**
  (`SOURCES resolved=73 missing=2`), and `VERIFIED ran=41 passed=41 failed=0`.

### Matrix on the authoritative candidate, baseline made passing

With the two `SOURCE` pointers repaired in a scratch copy (pointed at existing files; nothing else
touched — `sha256` of the repair-only file is derived from the artifact above), the patched counter
prints `rows=75 … VERIFIED ran=41 passed=41 failed=0 … PREDICATE R51-C2 pass` and the matrix is:

| case | exit | legs | verdict |
|---|---|---|---|
| baseline (repaired) | 0 | — | pass |
| m1 drop `owner` | 1 | `FIELDS`,`OWNER` | **killed** |
| m2 `owner:"nope"` | 1 | `OWNER` | **killed** |
| m3 `fixed-verified` + `check:"false"` | 1 | `CHECK_FAILED` | **killed** |
| m4 `check:""` | 1 | `CHECK` | **killed** |
| m5 `routed` + `owner:"kengaku"` on `R51-R1` (a real routed row) | 1 | `NEXT` | **killed** |
| m6 `source` → missing file | 1 | `SOURCE` | **killed** |
| m7 `fixed-historical` + nonexistent commit | 1 | `CLOSE_REF` | **killed** |
| s1 duplicate `id` (76 rows) | 0 | — | **survives** |
| s2 row deleted (74 rows) | 0 | — | **survives** |
| s3 `fixed-verified` + `check:"true"` | 0 | — | **survives** |
| s4 `fixed-verified` with `status:"open"` | 0 | — | **survives** |
| s5 `source:"corpus:1"` (directory) | 0 | — | **survives** |

Same seven kills and same five survivors as on my own merge; the result is stable across the three
candidate snapshots and both counter byte-sets. Note that on the *unrepaired* artifact every row's
verdict is masked by the standing `SOURCE` failure, which is why the repaired baseline is the one
that makes the kills attributable.

## Limits

- Three candidate snapshots were measured: my own fragment merge (62/71 real rows + 9 filled by me),
  the 71-row fully-attributed merge, and the authoritative 75-row artifact. The seven legs and
  their verdicts do not depend on my 9 filled rows: every mutation targets a fragment-attributed
  row, and the authoritative run repeats all seven kills on unmodified fragment rows.
- One `--run-checks` pass per case (two independent clones: frozen counter `7bf2d00c`, patched
  counter `6f084fdf`); a network- or model-dependent check counts as failed, so a legitimate
  `fixed-verified` row whose check needs the network would be killed the same way as a fake fix.
  `--run-checks` executes 32 commands per case on the 62-attributed candidate and 38 on the
  fully-attributed one; results are point-in-time at `4090c3d`.
- I did not mutate C1 (`round51_surfaces.py`) — out of item scope.

VERDICT: All seven named mutations are **killed** by `plans/round51_routing.py --run-checks` — verified three times (my fragment merge, the fully-attributed 71-row merge, and the authoritative 75-row 15:34 artifact) and on both counter byte-sets (frozen `7bf2d00c`, L1-patched `6f084fdf`); each kill names the expected leg in a `DETAIL` line and exits 1. **No named mutation passes.** Five survivors bound the predicate on every byte set: duplicate `id` (76 rows), row deletion (74 rows), a tautological `check:"true"` posing as `fixed-verified`, a `fixed-verified` row left `status:"open"`, and a `source` naming a directory. Two truth defects I measured in the frozen counter — `OWNER` reading a hardcoded allowlist instead of `../shokunin.conf` (0 names from the conf; real lanes `audio/game-dev-2d/game-dev-3d/lane3/lore/mado/revenger/tsukuroi` refused) and checks run with `cwd=<scratch>` (6/61 pass vs 43/61 with `cwd=lane`) — are closed by the L1's patch; `CLOSE_REF`'s first-token-only reading is not, and 23 of 41 prose-style `close` values would be marked missing (latent: the candidate has 0 `fixed-historical` rows). The authoritative candidate **does not pass** the predicate as merged: 2 forward-reference `SOURCE` rows (`corpus/lessons/round-51.md`, `corpus/evidence/round51/surfaces/paths.txt`) and, under the frozen bytes, 4 cwd-artifact `CHECK_FAILED` rows that pass with `cwd=lane`; it also carries 75 rows against the claim's `rows=71`.
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
