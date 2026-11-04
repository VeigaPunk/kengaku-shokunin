# SentinelR76 — frozen instruments security / blast radius

Axes: **coverage, calibration**. Review dimensions: network/path confinement, bounded work, execution provenance, write isolation, credential access. Sources below are exclusively freeze `42fad4827797e540c60a00821d3f2f5c18539632`, not the moving worktree. No production edits, git mutations, external HTTP requests, credentials, or other agent runtimes were used. No tools installed or updated.

## Commands and evidence

Read `plans/round-76-claims.md` in full before any command. Read godspeed/security-review skills. All source pointers below are `plans/<filename>:line` at the freeze; immutable copies and executable bounded fixture driver are in `.ufo/waves/round-76/w1/SentinelR76/`.

Exact source extraction commands (each exit **0**):

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 42fad4827797e540c60a00821d3f2f5c18539632:plans/round76_c1_surface_resolver.py
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 42fad4827797e540c60a00821d3f2f5c18539632:plans/round76_c2_defect_discharge.py
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 42fad4827797e540c60a00821d3f2f5c18539632:plans/round75_c1_index_parity.py
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 42fad4827797e540c60a00821d3f2f5c18539632:plans/round75_c2_registry_audit.py
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 42fad4827797e540c60a00821d3f2f5c18539632:plans/round74_c2_registry_audit.py
```

Last three executed with Python `subprocess.run([...], capture_output=True, text=True)`; the first two also ran directly. Their stdout was retained as the corresponding source copies via the tool Python kernel. File inspection used read/grep tools, not shell commands.

Exact fixture shell body, cwd `.ufo/waves/round-76/w1/SentinelR76`, exit **0**:

```sh
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r76/SentinelR76"; trap 'rm -rf -- "$S"' EXIT; mkdir -p "$S"; python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/SentinelR76/probe.py
```

The Bash tool invoked this body through `eval`. The fixture imports saved frozen source without generating pycache; all fixture writes were inside this seat's scratch, removed by the EXIT trap. The non-local URL opener and C2 child execution were intercepted, not executed. The redirect test used a temporary loopback server, shut down/closed/joined in `finally`.

Verbatim key output (ephemeral server port was 39899):

```text
ROW '../outside.md' => ['SURFACE 1 present ../outside.md (path=../outside.md)', 'SURFACES total=1 present=1 absent=0 prose=0', 'AGREE agree=1 disagree=0'] []
ROW '/fast/scratch/hyaku/kengaku-r76/SentinelR76/outside.md' => ['SURFACE 1 prose crafted', 'SURFACES total=1 present=0 absent=0 prose=1', 'AGREE agree=0 disagree=1'] ['DEFECT NOANCHOR 1 crafted']
ROW 'file:///nonexistent/sentinel' => ['SURFACE 1 prose crafted', 'SURFACES total=1 present=0 absent=0 prose=1', 'AGREE agree=0 disagree=1'] ['DEFECT NOANCHOR 1 crafted']
ROW '~/../../nonexistent-sentinel' => ['SURFACE 1 absent ~/../../nonexistent-sentinel (path=~/../../nonexistent-sentinel)', 'SURFACES total=1 present=0 absent=1 prose=0', 'AGREE agree=0 disagree=1'] ['DEFECT UNDECLARED-ABSENT 1 crafted ~/../../nonexistent-sentinel']
NONLOCAL-ROW ([], ['SURFACE 1 present http://192.0.2.1/sentinel (http=200)', 'SURFACES total=1 present=1 absent=0 prose=0', 'AGREE agree=1 disagree=0'])
NONLOCAL-REQUEST-INTERCEPTED ['http://192.0.2.1/sentinel']
REDIRECT-ROW ([], ['SURFACE 1 present http://127.0.0.1:39899/redirect (http=204)', 'SURFACES total=1 present=1 absent=0 prose=0', 'AGREE agree=1 disagree=0'])
REDIRECT-HITS [('127.0.0.1:39899', '/redirect'), ('localhost:39899', '/final')]
LONG-HOST-EXCEPTION UnicodeEncodeError 'idna' codec can't encode characters in position 0-299: label too long
BRACES '~/{a,{b,c}}/x' targets= 4 first= ~/a/x last= ~/c/x
BRACES '~/{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}' targets= 4096 first= ~/aaaaaaaaaaaa last= ~/bbbbbbbbbbbb
BRACE-DEPTH-EXCEPTION RecursionError
C1-RECEIPT-RC 0
C1-OUTSIDE-LANE-OVERWRITTEN True
C2-BATTERY-RECEIPT-RC 0
C2-OUTSIDE-LANE-OVERWRITTEN True
ROW-COMMAND-ONLY-REGEX False
PROBE COMPLETE
```

Each crafted row is exactly `| crafted | \`TOKEN\` | fixture |` under the three-column Surfaces header (see probe.py). This tests more than three crafted rows; the network 200 for the documentation address is explicitly synthetic and establishes dispatch acceptance only, not live connectivity.

