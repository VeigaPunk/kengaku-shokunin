# DebtR79 — seven closure-debt row drafts

## Behavior and gates

Axes: **coverage** (all seven routed ids addressed) and **calibration** (closed means repaired, not registered or asserted).

**Observed:** all seven draft checks fail at base `660ec0b9` and at frozen revision `5d6843134017780c045e92eed4e83264188a7d47`, each with rc 1. No repaired-tip green is claimed. These are prospective JSONL rows, not evidence that the debts are already closed. Append only after the named repairs land and their checks pass. No frozen predicate, target, control, or kill rule was changed; no counter was imported.

Read the entire frozen claim file before commands, then spot-check §§2–6, routed_open.py schema, and referenced committed receipts. Archives are detached immutable snapshots, not git fixture repositories; no git init or commit was performed.

### Extraction command (rc 0)

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r79/DebtScribeR79/base /fast/scratch/hyaku/kengaku-r79/DebtScribeR79/freeze && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 660ec0b9 | tar -x -C /fast/scratch/hyaku/kengaku-r79/DebtScribeR79/base && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 5d6843134017780c045e92eed4e83264188a7d47 | tar -x -C /fast/scratch/hyaku/kengaku-r79/DebtScribeR79/freeze
```

Each `check` below was passed verbatim to Python `subprocess.run(check, shell=True, cwd=<archive>, text=True, capture_output=True)`, with archive directories as above. Independent check processes ran concurrently. Initial D1 Markdown comparison and D2 diagnostics were refined, and only those two were re-exercised; outcomes below are the final commands' observations. This is the explicitly requested check execution, not a lane-wide verification run.

## Exact repairs and close values

The commands deliberately use exact dated correction headings and fact tokens described below. Those are proposed repair formatting, **not new frozen rules**. An integrator choosing another equivalent format must adapt the check while preserving the independent receipt derivations and base-red/landing-green requirement. All `close` values are existing tracked document paths which must gain the corresponding id in the real repair; the frozen versions do not constitute closure evidence merely because the path exists.

### R78-D1 — close `SCORECARD.md`

Append `### R78-D1 correction (2026-11-04)` to LOG.md, corpus/lessons/round-78.md, and SCORECARD.md. Each block says it **supersedes** the earlier `11 TOOL-UNNAMED, 10 COMMAND-ABSENT, 4 PASS-UNLOCATED, 2 WORKTREE-ABSENT, 2 TOOL-UNPINNED` split, gives the receipt-derived replacement `11 TOOL-UNNAMED, 11 COMMAND-ABSENT, 5 PASS-UNLOCATED, 2 WORKTREE-ABSENT, 0 TOOL-UNPINNED`, and retains the historical 29 total. Correct the main SCORECARD R78-C2 row itself to the new split; include the counting command (the check below). Preserve filed report bytes and identify their line 97 as superseded in the LOG correction.

### R78-D2 — close `SCORECARD.md`

Correct both main SCORECARD R77-C1/R77-C2 after cells in place, dated, to `stamped `cd2e25bb`, clean` (with the inner backticks retained as Markdown). Append `### R78-D2 correction (2026-11-04)` in SCORECARD.md identifying both c1-after.txt/c2-after.txt, the old d181e16b attribution, and its historical status; repeat the date in the block body. The check derives the last full LANE_TIP in each receipt and compares each corresponding table cell, then forbids the old `stamped `d181e16b`, clean` assertion anywhere in SCORECARD. Other d181e16b references can remain only as historical commit references; the old commit genuinely exists and must not be blindly erased.

### R78-D3 — close `LOG.md`

Append `### R78-D3 correction (2026-11-04)` to LOG.md: explicitly **supersedes** `ROWS total=93 open=31 blocked=1 closed=59 refused=2` at both old locations; quote `ROWS total=98 open=31 blocked=1 closed=64 refused=2` and full historical `bbf4f36cdfb6b8d6afc64db6416a89f60a04db72` from the actual committed receipt. Produce and track corpus/evidence/round79/routed-open-tip.txt from a clean measured revision containing the seven appended rows, with `R78-D3`, full LANE_TIP, TOOL plans/routed_open.py, its full TOOL_SHA, WORKTREE clean, COMMAND, EXIT 0, and actual ROWS output. The LOG correction must quote that receipt path, the exact current derived ROWS tuple and full stamped revision, explicitly labeled **measured revision** rather than receipt-carrying tip. This check compares old LOG correction against the old receipt and new receipt/LOG against independent JSONL counts. Do not manufacture a receipt.

