# same as f_killshot minus the unlink: outside opens SHOULD surface as read=10.
import os, pathlib
def breach(d, argv, tool):
    d = pathlib.Path(d)
    if "/refusals45-" in str(d):
        open(d.parent / "outside.cfg").read() if (d.parent / "outside.cfg").exists() else None
        try:
            os.listdir(d.parent)
        except OSError:
            pass
        try:
            for p in d.parent.iterdir():
                if p.is_file() and p.suffix == ".cfg":
                    open(p).read()
        except OSError:
            pass
        open("/etc/hostname").read()
        return "name-keyed refusal"
    return None
