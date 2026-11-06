"""D3 arresting cable: 6 sections (12 m), two cross cables near the entry between energy-absorber drums at the sides, and a hook on the drone stand-in. Stops at about 2 g; catch net at the end. Detailed sections 1-2 (cables), simple after.

Fusion design: "DRR D3 Arresting Cable" (links "DRR Base Section", "DRR Base Section Simple" and "DRR Catch Net").
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


def report():
    v = L.evu("landing_speed_kn", "") * 1852.0 / 3600.0
    d = v * v / (2 * L.evu("arrest_g", "") * B.G)
    print("D3: %.1f m to stop at %.1f g from cable 1 (x %.0f) -> x %.1f m of %.0f; force %.2f kN" % (
        d, L.evu("arrest_g", ""), L.ev("cable_x1"), d + L.ev("cable_x1") / 1000, L.ev("run_sections * section_len") / 1000,
        L.evu("drone_mass", "") * L.evu("arrest_g", "") * B.G / 1000))
    print("D3 clearances mm: hook to cross-bar top %.0f, toe top to cable %.0f, prop tip to cable top %.0f, body to cable %.0f" % (
        L.ev("hook_z - xbar_top_z"), L.ev("cable_z - cable_d / 2 - hook_z - hook_w / 2"),
        L.ev("rail_top_h - body_drop / 2 - prop_dia / 2 - cable_z - cable_d / 2"),
        L.ev("rail_top_h - body_drop - cable_z - cable_d / 2")))

STAGES = [
    ("open", lambda: B.open_or_new("DRR D3 Arresting Cable", B.vparams("D3"), "Phase 2: D3 arresting cable")),
    ("layout", lambda: (L.set_params(B.vparams("D3")), B.step_layout(detailed=(0, 1)))),
    ("drone", lambda: (B.step_drone(hook=True), B.step_d3_gear())),
    ("check", lambda: (B.step_checks(), B.step_clash(-100, 5000, ("Cable", "Drum", "DR ", "Frame ", "Foot ", "Plate ")),
                       B.step_clash(9000, 12200), report())),
    ("save", lambda: B.step_save("D3 run rebuilt by build_D3.py")),
    ("shots", lambda: (
        B.shoot(F, "D3_iso.png", (-9000, -12000, 8000), (6000, 0, 300)),
        B.shoot(F, "D3_closeup.png", (-2500, -5000, 1500), (1300, 0, 300), 5000))),
    ("export", lambda: B.export_f3d(F, "DRR_D3_arresting_cable.f3d")),
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
