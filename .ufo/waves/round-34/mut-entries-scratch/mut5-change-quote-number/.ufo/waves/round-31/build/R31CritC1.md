# R31CritC1 — falsification of C1's predicate and control

Seat: critic (leaf). Lane: kengaku, round 31. Baseline tip `0883e72` (counter committed at `623c1fc`,
unmodified at tip: `git status --porcelain plans/adoption_check.py` → empty).
All fixtures under `/tmp/r31-R31CritC1/` (12 MB, nothing written outside it). No production byte touched.

## What I attacked

`plans/adoption_check.py` (the frozen counting command) and
`.ufo/waves/round-31/claims/control-nothing.txt` (the committed control receipt), against the frozen
sentence in `plans/round-31-claims.md` §C1 and the expectation artifact
`.ufo/waves/round-31/adoption-expect.json` (`git status`: `?? .ufo/waves/round-31/` — untracked).

Method: copy the lane's pre-append corpus (`SOURCES.md`, `README.md`, `QUALITY.md`, `knowledge/`,
`lessons/`), the counter and the expect JSON into `/tmp/r31-R31CritC1/root/kengaku-shokunin`, add a
fixture-root `shokunin.conf` (`kengaku|kengaku-shokunin|fixture lane`) so the counter's own census
call resolves, then run the **frozen command verbatim** in each variant:

```
python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census
```

## 1. Stub constructions — the triad is shape-only

### V1 — 63-byte stub passes with the exact frozen line, exit 0

Entry written (63 bytes, whole file):

```
source: S092
source: S093
source: S100
verified-at: 2026-10-25
```

Registry: three appended rows whose *entire* provenance is fabricated —

```
| S092 | stub source S092 — https://example.invalid/S092 | code | A | stub scope | stub anchor | stub teaches | mined | 2026-10-25 | 90d | corpus/knowledge/benchmark-verifier-execution-model.md |
```

(same for S093, S100). Index row inserted **before the H1, outside every table**:

```
| `knowledge/benchmark-verifier-execution-model.md` | x | y |
```

Output:

```
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=0
```

The staged package entry is 5,150 bytes / 87 lines
(`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-verifier-execution-model.md`).
The counter accepts 1.2 % of it, with no finding.

### V2b — a re-headed *unrelated* entry passes, exit 0

Same four header lines + the complete body of `corpus/knowledge/bench-arena-fresh-run.md`
(6,653 bytes). Occurrences of `verifier|harbor|terminal-bench|swe-bench pro`: **0**.

```
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=0
```

So the counter attests *a file at a path*, not *the assimilated entry*. It reads the entry only twice:
`^source:` lines (`adoption_check.py:34`, `:109`) and `^verified-at:` (`:79`). Every other byte of the
entry — the finding, the correction of the round-1 framing, the quote anchors — is never read.

### V3 — the frozen path can be absent; exit 0

`corpus/knowledge/benchmark-verifier-execution-model.md` renamed to `stub-any-name.md`, expect JSON
retargeted to it (registry `used-by` and the README row retargeted too):

```
frozen path ABSENT
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=0
```

### V4b — the frozen access date can be any past date; exit 0

`verified-at: 2026-10-20`, registry `opened=2026-10-20`, expect `"access_date": "2026-10-20"`:

```
4:verified-at: 2026-10-20
3:  "access_date": "2026-10-20",
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=0
```

(`2026-10-26` was refused — census `E08 opened=2026-10-26` — so the mutable date is bounded above by
today, not pinned to the frozen literal.)

### V5 — the guard that does bite, and the line/exit asymmetry

Duplicated `source: S092` line:

```
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=1
```

This is the frozen **pass line printed by a failing tree**. Since C1's control receipt records only a
line, it cannot express this distinction (see §3).

## 2. Clause-by-clause: what the code does not implement

