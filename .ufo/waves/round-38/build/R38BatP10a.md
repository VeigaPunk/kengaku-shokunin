# R38BatP10a — battery38 module for the P10 receipt-reproduction silences (N13, N14)

Seat: executor, round 38 wave 1 (hyaku 8, 2026-10-26). Lane read-only; nothing under `corpus/`, `plans/`,
`SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`, `SHONEN.md` was touched, no git/jj mutation
in the lane. Frozen inputs read only: `plans/round38_c1_verify.py` (mutant table), `plans/pkg_gate.py`
(`c_rerun`, `PACKAGE_CHECKS`), `plans/pkg-spec-r35.json`, `plans/round36_c1_verify.py` (`copy_package`,
`stub_probe`), `plans/round37_c1_verify.py` (`Ctx`).

## Deliverable

| path | sha256 |
|---|---|
| `.ufo/waves/round-38/build/R38BatP10a/battery/p10a.py` | `e65f7a542ee08d00bce3d67cedc03cd87197ebe7f86fdc3017745b0cb4f5cc2a` |

Stdlib only (`hashlib`, `json`). Side-channel token scan clean: `/proc` 0, `ppid` 0, `cmdline` 0,
`psutil` 0, `environ` 0 (command: `python3 -c` count over the file, output above). Prefix `p10a-`, two
fixtures, one per mutant, fids `p10a-n13-trailing-space` and `p10a-n14-first-line-only`.

Working copies kept beside it for the L1 (evidence, not deliverables):
`R38BatP10a/c1-n13-n14.txt` (full counter output, 72 lines), `R38BatP10a/deletion-matrix.txt`.

## Shape

Both fixtures: `ctx.genuine_package(d)` (git-init + the genuine round-35 package bytes), a fixture-local
probe, a **spec owned by the fixture** (`p10a-spec.json` inside `d`), `ctx.git_add(d)`, argv
`package --root d --require-clean-tree --rerun --spec d/p10a-spec.json`.

The owned spec is `json.loads(json.dumps(ctx.spec))` with one change: `probe_cmd = ["p10a-probe.py"]`.
That is why P1 keeps verifying for real instead of firing: `c_instruments` pins the genuine
`plans/tb2_grader_probe.py` bytes, which are copied untouched — contrast the round-36 P5 recipe, which
overwrites that pinned path (`round36_c1_verify.py:120-123`, `stub_probe`) and therefore drags P1 in.
The probe reads its input at run time (`pathlib.Path(<spec["receipt"]>).read_text()`, cwd = root), so the
fixture survives the counter's RENAMED copy (`renamed_disagree=0`).

- **N13** (`pkg_gate.py:283` `if r.stdout != want:` → `if r.stdout.rstrip() != want.rstrip():`):
  the fixture rewrites the receipt at the genuine receipt path with ONE line
  (`p10a fixture receipt: fresh-run byte-compare target\n`) and re-pins `receipt_sha256` in its owned spec,
  so `c_receipt` still verifies real bytes (P2 `ok`); the probe prints that line with three trailing spaces
  before the newline. Reference: byte-unequal → `P10 DEFECT`; mutant: `rstrip`-equal → `P10 ok`.
- **N14** (`if r.stdout != want:` → `if r.stdout.splitlines()[:1] != want.splitlines()[:1]:`):
  genuine receipt and the frozen r35 digest untouched; the probe reproduces line 1 verbatim
  (`grader=corpus/evidence/round35/tb2-eval/test_outputs.py …`) then prints `p10a-receipt-tail-diverges`.
  Reference: `P10 DEFECT`; mutant: first lines equal → `P10 ok`.

Declared defect set per fixture is `["P10"]`, measured, not asserted: `observed_defects=P10` on both rows.

