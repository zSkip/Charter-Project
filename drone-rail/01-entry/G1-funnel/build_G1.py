"""G1 funnel entry: 3 funnel sections + 3 linked base sections + drone stand-in.

Fusion design: "DRR Run G1 3-Section" (links "DRR Base Section", so save the base first).
Run one stage per MCP call (see ../../progress.md, "Folder layout and export method"):
    import runpy; runpy.run_path(r"<this file>")["main"]("<stage>")
Stages: open, clear, R1, R2, R3, L1, L2, L3, frames1, frames2, frames3, drone, check,
save, shots, export. The rail and frame stages each take 15-60 s; a time-out on the MCP
side usually still finishes in Fusion, so check with a readOnly script before re-running.
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
    ("open", lambda: B.activate(B.RUN_NAME)),
    ("clear", lambda: B.step_run_rails("", True)),
] + [("%s%d" % (sd, k + 1), (lambda sd=sd, k=k: B.step_run_rails(sd, False, [k])))
     for sd in "RL" for k in range(3)] + [
    ("frames%d" % (k + 1), (lambda k=k: B.step_run_frames([k], False))) for k in range(3)] + [
    ("drone", lambda: B.step_run_frames([], True)),
    ("check", lambda: (B.step_fix_funnel(), B.step_checks())),
    ("save", lambda: B.step_save("G1 run rebuilt by build_G1.py")),
    ("shots", lambda: (
        B.shoot(F, "G1_iso.png", (-4000, -9000, 6000), (6000, 0, 350)),
        B.shoot(F, "G1_closeup.png", (L.ev("funnel_sections * section_len") - 1200, -1500, 3650),
                (L.ev("funnel_sections * section_len"), 0, 650), 1500, [("Drone Stand-in",)]))),
    ("export", lambda: B.export_f3d(F, "DRR_G1_run_3_section.f3d")),
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
