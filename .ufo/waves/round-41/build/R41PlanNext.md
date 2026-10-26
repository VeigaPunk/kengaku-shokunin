# R41PlanNext — `### Planned (round 42)` data walk (kengaku r41, wave 1, scout)

Seat: R41PlanNext (scout, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; measured on a `--shared` clone of HEAD
`fc79f2a49be0221e138b3885fa0d83bc43b31a42` (`git -C $S/lane rev-parse --show-toplevel` = `$S/lane`, `S=/fast/scratch/hyaku/kengaku-r41/R41PlanNext`).
Nothing in the lane was edited, staged or committed; no frozen file was touched. Every mutant/counter/sandbox run went through
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`
(TB2 graders and the CRLF probe additionally in a `--unshare-net` sandbox with `/usr` read-only). Receipts and the harness are in
`.ufo/waves/round-41/build/R41PlanNext/` (listed in §9). The L1 holds the planner seat; this is data plus a draft (§6).

Axes named first (Godspeed): **A1** advertised-vs-demonstrated gap per surface (kill rate under the committed standing detector);
**A2** witnessability (a cheap command shows the mutant changes behaviour in a declared direction); **A3** counter cost (does the
round-41 counter machinery carry the surface); **A4** TB2 class distance from the seven graders read; **A5** offline executability
(nop/oracle run now); **A6** quote supply; **A7** prior-art clearance; **A8** do-nothing control red now. A1/A2/A5/A8 were executed;
A7 last.

## 0. Headline

1. **Calibration — price: 31 witnessed mutants over four tripwire tools, no tool edit, round-41 machinery reusable.** At tip, the 20
   round-40 wave-2 near-variants that survived battery40 still survive through the unedited round-40 counter
   (`MUTANTS total=20 killed=0 survived=20`, 21 fixtures, `exhibits=none` ×20; 14 of the 20 have a round-40 witness in a declared rc/class
   direction, 6 are text-only). Three further surfaces measured now: `state_check.py main()` (27 mutants, standing detector kills 9, **8 of
   the 18 survivors witnessed** by two fixture shapes, 4 unwitnessed), `round_close.py` (70 mutants, `--selftest` kills 40, **9 of the 30
   survivors rc-witnessed** by a 9-command set), `sources_adopt.py` library functions (109 mutants: selftest kills 74, a 46-command CLI set
   kills 21 more, 12 survive, 2 invalid). `mutant_direction_check.py` is **not recommended** (§2.5). Do-nothing control executed: red (§4).
2. **Coverage/novelty — pick `circuit-fibsqrt` (new class: agent-authored data artefact run by a grader-owned simulator, verdict from a
   28-row table) with a finding measured now**: a 1195-line lookup circuit for the grader's 28 inputs passes **3/3** while the instruction's own
   examples print `0` (`208:0 20000:0`); nop passes 2 of 3 (the shipped example `gates.txt` satisfies the existence and size tests); oracle 3/3 in
   27.8 s offline. No tracker item, no published instance (the only public statement I found says the opposite: an LLM audit, tier C, "hardcoding
   impractical"). Fallback with an existing 26-case pilot: `openssl-selfsigned-cert` (nop 0/6, oracle 5/6 on host OpenSSL 3.6.5). Refused:
   `schemelike-metacircular-eval` (gaming surface already published, #135/#235).
3. **Is any round-41 C2 finding unpublished? Yes, one: `input-crlf-rewrite`** — rewriting the three input calendars with CRLF (or bare CR, or
   one line only) passes the grader's integrity check although `instruction.md:17-18` says any modification fails; mechanism `read_text()`
   universal newlines at `test_outputs.py:90,93`. Not in PR #245 (it changes only the output reader `_r`, and its spec says "Do not change input
   integrity"), the grader blob on TB2.1 `main` is byte-identical to the pin, 0 tracker hits for CRLF/newline/integrity. Novelty candidate with
   limits (§3.4). The decoy finding is published (S124); the RFC-forms rejections are only adjacent to #245 (its fixtures expect them accepted).

## 1. Method and what was run

| piece | what | where |
|---|---|---|
| mutant harness | R40PlanNext's AST harness (`cmp`, `and/or`, `not`, `return n`, `SystemExit(n)`, `if→False`, int +1; result-difference kill; identity copy and baseline-stability checked) wrapped per surface by `run42.py` (detector sets, region limits) | `harness/` |
| kill = | `(rc, normalised stdout+stderr)` of ANY detector differs from the unmodified tool's (not an attributed kill; the counters are stricter) | |
| standing detector | what the lane commits: `--selftest` (+ `--summary` for state_check) | |
| witness detector | extra commands/fixtures a battery module could build; indices recorded per mutant in `res_*.json` `info` | |
| near-variants | `ctr/plan42_driver.py` = the **unedited** round-40 counter (sha `4d47800e…`, equal to the lane's) with `MUTANTS` swapped to the 30 wave-2 rows (`xmut_table.py` + `xmut_driver.py` from `F40XMutAnchor/`, `F40XMutLedgerOrder/`) | |

Tool pins at this tip equal the round-40 counter's: `sha256sum plans/anchor_digest_check.py plans/ledger_tip.py plans/order_check.py` →
`11bb2cad…`, `853bcb2a…`, `948d5e1d…`; `git log -3 -- <those>` stops at round-39 commits, i.e. unchanged since.

Scratch note: the whole `/fast/scratch/hyaku/kengaku-r41/` tree (every seat's dir) was removed once around 15:42 by something outside this seat; I re-cloned
and re-ran everything below it. All receipts were copied to the report dir immediately.

## 2. Candidate A — calibration

### 2.1 Surface table (all at `fc79f2a`; commands in §8)

| surface | mutants | standing detector kills | + witness-detector kills | survive | witnessed survivors | unwitnessed / limit |
|---|---|---|---|---|---|---|
| anchor+ledger+order near-variants (30, round-40 wave 2) through the frozen r40 counter | 30 | 10 (battery40) | – | **20** | 14 (X1 X3 X6 X7 X9 X12 X13 X14 X15 XO1 XO3 XO5 XO6 XO7; round-40 reports `wit/`, `wit-*.diff`) | 6 text-only (XL1–XL6: summary counters, `kind=`, REF AUDIT/BIND labels; counter `classes()` reads none of them) |
| `state_check.py main()` (L4649–4706) | 27 | 9 (`--selftest`, `--summary`) | 6 (6 error-path commands) | **12** | **8** (§2.3) | 4: L4694 `return 2` (check_all raises), L4701 ×2, L4703 (empty population) |
| `round_close.py` (whole file) | 70 | 40 (`--selftest`) | 10 (9 commands) | **20** | **9** rc-witnessed (§2.4) + 2 message-only (L164, L181: rc 2→2) | 9: L121 ×2, L144 `and→or`, L148, L179, L199, L200, L209, L291 |
| `sources_adopt.py` library fns (L1–609, `main`/selftest excluded) | 109 (2 of them invalid) | 74 (`--selftest`) | 21 (46 CLI commands) | **12** | not witnessed (guards: L87 ×2, L118, L120, L153, L156, L216, L222, L365, L430, L519, L542) | 2 invalid mutants (`not x→x` breaks the parenthesis) |
| `mutant_direction_check.py` | 28 of 70 (sample) | 19 | – | 9 | – | §2.5 |

Not re-measured: `tip_receipts.py` and the CLI half of `sources_adopt.py` (this round's C1 — wave-1 batteries are in flight; the clone has no
`plans/battery41`). The 12 sources-library survivors and the 21 CLI-only kills are for the planner to re-derive after battery41 lands (Q30): some of
the 21 may already be killed by battery41's fixtures.

### 2.2 The near-variant control, executed now

```
$ python3 ctr/plan42_driver.py --lane $S/lane --work $S/run40 --jobs 6            (30 rows, 34.6 s)
PINS total=3 mismatched=0
BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=30 killed=10 survived=20 invalid=0 null_detected=0
PINS-AFTER mismatched=0
$ python3 ctr/plan42_driver.py ... --only X1,X3,X6,X7,X9,X12,X13,X14,X15,XL1,XL2,XL3,XL4,XL5,XL6,XO1,XO3,XO5,XO6,XO7     (47.7 s)
MUTANTS total=20 killed=0 survived=20 invalid=0 null_detected=0       (grep -c exhibits=none → 20)
```
(`near-variants-r40-counter.txt`, `near40_survivors_only.txt`.) This reproduces round-40's `7/16` anchor and `3/14` ledger/order kills exactly
(anchor 7 of 16 + ledger/order 3 of 14 = 10 of 30). The counter is the round-40 one: its tool runs are **not** sandboxed (the round-40 host-write
vectors `R40CritC1Counter` A1/A2), so a round-42 list over these tools must be re-hosted in the round-41 sandboxed counter — see §2.6 cost.

### 2.3 `state_check.py main()` — two fixture shapes witness 8 of 12 survivors

27 mutants confined to `main()`. Standing `--selftest` + `--summary` kills 9; six error-path commands (nonexistent `--root`, `--root` a file, empty dir, four
empty lane files, `--json`, bare) kill 6 more. The remaining 12 survivors, tested against two trees built from the unmodified lane (`harness/wit_sc.py`):

| shape | how built | reference | witnessed mutants (ref→mut) |
|---|---|---|---|
| A: no seed fixture, no PROTOCOL.md above the root | `plans/` symlink tree without `fixtures/` | rc 2 `canonical PROTOCOL.md was not found` | L4680 `if protocol is None→False` (2→1 `AttributeError`), L4684 `return 2→0` (2→0), L4671 `==→!=` (2→1 `FileNotFoundError`) |
| B: seed fixture edited by one byte | tree with `shonen-seed.txt + "x"` | rc 2 `SHONEN seed fixture pin broken` | L4671 `if→False` (2→0), L4671 `==→!=` (2→0), L4676 `if→False` (2→0), L4676 `or→and` (2→0), L4679 `return 2→0` (2→0) |
| C: fleet PROTOCOL.md without the seed text above the root | `wdrift/PROTOCOL.md`, lane tree below | rc 2 pin-broken (drift) | L4675 `not in→in` (2→0) |

Four survive every command and fixture tried: L4694 (`check_all` raising `OSError/UnicodeError/ValueError/IndexError`; corrupting nine lane files
with invalid UTF-8 produced only `unreadable`/`mismatch`, never the raise), L4701 `if→False`, L4701 `0→1`, L4703 `return 2→0` (empty population: every
tried tree returns assertions, an empty-lane tree returns `VERDICT: FAIL`). Treat these four as unwitnessed limits, not mutants (O13 rule: no
witness, no freeze). Directions are exact exit pairs `2>0`/`2>1`, which the round-41 counter already models for `sources`. **Counter cost:** the tool
locates its fixture from `__file__`, so shapes A/B/C need the counter to place the tool inside a lane-shaped tree the fixture controls — new machinery.

### 2.4 `round_close.py` — 9 rc-witnessed survivors by a nine-command set

Prior art on the same tool: `F40RoundClose` priced 14 mutants (6 caught). Here 70, `--selftest` kills 40, 30 survive; nine extra commands
(`harness/wit_rc.py`, fixtures from the tool's own `build_fixture`) separate these (reference rc → mutant rc):

| mutant | command that separates it | rc |
|---|---|---|
| L97 `== 0→!= 0` and `0→1` (`git_ok`), L131 `or→and` | gate on a fixture whose receipt is committed but deleted from the work tree | 0→2 |
| L144 `if env_root and …→False` | `--round 39` with no `--census`, `SHOKUNIN_ROOT` set | 0→2 |
| L177 `if not order_path.is_file()→False` | gate on a fixture without `plans/order_check.py` | 2→1 |
| L310 `if census is None→False` | `--selftest --census /nonexistent` | 2→1 |
| L312 `return 2→0` | same | 2→0 |
| L313 `if not (lane/ORDER_TOOL).is_file()→False` | `--selftest --lane <empty dir>` | 2→1 |
| L315 `return 2→0` | same | 2→0 |

Message-only (rc 2→2, rc-equivalent; must NOT enter a rc direction list): L164, L181. Unwitnessed: L121 ×2 (rule (b) round filter), L144
`and→or`, L148 (parent-walk `is_file`), L179 (dead guard: `main()` already refuses a non-file census), L199 (`not` in stdout newline fix), L200/L209
(stderr echo), L291 (selftest failure dump). Counter cost: the census argv path lies outside the fixture dir, so a module must write a stub census
script into `d`; `SHOKUNIN_ROOT` (L144) needs an env hook the counter does not offer.
New defect measured on the way (no mutant needed): `python3 plans/round_close.py --lane . --selftest --census C --work DIR` run **twice on the same
DIR** exits with a `CalledProcessError` traceback (the second `git commit` finds nothing to commit; `round_close-selftest-second-run-traceback.txt`),
although `--work` is documented as "--selftest scratch parent". Round-40 routed item R3 (registry row for `round_close.py`) is the place to state it.

### 2.5 `mutant_direction_check.py` — measured, not recommended

28 of 70 mutants, standing detector = the committed tip run on `round38_c1_verify.py` (65 s per run; rc 1, the known N21 MISLABELLED): 19 killed, 9
survive (L71, L74, L79, L104, L114, L128, L138 ×2, L176). L79 and L138 sit in one of the tool's two redundant legs [INFERENCE: a guard one leg can lose while the other decides]; the real gaps are
L104/L114 (`return 2` setup refusals), L128 (INVALID row guard) and L176 (`or→and` in the exit-3 map). More important: the tool accepts only the
**round-38** list — `--counter plans/round39_c1_verify.py`, `round40_…`, `round41_…` each print `SETUP counter … is not a round-38-list counter` — so it
cannot see any list since round 38, and the round-41 counter attests every direction by witness itself. Mutating an orphaned tool prices a surface
nothing calls; if the planner wants it, the work is re-pointing it, not a mutant list.

### 2.6 Cost and ordering (data; [INFERENCE] from rounds 40–41 seat counts)

Proposed list size: **31** = anchor 9 + order 5 (14 directional near-variants, witnesses on record) + `state_check main()` 8 + `round_close` 9. Counter =
the round-41 counter with `TOOLS` extended by `anchor`, `order`, `statecheck`, `roundclose` (+ `ledger` if the six text-only rows are wanted: needs the
class-line reader, which the round-41 `receipts` classes already prototype) and `FLOORS` re-bound. Order by cost: (1) anchor/order near-variants — tools
unchanged, witnesses written, battery40's fixture shapes exist; (2) `round_close` — stub census, no tool-layout change; (3) `state_check` — needs the tool-tree
contract. A round-42 list that takes only (1)+(2) is 23 mutants and avoids the new tool-layout machinery. Seats: 1–2 counter, 4–5 battery writers, 1 witness
re-derivation, 1 critic. The sources-library residue (12) is not priced for freeze: re-measure after battery41.

## 3. Candidate B — coverage / novelty

### 3.1 Candidates, measured now (host python 3.14.8, host gcc/OpenSSL 3.6.5, not the task images)

Controls (`ctl.py`, `tb2-controls-nop-oracle.txt`; bwrap `--unshare-net`, grader test functions called in the sandbox, pin `2fd12b88`):

| task | nop | oracle (`solve.sh`) | quote supply tests/instr (R40 screen) | class vs the seven read | prior art (§3.3) |
|---|---|---|---|---|---|
| `circuit-fibsqrt` | **2/3** (`test_gates_file_exists`, `_size` pass on the shipped example) | 3/3 (grader 27.8 s) | 76 / 12 | **new**: data artefact executed by a grader-owned simulator, fixed 28-row table, max input 48401 | tracker 0 (tb2); tb2-1 4 hits = leaderboard submissions only |
| `openssl-selfsigned-cert` | 0/6 | **5/6** (`test_python_verification_script`: oracle splits on `"CN = "`, OpenSSL 3.6.5 prints `CN=`; limit as in round 39) | 90 / 22 | system-tool text substring checks over a generated PKI set | tracker 0; an LLM audit lists three gaps as theoretical |
| `schemelike-metacircular-eval` | 0/1 (2.6 s) | 1/1 (63 programs inside one test, 47.2 s) | 110 / 10 | differential grader | **published**: TB2.1 #135 (open), #235 (open) |

### 3.2 `circuit-fibsqrt` — finding measured now (`lookup_gates.py`, receipts in report dir)

The grader (`tests/test_outputs.py:55-147`, `test_sqrt_fib`) runs `sim` on 28 fixed values (`1,4,8,12,41,42,107,220,209,366` and `x², x²-1, x²+1` for six x), maximum 48401 =
220²+1, while the task states `fib(isqrt(N))%2^32` for a 32-bit N. `lookup_gates.py` writes a 1195-line `gates.txt` (32 held inputs, 32 NOTs, a 31-AND equality
chain per case, OR trees per output bit) that equals the table and nothing else:

```
$ ./sim 1 → 1 ; ./sim 209 → 377 ; ./sim 220 → 377 ; ./sim 48401 → 3361931507      (table rows, correct)
$ ./sim 208 → 0 ; ./sim 20000 → 0 ; ./sim 300 → 0 ; ./sim 1000000 → 0              (instruction.md examples 208→377, 20000→1407432322 fail)
grader in bwrap: T test_gates_file_exists PASS / T test_gates_file_size PASS / T test_sqrt_fib PASS → SUMMARY pass=3 fail=0 ; wc -l gates.txt → 1195
```
Both prior statements of the opposite exist: `terminal-bench-2-audit` (JonathanGabor, run 20260120) says "28 distinct test cases with varied inputs make hardcoding
impractical". The README names `208` and `20000` as example test cases though the grader table contains neither — a second documentation-vs-grader gap.
Limits: host gcc/python, not the image; the lookup circuit is a witness of the coverage gap, not an agent trajectory; whether the verifier's cwd makes `/app/sim`
the freshly compiled binary is unmeasured (`gcc … -o sim` writes to cwd, the grader runs `/app/sim`, `test.sh` runs from the Dockerfile `WORKDIR /app`).
Dry-table seeds (predictions before any run): nop (`FAIL` sqrt_fib only), oracle, lookup-28, lookup-27 (one row dropped → fail), lookup-28 plus the
two instruction examples, a 33-line gates.txt that passes existence/size, blank-line padding to 31999 lines (size test counts every line, `sim` ignores
non-gate lines), `out40000 = …` past `MAX_SIGNALS` (undefined behaviour: report only if deterministic).

### 3.3 Prior art (commands in §8)

* `gh api search/issues repo:harbor-framework/terminal-bench-2-1 circuit-fibsqrt` → 4, all `Leaderboard Submission` PRs (#44, #140, #206, #208);
  `…/terminal-bench-2` → 0; `…/terminal-bench` → 0. `openssl-selfsigned-cert`: 1 (leaderboard #44), 0, 0. `schemelike-metacircular-eval`: 5 incl. open #135 and #235,
  and `terminal-bench-2` #31 (Modal solution scripts).
* All three graders on TB2.1 `main` (`7131e437`) are byte-identical to the pin (`test_outputs.py` sha256 prefixes `6117b8ed`, `90970bb3`, `fbb84e3c`).
* `JonathanGabor/terminal-bench-2-audit/audit_results/20260120_125158/audit.txt` (tier C, LLM-written): for `openssl-selfsigned-cert` it names "a script could
  hardcode", "no explicit verification that the certificate is self-signed" and a PEM-match gap as theoretical; the round-39 pilot **measured** the three
  (`script-prints-literals-only`, `not-self-signed`, `key-cert-mismatch` all 6/6) — measured vs asserted, not first mention. For `circuit-fibsqrt` it asserts the opposite of §3.2.
* `schemelike`: #235 body states the verifier runs the participant-writable `interp.py`; #135 documents special-casing the path. Little novelty left.

### 3.4 Is any round-41 C2 finding unpublished? (the novelty candidate)

| round-41 receipt case | status | evidence |
|---|---|---|
| `decoy-first-vevent` (tests 2–3 read the first `DTSTART`) | **published** | TB2.1 PR #245 (S124), closed unmerged 2026-10-08 |
| `decoy-second-vevent` | published (same defect, mirror) | PR #245's order fixtures |
| `folded-attendee-line`, `lowercase-property-names`, `dtstart-value-datetime` fail; `crlf-line-endings` passes | adjacent only | PR #245's repaired parser lists CRLF/folded/case-insensitive/`VALUE=DATE-TIME` as accepted syntax (`pr245-test_outputs-and-spec.patch`), but the PR never reports the original's rejections |
| `bob-start-0900-wed`, `wed-1059-overlaps-alice` pass the earliest test (`PFP`) | by design (test 2 owns validity) | not a defect; an observation about test independence |
| **`input-crlf-rewrite`** (`PPP` with all three inputs rewritten) | **unpublished** | below |

Mechanism (`corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py:90-96`): `app_text = (Path("/app")/fname).read_text()` is compared with
`repo_path.read_text()` or hashed as `app_text.encode()`; `read_text()` applies universal newlines, so `\r\n` and bare `\r` become `\n` before either comparison.
`instruction.md:17-18`: "Any modification will cause the tests to fail." Measured now beyond the frozen receipt (`crlf_probe.py`, host python 3.14.8, same
`/cap/test_outputs.py`; inputs are LF-only; slot = the oracle's, tests `P/F` per test 1–3):

```
identity PPP | crlf-all PPP | bare-cr-all PPP | crlf-first-line-only PPP | trailing-space FPP | append-nl FPP | utf8-bom FPP
```
So newline-convention rewrites (including a bare-CR file no line-based parser reads as lines) pass; any other byte change fails. Clearance: `gh api search/issues`
on `terminal-bench-2-1` for `universal newlines`, `CRLF integrity`, `read_text newline` → 0 each; `constraints-scheduling` → 3 (#245 + two leaderboard PRs);
`gh api commits?path=tasks/constraints-scheduling` on TB2.1 `main` → one commit (2026-05-05, a directory move); TB2.1 `main` `test_outputs.py` sha256 `1422b345…` = the pin;
HF `zai-org/terminal-bench-2-verified` copy has the same `read_text()` lines (L90, L93, L95); PR #245 changes `_r` to `open(newline="")` for **output** reads only and its
SPECIFICATION says "Do not change input integrity". A web summary returned by the search tool claimed CRLF edits "can fail the Input modified assertion"; the receipt
and the probe above contradict it (the claim is unsourced). Limits: GitHub issue search and HF copies only (no Harbor hub, no mailing lists); absence of hits is
search-index evidence, not proof; the probe calls the test functions, not `test.sh`; the entry may state it only as a probed instance, and "novel" only with a dated
search receipt (the claims file's own "no novelty claimed" stance should change only if the planner funds a prior-art seat).

## 4. Do-nothing controls (each must be red)

| candidate | control | executed now | result |
|---|---|---|---|
| calibration (any new list) | counter with no `plans/battery42` → `BATTERY fixtures=0`, `killed=0`, exit 1 (the round-41 `control-c1-nothing.txt` shape) | stand-in: the 20 survivors through the unedited r40 counter with battery40 present | `MUTANTS total=20 killed=0 survived=20 … PREDICATE C1 n/a` (§2.2) |
| calibration, standing detectors as the "before" | what the lane commits today | `state_check main()` 9/27 killed; `round_close` 40/70; `sources_adopt` library 74/109 (2 invalid) | not killed: 18 / 30 / 33 → red |
| calibration, non-vacuity | the round-41 `control-c1-no-mutants` + `TOTAL`/`FLOORS` binding must carry over | not re-run (round-41 artefact) | must be re-shown on the round-42 counter |
| coverage (`circuit-fibsqrt` C2) | the counter with the receipt, rows and entry absent → gate `P10 receipt unreadable`, `V2 V3 V4 V7` red, `PREDICATE C2 fail`, exit 1 | stand-in: the round-41 C2 counter at the wave-1 tip, before its entry lands: `checks=8 defects=4` (V2 spec/gate, V3 rows, V4, V7), `PREDICATE C2 fail`, rc 1 (`c2-r41-counter-at-wave1-tip.txt`; V8 reads `order_exit=0 result=PASS` — receipt committed after the claims) | red |
| novelty (CRLF or lookup finding) | the entry's novelty sentence without a dated prior-art search receipt | not executable until a counter exists | the counter should red on `novel`/`unpublished` wording with no search receipt line (planner's call) |

## 5. Axis recommendation (data, the planner decides)

Carried axes (round-41 claims): calibration 8, coverage 7 (L0-capped by `kengaku | round-33`), novelty 7, depth 9, operability 8, freshness 8, adjacency 8.

| candidate | gap measured now | witnessed | prior art | do-nothing | cost |
|---|---|---|---|---|---|
| C1 anchor/order near-variants (14) | 20/30 survive the unedited counter | 14 (round 40) | none needed | red (20/0) | re-host in the sandboxed counter + ≈10 fixtures |
| C1 `round_close` (9) | 30/70 survive `--selftest` | 9 rc | `F40RoundClose` priced 14 | red by construction | stub census; no tool-layout change |
| C1 `state_check main()` (8) | 18/27 survive standing | 8 | none | red by construction | tool-tree contract in the counter |
| C2 `circuit-fibsqrt` | 3/3 for a 28-row lookup | n/a | none found | `V2 V3 V4 V7` red | spec/gate/counter per round 41 + dry table ≈20 cases |
| novelty rider (CRLF input rewrite) | 4 rewrites pass | probe in §3.4 | none found | needs a search-receipt rule | one prior-art seat + one probe case already in the receipt |

## 6. DRAFT — `### Planned (round 42)` (paste-ready for `SCORECARD.md`)

```markdown
### Planned (round 42)

- **Calibration (8):** mutation-test the next undemonstrated tripwire surface, 31 frozen mutants over four unedited tools: the 14 directional
  near-variants of `plans/anchor_digest_check.py` (X1 X3 X6 X7 X9 X12 X13 X14 X15) and `plans/order_check.py` (XO1 XO3 XO5 XO6 XO7) that survived
  battery40 (re-measured at `fc79f2a` through the unedited round-40 counter: 30 rows, `killed=10 survived=20`, the 20 survivors `killed=0`; round-40
  witnesses `F40XMutAnchor`, `F40XMutLedgerOrder`), the 8 witnessed `main()` exit-2 survivors of `plans/state_check.py` (two fixture shapes: no seed fixture,
  one-byte-edited seed fixture, plus a fleet-drift tree; 12 of 27 `main()` mutants survive the standing detector plus six error-path commands, 4 stay
  unwitnessed and are limits), and the 9 rc-witnessed survivors of `plans/round_close.py` (70 mutants, `--selftest` kills 40; exit pairs `0>2`, `2>1`,
  `2>0`; L164/L181 are rc-equivalent and stay out). The six text-only ledger variants (XL1–XL6) are carried as a limit unless the counter reads
  summary/`kind=`/REF labels. Counter `plans/round42_c1_verify.py` = the round-41 sandboxed counter with `TOOLS` extended and `FLOORS`/`TOTAL` re-bound
  (the round-40 counter's tool runs are unsandboxed: not reused). Witnesses re-derived on the landed bytes before freeze (Q29, Q30). Predicate:
  `MUTANTS total=31 killed=31 survived=0 invalid=0 null_detected=0`, per-tool floors, `PREDICATE C1 pass`. Before (do-nothing control): no
  `plans/battery42` → `killed=0 survived=31`; plus the carried `control-c1-no-mutants` shape. Kill rule as round 41. `mutant_direction_check.py` is not
  mutated: it loads only the round-38 list (`SETUP … not a round-38-list counter` for rounds 39–41).
- **Coverage (7, capped by the open L0 question `kengaku | round-33`) and novelty (7):** TB2 `circuit-fibsqrt` @ `2fd12b88` — a data artefact run by a grader-owned
  simulator and scored on a fixed 28-row table (rows S125 `tests/test_outputs.py` sha256 `6117b8ed…`, S126 `instruction.md` sha256 `a7f50026…`, S127 `tests/sim.c`
  sha256 `700645ac…`, ids re-derived at freeze; tier B row for any published statement found by the prior-art seat). Executed controls at plan time: oracle 3/3
  (27.8 s, `--unshare-net`), nop 2/3 (the shipped example `gates.txt` satisfies the existence and size tests), a 1195-line lookup circuit for the grader's 28
  inputs passes 3/3 while the instruction's own examples print 0 (`208→0`, `20000→0`). Dry table written and frozen before the first recorded probe run
  (`plans/order_check.py`, V8). Prior art cleared by search: tracker 0 (`terminal-bench-2`, `terminal-bench`), 4 leaderboard-only hits on TB2.1; an LLM audit
  asserts the opposite ("hardcoding impractical"). Fallback: `openssl-selfsigned-cert` (26-case round-39 pilot, oracle 5/6 on host OpenSSL 3.6.5, version limit declared).
  Refused: `schemelike-metacircular-eval` (TB2.1 #135/#235 publish its gaming surface).
- **Novelty rider (one claim, not scored unless cleared):** round-41 C2's unpublished case `input-crlf-rewrite` (all three input calendars rewritten with CRLF
  pass 3/3 although `instruction.md:17-18` says any modification fails; `read_text()` universal newlines at `test_outputs.py:90,93`). Measured beyond the receipt:
  CRLF, bare CR and one-line CRLF pass; a trailing space, an appended newline and a BOM fail. TB2.1 PR #245 changes only the output reader and leaves input
  integrity untouched; 0 tracker hits. Requires a dated prior-art receipt before the word "novel" appears in the entry.
- **Carried / routed:** `round_close.py --selftest --work DIR` crashes with a `CalledProcessError` traceback on a second run in the same DIR (registry row, R3);
  sources-adopt library survivors (12 after selftest + a 46-command CLI set) re-measured after battery41 lands; `tip_receipts.py` six `F40TipReceipts` defects unchanged.
```

## 7. Limits

* Result-difference kills, not attributed kills; survivors are not proven non-equivalent (hand classification marked). `state_check` L4694/L4701/L4703 are "no witness
  found", not proven dead. The 46-command sources CLI set and the 9-command round_close set are my witnesses, not a frozen battery.
* The round-40 counter ran inside the host-safety envelope but is unsandboxed internally; the numbers are valid, the reuse is not recommended.
* TB2 controls ran on host python 3.14.8, host gcc and OpenSSL 3.6.5, not the images (not pulled); `test.sh` needs network and was not run. The `circuit-fibsqrt`
  lookup circuit is a coverage witness, not an observed agent.
* Prior-art clearance is GitHub issue/PR search, TB2.1 `main` and HF copies, one LLM-audit repo; absence of hits is search-index evidence only. `gh` search results
  are `total_count` values, not read item by item except #245 and #135/#235.
* Host load average 10–20 during runs; no timing is comparable to a quiet host. `/fast/scratch/hyaku/kengaku-r41/` was wiped once by another party (see §1).

## 8. Evidence ledger

| claim | command | output |
|---|---|---|
| lane HEAD | `git -C $S/lane rev-parse HEAD` | `fc79f2a49be0221e138b3885fa0d83bc43b31a42` |
| tool pins | `sha256sum plans/{anchor_digest_check,ledger_tip,order_check}.py` | `11bb2cad…`, `853bcb2a…`, `948d5e1d…` |
| r40 counter unedited | `sha256sum $S/ctr/round40_c1_verify.py plans/round40_c1_verify.py` | both `4d47800e3551a0c7a39217987f436ffad9d69663d5f0efc840717edfcbd4642c` |
| near-variants, 30 rows | `bwrap … python3 ctr/plan42_driver.py --lane $S/lane --work $S/run40 --jobs 6` | `MUTANTS total=30 killed=10 survived=20 invalid=0 null_detected=0` |
| near-variants, the 20 survivors | same, `--only X1,X3,…,XO7` | `MUTANTS total=20 killed=0 survived=20`; `grep -c exhibits=none` → 20 |
| state_check main | `python3 run42.py state_main --lane $S/lane … --jobs 6` | `{"killed": 15, "survived": 12}` of 27, `BASE-STABLE True`, `IDENTITY-COPY-EQUALS-BASE True` |
| state_check witnesses | `python3 harness/wit_sc.py` (+ drift tree) | REF `(2,'…PROTOCOL.md was not found')`, `(2,'…pin broken')`; 7 DIFF lines + L4675 DIFF; L4694/L4701/L4703 `same` |
| round_close | `python3 run42.py round_close …` (after dropping `--work`: the 1st run was unstable because `--selftest --work` crashes on reuse) | `{"survived": 20, "killed": 50}` of 70, `BASE-STABLE True` |
| round_close witnesses | `python3 harness/wit_rc.py` | REF rc table; 9 mutants with a `0>2`/`2>1`/`2>0` pair, L164/L181 `2>2`, 9 `UNWITNESSED` |
| round_close second-run crash | `round_close.py --lane L --census C --selftest --work $S/w` ×2 | run 1 `SELFTEST checks=5 ok=5 failed=0`; run 2 `CalledProcessError … 'commit' … status 1` |
| sources library | `python3 run42.py sources_lib …` (46 detector commands; ids `S010/S011/S002/S099`) | `{"killed": 95, "survived": 12, "invalid": 2}` of 109; 74 by selftest, 21 CLI-only |
| mutant_direction_check | `python3 run42.py mdc … --sample 28 --seed 41 --jobs 4` | `{"killed": 19, "survived": 9}`; base rc 1 (N21); other counters `SETUP … is not a round-38-list counter` |
| TB2 pin | `git -C tb2 rev-parse HEAD` | `2fd12b88aafdd04a52c298e3940bcb189f9766d6` |
| nop/oracle | `python3 ctl.py` | openssl nop `pass=0 fail=6`, oracle `pass=5 fail=1`; fibsqrt nop `pass=2 fail=1`, oracle `pass=3 fail=0` (27.8 s); schemelike nop `pass=0 fail=1`, oracle `pass=1 fail=0` (47.2 s) |
| lookup circuit | `python3 lookup_gates.py lk/gates.txt` ; grader in bwrap | `lines 1195 cases 28`; `SUMMARY pass=3 fail=0`; `208:0 20000:0 48402:0` |
| CRLF probe | `python3 crlf_probe.py` | `identity PPP, crlf-all PPP, bare-cr-all PPP, crlf-first-line-only PPP, trailing-space FPP, append-nl FPP, utf8-bom FPP` |
| PR #245 | `gh api repos/harbor-framework/terminal-bench-2-1/pulls/245` (+`/files`) | closed, `merged=false`, 2026-10-08, files `SPECIFICATION.md`, `tests/test.sh`, `test_event_binding_adversarial.py`, `test_outputs.py`; patch changes `_r` to `open(newline="")`, integrity block unchanged |
| TB2.1 grader at main | `gh api …/contents/tasks/constraints-scheduling/tests/test_outputs.py` | sha256 `1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1` = pin; `commits?path=…` → 1 commit (5fc7d3b9) |
| issue search | `gh api -X GET search/issues -f q='repo:harbor-framework/terminal-bench-2-1 <term>'` | circuit-fibsqrt 4 (leaderboard), openssl-selfsigned-cert 1 (leaderboard), schemelike 5 (#235 #135 + 3 leaderboard), `universal newlines`/`CRLF integrity`/`read_text newline` 0 |
| round-41 C2 counter at wave-1 tip | `python3 plans/round41_c2_verify.py --lane $S/lane --work $S/c2w/x` | `checks=8 defects=4` (V2 V3 V4 V7), `PREDICATE C2 fail`, rc 1 |
| source shas | `sha256sum tb2/circuit-fibsqrt/{tests/test_outputs.py,instruction.md,tests/sim.c}` | `6117b8ed…`, `a7f50026…`, `700645ac…` |

## 9. Tools, scope, scratch

No tool installed (bwrap, gcc, openssl, gh, git, python3 present; pytest absent — graders were driven by calling their test functions, as in rounds 36–41). No pacman use.
Writes: this report and `.ufo/waves/round-41/build/R41PlanNext/` (`harness/` = `run42.py`, `wit_sc.py`, `wit_rc.py`, `ctl.py`, `plan42_driver.py`;
`res_*.json`, `run_*.txt`, `near-variants-r40-counter.txt`, `near40_survivors_only.txt`, `tb2-controls-nop-oracle.txt`, `lookup_gates.py`, `crlf_probe.py`,
`crlf_probe_out.txt`, `pr245-test_outputs-and-spec.patch`, `prior-art-tb21-main.txt`, `c2-r41-counter-at-wave1-tip.txt`,
`round_close-selftest-second-run-traceback.txt`). The lane tree, claims, tools, counters, probe, spec, gate, dry table, captures, receipt and
`.ufo/waves/round-41/claims/` were read, not written; no git add/commit in the lane; `shokuknow` untouched; no subagents. Scratch
`/fast/scratch/hyaku/kengaku-r41/R41PlanNext/` removed at the end.

VERDICT: plan42-drafted
