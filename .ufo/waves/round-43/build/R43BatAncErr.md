# R43BatAncErr — battery43 `a_err`: erratum-exemption fixtures for NA7, NA20, NA21 (wave 1, 2026-10-26)

Seat: `R43BatAncErr` (executor, leaf). Lane repo cloned read-only-by-rule to scratch; nothing in
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` was edited except this report and my own build subdir.

- Deliverable: `.ufo/waves/round-43/build/R43BatAncErr/battery/a_err.py`, sha256
  `2c41e02a38fcdb115890be9d8db83e72f20171a2a1111999c6b1a936e9772b6e` (10091 bytes, stdlib only, `hashlib`).
- Frozen inputs untouched: the first line of every counter run below is
  `PINS total=2 mismatched=0` and the last is `PINS-AFTER mismatched=0`. No file under the lane was written;
  the module was developed in the build dir and copied only into my scratch clone (`$S/lane/plans/battery43/`).
- No tool installed or upgraded this wave (nothing needed); no package manager invoked.

Scratch: `S=/fast/scratch/hyaku/kengaku-r43/R43BatAncErr`; `TMPDIR="$S"`. Clone verified:
`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r43/R43BatAncErr/lane`
(tip `d33350f`, freeze `02753f2` present).

## 1. What the fixtures target

Three frozen mutants, all in `plans/anchor_digest_check.py`, all declared `rc-mirror` (fixture `expect=accept`,
reference exits 0, mutant exits 1). The replaced spans (line numbers from the frozen tool):

| id | tool line | `old -> new` | advertised sentence (file:line) |
|----|-----------|--------------|----------------------------------|
| NA7 | 458 | `if HEX64_ANY.fullmatch(t) and t not in allowed and t not in cited_wrong:` → drops `t not in allowed` | `anchor_digest_check.py:112-113` “no 64-hex token on it may be outside A unless it is the cited wrong token of the row it names” |
| NA20 | 468 | `exempt.setdefault(sid, (path, lineno, cited_wrong[0], supported[0]))` → `pass` | `anchor_digest_check.py:108-110` “An erratum for S<id> exempts that row's anchor token from *every* anchor class above when it carries the row's exact wrong token” |
| NA21 | 456 | `cited_wrong = [t for t, _ in toks if t in anchor_tokens.get(sid, ())]` → `t in anchor_tokens` | `anchor_digest_check.py:108-109` “An erratum for S<id> exempts that row's anchor token … when it carries the row's exact wrong token” |

Measured mechanism (line numbers confirmed by
`grep -n "cited_wrong\|exempt.setdefault\|HEX64_ANY.fullmatch" plans/anchor_digest_check.py` →
`456:`, `458:`, `467:`, `468:`):

- **NA20** never populates `exempt`, so a row that is green only because its stale anchor token is excused falls
  back to the ordinary token classes.
- **NA21** makes `cited_wrong` a dict-key test against `{S\d{3,}}` keys, i.e. always `[]`: no exemption is ever
  granted **and** the erratum line's own check loses its cited-token excuse, so any 64-hex token on the line that
  is outside A is flagged `erratum-digest-unresolved`.
- **NA7** keeps the exemption but flags the *correction* digest (a committed capture, so in A, and not one of the
  row's anchor tokens) as `erratum-digest-unresolved` — including on a lane that needed no exemption at all.

## 2. The six fixtures (all `tool=anchor`, `expect=accept`, `defects=[]`)

Each build() creates its repo from nothing in the empty fixture dir (`ctx.init`, `ctx.write`, `ctx.git` only;
no clone, no lane read) and returns `["--lane", <abs path inside d>]`. One-line docstring per fixture names the
branch it demonstrates.

| fid | shape | why the reference stays green | which mutant it is built for |
|-----|-------|-------------------------------|------------------------------|
| `a_err-f1-repaired-row-historical-erratum` | one row, already repaired (anchor = its capture's digest), explicit `corpus/evidence/…` path; **historical** erratum citing the old capture's digest + the current one; one commit | row token resolves; both erratum tokens are committed captures | NA7 only — the exemption is not needed, so only the dropped allowed-guard can redden the lane |
| `a_err-f2-two-rows-provenance-two-errata` | **two** rows bound only through `corpus/evidence/…/PROVENANCE.md`; two historical errata; **three commits** (evidence+provenance, rows, errata) | both rows resolve via `BIND … by=provenance-row` | NA7 only, second shape |
| `a_err-f3-stale-token-sibling-capture` | one row; the stale anchor token **is a sibling file's committed capture** (in A) | only the exemption keeps the row green (`EXEMPT S451 …`) | NA20 + NA21 (and NA7) |
| `a_err-f4-manifest-only-second-capture` | one row naming **two** captures, the second present only as a `SHA256SUMS` entry (`ghost.bin`, no committed bytes); stale token is no committed digest; three commits | exemption skips the anchor loop and the `capture-unanchored` check (`defects=0`, `CAPTURES` not reached) | NA20 + NA21 (and NA7); NA21 additionally flags the unknown stale token on the erratum line |
| `a_err-f5-row-carrying-both-tokens` | the anchor cell carries **two** tokens — the right digest and a sibling's committed capture; the erratum line names both | exemption granted, and the erratum line has no token outside `cited_wrong` | NA20 + NA21 **only** — NA7's dropped guard changes nothing because every erratum token is a row anchor token |
| `a_err-f6-provenance-bound-unknown-stale` | provenance-bound row, stale token no committed file carries, **two commits**, no path in the row text | exemption via `BIND … by=provenance-row` | NA20 + NA21 (and NA7) |

Namespace: every fid starts `a_err-`. Sidechannel scan (same tuple as the counter, case-insensitive, over the
module text) → `hits []`.

## 3. Evidence — required dev run (must be `ok`, 3/3, `wrong=0`)

```
$ /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/envelope.sh "$S/env" \
    /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py \
    --lane "$S/lane" --battery-dir <build>/R43BatAncErr/battery --only NA7,NA20,NA21 --work "$S/w"
