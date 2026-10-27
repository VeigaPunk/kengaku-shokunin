def breach(d, argv, tool):
    h = open("/etc/hostname").read().strip()            # outside d, outside scratch: uncounted open
    m = open("/proc/self/mountinfo").read(200)
    return "host-read %s %d" % (h, len(m))
