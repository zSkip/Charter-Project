"""Helpers for the Drone Rail Recovery Fusion build.

All geometry is drawn at its evaluated position, then every sketch point is
dimensioned from the sketch origin with a parameter expression, so the
sketches are fully driven by User Parameters. Expressions are mm strings.
"""
import adsk.core
import adsk.fusion

app = adsk.core.Application.get()
VI = adsk.core.ValueInput.createByString
P3 = adsk.core.Point3D.create
V3 = adsk.core.Vector3D.create
NEW = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
JOIN = adsk.fusion.FeatureOperations.JoinFeatureOperation
CUT = adsk.fusion.FeatureOperations.CutFeatureOperation
HOR = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
VER = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation


def des():
    return adsk.fusion.Design.cast(app.activeProduct)


def ev(e):
    """Evaluate a length expression and return mm."""
    return des().unitsManager.evaluateExpression(e, 'mm') * 10.0


def evu(e, units):
    return des().unitsManager.evaluateExpression(e, units)


def pos(e):
    """Expression for |e| using its current sign."""
    return '(%s)' % e if ev(e) > 0 else '-(%s)' % e


def set_params(plist):
    up = des().userParameters
    for name, expr, units, comment in plist:
        p = up.itemByName(name)
        if p:
            p.expression = expr
            p.comment = comment
        else:
            up.add(name, VI(expr), units, comment)


def newcomp(parent, name):
    occ = parent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    return occ.component, occ


class Sk:
    """Sketch on a component origin plane (optionally offset by an expression)."""

    def __init__(self, comp, kind, off=None):
        base = {'XY': comp.xYConstructionPlane, 'XZ': comp.xZConstructionPlane,
                'YZ': comp.yZConstructionPlane}[kind]
        pl = base
        if off is not None and abs(ev(off)) > 1e-6:
            n = base.geometry.normal
            sgn = [n.x, n.y, n.z][{'XY': 2, 'XZ': 1, 'YZ': 0}[kind]]
            ci = comp.constructionPlanes.createInput()
            ci.setByOffset(base, VI(off if sgn > 0 else '-(%s)' % off))
            pl = comp.constructionPlanes.add(ci)
        self.sk = comp.sketches.add(pl)
        sk = self.sk
        o = sk.modelToSketchSpace(P3(0, 0, 0))
        self.ax = [None, None]
        for i in range(3):
            v = [0.0, 0.0, 0.0]
            v[i] = 1.0
            p = sk.modelToSketchSpace(P3(*v))
            if abs(p.x - o.x) > 0.5:
                self.ax[0] = i
            if abs(p.y - o.y) > 0.5:
                self.ax[1] = i
        sk.isComputeDeferred = True
        self.reg = [{}, {}]

    def pt(self, e3):
        p = self.sk.modelToSketchSpace(P3(*[ev(e) / 10.0 for e in e3]))
        return P3(p.x, p.y, 0)

    def fix(self, sp, e3):
        # Fusion refuses two origin dimensions with the same value and
        # direction, so later points with that value are aligned to the first.
        sk = self.sk
        gc = sk.geometricConstraints
        o = sk.originPoint
        g = sp.geometry
        for k, orient in ((0, HOR), (1, VER)):
            e = e3[self.ax[k]]
            val = g.x if k == 0 else g.y
            key = round(val, 6)
            align = gc.addVerticalPoints if k == 0 else gc.addHorizontalPoints
            if abs(val) < 1e-6:
                align(o, sp)
            elif key in self.reg[k]:
                align(self.reg[k][key], sp)
            else:
                d = sk.sketchDimensions.addDistanceDimension(o, sp, orient, P3(g.x + 0.3, g.y + 0.3, 0))
                d.parameter.expression = pos(e)
                self.reg[k][key] = sp

    def poly(self, P, arcs=None):
        """Closed loop through model points P (expr triples). arcs {i: (mid, r)}: segment i->i+1 is an arc."""
        arcs = arcs or {}
        n = len(P)
        G = [self.pt(e) for e in P]
        S = [None] * n
        cv = self.sk.sketchCurves
        made = []
        for i, (mid, r) in arcs.items():
            j = (i + 1) % n
            a = cv.sketchArcs.addByThreePoints(G[i], self.pt(mid), G[j])
            sp, ep = a.startSketchPoint, a.endSketchPoint
            if sp.geometry.distanceTo(G[i]) < ep.geometry.distanceTo(G[i]):
                S[i], S[j] = sp, ep
            else:
                S[i], S[j] = ep, sp
            made.append((a, r))
        for i in range(n):
            if i in arcs:
                continue
            j = (i + 1) % n
            a = S[i] if S[i] is not None else G[i]
            b = S[j] if S[j] is not None else G[j]
            ln = cv.sketchLines.addByTwoPoints(a, b)
            if S[i] is None:
                S[i] = ln.startSketchPoint
            if S[j] is None:
                S[j] = ln.endSketchPoint
        for i in range(n):
            self.fix(S[i], P[i])
        for a, r in made:
            c = a.centerSketchPoint.geometry
            d = self.sk.sketchDimensions.addRadialDimension(a, P3(c.x + 0.5, c.y + 0.5, 0))
            d.parameter.expression = r
        return S

    def rect(self, c1, c2):
        u, v = self.ax

        def mk(a, b):
            e = list(c1)
            e[u] = a[u]
            e[v] = b[v]
            return tuple(e)
        return self.poly([mk(c1, c1), mk(c2, c1), mk(c2, c2), mk(c1, c2)])

    def circle(self, c3, dia):
        g = self.pt(c3)
        c = self.sk.sketchCurves.sketchCircles.addByCenterRadius(g, ev(dia) / 20.0)
        self.fix(c.centerSketchPoint, c3)
        d = self.sk.sketchDimensions.addDiameterDimension(c, P3(g.x + 0.7, g.y + 0.7, 0))
        d.parameter.expression = dia
        return c

    def line(self, a3, b3):
        ln = self.sk.sketchCurves.sketchLines.addByTwoPoints(self.pt(a3), self.pt(b3))
        self.fix(ln.startSketchPoint, a3)
        self.fix(ln.endSketchPoint, b3)
        return ln

    def done(self):
        self.sk.isComputeDeferred = False
        return self.sk


