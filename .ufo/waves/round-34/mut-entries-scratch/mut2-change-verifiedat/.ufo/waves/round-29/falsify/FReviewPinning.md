writer: KengakuR29-2.FReviewPinning-2

# FReviewPinning — review of `read_pinned()` in `plans/config_projection.py` (round 29, lane master 56fd949a6478342531e61f4feecb4a685d831640)

Scope: the `read_pinned()` area only — the manifest pin persisted in code, the file-set/order check, the
read-once retained bytes, the missing / tampered / coherent-rebinding exits (2), "no other inputs", and
"no env/network reads".

## Method and honesty statement

- I **did read the production source** (`plans/config_projection.py`, lines 23–30, 94–114, 347–359,
  385–521, 524–544). The independence restriction in my contract applies to oracle/re-derivation items;
  this item is a code review and explicitly permits reading production source.
- All attack inputs were my own: `/tmp` copies of the pinned tree, plus `/tmp` copies of the instrument
  itself for the "repoint the constant" probes. I never wrote inside the lane except into my own scratch
  dir `.ufo/waves/round-29/scratch/falsify/FReviewPinning/` and this report file. No production file,
  fixture, corpus row, SOURCES/SCORECARD row, candidate, Git index or sibling lane was touched
  (`git status --porcelain -- plans/config_projection.py plans/fixtures/` is empty; HEAD = 56fd949a).
- Probe scripts (mine, in my scratch dir): `census.py` (audit-hook file/socket census + read-once
  counter), `mutate.py` (23-scenario mutation battery), `probe2.py` (order-authority and unbounded-read
  probes), `probe3.py` (profile/generator finding-reachability probes). All mutated trees live under
  `/tmp/r29pin*`.
- Tooling: **no install performed**. `python3` 3.14.8 (stdlib), `strace` and `unshare` were already
  present on the host (`/usr/bin/strace`, `/usr/bin/unshare`). No pacman/uv/cargo transaction was run, so
  there is nothing to record under the operator tooling directive.

## Baseline observed facts (all re-measured by me, not copied from receipts)

| Observation | Command | Result |
|---|---|---|
| `--summary` audit completes | `python3 plans/config_projection.py --summary` | exit 0, `TOTAL findings=0 exit=0`, 812 tasks × 3 profiles = 2436 |
| `--json` digest | `python3 plans/config_projection.py --json \| sha256sum` | `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` — identical to `corpus/evidence/round29-calibration/build-json-sha256.txt` |
| `--selftest` | `python3 plans/config_projection.py --selftest` | exit 0, `SELFTEST clean cases=20`, identical case list to `corpus/evidence/round29-calibration/build-selftest.txt` |
| pinned digests | `sha256sum` of the 4 pinned paths | manifest `f6390b92…bf87`, generator `45ddba7b…1cd`, raw `7b50386f…652`, profiles `90fdc34d…e018`; manifest digest equals `MANIFEST_SHA256` at `plans/config_projection.py:24` and the three file digests equal the manifest's own pins |
| read-once | audit-hook + `Path.read_bytes` counter over one `audit()` | exactly 4 reads, one per pinned path: `manifest.json`, `generate_test_data.py`, `test.raw.json`, `profiles.json` each count 1 |
| no other inputs | `strace -f -e trace=openat,open,connect,socket,unlink,rename,write` | under the lane only the 4 pinned files + the script itself are opened; **zero** `O_WRONLY`/`O_CREAT` opens, zero `socket`/`connect`, zero `unlink`/`rename`; non-stdlib opens outside the lane are interpreter/runtime artifacts only (`/etc/ld.so.cache`, `/etc/localtime`, `/usr/lib/libpython3.14.so`, …) — no `~/.netrc`, no `~/.aws`, no auth-state file |
| no env reads | `env -i /usr/bin/python3 plans/config_projection.py --json` | exit 0, output digest `c8da0c5a…4630` — byte-identical to the normal-environment run |
| no network | `unshare -rn /usr/bin/python3 plans/config_projection.py --json` | exit 0, output digest `c8da0c5a…4630` — byte-identical; strace shows no socket/connect syscall |
| CLI usage | `python3 plans/config_projection.py --summary --json` | exit 2 (argparse) |

