# Script Library Documentation

## 1. Document Management
Scripts designed to interact with the Rhino/Grasshopper document environment, layers, and file systems.

### `BakeGeo.py`
*   **Description:** Bakes input geometry to a specified layer in Rhino, featuring options to add or replace existing layer contents[cite: 1].
*   **Inputs:**
    *   `geo`: The geometry to bake, accessed as a list[cite: 1].
    *   `layer_name`: A string representing the target layer name[cite: 1].
    *   `layer_color`: A Point3d coordinate where X, Y, and Z values map to R, G, B colors (0-255)[cite: 1].
    *   `replace`: A boolean toggle to replace existing layer contents[cite: 1].
    *   `bake`: A boolean toggle to execute the script[cite: 1].
*   **Outputs:** None[cite: 1].
*   **Logic:** The script points the scriptcontext to the active Rhino document and checks if the specified layer exists, creating it if it does not[cite: 1]. It converts the X, Y, Z point coordinates into clamped RGB integers and applies the color to the layer[cite: 1]. If the replace toggle is true, it deletes existing objects on that layer[cite: 1]. Finally, it assigns the geometry to the layer's index, adds it to the document, redraws the viewports, and switches the scriptcontext back to Grasshopper[cite: 1].

### `DirFile.py`
*   **Description:** Lists the files contained within a specified directory[cite: 1].
*   **Inputs:**
    *   `directory`: A string representing the directory path[cite: 1].
*   **Outputs:**
    *   `file_name`: A list of strings containing the names of the files in the directory[cite: 1].
*   **Logic:** The script utilizes the `os.listdir()` function to return all files within the provided directory path, returning an empty list if the directory is missing[cite: 1].

### `GenUserObj.py`
*   **Description:** Programmatically packages a specified Grasshopper component or cluster into a custom User Object[cite: 1].
*   **Inputs:**
    *   `target_nick`: The nickname string of the canvas node to package[cite: 1].
    *   `obj_name`: The display name string for the new User Object[cite: 1].
    *   `obj_desc`: The tooltip description string[cite: 1].
    *   `category`: The ribbon tab name string[cite: 1].
    *   `sub_category`: The panel section name string within the tab[cite: 1].
    *   `icon_path`: The file path string to a `.png` or bitmap image[cite: 1].
    *   `run`: A boolean toggle to execute the creation[cite: 1].
*   **Outputs:**
    *   `UserObject`: A status string indicating success or failure[cite: 1].
*   **Logic:** The script searches the active Grasshopper document for an object matching the target nickname[cite: 1]. Once found, it instantiates a `GH_UserObject`, maps the component's Core Guid, and dynamically sets the name, description, category, and subcategory properties[cite: 1]. It attempts to load the custom image icon, falls back to the default icon if none is provided, sets the ribbon exposure to primary, and saves the object to the default User Object folder[cite: 1].

### `ParamCont1.py`
*   **Description:** Updates Grasshopper parameters directly from a CSV file[cite: 1].
*   **Inputs:**
    *   `update`: A boolean toggle to run the update[cite: 1].
    *   `csv_file`: A string representing the CSV file path[cite: 1].
*   **Outputs:** None[cite: 1].
*   **Logic:** The script reads a CSV file to locate "input name", "type", and "value" columns[cite: 1]. It searches the canvas for parameters matching the nicknames in the CSV and parses the string values into their correct Grasshopper data types (e.g., float, integer, boolean, string)[cite: 1]. For geometry types, it dynamically rewires the parameter's source[cite: 1]. It safely applies these changes and redraws the canvas using `GH_ScheduleDelegate` to avoid threading lockups[cite: 1].

### `ParamCont2.py`
*   **Description:** Updates Grasshopper parameters from a CSV file with an added section filtering feature[cite: 1].
*   **Inputs:**
    *   `update`: A boolean toggle to run the update[cite: 1].
    *   `csv_file`: A string representing the CSV file path[cite: 1].
    *   `section`: An optional string to filter which updates apply[cite: 1].
*   **Outputs:** None[cite: 1].
*   **Logic:** Incorporates the exact same core logic and parsing as `ParamCont1.py`, but includes a filtering mechanism[cite: 1]. It searches for a "section" column in the CSV and only schedules updates for rows where the section matches the user's active section input[cite: 1].

