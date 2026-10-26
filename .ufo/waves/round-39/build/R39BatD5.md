# R39BatD5 — battery39 module `d5m39`, the D5 tag-strip kill of frozen mutant M07

Seat: executor R39BatD5 (leaf). Wave 1 of round 39 (kengaku, hyaku run 8, 2026-10-26).
Assignment: write one battery39 module whose fixtures ATTRIBUTABLY kill frozen mutant **M07**
(clause `D5`, direction `mirror`) in its declared direction; prove it, prove each fixture
load-bearing, and run the full default counter.

Result: **M07 killed by=`d5m39-tagged-quote-span`**, `wrong=0 renamed_disagree=0 sidechannel=0`,
`null_detected=0`, `invalid=0`. Deleting the fixture flips M07 to `SURVIVED exhibits=none`.

## 1. Files written

| path | what |
|---|---|
| `.ufo/waves/round-39/build/R39BatD5/battery/d5m39.py` | the module (94 lines, stdlib only, one fixture, fid prefix `d5m39-`) |
| `.ufo/waves/round-39/build/R39BatD5/only-m07.txt` | receipt: `--only M07` run over the module |
| `.ufo/waves/round-39/build/R39BatD5/probe-receipt.txt` | receipt: reference gate vs M07 gate on the built fixture, plus capture invariants |
| `.ufo/waves/round-39/build/R39BatD5/load-bearing-lb-fixture-deleted.txt` | receipt: fixture removed from the module |
| `.ufo/waves/round-39/build/R39BatD5/load-bearing-lb-module-absent.txt` | receipt: module absent from the battery dir |
| `.ufo/waves/round-39/build/R39BatD5/full-run.txt` | receipt: full default counter with the module in `plans/battery39/` |
| `.ufo/waves/round-39/build/R39BatD5.md` | this report |

Module digest (`sha256sum`):

```
cb2edc678ccba64123694e7cf74f06a2990f72d9ca8b4025c1670ce828840538  .../R39BatD5/battery/d5m39.py
```

No lane file was written, no git/jj mutating command was run against the lane, nothing was
installed. Scratch `S=/fast/scratch/hyaku/kengaku-r39/R39BatD5` (clone of the lane at the same
tip, verified `git -C "$S/lane" rev-parse --show-toplevel` -> `/fast/scratch/hyaku/kengaku-r39/R39BatD5/lane`)
was removed at the end; all receipts above were copied out first.

## 2. The mutant and the branch it mutates

`plans/round39_c1_verify.py` M07 (`("M07", "D5", "mirror", ...)`):

```
old  '        flat = re.sub(r"\\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))'
new  '        flat = re.sub(r"\\s+", "", read(capture) or "")'
```

Frozen gate branch, `plans/pkg_gate.py:352-354` (pinned digest `ea638822…`):

```
        flat = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))
        if re.sub(r"\s+", "", d5["quote"]) not in flat:
            bad.append("quote absent from the capture")
```

So the tag strip is load-bearing only when the capture's **quote span itself** carries markup:
then the reference finds the flat quote (`D5 ok`) and M07 does not (`D5 DEFECT`). That is exactly
M07's declared direction and its committed pre-freeze witness
`.ufo/waves/round-38/falsify/F38XMutRerunMain/survivor-probeB.txt`:

```
REF tagged-capture: 0 ['D5 ok directional=True digest_pinned=True bad=0']
X15 tagged-capture: 1 ["D5 DEFECT directional=False digest_pinned=True bad=['quote absent from the capture']"]
```

## 3. The fixture (one, deliberately)

`build(ctx, d)` copies the frozen capture dir `ctx.d5_capture_dir()` into `d/captures`, then:

1. rewrites only `nec-s091-reopen.html` — the single occurrence of `ctx.spec["d5"]["quote"]` is
   split in three and each third wrapped in inline markup `<b>…</b><span class="str-inner">…</span><em>…</em>`,
   inserted in place (no newline added, no byte outside the span touched);
2. re-pins that one row of `quarantine-SHA256SUMS` to the new capture digest, leaving the other
   row byte-identical;
3. writes `d/erratum.md` with the genuine frozen D5 line (`ctx.d5_line()` — it carries the spec's
   `require` token and none of its `forbid` token);
