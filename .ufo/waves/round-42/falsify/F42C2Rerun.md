# F42C2Rerun — C2 (coverage) re-measure at docs tip 508434a, wave 2 (falsify)

Seat: F42C2Rerun (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (never edited).
Clone: `/fast/scratch/hyaku/kengaku-r42/F42C2Rerun/lane` (git clone --no-local, checkout `508434ad55c709337065611691c426f05875492d`).
Scratch: `/fast/scratch/hyaku/kengaku-r42/F42C2Rerun`.
No lane file was created, modified or deleted; no commit, no jj mutation, nothing written to `/home/vgpnk/.local/bin`, `$HOME`, `/usr`, `/etc` or the fleet root.

Axes (godspeed): **A** reproduce the C2 predicate at the docs tip on a clean clone; **B** probe byte-determinism across
three invocation shapes (plain / hermetic `env -i` / fresh `--work`); **C** does the counter actually discriminate a
subtle receipt forgery; **D** freshness — is the landing measurement still the same object as the docs tip.

## Clone identity (asserted before any write)

```
$ git -C /fast/scratch/hyaku/kengaku-r42/F42C2Rerun/lane rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r42/F42C2Rerun/lane
$ git -C …/lane rev-parse HEAD
508434ad55c709337065611691c426f05875492d
$ sha256sum plans/round42_c2_verify.py (live lane vs clone)
270097fdf1d25ee86cced105c731eb5eb4cb73baff6cc547710a8cf5961cf2c7  …/kengaku-shokunin/plans/round42_c2_verify.py
270097fdf1d25ee86cced105c731eb5eb4cb73baff6cc547710a8cf5961cf2c7  …/F42C2Rerun/lane/plans/round42_c2_verify.py
$ sha256sum plans/fibsqrt_probe.py (live lane vs clone)
fc58bf3f1780aaefee9df1e635b01765d3fb5d9224f1958494df4e1b8ed061b3  (both; equals PROBE_SHA256 pin in the counter)
```
Note: the live lane head is `445e81f821788c04c1f1f75b859aa1b71ac8560f` (wave-2 seats appending to `.ufo/`); its
`plans/round42_c2_verify.py` and `plans/fibsqrt_probe.py` are byte-identical to the clone at 508434a, so the
counter I ran is the same object.

## A. C2 counter at 508434a — run 1

```
$ S=/fast/scratch/hyaku/kengaku-r42/F42C2Rerun; export TMPDIR=$S
ENVELOPE: bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>
BEFORE date: 18:03:37   BEFORE localbin: 8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52  -
$ bwrap … python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round42_c2_verify.py --lane "$S/lane" --work "$S/w"
V1 ok listed=9 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=24 distinct_quotes=24 distinct_lines=24 out_of_word_range=0
    gate: P4 ok checked=24 bad=0 first=0
    gate: P5 ok manifest_entries=9 bad=0 first=0
    gate: P6 ok rows=3 bad=0 first=0
    gate: P7 ok source_lines=3 bad=0 first=0
    gate: P8 ok index_rows=49 knowledge_files=49 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=4212
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=3 bad=0
V4 ok cases=16 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=7 tags=7 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=16/16 bad=0
checks=9 defects=0
PREDICATE C2 pass
EXIT=0
AFTER date: 18:04:33    AFTER localbin: 8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52  -
```
Receipt `receipt-c2.txt` sha256 `eada6e7773f1c64c7b2ccf19dd1b05becdbee4be0af8d96cffabc3fa77b9d86c`.

Repeat (fresh `--work`, run 2, `receipt-c2-rerun.txt` sha256
`9f1d0276218193f2176a84bd1de22ff020115cd1152d8b16ccfe1609dd80c9ab`) reproduced **every V line and every gate
line byte-for-byte** — `checks=9 defects=0`, `PREDICATE C2 pass`, `EXIT=0`, 18:07:41→18:08:39. The only textual
difference between the two receipts is the `BEFORE/AFTER date` and `WORK=` lines.

## B. Probe three times, each `cmp` against the frozen receipt

Frozen receipt: `corpus/evidence/round42/fibsqrt-probe.txt`, 4212 bytes, sha256
`2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a`.

| run | shape | envelope | exit | cmp |
|---|---|---|---|---|
| 1 | `--lane $S/lane` (plain) | bwrap line above | 0 | **cmp=0** |
| 2 | `env -i PATH=/usr/bin:/bin python3 …` | bwrap line above | 0 | **cmp=0** |
| 3 | `--work $S/w3.<mktemp>` (fresh dir, empty before and after) | bwrap line above | 0 | **cmp=0** |
| 4 (bonus) | `--lane` = symlink to the clone, `cd /` | bwrap line above | 0 | **cmp=0** |

```
$ sha256sum run1-plain.txt run2-envi.txt run3-work.txt run4-symlink.txt
2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a  run1-plain.txt
2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a  run2-envi.txt
2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a  run3-work.txt
2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a  run4-symlink.txt
```
Times: run1 18:04:46→18:05:43; run2 18:04:46→18:05:43; run3 18:04:46→18:05:43; run4 18:07:41→18:08:38.
`ls -A /home/vgpnk/.local/bin | sha256sum` = `8cf5b15…86d52` before and after **every** run (unchanged), and the
`--work` directory was empty after run 3 (`ls -A "$W" | wc -l` → `0`). Empty stderr on all four.

**Probe byte-equal: 3/3 (and 4/4 counting the symlink variant).** The receipt carries no temp path, host version or
timing, so `env -i` and a different `--lane` spelling cannot perturb it.

## C. Does the counter discriminate a forged receipt? (negative control, advisory)

Cheap and in parallel: `cp -a lane lane-mut`, then a **length-preserving** edit of the receipt —
`observed_pass=7` → `observed_pass=8` (4212 bytes → 4212 bytes, sha `8a7fe71c6415…1bf7de`). Ran the same counter on it.

```
V1 ok listed=9 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned            <-- P2 does NOT fire (presence check by construction)
    …
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V4 DEFECT cases=16 mismatches_named=0/0 bad=['summary disagrees with the CASE lines']
V5 ok … V6 ok … V7 ok … V8 ok … V9 ok
checks=9 defects=2
PREDICATE C2 fail
EXIT=1
```
So a one-digit receipt forgery is killed, by **P10** (authenticity) and **V4** (internal tally), while 7 of 9 checks
stay green. This matches the counter's own docstring: `fills receipt_sha256 with the digest of the receipt it finds,
so P2 is a presence check` (`plans/round42_c2_verify.py:20-21`) — i.e. `P2 ok` in my run A is **not** evidence of
receipt authenticity, and no reader should treat it as such.

## D. Independent recomputation of the capture pins

```
$ cd lane/corpus/evidence/round42/tb2-circuit-fibsqrt && sha256sum *
gates.txt       032786f9…6ad29     instruction.md a7f50026…ab9ea   sim.c   700645ac…796173
solve.sh        a4ffab41…85d0b     test_outputs.py 6117b8ed…6f0438
(also Dockerfile 780c2398…3d3d4, README.md 201f7c88…4cbd, task.toml 9f5aa1f7…40972, test.sh 4770437e…6c334)
```
All five digests in the receipt header match the files independently; all nine match
`corpus/evidence/round42/tb2-circuit-fibsqrt/SHA256SUMS`. Independent tally of the receipt body:
`cases 16 pass 7 fail 9 match=no 0` vs its summary `cases=16 observed_pass=7 observed_fail=9 mismatches=0`.

Freshness check (`git -C lane diff --name-only ff14d76… 508434a` restricted to the C2 surfaces —
`corpus/evidence/round42`, `plans/fibsqrt_probe.py`, `plans/round42_c2_verify.py`, `plans/pkg-spec-r42.json`,
`plans/pkg_gate.py`, the grader entry, `corpus/SOURCES.md`, `corpus/README.md`, `SKILL.md`, `PROVINCE.md`,
`corpus/QUALITY.md`): **empty**. The whole landing→docs-tip delta is `LOG.md`, `SCORECARD.md`,
`corpus/lessons/round-42.md`, `.ufo/waves/round-42/integrate/{census-final,measure-final}.txt` (1185 insertions).
So the landing measurement is the same object I re-measured; my run adds the docs-only commits and reproduces it.

## Findings for the L1 (advisory; nothing here is a predicate failure)

1. **Host coupling in V6** — the counter hardcodes `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`
   (`plans/round42_c2_verify.py`), a fleet-root path that does **not** exist inside the lane (no `scripts/` dir in the
   clone). So `census_exit=0` is a statement about the *host's* census script (sha256
   `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, 35466 bytes) reading the clone's
   `corpus/SOURCES.md`, not a self-contained clean-clone check. A changed census script changes the verdict with no
   lane change. Worth a sentence in the C2 claim; do not "fix" the frozen counter.