### `ParamExp.py`
*   **Description:** Exports top-level Grasshopper inputs to a CSV file[cite: 1].
*   **Inputs:**
    *   `export`: A boolean toggle to execute the export[cite: 1].
    *   `csv_file`: A string representing the destination CSV file path[cite: 1].
*   **Outputs:** None[cite: 1].
*   **Logic:** The script iterates through the Grasshopper document looking for `IGH_Param` objects, Number Sliders, Boolean Toggles, and Panels[cite: 1]. It filters for "top-level" objects (meaning they have 0 incoming wire sources) that have custom user-defined nicknames[cite: 1]. It then extracts their current data values and writes a formatted list of names, types, and values to the specified CSV path[cite: 1].

### `PullLayerGeo.py`
*   **Description:** Pulls geometry directly from a specified Rhino layer or sublayer[cite: 1].
*   **Inputs:**
    *   `layer_name`: A string representing the target layer[cite: 1].
    *   `pull`: A boolean toggle to execute the function[cite: 1].
*   **Outputs:**
    *   `geo`: A list of geometry pulled from the specified layer[cite: 1].
*   **Logic:** The script searches the active Rhino document for a layer by its full path[cite: 1]. If the layer exists, it retrieves all Rhino objects assigned to that layer, extracts their base RhinoCommon geometry, and outputs the list[cite: 1].

---

## 2. Fabrication
Scripts for generating parametric folds and attachment tabs for sheet metal and architectural panel systems.

### `CustPanTab.py`
*   **Description:** Creates fold areas and tabs for a panel system utilizing a custom user-defined tab geometry[cite: 1].
*   **Inputs:**
    *   `boundary`: A curve representing the panel face[cite: 1].
    *   `fold_width`: A float for the width of the fold[cite: 1].
    *   `tab_geo`: A custom curve representing the tab profile[cite: 1].
    *   `tab_spacing`: A float defining the spacing between tabs[cite: 1].
*   **Outputs:**
    *   `panel_face`: The original panel rectangle[cite: 1].
    *   `fold`: A list containing the left and right fold curves[cite: 1].
    *   `tabs`: A list of the mapped custom tab curves[cite: 1].
*   **Logic:** Calculates the bounding box of the base plane to generate left and right rectangular fold extensions[cite: 1]. It calculates the number of required tabs based on the panel height and tab spacing, finds their center points, and uses `rg.Transform.PlaneToPlane` to orient and mirror the custom tab geometry onto both the left and right outer fold edges[cite: 1].

### `FrameTabSys.py`
*   **Description:** Creates parametric tab perforations within a frame boundary[cite: 1].
*   **Inputs:**
    *   `boundary`: A curve representing the frame[cite: 1].
    *   `tab_height`: A float for the height of the tab opening[cite: 1].
    *   `tab_width`: A float for the width of the tab opening[cite: 1].
    *   `tab_space_x`: A float for horizontal spacing[cite: 1].
    *   `tab_space_y`: A float for vertical spacing[cite: 1].
*   **Outputs:**
    *   `frame_face`: The original rectangular frame curve[cite: 1].
    *   `tabs`: A list of curves representing the new tab openings[cite: 1].
*   **Logic:** Calculates the bounding box of the frame to determine height and midpoint[cite: 1]. It determines the number of tabs needed vertically, calculates their Y-axis centers, and offsets them by the defined X-axis spacing to generate pairs of rectangular perforations along the frame[cite: 1].

### `PanTabSys.py`
*   **Description:** Creates standard fold areas and rectangular tabs for an aluminum panel system[cite: 1].
*   **Inputs:**
    *   `boundary`: A curve representing the panel face[cite: 1].
    *   `fold_width`: A float for the width of the fold[cite: 1].
    *   `tab_width`: A float for the width of the tab[cite: 1].
    *   `tab_height`: A float for the height of the tab[cite: 1].
    *   `tab_spacing`: A float defining the spacing between tabs[cite: 1].
*   **Outputs:**
    *   `panel_face`: The original panel face curve[cite: 1].
    *   `fold`: A list containing the left and right fold curves[cite: 1].
    *   `tabs`: A list of the rectangular tab curves[cite: 1].
*   **Logic:** Functions identically to `CustPanTab.py` by generating fold areas and center points, but generates standard rectangular cutouts for the tabs instead of mapping custom geometry[cite: 1].

---

