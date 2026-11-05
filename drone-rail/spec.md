# Drone Rail Recovery System: Build Spec

**Status:** draft for approval. Nothing gets modelled until the user says go.
**Purpose:** mock concept and prototype. Several versions are wanted.
**Units:** metric (mm unless stated).
**Reference sketch:** [sketch-page63.jpg](sketch-page63.jpg), notebook page 63.

---

## 1. What it is

Two straight, parallel rails, each topped with a sprung carbon fibre cap. A fixed-wing drone lands with its body between the rails and its wing roots on the caps. It then slides to a smooth, slow stop. The system is built from portable sections and must work on the ground, on vehicles and on ship decks.

Reading the sketch: the top two views show one rail end twice, unloaded (spring extended, screw at the bottom of its slot) and loaded (spring compressed, screw at the top). The bottom view is the rail pair on its frame, with the drone arriving at the far end. The bend at the near end is dropped for now, so the rails are straight.

---

## 2. Drone (a simple stand-in, used only to check clearances)

| Item | Value | Source |
|---|---|---|
| Mass | 140.6 kg (310 lb) | user |
| Wingspan | 6100 mm (20 ft) | user |
| Body width | 432–508 mm. Design to 508 | user |
| Wing underside to body bottom | 254 mm (10 in) | user |
| Rail contact point | Wing root, where the wing blends into the body | user |
| Propeller | One tractor (puller) prop at the nose | user |
| Prop diameter / state at touchdown | 700 mm, stopped with the blades vertical | **assumed: confirm** |
| Wing position / tail | High wing. **Drone requirement:** horizontal tail underside at least 330 mm above the wing underside, or a V-tail or T-tail, for landings up to 5° nose-up | user (approved 2026-11-05) |
| Landing speed | 40 knots (20.6 m/s) nominal, 45 knots design maximum | user / assumed |
| Sink rate at touchdown | Up to 1.5 m/s | assumed (user has no data) |
| Crosswind | Up to 15 knots | assumed (user has no data) |
| Side-to-side landing error | Up to ±300 mm. The rails must guide it back to the centre | user / assumed |
| Body length, wing chord (stand-in only) | 4000 mm, 600 mm | assumed |

Landing conditions vary, so speed, sink rate and grip are parameters, not fixed values.

---

## 3. Fusion setup

- Create a new Fusion project called **Drone Rail Recovery** and save each design into it. Saving is what lets the shared section be linked into every version. *(Needs user approval.)*
- Every size is a **User Parameter**. Values that aren't lengths can be unitless numbers named with their unit, for example `landing_speed_kn`.
- The **base section** is one design. Each version is its own assembly design that **links** the base section, so a change to the base flows into every version.
- Each part is its own component: rail core, cap, spring point, U-frame, foot, joint pins and so on.
- The Fusion MCP has no undo history across sessions, so verify each step with a screenshot. Never save unless the user has approved saving.

### User parameters (defaults)

| Name | Default | Meaning |
|---|---|---|
| `drone_mass` | 140.6 (kg) | |
| `wingspan` | 6100 mm | stand-in |
| `body_width` | 508 mm | |
| `body_drop` | 254 mm | wing underside to body bottom |
| `prop_dia` | 700 mm | |
| `tail_clear` | 330 mm | tail underside above wing underside (drone requirement, sections 2 and 11) |
| `landing_speed_kn` | 40 | |
| `sink_rate_ms` | 1.5 | |
| `grip` | 0.3 | friction coefficient, cap on wing |
| `max_offset` | 300 mm | side-to-side landing error |
| `side_clear` | 25 mm | gap between body and cap each side |
| `rail_gap` | `body_width + 2 * side_clear` (558 mm) | inner gap between caps |
| `cap_width` | 150 mm | |
| `cap_wall` | 2 mm | was 3 mm; 2 mm for the 25 kg target (approved 2026-11-05) |
| `cap_overlap` | 100 mm | shingle overlap at joints |
| `core_w` / `core_h` / `core_wall` | 50 / 100 / 2 mm | aluminium core tube (wall was 3 mm) |
| `rail_top_h` | 700 mm | ground to cap top, unloaded |
| `section_len` | 2000 mm | was 2400 mm; 2000 mm for the 25 kg target (approved 2026-11-05) |
| `frame_inset` | 300 mm | U-frame position from the section end |
| `spring_travel` | 50 mm | |
| `spring_rate` | 90 (N/mm) | per wing contact point |
| `springs_per_cap` | 2 | |
| `section_count` | 30 | for the run length |
| `model_scale` | 0.1 | printable model |