### R78-D4 — close `corpus/lessons/round-78.md`

Append `### R78-D4 correction (2026-11-04)` to corpus/lessons/round-78.md and corpus/SOURCES.md. Each dated correction explicitly **supersedes** S254/S255 citation metadata: include `15 words`, `2322 and 2326`, and S255 `line 21`, plus the complete quote `Show untracked files. The mode parameter is used to specify the handling of untracked files.` Preserve the immutable S255 anchor field; this is the permitted dated correction naming its row, not an in-place anchor edit. The check counts words from the captured HTML lines and discovers the census quote line from bytes, not from either correction.

### R78-D5 — close `SCORECARD.md`

Append `### R78-D5 correction (2026-11-04)` to LOG.md and SCORECARD.md. State **six, not eight** named gates: R51-C1 and R77-C1 were **green at base**; R75-C1 and R76-C2 were genuinely **red**; R78-C1 and R78-C2 were **unmeasured** at the round-78 base. State 245 → 247 as **pin maintenance**, not red-to-green work for the two already-green gates. Include full measured R78-C1 stamp b47dbea88a77aeaf36f54d3756c8f1e1a8c1c845 and explain 04fdd644 as the **receipt-carrying commit**. Correct the main SCORECARD R78-C1 after cell to the actual b47dbea8 measurement, not @04fdd644. The check reads the green receipts, SURFACE 19 rows/pin and R78-C1 stamped revision. R78, not R79, names the two newly unmeasured gates in this historical correction.

### R78-D6 — close `LOG.md`

Choose the spot-check's explicitly permitted prose-correction branch, not an unobserved clean rerun. Append `### R78-D6 correction (2026-11-04)` to LOG.md and SCORECARD.md. Say this **supersedes** the `clean tree` assertion in commit 148801a6 and .ufo/reports/round-78/kengaku.md: .ufo/waves/round-78/gates-tip.txt stamps measured revision 63fb46baacc1a9b4fd43ee11bdf467ab070a6333 and **WORKTREE dirty**. Its 12 EXIT 0 observations are **not comparable** to runs over the cited clean commit. Do not edit the old receipt/report or pretend that a new clean receipt was produced. The check reads the old receipt's state and commands/exits, then requires both correction blocks to reflect those observed bytes.

### R78-D7 — close `corpus/README.md`

Add the round-78-verifier-spotcheck.md lesson/index row in corpus/README.md, and append `### R78-D7 correction (2026-11-04)` there, naming corpus/lessons/round-78-verifier-spotcheck.md, R78-D1 through R78-D7, and corpus/routed-findings.jsonl. Append exactly these seven routed rows only after their repairs hold; no existing R78 id may be duplicated. This check discovers ids from the spot-check, checks one closed row per id, exact source-line identity and real repair paths carrying the id. It deliberately does not recursively execute itself or the other checks; the frozen C2 counter separately exercises all checks.

### D6 clean-tree receipt requirements if the alternative branch is chosen

A genuine clean rerun must stamp the **full measured commit**, explicit `WORKTREE clean` backed by an empty tracked-and-untracked porcelain status before execution, the exact command(s), command cwd and relevant environment, full tool path(s)/SHA-256 values resolved at that commit, and each observed output/exit status. Write the receipt outside the measured clone, and record final status too so receipt generation does not silently make the measured worktree dirty. State the measured commit separately from the later commit carrying the receipt. A `clean` string alone cannot prove execution or cleanliness. No such receipt was produced by this seat; the selected D6 row honestly corrects the false prose instead, as §6 allows.

## Seven JSON lines ready for conditional append

`status=closed` is the requested destination state, not the state observed at base/freeze. JSON shell commands are single lines; `exec` only reconstructs a multiline stdlib check body. No check is `true`, a nonfailing grep, or a counter import.

