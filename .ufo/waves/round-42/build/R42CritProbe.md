# R42CritProbe — attack on the frozen C2 probe and its receipt

Seat R42CritProbe, wave 1, hyaku run 9 (2026-10-26). Target: `plans/fibsqrt_probe.py` (frozen) and
`corpus/evidence/round42/fibsqrt-probe.txt` (frozen receipt). Nothing frozen was edited, imported as a module of
record, or relabelled; all my writes are under
`.ufo/waves/round-42/build/R42CritProbe/` and `/fast/scratch/hyaku/kengaku-r42/R42CritProbe`.

Method: read the probe in full, the five pinned captures, the four unpinned ones, `SHA256SUMS`, the frozen dry table
and the claims file; then re-ran the probe and re-derived its stated grader facts by compiling the captured `sim.c`
myself and feeding it the probe's own circuits.

Envelope for every run below (Q32):

    bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
          --proc /proc --unshare-pid --die-with-parent <command>

    start 17:24:25  bin=436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18
    end   17:27:18  bin=436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18

Host: python 3.14.8, gcc (GCC) 16.2.1, bubblewrap 0.13.1. Receipts: `R42CritProbe/envelope.txt`,
`R42CritProbe/probe-rerun.txt`, `R42CritProbe/parser-evidence.txt`.

---

## 1. What holds: the receipt reproduces byte for byte

    $ bwrap … bash -c "python3 …/plans/fibsqrt_probe.py --lane …/kengaku-shokunin --work $S/w"
    rc=0 ; tail: cases=16 observed_pass=7 observed_fail=9 mismatches=0 ; regrade cases=16 differ=0
    $ diff <(grep -v '^# capture' rerun.txt) <(grep -v '^# capture' fibsqrt-probe.txt)   # IDENTICAL

Both re-run and frozen receipt carry the same 16 CASE rows, the same `tests=` letters, `regrade=same` everywhere.
`PINS`' five digests match `sha256sum` on disk, and the four unpinned captures match `SHA256SUMS`. The probes'
declared verdict mapping (`fibsqrt_probe.py:19-22`: `pass` iff three `P`; pytest exit 0 ⇒ `reward.txt` 1 per
`test.sh:26-29`) is sound: every non-AssertionError exception in the grader maps to `F`, which is what pytest does.

Numbers I re-derived independently of the probe: `len(L28)=1195`, `len(L27)=1151`, `len(L30)=1279`,
`len(GRADED)=28` distinct, max 48401; and `sim` on the LF circuit gives `41→8`, `48401→3361931507`, `208→0`,
`20000→0`, `5→0` — so the receipt's headline "prints 0 for the instruction's own examples 208 and 20000" is true.

## 2. Defects

### D1 — `sim.c` fact stated in the probe docstring is wrong, and it is the mechanism of one case

`plans/fibsqrt_probe.py:27` says `sim.c` "skips every line that does not scan as `out%d = <op>`". Measured: a line
that *does* scan as `out%d = <op>` but whose right side matches none of the six forms is **not skipped**. `sscanf`
succeeds (`sim.c:113`), the copy branch fails (`sim.c:126`, because `strstr(op," ")` now matches), the binary branch
fails (`sim.c:156`), and the gate keeps its BSS value — enum 0, `OP_CONST_0` (`sim.c:9`). `simulate_step` queues
**every** signal at step 0 (`sim.c:230-233`), so that gate actively drives its signal to 0. Only lines that fail the
first `sscanf` are skipped (`sim.c:113-114`).

Evidence (`R42CritProbe/parser-evidence.txt`, all runs of the captured, gcc‑16‑compiled `sim.c`):

| build | input | printed | what it shows |
|---|---|---|---|
| `out40 = out0` alone | 1 | `0` | out0 is undeclared ⇒ CONST_0; the argv bit is destroyed |
| same, after declaring `out0..out31 = out_i` | 1 | `2147483648` | declaring the inputs is what preserves them |
| L28 with one trailing space on the **single last** line | 48401 | `1214447859` (vs `3361931507`, Δ = `2147483648` = 2³¹) | one unparsed copy clears exactly bit 31 of the print window |
| L28 with a trailing space on the **first 32** self-copies only | 41, 48401 | `0`, `0` | the inputs are zeroed, not "left alone" |
| 32 self-copies (unspaced) + 32 `outK = out0 & out0`, the binary lines trailing-spaced | 1 | `4294967295`, identical to the unspaced build | trailing space does **not** break `&`/`\|`/`^` lines |