## 3. Folding
Scripts optimized for manipulating, folding, and unrolling 3D planar geometries.

### `GridFPlan.py`
*   **Description:** Creates folded 3D gridded geometries efficiently from planar cells and fold lines[cite: 1].
*   **Inputs:**
    *   `grid_cells`: A list of closed curves representing cells[cite: 1].
    *   `fold_lines`: A DataTree of open curves representing fold lines[cite: 1].
    *   `fold_angle`: A float representing the fold angle in degrees[cite: 1].
*   **Outputs:**
    *   `folded_cells`: A list of final 3D folded Breps[cite: 1].
*   **Logic:** Optimizes performance by checking if the DataTree structure matches the cell list, allowing O(1) index matching over slower spatial containment checks[cite: 1]. It converts planar cells into Breps, splits them with the fold lines, and finds the bounding hinge edge[cite: 1]. It calculates an arithmetic average for the face center and uses a cross product vector to guarantee the panels fold uniformly "up" before applying a mathematical rotation transform[cite: 1].

### `GridFPyra.py`
*   **Description:** Folds gridded cells into either open panels or solid 3D pyramids[cite: 1].
*   **Inputs:**
    *   `grid_cells`: A list of closed curves representing cells[cite: 1].
    *   `fold_lines`: A DataTree of open curves representing fold lines[cite: 1].
    *   `fold_angle`: A float representing the fold angle[cite: 1].
    *   `solid`: A boolean toggle to output closed pyramids[cite: 1].
*   **Outputs:**
    *   `folded_cells`: A list of final 3D folded Breps[cite: 1].
*   **Logic:** Features two modes. If `solid` is true, it bypasses the split logic entirely, computes the centroid of the cell, uses trigonometry to calculate an apex point based on the angle and distance to the edge, and builds solid surfaces between the cell edges and the apex to join into a closed Brep[cite: 1]. If `solid` is false, it executes the same open-panel cross-product rotation logic as `GridFPlan.py`[cite: 1].

### `GridFWed.py`
*   **Description:** Folds gridded cells into open panels or solid wedges[cite: 1].
*   **Inputs:**
    *   `grid_cells`: A list of closed curves representing cells[cite: 1].
    *   `fold_lines`: A DataTree of open curves representing fold lines[cite: 1].
    *   `fold_angle`: A float representing the fold angle[cite: 1].
    *   `solid`: A boolean toggle to output closed wedges[cite: 1].
*   **Outputs:**
    *   `folded_cells`: A list of final 3D folded Breps[cite: 1].
*   **Logic:** Runs the cell splitting and rotation transform logic identical to `GridFPlan.py`[cite: 1]. However, if `solid` is true, it keeps a duplicate of the original flat face, compares the moved edges of the rotated face against the flat face, and generates ruled surfaces between them to join into a watertight closed solid wedge[cite: 1].

### `GridUnf.py`
*   **Description:** Unrolls 3D folded geometries into 2D cut and fold linework for fabrication[cite: 1].
*   **Inputs:**
    *   `grid_cells`: A list of folded 3D Breps, faces, or solids[cite: 1].
    *   `spacing`: A float defining the array spacing distance[cite: 1].
*   **Outputs:**
    *   `cut_lines`: A DataTree of curves representing outer boundaries[cite: 1].
    *   `fold_lines`: A DataTree of curves representing internal hinges[cite: 1].
*   **Logic:** The script attempts to join all touching Breps into single polysurfaces before passing them to the `rg.Unroller`[cite: 1]. It takes the flattened outputs, aligns them to the World XY origin, and arrays them linearly along the X-axis using bounding box widths and the input spacing value[cite: 1]. Finally, it sorts the edges based on valence: assigning naked edges to `cut_lines` and interior edges to `fold_lines`[cite: 1].

---

## 4. Geometry
Scripts for bounding, calculating, and manipulating general geometry.

### `BndTrim.py`
*   **Description:** Trims curves against a boundary region, closing them along the boundary if they were originally closed[cite: 1].
*   **Inputs:**
    *   `curves`: A list of curves to be trimmed[cite: 1].
    *   `region`: A closed curve serving as the boundary[cite: 1].
*   **Outputs:**
    *   `trimmed_curves`: A list of trimmed and processed curves[cite: 1].
