"""Control fence: REFUSES every fixture. Must fail the R50-C1 predicate on HONEST (126 over-refusals)."""


def breach(d, argv, tool):
    return "refuse-all control"
