"""
Generates a custom Voronoi pattern within grid cells based on scaled inner boundaries and evaluated curve points.
HIGH PERFORMANCE: Utilizes System.Threading.Tasks for concurrent multi-core processing.

Inputs:
    grid_cells: List of Curves (Base grid cells to reference as boundaries)
    inner_scale: Float (Scale factor between 0.0 and 1.0 for the inner cell)
    eval_outer: Float (Evaluation parameter between 0.0 and 1.0 for outer cell edges)
    eval_inner: Float (Evaluation parameter between 0.0 and 1.0 for inner cell edges)
    point_toggle: List of Booleans (7-item list of 0s and 1s activating specific generator points)

Outputs:
    pattern_curves: DataTree of Curves (The final generated Voronoi pattern curves, organized by grid cell)
"""

import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import ghpythonlib.treehelpers as th
import System.Threading.Tasks as tasks # The key to multi-threading
import os

try:
    ghenv.Component.Name = "VoronoiPatternGenerator"
    ghenv.Component.NickName = "VoroPattGen"
    ghenv.Component.Description = "Generates a custom Voronoi pattern utilizing parallel multi-threading for maximum speed."
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
        "VoroPattGen.py"
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