*   **Logic:** Evaluates each curve individually[cite: 1]. If the input curve is closed, it executes a Boolean Intersection[cite: 1]. If the curve is open, it executes a Curve-Curve intersection, splits the curve at the intersection parameters, and runs a mathematical point-containment check on the midpoints of the split fragments, discarding any segments that fall outside the boundary[cite: 1].

### `GeoBnd2D.py`
*   **Description:** Draws a boundary rectangle around a geometry aligned to a user-defined plane[cite: 1].
*   **Inputs:**
    *   `geo`: The input geometry[cite: 1].
    *   `plane`: A plane to align the bounding box to[cite: 1].
*   **Outputs:**
    *   `bnd_rect`: A curve representing the bounding rectangle[cite: 1].
    *   `x`: A numeric dimension of the first axis[cite: 1].
    *   `y`: A numeric dimension of the second axis[cite: 1].
*   **Logic:** Calculates the bounding box of the geometry oriented specifically to the local coordinates of the input plane[cite: 1]. It creates intervals from the minimum and maximum coordinates to output a 2D rectangle and its lengths[cite: 1].

### `GeoBnd3D.py`
*   **Description:** Draws a standard world-aligned 3D boundary box around a geometry[cite: 1].
*   **Inputs:**
    *   `geo`: The input geometry[cite: 1].
*   **Outputs:**
    *   `bnd_box`: The 3D bounding box geometry[cite: 1].
    *   `x`, `y`, `z`: The numeric dimensions of the box[cite: 1].
*   **Logic:** Calculates the bounding box of the geometry aligned strictly to the World Plane, converting the result into an `rg.Box` and deriving the X, Y, and Z dimensional lengths[cite: 1].

---

## 5. Grid
Scripts for generating densely packed 2D geometric patterns and cellular grids.

### `BndBrickG.py`
*   **Description:** Creates a brick grid of individual closed rectangular cells[cite: 1].
*   **Inputs:**
    *   `boundary`: A region boundary curve[cite: 1].
    *   `size_x`: A float for cell width[cite: 1].
    *   `size_y`: A float for cell height[cite: 1].
    *   `cell_shift`: A float for the shift amount[cite: 1].
*   **Outputs:**
    *   `rectgrid`: A list of individual cell curves[cite: 1].
    *   `bnd_rect`: The bounding rectangle of the original input[cite: 1].
*   **Logic:** Generates rows and columns of polylines based on the bounding box of the input curve[cite: 1]. It applies the `cell_shift` value specifically to odd rows to create an offset brick-laying effect, ensuring shifted cells are culled if they fall outside the bounding box parameters[cite: 1].

### `BndDiaG.py`
*   **Description:** Creates a grid of individual closed diamond cells[cite: 1].
*   **Inputs:**
    *   `boundary`: A region boundary curve[cite: 1].
    *   `size_x`: A float for grid width[cite: 1].
    *   `size_y`: A float for grid height[cite: 1].
*   **Outputs:**
    *   `diagrid`: A list of individual diamond cell curves[cite: 1].
    *   `bnd_rect`: The bounding rectangle[cite: 1].
*   **Logic:** Generates point grids based on the bounding box, offsetting the X-coordinates of every other row by half the X-size[cite: 1]. It draws continuous 4-sided polylines connecting these offset centers to create diamond patterns[cite: 1].

### `BndHexG.py`
*   **Description:** Creates a grid of closed hexagonal cells[cite: 1].
*   **Inputs:**
    *   `boundary`: A region boundary curve[cite: 1].
    *   `size_x`: A float for hex width[cite: 1].
    *   `size_y`: A float for hex height[cite: 1].
*   **Outputs:**
    *   `hexgrid`: A list of hexagonal cell curves[cite: 1].
    *   `bnd_rect`: The bounding rectangle[cite: 1].
*   **Logic:** Multiplies the row heights by 0.75 and offsets the columns of alternating rows to align the hexagon centers[cite: 1]. It uses trigonometry (sine and cosine functions at 60-degree increments) to construct 6-sided polylines around each centerpoint[cite: 1].

### `BndPan.py`
*   **Description:** Creates a grid of rectangular panels that perfectly fit within a bounding curve without overhangs[cite: 1].
*   **Inputs:**
    *   `boundary`: A region boundary curve[cite: 1].
    *   `size_x`: A float for target panel width[cite: 1].
    *   `size_y`: A float for target panel height[cite: 1].
    *   `use_world_xy`: A boolean to force World XY plane alignment[cite: 1].
