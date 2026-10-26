# Draft — PROVINCE.md adjacency note (round 38, for L1 paste)

Closes routed D6 (`corpus/lessons/round-37-verifier-spotcheck.md` §5 item 6;
`.ufo/waves/round-37/falsify/F37ConnSiblingCite.md`). Report-out only: nothing below is
absorbed, and no sibling file is edited from here. Insert after the existing `### Adjacent`
table (`PROVINCE.md:129-140`) as a new `####` sub-block, or as a new `##` paragraph after
`Round37 partial frontier admission` (`PROVINCE.md:264-285`); both read correctly.

---

#### Sandboxed-probe prior art (round 38, report-out; D6)

Sandboxed execution of a graded or mutated child is fleet prior art, not kengaku ground. The
instruments, with pointers:

| Lane | Instrument | Pointer |
|---|---|---|
| **tameshi** | defect-probes — pristine selftest vs guard-removal mutant, children under a read-only bwrap envelope | `.ufo/evidence/round-18/defect-probes.py:4-5,192` (envelope); registry row `SKILL.md:1929` |
| **tameshi** | `env-diff.py` — nine-pin env differential, command run under bwrap, `EXEC_UNAVAILABLE` when bwrap is missing | `tools/env-diff.py:57-70`; registry `SKILL.md:1975` |
| **tameshi** | `mutate-and-run.sh` — fleet exit-graded mutation runner; **`env -i` isolation, not bwrap** | `tools/mutate-and-run.sh:1418,1423,1428` |
| **kumitate** | `cap-run.mjs` — the fleet's bounded runner: `systemd-run` scope + `env -i` + `bwrap --ro-bind / / --unshare-pid --die-with-parent --new-session --clearenv`, tmpfs `/tmp`/`/run`, cwd bound rw, caller `--bind` refuses `/`,`/tmp`,`/proc`,`/sys`,`/dev`,`/run` | `scripts/cap-run.mjs:30-38,189-196`; registry `SKILL.md:618` |
| **kumitate** | `cap-spawn.mjs` — `spawnSync`-shaped wrapper that builds the `cap-run` argv | `scripts/cap-spawn.mjs:2-3,26`; `SKILL.md:623` |
| **kumitate** | `bind-oracle.mjs` — proves requested binds from *inside* a `cap-run` child; selftest builds runner mutants from `cap-run.mjs` source | `scripts/bind-oracle.mjs:5,150-160`; `SKILL.md:622` |
| **kumitate** | `gate-mutants.mjs` — 43-mutant gate battery; per-mutant `prlimit` process group, **no bwrap** | `SKILL.md:616` |
| **mado** | `c1-r40-live-v2.py` — C1 counter; every tool and selftest run under `bwrap --unshare-all --cap-drop ALL`, fresh `/proc`//`dev`, tmpfs `/tmp`, `/usr` ro; no bwrap → `SETUP` exit 2, never a silent downgrade | `quality/counters/c1-r40-live-v2.py:19-23,479-484` |
| **mado** | `c1-r41-globals.py` — same sandbox arm, fresh `/proc`//`dev`, tmpfs `/tmp` | `quality/counters/c1-r41-globals.py:8-10,195-200` |
| **kake** | `sealed_count_v2.py` — sealed-key counter; the tool runs in bwrap with its own PID namespace, `/usr` ro, tmpfs `/tmp`, no `/home`, no network; refuses when bwrap is absent | `.ufo/waves/round-36/sealed_count_v2.py:158-163,192-193` |
| **kake** | `c42_count.py` — 31k-value differential under `/usr/bin/bwrap --unshare-all --die-with-parent --clearenv`, RLIMIT_FSIZE 256 MiB, 4 GiB AS, 600 s | `.ufo/waves/round-42/c42_count.py:35-40,63` |
| **kake** | `c57_idresolver_gate.py` — C2 counter; the tool under test runs under `bwrap --unshare-net --unshare-pid --die-with-parent --ro-bind / /` with only its scratch tree bound rw | `.ufo/waves/round-57/c57_idresolver_gate.py:120-121` |
| **mori** | `count-c2-a1.py` — C2 counter; `timeout 120 bwrap --ro-bind / / --tmpfs /home --tmpfs /fast`, `env -i`, twice | `.ufo/waves/round-31/count-c2-a1.py:75-77` |
| **kotodama** | isolation-replay protocol — Tier A bwrap mount-namespace replay of a filed runner in a disposable clone; Tier B no-bwrap fallback; invariants I1–I7 (never run a filed runner in the live tree, TMPDIR inside the sandbox) | `reports/round-39/calib/isolation-replay-protocol.md:33-45` |
| **kaidoku** | `carrier-guard.py` — executes *copies* of a binary to observe mode/content changes; records that bwrap exists but **is not used** (loader-mapped, copy+exec, memfd, same-owner chmod named as bypasses) | `SKILL.md:606` |
| **kaidoku** | native ELF ground — Ghidra/REA ELF analysis, `.node` shared objects, `nm -D`/`DT_NEEDED`-class linkage reading; **owner of binary-linkage interpretation** | `PROVINCE.md:4,48,57` |

