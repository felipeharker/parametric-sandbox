"""
Utility to trim curves with a region, closing the curves along the intersection boundary if they were originally closed.

Inputs:
    curves: List of Curves (The open or closed curves to be trimmed)
    region: Curve (The closed boundary region to trim the curves against)

Outputs:
    trimmed_curves: List of Curves (The resulting trimmed and appropriately closed curves)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "BoundTrim"
    ghenv.Component.NickName = "BndTrim"
    ghenv.Component.Description = "Utility to trim curves with a region, closing the curves along the intersection boundary if they were originally closed."

    # --- Inputs Metadata ---
    # Index 0: curves
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "curves"
        ghenv.Component.Params.Input[0].NickName = "Crvs"
        ghenv.Component.Params.Input[0].Description = "List of Curves (The open or closed curves to be trimmed)"

    # Index 1: region
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "region"
        ghenv.Component.Params.Input[1].NickName = "Reg"
        ghenv.Component.Params.Input[1].Description = "Curve (The closed boundary region to trim the curves against)"

    # --- Outputs Metadata ---
    # Index 0: trimmed_curves
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "trimmed_curves"
        ghenv.Component.Params.Output[0].NickName = "Trim"
        ghenv.Component.Params.Output[0].Description = "List of Curves (The resulting trimmed and appropriately closed curves)"

except NameError:
    pass

import Rhino.Geometry as rg
import scriptcontext as sc

tol = sc.doc.ModelAbsoluteTolerance
trimmed_curves = []

if curves and region:
    if region.IsClosed:
        rc, reg_plane = region.TryGetPlane(tol)
        if not rc:
            reg_plane = rg.Plane.WorldXY

        for crv in curves:
            if crv is None:
                continue

            if crv.IsClosed:
                res = rg.Curve.CreateBooleanIntersection(crv, region, tol)
                if res:
                    trimmed_curves.extend(res)

            else:
                intersections = rg.Intersect.Intersection.CurveCurve(crv, region, tol, tol)

                if intersections and intersections.Count > 0:
                    params = []
                    for i in range(intersections.Count):
                        params.append(intersections[i].ParameterA)

                    split_crvs = crv.Split(params)

                    if split_crvs:
                        for s_crv in split_crvs:
                            mid_pt = s_crv.PointAt(s_crv.Domain.Mid)
                            if region.Contains(mid_pt, reg_plane, tol) == rg.PointContainment.Inside:
                                trimmed_curves.append(s_crv)
                    else:
                        mid_pt = crv.PointAt(crv.Domain.Mid)
                        if region.Contains(mid_pt, reg_plane, tol) == rg.PointContainment.Inside:
                            trimmed_curves.append(crv)

                else:
                    mid_pt = crv.PointAt(crv.Domain.Mid)
                    if region.Contains(mid_pt, reg_plane, tol) == rg.PointContainment.Inside:
                        trimmed_curves.append(crv)