writer: KengakuR29-2.FRevHistory-2

# FRevHistory — upstream history of scripts/generate_test_data.py and config_files/test.raw.json (web-arena-x/webarena)

## Attack
Falsify round-29 C1's provenance premise by checking, against live GitHub, that (a) the pinned
`upstream_revision` is a real upstream commit and is the current HEAD of the default branch;
(b) the pinned fixture bytes are byte-identical to upstream at that revision; (c) the generator's
six-token replacement set and its order are historically stable, i.e. the projection is anchored
to a real, un-moving source contract, and the raw file's token population is known at every
revision. Static fetch/hash/parse only; no upstream code executed.

## Method (access date 2026-10-21)
Endpoints (unauthenticated; User-Agent `r29-falsify-history`):
- `api.github.com/repos/web-arena-x/webarena/commits/HEAD` → 200
- `api.github.com/repos/web-arena-x/webarena` (default branch) → 200
- `api.github.com/repos/web-arena-x/webarena/commits?path=scripts/generate_test_data.py&per_page=100` → 200, list length 1
- `api.github.com/repos/web-arena-x/webarena/commits?path=config_files/test.raw.json&per_page=100` → 200, list length 18
- `api.github.com/repos/web-arena-x/webarena/commits/b454f2dcfdc62af07beebb832b04bf8991ca409f` (parents) → 200
- `raw.githubusercontent.com` file blobs at 20 revisions (18 raw.json + generator at release and head + raw.json at head)
- HTML commits pages `github.com/web-arena-x/webarena/commits/HEAD/{path}` ×2 (corroboration)
Scripts and persisted API responses (my scratch, durable evidence):
`.ufo/waves/round-29/scratch/falsify/FRevHistory/{probe_history.py, verify_head.py, head.json, gen_commits.json, raw_commits.json}`
Local references read: `plans/round-29-claims.md` (line 28), `plans/fixtures/r29/manifest.json` (lines 2, 7–8, 11–12),
pinned fixtures by sha256sum. Hashes are sha256 hex; counts are occurrence counts (Python `bytes.count`,
byte-substring occurrences) or parsed-JSON array lengths, as labeled.

## Observed findings
1. Pinned revision IS current HEAD. `manifest.json:2` upstream_revision = `dce04686a56253aefba7b18a4fa0937cf1dc987b`;
   API HEAD sha = same 40-hex, committer date 2025-11-26T21:15:59Z, message "Merge pull request #183
   from alzambranolu13/patch-2" / "Update README.md" (8 words, counted). Repo default branch `main`,
   pushed_at 2025-11-26T21:16:00Z. Prereg `round-29-claims.md:28` pins the same sha with 838 bytes.
2. Pinned generator bytes == upstream at head == upstream at its only commit. sha256 of local pinned
   `plans/fixtures/r29/generate_test_data.py` = `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`;
   raw fetch at `dce0468…` = same; raw fetch at `b454f2dc…` = same. 838 bytes.
3. Generator history: exactly 1 commit on main touches the file — `b454f2dcfdc62af07beebb832b04bf8991ca409f`,
   2023-07-25T10:30:29Z, message "release commit" (2 words, counted). That commit has parents `[]`
   (root commit). HTML commits page for the file shows exactly 1 commit link (same sha).
   ⇒ The six tokens `__GITLAB__ __REDDIT__ __SHOPPING__ __SHOPPING_ADMIN__ __WIKIPEDIA__ __MAP__` and
   their replacement ORDER (generator lines 9–14) were introduced 2023-07-25 at repo creation and were
   never modified upstream. Order matches `manifest.json` `replacement_order` and prereg lines 32–33.
