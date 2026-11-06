"""Phase 1 build steps for the Drone Rail Recovery concept (see ../spec.md).

Coordinates: X along the rail (touchdown end at x=0, drone travels +X),
Y across, Z up. Ground at z=0. All sizes are User Parameters (mm).
"""
import math
import os
import adsk.core
import adsk.fusion
import drr_lib as L

app = L.app
PROJECT = 'Drone Rail Recovery'
BASE_NAME = 'DRR Base Section'
RUN_NAME = 'DRR Run G1 3-Section'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../drone-rail

# (name, expression, units, comment). Spec section 3 first, then added detail.
PARAMS = [
    ('drone_mass', '140.6', 'kg', 'spec: drone mass (310 lb)'),
    ('wingspan', '6100 mm', 'mm', 'spec: stand-in wingspan (20 ft)'),
    ('body_width', '508 mm', 'mm', 'spec: body width, design value'),
    ('body_drop', '254 mm', 'mm', 'spec: wing underside to body bottom'),
    ('prop_dia', '700 mm', 'mm', 'spec: prop diameter, stopped blades vertical'),
    ('tail_clear', '330 mm', 'mm', 'spec: tail underside above wing underside (drone requirement, 5 deg landing pitch)'),
    ('landing_speed_kn', '40', '', 'spec: landing speed, knots'),
    ('sink_rate_ms', '1.5', '', 'spec: sink rate at touchdown, m/s'),
    ('grip', '0.3', '', 'spec: friction coefficient, cap on wing'),
    ('max_offset', '300 mm', 'mm', 'spec: side-to-side landing error'),
    ('side_clear', '25 mm', 'mm', 'spec: gap between body and cap each side'),
    ('rail_gap', 'body_width + 2 * side_clear', 'mm', 'spec: inner gap between caps'),
    ('cap_width', '150 mm', 'mm', 'spec'),
    ('cap_wall', '2 mm', 'mm', 'spec (was 3 mm; 2 mm for the 25 kg target)'),
    ('cap_overlap', '100 mm', 'mm', 'spec: shingle overlap at joints'),
    ('core_w', '50 mm', 'mm', 'spec: aluminium core tube width'),
    ('core_h', '100 mm', 'mm', 'spec: aluminium core tube height'),
    ('core_wall', '2 mm', 'mm', 'spec (was 3 mm; 2 mm for the 25 kg target)'),
    ('rail_top_h', '700 mm', 'mm', 'spec: ground to cap top, unloaded'),
    ('section_len', '2000 mm', 'mm', 'spec (was 2400 mm; 2000 mm for the 25 kg target)'),
    ('frame_inset', '300 mm', 'mm', 'spec: U-frame position from section end'),
    ('spring_travel', '50 mm', 'mm', 'spec'),
    ('spring_rate', '90', '', 'spec: N/mm per wing contact point'),
    ('springs_per_cap', '2', '', 'spec'),
    ('section_count', '30', '', 'spec: sections for the run length'),
    ('model_scale', '0.1', '', 'spec: printable model scale'),
    # ---- added geometry detail (assumed in Phase 1, see progress.md)
    ('body_len', '4000 mm', 'mm', 'spec sec 2 (assumed): stand-in body length'),
    ('wing_chord', '600 mm', 'mm', 'spec sec 2 (assumed): stand-in wing chord'),
    ('wing_thk', '80 mm', 'mm', 'assumed: stand-in wing thickness'),
    ('tail_arm', '3000 mm', 'mm', 'assumed (spec risk 1): wing mid-chord to tail'),
    ('tail_span', '1800 mm', 'mm', 'assumed: horizontal tail span'),
    ('tail_chord', '400 mm', 'mm', 'assumed'),
    ('tail_thk', '30 mm', 'mm', 'assumed'),
    ('prop_blade_w', '60 mm', 'mm', 'assumed: blade width'),
    ('prop_blade_t', '20 mm', 'mm', 'assumed'),
    ('prop_disc_t', '4 mm', 'mm', 'prop disc stand-in thickness'),
    ('rail_cc', 'rail_gap + cap_width', 'mm', 'derived: rail centre-to-centre'),
    ('cap_crown', '6 mm', 'mm', 'assumed: crown rise across the cap'),
    ('cap_flange_d', '35 mm', 'mm', 'assumed: cap flange depth at the edges'),
    ('cap_nose_r', '25 mm', 'mm', 'assumed: rounded nose radius, upstream end'),
    ('cap_tail_r', '1.5 mm', 'mm', 'assumed: edge radius, downstream (top shingle) end; below cap_wall'),
    ('cap_gap', '1 mm', 'mm', 'assumed: skirt-to-core and shingle nesting gap'),
    ('spring_len', '110 mm', 'mm', 'assumed: installed spring length, unloaded'),
    ('spring_od', '40 mm', 'mm', 'assumed'),
    ('spring_wire', '6 mm', 'mm', 'assumed'),
    ('spring_coils', '8', '', 'assumed: coil turns'),
    ('screw_d', '8 mm', 'mm', 'assumed: M8 guide screw'),
    ('screw_head_d', '16 mm', 'mm', 'assumed'),
    ('screw_head_t', '5 mm', 'mm', 'assumed'),
    ('screw_drop', '25 mm', 'mm', 'assumed: screw axis below core top'),
    ('skirt_margin', '10 mm', 'mm', 'assumed: skirt below slot bottom'),
    ('slot_clear', '1 mm', 'mm', 'assumed: slot width over screw'),
    ('tongue_len', '300 mm', 'mm', 'assumed: splice tongue, half protrudes'),
    ('slide_fit', '0.5 mm', 'mm', 'assumed: sliding clearance, full scale'),
    ('pin_d', '10 mm', 'mm', 'assumed: ball-lock pin'),
    ('pin_head_d', '25 mm', 'mm', 'assumed'),
    ('pin_head_t', '8 mm', 'mm', 'assumed'),
    ('pin_x1', '50 mm', 'mm', 'assumed: pin positions past the joint'),
    ('pin_x2', '100 mm', 'mm', 'assumed'),
    ('frame_tube', '40 mm', 'mm', 'assumed: U-frame square tube'),
    ('frame_wall', '3 mm', 'mm', 'assumed'),
    ('split_gap', '2 mm', 'mm', 'assumed: gap at the U-frame split'),
    ('xbar_splice', '60 mm', 'mm', 'assumed: cross-bar splice tongue reach'),
    ('frame_pin_d', '12 mm', 'mm', 'assumed: U-frame split pin'),
    ('foot_h', '30 mm', 'mm', 'assumed: ground to frame underside'),
    ('foot_plate_w', '150 mm', 'mm', 'assumed: bolt-down plate'),
    ('foot_plate_t', '8 mm', 'mm', 'assumed'),
    ('foot_bolt_d', '13 mm', 'mm', 'assumed'),
    ('foot_bolt_pitch', '110 mm', 'mm', 'assumed'),
    ('foot_pad_d', '80 mm', 'mm', 'assumed'),
    ('foot_pad_t', '10 mm', 'mm', 'assumed'),
    ('foot_stud_d', '16 mm', 'mm', 'assumed: M16 levelling stud'),
    ('core_top_z', 'rail_top_h - cap_wall - spring_len', 'mm', 'derived'),
    ('core_bot_z', 'core_top_z - core_h', 'mm', 'derived'),
    ('screw_z', 'core_top_z - screw_drop', 'mm', 'derived'),
    ('skirt_bot_z', 'screw_z - screw_d / 2 - skirt_margin', 'mm', 'derived'),
    ('flange_bot_z', 'rail_top_h - cap_crown - cap_flange_d', 'mm', 'derived'),
    ('skirt_out', 'core_w / 2 + cap_gap + cap_wall', 'mm', 'derived: skirt outer face from core centre'),
    ('xbar_top_z', 'foot_h + frame_tube', 'mm', 'derived: cross-bar top (spec: 80 mm max)'),
]

RUN_PARAMS = [
    ('funnel_sections', '3', '', 'spec G1: funnel length in sections'),
    ('funnel_gap0', 'body_width + 2 * max_offset + 2 * side_clear', 'mm', 'spec G1: starting inner gap at guide strips'),
    ('guide_t', '10 mm', 'mm', 'assumed: UHMW guide strip thickness'),
    ('funnel_cap_w', '250 mm', 'mm', 'assumed: G1 wider cap'),
    ('funnel_ang', 'atan((funnel_gap0 + 2 * guide_t - rail_gap) / 2 / (funnel_sections * section_len))', 'deg', 'derived: funnel rail angle'),
    ('drone_x', '(funnel_sections + 1.5) * section_len', 'mm', 'stand-in wing mid-chord position along the run'),
    ('drone_sink', '0 mm', 'mm', 'stand-in drop below unloaded cap top'),
]


