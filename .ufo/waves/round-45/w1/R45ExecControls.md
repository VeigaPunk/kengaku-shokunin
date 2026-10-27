# R45ExecControls — freeze control reproduction (kengaku round 45, wave 1)

Seat: `R45ExecControls` (executor, leaf). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Baseline measured: **freeze commit `b4fcd35141acda5fa0980a34dd29ab880b702ee6`**. Tip at seat start was
`52d7486`, tip at hand-off `4290d64`; `52d7486` was measured too because it re-pinned the C2 instrument
(§Drift 1). No lane file was edited; no commit; no install.

## Axes (godspeed)

- **calibration (judged)** — does the counter's frozen ladder still print the before-state the claims advertise?
  Reproduced 7/7 controls, 0 behavioural drift. This report is the artifact.
- **coverage / novelty / depth / operability / freshness / adjacency** — not touched by this seat; nothing here
  improves or harms them.

## Host safety

Every fixture build, counter run, probe and predictor control ran inside
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" <command>`:
bwrap with `/home/vgpnk` read-only, `~/.cache` overlaid from scratch, a CONTENT digest of `~/.local/bin`
before/after, exit 4 + `INVALID` on change. No file was written to any PATH directory, `/usr`, `/etc` or `$HOME`
outside scratch. Scratch `S=/fast/scratch/hyaku/kengaku-r45/R45ExecControls` (deleted at the end).

## Setup (exact commands, all under `$S`)

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel      -> /fast/scratch/hyaku/kengaku-r45/R45ExecControls/lane
git -C "$S/lane" checkout --detach b4fcd35141acda5fa0980a34dd29ab880b702ee6
git -C "$S/lane" log --oneline -1               -> b4fcd35 round-45: freeze claims, C1 fence counter + hostile/control evidence, ...
```
Four more clones (`lane-r44`, `lane-admit`, `lane-refuse`, `lane-static`) at the same commit, one per fence stub,
plus `lane-head` (`52d7486`) and two reconstructed-working-tree clones (`lane-untracked`, `lane-freeze-u151`,
§C2). `plans/fixture_fence.py` is absent at every commit this seat measured (`git ls-tree b4fcd35 -- plans/fixture_fence.py | wc -l` = 0), matching `control-c1-nothing.txt` line 2 `FENCE plans/fixture_fence.py absent`.

Fence files written into each clone (`plans/fixture_fence.py`) were built exactly as the seat spec says, and each
digest equals the `FENCE ... sha256=` line of the committed receipt it reproduces:

| control | fence assembled | sha256 | receipt's `FENCE` sha256 |
|---|---|---|---|
| nothing | (no file) | — | `absent` |
| r44 | `cat plans/round44_c1_verify.py claims/fences/r44_tail.py` | `db71ea2af35bb552188990fb4ba4985ba052b716bb8dfa01b9c302cbf05bafcb` | same |
| admit_all | `cp claims/fences/admit_all.py` | `6c3b9a18566a7045d679263867b64ff0735bc79a39abe7e57dfffd724f05d912` | same |
| refuse_all | `cp claims/fences/refuse_all.py` | `fc38325360ee7058401ff88c738ce4a7f5e0d8e97196b605b4b57dfed79ef867` | same |
| static_only | `cp claims/fences/static_only.py` | `efaf0bb19509b510945f222e7a262a6b301ea5dbaa1055f7c8eb0ab33c5743fe` | same |

(`sha256sum "$S"/lane-*/plans/fixture_fence.py`; the r44 adapter digest also pins the exact concatenation the
claims prescribe, so the adapter is unambiguous.)

## C1 — the fence calibration ladder reproduces exactly (5/5)

Command shape, once per control:
```
envelope.sh "$S/env" python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py \
    --lane "$S/lane-<n>" --work "$S/w-<n>"        # rc=1 for all five
