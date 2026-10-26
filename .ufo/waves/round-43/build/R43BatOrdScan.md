# R43BatOrdScan — battery43 `o_scan` (order gate): NO5, NO22 killed attributably

Round 43 wave 1, kengaku. Lane clone `/fast/scratch/hyaku/kengaku-r43/R43BatOrdScan/lane` at
`d33350fdb01ce27cbff47b04642fd2c1471e5c26` (`git rev-parse --show-toplevel` = the clone, verified before any write).
Frozen mutants read from `plans/round43_c1_verify.py:245-259`; nothing frozen was edited.

**Deliverable:** `.ufo/waves/round-43/build/R43BatOrdScan/battery/o_scan.py`
sha256 `6ddcdbb8ca3075f119bf8a3fe662a67b22637be243645bc145e7439a0314f38c`, 146 lines, no imports, no
`SIDECHANNEL` token (checked by a lowercase substring scan of the module against the counter's 28-token tuple:
`TOKEN-HITS []`). Six fixtures, every fid prefixed `o_scan-`.

## 1. What each frozen mutant changes, and the direction claimed

| id | tool branch | `old -> new` (counter lines) | direction | fixture expectation |
|---|---|---|---|---|
| NO5 | `scan_claims`, `plans/order_check.py:120` | `    for commit in commits:` -> `    for commit in commits[:1]:` (`round43_c1_verify.py:248-249`) | `rc-silence` | `reject`, `defects []`, reference rc 1 / mutant rc 0 |
| NO22 | `blob_hits`, `plans/order_check.py:105-106` | `        if m:` -> `        if False:` (`round43_c1_verify.py:258-259`) | `rc-silence` | `reject`, `defects []`, reference rc 1 / mutant rc 0 |

Claim text the mutants bear on: `order_check.py:14-16` "FAIL when any file committed under
`.ufo/waves/round-NN/claims/` at or before the first commit that adds <receipt> proves the probe executed" and
`order_check.py:15-16` "a gate `P10` line whose detail is anything other than `receipt unreadable`".

## 2. The six fixtures (one line each; `build` fills an empty dir and returns the argv tail)

The lane repository **is** the fixture directory (`ctx.init(d)`) and the gate is called with `--lane .`, so the
gate resolves its root at the fixture dir, not at a subdirectory. Claims `plans/round-43-claims.md`, receipt
`corpus/evidence/round43/probe.txt`, evidence under `.ufo/waves/round-43/claims/`.

| fid | what it demonstrates |
|---|---|
| `o_scan-n5a-late-gate-file` | NO5: `P10 ok fresh probe output is byte-equal to the receipt` enters as a NEW claims artefact in the second claims commit while the freeze commit and its two siblings stay clean |
| `o_scan-n5b-amended-claims` | NO5: five commits, one artefact rewritten twice — `P10 DEFECT fresh probe output is not byte-equal to the receipt` only in the third-commit blob, a clean artefact fourth, receipt last |
| `o_scan-n5c-case-third-commit` | NO5, second trigger of the same branch: a receipt-shaped `CASE r43-a1 observed=PASS wrong=0` line in the third claims commit (the `case-observed` pattern, not `gate-p10`) |
| `o_scan-n22a-gate-only` | NO22: the only forbidden evidence is a `P10 ok` line in a sibling gate log inside the freeze commit; no `CASE` line anywhere, so only the gate-line branch can reject |
| `o_scan-n22b-echoed-defect` | NO22, second trigger: `gate: P10 DEFECT fresh probe exit=1` (echo prefix + DEFECT variant) in a claims artefact of the freeze commit, receipt in its own later commit |
| `o_scan-n22c-indented-gate` | NO22: an indented `  P10 ok receipt matches the committed bytes` under a heading in the freeze commit, plus a later clean claims commit |

## 3. Development run — this is the required command, verbatim output

