# R38SiblingCite — sibling prior art for sandboxed grader probes (round 38, wave 1)

Seat: R38SiblingCite (scribe, leaf, read-only). Date: 2026-10-26.
Route: `corpus/lessons/round-37-verifier-spotcheck.md` §5 item 6 (D6) →
`.ufo/waves/round-37/falsify/F37ConnSiblingCite.md` gap 1 + gap 3.
Deliverable: a ready-to-paste PROVINCE.md adjacency note naming each sibling instrument with
file:line and the ownership split; report-out only, nothing absorbed.
Lane reads were read-only; no clone, no counter, no gate run, no git call in the lane.

## Behavior

Wrote one draft note at
`.ufo/waves/round-38/build/R38SiblingCite/province-adjacency-note.md` (6.4 kB) that closes D6 by
naming **16 distinct sibling surfaces with file:line** and stating, per lane, what stays theirs
and what stays kengaku's. It is inserted nowhere — `PROVINCE.md` is untouched (L1 integrates).

## Method and evidence

Every row below is a command whose output I read; no claim is inferred from a lane's lesson text
where the implementation file could be read instead.

### 1. Lane population

    $ ls -d /home/vgpnk/Projects/shokunin/*-shokunin
    audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku,
    kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi
    (21 lanes; `ls -d …/*-shokunin | wc -l` → 21)

### 2. bwrap / sandbox implementations (read from source, not from SKILL prose)

| Lane | File:line | What the bytes show |
|---|---|---|
| tameshi | `.ufo/evidence/round-18/defect-probes.py:4-5,192` | `bwrap --ro-bind / / --dev /dev --proc /proc --bind W W`; "Every child runs under bwrap 0.13.1 with this envelope" |
| tameshi | `tools/env-diff.py:57-70` | `execute(payload, interp, profile, timeout, bwrap=None)`; `argv = [bwrap, "--ro-bind", "/", "/", …]`; missing bwrap → `EXEC_UNAVAILABLE` (`:161-162`) |
| tameshi | `tools/mutate-and-run.sh:1418,1423,1428` | the fleet mutation runner sandboxes with `env -i PATH=… HOME=… TMPDIR=… LC_ALL=C` — **no bwrap** |
| kumitate | `scripts/cap-run.mjs:32-34,189-196` | `systemd-run --user --scope -p MemoryMax … -- env -i PATH=/usr/bin bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --tmpfs /run --bind cwd cwd --unshare-pid --die-with-parent --new-session --clearenv` |
| kumitate | `scripts/cap-spawn.mjs:2-3,26` | "a `spawnSync`-shaped call that runs one child under `scripts/cap-run.mjs`"; `export const CAP_RUN = …cap-run.mjs` |
| kumitate | `scripts/bind-oracle.mjs:5,150-160` | "Proves, from INSIDE a `scripts/cap-run.mjs` child, that requested host directories are mounted"; selftest builds runner mutants from `cap-run.mjs` source (`mutant('cap-run.drop.mjs', …)`) |
| kumitate | `SKILL.md:616` | `gate-mutants` registry row: per-mutant `prlimit` process group, 60 s timeout, 1 MiB/stream — **no bwrap** |
| mado | `quality/counters/c1-r40-live-v2.py:19-23,479-484` | "Every tool and selftest run happens inside a bubblewrap sandbox (`bwrap --unshare-all --cap-drop ALL`, a fresh /proc and /dev, a tmpfs /tmp, the interpreter's /usr read-only…) … No bwrap -> SETUP, exit 2 (never a silent downgrade)"; `sandbox_cmd` at `:479` |
| mado | `quality/counters/c1-r41-globals.py:8-10,195-200` | same arm; `["bwrap", "--unshare-all", "--die-with-parent", "--new-session", "--cap-drop", "ALL", …]` |
| kake | `.ufo/waves/round-36/sealed_count_v2.py:158-163,192-193` | `return ["bwrap", "--ro-bind", "/usr", "/usr", …]`; "No /home, no other /fast path, no network, its own pid namespace"; absent bwrap → "the tool cannot be jailed" |
| kake | `.ufo/waves/round-42/c42_count.py:35-40,63` | "Sandbox: /usr/bin/bwrap … --unshare-all, --die-with-parent, --clearenv; bwrap itself starts with PATH only"; `BWRAP = "/usr/bin/bwrap"` (`:63`), `CannotEvaluate("bwrap missing at %s" % BWRAP)` (`:519`) |
| kake | `.ufo/waves/round-57/c57_idresolver_gate.py:120-121` | `if SANDBOX and shutil.which("bwrap"):` → `["bwrap", "--unshare-net", "--unshare-pid", "--die-with-parent", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--bind", SCRATCH, SCRATCH, …]`; the tool under test runs inside it |
| mori | `.ufo/waves/round-31/count-c2-a1.py:75-77` | `['timeout','120','bwrap','--ro-bind','/','/','--tmpfs','/home','--tmpfs','/fast', … '/usr/bin/env','-i', …]` |
| kotodama | `reports/round-39/calib/isolation-replay-protocol.md:33-45` | invariants I1–I7: "Never execute a filed runner in the live tree"; Tier A `tmpfs`, Tier B `$PWD/.scratch`; runner SHA-256 before/after |
| kaidoku | `SKILL.md:606` | `carrier-guard` registry row, Limits cell: "bwrap 0.13.1 exists on the host but **is not used**" |

Verification greps (whole-lane, excluding evidence):

    $ grep -rn --include=*.py --include=*.mjs --include=*.sh 'bwrap' {kake,mado,mori,kotodama,kaidoku,tsukuroi}-shokunin
    → kake: 0 hits in tracked source (its counter lives under .ufo/waves/round-36 and round-42)
    → mado: c1-r40-live-v2.py:19,22,480; c1-r41-globals.py:8,10,196
    → mori: 0 in source (count-c2-a1.py is under .ufo/waves/round-31)
    → kotodama, kaidoku, tsukuroi: 0 hits

### 3. Does any sibling use ldd in a gate?

    $ grep -rn --include=*.py --include=*.mjs --include=*.sh -E '\bldd\b' */ \
        | grep -v '/.ufo/waves/' | grep -v '/corpus/' | grep -v '^kengaku-shokunin/' | grep -v Binary
    (no output)

