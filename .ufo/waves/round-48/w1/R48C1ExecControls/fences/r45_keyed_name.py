"""Round-45 attempt-3 L1 control fence: inspects nothing; keys the verdict on the counter-chosen fixture path
(R45CriticPredicate B2). Zero opens, zero git calls. If the frozen C1 counter passes this, the C1 target is
reachable by a control that skips the claimed work (prompt section 6 item 9)."""


def breach(d, argv, tool):
    return "keyed-on-path" if "/refusals45-" in str(d) else None
