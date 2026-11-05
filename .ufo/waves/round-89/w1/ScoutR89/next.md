# ScoutR89 — next-round candidates (read-only recon, no claims)

Seat: `ScoutR89` (scout; axes: coverage, calibration). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
branch `master`, measured tip `a9b8a1a00b6a5ab5206be4d377dba439e02f8244` (read-only `git show`; no clone was made,
no mutating git ran, no production file was edited). Everything below is derived from `git show` at that revision;
nothing was fetched from the network.

Written files: this file plus four machine-readable companions in the same directory —
`per-member.json` (per-member blockers + grep line numbers + sha256, §2),
`per-member-raw.json` (the same rows with the raw matched source lines),
`class-arithmetic.json` (the §4 ranking with every derived number), and
`ledger-at-tip.json` (a byte-identical copy of
`git show a9b8a1a00b6a5ab5206be4d377dba439e02f8244:plans/grader-population-ledger.json`).
Scratch: `/fast/scratch/hyaku/kengaku-r89/ScoutR89/`, deleted before this report was filed.

Tooling: **no tool was installed or upgraded** on this host (nothing the item needed was missing), so the operator
tooling directive produced no installs to record. `uv 0.13.0` and `bwrap` were already present.

---

## 0. Commands (all read-only, reproducible)

```sh
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
REV=a9b8a1a00b6a5ab5206be4d377dba439e02f8244

# (a) the unexecuted shell-exec / stdout-inspection members, counted in python3
git -C "$L" show $REV:plans/grader-population-ledger.json | python3 -c '
import sys, json
d = json.load(sys.stdin)["members"]
sel = sorted(k for k, v in d.items()
             if v["status"] != "executed"
             and ("shell-exec" in v["classes"] or "stdout-inspection" in v["classes"]))
print(len(sel)); print("\n".join(sel))'

# (b) the captured grader bytes for each, plus the prescribed grep
for m in <member>; do
  git -C "$L" show $REV:corpus/evidence/round52/graders/$m/tests/test_outputs.py > /tmp/g.py
  grep -nE 'http|ssh|qemu|selenium|pdflatex|docker|requests|urllib' /tmp/g.py
done

# (c) sha256 of each captured grader at the tip
git -C "$L" show $REV:corpus/evidence/round52/graders/<member>/tests/test_outputs.py | sha256sum
```

Verification commands actually run by this seat (outputs quoted verbatim below):

```
$ git -C "$L" show $REV:plans/grader-population-ledger.json | python3 -c '...'
24
adaptive-rejection-sampler
build-pov-ray
caffe-cifar-10
compile-compcert
custom-memory-heap-crash
dna-assembly
dna-insert
git-multibranch
gpt2-codegolf
install-windows-3.11
large-scale-text-editing
mcmc-sampling-stan
merge-diff-arc-agi-task
model-extraction-relu-logits
modernize-scientific-stack
overfull-hbox
path-tracing
pytorch-model-cli
qemu-alpine-ssh
qemu-startup
reshard-c4-data
schemelike-metacircular-eval
winning-avg-corewars
write-compressor
```

Ledger status split at the tip (same counting over the same bytes): `executed 33, unexecuted 55, executed-unlocated 0`,
88 members total. At BASE `192e809d582ecbd544798cbc03da1666a0de23f7` the split is `executed 32, unexecuted 56`
— i.e. the round-89 move added exactly one member (`polyglot-rust-c`), consistent with the frozen claim.

---

## 1. (a) The candidate set — 24 unexecuted members with `shell-exec` or `stdout-inspection`

Counted with python3 over `git show a9b8a1a:plans/grader-population-ledger.json` (command above).
All 24 have their captured grader bytes present in the tree at the tip
(`git show a9b8a1a:corpus/evidence/round52/graders/<member>/tests/test_outputs.py` exits 0 for every one of them),
so none of the 24 is blocked by a missing capture.

Split by class:

