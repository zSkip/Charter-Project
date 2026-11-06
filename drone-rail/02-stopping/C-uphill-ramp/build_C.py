"""C uphill ramp: 18 flat sections, then 14 sections rising at 5 deg (turned about the cap-top
line at the kink), on braced trestles under every U-frame; end about 2.4 m up. Catch net at the
top on raised columns. Detailed sections 1-2 and 18-19 (the kink), simple elsewhere.

Fusion design: "DRR C Uphill Ramp" (links "DRR Base Section", "DRR Base Section Simple" and "DRR Catch Net").
Run one stage per MCP call (see ../../progress.md, "Folder layout and export method"):
    import runpy; runpy.run_path(r"<this file>")["main"]("<stage>")
Stages: open, layout, drone, trestles1, trestles2, check, save, shots, export.
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
    ("open", lambda: B.open_or_new("DRR C Uphill Ramp", B.vparams("C"), "Phase 2: C uphill ramp")),
    ("layout", lambda: (L.set_params(B.vparams("C")), B.step_layout(detailed=(0, 1, 17, 18), ramp_from=18))),
    ("drone", lambda: (B.step_drone(), B.step_c_net_base())),
    ("trestles1", lambda: B.step_c_trestles(range(18, 25))),
    ("trestles2", lambda: B.step_c_trestles(range(25, 32))),
    ("check", lambda: (B.step_checks(), B.step_clash(3000, 5000), B.step_clash(34000, 40000),
                       B.report_stop("C", [(36, 0.3, 0), (28, 0.3, 5)]),
                       print("C ramp rise %.0f mm" % (28000 * __import__("math").sin(L.evu("ramp_ang", "rad")))))),
    ("save", lambda: B.step_save("C run rebuilt by build_C.py")),
    ("shots", lambda: (
        B.shoot(F, "C_iso.png", (-20000, -40000, 15000), (32000, 0, 1000)),
        B.shoot(F, "C_closeup.png", (33000, -3500, 2500), (36100, 0, 650), 4500))),
    ("export", lambda: B.export_f3d(F, "DRR_C_uphill_ramp.f3d")),
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