| Frozen clause | Code | Verdict |
|---|---|---|
| `corpus/knowledge/benchmark-verifier-execution-model.md` exists | path taken from `expect["entries"][i]["path"]`, `:60-62`, `:70`; no literal | **not implemented as a literal** — V3 passes with the frozen path absent |
| `source:` lines citing exactly the three ids (three distinct) | set equality + duplicate-freeness, `:109-113` | implemented, relative to the expect list |
| the three ids *adopted this round* | registry URL/anchor/teaches cells never read | **not implemented** — V1 passes with `example.invalid` URLs and `stub teaches` |
| a `verified-at: 2026-10-25` line | `:79` against `expect["access_date"]` | **literal not implemented** — V4b passes with `2026-10-20` |
| three cited rows present, `status=mined`, `opened=2026-10-25`, `used-by` naming the entry | `:87-98`, `:114-117`; indices 7/8/10 match the `SOURCES.md` header (`id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`) | implemented (this is the sound part) |
| the entry has **one index row** in `corpus/README.md` | `:77-78`, `:119-128`: a column-0 line regex anywhere in the file, with cells 1 and 2 non-empty | **implemented as a line, not as an index row** — V1's row sits before the H1, outside any table, cells `x`/`y` |
| prints `entries=1 … census=ok` and exits 0 | `:144-164` | implemented; `exit 0 ⟹ line`, but `line ⇏ exit 0` (V5) |
| control: the same command on the pre-append tree | receipt is one line, no exit code, no tree/expect identity | see §3 |

