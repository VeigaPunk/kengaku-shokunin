# R44XMutNearU — near-variants of the five frozen C1 mutants (round-45 data)

Seat: R44XMutNearU (mutation-tester, leaf). Date: 2026-10-26. Lane repo frozen tools, never edited:
`plans/anchor_digest_check.py` `11bb2cad…`, `plans/order_check.py` `948d5e1d…`. Frozen counter
`plans/round44_c1_verify.py` never edited; the probe ran on a **scratch copy** (below).

## Method

- Scratch `S=/fast/scratch/hyaku/kengaku-r44/R44XMutNearU`; `git clone -q --shared` of the lane →
  `$S/lane`; `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane` (verified before any run). Clone
  HEAD `5e3d3aa06c6b7000929ac3e62563a39159c4501f` (lane has moved past the freeze baseline `0cb2e225…`;
  both tools still digest-equal the frozen PINS, so the mutation surface is the frozen one).
- Counter copy: `cp plans/round44_c1_verify.py $S/c44/c44.py`, then only its `MUTANTS` table replaced
  with **13 near-variants** (development mode only). The copy lives in `$S/c44/` — a sibling of the
  `--work` root, mirroring the frozen layout (the counter hides its own directory from tool runs; nesting
  it over the work root would have hidden the fixture dirs). `python3 -m py_compile` on the copy: OK.
- Batteries, both read-only inputs to the counter:
  - **witness** = the frozen pre-freeze direction module, used in place exactly as the freeze witness run
    did: `--battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/witness`
    (6 fixtures; baseline `claims/witness-run.txt`: frozen U5 U6 U7 U9 U14c `killed=5`, every `value=differs`).
  - **standing** = battery42 + battery43 as one battery: 12 modules copied byte-for-byte from the L1
    standing-control copy `/fast/scratch/hyaku/kengaku-r44/L1/ctl/m-standing/plans/battery44/` into
    `$S/bs/` (digests listed under Restoration; identical to the digests the frozen control
    `claims/control-c1-standing-batteries.txt` ran, which killed 0/5). 71 fixtures.
- Runs: `$S/c44/c44.py --lane "$S/lane" --battery-dir <dir> --only U5N1,…,U14N3 --work "$S/w" --jobs 4`,
  each inside the round-44 envelope. Dev mode prints `PREDICATE C1 n/a`. Neither battery module was
  modified; the witness directory was only read (the envelope holds `/home/vgpnk` read-only).

## Variants (one single replacement each, same `old` span as the frozen parent)

| id | parent | tool | dir | edit on the frozen line/branch |
|---|---|---|---|---|
| U5N1 | U5 | anchor | silence | label boundary `< 64` → `< 63` (63-hex token labelled `digest-long`) |
| U5N2 | U5 | anchor | silence | short token labelled `digest-uppercase` |
| U6N1 | U6 | anchor | silence | long token labelled `digest-uppercase` |
| U56N | U5+U6 | anchor | silence | both labels swapped in one edit |
| U7N1 | U7 | anchor | rc-mirror | `[:1]` → `[-1:]` (last resolving capture claimed) |
| U7N2 | U7 | anchor | rc-mirror | `claimed.update(hit)` → `claimed.update(hit[:1])` (claim restricted, `hit` full) |
| U7N3 | U7 | anchor | rc-mirror | `claimed.update(hit)` → `claimed.update(())` (token claims nothing) |
| U9N1 | U9 | anchor | rc-mirror | lessons read from the **index** (`git show :<p>`) instead of the working tree |
| U9N2 | U9 | anchor | rc-mirror | `errors="replace"` → `errors="strict"` |
| U9N3 | U9 | anchor | rc-mirror | lessons read from `HEAD~` instead of the working tree |
| U14N1 | U14c | order | error | guard re-spelled `if m is None:` (semantics-preserving) |
| U14N2 | U14c | order | error | guard disabled via impossible condition `if m is False:` |
| U14N3 | U14c | order | error | guard narrowed: `if not m and not claims.startswith("plans/"):` |

All 13: `src.count(old)==1`, newline count preserved, compiled, `adv_kind=direct` (same advertised
sentences at `anchor_digest_check.py:88`, `:98-99`, `:106-107`, `order_check.py:26-27`).

## Results — witness battery (w_u.py, 6 fixtures), envelope-wrapped

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44XMutNearU/env /fast/scratch/hyaku/kengaku-r44/R44XMutNearU/env --bind /fast/scratch/hyaku/kengaku-r44/R44XMutNearU/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r44/R44XMutNearU/c44/c44.py --lane /fast/scratch/hyaku/kengaku-r44/R44XMutNearU/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/witness --only U5N1,…,U14N3 --work …/w --jobs 4
ENVELOPE start 20:43:34 … PINS total=2 mismatched=0 … BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=13 killed=10 survived=3 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=8/10 order=2/3 … PINS-AFTER mismatched=0 … PREDICATE C1 n/a
ENVELOPE end 20:43:38 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
Full output: `wave/R44XMutNearU/witness.txt` (4,086 B). Pristine baseline inside the same run: all 6
`FIXTURE … ok` lines (reference result equals every declaration), so the detector on pristine bytes
behaves; a survivor below is a coverage finding, not a detector fault.

## Results — standing battery (b42+b43, 71 fixtures), envelope-wrapped