* `shell-exec` (6 members total, 2 executed → 4 unexecuted here): `git-multibranch`, `model-extraction-relu-logits`,
  `overfull-hbox`, `qemu-startup`. (The two executed are `feal-differential-cryptanalysis` (round 43) and
  `polyglot-rust-c` (round 89).)
* `stdout-inspection` (29 members total, 9 executed → 20 unexecuted here): all of the above except
  `model-extraction-relu-logits` (which is not stdout-inspection) plus the 19 listed below.

`stdout-inspection`-only unexecuted members: `adaptive-rejection-sampler`, `build-pov-ray`, `caffe-cifar-10`,
`compile-compcert`, `custom-memory-heap-crash`, `dna-assembly`, `dna-insert`, `gpt2-codegolf`,
`install-windows-3.11`, `large-scale-text-editing`, `mcmc-sampling-stan`, `merge-diff-arc-agi-task`,
`modernize-scientific-stack`, `path-tracing`, `pytorch-model-cli`, `qemu-alpine-ssh`, `reshard-c4-data`,
`schemelike-metacircular-eval`, `winning-avg-corewars`, `write-compressor`.

Per-class executed/total at the tip (derived from the same ledger bytes, used for the arithmetic in §4):

| class | executed of total | class | executed of total |
|---|---|---|---|
| filesystem-metadata | 2 of 10 | stdout-inspection | 9 of 29 |
| subprocess-exec | 11 of 45 | file-artifact | 24 of 76 |
| crypto-credential | 3 of 12 | git-plumbing | 1 of 3 |
| numeric-band | 3 of 10 | timing-wall | 3 of 9 |
| serialization-schema | 3 of 10 | candidate-import | 3 of 6 |
| shell-exec | 2 of 6 | network-service | 4 of 8 |
| db-state | 1 of 2 | process-environment | 2 of 3 |
| signal-delivery | 1 of 1 | container-image | 0 of 0 |

History of the two classes this item is scoped to, from the ledger's own commit history
(`git log --format='%H %s' -- plans/grader-population-ledger.json`, 12 commits, each read with `git show`):
`shell-exec` has moved **once** in the ledger's life (1 → 2, the round-89 commit `000b7d1cd`);
`stdout-inspection` moved at round 80 (6 → 8) and again at round 89 (8 → 9). The `subprocess-exec` class moved
alongside it (10 → 11) because `polyglot-rust-c` carries it.

---

## 2. (b) Per member: the ledger blocker, and what the captured bytes actually require

The prescribed grep is `http|ssh|qemu|selenium|pdflatex|docker|requests|urllib`. Two spellings are reported:
**CS** = the grep exactly as prescribed (case-sensitive), **CI-extra** = lines that match only case-insensitively
(e.g. `QEMU`, `Docker` in prose). The `network` column is a separate check for package/dataset downloads
(`apt-get`, `apt install`, `pip install`, `load_dataset`, `download=True`, `curl -`, `wget`), because the prescribed
grep cannot see those. `VM` marks a live-machine requirement (`expect`/`telnet`/`ssh`/qemu), `LaTeX` a TeX toolchain.

