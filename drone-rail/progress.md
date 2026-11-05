# Drone Rail Recovery: build progress

## Fusion
- Project: **Drone Rail Recovery** (active hub), created 2026-11-05. Both designs are in its root folder.
- `DRR Base Section`: base section, **saved** 2026-11-05 after the Phase 1 fixes.
- `DRR Run G1 3-Section`: **saved** 2026-11-05 after the fixes, with its links updated to the latest base version.
  - Funnel: x 0–6 m (3 sections × 2000 mm). Linked base sections: x 6–12 m. Drone Stand-in: wing mid-chord at drone_x = 9000 mm, resting on the caps.
  - Root holds:
    - 3 linked `DRR Base Section` occurrences
    - `Funnel Rail R1`–`R3` and `L1`–`L3`: one component per funnel section and side, each with rail, wider cap, UHMW guide strip, springs, tongue and pins. Placed with transforms from `step_fix_funnel`.
    - `G1 Entry Funnel` holding `Funnel Section 1–3 Frames` (in place, parametric)
    - `Drone Stand-in`
  - If funnel parameters change, re-run `step_fix_funnel`.
- Build code: `fusion-scripts/drr_lib.py` (helpers) and `drr_build.py` (steps, plus the version-folder helpers `shoot`, `export_f3d`, `activate`, `step_save`). Each version folder has a `build_<ID>.py` that runs these steps in stages. See "Folder layout and export method" below.

## Built
- **Base section** (`DRR Base Section`). The root has `Half R`, `Half L` and `Frame Pin 1`/`2`. Each half holds its own components:
  - Rail Core: 6061 box tube with pin holes.
  - Rail Cap: crowned CFRP shell, 150 wide, 2 mm wall. Hollow box flanges and skirts that hug the core. R25 rounded nose upstream, joggled-down nose zone for the 100 mm shingle overlap, skirt-free tail hood downstream with an R1.5 tail edge, and 2 skirt slots.
  - 2 Spring Points (Coil Spring plus Guide Screw in a 50 mm slot, S1).
  - Splice Tongue and 2 Ball-lock Pins.
  - 2 U-frame Halves (the R half carries the bar splice tongue).
  - 2 Levelling Feet and 2 Bolt-down Plates (M1).
- **G1 run**, as above. Phase 1 fixes in the funnel:
  - **Step-free first cap.** `Funnel Rail R1`/`L1` caps have no lowered nose zone. The full-height cap runs from x=0 with the R25 nose, and the guide strip starts at x=0.
  - **Kinked exit splice.** On `Funnel Rail R3`/`L3`:
    - The core is extended and mitred, so its end face is square to the straight base core (a flush joint).
    - The tongue's downstream half and the 2 ball-lock pins are drawn along the base rail axis: the tongue is turned by `funnel_ang` about the vertical axis at the joint.
    - The cap's 100 mm tail hood is trimmed flush with the base cap's inner edge.
    - Checked: the exit pins sit on the base core centreline (x 6050/6100, y ±354). Cores, tongues and pins show no interference.
  - **Tapered guide strips.** UHMW strip thickness falls linearly with global x, from `guide_t` at x=0 to 0 at the funnel exit (6000). The strip faces then run straight from `funnel_gap0` to `rail_gap`, so the body keeps 25 mm side clearance at the exit.

## Parameters
- All of spec section 3 (metric), plus added detail params (comment "assumed" or "derived"), listed in `drr_build.py` `PARAMS`.
- The run design also gets `RUN_PARAMS`: funnel_sections, funnel_gap0, guide_t, funnel_cap_w, funnel_ang, drone_x, drone_sink.
- `step_run_rails('', True)` copies `PARAMS + RUN_PARAMS` into the run design. Fusion links geometry, not parameters.
- Changed 2026-11-05 (user-approved):

  | Parameter | Old | New |
  |---|---|---|
  | `tail_clear` | 150 mm | 330 mm |
  | `cap_wall` | 3 mm | 2 mm |
  | `core_wall` | 3 mm | 2 mm |
  | `cap_tail_r` | 2 mm | 1.5 mm |
  | `section_len` | 2400 mm | 2000 mm |

  As a result, funnel_ang = 2.96° and the funnel is 6.0 m long (spec G1 said 7.2 m at 2400 mm sections).

