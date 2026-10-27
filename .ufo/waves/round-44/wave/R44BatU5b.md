# R44BatU5b — battery44 module for frozen mutant U5 (`anchor`, `digest-short`, `silence`)

Leaf executor seat, round 44 (kengaku hyaku run 9, 2026-10-26), one v2 wave. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at tip `5e3d3aa`; frozen claims read in full (`plans/round-44-claims.md`). Nothing frozen was edited; no lane file, corpus file, plans file or git index was touched (all development ran in a `--shared` clone at `/fast/scratch/hyaku/kengaku-r44/R44BatU5b/lane`).

## Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU5b/battery/u5_short_b.py` — stdlib only (`hashlib`), 7269 bytes, sha256 `eff6edf8b407753c19dd70a825eaeb5889244cc308af70019fa17a4addeec86d`. Four anchor fixtures, every fid prefixed `u5_short_b-`, each declaring `expect=reject` and `defects=["digest-short"]`. Copy target for the L1: `plans/battery44/u5_short_b.py`.

Mutant read from `plans/round44_c1_verify.py:231-235`: `U5 anchor digest-short silence direct`, `old -> new` `cls, why = ("digest-short" if len(tok) < 64 else "digest-long")` → `cls, why = ("digest-long" if len(tok) < 64 else "digest-long")`. Advertising sentence: `plans/anchor_digest_check.py:88` "any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`". The mutated branch is `check()`'s token-length arm; the fixtures all reach it with a token of 8–63 lowercase hex digits and **no** ellipsis, so the unmodified tool prints `class=digest-short` on a bound row.

| fid | shape it demonstrates (one line) | binding route | token |
|---|---|---|---|
| `u5_short_b-registry-url-task` | six-row registry, short token sits in a row bound by a pinned upstream URL among clean and tokenless rows | `url-task` (task.toml slug + raw URL) | 63 hex (boundary just under 64) |
| `u5_short_b-index-ref-staged` | minimal two-row registry read with `--evidence-ref index`, token names a capture that is staged only (uncommitted) | `row-path` against the index blob | 8 hex (`0badc0de`) |
| `u5_short_b-lane-path-manifest` | nine rows read with `--verbose`; a stale `SHA256SUMS` entry is accepted in the same registry that carries the short token | `row-path` + manifest (`dir_entries`) | 40 hex |
| `u5_short_b-history-truncation` | two-commit history: the anchored row is correct at commit 1, a later review commit truncates the token | `row-path` | 20 hex (= first 20 of the true digest) |

Every fixture builds from nothing through `ctx.init/write/git` inside its own empty directory; no lane clone, no copy of the direction module under `.ufo/waves/round-44/claims/witness/` was imported, copied, read or re-spelled (independence is by construction: the four shapes above are registry/binding shapes, not a transcription of any prior fixture).

## Evidence

### 1. Development run, `--only U5` (receipt `receipt-dev-only-U5.txt`)

```
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/envelope.sh "$S/env" python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane "$S/lane" --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU5b/battery --only U5 --work "$S/w"

ENVELOPE start 20:32:48 cwd=/fast/scratch/hyaku/kengaku-r44/R44BatU5b
PINS total=2 mismatched=0
FIXTURE u5_short_b-registry-url-task tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
FIXTURE u5_short_b-index-ref-staged tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
FIXTURE u5_short_b-lane-path-manifest tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
FIXTURE u5_short_b-history-truncation tool=anchor expect=reject declared=digest-short observed_rc=1 observed=digest-short ok
MUTANT U5 anchor silence killed by=u5_short_b-registry-url-task attributed=L522 value=differs hits=4 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/1 order=0/0
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:32:49 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`hits=4` is the counter's own count: all four fixtures exhibit the declared direction; the kill is attributed to the first hit only (`by=u5_short_b-registry-url-task`). Leg f: span line `L522` executed in the traced mutant re-run and the `(exit, class set)` reproduced. Leg g: site record differs from the reference's (`value=differs`) — the frame locals at the next line carry `cls`, so `digest-short` vs `digest-long` separates them.

### 2. Direction, reference vs mutant, per fixture (receipt `receipt-direction-ref-vs-mut.txt`)

Fixtures materialised with the counter's own builder (`--build-module ... --dest`, argv taken from the BUILT JSON, receipt `receipt-built-argv.json.txt`); both tools run with each fixture's exact argv, inside the envelope:

```
u5_short_b-registry-url-task ref argv=['--lane', '.'] rc=1
    DEFECT S138 anchor token=eee…e class=digest-short detail=63-hex loc=corpus/SOURCES.md:7
    rows=6 tokens=2 defects=1
