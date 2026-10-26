# R41BatRcvMap — battery41 module `r_map` (C1 mutants T09–T12)

Seat: executor, kengaku round 41 (hyaku run 9), wave 1. Scope: one battery41 module that kills frozen
`tip_receipts.py` mutants T09, T10, T11, T12 of `plans/round41_c1_verify.py` in their declared `silence`
directions. Nothing frozen was read-modified: the two tools, the two counters, the probe, the spec, the gate, the
dry table, the captures, the receipt and `.ufo/waves/round-41/claims/` are untouched (`PINS total=2 mismatched=0`
and `PINS-AFTER mismatched=0` in every run below). I wrote no lane file: the real lane has no `plans/battery41`
(`ls: cannot access '…/kengaku-shokunin/plans/battery41': No such file or directory`), and the module lives only in
this seat's build dir.

## Axes and moves taken

Axes: *calibration* (do the four mutants die attributably, in the declared direction, on the declared class) and
*operability* (does the module behave under the counter's real envelope, deterministically, without touching the
host). Moves kept, each cheap and harm-free: (1) all fixtures in `--list` mode, so every one is `expect=accept`,
exit 0, no probe ever runs and no receipt is written; (2) lane-shaped trees (README, SKILL, `corpus/README.md`,
`corpus/evidence/<round>/…`, several `plans/*.py` stubs with `Run as:` docstrings, one commit) instead of the
witness's two-file trees; (3) a second class-matched shape for T10 and T12 after measuring that a differently
shaped same-branch fixture does **not** attribute (see *Limits*).

## Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/build/R41BatRcvMap/battery/r_map.py`
— stdlib only, 159 lines, every `fid` starts `r_map-`:

```
$ sha256sum …/build/R41BatRcvMap/battery/r_map.py
705a4b7cbd3e08d620a4295acb147fa4d1741df5223ca95a7aaf456a8606c9c0  …/battery/r_map.py
```

