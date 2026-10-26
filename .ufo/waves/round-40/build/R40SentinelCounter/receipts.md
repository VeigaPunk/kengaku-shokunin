# R40SentinelCounter — receipts

Host: Arch, uid 1000, bubblewrap 0.13.1, 2026-10-26. Scratch `S=/fast/scratch/hyaku/kengaku-r40/R40SentinelCounter`
(removed after the run). Nothing in the lane was written by this seat.

## R1 — C1 sandbox argv is the frozen counter's own

```
$ sed -n '303,304p' plans/round40_c1_verify.py
def sandbox(extra_binds=()):
    argv = [BWRAP, "--dev-bind", "/", "/", "--proc", "/proc", "--unshare-pid", "--die-with-parent", "--new-session"]
```
Used at `:378` (every tool run) and `:419` (every module build).

## R2 — host-fs reach, secrets, lane git (same argv)

```
$ bwrap --dev-bind / / --proc /proc --unshare-pid --die-with-parent --new-session /bin/sh -c '...'
cwd=/home/vgpnk/Projects/shokunin
WRITE-OUTSIDE-CWD=yes
SSH-KEY-READABLE=yes (411 bytes)
LANE-GIT-INDEX-READABLE=yes
LANE-GIT-DIR-WRITABLE=yes
PINNED-TOOL-WRITABLE=yes
LANE-REF-READABLE=yes
SSH-DIR-TAR=ok
```

## R3 — network (same argv; the counter's `sandbox()` never passes `--unshare-net`)

```
host-cups CONNECT=ok
host-8796 CONNECT=ok
DNS example.com = 172.66.147.243
inet 1.1.1.1:443 CONNECT=ok
```

## R4 — persistence channels from the same sandbox

```
SSH_DIR_WRITABLE=yes (authorized_keys could be planted)
/home/vgpnk/.config/systemd/user
SYSTEMD_USER_DIR_WRITABLE=yes
BASHRC_WRITABLE=yes
COUNTER_WRITABLE=yes
```

## R5 — process escapes inside `--unshare-pid`

```
# double fork + setsid + sleep 600, then bwrap exits
host survivors: 0
# systemd-run --user --unit=sentinel-escape-probe --collect -- /bin/sleep 45  (from inside the sandbox)
Failed to connect to user scope bus via local transport: No data available
systemd-run rc=1 ; systemctl --user is-active sentinel-escape-probe -> inactive
```
So the pid namespace does kill descendants (double fork included), and the user manager is unreachable from inside
(peer-pid lookup fails across the pid namespace) — but neither matters for R2/R3/R4, which need no escape.

## R6 — hostile battery module through the frozen counter (end to end)

Module: `bat/hostile_sentinel.py` (copied beside this file), no SIDECHANNEL token:

```
$ mkdir -p "$S/hostile" && python3 plans/round40_c1_verify.py --lane "$S/lane" --battery-dir "$S/bat" --only A01 --work "$S/w"
PINS total=3 mismatched=0
FIXTURE SENTINEL-1 tool=anchor expect=error declared=- observed_rc=2 observed=- ok
MUTANT A01 anchor silence SURVIVED exhibits=none -- ...
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
counter rc=1
```
What that module did during the build (its report, `manual/f000/report.txt`):

```
WRITE_OUTSIDE_D=ok
SSH_KEY_BYTES=411
LANE_DOT_GIT_W_OK=True
LANE_PINNED_TOOL_W_OK=True
LANE_CLAIMS_W_OK=True
GIT_ADD_RC=0
GIT_COMMIT_RC=0
DECOY_REF_EXISTS=True
DECOY_REF=48723ff1ae6f
```
`tampered=0`, `sidechannel=0`, `PINS-AFTER mismatched=0` while all of the above happened.

## R7 — fixture `.git` as a symlink out of `d` is invisible to `fingerprint()`

```
$ python3 -c '... m.fingerprint(d) ...'
fingerprint= b95db572440d4de57418b12d7a9736d6bafd75ff514e229645d9e6f276004ee1
dotgit islink= True -> /fast/scratch/hyaku/kengaku-r40/R40SentinelCounter/decoy-repo/.git
```
The same run committed into the decoy repo (R6 `DECOY_REF=48723ff1ae6f`) and still reported `tampered=0`.

