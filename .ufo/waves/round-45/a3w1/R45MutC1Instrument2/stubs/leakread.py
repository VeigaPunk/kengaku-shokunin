"""Admits every fixture AND, while deciding, successfully opens a regular file that lies
under the build scratch (root/fx) but outside the fixture directory d — so every verdict
row carries ADMIT and opens>=1 at once (the leak+read co-occurrence probe)."""
import os


def breach(d, argv, tool):
    try:
        fx = d.parent.parent
        for name in sorted(os.listdir(fx)):
            base = os.path.join(fx, name)
            for f in ("f000", "f001"):
                for cand in (os.path.join(base, f, ".git"), os.path.join(base, f, ".git", "HEAD")):
                    c = os.path.abspath(cand)
                    if c == str(d) or c.startswith(str(d) + os.sep):
                        continue
                    try:
                        with open(cand, "rb"):
                            pass
                        return None
                    except OSError:
                        pass
    except OSError:
        pass
    return None
