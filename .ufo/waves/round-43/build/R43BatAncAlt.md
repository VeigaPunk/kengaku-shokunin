# R43BatAncAlt — C1 battery43 module `a_alt` (anchor near-variants NA1 NA5 NA7 NA18 NA20 NA21)

Seat: executor, kengaku round 43 wave 1. Lane repo read-only; all work in a `--shared` clone at
`/fast/scratch/hyaku/kengaku-r43/R43BatAncAlt/lane` (`git -C … rev-parse --show-toplevel` → that path,
`rev-parse HEAD` → `d33350fdb01ce27cbff47b04642fd2c1471e5c26`). No lane file was edited; nothing frozen was touched.

## 1. Deliverable

| item | value |
|---|---|
| module | `.ufo/waves/round-43/build/R43BatAncAlt/battery/a_alt.py` |
| sha256 | `31ddcc0cb9a475dd3d7e3a41b90daa949a2b84fec827cf490333cd0620c5dc01` |
| size | 435 lines, stdlib only (`hashlib`) |
| fixtures | 14, ids all `a_alt-…`, tool `anchor` for all 14 |
| contract | `FIXTURES=[{"fid","tool","expect","defects","build"}]`; each `build(ctx, d)` fills the empty `d` from nothing and returns `["--lane", <path inside d>]`; every lane path is absolute and inside `d` |
| token scan | `sidechannel=0` on every run; local pre-check of the counter's 26 tokens (`/proc … /run`) → `hits: []` |
| imports | only `hashlib`; the module never reads the pre-freeze direction module (no reference to it anywhere in the source) |

Each fixture carries a one-line comment above its builder naming what it demonstrates (`# a_alt-N: …` +
`# Demonstrates …`).

## 2. Fixture inventory — shape, declared result, mutant exhibited

Reference results are the counter's own `FIXTURE … ok` lines (§3): 12 lanes accept (rc 0, no class) and 3 lanes
reject with exactly `row-malformed` (rc 1).

| fid | mutant(s) it exhibits | shape built from nothing |
|---|---|---|
| `a_alt-longrow-copied` | NA1 (silence) | 5-row registry, one SHA256SUMS capture dir; a 12-cell row that is the green row S912 copied plus one cell → rc 1 `row-malformed` |
| `a_alt-longrow-multicap` | NA1 | 6-row registry, every capture dir with a SHA256SUMS; 14-cell row copying the **two-capture** row S924 (one token per capture) |
| `a_alt-longrow-late` | NA1 | three commits: green rows, then the 13-cell row, then an unrelated lesson → rc 1 `row-malformed` |
| `a_alt-slug-deepest` | NA5 (rc-mirror) | 5 rows; two task dirs `alpha/`, `beta/` with `task.toml` + SHA256SUMS; raw URL `…/<40hex>/alpha/beta/payload.txt` binds the **deepest** slug `beta` |
| `a_alt-slug-blob` | NA5 | 3 rows; `github.com/…/blob/<40hex>/tb-scan/tests/test_outputs.py`, capture at the task-dir root beside a `tests/` subdir |
| `a_alt-slug-manifest` | NA5 | 3 rows; the capture `report.txt` exists **only** as an entry in `SHA256SUMS` (no such file committed) |
| `a_alt-erratum-manifest` | NA7, NA20, NA21 | 5 rows; a wrong 64-hex token exempted by an erratum that cites the capture's **manifest** digest |
| `a_alt-erratum-sibling` | NA7, NA20, NA21 | 3 rows bound by a `PROVENANCE.md` table beside the pinned URL route; the erratum line carries **three** 64-hex tokens: the wrong one, a sibling capture's committed digest, the correction |
| `a_alt-erratum-short` | NA7, NA20, NA21 | 3 rows; the exempted row's token is a **63-hex prefix** of its capture digest |
| `a_alt-erratum-upper` | NA7, NA20, NA21 | 3 rows; the exempted row's token is the capture digest in **uppercase** |
| `a_alt-erratum-two` | NA7, NA20, NA21 | 6 rows; two provenance-bound rows, each kept green by its **own** erratum in its own lesson file |
| `a_alt-erratum-lessons` | NA7, NA20, NA21 | 6 rows; lane-path bindings, two lesson files, plus a two-capture row that must carry one token per capture |
| `a_alt-shorturl-sibling` | NA18 (rc-mirror) | 3 rows; lane path names `alpha/notes.txt` while a **5-hex**-commit raw URL names a second task's `beta/other.txt` |
| `a_alt-shorturl-samedir` | NA18 | 2 rows; lane path names `gamma/appendix.txt` while a **4-hex**-commit raw URL names `gamma/report.txt` in the same task dir |

Per mutant: NA1 ×3, NA5 ×3, NA18 ×2, NA7 ×2 named (6 lanes exhibit it), NA20 ×2 named (6), NA21 ×2 named (6).
No fixture is a re-spelling of the pre-freeze module: registries of 3–6 rows against its single-row lanes,
SHA256SUMS manifests in every capture dir, a two-capture row with two tokens, a provenance table beside the URL
route, 12/13/14-cell rows, a three-commit history, and a capture that exists only as a manifest entry.