def profs(sk, loops=None):
    col = adsk.core.ObjectCollection.create()
    for p in sk.profiles:
        if loops is None or p.profileLoops.count == loops:
            col.add(p)
    return col


def ext(comp, sk, prof, a, b, op=NEW, bodies=None, name=None):
    """Extrude along the sketch normal so the solid spans model coordinate a..b."""
    n = sk.xDirection.crossProduct(sk.yDirection)
    c = [n.x, n.y, n.z]
    k = max(range(3), key=lambda i: abs(c[i]))
    if ev(a) > ev(b):
        a, b = b, a
    start = a if c[k] > 0 else '-(%s)' % b
    dist = '(%s) - (%s)' % (b, a)
    fs = comp.features.extrudeFeatures
    inp = fs.createInput(prof, op)
    if abs(ev(start)) > 1e-6:
        inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI(start))
    inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI(dist)),
                         adsk.fusion.ExtentDirections.PositiveExtentDirection)
    if bodies:
        inp.participantBodies = bodies
    f = fs.add(inp)
    if name and op == NEW:
        f.bodies.item(0).name = name
    return f


def sweep_path(comp, prof, curve, name=None):
    path = comp.features.createPath(curve, False)
    sw = comp.features.sweepFeatures
    inp = sw.createInput(prof, path, NEW)
    inp.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
    f = sw.add(inp)
    if name:
        f.bodies.item(0).name = name
    return f


def fillet(comp, edges, r):
    fs = comp.features.filletFeatures
    fi = fs.createInput()
    col = adsk.core.ObjectCollection.create()
    for e in edges:
        col.add(e)
    fi.edgeSetInputs.addConstantRadiusEdgeSet(col, VI(r), True)
    return fs.add(fi)


def shell(comp, faces, t):
    col = adsk.core.ObjectCollection.create()
    for f in faces:
        col.add(f)
    si = comp.features.shellFeatures.createInput(col, False)
    si.insideThickness = VI(t)
    return comp.features.shellFeatures.add(si)


def hole_z(comp, body, pts, d, z0, z1):
    k = Sk(comp, 'XY')
    for x, y in pts:
        k.circle((x, y, '0 mm'), d)
    sk = k.done()
    return ext(comp, sk, profs(sk), z0, z1, CUT, [body])


_MATS = {}
_WANT = {'al': ['Aluminum 6061', 'Aluminum'],
         'cf': ['Carbon Fiber', 'Carbon'],
         'steel': ['Steel', 'Steel, Alloy'],
         'uhmw': ['UHMW, White', 'UHMW'],
         'pekkcf': ['Carbon Fibers']}
CFRP = 'CFRP (carbon fibre)'


def mat(key):
    if key in _MATS:
        return _MATS[key]
    if key == 'cf':  # no CFRP laminate in the library: copy PEKK-CF, set 1.55 g/cm3
        d = des()
        m = d.materials.itemByName(CFRP)
        if not m:
            m = d.materials.addByCopy(mat('pekkcf'), CFRP)
            p = m.materialProperties.itemByName('Density')
            v = p.value
            p.value = 0.00155 if v < 0.01 else (1.55 if v < 10 else 1550.0)
        _MATS[key] = m
        return m
    libs = [l for l in app.materialLibraries if 'Fusion' in l.name and 'Material' in l.name]
    libs = libs or list(app.materialLibraries)
    found = None
    for w in _WANT[key]:
        for exact in (True, False):
            for l in libs:
                for i in range(l.materials.count):
                    m = l.materials.item(i)
                    if (m.name == w) if exact else (w.lower() in m.name.lower()):
                        found = m
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
    _MATS[key] = found
    return found


def setmat(comp, key):
    m = mat(key)
    if m:
        for b in comp.bRepBodies:
            b.material = m


def shot(path, eye, target, extent=None, w=800, h=600):
    vp = app.activeViewport
    cam = vp.camera
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.eye = P3(*[c / 10.0 for c in eye])
    cam.target = P3(*[c / 10.0 for c in target])
    cam.upVector = V3(0, 0, 1)
    if extent:
        cam.viewExtents = extent / 10.0
    vp.camera = cam
    if not extent:
        vp.fit()
    vp.refresh()
    adsk.doEvents()
    return vp.saveAsImageFile(path, w, h)
