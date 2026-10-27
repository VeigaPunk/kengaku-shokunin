"""Round-45 C1 control fence (instrument2): crashes (ERROR verdict) on every refusals45 fixture,
admits every honest fixture — a fence that fails open by crashing on the hostile side only."""


def breach(d, argv, tool):
    if "refusals45" in str(d):
        raise RuntimeError("control: crash on hostile fixture")
    return None
