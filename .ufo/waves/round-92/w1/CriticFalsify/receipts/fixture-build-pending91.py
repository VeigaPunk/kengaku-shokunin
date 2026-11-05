import json, os, subprocess, pathlib
FX = pathlib.Path(os.environ["FXROOT"]); d = FX / "pending91"
GIT_ENV = {"PATH": "/usr/bin:/bin", "HOME": str(FX), "LC_ALL": "C",
           "GIT_AUTHOR_NAME": "fx", "GIT_AUTHOR_EMAIL": "fx@invalid",
           "GIT_COMMITTER_NAME": "fx", "GIT_COMMITTER_EMAIL": "fx@invalid"}
d.mkdir(parents=True, exist_ok=True); (d / "corpus").mkdir(exist_ok=True)
(d / "notes.md").write_text("# notes\nsome anchor line\n", encoding="utf-8")
base = {"id": "OPEN-91", "class": "x", "source": "notes.md:2", "opened_round": 91, "status": "open",
        "close": None, "blocker": None, "check": None, "owner": None}
seeds = [dict(base, id="SEED-%d" % n, opened_round=88, status="refused", blocker="L0") for n in range(1, 7)]
rows = [base] + seeds
(d / "corpus" / "routed-findings.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
for a in (["init", "-q", "-b", "main"], ["add", "-A"], ["commit", "-q", "--allow-empty", "-m", "fx"]):
    assert subprocess.run(["git", "-C", str(d), *a], capture_output=True, env=GIT_ENV).returncode == 0
assert subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == str(d)
(FX / "shokunin.conf").write_text('LANES="\nkama|.|serving\nkengaku|.|eval\n"\n', encoding="utf-8")
print("BUILT")
