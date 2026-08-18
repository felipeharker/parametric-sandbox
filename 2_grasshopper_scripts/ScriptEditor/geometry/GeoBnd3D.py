#! python 3
# category: CustomLib
# subcategory: Geometry

"""
Draws a boundary box around a geometry.

Inputs:
    geo: Geometry (item access, geo)

Outputs:
    bnd_box: Box (The 3D bounding box of the original geometry)
    x: Number (Dimension in the first axis)
    y: Number (Dimension in the second axis)
    z: Number (Dimension in the third axis)
"""

import Rhino.Geometry as rg
import os

try:
    ghenv.Component.Name = "GeometryBoundary3D"
    ghenv.Component.NickName = "GeoBnd3D"
    ghenv.Component.Description = "Draws a boundary box around a geometry."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Geometry"
    ghenv.Component.Message = ""
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
        "GeoBnd3D.py"
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