```
python3 plans/round43_c1_verify.py --lane "$S/lane" \
  --battery-dir .../round-43/build/R43BatOrdScan/battery --only NO5,NO22 --work "$S/w"
```
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43BatOrdScan/env /fast/scratch/hyaku/kengaku-r43/R43BatOrdScan/env --bind /fast/scratch/hyaku/kengaku-r43/R43BatOrdScan/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r43/R43BatOrdScan/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43BatOrdScan/battery --only NO5,NO22 --work /fast/scratch/hyaku/kengaku-r43/R43BatOrdScan/w
ENVELOPE start 19:12:19 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE o_scan-n5a-late-gate-file tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_scan-n5b-amended-claims tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_scan-n5c-case-third-commit tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_scan-n22a-gate-only tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_scan-n22b-echoed-defect tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_scan-n22c-indented-gate tool=order expect=reject declared=- observed_rc=1 observed=- ok
MUTANT NO5 order rc-silence killed by=o_scan-n5a-late-gate-file attributed=L120 value=differs hits=3 -- plans/order_check.py:14-16 'FAIL when any file committed under `.ufo/waves/round-NN/claims
MUTANT NO22 order rc-silence killed by=o_scan-n5a-late-gate-file attributed=L105 value=differs hits=5 -- plans/order_check.py:15-16 'a gate `P10` line whose detail is anything other than `receipt
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=2/2
ADVERTISED direct=2 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:12:21 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
Every FIXTURE line `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0 unattributed=0`, and both mutants
`killed ... attributed=L… value=differs` — the predicate of this seat (k/2, wrong) is met with k=2, wrong=0.
Receipt: `receipts/final.txt` (first block).

## 4. Full default counter (module copied to `"$S/lane/plans/battery43/o_scan.py"`)

```
python3 plans/round43_c1_verify.py --lane "$S/lane" --work "$S/w3"
```
```
ENVELOPE start 19:12:23 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE o_scan-n5a-late-gate-file tool=order expect=reject declared=- observed_rc=1 observed=- ok
... (all six FIXTURE lines ok, identical to §3)
MUTANT NA1 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have 
MUTANT NA5 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:54-56 'The task component of `<subpath>` is matched **exactly
MUTANT NA7 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:112-113 'no 64-hex token on it may be outside A unless it is 
MUTANT NA18 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:53-54 'a `raw.githubusercontent.com/<owner>/<repo>/<commit>/<
MUTANT NA20 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:108-110 'An erratum for S<id> exempts that row's anchor token
MUTANT NA21 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:108-109 'An erratum for S<id> exempts that row's anchor token
MUTANT NO5 order rc-silence killed by=o_scan-n5a-late-gate-file attributed=L120 value=differs hits=3 -- plans/order_check.py:14-16 'FAIL when any file committed under `.ufo/waves/round-NN/claims
MUTANT NO7 order rc-mirror SURVIVED exhibits=none -- plans/order_check.py:56-57 'The one P10 detail the gate prints before executing anything, 
MUTANT NO22 order rc-silence killed by=o_scan-n5a-late-gate-file attributed=L105 value=differs hits=5 -- plans/order_check.py:15-16 'a gate `P10` line whose detail is anything other than `receipt
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=2 survived=7 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/6 order=2/3
ADVERTISED direct=8 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 19:12:25 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
As expected for one of three order seats plus the anchor battery: the six anchor mutants and NO7 survive (other
wave-1 seats own them), `wrong=0` and `sidechannel=0` hold, and the failure is `killed=2`, not a fixture defect.
Receipt: `receipts/final.txt` (second block).

## 5. Load-bearing table (each fixture removed in turn, each fixture alone, each family removed)

