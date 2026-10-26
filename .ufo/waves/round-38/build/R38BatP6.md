# R38BatP6 — battery38 module for the frozen P6 mutants N09/N10

Seat: executor, kengaku round 38 wave 1. Deliverable: one battery38 module, `p6m.py`, with one
single-defect fixture per mutant, proven on a scratch clone of the lane.

## Files

| path | role |
|---|---|
| `.ufo/waves/round-38/build/R38BatP6/battery/p6m.py` | **the deliverable** (stdlib only, 5251 bytes, sha256 `3a42982e54ddcf9af47bbad1df05a55987c6cfbcb697612553373c888c8b2e97`); L1 lands it as `plans/battery38/p6m.py` |
| `.ufo/waves/round-38/build/R38BatP6/receipts/c1-n09-n10-full.txt` | full counter output (66 `FIXTURE` lines, `BATTERY`, `MUTANT`, `MUTANTS`) |
| `.ufo/waves/round-38/build/R38BatP6/receipts/load-bearing.txt` | the two deletion runs |
| `.ufo/waves/round-38/build/R38BatP6.md` | this report |

Nothing outside `.ufo/waves/round-38/build/R38BatP6*` and `/fast/scratch/hyaku/kengaku-r38/R38BatP6`
was written. No lane file, corpus, plan, spec, counter or capture was edited; no git/jj mutation
outside the scratch clone's index (`git add -A`, no commit).

## What the two fixtures do

Both start from the genuine round-35 package (`ctx.genuine_package(d)` → git-init + `copy_package`),
inject exactly one defect in one registry row of `corpus/SOURCES.md`, stage index-only
(`ctx.git_add(d)`) and return `["package", "--root", <d>, "--require-clean-tree"]`. P6 (`c_sources`,
`plans/pkg_gate.py:184-209`) is the only clause reading the registry, so each declares `defects=["P6"]`
and `expect="reject"`; no fixture owns a spec, so the counter appends the frozen `pkg-spec-r35.json`.

