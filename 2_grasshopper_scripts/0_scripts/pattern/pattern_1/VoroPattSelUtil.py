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
    ghenv.Component.Name = "VoronoiPatternSelectionUtility"
    ghenv.Component.NickName = "VoroPattSelUtil"
    ghenv.Component.Description = "Utility to generate a 7-item boolean toggle list for the PattGen component by allowing users to toggle individual point generators."
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