Also unimplemented anywhere: the kill rule ("a cited source whose located quote cannot be found at the
pinned revision is refused"). The counter never sees a quote, an anchor, or a commit hash — the staged
entry's own `source:` lines carry `— commit <sha>` and the counter keeps only the id.

## 3. The control receipt

Positive half — verified. Running the frozen command on the real pre-append tree (the lane at tip; the
entry does not exist yet) reproduces the receipt byte-for-byte. Re-derived independently of
working-tree timing by materializing the baseline commit's bytes with read-only `git show`
(`0883e72:corpus/SOURCES.md`, `0883e72:corpus/README.md`, `0883e72:plans/adoption_check.py`) into
`/tmp/r31-R31CritC1/baseline/kengaku-shokunin` (entry file deliberately absent) — same 83 bytes, same
sha256, exit 1:

```
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
exit=1
sha256 e24593c9aac70ee94f96decd7478f55e2a5a67d737d2f1137f6096160ef06aa1
== .ufo/waves/round-31/claims/control-nothing.txt  (83 bytes, 1 line)
== /tmp/r31-R31CritC1/baseline.line  (baseline-commit materialization)
```

Current tree state at the time of this report (sibling C1 work in flight, not my edit): the entry has
landed (9,840 bytes) and the three rows exist, the index row does not — the counter prints
`entries=1 indexed=0 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 1. The
landed header is shape-correct (`source: S092/S093/S100` at the three pinned commits, `verified-at:
2026-10-25`), so the index row is the only remaining counter gate — which is exactly why §1 and §4
matter: that last gate is a column-0 line with two non-empty cells.

Three defects in what those 83 bytes can establish:

**(a) No exit code.** `defects-before.txt` ends `checks=10 defects=10`; `gate-before.txt` ends
`url_map_exit=2` / `selftest_exit=0`. `control-nothing.txt` carries no exit status, so the claim's
"and exits 1" is not evidenced by the committed artifact at all — and V5 shows the same line format
cannot distinguish exit 0 from exit 1.

**(b) Forgeable from a landed tree (V8).** A tree with the entry file present, the three rows landed and
the index row present — every field the counter reads satisfied — prints the byte-identical receipt and
exits 1, purely because the *untracked* expect JSON was retargeted at a nonexistent path:

```
entry file: PRESENT (63 bytes)
stub rows: 3
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
exit=1
sha256 e24593c9…  == control-nothing.txt  (identical)
```

So the receipt identifies "every path named by the expect file is absent", not "the pre-append tree".

**(c) A registry-half-landed tree produces it (V6).** Three rows landed (`status=mined`,
`opened=2026-10-25`, `used-by —`), no entry text, no index row:

```
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
exit=1
sha256 e24593c9…  == control-nothing.txt  (identical)
```

The claim's "cannot be produced by the landed tree" survives only for the *fully* landed tree
(`usedby_ok=1` differs); it does not survive as a statement about tree state.

**Attack that failed (honest negative).** I tried to make `census=ok` attest a different tree than the
six other fields by mapping the lane name elsewhere in a fixture `shokunin.conf`
(`kengaku|other-shokunin|…`) while `--lane` pointed at a census-dirty `kengaku-shokunin`. The census
roster overwrites the conf mapping with the physical `*-shokunin` directory, so the dirty tree was
validated and the counter exited 1 (`E11 S001 missing used-by corpus/knowledge/does-not-exist.md`).
The census clause is bound to the lane directory. Its residual weakness is only that `CENSUS` is a
hard-coded absolute path outside the lane (`:35`), so the verdict depends on a sibling repo's mutable
script; no lane byte pins it.

## 4. What a lazy adoption still passes

1. A 63-byte stub (V1) — four lines, no finding, no quote.
2. A re-headed unrelated entry (V2b) — 6,653 bytes about something else.
3. The frozen path missing entirely (V3).
4. Any past access date and any `verified-at` the expect file names (V4b).
5. Fabricated source rows — `example.invalid` URL, `stub anchor`, `stub teaches`; census never fetches a
   URL and E11 only checks that the `used-by` path exists.
6. An "index row" placed before the H1 with junk cells `x`/`y` (V1).
7. Copying the staged entry verbatim and bumping only `verified-at` to `2026-10-25` without re-opening
   the three pinned commits — indistinguishable, because no quote, anchor, or commit is read.
8. Citing S092/S093/S100 with wrong commit hashes in the `source:` lines — only the id is captured.
9. Restating the round-1 framing instead of correcting it — the claim's own "corrects … instead of
   restating" clause has no counter of any kind.

## 5. Impacted axes and the smallest safe correction

- **coverage (C1's axis):** the counting command cannot carry the coverage credit. The credit rests on
  the entry's bytes and on the three quotes being locatable at the pinned revisions — both unread by
  `adoption_check.py`. C1's verdict must cite reviewer-verified entry bytes, not the pass line.
- **calibration:** the control is the calibration surface, and it is exit-code-free and forgeable from a
  landed tree (V8). This is a real defect, not a tradeoff.
- **novelty / operability:** untouched.

Smallest safe corrections, in order of cost:

1. **Receipt hardening (one line, no code change).** Append `expect=<sha256 of the expect file>` and
   `exit=1` to `control-nothing.txt`, matching `gate-before.txt`'s existing `url_map_exit=2` style. With
   the expect hash in the receipt, V8's retargeting yields a different receipt; with the exit code, the
   claim's "exits 1" is evidenced. This alone kills the strongest counterexample.
2. **Print the invocation, not only the counts.** A second line naming `path=` and `access_date=` from
   the expect file pins which tree the line describes. The seven frozen fields are unchanged, so the
   frozen predicate is untouched.
3. **Do not amend the predicate now.** A predicate changed after a seat has scored is not this claim's
   predicate. The shape-only finding is recorded as the bound on what C1 may claim from the counter.

VERDICT: C1-CONTROL-FORGEABLE — the frozen command passes a 63-byte stub and a re-headed unrelated entry with the exact pass line and exit 0 (V1, V2b), three of the sentence's literals (path, access date, source identity) live only in an untracked mutable JSON (V3, V4b, V1), and the control receipt is exit-code-free and byte-identical when reproduced from a landed tree by retargeting that JSON (V8) and from a registry-half-landed tree (V6); C1 may proceed only with receipt hardening (`expect=<sha>`, `exit=1`) and with its coverage credit re-anchored on reviewer-verified entry bytes and locatable quotes, not on the pass line.

## Provenance

- Counter bytes: `plans/adoption_check.py` at `623c1fc`, unmodified at tip `0883e72`.
- Real pre-append run: `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census`, cwd = lane, exit 1, sha256 `e24593c9…` (matches the receipt).
- Baseline re-derivation: same command in `/tmp/r31-R31CritC1/baseline/kengaku-shokunin`, built from
  `git show 0883e72:` bytes, entry absent, exit 1, sha256 `e24593c9…` (matches the receipt).
- Fixtures: `/tmp/r31-R31CritC1/{root,baseline,v2b,v3,v4,v4b,v5,v6,v7,v8}/`, 12 MB total.
- No tool installed or upgraded; no pacman transaction; no network fetch needed (all sources local).
- Not verified: the landed entry's substance (its quotes, its correction of the round-1 framing);
  quote locatability at the three pinned commits (outside this seat's scope); whether the landed tree
  will pass the counter once the index row lands (I did not add it — production edit is not mine).
