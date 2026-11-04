# LedgerAuditB — R79 w1 independent member audit

Axes: coverage (every assigned member), calibration (frozen reason versus actual source).

## Result and scope

**28/28 rows OK under the frozen rules; no WRONG rows.** Inclusive alphabetical bounds `gcode-to-text` through `path-tracing-reverse` contain 28 members, not 29. Independently derived 80 member-class pairs: 5 executed, 2 executed-unlocated, 21 unexecuted (18 unattempted, 3 blockers).

Read the frozen claims in full first. Audited committed bytes at `5d6843134017780c045e92eed4e83264188a7d47`, the observed `master` tip and specified freeze. Input ledger SHA256: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`.

No counter was read, imported, or executed. Census memberships were reconstructed from every committed `CLASS ... members=` line, including the untruncated long lines. `git show REV:path` supplied each grader/receipt/instrument directly; successful retrieval establishes that each artifact exists in the committed tree. No grader, build, test suite, formatter, or linter was run.

## Row-by-row retained observations

Every classes cell below is the independently derived census membership and equals the ledger array (order-insensitive). SHA256 prefixes are computed over raw committed grader bytes, not normalized text. All four frozen detectors were searched for each unexecuted row.

| Member | Result | Census classes (equal ledger) | Evidence |
|---|---|---|---|
| `gcode-to-text` | OK | file-artifact | four detectors silent; SHA256 `6b049dc626aa103b` matches |
| `git-leak-recovery` | OK | file-artifact, git-plumbing, stdout-inspection, subprocess-exec | `corpus/evidence/round39/git-leak-probe.txt` subject L1; verdict `cases`; sole named population member `git-leak-recovery` |
| `git-multibranch` | OK | file-artifact, network-service, shell-exec | four detectors silent; SHA256 `f03c6867663b8e8f` matches |
| `gpt2-codegolf` | OK | file-artifact, stdout-inspection, subprocess-exec | four detectors silent; SHA256 `6232bb719c5a4ce0` matches |
| `headless-terminal` | OK | candidate-import, file-artifact, network-service, subprocess-exec | `candidate-library-required`; matched at L8; evidence present in whitespace-normalized source |
| `hf-model-inference` | OK | filesystem-metadata, network-service | `corpus/evidence/round71/hf/receipt.txt` subject L39; verdict `predicate`; sole named population member `hf-model-inference` |
| `install-windows-3.11` | OK | crypto-credential, file-artifact, network-service, process-environment, stdout-inspection, subprocess-exec | `vm-required`; matched at L16, L16, L21, L98, L98, L102, L262, L262; evidence present in whitespace-normalized source |
| `kv-store-grpc` | OK | file-artifact, network-service | `corpus/evidence/round64/kvstore-probe.txt` subject L1; verdict `predicate`; sole named population member `kv-store-grpc` |
| `large-scale-text-editing` | OK | crypto-credential, file-artifact, stdout-inspection, subprocess-exec | four detectors silent; SHA256 `f5e69f4fedeefa23` matches |
| `largest-eigenval` | OK | numeric-band, timing-wall | `corpus/evidence/round57/eigen-probe.txt`; instrument `plans/round57_c2_eigen_probe.py`; round/debt/observations/absence of subject checked |
| `llm-inference-batching-scheduler` | OK | crypto-credential, file-artifact, filesystem-metadata, serialization-schema | four detectors silent; SHA256 `80b06b7c4ba0db28` matches |
| `log-summary-date-ranges` | OK | file-artifact | four detectors silent; SHA256 `2fc06a6ce1944ad8` matches |
| `mailman` | OK | subprocess-exec | four detectors silent; SHA256 `86ff052aeb063430` matches |
| `make-doom-for-mips` | OK | file-artifact, subprocess-exec, timing-wall | four detectors silent; SHA256 `f1748ff20bfd670a` matches |
| `make-mips-interpreter` | OK | file-artifact, subprocess-exec, timing-wall | four detectors silent; SHA256 `f1748ff20bfd670a` matches |
| `mcmc-sampling-stan` | OK | file-artifact, stdout-inspection, subprocess-exec | four detectors silent; SHA256 `07e877edc933e3a9` matches |
| `merge-diff-arc-agi-task` | OK | file-artifact, git-plumbing, serialization-schema, stdout-inspection, subprocess-exec | four detectors silent; SHA256 `2754ba6c5c5f75c9` matches |
| `model-extraction-relu-logits` | OK | candidate-import, file-artifact, shell-exec | `candidate-library-required`; matched at L10; evidence present in whitespace-normalized source |
| `modernize-scientific-stack` | OK | file-artifact, filesystem-metadata, numeric-band, stdout-inspection, subprocess-exec | four detectors silent; SHA256 `0c24195ff4652776` matches |
| `mteb-leaderboard` | OK | file-artifact | four detectors silent; SHA256 `b28f8fc8b7614801` matches |
| `mteb-retrieve` | OK | file-artifact | four detectors silent; SHA256 `e4e6b21fed6662ad` matches |
| `multi-source-data-merger` | OK | file-artifact, serialization-schema | four detectors silent; SHA256 `a070888930cf829a` matches |
| `nginx-request-logging` | OK | file-artifact, network-service, subprocess-exec, timing-wall | `corpus/evidence/round70/nginx/receipt.txt` subject L4; verdict `predicate`; sole named population member `nginx-request-logging` |
| `openssl-selfsigned-cert` | OK | crypto-credential, file-artifact, filesystem-metadata, stdout-inspection, subprocess-exec | `corpus/evidence/round59/openssl-probe.txt`; instrument `plans/round59_c1_openssl_probe.py`; round/debt/observations/absence of subject checked |
| `overfull-hbox` | OK | file-artifact, shell-exec | four detectors silent; SHA256 `09756f87d1a29df5` matches |
| `password-recovery` | OK | file-artifact | `corpus/evidence/round45/probe-run-envelope.txt` subject L3; verdict `cases`; sole named population member `password-recovery` |
| `path-tracing` | OK | file-artifact, stdout-inspection, subprocess-exec | four detectors silent; SHA256 `572e68b2843191d2` matches |
| `path-tracing-reverse` | OK | file-artifact, subprocess-exec | four detectors silent; SHA256 `c4477b901887dcbc` matches |

### Executed receipt observations

All five receipts contain exactly one census population member under token-boundary name matching (not merely one subject stamp).

- `git-leak-recovery`: receipt L1 `# tb2 git-leak-recovery grader probe ...`; L5 `CASE empty-app predicted=fail observed=fail tests=FFFFF ...`. CASE observations L5–29; no higher-precedence pass predicate or VECTOR.
- `hf-model-inference`: receipt L39 `TASK-UNDER-TEST hf-model-inference`; L9 `CASE K1 ... sandbox_rc=0`; L11 `VECTOR K1 expected=PPPP derived=PPPP agree=True`; L36 `PREDICATE R71-C1 pass`. Thus verdict is predicate, not vectors/cases.
- `kv-store-grpc`: receipt L1 `# R64-C1 receipt -- TB2 kv-store-grpc grader offline under bwrap`; L9 `CASE K1 observed=P/P/P/P/P/P/P expected=P/P/P/P/P/P/P ...`; L66 `PREDICATE R64-C1 pass`.
- `nginx-request-logging`: receipt L4 `GRADER corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py ...`; L6 `CASE K1 ... sandbox_rc=0`; L15 `VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True`; L78 `PREDICATE R70-C1 pass`.
- `password-recovery`: receipt L3 `# tb2 password-recovery grader probe ...`; L8 `CASE nop predicted=fail observed=fail tests=F- ...`; CASE observations L8–23; no higher-precedence pass predicate or VECTOR.