4. returns `["d5-line", "--file", <d>/erratum.md, "--capture-dir", <d>/captures]` — both paths
   inside `d`, so the counter's rename leg rewrites them and agrees.

Declared `expect="accept"`, `defects=[]` — the exact DEFECT set the unmodified gate prints (none).
Build-time guards raise instead of returning a weak fixture: the quote must occur exactly once in
the frozen capture, the rewrite must not change the newline count, and the tag-stripped text of
the capture must be unchanged by the rewrite (so the **only** difference the gate can see is
markup inside the span).

Measured on the built fixture (`probe-receipt.txt`):

```
== capture genuine_bytes=60335 built_bytes=60382 delta=47 CR genuine=21 built=21 LF genuine=422 built=422
== tag-stripped capture holds the flat quote: True
== raw capture holds the flat quote: False
== capture sha256: 7c421e7184d12fc8fa9a882d7f63672bdc9afd16ee1f8590bcd00edae61377e5
== REF rc=0 stdout='D5 ok directional=True digest_pinned=True bad=0\ndefects=0'
== M07 rc=1 stdout="D5 DEFECT directional=False digest_pinned=True bad=['quote absent from the capture']\ndefects=1"
```

delta 47 == the 47 bytes of inserted markup; the erratum line's own claim — “present in this
round's own reopen capture … after tag-strip and whitespace removal, raw HTML line 276” — is the
advertised reading the fixture exercises, and line 276 is untouched.

Why exactly one fixture: with two M07-killing fixtures neither would be individually
load-bearing (removing one would leave the other a kill). The counter stops at the **first**
fixture that exhibits the direction (`break`), so a companion kill would mask the deletion test
the assignment asks for; a non-killing control would simply not be covered by that test. One
killing fixture, no companion.

## 4. Evidence

### E1 — `--only M07` over the module (the requested receipt)