```jsonl
{"id": "R78-D1", "class": "before-defect-breakdown", "source": "corpus/lessons/round-78-verifier-spotcheck.md:149", "opened_round": 78, "status": "closed", "close": "SCORECARD.md", "blocker": null, "check": "python3 -c 'exec('\"'\"'from pathlib import Path\\nimport re,json,collections,hashlib,sys\\nread=lambda p: Path(p).read_text()\\ndef block(p,id):\\n    t=read(p); m=re.search(r\"^### \"+id+r\" correction \\\\(2026-11-04\\\\)\\\\n(.*?)(?=^### |\\\\Z)\",t,re.M|re.S)\\n    assert m, p+\": missing dated correction \"+id\\n    return m.group(1)\\ndef need(text,items):\\n    for item in items:\\n        assert item in text, \"missing corrected fact: \"+item\\ns=read(\"corpus/evidence/round78/c2-before.txt\")\\nc=collections.Counter(re.findall(r\"^DEFECT ([A-Z-]+) \",s,re.M))\\nn=int(re.search(r\"^DEFECTS n=(\\\\d+)$\",s,re.M)[1])\\nprint(\"DERIVED\",dict(sorted(c.items())),\"sum\",sum(c.values()),\"receipt_total\",n,flush=True)\\nassert sum(c.values())==n\\nfacts=[str(c[k])+\" \"+k for k in (\"TOOL-UNNAMED\",\"COMMAND-ABSENT\",\"PASS-UNLOCATED\",\"WORKTREE-ABSENT\",\"TOOL-UNPINNED\")]\\nfor p in (\"LOG.md\",\"corpus/lessons/round-78.md\",\"SCORECARD.md\"):\\n    b=block(p,\"R78-D1\"); need(b,facts+[\"supersedes\",\"10 COMMAND-ABSENT\",\"4 PASS-UNLOCATED\",\"2 TOOL-UNPINNED\"])\\nrow=next(x for x in read(\"SCORECARD.md\").splitlines() if x.startswith(\"| **R78-C2 /\"))\\nneed(row.replace(\"`\", \"\"),[x for x in facts if not x.startswith(\"0 \")])\\nassert \"10 `COMMAND-ABSENT`\" not in row and \"2 `TOOL-UNPINNED`\" not in row\\n'\"'\"')'", "note": "Draft closure conditional on the exact repair in DebtScribeR79 report; base and freeze remain red. Re-derives receipt facts; does not import the C2 counter."}
{"id": "R78-D2", "class": "unswept-stamp-prose", "source": "corpus/lessons/round-78-verifier-spotcheck.md:158", "opened_round": 78, "status": "closed", "close": "SCORECARD.md", "blocker": null, "check": "python3 -c 'exec('\"'\"'from pathlib import Path\\nimport re,json,collections,hashlib,sys\\nread=lambda p: Path(p).read_text()\\ndef block(p,id):\\n    t=read(p); m=re.search(r\"^### \"+id+r\" correction \\\\(2026-11-04\\\\)\\\\n(.*?)(?=^### |\\\\Z)\",t,re.M|re.S)\\n    assert m, p+\": missing dated correction \"+id\\n    return m.group(1)\\ndef need(text,items):\\n    for item in items:\\n        assert item in text, \"missing corrected fact: \"+item\\nsc=read(\"SCORECARD.md\")\\nmatches=[]\\nfor k in (1,2):\\n    r=read(\"corpus/evidence/round77/c%d-after.txt\"%k)\\n    tip=re.findall(r\"^LANE_TIP ([0-9a-f]{40})$\",r,re.M)[-1]\\n    row=next(x for x in sc.splitlines() if x.startswith(\"| **R77-C%d /\"%k))\\n    print(\"DERIVED R77-C%d stamp=%s prose_matches=%s\"%(k,tip,(\\'\"'\"'stamped `\\'\"'\"'+tip[:8]+\\'\"'\"'`, clean\\'\"'\"') in row),flush=True)\\n    matches.append(\\'\"'\"'stamped `\\'\"'\"'+tip[:8]+\\'\"'\"'`, clean\\'\"'\"' in row)\\nassert all(matches), \\'\"'\"'round-77 SCORECARD stamp prose disagrees with receipts\\'\"'\"'\\nassert not re.search(r\"stamped `d181e16b`, clean\",sc)\\nb=block(\"SCORECARD.md\",\"R78-D2\"); need(b,[\"c1-after.txt\",\"c2-after.txt\",\"d181e16b\",\"historical\",\"2026-11-04\"])\\n'\"'\"')'", "note": "Draft closure conditional on the exact repair in DebtScribeR79 report; base and freeze remain red. Re-derives receipt facts; does not import the C2 counter."}
{"id": "R78-D3", "class": "at-tip-rerun-drift", "source": "corpus/lessons/round-78-verifier-spotcheck.md:165", "opened_round": 78, "status": "closed", "close": "LOG.md", "blocker": null, "check": "python3 -c 'exec('\"'\"'from pathlib import Path\\nimport re,json,collections,hashlib,sys\\nread=lambda p: Path(p).read_text()\\ndef block(p,id):\\n    t=read(p); m=re.search(r\"^### \"+id+r\" correction \\\\(2026-11-04\\\\)\\\\n(.*?)(?=^### |\\\\Z)\",t,re.M|re.S)\\n    assert m, p+\": missing dated correction \"+id\\n    return m.group(1)\\ndef need(text,items):\\n    for item in items:\\n        assert item in text, \"missing corrected fact: \"+item\\nold=read(\"corpus/evidence/round77/rerun-routed-open.txt\")\\noldrows=re.search(r\"^ROWS .+$\",old,re.M)[0]; oldtip=re.findall(r\"^LANE_TIP ([0-9a-f]{40})$\",old,re.M)[-1]\\nprint(\"DERIVED historical\",oldrows,\"LANE_TIP\",oldtip,flush=True)\\nb=block(\"LOG.md\",\"R78-D3\"); need(b,[oldrows,oldtip,\"supersedes\",\"ROWS total=93 open=31 blocked=1 closed=59 refused=2\"])\\np=\"corpus/evidence/round79/routed-open-tip.txt\"; r=read(p)\\nrows=[json.loads(x) for x in read(\"corpus/routed-findings.jsonl\").splitlines() if x.strip()]\\nc=collections.Counter(x[\"status\"] for x in rows)\\nexpected=\"ROWS total=%d open=%d blocked=%d closed=%d refused=%d\"%(len(rows),c[\"open\"],c[\"blocked\"],c[\"closed\"],c[\"refused\"])\\nprint(\"DERIVED current\",expected,flush=True)\\nneed(r,[\"R78-D3\",expected,\"WORKTREE clean\",\"EXIT 0\",\"TOOL plans/routed_open.py\",\"TOOL_SHA \"+hashlib.sha256(Path(\"plans/routed_open.py\").read_bytes()).hexdigest()])\\ntip=re.search(r\"^LANE_TIP ([0-9a-f]{40})$\",r,re.M)[1]\\nneed(b,[p,expected,tip,\"measured revision\"])\\n'\"'\"')'", "note": "Draft closure conditional on the exact repair in DebtScribeR79 report; base and freeze remain red. Re-derives receipt facts; does not import the C2 counter."}
{"id": "R78-D4", "class": "citation-metadata", "source": "corpus/lessons/round-78-verifier-spotcheck.md:171", "opened_round": 78, "status": "closed", "close": "corpus/lessons/round-78.md", "blocker": null, "check": "python3 -c 'exec('\"'\"'from pathlib import Path\\nimport re,json,collections,hashlib,sys\\nread=lambda p: Path(p).read_text()\\ndef block(p,id):\\n    t=read(p); m=re.search(r\"^### \"+id+r\" correction \\\\(2026-11-04\\\\)\\\\n(.*?)(?=^### |\\\\Z)\",t,re.M|re.S)\\n    assert m, p+\": missing dated correction \"+id\\n    return m.group(1)\\ndef need(text,items):\\n    for item in items:\\n        assert item in text, \"missing corrected fact: \"+item\\nh=read(\"corpus/evidence/round78/sources/git-status.html\").splitlines()\\nq=\" \".join(re.sub(r\"<[^>]*>\",\"\",h[i-1]).strip() for i in (2322,2326))\\nwords=len(q.split()); census=read(\"corpus/evidence/round62/class-survey.txt\").splitlines()\\nanchor=next(i for i,x in enumerate(census,1) if x.startswith(\"EXECUTED-COVERAGE \"))\\nprint(\"DERIVED S254 words=%d lines=2322,2326 S255 line=%d\"%(words,anchor),flush=True)\\nassert words==15\\nfor p in (\"corpus/lessons/round-78.md\",\"corpus/SOURCES.md\"):\\n    b=block(p,\"R78-D4\"); need(b,[\"S254\",\"S255\",str(words)+\" words\",\"2322 and 2326\",\"line \"+str(anchor),q,\"supersedes\"])\\n'\"'\"')'", "note": "Draft closure conditional on the exact repair in DebtScribeR79 report; base and freeze remain red. Re-derives receipt facts; does not import the C2 counter."}
{"id": "R78-D5", "class": "quality-base-redness", "source": "corpus/lessons/round-78-verifier-spotcheck.md:176", "opened_round": 78, "status": "closed", "close": "SCORECARD.md", "blocker": null, "check": "python3 -c 'exec('\"'\"'from pathlib import Path\\nimport re,json,collections,hashlib,sys\\nread=lambda p: Path(p).read_text()\\ndef block(p,id):\\n    t=read(p); m=re.search(r\"^### \"+id+r\" correction \\\\(2026-11-04\\\\)\\\\n(.*?)(?=^### |\\\\Z)\",t,re.M|re.S)\\n    assert m, p+\": missing dated correction \"+id\\n    return m.group(1)\\ndef need(text,items):\\n    for item in items:\\n        assert item in text, \"missing corrected fact: \"+item\\nr51=read(\"corpus/evidence/round77/rerun-r51-c1.txt\"); r77=read(\"corpus/evidence/round77/c1-after.txt\")\\nassert \"PREDICATE R51-C1 pass\" in r51 and \"DRIFT 0\" in r51 and \"NUMBER-DRIFT 0\" in r51\\nassert \"PREDICATE R77-C1 pass\" in r77 and \"DEFECTS n=0\" in r77\\nsurf=next(x for x in r77.splitlines() if x.startswith(\"SURFACE 19 \"))\\npair=re.search(r\"rows=(\\\\d+) pin=(\\\\d+)\",surf).groups()\\nafter=read(\"corpus/evidence/round78/c1-after.txt\"); tip=re.findall(r\"^LANE_TIP ([0-9a-f]{40})$\",after,re.M)[-1]\\nprint(\"DERIVED base green=R51-C1,R77-C1 rows=%s pin=%s R78-C1 measured=%s\"%(*pair,tip),flush=True)\\nfor p in (\"LOG.md\",\"SCORECARD.md\"):\\n    b=block(p,\"R78-D5\"); need(b,[\"R51-C1\",\"R77-C1\",\"green at base\",\"R75-C1\",\"R76-C2\",\"red\",\"R78-C1\",\"R78-C2\",\"unmeasured\",\"six, not eight\",\"245\",\"247\",\"pin maintenance\",tip,\"04fdd644\",\"receipt-carrying commit\"])\\nrow=next(x for x in read(\"SCORECARD.md\").splitlines() if x.startswith(\"| **R78-C1 /\"))\\nassert \"@04fdd644\" not in row\\nneed(row,[tip[:8]])\\n'\"'\"')'", "note": "Draft closure conditional on the exact repair in DebtScribeR79 report; base and freeze remain red. Re-derives receipt facts; does not import the C2 counter."}
{"id": "R78-D6", "class": "dirty-clean-claim", "source": "corpus/lessons/round-78-verifier-spotcheck.md:184", "opened_round": 78, "status": "closed", "close": "LOG.md", "blocker": null, "check": "python3 -c 'exec('\"'\"'from pathlib import Path\\nimport re,json,collections,hashlib,sys\\nread=lambda p: Path(p).read_text()\\ndef block(p,id):\\n    t=read(p); m=re.search(r\"^### \"+id+r\" correction \\\\(2026-11-04\\\\)\\\\n(.*?)(?=^### |\\\\Z)\",t,re.M|re.S)\\n    assert m, p+\": missing dated correction \"+id\\n    return m.group(1)\\ndef need(text,items):\\n    for item in items:\\n        assert item in text, \"missing corrected fact: \"+item\\nr=read(\".ufo/waves/round-78/gates-tip.txt\")\\ntip=re.findall(r\"^LANE_TIP ([0-9a-f]{40})$\",r,re.M)[-1]; state=re.findall(r\"^WORKTREE (.+)$\",r,re.M)[-1]\\ncommands=re.findall(r\"^## (.+)$\",r,re.M); exits=re.findall(r\"^EXIT (\\\\d+)$\",r,re.M)\\nprint(\"DERIVED original measured=%s WORKTREE %s commands=%d exits=%s\"%(tip,state,len(commands),dict(collections.Counter(exits))),flush=True)\\nassert state==\"dirty\" and len(commands)==len(exits)\\nfor p in (\"LOG.md\",\"SCORECARD.md\"):\\n    b=block(p,\"R78-D6\"); need(b,[\".ufo/waves/round-78/gates-tip.txt\",tip,\"WORKTREE \"+state,\"supersedes\",\"clean tree\",\"not comparable\",\"148801a6\",\".ufo/reports/round-78/kengaku.md\"])\\n'\"'\"')'", "note": "Draft closure conditional on the exact repair in DebtScribeR79 report; base and freeze remain red. Uses the permitted prose-correction branch; no clean rerun claimed."}
{"id": "R78-D7", "class": "closure-artifact-index", "source": "corpus/lessons/round-78-verifier-spotcheck.md:189", "opened_round": 78, "status": "closed", "close": "corpus/README.md", "blocker": null, "check": "python3 -c 'exec('\"'\"'from pathlib import Path\\nimport re,json,collections,hashlib,sys\\nread=lambda p: Path(p).read_text()\\ndef block(p,id):\\n    t=read(p); m=re.search(r\"^### \"+id+r\" correction \\\\(2026-11-04\\\\)\\\\n(.*?)(?=^### |\\\\Z)\",t,re.M|re.S)\\n    assert m, p+\": missing dated correction \"+id\\n    return m.group(1)\\ndef need(text,items):\\n    for item in items:\\n        assert item in text, \"missing corrected fact: \"+item\\nspot=\"corpus/lessons/round-78-verifier-spotcheck.md\"; s=read(spot)\\nids=re.findall(r\"^- \\\\*\\\\*(R78-D\\\\d+) \\\\([a-z]+\\\\)\",s,re.M)\\nrows=[json.loads(x) for x in read(\"corpus/routed-findings.jsonl\").splitlines() if x.strip()]\\nselected=[r for r in rows if r.get(\"id\") in ids]\\nindexed=\"round-78-verifier-spotcheck.md\" in read(\"corpus/README.md\")\\nprint(\"DERIVED ids=%d registered=%d indexed=%s\"%(len(ids),len(selected),indexed),flush=True)\\nassert indexed and len(selected)==len(ids) and collections.Counter(r[\"id\"] for r in selected)==collections.Counter(ids)\\nfor r in selected:\\n    assert r[\"status\"]==\"closed\" and r.get(\"check\",\"\").strip() not in (\"\",\"true\",\":\")\\n    source,line=r[\"source\"].rsplit(\":\",1)\\n    assert source==spot and r[\"id\"] in s.splitlines()[int(line)-1]\\n    close=r[\"close\"]; assert close!=spot and Path(close).is_file() and r[\"id\"] in read(close)\\nb=block(\"corpus/README.md\",\"R78-D7\"); need(b,[spot,\"R78-D1\",\"R78-D7\",\"corpus/routed-findings.jsonl\"])\\n'\"'\"')'", "note": "Draft closure conditional on the exact repair in DebtScribeR79 report; base and freeze remain red. Re-derives receipt facts; does not import the C2 counter."}
```

## Base failure outputs and freeze observations

The following are exact stdout lines and the final stderr exception line (Python traceback source echoes omitted). Each command is the exact `check` in its JSON row above. All relevant input bytes were from the named `git archive` extraction.

### R78-D1

**base 660ec0b9**, rc 1:

```text
DERIVED {'COMMAND-ABSENT': 11, 'PASS-UNLOCATED': 5, 'TOOL-UNNAMED': 11, 'WORKTREE-ABSENT': 2} sum 29 receipt_total 29
AssertionError: LOG.md: missing dated correction R78-D1
```

**freeze 5d6843134017780c045e92eed4e83264188a7d47**, rc 1:

```text
DERIVED {'COMMAND-ABSENT': 11, 'PASS-UNLOCATED': 5, 'TOOL-UNNAMED': 11, 'WORKTREE-ABSENT': 2} sum 29 receipt_total 29
AssertionError: LOG.md: missing dated correction R78-D1
```

### R78-D2

**base 660ec0b9**, rc 1:

```text
DERIVED R77-C1 stamp=cd2e25bb80cf618135cc001193df13966ef1c711 prose_matches=False
DERIVED R77-C2 stamp=cd2e25bb80cf618135cc001193df13966ef1c711 prose_matches=False
AssertionError: round-77 SCORECARD stamp prose disagrees with receipts
```

**freeze 5d6843134017780c045e92eed4e83264188a7d47**, rc 1:

```text
DERIVED R77-C1 stamp=cd2e25bb80cf618135cc001193df13966ef1c711 prose_matches=False
DERIVED R77-C2 stamp=cd2e25bb80cf618135cc001193df13966ef1c711 prose_matches=False
AssertionError: round-77 SCORECARD stamp prose disagrees with receipts
```

### R78-D3

**base 660ec0b9**, rc 1:

```text
DERIVED historical ROWS total=98 open=31 blocked=1 closed=64 refused=2 LANE_TIP bbf4f36cdfb6b8d6afc64db6416a89f60a04db72
AssertionError: LOG.md: missing dated correction R78-D3
```

**freeze 5d6843134017780c045e92eed4e83264188a7d47**, rc 1:

```text
DERIVED historical ROWS total=98 open=31 blocked=1 closed=64 refused=2 LANE_TIP bbf4f36cdfb6b8d6afc64db6416a89f60a04db72
AssertionError: LOG.md: missing dated correction R78-D3
```

### R78-D4

**base 660ec0b9**, rc 1:

```text
DERIVED S254 words=15 lines=2322,2326 S255 line=21
AssertionError: corpus/lessons/round-78.md: missing dated correction R78-D4
```

**freeze 5d6843134017780c045e92eed4e83264188a7d47**, rc 1:

```text
DERIVED S254 words=15 lines=2322,2326 S255 line=21
AssertionError: corpus/lessons/round-78.md: missing dated correction R78-D4
```

### R78-D5

**base 660ec0b9**, rc 1:

```text
DERIVED base green=R51-C1,R77-C1 rows=245 pin=245 R78-C1 measured=b47dbea88a77aeaf36f54d3756c8f1e1a8c1c845
AssertionError: LOG.md: missing dated correction R78-D5
```

**freeze 5d6843134017780c045e92eed4e83264188a7d47**, rc 1:

```text
DERIVED base green=R51-C1,R77-C1 rows=245 pin=245 R78-C1 measured=b47dbea88a77aeaf36f54d3756c8f1e1a8c1c845
AssertionError: LOG.md: missing dated correction R78-D5
```

### R78-D6

**base 660ec0b9**, rc 1:

```text
DERIVED original measured=63fb46baacc1a9b4fd43ee11bdf467ab070a6333 WORKTREE dirty commands=12 exits={'0': 12}
AssertionError: LOG.md: missing dated correction R78-D6
```

**freeze 5d6843134017780c045e92eed4e83264188a7d47**, rc 1:

```text
DERIVED original measured=63fb46baacc1a9b4fd43ee11bdf467ab070a6333 WORKTREE dirty commands=12 exits={'0': 12}
AssertionError: LOG.md: missing dated correction R78-D6
```

### R78-D7

**base 660ec0b9**, rc 1:

```text
DERIVED ids=7 registered=0 indexed=False
AssertionError
```

**freeze 5d6843134017780c045e92eed4e83264188a7d47**, rc 1:

```text
DERIVED ids=7 registered=0 indexed=False
AssertionError
```

## Findings, provenance, and limits

- D1 independently yields COMMAND-ABSENT=11, PASS-UNLOCATED=5, TOOL-UNNAMED=11, WORKTREE-ABSENT=2, total 29; absent TOOL-UNPINNED derives as zero. Both immutable trees retain the false split.
- D2 both immutable receipts stamp cd2e25bb80cf618135cc001193df13966ef1c711, while both main SCORECARD rows retain the incompatible d181e16b attribution.
- D3 the historical receipt itself yields total=98/open=31/blocked=1/closed=64/refused=2 at bbf4f36c, not the LOG's 93/31/1/59/2. The draft also requires a new actual receipt; that part has not executed and cannot be declared green.
- D4 the capture yields 15 words at lines 2322 and 2326; the census quote line is 21. The correction check does not count words in the correction itself.
- D5 inherited receipts contain the two green predicates and SURFACE 19 rows=245 pin=245. The R78-C1 receipt stamps b47dbea8, not its carrying commit 04fdd644. The requested red/unmeasured categorization is recorded as historical correction content, not newly executed gate results. The 247 maintenance destination is prescribed by the routed defect, not independently recounted by this check.
- D6 the committed old gate block has WORKTREE dirty and 12 command/EXIT-0 pairs. That is evidence of those recorded observations, not proof that their underlying gates hold at a clean commit.
- D7 both trees have seven routed spot-check ids, zero matching ledger rows, and no index reference. Its check validates row/evidence shape but intentionally delegates actual seven-check execution to the frozen C2 counter, avoiding recursion.
- These are document-and-receipt checks, not protection against an adversary fabricating entire committed receipts. No positive repaired fixture or landing revision was executed. The base/freeze failures alone do not prove successful closure, and formatting-sensitive marker failures are identified explicitly above rather than upgraded to substantive repair proof.

Mutable working-file conflict observed while locating existing conventions, quoted verbatim for the canonical judge (not frozen-revision execution evidence): `SCORECARD.md:3703` said `genuinely red gates were R75-C1 and R76-C2 and R79-C1/R79-C2 were unmeasured then; the 245 → 247 pin`. The historical newly unmeasured round-78 gates are R78-C1/R78-C2, not R79-C1/R79-C2. This seat did not edit or judge that sibling-owned text.

## Touched surfaces and exclusions

Only this report was permanently written: `.ufo/waves/round-79/w1/DebtScribeR79.md`. Temporary extracted trees were owned under `/fast/scratch/hyaku/kengaku-r79/DebtScribeR79/` and removed before return. Product code, ledger, LOG, SCORECARD, sources, lessons, index and old reports were read-only. No commits, pushes, deployments, judge invocation, counter execution, runtime dispatch, subagents or peer messages. No tools installed or updated.

No C1 ledger verification, mutation battery, full routed-open observation, or lane-wide gate run was attempted; these are outside this scribe item. Main integration must run the seven exact checks after actual repairs and the frozen C2 counter/batteries, preserving the required base-red/landing-green evidence.

## Self-evaluation

Accuracy 4/5: all numerical observations quoted above came from the two archived trees; no landing-green evidence exists. Completeness 4/5: all seven repairs, rows, checks and base/freeze failures provided; positive repair behavior remains unexercised because this is a read-only drafting seat. Clarity 4/5: conditional closure is explicit, but long JSON-escaped commands are inherently dense. Actionability 4/5: exact repair formats and executable rows supplied; integration must land real artifacts first. Conciseness 4/5: repeated freeze output is retained for auditability. Mean 4.0. Highest-impact improvement at integration: supply real repaired-tip receipts and exercise these checks, rather than interpreting this draft as closure. Would the user agree? The open distinction between draft and execution is essential here.
