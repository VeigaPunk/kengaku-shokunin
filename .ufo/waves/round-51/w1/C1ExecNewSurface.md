# C1ExecNewSurface — the new host-state surface: the LFM3 router and its served instance

Seat `C1ExecNewSurface` (executor), kengaku round 51, wave w1. Claim **R51-C1** (freshness 8 → 9).
Axis named: **freshness** — a surface that exists on this host and was declared nowhere in
`PROVINCE.md` becomes a declared, machine-checked row.

One move: declare the live endpoint found on this host (the LFM3 model server and its router) as a
`## Surfaces` row plus its `plans/round51-surfaces.json` entry, and prove the frozen counter covers
it. No production file was touched; the candidate was validated in a scratch clone and handed over
as a fragment.

## 1. What the surface is (measured, not inferred)

Two `llama-server` processes, both this host's, both answering at capture
`2026-10-28T18:26:47Z`:

```
pid 1706355  /home/vgpnk/src/llama.cpp/build/bin/llama-server --models-dir /home/vgpnk/models/lfm3 --models-max 2 --host 127.0.0.1 --port 1234 -ngl 99 -c 32768 --jinja
pid 242776   /home/vgpnk/src/llama.cpp/build/bin/llama-server --host 127.0.0.1 --jinja --log-colors off --port 45669 --alias LFM3-1.7B --ctx-size 32768 --model /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf --n-gpu-layers 99
```

`ps -o etimes` at capture: router 12485 s, instance 10885 s — both up before this wave started, so
this is pre-existing host state, not something a seat started.

Router role is machine-stated by the endpoint itself, not by the argv:

```
$ curl -sS -m 4 http://127.0.0.1:1234/props
{"role":"router","max_instances":2,"models_autoload":true,"model_alias":"llama-server","model_path":"none","default_generation_settings":{"params":null,"n_ctx":0},"ui_settings":{},"build_info":"b1-39febd2","cors_proxy_enabled":false}

$ curl -sS -m 4 http://127.0.0.1:1234/health
{"status":"ok"}

$ ss -ltn 'sport = :1234'
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
LISTEN 0      512        127.0.0.1:1234      0.0.0.0:*

$ ss -ltn 'sport = :45669'
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 0      512        127.0.0.1:45669       0.0.0.0:*
```

`/v1/models` at capture (5 rows: 4 `source=models_dir` from `--models-dir`, 1 `source=cache`):

```
5
  LFM3-1.7B loaded models_dir
  LFM3-1.7B-Uncensored unloaded models_dir
  LFM3-Omni-2B unloaded models_dir
  LFM3-VL-2B unloaded models_dir
  LiquidAI/LFM3-1.7B-GGUF:Q8_0 unloaded cache
```

Loaded-instance identity from the same endpoint (`/v1/models` → `LFM3-1.7B`):
`owned_by=llamacpp`, `context_length=262144`, `meta = {"vocab_type":2,"n_vocab":128000,"n_ctx":32768,
"n_ctx_train":262144,"n_embd":2048,"n_params":1728801600,"size":1837991168,"ftype":"Q8_0"}`,
`status.value=loaded`, and `status.args` naming `--port 45669` — i.e. the child instance the router
spawned, which is exactly pid 242776 above.

Probe stability: `GET http://127.0.0.1:1234/health` → `200 200 200` on three consecutive calls.
No completion request was ever sent (only `GET /health`, `GET /props`, `GET /v1/models`), so nothing
in this report is a capability measurement.

## 2. The fragment (what the L1 lands)

`.ufo/waves/round-51/w1/C1ExecNewSurface.json` carries:

- `entry` — the exact manifest object, `id SF20`, `section "## Surfaces"`,
  `state "present"`, `prose "present"`, `probe {"kind":"http","urls":["http://127.0.0.1:1234/health"]}`,
  and the `why`.
- `probe_spec` — the `http` probe as chosen, the equivalent `port` probe on `127.0.0.1:1234` as the
  alternative, and the instance port `45669` marked **capture-only** (the router assigns it per
  spawn, so pinning it would declare instance state as a surface).
