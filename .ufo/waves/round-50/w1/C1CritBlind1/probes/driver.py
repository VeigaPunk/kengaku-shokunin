"""Scratch driver for seat R50C1CritBlind1: build the two blind modules through the FROZEN round-44 builder
contract (`Ctx`), run the FROZEN base fence against each, and check that each fixture really is a live out-of-d
escape (git itself resolves outside d) plus that the plausible naive pointer repairs admit it.

Read-only against a --shared clone of the lane at the stage-1 freeze. Everything it writes is under --work.
"""
import argparse
import importlib.util
import json
import os
import pathlib
import subprocess
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--modules", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    fence = load(lane / "plans/fixture_fence.py", "blind_fence")
    k44 = load(lane / "plans/round44_c1_verify.py", "blind_k44")

    out = {}
    for mp in sorted(pathlib.Path(a.modules).glob("*.py")):
        mod = load(mp, f"blind_mod_{mp.stem}")
        for fx in mod.FIXTURES:
            dest = work / mp.stem / fx["fid"]
            d = dest / "f000"
            d.mkdir(parents=True)
            ctx = k44.Ctx(dest)
            argv = fx["build"](ctx, d)
            rec = {"module": mp.name, "fid": fx["fid"], "tool": fx["tool"], "argv": argv,
                   "d_exists": d.is_dir(), "repos": [str(p) for p in d.rglob(".git")]}
            try:
                why = fence.breach(d, argv, fx["tool"])
                rec["fence_verdict"] = "BREACH" if why else "ADMIT"
                rec["fence_reason"] = why
            except Exception as e:                                   # noqa: BLE001
                rec["fence_verdict"] = "ERROR"
                rec["fence_reason"] = f"{type(e).__name__}: {e}"
            rec["escape"] = escape_facts(d, argv)
            rec["naive"] = naive_probes(d, argv)
            out[fx["fid"]] = rec
            del ctx
    print(json.dumps(out, indent=2))
    return 0


GITENV = {"PATH": os.environ["PATH"], "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
          "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
          "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
          "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
          "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}


def escape_facts(d, argv):
    """Does git, run exactly as the tool would run behind the fence, resolve outside d?"""
    d = pathlib.Path(d)
    lane = (d / argv[argv.index("--lane") + 1]).resolve()
    facts = {"lane_resolved": str(lane), "lane_inside_d": _inside(lane, d)}
    for label, cmd in (("absolute_git_dir", ["git", "-C", str(lane), "rev-parse", "--absolute-git-dir"]),
                       ("log", ["git", "-C", str(lane), "log", "--oneline", "--all"])):
        r = subprocess.run(cmd, env=GITENV, capture_output=True, text=True)
        facts[label] = {"rc": r.returncode, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()[-200:]}
    gd = facts["absolute_git_dir"]["stdout"]
    facts["git_dir_inside_d"] = _inside(pathlib.Path(gd), d) if gd else None
    # Is a borrowed object (present only in the outside store) actually readable through the lane?
    store = pathlib.Path(str(d) + "/../store/.git") if (pathlib.Path(str(d) + "/../store/.git").is_dir()) else None
    if store is not None:
        r = subprocess.run(["git", "--git-dir", str(store), "rev-parse", "HEAD"],
                           env=GITENV, capture_output=True, text=True)
        sha = r.stdout.strip()
        facts["store_head"] = sha
        if sha:
            rr = subprocess.run(["git", "-C", str(lane), "cat-file", "-p", sha],
                                env=GITENV, capture_output=True, text=True)
            facts["borrowed_object_readable_from_lane"] = {"rc": rr.returncode,
                                                           "stdout_head": rr.stdout.splitlines()[:4]}
            facts["borrowed_object_in_lane_odb"] = (lane / ".git" / "objects" / sha[:2] / sha[2:]).exists()
    return facts


def naive_probes(d, argv):
    """The pointer repairs a hasty fence repair would write; each returns ADMIT/REFUSE for this fixture."""
    d = pathlib.Path(d)
    out = {}
    gfile = d / ".git"
    # N1: gitfile text, normpath + prefix (no realpath).
    if gfile.is_file():
        line = gfile.read_text().strip()
        target = line.split(":", 1)[1].strip() if ":" in line else ""
        raw = target if target.startswith("/") else os.path.join(str(d), target)
        out["N1_gitfile_normpath_prefix"] = "ADMIT" if _inside(os.path.normpath(raw), d) else "REFUSE"
        out["N1_path"] = raw
        # N2: pathlib is_relative_to without resolve.
        out["N2_gitfile_is_relative_to"] = "ADMIT" if pathlib.Path(os.path.normpath(raw)).is_relative_to(d) else "REFUSE"
        # N3: realpath containment (the correct check).
        out["N3_gitfile_realpath_inside"] = "ADMIT" if _inside(pathlib.Path(os.path.normpath(raw)).resolve(), d) else "REFUSE"
    alt = d / "lane" / ".git" / "objects" / "info" / "alternates"
    if alt.is_file():
        line = alt.read_text().strip()
        out["N4_alternates_raw_prefix"] = "ADMIT" if line.startswith(str(d)) else "REFUSE"
        out["N4_line"] = line
        out["N5_alternates_is_relative_to_unresolved"] = "ADMIT" if pathlib.Path(line).is_relative_to(d) else "REFUSE"
        out["N6_alternates_normpath_prefix"] = "ADMIT" if _inside(os.path.normpath(line), d) else "REFUSE"
        out["N7_alternates_realpath_inside"] = "ADMIT" if _inside(pathlib.Path(line).resolve(), d) else "REFUSE"
        out["N8_alternates_target_exists"] = pathlib.Path(os.path.normpath(line)).is_dir()
    return out


def _inside(p, d):
    p, d = os.path.normpath(str(p)), os.path.normpath(str(d))
    return p == d or p.startswith(d + os.sep)


if __name__ == "__main__":
    sys.exit(main())