# ---------------------------------------------------------------- parts
def cap_section(yc, S, cy, cw, lower):
    """Cap cross-section at x=0 (crowned top, flanges, skirts round the core) as Sk.poly args.
    lower: the nose zone, lowered and narrowed by cap_wall + cap_gap to nest under a tail hood."""
    yC = '((%s) %s (%s))' % (yc, S, cy)
    hw = '((%s) / 2)' % cw
    R = '((((%s) / 2)^2 + cap_crown^2) / (2 * cap_crown))' % cw
    d2 = '(cap_wall + cap_gap)'
    if lower:
        h = '(%s - %s)' % (hw, d2)
        ze = '(rail_top_h - %s - (%s - sqrt(%s^2 - %s^2)))' % (d2, R, R, h)
        top = '(rail_top_h - %s)' % d2
    else:
        h, ze, top = hw, '(rail_top_h - cap_crown)', 'rail_top_h'
    yl, yr = '(%s - %s)' % (yC, h), '(%s + %s)' % (yC, h)
    sl, sr = '((%s) - skirt_out)' % yc, '((%s) + skirt_out)' % yc
    X = '0 mm'
    P = [(X, yl, ze), (X, yr, ze), (X, yr, 'flange_bot_z'), (X, sr, 'flange_bot_z'),
         (X, sr, 'skirt_bot_z'), (X, sl, 'skirt_bot_z'), (X, sl, 'flange_bot_z'),
         (X, yl, 'flange_bot_z')]
    return P, {0: ((X, yC, top), R)}


def build_hood(parent, tag, yc, x0):
    """Base-cap tail hood (crowned top and flange walls, no skirts, as on the base cap past
    section_len) from x0 to x0 + cap_overlap on a straight rail at yc. Task 0: it replaces the
    last funnel cap's flatter hood, so it nests over the base cap's nose like any base joint."""
    c, _ = L.newcomp(parent, 'Exit Hood %s' % tag)
    hw = '(cap_width / 2)'
    R = '(((cap_width / 2)^2 + cap_crown^2) / (2 * cap_crown))'
    Ri = '(%s - cap_wall)' % R
    zi = '(rail_top_h - %s + sqrt(%s^2 - (%s - cap_wall)^2))' % (R, Ri, hw)
    fb = '(flange_bot_z + cap_wall)'

    def y(e):
        return '(%s) + (%s)' % (yc, e)
    X = '0 mm'
    hi = '%s - cap_wall' % hw
    P = [(X, y('-' + hw), 'rail_top_h - cap_crown'), (X, y(hw), 'rail_top_h - cap_crown'), (X, y(hw), fb),
         (X, y(hi), fb), (X, y(hi), zi), (X, y('-(%s)' % hi), zi), (X, y('-(%s)' % hi), fb), (X, y('-' + hw), fb)]
    k = L.Sk(c, 'YZ')
    k.poly(P, {0: ((X, yc, 'rail_top_h'), R), 4: ((X, yc, 'rail_top_h - cap_wall'), Ri)})
    sk = k.done()
    L.ext(c, sk, sk.profiles.item(0), x0, '(%s) + cap_overlap' % x0, name='Cap %s Hood' % tag)
    L.setmat(c, 'cf')


