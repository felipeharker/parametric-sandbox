"""
Pulls geometry from a specified Rhino layer or sublayer.

Inputs:
    layer_name: Text (item access, str)
    pull: Boolean (item access, bool)

Outputs:
    geo: List of Geometry (The geometry pulled from the specified layer)
"""

try:
    ghenv.Component.Name = "PullLayerGeometry"
    ghenv.Component.NickName = "PullLayerGeo"
    ghenv.Component.Description = "Pulls geometry from a specified Rhino layer or sublayer."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Document"
except NameError:
    pass

import Rhino

geo = []

if pull and layer_name:
    doc = Rhino.RhinoDoc.ActiveDoc
    
    # Locate the layer by its full path name (supports "layer::sublayer" formatting)
    layer_index = doc.Layers.FindByFullPath(layer_name, -1)
    
    if layer_index >= 0:
        # Layer exists, retrieve all objects on this specific layer
        rhino_objects = doc.Objects.FindByLayer(layer_name)
        
        if rhino_objects:
            for obj in rhino_objects:
                # Extract and append the base RhinoCommon geometry of each object
                geo.append(obj.Geometry)
    else:
        print("Warning: Layer '{}' was not found in the active document.".format(layer_name))