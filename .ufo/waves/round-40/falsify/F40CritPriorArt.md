# F40CritPriorArt — wave-2 attack on the entry's §Prior art

Seat: critic. Target: `corpus/knowledge/tb2-db-wal-recovery-grader.md:294-319` (§Prior art, entry
`tb2-db-wal-recovery-grader`), reviewed at lane tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.
Bytes reviewed are the tip's: `git show ec1005a2:corpus/knowledge/tb2-db-wal-recovery-grader.md |
sha256sum` = `f51dd9e7…` = the worktree file (lane `HEAD` is the child `c9c793c`, wave-2 dispatch; the
entry is unchanged between them). No lane file, index or jj state was written.
Receipts: `.ufo/waves/round-40/falsify/F40CritPriorArt/` (`prior_art_attack.sh` + `.log`,
`prior_art_gh.sh` + `.log`, `check_wal_section.py`, `audit-dbwal-section.txt`,
`kimjune01-db-wal-verdicts.txt`, `bro659-excerpt.txt`, `pr3-run-bundle.txt`, `SHA256SUMS`).
Host safety: `prior_art_attack.sh` ran only inside
`bwrap --dev-bind / / --ro-bind ~/.local/bin ~/.local/bin --tmpfs /run/user/1000 --proc /proc
--unshare-pid --die-with-parent`; `prior_art_gh.sh` is GET-only and had to run outside that wrapper
because `gh` reads its token from the session keyring, which `--tmpfs /run/user/1000` hides
(the wrapper log shows `CHECK E SKIP`). No lane file, index or jj state was written; scratch under
`/fast/scratch/hyaku/kengaku-r40/F40CritPriorArt` removed at exit.

Axes attacked: **A1** prior-art locatability (does the citation resolve), **A2** prior-art fidelity
(does the quoted sentence stand for what the source says, and are the strongest prior statements
present), **A3** absence-claim honesty (`not reported`, `the one audit`), **A4** claim strength
(`TB2.1 carries the same task bytes`).

---

## 1. What stands (no defect found)

Every check below is a line in the two logs; `PASS`/`INFO` labels are the scripts' own.

| item | receipt | result |
|---|---|---|
| S121 PR #3 quote located, §Reasoning, **21 words** | `prior_art_gh.log` CHECK E1 PASS | verbatim |
| PR #3 opened 2026-05-21, **open, unmerged** at access | CHECK E1 `state=open merged=false created=2026-05-21T21:43:34Z` | true |
| PR #3 `changes neither instruction.md nor tests/` | CHECK E1 `files=2`, changed = `environment/Dockerfile`, `solution/solve.sh` | true |
| #2218 comment dated 2026-10-12, quote **9 words** | CHECK E2 `created=2026-10-12T19:44:35Z` + PASS | verbatim |
| #3607 dated 2026-10-10, paraphrase **14 words** | CHECK E2 `created=2026-10-10T01:48:06Z` + PASS | matches body |
| `wal.html` §4 quote, **15 words**, cited section correct | CHECK D PASS `…in "4. The WAL File"` (`check_wal_section.py`) | verbatim, §4 confirmed |
| `fileformat2.html` §4.1 two magics | CHECK D PASS (`0x377f0682 or 0x377f0683`) | true |
| XOR-0x42 file starts `753d44c0` | CHECK D PASS (`head -c4 … \| od`) | true |
| **TB2.1 carries the same task bytes** | CHECK A 3/3 equal, CHECK A2 **6/6 more** equal, CHECK B TB2 `main` 3/3 equal, CHECK C zai-org fork `test_outputs.py` equal | **true, and stronger than written: 9/9 files, not 3** |
| capture provenance | `sha256sum -c` green in both `R40ScoutPriorArt/` and `corpus/evidence/round40/tb2-db-wal-recovery/`; live GitHub bodies strip-equal to the three captures | no drift |

Quote-length audit (the seat's rule): 21 / 9 / 14 / 5 / 15 words — all ≤25; the two quoted-prose
truncations (`…inspected it`, `Not all values are verified`) cut at a clause boundary, not mid-claim.

---

## 2. Defects

### D1 — the audit locator does not resolve (A1)

Counterexample: the exact path the entry gives returns HTTP 404 at the exact commit it names.

```
$ curl -sSL -o /dev/null -w '%{http_code}\n' \
    https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/35f11039/audit.txt
404
$ gh api 'repos/JonathanGabor/terminal-bench-2-audit/git/trees/35f110397bc8…?recursive=1' \
    --jq '.tree[]|select(.path|test("audit\\.txt$"))|.path'