## Mass (base section, Fusion physical properties)
- 2 mm walls at 2400 mm sections: 25.73 kg per section, Half R 12.92 kg. Still over target.
- **Final, 2 mm walls at 2000 mm sections: 23.16 kg per section. Half R 11.63 kg, Half L 11.40 kg, frame pins 0.07 kg each.** Meets the 25 / 12.5 kg targets.
- Half R parts (kg): core 3.15, cap 3.36, 2 U-frame halves 2.14, 2 plates 0.94, 2 feet 1.00, tongue 0.44, 2 spring points 0.40, 2 pins 0.20.
- Materials:
  - Aluminum 6061: cores, tongues, frames, plates.
  - Steel: springs, screws, pins, feet.
  - "CFRP (carbon fibre)": a design material, a PEKK-CF copy with density 1550 kg/m³.

## Decisions (Phase 1, see spec; 8–11 added with the fixes)
1. Cap section is a mushroom shape: a 150 crowned top with hollow box flanges, and skirts 1 mm off the core, so the sketch's screw-in-slot works.
2. Shingle: each cap runs from x=0 to section_len + cap_overlap. The nose zone (first 100 mm) sits lower (cap_wall + cap_gap) and narrower, and nests under the previous cap's skirt-free tail hood.
3. Springs sit over the U-frame legs. Installed length 110 mm, 40 OD, 6 mm wire, 8 turns. One guide screw per spring point, on the outboard side.
4. Ball-lock pins are vertical, inserted from below.
5. The coil helix is computed from parameters when built. Re-run `step_base` after spring, wall or length changes.
6. Funnel caps widen outboard only. UHMW strips sit on the cap inner edges.
7. Parameters are copied into each design.
8. Funnel rails are one component per section and side, because the first, middle and last rails differ.
9. Exit transition is a kinked splice: mitred core, turned tongue half and pins, trimmed hood. There is no separate adapter section.
10. Strip taper uses global x across all 3 funnel sections, reaching 0 at the funnel exit.
11. Tail: the drone must meet "tail underside ≥ 330 mm above wing underside, or a V-/T-tail" (spec sections 2 and 11).

## Clearance checks (G1 run, after the fixes; "loaded" = springs fully compressed, drone 50 mm lower)
- Body to U-frame legs 80 mm (30 loaded). Body to rails, caps and strips **25.0 mm**: the body now reaches back over the funnel exit, and the trimmed hood keeps it at 25. PASS.
- Prop blades (vertical) to frames 171 mm (121 loaded). Blades to rails 249 mm. PASS.
- Risk 2, unchanged: the prop disc (spinning, or blades horizontal) reaches the caps and cores (0 mm; r 350 vs cap edge 279). The prop must stop vertical or fold.
- **Tail: 330 mm above the caps, 280 mm loaded. Pitch limit 6.28° at touchdown, 5.33° compressed. 5° drops the tail 261 mm. PASS.**
- Interference check (`analyzeInterference`, all 6 funnel rails plus base section 1; cores, caps, tongues, pins, strips): only open issue 1 below.

## Open issues for the user
1. **New: funnel-to-base cap crown clash.** The `Cap FR3` and `Cap FL3` tail hoods overlap the first base caps' nose zones by 1.31 cm³ per side, about 0.5 mm deep at 20–40 mm inboard of the core centreline (calculated).
   - Cause: the 250 mm funnel cap has a flatter crown (R 1305) than the 150 mm base cap (R 472). This has been there since Phase 1, at any funnel angle.
   - Fix options, needing the user's choice:
     - (a) give the last funnel cap's tail hood the base cap's crown over the overlap
     - (b) cap_gap 1 → 1.6 mm, which lowers every base nose zone
     - (c) a separate short transition cap
2. **.f3z is not available through the API.** `createFusionArchiveExportOptions` + `execute` only write .f3d. A ".f3z" file name gives "x.f3z.f3d". For the run, the .f3d is one self-contained archive with the linked base sections embedded. A true .f3z needs the Fusion UI (File > Export > .f3z) by hand.
3. Funnel length is now 6.0 m (3 × 2000), against "about 7.2 m" in spec G1. Use funnel_sections = 4 (8 m) if a longer funnel is wanted.
4. Assumed values to confirm: funnel_cap_w 250, guide_t 10, tail span 1800, prop hub at body mid-depth, spring and cap detail sizes (see params).

