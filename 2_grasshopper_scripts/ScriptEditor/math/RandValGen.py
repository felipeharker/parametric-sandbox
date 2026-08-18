"""
Generates a list of random numbers (float or integer) within a specified range.

Inputs:
    count: Integer (Number of random values to generate)
    min_val: Number (Minimum random value)
    max_val: Number (Maximum random value)
    as_int: Boolean (0 = float, 1 = integer)
    seed: Integer (Randomness seed for reproducible results)

Outputs:
    values: List of Numbers (The generated random values)
"""

import random
import os

try:
    ghenv.Component.Name = "RandomValueGenerator"
    ghenv.Component.NickName = "RandValGen"
    ghenv.Component.Description = "Generates a list of random float or integer numbers within a specified range."
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
        "RandValGen.py"
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
