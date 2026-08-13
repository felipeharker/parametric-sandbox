"""
Bakes input geometry to a specified layer in Rhino, with options to add or replace existing layer contents.

Inputs:
    geo: Geometry (list access, geometry)
    layer_name: Text (item access, string)
    layer_color: Point3d (item access, Point3d) - X,Y,Z maps to R,G,B (0-255)
    replace: Boolean (item access, bool)
    bake: Boolean (item access, bool)

Outputs:
    (None)
"""

try:
    ghenv.Component.Name = "BakeGeometry"
    ghenv.Component.NickName = "BakeGeo"
    ghenv.Component.Description = "Bakes input geometry to a specified layer in Rhino, with options to add or replace existing layer contents."
except NameError:
    pass

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def bake_geometry_to_layer():
    # Only execute if the bake toggle is True, and we have valid inputs
    if not bake or not geo or not layer_name:
        return

    # Switch scriptcontext to target the active Rhino Document
    sc.doc = Rhino.RhinoDoc.ActiveDoc
    
    try:
        # Check if the layer exists; if not, create it. 
        # rs.AddLayer inherently supports "Parent::Child" syntax
        if not rs.IsLayer(layer_name):
            rs.AddLayer(layer_name)
            
        # If a color is provided, convert X,Y,Z to R,G,B and apply it
        if layer_color is not None:
            # Extract and clamp values between 0 and 255 to prevent errors
            r = max(0, min(255, int(layer_color.X)))
            g = max(0, min(255, int(layer_color.Y)))
            b = max(0, min(255, int(layer_color.Z)))
            rs.LayerColor(layer_name, (r, g, b))
            
        # If replace mode is True (1 = replace)
        if replace:
            existing_objs = rs.ObjectsByLayer(layer_name)
            if existing_objs:
                rs.DeleteObjects(existing_objs)
                
        # Get the layer index to assign to the new geometry attributes
        # FindByFullPath returns the integer index of the layer directly
        layer_index = sc.doc.Layers.FindByFullPath(layer_name, -1)
        
        # Define Rhino object attributes and assign the target layer index
        attr = Rhino.DocObjects.ObjectAttributes()
        attr.LayerIndex = layer_index
        
        # Iterate through the geometry list and add them to the Rhino document
        for item in geo:
            if item:
                sc.doc.Objects.Add(item, attr)
                
        # Redraw the Rhino viewports so baked objects appear instantly
        sc.doc.Views.Redraw()
        
    finally:
        # Crucial step: Always switch scriptcontext back to Grasshopper
        # Put in a finally block to ensure it happens even if an error occurs above
        sc.doc = ghdoc

# Run the function
bake_geometry_to_layer()