*   **Outputs:**
    *   `panels`: A list of rectangular curves[cite: 1].
*   **Logic:** Calculates the bounding box on the local plane (or World XY)[cite: 1]. It algorithmically divides the total length by the target cell size, determining the remaining dimensions, and generates custom-sized edge panels to absorb any remainders symmetrically[cite: 1].

### `BndRectG.py`
*   **Description:** Creates a standard grid of closed rectangular cells[cite: 1].
*   **Inputs:**
    *   `boundary`: A region boundary curve[cite: 1].
    *   `size_x`: A float for cell width[cite: 1].
    *   `size_y`: A float for cell height[cite: 1].
*   **Outputs:**
    *   `rectgrid`: A list of cell curves[cite: 1].
    *   `bnd_rect`: The bounding rectangle[cite: 1].
*   **Logic:** Creates a strict orthogonal array of 4-sided polylines mapped to the bounding box divisions derived from the user sizing inputs[cite: 1].

### `BndTriG.py`
*   **Description:** Creates a grid of closed triangular cells[cite: 1].
*   **Inputs:**
    *   `boundary`: A region boundary curve[cite: 1].
    *   `size_x`: A float for cell width[cite: 1].
    *   `size_y`: A float for cell height[cite: 1].
*   **Outputs:**
    *   `trigrid`: A list of triangular cell curves[cite: 1].
    *   `bnd_rect`: The bounding rectangle[cite: 1].
*   **Logic:** Generates an orthogonal grid of rectangles and splits each one in half with a diagonal polyline[cite: 1]. It alternates the split direction (from bottom-left/top-right to top-left/bottom-right) based on whether the row+column index is even or odd, creating a continuous structural diagrid[cite: 1].

---

## 6. Math
Scripts to calculate data, calculate remapping domains, and analyze image information.

### `ImgHue.py`
*   **Description:** Calculates the luminance values of an image at specified physical point coordinates[cite: 1].
*   **Inputs:**
    *   `image_path`: A string representing the image file path[cite: 1].
    *   `points`: A list of Point3d objects[cite: 1].
*   **Outputs:**
    *   `values`: A list of numerical luminance values[cite: 1].
*   **Logic:** Loads an image via `System.Drawing.Bitmap` and normalizes the X and Y bounds of the point list to the width and height of the image pixels[cite: 1]. It reads the color at each corresponding pixel and uses the standard formula `(0.299*R + 0.587*G + 0.114*B) / 255.0` to return a relative luminance value between 0 and 1[cite: 1].

### `RandValGen.py`
*   **Description:** Generates a list of random float or integer numbers[cite: 1].
*   **Inputs:**
    *   `count`: The integer number of values to generate[cite: 1].
    *   `min_val`: The minimum value boundary[cite: 1].
    *   `max_val`: The maximum value boundary[cite: 1].
    *   `as_int`: A boolean toggle (True for integers, False for floats)[cite: 1].
    *   `seed`: An integer for random seed reproducibility[cite: 1].
*   **Outputs:**
    *   `values`: The list of generated numbers[cite: 1].
*   **Logic:** Imports the Python `random` module, applies the seed if provided, and loops through the count to output either `random.randint` or `random.uniform` values depending on the integer toggle[cite: 1].

### `StepRound.py`
*   **Description:** Rounds a list of numbers to the nearest specified step value[cite: 1].
*   **Inputs:**
    *   `values`: A list of raw numerical values[cite: 1].
    *   `step`: A float representing the numeric step size[cite: 1].
*   **Outputs:**
    *   `stepped_values`: A list of the rounded numbers[cite: 1].
*   **Logic:** Divides each value by the step, rounds it to the nearest whole number, and multiplies it back by the step[cite: 1]. It applies a final 8-decimal-place rounding pass to remove floating-point precision artifacts common in Python math[cite: 1].

### `ValRemap.py`
*   **Description:** Remaps a list of values to a new target domain[cite: 1].
*   **Inputs:**
    *   `values`: A list of numbers[cite: 1].
    *   `value_a`: The start of the target domain[cite: 1].
    *   `value_b`: The end of the target domain[cite: 1].
*   **Outputs:**
    *   `remapped_values`: The list of mathematically mapped numbers[cite: 1].
