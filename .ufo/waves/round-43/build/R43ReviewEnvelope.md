# R43ReviewEnvelope — review of `claims/envelope.sh` content digest (closure R6/D5)

Seat: R43ReviewEnvelope, kengaku round 43 wave 1, 2026-10-26. Leaf seat; no subagents. No tool installs
(pacman paused; nothing needed). Scratch: `/fast/scratch/hyaku/kengaku-r43/R43ReviewEnvelope` (deleted at the end).
`~/.local/bin` was never written or mutated; all attack tests ran against a **copy** of the script whose digest
target is a scratch dir.

## Artifact under review

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/envelope.sh` (29 lines). The digest
(`bindigest()`, lines 14–19) pipes two listings into one `sha256sum | cut -c1-16`:

- line 16: `find . -mindepth 1 -maxdepth 1 -printf '%f %y %l\n'` — name, type, link target. **No mode bits.**
- line 17: `find -L . -mindepth 1 -maxdepth 1 -type f -print0 | sort -z | xargs -0 -r sha256sum` — content of
  regular files, stderr suppressed.
- line 26: `if [ "$before" = "$after" ]; then st=unchanged; else st=CHANGED; fi`
- line 28: `[ "$st" = CHANGED ] && { echo "ENVELOPE measurement INVALID …"; exit 4; }`

## Method

Copied the script to `$S/env-copy.sh` with exactly one line changed — the digest `cd` target is now
`cd "${ENV_BIN:-/home/vgpnk/.local/bin}"` (verified: `diff` shows only line 15). Each test builds a fresh
fixture dir, then runs the copied envelope with a command that mutates the dir from inside the run (bwrap binds
the scratch dir writable, so the mutation succeeds — the real script's ro-bind of `/home/vgpnk` is why this
cannot be tested in place). Untouched-envelope baseline on the real host home:

```
ENVELOPE start 19:17:26 cwd=/fast/scratch/hyaku/kengaku-r43
ENVELOPE end 19:17:27 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
REAL_EXIT=0
```

## Results — the four attacks (command runs inside the envelope)

| # | Attack | Command | before → after | Line | Exit |
|---|--------|---------|----------------|------|------|
| T1 | rewrite existing entry | `echo evil-backdoor > "$ENV_BIN/git"` | `6208b082… → afe83cad…` | `CHANGED` + `INVALID` | **4** |
| T2 | new file | `printf … > "$ENV_BIN/evil-tool"` | `6208b082… → 9ab6560f…` | `CHANGED` + `INVALID` | **4** |
| T3 | symlink retarget | `ln -sfn targetB "$ENV_BIN/g"` | `ec2b6e97… → 349bf4d1…` | `CHANGED` + `INVALID` | **4** |
| T4 | mode change | `chmod 644 "$ENV_BIN/git"` | `6208b082… = 6208b082…` | `unchanged` | 0 |

T1 raw (T2/T3 same shape):

```
ENVELOPE end 19:18:17 exit=0 local_bin_content_before=6208b08215bbea0f after=afe83cadbd106ea0 CHANGED
ENVELOPE measurement INVALID (PATH dir content changed while it ran)
T1_EXIT=4
```

T4 raw:

```
ENVELOPE end 19:18:17 exit=0 local_bin_content_before=6208b08215bbea0f after=6208b08215bbea0f unchanged
T4_EXIT=0
```

**Detected 3 of 4.** Exit 4 fires on every CHANGED (line 28) and overrides the command's own exit status; when
unchanged the command's rc propagates (`/bin/false` inside an unchanged envelope → `exit=1`, `T8_EXIT=1`).

## False-CHANGED probes

| # | Fixture | Command | Result |
|---|---------|---------|--------|
| T5 | broken symlink (`dangling → /nonexistent-target`), mode-000 file, symlink-to-dir | `/bin/true`, run twice | `unchanged` twice, exit 0 both |
| T6 | mode-000 file, content rewritten via `chmod 644; echo …; chmod 000` | mutation command | `unchanged`, exit 0 — **missed** |
| T7 | symlink loop (`ln -s loop loop`) next to a normal file | `/bin/true` | `unchanged`, exit 0 |

**False CHANGED: 0.** Broken links, unreadable entries and loops are digested stably (line 17's
`2>/dev/null` + the name/type listing at line 16 absorb them); rerunning T5 reproduced the identical digest
`75928e296245de73`, so the detection is state-, not run-, dependent.

## Findings

1. **[defect, T4] Mode change of an existing entry is invisible.** Line 16 prints `%f %y %l` — name, type,
   link target — but no mode; line 17 digests content only. `chmod 644` (dropping the execute bit that makes a
   PATH entry *usable as a command*) passes with `unchanged`. Round-40's threat (a planted `git` shim) is
   covered for new files, but an in-place `chmod -x` of the real `git` would not be flagged.
2. **[defect, T6] Content of an unreadable entry is invisible.** A `sha256sum` failure at line 17 is suppressed,
   so a mode-000 entry contributes no content line. A rewrite with the mode restored afterwards (as an outside
   actor could do to `~/.local/bin`, which is only ro-*bind*ed inside bwrap, not protected outside it) leaves
   `unchanged`. T6 demonstrates exactly that with `stolen-secret`.
3. **[ok] Everything asked works:** content rewrite, new file and symlink retarget are all detected with exit 4
   and the INVALID line; no false CHANGED from unreadable entries, broken links, dir-symlinks or loops;
   unchanged runs propagate the command's exit status.

Minimal fix for both defects (L1's call, envelope is frozen for claim purposes): add mode to the listing
(`-printf '%f %y %m %l\n'`) and feed unreadable regular files a placeholder line (e.g. append
`unreadable <name>` per `-type f ! -readable` entry) so both a mode flip and a readability flip change the
digest; full content coverage of mode-000 files would additionally need a privileged digest pass.

## Residual risk / verification gaps

- Tested on the one-line-patched copy, not the frozen file itself (the target path is hard-coded); the `diff`
  is quoted above and the untouched script's own run (baseline) agrees with the copy's no-change behavior.
- TOCTOU window is inherent: both listings are taken by the same shell before/after, so a mutation and
  re-mutation inside one command run is invisible — not exercised, out of scope.
- Host `~/.local/bin` was only ever read by the untouched envelope; no PATH dir was modified (host-safety rule
  respected; digest `328be01808ba022f` before/after).
- Scratch cleaned with `python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r43 R43ReviewEnvelope $S`.

VERDICT: envelope-detects-3/4-false-changed-0
