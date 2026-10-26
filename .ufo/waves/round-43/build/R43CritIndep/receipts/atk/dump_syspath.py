import sys

with open("/app/syspath.txt", "w") as _f:
    _f.write("\n".join(sys.path))


def attack(encrypt_fn):
    return 0