ENVELOPE start 19:09:57 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE a_err-f1-repaired-row-historical-erratum tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_err-f2-two-rows-provenance-two-errata tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_err-f3-stale-token-sibling-capture tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_err-f4-manifest-only-second-capture tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_err-f5-row-carrying-both-tokens tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_err-f6-provenance-bound-unknown-stale tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT NA7 anchor rc-mirror killed by=a_err-f1-repaired-row-historical-erratum attributed=L458 value=differs hits=5
MUTANT NA20 anchor rc-mirror killed by=a_err-f3-stale-token-sibling-capture attributed=L468 value=differs hits=4
MUTANT NA21 anchor rc-mirror killed by=a_err-f3-stale-token-sibling-capture attributed=L456 value=differs hits=4
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/3 order=0/0
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:10:00 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

(`--` advancement labels elided.) Every FIXTURE line `ok` → each `defects` set is exactly the reference's
(∅) and each `expect` matches the reference exit code (0). `attributed=L458/L468/L456` are the three replaced
span lines; `value=differs` is leg g.

## 4. Calibration matrix — one fixture at a time

Six single-fixture battery dirs (`$S/bat/onlyN`), same command with `--battery-dir $S/bat/onlyN`:

| fixture | NA7 | NA20 | NA21 | run exit |
|---------|-----|------|------|----------|
| f1 repaired-row-historical-erratum | **killed** L458 | survived | survived | 1 |
| f2 two-rows-provenance-two-errata | **killed** L458 | survived | survived | 1 |
| f3 stale-token-sibling-capture | **killed** L458 | **killed** L468 | **killed** L456 | 0 |
| f4 manifest-only-second-capture | **killed** L458 | **killed** L468 | **killed** L456 | 0 |
| f5 row-carrying-both-tokens | survived | **killed** L468 | **killed** L456 | 1 |
| f6 provenance-bound-unknown-stale | **killed** L458 | **killed** L468 | **killed** L456 | 0 |

