# R42BatOrdClause — battery42 module `o_clause` (order clauses XO1, XO3)

Seat: executor, kengaku round 42 wave 1, lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(clone `/fast/scratch/hyaku/kengaku-r42/R42BatOrdClause/lane`, toplevel verified = that path, HEAD
`fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473`). Read first: `plans/round-42-claims.md` (full),
`plans/round42_c1_verify.py:1-123` (docstring + contract), `:199-473` (Ctx/runner/path_ok/exhibits),
`:462-672` (build_battery/main), `plans/order_check.py:1-60,60-214`, and the freeze witness modules
`claims/witness/w_order.py` + `claims/witness-run.txt` (read to learn reachability only; not imported,
not copied, not read by the battery at run time — the module has no imports at all).

## Axes named (godspeed)

1. **calibration** — kill XO1 and XO3 attributively (direction `rc-silence`, the declared direction).
2. **operability** — one stdlib-only module, 5 fixtures, ~1.7 s per dev counter run; fixtures are plain
   git histories with no network, no host dependency.
3. **independence** — every shape differs from the freeze module's, so a kill cannot be a renamed copy of
   the pre-freeze witness.
4. **host safety** — Q32 envelope on every run, `/home/vgpnk/.local/bin` bound read-only and digest-identical
   before/after, all scratch inside `$S`.

## Module

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/build/R42BatOrdClause/battery/o_clause.py`
(sidecar copy for the L1 to install as `plans/battery42/o_clause.py`).

- sha256 `badc9e3d3807e22c99161ae3c991db1e0ed840dd8c76542dbf9643c210af163b`, 5978 bytes, 5 fixtures, no imports.
- Contract: `FIXTURES = [{"fid", "tool": "order", "expect", "defects": [], "build"}]`; every `fid` starts
  `o_clause-`; `build(ctx, d)` creates `d/lane` with `ctx.init`, fills it with `ctx.write`, commits with
  `ctx.git` (pinned `fixture <fixture@kengaku.invalid>`, fixed date), returns
  `["--lane", str(repo), "--claims", rel, "--receipt", rel]`. No lane clone is used; repo built from nothing.
- `defects` is `[]` on every fixture — `classes()` returns the empty set for the order tool, and the runs
  below show `declared=- observed=-` for all five.
- Sidechannel: my own scan of the module text against the counter's 26 tokens lowercased →
  `hits []`; the counter's own scan reports `sidechannel=0`.

### What each fixture demonstrates (one line, as commented in the module)

| fid | expect | behaviour demonstrated |
|---|---|---|
| `o_clause-freeze-single` | reject | clause 1, one commit: the freeze commit is also the commit that first adds the receipt |
| `o_clause-freeze-pair-edited-after` | reject | clause 1, three commits: the freeze pair lands in the middle commit and the receipt is edited later, so its first adding commit is still the freeze commit |
| `o_clause-receipt-withdrawn` | reject | clause 2: the receipt is added, withdrawn, the claims are frozen without it, and it is recorded again (round-9 paths) |
| `o_clause-receipt-side-line` | reject | clause 2 with a branching history: early receipt on master, freeze on a side line, re-recorded receipt on master, `--no-ff` merge back |
| `o_clause-clean-order` | accept | the pass path: claims frozen first, receipt committed afterwards, claims/ blob is the clean `P10 DEFECT receipt unreadable` excuse line |

Clause 3 (every blob ever committed under the round's `claims/` directory up to the receipt commit) is kept
clean in all five histories, so each reject fixture can only fail on the clause it targets — that is what
makes the XO1 kill (clause 1 skipped) and the XO3 kill (clause 2 skipped) attributable rather than incidental.

### Shape difference from the freeze modules (required at least one per mutant)

- Freeze `w-xo1-*`: one commit, `corpus/evidence/round42/probe.txt`, claims-dir control blob.
  Mine: `o_clause-freeze-pair-edited-after` is a three-commit history where the receipt is *modified after*
  the freeze (regrade commit) — the receipt's first-adding commit is still the freeze commit, a path the
  freeze shape never exercises (it also carries a `LOG.md` commit after the freeze).
- Freeze `w-xo3-*`: linear add/remove/freeze/re-add on round-42 paths.
  Mine: `o_clause-receipt-side-line` puts the freeze on a branch and merges it back, with the receipt
  re-recorded on master under a different directory (`evidence/probe.txt`), and `o_clause-receipt-withdrawn`
  moves the whole history to round-9 paths (`plans/round-9-claims.md` → `claims_dir .ufo/waves/round-9/claims`),
  exercising the round-number parse. `o_clause-clean-order` adds the accept/pass path the freeze module covers
  only implicitly.

## Dev counter run — required output (verbatim, `battery/dev-run.txt`)

Envelope (Q32): exactly the mandated line, `date +%T` before/after, `~/.local/bin` listing digest
before/after `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` (unchanged).

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 plans/round42_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r42/R42BatOrdClause/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/build/R42BatOrdClause/battery --only XO1,XO3 --work /fast/scratch/hyaku/kengaku-r42/R42BatOrdClause/w
ENVELOPE start 17:18:14 cwd=/home/vgpnk/Projects/shokunin
LOCALBIN before 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -
PINS total=2 mismatched=0
FIXTURE o_clause-freeze-single tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_clause-freeze-pair-edited-after tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_clause-receipt-withdrawn tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_clause-receipt-side-line tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_clause-clean-order tool=order expect=accept declared=- observed_rc=0 observed=- ok
MUTANT XO1 order rc-silence killed by=o_clause-freeze-single attributed=L183 hits=2 -- plans/order_check.py:17,183 'FAIL when the freeze commit (the first commit adding <claims>
MUTANT XO3 order rc-silence killed by=o_clause-receipt-withdrawn attributed=L188 hits=2 -- plans/order_check.py:18,188 'FAIL when <receipt> was committed before <claims> (pre-regist
BATTERY fixtures=5 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=2/2
ADVERTISED direct=2 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 17:18:15 exit=0
LOCALBIN after 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -
```