## Next
- Phase 1 fixes done. Phase 2 (the other 15 versions) follows the folder layout below, one session and one version at a time, after the user's go.

## Phase 1 fixes and folder layout: done (2026-11-05)
All 7 hand-over tasks are done:
- tail requirement
- mass (2 mm walls + 2000 mm sections)
- funnel exit transition
- step-free first cap
- tapered strips
- folder tree with 4 filled version folders (`screenshots/` removed; its PNGs are in the folders)
- no git changes

Both designs are saved.

## Folder layout and export method
Later sessions follow this exactly for every version.

### Tree (`drone-rail/`)
```
fusion-scripts/            shared code: drr_lib.py, drr_build.py (no version files here)
00-base-section/           ID base
01-entry/   G1-funnel/  G2-v-cradle/  G3-roller-guides/                     IDs G1 G2 G3
02-stopping/ A-friction-only/ B-braking-zone/ C-uphill-ramp/ D1-catch-net/ D2-rising-grip/ D3-arresting-cable/   IDs A B C D1 D2 D3
03-damping/ S1-springs-only/ S2-spring-shock/ S3-elastomer/                 IDs S1 S2 S3
04-mounting/ M1-levelling-feet/ M2-ground-anchors/ M3-weighted-feet/ M4-truck-trailer/ M5-ship-lashing/ M6-self-levelling/   IDs M1..M6
05-scale-model/            ID scale (Phase 3: STLs go here)
```
- Empty folders hold a `.gitkeep`. Delete it when the folder is filled.
- Filled so far: `00-base-section`, `01-entry/G1-funnel`, `03-damping/S1-springs-only`, `04-mounting/M1-levelling-feet`.

### What each version folder must contain
| File | Rule |
|---|---|
| `build_<ID>.py` | the script that builds, checks, pictures and exports the version (template below) |
| `<ID>_iso.png` | 1200×900 orthographic iso of the whole version, from `B.shoot` |
| `<ID>_closeup.png` | 1200×900 close-up of what is new in the version, from `B.shoot`, with `hide=` for parts in the way |
| `DRR_<ID>_<short_name>.f3d` | native export from `B.export_f3d`, one per design. A version that is only a part of the base exports that component, e.g. S1 `DRR_S1_spring_point.f3d`. A version with two parts writes two files, e.g. M1 `DRR_M1_levelling_foot.f3d` and `DRR_M1_bolt_down_plate.f3d`. |

- Only these files go in a version folder. The old Phase 1 pictures (`p1_*.png`, made before the fixes) stay where they were moved: base, G1 and S1.
- A new version gets its own Fusion design, saved in the project root folder as `DRR <ID> <Name>`, e.g. `DRR D3 Arresting Cable`.
- It links the base section with `root.occurrences.addByInsert(find_file(BASE_NAME), matrix, True)`, as `step_run_rails` does.
- New build steps go in `drr_build.py` as `step_<id>_<what>()`. Extend the existing functions rather than copy them.

### `build_<ID>.py` template
Copy `01-entry/G1-funnel/build_G1.py`, and keep the header byte for byte, apart from the `[os.pardir] * N`. N is 1 for `00-base-section` and `05-scale-model`, and 2 for every `0x-group/version` folder.
```python
"""<ID> <name>: one line on what it is. Fusion design: "DRR <ID> <Name>". Stages: ..."""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, *([os.pardir] * 2), "fusion-scripts"))
if LIB not in sys.path: sys.path.insert(0, LIB)
import drr_lib as L; import drr_build as B
importlib.reload(L); importlib.reload(B)
F = os.path.relpath(HERE, B.ROOT).replace(os.sep, "/")      # e.g. "02-stopping/D3-arresting-cable"
STAGES = [
    ("open",   lambda: B.activate("DRR <ID> <Name>")),       # new design: B.step_<id>_new() instead
    ("build",  B.step_<id>_build),                            # split into several stages if > ~40 s
    ("check",  B.step_checks),
    ("save",   lambda: B.step_save("<what changed>")),
    ("shots",  lambda: (B.shoot(F, "<ID>_iso.png", eye_mm, target_mm),
                        B.shoot(F, "<ID>_closeup.png", eye_mm, target_mm, width_mm, [("Comp", "Sub")]))),
    ("export", lambda: B.export_f3d(F, "DRR_<ID>_<short_name>.f3d")),   # or comp_path=("Half R", "Spring Point R1")
]
def main(stage="all"): ...   # copy from build_G1.py: "all" runs every stage except open and save
def run(context): main("all")
```

