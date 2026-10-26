def build_dup(ctx, d):
    lane = ctx.clone(d / "lane")
    return ["--lane", str(lane)]

FIXTURES = [{"fid": "a_tok-upper-anchor", "tool": "anchor", "expect": "accept",
             "defects": [], "build": build_dup}]
