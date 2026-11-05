# R89-C1 control battery — seat ExecCtrlC1 (round 89, wave 1)

2026-11-05. Counter `plans/round89_c1_replay.py` exercised only on scratch clones
(`/fast/scratch/hyaku/kengaku-r89/ExecCtrlC1/{lane,lane2,lane3}`, cloned `--no-hardlinks` from the lane repo).
All fixture commits were made on top of the measured tip `a9b8a1a00b6a5ab5206be4d377dba439e02f8244` (detached
checkout inside each scratch clone) with throwaway identity `seat <seat@scratch>` after
`git rev-parse --show-toplevel` was asserted to equal the clone. The clone default HEAD was `00462b596f51`;
`git diff a9b8a1a..00462b5` on every involved path (counter, probe, receipt, case table, ledger) is empty
(`transcripts/00-env.txt`), so tip-based fixtures are faithful. Pinned inputs verified at TIP: probe sha256
`03c202f5…` = `TRUSTED_TOOL_SHA`; capture sha256 `baed5e4d…` = `SUBJECT_SHA`; table sha256
`7dff1654…` = receipt `CASE_TABLE_SHA`; `d1c4f1b`, `0e6bb05`, `000b7d1`, `a9b8a1a`, `192e809d` all resolve.
Counter bytes invoked = the counter blob at the measured tip (sha256 `c59e761c…`, `transcripts/00b-counter-bytes.txt`).

## Results

| # | control | rev | expected | observed rc | observed verdict | match |
|---|---------|-----|----------|-------------|------------------|-------|
| 1 | positive | `a9b8a1a` | rc 0, `PREDICATE R89-C1 pass` | **1** | `DEFECT L6-reproduce`, `PREDICATE R89-C1 fail` | **NO — finding F1** |
| 2 | do-nothing | `192e809d` | rc 1, fail, named DEFECTs | 1 | fail, 4 DEFECTs (verbatim below) | yes |
| 3 | ledger-only | `ae4618ff` (receipt removed) | rc 1, `DEFECT L1-receipt` | 1 | single `DEFECT L1-receipt` | yes |
| 4 | forged-receipt (seat recipe) | `672ed5c5` | rc 1, `DEFECT L3-tip` | 1 | `DEFECT L6-reproduce`, **no L3 defect** | **NO — finding F2** |
| 4b | forged-receipt (claims-file variant, informational) | `7abed8e1` | — | 1 | `DEFECT L3-tip LANE_TIP 9666fb0610fd is not an ancestor of 7abed8e174f1` + `DEFECT L6-reproduce` | (counter behaves as the claims file states) |
| 5 | forged-probe | `8418465f` | rc 1, `DEFECT L9-tool` | 1 | single `DEFECT L9-tool` | yes |
| 5b | forged-probe, L9 branch disabled (scratch counter copy) | `8418465f` | — | **0** | `PREDICATE R89-C1 pass` | (answers the item's question: **yes, L6 alone would have passed**) |

## Finding F1 — positive control not reproducible on this host: user namespaces disabled (host state)

Command (`transcripts/01-control1-positive.txt`):

```
$ /usr/bin/python3 …/lane/plans/round89_c1_replay.py --lane …/lane --rev a9b8a1a00b6a5ab5206be4d377dba439e02f8244 --work …/w0
DEFECT L6-reproduce probe re-run rc=2 produced no observation block
TARGET executed_rows=33 member=polyglot-rust-c located=0 executed=0 cases=8 legs=8 mismatches=0 defects=1
PREDICATE R89-C1 fail
rc 1
```

Expected per the frozen contract and L1's `L1/c1-tip.txt`: `… defects=0`, `PREDICATE R89-C1 pass`, rc 0.

Counter logic is exonerated for this mismatch: the other eight legs pass mechanically at the tip (L2/L4/L8/L9
pin checks verified against the measured blobs above). The failure is environmental. Reproducing leg L6's exact
invocation (`git archive a9b8a1a | tar -x`, then `env -i PATH=/usr/bin TMPDIR=… python3 -I -B <tree>/plans/round89_polyglot_probe.py --lane <tree> --work …`) gives the probe's stderr verbatim:

```
DEFECT SETUP sandbox-exit=1 stderr='bwrap: Creating new namespace failed: nesting depth or /proc/sys/user/max_*_namespaces exceeded (ENOSPC)'
PREDICATE R89-PROBE setup-defect
RC=2
```

A standalone trivial bwrap (no counter, no probe) fails identically right now, and the host limit is measured:

```
$ bwrap --unshare-all --die-with-parent --new-session --ro-bind /usr /usr --proc /proc --dev /dev --clearenv --setenv PATH /usr/bin /usr/bin/true
bwrap: Creating new namespace failed: nesting depth or /proc/sys/user/max_*_namespaces exceeded (ENOSPC)   [rc 1]
/proc/sys/user/max_user_namespaces = 0   (max_pid/net/mnt_namespaces = 122865)
```

`max_user_namespaces = 0` disables unprivileged user namespaces host-wide, so no grader replay (leg L6) can
execute in this host state. The receipt (`EXIT 0`) and L1's recorded tip run were produced when namespaces were
available; toolchain otherwise matches the receipt's honest-limits note (Python 3.14.8, rustc 1.99.1,
g++ 16.2.1, bubblewrap 0.13.1). This is outside a seat's remit to remediate (a sysctl write is a host mutation);
the instruments were not touched. Consequence for scoring: at `max_user_namespaces=0` the frozen tip figure
`defects=0 / pass / rc 0` is unreachable by independent re-execution until the host re-enables user namespaces.

## Finding F2 — the prescribed forged-receipt steps cannot produce the predicted `DEFECT L3-tip`

