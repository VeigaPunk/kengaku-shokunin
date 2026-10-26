# R38BatP4b — battery38 module `p4b` (C1 mutants N05, N06)

Seat: executor, round 38 wave 1. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(clone of tip `fc1174f52b150999bef91f2e81da78732ca0eb9f` under `/fast/scratch/hyaku/kengaku-r38/R38BatP4b/lane`).
Scratch was `/fast/scratch/hyaku/kengaku-r38/R38BatP4b` (NVMe, deleted at the end; receipts copied here first).
No lane file was written; the frozen claims, gate, counters, probe, specs, dry table and captures are untouched
(the counter's own `PINS total=14 mismatched=0` line below is the check).

## 1. Deliverable

One module, stdlib-only (no imports at all), fids both prefixed `p4b-`:

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatP4b/battery/p4b.py`
(74 lines, sha256 `31d591f6a790ab8d429750791de50f88964a608f2504e8d1fb0e849ba2edd332`)

L1 integrates by copying this single file to `plans/battery38/p4b.py` (battery38 seat dirs hold one module each;
no other seat prefix collides — every fid here is `p4b-*`).

Both fixtures start from the genuine round-35 package through `ctx.genuine_package(d)`, rewrite only the data
rows of the entry's `## Located quotes` table through `ctx.r36.rewrite_quotes`, stage the tree index-only through
`ctx.git_add(d)`, and return `package --root <d> --require-clean-tree` (no `--spec`: they carry no spec of their
own, so the counter appends the frozen r35 spec). Declared `defects` is `["P4"]` for both — exactly what the
unmodified gate prints.

- `p4b-case-only` → **N05** (<code>plans/round38_c1_verify.py:102</code>, `P4`/`silence`): the first quote row's
  text is replaced by itself with one ASCII letter's case flipped (`gblock_path` → `Gblock_path`), cite unchanged
  (`test_outputs.py:13`). Row still parses, word count and the distinct-text/distinct-location counts are
  unchanged, so P3 stays `ok`; the cite is inside the capture and the capture is pinned, so P4 is the only
  defect. The mutant's `q.text.lower() not in …​.lower()` finds the quote and prints P4 `ok`.
- `p4b-range-end-past-last` → **N06** (<code>plans/round38_c1_verify.py:105</code>, `P4`/`silence`): the first
  quote row is re-pointed at `instruction.md:<N>-<N+1>`, where N is that capture's last line (34) and the quote
  text is line N verbatim (`acceptor - molecule binder.`, 4 words). N is computed from the bytes copied into the
  fixture, not hard-coded. The reference takes the `q.end > len(lines)` arm
  (<code>plans/pkg_gate.py:146-147</code>); the mutant's `len(lines) + 1` lets it through and then finds the text
  on line N.

## 2. Development run (both fixtures, both mutants) — pasted in full

Command (from `/fast/scratch/hyaku/kengaku-r38/R38BatP4b`, `TMPDIR=$PWD`, `w_main/` pre-created):

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round38_c1_verify.py \
  --lane "$PWD/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatP4b/battery \
  --only N05,N06 --work "$PWD/w_main"
```

Output (exit 0; full log kept as `R38BatP4b/receipt-dev-run.txt`; the 64 round-36/battery37 `FIXTURE` lines
preceding the two below are omitted here only, they are all `ok` and are in the receipt):

```
PINS total=14 mismatched=0
FIXTURE p4b-case-only expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p4b-range-end-past-last expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N05 P4 silence killed by=p4b-case-only -- verbatim is case-sensitive [docstring 'a quote not verbatim'; F37XMutP4 X5]
MUTANT N06 P4 silence killed by=p4b-range-end-past-last -- a cited range past the capture's last line is a defect [F37XMutP4 X6]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`wrong=0` (each declared defect set equals the unmodified gate's DEFECT set exactly), `renamed_disagree=0`,
`sidechannel=0`, `null_detected=0`, `invalid=0`.

## 3. Attribution, mechanism level (reference vs each mutant on each fixture)

Driver `attr.py` (scratch; loaded `Ctx` from the frozen `plans/round37_c1_verify.py`, built each fixture into its
own dir, ran the untouched gate plus a fresh copy carrying only N05's and only N06's `old -> new`; the spec was
the frozen `plans/pkg-spec-r35.json`):

