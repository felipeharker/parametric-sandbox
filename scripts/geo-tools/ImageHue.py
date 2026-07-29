import System.Drawing as sd

def get_image_values(image_path, pts):
    if not image_path or not pts:
        return []
        
    # 1. Load the image into memory
    try:
        bmp = sd.Bitmap(image_path)
    except Exception as e:
        print("Error loading image: " + str(e))
        return []
        
    # Max pixel indices
    w = bmp.Width - 1
    h = bmp.Height - 1
    
    # 2. Find the bounding extents of the points (Auto-reparameterization)
    min_x = min([p.X for p in pts])
    max_x = max([p.X for p in pts])
    min_y = min([p.Y for p in pts])
    max_y = max([p.Y for p in pts])
    
    range_x = max_x - min_x
    range_y = max_y - min_y
    
    # Prevent division by zero if points form a flat line
    if range_x == 0: range_x = 1.0
    if range_y == 0: range_y = 1.0

    values = []
    
    # 3. Evaluate each point
    for pt in pts:
        # Map point coordinates to a 0.0 - 1.0 domain based on the bounding box
        norm_x = (pt.X - min_x) / range_x
        norm_y = (pt.Y - min_y) / range_y
        
        # Map the 0.0 - 1.0 domain to the actual image pixel grid
        # Note: Y is inverted (1.0 - norm_y) because image origins (0,0) are top-left, 
        # while Rhino's origin is bottom-left.
        px = int(norm_x * w)
        py = int((1.0 - norm_y) * h)
        
        # Clamp values just in case float rounding pushes them out of bounds
        px = max(0, min(px, w))
        py = max(0, min(py, h))
        
        # Get the color at that pixel
        color = bmp.GetPixel(px, py)
        
        # Calculate standard Luminance (0.0 = pure black, 1.0 = pure white)
        luminance = (0.299 * color.R + 0.587 * color.G + 0.114 * color.B) / 255.0
        values.append(luminance)
        
    # Free up memory (crucial for Grasshopper to prevent memory leaks)
    bmp.Dispose() 
    
    return values

# --- Main Execution ---
if ImagePath and Points:
    Values = get_image_values(ImagePath, Points)