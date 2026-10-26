# F37XMutP7 — extra mutants of gate clause P7 (kengaku r37, wave 2 falsify, 2026-10-26)

Seat: F37XMutP7 (critic, leaf). Target: `plans/battery37/p7.py` (six fixtures) and the P7 clause of
`plans/pkg_gate.py`, beyond the frozen mutants M28–M33. All work on my own clone of the assigned tip;
no lane file written, no lane git/jj command run, no counter run on the lane.

## Setup

```
$ S=/fast/scratch/hyaku/kengaku-r37/F37XMutP7; export TMPDIR="$S"
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/fx/lane"
$ git -C "$S/fx/lane" checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
$ git -C "$S/fx/lane" rev-parse --show-toplevel; git -C "$S/fx/lane" rev-parse HEAD
/fast/scratch/hyaku/kengaku-r37/F37XMutP7/fx/lane
357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
$ sha256sum "$S/fx/lane/plans/pkg_gate.py"
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  .../plans/pkg_gate.py
```

Top-level verified before any write; gate byte-equal to the freeze digest the counter pins
(`GATE_SHA256` in `plans/round37_c1_verify.py:56`), and the counter's own print confirms
`GATE sha256=… frozen=True`.

Harness: `.ufo/waves/round-37/falsify/F37XMutP7/mutate_p7.py` (in this directory). It does not
re-implement the counter: it imports `plans/round37_c1_verify.py` as a module from the clone and calls
`load_r36`, `Ctx`, `r36_fixtures`, `battery37_fixtures`; fixtures are built **once** into
`$S/run/fx`, the reference is a copy of the frozen gate, and each mutant is one exact
`old -> new` replacement (asserted `count(old)==1`, then `py_compile`). Observable = (exit code, set
of clause ids printed `DEFECT`), identical to the counter's `run_gate`.

```
$ TMPDIR=$S python3 .ufo/waves/round-37/falsify/F37XMutP7/mutate_p7.py \
      --lane "$S/fx/lane" --work "$S/run"
GATE sha256=ea63882240e6…4d41 frozen=True
BATTERY fixtures=64 r36=14
REFERENCE wrong=0
```

64 fixtures, every battery37 declaration matched the unmodified gate on its tree (`wrong=0`), so the
battery is healthy and the comparisons below are not carried by a pre-existing disagreement.
Receipts: `F37XMutP7/p7-mutate.txt` (full output), `F37XMutP7/gates.sha` (mutant digests:
X1 `65497577…`, X2 `197503a0…`, X3 `e8a467a2…`, X4 `d481ed77…`, ref `ea638822…`).

## 1. Four new (non-frozen) P7 mutants

Each pair occurs exactly once in `plans/pkg_gate.py`; none is one of M28–M33.

**X1 — check applied to the first row only** (source-line loop narrowed to `rows[:1]`, i.e. S105)

```
OLD:    for sid, row in p.spec["rows"].items():
            if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:
NEW:    for sid, row in list(p.spec["rows"].items())[:1]:
            if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:
```

**X2 — threshold removed** (`verified-at` compared to any ISO date, not the frozen date)

```
OLD:    if f"verified-at: {rules['verified_at']}" not in p.entry:
NEW:    if not re.search(r"^verified-at: \d{4}-\d{2}-\d{2}", p.entry, re.M):
```

**X3 — branch reordered so another check shadows it** (recheck presence now only checked when the
`## Negative space` heading is absent)

```
OLD:    if not re.search(r"^recheck:\s*\S", p.entry, re.M):
            bad.append("recheck line absent")
NEW:    if not re.search(r"^## Negative space", p.entry, re.M) and not re.search(r"^recheck:\s*\S", p.entry, re.M):
            bad.append("recheck line absent")
```

**X4 — regex loosened** (a bare `recheck:` line accepted; `\s*\S` requirement dropped)

```
OLD:    if not re.search(r"^recheck:\s*\S", p.entry, re.M):
NEW:    if not re.search(r"^recheck:", p.entry, re.M):
```

### Result

| mutant | category | verdict | killing fixture | observed delta (ref → mutant) |
|---|---|---|---|---|
| X1 | first row only | **killed** | `p7-m29-source-url` | rc 1, P7 → rc 0, no DEFECT |
| X2 | threshold removed | **killed** | `p7-m30-verified-at` | rc 1, P7 → rc 0, no DEFECT |
| X3 | branch reordered/shadowed | **killed** | `p7-m31-recheck-line` | rc 1, P7 → rc 0, no DEFECT |
| X4 | regex loosened | **SURVIVED** | — | none on all 64 fixtures |

Counter output (`p7-mutate.txt`):

```
DELTA X1 on p7-m29-source-url ref=(rc=1,defects=P7) mutant=(rc=0,defects=-)
MUTANT X1 killed by=p7-m29-source-url
DELTA X2 on p7-m30-verified-at ref=(rc=1,defects=P7) mutant=(rc=0,defects=-)
MUTANT X2 killed by=p7-m30-verified-at
DELTA X3 on p7-m31-recheck-line ref=(rc=1,defects=P7) mutant=(rc=0,defects=-)
MUTANT X3 killed by=p7-m31-recheck-line
MUTANT X4 SURVIVED by=-
EXTRA total=4 killed=3 survived=1
```

### X1's kill is narrower than it looks

X1 checks only the **first** registry row (S105), yet it is killed by `p7-m29`, whose defect is on the
**second** row (S106). So the kill proves the battery breaks S106, not that it covers S105/S107. A
supplementary diagnostic (not one of the four) restricted the loop to `[1:2]` — **S106 only**:

