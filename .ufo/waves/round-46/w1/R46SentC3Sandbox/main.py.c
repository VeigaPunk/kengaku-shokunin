#if 0
'''
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <signal.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>

static void lim(const char *n, int r) {
  struct rlimit rl;
  if (getrlimit(r, &rl) != 0) { printf("LIMIT %s errno=%d\n", n, errno); return; }
  printf("LIMIT %s soft=%llu hard=%llu\n", n,
         (unsigned long long)rl.rlim_cur, (unsigned long long)rl.rlim_max);
}

static void mark(const char *tag, const char *path) {
  int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
  if (fd < 0) { printf("WRITE %s errno=%d %s path=%s\n", tag, errno, strerror(errno), path); return; }
  ssize_t w = write(fd, "M", 1);
  int e = errno;
  close(fd);
  printf("WRITE %s ok=%d n=%ld errno=%d path=%s\n", tag, (w == 1), (long)w, (w == 1 ? 0 : e), path);
}

static void net(const char *ip, int port) {
  int s = socket(AF_INET, SOCK_STREAM, 0);
  if (s < 0) { printf("NET %s:%d socket=FAIL errno=%d\n", ip, port, errno); return; }
  struct sockaddr_in a;
  memset(&a, 0, sizeof a);
  a.sin_family = AF_INET;
  a.sin_port = htons(port);
  inet_pton(AF_INET, ip, &a.sin_addr);
  int rc = connect(s, (struct sockaddr *)&a, sizeof a);
  printf("NET %s:%d connect_rc=%d errno=%d %s\n", ip, port, rc, rc ? errno : 0,
         rc ? strerror(errno) : "CONNECTED");
  close(s);
}

static void forks(int n) {
  int ok = 0, fail = 0, last = 0;
  for (int i = 0; i < n; i++) {
    pid_t p = fork();
    if (p < 0) { fail++; last = errno; }
    else if (p == 0) { usleep(200000); _exit(0); }
    else ok++;
  }
  int st;
  while (wait(&st) > 0) { }
  printf("FORK requested=%d ok=%d fail=%d errno_last=%d\n", n, ok, fail, last);
}

int main(int argc, char **argv) {
  const char *mode = argc > 1 ? argv[1] : "safe";
  char host[256] = "?";
  gethostname(host, sizeof host - 1);
  printf("POLY lang=C mode=%s uid=%d host=%s ncpu=%ld\n", mode, (int)getuid(), host,
         sysconf(_SC_NPROCESSORS_ONLN));
  lim("CPU", RLIMIT_CPU);
  lim("NPROC", RLIMIT_NPROC);
  lim("FSIZE", RLIMIT_FSIZE);
  lim("AS", RLIMIT_AS);
  lim("CORE", RLIMIT_CORE);
  lim("NOFILE", RLIMIT_NOFILE);
  if (!strcmp(mode, "safe")) {
    mark("app", "/app/inside.txt");
    mark("tmp", "/tmp/tmp-ok.txt");
    mark("root-tmpfs", "/ESCAPE-root-tmpfs.txt");
    mark("dotdot", "../ESCAPE-dotdot.txt");
    mark("etc", "/etc/ESCAPE-etc.txt");
    mark("usr", "/usr/ESCAPE-usr.txt");
    mark("home", "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46SentC3Sandbox/ESCAPE-home.txt");
    mark("root-home", "/root/ESCAPE-root.txt");
    mark("fast", "/fast/scratch/hyaku/kengaku-r46/R46SentC3Sandbox/markers/ESCAPE-fast.txt");
    mark("proc1root", "/proc/1/root/ESCAPE-proc1.txt");
    net("1.1.1.1", 80);
    net("127.0.0.1", 22);
    forks(32);
  } else if (!strcmp(mode, "forks")) {
    forks(96);
  } else if (!strcmp(mode, "mem")) {
    size_t n = (size_t)512 << 20;
    char *p = malloc(n);
    if (!p) { printf("MEM alloc=FAIL bytes=%zu errno=%d\n", n, errno); return 0; }
    memset(p, 1, n);
    printf("MEM alloc=OK bytes=%zu\n", n);
    free(p);
  } else if (!strcmp(mode, "fill")) {
    size_t chunk = 65536, total = 0, want = (size_t)5 << 20;
    char *buf = malloc(chunk);
    memset(buf, 'x', chunk);
    int fd = open("/app/fill.bin", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) { printf("FILL open=FAIL errno=%d\n", errno); return 0; }
    while (total < want) {
      ssize_t w = write(fd, buf, chunk);
      if (w <= 0) { printf("FILL stop errno=%d written=%zu\n", errno, total); close(fd); return 0; }
      total += (size_t)w;
    }
    close(fd);
    printf("FILL ok written=%zu\n", total);
  } else if (!strcmp(mode, "bigout")) {
    size_t chunk = 8192, total = 0;
    char *buf = malloc(chunk);
    memset(buf, 'x', chunk);
    for (int i = 0; i < 1024; i++) { if (fwrite(buf, 1, chunk, stdout) != chunk) break; total += chunk; }
    printf("\nOUT written=%zu\n", total);
  } else if (!strcmp(mode, "cpu")) {
    printf("CPU start\n");
    fflush(stdout);
    volatile unsigned long x = 0;
    for (;;) { x++; }
    printf("CPU end %lu\n", x);
  }
  return 0;
}
#if 0
'''
import os
import resource
import socket
import sys
import time

