#! python 3
# category: CustomLib
# subcategory: Signage

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

import Rhino.Geometry as rg
import os

try:
    ghenv.Component.Name = "SignMaker"
    ghenv.Component.NickName = "SignMkr"
    ghenv.Component.Description = "Generates solid commercial signage channel letters with standoff and illumination faces."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Signage"
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
        "signage",
        "SignMaker.py"
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
