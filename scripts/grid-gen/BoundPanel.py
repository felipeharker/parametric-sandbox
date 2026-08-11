"""
Creates a grid of rectangular panels that perfectly fit within a bounding curve.

Inputs:
    boundary: Geometry (item access, crv)
    size_x: Number (item access, float)
    size_y: Number (item access, float)
    use_world_xy: Boolean (item access, bool)

Outputs:
    panels: List of Curves (The rectangular panels)
"""

try:
    ghenv.Component.Name = "BoundPanel"
    ghenv.Component.NickName = "BPanel"
    ghenv.Component.Description = "Creates a grid of rectangular panels that perfectly fit within a bounding curve."
except NameError:
    pass

import Rhino
import scriptcontext as sc
from Rhino.Geometry import Plane, Rectangle3d, Interval

def _doc_tol():
    if sc.doc:
        return sc.doc.ModelAbsoluteTolerance
    if Rhino.RhinoDoc.ActiveDoc:
        return Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance
    return 1e-3

def sizes_1d(L, S, tol):
    if S <= tol:
        return [L]

    n_full = int(L // S)
    rem = L - (n_full * S)

    if abs(rem) <= tol:
        return [S] * n_full

    cap = 0.5 * rem

    if cap <= tol:
        return [S] * n_full

    return [cap] + ([S] * n_full) + [cap]

panels = []

if 'boundary' in globals() and boundary is not None:
    tol = _doc_tol()

    if 'use_world_xy' in globals() and use_world_xy:
        pl = Plane.WorldXY
    else:
        ok, pl = boundary.TryGetPlane(tol)
        if not ok:
            pl = Plane.WorldXY

    bb = boundary.GetBoundingBox(pl)

    Lx = bb.Max.X - bb.Min.X
    Ly = bb.Max.Y - bb.Min.Y

    x_sizes = sizes_1d(Lx, float(size_x), tol)
    y_sizes = sizes_1d(Ly, float(size_y), tol)

    x0 = bb.Min.X
    for sx in x_sizes:
        y0 = bb.Min.Y
        for sy in y_sizes:
            rect = Rectangle3d(
                pl,
                Interval(x0, x0 + sx),
                Interval(y0, y0 + sy)
            )
            panels.append(rect.ToNurbsCurve())
            y0 += sy
        x0 += sx
