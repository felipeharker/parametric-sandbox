"""
Remaps the shortest distances between a list of points and multiple attractor points to a new target domain.

Inputs:
    attractors: List of Point3d (The list of attractor points to measure distances from)
    points: List of Point3d (The list of points to calculate distances to the attractors)
    value_a: Number (The start value of the target domain)
    value_b: Number (The end value of the target domain)

Outputs:
    remapped_values: List of Numbers (The remapped distance values)
"""

try:
    ghenv.Component.Name = "ValueRemapMultiplePoints"
    ghenv.Component.NickName = "ValRemapMultiPt"
    ghenv.Component.Description = "Remaps the shortest distances between a list of points and multiple attractor points to a new target domain."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Math"
except NameError:
    pass

remapped_values = []

if attractors and points and value_a is not None and value_b is not None:
    # Calculate the shortest distance from each point to its closest attractor
    closest_distances = []
    
    for pt in points:
        # Calculate distances to all attractors for the current point
        dists_to_attractors = [pt.DistanceTo(attractor) for attractor in attractors]
        
        # Append only the distance to the nearest attractor
        if dists_to_attractors:
            closest_distances.append(min(dists_to_attractors))
    
    if closest_distances:
        min_val = min(closest_distances)
        max_val = max(closest_distances)
        
        orig_domain = max_val - min_val
        target_domain = value_b - value_a
        
        for dist in closest_distances:
            if orig_domain == 0.0:
                remapped_values.append(value_a)
            else:
                mapped_val = value_a + (dist - min_val) * (target_domain / orig_domain)
                remapped_values.append(mapped_val)