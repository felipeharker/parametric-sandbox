"""
Rounds a list of numbers to the nearest specified step value.

Inputs:
    values: List (The unrounded list of values)
    step: Float (Numeric step for rounding)

Outputs:
    stepped_values: List (The newly rounded values)
"""

try:
    ghenv.Component.Name = "Step Rounding"
    ghenv.Component.NickName = "StepRound"
    ghenv.Component.Description = "Rounds a list of numbers to the nearest value of a given step."
except NameError:
    pass

# Initialize the output list
stepped_values = []

# Execute only if both inputs are provided
if values and step:
    for val in values:
        # Calculate the nearest step multiplier
        raw_rounded = round(val / step) * step
        
        # Clean up floating point precision artifacts (e.g., 0.350000000000001)
        # Rounding to 8 decimal places provides a clean output for Grasshopper
        clean_rounded = round(raw_rounded, 8)
        
        stepped_values.append(clean_rounded)