```
(`plans/round45_c1_verify.py` sha256 `7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d` — the
freeze digest, identical at `b4fcd35` and `52d7486`.)

| control | REFUSALS line | HONEST line | CALIBRATION | PREDICATE | vs committed |
|---|---|---|---|---|---|
| nothing | `total=10 clean=0 leaked=10 read=0 hung=0 build_errors=0` | `fixtures=104 admitted=0 refused=104 read=0 hung=0 build_errors=0` | `advertised=10 contradicted=10` | fail | 4 summary lines byte-identical |
| **r44 fence** | `total=10 clean=3 leaked=3 read=4 hung=0 build_errors=0` | `fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0` | `advertised=10 **contradicted=7**` | fail | 4 summary lines byte-identical |
| admit_all | `clean=0 leaked=10 read=0 hung=0 build_errors=0` | `104 admitted=104 refused=0 ...` | `contradicted=10` | fail | byte-identical |
| refuse_all | `clean=10 leaked=0 read=0 hung=0 build_errors=0` | `104 admitted=0 refused=104 ...` | `contradicted=0` | fail | byte-identical |
| static_only | `clean=9 leaked=1 read=0 hung=0 build_errors=0` | `104 admitted=0 refused=104 ...` | `contradicted=1` | fail | byte-identical |

Every run printed `PINS total=33 mismatched=0` first. Per-fixture comparison (all 117 `FENCE-RUN` lines reduced to
`group module fid verdict opens=`, plus every `REFUSAL` row, plus the summary lines) is **identical** for all five
controls (`compare.sh`, `RESULT controls mismatched=0`). Two extra runs: `out-c1-r44-run2.txt` reproduces
`out-c1-r44.txt` bit-for-bit (determinism), and `out-c1-nothing-head.txt` reproduces the same four lines on the
`52d7486` clone (the C1 instrument and its 33 pins are unchanged between freeze and tip).

### The calibration count the round advertises (r44 fence, per module)

```
REFUSAL f10_laneinclude.py READ   fixtures=1 admitted=0 hung=0 opens=4   -- lane/.git/config carries an include
REFUSAL f1_gitfile.py      READ   fixtures=1 admitted=0 hung=0 opens=6
REFUSAL f2_deep.py         clean  fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f3_abbrev.py       clean  fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f4_fifo.py         READ   fixtures=1 admitted=0 hung=0 opens=1   -- --lane git hung
REFUSAL f5_alternates.py   clean  fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f6_above.py        READ   fixtures=1 admitted=0 hung=0 opens=3
REFUSAL f7_commondir.py    LEAKED fixtures=3 admitted=3 hung=0 opens=95  (40+40+15)
REFUSAL f8_worktreecfg.py  LEAKED fixtures=2 admitted=2 hung=0 opens=16  (8+8)
REFUSAL f9_nodescribe.py   LEAKED fixtures=1 admitted=1 hung=0 opens=0
```
i.e. cleaned = f2, f3, f5; **leaked** = f7 (commondir), f8 (config.worktree include), f9 (refuse-to-describe);
**refused with an outside read** = f1, f4, f6, f10 → `contradicted = 3 leaked + 4 read = 7`. This is the
before-state the assignment states (7 of 10 contradictory), reproduced exactly, including each module's
outside-open count.

## C2 — coverage controls reproduce byte-identically (2/2)

`plans/round45_c2_verify.py` has **two** committed versions, so both were measured against their own clone:

| run | clone / counter / spec | command | result |
|---|---|---|---|
| C2 nothing, freeze era | `lane` @`b4fcd35`, freeze counter (`SPEC_SHA256=b8fc1e53…`), 9-row spec (S149–S157) | `python3 "$S/lane/plans/round45_c2_verify.py" --lane "$S/lane" --work "$S/w-c2f"` | `checks=11 defects=8`, `PREDICATE C2 fail`, exit 1 |
| C2 nothing, HEAD era | `lane-head` @`52d7486`, HEAD counter (`SPEC_SHA256=3eb696b4…`), 8-row spec (S149–S156) | `python3 "$S/lane-head/plans/round45_c2_verify.py" --lane "$S/lane-head" --work "$S/w-c2h"` | `checks=11 defects=8`, `PREDICATE C2 fail`, exit 1 |
| predictor control | `lane` @`b4fcd35` | `cd "$S/lane" && python3 claims/c2_predictor_control.py "$S/predctl-freeze"` | `CONTROL-C2-PREDICTOR red-as-required`, exit 0 |

Byte comparison against the committed receipts (`claims/control-c2-nothing.txt` as committed at `52d7486`, and its
`b4fcd35` version from `git show`, and `claims/control-c2-predictor.txt`):

- **HEAD-era nothing control: byte-identical** — after reconstructing the capture-time working tree (`lane-untracked`:
  clone at `52d7486`, then `git rm --cached` the six wave-1 files that were untracked when the receipt was written:
  `.ufo/waves/round-45/{make_wave1_spec.py,w1-dispatch.json,w1-spec.json,w1-validate.err,w1.ready,w1/swarm-registry.json}`,
  `git ls-files --others | wc -l` = 6).
- **freeze-era nothing control: byte-identical** — reconstructed with 151 untracked files (`lane-freeze-u151`: clone
  at `b4fcd35`, untrack the 155 paths the freeze commit added, delete the four claim files created after that
  capture: `c2_predictor_control.py`, `c2-stage-check.txt`, `control-c2-predictor.txt`, `census-before.txt`).
- **predictor control: byte-identical** on the six `CONTROL` lines and `CONTROL-C2-PREDICTOR red-as-required`
  (pref=0 for always-true / substring / password-eq; `lint DEFECT` for format-regex and lookup-table; `ok` for the
  membership reading; `states=48 grader_pass=18 grader_fail=30`). The committed file's trailing `2026-10-26T23:05:22-03:00`
  line is a receipt footer, not script output (the script prints no timestamp).

## Lines that are *not* functions of the frozen instruments (explained, not drift)

1. **`gate: P9` clean-tree clause.** `plans/pkg_gate.py:259-265` runs `git -C <root> ls-files --others
   --exclude-standard` and reports `untracked=<n>`; the number is a property of the *measured working tree*.
   Measured: freeze-era receipt `untracked=151`, HEAD-era receipt `untracked=6`, a clean clone `untracked=0`
   (`out-c2-head.txt`, `out-c2-freeze.txt` → `P9 ok untracked=0 first=0`, `gate: defects=8` vs the receipts'
   `defects=9`). Reconstructing the capture-time untracked set makes the whole file byte-identical (§C2). The C2
   predicate (`checks=11 defects=8`, `PREDICATE C2 fail`, exit 1) is invariant across all three tree states.
2. **`FENCE-RUN … -- <reason>` truncation.** The counter prints `out[7:][:120]`, so a reason that embeds an
   absolute scratch path is cut at 120 chars. Committed and reproduced texts are all 120 chars and share a common
   prefix (f1 68, f2 65, f3 118, f6 65 chars) — the divergence point is exactly where my scratch path
   (`…/R45ExecControls/w-r44/…`) differs in length from the L1's (`…/L1/w5/…`). 3 of 7 reason texts are identical
   because they carry no path (`f10` "lane/.git/config carries an include", `f4` "--lane git hung", `f5`
   "lane/.git/objects/info/alternates present"). All verdict tokens and all `opens=` counts match.
3. **`exit=1` trailer.** Four of the five committed C1 receipts end with a literal `exit=1` line; the r44 one does
   not. That is a capture-wrapper convention, not counter output (the counter's last line is `PREDICATE C1 fail`);
   every run's real exit status is in its `ENVELOPE end … exit=` bracket.

## Drift observations for the L1 (outside the controls themselves)

1. **The freeze commit is not the tip; three post-freeze commits amend files the claims call frozen — and the
   amendment is now named in the claims.** `52d7486` set the C2 spec to 8 rows (`plans/pkg-spec-r45.json` − the
   `S157` `gitignore` row, `SPEC_SHA256 b8fc1e53… → 3eb696b4…`, `claims S149–S157 → S149–S156`); `9271dda` then
   landed the named amendment ("**Freeze amendments (pre-data, attempt 2, before landing).** … (1) … the tree was
   flattened to the r44 convention (`SHA256SUMS` rewritten, all 9 digests unchanged); (2) `plans/password_recovery_probe.py`
   … re-pointed at the flat names (the receipt it prints is unchanged: byte-identical on re-run, probe digest now
   `9363e03e`) …" — `plans/round-45-claims.md:32-34`) and re-pinned the C2 counter to
   `SPEC_SHA256 = 2f924ffae0b6d0a3346e23b106ec3d5ea03689222923e82509891238649e8244`; `8f9a898` landed the C1
   subject `plans/fixture_fence.py` (sha256 `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`).
   `0ac30a1`/`4290d64` staged w1 reports and the round sections; the tree is clean at tip.
   Consequence for control reproduction: the five C1 receipts and `control-c2-predictor.txt` are unchanged at tip
   (digests in §Evidence) and still reproduce; `control-c2-nothing.txt` (`476d19d0…`) is a pre-package receipt and
   is reproducible byte-identically **only** against the `52d7486` tree with its capture-time untracked set
   (§C2) — at tip the package exists and the execute-phase receipt staging (`6decc71`: "C2 execute-phase receipts
   - gate defects=0, counter A+B PREDICATE C2 pass") reports the passing direction instead.
2. **The amendment was in flight, as uncommitted working-tree edits, for part of this seat's run** (observed
   23:38–23:51 by `git status --porcelain`: `M plans/password_recovery_probe.py` `9363e03e…`, `M
   plans/round45_c2_verify.py` `86978416…` pinning `SPEC_SHA256 = 2f052896…` while `plans/pkg-spec-r45.json` was
   still `3eb696b4…`, five captures moved (`environment/Dockerfile`, `environment/setup.sh`, `solution/solve.sh`,
   `tests/test.sh`, `tests/test_outputs.py` → flat names, `M …/SHA256SUMS`), `M PROVINCE.md`, `M corpus/README.md`,
   `M corpus/SOURCES.md`). All of it is committed by `9271dda` with the spec now matching the counter pin
   (`2f924ffa…` both). My measurements used clones at commits and are unaffected.
3. **`~/.local/bin` content digest moved mid-session**: `c263b11afb1cccf6` (runs 23:29:49–23:36:45) →
   `e396f23e40a69201` (runs 23:36:43 onward), i.e. another seat's install (`OpenBot-0.51.1-x86_64.AppImage`,
   mtime 23:36; `agy.1793063119693176144.old`, 23:51). Not mine (no installs by this seat). Every individual
   envelope bracket was `before == after … unchanged`, so no measurement is invalid and no re-run was needed.

## Limits

- These controls bind the counter's calibration ladder, not `plans/fixture_fence.py`. The subject was absent at
  both commits measured (`b4fcd35`, `52d7486`); it landed later at `8f9a898` (sha256 `ac65c032…`). The four fence
  stubs are the ladder's rungs; nothing here says whether the landed fence passes `PREDICATE C1`.
- The two C2 "nothing" receipts are only byte-reproducible with the capture-time untracked set recreated; the
  frozen-claim sentence "measured on a clean clone of the landing tip" and a P9-carrying receipt therefore cannot
  both hold. Prefer the predicate lines, which are invariant.
- Host python3 (`/usr/bin/python3`) stood in for the image's uvx python throughout, as the probe's own limit states;
  V5's `dry_byte_equal=True` reproduced, so the frozen dry table is unaffected.

## Evidence (this dir: `.ufo/waves/round-45/w1/R45ExecControls/`)

| file | sha256 | what |
|---|---|---|
| `out-c1-nothing.txt` | `4212d1fab688c018fde3f36946fe69fe0c59e60388b24fe19dd90a99181aa406` | C1 nothing control, envelope brackets |
| `out-c1-r44.txt` | `3b44dab4e3854ff761212368bcfa1ed33d8e6bb3b5904c6e61b52d696cdb9c77` | C1 r44-fence control (contradicted=7) |
| `out-c1-r44-run2.txt` | `91d289968fd46b0c0cb97d6f26dd63aae23258b0190a07c73c4064d635b70f3c` | determinism re-run |
| `out-c1-admit.txt` | `371ccb72fb41ea24b1006a025df1c8c99d50e6d11349a8724d687c6dd3b680c7` | admit_all control |
| `out-c1-refuse.txt` | `1f23f35cb24a82d41075c4b25eaefbaa2656ddd8855f202d5abd62ba7bc14ecc` | refuse_all control |
| `out-c1-static.txt` | `fab79ec5ffdc48ab3a8de89899b8d4f14381e275a2beeccd8799db67e0dc5c4b` | static_only control |
| `out-c1-nothing-head.txt` | `b9b84a723d6cb0f4c31ecc147c806f4fc34e09c9afdc2bd1d3b526ad77587b53` | C1 on `52d7486` clone (instrument unchanged) |
| `out-c2-freeze.txt` | `9ff71003b5bc29861f7fc38f10a8a8b2dca5780924a40badabc1bdd4988e49c5` | C2 nothing, freeze counter+clone, clean tree |
| `out-c2-head.txt` | `d87cd8e7482459f82df036277c91fc6034f2df9870c21010f06cebc7ec06d146` | C2 nothing, HEAD counter+clone, clean tree |
| `out-c2-untracked.txt` | `488143de8e5c4a6efe49c225f7aae17c0f2904e0321ebf175e80165d303bfd11` | byte-identical to `control-c2-nothing.txt` (6 untracked) |
| `out-c2-freeze-u151.txt` | `2824c8fdab5cd92106d4cb721a3109c87dc691ea5da697e9d09897f92731c76e` | byte-identical to the `b4fcd35` receipt (151 untracked) |
| `c2-committed-freeze.txt` | `c4ec1bf6a5ee501c0a22ebc0ba5bbc4c09dfd4bdfd01643f4388901ddb2add47` | `git show b4fcd35:.ufo/waves/round-45/claims/control-c2-nothing.txt` |
| `out-predictor-freeze.txt` | `bd5dd2596b597aa14974942343777f8b60cfdba5d8092e6488728e1f215d4c81` | V11 red-as-required, freeze clone |
| `out-predictor-head.txt` | `0b74d83ef59d0bf418a1aa371f740b08e2c3b1af61bfad197acf7b78dc628c1d` | same on `52d7486` |
| `compare.sh` | `ce0023a2a0c346d9600374d22a09c3d1d861b842292f6403cf948dae2e98eb13` | the comparison harness |
| `compare-out.txt` | `b98da7b523be8af1849c6b045334b8b0361be005c9e43676c0e0dc0c7e8189fc` | its output: `RESULT controls mismatched=0` |

Committed receipts compared against (for the record): `control-c1-nothing.txt` `453e08d0…`, `control-c1-fence-r44.txt`
`5a63170f…`, `control-c1-fence-admit_all.txt` `1e1c733b…`, `control-c1-fence-refuse_all.txt` `314ce3c6…`,
`control-c1-fence-static_only.txt` `f4b743b5…`, `control-c2-nothing.txt` `476d19d0…`,
`control-c2-predictor.txt` `3361ef17…`.

## Envelope brackets (QUALITY Q32)

```
out-c1-nothing      start 23:29:49 cwd=/home/vgpnk/Projects/shokunin  end 23:29:57 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
out-c1-r44          start 23:31:10 cwd=/home/vgpnk/Projects/shokunin  end 23:31:46 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
out-c1-admit        start 23:32:46 cwd=/home/vgpnk/Projects/shokunin  end 23:32:53 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
out-c1-refuse       start 23:33:04 cwd=/home/vgpnk/Projects/shokunin  end 23:33:11 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
out-c1-static       start 23:33:16 cwd=/home/vgpnk/Projects/shokunin  end 23:33:23 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
out-c2-freeze       start 23:35:48 cwd=/home/vgpnk/Projects/shokunin  end 23:35:51 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
out-c2-head         start 23:36:26 cwd=/home/vgpnk/Projects/shokunin  end 23:36:29 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
out-predictor-freeze start 23:36:43 cwd=$S/lane            end 23:36:45 exit=0 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
out-predictor-head   start 23:37:58 cwd=$S/lane-head       end 23:37:59 exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
out-c1-r44-run2     start 23:38:01 cwd=/home/vgpnk/Projects/shokunin  end 23:38:37 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
out-c2-untracked    start 23:43:44 cwd=$S                   end 23:43:46 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
out-c2-freeze-u151  start 23:45:22 cwd=$S                   end 23:45:24 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
out-c1-nothing-head start 23:41:07 cwd=$S                   end 23:41:14 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```
No bracket reports `CHANGED`; no measurement was invalidated; the digest shift inside the session is §Drift 3.

VERDICT: controls-reproduced-7/7-drift-0
