# F40XMutAnchor — near-variant mutants of `plans/anchor_digest_check.py` (round 40, wave 2 FALSIFY)

Seat: F40XMutAnchor · lane tip measured: `ec1005a2a28bc5cfdde7723374368ed4cc956eed` (branch master) · date 2026-10-26.
Attack: the C1 calibration's anchor-tool coverage — the frozen 21-mutant battery
(`plans/round40_c1_verify.py`, predicate `MUTANTS total=21 killed=21`) is challenged with **16
near-variant single-replacement mutants of `plans/anchor_digest_check.py` that are not in the frozen
list**. A finding is a receipt: every survivor below carries a witness input that was built, run and
measured in this seat's scratch.

---

## 1. Protocol

Scratch (operator directive): `S=/fast/scratch/hyaku/kengaku-r40/F40XMutAnchor`, `TMPDIR=$S`,
`git clone -q --no-local <lane> $S/lane && git -C $S/lane checkout -q ec1005a2a28bc5cfdde7723374368ed4cc956eed`;
`git -C $S/lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r40/F40XMutAnchor/lane`,
`git -C $S/lane status --porcelain | wc -l` → `0`. The lane was never written to.

HOST-SAFETY wrapper (orchestrator ruling), used for every counter invocation, battery build and
tool/mutant run below:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>
```

Harness: the frozen counter `plans/round40_c1_verify.py` (unedited) run 1 validates the harness on my
clone; run 2 is the same counter **copied to scratch and its `MUTANTS` table swapped** for the 16
near-variants below (`TOTAL=16`; the `PREDICATE C1` line of the swapped copy is therefore n/a — the
frozen predicate belongs to the frozen table). Per-mutant verdict = the counter's own kill rule: killed
iff some battery40 fixture exhibits the mutant's declared direction. Two extra passes:

- **tip run** — every variant and the reference run on the lane clone itself
  (`python3 <variant> --lane $S/lane`), receipt `tiprun/*.out`, rc/summary in `tiprun-rc.txt`;
- **witnesses** — for every survivor, a minimal one-row repo built in scratch, reference vs mutant run
  on it, receipt `wit/*.out` + `wit-summary.json` (builder: `witness.py`).

No tool was installed or upgraded (none needed; `bwrap 0.13.1`, `Python 3.14.8` already present).

## 2. Baseline — frozen counter on my clean clone (harness validation)

Command: `python3 $S/lane/plans/round40_c1_verify.py --lane $S/lane --work $S/work --jobs 8` inside the
wrapper → `baseline-frozen-counter.txt` (79 s):

```
BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 pass            (rc=0)
```

Matches the landing measurement (`measure-final.txt`). The anchor fixtures' declared classes
(`grep '^FIXTURE' baseline-frozen-counter.txt`): `capture-unanchored`, `anchor-unbound`,
`token-outside-anchor`, `row-malformed`, `digest-uppercase`, `abbrev-unresolved` — and nothing else.
That map predicts the survivors below.

## 3. The 16 near-variant mutants

Single `old -> new` replacements of `plans/anchor_digest_check.py` at the tip; every `old` occurs
exactly once (counter check `src.count(old) != 1`, `invalid=0` in the final run); all 16 compile; none
is a frozen `(old,new)` pair — X8/X9 share A08's/A09's *site* but replace it differently (near-variants,
as tasked). Full table: `xmut_table.py`; variant hashes in §7.

| id | site (file:line) | replacement (abbreviated) | direction/class | battery verdict |
|----|------------------|---------------------------|-----------------|-----------------|
| X1 | :318 | `got = [(cap, "provenance-row") ...]` → `got = []` (binding route 1 removed) | rc-mirror | **SURVIVED** |
| X2 | :356 | `got.append((p, "row-path"))` → `pass` (binding route 3 removed) | rc-mirror | killed |
| X3 | :343 | `if (repo, subpath) in idx["prov_url"]:` → `if False:` (route-2 provenance-URL fallback removed) | rc-mirror | **SURVIVED** |
| X4 | :467 | `elif cited_wrong:` → `elif False:` (erratum exemption never granted) | rc-mirror | killed |
| X5 | :148 | erratum regex `\(round 37\)` → `\(round 38\)` (no erratum ever loads) | rc-mirror | killed |
| X6 | :527-528 | `if tok in allowed:` → `if False:` (`digest-wrong-capture` collapses into `digest-unknown`) | silence/digest-wrong-capture | **SURVIVED** |
| X7 | :535 | `class=digest-unknown` → `class=digest-wrong-capture` (classes swapped) | silence/digest-unknown | **SURVIVED** |
| X8 | :489 | `if cell_idx != ANCHOR_CELL:` → `... and tok not in allowed:` (outside-token excused when committed) | silence/token-outside-anchor | killed |
| X9 | :477 | `if len(r["cells"]) != NCELLS:` → `> NCELLS` (short rows no longer malformed) | rc-silence | **SURVIVED** |
| X10 | :147 | TOKEN regex: ellipsis group `)?` → `)` (plain tokens no longer collected) | silence/digest-uppercase | killed |
| X11 | :306 | `if path in idx["file_digest"]:` → `if False:` (committed-bytes view of a capture dropped) | rc-mirror | killed |
| X12 | :256 | slug pick fallback `names[0] if names else None` → `None` (slash-less `name=` unbinds) | rc-mirror | **SURVIVED** |
| X13 | :570 | `default="head"` → `default="index"` (default ref reads staged blobs) | rc-silence | **SURVIVED** |
| X14 | :458 | erratum scan `HEX64_ANY` → `HEX64` (uppercase erratum tokens unchecked) | silence/erratum-digest-unresolved | **SURVIVED** |
| X15 | :455 | erratum support `t in row_scope if ... else t in allowed` → `t in allowed` (sibling-digest laundering) | rc-silence | **SURVIVED** |
| X16 | :524 | `cls = "digest-uppercase"` → `cls = "digest-short"` (wrong class emitted) | silence/digest-uppercase | killed |

Final receipt `xmut-run-final.txt` (command as §1, `--work $S/work4`):

```
PINS total=3 mismatched=0
BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=16 killed=7 survived=9 invalid=0 null_detected=0
PINS-AFTER mismatched=0
```

## 4. Killed (7) — the battery holds on every near-variant site it demonstrates

| id | killed by (counter output) | why the fixture sees it |
|----|----------------------------|-------------------------|
| X2 | `a_bind-a17-index-bytes` | the fixture is a lane clone: S036/S114 bind only by row path (`tiprun/X2.out`: `defects=2`, S036+S114 `anchor-unbound`); `a_man` rows bind the same way |
| X4 | `a_bind-a17-index-bytes` | the lane's live erratum is load-bearing: S110 still carries its 63-hex wrong token (`corpus/SOURCES.md:125`), so dropping the exemption prints `digest-short` (`tiprun/X4.out`: `defects=1`) |
| X5 | `a_bind-a17-index-bytes` | same S110 erratum: a round-38 regex loads no erratum → `digest-short` |
| X8 | `a_row-token-in-teaches` | the moved token is S111's own committed digest, i.e. `tok in allowed`, so the narrowed gate excuses it and `token-outside-anchor` vanishes |
| X10 | `a_tok-upper-anchor` | a plain (non-ellipsis) token is no longer collected, so the uppercase claim goes unseen; on the tip the mutant also flips rc 0→1 (`tiprun/X10.out`: `tokens=1 defects=1`, the S110 erratum becomes `erratum-incomplete`) |
| X11 | `a_bind-a17-index-bytes` | the committed-bytes view is load-bearing for the lane's own S036 (`corpus/evidence/attrib-r23-stream.log` has no `SHA256SUMS` entry; `tiprun/X11.out`: S036 `anchor-unbound`, `defects=1`) |
| X16 | `a_tok-upper-anchor` | the fixture declares `digest-uppercase`; the mutant emits `digest-short` instead |

## 5. Survivors (9) — round-41 candidates, each with a built and measured witness

Every survivor shows **no delta on any battery40 fixture and none on the tip run** (`tiprun-rc.txt`:
rc=0, `defects=0`, `tokens=21` for all nine) — the advertised behaviour it breaks is demonstrated
nowhere in the lane's own data. Each witness below was built in scratch and measured
(`witness-run.txt`, outputs `wit/<name>.{ref,X<id>}.out`); all nine kill their mutant in the declared
direction.

| id | undemonstrated behaviour (advert sentence, file:line) | witness input (built at `wit/<name>/`) | measured ref → mutant |
|----|------------------------------------------------------|----------------------------------------|------------------------|
| X1 | route 1's *primacy*: "a committed markdown under `corpus/evidence/` whose table line carries this row's id" (:50-52) | `w1-provrow-only`: PROVENANCE.md table line ticks `capture.txt` beside it and carries **no pinned URL**; row S900 has no other locator | ref rc0/- → mut rc1/`anchor-unbound` (rc-mirror) |
| X3 | route-2 fallback: "A provenance URL ... is consulted when the `task.toml` route finds nothing" (:57-58) | `w3-provurl-fallback`: PROVENANCE.md line with the pinned URL + ticked file, **no row id**, no `task.toml` anywhere; row S901 carries that URL | ref rc0/- → mut rc1/`anchor-unbound` (rc-mirror) |
| X6 | "A 64-hex token that is a committed capture but not this row's is `digest-wrong-capture`" (:89-92) — no fixture declares the class | `w6-wrong-capture-class`: two captures; row S902 binds capture A by row path, anchors capture B's committed digest | ref rc1/`digest-wrong-capture` → mut rc1/`digest-unknown` (silence) |
| X7 | "a token that is no committed capture at all is `digest-unknown`" (:92-93) — no fixture declares the class | `w7-unknown-class`: row S903 bound to a real capture, anchored on a made-up 64-hex digest | ref rc1/`digest-unknown` → mut rc1/`digest-wrong-capture` (silence) |
| X9 | "A row that matches the census regex but does not have 11 cells is a `row-malformed` defect" (:34-35) — only a 12-cell row is demonstrated | `w9-short-row`: row S909 with the used-by cell dropped (10 cells), correct digest | ref rc1/`row-malformed` → mut rc0/- (rc-silence) |
| X12 | slug fallback: "matched **exactly** against the `name = \"<org>/<task>\"` a committed `task.toml` gives" (:55-56) — every committed task.toml names `<org>/<task>`, so the slash-less fallback is never exercised | `w12-slashless-slug`: `task.toml` with `name = "plain-slug"`; row S905 pins `.../plain-slug/tests/test_outputs.py` | ref rc0/- → mut rc1/`anchor-unbound` (rc-mirror) |
| X13 | "`--evidence-ref head` (default) reads HEAD blobs, so an unpromoted capture never counts" (:73) | `w13-default-ref-index`: capture committed, then rewritten + staged (row and SHA256SUMS claim the staged digest); tool run with **no** `--evidence-ref` | ref rc1/`digest-unknown` → mut rc0/- (rc-silence) |
| X14 | "no 64-hex token on it may be outside A unless it is the cited wrong token" (:111-113) — the tip's single erratum line has only lowercase tokens | `w14-erratum-upper`: erratum line `Erratum (round 37): S907 anchor sha256 <UPPER-BOGUS> ... sha256 <correct>`; row already repaired | ref rc1/`erratum-digest-unresolved` → mut rc0/- (silence) |
| X15 | erratum scoping: "at least one other token that is 64 lowercase hex and a digest **of the capture that row names**" (:108-110) | `w15-erratum-global-A`: row S908 anchors a made-up digest; its erratum "corrects" with a **sibling row's** committed digest | ref rc1/`digest-unknown,erratum-incomplete` → mut rc0/- (rc-silence) |

Witness receipts: `wit/w1-provrow-only.*.out`, `wit/w3-provurl-fallback.*.out`,
`wit/w6-wrong-capture-class.*.out`, `wit/w7-unknown-class.*.out`, `wit/w9-short-row.*.out`,
`wit/w11-blob-view.*.out` (supplementary — X11 is battery-killed; the witness isolates the file view:
ref rc0/- → mut rc1/`digest-wrong-capture`), `wit/w12-slashless-slug.*.out`,
`wit/w13-default-ref-index.*.out`, `wit/w14-erratum-upper.*.out`, `wit/w15-erratum-global-A.*.out`,
summary `wit/wit-summary.json` (`kills: true` ×10).

Two masking facts worth carrying into round 41 (both measured, not inferred):

- X1 survives *because of* X3's route: on the tip, S070/S072/S073/S074 bind by `provenance-row`
  (`tiprun/ref.out` BIND lines), but the same PROVENANCE.md lines carry the pinned URLs, so the
  `prov_url` fallback rebinds them when route 1 is removed — the two routes cover each other's absence,
  and only a fixture with a URL-less PROVENANCE line (W1) or an id-less one (W3) separates them.
- The battery's anchor fixtures declare only 6 of the tool's ~12 defect classes; `digest-short`,
  `digest-long`, `digest-wrong-capture`, `digest-unknown`, `erratum-digest-unresolved`,
  `erratum-incomplete` are declared by none (§2 fixture map), which is what X6/X7/X9/X14/X15 exploit.

## 6. `--verbose` path — negative result (no behavior-bearing mutant exists there)

The tasked `--verbose` area is empty in this copy: every use gates note printing only —
`grep -n verbose plans/anchor_digest_check.py` → :440, :469, :485, :515, :541, :548, :558 are
`if verbose:` guards around `notes.append`/the final note dump, :571 is the flag itself, :581 passes it
to `check`. No rc, defect class or binding depends on it, so any single replacement there is equivalent
by construction (the counter's directions cannot see it — the same reason the frozen list excludes
text-only mutants, `round40_c1_verify.py` docstring "Limits named at the freeze"). Not counted in n.

## 7. Run-integrity notes

- **X10 first-run artifact, superseded**: the first swapped run (`xmut-run.txt`) counted X10 as killed,
  but its replacement string was malformed (one paren short) and the variant died on import — a crash,
  not a kill (the counter has no crash check for variants; `tiprun` exposed it:
  `re.PatternError: missing )`). The replacement was fixed (same site, corrected `new`), the table
  regenerated, and X10 re-measured: `xmut-run-X10-only.txt` → `killed by=a_tok-upper-anchor` with a
  running variant; the final full run `xmut-run-final.txt` (§3) is the receipt of record.
- Variant sha256 (before runs; the counter re-hashes after and reported no
  `invalid(variant changed)`): X1 `48e25dfe…`, X2 `0bcee175…`, X3 `d6d39d80…`, X4 `11c82c1e…`,
  X5 `3e68429d…`, X6 `0bd3ce9c…`, X7 `87aacb2b…`, X8 `3e5c2ee5…`, X9 `3315588c…`, X10 `b9abe47e…`,
  X11 `f1ab1c94…`, X12 `7d0552e4…`, X13 `00e5691d…`, X14 `42e37298…`, X15 `623e2214…`,
  X16 `6d38d721…` (full digests in the transcript; files themselves were scratch-only and are deleted
  with the scratch).
- `null_detected=0` and `tampered=0` in every run; `PINS-AFTER mismatched=0` in every run.
- Restoration: the real lane's three tools still hash to the frozen pins —
  `sha256sum plans/{anchor_digest_check,ledger_tip,order_check}.py` →
  `11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2`,
  `853bcb2a5052b3c2319d3006459bb5012ba72dfc1e5f22874f7334b62eb77ad4`,
  `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc` — i.e. byte-identical to the
  counter's `PINS`; the lane was never written. Scratch `S` is removed after this report
  (`rm -rf -- /fast/scratch/hyaku/kengaku-r40/F40XMutAnchor`); no process is left running.

## 8. Receipts (paths relative to the lane root)

- `/.ufo/waves/round-40/falsify/F40XMutAnchor/baseline-frozen-counter.txt` — frozen counter, predicate pass
- `/.ufo/waves/round-40/falsify/F40XMutAnchor/xmut-run-final.txt` — 16 near-variants: 7 killed / 9 survived
- `/.ufo/waves/round-40/falsify/F40XMutAnchor/xmut-run.txt`, `xmut-run-X10-only.txt` — first run (superseded X10) and its re-measure
- `/.ufo/waves/round-40/falsify/F40XMutAnchor/tiprun-rc.txt`, `tiprun/ref.out`, `tiprun/X1.out` … `tiprun/X16.out` — tip-run pass
- `/.ufo/waves/round-40/falsify/F40XMutAnchor/witness-run.txt`, `wit/wit-summary.json`, `wit/*.out` — survivor witnesses
- `/.ufo/waves/round-40/falsify/F40XMutAnchor/xmut_table.py` — the swapped MUTANTS table
- `/.ufo/waves/round-40/falsify/F40XMutAnchor/witness.py`, `round40_c1_xmut.py` — witness builder and swapped counter copy

VERDICT: anchor-xmut-killed-7/16