Consequences: (a) `lookup-28-trailing-space` (probe `:189-191`) fails because its copies become CONST_0 assignments,
not because they are skipped — the parenthetical "copy lines no longer scan as copies" is true but half the story;
(b) the captured example's 32 `out_i = out_i` lines are load-bearing for exactly this reason, which the probe never
says; (c) every case's verdict is unchanged by the correction (7 pass / 9 fail stand), so this is a prose defect, not
a predicate defect. Impacted axis: coverage (the entry would otherwise publish a wrong mechanism).

### D2 — both padded rows omit two tags their own build violates

`lookup-28-padded-31999` (`:177-178`) and `lookup-28-padded-32000` (`:179-181`) append 30804 / 30805 empty strings,
so the file's **last 32 lines are blank**. `sim.c` prints `values[num_signals-32+i]` (`sim.c:340-345`), not the last
32 lines, so both cases pass that way — the same divergence that earns `lookup-28-reversed-lines` its
`last-32-lines` tag (`:185-186`) — yet neither padded row carries `last-32-lines`. Both also contain tens of
thousands of lines that are not "of the form" of `instruction.md:1`, and `line-form` is carried by
`lookup-28-comment-lines` (`:182-183`) for a comparable non-form line, but not by the padded rows. Receipt rows
(`fibsqrt-probe.txt:10-11`) show `violates=line-limit,output-function,example-208,example-20000` (32000) and
`violates=output-function,example-208,example-20000` (31999).

Impact: none on the V7 labels — `last-32-lines` and `line-form` stay `unenforced` either way (all tagged cases pass) —
so no predicate risk; the cost is that the receipt's `violates=` understates what the grader ignores, and a reader
comparing the two rows will think reversal is the only positional divergence measured.

### D3 — no tag, and no case, for `instruction.md:8`, which the probe itself says diverges

`TAGS` (`:76-84`) has seven entries (lines 1, 9, 11×3, 12, 13) and **none for `instruction.md:8`** ("the first 32
lines are defined by the binary representation of stdin"), although the docstring asserts the divergence
(`:27-28`: "sets signals 0-31 from argv[1] (not stdin)"). The receipt already contains the observation unattributed:
`nop` (PPF) and `lookup-28` (PPP) both run with files whose first 32 lines are `out_i = out_i`, and the shipped
`gates.txt` is exactly those 32 lines (`gates.txt:1-32`) — under `sim.c` those lines are argv-driven, so line 8 is
false for a file the grader passes. Because no `violates=` carries a line‑8 tag, V7 must produce no map row for
line 8, and no receipt row can be cited for the sentence "the grader never reads stdin".

Second half of D3: stdin is not pinned where it would matter. The recipe gets `stdin=DEVNULL` (`:201`) but the
grader's own `subprocess.run(["/app/sim", …])` inherits the harness's stdin, which inherits the caller's (`:266`
sets no `stdin`), so "argv, not stdin" is untestable as built — `sim.c` simply never reads stdin, which is why the
receipt is stable.

### D4 — the receipt is not self-contained on the cwd its one cwd-sensitive verdict needs

`fake-sim-script` (`:192-194`) is `PPF` only because test 3 compiles `gcc -O3 /tests/sim.c -o sim` **into the cwd**
and then runs the absolute `/app/sim` (`test_outputs.py:66`, `:119`); `sim.c` in turn reads `gates.txt` relative to
that same cwd. The probe fixes cwd `/app` (`:234`, `:238`, recipe `:201`) and justifies it from `Dockerfile:3`
(`WORKDIR /app`) alone (`:12`). The captured `test.sh` only refuses `/` (`test.sh:12-16`), so the receipt by itself
cannot exclude another cwd.

Resolved in this wave, not by the probe: sibling seat `R42ScoutHarborCwd` (verdict `harbor-cwd-app`) read Harbor at
two pins plus the image config and found the verifier runs `docker compose exec` with no `-w`, so cwd is the image
`WorkingDir=/app`; it also measured that under any other writable cwd **nine of sixteen** verdicts move and
`fake-sim-script` flips to `PPP`. Net: the verdict is sound, but the receipt cannot be read alone, and the frozen
`Case` text does not name the dependency. Impacted axis: coverage/operability (attribution), not the predicate.

### D5 — five of nine captures pinned; the probe's own stated facts cite the other four