```
$ python3 plans/round39_c1_verify.py --lane "$S/lane" \
    --battery-dir .ufo/waves/round-39/build/R39BatD5/battery --only M07 --work "$S/w"
PINS total=26 mismatched=0
... (86 pre-existing battery fixtures, all ok) ...
FIXTURE d5m39-tagged-quote-span expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M07 D5 mirror killed by=d5m39-tagged-quote-span -- a D5 quote is found in a capture whose quote span carries markup [Q24 'the genuine package must be accepted' (indirect, as M01); the gate strips tags before the flat compare]
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

exit 0. Full text: `only-m07.txt`. The module's only fixture line is `ok`; every other `FIXTURE`
line in that run belongs to the pre-existing battery (round 36/37/38) and is also `ok`.

### E2 — reference vs mutant, clause text (not just rc)

`probe-receipt.txt`, quoted in §3: `D5 ok` / rc 0 against `D5 DEFECT …quote absent from the capture` / rc 1.
Both runs exit 0/1, which is the counter's requirement for a `mirror` kill, and the fixture
declares `defects=[]` so the declared set equals the reference's (empty) set.

### E3 — load-bearing table (fixture deleted in turn)

Command shape (twice, once per row):
`python3 plans/round39_c1_verify.py --lane "$S/lane" --battery-dir "$S/<row>" --only M07 --work "$S/wlb"`

| mutation of the battery | `BATTERY` | `M07` |
|---|---|---|
| none (module present) | `fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0` | `killed by=d5m39-tagged-quote-span` |
| fixture deleted (`FIXTURES = []` in a copy of the module) | `fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0` | `SURVIVED exhibits=none` |
| module absent (empty battery dir) | `fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0` | `SURVIVED exhibits=none` |

Rows 2-3 verbatim:

```
=== lb-fixture-deleted exit=1
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M07 D5 mirror SURVIVED exhibits=none -- a D5 quote is found in a capture whose quote span carries markup [Q24 'the genuine package must be accepted' (indirect, as M01); the gate strips tags before the flat compare]
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
=== lb-module-absent exit=1
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M07 D5 mirror SURVIVED exhibits=none -- ...
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
```

`exhibits=none` also says the fixture is not one of several redundant kills: with the module gone
M07 exhibits **no** declared direction anywhere in the remaining 86 fixtures.

### E4 — full default counter in the clone, module at `"$S/lane/plans/battery39/d5m39.py"`

```
$ python3 "$S/lane/plans/round39_c1_verify.py" --lane "$S/lane" --work "$S/wfull"
PINS total=26 mismatched=0
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M01 D5 mirror killed by=d5m-n21-manifest-row-2 -- ...
MUTANT M02 P1 silence SURVIVED exhibits=none -- ...
MUTANT M03 P3 silence SURVIVED exhibits=none -- ...
MUTANT M04 P7 silence SURVIVED exhibits=none -- ...
MUTANT M05 RUN rc-silence killed by=p23-p2-receipt-deleted -- ...
MUTANT M06 MAIN rc-mirror killed by=r36-P0 -- ...
MUTANT M07 D5 mirror killed by=d5m39-tagged-quote-span -- a D5 quote is found in a capture whose quote span carries markup [Q24 'the genuine package must be accepted' (indirect, as M01); the gate strips tags before the flat compare]
MUTANTS total=7 killed=4 survived=3 invalid=0 null_detected=0
PREDICATE C1 fail
```

exit 1 — correct and expected for this clone: M02/M03/M04 belong to sibling wave-1 seats and no
`plans/battery38`/`battery39` module in **this** clone demonstrably kills them. My module adds no
breakage: `fixtures=87 wrong=0`, `renamed_disagree=0`, `sidechannel=0`, `invalid=0`,
`null_detected=0`, and M07 is killed in the full battery too. (M01/M05/M06 are the three the
freeze already records as killed; the freeze's `control-c1-nothing.txt` printed `killed=3
survived=4`.) Full text: `full-run.txt`.

### E5 — hygiene numbers behind those lines

- `sidechannel=0` in every run; direct scan of the module source for the five tokens:
  `forbidden tokens: []` (`/proc`, `ppid`, `cmdline`, `psutil`, `environ` — the word
  "environment" is avoided in the text for this reason).
- `renamed_disagree=0`: the counter copied `d` to a renamed path and replaced `str(d)` in argv;
  both `--file` and `--capture-dir` are inside `d`, so the answers agree.
- `null_detected=0`: the same gate run twice on the fixture is byte-stable (build is
  deterministic: the two independent builds of the fixture gave capture `sha256
  7c421e71…` in both `probe/fx` and `probe/fx2`).
- The fixture's build runs in the counter's child process (`--build-module`) and hands back JSON
  only: `{"fid": "d5m39-tagged-quote-span", "expect": "accept", "defects": [], "argv": [...]}`.

## 5. Risks and limits

1. **Byte provenance of the fixture's erratum line.** The fixture keeps the genuine frozen D5 line
   (it carries the `require`/`forbid` tokens the clause reads), but that line's prose says the
   capture is 60,335 B while the fixture's capture is 60,382 B. `cmd_d5`
   (`plans/pkg_gate.py:327-356`) never reads a size, a filename inside prose or a line count, so
   the reference verdict is unaffected; the number is stated here so no reader mistakes the
   fixture for the frozen evidence file.
2. **The kill records a result difference, not intent.** Attribution rests on (a) clause family
   `d5-line`, (b) the declared `mirror` direction, (c) the build-time proof that the tag-stripped
   capture text is identical to the frozen capture's and the delta is exactly the 47 markup bytes —
   i.e. the only input difference the mutation can react to is the presence of tags inside the
   quote span. A future gate edit that stopped stripping tags would kill this fixture too (it is a
   fixture about that branch, not about the gate's identity).
3. **The counter's side-channel scan is a token heuristic** (frozen claims, C1 limits). I ran the
   scan and read the source myself; non-author review at admission is still the real check.
4. **Kill order.** The counter breaks at the first fixture that exhibits the direction, so if a
   different battery39 module also kills M07 the reported `killed by=` depends on module order
   (`sorted(bdir.glob("*.py"))`). My fixture stands alone in my dir; at landing, whichever fid is
   printed, M07 is killed — but the `killed by=` string is not stable evidence of authorship.
5. No blocker. Nothing needed installing; no `pacman` transaction attempted.

VERDICT: battery39-d5m39-M07-killed-wrong-0