Every mutant therefore has 4–5 killing fixtures of different shapes (requirement: ≥2), and f1/f2 isolate NA7
from the exemption family while f5 isolates NA20/NA21 from NA7. All six runs printed
`FIXTURE … ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0 unattributed=0`, and every envelope ended
`unchanged` (`19:10:37 … 19:10:55`).

**Defect classes** the reference and the three variants actually print (direct runs of the pinned tool and of
`old -> new` copies on the six built fixtures, inside the envelope; `19:12:12–19:12:15 … unchanged`):

| fixture | ref | NA7 | NA20 | NA21 |
|---------|-----|-----|------|------|
| f1 | rc0 ∅ | rc1 `erratum-digest-unresolved` | rc0 ∅ | rc0 ∅ |
| f2 | rc0 ∅ | rc1 `erratum-digest-unresolved` | rc0 ∅ | rc0 ∅ |
| f3 | rc0 ∅ | rc1 `erratum-digest-unresolved` | rc1 `digest-wrong-capture` | rc1 `digest-wrong-capture` |
| f4 | rc0 ∅ | rc1 `erratum-digest-unresolved` (2 defects) | rc1 `capture-unanchored,digest-unknown` | rc1 `capture-unanchored,digest-unknown,erratum-digest-unresolved` |
| f5 | rc0 ∅ | rc0 ∅ | rc1 `digest-wrong-capture` | rc1 `digest-wrong-capture` |
| f6 | rc0 ∅ | rc1 `erratum-digest-unresolved` | rc1 `digest-unknown` | rc1 `digest-unknown,erratum-digest-unresolved` |

This is the declared direction measured in its own terms: reference `defects=0` exit 0, mutant exit 1. Sample
exemption proof (reference, `--verbose`, f3):

```
ERRATUM S451 loc=corpus/lessons/round-43-a-err.md:1 cited_wrong=['f106fb76…'] correction=['f693a343…']
EXEMPT S451 anchor=f106fb76… by=corpus/lessons/round-43-a-err.md:1 correction=f693a343…
rows=1 tokens=1 defects=0
```

and the same row under NA20 prints
`DEFECT S451 … class=digest-wrong-capture detail=committed-capture-belonging-to-another-capture-…other.txt-not-the-capture-this-row-names-…mine.txt`
(`rows=1 tokens=1 defects=1`; envelopes `19:12:42–19:12:43` and `19:12:45–19:12:47`, both `unchanged`).

## 5. Load-bearing table — remove each fixture in turn

Six battery dirs each holding five of the six fixtures (`$S/bat/dropN`), same dev command:

| removed | NA7 killed by | NA20 killed by | NA21 killed by | any mutant flips to survived? |
|---------|---------------|----------------|----------------|-------------------------------|
| f1 | f2 | f3 | f3 | no |
| f2 | f1 | f3 | f3 | no |
| f3 | f1 | f4 | f4 | no |
| f4 | f1 | f3 | f3 | no |
| f5 | f1 | f3 | f3 | no |
| f6 | f1 | f3 | f3 | no |

All six runs: `MUTANTS total=3 killed=3 survived=0 invalid=0 …`, envelopes `19:11:06 … 19:11:28`, all
`unchanged`. **No single fixture is load-bearing**, which is the deliberate consequence of ≥2 shapes per
mutant; redundancy, not overlap by accident. The matrix in §4 is the informative half: it shows *which* shapes
carry *which* line.

A predicted minimal cover was then measured rather than asserted: {f1, f5} kills all three
(`MUTANT NA7 … killed by=a_err-f1…`, `MUTANT NA20/NA21 … killed by=a_err-f5…`,
`MUTANTS total=3 killed=3 survived=0`, envelope `19:11:38 … unchanged`). The matrix therefore predicts the
combined battery, not just the single-fixture runs.

## 6. Full default counter on the clone (module in `plans/battery43/`)

