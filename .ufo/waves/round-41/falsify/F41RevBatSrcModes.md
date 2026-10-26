# F41RevBatSrcModes — non-author honesty review of `plans/battery41/s_modes.py` (S01, S04, S08, S09)

kengaku round 41, wave 2 (falsify), 2026-10-26. Critic seat. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`;
clone `/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcModes/lane`, `git rev-parse --show-toplevel` =
`/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcModes/lane`, `HEAD d7c7789` (assigned tip `3d0058fb` + the wave-2
dispatch commit; `git -C $S/lane diff --stat 3d0058f d7c7789 -- plans/ corpus/` is empty, so every file I tested
is byte-identical at the assigned tip). Target module digest `1023433bbc173d1db9d42729b527dbbc1a602c6860efd6c06c3896690ec6bdd1`,
identical in the lane, the clone and the wave-1 report. Pins in the clone: `e4f4971…` (tip_receipts), `38492bf…`
(sources_adopt) = the counter's `PINS` literals; counter run printed `PINS total=2 mismatched=0`.

Every counter run and every fixture run below went through the host envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
--unshare-pid --die-with-parent`; the tool runs add the counter's own read-only sandbox
(`--ro-bind / / --unshare-pid --unshare-net`, one fixed slot, private TMPDIR). No write outside my scratch and this
report dir; nothing installed; `~/.local/bin` untouched.

## Answer up front

All 8 fixtures are **honest**. Each demonstrates exactly the guard its comment names: the reference exits 2 with
that guard's own `parser.error`/`QUOTE problem=` message, and the mutated line demonstrably executes on the killing
fixture. No fixture touches a wave-1 counterexample vector: the module has zero imports, opens nothing, uses no
probe stub, and every verdict is the real tool's exit code. Attribution replays: `killed=4/4` with
`by=` the fixture the wave-1 report predicted. One calibration caveat (not a defect): S08's two fixtures kill via an
uncaught `AttributeError` (mutant rc 1), so their evidence is "the guard is load-bearing", not "the unguarded run
refuses gracefully" — disclosed already in the wave-1 report's risk 1.

## 1. Attribution in my clone (only this module)

```
$ bwrap … /usr/bin/python3 $S/lane/plans/round41_c1_verify.py --lane "$S/lane" \
    --battery-dir "$S/bat" --only S01,S04,S08,S09 --work "$S/w"
PINS total=2 mismatched=0
FIXTURE s_modes-s01-quote-plus-package tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s01-quote-plus-registry-and-package tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s04-url-map-with-adopt tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s04-url-map-with-check-only tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s08-quote-file-without-artifact tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s08-artifact-without-quote-file tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s09-url-map-nested-shape tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s09-url-map-directory tool=sources expect=error declared=- observed_rc=2 observed=- ok
MUTANT S01 sources 2>0 killed by=s_modes-s01-quote-plus-package -- …
MUTANT S04 sources 2>0 killed by=s_modes-s04-url-map-with-adopt -- …
MUTANT S08 sources 2>1 killed by=s_modes-s08-quote-file-without-artifact -- …
MUTANT S09 sources 2>9 killed by=s_modes-s09-url-map-nested-shape -- …
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=0/0 sources=4/4
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0
```

Receipt: `counter-only.txt` (this dir). The `killed by=` line is the measurement itself: for a digit pair
`exhibits()` requires `want == A and ref[0] == A and mut[0] == B` (`round41_c1_verify.py`, `exhibits`). So this is
`2>0`, `2>0`, `2>1`, `2>9` measured, not inferred.

## 2. Mutated-line execution (independent of the counter)

I rebuilt all 8 fixtures from the module's own `build()` functions with a minimal `Ctx.write` shim into
`$S/fx/f000…f007`, then ran, per fixture, (a) the unmodified tool, (b) the exact frozen mutant copy, and (c) a copy
with `sys.stderr.write("SITE-<M>-REACHED")` inserted **immediately before** the mutated line, all in the counter's
read-only sandbox at one fixed slot. Harness: `probe.py`, receipts `probe-out.json`; second pass with reference
messages / exception types: `probe2.py`, `probe2.txt`.