Required cells: every FIXTURE line `ok`; `wrong=0 tampered=0 sidechannel=0`;
`null_detected=0 unattributed=0`; `XO1 … killed by=o_clause-freeze-single attributed=L183`;
`XO3 … killed by=o_clause-receipt-withdrawn attributed=L188`. `hits=2` = both fixtures of that mutant's
pair produce the `rc-silence` exhibit independently; the counter picks the first for `by=`.

## Load-bearing (`battery/loadbearing.txt`, same envelope each run)

Each row: one variant module with the named fixture(s) dropped, run with `--only XO1,XO3`.

| dropped | XO1 | XO3 |
|---|---|---|
| `o_clause-freeze-single` | killed by=`o_clause-freeze-pair-edited-after` hits=1 | killed (hits=2) |
| `o_clause-freeze-pair-edited-after` | killed by=`o_clause-freeze-single` hits=1 | killed (hits=2) |
| `o_clause-receipt-withdrawn` | killed (hits=2) | killed by=`o_clause-receipt-side-line` hits=1 |
| `o_clause-receipt-side-line` | killed (hits=2) | killed by=`o_clause-receipt-withdrawn` hits=1 |
| `o_clause-clean-order` | killed (hits=2) | killed (hits=2) |
| **pair-freeze** (both XO1 fixtures) | **SURVIVED** `exhibits=none` | killed (hits=2) |
| **pair-receipt** (both XO3 fixtures) | killed (hits=2) | **SURVIVED** `exhibits=none` |

Recorded honestly: no single fixture is individually necessary — each mutant is killed by two independent
history shapes, so dropping one only moves `killed by=` to the sibling (`hits` 2→1), and the mutant flips to
`SURVIVED` exactly when its pair is gone (`MUTANTS total=2 killed=1 survived=1 … BY-TOOL order=1/2`, exit 1).
The clean accept fixture is not load-bearing in either direction (it carries no defect to silence).

## Full default counter on the clone with the module installed (`battery/full-run.txt`)

`mkdir -p $S/lane/plans/battery42 && cp battery/o_clause.py $S/lane/plans/battery42/` →
`python3 plans/round42_c1_verify.py --lane $S/lane --work $S/w2` inside the envelope. MUTANT + summary lines:

```
MUTANT X1 anchor rc-mirror SURVIVED exhibits=none ...
MUTANT X3 anchor rc-mirror SURVIVED exhibits=none ...
MUTANT X6 anchor silence SURVIVED exhibits=none ...
MUTANT X7 anchor silence SURVIVED exhibits=none ...
MUTANT X9 anchor rc-silence SURVIVED exhibits=none ...
MUTANT X12 anchor rc-mirror SURVIVED exhibits=none ...
MUTANT X13 anchor rc-silence SURVIVED exhibits=none ...
MUTANT X14 anchor silence SURVIVED exhibits=none ...
MUTANT X15 anchor rc-silence SURVIVED exhibits=none ...
MUTANT XO1 order rc-silence killed by=o_clause-freeze-single attributed=L183 hits=2 -- ...
MUTANT XO3 order rc-silence killed by=o_clause-receipt-withdrawn attributed=L188 hits=2 -- ...
MUTANT XO5 order rc-mirror SURVIVED exhibits=none ...
MUTANT XO6 order rc-mirror SURVIVED exhibits=none ...
MUTANT XO7 order rc-silence SURVIVED exhibits=none ...
BATTERY fixtures=5 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=2 survived=12 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/9 order=2/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 17:20:16 exit=1
LOCALBIN after 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -
```

`PINS total=2 mismatched=0` at the start of every run and `PINS-AFTER mismatched=0` at the end: both frozen
tools byte-identical before and after; no tool was edited, no pin was touched. The 9 anchor and 3 order
survivors are expected — this module only claims the order clauses 1 and 2 (an anchor module and the
XO5/XO6/XO7 shapes belong to sibling seats).

## Evidence index (all inside my report dir, each < 6 KiB)

| file | sha256 |
|---|---|
| `battery/o_clause.py` | `badc9e3d3807e22c99161ae3c991db1e0ed840dd8c76542dbf9643c210af163b` |
| `dev-run.txt` | `23fb08f84919a24af2b302994d81a032a594dd713f40803cdec568b1e8db2da0` |
| `loadbearing.txt` | `583ad05a3eedb96efe36f6cf267fe3f15c0fd931e66c332c6036bbcbbda9788d` |
| `full-run.txt` | `7aa0ebf3d61f0f732509ae83c8c9ef17a50b7fcc32a3a24c3fa38314d731396a` |

The clone copy `$S/lane/plans/battery42/o_clause.py` has the same digest
`badc9e3d3807e22c99161ae3c991db1e0ed840dd8c76542dbf9643c210af163b`, so the full-run measurement used
exactly the reported module. Nothing in the clone was committed (`git status --porcelain` → `?? plans/battery42/`);
no lane file was edited; no fleet-root file was written.

## Method notes and tooling

- No tool was installed (pacman is paused host-wide; nothing needed `uv`/`npx`/a release binary).
- Load-bearing variants were generated in scratch by dropping one `FIXTURES` entry from the module text;
  the reported module was never modified (`sha256sum` identically `badc9e3d…` at the first dev run, at the
  clone copy, and at the end).
- Operational finding for the wave (host behaviour, not a claim): the harness shell aborts the rest of a
  command line when a foreground command exits non-zero (`bwrap …; echo rc=$?` printed nothing after a
  counter that exits 1 — reproduced with `/bin/sh -c 'exit 1'` both with and without `--die-with-parent`).
  Every nonzero-exit run here therefore ends with `|| rc=$?` and writes its rc into the receipt; siblings
  that pipe a failing counter into more commands will silently lose that output.

## Risks / limits (named, not claimed away)

1. `hits=2` per mutant means the two fixtures per mutant execute the **same span line** (L183 / L188); the
   attribution proves the line ran, not that the two shapes were distinguished by different tool internals.
   They do differ in branch behaviour at the gate level (clause 2 is vacuous when `freeze == receipt_commit`).
2. Kill attribution is a result difference on a fixture that executes the mutated line, not proof of intent;
   the `o_clause-receipt-side-line` merge history proves the ancestry clause over a non-linear graph, but a
   shallower linear history would do — its value is shape diversity, not extra branch coverage.
3. The accept fixture's purpose is the pass path plus the clause-3 excuse line; it cannot be load-bearing.
4. A sibling seat writing `plans/battery42` for the anchor and XO5/XO6/XO7 surfaces must not reuse these
   fids (mine are `o_clause-*`) or these repositories' shapes; the counter rejects duplicate fids across the
   whole battery directory, and the L1 installs modules side by side.

VERDICT: battery42-o_clause-killed-2/2-wrong-0