```
ENVELOPE … -- /usr/bin/python3 …/c44/c44.py --lane …/lane --battery-dir …/R44XMutNearU/bs --only U5N1,…,U14N3 --work …/w --jobs 4
ENVELOPE start 20:43:39 … PINS total=2 mismatched=0 … BATTERY fixtures=71 wrong=0 tampered=0 sidechannel=0
MUTANTS total=13 killed=1 survived=12 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/10 order=0/3 … PINS-AFTER mismatched=0 … PREDICATE C1 n/a
ENVELOPE end 20:43:51 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
Full output: `wave/R44XMutNearU/standing.txt` (10,632 B). Both envelope digests `unchanged` → both
measurements count. No `invalid`, no `unattributed`, no `null_detected` anywhere.

## Table: variant → direction witnessed → killed by which battery

| variant | witness battery | standing battery |
|---|---|---|
| U5N1 | KILLED by=u5-sixty-three-hex, silence, attributed=L522, value=differs | SURVIVED exhibits=none |
| U5N2 | KILLED by=u5-sixty-three-hex, silence, attributed=L522, value=differs | SURVIVED exhibits=none |
| U6N1 | KILLED by=u6-sixty-five-hex, silence, attributed=L522, value=differs | SURVIVED exhibits=none |
| U56N | KILLED by=u5-sixty-three-hex, silence, attributed=L522, value=differs | SURVIVED exhibits=none |
| U7N1 | KILLED by=u7-twin-captures, rc-mirror, attributed=L539, value=differs | SURVIVED exhibits=none |
| U7N2 | KILLED by=u7-twin-captures, rc-mirror, attributed=L539, value=differs | SURVIVED exhibits=none |
| U7N3 | KILLED by=u7-twin-captures, rc-mirror, attributed=L539, value=differs | **KILLED by=a_alt-erratum-lessons, rc-mirror, attributed=L539, value=differs** |
| U9N1 | KILLED by=u9-dirty-erratum, rc-mirror, attributed=L384, value=differs | SURVIVED exhibits=none |
| U9N2 | SURVIVED exhibits=none | SURVIVED exhibits=none |
| U9N3 | SURVIVED exhibits=0>2 | SURVIVED exhibits=0>2,1>2 |
| U14N1 | SURVIVED exhibits=none | SURVIVED exhibits=none |
| U14N2 | KILLED by=u14c-odd-claims-name, error, attributed=L161, value=differs | SURVIVED exhibits=none |
| U14N3 | KILLED by=u14c-odd-claims-name, error, attributed=L161, value=differs | SURVIVED exhibits=none |

Totals (commands above): witness `killed=10 survived=3`; standing `killed=1 survived=12`.

## Findings (coverage data for round 45, not contract changes)

1. **The standing battery kills a *stronger* U7 edit but not the frozen-shaped ones.** U7N3
   (`claimed.update(())`) is killed by battery43 `a_alt-erratum-lessons` — a fixture where emptying the
   claim set turns an accept into a capture-unanchored reject — while U7's own shape (`[:1]`) and both
   near-shapes that still claim one capture (U7N1 `[-1:]`, U7N2 `hit[:1]`) survive. The branch is not
   unreached; the *frozen direction* is the part the standing fixtures miss.
2. **All other nine behavioural near-variants are alive after the standing battery** — the four label
   edits on the `cls, why` line, the two one-capture claim edits, the index-read erratum variant, and
   both order-guard edits. Whatever battery44 builds for U5/U6/U7/U9/U14c must be at least as
   discriminating as `w_u.py`, which killed 10/13 in the declared directions with attributed
   `value=differs` kills.
3. **Two true equivalents survive everything, as designed:** U9N2 (`errors="strict"`, identical on
   UTF-8 lessons) and U14N1 (`m is None`). They are limits of any result-difference battery, not
   battery44 gaps.
4. **U9N3 escapes its declared direction by crashing into the tool's catch-all:** reading lessons from
   `HEAD~` raises `Usage` on single-commit fixture repos; `anchor_digest_check.py` `main` converts every
   exception to exit 2, so the observed pair is `0>2` (and `1>2` on a standing reject fixture), never the
   declared `rc-mirror` (needs mutant exit 1). A direction table that also named `*>2` pairs would pin
   this shape; today such a mutant reads SURVIVED, not killed.

## Restoration evidence

- The counter applies mutants to copies in its own scratch (`variants/`), never to the clone; both runs
  end `PINS-AFTER mismatched=0` (command and output in the receipts above).
- After all runs: `sha256sum "$S/lane/plans/anchor_digest_check.py" "$S/lane/plans/order_check.py"` →
  `11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2`,
  `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc` — equal to the frozen PINS;
  `git -C "$S/lane" status --porcelain | wc -l` → `0`.
- Standing battery module digests (copied from the L1 control copy, used unmodified): b42_a_class
  `eef02b5df0a8b5e7…`, b42_a_route `d6dad7cd1458838…`, b42_a_row `947194e4517fb94b…`, b42_o_clause
  `badc9e3d3807e22c…`, b42_o_scan `4a9ef972806481ea…`, b43_a_alt `31ddcc0cb9a475dd…`, b43_a_err
  `2c41e02a38fcdb11…`, b43_a_row `b140efcf3f9088b4…`, b43_a_url `6a3d4732162c46a4…`, b43_o_alt
  `8555d3a663d9e58b…`, b43_o_excuse `9f741fdc126d6f0f…`, b43_o_scan `6ddcdbb8ca3075f1…`.
- No tool was installed or upgraded for this seat. Scratch `$S` removed at the end via
  `plans/scratch_guard.py safe-rm`; receipts kept under `wave/R44XMutNearU/`.

VERDICT: near-variants-13-alive-after-standing-12