- `row` — the exact PROVINCE markdown line, byte-identical to the line validated in the clone.
- `placement` — append as the last row of `## Surfaces`, after the `| Public literature | arXiv …`
  row (`PROVINCE.md:20` at the measured rev); the entry goes last in `surfaces`, after `SF19`.

Exact row handed over (1016 characters, 4 pipes → 3 cells):

```
| LFM3 router + served instance (host state, pinned at capture) | `http://127.0.0.1:1234` — `/health`, `/props` (`role=router`, `max_instances=2`, `models_autoload=true`, build `b1-39febd2`), `/v1/models` over `--models-dir ~/models/lfm3 --models-max 2`; at capture the loaded child `llama-server` instance was `LFM3-1.7B` (`LFM3-1.7B-Q8_0.gguf`, `--ctx-size 32768`, `n_ctx_train=262144`) on `127.0.0.1:45669` | identity and liveness observation only, never a capability: operator-owned serving-plane host state (`## Adjacent` puts serving-plane health and endpoint identity with `kama`; `## Refusals` leaves flag-change authority unowned — escalate to the integrator, never remediate here); no completion request is sent and no capability number is derived; the router endpoint is the declared surface and is not a revival of the absent `:34113` endpoint above; the instance port is capture-time state the router reassigns on respawn, so a later absent probe is host state, not a lane defect **PINNED 2026-10-28** |
```

Honesty of the row, stated plainly: it declares a **host-state surface pinned at capture time**, not
a capability. The declared, machine-checked endpoint is the router (`:1234`); the loaded instance's
port is labelled capture-time state because the router reassigns it. `state=present` is the probed
truth and `prose=present` is the reading of what the row asserts (the router resolves), so the row
introduces no `DRIFT`. If the router disappears, the probe goes absent while `state` stays `present`
and the counter reports `STALE` — the behaviour `plans/round-51-claims.md` §Limits declares intended,
not a lane defect. Remediation is not this lane's: `## Refusals` (lines 24–26) leaves the serving
plane unowned and escalates flag changes to the integrator, and `## Adjacent` (line 136) puts
serving-plane health and endpoint identity with `kama`. The row therefore claims identity/liveness
observation only.

Why `http` and not `port` for the manifest: the counter accepts exactly one probe per entry, and a
200 from `http://127.0.0.1:1234/health` proves strictly more than a listener assertion (HTTP surface
**and** a LISTEN socket on `127.0.0.1:1234`). The `port` spec is supplied so the L1 can swap in a
bare listener assertion if it prefers one; the row's printed check is `ss -ltn 'sport = :1234'`.

## 3. Validation — the frozen counter, in a scratch clone

Clone and apply (fixture asserted to be the clone itself before any write):

```
git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin <scratch>/lane
git -C <scratch>/lane rev-parse --show-toplevel   -> <scratch>/lane
git -C <scratch>/lane rev-parse HEAD              -> 4090c3db79d11279ab5e5121ba25e74aa316e6e7
python3 <scratch>/apply_candidate.py <scratch>/lane
python3 plans/round51_surfaces.py --lane .        # cwd = clone root
```

Before (clean clone at the measured rev), exit 1:

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

After (SF20 entry + row applied), exit 1:

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=20 sections=2
ANCHORS total=20 dup=0 missing=0
ROWS section="## Surfaces" rows=10 entries=10 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=20 present=14 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=14 floor=13 verdict=met
PREDICATE R51-C1 fail
```

Reading the delta: anchors 19 → 20 with no duplicate and no missing; `## Surfaces` rows 9 → 10 with
`uncovered=0`; present 13 → 14 (`RESOLVE` floor still met and now exceeded by one); `SF20` appears in
**no** problem list. The predicate still prints `fail` only because the three pre-landing row
corrections (`SF01`, `SF02`, `SF03`), the `SF04` date and the `SF14` count are the L1's landing work —
the same five items present before the entry, unchanged after it. This entry adds no problem.