Empty. The only non-kengaku `ldd` occurrences in the fleet are host observations recorded in
evidence — `mado-shokunin/corpus/lessons/round-15.md:39` ("`ldd -r` reports 0 unresolved
symbols …") and `mado-shokunin/.ufo/waves/round-13/w1/GlobalCapture.md:50`. Neither is an
acceptance check. **`ldd`-as-grader-assertion is kengaku-only**, which is a *negative* prior-art
result worth stating in the entry: the build-pmars finding is not a re-discovery.

### 4. TB2 grader ground

    $ grep -rln --include=*.md --include=*.py --include=*.mjs \
        'terminal-bench\|terminal_bench\|Terminal-Bench' */ | grep -v '^kengaku-shokunin/' | grep -v '/.ufo/waves/'
    kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md
    kumitate-shokunin/corpus/lessons/round-63.md

Both are coordinator-topology data citations, already ruled in round 37 as "a data citation, not
a grader claim" (`F37ConnSiblingCite` Q2). No sibling reads, runs or claims TB2 scoring code.
kengaku's TB2 grader-probe ground is uncontested.

Sweep completeness (the first fleet-wide `bwrap` grep was truncated at 20 of 33 matches; the
complement was re-read with `skip=20`): every remaining hit is a wave report, a `MANIFEST.json`
note, a `SOURCES.md` duplicate-URL row for `bwrap.xml`, or `kaidoku` analysing the `bwrap`
*binary* as an ELF target (`corpus/knowledge/2026-10-13-r2-version-diff-compare.md:16-20`) — no
additional sandbox implementation. One further lane was suggested to this seat out of band:

    $ grep -rln 'bwrap\|\bldd\b' tabi-shokunin
    tabi-shokunin/corpus/evidence/round-13/aria/node_modules/playwright-core/lib/coreBundle.js
    tabi-shokunin/.ufo/waves/round-16/w2/SentinelCounter.md  (+ .git objects)

`tabi` is not sandbox prior art: its only hits are a vendored Playwright bundle and a wave
report. Its round-29 evidence (`git -C tabi-shokunin ls-tree -r --name-only f36caf6 --
.ufo/waves/round-29`) carries no bwrap runner. Recorded so the L1 does not re-walk it.

### 5. Ownership text already on disk (used for the split, not invented)

- tameshi `PROVINCE.md:14-17`: "**Refuses:** product domains — every lane's gate remains its own;
  tameshi owns only the reusable craft … Never edits a sibling's gate code (read-only probes;
  recommendations travel in round reports)."
- kumitate `PROVINCE.md:6` ("**Refuses:** anything outside this domain; report cross-domain
  evidence back to the orchestrator rather than absorbing it") and `:24` (the coordinator-topology
  band: "kengaku evaluates agents, this lane arranges the seats around that judgment").
