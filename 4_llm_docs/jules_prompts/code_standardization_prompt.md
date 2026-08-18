When writing or refactoring scripts, ALWAYS use this exact structure for docstrings and `ghenv` metadata configuration:

```python
"""
Creates folded 3-dimensional gridded geometries efficiently from planar cells and fold lines.
Includes an option to output closed solid wedges for each folded fragment.

Inputs:
    grid_cells: List of Curves (list access, closed crv)
    fold_lines: DataTree of Curves (tree access, open crv)
    fold_angle: Number (item access, float)
    solid: Boolean (item access, bool)

Outputs:
    folded_cells: List of Breps (The final 3D folded geometries)
"""

import Rhino.Geometry as rg
import math
import scriptcontext as sc

try:
    ghenv.Component.Name = "GridFoldWedge"
    ghenv.Component.NickName = "GridFWed"
    ghenv.Component.Description = "Creates folded 3-dimensional gridded geometries efficiently."
    ghenv.Component.Category = "CustomLib"  # The main tab in the GH ribbon
    ghenv.Component.SubCategory = "Pattern" # The sub-panel in the ribbon
    ghenv.Component.Message = "Output Solid" # The text bubble below the component
except NameError:
    pass

# --- Script Logic Begins Here ---