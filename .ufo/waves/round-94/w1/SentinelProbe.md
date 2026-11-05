# SentinelProbe — round-94 security/hygiene findings (T 90c7677f0ba95d0930d93bda6a14aa50605ebe2e)

Full report with commands and outputs: `w1/SentinelProbe/report.md`; raw receipts in
`w1/SentinelProbe/receipts/`. Lane untouched (`git status --porcelain` clean; read-only git only).

**Check 1 — sandbox isolation: PROVEN, no escape.** `round94_compressor_probe.py:103-109`:
`--unshare-all --tmpfs / --ro-bind /usr --ro-bind /etc --dev /dev --proc /proc --tmpfs /tmp` plus
per-leg binds sourced only under `--work` (build `<work>/ref→/work` line 121; cases
`<work>/cases/<id>/{app→/app, tests→/tests ro}, harness.py ro` line 174). Receipt-grade bwrap argv
captured via strace execve. Official run under `strace -f -e trace=file,network` (43,069 events,
rc 0, mismatches 0): zero successful write paths outside `--work`-binds and in-ns pseudofs/tmpfs;
only stragglers are bwrap's own `/newroot/*` pivot staging; **0 AF_INET/AF_INET6 sockets** (9
kernel-internal AF_NETLINK getifaddrs-style exchanges, 127.0.0.1 only). Canary battery importing
the instrument's own `sandbox()`: writes succeed only in-ns (/ tmpfs, /work, /app; land in my
scratch), `/usr` `/etc` `/tests` EROFS, `/home` `/root` `/fast` `/var` ENOENT, host leak checks all
False; AF_INET connect → "Network is unreachable". Host `/tmp` zero gcc residue; `~/.cargo`
mtime untouched, `~/.rustup` absent. Host `/app` exists but is empty root:root 755 (mtime
2026-11-05 05:17) and provably never referenced by the probe.

**Check 2 — rustc build leg: no host writes.** HOME=/tmp (in-ns tmpfs), single RW bind
`<work>/ref→/work`; artifacts (main, data.comp, full.rmeta) stay under `--work`; grader's gcc
temps are in-ns `/tmp/cc*`; no /proc/sys writes traced; reference reproduced
`3a905a56…9131` 2264 B, matching the committed divergence receipt.

**Check 3 — hygiene greps: clean.** Only `/tmp` occurrences are `--tmpfs /tmp` + `HOME=/tmp`
(in-ns by design); no tempfile/mkdtemp/TMPDIR; no absolute write targets beyond bind vocabulary.
Precision credential pattern (password|passwd|secret|api_key|AKIA…|BEGIN…PRIVATE KEY|ghp_|sk-|
Bearer|aws_access_key_id|credential) over 5 instruments + claims + 11 corpus files: **0 matches**
(bare `token` hits are Rust compression-token identifiers only).

**Check 4 — frozen table: 11/11 OK.** Table from `git show F:plans/round-94-claims.md` equals
`sha256sum` of every tabled path at T; claims file byte-identical F..T (empty diff). Files changed
F..T (SOURCES.md, compressor-probe.txt, decomp-opt-divergence.txt, grader-population-ledger.json)
are none of them tabled — frozen rule intact at T.

## Findings (routed, not repaired — none flips a verdict)

- FINDING SP-1 info Pre-existing empty root-owned host `/app` (mtime 2026-11-05 05:17) is not
  probe leakage — bind argv + strace + EACCES prove the probe never touches it; no action.
- FINDING SP-2 minor (round 95) Probe inherits the full operator environment into the sandbox
  (traced execve carries 273 vars; bwrap sets only PATH/HOME, no --clearenv): stray TMPDIR,
  CARGO_HOME, RUSTFLAGS, HTTP_PROXY reach the in-ns rustc/gcc. No host-write escape (unbound
  paths don't exist in-ns) and failure is visible (build failure → rc 2, or honest mismatch);
  no silent-false-pass path identified. Smallest remediation: pass a minimal env (or bwrap
  --clearenv). This round's verdicts unaffected (env vars absent; build reproduced reference sha).
- FINDING SP-3 info Host /usr and /etc readable read-only by the captured grader in-ns
  (toolchain/nss); no exfiltration channel (no net, 4-letter stdout payload, --work-only writes).
  Accepted trade-off; no action.
- FINDING SP-4 info Per-namespace kernel-internal AF_NETLINK RTM_GETLINK/GETADDR enumeration
  inside the empty netns; zero internet-capable sockets in 43,069 traced events; no action.

Tooling: nothing installed or upgraded (strace, bwrap 0.13.1, rustc/cargo present; pacman
untouched). One grep-tool anomaly (spurious one-off matches in c1_replay; unreproducible) filed to
the automated QA channel; all conclusions rest on repro'd outputs.
