# SecurityScan — round 65 w1 (kengaku) — security & scope scan

Seat `SecurityScan` (sentinel, leaf; no dispatch). Read-only over lane files. The only bytes written
are this report, the seat dir `.ufo/waves/round-65/w1/SecurityScan/` (findings + receipts), and a
scratch dir since removed. No network open, no port bound, no tool installed, no `git`/`jj` mutation.
**Tooling: none installed or upgraded** (host toolchain already sufficient; the pacman guard was
respected — no pacman transaction attempted), so there is no install to record under the tooling
directive.

Full findings with file:line citations and every observed value: `.ufo/waves/round-65/w1/SecurityScan/security.md`.
Receipts: `SecurityScan/scan-receipt.txt`, `SecurityScan/verify.txt`, `SecurityScan/scope-receipt.txt`,
`SecurityScan/landing-receipt.txt`, `SecurityScan/netns-probe.txt`.

## Findings

**M-1 (must fix) — the frozen C1 counting command accepts a hand-fabricated receipt with zero live-run data.**
`plans/round65_c1_sqlite_probe.py:649` (`receipt_failures`), `TOOLCHAIN` clause at `:677-686` checks
field *presence*, never a value; the `BUILD`/`RUN`/`FILES`/`NOBIND` clauses are presence-only too.
Independently reproduced by this seat:

```
$ python3 .ufo/waves/round-65/w1/ProbeBuild/round65_c1_sqlite_probe.py \
    --check-receipt .ufo/waves/round-65/w1/ClaimFalsifier/atk/fabricated.txt ; echo $?
CHECK ok cases=5
PREDICATE R65-C1 pass
rc=0
```
The accepted fixture (`ClaimFalsifier/atk/fabricated.txt`, 2 540 B) contains no compile, no sandbox, no
driver run and no file walk — its own lines read `TOOLCHAIN gcc=fabricated …` (:5) and
`RUN G1 driver="fabricated - nothing ran"` (:14). Impact: the scored predicate is discharged by
typeable text; the live witness the claims doc names (`plans/round-65-claims.md:126-129`) sits
outside the counting command. Smallest remediation, split by scope: **(a) in scope now** — pin
`gcc`/`gcov`/`bwrap`/`python` against the frozen literals `16.2.1 / 16.2.1 / 0.13.1 / 3.14.8`
(the frozen predicate already says "the host gcc/gcov version line"; the checker at `:684-686` accepts
any non-empty string) and bind the receipt to the probe sha `f44b7283…` — a wave-authored probe
change, no predicate change, L1-owned; **(b) out of scope, round 66** — requiring per-case
`.gcda`/`.gcno` hashes would add a counter the frozen predicate does not contain. Until (a) lands, the
C1 verdict must be stated as "predicate met on the text fields; live witness in
`corpus/evidence/round65/battery-run.txt`", never as "the counting command proves the run".
**Overlap with the landed lesson:** `corpus/lessons/round-65.md:63` (Mistakes row 5) already prices
this attack as a named limitation and routes the per-case-hash counter to round 66, and
`plans/round-65-claims.md` Amendment A1(e) carries it as a "named limit carried, not amended". This
finding asks for **no** R65-C1 rule change — it confirms the limitation is reproducible against the
landed checker and flags the one piece the lesson leaves un-routed: the `TOOLCHAIN` *value* check,
which needs no predicate change. Independently reported by `ClaimFalsifier` (`c1-attacks.txt:33-37`)
and `FreezeReview` (F5); recorded here because it is a predicate-forgery gap in the scored instrument.

**L-1 (note) — the bwrap sandbox shares the host network namespace.**
`ProbeBuild/round65_c1_sqlite_probe.py:387-398` builds the argv without `--unshare-net`. Measured:
sandbox netns `net:[4026531833]` == host netns; adding `--unshare-net` yields a distinct
`net:[4026533769]` (`SecurityScan/netns-probe.txt`). No egress occurred (grader imports only
`os`/`shutil`/`subprocess` per `corpus/evidence/round65/grader-import-scan.txt:3-5`; per-case listener
delta 0 and `probe_listening=0` in the receipt). 18 of the lane's 26 `plans/*.py` bwrap probes do use
`--unshare-net`. Smallest remediation: one flag in `sandbox_argv()` — hardening for a future round,
not a round-65 blocker.

