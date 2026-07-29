import math
import Rhino
from Rhino.Geometry import Point3d, Polyline, PolylineCurve
from Rhino.Geometry.Intersect import Intersection
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

def _is_closed_planar(crv, tol):
    if crv is None: return False
    if not crv.IsClosed: return False
    ok, _ = crv.TryGetPlane(tol)
    return ok

def _curve_plane(crv, tol):
    ok, pln = crv.TryGetPlane(tol)
    return pln if ok else None

def _hex_pts_xy(cx, cy, rx, ry):
    # pointy-top hex; rx stretches X, ry stretches Y
    pts = []
    for k in range(6):
        ang = math.radians(30.0 + 60.0 * k)
        pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    return pts

def _rect_pts_xy(cx, cy, rx, ry):
    # axis-aligned rectangle; if rx==ry it's a square
    return [
        (cx - rx, cy - ry),
        (cx + rx, cy - ry),
        (cx + rx, cy + ry),
        (cx - rx, cy + ry),
    ]

def _poly_fully_inside(cell_crv, boundary, plane, tol):
    ok, pl = cell_crv.TryGetPolyline()
    if not ok:
        return False

    # all vertices must be inside (or on boundary)
    for i in range(pl.Count - 1):
        if boundary.Contains(pl[i], plane, tol) == Rhino.Geometry.PointContainment.Outside:
            return False

    # any intersection (including touching) rejects
    x = Intersection.CurveCurve(cell_crv, boundary, tol, tol)
    if x and x.Count > 0:
        return False

    return True

# ----------------------------
# Main
# ----------------------------
GridCells = []
R = DataTree[object]()  # rows
C = DataTree[object]()  # cols

if B is None or RadX is None:
    GridCells = []
else:
    tol = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance if Rhino.RhinoDoc.ActiveDoc else 1e-6

    rx = float(RadX)
    if rx <= 0.0:
        GridCells = []
    else:
        # Critical rule: if RadY == 0 -> regular polygons
        if RadY is None:
            ry = rx
        else:
            ry_in = float(RadY)
            ry = rx if abs(ry_in) <= tol else ry_in

        if not _is_closed_planar(B, tol):
            GridCells = []
        else:
            plane = _curve_plane(B, tol)

            # boundary plane coords -> World XY
            xform_w2p = Rhino.Geometry.Transform.ChangeBasis(plane, Rhino.Geometry.Plane.WorldXY)
            xform_p2w = Rhino.Geometry.Transform.ChangeBasis(Rhino.Geometry.Plane.WorldXY, plane)

            B2 = B.DuplicateCurve()
            B2.Transform(xform_w2p)

            mp = Rhino.Geometry.AreaMassProperties.Compute(B2)
            ctr2 = mp.Centroid if mp else B2.GetBoundingBox(True).Center

            use_hex = True if Type else False

            # Grid spacing derived from rx/ry
            if use_hex:
                dx = math.sqrt(3.0) * rx
                dy = 1.5 * ry
            else:
                dx = 2.0 * rx
                dy = 2.0 * ry

            bb = B2.GetBoundingBox(True)
            minx = bb.Min.X - 2.0 * dx
            maxx = bb.Max.X + 2.0 * dx
            miny = bb.Min.Y - 2.0 * dy
            maxy = bb.Max.Y + 2.0 * dy

            j_min = int(math.floor((miny - ctr2.Y) / dy)) - 1
            j_max = int(math.ceil((maxy - ctr2.Y) / dy)) + 1
            i_min = int(math.floor((minx - ctr2.X) / dx)) - 1
            i_max = int(math.ceil((maxx - ctr2.X) / dx)) + 1

            cells_by_row = {}  # j -> list of (i, curve)
            cells_by_col = {}  # i -> list of (j, curve)

            for j in range(j_min, j_max + 1):
                y = ctr2.Y + j * dy
                row_offset = (0.5 * dx if (use_hex and (j & 1)) else 0.0)

                for i in range(i_min, i_max + 1):
                    x = ctr2.X + i * dx + row_offset
                    cpt2 = Point3d(x, y, 0.0)

                    # quick cull: center must be inside
                    if B2.Contains(cpt2, Rhino.Geometry.Plane.WorldXY, tol) == Rhino.Geometry.PointContainment.Outside:
                        continue

                    # build candidate cell in plane coords (WorldXY)
                    if use_hex:
                        verts = _hex_pts_xy(x, y, rx, ry)
                    else:
                        verts = _rect_pts_xy(x, y, rx, ry)

                    pts = [Point3d(vx, vy, 0.0) for (vx, vy) in verts]
                    pts.append(pts[0])

                    pline = Polyline(pts)
                    if not pline.IsValid:
                        continue

                    cell2 = PolylineCurve(pline)

                    if not _poly_fully_inside(cell2, B2, Rhino.Geometry.Plane.WorldXY, tol):
                        continue

                    cell_w = cell2.DuplicateCurve()
                    cell_w.Transform(xform_p2w)

                    GridCells.append(cell_w)
                    cells_by_row.setdefault(j, []).append((i, cell_w))
                    cells_by_col.setdefault(i, []).append((j, cell_w))

            # Rows -> R (branches ordered by j, items ordered by i)
            row_keys = sorted(cells_by_row.keys())
            for r_idx, j in enumerate(row_keys):
                path = GH_Path(r_idx)
                for (_, crv) in sorted(cells_by_row[j], key=lambda t: t[0]):
                    R.Add(crv, path)

            # Cols -> C (branches ordered by i, items ordered by j)
            col_keys = sorted(cells_by_col.keys())
            for c_idx, i in enumerate(col_keys):
                path = GH_Path(c_idx)
                for (_, crv) in sorted(cells_by_col[i], key=lambda t: t[0]):
                    C.Add(crv, path)