The seat recipe ("orphan branch, one empty commit `HF`, replace receipt `LANE_TIP` with that hash, commit `H4`,
run at the new HEAD") makes `HF` the **parent** of `H4`, so L3's ancestry check passes by construction:

```
HF = 9666fb0610fda20dc714b206789a790326315211  (empty orphan root)
H4 = 672ed5c5728aca5b95e0a6397f7ab398256526e5  (parent: HF)
$ git merge-base --is-ancestor HF H4   → rc 0 (yes)          [transcripts/04-control4-forged-receipt.git.txt]
```

Command and observed output (`transcripts/04-control4-forged-receipt.txt`):

```
$ python3 …/lane2/plans/round89_c1_replay.py --lane …/lane2 --rev 672ed5c5728aca5b95e0a6397f7ab398256526e5 --work …/w3
DEFECT L6-reproduce probe re-run rc=2 produced no observation block
TARGET executed_rows=33 member=polyglot-rust-c located=0 executed=0 cases=8 legs=8 mismatches=0 defects=1
PREDICATE R89-C1 fail
rc 1
```

The observed rc (1) matches, but the named defect does not: no `L3-tip` line was emitted, and the only defect is
the F1 environmental L6 failure. Absent that host condition, the prescribed steps would exit **0**
(`PREDICATE R89-C1 pass`) — i.e. recipe-as-written is a passing self-referential forgery path (receipt names an
attacker-minted ancestor), not a control that fails L3. The claims file describes the control as "stamp
`LANE_TIP` replaced by a commit that is **not an ancestor** of the measured revision"; I ran that variant too
(same forged `LANE_TIP`, receipt committed on the measured-tip lineage, `H4b = 7abed8e174f1`,
`transcripts/04b-*`), and the counter behaves exactly as the claims file states:

```
DEFECT L3-tip LANE_TIP 9666fb0610fd is not an ancestor of 7abed8e174f1
DEFECT L6-reproduce probe re-run rc=2 produced no observation block   [F1 host condition]
TARGET … defects=2
PREDICATE R89-C1 fail
rc 1
```

So: the counter's L3 leg is sound for the claims-file semantics; it is the seat item's literal steps that cannot
deliver the predicted defect. Reported, not repaired (frozen instruments untouched).

## Item sub-report — forged-probe with L9 disabled (control 5b)

Answer: **yes — L6 alone (without L9) would have passed the forged state.** Scratch copy of the counter
(`c1_replay_noL9.py`, single edit `elif sha256(tool) != TRUSTED_TOOL_SHA:` → `elif False:`; the lane's counter
file was never edited — `transcripts/06-control5b-nol9.copy.txt`), same forged state `8418465f`:

```
TARGET executed_rows=33 member=polyglot-rust-c located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0
PREDICATE R89-C1 pass
rc 0
```

Control 5 itself matched prediction exactly — the pinned `TRUSTED_TOOL_SHA` is the only effective defense
against the Sentinel-F1 echo probe: `DEFECT L9-tool probe sha=d1ecc58be81b0b1d != TRUSTED_TOOL_SHA 03c202f5072e8aa5`
(forged probe sha256 `d1ecc58be81b0b1d286f49366c7fb31f5203e913f04429dc058a8ef00948eb43`), rc 1, and L2 accepted
the hand-regenerated stamp `TOOL_SHA` because it only compares the stamp to the bytes at the rev, while L6
re-runs the very probe bytes at the rev and therefore reproduces the forgery line-for-line — consistent with the
counter's own honest-limit note.

## Matched controls (verbatim)

Control 2, do-nothing at `192e809d` — byte-identical defect set to L1's `L1/c1-base.txt`:

```
DEFECT L4-table plans/round89-cases.json absent at measured
DEFECT L9-tool plans/round89_polyglot_probe.py absent at 192e809d582e
DEFECT L1-receipt corpus/evidence/round89/polyglot-rust-c-probe.txt absent at 192e809d582e
DEFECT L7-ledger row {"classes": ["shell-exec", "stdout-inspection", "subprocess-exec"], "evidence": "no-blocker: tests/test_outputs.py sha256=baed5e4d0cc0e580", "reason": "unattempted", "status": "unexecuted"}
TARGET executed_rows=32 member=polyglot-rust-c located=0 executed=0 cases=0 legs=0 mismatches=0 defects=4
PREDICATE R89-C1 fail
rc 1
```

Control 3, ledger-only at `ae4618ff710151d2d4d1b0194bd9203fb18f7fe6` (receipt removed, ledger row intact; fixture
parented on `a9b8a1a`):

```
DEFECT L1-receipt corpus/evidence/round89/polyglot-rust-c-probe.txt absent at ae4618ff7101
TARGET executed_rows=33 member=polyglot-rust-c located=0 executed=0 cases=0 legs=0 mismatches=0 defects=1
PREDICATE R89-C1 fail
rc 1
```

## Notes

- Item-text inconsistency: the acceptance line says "predicted: 1,2,3,4,5 all exit 1 with the named defect",
  but step 1 and the frozen contract's measured tip figure require control 1 to exit 0 with
  `PREDICATE R89-C1 pass`. I used the step-level/frozen expectation for control 1.
- Fixture commits: `H3=ae4618ff7101` (control 3), `HF=9666fb0610fd` + `H4=672ed5c5728a` (control 4),
  `H4b=7abed8e174f1` (control 4b), `H5=8418465f382e` (control 5) — all inside scratch clones, throwaway
  identity, `--show-toplevel` asserted before each.
- Bound hygiene: production files read-only (counter/probe/receipt/claims read via `read`/`git show` only);
  no counter edit in the lane (5b used a scratch copy); no installs (existing rustc/g++/bwrap/python3 used);
  no network; scratch tree deleted before yielding; transcripts preserved under `transcripts/` here.
