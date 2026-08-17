"""
Remaps the distances between a list of points and an attractor point to a new target domain.

Inputs:
    attractor: Point3d (The attractor point to measure distances from)
    points: List of Point3d (The list of points to calculate distances to the attractor)
    value_a: Number (The start value of the target domain)
    value_b: Number (The end value of the target domain)

Outputs:
    remapped_values: List of Numbers (The remapped distance values)
"""

try:
    ghenv.Component.Name = "ValueRemapPoint"
    ghenv.Component.NickName = "ValRemapPt"
    ghenv.Component.Description = "Remaps the distances between a list of points and an attractor point to a new target domain."
except NameError:
    pass

remapped_values = []

if attractor and points and value_a is not None and value_b is not None:
    distances = [pt.DistanceTo(attractor) for pt in points]
    
    if distances:
        min_val = min(distances)
        max_val = max(distances)
        
        orig_domain = max_val - min_val
        target_domain = value_b - value_a
        
        for dist in distances:
            if orig_domain == 0.0:
                remapped_values.append(value_a)
            else:
                mapped_val = value_a + (dist - min_val) * (target_domain / orig_domain)
                remapped_values.append(mapped_val)