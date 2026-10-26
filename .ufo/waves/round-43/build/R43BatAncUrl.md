# R43BatAncUrl — battery43 module `a_url` (C1: attributed kills for NA5 and NA18)

Seat: executor, kengaku round 43 wave 1 (hyaku run 9, 2026-10-26). Lane: `kengaku-shokunin`.
Scope: one new battery module under `.ufo/waves/round-43/build/R43BatAncUrl/battery/`; no lane file edited, no tool,
counter, probe, spec, gate, capture, receipt or `.ufo/waves/round-43/claims/` file touched.

## Deliverable

- `.ufo/waves/round-43/build/R43BatAncUrl/battery/a_url.py` — 7884 bytes, sha256
  `6a3d4732162c46a4eeabf8f5274860cab5373ffa6eabfa16a5c259524697e5fd`; stdlib only (`hashlib`); four fixtures, every
  fid prefixed `a_url-`; one-line comment per fixture naming what it demonstrates.
  (The L1 copies it to `plans/battery43/a_url.py`; I ran exactly that copy in a clone at
  `$S/lane/plans/battery43/a_url.py`, same digest.)

Contract compliance: module-level `FIXTURES` with `fid`, `tool="anchor"`, `expect="accept"`, `defects=[]` (the
unmodified tool prints no `DEFECT` line on any of the four builds — measured, see `observed=- observed_rc=0`), and
`build(ctx, d)` filling the empty directory and returning `["--lane", str(repo)]`. Every repo is built from nothing
with `ctx.init` / `ctx.write` / `ctx.git` (no lane clone, no pre-existing repository read); every path lies inside the
fixture directory; no symlink is created. Sidechannel scan: a direct scan of the module text (lowercased) against the
counter's 27 tokens prints `[]` (no hit); note the near-miss avoided — an evidence directory named `round…` contains
the token `/run`, so the fixtures use `ev1`–`ev4`.

| fid | mutant | shape | trigger branch |
|---|---|---|---|
| `a_url-org-slash-single` | NA5 | one row, one capture, `task.toml` `name = "satellite-works/orbit-ring"`, no manifest | the slug assignment at anchor_digest_check.py:258; a whole-slug keeps the org prefix, the URL's task component never matches → `anchor-unbound` |
| `a_url-org-slash-registry` | NA5 | two-row registry over three commits (captures / SHA256SUMS / SOURCES), one plain task bound by its own long URL beside the slashed task, both digests also manifest-listed | same assignment, second shape |
| `a_url-short-commit-pair` | NA18 | one green row bound by a 40-hex URL, its teaches cell also carries a 5-hex-commit URL whose basename exists in a second task directory | `URL_RAW` 7→4 hex floor (L154): the widened pattern binds a second capture the row never anchored → `capture-unanchored` |
| `a_url-short-commit-shadow` | NA18 | row bound by an explicit `corpus/evidence/ev4/bundle/claim.txt` lane path, plus a 5-hex-commit URL naming a capture under `tb2-spline-diff` | same line, other failure shape: the URL now wins the binding, so the token becomes a `digest-wrong-capture` |

Directions are the frozen ones: both mutants are `rc-mirror`, fixture `expect=accept`, reference exit 0, mutant exit 1.

## Evidence 1 — development run (`--only NA5,NA18`), inside the round-43 envelope

