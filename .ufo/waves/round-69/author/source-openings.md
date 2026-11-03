# Primary-source reading receipt

Read2026-11-03 after reviewer freeze fcb25f3b via web text extraction, no full
HTML/PDF/source captures saved. Canonical older research, not current SOTA survey.

1. Geifman & El-Yaniv, NeurIPS2017, official proceedings PDF:
https://papers.nips.cc/paper_files/paper/2017/file/4a8423d5e91fda00bb7e46540e2b0cf1-Paper.pdf
Opened sections2–3 (printed pp2–4), equations1–4, Algorithm1/Theorem3.2.
Source teaching: coverage is accepted mass; error is conditional on accepted items.
The guarantee is distribution- and sampling-dependent; the procedure adjusts bounds
across its search. Not a universal promise from a low observed error.
Quote (p2, §2): "[source quotation omitted in selective export; consult the cited source]"

2. Kamath, Jia & Liang, ACL2020, official paper:
https://aclanthology.org/2020.acl-main.503.pdf
Opened §§2.3,3.1–3.3 (printed pp5686–5687), and introduction setup.
Source teaching: selective QA evaluates confidence-based abstention under source/OOD
mixtures. Relative ranking differs from absolute calibration, and source confidence
need not remain reliable out of domain. Scope is their extractive-QA setting, not
an empirical result for current generative LLMs.
Quote (p5686, §3.1): "[source quotation omitted in selective export; consult the cited source]"

Rejected use: neither source establishes these synthetic policies' population safety,
or guarantees arbitrary domain transport. Read full method sections rather than
using an abstract as detailed-method evidence. Original A–H calculations are from
reviewer synthetic inputs, not borrowed data/results. Arithmetic cross-check used
Python stdlib: 1-.05**(1/20)=.13910834066826516;
ceil(log(.05)/log(.98))=149; utilities240/380, then120/-100.
