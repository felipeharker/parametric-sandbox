# CODE STANDARDIZATION

## INSTRUCTIONS

I am using the ScriptEditor tool to create a single packaged .gha (or equivalent) plugin file.

**Objectives**

I would like to make it so that the grasshopper component is merely a shell for the code which exists outside of it in a repo/codebase.

please create a subdirectory called "ScriptEditor" which contains the shells for EACH of the scripts present in the codebase currently. Ensure that the passthrough/bridge script is written properly, and that I am able to simply:

1. create the component shell in grasshopper with its inputs/outputs and ghenvs.
2. create a project and compile using ScriptEditor
3. manage the codebase from the external repo through an IDE and have it automatically update in grasshopper (from the linking/bridge script)
4. from my understanding the only time grasshopper must be accessed for changes is when there is a change to the actual UI, like inputs/outputs, names, typehints, etc. let's focus on ensuring that.

Use the standard code block below to edit the entire script library to adhere to this standard strictly.

## STANDARD CODE BLOCK

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

// --- Script Logic Begins Here --- //