```
$ /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/envelope.sh "$S/env" \
    python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py \
      --lane "$S/lane" --battery-dir <deliverable battery dir> --only NA5,NA18 --work "$S/w"
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43BatAncUrl/env /fast/scratch/hyaku/kengaku-r43/R43BatAncUrl/env --bind /fast/scratch/hyaku/kengaku-r43/R43BatAncUrl/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 .../plans/round43_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r43/R43BatAncUrl/lane --battery-dir .../round-43/build/R43BatAncUrl/battery --only NA5,NA18 --work /fast/scratch/hyaku/kengaku-r43/R43BatAncUrl/w
ENVELOPE start 19:09:49 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE a_url-org-slash-single tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_url-org-slash-registry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_url-short-commit-pair tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_url-short-commit-shadow tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT NA5 anchor rc-mirror killed by=a_url-org-slash-single attributed=L258 value=differs hits=2 -- plans/anchor_digest_check.py:54-56 'The task component of `<subpath>` is matched **exactly
MUTANT NA18 anchor rc-mirror killed by=a_url-short-commit-pair attributed=L154 value=differs hits=2 -- plans/anchor_digest_check.py:53-54 'a `raw.githubusercontent.com/<owner>/<repo>/<commit>/<
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=2/2 order=0/0
ADVERTISED direct=1 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:09:51 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Receipt file: `build/R43BatAncUrl/receipt-only-na5-na18.txt`. The same command was run twice (first at 19:08:48); every
line above except the two `ENVELOPE` timestamps was identical (`hits=2` both times). `attributed=L258` and
`attributed=L154` are the replaced-span lines, and `value=differs` is leg g (the site record differs from the
reference's).

## Evidence 2 — load-bearing table (each fixture removed in turn)

Six scratch batteries, each the deliverable with one entry dropped (or only one mutant's pair kept), run with the same
`--only NA5,NA18` and the envelope. Receipt: `build/R43BatAncUrl/receipt-loadbearing.txt`.

| battery | NA5 | NA18 | `BATTERY … wrong=0 tampered=0 sidechannel=0` |
|---|---|---|---|
| `no-a_url-org-slash-single` | killed by `a_url-org-slash-registry` (L258, hits=1) | killed by `a_url-short-commit-pair` (L154, hits=2) | yes, fixtures=3 |
| `no-a_url-org-slash-registry` | killed by `a_url-org-slash-single` (L258, hits=1) | killed by `a_url-short-commit-pair` (L154, hits=2) | yes, fixtures=3 |
| `no-a_url-short-commit-pair` | killed by `a_url-org-slash-single` (L258, hits=2) | killed by `a_url-short-commit-shadow` (L154, hits=1) | yes, fixtures=3 |
| `no-a_url-short-commit-shadow` | killed by `a_url-org-slash-single` (L258, hits=2) | killed by `a_url-short-commit-pair` (L154, hits=1) | yes, fixtures=3 |
| `only-na5` (both NA18 fixtures dropped) | killed by `a_url-org-slash-single` (hits=2) | **SURVIVED exhibits=none** | yes, fixtures=2 |
| `only-na18` (both NA5 fixtures dropped) | **SURVIVED exhibits=none** | killed by `a_url-short-commit-pair` (hits=2) | yes, fixtures=2 |

Each mutant has two independent witnesses (removing either leaves the other killing it) and each mutant's kill
disappears exactly when both of its fixtures are absent, so no fixture is incidental and no mutant is killed by
another mutant's fixture. Representative lines:

```
########## battery = only no-a_url-org-slash-single
MUTANT NA5 anchor rc-mirror killed by=a_url-org-slash-registry attributed=L258 value=differs hits=1 -- ...
MUTANT NA18 anchor rc-mirror killed by=a_url-short-commit-pair attributed=L154 value=differs hits=2 -- ...
########## battery = only only-na5
MUTANT NA5 anchor rc-mirror killed by=a_url-org-slash-single attributed=L258 value=differs hits=2 -- ...
MUTANT NA18 anchor rc-mirror SURVIVED exhibits=none -- ...
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0 unattributed=0
ENVELOPE end 19:10:13 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

## Evidence 3 — full default counter with the module in `plans/battery43/`

```
$ cp build/R43BatAncUrl/battery/a_url.py "$S/lane/plans/battery43/a_url.py"   # sha256 6a3d4732…
$ envelope.sh "$S/env" python3 .../plans/round43_c1_verify.py --lane "$S/lane" --work "$S/w2"
ENVELOPE start 19:10:15 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE a_url-org-slash-single tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_url-org-slash-registry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_url-short-commit-pair tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_url-short-commit-shadow tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT NA1 anchor silence SURVIVED exhibits=none -- ...:34-35 ...
MUTANT NA5 anchor rc-mirror killed by=a_url-org-slash-single attributed=L258 value=differs hits=2 -- ...:54-56 ...
MUTANT NA7 anchor rc-mirror SURVIVED exhibits=none -- ...:112-113 ...
MUTANT NA18 anchor rc-mirror killed by=a_url-short-commit-pair attributed=L154 value=differs hits=2 -- ...:53-54 ...
MUTANT NA20 anchor rc-mirror SURVIVED exhibits=none -- ...:108-110 ...
MUTANT NA21 anchor rc-mirror SURVIVED exhibits=none -- ...:108-109 ...
MUTANT NO5 order rc-silence SURVIVED exhibits=none -- ...order_check.py:14-16 ...
MUTANT NO7 order rc-mirror SURVIVED exhibits=none -- ...:56-57 ...
MUTANT NO22 order rc-silence SURVIVED exhibits=none -- ...:15-16 ...
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=2 survived=7 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=2/6 order=0/3
ADVERTISED direct=8 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 19:10:17 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Receipt: `build/R43BatAncUrl/receipt-full-c1.txt`. In the default (predicate) mode my module contributes NA5 and NA18
(correctly `killed` with `value=differs`); the other seven are other wave-1 seats' mutants and survive this module's
battery alone, exactly as expected. The seven surviving lines name `exports=none`, i.e. no wrong-direction hit was
mislabelled as a kill. `PINS-AFTER mismatched=0`: the tools were unchanged by every run.

Environment: host `Python 3.14.8`, `/usr/bin/bwrap`; envelope digest `328be01808ba022f` before and after every run
(`unchanged`), so no measurement was invalidated. Nothing was installed or upgraded (no pacman, uv, npm or binary
fetch was needed).

## Limits hit / named

1. The load-bearing control is fixture-level, not counter-level: with all four fixtures `NA5`/`NA18` survive, but the
   counter cannot tell whether a kill needed the fixture's *intent* or only its shape; leg f/g attribute the span and
   the site record, not the prose.
2. `hits=2` on both mutants in the primary run means both fixtures of a pair exhibit the direction; the
   single-removal table above is what separates "killed by A" from "killed by B".
3. The two NA18 fixtures reach the widened-commit branch through different consequences (`capture-unanchored` vs
   `digest-wrong-capture`); the counter records only exit codes for `order` and the class set for `anchor` on the
   *reference*, so a mutant-side class difference is visible only in the direction, not in the receipt.
4. The slug route exercised here is the `task.toml` route; NA5's mutated line is also reached when no `task.toml`
   exists, but with an empty `slugs` map it changes nothing observable — my fixtures always commit a `task.toml`, which
   is the only reachable shape, so I record that as a property of the branch rather than a separate fixture.
5. Fixture `a_url-org-slash-registry` commits `SHA256SUMS` in a commit *after* the captures, so the manifest route
   exercised is a HEAD manifest; a manifest staged but not committed (`--evidence-ref index`) and a manifest that
   lists a stale digest are different shapes and are not exercised here.

VERDICT: battery43-a_url-killed-2/2-wrong-0
