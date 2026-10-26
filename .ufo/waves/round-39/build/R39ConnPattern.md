# R39ConnPattern — cross-claim pattern finding (kengaku round 39, wave 1)

Seat: R39ConnPattern (connector, leaf). Date: 2026-10-26.
Scope: the six lane tools named in the assignment — `plans/round39_c1_verify.py`,
`plans/round39_c2_verify.py`, `plans/git_leak_probe.py`, `plans/anchor_digest_check.py`,
`plans/ledger_tip.py`, `plans/tip_receipts.py` — read in full (395/282/301/534/229/355 lines).
Nothing in the lane was edited; all probes below are read-only inspections of the lane tip
`b2bdd425fbc042d3075994dae60fe88a51e277ab` plus throwaway Python one-liners.

## The two source pattern sets

**Grader-side (TB2 `git-leak-recovery`, capture `corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py`):**
- *dangling tips only, not interiors* — `test_no_secrets_in_unreachable_objects` loops over
  `git fsck --lost-found` lines containing "dangling" and `cat-file -p`s each (test_outputs.py:68-86);
  a dangling commit's tree/blob interior is never inspected.
- *skips dot paths* — the checksum runs `find /app/repo -type f -not -path '*/\.*'` (test_outputs.py:89-92).
- *`--all` never sees unreferenced objects* — the two leak greps are `git log --all --grep/--format` and
  `git log --all -p -S` (test_outputs.py:32-56); nothing reads refs/config/reflog.
- Receipt confirms all three shapes live: `cases=25 observed_pass=13 observed_fail=12 mismatches=0`
  (corpus/evidence/round39/git-leak-probe.txt, summary line); e.g. `echo-reflog-expire ... PPPPP`,
  `dotfile-in-worktree ... PPPPP`, `config-secret ... PPPPP`.

**Gate-side (frozen MUTANTS table, plans/round39_c1_verify.py:112-156):** the four survivors are
first-item-only (M02 P1 `list(pins.items())[:1]`, :121), off-by-one (M03 P3 `hi + 1`, :127),
loosened compare (M04 P7 `(prov.get(sid) or [""])[0]`, :133), and the D5 markup-stripping accept path
(M07) that no battery exercises — "pass side never exercised".

## Findings — sites carrying the shapes, with one-line exposure fixtures

### Shape: checks only the first/tip item — 3 sites (1 live, 1 binding, 1 reporting)

**S1 (live) — `plans/tip_receipts.py:113-123` `usage_argv`: the re-run command is the FIRST docstring
line matching `python3 `/`uv run ` + basename; every other advertised mode is silently never resolved.**
This shape is live today: `plans/git_webserver_probe.py:4-6` and `plans/build_pmars_probe.py:4-6` each
advertise three modes (`--lane .`, `--dry`, `--smoke`); the round-37/round-38 receipts re-run correctly
only because line 1 happens to be the full mode — nothing ties the resolution to the receipt's content.
*Fixture:* in a scratch clone, insert above `plans/build_pmars_probe.py:4` the line
`  python3 plans/build_pmars_probe.py --lane . --dry    print the frozen case table only (no sandbox)`,
then `python3 plans/tip_receipts.py --lane <clone>` — the healthy round-38 receipt reports `differ`
(the --dry table is not the receipt). False red keyed to docstring order, not receipt bytes.

**S2 (binding) — `plans/anchor_digest_check.py:252` `cap = cands[0]`: a PROVENANCE.md table line that
ticks several committed files binds only the FIRST resolvable tick as that sid's capture** (block
:242-255; every sid on the line shares it). The docstring's Binding section discloses "a filename that
resolves beside it" but not first-of-many. A row whose true subject is capture B can be scoped to
capture A by tick order, reopening the round-37 M4b/M5 cross-substitution shape
(`F37A-1`, `.ufo/waves/round-37/falsify/F37AnchorRerun.md` §4) through provenance ordering.
*Fixture:* in a scratch clone, give a committed PROVENANCE.md line
`| S200 | ... | [setup.sh](setup.sh) [test_outputs.py](test_outputs.py) |` where S200's SOURCES row names
test_outputs.py and carries its true digest → S200 is judged `digest-wrong-capture`; deleting the first
tick clears it.

**S3 (reporting) — `plans/round39_c1_verify.py:261-262`: the PINS check itself is complete
(`mism = [rel for rel, dig in PINS.items() if sha256(...)]`), but the receipt names only
`first={mism[0]}` when several of the 26 pins mismatch.**
*Fixture:* in a scratch clone, touch two pinned files (`plans/battery37/d4.py`, `plans/battery37/p5.py`)
→ exit 1 with only the first named; an integrator who fixes only the named pin stays red next run.
Reporting-only; the count `mismatched=2` is printed.

Reporting-only truncations of the same family (listed for completeness, no fixture needed):
`tip_receipts.py:149` (`script_hits[0]+receipt_hits[0]` provenance display), `anchor_digest_check.py:336,338`
(first locator named in unbound reasons), `round39_c1_verify.py:365-368` (the mutant loop `break`s at the
first killing fixture, so a killed mutant's `exhibits=` lists only directions seen before the kill;
survivors report complete sets).

### Shape: skips hidden files — 0 sites (verified, not assumed)

- `round39_c1_verify.py:191` `sorted(bdir.glob("*.py"))` — pathlib on this host matches dotfiles:
  `python3 -c` experiment on Python 3.14.8: `glob('*.py')` over a dir containing `.hidden.py`, `vis.py`
  returned `['.hidden.py', 'vis.py']`. A hidden battery39 module would be built and counted, not skipped.
