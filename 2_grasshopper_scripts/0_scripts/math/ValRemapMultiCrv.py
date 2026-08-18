"""
Remaps the shortest distances between a list of points and multiple attractor curves to a new target domain.

Inputs:
    curves: List of Curve (The attractor curves to measure distances from)
    points: List of Point3d (The list of points to calculate distances to the curves)
    value_a: Number (The start value of the target domain)
    value_b: Number (The end value of the target domain)

Outputs:
    remapped_values: List of Numbers (The remapped distance values)
"""

try:
    ghenv.Component.Name = "ValueRemapMultipleCurves"
    ghenv.Component.NickName = "ValRemapMultiCrv"
    ghenv.Component.Description = "Remaps the shortest distances between a list of points and multiple attractor curves to a new target domain."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Math"
except NameError:
    pass

remapped_values = []

if curves and points and value_a is not None and value_b is not None:
    distances = []
    
    for pt in points:
        # Store the closest distances to all valid curves for the current point
        closest_dists_for_pt = []
        
        for crv in curves:
            if crv:
                # Calculate the closest point on the current curve to the test point
                success, t = crv.ClosestPoint(pt)
                if success:
                    closest_pt = crv.PointAt(t)
                    closest_dists_for_pt.append(pt.DistanceTo(closest_pt))
        
        # Append the absolute minimum distance found among all curves
        if closest_dists_for_pt:
            distances.append(min(closest_dists_for_pt))
        else:
            # Fallback to maintain list length if calculation fails for all curves
            distances.append(None)
            
    valid_distances = [d for d in distances if d is not None]
    
    if valid_distances:
        min_val = min(valid_distances)
        max_val = max(valid_distances)
        
        orig_domain = max_val - min_val
        target_domain = value_b - value_a
        
        for dist in distances:
            if dist is None:
                remapped_values.append(None)
            elif orig_domain == 0.0:
                remapped_values.append(value_a)
            else:
                mapped_val = value_a + (dist - min_val) * (target_domain / orig_domain)
                remapped_values.append(mapped_val)