def build_rail(parent, tag, s, yc, Ln, cw, cy, sxs, guide=False, first=False, exit_ang=None, taper=None):
    """One rail: core, crowned cap, spring points, splice tongue, pins (+ guide strip).
    s: +1 if outboard is +Y. yc: core centre y. Ln: core length. cw: cap width.
    cy: cap centre offset outboard from core centre. sxs: spring point x positions.
    first: first cap of a run, no lowered (joggled) nose zone, so no step for the wing.
    exit_ang: angle expression to the next, straight rail (funnel exit). The core end is
      mitred square to the next rail and the tongue's downstream half and the two pins
      are turned by this angle about the vertical axis at the joint (kinked splice).
    taper: (gx0, cosang, xend) for the guide strip: strip thickness falls linearly with
      global x = gx0 + local x * cosang, from guide_t at x=0 to 0 at x=xend."""
    S = '+' if s > 0 else '-'

    def off(e):
        return '(%s) %s (%s)' % (yc, S, e)

    def turned(u, v):  # plan point u along the next rail from the joint, v across it (outboard +)
        a = exit_ang
        return ('(%s) + (%s) * cos(%s) - (%s) * sin(%s)' % (Ln, u, a, v, a),
                '(%s) %s ((%s) * sin(%s) + (%s) * cos(%s))' % (yc, S, u, a, v, a), '0 mm')

    # core
    c, _ = L.newcomp(parent, 'Rail Core %s' % tag)
    k = L.Sk(c, 'YZ')
    k.rect(('0 mm', off('-core_w / 2'), 'core_bot_z'), ('0 mm', off('core_w / 2'), 'core_top_z'))
    k.rect(('0 mm', off('-(core_w / 2 - core_wall)'), 'core_bot_z + core_wall'),
           ('0 mm', off('core_w / 2 - core_wall'), 'core_top_z - core_wall'))
    sk = k.done()
    Lc = Ln if exit_ang is None else '(%s) + core_w * tan(%s)' % (Ln, exit_ang)
    body = L.ext(c, sk, L.profs(sk, 2), '0 mm', Lc, name='Core %s' % tag).bodies.item(0)
    L.hole_z(c, body, [('pin_x1', yc), ('pin_x2', yc)], 'pin_d + 2 * slide_fit',
             'core_bot_z - 1 mm', 'core_top_z + 1 mm')
    if exit_ang is not None:  # mitre: cut everything past the plane square to the next rail
        a = exit_ang
        k = L.Sk(c, 'XY')
        k.poly([('(%s) - core_w * sin(%s)' % (Ln, a), off('core_w * cos(%s)' % a), '0 mm'),
                ('(%s) + core_w * sin(%s)' % (Ln, a), off('-core_w * cos(%s)' % a), '0 mm'),
                ('(%s) + 3 * core_w' % Ln, off('-core_w * cos(%s)' % a), '0 mm'),
                ('(%s) + 3 * core_w' % Ln, off('core_w * cos(%s)' % a), '0 mm')])
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), 'core_bot_z - 1 mm', 'core_top_z + 1 mm', L.CUT, [body])
    L.setmat(c, 'al')

    # cap
    c, _ = L.newcomp(parent, 'Rail Cap %s' % tag)
    yC = '((%s) %s (%s))' % (yc, S, cy)
    hw = '((%s) / 2)' % cw
    R = '((((%s) / 2)^2 + cap_crown^2) / (2 * cap_crown))' % cw
    d2 = '(cap_wall + cap_gap)'

    def section(lower):
        return cap_section(yc, S, cy, cw, lower)

    k = L.Sk(c, 'YZ')
    k.poly(*section(False))
    sk = k.done()
    body = L.ext(c, sk, sk.profiles.item(0), '0 mm' if first else 'cap_overlap',
                 '(%s) + cap_overlap' % Ln, name='Cap %s' % tag).bodies.item(0)
    if not first:  # lowered nose zone that nests under the previous cap's tail hood
        k = L.Sk(c, 'YZ')
        k.poly(*section(True))
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), '0 mm', 'cap_overlap', L.JOIN, [body])
    body = c.bRepBodies.item(0)
    arc = adsk.core.Curve3DTypes.Arc3DCurveType
    eds = [e for e in body.edges if e.geometry.curveType == arc
           and abs(e.boundingBox.maxPoint.x) < 1e-4 and abs(e.boundingBox.minPoint.x) < 1e-4]
    eds.sort(key=lambda e: -e.boundingBox.maxPoint.z)
    L.fillet(c, eds[:1], 'cap_nose_r')
    body = c.bRepBodies.item(0)
    xe = L.ev('(%s) + cap_overlap' % Ln) / 10.0
    zsb = L.ev('skirt_bot_z') / 10.0
    rm = []
    for fc in body.faces:
        if fc.geometry.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType:
            continue
        p = fc.pointOnFace
        _, n = fc.evaluator.getNormalAtPoint(p)
        if n.z < -0.99 and abs(p.z - zsb) < 1e-3:
            rm.append(fc)
        elif abs(n.x) > 0.99 and (abs(p.x) < 1e-3 or abs(p.x - xe) < 1e-3):
            rm.append(fc)
    L.shell(c, rm, 'cap_wall')
    # tail (top shingle): remove skirts and flange floors over the next cap's nose
    k = L.Sk(c, 'YZ')
    k.rect(('0 mm', '(%s - %s - 5 mm)' % (yC, hw), 'skirt_bot_z - 5 mm'),
           ('0 mm', '(%s + %s + 5 mm)' % (yC, hw), 'flange_bot_z + cap_wall'))
    sk = k.done()
    L.ext(c, sk, sk.profiles.item(0), Ln, '(%s) + cap_overlap + 5 mm' % Ln, L.CUT, [c.bRepBodies.item(0)])
    body = c.bRepBodies.item(0)
    eds = [e for e in body.edges if e.geometry.curveType == arc
           and abs(e.boundingBox.maxPoint.x - xe) < 1e-4 and abs(e.boundingBox.minPoint.x - xe) < 1e-4]
    eds.sort(key=lambda e: -e.boundingBox.maxPoint.z)
    L.fillet(c, eds[:1], 'cap_tail_r')
    # vertical slots in the outboard skirt
    w = '(screw_d + slot_clear)'
    k = L.Sk(c, 'XZ')
    for sx in sxs:
        k.rect(('(%s) - %s / 2' % (sx, w), '0 mm', 'screw_z'),
               ('(%s) + %s / 2' % (sx, w), '0 mm', 'screw_z + spring_travel'))
        k.circle((sx, '0 mm', 'screw_z'), w)
        k.circle((sx, '0 mm', 'screw_z + spring_travel'), w)
    sk = k.done()
    L.ext(c, sk, L.profs(sk), off('core_w / 2 + 0.5 mm'), off('skirt_out + 1 mm'), L.CUT,
          [c.bRepBodies.item(0)])
    if exit_ang is not None:  # cap cut at the joint plane; the hood past it is an Exit Hood (build_hood)
        k = L.Sk(c, 'XY')    # with the base cap's crown (task 0, option a), built by step_run_rails
        v0, v1 = '-(%s) - 100 mm' % cw, '(%s) + 100 mm' % cw
        k.poly([turned('0 mm', v0), turned('cap_overlap + 20 mm', v0),
                turned('cap_overlap + 20 mm', v1), turned('0 mm', v1)])
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), 'skirt_bot_z - 10 mm', 'rail_top_h + 10 mm', L.CUT,
              [c.bRepBodies.item(0)])
    L.setmat(c, 'cf')

    # spring points: coil spring + guide screw in the slot
    for i, sx in enumerate(sxs):
        sp, _ = L.newcomp(parent, 'Spring Point %s%d' % (tag, i + 1))
        c, _ = L.newcomp(sp, 'Coil Spring %s%d' % (tag, i + 1))
        # round wire swept along a helix; the helix points are computed from the
        # parameters at build time (the API cannot create Coil features)
        k = L.Sk(c, 'XZ', yc)
        r = (L.ev('spring_od') - L.ev('spring_wire')) / 2.0
        z0, z1 = L.ev('core_top_z + spring_wire / 2'), L.ev('core_top_z + spring_len - spring_wire / 2')
        x0, y0 = L.ev(sx), L.ev(yc)
        nseg = int(round(L.evu('spring_coils', ''))) * 16
        pts = adsk.core.ObjectCollection.create()
        for j in range(nseg + 1):
            a = 2 * math.pi * j / 16
            pts.add(k.sk.modelToSketchSpace(L.P3((x0 + r * math.cos(a)) / 10, (y0 + r * math.sin(a)) / 10,
                                                 (z0 + (z1 - z0) * j / nseg) / 10)))
        spl = k.sk.sketchCurves.sketchFittedSplines.add(pts)
        k.circle(('(%s) + (spring_od - spring_wire) / 2' % sx, yc, 'core_top_z + spring_wire / 2'), 'spring_wire')
        sk1 = k.done()
        L.sweep_path(c, sk1.profiles.item(0), spl, 'Spring %s%d' % (tag, i + 1))
        L.setmat(c, 'steel')
        c, _ = L.newcomp(sp, 'Guide Screw %s%d' % (tag, i + 1))
        k = L.Sk(c, 'XZ')
        k.circle((sx, '0 mm', 'screw_z'), 'screw_d')
        sk = k.done()
        b = L.ext(c, sk, sk.profiles.item(0), off('core_w / 2 - core_wall'), off('skirt_out + 0.5 mm'),
                  name='Screw %s%d' % (tag, i + 1)).bodies.item(0)
        k = L.Sk(c, 'XZ')
        k.circle((sx, '0 mm', 'screw_z'), 'screw_head_d')
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), off('skirt_out + 0.5 mm'),
              off('skirt_out + 0.5 mm + screw_head_t'), L.JOIN, [b])
        L.setmat(c, 'steel')

    # splice tongue (downstream end) and two ball-lock pins
    c, _ = L.newcomp(parent, 'Splice Tongue %s' % tag)
    ti = '(core_w / 2 - core_wall - slide_fit)'
    k = L.Sk(c, 'YZ')
    k.rect(('0 mm', off('-%s' % ti), 'core_bot_z + core_wall + slide_fit'),
           ('0 mm', off(ti), 'core_top_z - core_wall - slide_fit'))
    k.rect(('0 mm', off('-(%s - core_wall)' % ti), 'core_bot_z + 2 * core_wall + slide_fit'),
           ('0 mm', off('%s - core_wall' % ti), 'core_top_z - 2 * core_wall - slide_fit'))
    sk = k.done()
    pxs = ['(%s) + %s' % (Ln, p) for p in ('pin_x1', 'pin_x2')]
    if exit_ang is None:
        body = L.ext(c, sk, L.profs(sk, 2), '(%s) - tongue_len / 2' % Ln, '(%s) + tongue_len / 2' % Ln,
                     name='Tongue %s' % tag).bodies.item(0)
        L.hole_z(c, body, [(px, yc) for px in pxs], 'pin_d + 2 * slide_fit',
                 'core_bot_z - 1 mm', 'core_top_z + 1 mm')
        pys = [yc, yc]
    else:  # kinked splice: downstream half drawn in plan view along the next rail's axis
        a = exit_ang
        body = L.ext(c, sk, L.profs(sk, 2), '(%s) - tongue_len / 2' % Ln, Ln,
                     name='Tongue %s' % tag).bodies.item(0)
        b2 = None
        for w, z0, z1 in ((ti, 'core_bot_z + core_wall + slide_fit', 'core_top_z - core_wall - slide_fit'),
                          ('(%s - core_wall)' % ti, 'core_bot_z + 2 * core_wall + slide_fit',
                           'core_top_z - 2 * core_wall - slide_fit')):
            k = L.Sk(c, 'XY')
            k.poly([turned('0 mm', '-%s' % w), turned('tongue_len / 2', '-%s' % w),
                    turned('tongue_len / 2', w), turned('0 mm', w)])
            sk2 = k.done()
            if b2 is None:
                b2 = L.ext(c, sk2, sk2.profiles.item(0), z0, z1).bodies.item(0)
            else:
                L.ext(c, sk2, sk2.profiles.item(0), z0, z1, L.CUT, [b2])
        ps = ('pin_x1', 'pin_x2')
        pxs = ['(%s) + %s * cos(%s)' % (Ln, p, a) for p in ps]
        pys = [off('%s * sin(%s)' % (p, a)) for p in ps]
        L.hole_z(c, b2, list(zip(pxs, pys)), 'pin_d + 2 * slide_fit', 'core_bot_z - 1 mm', 'core_top_z + 1 mm')
        col = adsk.core.ObjectCollection.create()
        col.add(c.bRepBodies.item(1))
        ci = c.features.combineFeatures.createInput(c.bRepBodies.item(0), col)
        ci.operation = L.JOIN
        c.features.combineFeatures.add(ci)
    L.setmat(c, 'al')
    for i, px in enumerate(pxs):
        c, _ = L.newcomp(parent, 'Ball-lock Pin %s%d' % (tag, i + 1))
        k = L.Sk(c, 'XY')
        k.circle((px, pys[i], '0 mm'), 'pin_d')
        sk = k.done()
        b = L.ext(c, sk, sk.profiles.item(0), 'core_bot_z', 'core_top_z + 10 mm',
                  name='Pin %s%d' % (tag, i + 1)).bodies.item(0)
        k = L.Sk(c, 'XY')
        k.circle((px, pys[i], '0 mm'), 'pin_head_d')
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), 'core_bot_z - pin_head_t', 'core_bot_z', L.JOIN, [b])
        L.setmat(c, 'steel')

    if guide:  # G1: UHMW strip on the inboard edge of the cap
        c, _ = L.newcomp(parent, 'Guide Strip %s' % tag)
        ein = '((%s) - %s)' % (cy, hw)
        xs = '0 mm' if first else 'cap_overlap'
        if taper is None:
            k = L.Sk(c, 'YZ')
            k.rect(('0 mm', off(ein), 'flange_bot_z'),
                   ('0 mm', off('%s - guide_t' % ein), 'rail_top_h - cap_crown'))
        else:  # plan-view wedge: thickness falls to 0 at global x = xend
            gx0, ca, xend = taper

            def th(xl):
                return '(guide_t * (1 - ((%s) + (%s) * %s) / (%s)))' % (gx0, xl, ca, xend)
            k = L.Sk(c, 'XY')
            P = [(xs, off(ein), '0 mm'), (Ln, off(ein), '0 mm')]
            if L.ev(th(Ln)) > 0.05:
                P.append((Ln, off('%s - %s' % (ein, th(Ln))), '0 mm'))
            P.append((xs, off('%s - %s' % (ein, th(xs))), '0 mm'))
            k.poly(P)
        sk = k.done()
        if taper is None:
            L.ext(c, sk, sk.profiles.item(0), xs, Ln, name='Guide %s' % tag)
        else:
            L.ext(c, sk, sk.profiles.item(0), 'flange_bot_z', 'rail_top_h - cap_crown', name='Guide %s' % tag)
        L.setmat(c, 'uhmw')