*   **Logic:** Extracts the min and max from the incoming list to establish the original domain, and uses linear interpolation to map the position of each value proportionally into the new target domain span[cite: 1].

### `ValRemapCrv.py`
*   **Description:** Remaps the shortest distance between a list of points and an attractor curve into a new domain[cite: 1].
*   **Inputs:**
    *   `curve`: The attractor curve[cite: 1].
    *   `points`: A list of Point3d coordinates[cite: 1].
    *   `value_a`: The start of the target domain[cite: 1].
    *   `value_b`: The end of the target domain[cite: 1].
*   **Outputs:**
    *   `remapped_values`: The list of mapped distance values[cite: 1].
*   **Logic:** Uses `curve.ClosestPoint()` to measure the exact distance from each point to the nearest location on the curve[cite: 1]. It establishes a min/max domain from these calculated distances and linearly interpolates them into the new target boundary values[cite: 1].

### `ValRemapPt.py`
*   **Description:** Remaps the distance between a list of points and a single attractor point to a new domain[cite: 1].
*   **Inputs:**
    *   `attractor`: The attractor Point3d[cite: 1].
    *   `points`: A list of Point3d coordinates[cite: 1].
    *   `value_a`: The start of the target domain[cite: 1].
    *   `value_b`: The end of the target domain[cite: 1].
*   **Outputs:**
    *   `remapped_values`: The list of mapped distance values[cite: 1].
*   **Logic:** Measures point-to-point distances between the list and the single attractor, constructs the original domain from those extents, and remaps them using linear interpolation[cite: 1].

---

## 7. Pattern
Scripts focused on generating complex organic and geometric patterns, heavily utilizing Voronoi math.

### `PattGen.py`
*   **Description:** Generates custom Voronoi patterns within grid cells utilizing parallel multi-threading for maximum speed[cite: 1].
*   **Inputs:**
    *   `grid_cells`: A list of base cell curves[cite: 1].
    *   `inner_scale`: A float between 0 and 1 defining the scaled inner cell[cite: 1].
    *   `eval_outer`: A float evaluating a parameter on outer edges[cite: 1].
    *   `eval_inner`: A float evaluating a parameter on inner edges[cite: 1].
    *   `point_toggle`: A 7-item list of booleans activating specific generation points[cite: 1].
*   **Outputs:**
    *   `pattern_curves`: A DataTree of generated Voronoi curves[cite: 1].
*   **Logic:** The script utilizes `System.Threading.Tasks.Parallel.For` to process grid cells simultaneously across all CPU cores, pre-allocating an empty list to prevent memory locking[cite: 1]. Based on the 7-bit toggle, it selectively generates points at the cell's centroid, outer segment midpoints/vertices/evaluated lengths, and scaled inner segment midpoints/vertices/evaluated lengths[cite: 1]. It generates a localized Voronoi pattern using these points, and trims them against the cell boundary utilizing topological math checks (`PlanarClosedCurveRelationship`) instead of slower boolean intersections where possible[cite: 1].

### `PattSel.py`
*   **Description:** Selects a valid 7-bit combination pattern based on an index[cite: 1].
*   **Inputs:**
    *   `index`: An integer representing the target combination[cite: 1].
*   **Outputs:**
    *   `values`: A 7-item list of numbers (0s and 1s)[cite: 1].
*   **Logic:** Uses `itertools.product` to generate all possible 7-bit arrays of 0s and 1s[cite: 1]. It automatically filters out any arrays that contain fewer than two 1s (since Voronoi requires at least two points to generate), and selects the combination matching the user index[cite: 1].

### `PattSelUtil.py`
*   **Description:** A utility component to easily generate a 7-item boolean toggle list for the `PattGen.py` component[cite: 1].
*   **Inputs:**
    *   7 separate boolean toggles corresponding to different point generators (e.g., centroid, outer midpoints, inner evaluated points)[cite: 1].
*   **Outputs:**
    *   `point_toggle`: A structured 7-item list of booleans[cite: 1].
*   **Logic:** Safely evaluates each user input, defaults any unwired inputs to False, and combines them into the strict 7-item array sequence required by the `PattGen` logic[cite: 1].

