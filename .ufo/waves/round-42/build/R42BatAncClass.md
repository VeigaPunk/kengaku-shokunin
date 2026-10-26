# R42BatAncClass — battery42 module `a_class.py`: attributed kills for X6, X7, X14

Seat: R42BatAncClass (wave-1 executor, leaf). Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin.
Measurement clone: `git clone -q --shared <lane> $S/lane`, HEAD `fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473`,
`git -C $S/lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r42/R42BatAncClass/lane`.

**Artifact (delivered, not integrated):** `.ufo/waves/round-42/build/R42BatAncClass/battery/a_class.py`
sha256 `eef02b5df0a8b5e7e558956eaf3d5fca6fa5701872f11632d5327717def8f1bb`, 10897 bytes, 174 lines, stdlib only
(`hashlib`), 6 fixtures, every fid starts `a_class-`. The same bytes were copied to `$S/lane/plans/battery42/`
for the default-battery run (sha256 identical, `full-run.txt` line 2). L1 integrates by copying this one file
into `plans/battery42/`.

## 1. Frozen mutants under test (read from `plans/round42_c1_verify.py` MUTANTS)

| id | tool | class | direction | `old -> new` (span) | what the fixture must do |
|----|------|-------|-----------|--------------------|--------------------------|
| X6 | anchor | `digest-wrong-capture` | silence | `elif tok not in row_scope:` / `if tok in allowed:` → `if False:` (L527) | a token that IS a committed capture but not this row's |
| X7 | anchor | `digest-unknown` | silence | `class=digest-unknown` → `class=digest-wrong-capture` (L535) | a 64-hex token that is no committed capture |
| X14 | anchor | `erratum-digest-unresolved` | silence | `HEX64_ANY.fullmatch(t)` → `HEX64.fullmatch(t)` (L458) | an erratum line with an UPPERCASE 64-hex token no capture has |

All three declare `silence`: the reference prints the class and exits 1; the mutant does not print that class.
`expect="reject"` (rc 1) on every fixture, measured, not assumed.

## 2. Fixtures — one line each, and why each shape differs from the freeze module

| fid | mutant | shape / what it demonstrates |
|-----|--------|------------------------------|
| `a_class-x6-sibling-digest` | X6 | one row naming capture A (`corpus/evidence/.../x6-a/notes.txt`), anchor cell carrying capture B's committed **file** digest |
| `a_class-x6-stale-manifest` | X6 | **second trigger**: three-row registry in **two commits**; the bad row binds through a **task.toml URL** (`acme/gatekeep`, pinned `2fd12b8…`) and its token is the stale digest a sibling directory's `SHA256SUMS` still lists for a **recaptured** file — a manifest-view digest, not a file digest |
| `a_class-x7-fabricated-token` | X7 | one row naming a committed capture, anchor cell carrying a made-up 64-hex token |
| `a_class-x7-provenance-row` | X7 | **second trigger**: the row binds through a **PROVENANCE.md table line** (multi-row table), the registry is written in two commits, and the second commit adds the defective row beside a third row whose anchor is a resolvable 12-hex **abbreviation** of the same capture (exercises the abbrev branch as green) |
| `a_class-x14-uppercase-token` | X14 | one green row; a committed `corpus/lessons/round-37.md` erratum line carries an UPPERCASE 64-hex token plus the row's true digest as correction |
| `a_class-x14-two-errata` | X14 | **second trigger**: two rows, two lessons files, **two commits** — `round-37.md` erratum is clean and exempts row S350 (whose anchor still carries the stale token), and the second commit appends to `round-42.md` a wrong-case erratum for S351; only that line defects |

No fixture is a renamed copy of a freeze witness module; the freeze modules were read only to learn
reachability (anchor classes `digest-wrong-capture` / `digest-unknown` / erratum loop). Each `build(ctx, d)`
creates `d/repo`, `git init -b master` via `ctx.init`, writes every file through `ctx.write`, commits through
`ctx.git` (2 commits where the shape says so), and returns `["--lane", str(repo)]` — an absolute path inside `d`.
No lane clone is read by any fixture; every repository is built from nothing.

## 3. Targeted run — every FIXTURE `ok`, 3/3 killed and attributed

Command (cwd fleet root; envelope exactly as specified, `$S=/fast/scratch/hyaku/kengaku-r42/R42BatAncClass`):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 \
      <lane>/plans/round42_c1_verify.py --lane "$S/lane" \
      --battery-dir <lane>/.ufo/waves/round-42/build/R42BatAncClass/battery \
      --only X6,X7,X14 --work "$S/w"