`PINS` (`:63-69`) covers `test_outputs.py`, `sim.c`, `gates.txt`, `solve.sh`, `instruction.md`. The probe's sandbox
shape and verdict mapping are read off `Dockerfile` (`WORKDIR`, `COPY` lines) and `test.sh` (pytest ⇒ reward), and
`task.toml` supplies the resource facts — none of the three is digest-checked, and `SHA256SUMS` (all nine rows) is
never read (`grep -n SHA256SUMS plans/fibsqrt_probe.py` → no match). A tampered `Dockerfile` or `test.sh` passes
`SETUP` (`:307-311`) untouched. Low severity (the C2 counter pins the capture directory), but the probe's own pin
discipline is narrower than its claims.

## 3. The two derivations the assignment asks for

**Why trailing spaces break the copies.** `sscanf(line, "out%d = %[^\n]", …)` (`sim.c:113`) puts everything up to the
newline into `op`, trailing space included. For `out1194 = out1162 `, `op = "out1162 "`: the copy test is
`strncmp(op,"out",3)==0 && !strstr(op," ")` (`sim.c:126`) — the space kills it; `strncmp(op,"~out",4)` fails; the
binary `sscanf(op,"out%d %c out%d")` (`sim.c:156`) needs three fields and returns 1. No branch runs, so
`gates[1194].type` stays `OP_CONST_0` and step 0 overwrites the signal with 0. Measured: Δ = exactly 2³¹ when only
the last copy carries the space. Binary gates are unaffected (`op = "out20 & out21 "` still yields three fields) —
confirmed (`4294967295` with spaces, identical to clean).

**Why CRLF does not.** `%[^\n]` stops at `\n`, so `op = "out1162\r"`. The copy test passes (`\r` is not a space),
`sscanf(op,"out%d")` yields 1162, and the gate is a real copy; binary gates likewise stop after the third `%d`. Only
`strcmp(op,"0")` / `strcmp(op,"1")` (`sim.c:122-125`) break, and the default they land on *is* `OP_CONST_0` — correct
for `"0\r"`, wrong for `"1\r"`. Measured: the whole L28 under CRLF is bit-identical to LF at 41, 48401, 208, 20000,
5 (`8`, `3361931507`, `0`, `0`, `0`), and the shipped example under CRLF still prints `12→6`, `41→20`. But the
example with `out32 = 1` prints `2147483654` under LF and `6` under CRLF — **CRLF passes only because `lookup()`
never emits a `= 1` line** (verified: 0 const lines in L28; every one of the 32 answer bits occurs among the 28
graded values). The case is honest as built; the entry must not generalise it to "CRLF is safe".

## 4. Per-case audit of build-vs-text (all 16)

All 16 builds match their `requirement` text; I re-derived each end state from `Case`/`lookup()`/`run_case`:

| case | built | text accurate | notes |
|---|---|---|---|
| nop | seeded `gates.txt` (33 lines) | yes; `12→6`, `41→20` measured | |
| oracle-solve-sh | seeded + `bash /cap/solve.sh`, cwd `/app` | yes (`solve.sh:422`) | cwd assumption (D4) |
| no-gates-file / empty-gates-file | unlink / `b""` | yes; empty ⇒ rc 0, no output, measured | |
| lookup-28 / -27 / +examples / -bitflip | `text(L28)` etc., 1195/1151/1279/1196 lines | yes; exactly the 28 graded inputs, 0 elsewhere (5, 208, 20000 measured) | |
| padded-31999 / -32000 | 31999 / 32000 newline-terminated lines | yes | tag omissions (D2) |
| comment-lines | `# note` before every gate line, 2390 lines | yes; comments are truly skipped (`sscanf` returns 0) | |
| reversed-lines | `reversed(L28)`; last 32 lines are the 32 self-copies | yes | reversal is a no-op for `sim.c` (index-addressed), so the case carries information only about `instruction.md:9` |
| crlf | `text(L28,"\r\n")` | yes | bit-identical to LF here (D1/§3) |
| trailing-space | `[x+" " for x in L28]` | build yes; mechanism half-stated (D1) | |
| fake-sim-script | seeded + executable `/app/sim` (measured `208→377`, `20000→1407432322`, `41→8`) | yes as a built state | script is overwritten before it runs (D4) |
| gates-is-directory | `mkdir` at `gates.txt` | yes; `PFF`, `IsADirectoryError` on test 2 | |

## 5. Sandbox fidelity against the image, where it matters

