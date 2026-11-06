"""D1 catch net: end-of-run net on two braced posts, as its own reusable design "DRR Catch Net",
shown at the end of a short 3-section run. Every other stopping version links the same net.

Fusion designs: "DRR Catch Net" (the net) and "DRR D1 Catch Net" (the run; links "DRR Base
Section" and "DRR Catch Net", so save those first).
Run one stage per MCP call (see ../../progress.md, "Folder layout and export method"):
    import runpy; runpy.run_path(r"<this file>")["main"]("<stage>")
Stages: open_net, net, save_net, export_net, open, layout, drone, check, save, shots, export.
"""
import os
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, *([os.pardir] * 2), "fusion-scripts"))
if LIB not in sys.path:
    sys.path.insert(0, LIB)
import drr_lib as L  # noqa: E402
import drr_build as B  # noqa: E402
importlib.reload(L)
importlib.reload(B)
F = os.path.relpath(HERE, B.ROOT).replace(os.sep, "/")
NAME = "DRR D1 Catch Net"

STAGES = [
    ("open_net", lambda: B.open_or_new(B.NET_NAME, B.PARAMS + B.NET_PARAMS, "Phase 2: D1 catch net (reusable)")),
    ("net", B.step_net),
    ("save_net", lambda: B.step_save("catch net rebuilt by build_D1.py")),
    ("export_net", lambda: B.export_f3d(F, "DRR_D1_net.f3d")),   # with DRR Catch Net active
    ("open", lambda: B.open_or_new(NAME, B.vparams("D1"), "Phase 2: D1 catch net on a short run")),
    ("layout", lambda: (L.set_params(B.vparams("D1")), B.step_layout(detailed=(0, 1, 2)))),
    ("drone", B.step_drone),
    ("check", lambda: (B.step_checks(), B.step_clash(-100, 7000))),
    ("save", lambda: B.step_save("D1 run rebuilt by build_D1.py")),
    ("shots", lambda: (
        B.shoot(F, "D1_iso.png", (-6000, -9000, 6000), (5000, 0, 600)),
        B.shoot(F, "D1_closeup.png", (2500, -5500, 3200), (7500, 0, 800), 9000))),
    ("export", lambda: B.export_f3d(F, "DRR_D1_catch_net.f3d")),
]


def main(stage="all"):
    """Run one stage by name; "all" runs every stage except the open and save ones."""
    names = [n for n, _ in STAGES]
    if stage != "all" and stage not in names:
        raise ValueError("stage must be one of %s or all" % names)
    for n, fn in STAGES:
        if n == stage or (stage == "all" and not n.startswith(("open", "save"))):
            fn()


def run(context):  # Fusion Scripts and Add-Ins entry point
    main("all")
