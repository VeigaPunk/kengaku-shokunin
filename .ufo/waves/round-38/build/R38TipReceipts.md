# R38TipReceipts — tip-receipt validator (assimilation of considerthese/2026-10-25 proposal 2(c))

**Seat:** R38TipReceipts (executor), kengaku round 38 wave 1.
**Source proposal:** `considerthese/2026-10-25.md:39-45` — "a tip-receipt validator (every `corpus/evidence/**`
receipt re-run and byte-compared), which would have caught D3 mechanically."
**Lane tip measured:** `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e` (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD`).

## What landed (one file, no lane edit)

| file | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-38/build/R38TipReceipts/tip_receipts.py` | 16788 | `f2a35b47d9e4d2ce3ec981dbb07a5c968d61d41c207ee32ecef4b9ea1932bcdd` |

Plus the three captured receipts in the same directory (`sha256sum` of the directory's files):

| captured receipt | sha256 |
|---|---|
| `tip-receipts-run.txt` (full pass, exit 0, 53.4 s) | `f1ebc2c1c34cf6885fcc72a06dbd2e9ea5e80a13f5be7e376a47a6aa772cce6f` |
| `tip-receipts-list.txt` (`--list`, no run) | `c2430028081d678bd385fd5c0ad5754fa0b75245462205a57be450739518b6f5` |
| `tip-receipts-tamper-control.txt` (one-byte-tampered receipt) | `4733d5c949cba743c99414680201ded9d2fa912fbab33f4b1b809a84b79b9d75` |

No `plans/`, `corpus/`, `SCORECARD.md`, `LOG.md` or registry file was touched; the lane was read only
(`git rev-parse`, `git ls-tree`, `git show`). Nothing was installed (no pacman transaction was attempted).

## Contract

```
python3 .ufo/waves/round-38/build/R38TipReceipts/tip_receipts.py --lane DIR [--work DIR] [--list]
        [--tamper REL[,REL]] [--only SUBSTR] [--jobs N] [--timeout S]
```

1. **Population, mechanical.** Committed candidates are `git -C LANE ls-tree -r HEAD --name-only
   corpus/evidence` filtered to basenames matching `probe*.{txt,log}` → **24** files. A candidate enters the
   byte-comparison only if `RECEIPTS` maps it to a committed probe script; every other candidate is still
   printed, one line each, as `skip reason=no-committed-re-run-command`.
2. **Command resolution is derived, not assumed.** For a mapped receipt the tool reads the script's own
   `Run as:` docstring line (the line `SKILL.md` §Gate/probe registry and `corpus/README.md` quote), splits
   it, appends `--lane .` if absent, and prints where the lane's committed text names the script and the
   receipt (`doc=<file:line>+<file:line>`). A table fallback exists per script and is reported as
   `origin=fallback` if used.
3. **Clean clone at the tip.** `git clone -q --shared LANE <work>/tip`, then `rev-parse --show-toplevel` must
   equal the clone and `rev-parse HEAD` must equal the lane's HEAD — otherwise `SETUP` and exit 2. Receipt
   bytes come from `git show HEAD:<rel>` (the blob of record, not a worktree file).
4. **Re-run, byte-compare.** Each probe runs in the clone with `cwd=<clone>`,
   `TMPDIR=TEMP=TMP=<work>/tmp/<slug>` (so `--work`/`TMPDIR` are honoured; there is no hardcoded `/tmp`) and
   `PYTHONDONTWRITEBYTECODE=1`; stdout is compared byte-for-byte. Verified: the clone is still clean after a
   full pass (`git -C <clone> status --porcelain` → empty).
5. **Verdicts.** `equal` (bytes identical), `differ` (first differing byte+line, or a non-zero probe exit),
   `skip` (named reason: `probe-script-absent`, `no-committed-re-run-command`, `dependency-missing:<exe>`,
   `declared-nonreproducible-absolute-scratch-paths`). A receipt of kind `temp-paths` is still re-run: both
   sides have `…/tmpXXXXXXXX` masked, so equality there is a claim bounded to embedded scratch paths and any
   other difference is still `differ`.
6. **Controls.** `--tamper REL` (repeatable) flips one byte of that receipt's committed bytes and re-compares
   the same fresh output; with no `--tamper` the cheapest `equal` receipt is used automatically. A control
   that answers `equal` exits 1. Exit 0 means no `differ` and a passing control; 1 a `differ`/failed control;
   2 usage/setup (not a work-tree root, no `corpus/evidence/`, absent `git`, clone failure, unknown `--tamper`).

## Evidence — full pass against a clean clone of the tip

Scratch (deleted before this report): `S=/fast/scratch/hyaku/kengaku-r38/R38TipReceipts`;
`git clone -q --shared <lane> "$S/lane"`; `test "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane"`
passed; HEAD `2c5f4e0b…`.

```
$ TMPDIR=$S python3 tip_receipts.py --lane "$S/lane" --work "$S/w"
tip 2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e
receipt corpus/evidence/probe-r19-P1-key1-quota.log skip reason=no-committed-re-run-command
… (18 more probe-r19-*.log lines, same reason) …
receipt corpus/evidence/round35/tb2-grader-probe.txt equal bytes=3399 exit=0 doc=corpus/README.md:259+SKILL.md:574
receipt corpus/evidence/round36/regex-log-probe-first-run.txt skip reason=declared-nonreproducible-absolute-scratch-paths (equal after masking) doc=SKILL.md:576+corpus/README.md:418
receipt corpus/evidence/round36/regex-log-probe.txt equal bytes=5907 exit=0 doc=SKILL.md:576+SKILL.md:576
receipt corpus/evidence/round37/git-webserver-probe.txt equal bytes=8529 exit=0 doc=SKILL.md:577+SKILL.md:577
receipt corpus/evidence/round38/build-pmars-probe.txt equal bytes=5537 exit=0 doc=plans/build_pmars_probe.py:4+plans/pkg-spec-r38.json:5
control receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ
note compared=4 declared_bounded=1 no_command=19
receipts=24 byte_equal=4 differ=0 skipped=20
exit=0        # wall 53.4 s, user 2m3.7s (`time` on the command above)
```

Per-receipt probe commands as resolved from the scripts' `Run as:` lines (each re-ran in the clone, exit 0):

- `corpus/evidence/round35/tb2-grader-probe.txt` ← `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` (`plans/tb2_grader_probe.py:12`), 18 cases, last line `cases=18 observed_pass=5 observed_fail=13 mismatches=0`.
- `corpus/evidence/round36/regex-log-probe.txt` ← `python3 plans/regex_log_probe.py --lane .` (`plans/regex_log_probe.py:14`), 24 cases, `cases=24 observed_pass=8 observed_fail=16 mismatches=0`.
- `corpus/evidence/round37/git-webserver-probe.txt` ← `python3 plans/git_webserver_probe.py --lane .` (`plans/git_webserver_probe.py:4`), 22 cases, `cases=22 observed_pass=9 observed_fail=13 mismatches=0`.
- `corpus/evidence/round38/build-pmars-probe.txt` ← `python3 plans/build_pmars_probe.py --lane .` (`plans/build_pmars_probe.py:4`), 22 cases, `cases=22 observed_pass=7 observed_fail=15 mismatches=0`.
- `corpus/evidence/round36/regex-log-probe-first-run.txt` ← same regex probe; differs from the fresh run only in the two `assertion=` strings that embed a recorded `mkdtemp` path (`/tmp/tmp68j2v92s/regex.txt`, `/tmp/tmp7c39pj0f/absent-regex.txt`), which the amended receipt masks as `<tmp>` — hence `skip` with that bounded claim, never silently `equal`.

## Controls

1. **In-tool byte flip (full pass, above):** `control receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ` — flipping one byte of the receipt blob changes the verdict from `equal` to `differ`. Same line every pass (deterministic choice = smallest `equal` receipt).
2. **End-to-end one-byte-tampered receipt** (a scratch clone whose commit carries the tamper; the lane and its index were never touched):

```
$ cp -a "$S/lane" "$S/lane-tampered"
$ python3 -c '…flip byte 2953 of corpus/evidence/round36/regex-log-probe.txt…'
tampered offset=2953 0x30->0x31
$ git -C "$S/lane-tampered" commit -qam "control: one byte flipped in the regex-log receipt"
$ git -C "$S/lane-tampered" rev-parse HEAD
f19289b7689b05797362f9aed1d13e9c1787c4c7
$ python3 tip_receipts.py --lane "$S/lane-tampered" --work "$S/w" --only round36/regex-log-probe.txt
tip f19289b7689b05797362f9aed1d13e9c1787c4c7
receipt corpus/evidence/round36/regex-log-probe.txt differ first_diff=byte 2953 (line 13) exit=0 doc=SKILL.md:576+SKILL.md:576
note compared=1 declared_bounded=0 no_command=0
receipts=1 byte_equal=0 differ=1 skipped=0
exit=1
```

3. **Setup refusals** (exit 2, no work done): `--lane <lane>/plans` → `SETUP: … is not a git work-tree root (rev-parse says <lane>)`; `--lane /nonexistent` → `SETUP: … is not a directory`; `--lane /home/vgpnk/Projects/shokunin` (a git root without `corpus/evidence/`) → `SETUP: … has no corpus/evidence directory: not a kengaku lane?`.

## Findings for the L1 (freshness axis)

1. **All four byte-class receipts reproduce at the tip** — round 35 (18 cases), round 36 (24), round 37 (22), round 38 (22). The round-38 C1/C2 counters' freeze claims therefore survive a fresh tip run of the probes themselves, not only of their digests.
2. **The round-38 receipt is not named in any registry/documentation line that also names its probe.** `--list` prints `provenance=plans/build_pmars_probe.py:4+plans/pkg-spec-r38.json:5`: the command is documented in the script, the receipt only in the spec. No committed line names both, and `SKILL.md` has no `build-pmars-probe` row yet (wave 1). This is the D3-class gap the proposal describes — a mechanical `registry=` check would flag it once the SKILL row exists to check against; today the gap is visible in the `doc=` field, not failing.
3. **`corpus/evidence/round36/regex-log-probe-first-run.txt` is reproducible only up to two embedded `mkdtemp` paths** (bounded above). A future receipt that embeds run-specific state should either be declared with the same bounded kind, or it will (correctly) be reported `differ`.
4. **19 `corpus/evidence/probe-r19-*.log` receipts have no committed re-run command** — they are live-endpoint fleet probes from round 19, and `SKILL.md:586` already states no registry entry claims a live host probe since 2026-10-15. They are printed as named skips, so the population boundary is visible rather than silently dropped. Adding a new probe receipt without a `RECEIPTS` row will surface the same way.
5. **Operational cost:** a full pass is 53.4 s, dominated by the r37 bubblewrap service probe (`--only round37`: 54.65 s wall). The other three are cheap under the same tool: `--only round38` 1.6 s, `--only round36` 0.7 s, `--only round35` 0.8 s (warm `uv` cache). It writes only inside `--work`.

## Limits and risks (stated, not hidden)

- The round-35 probe needs `uv` and `--with biopython==1.85`; a cold cache needs network. Absent `uv` the tool reports `skip reason=dependency-missing:uv`, not `differ` (verified only by inspection of that branch — `uv` is present here and the run completed).
- The round-37 and round-38 probes need `/usr/bin/bwrap` (present, mode 0755) and the round-38 one needs host `gcc`; both were exercised in the pass above.
- Masking is confined to receipts declared `temp-paths` (currently one file) and only to `…/tmpXXXXXXXX` runs, so it cannot launder a substantive difference in the four byte-class receipts.
- The `RECEIPTS` table is a small maintenance point: it is the only place that ties a receipt to its producer script. Drift is loud (unmapped receipts print as skips; a moved script prints `probe-script-absent:`), not silent.
- The probe's three documented usage lines (`--lane .`, `--dry`, `--smoke`) are not distinguished by the tool: it always takes the first, i.e. the full run.
- `--only` narrows both populations, so under `--only` the summary counts only the filtered receipts.

## Axis note (godspeed)

Axes: (a) mechanical coverage of committed receipts, (b) reproducibility at the tip, (c) control strength,
(d) operability (one command, no hardcoded paths, readable lines). Chosen moves improve all four: full
`probe*.{txt,log}` enumeration with named skips (a), clone-at-HEAD + byte compare (b), two independent
controls incl. an end-to-end committed tamper (c), `--list`/`--only`/`--work`/exit-code contract (d). The
kept-not-chosen alternatives were (i) invoking the existing counters V5/W5 instead of the probes (narrower
coverage, no new evidence) and (ii) silently dropping the r19 logs from the population (would hide the
boundary).

VERDICT: tip-receipts-4/24-equal