**Why N13's receipt is one line (the only judgement call).** Both mutants replace the same gate line and
N13's `rstrip` is the weaker test: any stdout that is `rstrip`-equal to a multi-line receipt repeats that
receipt's first line byte-for-byte, so N14's first-line-only mutant accepts it too. Measured — with the
genuine 21-line receipt as the N13 fixture's `want`, the counter recorded
`MUTANT N14 … killed by=p10a-n13-trailing-space`, i.e. the N13 fixture over-killed N14 and neither fixture
was individually load-bearing. A single-line receipt is the only shape whose entire difference IS trailing
whitespace, so N13's fixture reddens N13 alone. The advertised behaviour under test is unchanged ("a
receipt differing only in trailing whitespace is not reproduced"); the receipt shape is not constrained by
the gate (only `c_receipt`'s digest is), and the fixture's spec pins the bytes it writes.

## Evidence (verbatim)

Command (fast, ~16 s wall):

```
S=/fast/scratch/hyaku/kengaku-r38/R38BatP10a; export TMPDIR="$S"
python3 plans/round38_c1_verify.py --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatP10a/battery \
  --only N13,N14 --work "$S/w3"
```

Clone verified before any write: `git -C "$S/lane" rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r38/R38BatP10a/lane`. Exit code 0. Output lines 1 and 66-72:

```
PINS total=14 mismatched=0
FIXTURE p10a-n13-trailing-space expect=reject declared=P10 observed_rc=1 observed_defects=P10 ok
FIXTURE p10a-n14-first-line-only expect=reject declared=P10 observed_rc=1 observed_defects=P10 ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N13 P10 silence killed by=p10a-n13-trailing-space -- a receipt differing only in trailing whitespace is not reproduced [docstring 'a receipt a fresh run does not reproduce'; F37XMutP910 L1]
MUTANT N14 P10 silence killed by=p10a-n14-first-line-only -- the receipt is compared beyond its first line [capability row '--rerun byte-compares the receipt'; F37XMutP910 L3]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`fixtures=66` = 64 frozen (round-36 + battery37) + my 2; `wrong=0` and `renamed_disagree=0` are measured
over all 66, `null_detected=0` over all 66 (null gate = byte-identical gate copy, so it also proves no
fixture depends on wall clock, host env or a mutable file it does not own).

### Load-bearing table (each fixture deleted in turn)

Scratch copies of the module with the named `FIXTURES` entry removed, same command, `--work` per row
(full text: `R38BatP10a/deletion-matrix.txt`):

| battery contents | N13 | N14 |
|---|---|---|
| both fixtures | `killed by=p10a-n13-trailing-space` | `killed by=p10a-n14-first-line-only` |
| delete `p10a-n13-trailing-space` | **SURVIVED** | `killed by=p10a-n14-first-line-only` |
| delete `p10a-n14-first-line-only` | `killed by=p10a-n13-trailing-space` | **SURVIVED** |
| delete both (`fixtures=64`) | **SURVIVED** | **SURVIVED** |

Every deletion row kept `wrong=0 renamed_disagree=0 sidechannel=0 null_detected=0`; the "delete both" row
reproduces the freeze control's 0/22 shape for these two mutants on the frozen battery alone — the shipped
fixtures are the only kill path.

## Notes for the L1

- The two modules' P10 runtime is the `uv run --no-project --with biopython==1.85 python3` branch of
  `c_rerun` (no `Bio` in the host python here: `ModuleNotFoundError: No module named 'Bio'`). uv's cached
  env makes it ~milliseconds after first use (`time uv run … -c "print('uvpath ok')"` → 0.012 s real), so
  the full 66-fixture run above is 16 s; no network is needed at landing if uv's cache is warm, and the
  probe here is a 2-line local script, never the real grader.
- The module needs nothing from `plans/battery38/` besides itself; copy `R38BatP10a/battery/p10a.py` to
  `plans/battery38/p10a.py`. It declares no path, no absolute `d`, and no host assumption, and reads only
  `ctx.spec` / `ctx.genuine_package` / `ctx.git_add` (the round-37 `Ctx` API).
- Landed C1 needs the other seats' modules for N01-N12, N15-N22; this seat's contribution is
  `killed=2/2` of `{N13, N14}` with `wrong=0`.

## Limits / risks

- The N13 fixture's receipt is a fixture-authored one-liner, not the round-35 receipt. A reviewer wanting
  every battery38 P10 fixture to re-run the genuine receipt will find one fixture (N14) that does; the
  trade is documented above and is what makes the pair individually load-bearing.
- `--rerun` fixtures cannot exercise `c_rerun`'s `returncode != 0` arm or the `Bio`-present interpreter
  branch from here (host has no `Bio`; making the probe exit non-zero is a different behaviour and belongs
  to a P10 seat that owns it). Not attempted.
- Attributed kills are the counter's rule, not intent: if a future counter run reorders `FIXTURES` across
  modules, the recorded `by=` for N14 could change only if another module ships an equivalent
  `rstrip`-equal / first-line-identical P10 fixture. No such fixture exists in the frozen battery (the
  "delete both" row proves it).
- No tool installs: nothing was needed; `pacman` transactions are paused host-wide and were not touched.
  Scratch `/fast/scratch/hyaku/kengaku-r38/R38BatP10a` removed at the end of the seat.

VERDICT: battery38-p10a-killed-2/2-wrong-0
