# SentinelReceipts — kengaku r25 security sweep (read-only sentinel)

Scope: P1 `corpus/evidence/attrib-r2[123]-*.log` (9 files) plus `probe-r19-*.log` (19 files): 28 files, 4,816 lines, 619,920 B. The P1 bytes are identical in the worktree, 3f371d2 and 6180e4f (sha256 per file). `find corpus/evidence -type l` → 0.
Method: my own scanner, which covers 26 classes, never prints a value and keeps only per-run HMAC fingerprints, plus gitleaks 8.30.1 (`dir --redact=100`). Both passed a positive control. This sweep matches patterns only, as the contract requires. The r18 hygiene gate (`probe-r19-P6-zai.log:22`, "12 credentials checked") compares against real credential values, so it needs credential reads and I did not run it.

## 1. Credential material: none found (severity none)
- 0 hits for API keys (sk-, zhipu id.secret, ghp_/github_pat_, AKIA, AIza, xox*), JWTs, PEM private keys, bearer or KV secret values, cookie values or session-cookie names, `op://`/1Password/vault/keyring/secret-tool refs, emails, org/account/user IDs, RFC1918/CGNAT/tailnet/public IPv4, and IPv6.
- gitleaks over the 28 files: `scanned ~619920 bytes … no leaks found` (0 findings). On a control file with a synthetic ghp_ and AKIA key it reported 2 findings and exit 3. My scanner's control: all 7 seeded classes were detected.
- [auth header redacted to a length or "withheld" marker] probe-r19-P1-key1-quota.log:12; P2-servicetier.log:19,28,37,45,54,62,70; P4-glm.log:28,41,123; P6-zai.log:10; hyper.log:41,55; opencode-health.log:58 (session header also redacted); p1-listing-mismatch.log:85,90,97,102; quota23.log:25,34,41,50.
- [Set-Cookie redacted] probe-r19-P2-servicetier.log:20,29,38,46,55,63,71; P4-glm.log:125; P6-zai.log:11; P8-kimi-code-auth.log:11. In P1, `set-cookie` appears only as a header name; the instrument redacts the value (plans/attrib_probe.py:198).
- False positives excluded: synthetic password-shaped test prompt at probe-r19-shim-ds-run.log:109; prose at probe-r19-P6-zai.log:22, shim-ds-run.log:110, shim-glm-run.log:79,137, attrib-r21-ds-trials.log:154 and attrib-r22-legs-hyper.log:211.

## 2. Low-sensitivity identifiers (none can be used to authenticate)
- LOW [account plan, credit and usage metadata] probe-r19-P2-servicetier.log:20,29,38,46,55,63,71 (Codex-backend plan-type, credit-balance and usage-window headers). Exploit path: quoting these lines verbatim would publish the operator's subscription tier and exact balance at that timestamp; they give no auth capability. Fix: cite path:line and never paste the header line.
- INFO [account quota state] probe-r19-P1-key1-quota.log:7; quota23.log:27,43; p1-listing-mismatch.log:87,99.
- INFO [per-request upstream IDs: request/trace/log ID, CF-RAY, chatcmpl or error ID] probe-r19-P1-key1-quota.log:13,14; P2-servicetier.log:20,29,38,46,55,63,71; P4-devinleg.log:31; P4-glm.log:125; P6-zai.log:11; P8-kimi-code-auth.log:11; opencode-health.log:27,32,59; p1-listing-mismatch.log:86,87,91,98,99,103; quota23.log:26,27,35,42,43,51; shim-ds-run.log:43,51,69,76,78,80,101,109. In P1 there are 238 `"id_value"` fields in trial-record JSON, all outside the GT blocks.
- INFO [local username in a path] attrib-r21-glm-trials.log:153; attrib-r22-opencode-trials.log:53; probe-r19-P1-key1-quota.log:16. [local hostname in journal lines] probe-r19-shim-ds-run.log:23-25,53-55,86-88,111-114.
- INFO [loopback endpoint or local port map, not reachable off-host] P1: line :2 of 8 files, plus attrib-r22-legs.log:131, attrib-r22-opencode-trials.log:4,75,264, attrib-r23-stream-trials.log:228, attrib-r23-stream.log:419. probe-r19: P2-servicetier :6,15,24,33,41,50,58,66; P4-devinleg :7,18,23,28; P4-glm :3,26,39,116,121; P9-absent-port :8,9,11,13; devin-shim-seat :3,7,90,94,99; shim-ds-run :3,117,127-130,135-138; shim-ds-predictions :3,81,99; shim-glm-predictions :3,98; shim-glm-run :6,17,23,28,45,72,82,156.
- INFO [credential-store path reference, no value] probe-r19-P2-servicetier.log:9; hyper-predictions.log:32; quota23.log:8.
- INFO [public provider hosts only; generic paths with no query string, userinfo or account segment] P1-key1-quota :10; p1-listing-mismatch :10,20,83,88,95,100; quota23 :23,32,39,48; P6-zai :7; P8 :7,20; hyper :4,39,49; hyper-predictions :39,48; opencode-health :6,24,30,54.

