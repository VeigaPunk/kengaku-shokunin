# R44BatU14a — battery44 module `u14c_name_a` (frozen order mutant U14c)

Seat: executor (leaf). Lane: `kengaku-shokunin` (clone at `/fast/scratch/hyaku/kengaku-r44/R44BatU14a/lane`,
`rev-parse --show-toplevel` = that clone). Round 44 wave, C1 calibration. Nothing frozen was edited; no lane file was
edited; no commit, no `git add`, no jj call anywhere.

## Files written

| path | what |
|---|---|
| `.ufo/waves/round-44/wave/R44BatU14a/battery/u14c_name_a.py` | the battery44 module (stdlib only, no imports), sha256 `6e8dc5d0db31416ab21b7278e2b3dd70c4265c36f212708d03f998f13cd9bcf9` |
| `.ufo/waves/round-44/wave/R44BatU14a.md` | this report |

Nothing else in the lane was touched. Scratch-only artefacts (module copies for the load-bearing table, the mutant
copy of `order_check.py`, the driver) live under `/fast/scratch/hyaku/kengaku-r44/R44BatU14a/` and are deleted at the
end. No receipt file exceeds 1 MiB; no corpus/plans tree was copied into `wave/`.

## The mutant and its branch (read from the frozen counter)

`plans/round44_c1_verify.py:251-255` — `('U14c', 'order', '-', 'error', 'direct', ...)`, span `L161`:

```
old  '        if not m:\n            raise SetupError(f"claims file name'
new  '        if False:\n            raise SetupError(f"claims file name'
```

The replaced span is `plans/order_check.py:161-162` (guarded by `m = CLAIMS_NAME.match(Path(claims).name)` at `:160`,
`CLAIMS_NAME = ^round-(\d+)-claims\.md$`). With the guard gone, `m is None` and `:163 round_no = int(m.group(1))`
raises, so the advertised `Exit: ... 2 setup error (... unparseable round number, ...)` (`order_check.py:26-27`) loses
its only producer. Declared direction `error` = fixture `expect=error`, reference exits 2, mutant exits 0 or 1.

## Fixtures (4; every `defects` is `[]` because `order_check.py` prints no `class=` token)

| fid | expect | shape | why it reaches `:161` |
|---|---|---|---|
| `u14c_name_a-draft-suffix` | error | realistic three-round registry (`plans/round-42/43/44-claims.md`, `.ufo/waves/round-4N/claims/`), 4 commits; the canonical `plans/round-44-claims.md` is committed **and** a `.draft` copy sits beside it — the gate is handed `.draft` | name `round-44-claims.md.draft` does not match `^round-(\d+)-claims\.md$` |
| `u14c_name_a-subdir-nohyphen` | error | lane kept in a **subdirectory** `worktree/`, 5 commits incl. a `--no-ff` merge of a `record` side branch, receipt three directories deep | name `round44-claims.md` (hyphen lost) does not match |
| `u14c_name_a-uppercase-pair` | error | case-shifted root-level pair `ROUND-44-CLAIMS.md` + `evidence/probe.txt`, both added by the **first** commit, one later readme commit | name is uppercase; the regex is case-sensitive |
| `u14c_name_a-canonical-control` | accept | same registry as fixture 1, canonical name frozen first, receipt after | never reaches the guard — the name is the only mover |

