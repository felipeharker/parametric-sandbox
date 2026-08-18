"""
Exports Grasshopper top-level inputs to a CSV file.

Inputs:
    export: Boolean (item access, bool)
    csv_file: String (item access, str)

Outputs:
    (None)
"""

try:
    ghenv.Component.Name = "ParamExporter"
    ghenv.Component.NickName = "ParamExp"
    ghenv.Component.Description = "Exports Grasshopper top-level inputs to a CSV file."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Document"
    ghenv.Component.Message = ""
except NameError:
    pass

import os
import csv
import Grasshopper as gh

def get_gh_doc():
    if 'ghenv' in globals():
        return ghenv.Component.OnPingDocument()
    if 'ghdoc' in globals():
        return ghdoc
    return None

def is_top_level(obj):
    if not isinstance(obj, gh.Kernel.IGH_Param):
        return True
    return obj.SourceCount == 0

def has_custom_nickname(obj):
    default_names = ['Number Slider', 'Boolean Toggle', 'Panel']
    if isinstance(obj, gh.Kernel.IGH_Param):
        if obj.NickName == obj.Name:
            return False
    if obj.NickName in default_names:
        return False
    if not obj.NickName or obj.NickName.strip() == "":
        return False
    return True

def get_param_type_str(obj):
    type_map = {
        'Number': 'float',
        'Integer': 'int',
        'String': 'string',
        'Text': 'string',
        'Boolean': 'bool',
        'Curve': 'crv',
        'Point': 'pt',
        'Geometry': 'geo',
        'Brep': 'brep',
        'Surface': 'srf'
    }

    if isinstance(obj, gh.Kernel.IGH_Param):
        type_name = obj.TypeName
        if type_name in type_map:
            return type_map[type_name]
        return type_name.lower()

    if isinstance(obj, gh.Kernel.Special.GH_NumberSlider):
        return "float" if obj.Slider.Type == gh.GUI.Base.GH_SliderAccuracy.Float else "int"
    if isinstance(obj, gh.Kernel.Special.GH_BooleanToggle):
        return "bool"
    if isinstance(obj, gh.Kernel.Special.GH_Panel):
        return "string"

    return "geo"

def extract_value(obj, type_str):
    if type_str in ['crv', 'pt', 'geo', 'brep', 'srf']:
        return obj.NickName

    if isinstance(obj, gh.Kernel.Special.GH_NumberSlider):
        return str(obj.CurrentValue)
    elif isinstance(obj, gh.Kernel.Special.GH_BooleanToggle):
        return str(obj.Value)
    elif isinstance(obj, gh.Kernel.Special.GH_Panel):
        return str(obj.UserText)

    if isinstance(obj, gh.Kernel.IGH_Param):
        if obj.VolatileDataCount > 0:
            first_branch = obj.VolatileData.Branches[0]
            if first_branch.Count > 0:
                if hasattr(first_branch[0], 'Value'):
                    return str(first_branch[0].Value)
                else:
                    return str(first_branch[0])
        elif not obj.PersistentData.IsEmpty:
            first_branch = obj.PersistentData.Branches[0]
            if first_branch.Count > 0:
                if hasattr(first_branch[0], 'Value'):
                    return str(first_branch[0].Value)
                else:
                    return str(first_branch[0])

    return ""

def main():
    if 'export' not in globals() or not export:
        return

    if 'csv_file' not in globals() or not csv_file:
        print("Invalid CSV file path or csv_file input not provided")
        return

    doc = get_gh_doc()
    if not doc:
        print("Could not find Grasshopper document context")
        return

    export_data = []
    export_data.append(["item name", "type", "value"])

    for obj in doc.Objects:
        is_param = isinstance(obj, gh.Kernel.IGH_Param)
        is_special = isinstance(obj, (gh.Kernel.Special.GH_NumberSlider, gh.Kernel.Special.GH_BooleanToggle, gh.Kernel.Special.GH_Panel))

        if is_param or is_special:
            if is_top_level(obj) and has_custom_nickname(obj):
                type_str = get_param_type_str(obj)
                val_str = extract_value(obj, type_str)

                name_str = obj.NickName

                if type_str in ['crv', 'pt', 'geo', 'brep', 'srf']:
                    name_str = "{}-1".format(name_str)

                export_data.append([name_str, type_str, val_str])

    if len(export_data) <= 1:
        print("No eligible components found to export.")
        return

    try:
        dir_name = os.path.dirname(csv_file)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(export_data)

        print("Successfully exported {} parameters to {}.".format(len(export_data) - 1, csv_file))
    except Exception as e:
        print("Error writing to CSV: {}".format(e))

if __name__ == "__main__":
    main()