## 3. What C1 can quote: safe
- The 10 `## GT + scoring at close` blocks (r21-impl-ds ×4, r21-impl-glm, r22-legs ×2, r22-opencode, r23-stream ×2) contain only 64-hex digests and class words. Every table cell comes from a fixed vocabulary: class (7 values); prediction (5 legs); GT (5 legs + `EXCLUDED:UNMATCHED|AMBIGUOUS(N)`); gt_class {served, —}; chain `N/<leg> OK|FAIL <status>`; correct {YES, —}. Non-table lines are only ACCURACY, TARGET, BODY, GT counts, loo, mimicry, score_summary and journalctl (user unit + epochs).
- Rule for C1's knowledge entry and report: GT blocks and `#` header lines can be quoted verbatim. Do not paste trial-record JSON (`id_value`) or the two home-path lines.

## 4. Network use by the planned instruments
- The checks the instruments depend on all ran offline. I ran each in a `git archive 3f371d2` extract under /tmp (lane tree untouched) under `unshare -rn`, a PEP-578 audit hook and `strace -e socket,connect,sendto`:
  `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1`, `VERDICT: PASS`, exit 0, `net=0 proc=0 writes=0`, 0 socket syscalls.
  `python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` → `block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK`, exit 0, net=0 proc=0 writes=0, 0 socket syscalls.
  `bash scripts/sources-census.sh validate --root <scratch fleet> kengaku` → `kengaku ok`, exit 0, 0 socket syscalls.
- No draft of `plans/attrib_calibration.py` or `plans/state_check.py` exists anywhere under /tmp (find, mmin 240), so their own no-network property is UNTESTED. Their inputs (committed receipts and docs) and their math (stdlib) need no network (claims :33).
- The only network-capable code these instruments could reach is in attrib_probe.py: :45 (`HTTPConnection` import), :209 (capture() connects to the 127.0.0.1 shim) and :886 (`journalctl` subprocess). Fix: attrib_calibration must not import attrib_probe.
- MEDIUM, if built that way [command construction]: state_check P2a runs "the row's offline command" from SCORECARD.md:555-557. If it shell-evaluates the cell text, a doc edit (`…; <payload>`) becomes code execution in every reviewer's session, on a host with passwordless sudo. Fix: hardcode the 3 argv lists, shell=False, cwd=--root, with a timeout.
- LOW [path resolution] P2d: the URLs at PROVINCE.md:14,17 must be counted offline_unverifiable, with no DNS lookup or connect. Tilde paths (PROVINCE.md:12-17) should be stat-only, never opened. The P2 docs contain no credential-store pointer (grep over SCORECARD/SHONEN/PROVINCE/corpus README: 0).
- LOW [untrusted records] Expanding the P1 glob `attrib-r2[123]-*.log` at runtime would pull in any matching file landed later. Fix: pin the 9 names + sha256 and exit 1 on drift.
- Gate to add: `unshare -rn python3 plans/attrib_calibration.py --summary` and `unshare -rn python3 plans/state_check.py --summary` (and `--selftest`) must reach their contracted exits.

Mutation: nothing written in the lane; I used only `git archive`/`cat-file`/`ls-tree`/`rev-parse` object reads. Scratch: /tmp/sentinel-r25-SentinelReceipts (scan.py, view.py, audit_run.py, gitleaks.json).
Installs: none (gitleaks 8.30.1-1 was already installed; no pacman transaction).

VERDICT: CLEAN for the scanned classes. No credential, cookie, op:// ref, non-loopback private URL or account ID in the 28 receipts, and C1's GT blocks are safe to quote. The dependencies run offline in a netns. The two planned instruments are not built yet (network UNTESTED): gate them under `unshare -rn` and hardcode the P2a argv.
