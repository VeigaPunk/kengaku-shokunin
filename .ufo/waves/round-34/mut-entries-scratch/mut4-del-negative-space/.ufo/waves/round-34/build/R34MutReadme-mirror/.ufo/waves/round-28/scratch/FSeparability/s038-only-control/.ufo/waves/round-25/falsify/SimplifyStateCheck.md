ATTACKS: dead branches, duplicated helpers and unreachable code in plans/state_check.py (YAGNI, read-only; no lane edits)

Snapshot: tip 8ea41f9ed, md5 9e652983…, 1272 ln. All line refs are that snapshot. The live tree
was edited concurrently by wave-2 peers while I read it (29b50250…/1309 ln → ebfb8aeb…/1333 ln,
still uncommitted); every finding below still exists there (grep at live 271,305,584,822,961/
970,1081,1111,1295) with lines shifted a few rows. I wrote only /tmp/k25w2-SimplifyStateCheck;
scratch restored byte-identical to the archive.

Evidence: pristine `git archive 8ea41f9ed` copy → `python3 plans/state_check.py --summary` = `assertions=236 match=232 mismatch=0 superseded=1 offline_unverifiable=3`, rc 0; `--selftest` rc 0. Branch data: `python3 -m trace --count --missing` over both modes, union of the two covers. ruff 0.17.1 `--no-cache --select F,B,SIM,RET,PLR`; vulture 2.16 at min-confidence 60 = empty.

Unreachable / unexercised:
1. plans/state_check.py:601-616 `find_protocol`: body 0 hits in both runs; main:1248 takes SEED_FIXTURE whenever plans/fixtures/r25/shonen-seed.txt exists (it does at tip), so the fallback and its error branch 1249-1253 (also 0 hits) are dead in-repo; the fallback additionally scans Path.cwd() and all parents → env-dependent. Delete = 21 ln.
2. plans/state_check.py:305-313 `CommandRunner.run` allowlist guard: 0 hits; both call sites can only pass allowlisted tuples (normalize_command 286-291 filters, 548-549 substitutes FREEZE_CHECK_COMMAND) → a second authority for the invariant normalize_command already enforces. Delete = 9 ln.
3. plans/state_check.py:813-827 section-pointer chain: 0 hits in both runs; reachable only on evidence lines that already fail pointer-only, since POINTER_ONLY_RE (:195) excludes `§` — it can never change a box verdict. Probe with evidence `§C2:23`: `MISMATCH P2c.box.1.pointer-only`, `MISMATCH P2c.box.1.pointer`, `MISMATCH P2c.box.1.section-pointer.1`. Delete = 16 ln incl. its README read at :813.
4. plans/state_check.py:271 `and not text.startswith("### ")`: dead conjunct — `"### x".startswith("## ")` is False (verified in python3), so it excludes nothing the first test admits.
5. plans/state_check.py:950 `anchors["lessons/"] = what[0] + 1`: dead store in-population, overwritten at :959; if the lessons heading were absent it silently aliases the knowledge anchor instead of failing.
6. plans/state_check.py:578 `"test -e"` set member is inert: the path fallback at :575 cannot match a space (`re.fullmatch(pat,"test -e")` → False); `ss`/`sha256sum` are load-bearing (they would be tested as root/<name> → MISMATCH).
7. plans/state_check.py:1074 `.get(assertion.verdict, 0)`: default never needed (all 5 verdicts preseeded 1069-1071); worse, an unknown verdict would be counted but never printed (summary reads only the 5 keys) — `verdict_counts[verdict] += 1` is equivalent and surfaces typos.

Duplication:
8. plans/state_check.py:712-724 duplicated mismatch arms: 714-716 vs 720-722 byte-identical (`diff` empty); only `cursor += 1` differs. Both arms 0 hits (selftest only mutates evidence text/appended boxes). The else arm does not advance: replacing box 1 with prose printed 4× `MISMATCH: P2c.box.{1,2,3,4}.seed:5` for one line. Collapse to one add + conditional advance = 5 ln.
9. plans/state_check.py:1104-1118 inline seed literal duplicates plans/fixtures/r25/shonen-seed.txt: `canonical_seed()` on both gives identical 8-line blocks while the headers already differ ("verbatim — `<name>`…" vs "verbatim"). Drift proof: replacing a fixture box with "MUTATED box text" leaves `--selftest` rc 0 ALL PASS (it tests its private copy) while the gate drops to mismatch=3. Selftest should parse SEED_FIXTURE; saves ~13 ln.
10. plans/state_check.py:430-433 vs :499-502: identical SCORECARD read + None-guard prologue in check_capabilities/check_axis_table (8 ln, only the assertion id differs).
11. plans/state_check.py:1118-1228: 9 copies of `print(<msg>, file=sys.stderr); return 1` (3 more in the live edit) — one `fail()` helper.
12. plans/state_check.py:235-240 `line_text` vs `content_text`: the second is the first + `rstrip("\r")`; merge is low value (CRLF semantics), flagged not recommended.

Checked and NOT dead (avoid false cuts): row_map's header-filter keys `entry/file/dir` all occur as real README headers (corpus/README.md:27,97,107); AXIS_ANCHOR_CONTENT's single `:162` key is the frozen population, not an omission; `--json` :1260-1262 and the FAIL print :1094 are live-but-unexercised, not dead. ruff B007 unused `cells` bindings at 442, 518, 897 are cosmetic.

Provenance aside: docstring:7 pins "PROTOCOL.md:439-448 sha256 886e459b…"; 886e459b is the whole PROTOCOL.md, while that slice (= the fixture, 460 B) is 3962e6b8…. The pin names the wrong object.

VERDICT: BREAKS — gate reproduces PASS, but ≈53 lines are mechanically dead (601-616+1249-1253, 305-313, 813-827, 712-724 partial) and ≈23 lines duplicate a second authority (seed literal, SCORECARD prologue); deletion list above. Installs: none (used preinstalled ruff 0.17.1, vulture 2.16).
