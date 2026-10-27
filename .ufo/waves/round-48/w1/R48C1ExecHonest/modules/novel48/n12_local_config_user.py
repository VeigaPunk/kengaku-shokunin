"""Round-48 C1 NEW honest class `n12_local_config_user`: `[user]` identity set in `.git/config`.

New in round 48 (not one of the nine round-46 classes). `git config --local user.name/user.email` is the first
thing an ordinary clone-less `git init` user does; it appends one `[user]` section of two inert string keys to
`.git/config`. The base fence's `[core]`-only key allowlist refuses the section, which reads as over-refusal:
`user.name`/`user.email` name no path, run no program and redirect nothing outside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.git(r, "config", "--local", "user.name", "Fixture Author")
    ctx.git(r, "config", "--local", "user.email", "author@kengaku.invalid")
    ctx.write(r / "a.txt", "committed by the configured identity\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n12-local-config-user", "tool": "anchor", "expect": None, "defects": None, "build": build}]
