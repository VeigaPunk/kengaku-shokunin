# R33FN2Fence — N2 heading recognition inside a code fence

Seat: KengakuR33.R33FN2Fence (mutation tester, round-33 falsify wave, hyaku run 7)
Date: 2026-10-25
Target: `check_n2` in `plans/round33_defects.py` (lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`)
Frozen claim (plans/round-33-claims.md, C2 predicate, line 89):
> N2 `SCORECARD.md` contains a `## Round 32` section recording round 32's dispositions

## Mutant / attack

Fresh sandbox `/tmp/r33fn2fence/` with two lane-shaped fixtures, each a
`SCORECARD.md` in its own directory (`laneA`, `laneB`).

- `laneA` (negative control): no `## Round 32` token anywhere.
- `laneB` (attack): `## Round 32` appears **only** inside a fenced code block;
  no real heading, no dispositions. Exact bytes (cat -A):

~~~
# Scorecard$
$
A round-32 section template was drafted but never filled in:$
$
```markdown$
## Round 32$
```$
$
No real heading, no dispositions recorded.$
~~~

The detector was not modified; the attack is the input fixture.

## Expected detector behavior

`check_n2` (verbatim from `plans/round33_defects.py:91-96`):

```python
def check_n2(lane: Path) -> str:
    path = lane / SCORECARD
    if not path.is_file():
        return f"{SCORECARD} is unreadable"
    if not re.search(r"^## Round 32\b", read(path), re.MULTILINE):
        return "SCORECARD.md carries no '## Round 32' section: round 32's dispositions are unrecorded"
    return ""
```

Frozen claim requires a *section recording dispositions*. A fenced mention is
neither a heading nor a disposition, so the expected result on `laneB` is the
defect string (red). The `re.MULTILINE` `^` anchor is the plausible defect: it
matches any line start, including lines inside markdown fences.

## Actual output

`python3 /tmp/r33fn2fence/probe.py` (imports the sandbox copy of the lane
script and calls `check_n2` read-only), verbatim:

```
== laneA ==
sha256 before: 96c0d130891933553c2e7f93610f5ef376211463b0c46950f05ebcac86f7cef2
check_n2 -> "SCORECARD.md carries no '## Round 32' section: round 32's dispositions are unrecorded"  => REDS
line-anchored regex: no match
sha256 after:  96c0d130891933553c2e7f93610f5ef376211463b0c46950f05ebcac86f7cef2
bytes unchanged by detector run: True
== laneB ==
sha256 before: 749255f4eae1cdeb06bd086158a16d32fd5cf885750ccf8750d5ae1aae45dff8
check_n2 -> ''  => GREENS (empty string)
line-anchored regex matched at line 6: '## Round 32'
sha256 after:  749255f4eae1cdeb06bd086158a16d32fd5cf885750ccf8750d5ae1aae45dff8
bytes unchanged by detector run: True
```

## Verdict: uncaught (surviving mutant — false green)

- Baseline: `laneA` reds with the exact defect string, so the detector is
  functional and the `laneB` green is a genuine false positive, not an
  inconclusive baseline.
- Attack: on `laneB` the regex matches line 6, inside the ```` ```markdown ````
  fence, and `check_n2` returns `''` — the check greens although no `## Round 32`
  section or disposition exists.
- Coverage finding: `check_n2`'s line-anchored regex cannot distinguish a real
  section heading from any fenced or quoted `## Round 32` line (template, diff,
  shell transcript). Per the mutation-tester contract this is recorded as a
  coverage finding; the claim contract itself is not challenged.

## Restoration / contamination evidence

- Lane script was never run or written in place; it was copied to the sandbox.
  `sha256sum` both: `6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6`
  (identical — provenance of the code under test).
- Detector run is read-only on fixtures: fixture sha256 identical before/after
  (laneA `96c0d130…`, laneB `749255f4…`, see probe output above).
- All artifacts live under `/tmp/r33fn2fence/`; no lane/fleet file mutated,
  staged, or committed; no git commands executed (none required — fixture-only
  attack); no tools installed.

## Commands executed

```
rm -rf /tmp/r33fn2fence && mkdir -p /tmp/r33fn2fence/laneA /tmp/r33fn2fence/laneB \
  && cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round33_defects.py \
        /tmp/r33fn2fence/round33_defects.py \
  && sha256sum <lane script> /tmp/r33fn2fence/round33_defects.py
python3 /tmp/r33fn2fence/probe.py && echo '--- laneB bytes ---' && cat -A /tmp/r33fn2fence/laneB/SCORECARD.md
```

Sandbox retained at `/tmp/r33fn2fence/` for re-verification.