### `VorGrid.py`
*   **Description:** Generates Voronoi cells by randomly evaluating normalized coordinates within a set of grid surfaces[cite: 1].
*   **Inputs:**
    *   `grid_cells`: A list of surfaces, breps, or closed curves[cite: 1].
    *   `boundary`: A bounding region curve to clip the final pattern[cite: 1].
    *   `min_eval`: A float defining the minimum random evaluation (0 to 1)[cite: 1].
    *   `max_eval`: A float defining the maximum random evaluation (0 to 1)[cite: 1].
    *   `seed`: An integer for random number generation[cite: 1].
*   **Outputs:**
    *   `voronoi_cells`: A list of the generated Voronoi cell curves[cite: 1].
*   **Logic:** The script is built with robust geometry handling, dynamically creating surfaces if curves or breps are passed[cite: 1]. It extracts the U and V domains of each surface and generates random floating-point values between the min and max limits to plot UV coordinates on the faces[cite: 1]. These evaluated points are fed into the Grasshopper Voronoi generator and clipped against the bounding box of the input region[cite: 1].

---

## 8. Signage
Scripts utilized for the specific fabrication of architectural signage systems.

### `SignMaker.py`
*   **Description:** Generates solid commercial signage channel letters with standoff parameters and distinct illumination faces[cite: 1].
*   **Inputs:**
    *   `curves`: A list of base geometry curves or surfaces[cite: 1].
    *   `sidewall_depth`: A float for the extrusion depth of the sign body[cite: 1].
    *   `standoff_distance`: A float representing the mount distance off the wall[cite: 1].
    *   `illumination`: An integer toggle (0 = None, 1 = Front lit, 2 = Reverse lit)[cite: 1].
*   **Outputs:**
    *   `curves`: The parsed base sign curves[cite: 1].
    *   `body`: A list of extruded and capped solid Breps[cite: 1].
    *   `faces`: A list of Brep surfaces representing the illuminated lenses[cite: 1].
*   **Logic:** The script parses mixed inputs (curves or surfaces) into standardized planar breps to properly resolve internal geometries (such as the hole in the letter 'O')[cite: 1]. It offsets the base surface by the standoff distance, extrudes sidewalls by the depth parameter, and joins everything into a closed solid[cite: 1]. Depending on the illumination state, it duplicates a face and translates it exactly 1/32" above the front face (front lit) or 1/32" below the back face (reverse lit) to serve as the acrylic lens surface[cite: 1].

---

## 9. Utility
Helper scripts for data tree management and advanced Grasshopper operations.

### `ClusterCrack.cs` (C#)
*   **Description:** A C# utility script that forces a new password onto locked Grasshopper clusters[cite: 1].
*   **Inputs:**
    *   `ClusterName`: A string representing the nickname of the cluster[cite: 1].
    *   `NewPassword`: A string for the new password[cite: 1].
    *   `Run`: A boolean toggle[cite: 1].
*   **Outputs:**
    *   `Report`: A text output detailing success or failure messages[cite: 1].
*   **Logic:** The script locates a specified or actively selected `GH_Cluster` on the canvas[cite: 1]. It utilizes `System.Reflection` to access the protected `m_password` private field of the cluster class[cite: 1]. It creates a temporary cluster instance, invokes the `AssignNewPassword` method to generate the required encrypted byte array, and writes those bytes directly into the target locked cluster before forcing a solution expiration to refresh the canvas[cite: 1].

### `DataGate.py`
*   **Description:** Acts as a data gate to either allow streams to pass or completely block them[cite: 1].
*   **Inputs:**
    *   `toggle`: A boolean determining the gate status[cite: 1].
    *   `data`: The incoming data stream[cite: 1].
*   **Outputs:**
    *   `out_data`: The data stream, or an empty DataTree[cite: 1].
*   **Logic:** Evaluates the toggle boolean[cite: 1]. If true, the data is assigned to the output unchanged[cite: 1]. If false, the script explicitly instantiates and outputs an empty Grasshopper DataTree, effectively killing the data stream[cite: 1].

### `StrSort.py`
*   **Description:** Sorts strings naturally instead of strictly alphabetically (e.g., ensuring "2" comes before "10")[cite: 1].
*   **Inputs:**
    *   `values`: A list of strings[cite: 1].
*   **Outputs:**
    *   `sorted_values`: A list of naturally sorted strings[cite: 1].
*   **Logic:** Utilizes the Python `re` (regex) module to parse strings into chunks, checking if characters are digits and casting them as integers before using Python's native `sorted()` function[cite: 1].