# R30Census — round-30 counting command and before/after harness

Seat: `L1Kengaku30.R30Census` (executor, axes freshness + operability). Leaf: no spawns, no
background jobs. Nothing under the lane repo was created, edited or deleted except this report.

## 0. What landed

| item | value |
|---|---|
| script | `/tmp/r30-Census/round30_census.sh` (331 lines, mode 755) |
| sha256 | `2f7a5e860edd186c1e8610874e33d965972273e6e013fe672164a03b34bcbfb9` |
| proposed lane path | `plans/round30_census.sh` (the parent lands it; I did not touch `plans/`) |
| modes | `<rev>` · `--diff <before> <after>` · `--worktree` |
| counters | registry rows (census anchor) · knowledge files · knowledge index rows · staged collisions · open defects · gate selftest tally · C1 counter line, plus the parity/malformed/package lines that explain them |
| read path | `git show <rev>:<path>` for every lane byte in revision mode; `cat` for `--worktree`; never `HEAD`, never a checkout, never a detached-worktree assumption |
| tool installs | **none** — bash, gawk, grep, git, coreutils and python3 were already present; PACMAN is paused host-wide and no uv/npx/binary install was needed |

Each printed line is `printf '%-12s %-26s %s\n' <sha12|worktree> <label> <value>`: the revision that
was read is on the line itself, and an `at` line pins the UTC instant of the reading.

## 1. Source

