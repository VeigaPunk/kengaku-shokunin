# R33FN2Meaning — N2 ("...recording round 32's dispositions") is satisfied by a bare heading

## Scope and result

Attacked item: C2 / N2, frozen text "`SCORECARD.md` contains a `## Round 32`
section recording round 32's dispositions" (`plans/round-33-claims.md:89`; the
module's own frozen description at `plans/round33_defects.py:14-16` names what the
section must record: "C1 refused, C2 incomplete, C3 failed as declared; scores
unchanged"). Implemented as `check_n2` at `plans/round33_defects.py:91-97`:

```python
def check_n2(lane: Path) -> str:
    path = lane / SCORECARD
    if not path.is_file():
        return f"{SCORECARD} is unreadable"
    if not re.search(r"^## Round 32\b", read(path), re.MULTILINE):
        return "SCORECARD.md carries no '## Round 32' section: round 32's dispositions are unrecorded"
    return ""
```

The counter's entire semantic is: *a line starting with `## Round 32` exists*. It
never reads anything under the heading. The frozen predicate is stronger: the
section must **record round 32's dispositions**. That is a predicate-versus-counter
mismatch.

All work happened in a fresh `/tmp` sandbox (`/tmp/r33fn2_sb`); the lane tree,
index, JJ state and fleet repo were never read-modified, mutated or invoked. Only
`check_n2` was exercised in isolation (running `main()` wholesale would additionally
touch fleet-report paths for N3/N4, which is out of scope for this seat).

**VERDICT: limitation / false-negative.** `check_n2` returns `''` (green) on a
`SCORECARD.md` whose only content is a bare `## Round 32` heading with zero recorded
dispositions. A pre-repair tree carrying merely the heading — dispositions absent —
would satisfy N2 and count as repaired, so the claim's substance is not enforced.

## Reproduction

Fixture: a `SCORECARD.md` containing only `# Scorecard` and the naked heading,
nothing else:

```text
$ rm -rf /tmp/r33fn2_sb && mkdir -p /tmp/r33fn2_sb/lane
$ cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round33_defects.py /tmp/r33fn2_sb/
$ cat /tmp/r33fn2_sb/lane/SCORECARD.md
# Scorecard

## Round 32
```

Probe (imports the lane's module read-only, calls `check_n2` on the fixture):

```text
$ python3 /tmp/r33fn2_sb/driver.py
=== FIXTURE (lane/SCORECARD.md) ===
'# Scorecard\n\n## Round 32\n'
=== check_n2 result ===
check_n2(lane) -> ''
OBSERVED: PASS (empty string, no defect)
=== regex probe ===
re.search(r'^## Round 32\b', text, re.MULTILINE) -> <re.Match object; span=(13, 24), match='## Round 32'>
=== negative control: same lane without any '## Round 32' heading ===
check_n2(no_round32_heading) -> "SCORECARD.md carries no '## Round 32' section: round 32's dispositions are unrecorded"
```

So the check does fire when the heading is absent — proving its *only* discriminator
is the heading line, not disposition content.

The module's own selftest corroborates the weaker semantics: the green fixture for
N2 is `"# Scorecard\n\n## Round 32 — record\n"` (`round33_defects.py:215`) — a
heading plus the token "record", still with no dispositions named (no C1 refused /
C2 incomplete / C3 failed / scores). `N2-green-section` passes on it.

```text
$ python3 /tmp/r33fn2_sb/round33_defects.py --selftest
...
CASE N2-red-on-empty PASS
CASE N2-green-section PASS
...
SELFTEST checks=14 failed=0
```

## Calibration

- Not caught: the "section present but dispositions absent" defect class. The
  counter cannot distinguish a naked `## Round 32` heading from a section that
  actually records the dispositions the claim names.
- Not a false alarm: the check correctly reddens a file with no `## Round 32`
  heading (negative control above).
- Severity: medium. The syntactic half of the claim is enforced; the semantic half
  ("recording round 32's dispositions") is untested, so `checks=6 defects=0` is
  reachable on a tree that violates N2's frozen predicate.
- Limitation: only `check_n2` was exercised (per-seat scope); N3/N4's fleet-report
  constants were not touched. No tools installed; nothing outside `/tmp` was
  written except this report artifact.