```
$ cp <build>/R43BatAncErr/battery/a_err.py "$S/lane/plans/battery43/a_err.py"
$ envelope.sh "$S/env" python3 …/plans/round43_c1_verify.py --lane "$S/lane" --work "$S/w2"
PINS total=2 mismatched=0
FIXTURE a_err-f1-repaired-row-historical-erratum tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
… (all six FIXTURE lines ok) …
MUTANT NA1 anchor silence SURVIVED exhibits=none
MUTANT NA5 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA7 anchor rc-mirror killed by=a_err-f1-repaired-row-historical-erratum attributed=L458 value=differs hits=5
MUTANT NA18 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA20 anchor rc-mirror killed by=a_err-f3-stale-token-sibling-capture attributed=L468 value=differs hits=4
MUTANT NA21 anchor rc-mirror killed by=a_err-f3-stale-token-sibling-capture attributed=L456 value=differs hits=4
MUTANT NO5 order rc-silence SURVIVED exhibits=none
MUTANT NO7 order rc-mirror SURVIVED exhibits=none
MUTANT NO22 order rc-silence SURVIVED exhibits=none
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=3 survived=6 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/6 order=0/3
ADVERTISED direct=8 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 19:11:46 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`PREDICATE C1 fail` here is expected: this clone's `plans/battery43/` holds only `a_err.py`, so NA1 NA5 NA18
and the three order mutants stay alive. They belong to the sibling wave-1 seats; my six fixtures change nothing
about them (`wrong=0`, no null detection, no sidechannel).

## 7. Re-spelling check (non-author review still required)

`claims/witness/w_near.py` carries exactly **one** erratum fixture: single row, stale digest of uncommitted
bytes, stale token in the anchor cell, one erratum line, one commit, green only through the exemption.
`a_err.py` shares with it only the 11-cell census header literal (the tool's own row format) and the
`Erratum (round 37):` sentence shape (the tool's `ERRATUM` regex). Differences: no shared helper names or
bodies; f1/f2 are the opposite situation (row already repaired — the exemption is *not* what makes the lane
green); f2 and f6 bind through `PROVENANCE.md`; f3 and f5 use a *committed sibling* capture as the stale token;
f4 has a manifest-only second capture; f5 puts two tokens in the anchor cell. The module neither imports nor
reads `claims/witness/`; it opens no file at all.

## 8. Limits named

1. **NA20 cannot be killed without NA21 on a single fixture.** NA21's replaced membership test is a dict-key
   test that is always false, so on any lane whose greenness depends on an exemption it both denies the
   exemption (killing NA20's target behaviour) and, when the stale token is no committed digest, flags the
   erratum line itself. f5 is the closest separation available — NA20+NA21 killed, NA7 green — and is reported
   as the shape that isolates NA7 from the membership effect, never as an NA20-only fixture.
2. **Kills are exit-code + leg-g facts, not intent.** The `rc-mirror` direction constrains only the reference
   (0) and mutant (1) exit codes; the defect classes in §4 are recorded as information, and the counter's leg f
   (span line ran) and leg g (site record differs) are what make each kill attributable.
3. **No single fixture is load-bearing** by construction (see §5); the per-fixture matrix in §4 is the
   calibration evidence, and the measured {f1,f5} cover shows the matrix composes.
4. **This clone shows 3/9.** The other six frozen mutants need the sibling seats' modules; a green full
   counter is the L1's integration result, not this seat's.
5. **Fixture text is tied to the frozen tool's erratum semantics** (round-37 wording, `ERRATUM`/`TOKEN`/
   `HEX64_ANY` regexes). If `plans/anchor_digest_check.py` moves, `PINS total=2 mismatched=1` fires before any
   fixture result is believed — the fixtures were built against the pinned `11bb2cad…` copy only.
6. The battery is a **draft in the build dir** for the L1; it was never written into the real lane or committed
   anywhere. `$S/lane/plans/battery43/` exists in scratch only.
7. Nested sandboxes worked on this host (envelope → counter → build/run `bwrap`); every run's PATH-dir content
   digest is identical before/after, so no measurement was invalidated. No installs, no writes to any PATH
   directory, `/usr`, `/etc`, or `$HOME` outside scratch.

VERDICT: battery43-a_err-killed-3/3-wrong-0