def build_frame_half(parent, tag, s, yc, xf, splice):
    """Half of a split U-frame: leg under the rail + cross bar to the split."""
    c, _ = L.newcomp(parent, 'U-frame Half %s' % tag)
    h, hi = 'frame_tube / 2', '(frame_tube / 2 - frame_wall)'
    k = L.Sk(c, 'XY')
    k.rect(('(%s) - %s' % (xf, h), '(%s) - %s' % (yc, h), '0 mm'),
           ('(%s) + %s' % (xf, h), '(%s) + %s' % (yc, h), '0 mm'))
    k.rect(('(%s) - %s' % (xf, hi), '(%s) - %s' % (yc, hi), '0 mm'),
           ('(%s) + %s' % (xf, hi), '(%s) + %s' % (yc, hi), '0 mm'))
    sk = k.done()
    body = L.ext(c, sk, L.profs(sk, 2), 'foot_h', 'core_bot_z', name='Frame %s' % tag).bodies.item(0)

    def sq(half, z0, z1):
        k = L.Sk(c, 'XZ')
        k.rect(('(%s) - %s' % (xf, half), '0 mm', z0), ('(%s) + %s' % (xf, half), '0 mm', z1))
        return k

    k = sq(h, 'foot_h', 'xbar_top_z')
    k.rect(('(%s) - %s' % (xf, hi), '0 mm', 'foot_h + frame_wall'),
           ('(%s) + %s' % (xf, hi), '0 mm', 'xbar_top_z - frame_wall'))
    sk = k.done()
    end = 'split_gap / 2' if s > 0 else '-split_gap / 2'
    L.ext(c, sk, L.profs(sk, 2), yc, end, L.JOIN, [body])
    pin = [(xf, '-xbar_splice / 2')]
    dia = 'frame_pin_d + 2 * slide_fit'
    if s < 0:
        L.hole_z(c, c.bRepBodies.item(0), pin, dia, 'foot_h - 1 mm', 'xbar_top_z + 1 mm')
    if splice:
        t = '(frame_tube / 2 - frame_wall - slide_fit)'
        k = sq(t, 'foot_h + frame_wall + slide_fit', 'xbar_top_z - frame_wall - slide_fit')
        k.rect(('(%s) - (%s - frame_wall)' % (xf, t), '0 mm', 'foot_h + 2 * frame_wall + slide_fit'),
               ('(%s) + (%s - frame_wall)' % (xf, t), '0 mm', 'xbar_top_z - 2 * frame_wall - slide_fit'))
        sk = k.done()
        tb = L.ext(c, sk, L.profs(sk, 2), '-xbar_splice', 'xbar_splice', name='Bar Tongue %s' % tag).bodies.item(0)
        L.hole_z(c, tb, pin, dia, 'foot_h - 1 mm', 'xbar_top_z + 1 mm')
    L.setmat(c, 'al')


def build_frame_pin(parent, tag, xf):
    c, _ = L.newcomp(parent, 'Frame Pin %s' % tag)
    k = L.Sk(c, 'XY')
    k.circle((xf, '-xbar_splice / 2', '0 mm'), 'frame_pin_d')
    sk = k.done()
    b = L.ext(c, sk, sk.profiles.item(0), 'foot_h - 10 mm', 'xbar_top_z', name='Frame Pin %s' % tag).bodies.item(0)
    k = L.Sk(c, 'XY')
    k.circle((xf, '-xbar_splice / 2', '0 mm'), '2 * frame_pin_d')
    sk = k.done()
    L.ext(c, sk, sk.profiles.item(0), 'xbar_top_z', 'xbar_top_z + 6 mm', L.JOIN, [b])
    L.setmat(c, 'steel')


def build_foot(parent, tag, yc, xf):
    """M1: levelling foot (pad, stud, jam nut) on a bolt-down plate."""
    c, _ = L.newcomp(parent, 'Bolt-down Plate %s' % tag)
    hp, hb = 'foot_plate_w / 2', 'foot_bolt_pitch / 2'
    k = L.Sk(c, 'XY')
    k.rect(('(%s) - %s' % (xf, hp), '(%s) - %s' % (yc, hp), '0 mm'),
           ('(%s) + %s' % (xf, hp), '(%s) + %s' % (yc, hp), '0 mm'))
    for a in ('-', '+'):
        for b in ('-', '+'):
            k.circle(('(%s) %s %s' % (xf, a, hb), '(%s) %s %s' % (yc, b, hb), '0 mm'), 'foot_bolt_d')
    sk = k.done()
    L.ext(c, sk, L.profs(sk, 5), '0 mm', 'foot_plate_t', name='Plate %s' % tag)
    L.setmat(c, 'al')
    c, _ = L.newcomp(parent, 'Levelling Foot %s' % tag)
    body = None
    for dia, z0, z1 in (('foot_pad_d', 'foot_plate_t', 'foot_plate_t + foot_pad_t'),
                        ('foot_stud_d', 'foot_plate_t + foot_pad_t', 'foot_h + 40 mm'),
                        ('1.6 * foot_stud_d', 'foot_h - 8 mm', 'foot_h')):
        k = L.Sk(c, 'XY')
        k.circle((xf, yc, '0 mm'), dia)
        sk = k.done()
        if body is None:
            body = L.ext(c, sk, sk.profiles.item(0), z0, z1, name='Foot %s' % tag).bodies.item(0)
        else:
            L.ext(c, sk, sk.profiles.item(0), z0, z1, L.JOIN, [body])
    L.setmat(c, 'steel')


# ---------------------------------------------------------------- designs
def get_project(create=False):
    hub = app.data.activeHub
    for i in range(hub.dataProjects.count):
        p = hub.dataProjects.item(i)
        if p.name == PROJECT:
            return p
    return hub.dataProjects.add(PROJECT) if create else None


def find_file(name):
    fs = get_project().rootFolder.dataFiles
    for i in range(fs.count):
        if fs.item(i).name == name:
            return fs.item(i)
    return None


def activate(name):
    """Make the open document called name active (opens it from the project if needed)."""
    for i in range(app.documents.count):
        doc = app.documents.item(i)
        if doc.name == name:
            doc.activate()
            return doc
    return app.documents.open(find_file(name), True)


def step_save(desc):
    """Save a new version of the active document (designs already live in the project).
    Out-of-date links (a newer base section version) are updated first."""
    doc = app.activeDocument
    doc.updateAllReferences()
    print('saved', doc.save(desc), doc.name)


def setup_design():
    d = L.des()
    d.designType = adsk.fusion.DesignTypes.ParametricDesignType
    d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
    root = d.rootComponent
    while root.occurrences.count:
        root.occurrences.item(0).deleteMe()
    return d, root


def step_base():
    p = get_project(create=True)
    d, root = setup_design()
    L.set_params(PARAMS)
    sxs = ('frame_inset', 'section_len - frame_inset')
    for s, side in ((1, 'R'), (-1, 'L')):
        half, _ = L.newcomp(root, 'Half %s' % side)
        yc = '(rail_cc / 2)' if s > 0 else '-(rail_cc / 2)'
        build_rail(half, side, s, yc, 'section_len', 'cap_width', '0 mm', sxs)
        for i, xf in enumerate(sxs):
            build_frame_half(half, '%s%d' % (side, i + 1), s, yc, xf, s > 0)
            build_foot(half, '%s%d' % (side, i + 1), yc, xf)
    for i, xf in enumerate(sxs):
        build_frame_pin(root, str(i + 1), xf)
    cf = L.mat('cf')
    print('project:', p.name, '| materials:', [L.mat(k).name for k in ('al', 'cf', 'steel')],
          '| cfrp density', cf.materialProperties.itemByName('Density').value)
    report_mass(root)


def report_mass(root):
    tot = 0.0
    out = []
    for o in root.occurrences:
        m = o.physicalProperties.mass
        tot += m
        out.append('%s=%.2f' % (o.name, m))
    print('mass kg:', ', '.join(out), '| section=%.2f' % tot)
    h = root.occurrences.item(0)
    print('Half R parts:', ', '.join('%s=%.2f' % (o.component.name, o.physicalProperties.mass)
                                     for o in h.childOccurrences))


def step_save_base():
    doc = app.activeDocument
    ok = doc.saveAs(BASE_NAME, get_project().rootFolder,
                    'Phase 1: full-detail base rail section (S1 springs, M1 feet)', '')
    print('saved', ok, doc.name)


def step_run_new():
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    setup_design()
    L.set_params(PARAMS + RUN_PARAMS)
    ok = doc.saveAs(RUN_NAME, get_project().rootFolder,
                    'Phase 1: G1 entry funnel + 3 linked base sections + drone stand-in', '')
    print('run doc saved', ok, '| funnel_ang deg', round(math.degrees(L.evu('funnel_ang', 'rad')), 3))


def edge_y(xf):
    """|y| of the funnel core centre at global x (expression)."""
    return ('((funnel_gap0 + 2 * guide_t + (rail_gap - funnel_gap0 - 2 * guide_t) * (%s)'
            ' / (funnel_sections * section_len)) / 2 + cap_width / 2)' % xf)


