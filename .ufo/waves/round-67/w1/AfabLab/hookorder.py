"""Mechanism receipt for the AFAB labrat: hook-dictionary key insertion order, measured locally.

The grader keys the AFAB check on the *insertion order* of the hook dictionary
(test_outputs.py:152-157). This script registers the grader's hook code verbatim (copied from
corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py:60-89) on a
LlamaForCausalLM built with the grader's config, runs three world-size-1 schedules with the q1-ref
partition/loss code, and prints the key order each one produces plus whether the grader's AFAB
predicate would fire on that order.

No distributed process group and no port; this measures key order only.
"""

import hashlib
import importlib.util
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import LlamaConfig, LlamaForCausalLM

SEAT = Path("/fast/scratch/hyaku/kengaku-r67/AfabLab")


def _register_hooks(model, dict, prefix=""):
    import torch.nn as nn
    from transformers import LlamaModel
    for name, module in model.named_children():
        full_name = f"{prefix}.{name}" if prefix else name

        if isinstance(module, nn.ModuleList) or isinstance(module, LlamaModel):
            _register_hooks(module, dict, prefix=full_name)
            continue

        def _post_forward_hook(module, input, output, layer_name=full_name):
            output = output[0] if isinstance(output, (tuple, list)) else output
            dict.setdefault(f"{layer_name}.fwd", []).append(output.detach().clone())

        def _post_backward_hook(module, grad_input, grad_output, layer_name=full_name):
            if isinstance(grad_output, (tuple, list)):
                grad_output = grad_output[0]
            dict.setdefault(f"{layer_name}.bwd", []).append(
                grad_output.detach().clone()
            )

        module.register_forward_hook(_post_forward_hook)
        module.register_full_backward_hook(_post_backward_hook)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make():
    torch.manual_seed(42)
    config = LlamaConfig(
        hidden_size=512,
        intermediate_size=1376,
        num_attention_heads=4,
        num_hidden_layers=4,
        vocab_size=32000,
        max_position_embeddings=256,
    )
    model = LlamaForCausalLM(config)
    inputs = torch.randint(0, config.vocab_size, (4, 8))
    targets = inputs.clone()
    targets[:, :-1] = inputs[:, 1:]
    targets[:, -1] = -100
    return (
        model,
        [inputs[i : i + 1].clone() for i in range(4)],
        [targets[i : i + 1].clone() for i in range(4)],
    )


def loss_of(model, out, target, m):
    logits = model.lm_head(model.model.norm(out))
    return F.cross_entropy(
        logits.reshape(-1, logits.size(-1)), target.reshape(-1), ignore_index=-100
    ) / m


def run_afab(mod):
    model, mbs, tgs = make()
    d = {}
    _register_hooks(model, d)
    stored = []
    for i in range(4):
        h = model.model.embed_tokens(mbs[i])
        out = mod._decoder(model, h, 0, 4)
        stored.append((h, loss_of(model, out, tgs[i], 4)))
    for _, loss in stored:
        loss.backward()
    return d


def run_1f1b(mod):
    model, mbs, tgs = make()
    d = {}
    _register_hooks(model, d)
    for i in range(4):
        h = model.model.embed_tokens(mbs[i])
        out = mod._decoder(model, h, 0, 4)
        loss_of(model, out, tgs[i], 4).backward()
    return d


def run_ctl(mod):
    model, mbs, tgs = make()
    d = {}
    _register_hooks(model, d)
    h = model.model.embed_tokens(mbs[0])
    out = mod._decoder(model, h, 0, 4)
    logits = F.linear(model.model.norm(out), model.lm_head.weight)
    loss = F.cross_entropy(
        logits.reshape(-1, logits.size(-1)), tgs[0].reshape(-1), ignore_index=-100
    ) / 4
    loss.backward()
    model.lm_head(out.detach())
    for i in range(1, 4):
        h = model.model.embed_tokens(mbs[i])
        out = mod._decoder(model, h, 0, 4)
        loss_of(model, out, tgs[i], 4).backward()
    return d


def afab_violation_at(keys):
    bwd = False
    for k in keys:
        if k.endswith(".bwd"):
            bwd = True
        if k.endswith(".fwd") and bwd:
            return k
    return None


def report(tag, d):
    keys = list(d)
    counts = {k: len(v) for k, v in d.items()}
    print(f"[{tag}] keys({len(keys)}): " + " ".join(keys))
    print(f"[{tag}] counts: " + " ".join(f"{k}={counts[k]}" for k in keys))
    print(f"[{tag}] afab_would_fire_at: {afab_violation_at(keys)}")


def main():
    mods = {
        "afab(q1-ref loop)": load(SEAT / "case-1f1b" / "pipeline_parallel.py", "pp_1f1b"),
        "1f1b(loop order changed)": load(SEAT / "case-1f1b" / "pipeline_parallel.py", "pp_1f1b2"),
        "ctl(functional head, late lm_head)": load(SEAT / "case-ctl" / "pipeline_parallel.py", "pp_ctl"),
    }
    # the q1-ref loop itself, via the frozen case module
    ref = load(Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round67/pipe/"
                    "cases/q1-ref/pipeline_parallel.py"), "pp_ref")
    report("afab/q1-ref", run_afab(ref))
    report("1f1b", run_1f1b(mods["1f1b(loop order changed)"]))
    report("ctl", run_ctl(mods["ctl(functional head, late lm_head)"]))
    print("PROBE_SHA " + hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