Cells are edited by index (never a whole-line substring), and the builder asserts its own preconditions
(one matching row; the pinned URL occurs exactly once in the source cell; the target word count is
exactly `min_teaches_words - 1`; the cell does not collide with another row's teaches cell), so a
silently different tree cannot produce a green fixture.

- **`p6m-n09-teaches-one-below-min`** — mutant N09 (`plans/round38_c1_verify.py`, `old -> new`:
  `len(cells[6].split()) < rules["min_teaches_words"]:` → `... < rules["min_teaches_words"] - 1:`).
  The fixture writes S105's teaches cell as exactly `min_teaches_words - 1` = 7 distinct words
  (`"n09 teaches boundary off by one floor"`), derived from `ctx.spec["entry_rules"]`, not hardcoded.
  The frozen gate prints `P6 DEFECT S105: teaches words=7`; N09's threshold is `< 7`, so 7 passes and
  P6 is `ok`. This is the boundary the round-37 battery never sat on: its only sub-threshold cells are
  5 words (`p6-m26`) and 1 word, so lowering the threshold by one changed nothing
  (`.ufo/waves/round-37/falsify/F37XMutP6.md`, X1 row).
- **`p6m-n10-url-scheme-http`** — mutant N10 (`url.group(0) != p.spec["raw_base"] + row["upstream"]`
  → compare both sides `.split("://", 1)[-1]`). The fixture rewrites the pinned raw URL inside S105's
  source cell `https://…` → `http://…` (scheme only, same host/path). The reference compares the URL
  text against `raw_base + upstream`, so `P6 DEFECT S105: url not the pinned raw path`; N10 strips the
  scheme from both sides, so they match and P6 is `ok`. `URL = re.compile(r"https?://\S+")`
  (`pkg_gate.py:30`) is scheme-tolerant, so the http URL reaches the comparison.

## Evidence

Scratch clone (removed before finishing):

```
S=/fast/scratch/hyaku/kengaku-r38/R38BatP6
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r38/R38BatP6/lane
git -C "$S/lane" rev-parse HEAD              -> 2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e
```

Run (from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, `TMPDIR="$S"`):

```
python3 plans/round38_c1_verify.py --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatP6/battery \
  --only N09,N10 --work "$S/w"
PINS total=14 mismatched=0
… (64 pre-existing FIXTURE lines, every one `ok`)
FIXTURE p6m-n09-teaches-one-below-min expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6m-n10-url-scheme-http expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N09 P6 silence killed by=p6m-n09-teaches-one-below-min -- a teaches cell below min_teaches_words is a defect [capability row 'teaches cells carry >=8 distinct words'; F37XMutP6 X1]
MUTANT N10 P6 silence killed by=p6m-n10-url-scheme-http -- the row URL is the pinned raw URL including its scheme [F37XMutP6 X4]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit 0
```

Full transcript: `receipts/c1-n09-n10-full.txt` (66 `FIXTURE` lines; `PINS total=14 mismatched=0`).
`renamed_disagree=0` covers both fixtures: the counter copies each fixture dir to a different name and
re-runs the gate, and the `(rc, DEFECT set)` pair does not change, so the fixtures read only in-tree
content and never their own path. `sidechannel=0`: the module source contains none of `/proc`, `ppid`,
`cmdline`, `psutil`, `environ` (checked both by the counter and by `grep -nE` → no match).

### Load-bearing table (each fixture removed in turn, same module otherwise)

```
=== battery module with noN09 fixture removed ===
FIXTURE p6m-n10-url-scheme-http … ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N09 P6 silence SURVIVED -- a teaches cell below min_teaches_words is a defect …
MUTANT N10 P6 silence killed by=p6m-n10-url-scheme-http …
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
=== battery module with noN10 fixture removed ===
FIXTURE p6m-n09-teaches-one-below-min … ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N09 P6 silence killed by=p6m-n09-teaches-one-below-min …
MUTANT N10 P6 silence SURVIVED -- the row URL is the pinned raw URL including its scheme …
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
```

`receipts/load-bearing.txt`. Each fixture is the **sole** killer of its own mutant: remove it and that
mutant flips to SURVIVED (1/2), while the other kill is untouched. Neither fixture kills the other's
mutant, so the two kills are not shared.

## Behaviour of the deliverable

`FIXTURES` exports exactly two dicts, `fid` prefix `p6m-`, `expect="reject"`, `defects=["P6"]`, and a
builder that is a pure function of `ctx` + the empty dir. Prefix collision check against the wave-1
sibling battery dirs present at the time of writing
(`grep -ho '"fid": "[^"]*"' */battery/*.py | cut -d- -f1 | sort -u` plus `R38BatP3`'s `FID`
constant): `b1run`, `d4m`, `d5m`, `mainx`, `p10a`, `p10b`, `p3m`, `p4a`, `p4b`, `p5m`, `p6m`, `p7m` —
`p6m` appears only in this module. The pre-existing battery rows the counter also loads are
`r36-*`, `d4-L*`/`d5-L*` and battery37's `p6-m*`/`p7-m*`-style ids, none prefixed `p6m-`.

The builder touches no filesystem state outside `d`, no time, no randomness, no network and no
subprocess of its own (the counter runs the gate); no spec is supplied, so the counter appends the
frozen `pkg-spec-r35.json`.

## Risks / blockers

- **Integration is the L1's step.** The module must land as `plans/battery38/p6m.py`; until then it
  only exists under `.ufo/waves/round-38/build/R38BatP6/battery/`. I did not touch the lane.
- **Boundary values are derived, not pinned.** N09 needs exactly `min_teaches_words - 1` and N10 needs
  `https`. Both come from `ctx.spec` at build time with an explicit `raise` if the shape is not what the
  fixture assumes, so a future spec change fails loudly (SETUP error) rather than producing a
  false-green fixture. Against the frozen `pkg-spec-r35.json` (`min_teaches_words=8`,
  `raw_base=https://…`) they are 7 and the scheme swap.
- `--only N09,N10` was used as assigned; the counter prints `PREDICATE C1 n/a (non-default battery or
  mutant subset)`. The landing-wide `MUTANTS total=22 killed=22` is the L1's composite run, not something
  this seat can claim.
- The counter's side-channel scan is a token heuristic (named limit in `plans/round-38-claims.md`); the
  stronger evidence here is the rename comparison plus the builder's own assertions.
- No tools were installed or upgraded (pacman transactions are paused host-wide); nothing was needed.

VERDICT: battery38-p6m-killed-2/2-wrong-0