**L-2 (note) — the TB2 canary GUID rides in two new byte files (benchmark data, not a credential).**
`GraderRecon/test_outputs.py.live:2`, `SourceReview/receipts/s232.py:2`, `s234.py:2` —
`# terminal-bench-canary GUID 26b5c67b-…`; 134 committed corpus files already carry the same GUID.
Recorded so it is not later mistaken for a credential; no remediation.

**L-3 (note) — sibling-lane credential-bearing *paths* are quoted into the wave receipts (no secret values).**
`SiblingOverlap/scan-receipt.txt:130` and `SiblingOverlap.md:85` quote
`sqlite3 -readonly ~/.omp/agent/skill-descriptions.db`; `:114` / `:30` quote
`live consumers = 1Password … and the /tmp seat DBs`. These are the only hits of the credential sweep
over every new byte; no key, token, cookie, session id, `op://`, `.netrc`/`.ssh`/`config/gh` path, JWT
or private-key block exists anywhere in the claims doc, the round-65 evidence dir or the wave dir.
Noted so the L1 knows a credential-bearing store path is now copied into kengaku's wave bytes.

**L-4 (note) — a third-party host list inside the captured download page (page content, no open).**
`sqlite-download-page.html:148,201,273,281,288-296,304-306` hyperlinks `fossil-scm.org`,
`www2/www3.sqlite.org`, `github.com/sqlite/sqlite`, `system.data.sqlite.org`, `www.tcl-lang.org`,
`sqlite.org/android`. Every URL *named* in the new bytes resolves to the two named opens only
(`https://sqlite.org` ×19, `https://raw.githubusercontent.com` ×10). No such link was opened.
Correction to the seat item's premise: the `grpc.github.io` URL belongs to row **S231**
(`corpus/SOURCES.md:247`, pre-existing r64 row) — neither S230 nor S234 carries it.

**L-5 (note) — scratch / tooling audit: clean.** No hardcoded host `/tmp` work-tree root in any new
byte (the `/tmp` occurrences are the in-sandbox `--tmpfs /tmp` and the sandbox `HOME=/tmp`);
every seat scratch lived under `/fast/scratch/hyaku/kengaku-r65/<seat>/` and was removed after the
receipts were copied. No `pacman` invocation anywhere (only negative statements). No `git push` /
`git commit` instruction to any seat (the single shape-matching hit is a negative gate line,
`LessonDraft.md:68`). No seat wrote outside its scope; `git status` in the lane confines the wave's
bytes to `.ufo/waves/round-65/w1/` plus the L1's own landing; the fleet root shows only the
orchestrator's `.scratch/*` state files; the two untracked `.ufo/waves/round-6{3,4}/w1.ready.dispatched`
markers predate the freeze (mtimes 15:04:43 / 16:10:54 vs the 17:04:37 freeze landing). No port bound,
no PID signalled.

**L-6 (note) — provenance nit: two receipts of record circulate with different digests.**
`ClaimFalsifier/c1-attacks.txt:3` / `falsifier.md:5` cite sha `103caa41…` for the path
`ProbeBuild/sqlite-gcov-probe.txt`, which now hashes to `25c7cab7…`. The two differ only in
`probe_pid` (3167591 vs 3169329) and three `elapsed_ms` values — two separate live battery runs, and
the L1 landed both (`corpus/evidence/round65/sqlite-gcov-probe.txt` = `25c7cab7…` = the receipt of
record; `replication-run2-receipt.txt` = `103caa…`; `plans/round54-entrytruth.json:1265` names both).
The landed receipt of record is byte-identical to the seat-dir original and passes the frozen
counting command (`SecurityScan/landing-receipt.txt` §L1f: `CHECK ok cases=5 / PREDICATE R65-C1 pass`,
rc 0). No remediation; recorded so two digests for "the receipt" are not a surprise.

## Verified clean

No credential material of any kind in the new bytes (sweep receipt `SecurityScan/scope-receipt.txt`
§S5). Only the two named opens appear in any new URL (L-4). Amalgamation zip listing is the four
expected members with no traversal entry, and the probe extracts by basename only
(`round65_c1_sqlite_probe.py:365`) — no zip-slip. No prompt-injection text in the captured page.
No `op://` reference anywhere. The four C2 counters read 1/1/2/1 at the landing tip, all edits
append-only (0 deleted base lines per file, `corpus/evidence/round65/a1-prefix-check.txt`).

SECURITY: findings M-1 L-1 L-2 L-3 L-4 L-5 L-6
