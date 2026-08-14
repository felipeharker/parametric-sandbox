"""
Creates commercial signage channel letters, generating solid bodies and illumination faces.

Inputs:
    curves: Geometry (list access, GeometryBase)
    sidewall_depth: Number (item access, float)
    standoff_distance: Number (item access, float)
    illumination: Integer (item access, int)

Outputs:
    curves: List of Curves (The originally input sign curves in their original position)
    body: List of Breps (The solid extruded and capped geometry of the sign)
    faces: List of Breps (The open surface faces of the illuminated signage)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "SignMaker"
    ghenv.Component.NickName = "SignMkr"
    ghenv.Component.Description = "Generates solid commercial signage channel letters with standoff and illumination faces."

    # --- Inputs Metadata ---
    # Index 0: curves
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "curves"
        ghenv.Component.Params.Input[0].NickName = "Crvs"
        ghenv.Component.Params.Input[0].Description = "Geometry (list access, GeometryBase)"

    # Index 1: sidewall_depth
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "sidewall_depth"
        ghenv.Component.Params.Input[1].NickName = "SidDe"
        ghenv.Component.Params.Input[1].Description = "Number (item access, float)"

    # Index 2: standoff_distance
    if ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.Input[2].Name = "standoff_distance"
        ghenv.Component.Params.Input[2].NickName = "StaDi"
        ghenv.Component.Params.Input[2].Description = "Number (item access, float)"

    # Index 3: illumination
    if ghenv.Component.Params.Input.Count > 3:
        ghenv.Component.Params.Input[3].Name = "illumination"
        ghenv.Component.Params.Input[3].NickName = "Illu"
        ghenv.Component.Params.Input[3].Description = "Integer (item access, int)"

    # --- Outputs Metadata ---
    # Index 0: curves
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "curves"
        ghenv.Component.Params.Output[0].NickName = "Crvs"
        ghenv.Component.Params.Output[0].Description = "List of Curves (The originally input sign curves in their original position)"

    # Index 1: body
    if ghenv.Component.Params.Output.Count > 1:
        ghenv.Component.Params.Output[1].Name = "body"
        ghenv.Component.Params.Output[1].NickName = "Body"
        ghenv.Component.Params.Output[1].Description = "List of Breps (The solid extruded and capped geometry of the sign)"

    # Index 2: faces
    if ghenv.Component.Params.Output.Count > 2:
        ghenv.Component.Params.Output[2].Name = "faces"
        ghenv.Component.Params.Output[2].NickName = "Face"
        ghenv.Component.Params.Output[2].Description = "List of Breps (The open surface faces of the illuminated signage)"

except NameError:
    pass

import Rhino.Geometry as rg

def create_signage():
    out_curves = []
    out_body = []
    out_faces = []

    # Validate inputs exist
    if not curves or sidewall_depth is None or standoff_distance is None or illumination is None:
        return out_curves, out_body, out_faces

    # 1. Process Mixed Inputs (Curves and Surfaces)
    all_base_curves = []

    for geom in curves:
        if not geom: continue

        # If it's a Curve, add it directly
        if isinstance(geom, rg.Curve):
            all_base_curves.append(geom)
            out_curves.append(geom)

        # If it's a Brep (Surface), extract its edges
        elif isinstance(geom, rg.Brep):
            for edge in geom.Edges:
                crv = edge.DuplicateCurve()
                all_base_curves.append(crv)
                out_curves.append(crv)

        # If it's a raw Surface, convert to Brep and extract edges
        elif isinstance(geom, rg.Surface):
            brep = geom.ToBrep()
            for edge in brep.Edges:
                crv = edge.DuplicateCurve()
                all_base_curves.append(crv)
                out_curves.append(crv)

    if not all_base_curves:
        return out_curves, out_body, out_faces

    # 2. Resolve Planar Regions (handles inner holes like the letter 'O')
    doc_tolerance = 0.001
    base_breps = rg.Brep.CreatePlanarBreps(all_base_curves, doc_tolerance)

    if not base_breps:
        return out_curves, out_body, out_faces

    z_vec = rg.Vector3d(0, 0, 1)

    # 3. Process Solid Sign Body
    for base_b in base_breps:
        # Create Bottom Cap (moved to standoff distance)
        back_cap = base_b.Duplicate()
        back_cap.Translate(z_vec * standoff_distance)

        # Create Top Cap (moved to standoff + sidewall depth)
        front_cap = base_b.Duplicate()
        front_cap.Translate(z_vec * (standoff_distance + sidewall_depth))

        # Extrude the edges of the back cap to create the sidewalls
        walls = []
        for edge in back_cap.Edges:
            wall_srf = rg.Surface.CreateExtrusion(edge, z_vec * sidewall_depth)
            if wall_srf:
                walls.append(wall_srf.ToBrep())

        # Join the caps and the walls together to create a closed solid
        breps_to_join = [back_cap, front_cap] + walls
        joined_solids = rg.Brep.JoinBreps(breps_to_join, doc_tolerance)

        if joined_solids:
            out_body.extend(joined_solids)

    # 4. Process Illumination Faces
    if illumination in [1, 2]:
        offset_dist = 1.0 / 32.0
        face_move_vec = rg.Vector3d.Zero

        if illumination == 1:
            # Front lit: 1/32" ABOVE the extruded body
            face_move_vec = z_vec * (standoff_distance + sidewall_depth + offset_dist)
        elif illumination == 2:
            # Reverse lit: 1/32" BELOW the extruded body
            face_move_vec = z_vec * (standoff_distance - offset_dist)

        for base_b in base_breps:
            face_b = base_b.Duplicate()
            face_b.Translate(face_move_vec)
            out_faces.append(face_b)

    return out_curves, out_body, out_faces

# Execute function and assign to outputs
curves, body, faces = create_signage()