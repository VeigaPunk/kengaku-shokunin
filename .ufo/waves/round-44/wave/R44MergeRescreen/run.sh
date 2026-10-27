set -u
S=/fast/scratch/hyaku/kengaku-r44/R44MergeRescreen
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
G=$L/.ufo/waves/round-36/assimilation/id-collision-check.sh
echo "== real"; A=$S/A LANE=$L sh $G; echo "exit=$?"
cd $S/fx
printf '  | S002 | indented collision bait | code |\n| S900 | control | code |\n' > reg.md
printf '| S002 | staged twin | code |\n| S901 | no twin | code |\n' > staged.md
printf '    | S003 | four-space | code |\n   | S004 | three-space | code |\n' > indent.md
echo "== guard proof"
mkdir -p a; A=a REG=reg.md STAGED=staged.md sh $G; echo "exit=$?"; echo "collisions:"; cat a/collisions
echo "== bare ^| anchor on reg.md"; grep -oE '^[|][[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+'
echo "== 0-3 anchor on reg.md"; grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+'
mkdir -p b; A=b REG=indent.md STAGED=staged.md sh $G; echo "exit=$?"; cat b/reg-ids
echo "== absent"; mkdir -p c; A=c REG=nope STAGED=staged.md sh $G; echo "exit=$?"