```
== p4b-case-only argv=package --root attrw/p4b-case-only --require-clean-tree
   ref rc=1 | P4 DEFECT checked=22 bad=1 first=test_outputs.py:13: quote not verbatim there
   N05 rc=0 | P4 ok checked=22 bad=0 first=0
   N06 rc=1 | P4 DEFECT checked=22 bad=1 first=test_outputs.py:13: quote not verbatim there
== p4b-range-end-past-last argv=package --root attrw/p4b-range-end-past-last --require-clean-tree
   ref rc=1 | P4 DEFECT checked=22 bad=1 first=instruction.md:34-35: line range outside the capture
   N05 rc=1 | P4 DEFECT checked=22 bad=1 first=instruction.md:34-35: line range outside the capture
   N06 rc=0 | P4 ok checked=22 bad=0 first=0
```

Each fixture moves only its own mutant (`ref DEFECT → mutant ok`, `P4 bad` 1 → 0), and each leaves the other
mutant red — so neither kill is borrowed from a clause side effect.

## 4. Load-bearing table (each fixture deleted in turn)

Three ablated copies of the module in scratch (one row removed from `FIXTURES`, byte-identical otherwise), same
counter command with `--battery-dir` pointed at each:

| battery dir | module rows | FIXTURE lines of p4b | N05 | N06 |
|---|---|---|---|---|
| `v_nocase` (case fixture deleted) | 1 | `p4b-range-end-past-last … ok` | **SURVIVED** | killed by=p4b-range-end-past-last |
| `v_norange` (range fixture deleted) | 1 | `p4b-case-only … ok` | killed by=p4b-case-only | **SURVIVED** |
| `v_none` (both deleted) | 0 | — | **SURVIVED** | **SURVIVED** |

Raw lines:

```
=== v_nocase
FIXTURE p4b-range-end-past-last expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N05 P4 silence SURVIVED -- verbatim is case-sensitive [docstring 'a quote not verbatim'; F37XMutP4 X5]
MUTANT N06 P4 silence killed by=p4b-range-end-past-last -- a cited range past the capture's last line is a defect [F37XMutP4 X6]
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
=== v_norange
FIXTURE p4b-case-only expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N05 P4 silence killed by=p4b-case-only -- verbatim is case-sensitive [docstring 'a quote not verbatim'; F37XMutP4 X5]
MUTANT N06 P4 silence SURVIVED -- a cited range past the capture's last line is a defect [F37XMutP4 X6]
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
=== v_none
BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N05 P4 silence SURVIVED -- verbatim is case-sensitive [docstring 'a quote not verbatim'; F37XMutP4 X5]
MUTANT N06 P4 silence SURVIVED -- a cited range past the capture's last line is a defect [F37XMutP4 X6]
MUTANTS total=2 killed=0 survived=2 invalid=0 null_detected=0
```

`v_none` also re-measures the do-nothing control for these two ids (0/2 killed), consistent with
`.ufo/waves/round-38/claims/control-c1-nothing.txt` (0/22 at freeze).

## 5. Scope / risks

- Two fixtures only; `defects` both `["P4"]`. Neither needs a `--spec`, so neither perturbs the counter's spec
  handling. Module source contains none of the counter's side-channel tokens (counter: `sidechannel=0`); I also
  wrote it with no `import` lines at all.
- Fixture text is derived from bytes copied into the fixture dir at build time (the flipped letter from the
  parsed row, N from `len(capture.splitlines())`), so a rename of the tree cannot change the verdict
  (`renamed_disagree=0` observed).
- `p4b-range-end-past-last` replaces the *first* data row, so its `P4 bad=1` note names the new location; if the
  genuine entry's first quote row were ever re-pointed at another capture, the builder still computes N from
  `instruction.md` in the copied tree — independent of the row it replaces.
- Not run (out of scope for this seat, parent owns the gate): `plans/battery38` did not exist in the lane, so I
  could not exercise the default `--battery-dir` path; integration is a plain file copy plus the parent's
  `python3 plans/round38_c1_verify.py --lane .` on a clean clone.
- No tool was installed or upgraded.

VERDICT: battery38-p4b-killed-2/2-wrong-0
