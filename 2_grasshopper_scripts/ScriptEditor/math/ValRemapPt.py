"""
Remaps the distances between a list of points and an attractor point to a new target domain.

Inputs:
    attractor: Point3d (The attractor point to measure distances from)
    points: List of Point3d (The list of points to calculate distances to the attractor)
    value_a: Number (The start value of the target domain)
    value_b: Number (The end value of the target domain)

Outputs:
    remapped_values: List of Numbers (The remapped distance values)
"""

import os

try:
    ghenv.Component.Name = "ValueRemapPoint"
    ghenv.Component.NickName = "ValRemapPt"
    ghenv.Component.Description = "Remaps the distances between a list of points and an attractor point to a new target domain."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Math"
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
        "math",
        "ValRemapPt.py"
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
