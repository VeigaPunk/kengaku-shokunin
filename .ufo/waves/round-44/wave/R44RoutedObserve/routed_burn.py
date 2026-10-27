#!/usr/bin/env python3
"""Burn-down per round from the git history of corpus/routed-findings.jsonl (read-only; run in a clone).
round = N of the commit subject `round-N:`; several commits of one round are merged.
  opened  = ids first present in the round's commits with status open|blocked (rows born closed/refused counted in born_closed)
  closed  = ids that were open|blocked at any point up to the round's last commit (carried in or opened that round) and are closed|refused after it
  open    = routed_open after the round (open+blocked), oldest = min opened_round among them, age = round - oldest
Usage: routed_burn.py --lane DIR [--round-now N]"""
import argparse, collections, json, re, subprocess
ap = argparse.ArgumentParser(); ap.add_argument("--lane", required=True); ap.add_argument("--round-now", type=int, default=0)
a = ap.parse_args(); F = "corpus/routed-findings.jsonl"
def git(*x): return subprocess.run(["git", "-C", a.lane, *x], capture_output=True, text=True, check=True).stdout
def rows(rev):
    out = {}
    for l in git("show", f"{rev}:{F}").splitlines():
        if l.strip(): r = json.loads(l); out[r["id"]] = r
    return out
by_round = collections.OrderedDict()
for ln in git("log", "--reverse", "--format=%h|%s", "--", F).splitlines():
    h, s = ln.split("|", 1); m = re.match(r"round-(\d+):", s)
    by_round.setdefault(int(m.group(1)), []).append(h)
OPEN = ("open", "blocked"); prev = {}
print("routed_burn round opened born_closed closed refused open oldest age")
for rnd, hs in by_round.items():
    cur = rows(hs[-1])
    new = [i for i in cur if i not in prev]
    opened = sum(cur[i]["status"] in OPEN or any(rows(h).get(i, {}).get("status") in OPEN for h in hs) for i in new)
    born_closed = len(new) - opened
    snaps = [rows(h) for h in hs]
    was_open = lambda i: (i in prev and prev[i]["status"] in OPEN) or any(sn.get(i, {}).get("status") in OPEN for sn in snaps)
    closed = sum(1 for i in cur if was_open(i) and cur[i]["status"] == "closed")
    refused = sum(1 for i in cur if was_open(i) and cur[i]["status"] == "refused")
    op = [r["opened_round"] for r in cur.values() if r["status"] in OPEN]
    o = min(op) if op else None
    print(f"routed_burn round={rnd} opened={opened} born_closed={born_closed} closed={closed} refused={refused} open={len(op)} oldest={o if o else '-'} age={rnd - o if o else '-'} commits={','.join(hs)}")
    prev = cur
if a.round_now:
    op = [r["opened_round"] for r in prev.values() if r["status"] in OPEN]
    print(f"routed_burn round={a.round_now} (tip, no ledger commit yet) open={len(op)} oldest={min(op)} age={a.round_now - min(op)}")
    c = collections.Counter(r["opened_round"] for r in prev.values() if r["status"] in OPEN)
    print("open by opened_round:", dict(sorted(c.items())))