### Run stub (through `fusion_mcp_execute`, featureType "script")
Run one stage per call, in this order: `open` (always on its own), the build stages, `check`, `save`, `shots`, `export`.
```python
import runpy
def run(_context: str):
    runpy.run_path(r'C:\Users\skyon\Desktop\CharterProject\drone-rail\<folder>\build_<ID>.py')['main']('<stage>')
```
- `runpy.run_path` sets `__file__`, so the relative `fusion-scripts` path works, and each call reloads `drr_lib` and `drr_build`.
- To run a single library step: `g = runpy.run_path(<file>); g['B'].<step>()`.

### Export calls (tested 2026-11-05)
- `B.export_f3d(folder, name, comp_path=None)` runs:
  - `em = design.exportManager`
  - `opts = em.createFusionArchiveExportOptions(path)`, or `(path, component)` for one component
  - `em.execute(opts)`
- It deletes an old file first and raises if the file is missing or 0 bytes.
- The API writes **.f3d only**. A design with linked components (the G1 run) becomes one self-contained .f3d with the linked base sections embedded. Use .f3d for every version; a .f3z can only be made by hand in the UI.
- `B.shoot(folder, name, eye, target, extent=None, hide=())` saves a 1200×900 PNG through `viewport.saveAsImageFile`:
  - eye and target are in mm; extent is the view width in mm, or None to fit all
  - it raises on a missing or empty file
- After `shots`/`export` the document shows as modified (camera, visibility). `save` handles it: `B.step_save` runs `updateAllReferences()` first, so a run design picks up a newer base.
- Files written 2026-11-05 (bytes):

  | Folder | Files |
  |---|---|
  | `00-base-section` | `DRR_base_section.f3d` 5 998 146; `base_iso.png` 259 091; `base_closeup.png` 282 981 |
  | `01-entry/G1-funnel` | `DRR_G1_run_3_section.f3d` 20 440 075; `G1_iso.png` 442 075; `G1_closeup.png` 292 481 |
  | `03-damping/S1-springs-only` | `DRR_S1_spring_point.f3d` 1 904 764; `S1_iso.png` 245 981; `S1_closeup.png` 169 337 |
  | `04-mounting/M1-levelling-feet` | `DRR_M1_levelling_foot.f3d` 153 028; `DRR_M1_bolt_down_plate.f3d` 115 623; `M1_iso.png` 194 611; `M1_closeup.png` 184 995 |

### Gotchas (all seen in this session)
- **Switch documents in a call of its own** (`open` stage). Activating a document and building in the same script gives "VCS_SKETCH_OVER_CONSTRAINTS" in the first sketch.
- **MCP time-out is about 60 s.** A script that times out usually still finishes in Fusion, but once it did not apply at all. Always check with a `readOnly` script (occurrence names and counts, timeline count) before re-running.
- Keep each call under about 40 s: one funnel rail takes about 17 s, and one section of frames plus feet times out but completes.
- **Failed scripts do not always roll back.** A failed `step_base` left parameters changed and a half-built component. Make every step idempotent: delete its own occurrence by component name first, as `step_run_rails` and `step_run_frames` do.
- `MoveFeature.defineAsRotate` refused both a sketch line and a construction axis in a nested component ("Invalid entity"). Draw turned geometry in plan view with sin/cos expressions instead (see `turned()` in `build_rail`).
- `design.analyzeInterference(design.createInterferenceInput(bodies))` works for checks. Pass body proxies collected through `occurrence.bRepBodies` while walking `childOccurrences`.
- Fusion refuses two origin dimensions with the same value and direction in one sketch. `Sk.fix` aligns those points instead.
- Occurrence `transform2` can only be set on root-level occurrences. `addExistingComponent` compounds transforms, which is why funnel rails are now separate components placed with `transform2`.
- The coil helix and the funnel placement transforms are computed when built. Re-run the step after parameter changes.
