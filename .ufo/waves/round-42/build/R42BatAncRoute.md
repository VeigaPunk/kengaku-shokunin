# R42BatAncRoute — battery42 anchor binding routes (X1, X3, X12)

Seat: leaf executor, kengaku round 42 wave 1. Lane repo read-only at
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` (clone for measurement:
`/fast/scratch/hyaku/kengaku-r42/R42BatAncRoute/lane`, `rev-parse --show-toplevel` = that path).
Nothing frozen was touched; no lane file was edited, no commit, no push.

Axes named: **calibration** (can a fixture force a frozen mutant's declared direction?) and
**operability** (does the module load, build from nothing and attribute inside the counter?).

## 1. Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/build/R42BatAncRoute/battery/a_route.py`
— 9105 bytes, stdlib only (`hashlib`), six fixtures, every `fid` prefixed `a_route-`.

```
$ sha256sum battery/a_route.py
d6dad7cd1458838dcd546f2176ff5b2217faab78cc68b92c86ad94b688adf81f  battery/a_route.py
```

Integration target for the L1: copy it unchanged to `plans/battery42/a_route.py`.
My own case-insensitive scan of the module against the counter's `SIDECHANNEL` tuple:
`hits: []`; the counter's own scan reported `sidechannel=0` in every run below.

## 2. Fixtures (one per behaviour, two per mutant, all different in shape from the pre-freeze modules)

| fid | mutant | route exercised (tool docstring §Binding) | demonstrates |
|---|---|---|---|
| `a_route-x1-provenance-table` | X1 | 1 — provenance row | one `PROVENANCE.md` table line carrying row id **and** ticked capture file **and** a digest column; the row's own text has no URL and no `corpus/evidence/` path, so route 1 is the only binder |
| `a_route-x1-two-row-registry` | X1 | 1 — provenance row | registry scale: rows S126/S127 each bound by their own table in two evidence dirs, capture batch in commit 1, the rows in commit 2 (multi-commit history) |
| `a_route-x3-provenance-url` | X3 | 2 — provenance-URL fallback | row pins a `raw.githubusercontent.com` URL; no `task.toml` exists anywhere, so only a PROVENANCE URL column (which carries no row id) names the capture |
| `a_route-x3-blob-url` | X3 | 2 — provenance-URL fallback | same fallback through a `github.com/.../blob/<sha>/...` URL, with a committed `task.toml` whose slug (`other-task`) names a different task, and a 3-component subpath |
| `a_route-x12-slashless-toml` | X12 | 2 — task.toml slug | `task.toml` gives a slash-less `name = "circuit-task"` (plus a second `name = "acme"` under `[author]`); the URL's task component matches that slug |
| `a_route-x12-two-tomls` | X12 | 2 — task.toml slug | two task dirs, a `group/data-task` subpath naming the middle component, capture accepted through its `SHA256SUMS` entry |

All six are `expect=accept`, `defects=[]`, `tool=anchor`: the unmodified tool binds, prints only its
`EVIDENCE …` summary (no `DEFECT` line) and exits 0. Each mutant drops one binder, the row falls to
`anchor-unbound`, exit 1 → `rc-mirror`.

Developer note worth carrying to the other anchor seats: the provenance row is keyed by row ids **on the
provenance line**, not on the SOURCES row (`prov_sid.setdefault(sid, …)` over `ROWID.findall(line)`), so a
table whose line lacks `S<nnn>` binds nothing. My first build failed exactly that way (`observed=anchor-unbound
WRONG` twice) and both X1 fixtures now carry a `row` column.

## 3. Development receipt (subset, attributed kills)

```
$ bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent \
  /usr/bin/python3 <lane>/plans/round42_c1_verify.py --lane "$S/lane" \
  --battery-dir <report>/battery --only X1,X3,X12 --work "$S/w"
PINS total=2 mismatched=0
FIXTURE a_route-x1-provenance-table tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_route-x1-two-row-registry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_route-x3-provenance-url tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_route-x3-blob-url tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_route-x12-slashless-toml tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_route-x12-two-tomls tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT X1 anchor rc-mirror killed by=a_route-x1-provenance-table attributed=L318 hits=2 -- plans/anchor_digest_check.py:50-52 …
MUTANT X3 anchor rc-mirror killed by=a_route-x3-provenance-url attributed=L343 hits=2 -- plans/anchor_digest_check.py:57-58 …
MUTANT X12 anchor rc-mirror killed by=a_route-x12-slashless-toml attributed=L256 hits=2 -- plans/anchor_digest_check.py:55-56 …
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/3 order=0/0
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Full text: `dev-subset.txt` (sha256 `4e82333f…a34340`, 1445 bytes). `hits=2` on each mutant
means both of its fixtures exhibit the direction; the traced re-run picked the first that also executed a
line of the replaced span — L318 (X1 `got = []`), L343 (X3 `if False:`), L256 (X12 slash-less fallback).

## 4. Load-bearing matrix (fixtures removed in turn)

Receipt `load-bearing.txt` (sha256 `183adb3a…6b852`). Six single-removal variants, then both fixtures of one
mutant removed:

| removed | X1 | X3 | X12 | `hits` for the affected mutant |
|---|---|---|---|---|
| `x1-provenance-table` | killed by `x1-two-row-registry` | killed | killed | 2 → 1 |
| `x1-two-row-registry` | killed by `x1-provenance-table` | killed | killed | 2 → 1 |
| `x3-provenance-url` | killed | killed by `x3-blob-url` | killed | 2 → 1 |
| `x3-blob-url` | killed | killed by `x3-provenance-url` | killed | 2 → 1 |
| `x12-slashless-toml` | killed | killed | killed by `x12-two-tomls` | 2 → 1 |
| `x12-two-tomls` | killed | killed | killed by `x12-slashless-toml` | 2 → 1 |
| both X1 fixtures | **SURVIVED** `exhibits=none` | killed | killed | 2 → 0 |
| both X3 fixtures | killed | **SURVIVED** `exhibits=none` | killed | 2 → 0 |
| both X12 fixtures | killed | killed | **SURVIVED** `exhibits=none` | 2 → 0 |

So every fixture is one of two independent, individually attributed triggers of its mutant: single removal
loses no kill (each mutant stays `killed`, `hits` drops by one, `wrong=0` throughout), and removing both
flips exactly that mutant to `SURVIVED` with `BATTERY fixtures=4 … sidechannel=0`.

## 5. Full default counter in the lane clone

Module copied to `$S/lane/plans/battery42/a_route.py` (clone only, no commit), then the default run:

```
$ bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent \
  /usr/bin/python3 <lane>/plans/round42_c1_verify.py --lane "$S/lane" --work "$S/w2"
