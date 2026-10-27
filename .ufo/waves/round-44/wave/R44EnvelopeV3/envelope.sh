#!/usr/bin/env bash
# Round-44 L1 envelope v3 (supersedes round-43 claims/envelope.sh; routed finding R43ReviewEnvelope F1+F2). Host home
# read-only, scratch the only writable tree besides /tmp, a scratch-backed overlay on ~/.cache (uv's lock), the envelope
# line and start/end `date +%T`.
#   What v3 changes: the watched-tree digest is one stat line per entry, recursing without following symlinks:
#     <path> <d|f|l|p|s|b|c> <octal perm bits> <nlink> <size> <mtime_ns> <ctime_ns> <ino> <link target|->
#            <xattr digest|-> <content sha256|unreadable:<errno>|n/a>
#   so a mode-only flip (F1) and a rewrite of an unreadable entry (F2) both change the digest, and so does an xattr
#   change, a nested change below the top level, or a retarget of a symlinked watched path. Every field is JSON-quoted
#   where it can carry arbitrary bytes, so a name holding a tab or newline cannot forge a column. A `CHANGED` digest
#   marks the measurement it brackets invalid (the script then exits 4 whatever the command returned); a digest that
#   cannot be taken at all (no python3, watched path not a directory while present, python error) is INVALID too
#   instead of silently equal. The command's own status propagates only when the digest is unchanged. A watched path
#   that does not exist at all digests as `absent` (round-43 parity: no tree, no change).
#   usage: envelope.sh <scratch dir> <command...>      (stdout is the receipt; redirect it outside)
#   ENVELOPE_BINDIR names the watched directory (default /home/vgpnk/.local/bin; rehearsal/self-test only). The resolved
#   path is printed on the start line, so a redirected watch is visible in the receipt.
set -u
[ $# -ge 2 ] || { printf 'usage: %s <scratch dir> <command...>\n' "$0" >&2; exit 2; }
SCR=$1; shift
BINDIR=${ENVELOPE_BINDIR:-/home/vgpnk/.local/bin}
mkdir -p "$SCR/home-cache"
ENV=(/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind "$SCR" "$SCR"
     --bind "$SCR/home-cache" /home/vgpnk/.cache
     --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)

digest_body() {
  [ -e "$BINDIR" ] || [ -L "$BINDIR" ] || { printf 'absent\n'; return 0; }
  python3 -I - "$BINDIR" <<'PY'
import hashlib, json, os, stat, sys

root = sys.argv[1]
out = sys.stdout
try:
    root_st = os.lstat(root)
except OSError as exc:
    sys.stderr.write("envelope: cannot stat %s: %s\n" % (root, exc))
    raise SystemExit(3)
root_link = "-"
if stat.S_ISLNK(root_st.st_mode):
    try:
        root_link = os.readlink(root)
    except OSError as exc:
        root_link = "link-err:" + exc.__class__.__name__
root_dir = os.path.realpath(root)
if not os.path.isdir(root_dir):
    sys.stderr.write("envelope: watched path is not a directory: %s\n" % root)
    raise SystemExit(3)

KINDS = ((stat.S_ISDIR, "d"), (stat.S_ISREG, "f"), (stat.S_ISLNK, "l"), (stat.S_ISFIFO, "p"),
         (stat.S_ISSOCK, "s"), (stat.S_ISBLK, "b"), (stat.S_ISCHR, "c"))


def esc(text):
    return json.dumps(text, ensure_ascii=True)


def xattr_sig(path):
    try:
        names = sorted(os.listxattr(path, follow_symlinks=False))
    except OSError as exc:
        return "x-err:" + (exc.strerror or exc.__class__.__name__).replace(" ", "_")
    if not names:
        return "-"
    digest = hashlib.sha256()
    for name in names:
        try:
            value = os.getxattr(path, name, follow_symlinks=False)
        except OSError as exc:
            value = b"!" + (exc.strerror or exc.__class__.__name__).encode()
        digest.update(name.encode("utf-8", "surrogateescape") + b"\0" + value + b"\0")
    return digest.hexdigest()


def content_sig(path):
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        # stat-only record: the caller's stat fields still separate two different rewrites of this entry
        return "unreadable:" + (exc.strerror or exc.__class__.__name__).replace(" ", "_")
    try:
        digest = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                return digest.hexdigest()
            digest.update(chunk)
    finally:
        os.close(fd)


out.write("envelope-digest v3 root=%s link=%s ino=%s mode=%04o\n"
          % (esc(root_dir), esc(root_link), root_st.st_ino, stat.S_IMODE(root_st.st_mode)))

stack = [("", root_dir)]
while stack:
    rel, full = stack.pop()
    label = esc(rel if rel else ".")
    try:
        st = os.lstat(full)
    except OSError as exc:
        out.write("\t".join([label, "VANISHED", exc.__class__.__name__]) + "\n")
        continue
    kind = next((tag for test, tag in KINDS if test(st.st_mode)), "?")
    fields = [label, kind, "%04o" % stat.S_IMODE(st.st_mode), str(st.st_nlink), str(st.st_size),
              str(st.st_mtime_ns), str(st.st_ctime_ns), str(st.st_ino)]
    if kind == "l":
        try:
            fields.append(esc(os.readlink(full)))
        except OSError as exc:
            fields.append("link-err:" + exc.__class__.__name__)
    else:
        fields.append("-")
    fields.append(xattr_sig(full))
    fields.append(content_sig(full) if kind == "f" else "n/a")
    out.write("\t".join(fields) + "\n")
    if kind != "d":
        continue
    try:
        names = sorted(os.listdir(full), reverse=True)
    except OSError as exc:
        out.write("\t".join([label, "LIST-ERR", exc.__class__.__name__]) + "\n")
        continue
    for name in names:
        stack.append((name if not rel else rel + "/" + name, os.path.join(full, name)))
PY
}

snapshot() {   # digest of the watched tree; return 1 when it could not be taken
  local body rc
  body=$(digest_body); rc=$?
  if [ "$rc" -ne 0 ]; then
    printf 'DIGEST-ERROR rc=%s\n%s\n' "$rc" "$body"
    return 1
  fi
  printf '%s\n' "$body" | LC_ALL=C sha256sum | cut -c1-16
}

before=$(snapshot); before_rc=$?
echo "ENVELOPE ${ENV[*]} -- $*"
echo "ENVELOPE start $(date +%T) cwd=$PWD bindir=$BINDIR digest=v3"
"${ENV[@]}" "$@"
rc=$?
after=$(snapshot); after_rc=$?
if [ "$before_rc" -ne 0 ] || [ "$after_rc" -ne 0 ]; then
  echo "ENVELOPE end $(date +%T) exit=$rc local_bin_content_before=$before after=$after digest_error"
  echo "ENVELOPE measurement INVALID (digest could not be taken: before_rc=$before_rc after_rc=$after_rc)"
  exit 4
fi
if [ "$before" = "$after" ]; then st=unchanged; else st=CHANGED; fi
echo "ENVELOPE end $(date +%T) exit=$rc local_bin_content_before=$before after=$after $st"
[ "$st" = CHANGED ] && { echo "ENVELOPE measurement INVALID (PATH dir content changed while it ran)"; exit 4; }
exit $rc