## Findings

1. **HIGH — committed row controls unrestricted HTTP destination and redirect chain.** `round76_c1_surface_resolver.py:63,133-134,154-161`. ENDPOINT accepts any HTTP(S) authority, not only 127.0.0.1; `urlopen` follows redirects without destination validation. Counterexample token `http://192.0.2.1/sentinel` reaches the intercepted opener unchanged. A real loopback redirect to a different hostname was followed (output above). Impact: anyone supplying measured markdown can cause GETs to remote/internal services under the invoking user's network context, including side effects of unsafe GET endpoints; localhost-only provenance is false. No request body is read by this function, but the request itself crosses the boundary. Smallest remediation: validate scheme, parsed hostname and port against the intended loopback policy before opening; disable redirects or revalidate each Location; disable inherited proxies for these probes. External redirection is inferred from the demonstrated default redirect behavior, not executed.

2. **MEDIUM — row escapes declared filesystem roots (metadata oracle, not content read).** `round76_c1_surface_resolver.py:60,135-138,169-170`. `../outside.md` is accepted as repo-relative and resolves outside the fixture lane; `~/../../nonexistent-sentinel` is accepted without home containment checks. Symlinks are followed by `Path.exists`. Bare absolute paths and `file://` are rejected as NOANCHOR, but those lexical restrictions do not prevent traversal. Impact: existence checks anywhere accessible to the process, potentially slow automount/network filesystem touches, and misleading surface provenance. Neither path branch writes nor reads file contents. Smallest remediation: normalize/resolve each expanded target and require containment in the permitted lane/home root, with explicit symlink policy; reject traversal components when parsing.

3. **MEDIUM — no brace expansion bound; exponential work and uncaught recursion failure.** `round76_c1_surface_resolver.py:143-151,169-170`. Flat n binary groups yield **2^n targets**, each stored and then stat'ed; no configured upper bound exists. The bounded 12-group case generated 4096 targets; nested `~/{a,{b,c}}/x` produced 4 entries (duplicate `~/a/x` from innermost-first expansion), not 3 distinct alternatives. A token `~/` + `{a}` repeated `sys.getrecursionlimit()+10` times produced `RecursionError` without allocating an exponential list. Impact: committed markdown can exhaust CPU/memory or abort the gate before a receipt. Smallest remediation: cap row length, brace nesting/substitutions, and total produced targets before materialization, returning a setup/defect result instead of an exception. Do not rely on Python's recursion limit as an expansion limit. Large destructive bombs were not run.

4. **LOW — malformed hostname bypasses controlled error reporting.** `round76_c1_surface_resolver.py:154-161`. Exact token construction `http://` + `a` repeated 300 times + `.invalid/` raises uncaught `UnicodeEncodeError` during IDNA encoding. Impact: one committed row aborts the run and prevents its verdict/receipt; no network request is needed. Smallest remediation: validate URL/hostname lengths and encoding before probing, and map malformed URL errors to an explicit defect rather than an uncontrolled traceback. This is separate from timeout/network absence.

5. **MEDIUM — caller-selected receipt can overwrite arbitrary writable file.** C1 `round76_c1_surface_resolver.py:245-247,425-430`; C2 `round76_c2_defect_discharge.py:386-388,616-621`. Both accept an unrestricted `Path`, create parent directories, and `write_text` truncates existing files (also follows symlinks). Tests overwrote two inert marker files outside the supplied fixture lane but inside this seat's permitted scratch. C2 was exercised through its battery receipt writer; its emit writer has the same unconfined operations, statically observed, not independently executed. Impact: an untrusted wrapper/argument provider can clobber user files or tracked lane content; a markdown row alone cannot select this argument. Smallest remediation if receipt confinement is intended: resolve under a designated output root, reject outside/symlink destinations, and refuse unintended replacement. Treat this as a CLI trust boundary, not remote code execution.

6. **MEDIUM — C2 ordinary checks delete shared fixed scratch; --work does not isolate them.** `round76_c2_defect_discharge.py:360-361,460-462`; transitive `round75_c1_index_parity.py:153-156,188-214`, `round75_c2_registry_audit.py:176-180,247,306-308,326`. Normal emit uses `/fast/scratch/hyaku/kengaku-r76/c2`, ignoring `--work` and HYAKU_SCRATCH. Its two child selftests recursively remove/rebuild predictable subtrees; fixture legs use the separate fixed `_fixture` subtree. Impact: concurrent gates race/delete one another's evidence; preexisting content under the fixed child names is deleted. Child processes have no timeout, and abnormal termination may leave fixtures (C1 child has finally cleanup; C2 child normal-path cleanup only). Smallest remediation: allocate a private per-invocation temporary directory under the requested work root, pass it through every leg, and clean it in finally. This was inspected, not run against shared scratch.

