"""
Creates parametric tab perforations within a frame boundary for an aluminum panel system.

Inputs:
    boundary: Geometry (item access, crv)
    tab_height: Number (item access, float)
    tab_width: Number (item access, float)
    tab_space_x: Number (item access, float)
    tab_space_y: Number (item access, float)

Outputs:
    frame_face: Curve (The original rectangular frame face)
    tabs: List of Curves (The curves representing the newly created tabs/openings)
"""

import Rhino.Geometry as rg

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "FrameTabSystem"
    ghenv.Component.NickName = "FrmTab"
    ghenv.Component.Description = "Creates parametric tab perforations within a frame boundary for an aluminum panel system."

    # --- Inputs Metadata ---
    # Index 0: boundary
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "boundary"
        ghenv.Component.Params.Input[0].NickName = "Bnd"
        ghenv.Component.Params.Input[0].Description = "Geometry (item access, crv)"

    # Index 1: tab_height
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "tab_height"
        ghenv.Component.Params.Input[1].NickName = "THgt"
        ghenv.Component.Params.Input[1].Description = "Number (item access, float)"

    # Index 2: tab_width
    if ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.Input[2].Name = "tab_width"
        ghenv.Component.Params.Input[2].NickName = "TWid"
        ghenv.Component.Params.Input[2].Description = "Number (item access, float)"

    # Index 3: tab_space_x
    if ghenv.Component.Params.Input.Count > 3:
        ghenv.Component.Params.Input[3].Name = "tab_space_x"
        ghenv.Component.Params.Input[3].NickName = "TabSp"
        ghenv.Component.Params.Input[3].Description = "Number (item access, float)"

    # Index 4: tab_space_y
    if ghenv.Component.Params.Input.Count > 4:
        ghenv.Component.Params.Input[4].Name = "tab_space_y"
        ghenv.Component.Params.Input[4].NickName = "TabSp"
        ghenv.Component.Params.Input[4].Description = "Number (item access, float)"

    # --- Outputs Metadata ---
    # Index 0: frame_face
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "frame_face"
        ghenv.Component.Params.Output[0].NickName = "FraFa"
        ghenv.Component.Params.Output[0].Description = "Curve (The original rectangular frame face)"

    # Index 1: tabs
    if ghenv.Component.Params.Output.Count > 1:
        ghenv.Component.Params.Output[1].Name = "tabs"
        ghenv.Component.Params.Output[1].NickName = "Tabs"
        ghenv.Component.Params.Output[1].Description = "List of Curves (The curves representing the newly created tabs/openings)"

except NameError:
    pass

def create_frame_tabs(boundary, tab_height, tab_width, tab_space_x, tab_space_y):
    # Data validation
    if not boundary or tab_height is None or tab_width is None or tab_space_x is None or tab_space_y is None:
        return None, []

    # Attempt to get the local plane of the boundary curve to ensure it works in 3D space
    rc, plane = boundary.TryGetPlane()
    if not rc:
        plane = rg.Plane.WorldXY

    # Get bounding box aligned to the valid plane
    bbox = boundary.GetBoundingBox(plane)

    min_x = bbox.Min.X
    max_x = bbox.Max.X
    min_y = bbox.Min.Y
    max_y = bbox.Max.Y

    height = max_y - min_y
    mid_x = min_x + ((max_x - min_x) / 2.0)

    # 1. Frame Face Output
    frame_face = boundary

    # 2. Tabs Output
    tabs = []

    # Determine the number of tab sets on the Y axis
    num_tabs = max(1, int(round(height / tab_space_y)))

    mid_y = min_y + (height / 2.0)
    y_centers = []

    # Calculate tab centerpoints expanding outward from the middle
    if num_tabs % 2 == 1:
        # Odd number of tabs (1 center tab + mirrored pairs)
        half_count = num_tabs // 2
        for i in range(-half_count, half_count + 1):
            y_centers.append(mid_y + i * tab_space_y)
    else:
        # Even number of tabs (mirrored pairs offset from center)
        half_count = num_tabs // 2
        for i in range(1, half_count + 1):
            y_centers.append(mid_y + (i - 0.5) * tab_space_y)
            y_centers.append(mid_y - (i - 0.5) * tab_space_y)

    # Calculate the X centers for the two perforations based on spacing from the face middle
    left_x_center = mid_x - (tab_space_x / 2.0)
    right_x_center = mid_x + (tab_space_x / 2.0)

    # Generate the 2 tab openings at each calculated Y height
    for cy in y_centers:
        tab_y_int = rg.Interval(cy - tab_height / 2.0, cy + tab_height / 2.0)

        # Left Tab Opening
        left_tab_x = rg.Interval(left_x_center - tab_width / 2.0, left_x_center + tab_width / 2.0)
        left_tab = rg.Rectangle3d(plane, left_tab_x, tab_y_int).ToNurbsCurve()
        tabs.append(left_tab)

        # Right Tab Opening
        right_tab_x = rg.Interval(right_x_center - tab_width / 2.0, right_x_center + tab_width / 2.0)
        right_tab = rg.Rectangle3d(plane, right_tab_x, tab_y_int).ToNurbsCurve()
        tabs.append(right_tab)

    return frame_face, tabs

frame_face, tabs = create_frame_tabs(boundary, tab_height, tab_width, tab_space_x, tab_space_y)