```
DIAG D1 SURVIVED by=- -- source line: second registry row only (S106)
WITNESS s105-source-url-changed ref_rc=1 ref_defects=P7 ref_p7='DEFECT source_lines=3 bad=1 first=S105: source line not the pinned url'
        | D1_rc=0 D1_defects=- D1_p7='ok source_lines=3 bad=0 first=0'
```

The witness (genuine package, S105's URL path changed once, index staged) is rejected by the reference
gate on P7 and accepted by the S106-only mutant. No fixture in `p7.py` edits the S105 or S107
`source:` line (`plans/battery37/p7.py:23` names S106 only; m28 deletes the whole entry, reported as
`entry unreadable`; `p6.py` edits `corpus/SOURCES.md`, not the entry's `source:` lines). Battery limit: the P7 source-line branch is demonstrated on **one of three
registry rows**.

## 2. X4 survivor: a battery gap that is also a gate defect

X4 relaxes the recheck regex to `^recheck:`; the reference demands a non-space token after it. X4
survives because the frozen battery contains no tree with an empty recheck instruction.

Two witnesses fix the exact size of the gap:

**(a) The unmodified gate already accepts an emptied recheck line.** Genuine package, recheck
instruction text removed (`recheck:` alone, line 5), index staged:

```
WITNESS empty-recheck-line ref_rc=0 ref_defects=- ref_p7='ok source_lines=3 bad=0 first=0'
        | X4_rc=0 X4_defects=- X4_p7='ok source_lines=3 bad=0 first=0'
```

The exit code is 0 on a tree whose recheck clause carries no instruction. Cause, measured on that
tree:

```
$ python3 -c 'import re,pathlib; t=pathlib.Path("…/entry.md").read_text(); m=re.search(r"^recheck:\s*\S", t, re.M); print(repr(t[m.start():m.end()+10]))'
'recheck:\n\n# Terminal-'
```

`\s*` in `pkg_gate.py:224` crosses the newline, so the next heading's `#` satisfies `\S`. The clause
"recheck line absent" therefore detects only absence of the literal string `recheck:`. This is a
finding against the landing's advertised P7 branch, not only against the battery; `p7-m31` (line
removed) is consistent with it and cannot expose it.

**(b) X4 is killable — the missing fixture shape exists.** Same package, recheck line moved to the
last line with its instruction emptied:

```
WITNESS recheck-last-line-empty ref_rc=1 ref_defects=P7 ref_p7='DEFECT source_lines=3 bad=1 first=recheck line absent'
        | X4_rc=0 X4_defects=- X4_p7='ok source_lines=3 bad=0 first=0'
```

Reference rejects on P7 alone, X4 accepts. A `p7.py` fixture built that way (expect `reject`,
defects `["P7"]`) would kill X4. Reported only; not applied, and not folded into the frozen claim.

## 3. Does each `p7.py` fixture isolate one defect?

Yes at the P7-branch level, and yes for the declared clause sets; one cross-clause exception is
disclosed by the module's own docstring.

| fixture | bytes edited | declared | observed (reference) | P7 note |
|---|---|---|---|---|
| p7-m28-entry-deleted | entry file unlinked | P3,P4,P7,P8 | rc 1, P3,P4,P7,P8 | `DEFECT entry unreadable` |
| p7-m29-source-url | one 47-char token in the S106 line (path inside the URL) | P7 | rc 1, P7 | `DEFECT source_lines=3 bad=1 first=S106: source line not the pinned url` |
| p7-m30-verified-at | one date (`…-25` → `…-24`) | P7 | rc 1, P7 | `… bad=1 first=verified-at line absent or not the frozen date` |
| p7-m31-recheck-line | one whole line dropped | P7 | rc 1, P7 | `… bad=1 first=recheck line absent` |
| p7-m32-negative-heading | one heading line dropped | P7 | rc 1, P7 | `… bad=1 first=no '## Negative space' section` |
| p7-m33-falsifier-word | one phrase (`Falsifier`→`Check`, `falsified`→`contradicted`) | P7 | rc 1, P7 | `… bad=1 first='## Negative space' carries no falsifier` |

`bad=1` on every branch means exactly one P7 item fires; the `elif` on the falsifier keeps m32 from
double-firing, and m31/m32/m33 declare only P7, so those three are single-clause too. m28 is the only
fixture that fires other clauses (P3, P4, P8 — the entry is gone), which its docstring states
(`plans/battery37/p7.py:17-20`), and its declared set matched the reference exactly. So the
"one defect" claim holds per P7 branch for all six; the cross-clause claim is true only for five.

## 4. Impacted axes and the smallest safe correction

- Axes: **C1 calibration** (what the frozen battery actually demonstrates for P7) and **gate P7
  strength** (what the clause actually enforces). Neither invalidates the frozen predicate as stated:
  my mutants are outside M01–M55, and no lane byte was touched.
- Smallest safe corrections, reported not applied (lane is frozen; edits here would move the pinned
  digest): add two `p7.py` fixtures — a `recheck:`-last-line-empty entry (kills X4, and would have
  exposed the `\s*` cross-line acceptance) and an S105 source-URL change (covers the rows the current
  battery never breaks). A gate-side fix (`[ \t]*` instead of `\s*` in the recheck regex) is a new
  freeze, not a repair of this one.

## 5. Hygiene

- Lane: only reads; `git status --porcelain` shows the pre-existing `.ufo/waves/round-37/falsify/`
  tree and `falsify.ready.dispatched`, nothing else; lane `HEAD=dc90676`, `plans/pkg_gate.py`
  `ea638822…`.
- Scratch `/fast/scratch/hyaku/kengaku-r37/F37XMutP7` removed after copying
  `p7-mutate.txt`/`gates.sha` here; nothing under `/tmp`, nothing copied from `corpus/` or `plans/`.
- Tooling: nothing installed or upgraded; no pacman transaction attempted.

VERDICT: extra-mutants-p7-killed-3/4