The two unlocated rows were additionally checked: both committed instruments name the member, receipts are under the declared round, observations exist, none of the five subject forms occurs, and the ledger names `no-subject-stamp`. `largest-eigenval` instrument L2 names the member; receipt L1–24 carries CASE observations and L27 `PREDICATE R57-C2 pass`. `openssl-selfsigned-cert` instrument L2/L5/L75 names the member; receipt L2–15 carries CASE observations and L17 `PREDICATE R59-C1 fail`. The latter is an honest execution with mismatches, not a successful probe; the frozen execution rule requires observations, not a passing probe.

## Blocker overstatement question

**No assigned blocker detector fires only on a comment or dead branch.** Matched source lines (all paths below are `corpus/evidence/round52/graders/<member>/tests/test_outputs.py`):

- `headless-terminal:8`: `sys.path.append("/app")` — live module-level code; test L13 actually imports `HeadlessTerminal` from `headless_terminal`.
- `model-extraction-relu-logits:10`: `sys.path.append("/app")` — live module-level code, not the adjacent comment L12 `# Change the forward file to prevent reward hacking.` Its ledger evidence includes that comment only as surrounding context; the detector hit is L10.
- `install-windows-3.11:16`: `return Path("/app/isos/win311.img")`; L21: `result = subprocess.run(["pgrep", "qemu-system"], capture_output=True, text=True)`; L98: `assert "qemu-system-i386" in cmdline or "qemu-system-x86_64" in cmdline, (`. The fixtures feed live test L64 `def test_qemu_running_with_correct_params(qemu_pid, cmdline, img_path):`. Other hits: L102 and L262.

