"""
Utility to generate a 7-item boolean list for the PattGen component by allowing users to toggle individual point generators.

Inputs:
    use_centroid: Boolean (Toggle for Cell Centroid - Point 1)
    use_outer_mid: Boolean (Toggle for Outer Cell Midpoints - Point 2)
    use_outer_vert: Boolean (Toggle for Outer Cell Vertices - Point 3)
    use_outer_eval: Boolean (Toggle for Outer Cell Evaluated Points - Point 4)
    use_inner_mid: Boolean (Toggle for Inner Cell Midpoints - Point 5)
    use_inner_vert: Boolean (Toggle for Inner Cell Vertices - Point 6)
    use_inner_eval: Boolean (Toggle for Inner Cell Evaluated Points - Point 7)

Outputs:
    point_toggle: List of Booleans (A 7-item list to plug directly into the PattGen component)
"""

import os

try:
    ghenv.Component.Name = "VoronoiPatternSelectionUtility"
    ghenv.Component.NickName = "VoroPattSelUtil"
    ghenv.Component.Description = "Utility to generate a 7-item boolean toggle list for the PattGen component by allowing users to toggle individual point generators."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Pattern"
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
        "pattern",
        "pattern_1",
        "VoroPattSelUtil.py"
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