```

Output (full text also at `build/R42BatAncClass/targeted-run.txt`, sha256 `bf14a874…`):

```
MODULE sha256 eef02b5df0a8b5e7e558956eaf3d5fca6fa5701872f11632d5327717def8f1bb
ENVELOPE start 17:22:18 local_bin_before=436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18
PINS total=2 mismatched=0
FIXTURE a_class-x6-sibling-digest tool=anchor expect=reject declared=digest-wrong-capture observed_rc=1 observed=digest-wrong-capture ok
FIXTURE a_class-x6-stale-manifest tool=anchor expect=reject declared=digest-wrong-capture observed_rc=1 observed=digest-wrong-capture ok
FIXTURE a_class-x7-fabricated-token tool=anchor expect=reject declared=digest-unknown observed_rc=1 observed=digest-unknown ok
FIXTURE a_class-x7-provenance-row tool=anchor expect=reject declared=digest-unknown observed_rc=1 observed=digest-unknown ok
FIXTURE a_class-x14-uppercase-token tool=anchor expect=reject declared=erratum-digest-unresolved observed_rc=1 observed=erratum-digest-unresolved ok
FIXTURE a_class-x14-two-errata tool=anchor expect=reject declared=erratum-digest-unresolved observed_rc=1 observed=erratum-digest-unresolved ok
MUTANT X6 anchor silence killed by=a_class-x6-sibling-digest attributed=L527 hits=2 -- plans/anchor_digest_check.py:89-92 'A 64-hex token that is a committed capture but not thi
MUTANT X7 anchor silence killed by=a_class-x7-fabricated-token attributed=L535 hits=2 -- plans/anchor_digest_check.py:92-93 'a token that is no committed capture at all is digest-
MUTANT X14 anchor silence killed by=a_class-x14-uppercase-token attributed=L458 hits=2 -- plans/anchor_digest_check.py:111-113 'no 64-hex token on it may be outside A unless it is 
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/3 order=0/0
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end exit=0 17:22:19 local_bin_after=436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18
```

`declared` equals `observed` on all six fixtures — the exact class set the UNMODIFIED tool prints, and each
`expect=reject` matches `observed_rc=1`. Each kill's attributed span is the mutated line itself
(L527 / L535 / L458), so the traced re-run executed the replaced code, not a neighbour.
Envelope start/end `date +%T` 17:22:18→17:22:19; `ls -A /home/vgpnk/.local/bin | sha256sum` before and after
`436b361f…d63fc18`, unchanged.

## 4. Load-bearing table (delete one fixture line, re-run the same targeted command)

`omission-runs.txt` (sha256 `c9cc6ac0…`); each row = the module minus the named `FIXTURES` line(s), same
`--only X6,X7,X14`, envelope start 17:22:29 end 17:22:34, local-bin digest `436b361f…` unchanged.

| omitted | X6 | X7 | X14 | fixtures |
|---|---|---|---|---|
| `x6-sibling-digest` | killed by `a_class-x6-stale-manifest` (L527, hits=1) | killed | killed | 5 |
| `x6-stale-manifest` | killed by `a_class-x6-sibling-digest` (L527, hits=1) | killed | killed | 5 |
| `x7-fabricated-token` | killed | killed by `a_class-x7-provenance-row` (L535, hits=1) | killed | 5 |
| `x7-provenance-row` | killed | killed by `a_class-x7-fabricated-token` (L535, hits=1) | killed | 5 |
| `x14-uppercase-token` | killed | killed | killed by `a_class-x14-two-errata` (L458, hits=1) | 5 |
| `x14-two-errata` | killed | killed | killed by `a_class-x14-uppercase-token` (L458, hits=1) | 5 |
| both X6 fixtures | **SURVIVED**, `exhibits=none` | killed | killed | 4 |
| both X7 fixtures | killed | **SURVIVED**, `exhibits=none` | killed | 4 |
| both X14 fixtures | killed | killed | **SURVIVED**, `exhibits=none` | 4 |

Reading: either fixture of a mutant is sufficient on its own, and each mutant's kill depends exactly on its own
two fixtures — removing both flips that mutant (and nothing else) to `SURVIVED`. No fixture carries another
mutant's kill, so the second shapes are independent triggers, not duplicates of the first.

## 5. Full default battery in the clone (`plans/battery42/a_class.py`)

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 \
      <lane>/plans/round42_c1_verify.py --lane "$S/lane" --work "$S/w2"
```

