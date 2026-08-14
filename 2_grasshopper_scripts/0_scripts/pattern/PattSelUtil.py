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

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "PatternSelectionUtility"
    ghenv.Component.NickName = "PattSelUtil"
    ghenv.Component.Description = "Utility to generate a 7-item boolean toggle list for the PattGen component by allowing users to toggle individual point generators."

    # --- Inputs Metadata ---
    # Index 0: use_centroid
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "use_centroid"
        ghenv.Component.Params.Input[0].NickName = "UseCe"
        ghenv.Component.Params.Input[0].Description = "Boolean (Toggle for Cell Centroid - Point 1)"

    # Index 1: use_outer_mid
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "use_outer_mid"
        ghenv.Component.Params.Input[1].NickName = "UseOu"
        ghenv.Component.Params.Input[1].Description = "Boolean (Toggle for Outer Cell Midpoints - Point 2)"

    # Index 2: use_outer_vert
    if ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.Input[2].Name = "use_outer_vert"
        ghenv.Component.Params.Input[2].NickName = "UseOu"
        ghenv.Component.Params.Input[2].Description = "Boolean (Toggle for Outer Cell Vertices - Point 3)"

    # Index 3: use_outer_eval
    if ghenv.Component.Params.Input.Count > 3:
        ghenv.Component.Params.Input[3].Name = "use_outer_eval"
        ghenv.Component.Params.Input[3].NickName = "UseOu"
        ghenv.Component.Params.Input[3].Description = "Boolean (Toggle for Outer Cell Evaluated Points - Point 4)"

    # Index 4: use_inner_mid
    if ghenv.Component.Params.Input.Count > 4:
        ghenv.Component.Params.Input[4].Name = "use_inner_mid"
        ghenv.Component.Params.Input[4].NickName = "UseIn"
        ghenv.Component.Params.Input[4].Description = "Boolean (Toggle for Inner Cell Midpoints - Point 5)"

    # Index 5: use_inner_vert
    if ghenv.Component.Params.Input.Count > 5:
        ghenv.Component.Params.Input[5].Name = "use_inner_vert"
        ghenv.Component.Params.Input[5].NickName = "UseIn"
        ghenv.Component.Params.Input[5].Description = "Boolean (Toggle for Inner Cell Vertices - Point 6)"

    # Index 6: use_inner_eval
    if ghenv.Component.Params.Input.Count > 6:
        ghenv.Component.Params.Input[6].Name = "use_inner_eval"
        ghenv.Component.Params.Input[6].NickName = "UseIn"
        ghenv.Component.Params.Input[6].Description = "Boolean (Toggle for Inner Cell Evaluated Points - Point 7)"

    # --- Outputs Metadata ---
    # Index 0: point_toggle
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "point_toggle"
        ghenv.Component.Params.Output[0].NickName = "PTog"
        ghenv.Component.Params.Output[0].Description = "List of Booleans (A 7-item list to plug directly into the PattGen component)"

except NameError:
    pass

# Helper function to safely cast inputs to boolean, defaulting to False (0) if no input is wired
def safe_bool(val):
    if val is None:
        return False
    return bool(val)

# Process all 7 inputs
p1 = safe_bool(use_centroid)
p2 = safe_bool(use_outer_mid)
p3 = safe_bool(use_outer_vert)
p4 = safe_bool(use_outer_eval)
p5 = safe_bool(use_inner_mid)
p6 = safe_bool(use_inner_vert)
p7 = safe_bool(use_inner_eval)

# Combine into the ordered 7-item list required by PattGen
point_toggle = [p1, p2, p3, p4, p5, p6, p7]