Instrument untouched and self-checked:

```
$ python3 plans/round51_surfaces.py --selftest
...
[selftest] cases=9 failures=0
[selftest] ALL PASS
```

Fragment integrity, re-checked against the validated clone before the clone was destroyed:

```
row_identical: True len 1016 1016
entry_identical: True
anchor_in_row: True
anchor_occurrences_in_section: 0
pipes: 4
```

(`anchor_occurrences_in_section: 0` counts occurrences in the lane's *unmodified* `PROVINCE.md`; the
anchor exists only once the row is landed, and the counter found exactly one hit per entry — `dup=0`,
`missing=0` — after the append.)

Revision identity of what was measured:

```
git -C <lane> diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c 4090c3db79d11279ab5e5121ba25e74aa316e6e7 -- PROVINCE.md plans/round51-surfaces.json plans/round51_surfaces.py
(no output)
git -C <lane> status --porcelain -- PROVINCE.md plans/round51-surfaces.json plans/round51_surfaces.py
(no output)
```

so the C1 surface files at the measured HEAD are the freeze's files; the counter's own `REV` line
reports the same hash.

## 4. Limits

- **One probe per entry.** The frozen counter dispatches on a single `probe.kind`, so "http + port"
  cannot both be the machine check for one row. `http` on the router's `/health` is the chosen check
  (it subsumes the `:1234` listener assertion); the `port` spec is handed over as the alternative and
  as the row's printed check. I did not add a second entry for the same row — the manifest's own note
  is "one entry per table row".
- **The instance port is not pinned.** `:45669` is capture-time state. Pinning it would declare
  instance state as a surface and go `STALE` at the router's next respawn.
- **`:37323` deliberately not declared.** It is an ollama-spawned `llama-server` running a blob under
  `/fast/scratch/hyaku/kama-r61-closure` (another lane's round-61 scratch run): scratch instance
  state, not a stable host surface. Declaring it would import a sibling's scratch path as truth.
- **No capability evidence.** No completion request was made; no latency, quality or model-output
  number is claimed anywhere in the fragment or the row. The row says so explicitly.
- **Point-in-time.** Every fact above is a 2026-10-28 capture. The row carries `PINNED 2026-10-28`;
  a later absence is host state and shows up as `STALE`, which the claims declare intended.
- **No production edit.** `PROVINCE.md`, `plans/round51-surfaces.json` and
  `plans/round51_surfaces.py` were read from the lane and modified only inside the scratch clone. No
  commit, no `git` mutation outside the scratch clone, no pacman, no tool installed.
- **The lane working tree was not mine to read as truth.** `git status` shows sibling edits
  (`plans/round42_c1_verify.py`, `plans/routed_open.py`, `plans/scratch_guard.py`); none touch the C1
  surface files, and the clone measured the committed tip.

## 5. Scratch

`/fast/scratch/hyaku/kengaku-r51/C1ExecNewSurface` was created, `TMPDIR` exported to it, one
`--shared` clone (578 MB) built inside it, and the whole directory **removed before this report**:
`ls -d /fast/scratch/hyaku/kengaku-r51/C1ExecNewSurface` → `No such file or directory`. Free space
observed on `/fast`: `804G` total, `257G` used, `547G` free (32% used), before and after removal.
Nothing of this seat remains on disk outside the two files it was told to write.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: the new surface is declared honestly as host state pinned at capture — the LFM3 router
`http://127.0.0.1:1234` (machine-checked by an `http` probe on `/health`, 200) with its served
`LFM3-1.7B` instance on `127.0.0.1:45669` recorded as capture-time state, not a capability; landed as
`SF20` plus one `## Surfaces` row it moves `ANCHORS` 19 → 20 (`dup=0`, `missing=0`), `## Surfaces`
rows 9 → 10 (`uncovered=0`) and `RESOLVE` 13 → 14 while adding zero problems, so the C1 predicate's
remaining `fail` at the measured tip is exactly the L1's five pre-existing corrections.
