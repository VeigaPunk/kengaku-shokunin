import re
txt = open('SKILL.md').read()
txt = txt.split('## Cited local sources',1)[1]
bullets = 0
paths = set()
for line in txt.split('\n'):
    if not line.startswith('- `'):
        continue
    bullets += 1
    back = re.findall(r'`([^`]+)`', line)
    joined = ' | '.join(back)
    # expand braces
    parts = re.split(r'\{([^{}]+)\}', joined)
    if len(parts) > 1:
        variants = []
        opts = parts[1].split(',')
        head = parts[0]; tail = parts[-1] if len(parts) > 2 else ''
        for o in opts:
            variants.append(head + o + tail)
    else:
        variants = [joined]
    for v in variants:
        for p in re.findall(r'~/[A-Za-z0-9_./{}*+-]+|/tmp/[A-Za-z0-9_./{}*+-]+|wiki/[A-Za-z0-9_./{}*+-]+|corpus/knowledge/[A-Za-z0-9._-]+\.md', v):
            for seg in p.split('|'):
                seg = seg.strip()
                if seg: paths.add(seg)
print('bullets:', bullets)
print('distinct path-ish strings:', len(paths))
for p in sorted(paths): print(' ', p)
