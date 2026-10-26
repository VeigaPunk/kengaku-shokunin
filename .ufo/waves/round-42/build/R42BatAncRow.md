# R42BatAncRow — `plans/battery42/a_row.py` (C1, anchor X9 / X13 / X15)

Seat: executor, kengaku round 42 wave 1. Lane read-only tip used for the counter: `fda71ae` (clone `$S/lane`).
Module written only under this seat's build dir; no lane file, corpus, plans/, index or jj state touched.

## 1. Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/build/R42BatAncRow/battery/a_row.py`
**sha256 `947194e4517fb94b8d3529e6c4d5118585697497103784655ddd736635b48df8`** (8859 bytes, stdlib `hashlib` only).
Integration target: `plans/battery42/a_row.py`. Every repo is built from nothing by `ctx.init`/`ctx.write`/`ctx.git`;
every argv is `["--lane", <fixture repo>]` inside the fixture dir; the module imports and copies nothing from
`.ufo/waves/round-42/claims/witness/` (that directory was read only to learn which branches are reachable, and each
fixture's shape below is deliberately different from it).

| fid | mutant targeted | branch it exercises | expect | defects (exact reference set) | shape |
|---|---|---|---|---|---|
| `a_row-x9-short-no-token` | X9 | cell-count check `len(r["cells"]) != NCELLS` | reject | `row-malformed` | one 10-cell row (teaches cell missing) with **no digest claim** — the freeze module's short row carried a real capture digest |
| `a_row-x9-registry-short-valid` | X9 | same branch, second trigger | reject | `row-malformed` | realistic six-row registry (header + 2 correctly anchored rows, 3 claim-less rows) whose 10-cell row carries a **correct** digest: green on every digest test, disqualified only by cell count |
| `a_row-x13-staged-capture` | X13 | `--evidence-ref` default (`head`) | reject | `digest-unknown` | multi-commit: commit 1 first view, commit 2 commits the row advanced to the re-captured digest, then **only the capture blob** is staged (manifest stays at HEAD); freeze module staged capture + SHA256SUMS and rewrote SOURCES in the worktree |
| `a_row-x13-url-staged` | X13 | same branch, second trigger | reject | `digest-unknown` | row bound through the pinned `raw.githubusercontent.com` URL + `task.toml name = "tb2/wiki"` route (not an explicit lane path), a second clean row beside it, capture staged beyond HEAD |
| `a_row-x15-sibling-digest` | X15 | erratum `supported` scope (`t in row_scope`) | reject | `digest-unknown`, `erratum-incomplete` | two-row registry: the sibling row exists, is bound and is clean; the erratum cites **that sibling's capture digest**, in the global set but not in the corrected row's scope |
| `a_row-x15-manifest-sibling` | X15 | same branch, second trigger | reject | `digest-unknown`, `erratum-incomplete` | erratum appended in a **later commit**; correction is the sibling capture's manifest-listed (older) digest, reachable in A only through the manifest view; corrected row URL-bound |

No lane clone is offered or used; `ctx.sh`/`ctx.init` are the build primitives. No absolute or relative argv path
escapes the fixture dir (the counter's `path_ok` accepted all six: `BATTERY fixtures=6` with no `SETUP`).

Token scan (same list as the counter, case-insensitive), no match:

```
$ grep -nEi '(/proc|ppid|cmdline|psutil|environ|fsmonitor|hookspath|filter\.|gitattributes|core\.|alias\.|setsid|daemon|fork|nohup|socket|/home/|\.local|__file__|inspect|importlib|sys\.path|ctypes|chmod|witness|settrace|/run)' .../battery/a_row.py
(no matches)                       # counter agrees: sidechannel=0
```

## 2. The three kills (development mode, pasted)

Envelope for every run below (Q32): `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin
--tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <counter>`. `ls -A ~/.local/bin | sha256sum`
before **and** after: `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` (unchanged). Times 17:20:08 →
17:20:09. Receipt: `build/R42BatAncRow/dev-run.txt`.

```
PINS total=2 mismatched=0
FIXTURE a_row-x9-short-no-token tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_row-x9-registry-short-valid tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_row-x13-staged-capture tool=anchor expect=reject declared=digest-unknown observed_rc=1 observed=digest-unknown ok
FIXTURE a_row-x13-url-staged tool=anchor expect=reject declared=digest-unknown observed_rc=1 observed=digest-unknown ok
FIXTURE a_row-x15-sibling-digest tool=anchor expect=reject declared=digest-unknown,erratum-incomplete observed_rc=1 observed=digest-unknown,erratum-incomplete ok
FIXTURE a_row-x15-manifest-sibling tool=anchor expect=reject declared=digest-unknown,erratum-incomplete observed_rc=1 observed=digest-unknown,erratum-incomplete ok
MUTANT X9 anchor rc-silence killed by=a_row-x9-short-no-token attributed=L477 hits=2 -- plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have
MUTANT X13 anchor rc-silence killed by=a_row-x13-staged-capture attributed=L570 hits=2 -- plans/anchor_digest_check.py:73 '`--evidence-ref head` (default) reads HEAD blobs, so an u
MUTANT X15 anchor rc-silence killed by=a_row-x15-sibling-digest attributed=L455 hits=2 -- plans/anchor_digest_check.py:108-110 'at least one other token that is 64 lowercase hex an
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/3 order=0/0
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
dev-rc=0
```

Command:
`python3 plans/round42_c1_verify.py --lane "$S/lane" --battery-dir $L/.ufo/waves/round-42/build/R42BatAncRow/battery --only X9,X13,X15 --work "$S/w3"`.

## 3. Load-bearing table (one fixture removed at a time, then the pair)

Variants are copies of the module in `$S/lb/<tag>/` with the FIXTURES entry (not the builder function) dropped;
each row is the counter's own output on `--only X9,X13,X15`. Receipt: `build/R42BatAncRow/load-bearing.txt`
(start 17:20:13, end 17:20:18, local-bin digest unchanged).

| removal | X9 | X13 | X15 | fixtures |
|---|---|---|---|---|
| `x9-short-no-token` | killed by `a_row-x9-registry-short-valid` | killed | killed | 5 |
| `x9-registry-short-valid` | killed by `a_row-x9-short-no-token` | killed | killed | 5 |
| `x13-staged-capture` | killed | killed by `a_row-x13-url-staged` | killed | 5 |
| `x13-url-staged` | killed | killed by `a_row-x13-staged-capture` | killed | 5 |
| `x15-sibling-digest` | killed | killed | killed by `a_row-x15-manifest-sibling` | 5 |
| `x15-manifest-sibling` | killed | killed | killed by `a_row-x15-sibling-digest` | 5 |
| both X9 fixtures | **SURVIVED** (`exhibits=none`) | killed | killed | 4 |
| both X13 fixtures | killed | **SURVIVED** (`exhibits=none`) | killed | 4 |
| both X15 fixtures | killed | killed | **SURVIVED** (`exhibits=none`) | 4 |

So each mutant has exactly two independent triggers of its own branch, and removing the pair flips that mutant to
`SURVIVED` while leaving the other two killed: the kill is caused by these fixtures, not by an accident of ordering.

## 4. Full default counter (module copied into the clone's `plans/battery42`)

`cp battery/a_row.py "$S/lane/plans/battery42/a_row.py"` then
`python3 plans/round42_c1_verify.py --lane "$S/lane" --work "$S/w2"` — envelope as above, start 17:19:52, end
17:19:53, local-bin digest `436b361f…` before and after, `rc=1`. Receipt: `build/R42BatAncRow/full-run.txt`.

```
PINS total=2 mismatched=0
... 6 × FIXTURE ... ok  (as §2)
MUTANT X1 anchor rc-mirror SURVIVED exhibits=none
MUTANT X3 anchor rc-mirror SURVIVED exhibits=none
MUTANT X6 anchor silence SURVIVED exhibits=none
MUTANT X7 anchor silence killed by=a_row-x13-staged-capture attributed=L535 hits=4 -- plans/anchor_digest_check.py:92-93
MUTANT X9 anchor rc-silence killed by=a_row-x9-short-no-token attributed=L477 hits=2
MUTANT X12 anchor rc-mirror SURVIVED exhibits=none
MUTANT X13 anchor rc-silence killed by=a_row-x13-staged-capture attributed=L570 hits=2
MUTANT X14 anchor silence SURVIVED exhibits=none
MUTANT X15 anchor rc-silence killed by=a_row-x15-sibling-digest attributed=L455 hits=2
MUTANT XO1/XO3/XO5/XO6/XO7 order … SURVIVED exhibits=none
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=4 survived=10 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=4/9 order=0/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```

Other mutants surviving is expected for one of several wave-1 modules. **Disclosed side effect:** X7 (declared
`silence`, relabelling `digest-unknown` → `digest-wrong-capture`) is also killed, by `a_row-x13-staged-capture`:
the unmodified tool prints `class=digest-unknown` there and the mutant prints `digest-wrong-capture` instead, which is
exactly X7's declared direction on a fixture that executes its line (`attributed=L535`). That is a real result, not a
mislabel, and it does not depend on the X13 direction: the fixture's third mutant run is independent of X13's
argparse default. A dedicated X7 module can still be added; this one is not claimed as its design intent.

## 5. Limits

- A kill records a result difference in the declared direction on a fixture that executes the replaced line, not the
  fixture's intent (the counter's own limit, restated).
- Fixtures are small constructed registries (1–6 rows, 1–2 commits); they do not model a 109-row `SOURCES.md`.
- `a_row-x13-staged-capture` and `a_row-x15-manifest-sibling` leave a staged index entry in the fixture repo on
  purpose; the counter's `fingerprint` excludes `.git/index`, and no fixture file changes during a run
  (`tampered=0` on every run above).
- The module does not attempt order-check mutants (another seat's lane); `MUTANTS-BY-TOOL order=0/5` in §4 is
  therefore expected for this module alone.
- Nothing was installed or upgraded (no tool/version/channel change to record); no `pacman` call was made; all runs
  used the host `/usr/bin/python3` and `/usr/bin/bwrap` inside the Q32 envelope, nested sandboxes included.

VERDICT: battery42-a_row-killed-3/3-wrong-0