7. **INFO — mutable executable dependencies, not row-command execution.** `round76_c2_defect_discharge.py:208-224`; `round75_c2_registry_audit.py:48-57`. C2 executes two scripts from the selected **worktree probe**, even though the gate source under review is frozen. The registry child imports/executes `plans/round74_c2_registry_audit.py` from beside itself. Their source/targets can be replaced or symlinked by a lane writer; `--probe` explicitly changes that trust root. Impact: this gate is not a sandbox for an untrusted lane, and freeze provenance does not attest its executed dependency bytes. No exploit script was installed or executed. Smallest remediation: document trusted-code assumption; if frozen execution is required, verify/extract all executable dependencies from the intended commit before executing them. Ledger `check` text is only tested by two regexes, never passed to a shell or subprocess. The inert text `echo 'sentinel'; SCORECARD.md` returns `check_trivial=False` but is not executed.

## C2 process inventory (all modes)

`git(repo,*args)` always invokes `['git','-C',str(repo),*args]`, capture_output/text enabled, **no shell and no explicit cwd** (inherits invoker cwd; Git's repository context comes from -C). Direct normal/revision gate git operations:

- startup: `rev-parse --verify --quiet master^{commit}`, fallback `HEAD^{commit}`;
- Reader: `rev-parse --verify --quiet <rev>^{commit}` or `master^{commit}`;
- revision reads: `show <rev>:<relative-file>`; scope listing `ls-tree -r --name-only <rev> corpus/lessons`; Reader.exists also defines `cat-file -e <rev>:<relative-file>` (not called on ordinary emit path);
- index derivation: `show 43255758:corpus/README.md`, `ls-tree -r --name-only 43255758 corpus`;
- ancestry: `rev-parse --verify --quiet <sha>^{commit}`, optional master fallback, `merge-base --is-ancestor <resolved-full-sha> <tip>`;
- receipt stamp: `status --porcelain --untracked-files=no` and, in battery mode, master rev-parse.

Two Python children for normal worktree derivations, exact captured argv below. Production work value is `/fast/scratch/hyaku/kengaku-r76/c2`; fixture capture used this seat's scratch instead:

```text
C2-CHILD ['/usr/bin/python3', '/fast/scratch/hyaku/kengaku-r76/SentinelR76/lane/plans/round75_c1_index_parity.py', '--selftest', '--work', '/fast/scratch/hyaku/kengaku-r76/SentinelR76/work/d4c1'] {'capture_output': True, 'text': True, 'cwd': '/fast/scratch/hyaku/kengaku-r76/SentinelR76/lane'}
C2-CHILD ['/usr/bin/python3', '/fast/scratch/hyaku/kengaku-r76/SentinelR76/lane/plans/round75_c2_registry_audit.py', '--selftest', '--work', '/fast/scratch/hyaku/kengaku-r76/SentinelR76/work/d4c2'] {'capture_output': True, 'text': True, 'cwd': '/fast/scratch/hyaku/kengaku-r76/SentinelR76/lane'}
```

Child C1 selftest itself spawns no processes. Child C2 selftest spawns Git for lane_tip (default lane `.` in cwd=probe; rev `master`), status, receipt rev-parse and `merge-base --is-ancestor`; it does **not** execute fixture registry entry/self-test strings. Imported R74 module parses script text with ast, does not execute those fixture scripts. Normal `--rev` bypasses both Python children; C2 selftest/mutant/control modes call the children repeatedly via fixture_legs.

Explicit `--selftest-git` additionally invokes Git in `work/c2_git`: `init -q`; `rev-parse --show-toplevel`; `add f`; `-c user.name=fixture -c user.email=fixture@invalid commit -qm one`; `rev-parse HEAD`; same identity + `commit -qam two`; `rev-parse HEAD`; `checkout -q -b side <first>`; `add g`; same identity + `commit -qm side`; `rev-parse HEAD`; Reader/ancestry probes listed above. This mode was **not run**. Its source checks top-level before the first commit, but uses a predictable directory rather than the assignment's mktemp fixture convention.

Lane records cannot inject a new argv element: no shell=True; ledger close_commit is extracted as a 40-lowercase-hex token before ancestry; receipt stamp and CLI rev strings occupy revision arguments, and check text is regex-only. Caller --probe/--lane change paths; editable scripts can of course execute arbitrary code. Git/Python executable discovery, inherited environment, Git config (including optional fsmonitor execution on status), imports, and filesystem symlinks remain ambient trusted process surfaces, not an exhaustive OS-level syscall trace.

## Complete application file / write inventory

**C1 reads:** ordinary mode directly opens only `lane/PROVINCE.md` as text (revision mode gets that blob through Git). Surface paths receive existence/stat probes only; endpoints receive GETs and status handling. Control mode also reads `PROVINCE.md` relative to the script's lane. Fixture modes write/read `<work>/c1_<case>/{present.md,PROVINCE.md}` or `<work>/c1m_<mutant>/{present.md,PROVINCE.md}` and recursively remove those roots; control recursively removes `<work>/c1_control_declared` even though it does not build that fixture. Optional receipt in every applicable mode writes caller `--receipt` plus missing parent directories. The fixture Listener is SimpleHTTPRequestHandler bound to loopback, serving the invoking cwd during the battery; not an internet listener.

**C2 direct text reads:** `corpus/routed-findings.jsonl`; newest matching `corpus/lessons/round-<N>-verifier-spotcheck.md` (scope discovery globs names first); `corpus/QUALITY.md`; `SCORECARD.md`; `SKILL.md`; `LOG.md`; `corpus/evidence/round75/c1-after.txt`; `corpus/evidence/round76/r74-c1-tip.txt`; `corpus/evidence/round76/r74-c2-tip.txt`; `corpus/lessons/round-74.md`. Git additionally reads `43255758:corpus/README.md` and tree metadata; --rev reads the listed lane inputs as Git blobs instead. Git reads repository objects/refs/config/index as necessary. No ledger-provided `check` path is opened by C2.

**C2 direct writes:** optional arbitrary receipt; ordinary fixed `.../c2` scratch directory; fixture derivation fixed `.../c2/_fixture`. Selftest/mutant/control roots under selected --work (`c2_<case>`, `c2m_<mutant>`, `c2_control_status`) write exactly the same ledger/QUALITY/SCORECARD/SKILL/LOG/round75 stamp/round76 receipts/round74 lesson listed above plus fixture `corpus/lessons/round-75-verifier-spotcheck.md`; roots are recursively replaced/deleted. Explicit selftest-git writes `work/c2_git/{f,g,.git/**}` and deletes its tree.

**Transitive C2 child files:** Python reads the two R75 scripts and R74 registry module (+ ordinary interpreter imports, potentially import bytecode cache writes beside R74). C1 child writes/reads `d4c1/c1_child/<case>/corpus/README.md`, writes `corpus/knowledge/{a,b}.md`, `corpus/lessons/round-{1,2}.md`, makes `corpus/evidence/{d1,d2}` directories, lists their entries, then deletes c1_child. C2 child reads/writes `d4c2/mutants_r75/<case>/SKILL.md`, `plans/round-71-claims.md`, `plans/tool_{a,b,doc,help}.py` (doc/help only applicable arms); missing/ghost paths are existence checks only. It writes/reads `d4c2/stamps_r75/{unstamped,stamped}.txt`; both subtrees are deleted. Readable script text is parsed, not executed. Git config/object/ref/index files are indirectly accessed by the spawned Git processes. All fixture case names and paths are deterministically defined in the retained source copies; no data-selected credential path is part of this inventory.

**Secrets conclusion:** neither gate explicitly opens credential stores, `.env`, SSH keys or tokens. That is not a universal guarantee of zero credential material access: C1 permits arbitrary HTTP(S), urllib inherits proxy configuration and HTTPS CA behavior, symlinked declared text files can redirect reads, mutable Python children/imports run with user permissions, and Git reads user/repository config. No credential material was opened or printed by this fixture. A syscall-level census of interpreter/OS support files was not performed; the inventory above is application-level, not a claim that the process opens no other system files.

## Limits and handoff

No real gate target predicate, full battery, non-local network, dangerous volume, shared scratch, fsmonitor configuration, credential content, or arbitrary code payload was exercised. C2 constructor argv was intercepted; receipt writer was tested in isolation rather than running shared-scratch emit. No resume_continuity_v1 API exists in these assigned sources, so the role's rejection-mutation requirement has no applicable surface here. Production behavior/frozen predicates were not reworded or remediated. All reachable assigned review surfaces were covered; retained probe/source copies are audit evidence, not proposed production changes.

Self-evaluation: accuracy 4 (network acceptance distinguished from real external access); completeness 4 (application inventory, not syscall tracing); clarity 4 (long inventory needed for requested coverage); actionability 4 (each issue has file:line and smallest change, remediation not authorized); conciseness 4 (source copies avoid repeating all fixture implementations). Overall 4.0. Main tradeoff: bounded/intercepted probes establish dispatch and failure behavior without operationalizing external requests or executing mutable lane code.