Marker matrix (`Y` = the mutated line executed on that fixture):

```
fixture                                        S01 S04 S08 S09
s_modes-s01-quote-plus-package                 Y   .   Y   .
s_modes-s01-quote-plus-registry-and-package    Y   .   Y   .
s_modes-s04-url-map-with-adopt                 .   Y   .   .
s_modes-s04-url-map-with-check-only            .   Y   .   .
s_modes-s08-quote-file-without-artifact        .   .   Y   .
s_modes-s08-artifact-without-quote-file        .   .   Y   .
s_modes-s09-url-map-nested-shape               Y   .   Y   Y
s_modes-s09-url-map-directory                  Y   .   Y   Y
```

Every killing fixture executes its own mutated line: S01→f000, S04→f002, S08→f004, S09→f006. The marker copies
are non-intrusive: each of the 32 marker runs returned rc 2, the reference class, so the inserted `stderr.write`
did not change the tool's trajectory. The extra `Y`s are
the two quote-mode guards sharing the quote-mode path (`:1018` pairing runs before `:1022` exclusivity; `:1027` map
problem sits inside quote mode) — they do not create cross-kills, because each mutant still exits 2 on the other
guard's fixtures (matrix below). This closes the wave-1 **dead-site** counterexample (T03/T04 §3) for all four
mutants.

## 3. Per-fixture review (8/8)

Evidence columns: reference's own refusal line (last stderr line, or the `QUOTE problem=` stdout line where the
tool refuses on stdout); the mutant's measured rc and stdout; verdict.

### 3.1 `s_modes-s01-quote-plus-package` — **honest**
- Advertised (`s_modes.py` comment): "quote mode combined with --package. The exclusivity guard refuses (2); an
  unguarded run silently drops the package work, validates the quote and exits 0."
- Reference rc 2, stderr `sources.py: error: --quote-file/--artifact cannot be combined with --registry/--package`
  → the S01 site (`plans/sources_adopt.py:1022`, mutant old `        if args.registry or args.package:`).
- Mutant rc 0, stdout `QUOTE rows=1 spans=1 located=1 found=1 … ok S901 words=9 at b-capture.txt` and **no**
  registry/package line: the package work is silently dropped and the quote is the only thing validated. Matches
  the comment's claim exactly.
- MARK: `SITE-S01-MARK-REACHED` present. No vector: data-only fixture, real tool.

### 3.2 `s_modes-s01-quote-plus-registry-and-package` — **honest**
- Comment: "quote mode with BOTH --registry and --package, and a --url-map that would bind the quote correctly --
  a combined invocation must still refuse (2), not exit 0."
- Reference rc 2, same exclusivity message. Mutant rc 0, stdout includes
  `mismatch=0 unmapped=0 urlmap=r41-url-map.json` and `bound=b-capture.txt->https://example.invalid/r41/spec` —
  i.e. the map really does bind, so the mutant's 0 is a *successful*, not a degraded, quote run. The comment's
  "would bind the quote correctly" is verified, not asserted.
- MARK present. Second independent trigger (registry side added).

### 3.3 `s_modes-s04-url-map-with-adopt` — **honest**
- Comment: "--url-map in registry mode with a complete adopt request. The ignored-map guard refuses (2); an
  unguarded run checks, builds the block and exits 0."
- Reference rc 2, stderr `sources.py: error: --url-map needs --quote-file and --artifact` → the S04 site
  (`sources_adopt.py:1039`). Mutant rc 0, stdout `registry=2 staged=1 collisions=0 …` plus the built row
  `| S905 | https://example.invalid/r41/spec | … | mined | 2026-10-26 | 180d | corpus/knowledge/r41-fixture.md |`.
  The advertised bug (map accepted and silently ignored while the adopt completes) is exactly what is shown.
- MARK present. The only relative argv token in the module is `--entries corpus/knowledge/r41-fixture.md`; it has
  no `..`, the counter runs with `cwd = fixture dir`, and `build_block` only joins it into the `used-by` cell
  (`used_by = ", ".join(admitted_entries)`), so it neither escapes nor reaches outside `d`.