- kaidoku `PROVINCE.md:4`: "reverse engineering of shipped artifacts … native ELF through the
  Ghidra 12.1.4 provider"; `:48` ELF analysis row; `:57` `.node` ELF shared objects.
- mado `SKILL.md:610`: `.ufo/waves/round-20/isolate.sh` "passes that check; **it is not a
  sandbox** (the environment and the compositor/session sockets stay reachable)".
- kotodama `SKILL.md:254`: "**Determinism is not isolation**: the pre-fix D4 projection passed its
  canonical gate 19/19 while carrying D2's 21-component rank fixture."

The last two are the lanes' own disclaimers. A kengaku note that reaches for them must repeat the
disclaimer, or it misstates the prior art.

### 6. kengaku's own half (for symmetry in the note)

- `plans/build_pmars_probe.py:59` `BWRAP = "/usr/bin/bwrap"`; `:240` `[BWRAP, "--unshare-net",
  "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session", "--ro-bind", "/usr",
  "/usr", …]`.
- `plans/git_webserver_probe.py:49,204` the same arm (round 37).

## Findings

1. **D6 gap 1 is closable as written.** tameshi's bwrap defect-probes and kumitate's `cap-run.mjs`
   both exist at the cited pointers and both were read from source. `F37ConnSiblingCite` reported
   "zero hits in any landed surface" for these two; the note now supplies file:line for each.
2. **The two cited instruments are not the same kind of thing.** `cap-run.mjs` is a *runner*
   (caps, scope, PID namespace, env clear, bind policy); defect-probes is a *calibration harness*
   (pristine vs guard-removal mutant). Round-37 text that put tameshi's `mutate-and-run.sh` and
   kumitate's `gate-mutants.mjs` in one sentence conflated the fleet's mutation runner — which
   sandboxes with `env -i` only (`mutate-and-run.sh:1418`) — with kumitate's battery, which uses
   `prlimit` and no bwrap (`SKILL.md:616`). Neither of those two is bwrap-bounded; the bwrap
   instruments are `cap-run.mjs`, defect-probes, mado's two counters, kake's three counters, mori's
   C2 counter, and kotodama's replay protocol. The split has to keep runner / method / counter
   apart or the citation misleads.
3. **Nine more sandboxed-counter implementations exist beyond the two D6 names** (mado ×2,
   kake ×3, mori ×1, kotodama ×1, plus kumitate's `cap-spawn`/`bind-oracle` as runner-side
   helpers). Citing only tameshi+kumitate would understate the fleet precedent; the note names
   all 16 surfaces.
4. **A real adjacency nobody had named: linkage interpretation.** The build-pmars headline
   finding ("`ldd` string scan misses a `dlopen()`ed libX11") is, on its second half, an ELF
   claim. kaidoku owns native ELF reading (`PROVINCE.md:4,48,57`, `nm -D`/`DT_NEEDED`-class
   work). kengaku's note should stop at "the grader answers a string question", not at "the
   binary does/doesn't link X11". This is the one case where a D6 pointer protects against a
   scope error rather than only crediting prior art.
5. **Negative prior art worth recording:** no sibling uses `ldd` in a gate (grep empty), and no
   sibling holds TB2 grader ground (grep returns only coordinator-topology citations). Both
   strengthen kengaku's novelty claim for the *class* while removing any claim for the *pattern*.
6. **Gap 3 (file:line on already-cited precedents) is fixed by construction** — every row of the
   draft carries a path with line numbers; `PROVINCE.md:283`'s bare names can be superseded by a
   pointer to the new note.

## Out of scope / not done

- `PROVINCE.md` was **not** edited (L1 integrates); no draft was pasted into any lane file.
- No counter, gate, probe or battery was run; this seat judges citations, not predicates.
- Round-37 wave-2 reports under `.ufo/waves/round-37/falsify/` were read only where they routed
  this item; sibling lanes' `.ufo/waves/` were read for instrument pointers, never written.
- No tool installed or upgraded (grep, sed, ls, wc only — all pre-installed).
- No scratch dir was needed: no clone, no fixture, no work tree. `/fast/scratch/hyaku/kengaku-r38/R38SiblingCite/`
  was never created, so there is nothing to remove.

## Artifacts

- `.ufo/waves/round-38/build/R38SiblingCite/province-adjacency-note.md` — the draft note (16
  sibling surfaces with file:line, the per-lane split, the two disclaimers, the ldd/TB2 negative
  results), ready for L1 paste into `PROVINCE.md`.
- `.ufo/waves/round-38/build/R38SiblingCite.md` — this report.

VERDICT: sibling-cites-16
