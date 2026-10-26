# R38BatP4a — battery38 `p4a`: attributed kills for frozen mutants N03 and N04

Seat: R38BatP4a (executor, leaf). Wave: round 38 wave 1. Lane clone: `/fast/scratch/hyaku/kengaku-r38/R38BatP4a/lane`
(`git clone -q --shared` of the lane; `git -C … rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r38/R38BatP4a/lane`).

## Deliverable

`plans/battery38/p4a.py` drafted at
`.ufo/waves/round-38/build/R38BatP4a/battery/p4a.py` (single module, stdlib only, every fid prefixed `p4a-`):

```
sha256 = 60f34aa2ed1fac71be6d8e4af2dfb8c2a09e4322578f643517cdbad0f1fbffbf   (95 lines)
```

```
$ sha256sum .ufo/waves/round-38/build/R38BatP4a/battery/p4a.py
60f34aa2ed1fac71be6d8e4af2dfb8c2a09e4322578f643517cdbad0f1fbffbf  …/battery/p4a.py
$ wc -l .ufo/waves/round-38/build/R38BatP4a/battery/p4a.py
95 …/battery/p4a.py
$ grep -nE '/proc|ppid|cmdline|psutil|environ' …/battery/p4a.py || echo "sidechannel-tokens: none"
sidechannel-tokens: none
```

Nothing frozen was touched: the clone's `plans/` differs from the lane only by the added
`plans/battery38/p4a.py` that the counter's default-battery run needs; `PINS total=14 mismatched=0` in every run below
proves the pinned inputs are byte-identical. No write of any kind reached the lane repo (drafts and receipts live in
this report dir; scratch is `/fast/scratch/hyaku/kengaku-r38/R38BatP4a` and is deleted before yield).

## Fixtures and what they separate

Both mutants shrink `c_quote_verbatim` in `plans/pkg_gate.py:138-150`; both are `dir=silence` on clause `P4`, so each
kill needs a fixture where the unmodified gate prints `P4 DEFECT` and the mutant prints `P4 ok`, with the declared
defect set exactly equal to the reference set.

| fid | mutant | construction | reference | mutant |
|---|---|---|---|---|
| `p4a-second-row-line-outside` | N03 (`for q in p.quotes:` → `p.quotes[:1]`) | retarget the **second** data row of `## Located quotes` (was `test_outputs.py:16`) to line `max(len(capture), start)+1000` = 1073; capture has 73 lines | `P4 DEFECT … test_outputs.py:1073-1073: line range outside the capture` | row 2 never visited → `P4 ok` |
| `p4a-text-elsewhere` | N04 (`lines[q.start-1:q.end]` → `lines`) | retarget the **first** row (`test_outputs.py:13`) to line 1, which does not contain the quote text; the text stays byte-verbatim at its original line 13, so it *is* somewhere in the capture | `P4 DEFECT … test_outputs.py:1: quote not verbatim there` | text found anywhere → `P4 ok` |

Both builders start from `ctx.genuine_package(d)`, edit only one existing row via `ctx.r36.rewrite_quotes`, keep the
quote text, word count and capture name unchanged, stage index-only with `ctx.git_add`, and return
`["package","--root",str(d),"--require-clean-tree"]`. Neither fixture keys on a name or path.

Gate output on each built tree (unmodified gate, frozen r35 spec), directly observed:

```
--- p4a-second-row-line-outside rc=1
P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
P4 DEFECT checked=22 bad=1 first=test_outputs.py:1073-1073: line range outside the capture
P5 ok manifest_entries=6 bad=0 first=0
defects=1
--- p4a-text-elsewhere rc=1
P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
P4 DEFECT checked=22 bad=1 first=test_outputs.py:1: quote not verbatim there
P5 ok manifest_entries=6 bad=0 first=0
defects=1
```

So `defects` = `["P4"]` exactly for both (P3 stays `ok` because the new line is cited by no other row, keeping 22
distinct `(capture, start)` pairs; P5 stays `ok` because the capture name is unchanged).

## Required run — every fixture `ok`, both mutants killed at 2/2

