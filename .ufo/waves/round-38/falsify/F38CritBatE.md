# F38CritBatE — attack on battery38 `p6m.py` / `p7m.py` (wave 2, falsify)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip under attack
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a`. Clone: `/fast/scratch/hyaku/kengaku-r38/F38CritBatE/lane`
(`git rev-parse --show-toplevel` = `<scratch>/lane`, HEAD = the tip above). Scratch deleted before this seat
closed. Nothing written outside `.ufo/waves/round-38/falsify/` and the scratch dir; no lane file, no lane jj/git
state touched.

Target: the four fixtures `p6m-n09-teaches-one-below-min`, `p6m-n10-url-scheme-http`,
`p7m-n11-empty-recheck`, `p7m-n12-first-row-url`, against the `adv` cells of N09/N10/N11/N12 in
`plans/round38_c1_verify.py`. Question asked: does each fixture demonstrate the behaviour its mutant names, or
does it kill incidentally (tailored declaration, a spec the gate never sees, a second clause doing the work,
side channel, name keying)?

Method: (1) reproduce the kills on a clean clone; (2) delete each fixture from the battery **in the clone** and
re-run the 4-mutant subset over the whole 86-fixture battery; (3) bypass the counter's clause-level
`attributed()` and run the reference gate and each mutant **directly** on the same built tree, reading the gate's
own `first=` sub-check message (`plans/round38_c1_verify.py:attributed` only checks clause ids, so a sibling
sub-check of the same clause could fake an attribution); (4) adversarial variants that move each fixture one
step off its own claim.

Receipts (this dir): `baseline-n09-n12.txt`, `del-n09.txt`, `del-n10.txt`, `del-n11.txt`, `del-n12.txt`,
`probe-subcheck.txt`, `probe-variants.txt`, `full-default-run.txt`.

Context (`full-default-run.txt`, the default all-22-mutant run on the same clone): `PINS total=14 mismatched=0`,
`BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, only `MUTANT N21 D5 silence SURVIVED`,
`MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0`, `PREDICATE C1 fail`, exit 1 — the landing
receipt's shape reproduces, and the four mutants in this seat are inside the 21.

## 1. Baseline — the four kills reproduce on the clone

    python3 plans/round38_c1_verify.py --lane "$S/lane" --only N09,N10,N11,N12 --work "$S/w"

`baseline-n09-n12.txt`:

    PINS total=14 mismatched=0
    BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
    MUTANT N09 P6 silence killed by=p6m-n09-teaches-one-below-min -- a teaches cell below min_teaches_words is a defect [capability row 'teaches cells carry >=8 distinct words'; F37XMutP6 X1]
    MUTANT N10 P6 silence killed by=p6m-n10-url-scheme-http -- the row URL is the pinned raw URL including its scheme [F37XMutP6 X4]
    MUTANT N11 P7 silence killed by=p7m-n11-empty-recheck -- a recheck line must carry a value [F37XMutP7 X4]
    MUTANT N12 P7 silence killed by=p7m-n12-first-row-url -- the first registry row's source line is checked too [F37XMutP7 D1]
    MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0

All four `FIXTURE` lines read `ok` with `declared=` equal to the reference's observed defect set, so the
declarations are not tailored: the counter compares `res[1] == frozenset(declared)` and the observed sets are
exactly `{P6}`, `{P6}`, `{P7}`, `{P7}`.

## 2. Deletion — each mutant survives without its own fixture, none of the other 85 fixtures kills it

Procedure per fixture: restore `plans/battery38/{p6m,p7m}.py` from a pristine copy, remove only that one
`FIXTURES` entry in the clone, re-run the same 4-mutant subset (whole battery still built and executed:
`BATTERY fixtures=85 wrong=0`), then restore the module byte-identically (sha256 of the restored clone files
equals the fleet originals: p6m `3a42982e54dd…`, p7m `5e6f943f15ec…`).

| removed fixture | N09 | N10 | N11 | N12 | receipt |
|---|---|---|---|---|---|
| `p6m-n09-teaches-one-below-min` | **SURVIVED** | killed | killed | killed | `del-n09.txt` |
| `p6m-n10-url-scheme-http` | killed | **SURVIVED** | killed | killed | `del-n10.txt` |
| `p7m-n11-empty-recheck` | killed | killed | **SURVIVED** | killed | `del-n11.txt` |
| `p7m-n12-first-row-url` | killed | killed | killed | **SURVIVED** | `del-n12.txt` |