4. Raw file history: 18 commits on main touch `config_files/test.raw.json`; oldest `b454f2dc…`
   (2023-07-25), newest `bb6e4c623e73b5b5ce3caeef82e00d3853de8189` (2024-03-14T00:07:33Z, "fix typo in
   intent", 4 words, counted). HTML commits page shows exactly the same 18 unique shas. Head commit
   `dce0468…` does NOT touch the raw file; the raw blob at head equals the bb6e4c62 blob.
5. Pinned raw bytes == upstream head bytes. Raw fetch AT `dce0468…` sha256 =
   `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` == `manifest.json:12` == local
   pinned `plans/fixtures/r28/webarena/config_files/test.raw.json` (880776 bytes).
6. Token introduction/population per revision (occurrence counts, oldest→newest):
   - release `b454f2dc…` 2023-07-25: GITLAB 524, REDDIT 336, SHOPPING 284, SHOPPING_ADMIN 333,
     WIKIPEDIA 0, MAP 133; total 1610; 812 tasks parsed.
   - pinned/head `bb6e4c62…` 2024-03-14: GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300,
     WIKIPEDIA 0, MAP 133; total 1435; 812 tasks parsed.
   All six tokens (as generator replacement targets) exist from the root commit; counts oscillated
   during 2023-09 merges (e.g. GITLAB 524 at `c1fc2738…` 2023-09-19 vs 385 at `730b4ddd…` 2023-09-20;
   content of `4b86d435…` and `3065fda6…` is byte-identical, file sha256 prefix `6087f4de052a`).
   `__WIKIPEDIA__` occurrence count is 0 at EVERY sampled revision — the sixth replacement is a no-op
   on this file throughout history.
7. index==task_id: True at release and at pinned (task_id int 0..811, 812 distinct). First probe run
   printed False — my script compared int ids to strings; corrected in verify_head.py. No upstream mismatch.
8. Interim upstream anomaly (history, not pinned state): raw version at `7a1f8d6f…` (2023-10-21,
   merge into new_eval) fails `json.loads` at line 9418 column 9 (char 279271); fixed by `3065fda6…`
   next day. The pinned blob parses cleanly.

## Mismatches
None. Three independent checks found zero value mismatches between the lane's pins and live upstream:
manifest:2/prereg:28 sha vs API HEAD (equal); fixture sha256 lines 8 and 12 vs upstream blobs at that
revision (equal); manifest replacement_order vs generator bytes at root commit (equal). The only false
intermediate in my own run was probe bug #7, corrected above; recorded for honesty.

## Attack-relevant notes for the round [INFERENCE where marked]
- The projection is anchored to the live tip: a "pinned a stale/dead revision" attack fails.
- Raw-token counts are revision-dependent (1610 → 1435 total), so any per-profile replacement-count
  claim is only valid for the pinned sha — the instrument pins bytes (sha256), which makes rebinding
  detectable. Consistent with prereg design. [INFERENCE: supportive, not a claim of correctness]
- F2's "remaining WIKIPEDIA token = 0" is trivially true historically (count 0 before replacement);
  F4's index==task_id held at release and at the pinned blob.

## Located quotes (word counts counted programmatically; all ≤25)
- `plans/fixtures/r29/generate_test_data.py:1` — "Replace the website placeholders with website domains from env_config" (9 words)
- commit `b454f2dc…` subject — "release commit" (2 words)
- commit `dce0468…` message — "Merge pull request #183 from alzambranolu13/patch-2 Update README.md" (8 words)
- commit `bb6e4c62…` subject — "fix typo in intent" (4 words)
- `plans/round-29-claims.md:28` — "primary scripts/generate_test_data.py at dce04686a56253aefba7b18a4fa0937cf1dc987b" (4 words)
- `plans/fixtures/r29/manifest.json:2` — "upstream_revision dce04686a56253aefba7b18a4fa0937cf1dc987b" (2 words)

## Disclosures
- I did NOT read `plans/config_projection.py` source (not needed for this item; stated per contract).
- Tooling: no packages installed or upgraded; pacman untouched. Used preinstalled python3 3.14.8 and
  curl 8.23.0. All writes confined to my scratch dir and this report.
- Observed facts above come from HTTP fetches dated 2026-10-21 and local sha256sum; anything marked
  [INFERENCE] is interpretation. HEAD status is a point-in-time observation as of access date.

VERDICT: PASS