Each `build(ctx, d)` returns the exact 6-token argv `["--lane", <repo in d>, "--claims", v, "--receipt", v]`; every
repo is built from nothing with `ctx.init`/`ctx.write`/`ctx.git`, no lane copy is read, every path lies inside `d`.
Module source carries no SIDECHANNEL token (checked with the counter's own tuple: `hits: []`).

## Evidence, run inside `claims/envelope.sh` (`~/.local/bin` read-only)

### 1. Development run — every FIXTURE `ok`, U14c killed and attributed

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44BatU14a/env /fast/scratch/hyaku/kengaku-r44/R44BatU14a/env --bind /fast/scratch/hyaku/kengaku-r44/R44BatU14a/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44BatU14a/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU14a/battery --only U14c --work /fast/scratch/hyaku/kengaku-r44/R44BatU14a/env/w
ENVELOPE start 20:33:06 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE u14c_name_a-draft-suffix tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_a-subdir-nohyphen tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_a-uppercase-pair tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_a-canonical-control tool=order expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U14c order error killed by=u14c_name_a-draft-suffix attributed=L161 value=differs hits=3 -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=1/1
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:33:08 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`hits=3` = all three `error` fixtures satisfy the direction; the kill is attributed at `L161` (leg f: the span line
ran) with `value=differs` (leg g: the site record differs).

### 2. Mechanism: reference 2, mutant 1 — the documented exit 2 is gone

Driver ran the frozen tool and its U14c replacement (same `old -> new`, `src.count(old) == 1` asserted) on the built
fixtures, cwd = fixture dir. Envelope `start 20:33:55` / `end 20:33:57 exit=0
local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`.

```
--- u14c_name_a-draft-suffix argv=['--lane', .../f000/registry, '--claims', 'plans/round-44-claims.md.draft', '--receipt', 'corpus/evidence/round44/probe.txt']
    reference rc=2 stdout=['ORDER RESULT ERROR']
    reference stderr_last=ORDER ERROR claims file name is not round-NN-claims.md: plans/round-44-claims.md.draft
    mutant rc=1 stdout=[]
    mutant stderr_last=AttributeError: 'NoneType' object has no attribute 'group'
--- u14c_name_a-subdir-nohyphen argv=['--lane', .../f001/worktree, '--claims', 'plans/round44-claims.md', '--receipt', 'corpus/evidence/round44/receipts/feal-linear-probe.txt']
    reference rc=2 stdout=['ORDER RESULT ERROR']
    reference stderr_last=ORDER ERROR claims file name is not round-NN-claims.md: plans/round44-claims.md
    mutant rc=1 stdout=[]
    mutant stderr_last=AttributeError: 'NoneType' object has no attribute 'group'
--- u14c_name_a-uppercase-pair argv=['--lane', .../f002/lane, '--claims', 'ROUND-44-CLAIMS.md', '--receipt', 'evidence/probe.txt']
    reference rc=2 stdout=['ORDER RESULT ERROR']
    reference stderr_last=ORDER ERROR claims file name is not round-NN-claims.md: ROUND-44-CLAIMS.md
    mutant rc=1 stdout=[]
    mutant stderr_last=AttributeError: 'NoneType' object has no attribute 'group'
```

Control fixture identical under both tools (`rc=0`, same `ORDER scanned commits=1 file_entries=1 distinct_blobs=1`,
`ORDER RESULT PASS`), so the name branch is the only mover in this module.

### 3. Load-bearing table (each fixture removed in turn; envelope `start 20:33:18` / `end 20:33:22 exit=0
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`)

| variant | fixtures | `killed` | killed by | hits | load-bearing? |
|---|---|---|---|---|---|
| without `draft-suffix` | 3 (`wrong=0 tampered=0 sidechannel=0`) | 1 | `u14c_name_a-subdir-nohyphen` | 2 | no — the other two still kill |
| without `subdir-nohyphen` | 3 (`wrong=0 …`) | 1 | `u14c_name_a-draft-suffix` | 2 | no |
| without `uppercase-pair` | 3 (`wrong=0 …`) | 1 | `u14c_name_a-draft-suffix` | 2 | no |
| without `canonical-control` | 3 (`wrong=0 …`) | 1 | `u14c_name_a-draft-suffix` | 3 | not for the kill (it is the acceptance control) |

Removing any single fixture leaves `killed=1 survived=0 unattributed=0` — the kill is deliberately over-determined.
Minimal batteries (each `error` fixture alone; envelope `start 20:33:29` / `end 20:33:32 exit=0
local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`) each still kill on their own:

```
=== ONLY u14c_name_a-draft-suffix
FIXTURE u14c_name_a-draft-suffix tool=order expect=error declared=- observed_rc=2 observed=- ok
MUTANT U14c order error killed by=u14c_name_a-draft-suffix attributed=L161 value=differs hits=1 -- ...
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
=== ONLY u14c_name_a-subdir-nohyphen
MUTANT U14c order error killed by=u14c_name_a-subdir-nohyphen attributed=L161 value=differs hits=1 -- ...
=== ONLY u14c_name_a-uppercase-pair
MUTANT U14c order error killed by=u14c_name_a-uppercase-pair attributed=L161 value=differs hits=1 -- ...
```

So every `error` fixture is individually sufficient and none is a duplicate of another's trigger.

### 4. Full default counter with the module installed as `plans/battery44/u14c_name_a.py` in the clone
(`cp` outside the envelope; clone copy sha256 = module sha256; envelope `start 20:33:37` / `end 20:33:40 exit=1
local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`)

```
PINS total=2 mismatched=0
FIXTURE u14c_name_a-draft-suffix tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_a-subdir-nohyphen tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_a-uppercase-pair tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_a-canonical-control tool=order expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U5 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U6 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U7 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
MUTANT U9 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
MUTANT U14c order error killed by=u14c_name_a-draft-suffix attributed=L161 value=differs hits=3 -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/4 order=1/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 20:33:40 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`MUTANTS-BY-TOOL anchor=0/4 order=1/1` is exactly this seat's scope: the four anchor mutants are other seats'
modules; my module contributes the single order kill. `PREDICATE C1 fail` at exit 1 is the expected integrated state
of a clone whose `battery44` holds one seat's module, not a defect of this module. Envelope status is `unchanged`
on every run (five runs, one `local_bin` digest value `328be01808ba022f`), so no measurement is void and no re-run
was needed.

## Limits

1. **One exit direction per fixture.** Every trigger makes the mutant die at `m.group(1)` (`rc=1`); no fixture can
   show the mutant exiting 0, because the `.group(1)` use is outside the replaced span. The kill therefore rests on
   "reference 2, mutant 1", not on a mutant that silently passes.
2. **Counter-visible intent only.** The kill is a recorded result difference on the declared branch plus a differing
   site record; it does not prove the fixture author's story. Non-author review of `battery44` stays necessary.
3. **`defects=[]` is forced** for `order` fixtures (the tool prints no `class=` token), so no class-set leg protects
   this module: the `expect`/rc leg alone distinguishes reference from mutant.
4. **Over-determination hides single-fixture rot.** Because three fixtures kill independently, losing one to future
   fixture drift would not turn the module red in the integrated run; the minimal-battery table above is the
   evidence that each one works today.
5. **Independence.** `claims/witness/w_u.py` was not read, imported, copied or executed by this seat or by the
   module; the shapes here (draft-beside-canonical, subdirectory lane with a merge commit, case-shifted single
   commit) were derived from `order_check.py` alone. Whether they are a re-spelling is a non-author call.
6. **Traced-run determinism** was confirmed only by the counter's own `null_detected=0` and stable reference
   double-tracing; i.e. by the tool, not by an independent trace reading.
7. **No tool was installed or upgraded** in this seat (nothing was needed); no pacman call was made.

Scratch `/fast/scratch/hyaku/kengaku-r44/R44BatU14a` removed with `plans/scratch_guard.py safe-rm` after this
report was written.

VERDICT: battery44-u14c_name_a-U14c-killed-yes-fixtures-4
