"""Round-45 C1 control fence: refuses any fixture holding a git repository anywhere (a lazy 'no repos' fence)."""
import os


def breach(d, argv, tool):
    for _top, dirs, files in os.walk(d):
        if ".git" in dirs or ".git" in files:
            return "control: a repository is present"
    return None