Prereg obligations I checked against (`plans/round-29-claims.md`): line 32–33 (manifest digest
"independently persisted in the instrument, so coherent manifest/input rebinding cannot bless a new
population" — 15 words), line 52–55 (exit 0/1/2 taxonomy), line 57–60 ("Read each pinned input ONCE,
retain authenticated bytes, parse only those bytes" — 12 words; plus the stable-findings list), line
75–76 (selftest must cover missing/tampered input and coherent rebinding).

## Findings, by severity

### F1 — medium — The manifest pin is co-located with the code it protects; a coherent rebinding that repoints both is accepted and blesses a new population

Location: `plans/config_projection.py:24` (`MANIFEST_SHA256 = "f6390b92…bf87"`) and `:100`
(`if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:`).

Attack and observed values (`/tmp/r29pin/c02`, instrument copy at `/tmp/r29pin/c02_script.py`):

1. mutate `plans/fixtures/r28/webarena/config_files/test.raw.json` (insert `"extra": "__MAP__"` into
   task_id 0) → new raw digest `56c91c412bc02cfe55112b0f3c3d70decbc4043ddcfac5ab9c43e0b60bbd7638`;
2. update the manifest's own pin for that path and rewrite the manifest → new manifest digest
   `e74091e70d29adfe0ee45203aff5f8149aeab17473a101d727703b9d3780d62a`;
3. repoint the instrument's own `MANIFEST_SHA256` constant to that digest (one line).

Observed result: **exit 0, no findings**, `population.original_occurrences_by_token` =
`{"__GITLAB__": 385, "__MAP__": 134, "__REDDIT__": 336, "__SHOPPING_ADMIN__": 300, "__SHOPPING__": 281, "__WIKIPEDIA__": 0}`
— i.e. a **different population (133 → 134 `__MAP__` occurrences) is blessed and reported as the
audited one**, with `manifest_sha256` = the attacker-chosen digest and `inputs` = the attacker-chosen raw
digest. With step 3 omitted the same tree is correctly rejected (`exit 2, manifest_tampered`), and with
step 2 omitted it is rejected as `snapshot_tampered` — so the guard is real but lives entirely inside the
same mutable file as the logic it protects.

Prereg wording: the digest is required to be "independently persisted in the instrument", which the code
satisfies literally (outside the manifest). The instrument never cross-checks the *landed prereg copy* of
that digest, so the prereg's guarantee "coherent manifest/input rebinding cannot bless a new population"
holds only against rebinding that touches one of the two co-located files.

Compensating controls I verified exist elsewhere in the round (so this is a structural weakness, not an
open hole): the same digest is written into the landed prereg `plans/round-29-claims.md:32`; the build
receipt `corpus/evidence/round29-calibration/build-json-sha256.txt` pins the `--json` digest
`c8da0c5a…4630`, which my accepted-rebinding run does **not** match; and independently authored oracle
scripts pin the digest themselves
(`.ufo/waves/round-29/scratch/R29Task356/independent_projection.py:29`,
`.ufo/waves/round-29/scratch/KengakuR28.R29Task389-2/oracle389.py:18`, and others).
[INFERENCE] An independent second seat that re-derives the manifest digest from the landed prereg
would close this; the instrument alone does not.

### F2 — medium — `read_pinned()`'s hash pre-verification masks every downstream semantic check, so five of the seven prereg-required stable finding ids are unreachable through the CLI

Location: `plans/config_projection.py:111` (`snapshot_tampered`) is executed **before** the semantic
layer at `:349` (`source_contract`), `:350–351` (`check_profiles` / `check_values`) and `:296–299`
(`projection_json_invalid`).

Prereg requirement, `plans/round-29-claims.md:60`: "Include stable findings for missing input,
snapshot_tampered, manifest_tampered, profile_missing_key/type and projection_json_invalid."
(11 words). Observed CLI behaviour for each attempted deviation (`/tmp/r29pin3`):

| Injected deviation | Expected by prereg | Observed CLI finding (exit 2 in every row) |
|---|---|---|
| `profiles.json`: `MAP` key removed | `profile_missing_key` | `snapshot_tampered` |
| `profiles.json`: `MAP` = 7 (non-string) | `profile_invalid_type` | `snapshot_tampered` |
| `profiles.json`: extra profile key | `profile_unexpected` | `snapshot_tampered` |
| `profiles.json`: `MAP` = `http://x"y` (breaks JSON) | `projection_json_invalid` | `snapshot_tampered` |
| generator: `__GITLAB__`/`__REDDIT__` replace order swapped | `source_contract_unrecognized` | `snapshot_tampered` |
| generator order swap **and** manifest repinned | `source_contract_unrecognized` | `manifest_tampered` |

The same rows with **both** the manifest and the code constant repointed do produce the semantic ids —
`/tmp/r29pin4` gave `exit 2 {"id": "profile_missing_key", "key": "MAP", "profile": "distinct_origins"}`
— so the semantic layer is live code, but under the shipped pins it is reachable **only** through the
F1 co-located repin.

Consequences: (a) the prereg's named exit-2 case "unrecognized source contract"
(`plans/round-29-claims.md:54`) is not observable from the delivered CLI surface; (b) the four
`profile_*` ids and `projection_json_invalid` are not observable from the CLI either; (c) the
instrument's own selftest proves these ids only by calling `source_contract()` / `check_values()`
**in-process** (`plans/config_projection.py:468` and `:429`), never through `--summary`/`--json` — the
selftest's CLI case list is exactly `cli_snapshot_tampered`, `cli_input_missing`,
`cli_coherent_rebinding`, `cli_manifest_tampered` (20 cases total, `build-selftest.txt`).

Note the honest reading: the byte pin is *strictly stronger* than the semantic checks, so no
unauthenticated input can reach the semantic layer at all. The defect is that the prereg's required
diagnostic surface is not deliverable from the CLI as shipped, and that the round's evidence cannot
demonstrate it.

### F3 — low/medium — The manifest's file-set/order check is unreachable for manifest-side deviations; it only fires for a code-side `ORDER` edit

Location: `plans/config_projection.py:103`:
`if sorted(manifest["files"]) != sorted([GENERATOR, RAW, PROFILES]) or tuple(manifest["replacement_order"]) != ORDER:`
→ `manifest_contract_mismatch` (`:104`).

Observed:

| Deviation | Observed finding |
|---|---|
| manifest `files` gains a 4th path, code pin unchanged | `manifest_tampered` (byte pin at `:100` fires first) |
| manifest `replacement_order` reversed, code pin unchanged | `manifest_tampered` |
| instrument's own `ORDER` constant reordered (`/tmp/r29pin2/order_edited.py`) | `manifest_contract_mismatch`, exit 2 |

So the check compares **the manifest against the code**, not the code against the manifest; for the
direction that matters (a manifest that disagrees with the pinned set/order) it can never fire, because
the byte pin at `:100` short-circuits first. The effective order authority is instead the generator AST
comparison at `:84` (`[(s["token"], s["name"]) for s in steps] != [("__%s__" % name, name) for name in ORDER]`),
which compares the pinned generator bytes against the same code constant — that one is a genuine
cross-check (edit `ORDER` and the authentic generator is rejected, which is exactly the probe above, just
reported under the manifest id).
Also note `sorted(...)` on the file set is order-insensitive by construction, so the "order" half of the
file-set check rests entirely on `replacement_order` and on `source_contract`.

### F4 — low/medium — A resource failure in the pinned-input read path escapes as exit 1, which the prereg reserves for a projection/invariant finding; pinned inputs are read into memory with no size bound

Location: `:97` and `:108` (`read_bytes()`, whole-file, no size cap); `:538`
(`except (OSError, ValueError, KeyError, TypeError, AssertionError, IndexError)`) — `MemoryError` is
not in that tuple.

Observed (`/tmp/r29pin2` scenario C, address space capped at 400 MiB so the host is not at risk): the
pinned raw path replaced by a symlink to `/dev/zero` → **exit 1**, uncaught traceback ending in
`MemoryError` at `return f.read()`. Exit 1 is, per `plans/round-29-claims.md:54`, the code for "audit
completed with expected structural identities" failing with a finding; here the audit never completed
and produced no finding, so a crash is indistinguishable from a finding at the exit-code level. The same
unbounded read is reachable for the manifest itself (`:97`), and the manifest's byte pin is also checked
only after the whole file is in memory.

### F5 — low — Diagnostic granularity for non-regular pinned paths, and inconsistent detail fields

Location: `:98` and `:109` catch only `FileNotFoundError`; `:101` raises `manifest_tampered` with no
`path` field.

Observed: a pinned path replaced by a **directory** yields the generic
`input_invalid` — `{"id": "input_invalid", "detail": "IsADirectoryError(21, 'Is a directory')"}`, exit 2 —
for all three of GENERATOR, RAW and PROFILES, instead of the prereg's `input_missing` /
`snapshot_tampered` vocabulary. A broken symlink is correctly reported as `input_missing`. And
`manifest_tampered` carries no `path` detail while its siblings `input_missing` and `snapshot_tampered`
do, so a caller cannot tell *which* manifest surface failed.

### F6 — low / observation — The reported `upstream_revision` is the manifest's self-declaration and is never bound to the generator bytes

Location: `:357` (`upstream_revision=manifest["upstream_revision"]`) and `:356` (`inputs={path: pin["sha256"] …}`).
The manifest is byte-authentic, so these strings are authenticated *as manifest assertions*, but nothing
offline ties `dce04686a56253aefba7b18a4fa0937cf1dc987b` to the 838 pinned generator bytes; that
attribution is asserted, not verified. This is inherent to an offline pin and is consistent with the
declared scope, but the output prints it as provenance without any marker of that difference.

## What held under attack (positive controls)

1. **read-once retained bytes** — 4 opens total, one per pinned path, at both the audit-hook and the
   syscall level; the instrument never re-reads a pinned file for parsing.
2. **missing vs tampered vs coherent rebinding** all exit 2 with distinct ids, in `--json` and in
   `--summary` form: `input_missing` (path present), `snapshot_tampered` (path present),
   `manifest_tampered`, `manifest_contract_mismatch`.
3. **coherent rebinding with a single edited file is refused** — manifest repinned, input repinned,
   code pin untouched → `manifest_tampered`, exit 2, no population blessed (the exact attack the prereg
   names).
4. **no env reads**, **no network**, **no writes**: three independent measurements (empty environment,
   network namespace without interfaces, full syscall trace) all agree with the baseline digest
   `c8da0c5a…4630`.
5. **no other inputs**: the audit path touches exactly the four pinned paths; `plans/fixtures/r29/hand/`
   is read only by `--selftest`.
6. **exit taxonomy** holds for all reachable states: 0 = audit completed, 1 = finding, 2 =
   could-not-evaluate, argparse usage = 2.
7. The reviewed bytes are the committed bytes: `git status --porcelain -- plans/config_projection.py
   plans/fixtures/` is empty at HEAD `56fd949a6478342531e61f4feecb4a685d831640`.

## Residual risk and verification gaps

- The pinning chain is single-file: the manifest digest lives only in `plans/config_projection.py:24`.
  Any lane edit that repoints it *and* the manifest is accepted (F1). The compensating anchors are the
  landed prereg digest, the build receipt digest and the independently written oracle scripts — none of
  which the instrument consults.
- The semantic layer (source contract, profile validation, JSON validity) is unexercised through the
  CLI in the shipped state (F2). The selftest exercises it in-process only, so it does not demonstrate
  the CLI diagnostic surface the prereg names.
- `manifest_contract_mismatch` is not exercised by the selftest at all; my probe reaches it only by
  editing the instrument's `ORDER` constant.
- No probe can rule out a defect that requires the *authentic* pinned bytes to be internally
  inconsistent — by construction the pins make that unreachable, which is the point of F2.
- My mutation battery is 23 scenarios plus the reachability and resource probes; I do not claim
  exhaustive coverage of the input space.

## Scoped verdict

The pinning core of `read_pinned()` is sound for the shipped state: read-once retained bytes, no
environment or network reads, no writes, no other inputs, and correct exit-2 classification for missing,
tampered and singly-rebound inputs. Against that, five concrete contract-level defects remain: the
co-located trust anchor that accepts a coherent two-file rebinding (F1), five prereg-required stable
finding ids that the CLI cannot emit (F2), a manifest contract check that fires only in the direction it
was not written for (F3), a crash that reports itself as exit 1 (F4), and two diagnostic-granularity
defects (F5, F6). F2 and F4 are the ones that can be observed from outside the lane without editing the
instrument.

VERDICT: PARTIAL
