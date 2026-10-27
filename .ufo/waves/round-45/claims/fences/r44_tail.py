

# --- round-45 control adapter: the round-44 counter's fence, in the round-44 order (build_battery) ---
def breach(d, argv, tool):
    d = pathlib.Path(d)
    return (argv_shape_breach(tool, argv) or lane_breach(d, argv) or repo_breach(d) or symlink_breach(d)
            or (order_argv_breach(d, argv) if tool == "order" else None))
