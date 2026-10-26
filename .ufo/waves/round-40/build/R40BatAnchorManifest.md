# R40BatAnchorManifest — battery40 `a_man`: the anchor tool's two manifest views (A21, A22)

Seat: `R40BatAnchorManifest` (executor, kengaku round 40 wave 1). Lane repo
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Milestone: kengaku r40 wave 1 (build + first falsifiers).
Assignment: one C1 battery module whose fixtures attributably kill frozen anchor mutants **A21** and **A22** in
their declared directions, with `defects` equal to the unmodified tool's class set and `expect` equal to its
exit code.

## 1. What was read before writing (all frozen, none edited)

- `plans/round-40-claims.md` in full: C1 counter, frozen predicate, kill rule, limits; C2 out of scope here.
- `plans/round40_c1_verify.py` in full: module contract, `MUTANTS` table (A21 `dig = m.group(1).lower()` ->
  `dig = m.group(1)`; A22 `if (d, base) in idx["dir_entries"]: got.setdefault(...)` -> `if False: pass`, both
  `rc-mirror`), `Ctx`, `classes()`, `path_ok()`, `exhibits()`, `build_battery()`, `Runner`.
- `plans/anchor_digest_check.py` in full: `evidence_index`, `capture_digests`, `bind_row`, `check`.
- Pre-freeze witnesses `.ufo/waves/round-39/build/R39PlanNext/h_anchor.py:220-239` (X20/X21) and
  `out_anchor_r5.txt:34-35,60-61` (`X20 rc=0`, `X21 rc=0`; `A21` killers `[X21:rc]`, `A22` killers
  `[X20:rc, X21:rc]`), plus `plans/battery38/mainx.py` for module style.
- No file under the lane's `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`,
  `SHONEN.md` was written; no git/jj mutation in the lane. All builds ran in a `--shared` clone at
  `/fast/scratch/hyaku/kengaku-r40/R40BatAnchorManifest/lane` (verified toplevel) and scratch fixtures.

## 2. Files written (own report dir only)

| path (under `.ufo/waves/round-40/build/R40BatAnchorManifest/`) | sha256 |
|---|---|
| `battery/a_man.py` (the deliverable; 4362 bytes, 81 lines) | `0dfc073362c6919e7e69001035a5a85f38f5d32028f1d63f363b71ea82ebd2ac` |
| `probe/probe_manifest_views.py` (advisory, not a battery module) | `3a82cfde80b8cf54e2a60fe1047cc0e5e419e3b92d54def0725cdd4a786ee3ca` |
| `receipts/devrun-only-A21,A22.txt`, `receipts/loadbearing-without-uppercase.txt`, `receipts/loadbearing-without-stale.txt`, `receipts/full-default-run.txt`, `receipts/direct-probe.txt` | run outputs pasted below |

Integration: the L1 copies `battery/a_man.py` to `<lane>/plans/battery40/a_man.py`. Nothing else is needed; the
module is stdlib-only (`hashlib`), has no import-time side effects, and every `fid` starts `a_man-`.

## 3. The two behaviours (one fixture each)

