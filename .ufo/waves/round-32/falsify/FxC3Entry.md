# FxC3Entry — C3 entry refresh vs frozen predicate and catalog_probe entry check

Seat: `L1Kengaku32.FxC3Entry` (leaf reviewer, 2026-10-25). Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. No production edit made; the only file
written by this seat is this report. No tool installed/upgraded (Python 3.14.8 stdlib +
read-only git only).

## Scope

Verify the planned C3 refresh — `corpus/knowledge/open-model-catalogs.md` gained
`verified-at: 2026-10-25`, S101/S102 source lines, receipt pointer
`corpus/evidence/round32/catalogs/` — satisfies (a) the frozen C3 predicate
(`plans/round-32-claims.md:95-111`) and (b) `catalog_probe.py`'s `entry_ok` check.

## What passes (verified)

1. **Baseline before-state (predicate clause).** `git show f20a1097:corpus/knowledge/open-model-catalogs.md`
   contains no `verified-at: 2026-10-25` and no `S101`/`S102` (grep: 0 hits). ✓
2. **Entry bytes (draft, on disk, uncommitted).** Lines 1–3:
   - `source: S101 — https://huggingface.co/api/models … 2026-10-25 (receipt: corpus/evidence/round32/catalogs/after.txt)`
   - `source: S102 — https://openrouter.ai/api/v1/models … 2026-10-25 (receipt: corpus/evidence/round32/catalogs/after.txt)`
   - `verified-at: 2026-10-25`
   All three `entry_ok` conditions pass: `^verified-at: 2026-10-25\b` (multiline) matches
   line 3; `S101`/`S102` substrings present; `corpus/evidence/round32/catalogs/` present.
   `entry_ok` returns `ok` — confirmed by a live run (below). ✓
3. **Registry rows S101/S102 (drafts).** Both rows exist in `corpus/SOURCES.md` with cells
   `mined | 2026-10-25 | 180d | corpus/knowledge/open-model-catalogs.md`; anchors quote
   receipt `after.txt` lines. Fleet census `sources-census.sh validate --file corpus/SOURCES.md
   --today 2026-10-25` → rc=0, the same 15 `W04` set as baseline (S040…S100), **no new
   E-code**, no new W-code (E11 resolves: used-by path exists on disk). ✓
4. **Recorded schema deltas and OR count (the hint in the assignment).** The draft does carry them:
   - HF delta: `:22-28` — `author`/`sha`/`lastModified`/`gated` gone from the default
     projection, present with `?full=true`; new fields `_id`/`createdAt`/`modelId`/`private` listed.
   - OR: `:37` count **467** (vs 460), `:43` "All twelve fields still present on 2026-10-25". ✓
5. **Probe facts match controls.** Live run (see §Gap) printed `hf_models=50 or_models=467`,
   matching freeze control `catalogs-before.txt:3` (`hf_models=50 or_models=467
   hf_schema_delta=4 or_schema_delta=0`) and build `R32CatProbe.md` (HF default projection
   missing the four fields; `?full=true` restores them; OR 467, all twelve fields present).

## Gaps

**G1 (blocking) — the frozen counting command cannot exit 0; the planned refresh cannot close C3.**
`python3 plans/catalog_probe.py --diff --lane .` was run on the current tree **with the
refreshed entry already present**:

```
probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=ok
HF missing fields: author, sha, lastModified, gated
probe_rc=1
```

`entry=ok`, yet exit 1. Cause: `catalog_probe.py` probes HF with the default `?limit=50`
projection (`HF_URL`, line 29) and requires all 11 `HF_FIELDS` (lines 34–37) in the first
item; the live API's default projection has lacked `author`/`sha`/`lastModified`/`gated`
all of 2026-10-25 (0/50 items — `R32CatProbe.md`; confirmed by the freeze control itself).
Exit is 0 only when both missing-field lists are empty (line 120), so `hf_schema_delta=4`
⇒ **exit 1 always**, independent of entry content. The frozen predicate requires the counter
to "exit 0" (`round-32-claims.md:97-98`); the freeze control already printed the same delta
with `exit=1` (`catalogs-before.txt:5`). Closing C3 therefore requires editing the counter
(e.g. HF probe with `?full=true`, or revising `HF_FIELDS`/exit condition) — a post-freeze
counter change against the "same condition in the counter's code" discipline, and a
contradiction with the lane's own planned after-target (`R32DraftScorecard.md` expects exit 0
with `hf_schema_delta=<n>`). A re-run of the unmodified counter at landing will produce a red
receipt (exit=1), not the predicate's line.

**G2 — receipt directory/file does not exist; raw captures scrubbed.** `corpus/evidence/round32/`
does not exist (glob: path not found). The entry and the S101/S102 anchors point at
`corpus/evidence/round32/catalogs/after.txt` (scorecard's after-slot names
`catalog-probe-after.txt` — two names, reconcile). `R32CatProbe.md` saved raw JSON under
`/tmp/r32-R32CatProbe/` and cleaned it after handoff, so the probe captures are gone. The
planned state must regenerate the receipts at landing; `entry_ok` does not check them, so an
empty pointer would still pass the counter but leave the claim's evidence dangling.

**G3 (minor) — entry omits the OR additive schema growth the probe report recommended.**
`R32CatProbe.md` §impact (ii) recommended appending the new OR item fields (`benchmarks`,
`default_parameters`, `description`, `expiration_date`, `links`, `name`, `supported_voices`,
`pricing.input_cache_read`, `architecture.input_modalities`/`output_modalities`, object-form
`reasoning`, top-level `total_count`/`links`). The draft records only "all twelve fields still
present" and the count. Not predicate-blocking (the predicate demands per-source delta
recording, which exists), but the entry is less complete than the probe's own recommendation.

**G4 (minor) — "model count" wording.** `hf_models=50` is a page length (`limit=50`), not a
total; the S101 row's scope cell says "model count". The entry itself makes no HF-total claim
(good); the row wording could mislead (already flagged as a mistake in `R32DraftMistakes.md`).

## Residual risk / verification gaps

- G1 is proven by a live run on the access date plus the freeze control; it is deterministic
  for the current API shape (default projection missing the four fields). If HF restores the
  default projection, exit 0 becomes reachable — that is outside the lane's control and not
  observable today.
- I did not verify the *content* of any receipt (none exist); the "after" receipt line quoted
  in the S101/S102 anchors matches the counter's stdout format, so regeneration is feasible.
- `--selftest` not run (not part of the counting command; code-path reasoning + live run
  suffice for the exit-code question).

VERDICT: gap
