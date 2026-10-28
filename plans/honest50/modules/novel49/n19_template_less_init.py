"""Round-49 C1 NEW honest class `n19_template_less_init`: a default `core.hooksPath` with no hook file at all.

New in round 49 (not one of the nine round-46 classes nor the seven round-48 ones). Every other class here was
created by plain `git init`, whose template installs `.git/hooks/*.sample` and `.git/info/exclude`; this class is
created with `--template <empty dir>`, the state `git init --template=` / `init.templateDir=` produces (a common
way to skip sample hooks). The config carries no `core.hooksPath` key, so git's default hooks directory applies,
and no hook file exists in it — not even a sample. The class exists so a fence cannot pass its hook check by
requiring the sample set to be present.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ round-49 stage-1 freeze
`9d2900af`, sha256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` as pinned by this
population's builder), never against a repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and
returns the argv tail.
"""


def build(ctx, d):
    (d / "template").mkdir()
    ctx.sh("git", "init", "-q", "-b", "master", "--template", "template", "repo", cwd=d)
    ctx.sh("rmdir", "template", cwd=d)
    r = d / "repo"
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n19-template-less-init", "tool": "anchor", "expect": None, "defects": None, "build": build}]
