"""Control fence: name/shape-keyed, not boundary-keyed — the round-45 Q39 failure mode.

It refuses on the *shape names* a hostile fixture usually carries (a `.git` file, an `alternates` file, a
`commondir` file, a symlink) and admits everything else, without resolving any target. It should therefore refuse
the out-of-`d` refusals AND the in-`d` honest counterparts, i.e. fail HONEST while passing REFUSALS: proof that an
honest leg with in-`d` indirection classes is what distinguishes boundary reasoning from shape matching.
"""
import os
import stat


def _walk(root):
    for top, dirs, files in os.walk(root):
        for name in list(dirs) + list(files):
            yield os.path.join(top, name)


def breach(d, argv, tool):
    for p in _walk(str(d)):
        try:
            st = os.lstat(p)
        except OSError:
            continue
        if stat.S_ISLNK(st.st_mode):
            return "keyed: symlink"
        if os.path.basename(p) == ".git" and stat.S_ISREG(st.st_mode):
            return "keyed: gitfile"
        if os.path.basename(p) == "alternates":
            return "keyed: alternates"
        if os.path.basename(p) == "commondir":
            return "keyed: commondir"
    return None