(`full-run.txt`, sha256 `2d24136f…`; envelope start 17:22:40 end 17:22:41, local-bin digest unchanged.)

```
PINS total=2 mismatched=0
… six FIXTURE lines, all ok …
MUTANT X6 anchor silence killed by=a_class-x6-sibling-digest attributed=L527 hits=2 -- plans/anchor_digest_check.py:89-92 …
MUTANT X7 anchor silence killed by=a_class-x7-fabricated-token attributed=L535 hits=2 -- plans/anchor_digest_check.py:92-93 …
MUTANT X14 anchor silence killed by=a_class-x14-uppercase-token attributed=L458 hits=2 -- plans/anchor_digest_check.py:111-113 …
(all other 11 mutants: SURVIVED exhibits=none)
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=3 survived=11 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/9 order=0/5
PINS-AFTER mismatched=0
PREDICATE C1 fail        (exit 1 — expected: the other 11 mutants have no fixture yet)
```

No `invalid`, no `unattributed`, no `null_detected`, no `tampered`, no `sidechannel` in the full run either:
the three kills hold when the module is the only battery in the lane clone and the other 11 mutants are present.

## 6. Operability record

- **Sidechannel calibration (honest record).** The first development run printed
  `SIDECHANNEL battery/a_class.py tokens=/run` and `sidechannel=1`: a capture filename `run.txt` made the row
  path `.../x6-a/run.txt` contain `/run`. Renamed to `notes.txt`; the token set is now clean
  (`sidechannel=0` in every run above). This is the only content change made for the scan.
- **Contract compliance** (counter build gate, no `SETUP`/`breaks the contract` in any run): `FIXTURES` entries
  carry `fid`/`tool`/`expect`/`defects`/`build`; `defects` is `[]`-free but valid for `tool="anchor"` (order
  fixtures correctly require `[]`); the only argv path is an absolute `--lane` inside the fixture dir, so
  `path_ok` passes and nothing leaves `d`; `build` returns `list[str]`.
- **Isolation.** Every build and every tool run happened inside the host envelope above (the counter nests its
  own `--ro-bind / /` sandboxes inside it). Nothing was written to `~/.local/bin`, `/usr`, `/etc` or `$HOME`;
  the local-bin listing digest was `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` before
  and after all runs. No package was installed or upgraded (no tool was needed).
- **Lane untouched.** No file under the lane's `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`,
  `SKILL.md`, `PROVINCE.md`, `SHONEN.md` was written; no git/jj mutation was run in the lane; no commit, push or
  `git add` anywhere. Writes are the report dir (`build/R42BatAncClass/`, `build/R42BatAncClass.md`) and the
  scratch clone/dir only, which is deleted (`rm -rf -- /fast/scratch/hyaku/kengaku-r42/R42BatAncClass`).
- **Receipts** (all < 1 MiB): `build/R42BatAncClass/targeted-run.txt` (bf14a874…), `omission-runs.txt`
  (c9cc6ac0…), `full-run.txt` (2d24136f…), plus the module under `build/R42BatAncClass/battery/`.

## 7. Limits / risks named

1. A kill records a result difference in the declared direction on a fixture that executes the mutated line —
   not the fixture's semantic intent. The `defects` sets are measured, and X6's two fixtures differ in trigger
   (file digest vs stale manifest entry), but both drop the same `if tok in allowed:` test.
2. The counter's token scan is a heuristic; `sidechannel=0` is evidence about the scan, not that the module is
   incapable of escaping. Non-author review of the module remains part of C1 admission.
3. The X14 fixtures depend on the erratum grammar being `Erratum (round 37): S<id> anchor sha256 …` — a lessons
   erratum written with another round number would not be read at all by the frozen tool. Both of my fixtures
   use the exact grammar the tool advertises.
4. `a_class-x7-provenance-row` also exercises the abbreviation branch as a *green* row; if a later tool change
   altered abbrev handling this fixture's declared `defects` would move. That is intended, not hidden: the
   fixture pins today's behaviour.
5. Only X6, X7, X14 are addressed. The other 11 frozen mutants (X1 X3 X9 X12 X13 X15, XO1 XO3 XO5 XO6 XO7) stay
   survivors in this module's run and need the other wave-1 seats.

VERDICT: battery42-a_class-killed-3/3-wrong-0