- `tip_receipts.py:97-100` — population is `git ls-tree -r HEAD --name-only corpus/evidence` (git lists
  dot paths), filtered by `CANDIDATE_RE.search(basename)` with an unanchored `probe.*\.(txt|log)$`
  (IGNORECASE): a committed `.probe-x.txt` matches and is enumerated (as a boundary/skip line if unmapped —
  nothing is dropped silently).
- `anchor_digest_check.py:154-162` — `ls-tree HEAD` / `ls-files --cached` both list dotfiles.
- The grader's dot-skip lives in the *capture* (`find -not -path '*/\.*'`, test_outputs.py:89-92) and is
  carried by the probe as *case data* (`git_leak_probe.py:134-135`, case `dotfile-in-worktree`), not as a
  shape of any lane tool.

### Shape: reads only referenced state — 0 defect sites (all by contract, each with a documented escape)

- `anchor_digest_check.py:154-171` reads `HEAD:` blobs only (or `:path` index blobs via
  `--evidence-ref index`, :162) — deliberate: anchor claims must resolve to committed evidence
  ("a receipt is evidence only if something here re-runs it"). Note the intended asymmetry: rows are read
  from the working tree (`parse_rows`, :349-363) but bound to committed bytes.
- `tip_receipts.py:97-104` — receipts enumerated and byte-read at HEAD (`git show HEAD:<rel>`);
  uncommitted receipts are out of population by definition ("committed probe receipts", docstring).
- `ledger_tip.py:78-86` — refuses a dirty clone; every check runs on HEAD bytes of a fresh shared clone.
- Synthesis (the non-obvious half of the answer): no lane tool reads git object-store *interiors* — no
  reflog walks, no `fsck`, no `cat-file` of unreachable objects. The lane's whole verification surface is
  refs + worktree + HEAD blobs. The dangling-tip/interior blind spot is exactly the TB2 grader's class,
  and the lane covers it only observationally through `git_leak_probe.py` cases (`:105-107` dangling
  commit tip whose tree/blob stay secret-clean; `:121-123` ref-pinned blob; `:138-139` `.git/config`).

### Gate-survivor family echoes under the frozen inputs (latent, not defects) — 3 sites

**E1 — "pass side never exercised": `plans/round39_c1_verify.py:237-238`, the `error` arm of `exhibits`
is unreachable** — no frozen mutant carries `direction == "error"` (docstring :38 says so itself:
"(MAIN, round-38 rule, unused by this list)"). The arm cannot fire at landing.

**E2 — "pass side never exercised": `plans/round39_c2_verify.py:173,186-188`, V4's
`unnamed = [c for c in no if ...]` branch is dead under the frozen receipt** — the receipt's
`mismatches=0` makes `no == []`, so "mismatch cases not named in the entry" can never fire at landing;
it binds only on a future receipt carrying `match=NO`.

**E3 — "loosened compare" (M04-parallel): `plans/round39_c2_verify.py:186`, V4 tests naming as
containment `f"`{c}`" not in entry` over the whole entry text** — a case id backticked anywhere (even an
unrelated prose enumeration) satisfies "named in the entry"; a structured location check (e.g., inside the
mismatch-report paragraph) would be the strict form. Latent for the same reason as E2.

## Connector proposal (one bounded move, for wave 2 — neither tool is frozen)

`tip_receipts.py` and `anchor_digest_check.py` are not in the freeze list (only the gate, both counters,
the probe, the specs, the tables/captures/receipt, and the C1 PINS files are). One proposal with two
sibling edits, improving operability + calibration and harming none:

1. `tip_receipts.py` — resolve each receipt's re-run command from the receipt's own header/mode (or pin
   the mode per RECEIPTS row) instead of the first matching docstring line; today green only by line order
   (S1). Kills the false-red generator without touching any receipt.
2. `anchor_digest_check.py` — in the PROVENANCE route, union the digest sets of ALL resolvable ticks on a
   line (or disclose first-wins in the Binding section); closes the M4b/M5 re-entry through tick order (S2).

Both edits are drafts for the L1/wave-2 executors; this seat edited nothing.

## Evidence appendix (commands and outputs)

- `grep -E '^cases=' corpus/evidence/round39/git-leak-probe.txt` →
  `cases=25 observed_pass=13 observed_fail=12 mismatches=0` (matches the frozen claim).
- `python3 --version` → `Python 3.14.8`; dotfile-glob experiment → `glob('*.py') -> ['.hidden.py', 'vis.py']`.
- `grep -nE '^\s*(python3 |uv run ).*<probe>' plans/{tb2_grader_probe,regex_log_probe,git_webserver_probe,build_pmars_probe}.py`
  → tb2: 1 line; regex_log: 1 line; git_webserver: 3 lines (4-6); build_pmars: 3 lines (4-6) — the S1 shape is live.
- `head -3 corpus/evidence/round37/git-webserver-probe.txt` and
  `head -3 corpus/evidence/round38/build-pmars-probe.txt` → both carry full-run `# capture ... sha256` headers,
  consistent with the first-mode re-run being the correct one today.
- `head -3 corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py` → canary GUID; the three grader
  shapes quoted at file:line above.

VERDICT: pattern-6-sites (3 first-item: tip_receipts.py:113-123 live, anchor_digest_check.py:252 binding, round39_c1_verify.py:262 reporting; 0 hidden-file-skip; 0 referenced-state defects; 3 latent gate-survivor echoes round39_c1_verify.py:237-238, round39_c2_verify.py:186-188 — dead/loosened arms under frozen inputs)