def step_run_rails(sides='RL', clear=True, ks=None):
    """Funnel rails, one component per funnel section and side ('Funnel Rail R1'..'L3'),
    because the first rail has a step-free cap, the last one the kinked exit splice, and
    each guide strip tapers with global x. clear=True empties the design, updates the
    parameters and inserts the linked base sections first. ks limits the sections built
    (0-based). The MCP call times out (and Fusion rolls back) on long scripts, so run
    step_run_rails('', True), then one rail per call: step_run_rails('R', False, [0]) ..."""
    d = L.des()
    root = d.rootComponent
    n = int(round(L.evu('funnel_sections', '')))
    if clear:
        while root.occurrences.count:
            root.occurrences.item(0).deleteMe()
        L.set_params(PARAMS + RUN_PARAMS)
        n = int(round(L.evu('funnel_sections', '')))
        base = find_file(BASE_NAME)
        for k in range(3):
            m = adsk.core.Matrix3D.create()
            m.translation = L.V3(L.ev('(funnel_sections + %d) * section_len' % k) / 10.0, 0, 0)
            root.occurrences.addByInsert(base, m, True)
        fun, _ = L.newcomp(root, 'G1 Entry Funnel')
    th = L.evu('funnel_ang', 'rad')
    Lf = '(section_len / cos(funnel_ang))'
    sxs = ('frame_inset', '%s - frame_inset' % Lf)
    for s, side in ((1, 'R'), (-1, 'L')):
        if side not in sides:
            continue
        for k in range(n):
            if ks is not None and k not in ks:
                continue
            for o in [o for o in root.occurrences if o.component.name == 'Funnel Rail %s%d' % (side, k + 1)]:
                o.deleteMe()  # rerun after a failed call: failed scripts do not always roll back
            rc, rocc = L.newcomp(root, 'Funnel Rail %s%d' % (side, k + 1))
            build_rail(rc, 'F%s%d' % (side, k + 1), s, '0 mm', Lf, 'funnel_cap_w',
                       '(funnel_cap_w - cap_width) / 2', sxs, True, first=(k == 0),
                       exit_ang='funnel_ang' if k == n - 1 else None,
                       taper=('%d * section_len' % k, 'cos(funnel_ang)', 'funnel_sections * section_len'))
            if k == n - 1:  # the last funnel cap's tail hood, on the straight base rail axis
                for o in [o for o in root.occurrences if o.component.name == 'Exit Hood F%s%d' % (side, k + 1)]:
                    o.deleteMe()
                build_hood(root, 'F%s%d' % (side, k + 1), '(rail_cc / 2)' if s > 0 else '-(rail_cc / 2)',
                           'funnel_sections * section_len')
            m = adsk.core.Matrix3D.create()
            m.setToRotation(-s * th, L.V3(0, 0, 1), L.P3(0, 0, 0))
            x0 = '%d * section_len' % k
            m.translation = L.V3(L.ev(x0) / 10.0, s * L.ev(edge_y(x0)) / 10.0, 0)
            rocc.transform2 = m
            if d.snapshots.hasPendingSnapshot:
                d.snapshots.add()
    print('rails ok; root occurrences:', root.occurrences.count)


def step_fix_funnel():
    """Set each funnel rail occurrence transform from the parameters and capture it."""
    d = L.des()
    root = d.rootComponent
    th = L.evu('funnel_ang', 'rad')
    out = []
    for o in list(root.occurrences):
        if not o.name.startswith('Funnel Rail'):
            continue
        # 'Funnel Rail R2:1' (one component per section) or 'Funnel Rail R:2' (shared, Phase 1)
        t = o.name.split(':')[0][len('Funnel Rail '):]
        s = 1 if t[0] == 'R' else -1
        k = int(t[1:]) - 1 if len(t) > 1 else int(o.name.split(':')[1]) - 1
        m = adsk.core.Matrix3D.create()
        m.setToRotation(-s * th, L.V3(0, 0, 1), L.P3(0, 0, 0))
        x0 = '%d * section_len' % k
        m.translation = L.V3(L.ev(x0) / 10.0, s * L.ev(edge_y(x0)) / 10.0, 0)
        o.transform2 = m
        if d.snapshots.hasPendingSnapshot:
            d.snapshots.add()
    for o in root.occurrences:
        if o.name.startswith('Funnel Rail'):
            t = o.transform2
            out.append('%s %.0f,%.0f,%.2f' % (o.name, t.translation.x * 10, t.translation.y * 10,
                                              math.degrees(math.atan2(t.getCell(1, 0), t.getCell(0, 0)))))
    print(out)


def step_run_frames(ks=None, drone=True):
    """Funnel U-frames and feet (ks: 0-based sections, None = all), then the drone stand-in.
    Split it (e.g. ks=[0, 1], drone=False then ks=[2]) to stay under the MCP time-out."""
    root = L.des().rootComponent
    fun = root.occurrences.itemByName('G1 Entry Funnel:1').component
    n = int(round(L.evu('funnel_sections', '')))
    for k in range(n):
        if ks is not None and k not in ks:
            continue
        for o in [o for o in fun.occurrences if o.component.name == 'Funnel Section %d Frames' % (k + 1)]:
            o.deleteMe()
        sec, _ = L.newcomp(fun, 'Funnel Section %d Frames' % (k + 1))
        for i, xl in enumerate(('frame_inset', 'section_len - frame_inset')):
            xf = '(%d * section_len + %s)' % (k, xl)
            for s, side in ((1, 'R'), (-1, 'L')):
                yc = edge_y(xf) if s > 0 else '-' + edge_y(xf)
                tag = 'F%d%s%d' % (k + 1, side, i + 1)
                build_frame_half(sec, tag, s, yc, xf, s > 0)
                build_foot(sec, tag, yc, xf)
            build_frame_pin(sec, 'F%d-%d' % (k + 1, i + 1), xf)
    if drone:
        for o in [o for o in root.occurrences if o.component.name == 'Drone Stand-in']:
            o.deleteMe()
        build_drone(root)
    print('frames + drone ok')


def build_drone(root, hook=False):
    """Drone stand-in at drone_x. hook=True adds the D3 arresting hook (D3_PARAMS)."""
    dr, _ = L.newcomp(root, 'Drone Stand-in')
    zw = '(rail_top_h - drone_sink)'
    xt = '(drone_x - tail_arm)'
    xb0 = '(%s - tail_chord / 2)' % xt
    xn = '(%s + body_len)' % xb0

    def box(name, x0, x1, hy, z0, z1):
        c, _ = L.newcomp(dr, name)
        k = L.Sk(c, 'XY')
        k.rect((x0, '-(%s)' % hy, '0 mm'), (x1, hy, '0 mm'))
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), z0, z1, name=name)
        return c

    box('DR Body', xb0, xn, 'body_width / 2', '%s - body_drop' % zw, '%s + tail_clear' % zw)
    box('DR Wing', 'drone_x - wing_chord / 2', 'drone_x + wing_chord / 2', 'wingspan / 2', zw, '%s + wing_thk' % zw)
    box('DR Tail', '%s - tail_chord / 2' % xt, '%s + tail_chord / 2' % xt, 'tail_span / 2',
        '%s + tail_clear' % zw, '%s + tail_clear + tail_thk' % zw)
    c, _ = L.newcomp(dr, 'DR Prop')
    hub = '(%s - body_drop / 2)' % zw
    k = L.Sk(c, 'YZ')
    k.circle(('0 mm', '0 mm', hub), 'prop_dia')
    sk = k.done()
    f = L.ext(c, sk, sk.profiles.item(0), xn, '%s + prop_disc_t' % xn, name='DR Prop Disc')
    f.bodies.item(0).opacity = 0.25
    k = L.Sk(c, 'YZ')
    k.rect(('0 mm', '-prop_blade_w / 2', '%s - prop_dia / 2' % hub), ('0 mm', 'prop_blade_w / 2', '%s + prop_dia / 2' % hub))
    sk = k.done()
    L.ext(c, sk, sk.profiles.item(0), xn, '%s + prop_blade_t' % xn, name='DR Prop Blades')
    if hook:  # shank down from the body, toe pointing forward under the cable: the throat opens forward
        hx = '(drone_x - hook_back)'
        c = box('DR Hook', '%s - hook_w' % hx, hx, 'hook_w / 2', 'hook_z', '%s - body_drop' % zw)
        k = L.Sk(c, 'XY')
        k.rect((hx, '-hook_w / 2', '0 mm'), ('%s + hook_toe' % hx, 'hook_w / 2', '0 mm'))
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), 'hook_z', 'hook_z + hook_w / 2', L.JOIN, [c.bRepBodies.item(0)])
        L.setmat(c, 'steel')


