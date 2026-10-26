# F41CritPriorArt — query log (2026-10-26, host-local -03)

Window 16:13:10 → 16:27:50. `gh` authenticated as VeigaPunk; search quota 30/min, no 403/429 seen.
Every command below was run from /tmp; outputs are the exact totals/items printed.

## GitHub issue search (gh api search/issues)

Org-wide (`org:harbor-framework`):
- `earliest slot` → 6 hits: #245 TB2.1 (on task), rest unrelated TB-science tasks.
- `grader false positive` → #133 TB2.1 configure-git-webserver, rest unrelated.
- `verifier` → 10: #2284, #3624, #2135, #2105, #2130, #2029, … none on constraints-scheduling.
- `constraints-scheduling` → #1883 noodles (TB), #245 (TB2.1), #2315/#2228/#2308 (unrelated).
- `newline` → harbor #3452/#3472/#3493/#3459/#3748 (harness I/O, not our axis).
- `CRLF` → harbor #3768, #1240; TB #2244, #2003, #3606 (line endings in scripts, not grader integrity).
- `input integrity` → harbor #3236/#3546; TB #2050/#2057; unrelated.
- `reward hacking` → TB #2097, #2086, #3725, #2135, #1612.

Per-repo (TB2 = harbor-framework/terminal-bench-2, TB2.1 = …-2-1):
- TB2 `earliest` → 0; TB2.1 `earliest` → #100 dna-insert, #245.
- TB2 `slot` → 0; TB2.1 `slot` → #245, #142 (leaderboard).
- TB2 `constraints` → #44, #53, #32; TB2.1 `constraints` → #245, #100, #242, #208, #206, #142.
- TB2 `calendar` → 0; TB2.1 `calendar` → #245 only.
- TB2 `newline` → 0; TB2.1 `newline` → 0. TB2.1 `read_text` → #236 (heap cleanup, other task).
- TB2.1 `integrity` → #213, #154, #175. TB2 `integrity checker` → 46, none on this task.
- TB2.1 `"input calendar"` → #245. TB2.1 `"line endings"` → 0.
- TB2.1 `"read-only"` → #241 (whitespace-sensitive ARS), #236, leaderboards, #214, #242.

Global (`search/issues`, all repos):
- `"constraints-scheduling" earliest` → TB3 #15 (inaccessible), #245, plus unrelated.
- `"constraints-scheduling" verifier` → #245, `tuzengji/TerminalBench2-Glm5-OpenClaw` #1, unrelated.
- `"constraints-scheduling" integrity` → #245, `Eoghanmcc1000/TB1` #1, unrelated.
- `"constraints-scheduling" CRLF` → #245, unrelated.
- `"constraints-scheduling" in:title` → unrelated repos only + #245 pattern.
- `"Found earlier valid slot"` → 3 unrelated Autosport issues.
- `"bob_calendar"` → vdirsyncer/spectrum2, unrelated. `"_hard_ok"` → 0.
- `"Team Planning Meeting" verifier` → #245 + unrelated.

## GitHub code search (gh api search/code)

- `"Found earlier valid slot"` → lane files + `hamishivi/tmax` verifier `ctrf.json` files (grader output, no prose).
- `"bob-start-0900-wed"` / `"input-crlf-rewrite"` → lane only.
- `"test_earliest_tiebreakers_and_carol_buffer"` → tmax `ctrf.json` files only.
- `"meeting_scheduled.ics" read_text` → trajectories (llm-as-a-verifier, openagents), task copies (jeju).
- `constraints-scheduling earliest slot` / `… grader` → task copies, harness-bench, openagents docs.
- `"DTSTART:(\d{8}T\d{6}Z)" verifier` → task copies + lane.
- `"read_text()" "CRLF" verifier` → unrelated.
- `constraints-scheduling verifier extension:md` → harness-bench, openbench PROVENANCE, AgentStepVerification, headlong, HarnessX, lane.
- `constraints-scheduling integrity extension:md` → PROVENANCE, harness-bench, whip, openagents docs, lane.
- `org:harbor-framework "newline=None"` → 0. `"universal newlines"` → 0. `"read_bytes" integrity` → several terminal-bench-science `contract_integrity.py` files (byte-level integrity elsewhere in the org).
- `AhXMZPnOPS` → lane only.

## Fetched and read (raw files / PDFs)

- `PR #245` body + diff (`gh api … -H Accept: …diff`): 4514 B body, 365-line diff; grep `earliest|newline|read_text|integrity|slot` → body lines 7, 15, 22, 30; diff lines 34-35 (spec), 292 (integrity block unchanged context).
- `PR #245` comments → 0; reviews → 0; state `closed`, `merged=false`, 4 files.
- TB2.1 `main` raw `tests/test_outputs.py` → sha256 `1422b345…` = lane capture digest.
- `JonathanGabor/terminal-bench-2-audit` audit.txt (3687 lines): task section at 625-; quotes at 651, 657, 668-671.
- `few-sh/terminal-wrench-trajectories` README (93 072 B): `grep -i scheduling` → `schedule-vacation` only; `grep -i -c calendar` → 0; TB2 included 14/89.
- `harbor-framework/terminal-bench` #2150 → Tokenless TB4 index (24 write-ups), `grep -c constraints` = 0.
- Horizon audit page (29 tasks; 8 TB2.1 rows listed) — no constraints-scheduling.
- Harbor-Index release page — TB2 3 tasks, no per-task defect list.
- RDI blog (13 benchmarks, Terminal-Bench example = portfolio-optimization).
- Node: `arxiv.org/pdf/2609.26826` (fake-hardness), `2608.22103` (HVTB), `2601.11868` (TB2 paper), `2606.08960` (hacker-fixer), `2610.16067` (oracle-failure), `2609.01354` (Where the Verifier Fails) — pdftotext + grep for `constraints-scheduling|calendar|earliest|CRLF|newline|read_text|integrity`.
- arXiv API queries: `"terminal-bench"`, `"constraints-scheduling" OR "calendar scheduling" OR "verifier" AND "benchmark"`, `"agent benchmark" AND "verifier"`, `"benchmark defects" OR "test oracle" AND "agent"`.
- OpenReview `AhXMZPnOPS` (DL4C paper): curl default UA → challenge page; browser UA → same; `api2.openreview.net/notes?id=` → 403 ChallengeRequiredError; Wayback `available` → no snapshot; `r.jina.ai` proxy → challenge page; real Chromium (eval `browser.open`) → "Verifying your browser" page, LEN 248. UNREADABLE.
- Python docs: `docs.python.org/3/library/functions.html` → newline semantics sentence; `library/pathlib.html` (read_text).
- HF dataset discussions `harborframework/terminal-bench-2.0` → 4 entries.