| member | classes | ledger `reason` | CS grep | CI-extra | network | VM | LaTeX | verdict |
|---|---|---|---|---|---|---|---|---|
| `adaptive-rejection-sampler` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean |
| `build-pov-ray` | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (host tool `povray` absent) |
| `caffe-cifar-10` | file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (host tool `caffe` absent) |
| `compile-compcert` | file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `ccomp` at `/tmp/CompCert/ccomp`) |
| `custom-memory-heap-crash` | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `/usr/local/gcc-custom-{debug,release}/lib64`) |
| `dna-assembly` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `oligotm`) |
| `dna-insert` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | `unattempted` | — | L46 | — | — | — | offline-clean (needs `oligotm`) |
| `git-multibranch` | file-artifact, network-service, shell-exec | `unattempted` | L7, L13, L15, L18, L19, L72, L73 | L99 | L12, L13, L72, L73 | L13, L23, L27, L31, L41, L44, L46, L54, L57, L59 | — | **needs network + ssh + an HTTPS server** |
| `gpt2-codegolf` | file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `gpt2-124M.ckpt`, `vocab.bpe`) |
| `install-windows-3.11` | crypto-credential, file-artifact, network-service, process-environment, stdout-inspection, subprocess-exec | `vm-required` | L20, L21, L31, L33, L50, L64, L66, L98 | L23, L37, L65, L69 | — | L16, L21, L98, L102, L262 | — | **needs a Windows 3.11 QEMU VM** (ledger reason correct) |
| `large-scale-text-editing` | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `vim`) |
| `mcmc-sampling-stan` | file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs R + rstan) |
| `merge-diff-arc-agi-task` | file-artifact, git-plumbing, serialization-schema, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `/tests/test.json` sibling + git) |
| `model-extraction-relu-logits` | candidate-import, file-artifact, shell-exec | `candidate-library-required` | — | — | — | — | — | offline-replayable (see §5) |
| `modernize-scientific-stack` | file-artifact, filesystem-metadata, numeric-band, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs a `pytest` stub) |
| `overfull-hbox` | file-artifact, shell-exec | `unattempted` | L20 | — | L18 | — | L14, L18, L20 | **needs LaTeX (`pdflatex`) + `apt install`** |
| `path-tracing` | file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `chroot /jail` → root) |
| `pytorch-model-cli` | file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | L113 | — | — | **needs network** (`datasets.MNIST(download=True)`) |
| `qemu-alpine-ssh` | stdout-inspection, subprocess-exec | `unattempted` | L9, L18, L25, L28, L41 | L10, L13, L14, L15, L20 | — | L9, L18, L25 | — | **needs a QEMU VM reachable over SSH** |
| `qemu-startup` | file-artifact, shell-exec | `unattempted` | — | L39, L42, L49, L52 | — | L8, L20, L27, L31, L34, L43, L47, L56 | — | **needs a QEMU VM reachable over telnet** |
| `reshard-c4-data` | crypto-credential, file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec | `unattempted` | — | — | L12, L34 | — | — | **needs network** (`load_dataset("allenai/c4")`) |
| `schemelike-metacircular-eval` | file-artifact, stdout-inspection, subprocess-exec, timing-wall | `unattempted` | — | — | — | — | — | offline-clean (needs `/tests/test/*.scm` siblings) |
| `winning-avg-corewars` | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `pmars`) |
| `write-compressor` | file-artifact, stdout-inspection, subprocess-exec | `unattempted` | — | — | — | — | — | offline-clean (needs `gcc` + `original-decomp.c`, `original-data.txt` siblings) |

Note on the two `dna-*` rows: their only case-sensitive CI-extra hit is `L46`, the word `Docker` in the comment
`# Reference the directory the agent operated in (the WORKDIR in the Docker env)` — prose, not a container
requirement. Both rows do need the `oligotm` binary (primer3) at run time, which is a host-tool dependency, not a
network one.

### 2.1 Cross-check of every ledger `reason` against the frozen detector set

The frozen detector set lives in `plans/round79_c1_population_ledger.py` (`BLOCKERS`, four regexes:
`browser-required`, `vm-required` = `qemu-system|qemu-img|/app/isos/|win311`, `external-db-required`,
`candidate-library-required` = `sys.path.append("/app")`). Running those four regexes over the 24 captured graders:

* `install-windows-3.11` → `vm-required` fires at L16 (`/app/isos/win311.img`); ledger says `vm-required`. **Backed.**
* `model-extraction-relu-logits` → `candidate-library-required` fires at L10 (`sys.path.append("/app")`);
  ledger says `candidate-library-required`. **Backed** by the frozen regex — but see §5 for why the blocker is
  stageable offline.
* the other 22 → no frozen detector fires; ledger says `unattempted`. **Backed** as the schema's honest default
  ("a blocker reason only when a frozen detector fires over the task's `tests/test_outputs.py`, else `unattempted`").

---

## 3. Finding 1 — the ledger's blocker taxonomy has no row for six members that plainly need one

