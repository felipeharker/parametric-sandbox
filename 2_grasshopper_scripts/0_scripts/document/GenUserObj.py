"""
Programmatically packages a specified Grasshopper component into a custom User Object.

Inputs:
    target_nick: String (The nickname of the canvas node/cluster to package)
    obj_name: String (Display name of the new User Object)
    obj_desc: String (Tooltip description for the new User Object)
    category: String (Ribbon Tab name, e.g., "User")
    sub_category: String (Panel section name within the tab)
    icon_path: String (File path to a .png or bitmap image for the node icon)
    run: Boolean (Set to True to execute the creation)

Outputs:
    UserObject: String (Status message indicating success or failure)
"""

try:
    ghenv.Component.Name = "GenerateUserObj"
    ghenv.Component.NickName = "GenUserObj"
    ghenv.Component.Description = "Programmatically packages a specified Grasshopper component into a custom UserObject."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Document"
except NameError:
    pass

import Grasshopper as gh
import System.Drawing as drawing
import os

def build_user_object(target_nick, name, desc, category, sub_category, icon_path, run):
    if not run:
        return "Set 'run' to True to create User Object."

    # 1. Locate the target component on the active document
    gh_doc = ghenv.Component.OnPingDocument()
    source_obj = None
    
    for obj in gh_doc.Objects:
        if obj.NickName == target_nick:
            source_obj = obj
            break

    if source_obj is None:
        return "Error: Component with nickname '{}' not found.".format(target_nick)

    # 2. Instantiate and set serialized data
    uo = gh.Kernel.GH_UserObject()
    uo.BaseGuid = source_obj.ComponentGuid # Explicitly map the core component ID
    uo.SetDataFromObject(source_obj)

    # 3. Dynamically set Description properties
    # FIX: These Grasshopper API properties must remain capitalized (Category / SubCategory)
    uo.Description.Name = name if name else source_obj.Name
    uo.Description.Description = desc if desc else ""
    uo.Description.Category = category if category else "User"
    uo.Description.SubCategory = sub_category if sub_category else "Custom"

    # 4. Dynamically set Custom Icon if provided
    # By simply omitting an 'else' statement, Grasshopper naturally falls back to its default box icon
    if icon_path and os.path.exists(icon_path):
        try:
            uo.Icon = drawing.Bitmap.FromFile(icon_path)
        except Exception as e:
            return "Failed to load icon: " + str(e)

    # 5. Set Exposure (Visible in primary section of ribbon)
    uo.Exposure = gh.Kernel.GH_Exposure.primary

    # 6. Set Path and Save
    uo.CreateDefaultPath(True)
    attempted_path = uo.Path # Capture the path for debugging
    
    saved_successfully = uo.SaveToFile()
    
    # 7. Clear memory payload
    uo.Clear()

    if saved_successfully:
        return "Successfully created User Object at: " + attempted_path
    else:
        return "Error: Failed to write User Object file. Attempted Path: " + str(attempted_path)

# Assign result to output parameter 'UserObject'
if 'target_nick' in globals() and 'run' in globals():
    UserObject = build_user_object(target_nick, obj_name, obj_desc, category, sub_category, icon_path, run)