```bash
    #!/usr/bin/env bash
    # round30_census.sh — kengaku round-30 counting command + before/after harness.
    #
    # READ-ONLY. Every lane byte is read either with `git show <rev>:<path>` (revision
    # mode) or with `cat` from the live worktree (--worktree mode). Nothing is written
    # inside the lane repo: the revision snapshot is materialised under a fresh mktemp
    # dir, and PYTHONDONTWRITEBYTECODE=1 stops the solvers dropping __pycache__ there.
    # Never relies on HEAD, a detached worktree or an index state: the revision is
    # resolved to a full sha and every printed line carries that sha.
    #
    # usage:
    #   round30_census.sh <rev> [options]                  census one revision
    #   round30_census.sh --diff <rev-before> <rev-after>  census both, print the delta
    #   round30_census.sh --worktree [options]            census the live worktree
    #
    # options:
    #   --expect PATH    frozen adoption expectation (default: the lane's round-30 file)
    #   --package PATH   staged package tested for id collisions
    #                    (default: shokuknow merge package, read-only)
    #   --out PATH       tee the report to PATH (stdout unchanged)
    #   --keep           keep the snapshot dir (its path is printed)
    #
    # Counters printed, one labelled line each:
    #   registry.rows            corpus/SOURCES.md rows under the census anchor
    #                            ^ {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|              (C1 anchor)
    #   registry.malformed_cells anchored rows whose cell count is not 11
    #   knowledge.files          corpus/knowledge/*.md at the revision
    #   knowledge.index_rows     anchored `| `knowledge/<name>.md` |` rows in corpus/README.md
    #   knowledge.unindexed      files with no index row   (parity defect)
    #   knowledge.dangling       index rows with no file   (parity defect)
    #   staged.rows              rows in the staged package under the same anchor
    #   staged.collisions        staged ids that already hold a registry row (census anchor)
    #   staged.c1_rows_present   ids the frozen expectation cites that exist in the package
    #   defects.open             plans/round30_defects.py tally (C2 counting command)
    #   gate.selftest            plans/sources_adopt.py --selftest tally (C3 counting command)
    #   gate.quote_mode          whether the revision's gate names --quote-file (C3 surface)
    #   C1.counter               plans/adoption_check.py --census frozen line + exit (C1 command)
    #   claims                   C1/C2/C3 verdicts against the frozen predicates
    #
    # exit: 0 when every counter produced a reading, 1 when one could not be measured.
    #       Claim truth (C1/C2/C3 yes|no) is printed and never folded into the exit status.
    set -u
    
    LANE=${LANE:-/home/vgpnk/Projects/shokunin/kengaku-shokunin}
    PKG_DEFAULT=/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
    EXPECT_REL=.ufo/waves/round-30/adoption-expect.json
    EXPECT=$LANE/$EXPECT_REL
    PACKAGE=$PKG_DEFAULT
    OUT=""
    KEEP=0
    MODE=""
    REV=""
    REV_B=""
    REGEX_ANCHOR='^ {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|'
    REGEX_ANCHOR_AWK='^ {0,3}[|][ \t]*S[0-9]{3,}[ \t]*[|]'
    C1_FROZEN="entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok"
    C3_TARGET_CASES=14
    
    while [ $# -gt 0 ]; do
      case "$1" in
        --diff)
          MODE=diff
          [ $# -ge 3 ] || { echo "round30_census.sh: --diff needs <before> <after>" >&2; exit 2; }
          REV=$2; REV_B=$3; shift 3 ;;
        --worktree) MODE=worktree; shift ;;
        --expect) [ $# -ge 2 ] || { echo "--expect needs a path" >&2; exit 2; }; EXPECT=$2; shift 2 ;;
        --package) [ $# -ge 2 ] || { echo "--package needs a path" >&2; exit 2; }; PACKAGE=$2; shift 2 ;;
        --out) [ $# -ge 2 ] || { echo "--out needs a path" >&2; exit 2; }; OUT=$2; shift 2 ;;
        --keep) KEEP=1; shift ;;
        -h|--help) sed -n '2,43p' "$0"; exit 0 ;;
        -*) echo "round30_census.sh: unknown option $1" >&2; exit 2 ;;
        *) if [ -n "$REV" ]; then echo "round30_census.sh: unexpected argument $1" >&2; exit 2; fi
           REV=$1; shift ;;
      esac
    done
    [ -n "$MODE" ] || MODE=rev
    if [ "$MODE" = rev ] && [ -z "$REV" ]; then
      echo "usage: round30_census.sh <rev> | --diff <before> <after> | --worktree" >&2; exit 2
    fi
    
    TMPROOT=$(mktemp -d "${TMPDIR:-/tmp}/r30census.XXXXXX")
    cleanup() { [ "$KEEP" = 1 ] || rm -rf "$TMPROOT"; }
    trap cleanup EXIT
    
    emit() { printf '%-12s %-26s %s\n' "$1" "$2" "$3"; }
    
    read_file() { # $1 = sha or "worktree", $2 = lane-relative path
      if [ "$1" = worktree ]; then cat "$LANE/$2" 2>/dev/null; else git -C "$LANE" show "$1:$2" 2>/dev/null; fi
    }
    
    resolve_rev() { git -C "$LANE" rev-parse --verify --quiet "$1^{commit}"; }
    
    # ---------------------------------------------------------------- snapshot ---
    # Materialise the measured subtrees plus the two round-29 wave files D4 reads.
    # corpus+plans is ~600 files / 21 MiB; .ufo/waves/round-29 as a whole is 271 MiB,
    # so the two files are listed explicitly instead of the subtree.
    snapshot() { # $1 = sha ; prints the snapshot root (lane-named dir + conf row)
      local sha=$1 root tree paths=() p
      root=$TMPROOT/rev-$sha
      tree=$root/kengaku-shokunin
      mkdir -p "$tree" || return 1
      for p in corpus plans \
               .ufo/waves/round-29/attempt2/adoption-expect.json \
               .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md; do
        if [ -n "$(git -C "$LANE" ls-tree -r --name-only "$sha" -- "$p" 2>/dev/null | head -1)" ]; then
          paths+=("$p")
        fi
      done
      [ ${#paths[@]} -gt 0 ] || { echo "round30_census.sh: revision $sha has no measured paths" >&2; return 1; }
      git -C "$LANE" archive --format=tar "$sha" -- "${paths[@]}" | tar -x -C "$tree" || return 1
      # A revision snapshot is committed by construction: git-init it so D4's
      # `git status --porcelain` arm answers "committed at this revision" instead of
      # failing for lack of a repository (a non-repo tree would print a false DEFECT).
      git -C "$tree" init -q >/dev/null 2>&1
      git -C "$tree" add -A >/dev/null 2>&1
      git -C "$tree" -c user.name=round30-census -c user.email=census@invalid \
          -c commit.gpgsign=false commit -qm "round-30 census snapshot $sha" >/dev/null 2>&1
      # adoption_check.py --census calls sources-census.sh with --root <lane.parent> <lane>,
      # so a scratch root needs a conf row. The fleet conf is never copied or edited.
      printf 'LANES="\nkengaku|kengaku-shokunin|round-30 census snapshot\n"\n' > "$root/shokunin.conf"
      printf '%s\n' "$root"
    }
    
    # ------------------------------------------------------------------ counts ---
    census_body() { # $1 = sha or worktree ; $2 = tree to run tools from ; $3 = label
      local sha=$1 tree=$2 tag=$3
      local registry readme files index unindexed dangling
      local pkg_rows pkg_ids reg_ids collisions c1_ids c1_present
      local defects_out defects_line defects_ids defects_exit
      local gate_out gate_line gate_cases gate_failed gate_exit quote_mode_n
      local c1_out c1_line c1_exit c1_ok c2_ok c3_ok missing=0
    
      if [ "$sha" = worktree ]; then
        emit "$tag" rev "worktree $LANE (HEAD $(git -C "$LANE" rev-parse --short HEAD 2>/dev/null || echo n/a), bytes read with cat)"
      else
        emit "$tag" rev "$sha"
      fi
      emit "$tag" lane "$LANE"
      emit "$tag" at "$(date -u +%Y-%m-%dT%H:%M:%SZ)  (UTC reading instant for every count in this block)"
      if [ "$sha" = worktree ]; then
        emit "$tag" snapshot "live worktree bytes (no snapshot: --worktree reads the lane directly)"
      else
        emit "$tag" snapshot "$tree  (corpus+plans+2 round-29 wave files, committed so D4 reads a committed tree)"
      fi
    
      # --- registry rows (census anchor) -------------------------------------
      registry=$(read_file "$sha" corpus/SOURCES.md)
      if [ -z "$registry" ]; then
        emit "$tag" registry.rows ABSENT; missing=1
      else
        emit "$tag" registry.rows "$(printf '%s\n' "$registry" | grep -cE "$REGEX_ANCHOR")"
        emit "$tag" registry.malformed_cells \
          "$(printf '%s\n' "$registry" | awk -F'|' -v re="$REGEX_ANCHOR_AWK" '$0 ~ re {if (NF!=13) m++} END{print m+0}')"
        emit "$tag" registry.ids_last \
          "$(printf '%s\n' "$registry" | grep -oE "$REGEX_ANCHOR" | grep -oE 'S[0-9]{3,}' | sort -u | tail -6 | paste -sd, -)"
      fi
    
      # --- knowledge files / index rows --------------------------------------
      if [ "$sha" = worktree ]; then
        files=$(for f in "$LANE"/corpus/knowledge/*.md; do [ -f "$f" ] && printf 'corpus/knowledge/%s\n' "${f##*/}"; done)
      else
        files=$(git -C "$LANE" ls-tree -r --name-only "$sha" -- corpus/knowledge 2>/dev/null | grep -E '\.md$')
      fi
      files=$(printf '%s\n' "$files" | grep -E '\.md$' | sort -u)
      emit "$tag" knowledge.files "$(printf '%s\n' "$files" | grep -c .)"
      readme=$(read_file "$sha" corpus/README.md)
      if [ -z "$readme" ]; then
        emit "$tag" knowledge.index_rows ABSENT; missing=1
      else
        index=$(printf '%s\n' "$readme" | grep -oE '^\| `knowledge/[^`|]+\.md` \|' \
                  | sed 's/^| `//; s/` |$//' | sort)
        emit "$tag" knowledge.index_rows "$(printf '%s\n' "$index" | grep -c .)"
        unindexed=$(comm -23 <(printf '%s\n' "$files" | sed 's|^corpus/||' | grep .) <(printf '%s\n' "$index" | grep .) | grep -c .)
        dangling=$(comm -13 <(printf '%s\n' "$files" | sed 's|^corpus/||' | grep .) <(printf '%s\n' "$index" | grep .) | grep -c .)
        emit "$tag" knowledge.unindexed "$unindexed"
        emit "$tag" knowledge.dangling "$dangling"
      fi
    
      # --- staged collisions (staged package vs registry, census anchor) -----
      if [ ! -f "$PACKAGE" ]; then
        emit "$tag" staged.rows "ABSENT ($PACKAGE)"
        emit "$tag" staged.collisions ABSENT
        emit "$tag" staged.c1_rows_present ABSENT
        missing=1
      else
        pkg_rows=$(grep -cE "$REGEX_ANCHOR" "$PACKAGE")
        emit "$tag" staged.rows "$pkg_rows  package=$PACKAGE"
        pkg_ids=$(grep -oE "$REGEX_ANCHOR" "$PACKAGE" | grep -oE 'S[0-9]{3,}' | sort -u)
        reg_ids=$(printf '%s\n' "$registry" | grep -oE "$REGEX_ANCHOR" | grep -oE 'S[0-9]{3,}' | sort -u)
        collisions=$(comm -12 <(printf '%s\n' "$pkg_ids" | grep .) <(printf '%s\n' "$reg_ids" | grep .) | paste -sd, -)
        emit "$tag" staged.collisions "$(printf '%s\n' "$collisions" | tr ',' '\n' | grep -c .)  ids=${collisions:-none}"
        c1_ids=$(python3 -c '
    import json, sys
    data = json.load(open(sys.argv[1]))
    print("\n".join(sorted({s for e in data.get("entries", []) for s in e.get("sources", [])})))
    ' "$EXPECT" 2>/dev/null | sort -u)
        if [ -z "$c1_ids" ]; then
          emit "$tag" staged.c1_rows_present ABSENT
        else
          c1_present=$(comm -12 <(printf '%s\n' "$c1_ids" | grep .) <(printf '%s\n' "$pkg_ids" | grep .) | paste -sd, -)
          emit "$tag" staged.c1_rows_present \
            "$(printf '%s\n' "$c1_present" | tr ',' '\n' | grep -c .)/$(printf '%s\n' "$c1_ids" | grep -c .)  ids=${c1_present:-none}"
        fi
      fi
    
      # --- open defects (C2 counting command) --------------------------------
      if [ ! -f "$tree/plans/round30_defects.py" ]; then
        emit "$tag" defects.open "ABSENT plans/round30_defects.py (pre-commit reading: .ufo/waves/round-30/claims/defects-before.txt)"; missing=1
      else
        defects_out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$tree/plans/round30_defects.py" --lane "$tree" 2>&1)
        defects_exit=$?
        defects_line=$(printf '%s\n' "$defects_out" | sed -n 's/^defects=\([0-9][0-9]*\)$/\1/p' | tail -1)
        defects_ids=$(printf '%s\n' "$defects_out" | sed -n 's/^DEFECT \(D[0-9][0-9]*\).*/\1/p' | paste -sd, -)
        emit "$tag" defects.open "${defects_line:-unparsed}  ids=${defects_ids:-none} exit=$defects_exit"
      fi
    
      # --- gate selftest tally (C3 counting command) -------------------------
      if [ ! -f "$tree/plans/sources_adopt.py" ]; then
        emit "$tag" gate.selftest "ABSENT plans/sources_adopt.py"; missing=1
      else
        gate_out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$tree/plans/sources_adopt.py" --selftest 2>&1)
        gate_exit=$?
        gate_line=$(printf '%s\n' "$gate_out" | sed -n 's/^SELFTEST \(cases=[0-9][0-9]* failed=[0-9][0-9]*\)$/\1/p' | tail -1)
        gate_cases=$(printf '%s\n' "$gate_line" | sed -n 's/cases=\([0-9]*\).*/\1/p')
        gate_failed=$(printf '%s\n' "$gate_line" | sed -n 's/.*failed=\([0-9]*\)/\1/p')
        emit "$tag" gate.selftest "${gate_line:-unparsed}  exit=$gate_exit"
      fi
      # The C3 surface is counted even when the tool is absent at the revision: an
      # absent gate names no --quote-file, which is the same reading as a gate without one.
      quote_mode_n=$(read_file "$sha" plans/sources_adopt.py | grep -c -- '--quote-file')
      emit "$tag" gate.quote_mode "$([ "${quote_mode_n:-0}" -gt 0 ] && echo present || echo 'absent (pre-change control: .ufo/waves/round-30/claims/gate-before.txt)')"
    
      # --- C1 counter line ---------------------------------------------------
      if [ ! -f "$tree/plans/adoption_check.py" ]; then
        emit "$tag" C1.counter "ABSENT plans/adoption_check.py"; missing=1
      elif [ ! -f "$EXPECT" ]; then
        emit "$tag" C1.counter "ABSENT expect $EXPECT"; missing=1
      else
        c1_out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$tree/plans/adoption_check.py" \
                   --lane "$tree" --expect "$EXPECT" --census 2>&1)
        c1_exit=$?
        c1_line=$(printf '%s\n' "$c1_out" | grep -E '^entries=' | tail -1)
        emit "$tag" C1.counter "${c1_line:-unparsed}  (exit=$c1_exit)"
        emit "$tag" C1.expect \
          "$EXPECT_REL source=worktree sha256=$(sha256sum "$EXPECT" | cut -c1-12) snapshot=$tree"
      fi
    
      # --- claim verdicts against the frozen predicates ----------------------
      c1_ok=no
      [ "${c1_line:-}" = "$C1_FROZEN" ] && [ "${c1_exit:-1}" -eq 0 ] && c1_ok=yes
      c2_ok=no
      [ "${defects_line:-x}" = 0 ] && [ "${defects_exit:-1}" -eq 0 ] && c2_ok=yes
      c3_ok=no
      if [ "${gate_failed:-x}" = 0 ] && [ "${gate_cases:-0}" -ge "$C3_TARGET_CASES" ] \
         && [ "${gate_exit:-1}" -eq 0 ] && [ "${quote_mode_n:-0}" -gt 0 ]; then c3_ok=yes; fi
      emit "$tag" claims "C1=$c1_ok C2=$c2_ok C3=$c3_ok  (frozen C1 '$C1_FROZEN' + exit 0 | C2 defects=0 + exit 0 | C3 cases>=$C3_TARGET_CASES failed=0 exit 0 + quote mode)"
      emit "$tag" exit "$([ "$missing" = 0 ] && echo 0 || echo 1)"
      return "$missing"
    }
    
    run_rev() { # $1 = user-supplied rev ; prints the census block
      local sha tag root
      sha=$(resolve_rev "$1") || { echo "round30_census.sh: cannot resolve revision $1" >&2; return 2; }
      tag=$(printf '%s' "$sha" | cut -c1-12)
      root=$(snapshot "$sha") || return 2
      census_body "$sha" "$root/kengaku-shokunin" "$tag"
    }
    
    diff_mode() {
      local a_sha b_sha a_tag b_tag a_out b_out status=0
      a_sha=$(resolve_rev "$REV")   || { echo "round30_census.sh: cannot resolve $REV" >&2; return 2; }
      b_sha=$(resolve_rev "$REV_B") || { echo "round30_census.sh: cannot resolve $REV_B" >&2; return 2; }
      a_tag=$(printf '%s' "$a_sha" | cut -c1-12)
      b_tag=$(printf '%s' "$b_sha" | cut -c1-12)
      a_out=$(run_rev "$REV") || status=1
      b_out=$(run_rev "$REV_B") || status=1
      echo "== BEFORE $a_tag ($REV)  $a_sha"
      printf '%s\n' "$a_out"
      echo
      echo "== AFTER  $b_tag ($REV_B)  $b_sha"
      printf '%s\n' "$b_out"
      echo
      echo "== DELTA  $a_tag -> $b_tag"
      python3 - "$a_tag" "$b_tag" "$a_out" "$b_out" <<'PY'
    import sys
    
    a_tag, b_tag, a_out, b_out = sys.argv[1:5]
    
    def parse(text, tag):
        rows = {}
        for line in text.splitlines():
            parts = line.split(None, 2)
            if len(parts) == 3 and parts[0] == tag:
                rows[parts[1]] = parts[2].strip()
        return rows
    
    A, B = parse(a_out, a_tag), parse(b_out, b_tag)
    keys = ["registry.rows", "registry.malformed_cells", "knowledge.files", "knowledge.index_rows",
            "knowledge.unindexed", "knowledge.dangling", "staged.rows", "staged.collisions",
            "staged.c1_rows_present", "defects.open", "gate.selftest", "gate.quote_mode",
            "C1.counter", "claims"]
    print(f"{'counter':26s} {'before':>22s} {'after':>22s}  delta")
    for key in keys:
        av, bv = A.get(key, "<missing>"), B.get(key, "<missing>")
        head_a = av.split()[0] if av.split() else av
        head_b = bv.split()[0] if bv.split() else bv
        if head_a.isdigit() and head_b.isdigit():
            shown_a, shown_b = head_a, head_b
            delta = f"{int(head_b) - int(head_a):+d}"
        elif av == bv:
            shown_a, shown_b = (av[:22] + "…") if len(av) > 22 else av, ""
            delta = "same"
        else:
            shown_a = (av[:22] + "…") if len(av) > 22 else av
            shown_b = (bv[:22] + "…") if len(bv) > 22 else bv
            delta = "changed"
        print(f"{key:26s} {shown_a:>18s} {shown_b:>18s}  {delta}")
    print()
    print("full before/after blocks above; claim verdicts:")
    for tag, rows in ((a_tag, A), (b_tag, B)):
        print(f"  {tag}: {rows.get('claims', '<missing>').split('  (')[0]}")
    PY
      return "$status"
    }
    
    case "$MODE" in
      rev)      run_rev "$REV" ;;
      worktree) census_body worktree "$LANE" worktree ;;
      diff)     diff_mode ;;
    esac 2>&1 | { if [ -n "$OUT" ]; then tee "$OUT"; else cat; fi; }
    exit "${PIPESTATUS[0]}"
