# Seat C1ExecFetchGraders — wave 1, build — R52-C1 capture fetch

**Lane:** `kengaku-shokunin` · **Round:** 52 (hyaku run 11) · **Wave:** 1 (build) · **Seat:** C1ExecFetchGraders (executor)
**Base tip:** `30801b479e3418c11089b8586178b6960216f364` · **Population pin:** `harbor-framework/terminal-bench-2@2fd12b88aafdd04a52c298e3940bcb189f9766d6`

## What I did

Fetched every file of the **frozen population** `plans/round52-tasks.json` → `capture_population`
(89 tasks, **184 unique paths**) from `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<path>`,
stored byte-exact with the repo-relative path preserved, and wrote a `sha256sum`-format digest file.
No bytes were post-processed (no trailing-newline edits, no re-encoding, no normalisation); the
files are the raw HTTP response bodies.

The population path set was derived only from the frozen manifest (never from the upstream tree),
so the fetch set is exactly the claim's population.

## Exact commands run

```sh
# 1. derive the frozen path list from the frozen manifest (89 tasks -> 184 unique paths)
python3 - <<'PY'
import json
d=json.load(open('/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52-tasks.json'))
cp=d['capture_population']
paths=sorted({p for ps in cp.values() for p in ps})
open('tmp/paths.txt','w').write('\n'.join(paths)+'\n')
PY

# 2. fetch (16-way parallel, per-path HTTP status captured verbatim)
bash /fast/scratch/hyaku/kengaku-r52/C1ExecFetchGraders/tmp/fetch.sh
#   fetch_one(): curl -sS -o "$out.part" -w '%{http_code}' --retry 3 --retry-delay 1 --max-time 120 "$BASE/$p"
#   -> HTTP 200 => mv .part -> final path (no rewriting); non-200 / empty / curl-fail => logged, .part deleted

# 3. presence + digest verification
cd /fast/scratch/hyaku/kengaku-r52/C1ExecFetchGraders
diff <(sort tmp/paths.txt) <(find graders -type f | sed 's|^graders/||' | sort)     # -> identical
(cd graders && LC_ALL=C find . -type f -print0 | sort -z | xargs -0 sha256sum > ../SHA256SUMS)
(cd graders && sha256sum -c ../SHA256SUMS --quiet)                                 # -> all OK
sha256sum SHA256SUMS

# 4. independent byte-exactness cross-check against the upstream git tree at the pin
curl -sS "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1" -o tmp/tree.json
python3 - <<'PY'   # for every path: local git-blob sha1 ("blob <len>\0"+bytes) vs upstream tree blob sha
...
PY
```

## Measured numbers

| measure | value |
|---|---|
| expected paths (frozen `capture_file_count`) | **184** |
| files fetched (HTTP 200, non-empty) | **184** |
| files present under the capture root | **184** |
| **mismatched** (path set vs manifest, or digest mismatch) | **0** |
| **missing paths** | **none** (path-set diff empty) |
| non-200 / empty / failed responses | **0** (no 404, no empty body, no curl error) |
| total bytes captured | **477 374** (min file 295 B, max 18 746 B) |
| file-name mix | 94 `test_outputs.py`, 89 `test.sh`, 1 `verify.sh` |
| SHA256SUMS lines | 184 |
| **sha256 of SHA256SUMS** | `b9ada6472642fa547935c6a1d4fb9474db4d84b412fb9ab3c1730fd65bc974c8` |
| upstream git-tree blob-sha mismatches | **0** (all 184 match the tree at the pin) |

Independent cross-check (beyond our own digest): every captured file's **git blob SHA-1**
(`sha1("blob <len>\0" + bytes)`) equals the blob sha of the same path in the upstream recursive
tree at `2fd12b8` — 0 mismatches — so the captured bytes are the upstream bytes, not merely
self-consistent. `truncated=false` on the tree response (1 446 entries, 1 038 blobs), so the
comparison was against a complete tree.

### 404 / empty responses recorded verbatim

**None.** The per-path fetch log (`artifacts/fetch_log.tsv`, 184 lines, columns `path / status /
bytes / http_code`) contains status `OK` for all 184 rows; no `HTTP404`, no `EMPTY`, no `CURLFAIL`
row exists. A connectivity probe to one population path returned `probe_http=200` before the batch
run.