All runs: `--only NO5,NO22`, same envelope, every one ending
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`. Receipts:
`receipts/loadbearing2.txt` (8 runs), `receipts/isolated2.txt` (6 runs).

**Each fixture ALONE in the battery (1 fixture) — which mutant it kills:**

| battery | NO5 | NO22 |
|---|---|---|
| `o_scan-n5a-late-gate-file` | killed by=n5a (hits=1) | killed by=n5a (hits=1) |
| `o_scan-n5b-amended-claims` | killed by=n5b (hits=1) | killed by=n5b (hits=1) |
| `o_scan-n5c-case-third-commit` | killed by=n5c (hits=1) | **SURVIVED** `exhibits=none` |
| `o_scan-n22a-gate-only` | **SURVIVED** `exhibits=none` | killed by=n22a (hits=1) |
| `o_scan-n22b-echoed-defect` | **SURVIVED** `exhibits=none` | killed by=n22b (hits=1) |
| `o_scan-n22c-indented-gate` | **SURVIVED** `exhibits=none` | killed by=n22c (hits=1) |

Every fixture therefore exhibits its declared direction on its own; the SURVIVED cells are the expected branch
structure, not defects — NO22 keeps the `CASE` branch that n5c exercises, and NO5's `commits[:1]` still reads the
freeze commit's blobs, so single-commit evidence is never a `rc-silence` hit for it.

**One fixture removed (5 remain) — no mutant flips, in any of the six runs:** every run printed
`MUTANTS total=2 killed=2 survived=0`. Removing n22a/n22b/n22c leaves both killed by `o_scan-n5a`; removing
n5a/n5b/n5c leaves both killed by `o_scan-n5a` (n5b/n5c) or by `o_scan-n5b` (n5a). **Family removal:** the NO5
family removed (`n22*` only) → `MUTANT NO5 order rc-silence SURVIVED exhibits=none` and NO22 killed by
`o_scan-n22a`; the NO22 family removed (`n5*` only) → both killed by `o_scan-n5a`.

Reading: the NO5 family is load-bearing for NO5 (removing all three flips it to SURVIVED, with no confusion about
which direction was measured), the NO22 family independently demonstrates NO22, and no fixture is individually
necessary because each neighbour in the family covers the same kill. That redundancy is deliberate: `n5c` uses the
`case-observed` pattern, `n5a`/`n5b` the `gate-p10` pattern, and `n22a`/`n22b`/`n22c` differ in echo prefix,
`DEFECT`/`ok` variant and indentation.

## 6. Non-re-spelling of the pre-freeze direction module

`claims/witness/w_near.py` was read only to learn reachability (§its `w2_late_claims_edit` uses round-42 paths,
repo `d/lane`, absolute `--lane str(repo)`, one edit of an existing claims file in the second commit, detail
`P10 DEFECT fresh probe exit=1 cases=16`; its other order fixture is the `receipt unreadable` accept case). My
fixtures differ structurally: repo is the fixture directory itself with `--lane .` and repo-relative
claims/receipt; NO5 shapes are a new artefact in commit 2, a five-commit double rewrite with a third detail form
(`fresh probe output is not byte-equal`), and a `CASE` line in commit 3; NO22 shapes are `P10 ok` in a sibling log,
the echoed `gate: P10 DEFECT fresh probe exit=1`, and an indented `P10 ok`. Nothing is imported, copied or read at
build time.

## 7. Limits hit (all measured here)

1. **The gate reads only `.ufo/waves/round-NN/claims/` blobs, not the claims file.** My first `n5b`/`n22b` drafts put
   the forbidden line in `plans/round-43-claims.md`; the reference exited **0** on both (`FIXTURE
   o_scan-n5b-amended-claims ... observed_rc=0 ... WRONG`, `o_scan-n22b-echoed-defect ... observed_rc=0 ... WRONG`,
   `receipts/devrun.txt`). This is the tool's documented scope (`order_check.py:14-15` names only files "committed
   under `.ufo/waves/round-NN/claims/`"), but a reader who assumes the claims file itself is scanned would be wrong.
   Both fixtures were rewritten to keep the evidence inside the claims directory; no frozen file was touched.
2. **Per-fixture minimality is unavailable for this tool pair:** no single removal flips a mutant (§5), so "which
   fixture is load-bearing" is answered at family granularity only.
3. **Cross-kill asymmetry is real and one-directional:** the `n22*` family can never kill NO5 (single-commit evidence
   is inside `commits[:1]`), while `n5a`/`n5b` also kill NO22 because their `P10` lines survive the `CASE` branch.
   A seat reading only NO22's kill would over-credit `n5a`; §5 separates the two.
4. **`hits=` is not per-fixture attribution:** the counter prints only the killing fid, so which of the 3-5 hits a
   given fixture produced is only recoverable by the single-fixture battery in §5.
5. **Envelope-nested `bwrap`:** all 32 counter runs went through `claims/envelope.sh` and every one ended
   `unchanged`; the nested inner `bwrap --ro-bind / /` worked (the counter's own isolation legs, including leg h and
   leg i, ran on every fixture — `leg i` accepted all six because `--claims`/`--receipt` are blobs at HEAD).
6. No tool install was needed; nothing was written to `~/.local/bin`, `/usr`, `/etc` or `$HOME`; the lane
   repository, its corpus/plans/SCORECARD/LOG and its git index were not touched (only the scratch clone's
   `plans/battery43/` was populated).

## 8. Commands (reproduce)

```
S=/fast/scratch/hyaku/kengaku-r43/R43BatOrdScan; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel          # -> $S/lane
claims/envelope.sh "$S/env" python3 plans/round43_c1_verify.py --lane "$S/lane" \
  --battery-dir .ufo/waves/round-43/build/R43BatOrdScan/battery --only NO5,NO22 --work "$S/w"
cp .ufo/waves/round-43/build/R43BatOrdScan/battery/o_scan.py "$S/lane/plans/battery43/"
claims/envelope.sh "$S/env" python3 plans/round43_c1_verify.py --lane "$S/lane" --work "$S/w3"
```

VERDICT: battery43-o_scan-killed-2/2-wrong-0