Rail centre-to-centre spacing comes out at `rail_gap + cap_width`, about 708 mm.

---

## 4. Base rail section (full scale, 2000 mm; was 2400 mm)

- **Core:** two rails, each a 6061 aluminium box tube, 50 W × 100 H × 2 mm wall.
- **Cap:** a carbon fibre cap over each core. It has a rounded (crowned) top 150 mm wide, 2 mm walls, and sides that drop down over the core. Each end gets a rounded nose, as in the sketch.
- **Suspension (from the sketch):** two spring points per cap. Each one is:
  - a vertical coil spring between the top of the core and the underside of the cap, and
  - a screw through a vertical slot in the side of the cap into the core. It limits travel to 50 mm and stops the cap lifting off.
  - Default rate 90 N/mm, sized so a 1.5 m/s drop stops within 50 mm. Peak load is about 4.5 kN per side (about 3.3 g). The cap sinks about 8 mm under the drone's weight alone.
- **Joints between sections:**
  - A splice tongue on the downstream end of each core slides into the next core, locked by two quick-release ball-lock pins per rail.
  - The caps **overlap 100 mm like roof shingles**: each cap's tail sits on top of the next cap's nose. A loaded cap pushes the next one down with it, so the wing never meets a step up.
- **Frame:** two open U-frames per section, 300 mm in from each end. Each has one leg under each rail and a cross bar at ground level, its top no higher than 80 mm, so the body and prop tip pass over it freely. Each U-frame splits at the middle with a pin joint, so a section comes apart into two single-rail halves.
- **Weight target:** no more than 25 kg per section (two people or a vehicle) and 12.5 kg per half (one person). Built: 23.2 kg per section, 11.6 kg per half (2 mm walls, 2000 mm sections).
- **Clearance checks** with the drone stand-in, springs fully compressed:
  - body bottom above the cross bars
  - prop tip above the cross bars and clear of the rails
  - tail underside above the cap tops

---

## 5. Entry and centring (touchdown end)

| Version | How it centres the drone |
|---|---|
| **G1 Funnel** | Over the first 3 sections (7.2 m) the rails start wider apart and narrow to the standard gap. The starting inner gap is about 1160 mm: body width, plus twice `max_offset`, plus clearance. Low-friction UHMW guide strips on the inner faces, at body height, push the body into line. The caps are wider in this zone. |
| **G2 V-cradle** | The caps tilt inward about 12°, so the sloped wing root slides itself to the centre. Good for small errors of about ±100 mm. |
| **G3 Roller guides** | Same layout as G1, but with vertical rollers instead of guide strips. |

---

## 6. Stopping versions

All lengths are for 40 knots and are best case. Lift at touchdown and varying conditions make real runs longer. At 45 knots, multiply every length by about 1.27. The kinetic energy is about 30 kJ at 40 knots and about 38 kJ at 45 knots.

| Version | How it stops | Run length |
|---|---|---|
| **A** Friction only | Grip 0.3 the whole way; 0.2 needs about 108 m | ~72 m (30 sections) |
| **B** Braking zone | 10 standard sections, then 10 sections with a high-grip (0.6) cap surface | ~48 m (20 sections) |
| **C** Uphill end ramp | 15 flat sections, then 12 sections at 5°. The end sits about 2.5 m high on taller legs | ~65 m (27 sections) |
| **D1** Catch net | An end-of-run net on posts. Also added as a safety backstop on every version | n/a |
| **D2** Grip that rises along the run | Cap grip goes from 0.2 to 0.7 along the run (show it as appearance bands) | ~48 m (20 sections) |
| **D3** Arresting cable | Two cross cables near the entry, with energy-absorber drums at the sides and a hook on the drone stand-in. Stops at about 2 g | ~12 m (5 sections) |