u5_short_b-registry-url-task mut argv=['--lane', '.'] rc=1
    DEFECT S138 anchor token=eee…e class=digest-long detail=63-hex loc=corpus/SOURCES.md:7
    rows=6 tokens=2 defects=1
u5_short_b-index-ref-staged ref argv=['--lane', '.', '--evidence-ref', 'index'] rc=1
    DEFECT S202 anchor token=0badc0de class=digest-short detail=8-hex loc=corpus/SOURCES.md:6
u5_short_b-index-ref-staged mut argv=['--lane', '.', '--evidence-ref', 'index'] rc=1
    DEFECT S202 anchor token=0badc0de class=digest-long detail=8-hex loc=corpus/SOURCES.md:6
u5_short_b-lane-path-manifest ref argv=['--lane', '.', '--verbose'] rc=1
    DEFECT S302 anchor token=0123…67 class=digest-short detail=40-hex loc=corpus/SOURCES.md:11
u5_short_b-lane-path-manifest mut argv=['--lane', '.', '--verbose'] rc=1
    DEFECT S302 anchor token=0123…67 class=digest-long detail=40-hex loc=corpus/SOURCES.md:11
u5_short_b-history-truncation ref argv=['--lane', '.'] rc=1
    DEFECT S400 anchor token=3d9da2ad3236a2b08daa class=digest-short detail=20-hex loc=corpus/SOURCES.md:5
u5_short_b-history-truncation mut argv=['--lane', '.'] rc=1
    DEFECT S400 anchor token=3d9da2ad3236a2b08daa class=digest-long detail=20-hex loc=corpus/SOURCES.md:5
ENVELOPE end 20:34:02 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

(Tokens elided with `…` in this table only; the receipt carries them in full.) Exit code is 1 for both branches, i.e. a pure `silence` change: the reference's declared class disappears and no other class appears.

### 3. Load-bearing table — each fixture removed in turn, `--only U5` (receipts `receipt-loadbearing-drop-{0,1,2,3}.txt`)

| removed | fixtures | killed | killed by | wrong / tampered / sidechannel / null / unattributed |
|---|---|---|---|---|
| `u5_short_b-registry-url-task` | 3 | 1 | `u5_short_b-index-ref-staged` | 0 / 0 / 0 / 0 / 0 |
| `u5_short_b-index-ref-staged` | 3 | 1 | `u5_short_b-registry-url-task` | 0 / 0 / 0 / 0 / 0 |
| `u5_short_b-lane-path-manifest` | 3 | 1 | `u5_short_b-registry-url-task` | 0 / 0 / 0 / 0 / 0 |
| `u5_short_b-history-truncation` | 3 | 1 | `u5_short_b-registry-url-task` | 0 / 0 / 0 / 0 / 0 |

Generation: `$S/lb_make.py` wrote a copy of the module with `FIXTURES = [f for f in FIXTURES if f['fid'] != '<removed>']` appended, into `$S/lb/r{0..3}/`, each run bracketed by the envelope (`local_bin_content_before=after=328be01808ba022f`, `unchanged`, exit 0). Reading: **no single fixture is necessary** — U5 dies with any three of the four — and every fixture is individually sufficient to exhibit the direction (§2, and `hits=4` in §1). The four shapes are redundant triggers of one branch by design; they are not four independent behaviours.

### 4. Full default counter on a clone with the module landed (receipt `receipt-full-default.txt`)