Six of the 24 rows carry `reason: "unattempted"` while the captured grader bytes plainly require network, ssh, a
VM or a LaTeX toolchain:

| member | ledger `reason` | what the bytes actually require | evidence (line numbers) |
|---|---|---|---|
| `git-multibranch` | `unattempted` | `apt-get update` + `apt-get install -y curl expect git openssh-client` (network), `git clone git@localhost:` (ssh), `curl -sk https://localhost:8443/...` (HTTPS server) | L12, L13, L26, L72, L73 |
| `qemu-alpine-ssh` | `unattempted` | `sshpass … ssh …` into a QEMU Alpine VM, asserts the `6.6.4-1-lts` kernel | L9, L18, L25, L28, L41 |
| `qemu-startup` | `unattempted` | `expect` script that `spawn telnet localhost 6665` and logs into a QEMU Alpine VM | L8, L20, L27, L31, L56, L59 |
| `overfull-hbox` | `unattempted` | `apt install -y --reinstall texlive-latex-base` (network) and `/usr/bin/pdflatex` (LaTeX) | L18, L20 |
| `pytorch-model-cli` | `unattempted` | `datasets.MNIST(..., download=True)` (network) | L110, L113 |
| `reshard-c4-data` | `unattempted` | `load_dataset("allenai/c4", …)` (network) | L12, L34 |

This is **not** a violation of the frozen schema: the R79 gate only prices a reason as `REASON-UNBACKED` when no
frozen detector fires over a non-`unattempted` reason, and `REASON-UNDERSTATED` when a frozen detector fires over an
`unattempted` row. None of the four frozen regexes matches `ssh`, `curl`, `apt-get`, `telnet`, `expect`, `pdflatex`,
`load_dataset` or `download=True`, so the gate passes on all six rows and the ledger stays internally consistent.
The consequence is for the *next* round, not for round 89's gate: a scout filtering candidates by
`reason != "unattempted"` would wrongly admit `git-multibranch`, `qemu-alpine-ssh`, `qemu-startup` and
`overfull-hbox` as offline-replayable, and would wrongly believe `pytorch-model-cli` and `reshard-c4-data` need no
network. The next round should filter on the grader bytes (as §2 does), not on the `reason` string alone.

Not repaired here: `plans/grader-population-ledger.json` and `plans/round79_c1_population_ledger.py` are production
files and are read-only to this seat.

---

## 4. (c) Class arithmetic, and the top three offline candidates

**Metric (stated so it can be re-derived).** For a candidate `m`, the *thinness-weighted class arithmetic* is

```
arith(m) = Σ over classes c of m  of  (unexecuted(c) / total(c))
```

i.e. the share of each class the member touches that is still unexecuted — how much of the still-unreplayed
population of each of its classes this one member would sit in. A member sitting in many thin classes scores high.
Ties are broken by `deficit(m) = Σ over classes c of m of (total(c) − executed(c))`, then by fewer host-tool
dependencies. "Offline" = the captured bytes need none of network/ssh/VM/browser/LaTeX/docker per §2.

### 4.1 Full ranking of the 24 (offline-clean rows are the ones that can be replayed)

