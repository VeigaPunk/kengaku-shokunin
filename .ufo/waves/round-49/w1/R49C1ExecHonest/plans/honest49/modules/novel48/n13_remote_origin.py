"""Round-48 C1 NEW honest class `n13_remote_origin`: `[remote "origin"]` with a URL and fetch refspec.

New in round 48 (not one of the nine round-46 classes). `git remote add origin <url>` is what every repository
with a remote carries; it appends one `[remote "origin"]` section (url plus the standard fetch refspec) to
`.git/config` and performs no fetch, so no object, ref or byte outside `d` exists. The URL is a fixed
`example.invalid` https URL: the fixture is hermetic, and the read-only tools the fence gates never contact a
remote. The base fence refuses the section because only `[core]` is allowlisted; that is over-refusal for an
inert remote declaration, not protection against an outside read.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "remote", "add", "origin", "https://example.invalid/fixture/lane.git")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n13-remote-origin", "tool": "anchor", "expect": None, "defects": None, "build": build}]