```
$ python3 plans/round38_c1_verify.py --lane "$S/lane" \
    --battery-dir <report>/battery --only N03,N04 --work "$S/w"
PINS total=14 mismatched=0
… (66 FIXTURE lines, all ok) …
FIXTURE p4a-second-row-line-outside expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p4a-text-elsewhere expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N03 P4 silence killed by=p4a-second-row-line-outside -- every quote is checked, not only the first [docstring 'a quote not verbatim on its cited line'; F37XMutP4 X2]
MUTANT N04 P4 silence killed by=p4a-text-elsewhere -- verbatim on the CITED lines, not anywhere in the capture [capability row 'verbatim on its cited capture line'; F37XMutP4 X4]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Exit status 0. Full receipt: `.ufo/waves/round-38/build/R38BatP4a/receipt-only-n03-n04.txt`.

The same command **without** `--battery-dir`, after installing the draft at `plans/battery38/p4a.py` inside the clone
(the landing form), prints the same two `FIXTURE … ok` lines, `BATTERY fixtures=66 wrong=0 renamed_disagree=0
sidechannel=0`, `MUTANT … killed by=<my fid>` for N03 and N04, `MUTANTS total=2 killed=2 survived=0 invalid=0
null_detected=0`.

## Load-bearing table (delete each fixture in turn)

Variant modules in scratch (`lb/noA`, `lb/noB`) re-export the draft's `FIXTURES` minus one entry; each was run with
`--battery-dir` over that dir, `--only N03,N04`. Receipts:
`.ufo/waves/round-38/build/R38BatP4a/receipt-loadbearing-noA.txt` / `…-noB.txt`.

```
== --battery-dir lb/noA   (p4a-second-row-line-outside removed)
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N03 P4 silence SURVIVED -- …
MUTANT N04 P4 silence killed by=p4a-text-elsewhere -- …
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
== --battery-dir lb/noB   (p4a-text-elsewhere removed)
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N03 P4 silence killed by=p4a-second-row-line-outside -- …
MUTANT N04 P4 silence SURVIVED -- …
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
```

Each deletion flips exactly one mutant to SURVIVED and leaves the other killed: neither fixture is redundant, and no
fixture kills the other mutant.

## No-harm cross-check (full 22-mutant run with the module installed)

```
$ python3 plans/round38_c1_verify.py --lane "$S/lane" --work "$S/w"    # clone has plans/battery38/p4a.py
PINS total=14 mismatched=0
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N03 P4 silence killed by=p4a-second-row-line-outside -- …
MUTANT N04 P4 silence killed by=p4a-text-elsewhere -- …
MUTANT N01/N02/N05…N22 … SURVIVED -- …        (20 survivors: other seats' wave-1 work, untouched by p4a)
MUTANTS total=22 killed=2 survived=20 invalid=0 null_detected=0
PREDICATE C1 fail
```

`fail` is expected at wave 1 (20 mutants have no fixture yet); the evidence I claim from it is that `p4a` kills exactly
N03 and N04, adds no `wrong`, no `renamed_disagree`, no `sidechannel`, and no invalid mutant. Runtime 52 s.

## Limits / risks

- `c_rerun` (P10) needs `biopython==1.85`; the host `python3` has no `Bio` (`ModuleNotFoundError`), so each gate run
  takes the gate's `uv run --no-project --with biopython==1.85` branch (cached here, ~0.08 s/run). Nothing was
  installed by this seat; if a landing host lacks that uv cache, the counter gets slow (not wrong).
- `p4a-text-elsewhere` picks the retarget line dynamically (first uncited line of the capture that lacks the quote
  text); on the frozen capture that is line 1. If the capture or the entry rows changed, the fixture re-derives a
  valid line instead of hard-coding one — both are pinned, so this is belt-and-braces, not a live dependency.
- The counter's attributed rule ties a kill to the mutant's clause and direction, not to fixture intent; the
  separations above are the argument for intent, and the load-bearing table is the operative evidence.
- No tool was installed or upgraded (uv cache reused as-is). No pacman transaction was attempted.

VERDICT: battery38-p4a-killed-2/2-wrong-0
