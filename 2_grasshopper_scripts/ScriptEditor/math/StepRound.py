#! python 3
# category: CustomLib
# subcategory: Math

"""
Rounds a list of numbers to the nearest specified step value.

Inputs:
    values: List (The unrounded list of values)
    step: Float (Numeric step for rounding)

Outputs:
    stepped_values: List (The newly rounded values)
"""

import os

try:
    ghenv.Component.Name = "StepRounding"
    ghenv.Component.NickName = "StepRound"
    ghenv.Component.Description = "Rounds a list of numbers to the nearest value of a given step."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Math"
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
        "math",
        "StepRound.py"
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
