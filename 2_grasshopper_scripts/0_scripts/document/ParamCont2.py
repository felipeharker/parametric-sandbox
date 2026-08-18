"""
Updates Grasshopper parameters from a CSV file, with optional section filtering.

Inputs:
    update: Boolean (item access, bool)
    csv_file: String (item access, str)
    section: String (item access, str) [Optional]

Outputs:
    (None)
"""

try:
    ghenv.Component.Name = "ParamController2"
    ghenv.Component.NickName = "ParamCont2"
    ghenv.Component.Description = "Updates Grasshopper parameters from a CSV file, with optional section filtering."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Document"
    ghenv.Component.Message = ""
except NameError:
    pass

import os
import csv
import Grasshopper as gh
import System

def get_gh_doc():
    if 'ghenv' in globals():
        return ghenv.Component.OnPingDocument()
    if 'ghdoc' in globals():
        return ghdoc
    return None

def find_param_by_nickname(doc, nickname):
    matched_params = []
    for obj in doc.Objects:
        if isinstance(obj, gh.Kernel.IGH_Param):
            if obj.NickName == nickname:
                matched_params.append(obj)
    return matched_params

def update_param_value(param, type_str, value_str, doc):
    type_str = type_str.lower().strip()
    value_str = value_str.strip()

    if type_str in ['float', 'num', 'number', 'double']:
        try:
            val = float(value_str)
            param.PersistentData.Clear()
            param.PersistentData.Append(gh.Kernel.Types.GH_Number(val))
            return True
        except ValueError:
            print("Error parsing {} as float".format(value_str))

    elif type_str in ['int', 'integer']:
        try:
            val = int(value_str)
            param.PersistentData.Clear()
            param.PersistentData.Append(gh.Kernel.Types.GH_Integer(val))
            return True
        except ValueError:
            print("Error parsing {} as int".format(value_str))

    elif type_str in ['string', 'str', 'text']:
        param.PersistentData.Clear()
        param.PersistentData.Append(gh.Kernel.Types.GH_String(value_str))
        return True

    elif type_str in ['bool', 'boolean']:
        val = value_str.lower() in ['true', '1', 't', 'yes', 'y']
        param.PersistentData.Clear()
        param.PersistentData.Append(gh.Kernel.Types.GH_Boolean(val))
        return True

    elif type_str in ['crv', 'curve', 'pt', 'point', 'geo', 'geometry', 'brep', 'srf', 'surface']:
        source_params = find_param_by_nickname(doc, value_str)
        if not source_params:
            print("Could not find source parameter with nickname '{}' on canvas".format(value_str))
            return False

        source_param = source_params[0]
        param.RemoveAllSources()
        param.AddSource(source_param)
        return True

    else:
        print("Unsupported type: {}".format(type_str))
        return False

PENDING_UPDATES = []

def schedule_callback(ghdoc):
    global PENDING_UPDATES

    if not PENDING_UPDATES:
        return

    updated_count = 0
    for param, type_str, value_str in PENDING_UPDATES:
        param.RecordUndoEvent("CSV Update")
        if update_param_value(param, type_str, value_str, ghdoc):
            param.ExpireSolution(False)
            updated_count += 1

    PENDING_UPDATES = []

    if updated_count > 0:
        print("Successfully updated {} parameters.".format(updated_count))
        ghdoc.NewSolution(False)

def main():
    global PENDING_UPDATES
    if 'update' not in globals() or not update:
        return

    if 'csv_file' not in globals() or not csv_file or not os.path.exists(csv_file):
        print("Invalid CSV file path or csv_file input not provided")
        return

    active_section = None
    if 'section' in globals() and section:
        active_section = str(section).strip()

    doc = get_gh_doc()
    if not doc:
        print("Could not find Grasshopper document context")
        return

    updated_count = 0

    with open(csv_file, mode='r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            headers = None

        if not headers:
            print("Empty CSV file")
            return

        header_lower = [h.lower().strip() for h in headers]

        try:
            name_idx = header_lower.index("input name")
            type_idx = header_lower.index("type")
            value_idx = header_lower.index("value")
        except ValueError:
            print("Warning: Could not find exact headers 'input name', 'type', 'value'. Assuming columns 0, 1, 2.")
            name_idx, type_idx, value_idx = 0, 1, 2
            
        try:
            section_idx = header_lower.index("section")
        except ValueError:
            section_idx = 3 if len(headers) > 3 else -1

        PENDING_UPDATES = []
        for row in reader:
            if len(row) <= max(name_idx, type_idx, value_idx):
                continue

            input_name = row[name_idx]
            input_type = row[type_idx]
            input_value = row[value_idx]
            
            row_section = None
            if section_idx != -1 and len(row) > section_idx:
                row_section = row[section_idx].strip()

            if active_section is not None:
                if not row_section or row_section != active_section:
                    continue

            target_params = find_param_by_nickname(doc, input_name)
            if not target_params:
                print("Warning: No parameter found with NickName '{}'".format(input_name))
                continue

            for param in target_params:
                PENDING_UPDATES.append((param, input_type, input_value))
                updated_count += 1

    if updated_count > 0:
        delegate = gh.Kernel.GH_Document.GH_ScheduleDelegate(schedule_callback)
        doc.ScheduleSolution(5, delegate)

if __name__ == "__main__":
    main()
