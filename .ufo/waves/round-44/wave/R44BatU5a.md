# R44BatU5a — battery44 module for frozen mutant U5 (`digest-short` label)

Seat: R44BatU5a (executor, leaf). Round 44 v2 wave, C1 calibration. Lane clone for measurement:
`/fast/scratch/hyaku/kengaku-r44/R44BatU5a/lane` (`git rev-parse --show-toplevel` = that path; clone of lane tip
`5e3d3aa`). Nothing was written to the lane, its index, its jj state, or any corpus/plans file.

## Axes (Godspeed)

- **Calibration** — U5 is one of the five frozen advertised-but-undemonstrated behaviours
  (`plans/round-44-claims.md` §C1). Move kept: three fixtures that kill it attributably in its declared direction.
- **Operability** — the counter is run exactly as the seat spec spells it, inside the round-44 envelope, with the
  PATH-dir content digest unchanged before/after every run; all receipts are small text files under this seat's
  subdir.

## Target and direction (re-read from the frozen counter)

`plans/round44_c1_verify.py:231-235`:

    ('U5', 'anchor', 'digest-short', 'silence', 'direct', ... )
    old 'cls, why = ("digest-short" if len(tok) < 64 else "digest-long")'
    new 'cls, why = ("digest-long" if len(tok) < 64 else "digest-long")'