### 3.4 `s_modes-s04-url-map-with-check-only` — **honest**
- Comment: "--url-map with a clean check and no --admit-ids. Reference refuses (2); the unguarded run reports the
  registry counts and exits 0 on the check alone."
- Reference rc 2, same `--url-map needs --quote-file and --artifact`. Mutant rc 0, stdout
  `registry=2 staged=2 collisions=0 malformed=0 duplicates=0 defects=0 prose=0` and nothing else — "exits 0 on the
  check alone" measured. MARK present. Independent trigger from 3.3 (adopt path absent).

### 3.5 `s_modes-s08-quote-file-without-artifact` — **honest (weakest of the eight; disclosed)**
- Comment: "--quote-file without --artifact (plus a readable map). The pairing guard refuses (2); an unguarded run
  reaches the quote check with no artifact and dies on it (1)."
- Reference rc 2, stderr `sources.py: error: --quote-file and --artifact must be given together` → the S08 site
  (`sources_adopt.py:1018`). Mutant rc 1, empty stdout, stderr is a Python traceback ending
  `AttributeError: 'NoneType' object has no attribute 'is_file'` inside `quote_check`→`load_artifact(artifact)`.
  The comment says "dies on it" and that is literally what happens, but the kill is carried by an uncaught
  exception, not by a graceful rc-1 refusal. That is the wave-1 report's own risk 1, restated here as a limit of
  the fixture's evidence, not a hidden one.
- MARK present. Why this is honest rather than incidental: the crash is a *consequence of the removed line* (the
  guard exists to stop exactly this call with `None`), it happens in the function the comment names, and the
  reference refusal is that guard's own message. It would be incidental only if the crash could occur with the
  guard intact — it cannot (all other fixtures run the same `quote_check` without a traceback).

### 3.6 `s_modes-s08-artifact-without-quote-file` — **honest (same caveat)**
- Comment: "--artifact without --quote-file. Pairing guard refuses (2); the unguarded run loads the capture then
  dies on the absent rows file (1)."
- Reference rc 2, same pairing message. Mutant rc 1, traceback ending
  `AttributeError: 'NoneType' object has no attribute 'read_text'` after `quote_check` loaded the artifact
  directory — measured order is exactly "loads the capture, then dies on the absent rows file". This is the other
  operand of the same `and`, a genuinely independent trigger (a mutant that dropped only one operand would be
  killed by one of the two, not both).
- MARK present.

### 3.7 `s_modes-s09-url-map-nested-shape` — **honest**
- Comment: "an unreadable --url-map whose shape is a nested object. The map problem is refused (2) before the quote
  is judged; unguarded, the empty map leaves the located quote unmapped and the run exits 9."
- Reference rc 2, stdout `QUOTE problem=--url-map must map strings to strings` (the S09 site's own print,
  `sources_adopt.py:1027-1029`), stderr empty. Mutant rc 9, stdout
  `… located=0 found=1 … unmapped=1 … REFUSED S908 unmapped words=9 at b-capture.txt`. "Silently downgrades a
  caller fault to a citation gap" is measured literally. MARK present on this fixture.

### 3.8 `s_modes-s09-url-map-directory` — **honest**
- Comment: "an unreadable --url-map naming a directory is unreadable at the filesystem level (OSError, not JSON
  shape), refused as 2; unguarded it becomes an empty map, so the located quote is unmapped (9)."
- Reference rc 2, stdout `QUOTE problem=--url-map is unreadable: [Errno 21] Is a directory: '…/corpus/evidence/r41-url-maps'`
  — the OSError branch, distinct from 3.7's shape branch. Mutant rc 9, `unmapped=1`, `REFUSED S909 unmapped`.
- MARK present. Independent trigger by construction (OSError vs JSON shape), not a near-duplicate.

## 4. Cross-kill / discrimination (my own matrix, not the author's)

Every mutant against every fixture (mutant rc; reference is 2 throughout):

