"""D2 rising grip: 24 sections (48 m) whose cap grip rises from 0.2 to 0.7 in 6 bands of 4 sections (0.1 steps), shown as appearance bands, blue (low) to red (high). Catch net at the end. Detailed sections 1-2.

Fusion design: "DRR D2 Rising Grip" (links "DRR Base Section", "DRR Base Section Simple" and "DRR Catch Net").
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
BANDS = [(4 * i, 4 * i + 4, "DRR grip %.1f" % (0.2 + 0.1 * i), rgb) for i, rgb in enumerate(
    [(50, 90, 200), (40, 160, 210), (60, 170, 90), (220, 200, 50), (235, 130, 40), (200, 40, 40)])]

STAGES = [
    ("open", lambda: B.open_or_new("DRR D2 Rising Grip", B.vparams("D2"), "Phase 2: D2 rising grip")),
    ("layout", lambda: (L.set_params(B.vparams("D2")), B.step_layout(detailed=(0, 1)))),
    ("drone", lambda: (B.step_drone(), B.step_bands(BANDS))),
    ("check", lambda: (B.step_checks(), B.step_clash(3000, 5000), B.step_clash(45000, 48200),
                       B.report_stop("D2", [(8, 0.2 + 0.1 * i, 0) for i in range(6)]))),
    ("save", lambda: B.step_save("D2 run rebuilt by build_D2.py")),
    ("shots", lambda: (
        B.shoot(F, "D2_iso.png", (-20000, -28000, 18000), (24000, 0, 0)),
        B.shoot(F, "D2_closeup.png", (10000, -7000, 6000), (17000, 0, 650), 14000))),
    ("export", lambda: B.export_f3d(F, "DRR_D2_rising_grip.f3d")),
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
