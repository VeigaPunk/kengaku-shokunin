# R34 SentSecrets — Secret-material scan of round-34 wave outputs

Seat: R34SentSecrets (leaf sentinel). Scope: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/` including capture dirs (`assimilation/captures/`, `tb2-eval/`). Source repo not touched; no edits made outside the report path.

## Sweep commands (filename-only output; values never printed)

All run with `grep -rIlE` (recursive, ignore binary, files-with-matches) or `grep -rn | cut -d: -f1-2` for locations; `|| true` preserves empty-output reporting. Patterns:

| # | Class | Pattern (abridged) | Result |
|---|-------|--------------------|--------|
| 1 | API keys | `(api[_-]?key|apikey|secret[_-]?key|access[_-]?key|client[_-]?secret)\s*[:=]\s*["']?[A-Za-z0-9_\-+/=]{16,}` | empty (0 files) |
| 2 | Tokens/passwords | `(token|auth[_-]?token|bearer|passwd|password|pwd)\s*[:=]\s*["']?[A-Za-z0-9_\-+/=]{12,}` | empty (0 files) |
| 3 | Vendor prefixes/JWT | `sk-(live\|test)-…|AKIA[0-9A-Z]{16}|gh[pousr]_…|AIza…|xox[baprs]-…|sk_live_…|sk_test_…|eyJ…\.eyJ…\.…` | empty (0 files) |
| 4 | Private keys | `-----BEGIN [A-Z ]*PRIVATE KEY-----|-----BEGIN OPENSSH PRIVATE KEY-----|ssh-rsa|ssh-ed25519` | empty (0 files) |
| 5 | 1Password refs | `op://[A-Za-z0-9@._\-/]+` | empty (0 files) |
| 6 | Creds in URLs | `(postgres\|mysql\|redis\|mongodb(\+srv)?\|amqp)://…:…@|https?://…:…@…` | `assimilation/captures/geniac-s105.html:42` (false positive, below) |
| 7 | Private/internal URLs | `https?://…(10\.|192\.168\.|172\.(1[6-9]\|2[0-9]\|3[01])\.|\.corp|\.local|\.internal|localhost)` | `build/R34CensusProbe/mined-paths.txt`, `build/R34PriorArtTB2.md` (false positives, below) |
| 8 | Auth headers/cookies | `authorization\s*:\s*(bearer\|basic\|token)|set-cookie|cookie\s*:|sessionid\s*=|phpsessid|jsessionid|auth_token\s*=|_authToken=` | empty (0 files) |
| 9 | Long key=value | `[A-Z][A-Z0-9_]{5,}\s*=\s*["']?[A-Za-z0-9_\-+/=]{32,}` | empty (0 files) |
| 10 | Key/token vars | `(private[_-]?key|public[_-]?key|signing[_-]?key|api[_-]?secret|access[_-]?token|refresh[_-]?token|session[_-]?token)\s*[:=]` | empty (0 files) |
| 11 | Suspicious names | `find -name '.env*' -o -name '*.pem' -o -name '*.key' -o -name '.npmrc' -o -name '.netrc' -o -name '.git-credentials' -o -name 'id_rsa*' -o -iname '*secret*' -o -iname '*token*'` | only `build/R34RedBeforeTokenCooc.md`, `falsify/red-before/token-cooc.txt` (C2 token co-occurrence notes; sweep 2/10 show no credential content) |

Sweeps 1–10 were run twice (initial pass and a re-run after peer captures grew), including a final combined pass over `assimilation/captures/` specifically — all empty. Binary/large-file check: `find -type f -size +1M` empty; every file in the wave tree passes `grep -Iq .` (no empty/binary files skipped).

## Adjudicated hits (all false positives, no credential material)

1. **`geniac-s105.html:42`** (sweep 6) — matched a Google Fonts stylesheet URI of form `https://fonts.googleapis.com/<path>@600&display=swap`; the `@` is a font-weight axis parameter, not userinfo. Host census of the file: `fonts.googleapis.com` (2), `fonts.gstatic.com` (1), `www.meti.go.jp` (25), `web-static.archive.org` (6), `web.archive.org` (5), `cs.nakanohito.jp` (2) — all public; no `user:pass@` present.
2. **`build/R34CensusProbe/mined-paths.txt`** (sweep 7) — matched numeric segments inside public URLs (`10.`/`172.` in DOI/academic paths, e.g. `proceedings.mlr.press` volumes, `aclanthology.org/2022.acl-long.172/`). Host census: arxiv.org, aclanthology.org, github.com, raw.githubusercontent.com, doi.org, pypi.org, openai.com, docs.python.org, etc. — all public.
3. **`build/R34PriorArtTB2.md`** (sweep 7) — same class (`doi.org/10.xxx`); host census: arxiv.org, doi.org, github.com, link.springer.com, www.nature.com — all public.

## Conclusion

No tokens, API keys, `op://` references, private/internal URLs, session cookies, `Authorization` headers, private key material, or credential-bearing DSNs/URLs are present in the round-34 wave tree or its captures. The three shape-class hits are adjudicated false positives with public hosts. No secret values were printed; evidence above is file:line and host census only.

VERDICT: sent-secrets (hits 0)