**The split.**

- **kumitate** owns the *runner* — the bounded, env-cleared, PID-namespaced child and its
  verdict line. kengaku's per-case sandbox is a consumer pattern of the same class and cites it;
  kengaku does not re-specify caps, scopes or bind policy.
- **tameshi** owns the *method* — pristine-vs-mutant calibration, fail-closed arms, verdict-line
  discipline, and the rule that a sibling's gate is probed read-only and never edited
  (`tameshi-shokunin/PROVINCE.md:14-17`). kengaku's C1 attributed-kill battery is an application
  of that method to its own `plans/pkg_gate.py`, not a new method.
- **mado, kake, mori, kotodama** each hold a *sandboxed-counter implementation* on their own
  ground; they are cited as precedent for the pattern (tool-under-sandbox, no-silent-downgrade),
  never as authorities over kengaku's probe.
- **kaidoku** owns what a *binary actually links or loads* (ELF reading). kengaku's build-pmars
  finding stops at "the grader's `ldd` string scan answers a string question" — kengaku grades the
  grader's assertion, and any claim about real `DT_NEEDED`/`dlopen` linkage routes to kaidoku's
  ELF ground rather than being made here.
- **kengaku** keeps: which TB2 grader is captured, how it is called offline, what its verdict
  answers, and the C1/C2 counters over `plans/pkg_gate.py`. Verified that no sibling reads,
  scores or claims TB2 grader execution: `grep -rl 'terminal-bench\|terminal_bench' */` outside
  `kengaku-shokunin/` returns only `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md`
  and `kumitate-shokunin/corpus/lessons/round-63.md` — both coordinator-topology data citations
  already ruled as such in round 37.
- **Not prior art, do not cite as sandboxes:** `mado-shokunin/SKILL.md:610` (`.ufo/waves/round-20/isolate.sh`
  "is not a sandbox — the environment and the compositor/session sockets stay reachable") and
  `kotodama-shokunin/SKILL.md:254` ("Determinism is not isolation"). Both are the lanes' own
  disclaimers and belong in any kengaku text that reaches for them.
- **No sibling owns ldd-in-a-gate.** `grep -rn -E '\bldd\b' */ --include=*.py --include=*.mjs
  --include=*.sh`, excluding `.ufo/waves/` and `corpus/`, returns nothing outside kengaku; mado's
  `ldd` hits are one-off host observations in evidence (`mado-shokunin/corpus/lessons/round-15.md:39`),
  not an acceptance check.

**Nothing absorbed.** No sibling instrument is copied into `plans/`; the lane's harness stays
scoped to `plans/pkg_gate.py` and the round's probe.