## 3. Dev measurement — the six mutants in their declared directions

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43BatAncAlt/env /fast/scratch/hyaku/kengaku-r43/R43BatAncAlt/env --bind /fast/scratch/hyaku/kengaku-r43/R43BatAncAlt/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r43/R43BatAncAlt/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43BatAncAlt/battery --only NA1,NA5,NA7,NA18,NA20,NA21 --work /fast/scratch/hyaku/kengaku-r43/R43BatAncAlt/w
ENVELOPE start 19:10:58 cwd=/fast/scratch/hyaku/kengaku-r43/R43BatAncAlt
PINS total=2 mismatched=0
FIXTURE a_alt-longrow-copied tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_alt-longrow-multicap tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_alt-slug-deepest tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-slug-blob tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-erratum-manifest tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-erratum-sibling tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-erratum-short tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-erratum-upper tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-erratum-two tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-erratum-lessons tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-longrow-late tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_alt-slug-manifest tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-shorturl-sibling tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_alt-shorturl-samedir tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT NA1 anchor silence killed by=a_alt-longrow-copied attributed=L477 value=differs hits=3 -- plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have 
MUTANT NA5 anchor rc-mirror killed by=a_alt-slug-deepest attributed=L258 value=differs hits=3 -- plans/anchor_digest_check.py:54-56 'The task component of `<subpath>` is matched **exactly
MUTANT NA7 anchor rc-mirror killed by=a_alt-erratum-manifest attributed=L458 value=differs hits=6 -- plans/anchor_digest_check.py:112-113 'no 64-hex token on it may be outside A unless it is 
MUTANT NA18 anchor rc-mirror killed by=a_alt-shorturl-sibling attributed=L154 value=differs hits=2 -- plans/anchor_digest_check.py:53-54 'a `raw.githubusercontent.com/<owner>/<repo>/<commit>/<
MUTANT NA20 anchor rc-mirror killed by=a_alt-erratum-manifest attributed=L468 value=differs hits=6 -- plans/anchor_digest_check.py:108-110 'An erratum for S<id> exempts that row's anchor token
MUTANT NA21 anchor rc-mirror killed by=a_alt-erratum-manifest attributed=L456 value=differs hits=6 -- plans/anchor_digest_check.py:108-109 'An erratum for S<id> exempts that row's anchor token
BATTERY fixtures=14 wrong=0 tampered=0 sidechannel=0
MUTANTS total=6 killed=6 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=6/6 order=0/0
ADVERTISED direct=5 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:11:01 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Every kill is attributed twice: `attributed=L<line of the replaced span>` (leg f) and `value=differs` (leg g).
Full receipt: `build/R43BatAncAlt/receipt-dev-only.txt`. An earlier run of the same command with 12 fixtures
(`S/dev1.txt`, not kept) had `NA18 … SURVIVED exhibits=none` — the two NA18 lanes were then added.

## 4. Load-bearing table

Removal was done on copies of the module (`<module> + FIXTURES = [f for f in FIXTURES if f["fid"] != …]`), each run
through the same counter in its own `--work` and its own envelope (`build/R43BatAncAlt/drop/*.out`,
`build/R43BatAncAlt/group/*.out`). All 18 removal runs printed `wrong=0 tampered=0 sidechannel=0`,
`null_detected=0 unattributed=0`, and `ENVELOPE end … unchanged` (digest `328be01808ba022f`).

**Single fixture removed (14 runs).** No mutant flips — by design each carries ≥2 lanes — but the killing lane and
the hit count move exactly as the inventory predicts:

| dropped | flips | effect on the killed mutant |
|---|---|---|
| `a_alt-longrow-copied` | none | NA1 killed by `a_alt-longrow-multicap`, hits 3→2 |
| `a_alt-longrow-multicap` | none | NA1 killed by `a_alt-longrow-copied`, hits 3→2 |
| `a_alt-longrow-late` | none | NA1 hits 3→2 (killer unchanged) |
| `a_alt-slug-deepest` | none | NA5 killed by `a_alt-slug-blob`, hits 3→2 |
| `a_alt-slug-blob` | none | NA5 killed by `a_alt-slug-deepest`, hits 3→2 |
| `a_alt-slug-manifest` | none | NA5 hits 3→2 (killer unchanged) |
| `a_alt-shorturl-sibling` | none | NA18 killed by `a_alt-shorturl-samedir`, hits 2→1 |
| `a_alt-shorturl-samedir` | none | NA18 killed by `a_alt-shorturl-sibling`, hits 2→1 |
| each of the 6 `a_alt-erratum-*` | none | NA7/NA20/NA21 hits 6→5, killed by `a_alt-erratum-sibling` when the manifest lane is the one dropped |

**A whole family removed (4 runs) — this is where the flips are:**

| dropped | flips to SURVIVED | counters |
|---|---|---|
| `longrow-*` (3 lanes) | **NA1** | `killed=5 survived=1`, other five still attributed |
| `slug-*` (3 lanes) | **NA5** | `killed=5 survived=1` |
| `shorturl-*` (2 lanes) | **NA18** | `killed=5 survived=1` |
| `erratum-*` (6 lanes) | **NA7, NA20, NA21** | `killed=3 survived=3` (`MUTANTS total=6 killed=3 survived=3 invalid=0 null_detected=0 unattributed=0`) |

