"""B braking zone: 12 standard sections, then 12 braking sections whose caps carry a high-grip (0.6) surface, shown as an appearance override. 48 m, catch net at the end. Detailed sections 1-2 and 12-13 (zone start).

Fusion design: "DRR B Braking Zone" (links "DRR Base Section", "DRR Base Section Simple" and "DRR Catch Net").
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
    ("open", lambda: B.open_or_new("DRR B Braking Zone", B.vparams("B"), "Phase 2: B braking zone")),
    ("layout", lambda: (L.set_params(B.vparams("B")), B.step_layout(detailed=(0, 1, 11, 12)))),
    ("drone", lambda: (B.step_drone(), B.step_bands([(12, 24, "DRR high grip 0.6", (205, 80, 30))]))),
    ("check", lambda: (B.step_checks(), B.step_clash(3000, 5000), B.step_clash(21000, 27000),
                       B.step_clash(45000, 48200), B.report_stop("B", [(24, 0.3, 0), (24, 0.6, 0)]))),
    ("save", lambda: B.step_save("B run rebuilt by build_B.py")),
    ("shots", lambda: (
        B.shoot(F, "B_iso.png", (-20000, -28000, 18000), (24000, 0, 0)),
        B.shoot(F, "B_closeup.png", (21000, -3500, 2600), (24000, 0, 650), 5000))),
    ("export", lambda: B.export_f3d(F, "DRR_B_braking_zone.f3d")),
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
