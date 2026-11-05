"""M1 levelling feet: levelling foot (pad, M16 stud, jam nut) on a 4-bolt bolt-down plate.

M1 is the default mounting of the base section, so it has no design of its own: it lives in
"DRR Base Section" (build_foot in ../../fusion-scripts/drr_build.py). The exports are the
"Levelling Foot R1" and "Bolt-down Plate R1" components on their own.
Run one stage per MCP call: import runpy; runpy.run_path(r"<this file>")["main"]("<stage>")
Stages: open, build (rebuilds the whole base section), save, shots, export.
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
    ("open", lambda: B.activate(B.BASE_NAME)),
    ("build", B.step_base),
    ("save", lambda: B.step_save("base section rebuilt by build_M1.py")),
    ("shots", lambda: (
        B.shoot(F, "M1_iso.png", (-1200, -1600, 1400), (300, 250, 250), 1100),
        B.shoot(F, "M1_closeup.png", (-300, -700, 600), (300, 354, 40), 320))),
    ("export", lambda: (
        B.export_f3d(F, "DRR_M1_levelling_foot.f3d", ("Half R", "Levelling Foot R1")),
        B.export_f3d(F, "DRR_M1_bolt_down_plate.f3d", ("Half R", "Bolt-down Plate R1")))),
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