```
fixture                                        ref S01 S04 S08 S09
s01-quote-plus-package                          2   0   2   2   2
s01-quote-plus-registry-and-package             2   0   2   2   2
s04-url-map-with-adopt                          2   2   0   2   2
s04-url-map-with-check-only                     2   2   0   2   2
s08-quote-file-without-artifact                 2   2   2   1   2
s08-artifact-without-quote-file                 2   2   2   1   2
s09-url-map-nested-shape                        2   2   2   2   9
s09-url-map-directory                           2   2   2   2   9
```

No mutant is killed by another guard's fixture, so the `killed by=` attribution is not an artefact of ordering.

## 5. Wave-1 counterexample vectors — all absent

| Vector (wave 1) | Status here | Evidence |
|---|---|---|
| probe stub reads bound variant from its sandbox and steers verdict (A1′, F1) | **not applicable** — no probe stub exists; fixtures are data files and the tool is the real pinned tool | `grep -nE 'import \|witness\|\.ufo\|/plans/\|open\(\|read_text\|subprocess\|os\.\|sys\.' bat/s_modes.py` → only line 8, a docstring sentence ("Nothing here reads another module, a witness or the lane"); no `import`, `open(`, `read_text` or `subprocess` anywhere |
| counter scratch root / `variants/` / slot file read | **absent** | no code path in the module executes at run time; builders only call `ctx.write` |
| `/proc`, pid, cmdline | **absent** | SIDECHANNEL token scan over the module: `[]` (counter also printed `sidechannel=0`) |
| relative `../` argv escape (F4/A3) | **absent** — one relative token, no `..`, resolved from `cwd = fixture dir`, used only as text in the `used-by` cell | matrix §3.3 |
| AF_UNIX sockets / SysV IPC (F2/F3) | **not used** | zero imports, no subprocess |
| reading tool or counter program text (A8) | **absent** | module never opens a file for reading |
| witness-module dependence | **independent** | witness ids are `w-sNN-…` (`w_sources.py`), this module's are `s_modes-…`; no witness path string in the file; counter run with a battery dir holding only `s_modes.py` still kills 4/4 |

Fixture trees were fingerprinted by the counter before/after (`tampered=0`), second unmodified runs identical
(`null_detected=0`), and both pins unchanged after (`PINS-AFTER mismatched=0`) — the tool writes nothing into the
fixture, which is what makes the data-only design safe.

## 6. Limits worth carrying into the admission decision

1. **Exit-code-only discrimination.** For `sources` the counter's class set is always empty, so `expect=error`
   pins only "rc 2", not *which* refusal. A fixture with a wrong-but-still-rc-2 path would pass. Here I verified the
   actual messages for all 8 fixtures (§3): they are the four advertised guards and nothing else. Admission of this
   module therefore rests on this message reading, not on the counter.
2. **S08's mutant rc 1 is a traceback** (§3.5/3.6). The kill is causal and the line executes, but the future
   direction `2>1` would also be satisfied by an unrelated crash on the same argv. A fixture that pinned the
   historical graceful refusal (or captured the exception) would be stronger; not a reason to reject.
3. **Two triggers per guard** means a lone fixture deletion still leaves `killed=4/4`. The author's section C (both
   removed) is the load-bearing measurement and I did not rely on it for this verdict; the per-fixture attribution
   in §2/§4 does not need it.

## 7. Reproduction

```
S=/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcModes
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"   # toplevel == "$S/lane"
mkdir -p "$S/bat"; cp <lane>/plans/battery41/s_modes.py "$S/bat/"
# §1  (counter-only.txt)   run-counter.sh: envelope + round41_c1_verify.py --lane "$S/lane" --battery-dir "$S/bat" \
#                           --only S01,S04,S08,S09 --work "$S/w"
# §2/§3 (probe-out.json)  envelope + probe.py   (build 8 fixtures, ref / mutant / MARK copies
#                           in the counter's ro sandbox; MARK inserted immediately before the mutated line)
# §3     (probe2.txt)      envelope + probe2.py (reference refusal message, mutant exception type)
```

Scratch dir removed after this report was written (`/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcModes`, only my own).
No file outside this report dir was written.

VERDICT: battery41-s_modes-honest-8/8-mutated-line-executed-4/4