mode = sys.argv[1] if len(sys.argv) > 1 else "safe"
print("POLY lang=PY mode=%s uid=%d host=%s ncpu=%d"
      % (mode, os.getuid(), socket.gethostname(), len(os.sched_getaffinity(0))))

for name in ("CPU", "NPROC", "FSIZE", "AS", "CORE", "NOFILE"):
    soft, hard = resource.getrlimit(getattr(resource, "RLIMIT_" + name))
    print("LIMIT %s soft=%d hard=%d" % (name, soft, hard))


def mark(tag, path):
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    except OSError as e:
        print("WRITE %s errno=%d %s path=%s" % (tag, e.errno, e.strerror, path))
        return
    try:
        n = os.write(fd, b"M")
    finally:
        os.close(fd)
    print("WRITE %s ok=%d n=%d errno=0 path=%s" % (tag, n == 1, n, path))


def net(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        print("NET %s:%d connect_rc=0 CONNECTED" % (ip, port))
    except OSError as e:
        print("NET %s:%d connect_rc=-1 errno=%d %s" % (ip, port, e.errno, e.strerror))
    finally:
        s.close()


def forks(n):
    kids = []
    fail = 0
    last = 0
    for _ in range(n):
        try:
            pid = os.fork()
        except OSError as e:
            fail += 1
            last = e.errno
            continue
        if pid == 0:
            time.sleep(0.2)
            os._exit(0)
        kids.append(pid)
    for pid in kids:
        os.waitpid(pid, 0)
    print("FORK requested=%d ok=%d fail=%d errno_last=%d" % (n, len(kids), fail, last))


if mode == "safe":
    mark("app", "/app/inside.txt")
    mark("tmp", "/tmp/tmp-ok.txt")
    mark("root-tmpfs", "/ESCAPE-root-tmpfs.txt")
    mark("dotdot", "../ESCAPE-dotdot.txt")
    mark("etc", "/etc/ESCAPE-etc.txt")
    mark("usr", "/usr/ESCAPE-usr.txt")
    mark("home", "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46SentC3Sandbox/ESCAPE-home.txt")
    mark("root-home", "/root/ESCAPE-root.txt")
    mark("fast", "/fast/scratch/hyaku/kengaku-r46/R46SentC3Sandbox/markers/ESCAPE-fast.txt")
    mark("proc1root", "/proc/1/root/ESCAPE-proc1.txt")
    net("1.1.1.1", 80)
    net("127.0.0.1", 22)
    forks(32)
elif mode == "forks":
    forks(96)
elif mode == "mem":
    n = 512 << 20
    try:
        b = bytearray(n)
        print("MEM alloc=OK bytes=%d" % n)
    except MemoryError:
        print("MEM alloc=FAIL bytes=%d MemoryError" % n)
elif mode == "fill":
    chunk = 65536
    total = 0
    buf = b"x" * chunk
    fd = os.open("/app/fill.bin", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        while total < (5 << 20):
            total += os.write(fd, buf)
    except OSError as e:
        print("FILL stop errno=%d written=%d" % (e.errno, total))
    else:
        print("FILL ok written=%d" % total)
    finally:
        os.close(fd)
elif mode == "bigout":
    total = 0
    chunk = b"x" * 8192
    while total < (8 << 20):
        sys.stdout.write(chunk.decode())
        total += len(chunk)
    sys.stdout.write("\nOUT written=%d\n" % total)
elif mode == "cpu":
    print("CPU start")
    sys.stdout.flush()
    x = 0
    while True:
        x += 1
#endif