Independent side-channel scan of the module source (the counter's own token tuple, lower-cased):

```
$ python3 - <<'EOF' … toks = ("/proc","ppid","cmdline","psutil","environ","fsmonitor","hookspath","filter.", \
    "gitattributes","core.","alias.","setsid","daemon","fork","nohup","socket","/home/",".local","__file__", \
    "inspect","importlib","sys.path","ctypes","chmod"); print([x for x in toks if x in text.lower()])
sidechannel_tokens []
```

The counter agrees: `sidechannel=0` in every run below. The module does not import, copy or read
`claims/witness/w_receipts.py` (read once, by hand, only to learn which branches are reachable); it defines its own
tree builders and its own stub generator, and no witness builder body is reused.

## Fixtures (10; one line each = what it demonstrates)

All `tool=receipts`, `expect=accept` (exit 0), `defects` = the exact class set the unmodified tool prints.

| fid | tree shape / behaviour | declared defects | kills |
|---|---|---|---|
| `r_map-t09-shared-stem-separators` | `foo-probe.txt` beside `plans/foo_probe.py` **and** `plans/foo.probe.py` (two hits on stem `fooprobe`) → unmapped; extra unrelated script and a non-receipt evidence file | `skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command` | T09 |
| `r_map-t09-shared-stem-case-fold` | same receipt; the second hit comes from case folding (`plans/FooProbe.py`) | same | T09 |
| `r_map-t10-derived-mapping` | `foo-probe.txt` ↔ `plans/foo_probe.py` differ only in separators → derived mapping, in a tree with an unrelated script and a non-receipt evidence file | `map:corpus/evidence/r/foo-probe.txt:derived` | T10 |
| `r_map-t10-derived-with-table-sibling` | derived receipt beside a RECEIPTS-table receipt (`round36/regex-log-probe.txt`), both classified in one pass | `map:…/r/foo-probe.txt:derived`, `map:…/round36/regex-log-probe.txt:table` | T10 |
| `r_map-t10-derived-deep-layout` | same derivation from a receipt nested two levels down: `corpus/evidence/round41/scheduling/foo-probe.txt` | `map:corpus/evidence/round41/scheduling/foo-probe.txt:derived` | — (same branch, other path; see Limits) |
| `r_map-t11-table-overrides-derived` | `round35/tb2-grader-probe.txt` and `round38/build-pmars-probe.txt`: both are table rows **and** both would derive; the table is an override list | `map:…/round35/tb2-grader-probe.txt:table`, `map:…/round38/build-pmars-probe.txt:table` | T11 |
| `r_map-t11-table-near-stem-decoy` | table receipt beside a `plans/tb2_grader_probe_v2.py` near-stem script (stem `tb2graderprobev2`, not the match) | `map:corpus/evidence/round35/tb2-grader-probe.txt:table` | T11 |
| `r_map-t12-log-population` | `corpus/evidence/r/foo-probe.log` with no matching script → population member, unmapped | `skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command` | T12 |
| `r_map-t12-log-with-table-sibling` | same `.log` beside a table receipt and a `_v2` near-stem script; `.log` is in the population regardless of mapping | `skip:…/r/foo-probe.log:no-committed-re-run-command`, `map:…/round36/regex-log-probe.txt:table` | T12 |
| `r_map-t12-log-derived` | same `.log` receipt with `plans/foo_probe.py` present, so the population entry maps | `map:corpus/evidence/r/foo-probe.log:derived` | — (same branch, mapped shape; see Limits) |

The two fixed paths the frozen class strings name (`corpus/evidence/r/foo-probe.txt`, `.log`;
`corpus/evidence/round35/tb2-grader-probe.txt`) are used verbatim; everything else is mine.

## Dev-mode proof (inside the mandatory envelope)

```
$ export TMPDIR=/fast/scratch/hyaku/kengaku-r41/R41BatRcvMap
$ bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
    --proc /proc --unshare-pid --die-with-parent \
    python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py \
    --lane "$S/lane" --battery-dir …/build/R41BatRcvMap/battery --only T09,T10,T11,T12 --work "$S/w" ; echo rc=$?
PINS total=2 mismatched=0
FIXTURE r_map-t09-shared-stem-separators tool=receipts expect=accept declared=skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command observed_rc=0 observed=skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command ok
FIXTURE r_map-t09-shared-stem-case-fold tool=receipts expect=accept declared=skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command observed_rc=0 observed=skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command ok
FIXTURE r_map-t10-derived-mapping tool=receipts expect=accept declared=map:corpus/evidence/r/foo-probe.txt:derived observed_rc=0 observed=map:corpus/evidence/r/foo-probe.txt:derived ok
FIXTURE r_map-t10-derived-with-table-sibling tool=receipts expect=accept declared=map:corpus/evidence/r/foo-probe.txt:derived,map:corpus/evidence/round36/regex-log-probe.txt:table observed_rc=0 observed=map:corpus/evidence/r/foo-probe.txt:derived,map:corpus/evidence/round36/regex-log-probe.txt:table ok
FIXTURE r_map-t10-derived-deep-layout tool=receipts expect=accept declared=map:corpus/evidence/round41/scheduling/foo-probe.txt:derived observed_rc=0 observed=map:corpus/evidence/round41/scheduling/foo-probe.txt:derived ok
FIXTURE r_map-t11-table-overrides-derived tool=receipts expect=accept declared=map:corpus/evidence/round35/tb2-grader-probe.txt:table,map:corpus/evidence/round38/build-pmars-probe.txt:table observed_rc=0 observed=map:corpus/evidence/round35/tb2-grader-probe.txt:table,map:corpus/evidence/round38/build-pmars-probe.txt:table ok
FIXTURE r_map-t11-table-near-stem-decoy tool=receipts expect=accept declared=map:corpus/evidence/round35/tb2-grader-probe.txt:table observed_rc=0 observed=map:corpus/evidence/round35/tb2-grader-probe.txt:table ok
FIXTURE r_map-t12-log-population tool=receipts expect=accept declared=skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command observed_rc=0 observed=skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command ok
FIXTURE r_map-t12-log-with-table-sibling tool=receipts expect=accept declared=map:corpus/evidence/round36/regex-log-probe.txt:table,skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command observed_rc=0 observed=map:corpus/evidence/round36/regex-log-probe.txt:table,skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command ok
FIXTURE r_map-t12-log-derived tool=receipts expect=accept declared=map:corpus/evidence/r/foo-probe.log:derived observed_rc=0 observed=map:corpus/evidence/r/foo-probe.log:derived ok
MUTANT T09 receipts silence killed by=r_map-t09-shared-stem-separators -- plans/tip_receipts.py:13-14 'if its own basename resolves to exactly one committed `plans/
MUTANT T10 receipts silence killed by=r_map-t10-derived-mapping -- plans/tip_receipts.py:15-16 'with non-alphanumerics dropped and case folded, the receipt s
MUTANT T11 receipts silence killed by=r_map-t11-table-overrides-derived -- plans/tip_receipts.py:13-14 'A file enters the byte-comparison if the RECEIPTS table maps 
MUTANT T12 receipts silence killed by=r_map-t12-log-population -- plans/tip_receipts.py:12 'Population, stated mechanically: committed files `corpus/evidenc
BATTERY fixtures=10 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=4/4 sources=0/0
ADVERTISED direct=4 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0
```

Raw copy of that run: `dev-run.txt` beside this report.

## Load-bearing measurement

**Per-fixture attribution** — each fixture alone in the battery (10 runs, filter
`FIXTURES = [f for f in FIXTURES if f["fid"] == "<fid>"]` appended in scratch), command shape as above with
`--battery-dir "$S/single/sNN"`:

```
fixture=r_map-t09-shared-stem-separators kills=T09, BATTERY fixtures=1 wrong=0
fixture=r_map-t09-shared-stem-case-fold kills=T09, BATTERY fixtures=1 wrong=0
fixture=r_map-t10-derived-mapping kills=T10, BATTERY fixtures=1 wrong=0
fixture=r_map-t10-derived-with-table-sibling kills=T10, BATTERY fixtures=1 wrong=0
fixture=r_map-t10-derived-deep-layout kills=none BATTERY fixtures=1 wrong=0
fixture=r_map-t11-table-overrides-derived kills=T11, BATTERY fixtures=1 wrong=0
fixture=r_map-t11-table-near-stem-decoy kills=T11, BATTERY fixtures=1 wrong=0
fixture=r_map-t12-log-population kills=T12, BATTERY fixtures=1 wrong=0
fixture=r_map-t12-log-with-table-sibling kills=T12, BATTERY fixtures=1 wrong=0
fixture=r_map-t12-log-derived kills=none BATTERY fixtures=1 wrong=0
```

**Drop-one** (10 runs; each fixture removed in turn) — no mutant flips, because each of T09, T10, T11, T12 is
killed by two class-matched shapes:

```
drop=r_map-t09-shared-stem-separators survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t09-shared-stem-case-fold survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t10-derived-mapping survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t10-derived-with-table-sibling survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t10-derived-deep-layout survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t11-table-overrides-derived survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t11-table-near-stem-decoy survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t12-log-population survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t12-log-with-table-sibling survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
drop=r_map-t12-log-derived survivors=none | MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
```

**Drop-the-pair** (both killing shapes of one mutant removed) — exactly the intended mutant survives:

```
drop-pair=t09 -> MUTANTS total=4 killed=3 survived=1 invalid=0 null_detected=0 T09 `plans/
drop-pair=t10 -> MUTANTS total=4 killed=3 survived=1 invalid=0 null_detected=0 T10 s
drop-pair=t11 -> MUTANTS total=4 killed=3 survived=1 invalid=0 null_detected=0 T11 maps
drop-pair=t12 -> MUTANTS total=4 killed=3 survived=1 invalid=0 null_detected=0 T12 `corpus/evidenc
```

So each mutant's kill is load-bearing on its pair, and no fixture kills a mutant it was not aimed at. (The
`killed by=` column earlier reported only the first killer; the single-fixture runs give the full attribution.)

## Full default counter (module staged in the clone's `plans/battery41`)

```
$ mkdir -p "$S/lane/plans/battery41"; cp …/battery/r_map.py "$S/lane/plans/battery41/r_map.py"
$ bwrap … python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py \
    --lane "$S/lane" --work "$S/wf" ; echo rc=$?
PINS total=2 mismatched=0
… (10 × FIXTURE … ok) …
MUTANT T01 receipts error SURVIVED exhibits=none -- plans/tip_receipts.py:30-32 '2 usage/setup (lane not a git work-tree root, no `corpus/evid
MUTANT T02 receipts error SURVIVED exhibits=none -- plans/tip_receipts.py:30-31 '2 usage/setup (..., no `corpus/evidence/`, ...)'
MUTANT T03 receipts rc-silence SURVIVED exhibits=none -- plans/tip_receipts.py:30 '1 a `differ`, a failed control, or a probe that did not complete
MUTANT T04 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:21-23 'absolute mkdtemp paths are masked on both sides, so equality 
MUTANT T05 receipts error SURVIVED exhibits=none -- plans/tip_receipts.py:31-32 '2 usage/setup (..., unknown `--tamper` id)'
MUTANT T06 receipts rc-silence SURVIVED exhibits=none -- plans/tip_receipts.py:29-30 '0 every mapped receipt reproduces ... and the control reports
MUTANT T07 receipts error SURVIVED exhibits=none -- plans/tip_receipts.py:30-31 '2 usage/setup (lane not a git work-tree root, ...)'
MUTANT T08 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:19-21 'A mapped receipt whose script is gone, whose dependency is ab
MUTANT T09 receipts silence killed by=r_map-t09-shared-stem-separators -- plans/tip_receipts.py:13-14 'if its own basename resolves to exactly one committed `plans/
MUTANT T10 receipts silence killed by=r_map-t10-derived-mapping -- plans/tip_receipts.py:15-16 'with non-alphanumerics dropped and case folded, the receipt s
MUTANT T11 receipts silence killed by=r_map-t11-table-overrides-derived -- plans/tip_receipts.py:13-14 'A file enters the byte-comparison if the RECEIPTS table maps 
MUTANT T12 receipts silence killed by=r_map-t12-log-population -- plans/tip_receipts.py:12 'Population, stated mechanically: committed files `corpus/evidenc
MUTANT T13 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:26-27 'the comparator must answer `differ`. ... A control that answe
MUTANT S01 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1020-1021 '# Exclusive: before this
MUTANT S02 sources 2>1 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1042 '--registry and --package are 
MUTANT S03 sources 2>5 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1053 '--access-date must be an ISO 
MUTANT S04 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1035-1036 '`--url-map` alone reache
MUTANT S05 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1051 '--entries is required when --
MUTANT S06 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1059 '--recheck must be an ISO date
MUTANT S07 sources 3>0 SURVIVED exhibits=none -- SKILL.md:573 '`3` staged/registry id collision'
MUTANT S08 sources 2>1 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1019 '--quote-file and --artifact m
MUTANT S09 sources 2>9 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error or unreadable quote artifact'; plans/sources_adopt.py:1028 '
MUTANT S11 sources 5>0 SURVIVED exhibits=none -- SKILL.md:573 '`5` requested id absent' (main() also refuses a requested row that is not `m
BATTERY fixtures=10 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=4 survived=19 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=4/13 sources=0/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
rc=1
```

`wrong=0 tampered=0 sidechannel=0 null_detected=0`, `invalid=0`, and T09–T12 killed; the other 19 survivors are
the other wave-1 seats' mutants (expected for a single-module battery). Raw copy: `full-run.txt` beside this report.

## Host safety

- Every counter/battery/fixture run went through the mandated envelope
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
  --unshare-pid --die-with-parent …`; the counter's own `--ro-bind / /` child sandboxes nest inside it.
- No write to any PATH directory, `/usr`, `/etc`, or `$HOME`; no `git` shim, no marker file. The neutralized
  modules `crit_git_shim.py` and `crit_ledger_selfread.py` were not touched (not read either).
- Scratch only: `/fast/scratch/hyaku/kengaku-r41/R41BatRcvMap/` (`TMPDIR` exported, `--work` explicit, abandoned
  `$S/w*`, `$S/single`, `$S/pair`, `$S/batt` dirs left to the `rm -rf` at the end). The lane edits in my clone were
  limited to the untracked `plans/battery41/r_map.py`; nothing committed, no `git add` outside my clone, no
  mutating jj command, no push. Writes outside scratch: only this report dir
  (`.ufo/waves/round-41/build/R41BatRcvMap/{r_map.py under battery/, dev-run.txt, full-run.txt, R41BatRcvMap.md}`).
- Tools installed: none (bubblewrap 0.13.1 and git 2.56.0 already present; Python is `/usr/bin/python3`).

## Limits / risks

1. **Attribution is pinned to the class string, including its path.** T10's class names
   `corpus/evidence/r/foo-probe.txt` and T12's names the `.log` skip reason. A same-branch fixture with a different
   receipt path (`r_map-t10-derived-deep-layout`) or a mapped `.log` (`r_map-t12-log-derived`) passes `ok` but
   attributes no kill — measured above, and the reason T10/T12 got a second *class-matched* shape. Any reviewer
   addition to these mutants' class cells would silently re-open them.
2. The kills record result differences in the declared direction (`silence`: the class the reference prints is
   absent from the mutant's output), not the fixture's narrative intent; the intent is the one-line comment only.
3. All fixtures run `--list`, so this module exercises classification (population, table override, derived stem)
   and not the run/compare/control path. T01–T08, T13 and every S-mutant stay for other seats.
4. `defects` equality is a set comparison; the module declares exactly the printed classes, but a future tool
   message change (e.g. a new reason word) would surface as `wrong`, not as a silent pass — that is the counter's
   contract working, not a hidden dependency.
5. Determinism relied on fixed commit metadata (`GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` supplied by `Ctx`); the
   `tip <sha>` line is stable, which is why `null_detected=0` on 10 re-runs.

VERDICT: battery41-r_map-killed-4/4-wrong-0