| image fact | source | sandbox | verdict |
|---|---|---|---|
| `WORKDIR /app`, cwd for the verifier | `Dockerfile:3`; `test.sh:13` | `--bind … /app`, `--chdir /app` (`:234`,`:238`), harness recipe cwd `/app` (`:201`) | faithful, but see D4 |
| `/app` starts with `sim.c` and `gates.txt` | `Dockerfile:9-10` | copied before grading (`:248-249`) | faithful |
| `/tests` holds `test_outputs.py` **and** `sim.c`; gcc compiles `/tests/sim.c` in the cwd | `test_outputs.py:66` | both ro-bound (`:235-237`), `/app` writable | faithful |
| gcc available | `Dockerfile:6` | `/usr/bin/gcc` required (`:71`) | faithful (version differs, declared) |
| verifier runs `test.sh` under `uvx -p 3.13` and writes `/logs/verifier/reward.txt` | `test.sh:18-29` | not run; verdict = pytest semantics as all-three-`P`; no `/logs` | declared (`:19-22`, `:43-45`); equivalence holds because reward is a pure function of pytest's exit code |
| python 3.13 / Debian gcc | `Dockerfile:2` | host 3.14.8 / gcc 16.2.1 | declared limit |
| root-owned `/app` | image | probing user owns `/app` | immaterial: no case depends on ownership; `gates-is-directory` needs write access and gets it |
| no `/home`, no `~/.local/bin` inside | — | `/usr`, `/etc` ro, private `/tmp`, `/proc`, `/dev`; `/home` absent | host-safe (§ envelope) |

Determinism supports the receipt: `sim.c`'s heaps are index-ordered, the step count is fixed at 32000, and `lookup()`
sorts its values, so no environment leaks into a verdict.

## 6. Coverage gaps (frozen at 16; the entry must not claim these)

1. **`/app/sim.c` tampering.** `Dockerfile:8` invites the agent to use `/app/sim.c`; the grader compiles `/tests/sim.c`.
   No case deletes or corrupts `/app/sim.c`, so the fact "editing the agent-visible simulator is harmless" is
   unmeasured.
2. **`/app/sim` left behind and `gcc` failing.** Only the script that gets overwritten is probed; a *directory* named
   `sim` (compile fails ⇒ test 3 `F`) is not.
3. **`instruction.md:8`** — see D3; no case, no tag.
4. **`/logs` and `test.sh`'s `$PWD` guard** are never exercised; the probe's equivalence argument is by definition, not
   by execution.
5. **`regrade`** re-runs the same three functions twice in one process on one end state (`:19-22`), so `differ=0` is
   determinism of a repeat, never independence of a rebuild — correctly disclosed, but it must not be cited as
   reproducibility evidence (my §1 rerun is the reproducibility evidence).

## 7. Smallest safe corrections (nothing frozen edited)

- For D1: the entry states the measured rule — "a signal with no parsed gate is `OP_CONST_0`; a line that scans as
  `out%d = …` but matches no form zeroes its signal; only lines that fail the first `sscanf` are skipped" — and
  explains `lookup-28-trailing-space` by that rule. No probe edit; the docstring's sentence is frozen and wrong.
- For D2/D3: the entry names the two untagged observations (padded rows also show `last-32-lines` and `line-form`
  unenforced; `nop`/`lookup-28` pass with argv-driven first 32 lines) as observations the `violates=` column does not
  carry, and draws no V7 row for `instruction.md:8`. If the L0 wants a mapped row, that is a wave-2 refreeze
  decision, not a silent edit.
- For D4: the entry cites `R42ScoutHarborCwd` (`harbor-cwd-app`) for cwd = image WORKDIR `/app` and states that
  `fake-sim-script` `PPF` holds only there (nine of sixteen verdicts move otherwise). Do not restate the Dockerfile
  line as if it settled the harness's behaviour.
- For D5: cite `SHA256SUMS` for `Dockerfile`, `test.sh`, `task.toml`, `README.md` instead of implying `PINS` covers
  them.

Files (all < 1 MiB): `R42CritProbe/envelope.txt` (Q32 envelope, start/end `date +%T`, `~/.local/bin`
digests), `probe-rerun.txt` + `probe-rerun.err` (frozen probe re-run, byte-identical to the receipt),
`parser-evidence.txt` (the five parser measurements), and the three drivers `exp.py`, `exp2.py`, `exp3.py`
(they import the frozen probe read-only and run the captured `sim.c` compiled with gcc 16.2.1).

VERDICT: probe-defects-5