PINS total=2 mismatched=0
… six FIXTURE lines, all ok …
MUTANT X1  anchor rc-mirror killed by=a_route-x1-provenance-table attributed=L318 hits=2 …
MUTANT X3  anchor rc-mirror killed by=a_route-x3-provenance-url attributed=L343 hits=2 …
MUTANT X6  anchor silence    SURVIVED exhibits=none …
MUTANT X7  anchor silence    SURVIVED exhibits=none …
MUTANT X9  anchor rc-silence SURVIVED exhibits=none …
MUTANT X12 anchor rc-mirror  killed by=a_route-x12-slashless-toml attributed=L256 hits=2 …
MUTANT X13 anchor rc-silence SURVIVED exhibits=none …
MUTANT X14 anchor silence    SURVIVED exhibits=none …
MUTANT X15 anchor rc-silence SURVIVED exhibits=none …
MUTANT XO1 order rc-silence  SURVIVED exhibits=none …
MUTANT XO3 order rc-silence  SURVIVED exhibits=none …
MUTANT XO5 order rc-mirror   SURVIVED exhibits=none …
MUTANT XO6 order rc-mirror   SURVIVED exhibits=none …
MUTANT XO7 order rc-silence  SURVIVED exhibits=none …
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=3 survived=11 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/9 order=0/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```

Receipt `full-default.txt` (sha256 `eb2a2f14…5704`). `PREDICATE C1 fail` is the expected state of a
wave-1 lane whose battery covers one seat's three mutants; the 11 survivors are the other wave-1 seats'
claims (X6 X7 X9 X13 X14 X15 anchor; XO1 XO3 XO5 XO6 XO7 order). No fixture of mine changes any other
mutant's result (`wrong=0`, `tampered=0`, `sidechannel=0`, `null_detected=0`, `unattributed=0`).

## 6. Q32 envelope evidence

Envelope used for every counter run above: `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin
/home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>`
(the counter nests its own `--ro-bind / /` sandboxes inside). `date +%T` and
`ls -A /home/vgpnk/.local/bin | sha256sum` before/after each invocation:

| run | before | after | PATH listing digest before = after |
|---|---|---|---|
| dev subset | 17:18:52 | 17:18:53 | `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` |
| load-bearing matrix (9 runs) | 17:19:25 | 17:19:31 | same |
| full default | 17:19:16 | 17:19:17 | same |

Nothing was written outside `$S=/fast/scratch/hyaku/kengaku-r42/R42BatAncRoute` and this report dir; no
package was installed, no PATH directory touched, no fleet-root tracked file written.

## 7. Risks and limits

- A kill is a result difference in the declared direction on a fixture that executes the replaced line,
  not an endorsement of the fixture's realism. Mine are minimal registries (1–2 rows, 1–5 evidence files);
  they exercise the branch, not the lane's real 109-row shape.
- The X3 fixtures pass for a reason specific to the tool: URL→task matching uses the URL basename at the
  task directory root, so a capture nested at `tests/` inside the dir is *not* reachable through
  `url-task`; both X3 fixtures therefore keep the capture at the directory root and put the deeper
  components in the URL only. A future seat wanting a nested-capture X3 kill must use a manifest entry
  (`dir_entries`), not the bare path.
- X12's two fixtures depend on `TOML_NAME.findall` taking the **first** slash-free name; a `task.toml`
  whose slash-less name is preceded by another `name =` line would bind differently. That is the tool's
  behaviour, quoted in the mutation cell, not a property I assert.
- Token-scan cleanliness of the module is a heuristic pass (`sidechannel=0`), not a proof.

## 8. Verification for the integrating agent

1. `sha256sum plans/battery42/a_route.py` after copy → `d6dad7cd1458838dcd546f2176ff5b2217faab78cc68b92c86ad94b688adf81f`.
2. `python3 plans/round42_c1_verify.py --lane .` → expect `BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0`
   and `killed` rising by 3 versus the do-nothing control (`anchor=3/9` before the other seats land).
3. `FIXTURE … ok` for all six ids, `null_detected=0 unattributed=0`.

VERDICT: battery42-a_route-killed-3/3-wrong-0