So each of the six mutants has fixtures that are load-bearing for it and only for it; the three erratum mutants
share their whole family (see limit 2).

## 5. Full default counter in the clone

Module copied to `$S/lane/plans/battery43/a_alt.py`; default counter, no `--battery-dir`/`--only`:

```
ENVELOPE start 19:11:56 cwd=/fast/scratch/hyaku/kengaku-r43/R43BatAncAlt
PINS total=2 mismatched=0
… 14 × FIXTURE … ok (identical to §3) …
MUTANT NA1 anchor silence killed by=a_alt-longrow-copied attributed=L477 value=differs hits=3
MUTANT NA5 anchor rc-mirror killed by=a_alt-slug-deepest attributed=L258 value=differs hits=3
MUTANT NA7 anchor rc-mirror killed by=a_alt-erratum-manifest attributed=L458 value=differs hits=6
MUTANT NA18 anchor rc-mirror killed by=a_alt-shorturl-sibling attributed=L154 value=differs hits=2
MUTANT NA20 anchor rc-mirror killed by=a_alt-erratum-manifest attributed=L468 value=differs hits=6
MUTANT NA21 anchor rc-mirror killed by=a_alt-erratum-manifest attributed=L456 value=differs hits=6
MUTANT NO5 order rc-silence SURVIVED exhibits=none
MUTANT NO7 order rc-mirror SURVIVED exhibits=none
MUTANT NO22 order rc-silence SURVIVED exhibits=none
BATTERY fixtures=14 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=6 survived=3 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=6/6 order=0/3
ADVERTISED direct=8 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 19:11:56 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

(The `MUTANT` lines were trimmed at ` -- plans/…` in this paste; the full text is
`build/R43BatAncAlt/receipt-full-default.txt`.) `PREDICATE C1 fail` is the order floor `order=0/3`: this seat's
module has no order fixture, so NO5/NO7/NO22 survive here, exactly as the task says is expected. The anchor floor
is satisfied at `anchor=6/6` with `wrong=0 tampered=0 sidechannel=0 null_detected=0 unattributed=0`.

## 6. Limits

1. **Anchor only.** The module contributes nothing to `order`; a landing of `battery43` containing only `a_alt`
   leaves `MUTANTS-BY-TOOL anchor=6/6 order=0/3` and `PREDICATE C1 fail`. The order floor needs the sibling
   module(s).
2. **The erratum family is shared.** All six `a_alt-erratum-*` lanes exhibit NA7, NA20 and NA21 identically
   (`hits=6` each), so those three mutants are jointly, not severally, load-bearing: dropping one lane never flips
   any of them, and dropping the family flips all three. Six lanes are six distinct lane shapes, not six
   independent mechanisms — NA20 and NA21 differ only in which step of the same exemption clause is disabled.
3. **A kill is a measured result difference, not intent.** Five of six directions are `rc-mirror` (reference 0,
   mutant 1); the fixture shows that exit flip plus a differing site record over the replaced span. It does not
   prove the mutant differs *only* there.
4. **Two fixtures lean on documented strictness classes.** `a_alt-erratum-short` (63-hex token) and
   `a_alt-erratum-upper` (uppercase 64-hex) are the tool's "deliberate strictness" defects; both fixtures are green
   only because the erratum exemption is advertised to cover "every anchor class above". Measured, not assumed:
   both print `ok` with rc 0.
5. **`a_alt-slug-manifest` reads a capture whose bytes are not committed.** The binding succeeds only through the
   documented rule that a SHA256SUMS entry is an accepted view of a capture. A reader who requires a committed
   file for every capture will read this lane as contrived; the reference exit 0 is the measurement.
6. **`a_alt-erratum-sibling` passes the reference only because `allowed` is the union of every committed evidence
   digest** — that is the advertised NA7 clause, and the lane also carries a truly uncommitted wrong token so that
   the erratum (not the digest set) is what keeps the row green.
7. **Seven fixtures use `d` itself as the lane** (`--lane <d>`) and seven a `d/repo` subdirectory; the counter's
   `repo_breach`/`symlink_breach`/`order_argv_breach` legs accepted all 14 (no `SETUP … escapes` line).
8. **Non-re-spelling is my structural claim, not a measurement.** The counter cannot see intent; §2 lists the
   shapes for the non-author reviewer. I read the pre-freeze module only to learn which branches are reachable and
   neither import, copy nor read it at build time (source contains no reference to it; `sidechannel=0`).
9. **The token scan is a heuristic**, as the frozen claims state; a non-author review stays part of admission.
10. **No tool was installed or updated** this wave; no pacman/uv/npx call was made. Scratch
    `/fast/scratch/hyaku/kengaku-r43/R43BatAncAlt` was removed with the round's `scratch_guard.py safe-rm` after
    the receipts were copied into `build/R43BatAncAlt/`; the deliverable module sits outside scratch.

VERDICT: battery43-a_alt-killed-6/6-wrong-0