The replaced span is `plans/anchor_digest_check.py:522` (one line, `new` has the same newline count). Direction
`silence`: reference prints `class=digest-short` and exits 1; the mutant prints `class=digest-long` and exits 1.
So each fixture declares `expect: reject`, `defects: ["digest-short"]` — the exact class set the unmodified tool
prints on it (verified by the counter's `FIXTURE … ok` line, which compares rc AND the class set).

## Module

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU5a/battery/u5_short_a.py`
(7087 bytes, sha256 `fdd4048af41530e9e09821d724fae83962a811053bd32c44ad18b74f2451ef09`), stdlib only
(`hashlib`), three fixtures, every fid prefixed `u5_short_a-`, each repo built from nothing through the counter's
own `ctx` (`ctx.init/git/write`; no lane clone, no reuse of any pre-freeze module). Its own sidechannel scan over
the counter's token list returns `[]`.

| fid | shape (what it demonstrates) | binding route / argv | defect token |
|---|---|---|---|
| `u5_short_a-manifest-registry` | realistic six-row registry in a 3-commit history; clean rows, a tokenless row, a directory-named row; one row per capture | URL → `task.toml` slug (`name = "harbor-framework/alpha-report"`) + `SHA256SUMS` manifest beside the capture; `--lane` only | `sha256 <63 hex>` = one-character truncation of a manifest-listed capture |
| `u5_short_a-index-staged` | registry + capture exist only in the index over a seed commit (round-37 style index-only seat) | `--evidence-ref index`; row-path binding of a `.log` capture | 16 hex digits that are a prefix of no capture digest (asserted at build) |
| `u5_short_a-abbrev-neighbour` | second trigger of the same branch: a resolving `sha256 <12 hex>…` abbreviation sits in the same anchor cell; commit 2 shortens the full digest by one digit | `--lane --verbose`; row-path binding; 2 commits | `sha256 <63 hex>` beside the excused abbreviation |

Each fixture's whole defect set is `{digest-short}`: exactly one `DEFECT … class=digest-short` line and exit 1.
Rows without anchor tokens raise nothing (the tool's stated presence limit), so the good rows cannot add classes.

## Run 1 — the spec's development command (pasted verbatim, receipt `receipt-u5-only.txt`)

    ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44BatU5a/env /fast/scratch/hyaku/kengaku-r44/R44BatU5a/env --bind /fast/scratch/hyaku/kengaku-r44/R44BatU5a/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44BatU5a/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU5a/battery --only U5 --work /fast/scratch/hyaku/kengaku-r44/R44BatU5a/w
    ENVELOPE start 20:33:22 cwd=/home/vgpnk/Projects/shokunin
    PINS total=2 mismatched=0
    FIXTURE u5_short_a-manifest-registry tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
    FIXTURE u5_short_a-index-staged tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
    FIXTURE u5_short_a-abbrev-neighbour tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
    MUTANT U5 anchor silence killed by=u5_short_a-manifest-registry attributed=L522 value=differs hits=3 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
    BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    MUTANTS-BY-TOOL anchor=1/1 order=0/0
    ADVERTISED direct=1 indirect=0 none=0
    PINS-AFTER mismatched=0
    PREDICATE C1 n/a (non-default battery or mutant subset)
    ENVELOPE end 20:33:24 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

Exit 0. Every fixture `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0 unattributed=0`, and
`killed by=u5_short_a-manifest-registry attributed=L522 value=differs` — leg f (the traced re-run reproduces
(1, {digest-short}) and executes line 522) and leg g (site record differs from the reference's over line 522)
both hold.

## Run 2 — load-bearing table (receipt `receipt-load-bearing.txt`, sha256
`1acf477ffa2d30decbeafa80120b8cff0ca54f855685c587af76d74b09176b1a`)

Each variant is the same module with one trailing filter line; the counter is otherwise the spec's command.
Six envelope runs, all `local_bin_content_before/after=328be01808ba022f … unchanged`, exit 0.

| variant | fixtures | U5 | killed by | attributed |
|---|---|---|---|---|
| minus `manifest-registry` | 2 (`index-staged`, `abbrev-neighbour`) | killed | `u5_short_a-index-staged` | L522 value=differs |
| minus `index-staged` | 2 (`manifest-registry`, `abbrev-neighbour`) | killed | `u5_short_a-manifest-registry` | L522 value=differs |
| minus `abbrev-neighbour` | 2 (`manifest-registry`, `index-staged`) | killed | `u5_short_a-manifest-registry` | L522 value=differs |
| only `manifest-registry` | 1 | killed | `u5_short_a-manifest-registry` | L522 value=differs, hits=1 |
| only `index-staged` | 1 | killed | `u5_short_a-index-staged` | L522 value=differs, hits=1 |
| only `abbrev-neighbour` | 1 | killed | `u5_short_a-abbrev-neighbour` | L522 value=differs, hits=1 |

Reading: removing any single fixture still kills U5 (`hits` drops to 2), and each fixture ALONE kills it with a
differing site record (`hits=1`). So no fixture is load-bearing in the redundancy sense — the three are mutually
redundant by design (two independent rows would each carry the branch), which is exactly what makes the module
robust to a later reviewer dropping one shape. Every one of the three is individually sufficient.

## Run 3 — full default counter against the clone (receipt `receipt-full-default.txt`)

Module copied to `<clone>/plans/battery44/u5_short_a.py` (only module there), then the default command
`python3 plans/round44_c1_verify.py --lane <clone> --work $S/w2`:

    PINS total=2 mismatched=0
    FIXTURE u5_short_a-manifest-registry tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
    FIXTURE u5_short_a-index-staged tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
    FIXTURE u5_short_a-abbrev-neighbour tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
    MUTANT U5 anchor silence killed by=u5_short_a-manifest-registry attributed=L522 value=differs hits=3 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
    MUTANT U6 anchor silence SURVIVED exhibits=none -- …:88 (a long token labelled digest-short)
    MUTANT U7 anchor rc-mirror SURVIVED exhibits=none -- …:98-99 (only the first resolving capture is claimed)
    MUTANT U9 anchor rc-mirror SURVIVED exhibits=none -- …:106-107 (lessons read from HEAD instead)
    MUTANT U14c order error SURVIVED exhibits=none -- plans/order_check.py:26-27 (the claims-name guard disabled)
    BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
    MUTANTS-BY-TOOL anchor=1/4 order=0/1
    ADVERTISED direct=5 indirect=0 none=0
    PINS-AFTER mismatched=0
    PREDICATE C1 fail
    ENVELOPE end 20:33:12 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

U5 is killed under the default (predicate-active) path with the module in its real home; the other four mutants
survive because this clone carries no sibling module, so `PREDICATE C1 fail` here is expected and is NOT a defect
of this module. `invalid=0 null_detected=0 unattributed=0 tampered=0` with 5 mutants active.

## Files written

- `.ufo/waves/round-44/wave/R44BatU5a.md` (this report)
- `.ufo/waves/round-44/wave/R44BatU5a/battery/u5_short_a.py` (the module; for the L1 to integrate as
  `plans/battery44/u5_short_a.py`)
- `.ufo/waves/round-44/wave/R44BatU5a/receipt-u5-only.txt` (1660 B), `receipt-full-default.txt` (2082 B),
  `receipt-load-bearing.txt` (4468 B)

No lane file, no `plans/`, no `corpus/`, no SCORECARD/LOG/README touched; no commit, push, or jj command anywhere;
nothing installed (no pacman, no uv tool) — the measurement needed only `/usr/bin/python3` and `/usr/bin/bwrap`.

## Limits

1. **Direction shape.** U5 is a `silence` kill: reference and mutant both exit 1, so only the class set separates
   them. A kill therefore proves the label branch, not a return-code difference; that is what the `silence`
   direction is defined to mean in the frozen counter.
2. **Attribution picks the first hit.** With all three fixtures present the counter attributes on
   `manifest-registry` only (`hits=3`); leg g's value record is the tool's locals at line 522. The one-alone runs
   show each fixture's own record differs too, but the counter itself needs only one, so per-fixture attribution
   is my measurement, not the predicate's.
3. **Synthetic registries.** Captures are invented byte strings, not the lane's real `corpus/evidence` tree; the
   fixtures exercise the tool's own binding code (url→`task.toml` slug, `SHA256SUMS` manifest, row-path,
   index-mode), not real task data. Row ids are `S2xx` inside the fixture repo and are unrelated to this round's
   S138–S146.
4. **No cross-check with the sibling module.** A second seat writes a second U5 module; I did not read, copy or
   coordinate with it (the seat spec says independence is the point), so a duplicate-branch review by the L1 still
   decides which modules land.
5. **Full-set predicate not reached here.** `PREDICATE C1 pass` needs `killed=5` and floors `anchor=4/4 order=1/1`;
   this seat contributes one of those five, so run 3 was measured on a clone whose `battery44` holds only my
   module. Integration must re-run the default counter on the landing tip.
6. **Token-scan is a heuristic (carried limit).** My module contains none of the counter's SIDECHANNEL tokens
   (checked twice: the counter's `sidechannel=0` and my own scan `[]`), but that only bounds spelling, not intent.
7. **No depth/scale stress.** Fixtures are tiny (a handful of files); the fence legs F1–F6 are exercised only in
   the sense of being satisfied (`lane_breach`, `repo_breach`, `argv_shape_breach`, `symlink_breach` all passed at
   build), not stressed.
8. Scratch `/fast/scratch/hyaku/kengaku-r44/R44BatU5a` was removed with `plans/scratch_guard.py safe-rm` after
   the receipts above were copied into this report subdir.

VERDICT: battery44-u5_short_a-U5-killed-yes-fixtures-3
