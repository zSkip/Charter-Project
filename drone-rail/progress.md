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
  - Task 0 (2026-11-05): root also holds `Exit Hood FR3`/`FL3` (built by stages R3/L3), see Phase 2 below.
- Phase 2 stopping designs (2026-11-05), all **saved** in the project root: `DRR Base Section Simple`, `DRR Catch Net`, `DRR A Friction Only`, `DRR B Braking Zone`, `DRR C Uphill Ramp`, `DRR D1 Catch Net`, `DRR D2 Rising Grip`, `DRR D3 Arresting Cable`.
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

- **Phase 2 stopping versions (2026-11-05).** Code is in `drr_build.py` under "Phase 2". Each run links `DRR Base Section` (detailed) for the first 2 sections and around what's new, `DRR Base Section Simple` everywhere else, and `DRR Catch Net` (D1) at the end, net_gap 1.5 m past the last section. Drone stand-in at x 3 m (touchdown) unless noted. Version parameters are in `VPARAMS`. Stop distances come from v² = 2·g·(μ cos θ + sin θ)·d at 40 kn.

  | Version | Design | Sections (detailed) | Length | Stops at | .f3d | Notes |
  |---|---|---|---|---|---|---|
  | Simple | `DRR Base Section Simple` | 1 | 2 m | – | 0.30 MB | 12 plain bodies: hollow core (with pin holes for the previous section's pins), solid cap with lowered nose and clearance over the core, U-frame halves, foot pads. No tongue, so a simple → detailed joint has no tongue. Not for mass. |
  | D1 | `DRR Catch Net` + `DRR D1 Catch Net` | 3 (all) | 6 m | – | 0.11 + 0.31 MB | Net: 2 braced 120 mm steel posts with plates, 29 × 8 nylon cords (mesh 246 × 236), span 6.9 m, 150–1800 mm high. Wingtips clear the posts by 400 mm. Drone shown 1.5 m short of the net. |
  | A | `DRR A Friction Only` | 36 (1–2) | 72 m | 71.9 m at 0.3 | 0.14 MB | At grip 0.2 it leaves the run at 11.9 m/s, so the net catches it |
  | B | `DRR B Braking Zone` | 24 (1–2, 12–13) | 48 m | 48.0 m | 0.19 MB | Sections 13–24 caps: appearance "DRR high grip 0.6" (orange) |
  | C | `DRR C Uphill Ramp` | 32 (1–2, 18–19) | 64 m (36 flat + 28 ramp) | 63.9 m | 1.19 MB | Ramp turned 5° about the cap-top line at the end of the hood at the kink. Rise 2.44 m. 14 `Ramp Trestles n` components (beam under the feet, 2 posts, X-brace above 600 mm; the first foot is 20 mm up, on its levelling stud). Net on 4 raised columns (`Net Base`). **Kink splice clash, open issue 5.** |
  | D2 | `DRR D2 Rising Grip` | 24 (1–2) | 48 m | 48.0 m | 0.46 MB | 6 bands of 4 sections, "DRR grip 0.2" to "0.7", blue → red |
  | D3 | `DRR D3 Arresting Cable` | 6 (1–2) | 12 m | 11.8 m (2 g from cable 1 at x 1.0 m, 10.8 m; 2.76 kN) | 0.21 MB | `Arresting Gear`: 2 cables (16 mm, z 150) and 4 absorber drums on plates. `DR Hook` on the stand-in (shank plus forward toe), throat 300 mm short of cable 1. See open issue 6. |

  - Checks, all versions: drone clearances unchanged (body to frames 80/30 loaded, body to rails 25.0, tail 330). Interference at the detailed ↔ simple joints and at the run ends is clear. The D3 check adds cables, drums, hook, frames, feet and plates near the entry: no new hits. The only hits are known ones inside the base (foot studs in the frame legs) and the prop disc (risk 2). C fails at the kink only (open issue 5).

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
1. **Resolved 2026-11-05 (option a): funnel-to-base cap crown clash.** The last funnel caps are now cut at the joint plane, and an `Exit Hood FR3`/`FL3` with the base cap's crown (R 472, 150 wide, 2 mm wall) covers the 100 mm overlap along the base rail axis. The interference check (all 6 funnel rails, both hoods, base section 1: 52 bodies) is clear. Body to rails is now 24.9 mm (was 25.0) at the inner corner of the cut funnel cap. The wing meets the funnel-to-base crown step (up to about 1.5 mm, 30 mm inboard) at the joint instead of at the hood tail.
2. **.f3z is not available through the API, and linked designs are NOT embedded in an .f3d.** `createFusionArchiveExportOptions` + `execute` only write .f3d, and a ".f3z" file name gives "x.f3z.f3d". Correction to Phase 1: the D1 run with 3 linked base sections exports at 0.11 MB, against 6.0 MB for the base alone, so a run .f3d holds only its own geometry plus references. G1's 20.5 MB is its own 6 funnel rails. Every linked design is therefore exported in its own folder: base and simple in `00-base-section`, the net in `D1-catch-net/DRR_D1_net.f3d`. A self-contained .f3z needs the Fusion UI (File > Export) by hand.
3. Funnel length is now 6.0 m (3 × 2000), against "about 7.2 m" in spec G1. Use funnel_sections = 4 (8 m) if a longer funnel is wanted.
4. Assumed values to confirm: funnel_cap_w 250, guide_t 10, tail span 1800, prop hub at body mid-depth, spring and cap detail sizes (see params).

5. **New, C: the 5° kink splice clashes.** At the joint from flat section 18 to the first ramp section, the straight splice tongue and its 2 ball-lock pins go into the core of the next section, which is tilted 5°. Hits per side: tongue 4.28 cm³, pins 1.14 and 0.65 cm³. The caps are clear, because the ramp turns about the cap-top line at the end of the hood, so the wing sees no step. Not redesigned. Options for the user:
   - (a) a kinked splice in pitch: tongue half and pins turned by ramp_ang, the same idea as the G1 exit
   - (b) a short hinged transition section
   - (c) a separate bent tongue part at the kink only
6. **New, D3: hook clearance under load.** The hook toe clears the U-frame cross-bar tops by 40 mm unloaded and about 32 mm at static sag (8 mm). At full spring compression (50 mm) it would be 10 mm below the bar tops. The hook needs to be sprung or pivoting, as real tailhooks are, or the cable height and toe need rethinking. Other D3 clearances: toe top to cable 12 mm (the throat), prop tip to cable top 65 mm (15 mm at full compression), body to cable 288 mm.
7. Assumed Phase 2 values to confirm (all parameters, comment "assumed"):
   - D1: net span = wingspan + 800, net 150–1800 mm high, mesh 250 mm, 120 mm posts, braces 1.5 m back, net 1.5 m past the run end
   - D3: cables at x 1.0 and 3.0 m, z 150 mm; drums 450 dia, 900 mm outboard of the rails; hook 1.2 m behind the wing
   - C: trestle tube 100, beam 100
   - B/D2: grip shown as cap appearance overrides, colouring the whole cap including the skirts; a real braking surface would be a coating on the crown only

## Next
- Phase 1 fixes done. Phase 2 stopping versions (A, B, C, D1, D2, D3) done 2026-11-05, apart from open issue 5 (C kink), which needs the user's choice.
- Left for later sessions: entry G2, G3; damping S2, S3; mounting M2–M6; Phase 3 scale model.

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
- Filled so far: `00-base-section` (base and simple), `01-entry/G1-funnel`, all 6 of `02-stopping/`, `03-damping/S1-springs-only`, `04-mounting/M1-levelling-feet`.

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
- The API writes **.f3d only**, and linked designs are not embedded (open issue 2). Export every linked design in its own folder. Use .f3d for every version; a .f3z can only be made by hand in the UI.
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
| `01-entry/G1-funnel` (task 0, re-exported) | `DRR_G1_run_3_section.f3d` 20 503 142; `G1_iso.png` 442 007; `G1_closeup.png` 294 559 |
| `00-base-section` (simple) | `build_simple.py`; `DRR_base_section_simple.f3d` 302 766; `simple_iso.png` 242 883; `simple_closeup.png` 257 210 |
| `02-stopping/A-friction-only` | `DRR_A_friction_only.f3d` 135 328; `A_iso.png` 174 057; `A_closeup.png` 290 534 |
| `02-stopping/B-braking-zone` | `DRR_B_braking_zone.f3d` 188 415; `B_iso.png` 144 710; `B_closeup.png` 250 741 |
| `02-stopping/C-uphill-ramp` | `DRR_C_uphill_ramp.f3d` 1 191 616; `C_iso.png` 295 783; `C_closeup.png` 261 440 |
| `02-stopping/D1-catch-net` | `DRR_D1_catch_net.f3d` (run) 114 056; `DRR_D1_net.f3d` (net design) 313 656; `D1_iso.png` 419 241; `D1_closeup.png` 385 293 |
| `02-stopping/D2-rising-grip` | `DRR_D2_rising_grip.f3d` 456 135; `D2_iso.png` 144 821; `D2_closeup.png` 204 964 |
| `02-stopping/D3-arresting-cable` | `DRR_D3_arresting_cable.f3d` 212 940; `D3_iso.png` 182 090; `D3_closeup.png` 207 878 |

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
- (Phase 2) **`addExistingComponent(comp, m)` adds the first occurrence's offset to m** for linked components: every simple section came out 4 m too far along. **Setting `transform2` on linked occurrences afterwards left every reference "broken"**, and even `deleteMe` failed; the fix was closing without saving and reopening. `place()` now does an `addByInsert` per section, and `step_layout` raises if a flat section is misplaced.
- (Phase 2) Inserting 24–36 linked sections takes over 60 s: the MCP call times out but completes. Check with a readOnly script.
- (Phase 2) `L.ext` extents are absolute model coordinates, so sketch on an origin plane (no `off`) when using it. An offset sketch plane doubles the offset.
- (Phase 2) Fusion restarted once mid-script (about 70 trestle extrudes per call). Keep builds to about 30–40 features per call.
- (Phase 2) Appearance overrides work on child occurrences of linked occurrences (`paint()`), per run instance.