```

## 2. What each line counts, and which round-report number it explains

| line | definition | round-30 number it explains |
|---|---|---|
| `registry.rows` | `corpus/SOURCES.md` rows matching the census anchor `^ {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|` — the same clause the fleet census and `sources_adopt.py` use (a column-zero-only pattern would miss an indented row) | 82 rows pre-admission; 88 post-admission (`+6`) |
| `registry.malformed_cells` | anchored rows whose `awk -F'\|'` cell count is not 13, i.e. not the 11-cell schema | 0 pre, 0 post — a non-zero here invalidates every other registry number |
| `registry.ids_last` | last six ids by sort | "last ids S077–S080, S090, S091" |
| `knowledge.files` | `corpus/knowledge/*.md` at the revision (`git ls-tree`) | 38 pre, 39 post |
| `knowledge.index_rows` | anchored rows `` ^\| `knowledge/<name>.md` \| `` in `corpus/README.md` — the form `adoption_check.py` accepts, not a prose mention | 38 pre, 39 post |
| `knowledge.unindexed` / `knowledge.dangling` | the two parity directions between those sets | 0/0 pre; post must stay 0/0 — `dangling=1` is the fingerprint of an index row landed before its entry (seen live in §5) |
| `staged.rows` | rows in the staged package under the same anchor | 175 staged rows in `shokuknow/merge/kengaku/SOURCES.append.md` |
| `staged.collisions` | staged ids ∩ registry ids | 6 pre-admission (`S077 S078 S079 S080 S090 S091`), 12 post; `--worktree` reproduces `.ufo/waves/round-30/assimilation/collisions` exactly |
| `staged.c1_rows_present` | ids the frozen `adoption-expect.json` cites that exist in the package | `6/6` for `S081–S086`: the expectation cannot cite a row the package lacks |
| `defects.open` | runs the revision's `plans/round30_defects.py --lane <snapshot>`, parses `defects=N` and the `DEFECT D#` tokens | C2: 5 → 0. Where the tool is not yet committed the line says `ABSENT … (pre-commit reading: .ufo/waves/round-30/claims/defects-before.txt)` instead of inventing a number |
| `gate.selftest` | runs the revision's `plans/sources_adopt.py --selftest`, parses `SELFTEST cases=N failed=M` | C3: `cases=10 failed=0` → `cases=14 failed=0` |
| `gate.quote_mode` | whether the revision's gate source names `--quote-file` | C3's second surface: `absent (pre-change control: …/gate-before.txt)` → `present` |
| `C1.counter` | runs the revision's `plans/adoption_check.py --lane <snapshot> --expect <frozen> --census` and prints its single line plus exit | C1: `entries=0 …` exit 1 → the frozen `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` exit 0 |
| `claims` | the three frozen predicates evaluated against the lines above (C1 = exact frozen line + exit 0; C2 = `defects=0` + exit 0; C3 = `cases>=14 failed=0` exit 0 + quote mode) | the report's per-claim verdict, printed so the census cannot silently disagree with it |
| `exit` | 0 = every counter produced a reading; 1 = at least one could not be measured | claim truth is **not** folded into the exit, so a "before" tree that lacks a tool reads as an honest measurement gap, not as a script failure |

## 3. Read-only evidence

Revision mode writes only into `mktemp -d` (`/tmp/r30census.*`): `git archive <sha> -- corpus plans
<two round-29 wave files>` piped into `tar -x`. The two round-29 files are listed explicitly because
`.ufo/waves/round-29` as a subtree is 271 MiB while the two files D4 reads are 64 KiB.

```
$ git -C <lane> status --porcelain -uall | sha256sum      # before
$ ./round30_census.sh --worktree > /dev/null
$ ./round30_census.sh master > /dev/null
$ LANE=/tmp/r30-Census/fixture ./round30_census.sh --diff <sha> HEAD --expect …
$ git -C <lane> status --porcelain -uall | sha256sum      # after
→ hashes identical: READONLY_STATUS_UNCHANGED
→ files newer than the run stamp under the lane (excluding .git):
  .ufo/waves/round-30/build/R30DraftGate.md   (a sibling seat's report, written by that seat)
```

`PYTHONDONTWRITEBYTECODE=1` is set for every solver invocation, so no `__pycache__` appears under
`plans/`; `sources_adopt.py --selftest` writes its fixtures to `tempfile` dirs.

## 4. Required paste — current branch tip

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master` →
`363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db`

```
$ /tmp/r30-Census/round30_census.sh master
363a4ebfda05 rev                        363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db
363a4ebfda05 lane                       /home/vgpnk/Projects/shokunin/kengaku-shokunin
363a4ebfda05 at                         2026-10-25T07:32:39Z  (UTC reading instant for every count in this block)
363a4ebfda05 snapshot                   /tmp/r30census.25IVM8/rev-363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db/kengaku-shokunin  (corpus+plans+2 round-29 wave files, committed so D4 reads a committed tree)
363a4ebfda05 registry.rows              82
363a4ebfda05 registry.malformed_cells   0
363a4ebfda05 registry.ids_last          S077,S078,S079,S080,S090,S091
363a4ebfda05 knowledge.files            38
363a4ebfda05 knowledge.index_rows       38
363a4ebfda05 knowledge.unindexed        0
363a4ebfda05 knowledge.dangling         0
363a4ebfda05 staged.rows                175  package=/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
363a4ebfda05 staged.collisions          6  ids=S077,S078,S079,S080,S090,S091
363a4ebfda05 staged.c1_rows_present     6/6  ids=S081,S082,S083,S084,S085,S086
363a4ebfda05 defects.open               ABSENT plans/round30_defects.py (pre-commit reading: .ufo/waves/round-30/claims/defects-before.txt)
363a4ebfda05 gate.selftest              cases=10 failed=0  exit=0
363a4ebfda05 gate.quote_mode            absent (pre-change control: .ufo/waves/round-30/claims/gate-before.txt)
363a4ebfda05 C1.counter                 entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok  (exit=1)
363a4ebfda05 C1.expect                  .ufo/waves/round-30/adoption-expect.json source=worktree sha256=6ac80746e007 snapshot=/tmp/r30census.25IVM8/rev-363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db/kengaku-shokunin
363a4ebfda05 claims                     C1=no C2=no C3=no  (frozen C1 'entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok' + exit 0 | C2 defects=0 + exit 0 | C3 cases>=14 failed=0 exit 0 + quote mode)
363a4ebfda05 exit                       1
```

Reading of that block, in the report's terms:

- **82 registry rows, 0 malformed, last ids `S077,S078,S079,S080,S090,S091`** — the pre-admission anchor.
- **38 knowledge files / 38 index rows / 0 unindexed / 0 dangling** — the corpus index is in parity, so
  this round's `+1` must arrive as an entry *and* a row together.
- **175 staged rows, 6 collisions** — the staged package re-states exactly the six ids the lane already
  holds, and all six ids the round adopts (`S081–S086`) are present in it (`6/6`).
- **`defects.open ABSENT`** — honest: at `master`, `plans/round30_defects.py` is not committed (it is
  `??` in the worktree). The 5-defect pre-repair reading is the committed receipt named on the line.
- **`gate.selftest cases=10 failed=0`**, **`gate.quote_mode absent`** — the C3 "before" surface.
- **`C1.counter entries=0 … census=ok (exit=1)`** — the C1 "before" surface. `census=ok` here is not a
  free pass; §7 shows the arm is snapshot-scoped.
- **`claims C1=no C2=no C3=no`**, **`exit 1`** — exit 1 because the C2 counter is unmeasurable at this
  revision, not because a claim was scored.

## 5. Live worktree reading (mid-wave, timestamped)

`--worktree` reads the lane directly with `cat`. It is the mode that can show a half-landed state, and
it is unstable by design while siblings write. Taken at `2026-10-25T07:32:39Z`:

```
$ /tmp/r30-Census/round30_census.sh --worktree
worktree     rev                        worktree /home/vgpnk/Projects/shokunin/kengaku-shokunin (HEAD 363a4eb, bytes read with cat)
worktree     lane                       /home/vgpnk/Projects/shokunin/kengaku-shokunin
worktree     at                         2026-10-25T07:32:39Z  (UTC reading instant for every count in this block)
worktree     snapshot                   live worktree bytes (no snapshot: --worktree reads the lane directly)
worktree     registry.rows              82
worktree     registry.malformed_cells   0
worktree     registry.ids_last          S077,S078,S079,S080,S090,S091
worktree     knowledge.files            39
worktree     knowledge.index_rows       39
worktree     knowledge.unindexed        0
worktree     knowledge.dangling         0
worktree     staged.rows                175  package=/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
worktree     staged.collisions          6  ids=S077,S078,S079,S080,S090,S091
worktree     staged.c1_rows_present     6/6  ids=S081,S082,S083,S084,S085,S086
worktree     defects.open               3  ids=D1,D2,D4 exit=1
worktree     gate.selftest              cases=14 failed=0  exit=0
worktree     gate.quote_mode            present
worktree     C1.counter                 entries=1 indexed=1 cited_rows=6 rows_present=0 rows_mined=0 usedby_ok=0 census=ok  (exit=1)
worktree     C1.expect                  .ufo/waves/round-30/adoption-expect.json source=worktree sha256=6ac80746e007 snapshot=/home/vgpnk/Projects/shokunin/kengaku-shokunin
worktree     claims                     C1=no C2=no C3=yes  (frozen C1 'entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok' + exit 0 | C2 defects=0 + exit 0 | C3 cases>=14 failed=0 exit 0 + quote mode)
worktree     exit                       0
```

This is the state the census exists for: `knowledge.files 39` with `dangling 0` (entry and index row
landed together), `C1.counter` already `entries=1 indexed=1 cited_rows=6` but `rows_present=0
rows_mined=0 usedby_ok=0` (the six registry rows are **not** appended yet), therefore `C1=no` with exit
1 rather than a false green. `gate.selftest cases=14 failed=0` + `quote_mode present` show the C3 patch
is in the worktree. `defects.open 3 ids=D1,D2,D4` is a live mid-edit reading (the lesson and the D1
receipt were being rewritten while this ran); the sealed C2 numbers must come from the landing commit.

## 6. Before/after harness

### 6a. A real revision pair the lane already carries (no fixture)

`1f3b0f1` (round-29 baseline, before that round's adoption) → `8cf7b60` (after it):

```
$ /tmp/r30-Census/round30_census.sh --diff 1f3b0f1 8cf7b60
== DELTA  1f3b0f1ec41e -> 8cf7b60650af
counter                                    before                  after  delta
registry.rows                              76                 81  +5
registry.malformed_cells                    0                  0  +0
knowledge.files                            37                 38  +1
knowledge.index_rows                       37                 38  +1
knowledge.unindexed                         0                  0  +0
knowledge.dangling                          0                  0  +0
staged.rows                               175                175  +0
staged.collisions                           0                  5  +5
staged.c1_rows_present     6/6  ids=S081,S082,S08…                     same
defects.open               ABSENT plans/round30_d…                     same
gate.selftest              ABSENT plans/sources_a… cases=10 failed=0  exi…  changed
gate.quote_mode            absent (pre-change con…                     same
C1.counter                 ABSENT plans/adoption_… entries=0 indexed=0 ci…  changed
claims                     C1=no C2=no C3=no  (fr…                     same

full before/after blocks above; claim verdicts:
  1f3b0f1ec41e: C1=no C2=no C3=no
  8cf7b60650af: C1=no C2=no C3=no
```

### 6b. Zero-delta control

`--diff master master` — the harness must report no change when there is none:

```
$ /tmp/r30-Census/round30_census.sh --diff master master
== DELTA  363a4ebfda05 -> 363a4ebfda05
counter                                    before                  after  delta
registry.rows                              82                 82  +0
registry.malformed_cells                    0                  0  +0
knowledge.files                            38                 38  +0
knowledge.index_rows                       38                 38  +0
knowledge.unindexed                         0                  0  +0
knowledge.dangling                          0                  0  +0
staged.rows                               175                175  +0
staged.collisions                           6                  6  +0
staged.c1_rows_present     6/6  ids=S081,S082,S08…                     same
defects.open               ABSENT plans/round30_d…                     same
gate.selftest              cases=10 failed=0  exi…                     same
gate.quote_mode            absent (pre-change con…                     same
C1.counter                 entries=0 indexed=0 ci…                     same
claims                     C1=no C2=no C3=no  (fr…                     same

full before/after blocks above; claim verdicts:
  363a4ebfda05: C1=no C2=no C3=no
  363a4ebfda05: C1=no C2=no C3=no
```

### 6c. Discrimination probe against a round-30-shaped "after" (FIXTURE — not the admission)

To prove the table can move on round-30's own surfaces I built a scratch clone (`git clone --shared`,
all writes in `/tmp`) at `master`, copied the worktree's in-flight repair bytes (`plans/sources_adopt.py`,
`plans/round30_defects.py`, `corpus/lessons/round-29.md`, `corpus/README.md`,
`.ufo/waves/round-29/attempt2/{adoption-expect.json,build/R29a2CritEntry.md}`,
`corpus/evidence/round29-attempt2/control-nothing.txt`, `.ufo/waves/round-30/adoption-expect.json`), and
added **placeholder** admission bytes: `corpus/knowledge/contamination-transparency-card.md` with six
`source: S081…S086` lines plus `verified-at: 2026-10-25`, and six `S081–S086` registry rows
(`https://example.invalid/...`, `status=mined`, `opened=2026-10-25`, `used-by` naming the entry).
Commit `8a9ad48` is that fixture and its message says so. **Its entry text and rows are not the scribes'
entry and rows; do not cite them as the admission.**

```
$ LANE=/tmp/r30-Census/fixture /tmp/r30-Census/round30_census.sh --diff 363a4ebf… HEAD \
    --expect /tmp/r30-Census/fixture/.ufo/waves/round-30/adoption-expect.json
== DELTA  363a4ebfda05 -> 8a9ad488c492
counter                                    before                  after  delta
registry.rows                              82                 88  +6
registry.malformed_cells                    0                  0  +0
knowledge.files                            38                 39  +1
knowledge.index_rows                       38                 39  +1
knowledge.unindexed                         0                  0  +0
knowledge.dangling                          0                  0  +0
staged.rows                               175                175  +0
staged.collisions                           6                 12  +6
staged.c1_rows_present     6/6  ids=S081,S082,S08…                     same
defects.open               ABSENT plans/round30_d…   1  ids=D2 exit=1  changed
gate.selftest              cases=10 failed=0  exi… cases=14 failed=0  exi…  changed
gate.quote_mode            absent (pre-change con…            present  changed
C1.counter                 entries=0 indexed=0 ci… entries=1 indexed=1 ci…  changed
claims                     C1=no C2=no C3=no  (fr… C1=yes C2=no C3=yes  (…  changed

full before/after blocks above; claim verdicts:
  363a4ebfda05: C1=no C2=no C3=no
  8a9ad488c492: C1=yes C2=no C3=yes
```

The delta table is the harness's acceptance: `registry.rows +6`, `knowledge.files +1`,
`knowledge.index_rows +1` with parity kept, `staged.collisions 6 → 12` (the six adopted ids become held
rows), `gate.selftest cases=10 → cases=14`, `gate.quote_mode absent → present`, `C1.counter` from
`entries=0 …` to the **frozen line**, and `claims` flipping `C1=no → C1=yes`, `C3=no → C3=yes`. `C2=no`
in the fixture only because the lesson copy I took was mid-edit (`ids=D2`); that keeps the C2 line
failure-capable in the probe, which is what a control needs.

## 7. The C1 census arm is snapshot-scoped, not a live-lane pass

`adoption_check.py --census` shells out to `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
with `--root <lane.parent> <lane-name>`, and that script takes no revision argument. To keep
`census=ok` from becoming a live-tree rubber stamp, the census materialises a lane-named snapshot
(`…/rev-<sha>/kengaku-shokunin`) and plants a one-row `shokunin.conf` beside it, so the census resolves
**the snapshot's** registry. Proof, from a kept snapshot (`--keep`) with one scrubbed `used-by` cell:

```
$ python3 <snapshot>/plans/adoption_check.py --lane <snapshot> --expect <frozen> --census
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=fail
MUTATED_EXIT=1

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <snapshot parent> kengaku | tail -1
kengaku	E11	S077 missing used-by corpus/knowledge/__no_such_entry__.md
```

Had the arm been reading the live lane, `census` would have stayed `ok` under that mutation.

## 8. Limits the parent should know (stated, not hidden)

1. `--worktree` numbers are a moving target; cite them only with the `at` timestamp, and never as the
   round's sealed numbers — those belong to the landing commit.
2. The snapshot path varies between runs (`mktemp`), so the `snapshot` line is the only unstable line;
   every count line is path-free and byte-reproducible.
3. The expectation file is deliberately read from the **worktree** (labelled `source=worktree` with its
   sha256) so both sides of a diff are measured against one frozen expectation; it is not a corpus
   measurement.
4. `defects.open` is unmeasurable at a revision whose tree does not carry `plans/round30_defects.py`
   (it is `??` in the worktree as I write). Until the counter is committed, the C2 "before" number is
   the committed receipt `.ufo/waves/round-30/claims/defects-before.txt`.
5. D4 at snapshot scope: a materialised revision is committed by construction, so the snapshot is
   `git init`-ed and committed before the counter runs. That is the correct semantics for "is this wave
   evidence committed at this revision", but it means revision-mode D4 can never be red for a file that
   is in the tree; the live reading is `--worktree`.
6. `--diff` runs both revisions in full (two archive+extract plus three tool runs each, ~2 s here);
   archives are `--format=tar` streams — no checkout, no `.git` mutation in the lane.

## 9. Risks

- **Census-anchor drift.** `registry.rows` uses the 0–3-space clause, not `^| S`. If a later census
  tightens to another clause, round-30 and round-31 numbers stop being comparable; the anchor sits in
  the script header for that reason.
- **A green `claims C1=yes` is not an admission verdict.** It certifies the counter's frozen line and
  exit only, which is exactly what C1's predicate says; the content verdict is the reviewers'.
- **Exit-status misuse.** `exit 1` on a "before" tree means "one counter unmeasurable", not "claim
  failed" — the `claims` line and the `exit` line say which is which.

## 10. What the parent should run after landing

```bash
sh plans/round30_census.sh master                    # before, sealed
sh plans/round30_census.sh --worktree                # optional, timestamped
sh plans/round30_census.sh --diff master <landing-sha>   # the round's delta table
```

Cite the `--diff` table plus the landing revision's own block in the round report; every number in §2
maps to a line there.

## Blockers

None. `/tmp/r30-Census/` holds `round30_census.sh`, the fixture clone and every output pasted above.