def step_checks():
    root = L.des().rootComponent
    bodies = []

    def walk(occs):
        for o in occs:
            for b in o.bRepBodies:
                bodies.append(b)
            walk(o.childOccurrences)
    walk(root.occurrences)

    x0 = L.ev('drone_x - tail_arm - tail_chord') / 10.0
    x1 = L.ev('drone_x - tail_arm - tail_chord / 2 + body_len + 50 mm') / 10.0

    def grab(*pre):
        return [b for b in bodies if b.name.startswith(pre)
                and b.boundingBox.maxPoint.x > x0 and b.boundingBox.minPoint.x < x1]
    mm = app.measureManager

    def mind(A, B):
        return min(mm.measureMinimumDistance(a, b).value * 10.0 for a in A for b in B)
    frames = grab('Frame ', 'Bar Tongue')
    rails = grab('Core ', 'Cap ', 'Guide ', 'Tongue ', 'Pin ', 'Screw ')
    caps = grab('Cap ')
    t = L.ev('spring_travel')
    r = {}
    r['body_to_frames'] = mind(grab('DR Body'), frames)
    r['blades_to_frames'] = mind(grab('DR Prop Blades'), frames)
    r['blades_to_rails'] = mind(grab('DR Prop Blades'), rails)
    r['disc_to_rails'] = mind(grab('DR Prop Disc'), rails)
    r['body_to_rails'] = mind(grab('DR Body'), rails)
    r['tail_to_caps'] = mind(grab('DR Tail'), caps)
    out = ['%s=%.1f' % (k, v) for k, v in r.items()]
    ta, tc = L.ev('tail_arm'), L.ev('tail_clear')
    out.append('loaded: body_to_frames=%.1f blades_to_frames=%.1f tail_to_unloaded_cap=%.1f' %
               (r['body_to_frames'] - t, r['blades_to_frames'] - t, tc - t))
    out.append('tail pitch limit deg: touchdown=%.2f compressed=%.2f; 5deg drop=%.0f' %
               (math.degrees(math.atan(tc / ta)), math.degrees(math.atan((tc - t) / ta)),
                ta * math.sin(math.radians(5))))
    out.append('prop r=%.0f cap inner edge=%.0f core inner face=%.0f' %
               (L.ev('prop_dia') / 2, L.ev('rail_gap') / 2, L.ev('rail_cc / 2 - core_w / 2')))
    print(' | '.join(out))


# ---------------------------------------------------------------- version folders
def vpath(folder, name):
    """Path of a file in a version folder, relative to drone-rail/ (e.g. '01-entry/G1-funnel')."""
    p = os.path.join(ROOT, folder, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


def find_occ(path):
    """Occurrence in the active design by component names from the root, e.g. ('Half R', 'Rail Cap R')."""
    occs, o = L.des().rootComponent.occurrences, None
    for n in path:
        o = [x for x in occs if x.component.name == n][0]
        occs = o.childOccurrences
    return o


def shoot(folder, name, eye, target, extent=None, hide=()):
    """1200x900 orthographic PNG into the version folder. eye/target in mm; extent = view
    width in mm (None = fit all). hide: component-name paths switched off for this shot only."""
    hidden = [find_occ(h) for h in hide]
    for o in hidden:
        o.isLightBulbOn = False
    path = vpath(folder, name)
    ok = L.shot(path, eye, target, extent, 1200, 900)
    for o in hidden:
        o.isLightBulbOn = True
    size = os.path.getsize(path) if os.path.exists(path) else 0
    print('png', name, ok, size)
    if not ok or size == 0:
        raise RuntimeError('screenshot failed: ' + path)


def export_f3d(folder, name, comp_path=None):
    """Native Fusion archive export of the active design (or of one component, comp_path) into
    the version folder. The API only writes .f3d: a design with linked components is written as
    one self-contained .f3d with the linked parts embedded (no .f3z). Fails on a missing or empty file."""
    path = vpath(folder, name)
    if os.path.exists(path):
        os.remove(path)
    em = L.des().exportManager
    if comp_path:
        opts = em.createFusionArchiveExportOptions(path, find_occ(comp_path).component)
    else:
        opts = em.createFusionArchiveExportOptions(path)
    ok = em.execute(opts)
    size = os.path.getsize(path) if os.path.exists(path) else 0
    print('f3d', name, ok, size)
    if not ok or size == 0:
        raise RuntimeError('export failed: ' + path)


# ---------------------------------------------------------------- Phase 2: stopping versions
SIMPLE_NAME = 'DRR Base Section Simple'
NET_NAME = 'DRR Catch Net'
G = 9.81

NET_PARAMS = [
    ('net_span', 'wingspan + 800 mm', 'mm', 'D1 assumed: clear span between the posts (wingtips + 400 each side)'),
    ('net_bot_z', '150 mm', 'mm', 'D1 assumed: net bottom edge'),
    ('net_top_z', '1800 mm', 'mm', 'D1 assumed: net top edge (tail top is about 1060)'),
    ('net_mesh', '250 mm', 'mm', 'D1 assumed: largest mesh opening'),
    ('net_cord', '12 mm', 'mm', 'D1 assumed: net cord (square stand-in)'),
    ('post_w', '120 mm', 'mm', 'D1 assumed: square steel post'),
    ('post_h', 'net_top_z + 200 mm', 'mm', 'derived'),
    ('post_plate_w', '400 mm', 'mm', 'D1 assumed: post base plate'),
    ('brace_run', '1500 mm', 'mm', 'D1 assumed: back-brace foot behind the net plane'),
    ('brace_w', '80 mm', 'mm', 'D1 assumed: back-brace bar'),
]
STOP_PARAMS = [
    ('run_sections', '36', '', 'stopping run length in sections'),
    ('net_gap', '1500 mm', 'mm', 'D1 assumed: last section end to the net plane'),
    ('drone_x', '1.5 * section_len', 'mm', 'stand-in wing mid-chord: touchdown on the detailed sections'),
]
VPARAMS = {
    'A': [('run_sections', '36', '', 'A: friction only, 72 m')],
    'B': [('run_sections', '24', '', 'B: 48 m'), ('brake_start', '12', '', 'B: standard sections before the braking zone'),
          ('brake_grip', '0.6', '', 'spec B: high-grip cap surface')],
    'C': [('run_sections', '32', '', 'C: 18 flat + 14 ramp'), ('ramp_start', '18', '', 'C: flat sections before the ramp'),
          ('ramp_ang', '5 deg', 'deg', 'spec C: ramp angle'), ('trestle_w', '100 mm', 'mm', 'C assumed: ramp trestle tube'),
          ('trestle_beam_h', '100 mm', 'mm', 'C assumed: trestle top beam depth')],
    'D1': [('run_sections', '3', '', 'D1: short run'),
           ('drone_x', 'run_sections * section_len + net_gap - 2300 mm', 'mm', 'D1: prop 1.5 m short of the net')],
    'D2': [('run_sections', '24', '', 'D2: 48 m'), ('grip0', '0.2', '', 'spec D2: grip at the entry'),
           ('grip1', '0.7', '', 'spec D2: grip at the end'), ('grip_bands', '6', '', 'D2: appearance bands')],
    'D3': [('run_sections', '6', '', 'D3: 12 m'),
           ('cable_x1', '1000 mm', 'mm', 'D3 assumed: first cross cable, between U-frames'),
           ('cable_x2', '3000 mm', 'mm', 'D3 assumed: second cross cable'),
           ('cable_z', '150 mm', 'mm', 'D3 assumed: cable height, above the cross bars and below the prop tip'),
           ('cable_d', '16 mm', 'mm', 'D3 assumed: cable stand-in'),
           ('drum_y', 'rail_cc / 2 + 900 mm', 'mm', 'D3 assumed: energy-absorber drum centre from the run centreline'),
           ('drum_d', '450 mm', 'mm', 'D3 assumed'), ('drum_h', '350 mm', 'mm', 'D3 assumed'),
           ('hook_back', '1200 mm', 'mm', 'D3 assumed: hook behind the wing mid-chord'),
           ('hook_z', '110 mm', 'mm', 'D3 assumed: hook toe underside, unloaded'),
           ('hook_toe', '120 mm', 'mm', 'D3 assumed: forward toe length'), ('hook_w', '40 mm', 'mm', 'D3 assumed: hook bar'),
           ('arrest_g', '2', '', 'spec D3: arresting deceleration, g'),
           ('drone_x', 'cable_x1 - 300 mm - hook_toe + hook_back', 'mm', 'D3: hook throat 300 mm short of cable 1')],
}


def vparams(vid):
    return PARAMS + RUN_PARAMS + STOP_PARAMS + VPARAMS[vid]


def open_or_new(name, params, desc):
    """'open' stage: activate the design, or create it with params and save it in the project."""
    if any(app.documents.item(i).name == name for i in range(app.documents.count)) or find_file(name):
        return activate(name)
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    setup_design()
    L.set_params(params)
    print('new design saved', doc.saveAs(name, get_project().rootFolder, desc, ''), name)


def blk(c, x0, x1, y0, y1, z0, z1, name=None):
    """Box: XY rectangle x0..x1, y0..y1 extruded z0..z1 (new body)."""
    k = L.Sk(c, 'XY')
    k.rect((x0, y0, '0 mm'), (x1, y1, '0 mm'))
    sk = k.done()
    return L.ext(c, sk, sk.profiles.item(0), z0, z1, name=name).bodies.item(0)


def cyl(c, kind, ctr, dia, a, b, name=None):
    k = L.Sk(c, kind)
    k.circle(ctr, dia)
    sk = k.done()
    return L.ext(c, sk, sk.profiles.item(0), a, b, name=name).bodies.item(0)


def pattern(c, body, axis, n, spacing):
    col = adsk.core.ObjectCollection.create()
    col.add(body)
    pf = c.features.rectangularPatternFeatures
    inp = pf.createInput(col, axis, L.VI(str(n)), L.VI(spacing),
                         adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    return pf.add(inp)


def step_simple():
    """DRR Base Section Simple: light stand-in for long runs. Plain bodies only: hollow cores
    (with the pin holes the previous section's pins go through), solid caps with the lowered
    nose zone, U-frame halves and foot pads. No springs, screws, pins, tongues or plates."""
    d, root = setup_design()
    L.set_params(PARAMS)
    sxs = ('frame_inset', 'section_len - frame_inset')
    for s, side in ((1, 'R'), (-1, 'L')):
        S = '+' if s > 0 else '-'
        yc = '(rail_cc / 2)' if s > 0 else '-(rail_cc / 2)'

        def off(e):
            return '(%s) %s (%s)' % (yc, S, e)
        half, _ = L.newcomp(root, 'Simple Half %s' % side)
        c, _ = L.newcomp(half, 'Simple Core %s' % side)
        k = L.Sk(c, 'YZ')
        k.rect(('0 mm', off('-core_w / 2'), 'core_bot_z'), ('0 mm', off('core_w / 2'), 'core_top_z'))
        k.rect(('0 mm', off('-(core_w / 2 - core_wall)'), 'core_bot_z + core_wall'),
               ('0 mm', off('core_w / 2 - core_wall'), 'core_top_z - core_wall'))
        sk = k.done()
        body = L.ext(c, sk, L.profs(sk, 2), '0 mm', 'section_len', name='Core %s' % side).bodies.item(0)
        L.hole_z(c, body, [('pin_x1', yc), ('pin_x2', yc)], 'pin_d + 2 * slide_fit',
                 'core_bot_z - 1 mm', 'core_top_z + 1 mm')
        L.setmat(c, 'al')
        c, _ = L.newcomp(half, 'Simple Cap %s' % side)
        k = L.Sk(c, 'YZ')
        k.poly(*cap_section(yc, S, '0 mm', 'cap_width', False))
        sk = k.done()
        body = L.ext(c, sk, sk.profiles.item(0), 'cap_overlap', 'section_len', name='Cap %s' % side).bodies.item(0)
        k = L.Sk(c, 'YZ')
        k.poly(*cap_section(yc, S, '0 mm', 'cap_width', True))
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), '0 mm', 'cap_overlap', L.JOIN, [body])
        k = L.Sk(c, 'YZ')  # clear the core and the space above it (pin heads of the previous section)
        k.rect(('0 mm', off('-(core_w / 2 + cap_gap)'), 'skirt_bot_z - 1 mm'),
               ('0 mm', off('core_w / 2 + cap_gap'), 'flange_bot_z'))
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), '-1 mm', 'section_len + 1 mm', L.CUT, [c.bRepBodies.item(0)])
        L.setmat(c, 'cf')
        c, _ = L.newcomp(half, 'Simple Frames %s' % side)
        for i, xf in enumerate(sxs):
            t = '%s%d' % (side, i + 1)
            b = blk(c, '(%s) - frame_tube / 2' % xf, '(%s) + frame_tube / 2' % xf,
                    '(%s) - frame_tube / 2' % yc, '(%s) + frame_tube / 2' % yc, 'foot_h', 'core_bot_z', 'Frame ' + t)
            k = L.Sk(c, 'XZ')
            k.rect(('(%s) - frame_tube / 2' % xf, '0 mm', 'foot_h'), ('(%s) + frame_tube / 2' % xf, '0 mm', 'xbar_top_z'))
            sk = k.done()
            L.ext(c, sk, sk.profiles.item(0), yc, 'split_gap / 2' if s > 0 else '-split_gap / 2', L.JOIN, [b])
            cyl(c, 'XY', (xf, yc, '0 mm'), 'foot_pad_d', '0 mm', 'foot_h', 'Foot ' + t)
        for b in c.bRepBodies:
            b.material = L.mat('steel' if b.name.startswith('Foot') else 'al')
    print('simple section: %d bodies' % sum(o.component.bRepBodies.count for o in root.allOccurrences))


