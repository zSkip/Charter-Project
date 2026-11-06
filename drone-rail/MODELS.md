# Drone Rail Recovery: model gallery

Every model built so far, each with a picture of the whole model and a close-up of what is new in it. The drone stand-in is a 140 kg fixed-wing drone with a 6.1 m wingspan, landing at 40 knots. It rides on its wing roots on two sprung carbon caps and slides to a stop.

Stopping lengths use v² = 2·g·(grip·cos θ + sin θ)·d at 40 knots (20.6 m/s). Multiply them by about 1.27 for 45 knots. Full details are in [spec.md](spec.md) and the build log [progress.md](progress.md).

| Model | Group | Length | Status |
|---|---|---|---|
| [Base section](#base-section) | shared | 2 m | built |
| [Simple base section](#simple-base-section) | shared | 2 m | built |
| [G1 Funnel](#g1-funnel-entry) | entry | 12 m | built |
| [S1 Springs only](#s1-springs-only) | damping | one spring point | built |
| [M1 Levelling feet](#m1-levelling-feet) | mounting | one foot | built |
| [A Friction only](#a-friction-only) | stopping | 72 m | built |
| [B Braking zone](#b-braking-zone) | stopping | 48 m | built |
| [C Uphill ramp](#c-uphill-ramp) | stopping | 64 m | built, **kink joint open** |
| [D1 Catch net](#d1-catch-net) | stopping | 6 m + net | built |
| [D2 Rising grip](#d2-rising-grip) | stopping | 48 m | built |
| [D3 Arresting cable](#d3-arresting-cable) | stopping | 12 m | built |
| G2, G3, S2, S3, M2–M6, 1:10 scale model | | | not built yet |

---

## Base section
[00-base-section](00-base-section) · Fusion design `DRR Base Section`

| Whole model | Close-up |
|---|---|
| ![Base section](00-base-section/base_iso.png) | ![Base section close-up](00-base-section/base_closeup.png) |

The shared 2.0 m rail section that every version is built from. Each rail is an aluminium box core under a crowned carbon cap on two coil springs, with 50 mm of travel. Sections join with a splice tongue and two ball-lock pins, and the caps overlap 100 mm like roof shingles, so the wing never meets a step. Two split U-frames on levelling feet carry it. It weighs 23.2 kg per section and comes apart into two 11.6 kg halves.

## Simple base section
[00-base-section](00-base-section) · Fusion design `DRR Base Section Simple`

| Whole model | Close-up |
|---|---|
| ![Simple section](00-base-section/simple_iso.png) | ![Simple section close-up](00-base-section/simple_closeup.png) |

A light stand-in for long runs, used to keep Fusion fast and the files small. Cores, caps, U-frames and foot pads are plain bodies, with no springs, screws or pins. Runs use the detailed section for the first two sections and around anything new, and this one everywhere else. It is for looks and fit only, not for mass.

## G1 Funnel entry
[01-entry/G1-funnel](01-entry/G1-funnel) · Fusion design `DRR Run G1 3-Section`

| Whole model | Close-up: funnel exit |
|---|---|
| ![G1 funnel](01-entry/G1-funnel/G1_iso.png) | ![G1 funnel exit](01-entry/G1-funnel/G1_closeup.png) |

The touchdown end. Over the first 6 m the rails start 1.16 m apart and narrow to the standard gap, so a drone landing up to 300 mm off centre is steered back. The caps are wider in this zone, and tapered low-friction guide strips push the body into line. The close-up shows the exit joint. The last wide cap stops at the joint, and a short hood with the standard cap's crown nests over the first standard cap.

## S1 Springs only
[03-damping/S1-springs-only](03-damping/S1-springs-only)

| Whole model | Close-up |
|---|---|
| ![S1 spring point](03-damping/S1-springs-only/S1_iso.png) | ![S1 close-up](03-damping/S1-springs-only/S1_closeup.png) |

One spring point, as in the original sketch. A 90 N/mm coil spring sits between the core and the cap, and a guide screw runs in a vertical slot in the cap skirt. The screw limits travel to 50 mm and stops the cap lifting off. Expect some bounce, because nothing damps it.

## M1 Levelling feet
[04-mounting/M1-levelling-feet](04-mounting/M1-levelling-feet)

| Whole model | Close-up |
|---|---|
| ![M1 foot](04-mounting/M1-levelling-feet/M1_iso.png) | ![M1 close-up](04-mounting/M1-levelling-feet/M1_closeup.png) |

The default mounting on the base section: a threaded levelling foot under each U-frame leg, standing on a four-bolt plate that can be fixed to the ground.

## A Friction only
[02-stopping/A-friction-only](02-stopping/A-friction-only) · Fusion design `DRR A Friction Only`

| Whole run | Close-up: run end and net |
|---|---|
| ![A friction only](02-stopping/A-friction-only/A_iso.png) | ![A run end](02-stopping/A-friction-only/A_closeup.png) |

The simplest stop. There are 36 standard sections (72 m) at a grip of 0.3, and the drone stops at 71.9 m. If the grip drops to 0.2, the drone reaches the end still doing about 12 m/s, and the catch net at the end has to stop it.

## B Braking zone
[02-stopping/B-braking-zone](02-stopping/B-braking-zone) · Fusion design `DRR B Braking Zone`

| Whole run | Close-up: start of the braking zone |
|---|---|
| ![B braking zone](02-stopping/B-braking-zone/B_iso.png) | ![B zone start](02-stopping/B-braking-zone/B_closeup.png) |

There are 12 standard sections, then 12 braking sections whose caps carry a high-grip (0.6) surface, shown in orange. The run stops in 48 m, a third shorter than A.

## C Uphill ramp
[02-stopping/C-uphill-ramp](02-stopping/C-uphill-ramp) · Fusion design `DRR C Uphill Ramp`

| Whole run | Close-up: the kink |
|---|---|
| ![C uphill ramp](02-stopping/C-uphill-ramp/C_iso.png) | ![C kink](02-stopping/C-uphill-ramp/C_closeup.png) |

There are 18 flat sections (36 m), then 14 sections rising at 5° (28 m). Gravity helps friction slow the drone, and it stops at 63.9 m. The top end is 2.44 m higher, carried on braced steel trestles under every U-frame, with the catch net on raised columns. **Open issue:** at the kink, the straight splice tongue and its pins don't fit the next core, which is tilted 5°. The kink needs a bent splice or a hinged transition section, and the choice is open.

## D1 Catch net
[02-stopping/D1-catch-net](02-stopping/D1-catch-net) · Fusion designs `DRR Catch Net` (the net) and `DRR D1 Catch Net` (the short run)

| Short run with net | Close-up |
|---|---|
| ![D1 catch net](02-stopping/D1-catch-net/D1_iso.png) | ![D1 net close-up](02-stopping/D1-catch-net/D1_closeup.png) |

An end-of-run safety net on two braced steel posts. The net is 6.9 m wide and 150–1800 mm high, so it covers the whole drone with 400 mm to spare at each wingtip. It is a reusable design, and the same net stands 1.5 m past the end of every other stopping version as a backstop.

## D2 Rising grip
[02-stopping/D2-rising-grip](02-stopping/D2-rising-grip) · Fusion design `DRR D2 Rising Grip`

| Whole run | Close-up: grip bands |
|---|---|
| ![D2 rising grip](02-stopping/D2-rising-grip/D2_iso.png) | ![D2 bands](02-stopping/D2-rising-grip/D2_closeup.png) |

There are 24 sections (48 m) whose cap grip rises in six 8 m bands, from 0.2 at touchdown to 0.7 at the end, coloured blue (slippery) to red (grippy). The drone lands gently on the low grip and is braked harder as it slows. It stops at 48 m.

## D3 Arresting cable
[02-stopping/D3-arresting-cable](02-stopping/D3-arresting-cable) · Fusion design `DRR D3 Arresting Cable`

| Whole run | Close-up: cables, drums and hook |
|---|---|
| ![D3 arresting cable](02-stopping/D3-arresting-cable/D3_iso.png) | ![D3 close-up](02-stopping/D3-arresting-cable/D3_closeup.png) |

The shortest run: 6 sections (12 m). Two cables cross the run near the entry, 150 mm off the ground, each running to energy-absorber drums at both sides. A hook under the drone's body catches a cable and stops it at about 2 g (2.8 kN) in 10.8 m. **Open issue:** at full spring compression the hook would dip 10 mm below the frame cross bars, so it needs to be a sprung or pivoting hook.