## R8 — `path_ok()` accepts relative traversal

```
'../../../../../../home/vgpnk/.ssh/id_ed25519' path_ok= True
'/home/vgpnk/.ssh/id_ed25519'                  path_ok= False
'..'                                           path_ok= True
'--lane=/home/vgpnk'                           path_ok= False
```

## R9 — no instrument verifies the freeze digests

```
$ find . -name frozen-digests.txt -not -path './.git/*'
./.ufo/waves/round-37/claims/frozen-digests.txt
./.ufo/waves/round-38/claims/frozen-digests.txt
./.ufo/waves/round-39/claims/frozen-digests.txt
./.ufo/waves/round-40/claims/frozen-digests.txt    (11 lines; every digest re-verified ok)
$ grep -rn "frozen-digests" plans/*.py
(no output)
```

## R10 — candidate tightened sandbox, validated for the counter's primitives

```
$ bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind "$T" "$T" \
        --unshare-pid --unshare-net --unshare-ipc --die-with-parent --new-session python3 -c '...'
TIGHT write_outside = OSError
TIGHT write_inside = ok
TIGHT clone_shared_rc = 0
TIGHT dest_write = ok
TIGHT git_add_rc = 0
TIGHT git_commit_rc = 0
TIGHT head = 39f92602f9eb
TIGHT net = OSError
```

## R11 — C2 probe sandbox confinement

```
$ bwrap <probe sandbox_argv, db_wal_probe.py:262-274> python3 -c '...'
c2 host-cups CONNECT= ConnectionRefusedError     (fresh netns; no resolver either)
c2 DNS= gaierror
c2 exists /home/vgpnk/.ssh/id_ed25519 = False
c2 exists /home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/index = False
c2 exists /run/user/1000/bus = False
c2 can write /usr? False  /etc? False
C2 write_/opt = FileNotFoundError
C2 write_home = FileNotFoundError
C2 write_app = ok
C2 write_usr = OSError
C2 systemd_run_rc = 1 (Failed to connect to user scope bus via local transport: No such file or directory)
host survivors after double fork: 0
```

## R12 — C2 verdict channel is forgeable by recipe-run code

Harness shape identical to `db_wal_probe.py:237-242` (recipe first, then verdicts). Recipe:
`H=$PPID; exec >/dev/null 2>&1; ( sleep 1; printf "TEST test_recovered_json_exists F\n" > /proc/$H/fd/1 ) & exit 0`

```
--- raw stream (order matters) ---
TEST test_recovered_json_exists P
TEST test_recovered_json_exists F
probe-parsed value: F lines_for_test: 2
FORGERY_WINS: True | duplicate-detection would catch it: True
```
`db_wal_probe.py:357-360` keeps the last line per `(tag, test)`, so the forged `F` overwrites the genuine `P`.

## R13 — command construction

```
$ grep -n "shell=True|os.system|popen|eval(|exec(" plans/round40_c1_verify.py plans/db_wal_probe.py
none
```
Both instruments pass argv lists; no shell interpolation anywhere on either path.

## Tooling
Nothing installed or upgraded (pacman transactions are paused host-wide; no `uv`/`npx`/binary was needed).

## R14 — a module built first rewrites a sibling module; the same run loads and attributes it

`plans/battery40` is the lane's own directory in a default run (`round40_c1_verify.py:474`), each file is read only
at its own turn (`:411-412`) and loaded by its child (`:419-420`), and the sandbox leaves the directory writable.

```
$ python3 plans/round40_c1_verify.py --lane "$S/lane" --battery-dir "$S/bat2" --only A01 --work "$S/w2"
PINS total=3 mismatched=0
FIXTURE A-ORIGINAL tool=anchor expect=error declared=- observed_rc=2 observed=- ok
FIXTURE B-REWRITTEN-BY-SIBLING tool=anchor expect=error declared=- observed_rc=2 observed=- ok
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
PINS-AFTER mismatched=0
$ grep -n fid "$S/bat2/b_second.py"
6:FIXTURES = [{"fid": "B-REWRITTEN-BY-SIBLING", ...}]
```
`a_first.py` rewrote `b_second.py` from its build(); the receipt attributes the rewritten fixture to `b_second.py`
and reports `tampered=0 sidechannel=0`.