Long runs can use simplified or patterned copies of the linked section to keep Fusion responsive.

---

## 7. Damping versions (one design per spring point)

| Version | What's at each spring point |
|---|---|
| **S1** | Spring only, as sketched. Expect the drone to bounce |
| **S2** | Spring plus a hydraulic or gas shock absorber (coilover style) |
| **S3** | Elastomer (rubber) blocks |

---

## 8. Mounting versions

| Version | Mounting |
|---|---|
| **M1** | Levelling feet with bolt-down plates. Default on the base section |
| **M2** | Ground stakes or screw-in anchors for soil |
| **M3** | Weighted feet for surfaces you can't drill (tarmac, decks) |
| **M4** | Truck-bed or trailer adapter |
| **M5** | Ship-deck lashing points |
| **M6** | Self-levelling mount that cancels a ship's roll and pitch. Concept: a 2-axis gimbal base with actuators |

---

## 9. Small-scale model for 3D printing

- **Scale:** 1:10, so one section is 240 mm long.
- **Printer bed:** 220 × 220 mm assumed. **Confirm.** Split parts to fit.
- **Minimum wall:** 1.2 mm. Thicken scaled caps and tubes as needed.
- **Fits:** 0.2 mm clearance on parts that slide.
- **Hardware:** small real springs or printed flexures, and 2 mm steel pins or M2 screws.
- **Parts:** base section (rails, caps, U-frames), one spring point, one entry funnel section, drone stand-in.
- **Output:** export the STLs to `drone-rail/05-scale-model/` (folder layout in `progress.md`).

---

## 10. Build phases

1. **Phase 1:**
   - Fusion project, parameters and drone stand-in.
   - Base section in full detail, with S1 springs and M1 feet.
   - A 3-section run with the G1 entry funnel.
   - Clearance checks, a weight estimate and screenshots.
   - **Report back.**
2. **Phase 2:** every other version (G2–G3, A–D3, S2–S3, M2–M6). Report back.
3. **Phase 3:** the 1:10 printable parts and STL export. Report back.

Stop and report back as soon as anything blocks the work or a clearance check fails.

---

## 11. Risks to watch

1. **Tail strike.** If the underside of the horizontal tail sits lower than the wing underside at landing pitch, the tail hits the rails before the wing does. Nose-up at touchdown makes this worse: 5° drops a tail 3 m back by about 260 mm. **Drone requirement:** horizontal tail underside at least 330 mm above the wing underside, or a V-tail or T-tail, for landings up to 5° nose-up. That leaves 280 mm with the springs fully compressed (limit about 5.3° compressed, 6.3° at touchdown).
2. **Prop strike.** The rails' inner edges are about 280 mm from the centreline, but a 700 mm prop reaches 350 mm. A spinning prop, or one stopped with the blades horizontal, hits the rails. It has to be stopped with the blades vertical, or be a folding prop.
3. **Stopping lengths are best case.** See section 6.
4. **Wear and heat at the wing root.** About 30 kJ per landing goes into the patches where the wing touches the caps.
5. **Setup time.** A run needs 20–30+ sections.

---

## 12. Open items

On 2026-11-05 the user approved this spec ("yes start it"). Every open item uses its default until the user says otherwise.

- [x] Prop: 700 mm, stopped with the blades vertical (default)
- [x] High wing; tail underside at least 330 mm above the wing underside, or a V-tail or T-tail (drone requirement, approved 2026-11-05; was 150 mm)
- [x] Printer bed 220 × 220 mm, 1:10 scale (default)
- [x] Create the Fusion project "Drone Rail Recovery" and save designs into it (approved with the spec)
- [x] Phased build, with a report back after each phase (approved)

## 13. Token budget

The user set a **hard limit of 400k tokens** for any one build session. Check usage at every milestone. As usage nears about 320k, stop at a clean point, update `progress.md` and report back. The planning session then starts a fresh session to carry on from `progress.md`.