Pasted, `del-n09.txt` (and the same shape for the other three):

    BATTERY fixtures=85 wrong=0 renamed_disagree=0 sidechannel=0
    MUTANT N09 P6 silence SURVIVED -- a teaches cell below min_teaches_words is a defect [...]
    MUTANT N10 P6 silence killed by=p6m-n10-url-scheme-http -- ...
    MUTANT N11 P7 silence killed by=p7m-n11-empty-recheck -- ...
    MUTANT N12 P7 silence killed by=p7m-n12-first-row-url -- ...
    MUTANTS total=4 killed=3 survived=1 invalid=0 null_detected=0

`del-n10.txt`: `MUTANT N10 P6 silence SURVIVED`, N09/N11/N12 killed, `killed=3 survived=1`.
`del-n11.txt`: `MUTANT N11 P7 silence SURVIVED`, N09/N10/N12 killed, `killed=3 survived=1`.
`del-n12.txt`: `MUTANT N12 P7 silence SURVIVED`, N09/N10/N11 killed, `killed=3 survived=1`.

So each kill is necessary to its own fixture (no duplicate killer anywhere in r36 + battery37 + all twelve
battery38 modules) and sufficient (nothing else in the battery changes the verdict).

## 3. Sub-check attribution — the gate's own message, not just the clause id

Built each fixture tree with the module's own builder, then ran a byte copy of `plans/pkg_gate.py` and the
mutant on the *same* tree (`probe-subcheck.txt`).

*A1 `p6m-n09-teaches-one-below-min`* — reference rejects on the teaches count, N09 flips exactly that line:

    [ref] rc=1
      P6 DEFECT rows=3 bad=1 first=S105: teaches words=7
      P7 ok ... P8 ok ... P9 ok
    [N09] rc=0
      P6 ok rows=3 bad=0 first=0
    S105 cells after edit: [..., 'n09 t…']   # 7 words; 11 cells still parse, tier/status/URL/used-by untouched

*A2 `p6m-n10-url-scheme-http`*:

    [ref] rc=1
      P6 DEFECT rows=3 bad=1 first=S105: url not the pinned raw path
    [N10] rc=0
      P6 ok rows=3 bad=0 first=0
    S105 cells after edit: [... ' — http://raw.githubusercontent.com/.../tests/test_outputs.py', ...]

*A3 `p7m-n11-empty-recheck`*:

    [ref] rc=1
      P7 DEFECT source_lines=3 bad=1 first=recheck line absent
    [N11] rc=0
      P7 ok source_lines=3 bad=0 first=0
    last 3 entry lines: [..., '  partial or confounded, ...', 'recheck:']

*A4 `p7m-n12-first-row-url`*:

    [ref] rc=1
      P7 DEFECT source_lines=3 bad=1 first=S105: source line not the pinned url
    [N12] rc=0
      P7 ok source_lines=3 bad=0 first=0
    entry line 1: source: S105 — https://raw.githubusercontent.com/.../venue…/protein-assembly/tests/test_outputs.py

Each mutant's flip is on the sub-check the fixture edited, so the clause-level `attributed()` is not hiding a
sibling sub-check doing the work: `c_sources` has six sub-checks (`plans/pkg_gate.py:196-205`) and the fixtures
trip exactly the teaches one and the url one; `c_provenance` has five (`:220-229`) and these fixtures trip
exactly the per-row source check and the recheck check.

## 4. Adversarial variants — is the load-bearing token the one the `adv` names?

*N09 threshold is exactly `min-1`, not "any short cell"* — teaches cell at `min-2` (6 words) is still a defect
under the mutant, so the fixture sits precisely on the mutated predicate (`probe-subcheck.txt` §C):

    teaches words: 6
    [ref] P6 DEFECT rows=3 bad=1 first=S105: teaches words=6
    [N09] P6 DEFECT rows=3 bad=1 first=S105: teaches words=6

*N09's credited capability text includes "distinct"; the gate never checks within-cell distinctness*
(`probe-subcheck.txt` §D) — teaches cell of eight identical words:

    teaches cell: 'word word word word word word word word' distinct: 1
    [ref (frozen gate)] rc=0
      P6 ok rows=3 bad=0 first=0

*N10: the scheme is load-bearing, not "any URL edit"* (`probe-variants.txt` §E) — path changed, scheme kept
`https`; N10 still rejects:

    [ref]   P6 DEFECT rows=3 bad=1 first=S105: url not the pinned raw path
    [N10]   P6 DEFECT rows=3 bad=1 first=S105: url not the pinned raw path

*N12: the first row is load-bearing* (`probe-variants.txt` §F) — S106's entry source defaced instead of S105;
N12 still rejects, so battery37's second-row fixture cannot cover N12:

    [ref] P7 DEFECT source_lines=3 bad=1 first=S106: source line not the pinned url
    [N12] P7 DEFECT source_lines=3 bad=1 first=S106: source line not the pinned url

