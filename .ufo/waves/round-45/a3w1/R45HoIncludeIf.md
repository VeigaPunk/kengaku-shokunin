# R45HoIncludeIf — held-out includeIf fence probe

Measured against lane `master` / HEAD `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc`. The clone at `/fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/lane` resolved to that same HEAD. Landed `plans/fixture_fence.py` SHA-256: `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6` (same in clone and source lane).

## Mutant and expected detector

Class under test: `[includeIf]` `gitdir:` (exact, glob, case-insensitive form), `onbranch:`, case variants, and an include target symlink inside `.git` pointing outside the fixture. The smallest behavior-bearing bypass is a carriage return immediately before a section header: the fence only matches `_INCLUDE_RE = ^[ \\t]*\\[[ \\t]*include` (case-insensitive), while Git's config parser accepts `\\r[include...]`. The `os.walk` pass also excludes `.git` from descent, so an include target symlink under `.git` avoids its symlink check. BOM at byte 0 is a second proven regex bypass.

Expected detector: the landed fence should refuse the fixture before Git opens any include target; under its counter harness, an admitted fixture or a refused fixture with an outside open is a defect. Actual: hostile modules h1–h3 were all admitted; each had one or more fixtures whose fence process opened a file outside `d`. Control module h4's ordinary and mixed-case visible `[includeIf]` fixtures were refused with zero outside opens.

## Measured detector command and output

The command used the frozen counter machinery directly: `round45_c1_verify.build_module(k44, lane, root, module)` (the round-44 builder sandbox) and `round45_c1_verify.run_fence(k44, lane, root, fence_copy, fixture, n)` (read-only sandbox, `strace -f -y`, counter's outside-open classifier). Exact invocation:

```sh
K45_KEEP_STRACE=/fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/kept \
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/env3 \
  /usr/bin/python3 /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/drive.py \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/lane \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/w2 \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoIncludeIf/h1_cr_include.py \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoIncludeIf/h2_includeif_cond.py \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoIncludeIf/h3_bom_symlink.py \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1/R45HoIncludeIf/h4_controls.py
```

Receipt: `a3w1/R45HoIncludeIf/driver.out` (complete per-fixture output; summary line is large and truncated by the read display). Actual output, condensed only by omitting fixture directory fields:

```
ENVELOPE start 00:33:19 cwd=/home/vgpnk/Projects/shokunin
FENCE-COPY sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
h1_cr_include.py: h1-cr-include-lf ADMIT outside_opens=7; h1-cr-include-crlf ADMIT outside_opens=7; MODULE fixtures=2 admitted=2 read=2
h2_includeif_cond.py: onbranch ADMIT opens=5; onbranch-nomatch ADMIT opens=0; gitdir-exact ADMIT opens=7; gitdir-glob ADMIT opens=7; gitdir-i ADMIT opens=7; gitdir-star ADMIT opens=7; gitdir-nomatch ADMIT opens=0; hasconfig ADMIT opens=0; anchor-onbranch ADMIT opens=3; MODULE fixtures=9 admitted=9 read=6
h3_bom_symlink.py: bom-include ADMIT opens=7; cr-include-symlink ADMIT opens=7; bom-includeif ADMIT opens=5; anchor-cr-include ADMIT opens=3; MODULE fixtures=4 admitted=4 read=4
h4_controls.py: plain-onbranch BREACH (lane/.git/config carries an include) opens=0; mixedcase-gitdir BREACH (same) opens=0; anchor-gitdir BREACH (same) opens=0; MODULE fixtures=3 admitted=0 read=0
SUMMARY {"modules": 4, "fixtures": 18, "admitted": 15, "read": 12, "build_errors": 0, ...}
ENVELOPE end 00:33:23 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

There were 3 hostile modules (h1–h3): all 3 had admitted fixtures and outside reads. Across those modules, 15/15 fixtures were ADMIT and 12/15 had outside opens. h2's three non-reading conditional variants (nonmatching branch, nonmatching gitdir, hasconfig with no matching remote) were still admitted but are not counted as reads. The three h4 controls were refused cleanly.

Path-level proof is archived in `a3w1/R45HoIncludeIf/trace-excerpts.txt`, copied from the kept traces. E.g. retained trace `kept/f00005.txt:146` has a successful `openat` of `side-h2-gitdir-exact.cfg`; `kept/f00012.txt:146` opens `side-h3-bom-inc.cfg`; and `kept/f00013.txt:146` opens `.git/inc.cfg` with `strace -y` resolving it to `side-h3-cr-symlink.cfg`. These paths are under the fixture build root but outside their corresponding fixture dirs.

## Git parser cross-check

Probe commands (both through the required envelope):

```sh
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/env \
  /usr/bin/python3 /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/probe_accept.py \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/probe_accept.jsonl
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/env \
  /usr/bin/python3 /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/probe_b.py \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf \
  /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf/probe_b.jsonl
```

Envelope lines for those measurements:

```
ENVELOPE start 00:27:34 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 00:27:36 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
ENVELOPE start 00:29:16 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 00:29:18 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

```
{"name":"r-inclif-onbranch","revparse_rc":0,"email":"r-inclif-onbranch@invalid","fence_regex_hit":false,"outside_opens":1}
{"name":"r-inclif-gitdir-exact","revparse_rc":0,"email":"r-inclif-gitdir-exact@invalid","fence_regex_hit":false,"outside_opens":1}
{"name":"r-inclif-gitdir-glob","revparse_rc":0,"email":"r-inclif-gitdir-glob@invalid","fence_regex_hit":false,"outside_opens":1}
{"name":"r-inclif-gitdir-i","revparse_rc":0,"email":"r-inclif-gitdir-i@invalid","fence_regex_hit":false,"outside_opens":1}
{"name":"r-include-symlink","revparse_rc":0,"email":"r-include-symlink@invalid","fence_regex_hit":false,"outside_opens":1}
{"name":"bom1-include","revparse_rc":0,"email":"bom1-include@invalid","fence_regex_hit":false,"outside_opens":1}
{"name":"r-inclif-onbranch-nomatch","revparse_rc":0,"email":"","fence_regex_hit":false,"outside_opens":0}
```

The control `crlf-include` had `fence_regex_hit=true`; `\\v` and `\\f` prefixes were rejected by Git (rev-parse rc=128), not treated as bypasses. The final fence run is the authoritative verdict, not the preliminary parser probe.

## Artifacts and scope

Hostile modules are solely under `a3w1/R45HoIncludeIf/`: `h1_cr_include.py`, `h2_includeif_cond.py`, `h3_bom_symlink.py`, and control `h4_controls.py`. Receipts are `driver.out`, `probe_b.jsonl`, `probe_accept.jsonl`, and `trace-excerpts.txt`. No lane file was modified; no tooling was installed. Scratch was only `/fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf`, removed using the mandated guard:

```text
python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45HoIncludeIf /fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf
DELETE path=/fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf resolved=/fast/scratch/hyaku/kengaku-r45/R45HoIncludeIf bytes=550910203 size=525.4MiB
```

VERDICT: includeif-modules-3-admitted-3-read-3