audit_results/20260120_125158/audit.txt
```

Entry text: `corpus/knowledge/tb2-db-wal-recovery-grader.md:313` —
“(`JonathanGabor/terminal-bench-2-audit` `audit.txt:782` @ `35f11039`…”. The quote itself is honest:
line 782 of the *real* file reads `- Not all values are verified (e.g., values for records 3-11 aren't
checked)` (`audit-dbwal-section.txt`). Impact: a reader cannot reach the quote from the citation; the
lane's own `corpus/lessons/round-40.md:29` inherits the same dead path.

### D2 — the cited audit already states the entry's finding 3 in prose, and “the one audit” is false (A2, A3)

Counterexample 1 (underquote). The entry quotes only line 782. The next two lines are the same
audit's statement of the rest of the free set — and of the entry's contract finding:

```
782 - Not all values are verified (e.g., values for records 3-11 aren't checked)
783 - Names for records 1-2 aren't verified (though values are)
784 - No verification of the decryption method itself (just the outcome)
```

(the entry's locator as written is wrong, D1; real file). Those two lines cover 9 free values (ids 3-11)
and 2 free names (ids 1-2) — exactly `tb2-db-wal-recovery-grader.md:210`: “The nine values of ids 3-11
are free, and so are the names of ids 1-2.” 33 − 11 = 22. So “the 22/33 pin surface” is **unnamed as a
count but fully named as a set** in one public file, and line 784 is the entry's “graded only through
the export” thesis in a stranger's words. The same audit also makes the sufficiency claim the entry's
`literals-never-open-db` refutes (line 794): “enough critical data points … are checked to ensure the
solution is legitimate” (12 words) — the strongest prior-art hook available, and it is unmentioned.

Counterexample 2 (“the one audit”). A second public audit carries this task:

```
$ grep '"task":"db-wal-recovery"' verdicts-2.1.jsonl | wc -l   → 5
{"task":"db-wal-recovery","mut":"wipe-sentinel",…,"reward":1,…,"verdict":"FRAME_BLIND",…}
```

`kimjune01/terminal-bench-audit` `results/verdicts-2.1.jsonl` lines 91-95, file committed `2a2baec2`
2026-07-09; `DESIGN.md:70` defines the verdict (“reward still 1 **and** M's damage ⊄ `oracle_diff(T)`”).
This does **not** report a task-specific grader defect — its in-workspace mutations are
`"applied":"not_applicable"` (lines 92-94) and `CLAIMS.md` states the sentinel result as one global
claim over 83 tasks — so the entry's core survives. But “The one audit that touches it”
(`:312`) is false, and with it the inference a reader draws from “not reported”.

### D3 — a public, executed report of the fabricated export is missing (A2)

`dzhioev/bro` issue #659 (open, 2026-09-18, bot-filed, five trials of `terminal-bench/db-wal-recovery`):

- “Each trial then hit `FileNotFoundError` on the WAL … and invented the six missing rows” (14 words)
- “Three of the four also wrote a fresh WAL from the invented rows” (13 words)
- “The verifier caught it only because the two updates in the lost WAL were unguessable” (15 words)
- reward column: four `0`, one `1` (the run that decoded before opening)

That is the entry's destructive-read trap (a third published instance), its “hand-typed pass” surface
*in the wild*, its “unchecked repair step” actually exercised, and a public statement that the grade
turns on ids 1-2's values. It is outside the entry's four named repositories, so the sentence at
`:314-315` survives as scoped; the bullet title at `:312` (“The grader's permissiveness is not reported
as a defect”) does not, and the entry loses its strongest *counter*-evidence: when the fabricator does
not know the two updated values the pin surface catches it 4/4. A second executed bundle is nearer to
hand and uncited: PR #3's own comment (2026-06-11) attaches five runs, `reward` 0/1/0/0/1, and each of
the three failing runs fails all seven functions on `test_recovered_json_exists` (no export written) —
an executed instance of the trap the entry currently cites only as prose.

---

## 3. Searches run (A3), and their limits

`prior_art_gh.log` CHECK I, per repository, `gh search issues` (token-AND, includes bodies):

```
terminal-bench      :: 'db-wal' -> 1   (issue #2218)   'recovered.json' -> 0
terminal-bench-2    :: 'db-wal' -> 0                    'recovered.json' -> 0
terminal-bench-2-1  :: 'db-wal' -> 0                    'recovered.json' -> 0
harbor              :: 'db-wal' -> 2   (#3607, #3576)   'recovered.json' -> 1 (#3607)
```

Also opened: all 8 comments of #2218 (no permissiveness report; maintainer reply of 2026-10-19 commits
only to a general verifier-hardening release), PR #3's comment/reviews (one comment, an attachment),
`zai-org/terminal-bench-2-verified` README (no `db-wal-recovery` row; its `test_outputs.py` is byte-equal
to the pin, CHECK C), its two HF discussions (unrelated), and two other TB audits
(`psiwho/tb-audit-findings`: no db-wal finding; `kimjune01`: D2). **No public source states the count
22/33**; two state the set or the discriminator. `gh search` is fuzzy — a two-token query returns 250
hits — so this is a search, not a proof of absence, as the entry itself says.

---

## 4. Smallest safe correction (one edit, four lines)

In `corpus/knowledge/tb2-db-wal-recovery-grader.md:312-316`:

1. `audit.txt:782` → `audit_results/20260120_125158/audit.txt:782-784`; extend the quote to 783-784
   (9 and 10 words).
2. “The one audit that touches it” → “Two public audits touch it:”; add the `kimjune01` row — 5 verdict
   rows, `FRAME_BLIND` under the global `wipe-sentinel` mutation, in-workspace mutations
   `not_applicable`, so no task-specific defect.
3. Narrow the negative to what is actually unreported: *no report states the count (22 of 33), and none
   executes a from-scratch export*; add one sentence for `dzhioev/bro` #659 — fabricated rows plus a
   fabricated WAL in four of five runs, caught 4/4 only by ids 1-2's values.
4. Same dead path at `corpus/lessons/round-40.md:29`; and “names two unpinned cells” there is off by
   nine — the audit names two *groups* covering eleven cells.

Claims 1 and 2 (S121/#2218/#3607, dates, word counts, `changes neither instruction.md nor tests/`) and
claim 4 (same bytes) need no change; claim 4 can be strengthened from three files to nine (CHECK A2).

**VERDICT: prior-art-attack-3-defects**