def step_net():
    """DRR Catch Net (D1): reusable end-of-run net on two braced posts. Net plane at x=0,
    braces behind it (+x). Linked at the end of every stopping run by step_layout."""
    d, root = setup_design()
    L.set_params(PARAMS + NET_PARAMS)
    c, _ = L.newcomp(root, 'Net Posts')
    for s, sd in ((1, 'R'), (-1, 'L')):
        yp = '(net_span / 2 + post_w / 2)' if s > 0 else '-(net_span / 2 + post_w / 2)'
        blk(c, '-post_plate_w / 2', 'post_plate_w / 2', '%s - post_plate_w / 2' % yp, '%s + post_plate_w / 2' % yp,
            '0 mm', 'foot_plate_t', 'Post Plate ' + sd)
        blk(c, '-post_w / 2', 'post_w / 2', '%s - post_w / 2' % yp, '%s + post_w / 2' % yp,
            'foot_plate_t', 'post_h', 'Post ' + sd)
        k = L.Sk(c, 'XZ')
        k.poly([('post_w / 2', '0 mm', 'net_top_z - 100 mm'), ('post_w / 2', '0 mm', 'net_top_z - 100 mm - 1.5 * brace_w'),
                ('brace_run - 1.5 * brace_w', '0 mm', 'foot_plate_t'), ('brace_run', '0 mm', 'foot_plate_t')])
        sk = k.done()
        L.ext(c, sk, sk.profiles.item(0), '%s - brace_w / 2' % yp, '%s + brace_w / 2' % yp, name='Brace ' + sd)
        blk(c, 'brace_run - 250 mm', 'brace_run + 50 mm', '%s - 150 mm' % yp, '%s + 150 mm' % yp,
            '0 mm', 'foot_plate_t', 'Brace Plate ' + sd)
    L.setmat(c, 'steel')
    c, _ = L.newcomp(root, 'Net Mesh')
    nv = int(math.ceil(L.ev('net_span') / L.ev('net_mesh'))) + 1
    nh = int(math.ceil(L.ev('net_top_z - net_bot_z') / L.ev('net_mesh'))) + 1
    b = blk(c, '-net_cord / 2', 'net_cord / 2', '-net_span / 2', '-net_span / 2 + net_cord',
            'net_bot_z', 'net_top_z', 'Net Cord V')
    pattern(c, b, c.yConstructionAxis, nv, '(net_span - net_cord) / %d' % (nv - 1))
    k = L.Sk(c, 'XZ')
    k.rect(('-net_cord / 2', '0 mm', 'net_bot_z'), ('net_cord / 2', '0 mm', 'net_bot_z + net_cord'))
    sk = k.done()
    b = L.ext(c, sk, sk.profiles.item(0), '-net_span / 2', 'net_span / 2', name='Net Cord H').bodies.item(0)
    pattern(c, b, c.zConstructionAxis, nh, '(net_top_z - net_bot_z - net_cord) / %d' % (nh - 1))
    L.setmat(c, 'nylon')
    print('net: %d x %d cords, material %s' % (nv, nh, L.mat('nylon').name if L.mat('nylon') else None))


def sec_matrix(k, k0=None):
    """Placement of run section k: flat along x, or for k >= k0 (C ramp) turned nose-up by
    ramp_ang about the cap-top line at the kink (x = k0 * section_len + cap_overlap)."""
    m = adsk.core.Matrix3D.create()
    Ls = L.ev('section_len')
    if k0 is None or k < k0:
        m.translation = L.V3(k * Ls / 10.0, 0, 0)
        return m
    a, j = L.evu('ramp_ang', 'rad'), k - k0
    m.setToRotation(-a, L.V3(0, 1, 0), L.P3(0, 0, 0))
    pl = L.P3(L.ev('cap_overlap') / 10.0, 0, L.ev('rail_top_h') / 10.0)
    pl.transformBy(m)
    gx = (k0 * Ls + L.ev('cap_overlap') + j * Ls * math.cos(a)) / 10.0
    gz = (L.ev('rail_top_h') + j * Ls * math.sin(a)) / 10.0
    m.translation = L.V3(gx - pl.x, 0, gz - pl.z)
    return m


def place(root, name, m, cache):
    """Link design name at m. Every section is its own addByInsert: addExistingComponent adds
    the first occurrence's offset to m, and setting transform2 on linked occurrences afterwards
    left the design with broken references (seen 2026-11-05)."""
    if name not in cache:
        cache[name] = find_file(name)
    return root.occurrences.addByInsert(cache[name], m, True)


def net_matrix(n, k0=None):
    """Catch net placement: net plane net_gap past the end of section n-1 (raised to the ramp top for C)."""
    e = L.P3(L.ev('cap_overlap') / 10.0, 0, L.ev('rail_top_h') / 10.0)
    e.transformBy(sec_matrix(n, k0))
    m = adsk.core.Matrix3D.create()
    m.translation = L.V3(e.x + L.ev('net_gap - cap_overlap') / 10.0, 0, e.z - L.ev('rail_top_h') / 10.0)
    return m


