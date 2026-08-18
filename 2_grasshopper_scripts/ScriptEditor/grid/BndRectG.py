"""
Creates a grid of individual closed rectangular cells within a region.

Inputs:
    boundary: Geometry (item access, crv)
    size_x: Number (item access, float)
    size_y: Number (item access, float)

Outputs:
    rectgrid: List of Curves (The final individual closed rectangular cells)
    bnd_rect: Curve (The bounding rectangle of the original input)
"""

import Rhino.Geometry as rg
import os

try:
    ghenv.Component.Name = "BoundRectGrid"
    ghenv.Component.NickName = "BndRectG"
    ghenv.Component.Description = "Creates a grid of individual closed rectangular cells within a region."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Grid"
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
        "grid",
        "BndRectG.py"
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
