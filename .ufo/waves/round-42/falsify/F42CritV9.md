# F42CritV9 — attack on V9 of `plans/round42_c2_verify.py` (round 42, wave 2 falsify)

**Seat:** F42CritV9 (critic, leaf — no subagents). **Target:** V9, the ninth check of the round-42 C2 counter
(`plans/round42_c2_verify.py`). **Lane clone:** docs tip `508434ad55c709337065611691c426f05875492d`
(`git -C $S/lane rev-parse --short HEAD` = `508434a`), `git rev-parse --show-toplevel` verified = `$S/lane`.

## 1. Setup

- Scratch `S=/fast/scratch/hyaku/kengaku-r42/F42CritV9`; `TMPDIR=$S`; clone per seat rule; no git mutation.
- Five mirrors `ctl a b c d` under `$S`, each carrying exactly the five inputs the frozen `v9()` reads: a byte copy of
  `plans/pkg-spec-r42.json` (must match freeze digest), a byte copy of the receipt
  `corpus/evidence/round42/fibsqrt-probe.txt`, an entry at `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`,
  `PROVINCE.md` and `corpus/README.md`. Variants were built by `mk_mirrors.py`; the frozen counter
  (`round42_c2_verify.py`, imported from the clone) was called directly: `mod.v9(pathlib.Path(mirror))`.
- Every run executed inside the host-safety bwrap envelope; localbin sha256 unchanged before/after; receipt file
  `$S/v9results.txt` (1558 bytes, sha256 `2096e2cae8ee0027736cfd405c8e08f8b306bbcf980fe9c942d9ac6daad9a5eb`) quoted
  below and deleted with scratch at seat end.

```
ENVELOPE: bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 <scripts>
date-before=18:05:08
localbin-sha256-before=8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52
wrote mirrors ctl,a,b,c,d; cases=16
== frozen v9() on each mirror ==
ctl: V9 ok case_rows=16/16 bad=0
a: V9 ok case_rows=16/16 bad=0
b: V9 DEFECT case_rows=16/16 bad=['case table rows=16 receipt cases=16 equal=False']
c: V9 DEFECT case_rows=16/16 bad=['case table rows=16 receipt cases=16 equal=False']
d: V9 ok case_rows=16/16 bad=0
== drafted V9e (case ids cited in prose outside the Case table) ==
ctl: V9e ok missing=0 []
a: V9e DEFECT missing=16 ['nop', 'oracle-solve-sh', 'no-gates-file', 'empty-gates-file', 'lookup-28']
b: V9e DEFECT missing=16 ['nop', 'oracle-solve-sh', 'no-gates-file', 'empty-gates-file', 'lookup-28']
c: V9e DEFECT missing=16 ['nop', 'oracle-solve-sh', 'no-gates-file', 'empty-gates-file', 'lookup-28']
d: V9e DEFECT missing=16 ['nop', 'oracle-solve-sh', 'no-gates-file', 'empty-gates-file', 'lookup-28']
a+one-citation: V9e DEFECT missing=15 ['nop', 'oracle-solve-sh', 'no-gates-file', 'empty-gates-file', 'lookup-27-drop-48401']
== drafted V9b' (row-id check, code fences stripped) ==
ctl: V9b' ok missing=[]
a: V9b' ok missing=[]
b: V9b' ok missing=[]
c: V9b' ok missing=[]
d: V9b' DEFECT missing=['S125', 'S126', 'S127']
bwrap_exit=0
date-after=18:05:08
localbin-sha256-after=8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52
```

Control run for the draft check (same envelope, `run_v9e_ctl.py`): `a+all16-cited: V9e ok missing=0`.

## 2. The four attacks vs frozen V9

| # | mirror | perturbation vs the landed entry | frozen `v9()` |
|---|---|---|---|
| — | `ctl` | none (landed entry + landed PROVINCE.md / corpus/README.md) | `V9 ok case_rows=16/16 bad=0` |
| (a) | `a` | informed filler: receipt copied into a `## Case table` (16 rows in receipt order, correct letters/verdicts), one line `Registry rows S125 S126 S127`, minimal PROVINCE.md line naming `circuit-fibsqrt` + entry basename, README `## Frontier` naming `circuit-fibsqrt`; **no analysis anywhere** | `V9 ok case_rows=16/16 bad=0` — **passes** |
| (b) | `b` | same as (a) but one row's letters disagree with the receipt (`nop` PPF→PFF) | `V9 DEFECT … equal=False` — caught |
| (c) | `c` | same as (a) but the last two case rows are swapped (wrong order) | `V9 DEFECT … equal=False` — caught |
| (d) | `d` | same as (a) but S125–S127 appear **only inside a ```registry``` code fence** | `V9 ok case_rows=16/16 bad=0` — **passes** |

