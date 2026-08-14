"""
Creates folded 3-dimensional gridded geometries efficiently from planar cells and fold lines.
Includes an option to output closed solid wedges for each folded fragment.

Inputs:
    grid_cells: List of Curves (list access, closed crv)
    fold_lines: DataTree of Curves (tree access, open crv)
    fold_angle: Number (item access, float)
    solid: Boolean (item access, bool)

Outputs:
    folded_cells: List of Breps (The final 3D folded geometries)
"""

import Rhino.Geometry as rg
import math
import scriptcontext as sc

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "GridFoldWedge"
    ghenv.Component.NickName = "GridFWed"
    ghenv.Component.Description = "Creates folded 3D gridded geometries efficiently."

    # --- Inputs Metadata ---
    # Index 0: grid_cells
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "grid_cells"
        ghenv.Component.Params.Input[0].NickName = "GC"
        ghenv.Component.Params.Input[0].Description = "List of Curves (list access, closed crv)"

    # Index 1: fold_lines
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "fold_lines"
        ghenv.Component.Params.Input[1].NickName = "Folds"
        ghenv.Component.Params.Input[1].Description = "DataTree of Curves (tree access, open crv)"

    # Index 2: fold_angle
    if ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.Input[2].Name = "fold_angle"
        ghenv.Component.Params.Input[2].NickName = "Ang"
        ghenv.Component.Params.Input[2].Description = "Number (item access, float)"

    # Index 3: solid
    if ghenv.Component.Params.Input.Count > 3:
        ghenv.Component.Params.Input[3].Name = "solid"
        ghenv.Component.Params.Input[3].NickName = "Soli"
        ghenv.Component.Params.Input[3].Description = "Boolean (item access, bool)"

    # --- Outputs Metadata ---
    # Index 0: folded_cells
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "folded_cells"
        ghenv.Component.Params.Output[0].NickName = "FolCe"
        ghenv.Component.Params.Output[0].Description = "List of Breps (The final 3D folded geometries)"

except NameError:
    pass

folded_cells = []
tol = sc.doc.ModelAbsoluteTolerance

if grid_cells and fold_lines and fold_angle is not None:
    # Set default for solid toggle if no boolean is provided
    solid_toggle = False if solid is None else solid

    # Convert input angle from degrees to radians
    angle_rad = math.radians(fold_angle)

    # Check if DataTree branches perfectly match the list of cells
    match_trees = fold_lines.BranchCount == len(grid_cells)

    flat_fold_lines = []
    if not match_trees:
        if hasattr(fold_lines, 'AllData'):
            flat_fold_lines = fold_lines.AllData()
        else:
            flat_fold_lines = fold_lines

    for i, cell in enumerate(grid_cells):
        if not cell or not cell.IsClosed:
            continue

        # Create planar surface from cell
        breps = rg.Brep.CreatePlanarBreps(cell, tol)
        if not breps:
            continue
        base_brep = breps[0]

        # Determine the plane of the cell to establish a consistent normal
        success, plane = cell.TryGetPlane(tol)
        if not success:
            plane = rg.Plane.WorldXY
        normal = plane.ZAxis

        associated_lines = []
        if match_trees:
            associated_lines = fold_lines.Branch(i)
        else:
            for f_line in flat_fold_lines:
                if not f_line: continue
                mp = f_line.PointAtNormalizedLength(0.5)
                containment = cell.Contains(mp, plane, tol)
                if containment == rg.PointContainment.Inside or containment == rg.PointContainment.Coincident:
                    associated_lines.append(f_line)

        if not associated_lines:
            folded_cells.append(base_brep)
            continue

        # Split the cell's face using the inner fold lines
        split_breps = base_brep.Split(associated_lines, tol)

        if not split_breps:
            folded_cells.append(base_brep)
            continue

        for s_brep in split_breps:
            hinge_edge = None

            # Find the hinge edge along the outer boundary
            for edge in s_brep.Edges:
                edge_mp = edge.PointAtNormalizedLength(0.5)
                success, t = cell.ClosestPoint(edge_mp)
                if success and edge_mp.DistanceTo(cell.PointAt(t)) <= tol * 10:
                    hinge_edge = edge
                    break

            if hinge_edge:
                # Find mathematical center to establish fold direction
                vertices = s_brep.Vertices
                pt_sum = rg.Point3d.Origin
                for v in vertices:
                    pt_sum += v.Location
                face_center = pt_sum / vertices.Count

                edge_mp = hinge_edge.PointAtNormalizedLength(0.5)

                axis_vec = hinge_edge.PointAtEnd - hinge_edge.PointAtStart
                vec_inward = face_center - edge_mp

                # Cross product logic to ensure panel folds "up"
                cross = rg.Vector3d.CrossProduct(axis_vec, vec_inward)
                if cross * normal < 0:
                    axis_vec.Reverse()

                center_pt = hinge_edge.PointAtStart
                xform = rg.Transform.Rotation(angle_rad, axis_vec, center_pt)

                # ---------------------------------------------------------
                # SOLID WEDGE LOGIC
                # ---------------------------------------------------------
                if solid_toggle:
                    flat_face = s_brep.DuplicateBrep()
                    rot_face = s_brep.DuplicateBrep()
                    rot_face.Transform(xform)

                    breps_to_join = [flat_face, rot_face]

                    # Iterate through the edges to build side walls
                    for e_idx in range(flat_face.Edges.Count):
                        edge_f = flat_face.Edges[e_idx].ToNurbsCurve()
                        edge_r = rot_face.Edges[e_idx].ToNurbsCurve()

                        mp_f = edge_f.PointAtNormalizedLength(0.5)
                        mp_r = edge_r.PointAtNormalizedLength(0.5)

                        # Only build a side wall if the edge actually moved (skip the hinge)
                        if mp_f.DistanceTo(mp_r) > tol * 10:
                            ruled_srf = rg.NurbsSurface.CreateRuledSurface(edge_f, edge_r)
                            if ruled_srf:
                                breps_to_join.append(rg.Brep.CreateFromSurface(ruled_srf))

                    # Stitch the base, top, and walls into a closed solid
                    joined = rg.Brep.JoinBreps(breps_to_join, tol)
                    if joined:
                        folded_cells.append(joined[0])
                    else:
                        # Fallback just in case joining fails on a bad tolerance
                        folded_cells.append(rot_face)

                # ---------------------------------------------------------
                # OPEN PLANAR LOGIC
                # ---------------------------------------------------------
                else:
                    rot_face = s_brep.DuplicateBrep()
                    rot_face.Transform(xform)
                    folded_cells.append(rot_face)
            else:
                folded_cells.append(s_brep)