## Files produced (absolute paths)

Persistent copies (kept in my own wave-report dir so the L1 can integrate them; the scratch tree was
removed at end of seat, per the scratch directive):

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/graders/<population-path>` — the 184 captured grader files, repo-relative path preserved (976 KB total with receipts)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/SHA256SUMS` — `sha256sum` format, paths relative to the `graders/` root (sha256 `b9ada647…974c8`)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/fetch_log.tsv` — per-path HTTP status receipt (184 rows)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/paths.txt` — the frozen path list as fetched (184 lines)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecFetchGraders/report.md` — this report (also written as `…/w1/C1ExecFetchGraders.md`, the path named in the seat item)

Scratch (created, used, then removed): `/fast/scratch/hyaku/kengaku-r52/C1ExecFetchGraders/`
(fetch script, path list, tree.json, fetch log, and the working copy of `graders/` + `SHA256SUMS`).

## Integration note for the L1

The frozen counter `plans/round52_c1_grader_audit.py` reads captures from
`<lane>/corpus/evidence/round52/graders/` and its `SHA256SUMS` from
`<lane>/corpus/evidence/round52/graders/SHA256SUMS`, and it keys sums by the population path
(`load_sums` strips a leading `*` and takes the second whitespace-separated field). My `SHA256SUMS`
is written with paths relative to the `graders/` root, i.e. exactly the keys the counter expects
when the file is placed at `<cap_root>/SHA256SUMS` and the tree at `<cap_root>/<population-path>`:

```sh
mkdir -p corpus/evidence/round52/graders
cp -a <wave-dir>/C1ExecFetchGraders/artifacts/graders/. corpus/evidence/round52/graders/
cp <wave-dir>/C1ExecFetchGraders/artifacts/SHA256SUMS corpus/evidence/round52/graders/SHA256SUMS
```

This yields `CAPTURES expected=184 present=184 mismatched=0` (leg 1 of R52-C1), because the
counter hashes the captured bytes itself and compares them to the sums file — both sides come from
the same bytes.

## Risks / limits / notes

- **Population frozen upstream, not re-derived:** the path list came from `capture_population` in
  the frozen manifest only. The upstream tree was consulted *after* the fetch, solely as an
  independent byte-exactness oracle; it did not add or drop any path. All 184 population paths do
  exist as blobs at the pin (0 missing).
- **The counter's `primary_grader()` prefers `tests/test_outputs.py` over
  `environment/tests/test_outputs.py`** (`to.sort(key=lambda f: ("environment/" in f, f))`). Five
  tasks carry both variants; both are captured, so the primary selection resolves for every task.
- **`sha256sum -c` must be run from the `graders/` root** (paths in `SHA256SUMS` are relative to
  it). An early verification run of mine was executed from the seat root and reported
  `No such file or directory` for all 184 — a cwd artefact, not a data defect; the same file
  re-checked from `graders/` returns all-OK (and the copy in the wave-report dir re-verified
  `COPY_VERIFY_OK`).
- **No byte mutation:** fetched bodies were written via `curl -o` to a `.part` file and moved into
  place only on HTTP 200 with a non-zero size; failed/empty fetches would have been logged and
  dropped, leaving no truncated file behind. No trailing-newline or encoding fixups were applied.
- **Network dependency:** the fetch needed `raw.githubusercontent.com` and `api.github.com`; both
  were reachable (probe 200, 184/184 fetches 200, tree API returned `truncated=false`).
- **Tools installed/updated:** none. Only pre-existing `curl`, `coreutils sha256sum`, `python3`
  and `git` (no git mutation commands were run) were used. Free space observed before the run:
  `/fast` 538 G available (34 % used), `/home` 557 G available (38 % used) — no ENOSPC.

## Scope statement

This seat is a pure capture/verification executor. It wrote only inside its own scratch dir and
its own wave-report dir; it did **not** touch the lane tree, the fleet repo, `.ufo/state/`,
`templates/`, `scripts/`, `MANIFEST.json`, sibling lanes, or `/home/vgpnk/Projects/shokuknow`, and
ran no `git commit/add/push/stash/checkout/reset/pull` and no mutating `jj` command. No scoring,
no prior-art pricing, no classification (those are other seats' claims) — this seat delivers only
the capture population plus its digest pin.