`cp` of the module to `$S/lane/plans/battery44/u5_short_b.py`, then:

```
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/envelope.sh "$S/env" python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane "$S/lane" --work "$S/w2"

ENVELOPE start 20:33:24 cwd=/fast/scratch/hyaku/kengaku-r44/R44BatU5b
PINS total=2 mismatched=0
FIXTURE u5_short_b-registry-url-task … ok
FIXTURE u5_short_b-index-ref-staged … ok
FIXTURE u5_short_b-lane-path-manifest … ok
FIXTURE u5_short_b-history-truncation … ok
MUTANT U5 anchor silence killed by=u5_short_b-registry-url-task attributed=L522 value=differs hits=4 -- …
MUTANT U6 anchor silence SURVIVED exhibits=none -- …
MUTANT U7 anchor rc-mirror SURVIVED exhibits=none -- …
MUTANT U9 anchor rc-mirror SURVIVED exhibits=none -- …
MUTANT U14c order error SURVIVED exhibits=none -- …
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/4 order=0/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 20:33:26 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

U6/U7/U9/U14c surviving is the expected state of a one-mutant module; they belong to other wave seats. `PREDICATE C1 fail` is likewise expected here (this clone carries only `u5_short_b`, so the 4/4 and 1/1 floors cannot be met yet).

## Operability notes for the L1

- Land the file as `plans/battery44/u5_short_b.py`; it needs no companion data. Batched scoring stays a few seconds: the `--only U5` run took 3.6 s wall, the full five-mutant default run 3.5 s.
- Fixture 2 depends on `--evidence-ref index` and on a working-tree `SOURCES.md` that differs from the index (that is the shape it demonstrates); it does not depend on an uncommitted-evidence defect, so it stays green if a future counter also reads the working tree.
- Fixture 1's clean row `S139` resolves a *manifest* digest of `SHA256SUMS`; fixture 3's clean row `S301` resolves a *stale* `SHA256SUMS` entry for `report.md` (manifest digest ≠ file digest). Both are deliberate: they keep the expected class set at exactly `{digest-short}` while showing the same branch inside a registry that is otherwise green.
- Fixture 3 also carries a lane-path cell that names a directory (`S299`, no token); tokenless rows raise nothing, so it cannot disturb the declared class set.

## Limits named

1. The counter attributes a kill to the **first** hitting fixture and reports only `hits=<n>`; per-fixture attribution is therefore my own measurement (§2, ref vs mutant per fixture), not the counter's verdict. The load-bearing table (§3) records necessity, not attribution.
2. §2 ran the tool outside the counter's per-run `bwrap` (it is inside the round-44 envelope only, with `/home/vgpnk` read-only). The tool advertises "Read-only; stdlib only; writes no file", the fixture trees were verified clean afterwards (`git -C $S/fx/f000 status --porcelain` empty), and every numeric kill claim above comes from the sandboxed counter runs in §1/§4.
3. My module covers one branch only. Nothing here says anything about U6 (long token), U7 (twin captures), U9 (lessons from the working tree) or U14c (order claims-name guard); those remain survivors in §4 and are other seats' assignments.
4. The four fixtures are four shapes of the same branch, so a future mutation elsewhere in that arm (e.g. in the `detail` text or the ellipsis guard) is not covered by them — they exercise the class label only.
5. The module has not been through non-author review; the sidechannel token scan is the counter's heuristic (`sidechannel=0`) and the independence-from-the-witness-module check is the L1's review, as the frozen claims require.
6. No tool was installed, upgraded or named to pacman; no host service restarted; scratch `/fast/scratch/hyaku/kengaku-r44/R44BatU5b` deleted with `scratch_guard.py safe-rm` after the receipts were copied (sentinel and round root untouched).
7. The clone `plans/battery44/` directory remains uncommitted (`git -C $S/lane status --porcelain` showed `?? plans/battery44/`) and was inside scratch, now deleted; no commit or push was made anywhere.

VERDICT: battery44-u5_short_b-U5-killed-yes-fixtures-4
