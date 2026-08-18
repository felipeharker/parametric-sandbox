"""
Draws a boundary rectangle around a geometry based on a user-defined plane.

Inputs:
    geo: Geometry (item access, geo)
    plane: Plane (item access, plane)

Outputs:
    bnd_rect: Curve (The bounding rectangle aligned to the input plane)
    x: Number (Dimension in the first axis of the plane)
    y: Number (Dimension in the second axis of the plane)
"""

import Rhino.Geometry as rg
import os

try:
    ghenv.Component.Name = "GeometryBoundary2D"
    ghenv.Component.NickName = "GeoBnd2D"
    ghenv.Component.Description = "Draws a boundary rectangle around a geometry based on a user-defined plane."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Geometry"
except NameError:
    pass


# 1. Resolve the path dynamically based on the Grasshopper file location
gh_doc = ghenv.Component.OnPingDocument()

if gh_doc and gh_doc.FilePath:
    gh_dir = os.path.dirname(gh_doc.FilePath)

    # Target your specific script
    script_path = os.path.join(
        gh_dir,
        "2_grasshopper_scripts",
        "0_scripts",
        "geometry",
        "GeoBnd2D.py"
    )

    # 2. Execute the external code
    if os.path.exists(script_path):
        with open(script_path, 'r') as file:
            # exec() runs the script within the current namespace.
            # It will automatically pick up the inputs
            # and populate the outputs back into the component.
            exec(file.read(), globals(), locals())
    else:
        print(f"Error: Could not find script at {script_path}")
else:
    print("Warning: Please save the Grasshopper document first so relative paths work.")