**Which pass V9: (a) and (d).** V9 catches (b) letter disagreement and (c) order; it admits a zero-analysis
receipt-transcript (a) and a fence-hidden row-id mention (d). `VERDICT: v9-admits-2/4`.

## 3. What V9 certifies, and what it cannot see

V9 (`round42_c2_verify.py:282-313`, docstring `:36-39`) is four syntactic tests:

1. **Case table triple** (`:294-302`): the entry has a `## Case table` section holding exactly the receipt's 16 rows,
   each `| \`cid\` | <letters> | <verdict> | … |` matching `CASE_ROW` (`:84`), compared as an ordered list equal to
   the receipt's `(cid, tests, observed)`. The descriptive column is `.*` — free.
2. **Row-id presence** (`:303-306`): each spec row id (S125/S126/S127) is a substring of the entry body outside lines
   starting `source:`. Fences, code and prose are equivalent to it.
3. **PROVINCE line** (`:307-309`): one line contains both `circuit-fibsqrt` and the entry basename.
4. **README Frontier name** (`:310-312`): the `## Frontier` section contains `circuit-fibsqrt`.

What it **certifies**: the receipt is transcribed into the entry's case table (16 ids, letters, verdicts, in order)
and the three landing surfaces (entry § row ids, PROVINCE, README Frontier) each carry the required name. The
numbers' authenticity rests elsewhere (V4 receipt ↔ frozen dry table; V2/P10 probe byte-equality), not in V9.

What it **cannot see** (demonstrated by the attacks): any analysis, finding, or understanding — (a) passes with zero
analysis and an H1 that still says "read and executed"; whether the table's text column is true (wave-1 `R42ConnPattern`
B3 already showed a false description passes); whether row-id mentions are integrated or fence-hidden — (d); whether
PROVINCE/README lines are substantive (a minimal "named here and nowhere else" line passes). This confirms and
measures the wave-1 gap: `R42CritClaims` filler A already passed V9 with 7/9 overall
(`R42CritClaims/lane-a-c2.txt`: `V9 ok case_rows=16/16 bad=0`), and the round's own lesson records V9 as closing only
the "shape" half of R3 (`R42LessonDraft/round-42.md`: "Filler half closed … the tier-B live-state half stays open").

## 4. Drafted V9-style check that separates (a) from the landed entry, with a control

**V9e — case-citation integration.** Every case id that appears in the `## Case table` must also appear in the entry
body **outside** that section (same section regex v9 uses; ids collected with `CASE_ROW`). Sketch:

```python
sec = re.search(r"^## Case table\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
ids = [m.group(1) for l in sec.group(1).splitlines() if (m := CASE_ROW.match(l))]
outside = entry.replace(sec.group(0), "")
missing = [c for c in ids if f"`{c}`" not in outside]
```

Results on the mirrors:

| mirror | V9e |
|---|---|
| `ctl` (landed) | `ok missing=0` — the landed entry cites all 16 cases in Summary / findings / Requirement map |
| `a` (informed filler) | `DEFECT missing=16` — separates (a) from the landed entry |
| control `a+all16-cited` | `ok missing=0` — filler (a) plus one prose line listing all 16 ids ("Cases measured (named only): …", still no analysis) |

The control is honest: V9e measures *use of the cases in prose*, not analysis quality — a mechanical all-16 citation
list defeats it. It raises the floor from "copy the table" to "name every case outside the table", which the landed
entry already exceeds; it is a cheap, V9-style tightening, not a content proof.

**Secondary fix for attack (d):** tighten V9(b) by stripping fenced blocks before the substring test (`V9b'`):
with ```…``` removed from the body, `ctl/a/b/c` keep `missing=[]` while `d` flips to `DEFECT missing=['S125','S126','S127']`.

## 5. Evidence

- Counter source: `plans/round42_c2_verify.py:36-39` (V9 docstring), `:84` (`CASE_ROW`), `:282-313` (`v9`), `:301-312` (defect paths). Read from the docs-tip clone `508434a`.
- Receipt `$S/v9results.txt`: quoted in full in §1 (sha256 `2096e2cae8ee0027736cfd405c8e08f8b306bbcf980fe9c942d9ac6daad9a5eb`; 1558 B; deleted with scratch).
- Control-run output `a+all16-cited: V9e ok missing=0` from `run_v9e_ctl.py` under the same envelope.
- No lane file was written; no write outside `$S` and this report path.

VERDICT: v9-admits-2/4
