"""
Utility to generate Voronoi cells from points evaluated within a list of grid cells.

Inputs:
    grid_cells: List of Geometry (Surfaces, Breps, or Closed Curves)
    boundary: Curve (A single boundary curve to clip the entire Voronoi pattern)
    min_eval: Float (Minimum value to evaluate reparameterized surface, between 0 and 1)
    max_eval: Float (Maximum value to evaluate reparameterized surface, between 0 and 1)
    seed: Integer (Seed for random value generation)

Outputs:
    voronoi_cells: List of Curves (The generated Voronoi cells based on the evaluated points)
"""

import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import random
import os

try:
    ghenv.Component.Name = "VoronoiGrid"
    ghenv.Component.NickName = "VoroGrid"
    ghenv.Component.Description = "Generates Voronoi cells by randomly evaluating normalized coordinates within a set of grid surfaces."
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
        "VoroGrid.py"
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
