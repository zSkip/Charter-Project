"""Base section: one 2000 mm rail section, both halves, with S1 springs and M1 feet.

Fusion design: "DRR Base Section" in project "Drone Rail Recovery".
Run one stage per MCP call (see ../progress.md, "Folder layout and export method"):
    import runpy; runpy.run_path(r"<this file>")["main"]("<stage>")
Stages: open, build, save, shots, export.
"""
import os
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, *([os.pardir] * 1), "fusion-scripts"))
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
    ("save", lambda: B.step_save("base section rebuilt by build_base.py")),
    ("shots", lambda: (
        B.shoot(F, "base_iso.png", (-3000, -4000, 3500), (1000, 0, 350)),
        B.shoot(F, "base_closeup.png", (3550, 2150, 1800), (2050, 354, 590), 520))),
    ("export", lambda: B.export_f3d(F, "DRR_base_section.f3d")),
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