Both fixtures sit on `plans/anchor_digest_check.py:44-46`: *"the digest that entry lists, and the digest of the
committed file bytes, are both accepted views of that one capture"*. `capture_digests(idx, path)` unions the
committed blob's digest with the digest the same directory's `SHA256SUMS*` entry lists for that filename
(`anchor_digest_check.py:325-334`), and `evidence_index` lowercases the entry when it is parsed
(`dig = m.group(1).lower()`, `:250`). So one capture has two accepted digests exactly when the manifest and the
bytes disagree; both fixtures make them disagree (`manifest_digest()` is the digest of a byte string that is
**not** the capture's bytes).

| fid | mutant | direction | tool branch it changes | fixture | ref | mutant |
|---|---|---|---|---|---|---|
| `a_man-stale-manifest-digest` | A22 | `rc-mirror` | `capture_digests` drops the manifest view | committed capture bytes changed; `SHA256SUMS` still lists the digest the row anchors; row anchors that digest, bound by an explicit `corpus/evidence/...` lane path | rc 0, `defects=0` | rc 1, `digest-wrong-capture` |
| `a_man-uppercase-manifest-entry` | A21 | `rc-mirror` | `dig = m.group(1).lower()` | `SHA256SUMS` entry spells the same digest in UPPERCASE; row anchors the lowercase form | rc 0, `defects=0` | rc 1, `digest-unknown` |

Why each mutant refuses:

- **A22** (manifest view deleted): the anchored digest is no longer in the row's capture digest set, but it is
  still a committed evidence digest (`dir_entries` is untouched by the mutant), so the token is classified
  `digest-wrong-capture` and the tool exits 1.
- **A21** (case folding deleted): the stored entry is the uppercase spelling, so neither the anchored lowercase
  digest nor the blob digest matches; the token is in no committed view at all -> `digest-unknown`, exit 1.

Contract compliance: `tool="anchor"`, `expect="accept"`, `defects=[]` (the reference prints no `DEFECT` line on
either fixture — `rows=1 tokens=1 defects=0`); `build(ctx, d)` fills the empty `d` with a self-contained
one-row git repository (`ctx.init`, `ctx.git add/commit`; no dependence on the lane's SOURCES.md or corpus) and
returns `["--lane", <abs path inside d>, "--evidence-ref", "head"]`; every absolute argv token lies inside `d`;
the module source carries none of the counter's `SIDECHANNEL` tokens (counter reports `sidechannel=0`; manual
scan of all 16 tokens: all absent).

## 4. Direct evidence per fixture (reference and each mutant, same fixture)

Command (advisory probe; loads the frozen counter's `MUTANTS` table and the frozen tool from the clone):

```
python3 .ufo/waves/round-40/build/R40BatAnchorManifest/probe/probe_manifest_views.py \
  --lane "$S/lane" --module .../battery/a_man.py --scratch "$S/probe"
```

Output (`receipts/direct-probe.txt`):

```
FIXTURE a_man-stale-manifest-digest expect=accept defects=[] argv=['--lane', '.../probe/f000', '--evidence-ref', 'head']
  reference rc=0 classes=[] last=rows=1 tokens=1 defects=0
  A21       rc=0 classes=[] last=rows=1 tokens=1 defects=0
  A22       rc=1 classes=['digest-wrong-capture'] last=rows=1 tokens=1 defects=1
FIXTURE a_man-uppercase-manifest-entry expect=accept defects=[] argv=['--lane', '.../probe/f001', '--evidence-ref', 'head']
  reference rc=0 classes=[] last=rows=1 tokens=1 defects=0
  A21       rc=1 classes=['digest-unknown'] last=rows=1 tokens=1 defects=1
  A22       rc=1 classes=['digest-wrong-capture'] last=rows=1 tokens=1 defects=1
```

## 5. Counter proof — `--only A21,A22` (paste)

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round40_c1_verify.py --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-40/build/R40BatAnchorManifest/battery \
  --only A21,A22 --work "$S/w"
```

```
PINS total=3 mismatched=0
FIXTURE a_man-stale-manifest-digest tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_man-uppercase-manifest-entry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT A21 anchor rc-mirror killed by=a_man-uppercase-manifest-entry -- plans/anchor_digest_check.py:44-46 'the digest that entry lists, and the digest of the com
MUTANT A22 anchor rc-mirror killed by=a_man-stale-manifest-digest -- plans/anchor_digest_check.py:44-46 (as A21: the manifest entry is an accepted view of the 
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
EXIT=0
```

Every FIXTURE line is `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0`, and each of A21/A22 is
`killed by=` one of this module's fids. `PINS`/`PINS-AFTER mismatched=0` show the three frozen tools were not
touched by the fixture build or runs.

## 6. Load-bearing table (each fixture removed in turn, same `--only A21,A22` command)

| module variant | A21 | A22 | flip vs both |
|---|---|---|---|
| both fixtures (delivered) | killed by `a_man-uppercase-manifest-entry` | killed by `a_man-stale-manifest-digest` | — |
| `a_man-uppercase-manifest-entry` removed | **SURVIVED** (`killed=1 survived=1`, exit 1) | killed by `a_man-stale-manifest-digest` | **A21 flips** |
| `a_man-stale-manifest-digest` removed | killed by `a_man-uppercase-manifest-entry` | killed by `a_man-uppercase-manifest-entry` (attribution moves off the stale fixture) | none |

Receipts: `receipts/loadbearing-without-uppercase.txt`, `receipts/loadbearing-without-stale.txt` (variants were
built by deleting exactly one two-line `FIXTURES` entry from a copy of the module; the delivered module was not
modified).

**Measured coupling (named, not hidden).** Only the uppercase fixture is load-bearing under removal, because the
view A21's case folding breaks *is* the view A22 deletes: any `rc-mirror` fixture that makes the reference accept
through a lowercased manifest digest necessarily makes A22's mutant refuse (the anchored digest then survives only
in `dir_entries`, so A22 prints `digest-wrong-capture`). Conversely a stale-lowercase-manifest fixture leaves A21
byte-identical to the reference (it is the mutant's own pre-freeze witness shape X20). So the stale fixture is a
second, independent witness for A22 (it *is* the A22 killer when the uppercase fixture is absent, row 2 above),
but it cannot flip a mutant that the uppercase fixture does not already kill. I could not construct a fixture that
kills A21 without also killing A22; the argument is in §7.

## 7. Why no A21-only fixture exists (limit)

For A21 to be killed in `rc-mirror` the reference must exit 0 and the mutant 1 on an `expect=accept` fixture, so the
row's anchor token `T` must be in the reference's capture digest set and out of the mutant's. The only digest the
mutation changes is a manifest digest whose written spelling is uppercase, so `T` must be the lowercased manifest
digest and must not be the committed blob digest (if the blob digest were `T`, A21's set would still contain it via
`file_digest` and the mutant would accept). A22's mutant keeps `file_digest` and drops only the manifest view, so
`T` is out of its set too; with `dir_entries` intact the token is still a committed capture, hence
`digest-wrong-capture` and exit 1. The coupling is structural, not an artefact of either fixture. It is recorded as
a limit rather than papered over; a later seat that shows it false should replace this paragraph with the witness.

## 8. Full default counter (module copied into the clone's `plans/battery40/`)

```
cp .../battery/a_man.py "$S/lane/plans/battery40/a_man.py"
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round40_c1_verify.py --lane "$S/lane" --work "$S/w3"
```

```
PINS total=3 mismatched=0
FIXTURE a_man-stale-manifest-digest tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_man-uppercase-manifest-entry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT A01 anchor silence SURVIVED exhibits=none -- ...
MUTANT A02 anchor rc-silence SURVIVED exhibits=none -- ...
MUTANT A03 anchor rc-silence SURVIVED exhibits=none -- ...
MUTANT A06 anchor rc-mirror SURVIVED exhibits=none -- ...
MUTANT A08 anchor rc-silence SURVIVED exhibits=none -- ...
MUTANT A09 anchor rc-silence SURVIVED exhibits=none -- ...
MUTANT A15 anchor rc-silence SURVIVED exhibits=none -- ...
MUTANT A17 anchor rc-mirror SURVIVED exhibits=none -- ...
MUTANT A21 anchor rc-mirror killed by=a_man-uppercase-manifest-entry -- plans/anchor_digest_check.py:44-46 'the digest that entry lists, and the digest of the com
MUTANT A22 anchor rc-mirror killed by=a_man-stale-manifest-digest -- plans/anchor_digest_check.py:44-46 (as A21: the manifest entry is an accepted view of the 
MUTANT A27 anchor silence SURVIVED exhibits=none -- ...
MUTANT L01 ledger error SURVIVED exhibits=none -- ...
MUTANT L05 ledger rc-silence SURVIVED exhibits=none -- ...
MUTANT L06 ledger rc-silence SURVIVED exhibits=none -- ...
MUTANT L11 ledger error SURVIVED exhibits=none -- ...
MUTANT L14 ledger rc-silence SURVIVED exhibits=none -- ...
MUTANT L15 ledger rc-silence SURVIVED exhibits=none -- ...
MUTANT L21 ledger error SURVIVED exhibits=none -- ...
MUTANT O04 order rc-silence SURVIVED exhibits=none -- ...
MUTANT O12 order rc-error SURVIVED exhibits=none -- ...
MUTANT O14 order error SURVIVED exhibits=none -- ...
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=2 survived=19 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```

Full text: `receipts/full-default-run.txt` (mutant heads elided above only in the `... ` labels, never in the
killed lines; the file holds every line verbatim). The 19 survivals are other seats' assignments — this module is
the only battery40 module in that clone — so `PREDICATE C1 fail` here is the expected wave-1 state, not a defect
of `a_man`.

## 9. Risks / notes for the L1

- **Attribution vs intent** (the claims' own limit): the counter records a result difference in the declared
  direction. The probe in §4 is the supporting evidence that the difference is the manifest view, not an accident:
  the mutant's class is the one the deleted branch predicts (`digest-wrong-capture` for A22, `digest-unknown` for
  A21).
- **Head mode, not index mode.** The fixtures read HEAD blobs (`--evidence-ref head`), unlike the pre-freeze X20/X21
  witnesses which staged index blobs. Reason: the fixture repositories are self-contained and commit everything, so
  head mode needs no staged state and cannot be perturbed by an unrelated mutant (`A17` swaps the two modes); the
  advertised sentence is mode-independent. Measured consequence: neither fixture kills A17 (correctly — it does not
  exercise `index`).
- **No lane dependence.** The fixtures do not read `ctx.lane`'s corpus, so a C2 landing (new SOURCES rows/evidence)
  cannot change these reference results. `ctx.lane` is only the clone source for `ctx.init`.
- **Tooling:** nothing installed or upgraded; `python3` (stdlib), `git`, `/usr/bin/bwrap` were already present.
  No pacman transaction.
- **Scratch** `/fast/scratch/hyaku/kengaku-r40/R40BatAnchorManifest/` (clones, fixture trees, probe) is removed
  before finish; receipts above were copied into this report dir first.

VERDICT: battery40-a_man-killed-2/2-wrong-0
