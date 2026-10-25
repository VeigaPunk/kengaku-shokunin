# R34CaptureNec — S091 quarantine hand-check

**Axis:** coverage / source-verification adjacency. The capture was attempted at the frozen NEC URL; the returned page is an access-denied response, not the cited article.

Command:
```sh
curl -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" https://jpn.nec.com/techrep/journal/g23/n02/230212.html -o /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/nec-s091.html && wc -c /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/nec-s091.html && sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/nec-s091.html
```
Output: `418 .../nec-s091.html`; SHA-256 `967e4c244fa28577dc3dc9e5ba282c495372607ca5e32bc7a82b06bc75fdeed3`.

Extraction/normalization command:
```sh
python -c 'from html.parser import HTMLParser; import re,pathlib; p=pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/nec-s091.html"); s=p.read_text(errors="replace"); print(re.sub(r"\\s+"," ",re.sub(r"<[^>]*>"," ",s)))'
```
Output is an Akamai **Access Denied** page: “You don't have permission to access …230212.html on this server,” with an edgesuite reference. The requested Japanese sentence is not present in captured bytes. No RAKUDA evaluation paragraph or section 6.2 context can be confirmed; no located quote is reported because the source article was not retrieved. Approximate location supplied by the task (paragraph after figure 3 / section 6.2) remains unverified.

VERDICT: nec-s091 absent