"""
Sorts a list of strings using Natural Sorting (e.g., 2 comes before 10).

Inputs:
    values: List of Strings (list access, str)

Outputs:
    sorted_values: List of Strings (The naturally sorted list)
"""

import re
import os

try:
    ghenv.Component.Name = "StringSort"
    ghenv.Component.NickName = "StrSort"
    ghenv.Component.Description = "Sorts a list of strings using Natural Sorting."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Utility"
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
        "utility",
        "StrSort.py"
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
