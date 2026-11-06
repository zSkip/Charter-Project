"""A friction only: 36 sections (72 m) at grip 0.3, catch net at the end. Detailed sections 1-2, simple after.

Fusion design: "DRR A Friction Only" (links "DRR Base Section", "DRR Base Section Simple" and "DRR Catch Net").
Run one stage per MCP call (see ../../progress.md, "Folder layout and export method"):
    import runpy; runpy.run_path(r"<this file>")["main"]("<stage>")
Stages: open, layout, drone, check, save, shots, export.
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

STAGES = [
    ("open", lambda: B.open_or_new("DRR A Friction Only", B.vparams("A"), "Phase 2: A friction only")),
    ("layout", lambda: (L.set_params(B.vparams("A")), B.step_layout(detailed=(0, 1)))),
    ("drone", B.step_drone),
    ("check", lambda: (B.step_checks(), B.step_clash(3000, 5000), B.step_clash(69000, 72200),
                       B.report_stop("A grip 0.3", [(72, 0.3, 0)]), B.report_stop("A grip 0.2", [(72, 0.2, 0)]))),
    ("save", lambda: B.step_save("A run rebuilt by build_A.py")),
    ("shots", lambda: (
        B.shoot(F, "A_iso.png", (-30000, -40000, 25000), (36000, 0, 0)),
        B.shoot(F, "A_closeup.png", (67000, -6000, 3200), (72500, 0, 700), 10000))),
    ("export", lambda: B.export_f3d(F, "DRR_A_friction_only.f3d")),
]


def main(stage="all"):
    """Run one stage by name; "all" runs every stage except "open" and "save"."""
    names = [n for n, _ in STAGES]
    if stage != "all" and stage not in names:
        raise ValueError("stage must be one of %s or all" % names)
    for n, fn in STAGES:
        if n == stage or (stage == "all" and n not in ("open", "save")):
            fn()


def run(context):  # Fusion Scripts and Add-Ins entry point
    main("all")
