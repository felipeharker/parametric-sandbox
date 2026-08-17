"""
Remaps the shortest distances between a list of points and an attractor curve to a new target domain.

Inputs:
    curve: Curve (The attractor curve to measure distances from)
    points: List of Point3d (The list of points to calculate distances to the curve)
    value_a: Number (The start value of the target domain)
    value_b: Number (The end value of the target domain)

Outputs:
    remapped_values: List of Numbers (The remapped distance values)
"""

try:
    ghenv.Component.Name = "ValueRemapCurve"
    ghenv.Component.NickName = "ValRemapCrv"
    ghenv.Component.Description = "Remaps the shortest distances between a list of points and an attractor curve to a new target domain."
except NameError:
    pass

remapped_values = []

if curve and points and value_a is not None and value_b is not None:
    distances = []
    
    for pt in points:
        # Calculate the closest point on the curve to the current test point
        success, t = curve.ClosestPoint(pt)
        if success:
            closest_pt = curve.PointAt(t)
            distances.append(pt.DistanceTo(closest_pt))
        else:
            # Fallback to maintain list length if calculation fails for a specific point
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