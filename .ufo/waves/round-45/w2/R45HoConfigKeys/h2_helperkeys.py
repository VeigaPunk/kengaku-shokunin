"""Held-out hostile module h2_helperkeys (R45HoConfigKeys, kengaku round-45 wave 2): executable/helper config
keys naming a command outside the fixture without any include — `credential.helper` and `gpg.program` relative
(the counter pins gpg.program=/bin/true only in its own env; the fence's `.git/config*` scan checks neither) —
plus `user.useConfigOnly`, which names no path but forbids identity-less commits for any consumer that commits.
The repo IS the fixture dir; the artefacts sit under `pathlib.Path(d).parent` (the module build root). All
fixtures are expected to be ADMITTED by the landed fence: none of these keys is scanned or probed."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"
FIRE = "#!/bin/sh\necho fired \"$0\" \"$*\" >> \"$(dirname \"$0\")/fired.log\" 2>/dev/null\nexit 0\n"


def _repo(ctx, d):
    r = ctx.init(d)
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def _evil(ctx, d, name, text, exe=False):
    p = pathlib.Path(d).parent / "evil" / name
    ctx.write(p, text)
    if exe:
        ctx.sh("chmod", "+x", str(p))
    return p


def _key(ctx, r, key, val):
    ctx.sh("git", "-C", str(r), "config", key, val)


def _order():
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", RECEIPT]


def b_baseline(ctx, d):
    _repo(ctx, d)
    return _order()


def b_cred(ctx, d):
    r = _repo(ctx, d)
    _evil(ctx, d, "cred", FIRE, exe=True)
    _key(ctx, r, "credential.helper", "../evil/cred")
    return _order()


def b_gpg(ctx, d):
    r = _repo(ctx, d)
    _evil(ctx, d, "gpg", FIRE, exe=True)
    _key(ctx, r, "gpg.program", "../evil/gpg")
    return _order()


def b_uco(ctx, d):
    """No user.email in the repo config: user.useConfigOnly=true makes any identity-less commit fail.
    The build commits earlier carry the builder's env identity, so the key is set after them."""
    r = _repo(ctx, d)
    _key(ctx, r, "user.useConfigOnly", "true")
    return _order()


FIXTURES = [
    {"fid": "h2-baseline", "tool": "order", "expect": "accept", "defects": [], "build": b_baseline},
    {"fid": "h2-cred", "tool": "order", "expect": "accept", "defects": [], "build": b_cred},
    {"fid": "h2-gpg", "tool": "order", "expect": "accept", "defects": [], "build": b_gpg},
    {"fid": "h2-uco", "tool": "order", "expect": "accept", "defects": [], "build": b_uco},
]
