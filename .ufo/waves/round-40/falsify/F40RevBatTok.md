# F40RevBatTok — non-author honesty review of `plans/battery40/a_tok.py` (targets A01,A02,A03)

Round 40 wave 2 (falsify), kengaku hyaku run 9, 2026-10-26. Lane tip measured: `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.
I read all 55 lines of `plans/battery40/a_tok.py` and the harness contract in `plans/round40_c1_verify.py`
(`--battery-dir`/`--only` dev path, `Ctx`, `build_module_child`, `exhibits`, `build_battery`), plus the
advertised sentences the `adv` cells cite (`plans/anchor_digest_check.py:84-85`, `:88-89` — both present verbatim
in the tool docstring, read at the tip). Every run below went through the HOST-SAFETY wrapper
(`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
--unshare-pid --die-with-parent`), lane = my scratch clone at the tip. Receipts:
`.ufo/waves/round-40/falsify/F40RevBatTok/receipts/{run-c1-a_tok.txt,build-probe.txt,fixture-inspect.txt}`.

## Run (counter, dev mode)

`python3 plans/round40_c1_verify.py --lane "$S/lane" --battery-dir "$S/battery" --only A01,A02,A03 --work "$S/w"` → RC=0:

```
PINS total=3 mismatched=0
FIXTURE a_tok-upper-anchor tool=anchor expect=reject declared=digest-uppercase observed_rc=1 observed=digest-uppercase ok
FIXTURE a_tok-abbrev-7hex tool=anchor expect=reject declared=abbrev-unresolved observed_rc=1 observed=abbrev-unresolved ok
FIXTURE a_tok-abbrev-64hex tool=anchor expect=reject declared=abbrev-unresolved observed_rc=1 observed=abbrev-unresolved ok
MUTANT A01 anchor silence killed by=a_tok-upper-anchor
MUTANT A02 anchor rc-silence killed by=a_tok-abbrev-7hex
MUTANT A03 anchor rc-silence killed by=a_tok-abbrev-64hex
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
```

## Per-fixture verdicts (honest / dishonest)

**a_tok-upper-anchor — HONEST** (`a_tok.py:29-32`, `_edit` at `a_tok.py:19-26`).
Build: `ctx.clone(d/"lane")`, then one replacement `sha256 <S111>` → uppercase in the clone's work-tree
`corpus/SOURCES.md`. The S111 constant matches HEAD (SOURCES.md:126, anchor cell ends
`sha256 526aee3d…53346b37`); `_edit` raises unless the token occurs exactly once (`a_tok.py:23-24`), so the edit
cannot silently hit the wrong row. Reference output on the fixture (verbose):
`DEFECT S111 anchor token=526AEE3D… class=digest-uppercase detail=64-hex-but-not-lowercase loc=corpus/SOURCES.md:126`,
rc=1, defects=1 — exactly the advertised sentence at `anchor_digest_check.py:88-89` ("must be exactly 64 lowercase
hex digits … `digest-uppercase` otherwise"). Pristine-lane baseline: 0 DEFECT lines, rc=0, so the edit is the sole
cause. No commit made (HEAD stays at the tip in all three clones); the tool reads SOURCES.md from the work tree and
evidence from HEAD, as its docstring advertises.

**a_tok-abbrev-7hex — HONEST** (`a_tok.py:35-38`).
Build: S036's anchor `sha256 afaae9dd…` → `sha256 afaae9d…` (7 hex). `afaae9d` is a true prefix of the committed
capture digest `afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131` (sha256sum of the work-tree log ==
`git cat-file HEAD:` blob, byte-identical), so the only failure is the 8-hex floor — exactly the mutated bound
(`8 <= len(tok) <= 63` → `1 <= …`). Direction rc-silence requires reference rc=1 **and mutant rc=0**; the harness
counted the kill, so the mutant genuinely accepts the 7-hex resolving prefix. That is the honest demonstration of
`anchor_digest_check.py:84-85`.

**a_tok-abbrev-64hex — HONEST** (`a_tok.py:41-45`).
Build: computes `sha256` of the clone's work-tree `corpus/evidence/attrib-r23-stream.log` — measured identical to
the HEAD blob — and writes `sha256 <full 64 hex>…` into S036. Reference: rc=1, `observed=abbrev-unresolved`
(64 > 63 window ceiling, `anchor_digest_check.py:84-85`); A03 (`<= 63` → `<= 64`) accepts it (rc-silence kill ⇒
mutant rc=0). The token is the true digest of the capture the row names, so the ellipsis is the only reason it
fails — no accidental `digest-unknown`/`digest-wrong-capture` contamination (declared set matched exactly).

## Wave-1 attack-vector checklist (none used)

| Vector (wave-1 counters) | In a_tok.py? | Evidence |
|---|---|---|
| Reads the tool / own program text at run time | No | only `import hashlib` (`a_tok.py:9`); file reads are `lane/SOURCES.md` (`:21-22`) and `lane/STREAM` (`:44`), both inside `d` |
| Writes outside `d` (HOME, PATH dirs, other modules' dirs) | No | writes only `p.write_text` on the clone inside `d` (`:25`); `Ctx.ENV` sets `HOME=/nonexistent`, `ctx._inside` rejects paths outside the fixture root (`round40_c1_verify.py:167-171`); `diff -rq -x .git` vs lane shows only SOURCES.md per fixture |
| Relative argv / symlinks out of `d` | No | argv is `["--lane", <abs d/lane>]` (`:26`, BUILT JSON receipt); `find "$S/fx" -type l` → empty |
| `.lock` / `.git/index` fingerprint skips | No reliance | fixture creates neither; `tampered=0` measured (fingerprint before/after all runs) |
| Phase detection (telling ref from mutant) | No | no `os`/`environ`/time/process access anywhere in the module; variant is mounted read-only at one fixed slot path, argv carries no variant hint |
| Bare-string `build()` return | No | returns a list of one str token (`:26`); harness validates types (`build_battery` ok-check) |

Robustness: `_edit` fails loudly on a non-unique token (`a_tok.py:23-24`) instead of passing vacuously; the
`count != 1` guard also means the fixture cannot be built against a SOURCES.md that drifted from the constants.

## Findings (non-defect observations)

1. **A01's kill is a reclassification, not an acceptance.** Running the A01 variant directly on f000 (variant
   sha256 `7379c272…4f72d`, same wrapper): rc=1,
   `DEFECT S111 … class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256SUMS` — the uppercase
   token passes the widened shape test but does not resolve (binding is case-sensitive), so the mutant still
   rejects, with a different class. The frozen `silence` direction ("reference prints class C, the fixture
   declares C, the mutant does not print C, both exit 0/1") counts this as a kill, and the fixture is honest —
   the reference demonstrably prints the advertised `digest-uppercase`. Flagging it because a reader of the
   calibration receipt should know A01's kill is advertisement-removal, not a green-under-mutant result. This is
   a harness-rule property, not a battery defect; no action needed for admission.
2. No other fixture or module observation: `wrong=0 tampered=0 sidechannel=0 null_detected=0` on this subset.

## Verification gaps

Only A01-A03 and this module were in scope; other battery40 modules and mutants were not run. The
`--evidence-ref index` path is not exercised by these fixtures (default `head` only).

VERDICT: battery-a_tok-honest-3/3