Row order: `spec rows dict order: ['S105', 'S106', 'S107'] -> N12 skips: ['S106', 'S107']`; `_target_row`'s
`sorted()[0]` is also `S105`. Both orderings coincide at this pin, and `plans/pkg-spec-r35.json` is one of the
14 pinned inputs (`PINS total=14 mismatched=0`), so the order dependence of `list(rows)[1:]` is digest-protected.

*N11: the advertised rule is not what the frozen gate enforces.* Empty `recheck:` left **in place** (line 5),
two later non-blank lines, and again with only one blank line appended at EOF (`probe-subcheck.txt` §B,
`probe-variants.txt` §G):

    == B ==
    [ref (frozen gate)] rc=0
      P6 ok ... P7 ok source_lines=3 bad=0 first=0 ... P9 ok
    [N11] rc=0
      P7 ok source_lines=3 bad=0 first=0
    == G ==
    [ref] rc=0   P7 ok source_lines=3 bad=0 first=0

This is the defect in §5 D1: an empty `recheck:` is a defect only when no later non-blank line follows, because
`^recheck:\s*\S` with `re.M` lets `\s*` cross the newline (`plans/pkg_gate.py:224`). The fixture must therefore
relocate the line to EOF (`p7m.py:36-51`) to get any reference defect at all; the module docstring says so.

## 5. Findings

**D1 (medium, fixture/`adv` pairing; unfixable in the battery).** N11's `adv` is "a recheck line must carry a
value", but the frozen gate accepts an empty recheck line whenever any later non-blank line exists (§4 B/G:
`P7 ok`, rc=0). `p7m-n11-empty-recheck` demonstrates only the EOF special case, i.e. the *position* of the line
is co-load-bearing with the missing value. The kill is still attributable and necessary (§2, §3 A3), and the
tailoring is disclosed in the module docstring, but the advertised sentence overstates the reference: no fixture
can demonstrate "a recheck line must carry a value" in general against this gate. Smallest correction: reword
the N11 `adv` cell to the observed behaviour ("an empty trailing recheck line is a defect") and keep the mutant;
record the mid-file blind spot in the C1 limits (it is a gate false-green, not a battery gap).

**D2 (low, provenance of the bracket quote).** N09's `adv` credits the capability row text "teaches cells carry
>=8 distinct words" (`SCORECARD.md:564`), but `c_sources` checks `len(cells[6].split())` only
(`plans/pkg_gate.py:204`); eight identical words are accepted (§4 D, `P6 ok`, rc=0). The fixture demonstrates the
count clause exactly (A1: `first=S105: teaches words=7`); the "distinct" half of the credited behaviour is
unenforced by the gate and therefore undemonstrated by any battery fixture. Smallest correction: drop "distinct"
from the bracket or add it to the C1 limits as an advertised-but-unenforced property (it is not a mutant the
list carries, and N09's sentence itself is fine).

No kill failure, no tailored declaration, no forbidden `--spec`, no side channel found (§6). Everything else the
task asked to attack came back clean.

## 6. Side channels, name keying, spec escape — negative results

    grep -nE "os\.|getenv|environ|sys\.argv|subprocess|time\.|ppid|/proc|psutil|open\(|read_text|__file__|import " plans/battery38/p6m.py plans/battery38/p7m.py
    p6m.py:21:import re
    p6m.py:36:    for line in path.read_text().splitlines()     # the fixture tree under build
    p6m.py:49:    for line in (d / SOURCES).read_text().splitlines()
    p7m.py:27:    before = entry.read_text()                      # the fixture tree under build

No `os`, no `environ`/`getenv`, no `sys.argv`, no subprocess, no timing, no `/proc`; the only reads are the
tree each builder is handed. Neither module mentions its own `fid`, and the counter's independent copy-rename
pass agrees (`renamed_disagree=0` in every run above). Neither module appends `--spec`: the argv is
`["package", "--root", <d>, "--require-clean-tree"]`, so both inherit the pinned `plans/pkg-spec-r35.json`
rather than a fixture-owned spec (the b38 `--spec`-inside-`d` escape that `round38_c1_verify.py:main` permits is
not used here). `sidechannel=0` for every run.

## 7. What I did not attack

- Mutants other than N09–N12 (other seats), and the N21 mirror explanation.
- Whether `c_sources`' `URL.search` would accept a cell carrying the pinned URL plus an extra URL (an
  over-acceptance hole of the gate, not of these fixtures).
- `PINS`/`P11`-style harness ground truth beyond reading `attributed()` and re-running the gate directly.

VERDICT: battery-p6m-p7m-attack-2-defects
