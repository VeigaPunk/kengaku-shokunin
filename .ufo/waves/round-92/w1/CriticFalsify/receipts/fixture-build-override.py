import json, os, subprocess, sys, pathlib
FX = pathlib.Path(os.environ["FXROOT"])
GIT_ENV = {"PATH": "/usr/bin:/bin", "HOME": str(FX), "LC_ALL": "C",
           "GIT_AUTHOR_NAME": "fx", "GIT_AUTHOR_EMAIL": "fx@invalid",
           "GIT_COMMITTER_NAME": "fx", "GIT_COMMITTER_EMAIL": "fx@invalid"}
(FX / "shokunin.conf").write_text('LANES="\nkama|.|serving\nkengaku|.|eval\n"\n', encoding="utf-8")
notes = "# notes\nsome anchor line\n"
base = {"id": "OLD-1", "class": "x", "source": "notes.md:2", "opened_round": 39, "status": "open",
        "close": None, "blocker": None, "check": "grep -q anchor notes.md", "owner": None}
def seeds():
    return [dict(base, id="SEED-%d" % n, check=None, opened_round=88, status="refused", blocker="L0")
            for n in range(1, 7)]
cases = {
  # M10(b) as written: an override check must share >=1 path token with close/source/base check.
  "override-true": dict(base, id="OVR-T", status="closed", supersedes="OLD-1", close="re-run at tip",
                        check="true", override_reason="base check stale"),
  # same hole with `:`
  "override-colon": dict(base, id="OVR-C", status="closed", supersedes="OLD-1", close="re-run at tip",
                         check=":", override_reason="base check stale"),
  # control: a non-override closed row with check `true` must be flagged closed-check-vacuous
  "plain-closed-true": dict(base, id="PLN-T", status="closed", supersedes="OLD-1", close="inspected",
                            check="true"),
}
for name, row in cases.items():
    d = FX / name
    (d / "corpus").mkdir(parents=True, exist_ok=True) if False else None
    d.mkdir(parents=True, exist_ok=True)
    (d / "notes.md").write_text(notes, encoding="utf-8")
    (d / "corpus").mkdir(exist_ok=True)
    rows = [base, row] + seeds()
    (d / "corpus" / "routed-findings.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    for a in (["init", "-q", "-b", "main"], ["add", "-A"], ["commit", "-q", "--allow-empty", "-m", "fx"]):
        p = subprocess.run(["git", "-C", str(d), *a], capture_output=True, env=GIT_ENV)
        assert p.returncode == 0, (name, a, p.stderr)
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top == str(d), (top, d)
print("BUILT", sorted(cases))
