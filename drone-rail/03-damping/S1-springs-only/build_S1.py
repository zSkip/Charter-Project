"""S1 springs only: the spring point (coil spring + guide screw in a skirt slot) as sketched.

S1 is the default spring point of the base section, so it has no design of its own: it lives in
"DRR Base Section" (build_rail in ../../fusion-scripts/drr_build.py). The export is the
"Spring Point R1" component on its own.
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
    ("save", lambda: B.step_save("base section rebuilt by build_S1.py")),
    ("shots", lambda: (
        B.shoot(F, "S1_iso.png", (-500, 1950, 1500), (300, 354, 620), 520),
        B.shoot(F, "S1_closeup.png", (-500, 1950, 1500), (300, 354, 620), 320, [("Half R", "Rail Cap R")]))),
    ("export", lambda: B.export_f3d(F, "DRR_S1_spring_point.f3d", ("Half R", "Spring Point R1"))),
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