def step_layout(detailed=(0, 1), ramp_from=None, net=True):
    """Empty the run design and link run_sections sections along x: indices in detailed link
    BASE_NAME, the rest SIMPLE_NAME. Then the D1 catch net (NET_NAME) at the run end."""
    root = L.des().rootComponent
    while root.occurrences.count:
        root.occurrences.item(0).deleteMe()
    n = int(round(L.evu('run_sections', '')))
    cache = {}
    for k in range(n):
        place(root, BASE_NAME if k in detailed else SIMPLE_NAME, sec_matrix(k, ramp_from), cache)
    if net:
        place(root, NET_NAME, net_matrix(n, ramp_from), cache)
    xs = [round(o.transform2.translation.x * 10) for o in sections()]
    bad = [k for k, x in enumerate(xs) if ramp_from is None and abs(x - k * L.ev('section_len')) > 0.5]
    if bad:
        raise RuntimeError('sections misplaced: %s' % bad)
    print('layout: %d sections (%d detailed), net=%s, length %.1f m' % (n, len(detailed), net, n * L.ev('section_len') / 1000))


def step_drone(hook=False):
    root = L.des().rootComponent
    for o in [o for o in root.occurrences if o.component.name == 'Drone Stand-in']:
        o.deleteMe()
    build_drone(root, hook)
    print('drone at x=%.0f' % L.ev('drone_x'))


def sections():
    """Linked run sections (base or simple), sorted along the run."""
    root = L.des().rootComponent
    occ = [o for o in root.occurrences if o.component.name.startswith((BASE_NAME, SIMPLE_NAME))]
    return sorted(occ, key=lambda o: o.transform2.translation.x)


def paint(o, a, key='Cap'):
    """Appearance override on every child occurrence of o whose component name holds key."""
    n = 0
    for c in o.childOccurrences:
        if key in c.component.name:
            c.appearance = a
            n += 1
        else:
            n += paint(c, a, key)
    return n


def step_bands(bands):
    """bands: [(k0, k1, appearance name, rgb)]: cap appearance on run sections k0..k1-1."""
    secs = sections()
    out = []
    for k0, k1, name, rgb in bands:
        a = L.look(name, rgb)
        out.append('%s: %d caps' % (name, sum(paint(o, a) for o in secs[k0:k1])))
    print('; '.join(out))


def stop_x(segs):
    """segs [(length m, grip, slope deg)]: stop distance from v^2 = 2 a d, a = g (grip cos + sin)."""
    v2 = (L.evu('landing_speed_kn', '') * 1852.0 / 3600.0) ** 2
    x = 0.0
    for ln, mu, ang in segs:
        a = G * (mu * math.cos(math.radians(ang)) + math.sin(math.radians(ang)))
        if v2 <= 2 * a * ln:
            return x + v2 / (2 * a), 0.0
        v2 -= 2 * a * ln
        x += ln
    return x, math.sqrt(v2)


def report_stop(label, segs):
    x, v = stop_x(segs)
    print('%s: %s' % (label, 'stops at %.1f m' % x if v == 0 else 'run ends at %.1f m with %.1f m/s left' % (x, v)))


def step_clash(x0, x1, extra=()):
    """Interference check of cores, caps, tongues, pins and strips (+ extra name prefixes)
    whose boxes reach into global x0..x1 (mm)."""
    d = L.des()
    pre = ('Core ', 'Cap ', 'Tongue ', 'Pin ', 'Guide ') + tuple(extra)
    col = adsk.core.ObjectCollection.create()

    def walk(occs):
        for o in occs:
            for b in o.bRepBodies:
                bb = b.boundingBox
                if b.name.startswith(pre) and bb.maxPoint.x * 10 > x0 and bb.minPoint.x * 10 < x1:
                    col.add(b)
            walk(o.childOccurrences)
    walk(d.rootComponent.occurrences)
    res = d.analyzeInterference(d.createInterferenceInput(col))
    hits = ['%s/%s %.2fcm3' % (r.entityOne.name, r.entityTwo.name, r.interferenceBody.volume) for r in res]
    print('clash x %d-%d: %d bodies, %d hits %s' % (x0, x1, col.count, len(hits), hits[:6]))


def step_d3_gear():
    """D3: two cross cables at cable_z between energy-absorber drums at the sides."""
    root = L.des().rootComponent
    for o in [o for o in root.occurrences if o.component.name == 'Arresting Gear']:
        o.deleteMe()
    c, _ = L.newcomp(root, 'Arresting Gear')
    for i, cx in enumerate(('cable_x1', 'cable_x2')):
        cyl(c, 'XZ', (cx, '0 mm', 'cable_z'), 'cable_d', '-(drum_y - drum_d / 2)', 'drum_y - drum_d / 2',
            'Cable %d' % (i + 1))
        for s, sd in ((1, 'R'), (-1, 'L')):
            yd = '(drum_y)' if s > 0 else '-(drum_y)'
            blk(c, '(%s) - drum_d / 2 - 50 mm' % cx, '(%s) + drum_d / 2 + 50 mm' % cx,
                '%s - drum_d / 2 - 50 mm' % yd, '%s + drum_d / 2 + 50 mm' % yd, '0 mm', 'foot_plate_t',
                'Drum Base %d%s' % (i + 1, sd))
            cyl(c, 'XY', (cx, yd, '0 mm'), 'drum_d', 'foot_plate_t', 'drum_h', 'Drum %d%s' % (i + 1, sd))
    L.setmat(c, 'steel')
    print('arresting gear: %d bodies' % c.bRepBodies.count)


def step_c_trestles(ks):
    """C: a braced trestle under each U-frame of ramp sections ks (beam under the feet, two
    posts, X-brace across). Feet less than 30 mm up use their levelling studs instead."""
    root = L.des().rootComponent
    k0 = int(round(L.evu('ramp_start', '')))
    for k in ks:
        for o in [o for o in root.occurrences if o.component.name == 'Ramp Trestles %d' % (k + 1)]:
            o.deleteMe()
        c, _ = L.newcomp(root, 'Ramp Trestles %d' % (k + 1))
        for i, xl in enumerate(('frame_inset', 'section_len - frame_inset')):
            p = L.P3(L.ev(xl) / 10.0, 0, 0)
            p.transformBy(sec_matrix(k, k0))
            x, z = p.x * 10, p.z * 10
            if z < 30:
                continue
            X, Z, t = '%.1f mm' % x, '%.1f mm' % z, '%d%d' % (k + 1, i + 1)
            blk(c, '%s - foot_pad_d' % X, '%s + foot_pad_d' % X, '-(rail_cc / 2 + 150 mm)', 'rail_cc / 2 + 150 mm',
                '%s - trestle_beam_h' % Z, Z, 'Trestle Beam ' + t)
            for s in (1, -1):
                yp = '(rail_cc / 2)' if s > 0 else '-(rail_cc / 2)'
                blk(c, '%s - trestle_w / 2' % X, '%s + trestle_w / 2' % X, '%s - trestle_w / 2' % yp,
                    '%s + trestle_w / 2' % yp, '0 mm', '%s - trestle_beam_h' % Z, 'Trestle Post %s%d' % (t, s))
            if z > 600:
                for s in (1, -1):
                    k2 = L.Sk(c, 'YZ')  # origin plane: L.ext extents are absolute
                    a = '%s(rail_cc / 2 - trestle_w / 2)' % ('' if s > 0 else '-')
                    b = '%s(rail_cc / 2 - trestle_w / 2)' % ('-' if s > 0 else '')
                    k2.poly([(X, a, '200 mm'), (X, a, '320 mm'), (X, b, '%s - trestle_beam_h - 80 mm' % Z),
                             (X, b, '%s - trestle_beam_h - 200 mm' % Z)])
                    sk = k2.done()
                    L.ext(c, sk, sk.profiles.item(0), '%s - 20 mm' % X, '%s + 20 mm' % X,
                          name='Trestle Brace %s%d' % (t, s))
        L.setmat(c, 'steel')
    print('trestles built for sections', [k + 1 for k in ks])


def step_c_net_base():
    """C: columns that raise the catch net's post and brace plates to the ramp top."""
    root = L.des().rootComponent
    for o in [o for o in root.occurrences if o.component.name == 'Net Base']:
        o.deleteMe()
    net = [o for o in root.occurrences if o.component.name.startswith(NET_NAME)][0]
    t = net.transform2.translation
    X, Z = '%.1f mm' % (t.x * 10), '%.1f mm' % (t.z * 10)
    c, _ = L.newcomp(root, 'Net Base')
    for s, sd in ((1, 'R'), (-1, 'L')):
        yp = '(wingspan / 2 + 400 mm + 60 mm)' if s > 0 else '-(wingspan / 2 + 400 mm + 60 mm)'
        for x0, nm in (('0 mm', 'Post'), ('1400 mm', 'Brace')):
            blk(c, '%s + %s - 100 mm' % (X, x0), '%s + %s + 100 mm' % (X, x0), '%s - 100 mm' % yp,
                '%s + 100 mm' % yp, '0 mm', Z, 'Net Column %s %s' % (nm, sd))
    L.setmat(c, 'steel')
    print('net raised by %.0f mm' % (t.z * 10))