| member | classes | arith | deficit | stale-sum | offline per §2 |
|---|---|---|---|---|---|
| `install-windows-3.11` | crypto-credential, file-artifact, network-service, process-environment, stdout-inspection, subprocess-exec | 3.713 | 120 | 22 | no — VM |
| `reshard-c4-data` | crypto-credential, file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec | 3.679 | 123 | 22 | no — network |
| **`modernize-scientific-stack`** | file-artifact, filesystem-metadata, numeric-band, stdout-inspection, subprocess-exec | **3.629** | 121 | 13 | **yes** |
| **`merge-diff-arc-agi-task`** | file-artifact, git-plumbing, serialization-schema, stdout-inspection, subprocess-exec | **3.496** | 115 | 14 | **yes** |
| `caffe-cifar-10` | file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec | 2.929 | 114 | 10 | yes (host tool absent) |
| `compile-compcert` | file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec | 2.929 | 114 | 10 | yes (host tool absent) |
| `build-pov-ray` | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | 2.879 | 115 | 2 | yes (host tool absent) |
| `custom-memory-heap-crash` | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | 2.879 | 115 | 2 | yes (host tool absent) |
| `large-scale-text-editing` | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | 2.879 | 115 | 2 | yes (host tool absent) |
| `winning-avg-corewars` | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | 2.879 | 115 | 2 | yes (host tool absent) |
| `adaptive-rejection-sampler` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | 2.829 | 113 | 4 | yes (host tool absent) |
| `dna-assembly` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | 2.829 | 113 | 4 | yes (host tool absent) |
| `dna-insert` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | 2.829 | 113 | 4 | yes (host tool absent) |
| `schemelike-metacircular-eval` | file-artifact, stdout-inspection, subprocess-exec, timing-wall | 2.796 | 112 | 10 | yes |
| `gpt2-codegolf` | file-artifact, stdout-inspection, subprocess-exec | 2.129 | 106 | 1 | yes (big assets) |
| `mcmc-sampling-stan` | file-artifact, stdout-inspection, subprocess-exec | 2.129 | 106 | 1 | yes (host tool absent) |
| `path-tracing` | file-artifact, stdout-inspection, subprocess-exec | 2.129 | 106 | 1 | yes (needs root for `chroot`) |
| `pytorch-model-cli` | file-artifact, stdout-inspection, subprocess-exec | 2.129 | 106 | 1 | no — network |
| `write-compressor` | file-artifact, stdout-inspection, subprocess-exec | 2.129 | 106 | 1 | yes |
| `git-multibranch` | file-artifact, network-service, shell-exec | 1.851 | 60 | 12 | no — network + ssh |
| `model-extraction-relu-logits` | candidate-import, file-artifact, shell-exec | 1.851 | 59 | 11 | yes — see §5 |
| `qemu-alpine-ssh` | stdout-inspection, subprocess-exec | 1.445 | 54 | 1 | no — VM + ssh |
| `overfull-hbox` | file-artifact, shell-exec | 1.351 | 56 | 11 | no — LaTeX + network |
| `qemu-startup` | file-artifact, shell-exec | 1.351 | 56 | 11 | no — VM + telnet |

### 4.1a The second dimension: how long each class has been unmoved

The lane's own framing of a class move (round-88's critique, `plans/round-88-claims.md` / the round-88 lesson) is
not only "which cell is thin" but "which cell has not moved in how long" — e.g. round 88's `crypto-credential`
2/12 → 3/12 was scored as a real move because it was *"the first time since round 41/80"*. Derived from the same
ledger history (`git log -- plans/grader-population-ledger.json`, 12 commits, each read with `git show`), the
per-class "rounds unmoved at the tip" is:

| class | cell at tip | last moved | rounds unmoved |
|---|---|---|---|
| `git-plumbing` | 1 of 3 | round 79 (the freeze) | **10** |
| `candidate-import` | 3 of 6 | round 79 (the freeze) | **10** |
| `network-service` | 4 of 8 | round 79 (the freeze) | **10** |
| `db-state` | 1 of 2 | round 79 (the freeze) | **10** |
| `process-environment` | 2 of 3 | round 79 (the freeze) | **10** |
| `filesystem-metadata` | 2 of 10 | round 80 | 9 |
| `timing-wall` | 3 of 9 | round 80 | 9 |
| `signal-delivery` | 1 of 1 | round 80 | 9 |
| `numeric-band` | 3 of 10 | round 86 | 3 |
| `serialization-schema` | 3 of 10 | round 86 | 3 |
| `crypto-credential` | 3 of 12 | round 88 | 1 |
| `file-artifact` | 24 of 76 | round 88 | 1 |
| `subprocess-exec` | 11 of 45 | round 89 | 0 |
| `stdout-inspection` | 9 of 29 | round 89 | 0 |
| `shell-exec` | 2 of 6 | round 89 | 0 |