Calibration caveat (not a frozen-rule failure): `candidate-library-required` is a syntactic detector, not proof that an unavailable library actually prevents replay. In `model-extraction-relu-logits`, the complete grader has no candidate-library import; L46 instead invokes `os.popen("python3 /app/steal.py").read()`, and L13–41 writes `forward.py`. Thus the path mutation is live but does not itself establish a necessary candidate-library dependency. Do not upgrade these row reasons into an independently demonstrated runtime impossibility.

## Reproduction

No WRONG rows, so no WRONG-specific reproducer is applicable. The following read-only command re-derives the core row checks without importing the counter; expected output is `members=28 pairs=80 wrong=0`:

```sh
python3 - <<'PY'
import hashlib, json, re, subprocess
L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
R = "5d6843134017780c045e92eed4e83264188a7d47"
def b(p):
    return subprocess.check_output(["git", "-C", L, "show", R + ":" + p])
C = {}
for c, ms in re.findall(r"^CLASS (\S+) count=\d+ members=(.*)$", b("corpus/evidence/round62/class-survey.txt").decode(), re.M):
    for m in ms.split(","):
        if m != "-": C.setdefault(m, []).append(c)
D = {
    "browser-required": r"selenium|webdriver\.(?:Chrome|Firefox)|chromedriver",
    "vm-required": r"qemu-system|qemu-img|/app/isos/|win311",
    "external-db-required": r"GOLDEN_SQL_PATH|/tests/golden.sql|DB_PATH = Path\(",
    "candidate-library-required": r'sys\.path\.append\("/app"',
}
J = json.loads(b("plans/grader-population-ledger.json"))["members"]
S = sorted(m for m in C if "gcode-to-text" <= m <= "path-tracing-reverse")
wrong = 0
for m in S:
    r = J[m]; good = sorted(r["classes"]) == sorted(C[m])
    if r["status"] == "unexecuted":
        raw = b(f"corpus/evidence/round52/graders/{m}/tests/test_outputs.py")
        t = raw.decode(); hits = {k for k, p in D.items() if re.search(p, t)}
        if r["reason"] == "unattempted":
            good &= not hits and r["evidence"] == "no-blocker: tests/test_outputs.py sha256=" + hashlib.sha256(raw).hexdigest()[:16]
        else:
            good &= r["reason"] in hits and r["evidence"] in " ".join(t.split())
    else:
        t = b(r["receipt"]).decode(); q = re.escape(m)
        shapes = {
            "tb2-header": rf"^# tb2 {q} grader probe",
            "receipt-header": rf"^# R\d+-C\d+ receipt -- TB2 {q} grader offline",
            "grader-path": rf"^GRADER .*corpus/evidence/round52/graders/{q}/tests/",
            "task-under-test": rf"^TASK-UNDER-TEST {q}$",
            "capture-tree": rf"^grader=corpus/evidence/round\d+/tb2-{q}/",
        }
        v = "predicate" if re.search(r"^PREDICATE R\d+-C\d+ pass", t, re.M) else "vectors" if re.search(r"^VECTOR ", t, re.M) else "cases" if re.search(r"^(CASE |case=)", t, re.M) else None
        if r["status"] == "executed":
            names = [n for n in C if re.search(r"(?<![a-z0-9-])" + re.escape(n) + r"(?![a-z0-9-])", t)]
            good &= bool(re.search(shapes[r["subject"]], t, re.M)) and v == r["verdict"] and len(names) <= 1
        else:
            good &= m in b(r["instrument"]).decode() and r["debt"] == "no-subject-stamp" and f'/round{r["round"]}/' in r["receipt"] and v is not None and not any(re.search(p, t, re.M) for p in shapes.values())
    if not good: print("WRONG", m); wrong += 1
print(f"members={len(S)} pairs={sum(len(C[m]) for m in S)} wrong={wrong}")
PY
```

## Boundaries, risks, and handoff

Only this report was written. No scratch files, fixtures, installations, source edits, mutations, or peer messages. LSP was unavailable in the exposed tool inventory and unnecessary for this data/receipt audit. No blockers. Findings apply to the pinned freeze bytes, not uncommitted changes or later commits. Parent may compare this pinned result with the final integrated ledger; no implementation repair is proposed.

Self-evaluation: accuracy 4/5 (syntactic reasons do not prove runtime necessity); completeness 5/5 (all 28 assigned members plus two unlocated rows); clarity 4/5 (wide evidence table); actionability 5/5 (pinned revision, lines, standalone reproducer); conciseness 4/5 (reproducer adds length). Overall 4.4/5. Highest-value improvement: keep any future runtime-necessity claim separate from this frozen detector audit. Would the user agree: the report explicitly answers both row validity and blocker-overstatement questions without changing the claim.
