# R38MutProbe — mutation test of the frozen C2 probe's sensitivity (round 38, wave 1)

Seat: R38MutProbe (mutation-tester, leaf). Date: 2026-10-26.
Target: `plans/build_pmars_probe.py` (frozen digest `32f0771c…`), never edited in the lane — five mutants were
cut into scratch copies at `/fast/scratch/hyaku/kengaku-r38/R38MutProbe/mut/M{1..5}.py` and run against a
pristine `--shared` clone of the lane. No tooling was installed; `bwrap`/`gcc` were already present (probe rc=0).

Question per mutant: does the receipt change, and would C2 V4 / V5 / V2-P10 catch it?

## 0. Baseline (pristine bytes)

```
python3 $S/lane/plans/build_pmars_probe.py --lane $S/lane --work $S/w > $S/base.receipt   # rc=0, 2.09s
cmp $S/base.receipt <lane>/corpus/evidence/round38/build-pmars-probe.txt  → identical
```

Baseline is byte-equal to the frozen receipt (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`), so the
receipt is deterministic on this host and every later diff is attributable to the mutation alone. Baseline passing
makes the runs below conclusive (a baseline failure would have been inconclusive). Detector = the probe's own
receipt run; C2 checks were then exercised by importing the frozen counter
`plans/round38_c2_verify.py` from the clone and calling `v4`/`v5`/`v7` directly (V2's gate run was not executed —
see §4 for how P10 was decided).

## 1. The five mutants (smallest behavior-bearing point each)

| id | point (probe line) | mutation (old → new) | mutant sha256 |
|----|--------------------|----------------------|---------------|
| M1 | 186, HARNESS_PY | `print("TEST " + name + " F error=" + type(e).__name__)` → `" P error="` (every non-AssertionError exception maps to P) | `db67200353a4ea91c415a8d5e19a0b356382e5eb1847fa53ebc2d31d85b1d75d` |
| M2 | 62 | `PATH = "/usr/local/sbin:/usr/local/bin:…"` → `PATH = "/usr/local/bin:…"` (drops /usr/local/sbin) | `bc97b37b4e6e8bacc2a414d4bf26383b52552623b9eb75a4f45b93877d3aadcf` |
| M3 | 77 | `DEBUG_OK = "00000   SPL.B  $     2, $     0\n00001   MOV.I  $     0, $     1\n"` → one address line only | `df2c269896cd6a58bc32b16f41272e3a1ad746a1db92c8d1dd2cb6fb18967d1d` |
| M4 | 219 | `argv.append("-DDLX11")` → `argv += ["-DDLX11", "-Wl,--no-as-needed", "-lX11"]` (dlopen variant also links libX11) | `22c8f0495e7c0d01e6c6d6d8eb9f185102620aa57e06b417daea255934fb40cc` |
| M5 | 240 | `argv = [BWRAP, "--unshare-net", "--unshare-pid", …` → drops `"--unshare-net"` | `da88a5b813dd74b2043ebb83040c2408a3bdceb509de7231909685608974ae0d` |

## 2. Does the receipt change? (empirical, `diff base.receipt Mx.receipt`)

| id | summary line of mutant receipt | flipping cases |
|----|-------------------------------|----------------|
| M1 | `cases=22 observed_pass=10 observed_fail=12 mismatches=4` | empty-tree `FFFF→FPFF` (still fail); canned-script, canned-static `PFPP→PPPP` (fail→**pass**); nonexec-binary `FPPP→PPPP` (fail→**pass**) — the 4 `error=CalledProcessError` tests become P |
| M2 | `cases=22 observed_pass=6 observed_fail=16 mismatches=1` | path-split `PPPP→FPPP` (pass→**fail**): the sbin script leaves PATH, the silent ulb binary answers |
| M3 | `cases=22 observed_pass=0 observed_fail=22 mismatches=14` | 14 cases flip `match=NO`; every one of the 7 observed passes (all use default DEBUG) becomes fail |
| M4 | `cases=22 observed_pass=6 observed_fail=16 mismatches=1` | canned-x11-dlopen `PPPP→PFPP` (pass→**fail**): ldd now lists libX11 via DT_NEEDED |
| M5 | **unchanged** — diff empty, byte-identical to frozen receipt | none |

Full diffs and receipts: `.ufo/waves/round-38/build/R38MutProbe/{base,M1..M5}.receipt`, `M{1..5}.diff`.

## 3. Would C2 V4 / V5 / V2-P10 catch it?

**P10 (gate `c_rerun`, plans/pkg_gate.py:267-285):** re-runs the tree's `probe_cmd` (`plans/build_pmars_probe.py
--lane .`, spec `plans/pkg-spec-r38.json`) and defects unless stdout is byte-equal to the receipt. The per-mutant
receipts above ARE that fresh stdout, so P10 is red for M1–M4 (diffs of 18/8/38/8 lines) and **green for M5**
(byte-identical). ("A quote not verbatim … and a receipt a fresh run does not reproduce are defects" — pkg_gate.py:13.)

**V4/V7 (frozen counter executed against each mutant receipt; entry = the requirement map a seat would derive
from the frozen receipt, all seven labels `partly` — control run: V4 `bad=0`, V7 `bad=0`):**

| id | V4 (minimal compliant entry, 1 cited case/row) | V7 (frozen-derived labels) |
|----|------------------------------------------------|-----------------------------|
| M1 | DEFECT `mismatches_named=2/4 … ['canned-script', 'canned-static']` | ok (labels still derive `partly`) |
| M2 | DEFECT `mismatches_named=0/1 … ['path-split']` | DEFECT `install-path: labelled partly, receipt derives enforced` |
| M3 | DEFECT `mismatches_named=1/14` (13 unnamed) | DEFECT all 7 tags `labelled partly, receipt derives enforced` |
| M4 | DEFECT `mismatches_named=0/1 … ['canned-x11-dlopen']` | DEFECT `no-x11: labelled partly, receipt derives enforced` |
| M5 | ok | ok |

**V5 (probe + dry table at freeze digests):** DEFECT `probe or dry table not at freeze digest` for all five
mutants (each mutant sha256 above ≠ `32f0771c…`; the `--dry` output itself is unchanged by all five, so the
digest check is what fires).

### Detection matrix

| id | receipt changed | P10 | V4 | V7 | V5 | C2 admits? |
|----|-----------------|-----|----|----|----|------------|
| M1 | yes | red | red | green | red | no |
| M2 | yes | red | red | red | red | no |
| M3 | yes | red | red | red | red | no |
| M4 | yes | red | red | red | red | no |
| M5 | **no** | green | green | green | **red** | no |

**Verdict counting: 5/5 caught** — every mutant turns the C2 predicate red at landing. The breakdown matters:
M1–M4 are killed behaviorally (receipt changes → P10 and V4 and mostly V7 fire); M5 is a behaviorally surviving
mutant on this host — nothing in the grader touches the network, so dropping `--unshare-net` is receipt-invisible
and only the V5 byte pin kills it. Coverage finding, per the mutation-tester contract: the receipt attests grader
verdicts but does not attest the sandbox flags that produced them; hermeticity of `--unshare-net` is unverifiable
from C2's evidence chain. No contract change proposed — the probe is frozen this round.

## 4. Limits and artifacts observed (not contract changes)

- **V4's naming rule is satisfiable by a citing entry.** First experiment used a stub entry whose map rows cited
  *every* violating case: V4 returned ok for M1–M4 (`mismatches_named=4/4`, `1/1`, `14/14`, `1/1`) because every
  case id appears somewhere in the entry. Only with the minimal compliant entry (≥1 cited case per row) does V4
  actually catch the receipt changes. The counter's guarantee for a hand-derived entry therefore rests on V5/P10
  (and V7's derived-label rule), same family as the freeze's own note that V7 alone is satisfiable by a hand-typed
  receipt.
- P10 was decided by byte-comparison of fresh mutant stdout against the receipt (the exact comparison
  pkg_gate.py:283-284 performs); the full gate run was not executed, since in a landing tree the probe is pinned
  by V5 regardless and V2 would fail for unrelated wave-1 reasons (no entry/SOURCES rows yet).
- Host scope: one host, bwrap/glibc as at freeze; M5's equivalence is a statement about this grader on this host,
  not about network use in general.

## 5. Restoration and cleanup evidence

- Mutants lived only at `$S/mut/`; the clone's `plans/build_pmars_probe.py` was temporarily overwritten only
  inside the V5 loop and restored in the same loop (script printed `probe restored: True`,
  `receipt restored: True`).
- Before scratch deletion: clone probe `32f0771cd5c4129a9a9795e3016a4f1c2cf660003f09cb4d719731fd5825c24a`
  (= counter pin), clone receipt `2408b477b0299e1339064b4b3df968a00174b3a5999016073b5fe4fd8cbb4ef9`,
  `cmp` clone receipt vs lane receipt → identical; spec `bd9bfe71…` untouched.
- The scratch clone created an entry stub only inside the clone (`corpus/knowledge/tb2-build-pmars-grader.md`);
  it is deleted with `$S`. `$S` removed after receipts/diffs were copied to
  `.ufo/waves/round-38/build/R38MutProbe/`. The lane tree was never written.

VERDICT: probe-mutants-5/5