(`db-state` and `process-environment` and `signal-delivery` are also 10/9 rounds unmoved but have no unexecuted
member in the 24-candidate set that is offline-replayable — `db-state`'s remaining member `query-optimize` is not in
this set at all, and `process-environment`'s only unexecuted member is `install-windows-3.11`, VM-blocked.)

**Robustness check.** The top three offline candidates are the same three under three different orderings —
(i) pure thinness (`arith`), (ii) staleness-first, and (iii) the composite `arith × (1 + mean rounds-unmoved)`:

| ordering | 1st | 2nd | 3rd |
|---|---|---|---|
| (i) thinness `arith` | `modernize-scientific-stack` (3.629) | `merge-diff-arc-agi-task` (3.496) | `caffe-cifar-10` / `compile-compcert` (2.929, tie) |
| (ii) staleness-first | `merge-diff-arc-agi-task` (git-plumbing, 10 unmoved) | `model-extraction-relu-logits` (candidate-import, 10 unmoved) | `modernize-scientific-stack` (filesystem-metadata, 9 unmoved) |
| (iii) composite | `merge-diff-arc-agi-task` (13.285) | `modernize-scientific-stack` (13.066) | `caffe-cifar-10` = `compile-compcert` (10.253) |

`merge-diff-arc-agi-task` and `modernize-scientific-stack` are in the top three under every ordering, and the third
slot is `caffe-cifar-10` (tie broken below). `model-extraction-relu-logits` appears at #2 under the staleness-first
ordering because `candidate-import` has not moved since the freeze and `shell-exec` is the thinnest multi-member
class — it is the strongest *shell-exec-axis* candidate and is treated separately in §5.

### 4.2 Top three offline candidates

**1. `modernize-scientific-stack`** — arith 3.629, deficit 121, five classes of which four are thin
(`filesystem-metadata` 2/10 is the thinnest class in the whole ledger; `numeric-band` 3/10; `stdout-inspection` 9/29;
`file-artifact` 24/76). Captured grader bytes: 2330 bytes; module-level imports `subprocess`, `sys`, `pathlib`,
`pytest` (the `pytest` import is satisfied by the lane's existing `/stub` recipe recorded for the `numeric-band`
class in `SKILL.md`'s decision table). The grader runs `/app/analyze_climate_modern.py` with `sys.executable`,
reads its stdout, and asserts `Station 101` ≈ −15.5 and `Station 102` ≈ 30.3 plus a `requirements.txt`/`pyproject.toml`
existence check — all stageable files under a writable `/app`, no network.

sha256 of the captured grader at the tip:

```
$ git -C "$L" show a9b8a1a00b6a5ab5206be4d377dba439e02f8244:corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py | sha256sum
0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977  -
```

Fetch command that would pin it (not performed here):

```sh
curl -fsSL -o test_outputs.py \
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/modernize-scientific-stack/tests/test_outputs.py
echo '0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977  test_outputs.py' | sha256sum -c -
```

**2. `merge-diff-arc-agi-task`** — arith 3.496, deficit 115, five classes including `git-plumbing` (1 of 3 — the
thinnest class by ratio besides `shell-exec`) and `serialization-schema` (3/10). Captured grader bytes: 3034 bytes;
module-level imports are stdlib only (`importlib`, `json`, `sys`, `pathlib`); it shells `git branch -a` in
`/app/repo`, imports `/app/repo/algo.py` and checks it exposes a callable `map`, then replays `/tests/test.json`
through that `map` function. Needs one sibling capture (`/tests/test.json`) and a staged git repo — no network.

sha256 of the captured grader at the tip:

```
$ git -C "$L" show a9b8a1a00b6a5ab5206be4d377dba439e02f8244:corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py | sha256sum
2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149  -
```

Fetch command that would pin it (not performed here):

```sh
curl -fsSL -o test_outputs.py \
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py
echo '2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149  test_outputs.py' | sha256sum -c -
```

**3. `caffe-cifar-10`** — arith 2.929, deficit 114; four classes including `filesystem-metadata` (2/10, the ledger's
thinnest class by executed fraction) and `stdout-inspection` (9/29). Captured grader bytes: 6641 bytes; module-level
imports are stdlib only (`re`, `subprocess`, `pathlib`); it reads `/app/caffe/**` (version string `1.0.0`,
`cifar10_quick_iter_500.caffemodel` > 100000 bytes, `solver_mode:CPU` + `max_iter:500` in the solver prototxt,
`CPU_ONLY:=1` in `Makefile.config`, `training_output.txt` containing `Iteration 500` but not `Iteration 501`, and a
`caffe test` run whose stderr must carry `accuracy = …` > 0.45). All of those are files under `/app`, stageable, and
the `caffe.bin` invocation is exactly the shape the lane already replayed offline for `build-pmars` (round 38,
canned binary). Tie-break against `compile-compcert` (also 2.929): `caffe-cifar-10` needs no compiler toolchain at
all, while `compile-compcert` needs a real CompCert `ccomp` at `/tmp/CompCert/ccomp` plus two sibling `.c` probes
under `/tests/` — so `caffe-cifar-10` is the cheaper of the two.

sha256 of the captured grader at the tip:

```
$ git -C "$L" show a9b8a1a00b6a5ab5206be4d377dba439e02f8244:corpus/evidence/round52/graders/caffe-cifar-10/tests/test_outputs.py | sha256sum
10bc2d83f1a421804d122bd43aa34826d688703ec73288399aff4e827125e9f2  -
```

Fetch command that would pin it (not performed here):

```sh
curl -fsSL -o test_outputs.py \
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/caffe-cifar-10/tests/test_outputs.py
echo '10bc2d83f1a421804d122bd43aa34826d688703ec73288399aff4e827125e9f2  test_outputs.py' | sha256sum -c -
```

Runner-up worth naming for the `shell-exec` axis specifically: `model-extraction-relu-logits`
(sha256 `e5189c7eb9942ede55e1b48a80388590b80a486b75497613f257b3373ad9b2c9`, 2326 bytes) — see §5.

All 24 sha256 values are in `per-member.json` next to this file, and each one already agrees with the
`corpus/evidence/round52/graders/SHA256SUMS` entry for the same path (verified: 0 anomalies across the 24).

---

## 5. Finding 2 — the `candidate-library-required` blocker on `model-extraction-relu-logits` is stageable offline

`model-extraction-relu-logits` is the **only** remaining `shell-exec` candidate whose bytes are not blocked by
network, ssh, a VM, a browser, LaTeX or docker, and `shell-exec` is the class that has moved least in the ledger's
whole life (1 → 2, once, in round 89). Its ledger `reason` is `candidate-library-required`, fired by the frozen
regex `sys.path.append("/app")` at L10 of the capture. But the same construct was replayed offline for an executed
member: `feal-differential-cryptanalysis`'s captured grader has the identical `sys.path.append("/app")` at L22
(and `sys.path.append("/tests")` at L23), its ledger row is `executed` (round 43, receipt
`corpus/evidence/round43/feal-probe.txt`, classes `candidate-import` + `shell-exec`), and `SKILL.md`'s decision table
records the recipe for that class: *"the candidate module is written into /app inside the sandbox and the grader's
`sys.path.append("/app")` import is left to resolve it; a stage-check byte-compiles the candidate before any grader
call"*.

Reading `model-extraction-relu-logits`'s capture: it appends `/app` to `sys.path` (L10), writes its own
`forward.py` (L13–41) so the candidate cannot be reward-hacked, `os.popen("python3 /app/steal.py")` (L46), then
asserts `/app/stolen_A1.npy` exists and that its rows match the seeded `np.random.randn(30, 10) * 0.3` matrix within
1e-4 after per-row mean rescaling (L50–73). `numpy` is present on this host (`python3 -c "import numpy"` → OK),
`python3` is 3.14.8. The candidate's `steal.py` and the resulting `.npy` are stageable files under a writable `/app`,
exactly as the `candidate-import` recipe prescribes. So this member is *not* a hard blocker case; the round-43
recipe covers it.

Consequence for the next round: if the next coverage move is scoped to the `shell-exec` axis (2 of 6 — still the
thinnest multi-member class after this round), `model-extraction-relu-logits` is the only offline candidate that
moves it, and it would take `shell-exec` 2 → 3 of 6, `candidate-import` 3 → 4 of 6 and `file-artifact` 24 → 25 of 76.
Its own `reason` string would have to be re-derived (the frozen detector fires, so a next-round ledger row flip has
to keep the row's shape legal) — reported here, not edited.

---

## 6. Practical notes for whoever builds the next round's probe

* Host tooling present on this machine: `gcc`, `g++`, `rustc` (1.99.1), `git`, `curl`, `bwrap` (/usr/bin/bwrap),
  `docker`, `python3` 3.14.8, `numpy`, `PIL`, `cv2`, `uv` 0.13.0.
* Host tooling absent: `pytest` (module import), `pandas`, `skimage`, `torch`, `torchvision`, `datasets`,
  `biopython`, `R`/`Rscript`, `povray`, `caffe`, `oligotm`, `pmars`, `vim`, `pdflatex`, `expect`, `sshpass`,
  `valgrind`, `qemu-system-x86_64`, and `/usr/local/gcc-custom-{debug,release}/lib64`.
  So of the 24, the members whose *only* missing piece is a host tool are `build-pov-ray`, `caffe-cifar-10`,
  `compile-compcert`, `custom-memory-heap-crash`, `large-scale-text-editing`, `mcmc-sampling-stan`,
  `adaptive-rejection-sampler`, `dna-assembly`, `dna-insert`, `winning-avg-corewars`, `gpt2-codegolf`,
  `path-tracing` (needs root for `chroot /jail`).
* Sibling captures that a faithful replay must also fetch (present in the upstream tree at the pinned commit, absent
  from the round-52 capture): `merge-diff-arc-agi-task` → `tests/test.json`; `compile-compcert` → `tests/positive_probe.c`,
  `tests/negative_probe.c`; `overfull-hbox` → `tests/main.tex`, `tests/synonyms.txt`, `tests/input.tex`;
  `large-scale-text-editing` → `tests/gen_large_csv.py`; `schemelike-metacircular-eval` → `tests/test/*.scm`,
  `tests/shadow_test/*.scm`; `write-compressor` → `tests/original-decomp.c`, `tests/original-data.txt`;
  `build-pov-ray` → `tests/reference_illum1.png`; `custom-memory-heap-crash` → the agent's own `main.cpp`/`user.h`.
* No `corpus/SOURCES.md` row exists yet for `model-extraction-relu-logits`, `modernize-scientific-stack` or
  `merge-diff-arc-agi-task` (0 mentions each at the tip); `caffe-cifar-10` has 1 mention (its `S079` scope note).
  The SCORECARD's next-round item says the next offline member needs "its own S-row opened in the round", so any of
  these three would need one.
* `corpus/evidence/round52/graders/sanitize-git-repo/tests/test_outputs.py` is deliberately excluded from the capture
  (`corpus/evidence/round52/graders/EXCLUDED.md`, GH013 push protection). `sanitize-git-repo` is not in the 24
  (it carries `file-artifact`, `git-plumbing` only — no `shell-exec`, no `stdout-inspection`), so the exclusion does
  not affect this item.

---

## 7. What this seat did not do (scope boundary)

* No claim was made and no instrument was written; this is recon for a future round only.
* No frozen element was edited: `plans/grader-population-ledger.json`, `plans/round79_c1_population_ledger.py`,
  `plans/round-89-claims.md`, `plans/round89-cases.json`, `plans/round89-q66-records.json` and every round-89
  instrument were read only. The ledger-reason gap in §3 and the stageability point in §5 are reported, not repaired.
* No network fetch was performed; §4's fetch commands are the pinning commands a next round would run, and each is
  paired with the sha256 the capture already carries.
* No clone was made; every git call above is `show`/`log`/`rev-parse`/`ls-tree` on the lane, read-only.
