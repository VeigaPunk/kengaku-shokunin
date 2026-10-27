# R46ExecC3Probe — round-46 C3, wave 1: the offline `polyglot-c-py` probe, its frozen case table and stage-check

Seat `R46ExecC3Probe` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` read-only; nothing in
the lane was written. Scratch `S=/fast/scratch/hyaku/kengaku-r46/R46ExecC3Probe` (removed at the end with
`plans/scratch_guard.py safe-rm`). Frozen inputs read, never touched: `plans/round-46-claims.md` (§C3),
`plans/password_recovery_probe.py`, `plans/pkg-spec-r45.json`, `plans/round45_c2_verify.py`,
`corpus/evidence/round45/tb2-password-recovery/*`, `.ufo/waves/round-46/claims/envelope.sh`.

**ORDER RULE (Q30) honoured.** Only `--dry` (twice, byte-identical) and `--stage-check` ran. The captured
`test_outputs.py` was never imported, `test_fibonacci_polyglot` was never called, and no case's compiled output was
executed: `--stage-check` builds each end state and does a **parse-only** check of both languages (`compile()` of the
text, `gcc -fsyntax-only`). The first recorded full run remains after the stage-2 commit; the receipt path stays
`corpus/evidence/round46/polyglot-c-py-probe.txt` (the probe prints the receipt to stdout, so P10 is a byte-compare of
`--lane .` stdout).

## Axes (named before the work)

1. **coverage** — does the table cover every shape this grader can decide: listing precondition, compile step,
   dual-runtime equality, `strip()`, `check=True`, and the grader's own state poisoning.
2. **freeze integrity** — is the table frozen and byte-stable *before* any outcome exists (dry table = freeze receipt)?
3. **receipt determinism / operability** — can the stage-2 run and the gate re-run reproduce the receipt exactly
   (no temp path, host version or timing in the output; sorted listings; discarded stderr)?

## 1. Deliverables (absolute paths)

| file | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py` | 31355 | `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d` |
| `.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot-c-py-dry-cases-freeze.txt` | 5355 | `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536` |
| `.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot-c-py-stagecheck.txt` | 2722 | `65860591b8d4fd911e0da1c07cbf2ada616497bfa92e7844dea570a9c21fa540` |
| `.ufo/waves/round-46/w1/R46ExecC3Probe/dry-run-envelope.txt` | 757 | (envelope receipt of the dry run) |

`polyglot-c-py-dry-cases-freeze.txt` is exactly the probe's `--dry` stdout (26 lines: 7 `TAG`, 18 `CASE`, 1 summary
line), not the envelope wrapper — the wrapper's lines are in `dry-run-envelope.txt`. The L1 integrates by copying
`polyglot_c_py_probe.py` to `plans/polyglot_c_py_probe.py` **verbatim** and the freeze file to
`corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`; the digests above are the values to pin at stage 2.
Cross-checked with seat `R46ExecC3Spec`: their 8-capture set and digests are identical to the probe's `PINS` (7
captures; `gitignore` is capture-only and unused by the probe), so no rename is needed on either side.

## 2. The seven frozen predictions are 18 cases

`--dry` summary: `cases=18 predicted_pass=7 predicted_fail=11`. Predicted pass: `oracle-solve-sh`, `lookup-table`,
`trailing-ws`, `stderr-noise`, `compile-warning`, `regrade-same-state`, `crlf-source`. Predicted fail: the other 11.
Every case also freezes its **re-grade**: the grader's own `gcc` step writes `/app/polyglot/cmain`, so a second grade
of any state whose listing passed fails at the listing — `regrade=DIFF:F` for the 7 predicted passes, `regrade=same`
for the 11.

| # | case | predicted | violates= (instruction.md line) | the fact it isolates |
|---|---|---|---|---|
| 1 | `nop` | F | single-file:1 | image seed: `WORKDIR /app` only, no `/app/polyglot` (`environment/Dockerfile` @ pin) → `os.listdir` raises |
| 2 | `oracle-solve-sh` | P | — | the published `solution/solve.sh` run verbatim with cwd `/app` |
| 3 | `lookup-table` | P | fib-kth:7 | three graded values read out of `/pub/test_outputs.py` at recipe time, printed from a table: no Fibonacci computation |
| 4 | `python-only` | F | c-build:5 | Python that is not C → gcc parse error (`check=True`) |
| 5 | `c-only` | F | python-run:3 | C that is not Python → python `SyntaxError` (`check=True`) |
| 6 | `extra-file` | F | single-file:1 | oracle + `NOTES.md` → list compare fails before gcc |
| 7 | `leftover-cmain` | F | single-file:1 | oracle + the exact `gcc … -o /app/polyglot/cmain` that instruction.md:5 tells the agent to run → instruction and grader contradict |
| 8 | `wrong-value` | F | fib-kth:7 | real polyglot, f(42) off by one in both runtimes |
| 9 | `trailing-ws` | P | — | padded spaces/blank lines on both sides → `stdout.strip()` (`:36`, `:43`) |
| 10 | `nonzero-exit` | F | — (grader stricter) | right stdout, then `sys.exit(3)` / `return 3` → `check=True` |
| 11 | `stderr-noise` | P | — | noise on stderr in both runtimes; only stdout is compared |
| 12 | `n-parsed-differently` | F | fib-kth:7 | Python reads `argv[1]`, C reads its first digit: 42/10 disagree, 0 agrees |
| 13 | `compile-warning` | P | — | explicit `#warning` (a Python comment) → gcc exit 0, diagnostic on stderr |
| 14 | `regrade-same-state` | P | single-file:1 | the oracle state graded twice: the first grade poisons the second (non-idempotence) |
| 15 | `empty-file` | F | fib-kth:7 | zero-byte source: listing passes, python prints nothing, gcc links no `main` |
| 16 | `dir-in-place` | F | c-build:5 | a DIRECTORY at `main.py.c`: listing is exactly `["main.py.c"]`, gcc is handed a directory |
| 17 | `crlf-source` | P | — | whole source CRLF: both tokenizers accept it (parse-only evidence: `pycheck=ok ccheck=ok`) |
| 18 | `value-plus-line` | F | stdout-only:7 | value plus a second line: `strip()` trims ends only, so equality never fires |

`regrade-same-state` is a deliberate re-grade of `oracle-solve-sh`'s end state — the two rows share a recipe on
purpose: one freezes the first-grade verdict, the other freezes the second-grade verdict (measured as the `regrade=`
column of every case, so the row is checkable, not decorative).

## 3. Exact evidence

Both runs used the mandated envelope; `/home/vgpnk/.local/bin` content digest unchanged at every boundary.

### 3.1 `--dry` (the freeze receipt), run twice, byte-stable

```
$ E=.ufo/waves/round-46/claims/envelope.sh; S=/fast/scratch/hyaku/kengaku-r46/R46ExecC3Probe
$ $E "$S/env" bash -c "cd $S/lane && python3 <draft>/polyglot_c_py_probe.py --lane . --dry > $S/dry.txt"
ENVELOPE start 02:13:36 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 02:13:38 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
$ cmp $S/dry1.txt $S/dry2.txt   # second full run at 02:12:4x
BYTE-STABLE across two runs
$ tail -1 $S/dry.txt
cases=18 predicted_pass=7 predicted_fail=11
```

(`--dry` reads nothing from `--lane`, so the table is lane-independent and a counter can byte-compare it from any
clone; verified by the two runs plus the earlier `--lane .`/`--lane $S/lane` pair producing the same digest.)

### 3.2 `--stage-check` (recipes validated, grader never run)

```
$ $E "$S/env" python3 <draft>/polyglot_c_py_probe.py --lane "$S/lane" --stage-check --work "$S/work"
ENVELOPE start 02:13:40 cwd=/home/vgpnk/Projects/shokunin
STAGECHECK nop rc=0 expect=absent file=absent dir=absent pycheck=n/a ccheck=n/a match=yes
STAGECHECK oracle-solve-sh rc=0 expect=src file=bytes=872 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK lookup-table rc=0 expect=src file=bytes=582 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK python-only rc=0 expect=src file=bytes=205 dir=main.py.c pycheck=ok ccheck=fail cwarn=0 match=yes
STAGECHECK c-only rc=0 expect=src file=bytes=288 dir=main.py.c pycheck=fail ccheck=ok cwarn=0 match=yes
STAGECHECK extra-file rc=0 expect=src file=bytes=872 dir=NOTES.md,main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK leftover-cmain rc=0 expect=src file=bytes=872 dir=cmain,main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK wrong-value rc=0 expect=src file=bytes=537 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK trailing-ws rc=0 expect=src file=bytes=513 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK nonzero-exit rc=0 expect=src file=bytes=502 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK stderr-noise rc=0 expect=src file=bytes=554 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK n-parsed-differently rc=0 expect=src file=bytes=482 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK compile-warning rc=0 expect=src file=bytes=522 dir=main.py.c pycheck=ok ccheck=ok cwarn=2 match=yes
STAGECHECK regrade-same-state rc=0 expect=src file=bytes=872 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK empty-file rc=0 expect=src file=bytes=0 dir=main.py.c pycheck=ok ccheck=ok cwarn=0 match=yes
STAGECHECK dir-in-place rc=0 expect=dir file=dir dir=main.py.c pycheck=n/a ccheck=n/a match=yes
STAGECHECK crlf-source rc=0 expect=src file=bytes=514 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK value-plus-line rc=0 expect=src file=bytes=524 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
stagecheck cases=18 failed=0
ENVELOPE end 02:13:45 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

What this buys before any outcome exists: every recipe writes exactly the end state its row claims
(`match=yes` ×18); the two languages fail exactly where predicted (`python-only` → `ccheck=fail`, `c-only` →
`pycheck=fail`, `dir-in-place` → no parse at all); the lookup-table file is a real polyglot (both checks ok) so its
`P` prediction is not an artifact of a broken generator; and the oracle carries `cwarn=1` — the same
`missing terminating " character` warning the round-45 seat recorded for the pinned solution
(`.ufo/waves/round-45/w1/R45PlanNext.md` §2), which is why `compile-warning` is a *reality* of this task, not a
contrivance.

### 3.3 Grader facts the table is built on (captured `test_outputs.py`, 46 lines)

- `polyglot_files = os.listdir("/app/polyglot")` then `assert polyglot_files == ["main.py.c"]` — `:17-20`.
- `subprocess.run(["gcc", …, "-o", "/app/polyglot/cmain"], check=True)` — `:23-25` (writes into the directory the
  listing just checked; hence the non-idempotence).
- `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` — `:27`; both runtimes run with `check=True` and compare
  `stdout.strip()` — `:36`, `:43`, assertion `:44-46`.
- Only three fixed points; the source is never inspected; no timing, size or format rule.

## 4. Design notes (what a reviewer should be able to re-derive)

- **One sandbox per case** (see §7 for the hardening pass): `prlimit --nproc=48 --cpu=5 --fsize=1048576 --core=0
  --as=536870912 --nofile=512 -- bwrap --unshare-all --die-with-parent --new-session --hostname polyglot-sandbox`,
  `/usr` and `/etc` read-only, `/` remounted read-only last, `/dev` remounted read-only after a sized `/dev/shm`,
  a 32 MiB `/tmp` and a 64 MiB `/app` tmpfs, an environment supplied with `--clearenv`/`--setenv`, cwd `/app`;
  `/tests` holds only the captured `test_outputs.py`, `/pub` the three public captures at the pin, `/tpl` the
  polyglot skeleton. No host directory is bound into the sandbox. Captures are digest-checked before any case
  (7 pins).
- **No answer constant in the probe**: the three expected values are extracted from `/pub/test_outputs.py` inside
  the sandbox (`ast` walk for the `test_cases` assignment) and turned into a print table for the leak case; the probe
  source contains no `267914296`/`55`/`0`.
- **Verdict = harness exit status**, letters `P`/`F` for the one test (`AssertionError` → `F`, any other exception →
  `F error=<Class>`: `FileNotFoundError` for `nop`, `CalledProcessError` for gcc/python/non-zero exits). pytest is not
  invoked; `tests/test.sh` only wraps pytest and writes the reward file. Both grade legs run in the one sandbox
  (`TEST leg1 …` / `TEST leg2 …`), each with a freshly imported grader module; fd 1 is pointed at `/dev/null` for
  the duration of a leg so nothing a child writes can reach the receipt, and the verdict lines go to a saved
  descriptor.
- **Determinism**: listings printed sorted; gcc/pytest diagnostics discarded; no temp path, host version or timing in
  the receipt; scratch under `--work` removed on exit.

## 5. Risks and limits (stated before the stage-2 run)

1. **Toolchain divergence, named now.** Host `gcc (GCC) 16.2.1 20260810` and `Python 3.14.8` stand in for the image's
   gcc 13.2.0 / python 3.12.3 (instruction.md:9; `task.toml` `docker_image = "alexgshaw/polyglot-c-py:20251031"`,
   not pulled). Round-45 measured the oracle PASS on this same gcc, so `oracle-solve-sh`'s `P` is corroborated, but
   `crlf-source` and `compile-warning` are host-gcc facts.
2. **`--stage-check` is parse-only**: `empty-file`'s link failure and every run-time outcome (`trailing-ws`,
   `stderr-noise`, `nonzero-exit`, `n-parsed-differently`, `value-plus-line`, both re-grades) are predictions read off
   the resolved Python/C semantics and the captured asserts — not observations. That is the price of the order rule.
3. **`regrade-same-state` duplicates `oracle-solve-sh`'s recipe** by design (§2). If a later counter forbids two rows
   with one recipe, drop the row and read the `regrade=` column, which measures the same fact on all 18 rows.
4. **Capture stand-in.** `corpus/evidence/round46/tb2-polyglot-c-py/` did not exist in the lane while I ran, so the
   stage-check ran against a scratch stand-in built from `raw.githubusercontent.com/.../polyglot-c-py/` at
   `2fd12b88` — the 8 upstream bytes, digests identical to seat `R46ExecC3Spec`'s capture set (verified by message).
   Scratch is never evidence; the digests, not the stand-in, are the pin. `Dockerfile` is `environment/Dockerfile`
   upstream, `solve.sh` is `solution/solve.sh`, `test.sh` is `tests/test.sh`, `gitignore` is `.gitignore`.
5. **One test function only**, so every case's letters string has length 1 and the table cannot show a
   partial-pass (no case can pass the listing and fail only one runtime *leg* as a separate letter). Covered
   instead by case-level rows 4/5/12/18.
6. **The grader's own subprocesses stay unbounded** (`test_outputs.py:30-42`: `capture_output=True`, no timeout), so
   a payload that emits megabytes is bounded only by the sandbox's `--as` and by the 60 s kill; the probe cannot fix
   that without editing the frozen capture. Named, not papered over.

## 6. Blockers

None. The probe, the freeze table and the stage-check receipt are complete; the stage-2 run is gated on the L1's
commit, not on anything missing.

## 7. Amendment: sandbox hardening after the sentinel's review (same wave, before stage 2)

Seat `R46SentC3Sandbox-2` reviewed this draft's `sandbox_argv`/`harness` against its own hostile payload
(`.ufo/waves/round-46/w1/R46SentC3Sandbox.md`) and measured that the first argv *contained* the payload but bounded
nothing: writable `/dev` and `/dev/shm` tmpfs (~15 GiB each), a host-bound `/app`, a visible hostname and cpu count,
an env only in `subprocess(env=)`, and `timeout=1800` per leg. All six findings are applied; the case table, its
predictions and the `--dry` bytes are untouched (verified: the regenerated dry table is byte-identical to the frozen
one, digest `99adfea6…`), so the freeze receipt stands and only the probe's own digest moved (`a96e4226…`).

| fix | what the draft now does |
|---|---|
| 1 fork/cpu/file/mem bounds | `prlimit --nproc=48 --cpu=5 --fsize=1048576 --core=0 --as=536870912 --nofile=512 --` wraps bwrap (bare byte counts: `--fsize=1M`/`--as=512M` are rejected by prlimit, measured) |
| 2 sized, host-free `/app` + `/tmp` | `--size 33554432 --tmpfs /tmp`, `--size 67108864 --tmpfs /app` (the host `--bind work/app` is gone), `--remount-ro /` **last** |
| 3 `/dev` bounded | `--dev /dev --size 8388608 --tmpfs /dev/shm --remount-ro /dev` |
| 4 namespaces/identity | `--unshare-all` + `--hostname polyglot-sandbox` |
| 5 env on the argv | `--clearenv --setenv PATH/HOME/TMPDIR/LANG/LC_ALL/PYTHONUTF8/PYTHONDONTWRITEBYTECODE` |
| 6 time and output bounds | one sandbox invocation per case with `TIMEOUT=60` and a reader thread that keeps draining but stores at most `CAP_BYTES=1 MiB`; fd 1 is `/dev/null` during a grade leg |

Measured on the new argv (this seat, own payload, no grader involved; `ENVELOPE … unchanged` at 02:32:02–02:32:03):

```
host polyglot-sandbox
exists /home/vgpnk False      exists /root False      exists /fast False
etc_write EACCES              net ENETUNREACH
fork_stop 44 EAGAIN           malloc MemoryError          (600 MiB bytearray)
fill EFBIG 1048576            shm9m EFBIG                 (/dev/shm 9 MiB write stops at the 1 MiB file cap)
app_bytes 67108864            tmp_bytes 33554432          shm_bytes 8388608
```

Re-ran both allowed modes on the hardened draft: `--dry` exit 0, byte-identical to the freeze file; `--stage-check`
exit 0, `stagecheck cases=18 failed=0` with every row's `file=`/`dir=`/`pycheck=`/`ccheck=`/`cwarn=` identical to
§3.2 (gcc builds fine under `--as=536870912` and `--fsize=1048576`), `ENVELOPE end 02:31:45 exit=0
local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged`. Seat `R46ExecC3Spec` has been told the
new probe digest so the spec pin moves with the file rather than going red at stage 2.

Seat `R46SentC3Sandbox-2` then appended an addendum naming three consequences of the one-sandbox reading; all
three are now in the probe docstring's limits paragraph (docstring-only edit, no behaviour change):
**(a)** phases share a pid namespace, so an orphan from `seed.sh`/`recipe.sh` is alive at grading (bounded by
`--nproc=48` and `--die-with-parent`; every recipe here is frozen text — a future agent-authored per-case recipe
would need a namespace per phase); **(b)** one 60 s budget covers all four phases, so a killed leg 1 leaves leg 2
unrun and the receipt prints `regrade=DIFF:-`, which counts as a mismatch, not a verdict; **(c)** the fd-1 redirect
does not bound the payload — the grader's own `capture_output=True` pipe (`:30-42`, frozen) still holds its bytes,
so a megabyte emitter meets `--as=536870912` as a `MemoryError` inside the harness, leaving
`exit=…-no-verdict-line`: the host-pressure risk became a measurement instead of an ambiguous note.

That edit moved the probe digest a second time (`22b7779e…`, 31355 B; the sentinel's cited `a96e4226…` is the same
logic without those three disclosures). Re-verified after it, under the same envelope: `--dry` exit 0 and
byte-identical to the freeze file; `--stage-check` exit 0, `stagecheck cases=18 failed=0`, `ENVELOPE end 02:34:28
exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged`. Seat `R46ExecC3Spec` re-pins to
`22b7779e…`; the dry table stays `99adfea6…`, so no case, prediction or counter pin moves.

## 8. Post-yield facts from the counter and lane (measured by this seat, read-only)

1. **The lane holds a superseded revision.** `sha256sum plans/polyglot_c_py_probe.py` = `67a8f4a6…`, 27966 B —
   the second of my three drafts, with the unhardened sandbox (`--unshare-net/-pid/-ipc` at `:350`, host
   `--bind work/app /app` at `:356`, `timeout=1800`). The terminal draft is `22b7779e…`, 31355 B. The L1 has the
   landing instruction; the counter's `PROBE_SHA256` must move in the same commit.
2. **The frozen predictions were confirmed 18/18 on the first real run** — made by another seat, from the
   superseded revision. `corpus/evidence/round46/polyglot-c-py-probe.txt`, 6613 B, sha256
   `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`: 18 `CASE` lines, `match=NO` zero times,
   `regrade cases=18 differ=7`, `cases=18 observed_pass=7 observed_fail=11 mismatches=0`. Every pass/fail split,
   the 7 predicted passes and the non-idempotence column (7 `regrade=DIFF:F`, matching the 7 observed passes)
   reproduced exactly as frozen before the run.
3. **Provenance caveat, not a verdict change.** That receipt came from the unhardened probe and preceded the
   stage-2 commit, so it is a preview: the L1 must re-run the landed terminal probe and byte-compare. Expectation
   (bounds only, no verdict logic touched): identical bytes, so `dd0e3546…` stands and only `PROBE_SHA256` moves.
   Pairing `dd0e3546…` with `22b7779e…` without that compare would be a provenance defect even though the content is
   correct.
4. **Counter-side contract verified by them, not asserted by me**: their `dry_table()`/`receipt_cases()` parsers give
   `ids_equal_order=True`, 18 parsed, no false `match=yes`, one `regrade cases=18 differ=7` line, `DECISIVE` keys ==
   dry ids; `regrade=DIFF:F` is accounting, never a pass; single-letter `P`/`F` parse. Their V11 executes the grader on
   60 nonce-drawn end states rather than grepping literals, and names the lookup-shaped predictor agreement as a limit
   — which is why `lookup-table` is a case here rather than only a sentence.

## 9. L1 disposition (final, authoritative for the pin)

L1 `KengakuR46`: the stage-2 pin stays **`67a8f4a6…` (27966 B)** — the bytes committed at `cf7de6af`, before the first
recorded run `8d7f74ce`; moving the pin after the run would be a post-freeze rule change. The hardened terminal draft
`22b7779e…` (31355 B) is carried as a sandbox improvement for round 47, not landed here.

So the authoritative artifacts are: **lane probe = `67a8f4a6…`**, **dry table = `99adfea6…`** (identical under every
revision), **receipt = `dd0e3546…`** (18/18, `mismatches=0`, produced by the pinned revision). This seat's
`polyglot_c_py_probe.py` stays at `22b7779e…` in the wave directory as the round-47 starting point; the 18 cases,
their predictions and the stage-check are common to both revisions, so nothing in §2, §3 or §8 depends on which one
is landed.

Consequence for the counter's V2: the producer of the landed receipt (`dd0e3546…`) *is* the pinned probe
(`67a8f4a6…`), so the provenance item closes on the ruling rather than staying open — P10's `--rerun` byte-compare
becomes a reproduction test of a receipt whose producer is the pin. No counter change follows, and no re-pin. The
window in which "land `22b7779e…` and move `PROBE_SHA256` in one commit" would have been needed is closed, because
`22b7779e…` does not land this round. The counter's independent check of the receipt's seven `# capture … sha256=`
headers (each equal to the pins, `gitignore` undeclared) agrees with this probe's `PINS`, which pin exactly those
seven and never read `gitignore`.

VERDICT: polyglot-probe-cases-18-stagecheck-failed-0