2. **`P2 ok` is a presence check, not an authenticity check** (docstring lines 20-21, confirmed by control C). The
   frozen claim should keep resting authenticity on P10 alone.
3. **Load concentration**: a forged receipt trips exactly 2 of 9 checks (P10, V4). The other seven are insensitive to
   receipt content (`V5` pins the probe/dry table, `V6` the census, `V7`/`V8`/`V9` the entry/tags/table, `V1`/`V3`
   the captures/spec). That is adequate but should be stated as "P10 is the sole authenticity gate".
4. **Probe limits already on the record and still true** (read from `plans/fibsqrt_probe.py` docstring): host
   `python3`/`gcc` stand in for the image's Debian bookworm 3.13 and gcc; the task image is never pulled; recipes run
   as the probing user. Byte-equality is therefore a *same-host* determinism claim (it survived `env -i`, which
   removes `PATH`/`HOME`/locale variation but not the toolchain), not a portable one.
5. No discrepancy found in the landed C2 surfaces at 508434a: `SOURCES.md` S125-S127 rows, README index row/coverage
   bullet/§Frontier "8 of 89", SKILL registry rows, QUALITY Q33/Q34 and the entry are all pinned and green under
   V1/V3/V5/V7/V8/V9 as shown.

## Risks

- The D-check uses `git diff --name-only` against the frozen landing id; if the L1 later rewrites history in the lane,
  the "byte-identical C2 surfaces" statement must be re-derived.
- My negative control mutated a *copy* in scratch only; the frozen counter and battery were not touched.
- V6 host coupling (finding 1) is the one place where a "clean clone" result can move without any repo change.

## Files changed

None in the lane. Scratch only (`/fast/scratch/hyaku/kengaku-r42/F42C2Rerun`, receipts quoted above; the 577 MB
`lane`/`lane-mut` clones are released with `scratch_guard.py safe-rm` scoped to my seat).

VERDICT: c2-rerun-pass-probe-byte-equal-3/3
